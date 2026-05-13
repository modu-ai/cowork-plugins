"""
audit_meta_account 도구 — REQ-AUDIT-MCP-006.
4 카테고리 합산 health score + A-F 등급 + 카테고리별 분해 반환.

이 도구는 audit 마스터 진입점으로,
Pixel/CAPI·Creative·Account Structure·Audience 4 카테고리를 오케스트레이션한다.
v1에서는 Pixel/CAPI 도구를 직접 호출하고 나머지 3종은 placeholder를 반환한다.

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    See NOTICE.md §"agricidaniel/claude-ads (MIT)".
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from moai_ads_audit.parsers.xlsx import XlsxParseOutput, parse_xlsx_files
from moai_ads_audit.scoring.weighted import (
    CategoryName,
    CheckResult,
    CheckStatus,
    SeverityLevel,
    WeightedScoreResult,
    calculate_weighted_score,
)
from moai_ads_audit.tools.audit_pixel_capi import (
    AuditPixelCapiInput,
    AuditPixelCapiOutput,
    audit_pixel_capi_impl,
)
from moai_ads_audit.tools.calculate_health_score import (
    CalculateHealthScoreInput,
    CalculateHealthScoreOutput,
    _GRADE_KR_LABELS,
    calculate_health_score_impl,
)


class AuditMetaAccountInput(BaseModel):
    """audit_meta_account 도구 입력 스키마."""

    scope: str = Field(
        default="account",
        description="audit 범위 ('account' | 'campaign' | 'adset')",
    )
    time_range: str = Field(
        description="분석 기간 라벨 (예: '2026-03 ~ 2026-04')"
    )
    xlsx_path: str | None = Field(
        default=None,
        description=".xlsx 보고서 경로 (Layer 1 외부 MCP 비활성 시 fallback)",
    )
    # Pixel/CAPI 관련 선택 입력
    pixel_id: str | None = Field(
        default=None,
        description="Meta Pixel ID (선택 — 없으면 xlsx에서 추정)",
    )
    emq_scores: dict[str, float] | None = Field(
        default=None,
        description="이벤트별 EMQ 점수 직접 입력 (선택)",
    )
    capi_enabled: bool | None = Field(
        default=None,
        description="Server-Side CAPI 활성 여부 (선택)",
    )
    has_em_hash: bool | None = Field(default=None, description="em 해시화 여부")
    has_ph_hash: bool | None = Field(default=None, description="ph 해시화 여부")
    has_external_id: bool | None = Field(default=None, description="external_id 적용 여부")


class AuditMetaAccountOutput(BaseModel):
    """audit_meta_account 도구 출력 스키마."""

    scope: str
    time_range: str
    # 합산 점수 + 등급
    total_score: float = Field(description="0-100 가중치 합산 점수")
    grade: str = Field(description="A-F 등급")
    grade_kr_label: str = Field(description="한국 시장 등급 표현 (Layer 3 렌더링 권장)")
    # 카테고리별 분해
    category_scores: dict[str, float] = Field(description="카테고리별 0-100 점수")
    # 각 카테고리 check 결과 요약
    pixel_capi_result: dict = Field(description="Pixel/CAPI audit 결과 (M01-M10)")
    creative_result: dict = Field(description="Creative audit 결과 (라운드 4 예정)")
    account_structure_result: dict = Field(description="Account Structure audit 결과 (라운드 4 예정)")
    audience_result: dict = Field(description="Audience audit 결과 (라운드 4 예정)")
    # xlsx 파싱 요약 (있다면)
    xlsx_summary: dict | None = Field(default=None, description="xlsx 파싱 요약")
    # Attribution (REQ-AUDIT-MCP-003)
    attribution: str = Field(
        default=(
            "Methodology adapted from agricidaniel/claude-ads v1.5.1 under MIT. "
            "See .claude/rules/moai/NOTICE.md §'agricidaniel/claude-ads (MIT)'."
        )
    )


# ============================================================
# v1 placeholder — Creative·Account·Audience 카테고리
# 라운드 4에서 각각 전용 도구로 분리 구현 예정
# ============================================================

def _placeholder_category_checks(
    category: CategoryName,
    check_ids: list[str],
    default_severity: SeverityLevel = SeverityLevel.MEDIUM,
) -> list[CheckResult]:
    """
    라운드 4 미구현 카테고리에 대한 N/A placeholder check 생성.
    N/A 상태는 점수 계산에서 제외되므로 합산에 영향 없음.
    """
    return [
        CheckResult(
            check_id=cid,
            status=CheckStatus.NA,
            severity=default_severity,
            category=category,
            description=f"{cid}: 라운드 4 구현 예정 (현재 N/A)",
        )
        for cid in check_ids
    ]


# Creative 카테고리 check ID 목록 (M25-M32 + M-CR1~4)
CREATIVE_CHECK_IDS = [
    "M25", "M26", "M27", "M28", "M29", "M30", "M31", "M32",
    "M-CR1", "M-CR2", "M-CR3", "M-CR4",
]

# Account Structure 카테고리 check ID 목록 (M11-M18 + M-ST1~2)
ACCOUNT_STRUCTURE_CHECK_IDS = [
    "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18",
    "M-ST1", "M-ST2",
]

# Audience 카테고리 check ID 목록 (M19-M24 + M-TH1)
AUDIENCE_CHECK_IDS = [
    "M19", "M20", "M21", "M22", "M23", "M24", "M-TH1",
]


def audit_meta_account_impl(inp: AuditMetaAccountInput) -> AuditMetaAccountOutput:
    """
    Meta 계정 전체 audit 오케스트레이션.

    REQ-AUDIT-MCP-006: 4 카테고리 합산 점수 + A-F 등급 + 카테고리별 분해.
    REQ-AUDIT-MCP-005: xlsx fallback 지원.
    REQ-AUDIT-MCP-021: 단정적 명령 금지.

    Args:
        inp: AuditMetaAccountInput

    Returns:
        AuditMetaAccountOutput
    """
    # xlsx 파싱 (있다면)
    xlsx_summary: dict | None = None
    if inp.xlsx_path:
        xlsx_out: XlsxParseOutput = parse_xlsx_files([inp.xlsx_path])
        if xlsx_out.blocker:
            # 블로커 발생 — 부분 결과 반환 (도구는 계속 실행)
            xlsx_summary = {
                "status": "blocker",
                "message": xlsx_out.blocker,
                "rows_parsed": 0,
            }
        else:
            xlsx_summary = {
                "status": "ok",
                "rows_parsed": len(xlsx_out.merged_rows),
                "report_type": xlsx_out.validation.report_type,
                "spend_total": xlsx_out.validation.spend_total,
                "purchases_total": xlsx_out.validation.purchases_total,
                "validation_errors": xlsx_out.validation.errors,
                "validation_warnings": xlsx_out.validation.warnings,
            }

    # ============================================================
    # Pixel/CAPI audit (M01-M10) — 구현 완료
    # ============================================================
    pixel_inp = AuditPixelCapiInput(
        pixel_id=inp.pixel_id or "",
        event_log=[],
        xlsx_path=inp.xlsx_path,
        emq_scores=inp.emq_scores,
        capi_enabled=inp.capi_enabled,
        has_em_hash=inp.has_em_hash,
        has_ph_hash=inp.has_ph_hash,
        has_external_id=inp.has_external_id,
    )
    pixel_result: AuditPixelCapiOutput = audit_pixel_capi_impl(pixel_inp)

    # Pixel/CAPI check 결과를 CheckResult로 변환 (합산 공식 입력)
    pixel_checks: list[CheckResult] = [
        CheckResult(
            check_id=c["check_id"],
            status=CheckStatus(c["status"]),
            severity=SeverityLevel(c["severity"]),
            category=CategoryName.PIXEL_CAPI,
            description=c.get("description", ""),
            expected_impact=c.get("expected_impact", ""),
            remediation_option=c.get("remediation_option", ""),
        )
        for c in pixel_result.checks
    ]

    # ============================================================
    # Creative·Account·Audience — v1 N/A placeholder (라운드 4 예정)
    # ============================================================
    creative_checks = _placeholder_category_checks(
        CategoryName.CREATIVE, CREATIVE_CHECK_IDS, SeverityLevel.HIGH
    )
    account_checks = _placeholder_category_checks(
        CategoryName.ACCOUNT_STRUCTURE, ACCOUNT_STRUCTURE_CHECK_IDS, SeverityLevel.HIGH
    )
    audience_checks = _placeholder_category_checks(
        CategoryName.AUDIENCE, AUDIENCE_CHECK_IDS, SeverityLevel.HIGH
    )

    # ============================================================
    # 전체 합산 (4 카테고리)
    # ============================================================
    all_checks = pixel_checks + creative_checks + account_checks + audience_checks
    score_result: WeightedScoreResult = calculate_weighted_score(all_checks)

    # 카테고리별 점수 추출
    cat_score_map: dict[str, float] = {
        cs.category.value: cs.raw_score for cs in score_result.category_scores
    }

    # Creative·Account·Audience는 모두 N/A이므로 점수 = 0 (공식 제외)
    # Pixel/CAPI 점수만 실질 합산에 기여 (v1)
    # Layer 3가 사용자에게 "라운드 4 구현 후 전체 합산" 안내 책임

    return AuditMetaAccountOutput(
        scope=inp.scope,
        time_range=inp.time_range,
        total_score=score_result.total_score,
        grade=score_result.grade,
        grade_kr_label=_GRADE_KR_LABELS.get(score_result.grade, "알 수 없음"),
        category_scores={
            "pixel_capi": cat_score_map.get(CategoryName.PIXEL_CAPI.value, 0.0),
            "creative": cat_score_map.get(CategoryName.CREATIVE.value, 0.0),
            "account_structure": cat_score_map.get(CategoryName.ACCOUNT_STRUCTURE.value, 0.0),
            "audience": cat_score_map.get(CategoryName.AUDIENCE.value, 0.0),
        },
        pixel_capi_result={
            "category_score": pixel_result.category_score,
            "pass_count": pixel_result.pass_count,
            "warning_count": pixel_result.warning_count,
            "fail_count": pixel_result.fail_count,
            "na_count": pixel_result.na_count,
            "checks": pixel_result.checks,
            "emq_summary": pixel_result.emq_summary,
            "dedup_rate": pixel_result.dedup_rate,
        },
        creative_result={
            "status": "NOT_IMPLEMENTED_V1",
            "message": "Creative Diversity & Fatigue audit (M25-M32 + M-CR1~4) 라운드 4 구현 예정",
            "check_count": len(CREATIVE_CHECK_IDS),
        },
        account_structure_result={
            "status": "NOT_IMPLEMENTED_V1",
            "message": "Account Structure audit (M11-M18 + M-ST1~2) 라운드 4 구현 예정",
            "check_count": len(ACCOUNT_STRUCTURE_CHECK_IDS),
        },
        audience_result={
            "status": "NOT_IMPLEMENTED_V1",
            "message": "Audience & Targeting audit (M19-M24 + M-TH1) 라운드 4 구현 예정",
            "check_count": len(AUDIENCE_CHECK_IDS),
        },
        xlsx_summary=xlsx_summary,
    )
