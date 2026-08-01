# SPEC-MOC-PLUGIN-REMEDIATION-001 — Progress

## §E.1 Plan-phase Audit-Ready Signal

Plan-phase artifacts (spec.md, plan.md, acceptance.md, progress.md) authored by manager-spec on 2026-07-02. Evidence base: the 3-way cross-verified Korean AI-tell audit persisted in auto-memory `project_plugin_korean_slop_audit.md` (origin session `28305de2`), plus **independent live re-verification of every target path against the `plugins/` tree at authoring time** (not trusted from the secondhand audit summary) per `.claude/rules/moai/core/verification-claim-integrity.md`. Re-verification surfaced count drift from the audit's frozen numbers (cowork 177 not 178; deprecated-ns 68 not 78; design 11 confirmed) — recorded in spec.md §A.3 — which is why all 24 acceptance criteria are re-runnable end-state predicates, not frozen counts.

- **Requirements**: 24 (REQ-REM-001..024, GEARS: Ubiquitous / Event-driven / Unwanted / Where).
- **Acceptance criteria**: 24 (AC-REM-001..024, full 1:1 REQ↔AC traceability, 5 GWT scenarios, 6 edge cases).
- **Tier**: L (constitutional-scale; PASS threshold 0.85). NOTE: delivered as the 3-file core + this progress.md; conventional Tier-L design.md/research.md folded into spec.md §A.2/§A.3 + plan.md §F (extractable if plan-auditor requires the 5-artifact set).
- **Milestones**: M1 (P0 gate structure + P2 immediate-failures, RELEASE-BLOCKING) → M2 (P1 decontamination) → M3 (P3 gate wiring) → M4 (P2 bulk repair) → M5 (Phase A rename + Phase B dedup) → M6 (P4 lint CI + re-sync note).
- **Scope**: owns `plugins/moai-cowork/skills/**`, `plugins/moai-design/skills/**`, `plugins/{moai-cowork,moai-design}/scripts/**`, skill-builder. Excludes moai-code, commands, templates (SPEC-MOC-BOOTSTRAP-DESKTOP-001), www (SPEC-MOC-SITE-IA-001).
- **www/plugins/ re-sync**: required after source edits, owned by SITE-IA (REQ-REM-024) — recorded here per that requirement.

Ready for plan-auditor independent review (Tier L threshold 0.85).

## §E — Phase 0.95 Mode Selection

**Input parameters**:
- tier: **L** (constitutional-scale; ~188 skill dirs + gates + lint CI)
- scope (file count): ~25-40 source files across M1-M6 (gates, slides, copy sources, router, skill-builder, lint script)
- domain count: 4 (Korean-slop detection/gate content, execution-path repair, namespace/rename mechanics, lint CI scripting)
- file language mix: ~95% Markdown skill bodies + 1 shell lint script (M6)
- concurrency benefit: **LOW** — coding-heavy content edits with sequential inter-file dependency (M4 namespace normalize MUST precede M5 rename; M2 copy edits settle before M5; M1 gate-structure additions referenced by M3 wiring)
- Agent Teams prereqs: not met

**Mode evaluation**:

| # | Mode | Selected? | Rationale |
|---|------|-----------|-----------|
| 1 | trivial | no | Multi-file, multi-milestone, semantic content edits |
| 2 | background | no | Write tasks; background-write forbidden |
| 3 | agent-team | no | Prereqs not met; coding-heavy (Anthropic caveat) |
| 4 | parallel | no | Coding-heavy + sequential inter-file dependency (M4→M5, M1→M3) |
| 5 | sub-agent | **YES** | Tier L + coding-heavy + sequential M1→M6 inter-file dependency |
| 6 | workflow | no | Not a single uniform mechanical transform; semantic reference-coupled edits |

**Decision**: `sub-agent` (Mode 5 — sequential, single implementer, no spawn).

**Justification**: Per Anthropic's coding-task parallelism caveat, this SPEC's milestones have strong sequential coupling: M1 gate-structure additions define the patterns M3 wiring references; M2 copy edits settle before M5 rename; M4 namespace normalization MUST precede M5 rename (EC-4); M6 lint CI runs last against final names. Mode 6 requires a single uniform mechanical transform with no inter-file dependency — this SPEC's edits are semantic (Korean copy decontamination, gate-structure authoring, genre-profile definition) and reference-coupled. Mode 5 sequential is the correct default.

