# Progress — SPEC-MOC-PM-ADVISORS-001

## §E.1 Plan-phase Audit-Ready Signal

- 2026-07-10: plan-phase artifact set authored by manager-spec (Tier L: spec.md, plan.md, design.md, acceptance.md, progress.md). Frontmatter `status: draft` across artifacts. SPEC ID self-check: `SPEC-MOC-PM-ADVISORS-001` → regex PASS. Design decisions FINAL per 2-round Socratic interview; open design risks recorded in plan.md (7 items), unresolved by design.
- 2026-07-10 (iter-2, version 0.2.0): plan-auditor FAIL 0.74 remediation. Re-baselined §A against the committed `e06086c` 18-plugin / marketplace v6.2.0 tree (working tree CLEAN). Fixes F1-F7 applied: F1 HARD-gate `^## .*\(HARD\)` fixed literal baseline 8 (source `[HARD]`=0, `(HARD)`=8 at lines 17,28,38,47,68,77,86,135); F2 English-anchor/conversation_language prose split declared (design §A.1, REQ-X-001); F3 AC-PMA-004 mechanized + AC-PMA-004b negative gate; F4 line-budget overflow policy migrated to REQ-G-005b + design §D + AC-PMA-005b (old open-risk #4 deleted); F5 `/moai project` vs `/moai --project` disambiguation (REQ-M-008) + 7-subcommand migration table (REQ-M-009, design §F.1) + AC-PMA-017/018; F6 traceability AC-PMA-019/020/021/022 for REQ-G-007/M-003/M-004/M-007; F7 `//project`→`/project`. Drift #4 verified RESOLVED (owner `moai-story`, 0 stale prefixes). AC set now 21 machine + 3 structural. Open design risks reduced to 6 (was 7).

## §F Phase 0.95 Mode Selection

- Date: 2026-07-11. Inputs: tier=L, scope ~30+ files but non-uniform semantic authoring (skill bodies, reference migration with in-flight drift fixes), domains=3 (goose skill / moai skill / docs+marketplace), language mix = markdown/JSON, concurrency benefit = LOW (authoring-heavy; M2∥M3 disjoint but sequential single agent is safe), Agent Teams prereqs NOT met.
- Mode evaluation: trivial NO / background NO (writes) / agent-team NO (gate fails) / parallel NO (authoring-heavy) / workflow NO (non-uniform transforms, disposition dependencies) / **sub-agent SELECTED**.
- Decision: sub-agent
- Justification: Verification-first M1 gates M2-M6; single sequential manager-develop (cycle_type=tdd, model=sonnet, effort=xhigh per plan.md §A). Run-gate re-audit this session: PASS 0.87 (report: .moai/reports/plan-audit/SPEC-MOC-PM-ADVISORS-001-2026-07-11.md). Implementation Kickoff Approval: obtained prior session (sequential SPEC-2→SPEC-1, sonnet xhigh; session 02e7a29f); SPEC-2 completed at 5b8a214.
- **D1 scope exception (orchestrator decision, pre-M5)**: M5 MAY additionally bump `plugins/moai/.claude-plugin/plugin.json` `.version` to match the `moai` marketplace entry (1.1.0) in lockstep — a 1-line version-field edit only, per the sibling SPEC-MOC-CODER-LSP-MCP-001 M6 handoff expectation. This documented authorization supersedes the plan.md §D "no other plugin source directories" clause for this single field; any other plugins/moai/** edit remains forbidden.

## §E.2 Run-phase Evidence

### M1 — Pre-flight capture (2026-07-11)

**Worktree note**: run-phase executed inside an isolated Claude Code worktree (`.claude/worktrees/agent-ae94631d2a4fe0329`). `.moai/specs/` is gitignored and was copied in from the main checkout at session start; final commits happen in the worktree branch and this progress.md (plus spec.md frontmatter) is copied back to the main checkout at session end per the worktree-note protocol in the delegation prompt.

**Drift item 1 re-grep** (`grep -rn "4-plugin\|4-플러그인\|27-플러그인" plugins/moai-pm/skills/project/references/core/`): confirmed ACTIVE in 5 files — `INDEX.md` (lines 5,8,9,20,103,105,131), `designer-setup.md` (line 3), `cowork-setup.md` (line 3), `coder-setup.md` (line 3), `init-protocol.md` (lines 315,335). `router.md` confirmed CLEAN (grep exit=1, 0 matches) — already fixed by `e06086c`, matches plan.md §B. Additionally observed (not the exact tracked pattern but same drift-1 class, fixed during migration as REQ-R-002 substance): `diagnostic-protocol.md` carried stale "27 화이트리스트"/"4 플러그인 / 234 스킬" hardcoded prose; `init-protocol.md:329` skill→plugin ownership table attributed `story-*`/`book-*` to `moai-coworker` instead of `moai-story` (drift-1 + drift-4 overlap) — both fixed in migrated goose content (M2).

**Drift item 2 re-grep** (`grep -n "Self-Refine\|self-refine\|metrics.csv" evolution-protocol.md`): confirmed ACTIVE — 7 hits at lines 5,9,76,99,102,272,286 (heavy Self-Refine model: self-refine-log.md, metrics.csv, forced scoring). `SKILL.md:146` confirmed as the CURRENT simplified model (`## 재귀적 자가 개선 (HARD)`). Migration policy applied at M2: DROP `evolution-protocol.md` entirely (per design.md §C); simplified model authored directly in goose SKILL.md.

**Drift item 3 re-grep** (`grep -c 에이전트 cowork-setup.md`): confirmed `0` matches — cowork-setup.md's 8-Phase summary (line 54) had Phase 7 = API 키 (line 65), zero custom-agent-generation mentions. `SKILL.md:123,135` confirmed as carrying the custom-agent generation phase (`## 커스텀 에이전트 생성 (--cowork Phase 7)`). Migration policy applied at M2: restored custom-agent generation as first-class Phase 7 in goose's `cowork-setup.md` successor.

**Drift item 4 re-verify** (`grep -rn "moai-coworker:story-\|moai-coworker:book-" plugins/moai-pm/skills/project/`): confirmed `0` matches (exit=1) — RESOLVED, no regression. `cowork-setup.md:124` confirmed citing `moai-story:story-project` correctly (preserved verbatim in M2 migration).

**HARD-block baseline**: `grep -cE '^## .*\(HARD\)' plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl` → **8** (FIXED literal baseline for AC-PMA-005). Bracket form `grep -c '\[HARD\]'` → `0` (confirms parenthesized form only, per plan.md §C step 2 warning). Exact lines: 17 (`## 2. 행동 원칙`), 28 (`## 3. 요청 평가 사다리`), 38 (`## 4. 파일 생성 기준`), 47 (`## 5. 문서·콘텐츠 생성 우선순위`), 68 (`## 6. AI 슬롭 후처리`), 77 (`## 7. 인용·저작권 가드`), 86 (`## 8. 톤 규칙`), 135 (`## 14. 맥락 적용 규칙`). Re-verified against the M2-produced `skills/goose/references/templates/CLAUDE.md.tmpl` after generation: also exactly 8, same lines shifted by -2 (no attribution comment lines) → 15,26,36,45,66,75,84,133.

**Marketplace baseline**: `.metadata.version` = `6.2.0`; `moai-pm` entry `.version` = `0.4.0` (M5 bump baseline, AC-PMA-009); `moai` entry `.version` = `1.0.0` (M5 bumps to `1.1.0` per sibling SPEC-MOC-CODER-LSP-MCP-001 M6 handoff, confirmed in that SPEC's progress.md line 117); 18 total plugin entries confirmed. `plugins/moai/.claude-plugin/plugin.json` `.version` = `1.0.0` (D1 lockstep bump target); `plugins/moai-pm/.claude-plugin/plugin.json` `.version` = `0.4.0` (M5 bump target, kept in sync with marketplace.json moai-pm entry).

**`/goose` command-name collision scan**: `grep -rln "^/goose\|'goose'\|\"goose\""` across `plugins/*/skills/*/SKILL.md` and `plugins/*/commands/*.md`, plus `find plugins -iname "*goose*"` → **zero matches**. `/goose` confirmed free.

**Sibling catalog confirmation** (SPEC-MOC-CODER-LSP-MCP-001 interface, design.md §H): `plugins/moai/references/dev-mcp-catalog.json` EXISTS, `$schema_version` = `"1.0.0"`, 6 servers (`playwright`, `supabase`, `vercel`, `neon`, `railway`, `claude-in-chrome`). `claude-in-chrome` entry confirmed `entry_type: "guidance-only"`, `transport: "none"` — no `.mcp.json` server entry generated for it (D2 constraint honored in M3 moai skill authoring — see §MCP Survey and `mcp-fallback-summary.md`).

**Interview grade A/B/C semantics re-verify** (open risk #5/#6): confirmed in `context-collector.md` §1 — A등급(필수, CLAUDE.md immediate), B등급(핵심, 80%+ recommended, Phase 1 interview + targeted AskUserQuestion), C등급(보강, deep interview). Matches design.md §B grade definitions. No drift — semantics migrated verbatim into goose's `context-collector.md` and summarized in both SKILL.md files.

**Anti-slop chain presence scan** (for AC-PMA-016): confirmed present in `execution-protocol.md`, `INDEX.md`, `claudemd-generator.md`, `cowork-setup.md`, `coder-setup.md`, `quality-evaluator.md`, `diagnostic-protocol.md`, `init-protocol.md`. All migrated into goose (except coder-setup.md → moai, which does not carry ai-slop chain content — dev-project scaffolding has no text-content chain to review).

**Disposition matrix frozen** (design.md §C, no deviations found during migration): router.md → split goose+moai; cowork-setup.md → goose; designer-setup.md → goose; coder-setup.md → moai; init-protocol.md → split goose(primary)+moai(dev-init); execution-protocol.md → split goose(primary)+moai(handoff); context-collector.md → goose only (moai embeds a condensed A/B/C summary directly in SKILL.md instead of a separate copy — "copy if needed" judged not needed given moai's narrower interview scope); claudemd-generator.md → both variants (goose Desktop full generator; moai dev variant documents two-template separation + delegation, since moai's actual CLAUDE.md generation is delegated to the coder plugin's own `moai-workflow-project`); evolution-protocol.md → DROP; evaluation-protocol.md → goose; quality-evaluator.md → goose; diagnostic-protocol.md → goose; INDEX.md → regenerate per skill (2 fresh INDEX.md files, goose + moai); CLAUDE.md.tmpl → both variants (moai has no separate tmpl file — see claudemd-generator.md rationale above).

### M2 — Goose skill build (2026-07-11)

13 files created under `plugins/moai-pm/skills/goose/`: `SKILL.md` (6 canonical H2 anchors in exact order — verified via S1 grep, see §E.3 evidence) + 11 `references/*.md` + `references/templates/CLAUDE.md.tmpl`. Drift fixed in-flight (not copy-then-fix): heavy Self-Refine model dropped (`evolution-protocol.md` not migrated per design.md §C); custom-agent generation restored as Phase 7 in `cowork-setup.md` successor; all 4-plugin/27-plugin remnants rewritten against live marketplace.json roster (no hardcoded counts); `diagnostic-protocol.md` stale "27 화이트리스트"/"4 플러그인 / 234 스킬" hardcodes replaced with roster citations. Commit: `f98b010`.

### M3 — MoAI skill build (2026-07-11)

8 files created under `plugins/moai-pm/skills/moai/`: `SKILL.md` (5 canonical H2 anchors in exact order — verified via S2 grep) + 6 `references/*.md`. REQ-M-008 disambiguation table + REQ-M-009 legacy-subcommand pointer to design.md §F.1 both present. `mcp-fallback-summary.md` implements REQ-M-006 embedded fallback (static 6-server snapshot, explicitly flagged inside the file as a driftable copy per plan.md open risk #1). Commit: `a02314a`.

### M4 — Legacy removal + integrity sweep (2026-07-11)

`plugins/moai-pm/skills/project/` removed in full (15 tracked files: SKILL.md + 13 `references/core/*.md` + `templates/CLAUDE.md.tmpl`). No stray `.claude/agent-memory/` or `.moai/state/` runtime-artifact directories were present under `skills/project/` in this worktree checkout (gitignored, untracked here — the main-checkout stray dirs noted in the delegation prompt Section A require a direct `rm -rf` outside git-tracked scope; see Residual Risk in §E.3). Repo-wide sweep of `plugins/moai-pm/` for all 4 tracked drift patterns after removal: 0 matches (`grep -rn "4-plugin\|4-플러그인\|27-플러그인\|27 화이트리스트\|Self-Refine\|self-refine\|metrics.csv\|moai-coworker:story-\|moai-coworker:book-" plugins/moai-pm/` → exit 1, no output). Commit: `8f3b13a`.

### M5 — Docs (2026-07-11)

- **README.md rewrite** (`plugins/moai-pm/README.md`): full rewrite as 2-skill entry (goose + moai), 18-plugin roster table with per-employee entry-skill column, command-surface disambiguation callout, self-improvement section, per-skill artifact tables. AC-PMA-008 verified PASS (both `/goose` and `--project` present).
- **marketplace.json version bumps** (D1 scope exception, single cross-SPEC owner per design.md §H F12): `moai-pm` entry `0.4.0 → 1.0.0` (MAJOR — breaking invocation-surface change: `/project` retired, replaced by `/goose --project` + `/moai --project`); `moai` entry `1.0.0 → 1.1.0` (MINOR, per sibling SPEC-MOC-CODER-LSP-MCP-001 M6 handoff — additive LSP/MCP/hook capability, zero breaking changes, confirmed in that SPEC's progress.md line 117). Top-level `metadata.description` stale `/project --cowork/--code` sentence also corrected (same file, same drift-fix spirit as REQ-R-002) — narrow single-sentence edit, no other metadata fields touched.
- **plugin.json lockstep** (D1 exception, per plan.md §F Mode Selection D1 note): `plugins/moai-pm/.claude-plugin/plugin.json` `0.4.0 → 1.0.0` + stale description sentence fixed in lockstep with README/marketplace; `plugins/moai/.claude-plugin/plugin.json` `1.0.0 → 1.1.0` (version field only — no other `plugins/moai/**` file touched, per the D1 authorization scope).
- All 3 JSON files (`marketplace.json`, both `plugin.json`) validated via `jq empty` — PASS.
- **www guide target-path list** (REQ-D-003 — run-phase records only, no `www/**` edits performed): a `grep -rl` sweep for `project --cowork|project --code|moai-pm.*project|/project resume|/project catalog` plus a broader `moai-pm`/`/project ` sweep identified the following living-doc targets for sync-phase update (historical `www/content/releases/*.md` point-in-time snapshots excluded — those describe past states and should NOT be retroactively rewritten):
  1. `www/content/plugins/_index.md:64` — `moai-pm` roster row cites `/project` command
  2. `www/content/plugins/teams.md:73,76` — describes `/project` command + install snippet
  3. `www/content/agent-teams/pm.md:4,25,31` — frontmatter description cites `/project` + "12개 AI 직원" (stale count, pre-18-plugin)
  4. `www/content/cowork/plugins.md:46` — references `/project init`
  5. `www/content/cowork/skills.md:115` — slash-command example table cites `/project init`
  6. `www/content/getting-started/first-task.md:64` — moai-pm role table row
  7. `www/content/getting-started/quick-start.md:16,27,51` — onboarding walkthrough cites `/project init` (delivery-app analogy, 3 occurrences)
  8. `www/data/agent_teams.json:99,193,1439` — skill catalog JSON entries reference `/project feedback`, `moai-coworker` "`/project` 역할", and the `moai-pm` id block
- **Legacy SPEC frontmatter note** (out of run-phase scope per spec.md §E "Out of Scope — Legacy SPEC frontmatter edits"): SPEC-MOC-PM-REDESIGN-001 should receive a `partially_superseded_by: [SPEC-MOC-PM-ADVISORS-001]` frontmatter addition at sync-phase — recorded here as a manager-docs task pointer only, not performed in run-phase.

## §E.3 Run-phase Audit-Ready Signal

### M6 — Self-verification batch (2026-07-11)

**AC matrix — 21/21 machine gates PASS + 3/3 structural reviews cited + 4/4 Given-When-Then scenarios PASS.** Every command below was actually executed against this run's tree; verbatim output/exit-status persisted at `.moai/state/verify/SPEC-MOC-PM-ADVISORS-001/ac-*.log` (also `s1-s4.log`).

| AC | Status | Command | Actual Output |
|----|--------|---------|----------------|
| AC-PMA-001 | PASS | `test -f goose/SKILL.md && test -f moai/SKILL.md && test ! -e project` | `PASS` |
| AC-PMA-002 | PASS | `grep -rn "metrics.csv\|Self-Refine\|self-refine" plugins/moai-pm/` | exit=1 (no matches) |
| AC-PMA-003 | PASS | `grep -rn "moai-coworker:story-\|moai-coworker:book-" plugins/moai-pm/` | exit=1 (no matches) |
| AC-PMA-004 | PASS | heading + 3-class grep on goose/SKILL.md | `PASS` (no MISSING lines) |
| AC-PMA-004b | PASS | `.lsp.json\|hooks/` count on goose SKILL.md + claudemd-generator.md | `0` |
| AC-PMA-005 | PASS | `grep -cE '^## .*\(HARD\)' goose/references/templates/CLAUDE.md.tmpl` | `8` → `PASS` |
| AC-PMA-005b | PASS | 4-clause budget/chain/shrink/NFR grep on goose claudemd-generator.md | `PASS` |
| AC-PMA-006 | PASS | 4 trigger tokens on goose SKILL.md | no MISSING lines |
| AC-PMA-007 | PASS | `moai-pm:moai` + `moai:moai` on moai SKILL.md | `PASS` |
| AC-PMA-008 | PASS | `/goose` + `--project` on README.md | `PASS` |
| AC-PMA-009 | PASS | `jq -r '.plugins[] \| select(.name=="moai-pm") \| .version'` | `1.0.0` ≠ M1 baseline `0.4.0` |
| AC-PMA-010 | PASS | `grep -c "www/" progress.md` | `9` ≥ 1 |
| AC-PMA-011 | PASS | broken-link scan on both SKILL.md | no BROKEN lines (no markdown-link-form refs used — plain-text reference tables instead, so the regex matches 0 candidates, vacuously satisfying "no BROKEN lines") |
| AC-PMA-012 | PASS | `conversation_language` + `AskUserQuestion` on both SKILL.md | no MISSING lines |
| AC-PMA-013 | PASS | re-run of all 4 M1-captured drift patterns against `plugins/moai-pm/` | all 4 patterns exit=1 (no matches) |
| AC-PMA-017 | PASS | 7-subcommand row scan on design.md §F.1 | no MISSING lines |
| AC-PMA-018 | PASS | `/moai project` + `/moai --project` + `Skill("moai:moai")` on moai SKILL.md | `PASS` |
| AC-PMA-019 | PASS | CLAUDE.md + .claude/agents + 최대 3 on goose SKILL.md | `PASS` |
| AC-PMA-020 | PASS | 6 generation-target classes on moai SKILL.md | no MISSING lines |
| AC-PMA-021 | PASS | `## LSP Presence Check` heading + `LSP` on moai SKILL.md | `PASS` |
| AC-PMA-022 | PASS | `Claude Code (runtime\|런타임)` on moai SKILL.md | `PASS` |

**Structural-review ACs (014-016)**, file+section citations:

- **AC-PMA-014** (REQ-G-004, user-custom agents never prebuilt copies): `goose/SKILL.md` §Custom Agent & Skill-Chain Design, verbatim: "프리빌트 플러그인 에이전트를 복사하지 않는다 — 인벤토리에서 발견한 스킬을 체인으로 호출하는 에이전트 본문을 인터뷰 맥락에서 직접 합성한다."
- **AC-PMA-015** (REQ-R-004, Phase 7 restored): `goose/references/cowork-setup.md` §2 8-Phase table, row "7 커스텀 에이전트 생성" + workflow diagram line 51 both confirm Phase 7 = custom-agent generation (was API-key-only pre-migration).
- **AC-PMA-016** (REQ-X-003, anti-slop chain preserved): all 8 M1-identified source files with `ai-slop`/`AI 슬롭`/`humanize` content have their content preserved in the goose migration destination (`claudemd-generator.md`, `cowork-setup.md`, `diagnostic-protocol.md`, `execution-protocol.md`, `init-protocol.md`, `quality-evaluator.md`, `templates/CLAUDE.md.tmpl`, plus `SKILL.md` itself); `INDEX.md` was intentionally regenerated fresh (disposition matrix) rather than carrying old content verbatim; `moai/references/coder-setup.md` correctly carries only a contextual explanatory mention (not an actual chain mandate), consistent with the M1 note that dev-project scaffolding has no text-content ai-slop chain.

**Given-When-Then scenarios (all 4 PASS)**:

- **S1** (goose canonical flow order): 6 anchors extracted in exact order at lines 38/60/77/95/105/122 — matches design.md §A.1 order exactly.
- **S2** (moai degraded mode): `grep -q "fallback"` on moai SKILL.md → PASS (§Namespace & Routing documents both coder-installed and coder-absent branches, fallback never attempts execution routing).
- **S3** (re-invocation/overwrite confirmation): both SKILL.md files document explicit re-invocation confirmation (goose §Socratic Interview "재진입 확인 (S3)"; moai §Socratic Interview & Stack Detection "재진입 확인 (S3)" + execution-protocol.md §3).
- **S4** (interview stalls at grade C): goose §Socratic Interview "등급 C 정체 시 (S4)" documents both the block-and-ask path (high-risk) and the document-assumptions-and-proceed path (low-risk, into `.moai/context.md`).

**Write-scope verification**: `git diff --name-only 5b8a214..HEAD` → 39 files, every path under `plugins/moai-pm/**`, `.claude-plugin/marketplace.json`, or the single D1-exception file `plugins/moai/.claude-plugin/plugin.json` (1-line version field only). Zero `www/**` edits, zero other-SPEC-directory edits, zero unscoped `plugins/moai/**` edits. `git status --porcelain` → empty (clean tree, everything committed).

**Commit SHA list**: `f98b010` (M1+M2), `a02314a` (M3), `8f3b13a` (M4), `0539fd6` (M5). All Conventional Commits format with `🗿 MoAI` trailer, no `--no-verify` used.

**Open design risks (plan.md §Open design risks, 6 items) — run-phase status**:

1. **Catalog fallback drift** — STILL OPEN by design. `moai/references/mcp-fallback-summary.md` explicitly documents itself as a driftable copy with no automated sync mechanism; this is a known, flagged limitation carried to sync report (no code/doc claims otherwise).
2. **`/goose` name collision** — RESOLVED. M1 scan confirmed zero pre-existing `/goose` references across the plugin family; name is free and now claimed by this SPEC.
3. **`/moai` short-form dispatch ambiguity** — STILL OPEN (as plan.md anticipated — mitigated, not eliminated). `moai/SKILL.md` §Namespace & Routing documents explicit-namespace resolution (`moai-pm:moai` vs `moai:moai`); platform-defined short-form dispatch order remains outside this SPEC's control.
4. **Shared-reference duplication** — REALIZED AS DESIGNED (accepted risk, not a defect). Per-skill copies exist for `router.md`, `init-protocol.md`, `execution-protocol.md`, `claudemd-generator.md` — content is adapted per-skill (not verbatim duplicates) but both skills must be kept in sync manually on future changes; carried to sync report as a maintenance note.
5. **Interview grade model drift** — RESOLVED. M1 re-verified A/B/C semantics against the pre-migration `SKILL.md`/`context-collector.md`; no drift found; migrated verbatim into `goose/references/context-collector.md` and summarized consistently in both SKILL.md files.
6. **Live plugin-family churn** — MITIGATED BY DESIGN (built-in, not eliminated). Every migrated reference cites `.claude-plugin/marketplace.json` as roster authority instead of hardcoding counts (verified via AC-PMA-013's drift-pattern re-run); a family change after this commit could still race documentation prose, but no reference in this SPEC's output will itself go stale on a roster change.

**Residual risk (not in plan.md's 6, discovered at M1/M4)**: stray `.claude/agent-memory/` and `.moai/state/` runtime-artifact directories were noted in the delegation prompt as present under the MAIN CHECKOUT's `skills/project/` (not this worktree's checkout, where they were gitignored-absent). Since `skills/project/` is now fully deleted in this SPEC's commits, those stray directories become orphaned once this branch is merged/pushed to the main checkout — they should be removed by a direct `rm -rf` on the main checkout as a non-git-tracked cleanup step (outside this SPEC's commit scope, since they were never git-tracked to begin with).

run_complete_at: 2026-07-11
run_status: complete
ac_pass_count: 21
ac_fail_count: 0
preserve_list_post_run_count: n/a (Tier L authoring SPEC, no PRESERVE list in plan.md §D beyond write-scope enumeration)
new_warnings_or_lints_introduced: n/a (markdown/JSON-only SPEC, no lint/build toolchain applicable)
total_run_phase_files: 39 (git diff --name-only count, includes 15 deletions)
m1_to_mN_commit_strategy: per-milestone separate commits (M1+M2 combined since M1 produced no git-tracked changes; M3/M4/M5 individually)

## §E.4 Sync-phase Audit-Ready Signal

### Sync scope (Route A — Hybrid Trunk, single sync commit direct to main, NO PR)

Standard scope per user approval. Deliverables: CHANGELOG `[Unreleased]` entry, frontmatter 3-phase close on all 4 artifacts, REQ-D-003 www handoff record (below), SPEC-MOC-PM-REDESIGN-001 partial-supersession frontmatter.

**Tracked-file reality note (deviation from delegation premise)**: the delegation prompt stated "only CHANGELOG.md is tracked". Observed reality: `.moai/specs/SPEC-MOC-PM-REDESIGN-001/spec.md` **is git-tracked** (force-added historically, as are SPEC-MOC-BOOTSTRAP-DESKTOP-001 / SPEC-MOC-PLUGIN-MOAI-V2-001 / SPEC-MOC-PLUGIN-REMEDIATION-001), while this SPEC's own directory has 0 tracked files (genuinely gitignored). The authorized one-line `partially_superseded_by` edit was therefore included in the sync commit rather than left as a dangling working-tree edit. Sync commit touches exactly 2 files, both within the authorized write scope.

### B12 CHANGELOG emission self-test (3/3 PASS)

1. **Pre-emission grep**: `grep -c '^### Added — SPEC-MOC-PM-ADVISORS-001' CHANGELOG.md` → `0` (no duplicate entry). The 1 pre-existing `SPEC-MOC-PM-ADVISORS-001` string match was a cross-reference inside the sibling SPEC-MOC-CODER-LSP-MCP-001 `**Residual**` line (line 30), not an entry heading — emission cleared.
2. **AC count match**: `acceptance.md` SSOT = 21 machine gates (AC-PMA-001..013 incl. 004b/005b, 017..022) + 3 structural (014..016) = 24 total. CHANGELOG entry states "21/21 machine-gate AC PASS + 3/3 structural-review AC cited + 4/4 Given-When-Then scenarios PASS (24 AC total)" — matches SSOT.
3. **File path verification**: every path claimed in the CHANGELOG entry verified via `find`/`ls`/`jq` before commit — goose 13 files, moai 8 files, `skills/project/` absent, README 157 lines, marketplace `moai-pm=1.0.0` / `moai=1.1.0`, both `plugin.json` at 1.0.0 / 1.1.0. Zero claimed-not-observed paths.

### Frontmatter status transitions (in-progress → implemented → completed, merged on the single sync commit)

| Artifact | status (pre) | status (post) | updated |
|----------|--------------|---------------|---------|
| spec.md | in-progress | **completed** | 2026-07-11 |
| plan.md | draft | **completed** | 2026-07-11 |
| design.md | draft | **completed** | 2026-07-11 |
| acceptance.md | draft | **completed** | 2026-07-11 |

`updated:` was already `2026-07-11` on all 4 (run-phase date == sync-phase date) — no date change required. Zero body-content modifications (manager-docs ownership boundary honored).

### REQ-D-003 — www guide target-path handoff (sync → follow-up)

The 8 living-doc targets below were identified at run-phase M5 (`grep -rl` sweep; §E.2). **No `www/**` edits were performed in run-phase or sync-phase** — this list is the handoff record for a follow-up SPEC or docs pass. Historical `www/content/releases/*.md` point-in-time snapshots are deliberately EXCLUDED (they describe past states and must not be retroactively rewritten).

1. `www/content/plugins/_index.md:64` — `moai-pm` roster row cites `/project` command
2. `www/content/plugins/teams.md:73,76` — describes `/project` command + install snippet
3. `www/content/agent-teams/pm.md:4,25,31` — frontmatter description cites `/project` + "12개 AI 직원" (stale count, pre-18-plugin)
4. `www/content/cowork/plugins.md:46` — references `/project init`
5. `www/content/cowork/skills.md:115` — slash-command example table cites `/project init`
6. `www/content/getting-started/first-task.md:64` — moai-pm role table row
7. `www/content/getting-started/quick-start.md:16,27,51` — onboarding walkthrough cites `/project init` (3 occurrences)
8. `www/data/agent_teams.json:99,193,1439` — skill catalog JSON entries reference `/project feedback`, `moai-coworker` "`/project` 역할", and the `moai-pm` id block

Required substance: `/project` → `/goose --project` (Desktop) or `/moai --project` (development); stale "12개 AI 직원" → 18-plugin roster.

### SPEC-MOC-PM-REDESIGN-001 partial supersession — DONE

`partially_superseded_by: [SPEC-MOC-PM-ADVISORS-001]` added to `.moai/specs/SPEC-MOC-PM-REDESIGN-001/spec.md` frontmatter (single line; `status: completed` and all other fields untouched). Per spec.md §E, that SPEC's `project` skill **artifact** is replaced, not its historical record — hence *partial* supersession, not `superseded`.

### Residual / still-open (carried from §E.3 run-phase status)

| # | Item | Status | Disposition |
|---|------|--------|-------------|
| 1 | Catalog-fallback drift — `moai/references/mcp-fallback-summary.md` is a static snapshot of the sibling's MCP catalog with **no automated sync mechanism** | **STILL OPEN** | Flagged in-file as a driftable copy; follow-up SPEC candidate (schema handshake with SPEC-MOC-CODER-LSP-MCP-001) |
| 2 | `/moai` short-form dispatch ambiguity | **STILL OPEN** | Mitigated (explicit-namespace docs `moai-pm:moai` vs `moai:moai`) but **platform-defined** — outside this SPEC's control |
| 3 | Runtime E2E of both skills | **NOT EXECUTED** | Static verification only (21 machine gates); runtime skill-load + interview-flow E2E deferred |
| 4 | Shared-reference duplication (`router.md`, `init-protocol.md`, `execution-protocol.md`, `claudemd-generator.md` per-skill copies) | **ACCEPTED (realized as designed)** | Not a defect; manual sync required on future changes — maintenance note |
| 5 | `www/**` guide updates (REQ-D-003) | **HANDED OFF** | 8 target paths recorded above |
| 6 | Stray untracked runtime-artifact dirs under the deleted `skills/project/` (main checkout) | **OPEN — non-git cleanup** | Never git-tracked; requires direct `rm -rf` on main checkout, outside commit scope |

Resolved at run-phase: `/goose` name collision (#2 of plan.md's 6 — zero pre-existing refs, name claimed), interview grade-model drift (#5 — no drift, migrated verbatim), live plugin-family churn (#6 — mitigated by design: roster cited from marketplace.json, never hardcoded).

```yaml
sync_complete_at: 2026-07-11
sync_commit_sha: a863ed6
sync_status: complete
sync_route: A (Hybrid Trunk — single commit direct to main, no PR)
sync_commit_files: 2  # CHANGELOG.md + .moai/specs/SPEC-MOC-PM-REDESIGN-001/spec.md (tracked)
b12_self_test_a: PASS  # pre-emission grep — 0 duplicate entry headings
b12_self_test_b: PASS  # AC count match — 21 machine + 3 structural = 24, matches acceptance.md SSOT
b12_self_test_c: PASS  # file path verification — all claimed paths observed via find/ls/jq
changelog_entry_position: "[Unreleased] first entry (### Changed — SPEC-MOC-PM-ADVISORS-001), above sibling SPEC-MOC-CODER-LSP-MCP-001 (preserved, untouched)"
frontmatter_status_transitions:
  spec.md: "in-progress -> completed"
  plan.md: "draft -> completed"
  design.md: "draft -> completed"
  acceptance.md: "draft -> completed"
  updated_field: "2026-07-11 (already current, no change)"
  body_content_modified: false
supersession_task:
  target: SPEC-MOC-PM-REDESIGN-001
  field_added: "partially_superseded_by: [SPEC-MOC-PM-ADVISORS-001]"
  status: done
req_d_003_www_handoff:
  targets_recorded: 8
  www_edits_performed: 0
  status: handed-off
residual_open_count: 4  # catalog-fallback drift, /moai dispatch ambiguity, runtime E2E, stray-dir cleanup
residual_accepted_count: 1  # shared-reference duplication
residual_handed_off_count: 1  # www/** guide updates
```
