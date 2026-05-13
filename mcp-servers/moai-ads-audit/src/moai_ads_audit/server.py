"""
MCP stdio 서버 + 도구 10종 등록.
FastMCP를 사용하여 도구를 선언적으로 등록한다.

REQ-AUDIT-MCP-001: stdio 실행 가능
REQ-AUDIT-MCP-004: 도구 10종 전체 노출
REQ-AUDIT-MCP-017: v1 = Meta 단독, TikTok·Naver·Kakao 노출 금지

v0.2.0 (라운드 4): 10종 도구 전체 구현 완료.
"""
from mcp.server.fastmcp import FastMCP

from moai_ads_audit import __version__
from moai_ads_audit.tools.audit_meta_account import (
    AuditMetaAccountInput,
    AuditMetaAccountOutput,
    audit_meta_account_impl,
)
from moai_ads_audit.tools.audit_pixel_capi import (
    AuditPixelCapiInput,
    AuditPixelCapiOutput,
    audit_pixel_capi_impl,
)
from moai_ads_audit.tools.audit_creative_diversity import (
    AuditCreativeDiversityInput,
    AuditCreativeDiversityOutput,
    audit_creative_diversity_impl,
)
from moai_ads_audit.tools.audit_account_structure import (
    AuditAccountStructureInput,
    AuditAccountStructureOutput,
    audit_account_structure_impl,
)
from moai_ads_audit.tools.audit_audience_targeting import (
    AuditAudienceTargetingInput,
    AuditAudienceTargetingOutput,
    audit_audience_targeting_impl,
)
from moai_ads_audit.tools.audit_andromeda_emq import (
    AuditAndromedaEmqInput,
    AuditAndromedaEmqOutput,
    audit_andromeda_emq_impl,
)
from moai_ads_audit.tools.calculate_health_score import (
    CalculateHealthScoreInput,
    CalculateHealthScoreOutput,
    calculate_health_score_impl,
)
from moai_ads_audit.tools.generate_quick_wins import (
    GenerateQuickWinsInput,
    GenerateQuickWinsOutput,
    generate_quick_wins_impl,
)
from moai_ads_audit.tools.apply_korean_benchmarks import (
    ApplyKoreanBenchmarksInput,
    ApplyKoreanBenchmarksOutput,
    apply_korean_benchmarks_impl,
)
from moai_ads_audit.tools.apply_korean_compliance import (
    ApplyKoreanComplianceInput,
    ApplyKoreanComplianceOutput,
    apply_korean_compliance_impl,
)

# MCP 서버 인스턴스 — stdio 트랜스포트 기본값
# @MX:NOTE: [AUTO] FastMCP 생성자는 version 파라미터를 지원하지 않음 (mcp>=1.0.0 호환)
mcp = FastMCP(
    name=f"moai-ads-audit-mcp/{__version__}",
)


# ============================================================
# 도구 10종 (라운드 3 + 4 통합 구현 완료, v0.2.0)
# ============================================================


