"""Cafe24 Admin API — Customer domain (회원).

Covers customergroups (회원등급) + members, customer memos, payment information,
plusapp install info, social account links, autoupdate tier details, and signup
field (properties) config. Member search requires ``member_id`` or ``cellphone``.

Scopes: ``mall.read_customer`` / ``mall.write_customer``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "customer"
_R = "mall.read_customer"
_W = "mall.write_customer"
_BASE = "/api/v2/admin/customers"
_GRP = "/api/v2/admin/customergroups"

register(
    # === Customers (회원) ===
    Endpoint(name="cafe24_customer_list", category=_C, method="GET", path=_BASE, scope=_R,
             summary="회원 목록 조회 (member_id 또는 cellphone 필수)", resource_key="customer", list_endpoint=True,
             query_params=(Param("member_id", description="회원아이디 (콤마 다중)"),
                           Param("cellphone", description="휴대전화 (콤마 다중, 전체번호)"))),
    Endpoint(name="cafe24_customer_delete", category=_C, method="DELETE", path=f"{_BASE}/{{member_id}}", scope=_W,
             summary="회원 탈퇴 처리 (특정클라이언트)", resource_key="customer",
             query_params=(Param("is_point_check", description="적립금보유 회원 탈퇴여부: T/F"),)),

    # === Customer memos ===
    Endpoint(name="cafe24_customer_memo_count", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/memos/count", scope=_R,
             summary="회원 메모 수", resource_key="count"),
    Endpoint(name="cafe24_customer_memo_list", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/memos", scope=_R,
             summary="회원 메모 목록", resource_key="memo", list_endpoint=True,
             query_params=(Param("start_date"), Param("end_date"), Param("important_flag", description="T/F"), Param("limit", type="int"), Param("offset", type="int"))),
    Endpoint(name="cafe24_customer_memo_get", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/memos/{{memo_no}}", scope=_R,
             summary="회원 메모 상세", resource_key="memo"),
    Endpoint(name="cafe24_customer_memo_create", category=_C, method="POST", path=f"{_BASE}/{{member_id}}/memos", scope=_W,
             summary="회원 메모 등록", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_customer_memo_update", category=_C, method="PUT", path=f"{_BASE}/{{member_id}}/memos/{{memo_no}}", scope=_W,
             summary="회원 메모 수정", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_customer_memo_delete", category=_C, method="DELETE", path=f"{_BASE}/{{member_id}}/memos/{{memo_no}}", scope=_W,
             summary="회원 메모 삭제", resource_key="memo"),

    # === Payment information ===
    Endpoint(name="cafe24_customer_paymentinfo_list", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/paymentinformation", scope=_R,
             summary="회원 결제수단 정보 목록", resource_key="paymentinformation", list_endpoint=True),
    Endpoint(name="cafe24_customer_paymentinfo_delete_all", category=_C, method="DELETE", path=f"{_BASE}/{{member_id}}/paymentinformation", scope=_W,
             summary="회원 결제수단 정보 전체 삭제", resource_key="paymentinformation"),
    Endpoint(name="cafe24_customer_paymentinfo_delete", category=_C, method="DELETE", path=f"{_BASE}/{{member_id}}/paymentinformation/{{payment_method_id}}", scope=_W,
             summary="회원 결제수단 정보 개별 삭제", resource_key="paymentinformation"),

    # === Plusapp & social ===
    Endpoint(name="cafe24_customer_plusapp_get", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/plusapp", scope=_R,
             summary="플러스앱 설치 정보 조회", resource_key="plusapp", list_endpoint=True),
    Endpoint(name="cafe24_customer_social_get", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/social", scope=_R,
             summary="연동 SNS 계정 조회 (특정클라이언트)", resource_key="social", list_endpoint=True),

    # === Autoupdate tier ===
    Endpoint(name="cafe24_customer_autoupdate_get", category=_C, method="GET", path=f"{_BASE}/{{member_id}}/autoupdate", scope=_R,
             summary="회원등급 자동변경 정보 (다음 예상 등급 등)", resource_key="autoupdate"),

    # === Customer properties (회원가입항목) ===
    Endpoint(name="cafe24_customer_property_list", category=_C, method="GET", path=f"{_BASE}/properties", scope=_R,
             summary="회원가입항목 조회", resource_key="property", list_endpoint=True,
             query_params=(Param("type", description="join 회원가입 / edit 회원정보수정"),)),
    Endpoint(name="cafe24_customer_property_update", category=_C, method="PUT", path=f"{_BASE}/properties", scope=_W,
             summary="회원가입항목 수정", resource_key="property", takes_body=True, body_key="properties"),

    # === Customer groups (회원등급) ===
    Endpoint(name="cafe24_customergroup_list", category=_C, method="GET", path=_GRP, scope=_R,
             summary="회원등급 목록", resource_key="customergroup", list_endpoint=True,
             query_params=(Param("group_no"), Param("group_name"))),
    Endpoint(name="cafe24_customergroup_count", category=_C, method="GET", path=f"{_GRP}/count", scope=_R,
             summary="회원등급 수", resource_key="count"),
    Endpoint(name="cafe24_customergroup_get", category=_C, method="GET", path=f"{_GRP}/{{group_no}}", scope=_R,
             summary="회원등급 상세", resource_key="customergroup"),
    Endpoint(name="cafe24_customergroup_setting_get", category=_C, method="GET", path=f"{_GRP}/setting", scope=_R,
             summary="회원등급 자동변경 설정 조회", resource_key="customergroup_setting"),
    Endpoint(name="cafe24_customergroup_customer_assign", category=_C, method="POST", path=f"{_GRP}/{{group_no}}/customers", scope=_W,
             summary="회원을 특정 등급으로 지정 (최대 200건)", resource_key="customergroup_customer", takes_body=True, body_key="customers"),
)
