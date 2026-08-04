"""분산 발행(batch) 단위 테스트 — 순수 스케줄 계산 + threads_queue_add_batch 도구.

검증:
  (a) ``_compute_batch_schedule`` — 주입 clock 으로 결정적 결과
      - weekly_3 월요일 아침 시작 → 화/수/목 정오 (faithful to "next N target noon slots")
      - weekly_3 화요일 오후(정오 과거) 시작 → 수/목/다음주 화 (오늘 정오 과거 스킵)
      - weekly_5 → 다음 5개 평일 정오
      - manual → 전부 None
      - 지원 않는 cadence → ValueError
  (b) ``threads_queue_add_batch`` 도구 — tmp DB + 싱글톤 큐
      - PENDING 일괄 등록 (approve=False)
      - APPROVED 일괄 등록 (approve=True) + scheduled_at 반영
      - 빈 posts / 잘못된 media_type → error dict
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from threads_poster import server
from threads_poster.server import _compute_batch_schedule

SEOUL = ZoneInfo("Asia/Seoul")


# --- fixtures (test_server.py 의 패턴 재사용) ------------------------------------
@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """각 테스트마다 큐/자격증명 환경변수 정리 + 싱글톤 초기화."""
    for key in (
        "THREADS_ACCESS_TOKEN",
        "THREADS_USER_ID",
        "THREADS_PUBLISH_DELAY",
        "THREADS_POSTER_DB",
        "CLAUDE_PLUGIN_ROOT",
    ):
        monkeypatch.delenv(key, raising=False)
    server._reset_client_for_tests()
    server._reset_queue_for_tests()
    yield
    server._reset_client_for_tests()
    server._reset_queue_for_tests()


@pytest.fixture
def queue_db(tmp_path, monkeypatch):
    """도구 테스트용: DB 를 tmp_path 로 격리."""
    db = tmp_path / "batch.db"
    monkeypatch.setenv("THREADS_POSTER_DB", str(db))
    server._reset_queue_for_tests()
    yield db
    server._reset_queue_for_tests()


# === (a) _compute_batch_schedule — pure helper ==================================
def test_weekly_3_from_monday_morning_yields_tue_wed_thu():
    # 2026-08-10 은 월요일 아침 08:00 (정오 전).
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    out = _compute_batch_schedule(3, "weekly_3", None, now)
    assert out == [
        "2026-08-11T12:00:00+09:00",  # 화
        "2026-08-12T12:00:00+09:00",  # 수
        "2026-08-13T12:00:00+09:00",  # 목
    ]


def test_weekly_3_from_tuesday_past_noon_skips_today():
    # 2026-08-11 은 화요일 13:00 (정오 과거) → 오늘(화) 스킵 → 수/목/다음주 화.
    # 이것이 "수, 목, 다음주 화" 시퀀스 (task 예시의 출력과 일치).
    now = datetime(2026, 8, 11, 13, 0, 0, tzinfo=SEOUL)
    out = _compute_batch_schedule(3, "weekly_3", None, now)
    assert out == [
        "2026-08-12T12:00:00+09:00",  # 수
        "2026-08-13T12:00:00+09:00",  # 목
        "2026-08-18T12:00:00+09:00",  # 다음주 화
    ]


def test_weekly_3_respects_explicit_start_date_in_future():
    # 명시적 미래 start_date — now 와 무관하게 그 날짜부터 탐색.
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    # 2026-08-25 는 화요일.
    out = _compute_batch_schedule(2, "weekly_3", "2026-08-25", now)
    assert out == [
        "2026-08-25T12:00:00+09:00",  # 화
        "2026-08-26T12:00:00+09:00",  # 수
    ]


def test_weekly_3_skips_past_start_date_to_future_slots():
    # 과거 start_date 주어도 now 이후 슬롯만 나온다.
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    # 2026-08-03 은 지난 월요일 — 모든 과거 슬롯은 now 보다 작아 스킵.
    out = _compute_batch_schedule(1, "weekly_3", "2026-08-03", now)
    assert out == ["2026-08-11T12:00:00+09:00"]  # 다가오는 화


def test_weekly_5_yields_five_weekdays():
    # 2026-08-10(월) 아침 08:00 — 월요일 자체도 정오 전이므로 같은 주 월~금 슬롯.
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    out = _compute_batch_schedule(5, "weekly_5", None, now)
    assert out == [
        "2026-08-10T12:00:00+09:00",  # 월 (오늘, 정오 전)
        "2026-08-11T12:00:00+09:00",  # 화
        "2026-08-12T12:00:00+09:00",  # 수
        "2026-08-13T12:00:00+09:00",  # 목
        "2026-08-14T12:00:00+09:00",  # 금
    ]


def test_weekly_5_from_friday_afternoon_wraps_to_next_week():
    # 금요일 오후(정오 과거) → 이번 주 남은 평일 슬롯 없음 → 다음 주 월~금.
    now = datetime(2026, 8, 14, 15, 0, 0, tzinfo=SEOUL)  # 2026-08-14 금
    out = _compute_batch_schedule(2, "weekly_5", None, now)
    assert out == [
        "2026-08-17T12:00:00+09:00",  # 다음주 월
        "2026-08-18T12:00:00+09:00",  # 다음주 화
    ]


def test_manual_returns_all_none():
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    out = _compute_batch_schedule(3, "manual", None, now)
    assert out == [None, None, None]


def test_zero_n_returns_empty():
    out = _compute_batch_schedule(0, "weekly_3", None, datetime(2026, 8, 10, tzinfo=SEOUL))
    assert out == []


def test_unsupported_cadence_raises_value_error():
    now = datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    with pytest.raises(ValueError, match="unsupported cadence"):
        _compute_batch_schedule(2, "daily", None, now)


def test_naive_now_is_treated_as_seoul():
    # aware now 와 동일한 결과(naive 는 Seoul 로 간주).
    out_naive = _compute_batch_schedule(1, "weekly_3", None, datetime(2026, 8, 10, 8, 0, 0))
    out_aware = _compute_batch_schedule(
        1, "weekly_3", None, datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    )
    assert out_naive == out_aware == ["2026-08-11T12:00:00+09:00"]


# === (b) threads_queue_add_batch — MCP 도구 =====================================
def test_batch_enqueues_as_pending_with_schedules(queue_db, monkeypatch):
    # clock 고정: 2026-08-10(월) 아침 → 화/수/목 정오 슬롯.
    monkeypatch.setattr(
        server, "_now_seoul", lambda: datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    )
    out = server.threads_queue_add_batch(
        posts=[
            {"media_type": "TEXT", "text": "첫째"},
            {"media_type": "TEXT", "text": "둘째"},
            {"media_type": "TEXT", "text": "셋째"},
        ],
        cadence="weekly_3",
    )
    assert out["count"] == 3
    assert out["cadence"] == "weekly_3"
    assert len(out["post_ids"]) == 3
    assert len(out["schedules"]) == 3
    # 모두 PENDING
    for pid in out["post_ids"]:
        assert server.threads_queue_get(pid)["status"] == "PENDING"
    # 예약 시각이 슬롯에 반영됨
    scheduled_ats = [s["scheduled_at"] for s in out["schedules"]]
    assert scheduled_ats == [
        "2026-08-11T12:00:00+09:00",
        "2026-08-12T12:00:00+09:00",
        "2026-08-13T12:00:00+09:00",
    ]
    # schedules 의 post_id 가 post_ids 와 정렬 일치
    assert [s["post_id"] for s in out["schedules"]] == out["post_ids"]


def test_batch_approve_true_enqueues_as_approved(queue_db, monkeypatch):
    monkeypatch.setattr(
        server, "_now_seoul", lambda: datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    )
    out = server.threads_queue_add_batch(
        posts=[{"media_type": "TEXT", "text": "승인건"}],
        cadence="weekly_3",
        approve=True,
    )
    assert out["count"] == 1
    pid = out["post_ids"][0]
    post = server.threads_queue_get(pid)
    assert post["status"] == "APPROVED"
    assert post["scheduled_at"] == "2026-08-11T12:00:00+09:00"


def test_batch_manual_leaves_scheduled_at_null(queue_db, monkeypatch):
    out = server.threads_queue_add_batch(
        posts=[{"text": "수동1"}, {"text": "수동2"}],
        cadence="manual",
    )
    assert out["count"] == 2
    for s in out["schedules"]:
        assert s["scheduled_at"] is None
    for pid in out["post_ids"]:
        post = server.threads_queue_get(pid)
        assert post["status"] == "PENDING"
        assert post["scheduled_at"] is None


def test_batch_defaults_media_type_to_text(queue_db, monkeypatch):
    monkeypatch.setattr(
        server, "_now_seoul", lambda: datetime(2026, 8, 10, 8, 0, 0, tzinfo=SEOUL)
    )
    out = server.threads_queue_add_batch(
        posts=[{"text": "타입 생략"}], cadence="weekly_3"
    )
    pid = out["post_ids"][0]
    assert server.threads_queue_get(pid)["media_type"] == "TEXT"


def test_batch_empty_posts_returns_error(queue_db):
    out = server.threads_queue_add_batch(posts=[], cadence="weekly_3")
    assert out["error"] is True
    assert "posts" in out["message"]


def test_batch_not_a_list_returns_error(queue_db):
    out = server.threads_queue_add_batch(posts="not-a-list", cadence="weekly_3")
    assert out["error"] is True


def test_batch_bad_cadence_returns_error(queue_db):
    out = server.threads_queue_add_batch(
        posts=[{"text": "x"}], cadence="hourly"
    )
    assert out["error"] is True
    assert "cadence" in out["message"]


def test_batch_bad_media_type_returns_error(queue_db):
    out = server.threads_queue_add_batch(
        posts=[{"media_type": "GIF", "text": "x"}], cadence="weekly_3"
    )
    assert out["error"] is True
    assert "media_type" in out["message"]


def test_batch_validation_happens_before_any_enqueue(queue_db, monkeypatch):
    # 첫 draft 는 유효, 둘째가 잘못된 media_type → 어떤 것도 등록되지 않는다.
    before = server.threads_queue_list()["count"]
    out = server.threads_queue_add_batch(
        posts=[
            {"media_type": "TEXT", "text": "ok"},
            {"media_type": "GIF", "text": "bad"},
        ],
        cadence="weekly_3",
    )
    assert out["error"] is True
    after = server.threads_queue_list()["count"]
    assert before == after  # 부분 등록 없음
