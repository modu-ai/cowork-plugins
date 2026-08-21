#!/usr/bin/env python3
"""윤문 사후 구조 게이트 — 4축 결정적 판정, LLM 콜 0.

문자 diff는 구조 편집에 눈이 없다. 실측에서 change_rate 2.77% 뒤에 문장
터치율 29.7%와 대구 -75%가 숨어 있었다. 이 스크립트는 문자율에 세 축을
더해 그 사각지대를 메운다.

축:
    P0 문자율   — 측정된 문자 변경률 vs 경고 30% / 중단 50%
    P1 목표달성 — 윤문 전에 걸렸던 S1 지표가 윤문 후 제자리로 왔는가.
                  미달도 과교정도 경고다.
    P2 전멸    — C-8 대구가 before >= 5 이고 after == 0 이면 실패.
                  줄인 게 아니라 수사 구조를 몰살한 것이다.
    P3 불변식  — checks.py: 수치·직접 인용·이모지 잔존·격식 혼재
    P4 터치율  — 보고 전용. 게이트가 아니다.

종료 코드:
    0  수렴   — 전 축 통과
    1  경고   — 문자율 30~50% / S1 미달·과교정 / 전멸 / 불변식 위반
    2  중단   — 문자율 50% 이상. 윤문본 채택 금지, 롤백.
    3  오류   — 실행 불가(입력 파일 없음 등). 게이트를 건너뛰지 않는다.

사용:
    python3 verify_gates.py --before 01_input.txt --after final.md --genre essay
    python3 verify_gates.py --before a.txt --after b.txt --json

출처: `epoko77-ai/im-not-ai`(MIT, © 2026 epoko77-ai)의 `verify_gates.py`를
이 스킬 구조에 맞춰 정리했다. NOTICE §1.8.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from typing import Any, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))

EXIT_OK, EXIT_WARN, EXIT_ABORT, EXIT_ERROR = 0, 1, 2, 3

# P1 임계. 윤문 전 |z| > 2.0 로 걸렸던 지표는 윤문 후 |z| <= 1.0 안으로
# 들어와야 한다. 교정 방향으로 -1.5를 넘어가면 과교정이다.
Z_FLAGGED = 2.0
Z_TARGET = 1.0
Z_OVERCORRECT = -1.5

# P2. 대구는 사람 글에도 흔한 정상 수사이므로 절대 개수로 판정하지 않는다.
# 분명히 있던 구조가 통째로 사라진 경우만 잡는다.
ANNIHILATION_BEFORE_MIN = 5

# 카피 모드는 문자 변경률 가드를 쓰지 않는다. 헤드라인을 다시 쓰면 글자는
# 대부분 바뀌지만 사실 앵커만 지키면 정상이다 — 산문 기준을 그대로 들이대면
# 정상 리라이트가 ABORT된다. 이 장르에서 P0은 보고만 하고, 판정은 P3
# 불변식(수치·인용·고유명사)이 맡는다.
COPY_GENRES = {"copy", "headline", "cta", "landing", "slide", "social", "sns", "story"}

# z 산출이 quantization 노이즈가 되는 하한. 원 코퍼스 표본이 400~900자였다.
MIN_SENTENCES_FOR_Z = 15


def _load(name: str):
    """같은 디렉터리의 모듈을 파일 경로로 적재한다(패키지 설치 불필요)."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(_HERE, f"{name}.py"))
    if spec is None or spec.loader is None:
        raise ImportError(f"{name}.py 를 {_HERE} 에서 찾지 못했다")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _signed_z(z: Optional[float], direction: Optional[str]) -> Optional[float]:
    """z를 'AI다울수록 양수'가 되도록 뒤집는다."""
    if z is None:
        return None
    return -z if direction == "low_is_ai" else z


def judge_change_rate(rate: float, warn: float, abort: float) -> tuple[str, str]:
    if rate >= abort:
        return "ABORT", f"문자 변경률 {rate:.1%} ≥ {abort:.0%} — 윤문본 채택 금지, 롤백"
    if rate > warn:
        return "WARN", f"문자 변경률 {rate:.1%} > {warn:.0%} — 변경 하나하나를 탐지 근거와 대조할 것"
    if rate < 0.05:
        return "WARN", f"문자 변경률 {rate:.1%} < 5% — 저윤문. S1 패턴이 남아 있는지 재확인"
    return "PASS", f"문자 변경률 {rate:.1%} — 권장 5~30% 안"


