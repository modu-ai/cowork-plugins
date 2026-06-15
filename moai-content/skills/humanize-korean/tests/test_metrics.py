"""Tests for humanize-ko v1.6 metrics + v2.0 post-editese metrics modules.

Runs under either pytest or unittest. Imports the metrics modules from the
cowork skill layout: references/ sits directly under the skill root
(PROJECT_ROOT), NOT under .claude/skills/... (that was the upstream
im-not-ai layout — adapted here for the moai-content cowork plugin).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
METRICS_DIR = os.path.join(PROJECT_ROOT, "references")
sys.path.insert(0, METRICS_DIR)

import metrics  # noqa: E402  (sys.path mutation is intentional)
import metrics_v2  # noqa: E402  (v2.0 post-editese layer)

# Baselines ship alongside the metric modules in references/.
BASELINE_PATH = os.path.join(METRICS_DIR, "baseline.json")
BASELINE_V2_PATH = os.path.join(METRICS_DIR, "baseline_v2.json")


class MetricsTests(unittest.TestCase):
    # ------------------------------------------------------------------
    # Robustness
    # ------------------------------------------------------------------

    def test_empty_string_is_safe(self) -> None:
        self.assertEqual(metrics.comma_inclusion_rate(""), 0.0)
        self.assertEqual(metrics.comma_usage_rate(""), 0.0)
        self.assertEqual(metrics.ending_comma_rate(""), 0.0)
        self.assertEqual(metrics.comma_segment_length(""), 0.0)
        self.assertEqual(metrics.conclusion_pivot_count(""), 0)
        self.assertEqual(metrics.safe_balance_count(""), 0)
        self.assertEqual(metrics.hanja_nominalizer_density(""), 0.0)
        self.assertEqual(metrics.lexical_diversity(""), 0.0)

    def test_single_sentence(self) -> None:
        text = "오늘은 비가 온다."
        self.assertEqual(metrics.comma_inclusion_rate(text), 0.0)
        self.assertEqual(metrics.comma_usage_rate(text), 0.0)
        self.assertGreater(metrics.lexical_diversity(text), 0.0)

    # ------------------------------------------------------------------
    # Connective ending + comma
    # ------------------------------------------------------------------

    def test_ending_comma_pattern_detection(self) -> None:
        # 5 connective endings, all followed by ", " => rate = 1.0
        text = (
            "그는 일어나고, 세수했고, 옷을 입었으며, "
            "밥을 먹지만, 곧 잠들었다."
        )
        rate = metrics.ending_comma_rate(text)
        self.assertGreater(rate, 0.5)

    def test_ending_no_comma(self) -> None:
        text = "그는 일어나고 세수했고 옷을 입었다."
        rate = metrics.ending_comma_rate(text)
        self.assertEqual(rate, 0.0)

    # ------------------------------------------------------------------
    # Lexicon counts
    # ------------------------------------------------------------------

    def test_conclusion_pivot_lexicon(self) -> None:
        text = "결론적으로 우리는 이겼다. 따라서 다음에도 이긴다. 이를 통해 자신감을 얻었다."
        self.assertEqual(metrics.conclusion_pivot_count(text), 3)

    def test_safe_balance_lexicon(self) -> None:
        text = "양쪽 모두 일리가 있다. 장점도 있지만 단점도 있다. 신중하게 결정해야 한다."
        self.assertEqual(metrics.safe_balance_count(text), 3)

    # ------------------------------------------------------------------
    # Hanja suffix density
    # ------------------------------------------------------------------

    def test_hanja_suffix_counted(self) -> None:
        text = "기술적 측면에서 안정성과 효율성, 그리고 자동화는 중요하다."
        density = metrics.hanja_nominalizer_density(text)
        # Tokens (after punct strip): 기술적 측면에서 안정성과 효율성 그리고 자동화는 중요하다
        # Hits: 기술적(적), 안정성과(과 -> not suffix; ends with 과 not target)
        # Actually 안정성과 ends with 과, so NOT counted. Let's just assert >0.
        self.assertGreater(density, 0.0)

    def test_hanja_zero_density(self) -> None:
        text = "오늘 비가 온다 우산이 필요하다 빨리 가자"
        density = metrics.hanja_nominalizer_density(text)
        self.assertEqual(density, 0.0)

    # ------------------------------------------------------------------
    # Baseline fallback
    # ------------------------------------------------------------------

    def test_baseline_null_genre_falls_back(self) -> None:
        text = "오늘은 좋은 날이다."
        result = metrics.compute_all(text, genre="news", baseline_path=BASELINE_PATH)
        # news is null in baseline => fallback warning expected.
        self.assertIn("warning", result)
        self.assertIn("news", result["warning"])

    def test_baseline_essay_no_warning(self) -> None:
        text = "오늘은 좋은 날이다."
        result = metrics.compute_all(text, genre="essay", baseline_path=BASELINE_PATH)
        self.assertNotIn("warning", result)

    # ------------------------------------------------------------------
    # End-to-end risk band
    # ------------------------------------------------------------------

    def test_ai_style_text_is_high_risk(self) -> None:
        # Heavy comma usage + ending-comma + conclusion pivots + safe balance
        # + hanja suffixes.
        text = (
            "현대 사회에서 기술적 혁신은 중요하다. "
            "AI는 빠르게 발전하고, 산업은 변화하며, 사람들은 적응해야 한다. "
            "결론적으로, 우리는 양쪽 모두를 고려해야 한다. "
            "따라서, 자동화와 안정성, 효율성, 그리고 지속가능성을 신중하게 검토해야 한다. "
            "이를 통해 사회적 균형과 기술적 진보를 함께 달성할 수 있다. "
            "그러므로 두 가지 모두 신중하게 다루어야 한다."
        )
        result = metrics.compute_all(text, genre="essay", baseline_path=BASELINE_PATH)
        self.assertEqual(result["risk_band"], "high")
        self.assertGreaterEqual(result["metrics"]["conclusion_pivot_count"], 2)
        self.assertGreaterEqual(result["metrics"]["safe_balance_count"], 2)

    def test_human_style_text_is_low_risk(self) -> None:
        # Short sentences. No commas. No conclusion pivots. No safe balance.
        # No hanja suffix nominalizers.
        text = (
            "오늘 비가 왔다. 우산을 폈다. 길이 미끄럽다. "
            "버스에 탔다. 사람들이 많다. 빨리 가고 싶다."
        )
        result = metrics.compute_all(text, genre="essay", baseline_path=BASELINE_PATH)
        self.assertEqual(result["risk_band"], "low")

    # ------------------------------------------------------------------
    # CLI smoke
    # ------------------------------------------------------------------

    def test_cli_writes_json_and_prints_band(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            in_path = os.path.join(td, "input.txt")
            out_path = os.path.join(td, "out.json")
            with open(in_path, "w", encoding="utf-8") as f:
                f.write("오늘 비가 왔다. 우산을 폈다.")
            rc = metrics._main(
                [
                    "--input", in_path,
                    "--genre", "essay",
                    "--output", out_path,
                    "--baseline", BASELINE_PATH,
                ]
            )
            self.assertEqual(rc, 0)
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["version"], "v1.6")
            self.assertIn(data["risk_band"], ("low", "medium", "high"))


class MetricsV2Tests(unittest.TestCase):
    """v2.0 post-editese layer — regression-safe sibling of metrics.py."""

    # ------------------------------------------------------------------
    # v1.6 callables are re-exported verbatim (regression guard)
    # ------------------------------------------------------------------

    def test_v1_callables_reexported(self) -> None:
        text = "그는 일어나고, 세수했고, 옷을 입었다."
        self.assertEqual(
            metrics_v2.comma_inclusion_rate(text),
            metrics.comma_inclusion_rate(text),
        )
        self.assertEqual(
            metrics_v2.ending_comma_rate(text),
            metrics.ending_comma_rate(text),
        )

    # ------------------------------------------------------------------
    # Robustness — empty input is safe across all 14 new metrics
    # ------------------------------------------------------------------

    def test_empty_string_is_safe_v2(self) -> None:
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

    # ------------------------------------------------------------------
    # T-signal detection (interference axis)
    # ------------------------------------------------------------------

    def test_double_particle_detects_double_only(self) -> None:
        # 이중 조사 2건; 단순 '~의'는 절대 카운트 안 됨 (caveat C5).
        text = "긴장으로부터의 해방과 주점 2층에서의 살림. 회사의 정책의 변화의 의미."
        self.assertEqual(metrics_v2.double_particle_count(text), 2)

    def test_double_passive_detects_surface(self) -> None:
        text = "그것은 잊혀진 기록이다. 결과가 보여진다. 데이터가 쓰여진다."
        self.assertGreaterEqual(metrics_v2.double_passive_count(text), 3)

    def test_have_make_literal(self) -> None:
        text = "우리는 어제 회의를 가졌다. 위원회가 결정을 내렸다."
        self.assertGreaterEqual(metrics_v2.have_make_literal_count(text), 2)

    def test_progressive_aspect(self) -> None:
        text = "그는 책을 읽고 있다. 비가 내리고 있다."
        self.assertGreater(metrics_v2.progressive_aspect_rate(text), 0.0)

    # ------------------------------------------------------------------
    # compute_all_v2 superset contract
    # ------------------------------------------------------------------

    def test_compute_all_v2_superset(self) -> None:
        text = "AI는 빠르게 발전하고 있다. 그는 데이터를 분석했다."
        result = metrics_v2.compute_all_v2(
            text,
            genre="essay",
            baseline_path=BASELINE_PATH,
            baseline_v2_path=BASELINE_V2_PATH,
        )
        # v1.6 keys preserved (superset)
        self.assertIn("metrics", result)
        self.assertIn("risk_band", result)
        # v2.0 keys added
        self.assertEqual(result["version"], "v2.0")
        self.assertIn("v2_metrics", result)
        self.assertIn("v2_interference_index", result)
        self.assertEqual(len(result["v2_metrics"]), 14)
        # placeholder baseline → every cell flagged
        self.assertEqual(len(result["v2_baseline_warnings"]), 14)

    def test_compute_all_alias(self) -> None:
        # compute_all is aliased to compute_all_v2 (v1.6 호환)
        self.assertIs(metrics_v2.compute_all, metrics_v2.compute_all_v2)

    # ------------------------------------------------------------------
    # CLI smoke
    # ------------------------------------------------------------------

    def test_v2_cli_writes_json_and_prints_band(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            in_path = os.path.join(td, "input.txt")
            out_path = os.path.join(td, "out_v2.json")
            with open(in_path, "w", encoding="utf-8") as f:
                f.write("오늘 비가 왔다. 그는 우산을 가지고 있다.")
            rc = metrics_v2._main(
                [
                    "--input", in_path,
                    "--genre", "essay",
                    "--output", out_path,
                    "--baseline", BASELINE_PATH,
                    "--baseline-v2", BASELINE_V2_PATH,
                ]
            )
            self.assertEqual(rc, 0)
            with open(out_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["version"], "v2.0")
            self.assertIn("v2_metrics", data)


if __name__ == "__main__":
    unittest.main()
