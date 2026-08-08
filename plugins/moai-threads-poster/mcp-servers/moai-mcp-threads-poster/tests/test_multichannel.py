"""멀티 채널 포맷터 단위 테스트 — threads_format_multi_channel + _split_for_x_thread.

검증 (coverage):
  (a) ``_split_for_x_thread`` 순수 헬퍼 — 경계 케이스
      - 600자 → ≥3 트윗, 각 ≤280, 번호 ``N/ ``
      - 정확히 한 트윗에 들어가는 분량(≤ budget) → 1 트윗
      - 단일 예산 초과 → 2+ 트윗
      - 단어 중간 cut 금지 (재조립 시 원본 단어 열과 동일)
      - 빈 입력 → 빈 리스트
      - 단일 단어가 예산 초과 → 글자 단위 강제 분할 (각 조각 ≤ budget)
      - 커스텀 counter 주입 존중 (바이트 카운터)
  (b) ``threads_format_multi_channel`` 도구
      - free tier: 600자 → ≥3 트윗, 각 ≤280
      - premium tier: 단일 문자열
      - threads 출력 ≤500 바이트 (한글 문자열로 바이트 계산 exercise)
      - facebook 출력은 문자열
      - 잘못된 x_tier → error dict
      - 빈 text 처리
      - 기본 channels 3종 / 커스텀 channels 부분집합
"""

from __future__ import annotations

import re

import pytest

from moai_mcp_threads_poster.server import (
    _split_for_x_thread,
    threads_format_multi_channel,
)

# X 무료 tier 트윗당 글자 수 상한 (접두 포함).
X_FREE_LIMIT = 280


# === (a) _split_for_x_thread — pure helper ======================================

def test_split_empty_returns_empty_list():
    assert _split_for_x_thread("") == []
    assert _split_for_x_thread("   \n  \t ") == []


def test_split_short_text_fits_in_one_tweet():
    out = _split_for_x_thread("Hello, world!", limit=X_FREE_LIMIT)
    assert len(out) == 1
    assert out[0] == "1/ Hello, world!"
    assert len(out[0]) <= X_FREE_LIMIT


def test_split_600_chars_yields_at_least_3_tweets_each_under_280():
    # 트윗당 내용 예산 = 280 - len("N/ ") ≈ 277자. ≥3 트윗이 되려면 내용이
    # 2×277 = 554자 를 초과해야 한다. "word" 130개 = 649자 → 3 트윗.
    text = " ".join(["word"] * 130)
    assert len(text) > 554  # ≥3 트윗을 보장하는 분량
    out = _split_for_x_thread(text, limit=X_FREE_LIMIT)
    assert len(out) >= 3
    for tweet in out:
        assert len(tweet) <= X_FREE_LIMIT
    # 모두 번호 접두로 시작
    for tweet in out:
        assert re.match(r"^\d+/\s", tweet)


def test_split_numbering_is_sequential():
    text = " ".join(["word"] * 110)
    out = _split_for_x_thread(text, limit=X_FREE_LIMIT)
    # 접두 번호가 1, 2, 3, ... 순서여야 한다.
    nums = [int(re.match(r"^(\d+)/\s", t).group(1)) for t in out]
    assert nums == list(range(1, len(out) + 1))


def test_split_never_cuts_mid_word():
    # 분할 후 각 트윗의 내용(접두 제외) 단어 열을 합치면 원본 단어 열과 동일해야 한다.
    original = (
        "The quick brown fox jumps over the lazy dog. "
        "Pack my box with five dozen liquor jugs. "
        "Sphinx of black quartz, judge my vow."
    )
    out = _split_for_x_thread(original, limit=40)  # 작은 limit → 여러 청크
    # 접두 제거 후 내용 단어 모으기
    content_words: list[str] = []
    for tweet in out:
        body = re.sub(r"^\d+/\s", "", tweet)
        content_words.extend(body.split())
    assert content_words == original.split()


def test_split_exactly_fits_one_tweet_at_boundary():
    # 접두 "1/ " (3문자) + 단어 하나 = 정확히 280 이 되도록 단일 단어 길이 277.
    word = "a" * 277
    out = _split_for_x_thread(word, limit=X_FREE_LIMIT)
    assert len(out) == 1
    assert out[0] == "1/ " + word
    assert len(out[0]) == X_FREE_LIMIT  # 정확히 280


