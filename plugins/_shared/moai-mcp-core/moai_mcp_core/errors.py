"""자체 제작 MCP 서버 공통 오류 타입.

MCP 도구는 예외를 밖으로 던지면 안 된다 — 서버가 죽으면 사용자는 원인을 모른 채
연결이 끊긴 화면만 본다. 대신 구조화된 오류 응답을 돌려주고 서버는 살아 있는다.

`to_tool_result()` 가 그 변환을 담당한다.
"""

from __future__ import annotations

from typing import Any


class McpToolError(Exception):
    """도구 실행 중 발생한, 사용자에게 설명 가능한 오류."""

    code = "tool_error"
    retryable = False

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details: dict[str, Any] = details or {}

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": False,
            "error": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details:
            payload["details"] = self.details
        return payload


class SetupRequired(McpToolError):
    """자격증명이 아예 없는 상태.

    사용자가 아직 연동을 하지 않은 것이므로 실패가 아니라 안내 대상이다.
    서버는 절대 크래시하지 않고 이 오류를 돌려준다.
    """

    code = "setup_required"

    def __init__(
        self,
        message: str,
        *,
        missing: list[str] | None = None,
        guide: str | None = None,
    ) -> None:
        details: dict[str, Any] = {}
        if missing:
            details["missing_env"] = missing
        if guide:
            details["guide"] = guide
        super().__init__(message, details=details)


class AuthError(McpToolError):
    """토큰 갱신 실패·권한 부족 등 인증 단계 오류."""

    code = "auth_error"


class RateLimited(McpToolError):
    """상대 API의 호출 한도에 걸린 상태."""

    code = "rate_limited"
    retryable = True

    def __init__(self, message: str, *, retry_after: float | None = None) -> None:
        details: dict[str, Any] = {}
        if retry_after is not None:
            details["retry_after_seconds"] = retry_after
        super().__init__(message, details=details)
        self.retry_after = retry_after


class QuotaExhausted(McpToolError):
    """일일 할당량 소진. 재시도해도 그날 안에는 풀리지 않는다."""

    code = "quota_exhausted"


class UpstreamError(McpToolError):
    """상대 API가 4xx/5xx를 돌려준 경우."""

    code = "upstream_error"

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        body: str | None = None,
    ) -> None:
        details: dict[str, Any] = {}
        if status is not None:
            details["status"] = status
            self.retryable = status >= 500
        if body:
            # 응답 본문은 길 수 있고 자격증명이 섞일 수 있어 앞부분만 남긴다.
            details["body"] = body[:500]
        super().__init__(message, details=details)
        self.status = status


def to_tool_result(exc: Exception) -> dict[str, Any]:
    """예외를 MCP 도구 응답 딕셔너리로 변환한다.

    McpToolError 계열이 아닌 예외도 삼켜서 구조화한다 — 예상 못 한 오류로
    서버가 죽는 것이 가장 나쁜 결과이기 때문이다.
    """
    if isinstance(exc, McpToolError):
        return exc.to_dict()
    return {
        "ok": False,
        "error": "internal_error",
        "message": f"{type(exc).__name__}: {exc}",
        "retryable": False,
    }
