"""판매자정보(Seller) 도메인 도구 — 계정·채널·주소록·오늘출발."""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call


@mcp.tool()
def seller_account() -> dict:
    """인증 토큰의 판매자 계정 기본 정보. GET /v1/seller/account"""
    return call("GET", "/v1/seller/account")


@mcp.tool()
def seller_channels() -> dict:
    """계정 연결 채널(스마트스토어/브랜드스토어) 목록. GET /v1/seller/channels"""
    return call("GET", "/v1/seller/channels")


@mcp.tool()
def addressbook_list(params: dict[str, Any] | None = None) -> dict:
    """판매자 주소록 페이지 조회. GET /v1/seller/addressbooks-for-page"""
    return call("GET", "/v1/seller/addressbooks-for-page", params=params)


@mcp.tool()
def addressbook_get(address_book_no: str) -> dict:
    """주소록 1건 조회. GET /v1/seller/addressbooks/{addressBookNo}"""
    return call("GET", f"/v1/seller/addressbooks/{address_book_no}")


@mcp.tool()
def this_day_dispatch_get() -> dict:
    """오늘출발(즉시발송) 정책 설정값 조회. GET /v1/seller/this-day-dispatch"""
    return call("GET", "/v1/seller/this-day-dispatch")


@mcp.tool()
def this_day_dispatch_set(body: dict[str, Any]) -> dict:
    """오늘출발 정책 설정/변경. POST /v1/seller/this-day-dispatch"""
    return call("POST", "/v1/seller/this-day-dispatch", body=body)
