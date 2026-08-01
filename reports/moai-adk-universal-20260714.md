# moai-adk Universal Strategy — Claude Code 전용 → 멀티 에이전트 CLI 툴킷

Date: 2026-07-14 · Basis: web research (verified URLs) + moai-adk-go codebase scan

## Diagnosis (moai-adk-go)

- ~55–65% harness-neutral core: `internal/spec`, quality/security gates (`internal/hook/quality|security`, `foundation/trust`), `internal/git`/`worktree`, `internal/lsp`/`astgrep`/`mx`, `ciwatch`, `update`/`migration`.
- ~35–45% Claude Code adapter: hook JSON dispatcher (`internal/cli/hook.go` + `internal/hook`), `.claude/settings.json` engine (`internal/settings`), statusline, launchers (`cc/cg/glm/launcher.go`), `.claude/*` templates.
- GLM backend (`moai glm`/`moai cg`) = model-provider switching **inside** the Claude Code harness (Anthropic-compatible endpoint). No harness adapter interface exists yet; `unifiedLaunchDefault(mode)` is the extension seam.

## Ecosystem standards (the three portability layers)

1. **AGENTS.md** (instructions): Linux Foundation / Agentic AI Foundation stewardship, 60k+ repos, 20+ tools native. Codex reads it hierarchically, 32KiB `project_doc_max_bytes` truncation. Canonical pattern: AGENTS.md as SSOT + one-line `CLAUDE.md` = `@AGENTS.md` import (repo-portable; the reverse `project_doc_fallback_filenames` is user-level only).
2. **Agent Skills** (SKILL.md): opened by Anthropic 2025-12-18 (agentskills.io, Apache 2.0/CC-BY-4.0); adopted by 30+ tools incl. Codex, Gemini CLI, Copilot, Cursor, Goose, Junie, Kiro. Universal dir: `.agents/skills/`. Codex scan order: `./.agents/skills` → repo root → `~/.agents/skills` → `/etc/codex/skills`; skill list budget 2% of context / 8,000 chars. Vendor extension `agents/openai.yaml` ignored by other agents. Claude-only features (context fork/subagents) do not port.
3. **MCP** (tools): one server consumable by Claude Code (`.mcp.json`), Codex (`config.toml`, `codex mcp` subcommand), Gemini CLI (extension `mcpServers`). Best practices: narrow tools, least privilege, read-only defaults, project-scoped config committed to repo, on-demand tool loading (Anthropic code-execution pattern).

Gemini CLI additionally ships **extensions** (manifest `gemini-extension.json` + `GEMINI.md` + `commands/*.toml` + MCP servers) — near 1:1 with moai's plugin concept.

## Precedent: GitHub spec-kit

- Same category (SPEC-driven dev toolkit), supports 30+ agents from day one.
- Integration registry: per-agent self-contained subpackage; base classes `MarkdownIntegration` / `TomlIntegration` / `SkillsIntegration` / custom; registry = SSOT; new agent = config change, not code duplication.
- `specify init` adapts command files/context/dirs per agent; commands ship as slash commands or installable skills (`$speckit-<cmd>` in Codex).
- Multi-install safety (0.8.5+): isolated dirs + non-colliding context files + separate manifests.
- Agent key == executable name (detection via PATH lookup).

## Recommended architecture (4 layers)

- **L0 CLI-first core**: harness-agnostic commands (`moai gate`, `moai spec ...`, `moai mx ...`) with exit-code + JSON contract. Refactor: split Claude hook-event parsing from business logic in `internal/hook`.
- **L1 standard assets**: skills authored once under `.agents/skills/` (Agent Skills core only; vendor extras as overlays); generate AGENTS.md canonical + `CLAUDE.md` = `@AGENTS.md` (+ Claude-only layers); keep AGENTS.md < 32KiB.
- **L2 harness adapter registry**: `moai init --agent claude|codex|gemini` (multi-install-safe). Go interface: `Detect / Install / WireEvents / Launch`. First target Codex (mature skills + thin config.toml adapter), then Gemini CLI (extension packaging).
- **L3 `moai mcp serve`** (optional, later): narrow read-only-default tool set for shell-weak environments; skip where CLI suffices.

## Portability matrix

| Feature | Path | Verdict |
|---|---|---|
| SPEC workflow (plan/run/sync) | CLI + standard skills | portable |
| Quality gates (gate/fix/loop) | CLI (exit code + JSON) | portable |
| MX / codemaps / LSP | CLI, optional MCP | portable |
| Instructions (CLAUDE.md + rules) | AGENTS.md canonical + imports; path-scoped rules don't port → compress | partial |
| 28 skills | `.agents/skills/`; Claude-dependent skills need split | partial |
| Hooks (11+ events) | no equivalent in Codex/Gemini → explicit CLI calls in skill instructions; git hooks as floor | Claude-only |
| Subagents / output styles / AskUserQuestion / statusline | no counterpart → redesign per harness or keep Claude-only | Claude-only |

## Roadmap (order, no time estimates)

1. **M1** core/adapter boundary refactor (event abstraction in `internal/hook`; JSON output contracts). No behavior change.
2. **M2** dual-publish standard assets: AGENTS.md generator + `CLAUDE.md` import; skills canonical in `.agents/skills/` (link/copy to `.claude/skills/`). Cheapest win — Codex/Gemini users can already consume.
3. **M3** adapter registry + `moai init --agent` (Codex first, Gemini second; multi-install safety from the start).
4. **M4** `moai mcp serve` (demand-gated).
5. **M5** UX gap mitigation for hookless harnesses (`moai status --brief`, gate reminders in skills, git pre-commit/pre-push floor).

## Risks

- Avoid lowest-common-denominator regression: progressive enhancement (core everywhere, full orchestration on Claude Code).
- Test matrix growth → per-adapter smoke tests in CI, adapters isolated.
- Standard churn (Agent Skills <1yr old): keep canonical assets to spec core; vendor extensions as overlays.
- Instruction-layer compression loss (path-scoped `.claude/rules/` → single AGENTS.md, 32KiB cap): put contracts in AGENTS.md, details in skill references.
- Hook-backed safety degrades to instruction-following on other harnesses → double up with git hooks.

## Sources

- https://agentskills.io/home (verified)
- https://developers.openai.com/codex/skills (verified; redirects to learn.chatgpt.com/docs/build-skills)
- https://agents.md/ (verified)
- https://github.com/agentskills/agentskills
- https://developers.openai.com/codex/mcp · https://developers.openai.com/codex/concepts/customization
- https://github.com/github/spec-kit · https://github.github.io/spec-kit/reference/integrations.html
- https://google-gemini.github.io/gemini-cli/docs/extensions/
- https://www.anthropic.com/engineering/code-execution-with-mcp
- https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/docs/claude-code-with-codex.md
- https://agyn.io/blog/claude-md-agents-md-compatibility
- https://www.unite.ai/anthropic-opens-agent-skills-standard-continuing-its-pattern-of-building-industry-infrastructure/
- https://platform.uno/blog/mcp-configuration-across-ai-agents/
