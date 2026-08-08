"""Generated tools — Site-Info (사이트 정보). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_one_site_info_by_site_code': ('GET', '/site-info', [], [], False),
    'read_site_menu_list': ('GET', '/site-info/menu', [], ['unitCode'], False),
    'read_one_unit_info_by_unit_code': ('GET', '/site-info/unit/{unitCode}', ['unitCode'], [], False),
    'update_ground_app_integration_complete': ('PATCH', '/site-info/integration-complete', [], [], True),
    'update_ground_app_integration_cancellation': ('PATCH', '/site-info/integration-cancellation', [], [], False),
    'update_ground_app_integration_info': ('PATCH', '/site-info/integration-info', [], [], True),
}


class UpdateGroundAppIntegrationCompleteBody(BaseModel):
    """요청 본문 (action='update_ground_app_integration_complete' [PATCH /site-info/integration-complete])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    configData: dict | None = Field(None, description='연동에 필요한 데이터 아임웹과 협의된 앱만 전달해 주세요.')


class UpdateGroundAppIntegrationInfoBody(BaseModel):
    """요청 본문 (action='update_ground_app_integration_info' [PATCH /site-info/integration-info]). 필수 필드: configData."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    configData: dict = Field(..., description='연동에 필요한 데이터 아임웹과 협의된 앱만 전달해 주세요.')

Body = Union[UpdateGroundAppIntegrationCompleteBody, UpdateGroundAppIntegrationInfoBody]

@mcp.tool()
def imweb_site_info(action: Literal["read_one_site_info_by_site_code", "read_site_menu_list", "read_one_unit_info_by_unit_code", "update_ground_app_integration_complete", "update_ground_app_integration_cancellation", "update_ground_app_integration_info"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""사이트 정보 도구 — 6개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 6개 전체 공개).
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

