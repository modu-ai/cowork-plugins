"""
audit_account_structure 도구 — REQ-AUDIT-MCP-009.
Account Structure 10개 check (M11-M18 + M-ST1~2).

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    Learning Limited <30% threshold, CBO/ABO decision matrix cited from NOTICE.md.
    M-ST1·M-ST2 adapted from 정해준 강사 노하우 + 자료 3.
    See NOTICE.md §"agricidaniel/claude-ads (MIT)".
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from moai_ads_audit.scoring.weighted import (
    CategoryName,
    CheckResult,
    CheckStatus,
    SeverityLevel,
    WeightedScoreResult,
    calculate_weighted_score,
)

# ============================================================
# 임계값 — SPEC §3.1.3, claude-ads v1.5.1 + 정해준 강사 노하우
# ============================================================

# @MX:ANCHOR: [AUTO] Account Structure 임계값 SSOT — audit_account_structure·tests 공통 참조
# @MX:REASON: SPEC §3.1.3 (Learning Limited 30%·세트 수·예산 적정성) REQ-AUDIT-MCP-009 검증 조건.
LEARNING_LIMITED_THRESHOLD = 0.3  # claude-ads v1.5.1 (NOTICE.md 인용)
MIN_BUDGET_VS_CPA_RATIO = 50  # M14: 일예산 ÷ CPA ≥ 50 (학습 단계 진입 권장)
MAX_ADSETS_PER_CAMPAIGN = 5  # M37-M40 광고 세트 수 적정성
MIN_BUDGET_TIMES_UNIT_PRICE = 3  # M-ST2 예산 = 제품 단가 × 3 (자료 3)
AUDIENCE_NETWORK_ROAS_THRESHOLD = 0.5  # M35: Audience Network ROAS 미달 진단


class AuditAccountStructureInput(BaseModel):
    """audit_account_structure 도구 입력 스키마."""

    campaigns: list[dict] = Field(
        default_factory=list,
        description=(
            "캠페인 데이터 리스트. 각 항목 (모두 선택 필드): "
            "{campaign_id, campaign_name, objective, budget_type ('CBO'|'ABO'), "
            "daily_budget, adsets: [{adset_id, learning_status, placements, "
            "audience_size, ...}], placements_distribution, "
            "cpa, roas, audience_network_roas, product_unit_price}"
        ),
    )
    time_range: str = Field(
        default="",
        description="분석 기간 라벨",
    )


class AuditAccountStructureOutput(BaseModel):
    """audit_account_structure 도구 출력 스키마."""

    checks: list[dict] = Field(description="10개 check 결과 (M11-M18 + M-ST1~2)")
    category_score: float = Field(description="Account Structure 카테고리 0-100 점수")
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int
    learning_limited_ratio: float | None = Field(
        default=None, description="Learning Limited 광고 세트 비율"
    )
    structure_summary: dict = Field(description="구조 진단 요약")
    time_range: str = ""


def _make_check(
    check_id: str,
    status: CheckStatus,
    severity: SeverityLevel,
    description: str,
    expected_impact: str = "",
    remediation_option: str = "",
) -> CheckResult:
    return CheckResult(
        check_id=check_id,
        status=status,
        severity=severity,
        category=CategoryName.ACCOUNT_STRUCTURE,
        description=description,
        expected_impact=expected_impact,
        remediation_option=remediation_option,
    )


def _collect_adsets(campaigns: list[dict]) -> list[dict]:
    """모든 캠페인의 adsets 평탄화."""
    adsets: list[dict] = []
    for c in campaigns:
        for a in c.get("adsets") or []:
            adsets.append(a)
    return adsets


def audit_account_structure_impl(
    inp: AuditAccountStructureInput,
) -> AuditAccountStructureOutput:
    """
    Account Structure 10개 check (M11-M18 + M-ST1~2) 실행.

    REQ-AUDIT-MCP-009: Learning Limited <30% / CBO vs ABO 결정 /
    캠페인 목표·예산·노출 위치 정합성 / 광고 세트 수 적정성.
    REQ-AUDIT-MCP-021: 단정적 명령 금지.
    """
    campaigns = inp.campaigns
    adsets = _collect_adsets(campaigns)
    checks: list[CheckResult] = []
    structure_summary: dict = {}
    learning_limited_ratio: float | None = None

    # ============================================================
    # M11-M14: Learning Limited <30% (4 check 분해)
    # ============================================================
    if adsets:
        limited = [a for a in adsets if str(a.get("learning_status", "")).lower() in
                   {"limited", "learning_limited", "learning limited"}]
        learning_limited_ratio = len(limited) / len(adsets)
        structure_summary["learning_limited_count"] = len(limited)
        structure_summary["learning_limited_ratio"] = round(learning_limited_ratio, 2)
        structure_summary["total_adsets"] = len(adsets)

        # M11: 전체 비율
        if learning_limited_ratio < LEARNING_LIMITED_THRESHOLD:
            checks.append(_make_check(
                "M11", CheckStatus.PASS, SeverityLevel.CRITICAL,
                description=f"Learning Limited 비율 {learning_limited_ratio:.0%} — 임계값 <{LEARNING_LIMITED_THRESHOLD:.0%} 충족",
            ))
        else:
            checks.append(_make_check(
                "M11", CheckStatus.FAIL, SeverityLevel.CRITICAL,
                description=f"Learning Limited 비율 {learning_limited_ratio:.0%} — 임계값 <{LEARNING_LIMITED_THRESHOLD:.0%} 초과",
                expected_impact="학습 단계 통과 광고 세트 부족 — 전환 최적화 효율 저하 가능",
                remediation_option=(
                    "광고 세트 통합 또는 예산 증액으로 주간 전환 ≥50건 확보 검토 권장. "
                    "한국 소형 광고주 환경에서는 세트 통폐합 우선 검토."
                ),
            ))

        # M12: 학습 단계 통과 세트 존재 여부
        learned = [a for a in adsets if str(a.get("learning_status", "")).lower() in
                   {"learned", "active", "out_of_learning"}]
        if learned:
            checks.append(_make_check(
                "M12", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"학습 통과 세트 {len(learned)}개 운용 중",
            ))
        else:
            checks.append(_make_check(
                "M12", CheckStatus.WARNING, SeverityLevel.HIGH,
                description="학습 단계 통과 광고 세트 미감지",
                expected_impact="전체 광고 세트가 학습 미완 — 최적화 효율 미달",
                remediation_option=(
                    "전환 이벤트 변경·예산 조정·타깃 범위 재구성으로 학습 진입 검토 권장."
                ),
            ))

        # M13: 학습 단계 광고 세트 (정상 단계)
        in_learning = [a for a in adsets if str(a.get("learning_status", "")).lower() in
                       {"learning", "in_learning"}]
        if in_learning:
            checks.append(_make_check(
                "M13", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"학습 진행 중 세트 {len(in_learning)}개 — 단계 정상 진행",
            ))
        elif limited or learned:
            checks.append(_make_check(
                "M13", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description="학습 진행 단계 광고 세트 없음 (Limited 또는 완료 단계로 분류됨)",
            ))
        else:
            checks.append(_make_check(
                "M13", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="learning_status 데이터 불명확",
            ))

        # M14: 일예산 ÷ CPA ≥ 50 (학습 진입 조건)
        budget_ratios = []
        for a in adsets:
            db = a.get("daily_budget")
            cpa = a.get("cpa")
            if db and cpa and cpa > 0:
                budget_ratios.append(db / cpa)
        if budget_ratios:
            avg_ratio = sum(budget_ratios) / len(budget_ratios)
            structure_summary["avg_budget_cpa_ratio"] = round(avg_ratio, 2)
            if avg_ratio >= MIN_BUDGET_VS_CPA_RATIO:
                checks.append(_make_check(
                    "M14", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"평균 일예산÷CPA 비율 {avg_ratio:.1f} — 학습 진입 권장 기준 ≥{MIN_BUDGET_VS_CPA_RATIO} 충족",
                ))
            else:
                checks.append(_make_check(
                    "M14", CheckStatus.WARNING, SeverityLevel.HIGH,
                    description=f"평균 일예산÷CPA 비율 {avg_ratio:.1f} — 학습 진입 권장 기준 ≥{MIN_BUDGET_VS_CPA_RATIO} 미달",
                    expected_impact="예산 대비 CPA 비율 부족 — 학습 단계 진입 어려움 가능",
                    remediation_option=(
                        "광고 세트 예산 증액 또는 통폐합으로 일예산÷CPA ≥50 확보 검토 권장."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M14", CheckStatus.NA, SeverityLevel.HIGH,
                description="daily_budget 또는 cpa 데이터 미제공",
            ))
    else:
        for cid, sev in [("M11", SeverityLevel.CRITICAL), ("M12", SeverityLevel.HIGH),
                         ("M13", SeverityLevel.MEDIUM), ("M14", SeverityLevel.HIGH)]:
            checks.append(_make_check(
                cid, CheckStatus.NA, sev,
                description="campaigns/adsets 데이터 미제공",
            ))

    # ============================================================
    # M15-M18: CBO vs ABO 결정 + 캠페인 목표·예산·노출 위치 정합성
    # ============================================================
    if campaigns:
        cbo_count = sum(1 for c in campaigns if str(c.get("budget_type", "")).upper() == "CBO")
        abo_count = sum(1 for c in campaigns if str(c.get("budget_type", "")).upper() == "ABO")
        structure_summary["cbo_count"] = cbo_count
        structure_summary["abo_count"] = abo_count

        # M15: CBO/ABO 운영 철학 일관성
        if cbo_count > 0 and abo_count > 0:
            checks.append(_make_check(
                "M15", CheckStatus.WARNING, SeverityLevel.HIGH,
                description=f"CBO {cbo_count}개·ABO {abo_count}개 혼재 — 운영 철학 분기 가능성",
                expected_impact="운영 철학 혼재 — 학습·예산 분배 일관성 저하 가능",
                remediation_option=(
                    "캠페인 목적별 CBO·ABO 구분 정합성 검토 권장. "
                    "자동 신뢰형 (CBO) vs 적극 통제형 (ABO) 선택 기준 명확화 권장."
                ),
            ))
        elif cbo_count > 0 or abo_count > 0:
            mode = "CBO" if cbo_count > 0 else "ABO"
            checks.append(_make_check(
                "M15", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"{mode} 통일 운영 — 운영 철학 일관성 확인",
            ))
        else:
            checks.append(_make_check(
                "M15", CheckStatus.NA, SeverityLevel.HIGH,
                description="budget_type 데이터 미제공",
            ))

        # M16: 캠페인 목표 명시 여부
        objectives = [c.get("objective") for c in campaigns if c.get("objective")]
        if not objectives:
            checks.append(_make_check(
                "M16", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="캠페인 목표 데이터 미제공",
            ))
        elif len(objectives) == len(campaigns):
            checks.append(_make_check(
                "M16", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"전체 {len(campaigns)}개 캠페인 목표 명시 확인",
            ))
        else:
            checks.append(_make_check(
                "M16", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description=f"캠페인 목표 미명시 {len(campaigns) - len(objectives)}개",
                expected_impact="목표 미명시 캠페인 — 최적화 신호 부정확 가능",
                remediation_option="모든 캠페인에 명확한 목표 (Purchase·Lead 등) 설정 검토 권장.",
            ))

        # M17: 예산 분포 적정성
        budgets = [float(c.get("daily_budget", 0)) for c in campaigns if c.get("daily_budget")]
        if budgets:
            avg_b = sum(budgets) / len(budgets)
            max_b = max(budgets)
            structure_summary["avg_daily_budget"] = round(avg_b, 2)
            structure_summary["max_daily_budget"] = round(max_b, 2)
            if max_b > avg_b * 5:
                checks.append(_make_check(
                    "M17", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                    description=f"예산 분포 편중 — 최대/평균 비율 {max_b / avg_b:.1f}배",
                    expected_impact="특정 캠페인 예산 집중 — 학습·테스트 다양성 제한 가능",
                    remediation_option="캠페인 간 예산 분배 균형화 또는 통폐합 검토 권장.",
                ))
            else:
                checks.append(_make_check(
                    "M17", CheckStatus.PASS, SeverityLevel.MEDIUM,
                    description="캠페인 간 예산 분포 균형적",
                ))
        else:
            checks.append(_make_check(
                "M17", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="daily_budget 데이터 미제공",
            ))

        # M18: 노출 위치 정합성 (Audience Network ROAS 진단)
        an_roas_values = []
        for c in campaigns:
            an_roas = c.get("audience_network_roas")
            if an_roas is not None:
                an_roas_values.append(float(an_roas))
        if an_roas_values:
            avg_an_roas = sum(an_roas_values) / len(an_roas_values)
            structure_summary["audience_network_avg_roas"] = round(avg_an_roas, 2)
            if avg_an_roas < AUDIENCE_NETWORK_ROAS_THRESHOLD:
                checks.append(_make_check(
                    "M18", CheckStatus.WARNING, SeverityLevel.HIGH,
                    description=f"Audience Network 평균 ROAS {avg_an_roas:.2f} — 임계값 ≥{AUDIENCE_NETWORK_ROAS_THRESHOLD} 미달",
                    expected_impact="한국 시장에서 Audience Network ROAS 0 빈발 — 예산 낭비 가능",
                    remediation_option=(
                        "Audience Network 노출 위치 배제 옵션 검토 권장. "
                        "또는 별도 광고 세트로 분리 후 성과 모니터링."
                    ),
                ))
            else:
                checks.append(_make_check(
                    "M18", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"Audience Network 평균 ROAS {avg_an_roas:.2f} — 정상 범위",
                ))
        else:
            checks.append(_make_check(
                "M18", CheckStatus.NA, SeverityLevel.HIGH,
                description="audience_network_roas 데이터 미제공",
            ))
    else:
        for cid, sev in [("M15", SeverityLevel.HIGH), ("M16", SeverityLevel.MEDIUM),
                         ("M17", SeverityLevel.MEDIUM), ("M18", SeverityLevel.HIGH)]:
            checks.append(_make_check(
                cid, CheckStatus.NA, sev,
                description="campaigns 데이터 미제공",
            ))

    # ============================================================
    # M-ST1: 캠페인 통폐합 우선순위 (정해준 노하우)
    # ============================================================
    if campaigns:
        # 광고 세트 수가 많은 캠페인 감지
        adset_counts = [(c.get("campaign_name", "(이름 없음)"), len(c.get("adsets") or []))
                        for c in campaigns]
        oversized = [(name, n) for name, n in adset_counts if n > MAX_ADSETS_PER_CAMPAIGN]
        structure_summary["oversized_campaigns"] = [
            {"name": name, "adset_count": n} for name, n in oversized[:5]
        ]
        if not oversized:
            checks.append(_make_check(
                "M-ST1", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"모든 캠페인 광고 세트 수 ≤{MAX_ADSETS_PER_CAMPAIGN}개",
            ))
        else:
            checks.append(_make_check(
                "M-ST1", CheckStatus.WARNING, SeverityLevel.HIGH,
                description=f"광고 세트 {MAX_ADSETS_PER_CAMPAIGN}개 초과 캠페인 {len(oversized)}개",
                expected_impact="한국 소형 광고주 환경 — 세트 과다 시 학습 분산·예산 분배 비효율",
                remediation_option=(
                    "세트 통폐합 검토 권장 — 유사 타깃·노출 위치 광고 세트 통합. "
                    "정해준 강사 노하우: 캠페인당 광고 세트 5개 이하 권장."
                ),
            ))
    else:
        checks.append(_make_check(
            "M-ST1", CheckStatus.NA, SeverityLevel.HIGH,
            description="campaigns 데이터 미제공 — 통폐합 분석 불가",
        ))

    # ============================================================
    # M-ST2: 예산 적정성 (제품 단가 × 3) — 자료 3
    # ============================================================
    if campaigns:
        low_budget_campaigns = []
        for c in campaigns:
            unit_price = c.get("product_unit_price")
            db = c.get("daily_budget")
            if unit_price and db:
                threshold = unit_price * MIN_BUDGET_TIMES_UNIT_PRICE
                if db < threshold:
                    low_budget_campaigns.append({
                        "name": c.get("campaign_name", "(이름 없음)"),
                        "daily_budget": db,
                        "min_recommended": threshold,
                    })
        if not any(c.get("product_unit_price") for c in campaigns):
            checks.append(_make_check(
                "M-ST2", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="product_unit_price 데이터 미제공 — 예산 적정성 진단 불가",
            ))
        elif not low_budget_campaigns:
            checks.append(_make_check(
                "M-ST2", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"모든 캠페인 일예산 ≥ 제품 단가 × {MIN_BUDGET_TIMES_UNIT_PRICE} 충족",
            ))
        else:
            checks.append(_make_check(
                "M-ST2", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description=f"일예산 부족 캠페인 {len(low_budget_campaigns)}개 (자료 3 기준 단가×{MIN_BUDGET_TIMES_UNIT_PRICE} 미달)",
                expected_impact="예산 부족 — 학습 단계 진입 어려움·표본 부족 가능",
                remediation_option=(
                    f"일예산을 제품 단가 × {MIN_BUDGET_TIMES_UNIT_PRICE} 수준으로 증액 검토 권장. "
                    "자료 3 기준: 표본 확보·CPA 안정화에 필요한 최소 예산."
                ),
            ))
        structure_summary["low_budget_campaigns"] = low_budget_campaigns[:5]
    else:
        checks.append(_make_check(
            "M-ST2", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="campaigns 데이터 미제공 — 예산 적정성 진단 불가",
        ))

    # ============================================================
    # 카테고리 점수 계산
    # ============================================================
    score_result: WeightedScoreResult = calculate_weighted_score(checks)
    cat_score = next(
        (cs.raw_score for cs in score_result.category_scores
         if cs.category == CategoryName.ACCOUNT_STRUCTURE),
        0.0,
    )

    return AuditAccountStructureOutput(
        checks=[
            {
                "check_id": c.check_id,
                "status": c.status.value,
                "severity": c.severity.value,
                "description": c.description,
                "expected_impact": c.expected_impact,
                "remediation_option": c.remediation_option,
            }
            for c in checks
        ],
        category_score=cat_score,
        pass_count=score_result.pass_count,
        warning_count=score_result.warning_count,
        fail_count=score_result.fail_count,
        na_count=score_result.na_count,
        learning_limited_ratio=learning_limited_ratio,
        structure_summary=structure_summary,
        time_range=inp.time_range,
    )
