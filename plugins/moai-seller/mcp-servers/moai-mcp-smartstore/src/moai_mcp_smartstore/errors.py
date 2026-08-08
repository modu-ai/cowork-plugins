"""네이버 커머스 MCP 에러 계층."""
from __future__ import annotations


class NaverCommerceError(Exception):
    """네이버 커머스 MCP 오류 최상위."""


class ConfigError(NaverCommerceError):
    """환경변수 누락 등 설정 오류 (자격증명 미주입 상태)."""


class AuthError(NaverCommerceError):
    """토큰 발급 실패 또는 인증 오류."""


class ApiError(NaverCommerceError):
    """네이버 커머스 API 게이트웨이가 4xx/5xx 응답."""

    def __init__(self, status_code: int, body: str, response=None) -> None:
        super().__init__(f"naver commerce API error {status_code}: {body}")
        self.status_code = status_code
        self.body = body
        self.response = response
