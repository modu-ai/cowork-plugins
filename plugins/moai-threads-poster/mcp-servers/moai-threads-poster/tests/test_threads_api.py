"""ThreadsClient 단위 테스트 — 네트워크 없음 (httpx.MockTransport 주입).

검증 항목:
  (a) create_container 가 TEXT/IMAGE/VIDEO 각각 올바른 파라미터를 송신
  (b) 500 UTF-8 바이트 초과 시 ValueError (이모지·한글 바이트 계산 포함)
  (c) publish 가 올바른 엔드포인트/creation_id 호출
  (d) 4xx 응답이 ThreadsAPIError 로 파싱
  (e) get_profile / refresh_token 동작
  (f) 클라이언트 구성 검증 (토큰/사용자 ID 필수)
"""

from __future__ import annotations

import httpx
import pytest

from threads_poster.threads_api import (
    DEFAULT_BASE_URL,
    ThreadsAPIError,
    ThreadsClient,
)


def _make_client(handler, base_url=DEFAULT_BASE_URL) -> ThreadsClient:
    """가짜 transport 를 주입한 ThreadsClient 생성 (inject a fake transport)."""
    transport = httpx.MockTransport(handler)
    http = httpx.Client(transport=transport)
    return ThreadsClient(
        access_token="tok",
        threads_user_id="UID",
        base_url=base_url,
        client=http,
    )


# --- (a) create_container 파라미터 ----------------------------------------------
def test_create_container_text_sends_correct_params():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler)
    cid = client.create_container("TEXT", text="안녕 threads")
    assert cid == "C1"

    req = captured[0]
    assert req.method == "POST"
    assert req.url.path == "/v1.0/UID/threads"
    q = dict(req.url.params)
    assert q["media_type"] == "TEXT"
    assert q["text"] == "안녕 threads"
    assert q["access_token"] == "tok"
    assert "image_url" not in q
    assert "video_url" not in q


def test_create_container_image_sends_correct_params():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C2"})

    client = _make_client(handler)
    cid = client.create_container(
        "IMAGE", image_url="https://example.com/p.png", text="캡션"
    )
    assert cid == "C2"

    q = dict(captured[0].url.params)
    assert q["media_type"] == "IMAGE"
    assert q["image_url"] == "https://example.com/p.png"
    assert q["text"] == "캡션"
    assert "video_url" not in q


def test_create_container_video_sends_correct_params():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C3"})

    client = _make_client(handler)
    cid = client.create_container("VIDEO", video_url="https://example.com/v.mp4")
    assert cid == "C3"

    q = dict(captured[0].url.params)
    assert q["media_type"] == "VIDEO"
    assert q["video_url"] == "https://example.com/v.mp4"
    assert "image_url" not in q


def test_create_container_is_carousel_item_emitted_when_true():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C4"})

    client = _make_client(handler)
    client.create_container("IMAGE", image_url="https://example.com/i.png", is_carousel_item=True)
    assert dict(captured[0].url.params)["is_carousel_item"] == "true"


def test_create_container_image_requires_image_url():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="image_url"):
        client.create_container("IMAGE")


def test_create_container_video_requires_video_url():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="video_url"):
        client.create_container("VIDEO")


def test_create_container_rejects_unknown_media_type():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    with pytest.raises(ValueError, match="unsupported media_type"):
        client.create_container("GIF")


# --- (b) 500 UTF-8 바이트 제한 --------------------------------------------------
def test_text_over_500_bytes_raises():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    # ASCII 501자 = 501바이트 → 제한 초과
    with pytest.raises(ValueError, match="500"):
        client.create_container("TEXT", text="A" * 501)


def test_text_at_exactly_500_bytes_is_allowed():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler)
    # ASCII 500자 = 500바이트 → 경계값 통과
    cid = client.create_container("TEXT", text="A" * 500)
    assert cid == "C1"
    assert dict(captured[0].url.params)["text"] == "A" * 500


