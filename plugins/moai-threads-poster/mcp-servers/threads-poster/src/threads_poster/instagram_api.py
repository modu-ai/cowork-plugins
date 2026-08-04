"""Instagram Graph API 클라이언트 — Facebook Login for Business 호스트.

Threads 클라이언트(threads_api.py) 와 같은 2단계 발행 모델을 따르지만, 호스트·인증·
미디어 타입 규칙이 다르다 (Facebook Login for Business ≠ Threads OAuth2).

2단계 발행 모델 (two-step publishing):
  1. :meth:`InstagramClient.create_container` → 미디어 컨테이너 생성 (``POST /{ig_user_id}/media``)
  2. :meth:`InstagramClient.publish`          → 컨테이너 발행       (``POST /{ig_user_id}/media_publish``)

Threads 와의 주요 차이 (key differences vs Threads):
  - 호스트 (host): ``graph.facebook.com`` (Facebook Login for Business) — ``graph.threads.com`` 아님.
  - 이미지 (images): **JPEG-only**. Threads 와 달리 PNG 를 허용하지 않는다 (빠른 실패 휴리스틱).
  - 미디어 타입: ``IMAGE`` | ``VIDEO`` | ``REELS``. **TEXT-only 게시 없음** (캡션은 미디어에 붙음).
  - REELS: ``share_to_feed`` 플래그 지원.
  - VIDEO/REELS 발행: ``media_publish`` 전에 컨테이너 상태가 ``FINISHED`` 가 될 때까지 폴링 필수.
  - 스케줄링: **서버 측 스케줄링 파라미터가 없다** — 큐가 유일한 예약 경로 (REQ-INST-009).

모든 HTTP 호출은 주입 가능한 :class:`httpx.Client` 로 수행한다 (테스트에서 가짜 transport 주입).
non-2xx 응답은 :class:`InstagramAPIError` 로 변환된다 (``ThreadsAPIError`` 와 동일 필드 세트).

참고 (reference, verified against official Meta "Content Publishing" doc, 2026-06-30):
  - Base URL: ``https://graph.facebook.com/{GRAPH_API_VERSION}``
  - 인증 (auth): Facebook Page access token, ``access_token`` 쿼리/폼 파라미터
  - 계정 (account): Instagram Professional (Business or Creator) 만 지원. Personal 불가.
  - 레이트리밋 (rate limit): 24시간 100 포스트 (media_publish 는 50). ``content_publishing_limit`` 로 확인.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Optional

import httpx

# @MX:TODO: [AUTO] Graph API 버전 drift 게이트 — v23.0 은 2026-06-30 Meta 문서 기준 pin 값이다.
#   run-phase 이후 공식 문서를 재검증해야 한다 (acceptance.md §D.4). 버전이 바뀌면 이 상수 한 줄만
#   수정하면 된다 (centralized). 본 마커는 엔드포인트 경로 검증 부채가 아니라 *버전* 검증 부채다.
GRAPH_API_VERSION = "v23.0"
DEFAULT_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"
DEFAULT_TIMEOUT = 30.0
# 비디오/릴스 컨테이너 폴링 기본값 — 약 1분 간격, 최대 5분 (spec §E item 7).
DEFAULT_POLL_INTERVAL = 60.0
DEFAULT_POLL_TIMEOUT = 300.0

# Instagram 은 TEXT-only 게시가 없다 (캡션은 미디어에 붙음). CAROUSEL 은 범위 밖(spec §H).
_VALID_MEDIA_TYPES = {"IMAGE", "VIDEO", "REELS"}
# 컨테이너 상태값 (spec §E item 7). PUBLISHED 는 드물지만 폴링 루프에선 종단이 아님.
_TERMINAL_ERROR_STATUSES = {"EXPIRED", "ERROR"}


class InstagramAPIError(RuntimeError):
    """Instagram API 가 non-2xx 응답을 반환했을 때 발생 (raised on non-2xx response).

    응답 본문의 ``error`` 필드에서 ``message``/``type``/``code`` 를 파싱해 담는다.
    ``ThreadsAPIError`` 와 **동일한 필드 세트**(``status``/``body``/``error_message``/
    ``error_type``/``error_code``) 를 가져 MCP ``_error_dict`` 래퍼가 양쪽에 범용으로 동작한다.

    Instagram 오류 형태 (Threads 와 동일한 Meta 오류 봉투)::

        {"error": {"message": "...", "type": "OAuthException", "code": 10, "fbtrace_id": "..."}}
    """

    def __init__(self, status: int, body: Any):
        self.status = status
        self.body = body
        err = body.get("error") if isinstance(body, dict) else None
        err = err if isinstance(err, dict) else {}
        self.error_message: Optional[str] = err.get("message")
        self.error_type: Optional[str] = err.get("type")
        self.error_code: Optional[int] = err.get("code")
        msg = f"Instagram API 오류 (HTTP {status})"
        if self.error_type:
            msg += f" [{self.error_type}"
            if self.error_code is not None:
                msg += f" {self.error_code}"
            msg += "]"
        if self.error_message:
            msg += f": {self.error_message}"
        super().__init__(msg)


class InstagramClient:
    """Instagram Graph API 클라이언트 (Instagram Graph API client).

    Args:
        access_token: Facebook Page 액세스 토큰 (long-lived).
        ig_user_id: Instagram Professional 계정 ID (API 경로의 ``ig-user-id``).
        base_url: Graph API 베이스 URL (기본값 ``https://graph.facebook.com/{GRAPH_API_VERSION}``).
        client: 주입할 :class:`httpx.Client` (테스트용; 미지정 시 기본 클라이언트 생성).
            주입한 클라이언트는 호출자가 소유하며 :meth:`close` 로 닫지 않는다.
    """

    def __init__(
        self,
        access_token: str,
        ig_user_id: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        client: Optional[httpx.Client] = None,
    ):
        if not access_token:
            raise ValueError("access_token 이 필요합니다 (access_token is required)")
        if not ig_user_id:
            raise ValueError("ig_user_id 가 필요합니다 (ig_user_id is required)")
        self._access_token = access_token
        self._ig_user_id = ig_user_id
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
        share_to_feed: Optional[bool] = None,
    ) -> str:
        """미디어 컨테이너 생성 → container_id(creation_id) 반환 (create a media container).

        ``POST /{ig_user_id}/media``

        검증 (validation):
          - ``media_type=IMAGE`` → ``image_url`` 필수 (공개 URL, JPEG 권장 — PNG 는 빠른 실패)
          - ``media_type=VIDEO`` → ``video_url`` 필수 (공개 URL)
          - ``media_type=REELS`` → ``video_url`` 필수 (공개 URL) + ``share_to_feed`` 선택
          - ``TEXT`` 지원 안 함 (Instagram 은 텍스트 전용 게시가 없다)

        Args:
            media_type: ``IMAGE`` | ``VIDEO`` | ``REELS``.
            text: 캡션(선택).
            image_url: 공개 이미지 URL (IMAGE 필수). JPEG 권장 — ``.png`` 접미면 빠르게 실패.
            video_url: 공개 비디오 URL (VIDEO/REELS 필수).
            share_to_feed: REELS 를 피드에도 공유할지 (선택, REELS 전용).

        Returns:
            creation_id (``str``) — :meth:`publish` 의 ``creation_id`` 로 전달.
            VIDEO/REELS 의 경우 :meth:`wait_until_finished` 로 ``FINISHED`` 를 기다린 뒤 발행.
        """
        _validate_media_type(media_type)
        if media_type == "IMAGE":
            if not image_url:
                raise ValueError(
                    "media_type=IMAGE 에는 image_url 이 필요합니다 "
                    "(image_url is required for IMAGE posts)"
                )
            _validate_image_jpeg(image_url)
        elif media_type == "VIDEO":
            if not video_url:
                raise ValueError(
                    "media_type=VIDEO 에는 video_url 이 필요합니다 "
                    "(video_url is required for VIDEO posts)"
                )
        elif media_type == "REELS":
            if not video_url:
                raise ValueError(
                    "media_type=REELS 에는 video_url 이 필요합니다 "
                    "(video_url is required for REELS posts)"
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
        if share_to_feed is not None:
            params["share_to_feed"] = "true" if share_to_feed else "false"

        data = self._request("POST", f"/{self._ig_user_id}/media", params=params)
        if not isinstance(data, dict) or "id" not in data:
            raise InstagramAPIError(
                200,
                {"error": {"message": "컨테이너 ID 가 응답에 없습니다 (no container id in response)", "type": "MalformedResponse"}},
            )
        return str(data["id"])

    # ------------------------------------------------------------------ publish
    def publish(self, creation_id: str) -> str:
        """컨테이너 발행 → media_id 반환 (publish the container).

        ``POST /{ig_user_id}/media_publish?creation_id=...``

        VIDEO/REELS 의 경우 먼저 :meth:`wait_until_finished` 로 컨테이너 상태가
        ``FINISHED`` 인지 확인한 뒤 호출할 것 (spec §E item 7).
        """
        if not creation_id:
            raise ValueError("creation_id 가 필요합니다 (creation_id is required)")
        params = {"creation_id": creation_id, "access_token": self._access_token}
        data = self._request("POST", f"/{self._ig_user_id}/media_publish", params=params)
        if not isinstance(data, dict) or "id" not in data:
            raise InstagramAPIError(
                200,
                {"error": {"message": "미디어 ID 가 응답에 없습니다 (no media id in response)", "type": "MalformedResponse"}},
            )
        return str(data["id"])

    # ------------------------------------------------------------------ container status
    def get_container_status(self, creation_id: str) -> str:
        """컨테이너 처리 상태 조회 (fetch container processing status).

        ``GET /{creation_id}?fields=status_code&access_token=...``

        Returns:
            상태 문자열 ∈ {``EXPIRED``, ``ERROR``, ``FINISHED``, ``IN_PROGRESS``, ``PUBLISHED``}.
        """
        if not creation_id:
            raise ValueError("creation_id 가 필요합니다 (creation_id is required)")
        params = {"fields": "status_code", "access_token": self._access_token}
        data = self._request("GET", f"/{creation_id}", params=params)
        if isinstance(data, dict) and "status_code" in data:
            return str(data["status_code"])
        raise InstagramAPIError(
            200,
            {"error": {"message": "status_code 가 응답에 없습니다 (no status_code in response)", "type": "MalformedResponse"}},
        )

    def wait_until_finished(
        self,
        creation_id: str,
        *,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
        timeout: float = DEFAULT_POLL_TIMEOUT,
        sleeper: Callable[..., None] = time.sleep,
    ) -> str:
        """컨테이너가 ``FINISHED`` 가 될 때까지 폴링 (poll until the container is FINISHED).

        ``GET /{creation_id}?fields=status_code`` 를 약 ``poll_interval`` 초 간격(기본 60초)으로
        ``timeout`` 초(기본 300초 = 5분) 한도 내에서 반복 호출한다.

        동작 (behavior):
          - ``FINISHED`` → 반환.
          - ``EXPIRED`` / ``ERROR`` → :class:`InstagramAPIError` 발생.
          - ``IN_PROGRESS`` / 그 외 → 계속 폴링.
          - 예산(timeout) 소진 → :class:`InstagramAPIError` 발생.

        Args:
            creation_id: 폴링할 컨테이너 ID.
            poll_interval: 폴링 간격(초). 기본 60.
            timeout: 최대 대기 시간(초). 기본 300 (spec §E item 7 의 ≤5분).
            sleeper: sleep callable (테스트에서 가짜 sleeper 주입용). 기본 ``time.sleep``.

        Returns:
            ``"FINISHED"``.
        """
        deadline = time.monotonic() + timeout
        while True:
            status = self.get_container_status(creation_id)
            if status == "FINISHED":
                return status
            if status in _TERMINAL_ERROR_STATUSES:
                raise InstagramAPIError(
                    200,
                    {
                        "error": {
                            "message": (
                                f"컨테이너 {status} (container {status}): {creation_id}"
                            ),
                            "type": f"Container{status.title()}",
                        }
                    },
                )
            # IN_PROGRESS / PUBLISHED / 알 수 없음 → 계속 폴링
            if time.monotonic() >= deadline:
                raise InstagramAPIError(
                    200,
                    {
                        "error": {
                            "message": (
                                f"폴링 타임아웃 (polling timeout, {timeout}s 초과): "
                                f"{creation_id}"
                            ),
                            "type": "PollingTimeout",
                        }
                    },
                )
            sleeper(poll_interval)

    # ------------------------------------------------------------------ profile
    def get_profile(self) -> dict[str, Any]:
        """프로필 조회 (health check / who-am-I).

        ``GET /{ig_user_id}?fields=username,id,followers_count,media_count``
        """
        # @MX:TODO: [AUTO] get_profile fields 는 run-phase 에서 현행 Meta 문서로 재검증 필요
        #   (acceptance.md §D.4). username/id/followers_count/media_count 는 표준 필드지만
        #   권한·가용성이 바뀔 수 있다.
        params = {
            "fields": "username,id,followers_count,media_count",
            "access_token": self._access_token,
        }
        data = self._request("GET", f"/{self._ig_user_id}", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    # ------------------------------------------------------------------ token refresh
    def refresh_token(self) -> str:
        """장기 Page 토큰 갱신 → 새 access_token 반환 (refresh long-lived Page token).

        Facebook Page 장기 토큰 갱신 흐름. 정확한 엔드포인트는 run-phase 검증 대상이다.
        """
        # @MX:TODO: [AUTO] Facebook Page 장기 토큰 갱신 엔드포인트/파라미터는 run-phase 검증 필요
        #   (acceptance.md §D.4). Threads 의 th_refresh_token 흐름과 다르다. 본 구현은 반환 파싱만
        #   보장하고, 정확한 경로는 현행 Meta 문서로 확정 전이다.
        params = {"grant_type": "fb_exchange_token", "access_token": self._access_token}
        data = self._request("GET", "/refresh_access_token", params=params)
        if not isinstance(data, dict) or "access_token" not in data:
            raise InstagramAPIError(
                200,
                {"error": {"message": "갱신 응답에 access_token 이 없습니다 (no access_token in refresh response)", "type": "MalformedResponse"}},
            )
        return str(data["access_token"])

    # ------------------------------------------------------------------ publish limit
    def get_publish_limit(self) -> dict[str, Any]:
        """24시간 발행 한도 잔여량 조회 (fetch 24h content publishing quota).

        ``GET /{ig_user_id}/content_publishing_limit?access_token=...``

        Returns:
            Meta 가 돌려주는 quota 봉투 (``data[0].quota_usage`` / ``config.quota_total`` 등).
            원본을 그대로 반환 — runner 가 ``data[0]`` 를 해석한다.
        """
        params = {"access_token": self._access_token}
        data = self._request("GET", f"/{self._ig_user_id}/content_publishing_limit", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    # ------------------------------------------------------------------ comments (permission: manage_comments)
    def comments_list(self, media_id: str) -> dict[str, Any]:
        """미디어의 댓글 목록 조회 (list comments on a media object).

        ``manage_comments`` 권한 필요 (REQ-INST-018). 엔드포인트 경로는 run-phase 검증 대상.
        """
        # @MX:TODO: [AUTO] comments 엔드포인트 경로(/{media-id}/comments 등) 는 run-phase 에서 현행
        #   Meta "Instagram Graph API Reference" 로 검증 필요 (acceptance.md §D.4, spec REQ-INST-018).
        #   권한 게이트(manage_comments) 가 부여된 경우에만 호출되며, 경로가 확정되면 본 마커를 지운다.
        if not media_id:
            raise ValueError("media_id 가 필요합니다 (media_id is required)")
        params = {"access_token": self._access_token}
        data = self._request("GET", f"/{media_id}/comments", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    def comments_reply(self, comment_id: str, text: str) -> dict[str, Any]:
        """댓글에 답글 작성 (reply to a comment).

        ``manage_comments`` 권한 필요 (REQ-INST-018). 엔드포인트 경로는 run-phase 검증 대상.
        """
        # @MX:TODO: [AUTO] comments_reply 엔드포인트/파라미터 검증 필요 (run-phase, acceptance.md §D.4).
        if not comment_id:
            raise ValueError("comment_id 가 필요합니다 (comment_id is required)")
        if not text:
            raise ValueError("text 가 필요합니다 (text is required)")
        params = {"message": text, "access_token": self._access_token}
        data = self._request("POST", f"/{comment_id}/replies", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    def comments_hide(self, comment_id: str) -> dict[str, Any]:
        """댓글 숨김 토글 (hide a comment).

        ``manage_comments`` 권한 필요 (REQ-INST-018). 엔드포인트 경로는 run-phase 검증 대상.
        """
        # @MX:TODO: [AUTO] comments_hide 엔드포인트/파라미터 검증 필요 (run-phase, acceptance.md §D.4).
        if not comment_id:
            raise ValueError("comment_id 가 필요합니다 (comment_id is required)")
        params = {"hidden": "true", "access_token": self._access_token}
        data = self._request("POST", f"/{comment_id}", params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    # ------------------------------------------------------------------ insights (permission: manage_insights)
    def insights(
        self,
        metric: str = "reach,impressions",
        period: str = "day",
        *,
        media_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """인사이트 조회 (fetch account-level or media-level insights).

        ``manage_insights`` 권한 필요 (REQ-INST-019). ``media_id`` 미지정 시 계정 수준,
        지정 시 해당 미디어 수준 인사이트. 엔드포인트/파라미터는 run-phase 검증 대상.
        """
        # @MX:TODO: [AUTO] insights 엔드포인트/파라미터(metric/period) 는 run-phase 에서 현행 Meta
        #   문서로 검증 필요 (acceptance.md §D.4, spec REQ-INST-019). 권한 게이트(manage_insights)
        #   가 부여된 경우에만 호출된다.
        params: dict[str, Any] = {
            "metric": metric,
            "period": period,
            "access_token": self._access_token,
        }
        path = f"/{media_id}/insights" if media_id else f"/{self._ig_user_id}/insights"
        data = self._request("GET", path, params=params)
        return data if isinstance(data, dict) else {"_raw": data}

    # ------------------------------------------------------------------ internal
    def _request(self, method: str, path: str, *, params: dict[str, Any]) -> Any:
        url = f"{self._base_url}{path}"
        resp = self._http.request(method, url, params=params)
        return self._parse(resp)

    def _parse(self, resp: httpx.Response) -> Any:
        body = _safe_json(resp)
        if resp.status_code >= 400:
            raise InstagramAPIError(resp.status_code, body)
        return body

    def close(self) -> None:
        """기본 클라이언트를 직접 만든 경우에만 닫는다 (close owned client only)."""
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> "InstagramClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


# ------------------------------------------------------------------ helpers
def _validate_media_type(media_type: str) -> None:
    if media_type not in _VALID_MEDIA_TYPES:
        raise ValueError(
            f"지원하지 않는 media_type 입니다 (unsupported media_type): {media_type!r}. "
            f"허용값 (allowed): IMAGE, VIDEO, REELS"
        )


def _validate_image_jpeg(image_url: str) -> None:
    """IMAGE URL 의 JPEG-only 휴리스틱 빠른 실패 (fast-fail JPEG-only heuristic).

    Instagram 은 Threads 와 달리 PNG 를 허용하지 않는다 (spec §E item 3). URL 접미사로
    빠르게 실패시킨다 — 이것은 *휴리스틱*이며 최종 권위는 API 의다. 쿼리스트링은 무시하고
    경로의 확장자만 본다.
    """
    path = image_url.lower().split("?", 1)[0]
    if path.endswith(".png"):
        raise ValueError(
            "Instagram 은 PNG 를 지원하지 않습니다 — JPEG 만 허용됩니다 "
            "(Instagram is JPEG-only; PNG is not supported). "
            "이미지를 JPEG 로 변환 후 다시 시도하세요."
        )


def _safe_json(resp: httpx.Response) -> Any:
    """본문이 JSON 이면 파싱, 아니면 원문을 ``_raw`` 로 감싼다."""
    try:
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
    except Exception:
        pass
    return {"_raw": resp.text}
