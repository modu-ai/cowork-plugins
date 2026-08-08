"""Cafe24 Admin API — Supply domain (공급사 정보).

공급사 본체 + 공급사 운영자(suppliers/users) + 공급사 배송설정(shipping/suppliers)
+ 공급사 지역별 배송비(regionalsurcharges).

Scopes: ``mall.read_supply`` / ``mall.write_supply``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "supply"
_R = "mall.read_supply"
_W = "mall.write_supply"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))

register(
    # === Suppliers ===
    Endpoint(name="cafe24_supplier_list", category=_C, method="GET", path=f"{_A}/suppliers", scope=_R,
             summary="공급사 목록", resource_key="supplier", list_endpoint=True,
             query_params=_LIST + (Param("supplier_code"), Param("supplier_name"))),
    Endpoint(name="cafe24_supplier_count", category=_C, method="GET", path=f"{_A}/suppliers/count", scope=_R,
             summary="공급사 수", resource_key="count"),
    Endpoint(name="cafe24_supplier_get", category=_C, method="GET", path=f"{_A}/suppliers/{{supplier_code}}", scope=_R,
             summary="공급사 상세", resource_key="supplier"),
    Endpoint(name="cafe24_supplier_create", category=_C, method="POST", path=f"{_A}/suppliers", scope=_W,
             summary="공급사 생성", resource_key="supplier", takes_body=True),
    Endpoint(name="cafe24_supplier_update", category=_C, method="PUT", path=f"{_A}/suppliers/{{supplier_code}}", scope=_W,
             summary="공급사 수정", resource_key="supplier", takes_body=True),
    Endpoint(name="cafe24_supplier_delete", category=_C, method="DELETE", path=f"{_A}/suppliers/{{supplier_code}}", scope=_W,
             summary="공급사 삭제", resource_key="supplier"),

    # === Supplier shipping settings ===
    Endpoint(name="cafe24_supplier_shipping_get", category=_C, method="GET", path=f"{_A}/shipping/suppliers/{{supplier_id}}", scope=_R,
             summary="공급사 배송 설정 조회", resource_key="supplier_shipping"),
    Endpoint(name="cafe24_supplier_shipping_update", category=_C, method="PUT", path=f"{_A}/shipping/suppliers/{{supplier_id}}", scope=_W,
             summary="공급사 배송 설정 수정", resource_key="supplier_shipping", takes_body=True),

    # === Supplier users (운영자) ===
    Endpoint(name="cafe24_supplier_user_list", category=_C, method="GET", path=f"{_A}/suppliers/users", scope=_R,
             summary="공급사 운영자 목록", resource_key="supplier_user", list_endpoint=True,
             query_params=_LIST + (Param("user_id"), Param("supplier_code"), Param("supplier_name"))),
    Endpoint(name="cafe24_supplier_user_count", category=_C, method="GET", path=f"{_A}/suppliers/users/count", scope=_R,
             summary="공급사 운영자 수", resource_key="count"),
    Endpoint(name="cafe24_supplier_user_get", category=_C, method="GET", path=f"{_A}/suppliers/users/{{user_id}}", scope=_R,
             summary="공급사 운영자 상세", resource_key="supplier_user"),
    Endpoint(name="cafe24_supplier_user_create", category=_C, method="POST", path=f"{_A}/suppliers/users", scope=_W,
             summary="공급사 운영자 생성", resource_key="supplier_user", takes_body=True),
    Endpoint(name="cafe24_supplier_user_update", category=_C, method="PUT", path=f"{_A}/suppliers/users/{{user_id}}", scope=_W,
             summary="공급사 운영자 수정", resource_key="supplier_user", takes_body=True),
    Endpoint(name="cafe24_supplier_user_delete", category=_C, method="DELETE", path=f"{_A}/suppliers/users/{{user_id}}", scope=_W,
             summary="공급사 운영자 삭제", resource_key="supplier_user"),

    # === Supplier regional surcharges ===
    Endpoint(name="cafe24_supplier_regionalsurcharge_list", category=_C, method="GET",
             path=f"{_A}/suppliers/users/{{supplier_id}}/regionalsurcharges", scope=_R,
             summary="공급사 지역별 배송비 목록", resource_key="regionalsurcharge", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_supplier_regionalsurcharge_create", category=_C, method="POST",
             path=f"{_A}/suppliers/users/{{supplier_id}}/regionalsurcharges", scope=_W,
             summary="공급사 지역별 배송비 등록", resource_key="regionalsurcharge", takes_body=True),
    Endpoint(name="cafe24_supplier_regionalsurcharge_delete", category=_C, method="DELETE",
             path=f"{_A}/suppliers/users/{{supplier_id}}/regionalsurcharges/{{regional_surcharge_no}}", scope=_W,
             summary="공급사 지역별 배송비 삭제", resource_key="regionalsurcharge"),
    Endpoint(name="cafe24_supplier_regionalsurcharge_setting_get", category=_C, method="GET",
             path=f"{_A}/suppliers/users/{{supplier_id}}/regionalsurcharges/setting", scope=_R,
             summary="공급사 지역별 배송비 설정 조회", resource_key="regionalsurcharge_setting"),
    Endpoint(name="cafe24_supplier_regionalsurcharge_setting_update", category=_C, method="PUT",
             path=f"{_A}/suppliers/users/{{supplier_id}}/regionalsurcharges/setting", scope=_W,
             summary="공급사 지역별 배송비 설정 수정", resource_key="regionalsurcharge_setting", takes_body=True),
)
