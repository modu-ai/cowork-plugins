"""Cafe24 Admin API — Application domain (앱).

Covers app info/version, appstore orders & payments, databridge webhook logs,
recipes (automation triggers), script tags (front-end script injection), and
webhook logs/settings.

Scopes: ``mall.read_application`` / ``mall.write_application``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "application"
_R = "mall.read_application"
_W = "mall.write_application"
_A = "/api/v2/admin"

register(
    # === Apps ===
    Endpoint(name="cafe24_app_get", category=_C, method="GET", path=f"{_A}/apps", scope=_R,
             summary="앱 정보/버전 조회", resource_key="app"),
    Endpoint(name="cafe24_app_update", category=_C, method="PUT", path=f"{_A}/apps", scope=_W,
             summary="앱 버전 변경", resource_key="app", takes_body=True),

    # === Appstore orders ===
    Endpoint(name="cafe24_appstore_order_get", category=_C, method="GET", path=f"{_A}/appstore/orders/{{order_id}}", scope=_R,
             summary="앱스토어 주문 조회", resource_key="appstore_order"),
    Endpoint(name="cafe24_appstore_order_create", category=_C, method="POST", path=f"{_A}/appstore/orders", scope=_W,
             summary="앱스토어 주문 생성 (사용요금 부과)", resource_key="appstore_order", takes_body=True),

    # === Appstore payments ===
    Endpoint(name="cafe24_appstore_payment_list", category=_C, method="GET", path=f"{_A}/appstore/payments", scope=_R,
             summary="앱스토어 결제 내역 목록", resource_key="appstore_payment", list_endpoint=True,
             query_params=(Param("start_date", required=True), Param("end_date", required=True), Param("order_id"))),
    Endpoint(name="cafe24_appstore_payment_count", category=_C, method="GET", path=f"{_A}/appstore/payments/count", scope=_R,
             summary="앱스토어 결제 내역 수", resource_key="count",
             query_params=(Param("start_date", required=True), Param("end_date", required=True))),

    # === Databridge logs ===
    Endpoint(name="cafe24_databridge_log_list", category=_C, method="GET", path=f"{_A}/databridge/logs", scope=_R,
             summary="Databridge 웹훅 로그 목록", resource_key="databridge_log", list_endpoint=True,
             query_params=(Param("requested_start_date"), Param("requested_end_date"), Param("success", description="T/F"), Param("since_log_id", type="int"), Param("limit", type="int"))),

    # === Recipes ===
    Endpoint(name="cafe24_recipe_list", category=_C, method="GET", path=f"{_A}/recipes", scope=_R,
             summary="레시피 목록", resource_key="recipe", list_endpoint=True),
    Endpoint(name="cafe24_recipe_create", category=_C, method="POST", path=f"{_A}/recipes", scope=_W,
             summary="레시피 등록", resource_key="recipe", takes_body=True, body_key="recipes"),
    Endpoint(name="cafe24_recipe_delete", category=_C, method="DELETE", path=f"{_A}/recipes/{{recipe_code}}", scope=_W,
             summary="레시피 등록해제", resource_key="recipe"),

    # === Script tags ===
    Endpoint(name="cafe24_scripttag_list", category=_C, method="GET", path=f"{_A}/scripttags", scope=_R,
             summary="스크립트태그 목록", resource_key="scripttag", list_endpoint=True,
             query_params=(Param("script_no"), Param("src"), Param("display_location"), Param("skin_no"))),
    Endpoint(name="cafe24_scripttag_count", category=_C, method="GET", path=f"{_A}/scripttags/count", scope=_R,
             summary="스크립트태그 수", resource_key="count"),
    Endpoint(name="cafe24_scripttag_get", category=_C, method="GET", path=f"{_A}/scripttags/{{script_no}}", scope=_R,
             summary="스크립트태그 상세", resource_key="scripttag"),
    Endpoint(name="cafe24_scripttag_create", category=_C, method="POST", path=f"{_A}/scripttags", scope=_W,
             summary="스크립트태그 설치", resource_key="scripttag", takes_body=True),
    Endpoint(name="cafe24_scripttag_update", category=_C, method="PUT", path=f"{_A}/scripttags/{{script_no}}", scope=_W,
             summary="스크립트태그 수정", resource_key="scripttag", takes_body=True),
    Endpoint(name="cafe24_scripttag_delete", category=_C, method="DELETE", path=f"{_A}/scripttags/{{script_no}}", scope=_W,
             summary="스크립트태그 삭제", resource_key="scripttag"),

    # === Webhooks ===
    Endpoint(name="cafe24_webhook_log_list", category=_C, method="GET", path=f"{_A}/webhooks/logs", scope=_R,
             summary="웹훅 로그 목록", resource_key="webhook_log", list_endpoint=True,
             query_params=(Param("event_no"), Param("requested_start_date"), Param("requested_end_date"), Param("success", description="T/F"), Param("log_type", description="G/R/T"), Param("since_log_id", type="int"))),
    Endpoint(name="cafe24_webhook_setting_get", category=_C, method="GET", path=f"{_A}/webhooks/setting", scope=_R,
             summary="웹훅 수신 설정 조회", resource_key="webhook_setting"),
    Endpoint(name="cafe24_webhook_setting_update", category=_C, method="PUT", path=f"{_A}/webhooks/setting", scope=_W,
             summary="웹훅 수신 설정 수정", resource_key="webhook_setting", takes_body=True),
)
