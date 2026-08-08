"""문의(Inquiry) 도메인 도구 — 상품 QnA·고객(네이버페이 결제) 문의 답변."""
from __future__ import annotations

from typing import Any

from ..server import mcp
from ._common import call


@mcp.tool()
def qna_list(params: dict[str, Any] | None = None) -> dict:
    """상품 문의 목록 조회(미답변 모니터링/SLA 관리). GET /v1/contents/qnas"""
    return call("GET", "/v1/contents/qnas", params=params)


@mcp.tool()
def qna_answer(question_id: str, body: dict[str, Any]) -> dict:
    """상품 문의 답변 등록/수정. PUT /v1/contents/qnas/{questionId}

    body 예: {"answer": "답변 내용"}
    """
    return call("PUT", f"/v1/contents/qnas/{question_id}", body=body)


@mcp.tool()
def qna_templates() -> dict:
    """판매자 답변 템플릿 목록. GET /v1/contents/qnas/templates"""
    return call("GET", "/v1/contents/qnas/templates")


@mcp.tool()
def customer_inquiry_list(params: dict[str, Any] | None = None) -> dict:
    """고객 문의(네이버페이 결제 문의) 내역 조회. GET /v1/pay-user/inquiries"""
    return call("GET", "/v1/pay-user/inquiries", params=params)


@mcp.tool()
def customer_inquiry_answer(inquiry_no: str, body: dict[str, Any]) -> dict:
    """고객 문의 신규 답변 등록. POST /v1/pay-merchant/inquiries/{inquiryNo}/answer"""
    return call(
        "POST",
        f"/v1/pay-merchant/inquiries/{inquiry_no}/answer",
        body=body,
    )


@mcp.tool()
def customer_inquiry_answer_update(
    inquiry_no: str, answer_content_id: str, body: dict[str, Any]
) -> dict:
    """고객 문의 기존 답변 수정. PUT /v1/pay-merchant/inquiries/{inquiryNo}/answer/{answerContentId}"""
    return call(
        "PUT",
        f"/v1/pay-merchant/inquiries/{inquiry_no}/answer/{answer_content_id}",
        body=body,
    )
