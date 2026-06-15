"""humanize-korean 메트릭 모듈(metrics.py + metrics_v2.py) 자체 테스트 스위트.

Python 표준 라이브러리(unittest)만으로 실행한다. 외부 패키지나 형태소
분석기에 의존하지 않는다. references/ 폴더가 스킬 루트 바로 아래에 있는
cowork 배치를 가정하고 모듈을 임포트한다.

검증 범위:
- 8개 v1.6 지표의 경계/정상 동작
- baseline 장르 폴백 경고
- 위험 등급(low/medium/high) 종단 판정
- CLI 인자(--input/--genre/--output/--baseline)와 JSON 8키 스키마
- 14개 v2.0 post-editese 지표 + interference index
- compute_all_v2 상위집합 계약 + compute_all 별칭
- 회귀 가드: 알려진 입력에 대한 위험 등급 고정(REGRESSION_FIXTURES)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.abspath(os.path.join(_TEST_DIR, ".."))
_REFERENCES = os.path.join(_SKILL_ROOT, "references")
sys.path.insert(0, _REFERENCES)

import metrics  # noqa: E402  (sys.path 조작 의도적)
import metrics_v2  # noqa: E402

_BASELINE = os.path.join(_REFERENCES, "baseline.json")
_BASELINE_V2 = os.path.join(_REFERENCES, "baseline_v2.json")

# v1.6 출력 JSON의 최상위 키 8종 — CLI 스키마 계약.
_REQUIRED_KEYS = {
    "version",
    "genre",
    "char_count",
    "metrics",
    "z_scores",
    "risk_band",
    "risk_score",
    "evidence",
}

# metrics 객체가 담아야 할 지표 키 8종.
_REQUIRED_METRIC_KEYS = {
    "comma_inclusion_rate",
    "comma_usage_rate",
    "ending_comma_rate",
    "comma_segment_length",
    "conclusion_pivot_count",
    "safe_balance_count",
    "hanja_nominalizer_density",
    "lexical_diversity",
}

# 회귀 가드 — (이름, 본문, 기대 risk_band). 측정 알고리즘이 바뀌어도 이 등급은
# 유지되어야 한다(기능 동등성 잠금장치). 본문은 모두 자체 창작 예문이다.
_REGRESSION_FIXTURES = [
    (
        "ai_heavy_column",
        (
            "현대 사회에서 기술적 혁신은 매우 중요한 의미를 가지고 있다. "
            "인공지능은 빠르게 발전하고, 산업은 변화하며, 사람들은 적응해야 한다. "
            "결론적으로, 우리는 효율성과 안정성 양쪽 모두를 신중하게 고려해야 한다. "
            "따라서, 자동화와 지속가능성, 그리고 사회적 균형을 함께 검토해야 한다. "
            "이를 통해 기술적 진보와 인간적 가치를 동시에 달성할 수 있다. "
            "그러므로 두 가지 모두 균형 있게 다루어야 한다."
        ),
        "high",
    ),
    (
        "plain_diary",
        (
            "오늘 아침에 카페에 갔다. 커피가 맛있었다. 창밖으로 비가 내렸다. "
            "나는 책을 읽었다. 시간이 빨리 갔다. 집에 오는 길은 추웠다."
        ),
        "low",
    ),
    (
        "three_short_lines",
        "밥을 먹었다. 잠을 잤다. 일어났다.",
        "low",
    ),
]


class V1MetricFunctionTests(unittest.TestCase):
    """v1.6 8개 지표 함수의 단위 동작."""

    def test_blank_input_returns_zero(self) -> None:
        for fn in (
            metrics.comma_inclusion_rate,
            metrics.comma_usage_rate,
            metrics.ending_comma_rate,
            metrics.comma_segment_length,
            metrics.hanja_nominalizer_density,
            metrics.lexical_diversity,
        ):
            self.assertEqual(fn(""), 0.0, msg=fn.__name__)
        self.assertEqual(metrics.conclusion_pivot_count(""), 0)
        self.assertEqual(metrics.safe_balance_count(""), 0)

    def test_one_sentence_has_no_commas(self) -> None:
        sample = "바람이 차게 분다."
        self.assertEqual(metrics.comma_inclusion_rate(sample), 0.0)
        self.assertEqual(metrics.comma_usage_rate(sample), 0.0)
        self.assertGreater(metrics.lexical_diversity(sample), 0.0)

    def test_connective_followed_by_comma_is_detected(self) -> None:
        # 연결어미 4곳이 모두 쉼표를 동반 → 비율이 절반을 넘는다.
        sample = "문을 열고, 불을 켜고, 의자에 앉았으며, 노트를 펼쳤다."
        self.assertGreater(metrics.ending_comma_rate(sample), 0.5)

    def test_connective_without_comma_is_zero(self) -> None:
        sample = "문을 열고 불을 켜고 의자에 앉았다."
        self.assertEqual(metrics.ending_comma_rate(sample), 0.0)

    def test_conclusion_pivot_terms_are_summed(self) -> None:
        sample = "결론적으로 정리하면 그렇다. 따라서 다음으로 넘어간다. 이를 통해 배웠다."
        self.assertEqual(metrics.conclusion_pivot_count(sample), 3)

    def test_safe_hedge_terms_are_summed(self) -> None:
        sample = "양쪽 모두 일리가 있다. 장점도 있지만 한계도 있다. 신중하게 보아야 한다."
        self.assertEqual(metrics.safe_balance_count(sample), 3)

    def test_sino_nominalizer_density_positive(self) -> None:
        sample = "기술적 측면의 안정성과 효율성, 자동화는 핵심이다."
        self.assertGreater(metrics.hanja_nominalizer_density(sample), 0.0)

    def test_sino_nominalizer_density_zero(self) -> None:
        sample = "비가 오니 우산을 챙기자 빨리 나가자"
        self.assertEqual(metrics.hanja_nominalizer_density(sample), 0.0)


class V1ReportTests(unittest.TestCase):
    """compute_all 종단 동작 — 스키마, 폴백, 위험 등급."""

    def test_unknown_genre_falls_back_with_warning(self) -> None:
        report = metrics.compute_all("좋은 하루였다.", genre="news", baseline_path=_BASELINE)
        self.assertIn("warning", report)
        self.assertIn("news", report["warning"])

    def test_essay_genre_has_no_warning(self) -> None:
        report = metrics.compute_all("좋은 하루였다.", genre="essay", baseline_path=_BASELINE)
        self.assertNotIn("warning", report)

    def test_report_carries_required_keys(self) -> None:
        report = metrics.compute_all("좋은 하루였다.", genre="essay", baseline_path=_BASELINE)
        self.assertTrue(_REQUIRED_KEYS <= set(report.keys()))
        self.assertTrue(_REQUIRED_METRIC_KEYS <= set(report["metrics"].keys()))
        self.assertIn(report["risk_band"], ("low", "medium", "high"))

    def test_dense_ai_text_is_high_risk(self) -> None:
        sample = (
            "현대 사회에서 기술적 혁신은 중요하다. "
            "AI는 빠르게 발전하고, 산업은 변화하며, 사람들은 적응해야 한다. "
            "결론적으로, 우리는 양쪽 모두를 신중하게 고려해야 한다. "
            "따라서, 자동화와 안정성, 효율성, 지속가능성을 균형 있게 검토해야 한다. "
            "이를 통해 사회적 균형과 기술적 진보를 함께 달성할 수 있다. "
            "그러므로 두 가지 모두 신중하게 다루어야 한다."
        )
        report = metrics.compute_all(sample, genre="essay", baseline_path=_BASELINE)
        self.assertEqual(report["risk_band"], "high")
        self.assertGreaterEqual(report["metrics"]["conclusion_pivot_count"], 2)
        self.assertGreaterEqual(report["metrics"]["safe_balance_count"], 2)

    def test_plain_text_is_low_risk(self) -> None:
        sample = (
            "비가 왔다. 우산을 폈다. 길이 미끄럽다. "
            "버스를 탔다. 사람이 많다. 빨리 가고 싶다."
        )
        report = metrics.compute_all(sample, genre="essay", baseline_path=_BASELINE)
        self.assertEqual(report["risk_band"], "low")


class V1CliTests(unittest.TestCase):
    """CLI 인자 + JSON 출력 스키마 계약."""

    def test_cli_writes_json_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "doc.txt")
            dst = os.path.join(tmp, "out.json")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write("비가 왔다. 우산을 폈다.")
            code = metrics._main(
                ["--input", src, "--genre", "essay", "--output", dst, "--baseline", _BASELINE]
            )
            self.assertEqual(code, 0)
            with open(dst, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            self.assertEqual(data["version"], "v1.6")
            self.assertTrue(_REQUIRED_KEYS <= set(data.keys()))
            self.assertIn(data["risk_band"], ("low", "medium", "high"))


class V2ReexportTests(unittest.TestCase):
    """v1.6 콜러블이 metrics_v2에서 그대로 재노출되는지(회귀 가드)."""

    def test_v1_callables_match(self) -> None:
        sample = "문을 열고, 불을 켜고, 의자에 앉았다."
        self.assertEqual(
            metrics_v2.comma_inclusion_rate(sample),
            metrics.comma_inclusion_rate(sample),
        )
        self.assertEqual(
            metrics_v2.ending_comma_rate(sample),
            metrics.ending_comma_rate(sample),
        )
        self.assertEqual(
            metrics_v2.hanja_nominalizer_density(sample),
            metrics.hanja_nominalizer_density(sample),
        )


class V2SignalTests(unittest.TestCase):
    """v2.0 14개 지표의 경계/정상 동작."""

    def test_blank_input_is_safe_across_all(self) -> None:
        self.assertEqual(metrics_v2.lexical_density(""), 0.0)
        self.assertEqual(metrics_v2.ending_diversity(""), 0.0)
        self.assertEqual(metrics_v2.normalisation_score(""), 0.0)
        self.assertEqual(metrics_v2.da_streak_rate(""), 0)
        self.assertEqual(metrics_v2.inanimate_subject_rate(""), 0.0)
        self.assertEqual(metrics_v2.by_passive_count(""), 0)
        self.assertEqual(metrics_v2.double_passive_count(""), 0)
        self.assertEqual(metrics_v2.pronoun_density(""), 0.0)
        self.assertEqual(metrics_v2.deul_overuse_rate(""), 0.0)
        self.assertEqual(metrics_v2.relative_clause_nesting(""), 0)
        self.assertEqual(metrics_v2.have_make_literal_count(""), 0)
        self.assertEqual(metrics_v2.double_particle_count(""), 0)
        self.assertEqual(metrics_v2.progressive_aspect_rate(""), 0.0)

    def test_double_particle_counts_double_only(self) -> None:
        # 이중 조사 2건; 단일 '~의'는 절대 세지 않는다(caveat #5).
        sample = "긴장으로부터의 해방과 시장에서의 경쟁. 회사의 정책의 변화의 의미."
        self.assertEqual(metrics_v2.double_particle_count(sample), 2)

    def test_double_passive_surface_forms(self) -> None:
        sample = "그것은 잊혀진 약속이다. 수치가 보여진다. 문장이 쓰여진다."
        self.assertGreaterEqual(metrics_v2.double_passive_count(sample), 3)

    def test_light_verb_literal_count(self) -> None:
        sample = "우리는 오늘 회의를 가졌다. 위원회가 결정을 내렸다."
        self.assertGreaterEqual(metrics_v2.have_make_literal_count(sample), 2)

    def test_progressive_aspect_positive(self) -> None:
        sample = "그는 글을 쓰고 있다. 눈이 내리고 있다."
        self.assertGreater(metrics_v2.progressive_aspect_rate(sample), 0.0)

    def test_agent_passive_detects_sino_passive(self) -> None:
        # 축약 한자어 피동 '에 의해 + 된/되었다'.
        self.assertGreaterEqual(metrics_v2.by_passive_count("AI에 의해 생성된 보고서"), 1)
        self.assertGreaterEqual(
            metrics_v2.by_passive_count("다리가 지진에 의해 무너졌다고 알려졌다"), 0
        )
        # bare '에 의해'(피동 동사 부재)는 세지 않는다.
        self.assertEqual(metrics_v2.by_passive_count("이에 의해 우리는 성장했다"), 0)

    def test_relative_clause_excludes_topic_markers(self) -> None:
        # 주제/주격/목적격 조사가 여럿이어도 관계절 중첩으로 오탐하지 않는다.
        topic_only = "그는 학생이고 나는 교사이고 회사는 자라지만 시장은 변한다."
        self.assertEqual(metrics_v2.relative_clause_nesting(topic_only), 0)
        # 실제 3중 이상 좌향 수식(직역체)은 탐지한다. 관형사형 어미가 2음절 이상인
        # 수식어를 세 겹 이상 쌓는다(분석한·작성한·검토했던).
        nested = (
            "그는 자료를 분석한 동료가 작성한 보고서를 "
            "오래도록 검토했던 한 연구자를 추천했다."
        )
        self.assertGreaterEqual(metrics_v2.relative_clause_nesting(nested), 1)

    def test_normalisation_and_ending_diversity_range(self) -> None:
        sample = "이것은 사실이다. 저것도 사실이다. 모두 사실이다."
        self.assertGreaterEqual(metrics_v2.normalisation_score(sample), 0.0)
        self.assertLessEqual(metrics_v2.normalisation_score(sample), 1.0)
        self.assertGreaterEqual(metrics_v2.ending_diversity(sample), 0.0)
        self.assertLessEqual(metrics_v2.ending_diversity(sample), 1.0)


class V2ReportTests(unittest.TestCase):
    """compute_all_v2 상위집합 계약 + 별칭 + CLI."""

    def test_compute_all_v2_is_superset(self) -> None:
        sample = "AI는 빠르게 발전하고 있다. 그는 데이터를 분석했다."
        report = metrics_v2.compute_all_v2(
            sample,
            genre="essay",
            baseline_path=_BASELINE,
            baseline_v2_path=_BASELINE_V2,
        )
        # v1.6 키 보존
        self.assertTrue(_REQUIRED_KEYS <= set(report.keys()))
        # v2.0 키 추가
        self.assertEqual(report["version"], "v2.0")
        self.assertIn("v2_metrics", report)
        self.assertIn("v2_interference_index", report)
        self.assertEqual(len(report["v2_metrics"]), 14)
        # 모든 placeholder 셀이 경고로 표시됨
        self.assertEqual(len(report["v2_baseline_warnings"]), 14)
        # interference index 구조
        idx = report["v2_interference_index"]
        self.assertIn("components", idx)
        self.assertIn("weighted_total", idx)
        self.assertEqual(len(idx["components"]), 9)

    def test_compute_all_is_alias_of_v2(self) -> None:
        self.assertIs(metrics_v2.compute_all, metrics_v2.compute_all_v2)

    def test_v2_cli_writes_json_and_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "doc.txt")
            dst = os.path.join(tmp, "out_v2.json")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write("비가 왔다. 그는 우산을 가지고 있다.")
            code = metrics_v2._main(
                [
                    "--input", src,
                    "--genre", "essay",
                    "--output", dst,
                    "--baseline", _BASELINE,
                    "--baseline-v2", _BASELINE_V2,
                ]
            )
            self.assertEqual(code, 0)
            with open(dst, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            self.assertEqual(data["version"], "v2.0")
            self.assertIn("v2_metrics", data)


class RiskBandRegressionTests(unittest.TestCase):
    """알려진 입력에 대한 위험 등급 고정 — 기능 동등성 잠금장치.

    측정 알고리즘 내부가 바뀌어도 이 등급들은 유지되어야 한다. 본문 예문은
    전부 자체 창작이며, v1.6과 v2.0 양쪽 경로에서 같은 등급을 산출해야 한다.
    """

    def test_v1_risk_band_is_stable(self) -> None:
        for name, body, expected in _REGRESSION_FIXTURES:
            report = metrics.compute_all(body, genre="essay", baseline_path=_BASELINE)
            self.assertEqual(report["risk_band"], expected, msg=name)

    def test_v2_risk_band_matches_v1(self) -> None:
        # v2.0 출력은 v1.6의 상위집합이므로 risk_band가 동일해야 한다.
        for name, body, expected in _REGRESSION_FIXTURES:
            report = metrics_v2.compute_all_v2(
                body,
                genre="essay",
                baseline_path=_BASELINE,
                baseline_v2_path=_BASELINE_V2,
            )
            self.assertEqual(report["risk_band"], expected, msg=name)


if __name__ == "__main__":
    unittest.main()