def test_text_korean_byte_count_enforced():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    # 한국어 168자 = 504바이트 → 초과 (한글 1자 = 3바이트)
    assert len(("가" * 168).encode("utf-8")) == 504
    with pytest.raises(ValueError, match="500"):
        client.create_container("TEXT", text="가" * 168)


def test_text_emoji_byte_count_enforced():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "X"}))
    # 이모지 126자 = 504바이트 → 초과 (이모지 1자 = 4바이트)
    assert len(("🚀" * 126).encode("utf-8")) == 504
    with pytest.raises(ValueError, match="500"):
        client.create_container("TEXT", text="🚀" * 126)


# --- (c) publish ----------------------------------------------------------------
def test_publish_calls_correct_endpoint_with_creation_id():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "M1"})

    client = _make_client(handler)
    mid = client.publish("C1")
    assert mid == "M1"

    req = captured[0]
    assert req.method == "POST"
    assert req.url.path == "/v1.0/UID/threads_publish"
    q = dict(req.url.params)
    assert q["creation_id"] == "C1"
    assert q["access_token"] == "tok"


def test_publish_requires_creation_id():
    client = _make_client(lambda req: httpx.Response(200, json={"id": "M"}))
    with pytest.raises(ValueError, match="creation_id"):
        client.publish("")


# --- (d) 4xx → ThreadsAPIError --------------------------------------------------
def test_4xx_raises_threads_api_error_with_parsed_error():
    def handler(req):
        return httpx.Response(
            403,
            json={"error": {"message": "권한 없음", "type": "OAuthException", "code": 190}},
        )

    client = _make_client(handler)
    with pytest.raises(ThreadsAPIError) as exc:
        client.create_container("TEXT", text="hi")
    assert exc.value.status == 403
    assert exc.value.error_type == "OAuthException"
    assert exc.value.error_code == 190
    assert "권한 없음" in str(exc.value)


def test_5xx_also_raises_threads_api_error():
    client = _make_client(lambda req: httpx.Response(500, json={"error": {"message": "boom"}}))
    with pytest.raises(ThreadsAPIError) as exc:
        client.publish("C1")
    assert exc.value.status == 500


def test_non_json_error_body_still_raises():
    client = _make_client(lambda req: httpx.Response(502, text="Bad Gateway"))
    with pytest.raises(ThreadsAPIError) as exc:
        client.get_profile()
    assert exc.value.status == 502


# --- (e) get_profile / refresh_token -------------------------------------------
def test_get_profile_returns_fields():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(
            200,
            json={"username": "goos", "id": "UID", "followers_count": 42, "profile_picture_url": "https://x/av.png"},
        )

    client = _make_client(handler)
    prof = client.get_profile()
    assert prof["username"] == "goos"
    assert prof["followers_count"] == 42

    req = captured[0]
    assert req.method == "GET"
    # 쉼표는 URL 인코딩(%2C) 되므로 디코딩된 params 에서 검증.
    q = dict(req.url.params)
    assert q["fields"] == "username,id,followers_count,profile_picture_url"
    assert q["access_token"] == "tok"


def test_refresh_token_returns_new_token():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(
            200, json={"access_token": "newlong", "token_type": "bearer", "expires_in": 5184000}
        )

    client = _make_client(handler)
    tok = client.refresh_token()
    assert tok == "newlong"
    assert dict(captured[0].url.params)["grant_type"] == "th_refresh_token"


# --- (f) 클라이언트 구성 ---------------------------------------------------------
def test_client_requires_access_token():
    with pytest.raises(ValueError, match="access_token"):
        ThreadsClient(access_token="", threads_user_id="UID")


def test_client_requires_user_id():
    with pytest.raises(ValueError, match="threads_user_id"):
        ThreadsClient(access_token="tok", threads_user_id="")


def test_custom_base_url_used():
    captured: list[httpx.Request] = []

    def handler(req):
        captured.append(req)
        return httpx.Response(200, json={"id": "C1"})

    client = _make_client(handler, base_url="https://example.test/v2")
    client.create_container("TEXT", text="hi")
    assert captured[0].url.host == "example.test"
    assert captured[0].url.path == "/v2/UID/threads"
