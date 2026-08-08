"""커머스솔루션(Commerce Solution) 도메인 도구 — 솔루션 구독 생명주기·결제내역."""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call

_CS = "/v1/commerce-solutions"


@mcp.tool()
def solution_seller_info_by_token(params: dict[str, Any]) -> dict:
    """판매자 인증 JWE 토큰 해석 → 판매자 식별 정보. GET /v1/commerce-solutions/seller-info-by-token"""
    return call("GET", f"{_CS}/seller-info-by-token", params=params)


@mcp.tool()
def solution_subscription_get(account_uid: str) -> dict:
    """특정 accountUid 솔루션 사용 상태 조회. GET /v1/commerce-solutions/subscriptions/{accountUid}"""
    return call("GET", f"{_CS}/subscriptions/{account_uid}")


@mcp.tool()
def solution_transactions(params: dict[str, Any] | None = None) -> dict:
    """비즈월렛 결제 내역 조회. GET /v1/commerce-solutions/transactions"""
    return call("GET", f"{_CS}/transactions", params=params)


@mcp.tool()
def solution_external_transaction_send(body: dict[str, Any]) -> dict:
    """솔루션 자체 결제 내역을 네이버 정산 데이터로 전송(멱등 키 필수). POST .../external-transactions"""
    return call("POST", f"{_CS}/external-transactions", body=body)


@mcp.tool()
def solution_approve(body: dict[str, Any]) -> dict:
    """솔루션 사용 시작 신청 최종 승인. PUT /v1/commerce-solutions/subscriptions/approve"""
    return call("PUT", f"{_CS}/subscriptions/approve", body=body)


@mcp.tool()
def solution_reject(account_uid: str, body: dict[str, Any] | None = None) -> dict:
    """솔루션 사용 시작 거절. PUT /v1/commerce-solutions/subscriptions/{accountUid}/reject"""
    return call("PUT", f"{_CS}/subscriptions/{account_uid}/reject", body=body or {})


@mcp.tool()
def solution_unsubscribe(account_uid: str, body: dict[str, Any] | None = None) -> dict:
    """솔루션 사용 중지(결제정지 동반). PUT /v1/commerce-solutions/subscriptions/{accountUid}/unsubscription"""
    return call("PUT", f"{_CS}/subscriptions/{account_uid}/unsubscription", body=body or {})


@mcp.tool()
def solution_unsubscribe_approve(body: dict[str, Any]) -> dict:
    """솔루션 사용 해지 신청 최종 승인. PUT /v1/commerce-solutions/subscriptions/unsubscription/approve"""
    return call("PUT", f"{_CS}/subscriptions/unsubscription/approve", body=body)
