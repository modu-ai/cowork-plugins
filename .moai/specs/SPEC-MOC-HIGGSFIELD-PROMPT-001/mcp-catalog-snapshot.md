# Higgsfield MCP — Live Catalog Snapshot

**Captured**: 2026-07-12
**Method**: direct `models_explore(action: "list", type: <image|video|audio|3d>)` calls against the live Higgsfield MCP endpoint (`https://mcp.higgsfield.ai/mcp`), authenticated session.
**Status**: OBSERVED — every row below is verbatim from the MCP response. Nothing here is inferred.
**Purpose**: this file is the plan-phase evidence baseline. It is a *point-in-time* snapshot, NOT a source of truth for the runtime skill — the runtime skill MUST re-query `models_explore` live. See `spec.md` § Design Principle.

---

## 0. Call-Schema Ground Truth

The generation tools take a **nested `params` object**, not flat top-level arguments.

### `generate_image`

```
generate_image({
  params: {
    model:        <string, REQUIRED>   // model id from the catalog
    prompt:       <string>             // text description
    aspect_ratio: <string>             // must be one of the model's declared aspect_ratios
    count:        <int 1-4, default 1> // number of parallel jobs
    medias:       [{ role: <string>, value: <media_id|job_id> }]
    get_cost:     <bool>               // true = return credit cost, submit NO job
    ...<model-specific top-level params, e.g. resolution / quality / soul_id>
  }
})
```

### `generate_video`

```
generate_video({
  params: {
    model:        <string, REQUIRED>
    prompt:       <string>             // optional for Marketing Studio workflows
    aspect_ratio: <string>
    duration:     <int>                // seconds; must satisfy the model's durations / duration_range
    count:        <int 1-4>
    medias:       [{ role: <string>, value: <media_id|job_id> }]
    preset_id:    <string>             // ONLY with model: higgsfield_preset
    get_cost:     <bool>
    ...<model-specific top-level params>
  }
})
```

### HARD constraints observed in the tool schema

| Constraint | Detail |
|---|---|
| `medias[].value` | MUST be a `media_id` (from `media_upload` / `media_import_url`) or a `job_id` from a prior generation. A raw `https://` URL is REJECTED. |
| `medias[].role` | Model-specific. Inspect the model's declared `medias[].roles`. Common: `image`, `image_references`, `start_image`, `end_image`, `video_references`, `audio_references`, `input_video`, `input_audio`. |
| `aspect_ratio` | Must be in the model's declared `aspect_ratios` list. Some models declare `[]` (aspect not applicable). |
| `duration` | Models declare EITHER `durations: [5,10]` (enum) OR `duration_range: {min,max}` (range). Unsupported values are clamped or snapped to the nearest allowed. |
| `get_cost: true` | Preflight — returns credit cost WITHOUT submitting a job. Zero credit consumption. Also surfaces parameter-validation errors. |
| `count` vs `batch_size` | `count` (1-4) = number of parallel JOBS. `batch_size` (only on `ms_image`, 1-20) = images per job. They are distinct. |
| Tool namespace | Depends on registration. Plugin `.mcp.json` (server name `higgsfield`) → `mcp__higgsfield__*`. Claude Desktop connector → `mcp__claude_ai_higgsfield__*`. The skill MUST resolve the namespace at runtime, not hard-code one. |

### Anti-pattern: parameters that DO NOT EXIST

The following appear in the current (pre-SPEC) skill bodies and are **not in the live schema**. Passing them is at best ignored, at worst an error:

`width_and_height` · `quality` as a flat top-level arg on `generate_image` · `batch_size` (except on `ms_image`) · `enhance_prompt` · `style_id` (except on `ms_image`, where it is REQUIRED) · `style_strength` · `seed` (except on some 3D models) · `custom_reference_id` · `image_reference_url` · `image_url` · `duration_seconds` · `preset` (the field is `preset_id`, and only for `higgsfield_preset`)

---

## 1. Image Models (30)

Notation: `param[options]=default`.

### In-scope prompt-craft families (7)

