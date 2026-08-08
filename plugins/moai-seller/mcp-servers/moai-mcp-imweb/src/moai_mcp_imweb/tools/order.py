"""Generated tools — Order (주문). DO NOT EDIT; regenerate via tools/_generator.py."""
from __future__ import annotations

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from .._app import mcp
from .._base import get_client

# action -> (method, path, path_params, query_params, has_body)
_OPS: dict[str, tuple] = {
    'read_all_parcel_company_list': ('GET', '/orders/parcel-company-list', [], [], False),
    'read_all_shipping_place_list': ('GET', '/orders/shipping-places', [], ['unitCode', 'shippingPlaceCode', 'shippingPlaceName'], False),
    'read_all_order': ('GET', '/orders', [], ['isDeliveryHold', 'orderSectionStatus', 'deliveryType', 'deliveryPayType', 'startDeliverySendTime', 'endDeliverySendTime', 'startDeliveryCompleteTime', 'endDeliveryCompleteTime', 'startCancelRequestTime', 'endCancelRequestTime', 'page', 'limit', 'unitCode', 'saleChannel', 'isMember', 'memberUid', 'memberCode', 'orderType', 'ordererName', 'ordererCall', 'isFirst', 'isCancelReq', 'isRequestPayment', 'startWtime', 'endWtime', 'isGift', 'shippingPlaceCode', 'paymentMethod', 'paymentStatus', 'includeOrderPending'], False),
    'read_one_order_by_order_no': ('GET', '/orders/{orderNo}', ['orderNo'], [], False),
    'read_all_order_section': ('GET', '/orders/{orderNo}/order-sections', ['orderNo'], ['isDeliveryHold', 'orderSectionStatus', 'deliveryType', 'deliveryPayType', 'startDeliverySendTime', 'endDeliverySendTime', 'startDeliveryCompleteTime', 'endDeliveryCompleteTime', 'startCancelRequestTime', 'endCancelRequestTime'], False),
    'read_one_order_section': ('GET', '/orders/{orderNo}/order-section/{orderSectionCode}', ['orderNo', 'orderSectionCode'], [], False),
    'read_all_order_section_item': ('GET', '/orders/{orderNo}/order-section/{orderSectionCode}/order-section-items', ['orderNo', 'orderSectionCode'], [], False),
    'read_one_order_section_item': ('GET', '/orders/{orderNo}/order-section/{orderSectionCode}/order-section-item/{orderSectionItemNo}', ['orderNo', 'orderSectionCode', 'orderSectionItemNo'], [], False),
    'read_order_coupons': ('GET', '/orders/{orderNo}/coupons', ['orderNo'], [], False),
    'update_order_shipping_operation': ('PATCH', '/orders/{orderNo}/shipping-operation', ['orderNo'], [], True),
    'update_order_section_shipping_operation': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/shipping-operation', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_shipping_operation': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/shipping-operation', ['orderNo', 'orderSectionItemNo'], [], True),
    'create_order_invoice': ('POST', '/orders/{orderNo}/invoice', ['orderNo'], [], True),
    'update_order_invoice': ('PATCH', '/orders/{orderNo}/invoice', ['orderNo'], [], True),
    'remove_order_invoice': ('DELETE', '/orders/{orderNo}/invoice', ['orderNo'], [], True),
    'create_order_section_invoice': ('POST', '/orders/{orderNo}/order-section/{orderSectionCode}/invoice', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_invoice': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/invoice', ['orderNo', 'orderSectionCode'], [], True),
    'remove_order_section_invoice': ('DELETE', '/orders/{orderNo}/order-section/{orderSectionCode}/invoice', ['orderNo', 'orderSectionCode'], [], False),
    'create_order_section_item_invoice': ('POST', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/invoice', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_cancel_request': ('PATCH', '/orders/{orderNo}/cancel-request', ['orderNo'], [], True),
    'update_order_section_cancel_request': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/cancel-request', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_cancel_request': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-request', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_cancel_reject': ('PATCH', '/orders/{orderNo}/cancel-reject', ['orderNo'], [], True),
    'update_order_section_cancel_reject': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/cancel-reject', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_cancel_reject': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-reject', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_return_request': ('PATCH', '/orders/{orderNo}/return-request', ['orderNo'], [], True),
    'update_order_section_return_request': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/return-request', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_return_request': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-request', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_section_retrieve_complete': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/retrieve-complete', ['orderNo', 'orderSectionCode'], [], False),
    'update_order_return_reject': ('PATCH', '/orders/{orderNo}/return-reject', ['orderNo'], [], True),
    'update_order_section_return_reject': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/return-reject', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_return_reject': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-reject', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_exchange_request': ('PATCH', '/orders/{orderNo}/exchange-request', ['orderNo'], [], True),
    'update_order_section_exchange_request': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/exchange-request', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_exchange_request': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/exchange-request', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_exchange_reject': ('PATCH', '/orders/{orderNo}/exchange-reject', ['orderNo'], [], True),
    'update_order_section_exchange_reject': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/exchange-reject', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_exchange_reject': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/exchange-reject', ['orderNo', 'orderSectionItemNo'], [], False),
    'update_order_section_cancel_approve': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/cancel-approve', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_cancel_approve': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-approve', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_section_return_approve': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/return-approve', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_return_approve': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-approve', ['orderNo', 'orderSectionItemNo'], [], True),
    'update_order_section_exchange_approve': ('PATCH', '/orders/{orderNo}/order-section/{orderSectionCode}/exchange-approve', ['orderNo', 'orderSectionCode'], [], True),
    'update_order_section_item_exchange_approve': ('PATCH', '/orders/{orderNo}/order-section-items/{orderSectionItemNo}/exchange-approve', ['orderNo', 'orderSectionItemNo'], [], True),
}


class UpdateOrderShippingOperationBody(BaseModel):
    """요청 본문 (action='update_order_shipping_operation' [PATCH /orders/{orderNo}/shipping-operation]). 필수 필드: orderSectionStatus."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionStatus: str = Field(..., description='배송처리할 상태')
    orderSectionCodeList: list[str] | None = Field(None, description='배송 처리할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')
    invoiceNo: str | None = Field(None, description='송장번호')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx')


class UpdateOrderSectionShippingOperationBody(BaseModel):
    """요청 본문 (action='update_order_section_shipping_operation' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/shipping-operation]). 필수 필드: orderSectionStatus."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionStatus: str = Field(..., description='배송처리할 상태')
    orderSectionItemDataList: list[dict] | None = Field(None, description='배송 처리할 주문 섹션아이템 번호 및 수량')
    invoiceNo: str | None = Field(None, description='송장번호')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx')


