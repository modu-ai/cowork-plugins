#!/usr/bin/env python3
"""텍스트 위생 — 결정적 전처리, LLM 콜 0.

윤문 **전에** 입력을 한 번 정돈해, 이후의 변경률·diff·글자 수가 모두 같은
기준을 쓰게 한다. 눈에 보이지 않는 문자가 섞여 있으면 사람이 보기엔 똑같은
글이 코드에겐 다른 글이 되고, 그러면 변경률 게이트가 헛돈다.

하는 일:
  1. 제로폭 문자 제거 (U+200B~U+200D, U+FEFF, U+2060)
  2. 양방향 제어 문자 제거 (U+202A~U+202E, U+2066~U+2069)
  3. 특수 공백을 보통 공백으로 (U+00A0, U+2000~U+200A, U+202F, U+205F, U+3000)
  4. 한글 NFD → NFC 정규화 (자모 분리 표기를 완성형으로)
  5. 줄 끝 공백 제거, CRLF → LF

**[중요] 이것은 AI 워터마크 제거 기능이 아니다.** 목적은 측정 기준을 하나로
맞추는 것이고, 부수 효과로 일부 비가시 문자가 사라질 뿐이다. 탐지 회피
도구로 쓰거나 그렇게 소개하지 않는다. macOS 파일명처럼 NFD가 정상인
맥락도 있으므로, 정규화는 **본문 텍스트에만** 적용한다.

사용:
    python3 sanitize_text.py --input in.txt --output out.txt
    python3 sanitize_text.py --input in.txt --report        # 무엇이 바뀌는지만
    cat in.txt | python3 sanitize_text.py                   # stdin → stdout

종료 코드: 0 성공, 2 입출력 오류.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import unicodedata
from typing import Any

# 제로폭 — 붙여넣기로 흘러드는 대표적 비가시 문자.
# **U+200D(ZWJ)와 U+200C(ZWNJ)는 지우지 않는다.** ZWJ는 👩‍💻 같은 이모지
# 결합 시퀀스의 접착제라 지우면 한 글자가 둘로 쪼개진다. ZWNJ도 일부 문자
# 체계에서 의미를 가진다. 순수 잡음인 셋만 제거한다.
ZERO_WIDTH = "​⁠﻿"
# 양방향 제어 — 표시 순서를 바꿔 눈속임이 가능하다.
BIDI_CONTROL = "‪‫‬‭‮⁦⁧⁨⁩"
# 특수 공백 — 보통 공백으로 접는다. U+3000(전각 공백)도 포함.
SPECIAL_SPACES = (
    "          "
    "     　"
)

_ZERO_WIDTH_RE = re.compile(f"[{ZERO_WIDTH}]")
_BIDI_RE = re.compile(f"[{BIDI_CONTROL}]")
_SPACE_RE = re.compile(f"[{SPECIAL_SPACES}]")

# 자릿수 구분자 보호. 숫자 사이의 비분리 공백은 "10 000원"처럼 표기의 일부라
# 보통 공백으로 접으면 표기가 바뀐다(감사에서 재현됨). 접기 전에 빼두고
# 접은 뒤 되돌린다.
_DIGIT_NBSP_RE = re.compile("(?<=\\d)[\u00a0\u202f\u2007](?=\\d)")
_NBSP_PLACEHOLDER = "\x00NBSP\x00"

# 줄 끝 공백 — **정확히 두 칸은 마크다운 강제 개행**이므로 남긴다.
# 한 칸, 셋 칸 이상, 탭이 섞인 것만 잡음으로 보고 지운다.
_TRAILING_WS_RE = re.compile(r"(?<![ \t])[ \t]$|[ \t]{3,}$|\t[ \t]*$", re.MULTILINE)


def sanitize(text: str) -> tuple[str, dict[str, Any]]:
    """정돈된 텍스트와 무엇을 몇 개 고쳤는지 리포트를 함께 돌려준다."""
    original = text
    report: dict[str, Any] = {}

    hits = _ZERO_WIDTH_RE.findall(text)
    if hits:
        report["zero_width_removed"] = len(hits)
        text = _ZERO_WIDTH_RE.sub("", text)

    hits = _BIDI_RE.findall(text)
    if hits:
        report["bidi_control_removed"] = len(hits)
        text = _BIDI_RE.sub("", text)

    text, guarded_n = _DIGIT_NBSP_RE.subn(_NBSP_PLACEHOLDER, text)
    hits = _SPACE_RE.findall(text)
    if hits:
        report["special_spaces_folded"] = len(hits)
        text = _SPACE_RE.sub(" ", text)
    if guarded_n:
        report["digit_separators_preserved"] = guarded_n
        text = text.replace(_NBSP_PLACEHOLDER, "\u00a0")

    if "\r\n" in text or "\r" in text:
        report["crlf_normalized"] = text.count("\r\n") + text.count("\r")
        text = text.replace("\r\n", "\n").replace("\r", "\n")

    normalized = unicodedata.normalize("NFC", text)
    if normalized != text:
        report["nfc_normalized"] = True
        report["nfc_char_delta"] = len(text) - len(normalized)
        text = normalized

    stripped = _TRAILING_WS_RE.sub("", text)
    if stripped != text:
        report["trailing_whitespace_lines"] = len(_TRAILING_WS_RE.findall(text))
        text = stripped

    report["changed"] = text != original
    report["chars_before"] = len(original)
    report["chars_after"] = len(text)
    report["note"] = (
        "측정 기준을 하나로 맞추는 전처리다. AI 워터마크 제거 기능이 아니며, "
        "탐지 회피 목적으로 쓰지 않는다."
    )
    return text, report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="korean-humanize 텍스트 위생")
    ap.add_argument("--input", help="입력 파일 (생략 시 stdin)")
    ap.add_argument("--output", help="출력 파일 (생략 시 stdout)")
    ap.add_argument("--report", action="store_true", help="본문 대신 변경 리포트만 출력")
    args = ap.parse_args(argv)

    try:
        if args.input:
            with open(args.input, encoding="utf-8") as fh:
                raw = fh.read()
        else:
            raw = sys.stdin.read()
    except OSError as exc:
        print(f"읽기 실패: {exc}", file=sys.stderr)
        return 2

    cleaned, report = sanitize(raw)

    if args.report:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    try:
        if args.output:
            # **원자적 쓰기.** 입력=출력으로 부르는 것이 정상 사용법이라
            # (SKILL.md Phase 1), 쓰는 도중 중단되면 원본이 잘린 채 남는다.
            # 같은 디렉터리 임시 파일에 다 쓰고 교체한다.
            d = os.path.dirname(os.path.abspath(args.output)) or "."
            fd, tmp = tempfile.mkstemp(dir=d, prefix=".sanitize-", suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    fh.write(cleaned)
                    fh.flush()
                    os.fsync(fh.fileno())
                os.replace(tmp, args.output)
            except BaseException:
                if os.path.exists(tmp):
                    os.unlink(tmp)
                raise
            if report["changed"]:
                print(json.dumps(report, ensure_ascii=False), file=sys.stderr)
        else:
            sys.stdout.write(cleaned)
    except OSError as exc:
        print(f"쓰기 실패: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
