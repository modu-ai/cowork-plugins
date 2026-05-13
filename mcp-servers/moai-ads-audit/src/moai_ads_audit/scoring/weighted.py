"""
가중치 스코어링 공식 구현 — claude-ads v1.5.1 (MIT) 인용.
REQ-AUDIT-MCP-012: S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100

Attribution:
    Scoring formula adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    See `.claude/rules/moai/NOTICE.md` §"agricidaniel/claude-ads (MIT)".
"""
from __future__ import annotations

from enum import Enum
from typing import NamedTuple

from pydantic import BaseModel, Field


# ============================================================
# 상수 정의 — claude-ads v1.5.1 인용
# ============================================================

class CheckStatus(str, Enum):
    """4상태 매핑 — NOTICE.md §"Weighted Scoring Algorithm" 직접 인용."""
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    NA = "N/A"


class SeverityLevel(str, Enum):
    """Severity 레벨 — claude-ads v1.5.1 (NOTICE.md 직접 인용)."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class CategoryName(str, Enum):
    """5 카테고리 — claude-ads v1.5.1 가중치 구조 + Andromeda 진단 (weight=0)."""
    PIXEL_CAPI = "pixel_capi"
    CREATIVE = "creative"
    ACCOUNT_STRUCTURE = "account_structure"
    AUDIENCE = "audience"
    # ANDROMEDA: weight=0 별도 진단 카테고리 (SPEC §3.1.5)
    # 가중치 합산에 기여하지 않고 정보 제공 목적 (manifest.json categories[4]._note)
    ANDROMEDA = "andromeda"


# Severity multiplier — claude-ads v1.5.1 (NOTICE.md 직접 인용)
# @MX:ANCHOR: [AUTO] 가중치 스코어링 핵심 상수 — claude-ads v1.5.1 인용값. 변경 시 모든 unit test 재검증 필수.
# @MX:REASON: SPEC §3.2 "NOTICE.md 직접 인용" — 임의 변경 금지. REQ-AUDIT-MCP-012 검증 조건.
SEVERITY_MULTIPLIER: dict[SeverityLevel, float] = {
    SeverityLevel.CRITICAL: 5.0,
    SeverityLevel.HIGH: 3.0,
    SeverityLevel.MEDIUM: 1.5,
    SeverityLevel.LOW: 0.5,
}

# 카테고리 가중치 — claude-ads v1.5.1 (NOTICE.md 직접 인용)
# Andromeda는 weight=0 — 합산 기여 없음 (manifest.json categories[4]._note 직접 인용)
CATEGORY_WEIGHT: dict[CategoryName, float] = {
    CategoryName.PIXEL_CAPI: 0.30,      # 30%
    CategoryName.CREATIVE: 0.30,         # 30%
    CategoryName.ACCOUNT_STRUCTURE: 0.20, # 20%
    CategoryName.AUDIENCE: 0.20,         # 20%
    CategoryName.ANDROMEDA: 0.0,          # 별도 진단 (가중치 없음)
}

# PASS/WARNING/FAIL → C_pass 매핑 — NOTICE.md 직접 인용
STATUS_TO_CPASS: dict[CheckStatus, float] = {
    CheckStatus.PASS: 1.0,
    CheckStatus.WARNING: 0.5,
    CheckStatus.FAIL: 0.0,
    CheckStatus.NA: -1.0,  # -1 = C_total에서 제외 신호
}

# A-F 등급 임계값 — claude-ads v1.5.1 (NOTICE.md §"A-F grading" 직접 인용)
GRADE_THRESHOLDS: list[tuple[float, str]] = [
    (90.0, "A"),
    (75.0, "B"),
    (60.0, "C"),
    (40.0, "D"),
    (0.0, "F"),
]


# ============================================================
# 데이터 모델
# ============================================================

class CheckResult(BaseModel):
    """단일 check 결과."""
    check_id: str = Field(description="check ID (예: M01, M-CR1)")
    status: CheckStatus = Field(description="PASS/WARNING/FAIL/N/A")
    severity: SeverityLevel = Field(description="심각도")
    category: CategoryName = Field(description="소속 카테고리")
    # 체크 ID·심각도·예상 영향·시정 옵션 4요소 구조 (REQ-AUDIT-MCP-021 단정적 명령 금지)
    description: str = Field(default="", description="check 설명")
    expected_impact: str = Field(default="", description="예상 영향 (단정적 명령 금지)")
    remediation_option: str = Field(default="", description="시정 옵션 (검토 권장 형식)")


class CategoryScore(BaseModel):
    """카테고리별 점수."""
    category: CategoryName
    raw_score: float = Field(description="0-100 카테고리 내부 점수")
    weighted_contribution: float = Field(description="전체 점수 기여분")
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int


class WeightedScoreResult(BaseModel):
    """가중치 스코어링 최종 결과."""
    total_score: float = Field(description="0-100 합산 점수")
    grade: str = Field(description="A-F 등급")
    # 카테고리별 분해
    category_scores: list[CategoryScore]
    # 집계
    total_checks: int
    effective_checks: int  # N/A 제외
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int


# ============================================================
# 핵심 함수
# ============================================================

def get_grade(score: float) -> str:
    """
    0-100 점수 → A-F 등급 변환.
    claude-ads v1.5.1 A-F grading: A 90+ / B 75-89 / C 60-74 / D 40-59 / F <40
    """
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


def calculate_category_score(
    checks: list[CheckResult],
) -> tuple[float, int, int, int, int]:
    """
    단일 카테고리 내부 점수 계산.

    공식: Σ(C_pass × W_sev) / Σ(C_total × W_sev) × 100
    N/A 상태 check는 분자·분모 모두 제외.

    Returns:
        (raw_score, pass_count, warning_count, fail_count, na_count)
    """
    numerator = 0.0
    denominator = 0.0
    pass_count = warning_count = fail_count = na_count = 0

    for check in checks:
        w_sev = SEVERITY_MULTIPLIER[check.severity]
        c_pass = STATUS_TO_CPASS[check.status]

        if check.status == CheckStatus.NA:
            # N/A → C_total에서 제외 (NOTICE.md 직접 인용)
            na_count += 1
            continue

        denominator += w_sev  # C_total 항
        numerator += c_pass * w_sev  # C_pass × W_sev 항

        if check.status == CheckStatus.PASS:
            pass_count += 1
        elif check.status == CheckStatus.WARNING:
            warning_count += 1
        else:
            fail_count += 1

    # 유효 check 0개면 N/A 카테고리 → 0.0 반환
    raw_score = (numerator / denominator * 100.0) if denominator > 0 else 0.0
    return raw_score, pass_count, warning_count, fail_count, na_count


# @MX:ANCHOR: [AUTO] 가중치 스코어링 공식 핵심 진입점 — fan_in >= 3 (tools 3종 + tests)
# @MX:REASON: SPEC §3.2 공식 S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
#             REQ-AUDIT-MCP-012 검증 조건. 이 함수 변경 시 모든 scoring unit test 재검증 필수.
def calculate_weighted_score(
    check_results: list[CheckResult],
) -> WeightedScoreResult:
    """
    claude-ads v1.5.1 가중치 스코어링 공식 적용.

    S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100

    PASS  → C_pass = 1.0
    WARNING → C_pass = 0.5
    FAIL  → C_pass = 0.0
    N/A   → C_total에서 제외

    Args:
        check_results: 전체 check 결과 리스트 (4 카테고리 혼합 가능)

    Returns:
        WeightedScoreResult (total_score, grade, category_scores, ...)
    """
    # 카테고리별 분류
    category_map: dict[CategoryName, list[CheckResult]] = {
        cat: [] for cat in CategoryName
    }
    for check in check_results:
        category_map[check.category].append(check)

    # 카테고리별 점수 계산
    category_scores: list[CategoryScore] = []
    total_numerator = 0.0
    total_denominator = 0.0
    agg_pass = agg_warning = agg_fail = agg_na = 0

    for cat, checks in category_map.items():
        if not checks:
            # 데이터 없는 카테고리 — 기여 없음
            category_scores.append(
                CategoryScore(
                    category=cat,
                    raw_score=0.0,
                    weighted_contribution=0.0,
                    pass_count=0,
                    warning_count=0,
                    fail_count=0,
                    na_count=0,
                )
            )
            continue

        raw_score, p, w, f, n = calculate_category_score(checks)
        w_cat = CATEGORY_WEIGHT[cat]
        weighted_contribution = raw_score * w_cat

        # 전체 합산에 카테고리 가중치 반영
        # 유효 check가 있는 카테고리만 전체 공식에 반영
        effective = p + w + f
        if effective > 0:
            total_numerator += weighted_contribution
            total_denominator += 100.0 * w_cat  # 최대 기여분

        category_scores.append(
            CategoryScore(
                category=cat,
                raw_score=round(raw_score, 2),
                weighted_contribution=round(weighted_contribution, 2),
                pass_count=p,
                warning_count=w,
                fail_count=f,
                na_count=n,
            )
        )
        agg_pass += p
        agg_warning += w
        agg_fail += f
        agg_na += n

    # S_total 계산
    if total_denominator > 0:
        total_score = total_numerator / total_denominator * 100.0
    else:
        total_score = 0.0

    total_score = round(min(max(total_score, 0.0), 100.0), 2)
    grade = get_grade(total_score)

    return WeightedScoreResult(
        total_score=total_score,
        grade=grade,
        category_scores=category_scores,
        total_checks=len(check_results),
        effective_checks=agg_pass + agg_warning + agg_fail,
        pass_count=agg_pass,
        warning_count=agg_warning,
        fail_count=agg_fail,
        na_count=agg_na,
    )


def score_from_category_results(
    category_results: dict,
    severity_map: dict | None = None,
) -> WeightedScoreResult:
    """
    calculate_health_score 도구에서 호출하는 편의 함수.
    category_results dict → CheckResult 리스트 변환 후 가중치 공식 적용.

    Args:
        category_results: {"pixel_capi": [{"check_id": "M01", "status": "PASS", ...}], ...}
        severity_map: {"M01": "Critical", ...} (선택, 기본값은 check 내부 severity)
    """
    checks: list[CheckResult] = []
    severity_map = severity_map or {}

    for cat_name, check_list in category_results.items():
        # 카테고리 이름 정규화
        try:
            cat = CategoryName(cat_name)
        except ValueError:
            continue  # 알 수 없는 카테고리 skip

        for item in check_list:
            check_id = item.get("check_id", "UNKNOWN")
            status_raw = item.get("status", "N/A")
            severity_raw = severity_map.get(check_id, item.get("severity", "Medium"))

            try:
                status = CheckStatus(status_raw)
            except ValueError:
                status = CheckStatus.NA

            try:
                severity = SeverityLevel(severity_raw)
            except ValueError:
                severity = SeverityLevel.MEDIUM

            checks.append(
                CheckResult(
                    check_id=check_id,
                    status=status,
                    severity=severity,
                    category=cat,
                    description=item.get("description", ""),
                    expected_impact=item.get("expected_impact", ""),
                    remediation_option=item.get("remediation_option", ""),
                )
            )

    return calculate_weighted_score(checks)
