"""OAuth2Refresher — 갱신·회전·자격증명 부재."""

from __future__ import annotations

import httpx
import pytest

from moai_mcp_core.auth import OAuth2Config, OAuth2Refresher
from moai_mcp_core.errors import AuthError, SetupRequired
from moai_mcp_core.tokenstore import TokenStore


def _config(**over):
    base = dict(
        token_url="https://example.test/token",
        client_id="cid",
        client_secret="secret",
        refresh_token="r0",
    )
    base.update(over)
    return OAuth2Config(**base)


class _Clock:
    def __init__(self, now: float = 1000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


def test_리프레시로_액세스_토큰을_받는다(tmp_path):
    def handler(request: httpx.Request) -> httpx.Response:
        assert b"grant_type=refresh_token" in request.content
        return httpx.Response(200, json={"access_token": "a1", "expires_in": 3600})

    store = TokenStore("svc", path=tmp_path / "t.json")
    ref = OAuth2Refresher(
        _config(), store, transport=httpx.MockTransport(handler), clock=_Clock()
    )
    assert ref.access_token() == "a1"
    assert store.load()["access_token"] == "a1"


def test_유효한_토큰은_다시_갱신하지_않는다(tmp_path):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json={"access_token": f"a{calls['n']}", "expires_in": 3600})

    clock = _Clock()
    ref = OAuth2Refresher(
        _config(),
        TokenStore("svc", path=tmp_path / "t.json"),
        transport=httpx.MockTransport(handler),
        clock=clock,
    )
    assert ref.access_token() == "a1"
    assert ref.access_token() == "a1"
    assert calls["n"] == 1


def test_만료가_임박하면_미리_갱신한다(tmp_path):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json={"access_token": f"a{calls['n']}", "expires_in": 100})

    clock = _Clock()
    ref = OAuth2Refresher(
        _config(leeway_seconds=60),
        TokenStore("svc", path=tmp_path / "t.json"),
        transport=httpx.MockTransport(handler),
        clock=clock,
    )
    assert ref.access_token() == "a1"

    clock.now += 50  # 만료까지 50초 — leeway 60초 안쪽이므로 갱신되어야 한다
    assert ref.access_token() == "a2"
    assert calls["n"] == 2


def test_회전된_리프레시_토큰을_저장한다(tmp_path):
    """카페24처럼 갱신 때마다 리프레시 토큰이 바뀌는 서비스 대응.

    새 토큰을 놓치면 다음 갱신이 영구 실패한다.
    """

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"access_token": "a1", "refresh_token": "r1", "expires_in": 3600},
        )

    store = TokenStore("svc", path=tmp_path / "t.json")
    ref = OAuth2Refresher(
        _config(), store, transport=httpx.MockTransport(handler), clock=_Clock()
    )
    ref.refresh()

    assert ref.refresh_token == "r1"
    assert store.load()["refresh_token"] == "r1"


def test_저장된_리프레시_토큰이_설정값보다_우선한다(tmp_path):
    """환경변수는 최초 발급값에 머물러 있고, 회전된 최신값은 파일에 있다."""
    store = TokenStore("svc", path=tmp_path / "t.json")
    store.save({"refresh_token": "회전된최신값"})

    ref = OAuth2Refresher(
        _config(refresh_token="환경변수옛값"),
        store,
        transport=httpx.MockTransport(lambda r: httpx.Response(200, json={"access_token": "a"})),
    )
    assert ref.refresh_token == "회전된최신값"


def test_자격증명이_없으면_setup_required(tmp_path):
    ref = OAuth2Refresher(
        _config(refresh_token=None, client_id=None, setup_guide="CONNECTORS.md"),
        TokenStore("svc", path=tmp_path / "t.json"),
    )
    with pytest.raises(SetupRequired) as err:
        ref.access_token()

    result = err.value.to_dict()
    assert result["error"] == "setup_required"
    assert "REFRESH_TOKEN" in result["details"]["missing_env"]
    assert "CLIENT_ID" in result["details"]["missing_env"]
    assert result["details"]["guide"] == "CONNECTORS.md"


def test_갱신_거부는_auth_error(tmp_path):
    handler = lambda r: httpx.Response(400, json={"error": "invalid_grant"})  # noqa: E731
    ref = OAuth2Refresher(
        _config(),
        TokenStore("svc", path=tmp_path / "t.json"),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(AuthError):
        ref.refresh()


def test_access_token_이_없는_응답은_auth_error(tmp_path):
    handler = lambda r: httpx.Response(200, json={"token_type": "Bearer"})  # noqa: E731
    ref = OAuth2Refresher(
        _config(),
        TokenStore("svc", path=tmp_path / "t.json"),
        transport=httpx.MockTransport(handler),
    )
    with pytest.raises(AuthError):
        ref.refresh()
