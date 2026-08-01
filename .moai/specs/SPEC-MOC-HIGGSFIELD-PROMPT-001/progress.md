# progress.md — SPEC-MOC-HIGGSFIELD-PROMPT-001

## §E.1 Plan-phase Audit-Ready Signal

```yaml
plan_status: audit-ready
plan_complete_at: 2026-07-12
tier: L
route: main-direct   # Hybrid Trunk 1-person OSS — no branch, no PR, no worktree
artifacts:
  - spec.md              # authored
  - plan.md              # authored
  - acceptance.md        # authored
  - research.md          # pre-existing input (Deep Research, 15 families)
  - mcp-catalog-snapshot.md  # pre-existing input (fills the Tier L design-artifact slot — plan.md D-4)
  - progress.md          # this file
requirements: 28        # REQ-001..REQ-061 (GEARS)
acceptance_criteria: 28 # AC-HGF-001..AC-HGF-028 (18 BLOCKER / 9 MAJOR / 1 MINOR)
clarifications_open: 0
milestones: 7           # M1 core → M2/M3 image → M4/M5 video → M6 sweep → M7 E2E
e2e_budget: "10 credits observed; planned spend 5 (soul_2 1 + veo3_1_lite 4s 4)"
```

## §E.1a Plan-phase Harness Remediation (plan-auditor FAIL 0.70 → re-verify)

The acceptance §D.3 verification harness was remediated after plan-auditor
reproduced 11 defects with fixtures (SPEC substance PASSED; only the harness
failed). All fixes are in `acceptance.md` (+ this file's counts + one spec.md
MINOR typo). Each corrected command was re-verified against a deliberately-broken
fixture (confirmed it now FAILS on the defect it targets) AND an honest fixture
(confirmed no false-fail).

| # | Defect | Fix | Fixture verified |
|---|--------|-----|------------------|
| D1 | `grep -L PAT $CRAFT/*.md` word-split left the 7 image craft files unchecked | two explicit globs | citation-less soul.md now flagged |
| D2 | inverted `Official formula` regex false-failed honest `## No …`, false-passed `**Official Formula:**` | heading/bold + negation-subtract regex | `**Official Formula:**` flagged; `## No Official Formula` passes |
| D3 | generic-formula negative grepped English headings; skill prose is Korean | positive structural (per-family routing) + §D.5 inspection | Korean `## 범용 …` no longer evades (structural check) |
| D4 | `git diff HEAD~1` assumed single-commit; milestones use per-M commits | `git log --oneline -- <path> \| grep SPEC-ID` | per-M commit history recognized |
| D5 | retired-param sweep excluded ALL of call-schema.md | (5a) outside-file + (5b) fenced-block awk | fenced `image_url` in call-schema.md flagged |
| D6 | awk fenced-block toggle carried across files | `FNR==1{b=0}` reset | cross-file prose no longer false-flagged |
| D7 | `batch_size` check line-scoped | ±3-line proximity (while-read + awk) | `## batch_size` w/ distant ms_image flagged |
| D8 | count drift | 28 REQ / 18 BLOCKER / 9 MAJOR / 1 MINOR (4 sites) | matrix re-tallied |
| D9 | spec.md "seven" undercounted invented IDs | → "eight" (only permitted spec.md edit) | drift ledger cross-checked |
| D10 | REQ-011 had no mechanical tripwire | added `grep AskUserQuestion(` → expect 0 | tripwire fires on a planted call |
| D11 | R1–R5 counted mentions, not definitions | `grep '\*\*R[1-5]'` bold-label | mention-only fixture now fails |
| +portability | run shell is **zsh**; unquoted `$ALL` does not word-split → `grep $ALL` matched nothing (harness-wide FALSE-PASS beyond the 11) | glob `"$SK"/media-higgsfield-*` + `find -exec {} +` + `\| while read` | zsh `$0` confirmed; glob expands to 3 dirs in bash AND zsh |

## §E.2 Run-phase Evidence

### Execution note (deviation from §F, recorded for honesty)

§F selected `sub-agent` (Mode 5). At run time the Claude Code runtime **deterministically forced worktree isolation** on every `manager-develop` spawn (2 consecutive spawns each returned a structured blocker: `Write` locked to `.claude/worktrees/agent-*`, base `a863ed6` predating the SPEC commit — main-direct commit impossible from an isolated worktree). Root-cause investigation (`git worktree list`, settings.json, agent frontmatter) confirmed the isolation is runtime-autonomous with no orchestrator-controllable off switch. Per user approval (AskUserQuestion), **M1–M3 were authored orchestrator-direct in the main checkout** — the guaranteed non-isolated path honoring the main-direct route. The previously-untracked SPEC dir was first committed to main (`1c18e6b`) to make it reachable.

