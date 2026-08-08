"""할당량 회계 — 이 서버의 핵심 방어."""

from __future__ import annotations

from moai_youtube.quota import QuotaLedger, cost_of


class _Clock:
    def __init__(self, now: float = 1_700_000_000.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now


def test_검색이_조회보다_100배_비싸다():
    """이 비대칭이 서버 설계 전체를 규정한다."""
    assert cost_of("search.list") == 100
    assert cost_of("videos.list") == 1
    assert cost_of("playlistItems.list") == 1


def test_업로드는_더_이상_가장_비싼_작업이_아니다():
    """2025-12-04 개정으로 약 1,600 → 약 100 으로 내려갔다."""
    assert cost_of("videos.insert") == 100
    assert cost_of("videos.insert") < cost_of("captions.insert")


def test_분석_api는_할당량을_쓰지_않는다():
    assert cost_of("analytics.query") == 0


def test_모르는_엔드포인트는_보수적으로_1(tmp_path):
    assert cost_of("무언가.새로운것") == 1


def test_소모량이_누적되고_파일에_남는다(tmp_path):
    path = tmp_path / "q.json"
    ledger = QuotaLedger(path=path, clock=_Clock())
    ledger.charge("search.list")
    ledger.charge("videos.list")
    assert ledger.used == 101

    # 새 프로세스가 이어받는다
    assert QuotaLedger(path=path, clock=_Clock()).used == 101


def test_한도_초과를_사전에_판정한다(tmp_path):
    ledger = QuotaLedger(path=tmp_path / "q.json", daily_limit=150, clock=_Clock())
    ledger.charge("search.list")  # 100
    assert ledger.would_exceed("search.list") is True  # 100 + 100 > 150
    assert ledger.would_exceed("videos.list") is False  # 100 + 1 <= 150


def test_임계를_넘으면_경고한다(tmp_path):
    ledger = QuotaLedger(path=tmp_path / "q.json", daily_limit=100, warn_ratio=0.8, clock=_Clock())
    assert ledger.should_warn() is False
    ledger.charge("search.list")
    assert ledger.should_warn() is True
    assert ledger.snapshot()["warning"] is True


def test_날짜가_바뀌면_0으로_돌아간다(tmp_path):
    clock = _Clock()
    ledger = QuotaLedger(path=tmp_path / "q.json", clock=clock)
    ledger.charge("search.list")
    assert ledger.used == 100

    clock.now += 86_400  # 하루 뒤
    assert ledger.used == 0


def test_기록_실패가_도구_실패로_번지지_않는다(tmp_path):
    """원장을 못 써도 API 호출 자체는 계속돼야 한다."""
    blocker = tmp_path / "blocked"
    blocker.write_text("파일", encoding="utf-8")

    ledger = QuotaLedger(path=blocker / "q.json", clock=_Clock())
    ledger.charge("search.list")  # 예외가 나지 않아야 한다
    assert ledger.used == 100


def test_손상된_원장은_0에서_다시_시작한다(tmp_path):
    path = tmp_path / "q.json"
    path.write_text("{깨진 JSON", encoding="utf-8")
    assert QuotaLedger(path=path, clock=_Clock()).used == 0


def test_잔량_요약에_추정치임을_밝힌다(tmp_path):
    snapshot = QuotaLedger(path=tmp_path / "q.json", clock=_Clock()).snapshot()
    assert snapshot["remaining"] == 10_000
    assert "추정치" in snapshot["note"]
