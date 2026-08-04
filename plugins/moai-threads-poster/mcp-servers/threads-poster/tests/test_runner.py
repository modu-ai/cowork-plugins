"""runner 단위 테스트 — 가짜 Queue + 가짜 ThreadsClient 주입 (network/DB 없음).

검증 항목 (spec cases):
  (a) creds absent → exit 0 with message (호출 스크립트 실패 처리 회피)
  (b) happy path — due 포스트 1건 발행 + mark_published
  (c) 실패 포스트 — mark_failed 하고 다음 포스트로 계속
  (d) 24h 레이트리밋 초과 → 발행 시도 없이 중단
  (e) --dry-run — 상태 변경 없이 대상만 나열
  (f) --once — 특정 post id 강제 발행
"""

from __future__ import annotations

from threads_poster import runner
from threads_poster.threads_api import ThreadsAPIError


# --- 테스트용 가짜 객체 (fakes) -------------------------------------------------
class FakeClient:
    """가짜 ThreadsClient — HTTP 없이 create_container/publish 시뮬레이션."""

    def __init__(self, *, container_id: str = "C1", media_id: str = "M1"):
        self.container_id = container_id
        self.media_id = media_id
        self.calls: list[tuple] = []

    def create_container(self, media_type, **kwargs):
        self.calls.append(("create_container", media_type, kwargs))
        return self.container_id

    def publish(self, creation_id):
        self.calls.append(("publish", creation_id))
        return self.media_id

    def close(self):
        pass


class FlakyClient(FakeClient):
    """첫 번째 create_container 만 실패하는 가짜 클라이언트 (fail-once)."""

    def __init__(self):
        super().__init__()
        self._n = 0

    def create_container(self, media_type, **kwargs):
        self._n += 1
        if self._n == 1:
            raise ThreadsAPIError(
                500, {"error": {"message": "첫 번째 실패 (first call fails)"}}
            )
        return self.container_id


class FakeQueue:
    """가짜 Queue — due/get/mark_* 호출을 기록한다."""

    def __init__(self, due_posts=None, post_by_id=None, count_24h: int = 0):
        self._due = list(due_posts or [])
        self._by_id = dict(post_by_id or {})
        self._count_24h = count_24h
        self.published: list[dict] = []
        self.failed: list[dict] = []
        self.attempts: list[int] = []

    def due(self):
        return list(self._due)

    def get(self, pid):
        return self._by_id.get(pid)

    def published_in_last_24h(self):
        return self._count_24h

    def increment_attempt(self, pid):
        self.attempts.append(pid)

    def mark_published(self, pid, *, container_id, media_id, permalink_hint=None):
        self.published.append(
            {
                "id": pid,
                "container_id": container_id,
                "media_id": media_id,
                "permalink_hint": permalink_hint,
            }
        )

    def mark_failed(self, pid, *, error):
        self.failed.append({"id": pid, "error": error})


def _post(pid: int = 1, **kw) -> dict:
    """큐 row 형태의 딕셔너리 생성 (build a queue-row-shaped dict)."""
    base = {
        "id": pid,
        "media_type": "TEXT",
        "text": "hi",
        "image_url": None,
        "video_url": None,
        "status": "APPROVED",
    }
    base.update(kw)
    return base


