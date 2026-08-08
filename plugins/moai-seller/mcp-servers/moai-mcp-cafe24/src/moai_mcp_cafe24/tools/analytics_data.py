"""Cafe24 Analytics API (cafe24data) — 24 GET endpoints.

Surface host: ``https://ca-api.cafe24data.com`` (fixed; not mall-scoped).
Scope: ``mall.read_analytics`` (접속통계 읽기권한). All endpoints are read-only.

Common parameters (mall_id is auto-injected from config when omitted):
  * ``mall_id`` (required) — 몰 아이디
  * ``shop_no`` (optional, default 1) — 샵 번호
  * ``start_date`` / ``end_date`` (required) — YYYY-MM-DD
  * ``device_type`` (optional) — pc | mobile | total
  * ``limit`` (50–1000, default 100) / ``offset`` (default 0)
  * ``sort`` / ``order`` (endpoint-specific allowed values)

Token bucket rate limit applies (IP + URL based), distinct from the Admin API
leaky bucket. 429 backoff is handled centrally in :class:`Cafe24Client`.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_CATEGORY = "analytics"
_SCOPE = "mall.read_analytics"
_SURFACE = "analytics"


def _common(*extra: Param) -> tuple[Param, ...]:
    """Standard analytics query params + any endpoint-specific extras.

    ``shop_no`` is intentionally OMITTED — the dispatcher provides a universal
    optional ``shop_no`` on every tool. ``mall_id`` is auto-injected from config.
    """
    base = (
        Param("mall_id", required=True, description="몰 아이디 (미지정 시 설정 mall_id 자동 사용)"),
        Param("start_date", required=True, description="시작일 (YYYY-MM-DD)"),
        Param("end_date", required=True, description="종료일 (YYYY-MM-DD)"),
        Param("device_type", description="디바이스 타입: pc / mobile / total"),
        Param("limit", type="int", description="응답 갯수 (최소 50, 최대 1000, 기본 100)"),
        Param("offset", type="int", description="오프셋 (기본 0)"),
    )
    return base + extra


register(
    # --- Adeffect ---
    Endpoint(
        name="cafe24_analytics_adeffect_addetails", category=_CATEGORY, method="GET",
        path="/adeffect/addetails", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="광고 상세 통계 조회 — 광고매체·검색어별 방문/구매/매출",
        resource_key="adeffect_addetail",
        query_params=_common(
            Param("sort", description="정렬: ad / keyword / visit_count / purchase_count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    # --- Carts ---
    Endpoint(
        name="cafe24_analytics_carts_action", category=_CATEGORY, method="GET",
        path="/carts/action", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="장바구니 담기 통계 — 노출수 대비 장바구니 담긴수 비교",
        resource_key="cart_action",
        query_params=_common(
            Param("sort", description="정렬: product_name / count / add_cart_count / add_cart_rate"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    # --- Members ---
    Endpoint(
        name="cafe24_analytics_members_sales", category=_CATEGORY, method="GET",
        path="/members/sales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="회원/비회원 구매건수·매출액 통계",
        resource_key="member_sale",
        query_params=_common(),
    ),
    # --- Pages ---
    Endpoint(
        name="cafe24_analytics_pages_view", category=_CATEGORY, method="GET",
        path="/pages/view", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="많이 찾는 페이지 통계 — 방문자가 가장 많이 접속한 페이지",
        resource_key="page_view",
        query_params=_common(
            Param("sort", description="정렬: url / count / visit_count / first_visit_count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    # --- Products ---
    Endpoint(
        name="cafe24_analytics_products_categorydetails", category=_CATEGORY, method="GET",
        path="/products/categorydetails", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="카테고리별 상품 판매 통계 — 판매건수/물품수/금액/담긴수",
        resource_key="product_categorydetail",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬: product_name / category_name / sales_count_per_category 등"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_products_sales", category=_CATEGORY, method="GET",
        path="/products/sales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="상품별 매출 통계 — 판매건수/물품수/매출액",
        resource_key="product_sale",
        query_params=_common(
            Param("start_datetime", description="시작일시 (YYYY-MM-DD, 시간 단위 조회용)"),
            Param("end_datetime", description="종료일시"),
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬: product_no / product_name / order_count / order_amount 등"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
        notes="결제완료(입금완료)된 주문만 집계. 타 마켓연동 주문은 제외(자사몰 매출만).",
    ),
    Endpoint(
        name="cafe24_analytics_products_view", category=_CATEGORY, method="GET",
        path="/products/view", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="상품 조회수 통계 — 상품 상세 페이지 노출 횟수",
        resource_key="product_view",
        query_params=_common(
            Param("start_datetime", description="시작일시"),
            Param("end_datetime", description="종료일시"),
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬: product_no / product_name / count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    # --- Sales ---
    Endpoint(
        name="cafe24_analytics_sales_orderdetails", category=_CATEGORY, method="GET",
        path="/sales/orderdetails", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="주문별 매출 상세 — 광고/키워드/결제수단/매출액",
        resource_key="sale_orderdetail",
        query_params=_common(
            Param("orderId", description="특정 주문번호 필터"),
            Param("sort", description="정렬: order_id / ad / keyword / payment_method / order_amount"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_sales_paymethods", category=_CATEGORY, method="GET",
        path="/sales/paymethods", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="결제수단별 통계 — 구매자수/구매건수/매출액 (결제완료일 기준)",
        resource_key="sale_paymethod",
        query_params=_common(
            Param("sort", description="정렬: payment_method / buyers_count / order_count / order_amount"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
        notes="결제취소/결제대기/할인금액/쿠폰할인은 집계 제외.",
    ),
    Endpoint(
        name="cafe24_analytics_sales_pervisitors", category=_CATEGORY, method="GET",
        path="/sales/pervisitors", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="고객 가치 평가 — 방문/구매 1인당 매출액",
        resource_key="sale_pervisitor",
        query_params=_common(),
    ),
    Endpoint(
        name="cafe24_analytics_sales_times", category=_CATEGORY, method="GET",
        path="/sales/times", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="시간대별 매출 통계 — 구매자수/구매건수/매출액",
        resource_key="sale_time",
        query_params=_common(
            Param("sort", description="정렬: hour / buyers_count / order_count / order_amount"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
        notes="결제완료(입금확인)일 기준. 네이버페이/카카오페이 포함, 타 마켓연동 제외.",
    ),
    # --- Visitors ---
    Endpoint(
        name="cafe24_analytics_visitors_dailyactive", category=_CATEGORY, method="GET",
        path="/visitors/dailyactive", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="DAU — 일별 순수 사용자 수 (중복 방문 제거)",
        resource_key="visitor_dailyactive",
        query_params=_common(
            Param("sort", description="정렬: date / user_count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitors_pageview", category=_CATEGORY, method="GET",
        path="/visitors/pageview", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="페이지뷰 통계 — 방문자가 본 페이지 총 수 (일별/시간별)",
        resource_key="visitor_pageview",
        query_params=_common(
            Param("format_type", description="데이터 형식: day(일별) / hour(시간별), 기본 day"),
            Param("sort", description="정렬: date / page_view"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitors_unique", category=_CATEGORY, method="GET",
        path="/visitors/unique", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="순 방문자수 — 중복 IP 제거한 순수 방문자",
        resource_key="visitor_unique",
        query_params=_common(
            Param("sort", description="정렬: date / unique_visit_count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitors_view", category=_CATEGORY, method="GET",
        path="/visitors/view", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="전체 방문자수 — 처음/재방문자수 분리 (세션 60분 기준)",
        resource_key="visitor_view",
        query_params=_common(
            Param("format_type", description="데이터 형식: day / hour, 기본 day"),
            Param("sort", description="정렬: date / visit_count / first_visit_count / re_visit_count"),
            Param("order", description="정렬 순서: asc / desc"),
        ),
    ),
    # --- Visitpaths ---
    Endpoint(
        name="cafe24_analytics_visitpaths_adkeywordsales", category=_CATEGORY, method="GET",
        path="/visitpaths/adkeywordsales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="광고·검색어별 구매 통계 — 광고매체/키워드별 구매건수·매출액",
        resource_key="visitpath_adkeywordsale",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 기준 (기본 ad)"),
            Param("order", description="정렬 순서 (기본 asc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_ads", category=_CATEGORY, method="GET",
        path="/visitpaths/ads", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="유입 광고 통계 — 광고매체(UTM)별 방문수",
        resource_key="visitpath_ad",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 visit_count)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
        notes="UTM source+medium 필수 권장. 광고 정보 미존재 시 '채널 없음'.",
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_adsales", category=_CATEGORY, method="GET",
        path="/visitpaths/adsales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="광고매체별 방문·구매 통계 — 네이버/다음/구글/크리테오 등",
        resource_key="visitpath_adsale",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 order_amount)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_domains", category=_CATEGORY, method="GET",
        path="/visitpaths/domains", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="유입 도메인 통계 — 참조 도메인별 방문수",
        resource_key="visitpath_domain",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 visit_count)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
        notes="참조 도메인 미존재 시 '참조 도메인 없음'(직접/즐겨찾기/앱 유입).",
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_domainsales", category=_CATEGORY, method="GET",
        path="/visitpaths/domainsales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="유입 도메인별 구매 통계 — 구매건수·매출액",
        resource_key="visitpath_domainsale",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 order_amount)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_keyworddetails", category=_CATEGORY, method="GET",
        path="/visitpaths/keyworddetails", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="검색어 상세 통계 — 검색엔진/키워드별 방문·구매·전환율·매출",
        resource_key="visitpath_keyworddetail",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 keyword)"),
            Param("order", description="정렬 순서 (기본 asc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_keywords", category=_CATEGORY, method="GET",
        path="/visitpaths/keywords", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="검색광고 키워드 방문 통계 — 키워드별 방문수",
        resource_key="visitpath_keyword",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 visit_count)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_keywordsales", category=_CATEGORY, method="GET",
        path="/visitpaths/keywordsales", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="검색광고 키워드 구매 통계 — 키워드별 구매건수·매출액",
        resource_key="visitpath_keywordsale",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 order_amount)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
    ),
    Endpoint(
        name="cafe24_analytics_visitpaths_urls", category=_CATEGORY, method="GET",
        path="/visitpaths/urls", surface=_SURFACE, scope=_SCOPE, list_endpoint=True,
        summary="유입 URL 통계 — 접속 전 웹사이트 URL별 방문수",
        resource_key="visitpath_url",
        query_params=_common(
            Param("locale", description="로케일 (기본 ko-KR)"),
            Param("origin", description="출처 필터"),
            Param("sort", description="정렬 (기본 visit_count)"),
            Param("order", description="정렬 순서 (기본 desc)"),
        ),
    ),
)
