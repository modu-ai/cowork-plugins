"""Cafe24 Admin API — Salesreport domain (매출통계).

PG사별/상품별/시간대별 매출 및 판매수량 통계. 일부 엔드포인트는 특정클라이언트 전용.

Scope: ``mall.read_salesreport``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "salesreport"
_R = "mall.read_salesreport"
_A = "/api/v2/admin"

register(
    Endpoint(name="cafe24_salesreport_daily_list", category=_C, method="GET", path=f"{_A}/financials/dailysales", scope=_R,
             summary="일별 매출 통계 (PG사별, 특정클라이언트)", resource_key="financial_dailysale", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True),
                           Param("payment_gateway_name"), Param("partner_id"), Param("payment_method"))),
    Endpoint(name="cafe24_salesreport_monthly_list", category=_C, method="GET", path=f"{_A}/financials/monthlysales", scope=_R,
             summary="월별 매출 통계 (PG사별, 특정클라이언트)", resource_key="financial_monthlysale", list_endpoint=True,
             query_params=(Param("start_month", required=True, description="YYYY-MM"), Param("end_month", required=True),
                           Param("payment_gateway_name"), Param("partner_id"), Param("payment_method"))),
    Endpoint(name="cafe24_salesreport_hourly_list", category=_C, method="GET", path=f"{_A}/reports/hourlysales", scope=_R,
             summary="시간대별 정산통계 (특정클라이언트)", resource_key="report_hourlysale", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True),
                           Param("collection_hour", description="00~23"), Param("limit", type="int"), Param("offset", type="int"))),
    Endpoint(name="cafe24_salesreport_product_list", category=_C, method="GET", path=f"{_A}/reports/productsales", scope=_R,
             summary="상품판매 시간대별 통계 (특정클라이언트)", resource_key="report_productsale", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True),
                           Param("collection_hour"), Param("limit", type="int"), Param("offset", type="int"))),
    Endpoint(name="cafe24_salesreport_volume_list", category=_C, method="GET", path=f"{_A}/reports/salesvolume", scope=_R,
             summary="판매수량 통계", resource_key="report_salesvolume", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True),
                           Param("product_no"), Param("variants_code"), Param("category_no"),
                           Param("mobile", description="T 모바일/F 그외"), Param("delivery_type", description="A 국내/B 해외"),
                           Param("group_no"), Param("supplier_id"))),
)
