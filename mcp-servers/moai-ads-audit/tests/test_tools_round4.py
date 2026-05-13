"""
라운드 4 (v0.2.0) 잔여 7 도구 unit test.

대상 도구:
- audit_creative_diversity (REQ-AUDIT-MCP-008)
- audit_account_structure (REQ-AUDIT-MCP-009)
- audit_audience_targeting (REQ-AUDIT-MCP-010)
- audit_andromeda_emq (REQ-AUDIT-MCP-011)
- generate_quick_wins (REQ-AUDIT-MCP-013)
- apply_korean_benchmarks (REQ-AUDIT-MCP-014)
- apply_korean_compliance (REQ-AUDIT-MCP-015)

각 도구당 최소 3 시나리오:
- 빈 입력 → N/A 안전 처리
- 정상 입력 → PASS 정상 결과
- 위반 입력 → WARNING/FAIL 검출
"""
from __future__ import annotations

import pytest

from moai_ads_audit.tools.audit_creative_diversity import (
    AuditCreativeDiversityInput,
    audit_creative_diversity_impl,
)
from moai_ads_audit.tools.audit_account_structure import (
    AuditAccountStructureInput,
    audit_account_structure_impl,
)
from moai_ads_audit.tools.audit_audience_targeting import (
    AuditAudienceTargetingInput,
    audit_audience_targeting_impl,
)
from moai_ads_audit.tools.audit_andromeda_emq import (
    AuditAndromedaEmqInput,
    audit_andromeda_emq_impl,
)
from moai_ads_audit.tools.generate_quick_wins import (
    GenerateQuickWinsInput,
    generate_quick_wins_impl,
)
from moai_ads_audit.tools.apply_korean_benchmarks import (
    ApplyKoreanBenchmarksInput,
    apply_korean_benchmarks_impl,
)
from moai_ads_audit.tools.apply_korean_compliance import (
    ApplyKoreanComplianceInput,
    apply_korean_compliance_impl,
)


# ============================================================
# audit_creative_diversity (REQ-AUDIT-MCP-008, 12 checks)
# ============================================================

class TestAuditCreativeDiversity:
    """Creative Diversity & Fatigue audit 검증."""

    def test_empty_input_returns_all_na(self):
        """빈 ads_data → 12 checks 모두 N/A."""
        out = audit_creative_diversity_impl(AuditCreativeDiversityInput())
        assert len(out.checks) == 12
        assert out.na_count == 12
        assert out.pass_count == 0

    def test_diverse_ads_pass(self):
        """다양한 광고 데이터 → 다양성 PASS."""
        ads = [
            {
                "ad_id": f"ad-{i}",
                "headline": f"헤드라인 {i}",
                "primary_text": f"본문 {i}",
                "cta": ["구매하기", "더 알아보기", "장바구니"][i % 3],
                "media_type": ["image", "video", "carousel", "collection"][i % 4],
                "similarity_score": 30.0,
                "frequency": 2.0,
                "roas_monthly": [2.0, 2.1, 2.2],
                "impressions": 5000,
                "is_ugc": i % 2 == 0,
            }
            for i in range(4)
        ]
        out = audit_creative_diversity_impl(
            AuditCreativeDiversityInput(ads_data=ads)
        )
        assert out.pass_count >= 6  # 최소 절반은 PASS

    def test_high_andromeda_similarity_fails(self):
        """Andromeda similarity 80% → M25 FAIL."""
        ads = [{"similarity_score": 80.0} for _ in range(3)]
        out = audit_creative_diversity_impl(
            AuditCreativeDiversityInput(ads_data=ads)
        )
        m25 = next(c for c in out.checks if c["check_id"] == "M25")
        assert m25["status"] == "FAIL"

    def test_fatigue_detection(self):
        """2개월 연속 ROAS 하락 → M-CR2 WARNING."""
        ads = [{
            "ad_name": "노후화 광고",
            "roas_monthly": [3.0, 2.5, 2.0, 1.5],
        }]
        out = audit_creative_diversity_impl(
            AuditCreativeDiversityInput(ads_data=ads)
        )
        m_cr2 = next(c for c in out.checks if c["check_id"] == "M-CR2")
        assert m_cr2["status"] == "WARNING"
        assert out.fatigue_summary["fatigued_ad_count"] >= 1


