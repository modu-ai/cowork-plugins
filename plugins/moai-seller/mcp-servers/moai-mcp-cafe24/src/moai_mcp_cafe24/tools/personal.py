"""Cafe24 Admin API — Personal domain (개인화정보).

회원 장바구니(carts), 관심상품(wishlist), 상품별 장바구니 담은 회원(products carts).
읽기 전용 회원 행동 데이터.

Scope: ``mall.read_personal``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "personal"
_R = "mall.read_personal"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))

register(
    # === Carts (장바구니) ===
    Endpoint(name="cafe24_cart_list", category=_C, method="GET", path=f"{_A}/carts", scope=_R,
             summary="회원 장바구니 목록 (member_id 필수)", resource_key="cart", list_endpoint=True,
             query_params=_LIST + (Param("member_id", required=True, description="회원아이디 (콤마 다중)"),)),

    # === Customer wishlist ===
    Endpoint(name="cafe24_wishlist_count", category=_C, method="GET", path=f"{_A}/customers/{{member_id}}/wishlist/count", scope=_R,
             summary="회원 관심상품 수", resource_key="count"),
    Endpoint(name="cafe24_wishlist_list", category=_C, method="GET", path=f"{_A}/customers/{{member_id}}/wishlist", scope=_R,
             summary="회원 관심상품 목록", resource_key="wishlist", list_endpoint=True),

    # === Products carts (상품별 담은 회원) ===
    Endpoint(name="cafe24_product_cart_count", category=_C, method="GET", path=f"{_A}/products/{{product_no}}/carts/count", scope=_R,
             summary="상품을 장바구니에 담은 회원 수", resource_key="count"),
    Endpoint(name="cafe24_product_cart_list", category=_C, method="GET", path=f"{_A}/products/{{product_no}}/carts", scope=_R,
             summary="상품을 장바구니에 담은 회원 목록", resource_key="cart", list_endpoint=True, query_params=_LIST),
)
