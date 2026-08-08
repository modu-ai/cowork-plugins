"""환경변수 로드 + 클라이언트 조립.

자격증명이 없어도 **서버는 뜬다.** 각 도구가 호출될 때 `setup_required` 안내를
돌려줄 뿐이다. 서버가 기동에 실패하면 사용자는 원인을 알 수 없는 연결 오류만 본다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from moai_mcp_core import OAuth2Config, OAuth2Refresher, SetupRequired, TokenStore

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE = "https://www.googleapis.com/youtube/v3"
UPLOAD_BASE = "https://www.googleapis.com/upload/youtube/v3"
ANALYTICS_BASE = "https://youtubeanalytics.googleapis.com/v2"

SETUP_GUIDE = "mcp-servers/moai-mcp-youtube/CONNECTORS.md"


@dataclass(frozen=True)
class YouTubeConfig:
    client_id: str
    client_secret: str
    refresh_token: str
    channel_id: str
    api_base: str
    upload_base: str
    analytics_base: str
    token_file: Path | None
    quota_file: Path | None
    daily_limit: int
    search_cache_ttl: float

    @property
    def configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token)

    def require(self) -> None:
        """자격증명이 없으면 안내 오류를 올린다."""
        missing = [
            name
            for name, value in (
                ("YOUTUBE_CLIENT_ID", self.client_id),
                ("YOUTUBE_CLIENT_SECRET", self.client_secret),
                ("YOUTUBE_REFRESH_TOKEN", self.refresh_token),
            )
            if not value
        ]
        if missing:
            raise SetupRequired(
                "유튜브 연동이 아직 설정되지 않았습니다. Google Cloud 에서 OAuth 클라이언트를 "
                "만들고 최초 1회 동의를 거쳐 리프레시 토큰을 발급받아야 합니다.",
                missing=missing,
                guide=SETUP_GUIDE,
            )


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ[name])
    except (KeyError, ValueError):
        return default


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.environ[name])
    except (KeyError, ValueError):
        return default


def load_config() -> YouTubeConfig:
    token_file = os.environ.get("YOUTUBE_TOKEN_FILE")
    quota_file = os.environ.get("YOUTUBE_QUOTA_FILE")
    return YouTubeConfig(
        client_id=os.environ.get("YOUTUBE_CLIENT_ID", ""),
        client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET", ""),
        refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN", ""),
        channel_id=os.environ.get("YOUTUBE_CHANNEL_ID", ""),
        api_base=os.environ.get("YOUTUBE_API_BASE", API_BASE).rstrip("/"),
        upload_base=os.environ.get("YOUTUBE_UPLOAD_BASE", UPLOAD_BASE).rstrip("/"),
        analytics_base=os.environ.get("YOUTUBE_ANALYTICS_BASE", ANALYTICS_BASE).rstrip("/"),
        token_file=Path(token_file).expanduser() if token_file else None,
        quota_file=Path(quota_file).expanduser() if quota_file else None,
        daily_limit=_int_env("YOUTUBE_DAILY_QUOTA", 10_000),
        search_cache_ttl=_float_env("YOUTUBE_SEARCH_CACHE_TTL", 900.0),
    )


def build_refresher(config: YouTubeConfig, **kwargs: object) -> OAuth2Refresher:
    """설정에서 OAuth2 갱신기를 만든다."""
    store = TokenStore("youtube", path=config.token_file, env_var="YOUTUBE_TOKEN_FILE")
    oauth = OAuth2Config(
        token_url=os.environ.get("YOUTUBE_TOKEN_URL", TOKEN_URL),
        client_id=config.client_id,
        client_secret=config.client_secret,
        refresh_token=config.refresh_token,
        setup_guide=SETUP_GUIDE,
    )
    return OAuth2Refresher(oauth, store, **kwargs)  # type: ignore[arg-type]
