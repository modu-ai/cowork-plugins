# SPEC-MOC-PLUGIN-REMEDIATION-001 — Implementation Plan

---
id: SPEC-MOC-PLUGIN-REMEDIATION-001
status: implemented
updated: 2026-07-03
---

## HISTORY

- **2026-07-02** Initial authoring (manager-spec, plan-phase iteration 1). Milestones M1-M6 sequenced by dependency (release-blocking first; namespace-normalize before rename; rename before lint CI). Tier L.

## §A. Context

- **Working directory**: `/Users/goos/MoAI/claude.mo.ai.kr` (this meta-repo; the `plugins/` marketplace lives here, NOT a separate repo — unlike the retired cowork-plugins/ repo).
- **Branch**: `main` (Hybrid Trunk, 1-person OSS). Confirm HEAD at run-phase pre-flight.
- **SPEC artifacts**: `.moai/specs/SPEC-MOC-PLUGIN-REMEDIATION-001/{spec,plan,acceptance,progress}.md`.
- **Tier classification**: **L (Large / constitutional-scale)**. Rationale: scope spans ~177 cowork + 11 design skills, all 3 gate skills, the `project` router (~49 refs), a family-wide deprecated-namespace sweep, a 177-skill directory rename, a boundary dedup, and a NEW lint CI script. Review surface > 15 files by a wide margin. Per `.claude/rules/moai/workflow/spec-workflow.md` § SPEC Complexity Tier, Tier L PASS threshold = 0.85. NOTE: the task scoped deliverables to the 3-file core (spec/plan/acceptance) + the mandatory `progress.md` §E skeleton; the conventional Tier-L `design.md`/`research.md` are folded — `research.md` is effectively the audit auto-memory (`project_plugin_korean_slop_audit.md`) plus the plan-phase live re-verification recorded in `spec.md` §A.3, and design decisions live in §A.2 (root causes) + this plan's §F sequencing. If the orchestrator/plan-auditor requires the full 5-artifact Tier-L set, that is a bounded follow-up (extract §A.3 into research.md, §A.2 + §F into design.md).
- **Evidence base**: audit auto-memory `project_plugin_korean_slop_audit.md` + plan-phase live re-verification (`spec.md` §A.3). **Counts drifted between audit and plan-phase — re-baseline again at run-phase.**
- **cycle_type**: `ddd` (corrective work on a large existing content tree; ANALYZE the current gate/copy state, PRESERVE functional contracts, IMPROVE style + wiring).
- **PRESERVE**: every skill's functional contract (trigger keywords, I/O, workflow steps); the read-only re-port source `moai-code/.../korean.md`; all out-of-scope trees (moai-code, commands, templates, www).
- **EXTEND**: the 3 gate skills (+ patterns/genre), copy sources (decontamination), unwired skills (gate chains), the `project` router, skill-builder (authoring rules), scripts/ (new lint CI).

## §B. Known Issues (Tier-L relevant categories)

**B4. Frontmatter Canonical Schema** — this SPEC's `spec.md` uses all 12 canonical fields with `created:`/`updated:`/`tags:` (never snake_case aliases); `id` matches `^SPEC(-[A-Z][A-Z0-9]*)+-\d{3}$` (self-checked at authoring: SPEC | MOC | PLUGIN | REMEDIATION | 001 → PASS).

**B6. spec-lint Heading Convention** — `spec.md` §E uses `### Out of Scope — <topic>` H3 sub-headings with `-` bullets (6 of them), satisfying `OutOfScopeRule`/`MissingExclusions`.

**B8. Working Tree Hygiene** — the run-phase implementer MUST NOT touch runtime-managed files or any out-of-scope tree (REQ-REM-023). Use path-scoped `git add` (never `git add -A` from repo root — that would stage unrelated working-tree changes; note `git status` at session start shows many untracked top-level dirs).

**B9. Git Commit + Push (Hybrid Trunk Tier L)** — Tier L MAY route through a PR (per Tier-based PR routing) OR direct-to-main per this project's 1-person-OSS convention. Commit per-milestone with Conventional Commits subjects referencing this SPEC ID. Confirm push disposition with the orchestrator (Tier L is the PR-routing tier).

**B10. Untouched Paths PRESERVE** — parallel sessions may be active in this repo. Before spawning the write agent, the orchestrator runs the Pre-Spawn Sync Check (`agent-common-protocol.md`). Do not touch other SPEC dirs or the sibling-SPEC trees.

**B11. AskUserQuestion Prohibition** — if run-phase re-baselining finds the tree materially different from `spec.md` §A.3 (e.g. skill count changed, a target file moved), return a structured blocker report; never prompt the user directly.

## §C. Pre-flight Checklist (run-phase implementer re-baselines before ANY edit)

