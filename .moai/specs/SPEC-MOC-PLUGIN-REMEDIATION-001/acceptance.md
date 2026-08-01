# SPEC-MOC-PLUGIN-REMEDIATION-001 — Acceptance Criteria

---
id: SPEC-MOC-PLUGIN-REMEDIATION-001
status: implemented
updated: 2026-07-03
---

> **Verification-integrity contract.** Every AC below is a re-runnable predicate (command + expected output), executed from repo root `/Users/goos/MoAI/claude.mo.ai.kr`. No AC asserts a defect count. Defect predicates expect `0` (the desired end state); required-addition predicates expect `≥1`. All count-sensitive figures are re-baselined at run-phase pre-flight (`plan.md` §C) — a defect claim is a hypothesis until the tool confirms it (`.claude/rules/moai/core/verification-claim-integrity.md`).

## §A. Given-When-Then Scenarios

### Scenario 1 — Dash-contrast headline is caught by the mandatory gate

- **Given** most commerce/copy skills chain ONLY `ai-slop-reviewer`, whose checklist has no dash-contrast rule, so a headline like "복붙에서 위임으로 — 목표만 주면" passes the gate
- **When** the remediation registers the 3 structural patterns as S1 items in `ai-slop-reviewer` (REQ-REM-001)
- **Then** `ai-slop-reviewer/SKILL.md` contains all three pattern descriptors (대시 대비 헤드라인, 조사·체언 종결, "에서 … 로" 공식), so dash copy is now flagged by the mandatory gate

### Scenario 2 — A broken script path no longer fails immediately

- **Given** `pdf-writer/SKILL.md` calls `moai-office/skills/pdf-writer/scripts/render_pdf.py`, a path that does not exist in the installed plugin
- **When** the remediation repairs the path to `${CLAUDE_PLUGIN_ROOT}`-based (REQ-REM-006)
- **Then** `grep -c "moai-office" pdf-writer/SKILL.md` returns `0` and `grep -c "CLAUDE_PLUGIN_ROOT" pdf-writer/SKILL.md` returns `≥1`

### Scenario 3 — A slop example is decontaminated at its origin

- **Given** `html-slide/samples/deck-sample.json` is the direct origin of slide slop (its sample copy uses dash-contrast + trailing dash)
- **When** the remediation rewrites the sample (REQ-REM-008) and removes the deceptive-ad "집중력 200%" from `live-commerce` (REQ-REM-010)
- **Then** the dash-contrast pattern is absent from the rewritten sample and `grep -rc "집중력 200" live-commerce/` returns `0`

### Scenario 4 — A category-prefix rename leaves no dangling reference

- **Given** the live cowork skill set is renamed with category prefixes (REQ-REM-018)
- **When** the rename script runs and the full-tree grep verification executes
- **Then** for every renamed skill, a grep of the owned trees + `marketplace.json` + `llms.txt` for the OLD name returns `0` (no dangling reference)

### Scenario 5 — Scope discipline holds

- **Given** the remediation edits only the owned trees
- **When** `git diff --stat` is inspected after all milestones
- **Then** zero modified paths fall under `plugins/moai-code/`, `plugins/moai-cowork/commands/`, `internal/template/templates/`, or `www/`

## §B. Edge Cases

- **EC-1 — Run-phase count drift**: if `plan.md` §C re-baselining finds a different skill count / deprecated-ns file count / boilerplate file count than `spec.md` §A.3, the implementer records the LIVE baseline in `progress.md` §E.2 and proceeds against it — it does NOT act on the stale plan-phase number (this already happened once, audit → plan-phase).
- **EC-2 — Target file moved**: if a P0/P2-immediate target (e.g. `pdf-writer` line 56) has shifted, the implementer re-locates via grep before editing; a moved-but-present target is not a blocker.
- **EC-3 — Gate negative-example dash**: em-dash reduction (REQ-REM-012) MUST NOT count dashes inside a dash-rule *negative example* block (the gate legitimately quotes the bad pattern). The AC measures total em-dash minus quoted-example dashes; if the implementer cannot cleanly separate them, it reports the residual and the count is judged against guidance-prose dashes only.
- **EC-4 — Namespace normalize vs rename ordering**: if M5 rename is attempted before M4 namespace normalization, references would be renamed while still broken. The implementer MUST complete M4 (REQ-REM-015) before M5 (REQ-REM-018).
- **EC-5 — Parallel session in this repo**: per the Pre-Spawn Sync Check, the orchestrator fetches `origin/main` and queries active sessions before spawning the write agent; a concurrent session on the same trees is surfaced and resolved before edits begin.
- **EC-6 — Decontamination emptying examples**: rewriting a slop example MUST replace it with a *good* example, not delete it. An AC that finds the defect pattern absent AND the example section still non-empty passes; an emptied example section fails (regresses teaching value).
- **EC-7 — Shared-file boundary (`project/SKILL.md`)**: `plugins/moai-cowork/skills/project/SKILL.md` is a **shared file** touched by two SPECs. This SPEC (REMEDIATION-001) owns ONLY the **BODY-content remediation** — the deprecated 27-plugin routing topology → single consolidated `moai-cowork` architecture (REQ-REM-016 / AC-REM-016). **SPEC-MOC-BOOTSTRAP-DESKTOP-001** owns the **ENTRY behavior** — the `/project init` command, bare-`/project` initialization, and the resume aliases (verified on HEAD at lines 11, 43, 55-56, 99, 104, 111, 115). AC-REM-016's predicate targets ONLY routing-topology tokens (`moai-office:`, `moai-content:`, `moai-media:`, `27`/`29개 플러그인`, `distributed` — the "27개 moai 플러그인" routing body at HEAD lines 5, 16, 36, 66, 93) and MUST NOT claim, edit, or assert PASS/FAIL over BOOTSTRAP's `/project init` entry lines. If run-phase finds the routing body and the entry lines interleaved, the implementer edits ONLY the routing lines and returns the entry lines untouched.

## §C. Quality Gate Criteria

- All MUST-PASS ACs (§D.1) PASS with command-output evidence.
- Release-blocking group (M1: AC-REM-001..007) all PASS before any release consideration.
- Deprecated-namespace sweep (AC-REM-015) → 0 across both owned skill trees.
- Rename integrity (AC-REM-018) → 0 dangling old-name references.
- Scope discipline (AC-REM-023) → 0 out-of-scope modifications.
- Lint CI script (AC-REM-022) exists, is executable, and exits non-zero on each of the 4 registered pattern classes (self-test).

## §D. AC Matrix

Each row's **GEARS Statement** restates its paired REQ; the **Verification Command** + **Expected Result** are the mechanical predicate. Commands run from repo root.

