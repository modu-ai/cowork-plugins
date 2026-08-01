---
id: SPEC-MOC-PM-ADVISORS-001
document: plan
version: "0.2.1"
status: completed
created: 2026-07-10
updated: 2026-07-11
---

# Plan — SPEC-MOC-PM-ADVISORS-001

## §A Context

Tier L redesign of `plugins/moai-pm`: remove the monolithic `project` skill, build two super-advisor skills (`goose`, `moai`), migrate 13 canonical references + CLAUDE.md.tmpl with 4 drift fixes applied in-flight, and align docs. All design decisions are FINAL (2-round Socratic interview complete) — run-phase does not re-open them.

Run-phase implementation agents will be spawned with **model=sonnet, effort=xhigh**; milestones below are sized for that profile: independent, file-ownership-separated, each completable without cross-milestone context.

## §B Known Issues (input defects to fix during migration)

| # | Defect | Location (re-measured post-`e06086c`) | Fix policy |
|---|--------|----------|-----------|
| 1 | Old 4-plugin / 27-plugin remnants (ACTIVE — count re-captured at M1, not hardcoded) | `references/core/` across 5 files: `designer-setup.md`, `cowork-setup.md`, `INDEX.md`, `coder-setup.md`, `init-protocol.md` (`router.md` already clean; exact line anchors + hit count re-grepped at M1 per §C step 1, recorded to progress.md §E.2 — AC-PMA-013 closes against those greps, not a literal count) | Rewrite against live 18-plugin marketplace.json roster; story-*/book-* → moai-story |
| 2 | Dual self-evolution models (ACTIVE) | `evolution-protocol.md` heavy Self-Refine (7 hits: lines 5,9,76,99,102,272,286 — `metrics.csv`, `self-refine-log.md`, forced 1-10 scoring) vs `SKILL.md:146` `## 재귀적 자가 개선 (HARD)` (simplified, CURRENT) | Remove heavy model entirely; simplified model is the only model |
| 3 | Custom-agent generation absent from setup canon (ACTIVE) | `cowork-setup.md` 8-Phase summary has Phase 7 = **API 키** and 0 `에이전트` mentions; `SKILL.md:135` defines `## 커스텀 에이전트 생성 (--cowork Phase 7)` | Restore custom-agent generation as a first-class phase in goose setup canon |
| 4 | Skill-prefix ownership (RESOLVED by `e06086c` — re-verify only) | 0 stale `moai-coworker:story-`/`moai-coworker:book-` hits; owner is `moai-story:`; `cowork-setup.md:124` cites `moai-story:story-project` | No active fix — AC-PMA-003 re-verifies no stale prefix is re-introduced |

Line numbers above are content-token anchors re-measured against the committed `e06086c` tree (working tree CLEAN); M1 re-captures exact lines before editing in case a later commit lands. Item 4 is a verified no-op (retained as a regression gate only).

## §C Pre-flight (M1 detail)

1. Re-grep the 4 drift items and record exact current line matches to `progress.md §E.2` (files drift daily in this repo).
2. Snapshot baseline: `grep -cE '^## .*\(HARD\)' plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl` → **8** (the source marks HARD blocks with parenthesized `(HARD)` in H2 headings, verified at lines 17,28,38,47,68,77,86,135). NOTE: `grep -c '\[HARD\]'` returns **0** on this file and MUST NOT be used — the bracket form never appears. AC-PMA-005 asserts the goose Desktop template preserves exactly these 8 blocks (`== 8` against the FIXED literal baseline 8, NOT a runtime-recomputed count that a broken/emptied file could satisfy).
3. Snapshot current moai-pm version: `jq` from `.claude-plugin/marketplace.json` (bump target for M5, baseline for AC-PMA-009).
4. Command-name collision scan: grep the plugin family for an existing `goose` skill/command name; confirm `/goose` is free.
5. Freeze the reference disposition matrix (design.md §C) into a concrete per-file move list — any deviation discovered at run-phase is a blocker report, not a silent re-design.

## §D Constraints

