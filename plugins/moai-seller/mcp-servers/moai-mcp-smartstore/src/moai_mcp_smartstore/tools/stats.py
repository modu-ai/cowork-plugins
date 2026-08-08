"""통계(API 데이터솔루션) 도메인 도구 — 마케팅·판매·쇼핑·실시간·고객·재구매.

24개 통계 엔드포인트를 계열별 도구로 그룹화. 각 도구는 dataset 파라미터로 해당 계열의
하위 엔드포인트를 선택한다. API데이터솔루션 사용 신청이 선행되어야 한다.

공통 파라미터 예: {"startDate": "2024-01-01", "endDate": "2024-01-31"}
"""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call

# 계열별 허용 dataset 값 (공식 path suffix).
_MARKETING_DATASETS = {
    "all-daily", "all-detail", "custom-detail", "custom-simple",
    "hourly-detail", "hourly-simple", "search-detail", "search-keyword",
    "website-daily", "website-detail",
}
_SALES_DATASETS = {
    "delivery-detail", "hourly-detail", "product-detail",
    "product-marketing-category", "product-marketing-detail",
    "product-search-detail", "product-search-keyword-by-product",
}
_SHOPPING_DATASETS = {"page-detail", "product-detail"}


@mcp.tool()
def stats_marketing(channel_no: str, dataset: str, params: dict[str, Any] | None = None) -> dict:
    """마케팅 성과 통계. GET /v1/bizdata-stats/channels/{channelNo}/marketing/{dataset}

    dataset ∈ {all-daily, all-detail, custom-detail, custom-simple, hourly-detail,
    hourly-simple, search-detail, search-keyword, website-daily, website-detail}
    """
    if dataset not in _MARKETING_DATASETS:
        return {"ok": False, "error": "invalid_dataset",
                "message": f"dataset must be one of {sorted(_MARKETING_DATASETS)}"}
    return call(
        "GET",
        f"/v1/bizdata-stats/channels/{channel_no}/marketing/{dataset}",
        params=params,
    )


@mcp.tool()
def stats_sales(channel_no: str, dataset: str, params: dict[str, Any] | None = None) -> dict:
    """판매 성과 통계. GET /v1/bizdata-stats/channels/{channelNo}/sales/{dataset}

    dataset ∈ {delivery-detail, hourly-detail, product-detail, product-marketing-category,
    product-marketing-detail, product-search-detail, product-search-keyword-by-product}
    """
    if dataset not in _SALES_DATASETS:
        return {"ok": False, "error": "invalid_dataset",
                "message": f"dataset must be one of {sorted(_SALES_DATASETS)}"}
    return call(
        "GET",
        f"/v1/bizdata-stats/channels/{channel_no}/sales/{dataset}",
        params=params,
    )


@mcp.tool()
def stats_shopping(channel_no: str, dataset: str, params: dict[str, Any] | None = None) -> dict:
    """쇼핑행동 통계. GET /v1/bizdata-stats/channels/{channelNo}/shopping/{dataset}

    dataset ∈ {page-detail, product-detail}
    """
    if dataset not in _SHOPPING_DATASETS:
        return {"ok": False, "error": "invalid_dataset",
                "message": f"dataset must be one of {sorted(_SHOPPING_DATASETS)}"}
    return call(
        "GET",
        f"/v1/bizdata-stats/channels/{channel_no}/shopping/{dataset}",
        params=params,
    )


@mcp.tool()
def stats_realtime(channel_no: str, params: dict[str, Any] | None = None) -> dict:
    """오늘 실시간 채널 보고서(1~5분 폴링 권장). GET /v1/bizdata-stats/channels/{channelNo}/realtime/daily"""
    return call(
        "GET",
        f"/v1/bizdata-stats/channels/{channel_no}/realtime/daily",
        params=params,
    )


@mcp.tool()
def stats_customer_status(channel_no: str = "") -> dict:
    """고객 현황 통계. channel_no 미제공 시 계정(전 채널 합산), 제공 시 채널 단위.

    - 계정: GET /v1/customer-data/customer-status/account/statistics
    - 채널: GET /v1/customer-data/customer-status/channels/{channelNo}/statistics
    """
    if channel_no:
        return call(
            "GET",
            f"/v1/customer-data/customer-status/channels/{channel_no}/statistics",
        )
    return call("GET", "/v1/customer-data/customer-status/account/statistics")


@mcp.tool()
def stats_repurchase() -> dict:
    """계정 단위 재구매 통계(고객 충성도/재구매 캠페인 ROI). GET /v1/customer-data/repurchase/account/statistics"""
    return call("GET", "/v1/customer-data/repurchase/account/statistics")
