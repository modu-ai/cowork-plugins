"""v1.4.0 신규 — P5_리듬 축 (단문화 방지) 테스트.

이 축이 왜 있는가: C-11(연결어미 뒤 쉼표 제거)은 S1이고 E-1·E-4(이웃한
단문을 다시 잇기)는 S2다. `최소심각도: S1` 실행에서는 쪼개는 규칙만 돌고
잇는 규칙은 안 돌아, 산출물이 26~31자 단문으로 수렴한다. 개별 문장은 전부
자연스럽기 때문에 다른 네 축은 모두 PASS를 준다 — 이 축이 잡지 않으면
아무도 잡지 못한다.

감사 반례(2026-08-27 codex): 쉼표를 마침표로 바꿔 문장을 20→40개로 늘렸는데
게이트가 PASS/exit 0을 냈다. 아래 첫 테스트가 그 반례다.
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
gates = _load("verify_gates")

_PAIRS = [
    ("반복 업무를 스킬로 만들어 두면 다음부터는 이름만 부르면 되고",
     "그 스킬을 체인으로 묶으면 수집부터 출력까지 한 번에 흐릅니다"),
    ("팀원에게 넘기려면 설치 가이드가 필요하고",
     "그 가이드는 남이 읽고 자기 컴퓨터에 올릴 수 있어야 합니다"),
    ("예약을 걸어 두면 아무도 안 볼 때 알아서 시작하고",
     "결과는 지정한 폴더에 그대로 놓입니다"),
    ("지침에 회사 맥락을 한 번 적어 두면 매번 설명할 필요가 없어지고",
     "말투와 금지 규칙도 함께 고정됩니다"),
    ("커넥터를 붙이면 내 폴더와 메일을 직접 읽어 오고",
     "결과물도 같은 자리에 저장됩니다"),
]
_LONG = ("AI 기술이 빠르게 발전하면서 산업 전반의 생산성이 높아지는 가운데, 기업의 디지털 전환 "
         "속도가 가속화되고, 인재 확보 경쟁이 치열해지면서, 데이터 인프라 투자도 함께 확대되고 "
         "있는 상황입니다.")
_LONG_SPLIT = ("AI 기술이 빠르게 발전하면서 산업 전반의 생산성이 높아지고 있습니다. 그 가운데 기업의 "
               "디지털 전환 속도가 가속화되고 인재 확보 경쟁도 치열해지면서, 데이터 인프라 투자가 "
               "함께 확대되는 상황입니다.")
_FILLER = [
    "반복 업무를 스킬로 만들어 두면 다음부터는 이름만 부르면 되고 결과도 같은 자리에 쌓입니다.",
    "팀원에게 넘기려면 설치 가이드가 필요한데 그 가이드는 남이 읽고 올릴 수 있어야 합니다.",
    "예약을 걸어 두면 아무도 안 볼 때 알아서 시작해 결과를 지정한 폴더에 놓아둡니다.",
]


def _comma_joined() -> str:
    return "\n".join(f"{a}, {b}." for a, b in _PAIRS * 4)


def _period_split() -> str:
    return "\n".join(f"{a}. {b}." for a, b in _PAIRS * 4)


class RhythmGateTest(unittest.TestCase):
    """P5는 **REPORT 전용**이다. 통과·실패를 정하지 않고, 정독할 자리를 가리킨다.

    2026-08-27 codex 감사 finding 5: 임계 3종은 한 프로젝트 코퍼스와 논문
    1편에서 뽑은 값이라 보편 게이트로 쓸 근거가 없다. 차단 판정은 Phase 6
    정독 재판정(`contextual-review.md` §7)이 쥔다.
    """

    def test_단문화를_수치로_지목한다(self):
        """감사 반례 재현 — 20→40 문장. 실패로 단정하지 않고 '여기를 읽어라'로 낸다."""
        st, note, d = gates.judge_rhythm(m2, _comma_joined(), _period_split(), "essay")
        self.assertEqual(st, "REPORT")
        self.assertIn("단문화 의심", note)
        self.assertIn("20→40개로 늘었다", note)
        self.assertIn("정독", note)
        self.assertEqual(d["문장수"], [20, 40])

    def test_귀속을_주장하지_않는다(self):
        """before/after 두 파일만으로 편집 원인을 귀속할 수 없다(codex finding 1).
        '설명되지 않는 증가' 같은 인과 주장 필드를 내보내지 않는다."""
        _, _, d = gates.judge_rhythm(m2, _comma_joined(), _period_split(), "essay")
        self.assertNotIn("설명안되는증가", d)
        self.assertNotIn("원문장문수", d)

    def test_단문화_의심은_통과로_읽히지_않는다(self):
        """[fail-closed] P5는 보편 임계 게이트가 아니지만, 의심이 뜬 글이
        'PASS/exit 0'으로 나가지도 않는다. 앞선 감사에서 문장 20→40 반례가
        PASS를 받은 경로가 여기다(codex finding 1, 3차)."""
        out = gates.run(_comma_joined(), _period_split(), genre="essay")
        self.assertEqual(out["axes"]["P5_리듬"]["status"], "REPORT")
        # 중요한 성질은 "PASS로 나가지 않는다"이다. 어느 경고 등급이 먼저
        # 잡히는지는 다른 축의 상태에 따라 달라진다.
        self.assertNotEqual(out["verdict"], "PASS")
        self.assertNotEqual(out["exit_code"], 0)

    def test_장르_별칭이_모든_축에서_같게_동작한다(self):
        """정규화를 축마다 따로 하면 축마다 다른 장르가 된다 — 실측: `카피`가
        P0/P5에서는 카피, P3에서는 산문으로 판정됐다(codex finding 4, 3차)."""
        base = gates.run(_comma_joined(), _period_split(), genre="copy")
        alias = gates.run(_comma_joined(), _period_split(), genre="카피")
        self.assertEqual(alias["verdict"], base["verdict"])
        self.assertEqual(alias["exit_code"], base["exit_code"])
        for ax in base["axes"]:
            self.assertEqual(alias["axes"][ax]["status"], base["axes"][ax]["status"], ax)
        self.assertEqual(alias["genre_input"], "카피")

    def test_기준선_안이면_의심을_달지_않는다(self):
        """E-5가 정당하게 나눈 장문은 참고선 안에 든다."""
        before = "\n".join([_LONG] * 6 + _FILLER * 3)
        after = "\n".join([_LONG_SPLIT] * 6 + _FILLER * 3)
        st, note, _ = gates.judge_rhythm(m2, before, after, "essay")
        self.assertEqual(st, "REPORT")
        self.assertIn("참고 기준선 안", note)

    def test_최장_연속단문을_함께_센다(self):
        """'구간 수'만 세면 20개 연속이 1구간으로 잡혀 과소평가된다
        (codex finding 5). 최장 연속 길이를 따로 낸다."""
        _, _, d = gates.judge_rhythm(m2, _comma_joined(), _period_split(), "essay")
        self.assertIn("최장단문연속", d)
        self.assertGreaterEqual(d["최장단문연속"], d["스타카토구간"])

    def test_한국어_장르값이_가드를_탄다(self):
        """사용자 옵션은 `장르: 카피|슬라이드`로 들어온다. 영어만 비교하면
        한국어 값이 산문으로 판정된다 — 실측: slide→SKIP, 슬라이드→FAIL
        (codex finding 4)."""
        for g in ("슬라이드", "카피", "slide", "copy", "sns", "랜딩"):
            with self.subTest(genre=g):
                st, note, _ = gates.judge_rhythm(m2, _comma_joined(), _period_split(), g)
                self.assertEqual(st, "SKIP", f"{g}: {note}")

    def test_산문_장르값은_면제되지_않는다(self):
        for g in ("칼럼", "리포트", "essay", "블로그"):
            with self.subTest(genre=g):
                st, _, _ = gates.judge_rhythm(m2, _comma_joined(), _period_split(), g)
                self.assertEqual(st, "REPORT")

    def test_장르_정규화_표(self):
        self.assertEqual(gates.canonical_genre("슬라이드"), "slide")
        self.assertEqual(gates.canonical_genre("카피"), "copy")
        self.assertEqual(gates.canonical_genre("칼럼"), "essay")
        self.assertEqual(gates.canonical_genre("ESSAY"), "essay")

    def test_표본이_작으면_판정하지_않는다(self):
        """12문장 미만은 리듬을 말할 표본이 아니다. 모르는 것을 통과로 흘리지 않는다."""
        tiny = "짧은 문장입니다. 또 하나입니다. 셋째입니다."
        st, _, _ = gates.judge_rhythm(m2, tiny, tiny, "essay")
        self.assertEqual(st, "SKIP")



class SemanticLimitTest(unittest.TestCase):
    """[음성 회귀] 구조 게이트가 **못 잡는 것**을 코드로 못박는다.

    2026-08-27 codex 감사 finding 2: contextual-review.md §4가 한정어를
    "군더더기"로 지우라고 지시하고 있었다. `사실상 독점` → `독점`은 실질적
    지배를 법적 독점으로, `기본적으로 무료` → `무료`는 예외 있는 정책을
    무조건으로 바꾼다. 구조 게이트는 이 변화를 전부 통과시킨다.

    이 테스트는 결함이 아니라 **한계의 기록**이다. 게이트가 PASS를 냈다는
    이유로 의미가 보존됐다고 읽으면 안 된다는 것을, 실패가 아니라 명시로
    남긴다. 실제 방어선은 두 곳이다 — §4의 한정어 보존 조항(문서)과
    Phase 6 정독 재판정 7-b 의미 대조(사람/모델의 읽기).
    """

    _BEFORE = ("이 회사는 국내 시장에서 사실상 독점 지위에 있습니다. "
               "요금제는 기본적으로 무료이며, 대량 사용 시에만 과금됩니다. "
               "그러므로 규제 당국이 들여다보지 않을 수 없습니다.")
    _AFTER = ("이 회사는 국내 시장에서 독점 지위에 있습니다. "
              "요금제는 무료이며, 대량 사용 시에만 과금됩니다. "
              "그러므로 규제 당국이 들여다보아야 합니다.")

    def test_한정어_삭제를_구조게이트는_못_잡는다(self):
        out = gates.run(self._BEFORE, self._AFTER, genre="essay")
        self.assertEqual(out["axes"]["P3_불변식"]["status"], "PASS",
                         "P3는 수치·인용·이모지만 본다 — 의미는 보지 않는다")

    def test_문서가_한정어_보존_조항을_들고_있다(self):
        """§4가 다시 '지운다'로 돌아가면 이 테스트가 깨진다."""
        path = os.path.join(_REFS, "contextual-review.md")
        with open(path, encoding="utf-8") as fh:
            body = fh.read()
        self.assertIn("한정어를 지우면 주장이 강해진다", body)
        self.assertIn("양태를 바꾸는 치환은 금지한다", body)
        self.assertNotIn("아래는 지워도 뜻이 그대로다. 지운다.", body)


if __name__ == "__main__":
    unittest.main()
