"""
MCP stdio 서버 인스턴스 + 도구 등록 진입.

FastMCP 인스턴스(mcp)를 먼저 생성한 뒤, 각 도메인 도구 모듈을 import 하여
@mcp.tool() 데코레이터로 도구를 등록한다. 도구 모듈은 `from .server import mcp`
로 동일 인스턴스를 참조한다.

실행: `uvx moai-mcp-smartstore` → __main__.main() → mcp.run() (stdio)
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import __version__

# @MX:NOTE: [AUTO] FastMCP 생성자는 version 파라미터 미지원 (mcp>=1.0.0 호환)
mcp = FastMCP(
    name=f"moai-mcp-smartstore/{__version__}",
    instructions=(
        "네이버 커머스(스마트스토어) 운영/관리 MCP. "
        "자격증명은 환경변수(NAVER_COMMERCE_CLIENT_ID/SECRET/ACCOUNT_ID)에서 읽는다. "
        "먼저 smartstore_test_connection 으로 인증을 검증하고, "
        "각 도구의 endpoint 필드로 대상 API 를 식별한다. "
        "모든 도구는 {ok, endpoint, data|error} 형태로 응답한다."
    ),
)

# 도메인 도구 모듈 import — @mcp.tool() 등록 트리거 (mcp 정의 후).
from .tools import (  # noqa: E402,F401  (import for side-effect: tool registration)
    auth,
    inquiries,
    logistics,
    orders,
    products,
    seller,
    settlement,
    solutions,
    stats,
)
