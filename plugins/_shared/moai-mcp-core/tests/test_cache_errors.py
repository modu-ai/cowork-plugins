"""TTLCache 와 오류 매핑."""

from __future__ import annotations

from moai_mcp_core.cache import TTLCache
from moai_mcp_core.errors import (
    QuotaExhausted,
    RateLimited,
    SetupRequired,
    UpstreamError,
    to_tool_result,
)


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def test_캐시_적중과_실패():
    cache = TTLCache(ttl_seconds=10, clock=_Clock())
    assert cache.get("k") is None
    cache.set("k", {"v": 1})
    assert cache.get("k") == {"v": 1}
    assert cache.stats() == {"hits": 1, "misses": 1, "entries": 1}


def test_수명이_지나면_버린다():
    clock = _Clock()
    cache = TTLCache(ttl_seconds=10, clock=clock)
    cache.set("k", "v")

    clock.now = 9.9
    assert cache.get("k") == "v"
    clock.now = 10.0
    assert cache.get("k") is None


def test_get_or_call_은_한_번만_호출한다():
    """할당량 절약의 핵심 — 같은 검색을 두 번 하지 않는다."""
    calls = {"n": 0}

    def producer():
        calls["n"] += 1
        return "결과"

    cache = TTLCache(ttl_seconds=60, clock=_Clock())
    assert cache.get_or_call("검색:고양이", producer) == "결과"
    assert cache.get_or_call("검색:고양이", producer) == "결과"
    assert calls["n"] == 1


def test_최대_개수를_넘으면_오래된_것부터_버린다():
    cache = TTLCache(ttl_seconds=100, max_entries=2, clock=_Clock())
    cache.set("a", 1)
    cache.set("b", 2)
    cache.get("a")  # a 를 최근 사용으로 올린다
    cache.set("c", 3)

    assert cache.get("b") is None  # 가장 오래 안 쓴 b 가 밀려났다
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_무효화와_비우기():
    cache = TTLCache(clock=_Clock())
    cache.set("a", 1)
    cache.invalidate("a")
    assert cache.get("a") is None

    cache.set("b", 2)
    cache.clear()
    assert cache.get("b") is None


def test_setup_required_는_실패가_아니라_안내다():
    result = to_tool_result(
        SetupRequired("연동이 필요합니다.", missing=["YOUTUBE_CLIENT_ID"], guide="README.md")
    )
    assert result["ok"] is False
    assert result["error"] == "setup_required"
    assert result["details"]["missing_env"] == ["YOUTUBE_CLIENT_ID"]


def test_5xx_는_재시도_가능_4xx_는_불가():
    assert to_tool_result(UpstreamError("서버 오류", status=502))["retryable"] is True
    assert to_tool_result(UpstreamError("잘못된 요청", status=400))["retryable"] is False


def test_rate_limited_는_대기_시간을_알려준다():
    result = to_tool_result(RateLimited("한도 초과", retry_after=30))
    assert result["details"]["retry_after_seconds"] == 30
    assert result["retryable"] is True


def test_할당량_소진은_재시도해도_소용없다():
    assert to_tool_result(QuotaExhausted("오늘 할당량을 다 썼습니다."))["retryable"] is False


def test_예상하지_못한_예외도_삼켜서_구조화한다():
    """서버가 죽는 것이 가장 나쁜 결과다."""
    result = to_tool_result(ValueError("어딘가 터짐"))
    assert result["error"] == "internal_error"
    assert "ValueError" in result["message"]