# ============================================================
# audit_account_structure (REQ-AUDIT-MCP-009, 10 checks)
# ============================================================

class TestAuditAccountStructure:
    """Account Structure audit 검증."""

    def test_empty_input_returns_all_na(self):
        out = audit_account_structure_impl(AuditAccountStructureInput())
        assert len(out.checks) == 10
        assert out.na_count == 10

    def test_healthy_structure_passes(self):
        """정상 구조 → Learning Limited 0% → M11 PASS."""
        campaigns = [{
            "campaign_id": "c1",
            "campaign_name": "정상 캠페인",
            "objective": "Purchase",
            "budget_type": "CBO",
            "daily_budget": 100000,
            "adsets": [
                {"adset_id": "as1", "learning_status": "active"},
                {"adset_id": "as2", "learning_status": "learning"},
            ],
            "audience_network_roas": 1.5,
            "product_unit_price": 30000,
        }]
        out = audit_account_structure_impl(
            AuditAccountStructureInput(campaigns=campaigns)
        )
        assert out.learning_limited_ratio == 0.0
        m11 = next(c for c in out.checks if c["check_id"] == "M11")
        assert m11["status"] == "PASS"

    def test_learning_limited_over_threshold_fails(self):
        """Learning Limited 비율 >30% → M11 FAIL."""
        campaigns = [{
            "campaign_id": "c1",
            "adsets": [
                {"adset_id": f"as{i}", "learning_status": "limited"}
                for i in range(5)
            ],
        }]
        out = audit_account_structure_impl(
            AuditAccountStructureInput(campaigns=campaigns)
        )
        assert out.learning_limited_ratio == 1.0
        m11 = next(c for c in out.checks if c["check_id"] == "M11")
        assert m11["status"] == "FAIL"

    def test_oversized_campaign_warning(self):
        """광고 세트 6개 초과 캠페인 → M-ST1 WARNING."""
        campaigns = [{
            "campaign_id": "c1",
            "campaign_name": "과대 캠페인",
            "adsets": [{"adset_id": f"as{i}"} for i in range(7)],
        }]
        out = audit_account_structure_impl(
            AuditAccountStructureInput(campaigns=campaigns)
        )
        m_st1 = next(c for c in out.checks if c["check_id"] == "M-ST1")
        assert m_st1["status"] == "WARNING"


# ============================================================
# audit_audience_targeting (REQ-AUDIT-MCP-010, 7 checks)
# ============================================================

class TestAuditAudienceTargeting:
    """Audience & Targeting audit 검증."""

    def test_empty_input_returns_all_na(self):
        """빈 입력 — overlap 진단 데이터 부재(M20)는 의도적 WARNING (활용 권장 안내)."""
        out = audit_audience_targeting_impl(AuditAudienceTargetingInput())
        assert len(out.checks) == 7
        # 6 N/A + 1 WARNING (M20 = overlap 진단 활용 권장)
        assert out.na_count == 6
        assert out.warning_count == 1
        m20 = next(c for c in out.checks if c["check_id"] == "M20")
        assert m20["status"] == "WARNING"

    def test_low_overlap_passes(self):
        """overlap <20% → M19 PASS."""
        audiences = [
            {"audience_id": "a1", "overlap_pct_with": {"a2": 0.1}},
            {"audience_id": "a2", "overlap_pct_with": {"a1": 0.1}},
        ]
        out = audit_audience_targeting_impl(
            AuditAudienceTargetingInput(audiences=audiences)
        )
        m19 = next(c for c in out.checks if c["check_id"] == "M19")
        assert m19["status"] == "PASS"

    def test_high_overlap_warning_or_fail(self):
        """overlap ≥20% → M19 WARNING 또는 FAIL."""
        audiences = [
            {"audience_id": "a1", "overlap_pct_with": {"a2": 0.5}},
            {"audience_id": "a2", "overlap_pct_with": {"a1": 0.5}},
        ]
        out = audit_audience_targeting_impl(
            AuditAudienceTargetingInput(audiences=audiences)
        )
        m19 = next(c for c in out.checks if c["check_id"] == "M19")
        assert m19["status"] in {"WARNING", "FAIL"}

    def test_small_lookalike_seed_warning(self):
        """seed 크기 <1000 → M21 WARNING."""
        seeds = [{"seed_id": "s1", "seed_name": "soulja", "seed_size": 500}]
        out = audit_audience_targeting_impl(
            AuditAudienceTargetingInput(lookalike_seeds=seeds)
        )
        m21 = next(c for c in out.checks if c["check_id"] == "M21")
        assert m21["status"] == "WARNING"


