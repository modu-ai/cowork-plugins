"""카페24 API OAuth2 토큰 갱신.

갱신 로직은 공통 코어(`moai_mcp_core.OAuth2Refresher`)가 담당한다. 카페24 고유의
성질은 하나다.

**리프레시 토큰이 회전한다.** 갱신할 때마다 새 리프레시 토큰이 나오고 **이전 것은
즉시 무효화**된다(카페24 문서: "기존 refresh token은 만료처리되어 사용할 수
없습니다"). 새 값을 놓치면 다음 갱신이 영구 실패하므로, 반환된 쌍을 반드시 저장해야
한다 — 코어가 회전을 처리하고 `_base._persist_tokens` 가 저장 실패를 stderr 로 알린다.

액세스 토큰 수명은 2시간, 리프레시 토큰은 2주다. 최초 브라우저 인가는 이 서버가
수행하지 않는다 — `README.md` 의 1회 절차다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import httpx
from moai_mcp_core import AuthError, OAuth2Config, OAuth2Refresher, SetupRequired

from ._base import token_store

if TYPE_CHECKING:
    from ._base import Cafe24Config


class Cafe24AuthError(RuntimeError):
    """토큰 갱신 실패."""


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str


def refresh_access_token(
    config: "Cafe24Config", client: Optional[httpx.Client] = None
) -> TokenPair:
    """리프레시 토큰으로 액세스 토큰을 새로 받는다 (RFC 6749 §6).

    Returns:
        **새** 토큰 쌍. 카페24가 이전 리프레시 토큰을 무효화하므로 두 값 모두
        저장된 값을 대체해야 한다.

    Args:
        client: 예전 시그니처 호환용. 코어가 자체 클라이언트를 쓰므로 사용되지 않는다.
    """
    if not config.can_refresh:
        raise Cafe24AuthError(
            "토큰 갱신 불가 — CAFE24_MALL_ID / CAFE24_CLIENT_ID / CAFE24_CLIENT_SECRET / "
            "CAFE24_REFRESH_TOKEN 중 누락. README.md 의 절차에 따라 토큰을 (재)발급 받아 "
            ".mcp.json env 에 설정하세요."
        )

    refresher = OAuth2Refresher(
        OAuth2Config(
            token_url=f"{config.admin_base}/api/v2/oauth/token",
            client_id=config.client_id,
            client_secret=config.client_secret,
            refresh_token=config.refresh_token,
            basic_auth=True,
            setup_guide="README.md",
        ),
        token_store(config.token_file),
    )

    try:
        access = refresher.refresh()
    except (AuthError, SetupRequired) as exc:
        # 호출부(client.py)가 기대하는 예외 타입을 유지한다.
        raise Cafe24AuthError(
            f"토큰 갱신 실패: {exc}. "
            "refresh_token 이 만료(2주)되었을 수 있습니다 — README.md 재발급 절차 참고."
        ) from exc

    return TokenPair(
        access_token=access,
        # 서버가 예기치 않게 회전 토큰을 생략하면 쓰던 값을 유지한다.
        refresh_token=refresher.refresh_token or config.refresh_token,
    )
