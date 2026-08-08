"""Cafe24 Admin API — Product domain (상품).

Covers: Products + variants/options/inventories, images/additionalimages,
memos, SEO, tags, icons, decorationimages, discountprice, hits, approve,
customproperties (per-product + global), properties (field config),
bundleproducts (세트상품), categories↔products & mains↔products relations,
and categories/mains properties (list field config).

Scopes: ``mall.read_product`` / ``mall.write_product``.
Base host: ``https://{mall_id}.cafe24api.com``, prefix ``/api/v2/admin``.

The ``body`` argument on write tools accepts the full Cafe24 field set (see docs);
the dispatcher wraps it as ``{"<resource_key>": body}``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "product"
_R = "mall.read_product"
_W = "mall.write_product"
_P = "/api/v2/admin/products"

# Standard list pagination/filter params reused across product lists.
_LIST = (
    Param("limit", type="int", description="조회결과 최대건수 (기본 10, 최대 100)"),
    Param("offset", type="int", description="조회결과 시작위치 (products: 최대 5000)"),
)
_PRODUCT_FILTERS = _LIST + (
    Param("product_no", description="상품번호 (콤마로 다중)"),
    Param("product_code", description="상품코드 (콤마로 다중)"),
    Param("product_name", description="상품명 (콤마로 다중)"),
    Param("display", description="진열상태: T / F"),
    Param("selling", description="판매상태: T / F"),
    Param("brand_code", description="브랜드코드 (콤마로 다중)"),
    Param("category", description="분류 번호"),
    Param("created_start_date", description="등록일 시작 (YYYY-MM-DD)"),
    Param("created_end_date", description="등록일 종료"),
    Param("since_product_no", type="int", description="이 상품번호 이후 조회 (5000+ 초과시)"),
    Param("sort", description="정렬: created_date / updated_date / product_name"),
    Param("order", description="asc / desc"),
    Param("fields", description="특정 항목만 조회 (콤마 구분)"),
    Param("embed", description="하위 리소스 동시 조회: variants,inventories 등"),
)

register(
    # === Products (main) ===
    Endpoint(name="cafe24_product_list", category=_C, method="GET", path=f"{_P}", scope=_R,
             summary="상품 목록 조회", resource_key="product", list_endpoint=True, query_params=_PRODUCT_FILTERS,
             notes="offset 최대 5000. 그 이상은 since_product_no 사용. 1회당 최대 100건."),
    Endpoint(name="cafe24_product_count", category=_C, method="GET", path=f"{_P}/count", scope=_R,
             summary="상품 수 조회", resource_key="count", query_params=_PRODUCT_FILTERS),
    Endpoint(name="cafe24_product_get", category=_C, method="GET", path=f"{_P}/{{product_no}}", scope=_R,
             summary="상품 상세 조회", resource_key="product",
             query_params=(Param("embed", description="하위 리소스: variants,memos,hits,seo,tags,options,discountprice"),)),
    Endpoint(name="cafe24_product_create", category=_C, method="POST", path=f"{_P}", scope=_W,
             summary="상품 생성", resource_key="product", takes_body=True,
             description="필수: product_name, supply_price (또는 calculate_price_based_on=B 시 price_excluding_tax). price 권장."),
    Endpoint(name="cafe24_product_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}", scope=_W,
             summary="상품 수정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_product_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}", scope=_W,
             summary="상품 삭제 (하위 품목/옵션 포함)", resource_key="product"),

    # === Variants (품목) ===
    Endpoint(name="cafe24_product_variant_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/variants", scope=_R,
             summary="품목(variants) 목록 조회", resource_key="variant", list_endpoint=True,
             query_params=_LIST + (Param("embed", description="inventories: 재고 동시 조회"),)),
    Endpoint(name="cafe24_product_variant_get", category=_C, method="GET", path=f"{_P}/{{product_no}}/variants/{{variant_code}}", scope=_R,
             summary="특정 품목 조회", resource_key="variant"),
    Endpoint(name="cafe24_product_variant_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/variants/{{variant_code}}", scope=_W,
             summary="품목 수정 (진열/판매/재고/추가금액 등)", resource_key="variant", takes_body=True),
    Endpoint(name="cafe24_product_variant_update_bulk", category=_C, method="PUT", path=f"{_P}/{{product_no}}/variants", scope=_W,
             summary="품목 일괄 수정 (최대 100건)", resource_key="variant", takes_body=True, body_key="variants"),
    Endpoint(name="cafe24_product_variant_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/variants/{{variant_code}}", scope=_W,
             summary="품목 삭제", resource_key="variant"),

    # === Variant inventories (재고) ===
    Endpoint(name="cafe24_product_variant_inventory_get", category=_C, method="GET",
             path=f"{_P}/{{product_no}}/variants/{{variant_code}}/inventories", scope=_R,
             summary="품목 재고 상세 조회", resource_key="inventory"),
    Endpoint(name="cafe24_product_variant_inventory_update", category=_C, method="PUT",
             path=f"{_P}/{{product_no}}/variants/{{variant_code}}/inventories", scope=_W,
             summary="품목 재고 수정 (수량/중요재고/품절표시 등)", resource_key="inventory", takes_body=True),

    # === Options ===
    Endpoint(name="cafe24_product_option_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/options", scope=_R,
             summary="상품 옵션 조회", resource_key="option", list_endpoint=True),
    Endpoint(name="cafe24_product_option_create", category=_C, method="POST", path=f"{_P}/{{product_no}}/options", scope=_W,
             summary="상품 옵션 생성 (품목 자동 생성됨)", resource_key="option", takes_body=True),
    Endpoint(name="cafe24_product_option_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/options", scope=_W,
             summary="상품 옵션 수정 (옵션항목 추가/삭제 불가, 품목 초기화 안됨)", resource_key="option", takes_body=True),
    Endpoint(name="cafe24_product_option_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/options", scope=_W,
             summary="상품 옵션 삭제 (기존 품목도 함께 삭제 주의)", resource_key="option"),

    # === Images ===
    Endpoint(name="cafe24_product_image_upload", category=_C, method="POST", path=f"{_P}/{{product_no}}/images", scope=_W,
             summary="상품 이미지 업로드 (Base64)", resource_key="image", takes_body=True,
             description="필수: image_upload_type (A 대표/B 개별). image 용량제한 10MB, 호출당 30MB."),
    Endpoint(name="cafe24_product_image_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/images", scope=_W,
             summary="상품 이미지 전체 삭제", resource_key="image"),
    Endpoint(name="cafe24_product_additionalimage_create", category=_C, method="POST", path=f"{_P}/{{product_no}}/additionalimages", scope=_W,
             summary="추가 이미지 등록 (최대 20개, Base64)", resource_key="additionalimage", takes_body=True, body_key="additionalimages"),
    Endpoint(name="cafe24_product_additionalimage_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/additionalimages", scope=_W,
             summary="추가 이미지 수정", resource_key="additionalimage", takes_body=True, body_key="additionalimages"),
    Endpoint(name="cafe24_product_additionalimage_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/additionalimages", scope=_W,
             summary="추가 이미지 삭제", resource_key="additionalimage"),

    # === Memos ===
    Endpoint(name="cafe24_product_memo_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/memos", scope=_R,
             summary="상품 메모 목록 조회", resource_key="memo", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_product_memo_get", category=_C, method="GET", path=f"{_P}/{{product_no}}/memos/{{memo_no}}", scope=_R,
             summary="상품 메모 상세 조회", resource_key="memo"),
    Endpoint(name="cafe24_product_memo_create", category=_C, method="POST", path=f"{_P}/{{product_no}}/memos", scope=_W,
             summary="상품 메모 등록", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_product_memo_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/memos/{{memo_no}}", scope=_W,
             summary="상품 메모 수정", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_product_memo_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/memos/{{memo_no}}", scope=_W,
             summary="상품 메모 삭제", resource_key="memo"),

    # === SEO ===
    Endpoint(name="cafe24_product_seo_get", category=_C, method="GET", path=f"{_P}/{{product_no}}/seo", scope=_R,
             summary="상품 SEO 설정 조회", resource_key="seo"),
    Endpoint(name="cafe24_product_seo_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/seo", scope=_W,
             summary="상품 SEO 설정 수정", resource_key="seo", takes_body=True),

    # === Tags ===
    Endpoint(name="cafe24_product_tag_count", category=_C, method="GET", path=f"{_P}/{{product_no}}/tags/count", scope=_R,
             summary="상품 태그 수 조회", resource_key="count"),
    Endpoint(name="cafe24_product_tag_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/tags", scope=_R,
             summary="상품 태그 목록 조회", resource_key="tag", list_endpoint=True),
    Endpoint(name="cafe24_product_tag_create", category=_C, method="POST", path=f"{_P}/{{product_no}}/tags", scope=_W,
             summary="상품 태그 등록 (최대 100)", resource_key="tag", takes_body=True, body_key="tags"),
    Endpoint(name="cafe24_product_tag_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/tags/{{tag}}", scope=_W,
             summary="상품 태그 삭제", resource_key="tag"),

    # === Icons ===
    Endpoint(name="cafe24_product_icon_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/icons", scope=_R,
             summary="상품에 등록된 아이콘 조회", resource_key="icon", list_endpoint=True),
    Endpoint(name="cafe24_product_icon_set", category=_C, method="POST", path=f"{_P}/{{product_no}}/icons", scope=_W,
             summary="상품 아이콘 등록 (최대 5)", resource_key="icon", takes_body=True),
    Endpoint(name="cafe24_product_icon_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/icons", scope=_W,
             summary="상품 아이콘 수정 (표시기간 등)", resource_key="icon", takes_body=True),
    Endpoint(name="cafe24_product_icon_remove", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/icons/{{code}}", scope=_W,
             summary="상품 아이콘 등록해제", resource_key="icon"),

    # === Decoration images ===
    Endpoint(name="cafe24_product_decorationimage_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/decorationimages", scope=_R,
             summary="상품 꾸미기 이미지 조회", resource_key="decorationimage", list_endpoint=True),
    Endpoint(name="cafe24_product_decorationimage_set", category=_C, method="POST", path=f"{_P}/{{product_no}}/decorationimages", scope=_W,
             summary="상품 꾸미기 이미지 설정", resource_key="decorationimage", takes_body=True),
    Endpoint(name="cafe24_product_decorationimage_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/decorationimages", scope=_W,
             summary="상품 꾸미기 이미지 수정", resource_key="decorationimage", takes_body=True),
    Endpoint(name="cafe24_product_decorationimage_remove", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/decorationimages/{{code}}", scope=_W,
             summary="상품 꾸미기 이미지 삭제", resource_key="decorationimage"),

    # === Misc read ===
    Endpoint(name="cafe24_product_discountprice_get", category=_C, method="GET", path=f"{_P}/{{product_no}}/discountprice", scope=_R,
             summary="상품 할인판매가 조회 (PC/모바일/앱)", resource_key="discountprice"),
    Endpoint(name="cafe24_product_hits_count", category=_C, method="GET", path=f"{_P}/{{product_no}}/hits/count", scope=_R,
             summary="상품 조회수 조회", resource_key="count"),

    # === Approve (공급사 상품 승인) ===
    Endpoint(name="cafe24_product_approve_get", category=_C, method="GET", path=f"{_P}/{{product_no}}/approve", scope=_R,
             summary="상품 승인 상태 조회", resource_key="approve"),
    Endpoint(name="cafe24_product_approve_request", category=_C, method="POST", path=f"{_P}/{{product_no}}/approve", scope=_W,
             summary="상품 승인 요청", resource_key="approve", takes_body=True),
    Endpoint(name="cafe24_product_approve_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/approve", scope=_W,
             summary="상품 승인 상태 변경 (승인완료/거절/검수중)", resource_key="approve", takes_body=True),

    # === Custom properties (per-product) ===
    Endpoint(name="cafe24_product_customproperty_list", category=_C, method="GET", path=f"{_P}/{{product_no}}/customproperties", scope=_R,
             summary="상품별 사용자정의 속성 조회", resource_key="custom_property", list_endpoint=True),
    Endpoint(name="cafe24_product_customproperty_update", category=_C, method="PUT", path=f"{_P}/{{product_no}}/customproperties/{{property_no}}", scope=_W,
             summary="상품별 사용자정의 속성 수정", resource_key="custom_property", takes_body=True),
    Endpoint(name="cafe24_product_customproperty_delete", category=_C, method="DELETE", path=f"{_P}/{{product_no}}/customproperties/{{property_no}}", scope=_W,
             summary="상품별 사용자정의 속성 삭제", resource_key="custom_property"),

    # === Custom properties (global) ===
    Endpoint(name="cafe24_product_customproperty_global_list", category=_C, method="GET", path=f"{_P}/customproperties", scope=_R,
             summary="사용자정의 속성 전체 조회", resource_key="custom_property", list_endpoint=True),
    Endpoint(name="cafe24_product_customproperty_global_create", category=_C, method="POST", path=f"{_P}/customproperties", scope=_W,
             summary="사용자정의 속성 생성", resource_key="custom_property", takes_body=True),
    Endpoint(name="cafe24_product_customproperty_global_update", category=_C, method="PUT", path=f"{_P}/customproperties/{{property_no}}", scope=_W,
             summary="사용자정의 속성 수정", resource_key="custom_property", takes_body=True),
    Endpoint(name="cafe24_product_customproperty_global_delete", category=_C, method="DELETE", path=f"{_P}/customproperties/{{property_no}}", scope=_W,
             summary="사용자정의 속성 삭제", resource_key="custom_property"),

    # === Global icon/decoration lists + image upload ===
    Endpoint(name="cafe24_product_decorationimage_global_list", category=_C, method="GET", path=f"{_P}/decorationimages", scope=_R,
             summary="전체 꾸미기 이미지 목록 조회", resource_key="decorationimage", list_endpoint=True),
    Endpoint(name="cafe24_product_icon_global_list", category=_C, method="GET", path=f"{_P}/icons", scope=_R,
             summary="전체 상품 아이콘 목록 조회", resource_key="icon", list_endpoint=True),
    Endpoint(name="cafe24_product_image_global_upload", category=_C, method="POST", path=f"{_P}/images", scope=_W,
             summary="상세이미지 업로드 (상품등록 전 선행, Base64)", resource_key="image", takes_body=True, body_key="images"),

    # === Properties (상품 상세/목록 항목 필드 설정) ===
    Endpoint(name="cafe24_product_property_list", category=_C, method="GET", path=f"{_P}/properties", scope=_R,
             summary="상품 상세 화면 항목(필드) 조회", resource_key="property", list_endpoint=True),
    Endpoint(name="cafe24_product_property_create", category=_C, method="POST", path=f"{_P}/properties", scope=_W,
             summary="상품 상세 화면 항목 생성", resource_key="property", takes_body=True),
    Endpoint(name="cafe24_product_property_update", category=_C, method="PUT", path=f"{_P}/properties", scope=_W,
             summary="상품 상세 화면 항목 수정", resource_key="property", takes_body=True),

    # === Bundle products (세트상품) ===
    Endpoint(name="cafe24_bundleproduct_list", category=_C, method="GET", path="/api/v2/admin/bundleproducts", scope=_R,
             summary="세트상품 목록 조회", resource_key="product", list_endpoint=True, query_params=_PRODUCT_FILTERS),
    Endpoint(name="cafe24_bundleproduct_get", category=_C, method="GET", path="/api/v2/admin/bundleproducts/{product_no}", scope=_R,
             summary="세트상품 상세 조회", resource_key="product"),
    Endpoint(name="cafe24_bundleproduct_create", category=_C, method="POST", path="/api/v2/admin/bundleproducts", scope=_W,
             summary="세트상품 생성 (구성상품 + 세트할인 필수)", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_bundleproduct_update", category=_C, method="PUT", path="/api/v2/admin/bundleproducts/{product_no}", scope=_W,
             summary="세트상품 수정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_bundleproduct_delete", category=_C, method="DELETE", path="/api/v2/admin/bundleproducts/{product_no}", scope=_W,
             summary="세트상품 삭제", resource_key="product"),

    # === Categories ↔ Products (relation, scope read/write_product) ===
    Endpoint(name="cafe24_category_product_list", category=_C, method="GET",
             path="/api/v2/admin/categories/{category_no}/products", scope=_R,
             summary="분류 내 상품 목록 조회", resource_key="product", list_endpoint=True,
             query_params=(Param("display_group", type="int", required=True, description="상세 상품분류: 1 일반/2 추천/3 신상 (필수)"),
                           Param("limit", type="int", description="최대건수 (최대 50000)"))),
    Endpoint(name="cafe24_category_product_count", category=_C, method="GET",
             path="/api/v2/admin/categories/{category_no}/products/count", scope=_R,
             summary="분류 내 상품 수 조회", resource_key="count",
             query_params=(Param("display_group", type="int", required=True, description="1/2/3"),)),
    Endpoint(name="cafe24_category_product_add", category=_C, method="POST",
             path="/api/v2/admin/categories/{category_no}/products", scope=_W,
             summary="분류에 상품 배정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_category_product_update", category=_C, method="PUT",
             path="/api/v2/admin/categories/{category_no}/products", scope=_W,
             summary="분류 내 상품 정렬/고정 수정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_category_product_remove", category=_C, method="DELETE",
             path="/api/v2/admin/categories/{category_no}/products/{product_no}", scope=_W,
             summary="분류에서 상품 제거 (상품 자체는 유지)", resource_key="product",
             query_params=(Param("display_group", type="int", description="1/2/3 (기본 1)"),)),

    # === Categories properties (목록 항목 필드, scope read/write_product) ===
    Endpoint(name="cafe24_category_property_list", category=_C, method="GET",
             path="/api/v2/admin/categories/properties", scope=_R,
             summary="상품 목록 화면 항목 조회", resource_key="property", list_endpoint=True),
    Endpoint(name="cafe24_category_property_create", category=_C, method="POST",
             path="/api/v2/admin/categories/properties", scope=_W,
             summary="상품 목록 화면 항목 생성", resource_key="property", takes_body=True),
    Endpoint(name="cafe24_category_property_update", category=_C, method="PUT",
             path="/api/v2/admin/categories/properties", scope=_W,
             summary="상품 목록 화면 항목 수정", resource_key="property", takes_body=True),

    # === Mains ↔ Products (relation, scope read/write_product) ===
    Endpoint(name="cafe24_main_product_list", category=_C, method="GET",
             path="/api/v2/admin/mains/{display_group}/products", scope=_R,
             summary="메인분류 내 상품 목록 조회", resource_key="product", list_endpoint=True),
    Endpoint(name="cafe24_main_product_count", category=_C, method="GET",
             path="/api/v2/admin/mains/{display_group}/products/count", scope=_R,
             summary="메인분류 내 상품 수 조회", resource_key="count"),
    Endpoint(name="cafe24_main_product_set", category=_C, method="POST",
             path="/api/v2/admin/mains/{display_group}/products", scope=_W,
             summary="메인분류에 상품 배정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_main_product_update", category=_C, method="PUT",
             path="/api/v2/admin/mains/{display_group}/products", scope=_W,
             summary="메인분류 내 상품 고정정렬 수정", resource_key="product", takes_body=True),
    Endpoint(name="cafe24_main_product_remove", category=_C, method="DELETE",
             path="/api/v2/admin/mains/{display_group}/products/{product_no}", scope=_W,
             summary="메인분류에서 상품 제거", resource_key="product"),

    # === Mains properties (메인 화면 항목 필드) ===
    Endpoint(name="cafe24_main_property_list", category=_C, method="GET",
             path="/api/v2/admin/mains/properties", scope=_R,
             summary="메인 화면 항목 조회", resource_key="property", list_endpoint=True),
    Endpoint(name="cafe24_main_property_create", category=_C, method="POST",
             path="/api/v2/admin/mains/properties", scope=_W,
             summary="메인 화면 항목 생성", resource_key="property", takes_body=True),
    Endpoint(name="cafe24_main_property_update", category=_C, method="PUT",
             path="/api/v2/admin/mains/properties", scope=_W,
             summary="메인 화면 항목 수정", resource_key="property", takes_body=True),
)
