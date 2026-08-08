"""Cafe24 Admin API — Store domain (상점 설정).

Covers store/shops/dashboard/users info + the full set of store *settings*
(benefits, boards, carts, coupons, currency, customers, dormantaccount, images,
information, kakaoalimtalk, kakaopay, mobile, naverpay, orderform, orders,
payment, paymentgateway, paymentmethods, paymentservices, points, policy,
privacy, products, redirects, restocknotification, seo, shippingmanager, sms,
socials, subscription, taxmanager, automessages, categories/mains properties,
activitylogs, financials).

Most settings are GET (read_store) + PUT (write_store). ``shop_no`` is the
universal multi-shop selector (provided automatically by the dispatcher).
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "store"
_R = "mall.read_store"
_W = "mall.write_store"
_A = "/api/v2/admin"


def _setting(name: str, sub: str, summary: str, *, resource_key: str = "", extra_get=(), extra_put=()) -> tuple[Endpoint, Endpoint]:
    """Convenience: emit the GET (read) + PUT (write) pair for a setting."""
    base = f"{_A}/{sub}"
    rk = resource_key or sub.replace("/", "_")
    return (
        Endpoint(name=f"cafe24_store_{name}_get", category=_C, method="GET", path=base, scope=_R,
                 summary=f"{summary} 조회", resource_key=rk, query_params=extra_get),
        Endpoint(name=f"cafe24_store_{name}_update", category=_C, method="PUT", path=base, scope=_W,
                 summary=f"{summary} 수정", resource_key=rk, takes_body=True, query_params=extra_put),
    )


_settings_pairs = [
    _setting("benefits", "benefits/setting", "사은품/혜택 설정"),
    _setting("boards", "boards/setting", "게시판 설정"),
    _setting("carts", "carts/setting", "장바구니 설정"),
    _setting("coupons", "coupons/setting", "쿠폰 설정"),
    _setting("customers", "customers/setting", "회원 관련 설정"),
    _setting("dormantaccount", "dormantaccount", "휴면계정 설정"),
    _setting("images", "images/setting", "상품 이미지 사이즈 설정"),
    _setting("information", "information", "기타 이용안내"),
    _setting("kakaoalimtalk", "kakaoalimtalk/setting", "카카오알림톡 설정"),
    _setting("kakaopay", "kakaopay/setting", "카카오페이 설정"),
    _setting("mains_properties", "mains/properties/setting", "메인 화면 항목 추가 설정"),
    _setting("mobile", "mobile/setting", "모바일 설정"),
    _setting("naverpay", "naverpay/setting", "네이버페이 설정"),
    _setting("orderform", "orderform/setting", "주문서 설정"),
    _setting("orders", "orders/setting", "주문 설정"),
    _setting("payment", "payment/setting", "결제 설정"),
    _setting("points", "points/setting", "적립금 설정"),
    _setting("privacy_boards", "privacy/boards", "게시판 개인정보처리방침"),
    _setting("privacy_join", "privacy/join", "회원가입 개인정보처리방침"),
    _setting("privacy_orders", "privacy/orders", "주문 개인정보처리방침"),
    _setting("products_properties", "products/properties/setting", "상품 상세 항목 추가 설정"),
    _setting("restocknotification", "restocknotification/setting", "재입고알림 설정"),
    _setting("seo", "seo/setting", "SEO 설정"),
    _setting("sms", "sms/setting", "SMS 설정"),
    _setting("subscription", "subscription/shipments/setting", "정기배송 설정"),
    _setting("automessages", "automessages/setting", "자동메시지 발송 설정"),
    _setting("categories_properties", "categories/properties/setting", "상품 목록 항목 추가 설정"),
]
# Flatten the pairs into a single list and register.
_store_setting_endpoints: list[Endpoint] = []
for pair in _settings_pairs:
    _store_setting_endpoints.extend(pair)

register(
    # === Core store info ===
    Endpoint(name="cafe24_store_get", category=_C, method="GET", path=f"{_A}/store", scope=_R,
             summary="상점 기본 정보 조회 (쇼핑몰명/사업자/고객센터 등)", resource_key="store"),
    Endpoint(name="cafe24_store_account_list", category=_C, method="GET", path=f"{_A}/store/accounts", scope=_R,
             summary="무통장입금 계좌 목록", resource_key="account", list_endpoint=True),
    Endpoint(name="cafe24_store_dropshipping_get", category=_C, method="GET", path=f"{_A}/store/dropshipping", scope=_R,
             summary="드롭쉬핑 설정 조회", resource_key="dropshipping"),
    Endpoint(name="cafe24_store_dropshipping_update", category=_C, method="PUT", path=f"{_A}/store/dropshipping", scope=_W,
             summary="드롭쉬핑 설정 수정", resource_key="dropshipping", takes_body=True),
    Endpoint(name="cafe24_store_dashboard", category=_C, method="GET", path=f"{_A}/dashboard", scope=_R,
             summary="대시보드 조회 (주문/매출 현황 요약)", resource_key="dashboard"),
    Endpoint(name="cafe24_store_currency_get", category=_C, method="GET", path=f"{_A}/currency", scope=_R,
             summary="환율/화폐 정보 조회", resource_key="currency"),
    Endpoint(name="cafe24_store_currency_update", category=_C, method="PUT", path=f"{_A}/currency", scope=_W,
             summary="환율 정보 수정", resource_key="currency", takes_body=True),
    Endpoint(name="cafe24_store_policy_get", category=_C, method="GET", path=f"{_A}/policy", scope=_R,
             summary="이용약관/개인정보처리방침 조회", resource_key="policy"),
    Endpoint(name="cafe24_store_policy_update", category=_C, method="PUT", path=f"{_A}/policy", scope=_W,
             summary="이용약관/개인정보처리방침 수정", resource_key="policy", takes_body=True),
    Endpoint(name="cafe24_store_shippingmanager_get", category=_C, method="GET", path=f"{_A}/shippingmanager", scope=_R,
             summary="배송관리자 활성화 정보", resource_key="shippingmanager"),
    Endpoint(name="cafe24_store_taxmanager_get", category=_C, method="GET", path=f"{_A}/taxmanager", scope=_R,
             summary="세금관리자(MSA) 활성화 정보", resource_key="taxmanager"),
    Endpoint(name="cafe24_store_orders_status_get", category=_C, method="GET", path=f"{_A}/orders/status", scope=_R,
             summary="주문상태 표기 관리 조회", resource_key="order_status", list_endpoint=True),
    Endpoint(name="cafe24_store_orders_status_update", category=_C, method="PUT", path=f"{_A}/orders/status", scope=_W,
             summary="주문상태 표기 관리 수정", resource_key="order_status", takes_body=True, body_key="orders_status"),
    Endpoint(name="cafe24_store_products_setting_get", category=_C, method="GET", path=f"{_A}/products/setting", scope=_R,
             summary="상품 판매가 설정 조회", resource_key="products_setting"),

    # === Shops (multi-shop) ===
    Endpoint(name="cafe24_shop_list", category=_C, method="GET", path=f"{_A}/shops", scope=_R,
             summary="멀티쇼핑몰 목록", resource_key="shop", list_endpoint=True),
    Endpoint(name="cafe24_shop_get", category=_C, method="GET", path=f"{_A}/shops/{{shop_no}}", scope=_R,
             summary="멀티쇼핑몰 상세", resource_key="shop"),

    # === Users (운영자) ===
    Endpoint(name="cafe24_user_list", category=_C, method="GET", path=f"{_A}/users", scope=_R,
             summary="운영자 목록 조회", resource_key="user", list_endpoint=True,
             query_params=(Param("search_type", description="member_Id/name"), Param("keyword"), Param("admin_type", description="P 대표/A 부"))),
    Endpoint(name="cafe24_user_get", category=_C, method="GET", path=f"{_A}/users/{{user_id}}", scope=_R,
             summary="운영자 상세 조회", resource_key="user"),

    # === Menus ===
    Endpoint(name="cafe24_menu_list", category=_C, method="GET", path=f"{_A}/menus", scope=_R,
             summary="메뉴(프로/스마트/모바일 어드민) 조회", resource_key="menu", list_endpoint=True,
             query_params=(Param("mode", description="new_pro/mobile_admin"), Param("menu_no"), Param("contains_app_url", description="T/F"))),

    # === Activity logs ===
    Endpoint(name="cafe24_activitylog_list", category=_C, method="GET", path=f"{_A}/activitylogs", scope=_R,
             summary="활동로그 목록 (특정클라이언트 전용)", resource_key="activitylog", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("limit", type="int"), Param("offset", type="int"))),
    Endpoint(name="cafe24_activitylog_get", category=_C, method="GET", path=f"{_A}/activitylogs/{{process_no}}", scope=_R,
             summary="활동로그 상세", resource_key="activitylog"),

    # === Redirects ===
    Endpoint(name="cafe24_redirect_list", category=_C, method="GET", path=f"{_A}/redirects", scope=_R,
             summary="리다이렉트 목록", resource_key="redirect", list_endpoint=True),
    Endpoint(name="cafe24_redirect_create", category=_C, method="POST", path=f"{_A}/redirects", scope=_W,
             summary="리다이렉트 등록", resource_key="redirect", takes_body=True),
    Endpoint(name="cafe24_redirect_update", category=_C, method="PUT", path=f"{_A}/redirects/{{id}}", scope=_W,
             summary="리다이렉트 수정", resource_key="redirect", takes_body=True),
    Endpoint(name="cafe24_redirect_delete", category=_C, method="DELETE", path=f"{_A}/redirects/{{id}}", scope=_W,
             summary="리다이렉트 삭제", resource_key="redirect"),

    # === Automessages arguments ===
    Endpoint(name="cafe24_automessage_argument_list", category=_C, method="GET", path=f"{_A}/automessages/arguments", scope=_R,
             summary="자동메시지 사용 가능 변수 목록", resource_key="automessage_argument", list_endpoint=True),

    # === Kakao alimtalk profile ===
    Endpoint(name="cafe24_kakaoalimtalk_profile_get", category=_C, method="GET", path=f"{_A}/kakaoalimtalk/profile", scope=_R,
             summary="카카오채널 발신 프로필키 조회", resource_key="kakaoalimtalk_profile"),

    # === Payment gateway & methods ===
    Endpoint(name="cafe24_paymentgateway_create", category=_C, method="POST", path=f"{_A}/paymentgateway", scope=_W,
             summary="PG 등록 (특정클라이언트)", resource_key="paymentgateway", takes_body=True),
    Endpoint(name="cafe24_paymentgateway_update", category=_C, method="PUT", path=f"{_A}/paymentgateway/{{client_id}}", scope=_W,
             summary="PG 수정", resource_key="paymentgateway", takes_body=True),
    Endpoint(name="cafe24_paymentgateway_delete", category=_C, method="DELETE", path=f"{_A}/paymentgateway/{{client_id}}", scope=_W,
             summary="PG 삭제", resource_key="paymentgateway"),
    Endpoint(name="cafe24_paymentgateway_method_list", category=_C, method="GET", path=f"{_A}/paymentgateway/{{client_id}}/paymentmethods", scope=_R,
             summary="PG 결제수단 목록", resource_key="paymentgateway_paymentmethod", list_endpoint=True),
    Endpoint(name="cafe24_paymentgateway_method_create", category=_C, method="POST", path=f"{_A}/paymentgateway/{{client_id}}/paymentmethods", scope=_W,
             summary="PG 결제수단 등록", resource_key="paymentgateway_paymentmethod", takes_body=True),
    Endpoint(name="cafe24_paymentgateway_method_update", category=_C, method="PUT", path=f"{_A}/paymentgateway/{{client_id}}/paymentmethods/{{payment_method_code}}", scope=_W,
             summary="PG 결제수단 수정", resource_key="paymentgateway_paymentmethod", takes_body=True),
    Endpoint(name="cafe24_paymentgateway_method_delete", category=_C, method="DELETE", path=f"{_A}/paymentgateway/{{client_id}}/paymentmethods/{{payment_method_code}}", scope=_W,
             summary="PG 결제수단 삭제", resource_key="paymentgateway_paymentmethod"),
    Endpoint(name="cafe24_paymentmethod_list", category=_C, method="GET", path=f"{_A}/paymentmethods", scope=_R,
             summary="결제수단 목록 (특정클라이언트)", resource_key="paymentmethod", list_endpoint=True),
    Endpoint(name="cafe24_paymentprovider_list", category=_C, method="GET", path=f"{_A}/paymentmethods/{{code}}/paymentproviders", scope=_R,
             summary="결제수단 PG사 목록", resource_key="paymentprovider", list_endpoint=True),
    Endpoint(name="cafe24_paymentprovider_update", category=_C, method="PUT", path=f"{_A}/paymentmethods/{{code}}/paymentproviders/{{name}}", scope=_W,
             summary="결제수단 노출여부 수정", resource_key="paymentprovider", takes_body=True),
    Endpoint(name="cafe24_paymentservice_list", category=_C, method="GET", path=f"{_A}/paymentservices", scope=_R,
             summary="PG 설정 목록 (특정클라이언트)", resource_key="paymentservice", list_endpoint=True),

    # === Financials ===
    Endpoint(name="cafe24_financial_paymentgateway_list", category=_C, method="GET", path=f"{_A}/financials/paymentgateway", scope=_R,
             summary="PG 계약정보 목록 (특정클라이언트)", resource_key="financial_paymentgateway", list_endpoint=True),
    Endpoint(name="cafe24_financial_store_get", category=_C, method="GET", path=f"{_A}/financials/store", scope=_R,
             summary="상점 거래정보 (특정클라이언트)", resource_key="financial_store"),

    # === Socials ===
    Endpoint(name="cafe24_social_apple_get", category=_C, method="GET", path=f"{_A}/socials/apple", scope=_R,
             summary="애플 로그인 연동정보", resource_key="social_apple"),
    Endpoint(name="cafe24_social_apple_update", category=_C, method="PUT", path=f"{_A}/socials/apple", scope=_W,
             summary="애플 로그인 연동설정", resource_key="social_apple", takes_body=True),
    Endpoint(name="cafe24_social_kakaosync_get", category=_C, method="GET", path=f"{_A}/socials/kakaosync", scope=_R,
             summary="카카오싱크 설정 조회", resource_key="social_kakaosync"),
    Endpoint(name="cafe24_social_kakaosync_update", category=_C, method="PUT", path=f"{_A}/socials/kakaosync", scope=_W,
             summary="카카오싱크 설정 수정", resource_key="social_kakaosync", takes_body=True),
    Endpoint(name="cafe24_social_naverlogin_get", category=_C, method="GET", path=f"{_A}/socials/naverlogin", scope=_R,
             summary="네이버 로그인 설정 조회", resource_key="social_naverlogin"),
    Endpoint(name="cafe24_social_naverlogin_update", category=_C, method="PUT", path=f"{_A}/socials/naverlogin", scope=_W,
             summary="네이버 로그인 설정 수정", resource_key="social_naverlogin", takes_body=True),
    Endpoint(name="cafe24_social_navershopping_get", category=_C, method="GET", path=f"{_A}/socials/navershopping", scope=_R,
             summary="네이버쇼핑 설정 조회", resource_key="social_navershopping"),

    # === Naverpay create (POST variant for initial registration) ===
    Endpoint(name="cafe24_naverpay_create", category=_C, method="POST", path=f"{_A}/naverpay/setting", scope=_W,
             summary="네이버페이 설정 최초 등록 (가맹 인증키)", resource_key="naverpay", takes_body=True),

    *_store_setting_endpoints,
)
