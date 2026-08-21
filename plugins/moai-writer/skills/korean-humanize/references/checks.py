#!/usr/bin/env python3
"""윤문 전후 불변식 검사 — 결정적 코드, LLM 콜 0.

verify_gates.py의 P3축이 호출한다. 여기서 보는 것은 **의미가 아니라
증거로 남는 표층 불변식**이다 — 수치·직접 인용·이모지 잔존·격식 혼재.
의미 보존 자체는 사람이나 finalize 콜이 판정할 몫이며, 이 파일이 통과했다고
"의미가 보존됐다"고 말하면 안 된다.

각 검사는 (통과 여부, 사람이 읽는 사유)를 돌려주고, 왜 그런 판정을 했는지
근거가 되는 항목을 함께 싣는다. 판정을 뒤집을 수 있게 하려는 것이다.

표준 라이브러리만 쓴다.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any

# 수치 — 부호를 포함해 센다. 부호를 빼면 -5%가 5%로 바뀌어도 통과한다
# (감사에서 재현됨). 앞의 마이너스(ASCII/유니코드)를 캡처에 넣는다.
_NUMBER_RE = re.compile(r"[-−–]?\d[\d,._]*%?")
# 직접 인용 — 큰따옴표 계열만. 작은따옴표는 개념 강조로도 쓰여 제외한다.
_QUOTE_RE = re.compile(r"[\"“]([^\"”\n]{2,300})[\"”]")

# 큰따옴표 안이라고 다 인용은 아니다. `"AI 티"`처럼 한 낱말을 감싼 것은
# 개념 강조이고, 윤문이 용어를 바꾸는 것은 정상이다. 이걸 인용으로 보면
# 정상 윤문이 FAIL을 받는다(감사에서 재현됨). 인용으로 보호할 조건:
#   - 2어절 이상이거나
#   - 문장부호로 끝나거나
#   - 12자 이상
# 그 아래는 강조로 보고 REPORT만 한다.
# 인용인가 강조인가를 가르는 기준은 길이가 아니라 **서술어로 끝나는가**다.
# 한국어에서 따옴표 안이 절·문장이면 인용이고("속도를 포기하지 않는다"),
# 명사구로 끝나면 개념 강조다("AI 티"). 어절 수로 재면 세 어절짜리 인용을
# 놓치거나 두 어절짜리 용어를 인용으로 붙잡는다 — 둘 다 겪었다.
_PREDICATE_END_RE = re.compile(
    r"(?:다|요|까|죠|네|군|라|자|오|음|슴|니다|습니다|입니다)$"
)


def _is_citation(span: str) -> bool:
    span = span.strip().rstrip("\"'“”‘’")
    if re.search(r"[.!?。]$", span):
        return True                       # 문장부호로 끝나면 인용
    if _PREDICATE_END_RE.search(span):
        return True                       # 서술어로 끝나면 절·문장 = 인용
    return len(span) >= 20                # 아주 길면 용어일 리 없다
# 이모지 — 주요 픽토그래픽 블록.
# 이모지 — 픽토그래픽 블록만. U+2600~27BF 전체를 넣으면 ★(U+2605)·✓·→ 같은
# 평범한 활자 기호까지 이모지로 잡힌다(감사에서 재현됨). 실제로 AI 산출물에
# 나오는 것들만 좁혀 지정한다.
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F5FF"   # 기호·픽토그램
    "\U0001F600-\U0001F64F"   # 얼굴
    "\U0001F680-\U0001F6FF"   # 교통·기호
    "\U0001F900-\U0001FAFF"   # 보충 픽토그램
    "\U00002705"               # ✅
    "\U0000274C"               # ❌
    "\U000026A0"               # ⚠
    "\U0001F4A1"               # 💡
    "]"
)
# 격식 종결 — 합쇼체 / 해라체. 한 문서에 섞이면 E-7 후보.
_HAPSYO_RE = re.compile(r"(?:습니다|입니다|합니다|십시오)[.!?]")
# 합쇼체(`~습니다.`)도 `[가-힣]다.`에 걸려 해라체로 세지던 버그가 있었다.
# 그러면 격식이 일관된 문서가 항상 "혼재"로 보고된다(감사에서 재현됨).
# 앞이 `니`/`시`면 합쇼체이므로 제외한다.
# lookbehind는 `다` 바로 앞을 봐야 한다. 앞 버전은 한 음절 더 앞을 봐서
# `입니다.`가 그대로 해라체로 세졌다(감사에서 재현됨).
_HAERA_RE = re.compile(r"[가-힣](?<!니)(?<!시)다[.!?]")


def _norm(text: str) -> str:
    """비교 전 정규화 — NFC + 공백 접기. 표기 차이로 인한 가짜 손실을 막는다."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def check_numbers(before: str, after: str) -> dict[str, Any]:
    """원문에 있던 수치가 윤문본에서 사라졌는가.

    **경고이지 실패가 아니다.** 두 문장을 합치면서 중복 수치를 하나로 줄이는
    것은 정상 편집이다. 사라진 항목을 열거해 사람이 하나씩 확인하게 한다.
    """
    b = Counter(_NUMBER_RE.findall(_norm(before)))
    a = Counter(_NUMBER_RE.findall(_norm(after)))
    lost = sorted((b - a).elements())
    return {
        "name": "numbers",
        "status": "WARN" if lost else "PASS",
        "lost": lost,
        "reason": (
            f"수치 {len(lost)}건이 윤문본에서 발견되지 않았다: {lost[:8]}. "
            "문장 병합으로 중복 수치가 줄어든 것일 수 있으니 하나씩 확인할 것."
            if lost else "수치 전부 보존"
        ),
    }


