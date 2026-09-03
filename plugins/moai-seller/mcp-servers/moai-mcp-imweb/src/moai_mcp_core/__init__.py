# 이 파일은 자동 생성된 복제본입니다 — 직접 수정하지 마세요.
# 정본: plugins/_shared/moai-mcp-core/__init__.py
# 동기화: python3 scripts/sync-mcp-core.py
"""moai-mcp-core — 자체 제작 MCP 서버 공통 코어.

정본은 `plugins/_shared/moai-mcp-core/moai_mcp_core/` 다.
각 서버의 `src/moai_mcp_core/` 는 `scripts/sync-mcp-core.py` 가 만든 복제본이며
**직접 수정하면 다음 동기화에서 덮어써진다.**

설계 근거: `.moai/reports/mcp-naming-consolidation-design.md` §3, §4-1.
"""

from .auth import OAuth2Config, OAuth2Refresher
from .cache import TTLCache
from .credentials import CredentialStore, is_unset, load as load_credentials
from .errors import (
    AuthError,
    McpToolError,
    QuotaExhausted,
    RateLimited,
    SetupRequired,
    UpstreamError,
    to_tool_result,
)
from .http import HttpClient
from .tokenstore import DEFAULT_DIR, TokenStore

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_DIR",
    "AuthError",
    "CredentialStore",
    "HttpClient",
    "McpToolError",
    "OAuth2Config",
    "OAuth2Refresher",
    "QuotaExhausted",
    "RateLimited",
    "SetupRequired",
    "TTLCache",
    "TokenStore",
    "UpstreamError",
    "is_unset",
    "load_credentials",
    "to_tool_result",
]