| Model ID | Name | Provider | Params | Aspect ratios | medias roles |
|---|---|---|---|---|---|
| `soul_2` / `soul_v2` | Higgsfield Soul 2.0 | Higgsfield | `quality[1.5k\|2k]=2k`, `soul_id` | 1:1 16:9 9:16 4:3 3:4 3:2 2:3 | `image` (max 1) |
| `soul_cinematic` | Soul Cinema | Higgsfield | `quality[1.5k\|2k]=2k`, `soul_id` | 1:1 4:3 3:4 16:9 9:16 3:2 2:3 21:9 | `image` (max 1) |
| `soul_cast` | Soul Cast | Higgsfield | `budget[10-500]=50` | 16:9 only | — (text-only) |
| `soul_location` | Soul Location | Higgsfield | — | 1:1 4:3 3:4 16:9 9:16 3:2 2:3 21:9 9:21 | — |
| `nano_banana_pro` | Nano Banana Pro | Google | `resolution[1k\|2k\|4k]=1k` | 1:1 3:2 2:3 4:3 3:4 4:5 5:4 9:16 16:9 21:9 | `image` |
| `nano_banana_2` | Nano Banana 2 | Google | `resolution[1k\|2k\|4k]=1k` | same as above | `image` |
| `nano_banana_2_lite` | Nano Banana 2 Lite | Google | `resolution[1k]=1k`, `thinking[MINIMAL\|HIGH]=HIGH` | auto + above | `image_references` |
| `nano_banana` | Nano Banana | Google | — | same | `image_references` |
| `nano_banana_2_shots` | Nano Banana Pro (alias) | — | — | auto + above | `image_references` |
| `gpt_image_2` | GPT Image 2 | OpenAI | `resolution[1k\|2k\|4k]=1k`, `quality[low\|medium\|high]=low` | 1:1 4:3 3:4 16:9 9:16 3:2 2:3 | `image` |
| `openai_hazel` | OpenAI Hazel | OpenAI | `quality[low\|medium\|high]=medium` | 1:1 3:2 2:3 auto | `image_references` |
| `seedream_v5_pro` | Seedream 5.0 Pro | Bytedance | `resolution[1k\|1.5k\|2k]=2k` | 1:1 4:3 3:4 16:9 9:16 3:2 2:3 21:9 | `image_references` |
| `seedream_v5_lite` | Seedream 5.0 lite | Bytedance | `quality[basic\|high]=basic` | 1:1 16:9 9:16 4:3 3:4 | `image` |
| `seedream_v4_5` | Seedream 4.5 | Bytedance | `quality[basic\|high]=basic` (basic≈4K, high≈6K) | 1:1 4:3 16:9 3:2 21:9 3:4 9:16 2:3 | `image_references` |
| `flux_2` | FLUX.2 | Black Forest Labs | `resolution[1k\|2k]=1k`, `variant[pro\|flex\|max]=pro` | 1:1 4:3 3:4 16:9 9:16 | `image_references` |
| `flux_kontext` | Flux Kontext | Black Forest Labs | — | 1:1 4:3 3:4 16:9 9:16 | `image_references` |
| `recraft_v4_1` | Recraft V4.1 | Recraft | `resolution[1k\|2k]=1k`, `model_type[standard\|vector\|utility\|utility_vector]=standard`, `colors[]` (≤10 `#RRGGBB`), `background_color` | 1:1 3:4 4:3 4:5 5:4 3:2 2:3 16:9 9:16 | — |
| `marketing_studio_image` | Marketing Studio Image | Higgsfield | `resolution[1k\|2k\|4k]=1k` | auto + 10 more | `image` |
| `ms_image` | DTC Ads | Higgsfield | **`style_id` REQUIRED**, `brand_kit_id`, `resolution[1k\|2k\|4k]=1k`, `quality[low\|medium\|high]=low`, `batch_size[1-20]=1`, `product_ids[]` (≤4), `folder_id` | 15 ratios incl. 27:16, 9:8, 4:9 | `image` (max 14) |

**`ms_image` pre-call workflow (HARD)**: `style_id` has no default. `generate_image(model='ms_image')` without it **errors**. The MCP mandates: call `show_marketing_studio(type='image_style')` FIRST, let the user pick a style, only then generate. Style is the dominant creative driver.

### Out-of-scope (live-lookup only) — 13

