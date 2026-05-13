"""
한국 시장 8 카테고리 벤치마크 — SPEC §3.6.
NOTICE.md §"Korean Market Adaptation" Area 1 (Benchmarks)·Area 2 (Industry classification) 인용.

출처 (v0.1.0 placeholder):
    - 정해준 강사 노하우 + 자료 1·2·3·4 + 케어밀 사례 (GOOS행님 통합)
    - NOTICE.md §"Korean Market Adaptation" Area 1 직접 인용 수치
    - 케어밀 1.80 ROAS reference (저관여 식품 기준)
    - v1은 placeholder — 정식 검증 출처 확정 시 갱신 (SPEC §7 OQ4)

주의:
    - REQ-AUDIT-MCP-022: 시간 예측 표현 금지 (벤치마크 수치는 예측 아님)
    - REQ-AUDIT-MCP-021: 단정적 권장 금지 (결과는 비교 데이터만 반환)
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IndustryCategory(str, Enum):
    """한국 시장 8 카테고리 — SPEC §3.6."""
    FOOD_BEVERAGE = "식품/음료"
    FASHION_BEAUTY = "패션/뷰티"
    HEALTH_MEDICAL = "건강기능식품/의료"
    IT_DIGITAL = "IT/디지털"
    HOME_LIVING = "가정용품/생활"
    EDUCATION = "교육/지식"
    SERVICE_B2B = "서비스/B2B"
    OTHER = "기타"


@dataclass(frozen=True)
class BenchmarkRange:
    """벤치마크 범위 값."""
    min_val: float
    max_val: float
    unit: str = ""
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "min": self.min_val,
            "max": self.max_val,
            "unit": self.unit,
            "note": self.note,
        }


@dataclass(frozen=True)
class CategoryBenchmark:
    """카테고리별 5종 벤치마크."""
    category: IndustryCategory
    cpc: BenchmarkRange      # 클릭당 비용 (₩)
    ctr: BenchmarkRange      # 클릭률 (%)
    roas: BenchmarkRange     # 광고 수익률
    cpa: BenchmarkRange      # 전환당 비용 (₩, v0.1.0 추정치)
    cvr: BenchmarkRange      # 전환율 (%, v0.1.0 추정치)
    # 식약처 심의 강제 활성 여부 (건강기능식품/의료 카테고리)
    requires_mfds_review: bool = False

    def to_dict(self) -> dict:
        return {
            "category": self.category.value,
            "cpc": self.cpc.to_dict(),
            "ctr": self.ctr.to_dict(),
            "roas": self.roas.to_dict(),
            "cpa": self.cpa.to_dict(),
            "cvr": self.cvr.to_dict(),
            "requires_mfds_review": self.requires_mfds_review,
        }


# ============================================================
# 한국 시장 8 카테고리 벤치마크 — SPEC §3.6 NOTICE.md 직접 인용
# v0.1.0 placeholder: 정식 검증 출처 확정 시 갱신 (SPEC §7 OQ4)
# @MX:ANCHOR: [AUTO] 한국 벤치마크 SSOT — apply_korean_benchmarks 도구·tests 공통 참조
# @MX:REASON: SPEC §3.6 "8 카테고리 벤치마크 5종" REQ-AUDIT-MCP-014 검증 조건.
#             벤치마크 수치 변경 시 NOTICE.md §"Korean Market Adaptation" Area 1 동기 갱신 필수.
# ============================================================
KOREAN_BENCHMARKS: dict[IndustryCategory, CategoryBenchmark] = {
    IndustryCategory.FOOD_BEVERAGE: CategoryBenchmark(
        category=IndustryCategory.FOOD_BEVERAGE,
        cpc=BenchmarkRange(500, 1500, "₩", "케어밀 reference 포함"),
        ctr=BenchmarkRange(0.8, 2.0, "%"),
        roas=BenchmarkRange(1.5, 2.5, "x", "케어밀 1.80 ROAS reference (저관여 식품 기준)"),
        cpa=BenchmarkRange(5000, 20000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(1.0, 3.5, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.FASHION_BEAUTY: CategoryBenchmark(
        category=IndustryCategory.FASHION_BEAUTY,
        cpc=BenchmarkRange(800, 2500, "₩", "자료 1·2 차용"),
        ctr=BenchmarkRange(1.0, 2.5, "%"),
        roas=BenchmarkRange(2.0, 3.5, "x"),
        cpa=BenchmarkRange(8000, 30000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(1.5, 4.0, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.HEALTH_MEDICAL: CategoryBenchmark(
        category=IndustryCategory.HEALTH_MEDICAL,
        cpc=BenchmarkRange(1000, 3000, "₩"),
        ctr=BenchmarkRange(0.5, 1.5, "%"),
        roas=BenchmarkRange(1.8, 3.0, "x"),
        cpa=BenchmarkRange(15000, 50000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(0.8, 2.5, "%", "v0.1.0 추정치"),
        requires_mfds_review=True,  # 식약처 심의 강제 활성 (REQ-AUDIT-MCP-015)
    ),
    IndustryCategory.IT_DIGITAL: CategoryBenchmark(
        category=IndustryCategory.IT_DIGITAL,
        cpc=BenchmarkRange(600, 2000, "₩", "자료 4 차용"),
        ctr=BenchmarkRange(1.0, 2.5, "%"),
        roas=BenchmarkRange(2.5, 4.5, "x"),
        cpa=BenchmarkRange(6000, 25000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(1.5, 4.5, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.HOME_LIVING: CategoryBenchmark(
        category=IndustryCategory.HOME_LIVING,
        cpc=BenchmarkRange(400, 1200, "₩", "자료 3 차용"),
        ctr=BenchmarkRange(1.0, 2.0, "%"),
        roas=BenchmarkRange(1.8, 3.0, "x"),
        cpa=BenchmarkRange(5000, 18000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(1.2, 3.5, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.EDUCATION: CategoryBenchmark(
        category=IndustryCategory.EDUCATION,
        cpc=BenchmarkRange(700, 2500, "₩"),
        ctr=BenchmarkRange(0.8, 2.0, "%"),
        roas=BenchmarkRange(2.0, 4.0, "x"),
        cpa=BenchmarkRange(10000, 40000, "₩", "v0.1.0 추정치"),
        cvr=BenchmarkRange(1.0, 3.5, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.SERVICE_B2B: CategoryBenchmark(
        category=IndustryCategory.SERVICE_B2B,
        cpc=BenchmarkRange(1500, 5000, "₩"),
        ctr=BenchmarkRange(0.5, 1.5, "%"),
        roas=BenchmarkRange(1.5, 3.0, "x", "LTV 기반 ROAS 보정 권장"),
        cpa=BenchmarkRange(20000, 100000, "₩", "v0.1.0 추정치, LTV 기반 보정 권장"),
        cvr=BenchmarkRange(0.5, 2.0, "%", "v0.1.0 추정치"),
    ),
    IndustryCategory.OTHER: CategoryBenchmark(
        category=IndustryCategory.OTHER,
        cpc=BenchmarkRange(500, 3000, "₩", "8 카테고리 fallback — 자동 추정"),
        ctr=BenchmarkRange(0.5, 2.5, "%", "8 카테고리 fallback — 자동 추정"),
        roas=BenchmarkRange(1.5, 4.0, "x", "8 카테고리 fallback — 자동 추정"),
        cpa=BenchmarkRange(5000, 50000, "₩", "8 카테고리 fallback — 자동 추정"),
        cvr=BenchmarkRange(0.8, 4.0, "%", "8 카테고리 fallback — 자동 추정"),
    ),
}


def get_benchmark(category_name: str) -> CategoryBenchmark:
    """
    카테고리 이름 → CategoryBenchmark 반환.
    매칭 실패 시 OTHER fallback.

    Args:
        category_name: 카테고리 이름 (한국어 또는 영어)

    Returns:
        CategoryBenchmark 인스턴스
    """
    # 한국어 이름 직접 매칭
    for cat in IndustryCategory:
        if cat.value == category_name.strip():
            return KOREAN_BENCHMARKS[cat]

    # 영어 키 매칭 (IndustryCategory enum name)
    normalized = category_name.upper().replace(" ", "_").replace("/", "_")
    for cat in IndustryCategory:
        if cat.name == normalized:
            return KOREAN_BENCHMARKS[cat]

    # 부분 매칭 시도 (식품, 패션 등 약칭)
    for cat in IndustryCategory:
        if any(part in category_name for part in cat.value.split("/")):
            return KOREAN_BENCHMARKS[cat]

    # 매칭 실패 → OTHER fallback (SPEC §3.6 8번)
    return KOREAN_BENCHMARKS[IndustryCategory.OTHER]


def compare_with_benchmark(
    category_name: str,
    actual_cpc: float | None = None,
    actual_ctr: float | None = None,
    actual_roas: float | None = None,
    actual_cpa: float | None = None,
    actual_cvr: float | None = None,
) -> dict:
    """
    실측값 vs 한국 벤치마크 비교 결과 반환.
    REQ-AUDIT-MCP-021 단정적 명령 금지: 비교 결과만 반환, 권고 텍스트는 Layer 3 책임.

    Args:
        category_name: 산업 카테고리 이름
        actual_*: 실측 지표값 (None이면 비교 생략)

    Returns:
        비교 결과 dict (above/within/below/na 상태 + 벤치마크 범위)
    """
    benchmark = get_benchmark(category_name)

    def compare_metric(
        actual: float | None,
        bench: BenchmarkRange,
    ) -> dict:
        """단일 지표 비교."""
        if actual is None:
            return {
                "status": "na",
                "actual": None,
                "benchmark_min": bench.min_val,
                "benchmark_max": bench.max_val,
                "unit": bench.unit,
                "note": bench.note,
            }
        if actual < bench.min_val:
            status = "below"
        elif actual > bench.max_val:
            status = "above"
        else:
            status = "within"
        return {
            "status": status,
            "actual": actual,
            "benchmark_min": bench.min_val,
            "benchmark_max": bench.max_val,
            "unit": bench.unit,
            "note": bench.note,
        }

    return {
        "category": benchmark.category.value,
        "requires_mfds_review": benchmark.requires_mfds_review,
        "metrics": {
            "cpc": compare_metric(actual_cpc, benchmark.cpc),
            "ctr": compare_metric(actual_ctr, benchmark.ctr),
            "roas": compare_metric(actual_roas, benchmark.roas),
            "cpa": compare_metric(actual_cpa, benchmark.cpa),
            "cvr": compare_metric(actual_cvr, benchmark.cvr),
        },
        "benchmark_source": "v0.1.0 placeholder — 정식 출처 확정 시 갱신 예정 (SPEC §7 OQ4)",
    }
