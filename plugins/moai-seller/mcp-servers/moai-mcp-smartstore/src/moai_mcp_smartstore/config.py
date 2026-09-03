"""실행 설정.

네이버 커머스 API 자격증명은 코드·manifest·로그에 하드코딩하지 않는다
(CONNECTORS.md §보안 수칙). 값은 `moai_mcp_core.CredentialStore` 가
**환경변수 → `~/.moai/mcp/smartstore.json` → 기본값** 순으로 해석한다.

환경변수 하나에만 의존하지 않는 이유는 `moai_mcp_core/credentials.py` 에 적혀 있다 —
Claude·Codex 데스크톱 앱은 `.mcp.json` 의 `${KEY}` 를 확장하지 않고 자리표시자 문자열을
그대로 넘긴다. 그래서 자리표시자는 '값 없음' 으로 판정하고 파일로 넘어간다.

설정 키:
  NAVER_COMMERCE_CLIENT_ID     — 애플리케이션 ID (필수)
  NAVER_COMMERCE_CLIENT_SECRET — 애플리케이션 시크릿 = bcrypt salt (필수)
  NAVER_COMMERCE_ACCOUNT_ID    — 판매자 계정 ID (type=SELLER 시 필수)
  NAVER_COMMERCE_TYPE          — 인증 주체 타입: SELF(기본) | SELLER
  NAVER_COMMERCE_BASE_URL      — API 게이트웨이 베이스 (기본: 공식 운영 URL)
  NAVER_COMMERCE_TIMEOUT       — HTTP 타임아웃 초 (기본: 30)
"""
from __future__ import annotations

from dataclasses import dataclass

from moai_mcp_core import CredentialStore

# 자격증명 파일 슬러그 — `~/.moai/mcp/smartstore.json`.
SERVICE = "smartstore"

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
        """환경변수와 `~/.moai/mcp/smartstore.json` 에서 설정을 조립한다."""
        creds = CredentialStore(SERVICE)
        try:
            timeout = float(creds.get("NAVER_COMMERCE_TIMEOUT", "30"))
        except ValueError:
            # 잘못 적은 타임아웃 하나로 서버 전체가 못 뜨는 편보다 기본값이 낫다.
            timeout = 30.0
        return cls(
            client_id=creds.get("NAVER_COMMERCE_CLIENT_ID"),
            client_secret=creds.get("NAVER_COMMERCE_CLIENT_SECRET"),
            account_id=creds.get("NAVER_COMMERCE_ACCOUNT_ID"),
            type=creds.get("NAVER_COMMERCE_TYPE", "SELF").upper(),
            base_url=creds.get("NAVER_COMMERCE_BASE_URL", DEFAULT_BASE_URL),
            timeout=timeout,
        )

    @staticmethod
    def setup_hint() -> str:
        """자격증명이 비었을 때 사용자에게 보여줄 안내. 다 있으면 빈 문자열."""
        return CredentialStore(SERVICE).setup_hint(
            ["NAVER_COMMERCE_CLIENT_ID", "NAVER_COMMERCE_CLIENT_SECRET"]
        )

    @property
    def is_configured(self) -> bool:
        """토큰 발급에 필요한 최소 자격증명(client_id + client_secret) 존재 여부."""
        return bool(self.client_id and self.client_secret)

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/v1/oauth2/token"
