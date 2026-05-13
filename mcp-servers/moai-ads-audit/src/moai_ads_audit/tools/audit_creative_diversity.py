"""
audit_creative_diversity 도구 — REQ-AUDIT-MCP-008.
Creative Diversity & Fatigue 12개 check (M25-M32 + M-CR1~4).

Attribution:
    Check matrix adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
    Andromeda Similarity <60% threshold cited from NOTICE.md.
    M-CR1~4 items adapted from 정해준 강사 노하우 (UGC + 노후화 + 빈도).
    See NOTICE.md §"agricidaniel/claude-ads (MIT)".
"""
from __future__ import annotations

from collections import Counter
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
# 임계값 — SPEC §3.1.2, claude-ads v1.5.1 + 정해준 강사 노하우
# ============================================================

# @MX:ANCHOR: [AUTO] Creative Diversity 임계값 SSOT — audit_creative_diversity·tests 공통 참조
# @MX:REASON: SPEC §3.1.2 (Andromeda Similarity 60%·빈도 3.0·노후화 2개월) REQ-AUDIT-MCP-008 검증 조건.
ANDROMEDA_SIMILARITY_THRESHOLD = 60.0  # claude-ads v1.5.1 (NOTICE.md 인용)
FREQUENCY_THRESHOLD = 3.0  # M-CR1 한국 사용자 빈도 민감도
FATIGUE_MONTHS_THRESHOLD = 2  # M-CR2 정해준 노하우: 2개월 연속 ROAS 하락
AB_TEST_MIN_SAMPLE = 1000  # M-CR3 A/B 테스트 최소 표본 (impressions)
UGC_MIN_RATIO = 0.2  # M-CR4 UGC 비율 최소 20% (정해준 노하우)
DIVERSITY_MIN_UNIQUE_RATIO = 0.5  # 헤드라인·CTA 등 유니크 비율 최소 50%

# 미디어 타입 4종 — SPEC §3.1.2 M29-M32
MEDIA_TYPES = ["image", "video", "carousel", "collection"]


class AuditCreativeDiversityInput(BaseModel):
    """audit_creative_diversity 도구 입력 스키마."""

    ads_data: list[dict] = Field(
        default_factory=list,
        description=(
            "광고 소재 데이터 리스트. 각 항목 (모두 선택 필드): "
            "{ad_id, ad_name, frequency, headline, primary_text, cta, "
            "media_type ('image'|'video'|'carousel'|'collection'), "
            "similarity_score (0-100, Andromeda), "
            "roas_monthly (list[float]: 월별 ROAS), "
            "impressions, is_ugc (bool)}"
        ),
    )
    time_window: str = Field(
        default="",
        description="분석 기간 라벨 (예: '2026-03 ~ 2026-04')",
    )


class AuditCreativeDiversityOutput(BaseModel):
    """audit_creative_diversity 도구 출력 스키마."""

    checks: list[dict] = Field(description="12개 check 결과 (M25-M32 + M-CR1~4)")
    category_score: float = Field(description="Creative 카테고리 0-100 점수")
    pass_count: int
    warning_count: int
    fail_count: int
    na_count: int
    # 진단 요약
    diversity_summary: dict = Field(description="다양성 진단 요약")
    fatigue_summary: dict = Field(description="노후화 진단 요약")
    time_window: str = ""


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
        category=CategoryName.CREATIVE,
        description=description,
        expected_impact=expected_impact,
        remediation_option=remediation_option,
    )


def _unique_ratio(values: list) -> float:
    """비어있지 않은 값의 유니크 비율."""
    cleaned = [v for v in values if v and str(v).strip()]
    if not cleaned:
        return 0.0
    return len(set(cleaned)) / len(cleaned)


def _diversity_check(
    check_id: str,
    field_label: str,
    values: list,
    severity: SeverityLevel = SeverityLevel.HIGH,
) -> CheckResult:
    """단일 다양성 지표 검사 (헤드라인·primary text·CTA 공통 패턴)."""
    cleaned = [v for v in values if v and str(v).strip()]
    if not cleaned:
        return _make_check(
            check_id, CheckStatus.NA, severity,
            description=f"{field_label} 데이터 미제공",
        )
    ratio = _unique_ratio(values)
    if ratio >= DIVERSITY_MIN_UNIQUE_RATIO:
        return _make_check(
            check_id, CheckStatus.PASS, severity,
            description=f"{field_label} 유니크 비율 {ratio:.0%} — 기준 ≥{DIVERSITY_MIN_UNIQUE_RATIO:.0%} 충족",
        )
    return _make_check(
        check_id, CheckStatus.WARNING, severity,
        description=f"{field_label} 유니크 비율 {ratio:.0%} — 기준 ≥{DIVERSITY_MIN_UNIQUE_RATIO:.0%} 미달",
        expected_impact=f"{field_label} 동질성 — Andromeda 유사도 상승·소재 노후 가속 가능",
        remediation_option=(
            f"{field_label} 변이 다양화 검토 권장: "
            "존댓말·반말·해체 카피 변이, 길이·구조 변화, 한국어 톤 분산."
        ),
    )


