---
id: SPEC-MOC-HIGGSFIELD-PROMPT-001
title: "Higgsfield prompt-craft skills — live-queried parameters, statically-cited craft"
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

# SPEC-MOC-HIGGSFIELD-PROMPT-001 — Higgsfield prompt-craft skills

## HISTORY

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1.0 | 2026-07-12 | manager-spec | Initial draft. Derived from `research.md` (15-family Deep Research, evidence-tiered) and `mcp-catalog-snapshot.md` (live 60-model catalog + call schema + observed credit costs). Tier L, main-direct (Hybrid Trunk 1-person OSS). |

---

## §A — Context and Problem

`plugins/moai-media/` ships two Higgsfield skills — `media-higgsfield-image` and `media-higgsfield-video`. Both are **non-functional**, not merely stale.

Three findings, each independently sufficient to condemn the current design (full evidence: `research.md` §1, `mcp-catalog-snapshot.md` §6):

1. **The existing skills invent their own API.** They document a `sora_2` model that does not exist in the catalog, eight further model IDs that do not exist, and a flat parameter shape (`width_and_height`, `duration_seconds`, `image_url`, `enhance_prompt`, `batch_size`) that the live MCP schema does not accept. Following them produces failed or silently-ignored calls.
2. **Higgsfield's own documentation disagrees with Higgsfield's own MCP.** The vendor's official agent docs name the mandatory DTC-ads field `format_id`; the live MCP schema names it `style_id`. Both are correct — for different surfaces (CLI vs MCP). A skill that hard-codes either is wrong half the time.
3. **The hosting platform's craft guide contradicts the model vendor's craft guide for the same model.** Higgsfield's Seedance guide prescribes timestamp-beat prompting; ByteDance — who trained the model — states verbatim that *"the model's support for precise timing (such as 0–3 seconds) is unstable, and forcibly limiting duration may lead to abnormal generation results."*

The vendor endorses the corrective design in its own words. Higgsfield's agent documentation instructs: **"When unsure, run `higgsfield model get <model>` and inspect the schema."** The vendor refuses to publish a static parameter contract, because it does not have one.

---

## §B — Design Principle (the spine of this SPEC)

> **Parameters are live-queried. Prompt craft is static and cited.**

Two axes, two sources of truth. They must never be conflated.

| Axis | Source of truth | How the skill obtains it | Volatility |
|---|---|---|---|
| **Parameters** — model IDs, parameter enums, aspect ratios, durations, media roles, credit cost | the **live MCP** | `models_explore` / `show_marketing_studio` / `presets_show` / `get_cost`, at call time | changes without notice; any hard-coded table is wrong on arrival |
| **Prompt craft** — formula, structure, audio syntax, exclusion expression, reference conventions | the **model vendor's official docs** | static, curated per family, frozen at authoring time, cited, evidence-tiered | stable; changes at model-release cadence |

**Conflict-resolution rule.** Where the hosting platform's craft guidance conflicts with the model vendor's, **the model vendor outranks the platform.** Higgsfield is a re-proxy; ByteDance, Google, OpenAI, BFL, Alibaba, and xAI trained the models. Where the two conflict, cite the vendor and record the conflict.

### Corollary — a single generic "video prompt formula" would be actively harmful

Alibaba's official Wan guide prescribes **explicit timestamp ranges** (`[0–3s]`) for multi-shot prompts. ByteDance's official Seedance guide warns that **timestamps destabilize the model** and instructs a bare labeled shot list with no timing. These are opposite conventions, officially documented, for the same output modality.

Per-family craft files are therefore a **correctness requirement**, not an organizational preference. Any refactor that collapses them into one shared "video formula" reintroduces a defect this SPEC exists to remove.

---

## §C — Deliverable Structure

A new shared core skill plus a full rewrite of the two consumer skills, all under `plugins/moai-media/skills/`:

