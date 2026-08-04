"""InstagramClient 단위 테스트 — 네트워크 없음 (httpx.MockTransport 주입).

검증 항목 (SPEC-THREADS-POSTER-INSTAGRAM-001 M2):
  (a) create_container 가 IMAGE/VIDEO/REELS 각각 올바른 파라미터를 송신 (Facebook Login host)
  (b) IMAGE 의 .png URL → ValueError (Instagram 은 JPEG-only, Threads 와 상이)
  (c) publish 가 /media_publish 엔드포인트 + creation_id 호출
  (d) get_container_status / wait_until_finished 폴링 (IN_PROGRESS → FINISHED, EXPIRED/ERROR 예외)
  (e) 4xx 응답이 InstagramAPIError 로 파싱 (ThreadsAPIError 와 동일 필드 세트)
  (f) 클라이언트 구성 검증 (access_token / ig_user_id 필수, Facebook host)
  (g) comments/insights 메서드 노출 + @MX:TODO 엔드포인트 검증 부채 기록
"""

from __future__ import annotations

import inspect

import httpx
import pytest

from threads_poster.instagram_api import (
    DEFAULT_BASE_URL,
    GRAPH_API_VERSION,
    InstagramAPIError,
    InstagramClient,
)


def _make_client(handler, base_url=DEFAULT_BASE_URL) -> InstagramClient:
    """가짜 transport 를 주입한 InstagramClient 생성 (inject a fake transport)."""
    transport = httpx.MockTransport(handler)
    http = httpx.Client(transport=transport)
    return InstagramClient(
        access_token="tok",
        ig_user_id="IGID",
        base_url=base_url,
        client=http,
    )


# --- (a) create_container 파라미터 ----------------------------------------------
def test_create_container_image_sends_correct_params():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler)
    cid = client.create_container("IMAGE", image_url="https://example.com/p.jpg", text="캡션")
    assert cid == "C1"

    req = captured[0]
    assert req.method == "POST"
    assert req.url.host == "graph.facebook.com"
    assert req.url.path == f"/{GRAPH_API_VERSION}/IGID/media"
    q = dict(req.url.params)
    assert q["media_type"] == "IMAGE"
    assert q["image_url"] == "https://example.com/p.jpg"
    assert q["text"] == "캡션"
    assert q["access_token"] == "tok"
    assert "video_url" not in q


def test_create_container_video_sends_correct_params():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C2"})

    client = _make_client(handler)
    cid = client.create_container("VIDEO", video_url="https://example.com/v.mp4")
    assert cid == "C2"

    q = dict(captured[0].url.params)
    assert q["media_type"] == "VIDEO"
    assert q["video_url"] == "https://example.com/v.mp4"
    assert "image_url" not in q


def test_create_container_reels_with_share_to_feed():
    """AC-M2-6: REELS 생성 시 media_type=REELS + video_url + share_to_feed 포함."""
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C3"})

    client = _make_client(handler)
    client.create_container("REELS", video_url="https://example.com/r.mp4", share_to_feed=True)

    q = dict(captured[0].url.params)
    assert q["media_type"] == "REELS"
    assert q["video_url"] == "https://example.com/r.mp4"
    assert q["share_to_feed"] == "true"


def test_create_container_reels_share_to_feed_false_emitted():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C9"})

    client = _make_client(handler)
    client.create_container("REELS", video_url="https://example.com/r.mp4", share_to_feed=False)
    assert dict(captured[0].url.params)["share_to_feed"] == "false"


# --- (b) PNG 거부 (JPEG-only) ---------------------------------------------------
def test_create_container_png_rejected():
    """AC-M2-5 / EC-1: .png URL → ValueError (Instagram 은 JPEG-only)."""
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="JPEG"):
        client.create_container("IMAGE", image_url="https://example.com/p.png")


def test_create_container_jpg_allowed():
    """JPEG URL 은 통과 (휴리스틱 빠른 실패가 JPEG 를 막지 않는다)."""
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler)
    client.create_container("IMAGE", image_url="https://example.com/p.jpeg")
    assert dict(captured[0].url.params)["image_url"] == "https://example.com/p.jpeg"


def test_create_container_image_requires_image_url():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="image_url"):
        client.create_container("IMAGE")


def test_create_container_video_requires_video_url():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="video_url"):
        client.create_container("VIDEO")


def test_create_container_reels_requires_video_url():
    """EC-2: REELS 인데 video_url 없으면 ValueError."""
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="video_url"):
        client.create_container("REELS")


def test_create_container_rejects_text_media_type():
    """Instagram 은 TEXT-only 게시가 없다 (캡션은 미디어에 붙음)."""
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="unsupported media_type"):
        client.create_container("TEXT", text="hi")


def test_create_container_rejects_unknown_media_type():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="unsupported media_type"):
        client.create_container("GIF")


