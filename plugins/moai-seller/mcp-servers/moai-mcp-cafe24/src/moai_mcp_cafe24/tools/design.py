"""Cafe24 Admin API — Design domain (디자인).

디자인 아이콘(icons), 테마(themes), 테마 페이지(themes pages).

Scopes: ``mall.read_design`` / ``mall.write_design``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "design"
_R = "mall.read_design"
_W = "mall.write_design"
_A = "/api/v2/admin"

register(
    # === Icons ===
    Endpoint(name="cafe24_design_icon_list", category=_C, method="GET", path=f"{_A}/icons", scope=_R,
             summary="디자인 아이콘 목록 (상품/게시판/카드/이벤트)", resource_key="icon", list_endpoint=True,
             query_params=(Param("type", description="pc/mobile"),)),

    # === Themes ===
    Endpoint(name="cafe24_theme_list", category=_C, method="GET", path=f"{_A}/themes", scope=_R,
             summary="디자인(테마) 목록", resource_key="theme", list_endpoint=True,
             query_params=(Param("type", description="pc/mobile"),)),
    Endpoint(name="cafe24_theme_count", category=_C, method="GET", path=f"{_A}/themes/count", scope=_R,
             summary="디자인 수", resource_key="count",
             query_params=(Param("type", description="pc/mobile"),)),
    Endpoint(name="cafe24_theme_get", category=_C, method="GET", path=f"{_A}/themes/{{skin_no}}", scope=_R,
             summary="디자인 상세", resource_key="theme"),

    # === Theme pages ===
    Endpoint(name="cafe24_theme_page_get", category=_C, method="GET", path=f"{_A}/themes/{{skin_no}}/pages", scope=_R,
             summary="테마 페이지 조회 (필수: path)", resource_key="theme_page",
             query_params=(Param("path", required=True, description="파일 경로"),)),
    Endpoint(name="cafe24_theme_page_create", category=_C, method="POST", path=f"{_A}/themes/{{skin_no}}/pages", scope=_W,
             summary="테마 페이지 설정 (특정클라이언트)", resource_key="theme_page", takes_body=True),
    Endpoint(name="cafe24_theme_page_update", category=_C, method="PUT", path=f"{_A}/themes/{{skin_no}}/pages", scope=_W,
             summary="테마 페이지 소스 수정 (특정클라이언트)", resource_key="theme_page", takes_body=True),
    Endpoint(name="cafe24_theme_page_delete", category=_C, method="DELETE", path=f"{_A}/themes/{{skin_no}}/pages", scope=_W,
             summary="테마 페이지 삭제 (기본디자인으로 복귀, 특정클라이언트)", resource_key="theme_page",
             query_params=(Param("path", required=True),)),
)