# --- (a) creds absent → exit 0 with message ------------------------------------
def test_main_no_creds_exits_zero_with_message(capsys, monkeypatch):
    for k in ("THREADS_ACCESS_TOKEN", "THREADS_USER_ID"):
        monkeypatch.delenv(k, raising=False)
    rc = runner.main(["--db", "/tmp/does-not-matter.db"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "THREADS_ACCESS_TOKEN" in out
    assert "THREADS_USER_ID" in out


def test_main_no_creds_does_not_build_queue(monkeypatch):
    """자격증명 없으면 큐/클라이언트 팩토리가 호출되지 않는다."""
    built = {"queue": False, "client": False}

    def _boom_queue(path):
        built["queue"] = True
        raise AssertionError("queue should not be built without creds")

    def _boom_client(tok, uid):
        built["client"] = True
        raise AssertionError("client should not be built without creds")

    monkeypatch.delenv("THREADS_ACCESS_TOKEN", raising=False)
    monkeypatch.delenv("THREADS_USER_ID", raising=False)
    monkeypatch.setattr(runner, "_build_queue", _boom_queue)
    monkeypatch.setattr(runner, "_build_client", _boom_client)
    rc = runner.main(["--db", "/tmp/x.db"])
    assert rc == 0
    assert built == {"queue": False, "client": False}


# --- (b) happy path ------------------------------------------------------------
def test_process_publishes_one_due_post():
    q = FakeQueue(due_posts=[_post(1)])
    c = FakeClient()
    result = runner._process(q, c, delay=0.0)
    assert result["published"] == 1
    assert result["failed"] == 0
    assert result["skipped"] == 0
    assert len(q.published) == 1
    assert q.published[0]["media_id"] == "M1"
    assert q.published[0]["container_id"] == "C1"
    assert 1 in q.attempts


def test_process_image_post_passes_image_url():
    q = FakeQueue(due_posts=[_post(1, media_type="IMAGE", image_url="https://x/i.png", text="캡션")])
    c = FakeClient()
    runner._process(q, c, delay=0.0)
    call = c.calls[0]
    assert call[0] == "create_container"
    assert call[1] == "IMAGE"
    assert call[2]["image_url"] == "https://x/i.png"
    assert call[2]["text"] == "캡션"


def test_process_video_post_passes_video_url():
    q = FakeQueue(due_posts=[_post(1, media_type="VIDEO", image_url=None, video_url="https://x/v.mp4")])
    c = FakeClient()
    runner._process(q, c, delay=0.0)
    call = c.calls[0]
    assert call[1] == "VIDEO"
    assert call[2]["video_url"] == "https://x/v.mp4"


# --- (c) 실패 포스트 — mark_failed 하고 계속 -----------------------------------
def test_process_failure_marks_failed_and_continues_to_next():
    q = FakeQueue(due_posts=[_post(1), _post(2)])
    c = FlakyClient()  # 첫 번째 create_container 실패, 두 번째 성공
    result = runner._process(q, c, delay=0.0)
    assert result["published"] == 1
    assert result["failed"] == 1
    assert len(q.failed) == 1
    assert q.failed[0]["id"] == 1
    assert "첫 번째 실패" in q.failed[0]["error"]
    assert len(q.published) == 1
    assert q.published[0]["id"] == 2


# --- (d) 24h 레이트리밋 초과 → 발행 시도 없이 중단 -----------------------------
def test_process_rate_limit_blocks_all_publishing():
    q = FakeQueue(due_posts=[_post(1), _post(2)], count_24h=250)
    c = FakeClient()
    result = runner._process(q, c, delay=0.0)
    assert result["published"] == 0
    assert result["failed"] == 0
    assert result["skipped"] == 2
    # 발행 시도 자체가 없었다
    assert c.calls == []
    assert q.published == []
    assert q.failed == []
    assert q.attempts == []


def test_process_rate_limit_under_threshold_publishes():
    q = FakeQueue(due_posts=[_post(1)], count_24h=249)
    c = FakeClient()
    result = runner._process(q, c, delay=0.0)
    assert result["published"] == 1


# --- (e) --dry-run -------------------------------------------------------------
def test_process_dry_run_changes_nothing():
    q = FakeQueue(due_posts=[_post(1), _post(2)])
    c = FakeClient()
    result = runner._process(q, c, dry_run=True, delay=0.0)
    assert result["published"] == 0
    assert result["failed"] == 0
    assert result["skipped"] == 2
    assert result["dry_run"] is True
    assert len(result["messages"]) == 2
    assert c.calls == []
    assert q.published == []
    assert q.failed == []
    assert q.attempts == []


# --- (f) --once ----------------------------------------------------------------
def test_process_once_publishes_specific_post():
    q = FakeQueue(post_by_id={42: _post(42)})
    c = FakeClient()
    result = runner._process(q, c, once=42, delay=0.0)
    assert result["published"] == 1
    assert len(q.published) == 1
    assert q.published[0]["id"] == 42


def test_process_once_skips_already_published():
    q = FakeQueue(post_by_id={42: _post(42, status="PUBLISHED")})
    c = FakeClient()
    result = runner._process(q, c, once=42, delay=0.0)
    assert result["published"] == 0
    assert result["skipped"] == 1
    assert c.calls == []


def test_process_once_missing_post_reports_not_found():
    q = FakeQueue()
    c = FakeClient()
    result = runner._process(q, c, once=99, delay=0.0)
    assert result["published"] == 0
    assert result["skipped"] == 0
    assert any("찾을 수 없음" in m for m in result["messages"])


def test_process_once_bypasses_rate_limit():
    """--once 는 수동 override 이므로 24h 한도 검사를 생략한다."""
    q = FakeQueue(post_by_id={42: _post(42)}, count_24h=250)
    c = FakeClient()
    result = runner._process(q, c, once=42, delay=0.0)
    assert result["published"] == 1


# --- limit 적용 ----------------------------------------------------------------
def test_process_respects_limit():
    q = FakeQueue(due_posts=[_post(i) for i in range(1, 6)])
    c = FakeClient()
    result = runner._process(q, c, limit=3, delay=0.0)
    assert result["published"] == 3


# --- 통합(boundary): 실제 Queue(tmp DB) + 실제 ThreadsClient(MockTransport) -----
def test_process_integration_real_queue_real_client(tmp_path):
    """실제 Queue row dict 모양이 _container_call 과 정확히 맞는지 검증.

    FakeQueue 가 아닌 real Queue.get/due 가 반환하는 dict 를 _process 가
    소비한다 — 스키마 필드명(media_type/text/image_url/...) 이 runner 기대치와
    일치하는지 확인한다 (boundary-verification).
    """
    import httpx

    from threads_poster.queue import Queue
    from threads_poster.threads_api import ThreadsClient

    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        # create_container 도 publish 도 같은 handler — 경로로 구분
        if "threads_publish" in req.url.path:
            return httpx.Response(200, json={"id": "M9"})
        return httpx.Response(200, json={"id": "C7"})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = ThreadsClient(access_token="tok", threads_user_id="UID", client=http)
    queue = Queue(str(tmp_path / "q.db"))

    # TEXT 포스트 1건을 enqueue → approve → _process 로 실제 발행
    pid = queue.enqueue("TEXT", text="실제 큐 통합 테스트")
    queue.approve(pid)

    result = runner._process(queue, client, delay=0.0)

    assert result["published"] == 1
    assert result["failed"] == 0
    # 실제로 create_container + publish 두 번의 HTTP 호출이 일어났다
    assert len(captured) == 2
    # DB 에 PUBLISHED 종단 상태가 기록되었다
    row = queue.get(pid)
    assert row["status"] == "PUBLISHED"
    assert row["container_id"] == "C7"
    assert row["media_id"] == "M9"
    assert row["attempts"] == 1
    queue.close()
    client.close()


def test_process_integration_mark_failed_on_api_error(tmp_path):
    """real Queue + real ThreadsClient(4xx) → mark_failed 종단 상태."""
    import httpx

    from threads_poster.queue import Queue
    from threads_poster.threads_api import ThreadsClient

    def handler(req):
        return httpx.Response(
            403, json={"error": {"message": "권한 없음", "type": "OAuthException"}}
        )

    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = ThreadsClient(access_token="tok", threads_user_id="UID", client=http)
    queue = Queue(str(tmp_path / "q.db"))
    pid = queue.enqueue("TEXT", text="실패 케이스")
    queue.approve(pid)

    result = runner._process(queue, client, delay=0.0)

    assert result["published"] == 0
    assert result["failed"] == 1
    row = queue.get(pid)
    assert row["status"] == "FAILED"
    assert "권한 없음" in row["last_error"]
    queue.close()
    client.close()
