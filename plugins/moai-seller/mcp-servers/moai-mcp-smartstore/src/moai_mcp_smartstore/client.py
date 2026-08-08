"""
네이버 커머스 API HTTP 클라이언트.

책임:
  1. OAuth2 토큰 발급 (bcrypt 전자서명) + 만료시간 캐싱(스레드 안전).
  2. 도메인 API 호출 시 Authorization: Bearer 헤더 자동 주입.
  3. 401 + GW.AUTHN 응답(토큰 만료) 감지 → 토큰 강제 재발급 후 1회 재시도.

공식 권장 fallback (https://apicenter.commerce.naver.com/docs/auth):
    retry { API_호출(access_token) }
    when { 401 && body.code == 'GW.AUTHN' }
    before { 토큰_재발급() }

토큰 발급 요청 본문은 OAuth2 표준(application/x-www-form-urlencoded)을 따른다.
"""
from __future__ import annotations

import threading
import time
from typing import Any

import requests

from .auth import generate_signature
from .config import Config
from .errors import ApiError, AuthError

# 토큰 만료 임계 여유분(초) — 만료 직전 미리 갱신.
_TOKEN_REFRESH_MARGIN = 60.0
# GW.AUTHN 오류 코드 — 401 응답에서 토큰 만료 신호.
_GW_AUTHN_CODE = "GW.AUTHN"


class NaverCommerceClient:
    """네이버 커머스 API 게이트웨이 호출 클라이언트."""

    def __init__(
        self,
        config: Config,
        session: requests.Session | None = None,
    ) -> None:
        self._config = config
        self._session = session or requests.Session()
        self._token: str | None = None
        self._token_expiry: float = 0.0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # 토큰 발급 / 캐싱
    # ------------------------------------------------------------------
    def _token_request_form(self, timestamp_ms: int) -> dict[str, str]:
        form: dict[str, str] = {
            "client_id": self._config.client_id,
            "timestamp": str(timestamp_ms),
            "grant_type": "client_credentials",
            "client_secret_sign": generate_signature(
                self._config.client_id,
                self._config.client_secret,
                timestamp_ms,
            ),
            "type": self._config.type,
        }
        if self._config.type == "SELLER" and self._config.account_id:
            form["account_id"] = self._config.account_id
        return form

    def get_token(self, force: bool = False) -> str:
        """캐시된 토큰 반환. 만료 임박/force 시 재발급. 스레드 안전."""
        with self._lock:
            now = time.time()
            if (
                not force
                and self._token
                and now < self._token_expiry - _TOKEN_REFRESH_MARGIN
            ):
                return self._token

            timestamp_ms = int(time.time() * 1000)
            form = self._token_request_form(timestamp_ms)
            resp = self._session.post(
                self._config.token_url,
                data=form,
                timeout=self._config.timeout,
            )
            if not resp.ok:
                raise AuthError(
                    f"token issuance failed: HTTP {resp.status_code} {resp.text}"
                )
            body = self._json(resp)
            token = body.get("access_token")
            if not token:
                raise AuthError(f"no access_token in token response: {body}")
            expires_in = float(body.get("expires_in", 3600))
            self._token = token
            self._token_expiry = now + expires_in
            return token

    # ------------------------------------------------------------------
    # 도메인 API 호출
    # ------------------------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """도메인 API 호출. path 는 '/v1/...' 또는 '/v2/...' 형태.

        401 GW.AUTHN 발생 시 토큰 재발급 후 1회 재시도.
        """
        url = f"{self._config.base_url}{path}"
        return self._request_with_retry(
            method, url, params=params, json=json, allow_retry=True
        )

    def _request_with_retry(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None,
        json: dict[str, Any] | None,
        allow_retry: bool,
    ) -> Any:
        token = self.get_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        resp = self._session.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json,
            timeout=self._config.timeout,
        )

        # 토큰 만료(401 + GW.AUTHN) → 재발급 후 1회 재시도.
        if resp.status_code == 401 and allow_retry:
            if self._is_token_expired(resp):
                self.get_token(force=True)
                return self._request_with_retry(
                    method, url, params=params, json=json, allow_retry=False
                )

        if not resp.ok:
            raise ApiError(resp.status_code, resp.text, response=resp)

        if resp.content:
            # 본문이 비어있지 않으면 JSON 우선 파싱, 실패 시 원문 반환.
            try:
                return resp.json()
            except ValueError:
                return resp.text
        return None

    # ------------------------------------------------------------------
    # 헬퍼
    # ------------------------------------------------------------------
    @staticmethod
    def _is_token_expired(resp: requests.Response) -> bool:
        try:
            body = resp.json()
        except ValueError:
            return False
        return str(body.get("code", "")).upper() == _GW_AUTHN_CODE

    @staticmethod
    def _json(resp: requests.Response) -> dict[str, Any]:
        try:
            data = resp.json()
        except ValueError as exc:
            raise AuthError(f"non-JSON token response: {resp.text}") from exc
        return data if isinstance(data, dict) else {"data": data}


# ----------------------------------------------------------------------
# 모듈 수준 싱글톤 — MCP 도구 호출마다 환경변수 재조립 비용 회피.
# ----------------------------------------------------------------------
_singleton_lock = threading.Lock()
_client: NaverCommerceClient | None = None


def get_client() -> NaverCommerceClient:
    """환경변수 설정 기반 싱글톤 클라이언트 반환."""
    global _client
    with _singleton_lock:
        if _client is None:
            _client = NaverCommerceClient(Config.from_env())
        return _client


def reset_client() -> None:
    """테스트/설정 변경 시 싱글톤 초기화."""
    global _client
    with _singleton_lock:
        _client = None
