"""Configuration + singleton client accessor for the Cafe24 API.

Cafe24 exposes TWO API surfaces with distinct base hosts:

  * **Admin API** — ``https://{mall_id}.cafe24api.com`` (mall-scoped host).
    Paths are prefixed ``/api/v2/admin/...``. Drives store/product/order/...
    operations. Requires ``mall.read_*`` / ``mall.write_*`` scopes.
  * **Analytics API** — ``https://ca-api.cafe24data.com`` (single fixed host).
    Paths are root-level (``/visitors/pageview``, ``/products/sales`` ...).
    Requires the ``mall.analytics`` scope (a.k.a. 접속통계 읽기권한).

Credentials are sourced from environment variables (interpolated by the MCP
host from ``.mcp.json`` ``env``). A refreshable ``access_token`` is mandatory;
``CLIENT_ID`` + ``CLIENT_SECRET`` + ``REFRESH_TOKEN`` enable automatic renewal
on HTTP 401. The access token lives 2 hours; the refresh token lives 2 weeks
and **rotates on every refresh** (Cafe24 invalidates the old refresh token and
returns a fresh one — see :mod:`moai_mcp_cafe24.auth`).

Token persistence: refreshed tokens are stored at
``~/.moai/mcp/cafe24-tokens.json`` (override via ``CAFE24_TOKEN_FILE``) so the
long-lived refresh token survives process restarts. Best-effort — falls back to
in-memory only when the path is not writable.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from moai_mcp_core import TokenStore

if TYPE_CHECKING:
    from .client import Cafe24Client

ANALYTICS_API_BASE = "https://ca-api.cafe24data.com"
DEFAULT_API_VERSION = "2026-03-01"  # Cafe24 app-default version (2025-09-01 retired → HTTP 400)
DEFAULT_TIMEOUT = 30.0
DEFAULT_SHOP_NO = 1
DEFAULT_TOKEN_FILE = Path.home() / ".moai" / "mcp" / "cafe24-tokens.json"


@dataclass(frozen=True)
class Cafe24Config:
    mall_id: str
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    api_version: str
    shop_no: int
    timeout: float
    token_file: Optional[Path]
    request_delay: float  # seconds slept between requests; 0 disables

    @property
    def admin_base(self) -> str:
        # Mall-scoped host: https://{mall_id}.cafe24api.com
        return f"https://{self.mall_id}.cafe24api.com"

    @property
    def analytics_base(self) -> str:
        return ANALYTICS_API_BASE

    @property
    def can_refresh(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token and self.mall_id)


def token_store(path: Optional[Path]) -> TokenStore:
    """공통 코어의 토큰 저장소. 경로가 없으면 기본 위치를 쓴다."""
    return TokenStore("cafe24", path=path) if path else TokenStore("cafe24")


def _load_persisted_tokens(path: Optional[Path]) -> tuple[Optional[str], Optional[str]]:
    """저장된 토큰을 읽는다. 손상·부재는 (None, None).

    파일 입출력은 공통 코어(`moai_mcp_core.TokenStore`)가 담당한다.
    """
    if not path:
        return None, None
    data = token_store(path).load()
    return data.get("access_token"), data.get("refresh_token")


def _persist_tokens(path: Optional[Path], access: Optional[str], refresh: Optional[str]) -> None:
    """토큰을 저장한다. 실패는 치명적이지 않지만 **조용하지도 않다.**

    카페24는 갱신할 때마다 리프레시 토큰을 회전시키고 이전 것을 즉시 무효화한다.
    저장에 실패하면 회전된 토큰이 메모리에만 남고, 다음 프로세스는 환경변수의
    이미 죽은 토큰을 다시 쓰다가 인증에 실패한다. 그 실패는 auth.py 의 메시지
    때문에 "리프레시 만료"로 오진되기 쉬우므로, 저장 실패는 stderr 로 알린다.
    """
    if not path:
        return
    if not token_store(path).save({"access_token": access, "refresh_token": refresh}):
        import sys

        print(
            f"[moai-cafe24] WARN: token persistence failed ({path}) — "
            "회전된 refresh token 이 메모리에만 남았습니다. 다음 실행에서 인증이 실패할 수 있습니다.",
            file=sys.stderr,
        )


def load_config() -> Cafe24Config:
    mall_id = os.environ.get("CAFE24_MALL_ID", "").strip()
    token_file_str = os.environ.get("CAFE24_TOKEN_FILE")
    token_file = Path(token_file_str).expanduser() if token_file_str else DEFAULT_TOKEN_FILE

    # Bootstrap from env (static .mcp.json values), then prefer persisted tokens.
    # The persisted refresh token is the result of the most recent rotation and
    # MUST supersede the static env value: Cafe24 invalidates the old refresh
    # token on every refresh, so the env value goes stale the first time a 401
    # triggers auth.refresh_access_token. A fresh process that falls back to the
    # stale env refresh token reuses an invalidated credential and fails auth —
    # persisted wins, env only bootstraps the very first run before any rotation.
    access = os.environ.get("CAFE24_ACCESS_TOKEN") or ""
    refresh = os.environ.get("CAFE24_REFRESH_TOKEN") or ""
    p_access, p_refresh = _load_persisted_tokens(token_file)
    access = p_access or access
    refresh = p_refresh or refresh

    return Cafe24Config(
        mall_id=mall_id,
        client_id=os.environ.get("CAFE24_CLIENT_ID", ""),
        client_secret=os.environ.get("CAFE24_CLIENT_SECRET", ""),
        access_token=access,
        refresh_token=refresh,
        api_version=os.environ.get("CAFE24_API_VERSION", DEFAULT_API_VERSION),
        shop_no=_int_env("CAFE24_SHOP_NO", DEFAULT_SHOP_NO),
        timeout=_float_env("CAFE24_TIMEOUT", DEFAULT_TIMEOUT),
        token_file=token_file,
        request_delay=_float_env("CAFE24_REQUEST_DELAY", 0.0),
    )


def _float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def now_ts() -> float:
    return time.time()


# --- singleton client -------------------------------------------------------
_client_singleton: Optional["Cafe24Client"] = None  # type: ignore[name-defined]


def get_client() -> "Cafe24Client":  # type: ignore[name-defined]
    """Return the process-wide Cafe24Client (lazy-initialised on first call)."""
    global _client_singleton
    if _client_singleton is None:
        from .client import Cafe24Client

        _client_singleton = Cafe24Client(load_config())
    return _client_singleton
