"""Generated tools — Product (상품). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_all_shop_products_by_filter': ('GET', '/products', [], ['page', 'limit', 'categoryCode', 'prodName', 'prodStatus', 'prodType', 'usePreSale', 'productAddTimeType', 'productAddTime', 'productEditTimeType', 'productEditTime', 'unitCode'], False),
    'create_product': ('POST', '/products', [], [], True),
    'read_all_shop_categories_by_site_code_and_unit_code': ('GET', '/products/shop-categories', [], ['unitCode'], False),
    'read_all_shop_showcases_by_site_code': ('GET', '/products/shop-showcases', [], [], False),
    'read_all_shop_naver_categories': ('GET', '/products/shop-naver-categories', [], ['page', 'limit', 'naverCategoryName'], False),
    'update_multiple_product_status': ('PATCH', '/products/status', [], [], True),
    'read_all_shop_product_options_by_prod_no': ('GET', '/products/{prodNo}/options', ['prodNo'], ['page', 'limit', 'unitCode'], False),
    'read_shop_product_options_by_prod_no': ('GET', '/products/{prodNo}/options/{optionCode}', ['prodNo', 'optionCode'], ['unitCode'], False),
    'update_product_options': ('PATCH', '/products/{prodNo}/options/{optionCode}', ['prodNo', 'optionCode'], [], True),
    'read_shop_product_options_by_prod_nos': ('GET', '/products/options', [], ['unitCode', 'prodNos'], False),
    'read_one_shop_products_by_prod_no': ('GET', '/products/{prodNo}', ['prodNo'], ['unitCode'], False),
    'update_product_info_by_prod_no': ('PATCH', '/products/{prodNo}', ['prodNo'], [], True),
    'read_all_shop_product_option_details_by_prod_no': ('GET', '/products/{prodNo}/option-details', ['prodNo'], ['page', 'limit', 'unitCode'], False),
    'read_shop_product_option_details_by_prod_no': ('GET', '/products/{prodNo}/option-details/{optionDetailCode}', ['prodNo', 'optionDetailCode'], ['unitCode'], False),
    'update_product_option_details': ('PATCH', '/products/{prodNo}/option-details/{optionDetailCode}', ['prodNo', 'optionDetailCode'], [], True),
    'read_shipping_service_settings': ('GET', '/products/{prodNo}/shipping-service-settings', ['prodNo'], ['unitCode'], False),
    'update_product_relative_info': ('PATCH', '/products/{prodNo}/relative-info', ['prodNo'], [], True),
    'update_product_seo_info': ('PATCH', '/products/{prodNo}/seo', ['prodNo'], [], True),
    'read_all_shop_product_shipping_settings_by_prod_no': ('GET', '/products/{prodNo}/shipping-settings', ['prodNo'], ['unitCode'], False),
    'update_product_shipping_settings_by_prod_no': ('PATCH', '/products/{prodNo}/shipping-settings', ['prodNo'], [], True),
    'update_product_stock_info_by_prod_no': ('PATCH', '/products/{prodNo}/stock-info', ['prodNo'], [], True),
    'update_product_price_by_prod_no': ('PATCH', '/products/{prodNo}/price', ['prodNo'], [], True),
    'update_product_discount_info_by_prod_no': ('PATCH', '/products/{prodNo}/discount-info', ['prodNo'], [], True),
    'update_product_display_info_by_prod_no': ('PATCH', '/products/{prodNo}/display', ['prodNo'], [], True),
    'update_product_classification': ('PATCH', '/products/{prodNo}/classification', ['prodNo'], [], True),
    'update_product_status': ('PATCH', '/products/{prodNo}/status', ['prodNo'], [], True),
    'update_product_external_integration_info': ('PATCH', '/products/{prodNo}/external-integration-info', ['prodNo'], [], True),
    'update_product_additional_info': ('PATCH', '/products/{prodNo}/additional-info', ['prodNo'], [], True),
    'update_product_etc_info': ('PATCH', '/products/{prodNo}/etc-info', ['prodNo'], [], True),
    'update_product_exhibitions': ('PATCH', '/products/{prodNo}/exhibitions', ['prodNo'], [], True),
    'create_product_images': ('POST', '/products/{prodNo}/images', ['prodNo'], [], True),
}


class CreateProductBody(BaseModel):
    """요청 본문 (action='create_product' [POST /products]). 필수 필드: productImages, productBaseInfo, productClassificationInfo, productPriceInfo, productDiscountInfo."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    productImages: list[str] = Field(..., description='상품 이미지<br> 상품 등록 시 이미지는 최대 10개까지 등록할 수 있고, 더 추가하려면 상품 수정 API를 이용하시면 됩니다.')
    digitalImage: str | None = Field(None, description='디지털 상품 등록 시 업로드할 파일<br> 디지털 상품 파일은 최대 1개까지 업로드 할 수 있습니다.')
    externalIntegrationImage: str | None = Field(None, description='외부 연동 이미지<br> 외부 연동 이미지는 최대 1개까지 업로드 할 수 있습니다.')
    productBaseInfo: dict = Field(..., description='상품 기본 정보 데이터')
    productClassificationInfo: dict = Field(..., description='상품 분류 데이터')
    productPriceInfo: list[dict] = Field(..., description='상품 가격 데이터')
    productDiscountInfo: list[dict] = Field(..., description='상품 할인 설정 데이터')
    productShippingSettingInfo: list[dict] | None = Field(None, description='상품 배송 설정 데이터')
    productEtcInfo: dict | None = Field(None, description='상품 기타 정보 데이터')
    productExhibitionInfo: list[dict] | None = Field(None, description='상품 전시 설정 데이터')
    productSeoInfo: list[dict] | None = Field(None, description='상품 SEO 설정 데이터')
    productOptionInfo: dict | None = Field(None, description='상품 옵션 데이터')
    productExternalIntegrationInfo: dict | None = Field(None, description='상품 외부 연동 정보 데이터')


