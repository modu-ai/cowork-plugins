"""
NaverCommerceClient 테스트 — 네트워크 없이 FakeSession 으로
토큰 캐싱·401 GW.AUTHN 재시도·에러 처리를 검증한다.
"""
from __future__ import annotations

from typing import Any

import bcrypt
import pytest

from moai_mcp_smartstore.client import NaverCommerceClient
from moai_mcp_smartstore.config import Config
from moai_mcp_smartstore.errors import ApiError, AuthError

# 운영 client_secret 은 bcrypt.gensalt() 로 만들어진 진짜 bcrypt salt 이다.
# 공식 인증 문서 예시의 placeholder `$2a$10$abcdefghijklmnopqrstuv` 는
# bcrypt 4.x 까지는 수용되었으나 bcrypt 5.x 가 "Invalid salt" 로 거부한다.
# (재현 함정의 자세한 배경은 tests/test_auth.py 의
#  test_official_doc_example_salt_is_rejected_by_bcrypt5 참조.)
# 따라서 본 테스트는 운영 환경과 동일하게 진짜 salt 를 생성해 사용한다.
_SALT = bcrypt.gensalt(rounds=10, prefix=b"2a").decode("utf-8")


class FakeResponse:
    def __init__(
        self,
        status_code: int,
        json_body: Any = None,
        text: str = "",
    ) -> None:
        self.status_code = status_code
        self._json = json_body
        if text:
            self.text = text
        elif json_body is not None:
            self.text = str(json_body)
        else:
            self.text = ""
        self.content = self.text.encode("utf-8") if self.text else b""

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    def json(self) -> Any:
        if self._json is None:
            raise ValueError("no json body")
        return self._json


class FakeSession:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self._queue: list[FakeResponse] = []

    def queue(self, resp: FakeResponse) -> None:
        self._queue.append(resp)

    def _next(self, method: str, url: str, **kw: Any) -> FakeResponse:
        self.calls.append((method, url, kw))
        assert self._queue, f"no queued response for {method} {url}"
        return self._queue.pop(0)

    def post(self, url: str, **kw: Any) -> FakeResponse:
        return self._next("POST", url, **kw)

    def request(self, method: str, url: str, **kw: Any) -> FakeResponse:
        return self._next(method, url, **kw)


def _cfg(type_: str = "SELF", account_id: str = "") -> Config:
    return Config(
        client_id="cid",
        client_secret=_SALT,
        account_id=account_id,
        type=type_,
        base_url="https://api.commerce.naver.com/external",
        timeout=10.0,
    )


def _client(session: FakeSession, type_: str = "SELF", account_id: str = ""):
    return NaverCommerceClient(_cfg(type_, account_id), session=session)


def test_get_token_caches_between_calls():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "tok1", "expires_in": 3600}))
    c = _client(s)

    assert c.get_token() == "tok1"
    assert c.get_token() == "tok1"  # 캐시 hit

    token_posts = [x for x in s.calls if x[0] == "POST"]
    assert len(token_posts) == 1  # 토큰 발급은 1회만


def test_get_token_force_refresh():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "t1", "expires_in": 3600}))
    s.queue(FakeResponse(200, {"access_token": "t2", "expires_in": 3600}))
    c = _client(s)

    assert c.get_token() == "t1"
    assert c.get_token(force=True) == "t2"


def test_token_request_form_includes_signature_and_type():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "tok", "expires_in": 3600}))
    c = _client(s, type_="SELLER", account_id="acct-123")

    c.get_token()

    token_post = s.calls[0]
    form = token_post[2]["data"]
    assert form["client_id"] == "cid"
    assert form["grant_type"] == "client_credentials"
    assert form["type"] == "SELLER"
    assert form["account_id"] == "acct-123"
    assert "client_secret_sign" in form
    # 원문 client_secret 는 절대 전송되지 않는다.
    assert "client_secret" not in form


def test_request_attaches_bearer_and_returns_json():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "tok", "expires_in": 3600}))
    s.queue(FakeResponse(200, {"data": [{"id": 1}]}))
    c = _client(s)

    data = c.request("GET", "/v1/categories")
    assert data == {"data": [{"id": 1}]}

    domain_call = s.calls[1]
    headers = domain_call[2]["headers"]
    assert headers["Authorization"] == "Bearer tok"


def test_request_retries_once_on_gw_authn_then_succeeds():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "old", "expires_in": 3600}))
    s.queue(FakeResponse(401, {"code": "GW.AUTHN", "message": "expired"}))
    s.queue(FakeResponse(200, {"access_token": "new", "expires_in": 3600}))
    s.queue(FakeResponse(200, {"ok": True}))
    c = _client(s)

    data = c.request("GET", "/v1/seller/account")
    assert data == {"ok": True}
    # 재발급 후 새 토큰 사용
    assert c.get_token() == "new"


def test_request_does_not_retry_on_non_gwauthn_401():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "tok", "expires_in": 3600}))
    s.queue(FakeResponse(401, {"code": "GW.AUTHZ", "message": "forbidden"}))
    c = _client(s)

    with pytest.raises(ApiError) as ei:
        c.request("GET", "/v1/seller/account")
    assert ei.value.status_code == 401
    # 재시도 없이 도메인 호출 1회만
    domain_calls = [x for x in s.calls if x[1].endswith("/v1/seller/account")]
    assert len(domain_calls) == 1


def test_request_raises_apierror_on_5xx():
    s = FakeSession()
    s.queue(FakeResponse(200, {"access_token": "tok", "expires_in": 3600}))
    s.queue(FakeResponse(500, {"code": "INTERNAL", "message": "boom"}))
    c = _client(s)

    with pytest.raises(ApiError) as ei:
        c.request("GET", "/v1/seller/account")
    assert ei.value.status_code == 500


def test_token_issuance_failure_raises_autherror():
    s = FakeSession()
    s.queue(FakeResponse(400, {"error": "invalid_client"}))
    c = _client(s)

    with pytest.raises(AuthError):
        c.get_token()


def test_token_without_access_token_raises_autherror():
    s = FakeSession()
    s.queue(FakeResponse(200, {"unexpected": True}))
    c = _client(s)

    with pytest.raises(AuthError):
        c.get_token()
