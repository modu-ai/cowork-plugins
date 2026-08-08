"""Compile the endpoint registry into one category-dispatch tool per category.

Mirrors the moai-imweb "category-dispatch (B안)" pattern: one tool per Cafe24 API
category, dispatching its many actions through a single ``action`` enum.

Implementation note — why we render real ``def`` functions via ``exec`` rather
than hand-building an ``inspect.Signature``: FastMCP lifts per-parameter
descriptions from ``Annotated[type, Field(description=...)]`` annotations on a
*real* function definition (the path that ``@mcp.tool()`` / ``add_tool`` takes
through ``inspect.signature(fn)``). A hand-built ``inspect.Signature`` with the
same annotations is NOT read the same way — the Field descriptions silently
disappear from the tool inputSchema. Rendering each category as a real ``def``
via ``exec`` (the runtime equivalent of imweb's code-generation-to-file step)
makes the Annotated Field descriptions reach the model. The generated source is
deterministic and inspectable in any debugger via the function's __code__.

Each category tool has the shape::

    cafe24_<category>(
        action: Literal[<every action key in this category>],
        params: dict | None,      # path + query parameters
        body:   dict | None,      # POST/PUT/PATCH fields (wrapped via body_key)
        shop_no: int | None,      # universal multi-shop selector
        paginate: bool,           # auto-follow offset paging on list actions
        max_pages: int,           # cap on pages when paginating
    ) -> dict

The ``action`` Literal lifts the full per-category action catalog into the tool's
inputSchema ``enum`` — which Claude Code does NOT truncate (unlike the 2KB
description/instructions ceiling) — so a 105-action tool (order) still exposes
every action to the model. The docstring stays short.

Cafe24-specific behaviour preserved:
  * ``shop_no`` placement — GET/DELETE → query, POST/PUT/PATCH → body.
  * Analytics surface ``mall_id`` auto-injection (config-derived).
  * Dual-surface routing (admin vs analytics) per endpoint.
  * ``paginate``/``max_pages`` on list endpoints via ``Cafe24Client.list_paginated``.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .._app import mcp
from ..registry import REGISTRY, Endpoint

# Korean labels for each category — appears at the head of the tool docstring.
_CATEGORY_LABELS: dict[str, str] = {
    "analytics": "접속통계 분석 (cafe24data: 방문자·매출·광고·키워드·방문경로)",
    "analytics_admin": "분석 관리",
    "application": "앱 (installed apps / authorization)",
    "category": "상품분류 (categories)",
    "collection": "판매분류 (collections)",
    "community": "커뮤니티 (boards / Q&A / reviews)",
    "customer": "회원 (customers / groups)",
    "design": "디자인 (icons / themes / skins)",
    "mileage": "적립금 (mileage / points / credit)",
    "notification": "알림 (automail / customer invitations)",
    "order": "주문 (orders / claims / exchanges / returns)",
    "personal": "개인화 추천 (carts / wishlists)",
    "privacy": "개인정보 (privacy consents / withdrawal)",
    "product": "상품 (products / variants / options / inventories)",
    "promotion": "프로모션 (benefits / coupons / discounts / members-grade)",
    "salesreport": "매출통계 (daily / monthly / hourly reports)",
    "shipping": "배송 (carriers / shipping methods / zones)",
    "store": "스토어 (shop settings / accounts / dropshipping / 27 setting groups)",
    "supply": "공급사 (suppliers / supply amounts)",
    "translation": "번역 (category / product / etc.)",
}


def _short_key(category: str, ep: Endpoint) -> str:
    """Short action key — strip ``cafe24_{category}_`` then ``cafe24_``.

    ``cafe24_product_list`` (category=product) → ``list``;
    ``cafe24_theme_list`` (category=design, no ``design_`` segment) → ``theme_list``.
    """
    name = ep.name
    for prefix in (f"cafe24_{category}_", "cafe24_"):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def _full_key(ep: Endpoint) -> str:
    """Full post-``cafe24_`` name — globally unique, used to disambiguate collisions."""
    name = ep.name
    return name[len("cafe24_"):] if name.startswith("cafe24_") else name


def _resolve_actions(category: str, endpoints: list[Endpoint]) -> dict[str, Endpoint]:
    """Build ``action → Endpoint`` with prefix shortening + collision fallback.

    Pass 1: shorten every endpoint name to its short key. Pass 2: a short key
    that maps to exactly one endpoint wins; a colliding group falls back to each
    endpoint's full (globally-unique) name. Raises only if two endpoints share
    the same full name (impossible given a globally-unique registry).
    """
    candidates: dict[str, list[Endpoint]] = {}
    for ep in endpoints:
        candidates.setdefault(_short_key(category, ep), []).append(ep)

    ops: dict[str, Endpoint] = {}
    for short, eps in candidates.items():
        if len(eps) == 1:
            ops[short] = eps[0]
        else:
            for ep in eps:
                full = _full_key(ep)
                if full in ops:
                    raise ValueError(
                        f"unresolvable action collision in category '{category}': "
                        f"'{full}' — two endpoints share the full name"
                    )
                ops[full] = ep
    return ops


def _py_repr(v: Any) -> str:
    """repr() suitable for embedding in generated source."""
    return repr(v)


def _render_ops_table(ops: dict[str, Endpoint]) -> str:
    """Render the per-category ``_OPS`` table as source lines.

    Tuple shape: (method, path, surface, path_param_names, query_param_names, body_key, has_body, is_list)
    """
    lines: list[str] = []
    for action in sorted(ops):
        ep = ops[action]
        pp = tuple(ep.path_param_names)
        qp = tuple(p.name for p in ep.query_params)
        bk = ep.resolved_body_key
        lines.append(
            "    "
            + _py_repr(action)
            + f": ({ep.method!r}, {ep.path!r}, {ep.surface!r}, {pp!r}, {qp!r}, "
            f"{bk!r}, {ep.takes_body!r}, {ep.list_endpoint!r}),"
        )
    return "\n".join(lines)


def _render_category_source(category: str, ops: dict[str, Endpoint]) -> str:
    """Render one category-dispatch tool as real Python source (exec'd at compile)."""
    label = _CATEGORY_LABELS.get(category, category)
    actions = sorted(ops)
    actions_lit = ", ".join(f"{a!r}" for a in actions)
    n = len(actions)
    ops_table = _render_ops_table(ops)

    src = f'''"""Generated category-dispatch tool — {category} ({label}).

DO NOT EDIT by hand; the source is rendered at runtime by
:mod:`moai_mcp_cafe24.tools._dispatch._render_category_source` from the endpoint
registry. {n} actions are dispatched via the ``action`` Literal enum below.
"""

from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import Field

from moai_mcp_cafe24._app import mcp  # noqa: F401 — mcp is the registration target in register_all
from moai_mcp_cafe24._base import get_client
from moai_mcp_cafe24.client import SURFACE_ANALYTICS as _SURFACE_ANALYTICS

# action -> (method, path, surface, path_param_names, query_param_names, body_key, has_body, is_list)
_OPS: dict[str, tuple] = {{
{ops_table}
}}


def cafe24_{category}(
    action: Annotated[
        Literal[{actions_lit}],
        Field(description="수행 작업 키 (inputSchema enum 으로 {n}개 전체 공개)"),
    ],
    params: Annotated[
        Optional[dict],
        Field(description="path + query 파라미터 딕셔너리. 예: {{'product_no': 123, 'limit': 50}}"),
    ] = None,
    body: Annotated[
        Optional[dict],
        Field(description="POST/PUT/PATCH 본문 필드 (action 별 body_key 래핑 자동)"),
    ] = None,
    shop_no: Annotated[
        Optional[int],
        Field(description="multi-shop number (GET/DELETE→query, POST/PUT→body 자동 배치)"),
    ] = None,
    paginate: Annotated[
        bool, Field(description="list 계열 action 전체 페이지 자동 집계 (기본 False)")
    ] = False,
    max_pages: Annotated[
        int, Field(description="페이지네이션 시 최대 페이지 (기본 50)")
    ] = 50,
) -> dict:
    """{label} 도구 — {n}개 action 을 디스패치합니다.

    Args:
        action: 수행 작업 키 (inputSchema enum 으로 {n}개 전체 공개).
        params: path + query 파라미터 딕셔너리.
        body: POST/PUT/PATCH 본문 필드 (action 별 body_key 래핑 자동).
        shop_no: 멀티샵 번호 (GET/DELETE→query, POST/PUT→body 자동 배치).
        paginate: list 계열 action 전체 페이지 자동 집계 (기본 False).
        max_pages: 페이지네이션 시 최대 페이지 (기본 50).

    Returns:
        API JSON. Analytics 계열은 mall_id 자동 주입, 이중 레이트리밋 자동 준수.
    """
    _method, _path, _surface, _pp, _qp, _body_key, _has_body, _is_list = _OPS[action]
    _client = get_client()
    _params = params or {{}}
    _path_params = {{k: _params[k] for k in _pp if k in _params}}
    _query = {{k: _params[k] for k in _qp if k in _params}}
    if shop_no is not None:
        if _method in ("GET", "DELETE"):
            _query["shop_no"] = shop_no
        else:
            body = dict(body or {{}})
            body.setdefault("shop_no", shop_no)
    if _surface == _SURFACE_ANALYTICS and not _query.get("mall_id"):
        _query["mall_id"] = _client.config.mall_id
    _json_body = None
    if _has_body and body is not None:
        _json_body = {{_body_key: body}} if _body_key else body
    if _is_list and paginate:
        return _client.list_paginated(
            _path, surface=_surface, params=_query or None, max_pages=max_pages
        )
    return _client.request(
        _method,
        _path,
        surface=_surface,
        path_params=_path_params or None,
        params=_query or None,
        json_body=_json_body,
    )
'''
    return src


def _compile_category(category: str, endpoints: list[Endpoint]) -> Any:
    """Render + exec one category tool, returning the registered function.

    The exec'd source uses ``@mcp.tool()`` so the tool self-registers; this
    function returns the function object for parity/testing. The real-function
    path is what lets FastMCP lift the Annotated Field descriptions into the
    tool inputSchema (per-parameter descriptions).
    """
    ops = _resolve_actions(category, endpoints)
    src = _render_category_source(category, ops)
    filename = f"<moai_mcp_cafe24:generated:{category}>"
    ns: dict[str, Any] = {"__name__": f"moai_mcp_cafe24._generated_{category}"}
    exec(compile(src, filename, "exec"), ns)  # noqa: S102 — deterministic local render
    return ns[f"cafe24_{category}"]


def _tool_meta(category: str, endpoints: list[Endpoint]) -> dict[str, Any]:
    """Per-tool ``_meta`` — list-bearing categories raise the persist-to-disk ceiling.

    A list action can return up to ``max_pages × page_size`` rows (default
    50 × 100 = 5,000 rows) in one response, exceeding the MCP 25K default limit
    and being silently truncated. Declare a raised ceiling so the host keeps the
    full result inline. Per-call token budget still applies.
    """
    if any(ep.list_endpoint for ep in endpoints):
        return {"anthropic/maxResultSizeChars": 200000}
    return {}


def register_all() -> int:
    """Register one category-dispatch tool per Cafe24 API category.

    The exec'd source already self-registers via ``@mcp.tool()``; this function
    additionally sets the per-tool ``_meta`` (maxResultSizeChars for list-bearing
    categories) by re-adding with meta. Returns the number of tools registered.

    Idempotent guard prevents duplicate registration across re-imports.
    """
    by_cat: dict[str, list[Endpoint]] = defaultdict(list)
    for ep in REGISTRY.all():
        by_cat[ep.category].append(ep)

    count = 0
    for category, eps in sorted(by_cat.items()):
        fn = _compile_category(category, eps)
        try:
            # Re-add with meta so list-bearing categories get the raised ceiling.
            # FastMCP treats a re-add of an existing name as upsert (or raises,
            # which we treat as already-registered-without-meta and skip).
            mcp.add_tool(
                fn,
                name=f"cafe24_{category}",
                description=fn.__doc__,
                meta=_tool_meta(category, eps),
            )
        except Exception:
            # Already registered by @mcp.tool(); meta upgrade is best-effort.
            pass
        count += 1
    return count