@mcp.tool()
def audit_meta_account(
    scope: str,
    time_range: str,
    xlsx_path: str | None = None,
    pixel_id: str | None = None,
    ads_data: list[dict] | None = None,
    campaigns: list[dict] | None = None,
    audiences: list[dict] | None = None,
    lookalike_seeds: list[dict] | None = None,
) -> dict:
    """
    Meta 광고 계정 전체 audit — 4 카테고리 합산 점수 + A-F 등급 반환.

    REQ-AUDIT-MCP-006: 4 카테고리 (Pixel/CAPI 30% + Creative 30% +
    Account Structure 20% + Audience 20%) 합산 health score (0-100) + A-F 등급.

    v0.2.0: Creative·Account·Audience 4개 카테고리 모두 실제 audit 호출.
    데이터 미제공 시 자동 N/A (합산 공식에서 제외).

    Args:
        scope: audit 범위 ("account" | "campaign" | "adset")
        time_range: 분석 기간 라벨 (예: "2026-03 ~ 2026-04")
        xlsx_path: .xlsx 보고서 경로 (Layer 1 외부 MCP 비활성 시 fallback)
        pixel_id: Meta Pixel ID (선택)
        ads_data: Creative audit용 광고 소재 데이터 (선택)
        campaigns: Account Structure audit용 캠페인 데이터 (선택)
        audiences: Audience audit용 오디언스 데이터 (선택)
        lookalike_seeds: Lookalike seed 데이터 (선택)

    Returns:
        4 카테고리 합산 점수 + A-F 등급 + 카테고리별 분해 JSON
    """
    inp = AuditMetaAccountInput(
        scope=scope,
        time_range=time_range,
        xlsx_path=xlsx_path,
        pixel_id=pixel_id,
        ads_data=ads_data,
        campaigns=campaigns,
        audiences=audiences,
        lookalike_seeds=lookalike_seeds,
    )
    result: AuditMetaAccountOutput = audit_meta_account_impl(inp)
    return result.model_dump()


@mcp.tool()
def audit_pixel_capi(
    pixel_id: str,
    event_log: list[dict] | None = None,
    xlsx_path: str | None = None,
) -> dict:
    """
    Pixel/CAPI Health 10개 check (M01-M10) — PASS/WARNING/FAIL/N/A 4상태 반환.

    REQ-AUDIT-MCP-007: event_id 매칭 / EMQ tiered targets
    (Purchase ≥8.5 / AddToCart ≥6.5 / PageView ≥5.5) / dedup rate ≥90% /
    AEM top 8 events / em·ph·external_id·fbp·fbc 키 파라미터 검사.

    Args:
        pixel_id: Meta Pixel ID
        event_log: CAPI 이벤트 로그 리스트 (선택, Layer 1 MCP 출력)
        xlsx_path: .xlsx 보고서 경로 (Layer 1 비활성 시 fallback)

    Returns:
        10개 check 결과 (PASS/WARNING/FAIL/N/A) + 카테고리 점수 JSON
    """
    inp = AuditPixelCapiInput(
        pixel_id=pixel_id,
        event_log=event_log or [],
        xlsx_path=xlsx_path,
    )
    result: AuditPixelCapiOutput = audit_pixel_capi_impl(inp)
    return result.model_dump()


@mcp.tool()
def audit_creative_diversity(
    ads_data: list[dict],
    time_window: str = "",
) -> dict:
    """
    Creative Diversity & Fatigue 12개 check (M25-M32 + M-CR1~4).

    REQ-AUDIT-MCP-008: Andromeda Similarity <60% / 빈도 임계값 3.0 /
    헤드라인·primary text·CTA·미디어 4축 다양성 / 소재 노후화 진단 (2개월 연속 ROAS 하락) /
    A/B 테스트 표본 크기 (≥1000) / UGC 비율 (≥20%).

    Args:
        ads_data: 광고 소재 데이터 리스트
        time_window: 분석 기간 라벨

    Returns:
        12개 check 결과 + 다양성·노후화 진단 요약 JSON
    """
    inp = AuditCreativeDiversityInput(
        ads_data=ads_data or [],
        time_window=time_window,
    )
    result: AuditCreativeDiversityOutput = audit_creative_diversity_impl(inp)
    return result.model_dump()


@mcp.tool()
def audit_account_structure(
    campaigns: list[dict],
    time_range: str = "",
) -> dict:
    """
    Account Structure 10개 check (M11-M18 + M-ST1~2).

    REQ-AUDIT-MCP-009: Learning Limited <30% / CBO vs ABO 결정 /
    캠페인 목표·예산·노출 위치 정합성 / 광고 세트 수 적정성 (≤5) /
    캠페인 통폐합 우선순위 / 예산 적정성 (단가 × 3).

    Args:
        campaigns: 캠페인 데이터 리스트
        time_range: 분석 기간 라벨

    Returns:
        10개 check 결과 + Learning Limited 비율 + 구조 진단 요약 JSON
    """
    inp = AuditAccountStructureInput(
        campaigns=campaigns or [],
        time_range=time_range,
    )
    result: AuditAccountStructureOutput = audit_account_structure_impl(inp)
    return result.model_dump()


