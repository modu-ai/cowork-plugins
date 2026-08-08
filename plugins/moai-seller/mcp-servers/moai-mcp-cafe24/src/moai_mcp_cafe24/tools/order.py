"""Cafe24 Admin API — Order domain (주문).

The largest and most operationally critical domain. Covers orders + the full
CS lifecycle: cancellation / exchange / return / refund (both bulk top-level
resources and per-order sub-resources), shipments, fulfillments, items &
item labels/options, buyer & receivers (with history), payment timeline,
cash receipts, claims requests, dashboard, inflow groups, sales channels,
subscriptions, unpaid orders, and order migrations.

Scopes: ``mall.read_order`` / ``mall.write_order``.

Note on order status codes (N00/N10/.../N50, C00..C49, R00..R43, E00..E40):
pass them comma-joined to ``order_status``. Search windows are ≤ 3 months per
call (use ``date_type`` + start/end to page through history).
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "order"
_R = "mall.read_order"
_W = "mall.write_order"
_O = "/api/v2/admin/orders"

_ORDER_FILTERS = (
    Param("start_date", description="검색 시작일 (date_type 기준)"),
    Param("end_date", description="검색 종료일 (한 호출에 3개월 이내)"),
    Param("date_type", description="검색날짜 유형: order_date/pay_date/shipbegin_date/shipend_date/cancel_date/..."),
    Param("order_id", description="주문번호 (콤마로 다중)"),
    Param("order_status", description="주문상태 코드 (콤마로 다중): N00,N10,...,C40,R40,E40 등"),
    Param("payment_status", description="결제상태: F/M/T/A/P"),
    Param("member_id", description="회원아이디"),
    Param("buyer_name", description="주문자명"),
    Param("receiver_name", description="수령자명"),
    Param("product_no", description="상품번호"),
    Param("payment_method", description="결제수단 코드 (콤마로 다중)"),
    Param("order_place_id", description="주문경로 (콤마로 다중)"),
    Param("embed", description="하위 리소스: items,receivers,buyer,return,cancellation,exchange,benefits,coupons,refunds"),
    Param("limit", type="int", description="최대건수 (최대 1000)"),
    Param("offset", type="int", description="시작위치 (orders: 최대 15000)"),
)

register(
    # === Orders (main) ===
    Endpoint(name="cafe24_order_list", category=_C, method="GET", path=_O, scope=_R,
             summary="주문 목록 조회", resource_key="order", list_endpoint=True, query_params=_ORDER_FILTERS,
             notes="검색기간 한 호출당 3개월 이내. offset 최대 15000."),
    Endpoint(name="cafe24_order_get", category=_C, method="GET", path=f"{_O}/{{order_id}}", scope=_R,
             summary="주문 상세 조회", resource_key="order",
             query_params=(Param("embed", description="items,receivers,buyer,benefits,coupons,return,cancellation,exchange,refunds"),)),
    Endpoint(name="cafe24_order_count", category=_C, method="GET", path=f"{_O}/count", scope=_R,
             summary="주문 수 조회", resource_key="count", query_params=_ORDER_FILTERS),
    Endpoint(name="cafe24_order_update_bulk", category=_C, method="PUT", path=_O, scope=_W,
             summary="주문 일괄 상태수정 (최대 100건)", resource_key="order", takes_body=True, body_key="orders"),
    Endpoint(name="cafe24_order_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}", scope=_W,
             summary="주문 1건 상태수정 (배송준비중/상품준비중/배송보류 등)", resource_key="order", takes_body=True),

    # === Order items (품주) ===
    Endpoint(name="cafe24_order_item_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/items", scope=_R,
             summary="주문 품주 목록 조회", resource_key="item", list_endpoint=True,
             query_params=(Param("supplier_id", description="공급사 아이디"),)),
    Endpoint(name="cafe24_order_item_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/items", scope=_W,
             summary="세트 품주 나눔처리", resource_key="item", takes_body=True),
    Endpoint(name="cafe24_order_item_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/items/{{order_item_code}}", scope=_W,
             summary="품주 상태수정 (취소/반품/교환 사유 입력)", resource_key="item", takes_body=True),

    # === Item labels ===
    Endpoint(name="cafe24_order_item_label_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/labels", scope=_R,
             summary="품목 라벨 조회", resource_key="label", list_endpoint=True),
    Endpoint(name="cafe24_order_item_label_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/labels", scope=_W,
             summary="품목 라벨 등록", resource_key="label", takes_body=True, body_key="labels"),
    Endpoint(name="cafe24_order_item_label_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/labels", scope=_W,
             summary="품목 라벨 수정", resource_key="label", takes_body=True, body_key="labels"),
    Endpoint(name="cafe24_order_item_label_delete", category=_C, method="DELETE", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/labels/{{name}}", scope=_W,
             summary="품목 라벨 삭제", resource_key="label"),

    # === Item options ===
    Endpoint(name="cafe24_order_item_option_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/options", scope=_W,
             summary="품목 추가입력 옵션 등록", resource_key="option", takes_body=True),
    Endpoint(name="cafe24_order_item_option_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/items/{{order_item_code}}/options", scope=_W,
             summary="품목 추가입력 옵션 수정", resource_key="option", takes_body=True),

    # === Order memos (per-order) ===
    Endpoint(name="cafe24_order_memo_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/memos", scope=_R,
             summary="주문 메모 목록 조회", resource_key="memo", list_endpoint=True),
    Endpoint(name="cafe24_order_memo_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/memos", scope=_W,
             summary="주문 메모 등록", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_order_memo_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/memos/{{memo_no}}", scope=_W,
             summary="주문 메모 수정", resource_key="memo", takes_body=True),
    Endpoint(name="cafe24_order_memo_delete", category=_C, method="DELETE", path=f"{_O}/{{order_id}}/memos/{{memo_no}}", scope=_W,
             summary="주문 메모 삭제", resource_key="memo"),

    # === Buyer & receivers ===
    Endpoint(name="cafe24_order_buyer_get", category=_C, method="GET", path=f"{_O}/{{order_id}}/buyer", scope=_R,
             summary="주문자 정보 조회", resource_key="buyer"),
    Endpoint(name="cafe24_order_buyer_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/buyer", scope=_W,
             summary="주문자 정보 수정", resource_key="buyer", takes_body=True),
    Endpoint(name="cafe24_order_buyer_history", category=_C, method="GET", path=f"{_O}/{{order_id}}/buyer/history", scope=_R,
             summary="주문자 수정 이력 조회", resource_key="history", list_endpoint=True),
    Endpoint(name="cafe24_order_receiver_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/receivers", scope=_R,
             summary="수령자 정보 목록 조회", resource_key="receiver", list_endpoint=True),
    Endpoint(name="cafe24_order_receiver_update_bulk", category=_C, method="PUT", path=f"{_O}/{{order_id}}/receivers", scope=_W,
             summary="수령자 정보 일괄 수정", resource_key="receiver", takes_body=True, body_key="receivers"),
    Endpoint(name="cafe24_order_receiver_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/receivers/{{shipping_code}}", scope=_W,
             summary="특정 배송번호 수령자/배송정보 수정", resource_key="receiver", takes_body=True),
    Endpoint(name="cafe24_order_receiver_history", category=_C, method="GET", path=f"{_O}/{{order_id}}/receivers/history", scope=_R,
             summary="수령자 변경 이력 조회", resource_key="history", list_endpoint=True),

    # === Shipments (per-order) ===
    Endpoint(name="cafe24_order_shipment_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/shipments", scope=_R,
             summary="주문 배송정보 목록 조회", resource_key="shipment", list_endpoint=True),
    Endpoint(name="cafe24_order_shipment_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/shipments", scope=_W,
             summary="주문 배송정보 등록 (배송대기/배송중)", resource_key="shipment", takes_body=True),
    Endpoint(name="cafe24_order_shipment_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/shipments/{{shipping_code}}", scope=_W,
             summary="주문 배송정보 수정", resource_key="shipment", takes_body=True),
    Endpoint(name="cafe24_order_shipment_delete", category=_C, method="DELETE", path=f"{_O}/{{order_id}}/shipments/{{shipping_code}}", scope=_W,
             summary="주문 배송번호 삭제", resource_key="shipment"),

    # === Payments (per-order) ===
    Endpoint(name="cafe24_order_payment_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/payments", scope=_W,
             summary="주문 결제상태 수정", resource_key="payment", takes_body=True),
    Endpoint(name="cafe24_order_paymenttimeline_list", category=_C, method="GET", path=f"{_O}/{{order_id}}/paymenttimeline", scope=_R,
             summary="주문 결제 타임라인 조회", resource_key="payment", list_endpoint=True),
    Endpoint(name="cafe24_order_paymenttimeline_get", category=_C, method="GET", path=f"{_O}/{{order_id}}/paymenttimeline/{{payment_no}}", scope=_R,
             summary="결제번호 1건 상세 조회", resource_key="payment"),

    # === Per-order claims ===
    Endpoint(name="cafe24_order_cancellation_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/cancellation", scope=_W,
             summary="주문 취소처리 (PG취소 옵션 포함)", resource_key="cancellation", takes_body=True),
    Endpoint(name="cafe24_order_cancellation_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/cancellation/{{claim_code}}", scope=_W,
             summary="주문 취소접수 철회/수정", resource_key="cancellation", takes_body=True),
    Endpoint(name="cafe24_order_return_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/return", scope=_W,
             summary="주문 반품처리 (PG취소 옵션 포함)", resource_key="return", takes_body=True),
    Endpoint(name="cafe24_order_return_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/return/{{claim_code}}", scope=_W,
             summary="주문 반품접수 철회/수정", resource_key="return", takes_body=True),
    Endpoint(name="cafe24_order_exchange_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/exchange", scope=_W,
             summary="주문 교환접수 처리", resource_key="exchange", takes_body=True),
    Endpoint(name="cafe24_order_exchange_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/exchange/{{claim_code}}", scope=_W,
             summary="주문 교환접수 철회/수정", resource_key="exchange", takes_body=True),
    Endpoint(name="cafe24_order_exchangerequest_reject", category=_C, method="PUT", path=f"{_O}/{{order_id}}/exchangerequests", scope=_W,
             summary="교환요청 접수거부", resource_key="exchangerequest", takes_body=True),
    Endpoint(name="cafe24_order_refund_update", category=_C, method="PUT", path=f"{_O}/{{order_id}}/refunds/{{refund_code}}", scope=_W,
             summary="주문 환불상태 수정 (환불완료 처리)", resource_key="refund", takes_body=True),

    # === Misc per-order ===
    Endpoint(name="cafe24_order_benefit_list", category=_C, method="GET", path=f"{_O}/benefits", scope=_R,
             summary="주문 적용 혜택 조회", resource_key="benefit", list_endpoint=True,
             query_params=(Param("order_id", required=True, description="주문번호 (콤마 다중)"),)),
    Endpoint(name="cafe24_order_coupon_list", category=_C, method="GET", path=f"{_O}/coupons", scope=_R,
             summary="주문 적용 쿠폰 조회", resource_key="coupon", list_endpoint=True,
             query_params=(Param("order_id", required=True, description="주문번호 (콤마 다중)"),)),
    Endpoint(name="cafe24_order_paymentamount_get", category=_C, method="GET", path=f"{_O}/paymentamount", scope=_R,
             summary="품목별 실결제금액 조회 (할인금액자동계산 대상만)", resource_key="payment_amount", list_endpoint=True,
             query_params=(Param("order_item_code", required=True, description="품주코드 (콤마 다중)"),)),
    Endpoint(name="cafe24_order_autocalculation_remove", category=_C, method="DELETE", path=f"{_O}/{{order_id}}/autocalculation", scope=_W,
             summary="주문 자동금액계산 해제 (취소/교환/반품 허용)", resource_key="autocalculation"),
    Endpoint(name="cafe24_order_shippingfeecancellation_get", category=_C, method="GET", path=f"{_O}/{{order_id}}/shippingfeecancellation", scope=_R,
             summary="배송비 취소현황 조회", resource_key="shippingfeecancellation", list_endpoint=True),
    Endpoint(name="cafe24_order_shippingfeecancellation_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/shippingfeecancellation", scope=_W,
             summary="배송비 취소처리 요청", resource_key="shippingfeecancellation", takes_body=True),
    Endpoint(name="cafe24_order_shortagecancellation_create", category=_C, method="POST", path=f"{_O}/{{order_id}}/shortagecancellation", scope=_W,
             summary="재고부족 취소처리 (취소완료+환불)", resource_key="shortagecancellation", takes_body=True),

    # === Order-level (non order_id path) ===
    Endpoint(name="cafe24_order_dashboard", category=_C, method="GET", path=f"{_O}/dashboard", scope=_R,
             summary="주문 요약 대시보드 (최근 1개월 누적)", resource_key="dashboard"),
    Endpoint(name="cafe24_order_calculation", category=_C, method="POST", path=f"{_O}/calculation", scope=_W,
             summary="결제예정금액 계산", resource_key="calculation", takes_body=True),
    Endpoint(name="cafe24_order_memo_global_list", category=_C, method="GET", path=f"{_O}/memos", scope=_R,
             summary="여러 주문의 관리자 메모 목록 조회", resource_key="memo", list_endpoint=True,
             query_params=(Param("order_id", required=True, description="주문번호 (콤마 다중)"), Param("limit", type="int"), Param("offset", type="int"))),
    Endpoint(name="cafe24_order_migration_list", category=_C, method="GET", path=f"{_O}/migrations", scope=_R,
             summary="이전몰 주문 조회", resource_key="migration", list_endpoint=True),
    Endpoint(name="cafe24_order_migration_create", category=_C, method="POST", path=f"{_O}/migrations", scope=_W,
             summary="이전몰 주문 등록", resource_key="migration", takes_body=True, body_key="migrations"),
    Endpoint(name="cafe24_order_migration_update", category=_C, method="PUT", path=f"{_O}/migrations", scope=_W,
             summary="이전몰 주문 수정", resource_key="migration", takes_body=True, body_key="migrations"),
    Endpoint(name="cafe24_order_migration_delete", category=_C, method="DELETE", path=f"{_O}/migrations/{{order_id}}", scope=_W,
             summary="이전몰 주문 삭제", resource_key="migration"),

    # === Inflow groups & inflows ===
    Endpoint(name="cafe24_order_inflowgroup_list", category=_C, method="GET", path=f"{_O}/inflowgroups", scope=_R,
             summary="유입경로 그룹 목록", resource_key="inflowgroup", list_endpoint=True),
    Endpoint(name="cafe24_order_inflowgroup_create", category=_C, method="POST", path=f"{_O}/inflowgroups", scope=_W,
             summary="유입경로 그룹 생성", resource_key="inflowgroup", takes_body=True),
    Endpoint(name="cafe24_order_inflowgroup_update", category=_C, method="PUT", path=f"{_O}/inflowgroups/{{inflow_group_id}}", scope=_W,
             summary="유입경로 그룹 수정", resource_key="inflowgroup", takes_body=True),
    Endpoint(name="cafe24_order_inflowgroup_delete", category=_C, method="DELETE", path=f"{_O}/inflowgroups/{{inflow_group_id}}", scope=_W,
             summary="유입경로 그룹 삭제", resource_key="inflowgroup"),
    Endpoint(name="cafe24_order_inflow_list", category=_C, method="GET", path=f"{_O}/inflowgroups/{{group_id}}/inflows", scope=_R,
             summary="그룹 내 유입경로 목록", resource_key="inflow", list_endpoint=True),
    Endpoint(name="cafe24_order_inflow_create", category=_C, method="POST", path=f"{_O}/inflowgroups/{{group_id}}/inflows", scope=_W,
             summary="그룹 내 유입경로 생성", resource_key="inflow", takes_body=True),
    Endpoint(name="cafe24_order_inflow_update", category=_C, method="PUT", path=f"{_O}/inflowgroups/{{group_id}}/inflows/{{inflow_id}}", scope=_W,
             summary="그룹 내 유입경로 수정", resource_key="inflow", takes_body=True),
    Endpoint(name="cafe24_order_inflow_delete", category=_C, method="DELETE", path=f"{_O}/inflowgroups/{{group_id}}/inflows/{{inflow_id}}", scope=_W,
             summary="그룹 내 유입경로 삭제", resource_key="inflow"),

    # === Sales channels ===
    Endpoint(name="cafe24_order_saleschannel_list", category=_C, method="GET", path=f"{_O}/saleschannels", scope=_R,
             summary="판매채널 목록", resource_key="saleschannel", list_endpoint=True),
    Endpoint(name="cafe24_order_saleschannel_create", category=_C, method="POST", path=f"{_O}/saleschannels", scope=_W,
             summary="판매채널 등록", resource_key="saleschannel", takes_body=True),
    Endpoint(name="cafe24_order_saleschannel_update", category=_C, method="PUT", path=f"{_O}/saleschannels/{{sales_channel_id}}", scope=_W,
             summary="판매채널 수정", resource_key="saleschannel", takes_body=True),
    Endpoint(name="cafe24_order_saleschannel_delete", category=_C, method="DELETE", path=f"{_O}/saleschannels/{{sales_channel_id}}", scope=_W,
             summary="판매채널 삭제", resource_key="saleschannel"),

    # === Orderform properties (주문서 추가항목) ===
    Endpoint(name="cafe24_orderform_property_list", category=_C, method="GET", path="/api/v2/admin/orderform/properties", scope=_R,
             summary="주문서 추가항목 조회", resource_key="orderform_property", list_endpoint=True),
    Endpoint(name="cafe24_orderform_property_create", category=_C, method="POST", path="/api/v2/admin/orderform/properties", scope=_W,
             summary="주문서 추가항목 생성", resource_key="orderform_property", takes_body=True, body_key="orderform_properties"),
    Endpoint(name="cafe24_orderform_property_update", category=_C, method="PUT", path="/api/v2/admin/orderform/properties/{orderform_property_id}", scope=_W,
             summary="주문서 추가항목 수정", resource_key="orderform_property", takes_body=True),
    Endpoint(name="cafe24_orderform_property_delete", category=_C, method="DELETE", path="/api/v2/admin/orderform/properties/{orderform_property_id}", scope=_W,
             summary="주문서 추가항목 삭제", resource_key="orderform_property"),

    # === Bulk claims (top-level, multi-order) ===
    Endpoint(name="cafe24_cancellation_get", category=_C, method="GET", path="/api/v2/admin/cancellation/{claim_code}", scope=_R,
             summary="취소 상세 조회", resource_key="cancellation"),
    Endpoint(name="cafe24_cancellation_create_bulk", category=_C, method="POST", path="/api/v2/admin/cancellation", scope=_W,
             summary="다건 주문 취소 (PG취소 미진행)", resource_key="cancellation", takes_body=True, body_key="cancellations"),
    Endpoint(name="cafe24_cancellation_update_bulk", category=_C, method="PUT", path="/api/v2/admin/cancellation", scope=_W,
             summary="다건 취소 상태 수정/철회", resource_key="cancellation", takes_body=True, body_key="cancellations"),
    Endpoint(name="cafe24_cancellationrequest_create", category=_C, method="POST", path="/api/v2/admin/cancellationrequests", scope=_W,
             summary="취소요청 접수 (다건)", resource_key="cancellationrequest", takes_body=True, body_key="cancellationrequests"),
    Endpoint(name="cafe24_cancellationrequest_reject", category=_C, method="PUT", path="/api/v2/admin/cancellationrequests", scope=_W,
             summary="취소요청 접수거부 (다건)", resource_key="cancellationrequest", takes_body=True, body_key="cancellationrequests"),
    Endpoint(name="cafe24_exchange_get", category=_C, method="GET", path="/api/v2/admin/exchange/{claim_code}", scope=_R,
             summary="교환 상세 조회", resource_key="exchange"),
    Endpoint(name="cafe24_exchange_create_bulk", category=_C, method="POST", path="/api/v2/admin/exchange", scope=_W,
             summary="다건 교환접수", resource_key="exchange", takes_body=True, body_key="exchanges"),
    Endpoint(name="cafe24_exchange_update_bulk", category=_C, method="PUT", path="/api/v2/admin/exchange", scope=_W,
             summary="다건 교환 수정/철회", resource_key="exchange", takes_body=True, body_key="exchanges"),
    Endpoint(name="cafe24_exchangerequest_create", category=_C, method="POST", path="/api/v2/admin/exchangerequests", scope=_W,
             summary="교환요청 접수 (다건)", resource_key="exchangerequest", takes_body=True, body_key="exchangerequests"),
    Endpoint(name="cafe24_exchangerequest_reject", category=_C, method="PUT", path="/api/v2/admin/exchangerequests", scope=_W,
             summary="교환요청 접수거부 (다건)", resource_key="exchangerequest", takes_body=True, body_key="exchangerequests"),
    Endpoint(name="cafe24_return_get", category=_C, method="GET", path="/api/v2/admin/return/{claim_code}", scope=_R,
             summary="반품 상세 조회", resource_key="return"),
    Endpoint(name="cafe24_return_create_bulk", category=_C, method="POST", path="/api/v2/admin/return", scope=_W,
             summary="다건 반품접수", resource_key="return", takes_body=True, body_key="returns"),
    Endpoint(name="cafe24_return_update_bulk", category=_C, method="PUT", path="/api/v2/admin/return", scope=_W,
             summary="다건 반품 수정/철회", resource_key="return", takes_body=True, body_key="returns"),
    Endpoint(name="cafe24_returnrequest_create", category=_C, method="POST", path="/api/v2/admin/returnrequests", scope=_W,
             summary="반품요청 접수 (다건)", resource_key="returnrequest", takes_body=True, body_key="returnrequests"),
    Endpoint(name="cafe24_returnrequest_reject", category=_C, method="PUT", path="/api/v2/admin/returnrequests", scope=_W,
             summary="반품요청 접수거부 (다건)", resource_key="returnrequest", takes_body=True, body_key="returnrequests"),
    Endpoint(name="cafe24_refund_list", category=_C, method="GET", path="/api/v2/admin/refunds", scope=_R,
             summary="환불 목록 조회", resource_key="refund", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True),
                           Param("date_type", description="accepted_refund_date/refund_date"), Param("order_id"), Param("refund_status"))),
    Endpoint(name="cafe24_refund_get", category=_C, method="GET", path="/api/v2/admin/refunds/{refund_code}", scope=_R,
             summary="환불 상세 조회", resource_key="refund"),

    # === Payments / Shipments / Fulfillments / Collect (bulk, multi-order) ===
    Endpoint(name="cafe24_payment_update_bulk", category=_C, method="PUT", path="/api/v2/admin/payments", scope=_W,
             summary="다건 결제상태 수정 (입금확인/취소)", resource_key="payment", takes_body=True, body_key="payments"),
    Endpoint(name="cafe24_shipment_create_bulk", category=_C, method="POST", path="/api/v2/admin/shipments", scope=_W,
             summary="다건 배송정보 등록 (배송대기/배송중)", resource_key="shipment", takes_body=True, body_key="shipments"),
    Endpoint(name="cafe24_shipment_update_bulk", category=_C, method="PUT", path="/api/v2/admin/shipments", scope=_W,
             summary="다건 배송정보 수정", resource_key="shipment", takes_body=True, body_key="shipments"),
    Endpoint(name="cafe24_fulfillment_create_bulk", category=_C, method="POST", path="/api/v2/admin/fulfillments", scope=_W,
             summary="Fulfillment 배송정보 등록 (배송앱 연동)", resource_key="fulfillment", takes_body=True, body_key="fulfillments"),
    Endpoint(name="cafe24_collectrequest_update", category=_C, method="PUT", path="/api/v2/admin/collectrequests/{request_no}", scope=_W,
             summary="수거신청 정보 수정 (수거 송장번호)", resource_key="collectrequest", takes_body=True),
    Endpoint(name="cafe24_label_list", category=_C, method="GET", path="/api/v2/admin/labels", scope=_R,
             summary="주문 라벨 조회", resource_key="label", list_endpoint=True),
    Endpoint(name="cafe24_label_create_bulk", category=_C, method="POST", path="/api/v2/admin/labels", scope=_W,
             summary="다건 주문 라벨 등록", resource_key="label", takes_body=True, body_key="labels"),
    Endpoint(name="cafe24_control", category=_C, method="PUT", path="/api/v2/admin/control", scope=_W,
             summary="주문 입금확인 제한여부 설정", resource_key="control", takes_body=True),

    # === Cash receipts ===
    Endpoint(name="cafe24_cashreceipt_list", category=_C, method="GET", path="/api/v2/admin/cashreceipt", scope=_R,
             summary="현금영수증 목록 (한국어 쇼핑몰만)", resource_key="cashreceipt", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("order_id"), Param("status"))),
    Endpoint(name="cafe24_cashreceipt_create", category=_C, method="POST", path="/api/v2/admin/cashreceipt", scope=_W,
             summary="현금영수증 발급", resource_key="cashreceipt", takes_body=True),
    Endpoint(name="cafe24_cashreceipt_update", category=_C, method="PUT", path="/api/v2/admin/cashreceipt/{cashreceipt_no}", scope=_W,
             summary="현금영수증 수정", resource_key="cashreceipt", takes_body=True),
    Endpoint(name="cafe24_cashreceipt_cancellation", category=_C, method="PUT", path="/api/v2/admin/cashreceipt/{cashreceipt_no}/cancellation", scope=_W,
             summary="현금영수증 신청/발행 취소", resource_key="cashreceipt", takes_body=True),

    # === Reservations & unpaid ===
    Endpoint(name="cafe24_reservation_list", category=_C, method="GET", path="/api/v2/admin/reservations", scope=_R,
             summary="예약(서비스) 주문 조회", resource_key="reservation", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("date_type"))),
    Endpoint(name="cafe24_unpaidorder_list", category=_C, method="GET", path="/api/v2/admin/unpaidorders", scope=_R,
             summary="미입금 주문 조회", resource_key="unpaidorder", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("payment_method"))),

    # === Subscription shipments ===
    Endpoint(name="cafe24_subscription_shipment_list", category=_C, method="GET", path="/api/v2/admin/subscription/shipments", scope=_R,
             summary="정기배송 목록 조회", resource_key="subscription", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("date_type"), Param("subscription_state"))),
    Endpoint(name="cafe24_subscription_shipment_create", category=_C, method="POST", path="/api/v2/admin/subscription/shipments", scope=_W,
             summary="정기배송 등록", resource_key="subscription", takes_body=True, body_key="subscriptions"),
    Endpoint(name="cafe24_subscription_shipment_update", category=_C, method="PUT", path="/api/v2/admin/subscription/shipments/{subscription_id}", scope=_W,
             summary="정기배송 수정 (수령자/상태)", resource_key="subscription", takes_body=True),
    Endpoint(name="cafe24_subscription_shipment_item_update", category=_C, method="PUT", path="/api/v2/admin/subscription/shipments/{subscription_id}/items", scope=_W,
             summary="정기배송 품목별 수정", resource_key="subscription", takes_body=True, body_key="items"),
)
