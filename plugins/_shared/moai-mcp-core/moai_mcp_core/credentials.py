"""사용자 자격증명(API 키·토큰)의 해석.

## 왜 필요한가

`.mcp.json` 의 `"env": {"KEY": "${KEY}"}` 로 자격증명을 나르는 방식은 **네 실행 환경 중
세 곳에서 동작하지 않는다**(2026-09-03 실측):

| 실행 환경 | `${KEY}` 확장 |
|---|---|
| Claude Code CLI | 확장됨 (셸에 export 된 경우에 한해) |
| Claude 데스크톱 앱 | **안 됨** — 서버가 문자열 `"${KEY}"` 를 그대로 받는다 |
| Codex CLI | **안 됨** — 동일 |
| Codex 데스크톱 앱 | **안 됨** — 동일 |

게다가 비개발자는 셸에 export 할 수 없다. 그래서 자격증명은 환경변수 하나에 의존하지
않고 **여러 출처를 순서대로 훑어** 해석한다.

## 우선순위

1. **환경변수** — 값이 실제로 들어 있을 때만. Claude 의 `${user_config.KEY}` 가 채워진
   경우, `codex mcp add --env` 로 넣은 경우, 개발자가 셸에 export 한 경우가 여기 해당한다.
2. **자격증명 파일** — `~/.moai/mcp/<service>.json`. 설정 스킬이 대화로 물어보고 적는다.
   런타임과 무관하므로 네 실행 환경 모두에서 동일하게 동작한다.
3. **기본값** — 호출부가 준 값. 없으면 빈 문자열.

## '값 없음' 의 판정

환경변수가 **존재하는데도 값 없음으로 취급**해야 하는 경우가 둘 있다. 이 판정이 이 모듈의
핵심이며, 지금까지의 결함이 정확히 여기서 났다.

- `"${NAVER_COMMERCE_CLIENT_ID}"` — 확장되지 않은 자리표시자. 위 표의 세 환경이 이 값을
  넘긴다. 이걸 진짜 키로 믿으면 서버는 정상 기동한 뒤 모든 호출이 401 로 실패한다.
- `""` — Claude 의 `${user_config.KEY}` 는 사용자가 아직 입력하지 않았을 때 빈 문자열로
  치환된다(실측). 빈 값은 미설정이지 설정된 빈 키가 아니다.

경로는 macOS·Windows 양쪽에서 같게 동작하도록 pathlib 으로만 조립한다.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from .tokenstore import DEFAULT_DIR

#: 확장되지 않은 자리표시자. `${KEY}` · `${user_config.KEY}` 양쪽을 잡는다.
_PLACEHOLDER_RE = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_.]*\}$")


def is_unset(value: str | None) -> bool:
    """이 값이 '설정되지 않음' 인가.

    `None`, 빈 문자열(공백만 있는 경우 포함), 확장되지 않은 `${...}` 자리표시자가 모두
    미설정이다. 자리표시자를 값으로 믿는 것이 이 모듈이 막으려는 결함이다.
    """
    if value is None:
        return True
    stripped = value.strip()
    if not stripped:
        return True
    return bool(_PLACEHOLDER_RE.match(stripped))


class CredentialStore:
    """서비스 하나의 자격증명을 여러 출처에서 해석한다.

    Args:
        service: 서비스 슬러그. 파일명이 된다 (`smartstore` → `smartstore.json`).
        path: 자격증명 파일 경로를 직접 지정할 때.
        env_var: 경로를 덮어쓸 환경변수 이름 (예: `SMARTSTORE_CREDENTIALS_FILE`).

    파일을 읽지 못해도 예외를 던지지 않는다. 자격증명이 환경변수로만 들어오는 배치도
    정상 사용이며, 그때 파일은 그냥 없다.
    """

    def __init__(
        self,
        service: str,
        *,
        path: Path | None = None,
        env_var: str | None = None,
    ) -> None:
        self.service = service
        self.path = self._resolve_path(service, path, env_var)
        self._file: dict[str, str] = self._read_file()

    @staticmethod
    def _resolve_path(
        service: str,
        path: Path | None,
        env_var: str | None,
    ) -> Path:
        if path is not None:
            return Path(path).expanduser()
        if env_var:
            override = os.environ.get(env_var)
            if not is_unset(override):
                return Path(override).expanduser()  # type: ignore[arg-type]
        return DEFAULT_DIR / f"{service}.json"

    def _read_file(self) -> dict[str, str]:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            return {}
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            # 손상된 파일 때문에 서버가 못 뜨는 편보다, 없는 셈 치고 환경변수로
            # 넘어가는 편이 낫다. 어느 쪽이든 아래 missing() 이 사실을 보고한다.
            return {}
        if not isinstance(payload, dict):
            return {}
        return {str(k): str(v) for k, v in payload.items() if v is not None}

    def get(self, key: str, default: str = "") -> str:
        """`key` 를 환경변수 → 파일 → 기본값 순으로 해석한다."""
        env_value = os.environ.get(key)
        if not is_unset(env_value):
            return env_value.strip()  # type: ignore[union-attr]

        file_value = self._file.get(key)
        if not is_unset(file_value):
            return file_value.strip()  # type: ignore[union-attr]

        return default

    def missing(self, keys: list[str]) -> list[str]:
        """`keys` 중 어느 출처에서도 값을 얻지 못한 항목."""
        return [key for key in keys if not self.get(key)]

    def setup_hint(self, keys: list[str]) -> str:
        """미설정 키를 사람이 읽을 안내문으로. 값이 다 있으면 빈 문자열."""
        absent = self.missing(keys)
        if not absent:
            return ""
        return (
            f"{self.service} 자격증명이 설정되지 않았습니다: {', '.join(absent)}. "
            f"파일 {self.path} 에 적거나, Claude 에서는 플러그인 설정 화면에서 입력하세요."
        )


def load(
    service: str,
    keys: list[str],
    *,
    path: Path | None = None,
    env_var: str | None = None,
) -> dict[str, str]:
    """`service` 의 `keys` 를 한 번에 해석한다. 미설정 키는 빈 문자열이 된다."""
    store = CredentialStore(service, path=path, env_var=env_var)
    return {key: store.get(key) for key in keys}
