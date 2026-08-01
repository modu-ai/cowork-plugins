---
id: SPEC-MOC-PLUGIN-REMEDIATION-001
title: "모두의 클로드 plugin family Korean-slop remediation (cowork + design skills) — gate structure, decontamination, execution-path repair, prefix rename, boundary dedup"
version: "0.1.0"
status: completed
created: 2026-07-02
updated: 2026-07-09
author: manager-spec
priority: P0
phase: "v0.1.0 (release-blocking)"
module: "plugins/moai-cowork/skills + plugins/moai-design/skills"
lifecycle: spec-anchored
tags: "korean, ai-slop, remediation, gate, humanize, cowork, design, plugin, release-blocking"
related_specs: [SPEC-MOC-PLUGIN-COWORK-002, SPEC-MOC-PLUGIN-DESIGN-001]
tier: L
---

# SPEC-MOC-PLUGIN-REMEDIATION-001 — 모두의 클로드 Plugin Family Korean-Slop Remediation

## HISTORY

- **2026-07-02** Initial authoring (manager-spec, plan-phase iteration 1). Evidence base: the full 3-way cross-verified Korean AI-tell ("slop") audit of all family skills (177 cowork + 11 design + code plugin), persisted in auto-memory `project_plugin_korean_slop_audit.md` (origin session `28305de2`). Every target path in this SPEC was **independently re-verified against the live `plugins/` tree at authoring time** (not trusted from the secondhand audit summary) per `.claude/rules/moai/core/verification-claim-integrity.md` §1.1 surface 3 (a defect claim is a hypothesis until the tool confirms it). Re-verification surfaced **count drift** from the audit's frozen numbers — see §A.3 — which is the direct reason every acceptance criterion in `acceptance.md` is a re-runnable **end-state predicate** (grep → 0 for defect patterns, grep → ≥1 for required additions), NOT a frozen defect count. Requirements: 24 (REQ-REM-001..024, GEARS). Tier: L (constitutional-scale — ~188 skill dirs in scope + gates + a new lint CI). RELEASE-BLOCKING.

---

## §A. Background and Purpose

### A.1 Business Context

The "모두의 클로드" (Modu-ui Claude) plugin family ships a Claude Code marketplace (`.claude-plugin/marketplace.json`, `name: moai-claude`, `v0.1.0`) with three plugins: `moai-cowork` (Korean business-domain workflow skills + smartstore MCP), `moai-design` (design-system skills + design constitution + GAN loop), and `moai-code` (workflow commands). A user-reported defect — Korean slide copy in English-advertising translationese (e.g. dash-contrast headline "복붙에서 위임으로 — 목표만 주면, 나머지는 에이전트가", particle/noun-ending fragments) — triggered a full audit. The audit found the slop is not incidental: it is produced and reinforced by four structural root causes across the family's skills. This SPEC remediates all four causes plus two enabling structural changes (prefix rename, boundary dedup). It is release-blocking because the marketplace publishes user-facing Korean copy generators, and shipping slop-producing skills degrades every downstream deliverable.

### A.2 The Four Root Causes (from the audit, condensed)

1. **Structural blind-spot in the gates.** The three review skills (`ai-slop-reviewer`, `humanize-korean`, design's `cd-slop-check`) operate at word-dictionary level. Three *structural* slop patterns are unregistered: (a) dash-contrast headline "X — Y", (b) particle/noun-ending sentence fragments (조사·체언 종결 조각문), (c) "A에서 B로" transition formula. The dash rule exists ONLY in `humanize-korean`, and is **absent from `ai-slop-reviewer`'s checklist** — yet most commerce/copy skills chain ONLY `ai-slop-reviewer`, so dash copy passes the mandatory gate. There is no "slide/copy" genre profile.
2. **Style contagion.** Guidance prose and example copy actively *teach* the dash style. Slop copy is enshrined as "good examples" across many skills. Translationese boilerplate ("협력하여 ~하는 하네스입니다") is copied across many files, and the internal term "하네스" leaks into user-facing docs.
3. **Gate execution/location defects.** `pdf-writer` and `humanize-korean` reference non-existent script paths (immediate failure). `pptx-designer` has no copy-only stage → headlines are never gated. `notebooklm-slide-prompt` gates only the prompt, while the real copy is generated downstream (outside the gate). Gate references use inconsistent/deprecated namespaces.
4. **Unwired gates.** Many Korean-copy-producing skills have no gate chain at all. Some skills use advisory ("정리하면 좋습니다") rather than mandatory tone.

Plus structural debt: deprecated 9-namespace references, a `project` router that routes to a retired 27-plugin topology, broken relative links, phantom directories, and a `design-system-library` duplicated across cowork and design.

### A.3 Current State — independently re-verified at plan-phase (do NOT trust the audit's frozen counts; re-run at run-phase)

Verified against the live tree `/Users/goos/MoAI/claude.mo.ai.kr/plugins/` on 2026-07-02:

| Item | Audit's frozen number | Re-verified live number | Predicate used | Implication |
|------|-----------------------|-------------------------|----------------|-------------|
| cowork skills | 178 | **177** (`find plugins/moai-cowork/skills -name SKILL.md \| wc -l`) | file count | Phase A rename targets the **live** count, re-measured at run-phase — NOT a frozen 178 |
| design skills | 11 | **11** (same predicate) | file count | matches |
| deprecated-namespace files | 78 | **68** (`grep -rl` of the 9 ns tokens) | content grep | predicate differs from the audit's per-ns enumeration; **run-phase re-baselines** |
| "하네스" boilerplate files | 29 files / 13 skills | **77** files match bare `하네스` (`grep -rl "하네스"`) | content grep | the audit measured the specific boilerplate *sentence*; a bare-term grep is broader — REQ-REM-011 targets the sentence pattern, re-baselined at run-phase |
| `ai-slop-reviewer` em-dash | (unstated) | **10** (`grep -c "—"`) | content grep | REQ-REM-012 baseline |
| `humanize-korean` em-dash | 43 (self-contradiction) | **41** (`grep -c "—"`) | content grep | REQ-REM-012 baseline |
| `pdf-writer` broken `moai-office/` path | 4 spots | **4** (lines 56, 59, 60, 95) | `grep -n moai-office` | confirmed |
| `humanize-korean` broken `moai-content/` path | 3 spots | **3+** (lines 73, 89, 170, refs of `moai-content/skills/humanize-korean/references/metrics.py`) | `grep -n moai-content` | confirmed |
| `live-commerce` deceptive-ad "집중력 200%" | flagged | **present** (`references/live-script.md:79`) | `grep -n` | confirmed |
| `newsletter` ★★★★ dash formula | line 35 | **present** (`SKILL.md:35` "오늘 마감 — ~ 신청 안 하셨다면") | `grep -n` | confirmed |
| `detail-page-copy` CTA "지금 바로 만나보기" | flagged | **present** (`references/13-sections.md:38`) | `grep -rn` | confirmed |
| `design-system-library` duplicate | cowork + design | **both exist** | `ls -d` | Phase B dedup target confirmed |
| existing lint/gate script | none | **none** (only doc-generation scripts + `build-moai-design.sh`) | `ls scripts/` | P4 creates a NEW lint script |

**Lesson codified into this SPEC's AC design:** because the audit's frozen counts drifted between the audit session and this plan-phase, and may drift again before run-phase, no acceptance criterion asserts a count. Every AC is a re-runnable predicate expressing the desired **end state** (defect grep → 0, required-addition grep → ≥1), and every count-sensitive milestone re-baselines at run-phase pre-flight (`plan.md` §C).

### A.4 What This SPEC Solves

The four root causes (§A.2) plus the structural debt, sequenced so that the two **release-blocking** categories land first: (M1) P0 gate structure + P2 immediate-failure path repair; then (M2) P1 decontamination, (M3) P3 gate wiring, (M4) P2 bulk execution-path repair, (M5) Phase A prefix rename + Phase B boundary dedup, (M6) P4 re-occurrence-prevention lint CI. After source edits, `www/plugins/` marketplace copies require a re-sync owned by the SITE-IA SPEC (this SPEC records the requirement, does not perform it — §E, REQ-REM-024).

---

## §B. Requirements — GEARS Format

> `<subject>` in this SPEC is **"the remediation process"** (the run-phase implementer, `manager-develop`, `cycle_type=ddd` — corrective work on an existing large content tree, not new-feature TDD), except where a more specific subject (the gate, a named skill, the lint script) is clearer. Skill file paths are relative to `plugins/`. Korean quoted strings are the actual on-disk artifact text and remain in Korean.

### Group P0 — Gate structure + genre profile + gate location (release-blocking, M1)

#### REQ-REM-001 — Structural slop patterns registered in `ai-slop-reviewer` (Ubiquitous, PRIMARY)

The `ai-slop-reviewer` checklist (`moai-cowork/skills/ai-slop-reviewer/SKILL.md`) **SHALL** register the three structural slop patterns as S1-severity checklist items: (a) dash-contrast headline (대시 대비 헤드라인 "X — Y"), (b) particle/noun-ending fragment (조사·체언 종결 조각문), (c) "A에서 B로" transition formula. This is the PRIMARY target because most commerce/copy skills chain ONLY `ai-slop-reviewer`; the re-ported detection source is `plugins/moai-code/skills/moai-domain-humanize/modules/korean.md` (D-cat "X에서 Y로", read-only reference — that tree is out of scope for edits).

#### REQ-REM-002 — Same patterns propagated to the other gates + slide QA checklists (Ubiquitous)

The remediation process **SHALL** register the same three structural patterns (REQ-REM-001) in `moai-cowork/skills/humanize-korean/SKILL.md`, in design's `moai-design/skills/cd-slop-check/SKILL.md`, and in the QA checklists of the three slide skills (`pptx-designer`, `html-slide`, `notebooklm-slide-prompt`).

#### REQ-REM-003 — Slide/copy genre profile added to `humanize-korean` (Ubiquitous)

`humanize-korean` **SHALL** define a "slide/copy genre profile" that ALLOWS complete noun-phrase titles while FORBIDDING dash-connection and particle-ending, so that legitimate slide titles are not false-flagged while the slop patterns are still caught.

#### REQ-REM-004 — `pptx-designer` copy-only gate stage (Event-driven)

**When** `pptx-designer` produces headline/body copy, the gate **SHALL** see the final copy: `moai-cowork/skills/pptx-designer/SKILL.md` **SHALL** add a copy-only stage and a mandatory gate chain to `ai-slop-reviewer`/`humanize-korean` so headlines are gated (currently there is no copy stage, so headlines are never gated).

#### REQ-REM-005 — `notebooklm-slide-prompt` embeds title rules into its template (Event-driven)

**When** `notebooklm-slide-prompt` emits its 6-block prompt template (whose downstream copy is generated OUTSIDE the family gate), the remediation process **SHALL** embed the title-writing rules (the three anti-patterns of REQ-REM-001) directly INTO the 6-block prompt template text, since a downstream generator cannot be gated by a family skill.

### Group P2-immediate — Broken execution paths (release-blocking, M1)

#### REQ-REM-006 — `pdf-writer` script path repair (Unwanted)

`moai-cowork/skills/pdf-writer/SKILL.md` **SHALL NOT** reference the non-existent `moai-office/skills/pdf-writer/...` script or asset paths (currently 4 spots: lines 56, 59, 60, 95). It **SHALL** use `${CLAUDE_PLUGIN_ROOT}`-based paths that resolve inside the installed `moai-cowork` plugin.

#### REQ-REM-007 — `humanize-korean` metrics path repair (Unwanted)

`moai-cowork/skills/humanize-korean/SKILL.md` **SHALL NOT** reference the broken `moai-content/skills/humanize-korean/references/metrics.py` path (currently at lines 73, 89, 170). It **SHALL** use `${CLAUDE_PLUGIN_ROOT}`-based paths that resolve to the skill's actual `references/` directory.

### Group P1 — Decontaminate the sources (M2)

#### REQ-REM-008 — Slide/deck genre decontamination (Ubiquitous)

The remediation process **SHALL** rewrite the slide-genre example sources so they no longer teach the dash/particle-ending style: `moai-cowork/skills/html-slide/samples/deck-sample.json` (and its `deck-sample.html`) — the direct origin of slide slop — plus the dash headings in `notebooklm-slide-prompt` and any dash-teaching prose in `html-slide/SKILL.md`.

#### REQ-REM-009 — Commerce/marketplace/detail-page copy decontamination (Ubiquitous)

The remediation process **SHALL** rewrite the enumerated commerce/copy slop examples: `commerce-promotion-planner` ("good pattern" table), `commerce-repurchase-timer`, `commerce-product-naming`, `commerce-channel-message`, `marketplace-curation`, `detail-page-copy` (headline formulas + the CTA "지금 바로 만나보기" at `references/13-sections.md:38`), and the `newsletter` ★★★★ formula "오늘 마감 — ~ 신청 안 하셨다면" (`SKILL.md:35`), so none present dash-contrast/particle-ending copy as exemplary.

#### REQ-REM-010 — Remaining sample decontamination + deceptive-ad removal (Ubiquitous)

The remediation process **SHALL** rewrite the remaining slop sources: `live-commerce` (spoken-script dash + remove the deceptive-ad exaggeration "집중력 200%" at `references/live-script.md:79`, a deceptive-advertising risk), `executive-summary`, `pm-weekly-report`, `html-report`, `design-system-library` samples, `interview-coach`'s answer formula, and `ai-slop-reviewer`'s own model-answer dash (a gate that models slop is self-defeating).

#### REQ-REM-011 — Boilerplate naturalization + internal-term removal (Ubiquitous)

The remediation process **SHALL** naturalize the translationese boilerplate sentence pattern "협력하여 …하는 하네스입니다" across the affected skills, and **SHALL** remove the internal term "하네스" from user-facing skill documentation (replacing it with a user-facing term). The exact file set is re-baselined at run-phase (`plan.md` §C) since the live count differs from the audit's.

#### REQ-REM-012 — Em-dash density reduction in guidance prose (Ubiquitous)

The remediation process **SHALL** reduce em-dash density in guidance prose, starting with the two gate skills. Post-edit em-dash count in `ai-slop-reviewer/SKILL.md` and `humanize-korean/SKILL.md` **SHALL** be strictly below the plan-phase baselines (ai-slop-reviewer 10, humanize-korean 41). Em-dashes that appear inside a *dash-rule negative example* (the gate legitimately quoting a bad pattern) are exempt and MUST NOT be counted against the reduction — the AC records this exemption.

### Group P3 — Complete gate wiring (M3)

#### REQ-REM-013 — Wire unwired Korean-copy skills to a gate chain (Ubiquitous)

Every Korean-copy-producing skill currently lacking a gate chain **SHALL** declare a mandatory gate chain (to `humanize-korean` and/or `ai-slop-reviewer`), prioritizing consumer-facing copy: the marketplace 5종 first, then `live-commerce`, `landing-page`, `hwpx-writer`, `learning-material`, `detail-page-planner`, `job-analyzer`, `data-visualizer`, then `ai-diagnostic`, `assessment-creator`, `conflict-handler`, `curriculum-designer`, then `interactive`. The full set is re-baselined at run-phase.

#### REQ-REM-014 — Wire `moai-workflow-design` + standardize advisory→required (Ubiquitous)

The remediation process **SHALL** wire `moai-workflow-design` into the main line, and **SHALL** standardize advisory phrasing ("정리하면 좋습니다") to mandatory phrasing ("필수(required)") wherever a gate is intended to be enforced rather than suggested.

### Group P2-bulk — Repair broken execution paths (M4)

#### REQ-REM-015 — Deprecated-namespace normalization (Unwanted)

No skill under `moai-cowork/skills` or `moai-design/skills` **SHALL** reference a deprecated namespace (`moai-office`, `moai-content`, `moai-media`, `moai-finance`, `moai-book`, `moai-business`, `moai-marketing`, `moai-education`, `moai-legal`). All such references **SHALL** be normalized to the `moai-cowork:` prefix (or the correct in-plugin relative path).

#### REQ-REM-016 — `project` router rewrite for single-plugin architecture (Event-driven)

**When** the `project` skill (`moai-cowork/skills/project/SKILL.md`) routes to a target skill, it **SHALL** route within the single consolidated `moai-cowork` architecture and **SHALL NOT** route to the retired 27-plugin topology (currently ~49 routing references to the deprecated multi-plugin layout).

#### REQ-REM-017 — Broken links / phantom dirs / stale dependencies repair (Ubiquitous)

The remediation process **SHALL** repair: broken relative links in `codex-image` and `data-visualizer`; phantom directories (e.g. an empty `moai-content/skills/html-slide/` ghost dir under `design-system-library`); `html-slide`'s dependency on an undeployed `CLAUDE.local.md §3-2`; and the `.mcp.json` reference to a missing `CONNECTORS.md`. Each broken reference **SHALL** be replaced with an in-skill rule or a correct path.

### Group A — 178→177-skill category-prefix rename (M5, user-approved)

#### REQ-REM-018 — Category-prefix rename with reference integrity (Event-driven)

**When** category prefixes (`commerce-`, `legal-`, `content-`, `finance-`, `education-`, `media-`, …) are applied across the live cowork skill set, the remediation process **SHALL** perform the rename via a script and **SHALL** verify — by full-tree grep — that no dangling reference to any old skill name survives (in SKILL.md bodies, `marketplace.json`, `llms.txt`, gate chains, or the `project` router). The rename operates on the run-phase re-measured live skill count, not a frozen number. The per-skill old→new mapping lives in `acceptance.md` §D.9 (Phase A Rename Mapping) — that table is the authoritative rename source; the run-phase script reads §D.9 to determine the rename set, and AC-REM-018's grep predicate runs over every old-name listed there.

### Group B — Boundary contract + dedup (M5, 3-plugin separation upheld)

#### REQ-REM-019 — `design-system-library` dedup (Ubiquitous)

`design-system-library` **SHALL** be canonical in `moai-design`; the `moai-cowork` duplicate **SHALL** be removed and replaced with a pointer to the design plugin's canonical skill, upholding the boundary contract "산출물=cowork, 체계=design" (deliverables=cowork, systems=design).

#### REQ-REM-020 — `brand-identity` scope narrowing (Ubiquitous)

`moai-cowork/skills/brand-identity` scope **SHALL** be narrowed to "personal-branding deliverable"; system-building responsibility **SHALL** point to design's `moai-design/skills/moai-domain-brand-design`, per the boundary contract.

### Group P4 — Re-occurrence prevention (M6)

#### REQ-REM-021 — skill-builder/skill-template authoring rules (Ubiquitous)

`moai-cowork/skills/skill-builder` (and any skill-template it references) **SHALL** include Korean example-copy authoring rules — the three anti-patterns of REQ-REM-001 — so that new skills cannot be created with contaminated example copy at the source.

#### REQ-REM-022 — Lint CI script before market sync (Event-driven, capability gate)

**Where** a market re-sync (`www/plugins/` copy) is about to run, a lint script under `plugins/moai-cowork/scripts/` (and/or `plugins/moai-design/scripts/`) **SHALL** run as a CI gate BEFORE the sync, checking: dash density, cliché phrases, deprecated namespaces, and the boilerplate sentence shape. The script **SHALL** exit non-zero when any registered pattern is found.

### Cross-cutting scope discipline

#### REQ-REM-023 — Scope discipline (Unwanted)

The remediation process **SHALL NOT** modify any file outside the owned trees: `plugins/moai-cowork/skills/**`, `plugins/moai-design/skills/**`, `plugins/moai-cowork/scripts/**`, `plugins/moai-design/scripts/**`, and the skill-builder/skill-template files. It **SHALL NOT** touch `plugins/moai-code/**`, `plugins/moai-cowork/commands/**`, `internal/template/templates/**` (owned by SPEC-MOC-BOOTSTRAP-DESKTOP-001), or `www/**` (owned by SPEC-MOC-SITE-IA-001).

#### REQ-REM-024 — Market re-sync requirement recorded, not performed (Ubiquitous)

The remediation process **SHALL** record — in the completion report and `progress.md` — that `www/plugins/` marketplace copies require a re-sync after these source edits, cross-referencing the SITE-IA SPEC. It **SHALL NOT** itself edit any file under `www/`.

---

## §C. Constraints

### C.1 Technical Constraints

- All edits confined to the owned trees (REQ-REM-023). The marketplace manifest `.claude-plugin/marketplace.json` MAY be updated ONLY as required by the Phase A rename (REQ-REM-018) to keep skill references consistent — no other manifest change.
- Path repairs (REQ-REM-006/007/017) MUST use `${CLAUDE_PLUGIN_ROOT}` (the Claude Code plugin-root variable) so paths resolve inside the installed plugin, not a build-time absolute path.
- Decontamination (P1) rewrites EXAMPLE copy and GUIDANCE prose only — it MUST NOT change a skill's functional contract (its trigger keywords, its I/O, its workflow steps) beyond adding/adjusting gate-chain references (P3) and genre rules (P0).
- The re-ported detection source `plugins/moai-code/skills/moai-domain-humanize/modules/korean.md` is READ-ONLY (out-of-scope tree); its patterns are copied INTO the owned gate skills, the source file is not edited.

### C.2 Sequencing Constraints (dependency order)

- M1 (P0 gate structure + P2 immediate-failures) is release-blocking and runs FIRST.
- P2 bulk namespace normalization (M4, REQ-REM-015) runs BEFORE the Phase A prefix rename (M5, REQ-REM-018) so the rename operates on already-corrected namespace references (avoids double-touch and rename-of-broken-ref).
- Phase A rename (M5) runs AFTER content edits (M2/M3/M4) settle, to avoid editing a file and then renaming its directory in separate passes.
- P4 lint CI (M6) runs LAST against the final tree, so its patterns match final skill names.
- `www/plugins/` re-sync is downstream of this entire SPEC and owned by SITE-IA (REQ-REM-024).

### C.3 Verification Constraint (verification-claim-integrity)

Per `.claude/rules/moai/core/verification-claim-integrity.md`, every acceptance criterion in `acceptance.md` is a mechanically-runnable predicate (grep/lint command + expected output). No AC asserts a defect exists by text alone; run-phase re-baselines all count-sensitive figures before acting (a defect claim is a hypothesis until the tool confirms it).

---

## §D. Quality Attributes

| Attribute | Target | Verification |
|-----------|--------|--------------|
| Gate completeness | 3 structural patterns registered in all 3 gates + 3 slide QA checklists | pattern-descriptor grep per gate (AC-REM-001/002) |
| Path integrity | 0 references to non-existent script paths | `grep -c` broken-path predicates → 0 (AC-REM-006/007/015/017) |
| Decontamination | 0 dash-contrast/particle-ending example copy in enumerated sources; 0 "집중력 200%" | per-file defect grep → 0 (AC-REM-008/009/010) |
| Gate wiring | Priority copy skills all carry a gate chain | gate-chain grep per skill (AC-REM-013) |
| Rename integrity | 0 dangling references to old skill names | full-tree grep → 0 (AC-REM-018) |
| Boundary dedup | cowork `design-system-library` = pointer only; `brand-identity` scoped | pointer grep + scope grep (AC-REM-019/020) |
| Re-occurrence prevention | lint script exists, executable, detects all 4 pattern classes | lint self-test exit codes (AC-REM-022) |
| Scope discipline | 0 files modified outside owned trees | `git diff --stat` path check (AC-REM-023) |

---

## §E. Out of Scope

### Out of Scope — moai-code, commands, and template trees

`plugins/moai-code/**`, `plugins/moai-cowork/commands/**`, and `internal/template/templates/**` are owned by **SPEC-MOC-BOOTSTRAP-DESKTOP-001** and are NOT edited by this SPEC. The `moai-domain-humanize` skill under `plugins/moai-code/` is referenced READ-ONLY as the re-port source for the detection patterns (REQ-REM-001); it is not modified.

### Out of Scope — www docs-site synchronization

`www/**` (the Hugo docs site + `www/plugins/` marketplace copies) is owned by **SPEC-MOC-SITE-IA-001**. This SPEC records that a re-sync is required after its source edits (REQ-REM-024) but performs no `www/` edit. The market copies drift until SITE-IA re-syncs.

### Out of Scope — smartstore MCP

The `moai-smartstore` MCP server (`plugins/moai-cowork/mcp-servers/`) was vendored/corrected by a parallel session and is not part of this remediation.

### Out of Scope — English/Japanese/Chinese slop

This SPEC remediates Korean AI-tell only. The `moai-domain-humanize` classifier's `english.md`/`japanese.md`/`chinese.md` locales are not in scope; non-Korean copy quality is deferred.

### Out of Scope — skill functional redesign

Decontamination rewrites example copy and guidance prose and adds gate wiring; it does NOT redesign any skill's functional contract, trigger keywords, or workflow logic. A skill whose *only* defect is stylistic is corrected in place, not re-architected.

### Out of Scope — new domain skills

No new business-domain skills are authored. The Phase A rename re-labels existing skills; it does not add or remove skills (beyond the single `design-system-library` dedup removal in Phase B, REQ-REM-019).

---

## §F. Interfaces and Assets

### F.1 Owned trees (editable)

| Tree | Role |
|------|------|
| `plugins/moai-cowork/skills/**` | cowork skills — gates, copy sources, router, rename targets |
| `plugins/moai-design/skills/**` | design skills — `cd-slop-check`, `design-system-library` canonical, `moai-domain-brand-design` |
| `plugins/moai-cowork/scripts/**` | new lint script location (P4) |
| `plugins/moai-design/scripts/**` | design lint hook location (P4) |
| `plugins/moai-cowork/skills/skill-builder/**` | re-occurrence-prevention authoring rules (P4) |

### F.2 Read-only references (not edited)

| Asset | Role |
|-------|------|
| `plugins/moai-code/skills/moai-domain-humanize/modules/korean.md` | re-port source for the 3 structural patterns (D-cat "X에서 Y로") |
| `plugins/moai-cowork/skills/card-news/**` | reference model — chains `humanize-korean` + own `references/anti-ai-writing.md` |
| `plugins/moai-cowork/skills/campaign-planner/**` | reference model — post-processes prose only, excludes numbers/tables |

### F.3 Manifest touched only for rename consistency

| Asset | Operation |
|-------|-----------|
| `.claude-plugin/marketplace.json` | updated ONLY to keep skill references consistent with the Phase A rename (REQ-REM-018) |
| `plugins/moai-cowork/llms.txt` | updated ONLY for rename consistency |

---

## §G. Verification Summary

Detailed acceptance criteria live in `acceptance.md`. Core dimensions:

1. **Gate structure**: 3 structural patterns present in `ai-slop-reviewer` + `humanize-korean` + `cd-slop-check` + 3 slide QA checklists; slide/copy genre profile present; `pptx-designer` copy stage + chain present; `notebooklm` template embeds title rules.
2. **Path integrity**: broken `moai-office/` and `moai-content/` paths → 0; `${CLAUDE_PLUGIN_ROOT}` present.
3. **Decontamination**: enumerated slop examples rewritten (defect grep → 0); "집중력 200%" → 0; boilerplate sentence → 0; gate-skill em-dash below baseline.
4. **Gate wiring**: priority copy skills carry a gate chain; `moai-workflow-design` wired; advisory→required.
5. **Bulk repair**: deprecated-namespace grep → 0; `project` router single-plugin; broken links/phantom dirs → 0.
6. **Rename + boundary**: 0 dangling old-name references; cowork `design-system-library` = pointer; `brand-identity` scoped.
7. **P4**: skill-builder rules present; lint script exists + detects all 4 pattern classes.
8. **Scope discipline**: 0 out-of-scope file modifications; www re-sync requirement recorded.

---

## §H. Cross-References

- **Evidence base**: auto-memory `project_plugin_korean_slop_audit.md` (origin session `28305de2`) — the 3-way cross-verified audit this SPEC remediates.
- **Sibling SPECs (scope boundaries)**: `SPEC-MOC-BOOTSTRAP-DESKTOP-001` (moai-code/commands/templates), `SPEC-MOC-SITE-IA-001` (www + market re-sync).
- **Family SPECs**: `SPEC-MOC-PLUGIN-COWORK-002` (single-plugin migration), `SPEC-MOC-PLUGIN-DESIGN-001`.
- `.claude/rules/moai/core/verification-claim-integrity.md` — the no-unobserved-defect-claim invariant that shaped the re-runnable-predicate AC design.
- `.claude/rules/moai/development/spec-frontmatter-schema.md` § Status Transition Ownership Matrix.
- GEARS notation guide: `.claude/skills/moai-workflow-spec/SKILL.md` § GEARS Format.
- Reference models: `card-news` (gate chain + `anti-ai-writing.md`), `campaign-planner` (prose-only post-processing).
