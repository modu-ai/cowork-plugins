"""물류/N배송(Logistics) 도메인 도구 — 택배사·출고창고·SKU."""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call


@mcp.tool()
def logistics_companies() -> dict:
    """연동 택배사/물류사 정보(발송 deliveryCompanyCode 캐시용). GET /v1/logistics/logistics-companies"""
    return call("GET", "/v1/logistics/logistics-companies")


@mcp.tool()
def outbound_locations() -> dict:
    """판매자 출고 창고 정보. GET /v1/logistics/outbound-locations"""
    return call("GET", "/v1/logistics/outbound-locations")


@mcp.tool()
def return_delivery_companies() -> dict:
    """반품 처리 가능 택배사 목록. GET /v2/product-delivery-info/return-delivery-companies"""
    return call("GET", "/v2/product-delivery-info/return-delivery-companies")


@mcp.tool()
def sku_get(ns_id: str) -> dict:
    """N배송 SKU 1건 조회. GET /v1/logistics/products/sellers/me/skus/{nsId}"""
    return call("GET", f"/v1/logistics/products/sellers/me/skus/{ns_id}")


@mcp.tool()
def sku_mappings(ns_id: str, params: dict[str, Any] | None = None) -> dict:
    """SKU 연결(채널) 상품 매핑 현황 페이징 조회. GET .../skus/{nsId}/product-mappings"""
    return call(
        "GET",
        f"/v1/logistics/products/sellers/me/skus/{ns_id}/product-mappings",
        params=params,
    )


@mcp.tool()
def sku_list(body: dict[str, Any]) -> dict:
    """본인 SKU 복합조건 페이징 검색. POST /v1/logistics/products/sellers/me/skus/query-paged-list"""
    return call(
        "POST",
        "/v1/logistics/products/sellers/me/skus/query-paged-list",
        body=body,
    )
