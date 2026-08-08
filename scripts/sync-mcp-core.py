#!/usr/bin/env python3
"""moai-mcp-core 정본을 각 MCP 서버로 복제한다.

플러그인은 각자 독립 설치되므로 런타임에 `plugins/_shared/` 를 참조할 수 없다.
그래서 코어를 각 서버 안으로 복제한다(vendor). 유일한 위험은 복제본 드리프트이고,
이 스크립트가 그것을 기계적으로 막는다.

    python3 scripts/sync-mcp-core.py            # 정본 → 채택한 서버 전체로 복제
    python3 scripts/sync-mcp-core.py --check    # 드리프트 검사 (불일치면 종료코드 1)
    python3 scripts/sync-mcp-core.py --adopt plugins/moai-youtuber/mcp-servers/moai-youtube

**채택(adopt)은 명시적이다.** 서버의 pyproject `packages` 에 `src/moai_mcp_core` 가
들어 있는 서버만 동기화 대상이 된다. 아직 코어로 이관하지 않은 서버를 건드리지 않기 위해서다.

설계 근거: `.moai/reports/mcp-naming-consolidation-design.md` §4-1.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = REPO_ROOT / "plugins" / "_shared" / "moai-mcp-core" / "moai_mcp_core"
PACKAGE_NAME = "moai_mcp_core"
VENDOR_MARKER = f"src/{PACKAGE_NAME}"

BANNER = (
    "# 이 파일은 자동 생성된 복제본입니다 — 직접 수정하지 마세요.\n"
    "# 정본: plugins/_shared/moai-mcp-core/{name}\n"
    "# 동기화: python3 scripts/sync-mcp-core.py\n"
)


def canonical_files() -> list[Path]:
    if not CANONICAL.is_dir():
        raise SystemExit(f"정본을 찾을 수 없습니다: {CANONICAL}")
    return sorted(p for p in CANONICAL.glob("*.py"))


def expected_content(source: Path) -> str:
    """복제본에 들어가야 할 내용(배너 + 정본 본문)."""
    body = source.read_text(encoding="utf-8")
    return BANNER.format(name=source.name) + body


def find_servers() -> list[Path]:
    """코어를 채택한 서버 디렉터리 목록."""
    servers = []
    for pyproject in sorted(REPO_ROOT.glob("plugins/*/mcp-servers/*/pyproject.toml")):
        if VENDOR_MARKER in pyproject.read_text(encoding="utf-8"):
            servers.append(pyproject.parent)
    return servers


def sync_server(server: Path, *, check_only: bool) -> list[str]:
    """서버 하나를 동기화하거나 검사한다.

    Returns:
        불일치 항목 설명 목록. 비어 있으면 정합.
    """
    target_dir = server / "src" / PACKAGE_NAME
    problems: list[str] = []
    sources = canonical_files()
    expected_names = {s.name for s in sources}

    if not check_only:
        target_dir.mkdir(parents=True, exist_ok=True)

    for source in sources:
        target = target_dir / source.name
        wanted = expected_content(source)
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == wanted:
            continue
        rel = target.relative_to(REPO_ROOT)
        if check_only:
            problems.append(f"{'누락' if current is None else '불일치'}: {rel}")
        else:
            target.write_text(wanted, encoding="utf-8")

    # 정본에서 삭제된 모듈이 복제본에 남아 있으면 유령 코드가 된다.
    if target_dir.is_dir():
        for stale in sorted(target_dir.glob("*.py")):
            if stale.name in expected_names:
                continue
            rel = stale.relative_to(REPO_ROOT)
            if check_only:
                problems.append(f"잔존(정본에 없음): {rel}")
            else:
                stale.unlink()

    return problems


def adopt(server: Path) -> None:
    """서버가 코어를 쓰도록 pyproject 를 고치고 첫 복제를 수행한다."""
    pyproject = server / "pyproject.toml"
    if not pyproject.is_file():
        raise SystemExit(f"pyproject.toml 이 없습니다: {pyproject}")

    text = pyproject.read_text(encoding="utf-8")
    if VENDOR_MARKER in text:
        print(f"이미 채택됨: {server.relative_to(REPO_ROOT)}")
    else:
        marker = "packages = ["
        index = text.find(marker)
        if index == -1:
            raise SystemExit(
                f"packages 항목을 찾을 수 없습니다. 수동으로 추가하세요: {pyproject}"
            )
        insert_at = index + len(marker)
        text = f'{text[:insert_at]}"{VENDOR_MARKER}", {text[insert_at:]}'
        pyproject.write_text(text, encoding="utf-8")
        print(f"채택 완료: {server.relative_to(REPO_ROOT)} (pyproject packages 갱신)")

    sync_server(server, check_only=False)
    print(f"  복제: src/{PACKAGE_NAME}/ ({len(canonical_files())}개 모듈)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="복제하지 않고 드리프트만 검사")
    parser.add_argument("--adopt", metavar="서버경로", help="서버가 코어를 쓰도록 채택")
    args = parser.parse_args()

    if args.adopt:
        path = Path(args.adopt)
        adopt(path if path.is_absolute() else REPO_ROOT / path)
        return 0

    servers = find_servers()
    if not servers:
        print("코어를 채택한 서버가 아직 없습니다. --adopt 로 채택하세요.")
        return 0

    all_problems: list[str] = []
    for server in servers:
        problems = sync_server(server, check_only=args.check)
        rel = server.relative_to(REPO_ROOT)
        if args.check:
            status = "불일치" if problems else "정합"
            print(f"[{status}] {rel}")
            all_problems.extend(problems)
        else:
            print(f"동기화: {rel}")

    if args.check and all_problems:
        print("\n드리프트가 발견되었습니다:", file=sys.stderr)
        for problem in all_problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            "\n해결: python3 scripts/sync-mcp-core.py 를 실행하고 함께 커밋하세요.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
