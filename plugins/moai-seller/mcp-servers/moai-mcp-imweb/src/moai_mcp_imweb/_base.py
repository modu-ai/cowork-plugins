"""Configuration + singleton client accessor.

Credentials are resolved by ``moai_mcp_core.CredentialStore``: environment first,
then ``~/.moai/mcp/imweb.json``. Environment alone is not enough — the Claude and
Codex desktop apps do not interpolate ``${KEY}`` in ``.mcp.json`` ``env`` and hand
the placeholder through verbatim (see ``moai_mcp_core/credentials.py``).
A refreshable access token is mandatory; ``CLIENT_ID``
+ ``CLIENT_SECRET`` + ``REFRESH_TOKEN`` enable automatic renewal on 401.

Token persistence: when ``IMWEB_TOKEN_FILE`` is set (or the default
``~/.moai/mcp/imweb-tokens.json`` is writable), refreshed tokens are persisted so
the long-lived refresh token survives restarts. Falls back gracefully to
in-memory only when the path is not writable.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from moai_mcp_core import CredentialStore, TokenStore

if TYPE_CHECKING:
    from .client import ImwebClient

#: 자격증명 파일 슬러그 — `~/.moai/mcp/imweb.json`.
SERVICE = "imweb"

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
    # 자격증명은 환경변수 → ~/.moai/mcp/imweb.json 순으로 해석한다. 데스크톱 앱은
    # `.mcp.json` 의 ${KEY} 를 확장하지 않으므로 환경변수 단독으로는 부족하다
    # (근거: moai_mcp_core/credentials.py).
    creds = CredentialStore(SERVICE)

    api_base = creds.get("IMWEB_API_BASE", DEFAULT_API_BASE).rstrip("/")
    token_file_str = creds.get("IMWEB_TOKEN_FILE")
    token_file = Path(token_file_str).expanduser() if token_file_str else DEFAULT_TOKEN_FILE

    access = creds.get("IMWEB_ACCESS_TOKEN")
    refresh = creds.get("IMWEB_REFRESH_TOKEN")

    # Prefer the most-recent persisted token when the env value is absent.
    if not access or not refresh:
        p_access, p_refresh = _load_persisted_tokens(token_file)
        access = access or p_access or ""
        refresh = refresh or p_refresh or ""

    timeout = _float_setting(creds, "IMWEB_TIMEOUT", DEFAULT_TIMEOUT)
    request_delay = _float_setting(creds, "IMWEB_REQUEST_DELAY", 0.0)

    return ImwebConfig(
        api_base=api_base,
        client_id=creds.get("IMWEB_CLIENT_ID"),
        client_secret=creds.get("IMWEB_CLIENT_SECRET"),
        access_token=access,
        refresh_token=refresh,
        unit_code=creds.get("IMWEB_UNIT_CODE"),
        timeout=timeout,
        token_file=token_file,
        request_delay=request_delay,
    )


def setup_hint() -> str:
    """자격증명이 비었을 때 보여줄 안내. 다 있으면 빈 문자열."""
    return CredentialStore(SERVICE).setup_hint(["IMWEB_CLIENT_ID", "IMWEB_CLIENT_SECRET"])


def _float_setting(creds: CredentialStore, name: str, default: float) -> float:
    raw = creds.get(name)
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
