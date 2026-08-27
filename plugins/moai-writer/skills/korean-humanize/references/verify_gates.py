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

# [HARD] 사용자 옵션은 한국어로 들어온다(`장르: 카피|슬라이드`). 영어 값만
# 비교하면 `슬라이드`가 카피 가드를 못 타고 산문으로 판정된다 — 실측:
# slide → SKIP, 슬라이드 → FAIL. 경계에서 정규화해 같은 값으로 만든다.
GENRE_ALIASES = {
    "카피": "copy", "헤드라인": "headline", "랜딩": "landing", "슬라이드": "slide",
    "소셜": "social", "에스엔에스": "sns", "스토리": "story", "광고": "copy",
    "칼럼": "essay", "리포트": "report", "보고서": "report", "블로그": "blog",
    "공적": "official", "공문": "official", "산문": "essay", "안내문": "official",
}


def canonical_genre(genre: str) -> str:
    """한국어·영어 장르값을 하나의 표기로 모은다."""
    g = (genre or "").strip()
    return GENRE_ALIASES.get(g, g.lower())

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


# ── R축 참고 기준선 (산문 전용 · REPORT 전용) ────────────────────────
# [HARD] 이 수치는 **게이트가 아니라 참고선**이다. 표본이 한 프로젝트의
# 코퍼스와 논문 1편이라 절단점을 보편 임계로 쓸 근거가 못 된다(2026-08-27
# codex 감사 finding 5). 넘었다고 실패가 아니라 "정독할 때 여기를 보라"는
# 신호이며, 최종 판정은 Phase 2.5 정독 소견과 Phase 6 정독 재판정이 한다.
# 실측 기준선(2026-08-27, 한국어 34만 자 + 국립국어원 새국어생활 22-1):
#   사람이 쓴 모집 카피 단락 45.5자 · 25자 미만 13.7% · 물음표 4
#   사람이 쓴 학술 산문        62.7자
#   C-11을 S1로 강제한 파이프라인 산출물 26.9~37.2자 · 27.4~61.1% · 물음표 0
RHYTHM_MIN_AVG   = 33.0   # 평균 문장길이 하한
RHYTHM_MAX_SHORT = 0.40   # 25자 미만 단문 비율 상한
RHYTHM_MAX_RUN   = 3      # 단문 3연속 구간 허용 개수
SHORT_CHARS      = 25


