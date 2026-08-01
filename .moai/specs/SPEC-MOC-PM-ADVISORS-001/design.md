---
id: SPEC-MOC-PM-ADVISORS-001
document: design
version: "0.2.1"
status: completed
created: 2026-07-10
updated: 2026-07-11
---

# Design — SPEC-MOC-PM-ADVISORS-001

## §A Two-skill architecture

```
plugins/moai-pm/
├── README.md                      # 2-skill entry (M5 rewrite)
├── .claude-plugin/plugin.json     # untouched by run-phase except via marketplace sync conventions
└── skills/
    ├── goose/                     # /goose --project — Desktop super-orchestrator/advisor
    │   ├── SKILL.md
    │   └── references/            # migrated per §C disposition matrix
    └── moai/                      # /moai --project — dev-project initialization advisor
        ├── SKILL.md
        └── references/
```

Job split:

| Axis | goose | moai |
|------|-------|------|
| Runtime assumption | Claude Cowork (Desktop) | Claude Code |
| Domain | ALL non-coding work | Development-project initialization |
| Generates | CLAUDE.md (≤200 lines), .claude/agents/, .moai/ scaffold | CLAUDE.md, .claude/agents/, .claude/skills/, .claude/settings.json, hooks, .mcp.json |
| Hooks/LSP/output-styles | PROHIBITED (Desktop parity) | Valid (Code runtime) |
| Self-improvement | Simplified recursive model, 4 triggers | Delegates to moai-adk conventions in target project |
| Downstream routing | Skill chains across installed family plugins | Routes execution to coder plugin `moai` when installed |

### A.1 Goose flow (canonical section order in SKILL.md — these headings are AC grep anchors)

> **Language-anchor split declaration (reconciles REQ-X-001 with the machine-gate ACs).** In the NEW goose/moai `SKILL.md` files authored by run-phase, the **structural H2 section anchors** and the **self-improvement trigger keyword tokens** are **English identifiers** (machine-facing grep anchors — treated as identifiers under REQ-X-001, the same class as skill/agent names). The **explanatory body prose** beneath each anchor is authored in the user's `conversation_language`. This is a deliberate divergence from the pre-existing `plugins/moai-pm/skills/project/SKILL.md`, whose H2 headings are Korean (`## 개요`, `## 라우팅 (핵심)`, `## 재귀적 자가 개선 (HARD)`, `## 커스텀 에이전트 생성 (--cowork Phase 7)`, …) and whose self-improvement triggers are Korean prose (`SKILL.md:149-156`). The new skills adopt English anchors so every grep AC (AC-PMA-004/006/007/012, S1, S2) targets a language-stable string. Every grep AC in `acceptance.md` targets **exactly** the anchor form enumerated below (goose) and in §A.2 (moai); run-phase authors the headings verbatim.

1. `## Socratic Interview` — context grades A/B/C; no re-asking; AskUserQuestion-only
2. `## Plugin Inventory Scan` — `~/.claude/plugins/` enumeration before any design
3. `## Custom Agent & Skill-Chain Design` — user-custom, generated from interview context; never copies of prebuilt plugin agents
4. `## Generation Targets` — CLAUDE.md / agents / .moai scaffold
5. `## Recursive Self-Improvement` — 4 English trigger keyword tokens (`repeated correction`, `chain failure`, `/project evolve`, `inventory drift`) + guardrails; explanatory prose in conversation_language
6. `## Desktop Parity Constraints` — hooks, LSP, output-styles prohibition (all three artifact classes named by class name — bare words, never artifact-path tokens; see §G authoring constraint)

### A.2 MoAI flow (canonical section order — AC grep anchors)

1. `## Socratic Interview & Stack Detection`
2. `## Generation Targets` — CLAUDE.md / agents / skills / settings.json / hooks / .mcp.json
3. `## LSP Presence Check` — consumes SPEC-MOC-CODER-LSP-MCP-001 guidance
4. `## MCP Survey` — catalog-driven selection; credentials never bundled
5. `## Namespace & Routing` — moai-pm:moai vs moai:moai + degraded mode

## §B Interview design

- **Grades**: A = sufficient context to proceed without questions on that topic; B = partial (targeted questions only); C = absent (full topic interview). Grading is per-topic, not per-session. No question may be re-asked once its answer is derivable from prior answers or scanned context.
- **Channel**: AskUserQuestion-only for all questions (Desktop/Code both). Agents that goose/moai GENERATE must carry the subagent boundary: return blocker reports, never prompt.
- **Termination**: interview ends when all generation-blocking topics reach grade A/B-with-assumption; grade-C-remaining topics either block (with explicit ask) or proceed with documented assumptions (edge case S4 in acceptance.md).
- Re-verify grade semantics against current SKILL.md at M1 (open risk #6): SKILL.md drifted after the audit.

## §C Reference disposition matrix (13 files + tmpl)

FINAL at plan level; M1 freezes it into a per-file move list; deviations at run-phase are blocker reports.

| Source (`references/core/`) | Destination | Disposition | Drift fixes applied in-flight |
|---|---|---|---|
| `router.md` | split → goose + moai | Entry routing splits per skill: goose keeps non-coding routing; moai keeps dev-init routing | prefix sweep (item 4) |
| `cowork-setup.md` | goose | Migrate; restore custom-agent generation phase into the setup canon | items 1 (lines 29,84), 3, 4 |
| `designer-setup.md` | goose | Migrate | item 4 |
| `coder-setup.md` | moai | Migrate | items 1, 4 |
| `init-protocol.md` | split → goose (primary) + moai (dev-init sections) | Migrate with split | item 1 (line 329), 4 |
| `execution-protocol.md` | split → goose (primary) + moai (execution handoff) | Migrate; the deprecation note (664-666) is honored by REMOVING the heavy model, then the note itself becomes obsolete and is dropped | items 2, 4 |
| `context-collector.md` | goose (copy to moai if needed) | Migrate | item 4 |
| `claudemd-generator.md` | both (per-skill variants) | goose = Desktop variant (≤200 lines, HARD preservation); moai = dev variant | item 4 |
| `evolution-protocol.md` | **DROP** | Content NOT migrated; simplified model is authored directly in goose SKILL.md §Recursive Self-Improvement | item 2 (removal) |
| `evaluation-protocol.md` | goose | Migrate (advisor QA) | item 4 |
| `quality-evaluator.md` | goose | Migrate | item 4 |
| `diagnostic-protocol.md` | goose | Migrate; moai links | item 4 |
| `INDEX.md` | regenerate per skill | NOT migrated; each skill gets a fresh INDEX over its own references | item 1 (line 103) resolved by regeneration |
| `templates/CLAUDE.md.tmpl` | both (per-skill variants) | goose variant preserves ALL HARD rule blocks (count baseline at M1) + Desktop content; moai variant = dev-project template | — |

Duplication policy: per-skill copies are ACCEPTED where both skills need content (open risk #5 dual-maintenance noted); no shared cross-skill reference directory is introduced.

## §D Generated artifact schemas (goose outputs)

- **CLAUDE.md** (target project): ≤200 lines; structure = header + HARD rule blocks (verbatim from template) + project context + `<!-- evolution-log -->` marker section (1-line entries appended by self-improvement).
  - **Line-budget overflow policy (migrated from `claudemd-generator.md` — REQ-G-005b).** The pre-existing generator already has an overflow policy (contra plan.md's earlier "no overflow policy" risk, now deleted). The goose Desktop `claudemd-generator` variant MUST retain, verbatim in intent:
    1. The `### 2.1 라인 예산 (200라인 이내)` line-budget table (provenance `claudemd-generator.md:41`).
    2. The NFR-PMR-002 invariant — generated `CLAUDE.md ≤ 200 lines` — carried as an `@MX:ANCHOR` proof point (provenance `claudemd-generator.md:43`).
    3. The **shrink-chains-only** rule: on >200-line overflow, the ONLY auto-shrink target is skill-chain enumerations (reduced to at most 10 chains); the 8 `## N. … (HARD)` blocks are **never shrunk or deleted** (provenance `claudemd-generator.md:14,159,178` + `CLAUDE.md.tmpl:26` `@MX:REASON`).
  - The 8 `## N. … (HARD)` H2 blocks preserved by REQ-G-005a are, verbatim from the source `templates/CLAUDE.md.tmpl` (section number + title, in source order):
    - `## 2. 행동 원칙 (HARD)`
    - `## 3. 요청 평가 사다리 (HARD)`
    - `## 4. 파일 생성 기준 (HARD)`
    - `## 5. 문서·콘텐츠 생성 우선순위 (HARD)`
    - `## 6. AI 슬롭 후처리 (HARD)`
    - `## 7. 인용·저작권 가드 (HARD)`
    - `## 8. 톤 규칙 (HARD)`
    - `## 14. 맥락 적용 규칙 (HARD)`

    Count is exactly 8 (`grep -cE '^## .*\(HARD\)' templates/CLAUDE.md.tmpl` → 8; parenthesized `(HARD)`, never bracketed `[HARD]`). AC-PMA-005 (count == 8) + AC-PMA-005b (budget-table + shrink-chains-only rule present) gate this.
- **`.claude/agents/*.md`**: one per recurring task type. Frontmatter: `name`, `description`, `tools:` minimal-permission list (only tools the task type needs; no `Agent` tool → no nesting). Body: 7-step agent loop + injected project context + subagent boundary (blocker reports, never prompt).
- **`.moai/` scaffold**: `config.json` (project meta + language + installed-plugin snapshot), `context.md` (interview digest), `credentials.env` GUIDANCE only (placeholder file with instructions; never real values), `cache/` (empty, .gitkeep), `evolution/` (self-improvement diagnosis records).

## §E Self-improvement model (single model, simplified)

- **Triggers (4)** (authored as English keyword tokens per §A.1 declaration): (1) `repeated correction` — ≥2 on the same behavior; (2) `chain failure` — skill-chain repeatedly fails/detours at the same step; (3) explicit `/project evolve` (single-slash legacy manual-evolve subcommand); (4) `inventory drift` — installed-plugin inventory diverges from the `.moai/config.json` snapshot.
- **Cycle**: signal detection → diagnosis → minimal diff (≤3 files) → 1-line log under CLAUDE.md `<!-- evolution-log -->`.
- **Guardrails**: only `CLAUDE.md` + `.claude/agents/` are modifiable; ≤3 files per improvement; no metrics.csv, no forced 1-10 scoring, no 5-step Self-Refine loop (removed model).

## §F Namespace & routing

- `moai-pm:moai` (this SPEC) = Desktop-side INITIALIZATION advisor. `moai:moai` (coder plugin) = execution.
- **Where** coder plugin installed → moai-pm:moai routes execution to it after initialization artifacts are generated.
- **Where** absent → guidance-only degraded mode: generated artifacts + install pointer + embedded catalog fallback summary (REQ-M-006).
- SKILL.md must document collision resolution by explicit namespace; short-form `/moai` runtime dispatch order is acknowledged as platform-defined (open risk #3).

### §F.1 Command-surface disambiguation + legacy subcommand migration (REQ-M-008 / REQ-M-009)

**Two colliding `moai`+`project` surfaces (REQ-M-008).** The moai `SKILL.md` MUST document both, and state they are distinct entry points:

| Surface | Form | Owner | Semantics | Verified provenance |
|---------|------|-------|-----------|---------------------|
| `/moai project` | subcommand (space) | coder plugin (`plugins/moai`) | Generate `product.md` / `structure.md` / `tech.md` / `codemaps/` for the current project. Dispatches `Skill("moai:moai") with arguments: project $ARGUMENTS`. | `plugins/moai/commands/project.md:2,8` (exists today) |
| `/moai --project` | flag (double-dash) | moai-pm `moai` skill (this SPEC) | Dev-project initialization advisor: interview + stack detection + generate CLAUDE.md/agents/skills/settings.json/hooks/.mcp.json. | this SPEC |

Rule: `/moai --project` (flag) does NOT shadow, replace, or intercept `/moai project` (subcommand). The moai `SKILL.md` documents the distinction explicitly (AC-PMA-018 grep-verifies both forms are documented).

**Legacy `/project` subcommand-surface migration (REQ-M-009).** The pre-existing unified `/project` skill exposed 7 subcommands (`SKILL.md:10,175-181`). Each has exactly ONE documented destination:

| Legacy subcommand | Destination | Rationale |
|-------------------|-------------|-----------|
| resume | both (goose + moai) | Gap-detection re-entry is per-skill; each advisor supports resuming its own interrupted init flow. |
| catalog | goose | Family/skill catalog listing is a Desktop non-coding advisory concern (18-plugin roster from marketplace.json). |
| status | both (goose + moai) | "current config status" is meaningful for either advisor's generated artifacts. |
| apikey | both (goose + moai) | Credentials-guidance surface; both skills emit `.env` / `credentials.env` guidance (never real values). |
| doctor | moai | Environment/toolchain diagnostics are a Claude Code dev-init concern; goose (Desktop) has no LSP/hooks toolchain to diagnose. |
| feedback | dropped | Superseded by the coder `/moai feedback` workflow; not re-exposed under goose/moai init advisors. |
| evolve | goose | Manual trigger of the recursive self-improvement cycle, which lives in goose (REQ-G-006). Canonical form `/project evolve` (single slash). |

AC-PMA-017 machine-verifies every one of the 7 subcommand tokens has a `| <token> |` row (with a destination) in this table.

## §G Desktop parity constraints

Provenance: `.moai/reports/expert-plugin-expansion-plan-2026-07-09.html` — hooks, LSP, output-styles do NOT function in Claude Cowork. Consequences encoded in goose:

- No hooks wiring, no LSP configuration, no output-style files in ANY goose generation path — expressed with class names, never artifact-path tokens.
- The prohibition is stated in a dedicated `## Desktop Parity Constraints` section (AC grep anchor) naming all three artifact classes by class name (`hooks`, `LSP`, `output-styles`).
- [HARD] Authoring constraint (satisfies AC-PMA-004 + AC-PMA-004b): the goose `## Desktop Parity Constraints` section AND the goose `claudemd-generator` variant MUST name the three prohibited classes by class name ONLY — the bare words `hooks`, `LSP`, `output-styles`, which satisfy the positive-presence grep AC-PMA-004 — and MUST NOT contain the artifact-path token literals enumerated in `acceptance.md` AC-PMA-004b (the LSP JSON-config filename and the hooks-directory path token). AC-PMA-004b greps the goose SKILL.md + claudemd-generator.md for those path-token literals and requires a zero count; writing them in the prose would false-fail the gate.

## §H Interface contract with SPEC-MOC-CODER-LSP-MCP-001

| Contract item | Value |
|---|---|
| Canonical MCP catalog | JSON file owned by SPEC-2 under `plugins/moai/` (default contract path: `plugins/moai/references/dev-mcp-catalog.json`; SPEC-2 M4 may finalize the exact path — moai skill references the path recorded in SPEC-2's progress.md) |
| Consumption | moai-pm:moai reads the catalog when coder plugin installed; embedded fallback summary otherwise |
| LSP guidance | per-language install-command content owned by SPEC-2 (M3 there); moai-pm:moai consumes/points, never duplicates the full table |
| Credentials | catalog carries `.env` guidance only; moai-pm:moai must not inline any credential value into generated `.mcp.json` |
| Failure mode | catalog absent/unparseable → degrade to fallback summary + advisory note (never hard-fail initialization) |
| **marketplace.json single-owner (F12)** | This SPEC's **M5 is the SOLE writer** of `.claude-plugin/marketplace.json` for BOTH plugin entries — the `moai-pm` entry (this SPEC) AND the `moai` entry (SPEC-MOC-CODER-LSP-MCP-001 hands its version-bump delta via the orchestrator, recorded in the sibling's progress.md §E.2). This eliminates the cross-SPEC write race on the shared roster file. Baseline observed 2026-07-11: `.metadata.version == "6.2.0"`, `moai-pm` entry `0.4.0`, `moai` entry `1.0.0`. Ordering: SPEC-1 M5 runs after the sibling's M6 delta is recorded (or the orchestrator serializes the two final-docs milestones). |
