"""OAuth2 액세스 토큰 갱신.

우리가 붙는 서비스(네이버 커머스·아임웹·카페24·Threads·YouTube)는 모두
"짧은 액세스 토큰 + 긴 리프레시 토큰" 구조다. 세부 차이는 두 가지뿐이다.

1. 리프레시 토큰이 **회전**하는가 (카페24가 그렇다 — 갱신 때마다 새로 발급되고 옛것은 죽는다)
2. 만료 시각을 어떻게 주는가 (`expires_in` 초 단위가 표준)

이 모듈은 둘 다 처리한다. 서비스별 차이는 `OAuth2Config` 로만 표현한다.
"""

from __future__ import annotations

import base64
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import httpx

from .errors import AuthError, SetupRequired
from .tokenstore import TokenStore


#: 갱신 요청 본문의 키 이름. 표준은 snake_case지만 camelCase를 요구하는 서비스가 있다
#: (아임웹이 그렇다 — `grantType` / `refreshToken` / `clientId` / `clientSecret`).
KEY_STYLES: dict[str, dict[str, str]] = {
    "snake": {
        "grant_type": "grant_type",
        "refresh_token": "refresh_token",
        "client_id": "client_id",
        "client_secret": "client_secret",
    },
    "camel": {
        "grant_type": "grantType",
        "refresh_token": "refreshToken",
        "client_id": "clientId",
        "client_secret": "clientSecret",
    },
}


@dataclass
class OAuth2Config:
    """서비스별 OAuth2 갱신 설정."""

    token_url: str
    client_id: str | None = None
    client_secret: str | None = None
    refresh_token: str | None = None
    #: 갱신 요청에 함께 보낼 추가 파라미터 (서비스마다 요구가 다르다).
    extra_params: dict[str, str] = field(default_factory=dict)
    #: 자격증명이 없을 때 사용자에게 안내할 문서 경로.
    setup_guide: str | None = None
    #: 만료 몇 초 전부터 미리 갱신할지. 요청 도중 만료되는 사고를 막는다.
    leeway_seconds: float = 60.0
    #: 요청 본문 키 표기 — `snake`(표준) 또는 `camel`.
    key_style: str = "snake"
    #: HTTP Basic 인증 헤더를 함께 보낼지. 요구하는 서버는 통과하고,
    #: 무시하는 서버는 그냥 넘어가므로 켜도 해롭지 않다.
    basic_auth: bool = False


class OAuth2Refresher:
    """액세스 토큰을 캐시하고, 만료가 임박하면 갱신한다.

    Args:
        config: 서비스별 설정.
        store: 토큰 영속화 담당.
        transport: 테스트에서 갈아 끼울 httpx 전송 계층.
        clock: 테스트에서 시간을 고정하기 위한 시각 함수.
    """

    def __init__(
        self,
        config: OAuth2Config,
        store: TokenStore,
        *,
        transport: httpx.BaseTransport | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.config = config
        self.store = store
        self._clock = clock
        self._transport = transport

        saved = store.load()
        self._access_token: str | None = saved.get("access_token")
        self._expires_at: float = float(saved.get("expires_at") or 0)
        # 저장된 리프레시 토큰이 환경변수보다 최신이다(회전했을 수 있으므로).
        self._refresh_token: str | None = saved.get("refresh_token") or config.refresh_token

    @property
    def refresh_token(self) -> str | None:
        return self._refresh_token

    def access_token(self, *, force: bool = False) -> str:
        """유효한 액세스 토큰을 돌려준다. 필요하면 갱신한다.

        Args:
            force: 만료 전이라도 강제로 갱신한다 (401을 받았을 때 사용).
        """
        if not force and self._access_token and not self._is_expiring():
            return self._access_token
        return self.refresh()

    def refresh(self) -> str:
        """리프레시 토큰으로 액세스 토큰을 새로 받는다."""
        self._require_credentials()

        keys = KEY_STYLES.get(self.config.key_style, KEY_STYLES["snake"])
        data = {
            keys["grant_type"]: "refresh_token",
            keys["refresh_token"]: self._refresh_token,
            **self.config.extra_params,
        }
        if self.config.client_id:
            data[keys["client_id"]] = self.config.client_id
        if self.config.client_secret:
            data[keys["client_secret"]] = self.config.client_secret

        headers = {"Accept": "application/json"}
        if self.config.basic_auth and self.config.client_id:
            raw = f"{self.config.client_id}:{self.config.client_secret or ''}".encode()
            headers["Authorization"] = f"Basic {base64.b64encode(raw).decode()}"

        try:
            with httpx.Client(transport=self._transport, timeout=30.0) as client:
                response = client.post(self.config.token_url, data=data, headers=headers)
        except httpx.HTTPError as exc:
            raise AuthError(f"토큰 갱신 요청이 실패했습니다: {exc}") from exc

        if response.status_code >= 400:
            raise AuthError(
                "토큰 갱신이 거부되었습니다. 리프레시 토큰이 만료되었거나 취소되었을 수 있습니다.",
                details={"status": response.status_code, "body": response.text[:500]},
            )

        try:
            payload: dict[str, Any] = response.json()
        except ValueError as exc:
            raise AuthError("토큰 갱신 응답을 해석할 수 없습니다.") from exc

        # 응답 키는 관대하게 읽는다 — 같은 서비스가 문서와 실제 응답에서
        # 다른 표기를 쓰는 경우가 있어, 둘 다 받아들이는 편이 안전하다.
        access = payload.get("access_token") or payload.get("accessToken")
        if not access:
            raise AuthError(
                "토큰 갱신 응답에 access_token 이 없습니다.",
                details={"keys": sorted(payload)},
            )

        self._access_token = str(access)
        expires_in = payload.get("expires_in") or payload.get("expiresIn")
        try:
            self._expires_at = self._clock() + float(expires_in) if expires_in else 0.0
        except (TypeError, ValueError):
            self._expires_at = 0.0

        # 회전형 서비스는 새 리프레시 토큰을 함께 준다. 놓치면 다음 갱신이 영구 실패한다.
        rotated = payload.get("refresh_token") or payload.get("refreshToken")
        if rotated:
            self._refresh_token = str(rotated)

        self.store.save(
            {
                "access_token": self._access_token,
                "refresh_token": self._refresh_token,
                "expires_at": self._expires_at,
            }
        )
        return self._access_token

    def _is_expiring(self) -> bool:
        if not self._expires_at:
            # 만료 시각을 모르면 캐시된 토큰을 그대로 쓴다.
            # 실제로 만료됐다면 401이 오고, HttpClient가 강제 갱신한다.
            return False
        return self._clock() >= self._expires_at - self.config.leeway_seconds

    def _require_credentials(self) -> None:
        missing = []
        if not self._refresh_token:
            missing.append("REFRESH_TOKEN")
        if not self.config.client_id:
            missing.append("CLIENT_ID")
        if not self.config.client_secret:
            missing.append("CLIENT_SECRET")
        if missing:
            raise SetupRequired(
                "연동에 필요한 자격증명이 아직 설정되지 않았습니다.",
                missing=missing,
                guide=self.config.setup_guide,
            )
