"""Configuration + singleton client accessor.

Credentials are sourced from environment variables (interpolated by the MCP host
from ``.mcp.json`` ``env``). A refreshable access token is mandatory; ``CLIENT_ID``
+ ``CLIENT_SECRET`` + ``REFRESH_TOKEN`` enable automatic renewal on 401.

Token persistence: when ``IMWEB_TOKEN_FILE`` is set (or the default
``~/.moai/mcp/imweb-tokens.json`` is writable), refreshed tokens are persisted so
the long-lived refresh token survives restarts. Falls back gracefully to
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
    from .client import ImwebClient

DEFAULT_API_BASE = "https://openapi.imweb.me"
DEFAULT_TIMEOUT = 30.0
DEFAULT_TOKEN_FILE = Path.home() / ".moai" / "mcp" / "imweb-tokens.json"


@dataclass(frozen=True)
class ImwebConfig:
    api_base: str
    client_id: str
    client_secret: str
    access_token: str
    refresh_token: str
    unit_code: str
    timeout: float
    token_file: Optional[Path]
    request_delay: float  # seconds slept between requests; 0 disables

    @property
    def can_refresh(self) -> bool:
        return bool(self.client_id and self.client_secret and self.refresh_token)


def token_store(path: Optional[Path]) -> TokenStore:
    """공통 코어의 토큰 저장소. 경로가 없으면 기본 위치를 쓴다."""
    return TokenStore("imweb", path=path) if path else TokenStore("imweb")


def _load_persisted_tokens(path: Optional[Path]) -> tuple[Optional[str], Optional[str]]:
    """저장된 토큰을 읽는다. 손상·부재는 (None, None).

    실제 파일 입출력은 공통 코어(`moai_mcp_core.TokenStore`)가 담당한다 —
    쓰기 불가 환경의 인메모리 폴백, utf-8 고정, 임시 파일 후 교체가 거기에 있다.
    """
    if not path:
        return None, None
    data = token_store(path).load()
    return data.get("access_token"), data.get("refresh_token")


def _persist_tokens(path: Optional[Path], access: Optional[str], refresh: Optional[str]) -> None:
    """토큰을 저장한다. 실패는 치명적이지 않다(최선 노력)."""
    if not path:
        return
    token_store(path).save({"access_token": access, "refresh_token": refresh})


def load_config() -> ImwebConfig:
    api_base = os.environ.get("IMWEB_API_BASE", DEFAULT_API_BASE).rstrip("/")
    token_file_str = os.environ.get("IMWEB_TOKEN_FILE")
    token_file = Path(token_file_str).expanduser() if token_file_str else DEFAULT_TOKEN_FILE

    access = os.environ.get("IMWEB_ACCESS_TOKEN") or ""
    refresh = os.environ.get("IMWEB_REFRESH_TOKEN") or ""

    # Prefer the most-recent persisted token when the env value is absent.
    if not access or not refresh:
        p_access, p_refresh = _load_persisted_tokens(token_file)
        access = access or p_access or ""
        refresh = refresh or p_refresh or ""

    timeout = _float_env("IMWEB_TIMEOUT", DEFAULT_TIMEOUT)
    request_delay = _float_env("IMWEB_REQUEST_DELAY", 0.0)

    return ImwebConfig(
        api_base=api_base,
        client_id=os.environ.get("IMWEB_CLIENT_ID", ""),
        client_secret=os.environ.get("IMWEB_CLIENT_SECRET", ""),
        access_token=access,
        refresh_token=refresh,
        unit_code=os.environ.get("IMWEB_UNIT_CODE", ""),
        timeout=timeout,
        token_file=token_file,
        request_delay=request_delay,
    )


def _float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def now_ts() -> float:
    # ``time.time`` is used (not ``datetime.now``) for monotonic-ish wall clock
    # without pulling datetime into tool-call surfaces.
    return time.time()


# --- singleton client -------------------------------------------------------
_client_singleton: Optional["ImwebClient"] = None  # type: ignore[name-defined]


def get_client() -> "ImwebClient":  # type: ignore[name-defined]
    """Return the process-wide ImwebClient (lazy-initialised on first call)."""
    global _client_singleton
    if _client_singleton is None:
        from .client import ImwebClient

        _client_singleton = ImwebClient(load_config())
    return _client_singleton
