"""codex 적대적 감사(2026-08-22)가 잡아낸 결함 12건의 회귀 방지 테스트.

각 테스트는 **실제로 재현됐던 결함**에 대응한다. 하나가 깨지면 그 결함이
돌아온 것이다. 주석의 번호는 감사 리포트의 항목 번호다.

표준 라이브러리(unittest)만 쓴다.
"""

from __future__ import annotations

import importlib.util
import os
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
_B = os.path.join(_REFS, "baseline.json")
_B2 = os.path.join(_REFS, "baseline_v2.json")


class C8DetectionTests(unittest.TestCase):
    """② 원형 대구를 못 잡으면, 전량 삭제해도 전멸 게이트가 통과한다."""

    def test_symmetric_form_is_detected(self):
        text = ("확장인가, 집중인가. 속도인가, 안정인가. 양인가, 질인가. "
                "규모인가, 밀도인가. 숫자인가, 맥락인가.")
        self.assertGreaterEqual(m2.antithesis_count(text), 5)

    def test_annihilating_symmetric_form_is_caught(self):
        before = ("확장인가, 집중인가. 속도인가, 안정인가. 양인가, 질인가. "
                  "규모인가, 밀도인가. 숫자인가, 맥락인가. "
                  "시장은 커지고 기업은 뒤늦게 움직였다. 소비자는 이미 떠났다.")
        after = ("확장에 걸어야 한다. 속도를 택한다. 양을 늘린다. "
                 "규모를 키운다. 숫자를 믿는다. "
                 "시장은 커지고 기업은 뒤늦게 움직였다. 소비자는 이미 떠났다.")
        res = gates.run(before, after, baseline=_B, baseline_v2=_B2)
        self.assertEqual(res["axes"]["P2_전멸"]["status"], "FAIL")


class C8FalsePositiveTests(unittest.TestCase):
    """③ 정상 한국어를 대구로 오인하면 P2가 헛되이 FAIL을 낸다."""

    def test_attributive_anira_is_not_antithesis(self):
        self.assertEqual(m2.antithesis_count("그건 문제가 아니라는 점이 중요하다."), 0)

    def test_temporal_ijeone_is_not_antithesis(self):
        self.assertEqual(m2.antithesis_count("문제가 되기 이전에 예방한다."), 0)

    def test_real_antithesis_still_counts(self):
        self.assertEqual(m2.antithesis_count("도구가 아니라 원칙이다."), 1)


class SkipIsNotPassTests(unittest.TestCase):
    """④ 검사하지 못한 것을 통과로 읽으면 안 된다."""

    def test_short_sample_is_inconclusive_not_pass(self):
        res = gates.run("회사는 흑자를 냈다. 매출이 늘었다. 비용도 줄었다.",
                        "회사는 적자를 냈다. 매출이 줄었다. 비용은 늘었다.",
                        baseline=_B, baseline_v2=_B2)
        self.assertNotEqual(res["verdict"], "PASS")
        self.assertNotEqual(res["exit_code"], gates.EXIT_OK)

    def test_missing_baseline_is_not_pass(self):
        status, _ = gates.judge_s1_targets(
            m2, "가나다. " * 20, "가나다. " * 20, "essay", None, "/nonexistent.json")
        self.assertIn(status, ("NO_BASELINE", "SKIP"))


class CopyModeTests(unittest.TestCase):
    """⑥ 카피 모드는 문자 변경률 가드를 쓰지 않는다."""

    def test_copy_rewrite_does_not_abort(self):
        res = gates.run("가나다 " * 20, "전혀 다른 카피 " * 20, genre="copy", baseline_v2=_B2)
        self.assertNotEqual(res["verdict"], "ABORT")

    def test_prose_rewrite_still_aborts(self):
        res = gates.run("가나다 " * 20, "전혀 다른 산문 " * 20, genre="essay", baseline_v2=_B2)
        self.assertEqual(res["verdict"], "ABORT")


