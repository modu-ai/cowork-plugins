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


# === M3: platform dispatch (SPEC-THREADS-POSTER-INSTAGRAM-001) ====================
# AC-M3-5..M3-8 + D1.a(skip-and-continue): client_resolver 주입, 혼합 큐 분기,
# IG VIDEO/REELS 폴링, IG 레이트리밋, IG 자격증명 미설정 스킵.


class FakeInstagramClient:
    """가짜 InstagramClient — HTTP 없이 create_container/publish/wait_until_finished 시뮬레이션."""

    def __init__(self, *, container_id: str = "IGC1", media_id: str = "IGM1", quota_remaining: int = 100):
        self.container_id = container_id
        self.media_id = media_id
        self.calls: list[tuple] = []
        self._quota_remaining = quota_remaining

    def create_container(self, media_type, **kwargs):
        self.calls.append(("create_container", media_type, kwargs))
        return self.container_id

    def publish(self, creation_id):
        self.calls.append(("publish", creation_id))
        return self.media_id

    def wait_until_finished(self, creation_id, **kwargs):
        self.calls.append(("wait_until_finished", creation_id))
        return "FINISHED"

    def get_publish_limit(self):
        # Meta 봉투 형태: data[0].quota_usage / config.quota_total
        used = max(0, 100 - self._quota_remaining)
        return {"data": [{"quota_usage": used, "config": {"quota_total": 100}}]}

    def close(self):
        pass


def _ig_post(pid: int = 10, **kw) -> dict:
    """Instagram 큐 row 형태 (build an instagram queue-row dict)."""
    base = {
        "id": pid,
        "media_type": "IMAGE",
        "text": None,
        "image_url": "https://example.com/i.jpg",
        "video_url": None,
        "status": "APPROVED",
        "platform": "instagram",
    }
    base.update(kw)
    return base


def test_process_mixed_queue_dispatches_per_platform():
    """AC-M3-5: 혼합 큐 — threads row 는 ThreadsClient, instagram row 는 InstagramClient."""
    threads_client = FakeClient()
    ig_client = FakeInstagramClient()
    q = FakeQueue(due_posts=[
        _post(1, media_type="TEXT", text="threads-post"),          # platform 기본 threads
        _ig_post(2, media_type="IMAGE", image_url="https://example.com/a.jpg"),
    ])

    def resolver(platform, post):
        return threads_client if platform == "threads" else ig_client

    result = runner._process(q, client_resolver=resolver, delay=0.0)
    assert result["published"] == 2
    # threads row → ThreadsClient.create_container
    assert any(c[0] == "create_container" for c in threads_client.calls)
    # instagram row → InstagramClient.create_container
    assert any(c[0] == "create_container" for c in ig_client.calls)
    # 교차 오염 없음: threads_client 이 IG row 를, ig_client 이 threads row 를 처리하지 않았다
    # threads row 는 TEXT 이고 IG row 는 IMAGE — create_container 의 media_type 으로 구분
    threads_mts = {c[1] for c in threads_client.calls if c[0] == "create_container"}
    ig_mts = {c[1] for c in ig_client.calls if c[0] == "create_container"}
    assert threads_mts == {"TEXT"}
    assert ig_mts == {"IMAGE"}


def test_process_threads_only_queue_byte_identical_with_resolver():
    """AC-M3-6 (load-bearing): 기본 리졸버 경로도 Threads-only 큐는 기존과 동일."""
    # (1) legacy 경로 — raw client
    q1 = FakeQueue(due_posts=[_post(1), _post(2)])
    c1 = FakeClient()
    legacy = runner._process(q1, c1, delay=0.0)
    # (2) resolver 경로 — 같은 큐를 resolver 로
    q2 = FakeQueue(due_posts=[_post(1), _post(2)])
    c2 = FakeClient()
    res = runner._process(q2, client_resolver=lambda platform, post: c2, delay=0.0)
    assert res["published"] == legacy["published"] == 2
    assert res["failed"] == legacy["failed"] == 0
    assert res["skipped"] == legacy["skipped"] == 0
    # mark_published 호출 수 동일
    assert len(q1.published) == len(q2.published) == 2
    # 같은 media_id / container_id
    assert q1.published[0]["media_id"] == q2.published[0]["media_id"]


