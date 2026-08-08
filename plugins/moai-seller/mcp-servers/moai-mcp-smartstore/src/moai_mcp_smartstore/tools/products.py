"""상품(Product) 도메인 도구 — 상품 CRUD·재고·상태·카테고리·브랜드·제조사·공지·그룹상품·이미지.

엔드포인트 상세 본문은 공식 문서(https://apicenter.commerce.naver.com) 의 대응
.md 파일을 참고. body/params 는 공식 요청 스키마를 그대로 pass-through 한다.
"""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call


# ============================================================
# 상품 검색·조회
# ============================================================


@mcp.tool()
def product_search(body: dict[str, Any]) -> dict:
    """상품 목록을 복합 조건으로 페이징 조회한다.

    POST /v1/products/search — 다건 ID 본문 전달을 위해 POST 형태.
    body 예: {"keyword": ..., "status": ..., "pageSize": 100, "pageNumber": 1}
    """
    return call("POST", "/v1/products/search", body=body)


@mcp.tool()
def product_get_origin(origin_product_no: str) -> dict:
    """원상품 1건 상세 조회. GET /v2/products/origin-products/{originProductNo}"""
    return call(
        "GET",
        f"/v2/products/origin-products/{origin_product_no}",
        endpoint=f"GET /v2/products/origin-products/{origin_product_no}",
    )


@mcp.tool()
def product_get_channel(channel_product_no: str) -> dict:
    """채널 상품 1건 상세 조회. GET /v2/products/channel-products/{channelProductNo}"""
    return call(
        "GET",
        f"/v2/products/channel-products/{channel_product_no}",
        endpoint=f"GET /v2/products/channel-products/{channel_product_no}",
    )


# ============================================================
# 상품 등록·수정·삭제
# ============================================================


@mcp.tool()
def product_create(body: dict[str, Any]) -> dict:
    """신규 상품(원상품) 등록. POST /v2/products — 카테고리/이미지/가격/재고가 실무상 필수."""
    return call("POST", "/v2/products", body=body)


@mcp.tool()
def product_update_origin(origin_product_no: str, body: dict[str, Any]) -> dict:
    """원상품 수정(전체 본문). PUT /v2/products/origin-products/{originProductNo}"""
    return call(
        "PUT",
        f"/v2/products/origin-products/{origin_product_no}",
        body=body,
        endpoint=f"PUT /v2/products/origin-products/{origin_product_no}",
    )


@mcp.tool()
def product_update_channel(channel_product_no: str, body: dict[str, Any]) -> dict:
    """채널 상품 수정(전체 본문). PUT /v2/products/channel-products/{channelProductNo}"""
    return call(
        "PUT",
        f"/v2/products/channel-products/{channel_product_no}",
        body=body,
        endpoint=f"PUT /v2/products/channel-products/{channel_product_no}",
    )


@mcp.tool()
def product_delete_origin(origin_product_no: str) -> dict:
    """원상품 삭제(비가역). DELETE /v2/products/origin-products/{originProductNo}"""
    return call(
        "DELETE",
        f"/v2/products/origin-products/{origin_product_no}",
        endpoint=f"DELETE /v2/products/origin-products/{origin_product_no}",
    )


@mcp.tool()
def product_delete_channel(channel_product_no: str) -> dict:
    """채널 상품 삭제(비가역). DELETE /v2/products/channel-products/{channelProductNo}"""
    return call(
        "DELETE",
        f"/v2/products/channel-products/{channel_product_no}",
        endpoint=f"DELETE /v2/products/channel-products/{channel_product_no}",
    )


# ============================================================
# 상태·재고·일괄 변경
# ============================================================


@mcp.tool()
def product_change_status(origin_product_no: str, body: dict[str, Any]) -> dict:
    """원상품 판매 상태(판매중/판매중지) 변경. PUT /v1/products/origin-products/{id}/change-status

    body 예: {"status": "SALE" | "OUT_OF_STOCK" | "STOP"} (공식 status enum 준용)
    """
    return call(
        "PUT",
        f"/v1/products/origin-products/{origin_product_no}/change-status",
        body=body,
    )


@mcp.tool()
def product_update_stock(origin_product_no: str, body: dict[str, Any]) -> dict:
    """원상품 옵션별 재고·가격·할인가 변경. PUT /v1/products/origin-products/{id}/option-stock

    동일 원상품 동시 호출은 직렬화 권장(정합성).
    """
    return call(
        "PUT",
        f"/v1/products/origin-products/{origin_product_no}/option-stock",
        body=body,
    )


@mcp.tool()
def product_bulk_update(body: dict[str, Any]) -> dict:
    """다건 원상품 일괄 PUT 갱신. PUT /v1/products/origin-products/bulk-update"""
    return call("PUT", "/v1/products/origin-products/bulk-update", body=body)


@mcp.tool()
def product_multi_update(body: dict[str, Any]) -> dict:
    """다건 원상품 일부 속성 일괄 변경(PATCH). PATCH /v1/products/origin-products/multi-update

    가격 일괄 인상·노출 여부 변경 등에 적합.
    """
    return call("PATCH", "/v1/products/origin-products/multi-update", body=body)


