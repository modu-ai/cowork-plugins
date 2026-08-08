"""Generated tools — Payment (결제). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'confirm_bank_transfer_by_order_no': ('PATCH', '/payments/{orderNo}/bank-transfer/confirm', ['orderNo'], [], False),
}

@mcp.tool()
def imweb_payment(action: Literal["confirm_bank_transfer_by_order_no"], params: dict | None = None, body: dict | None = None, paginate: bool = False) -> dict:
    r"""결제 도구 — 1개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 1개 전체 공개).
    params: path + query 파라미터 딕셔너리. 예: {"orderNo": "ORD123", "page": 1}.
    body: 미사용 (본문이 있는 action 없음).
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
        _bd = body or {}
        _kw["json_body"] = _bd
    return _client.request(_method, _path, **_kw)