def test_process_instagram_video_triggers_wait_until_finished():
    """AC-M3-7: IG VIDEO row → wait_until_finished 가 create_container 와 publish 사이."""
    ig_client = FakeInstagramClient()
    q = FakeQueue(due_posts=[_ig_post(1, media_type="VIDEO", image_url=None, video_url="https://example.com/v.mp4")])
    runner._process(q, client_resolver=lambda p, post: ig_client, delay=0.0)
    names = [c[0] for c in ig_client.calls]
    assert "create_container" in names and "wait_until_finished" in names and "publish" in names
    assert names.index("wait_until_finished") > names.index("create_container")
    assert names.index("publish") > names.index("wait_until_finished")


def test_process_instagram_reels_triggers_wait_until_finished():
    """REELS 도 VIDEO 와 같이 폴링한다."""
    ig_client = FakeInstagramClient()
    q = FakeQueue(due_posts=[_ig_post(1, media_type="REELS", image_url=None, video_url="https://example.com/r.mp4")])
    runner._process(q, client_resolver=lambda p, post: ig_client, delay=0.0)
    names = [c[0] for c in ig_client.calls]
    assert "wait_until_finished" in names
    assert "publish" in names


def test_process_instagram_rate_limit_skips_and_continues():
    """AC-M3-8: IG quota 소진 → IG row 스킵, 발행 시도 없음, 메시지 기록."""
    ig_client = FakeInstagramClient(quota_remaining=0)  # 잔여 0
    q = FakeQueue(due_posts=[_ig_post(1, media_type="IMAGE")])
    result = runner._process(q, client_resolver=lambda p, post: ig_client, delay=0.0)
    assert result["published"] == 0
    assert result["skipped"] == 1
    # 발행 시도 자체가 없었다 (create_container/publish 미호출)
    assert ig_client.calls == []
    # 메시지에 레이트리밋 스킵 기록
    assert any("한도" in m or "rate-limit" in m.lower() or "limit" in m.lower() for m in result["messages"])


def test_process_ig_row_without_resolver_skips_with_setup_required():
    """D1.a(b): resolver 없이 raw Threads client 만 전달된 IG row → setup_required 스킵."""
    threads_client = FakeClient()
    q = FakeQueue(due_posts=[
        _post(1, media_type="TEXT", text="threads-ok"),
        _ig_post(2, media_type="IMAGE"),
    ])
    # client_resolver 없이 threads client 만 — IG row 는 row_client=None → 스킵
    result = runner._process(q, threads_client, delay=0.0)
    assert result["published"] == 1   # threads row 만 발행
    assert result["skipped"] == 1     # IG row 스킵
    # IG 스킵 메시지에 setup_required 언급
    assert any("setup_required" in m or "자격증명" in m for m in result["messages"])


def test_process_resolver_returns_none_for_ig_skips_but_continues_threads():
    """D1.a(b): resolver 가 IG creds 부재로 None 반환 → IG row 스킵, threads row 는 계속 발행."""
    threads_client = FakeClient()
    ig_calls = []

    def resolver(platform, post):
        if platform == "threads":
            return threads_client
        # instagram → None (creds 부재)
        ig_calls.append(("resolved_none", post["id"]))
        return None

    q = FakeQueue(due_posts=[
        _post(1, media_type="TEXT", text="t"),
        _ig_post(2, media_type="IMAGE"),
        _post(3, media_type="TEXT", text="t2"),
    ])
    result = runner._process(q, client_resolver=resolver, delay=0.0)
    assert result["published"] == 2   # threads row 2개 발행
    assert result["skipped"] == 1     # IG row 1개 스킵
    assert len(q.published) == 2


def test_process_permalink_differs_per_platform():
    """D4: threads 와 instagram 의 permalink 힌트가 다르다."""
    threads_client = FakeClient(media_id="TM")
    ig_client = FakeInstagramClient(media_id="IM")
    q = FakeQueue(due_posts=[
        _post(1, media_type="TEXT", text="t"),
        _ig_post(2, media_type="IMAGE"),
    ])
    runner._process(
        q,
        client_resolver=lambda p, post: threads_client if p == "threads" else ig_client,
        delay=0.0,
    )
    threads_link = q.published[0]["permalink_hint"]
    ig_link = [p for p in q.published if p["id"] == 2][0]["permalink_hint"]
    assert "threads.net" in threads_link
    assert "instagram.com" in ig_link
