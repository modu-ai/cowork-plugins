"""아임웹 OPEN API OAuth2 토큰 갱신.

갱신 로직 자체는 공통 코어(`moai_mcp_core.OAuth2Refresher`)가 담당한다. 이 모듈은
아임웹 고유의 두 가지만 설정으로 표현한다.

1. **camelCase 키** — 아임웹은 `grantType` / `refreshToken` / `clientId` /
   `clientSecret` 표기를 쓴다(`/oauth2/authorize` 파라미터와 같은 계열). 문법 값
   (`refresh_token`)은 OAuth2 표준 그대로다.
2. **HTTP Basic 병행** — 요구하는 배포본은 통과하고, 무시하는 배포본은 그냥 넘어간다.

최초 브라우저 인가는 이 서버가 수행하지 않는다 — `CONNECTORS.md` 의 1회 절차다.
토큰 회전(아임웹은 줄 수도, 안 줄 수도 있다)은 코어가 처리한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import httpx
from moai_mcp_core import AuthError, OAuth2Config, OAuth2Refresher, SetupRequired

from ._base import token_store

if TYPE_CHECKING:
    from ._base import ImwebConfig


class ImwebAuthError(RuntimeError):
    """토큰 갱신 실패."""


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


def refresh_access_token(
    config: "ImwebConfig", client: Optional[httpx.Client] = None
) -> TokenPair:
    """리프레시 토큰으로 액세스 토큰을 새로 받는다 (RFC 6749 §6).

    Args:
        client: 예전 시그니처 호환용. 코어가 자체 클라이언트를 쓰므로 사용되지 않는다.
    """
    if not config.can_refresh:
        raise ImwebAuthError(
            "토큰 갱신 불가 — IMWEB_CLIENT_ID / IMWEB_CLIENT_SECRET / IMWEB_REFRESH_TOKEN 중 누락. "
            "CONNECTORS.md 의 절차에 따라 토큰을 (재)발급 받아 .mcp.json env 에 설정하세요."
        )

    refresher = OAuth2Refresher(
        OAuth2Config(
            token_url=f"{config.api_base}/oauth2/token",
            client_id=config.client_id,
            client_secret=config.client_secret,
            refresh_token=config.refresh_token,
            key_style="camel",
            basic_auth=True,
            setup_guide="CONNECTORS.md",
        ),
        token_store(config.token_file),
    )

    try:
        access = refresher.refresh()
    except (AuthError, SetupRequired) as exc:
        # 호출부(client.py)와 기존 테스트가 기대하는 예외 타입을 유지한다.
        raise ImwebAuthError(
            f"토큰 갱신 실패: {exc}. "
            "refresh_token 이 만료되었을 수 있습니다 — CONNECTORS.md 재발급 절차 참고."
        ) from exc

    return TokenPair(
        access_token=access,
        refresh_token=refresher.refresh_token or config.refresh_token,
    )