### Scope of this evidence: M1 + M2 + M3 (core skill + image modality). M4–M7 (video, integrity sweep, E2E) NOT executed — deferred.

### Deliverables

- **M1** `media-higgsfield-core/` CREATED — `SKILL.md` + 5 references (`call-schema.md`, `catalog-protocol.md`, `universal-rules.md`, `interview-schema.md`, `job-lifecycle.md`).
- **M2** `media-higgsfield-image/references/prompt-craft/` CREATED — 7 files (`soul.md`, `nano-banana.md`, `openai.md`, `seedream.md`, `flux.md`, `recraft.md`, `marketing-studio.md`), each from research.md §3 with `Evidence tier:` + ≥1 `https://` citation.
- **M3** `media-higgsfield-image/SKILL.md` REWRITTEN (drift removed → live-query flow); `references/model-guide.md` DELETED (`git rm`, D-3).

### AC binary matrix (image + core scope; verified via acceptance.md §D.3, core+image glob)

| AC | Sev | Result | Evidence (observed) |
|----|-----|--------|---------------------|
| AC-HGF-001 | BLOCKER | PASS | core = SKILL.md + 5 named refs |
| AC-HGF-002 | BLOCKER | PASS | image craft = 7 named files; `model-guide.md removed: PASS` |
| AC-HGF-004 | BLOCKER | PASS | invented IDs in core+image = 0 (`grep -rnE '<F1\|F2>' $CORE $IMG` → 0) |
| AC-HGF-005 | BLOCKER | PASS | 5a=0 (outside call-schema), 5b=0 (fenced in call-schema), L19 `do not exist` present |
| AC-HGF-006 | MAJOR | PASS | batch_size w/o ms_image ±3 = 0 |
| AC-HGF-007 | BLOCKER | PASS | bracket-enum in core+image SKILL.md = 0 |
| AC-HGF-008 | MAJOR | PASS | negative_prompt in fenced block = 0 |
| AC-HGF-009 | BLOCKER | PASS | `grep -L models_explore` (core+image SKILL) empty; `grep -L get_cost` (image SKILL + job-lifecycle) empty |
| AC-HGF-010 | MAJOR | PASS | call-schema namespaces: mcp__higgsfield__=2, mcp__claude_ai_higgsfield__=2, namespace=4 |
| AC-HGF-011 | BLOCKER | PASS | `grep -L adjustments` empty; `grep -L credits_exact job-lifecycle.md` empty |
| AC-HGF-012 | MINOR | PASS (advisory) | image SKILL: models_explore(L5) < get_cost(L73) < generate_image(L77) |
| AC-HGF-013 | BLOCKER | PASS | all 7 image craft cite `https://` |
| AC-HGF-014 | BLOCKER | PASS | all 7 image craft carry `Evidence tier:` |
| AC-HGF-015 | BLOCKER | PASS | soul.md `no official prompt formula`=2; fabricated-formula-label check = 0 |
| AC-HGF-017 | MAJOR | PASS | openai.md `openai_hazel`=5, `unverified`=4 |
| AC-HGF-018 | BLOCKER | PASS | universal-rules.md `**R[1-5]` distinct = 5 |
| AC-HGF-019 | MAJOR | PASS | image SKILL `live lookup` (ci) = 3 |
| AC-HGF-024 | MAJOR | PASS | image marketing-studio: style_id=3, `no default`(ci)=1, show_marketing_studio=4 |
| REQ-011 tripwire | — | PASS | `grep -rn 'AskUserQuestion('` core+image = 0 |

### Deferred to M4–M7 (NOT claimed PASS)

AC-HGF-003 (video craft set), AC-HGF-016 (grok audio absence), AC-HGF-020 (Wan↔Seedance contradiction), AC-HGF-021 (gemini-omni broken-refs), AC-HGF-022 (minimax prompt_optimizer), AC-HGF-023 (marketing_studio_video mutual exclusion), AC-HGF-025..028 (E2E live MCP). The video skill tree is UNTOUCHED and still carries its pre-SPEC drift (13 invented IDs / 10 retired params measured) — that is M4–M5 scope, not a regression.

### Gaps / residual risk