def audit_creative_diversity_impl(
    inp: AuditCreativeDiversityInput,
) -> AuditCreativeDiversityOutput:
    """
    Creative Diversity & Fatigue 12개 check (M25-M32 + M-CR1~4) 실행.

    REQ-AUDIT-MCP-008: Andromeda Similarity <60% / 빈도 임계값 /
    헤드라인·primary text·CTA·미디어 4축 다양성 / 소재 노후화 진단.
    REQ-AUDIT-MCP-021: 단정적 명령 금지.
    """
    ads = inp.ads_data
    checks: list[CheckResult] = []
    diversity_summary: dict = {}
    fatigue_summary: dict = {}

    # ============================================================
    # M25: Andromeda Similarity <60% (한국 광고 소재 패턴 동질성)
    # ============================================================
    if ads:
        similarity_scores = [
            float(a["similarity_score"]) for a in ads
            if a.get("similarity_score") is not None
        ]
        if similarity_scores:
            avg_sim = sum(similarity_scores) / len(similarity_scores)
            diversity_summary["andromeda_avg"] = round(avg_sim, 2)
            if avg_sim < ANDROMEDA_SIMILARITY_THRESHOLD:
                checks.append(_make_check(
                    "M25", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"Andromeda Similarity 평균 {avg_sim:.1f}% — 임계값 <{ANDROMEDA_SIMILARITY_THRESHOLD}% 충족",
                ))
            else:
                checks.append(_make_check(
                    "M25", CheckStatus.FAIL, SeverityLevel.HIGH,
                    description=f"Andromeda Similarity 평균 {avg_sim:.1f}% — 임계값 <{ANDROMEDA_SIMILARITY_THRESHOLD}% 초과",
                    expected_impact="2026 Meta Andromeda 알고리즘이 동질 소재 노출 우선순위 하향 가능",
                    remediation_option=(
                        "소재 다양화 검토 권장: 헤드라인·primary text·CTA 변이 추가, "
                        "UGC 비중 확대, 미디어 타입 (image/video/carousel/collection) 균형 분배."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M25", CheckStatus.NA, SeverityLevel.HIGH,
                description="Andromeda Similarity 점수 미제공",
            ))
    else:
        checks.append(_make_check(
            "M25", CheckStatus.NA, SeverityLevel.HIGH,
            description="ads_data 미제공 — Andromeda Similarity 산출 불가",
        ))

    # ============================================================
    # M26-M28: 헤드라인·primary text·CTA 다양성
    # ============================================================
    if ads:
        headlines = [a.get("headline") for a in ads]
        primary_texts = [a.get("primary_text") for a in ads]
        ctas = [a.get("cta") for a in ads]

        diversity_summary["headline_unique_ratio"] = round(_unique_ratio(headlines), 2)
        diversity_summary["primary_text_unique_ratio"] = round(_unique_ratio(primary_texts), 2)
        diversity_summary["cta_unique_ratio"] = round(_unique_ratio(ctas), 2)

        checks.append(_diversity_check("M26", "헤드라인", headlines, SeverityLevel.HIGH))
        checks.append(_diversity_check("M27", "primary text", primary_texts, SeverityLevel.HIGH))
        checks.append(_diversity_check("M28", "CTA", ctas, SeverityLevel.HIGH))
    else:
        for cid, label in [("M26", "헤드라인"), ("M27", "primary text"), ("M28", "CTA")]:
            checks.append(_make_check(
                cid, CheckStatus.NA, SeverityLevel.HIGH,
                description=f"ads_data 미제공 — {label} 다양성 산출 불가",
            ))

    # ============================================================
    # M29-M32: 미디어 다양성 (이미지·영상·캐러셀·collections)
    # ============================================================
    if ads:
        media_counter = Counter(
            (a.get("media_type") or "").lower() for a in ads
            if a.get("media_type")
        )
        diversity_summary["media_distribution"] = dict(media_counter)

        for cid, media in zip(["M29", "M30", "M31", "M32"], MEDIA_TYPES):
            count = media_counter.get(media, 0)
            if not media_counter:
                checks.append(_make_check(
                    cid, CheckStatus.NA, SeverityLevel.MEDIUM,
                    description=f"미디어 타입 데이터 미제공 ({media})",
                ))
            elif count > 0:
                checks.append(_make_check(
                    cid, CheckStatus.PASS, SeverityLevel.MEDIUM,
                    description=f"미디어 타입 '{media}' {count}개 광고 운용 확인",
                ))
            else:
                checks.append(_make_check(
                    cid, CheckStatus.WARNING, SeverityLevel.MEDIUM,
                    description=f"미디어 타입 '{media}' 미운용 — 한국 모바일 환경 (>80% 모바일 노출) 다변화 권장",
                    expected_impact="단일 미디어 타입 의존 — 소재 노후 가속 + 도달 폭 제한 가능",
                    remediation_option=(
                        f"'{media}' 형식 소재 추가 검토 권장. "
                        "특히 video·carousel은 한국 모바일 환경 효과 높음."
                    ),
                ))
    else:
        for cid, media in zip(["M29", "M30", "M31", "M32"], MEDIA_TYPES):
            checks.append(_make_check(
                cid, CheckStatus.NA, SeverityLevel.MEDIUM,
                description=f"ads_data 미제공 — 미디어 '{media}' 운용 확인 불가",
            ))

    # ============================================================
    # M-CR1: 광고 단위 빈도 ≤3.0 (한국 사용자 빈도 민감도)
    # ============================================================
    if ads:
        frequencies = [
            float(a["frequency"]) for a in ads
            if a.get("frequency") is not None
        ]
        if frequencies:
            high_freq = [f for f in frequencies if f > FREQUENCY_THRESHOLD]
            fatigue_summary["high_frequency_count"] = len(high_freq)
            fatigue_summary["frequency_max"] = round(max(frequencies), 2)
            fatigue_summary["frequency_avg"] = round(sum(frequencies) / len(frequencies), 2)
            if not high_freq:
                checks.append(_make_check(
                    "M-CR1", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"광고 단위 빈도 — 모든 광고 ≤{FREQUENCY_THRESHOLD} 이하",
                ))
            else:
                ratio = len(high_freq) / len(frequencies)
                status = CheckStatus.WARNING if ratio < 0.3 else CheckStatus.FAIL
                checks.append(_make_check(
                    "M-CR1", status, SeverityLevel.HIGH,
                    description=f"빈도 {FREQUENCY_THRESHOLD} 초과 광고 {len(high_freq)}개 ({ratio:.0%})",
                    expected_impact="한국 사용자 빈도 민감도 — 광고 피로도 누적·CTR 하락·CPM 상승 가능",
                    remediation_option=(
                        "고빈도 광고 단위 노출 캡 조정 또는 소재 신규 추가 검토 권장. "
                        "빈도 3.0 초과 시 ROAS 하락 패턴 모니터링 권장."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M-CR1", CheckStatus.NA, SeverityLevel.HIGH,
                description="frequency 데이터 미제공",
            ))
    else:
        checks.append(_make_check(
            "M-CR1", CheckStatus.NA, SeverityLevel.HIGH,
            description="ads_data 미제공 — 빈도 분석 불가",
        ))

    # ============================================================
    # M-CR2: 소재 노후화 (2개월 연속 ROAS 하락) — 정해준 노하우
    # ============================================================
    if ads:
        fatigued_ads = []
        for a in ads:
            roas_monthly = a.get("roas_monthly") or []
            if len(roas_monthly) < FATIGUE_MONTHS_THRESHOLD + 1:
                continue
            # 최근 N개 월에서 연속 하락 감지
            recent = roas_monthly[-(FATIGUE_MONTHS_THRESHOLD + 1):]
            declining = all(
                recent[i] < recent[i - 1]
                for i in range(1, len(recent))
            )
            if declining:
                fatigued_ads.append(a.get("ad_name") or a.get("ad_id") or "(이름 없음)")

        fatigue_summary["fatigued_ad_count"] = len(fatigued_ads)
        fatigue_summary["fatigued_ad_names"] = fatigued_ads[:5]  # 최대 5개 노출

        if any(a.get("roas_monthly") for a in ads):
            if not fatigued_ads:
                checks.append(_make_check(
                    "M-CR2", CheckStatus.PASS, SeverityLevel.HIGH,
                    description=f"노후화 의심 광고 미감지 ({FATIGUE_MONTHS_THRESHOLD}개월 연속 ROAS 하락 기준)",
                ))
            else:
                checks.append(_make_check(
                    "M-CR2", CheckStatus.WARNING, SeverityLevel.HIGH,
                    description=f"노후화 의심 광고 {len(fatigued_ads)}개 감지",
                    expected_impact=f"{FATIGUE_MONTHS_THRESHOLD}개월 연속 ROAS 하락 — 소재 노후·시장 변화 가능",
                    remediation_option=(
                        "해당 광고 단위 소재 신규 변형 또는 빈도 조정 검토 권장. "
                        "ROAS 회복 가능성 평가 후 통폐합·재구성 옵션 검토."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M-CR2", CheckStatus.NA, SeverityLevel.HIGH,
                description="roas_monthly 시계열 데이터 미제공",
            ))
    else:
        checks.append(_make_check(
            "M-CR2", CheckStatus.NA, SeverityLevel.HIGH,
            description="ads_data 미제공 — 노후화 분석 불가",
        ))

    # ============================================================
    # M-CR3: A/B 테스트 표본 크기 (한국 소형 광고주 표본 한계 인지)
    # ============================================================
    if ads:
        impressions = [int(a["impressions"]) for a in ads if a.get("impressions")]
        if impressions:
            small_sample = [i for i in impressions if i < AB_TEST_MIN_SAMPLE]
            ratio = len(small_sample) / len(impressions)
            if ratio == 0:
                checks.append(_make_check(
                    "M-CR3", CheckStatus.PASS, SeverityLevel.MEDIUM,
                    description=f"모든 광고 노출수 ≥{AB_TEST_MIN_SAMPLE} — A/B 테스트 표본 적정",
                ))
            elif ratio < 0.5:
                checks.append(_make_check(
                    "M-CR3", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                    description=f"노출수 <{AB_TEST_MIN_SAMPLE} 광고 {len(small_sample)}개 ({ratio:.0%})",
                    expected_impact="표본 부족 광고 — A/B 테스트 통계적 유의성 미달 가능",
                    remediation_option=(
                        "표본 부족 광고의 추가 노출 확보 또는 통합 후 재평가 검토 권장. "
                        "한국 소형 광고주 환경 표본 한계 인지 후 의사결정."
                    ),
                ))
            else:
                checks.append(_make_check(
                    "M-CR3", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                    description=f"노출수 <{AB_TEST_MIN_SAMPLE} 광고 비율 {ratio:.0%} 초과 — 표본 부족 다수",
                    expected_impact="A/B 테스트 결과 신뢰성 저하 — 다수 광고가 통계적 유의성 미달",
                    remediation_option=(
                        "광고 통폐합·예산 재분배로 단위당 노출수 ≥1,000 확보 검토 권장."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M-CR3", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="impressions 데이터 미제공",
            ))
    else:
        checks.append(_make_check(
            "M-CR3", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="ads_data 미제공 — A/B 표본 분석 불가",
        ))

    # ============================================================
    # M-CR4: UGC vs 광고 소재 비율 (한국 UGC 효과 높음, 자료 2)
    # ============================================================
    if ads:
        ugc_flags = [a.get("is_ugc") for a in ads if "is_ugc" in a]
        if ugc_flags:
            ugc_count = sum(1 for f in ugc_flags if f)
            ratio = ugc_count / len(ugc_flags)
            diversity_summary["ugc_ratio"] = round(ratio, 2)
            if ratio >= UGC_MIN_RATIO:
                checks.append(_make_check(
                    "M-CR4", CheckStatus.PASS, SeverityLevel.MEDIUM,
                    description=f"UGC 비율 {ratio:.0%} — 권장 ≥{UGC_MIN_RATIO:.0%} 충족",
                ))
            else:
                checks.append(_make_check(
                    "M-CR4", CheckStatus.WARNING, SeverityLevel.MEDIUM,
                    description=f"UGC 비율 {ratio:.0%} — 권장 ≥{UGC_MIN_RATIO:.0%} 미달",
                    expected_impact="한국 시장 UGC 효과 — 신뢰도·전환율 상승 기회 미활용 가능 (자료 2)",
                    remediation_option=(
                        "UGC (사용자 후기·리뷰 영상·구매 인증) 소재 비중 확대 검토 권장. "
                        "한국 시장은 UGC 형태가 광고 효과 높음."
                    ),
                ))
        else:
            checks.append(_make_check(
                "M-CR4", CheckStatus.NA, SeverityLevel.MEDIUM,
                description="is_ugc 플래그 데이터 미제공",
            ))
    else:
        checks.append(_make_check(
            "M-CR4", CheckStatus.NA, SeverityLevel.MEDIUM,
            description="ads_data 미제공 — UGC 비율 분석 불가",
        ))

    # ============================================================
    # 카테고리 점수 계산
    # ============================================================
    score_result: WeightedScoreResult = calculate_weighted_score(checks)
    cat_score = next(
        (cs.raw_score for cs in score_result.category_scores
         if cs.category == CategoryName.CREATIVE),
        0.0,
    )

    return AuditCreativeDiversityOutput(
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
        diversity_summary=diversity_summary,
        fatigue_summary=fatigue_summary,
        time_window=inp.time_window,
    )