def check_quotations(before: str, after: str) -> dict[str, Any]:
    """직접 인용이 글자 그대로 남아 있는가.

    **실패다.** 직접 인용은 100% 보존 대상이며, 변형은 사실 왜곡이다.
    """
    a_norm = _norm(after)
    spans = [_norm(q) for q in _QUOTE_RE.findall(before)]
    lost_cit = [q for q in spans if _is_citation(q) and q not in a_norm]
    lost_emph = [q for q in spans if not _is_citation(q) and q not in a_norm]
    if lost_cit:
        status = "FAIL"
        reason = (f"직접 인용 {len(lost_cit)}건이 원문 그대로 남아 있지 않다. "
                  "인용은 글자 단위 보존 대상이다.")
    elif lost_emph:
        status = "REPORT"
        reason = (f"강조 따옴표 {len(lost_emph)}건이 바뀌었다: {lost_emph[:5]}. "
                  "용어 교체라면 정상이니 확인만 할 것.")
    else:
        status = "PASS"
        reason = "직접 인용 전부 보존"
    return {
        "name": "quotations",
        "status": status,
        "lost": lost_cit[:10],
        "changed_emphasis": lost_emph[:10],
        "reason": reason,
    }


def check_emoji_residue(after: str, genre: str = "essay") -> dict[str, Any]:
    """C-5 이모지가 남아 있는가. 칼럼·리포트 장르에서만 실패로 본다."""
    hits = _EMOJI_RE.findall(after)
    applies = genre not in ("copy", "social", "sns")
    status = "FAIL" if (hits and applies) else ("REPORT" if hits else "PASS")
    return {
        "name": "emoji_residue",
        "status": status,
        "count": len(hits),
        "reason": (
            f"이모지 {len(hits)}개 잔존 (장르={genre}). C-5는 S1이다."
            if hits else "이모지 없음"
        ),
    }


def check_register_mix(after: str) -> dict[str, Any]:
    """E-7 격식 혼재 — 합쇼체와 해라체가 한 문서에 섞였는가.

    **보고이지 실패가 아니다.** 인용된 대화가 섞이는 것은 정상이고, 표층
    정규식으로는 인용 안팎을 가르지 못한다. 사람이 볼 근거만 제공한다.
    """
    hap = len(_HAPSYO_RE.findall(after))
    hae = len(_HAERA_RE.findall(after))
    minor = min(hap, hae)
    mixed = minor >= 2 and minor / max(hap + hae, 1) > 0.15
    return {
        "name": "register_mix",
        "status": "REPORT",
        "hapsyo": hap,
        "haera": hae,
        "reason": (
            f"격식 혼재 가능성: 합쇼체 {hap} / 해라체 {hae}. "
            "인용 대화라면 정상이니 확인만 할 것."
            if mixed else f"격식 일관 (합쇼체 {hap} / 해라체 {hae})"
        ),
    }


def run_checks(before: str, after: str, genre: str = "essay") -> dict[str, Any]:
    """전 검사를 돌리고 (실패 목록, 경고 목록, 전체 결과)를 돌려준다."""
    results = [
        check_numbers(before, after),
        check_quotations(before, after),
        check_emoji_residue(after, genre),
        check_register_mix(after),
    ]
    return {
        "results": results,
        "failed": [r["name"] for r in results if r["status"] == "FAIL"],
        "warned": [r["name"] for r in results if r["status"] == "WARN"],
        "reported": [r["name"] for r in results if r["status"] == "REPORT"],
        "caveat": (
            "표층 불변식만 본다. 이 검사가 전부 통과해도 '의미가 보존됐다'는 "
            "뜻은 아니다 — 의미 보존은 원문 대조로 따로 판정해야 한다."
        ),
    }