- Write scope: `plugins/moai-pm/**`, `.claude-plugin/marketplace.json` (this SPEC's M5 is the SINGLE cross-SPEC owner — edits BOTH the `moai-pm` entry AND the `moai` entry-delta handed by SPEC-MOC-CODER-LSP-MCP-001 per design.md §H / F12), `.moai/specs/SPEC-MOC-PM-ADVISORS-001/**`. NO `www/**`, no other plugin source directories (editing the `moai` marketplace ROSTER entry is not editing the `moai` plugin source).
- The working tree carries uncommitted files from parallel sessions — commits MUST be pathspec-scoped to the files this SPEC owns (lesson: parallel-session stash race).
- Drift fixes are applied DURING migration (copy-and-fix in one edit), never as a separate later pass.
- User-facing generated text in conversation_language; identifiers English (REQ-X-001).
- No time estimates; priority labels only.

## §E Self-Verification

Run-phase completion requires executing every command in `acceptance.md §D` and recording verbatim evidence (exit codes + bounded tails) in `progress.md §E.2`/`§E.3`. Key gates:

- 2-skill structure exists; `skills/project/` fully absent (AC-PMA-001)
- Zero heavy-Self-Refine remnants; zero stale prefixes; zero 4-plugin remnants (AC-PMA-002/003 + drift-line checklist from M1)
- Canonical grep-anchor headings present in both SKILL.md files (AC-PMA-004..007)
- README/marketplace/link-integrity gates (AC-PMA-008/009/011)

## §F Milestones

Priority-based; no time estimates. M2 ∥ M3 are parallelizable (disjoint write ownership) after M1.

| M | Priority | Scope | File ownership (write) | Depends on |
|---|----------|-------|------------------------|------------|
| M1 | High | Pre-flight capture: drift-line re-grep, HARD-block baseline, marketplace version baseline, `/goose` collision scan, disposition-matrix freeze | `.moai/specs/SPEC-MOC-PM-ADVISORS-001/progress.md` only | — |
| M2 | High | Goose skill build: `skills/goose/SKILL.md` + `skills/goose/references/**` — absorb assigned references per disposition matrix, apply drift fixes 1/2/3/4 in migrated content, encode interview (A/B/C), inventory scan, custom-agent design, generation targets, simplified self-improvement (4 triggers + guardrails), Desktop parity prohibition | `plugins/moai-pm/skills/goose/**` | M1 |
| M3 | High | MoAI skill build: `skills/moai/SKILL.md` + `skills/moai/references/**` — interview + stack detection, generation targets (CLAUDE.md / agents / skills / settings.json / hooks / .mcp.json), LSP presence-check consumption, namespace routing + degraded mode, embedded catalog fallback summary | `plugins/moai-pm/skills/moai/**` | M1 |
| M4 | Medium | Legacy removal + integrity sweep: delete `skills/project/` (incl. stray `.claude/`, `.moai/` runtime artifacts), regenerate INDEX per skill, repo-wide prefix/remnant sweep within `plugins/moai-pm/` | `plugins/moai-pm/skills/project/` (delete), both skills' INDEX/reference cross-links | M2, M3 |
| M5 | Medium | Docs: README 2-skill rewrite, marketplace.json version bumps (SINGLE cross-SPEC owner — `moai-pm` entry + the `moai` entry-delta handed by SPEC-MOC-CODER-LSP-MCP-001 M6 per §H/F12), www guide target-path list recorded to progress.md | `plugins/moai-pm/README.md`, `.claude-plugin/marketplace.json` (both `moai-pm` and `moai` entries), progress.md | M4, sibling SPEC M6 delta recorded |
| M6 | Medium | Self-verification batch: run all acceptance.md commands, record evidence, resolve or report residuals | progress.md | M5 |

## §G Anti-Patterns (run-phase)

- Copying a reference file verbatim and deferring drift fixes ("fix later") — violates §D constraint.
- Retaining `evolution-protocol.md` with a DEPRECATED banner — REQ-R-003 mandates removal.
- Hardcoding a plugin-family count ("15-plugin", "16-plugin") in migrated references — cite marketplace.json as roster authority instead.
- Generating hooks/LSP/output-styles examples inside goose references (violates REQ-G-008 even as documentation examples, unless clearly marked as prohibited-example).
- Unscoped `git add -A` commits (parallel-session working tree).
- Editing acceptance.md mid-run without orchestrator re-delegation (D-NEW-1 pattern required).

## §H Cross-References

- `design.md` §C — reference disposition matrix (M2/M3 input)
- `design.md` §H — SPEC-MOC-CODER-LSP-MCP-001 interface contract (M3 input)
- `acceptance.md` — AC matrix (M6 input)
- Soft ordering note: SPEC-MOC-CODER-LSP-MCP-001's catalog (its M4) should exist before this SPEC's M3 finalizes the catalog path reference; if run in parallel, M3 references the contracted path from design.md §H and flags a residual if the sibling SPEC has not landed it.

## Open design risks (identified at plan-phase; NOT resolved here)

1. **Catalog fallback drift**: REQ-M-006's embedded fallback summary duplicates SPEC-2 catalog data inside moai-pm → two sources that can drift. No sync mechanism is specified.
2. **`/goose` name collision**: assumed free; M1 scan is the gate. If a family plugin claims `goose`, naming needs a user decision (blocker).
3. **`/moai` short-form dispatch ambiguity**: with both moai-pm and coder `moai` installed, runtime resolution order of the short `/moai` form is platform-defined and may not be controllable; explicit-namespace documentation (REQ-M-005) + the `/moai project` vs `/moai --project` disambiguation table (REQ-M-008, design.md §F.1) mitigate but do not eliminate.
4. **Shared-reference duplication**: several references serve both skills (e.g. context-collector, claudemd-generator); Desktop skill loaders may not support a shared directory across two skills → per-skill copies accepted, creating a dual-maintenance surface.
5. **Interview grade model drift**: A/B/C semantics cited from SKILL.md at audit time; M1 must re-verify semantics against current `SKILL.md` before M2 encodes them.
6. **Live plugin-family churn**: the family reached 18 plugins at `e06086c`; marketplace.json-as-authority handles roster churn, but references written during run-phase may still race a later family change.

> **Resolved at iter-2 (was open risk #4 — "no overflow policy"):** the pre-existing `claudemd-generator.md` DOES specify an overflow policy (≤200 lines; auto-shrink targets skill-chain enumerations only, max 10; the 8 HARD blocks are never shrunk/deleted — `claudemd-generator.md:8,14,41,43,159,178` + `CLAUDE.md.tmpl:26`). The policy is now migrated into REQ-G-005b + design.md §D and gated by AC-PMA-005b; the risk is deleted, not carried forward.
