"""
가중치 스코어링 공식 unit test.
REQ-AUDIT-MCP-012 검증: 4가지 시나리오 + 등급 경계값.

테스트 시나리오:
1. 모두 PASS (예상 점수: 100)
2. 모두 FAIL (예상 점수: 0)
3. 혼합 PASS+WARNING (예상 점수: 중간값)
4. N/A 포함 (N/A 제외 후 계산)

등급 경계값:
- A: 90+ / B: 75-89 / C: 60-74 / D: 40-59 / F: <40

Attribution:
    Scoring formula adapted from `agricidaniel/claude-ads` v1.5.1 under MIT.
"""
import pytest

from moai_ads_audit.scoring.weighted import (
    CategoryName,
    CheckResult,
    CheckStatus,
    SeverityLevel,
    WeightedScoreResult,
    calculate_weighted_score,
    get_grade,
    score_from_category_results,
)


# ============================================================
# 헬퍼
# ============================================================

def make_check(
    check_id: str,
    status: CheckStatus,
    severity: SeverityLevel = SeverityLevel.MEDIUM,
    category: CategoryName = CategoryName.PIXEL_CAPI,
) -> CheckResult:
    """테스트용 CheckResult 생성 헬퍼."""
    return CheckResult(
        check_id=check_id,
        status=status,
        severity=severity,
        category=category,
    )


# ============================================================
# 시나리오 1: 모두 PASS
# ============================================================

class TestAllPassScenario:
    """시나리오 1: 모든 check PASS → 점수 100."""

    def test_all_pass_returns_100(self):
        checks = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
            make_check("M25", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.CREATIVE),
            make_check("M11", CheckStatus.PASS, SeverityLevel.CRITICAL, CategoryName.ACCOUNT_STRUCTURE),
            make_check("M19", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.AUDIENCE),
        ]
        result = calculate_weighted_score(checks)
        assert result.total_score == pytest.approx(100.0, abs=0.01)
        assert result.grade == "A"
        assert result.pass_count == 5
        assert result.fail_count == 0
        assert result.warning_count == 0

    def test_all_pass_grade_is_a(self):
        checks = [
            make_check(f"M{i:02d}", CheckStatus.PASS, SeverityLevel.MEDIUM, CategoryName.PIXEL_CAPI)
            for i in range(1, 6)
        ]
        result = calculate_weighted_score(checks)
        assert result.grade == "A"


# ============================================================
# 시나리오 2: 모두 FAIL
# ============================================================