`grok_image` (xAI; `resolution[1k|2k]`, `mode[std|quality]`) · `kling_omni_image` (Kling O1; `resolution[1k|2k]`) · `z_image` (Tongyi-MAI; fast/budget, no params) · `cinematic_studio_2_5` (Cinema Studio Image 2.5; `resolution[1k|2k|4k]`) · `image_auto` (auto-routing) · `autosprite` (game sprite sheets; `kind`, `frame_count`, `video_tier`…) · `image_background_remover` · `outpaint` · `topaz_image` · `topaz_image_generative` · `bytedance_image_upscale`

> Note: `cinematic_studio_2_5` is Higgsfield-native and belongs conceptually to the Cinema Studio family; it is covered by the Cinema Studio video reference's craft notes plus live lookup.

---

## 2. Video Models (30)

### In-scope prompt-craft families (8)

| Model ID | Name | Provider | Params | Aspect | Duration | medias roles |
|---|---|---|---|---|---|---|
| `veo3` | Google Veo 3 | Google | `variant[veo-3-preview\|veo-3-fast]=veo-3-fast` | 16:9 9:16 | — | `start_image` |
| `veo3_1` | Google Veo 3.1 | Google | `duration[4\|6\|8]=8`, `quality[basic\|high\|ultra]=basic`, `variant[veo-3-1-preview\|veo-3-1-fast]=veo-3-1-fast` | 16:9 9:16 | 4/6/8 | `start_image` |
| `veo3_1_lite` | Veo 3.1 Lite | Google | `duration[4\|6\|8]=8`, `generate_audio=false` | 16:9 9:16 auto | 4/6/8 | `start_image`, `end_image` |
| `kling3_0` | Kling v3.0 | Kling | `duration[3-15]=5`, `mode[std\|pro\|4k]=std`, `sound[on\|off]=on` | 16:9 9:16 1:1 | 3-15 | `start_image`, `end_image` |
| `kling3_0_turbo` | Kling 3.0 Turbo | Kling | `resolution[720p\|1080p]=720p`, `duration[3-15]=5` | 16:9 9:16 1:1 | 3-15 | `start_image` |
| `kling2_6` | Kling 2.6 Video | Kling | `duration[5\|10]=5`, `sound=true` | 16:9 9:16 1:1 | 5/10 | `start_image` |
| `seedance_2_0` | Seedance 2.0 | Bytedance | `duration[4-15]=5`, `resolution[480p\|720p\|1080p\|4k]=720p`, `mode[std\|fast]=std`, `bitrate_mode[standard\|high]`, `genre[auto\|action\|horror\|comedy\|noir\|drama\|epic]=auto`, `generate_audio=true` | auto 16:9 9:16 4:3 3:4 1:1 21:9 | 4-15 | `start_image`, `end_image`, `image_references`, `video_references`, `audio_references` |
| `seedance_2_0_mini` | Seedance 2.0 Mini | Bytedance | as above, `resolution[480p\|720p]` only | same | 4-15 | same |
| `seedance1_5` | Seedance 1.5 Pro | Bytedance | `duration[4\|8\|12]=4`, `resolution[480p\|720p\|1080p]=720p`, `generate_audio=true` | auto + 6 | 4/8/12 | `start_image`, `end_image` |
| `cinematic_studio_3_0` | Cinema Studio Video 3.0 | Higgsfield | `resolution[480p\|720p\|1080p\|4k]=720p`, `genre[auto\|action\|horror\|comedy\|noir\|drama\|epic]=auto`, `generate_audio=false` | auto 21:9 16:9 4:3 1:1 3:4 9:16 | 4-15 | `image`, `start_image`, `end_image` |
| `cinematic_studio_video_v2` | Cinema Studio Video | Higgsfield | `genre[auto\|action\|horror\|comedy\|western\|suspense\|intimate\|spectacle]=auto`, `mode[pro\|std]=std`, `sound[on\|off]=on`, `speedramp[auto\|custom\|linear\|slowmo\|speedup\|impact]=auto`, `multi_shots=false`, `multi_shot_mode[auto\|custom]=custom`, `cfg_scale[0-1]=0.5`, `preset_id` | 1:1 4:3 3:4 16:9 9:16 | 3-12 | `image`, `start_image`, `end_image` |
| `cinematic_studio_video` | Cinema Studio Video (v1) | Higgsfield | `slow_motion=false`, `sound=true` | 1:1 4:3 3:4 16:9 9:16 | 5/10 | `image`, `start_image`, `end_image` |
| `marketing_studio_video` | Marketing Studio | Higgsfield | `resolution[480p\|720p\|1080p]=720p`, `generate_audio=true`, `mode` (preset slug), `folder_id`, `width`, `height`, `avatar_ids[]` (max 1), `product_ids[]`, `assets[]`, `hook_id`, `setting_id`, `ad_reference_id` | auto 21:9 16:9 4:3 1:1 3:4 9:16 | 12-15 | `avatars`, `medias` (`image`/`start_image`/`end_image`) |
| `wan2_6` | Wan 2.6 Video | Wan | `quality[720p\|1080p]=720p`, `duration[5\|10\|15]=5` | 16:9 9:16 1:1 | 5/10/15 | `image_references`, `video_references`, `audio_references` |
| `wan2_7` | Wan 2.7 | Wan | `duration[2-15]=5`, `resolution[720p\|1080p]=720p` | 16:9 9:16 1:1 4:3 3:4 | 2-15 | `start_image`, `end_image`, `audio_references` |
| `grok_video` | Grok Video | xAI | `duration[1-15]=5` | 16:9 9:16 1:1 | 1-15 | `start_image` |
| `grok_video_v15` | Grok Video 1.5 | xAI | `resolution[480p\|720p]=720p`, `duration[2-15]=5` | — | 2-15 | `start_image` |
| `gemini_omni` | Gemini Omni Flash | Google | `duration[4-10]=8`, `resolution[720p]=720p` | 16:9 9:16 | 4-10 | `image_references`, `video_references` |
| `minimax_hailuo` | Minimax Hailuo | Hailuo | `variant[minimax\|minimax-fast\|minimax-2.3\|minimax-2.3-fast]=minimax-2.3`, `duration[6\|10]=6`, `resolution[512\|768\|1080]=768` | — | 6/10 | `start_image`, `end_image` |

