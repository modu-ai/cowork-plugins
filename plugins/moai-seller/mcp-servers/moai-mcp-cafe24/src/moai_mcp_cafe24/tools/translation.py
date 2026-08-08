"""Cafe24 Admin API — Translation domain (번역).

상품분류/상품/상점/테마 다국어 번역 정보 조회 및 수정.

Scopes: ``mall.read_translation`` / ``mall.write_translation``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "translation"
_R = "mall.read_translation"
_W = "mall.write_translation"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"),
         Param("language_code", description="언어코드: ko_KR/en_US/zh_CN/zh_TW/ja_JP/vi_VN/..."))

register(
    # === Categories ===
    Endpoint(name="cafe24_translation_category_list", category=_C, method="GET", path=f"{_A}/translations/categories", scope=_R,
             summary="상품분류 번역 목록", resource_key="translation_category", list_endpoint=True,
             query_params=_LIST + (Param("category_no"),)),
    Endpoint(name="cafe24_translation_category_update", category=_C, method="PUT", path=f"{_A}/translations/categories/{{category_no}}", scope=_W,
             summary="상품분류 번역 수정 (language_code 필수)", resource_key="translation_category", takes_body=True),

    # === Products ===
    Endpoint(name="cafe24_translation_product_list", category=_C, method="GET", path=f"{_A}/translations/products", scope=_R,
             summary="상품 번역 목록", resource_key="translation_product", list_endpoint=True,
             query_params=_LIST + (Param("product_no"), Param("product_name"))),
    Endpoint(name="cafe24_translation_product_update", category=_C, method="PUT", path=f"{_A}/translations/products/{{product_no}}", scope=_W,
             summary="상품 번역 수정 (language_code 필수)", resource_key="translation_product", takes_body=True),

    # === Store ===
    Endpoint(name="cafe24_translation_store_list", category=_C, method="GET", path=f"{_A}/translations/store", scope=_R,
             summary="상점 번역 목록", resource_key="translation_store", list_endpoint=True,
             query_params=(Param("language_code"),)),
    Endpoint(name="cafe24_translation_store_update", category=_C, method="PUT", path=f"{_A}/translations/store", scope=_W,
             summary="상점 번역 수정 (language_code 필수)", resource_key="translation_store", takes_body=True),

    # === Themes ===
    Endpoint(name="cafe24_translation_theme_list", category=_C, method="GET", path=f"{_A}/translations/themes", scope=_R,
             summary="테마 번역 목록", resource_key="translation_theme", list_endpoint=True),
    Endpoint(name="cafe24_translation_theme_get", category=_C, method="GET", path=f"{_A}/translations/themes/{{skin_no}}", scope=_R,
             summary="테마 번역 상세 (필수: language_code)", resource_key="translation_theme",
             query_params=(Param("language_code", required=True),)),
    Endpoint(name="cafe24_translation_theme_update", category=_C, method="PUT", path=f"{_A}/translations/themes/{{skin_no}}", scope=_W,
             summary="테마 번역 수정 (language_code + source 필수)", resource_key="translation_theme", takes_body=True),
)