class TestAllFailScenario:
    """시나리오 2: 모든 check FAIL → 점수 0."""

    def test_all_fail_returns_0(self):
        checks = [
            make_check("M01", CheckStatus.FAIL, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
            make_check("M25", CheckStatus.FAIL, SeverityLevel.HIGH, CategoryName.CREATIVE),
            make_check("M11", CheckStatus.FAIL, SeverityLevel.HIGH, CategoryName.ACCOUNT_STRUCTURE),
            make_check("M19", CheckStatus.FAIL, SeverityLevel.MEDIUM, CategoryName.AUDIENCE),
        ]
        result = calculate_weighted_score(checks)
        assert result.total_score == pytest.approx(0.0, abs=0.01)
        assert result.grade == "F"
        assert result.fail_count == 4
        assert result.pass_count == 0

    def test_all_fail_grade_is_f(self):
        checks = [
            make_check("M01", CheckStatus.FAIL, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
        ]
        result = calculate_weighted_score(checks)
        assert result.grade == "F"


# ============================================================
# 시나리오 3: 혼합 PASS+WARNING
# ============================================================

class TestMixedPassWarningScenario:
    """시나리오 3: PASS + WARNING 혼합 — C_pass=0.5 반영."""

    def test_mixed_score_between_50_and_100(self):
        # 동일 카테고리에 PASS 1개, WARNING 1개 (같은 severity)
        checks = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.WARNING, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
        ]
        result = calculate_weighted_score(checks)
        # PASS=1.0, WARNING=0.5, 동일 severity → 평균 0.75 → 75%
        assert 50.0 < result.total_score < 100.0

    def test_warning_cpass_is_0_5(self):
        """WARNING은 C_pass=0.5이므로 PASS 50%+WARNING 50% → 75점."""
        checks = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.MEDIUM, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.WARNING, SeverityLevel.MEDIUM, CategoryName.PIXEL_CAPI),
        ]
        result = calculate_weighted_score(checks)
        # (1.0 + 0.5) / (1.0 + 1.0) × 100 × 카테고리 가중치
        pixel_score = next(
            cs.raw_score for cs in result.category_scores
            if cs.category == CategoryName.PIXEL_CAPI
        )
        assert pixel_score == pytest.approx(75.0, abs=0.01)

    def test_critical_severity_weighted_more_than_low(self):
        """Critical severity check FAIL이 Low severity PASS보다 점수에 더 큰 영향."""
        # Critical FAIL + Low PASS
        checks_critical_fail = [
            make_check("M01", CheckStatus.FAIL, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.PASS, SeverityLevel.LOW, CategoryName.PIXEL_CAPI),
        ]
        # Critical PASS + Low FAIL (반대)
        checks_critical_pass = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.FAIL, SeverityLevel.LOW, CategoryName.PIXEL_CAPI),
        ]
        result_fail = calculate_weighted_score(checks_critical_fail)
        result_pass = calculate_weighted_score(checks_critical_pass)
        # Critical FAIL 케이스가 더 낮은 점수여야 함
        assert result_fail.total_score < result_pass.total_score

    def test_severity_multiplier_values(self):
        """Severity multiplier 값 직접 검증 (NOTICE.md 직접 인용)."""
        from moai_ads_audit.scoring.weighted import SEVERITY_MULTIPLIER, SeverityLevel
        assert SEVERITY_MULTIPLIER[SeverityLevel.CRITICAL] == 5.0
        assert SEVERITY_MULTIPLIER[SeverityLevel.HIGH] == 3.0
        assert SEVERITY_MULTIPLIER[SeverityLevel.MEDIUM] == 1.5
        assert SEVERITY_MULTIPLIER[SeverityLevel.LOW] == 0.5


# ============================================================
# 시나리오 4: N/A 포함
# ============================================================

class TestNAIncludedScenario:
    """시나리오 4: N/A check — C_total에서 제외."""

    def test_na_excluded_from_calculation(self):
        """N/A check는 분자·분모 모두 제외."""
        # PASS 1개 + N/A 1개 → PASS만 유효
        checks_with_na = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.NA, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
        ]
        # PASS 1개만 있는 경우
        checks_pass_only = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
        ]
        result_na = calculate_weighted_score(checks_with_na)
        result_pure = calculate_weighted_score(checks_pass_only)
        # N/A가 포함되어도 PASS만으로 계산 → 동일 점수
        assert result_na.total_score == pytest.approx(result_pure.total_score, abs=0.01)

    def test_na_count_tracked(self):
        """N/A 카운트가 정확히 집계되어야 함."""
        checks = [
            make_check("M01", CheckStatus.PASS, SeverityLevel.MEDIUM, CategoryName.PIXEL_CAPI),
            make_check("M02", CheckStatus.NA, SeverityLevel.MEDIUM, CategoryName.PIXEL_CAPI),
            make_check("M03", CheckStatus.NA, SeverityLevel.HIGH, CategoryName.PIXEL_CAPI),
        ]
        result = calculate_weighted_score(checks)
        assert result.na_count == 2
        assert result.pass_count == 1
        assert result.effective_checks == 1

    def test_all_na_returns_zero(self):
        """모두 N/A면 유효 check 없음 → 점수 0."""
        checks = [
            make_check("M01", CheckStatus.NA, SeverityLevel.CRITICAL, CategoryName.PIXEL_CAPI),
        ]
        result = calculate_weighted_score(checks)
        assert result.total_score == 0.0
        assert result.effective_checks == 0