**`marketing_studio_video` composition rules (HARD, from the MCP schema)**:
- `hook_id` (the "what" — attention mechanic) and `setting_id` (the "where" — location/vibe) are **INDEPENDENT** of each other (pass either, both, or neither).
- `hook_id`/`setting_id` are **MUTUALLY EXCLUSIVE** with `ad_reference_id`. Hook/setting compose from explicit building blocks; `ad_reference_id` recreates an existing video's scenario. Pick one approach, never both.
- Hooks/settings are supported ONLY for presets: **UGC, Tutorial, Unboxing, Product Review, UGC Virtual Try On**.
- `ad_reference_id` does **NOT** auto-pull its linked avatar/product — they MUST be passed explicitly as `avatar_ids` / `product_ids` on the generate call.
- `product_ids` is plural-array only. `product_id` (singular) is rejected.
- Default aspect is landscape 16:9 — pass `9:16` **explicitly** for TikTok/Reels.

**`higgsfield_preset` (preset-routed i2v)**: `preset_id` REQUIRED (from `presets_show`); `medias: [{role: 'image'}]` REQUIRED (max 1). Aspect 16:9/9:16/1:1.

### Out-of-scope (live-lookup only)

`clipify` (Personal Clipper — YouTube → clips; `urls[]` required, `clips_num`, `clip_aspect`, subtitle styling) · `higgsfield_preset` · `explainer_video` · `sync_so` (Lipsync) · `video_background_remover` · `sam_3_video` · `topaz_video` · `bytedance_video_upscale` · `video_upscale` · `video_deflicker` · `llm_text`

---

## 3. Audio Models (5) — OUT OF SCOPE for this SPEC

`seed_audio` (ByteDance TTS) · `text2speech_v2` (Higgsfield; `variant[elevenlabs|minimax|seed_speech|vibe_voice|cozy_voice]`) · `sonilo_music` (FAL, game-pipeline only) · `mirelo_text_to_audio` (FAL SFX, game-pipeline only) · `inworld_text_to_speech` (FAL; 120+ named voices incl. 4 Korean)

> The `moai-media` plugin currently routes audio through the ElevenLabs MCP (`media-audio-gen` skill). Higgsfield's own audio surface overlaps and is a candidate for a follow-up SPEC. Explicitly out of scope here.

## 4. 3D Models (8) — OUT OF SCOPE for this SPEC