# --- (c) publish ----------------------------------------------------------------
def test_publish_calls_media_publish_with_creation_id():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "M1"})

    client = _make_client(handler)
    mid = client.publish("C1")
    assert mid == "M1"

    req = captured[0]
    assert req.method == "POST"
    assert req.url.path == f"/{GRAPH_API_VERSION}/IGID/media_publish"
    q = dict(req.url.params)
    assert q["creation_id"] == "C1"
    assert q["access_token"] == "tok"


def test_publish_requires_creation_id():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "M"}))
    with pytest.raises(ValueError, match="creation_id"):
        client.publish("")


# --- (d) container status / 폴링 ------------------------------------------------
def test_get_container_status_returns_status_code():
    def handler(req):
        return httpx.Response(200, json={"status_code": "FINISHED"})

    client = _make_client(handler)
    assert client.get_container_status("C1") == "FINISHED"


def test_wait_until_finished_returns_on_first_finished():
    """한 번에 FINISHED → sleeper 호출 없이 즉시 반환."""
    calls = {"status": 0, "sleeps": 0}

    def handler(req):
        calls["status"] += 1
        return httpx.Response(200, json={"status_code": "FINISHED"})

    def fake_sleep(_secs):
        calls["sleeps"] += 1

    client = _make_client(handler)
    result = client.wait_until_finished("C1", poll_interval=0, timeout=300, sleeper=fake_sleep)
    assert result == "FINISHED"
    assert calls["status"] == 1
    assert calls["sleeps"] == 0


def test_wait_until_finished_polls_then_succeeds():
    """AC-M2-7: IN_PROGRESS×2 → FINISHED. sleeper 정확히 2회 호출."""
    seq = ["IN_PROGRESS", "IN_PROGRESS", "FINISHED"]
    calls = {"status": 0, "sleeps": 0}

    def handler(req):
        i = calls["status"]
        calls["status"] += 1
        return httpx.Response(200, json={"status_code": seq[i]})

    def fake_sleep(_secs):
        calls["sleeps"] += 1

    client = _make_client(handler)
    result = client.wait_until_finished("C1", poll_interval=0, timeout=300, sleeper=fake_sleep)
    assert result == "FINISHED"
    assert calls["status"] == 3
    assert calls["sleeps"] == 2  # IN_PROGRESS 두 번 → sleep 두 번


def test_wait_until_finished_raises_on_expired():
    """AC-M2-8 / EC-4: EXPIRED → InstagramAPIError (메시지에 EXPIRED)."""
    def handler(req):
        return httpx.Response(200, json={"status_code": "EXPIRED"})

    client = _make_client(handler)
    with pytest.raises(InstagramAPIError, match="EXPIRED"):
        client.wait_until_finished("C1", poll_interval=0, timeout=300)


def test_wait_until_finished_raises_on_error_status():
    def handler(req):
        return httpx.Response(200, json={"status_code": "ERROR"})

    client = _make_client(handler)
    with pytest.raises(InstagramAPIError, match="ERROR"):
        client.wait_until_finished("C1", poll_interval=0, timeout=300)


def test_wait_until_finished_timeout_raises():
    """EC-3: IN_PROGRESS 지속 + 폴링 예산 소진 → 타임아웃 예외."""
    def handler(req):
        return httpx.Response(200, json={"status_code": "IN_PROGRESS"})

    client = _make_client(handler)
    with pytest.raises(InstagramAPIError, match="timeout|타임아웃"):
        client.wait_until_finished("C1", poll_interval=0, timeout=0.0)


# --- (e) 4xx → InstagramAPIError ------------------------------------------------
def test_4xx_raises_instagram_api_error_with_parsed_fields():
    """AC-M2-9: ThreadsAPIError 와 동일 필드 세트 (status/message/type/code)."""
    def handler(req):
        return httpx.Response(
            403,
            json={"error": {"message": "perm", "type": "OAuthException", "code": 10}},
        )

    client = _make_client(handler)
    with pytest.raises(InstagramAPIError) as exc:
        client.create_container("IMAGE", image_url="https://example.com/p.jpg")
    assert exc.value.status == 403
    assert exc.value.error_message == "perm"
    assert exc.value.error_type == "OAuthException"
    assert exc.value.error_code == 10
    assert "perm" in str(exc.value)


def test_5xx_raises_instagram_api_error():
    client = _make_client(lambda req: httpx.Response(500, json={"error": {"message": "boom"}}))
    with pytest.raises(InstagramAPIError) as exc:
        client.publish("C1")
    assert exc.value.status == 500


def test_non_json_error_body_still_raises():
    client = _make_client(lambda req: httpx.Response(502, text="Bad Gateway"))
    with pytest.raises(InstagramAPIError) as exc:
        client.get_profile()
    assert exc.value.status == 502


# --- (f) 클라이언트 구성 ---------------------------------------------------------
def test_client_requires_access_token():
    with pytest.raises(ValueError, match="access_token"):
        InstagramClient(access_token="", ig_user_id="IGID")