def test_split_just_over_boundary_yields_two_tweets():
    # 단일 단어 278자 → budget 277 초과 → 강제 분할 → 2 트윗.
    # (일반 단어 케이스가 아닌 hard-split 경로지만, 경계(277/278) 검증용으로 사용.)
    word = "a" * 278
    out = _split_for_x_thread(word, limit=X_FREE_LIMIT)
    assert len(out) == 2
    for tweet in out:
        assert len(tweet) <= X_FREE_LIMIT


def test_split_two_words_second_does_not_fit_starts_new_chunk():
    # budget=277. 첫 단어 270 → 청크1. 둘째 단어 270 → 청크1 에 못 들어(270+1+270>277) → 청크2.
    w = "a" * 270
    out = _split_for_x_thread(f"{w} {w}", limit=X_FREE_LIMIT)
    assert len(out) == 2
    assert out[0] == "1/ " + w
    assert out[1] == "2/ " + w


def test_split_oversized_single_word_hard_splits_within_budget():
    # 단일 단어가 budget(277) 초과 → 글자 단위 강제 분할, 각 조각(접두 포함) ≤280.
    huge = "Z" * 600
    out = _split_for_x_thread(huge, limit=X_FREE_LIMIT)
    assert len(out) >= 3
    for tweet in out:
        assert len(tweet) <= X_FREE_LIMIT
    # 모든 Z 가 보존돼야 한다 (접두 제거 후 합치면 원본 복원).
    body_zs = "".join(re.sub(r"^\d+/\s", "", t) for t in out)
    assert body_zs == huge


def test_split_respects_injected_byte_counter():
    # 한글 1글자 = UTF-8 3바이트. counter 를 바이트 기반으로 주입하면
    # 한글 텍스트가 *바이트* 예산 안에서 더 적게 쪼개지는지(더 많은 청크) 검증.
    text = "안녕하세요" * 50  # 250글자 = 750 UTF-8 바이트
    # 문자 수 카운터(len) — 250글자, limit 280 → 1 청크에 다 들어감.
    by_chars = _split_for_x_thread(text, limit=280, counter=len)
    # 바이트 카운터 — 750바이트, limit 280 → 여러 청크.
    by_bytes = _split_for_x_thread(text, limit=280, counter=lambda s: len(s.encode("utf-8")))
    assert len(by_chars) < len(by_bytes)
    # 바이트 기반 분할의 각 청크는 280 바이트 이하.
    for tweet in by_bytes:
        assert len(tweet.encode("utf-8")) <= 280


def test_split_limit_too_small_raises():
    with pytest.raises(ValueError, match="limit too small"):
        _split_for_x_thread("hello", limit=2)


def test_split_non_string_text_raises_type_error():
    with pytest.raises(TypeError, match="text must be str"):
        _split_for_x_thread(12345)  # type: ignore[arg-type]


def test_split_preserves_korean_word_boundaries():
    # 한국어: 공백으로 단어 분리, 단어 중간 cut 금지.
    original = "오늘 날씨가 정말 좋습니다. 산책을 가고 싶어지네요. 여러분은 어떠세요?"
    out = _split_for_x_thread(original, limit=30)
    assert len(out) >= 2
    content_words: list[str] = []
    for tweet in out:
        assert len(tweet) <= 30
        body = re.sub(r"^\d+/\s", "", tweet)
        content_words.extend(body.split())
    assert content_words == original.split()


# === (b) threads_format_multi_channel — MCP 도구 ================================

def test_free_x_splits_600_chars_into_tweets_under_280():
    # ≥3 트윗이 되려면 내용이 554자(2×277) 초과여야 한다. 130 단어 = 649자 → 3 트윗.
    text = " ".join(["word"] * 130)
    assert len(text) > 554
    out = threads_format_multi_channel(text, x_tier="free")
    assert out["x_tier"] == "free"
    tweets = out["x"]
    assert isinstance(tweets, list)
    assert len(tweets) >= 3
    for tw in tweets:
        assert isinstance(tw, str)
        assert len(tw) <= 280
        assert re.match(r"^\d+/\s", tw)