- Video modality + E2E remain. The full drift-sweep ACs (AC-004/005 over all 3 trees) will only pass after M4–M5 rewrites the video skill.
- S1 (plan-audit SHOULD-FIX): `marketing_studio_video` lacks a live-query REQ/AC symmetric to REQ-040/AC-024 — to be recorded as documented debt when M4 authors the video marketing-studio craft (per user decision: proceed, record as debt).
- Skill runtime behavior (actual MCP calls) not exercised — that is M7 E2E.

### M4–M6 addendum (video modality + integrity sweep)

Continued orchestrator-direct in the same session (user-approved). **M4** created 8 video prompt-craft files (`veo`, `kling`, `seedance`, `cinema-studio`, `marketing-studio`, `wan`, `gemini-omni`, `grok`) from research.md §4 + updated `references/dop-motions.md` in place (fictional 6-preset table → 26 live-verified slugs framed as illustrative, not a hard-coded contract). **M5** rewrote `media-higgsfield-video/SKILL.md` (drift removed → live-query flow + per-family routing + hazard block). **M6** ran the full acceptance.md §D.3 sweep across all 3 trees.

Clean counts: core = 6 files, image craft = 7, video craft = 8, dop-motions.md present + updated.

Whole-tree AC results (observed):
- AC-HGF-003 (BLOCKER): video craft = 8 named files PASS; dop-motions.md present + modified by this SPEC (git-log SPEC-ID match verified at commit).
- AC-HGF-004 (BLOCKER): invented IDs across ALL 3 trees = **0** (video drift eliminated).
- AC-HGF-005 (BLOCKER): retired params outside call-schema = 0 (all 3 trees).
- AC-HGF-016 (BLOCKER): grok.md `no audio documentation`=2, fabricated-formula-label=0.
- AC-HGF-020 (BLOCKER): seedance `unstable`=2, wan `Timestamp`=2, video SKILL `per-family`=2, `prompt-craft/` routing=15 (Wan↔Seedance contradiction preserved).
- AC-HGF-021 (MAJOR): gemini-omni.md carries Google's verbatim `not correctly processed by the model at this time`.
- AC-HGF-022 (MAJOR): video SKILL `prompt_optimizer`=1 (MiniMax silent-override hazard warned).
- AC-HGF-023 (MAJOR): ms-video `ad_reference_id`=2, `mutually exclusive`=1.
- AC-HGF-007/008/009/011/013/014/019 re-verified PASS across all 3 trees; boundary `AskUserQuestion(`=0.

§D.5 inspection (video, honest): video SKILL routes to per-family `prompt-craft/` files and presents NO single unified generic video-formula section (Korean or otherwise) — AP-1 avoided. Wan/Seedance opposite conventions are stated in-file, not averaged.

**Only M7 (E2E live MCP) remains** — requires an authenticated Higgsfield MCP session + real credit spend (≤10 credit budget). Deferred: AC-HGF-025..028 (E2E), not yet claimed.

## §E.3 Run-phase Audit-Ready Signal

_<pending — M7 E2E (AC-025..028) remains; requires authenticated Higgsfield MCP + real credit spend. All grep-verifiable ACs (M1-M6) PASS. S1 debt (marketing_studio_video live-query symmetry) mitigated in-file: dop-motions.md + prompt-craft/marketing-studio.md frame the 26 preset slugs as illustrative, runtime-queried via show_marketing_studio, not a hard-coded contract.>_

## §E.4 Sync-phase Audit-Ready Signal

_<pending sync-phase — manager-docs>_

## §F Phase 0.95 Mode Selection

- **Input**: tier=L, scope=~24 files (new+rewrite), domains=multi (skill bodies + references + MCP calls), language mix=Korean prose + English technical, concurrency benefit=LOW (sequential inter-file dependency: M1 core blocks M3/M5)
- **Mode evaluation**: trivial=no (semantic authoring) | background=no (writes) | agent-team=RETIRED | parallel=no (coding-heavy, Anthropic coding-parallelism caveat) | workflow=no (not mechanical-uniform; per-family distinct craft) | **sub-agent=SELECTED**
- **Decision**: sub-agent
- **Justification**: Coding-heavy multi-domain authoring with sequential dependencies (core -> consumers). Per Anthropic coding-task parallelism caveat, sequential sub-agent is the safe default over parallel. prompt-craft reference files are batched within a milestone since they are independent leaf files, but SKILL.md rewrites are sequenced after core.
