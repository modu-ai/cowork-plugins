"""HttpClient — 재시도·401 재인증·429·오류 매핑."""

from __future__ import annotations

import httpx
import pytest

from moai_mcp_core.errors import AuthError, RateLimited, UpstreamError
from moai_mcp_core.http import HttpClient


class _FakeAuth:
    """access_token()/force 인터페이스만 흉내 내는 토큰 공급자."""

    def __init__(self) -> None:
        self.token = "t1"
        self.force_calls = 0

    def access_token(self, *, force: bool = False) -> str:
        if force:
            self.force_calls += 1
            self.token = f"t{self.force_calls + 1}"
        return self.token


def _client(handler, **kw) -> HttpClient:
    kw.setdefault("sleep", lambda _s: None)  # 테스트에서 실제로 자지 않는다
    return HttpClient("https://api.test", transport=httpx.MockTransport(handler), **kw)


def test_성공_응답을_그대로_돌려준다():
    with _client(lambda r: httpx.Response(200, json={"ok": True})) as c:
        assert c.get_json("/v1/things") == {"ok": True}


def test_인증_헤더를_붙인다():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={})

    with _client(handler, auth=_FakeAuth()) as c:
        c.get_json("/v1/me")
    assert seen["auth"] == "Bearer t1"


def test_401이면_토큰을_강제_갱신하고_한_번_재시도한다():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(401, json={"error": "expired"})
        return httpx.Response(200, json={"ok": True})

    auth = _FakeAuth()
    with _client(handler, auth=auth) as c:
        assert c.get_json("/v1/me") == {"ok": True}
    assert auth.force_calls == 1
    assert calls["n"] == 2


def test_두_번째도_401이면_포기한다():
    """무한 재인증 루프를 막는다 — 자격증명 자체가 잘못된 경우다."""
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(401, json={"error": "revoked"})

    with _client(handler, auth=_FakeAuth()) as c, pytest.raises(AuthError):
        c.get_json("/v1/me")
    assert calls["n"] == 2


def test_429는_retry_after_만큼_기다렸다_재시도한다():
    slept: list[float] = []
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "7"})
        return httpx.Response(200, json={"ok": True})

    c = HttpClient(
        "https://api.test",
        transport=httpx.MockTransport(handler),
        sleep=slept.append,
    )
    assert c.get_json("/v1/x") == {"ok": True}
    assert slept == [7.0]


def test_429가_계속되면_rate_limited():
    c = _client(lambda r: httpx.Response(429, headers={"Retry-After": "1"}), max_retries=2)
    with pytest.raises(RateLimited) as err:
        c.get_json("/v1/x")
    assert err.value.to_dict()["retryable"] is True


def test_5xx는_재시도하고_끝내_실패하면_upstream_error():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(503, text="down")

    with _client(handler, max_retries=2) as c, pytest.raises(UpstreamError) as err:
        c.get_json("/v1/x")
    assert calls["n"] == 3  # 최초 1회 + 재시도 2회
    assert err.value.to_dict()["retryable"] is True


def test_5xx가_중간에_회복되면_성공한다():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(500)
        return httpx.Response(200, json={"ok": True})

    with _client(handler) as c:
        assert c.get_json("/v1/x") == {"ok": True}


def test_400은_재시도하지_않는다():
    """같은 요청은 같은 결과를 낸다 — 재시도가 무의미하다."""
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(400, text="bad request")

    with _client(handler) as c, pytest.raises(UpstreamError) as err:
        c.get_json("/v1/x")
    assert calls["n"] == 1
    assert err.value.to_dict()["retryable"] is False


def test_JSON이_아닌_응답은_upstream_error():
    with _client(lambda r: httpx.Response(200, text="<html>")) as c:
        with pytest.raises(UpstreamError):
            c.get_json("/v1/x")


def test_본문이_비면_None():
    with _client(lambda r: httpx.Response(204)) as c:
        assert c.get_json("/v1/x") is None


def test_오류_본문은_잘라서_담는다():
    """자격증명이 섞인 긴 본문이 통째로 로그에 남지 않게 한다."""
    with _client(lambda r: httpx.Response(400, text="x" * 5000)) as c:
        with pytest.raises(UpstreamError) as err:
            c.get_json("/v1/x")
    assert len(err.value.to_dict()["details"]["body"]) == 500