`sam_3_3d` (Meta) · `image_to_3d` / `meshy_image_to_3d` (Meshy) · `multi_image_to_3d` / `meshy_multi_image_to_3d` · `3d_rigging` / `meshy_rigging` · `tripo_3d` (text-to-3D; **has a `negative_prompt` param — the only model in the catalog that does**)

---

## 5. Supporting MCP Surface (self-documenting)

| Tool | Role in the runtime flow |
|---|---|
| `models_explore(list/search/get/recommend)` | **Catalog SSOT.** `get` returns one model's exact constraints; `recommend` takes a goal + input context. |
| `presets_show` | Preset catalog for `higgsfield_preset`. |
| `show_marketing_studio(type=image_style\|brand_kit\|product\|hook\|setting\|ad_reference)` | Mandatory pre-call listing for `ms_image` / `marketing_studio_video`. |
| `get_workflow_instructions()` | Made-to-brief workflow catalog. Currently returns 1 workflow: `video-explainer` (narrated non-photoreal explainer/story video). Call with no arg for the catalog, then with `{workflow}` for full instructions. |
| `media_upload` / `media_upload_widget` / `media_import_url` | Turn a local file or web URL into a `media_id` for `medias[].value`. |
| `job_status` / `job_display` | Async job polling. |
| `balance` | Credit balance. **Observed 2026-07-12: 10 credits, `free` plan.** |
| `animation_actions` | 678-action library for 3D rig animation. |

### 5.0.1 `style_id` vs `format_id` — conflict RESOLVED by live call

Higgsfield's official agent docs (`github.com/higgsfield-ai/skills`, `references/marketing-dtc-ads.md`) state the mandatory DTC-ads field is **`format_id`**. The live MCP `generate_image` schema states it is **`style_id`**. These are **not contradictory** — they describe two different surfaces:

- **`format_id`** = the **CLI** surface (`higgsfield marketing-studio …`).
- **`style_id`** = the **MCP** surface. **For MCP calls, `style_id` governs.**

Confirmed by an actual `show_marketing_studio(action='list', type='image_style')` call, which returned **42 image styles**, each with a UUID `id` — these UUIDs are what `style_id` takes. Examples: `Headline`, `Special Offer`, `Customer Quote`, `Key Features`, `Social Proof`, `Then vs Now`, `Comparison Table`, `App Screenshot`, `Whiteboard Explainer`, `UGC Side-by-Side`, `Bold Statement`.

The same response ALSO returned the **video preset catalog** — the `mode` slugs for `marketing_studio_video`. There are **26 presets**, not the 6 the current skill claims:

`ugc` · `ugc_gadget_saved_me` · `ugc_giant_figure` · `ugc_unboxing_virtual_try_on` · `ugc_unboxing_asmr` · `ugc_virtual_try_on_sneakers` · `couple_sharing_home` · `ugc_selfie_testimonial` · `ugc_direct_to_camera` · `ugc_secret_hack_reveal` · `crush_test` · `hypermotion_oj` · `camera_pov` · `classic_meets_modern` · `mess_to_fresh` · `mystery_box` · `product_showcase` · `reboxing` · `tv_spot` · `ugc_addiction` · `ugc_before_and_after` · `ugc_how_to` (Tutorial) · `ugc_unboxing` · `ugc_virtual_try_on` · `virtual_try_on` (Pro) · `wild_card`