@mcp.tool()
def audit_audience_targeting(
    audiences: list[dict],
    lookalike_seeds: list[dict] | None = None,
    threshold_changes_acknowledged: bool | None = None,
) -> dict:
    """
    Audience & Targeting 7개 check (M19-M24 + M-TH1).

    REQ-AUDIT-MCP-010: audience overlap <20% / Lookalike seed quality (≥1000명) /
    Custom Audience 신선도 (≤180일) / 광범위 vs 상세 타깃 분리 (Advantage+ 권장) /
    Threshold 변화 영향도 (2026 Meta).

    Args:
        audiences: 타깃 오디언스 리스트
        lookalike_seeds: Lookalike 시드 오디언스 리스트 (선택)
        threshold_changes_acknowledged: 2026 Threshold 변경 인지 여부 (M-TH1)

    Returns:
        7개 check 결과 + overlap·오디언스 진단 요약 JSON
    """
    inp = AuditAudienceTargetingInput(
        audiences=audiences or [],
        lookalike_seeds=lookalike_seeds or [],
        threshold_changes_acknowledged=threshold_changes_acknowledged,
    )
    result: AuditAudienceTargetingOutput = audit_audience_targeting_impl(inp)
    return result.model_dump()


@mcp.tool()
def audit_andromeda_emq(
    pixel_events: list[dict] | None = None,
    ads_data: list[dict] | None = None,
    threshold_changes_acknowledged: bool | None = None,
) -> dict:
    """
    Andromeda & Platform Changes 4개 check (M-AN1·M-AT1·M-IA1·M-TH1).

    REQ-AUDIT-MCP-011: 2026 Meta 플랫폼 업데이트 영향도 진단 —
    Andromeda 알고리즘 / Advantage+ Targeting / Incremental Attribution / Threshold.
    카테고리 가중치 = 0 (정보 제공 — 합산 기여 없음).

    Args:
        pixel_events: Pixel 이벤트 데이터 리스트 (선택)
        ads_data: 광고 데이터 리스트 (선택)
        threshold_changes_acknowledged: 2026 Threshold 변경 인지 여부

    Returns:
        4개 check 결과 + 진단 점수 + 2026 Meta 4종 업데이트 영향도 JSON
    """
    inp = AuditAndromedaEmqInput(
        pixel_events=pixel_events or [],
        ads_data=ads_data or [],
        threshold_changes_acknowledged=threshold_changes_acknowledged,
    )
    result: AuditAndromedaEmqOutput = audit_andromeda_emq_impl(inp)
    return result.model_dump()


@mcp.tool()
def calculate_health_score(
    category_results: dict,
    severity_map: dict | None = None,
) -> dict:
    """
    가중치 스코어링 공식으로 0-100 점수 + A-F 등급 산출.

    REQ-AUDIT-MCP-012: S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
    Severity multiplier: Critical 5.0× / High 3.0× / Medium 1.5× / Low 0.5×
    카테고리 가중치: Pixel/CAPI 30% / Creative 30% / Account Structure 20% / Audience 20%
    A-F 등급: A 90+ / B 75-89 / C 60-74 / D 40-59 / F <40

    Args:
        category_results: 카테고리별 check 결과 딕셔너리
        severity_map: check ID별 심각도 오버라이드 (선택)

    Returns:
        0-100 점수 + A-F 등급 + 카테고리 분해 JSON
    """
    inp = CalculateHealthScoreInput(
        category_results=category_results,
        severity_map=severity_map or {},
    )
    result: CalculateHealthScoreOutput = calculate_health_score_impl(inp)
    return result.model_dump()


