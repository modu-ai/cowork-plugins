"""Queue 단위 테스트 — tmp_path DB + clock 주입 (network 없음).

검증 항목:
  (a) enqueue → approve → due → mark_published 상태 머신
  (b) mark_failed 종단 상태
  (c) increment_attempt 카운터
  (d) published_in_last_24h — clock 주입으로 결정적 검증
  (e) idempotent schema (같은 경로 두 번 열기)
  (f) clock 주입: 미래 예약은 due 아님 / 과거 예약은 due / NULL scheduled_at 은 due
  (g) list newest-first + status 필터 + media_type 검증
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from threads_poster.queue import Queue


def _fixed_clock(at: datetime):
    """고정 시각을 반환하는 clock callable 생성 (build a fixed-time clock)."""
    return lambda: at


# --- (a) enqueue → approve → due → mark_published 상태 머신 ----------------------
def test_enqueue_returns_id_and_defaults(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    pid = q.enqueue("TEXT", text="hi")
    assert isinstance(pid, int) and pid > 0
    post = q.get(pid)
    assert post["status"] == "PENDING"
    assert post["media_type"] == "TEXT"
    assert post["text"] == "hi"
    assert post["attempts"] == 0
    assert post["scheduled_at"] is None
    assert post["created_at"] is not None
    q.close()


def test_approve_flips_status_and_sets_scheduled(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    pid = q.enqueue("TEXT", text="hi")
    ok = q.approve(pid)
    assert ok is True
    post = q.get(pid)
    assert post["status"] == "APPROVED"
    assert post["approved_at"] is not None
    # scheduled_at 기본값 = now (즉시 due 가 되도록)
    assert post["scheduled_at"] is not None
    q.close()


def test_approve_preserves_explicit_schedule(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    pid = q.enqueue("TEXT", text="hi")
    future = (now + timedelta(hours=3)).isoformat()
    q.approve(pid, scheduled_at=future)
    post = q.get(pid)
    assert post["scheduled_at"] == future
    q.close()


def test_due_returns_approved_and_due_posts(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    pid = q.enqueue("TEXT", text="hi")
    q.approve(pid)  # scheduled_at = now → due
    due = q.due()
    assert len(due) == 1
    assert due[0]["id"] == pid
    q.close()


def test_mark_published_sets_terminal_state(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    pid = q.enqueue("TEXT", text="hi")
    q.approve(pid)
    ok = q.mark_published(
        pid, container_id="C1", media_id="M1", permalink_hint="https://x"
    )
    assert ok is True
    post = q.get(pid)
    assert post["status"] == "PUBLISHED"
    assert post["container_id"] == "C1"
    assert post["media_id"] == "M1"
    assert post["permalink_hint"] == "https://x"
    assert post["published_at"] is not None
    # PUBLISHED 는 due() 에서 제외된다
    assert q.due() == []
    q.close()


# --- (b) mark_failed 종단 상태 --------------------------------------------------
def test_mark_failed_sets_terminal_state_and_removes_from_due(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    pid = q.enqueue("TEXT", text="hi")
    q.approve(pid)
    q.mark_failed(pid, error="boom")
    post = q.get(pid)
    assert post["status"] == "FAILED"
    assert post["last_error"] == "boom"
    assert q.due() == []
    q.close()


def test_approve_returns_false_for_missing_post(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    assert q.approve(9999) is False
    q.close()


def test_get_returns_none_for_missing_post(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    assert q.get(9999) is None
    q.close()


# --- (c) increment_attempt -----------------------------------------------------
def test_increment_attempt_bumps_counter(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    pid = q.enqueue("TEXT", text="hi")
    q.increment_attempt(pid)
    q.increment_attempt(pid)
    assert q.get(pid)["attempts"] == 2
    q.close()


# --- (d) published_in_last_24h — clock 주입으로 결정적 검증 ---------------------
def test_published_in_last_24h_counts_only_recent(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))

    # 발행 1: 1시간 전 (within 24h) — clock 을 1시간 전으로 움직여 published_at 기록
    pid1 = q.enqueue("TEXT", text="recent")
    q._clock = _fixed_clock(now - timedelta(hours=1))
    q.approve(pid1)
    q.mark_published(pid1, container_id="C", media_id="M")

    # 발행 2: 2일 전 (outside 24h)
    q._clock = _fixed_clock(now - timedelta(days=2))
    pid2 = q.enqueue("TEXT", text="old")
    q.approve(pid2)
    q.mark_published(pid2, container_id="C", media_id="M")

    # clock 복구 후 집계 — 24h 이내 1건만 카운트
    q._clock = _fixed_clock(now)
    assert q.published_in_last_24h() == 1
    q.close()


def test_published_in_last_24h_zero_when_empty(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    assert q.published_in_last_24h() == 0
    q.close()


# --- (e) idempotent schema (같은 경로 두 번 열기) ------------------------------
def test_schema_idempotent_open_twice_preserves_data(tmp_path):
    path = str(tmp_path / "q.db")
    q1 = Queue(path)
    pid = q1.enqueue("TEXT", text="hi")
    q1.close()

    # 다시 열어도 에러 없음, 기존 데이터 보존
    q2 = Queue(path)
    assert q2.get(pid)["text"] == "hi"
    # 세 번째도 OK
    q2.close()
    q3 = Queue(path)
    assert q3.get(pid)["text"] == "hi"
    q3.close()


# --- (f) clock 주입: scheduled_at 비교 -----------------------------------------
def test_future_scheduled_post_is_not_due(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    future = (now + timedelta(hours=1)).isoformat()
    q.enqueue("TEXT", text="hi", scheduled_at=future, status="APPROVED")
    assert q.due() == []
    q.close()


def test_past_scheduled_post_is_due(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    past = (now - timedelta(hours=1)).isoformat()
    pid = q.enqueue("TEXT", text="hi", scheduled_at=past, status="APPROVED")
    due = q.due()
    assert len(due) == 1
    assert due[0]["id"] == pid
    q.close()


def test_approved_null_scheduled_is_due(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    # enqueue 로 status=APPROVED + scheduled_at=None 직접 생성 (approve 경유 X)
    pid = q.enqueue("TEXT", text="hi", status="APPROVED")
    due = q.due()
    assert len(due) == 1
    assert due[0]["id"] == pid
    q.close()


def test_due_includes_null_and_past_excludes_future(tmp_path):
    now = datetime(2026, 8, 4, 12, 0, 0)
    q = Queue(str(tmp_path / "q.db"), clock=_fixed_clock(now))
    pid_null = q.enqueue("TEXT", text="null", status="APPROVED")
    pid_past = q.enqueue(
        "TEXT", text="past", scheduled_at=(now - timedelta(hours=1)).isoformat(),
        status="APPROVED",
    )
    q.enqueue(
        "TEXT", text="future", scheduled_at=(now + timedelta(hours=1)).isoformat(),
        status="APPROVED",
    )
    due_ids = {p["id"] for p in q.due()}
    assert due_ids == {pid_null, pid_past}
    q.close()


# --- (g) list / media_type 검증 ------------------------------------------------
def test_list_newest_first(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    ids = [q.enqueue("TEXT", text=str(i)) for i in range(3)]
    listed = q.list()
    assert [p["id"] for p in listed] == list(reversed(ids))
    q.close()


def test_list_filter_by_status(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    p1 = q.enqueue("TEXT", text="a")
    p2 = q.enqueue("TEXT", text="b")
    q.approve(p1)
    pending = q.list(status="PENDING")
    assert len(pending) == 1
    assert pending[0]["id"] == p2
    approved = q.list(status="APPROVED")
    assert len(approved) == 1
    assert approved[0]["id"] == p1
    q.close()


def test_enqueue_rejects_unknown_media_type(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    with pytest.raises(ValueError, match="unsupported media_type"):
        q.enqueue("GIF")
    q.close()


def test_enqueue_rejects_unknown_status(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    with pytest.raises(ValueError, match="unsupported status"):
        q.enqueue("TEXT", text="hi", status="WEIRD")
    q.close()


def test_enqueue_image_and_video_store_urls(tmp_path):
    q = Queue(str(tmp_path / "q.db"))
    pid_img = q.enqueue("IMAGE", image_url="https://example.com/i.png", text="캡션")
    pid_vid = q.enqueue("VIDEO", video_url="https://example.com/v.mp4")
    assert q.get(pid_img)["image_url"] == "https://example.com/i.png"
    assert q.get(pid_vid)["video_url"] == "https://example.com/v.mp4"
    q.close()