def test_premium_x_returns_single_string():
    text = "프리미엄 티어는 긴 글을 한 트윗으로 올릴 수 있습니다. " * 10
    out = threads_format_multi_channel(text, x_tier="premium")
    assert out["x_tier"] == "premium"
    x = out["x"]
    assert isinstance(x, str)
    # 프리미엄 상한 25000자 이하
    assert len(x) <= 25000


def test_threads_output_under_500_bytes_with_korean():
    # 한글 200글자 = 600 UTF-8 바이트 → 500 바이트 이하로 잘려야 한다.
    text = "안녕" * 100  # 200글자, 600바이트
    out = threads_format_multi_channel(text)
    threads = out["threads"]
    assert isinstance(threads, dict)
    assert threads["bytes"] <= 500
    assert threads["max_bytes"] == 500
    # 실제로 인코딩해 봐도 500 이하
    assert len(threads["text"].encode("utf-8")) <= 500


def test_threads_short_text_passes_through_unchanged():
    text = "짧은 한글 포스트"
    out = threads_format_multi_channel(text)
    threads = out["threads"]
    assert threads["text"] == text
    assert threads["bytes"] == len(text.encode("utf-8"))


def test_facebook_returns_string():
    text = "페이스북용 텍스트입니다. 대화체로 올려주세요."
    out = threads_format_multi_channel(text)
    fb = out["facebook"]
    assert isinstance(fb, str)
    # 가벼운 정규화만 — 내용 보존
    assert "페이스북" in fb


def test_facebook_collapses_excessive_blank_lines():
    text = "첫줄\n\n\n\n\n둘째줄"
    out = threads_format_multi_channel(text)
    assert out["facebook"] == "첫줄\n\n둘째줄"


def test_invalid_x_tier_returns_error():
    out = threads_format_multi_channel("text", x_tier="bogus")
    assert out["error"] is True
    assert "x_tier" in out["message"]


def test_non_string_text_returns_error():
    out = threads_format_multi_channel(12345)  # type: ignore[arg-type]
    assert out["error"] is True
    assert "text must be str" in out["message"]


def test_empty_text_handled():
    out = threads_format_multi_channel("", x_tier="free")
    # threads: 빈 문자열, 0바이트
    assert out["threads"]["text"] == ""
    assert out["threads"]["bytes"] == 0
    # facebook: 빈 문자열
    assert out["facebook"] == ""
    # x free: 빈 리스트
    assert out["x"] == []


def test_default_channels_includes_all_three():
    out = threads_format_multi_channel("텍스트", x_tier="free")
    assert out["channels"] == ["threads", "facebook", "x"]
    assert "threads" in out
    assert "facebook" in out
    assert "x" in out
    # 복붙 안내 note 포함
    assert "note" in out
    assert "복붙" in out["note"]


def test_custom_channels_subset():
    out = threads_format_multi_channel("텍스트", x_tier="free", channels=["x"])
    assert out["channels"] == ["x"]
    assert "x" in out
    assert "threads" not in out
    assert "facebook" not in out


def test_unknown_channels_are_filtered_out():
    out = threads_format_multi_channel(
        "텍스트", x_tier="free", channels=["x", "linkedin", "tiktok"]
    )
    assert out["channels"] == ["x"]


def test_premium_over_25000_chars_truncates_with_flag():
    # 25000자 초과 단일 단어(공백 없음) — premium 단일 문자열 잘림 검증.
    huge = "A" * 30000
    out = threads_format_multi_channel(huge, x_tier="premium")
    assert len(out["x"]) == 25000
    assert out.get("x_truncated") is True


def test_note_states_facebook_x_are_copy_paste_only():
    out = threads_format_multi_channel("텍스트", x_tier="free")
    # note 가 Facebook/X 미발행을 명시하는지.
    assert "발행하지 않" in out["note"]


def test_threads_emoji_byte_count_exercised():
    # 이모지는 4바이트 — 500 바이트 예산을 빨리 소비.
    text = "🎉" * 200  # 800바이트
    out = threads_format_multi_channel(text)
    assert out["threads"]["bytes"] <= 500
    assert len(out["threads"]["text"].encode("utf-8")) <= 500
