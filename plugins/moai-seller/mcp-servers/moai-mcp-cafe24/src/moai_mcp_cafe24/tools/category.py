"""Cafe24 Admin API — Category domain (상품분류).

Covers autodisplay (자동진열), categories CRUD (상품분류), categories
decorationimages & seo, and mains (메인분류) CRUD.

NOTE: the *products-within-a-category* relations live in :mod:`product`
(``cafe24_category_product_*`` / ``cafe24_main_product_*``) because they carry
read_product/write_product scopes.

Scopes: ``mall.read_category`` / ``mall.write_category``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "category"
_R = "mall.read_category"
_W = "mall.write_category"
_A = "/api/v2/admin"

_LIST = (Param("limit", type="int", description="최대건수 (최대 100)"), Param("offset", type="int", description="시작위치"))

register(
    # === Categories (상품분류) ===
    Endpoint(name="cafe24_category_list", category=_C, method="GET", path=f"{_A}/categories", scope=_R,
             summary="상품분류 목록", resource_key="category", list_endpoint=True,
             query_params=_LIST + (Param("category_depth", type="int", description="1~4"),
                                   Param("category_no"), Param("parent_category_no", description="1=대분류"), Param("category_name"))),
    Endpoint(name="cafe24_category_count", category=_C, method="GET", path=f"{_A}/categories/count", scope=_R,
             summary="상품분류 수", resource_key="count"),
    Endpoint(name="cafe24_category_get", category=_C, method="GET", path=f"{_A}/categories/{{category_no}}", scope=_R,
             summary="상품분류 상세", resource_key="category"),
    Endpoint(name="cafe24_category_create", category=_C, method="POST", path=f"{_A}/categories", scope=_W,
             summary="상품분류 생성 (category_name 필수)", resource_key="category", takes_body=True),
    Endpoint(name="cafe24_category_update", category=_C, method="PUT", path=f"{_A}/categories/{{category_no}}", scope=_W,
             summary="상품분류 수정", resource_key="category", takes_body=True),
    Endpoint(name="cafe24_category_delete", category=_C, method="DELETE", path=f"{_A}/categories/{{category_no}}", scope=_W,
             summary="상품분류 삭제", resource_key="category"),

    # === Categories decorationimages ===
    Endpoint(name="cafe24_category_decorationimage_get", category=_C, method="GET", path=f"{_A}/categories/{{category_no}}/decorationimages", scope=_R,
             summary="분류 꾸미기 이미지 조회", resource_key="category_decorationimage"),
    Endpoint(name="cafe24_category_decorationimage_update", category=_C, method="PUT", path=f"{_A}/categories/{{category_no}}/decorationimages", scope=_W,
             summary="분류 꾸미기 이미지 수정", resource_key="category_decorationimage", takes_body=True),

    # === Categories SEO ===
    Endpoint(name="cafe24_category_seo_get", category=_C, method="GET", path=f"{_A}/categories/{{category_no}}/seo", scope=_R,
             summary="분류 SEO 조회", resource_key="category_seo"),
    Endpoint(name="cafe24_category_seo_update", category=_C, method="PUT", path=f"{_A}/categories/{{category_no}}/seo", scope=_W,
             summary="분류 SEO 수정", resource_key="category_seo", takes_body=True),

    # === Autodisplay (자동진열) ===
    Endpoint(name="cafe24_autodisplay_list", category=_C, method="GET", path=f"{_A}/autodisplay", scope=_R,
             summary="자동진열 목록", resource_key="autodisplay", list_endpoint=True),
    Endpoint(name="cafe24_autodisplay_create", category=_C, method="POST", path=f"{_A}/autodisplay", scope=_W,
             summary="자동진열 생성", resource_key="autodisplay", takes_body=True),
    Endpoint(name="cafe24_autodisplay_update", category=_C, method="PUT", path=f"{_A}/autodisplay/{{display_no}}", scope=_W,
             summary="자동진열 수정", resource_key="autodisplay", takes_body=True),
    Endpoint(name="cafe24_autodisplay_delete", category=_C, method="DELETE", path=f"{_A}/autodisplay/{{display_no}}", scope=_W,
             summary="자동진열 삭제", resource_key="autodisplay"),

    # === Mains (메인분류 CRUD) ===
    Endpoint(name="cafe24_main_list", category=_C, method="GET", path=f"{_A}/mains", scope=_R,
             summary="메인분류 목록", resource_key="main", list_endpoint=True),
    Endpoint(name="cafe24_main_create", category=_C, method="POST", path=f"{_A}/mains", scope=_W,
             summary="메인분류 추가", resource_key="main", takes_body=True),
    Endpoint(name="cafe24_main_update", category=_C, method="PUT", path=f"{_A}/mains/{{display_group}}", scope=_W,
             summary="메인분류 수정", resource_key="main", takes_body=True),
    Endpoint(name="cafe24_main_delete", category=_C, method="DELETE", path=f"{_A}/mains/{{display_group}}", scope=_W,
             summary="메인분류 삭제", resource_key="main"),
)