class SummaryMarkerTests(unittest.TestCase):
    """⑧ 마커 하나로 뒤의 모든 변경을 숨길 수 있으면 안 된다."""

    def test_mid_text_marker_cannot_hide_changes(self):
        b = "본문 A. 두 번째 문장. 세 번째 문장."
        r1 = m2.change_rate(b, "본문 A. <!-- HUMANIZE-SUMMARY --> 완전히 다른 내용")
        r2 = m2.change_rate(b, "본문 A. <!-- HUMANIZE-SUMMARY --> 또 다른 내용")
        self.assertNotAlmostEqual(r1, r2, places=6)

    def test_terminal_block_is_still_ignored(self):
        self.assertEqual(m2.change_rate("본문.", "본문.\n<!-- HUMANIZE-SUMMARY 메트릭 -->"), 0.0)


class MetricUnitTests(unittest.TestCase):
    """⑨ 비율은 비율이어야 하고, 중복 문장 삭제가 보여야 한다."""

    def test_antithesis_rate_never_exceeds_one(self):
        self.assertLessEqual(m2.antithesis_rate("도구가 아니라 원칙이고 속도가 아니라 방향이다."), 1.0)

    def test_geosida_counts_only_terminal(self):
        self.assertEqual(m2.geosida_rate("그것이다는 말은 틀렸다."), 0.0)
        self.assertGreater(m2.geosida_rate("변화가 큰 것이다."), 0.0)

    def test_duplicate_sentence_deletion_is_seen(self):
        _, touched, _ = m2.sentence_touch_rate("같다. 같다. 다르다.", "같다. 다르다.")
        self.assertGreater(touched, 0)


class InvariantCheckTests(unittest.TestCase):
    """⑩⑪ 불변식 검사가 오탐도 누락도 하지 않아야 한다."""

    def test_number_sign_is_preserved(self):
        self.assertNotEqual(ck.check_numbers("이익은 -5%다.", "이익은 5%다.")["status"], "PASS")

    def test_emphasis_quote_change_is_not_fail(self):
        out = ck.check_quotations('이른바 "AI 티"가 있다.', '이른바 "AI 흔적"이 있다.')
        self.assertNotEqual(out["status"], "FAIL")

    def test_real_citation_loss_is_fail(self):
        out = ck.check_quotations('대표는 "속도를 포기하지 않는다"고 했다.', "대표가 그렇게 말했다.")
        self.assertEqual(out["status"], "FAIL")

    def test_hapsyo_is_not_counted_as_haera(self):
        out = ck.check_register_mix("이것은 사실입니다. 저것도 사실입니다. 그것 또한 사실입니다.")
        self.assertEqual(out["haera"], 0)

    def test_real_haera_is_counted(self):
        out = ck.check_register_mix("이것은 사실이다. 저것도 사실이다. 그것 또한 사실이다.")
        self.assertGreater(out["haera"], 0)

    def test_typographic_star_is_not_emoji(self):
        self.assertEqual(ck.check_emoji_residue("핵심 ★ 항목", "essay")["count"], 0)

    def test_real_emoji_still_detected(self):
        self.assertGreater(ck.check_emoji_residue("효율 🚀", "essay")["count"], 0)


class SanitizerSafetyTests(unittest.TestCase):
    """⑫ 위생 처리가 내용을 손상시키면 안 된다."""

    def test_zwj_emoji_sequence_survives(self):
        self.assertEqual(san.sanitize("👩‍💻")[0], "👩‍💻")

    def test_digit_group_separator_survives(self):
        self.assertEqual(san.sanitize("10 000원")[0], "10 000원")

    def test_markdown_hard_break_survives(self):
        self.assertIn("  \n", san.sanitize("두 칸  \n다음")[0])

    def test_single_trailing_space_is_noise(self):
        self.assertNotIn(" \n", san.sanitize("한 칸 \n다음")[0])

    def test_zero_width_space_still_removed(self):
        self.assertEqual(san.sanitize("AI​ 규제")[1].get("zero_width_removed"), 1)


class ExitCodeTests(unittest.TestCase):
    """⑦ 인자 오타가 ABORT(2)로 읽히면 안 된다."""

    def test_bad_arguments_exit_error_not_abort(self):
        with self.assertRaises(SystemExit) as cm:
            gates.main(["--before", "/only-one-arg"])
        self.assertEqual(cm.exception.code, gates.EXIT_ERROR)


if __name__ == "__main__":
    unittest.main()