# ============================================================
# audit_andromeda_emq (REQ-AUDIT-MCP-011, 4 checks)
# ============================================================

class TestAuditAndromedaEmq:
    """Andromeda & Platform Changes audit 검증."""

    def test_empty_input_returns_all_na(self):
        out = audit_andromeda_emq_impl(AuditAndromedaEmqInput())
        assert len(out.checks) == 4
        assert out.na_count == 4

    def test_high_andromeda_score_passes(self):
        """Andromeda score 80 → M-AN1 PASS."""
        out = audit_andromeda_emq_impl(AuditAndromedaEmqInput(
            ads_data=[{"andromeda_score": 80.0}],
        ))
        m_an1 = next(c for c in out.checks if c["check_id"] == "M-AN1")
        assert m_an1["status"] == "PASS"

    def test_threshold_acknowledged_passes(self):
        """threshold_changes_acknowledged=True → M-TH1 PASS."""
        out = audit_andromeda_emq_impl(AuditAndromedaEmqInput(
            threshold_changes_acknowledged=True,
        ))
        m_th1 = next(c for c in out.checks if c["check_id"] == "M-TH1")
        assert m_th1["status"] == "PASS"


# ============================================================
# generate_quick_wins (REQ-AUDIT-MCP-013)
# ============================================================

class TestGenerateQuickWins:
    """Quick Wins 추출 검증."""

    def test_empty_audit_returns_empty_quick_wins(self):
        out = generate_quick_wins_impl(GenerateQuickWinsInput(audit_results={}))
        assert out.total_count == 0

    def test_low_severity_excluded(self):
        """Low severity는 Quick Win 대상 아님."""
        audit = {
            "pixel_capi_result": {
                "checks": [
                    {"check_id": "M07", "status": "FAIL", "severity": "Low"},
                ]
            }
        }
        out = generate_quick_wins_impl(GenerateQuickWinsInput(audit_results=audit))
        assert out.total_count == 0

    def test_critical_high_short_effort_included(self):
        """Critical/High + 15분 미만 effort → Quick Win 포함."""
        audit = {
            "pixel_capi_result": {
                "checks": [
                    {"check_id": "M01", "status": "FAIL", "severity": "Critical"},  # 5분
                    {"check_id": "M06", "status": "WARNING", "severity": "High"},   # 10분
                    {"check_id": "M10", "status": "FAIL", "severity": "High"},      # 120분 (제외)
                ]
            }
        }
        out = generate_quick_wins_impl(
            GenerateQuickWinsInput(audit_results=audit, threshold_minutes=15)
        )
        assert out.total_count == 2  # M01, M06 (M10은 120분으로 제외)
        # Critical이 먼저 (priority_rank 1)
        assert out.quick_wins[0]["severity"] == "Critical"

    def test_pass_excluded_from_quick_wins(self):
        """PASS 상태는 Quick Win 대상 아님 (이미 충족)."""
        audit = {
            "pixel_capi_result": {
                "checks": [
                    {"check_id": "M01", "status": "PASS", "severity": "Critical"},
                ]
            }
        }
        out = generate_quick_wins_impl(GenerateQuickWinsInput(audit_results=audit))
        assert out.total_count == 0


