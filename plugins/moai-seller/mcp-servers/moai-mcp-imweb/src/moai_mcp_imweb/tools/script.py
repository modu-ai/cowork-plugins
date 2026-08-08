"""Generated tools — Script (스크립트). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_script_by_unit_code': ('GET', '/script', [], ['unitCode', 'position'], False),
    'create_script': ('POST', '/script', [], [], True),
    'update_script': ('PUT', '/script', [], [], True),
    'delete_script': ('DELETE', '/script', [], ['unitCode', 'position'], False),
}


class CreateScriptBody(BaseModel):
    """요청 본문 (action='create_script' [POST /script]). 필수 필드: unitCode, position, scriptContent."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    position: str = Field(..., description='스크립트 삽입 위치입니다. - header: 헤더 영역 - body: 바디 영역 - footer: 푸터 영역 - product_detail: 상품 상세 페이지 - login: 로그인 페이지 - cart: 장바구니 페이지 - join: 회원가입 페이지 - mypage: 마이페이지 - sh…')
    scriptContent: str = Field(..., description='스크립트 내용')


class UpdateScriptBody(BaseModel):
    """요청 본문 (action='update_script' [PUT /script]). 필수 필드: unitCode, position, scriptContent."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    position: str = Field(..., description='스크립트 삽입 위치입니다. - header: 헤더 영역 - body: 바디 영역 - footer: 푸터 영역 - product_detail: 상품 상세 페이지 - login: 로그인 페이지 - cart: 장바구니 페이지 - join: 회원가입 페이지 - mypage: 마이페이지 - sh…')
    scriptContent: str = Field(..., description='스크립트 내용')

Body = Union[CreateScriptBody, UpdateScriptBody]

@mcp.tool()
def imweb_script(action: Literal["read_script_by_unit_code", "create_script", "update_script", "delete_script"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""스크립트 도구 — 4개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 4개 전체 공개).
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

