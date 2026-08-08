"""도구 공용 헬퍼 — 자격증명 검증, 도메인 API 호출, 결과 래핑.

모든 MCP 도구는 call() 을 통해 네이버 커머스 API 를 호출한다. 자격증명 미설정·
API 에러·네트워크 오류를 예외가 아닌 안전한 dict 로 반환해, MCP 호출자(LLM)가
항상 구조화된 응답을 받도록 한다.
"""
from __future__ import annotations

from typing import Any

from ..client import get_client
from ..config import Config

_NOT_CONFIGURED_MSG = (
    "네이버 커머스 API 자격증명이 설정되지 않았습니다. "
    "NAVER_COMMERCE_CLIENT_ID, NAVER_COMMERCE_CLIENT_SECRET 환경변수를 설정하세요. "
    "발급 절차는 CONNECTORS.md 참고."
)


def call(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    endpoint: str | None = None,
) -> dict[str, Any]:
    """도메인 API 호출 + 표준 결과 래핑.

    Returns:
        성공: {"ok": True, "endpoint": ..., "data": <원시 API JSON>}
        실패: {"ok": False, "endpoint": ..., "error": ..., "status": ..., "message": ...}
        미설정: {"ok": False, "error": "not_configured", "message": ...}
    """
    if not Config.from_env().is_configured:
        return {"ok": False, "error": "not_configured", "message": _NOT_CONFIGURED_MSG}

    ep = endpoint or f"{method} {path}"
    try:
        data = get_client().request(method, path, params=params, json=body)
    except Exception as exc:  # ApiError / AuthError / 네트워크 오류
        return {
            "ok": False,
            "endpoint": ep,
            "error": type(exc).__name__,
            "status": getattr(exc, "status_code", None),
            "message": str(exc),
        }
    return {"ok": True, "endpoint": ep, "data": data}


def config_status() -> dict[str, Any]:
    """자격증명 설정 상태(로컬, API 미호출). 비밀키 원문은 절대 포함하지 않는다."""
    cfg = Config.from_env()
    return {
        "configured": cfg.is_configured,
        "type": cfg.type,
        "base_url": cfg.base_url,
        "account_id_set": bool(cfg.account_id),
        "client_id_set": bool(cfg.client_id),
    }