# ============================================================
# apply_korean_benchmarks (REQ-AUDIT-MCP-014)
# ============================================================

class TestApplyKoreanBenchmarks:
    """한국 시장 벤치마크 비교 검증."""

    def test_food_beverage_within_benchmark(self):
        """식품/음료 ROAS 1.8 → 케어밀 reference within."""
        out = apply_korean_benchmarks_impl(ApplyKoreanBenchmarksInput(
            industry_category="식품/음료",
            actual_roas=1.80,
        ))
        assert out.industry_category == "식품/음료"
        assert out.comparison["roas"]["status"] == "within"

    def test_health_medical_requires_mfds(self):
        """건강기능식품/의료 카테고리 → MFDS 강제 활성."""
        out = apply_korean_benchmarks_impl(ApplyKoreanBenchmarksInput(
            industry_category="건강기능식품/의료",
        ))
        assert out.requires_mfds_review is True

    def test_unknown_category_falls_back_to_other(self):
        """알 수 없는 카테고리 → 기타 fallback."""
        out = apply_korean_benchmarks_impl(ApplyKoreanBenchmarksInput(
            industry_category="우주 광고",
        ))
        assert out.industry_category == "기타"

    def test_roas_below_benchmark(self):
        """식품/음료 ROAS 0.5 → below."""
        out = apply_korean_benchmarks_impl(ApplyKoreanBenchmarksInput(
            industry_category="식품/음료",
            actual_roas=0.5,
        ))
        assert out.comparison["roas"]["status"] == "below"
        assert out.summary["primary_concern"] == "roas"


# ============================================================
# apply_korean_compliance (REQ-AUDIT-MCP-015)
# ============================================================

class TestApplyKoreanCompliance:
    """한국 규제 검사 검증."""

    def test_clean_text_mostly_passes(self):
        """위반 표현 없음 → 표시광고법·식약처 PASS."""
        text = "건강한 하루를 시작하세요. 수신거부: 080-123-4567"
        out = apply_korean_compliance_impl(ApplyKoreanComplianceInput(
            creative_text=text,
            product_category="기타",
        ))
        # 표시광고법 PASS 확인
        adv = next(c for c in out.checks if c["regulation"] == "표시광고법")
        assert adv["status"] == "PASS"
        # 식약처 PASS 확인 (기타 카테고리 → force_active=False)
        mfds = next(c for c in out.checks if c["regulation"] == "식약처 광고 심의")
        assert mfds["status"] == "PASS"

    def test_health_food_category_activates_mfds(self):
        """건강기능식품 카테고리 + 심의 번호 부재 → MFDS WARNING/FAIL."""
        out = apply_korean_compliance_impl(ApplyKoreanComplianceInput(
            creative_text="건강기능식품 광고입니다",
            product_category="건강기능식품/의료",
        ))
        assert out.mfds_force_active is True

    def test_prohibited_patterns_detected(self):
        """1위 + 100% 효과 → 표시광고법 WARNING + 매칭 패턴 노출."""
        out = apply_korean_compliance_impl(ApplyKoreanComplianceInput(
            creative_text="업계 1위! 100% 효과 보장",
            product_category="기타",
        ))
        adv = next(c for c in out.checks if c["regulation"] == "표시광고법")
        assert adv["status"] == "WARNING"
        assert len(adv["matched_patterns"]) >= 2  # 1위 + 100%

    def test_mfds_prohibited_disease_terms_fail(self):
        """질병 치료·완치 표현 → 식약처 FAIL."""
        out = apply_korean_compliance_impl(ApplyKoreanComplianceInput(
            creative_text="당뇨 치료 효과 완치 보장",
            product_category="건강기능식품/의료",
        ))
        mfds = next(c for c in out.checks if c["regulation"] == "식약처 광고 심의")
        assert mfds["status"] == "FAIL"
        assert len(mfds["matched_patterns"]) >= 1