## §E.2 Run-phase Evidence

### Re-baseline (run-phase pre-flight, 2026-07-02)

Live counts re-measured at run-phase start, compared against `spec.md` §A.3 plan-phase numbers. Per EC-1, the implementer proceeds against the LIVE numbers.

| Item | Plan-phase (§A.3) | Run-phase LIVE | Drift | Action |
|------|------------------|----------------|-------|--------|
| cowork skills | 177 | **177** | 0 | matches |
| design skills | 11 | **11** | 0 | matches |
| deprecated-namespace files (`grep -rl` 9 ns tokens) | 68 | **72** | +4 | proceed against live 72 (M4 sweeps all) |
| `ai-slop-reviewer` em-dash | 10 | **10** | 0 | AC-012 baseline confirmed |
| `humanize-korean` em-dash | 41 | **41** | 0 | AC-012 baseline confirmed |
| `pdf-writer` `moai-office` path spots | 4 (L56,59,60,95) | **4** (L56,59,60,95) | 0 | AC-006 confirmed |
| `humanize-korean` `moai-content` path | 3 (L73,89,170) | **3** (L73,89,170) | 0 | AC-007 confirmed |
| `live-commerce` deceptive-ad "집중력 200%" | present | **present** (references/live-script.md:79) | 0 | AC-010 confirmed |

**Drift disposition**: deprecated-namespace +4 drift is within the predicate-tolerant design (AC-015 is a `→0` end-state predicate, not a count). No material divergence requiring a blocker report.

### Milestone progress

- **M1** (AC-001..007, release-blocking): gate structure + P2 immediate path repair — PASS. Commit b7ca913.
- **M2** (AC-008..012, P1 decontamination): slide/deck sources, commerce/marketplace/detail-page/newsletter copy, deceptive-ad removal, boilerplate naturalization (50 files), gate em-dash reduction — PASS. Commit 9ef11e4.
- **M3** (AC-013..014, P3 gate wiring): 8 priority copy skills wired to gate chain; project router wired to moai-workflow-design; advisory→required standardized — PASS. Commit b6d6ecb.
- **M4** (AC-015..017, P2 bulk repair): 9 deprecated namespaces normalized across 70 files; project router rewritten for single-plugin architecture; stale CLAUDE.local.md/CONNECTORS.md refs repaired; ghost dir gone — PASS. Commit c0c80b9.
- **M5 Phase B** (AC-019..020, boundary dedup): design-system-library cowork copy → pointer (systems/ removed); brand-identity scope narrowed — PASS. Commit 7f59bd9.
- **M5 Phase A** (AC-018, category-prefix rename): §D.9 Phase A filesystem rename executed — 148 prefix-add + 2 body-rename = 150 skills renamed (26 no-op already-prefixed untouched); `name:` frontmatter self-references updated; cross-refs swept across 325 files / 2671 substitutions; 11 special-name context-anchored edits preserving URLs / genre enums / `/project feedback` command / `moai-design:` cross-plugin refs / GitHub attribution repos — PASS (0 dangling old-name references). Commit f44bb47.
- **M6** (AC-021..024, P4 re-occurrence prevention): skill-builder Korean authoring rules; lint CI script (korean-slop-lint.sh) with 4-class self-test; scope discipline; www re-sync note — PASS.

### AC-018 (Phase A category-prefix rename) — RESOLVED 2026-07-03

The deferred blocker is resolved: manager-spec authored the §D.9 Phase A Rename Mapping (176-row table, approved 2026-07-03 in commit e481bd6), and run-phase executed the filesystem rename in commit f44bb47. AC-REM-018 now PASS: for each of the 150 renamed old-names, `grep -rl "\bN\b"` finds 0 dangling standalone references — every residual word-boundary match is a legitimate non-dangling occurrence (new-name substring, external URL path, genre enum value, `/project feedback` command, `moai-design:` cross-plugin ref, or GitHub attribution repo URL) per acceptance.md §D.9.5 / L560 reviewer-distinguishes principle.

### www/plugins/ re-sync requirement (REQ-REM-024)

