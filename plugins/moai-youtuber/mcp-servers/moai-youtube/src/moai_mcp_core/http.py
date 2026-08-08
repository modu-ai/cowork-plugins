# 이 파일은 자동 생성된 복제본입니다 — 직접 수정하지 마세요.
# 정본: plugins/_shared/moai-mcp-core/http.py
# 동기화: python3 scripts/sync-mcp-core.py
"""공통 HTTP 클라이언트.

각 서버가 따로 만들던 재시도·백오프·401 재인증 로직을 한곳으로 모았다.

정책은 세 가지다.

- **401** — 액세스 토큰을 강제 갱신하고 **딱 한 번** 재시도한다. 두 번째도 401이면
  자격증명 자체가 잘못된 것이므로 재시도가 무의미하다.
- **429** — `Retry-After` 를 존중한다. 헤더가 없으면 지수 백오프.
- **5xx** — 지수 백오프로 재시도. 상대 서버의 일시적 문제일 가능성이 높다.

4xx(401·429 제외)는 재시도하지 않는다 — 같은 요청은 같은 결과를 낸다.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import Any, Protocol

import httpx

from .errors import AuthError, RateLimited, UpstreamError


class TokenProvider(Protocol):
    """`OAuth2Refresher` 가 만족하는 최소 인터페이스."""

    def access_token(self, *, force: bool = False) -> str: ...


class HttpClient:
    """인증·재시도가 붙은 HTTP 클라이언트.

    Args:
        base_url: API 기본 주소.
        auth: 액세스 토큰 공급자. None이면 인증 헤더를 붙이지 않는다.
        max_retries: 재시도 가능한 응답에 대한 최대 재시도 횟수.
        transport: 테스트에서 갈아 끼울 httpx 전송 계층.
        sleep: 테스트에서 대기를 없애기 위한 주입점.
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth: TokenProvider | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        max_backoff: float = 30.0,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.auth = auth
        self.max_retries = max_retries
        self.max_backoff = max_backoff
        self._sleep = sleep
        self._client = httpx.Client(
            transport=transport,
            timeout=timeout,
            headers=default_headers or {},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """요청을 보내고 성공 응답을 돌려준다. 실패는 예외로 올린다."""
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        reauthed = False
        attempt = 0

        while True:
            headers = dict(kwargs.pop("headers", {}) or {})
            if self.auth is not None:
                headers.setdefault("Authorization", f"Bearer {self.auth.access_token()}")

            try:
                response = self._client.request(method, url, headers=headers, **kwargs)
            except httpx.HTTPError as exc:
                if attempt >= self.max_retries:
                    raise UpstreamError(f"요청이 실패했습니다: {exc}") from exc
                self._sleep(self._backoff(attempt))
                attempt += 1
                continue

            if response.status_code < 400:
                return response

            if response.status_code == 401 and self.auth is not None and not reauthed:
                # 토큰이 만료됐을 수 있다. 한 번만 강제 갱신하고 재시도한다.
                reauthed = True
                self.auth.access_token(force=True)
                continue

            if response.status_code == 401:
                raise AuthError(
                    "인증에 실패했습니다. 토큰이 취소되었거나 권한(scope)이 부족할 수 있습니다.",
                    details={"status": 401, "body": response.text[:500]},
                )

            if response.status_code == 429:
                retry_after = self._retry_after(response)
                if attempt >= self.max_retries:
                    raise RateLimited(
                        "호출 한도에 걸렸습니다. 잠시 후 다시 시도하세요.",
                        retry_after=retry_after,
                    )
                self._sleep(retry_after if retry_after is not None else self._backoff(attempt))
                attempt += 1
                continue

            if response.status_code >= 500:
                if attempt >= self.max_retries:
                    raise UpstreamError(
                        "상대 서버가 오류를 돌려주었습니다.",
                        status=response.status_code,
                        body=response.text,
                    )
                self._sleep(self._backoff(attempt))
                attempt += 1
                continue

            raise UpstreamError(
                "요청이 거부되었습니다.",
                status=response.status_code,
                body=response.text,
            )

    def get_json(self, path: str, **kwargs: Any) -> Any:
        return self._json(self.request("GET", path, **kwargs))

    def post_json(self, path: str, **kwargs: Any) -> Any:
        return self._json(self.request("POST", path, **kwargs))

    @staticmethod
    def _json(response: httpx.Response) -> Any:
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise UpstreamError(
                "응답이 JSON 형식이 아닙니다.",
                status=response.status_code,
                body=response.text,
            ) from exc

    @staticmethod
    def _retry_after(response: httpx.Response) -> float | None:
        raw = response.headers.get("Retry-After")
        if not raw:
            return None
        try:
            return max(0.0, float(raw))
        except ValueError:
            # HTTP-date 형식은 지원하지 않는다 — 백오프로 넘긴다.
            return None

    def _backoff(self, attempt: int) -> float:
        """지수 백오프 + 지터.

        지터가 없으면 여러 요청이 동시에 재시도해 같은 순간에 몰린다.
        """
        base = min(self.max_backoff, 2.0**attempt)
        return base * (0.5 + random.random() / 2)
