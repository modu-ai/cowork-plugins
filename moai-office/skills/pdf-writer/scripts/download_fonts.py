#!/usr/bin/env python3
"""
Noto Sans CJK 폰트 자동 다운로드 스크립트.

pdf-writer 스킬 최초 실행 시 폰트 부재를 감지하면 자동 호출됩니다.
notofonts/noto-cjk 공식 저장소에서 한국어 변형(KR) 4종 weight를 가져옵니다.

사용법:
    python3 scripts/download_fonts.py            # 누락된 폰트만 다운로드
    python3 scripts/download_fonts.py --force    # 전체 재다운로드
    python3 scripts/download_fonts.py --check    # 다운로드 없이 상태만 확인

종료 코드:
    0 — 모든 폰트 정상 (혹은 다운로드 성공)
    1 — 다운로드 실패 (네트워크/URL/권한)
    2 — 사용법 오류
"""
from __future__ import annotations

import sys
import urllib.request
import urllib.error
from pathlib import Path

# 한국어 변형(KR) — 한·중·일·영 글리프 모두 커버, 한국어 디자인 우선
BASE_URL = "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Korean"
WEIGHTS = ["Light", "Regular", "Medium", "Bold"]
EXPECTED_MIN_SIZE = 10 * 1024 * 1024  # 10MB — 정상 OTF는 약 16MB

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"


def font_path(weight: str) -> Path:
    return FONT_DIR / f"NotoSansCJK-{weight}.otf"


def is_valid(path: Path) -> bool:
    """파일 존재 + 최소 크기 + OTF 매직바이트 확인."""
    if not path.exists():
        return False
    if path.stat().st_size < EXPECTED_MIN_SIZE:
        return False
    with path.open("rb") as f:
        magic = f.read(4)
    # OTF 매직: 'OTTO' (CFF 기반) 또는 0x00010000 (TrueType)
    return magic == b"OTTO" or magic == b"\x00\x01\x00\x00"


def download_one(weight: str, force: bool = False) -> bool:
    dest = font_path(weight)
    if not force and is_valid(dest):
        print(f"  [SKIP] {dest.name} 이미 정상 ({dest.stat().st_size:,} bytes)")
        return True

    src = f"{BASE_URL}/NotoSansCJKkr-{weight}.otf"
    print(f"  [DL]   {weight}: {src}")
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(src, timeout=60) as resp:
            data = resp.read()
        dest.write_bytes(data)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f"  [FAIL] {weight}: {e}", file=sys.stderr)
        return False

    if not is_valid(dest):
        print(f"  [FAIL] {weight}: 다운로드 파일이 OTF 형식이 아님", file=sys.stderr)
        try:
            dest.unlink()
        except OSError:
            pass
        return False

    print(f"  [OK]   {dest.name} ({dest.stat().st_size:,} bytes)")
    return True


def status_report() -> int:
    """전체 폰트 상태 점검만 실행 — 다운로드 없음."""
    print(f"폰트 디렉토리: {FONT_DIR}")
    missing: list[str] = []
    for w in WEIGHTS:
        p = font_path(w)
        if is_valid(p):
            print(f"  [OK]      {p.name} ({p.stat().st_size:,} bytes)")
        else:
            print(f"  [MISSING] {p.name}")
            missing.append(w)
    if missing:
        print(f"\n누락 weight: {', '.join(missing)}")
        print("→ 다운로드: python3 scripts/download_fonts.py")
        return 1
    print("\n모든 폰트 정상.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] not in ("--force", "--check"):
        print(f"사용법: {argv[0]} [--force | --check]", file=sys.stderr)
        return 2

    mode = argv[1] if len(argv) > 1 else ""

    if mode == "--check":
        return status_report()

    force = mode == "--force"
    print(f"Noto Sans CJK KR 4종 다운로드 시작 (force={force})")
    print(f"대상 디렉토리: {FONT_DIR}\n")

    failed = [w for w in WEIGHTS if not download_one(w, force=force)]

    print()
    if failed:
        print(f"실패: {', '.join(failed)}", file=sys.stderr)
        return 1
    print("모든 폰트 다운로드 완료.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
