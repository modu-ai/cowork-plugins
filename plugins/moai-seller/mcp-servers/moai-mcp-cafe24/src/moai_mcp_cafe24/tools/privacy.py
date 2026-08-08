"""Cafe24 Admin API — Privacy domain (개인정보).

회원 개인정보(customersprivacy) — 민감 데이터. 조회/수정 권한 분리.
검색은 회원정보 기반(search_type=customer_info) 또는 가입일 기반(created_date) 지원.

Scopes: ``mall.read_privacy`` / ``mall.write_privacy``.

NOTE: 상품을 관심상품에 담은 *회원* 조회(products/{product_no}/wishlist/customers)는
``mall.read_privacy`` 스코프이나 성격상 privacy 도메인에 포함.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "privacy"
_R = "mall.read_privacy"
_W = "mall.write_privacy"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int", description="최대건수 (최대 1000)"), Param("offset", type="int", description="시작위치 (최대 8000)"))

register(
    # === Customer privacy ===
    Endpoint(name="cafe24_customerprivacy_list", category=_C, method="GET", path=f"{_A}/customersprivacy", scope=_R,
             summary="회원 개인정보 목록", resource_key="customerprivacy", list_endpoint=True,
             query_params=_LIST + (Param("search_type", description="customer_info/created_date"),
                                   Param("created_start_date", description="가입일 검색시 (created_date)"),
                                   Param("member_id"), Param("search_field", description="id/name/hp/tel/mail/shop_name"),
                                   Param("keyword"), Param("date_type", description="join/login/age/account_reactivation/wedding"),
                                   Param("start_date"), Param("end_date"))),
    Endpoint(name="cafe24_customerprivacy_count", category=_C, method="GET", path=f"{_A}/customersprivacy/count", scope=_R,
             summary="회원 개인정보 수", resource_key="count"),
    Endpoint(name="cafe24_customerprivacy_get", category=_C, method="GET", path=f"{_A}/customersprivacy/{{member_id}}", scope=_R,
             summary="회원 개인정보 상세", resource_key="customerprivacy"),
    Endpoint(name="cafe24_customerprivacy_update", category=_C, method="PUT", path=f"{_A}/customersprivacy/{{member_id}}", scope=_W,
             summary="회원 개인정보 수정 (연락처/수신동의/주소 등)", resource_key="customerprivacy", takes_body=True),

    # === Product wishlist customers (read_privacy scope) ===
    Endpoint(name="cafe24_product_wishlist_customer_list", category=_C, method="GET", path=f"{_A}/products/{{product_no}}/wishlist/customers", scope=_R,
             summary="상품을 관심상품에 담은 회원 목록", resource_key="customer", list_endpoint=True),
    Endpoint(name="cafe24_product_wishlist_customer_count", category=_C, method="GET", path=f"{_A}/products/{{product_no}}/wishlist/customers/count", scope=_R,
             summary="상품을 관심상품에 담은 회원 수", resource_key="count"),
)
