---
id: SPEC-MOC-HIGGSFIELD-PROMPT-001
title: "Implementation plan — Higgsfield prompt-craft skills"
version: "0.1.0"
status: draft
created: 2026-07-12
updated: 2026-07-12
author: manager-spec
priority: P1
phase: "moai-media v0.2.0"
module: "plugins/moai-media/skills"
lifecycle: spec-anchored
tier: L
tags: "higgsfield, mcp, prompt-craft, media, skills, drift-elimination"
---

# plan.md — SPEC-MOC-HIGGSFIELD-PROMPT-001

## §A — Context

### A.1 Location and route

| Item | Value |
|---|---|
| Project root | `/Users/goos/MoAI/claude.mo.ai.kr` |
| Tier | **L** |
| Git route | **main-direct** (Hybrid Trunk, 1-person OSS). No feature branch, no PR, no worktree. |
| Commit convention | `feat(SPEC-MOC-HIGGSFIELD-PROMPT-001): M{N} <subject>` + `🗿 MoAI` trailer |
| Write scope | `plugins/moai-media/skills/media-higgsfield-{core,image,video}/**` and `.moai/specs/SPEC-MOC-HIGGSFIELD-PROMPT-001/progress.md` — nothing else |

### A.2 Artifact set (Tier L)

| Artifact | Status |
|---|---|
| `spec.md` | authored (this SPEC) |
| `plan.md` | authored (this file) |
| `acceptance.md` | authored |
| `research.md` | **pre-existing** — Deep Research, 15 families, evidence-tiered. Input, not output. |
| `mcp-catalog-snapshot.md` | **pre-existing** — serves the Tier L design-artifact role: it is the design evidence baseline for the call-schema contract. **No separate `design.md` is authored**; a fifth file restating the snapshot would be duplication, and the snapshot is already the design's ground truth. |
| `progress.md` | skeleton emitted at plan-phase (§E.1 populated; §E.2–§E.4 placeholders) |

### A.3 PRESERVE list (do not touch)

- `plugins/moai-media/skills/media-audio-gen/**`
- `plugins/moai-media/skills/media-gemini-3-image-prompt/**`
- `plugins/moai-media/skills/media-gpt-image-2-prompt/**`
- `plugins/moai-media/skills/media-midjourney-v8-prompt/**`
- `plugins/moai-media/skills/media-codex-image/**`
- `plugins/moai-media/skills/media-notebooklm-slide-prompt/**`
- `plugins/moai-media/skills/media-asset-production/**`
- `plugins/moai-media/.mcp.json` — **verify only**, do not edit
- `.moai/specs/SPEC-MOC-HIGGSFIELD-PROMPT-001/research.md` — **read-only input**
- `.moai/specs/SPEC-MOC-HIGGSFIELD-PROMPT-001/mcp-catalog-snapshot.md` — **read-only input**

### A.4 EXTEND / REPLACE targets

| Path | Action |
|---|---|
| `skills/media-higgsfield-core/**` | **CREATE** (new skill, 1 + 5 files) |
| `skills/media-higgsfield-image/SKILL.md` | **REWRITE** (full) |
| `skills/media-higgsfield-image/references/prompt-craft/*.md` | **CREATE** (7 files) |
| `skills/media-higgsfield-image/references/model-guide.md` | **DELETE** (see D-3) |
| `skills/media-higgsfield-video/SKILL.md` | **REWRITE** (full) |
| `skills/media-higgsfield-video/references/prompt-craft/*.md` | **CREATE** (8 files) |
| `skills/media-higgsfield-video/references/dop-motions.md` | **UPDATE in place** — do NOT delete |

---

## §B — Decisions (settled; do not re-open)

