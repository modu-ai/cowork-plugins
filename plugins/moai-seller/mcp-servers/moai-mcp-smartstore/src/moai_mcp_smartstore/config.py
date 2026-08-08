"""
환경변수 기반 설정.

네이버 커머스 API 자격증명은 환경변수로만 주입한다 — 코드·manifest·로그에
하드코딩 절대 금지 (CONNECTORS.md §보안 수칙).

환경변수:
  NAVER_COMMERCE_CLIENT_ID     — 애플리케이션 ID (필수)
  NAVER_COMMERCE_CLIENT_SECRET — 애플리케이션 시크릿 = bcrypt salt (필수)
  NAVER_COMMERCE_ACCOUNT_ID    — 판매자 계정 ID (type=SELLER 시 필수)
  NAVER_COMMERCE_TYPE          — 인증 주체 타입: SELF(기본) | SELLER
  NAVER_COMMERCE_BASE_URL      — API 게이트웨이 베이스 (기본: 공식 운영 URL)
  NAVER_COMMERCE_TIMEOUT       — HTTP 타임아웃 초 (기본: 30)
"""
from __future__ import annotations

import os
from dataclasses import dataclass

# 네이버 커머스 API 게이트웨이 (공식 운영 엔드포인트).
# 인증 토큰 발급: POST {BASE}/v1/oauth2/token
# 도메인 API  : {BASE}/v1/... , {BASE}/v2/...
DEFAULT_BASE_URL = "https://api.commerce.naver.com/external"


@dataclass(frozen=True)
class Config:
    """네이버 커머스 API 실행 설정 (환경변수에서 조립)."""

    client_id: str
    client_secret: str
    account_id: str
    type: str  # "SELF" | "SELLER"
    base_url: str
    timeout: float

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            client_id=os.environ.get("NAVER_COMMERCE_CLIENT_ID", ""),
            client_secret=os.environ.get("NAVER_COMMERCE_CLIENT_SECRET", ""),
            account_id=os.environ.get("NAVER_COMMERCE_ACCOUNT_ID", ""),
            type=(os.environ.get("NAVER_COMMERCE_TYPE", "SELF") or "SELF").upper(),
            base_url=os.environ.get("NAVER_COMMERCE_BASE_URL", DEFAULT_BASE_URL),
            timeout=float(os.environ.get("NAVER_COMMERCE_TIMEOUT", "30")),
        )

    @property
    def is_configured(self) -> bool:
        """토큰 발급에 필요한 최소 자격증명(client_id + client_secret) 존재 여부."""
        return bool(self.client_id and self.client_secret)

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/v1/oauth2/token"
