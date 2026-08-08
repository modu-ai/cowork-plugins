"""YouTube Data API 할당량 회계.

기본 할당량은 하루 10,000 units다. 단가가 균일하지 않은 것이 함정이다.

- `videos.list` · `playlistItems.list` = **1 unit**
- `search.list` = **100 units** → 하루 100회면 끝
- `videos.insert`(업로드) = 약 100 units (2025-12-04 개정 전에는 약 1,600)

즉 지금 할당량을 가장 빨리 태우는 것은 업로드가 아니라 **검색**이다. 그래서
`search` 는 캐시를 강제하고, 채널 자기 영상 목록은 `search` 대신
`playlistItems.list`(업로드 재생목록)로 받는다.

이 모듈은 소모량을 기록해 사용자가 잔량을 인지하게 하고, 임계를 넘으면
호출 전에 막는다. 할당량 재설정은 태평양 시간 자정이라 날짜 경계는 근사치다 —
정확한 잔량은 Google Cloud 콘솔이 정본이고, 여기 값은 방어용 추정이다.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

DEFAULT_DAILY_LIMIT = 10_000

#: 엔드포인트별 단가. 키는 `리소스.동작` 형식.
COST: dict[str, int] = {
    # 조회 — 대부분 1
    "videos.list": 1,
    "channels.list": 1,
    "playlists.list": 1,
    "playlistItems.list": 1,
    "commentThreads.list": 1,
    "liveBroadcasts.list": 1,
    "liveStreams.list": 1,
    "liveChatMessages.list": 1,
    # 검색 — 압도적으로 비싸다
    "search.list": 100,
    # 쓰기
    "videos.insert": 100,
    "videos.update": 50,
    "playlists.insert": 50,
    "playlistItems.insert": 50,
    "playlistItems.update": 50,
    "thumbnails.set": 50,
    "comments.insert": 50,
    "comments.setModerationStatus": 50,
    "liveBroadcasts.insert": 50,
    "liveBroadcasts.bind": 50,
    "liveBroadcasts.transition": 50,
    "liveChatMessages.insert": 50,
    # 자막
    "captions.list": 50,
    "captions.insert": 400,
}

#: Analytics API 는 Data API 할당량을 쓰지 않는다.
FREE_OPERATIONS = {"analytics.query"}


def cost_of(operation: str) -> int:
    """엔드포인트 단가. 모르는 엔드포인트는 보수적으로 1로 본다."""
    if operation in FREE_OPERATIONS:
        return 0
    return COST.get(operation, 1)


class QuotaLedger:
    """하루 소모량을 파일에 누적한다.

    Args:
        path: 원장 파일 경로. 없으면 `~/.moai/mcp/youtube-quota.json`.
        daily_limit: 일일 한도.
        warn_ratio: 이 비율을 넘으면 응답에 경고를 붙인다.
        clock: 테스트용 시각 함수.
    """

    def __init__(
        self,
        *,
        path: Path | None = None,
        daily_limit: int = DEFAULT_DAILY_LIMIT,
        warn_ratio: float = 0.8,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.path = path or (Path.home() / ".moai" / "mcp" / "youtube-quota.json")
        self.daily_limit = daily_limit
        self.warn_ratio = warn_ratio
        self._clock = clock
        self._day: str = ""
        self._used: int = 0
        self._persistent = True
        self._load()

    @property
    def used(self) -> int:
        self._roll_over_if_new_day()
        return self._used

    @property
    def remaining(self) -> int:
        return max(0, self.daily_limit - self.used)

    def would_exceed(self, operation: str) -> bool:
        """이 호출을 하면 한도를 넘는가."""
        return self.used + cost_of(operation) > self.daily_limit

    def should_warn(self) -> bool:
        return self.used >= self.daily_limit * self.warn_ratio

    def charge(self, operation: str) -> int:
        """소모량을 기록하고 이번 호출의 단가를 돌려준다."""
        amount = cost_of(operation)
        if amount == 0:
            return 0
        self._roll_over_if_new_day()
        self._used += amount
        self._save()
        return amount

    def snapshot(self) -> dict[str, Any]:
        """도구 응답에 붙일 잔량 정보."""
        return {
            "used": self.used,
            "remaining": self.remaining,
            "daily_limit": self.daily_limit,
            "warning": self.should_warn(),
            "note": "추정치입니다. 정확한 잔량은 Google Cloud 콘솔이 정본입니다.",
        }

    # --- 내부 -------------------------------------------------------------

    def _today(self) -> str:
        # 태평양 시간 자정 재설정을 근사한다. 정밀한 시간대 변환은 하지 않는다 —
        # 이 값은 방어용 추정이지 과금 기준이 아니다.
        return time.strftime("%Y-%m-%d", time.gmtime(self._clock() - 8 * 3600))

    def _roll_over_if_new_day(self) -> None:
        today = self._today()
        if self._day != today:
            self._day = today
            self._used = 0

    def _load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self._day = self._today()
            self._used = 0
            return
        if not isinstance(data, dict):
            data = {}
        self._day = str(data.get("day") or self._today())
        try:
            self._used = int(data.get("used") or 0)
        except (TypeError, ValueError):
            self._used = 0
        self._roll_over_if_new_day()

    def _save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps({"day": self._day, "used": self._used}, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError:
            # 기록 실패가 도구 실패가 되면 안 된다. 이번 프로세스 동안만 메모리로 센다.
            self._persistent = False