class UpdateMultipleProductStatusBody(BaseModel):
    """요청 본문 (action='update_multiple_product_status' [PATCH /products/status]). 필수 필드: status, prodNos."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: str = Field(..., description='상품 상태 코드')
    prodNos: list[float] = Field(..., description='수정할 상품 번호 리스트')


class UpdateProductOptionsBody(BaseModel):
    """요청 본문 (action='update_product_options' [PATCH /products/{prodNo}/options/{optionCode}]). 필수 필드: unitCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    name: str | None = Field(None, description='옵션 명')
    optionValueList: list[dict] | None = Field(None, description='수정할 옵션 값 정보')


class UpdateProductInfoByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_info_by_prod_no' [PATCH /products/{prodNo}]). 필수 필드: unitCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    digitalProductFile: str | None = Field(None, description='디지털 상품 이미지')
    unitCode: str = Field(..., description='unitCode')
    productName: str | None = Field(None, description='상품명')
    summaryDescription: str | None = Field(None, description='상품 요약 설명')
    description: str | None = Field(None, description='상품 상세 설명')
    images: list[str] | None = Field(None, description='상품 이미지 URL 목록')
    useMobileDescription: str | None = Field(None, description='모바일 상세 설명 사용 여부')
    mobileDescription: str | None = Field(None, description='모바일 상세 설명')
    commonHeaderSettingType: str | None = Field(None, description='상품 상세 상단 공통 설정 타입')
    commonHeaderCode: str | None = Field(None, description='상품 상세 상단 공통 설정 코드(상품 상세 상단 공통 설정 타입이 custom일 경우 필수)')
    commonFooterSettingType: str | None = Field(None, description='상품 상세 하단 공통 설정 타입')
    commonFooterCode: str | None = Field(None, description='상품 상세 하단 공통 설정 코드(상품 상세 하단 공통 설정 타입이 custom일 경우 필수)')
    customProductCode: str | None = Field(None, description='자체 상품 코드')
    productType: str | None = Field(None, description='판매 방식 설정')
    digitalData: dict | None = Field(None, description='디지털 상품 데이터')
    subscribeData: dict | None = Field(None, description='회원그룹 이용권 데이터')
    useSalesPeriod: str | None = Field(None, description='판매기간 사용 여부')
    salesStartDate: str | None = Field(None, description='판매 기간 시작일')
    salesEndDate: str | None = Field(None, description='판매 기간 종료일')
    productInfoNoticeType: str | None = Field(None, description='상품정보제공고시 타입')
    productInfoNotice: str | None = Field(None, description='상품정보제공고시')


class UpdateProductOptionDetailsBody(BaseModel):
    """요청 본문 (action='update_product_option_details' [PATCH /products/{prodNo}/option-details/{optionDetailCode}]). 필수 필드: unitCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    price: float | None = Field(None, description='옵션 가격')
    supplyPrice: float | None = Field(None, description='옵션 공급가 (원가)')
    stock: float | None = Field(None, description='변경할 재고 수량(+ or -)')
    stockSku: str | None = Field(None, description='재고관리 코드(SKU)')
    status: str | None = Field(None, description='옵션 상세 상태')


class UpdateProductRelativeInfoBody(BaseModel):
    """요청 본문 (action='update_product_relative_info' [PATCH /products/{prodNo}/relative-info]). 필수 필드: relativeData."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    relativeData: list[dict] = Field(..., description='수정할 연관 상품 정보 리스트')


