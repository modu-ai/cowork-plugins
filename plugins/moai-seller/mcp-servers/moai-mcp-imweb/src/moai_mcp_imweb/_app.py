"""FastMCP application instance — single shared `mcp` object.

Tools live in :mod:`moai_mcp_imweb.tools.*` and register themselves on this instance
via ``@mcp.tool()``. :mod:`moai_mcp_imweb.server` imports the tools package to trigger
registration, then runs the server.

Keeping the instance in its own module avoids a circular import between
``server`` (runs the server) and ``tools.*`` (register tools).
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

# Server instructions — surfaced to the model so it knows WHEN to search this
# server's tools (tool-search deferral is the default since Claude Code v2.1.121).
# Truncated at 2KB by Claude Code, so keep concise and front-load the category list.
_INSTRUCTIONS = (
    "아임웹(Imweb) OPEN API v3 쇼핑몰 운영 MCP. "
    "주문·상품·회원·커뮤니티(Q&A·구매평)·프로모션(적립금·쿠폰)·결제·"
    "사이트 정보·스크립트 8 카테고리. 각 도구는 action(enum)으로 세부 작업을 "
    "디스패치 — params=path+query, body=POST/PATCH 본문(action별 typed Body 모델), "
    "paginate=True로 list 계열 전체 페이지 자동 집계. "
    "OAuth2 authorizationCode + JWT(자동 갱신)."
)
mcp: FastMCP = FastMCP("moai-imweb", instructions=_INSTRUCTIONS)
