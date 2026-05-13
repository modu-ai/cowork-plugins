"""
audit_audience_targeting 도구 — REQ-AUDIT-MCP-010.
Audience & Targeting 7개 check (M19-M24 + M-TH1).

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    Audience overlap <20%, Lookalike seed quality (≥1000), Custom Audience freshness (≤180d)
    thresholds cited from NOTICE.md.
    M-TH1 (Threshold) is cross-referenced with audit_andromeda_emq.
    See NOTICE.md §"agricidaniel/claude-ads (MIT)".
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

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
# 임계값 — SPEC §3.1.4, claude-ads v1.5.1
# ============================================================

# @MX:ANCHOR: [AUTO] Audience Targeting 임계값 SSOT — audit_audience_targeting·tests 공통 참조
# @MX:REASON: SPEC §3.1.4 (overlap 20%·LAL seed 1000·CA 180일) REQ-AUDIT-MCP-010 검증 조건.
AUDIENCE_OVERLAP_THRESHOLD = 0.20  # 20% (claude-ads v1.5.1, NOTICE.md 인용)
LOOKALIKE_MIN_SEED_SIZE = 1000  # M21-M22 seed 최소 1,000명
CUSTOM_AUDIENCE_MAX_DAYS = 180  # M23 신선도 ≤180일 (한국 PIPA 보관 한계)
BROAD_AUDIENCE_MIN_SIZE = 1_000_000  # M24 광범위 타깃 최소 100만 (Advantage+ 권장)


class AuditAudienceTargetingInput(BaseModel):
    """audit_audience_targeting 도구 입력 스키마."""

    audiences: list[dict] = Field(
        default_factory=list,
        description=(
            "오디언스 리스트. 각 항목 (선택 필드): "
            "{audience_id, audience_name, audience_type ('custom'|'lookalike'|'broad'|'saved'), "
            "size (int), created_at (ISO date), last_updated (ISO date), "
            "overlap_pct_with: {other_audience_id: float}, "
            "is_advantage_plus (bool)}"
        ),
    )
    lookalike_seeds: list[dict] = Field(
        default_factory=list,
        description=(
            "Lookalike seed 오디언스 리스트. 각 항목 (선택): "
            "{seed_id, seed_name, seed_size (int), seed_type ('Purchase'|'Lead'|'PageView')}"
        ),
    )
    threshold_changes_acknowledged: bool | None = Field(
        default=None,
        description="2026 Meta Threshold 변경 영향도 인지 여부 (M-TH1)",
    )


class AuditAudienceTargetingOutput(BaseModel):
    """audit_audience_targeting 도구 출력 스키마."""

    checks: list[dict] = Field(description="7개 check 결과 (M19-M24 + M-TH1)")
    category_score: float = Field(description="Audience 카테고리 0-100 점수")
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int
    overlap_summary: dict = Field(description="overlap 진단 요약")
    audience_summary: dict = Field(description="오디언스 진단 요약")


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
        category=CategoryName.AUDIENCE,
        description=description,
        expected_impact=expected_impact,
        remediation_option=remediation_option,
    )


def _parse_date(value: Any) -> date | None:
    """ISO 날짜 문자열·datetime → date 변환."""
    if not value:
        return None
    if isinstance(value, date):
        return value if not isinstance(value, datetime) else value.date()
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        return None


def audit_audience_targeting_impl(
    inp: AuditAudienceTargetingInput,
) -> AuditAudienceTargetingOutput:
    """
    Audience & Targeting 7개 check (M19-M24 + M-TH1) 실행.

    REQ-AUDIT-MCP-010: audience overlap <20% / Lookalike seed quality /
    Custom Audience 신선도 / 광범위 타깃 vs 상세 타깃 분리.
    """
    audiences = inp.audiences
    lookalike_seeds = inp.lookalike_seeds
    checks: list[CheckResult] = []
    overlap_summary: dict = {}
    audience_summary: dict = {
        "total_audiences": len(audiences),
        "total_lookalike_seeds": len(lookalike_seeds),
    }

    # ============================================================
    # M19-M20: audience overlap <20% (2 check 분해)
    # ============================================================
    overlap_pairs = []
    for a in audiences:
        overlaps = a.get("overlap_pct_with") or {}
        for other, pct in overlaps.items():
            try:
                pct_val = float(pct)
            except (ValueError, TypeError):
                continue
            overlap_pairs.append((a.get("audience_id", "?"), other, pct_val))

    high_overlap = [p for p in overlap_pairs if p[2] >= AUDIENCE_OVERLAP_THRESHOLD]
    overlap_summary["high_overlap_count"] = len(high_overlap)
    overlap_summary["max_overlap"] = round(max([p[2] for p in overlap_pairs], default=0.0), 3)
    overlap_summary["high_overlap_pairs"] = [
        {"audience": p[0], "other": p[1], "overlap": round(p[2], 3)}
        for p in high_overlap[:5]
    ]

    # M19: overlap 임계값 충족 여부
    if not overlap_pairs:
        checks.append(_make_check(
            "M19", CheckStatus.NA, SeverityLevel.HIGH,
            description="overlap_pct_with 데이터 미제공",
        ))
    elif not high_overlap:
        checks.append(_make_check(
            "M19", CheckStatus.PASS, SeverityLevel.HIGH,
            description=f"모든 오디언스 쌍 overlap <{AUDIENCE_OVERLAP_THRESHOLD:.0%} 충족",
        ))
    else:
        ratio = len(high_overlap) / len(overlap_pairs)
        status = CheckStatus.FAIL if ratio > 0.5 else CheckStatus.WARNING
        checks.append(_make_check(
            "M19", status, SeverityLevel.HIGH,
            description=f"overlap ≥{AUDIENCE_OVERLAP_THRESHOLD:.0%} 쌍 {len(high_overlap)}개 ({ratio:.0%})",
            expected_impact="오디언스 중복 — 동일 사용자에게 다중 광고 노출·예산 비효율 가능",
            remediation_option=(
                "고중복 쌍 통폐합 또는 제외 옵션 (exclude) 설정 검토 권장. "
                "한국 광고주 환경에서 overlap 빈발 — 정기 모니터링 권장."
            ),
        ))

    # M20: overlap 점검 빈도 (인사이트 — overlap 데이터 자체 존재 여부)
    if overlap_pairs:
        checks.append(_make_check(
            "M20", CheckStatus.PASS, SeverityLevel.MEDIUM,
            description=f"오디언스 overlap 데이터 {len(overlap_pairs)}쌍 확인 — 정기 모니터링 가능",
        ))
    else:
        checks.append(_make_check(
            "M20", CheckStatus.WARNING, SeverityLevel.MEDIUM,
            description="overlap 진단 데이터 부재 — Meta 광고관리자 overlap 도구 활용 권장",
            expected_impact="overlap 모니터링 미수행 — 오디언스 비효율 누적 가능",
            remediation_option=(
                "Meta 광고관리자 → Audiences → Show Audience Overlap 정기 활용 검토 권장."
            ),
        ))

    # ============================================================
    # M21-M22: Lookalike seed 품질 (≥1,000명)
    # ============================================================
    lookalike_audiences = [a for a in audiences if a.get("audience_type") == "lookalike"]

    # M21: LAL seed 크기 ≥1000
    if lookalike_seeds:
        small_seeds = [s for s in lookalike_seeds
                       if (s.get("seed_size") or 0) < LOOKALIKE_MIN_SEED_SIZE]
        audience_summary["small_seed_count"] = len(small_seeds)
        audience_summary["small_seeds"] = [
            {"name": s.get("seed_name", "(이름 없음)"), "size": s.get("seed_size")}
            for s in small_seeds[:5]
        ]
        if not small_seeds:
            checks.append(_make_check(
                "M21", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"모든 Lookalike seed 크기 ≥{LOOKALIKE_MIN_SEED_SIZE}명",
            ))
        else:
            checks.append(_make_check(
                "M21", CheckStatus.WARNING, SeverityLevel.HIGH,
                description=f"seed 크기 <{LOOKALIKE_MIN_SEED_SIZE}명 LAL {len(small_seeds)}개",
                expected_impact="한국 소형 광고주 환경 — seed 부족 시 LAL 품질·도달 제한 가능",
                remediation_option=(
                    f"seed 오디언스 확장 (최소 {LOOKALIKE_MIN_SEED_SIZE}명) 검토 권장. "
                    "Custom Audience 보존 기간 연장·복수 이벤트 통합 옵션 검토."
                ),
            ))
    elif lookalike_audiences:
        checks.append(_make_check(
            "M21", CheckStatus.WARNING, SeverityLevel.HIGH,
            description=f"Lookalike 오디언스 {len(lookalike_audiences)}개 운용 중이나 seed 정보 미제공",
            expected_impact="seed 품질 미확인 — LAL 효율 진단 불가",
            remediation_option="lookalike_seeds 데이터 제공 검토 권장.",
        ))
    else:
        checks.append(_make_check(
            "M21", CheckStatus.NA, SeverityLevel.HIGH,
            description="Lookalike 오디언스·seed 데이터 미제공",
        ))

    # M22: LAL seed 유형 다양성 (Purchase·Lead·PageView)
    if lookalike_seeds:
        seed_types = {s.get("seed_type") for s in lookalike_seeds if s.get("seed_type")}
        audience_summary["seed_types"] = sorted(seed_types) if seed_types else []
        if not seed_types:
            checks.append(_make_check(
                "M22", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="seed_type 데이터 미제공",
            ))
        elif "Purchase" in seed_types:
            checks.append(_make_check(
                "M22", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"Purchase 기반 seed 운용 확인 (유형 {len(seed_types)}종)",
            ))
        else:
            checks.append(_make_check(
                "M22", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description=f"Purchase 기반 seed 부재 — 현재 유형: {sorted(seed_types)}",
                expected_impact="Purchase 기반 LAL 부재 — 전환 최적화 LAL 효율 제한 가능",
                remediation_option=(
                    "Purchase 이벤트 기반 Custom Audience 생성 + LAL 시드로 활용 검토 권장."
                ),
            ))
    else:
        checks.append(_make_check(
            "M22", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="lookalike_seeds 미제공",
        ))

    # ============================================================
    # M23: Custom Audience 신선도 (≤180일, 한국 PIPA 보관 한계)
    # ============================================================
    custom_audiences = [a for a in audiences if a.get("audience_type") == "custom"]
    if custom_audiences:
        today = date.today()
        stale_audiences = []
        for a in custom_audiences:
            last_updated = _parse_date(a.get("last_updated") or a.get("created_at"))
            if last_updated:
                age_days = (today - last_updated).days
                if age_days > CUSTOM_AUDIENCE_MAX_DAYS:
                    stale_audiences.append({
                        "name": a.get("audience_name", "(이름 없음)"),
                        "age_days": age_days,
                    })
        audience_summary["stale_audience_count"] = len(stale_audiences)
        audience_summary["stale_audiences"] = stale_audiences[:5]
        if not stale_audiences:
            checks.append(_make_check(
                "M23", CheckStatus.PASS, SeverityLevel.MEDIUM,
                description=f"모든 Custom Audience 신선도 ≤{CUSTOM_AUDIENCE_MAX_DAYS}일",
            ))
        else:
            checks.append(_make_check(
                "M23", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                description=f"신선도 >{CUSTOM_AUDIENCE_MAX_DAYS}일 Custom Audience {len(stale_audiences)}개",
                expected_impact="오래된 오디언스 — 매칭률 저하·PIPA 보관 한계 가능",
                remediation_option=(
                    f"Custom Audience 갱신 또는 {CUSTOM_AUDIENCE_MAX_DAYS}일 이내 재생성 검토 권장. "
                    "PIPA 개인정보 보관 기간 정책 동시 검토 권장."
                ),
            ))
    else:
        checks.append(_make_check(
            "M23", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="Custom Audience 데이터 미제공",
        ))

    # ============================================================
    # M24: 광범위 타깃 vs 상세 타깃 분리 (Advantage+ 권장)
    # ============================================================
    broad_audiences = [a for a in audiences if a.get("audience_type") == "broad"
                       or (a.get("size") and int(a["size"]) >= BROAD_AUDIENCE_MIN_SIZE)]
    detail_audiences = [a for a in audiences if a.get("audience_type") in
                        {"saved", "custom", "lookalike"}
                        and (not a.get("size") or int(a.get("size", 0)) < BROAD_AUDIENCE_MIN_SIZE)]
    advantage_plus = [a for a in audiences if a.get("is_advantage_plus")]

    audience_summary["broad_count"] = len(broad_audiences)
    audience_summary["detail_count"] = len(detail_audiences)
    audience_summary["advantage_plus_count"] = len(advantage_plus)

    if not audiences:
        checks.append(_make_check(
            "M24", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="audiences 데이터 미제공 — 광범위·상세 타깃 분리 진단 불가",
        ))
    elif broad_audiences and detail_audiences:
        checks.append(_make_check(
            "M24", CheckStatus.PASS, SeverityLevel.MEDIUM,
            description=f"광범위 {len(broad_audiences)}개·상세 {len(detail_audiences)}개 분리 운용 확인",
        ))
    elif advantage_plus:
        checks.append(_make_check(
            "M24", CheckStatus.PASS, SeverityLevel.MEDIUM,
            description=f"Advantage+ {len(advantage_plus)}개 운용 — 한국 시장 권장",
        ))
    else:
        checks.append(_make_check(
            "M24", CheckStatus.WARNING, SeverityLevel.MEDIUM,
            description="광범위·상세 타깃 분리 또는 Advantage+ 운용 미감지",
            expected_impact="타깃 다변화 미흡 — 알고리즘 탐색 폭 제한 가능",
            remediation_option=(
                "Advantage+ 적극 활용 또는 광범위·상세 타깃 광고 세트 분리 검토 권장. "
                "한국 시장 2026 Meta 가이드 — Advantage+ 권장."
            ),
        ))

    # ============================================================
    # M-TH1: Threshold 변화 영향도 (2026 Meta 업데이트)
    # cross-reference: audit_andromeda_emq의 M-TH1과 동일 키
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
            expected_impact="한국 일부 광고주 미인지 — Threshold 변경에 따른 노출·전환 변동 대응 부재 가능",
            remediation_option=(
                "Meta 공식 2026 Threshold 변경 가이드 확인 검토 권장. "
                "Advantage+ Audience 전환 결정 시점·기존 오디언스 영향도 평가 권장."
            ),
        ))
    else:
        checks.append(_make_check(
            "M-TH1", CheckStatus.NA, SeverityLevel.HIGH,
            description="threshold_changes_acknowledged 데이터 미제공",
        ))

    # ============================================================
    # 카테고리 점수 계산
    # ============================================================
    score_result: WeightedScoreResult = calculate_weighted_score(checks)
    cat_score = next(
        (cs.raw_score for cs in score_result.category_scores
         if cs.category == CategoryName.AUDIENCE),
        0.0,
    )

    return AuditAudienceTargetingOutput(
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
        overlap_summary=overlap_summary,
        audience_summary=audience_summary,
    )