class UpdateOrderSectionItemShippingOperationBody(BaseModel):
    """요청 본문 (action='update_order_section_item_shipping_operation' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/shipping-operation]). 필수 필드: orderSectionStatus."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionStatus: str = Field(..., description='배송처리할 상태')
    qty: float | None = Field(None, description='변경하려는 수량 (배송대기 변경 요청일 경우에만 입력 가능)')
    invoiceNo: str | None = Field(None, description='송장번호')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx')


class CreateOrderInvoiceBody(BaseModel):
    """요청 본문 (action='create_order_invoice' [POST /orders/{orderNo}/invoice])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allInvoiceNo: str | None = Field(None, description='하위 모든 섹션에 처리할 송장번호')
    allParcelCompanyIdx: float | None = Field(None, description='하위 모든 섹션에 처리할 택배사 고유 idx')
    orderSectionInvoiceDataList: list[dict] | None = Field(None, description='송장 처리할 섹션 정보 리스트 (없다면 하위 섹션 모두 allInvoiceNo, allParcelCompanyIdx 으로 처리)')


class UpdateOrderInvoiceBody(BaseModel):
    """요청 본문 (action='update_order_invoice' [PATCH /orders/{orderNo}/invoice])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allInvoiceNo: str | None = Field(None, description='하위 모든 섹션에 처리할 송장번호')
    allParcelCompanyIdx: float | None = Field(None, description='하위 모든 섹션에 처리할 택배사 고유 idx')
    orderSectionInvoiceDataList: list[dict] | None = Field(None, description='송장 처리할 섹션 정보 리스트 (없다면 하위 섹션 모두 allInvoiceNo, allParcelCompanyIdx 으로 처리)')


class RemoveOrderInvoiceBody(BaseModel):
    """요청 본문 (action='remove_order_invoice' [DELETE /orders/{orderNo}/invoice])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionCodeList: list[str] | None = Field(None, description='송장 삭제할 섹션 코드 목록')


