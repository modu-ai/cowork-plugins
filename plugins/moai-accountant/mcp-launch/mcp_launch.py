# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""제3자 MCP 서버를 자격증명과 함께 띄우는 런처.

## 왜 필요한가

`.mcp.json` 의 `"env": {"KEY": "${KEY}"}` 는 **네 실행 환경 중 세 곳에서 확장되지 않는다**
(2026-09-03 실측: Claude 데스크톱·Codex CLI·Codex 데스크톱). 자체 제작 서버는
`moai_mcp_core.CredentialStore` 로 직접 해결했지만, 제3자 서버(korean-dart-mcp,
elevenlabs-mcp 등)는 코드를 고칠 수 없다.

그래서 그 앞에 이 런처를 세운다. 런처가 `~/.moai/mcp/<서비스>.json` 을 읽어 **진짜 값을
환경변수에 채운 뒤** 원래 서버를 그대로 실행한다. 제3자 서버는 자기가 늘 기대하던
환경변수를 받으므로 아무것도 달라지지 않는다.

## 사용

    uv run --script mcp_launch.py --service dart --keys DART_API_KEY -- npx -y korean-dart-mcp

`--` 뒤가 원래 서버의 실행 명령이다. 런처는 그 명령을 **대체 실행**하므로(가능한 곳에서는
`os.execvp`) 프로세스가 하나 더 남지 않고, stdio 파이프도 그대로 이어진다.

## 값의 우선순위

1. 이미 들어 있는 환경변수 — 단, 확장되지 않은 `${...}` 자리표시자와 빈 값은 없는 것으로 본다
2. `~/.moai/mcp/<서비스>.json`
3. 없으면 그 키는 설정하지 않는다 — 제3자 서버가 자기 방식으로 안내하게 둔다

의존성이 없어야 `uv run --script` 가 네트워크 없이 즉시 뜬다. 표준 라이브러리만 쓴다.
경로는 macOS·Windows 양쪽에서 같게 동작하도록 pathlib 으로만 조립한다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

#: 자격증명 파일이 모여 있는 곳. moai_mcp_core.tokenstore.DEFAULT_DIR 과 같은 위치다.
CREDENTIALS_DIR = Path.home() / ".moai" / "mcp"

#: 확장되지 않은 자리표시자. `${KEY}` · `${user_config.KEY}` 양쪽을 잡는다.
_PLACEHOLDER_RE = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_.]*\}$")


def is_unset(value: str | None) -> bool:
    """`None`, 빈 값, 확장되지 않은 `${...}` 는 모두 '설정되지 않음'."""
    if value is None:
        return True
    stripped = value.strip()
    if not stripped:
        return True
    return bool(_PLACEHOLDER_RE.match(stripped))


def read_credentials(service: str) -> dict[str, str]:
    """`~/.moai/mcp/<service>.json` 을 읽는다. 없거나 깨졌으면 빈 사전."""
    path = CREDENTIALS_DIR / f"{service}.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(payload, dict):
        return {}
    return {str(k): str(v) for k, v in payload.items() if v is not None}


def resolve_env(service: str, keys: list[str]) -> dict[str, str]:
    """자식 프로세스에 넘길 환경을 만든다.

    자리표시자가 들어 있던 키는 **지운다**. 남겨두면 제3자 서버가 그것을 진짜 키로
    믿고 인증에 실패하는데, 그 실패는 "키가 틀렸다" 로 보이지 "키가 없다" 로 보이지 않는다.
    """
    env = dict(os.environ)
    stored = read_credentials(service)

    for key in keys:
        current = env.get(key)
        if not is_unset(current):
            continue  # 이미 진짜 값이 들어 있다
        value = stored.get(key)
        if is_unset(value):
            env.pop(key, None)
        else:
            env[key] = value.strip()  # type: ignore[union-attr]

    return env


def main() -> int:
    parser = argparse.ArgumentParser(
        description="제3자 MCP 서버를 ~/.moai/mcp/<서비스>.json 의 자격증명과 함께 실행한다.",
    )
    parser.add_argument("--service", required=True, help="자격증명 파일 슬러그 (예: dart)")
    parser.add_argument(
        "--keys",
        required=True,
        help="채울 환경변수 이름들, 쉼표로 구분 (예: DART_API_KEY)",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="`--` 뒤에 원래 서버의 실행 명령",
    )
    args = parser.parse_args()

    command = [part for part in args.command if part != "--"]
    if not command:
        parser.error("실행할 명령이 없습니다. `--` 뒤에 원래 서버 명령을 적으세요.")

    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    env = resolve_env(args.service, keys)

    if os.name == "nt":
        # Windows 에는 execvp 의 프로세스 대체 의미가 없다(부모가 먼저 끝나면 콘솔이
        # 자식을 거둬간다). 자식을 낳고 그 종료코드를 그대로 물려준다.
        return subprocess.run(command, env=env, check=False).returncode

    try:
        os.execvpe(command[0], command, env)
    except OSError as error:
        print(f"[mcp-launch] {command[0]} 를 실행하지 못했습니다: {error}", file=sys.stderr)
        return 127
    return 0  # execvpe 가 성공하면 여기에 오지 않는다


if __name__ == "__main__":
    raise SystemExit(main())
