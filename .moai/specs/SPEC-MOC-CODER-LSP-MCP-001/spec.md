---
id: SPEC-MOC-CODER-LSP-MCP-001
title: "moai coder plugin expansion — LSP 12-language coverage + survey-driven dev MCP catalog"
version: "0.2.1"
status: completed
created: 2026-07-10
updated: 2026-07-11
author: manager-spec
priority: P1
phase: "marketplace v6.2.0 target"
module: "plugins/moai"
lifecycle: spec-anchored
tags: "plugin, moai, lsp, mcp, hooks, meta-harness, settings"
related_specs: [SPEC-MOC-PM-ADVISORS-001]
tier: M
---

# SPEC-MOC-CODER-LSP-MCP-001 — moai coder plugin expansion: LSP full coverage + survey-driven dev MCP

## HISTORY

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-07-10 | 0.1.0 | Initial plan-phase authoring (Tier M: spec + plan + acceptance + progress). Design decisions FINAL per 2-round Socratic interview. | manager-spec |
| 2026-07-11 | 0.2.0 | plan-auditor iter-2 (PASS-WITH-DEBT 0.81 → hardening). F8 REQ-L-004 reworded as GEARS (enumeration → plan.md §I candidate table). F9 REQ-C-002 ownership reworded to template+catalog deliverable + AC-CLM-013. F10 AC-CLM-006 mechanized (synthetic SessionStart stdin, `"decision"`/`"block"` count == 0); AC-CLM-009/010/012 tightened. F11 M4 generation-template path pinned to `plugins/moai/references/` (disjoint from M5 `templates/`). F12 marketplace.json single cross-SPEC owner = SPEC-1 M5 (baseline v6.2.0 / moai 1.0.0). F13 Out-of-Scope languages heading (elixir/scala/r/flutter). | manager-spec |
| 2026-07-11 | 0.2.1 | plan-auditor iter-2 polish (non-blocking; PASS 0.88). P4: JavaScript coverage reconciliation note added to §C.1 — JavaScript is served by the existing `typescript` entry via its `extensionToLanguage` map (`.js`/`.jsx`/`.mjs`/`.cjs`, verified in live `plugins/moai/.lsp.json`), so it is deliberately absent from both the in-scope 12 and the Out-of-Scope 4. AC-CLM-013 instantiation-harness reproducibility note added to `acceptance.md`. No REQ/AC renumbering; no design decisions re-opened. | manager-spec |

## §A Context & Problem

### A.1 Current state (measured 2026-07-10, verified this session)

- `plugins/moai/.lsp.json` declares exactly 5 languages: `go` (gopls), `python` (pyright-langserver), `rust` (rust-analyzer), `swift` (sourcekit-lsp), `typescript` (typescript-language-server). Schema per entry: `command`, `args`, `extensionToLanguage`, `restartOnCrash`, `maxRestarts`. No install-missing guidance exists anywhere in the plugin.
- `plugins/moai/.mcp.json` declares `context7` only (`alwaysLoad: true`), plus `staggeredStartup` config.
- `plugins/moai/hooks/`: `dispatch.sh` + `gates/` (5 gate scripts) + `hooks.json`, covering SessionStart / PreCompact / SessionEnd / PreToolUse / PostToolUse.

### A.2 Problem

The coder plugin's LSP coverage (5 languages) trails the official Claude Code marketplace language set (11), server binaries are NOT bundled by Claude Code (official docs) so missing-binary situations degrade silently, and there is no vetted path for wiring common dev-service MCP servers into a user's project without hand-authoring `.mcp.json` (credential-safety risk).

## §B Goals

1. `.lsp.json`: 5 → 12 language coverage (official marketplace 11 + keep Swift).
2. Install guidance: per-language install commands at `/moai --project` init + a non-blocking SessionStart advisory when a declared server is missing.
3. MCP: plugin `.mcp.json` stays context7-only; a verified, extensible dev-MCP catalog drives survey-based generation of the TARGET project's `.mcp.json` (credentials never bundled).
4. Meta-harness: `/moai --project` generates project-level `.claude/settings.json` + hooks from survey-parameterized templates; plugin-level hooks stay as-is.

## §C Requirements (GEARS)

### C.1 LSP coverage