```
media-higgsfield-core/                 # NEW — call-schema SSOT + orchestration contract
  SKILL.md
  references/
    catalog-protocol.md                # models_explore / show_marketing_studio / presets_show live-query protocol
    call-schema.md                     # params{} shape, medias roles, get_cost, adjustments, namespace resolution
    interview-schema.md                # Socratic slot definitions (image + video)
    universal-rules.md                 # R1-R5 (§D)
    job-lifecycle.md                   # polling, error taxonomy, cost surfacing

media-higgsfield-image/                # REWRITE
  SKILL.md
  references/prompt-craft/
    soul.md  nano-banana.md  openai.md  seedream.md  flux.md  recraft.md  marketing-studio.md

media-higgsfield-video/                # REWRITE
  SKILL.md
  references/prompt-craft/
    veo.md  kling.md  seedance.md  cinema-studio.md  marketing-studio.md  wan.md  gemini-omni.md  grok.md
  references/dop-motions.md            # EXISTING — update in place, do not delete
```

The image skill's existing `references/model-guide.md` — a hard-coded 11-model table — is the drift source itself and is removed (see plan.md D-3).

---

## §D — Universal Rules (R1–R5, owned by `media-higgsfield-core`)

Each rule below was confirmed independently across three or more vendors and is therefore family-independent. They live in the core skill, never duplicated per family.

- **R1 — Negative prompts do not exist. Express exclusions as positive scene content.** No image or video model in the catalog exposes a `negative_prompt` field. Google, Black Forest Labs, Kling, and Higgsfield converge on the same authoring rule independently — Kling recommends it *even though its own API has the field*. Write "an empty street", never "no cars".
- **R2 — For image-to-video, drop what the start image already supplies.** Alibaba's official image-to-video formula is literally `Motion + Camera movement`. Do not re-describe subject and scene the start frame already carries.
- **R3 — Literal in-image text goes in quotation marks, with the font named.** Confirmed by Google, OpenAI, BFL, and Recraft. Highest-leverage convention for the text-rendering models.
- **R4 — Edit prompts name the change AND the invariants.** "Change only X" + "keep everything else the same". Verb choice is load-bearing: *change* preserves identity, *transform* signals a full identity change.
- **R5 — Prompt length is per-vendor and often unstated.** There is no universal cap. Where a vendor states no length guidance, the skill says so rather than inventing one.

---

## §E — Requirements (GEARS)

### §E.1 — Architecture

- **REQ-001** (Ubiquitous) — The `media-higgsfield-core` skill **shall** be the single source of truth for the MCP call schema, the catalog-query protocol, the Socratic interview schema, the universal rules, and the job lifecycle; both consumer skills **shall** reference it rather than restate it.
- **REQ-002** (Ubiquitous) — The skill set **shall** separate the two axes of §B: parameters obtained live from the MCP, prompt craft carried as static cited per-family references.
- **REQ-003** (Unwanted) — The skills **shall not** hard-code model IDs, parameter enums, aspect ratios, durations, media roles, or credit costs anywhere in a call path.
- **REQ-004** (Unwanted) — The skills **shall not** carry a static model catalog table presented as a parameter contract. Where a model is named in a craft file, it is named as the *subject of a citation*, not as a callable parameter value.

### §E.2 — Runtime flow

- **REQ-010** (Event-driven) — **When** a user requests an image or video generation, the consuming skill **shall** execute the flow: intent parse → Socratic interview → model candidate selection → `models_explore(get)` live constraint fetch → load that family's prompt-craft reference → assemble the prompt per the official convention → `get_cost` preflight → `generate_*` → `job_status` poll → read back `adjustments` → report.
- **REQ-011** (Capability gate) — **Where** the acting agent is the MoAI orchestrator, the Socratic interview **shall** be conducted through `AskUserQuestion`. **Where** the acting agent is a subagent, the skill **shall** return a blocker report and **shall not** attempt to prompt the user.
- **REQ-012** (Event-driven) — **When** the skill has selected a model candidate, it **shall** call `models_explore(action: 'get')` for that model and derive every parameter value — aspect ratios, durations, enums, media roles — from the returned constraints.
- **REQ-013** (Ubiquitous) — The skill **shall** submit generation calls with a nested `params` object; flat top-level generation arguments **shall not** be used.
- **REQ-014** (Event-driven) — **When** a media reference is required, the skill **shall** first obtain a `media_id` via `media_upload` / `media_upload_widget` / `media_import_url`, or reuse a prior `job_id`. A raw `https://` URL **shall not** be passed as `medias[].value`.
- **REQ-015** (Ubiquitous) — The skill **shall** resolve the MCP tool namespace at runtime. The prefix differs by registration (`mcp__higgsfield__*` under the plugin `.mcp.json`; `mcp__claude_ai_higgsfield__*` under the Claude Desktop connector). Neither **shall** be hard-coded as the sole form.

