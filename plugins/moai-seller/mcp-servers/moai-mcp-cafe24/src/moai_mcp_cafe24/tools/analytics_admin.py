"""Cafe24 Admin API — Analytics domain (접속통계, admin-side).

Admin API 경로의 접속통계(일별 방문수). 상세 행동 분석은 별도 Analytics API
(cafe24data, :mod:`analytics_data`) 사용.

Scope: ``mall.read_analytics``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "analytics_admin"
_R = "mall.read_analytics"
_A = "/api/v2/admin"

register(
    Endpoint(name="cafe24_admin_dailyvisit_list", category=_C, method="GET", path=f"{_A}/financials/dailyvisits", scope=_R,
             summary="일별 방문수 통계 (Admin API, 특정클라이언트)", resource_key="financial_dailyvisit", list_endpoint=True,
             query_params=(Param("start_date", required=True, description="YYYY-MM-DD"),
                           Param("end_date", required=True, description="YYYY-MM-DD"))),
)