| # | Decision | Rationale |
|---|---|---|
| **D-1** | **Skill body language: Korean prose, English technical content.** Explanatory prose in Korean (matching all 7 sibling `moai-media` skills and the Korean-user-facing plugin). Model IDs, parameter names, prompt-craft conventions, vendor verbatim quotes, and all assembled prompt output stay in **English verbatim** — a translated `SFX:` tag or a translated `{curly brace}` dialogue delimiter is a broken convention, not a localized one. | Scope discipline: match the file/plugin's existing style. Override cost is trivial — state a preference before M1 and it is honored. |
| **D-2** | **Craft files are authored from `research.md` alone.** No new web research in the run phase. Every claim in a craft file traces to a `research.md` citation. | `research.md` is complete and evidence-tiered; its §6 ledger explicitly names the third-party sources that were *rejected* as evidence. Re-searching invites reintroducing them. |
| **D-3** | **`media-higgsfield-image/references/model-guide.md` is deleted.** It is an 11-model hard-coded table whose contents are, per the drift ledger, largely fictional. | A hard-coded model table is precisely what REQ-003/REQ-004 forbid. Keeping it as "background" would leave a live drift source inside the very skill built to eliminate drift. Its replacement is the live-query protocol in `core/references/catalog-protocol.md`. |
| **D-4** | **`mcp-catalog-snapshot.md` fills the Tier L design-artifact slot.** No separate `design.md`. | The snapshot *is* the design evidence — the call-schema contract, the medias-role model, the cost mechanics, and the drift ledger. A `design.md` would restate it. |
| **D-5** | **E2E spends real credits, once, on the budget-safe pair.** `get_cost: true` preflight sweep (zero credits) across the representative models first; then exactly one `soul_2` image (1 credit) and one `veo3_1_lite` 4s video (4 credits). | Balance is 10 credits, free plan. 5-credit spend leaves headroom for one retry. The snapshot §5.1 records the alternates (`z_image` 0.15 + `kling3_0_turbo` 7.5 = 7.65) if the primary pair's live cost has drifted upward. |

---

## §C — Pre-flight (run before any file change)

```bash
cd /Users/goos/MoAI/claude.mo.ai.kr

# 1. Branch + baseline (expect: main)
git branch --show-current && git rev-parse --short HEAD

# 2. Working tree hygiene — confirm no unrelated staged/modified files in scope
git status --porcelain plugins/moai-media/

# 3. Current skill tree (the thing being replaced)
find plugins/moai-media/skills/media-higgsfield-image plugins/moai-media/skills/media-higgsfield-video -type f

# 4. MCP registration still resolves (verify only — do not edit)
cat plugins/moai-media/.mcp.json

# 5. Live MCP reachable + balance (the E2E budget input)
#    Namespace is registration-dependent — resolve it, do not assume.
#    balance  →  expect ~10 credits, free plan
```

---

## §D — Constraints (DO NOT VIOLATE)

1. **No hard-coded parameters.** Any model ID, enum, aspect ratio, duration, media role, or credit figure appearing in a *call path* is a defect. Craft files may *name* a model as the subject of a citation; they may not present it as a callable contract.
2. **No invented craft.** Where `research.md` records an evidenced absence (Soul formula, Grok audio, `openai_hazel` identity), the craft file states the absence. Filling the gap with a plausible-sounding formula is the single worst failure mode available in this SPEC — it is worse than the current broken skill, because it is *confidently* wrong.
3. **No `AskUserQuestion` inside skill bodies.** The Socratic interview is an orchestrator-conducted flow; the skill documents the slots to collect, not the tool call. Subagents return blocker reports.
4. **No new dependencies, no `.mcp.json` edit, no plugin version bump** outside the run scope (marketplace/version handling, if any, is a separate concern — do not touch it).
5. **PRESERVE list (§A.3) is binding.** A parallel session may be active in this repo; touching anything outside the three `media-higgsfield-*` skill directories risks a race.
6. **Never `--no-verify`, never `--amend`, never force-push.**
7. **Snapshot is not a runtime contract.** If run-phase discovers the live catalog has drifted from `mcp-catalog-snapshot.md`, that is *expected* and *proves the design*. Record the drift in `progress.md` §E.2; do not "fix" the snapshot into the skills.

---

## §E — Self-Verification (report per the 5-section evidence format)

Each command below must be run and its **verbatim output** cited. See `acceptance.md` §D.3 for the full command set with expected outputs.

