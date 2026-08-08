"""Cafe24 Admin API — Shipping domain (배송).

배송사(carriers), 지역별 배송비(regionalsurcharges), 배송/반품 설정(shipping),
출고지(shippingorigins).

Scopes: ``mall.read_shipping`` / ``mall.write_shipping``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "shipping"
_R = "mall.read_shipping"
_W = "mall.write_shipping"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))

register(
    # === Carriers (배송사) ===
    Endpoint(name="cafe24_carrier_list", category=_C, method="GET", path=f"{_A}/carriers", scope=_R,
             summary="배송사 목록", resource_key="carrier", list_endpoint=True),
    Endpoint(name="cafe24_carrier_get", category=_C, method="GET", path=f"{_A}/carriers/{{carrier_id}}", scope=_R,
             summary="배송사 상세", resource_key="carrier"),
    Endpoint(name="cafe24_carrier_create", category=_C, method="POST", path=f"{_A}/carriers", scope=_W,
             summary="배송사 생성", resource_key="carrier", takes_body=True),
    Endpoint(name="cafe24_carrier_update", category=_C, method="PUT", path=f"{_A}/carriers/{{carrier_id}}", scope=_W,
             summary="배송사 수정 (기본배송사 설정 등)", resource_key="carrier", takes_body=True),
    Endpoint(name="cafe24_carrier_delete", category=_C, method="DELETE", path=f"{_A}/carriers/{{carrier_id}}", scope=_W,
             summary="배송사 삭제", resource_key="carrier"),

    # === Regional surcharges (지역별 배송비) ===
    Endpoint(name="cafe24_regionalsurcharge_get", category=_C, method="GET", path=f"{_A}/regionalsurcharges", scope=_R,
             summary="지역별 배송비 설정 조회", resource_key="regionalsurcharge"),
    Endpoint(name="cafe24_regionalsurcharge_update", category=_C, method="PUT", path=f"{_A}/regionalsurcharges", scope=_W,
             summary="지역별 배송비 설정 수정", resource_key="regionalsurcharge", takes_body=True),

    # === Shipping (배송/반품 설정) ===
    Endpoint(name="cafe24_shipping_get", category=_C, method="GET", path=f"{_A}/shipping", scope=_R,
             summary="배송/반품 설정 조회", resource_key="shipping"),
    Endpoint(name="cafe24_shipping_update", category=_C, method="PUT", path=f"{_A}/shipping", scope=_W,
             summary="배송/반품 설정 수정", resource_key="shipping", takes_body=True),

    # === Shipping origins (출고지) ===
    Endpoint(name="cafe24_shippingorigin_list", category=_C, method="GET", path=f"{_A}/shippingorigins", scope=_R,
             summary="출고지 목록", resource_key="shippingorigin", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_shippingorigin_get", category=_C, method="GET", path=f"{_A}/shippingorigins/{{origin_code}}", scope=_R,
             summary="출고지 상세 (품목정보 100건 이후 포함)", resource_key="shippingorigin"),
    Endpoint(name="cafe24_shippingorigin_create", category=_C, method="POST", path=f"{_A}/shippingorigins", scope=_W,
             summary="출고지 생성", resource_key="shippingorigin", takes_body=True),
    Endpoint(name="cafe24_shippingorigin_update", category=_C, method="PUT", path=f"{_A}/shippingorigins/{{origin_code}}", scope=_W,
             summary="출고지 수정", resource_key="shippingorigin", takes_body=True),
    Endpoint(name="cafe24_shippingorigin_delete", category=_C, method="DELETE", path=f"{_A}/shippingorigins/{{origin_code}}", scope=_W,
             summary="출고지 삭제 (기본/할당 출고지는 삭제 불가)", resource_key="shippingorigin"),
)