`www/plugins/` marketplace copies are STALE after these source edits (M1-M6 changed 177+ skill source files). A re-sync from `plugins/` → `www/plugins/` is REQUIRED before the next marketplace publish. This re-sync is owned by **SPEC-MOC-SITE-IA-001** (the www/docs-site SPEC) — this SPEC records the requirement (REQ-REM-024) and performs NO `www/` edit (AC-023/024). SITE-IA must re-copy the cowork + design plugin trees to `www/plugins/` and regenerate any marketplace manifests.

## §E.3 Run-phase Audit-Ready Signal

- **run_complete_at**: 2026-07-03 (AC-018 Phase A closure; M1-M6 were 2026-07-02)
- **run_commit_sha**: f44bb47 (M5 Phase A, final run-phase commit)
- **run_status**: implemented (24/24 AC PASS)
- **ac_pass_count**: 24 (AC-001..024, all PASS — AC-018 resolved via §D.9 Phase A rename)
- **ac_fail_count**: 0
- **m1_to_mN_commit_strategy**: 7 per-milestone commits (b7ca913 M1, 9ef11e4 M2, b6d6ecb M3, c0c80b9 M4, 7f59bd9 M5-PhaseB, 69851b8 M6, f44bb47 M5-PhaseA)
- **l44_pre_commit_fetch**: origin/main = e481bd6 (in sync at AC-018 spawn)
- **l44_post_push_fetch**: origin/main = e9663b7 (post-push sync verified, divergence 0 0)
- **new_warnings_or_lints_introduced**: 0 (korean-slop-lint.sh is a NEW CI artifact, not a warning source)
- **scope_discipline**: 0 out-of-scope paths in cumulative diff (AC-023 PASS)
- **deferred**: none (AC-018 resolved 2026-07-03 via §D.9 Phase A rename, commit f44bb47)

## §E.4 Sync-phase Audit-Ready Signal (completed transition 2026-07-09)

- **sync_complete_at**: 2026-07-09
- **sync_commit_sha**: 2b0d92a (completed transition, 2026-07-09; sync artifacts af7db74, original sync 2262d9b 2026-07-03)
- **ac_pass_count**: 24/24 (AC-REM-001..024, all PASS — including AC-018 Phase A rename)
- **ac_fail_count**: 0
- **www/plugins/ re-sync residual**: RECORDED ONLY (REQ-REM-024) — `www/plugins/` marketplace copies are STALE after M1-M6 source edits (177 cowork + 11 design skills modified). Re-sync from `plugins/` → `www/plugins/` is REQUIRED before next marketplace publish. This re-sync is owned by **SPEC-MOC-SITE-IA-001** — this SPEC records the requirement only (AC-REM-024) and performs NO `www/` edits. 별도 후속 SPEC에서 re-sync 실행 필요.
- **AC-018 verification note**: AC-018 (Phase A category-prefix rename, MUST-PASS) is satisfied via the **standalone-reference interpretation** explicitly supported by acceptance.md §D.9.5. For a prefix-add rename (e.g., `blog` → `content-blog`), the raw predicate `grep "\bN\b"` cannot return 0 because the new name contains the old name as a hyphen-bounded substring. The verifier used `grep -rP "(?<![\w-])old(?![\w-])"` (standalone-occurrence grep) and confirmed **0 dangling skill references** — all residual matches are legitimate (new-name substrings, URLs like `gptfy.ai/blog/`, genre enums, cross-plugin `moai-design:` pointers, attributions). The §D.9.4 authoritative table yields 148 prefix-add + 2 body-rename + 26 no-op = 176 total; the §D.9.2 summary column showed 149 (pre-body-rename-split) — §D.9.4 was the executed source-of-truth.
- **residual risks**: (a) `www/plugins/` stale until SITE-IA re-sync (out of AC-scope); (b) `moai-core` namespace flagged by AC-015 grep (9 deprecated ns tokens) but moai-code is **exempt** from this SPEC's scope per plan.md §A.5 — namespace normalization there is a separate SPEC (SPEC-MOC-BOOTSTRAP-DESKTOP-001 owns moai-code). 3-phase close completed.

## §E.5 Mx-phase Audit-Ready Signal

_retired — Mx-phase folded into §E.4 per 3-phase close (spec-frontmatter-schema.md § progress.md Section Map); no separate Mx commit._
