"""
generate_quick_wins 도구 — REQ-AUDIT-MCP-013.
Critical/High severity + 추정 조치 소요 <15분 항목 필터 + 한국어 조치 가이드.

Attribution:
    Quick Wins logic adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    15-min threshold cited from NOTICE.md (classification threshold, not time prediction).
    See NOTICE.md §"agricidaniel/claude-ads (MIT)".

주의:
    REQ-AUDIT-MCP-013: "15분"은 claude-ads 원전 분류 기준값 (시간 예측 아님).
    REQ-AUDIT-MCP-022 예외 1.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


# ============================================================
# 체크별 조치 소요 추정값 (분류 기준값, REQ-AUDIT-MCP-022 예외)
# ============================================================

# @MX:ANCHOR: [AUTO] Quick Win 체크별 조치 소요 SSOT — generate_quick_wins·tests 공통 참조
# @MX:REASON: REQ-AUDIT-MCP-013 분류 기준값 (시간 예측 아님). 변경 시 SPEC §3.4 동기 갱신 필수.
# 분 단위: 광고관리자 UI에서 설정 변경에 필요한 추정 시간
CHECK_EFFORT_MINUTES: dict[str, int] = {
    # Pixel/CAPI Health — 일부는 개발자 작업 필요 (15+ 분)
    "M01": 5,    # Pixel 설치 확인 (UI 점검)
    "M02": 30,   # event_id 매칭 (개발자 작업)
    "M03": 30,   # EMQ Purchase 개선 (개발자 작업)
    "M04": 30,   # EMQ AddToCart
    "M05": 30,   # EMQ PageView
    "M06": 10,   # AEM top 8 events (광고관리자 UI)
    "M07": 60,   # em (email hash) — 개발자 작업
    "M08": 60,   # ph (phone hash)
    "M09": 60,   # external_id — 개발자 작업
    "M10": 120,  # Server-Side CAPI — 인프라 작업

    # Creative Diversity & Fatigue — 광고관리자 UI 작업
    "M25": 10,   # Andromeda Similarity (소재 추가)
    "M26": 5,    # 헤드라인 다양성 (UI 카피 변경)
    "M27": 5,    # primary text 다양성
    "M28": 5,    # CTA 다양성
    "M29": 10,   # 미디어 타입 (image 추가)
    "M30": 10,   # 미디어 타입 (video 추가)
    "M31": 10,   # 미디어 타입 (carousel 추가)
    "M32": 10,   # 미디어 타입 (collection 추가)
    "M-CR1": 5,  # 빈도 캡 조정 (UI 설정)
    "M-CR2": 15, # 노후화 소재 교체 결정
    "M-CR3": 10, # A/B 표본 통폐합 결정
    "M-CR4": 30, # UGC 비중 확대 (소재 수집·검수)

    # Account Structure — 광고관리자 UI 작업
    "M11": 15,   # Learning Limited 통폐합
    "M12": 10,   # 학습 통과 세트 확인
    "M13": 5,    # 학습 진행 상태 점검
    "M14": 10,   # 일예산 조정
    "M15": 15,   # CBO/ABO 정합성 결정
    "M16": 5,    # 캠페인 목표 설정
    "M17": 10,   # 예산 분배 조정
    "M18": 5,    # Audience Network 배제 (UI 토글)
    "M-ST1": 15, # 캠페인 통폐합 우선순위 결정
    "M-ST2": 10, # 예산 조정 (단가 × 3)

    # Audience & Targeting
    "M19": 10,   # overlap 통폐합 결정
    "M20": 5,    # overlap 진단 도구 활용
    "M21": 30,   # LAL seed 확장 (Custom Audience 작업)
    "M22": 15,   # LAL seed 유형 다양화
    "M23": 10,   # Custom Audience 갱신
    "M24": 10,   # Advantage+ 활성화 (UI 토글)
    "M-TH1": 15, # Threshold 변경 가이드 확인

    # Andromeda & Platform Changes
    "M-AN1": 30, # Andromeda 점수 개선 (소재 작업)
    "M-AT1": 10, # Advantage+ Targeting 전환
    "M-IA1": 5,  # Incremental Attribution 활성화 (UI 토글)

    # Korean Compliance
    "PIPA-001": 30,
    "ITNA-001": 15,
    "ECOM-001": 30,
    "ADV-001": 15,
    "MFDS-001": 60,
}

# 기본값 (체크 ID 미등록 시)
DEFAULT_EFFORT_MINUTES = 30

# Quick Win 분류 기준값 (claude-ads v1.5.1)
DEFAULT_QUICK_WIN_THRESHOLD_MINUTES = 15

# Quick Win 대상 severity (claude-ads v1.5.1)
QUICK_WIN_SEVERITIES = {"Critical", "High"}


class GenerateQuickWinsInput(BaseModel):
    """generate_quick_wins 도구 입력 스키마."""

    audit_results: dict = Field(
        description=(
            "전체 audit 결과 딕셔너리. 다음 키 중 1개 이상 포함: "
            "pixel_capi_result, creative_result, account_structure_result, "
            "audience_result, andromeda_result, compliance_results. "
            "각 값은 {checks: [{check_id, status, severity, ...}]} 구조."
        ),
    )
    threshold_minutes: int = Field(
        default=DEFAULT_QUICK_WIN_THRESHOLD_MINUTES,
        description=(
            f"Quick Win 분류 기준값 (기본 {DEFAULT_QUICK_WIN_THRESHOLD_MINUTES}분, claude-ads 원전). "
            "주의: 분류 기준값 — 시간 예측 아님 (REQ-AUDIT-MCP-022 예외 1)."
        ),
    )


class GenerateQuickWinsOutput(BaseModel):
    """generate_quick_wins 도구 출력 스키마."""

    quick_wins: list[dict] = Field(
        description=(
            "Quick Win 항목 리스트. 각 항목: "
            "{check_id, severity, category, description, expected_impact, "
            "remediation_option, effort_minutes (분류 기준값), priority_rank}"
        ),
    )
    total_count: int = Field(description="Quick Win 총 개수")
    by_severity: dict = Field(description="severity별 Quick Win 개수")
    by_category: dict = Field(description="카테고리별 Quick Win 개수")
    threshold_minutes_used: int = Field(description="실제 사용된 임계값")
    threshold_note: str = Field(
        default=(
            "임계값은 claude-ads v1.5.1 원전 분류 기준값으로, "
            "실제 조치 시간 예측이 아닙니다 (REQ-AUDIT-MCP-022 예외 1)."
        ),
    )


def _collect_checks(audit_results: dict) -> list[tuple[dict, str]]:
    """
    audit_results 딕셔너리에서 모든 check를 평탄화.

    Returns:
        list of (check_dict, category_name)
    """
    collected: list[tuple[dict, str]] = []
    category_keys = {
        "pixel_capi_result": "pixel_capi",
        "creative_result": "creative",
        "account_structure_result": "account_structure",
        "audience_result": "audience",
        "andromeda_result": "andromeda",
        "andromeda_emq_result": "andromeda",
    }
    for key, cat_name in category_keys.items():
        result = audit_results.get(key)
        if not isinstance(result, dict):
            continue
        for c in result.get("checks") or []:
            if isinstance(c, dict):
                collected.append((c, cat_name))

    # Compliance results (5개 한국 규제)
    compliance = audit_results.get("compliance_results") or audit_results.get("korean_compliance_result")
    if isinstance(compliance, dict):
        for c in compliance.get("checks") or []:
            if isinstance(c, dict):
                collected.append((c, "compliance"))
    elif isinstance(compliance, list):
        for c in compliance:
            if isinstance(c, dict):
                collected.append((c, "compliance"))

    # 최상위 checks (audit_meta_account 직접 출력 등)
    for c in audit_results.get("checks") or []:
        if isinstance(c, dict):
            collected.append((c, "unknown"))

    return collected


def _severity_rank(severity: str) -> int:
    """severity 우선순위 정렬 키. 작을수록 우선."""
    return {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}.get(severity, 9)


def generate_quick_wins_impl(
    inp: GenerateQuickWinsInput,
) -> GenerateQuickWinsOutput:
    """
    Quick Win 항목 추출.

    REQ-AUDIT-MCP-013: Critical/High severity + 추정 조치 소요 <threshold_minutes 필터.
    각 항목에 (check ID·심각도·예상 영향·한국어 조치 가이드) 포함.
    REQ-AUDIT-MCP-021: 단정적 명령 금지.
    REQ-AUDIT-MCP-022 예외 1: "15분" 임계값은 분류 기준값.
    """
    all_checks = _collect_checks(inp.audit_results)
    quick_wins: list[dict] = []
    by_severity: dict[str, int] = {"Critical": 0, "High": 0}
    by_category: dict[str, int] = {}

    for check, category in all_checks:
        severity = check.get("severity", "Medium")
        if severity not in QUICK_WIN_SEVERITIES:
            continue
        status = check.get("status")
        # PASS는 quick win 대상 아님 (이미 충족)
        if status == "PASS":
            continue

        check_id = check.get("check_id", "UNKNOWN")
        effort = CHECK_EFFORT_MINUTES.get(check_id, DEFAULT_EFFORT_MINUTES)
        # 임계값 미만만 quick win
        if effort > inp.threshold_minutes:
            continue

        quick_wins.append({
            "check_id": check_id,
            "severity": severity,
            "category": category,
            "status": status,
            "description": check.get("description", ""),
            "expected_impact": check.get("expected_impact", ""),
            "remediation_option": check.get("remediation_option", ""),
            "effort_minutes": effort,
            "effort_note": (
                f"분류 기준값 {effort}분 — 실제 시간 예측 아님 (claude-ads 원전 인용)"
            ),
        })
        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_category[category] = by_category.get(category, 0) + 1

    # 우선순위 정렬: severity → effort → check_id
    quick_wins.sort(key=lambda q: (
        _severity_rank(q["severity"]),
        q["effort_minutes"],
        q["check_id"],
    ))

    # priority_rank 부여
    for rank, q in enumerate(quick_wins, start=1):
        q["priority_rank"] = rank

    return GenerateQuickWinsOutput(
        quick_wins=quick_wins,
        total_count=len(quick_wins),
        by_severity=by_severity,
        by_category=by_category,
        threshold_minutes_used=inp.threshold_minutes,
    )
