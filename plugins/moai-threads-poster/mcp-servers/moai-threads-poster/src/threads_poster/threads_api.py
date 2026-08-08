"""Threads(Meta) Graph API 클라이언트 — 순수 HTTP 래퍼, 네트워크 상태 없음.

2단계 발행 모델 (two-step publishing):
  1. :meth:`ThreadsClient.create_container` → 미디어 컨테이너 생성 (``POST /{user_id}/threads``)
  2. :meth:`ThreadsClient.publish`          → 컨테이너 발행       (``POST /{user_id}/threads_publish``)

모든 HTTP 호출은 주입 가능한 :class:`httpx.Client` 로 수행한다 (테스트에서 가짜 transport
주입). 기본 클라이언트는 생성자에서 lazily 만들어지며, non-2xx 응답은
:class:`ThreadsAPIError` 로 변환된다.

참고 (reference, verified from official docs):
  - Base URL: ``https://graph.threads.com/v1.0/``
  - 인증 (auth): OAuth 2.0 Bearer, ``access_token`` 쿼리/폼 파라미터
  - 권한 (permissions): ``threads_basic`` (전 엔드포인트), ``threads_content_publish`` (발행)
  - 레이트리밋 (rate limit): 24시간 250 포스트
  - 텍스트 제한: 500 (이모지·한글은 UTF-8 바이트 단위로 계산)
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

DEFAULT_BASE_URL = "https://graph.threads.com/v1.0"
DEFAULT_TIMEOUT = 30.0
# Threads 텍스트 예산: 500. 이모지·한글은 UTF-8 바이트 단위로 소비한다.
# Threads text budget: 500, counted as UTF-8 bytes (emoji/Korean consume multiple bytes).
TEXT_MAX_BYTES = 500

_VALID_MEDIA_TYPES = {"TEXT", "IMAGE", "VIDEO", "CAROUSEL"}


class ThreadsAPIError(RuntimeError):
    """Threads API 가 non-2xx 응답을 반환했을 때 발생 (raised on non-2xx response).

    응답 본문의 ``error`` 필드에서 ``message``/``type``/``code`` 를 파싱해 담는다.
    Threads 오류 형태::

        {"error": {"message": "...", "type": "OAuthException", "code": 190, "fbtrace_id": "..."}}
    """

    def __init__(self, status: int, body: Any):
        self.status = status
        self.body = body
        err = body.get("error") if isinstance(body, dict) else None
        err = err if isinstance(err, dict) else {}
        self.error_message: Optional[str] = err.get("message")
        self.error_type: Optional[str] = err.get("type")
        self.error_code: Optional[int] = err.get("code")
        msg = f"Threads API 오류 (HTTP {status})"
        if self.error_type:
            msg += f" [{self.error_type}"
            if self.error_code is not None:
                msg += f" {self.error_code}"
            msg += "]"
        if self.error_message:
            msg += f": {self.error_message}"
        super().__init__(msg)


class ThreadsClient:
    """Threads Graph API 클라이언트 (Threads Graph API client).

    Args:
        access_token: OAuth 2.0 액세스 토큰 (Bearer).
        threads_user_id: Threads 사용자 ID (컨테이너/발행 경로에 사용).
        base_url: Graph API 베이스 URL (기본값 ``https://graph.threads.com/v1.0``).
        client: 주입할 :class:`httpx.Client` (테스트용; 미지정 시 기본 클라이언트 생성).
            주입한 클라이언트는 호출자가 소유하며 :meth:`close` 로 닫지 않는다.
    """

    def __init__(
        self,
        access_token: str,
        threads_user_id: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        client: Optional[httpx.Client] = None,
    ):
        if not access_token:
            raise ValueError("access_token 이 필요합니다 (access_token is required)")
        if not threads_user_id:
            raise ValueError("threads_user_id 가 필요합니다 (threads_user_id is required)")
        self._access_token = access_token
        self._user_id = threads_user_id
        self._base_url = base_url.rstrip("/")
        if client is not None:
            self._http = client
            self._owns_client = False
        else:
            self._http = httpx.Client(timeout=DEFAULT_TIMEOUT)
            self._owns_client = True

    # ------------------------------------------------------------------ create
    def create_container(
        self,
        media_type: str,
        *,
        text: Optional[str] = None,
        image_url: Optional[str] = None,
        video_url: Optional[str] = None,
        is_carousel_item: bool = False,
    ) -> str:
        """미디어 컨테이너 생성 → container_id 반환 (create a media container).

        ``POST /{threads_user_id}/threads``

        검증 (validation):
          - ``media_type=TEXT``  → ``text`` 필수, 500 UTF-8 바이트 이하
          - ``media_type=IMAGE`` → ``image_url`` 필수 (공개 URL)
          - ``media_type=VIDEO`` → ``video_url`` 필수 (공개 URL)
          - ``media_type=CAROUSEL`` → 풀 캐러셀 플로우는 M2+, 단일 아이템은
            ``is_carousel_item=True`` 로 생성 가능

        Returns:
            container_id (``str``) — :meth:`publish` 의 ``creation_id`` 로 전달.
        """
        _validate_media_type(media_type)
        _validate_text_budget(text)
        if media_type == "TEXT" and not text:
            raise ValueError(
                "media_type=TEXT 에는 text 가 필요합니다 (text is required for TEXT posts)"
            )
        if media_type == "IMAGE" and not image_url:
            raise ValueError(
                "media_type=IMAGE 에는 image_url 이 필요합니다 "
                "(image_url is required for IMAGE posts)"
            )
        if media_type == "VIDEO" and not video_url:
            raise ValueError(
                "media_type=VIDEO 에는 video_url 이 필요합니다 "
                "(video_url is required for VIDEO posts)"
            )

        params: dict[str, Any] = {
            "media_type": media_type,
            "access_token": self._access_token,
        }
        if text is not None:
            params["text"] = text
        if image_url is not None:
            params["image_url"] = image_url
        if video_url is not None:
            params["video_url"] = video_url
        if is_carousel_item:
            params["is_carousel_item"] = "true"

        data = self._request("POST", f"/{self._user_id}/threads", params=params)
        if not isinstance(data, dict) or "id" not in data:
            raise ThreadsAPIError(
                200,
                {"error": {"message": "컨테이너 ID 가 응답에 없습니다 (no container id in response)", "type": "MalformedResponse"}},
            )
        return str(data["id"])

    # ------------------------------------------------------------------ publish
    def publish(self, creation_id: str) -> str:
        """컨테이너 발행 → media_id 반환 (publish the container).

        ``POST /{threads_user_id}/threads_publish?creation_id=...``
        권장: :meth:`create_container` 이후 평균 ~30초 대기 후 발행.
        """
        if not creation_id:
            raise ValueError("creation_id 가 필요합니다 (creation_id is required)")
        params = {"creation_id": creation_id, "access_token": self._access_token}
        data = self._request("POST", f"/{self._user_id}/threads_publish", params=params)
        if not isinstance(data, dict) or "id" not in data:
            raise ThreadsAPIError(
                200,
                {"error": {"message": "미디어 ID 가 응답에 없습니다 (no media id in response)", "type": "MalformedResponse"}},
            )
        return str(data["id"])

    # ------------------------------------------------------------------ refresh
    def refresh_token(self) -> str:
        """장기 토큰 갱신 → 새 access_token 반환 (refresh long-lived token).

        ``GET /refresh_access_token?grant_type=th_refresh_token&access_token=...``
        단기 토큰(1h) 은 먼저 장기 토큰(60일) 로 교환해야 한다. 본 메서드는
        이미 장기 토큰을 보유한 상태에서 갱신할 때 사용.
        """
        params = {"grant_type": "th_refresh_token", "access_token": self._access_token}
        data = self._request("GET", "/refresh_access_token", params=params)
        if not isinstance(data, dict) or "access_token" not in data:
            raise ThreadsAPIError(
                200,
                {"error": {"message": "갱신 응답에 access_token 이 없습니다 (no access_token in refresh response)", "type": "MalformedResponse"}},
            )
        return str(data["access_token"])

    # ------------------------------------------------------------------ profile
    def get_profile(self) -> dict[str, Any]:
        """프로필 조회 (health check / who-am-I).

        ``GET /{threads_user_id}?fields=username,id,followers_count,profile_picture_url``
        """
        params = {
            "fields": "username,id,followers_count,profile_picture_url",
            "access_token": self._access_token,
        }
        data = self._request("GET", f"/{self._user_id}", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    # ------------------------------------------------------------------ internal
    def _request(self, method: str, path: str, *, params: dict[str, Any]) -> Any:
        url = f"{self._base_url}{path}"
        resp = self._http.request(method, url, params=params)
        return self._parse(resp)

    def _parse(self, resp: httpx.Response) -> Any:
        body = _safe_json(resp)
        if resp.status_code >= 400:
            raise ThreadsAPIError(resp.status_code, body)
        return body

    def close(self) -> None:
        """기본 클라이언트를 직접 만든 경우에만 닫는다 (close owned client only)."""
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> "ThreadsClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


# ------------------------------------------------------------------ helpers
def _validate_media_type(media_type: str) -> None:
    if media_type not in _VALID_MEDIA_TYPES:
        raise ValueError(
            f"지원하지 않는 media_type 입니다 (unsupported media_type): {media_type!r}. "
            f"허용값 (allowed): TEXT, IMAGE, VIDEO, CAROUSEL"
        )


def _validate_text_budget(text: Optional[str]) -> None:
    """텍스트가 주어졌을 때 500 UTF-8 바이트 예산을 검사 (enforce 500-byte budget).

    이모지·한글은 멀티바이트로 계산된다 — 예산은 문자 수가 아닌 UTF-8 바이트 수다.
    """
    if text is None:
        return
    n = len(text.encode("utf-8"))
    if n > TEXT_MAX_BYTES:
        raise ValueError(
            f"텍스트가 {TEXT_MAX_BYTES} UTF-8 바이트 제한을 초과합니다 "
            f"(text exceeds the {TEXT_MAX_BYTES}-byte UTF-8 limit): 현재 (now) {n}바이트. "
            "이모지·한글은 바이트 단위로 계산됩니다 (emoji/Korean count as multi-byte)."
        )


def _safe_json(resp: httpx.Response) -> Any:
    """본문이 JSON 이면 파싱, 아니면 원문을 ``_raw`` 로 감싼다."""
    try:
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
    except Exception:
        pass
    return {"_raw": resp.text}
