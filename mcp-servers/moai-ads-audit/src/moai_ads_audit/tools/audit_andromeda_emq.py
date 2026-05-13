"""
audit_andromeda_emq 도구 — REQ-AUDIT-MCP-011.
Andromeda & Platform Changes 4개 check (M-AN1·M-AT1·M-IA1·M-TH1).

이 도구는 2026 Meta 플랫폼 업데이트 영향도 진단 전용.
카테고리 가중치 = 0 (manifest.json categories[4]._note) — 합산 기여 없음.
정보 제공 목적 — Layer 3가 사용자에게 영향도 컨텍스트 제공.

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    2026 Meta updates: Andromeda algorithm, Advantage+ Targeting, Incremental Attribution, Threshold.
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
# 임계값 — SPEC §3.1.5
# ============================================================

# @MX:ANCHOR: [AUTO] Andromeda EMQ 진단 임계값 SSOT — audit_andromeda_emq·tests 공통 참조
# @MX:REASON: SPEC §3.1.5 (2026 Meta 4종 업데이트) REQ-AUDIT-MCP-011 검증 조건.
ADVANTAGE_PLUS_MIN_ADOPTION = 0.5  # M-AT1 Advantage+ 적용 50% 이상 권장
INCREMENTAL_LIFT_THRESHOLD = 0.05  # M-IA1 Incremental Attribution 측정 가능 최소 lift


class AuditAndromedaEmqInput(BaseModel):
    """audit_andromeda_emq 도구 입력 스키마."""

    pixel_events: list[dict] = Field(
        default_factory=list,
        description=(
            "Pixel 이벤트 데이터 리스트 (선택). 각 항목: "
            "{event_name, event_id, timestamp, parameters: {...}}"
        ),
    )
    ads_data: list[dict] = Field(
        default_factory=list,
        description=(
            "광고 데이터 리스트 (선택). 각 항목: "
            "{ad_id, ad_name, is_advantage_plus_targeting, "
            "incremental_attribution_enabled, threshold_status, "
            "andromeda_score (0-100)}"
        ),
    )
    threshold_changes_acknowledged: bool | None = Field(
        default=None,
        description="2026 Meta Threshold 변경 영향도 인지 여부 (M-TH1, audit_audience_targeting와 cross-ref)",
    )


class AuditAndromedaEmqOutput(BaseModel):
    """audit_andromeda_emq 도구 출력 스키마."""

    checks: list[dict] = Field(description="4개 check 결과 (M-AN1·M-AT1·M-IA1·M-TH1)")
    diagnostic_score: float = Field(
        description="Andromeda 진단 점수 (정보 제공 — 합산 가중치 0)",
    )
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int
    # 2026 Meta 업데이트 영향도 요약
    platform_updates_summary: dict = Field(
        description="2026 Meta 4종 업데이트 영향도 요약 (Andromeda·AT·IA·TH)",
    )


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
        category=CategoryName.ANDROMEDA,
        description=description,
        expected_impact=expected_impact,
        remediation_option=remediation_option,
    )


def audit_andromeda_emq_impl(
    inp: AuditAndromedaEmqInput,
) -> AuditAndromedaEmqOutput:
    """
    Andromeda & Platform Changes 4개 check (M-AN1·M-AT1·M-IA1·M-TH1) 실행.

    REQ-AUDIT-MCP-011: 2026 Meta 플랫폼 업데이트 영향도 진단 —
    Andromeda 알고리즘 / Advantage+ Targeting / Incremental Attribution / Threshold.
    카테고리 가중치 = 0 (정보 제공 목적).
    """
    ads = inp.ads_data
    checks: list[CheckResult] = []
    platform_summary: dict = {}

    # ============================================================
    # M-AN1: Andromeda 알고리즘 영향도 (2026 Meta 한국 시장 적용)
    # ============================================================
    andromeda_scores = [
        float(a["andromeda_score"]) for a in ads
        if a.get("andromeda_score") is not None
    ]
    if andromeda_scores:
        avg_score = sum(andromeda_scores) / len(andromeda_scores)
        platform_summary["andromeda_avg_score"] = round(avg_score, 2)
        # Andromeda 점수가 높으면 알고리즘 적합 (반대로 Similarity와 무관)
        if avg_score >= 70:
            checks.append(_make_check(
                "M-AN1", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"Andromeda 평균 점수 {avg_score:.1f} — 2026 알고리즘 적합",
            ))
        elif avg_score >= 40:
            checks.append(_make_check(
                "M-AN1", CheckStatus.WARNING, SeverityLevel.HIGH,
                description=f"Andromeda 평균 점수 {avg_score:.1f} — 중간 수준",
                expected_impact="2026 Andromeda 알고리즘에서 노출 우선순위 중간 — 개선 여지",
                remediation_option=(
                    "소재 다양화·UGC 비중 확대·미디어 타입 균형으로 점수 개선 검토 권장."
                ),
            ))
        else:
            checks.append(_make_check(
                "M-AN1", CheckStatus.FAIL, SeverityLevel.HIGH,
                description=f"Andromeda 평균 점수 {avg_score:.1f} — 낮음",
                expected_impact="2026 Andromeda에서 노출 비효율 — 도달·전환 하락 가능",
                remediation_option=(
                    "소재 전면 재구성 검토 권장. "
                    "헤드라인·primary text·CTA 변이, UGC 증가, 미디어 균형."
                ),
            ))
    else:
        checks.append(_make_check(
            "M-AN1", CheckStatus.NA, SeverityLevel.HIGH,
            description="andromeda_score 데이터 미제공 — 알고리즘 영향도 산출 불가",
        ))

    # ============================================================
    # M-AT1: Advantage+ Targeting 적용 (한국 광고주 일부 미적용)
    # ============================================================
    if ads:
        adv_plus_ads = [a for a in ads if a.get("is_advantage_plus_targeting")]
        adoption = len(adv_plus_ads) / len(ads)
        platform_summary["advantage_plus_adoption_pct"] = round(adoption, 2)
        if not any("is_advantage_plus_targeting" in a for a in ads):
            checks.append(_make_check(
                "M-AT1", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="is_advantage_plus_targeting 데이터 미제공",
            ))
        elif adoption >= ADVANTAGE_PLUS_MIN_ADOPTION:
            checks.append(_make_check(
                "M-AT1", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"Advantage+ Targeting 채택률 {adoption:.0%} — 권장 기준 ≥{ADVANTAGE_PLUS_MIN_ADOPTION:.0%} 충족",
            ))
        else:
            checks.append(_make_check(
                "M-AT1", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description=f"Advantage+ Targeting 채택률 {adoption:.0%} — 권장 기준 ≥{ADVANTAGE_PLUS_MIN_ADOPTION:.0%} 미달",
                expected_impact="2026 Meta가 Advantage+ 우선 학습 — 미적용 시 효율 손실 가능",
                remediation_option=(
                    "기존 상세 타깃 광고 세트 일부를 Advantage+로 전환 테스트 검토 권장. "
                    "한국 시장에서 Advantage+ 효과 — 광범위 + 알고리즘 신호 자동 최적화."
                ),
            ))
    else:
        checks.append(_make_check(
            "M-AT1", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="ads_data 미제공 — Advantage+ 채택률 산출 불가",
        ))

    # ============================================================
    # M-IA1: Incremental Attribution 활성 (한국 광고주 일부 미인지)
    # ============================================================
    if ads:
        ia_enabled = [a for a in ads if a.get("incremental_attribution_enabled")]
        ia_ratio = len(ia_enabled) / len(ads) if ads else 0
        platform_summary["incremental_attribution_adoption_pct"] = round(ia_ratio, 2)
        if not any("incremental_attribution_enabled" in a for a in ads):
            checks.append(_make_check(
                "M-IA1", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="incremental_attribution_enabled 데이터 미제공",
            ))
        elif ia_ratio > 0:
            checks.append(_make_check(
                "M-IA1", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"Incremental Attribution 활성 광고 {len(ia_enabled)}개 ({ia_ratio:.0%})",
            ))
        else:
            checks.append(_make_check(
                "M-IA1", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description="Incremental Attribution 활성 광고 미감지",
                expected_impact="실제 광고 기여도 측정 부재 — 마지막 클릭 편향 가능",
                remediation_option=(
                    "Meta Incremental Attribution 활성화 검토 권장 — 광고가 실제 추가로 만들어낸 전환 측정. "
                    "한국 광고주 일부 미인지 — 2026 Meta 가이드 동시 확인 권장."
                ),
            ))
    else:
        checks.append(_make_check(
            "M-IA1", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="ads_data 미제공 — Incremental Attribution 진단 불가",
        ))

    # ============================================================
    # M-TH1: Threshold 변화 영향도 (cross-reference with audit_audience_targeting)
    # ============================================================
    if inp.threshold_changes_acknowledged is True:
        checks.append(_make_check(
            "M-TH1", CheckStatus.PASS, SeverityLevel.HIGH,
            description="2026 Meta Threshold 변경 영향도 인지 확인",
        ))
    elif inp.threshold_changes_acknowledged is False:
        checks.append(_make_check(
            "M-TH1", CheckStatus.WARNING, SeverityLevel.HIGH,
            description="2026 Meta Threshold 변경 영향도 미인지",
            expected_impact="Threshold 변경 — 광고 세트 학습·노출 패턴 변동 대응 부재 가능",
            remediation_option=(
                "Meta 공식 Threshold 변경 가이드 확인 검토 권장. "
                "audit_audience_targeting M-TH1과 cross-reference."
            ),
        ))
    else:
        # 광고 데이터에서 threshold_status 추출 시도
        threshold_statuses = [a.get("threshold_status") for a in ads
                              if a.get("threshold_status")]
        if threshold_statuses:
            unknown_count = sum(1 for s in threshold_statuses if str(s).lower() in
                                {"unknown", "not_set", ""})
            if unknown_count > 0:
                checks.append(_make_check(
                    "M-TH1", CheckStatus.WARNING, SeverityLevel.HIGH,
                    description=f"광고 {unknown_count}개 Threshold 상태 불명확",
                    remediation_option="Meta 광고관리자 Threshold 진단 확인 검토 권장.",
                ))
            else:
                checks.append(_make_check(
                    "M-TH1", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"광고 {len(threshold_statuses)}개 Threshold 상태 명확",
                ))
        else:
            checks.append(_make_check(
                "M-TH1", CheckStatus.NA, SeverityLevel.HIGH,
                description="threshold_changes_acknowledged·threshold_status 데이터 미제공",
            ))

    # 2026 Meta 4종 업데이트 영향도 종합
    platform_summary["meta_2026_updates"] = {
        "andromeda": {
            "label": "Andromeda 알고리즘",
            "diagnosis": "소재 다양성·동질성 패턴 진단",
        },
        "advantage_plus_targeting": {
            "label": "Advantage+ Targeting",
            "diagnosis": "광범위 + 알고리즘 자동 최적화",
        },
        "incremental_attribution": {
            "label": "Incremental Attribution",
            "diagnosis": "광고 실제 추가 전환 측정",
        },
        "threshold": {
            "label": "Threshold 변경",
            "diagnosis": "학습·노출 임계값 변경 영향도",
        },
    }

    # ============================================================
    # 진단 점수 계산 (정보 제공 — 합산 기여 없음, weight=0)
    # ============================================================
    # ANDROMEDA 카테고리는 weight=0이므로 calculate_weighted_score의 합산에 기여하지 않음.
    # 단독 카테고리 점수를 별도로 계산하여 출력에 포함.
    pass_count = sum(1 for c in checks if c.status == CheckStatus.PASS)
    warning_count = sum(1 for c in checks if c.status == CheckStatus.WARNING)
    fail_count = sum(1 for c in checks if c.status == CheckStatus.FAIL)
    na_count = sum(1 for c in checks if c.status == CheckStatus.NA)
    effective = pass_count + warning_count + fail_count
    if effective > 0:
        diagnostic_score = (pass_count + 0.5 * warning_count) / effective * 100.0
    else:
        diagnostic_score = 0.0

    return AuditAndromedaEmqOutput(
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
        diagnostic_score=round(diagnostic_score, 2),
        pass_count=pass_count,
        warning_count=warning_count,
        fail_count=fail_count,
        na_count=na_count,
        platform_updates_summary=platform_summary,
    )