- **REQ-L-001** (Ubiquitous): `plugins/moai/.lsp.json` shall cover 12 languages: Python, TypeScript, Go, Rust, Java, C/C++, C#, PHP, Kotlin, Ruby, HTML/CSS (official Claude Code marketplace 11) + Swift (retained). The 5 existing entries shall be preserved unchanged unless verification (REQ-L-003) finds a defect.
  - **Note — JavaScript coverage (language-partition reconciliation)**: JavaScript is intentionally NOT a standalone `.lsp.json` entry and therefore appears in NEITHER the in-scope 12 (official 11 + Swift) NOR the Out-of-Scope 4 (`elixir`/`scala`/`r`/`flutter`, §E). It is already served by the existing `typescript` entry through its `extensionToLanguage` map, which maps `.js` → `javascript`, `.jsx` → `javascriptreact`, `.mjs` → `javascript`, `.cjs` → `javascript` (verified in the live `plugins/moai/.lsp.json`). JavaScript files are handled by `typescript-language-server` and need no separate slot — this reconciles the 16-language set MoAI supports elsewhere with the 12-in / 4-out partition (JavaScript folded into `typescript`). REQ-L-001's "5 existing entries preserved unchanged" already protects these JS extension mappings.
- **REQ-L-002** (Ubiquitous): Every `.lsp.json` entry shall conform to the existing schema: `command`, `args`, `extensionToLanguage`, `restartOnCrash: true`, `maxRestarts: 3`.
- **REQ-L-003** (Event): **When** run-phase authors a new entry, the implementer shall verify the exact server binary name and launch args against the server's official documentation (Context7 / WebFetch) BEFORE writing it — a mandated verification step; official docs confirm binaries are NOT bundled with Claude Code.
- **REQ-L-004** (Ubiquitous): The implementer shall select each new language server from the verified candidate table in `plan.md §I` (Candidate Server Table), and shall not write any `.lsp.json` entry whose exact binary name and launch args were not confirmed by the REQ-L-003 verification step. The candidate table is advisory input (candidates, not final); REQ-L-003 verification is the authority for the written entry.

### C.2 LSP install guidance

- **REQ-L-005** (Compound): **Where** the coder plugin is installed **When** `/moai --project` init detects a project language whose declared server binary is absent from `PATH`, the guidance content shall supply per-language install commands (brew / npm / pip / gem / etc.), macOS-first with cross-platform notes. (Flow ownership: the `/moai --project` flow itself belongs to SPEC-MOC-PM-ADVISORS-001; THIS SPEC owns the guidance content it consumes.)
- **REQ-L-006** (Event): **When** a session starts and a language declared in `.lsp.json` matches project files but its server binary is missing from `PATH`, the SessionStart advisory hook shall emit an advisory message naming the language, the binary, and the install-guidance pointer.
- **REQ-L-007** (Unwanted): The SessionStart advisory shall not block: the hook shall always exit 0 and shall never emit blocking decision JSON.
- **REQ-L-008** (Ubiquitous): The existing 5 gate scripts shall remain byte-unchanged; the advisory is ADDITIVE (a new gate script + its `hooks.json` registration only).

### C.3 MCP catalog & generation