### §E.3 — Cost and server substitution

- **REQ-020** (Event-driven) — **When** a generation is about to be submitted, the skill **shall** first issue the identical call with `get_cost: true`, which consumes zero credits, and **shall** surface the returned cost before spending.
- **REQ-021** (Ubiquitous) — The skill **shall** report `credits` (the billed figure), not `credits_exact`. The two diverge: `soul_2` returns `credits: 1` against `credits_exact: 0.12` — there is a rounding / minimum-charge floor.
- **REQ-022** (Event-driven) — **When** an MCP response carries an `adjustments` object, the skill **shall** surface every server-substituted default to the user. Without this, a user who asked for audio receives a silent video and is never told.
- **REQ-023** (State-driven) — **While** the account balance is known and the preflight cost exceeds it, the skill **shall** halt and report rather than submit a call that will queue indefinitely.

### §E.4 — Prompt craft

- **REQ-030** (Ubiquitous) — `media-higgsfield-core` **shall** carry the universal rules R1–R5 of §D.
- **REQ-031** (Ubiquitous) — The image skill **shall** carry exactly seven prompt-craft references: Soul, Nano Banana, OpenAI, Seedream, FLUX, Recraft, Marketing Studio.
- **REQ-032** (Ubiquitous) — The video skill **shall** carry exactly eight prompt-craft references: Veo, Kling, Seedance, Cinema Studio, Marketing Studio, Wan, Gemini Omni, Grok.
- **REQ-033** (Ubiquitous) — Every prompt-craft reference **shall** cite at least one source URL and **shall** declare its evidence tier.
- **REQ-034** (Unwanted) — **When** `research.md` records an evidenced *absence* of official guidance, the corresponding craft file **shall** state the absence explicitly and fall back to R1–R5. It **shall not** present an invented formula. Fabricating craft where the vendor published none is a defect, not a convenience. The three recorded absences are:
  - **Soul** — no official prompt formula exists; the vendor's stated philosophy is explicitly anti-formula.
  - **Grok** — no audio, dialogue, or sound-design guidance exists anywhere in xAI's documentation, *despite the MCP catalog tagging `grok_video_v15` as having native audio direction*.
  - **`openai_hazel`** — the model name appears nowhere in OpenAI's documentation; GPT Image conventions are applied on an explicitly flagged, unverified assumption.
- **REQ-035** (Capability gate) — **Where** a requested model falls outside the fifteen in-scope prompt-craft families, the skill **shall** handle it by live catalog lookup plus the universal rules, and **shall** say so. This is a stated scope boundary, not an omission.
- **REQ-036** (Unwanted) — The video skill **shall not** present a single generic video prompt formula. Per §B corollary, per-family craft is a correctness requirement.

### §E.5 — Family-specific workflow constraints

- **REQ-040** (Event-driven) — **When** the selected image model is `ms_image`, the skill **shall** call `show_marketing_studio(type='image_style')`, present the styles, and let the user pick. `style_id` has no default and is the dominant creative driver; the skill **shall not** auto-default it.
- **REQ-041** (Event-driven) — **When** the selected video model is `marketing_studio_video`, the skill **shall** enforce that `hook_id`/`setting_id` are mutually exclusive with `ad_reference_id`, that `product_ids` accompanies any hook, and that a portrait aspect is passed explicitly (the default is landscape 16:9).
- **REQ-042** (Ubiquitous) — The skills **shall** carry the following hazard warnings verbatim in intent:
  - `gemini_omni` video-references are **known-broken in Google's own words** — accepted by the API schema, not correctly processed by the model.
  - `minimax_hailuo` camera commands **may be silently overridden** — MiniMax's `prompt_optimizer` defaults on, and Higgsfield does not expose the switch to disable it.
  - Grok's catalog "native audio" tag is **not backed by any xAI documentation**.

### §E.6 — Drift elimination

