"""YouTube API 클라이언트.

`moai_mcp_core.HttpClient` 위에 유튜브 고유의 두 가지를 얹는다.

1. **할당량 회계** — 호출 전에 한도를 확인하고, 호출 후 소모량을 기록한다.
2. **검색 캐시** — `search.list` 는 1회 100 units라 같은 검색을 두 번 하면 그만큼
   그날 할 수 있는 일이 줄어든다.

인증·재시도·401 재인증은 코어가 처리하므로 여기에 없다.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from moai_mcp_core import HttpClient, QuotaExhausted, TTLCache, UpstreamError

from .config import YouTubeConfig, build_refresher
from .quota import QuotaLedger


class YouTubeClient:
    """유튜브 3개 API(Data · Live · Analytics)를 한 클라이언트로 다룬다."""

    def __init__(
        self,
        config: YouTubeConfig,
        *,
        transport: httpx.BaseTransport | None = None,
        ledger: QuotaLedger | None = None,
        cache: TTLCache | None = None,
        sleep=None,
    ) -> None:
        self.config = config
        self.ledger = ledger or QuotaLedger(
            path=config.quota_file, daily_limit=config.daily_limit
        )
        self.cache = cache or TTLCache(ttl_seconds=config.search_cache_ttl)
        self._refresher = build_refresher(config, transport=transport)

        http_kwargs: dict[str, Any] = {"auth": self._refresher, "transport": transport}
        if sleep is not None:
            http_kwargs["sleep"] = sleep
        self._http = HttpClient(config.api_base, **http_kwargs)

    def close(self) -> None:
        self._http.close()

    # --- Data API ---------------------------------------------------------

    def call(
        self,
        operation: str,
        method: str,
        path: str,
        *,
        base: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """할당량을 확인·기록하며 API를 호출한다.

        Args:
            operation: 단가표의 키 (`videos.list` 등).
            base: 기본 API 주소를 벗어날 때 (업로드·분석).
        """
        self.config.require()

        if self.ledger.would_exceed(operation):
            raise QuotaExhausted(
                "오늘 사용할 수 있는 유튜브 API 할당량을 모두 썼습니다. "
                "태평양 시간 자정에 재설정됩니다.",
                details=self.ledger.snapshot(),
            )

        url = path if path.startswith("http") else f"{(base or self.config.api_base)}/{path.lstrip('/')}"
        response = self._http.request(method, url, **kwargs)
        self.ledger.charge(operation)

        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise UpstreamError(
                "유튜브 응답이 JSON 형식이 아닙니다.",
                status=response.status_code,
                body=response.text,
            ) from exc

    def get(self, operation: str, path: str, params: dict[str, Any], **kw: Any) -> Any:
        return self.call(operation, "GET", path, params=_clean(params), **kw)

    def post(
        self,
        operation: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        **kw: Any,
    ) -> Any:
        return self.call(
            operation, "POST", path, params=_clean(params or {}), json=body, **kw
        )

    def put(
        self,
        operation: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        **kw: Any,
    ) -> Any:
        return self.call(
            operation, "PUT", path, params=_clean(params or {}), json=body, **kw
        )

    # --- 검색 (캐시 강제) --------------------------------------------------

    def search(self, params: dict[str, Any]) -> Any:
        """`search.list` 호출. 같은 조건은 캐시에서 돌려준다.

        캐시가 목적이 성능이 아니라 할당량 절약이므로, 캐시 적중 시에는 소모량을
        기록하지 않는다.
        """
        cleaned = _clean(params)
        key = "search:" + json.dumps(cleaned, sort_keys=True, ensure_ascii=False)
        cached = self.cache.get(key)
        if cached is not None:
            return cached
        result = self.get("search.list", "search", cleaned)
        self.cache.set(key, result)
        return result

    # --- 채널 자기 영상 (search 회피) --------------------------------------

    def uploads_playlist_id(self, channel_id: str | None = None) -> str:
        """업로드 재생목록 ID.

        내 채널의 영상 목록은 `search`(100 units) 가 아니라 이 재생목록을 통해
        `playlistItems.list`(1 unit) 로 받는다. 100배 차이다.
        """
        params: dict[str, Any] = {"part": "contentDetails"}
        target = channel_id or self.config.channel_id
        if target:
            params["id"] = target
        else:
            params["mine"] = "true"

        data = self.get("channels.list", "channels", params) or {}
        items = data.get("items") or []
        if not items:
            raise UpstreamError("채널을 찾을 수 없습니다.", status=404)
        related = items[0].get("contentDetails", {}).get("relatedPlaylists", {})
        uploads = related.get("uploads")
        if not uploads:
            raise UpstreamError("업로드 재생목록을 찾을 수 없습니다.", status=404)
        return str(uploads)

    # --- 파일 업로드 (resumable) -------------------------------------------

    def resumable_upload(
        self,
        operation: str,
        path: str,
        *,
        file_path: str,
        metadata: dict[str, Any],
        params: dict[str, Any] | None = None,
        content_type: str = "application/octet-stream",
    ) -> Any:
        """재개 가능 업로드로 파일을 올린다.

        영상 파일은 크다. 한 번의 요청으로 통째로 보내면 중간에 끊겼을 때 처음부터
        다시 해야 하므로, 유튜브가 권장하는 2단계 방식을 쓴다.

        1. 메타데이터를 보내 업로드 세션 URL(`Location` 헤더)을 받는다
        2. 그 URL로 파일 본문을 올린다
        """
        self.config.require()

        source = Path(file_path).expanduser()
        if not source.is_file():
            raise UpstreamError(f"파일을 찾을 수 없습니다: {source}", status=400)
        size = source.stat().st_size

        if self.ledger.would_exceed(operation):
            raise QuotaExhausted(
                "오늘 사용할 수 있는 유튜브 API 할당량을 모두 썼습니다.",
                details=self.ledger.snapshot(),
            )

        query = _clean({**(params or {}), "uploadType": "resumable"})
        init = self._http.request(
            "POST",
            f"{self.config.upload_base}/{path.lstrip('/')}",
            params=query,
            json=metadata,
            headers={
                "X-Upload-Content-Length": str(size),
                "X-Upload-Content-Type": content_type,
            },
        )
        session_url = init.headers.get("Location")
        if not session_url:
            raise UpstreamError(
                "업로드 세션을 열지 못했습니다. 응답에 Location 헤더가 없습니다.",
                status=init.status_code,
                body=init.text,
            )

        with source.open("rb") as handle:
            uploaded = self._http.request(
                "PUT",
                session_url,
                content=handle.read(),
                headers={"Content-Type": content_type, "Content-Length": str(size)},
            )

        self.ledger.charge(operation)
        if not uploaded.content:
            return None
        try:
            return uploaded.json()
        except ValueError as exc:
            raise UpstreamError(
                "업로드 응답이 JSON 형식이 아닙니다.",
                status=uploaded.status_code,
                body=uploaded.text,
            ) from exc

    def media_upload(
        self,
        operation: str,
        path: str,
        *,
        file_path: str,
        params: dict[str, Any] | None = None,
        content_type: str = "application/octet-stream",
    ) -> Any:
        """작은 파일(썸네일 등)을 한 번의 요청으로 올린다."""
        self.config.require()

        source = Path(file_path).expanduser()
        if not source.is_file():
            raise UpstreamError(f"파일을 찾을 수 없습니다: {source}", status=400)

        if self.ledger.would_exceed(operation):
            raise QuotaExhausted(
                "오늘 사용할 수 있는 유튜브 API 할당량을 모두 썼습니다.",
                details=self.ledger.snapshot(),
            )

        query = _clean({**(params or {}), "uploadType": "media"})
        response = self._http.request(
            "POST",
            f"{self.config.upload_base}/{path.lstrip('/')}",
            params=query,
            content=source.read_bytes(),
            headers={"Content-Type": content_type},
        )
        self.ledger.charge(operation)
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise UpstreamError(
                "업로드 응답이 JSON 형식이 아닙니다.",
                status=response.status_code,
                body=response.text,
            ) from exc

    def quota(self) -> dict[str, Any]:
        return self.ledger.snapshot()


def _clean(params: dict[str, Any]) -> dict[str, Any]:
    """None 값을 걸러낸다 — 유튜브 API는 빈 파라미터를 오류로 본다."""
    return {k: v for k, v in params.items() if v is not None}