```bash
cd /Users/goos/MoAI/claude.mo.ai.kr

# 1. Branch + baseline
git branch --show-current                 # expect: main
git rev-parse HEAD

# 2. RE-BASELINE the drift-prone counts (spec.md §A.3 numbers are plan-phase, may have moved)
find plugins/moai-cowork/skills -name SKILL.md | wc -l        # cowork skill count (plan-phase: 177)
find plugins/moai-design/skills  -name SKILL.md | wc -l       # design skill count (plan-phase: 11)
grep -rl "moai-office\|moai-content\|moai-media\|moai-finance\|moai-book\|moai-business\|moai-marketing\|moai-education\|moai-legal" plugins/moai-cowork/skills plugins/moai-design/skills | wc -l   # deprecated-ns files (plan-phase: 68)
grep -rl "협력하여.*하네스입니다\|하는 하네스입니다" plugins/moai-cowork/skills plugins/moai-design/skills | wc -l   # boilerplate sentence files
grep -c "—" plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md   # em-dash baseline (plan-phase: 10)
grep -c "—" plugins/moai-cowork/skills/humanize-korean/SKILL.md    # em-dash baseline (plan-phase: 41)

# 3. Confirm P0/P2-immediate target paths still present
grep -n "moai-office" plugins/moai-cowork/skills/pdf-writer/SKILL.md          # expect: lines 56,59,60,95 (or moved)
grep -n "moai-content/skills/humanize-korean" plugins/moai-cowork/skills/humanize-korean/SKILL.md   # expect: 73,89,170
grep -rn "집중력 200" plugins/moai-cowork/skills/live-commerce/                # expect: references/live-script.md:79
grep -n "오늘 마감" plugins/moai-cowork/skills/newsletter/SKILL.md             # expect: line 35

# 4. Confirm Phase B dedup + reference models
ls -d plugins/moai-cowork/skills/design-system-library plugins/moai-design/skills/design-system-library   # both exist
ls plugins/moai-cowork/skills/card-news/references plugins/moai-cowork/skills/campaign-planner            # reference models

# 5. Confirm out-of-scope trees exist (to avoid touching): read-only source
ls plugins/moai-code/skills/moai-domain-humanize/modules/korean.md            # read-only re-port source
```

If any step-2 count differs materially from `spec.md` §A.3, record the new baseline in `progress.md` §E.2 and proceed against the LIVE numbers (do NOT act on stale plan-phase counts). If a step-3 target path has moved, re-locate via grep before editing.

## §D. Constraints (DO NOT VIOLATE)

- **Owned trees only** (REQ-REM-023): `plugins/moai-cowork/skills/**`, `plugins/moai-design/skills/**`, `plugins/moai-cowork/scripts/**`, `plugins/moai-design/scripts/**`. Manifest (`marketplace.json`, `llms.txt`) touched ONLY for Phase A rename consistency.
- **Never touch**: `plugins/moai-code/**`, `plugins/moai-cowork/commands/**`, `internal/template/templates/**`, `www/**`.
- **Read-only**: `plugins/moai-code/skills/moai-domain-humanize/modules/korean.md` (re-port source).
- **Preserve functional contracts**: decontamination changes copy/prose + gate wiring only; no trigger-keyword or workflow-logic redesign.
- **Path repairs use `${CLAUDE_PLUGIN_ROOT}`** (not build-time absolute paths).
- **Staging**: path-scoped `git add <owned-path>` only; never `git add -A` / `git add .` from repo root.
- **Forbidden commands**: `--no-verify`, `--amend`, force-push.
- **No AskUserQuestion**: ambiguity → structured blocker report.

## §E. Self-Verification Deliverables (required in the completion report)

**E1. AC Binary PASS/FAIL Matrix** — all 24 ACs (AC-REM-001..024) from `acceptance.md` §D, with command output per row.

**E2. Broken-path grep (release-blocking)**
```
$ grep -c "moai-office" plugins/moai-cowork/skills/pdf-writer/SKILL.md          → 0
$ grep -c "moai-content/skills/humanize-korean" plugins/moai-cowork/skills/humanize-korean/SKILL.md → 0
$ grep -rc "CLAUDE_PLUGIN_ROOT" plugins/moai-cowork/skills/pdf-writer/SKILL.md plugins/moai-cowork/skills/humanize-korean/SKILL.md → ≥1 each
```

**E3. Deprecated-namespace sweep**
```
$ grep -rl "moai-office\|moai-content\|moai-media\|moai-finance\|moai-book\|moai-business\|moai-marketing\|moai-education\|moai-legal" plugins/moai-cowork/skills plugins/moai-design/skills → (empty)
```