- **REQ-050** (Unwanted) — The rewritten skills **shall not** contain any of the invented model IDs (`sora_2`, `veo_3`, `kling_2_5_turbo`, `kling_2_1_master`, `kling_avatars_2_0`, `seedance_pro`, `cinema_studio_3_5`, `minimax_hailuo_02`, `wan_2_5`, `soul_2_0`, `seedream_4_0`, `wan_2_2_image`).
- **REQ-051** (Unwanted) — The rewritten skills **shall not** contain the non-existent parameter names (`width_and_height`, `duration_seconds`, `image_url`, `enhance_prompt`, `style_strength`, `custom_reference_id`, `image_reference_url`), except inside an explicitly-labelled anti-pattern section of `media-higgsfield-core/references/call-schema.md`. `batch_size` is valid **only** on `ms_image` and **shall** be named only in that context.

### §E.7 — End-to-end proof

- **REQ-060** (Event-driven) — **When** the skills are complete, the implementation **shall** prove both modalities end-to-end against the live MCP: a `get_cost: true` preflight on at least one representative model per modality (zero credits), then one real image and one real video generation, each polled to `completed` with a result URL returned.
- **REQ-061** (State-driven) — **While** the observed balance is 10 credits on the free plan, total E2E spend **shall not** exceed it. The budget-safe pair is `soul_2` (1 credit) + `veo3_1_lite` at 4s (4 credits) = 5 credits, with alternates recorded in `mcp-catalog-snapshot.md` §5.1.

---

## §F — Out of Scope

This SPEC states its boundaries explicitly. Each exclusion below is a deliberate decision with a reason, not an oversight.

### Out of Scope — the 45 catalog models outside the 15 prompt-craft families

- The catalog carries 30 image + 30 video models. Fifteen families receive a static, cited craft file. Every other model — `grok_image`, `kling_omni_image`, `z_image`, `image_auto`, `autosprite`, `clipify`, `higgsfield_preset`, `explainer_video`, the upscalers, the background removers, and the rest — is handled by **live catalog lookup plus the universal rules R1–R5**.
- This is the design working as intended: the live-query layer covers the whole catalog; the craft layer covers the families where the vendor published guidance worth curating.

### Out of Scope — audio and 3D model families

- The catalog's 5 audio models (`seed_audio`, `text2speech_v2`, `sonilo_music`, `mirelo_text_to_audio`, `inworld_text_to_speech`) and 8 3D models (`sam_3_3d`, the Meshy family, `tripo_3d`) are excluded.
- `moai-media` currently routes audio through the ElevenLabs MCP (`media-audio-gen`). Higgsfield's audio surface overlaps it and is a candidate for a follow-up SPEC — not a silent absorption here.

### Out of Scope — MCP surface and vendor behavior

- No change to `plugins/moai-media/.mcp.json` beyond verifying the registration still resolves.
- No attempt to work around vendor-side defects. The `gemini_omni` broken video-references and the `minimax_hailuo` silent camera override are **warned about**, not patched. A skill cannot fix a model.
- The `seedream_v5_pro` overlay-marker editing capability (coordinate points, doodles) is not exposed through the MCP; the craft file records it as a platform-surface limitation and does not attempt to synthesize it.

### Out of Scope — the snapshot as a runtime contract

- `mcp-catalog-snapshot.md` is a **point-in-time plan-phase evidence baseline**, not a source of truth for the runtime skill. The skill must re-query live. Any implementation that reads model IDs or enums *out of the snapshot* has reintroduced the exact defect this SPEC removes.

### Out of Scope — new research

- `research.md` is complete, cited, and evidence-tiered. The run phase authors craft files **from it**. Re-deriving the research, or supplementing it with third-party guides listed in its §6 "explicitly NOT used as evidence" ledger, is prohibited.

---

## §G — Cross-References

| Artifact | Role |
|---|---|
| `research.md` | Prompt-craft evidence base — 15 families, per-vendor official conventions, evidence tiers, gap register (G1–G10), source ledger |
| `mcp-catalog-snapshot.md` | Parameter evidence base — live 60-model catalog, true call schema, observed credit costs, drift ledger |
| `plan.md` | Milestones, decisions, constraints, risks |
| `acceptance.md` | Mechanically-verifiable acceptance criteria + pinned-literal registry |
| `plugins/moai-media/.mcp.json` | Higgsfield MCP registration (`https://mcp.higgsfield.ai/mcp`) |
