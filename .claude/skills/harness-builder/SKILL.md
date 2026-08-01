---
name: harness-builder
description: Companion skill for /harness:builder — generates marketplace plugin (moai-coworker/moai/moai-designer/moai-pm/moai-seller + future expert plugins) core skills from a 3-Layer research pipeline (qmd vault → Claude official docs → web search) with category constraints.
metadata:
  version: "0.2.0"
  category: harness
  status: active
  updated: 2026-07-10
  tags: "harness, plugin, skill-generation, qmd, claude-docs"
---

# harness-builder — Marketplace Plugin Skill Generator

Companion skill for the `/harness:builder` harness. Turns a natural-language directive into a plugin-scoped core skill via a 7-Phase pipeline with 3-Layer research + audit.

## Target Plugin Resolution (marketplace-driven, NOT a fixed enum)

The target plugin is resolved from natural language against the **plugins list in `.claude-plugin/marketplace.json`** (SSOT). Current family: `moai-coworker` (실무 올인원), `moai` (code/개발), `moai-designer` (디자인), `moai-pm` (프로젝트 허브), `moai-seller` (이커머스), plus future expert plugins (`moai-writer` / `moai-marketer` / `moai-officer` / `moai-lawyer` / `moai-accountant` / `moai-recruiter` / `moai-tutor`) as they register in the marketplace. Do NOT hardcode a 2-value cowork/code enum — the intent-parser reads the marketplace manifest at runtime.

## 7-Phase Pipeline (Pipeline + Producer-Reviewer)

1. **Discovery** (`intent-parser`) — parse natural-language `$ARGUMENTS` → target plugin (resolved against `.claude-plugin/marketplace.json` plugins list) + skill topic + intent. Returns structured block (NOT free-form). The orchestrator surfaces ambiguities via AskUserQuestion.
2. **3-Layer Research** (`research-collector`, dynamic-workflow fan-out):
   - Layer 1 qmd vault — `scripts/qmd-search.sh "<keyword>" [TOP_N]`
   - Layer 2 Claude official docs — `code.claude.com/docs`, `docs.claude.com`
   - Layer 3 web search — supplementary
3. **Curation** (`plugin-curator`) — 4-dimension rubric (Relevance / Specificity / Practicality / Reusability, 0–5 each), top-5 selection. Producer-Reviewer pattern: curator is the evaluator.
4. **User Report & Selection** — orchestrator surfaces top-5 via AskUserQuestion.
5. **Build** (`skill-builder`, opus/high) — generate the plugin-scoped skill under the category constraints.
6. **Audit** (`auditor`) — Claude 공식 문서 기준 감사 (skill-authoring 스키마: name kebab ≤64, description ≤1536 folded scalar, metadata; 카테고리 제약; 공식 문서 정합성; 중복 회피). PASS or violations → orchestrator가 skill-builder에 재위임.
7. **Final Report** — audit verdict (pass/violations) 포함.

## Category Constraints (HARD — skill-builder enforces)

Aligned with the official Claude Code plugin component model (skills, agents, hooks, MCP servers, LSP servers, commands [legacy], output-styles) + the v6 expert-plugin design:

| Target plugin | Allowed components | Forbidden components |
|---------------|-------------------|---------------------|
| Expert plugins — all non-code (moai-coworker / moai-designer / moai-pm / moai-seller / future moai-writer·marketer·officer·lawyer·accountant·recruiter·tutor) | `skills/`, `agents/`, MCP declarations (plugin-root `.mcp.json` or `mcpServers` in plugin.json; vendored `mcp-servers/`) | `commands/`, `hooks/`, `output-styles/`, LSP (`.lsp.json`), `rules/` |
| Code plugin (`moai`) | Full surface: `commands/`, `skills/`, `agents/`, `hooks/`, `output-styles/`, MCP (`.mcp.json`/`mcp-servers/`), LSP (`.lsp.json`) | `rules/` (not an official plugin component) |

## Official Schema Notes (code.claude.com/docs plugins / plugins-reference)

- `.claude-plugin/plugin.json` requires ONLY `name` (kebab-case). Optional: `displayName`, `version` (semver; omitted → git SHA), `description`, `author`, `defaultEnabled`.
- Plugin skills invoke as `/plugin-name:skill`. Skill frontmatter `name` is kebab-case ≤64 chars (optional, defaults to directory name); `description` is a YAML folded scalar; combined `description` + `when_to_use` listing cap is **1,536 chars**.
- MCP servers: declare in plugin-root `.mcp.json` (or `mcpServers` in plugin.json); use `${CLAUDE_PLUGIN_ROOT}` for plugin-internal paths (marketplace plugins are cache-copied — external absolute paths break).

## qmd Layer (Layer 1)

- Wrapper: `scripts/qmd-search.sh "<query>" [TOP_N]` — qmd hybrid (BM25 + semantic + LLM rerank), automatic ripgrep fallback when qmd unavailable or vectors < `VAULT_QMD_MIN_VECTORS` (default 1000).
- Env vars: `VAULT_QMD_COLLECTION` (default `moai-vault`), `VAULT_SEARCH_TOP` (default 10), `MOAI_OBSIDIAN_VAULT`.
- Auto-sync: `scripts/sync.sh --quiet` runs before search (incremental qmd update + embed).

## References

- Manifest: `.claude/commands/harness/builder/manifest.json`
- Runner: `.claude/workflows/harness-builder-run.js`
- Entry command: `.claude/commands/harness/builder.md`