def judge_s1_targets(m2, before: str, after: str, genre: str,
                     baseline: Optional[str], baseline_v2: Optional[str]) -> tuple[str, list[str]]:
    """P1 — 윤문 전에 걸렸던 S1 지표가 제자리로 왔는가."""
    kw = dict(genre=genre, baseline_path=baseline, baseline_v2_path=baseline_v2)
    b_rep = m2.compute_all_v2(before, **kw)
    a_rep = m2.compute_all_v2(after, **kw)

    if len(m2._segment_sentences(before)) < MIN_SENTENCES_FOR_Z:
        return "SKIP", [f"문장 {len(m2._segment_sentences(before))}개 — {MIN_SENTENCES_FOR_Z}개 미만이라 "
                        "비율 지표가 quantization 노이즈다. z 판정을 건너뛴다."]

    raw = m2._read_baseline_v2(baseline_v2)
    by_genre = (raw or {}).get("genres", {}) or {}
    cells = by_genre.get(genre) or by_genre.get("essay") or {}
    if not cells:
        return "NO_BASELINE", ["baseline을 읽지 못했다 — P1은 판정하지 못한다. "
                               "결과를 통과로 읽지 말 것."]

    notes: list[str] = []
    status = "PASS"
    for key, cell in cells.items():
        if not isinstance(cell, dict) or not cell.get("s1"):
            continue
        if cell.get("_placeholder"):
            continue  # 미보정 셀로는 판정하지 않는다
        bz = _signed_z(b_rep["v2_z_scores"].get(key), cell.get("direction"))
        az = _signed_z(a_rep["v2_z_scores"].get(key), cell.get("direction"))
        if bz is None or az is None or bz <= Z_FLAGGED:
            continue
        if az > Z_TARGET:
            status = "WARN"
            notes.append(f"{key}: z {bz:+.2f} → {az:+.2f} — 목표({Z_TARGET:+.1f}) 미달")
        elif az < Z_OVERCORRECT:
            status = "WARN"
            notes.append(f"{key}: z {bz:+.2f} → {az:+.2f} — {Z_OVERCORRECT:+.1f} 넘어 과교정")
        else:
            notes.append(f"{key}: z {bz:+.2f} → {az:+.2f} — 목표 달성")
    if not notes:
        notes.append("윤문 전에 걸린 보정 완료 S1 지표가 없다")
    return status, notes


def judge_annihilation(m2, before: str, after: str) -> tuple[str, str]:
    """P2 — 대구를 줄인 게 아니라 몰살했는가."""
    b, a = m2.antithesis_count(before), m2.antithesis_count(after)
    if b >= ANNIHILATION_BEFORE_MIN and a == 0:
        return "FAIL", (
            f"대구 {b} → 0. 줄인 게 아니라 전멸시켰다. C-8 처방은 "
            "'하나만 살리고 나머지를 비대칭으로'이지 전량 삭제가 아니다."
        )
    return "PASS", f"대구 {b} → {a}"


def judge_invariants(ck, before: str, after: str, genre: str) -> tuple[str, str, dict[str, Any]]:
    """P3 — 표층 불변식(수치·인용·이모지·격식)."""
    out = ck.run_checks(before, after, genre)
    if out["failed"]:
        return "FAIL", "불변식 위반: " + ", ".join(out["failed"]), out
    if out["warned"]:
        return "WARN", "불변식 경고: " + ", ".join(out["warned"]), out
    return "PASS", "수치·인용·이모지·격식 이상 없음", out


