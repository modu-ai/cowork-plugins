# 이 파일은 자동 생성된 복제본입니다 — 직접 수정하지 마세요.
# 정본: plugins/_shared/moai-mcp-core/tokenstore.py
# 동기화: python3 scripts/sync-mcp-core.py
"""갱신된 OAuth 토큰의 영속화.

리프레시 토큰은 수명이 길고(서비스에 따라 회전한다) 프로세스가 재시작돼도 살아 있어야
한다. 그래서 파일에 남긴다. 다만 **쓰지 못하는 환경에서도 서버는 계속 돌아가야 하므로**
실패하면 조용히 인메모리로 폴백한다.

경로는 macOS·Windows 양쪽에서 동일하게 동작하도록 pathlib으로만 조립한다.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from typing import Any

#: 모든 자체 제작 MCP 서버가 공유하는 토큰 저장 위치.
DEFAULT_DIR = Path.home() / ".moai" / "mcp"


class TokenStore:
    """서비스 하나의 토큰 묶음을 읽고 쓴다.

    Args:
        service: 서비스 슬러그. 파일명이 된다 (`youtube` → `youtube-tokens.json`).
        path: 저장 경로를 직접 지정할 때. 없으면 환경변수 → 기본 경로 순으로 정한다.
        env_var: 경로를 덮어쓸 환경변수 이름 (예: `YOUTUBE_TOKEN_FILE`).
    """

    def __init__(
        self,
        service: str,
        *,
        path: Path | None = None,
        env_var: str | None = None,
    ) -> None:
        self.service = service
        self._memory: dict[str, Any] = {}
        self._persistent = True

        if path is not None:
            self.path = Path(path)
        else:
            from_env = os.environ.get(env_var) if env_var else None
            self.path = Path(from_env) if from_env else DEFAULT_DIR / f"{service}-tokens.json"

    @property
    def persistent(self) -> bool:
        """마지막 저장이 파일에 기록됐는지. False면 인메모리로만 유지 중이다."""
        return self._persistent

    def load(self) -> dict[str, Any]:
        """저장된 토큰을 읽는다. 없거나 깨졌으면 빈 딕셔너리."""
        if not self._persistent:
            return dict(self._memory)
        try:
            raw = self.path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            return dict(self._memory)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # 손상된 파일은 없는 것으로 취급한다. 다음 저장에서 덮어써진다.
            return dict(self._memory)
        if not isinstance(data, dict):
            return dict(self._memory)
        self._memory = data
        return dict(data)

    def save(self, tokens: dict[str, Any]) -> bool:
        """토큰을 저장한다.

        Returns:
            파일에 기록했으면 True, 인메모리 폴백이면 False.
        """
        self._memory = dict(tokens)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # 같은 디렉터리에 임시 파일로 쓴 뒤 바꿔치기한다.
            # 저장 도중 프로세스가 죽어도 기존 파일이 반쯤 망가지지 않는다.
            tmp = self.path.with_name(self.path.name + ".tmp")
            tmp.write_text(
                json.dumps(tokens, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            os.replace(tmp, self.path)
            self._restrict_permissions()
        except OSError:
            self._persistent = False
            return False
        self._persistent = True
        return True

    def clear(self) -> None:
        """저장된 토큰을 지운다. 파일이 없어도 오류가 아니다."""
        self._memory = {}
        try:
            self.path.unlink(missing_ok=True)
        except OSError:
            pass

    def _restrict_permissions(self) -> None:
        """소유자만 읽도록 제한한다.

        Windows에서는 이 호출이 의미 없거나 실패할 수 있으므로 최선 노력으로만 수행한다.
        """
        try:
            self.path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass
