---
id: SPEC-MOC-PM-ADVISORS-001
title: "moai-pm plugin redesign — Goose & MoAI super-advisor skills"
version: "0.2.1"
status: completed
created: 2026-07-10
updated: 2026-07-11
author: manager-spec
priority: P1
phase: "marketplace v6.2.0 target"
module: "plugins/moai-pm"
lifecycle: spec-anchored
tags: "plugin, moai-pm, skill, goose, advisor, desktop-parity, self-improvement"
related_specs: [SPEC-MOC-CODER-LSP-MCP-001, SPEC-MOC-PM-REDESIGN-001]
tier: L
---

# SPEC-MOC-PM-ADVISORS-001 — moai-pm plugin redesign: Goose & MoAI super-advisor skills

## HISTORY

| Date | Version | Change | Author |
|------|---------|--------|--------|
| 2026-07-10 | 0.1.0 | Initial plan-phase authoring (Tier L: spec + plan + acceptance + design + progress). Design decisions FINAL per 2-round Socratic interview. | manager-spec |
| 2026-07-10 | 0.2.0 | plan-auditor iter-2 (FAIL 0.74 → revision). Re-baselined §A against post-`e06086c` 18-plugin/v6.2.0 tree. F1 HARD-gate fixed to `^## .*\(HARD\)` baseline 8. F2 Korean-source/English-anchor reconciled (REQ-X-001 + design §A.1). F4 line-budget policy migrated to REQ-G-005b + design §D. F5 `/moai project` vs `--project` disambiguation + subcommand-surface migration (REQ-M-008/009). F6 traceability ACs. F7 `//project`→`/project`. Drift #4 marked RESOLVED (owner `moai-story`). | manager-spec |
| 2026-07-11 | 0.2.1 | plan-auditor iter-2 polish (non-blocking; PASS-WITH-DEBT 0.85). P1: Desktop-parity prohibition worded with class names (`hooks`/`LSP`/`output-styles`), never artifact-path tokens, in REQ-G-008 + design §A.1/§G (adds a §G authoring constraint) so a copied wording cannot false-fail AC-PMA-004b. P2: design §D HARD-block narrative arithmetic replaced with the verbatim 8-block enumeration. P3: drift #1 hardcoded hit count removed — deferred to M1 re-capture (AC-PMA-013 keys off M1 greps, never a literal). No REQ/AC renumbering; no design decisions re-opened. | manager-spec |

> Relationship to SPEC-MOC-PM-REDESIGN-001: that completed SPEC delivered the single `project` skill (v0.3.0). This SPEC **replaces the artifact** (the `project` skill is removed), not the historical record. Sync-phase SHOULD add `partially_superseded_by: [SPEC-MOC-PM-ADVISORS-001]` to the old SPEC's frontmatter (manager-docs task, not run-phase).

## §A Context & Problem

### A.1 Current state (re-measured 2026-07-10 against post-`e06086c` committed tree; working tree CLEAN)

- `plugins/moai-pm/` exposes exactly ONE skill: `skills/project/SKILL.md` + `references/core/` (13 canonical files: `router.md`, `cowork-setup.md`, `coder-setup.md`, `designer-setup.md`, `init-protocol.md`, `execution-protocol.md`, `context-collector.md`, `claudemd-generator.md`, `evolution-protocol.md`, `evaluation-protocol.md`, `diagnostic-protocol.md`, `quality-evaluator.md`, `INDEX.md`) + `references/templates/CLAUDE.md.tmpl`.
- Stray runtime artifacts exist INSIDE the skill directory (`skills/project/.claude/agent-memory/`, `skills/project/.moai/state/context-usage.json`) — junk from a prior agent run; must be removed with the skill.
- The plugin family on disk is **18 directories** (post-`e06086c` 18-plugin regrouping, marketplace v6.2.0; new plugins `moai-analyst`, `moai-media`, `moai-story`). The marketplace catalog (`.claude-plugin/marketplace.json`: `.metadata.version == "6.2.0"`, 18 plugin entries; the `moai-pm` entry version is `0.4.0`) is the authoritative family roster. Any hardcoded plugin count in migrated references is drift-by-construction — references cite marketplace.json as roster authority, never a literal count.

### A.2 Documented drift (re-measured 2026-07-10 against post-`e06086c` tree — 3 ACTIVE + 1 RESOLVED)

1. **Old 4-plugin / 27-plugin architecture remnants** (ACTIVE): remnants across 5 files under `plugins/moai-pm/skills/project/references/core/` — `designer-setup.md`, `cowork-setup.md`, `INDEX.md`, `coder-setup.md`, `init-protocol.md` (patterns `4-plugin` / `4-플러그인` / `27-플러그인`); `router.md` was already fixed by `e06086c` (0 hits). The exact hit count and per-file line anchors are NOT hardcoded here — they drift as commits land, so they are re-captured at M1 (`plan.md §C` step 1) and recorded to `progress.md §E.2`; AC-PMA-013 closes against those M1-recaptured drift greps, never a literal count. The migration rewrites each remnant against the live 18-plugin `.claude-plugin/marketplace.json` roster (never a literal count).
2. **Two conflicting self-evolution models** (ACTIVE): the simplified "recursive self-improvement" model in `SKILL.md:146` (`## 재귀적 자가 개선 (HARD)`; signal detection → diagnosis → minimal diff ≤3 files → 1-line log under CLAUDE.md `<!-- evolution-log -->`) is CURRENT; `evolution-protocol.md` carries the heavy 5-step Self-Refine model (7 hits at lines 5,9,76,99,102,272,286 for `Self-Refine` / `self-refine` / `metrics.csv`: `self-refine-log.md`, `metrics.csv`, forced 1-10 scoring) and is DEPRECATED. The migration REMOVES the heavy model entirely (not deprecated-in-place).
3. **Custom-agent generation phase absent from setup canon** (ACTIVE): `cowork-setup.md`'s 8-Phase summary is `1 인터뷰 → 2 인벤토리 → 3 체인 설계 → 4 Gap Detection → 5 확인 → 6 CLAUDE.md 생성 → 7 API 키 → 8 첫 실행 안내` — its Phase 7 is **API-key registration**, and the file contains **zero** `에이전트` (agent) mentions (`grep -c 에이전트 cowork-setup.md` → `0`) — while `SKILL.md:135` defines `## 커스텀 에이전트 생성 (--cowork Phase 7)`. The migration restores custom-agent generation as a first-class phase in the goose setup canon.
4. **Skill-prefix ownership** (RESOLVED by `e06086c` — no run-phase fix needed): `grep -rn "moai-coworker:(story-|book-)"` → **0** stale hits; `story-*` skills now live in `plugins/moai-story/` (16 skills, owner prefix `moai-story:`), and `cowork-setup.md:124` already cites `moai-story:story-project`. Retained here only as a re-verification gate (AC-PMA-003) that no stale prefix is re-introduced during migration. NOTE: the pre-`e06086c` SPEC draft incorrectly attributed `story-*` ownership to `moai-writer`; the correct owner is `moai-story`.

### A.3 Problem

One monolithic `project` skill conflates two distinct advisory jobs — (a) non-coding Cowork/Desktop project orchestration and (b) development-project initialization with moai-adk v3.0 philosophy — while carrying 4 documented drift defects. The redesign splits them into two purpose-built super-advisor skills and fixes all drift during the reference migration.

## §B Goals

1. Replace the `project` skill with two skills: `goose` (Desktop super-orchestrator/advisor) and `moai` (dev-project initialization advisor).
2. Migrate + fix: all 13 canonical references and the CLAUDE.md.tmpl are split/absorbed with the 4 drift items fixed during the move (never copied-then-fixed-later).
3. Align docs: README (2-skill entry), marketplace version bump, www guide update target list (sync-phase, list only).

## §C Requirements (GEARS)

### C.1 Goose skill (`/goose --project`)

