# 이 파일은 자동 생성된 복제본입니다 — 직접 수정하지 마세요.
# 정본: plugins/_shared/moai-mcp-core/cache.py
# 동기화: python3 scripts/sync-mcp-core.py
"""읽기 응답 TTL 캐시.

목적은 성능이 아니라 **할당량 절약**이다. YouTube Data API의 `search.list` 는 한 번에
100 units를 먹는데 기본 할당량이 하루 10,000 units라, 같은 검색을 두 번 하면 하루에
할 수 있는 일이 그만큼 줄어든다.

쓰기 작업은 절대 캐시하지 않는다.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any


class TTLCache:
    """수명이 있는 소형 LRU 캐시.

    Args:
        ttl_seconds: 항목 수명.
        max_entries: 최대 보관 개수. 넘으면 가장 오래 안 쓴 것부터 버린다.
        clock: 테스트에서 시간을 고정하기 위한 시각 함수.
    """

    def __init__(
        self,
        ttl_seconds: float = 300.0,
        *,
        max_entries: int = 256,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._clock = clock
        self._entries: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any | None:
        """살아 있는 값을 돌려준다. 없거나 만료됐으면 None."""
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        expires_at, value = entry
        if self._clock() >= expires_at:
            del self._entries[key]
            self.misses += 1
            return None
        self._entries.move_to_end(key)
        self.hits += 1
        return value

    def set(self, key: str, value: Any, *, ttl_seconds: float | None = None) -> None:
        ttl = self.ttl_seconds if ttl_seconds is None else ttl_seconds
        self._entries[key] = (self._clock() + ttl, value)
        self._entries.move_to_end(key)
        while len(self._entries) > self.max_entries:
            self._entries.popitem(last=False)

    def get_or_call(
        self,
        key: str,
        producer: Callable[[], Any],
        *,
        ttl_seconds: float | None = None,
    ) -> Any:
        """캐시에 있으면 그대로, 없으면 `producer()` 를 호출해 채운다."""
        cached = self.get(key)
        if cached is not None:
            return cached
        value = producer()
        self.set(key, value, ttl_seconds=ttl_seconds)
        return value

    def invalidate(self, key: str) -> None:
        self._entries.pop(key, None)

    def clear(self) -> None:
        self._entries.clear()

    def stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "entries": len(self._entries)}
