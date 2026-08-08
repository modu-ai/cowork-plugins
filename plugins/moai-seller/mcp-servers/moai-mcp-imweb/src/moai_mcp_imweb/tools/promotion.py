"""Generated tools — Promotion (프로모션 (적립금/쿠폰)). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_member_shop_point_by_filter': ('GET', '/promotion/shop-point', [], ['page', 'limit', 'memberUid', 'pointType', 'pointValue', 'unitCode'], False),
    'read_member_shop_point_log': ('GET', '/promotion/shop-point-log', [], ['page', 'limit', 'type', 'memberUid', 'memberUids', 'adminUid', 'orderNo', 'timeType', 'timeValue', 'unitCode'], False),
    'change_shop_point_by_member': ('PUT', '/promotion/shop-point/change/member/{memberUid}', ['memberUid'], [], True),
    'change_shop_point_by_group_type': ('PUT', '/promotion/shop-point/change/type', [], [], True),
    'read_one_shop_coupon_by_coupon_code': ('GET', '/promotion/shop-coupon/{shopCouponCode}', ['shopCouponCode'], ['unitCode'], False),
    'read_shop_coupon_by_filter': ('GET', '/promotion/shop-coupon', [], ['page', 'limit', 'type', 'startDateType', 'startDateValue', 'endDateType', 'endDateValue', 'editDateType', 'editDateValue', 'isUnlimitedDate', 'unitCode'], False),
    'create_shop_coupon_definition': ('POST', '/promotion/shop-coupon', [], [], True),
    'create_shop_coupon': ('POST', '/promotion/shop-coupon/{couponCode}/issue', ['couponCode'], [], True),
    'create_shop_coupon_bulk': ('POST', '/promotion/shop-coupon/{couponCode}/issue/bulk', ['couponCode'], [], True),
    'create_shop_coupon_by_group_type': ('POST', '/promotion/shop-coupon/{couponCode}/issue/group', ['couponCode'], [], True),
    'read_coupon_issue_list': ('GET', '/promotion/shop-coupon/{shopCouponCode}/coupon-issue', ['shopCouponCode'], ['page', 'memberUid', 'startDateType', 'startDateValue', 'endDateType', 'endDateValue', 'isUse', 'unitCode', 'limit'], False),
    'read_shop_coupon_issue_target_list': ('GET', '/promotion/shop-coupon/{shopCouponCode}/coupon-issue-target', ['shopCouponCode'], ['page', 'limit', 'unitCode', 'memberUid'], False),
    'read_member_shop_coupon_issue_target_list': ('GET', '/promotion/shop-coupon/member/{memberUid}/coupon-issue-target', ['memberUid'], ['page', 'limit', 'unitCode'], False),
    'read_member_coupon_issue_list': ('GET', '/promotion/shop-coupon/member/{memberUid}/coupon-issue', ['memberUid'], ['page', 'limit', 'unitCode', 'isUse'], False),
}


class ChangeShopPointByMemberBody(BaseModel):
    """요청 본문 (action='change_shop_point_by_member' [PUT /promotion/shop-point/change/member/{memberUid}]). 필수 필드: unitCode, changeType, point, reason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    changeType: str = Field(..., description='변경 타입(지급/차감)')
    point: float = Field(..., description='적립금')
    reason: str = Field(..., description='사유')


class ChangeShopPointByGroupTypeBody(BaseModel):
    """요청 본문 (action='change_shop_point_by_group_type' [PUT /promotion/shop-point/change/type]). 필수 필드: unitCode, division, groupCode, changeType, point, reason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    division: str = Field(..., description='그룹 구분 타입')
    groupCode: str = Field(..., description='그룹 코드')
    changeType: str = Field(..., description='변경 타입(지급/차감)')
    point: float = Field(..., description='적립금')
    reason: str = Field(..., description='사유')


class CreateShopCouponBody(BaseModel):
    """요청 본문 (action='create_shop_coupon' [POST /promotion/shop-coupon/{couponCode}/issue]). 필수 필드: unitCode, memberUid."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    memberUid: str = Field(..., description='아임웹 회원 아이디')


class CreateShopCouponBulkBody(BaseModel):
    """요청 본문 (action='create_shop_coupon_bulk' [POST /promotion/shop-coupon/{couponCode}/issue/bulk]). 필수 필드: unitCode, memberUids."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    memberUids: list[str] = Field(..., description='회원 아이디 목록. 최대 50명')


class CreateShopCouponByGroupTypeBody(BaseModel):
    """요청 본문 (action='create_shop_coupon_by_group_type' [POST /promotion/shop-coupon/{couponCode}/issue/group]). 필수 필드: unitCode, division, groupCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    division: str = Field(..., description='그룹 구분 타입')
    groupCode: str = Field(..., description='그룹 코드')

Body = Union[ChangeShopPointByMemberBody, ChangeShopPointByGroupTypeBody, CreateShopCouponBody, CreateShopCouponBulkBody, CreateShopCouponByGroupTypeBody]

@mcp.tool()
def imweb_promotion(action: Literal["read_member_shop_point_by_filter", "read_member_shop_point_log", "change_shop_point_by_member", "change_shop_point_by_group_type", "read_one_shop_coupon_by_coupon_code", "read_shop_coupon_by_filter", "create_shop_coupon_definition", "create_shop_coupon", "create_shop_coupon_bulk", "create_shop_coupon_by_group_type", "read_coupon_issue_list", "read_shop_coupon_issue_target_list", "read_member_shop_coupon_issue_target_list", "read_member_coupon_issue_list"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""프로모션 (적립금/쿠폰) 도구 — 14개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 14개 전체 공개).
    params: path + query 파라미터 딕셔너리. 예: {"orderNo": "ORD123", "page": 1}.
    body: POST/PATCH/PUT 본문. action 별 Body 모델(inputSchema anyOf) 중 해당 action 의 필드만 채움 (모델명 = action 의 PascalCase + Body).
    paginate: list 계열 GET 에서 전체 페이지 자동 집계 (기본 False = 단일 페이지).

Returns: API JSON."""
    _method, _path, _pp, _qp, _has_body = _OPS[action]
    _params = params or {}
    _pp_val = {k: _params[k] for k in _pp if k in _params}
    _qp_val = {k: _params[k] for k in _qp if k in _params}
    _client = get_client()
    if paginate and _method == "GET":
        return _client.list_all_pages(_path, params=_qp_val or None)
    _kw = {}
    if _pp_val:
        _kw["path_params"] = _pp_val
    if _qp_val:
        _kw["params"] = _qp_val
    if _has_body:
        _bd = body.model_dump(exclude_none=True, by_alias=True) if body else {}
        _kw["json_body"] = _bd
    return _client.request(_method, _path, **_kw)

