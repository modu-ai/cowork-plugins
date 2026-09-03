#!/usr/bin/env python3
"""플러그인이 네 실행 환경 모두에서 동작하는지 기계적으로 검사한다.

    Claude 데스크톱 · Claude Code CLI · Codex 데스크톱 · Codex CLI
    (그리고 그 각각이 macOS 와 Windows)

    python3 scripts/check-plugin-runtimes.py            # 전체
    python3 scripts/check-plugin-runtimes.py moai-seller

## 왜 눈으로는 못 잡는가

여기서 걸러내는 결함은 **아무 신호도 내지 않는다**. 서버는 정상 기동하고 도구 목록도
정상으로 뜨는데 호출만 실패하거나, 한 런타임에서만 조용히 빠진다. 2026-09-03 실측으로
확인한 갈라짐이 근거다:

| | Claude | Codex |
|---|---|---|
| args·env 의 `${CLAUDE_PLUGIN_ROOT}` | 확장 | **리터럴 통과** |
| env 의 `${KEY}` / `${user_config.KEY}` | 확장 | **리터럴 통과** |
| `cwd` | 스키마에 없어 버려짐 | **플러그인 루트로 해석** |
| 서버 env 의 `CLAUDE_PLUGIN_ROOT` | 자동 주입 | 없음 |

그래서 경로에 의존하는 서버는 `.mcp.json`(Claude 용)과 `.codex-plugin/plugin.json` 의
인라인 `mcpServers`(Codex 용)로 나뉜다. 이 검사기는 그 두 벌이 서로 어긋나지 않는지,
그리고 각자가 자기 런타임의 규칙을 지키는지 본다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
CANONICAL_LAUNCHER = REPO_ROOT / "plugins" / "_shared" / "mcp-launch" / "mcp_launch.py"

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)*$")
PLACEHOLDER_RE = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_.]*\}")

#: codex 플러그인 매니페스트가 받아들이는 최상위 키 (codex 0.152 검증기 기준).
CODEX_MANIFEST_KEYS = {
    "id", "name", "version", "description", "skills", "apps",
    "mcpServers", "interface", "author", "homepage", "repository",
    "license", "keywords",
}

#: Windows 에 없거나 셸을 타는 런처. `command` 에 오면 안 된다.
WINDOWS_HOSTILE_COMMANDS = {"sh", "bash", "/bin/sh", "/bin/bash", "zsh", "python", "python3"}

#: 인자에 들어가면 셸을 전제하게 되는 연산자.
SHELL_OPERATORS = ("&&", "||", "|", ">", "<", "`", "~/")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, plugin: str, message: str) -> None:
        self.errors.append(f"{plugin}: {message}")

    def warn(self, plugin: str, message: str) -> None:
        self.warnings.append(f"{plugin}: {message}")


def normalize_contract_path(raw: str) -> str:
    """codex 검증기와 같은 방식으로 상대경로를 정규화한다 (`./skills/` → `skills`)."""
    return Path(str(raw)).as_posix().rstrip("/")


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path} 를 읽지 못했습니다: {error}") from error


def check_codex_manifest(name: str, plugin: Path, report: Report) -> dict | None:
    """codex 매니페스트가 codex 검증기를 통과할 모양인지."""
    path = plugin / ".codex-plugin" / "plugin.json"
    manifest = read_json(path)
    if manifest is None:
        report.error(name, ".codex-plugin/plugin.json 이 없습니다 (Codex 에서 설치되지 않습니다)")
        return None

    for key in sorted(set(manifest) - CODEX_MANIFEST_KEYS):
        report.error(name, f".codex-plugin: `{key}` 는 codex 검증기가 거부하는 키입니다")

    for required in ("name", "version", "description"):
        if not str(manifest.get(required, "")).strip():
            report.error(name, f".codex-plugin: `{required}` 가 비었습니다")

    version = str(manifest.get("version", ""))
    if version and not SEMVER_RE.match(version):
        report.error(name, f".codex-plugin: version `{version}` 이 semver 가 아닙니다")

    skills = manifest.get("skills")
    if skills is not None and normalize_contract_path(skills) != "skills":
        report.error(name, f".codex-plugin: skills 는 `./skills/` 여야 합니다 (현재 {skills})")

    servers = manifest.get("mcpServers")
    if isinstance(servers, str):
        if normalize_contract_path(servers) != ".mcp.json":
            report.error(name, f".codex-plugin: mcpServers 경로는 `./.mcp.json` 이어야 합니다 (현재 {servers})")
        elif not (plugin / ".mcp.json").is_file():
            report.error(name, ".codex-plugin: mcpServers 를 선언했는데 .mcp.json 이 없습니다")

    interface = manifest.get("interface")
    if isinstance(interface, dict):
        for required in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            if not str(interface.get(required, "")).strip():
                report.error(name, f".codex-plugin: interface.{required} 가 비었습니다")
        if "defaultPrompt" not in interface and "default_prompt" not in interface:
            report.error(name, ".codex-plugin: interface.defaultPrompt 가 없습니다")

    return manifest


def check_skill_frontmatter(name: str, plugin: Path, report: Report) -> None:
    """codex 는 스킬마다 SKILL.md 와 name/description 프런트매터를 요구한다."""
    skills_dir = plugin / "skills"
    if not skills_dir.is_dir():
        return
    for skill in sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        md = skill / "SKILL.md"
        if not md.is_file():
            report.error(name, f"스킬 `{skill.name}` 에 SKILL.md 가 없습니다")
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            report.error(name, f"스킬 `{skill.name}` 이 YAML 프런트매터로 시작하지 않습니다")
            continue
        end = text.find("\n---", 4)
        if end == -1:
            report.error(name, f"스킬 `{skill.name}` 의 프런트매터가 닫히지 않았습니다")
            continue
        block = text[4:end]
        for field in ("name", "description"):
            if not re.search(rf"^{field}\s*:\s*\S", block, re.MULTILINE):
                report.error(name, f"스킬 `{skill.name}` 프런트매터에 `{field}` 가 없습니다")


def check_command_portability(name: str, where: str, server: str, cfg: dict, report: Report) -> None:
    """Windows 에서 깨지는 실행 형태를 잡는다."""
    command = cfg.get("command")
    if command and Path(str(command)).name in WINDOWS_HOSTILE_COMMANDS:
        report.error(
            name,
            f"{where}/{server}: `{command}` 는 Windows 에 없거나 셸을 탑니다 — uv·uvx·npx 를 쓰세요",
        )
    for arg in cfg.get("args", []) or []:
        if any(op in str(arg) for op in SHELL_OPERATORS):
            report.error(name, f"{where}/{server}: 인자에 셸 연산자가 있습니다 — {arg!r}")
        if str(arg).startswith("/") and "mcp-servers" in str(arg):
            report.error(name, f"{where}/{server}: 절대경로 인자 — {arg!r}")


def check_claude_wiring(name: str, plugin: Path, report: Report) -> dict:
    """`.mcp.json` 은 Claude 용. 경로는 ${CLAUDE_PLUGIN_ROOT} 로만 잡는다."""
    doc = read_json(plugin / ".mcp.json")
    if doc is None:
        return {}
    servers = doc.get("mcpServers") or {}
    if not isinstance(servers, dict):
        report.error(name, ".mcp.json: mcpServers 가 객체가 아닙니다")
        return {}

    for server, cfg in servers.items():
        if not isinstance(cfg, dict):
            report.error(name, f".mcp.json/{server}: 항목이 객체가 아닙니다")
            continue
        check_command_portability(name, ".mcp.json", server, cfg, report)

        joined = " ".join(str(a) for a in cfg.get("args", []) or [])
        if "mcp-servers/" in joined or "mcp-launch/" in joined:
            if "${CLAUDE_PLUGIN_ROOT}" not in joined:
                report.error(
                    name,
                    f".mcp.json/{server}: 플러그인 안의 경로를 참조하면서 "
                    "${CLAUDE_PLUGIN_ROOT} 를 쓰지 않았습니다 (Claude 는 cwd 를 무시합니다)",
                )
        if "cwd" in cfg:
            report.warn(name, f".mcp.json/{server}: cwd 는 Claude 스키마에 없어 무시됩니다")
    return servers


def check_codex_wiring(name: str, plugin: Path, manifest: dict, report: Report) -> dict:
    """codex 쪽 배선. 자리표시자가 남아 있으면 리터럴로 새어 나간다."""
    servers = manifest.get("mcpServers")
    if not isinstance(servers, dict):
        return {}

    for server, cfg in servers.items():
        if not isinstance(cfg, dict):
            report.error(name, f"codex/{server}: 항목이 객체가 아닙니다")
            continue
        check_command_portability(name, "codex", server, cfg, report)

        for arg in cfg.get("args", []) or []:
            if PLACEHOLDER_RE.search(str(arg)):
                report.error(
                    name,
                    f"codex/{server}: 인자에 자리표시자가 남았습니다 — {arg!r} "
                    "(codex 는 확장하지 않고 그대로 넘깁니다)",
                )
        if PLACEHOLDER_RE.search(str(cfg.get("url", ""))):
            report.error(name, f"codex/{server}: url 에 자리표시자가 남았습니다")
        if cfg.get("env"):
            report.error(
                name,
                f"codex/{server}: env 로 값을 넘기고 있습니다 — codex 는 ${{...}} 를 "
                "확장하지 않으므로 자격증명은 파일이나 env_vars 로 받아야 합니다",
            )

        joined = " ".join(str(a) for a in cfg.get("args", []) or [])
        if ("mcp-servers/" in joined or "mcp-launch/" in joined) and cfg.get("cwd") != ".":
            report.error(
                name,
                f"codex/{server}: 플러그인 안의 경로를 참조하면서 `\"cwd\": \".\"` 가 없습니다 "
                "(codex 는 세션 디렉터리에서 실행합니다)",
            )
    return servers


def check_parity(name: str, claude: dict, codex: dict, manifest: dict, report: Report) -> None:
    """두 런타임이 같은 서버 집합을 보는지. 다르면 의도를 밝혀야 한다."""
    declared = manifest.get("mcpServers")
    if declared is None:
        # codex 매니페스트가 MCP 를 아예 싣지 않는다. `.mcp.json` 에 서버가 있다면
        # 그것은 Claude 전용이라는 뜻이고, 조용히 빠지는 쪽이 가장 눈에 안 띈다.
        for server in sorted(claude):
            report.warn(name, f"`{server}` 는 Claude 에만 실립니다 — codex 매니페스트에 mcpServers 가 없습니다")
        return
    if not isinstance(declared, dict):
        return  # 문자열 경로 = 분기 없음 = 정의상 동일
    only_claude = sorted(set(claude) - set(codex))
    only_codex = sorted(set(codex) - set(claude))
    for server in only_claude:
        report.warn(name, f"`{server}` 는 Claude 에만 있습니다 — 의도한 제외인지 확인하세요")
    for server in only_codex:
        report.error(name, f"`{server}` 가 Codex 에만 있습니다 — Claude 쪽 배선이 빠졌습니다")


def check_user_config(name: str, plugin: Path, claude: dict, report: Report) -> None:
    """`${user_config.KEY}` 로 참조한 키가 실제로 선언돼 있는지."""
    manifest = read_json(plugin / ".claude-plugin" / "plugin.json") or {}
    declared = set(manifest.get("userConfig") or {})

    referenced: set[str] = set()
    for cfg in claude.values():
        if not isinstance(cfg, dict):
            continue
        blob = json.dumps(cfg, ensure_ascii=False)
        referenced |= set(re.findall(r"\$\{user_config\.([A-Za-z_]\w*)\}", blob))

    for key in sorted(referenced - declared):
        report.error(
            name,
            f".claude-plugin: `${{user_config.{key}}}` 를 참조하는데 userConfig 에 선언이 없습니다",
        )
    for key in sorted(declared - referenced):
        report.warn(name, f".claude-plugin: userConfig `{key}` 가 어디에서도 쓰이지 않습니다")


def launcher_keys(servers: dict) -> dict[str, list[str]]:
    """런처를 거치는 서버별 `--keys` 값. 런처를 안 쓰는 서버는 빠진다."""
    found: dict[str, list[str]] = {}
    for server, cfg in servers.items():
        if not isinstance(cfg, dict):
            continue
        args = [str(a) for a in cfg.get("args", []) or []]
        if not any("mcp-launch/" in a for a in args):
            continue
        if "--keys" in args:
            i = args.index("--keys")
            if i + 1 < len(args):
                found[server] = [k.strip() for k in args[i + 1].split(",") if k.strip()]
    return found


def check_launcher_keys(name: str, plugin: Path, claude: dict, codex: dict, report: Report) -> None:
    """런처의 `--keys` 이름이 실제로 존재하는 키를 가리키는지.

    오타 하나가 조용히 통과하면 런처가 엉뚱한 이름을 채우고, 제3자 서버는 키를 못 받은 채
    뜬다 — 이 저장소가 없애려던 바로 그 실패 형태다. `--keys` 는 다른 어떤 검사도 보지
    않으므로, 여기서 두 방향을 대조한다.
    """
    manifest = read_json(plugin / ".claude-plugin" / "plugin.json") or {}
    declared = set(manifest.get("userConfig") or {})

    claude_keys = launcher_keys(claude)
    codex_keys = launcher_keys(codex)

    # (1) Claude 쪽 --keys 는 userConfig 에 선언돼 있어야 한다.
    for server, keys in claude_keys.items():
        for key in keys:
            if key not in declared:
                report.error(
                    name,
                    f".mcp.json/{server}: 런처 `--keys` 의 `{key}` 가 userConfig 에 없습니다 "
                    "(오타면 런처가 빈 값을 채우고 서버는 조용히 인증에 실패합니다)",
                )

    # (2) 두 런타임의 --keys 가 어긋나면 한쪽만 자격증명을 받는다.
    for server in sorted(set(claude_keys) & set(codex_keys)):
        if claude_keys[server] != codex_keys[server]:
            report.error(
                name,
                f"{server}: 런처 `--keys` 가 두 런타임에서 다릅니다 — "
                f"claude={claude_keys[server]} codex={codex_keys[server]}",
            )


def check_launcher_copy(name: str, plugin: Path, report: Report) -> None:
    """벤더된 런처 사본이 정본과 같은지 (드리프트 방지)."""
    copy = plugin / "mcp-launch" / "mcp_launch.py"
    if not copy.is_file():
        return
    if not CANONICAL_LAUNCHER.is_file():
        report.error(name, f"런처 정본을 찾을 수 없습니다: {CANONICAL_LAUNCHER}")
        return
    if copy.read_bytes() != CANONICAL_LAUNCHER.read_bytes():
        report.error(
            name,
            "mcp-launch/mcp_launch.py 가 정본과 다릅니다 — "
            "plugins/_shared/mcp-launch/mcp_launch.py 에서 다시 복사하세요",
        )


def check_launcher_referenced(name: str, claude: dict, codex: dict, plugin: Path, report: Report) -> None:
    """런처를 참조하는데 사본이 없으면 그 서버는 뜨지 않는다."""
    needs = any(
        "mcp-launch/" in " ".join(str(a) for a in (cfg or {}).get("args", []) or [])
        for group in (claude, codex)
        for cfg in group.values()
        if isinstance(cfg, dict)
    )
    if needs and not (plugin / "mcp-launch" / "mcp_launch.py").is_file():
        report.error(name, "런처를 참조하는데 mcp-launch/mcp_launch.py 가 없습니다")


def check_plugin(plugin: Path, report: Report) -> None:
    name = plugin.name
    manifest = check_codex_manifest(name, plugin, report)
    if manifest is None:
        return
    check_skill_frontmatter(name, plugin, report)
    claude = check_claude_wiring(name, plugin, report)
    codex = check_codex_wiring(name, plugin, manifest, report)
    check_parity(name, claude, codex, manifest, report)
    check_user_config(name, plugin, claude, report)
    check_launcher_keys(name, plugin, claude, codex, report)
    check_launcher_copy(name, plugin, report)
    check_launcher_referenced(name, claude, codex, plugin, report)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugins", nargs="*", help="검사할 플러그인 이름 (기본: 전체)")
    args = parser.parse_args()

    targets = (
        [PLUGINS_DIR / n for n in args.plugins]
        if args.plugins
        else sorted(p for p in PLUGINS_DIR.glob("moai-*") if p.is_dir())
    )

    report = Report()
    for plugin in targets:
        if not plugin.is_dir():
            report.errors.append(f"{plugin.name}: 디렉터리가 없습니다")
            continue
        check_plugin(plugin, report)

    for warning in report.warnings:
        print(f"참고  {warning}")
    for error in report.errors:
        print(f"오류  {error}", file=sys.stderr)

    print(
        f"\n검사한 플러그인 {len(targets)}개 — 오류 {len(report.errors)}건, 참고 {len(report.warnings)}건"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
