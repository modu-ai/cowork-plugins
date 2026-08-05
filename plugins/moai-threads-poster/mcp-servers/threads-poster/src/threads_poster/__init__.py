"""moai-threads-poster MCP — Threads(Meta) Graph API 자동 포스팅 클라이언트 + MCP 서버.

패키지 구성:
  - :mod:`threads_poster.threads_api` — 순수 HTTP 클라이언트 (:class:`ThreadsClient`)
  - :mod:`threads_poster.queue`       — SQLite 백업 발행 큐 (:class:`Queue`) (M2)
  - :mod:`threads_poster.runner`      — 발행 runner CLI (수동 킥 + server.py 재사용) (M2)
  - :mod:`threads_poster.server`      — stdio MCP 서버 (FastMCP)
"""

from __future__ import annotations

from .queue import Queue
from .threads_api import ThreadsAPIError, ThreadsClient

__all__ = ["ThreadsClient", "ThreadsAPIError", "Queue"]
__version__ = "0.2.0"