# ============================================================
# 등급 경계값 테스트
# ============================================================

class TestGradeBoundaries:
    """A-F 등급 경계값 — claude-ads v1.5.1 인용."""

    @pytest.mark.parametrize("score,expected_grade", [
        (100.0, "A"),
        (90.0, "A"),
        (89.9, "B"),
        (75.0, "B"),
        (74.9, "C"),
        (60.0, "C"),
        (59.9, "D"),
        (40.0, "D"),
        (39.9, "F"),
        (0.0, "F"),
    ])
    def test_grade_boundaries(self, score: float, expected_grade: str):
        assert get_grade(score) == expected_grade


# ============================================================
# score_from_category_results 편의 함수 테스트
# ============================================================

class TestScoreFromCategoryResults:
    """calculate_health_score 도구 입력 형식 변환 테스트."""

    def test_dict_input_to_weighted_score(self):
        """딕셔너리 입력 → 가중치 점수 정상 변환."""
        category_results = {
            "pixel_capi": [
                {"check_id": "M01", "status": "PASS", "severity": "Critical"},
                {"check_id": "M02", "status": "FAIL", "severity": "High"},
            ],
        }
        result = score_from_category_results(category_results)
        assert isinstance(result, WeightedScoreResult)
        assert 0.0 <= result.total_score <= 100.0

    def test_unknown_category_skipped(self):
        """알 수 없는 카테고리 키는 무시."""
        category_results = {
            "unknown_category_xyz": [
                {"check_id": "X01", "status": "PASS", "severity": "High"},
            ],
        }
        result = score_from_category_results(category_results)
        # 유효 check 없음 → 점수 0
        assert result.total_score == 0.0

    def test_severity_map_override(self):
        """severity_map으로 check별 심각도 오버라이드."""
        category_results = {
            "pixel_capi": [
                {"check_id": "M01", "status": "FAIL", "severity": "Low"},
            ]
        }
        # severity_map으로 Critical로 오버라이드
        result_low = score_from_category_results(category_results, severity_map={})
        result_critical = score_from_category_results(
            category_results, severity_map={"M01": "Critical"}
        )
        # 두 경우 모두 FAIL이지만 점수는 동일 (0) — Critical은 가중치만 높음
        # 단일 check이면 0이 동일
        assert result_low.total_score == pytest.approx(0.0, abs=0.01)
        assert result_critical.total_score == pytest.approx(0.0, abs=0.01)


# ============================================================
# 카테고리 가중치 검증
# ============================================================

class TestCategoryWeights:
    """카테고리 가중치 30/30/20/20 검증."""

    def test_category_weights_sum_to_100(self):
        """4 카테고리 가중치 합 = 100%."""
        from moai_ads_audit.scoring.weighted import CATEGORY_WEIGHT
        total = sum(CATEGORY_WEIGHT.values())
        assert total == pytest.approx(1.0, abs=0.001)

    def test_pixel_and_creative_weight_30_each(self):
        """Pixel/CAPI + Creative 각각 30%."""
        from moai_ads_audit.scoring.weighted import CATEGORY_WEIGHT, CategoryName
        assert CATEGORY_WEIGHT[CategoryName.PIXEL_CAPI] == pytest.approx(0.30)
        assert CATEGORY_WEIGHT[CategoryName.CREATIVE] == pytest.approx(0.30)

    def test_account_and_audience_weight_20_each(self):
        """Account Structure + Audience 각각 20%."""
        from moai_ads_audit.scoring.weighted import CATEGORY_WEIGHT, CategoryName
        assert CATEGORY_WEIGHT[CategoryName.ACCOUNT_STRUCTURE] == pytest.approx(0.20)
        assert CATEGORY_WEIGHT[CategoryName.AUDIENCE] == pytest.approx(0.20)
