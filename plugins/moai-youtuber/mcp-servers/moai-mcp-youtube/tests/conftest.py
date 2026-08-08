"""테스트 공통 픽스처 — 네트워크 없이 유튜브 API를 흉내 낸다."""

from __future__ import annotations

from typing import Any, Callable

import httpx
import pytest

from moai_mcp_youtube.client import YouTubeClient
from moai_mcp_youtube.config import YouTubeConfig
from moai_mcp_youtube.quota import QuotaLedger

TOKEN_URL = "https://oauth2.googleapis.com/token"


@pytest.fixture
def config(tmp_path) -> YouTubeConfig:
    return YouTubeConfig(
        client_id="cid",
        client_secret="secret",
        refresh_token="r0",
        channel_id="UC_test",
        api_base="https://api.test/youtube/v3",
        upload_base="https://upload.test/youtube/v3",
        analytics_base="https://analytics.test/v2",
        token_file=tmp_path / "tokens.json",
        quota_file=tmp_path / "quota.json",
        daily_limit=10_000,
        search_cache_ttl=900.0,
    )


@pytest.fixture
def unconfigured(tmp_path) -> YouTubeConfig:
    """자격증명이 하나도 없는 상태."""
    return YouTubeConfig(
        client_id="",
        client_secret="",
        refresh_token="",
        channel_id="",
        api_base="https://api.test/youtube/v3",
        upload_base="https://upload.test/youtube/v3",
        analytics_base="https://analytics.test/v2",
        token_file=tmp_path / "tokens.json",
        quota_file=tmp_path / "quota.json",
        daily_limit=10_000,
        search_cache_ttl=900.0,
    )


class Recorder:
    """오간 요청을 기록하는 가짜 전송 계층."""

    def __init__(self, routes: dict[str, Any] | None = None) -> None:
        self.routes = routes or {}
        self.requests: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if str(request.url).startswith(TOKEN_URL):
            return httpx.Response(200, json={"access_token": "at", "expires_in": 3600})
        for fragment, response in self.routes.items():
            if fragment in str(request.url):
                return response(request) if callable(response) else response
        return httpx.Response(200, json={})

    @property
    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handler)

    def paths(self) -> list[str]:
        """토큰 요청을 뺀 API 경로 목록."""
        return [r.url.path for r in self.requests if not str(r.url).startswith(TOKEN_URL)]


@pytest.fixture
def recorder() -> Callable[..., Recorder]:
    return Recorder


def make_client(config: YouTubeConfig, rec: Recorder, **kw: Any) -> YouTubeClient:
    return YouTubeClient(
        config,
        transport=rec.transport,
        ledger=QuotaLedger(path=config.quota_file, daily_limit=config.daily_limit),
        sleep=lambda _s: None,
        **kw,
    )
