"""Cafe24 Admin API — Mileage domain (적립금/예치금).

적립금(points) 조회/지급/차감, 예치금(credits), 적립금/예치금 통계(report),
적립금 자동만료(autoexpiration). 민감 API — 이용 주의.

Scopes: ``mall.read_mileage`` / ``mall.write_mileage``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "mileage"
_R = "mall.read_mileage"
_W = "mall.write_mileage"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))
_DATE = (Param("start_date", required=True), Param("end_date", required=True))

register(
    # === Credits (예치금) ===
    Endpoint(name="cafe24_credit_list", category=_C, method="GET", path=f"{_A}/credits", scope=_R,
             summary="예치금 내역 목록", resource_key="credit", list_endpoint=True,
             query_params=_DATE + (Param("type", description="I 지급/D 차감"), Param("case"), Param("member_id"), Param("order_id"))),
    Endpoint(name="cafe24_credit_report", category=_C, method="GET", path=f"{_A}/credits/report", scope=_R,
             summary="예치금 통계 (기간내 증감/잔액)", resource_key="credit_report",
             query_params=_DATE + (Param("type"), Param("case"))),

    # === Points (적립금) ===
    Endpoint(name="cafe24_point_list", category=_C, method="GET", path=f"{_A}/points", scope=_R,
             summary="적립금 내역 목록", resource_key="point", list_endpoint=True,
             query_params=_DATE + (Param("member_id"), Param("order_id"), Param("case"), Param("points_category", description="available/unavailable/unavailable_coupon"))),
    Endpoint(name="cafe24_point_issue", category=_C, method="POST", path=f"{_A}/points", scope=_W,
             summary="적립금 지급/차감 (필수: member_id/amount/type)", resource_key="point", takes_body=True,
             description="1회당 최대 1,000,000. 가용 적립금 초과 차감 불가."),
    Endpoint(name="cafe24_point_report", category=_C, method="GET", path=f"{_A}/points/report", scope=_R,
             summary="적립금 통계 (가용 증감/잔액, 미가용)", resource_key="point_report",
             query_params=_DATE + (Param("member_id"), Param("group_no"))),

    # === Points autoexpiration ===
    Endpoint(name="cafe24_point_autoexpiration_get", category=_C, method="GET", path=f"{_A}/points/autoexpiration", scope=_R,
             summary="적립금 자동만료 설정 조회", resource_key="autoexpiration"),
    Endpoint(name="cafe24_point_autoexpiration_create", category=_C, method="POST", path=f"{_A}/points/autoexpiration", scope=_W,
             summary="적급금 자동만료 설정 등록", resource_key="autoexpiration", takes_body=True),
    Endpoint(name="cafe24_point_autoexpiration_delete", category=_C, method="DELETE", path=f"{_A}/points/autoexpiration", scope=_W,
             summary="적립금 자동만료 설정 삭제", resource_key="autoexpiration"),
)
