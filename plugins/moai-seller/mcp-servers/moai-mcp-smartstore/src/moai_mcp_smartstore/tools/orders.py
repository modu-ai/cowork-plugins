"""주문(Order) 도메인 도구 — 조회·발주/발송·지연·취소/반품/교환 클레임 전流程.

클레임(취소/반품/교환)은 각 상태 전이가 별도 엔드포인트이므로 도구도 개별 노출한다.
상태 전이 흐름은 공식 위키 '주문 상태 변경 흐름도' 참고.
"""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call

_PO = "/v1/pay-order/seller/product-orders"


# ============================================================
# 주문 조회
# ============================================================


@mcp.tool()
def order_list_product_orders(params: dict[str, Any] | None = None) -> dict:
    """조건형 상품 주문 상세 내역 페이징 조회. GET /v1/pay-order/seller/product-orders

    params 예: {"productOrderStatuses": "PAYED", "pageSize": 100}
    """
    return call("GET", _PO, params=params)


@mcp.tool()
def order_query_product_orders(body: dict[str, Any]) -> dict:
    """다수 productOrderId 상세 주문 내역 일괄 조회. POST /v1/pay-order/seller/product-orders/query

    body 예: {"productOrderIds": ["20240101-0001", ...]}
    """
    return call("POST", f"{_PO}/query", body=body)


@mcp.tool()
def order_changed_product_orders(params: dict[str, Any] | None = None) -> dict:
    """지정 시점 이후 변경된 상품 주문 조회(변경 피드). GET .../last-changed-statuses

    OMS/CRM 주문 동기화 핵심. 1~3분 주기 폴링 권장.
    params 예: {"fromDateString": "2024-01-01T00:00:00+09:00"}
    """
    return call("GET", f"{_PO}/last-changed-statuses", params=params)


@mcp.tool()
def order_list_by_order(order_id: str) -> dict:
    """주문(orderId) 내 상품 주문 ID 목록. GET /v1/pay-order/seller/orders/{orderId}/product-order-ids"""
    return call(
        "GET",
        f"/v1/pay-order/seller/orders/{order_id}/product-order-ids",
    )


# ============================================================
# 발주·발송·지연
# ============================================================


@mcp.tool()
def order_confirm(body: dict[str, Any]) -> dict:
    """결제완료 주문 발주 확인 일괄 처리. POST /v1/pay-order/seller/product-orders/confirm

    body 예: {"productOrderIds": [...]}
    """
    return call("POST", f"{_PO}/confirm", body=body)


@mcp.tool()
def order_dispatch(body: dict[str, Any]) -> dict:
    """다건 상품 주문 발송 처리(택배사/송장번호 등록). POST .../dispatch

    deliveryMethod/택배사 코드/송장번호가 실무상 필수.
    """
    return call("POST", f"{_PO}/dispatch", body=body)


@mcp.tool()
def order_delay(product_order_id: str, body: dict[str, Any]) -> dict:
    """발송 지연 등록(사유코드+새 발송예정일). POST .../{productOrderId}/delay"""
    return call("POST", f"{_PO}/{product_order_id}/delay", body=body)


@mcp.tool()
def order_change_hope_delivery(product_order_id: str, body: dict[str, Any]) -> dict:
    """배송 희망일 변경 처리. POST .../{productOrderId}/hope-delivery/change"""
    return call("POST", f"{_PO}/{product_order_id}/hope-delivery/change", body=body)


# ============================================================
# 취소 클레임
# ============================================================


@mcp.tool()
def order_cancel_request(product_order_id: str, body: dict[str, Any]) -> dict:
    """판매자 주도 취소 요청(재고부족 등). POST .../{id}/claim/cancel/request"""
    return call("POST", f"{_PO}/{product_order_id}/claim/cancel/request", body=body)


@mcp.tool()
def order_cancel_approve(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """고객 취소 요청 승인(승인 즉시 환불). POST .../{id}/claim/cancel/approve"""
    return call("POST", f"{_PO}/{product_order_id}/claim/cancel/approve", body=body or {})


# ============================================================
# 반품 클레임
# ============================================================


@mcp.tool()
def order_return_request(product_order_id: str, body: dict[str, Any]) -> dict:
    """판매자 주도 반품 요청 등록. POST .../{id}/claim/return/request"""
    return call("POST", f"{_PO}/{product_order_id}/claim/return/request", body=body)


@mcp.tool()
def order_return_approve(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """고객 반품 요청 승인(수거완료 건 자동/일괄 승인, 이후 환불). POST .../{id}/claim/return/approve"""
    return call("POST", f"{_PO}/{product_order_id}/claim/return/approve", body=body or {})


@mcp.tool()
def order_return_reject(product_order_id: str, body: dict[str, Any]) -> dict:
    """반품 요청 거부/철회(거부사유코드+안내메시지). POST .../{id}/claim/return/reject"""
    return call("POST", f"{_PO}/{product_order_id}/claim/return/reject", body=body)


@mcp.tool()
def order_return_holdback(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """반품 환불 일시 보류(추가 협의 필요 시). POST .../{id}/claim/return/holdback"""
    return call("POST", f"{_PO}/{product_order_id}/claim/return/holdback", body=body or {})


@mcp.tool()
def order_return_holdback_release(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """반품 보류 해제(환불 재개). POST .../{id}/claim/return/holdback/release"""
    return call(
        "POST",
        f"{_PO}/{product_order_id}/claim/return/holdback/release",
        body=body or {},
    )


# ============================================================
# 교환 클레임
# ============================================================


@mcp.tool()
def order_exchange_collect_approve(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """교환 수거(회수) 완료 등록 → 자동 재배송 단계 전이. POST .../{id}/claim/exchange/collect/approve"""
    return call(
        "POST",
        f"{_PO}/{product_order_id}/claim/exchange/collect/approve",
        body=body or {},
    )


@mcp.tool()
def order_exchange_dispatch(product_order_id: str, body: dict[str, Any]) -> dict:
    """교환 상품 재배송 처리(택배사/송장번호 필수). POST .../{id}/claim/exchange/dispatch"""
    return call("POST", f"{_PO}/{product_order_id}/claim/exchange/dispatch", body=body)


@mcp.tool()
def order_exchange_holdback(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """교환 일시 보류. POST .../{id}/claim/exchange/holdback"""
    return call("POST", f"{_PO}/{product_order_id}/claim/exchange/holdback", body=body or {})


@mcp.tool()
def order_exchange_holdback_release(product_order_id: str, body: dict[str, Any] | None = None) -> dict:
    """교환 보류 해제. POST .../{id}/claim/exchange/holdback/release"""
    return call(
        "POST",
        f"{_PO}/{product_order_id}/claim/exchange/holdback/release",
        body=body or {},
    )


@mcp.tool()
def order_exchange_reject(product_order_id: str, body: dict[str, Any]) -> dict:
    """교환 거부/철회(재고부족·사유미충족). POST .../{id}/claim/exchange/reject"""
    return call("POST", f"{_PO}/{product_order_id}/claim/exchange/reject", body=body)