- **REQ-G-001** (Ubiquitous): The moai-pm plugin shall expose a `goose` skill invoked as `/goose --project <natural-language instruction>`, acting as the super-orchestrator/advisor for ALL non-coding Claude Cowork (Desktop) work.
- **REQ-G-002** (Event): **When** `/goose --project` is invoked, the goose skill shall conduct a Socratic interview that assigns context grades A/B/C and shall not re-ask questions whose answers are already known from context.
- **REQ-G-003** (Event): **When** the interview completes, the goose skill shall scan the installed-plugin inventory at `~/.claude/plugins/` before designing any agent or skill chain.
- **REQ-G-004** (Ubiquitous): The goose skill shall design USER-CUSTOM agents and skill chains generated per-user from interview context; it shall not copy prebuilt plugin agents.
- **REQ-G-005** (Event): **When** generation begins, the goose skill shall produce: (a) a project `CLAUDE.md` of at most 200 lines whose Desktop-variant template preserves **all 8** `## N. … (HARD)` H2 rule blocks of the source `CLAUDE.md.tmpl` (the HARD blocks are marked with parenthesized `(HARD)` in H2 headings — pattern `^## .*\(HARD\)`; the source count is exactly 8, measured at M1); (b) `.claude/agents/*.md` — one per recurring task type, each with minimal-permission frontmatter, the 7-step agent loop, and project context; (c) a `.moai/` scaffold (`config.json`, `context.md`, `credentials.env` guidance, `cache/`, `evolution/`).
  - **REQ-G-005a** (Ubiquitous — HARD-block preservation invariant): The goose Desktop `CLAUDE.md` template shall contain exactly the 8 source `## N. … (HARD)` H2 blocks (`grep -cE '^## .*\(HARD\)'` == 8; the source uses parenthesized `(HARD)`, never bracketed `[HARD]`). The line-budget overflow policy (≤200 lines; auto-shrink targets skill-chain enumerations only; HARD blocks are never shrunk or deleted) is preserved per REQ-G-005b.
  - **REQ-G-005b** (Ubiquitous — line-budget overflow policy): The goose Desktop `claudemd-generator` variant shall retain the `### 2.1 라인 예산 (200라인 이내)` budget table, the NFR-PMR-002 invariant (`generated CLAUDE.md ≤ 200 lines`), and the shrink-chains-only rule (on >200-line overflow, only skill-chain enumerations are auto-shrunk to at most 10; the 8 HARD blocks are never shrunk or deleted). Provenance: `claudemd-generator.md:8,14,41,43,159,178` + `CLAUDE.md.tmpl:26` `@MX:REASON`.
- **REQ-G-006** (Event): **When** any of the 4 self-improvement triggers is detected, the goose skill shall run the simplified recursive self-improvement cycle: signal detection → diagnosis → minimal diff (≤3 files) → 1-line log appended under the CLAUDE.md `<!-- evolution-log -->` marker. The 4 triggers are authored in the goose `## Recursive Self-Improvement` section as English machine-anchor keyword tokens (per REQ-X-001 identifier rule; explanatory prose is conversation_language): **`repeated correction`** (≥2 on the same behavior), **`chain failure`** (skill-chain repeatedly fails/detours at the same step), explicit **`/project evolve`** (single-slash — the legacy manual-evolve subcommand), **`inventory drift`** (installed-plugin inventory diverges from the `.moai/config.json` snapshot).
- **REQ-G-007** (State): **While** executing a self-improvement cycle, the goose skill shall modify only `CLAUDE.md` and `.claude/agents/` (guardrail).
- **REQ-G-008** (Unwanted — Desktop parity): The goose skill shall not generate hooks, LSP configuration, or output-styles. Provenance: hooks, LSP, and output-styles do not function in Claude Cowork (`.moai/reports/expert-plugin-expansion-plan-2026-07-09.html`). The Desktop-parity prohibition is worded with these class names only — never the artifact-path tokens AC-PMA-004b greps for (see `design.md §G` authoring constraint).

### C.2 MoAI skill (`/moai --project`)