def test_client_requires_ig_user_id():
    with pytest.raises(ValueError, match="ig_user_id"):
        InstagramClient(access_token="tok", ig_user_id="")


def test_facebook_host_not_threads():
    """AC-M2-3: 호스트가 graph.facebook.com (graph.threads.com 아님)."""
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler)
    client.create_container("IMAGE", image_url="https://example.com/p.jpg")
    assert captured[0].url.host == "graph.facebook.com"
    assert captured[0].url.host != "graph.threads.com"


def test_custom_base_url_used():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler, base_url="https://example.test/v99")
    client.create_container("IMAGE", image_url="https://example.com/p.jpg")
    assert captured[0].url.host == "example.test"
    assert captured[0].url.path == "/v99/IGID/media"


def test_injected_client_not_closed():
    """AC-M2-1: 주입한 httpx.Client 는 close() 로 닫지 않는다 (호출자 소유)."""
    http = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"id": "x"})))
    client = InstagramClient(access_token="tok", ig_user_id="IGID", client=http)
    client.close()
    # 주입한 클라이언트는 여전히 살아있어야 한다 (is_closed False)
    assert http.is_closed is False
    http.close()


def test_context_manager_closes_owned_client():
    """기본 클라이언트를 직접 만든 경우 __exit__ 가 닫는다."""
    client = InstagramClient(access_token="tok", ig_user_id="IGID")
    owned = client._http
    with client:
        pass
    assert owned.is_closed is True


def test_published_method_surface():
    """AC-M2-1: ThreadsClient 대칭 메서드 세트 노출."""
    client = InstagramClient(access_token="tok", ig_user_id="IGID")
    for name in (
        "create_container", "publish", "get_container_status",
        "wait_until_finished", "get_profile", "refresh_token",
        "get_publish_limit", "comments_list", "comments_reply",
        "comments_hide", "insights", "close", "__enter__", "__exit__",
    ):
        assert hasattr(client, name), f"missing method: {name}"
    client.close()


# --- (g) get_profile / get_publish_limit / refresh_token -----------------------
def test_get_profile_returns_fields():
    def handler(req):
        return httpx.Response(
            200,
            json={"username": "goos", "id": "IGID", "followers_count": 42, "media_count": 7},
        )

    client = _make_client(handler)
    prof = client.get_profile()
    assert prof["username"] == "goos"
    assert prof["followers_count"] == 42


def test_get_publish_limit_returns_quota():
    def handler(req):
        return httpx.Response(
            200,
            json={"data": [{"quota_usage": 12, "config": {"quota_total": 25}}]},
        )

    client = _make_client(handler)
    limit = client.get_publish_limit()
    # 클라이언트는 Meta 의 원본 봉투를 그대로 반환한다 (runner 가 data[0] 를 해석).
    assert isinstance(limit, dict)
    assert limit["data"][0]["quota_usage"] == 12


def test_refresh_token_returns_new_token():
    """Facebook Page 장기 토큰 갱신 — 엔드포인트 경로는 run-phase 검증 대상(@MX:TODO).

    본 테스트는 *반환 파싱* 만 검증한다 (특정 엔드포인트 경로를 사실로 단정하지 않는다).
    """
    def handler(req):
        return httpx.Response(200, json={"access_token": "newlong"})

    client = _make_client(handler)
    tok = client.refresh_token()
    assert tok == "newlong"


# --- (h) comments/insights 메서드 + @MX:TODO 부채 기록 (AC-M2-10) ----------------
def test_comments_insights_methods_present():
    client = InstagramClient(access_token="tok", ig_user_id="IGID")
    for name in ("comments_list", "comments_reply", "comments_hide", "insights"):
        assert callable(getattr(client, name))
    client.close()


def test_comments_insights_methods_carry_mx_todo():
    """AC-M2-10: comments_list/reply/hide/insights 각각 @MX:TODO 마커를 가져야 한다."""
    import threads_poster.instagram_api as mod

    src = inspect.getsource(mod)
    # 각 메서드 이름 근처에 @MX:TODO 가 있는지 확인 (메서드별 최소 한 개).
    for method in ("comments_list", "comments_reply", "comments_hide", "insights"):
        # 메서드 정의 이후부터 다음 def 전까지의 라인 블록에서 @MX:TODO 탐색.
        lines = src.splitlines()
        start = next(i for i, ln in enumerate(lines) if f"def {method}(" in ln)
        end = next(
            (i for i, ln in enumerate(lines[start + 1:], start=start + 1)
             if ln.startswith("    def ") and not ln.strip().startswith("def ")),
            len(lines),
        )
        block = "\n".join(lines[start:end])
        assert "@MX:TODO" in block, (
            f"{method} 에 @MX:TODO 엔드포인트 검증 부채 마커가 없다 (AC-M2-10)"
        )
