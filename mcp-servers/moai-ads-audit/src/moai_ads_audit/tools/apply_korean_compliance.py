"""
apply_korean_compliance 도구 — REQ-AUDIT-MCP-015.
5개 한국 규제 검사 — PIPA·ITNA·전자상거래법·표시광고법·식약처 광고 심의.

Attribution:
    Korean regulations adapted from NOTICE.md §"Korean Market Adaptation" Area 3.
    식약처 강제 활성: 건강기능식품·의료기기·의약품 카테고리 시 (REQ-AUDIT-MCP-015).

주의:
    REQ-AUDIT-MCP-021: 단정적 명령 금지 — "검토 권장" 형식.
    REQ-AUDIT-MCP-022: ITNA 21시-08시는 법률 시간 정의 (예외).
    v1: 키워드 매칭 + 시정 가이드까지. 실제 심의 통과는 사용자 책임.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from moai_ads_audit.compliance.korean import (
    MFDS_REQUIRED_CATEGORIES,
    check_korean_compliance,
)


class ApplyKoreanComplianceInput(BaseModel):
    """apply_korean_compliance 도구 입력 스키마."""

    creative_text: str = Field(
        description=(
            "광고 소재 텍스트 — 카피·헤드라인·primary text·CTA·랜딩 페이지 텍스트 등 "
            "모든 광고 텍스트를 통합한 문자열. "
            "PIPA·표시광고법·식약처 등 텍스트 기반 검사 대상."
        ),
    )
    product_category: str = Field(
        description=(
            "제품 카테고리 — 식약처 심의 강제 활성 판단 기준. "
            "예: '식품/음료', '건강기능식품/의료', 'IT/디지털', '기타'. "
            "건강기능식품·의료기기·의약품 카테고리 시 식약처 검사 강제 활성화."
        ),
    )
    pixel_context: dict | None = Field(
        default=None,
        description=(
            "Pixel 설정 정보 (선택). PIPA em/ph 해시화 직접 검사용. "
            "{em_hashed: bool, ph_hashed: bool}"
        ),
    )


class ApplyKoreanComplianceOutput(BaseModel):
    """apply_korean_compliance 도구 출력 스키마."""

    checks: list[dict] = Field(
        description=(
            "5개 규제 검사 결과 리스트. 각 항목: "
            "{regulation, status (PASS/WARNING/FAIL), check_id, severity, "
            "description, expected_impact, remediation_option, matched_patterns}"
        ),
    )
    summary: dict = Field(
        description=(
            "전체 진단 요약: {pass_count, warning_count, fail_count, "
            "mfds_force_active, total_violations}"
        ),
    )
    mfds_force_active: bool = Field(
        description="식약처 심의 강제 활성 여부 (건강기능식품/의료 카테고리)",
    )
    attribution: str = Field(
        default=(
            "Korean regulations adapted from NOTICE.md §'Korean Market Adaptation' Area 3. "
            "v1: 키워드 매칭까지 자동, 실제 심의 통과는 사용자 책임."
        ),
    )


def apply_korean_compliance_impl(
    inp: ApplyKoreanComplianceInput,
) -> ApplyKoreanComplianceOutput:
    """
    5개 한국 규제 검사 실행 + 결과 + 한국어 시정 가이드 반환.

    REQ-AUDIT-MCP-015: 5개 규제 모두 검사 — PIPA·ITNA·전자상거래법·표시광고법·식약처.
    식품·건강기능식품 카테고리 시 식약처 심의 강제 활성화.
    REQ-AUDIT-MCP-021: 단정적 명령 금지.
    """
    # compliance/korean.py 호출 — _check_pixel_context 지원 추가 필요 시 후속 작업
    results = check_korean_compliance(
        creative_text=inp.creative_text,
        product_category=inp.product_category,
    )

    # pixel_context가 제공되면 PIPA check를 보강
    # (compliance/korean.py _check_pipa는 pixel_context 인자를 받지만 공개 진입점에서
    #  미전달 — 본 도구에서는 결과 후 보강만 수행하여 인터페이스 일관성 유지)
    if inp.pixel_context:
        for r in results:
            if r.regulation.value == "개인정보보호법":
                em_h = bool(inp.pixel_context.get("em_hashed", False))
                ph_h = bool(inp.pixel_context.get("ph_hashed", False))
                if em_h and ph_h:
                    # 해시화 확인되면 PIPA WARNING을 PASS로 격상 (보조 평가)
                    from moai_ads_audit.scoring.weighted import CheckStatus
                    if r.status != CheckStatus.PASS:
                        r.description += " | Pixel em·ph 해시화 확인 — 위험도 완화"
                        r.status = CheckStatus.PASS
                        r.remediation_option = ""

    # 식약처 강제 활성 판단
    mfds_force = any(
        cat in inp.product_category for cat in MFDS_REQUIRED_CATEGORIES
    ) or inp.product_category in MFDS_REQUIRED_CATEGORIES

    # 직렬화 + 요약
    pass_count = sum(1 for r in results if r.status.value == "PASS")
    warning_count = sum(1 for r in results if r.status.value == "WARNING")
    fail_count = sum(1 for r in results if r.status.value == "FAIL")
    total_violations = sum(len(r.matched_patterns) for r in results)

    return ApplyKoreanComplianceOutput(
        checks=[r.to_dict() for r in results],
        summary={
            "pass_count": pass_count,
            "warning_count": warning_count,
            "fail_count": fail_count,
            "mfds_force_active": mfds_force,
            "total_violations": total_violations,
            "total_checks": len(results),
        },
        mfds_force_active=mfds_force,
    )
