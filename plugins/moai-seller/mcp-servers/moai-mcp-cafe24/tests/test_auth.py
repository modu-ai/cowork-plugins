"""토큰 갱신 — 회전 대응이 핵심이다.

카페24는 갱신할 때마다 리프레시 토큰을 바꾸고 이전 것을 즉시 무효화한다. 새 값을
저장하지 못하면 다음 실행에서 인증이 영구 실패한다. 이 파일은 그 경로를 지킨다.
"""

from __future__ import annotations

from dataclasses import replace

import pytest
import respx
from httpx import Response

from moai_mcp_cafe24._base import _load_persisted_tokens, _persist_tokens
from moai_mcp_cafe24.auth import Cafe24AuthError, refresh_access_token

TOKEN_URL = "https://testmall.cafe24api.com/api/v2/oauth/token"


@respx.mock
def test_회전된_리프레시_토큰을_반환하고_저장한다(cfg):
    """이것이 카페24 연동의 생명줄이다."""
    respx.post(TOKEN_URL).mock(
        return_value=Response(
            200, json={"access_token": "새액세스", "refresh_token": "새리프레시"}
        )
    )

    pair = refresh_access_token(cfg)

    assert pair.access_token == "새액세스"
    assert pair.refresh_token == "새리프레시"
    # 파일에도 남아야 다음 프로세스가 이어받는다
    assert _load_persisted_tokens(cfg.token_file) == ("새액세스", "새리프레시")


@respx.mock
def test_표준_snake_case_키로_요청한다(cfg):
    route = respx.post(TOKEN_URL).mock(return_value=Response(200, json={"access_token": "a"}))
    refresh_access_token(cfg)

    body = route.calls[0].request.content.decode()
    assert "grant_type=refresh_token" in body
    assert "refresh_token=rtok" in body


@respx.mock
def test_basic_인증_헤더를_함께_보낸다(cfg):
    route = respx.post(TOKEN_URL).mock(return_value=Response(200, json={"access_token": "a"}))
    refresh_access_token(cfg)

    assert route.calls[0].request.headers["Authorization"].startswith("Basic ")


@respx.mock
def test_회전_토큰을_생략하면_기존_값을_유지한다(cfg):
    """예기치 않은 응답에도 연동이 끊기지 않게 한다."""
    respx.post(TOKEN_URL).mock(return_value=Response(200, json={"access_token": "a"}))

    assert refresh_access_token(cfg).refresh_token == "rtok"


@respx.mock
def test_갱신_거부는_Cafe24AuthError(cfg):
    """호출부(client.py)가 기대하는 예외 타입을 유지해야 한다."""
    respx.post(TOKEN_URL).mock(return_value=Response(400, json={"error": "invalid_grant"}))

    with pytest.raises(Cafe24AuthError) as err:
        refresh_access_token(cfg)
    assert "README.md" in str(err.value)


def test_자격증명이_없으면_요청_전에_막는다(cfg):
    with pytest.raises(Cafe24AuthError):
        refresh_access_token(replace(cfg, refresh_token=""))


def test_저장_실패는_경고를_남기되_예외는_아니다(tmp_path, capsys):
    """조용히 실패하면 다음 실행의 인증 실패가 '리프레시 만료'로 오진된다."""
    blocker = tmp_path / "blocked"
    blocker.write_text("파일", encoding="utf-8")

    _persist_tokens(blocker / "t.json", "a", "r")  # 예외 없이 통과

    warning = capsys.readouterr().err
    assert "WARN" in warning
    assert "회전된 refresh token" in warning


def test_저장에_성공하면_경고가_없다(tmp_path, capsys):
    _persist_tokens(tmp_path / "t.json", "a", "r")
    assert capsys.readouterr().err == ""


def test_손상된_토큰_파일은_없는_것으로_취급한다(tmp_path):
    path = tmp_path / "t.json"
    path.write_text("{깨진 JSON", encoding="utf-8")
    assert _load_persisted_tokens(path) == (None, None)