class UpdateProductSeoInfoBody(BaseModel):
    """요청 본문 (action='update_product_seo_info' [PATCH /products/{prodNo}/seo]). 필수 필드: unitCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    seoAccessBot: str | None = Field(None, description='상품 검색엔진 노출 여부')
    seoTitle: str | None = Field(None, description='SEO(검색엔진 최적화) 제목')
    seoDescription: str | None = Field(None, description='SEO(검색엔진 최적화) 설명')


class UpdateProductShippingSettingsByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_shipping_settings_by_prod_no' [PATCH /products/{prodNo}/shipping-settings]). 필수 필드: unitCode, useShippingNoticeTemplate."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    weight: float | None = Field(None, description='상품 무게')
    useDefaultShippingTemplate: str | None = Field(None, description='기본 배송 템플릿 사용 여부')
    shippingTemplateCode: str | None = Field(None, description='선택할 배송 템플릿 코드')
    useShippingNoticeTemplate: str = Field(..., description='배송 관련 안내 템플릿 사용 여부')
    notice: str | None = Field(None, description='배송 관련 안내')
    shippingSettingDataList: list[dict] | None = Field(None, description='국가별 상품 배송 설정')


class UpdateProductStockInfoByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_stock_info_by_prod_no' [PATCH /products/{prodNo}/stock-info])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    stock: float | None = Field(None, description='변경할 재고 수량(+ or -)')
    customSkuCode: str | None = Field(None, description='판매자 임의설정 재고 관리 번호(코드)')
    isUseStock: str | None = Field(None, description='재고 관리 기능 사용 여부')
    isUnlimitedStock: str | None = Field(None, description='재고 소진 후에도 주문 가능 여부')


class UpdateProductPriceByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_price_by_prod_no' [PATCH /products/{prodNo}/price]). 필수 필드: unitCode."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    supplyPrice: float | None = Field(None, description='상품 공급가 (원가)')
    isPriceTaxIncluded: str | None = Field(None, description='부가세 포함 여부')
    isPriceNone: str | None = Field(None, description='가격 없음 여부')
    price: float | None = Field(None, description='판매가')
    originalPrice: float | None = Field(None, description='정가')


class UpdateProductDiscountInfoByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_discount_info_by_prod_no' [PATCH /products/{prodNo}/discount-info]). 필수 필드: unitCode, coupon, point, shoppingGroup, period."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    coupon: str = Field(..., description='쿠폰 할인 설정 여부')
    point: str = Field(..., description='포인트 할인 설정 여부')
    shoppingGroup: str = Field(..., description='쇼핑등급 할인 설정 여부')
    givePointType: str | None = Field(None, description='적립금 지급 기준 타입')
    pointCriteria: dict | None = Field(None, description='적립금 지급 기준 설정')
    period: str = Field(..., description='즉시/기간 할인 설정 여부')
    periodData: dict | None = Field(None, description='기간 할인 설정 데이터')


class UpdateProductDisplayInfoByProdNoBody(BaseModel):
    """요청 본문 (action='update_product_display_info_by_prod_no' [PATCH /products/{prodNo}/display]). 필수 필드: unitCode, display."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    display: list[str] = Field(..., description='노출 설정')


class UpdateProductClassificationBody(BaseModel):
    """요청 본문 (action='update_product_classification' [PATCH /products/{prodNo}/classification])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    badge: dict | None = Field(None, description='상품 뱃지 설정')
    categories: list[str] | None = Field(None, description='상품 카테고리')
    showcases: list[str] | None = Field(None, description='상품 기획전')
    origin: str | None = Field(None, description='원산지')
    maker: str | None = Field(None, description='제조사')
    brand: str | None = Field(None, description='브랜드')


class UpdateProductStatusBody(BaseModel):
    """요청 본문 (action='update_product_status' [PATCH /products/{prodNo}/status]). 필수 필드: status."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    status: str = Field(..., description='상품 상태 코드')


