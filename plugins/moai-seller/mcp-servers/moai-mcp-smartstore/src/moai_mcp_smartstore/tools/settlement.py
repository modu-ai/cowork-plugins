"""정산(Settlement) 도메인 도구 — 일별/건별 정산·수수료 상세·부가세."""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call

_SETTLE = "/v1/pay-settle"


@mcp.tool()
def settlement_daily(params: dict[str, Any] | None = None) -> dict:
    """일별 정산 합계 내역(계좌이체/충전금 구분). GET /v1/pay-settle/settle/daily

    params 예: {"startSettleDate": "2024-01-01", "endSettleDate": "2024-01-31"}
    """
    return call("GET", f"{_SETTLE}/settle/daily", params=params)


@mcp.tool()
def settlement_case(params: dict[str, Any] | None = None) -> dict:
    """건별 정산 내역(주문/상품주문/배송비 단위 분해). GET /v1/pay-settle/settle/case"""
    return call("GET", f"{_SETTLE}/settle/case", params=params)


@mcp.tool()
def settlement_commission_details(params: dict[str, Any] | None = None) -> dict:
    """수수료 상세 내역(수수료 유형/결제수단 분해). GET /v1/pay-settle/settle/commission-details"""
    return call("GET", f"{_SETTLE}/settle/commission-details", params=params)


@mcp.tool()
def vat_daily(params: dict[str, Any] | None = None) -> dict:
    """일별 부가세 합산 내역(세무 신고 기초자료). GET /v1/pay-settle/vat/daily"""
    return call("GET", f"{_SETTLE}/vat/daily", params=params)


@mcp.tool()
def vat_case(params: dict[str, Any] | None = None) -> dict:
    """건별 부가세 내역(상품주문 단위 원천 분개). GET /v1/pay-settle/vat/case"""
    return call("GET", f"{_SETTLE}/vat/case", params=params)