def run(before: str, after: str, genre: str = "essay",
        ignore_markup: bool = False,
        baseline: Optional[str] = None,
        baseline_v2: Optional[str] = None) -> dict[str, Any]:
    m2 = _load("metrics_v2")
    ck = _load("checks")

    rate = m2.change_rate(before, after, ignore_markup)
    rate_nm = m2.change_rate(before, after, True)
    is_copy = genre in COPY_GENRES
    if is_copy:
        p0_s = "REPORT"
        p0_n = (f"문자 변경률 {rate:.1%} — 카피 모드라 변경률 게이트를 적용하지 않는다. "
                "판정은 P3 사실 앵커가 맡는다.")
    else:
        p0_s, p0_n = judge_change_rate(rate, m2.CHANGE_RATE_WARN, m2.CHANGE_RATE_ABORT)
    p1_s, p1_n = judge_s1_targets(m2, before, after, genre, baseline, baseline_v2)
    p2_s, p2_n = judge_annihilation(m2, before, after)
    p3_s, p3_n, p3_d = judge_invariants(ck, before, after, genre)
    touch, touched, total = m2.sentence_touch_rate(before, after)

    if p0_s == "ABORT":
        verdict, code = "ABORT", EXIT_ABORT
    elif "WARN" in (p0_s, p1_s, p3_s) or "FAIL" in (p2_s, p3_s):
        verdict, code = "WARN", EXIT_WARN
    elif p1_s in ("SKIP", "NO_BASELINE"):
        # **검사하지 못한 것을 통과로 읽지 않는다.** 표본이 짧거나 baseline이
        # 없으면 P1은 아무 말도 하지 못하는데, 그걸 PASS로 흘리면 "게이트가
        # 봤고 괜찮다더라"로 읽힌다. 감사에서 6문장짜리 의미 반전이 변경률
        # 9.9%로 PASS/exit 0을 받은 것이 그 경로다.
        verdict, code = "INCONCLUSIVE", EXIT_WARN
    else:
        verdict, code = "PASS", EXIT_OK

    return {
        "verdict": verdict,
        "exit_code": code,
        "genre": genre,
        "axes": {
            "P0_문자율": {"status": p0_s, "note": p0_n,
                          "value": round(rate, 4), "마크업제외": round(rate_nm, 4)},
            "P1_목표달성": {"status": p1_s, "notes": p1_n},
            "P2_전멸": {"status": p2_s, "note": p2_n},
            "P3_불변식": {"status": p3_s, "note": p3_n, "detail": p3_d},
            "P4_터치율": {"status": "REPORT",
                          "note": f"원문 문장 {touched}/{total}개가 그대로 남지 않았다 ({touch:.1%})"},
        },
        "caveat": (
            "P1은 stdev가 추정치인 z에 기대므로 지시적 수치다. P0·P2는 정확한 셈이다. "
            "이 게이트는 구조를 볼 뿐 의미를 보지 않는다 — 의미 보존 판정은 따로 해야 한다."
        ),
    }


class _GateArgParser(argparse.ArgumentParser):
    """인자 오류를 exit 3(실행 오류)으로 낸다.

    argparse 기본값은 exit 2인데, 이 스크립트에서 2는 ABORT(과윤문으로
    채택 금지)를 뜻한다. 오타 하나가 과윤문 사고로 읽히면 안 된다.
    """

    def error(self, message: str):  # noqa: D102
        self.print_usage(sys.stderr)
        print(f"{self.prog}: 인자 오류: {message}", file=sys.stderr)
        raise SystemExit(EXIT_ERROR)


def main(argv: Optional[list[str]] = None) -> int:
    ap = _GateArgParser(description="korean-humanize 구조 게이트 (4축)")
    ap.add_argument("--before", required=True, help="윤문 전 원문")
    ap.add_argument("--after", required=True, help="윤문본")
    ap.add_argument("--genre", default="essay")
    ap.add_argument("--ignore-markup", action="store_true",
                    help="문자율을 잴 때 마크업을 벗긴다(교차 확인용)")
    ap.add_argument("--baseline", default=None)
    ap.add_argument("--baseline-v2", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        before, after = _read(args.before), _read(args.after)
    except OSError as exc:
        print(f"게이트 실행 불가: {exc}", file=sys.stderr)
        return EXIT_ERROR

    try:
        result = run(before, after, args.genre, args.ignore_markup,
                     args.baseline, args.baseline_v2)
    except Exception as exc:  # noqa: BLE001 — 게이트가 조용히 죽으면 안 된다
        print(f"게이트 실행 오류: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result["exit_code"]

    print(f"판정: {result['verdict']}  (장르={result['genre']})")
    for axis, data in result["axes"].items():
        print(f"  [{data['status']:<6}] {axis}")
        if "note" in data:
            print(f"           {data['note']}")
        for n in data.get("notes", []):
            print(f"           {n}")
    print(f"\n{result['caveat']}")
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