**E4. Rename integrity (Phase A)**
```
$ # for every renamed skill old-name, grep the whole owned tree + manifest → 0 dangling
```

**E5. Gate-structure presence**
```
$ grep -c "대시\|조사·체언\|에서.*로" plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md → ≥3 pattern descriptors
```

**E6. Scope-discipline diff review**
```
$ git diff --stat  → every path under plugins/moai-cowork/{skills,scripts} or plugins/moai-design/{skills,scripts} + (rename-only) manifest; ZERO paths under plugins/moai-code, commands, templates, www
```

**E7. Blocker report** — if run-phase re-baselining disagrees with `spec.md` §A.3, or any target file is missing/moved beyond grep re-location, report as a structured blocker.

## §F. Milestones (priority-based, no time estimates)

1. **M1 — P0 gate structure + P2 immediate-failures (RELEASE-BLOCKING).** Register the 3 structural patterns in `ai-slop-reviewer` (PRIMARY), `humanize-korean`, `cd-slop-check`, + 3 slide QA checklists (REQ-REM-001/002). Add slide/copy genre profile to `humanize-korean` (003). Add `pptx-designer` copy stage + chain (004); embed title rules in `notebooklm` template (005). Repair `pdf-writer` (006) + `humanize-korean` metrics (007) broken paths to `${CLAUDE_PLUGIN_ROOT}`.
2. **M2 — P1 decontamination.** Rewrite slide/deck sources (008), commerce/marketplace/detail-page/newsletter copy (009), remaining samples + remove "집중력 200%" deceptive-ad (010). Naturalize boilerplate + remove "하네스" from user-facing docs (011). Reduce gate-skill em-dash below baseline (012).
3. **M3 — P3 gate wiring.** Wire unwired copy skills to a gate chain, marketplace 5종 first (013). Wire `moai-workflow-design`; standardize advisory→required (014).
4. **M4 — P2 bulk execution-path repair.** Normalize deprecated namespaces to `moai-cowork:` (015). Rewrite `project` router for single-plugin architecture (016). Repair broken links, phantom dirs, stale `CLAUDE.local.md`/`CONNECTORS.md` refs (017). *(Runs before M5 rename so the rename operates on corrected refs.)*
5. **M5 — Phase A rename + Phase B boundary dedup.** Script-based category-prefix rename of the live cowork skill set + full-tree grep verifying 0 dangling refs (018). Dedup `design-system-library` (cowork → pointer, design canonical) (019). Narrow `brand-identity` scope + pointer to `moai-domain-brand-design` (020).
6. **M6 — P4 re-occurrence prevention + re-sync note.** Add Korean example-copy rules to skill-builder/skill-template (021). Author the lint CI script (dash/cliché/old-ns/boilerplate) that exits non-zero on any pattern, wired before market sync (022). Record the `www/plugins/` re-sync requirement cross-referencing SITE-IA (024). Verify scope discipline across the whole SPEC (023).

## §G. Anti-Patterns (do not repeat)

- Acting on `spec.md` §A.3's plan-phase counts without re-baselining at run-phase (§C step 2) — the counts already drifted once (audit → plan-phase); they may drift again.
- Running `git add -A` / `git add .` from repo root — the working tree has many untracked top-level dirs; use path-scoped adds only (B8).
- Renaming skill directories (M5) BEFORE normalizing deprecated namespaces (M4) — would rename references that are themselves broken, compounding the fix.
- Editing the read-only re-port source `moai-code/.../korean.md` instead of copying its patterns INTO the owned gate skills.
- "Fixing" slop by deleting example copy rather than rewriting it — the skills need *good* examples; empty examples regress the teaching value.
- Counting a dash inside a gate's negative-example block against the em-dash reduction (REQ-REM-012) — those dashes are intentional (the gate quotes the bad pattern).
- Touching `www/**` to "also fix the market copy" — that is SITE-IA's scope (REQ-REM-024); this SPEC only records the requirement.
- Redesigning a skill's trigger keywords/workflow while decontaminating its copy — scope is copy + gate wiring, not functional redesign.

## §H. Cross-References

- `spec.md` (§B REQ-REM-001..024 requirements, §A.3 plan-phase re-verification table)
- `acceptance.md` (AC-REM-001..024 matrix)
- `progress.md` (§E.1 plan-phase signal; §E.2-§E.5 placeholders)
- audit auto-memory `project_plugin_korean_slop_audit.md`
- Sibling SPECs: `SPEC-MOC-BOOTSTRAP-DESKTOP-001`, `SPEC-MOC-SITE-IA-001`
- `.claude/rules/moai/development/manager-develop-prompt-template.md` — Tier L delegation template (this plan supplies Sections A-E)
- `.claude/rules/moai/core/verification-claim-integrity.md` — re-runnable-predicate AC design rationale