class CreateOrderSectionInvoiceBody(BaseModel):
    """요청 본문 (action='create_order_section_invoice' [POST /orders/{orderNo}/order-section/{orderSectionCode}/invoice])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    allInvoiceNo: str | None = Field(None, description='하위 모든 섹션에 처리할 송장번호')
    allParcelCompanyIdx: float | None = Field(None, description='하위 모든 섹션에 처리할 택배사 고유 idx')
    orderSectionItemInvoiceDataList: list[dict] | None = Field(None, description='송장 처리할 섹션 아이템 정보 리스트 (없다면 allInvoiceNo, allParcelCompanyIdx 으로 처리)')


class UpdateOrderSectionInvoiceBody(BaseModel):
    """요청 본문 (action='update_order_section_invoice' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/invoice]). 필수 필드: invoiceNo, parcelCompanyIdx."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    invoiceNo: str = Field(..., description='송장번호')
    parcelCompanyIdx: float = Field(..., description='택배사 고유 idx')


class CreateOrderSectionItemInvoiceBody(BaseModel):
    """요청 본문 (action='create_order_section_item_invoice' [POST /orders/{orderNo}/order-section-items/{orderSectionItemNo}/invoice]). 필수 필드: invoiceNo, parcelCompanyIdx."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    invoiceNo: str = Field(..., description='송장번호')
    parcelCompanyIdx: float = Field(..., description='택배사 고유 idx')


class UpdateOrderCancelRequestBody(BaseModel):
    """요청 본문 (action='update_order_cancel_request' [PATCH /orders/{orderNo}/cancel-request]). 필수 필드: cancelReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    cancelReason: str = Field(..., description='취소 사유')
    cancelReasonDetail: str | None = Field(None, description='취소 사유 상세')
    orderSectionCodeList: list[str] | None = Field(None, description='취소 처리할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')


class UpdateOrderSectionCancelRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_cancel_request' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/cancel-request]). 필수 필드: cancelReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    cancelReason: str = Field(..., description='취소 사유')
    cancelReasonDetail: str | None = Field(None, description='취소 사유 상세')
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')


class UpdateOrderSectionItemCancelRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_item_cancel_request' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-request]). 필수 필드: cancelReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    cancelReason: str = Field(..., description='취소 사유')
    cancelReasonDetail: str | None = Field(None, description='취소 사유 상세')
    qty: float | None = Field(None, description='변경하려는 섹션아이템의 수량')