Hook/setting composition is gated to these 5 slugs only: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`.

**Doctrine consequence**: this is a second, independent proof of the SPEC's core design principle. Even Higgsfield's OWN official documentation disagrees with Higgsfield's OWN live MCP schema on a field name. A skill that hard-codes either one is wrong half the time. The skill MUST query the live surface (`models_explore` / `show_marketing_studio` / `presets_show`) and treat every static doc — including the vendor's own — as craft guidance, never as a parameter contract.

---

## 5.1 Observed Credit Costs (`get_cost: true`, 2026-07-12)

Every row below was obtained by an actual `get_cost: true` preflight call. **Zero credits consumed.** These are OBSERVED values, not estimates.

### Image (per job, count=1)

| Model | Params used | `credits` | `credits_exact` |
|---|---|---:|---:|
| `z_image` | 1:1 | **0.15** | 0.15 |
| `soul_2` | 16:9, quality=2k | **1** | 0.12 |
| `flux_2` | 1:1, 1k, variant=pro | **1** | 1 |
| `nano_banana_pro` | 16:9, resolution=2k | **2** | 2 |
| `gpt_image_2` | 16:9, 1k, quality=medium | **2** | 2 |
| `recraft_v4_1` | 1:1, model_type=vector | **2.5** | 2.5 |
| `openai_hazel` | 1:1, quality=medium | **4** | 4 |

### Video (per job, count=1)

| Model | Params used | `credits` |
|---|---|---:|
| `veo3_1_lite` | 16:9, 4s | **4** |
| `kling3_0_turbo` | 16:9, 5s, 720p | **7.5** |
| `seedance_2_0_mini` | 16:9, 5s, 720p | **12.5** |
| `wan2_6` | 16:9, 5s, 720p | **13** |
| `cinematic_studio_3_0` | 16:9, 5s, 720p | **25** |

### Two mechanics discovered by these calls

1. **`credits` vs `credits_exact` diverge.** `soul_2` returned `credits: 1` but `credits_exact: 0.12` — there is a rounding / minimum-charge floor. The skill MUST surface `credits` (what is actually billed), not `credits_exact`.
2. **`adjustments` is returned when the server fills a default.** The `cinematic_studio_3_0` preflight returned:
   ```json
   "adjustments": {
     "params.genre":          {"requested":"(unset)","used":"auto",  "reason":"default for model"},
     "params.generate_audio": {"requested":"(unset)","used":false,   "reason":"default for model"}
   }
   ```
   The `generate_*` tool descriptions instruct "apply `adjustments`". The skill MUST read this field back and report to the user what the server silently substituted — otherwise a user asking for audio gets a silent-default silent video.

### Budget implication for this SPEC's E2E acceptance criterion

Balance is **10 credits (free plan)**. Both an image AND a video E2E generation fit:

- image `soul_2` (1) + video `veo3_1_lite` 4s (4) = **5 credits** — comfortable headroom
- image `z_image` (0.15) + video `kling3_0_turbo` 5s (7.5) = **7.65 credits** — also fits

This **overturns** the plan-phase assumption that a video E2E was unaffordable. Both skills can be proven end-to-end within the existing balance.

---

## 6. Drift Ledger — current skill bodies vs live catalog

Verified by direct comparison of `plugins/moai-media/skills/media-higgsfield-{image,video}/SKILL.md` against this snapshot.

| Skill claim | Reality |
|---|---|
| `sora_2` listed as the ★ top video model | **Sora 2 does not exist in the catalog.** |
| `veo_3`, `kling_2_5_turbo`, `kling_2_1_master`, `kling_avatars_2_0`, `seedance_pro`, `cinema_studio_3_5`, `minimax_hailuo_02`, `wan_2_5` | None of these IDs exist. Real: `veo3`, `kling3_0_turbo`, `kling2_6`, `seedance_2_0`, `cinematic_studio_3_0`, `minimax_hailuo`, `wan2_6`/`wan2_7`. |
| "11 image models" incl. `Wan 2.2 Image`, `GPT Image` (1st gen), `Seedream 4.0` | 30 image models. Those three IDs do not exist. Missing entirely: `openai_hazel`, `recraft_v4_1`, `flux_2`, `grok_image`, `kling_omni_image`, `z_image`, `soul_cast`, `soul_location`, `ms_image`, `marketing_studio_image`, `image_auto`, `nano_banana_2*`. |
| "6 video presets (UGC / Unboxing / Product review / Hyper motion / TV spot / Wild Card)" | Not a `preset` param. Marketing Studio uses `mode` (preset slug from `show_marketing_studio`), plus `hook_id`/`setting_id`. `higgsfield_preset` uses `preset_id` from `presets_show`. |
| Flat params (`width_and_height`, `quality`, `batch_size`, `enhance_prompt`, `duration_seconds`, `image_url`, `preset`, `seed`, `custom_reference_id`) | None exist in the live schema. See § 0 anti-pattern list. |
| `mcp__higgsfield__generate_image` | Namespace is registration-dependent; must be resolved at runtime. |

**Conclusion**: the existing skills are not merely stale — following them produces failed or silently-ignored calls. This SPEC's primary correctness goal is to eliminate this entire class of drift by making the runtime skill query the catalog instead of trusting a hard-coded table.