@mcp.tool()
def product_upload_images(body: dict[str, Any]) -> dict:
    """상품 이미지 다건 업로드 → 호스팅 URL 발급. POST /v1/product-images/upload"""
    return call("POST", "/v1/product-images/upload", body=body)


# ============================================================
# 카테고리·브랜드·제조사·속성·원산지
# ============================================================


@mcp.tool()
def category_list() -> dict:
    """커머스 전체 카테고리 트리 조회. GET /v1/categories"""
    return call("GET", "/v1/categories")


@mcp.tool()
def category_get(category_id: str) -> dict:
    """카테고리 1건 상세(표시명/속성/상위경로). GET /v1/categories/{categoryId}"""
    return call("GET", f"/v1/categories/{category_id}")


@mcp.tool()
def category_subcategories(category_id: str) -> dict:
    """특정 카테고리의 하위 카테고리만 조회. GET /v1/categories/{categoryId}/sub-categories"""
    return call("GET", f"/v1/categories/{category_id}/sub-categories")


@mcp.tool()
def brand_search(keyword: str = "") -> dict:
    """상품에 사용 가능한 브랜드 조회(키워드). GET /v1/product-brands"""
    params = {"keyword": keyword} if keyword else None
    return call("GET", "/v1/product-brands", params=params)


@mcp.tool()
def manufacturer_search(keyword: str = "") -> dict:
    """상품에 사용 가능한 제조사 조회(키워드). GET /v1/product-manufacturers"""
    params = {"keyword": keyword} if keyword else None
    return call("GET", "/v1/product-manufacturers", params=params)


@mcp.tool()
def product_attributes(category_id: str = "") -> dict:
    """카테고리별 상품 속성 목록. GET /v1/product-attributes/attributes?categoryId="""
    params = {"categoryId": category_id} if category_id else None
    return call("GET", "/v1/product-attributes/attributes", params=params)


@mcp.tool()
def product_origin_areas(keyword: str = "") -> dict:
    """원산지 코드 정보 전체/다건 조회. GET /v1/product-origin-areas"""
    params = {"keyword": keyword} if keyword else None
    return call("GET", "/v1/product-origin-areas", params=params)


# ============================================================
# 판매자 공지사항
# ============================================================


@mcp.tool()
def seller_notice_list(params: dict[str, Any] | None = None) -> dict:
    """판매자 공지사항 목록 조회. GET /v1/contents/seller-notices"""
    return call("GET", "/v1/contents/seller-notices", params=params)


@mcp.tool()
def seller_notice_get(seller_notice_id: str) -> dict:
    """판매자 공지사항 1건 조회. GET /v1/contents/seller-notices/{sellerNoticeId}"""
    return call("GET", f"/v1/contents/seller-notices/{seller_notice_id}")


@mcp.tool()
def seller_notice_create(body: dict[str, Any]) -> dict:
    """판매자 공지사항 신규 등록. POST /v1/contents/seller-notices"""
    return call("POST", "/v1/contents/seller-notices", body=body)


@mcp.tool()
def seller_notice_update(seller_notice_id: str, body: dict[str, Any]) -> dict:
    """판매자 공지사항 수정(전체 본문). PUT /v1/contents/seller-notices/{sellerNoticeId}"""
    return call("PUT", f"/v1/contents/seller-notices/{seller_notice_id}", body=body)


@mcp.tool()
def seller_notice_delete(seller_notice_id: str) -> dict:
    """판매자 공지사항 삭제. DELETE /v1/contents/seller-notices/{sellerNoticeId}"""
    return call("DELETE", f"/v1/contents/seller-notices/{seller_notice_id}")


# ============================================================
# 그룹상품 (표준형 옵션)
# ============================================================


@mcp.tool()
def group_product_create(body: dict[str, Any]) -> dict:
    """표준형 옵션 기반 그룹상품 신규 등록. POST /v2/standard-group-products"""
    return call("POST", "/v2/standard-group-products", body=body)


@mcp.tool()
def group_product_status(body: dict[str, Any]) -> dict:
    """그룹상품 비동기 작업 처리 결과 조회. GET /v2/standard-group-products/status"""
    return call("GET", "/v2/standard-group-products/status", params=body)


@mcp.tool()
def group_product_convert(body: dict[str, Any]) -> dict:
    """개별 상품 → 표준형 그룹상품 전환(비동기). POST /v2/standard-group-products/convert-products"""
    return call("POST", "/v2/standard-group-products/convert-products", body=body)


@mcp.tool()
def group_product_release(body: dict[str, Any]) -> dict:
    """그룹상품 그룹화 해제(개별 상품로 분리). POST /v2/standard-group-products/release-group"""
    return call("POST", "/v2/standard-group-products/release-group", body=body)


# ============================================================
# 검수(수정 요청)
# ============================================================


@mcp.tool()
def inspection_list(params: dict[str, Any] | None = None) -> dict:
    """검수 수정 요청 발생 채널 상품 목록. GET /v1/product-inspections/channel-products"""
    return call("GET", "/v1/product-inspections/channel-products", params=params)


@mcp.tool()
def inspection_restore(channel_product_no: str) -> dict:
    """검수 수정 요청 상품 복원(재노출). PUT /v1/product-inspections/channel-product/{id}/restore"""
    return call(
        "PUT",
        f"/v1/product-inspections/channel-product/{channel_product_no}/restore",
    )