| AC ID | GEARS Statement | REQ | Verification Command | Expected Result |
|-------|-----------------|-----|----------------------|-----------------|
| AC-REM-001 | The `ai-slop-reviewer` checklist **SHALL** register the 3 structural patterns as S1 items. | 001 | `grep -c "대시" plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md; grep -c "조사·체언\|체언 종결\|조사 종결" plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md; grep -c "전환 공식" plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md` | each `≥1` — HEAD pre-state **0 / 0 / 0**. Sub-predicate (c) hardened iter-3: old `에서.*로`=**6** self-passed (natural Korean postposition co-occurrence, MUST-PASS clause was vacuous); `전환 공식` is the HEAD-absent descriptor literal for the "A에서 B로" pattern (§D.8.10) |
| AC-REM-002 | The remediation process **SHALL** register the same 3 patterns in `humanize-korean`, `cd-slop-check`, and the 3 slide QA checklists. | 002 | `for f in plugins/moai-cowork/skills/humanize-korean/SKILL.md plugins/moai-design/skills/cd-slop-check/SKILL.md plugins/moai-cowork/skills/pptx-designer/SKILL.md plugins/moai-cowork/skills/html-slide/SKILL.md plugins/moai-cowork/skills/notebooklm-slide-prompt/SKILL.md; do echo "$f"; grep -c "대시" "$f"; grep -c "조사·체언\|체언 종결\|조사 종결" "$f"; grep -c "전환 공식" "$f"; done` | per file **all 3** patterns `≥1` (대시 AND 조사·체언 AND 전환 공식) — HEAD pre-state **0 / 0 / 0** per file (5 files). Iter-3: extended from single `대시` (covered 1 of REQ-002's 3 patterns) to all 3, using the HEAD-absent `전환 공식` for pattern (c) rather than the self-passing `에서.*로` |
| AC-REM-003 | `humanize-korean` **SHALL** define a slide/copy genre profile allowing noun-phrase titles, forbidding dash-connection + particle-ending. | 003 | `grep -cE "^#{2,4}.*(슬라이드/카피 장르 프로파일\|카피 장르 프로파일)" plugins/moai-cowork/skills/humanize-korean/SKILL.md` | `≥1` (distinctly-named genre-profile section **heading**) — HEAD pre-state **0**. Iter-3: old `슬라이드\|카피 장르\|genre`=**5** self-passed on `--genre` CLI flags (L75/91/172/227/261, `genre_hint`); replaced with a HEAD-absent structural section heading (§D.8.10) |
| AC-REM-004 | **When** `pptx-designer` produces copy, the gate **SHALL** see it: a **copy-only STAGE** with a nested gate chain exists. | 004 | Hardened structural predicate — see §D.8 (copy-only stage heading `카피 전용 게이트` + `ai-slop-reviewer`/`humanize-korean` nested INSIDE that stage). | stage heading `≥1` AND both gate skills nested `≥1` — HEAD pre-state 0 / 0 / 0 (old predicate `카피\|copy`=5 + gate=1 both self-passed pre-remediation) |
| AC-REM-005 | **When** `notebooklm` emits its 6-block template, title-writing rules **SHALL** be embedded INSIDE the template. | 005 | Hardened structural predicate — see §D.8 (title-rule descriptor extracted from the 6-block template section ONLY; broad `에서.*로` OR dropped). | `≥1` inside the template block — HEAD pre-state 0 (old predicate self-passed at 3: the `에서.*로` matches are natural Korean co-occurrence OUTSIDE the template, lines 31/165/210) |
| AC-REM-006 | `pdf-writer` **SHALL NOT** reference `moai-office/` paths; **SHALL** use `${CLAUDE_PLUGIN_ROOT}`. | 006 | `grep -c "moai-office" plugins/moai-cowork/skills/pdf-writer/SKILL.md; grep -c "CLAUDE_PLUGIN_ROOT" plugins/moai-cowork/skills/pdf-writer/SKILL.md` | `0` then `≥1` |
| AC-REM-007 | `humanize-korean` **SHALL NOT** reference `moai-content/skills/humanize-korean/` paths; **SHALL** use `${CLAUDE_PLUGIN_ROOT}`. | 007 | `grep -c "moai-content/skills/humanize-korean" plugins/moai-cowork/skills/humanize-korean/SKILL.md; grep -c "CLAUDE_PLUGIN_ROOT" plugins/moai-cowork/skills/humanize-korean/SKILL.md` | `0` then `≥1` |
| AC-REM-008 | The slide/deck example sources **SHALL NOT** teach dash/particle-ending copy. | 008 | `grep -c "PPTX — 브라우저에서" plugins/moai-cowork/skills/html-slide/samples/deck-sample.json; grep -c "example 로 —" plugins/moai-cowork/skills/html-slide/samples/deck-sample.json`; manual confirm rewritten sample non-empty (`wc -l` > 0) | each exemplary-slop literal `0`; sample non-empty (EC-6) — HEAD pre-state each `≥1` (subtitle dash-contrast L17 `PPTX — 브라우저에서`, trailing-dash L107 `example 로 —`). Iter-3: bare `grep -c " — "`=**8** dropped — it over-counted legitimate data-array bullet dashes (metric rows L56-58/68-71), not title-field slop (§D.8.10 + §D.6 em-dash-not-a-discriminator finding) |
| AC-REM-009 | Commerce/marketplace/detail-page/newsletter slop examples **SHALL** be rewritten (per-source). | 009 | Per-source specific-literal defect→0 — see §D.8 table (all 7 REQ-009 sources, 12 confirmed exemplary-slop literals). | each literal `0` — HEAD pre-state each `≥1` (discriminates; old predicate covered only 2 of 7 sources) |
| AC-REM-010 | Remaining samples **SHALL** be rewritten; the deceptive-ad "집중력 200%" **SHALL** be removed (per-source). | 010 | Per-source predicate — see §D.8 (live-commerce specific-literal defect→0; executive-summary/pm-weekly-report/html-report/interview-coach guidance-prose em-dash `< baseline` with EC-3 exemption; design-system-library → AC-019; ai-slop-reviewer → AC-012). | live-commerce literals `0`; density files `< baseline`; subsumed sources cross-referenced — HEAD pre-state proven in §D.8 |
| AC-REM-011 | The boilerplate "…하는 하네스입니다" **SHALL** be naturalized and "하네스" removed from user-facing docs. | 011 | `grep -rl "협력하여.*하네스입니다\|하는 하네스입니다" plugins/moai-cowork/skills plugins/moai-design/skills \| wc -l` | `0` (boilerplate sentence eliminated) |
| AC-REM-012 | Em-dash density in the 2 gate skills' **guidance prose** **SHALL** drop below baseline; dash-rule descriptors + negative examples are EXEMPT. | 012 | Exemption-encoded predicate — see §D.8 (em-dash count EXCLUDING dash-rule descriptor + negative-example lines, so the remediation-added dash descriptors of REQ-001/002 do not inflate the count). | `< 41` (humanize-korean) and `< 10` (ai-slop-reviewer), guidance-prose dashes only — HEAD baseline 41 / 10; `대시`-marker lines = 0 on HEAD, so REQ-001/002 additions auto-exempt |
| AC-REM-013 | Priority Korean-copy skills **SHALL** each declare a gate chain. | 013 | `for s in marketplace-curation live-commerce landing-page hwpx-writer learning-material detail-page-planner job-analyzer data-visualizer; do grep -cl "humanize-korean\|ai-slop-reviewer" plugins/moai-cowork/skills/$s/SKILL.md; done` | each `≥1` (gate chain present) |
| AC-REM-014 | `moai-workflow-design` **SHALL** be wired into the main-line router; advisory tone **SHALL** be standardized to required. | 014 | `grep -c "moai-workflow-design" plugins/moai-cowork/skills/project/SKILL.md; grep -rc "정리하면 좋습니다" plugins/moai-cowork/skills` | main-line wiring `≥1` in the `project` router; advisory-phrase count strictly below plan-phase baseline (→ trending 0) — HEAD pre-state: `project/SKILL.md` moai-workflow-design=**0**; advisory `정리하면 좋습니다` baseline **3** (copywriting/blog/newsletter). Iter-3: recursive `grep -rc … skills`≥1 self-passed at 6 peripheral files (cd-handoff-reader, moai-domain-brand-design, design-plugin internals — none the main-line router); anchored to the `project` router where the token is HEAD-absent (§D.8.10) |
| AC-REM-015 | No skill **SHALL** reference a deprecated namespace. | 015 | `grep -rl "moai-office\|moai-content\|moai-media\|moai-finance\|moai-book\|moai-business\|moai-marketing\|moai-education\|moai-legal" plugins/moai-cowork/skills plugins/moai-design/skills \| wc -l` | `0` |
| AC-REM-016 | **When** `project` routes, it **SHALL** target the single `moai-cowork` architecture, not the 27-plugin topology. | 016 | `grep -c "moai-office:\|moai-content:\|moai-media:\|27\|29개 플러그인\|distributed" plugins/moai-cowork/skills/project/SKILL.md` | `0` (no retired-topology routing) |
| AC-REM-017 | Broken links, phantom dirs, stale `CLAUDE.local.md`/`CONNECTORS.md` refs **SHALL** be repaired. | 017 | `grep -rc "CLAUDE.local.md\|CONNECTORS.md" plugins/moai-cowork/skills; test ! -d plugins/moai-cowork/skills/design-system-library/moai-content && echo GHOST-GONE \|\| echo GHOST-PRESENT` | stale-ref count `0`; specific ghost `GHOST-GONE` — HEAD pre-state: stale-refs **3** (html-slide/audio-gen/higgsfield-image) → 0; ghost `design-system-library/moai-content/skills/html-slide/{references,samples}` **present** → GHOST-GONE. Iter-3: bare `find … -type d -empty` dropped — it over-reached 7 unrelated empty `references/` dirs (draft-offer, nda-triage, xlsx-creator, variance-analysis, media-production), only 1 is REQ-017's ghost (§D.8.10) |
| AC-REM-018 | **When** category prefixes are applied, no dangling old-name reference **SHALL** survive. | 018 | run-phase: for each renamed old-name `N` listed in §D.9 Phase A Rename Mapping table, `grep -rl "\bN\b" plugins/moai-cowork plugins/moai-design .claude-plugin/marketplace.json` | `0` per old-name (full-tree integrity). §D.9 (approved 2026-07-03) is the rename source-of-truth; the run-phase script MUST NOT invent rename pairs outside that table. |
| AC-REM-019 | `design-system-library` **SHALL** be canonical in design; the cowork copy **SHALL** be a pointer. | 019 | `grep -c "moai-design 플러그인의 정본" plugins/moai-cowork/skills/design-system-library/SKILL.md; test ! -d plugins/moai-cowork/skills/design-system-library/systems && echo DEDUP-DONE \|\| echo STILL-FULL; test -f plugins/moai-design/skills/design-system-library/SKILL.md && echo CANONICAL-PRESENT` | HEAD-absent pointer sentence `≥1` AND cowork `systems/` dir removed (`DEDUP-DONE`) AND design canonical present — HEAD pre-state: pointer sentence **0**; cowork `systems/` **present** (78 entries) + full 180-line SKILL.md → `STILL-FULL`. Iter-3: old `moai-design\|pointer\|canonical\|참조`=**6** self-passed on incidental `참조` while design canonical already pre-exists; replaced with a structural dedup signal + HEAD-absent pointer sentence (§D.8.10) |
| AC-REM-020 | `brand-identity` scope **SHALL** be narrowed to personal-branding; system work points to `moai-domain-brand-design`. | 020 | `grep -c "퍼스널 브랜딩 산출물 전용" plugins/moai-cowork/skills/brand-identity/SKILL.md; grep -c "moai-domain-brand-design" plugins/moai-cowork/skills/brand-identity/SKILL.md` | scope-boundary literal `≥1` AND pointer `moai-domain-brand-design` `≥1` — HEAD pre-state **0 / 0**. Iter-3: old `moai-domain-brand-design\|퍼스널\|personal`=**2** self-passed on the pre-existing `moai-cowork:personal-branding` row (L15/L195); `moai-domain-brand-design` itself is HEAD-absent in this file, and `퍼스널 브랜딩 산출물 전용` is a HEAD-absent scope literal (§D.8.10) |
| AC-REM-021 | skill-builder/skill-template **SHALL** include Korean example-copy authoring rules. | 021 | `grep -c "대시 대비 헤드라인" plugins/moai-cowork/skills/skill-builder/SKILL.md; grep -c "대시\|조사·체언\|슬롭" plugins/moai-cowork/skills/skill-builder/SKILL.md` | authoring-rules descriptor `대시 대비 헤드라인` `≥1` AND `대시\|조사·체언\|슬롭` `≥1` — HEAD pre-state **0 / 0**. Iter-3: old `…\|에서.*로\|slop`=**5** self-passed (`에서.*로`=3 incidental prose; `slop`=2 ⊂ `ai-slop-reviewer` at L245/251); dropped both, anchored to the HEAD-absent descriptor literal introduced by REQ-001 (§D.8.10) |
| AC-REM-022 | A lint script **SHALL** exist, be executable, and exit non-zero on each of the 4 pattern classes. | 022 | `ls -l plugins/moai-cowork/scripts/*lint* 2>/dev/null; test -x <lint-script>; <lint-script> --self-test` | script present + executable; self-test exit non-zero on dash/cliché/old-ns/boilerplate inputs |
| AC-REM-023 | The remediation process **SHALL NOT** modify files outside the owned trees. | 023 | `git diff --name-only \| grep -E "^plugins/moai-code/\|^plugins/moai-cowork/commands/\|^internal/template/templates/\|^www/" \| wc -l` | `0` |
| AC-REM-024 | The remediation process **SHALL** record the `www/plugins/` re-sync requirement and **SHALL NOT** edit `www/`. | 024 | `git diff --name-only \| grep -c "^www/"; awk '/^## §E\.2 Run-phase Evidence/{c=1;next} /^## §E\./{c=0} c' .moai/specs/SPEC-MOC-PLUGIN-REMEDIATION-001/progress.md \| grep -c "SITE-IA\|www/plugins"` | www edits `0`; **run-phase** re-sync note in §E.2 `≥1` — HEAD pre-state: §E.2 is `_<pending>_` placeholder → **0**. Iter-3: old file-wide `grep -c … progress.md`=**2** self-passed on the plan-phase §E.1 scope/recording lines (L11-12); scoped to the run-phase §E.2 section via `awk` range so the AC verifies the run-phase actor recorded it (§D.8.10) |

### §D.1 Severity Classification

| Severity | AC IDs | Rationale |
|----------|--------|-----------|
| MUST-PASS (blocking, release-blocking subset) | AC-REM-001, 002, 004, 005, 006, 007 | P0 gate structure + P2 immediate-failure path repair — the release-blocking core (M1) |
| MUST-PASS (blocking) | AC-REM-015, 018, 023 | Deprecated-namespace sweep, rename integrity, scope discipline — repository-integrity gates |
| SHOULD-PASS | AC-REM-003, 008, 009, 010, 011, 012, 013, 014, 016, 017, 019, 020, 021, 022 | High-value decontamination / wiring / re-occurrence-prevention — deferrable one iteration without breaking repository integrity |
| RECORD-ONLY | AC-REM-024 | Records the downstream re-sync requirement; the re-sync itself is SITE-IA's work |

### §D.2 Traceability (REQ ↔ AC)

Each REQ-REM-0XX maps 1:1 to AC-REM-0XX by shared numeric suffix (REQ-REM-001 ↔ AC-REM-001, … through 024). No REQ is unverified; no AC lacks a source REQ. 24 requirements ↔ 24 acceptance criteria. AC-REM-009 and AC-REM-010 decompose into **per-source sub-predicates** (§D.8) that fan out across every source their REQ enumerates — the 1:1 REQ↔AC mapping is preserved (one AC per REQ) while the mechanical coverage now spans all listed sources rather than 2-3 samples.

### §D.3 Indirect Verification

- The functional-contract PRESERVE constraint (spec.md §C.1) is verified indirectly: AC-REM-023's scope-discipline diff plus the decontamination ACs (which target copy/prose lines, not trigger/workflow blocks) together evidence that no functional contract changed, without a per-skill contract-diff AC.
- Reference-model conformance (`card-news`, `campaign-planner`) is verified indirectly via AC-REM-013 (the wired skills adopt the same gate-chain pattern the reference models exemplify).

### §D.4 Closure Gates

- All MUST-PASS ACs (§D.1, both blocking rows) PASS with command-output evidence.
- The release-blocking subset (AC-REM-001..007) PASS is a hard prerequisite for any release-readiness claim.
- SHOULD-PASS ACs PASS, or each deferral is explicitly recorded with rationale in the completion report.
- `git diff --stat` confirms zero out-of-scope modifications (AC-REM-023).
- The `www/plugins/` re-sync requirement is recorded (AC-REM-024) and handed to SITE-IA.

### §D.5 Definition of Done

1. All MUST-PASS ACs PASS with command-output evidence in the completion report.
2. Release-blocking subset (AC-REM-001..007) PASS confirmed.
3. SHOULD-PASS ACs PASS or explicitly deferred with rationale.
4. Phase A rename integrity (AC-REM-018) shows 0 dangling references across the owned trees + manifest.
5. Scope discipline (AC-REM-023) = 0 out-of-scope file modifications.
6. `progress.md` §E.2/§E.3 populated by the run-phase implementer with the evidence above (this plan-phase artifact carries only the §E.1 signal + placeholder §E.2-§E.5 headings).
7. The `www/plugins/` re-sync requirement recorded and cross-referenced to SITE-IA (AC-REM-024).

### §D.6 Residual Risks

- **Count drift (already observed)**: audit → plan-phase counts drifted (177 vs 178 skills, 68 vs 78 ns files). Run-phase MUST re-baseline (EC-1); acting on stale numbers is the primary residual risk, mitigated by the predicate-based AC design.
- **Em-dash negative-example ambiguity**: REQ-REM-012's count could be inflated by legitimate negative-example dashes in the gate skills (EC-3); the AC records the exemption, but exact separation depends on the implementer's markup discipline.
- **Rename blast radius**: the Phase A rename (REQ-REM-018) touches every renamed skill's references family-wide; an incomplete grep sweep would leave a dangling route. Mitigated by the per-old-name grep→0 AC and by sequencing rename after namespace normalization (EC-4).
- **Market copy drift window**: between this SPEC's source edits and SITE-IA's re-sync, `www/plugins/` copies are stale (REQ-REM-024). Accepted; SITE-IA owns closure.
- **Boilerplate predicate breadth**: the bare-term "하네스" grep (77 files) is broader than the boilerplate-sentence target (REQ-REM-011); the AC targets the sentence pattern, so some benign "하네스" mentions may remain and are out of this AC's scope.
- **Em-dash is not a clean slop discriminator (iteration-2 finding)**: plan-phase iter-2 verification (§D.8) established that a bare/spaced/quoted em-dash predicate over-reaches — most `—` in the copy skills are legitimate (definition-table cells, skill titles, cross-ref lists, `/command — args` CLI examples, JSON QA statuses). AC-009 and (iter-3) AC-008 therefore use specific exemplary-slop literals, and AC-010/AC-012 apply EC-3 exemptions. Iter-3 additionally dropped bare `find -type d -empty` (AC-017 over-reach) in favor of the specific ghost path.
- **Iter-3 literal-exactness dependency (NEW)**: the hardened addition-predicates now key on EXACT HEAD-absent literals the run-phase implementer must author verbatim — `전환 공식` (AC-001c/002c), `대시 대비 헤드라인` (AC-002a/021), the `슬라이드/카피 장르 프로파일` heading (AC-003), `moai-design 플러그인의 정본` (AC-019), `퍼스널 브랜딩 산출물 전용` (AC-020). A semantically-correct deliverable that phrases these differently would FAIL the AC. Mitigation: these exact strings are the recommended descriptor/heading/pointer wording and are recorded in §D.8.10; the run-phase implementer SHOULD adopt them verbatim, or record a blocker if a different wording is required (then the AC literal is updated to match). This is the accepted trade-off for closing the false-pass class — a specific literal discriminates; a broad regex self-passes. Residual risk: the specific-literal approach only catches the enumerated exemplary-slop strings; a NEW dash-contrast headline the run-phase might introduce, or a slop instance the audit did not enumerate, is not guarded by these predicates. Mitigation: the P4 lint CI (REQ-REM-022 / AC-REM-022) is the standing net for dash-density + cliché patterns family-wide, and EC-6 (non-empty rewrite) is judged by the run-phase reviewer.
- **AC-010 density-predicate weakness**: for executive-summary/pm-weekly-report/html-report/interview-coach the `< baseline` guidance-prose em-dash predicate is satisfiable by a single-dash removal (§D.8 honest limitation). Substantive decontamination of these four report skills relies on the run-phase reviewer's EC-6 judgment, not the density delta alone.

### §D.7 Forward-Looking Checks

- After this SPEC closes, natural follow-ups: (a) SITE-IA `www/plugins/` re-sync (REQ-REM-024); (b) non-Korean (en/ja/zh) copy-quality pass using `moai-domain-humanize` locales (out of scope here); (c) extending the lint CI (REQ-REM-022) into a pre-commit hook, not only pre-market-sync; (d) a Tier-L `design.md`/`research.md` extraction if the plan-auditor requires the full 5-artifact set.

### §D.8 Hardened Predicates — discrimination proofs (iter-2: AC-004/005/009/010/012; iter-3: AC-001c/002/003/008/014/017/019/020/021/024)

> These predicates were re-authored to remove **mechanical false-pass** (a `≥1` addition-predicate that already returns `≥1` pre-remediation, or a defect-predicate whose pattern matches incidental language, has zero discriminating power) per `.claude/rules/moai/core/verification-claim-integrity.md`. Each was executed READ-ONLY against HEAD (`6d78fbf`) to prove it returns the pre-remediation / not-yet-done state. HEAD counts below are the plan-phase-observed baselines; run-phase re-baselines per `plan.md` §C.
>
> **Iter-3 generalization (root-cause fix).** Iter-2 hardened only the 5 named predicates (004/005/009/010/012) and left the SAME false-pass class in ≥6 sibling ACs — the Opus "does not silently generalize" failure. Iter-3 ran the ENTIRE `≥1` addition-predicate set against HEAD (not just the flagged ones) and rewrote every self-pass. The full sweep matrix is §D.8.10; the iter-2 subsections (§D.8 AC-004…AC-012) are retained below unchanged.

#### AC-004 — `pptx-designer` copy-only STAGE + nested gate chain (BLOCKING / D1)

```bash
F=plugins/moai-cowork/skills/pptx-designer/SKILL.md
# (a) copy-only STAGE heading present (distinctly-named, ABSENT on HEAD)
grep -cE "^#{2,4}.*카피 전용 게이트" "$F"
# (b) gate chain nested INSIDE that stage (structural extraction, not file-wide)
awk '/^#{2,4}.*카피 전용 게이트/{c=1;print;next} /^#{2,4} /{c=0} c' "$F" | grep -c "ai-slop-reviewer"
awk '/^#{2,4}.*카피 전용 게이트/{c=1;print;next} /^#{2,4} /{c=0} c' "$F" | grep -c "humanize-korean"
```
- **Expected (remediated)**: (a) `≥1`; (b) `≥1` AND `≥1`.
- **HEAD pre-state**: `0` / `0` / `0` (also: `ai-slop-reviewer` appears 0 times file-wide on HEAD). The OLD predicate (`grep -c "카피\|copy"` = **5**, `grep -c "ai-slop-reviewer\|humanize-korean"` = **1**) had BOTH halves passing pre-remediation → zero discriminating power. The NEW predicate demands a NEW distinctly-named copy-only stage heading (`카피 전용 게이트`, absent from the current `1단계`…`6단계` workflow) AND the gate chain nested inside that stage (AND-semantics, structural — the `awk` range restricts the grep to the stage body).

#### AC-005 — `notebooklm` title rules INSIDE the 6-block template (BLOCKING / D2)

```bash
G=plugins/moai-cowork/skills/notebooklm-slide-prompt/SKILL.md
awk '/^#### NotebookLM Prompt 본문 6블록 템플릿/{c=1;next} /^#### /{c=0} c' "$G" \
  | grep -c "대시\|조사·체언\|체언 종결"
```
- **Expected (remediated)**: `≥1` (title-writing rules embedded inside the template block).
- **HEAD pre-state**: `0`. The broad `에서.*로` OR clause was DROPPED: on HEAD it matched **3** natural Korean co-occurrences (line 31 `Keynote에서 … 열림`, line 165 `카탈로그에서 … 사용`, line 210 `NotebookLM에서 revise로`), ALL OUTSIDE the template, so the OLD file-wide predicate self-passed at 3. The NEW predicate (i) extracts the 6-block template section only (AND-semantics: descriptor present AND inside the template) and (ii) uses `대시`/`조사·체언`/`체언 종결` literals, which are 0 in the template block on HEAD.

#### AC-009 — per-source exemplary-slop literals (7 REQ-009 sources, SHOULD-PASS / D4)

Each literal is a confirmed exemplary marketing-copy slop string (a dash-contrast / CTA headline TAUGHT as a good example), verified present on HEAD. **Bare/spaced em-dash counts are deliberately NOT used**: inspection shows the em-dashes in these files are overwhelmingly legitimate (definition-table cells `| **N** — Need |`, skill titles, cross-ref lists, `/command — args` CLI examples, JSON QA statuses `"PASS — …"`), so a bare-`—`→0 (or quoted-`"… — …"`→0) predicate would over-reach and contradict REQ-001/002 + EC-3. Per governing principle (a), specific literals discriminate; broad regex does not.

| Source | Literal(s) — defect→0 | File | HEAD count |
|--------|-----------------------|------|-----------:|
| commerce-promotion-planner | `1주년 감사 —` ; `올해 마지막 —` | `plugins/moai-cowork/skills/commerce-promotion-planner/SKILL.md` | 2 ; 1 |
| commerce-repurchase-timer | `이번 통 끝나가요 —` ; `다시 만날 시간 — 첫 박스` | `plugins/moai-cowork/skills/commerce-repurchase-timer/SKILL.md` | 1 ; 1 |
| commerce-product-naming | `집에서 진정 — 비건 세럼` | `plugins/moai-cowork/skills/commerce-product-naming/SKILL.md` | 1 |
| commerce-channel-message | `올빼미가 슬퍼해요 —` ; `사이즈 마지막 1개 —` | `plugins/moai-cowork/skills/commerce-channel-message/SKILL.md` | 1 ; 1 |
| marketplace-curation | `11월 한정 100세트` ; `양만큼만` | `plugins/moai-cowork/skills/marketplace-curation/references/kakao-makers.md` | 1 ; 1 |
| detail-page-copy | `지금 바로 만나보기` ; `방수 — 직장인 통근` | `.../detail-page-copy/references/13-sections.md` ; `.../references/category-briefs.md` | 1 ; 1 |
| newsletter | `오늘 마감 —` | `plugins/moai-cowork/skills/newsletter/SKILL.md` | 1 |

- **Expected (remediated)**: every literal `grep -c` → `0`. **HEAD pre-state**: every literal `≥1` (discriminates). EC-6 non-empty guard applies (rewrite each into a good example, do not delete).

#### AC-010 — per-source, tool-confirmed state (7 REQ-010 sources, SHOULD-PASS / D5)

grep-on-HEAD confirms a dash-contrast **exemplary-copy** defect for `live-commerce` ONLY; the remaining REQ-010 sources carry prose-density dashes (no exemplary-copy literal) or are subsumed by another AC. Per verification-claim-integrity §1.1 surface 3 (a defect claim is a hypothesis until the tool confirms it), each source gets the predicate its actual on-HEAD state supports rather than a fabricated dash-copy literal.

| Source | Predicate | Expected | HEAD |
|--------|-----------|----------|-----:|
| live-commerce | `grep -rc "집중력 200" .../live-commerce/` (deceptive ad) ; `grep -c "케이스 — 가죽 케이스" .../live-commerce/references/live-script.md` (spoken-script dash) | both `0` | 1 ; 1 |
| executive-summary | guidance-prose em-dash `< baseline` — `grep -c "—" .../executive-summary/SKILL.md` (EC-3 exempt) | `< 33` | 33 |
| pm-weekly-report | guidance-prose em-dash `< baseline` — `grep -c "—" .../pm-weekly-report/SKILL.md` (EC-3 exempt) | `< 33` | 33 |
| html-report | guidance-prose em-dash `< baseline` — `grep -c "—" .../html-report/SKILL.md` (SKILL.md prose only; `references/` HTML+CSS+token tables are legitimate, not counted) | `< 25` | 25 |
| interview-coach | guidance-prose em-dash `< baseline` — `grep -c "—" .../interview-coach/SKILL.md` (EC-3 exempt) | `< 20` | 20 |
| design-system-library | **subsumed by AC-REM-019** — the cowork copy is reduced to a pointer (dedup), removing its samples entirely | pointer present (AC-019) | n/a |
| ai-slop-reviewer | **subsumed by AC-REM-012** — the gate skill's own model-answer / negative-example dash is governed by the guidance-prose em-dash reduction (EC-3 exempts genuine negative examples) | `< 10` (AC-012) | 10 |

Prose-density baselines are re-measured at run-phase pre-flight (`plan.md` §C); the `< baseline` form is discriminating (`< N` fails at the current value `N`, passes only after a reduction). **Honest limitation**: a `< baseline` density predicate is satisfiable by removing a single guidance-prose dash — it guards against non-reduction, but the substantive decontamination of these four report skills is judged by the run-phase reviewer against EC-6, not by the density delta alone. This limitation is recorded rather than papered over with a false-precision literal.

#### AC-012 — exemption-encoded guidance-prose em-dash (SHOULD-PASS / D6)

```bash
for F in plugins/moai-cowork/skills/humanize-korean/SKILL.md \
         plugins/moai-cowork/skills/ai-slop-reviewer/SKILL.md; do
  grep "—" "$F" | grep -vE "대시|❌|✅|나쁜 예|좋은 예" | wc -l
done
```
- **Expected (remediated)**: `< 41` (humanize-korean) and `< 10` (ai-slop-reviewer), guidance-prose dashes only.
- **HEAD baseline**: `41` / `10`. On HEAD every em-dash is a guidance-prose connector (`적용 대상 — 모든…`, `# Humanize Korean — …`, reference-list `[quick-rules.md](…) — …`) and `대시`-marker lines = **0**, so the exclusion baseline equals the raw count. The `grep -vE "대시|❌|✅|나쁜 예|좋은 예"` exclusion **encodes the EC-3 exemption**: REQ-001/002 register the dash-rule descriptor named "대시 대비 헤드라인" (which itself contains a `—`) and negative-example blocks quote the bad pattern — both are excluded so they cannot inflate the count. This resolves the D6 contradiction where a bare `grep -c "—"` would count the remediation's own dash descriptors against the reduction, making a correctly-decontaminated file potentially fail the AC.

#### §D.8.10 — iter-3 generalized addition-predicate sweep (EVERY `≥1` predicate against HEAD)

This is the **complete** discrimination proof for every `≥1` addition-predicate in the §D matrix, executed READ-ONLY against HEAD (`6d78fbf`) on 2026-07-02. Column **HEAD** is the pre-remediation count of the CURRENT (post-iter-3) predicate; a discriminating addition-predicate MUST show the not-yet-done state (`0`, `STILL-FULL`, `GHOST-PRESENT`) so it can only PASS after the REQ deliverable lands. Defect-predicates (`→0`) are inherently immune (a pattern already absent is a true pass) and are excluded from this table (they live in §D.8 AC-009/010 + the matrix defect rows). New descriptor/heading/pointer literals were each grep-verified HEAD-absent tree-wide before adoption.

| AC | Addition-predicate (post-iter-3) | HEAD | Discriminates? (pre-remediation state) | Iter-3 change |
|----|----------------------------------|-----:|----------------------------------------|---------------|
| 001(a) | `grep -c "대시"` ai-slop-reviewer | 0 | YES — descriptor absent | (unchanged, already discriminated) |
| 001(b) | `grep -c "조사·체언\|체언 종결\|조사 종결"` | 0 | YES — descriptor absent | (unchanged) |
| 001(c) | `grep -c "전환 공식"` | 0 | YES — was `에서.*로`=6 self-pass | **FIXED** — HEAD-absent literal for "A에서 B로" |
| 002 (×5) | per file: `대시` + `조사·체언…` + `전환 공식` | 0/0/0 | YES — all 3 absent per file | **FIXED** — extended 1→3 patterns, `전환 공식` not `에서.*로` |
| 003 | `grep -cE "^#{2,4}.*(슬라이드/카피 장르 프로파일\|카피 장르 프로파일)"` | 0 | YES — heading absent | **FIXED** — was `슬라이드\|카피 장르\|genre`=5 (`--genre` flags) |
| 004(a) | `카피 전용 게이트` stage heading | 0 | YES — stage absent | (iter-2, re-verified) |
| 004(b) | nested `ai-slop-reviewer` / `humanize-korean` (awk range) | 0/0 | YES — no nested gate | (iter-2, re-verified) |
| 005 | title-rule in 6-block template (awk range) | 0 | YES — rules not embedded | (iter-2, re-verified) |
| 006 | `grep -c "CLAUDE_PLUGIN_ROOT"` pdf-writer | 0 | YES — not yet migrated | (unchanged) |
| 007 | `grep -c "CLAUDE_PLUGIN_ROOT"` humanize-korean | 0 | YES — not yet migrated | (unchanged) |
| 013 (×8) | `humanize-korean\|ai-slop-reviewer` per skill | 0 (all 8) | YES — no gate chain on any | (unchanged, verified all 8: marketplace-curation, live-commerce, landing-page, hwpx-writer, learning-material, detail-page-planner, job-analyzer, data-visualizer) |
| 014 wiring | `grep -c "moai-workflow-design"` **project/SKILL.md** | 0 | YES — router lacks wiring | **FIXED** — was recursive `grep -rc … skills`≥1 (6 peripheral files) |
| 014 advisory | `grep -rc "정리하면 좋습니다"` `< baseline 3` | 3 | YES — density delta | (unchanged, still discriminates) |
| 019 pointer | `grep -c "moai-design 플러그인의 정본"` | 0 | YES — pointer sentence absent | **FIXED** — was `moai-design\|pointer\|canonical\|참조`=6 |
| 019 dedup | `test ! -d …/design-system-library/systems` | STILL-FULL | YES — systems/ present (78) | **FIXED** — structural dedup signal added |
| 020 scope | `grep -c "퍼스널 브랜딩 산출물 전용"` | 0 | YES — scope literal absent | **FIXED** — was `…\|퍼스널\|personal`=2 |
| 020 pointer | `grep -c "moai-domain-brand-design"` brand-identity | 0 | YES — pointer target absent | **FIXED** — target itself HEAD-absent in file |
| 021 descriptor | `grep -c "대시 대비 헤드라인"` skill-builder | 0 | YES — descriptor absent | **FIXED** — was `…\|에서.*로\|slop`=5 |
| 021 remainder | `grep -c "대시\|조사·체언\|슬롭"` skill-builder | 0 | YES — dropped incidental `에서.*로`/`slop` | **FIXED** |
| 022 | lint script present + executable | (absent) | YES — new artifact, no `*lint*` in scripts/ | (unchanged, new script) |
| 024 note | run-phase §E.2 (awk range) `SITE-IA\|www/plugins` | 0 | YES — §E.2 is `_<pending>_` | **FIXED** — was file-wide=2 (plan-phase §E.1 L11-12) |
| 008 | `PPTX — 브라우저에서` + `example 로 —` (defect→0) | 1 / 1 | YES — literals present pre-remediation | **FIXED** — was bare `grep -c " — "`=8 over-reach |
| 017 ghost | `test ! -d …/design-system-library/moai-content` | GHOST-PRESENT | YES — ghost dir present | **FIXED** — was `find -type d -empty` (7 dirs, 1 ghost) |

**Verdict**: every `≥1` addition-predicate now shows the pre-remediation / not-yet-done state on HEAD. The 6 iter-2-surviving self-passes (001c/003/014wiring/019/020/021) + AC-024 (newly caught) + 3 over-reach defect predicates (008/017 + AC-002 coverage) are all resolved. Descriptor/heading/pointer literals adopted (`전환 공식`, `대시 대비 헤드라인`, `슬라이드/카피 장르 프로파일`, `moai-design 플러그인의 정본`, `퍼스널 브랜딩 산출물 전용`) were each verified `grep -rl … = 0` across both owned trees before adoption. The AND-semantics (019: pointer AND systems-removed; 020: scope-literal AND pointer; 021: descriptor AND remainder) prevent a single incidental match from re-introducing a self-pass.

### §D.9 Phase A Rename Mapping (approved 2026-07-03 — double-prefix collisions resolved via body-rename; 38 remaining REVIEW accepted as default; stub disposition = rename)

**Status**: APPROVED 2026-07-03 — authored by manager-spec on 2026-07-02 per Option 1 (manager-spec authors draft → user reviews/approves → run-phase re-executes AC-018); user approved 2026-07-03 with two decisions: (1) double-prefix collisions resolved via body-rename (cluster 8 — `media-production` → `media-asset-production`, `content-calendar` → `content-editorial-calendar`); (2) remaining 38 REVIEW accepted as default classification. This section is now the rename source-of-truth that AC-REM-018's grep predicate iterates over; the run-phase filesystem rename MAY proceed.

**Live scope**: 176 cowork skills (re-baselanced 2026-07-02 against `plugins/moai-cowork/skills/` via `find … -maxdepth 1 -mindepth 1 -type d -not -name project | wc -l`). Plan-phase baseline was 177 — delta 1 is attributable to the Phase B boundary dedup commits (M5 work in commits `b7ca913`→`665bbb3`) per the task hint, NOT run-phase count drift (EC-1 does not apply). The `project` skill is excluded per EC-7 (shared-file boundary with SPEC-MOC-BOOTSTRAP-DESKTOP-001).

#### §D.9.1 Taxonomy — 11 prefix buckets

The 11 buckets derive from three authoritative sources:

1. **The 9 deprecated AC-015 namespaces** → 9 prefixes: `office-`, `content-`, `media-`, `finance-`, `book-`, `business-`, `marketing-`, `education-`, `legal-` (mirrors `moai-office`, `moai-content`, `moai-media`, `moai-finance`, `moai-book`, `moai-business`, `moai-marketing`, `moai-education`, `moai-legal`)
2. **REQ-018 explicit example** → 1 prefix: `commerce-`
3. **Residual bucket** → 1 prefix: `general-` (gates, meta, tooling, cross-domain utilities)

The taxonomy is intentionally aligned with AC-015's namespace set so that Phase A prefix rename and M4 (REQ-015) namespace normalization share the same domain vocabulary — the same prefix that classifies a skill also names the namespace it belongs to once the deprecated `moai-*` references are normalized.

**Residual-bucket policy — what goes to `general-`**:
- **Gates** (Korean-slop detection infrastructure, not a domain skill): `ai-slop-reviewer`, `humanize-korean`, `cd-slop-check`
- **Meta / authoring tooling**: `skill-builder`, `skill-template`, `skill-tester`, `mcp-connector-setup`, `feedback`, `ai-diagnostic`
- **Claude Design integration tooling** (the non-gate `cd-*` family; task hint names "cd-skill-*" as residual): `cd-brief`, `cd-handoff-reader`, `cd-prompt-builder`, `cd-system-prep`
- **Lifestyle / personal** (no AC-015-aligned domain; project router's `moai-lifestyle` category): `self-care`, `wellness-coach`, `event-planner`, `travel-planner` — marked ⚠ REVIEW (the user MAY prefer an `office-` productivity grouping or a 12th `lifestyle-` prefix)

The `project` router's category-routing table uses additional namespace names (`moai-hr`, `moai-product`, `moai-support`, `moai-research`, `moai-career`, `moai-comms`, `moai-productivity`, `moai-operations`, `moai-data`, `moai-public-data`, `moai-bi`, `moai-pm`, `moai-sales`, `moai-wealth`, `moai-core`, `moai-workflow-design`) — these are NOT in AC-015's deprecated-9 sweep, so they have no natural AC-015-aligned prefix. Skills belonging to these categories collapse into the closest-fitting AC-015 prefix (typically `business-` or `office-`) or into `general-` (cross-domain) with ⚠ REVIEW.

**Stub-skill handling**: 4 stubs are already-relocated pointers to canonical `public-data-*` skills (`business-real-estate-search`, `data-public-data`, `finance-court-auction-search`, `finance-korean-stock-search`) plus 1 deprecated stub (`social-media` → `sns-content`). All 5 are renamed for prefix consistency in this draft. The user MAY alternatively choose to DELETE the stubs in a Phase-B-style cleanup rather than rename — marked ⚠ REVIEW.

**Already-prefixed no-ops**: 18 of 31 `commerce-*` skills + 8 of 8 `book-*` skills already carry their target prefix (total 26); their rename is a no-op (old name == new name). They are listed explicitly in the table for verification — the run-phase script MUST treat them as no-renames but STILL include them in the dangling-reference grep, since any old-name reference is still a dangling reference. (`content-calendar` was originally counted here but moved to body-rename per the 2026-07-03 user decision — see cluster 8.)

#### §D.9.2 Category distribution — count summary

| # | Prefix | Count | Already prefixed (no-op) | Needs prefix added | ⚠ REVIEW count |
|---|--------|------:|-------------------------:|-------------------:|---------------:|
| 1 | `commerce-` | 31 | 18 | 13 | 1 |
| 2 | `content-` | 8 | 0 | 7 | 0 |
| 3 | `marketing-` | 11 | 0 | 11 | 2 |
| 4 | `media-` | 9 | 0 | 9 | 1 |
| 5 | `finance-` | 11 | 0 | 11 | 0 |
| 6 | `book-` | 8 | 8 | 0 | 0 |
| 7 | `legal-` | 8 | 0 | 8 | 4 |
| 8 | `education-` | 11 | 0 | 11 | 4 |
| 9 | `business-` | 37 | 0 | 37 | 13 |
| 10 | `office-` | 26 | 0 | 26 | 9 |
| 11 | `general-` | 16 | 0 | 16 | 4 |
| **Total** | | **176** | **26** | **149** | **38** |

**Note (added 2026-07-03)**: 2 double-prefix collisions (`media-production`, `content-calendar`) resolved via body-rename — not counted as no-op or simple-prefix-add.

#### §D.9.3 REVIEW — 8 thematic clusters (resolved 2026-07-03: 2 via body-rename in cluster 8, 38 accepted as default across clusters 1-7)

The original 40 ⚠ REVIEW markings fell into 8 thematic clusters. Per user review on 2026-07-03, cluster 8 (double-prefix collisions) was resolved via body-rename, and the remaining 38 REVIEW were accepted as default classification. Clusters are listed below for the audit trail:

1. **Academic-research cluster** (4 skills, default `education-`): `grant-writer`, `paper-search`, `paper-writer`, `research-assistant`. The project router mapped these to `moai-research` (not in AC-015's 9). Default `education-` (academia = teaching + research); alternatives: `book-` (publishing-adjacent) or `general-`.

2. **Regulatory / IP cluster** (4 skills, default `legal-`): `mfds-safety` (Korean FDA compliance lookup), `iros-registry-automation` (corporate registry automation), `patent-analyzer`, `patent-search`. Default `legal-` (regulatory/IP-law framing); alternatives: `office-` (data lookup utility) for mfds-safety / iros-registry-automation, `education-` (research tools) for patents.

3. **Public-data lookup cluster** (4 canonical + 4 stubs = 8 skills, default `office-`): `public-data-court-auction-search`, `public-data-korean-stock-search`, `public-data-public-data`, `public-data-real-estate-search` + stubs `business-real-estate-search`, `data-public-data`, `finance-court-auction-search`, `finance-korean-stock-search`. The project router mapped these to `moai-public-data` (not in AC-015's 9). Default `office-` (data utility); alternatives: distribute by domain (court-auction → `legal-`/`finance-`, stock → `finance-`, real-estate → `finance-`). Stubs may alternatively be DELETED rather than renamed (the user's call).

4. **Personal-productivity cluster** (4 skills, default `office-`): `goal-planner`, `habit-routine`, `retro-builder`, `time-system`. The project router mapped these to `moai-productivity` (not in AC-015's 9). Default `office-` (productivity tools); alternative `general-`.

5. **Lifestyle cluster** (4 skills, default `general-`): `event-planner`, `self-care`, `travel-planner`, `wellness-coach`. The project router mapped these to `moai-lifestyle`. Default `general-` (no AC-015-aligned domain); alternatives: introduce a 12th `lifestyle-` prefix, or `office-` (personal productivity), or split (event-planner → `business-`, others → `general-`).

6. **Business-ambiguous cluster** (13 skills, default `business-`): `draft-response`, `escalation-manager`, `feedback-loop`, `kb-article`, `kr-gov-grant`, `meeting-facilitator`, `negotiation-1on1`, `proposal-writer`, `report-speak`, `roadmap-manager`, `sales-playbook`, `sbiz365-analyst`, `spec-writer`, `ticket-triage`, `ux-designer`, `ux-researcher`. The project router split these into `moai-comms` (4), `moai-support` (4), `moai-sales` (2), `moai-product` (4), `moai-wealth` (1). Default `business-` (broadest fit); alternatives: `general-` (cross-domain), or `marketing-` (for sales-ad-adjacent: `sales-playbook`, `proposal-writer`).

7. **Boundary cases** (5 skills):
   - `personal-branding` (default `marketing-`): alt `business-` (career branding parallels `brand-identity` in business-)
   - `youtube-podcast-planner` (default `marketing-`): alt `content-` (content planning)
   - `notebooklm-slide-prompt` (default `media-`): alt `office-` (slide/prompt tool)
   - `coupang-ad-optimizer` (default `commerce-`): alt `marketing-` (broader ad tools)

8. **Double-prefix naming collisions** (2 skills, RESOLVED 2026-07-03 via body-rename): `media-production` → `media-asset-production`; `content-calendar` → `content-editorial-calendar`. The user selected option (c) body-rename on 2026-07-03 to avoid the awkward literal double-prefix (`media-media-production`, `content-content-calendar`) while preserving the category signal in the body of the new name. Both skills are now counted as body-renames (neither no-op nor simple-prefix-add); see their §D.9.4 rows.

#### §D.9.4 Full rename mapping table (176 rows)

Each row: `| old skill name | new prefixed name | category | rationale (1 short line) |`. Sorted by category, then alphabetical within category. ⚠ REVIEW marks the 40 skills the user should focus on per §D.9.3.

##### commerce- (31 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| commerce-automation-audit | commerce-automation-audit | commerce | already prefixed (no-op) |
| commerce-channel-message | commerce-channel-message | commerce | already prefixed (no-op) |
| commerce-early-fan-builder | commerce-early-fan-builder | commerce | already prefixed (no-op) |
| commerce-influencer-collab | commerce-influencer-collab | commerce | already prefixed (no-op) |
| commerce-integrated-strategy | commerce-integrated-strategy | commerce | already prefixed (no-op) |
| commerce-jtbd-persona | commerce-jtbd-persona | commerce | already prefixed (no-op) |
| commerce-ltv-cac-architect | commerce-ltv-cac-architect | commerce | already prefixed (no-op) |
| commerce-margin-calculator | commerce-margin-calculator | commerce | already prefixed (no-op) |
| commerce-market-research | commerce-market-research | commerce | already prefixed (no-op) |
| commerce-marketing-compliance-kr | commerce-marketing-compliance-kr | commerce | already prefixed (no-op) |
| commerce-morning-brief | commerce-morning-brief | commerce | already prefixed (no-op) |
| commerce-product-image-pipeline | commerce-product-image-pipeline | commerce | already prefixed (no-op) |
| commerce-product-naming | commerce-product-naming | commerce | already prefixed (no-op) |
| commerce-promotion-planner | commerce-promotion-planner | commerce | already prefixed (no-op) |
| commerce-repurchase-timer | commerce-repurchase-timer | commerce | already prefixed (no-op) |
| commerce-season-calendar | commerce-season-calendar | commerce | already prefixed (no-op) |
| commerce-subscription-strategist | commerce-subscription-strategist | commerce | already prefixed (no-op) |
| commerce-voc-triage | commerce-voc-triage | commerce | already prefixed (no-op) |
| coupang-ad-optimizer | commerce-coupang-ad-optimizer | commerce | ⚠ REVIEW — alt `marketing-coupang-ad-optimizer` (broader ad tools) |
| detail-page-copy | commerce-detail-page-copy | commerce | commerce detail-page copy |
| detail-page-image | commerce-detail-page-image | commerce | commerce detail-page image |
| detail-page-planner | commerce-detail-page-planner | commerce | commerce detail-page planner |
| live-commerce | commerce-live-commerce | commerce | live commerce |
| marketplace-coupang | commerce-marketplace-coupang | commerce | coupang marketplace |
| marketplace-coupang-ads | commerce-marketplace-coupang-ads | commerce | coupang ads marketplace |
| marketplace-crowdfunding | commerce-marketplace-crowdfunding | commerce | crowdfunding marketplace |
| marketplace-curation | commerce-marketplace-curation | commerce | curation marketplace |
| marketplace-d2c | commerce-marketplace-d2c | commerce | D2C marketplace |
| marketplace-naver | commerce-marketplace-naver | commerce | naver marketplace |
| product-detail | commerce-product-detail | commerce | product detail page |
| product-photo-brief | commerce-product-photo-brief | commerce | product photo brief |

##### content- (8 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| blog | content-blog | content | blog posting |
| card-news | content-card-news | content | SNS card-news |
| content-calendar | content-editorial-calendar | content | body-rename (approved 2026-07-03): avoids literal double-prefix `content-content-calendar` |
| copywriting | content-copywriting | content | copywriting |
| email-sequence | content-email-sequence | content | email drip sequence |
| newsletter | content-newsletter | content | email newsletter |
| sns-content | content-sns-content | content | SNS content |
| social-media | content-social-media | content | DEPRECATED stub → points to `content-sns-content` |

##### marketing- (11 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| campaign-planner | marketing-campaign-planner | marketing | campaign planning |
| landing-page | marketing-landing-page | marketing | conversion landing page |
| landing-page-conversion-audit | marketing-landing-page-conversion-audit | marketing | landing audit |
| meta-ads-analyzer | marketing-meta-ads-analyzer | marketing | Meta ads analysis |
| meta-ads-manager | marketing-meta-ads-manager | marketing | Meta ads live ops |
| performance-report | marketing-performance-report | marketing | ROAS/performance report |
| personal-branding | marketing-personal-branding | marketing | ⚠ REVIEW — alt `business-personal-branding` (parallels brand-identity) |
| pixel-audit | marketing-pixel-audit | marketing | pixel infra audit |
| seo-audit | marketing-seo-audit | marketing | SEO/GEO audit |
| target-script | marketing-target-script | marketing | target messaging |
| youtube-podcast-planner | marketing-youtube-podcast-planner | marketing | ⚠ REVIEW — alt `content-youtube-podcast-planner` (content planning) |

##### media- (9 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| audio-gen | media-audio-gen | media | audio generation |
| codex-image | media-codex-image | media | codex/gpt-image-2 generation |
| gemini-3-image-prompt | media-gemini-3-image-prompt | media | Gemini image prompt |
| gpt-image-2-prompt | media-gpt-image-2-prompt | media | GPT image prompt |
| higgsfield-image | media-higgsfield-image | media | Higgsfield image |
| higgsfield-video | media-higgsfield-video | media | Higgsfield video |
| media-production | media-asset-production | media | body-rename (approved 2026-07-03): avoids literal double-prefix `media-media-production` |
| midjourney-v8-prompt | media-midjourney-v8-prompt | media | Midjourney prompt |
| notebooklm-slide-prompt | media-notebooklm-slide-prompt | media | ⚠ REVIEW — alt `office-notebooklm-slide-prompt` (slide/prompt tool) |

##### finance- (11 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| close-management | finance-close-management | finance | accounting close |
| econ-literacy | finance-econ-literacy | finance | economic literacy |
| financial-statements | finance-financial-statements | finance | financial statements |
| household-budget | finance-household-budget | finance | household budget |
| insurance-fit | finance-insurance-fit | finance | insurance fit |
| invest-primer | finance-invest-primer | finance | investment primer |
| investor-relations | finance-investor-relations | finance | IR materials |
| personal-tax-saver | finance-personal-tax-saver | finance | personal tax |
| tax-helper | finance-tax-helper | finance | tax helper |
| variance-analysis | finance-variance-analysis | finance | variance analysis |
| wealth-roadmap | finance-wealth-roadmap | finance | personal wealth |

##### book- (8 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| book-author-bio | book-author-bio | book | already prefixed (no-op) |
| book-chapter-writer | book-chapter-writer | book | already prefixed (no-op) |
| book-concept-planner | book-concept-planner | book | already prefixed (no-op) |
| book-outline-designer | book-outline-designer | book | already prefixed (no-op) |
| book-proposal-writer | book-proposal-writer | book | already prefixed (no-op) |
| book-publisher-matcher | book-publisher-matcher | book | already prefixed (no-op) |
| book-revision-coach | book-revision-coach | book | already prefixed (no-op) |
| book-target-reader | book-target-reader | book | already prefixed (no-op) |

##### legal- (8 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| compliance-check | legal-compliance-check | legal | compliance check |
| contract-review | legal-contract-review | legal | contract review |
| iros-registry-automation | legal-iros-registry-automation | legal | ⚠ REVIEW — alt `office-iros-registry-automation` (automation utility) |
| legal-risk | legal-legal-risk | legal | legal risk (literal double "legal" — accepted) |
| mfds-safety | legal-mfds-safety | legal | ⚠ REVIEW — alt `office-mfds-safety` (Korean FDA data lookup) |
| nda-triage | legal-nda-triage | legal | NDA triage |
| patent-analyzer | legal-patent-analyzer | legal | ⚠ REVIEW — alt `education-patent-analyzer` (research tool) |
| patent-search | legal-patent-search | legal | ⚠ REVIEW — alt `education-patent-search` (research tool) |

##### education- (11 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| assessment-creator | education-assessment-creator | education | assessment creation |
| course-followup-sequence | education-course-followup-sequence | education | course followup |
| course-operations-manual | education-course-operations-manual | education | course ops |
| curriculum-designer | education-curriculum-designer | education | curriculum design |
| grant-writer | education-grant-writer | education | ⚠ REVIEW — alt `book-grant-writer` or `general-grant-writer` (R&D grant, no clean AC-015 fit) |
| learning-material | education-learning-material | education | learning material |
| learning-project | education-learning-project | education | learning project |
| paper-search | education-paper-search | education | ⚠ REVIEW — alt `book-paper-search` or `general-paper-search` (academic research) |
| paper-writer | education-paper-writer | education | ⚠ REVIEW — alt `book-paper-writer` or `general-paper-writer` (academic research) |
| research-assistant | education-research-assistant | education | ⚠ REVIEW — alt `book-research-assistant` or `general-research-assistant` (academic research) |
| tutor-research | education-tutor-research | education | tutor research |

##### business- (37 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| brand-identity | business-brand-identity | business | corporate brand (post-Phase B deliverable scope) |
| conflict-handler | business-conflict-handler | business | workplace conflict handling |
| consulting-brief | business-consulting-brief | business | consulting brief |
| draft-offer | business-draft-offer | business | offer letter (HR) |
| draft-response | business-draft-response | business | ⚠ REVIEW — alt `general-draft-response` (CX support) |
| employment-manager | business-employment-manager | business | hiring (HR) |
| escalation-manager | business-escalation-manager | business | ⚠ REVIEW — alt `general-escalation-manager` (CX support) |
| executive-summary | business-executive-summary | business | exec 1-pager (BI) |
| feedback-loop | business-feedback-loop | business | ⚠ REVIEW — alt `general-feedback-loop` (workplace comms) |
| interview-coach | business-interview-coach | business | interview prep (career) |
| job-analyzer | business-job-analyzer | business | JD analysis (career) |
| kb-article | business-kb-article | business | ⚠ REVIEW — alt `general-kb-article` (CX knowledge base) |
| kr-gov-grant | business-kr-gov-grant | business | ⚠ REVIEW — alt `finance-kr-gov-grant` (gov financial support) |
| market-analyst | business-market-analyst | business | market analysis (BI) |
| meeting-facilitator | business-meeting-facilitator | business | ⚠ REVIEW — alt `general-meeting-facilitator` (workplace comms) |
| negotiation-1on1 | business-negotiation-1on1 | business | ⚠ REVIEW — alt `general-negotiation-1on1` (workplace comms) |
| people-operations | business-people-operations | business | HR ops |
| performance-review | business-performance-review | business | perf review (HR) |
| pm-weekly-report | business-pm-weekly-report | business | PM weekly report |
| portfolio-guide | business-portfolio-guide | business | portfolio (career) |
| process-manager | business-process-manager | business | process ops |
| productivity-weekly-report | business-productivity-weekly-report | business | weekly status report |
| proposal-writer | business-proposal-writer | business | ⚠ REVIEW — alt `marketing-proposal-writer` (B2B sales) |
| report-speak | business-report-speak | business | ⚠ REVIEW — alt `general-report-speak` (workplace comms) |
| resume-builder | business-resume-builder | business | resume (career) |
| resume-screener | business-resume-screener | business | resume screening (HR) |
| roadmap-manager | business-roadmap-manager | business | ⚠ REVIEW — alt `general-roadmap-manager` (product mgmt) |
| sales-playbook | business-sales-playbook | business | ⚠ REVIEW — alt `marketing-sales-playbook` (B2B sales) |
| sbiz365-analyst | business-sbiz365-analyst | business | ⚠ REVIEW — alt `finance-sbiz365-analyst` or `commerce-sbiz365-analyst` (commercial-area analysis) |
| spec-writer | business-spec-writer | business | ⚠ REVIEW — alt `general-spec-writer` (product mgmt) |
| startup-launchpad | business-startup-launchpad | business | startup strategy |
| status-reporter | business-status-reporter | business | status reporting |
| strategy-planner | business-strategy-planner | business | strategy |
| ticket-triage | business-ticket-triage | business | ⚠ REVIEW — alt `general-ticket-triage` (CX support) |
| ux-designer | business-ux-designer | business | ⚠ REVIEW — alt `general-ux-designer` (product mgmt) |
| ux-researcher | business-ux-researcher | business | ⚠ REVIEW — alt `general-ux-researcher` (product mgmt) |
| vendor-manager | business-vendor-manager | business | vendor management (ops) |

##### office- (26 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| business-real-estate-search | office-business-real-estate-search | office | RELOCATED stub → points to `office-public-data-real-estate-search`; ⚠ REVIEW — alt delete stub |
| daily-briefing | office-daily-briefing | office | daily news briefing |
| data-explorer | office-data-explorer | office | CSV/Excel profiling |
| data-public-data | office-data-public-data | office | RELOCATED stub → points to `office-public-data-public-data`; ⚠ REVIEW — alt delete stub |
| data-visualizer | office-data-visualizer | office | data visualization |
| design-system-library | office-design-system-library | office | post-Phase B pointer to moai-design canonical |
| docx-generator | office-docx-generator | office | .docx generator |
| finance-court-auction-search | office-finance-court-auction-search | office | RELOCATED stub → points to `office-public-data-court-auction-search`; ⚠ REVIEW — alt `legal-finance-court-auction-search`, or delete stub |
| finance-korean-stock-search | office-finance-korean-stock-search | office | RELOCATED stub → points to `office-public-data-korean-stock-search`; ⚠ REVIEW — alt `finance-finance-korean-stock-search`, or delete stub |
| goal-planner | office-goal-planner | office | ⚠ REVIEW — alt `general-goal-planner` (personal productivity) |
| habit-routine | office-habit-routine | office | ⚠ REVIEW — alt `general-habit-routine` (personal productivity) |
| html-report | office-html-report | office | single-file HTML report |
| html-slide | office-html-slide | office | single-file HTML slide deck |
| hwpx-writer | office-hwpx-writer | office | .hwpx writer |
| korean-spell-check | office-korean-spell-check | office | Korean spell check |
| mcp-connector-setup | office-mcp-connector-setup | office | MCP connector setup (task hint: residual; classified office- as productivity tooling — ⚠ REVIEW alt `general-`) |
| notion-template-kit | office-notion-template-kit | office | Notion template design |
| pdf-writer | office-pdf-writer | office | PDF writer |
| pptx-designer | office-pptx-designer | office | .pptx designer |
| public-data-court-auction-search | office-public-data-court-auction-search | office | ⚠ REVIEW — alt `legal-public-data-court-auction-search` or `finance-public-data-court-auction-search` |
| public-data-korean-stock-search | office-public-data-korean-stock-search | office | ⚠ REVIEW — alt `finance-public-data-korean-stock-search` |
| public-data-public-data | office-public-data-public-data | office | generic public-data lookup |
| public-data-real-estate-search | office-public-data-real-estate-search | office | ⚠ REVIEW — alt `finance-public-data-real-estate-search` |
| retro-builder | office-retro-builder | office | ⚠ REVIEW — alt `general-retro-builder` (personal productivity) |
| time-system | office-time-system | office | ⚠ REVIEW — alt `general-time-system` (personal productivity) |
| xlsx-creator | office-xlsx-creator | office | .xlsx creator |

##### general- (16 skills)

| old skill name | new prefixed name | category | rationale |
|----------------|-------------------|----------|-----------|
| ai-diagnostic | general-ai-diagnostic | general | multi-dimensional AI diagnostic (meta tooling) |
| ai-slop-reviewer | general-ai-slop-reviewer | general | Korean-slop gate |
| cd-brief | general-cd-brief | general | Claude Design 6-element brief builder (tooling) |
| cd-handoff-reader | general-cd-handoff-reader | general | Claude Design handoff reader (tooling) |
| cd-prompt-builder | general-cd-prompt-builder | general | Claude Design senior UX prompt builder (tooling) |
| cd-slop-check | general-cd-slop-check | general | Claude Design copy slop gate |
| cd-system-prep | general-cd-system-prep | general | Claude Design DESIGN.md synthesizer (tooling) |
| event-planner | general-event-planner | general | ⚠ REVIEW — alt `business-event-planner`, or 12th `lifestyle-` prefix (per §D.9.3 cluster 5) |
| feedback | general-feedback | general | project feedback / GitHub issue filer (meta) |
| humanize-korean | general-humanize-korean | general | Korean naturalization gate |
| self-care | general-self-care | general | ⚠ REVIEW — alt 12th `lifestyle-` prefix (per §D.9.3 cluster 5) |
| skill-builder | general-skill-builder | general | skill authoring (meta) |
| skill-template | general-skill-template | general | skill template (meta) |
| skill-tester | general-skill-tester | general | skill testing (meta) |
| travel-planner | general-travel-planner | general | ⚠ REVIEW — alt `office-travel-planner`, or 12th `lifestyle-` prefix (per §D.9.3 cluster 5) |
| wellness-coach | general-wellness-coach | general | ⚠ REVIEW — alt 12th `lifestyle-` prefix (per §D.9.3 cluster 5) |

#### §D.9.5 Verification recipe (informational; the binding predicate is AC-REM-018)

Once the user approves this mapping, the run-phase rename script iterates the table and applies the rename. AC-REM-018 then runs the dangling-reference grep per old-name. For a no-op row (e.g. `commerce-automation-audit` → `commerce-automation-audit`), the grep finds 0 references to the OLD form which equals the NEW form — but the grep is still valid because it would catch a stale reference written before the rename pass (none should exist for no-ops, but the grep is a safety net). For all non-no-op rows, the grep is the primary integrity check.

**Note on EC-7 (`project` router)**: the `project/SKILL.md` skill is EXCLUDED from this rename (it is not listed in any §D.9.4 sub-table). The router's category-routing text mentions skill names; any reference in the router to a renamed skill MUST be updated as part of the rename script's full-tree sweep — AC-REM-018's grep covers `plugins/moai-cowork` which includes `plugins/moai-cowork/skills/project/SKILL.md`.

**Note on canonical design targets**: `design-system-library` (post-Phase B pointer) and the cd-* family reference design-side skills (e.g. `moai-design:design-system-library`). Those cross-plugin references are NOT in scope for the rename (Phase A is cowork-only per REQ-018), but AC-018's grep will surface them — they are legitimate cross-plugin pointers (using `moai-design:` prefix) not dangling references, and the run-phase reviewer MUST distinguish them from real dangling refs.