- **REQ-C-001** (Ubiquitous): The plugin's own `.mcp.json` shall keep ONLY `context7` (no new always-loaded servers).
- **REQ-C-002** (Ubiquitous): This SPEC shall deliver the `.mcp.json` generation TEMPLATE plus the catalog it draws from (NOT the act of writing a target project's `.mcp.json` — that write is performed by the `/moai --project` flow owned by SPEC-MOC-PM-ADVISORS-001; see §E). Instantiating the delivered template with a fixed server selection shall yield valid JSON containing exactly the selected servers under `mcpServers` and zero credential literals (only `.env` placeholder references). The template + catalog are the deliverable; the flow that consumes them is the sibling SPEC's.
- **REQ-C-003** (Ubiquitous): The catalog shall contain exactly these 6 verified entries with these transports:
  - `playwright` — local stdio, `npx @playwright/mcp@latest`
  - `supabase` — remote `https://mcp.supabase.com/mcp` (OAuth); entry MUST carry the official warning verbatim in intent: dev/test only, never production data
  - `vercel` — remote `https://mcp.vercel.com` (OAuth, HTTP transport)
  - `neon` — remote `https://mcp.neon.tech/mcp` (OAuth) OR local `npx -y @neondatabase/mcp-server-neon start <KEY>`
  - `railway` — remote `https://mcp.railway.com` (OAuth); note: the npm package is now a Railway-CLI shim — prefer remote or railway CLI
  - `claude-in-chrome` — built into Claude Code, NO server entry generated; activation guidance only
- **REQ-C-004** (Ubiquitous): The catalog shall be a declarative, extensible structure: adding a future dev-service MCP shall be a data-only change (no generator-logic change).
- **REQ-C-005** (Unwanted): Credentials shall never be bundled — not in the catalog, not in generated `.mcp.json`, not in templates. Credential handling is `.env` guidance only (placeholders + instructions).

### C.4 Hooks / settings meta-harness

- **REQ-H-001** (Event): **When** `/moai --project` generation runs, it shall produce project-level `.claude/settings.json` (permissions allowlist, hooks registration) and project hooks scripts from templates parameterized by the survey (e.g., a quality gate wired to the detected toolchain).
- **REQ-H-002** (Ubiquitous): Meta-harness generation shall target the USER'S project folder exclusively; plugin-level hooks remain as-is (sole exception: the additive REQ-L-008 advisory gate).

### C.5 Cross-cutting

- **REQ-X-001** (Ubiquitous): All user-facing guidance text in conversation_language; identifiers, JSON keys, binary names in English.
- **REQ-X-002** (Ubiquitous): Acceptance criteria shall be machine-verifiable where possible (file existence, grep assertions, `jq` JSON validation of `.lsp.json` / catalog / generated-template outputs).

## §D Acceptance Criteria

Canonical AC enumeration with per-AC verification commands lives in `acceptance.md` (AC-CLM-001 … AC-CLM-013). Every AC is decided by a single command's exit status or numeric/`true`/`PASS` output.

## §E Exclusions

The following are explicitly out of scope for this SPEC.

### Out of Scope — moai-pm skill flow authoring

- The `/moai --project` interview/survey/generation FLOW is owned by SPEC-MOC-PM-ADVISORS-001. This SPEC owns the data and templates that flow consumes (catalog, guidance content, meta-harness templates) plus the plugin-side LSP/hook changes.

### Out of Scope — languages beyond the official Claude Code marketplace set (elixir, scala, r, flutter)

- REQ-L-001 fixes the 12-language set to the official Claude Code marketplace 11 + Swift. Languages MoAI supports elsewhere but which are NOT in the official marketplace LSP set — `elixir`, `scala`, `r`, `flutter` — are explicitly out of scope for this `.lsp.json` expansion. Adding them is a future data-only change (a new `.lsp.json` entry + a candidate-table row), not part of this SPEC.

### Out of Scope — LSP server binary installation by the plugin

- The plugin never installs binaries; it detects absence and emits guidance. No auto-install, no package-manager invocation on the user's behalf.

### Out of Scope — MCP credential provisioning

- No OAuth flows, keys, or tokens are provisioned, stored, or templated with real values. `.env` guidance only (REQ-C-005).

### Out of Scope — Windows install automation

- Install guidance is macOS-first with cross-platform NOTES; Windows-specific automation (winget scripts, cmd wrappers) is not delivered.

### Out of Scope — Runtime E2E

- Live LSP server attach tests and live MCP OAuth round-trips are post-sync manual validation; run-phase acceptance is structural (JSON validity, schema conformance, hook exit-code behavior under simulated PATH).

### Out of Scope — Plugin-level hook behavior changes

- The 5 existing gate scripts and dispatch.sh semantics are untouched (REQ-L-008); any gate refactoring is a separate SPEC.

### Out of Scope — direct `.claude-plugin/marketplace.json` edit

- To eliminate a cross-SPEC write race on the shared `marketplace.json` (both SPECs bump a plugin entry), this SPEC does NOT write `marketplace.json` directly. Its `moai` plugin-entry version-bump delta is HANDED to SPEC-MOC-PM-ADVISORS-001, whose final milestone (M5) is the SINGLE owner of the `marketplace.json` edit for BOTH the `moai-pm` and `moai` entries (interface contract: SPEC-1 `design.md §H`). Baseline observed 2026-07-11: `.metadata.version` = `6.2.0`, `moai` entry = `1.0.0`, `moai-pm` entry = `0.4.0`.

## §F Cross-References

- `plan.md` — milestones, verification-first approach, risks
- `acceptance.md` — AC matrix + verification commands
- SPEC-MOC-PM-ADVISORS-001 `design.md §H` — interface contract (catalog path, consumption, failure mode)
- Official Claude Code LSP marketplace language set (11 languages) — run-phase re-verifies against live docs per REQ-L-003
