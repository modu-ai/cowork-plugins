"""토큰 갱신 — 공통 코어 이관 후 아임웹 고유 규약이 지켜지는지 확인.

이관 전 코드가 하던 일을 그대로 하는지 검증한다. 특히 camelCase 키와 Basic 병행은
아임웹 고유 규약이라, 표준 snake_case 로 보내면 갱신이 조용히 실패한다.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
import respx
from httpx import Response

from moai_imweb._base import _load_persisted_tokens, _persist_tokens
from moai_imweb.auth import ImwebAuthError, refresh_access_token

TOKEN_URL = "https://openapi.imweb.me/oauth2/token"


@respx.mock
def test_camelCase_키로_갱신을_요청한다(cfg, tmp_path):
    """아임웹은 grantType/refreshToken/clientId/clientSecret 표기를 쓴다."""
    route = respx.post(TOKEN_URL).mock(
        return_value=Response(200, json={"accessToken": "새액세스", "refreshToken": "새리프레시"})
    )

    pair = refresh_access_token(replace(cfg, token_file=tmp_path / "t.json"))

    assert pair.access_token == "새액세스"
    assert pair.refresh_token == "새리프레시"

    body = route.calls[0].request.content.decode()
    assert "grantType=refresh_token" in body
    assert "clientId=cid" in body
    assert "grant_type=" not in body  # snake_case 로 보내면 아임웹이 못 알아듣는다


@respx.mock
def test_basic_인증_헤더를_함께_보낸다(cfg, tmp_path):
    route = respx.post(TOKEN_URL).mock(return_value=Response(200, json={"accessToken": "a"}))
    refresh_access_token(replace(cfg, token_file=tmp_path / "t.json"))

    assert route.calls[0].request.headers["Authorization"].startswith("Basic ")


@respx.mock
def test_갱신_결과가_파일에_남는다(cfg, tmp_path):
    """프로세스를 다시 켜도 최신 토큰을 이어받아야 한다."""
    path = tmp_path / "t.json"
    respx.post(TOKEN_URL).mock(
        return_value=Response(200, json={"accessToken": "a2", "refreshToken": "r2"})
    )

    refresh_access_token(replace(cfg, token_file=path))
    assert _load_persisted_tokens(path) == ("a2", "r2")


@respx.mock
def test_리프레시_토큰을_안_주면_기존_값을_유지한다(cfg, tmp_path):
    """아임웹은 회전할 수도, 안 할 수도 있다. 안 주면 쓰던 것을 계속 쓴다."""
    respx.post(TOKEN_URL).mock(return_value=Response(200, json={"accessToken": "a3"}))

    pair = refresh_access_token(replace(cfg, token_file=tmp_path / "t.json"))
    assert pair.refresh_token == "rtok"


@respx.mock
def test_갱신_거부는_ImwebAuthError(cfg, tmp_path):
    """호출부(client.py)가 기대하는 예외 타입을 유지해야 한다."""
    respx.post(TOKEN_URL).mock(return_value=Response(400, json={"error": "invalid_grant"}))

    with pytest.raises(ImwebAuthError) as err:
        refresh_access_token(replace(cfg, token_file=tmp_path / "t.json"))
    assert "CONNECTORS.md" in str(err.value)


def test_자격증명이_없으면_요청_전에_막는다(cfg):
    with pytest.raises(ImwebAuthError):
        refresh_access_token(replace(cfg, refresh_token=""))


def test_토큰_저장은_실패해도_예외를_올리지_않는다(tmp_path):
    """저장 실패가 API 호출 실패로 번지면 안 된다."""
    blocker = tmp_path / "blocked"
    blocker.write_text("파일", encoding="utf-8")

    _persist_tokens(blocker / "t.json", "a", "r")  # 예외 없이 통과해야 한다


def test_경로가_없으면_저장도_조회도_조용히_넘어간다():
    _persist_tokens(None, "a", "r")
    assert _load_persisted_tokens(None) == (None, None)