class UpdateProductExternalIntegrationInfoBody(BaseModel):
    """요청 본문 (action='update_product_external_integration_info' [PATCH /products/{prodNo}/external-integration-info])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    externalImage: str | None = Field(None, description='외부연동 이미지')
    productName: str | None = Field(None, description='외부 노출용 상품 명')
    eventDescription: str | None = Field(None, description='외부 노출용 이벤트 문구')
    naverCategoryCode: str | None = Field(None, description='네이버 연동 용 카테고리 코드')
    status: str | None = Field(None, description='외부 연동용 상품 상태')
    saleMethod: str | None = Field(None, description='외부 연동용 상품 판매 방식')
    parallelImport: str | None = Field(None, description='병행 수입 여부')
    orderMade: str | None = Field(None, description='주문제작 상품 여부')
    purchasingAgent: str | None = Field(None, description='구매 대행 여부')
    cultureBenefit: str | None = Field(None, description='도서공연비 소득공제 여부')


class UpdateProductAdditionalInfoBody(BaseModel):
    """요청 본문 (action='update_product_additional_info' [PATCH /products/{prodNo}/additional-info]). 필수 필드: unitCode, prodNos."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛 코드')
    prodNos: list[float] = Field(..., description='수정할 추가 상품 번호 리스트')


class UpdateProductEtcInfoBody(BaseModel):
    """요청 본문 (action='update_product_etc_info' [PATCH /products/{prodNo}/etc-info])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    minimumPurchaseQuantity: float | None = Field(None, description='최소 구매수량')
    maximumPurchaseQuantity: float | None = Field(None, description='1회 구매 시 최대 수량')
    maximumPurchaseQuantityType: str | None = Field(None, description='1회 구매 수량 제한 타입 (주문 단위, 품목 단위)')
    memberMaximumPurchaseQuantity: float | None = Field(None, description='1인 구매 시 최대 수량')
    optionalLimitType: str | None = Field(None, description='0원 선택옵션 구매 시 최대 구매 제한 타입 (본 상품 구매 수량만큼 구매 가능, 최대 구매 수량 제한, 1개만 구매 가능)')
    optionalLimit: float | None = Field(None, description='0원 선택옵션 구매 시 최대 구매 수량 (optionalLimitType 이 limit인 경우에만 입력)')
    useUnipassNumber: str | None = Field(None, description='개인통관고유부호 설정 (기본 방법을 따름, 사용함, 사용 안함)')
    adultPurchase: str | None = Field(None, description='미성년자 구매 불가능 여부 (구매불가, 구매가능)')


class UpdateProductExhibitionsBody(BaseModel):
    """요청 본문 (action='update_product_exhibitions' [PATCH /products/{prodNo}/exhibitions]). 필수 필드: unitCode, isDisplay."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    unitCode: str = Field(..., description='유닛코드')
    isDisplay: str = Field(..., description='진열 여부')


class CreateProductImagesBody(BaseModel):
    """요청 본문 (action='create_product_images' [POST /products/{prodNo}/images])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    images: list[str] | None = Field(None, description='업로드할 이미지 파일 목록')

Body = Union[CreateProductBody, UpdateMultipleProductStatusBody, UpdateProductOptionsBody, UpdateProductInfoByProdNoBody, UpdateProductOptionDetailsBody, UpdateProductRelativeInfoBody, UpdateProductSeoInfoBody, UpdateProductShippingSettingsByProdNoBody, UpdateProductStockInfoByProdNoBody, UpdateProductPriceByProdNoBody, UpdateProductDiscountInfoByProdNoBody, UpdateProductDisplayInfoByProdNoBody, UpdateProductClassificationBody, UpdateProductStatusBody, UpdateProductExternalIntegrationInfoBody, UpdateProductAdditionalInfoBody, UpdateProductEtcInfoBody, UpdateProductExhibitionsBody, CreateProductImagesBody]

@mcp.tool()
def imweb_product(action: Literal["read_all_shop_products_by_filter", "create_product", "read_all_shop_categories_by_site_code_and_unit_code", "read_all_shop_showcases_by_site_code", "read_all_shop_naver_categories", "update_multiple_product_status", "read_all_shop_product_options_by_prod_no", "read_shop_product_options_by_prod_no", "update_product_options", "read_shop_product_options_by_prod_nos", "read_one_shop_products_by_prod_no", "update_product_info_by_prod_no", "read_all_shop_product_option_details_by_prod_no", "read_shop_product_option_details_by_prod_no", "update_product_option_details", "read_shipping_service_settings", "update_product_relative_info", "update_product_seo_info", "read_all_shop_product_shipping_settings_by_prod_no", "update_product_shipping_settings_by_prod_no", "update_product_stock_info_by_prod_no", "update_product_price_by_prod_no", "update_product_discount_info_by_prod_no", "update_product_display_info_by_prod_no", "update_product_classification", "update_product_status", "update_product_external_integration_info", "update_product_additional_info", "update_product_etc_info", "update_product_exhibitions", "create_product_images"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""상품 도구 — 31개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 31개 전체 공개).
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

