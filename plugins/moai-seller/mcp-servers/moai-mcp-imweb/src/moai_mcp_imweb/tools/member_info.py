"""Generated tools — Member-Info (회원 정보). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_member_info_list': ('GET', '/member-info/members', [], ['page', 'limit', 'joinTimeRangeType', 'joinTimeRangeValue', 'lastLoginTimeRangeType', 'lastLoginTimeRangeValue', 'unitCode', 'memberCode', 'memberUid', 'smsAgree', 'emailAgree', 'thirdPartyAgree', 'callnum'], False),
    'read_member_info_list_by_cursor': ('GET', '/member-info/members/cursor', [], ['joinTimeRangeType', 'joinTimeRangeValue', 'lastLoginTimeRangeType', 'lastLoginTimeRangeValue', 'cursor', 'direction', 'limit', 'unitCode', 'smsAgree', 'emailAgree', 'thirdPartyAgree', 'callnum', 'editTimeRangeType', 'editTimeRangeValue'], False),
    'read_all_shop_prod_wish_by_prod_no': ('GET', '/member-info/members/product/wish-list', [], ['page', 'limit', 'prodNo'], False),
    'read_all_shop_order_cart_by_prod_no': ('GET', '/member-info/members/product/carts', [], ['page', 'limit', 'prodNo', 'unitCode'], False),
    'read_one_member_info_by_unit_code_and_member_uid': ('GET', '/member-info/members/{memberUid}', ['memberUid'], ['unitCode'], False),
    'read_member_group_list_by_site_code': ('GET', '/member-info/groups', [], ['page', 'limit'], False),
    'read_member_group_member_list': ('GET', '/member-info/groups/{memberGroupCode}/members', ['memberGroupCode'], ['page', 'limit', 'unitCode'], False),
    'read_member_grade_list_by_site_code': ('GET', '/member-info/grades', [], ['page', 'limit'], False),
    'read_member_list_by_member_grade': ('GET', '/member-info/grades/members', [], ['page', 'limit', 'unitCode', 'isDefaultGrade', 'memberGradeCode'], False),
    'read_admin_group_list': ('GET', '/member-info/admin/groups', [], ['page', 'limit'], False),
    'read_admin_group_member_list': ('GET', '/member-info/admin/groups/{siteGroupCode}/members', ['siteGroupCode'], ['page', 'limit', 'unitCode'], False),
    'read_one_admin_info_by_admin_uid': ('GET', '/member-info/admin/{adminUid}', ['adminUid'], [], False),
    'update_member_agree_info': ('PATCH', '/member-info/members/{memberUid}/agree-info', ['memberUid'], [], True),
    'update_member_group': ('PUT', '/member-info/members/{memberUid}/groups', ['memberUid'], [], True),
    'bulk_update_member_group': ('PUT', '/member-info/members/groups/bulk', [], [], True),
    'update_member_grade_by_member_uid': ('PUT', '/member-info/members/{memberUid}/grade', ['memberUid'], [], True),
    'bulk_update_member_grade': ('PUT', '/member-info/members/grades/bulk', [], [], True),
    'read_all_shop_prod_wish_by_member_uid': ('GET', '/member-info/members/{memberUid}/wish-list', ['memberUid'], [], False),
    'read_member_cart_list_by_member_uid': ('GET', '/member-info/members/{memberUid}/carts', ['memberUid'], ['unitCode'], False),
}


class UpdateMemberAgreeInfoBody(BaseModel):
    """요청 본문 (action='update_member_agree_info' [PATCH /member-info/members/{memberUid}/agree-info])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    smsAgree: str | None = Field(None, description='sms 수신 동의 여부')
    emailAgree: str | None = Field(None, description='email 수신 동의 여부')
    thirdPartyAgree: str | None = Field(None, description='제 3자 정보제공 동의 여부')


class UpdateMemberGroupBody(BaseModel):
    """요청 본문 (action='update_member_group' [PUT /member-info/members/{memberUid}/groups]). 필수 필드: unitCode, groupCodes."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    groupCodes: list[str] = Field(..., description='변경할 회원 그룹 코드 리스트')


class BulkUpdateMemberGroupBody(BaseModel):
    """요청 본문 (action='bulk_update_member_group' [PUT /member-info/members/groups/bulk]). 필수 필드: unitCode, memberUids, groupCodes."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    memberUids: list[str] = Field(..., description='그룹을 변경할 회원 ID 목록 (최대 30건)')
    groupCodes: list[str] = Field(..., description='최종 적용할 회원 그룹 코드 리스트')


class UpdateMemberGradeByMemberUidBody(BaseModel):
    """요청 본문 (action='update_member_grade_by_member_uid' [PUT /member-info/members/{memberUid}/grade]). 필수 필드: unitCode, isDefaultGrade, memberGradeCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    isDefaultGrade: str = Field(..., description='기본 등급 여부')
    useAutoGrade: str | None = Field(None, description='자동 등급 사용 여부')
    memberGradeCode: str = Field(..., description='변경할 회원 등급 코드')


class BulkUpdateMemberGradeBody(BaseModel):
    """요청 본문 (action='bulk_update_member_grade' [PUT /member-info/members/grades/bulk]). 필수 필드: unitCode, memberUids, isDefaultGrade."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    memberUids: list[str] = Field(..., description='등급을 변경할 회원 ID 목록 (최대 30건)')
    isDefaultGrade: str = Field(..., description='기본 등급 여부')
    useAutoGrade: str | None = Field(None, description='자동 등급 사용 여부')
    memberGradeCode: str | None = Field(None, description='변경할 회원 등급 코드')

Body = Union[UpdateMemberAgreeInfoBody, UpdateMemberGroupBody, BulkUpdateMemberGroupBody, UpdateMemberGradeByMemberUidBody, BulkUpdateMemberGradeBody]

@mcp.tool()
def imweb_member_info(action: Literal["read_member_info_list", "read_member_info_list_by_cursor", "read_all_shop_prod_wish_by_prod_no", "read_all_shop_order_cart_by_prod_no", "read_one_member_info_by_unit_code_and_member_uid", "read_member_group_list_by_site_code", "read_member_group_member_list", "read_member_grade_list_by_site_code", "read_member_list_by_member_grade", "read_admin_group_list", "read_admin_group_member_list", "read_one_admin_info_by_admin_uid", "update_member_agree_info", "update_member_group", "bulk_update_member_group", "update_member_grade_by_member_uid", "bulk_update_member_grade", "read_all_shop_prod_wish_by_member_uid", "read_member_cart_list_by_member_uid"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""회원 정보 도구 — 19개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 19개 전체 공개).
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

