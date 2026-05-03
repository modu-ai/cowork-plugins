#!/usr/bin/env python3
# 바른한글(nara-speller) 한국어 맞춤법 검사 helper
# 출처: NomaDamas/k-skill (MIT) — korean-spell-check
# 비상업·저빈도 사용 정책 준수. 1500자 청크 분할 + 청크 간 1초 휴지.

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)
URL = "https://nara-speller.co.kr/old_speller/results"
CHUNK_SIZE = 1500
SLEEP_BETWEEN = 1.0


def post(text: str) -> str:
    data = urllib.parse.urlencode({"text1": text}).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={
            "User-Agent": UA,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse(html: str) -> list[dict]:
    matches = re.findall(r"data\s*=\s*(\{.*?\});", html, flags=re.DOTALL)
    results: list[dict] = []
    for raw in matches:
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for entry in obj.get("errInfo", []) or []:
            results.append(
                {
                    "original": unescape(entry.get("orgStr", "")),
                    "suggestions": [unescape(s) for s in (entry.get("candWord", "") or "").split("|") if s],
                    "reason": unescape(entry.get("help", "")),
                }
            )
    return results


def chunked(text: str, size: int = CHUNK_SIZE):
    for i in range(0, len(text), size):
        yield text[i : i + size]


def check(text: str) -> list[dict]:
    out: list[dict] = []
    for i, chunk in enumerate(chunked(text)):
        if i > 0:
            time.sleep(SLEEP_BETWEEN)
        html = post(chunk)
        out.extend(parse(html))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Korean spell check via nara-speller")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="검사할 텍스트")
    src.add_argument("--file", help="검사할 UTF-8 텍스트 파일")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    args = ap.parse_args()

    text = args.text if args.text else Path(args.file).read_text(encoding="utf-8")
    results = check(text)

    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"원문: {r['original']}")
            print(f"교정: {', '.join(r['suggestions']) or '(제안 없음)'}")
            print(f"이유: {r['reason']}")
            print("-" * 40)
    return 0


if __name__ == "__main__":
    sys.exit(main())
