"""Cafe24 Admin API — Collection domain (판매분류).

판매분류(브랜드/자체분류/제조사/원산지/트렌드) 관리.

Scopes: ``mall.read_collection`` / ``mall.write_collection``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "collection"
_R = "mall.read_collection"
_W = "mall.write_collection"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))

register(
    # === Brands ===
    Endpoint(name="cafe24_brand_list", category=_C, method="GET", path=f"{_A}/brands", scope=_R,
             summary="브랜드 목록", resource_key="brand", list_endpoint=True,
             query_params=_LIST + (Param("brand_code"), Param("brand_name"), Param("use_brand", description="T/F"))),
    Endpoint(name="cafe24_brand_count", category=_C, method="GET", path=f"{_A}/brands/count", scope=_R,
             summary="브랜드 수", resource_key="count"),
    Endpoint(name="cafe24_brand_create", category=_C, method="POST", path=f"{_A}/brands", scope=_W,
             summary="브랜드 생성", resource_key="brand", takes_body=True),
    Endpoint(name="cafe24_brand_update", category=_C, method="PUT", path=f"{_A}/brands/{{brand_code}}", scope=_W,
             summary="브랜드 수정", resource_key="brand", takes_body=True),
    Endpoint(name="cafe24_brand_delete", category=_C, method="DELETE", path=f"{_A}/brands/{{brand_code}}", scope=_W,
             summary="브랜드 삭제", resource_key="brand"),

    # === Classifications (자체분류) ===
    Endpoint(name="cafe24_classification_list", category=_C, method="GET", path=f"{_A}/classifications", scope=_R,
             summary="자체분류 목록", resource_key="classification", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_classification_count", category=_C, method="GET", path=f"{_A}/classifications/count", scope=_R,
             summary="자체분류 수", resource_key="count"),

    # === Manufacturers (제조사) ===
    Endpoint(name="cafe24_manufacturer_list", category=_C, method="GET", path=f"{_A}/manufacturers", scope=_R,
             summary="제조사 목록", resource_key="manufacturer", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_manufacturer_get", category=_C, method="GET", path=f"{_A}/manufacturers/{{manufacturer_code}}", scope=_R,
             summary="제조사 상세", resource_key="manufacturer"),
    Endpoint(name="cafe24_manufacturer_count", category=_C, method="GET", path=f"{_A}/manufacturers/count", scope=_R,
             summary="제조사 수", resource_key="count"),
    Endpoint(name="cafe24_manufacturer_create", category=_C, method="POST", path=f"{_A}/manufacturers", scope=_W,
             summary="제조사 생성", resource_key="manufacturer", takes_body=True),
    Endpoint(name="cafe24_manufacturer_update", category=_C, method="PUT", path=f"{_A}/manufacturers/{{manufacturer_code}}", scope=_W,
             summary="제조사 수정", resource_key="manufacturer", takes_body=True),

    # === Origin (원산지) ===
    Endpoint(name="cafe24_origin_list", category=_C, method="GET", path=f"{_A}/origin", scope=_R,
             summary="원산지 목록", resource_key="origin", list_endpoint=True,
             query_params=_LIST + (Param("origin_place_no"), Param("origin_place_name"), Param("foreign", description="T/F"))),

    # === Trends (트렌드) ===
    Endpoint(name="cafe24_trend_list", category=_C, method="GET", path=f"{_A}/trends", scope=_R,
             summary="트렌드 목록", resource_key="trend", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_trend_count", category=_C, method="GET", path=f"{_A}/trends/count", scope=_R,
             summary="트렌드 수", resource_key="count"),
)