| # | Check | Command sketch |
|---|---|---|
| E1 | AC binary PASS/FAIL matrix | per `acceptance.md` §D — every AC row with its command + actual output |
| E2 | File-count integrity | `find plugins/moai-media/skills/media-higgsfield-* -type f \| sort` |
| E3 | Forbidden-literal sweep (invented IDs, retired params) | `grep -rn` per `acceptance.md` §C.2 → expect 0 |
| E4 | Required-literal sweep (citations, evidence tiers, absence statements, hazards) | `grep -L` per `acceptance.md` §C.1 → expect empty |
| E5 | `dop-motions.md` still exists and was updated (not recreated empty) | `test -f` + `git diff --stat` on that path |
| E6 | E2E evidence: preflight costs, 2 job IDs, 2 result URLs, balance before/after | MCP call transcripts recorded in `progress.md` §E.2 |
| E7 | Commit + push state | `git log --oneline origin/main..HEAD` then `git push origin main` |

---

## §F — Milestones (priority-ordered; no time estimates)

Sequencing constraint: **the core skill lands before its consumers** (both consumer skills reference the call-schema SSOT, so authoring a consumer first would force inventing the contract twice). **E2E lands last** (it validates the assembled system, and it is the only step that spends credits).

### M1 — `media-higgsfield-core` (Priority: Critical — blocks M3, M5)

Create the new skill: `SKILL.md` + the 5 reference files.