- **REQ-M-001** (Ubiquitous): The moai-pm plugin shall expose a `moai` skill invoked as `/moai --project <instruction>`, acting as the development-project initialization advisor carrying moai-adk v3.0 philosophy (SPEC plan/run/sync workflow, TRUST 5 quality, DDD/TDD).
- **REQ-M-002** (Event): **When** `/moai --project` is invoked, the moai skill shall run the Socratic interview plus stack/language detection before any generation.
- **REQ-M-003** (Event): **When** generation begins, the moai skill shall produce into the TARGET project: `CLAUDE.md`, `.claude/agents/`, project-specific `.claude/skills/`, `.claude/settings.json` (permissions allowlist, hooks wiring), hooks scripts, and a project `.mcp.json` restricted to survey-selected servers from the SPEC-MOC-CODER-LSP-MCP-001 catalog.
- **REQ-M-004** (Event): **When** generation begins, the moai skill shall perform an LSP server presence check and emit per-language install guidance (catalog + guidance content owned by SPEC-MOC-CODER-LSP-MCP-001; this skill consumes it).
- **REQ-M-005** (Capability gate): **Where** the coder plugin `moai` is installed, the moai-pm `moai` skill shall route execution to it; the skill documentation shall state the namespace resolution explicitly (`moai-pm:moai` = Desktop-side initialization advisor; `moai:moai` = coder-side execution).
- **REQ-M-006** (Capability gate): **Where** the coder plugin is NOT installed, the moai skill shall degrade gracefully to guidance-only output using an embedded fallback summary of the catalog (no execution routing attempted).
- **REQ-M-007** (Ubiquitous): The moai skill shall assume Claude Code runtime for its generated artifacts (hooks/LSP valid there) — the inverse of REQ-G-008.
- **REQ-M-008** (Ubiquitous — command-surface disambiguation): The moai skill documentation shall explicitly disambiguate two colliding surfaces that share the `moai` + `project` tokens: (i) `/moai project` — the PRE-EXISTING coder-plugin subcommand (`plugins/moai/commands/project.md`, which dispatches `Skill("moai:moai") with arguments: project $ARGUMENTS` to generate `product.md` / `structure.md` / `tech.md` / `codemaps/`); and (ii) `/moai --project` — the NEW moai-pm flag form (this SPEC's dev-project initialization advisor). The documentation shall state that the two are distinct entry points with different semantics and that `/moai --project` (flag) never shadows or replaces `/moai project` (subcommand). The precise mapping table lives in `design.md §F.1`.
- **REQ-M-009** (Ubiquitous — legacy subcommand-surface migration): The legacy unified `/project` skill exposed 7 subcommands (`resume`, `catalog`, `status`, `apikey`, `doctor`, `feedback`, `evolve` — `SKILL.md:10,175-181`). Each shall have a documented destination in the redesign (routed to `goose`, routed to `moai`, or explicitly dropped), enumerated in the `design.md §F.1` migration table with a one-line rationale per subcommand. No legacy subcommand may be silently lost.

### C.3 Reference reorganization

- **REQ-R-001** (Ubiquitous): The 13 canonical reference files + `CLAUDE.md.tmpl` shall be split/absorbed into `skills/goose/references/` and `skills/moai/references/` per the disposition matrix in `design.md §C`.
- **REQ-R-002** (Event): **When** a reference file is migrated, drift item 1 shall be fixed in the migrated copy: no old 4-plugin / 27-plugin architecture remnants; plugin-family statements align to the live `.claude-plugin/marketplace.json` 18-plugin roster; story-*/book-* skills attributed to `moai-story` (their post-`e06086c` owner — NOT `moai-writer`).
- **REQ-R-003** (Ubiquitous): The migrated references shall carry exactly ONE self-evolution model — the simplified recursive self-improvement model. The heavy 5-step Self-Refine (metrics.csv, forced 1-10 scoring) shall be removed, not deprecated-in-place.
- **REQ-R-004** (Ubiquitous): The custom-agent generation phase (current SKILL.md Phase 7) shall be restored into the goose setup canon (the migrated successor of `cowork-setup.md`'s phase sequence).
- **REQ-R-005** (Ubiquitous): Skill-prefix ownership shall be correct everywhere in migrated content (`moai-story:` for story-*/book-*; no stale `moai-coworker:story-` / `moai-coworker:book-` prefixes for moved skills). Post-`e06086c` baseline is already clean (0 stale hits); this REQ prevents re-introduction during migration.
- **REQ-R-006** (Unwanted): The legacy `skills/project/` directory shall not remain after the redesign, including the stray runtime artifacts inside it (`.claude/agent-memory/`, `.moai/state/`).

### C.4 Documentation

- **REQ-D-001** (Ubiquitous): `plugins/moai-pm/README.md` shall be rewritten as a 2-skill entry (goose + moai).
- **REQ-D-002** (Event): **When** run-phase completes, the `.claude-plugin/marketplace.json` moai-pm entry version shall be bumped.
- **REQ-D-003** (Ubiquitous): The www guide update points shall be recorded as a target-path list only (sync-phase task; run-phase shall not edit `www/**`).

### C.5 Cross-cutting

- **REQ-X-001** (Ubiquitous): All generated user-facing text (interview prompts, advisory messages, generated CLAUDE.md prose) shall be in the user's conversation_language; **identifiers shall be English** — where "identifiers" explicitly includes: skill/agent names, and, within the authored goose/moai `SKILL.md` files, the **structural H2 section anchors** (`## Socratic Interview`, `## Plugin Inventory Scan`, `## Custom Agent & Skill-Chain Design`, `## Generation Targets`, `## Recursive Self-Improvement`, `## Desktop Parity Constraints`, `## Namespace & Routing`, etc.) and the **self-improvement trigger keyword tokens** (`repeated correction`, `chain failure`, `/project evolve`, `inventory drift`). These English anchors/tokens are the grep targets for the machine-gate ACs; explanatory body prose under each anchor is authored in conversation_language. See `design.md §A.1` for the anchor/prose split declaration. (Note: the pre-existing `plugins/moai-pm/skills/project/SKILL.md` uses Korean H2 headings; the NEW goose/moai skills adopt the English-anchor convention above so the machine-gate ACs are language-stable.)
- **REQ-X-002** (Ubiquitous): Interview flows shall use AskUserQuestion-only interaction; subagents designed by goose/moai shall never prompt the user (blocker-report pattern instead).
- **REQ-X-003** (Ubiquitous): The anti-AI-slop post-processing chain shall be preserved wherever the current canon mandates it.

## §D Acceptance Criteria

Canonical AC enumeration with per-AC verification commands lives in `acceptance.md` — 21 machine-gate ACs (AC-PMA-001..013, plus 004b, 005b, and 017..022) and 3 structural-review ACs (AC-PMA-014..016). Every machine-gate AC is decided by a single command's exit status or numeric/`PASS`/`FAIL` output (file existence, grep assertions, `jq`/`test` checks); structural-review ACs are labelled and excluded from the machine-gate batch.

## §E Exclusions

The following are explicitly out of scope for this SPEC.

### Out of Scope — Runtime E2E in Claude Cowork / Claude Code

- Live invocation of `/goose --project` or `/moai --project` in a real Desktop or Code session is NOT verified in this SPEC's run-phase. Acceptance is authoring-level (structural greps, file existence, JSON validity). Runtime E2E is a post-sync manual validation item.

### Out of Scope — Coder plugin (`plugins/moai`) file changes

- `.lsp.json`, `.mcp.json`, MCP catalog, install-guidance content, SessionStart advisory hook, and meta-harness templates are owned by SPEC-MOC-CODER-LSP-MCP-001. This SPEC only CONSUMES the catalog interface (design.md §H).

### Out of Scope — Other plugins' skills

- No modifications to `moai-coworker`, `moai-writer`, `moai-designer`, or any other family plugin, even where drift fixes reference their skill prefixes.

### Out of Scope — www content authoring

- Run-phase lists www guide target paths only (REQ-D-003); actual www edits belong to sync-phase / a follow-up task.

### Out of Scope — Hooks / LSP / output-styles generation by Goose

- Per REQ-G-008 (Desktop parity), Goose never emits these artifact classes; adding Desktop support for them is not this SPEC's concern.

### Out of Scope — Legacy SPEC frontmatter edits

- Marking SPEC-MOC-PM-REDESIGN-001 as partially superseded is a sync-phase manager-docs task, not run-phase.

## §F Cross-References

- `plan.md` — milestones, technical approach, risks
- `design.md` — two-skill architecture, interview design, reference disposition matrix, artifact schemas, namespace routing, SPEC-2 interface contract
- `acceptance.md` — AC matrix + verification commands
- SPEC-MOC-CODER-LSP-MCP-001 — sibling SPEC (catalog/LSP/meta-harness provider)
- `.moai/reports/expert-plugin-expansion-plan-2026-07-09.html` — Desktop parity constraint provenance
