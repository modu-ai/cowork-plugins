"""
audit_pixel_capi 도구 — REQ-AUDIT-MCP-007.
Pixel/CAPI Health 10개 check (M01-M10) 검사.

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    EMQ tiered targets: Purchase ≥8.5 / AddToCart ≥6.5 / PageView ≥5.5.
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
# EMQ 임계값 — SPEC §3.5, claude-ads v1.5.1 (NOTICE.md 직접 인용)
# ============================================================
# @MX:ANCHOR: [AUTO] EMQ 임계값 SSOT — audit_pixel_capi·tests·audit_andromeda_emq 공통 참조
# @MX:REASON: SPEC §3.5 "EMQ tiered targets" NOTICE.md 직접 인용값. 임의 변경 금지.
#             REQ-AUDIT-MCP-007 검증 조건.
EMQ_THRESHOLDS: dict[str, float] = {
    "Purchase": 8.5,
    "AddToCart": 6.5,
    "PageView": 5.5,
}

# dedup rate 임계값 — claude-ads v1.5.1 (NOTICE.md 직접 인용)
DEDUP_RATE_THRESHOLD = 0.90  # ≥90%

# AEM top 8 events — iOS 14.5+ 대응
AEM_TOP_8_EVENTS = [
    "Purchase", "AddToCart", "InitiateCheckout",
    "AddPaymentInfo", "Lead", "CompleteRegistration",
    "ViewContent", "Search",
]

# 키 파라미터 목록 — claude-ads v1.5.1 EMQ 키 파라미터
KEY_PARAMETERS = ["em", "ph", "external_id", "fbp", "fbc"]


class AuditPixelCapiInput(BaseModel):
    """audit_pixel_capi 도구 입력 스키마."""

    pixel_id: str = Field(description="Meta Pixel ID")
    event_log: list[dict] = Field(
        default_factory=list,
        description=(
            "CAPI 이벤트 로그 리스트 (선택 — Layer 1 MCP 출력). "
            "각 항목: {event_name, event_id, dedup_key, emq_score, parameters: {em, ph, external_id, fbp, fbc}, ...}"
        ),
    )
    xlsx_path: str | None = Field(
        default=None,
        description=".xlsx 보고서 경로 (Layer 1 비활성 시 fallback, REQ-AUDIT-MCP-005)",
    )
    # 직접 제공 EMQ 점수 (event_log 없는 경우 사용)
    emq_scores: dict[str, float] | None = Field(
        default=None,
        description="이벤트별 EMQ 점수 직접 입력. 예: {'Purchase': 8.2, 'AddToCart': 6.1}",
    )
    # CAPI 설정 정보
    capi_enabled: bool | None = Field(
        default=None,
        description="Server-Side CAPI 활성 여부 (M10)",
    )
    has_em_hash: bool | None = Field(
        default=None,
        description="em (email hash) 키 파라미터 적용 여부 (M07)",
    )
    has_ph_hash: bool | None = Field(
        default=None,
        description="ph (phone hash) 키 파라미터 적용 여부 (M08)",
    )
    has_external_id: bool | None = Field(
        default=None,
        description="external_id 키 파라미터 적용 여부 (M09)",
    )


class AuditPixelCapiOutput(BaseModel):
    """audit_pixel_capi 도구 출력 스키마."""

    pixel_id: str
    # 10개 check 결과
    checks: list[dict] = Field(description="M01-M10 check 결과 리스트")
    # 카테고리 점수
    category_score: float = Field(description="Pixel/CAPI 카테고리 0-100 점수")
    # 집계
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int
    # EMQ 요약
    emq_summary: dict = Field(description="이벤트별 EMQ 현황")
    # dedup rate
    dedup_rate: float | None = Field(description="CAPI dedup rate (N/A이면 null)")


def _make_check(
    check_id: str,
    status: CheckStatus,
    severity: SeverityLevel,
    description: str,
    expected_impact: str = "",
    remediation_option: str = "",
) -> CheckResult:
    """CheckResult 생성 헬퍼."""
    return CheckResult(
        check_id=check_id,
        status=status,
        severity=severity,
        category=CategoryName.PIXEL_CAPI,
        description=description,
        expected_impact=expected_impact,
        remediation_option=remediation_option,
    )


def audit_pixel_capi_impl(inp: AuditPixelCapiInput) -> AuditPixelCapiOutput:
    """
    Pixel/CAPI Health 10개 check (M01-M10) 실행.

    데이터 우선순위:
    1. event_log (Layer 1 MCP 실데이터)
    2. emq_scores + 직접 입력 필드 (부분 정보)
    3. xlsx_path fallback (REQ-AUDIT-MCP-005)
    4. 데이터 없음 → N/A

    REQ-AUDIT-MCP-007: PASS/WARNING/FAIL/N/A 4상태 반환.
    REQ-AUDIT-MCP-021: 단정적 명령 금지 — 시정 옵션 형식.
    """
    checks: list[CheckResult] = []
    emq_summary: dict = {}
    dedup_rate: float | None = None

    # event_log 집계
    events_by_name: dict[str, list[dict]] = {}
    if inp.event_log:
        for ev in inp.event_log:
            name = ev.get("event_name", "Unknown")
            events_by_name.setdefault(name, []).append(ev)

    # ============================================================
    # M01: Pixel 설치 확인 + PIPA 동의 배너
    # ============================================================
    if inp.pixel_id:
        checks.append(_make_check(
            "M01", CheckStatus.PASS, SeverityLevel.CRITICAL,
            description=f"Pixel ID {inp.pixel_id} 확인됨",
            remediation_option="PIPA 동의 배너 적용 여부 별도 확인 권장",
        ))
    else:
        checks.append(_make_check(
            "M01", CheckStatus.FAIL, SeverityLevel.CRITICAL,
            description="Pixel ID가 제공되지 않았습니다",
            expected_impact="Pixel 미설치 시 CAPI·EMQ·dedup 전체 비활성",
            remediation_option="Meta 광고관리자 → Events Manager에서 Pixel 설치 확인 검토 권장",
        ))

    # ============================================================
    # M02: event_id 매칭 (dedup rate ≥90%)
    # ============================================================
    if inp.event_log:
        # event_id 중복 감지로 dedup rate 추정
        all_event_ids = [ev.get("event_id") for ev in inp.event_log if ev.get("event_id")]
        unique_event_ids = set(all_event_ids)
        if len(all_event_ids) > 0:
            dedup_rate = len(unique_event_ids) / len(all_event_ids)
        if dedup_rate is not None and dedup_rate >= DEDUP_RATE_THRESHOLD:
            checks.append(_make_check(
                "M02", CheckStatus.PASS, SeverityLevel.CRITICAL,
                description=f"dedup rate {dedup_rate:.1%} — 임계값 {DEDUP_RATE_THRESHOLD:.0%} 충족",
            ))
        elif dedup_rate is not None:
            checks.append(_make_check(
                "M02", CheckStatus.FAIL, SeverityLevel.CRITICAL,
                description=f"dedup rate {dedup_rate:.1%} — 임계값 {DEDUP_RATE_THRESHOLD:.0%} 미달",
                expected_impact="Pixel·CAPI 중복 집계로 전환수 과대계상 가능",
                remediation_option=(
                    "Pixel 이벤트와 CAPI 이벤트에 동일한 event_id 설정 검토 권장. "
                    "Meta Events Manager dedup 진단 탭 확인 검토 권장."
                ),
            ))
        else:
            checks.append(_make_check(
                "M02", CheckStatus.NA, SeverityLevel.CRITICAL,
                description="dedup rate 산출 불가 (event_id 데이터 부족)",
            ))
    else:
        checks.append(_make_check(
            "M02", CheckStatus.NA, SeverityLevel.CRITICAL,
            description="event_log 미제공 — CAPI 이벤트 데이터 필요",
        ))

    # ============================================================
    # M03-M05: EMQ tiered targets (Purchase / AddToCart / PageView)
    # ============================================================
    emq_data = inp.emq_scores or {}
    if inp.event_log:
        for ev in inp.event_log:
            name = ev.get("event_name")
            score = ev.get("emq_score")
            if name and score is not None:
                emq_data[name] = float(score)

    for check_id, event_name, threshold, sev in [
        ("M03", "Purchase", EMQ_THRESHOLDS["Purchase"], SeverityLevel.HIGH),
        ("M04", "AddToCart", EMQ_THRESHOLDS["AddToCart"], SeverityLevel.HIGH),
        ("M05", "PageView", EMQ_THRESHOLDS["PageView"], SeverityLevel.HIGH),
    ]:
        score = emq_data.get(event_name)
        emq_summary[event_name] = {
            "score": score,
            "threshold": threshold,
            "status": "unknown",
        }
        if score is None:
            checks.append(_make_check(
                check_id, CheckStatus.NA, sev,
                description=f"EMQ {event_name} 점수 미제공",
            ))
            emq_summary[event_name]["status"] = "na"
        elif score >= threshold:
            checks.append(_make_check(
                check_id, CheckStatus.PASS, sev,
                description=f"EMQ {event_name} {score:.1f} — 임계값 ≥{threshold} 충족",
            ))
            emq_summary[event_name]["status"] = "pass"
        else:
            checks.append(_make_check(
                check_id, CheckStatus.FAIL, sev,
                description=f"EMQ {event_name} {score:.1f} — 임계값 ≥{threshold} 미달",
                expected_impact=f"EMQ 점수 {threshold - score:.1f} 부족 — 전환 최적화 효율 저하 가능",
                remediation_option=(
                    f"EMQ {event_name} 개선 검토: "
                    "em(+4.0)·ph(+3.0)·external_id·fbp·fbc 키 파라미터 적용 검토 권장."
                ),
            ))
            emq_summary[event_name]["status"] = "fail"

    # ============================================================
    # M06: AEM top 8 events 매핑 (iOS 14.5+ 대응)
    # ============================================================
    if events_by_name:
        mapped = [ev for ev in AEM_TOP_8_EVENTS if ev in events_by_name]
        if len(mapped) >= 4:
            checks.append(_make_check(
                "M06", CheckStatus.PASS, SeverityLevel.HIGH,
                description=f"AEM top 8 events 중 {len(mapped)}개 매핑 확인",
            ))
        else:
            checks.append(_make_check(
                "M06", CheckStatus.WARNING, SeverityLevel.HIGH,
                description=f"AEM top 8 events 중 {len(mapped)}개만 매핑 (권장: 최소 4개 이상)",
                expected_impact="iOS 14.5+ 환경 데이터 손실 가능 — AEM 이벤트 우선순위 설정 검토 권장",
                remediation_option=(
                    "Meta Events Manager → 이벤트 구성에서 AEM 우선순위 이벤트 8개 등록 검토 권장."
                ),
            ))
    else:
        checks.append(_make_check(
            "M06", CheckStatus.NA, SeverityLevel.HIGH,
            description="event_log 미제공 — AEM 매핑 확인 불가",
        ))

    # ============================================================
    # M07: em (email hash) 키 파라미터 (PIPA 해시화 권장)
    # ============================================================
    if inp.has_em_hash is True:
        checks.append(_make_check(
            "M07", CheckStatus.PASS, SeverityLevel.HIGH,
            description="em (SHA-256 hashed email) 키 파라미터 적용 확인",
        ))
    elif inp.has_em_hash is False:
        checks.append(_make_check(
            "M07", CheckStatus.WARNING, SeverityLevel.HIGH,
            description="em (email hash) 키 파라미터 미적용",
            expected_impact="EMQ 점수 최대 +4.0 향상 가능 (NOTICE.md EMQ optimization tiers 인용)",
            remediation_option=(
                "Pixel 이벤트에 SHA-256 hashed email (em) 추가 검토 권장. "
                "PIPA 개인정보 처리 동의 사전 확인 권장."
            ),
        ))
    else:
        checks.append(_make_check(
            "M07", CheckStatus.NA, SeverityLevel.HIGH,
            description="em 파라미터 적용 여부 미제공",
        ))

    # ============================================================
    # M08: ph (phone hash) 키 파라미터 (PIPA 해시화 권장)
    # ============================================================
    if inp.has_ph_hash is True:
        checks.append(_make_check(
            "M08", CheckStatus.PASS, SeverityLevel.MEDIUM,
            description="ph (SHA-256 hashed phone) 키 파라미터 적용 확인",
        ))
    elif inp.has_ph_hash is False:
        checks.append(_make_check(
            "M08", CheckStatus.WARNING, SeverityLevel.MEDIUM,
            description="ph (phone hash) 키 파라미터 미적용",
            expected_impact="EMQ 점수 최대 +3.0 향상 가능",
            remediation_option=(
                "Pixel 이벤트에 SHA-256 hashed phone (ph) 추가 검토 권장. "
                "PIPA 개인정보 처리 동의 사전 확인 권장."
            ),
        ))
    else:
        checks.append(_make_check(
            "M08", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="ph 파라미터 적용 여부 미제공",
        ))

    # ============================================================
    # M09: external_id / fbp / fbc 키 파라미터 (PIPA 식별자 보호)
    # ============================================================
    if inp.has_external_id is True:
        checks.append(_make_check(
            "M09", CheckStatus.PASS, SeverityLevel.MEDIUM,
            description="external_id 키 파라미터 적용 확인 (fbp·fbc 포함 권장)",
        ))
    elif inp.has_external_id is False:
        checks.append(_make_check(
            "M09", CheckStatus.WARNING, SeverityLevel.MEDIUM,
            description="external_id 키 파라미터 미적용",
            expected_impact="고객 매칭률 저하 가능 — CAPI 효율 감소",
            remediation_option=(
                "Pixel 이벤트에 external_id·fbp·fbc 파라미터 추가 검토 권장. "
                "PIPA 식별자 보호 준수 범위 내 적용 권장."
            ),
        ))
    else:
        checks.append(_make_check(
            "M09", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="external_id 파라미터 적용 여부 미제공",
        ))

    # ============================================================
    # M10: Server-Side CAPI 활성 여부 (iOS 14.5+ 데이터 손실 보전)
    # ============================================================
    if inp.capi_enabled is True:
        checks.append(_make_check(
            "M10", CheckStatus.PASS, SeverityLevel.HIGH,
            description="Server-Side CAPI 활성 확인 — iOS 14.5+ 데이터 손실 보전",
        ))
    elif inp.capi_enabled is False:
        checks.append(_make_check(
            "M10", CheckStatus.FAIL, SeverityLevel.HIGH,
            description="Server-Side CAPI 비활성",
            expected_impact="iOS 14.5+ ATT Opt-out 사용자 전환 데이터 손실 가능",
            remediation_option=(
                "Meta Conversions API (CAPI) 활성화 검토 권장. "
                "CAPI Gateway 또는 서버 직접 구현 옵션 비교 검토 권장."
            ),
        ))
    else:
        checks.append(_make_check(
            "M10", CheckStatus.NA, SeverityLevel.HIGH,
            description="CAPI 활성 여부 미제공",
        ))

    # ============================================================
    # 카테고리 점수 계산
    # ============================================================
    score_result: WeightedScoreResult = calculate_weighted_score(checks)
    # Pixel/CAPI 단일 카테고리 점수 추출
    pixel_cat_score = next(
        (cs.raw_score for cs in score_result.category_scores
         if cs.category == CategoryName.PIXEL_CAPI),
        0.0,
    )

    return AuditPixelCapiOutput(
        pixel_id=inp.pixel_id,
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
        category_score=pixel_cat_score,
        pass_count=score_result.pass_count,
        warning_count=score_result.warning_count,
        fail_count=score_result.fail_count,
        na_count=score_result.na_count,
        emq_summary=emq_summary,
        dedup_rate=dedup_rate,
    )
