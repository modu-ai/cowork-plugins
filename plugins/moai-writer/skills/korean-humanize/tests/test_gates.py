"""v2.4 신규 — 실증 지표 · 구조 게이트 · 텍스트 위생 테스트.

표준 라이브러리(unittest)만 쓴다. 외부 패키지도, 형태소 분석기도 필요 없다.
"""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_REFS = os.path.join(_HERE, "..", "references")


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.join(_REFS, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m2 = _load("metrics_v2")
ck = _load("checks")
gates = _load("verify_gates")
san = _load("sanitize_text")


class AntithesisTests(unittest.TestCase):
    """C-8 부정 대구 — 실측 최강 신호(AI 5.8 vs 사람 0.6)."""

    def test_counts_negative_antithesis(self):
        text = "도구가 아니라 원칙이다. 속도가 아니라 방향이다. 양이 아니라 질이다."
        self.assertEqual(m2.antithesis_count(text), 3)

    def test_counts_raki_variant(self):
        self.assertEqual(m2.antithesis_count("이건 실패라기보다 실험이다."), 1)

    def test_empty_text_is_zero(self):
        self.assertEqual(m2.antithesis_count("   "), 0)

    def test_rate_is_normalized_by_sentence_count(self):
        """개수와 비율은 별개다 — 같은 baseline 셀에 물리면 짧은 글이 과대 평가된다."""
        text = "도구가 아니라 원칙이다. 속도가 아니라 방향이다."
        self.assertEqual(m2.antithesis_count(text), 2)
        self.assertAlmostEqual(m2.antithesis_rate(text), 1.0, places=3)


class LongSentenceTests(unittest.TestCase):
    """E-1의 실체는 '균일'이 아니라 '장문 부재'."""

    def test_short_only_scores_zero(self):
        self.assertEqual(m2.long_sentence_rate("짧다. 또 짧다. 여전히 짧다."), 0.0)

    def test_detects_long_sentence(self):
        long_one = "가" * 120 + "."
        rate = m2.long_sentence_rate(f"짧다. {long_one} 또 짧다.")
        self.assertGreater(rate, 0.0)


class GeosidaTests(unittest.TestCase):
    """I-1 — 사람이 2배 더 쓰므로 낮을수록 AI다."""

    def test_counts_geosida(self):
        self.assertGreater(m2.geosida_rate("변화가 크다는 것이다. 그래서 중요한 것이다."), 0.0)

    def test_absent_scores_zero(self):
        self.assertEqual(m2.geosida_rate("변화가 크다. 그래서 중요하다."), 0.0)


class ChangeRateTests(unittest.TestCase):
    """철칙 #4 게이트의 단일 진실 원천."""

    def test_identical_is_zero(self):
        self.assertEqual(m2.change_rate("같은 글이다.", "같은 글이다."), 0.0)

    def test_full_replacement_is_high(self):
        self.assertGreater(m2.change_rate("가나다라마바사", "ABCDEFG"), 0.9)

    def test_summary_block_is_stripped_before_compare(self):
        body = "본문이다."
        self.assertEqual(m2.change_rate(body, body + "\n<!-- HUMANIZE-SUMMARY 메트릭 -->"), 0.0)

    def test_ignore_markup_drops_heading_decoration(self):
        before = "# 제목\n\n본문이다."
        after = "본문이다."
        self.assertLess(m2.change_rate(before, after, ignore_markup=True),
                        m2.change_rate(before, after))

    def test_thresholds_are_exposed(self):
        self.assertEqual(m2.CHANGE_RATE_WARN, 0.30)
        self.assertEqual(m2.CHANGE_RATE_ABORT, 0.50)


class ChecksTests(unittest.TestCase):
    def test_lost_number_is_warn_not_fail(self):
        """문장 병합으로 중복 수치가 줄 수 있으므로 경고까지만."""
        out = ck.check_numbers("매출은 2조원, 이익률은 12.4%다.", "매출은 2조원이다.")
        self.assertEqual(out["status"], "WARN")
        self.assertIn("12.4", "".join(out["lost"]))

    def test_lost_quotation_is_fail(self):
        out = ck.check_quotations('대표는 "속도를 포기하지 않는다"고 말했다.', "대표가 그렇게 말했다.")
        self.assertEqual(out["status"], "FAIL")

    def test_quotation_preserved_passes(self):
        src = '대표는 "속도를 포기하지 않는다"고 말했다.'
        self.assertEqual(ck.check_quotations(src, src)["status"], "PASS")

    def test_emoji_residue_fails_in_prose_genre(self):
        self.assertEqual(ck.check_emoji_residue("효율 개선 🚀", "essay")["status"], "FAIL")

    def test_emoji_allowed_in_copy_genre(self):
        self.assertEqual(ck.check_emoji_residue("효율 개선 🚀", "copy")["status"], "REPORT")


class GateTests(unittest.TestCase):
    def _run(self, before, after, **kw):
        return gates.run(before, after,
                         baseline=os.path.join(_REFS, "baseline.json"),
                         baseline_v2=os.path.join(_REFS, "baseline_v2.json"), **kw)

    def test_identical_text_converges(self):
        text = "시장은 성장한다. 기업은 대응한다. 소비자는 반응한다."
        # 변경률 0%는 '저윤문' 경고가 맞다 — 아무것도 안 고쳤다는 뜻이므로.
        res = self._run(text, text)
        self.assertEqual(res["axes"]["P0_문자율"]["status"], "WARN")
        self.assertEqual(res["axes"]["P2_전멸"]["status"], "PASS")

    def test_annihilation_is_caught_even_when_p1_says_target_met(self):
        """P1만 보면 '성공'인데 실제로는 수사를 몰살한 경우 — P2가 잡아야 한다."""
        common = ("시장은 빠르게 커지고 있고 기업들은 뒤늦게 대응을 시작했다. "
                  "소비자는 이미 다른 선택지를 찾아 떠난 뒤였다. "
                  "데이터 인프라 투자는 늘었지만 인재 확보는 여전히 어렵다. "
                  "규제는 아직 명확한 형태를 갖추지 못했다. ")
        before = common + ("도구가 아니라 원칙이다. 속도가 아니라 방향이다. "
                           "양이 아니라 질이다. 규모가 아니라 밀도다. 숫자가 아니라 맥락이다.")
        after = common + ("원칙이 먼저다. 방향이 속도를 이긴다. "
                          "질이 남는다. 밀도가 중요하다. 맥락이 결과를 가른다.")
        res = self._run(before, after)
        self.assertEqual(res["axes"]["P2_전멸"]["status"], "FAIL")
        self.assertEqual(res["exit_code"], gates.EXIT_WARN)

    def test_over_edit_aborts(self):
        before = "가나다라마바사아자차카타파하 " * 10
        after = "ABCDEFGHIJKLMNOP " * 10
        res = self._run(before, after)
        self.assertEqual(res["verdict"], "ABORT")
        self.assertEqual(res["exit_code"], gates.EXIT_ABORT)

    def test_missing_file_exits_error_not_silently(self):
        """게이트를 건너뛰지 않는다 — 실행 불가는 exit 3으로 드러난다."""
        self.assertEqual(gates.main(["--before", "/nonexistent_a", "--after", "/nonexistent_b"]),
                         gates.EXIT_ERROR)

    def test_short_sample_skips_z_judgment(self):
        """문장이 적으면 비율 지표가 quantization 노이즈이므로 P1을 건너뛴다."""
        res = self._run("짧다.", "짧다!")
        self.assertEqual(res["axes"]["P1_목표달성"]["status"], "SKIP")


class SanitizeTests(unittest.TestCase):
    def test_removes_zero_width(self):
        cleaned, rep = san.sanitize("AI​ 규제")
        self.assertNotIn("​", cleaned)
        self.assertEqual(rep["zero_width_removed"], 1)

    def test_folds_full_width_space(self):
        cleaned, rep = san.sanitize("AI　규제")
        self.assertIn("AI 규제", cleaned)
        self.assertEqual(rep["special_spaces_folded"], 1)

    def test_normalizes_hangul_to_nfc(self):
        nfd = "한"  # 한 (분리형)
        cleaned, rep = san.sanitize(nfd)
        self.assertEqual(cleaned, "한")
        self.assertTrue(rep["nfc_normalized"])

    def test_clean_text_is_unchanged(self):
        cleaned, rep = san.sanitize("정상적인 한국어 문장이다.")
        self.assertFalse(rep["changed"])
        self.assertEqual(cleaned, "정상적인 한국어 문장이다.")

    def test_cli_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = os.path.join(d, "a.txt"), os.path.join(d, "b.txt")
            with open(src, "w", encoding="utf-8") as fh:
                fh.write("AI​ 규제　논의")
            self.assertEqual(san.main(["--input", src, "--output", dst]), 0)
            with open(dst, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "AI 규제 논의")


if __name__ == "__main__":
    unittest.main()
