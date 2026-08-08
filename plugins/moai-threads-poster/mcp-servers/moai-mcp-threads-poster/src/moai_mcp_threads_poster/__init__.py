"""moai-threads-poster MCP — Threads(Meta) Graph API 자동 포스팅 클라이언트 + MCP 서버.

패키지 구성:
  - :mod:`moai_mcp_threads_poster.threads_api`  — 순수 HTTP 클라이언트 (:class:`ThreadsClient`)
  - :mod:`moai_mcp_threads_poster.instagram_api` — Instagram Graph API 클라이언트 (:class:`InstagramClient`)
  - :mod:`moai_mcp_threads_poster.server`        — stdio MCP 서버 (FastMCP, 직접 발행 모델)
"""

from __future__ import annotations

from .threads_api import ThreadsAPIError, ThreadsClient

__all__ = ["ThreadsClient", "ThreadsAPIError"]
__version__ = "0.3.0"