- `SKILL.md` — what the core is, when a consumer loads it, the orchestration contract (the REQ-010 flow), the namespace-resolution rule.
- `references/call-schema.md` — the nested `params{}` shape; `medias[].role` / `.value` (media_id or job_id, **never a raw URL**); `count` vs `batch_size`; `get_cost`; the `adjustments` read-back; the **runtime namespace resolution** (both prefixes named); and the explicitly-labelled **anti-pattern section** listing the parameters that do not exist. This is the only file in the tree permitted to name the retired parameters.
- `references/catalog-protocol.md` — `models_explore(list/search/get/recommend)`, `show_marketing_studio`, `presets_show`, `get_workflow_instructions`. The live-query protocol, with the vendor's own instruction quoted: *"When unsure, run `higgsfield model get <model>` and inspect the schema."*
- `references/universal-rules.md` — R1–R5, each with its multi-vendor evidence.
- `references/interview-schema.md` — the Socratic slots the craft files actually consume: subject, action, scene, camera, lighting/atmosphere, style, literal text (+ font), audio/dialogue, references (+ **each reference's purpose**), shot count, aspect, duration, quality/budget tier.
- `references/job-lifecycle.md` — polling, error taxonomy (`queued`/`in_progress`/`completed`/`failed`/`nsfw`), cost surfacing (`credits` not `credits_exact`), and the `adjustments` reporting obligation.

### M2 — Image prompt-craft references (Priority: High)

Seven files under `media-higgsfield-image/references/prompt-craft/`, each authored from the matching `research.md` §3 subsection, each carrying ≥1 source URL and an evidence tier line.

| File | Anchor | Special obligation |
|---|---|---|
| `soul.md` | research §3.1 | **Evidenced absence.** State plainly that no official prompt formula exists and that the vendor is deliberately anti-formula. Document what *is* documented: Soul ID training mechanics (20+ photos), Soul Cast's 8 parameter categories, the `budget` slider semantics. Fall back to R1–R5. |
| `nano-banana.md` | research §3.2 | Google's 5-part formula; the model-generation mapping; the Creative Director vocabulary; the text-first hack; the `thinking` enum spelling caveat (Higgsfield `MINIMAL|HIGH` vs Google `low`/`high`). |
| `openai.md` | research §3.3 | GPT Image structure + text rendering + editing. **Flag the `openai_hazel` assumption as unverified** — the name appears nowhere in OpenAI's docs. |
| `seedream.md` | research §3.4 | ByteDance's five stated principles; the editing exemplars verbatim; the 5.0 Pro overlay-marker limitation (not MCP-exposed). |
| `flux.md` | research §3.5 | `Subject + Action + Style + Context`; word order is load-bearing; the 30–80-word ideal; **FLUX.2 has no negative prompts**; the Kontext verb-choice rule. |
| `recraft.md` | research §3.6 | The 8-step global-to-local structure; the vector/logo conventions and designer-recognizable terms; the "avoid texture language for vector work" rule. |
| `marketing-studio.md` | research §3.7 | **This family is a workflow, not a prompt.** The mandatory `show_marketing_studio` → user picks style → generate sequence. `style_id` has no default. |

### M3 — `media-higgsfield-image/SKILL.md` rewrite (Priority: High)

Full rewrite around the REQ-010 flow. Delete `references/model-guide.md` (D-3). The SKILL.md carries: the interview slots, the model-candidate selection heuristic (which *narrows candidates*, then live-queries — it never asserts parameters), the `get_cost` preflight step, the `adjustments` read-back, the out-of-scope-model fallback statement, and the `ms_image` style-pick hard rule.

### M4 — Video prompt-craft references + `dop-motions.md` (Priority: High)

Eight files under `media-higgsfield-video/references/prompt-craft/`, from `research.md` §4.

| File | Anchor | Special obligation |
|---|---|---|
| `veo.md` | research §4.1 | The Core Prompt Formula; **the audio syntax** (`"quoted dialogue"` / `SFX:` / `Ambient noise:`) — the highest-value single finding in the research. Do **not** backfill Veo 3.1's conventions onto `veo3`. |
| `kling.md` | research §4.2 | Flag the evidence tier honestly: **1차-relayed** (the vendor domain is WAF-blocked to direct fetch). The framework is a flexible writing guide, not a formula. Exclusions fold into the positive prompt — the vendor's own recommendation. |
| `seedance.md` | research §4.3 | **Timestamps are unstable — ByteDance's own words.** Labeled shot list, no timestamps. The `@Image N` / `@Video N` mention system *with an explicit purpose statement per reference*. The bracket conventions (music/SFX/dialogue/subtitles). Character-drift avoidance. |
| `cinema-studio.md` | research §4.4 | The 4-layer reference system; the motion-transfer literal syntax; the empty-prompt placement; **the parameter enums are deliberately unpublished — live-query them.** |
| `marketing-studio.md` | research §4.5 | 26 preset modes (not 6). `hook_id`/`setting_id` **mutually exclusive** with `ad_reference_id`. Hooks require `product_ids`. Default aspect is landscape — pass `9:16` explicitly. |
| `wan.md` | research §4.6 | The named formulas — including **`Motion + Camera movement`** for image-to-video (the R2 source) and the **timestamped multi-shot** formula. Note the direct contradiction with Seedance in-file; this is the corollary made concrete. |
| `gemini-omni.md` | research §4.7 | **Simple prompts work best for editing** — the inverse of Veo. The `<FIRST_FRAME>` / `<IMAGE_REF_N>` inline tokens. **The known-broken video-references warning, in Google's own words.** |
| `grok.md` | research §4.8 | **Evidenced absence.** No formula, no length guidance, no negative-prompt convention, **and no audio documentation at all** — despite the catalog tagging `grok_video_v15` "native audio". State this. Fall back to R1–R5 + the official plain-sentence exemplars. |

`references/dop-motions.md` — **update in place.** Replace the fictional "6 official video presets" table with the live-verified 26 preset slugs (obtained by `show_marketing_studio`, not copied from the snapshot as a contract) and the camera-direction craft that survives. Keep the file; keep its role.

### M5 — `media-higgsfield-video/SKILL.md` rewrite (Priority: High)

Full rewrite, same flow as M3. Additionally carries the hazard block: `gemini_omni` broken video-references, `minimax_hailuo` silent camera override (`prompt_optimizer` not exposed), Grok's undocumented audio tag. Explicitly states there is **no generic video formula** and routes to the per-family file.

### M6 — Integrity sweep (Priority: Medium)

Run the full `acceptance.md` §D.3 command set. Every forbidden literal → 0. Every required literal → present. File counts exact. `dop-motions.md` present and modified. Cross-references between the three skills resolve. `.mcp.json` unchanged.

### M7 — E2E verification (Priority: Medium — must be last)

1. `balance` → record starting credits.
2. `get_cost: true` preflight on the representative models per modality → record every returned `credits` value. **Zero credits consumed** — verify by re-reading `balance`.
3. One real image: `soul_2`, 16:9, quality 2k → poll `job_status` to `completed` → record job ID + result URL.
4. One real video: `veo3_1_lite`, 16:9, 4s → poll to `completed` → record job ID + result URL.
5. `balance` → record ending credits. Delta must be ≤ 10 and must reconcile with the reported `credits` figures.
6. Record every `adjustments` object returned, and confirm the skill's reporting rule surfaces them.
7. Write all of the above into `progress.md` §E.2 as run-phase evidence.

---

## §G — Risks and Anti-Patterns

| # | Risk | Mitigation |
|---|---|---|
| R-1 | **Fabricated craft.** Fifteen files to author, three of which must say "the vendor published nothing". The pull toward filling those gaps with a plausible formula is strong and the result is undetectable by casual review. | AC-HGF-012/013/014 pin *literal absence statements* and *forbid* an "Official formula" heading in `soul.md` / `grok.md`. D-2 forbids new research. A craft file with no citation fails AC-HGF-010. |
| R-2 | **Snapshot leaks into the skills as a contract.** The snapshot is a convenient, complete, well-formatted model table — exactly the shape of the defect being removed. | Constraint §D.7. AC-HGF-006 (no hard-coded model catalog table in any SKILL.md). The snapshot's own header already declares itself non-authoritative. |
| R-3 | **Live catalog has drifted since 2026-07-12.** A model ID or enum in a craft file's *example* may no longer exist. | This does not break the design — the skill live-queries. But craft-file examples that cite a dead model ID are confusing. M7 re-queries; any drift found is recorded in `progress.md` §E.2 and the affected example is corrected. |
| R-4 | **E2E overspends.** Costs may have risen since the snapshot. | `get_cost` preflight is mandatory and free. **HARD stop**: if the preflight total for the chosen pair exceeds 8 credits, fall back to the alternate pair or halt and report — do not submit. |
| R-5 | **Namespace mismatch at E2E.** The session may be running under either registration. | The skill resolves at runtime by design (REQ-015). If M7 runs under one namespace only, the *other* prefix remains unverified — record this honestly as a residual gap rather than claiming both. |
| R-6 | **Parallel session race.** This repo has seen concurrent sessions. | Write scope is three directories. Pre-flight `git status --porcelain plugins/moai-media/`. Fetch before push. |

### Anti-patterns (named, to be avoided)

- **AP-1 — "Universal video formula".** Collapsing the 8 video craft files into one shared formula section. Wan and Seedance officially prescribe opposite conventions; the collapse is a correctness regression.
- **AP-2 — Silent gap-filling.** Writing a Soul formula because the file "looks empty without one".
- **AP-3 — Hard-coded convenience table.** Adding a "quick reference: model IDs" table to a SKILL.md "just for readability". It will be wrong within weeks, and it is REQ-003.
- **AP-4 — `credits_exact` in the report.** Reporting the un-rounded figure the user is not billed.
- **AP-5 — Auto-defaulting `ms_image` style.** The style is the dominant creative driver and has no default; picking one silently produces a result the user did not ask for.
- **AP-6 — Re-researching.** Opening a browser during the run phase.

---

## §H — Cross-References

- `spec.md` §B — the design principle (two axes, two sources of truth) and its corollary.
- `acceptance.md` §C — the pinned-literal registry (required + forbidden literals). This is the mechanism that makes the ACs non-vacuous.
- `research.md` §2 — R1–R5 universal rules with multi-vendor evidence. §3/§4 — per-family craft. §5 — gap register (G1–G10). §6 — source ledger including the rejected-evidence list.
- `mcp-catalog-snapshot.md` §0 — call-schema ground truth. §5.0.1 — `style_id` vs `format_id` resolution. §5.1 — observed credit costs and the E2E budget. §6 — the drift ledger this SPEC eliminates.
- `.claude/rules/moai/development/spec-frontmatter-schema.md` — frontmatter schema (12 canonical fields + optional `tier`).