def judge_rhythm(m2, before: str, after: str, genre: str) -> tuple[str, str, dict[str, Any]]:
    """P5 — 문장 리듬. **C-11이 문장을 쪼개 단문화시키는 것을 막는다.**

    왜 이 축이 있는가: C-11(연결어미 뒤 쉼표 제거)은 S1이고 E-1·E-4(이웃한
    단문을 연결어미로 다시 묶기)는 S2다. `최소심각도: S1` 실행에서는 쪼개는
    규칙만 돌고 잇는 규칙은 안 돈다. 그 결과 개별 문장은 모두 자연스러운데
    글 전체가 26~31자 단문으로 수렴해 기계로 읽힌다 — 문장 단위 검사로는
    절대 잡히지 않는 실패 모드다.

    **E-5·C-12와 충돌하지 않는다.** E-5는 8어절 이상 절을, C-12는 쉼표
    과다 문장을 마침표로 나누라고 한다. 그 분리는 정당하므로, 문장 수 증가를
    무조건 실패로 보지 않고 **원문 장문(100자 이상)이 몇 개였는지로 귀속**해
    설명되지 않는 초과분만 잡는다.

    **카피·슬라이드 장르는 면제**한다(COPY_GENRES). 화면에 조각으로 뜨는
    글은 단문이 정상이며, 여기에 평균 33자를 들이대면 장르를 부순다.
    """
    # run()이 이미 정규화하지만, 이 함수를 직접 호출하는 경로도 있으므로
    # 여기서도 정규화한다(canonical_genre는 멱등이라 이중 적용이 무해하다).
    if canonical_genre(genre) in COPY_GENRES:
        return "SKIP", f"장르 '{genre}' — 의도적 단문이 정상이라 리듬 축을 적용하지 않는다", {}

    seg = m2._segment_sentences
    b, a = seg(before), seg(after)
    if len(a) < 12:
        return "SKIP", "문장 12개 미만 — 리듬을 판정할 표본이 아니다", {}

    L = [len(x) for x in a]
    avg = sum(L) / len(L)
    short = sum(1 for x in L if x < SHORT_CHARS) / len(L)
    run = runs = 0
    for x in L:
        if x < SHORT_CHARS:
            run += 1
        else:
            if run >= 3: runs += 1
            run = 0
    if run >= 3: runs += 1

    longest_run = 0
    cur = 0
    for x in L:
        cur = cur + 1 if x < SHORT_CHARS else 0
        longest_run = max(longest_run, cur)

    d = {"평균문장길이": round(avg, 1), "단문비율": round(short, 3),
         "스타카토구간": runs, "최장단문연속": longest_run,
         "문장수": [len(b), len(a)],
         "기준선": {"사람_모집카피_단락": [45.5, 0.137], "사람_학술산문": [62.7, None]}}

    # [HARD] 문장 수가 늘었다는 사실만으로 단문화라 부르지 않는다. E-5(8어절
    # 이상 절 분리)와 C-12(쉼표 과다 문장 분리)의 분리는 정당하고, before/after
    # 두 파일만으로는 어느 규칙이 나눴는지 귀속할 수 없다(codex finding 1).
    # 문장 수 변화는 사실로만 싣고, '의심'은 리듬 지표가 실제로 짧을 때만 단다.
    hint = []
    if avg < RHYTHM_MIN_AVG:
        hint.append(f"평균 {avg:.1f}자 < 참고 하한 {RHYTHM_MIN_AVG}자")
    if short > RHYTHM_MAX_SHORT:
        hint.append(f"25자 미만 {short:.1%} > 참고 상한 {RHYTHM_MAX_SHORT:.0%}")
    if longest_run > RHYTHM_MAX_RUN:
        hint.append(f"단문 최장 {longest_run}연속")
    if hint and len(a) > len(b):
        hint.append(f"문장이 {len(b)}→{len(a)}개로 늘었다(원인 귀속은 정독이 한다)")

    d["단문화_의심"] = bool(hint)
    note = (f"평균 {avg:.1f}자 · 단문 {short:.1%} · 최장 {longest_run}연속"
            + (f" — 단문화 의심: {' / '.join(hint)}. **판정은 Phase 2.5 정독 소견과 "
               f"Phase 6 정독 재판정이 한다**(이 축은 그쪽이 볼 곳을 가리킬 뿐이다)."
               if hint else " — 참고 기준선 안"))
    return "REPORT", note, d


def run(before: str, after: str, genre: str = "essay",
        ignore_markup: bool = False,
        baseline: Optional[str] = None,
        baseline_v2: Optional[str] = None) -> dict[str, Any]:
    m2 = _load("metrics_v2")
    ck = _load("checks")
    # [HARD] 여기서 한 번만 정규화한다. 축마다 따로 하면 축마다 다른 장르가
    # 된다 — 실측: `카피`가 P0/P5에서는 카피로, P3에서는 산문으로 판정돼
    # emoji_residue FAIL이 났다(2026-08-27 codex finding 4).
    display_genre = genre
    genre = canonical_genre(genre)

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
    p5_s, p5_n, p5_d = judge_rhythm(m2, before, after, genre)

    if p0_s == "ABORT":
        verdict, code = "ABORT", EXIT_ABORT
    elif "WARN" in (p0_s, p1_s, p3_s) or "FAIL" in (p2_s, p3_s):
        verdict, code = "WARN", EXIT_WARN
    elif p5_d.get("단문화_의심"):
        # [HARD] fail-closed. P5는 보편 임계 게이트가 아니지만(표본 부족),
        # 의심이 뜬 글을 "게이트가 봤고 괜찮다더라"로 흘려보내지도 않는다.
        # 통과시키려면 Phase 6 정독 재판정이 근거를 적고 accept를 내야 한다.
        # 앞선 감사에서 문장 20→40 반례가 PASS/exit 0을 받은 경로가 여기다.
        verdict, code = "INCONCLUSIVE", EXIT_WARN
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
        "genre_input": display_genre,
        "axes": {
            "P0_문자율": {"status": p0_s, "note": p0_n,
                          "value": round(rate, 4), "마크업제외": round(rate_nm, 4)},
            "P1_목표달성": {"status": p1_s, "notes": p1_n},
            "P2_전멸": {"status": p2_s, "note": p2_n},
            "P3_불변식": {"status": p3_s, "note": p3_n, "detail": p3_d},
            "P4_터치율": {"status": "REPORT",
                          "note": f"원문 문장 {touched}/{total}개가 그대로 남지 않았다 ({touch:.1%})"},
            "P5_리듬": {"status": p5_s, "note": p5_n, "detail": p5_d},
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
    ap = _GateArgParser(description="korean-humanize 구조 게이트 (5축)")
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
