"""서버 도구 등록 검증 — 9 도메인 도구가 누락 없이 등록되었는지 확인."""
from __future__ import annotations

from moai_mcp_smartstore.server import mcp


def _tool_names() -> set[str]:
    return set(mcp._tool_manager._tools.keys())


def test_total_tool_count_meets_floor():
    """90개 이상 도구 등록 (9 도메인 전 커버)."""
    names = _tool_names()
    assert len(names) >= 90


def test_auth_tools_present():
    names = _tool_names()
    assert "smartstore_test_connection" in names
    assert "smartstore_config_status" in names


def test_product_domain_tools_present():
    names = _tool_names()
    for t in [
        "product_search", "product_get_origin", "product_get_channel",
        "product_create", "product_update_origin", "product_delete_origin",
        "product_change_status", "product_update_stock", "product_bulk_update",
        "product_multi_update", "product_upload_images", "category_list",
        "brand_search", "manufacturer_search",
    ]:
        assert t in names, f"missing product tool: {t}"


def test_order_claim_flow_complete():
    """취소/반품/교환 클레임 상태 전이 도구가 전부 있어야 한다."""
    names = _tool_names()
    for t in [
        "order_list_product_orders", "order_query_product_orders",
        "order_changed_product_orders", "order_confirm", "order_dispatch",
        "order_delay", "order_cancel_request", "order_cancel_approve",
        "order_return_request", "order_return_approve", "order_return_reject",
        "order_return_holdback", "order_return_holdback_release",
        "order_exchange_collect_approve", "order_exchange_dispatch",
        "order_exchange_holdback", "order_exchange_holdback_release",
        "order_exchange_reject",
    ]:
        assert t in names, f"missing order tool: {t}"


def test_remaining_domains_present():
    names = _tool_names()
    for t in [
        # 정산
        "settlement_daily", "settlement_case", "settlement_commission_details",
        "vat_daily", "vat_case",
        # 문의
        "qna_list", "qna_answer", "qna_templates",
        "customer_inquiry_list", "customer_inquiry_answer", "customer_inquiry_answer_update",
        # 물류
        "logistics_companies", "outbound_locations", "sku_get", "sku_list", "sku_mappings",
        # 판매자
        "seller_account", "seller_channels", "addressbook_list", "addressbook_get",
        "this_day_dispatch_get", "this_day_dispatch_set",
        # 솔루션
        "solution_subscription_get", "solution_approve", "solution_unsubscribe",
        # 통계
        "stats_marketing", "stats_sales", "stats_shopping", "stats_realtime",
        "stats_customer_status", "stats_repurchase",
    ]:
        assert t in names, f"missing tool: {t}"
