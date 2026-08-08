"""Cafe24 Admin API — Promotion domain (프로모션).

Covers benefits (기간할인/재구매/대량구매/회원할인/신규상품할인/배송비할인/사은품/1+N),
commonevents (전시프로모션), coupons + issues (온라인/시리얼 쿠폰 + 발급이력),
customerevents (회원정보수정 이벤트), member coupons, discount codes, serial coupons.

Scopes: ``mall.read_promotion`` / ``mall.write_promotion``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "promotion"
_R = "mall.read_promotion"
_W = "mall.write_promotion"
_A = "/api/v2/admin"

_LIST = (Param("limit", type="int", description="최대건수"), Param("offset", type="int", description="시작위치"))

register(
    # === Benefits ===
    Endpoint(name="cafe24_benefit_list", category=_C, method="GET", path=f"{_A}/benefits", scope=_R,
             summary="혜택(할인/증정) 목록", resource_key="benefit", list_endpoint=True,
             query_params=_LIST + (Param("use_benefit", description="T/F"), Param("benefit_type", description="DP/DR/DQ/DM/DN/DV/PG/PB"), Param("benefit_name"))),
    Endpoint(name="cafe24_benefit_count", category=_C, method="GET", path=f"{_A}/benefits/count", scope=_R,
             summary="혜택 수", resource_key="count"),
    Endpoint(name="cafe24_benefit_get", category=_C, method="GET", path=f"{_A}/benefits/{{benefit_no}}", scope=_R,
             summary="혜택 상세", resource_key="benefit"),
    Endpoint(name="cafe24_benefit_create", category=_C, method="POST", path=f"{_A}/benefits", scope=_W,
             summary="혜택 생성", resource_key="benefit", takes_body=True),
    Endpoint(name="cafe24_benefit_update", category=_C, method="PUT", path=f"{_A}/benefits/{{benefit_no}}", scope=_W,
             summary="혜택 수정", resource_key="benefit", takes_body=True),
    Endpoint(name="cafe24_benefit_delete", category=_C, method="DELETE", path=f"{_A}/benefits/{{benefit_no}}", scope=_W,
             summary="혜택 삭제", resource_key="benefit"),

    # === Common events (전시프로모션) ===
    Endpoint(name="cafe24_commonevent_list", category=_C, method="GET", path=f"{_A}/commonevents", scope=_R,
             summary="전시프로모션 목록", resource_key="commonevent", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_commonevent_create", category=_C, method="POST", path=f"{_A}/commonevents", scope=_W,
             summary="전시프로모션 생성", resource_key="commonevent", takes_body=True),
    Endpoint(name="cafe24_commonevent_update", category=_C, method="PUT", path=f"{_A}/commonevents/{{event_no}}", scope=_W,
             summary="전시프로모션 수정", resource_key="commonevent", takes_body=True),
    Endpoint(name="cafe24_commonevent_delete", category=_C, method="DELETE", path=f"{_A}/commonevents/{{event_no}}", scope=_W,
             summary="전시프로모션 삭제", resource_key="commonevent"),

    # === Coupons ===
    Endpoint(name="cafe24_coupon_list", category=_C, method="GET", path=f"{_A}/coupons", scope=_R,
             summary="쿠폰 목록", resource_key="coupon", list_endpoint=True,
             query_params=_LIST + (Param("coupon_no"), Param("coupon_type", description="O 온라인/S 시리얼"), Param("benefit_type"), Param("issue_type"), Param("deleted", description="T/F"))),
    Endpoint(name="cafe24_coupon_count", category=_C, method="GET", path=f"{_A}/coupons/count", scope=_R,
             summary="쿠폰 수", resource_key="count"),
    Endpoint(name="cafe24_coupon_create", category=_C, method="POST", path=f"{_A}/coupons", scope=_W,
             summary="쿠폰 생성", resource_key="coupon", takes_body=True),
    Endpoint(name="cafe24_coupon_manage", category=_C, method="PUT", path=f"{_A}/coupons/{{coupon_no}}", scope=_W,
             summary="쿠폰 관리 (발급중지/재개/삭제)", resource_key="coupon", takes_body=True),

    # === Coupon issues (발급이력) ===
    Endpoint(name="cafe24_coupon_issue_list", category=_C, method="GET", path=f"{_A}/coupons/{{coupon_no}}/issues", scope=_R,
             summary="발급된 쿠폰 이력 목록", resource_key="coupon_issue", list_endpoint=True,
             query_params=_LIST + (Param("member_id"), Param("group_no"), Param("used_coupon", description="T/F"))),
    Endpoint(name="cafe24_coupon_issue_create", category=_C, method="POST", path=f"{_A}/coupons/{{coupon_no}}/issues", scope=_W,
             summary="쿠폰 발급", resource_key="coupon_issue", takes_body=True),

    # === Customer events (회원정보수정 이벤트) ===
    Endpoint(name="cafe24_customerevent_list", category=_C, method="GET", path=f"{_A}/customerevents", scope=_R,
             summary="회원정보수정 이벤트 목록", resource_key="customerevent", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_customerevent_create", category=_C, method="POST", path=f"{_A}/customerevents", scope=_W,
             summary="회원정보수정 이벤트 생성", resource_key="customerevent", takes_body=True),
    Endpoint(name="cafe24_customerevent_update", category=_C, method="PUT", path=f"{_A}/customerevents", scope=_W,
             summary="이벤트 상태 변경 (종료/삭제)", resource_key="customerevent", takes_body=True),

    # === Customer coupons (회원 보유 쿠폰) ===
    Endpoint(name="cafe24_customer_coupon_list", category=_C, method="GET", path=f"{_A}/customers/{{member_id}}/coupons", scope=_R,
             summary="회원 보유 쿠폰 목록", resource_key="coupon", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_customer_coupon_count", category=_C, method="GET", path=f"{_A}/customers/{{member_id}}/coupons/count", scope=_R,
             summary="회원 보유 쿠폰 수", resource_key="count"),
    Endpoint(name="cafe24_customer_coupon_delete", category=_C, method="DELETE", path=f"{_A}/customers/{{member_id}}/coupons/{{coupon_no}}", scope=_W,
             summary="회원 보유 쿠폰 삭제", resource_key="coupon"),

    # === Discount codes ===
    Endpoint(name="cafe24_discountcode_list", category=_C, method="GET", path=f"{_A}/discountcodes", scope=_R,
             summary="할인코드 목록", resource_key="discountcode", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_discountcode_get", category=_C, method="GET", path=f"{_A}/discountcodes/{{discount_code_no}}", scope=_R,
             summary="할인코드 상세", resource_key="discountcode"),
    Endpoint(name="cafe24_discountcode_create", category=_C, method="POST", path=f"{_A}/discountcodes", scope=_W,
             summary="할인코드 생성", resource_key="discountcode", takes_body=True),
    Endpoint(name="cafe24_discountcode_update", category=_C, method="PUT", path=f"{_A}/discountcodes/{{discount_code_no}}", scope=_W,
             summary="할인코드 수정", resource_key="discountcode", takes_body=True),
    Endpoint(name="cafe24_discountcode_delete", category=_C, method="DELETE", path=f"{_A}/discountcodes/{{discount_code_no}}", scope=_W,
             summary="할인코드 삭제", resource_key="discountcode"),

    # === Serial coupons ===
    Endpoint(name="cafe24_serialcoupon_list", category=_C, method="GET", path=f"{_A}/serialcoupons", scope=_R,
             summary="시리얼쿠폰 목록", resource_key="serialcoupon", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_serialcoupon_generate", category=_C, method="POST", path=f"{_A}/serialcoupons", scope=_W,
             summary="시리얼쿠폰 생성 (자동/수동)", resource_key="serialcoupon", takes_body=True),
    Endpoint(name="cafe24_serialcoupon_delete", category=_C, method="DELETE", path=f"{_A}/serialcoupons/{{coupon_no}}", scope=_W,
             summary="시리얼쿠폰 삭제", resource_key="serialcoupon"),
    Endpoint(name="cafe24_serialcoupon_issue_list", category=_C, method="GET", path=f"{_A}/serialcoupons/{{coupon_no}}/issues", scope=_R,
             summary="시리얼쿠폰 코드 발급 목록", resource_key="serialcoupon_issue", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_serialcoupon_issue_register", category=_C, method="POST", path=f"{_A}/serialcoupons/{{coupon_no}}/issues", scope=_W,
             summary="시리얼쿠폰 코드 등록 (수동)", resource_key="serialcoupon_issue", takes_body=True),
)