class UpdateOrderCancelRejectBody(BaseModel):
    """요청 본문 (action='update_order_cancel_reject' [PATCH /orders/{orderNo}/cancel-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionCodeList: list[str] | None = Field(None, description='취소 요청을 거절할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')
    invoiceNo: str | None = Field(None, description='외부채널 주문 시 필수 입력 - 송장번호')
    parcelCompanyIdx: float | None = Field(None, description='외부채널 주문 시 필수 입력 - 택배사 고유 idx')


class UpdateOrderSectionCancelRejectBody(BaseModel):
    """요청 본문 (action='update_order_section_cancel_reject' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/cancel-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')
    invoiceNo: str | None = Field(None, description='외부채널 주문 시 필수 입력 - 송장번호')
    parcelCompanyIdx: float | None = Field(None, description='외부채널 주문 시 필수 입력 - 택배사 고유 idx')


class UpdateOrderSectionItemCancelRejectBody(BaseModel):
    """요청 본문 (action='update_order_section_item_cancel_reject' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    invoiceNo: str | None = Field(None, description='외부채널 주문일 경우 취소 요청을 거절하며 배송을 동시에 진행해야 하는 정책에 따라,  해당 필드에 택배사를 함께 입력해야 합니다. 일반 주문의 경우에는 입력하지 않습니다.')
    parcelCompanyIdx: float | None = Field(None, description='외부채널 주문 시 필수 입력 - 택배사 고유 idx')


class UpdateOrderReturnRequestBody(BaseModel):
    """요청 본문 (action='update_order_return_request' [PATCH /orders/{orderNo}/return-request]). 필수 필드: retrieveType, returnReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    returnReason: str = Field(..., description='반품 사유<br>        외부채널 주문일 경우 다음 사유들 중 하나를 입력해주세요     - PRODUCT_UNSATISFIED: 서비스 및 상품 불만족 (네이버페이) - DELAYED_DELIVERY: 배송 지연 (네이버페이, 톡체크아웃) - SOLD_OUT: 상품 품절 (네이버…')
    returnReasonDetail: str | None = Field(None, description='반품 상세 사유')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    orderSectionCodeList: list[str] | None = Field(None, description='반품접수 처리할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')


class UpdateOrderSectionReturnRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_return_request' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/return-request]). 필수 필드: retrieveType, returnReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    returnReason: str = Field(..., description='반품 사유<br>        외부채널 주문일 경우 다음 사유들 중 하나를 입력해주세요     - PRODUCT_UNSATISFIED: 서비스 및 상품 불만족 (네이버페이) - DELAYED_DELIVERY: 배송 지연 (네이버페이, 톡체크아웃) - SOLD_OUT: 상품 품절 (네이버…')
    returnReasonDetail: str | None = Field(None, description='반품 상세 사유')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')


class UpdateOrderSectionItemReturnRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_item_return_request' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-request]). 필수 필드: retrieveType, returnReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    returnReason: str = Field(..., description='반품 사유<br>        외부채널 주문일 경우 다음 사유들 중 하나를 입력해주세요     - PRODUCT_UNSATISFIED: 서비스 및 상품 불만족 (네이버페이) - DELAYED_DELIVERY: 배송 지연 (네이버페이, 톡체크아웃) - SOLD_OUT: 상품 품절 (네이버…')
    returnReasonDetail: str | None = Field(None, description='반품 상세 사유')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    qty: float | None = Field(None, description='변경하려는 섹션아이템의 수량')


class UpdateOrderReturnRejectBody(BaseModel):
    """요청 본문 (action='update_order_return_reject' [PATCH /orders/{orderNo}/return-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionCodeList: list[str] | None = Field(None, description='반품 요청을 거절할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')
    externalRejectReason: str | None = Field(None, description='외부 채널 주문 - 거절 사유 <br> 외부 채널 주문은 거절 사유를 입력해야 합니다.')


class UpdateOrderSectionReturnRejectBody(BaseModel):
    """요청 본문 (action='update_order_section_return_reject' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/return-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')
    externalRejectReason: str | None = Field(None, description='외부 채널 주문 - 거절 사유 <br> 외부 채널 주문은 거절 사유를 입력해야 합니다.')


class UpdateOrderSectionItemReturnRejectBody(BaseModel):
    """요청 본문 (action='update_order_section_item_return_reject' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    externalRejectReason: str | None = Field(None, description='외부 채널 주문 - 거절 사유 <br> 외부 채널 주문은 거절 사유를 입력해야 합니다.')


class UpdateOrderExchangeRequestBody(BaseModel):
    """요청 본문 (action='update_order_exchange_request' [PATCH /orders/{orderNo}/exchange-request]). 필수 필드: retrieveType, exchangeReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    exchangeReason: str = Field(..., description='교환 사유')
    exchangeReasonDetail: str | None = Field(None, description='교환 상세 사유')
    orderSectionCodeList: list[str] | None = Field(None, description='교환접수 처리할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')
    exchangeOptionData: list[dict] | None = Field(None, description='옵션 변경이 필요한 섹션/섹션아이템별 교환 옵션 정보 (없다면 현재 옵션으로 교환)')


class UpdateOrderSectionExchangeRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_exchange_request' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/exchange-request]). 필수 필드: retrieveType, exchangeReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    exchangeReason: str = Field(..., description='교환 사유')
    exchangeReasonDetail: str | None = Field(None, description='교환 상세 사유')
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')


class UpdateOrderSectionItemExchangeRequestBody(BaseModel):
    """요청 본문 (action='update_order_section_item_exchange_request' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/exchange-request]). 필수 필드: retrieveType, exchangeReason."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    retrieveType: str = Field(..., description='수거타입')
    retrievePayType: str | None = Field(None, description='수거결제타입 (구매자 발송, 수동 수거신청일 경우 필수)')
    invoiceNo: str | None = Field(None, description='송장번호 (구매자 발송, 수동 수거신청일 경우 필수)')
    parcelCompanyIdx: float | None = Field(None, description='택배사 고유 idx (구매자 발송, 수동 수거신청일 경우 필수)')
    retrieveMemo: str | None = Field(None, description='수거 특이사항 메모 (수거 타입이 기타일 경우에만 입력 가능)')
    exchangeReason: str = Field(..., description='교환 사유')
    exchangeReasonDetail: str | None = Field(None, description='교환 상세 사유')
    optionDetailCodes: list[str] | None = Field(None, description='변경할 옵션 상세 코드 리스트')
    qty: float | None = Field(None, description='변경하려는 섹션아이템의 수량')


class UpdateOrderExchangeRejectBody(BaseModel):
    """요청 본문 (action='update_order_exchange_reject' [PATCH /orders/{orderNo}/exchange-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionCodeList: list[str] | None = Field(None, description='교환 요청을 거절할 주문 섹션 코드 리스트 (없다면 하위 섹션 모두 처리)')


class UpdateOrderSectionExchangeRejectBody(BaseModel):
    """요청 본문 (action='update_order_section_exchange_reject' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/exchange-reject])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    orderSectionItemDataList: list[dict] | None = Field(None, description='섹션아이템 목록')


class UpdateOrderSectionCancelApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_cancel_approve' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/cancel-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    returnedCoupons: list[str] | None = Field(None, description='반환할 쿠폰 코드 목록')
    excludeRefundAmount: float | None = Field(None, description='환불에서 제외할 금액')
    excludeRefundPoint: float | None = Field(None, description='환불에서 제외할 적립금 금액 (requestedRefundAmount와 동시 입력 불가)')
    requestedRefundAmount: float | None = Field(None, description='환불할 금액 (excludeRefundAmount와 동시 입력 불가, 최소 환불 금액은 0원 초과)')
    externalCancelReason: str | None = Field(None, description='외부채널 주문 용 취소 사유')
    externalCancelReasonDetail: str | None = Field(None, description='외부채널 주문 전용 취소 사유 상세')


class UpdateOrderSectionItemCancelApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_item_cancel_approve' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/cancel-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    returnedCoupons: list[str] | None = Field(None, description='반환할 쿠폰 코드 목록')
    excludeRefundAmount: float | None = Field(None, description='환불에서 제외할 금액')
    excludeRefundPoint: float | None = Field(None, description='환불에서 제외할 적립금 금액 (requestedRefundAmount와 동시 입력 불가)')
    requestedRefundAmount: float | None = Field(None, description='환불할 금액 (excludeRefundAmount와 동시 입력 불가, 최소 환불 금액은 0원 초과)')
    externalCancelReason: str | None = Field(None, description='외부채널 주문 전용 취소 사유')
    externalCancelReasonDetail: str | None = Field(None, description='외부채널 주문 전용 취소 사유 상세')


class UpdateOrderSectionReturnApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_return_approve' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/return-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    returnedCoupons: list[str] | None = Field(None, description='반환할 쿠폰 코드 목록')
    excludeRefundAmount: float | None = Field(None, description='환불에서 제외할 적립금 금액 (requestedRefundAmount와 동시 입력 불가)')
    excludeRefundPoint: float | None = Field(None, description='환불에서 제외할 적립금 금액')
    requestedRefundAmount: float | None = Field(None, description='환불할 금액 (excludeRefundAmount와 동시 입력 불가, 최소 환불 금액은 0원 초과)')


class UpdateOrderSectionItemReturnApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_item_return_approve' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/return-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    returnedCoupons: list[str] | None = Field(None, description='반환할 쿠폰 코드 목록')
    excludeRefundAmount: float | None = Field(None, description='환불에서 제외할 적립금 금액 (requestedRefundAmount와 동시 입력 불가)')
    excludeRefundPoint: float | None = Field(None, description='환불에서 제외할 적립금 금액')
    requestedRefundAmount: float | None = Field(None, description='환불할 금액 (excludeRefundAmount와 동시 입력 불가, 최소 환불 금액은 0원 초과)')


class UpdateOrderSectionExchangeApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_exchange_approve' [PATCH /orders/{orderNo}/order-section/{orderSectionCode}/exchange-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    requestedDeliveryAmount: float | None = Field(None, description='청구할 배송비 금액')
    excludeDeliveryAmount: float | None = Field(None, description='차감할 배송비 금액')


class UpdateOrderSectionItemExchangeApproveBody(BaseModel):
    """요청 본문 (action='update_order_section_item_exchange_approve' [PATCH /orders/{orderNo}/order-section-items/{orderSectionItemNo}/exchange-approve])."""
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    requestedDeliveryAmount: float | None = Field(None, description='청구할 배송비 금액')
    excludeDeliveryAmount: float | None = Field(None, description='차감할 배송비 금액')

Body = Union[UpdateOrderShippingOperationBody, UpdateOrderSectionShippingOperationBody, UpdateOrderSectionItemShippingOperationBody, CreateOrderInvoiceBody, UpdateOrderInvoiceBody, RemoveOrderInvoiceBody, CreateOrderSectionInvoiceBody, UpdateOrderSectionInvoiceBody, CreateOrderSectionItemInvoiceBody, UpdateOrderCancelRequestBody, UpdateOrderSectionCancelRequestBody, UpdateOrderSectionItemCancelRequestBody, UpdateOrderCancelRejectBody, UpdateOrderSectionCancelRejectBody, UpdateOrderSectionItemCancelRejectBody, UpdateOrderReturnRequestBody, UpdateOrderSectionReturnRequestBody, UpdateOrderSectionItemReturnRequestBody, UpdateOrderReturnRejectBody, UpdateOrderSectionReturnRejectBody, UpdateOrderSectionItemReturnRejectBody, UpdateOrderExchangeRequestBody, UpdateOrderSectionExchangeRequestBody, UpdateOrderSectionItemExchangeRequestBody, UpdateOrderExchangeRejectBody, UpdateOrderSectionExchangeRejectBody, UpdateOrderSectionCancelApproveBody, UpdateOrderSectionItemCancelApproveBody, UpdateOrderSectionReturnApproveBody, UpdateOrderSectionItemReturnApproveBody, UpdateOrderSectionExchangeApproveBody, UpdateOrderSectionItemExchangeApproveBody]

@mcp.tool()
def imweb_order(action: Literal["read_all_parcel_company_list", "read_all_shipping_place_list", "read_all_order", "read_one_order_by_order_no", "read_all_order_section", "read_one_order_section", "read_all_order_section_item", "read_one_order_section_item", "read_order_coupons", "update_order_shipping_operation", "update_order_section_shipping_operation", "update_order_section_item_shipping_operation", "create_order_invoice", "update_order_invoice", "remove_order_invoice", "create_order_section_invoice", "update_order_section_invoice", "remove_order_section_invoice", "create_order_section_item_invoice", "update_order_cancel_request", "update_order_section_cancel_request", "update_order_section_item_cancel_request", "update_order_cancel_reject", "update_order_section_cancel_reject", "update_order_section_item_cancel_reject", "update_order_return_request", "update_order_section_return_request", "update_order_section_item_return_request", "update_order_section_retrieve_complete", "update_order_return_reject", "update_order_section_return_reject", "update_order_section_item_return_reject", "update_order_exchange_request", "update_order_section_exchange_request", "update_order_section_item_exchange_request", "update_order_exchange_reject", "update_order_section_exchange_reject", "update_order_section_item_exchange_reject", "update_order_section_cancel_approve", "update_order_section_item_cancel_approve", "update_order_section_return_approve", "update_order_section_item_return_approve", "update_order_section_exchange_approve", "update_order_section_item_exchange_approve"], params: dict | None = None, body: Body | None = None, paginate: bool = False) -> dict:
    r"""주문 도구 — 44개 action 을 디스패치합니다.

Args:
    action: 수행 작업 키 (inputSchema enum 으로 44개 전체 공개).
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