@mcp.tool()
def generate_quick_wins(
    audit_results: dict,
    threshold_minutes: int = 15,
) -> dict:
    """
    Quick Win 항목 리스트 + 한국어 조치 가이드 반환.

    REQ-AUDIT-MCP-013: Critical/High severity + 추정 조치 소요 <15분 항목만 추출.
    각 항목: check ID·심각도·예상 영향·조치 가이드 한국어 텍스트.
    주의: "15분"은 claude-ads 원전 분류 기준값 (시간 예측 아님, REQ-AUDIT-MCP-022 예외).

    Args:
        audit_results: 전체 audit 결과 딕셔너리
        threshold_minutes: Quick Win 분류 기준값 (기본값: 15, claude-ads 원전)

    Returns:
        Quick Win 항목 리스트 + 한국어 조치 가이드 + 우선순위 JSON
    """
    inp = GenerateQuickWinsInput(
        audit_results=audit_results,
        threshold_minutes=threshold_minutes,
    )
    result: GenerateQuickWinsOutput = generate_quick_wins_impl(inp)
    return result.model_dump()


@mcp.tool()
def apply_korean_benchmarks(
    industry_category: str,
    audit_results: dict | None = None,
    actual_cpc: float | None = None,
    actual_ctr: float | None = None,
    actual_roas: float | None = None,
    actual_cpa: float | None = None,
    actual_cvr: float | None = None,
) -> dict:
    """
    8 카테고리 한국 시장 벤치마크 비교 결과 반환.

    REQ-AUDIT-MCP-014: 8 카테고리 (식품/음료·패션/뷰티·건강기능식품/의료·IT/디지털·
    가정용품/생활·교육/지식·서비스/B2B·기타) CPC/CTR/ROAS/CPA/CVR 비교.
    REQ-AUDIT-MCP-021 단정적 권장 금지 — 비교 데이터만 반환.

    Args:
        industry_category: 산업 카테고리 (8개 중 1개)
        audit_results: 전체 audit 결과 (선택 — 실측 지표 자동 추출)
        actual_cpc/ctr/roas/cpa/cvr: 실측 지표 직접 입력 (선택)

    Returns:
        벤치마크 비교 결과 (CPC/CTR/ROAS/CPA/CVR) + 진단 요약 JSON
    """
    inp = ApplyKoreanBenchmarksInput(
        audit_results=audit_results or {},
        industry_category=industry_category,
        actual_cpc=actual_cpc,
        actual_ctr=actual_ctr,
        actual_roas=actual_roas,
        actual_cpa=actual_cpa,
        actual_cvr=actual_cvr,
    )
    result: ApplyKoreanBenchmarksOutput = apply_korean_benchmarks_impl(inp)
    return result.model_dump()


@mcp.tool()
def apply_korean_compliance(
    creative_text: str,
    product_category: str,
    pixel_context: dict | None = None,
) -> dict:
    """
    5개 한국 규제 PASS/WARNING/FAIL + 시정 가이드 반환.

    REQ-AUDIT-MCP-015: (1) PIPA (2) 정보통신망법 (3) 전자상거래법
    (4) 표시광고법 (5) 식약처 광고 심의 — 한국어 시정 가이드.
    식품·건강기능식품 카테고리 시 식약처 강제 활성화.

    Args:
        creative_text: 광고 소재 텍스트 (카피·헤드라인·설명 포함)
        product_category: 제품 카테고리 (식약처 심의 강제 활성 판단 기준)
        pixel_context: Pixel 설정 정보 (선택, em/ph 해시화 직접 검사)

    Returns:
        5개 규제 PASS/WARNING/FAIL + 한국어 시정 가이드 JSON
    """
    inp = ApplyKoreanComplianceInput(
        creative_text=creative_text,
        product_category=product_category,
        pixel_context=pixel_context,
    )
    result: ApplyKoreanComplianceOutput = apply_korean_compliance_impl(inp)
    return result.model_dump()
