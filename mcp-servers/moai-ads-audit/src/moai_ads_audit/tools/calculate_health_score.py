"""
calculate_health_score 도구 — REQ-AUDIT-MCP-012.
가중치 스코어링 공식으로 0-100 점수 + A-F 등급 산출.

Attribution:
    Scoring formula adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from moai_ads_audit.scoring.weighted import (
    WeightedScoreResult,
    score_from_category_results,
)


class CalculateHealthScoreInput(BaseModel):
    """calculate_health_score 도구 입력 스키마."""

    category_results: dict = Field(
        description=(
            "카테고리별 check 결과 딕셔너리. "
            "키: pixel_capi | creative | account_structure | audience. "
            "값: [{check_id, status, severity, description, ...}, ...]"
        )
    )
    severity_map: dict = Field(
        default_factory=dict,
        description="check ID별 심각도 오버라이드 (선택). 예: {'M01': 'Critical'}",
    )


class CalculateHealthScoreOutput(BaseModel):
    """calculate_health_score 도구 출력 스키마."""

    # 합산 점수 + 등급
    total_score: float = Field(description="0-100 가중치 합산 점수")
    grade: str = Field(description="A-F 등급 (A: 90+ / B: 75-89 / C: 60-74 / D: 40-59 / F: <40)")
    # 한국 시장 표현 (Layer 3 권장, REQ-AUDIT-MCP-021)
    grade_kr_label: str = Field(description="한국 시장 등급 표현 (SPEC §3.3, Layer 3 렌더링 권장)")
    # 카테고리 분해
    category_breakdown: list[dict] = Field(description="카테고리별 점수 분해")
    # 집계
    summary: dict = Field(description="총 check 수 + PASS/WARNING/FAIL/NA 집계")
    # 공식 attribution (REQ-AUDIT-MCP-003)
    attribution: str = Field(
        default=(
            "Scoring formula adapted from agricidaniel/claude-ads v1.5.1 under MIT. "
            "See .claude/rules/moai/NOTICE.md §'agricidaniel/claude-ads (MIT)'."
        )
    )


# 한국 시장 등급 표현 — SPEC §3.3
_GRADE_KR_LABELS: dict[str, str] = {
    "A": "우수 — 현 운영 유지 검토 권장",
    "B": "양호 — 미세 조정 가능",
    "C": "보통 — 중도 옵션 검토 권장",
    "D": "미흡 — 적극 옵션 검토 권장",
    "F": "위험 — 즉시 진단 권장",
}


def calculate_health_score_impl(
    inp: CalculateHealthScoreInput,
) -> CalculateHealthScoreOutput:
    """
    가중치 스코어링 공식 실행.
    REQ-AUDIT-MCP-012: S_total 공식 + A-F 등급.

    Args:
        inp: CalculateHealthScoreInput (category_results + severity_map)

    Returns:
        CalculateHealthScoreOutput (total_score, grade, category_breakdown, summary)
    """
    result: WeightedScoreResult = score_from_category_results(
        category_results=inp.category_results,
        severity_map=inp.severity_map or {},
    )

    # 카테고리별 분해 직렬화
    category_breakdown = [
        {
            "category": cs.category.value,
            "raw_score": cs.raw_score,
            "weighted_contribution": cs.weighted_contribution,
            "pass_count": cs.pass_count,
            "warning_count": cs.warning_count,
            "fail_count": cs.fail_count,
            "na_count": cs.na_count,
        }
        for cs in result.category_scores
    ]

    return CalculateHealthScoreOutput(
        total_score=result.total_score,
        grade=result.grade,
        grade_kr_label=_GRADE_KR_LABELS.get(result.grade, "알 수 없음"),
        category_breakdown=category_breakdown,
        summary={
            "total_checks": result.total_checks,
            "effective_checks": result.effective_checks,
            "pass_count": result.pass_count,
            "warning_count": result.warning_count,
            "fail_count": result.fail_count,
            "na_count": result.na_count,
        },
    )
