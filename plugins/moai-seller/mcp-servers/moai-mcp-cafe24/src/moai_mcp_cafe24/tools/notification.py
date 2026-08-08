"""Cafe24 Admin API — Notification domain (알림).

자동메일(automails), 회원 초대(invitation), 발송그룹(recipientgroups),
SMS 발송(sms) + 잔여건수/수신자/발신자.

Scopes: ``mall.read_notification`` / ``mall.write_notification``.
"""

from __future__ import annotations

from ..registry import Endpoint, Param, register

_C = "notification"
_R = "mall.read_notification"
_W = "mall.write_notification"
_A = "/api/v2/admin"
_LIST = (Param("limit", type="int"), Param("offset", type="int"))

register(
    # === Automails ===
    Endpoint(name="cafe24_automail_list", category=_C, method="GET", path=f"{_A}/automails", scope=_R,
             summary="자동 알림메일 설정 목록", resource_key="automail", list_endpoint=True),
    Endpoint(name="cafe24_automail_update", category=_C, method="PUT", path=f"{_A}/automails", scope=_W,
             summary="자동 알림메일 설정 일괄 수정 (고객/운영자/공급사)", resource_key="automail", takes_body=True, body_key="automails"),

    # === Customer invitation ===
    Endpoint(name="cafe24_customer_invitation_send", category=_C, method="POST", path=f"{_A}/customers/{{member_id}}/invitation", scope=_W,
             summary="계정 활성화 초대 발송 (SMS/이메일)", resource_key="invitation", takes_body=True),

    # === Recipient groups (발송그룹) ===
    Endpoint(name="cafe24_recipientgroup_list", category=_C, method="GET", path=f"{_A}/recipientgroups", scope=_R,
             summary="대량메일 발송그룹 목록", resource_key="recipientgroup", list_endpoint=True, query_params=_LIST),
    Endpoint(name="cafe24_recipientgroup_get", category=_C, method="GET", path=f"{_A}/recipientgroups/{{group_no}}", scope=_R,
             summary="발송그룹 상세", resource_key="recipientgroup"),
    Endpoint(name="cafe24_recipientgroup_create", category=_C, method="POST", path=f"{_A}/recipientgroups", scope=_W,
             summary="발송그룹 생성", resource_key="recipientgroup", takes_body=True),
    Endpoint(name="cafe24_recipientgroup_update", category=_C, method="PUT", path=f"{_A}/recipientgroups/{{group_no}}", scope=_W,
             summary="발송그룹 수정", resource_key="recipientgroup", takes_body=True),
    Endpoint(name="cafe24_recipientgroup_delete", category=_C, method="DELETE", path=f"{_A}/recipientgroups/{{group_no}}", scope=_W,
             summary="발송그룹 삭제", resource_key="recipientgroup"),

    # === SMS ===
    Endpoint(name="cafe24_sms_send", category=_C, method="POST", path=f"{_A}/sms", scope=_W,
             summary="SMS/LMS 발송 (한국어 쇼핑몰만, 필수: sender_no/content)", resource_key="sms", takes_body=True),
    Endpoint(name="cafe24_sms_balance_get", category=_C, method="GET", path=f"{_A}/sms/balance", scope=_R,
             summary="SMS 잔여 발송건수 조회", resource_key="sms_balance"),
    Endpoint(name="cafe24_sms_receiver_list", category=_C, method="GET", path=f"{_A}/sms/receivers", scope=_R,
             summary="SMS 수신자(운영자/공급사 알림) 목록", resource_key="sms_receiver", list_endpoint=True,
             query_params=_LIST + (Param("recipient_type", description="ALL/S/A"), Param("user_id"), Param("supplier_id"))),
    Endpoint(name="cafe24_sms_sender_list", category=_C, method="GET", path=f"{_A}/sms/senders", scope=_R,
             summary="SMS 발신자 번호 목록 (인증상태 포함)", resource_key="sms_sender", list_endpoint=True, query_params=_LIST),
)
