"""
apply_korean_benchmarks 도구 — REQ-AUDIT-MCP-014.
8 카테고리 한국 시장 벤치마크 비교 (CPC/CTR/ROAS/CPA/CVR).

Attribution:
    Korean market benchmarks adapted from NOTICE.md §"Korean Market Adaptation" Area 1·2.
    8 categories (식품/음료·패션/뷰티·건강기능식품·IT/디지털·가정용품·교육·B2B·기타).
    v0.1.0 placeholder — 정식 출처 확정 시 갱신 (SPEC §7 OQ4).

주의:
    REQ-AUDIT-MCP-021: 단정적 권장 금지 — 비교 결과만 반환.
    REQ-AUDIT-MCP-022: 벤치마크 수치는 시간 예측 아님.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from moai_ads_audit.benchmarks.korean import (
    KOREAN_BENCHMARKS,
    IndustryCategory,
    compare_with_benchmark,
    get_benchmark,
)


class ApplyKoreanBenchmarksInput(BaseModel):
    """apply_korean_benchmarks 도구 입력 스키마."""

    audit_results: dict = Field(
        default_factory=dict,
        description=(
            "전체 audit 결과 (선택 — 실측 지표 추출용). 다음 키 인식: "
            "{cpc, ctr, roas, cpa, cvr, xlsx_summary: {spend_total, ...}}. "
            "또는 actual_metrics 키에 {cpc, ctr, roas, cpa, cvr} 직접 전달."
        ),
    )
    industry_category: str = Field(
        description=(
            "산업 카테고리 — 8개 중 1개: "
            "식품/음료 | 패션/뷰티 | 건강기능식품/의료 | IT/디지털 | "
            "가정용품/생활 | 교육/지식 | 서비스/B2B | 기타"
        ),
    )
    # 직접 지표 입력 (audit_results에서 추출 안 되는 경우)
    actual_cpc: float | None = Field(default=None, description="실측 CPC (₩)")
    actual_ctr: float | None = Field(default=None, description="실측 CTR (%)")
    actual_roas: float | None = Field(default=None, description="실측 ROAS")
    actual_cpa: float | None = Field(default=None, description="실측 CPA (₩)")
    actual_cvr: float | None = Field(default=None, description="실측 CVR (%)")


class ApplyKoreanBenchmarksOutput(BaseModel):
    """apply_korean_benchmarks 도구 출력 스키마."""

    industry_category: str = Field(description="매칭된 카테고리 이름")
    benchmark: dict = Field(description="해당 카테고리 벤치마크 5종 (CPC/CTR/ROAS/CPA/CVR)")
    comparison: dict = Field(
        description=(
            "실측 vs 벤치마크 비교 결과. "
            "각 지표: {status (above|within|below|na), actual, benchmark_min, benchmark_max, unit, note}"
        ),
    )
    requires_mfds_review: bool = Field(
        description="식약처 심의 강제 활성 여부 (건강기능식품/의료 카테고리)",
    )
    summary: dict = Field(
        description=(
            "전체 진단 요약: {within_count, below_count, above_count, na_count, "
            "primary_concern (지표 이름 또는 null)}"
        ),
    )
    benchmark_source: str = Field(
        default=(
            "v0.2.0 placeholder — 정해준 강사 노하우 + 자료 1·2·3·4 + 케어밀 사례. "
            "정식 검증 출처 확정 시 갱신 예정 (SPEC §7 OQ4)."
        ),
    )
    attribution: str = Field(
        default=(
            "Korean market benchmarks adapted from NOTICE.md §'Korean Market Adaptation'. "
            "Methodology from agricidaniel/claude-ads v1.5.1 under MIT."
        ),
    )


def _extract_metric(
    audit_results: dict, key: str, override: float | None
) -> float | None:
    """override 우선, 없으면 audit_results에서 추출."""
    if override is not None:
        return float(override)

    # 직접 키
    val = audit_results.get(key)
    if isinstance(val, (int, float)):
        return float(val)

    # actual_metrics 중첩
    actuals = audit_results.get("actual_metrics") or {}
    val = actuals.get(key)
    if isinstance(val, (int, float)):
        return float(val)

    # xlsx_summary 중첩 (parser 출력)
    xlsx = audit_results.get("xlsx_summary") or {}
    val = xlsx.get(key) or xlsx.get(f"{key}_avg")
    if isinstance(val, (int, float)):
        return float(val)

    return None


def apply_korean_benchmarks_impl(
    inp: ApplyKoreanBenchmarksInput,
) -> ApplyKoreanBenchmarksOutput:
    """
    한국 시장 8 카테고리 벤치마크 비교 결과 반환.

    REQ-AUDIT-MCP-014: 8 카테고리 (식품/음료·패션/뷰티·건강기능식품·IT/디지털·
    가정용품·교육·B2B·기타) CPC/CTR/ROAS/CPA/CVR 비교.
    REQ-AUDIT-MCP-021: 단정적 권장 금지 — 비교 데이터만 반환.
    """
    # 실측 지표 추출
    cpc = _extract_metric(inp.audit_results, "cpc", inp.actual_cpc)
    ctr = _extract_metric(inp.audit_results, "ctr", inp.actual_ctr)
    roas = _extract_metric(inp.audit_results, "roas", inp.actual_roas)
    cpa = _extract_metric(inp.audit_results, "cpa", inp.actual_cpa)
    cvr = _extract_metric(inp.audit_results, "cvr", inp.actual_cvr)

    # 벤치마크 비교
    comparison = compare_with_benchmark(
        category_name=inp.industry_category,
        actual_cpc=cpc,
        actual_ctr=ctr,
        actual_roas=roas,
        actual_cpa=cpa,
        actual_cvr=cvr,
    )

    benchmark = get_benchmark(inp.industry_category)

    # 요약 통계
    metrics = comparison["metrics"]
    within_count = sum(1 for m in metrics.values() if m["status"] == "within")
    below_count = sum(1 for m in metrics.values() if m["status"] == "below")
    above_count = sum(1 for m in metrics.values() if m["status"] == "above")
    na_count = sum(1 for m in metrics.values() if m["status"] == "na")

    # primary_concern: 우선 검토 지표 (ROAS below > CPA above > CPC above > 기타)
    primary_concern: str | None = None
    if metrics.get("roas", {}).get("status") == "below":
        primary_concern = "roas"
    elif metrics.get("cpa", {}).get("status") == "above":
        primary_concern = "cpa"
    elif metrics.get("cpc", {}).get("status") == "above":
        primary_concern = "cpc"
    elif metrics.get("cvr", {}).get("status") == "below":
        primary_concern = "cvr"
    elif metrics.get("ctr", {}).get("status") == "below":
        primary_concern = "ctr"

    return ApplyKoreanBenchmarksOutput(
        industry_category=benchmark.category.value,
        benchmark={
            "cpc": benchmark.cpc.to_dict(),
            "ctr": benchmark.ctr.to_dict(),
            "roas": benchmark.roas.to_dict(),
            "cpa": benchmark.cpa.to_dict(),
            "cvr": benchmark.cvr.to_dict(),
        },
        comparison=comparison["metrics"],
        requires_mfds_review=benchmark.requires_mfds_review,
        summary={
            "within_count": within_count,
            "below_count": below_count,
            "above_count": above_count,
            "na_count": na_count,
            "primary_concern": primary_concern,
            "total_metrics": 5,
            "effective_metrics": within_count + below_count + above_count,
        },
    )
