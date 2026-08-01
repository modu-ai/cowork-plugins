# research.md — SPEC-MOC-HIGGSFIELD-PROMPT-001

**Phase**: plan (Deep Research)
**Method**: 5 parallel research subagents (Mode 4 fan-out), each instructed to fetch every cited URL itself, to never fabricate a formula the source does not state, and to report evidenced ABSENCE rather than substitute third-party content as official.
**Companion artifact**: `mcp-catalog-snapshot.md` (live MCP catalog + call schema + observed credit costs). This file covers PROMPT CRAFT; that file covers PARAMETERS. The separation is the SPEC's core thesis.

---

## §1 — The Central Finding: two axes, two sources of truth

Research produced **three independent proofs** that a hard-coded parameter table is structurally wrong, and that prompt craft and parameters must be sourced separately.

### Proof 1 — the existing skill is not stale, it is non-functional
The current `media-higgsfield-{image,video}` skills document a `sora_2` model that does not exist, seven other model IDs that do not exist, and a flat parameter shape (`width_and_height`, `duration_seconds`, `image_url`, `batch_size`) that the live schema does not accept. See `mcp-catalog-snapshot.md` §6.

### Proof 2 — Higgsfield's own docs disagree with Higgsfield's own MCP
Higgsfield's official agent documentation (`github.com/higgsfield-ai/skills`, `references/marketing-dtc-ads.md`) states the mandatory DTC-ads field is **`format_id`**. The live MCP `generate_image` schema states it is **`style_id`**. Both are correct — for different surfaces (CLI vs MCP). A skill that hard-codes either is wrong half the time. Resolved by a live `show_marketing_studio` call (see snapshot §5.0.1).

### Proof 3 — the platform's craft guide contradicts the model vendor's craft guide
Higgsfield's blog guide for Seedance prescribes **timeline/beat prompting with explicit timestamps**. ByteDance's own official prompt guide for the same model says the opposite, verbatim:

> *"The model's support for precise timing (such as 0–3 seconds) is unstable, and forcibly limiting duration may lead to abnormal generation results."*
> — BytePlus ModelArk, Seedance 2.0 prompt guide (`docs.byteplus.com/en/docs/ModelArk/2222480`)

**Resolution rule adopted by this SPEC**: for prompt craft, **the model vendor's documentation outranks the hosting platform's**. Higgsfield is a re-proxy; ByteDance trained the model. Where the two conflict, cite the vendor and note the conflict.

### The resulting doctrine

| Axis | Source of truth | How the skill obtains it |
|---|---|---|
| **Parameters** (model IDs, enums, aspect ratios, durations, media roles, cost) | The **live MCP** | `models_explore(get)` / `show_marketing_studio` / `presets_show` / `get_cost` at call time. **Never hard-coded.** |
| **Prompt craft** (formula, structure, audio syntax, negative-expression, reference conventions) | The **model vendor's official docs** | Static, curated per family into `references/prompt-craft/*.md`. Frozen at authoring time, cited, with evidence tier. |

Higgsfield's own docs confirm this design independently. Their `references/` instructs agents: **"When unsure, run `higgsfield model get <model>` and inspect the schema"** — the vendor itself refuses to publish a static parameter contract.

---

## §2 — Cross-Family Universal Rules (promote to `media-higgsfield-core`)

These rules were independently confirmed across **three or more vendors** and belong in the shared core skill, not in per-family files.

### R1 — Negative prompts do not exist. Express exclusions as positive scene content.

Higgsfield's MCP exposes **no `negative_prompt` field on any image or video model** (sole exception: `tripo_3d`, out of scope). Independently, the vendors converge on the same authoring rule:

| Vendor | Verbatim guidance |
|---|---|
| **Google (Veo)** | *"To refine your output, describe what you wish to exclude. For example, specify 'a desolate landscape with no buildings or roads' instead of 'no man-made structures'."* |
| **Black Forest Labs (FLUX.2)** | FLUX.2 **does not support negative prompts** at all. Instead of "no blur" say *"sharp focus throughout"*; instead of "no people" describe *"an empty scene."* |
| **Kling** | *"It is recommended to supplement negative prompt via negative sentences within positive prompts."* — Kling recommends this **even though its own API has a negative_prompt field**. |
| **Higgsfield** (`prompt-engineering.md`) | Use positive framing — *"tack sharp"* rather than *"not blurry."* |
| **Google (Nano Banana)** | *"empty street"*, not *"no cars."* |

**Rule**: the skill NEVER emits a `negative_prompt` parameter and NEVER writes bare negation. Exclusions become described scene content.

### R2 — For image-to-video, drop what the start image already supplies.

Only two vendors state this explicitly, and they agree:

- **Wan (Alibaba, official)**: the image-to-video formula is literally **`Motion + Camera movement`** — *"Focus prompt on movement descriptions and specific camera directions rather than static elements."*
- **Higgsfield** (`prompt-engineering.md`): don't restate static visual info already present in the input image; use action verbs for motion.

**Rule**: when `medias[].role` includes `start_image`/`image`, the assembled prompt drops subject/scene re-description and leads with motion + camera.

### R3 — Literal in-image text goes in quotation marks, with the font named.

Confirmed independently by Google, OpenAI, BFL, and Recraft. Google's worked example (verbatim):

> *"For the top line, the word 'GLOW' in a flowing, elegant Brush Script font. For the middle line, the text '10% OFF' in a heavy, blocky Impact font."*

**Rule**: literal text → double quotes + explicit font/weight/placement. This is the single highest-leverage convention for the text-rendering models (`gpt_image_2`, `openai_hazel`, `nano_banana_pro`).

### R4 — Editing prompts: name what changes AND what must be preserved.

- **OpenAI**: *"Change only X"* + *"keep everything else the same"*; repeat the preservation list every iteration to prevent drift.
- **BFL Kontext**: `Replace '[original text]' with '[new text]'`. Verb choice is load-bearing — *"change"* preserves identity, *"transform"* signals a full identity change. Anchor the subject explicitly: *"Change the background to a beach while keeping the person in the exact same position, scale, and pose."*
- **ByteDance Seedream**: *"Replace the largest bread man with a croissant man, **keeping the action and expression unchanged**."*
- **Google (Gemini Omni)**: **inverse warning** — *"Simple prompts work best for video editing. Overly descriptive prompts can lead to unintended changes."*

**Rule**: edit prompts are short, name the single change, and enumerate invariants.

### R5 — Prompt length: no universal cap. Vendor-specific, and mostly unstated.

| Family | Official length guidance | Tier |
|---|---|---|
| Higgsfield (general) | **~200 tokens** soft ceiling — *"lengthier requests cause model distortion"* | 1차 |
| OpenAI GPT Image | **32,000 char** hard cap; no recommended length | 1차 |
| FLUX.2 | 10–30 words (explore) / **30–80 words (stated ideal)** / 80–300+ (complex). 32K token cap. | 1차 |
| Kling | **2,500 chars** (confirmed on `negative_prompt`; symmetry assumed for `prompt`) | 1차 (relayed) |
| MiniMax | **2,000 chars** | 1차 |
| Google Veo / Nano Banana | **No cap stated.** (Sibling Imagen: 480 tokens — directional only) | 1차 |
| Wan | **No cap stated** — guide deliberately declines to prescribe one | 1차 |
| ByteDance Seedance / Seedream | **No cap stated** — explicitly confirmed absent by direct search | 1차 |

**Note the internal contradiction in Higgsfield's own materials**: the ~200-token ceiling in `prompt-engineering.md` is violated by Higgsfield's own Cinema Studio worked examples, which run 500+ words. Reported as-is, not reconciled.

---

## §3 — Per-Family Craft Notes (IMAGE, 7 families)

### 3.1 Soul (`soul_2` / `soul_v2`, `soul_cinematic`, `soul_cast`, `soul_location`) — Higgsfield

**⚠ NO OFFICIAL PROMPT FORMULA EXISTS.** This is an evidenced absence, not a research gap. `soul-intro`, `soul-cinema`, and the Soul how-to pages are feature-overview marketing pages carrying zero prompt-craft guidance. Higgsfield's stated design philosophy is explicitly **anti-formula**: Soul is built so users *"name a look instead of describing it technically"*, leaning on presets and moodboards.

**Do not invent a Soul formula.** The skill falls back to the R1–R5 universal rules plus Higgsfield's general `prompt-engineering.md`.

**What IS documented — identity/consistency mechanics (1차):**
- **Soul ID**: train on **20+ photos** of one person; ~3–5 min. Learns facial structure, skin tone, hair texture, proportions; holds them *"regardless of preset, lighting, angle or prompt."* Photo requirements: well-lit, no sunglasses, no heavy shadows, no cropped faces; vary angle and expression; include one full-height shot for body proportion; photos from the last 4–5 months. Vendor caveat, verbatim: *"Consistency is high, not absolute — extreme style shifts may introduce minor drift."*
- **Referencing is by selection, not prompt syntax.** No inline `soul_id:` prompt token exists. The `soul_id` MCP param is the binding mechanism.
- **Soul Cast is explicitly NOT prompt-driven** — *"Build, don't describe."* It is parameterized by 8 categories: Genre (14 options), Budget (slider — higher = *"refined, blockbuster-grade"*, lower = *"grittier, more indie"* — this is what the `budget[10-500]` MCP param drives), Era, Archetype (12 Jungian types), Identity, Physical Appearance, Details, Outfit. The MCP catalog independently confirms `soul_cast` is text-only with no media refs.

**Evidence tier**: 1차 for mechanics. **none-found** for prompt formula and exemplar prompts.

### 3.2 Nano Banana (`nano_banana_pro`, `nano_banana_2`, `nano_banana_2_lite`, `nano_banana`) — Google

**Official formula (1차, Google Cloud Blog + blog.google):**
`[Subject] + [Action] + [Location/context] + [Composition] + [Style]`
Reference-driven variant: `[Reference images] + [Relationship instruction] + [New scenario]`

**Model-generation mapping (1차, ai.google.dev):** `nano_banana` = Gemini 2.5 Flash Image (legacy; Google recommends migrating off) · `nano_banana_2` = Gemini 3.1 Flash Image · `nano_banana_2_lite` = Gemini 3.1 Flash Lite Image · `nano_banana_pro` = Gemini 3 Pro Image (premium, "Thinking", highest text fidelity).

**Photorealistic template (verbatim):** *"A photorealistic [shot type] of a [subject] in a [setting]. [Light description]. Shot from a [angle] with a [lens type]."*

**Craft vocabulary (verbatim, Google's "Creative Director Prompting Framework"):**
- Lighting: `three-point softbox setup` · `Chiaroscuro lighting with harsh, high contrast` · `Golden hour backlighting creating long shadows`
- Camera: `low-angle shot with shallow depth of field (f/1.8)` · `wide-angle lens` · `macro lens`
- Hardware emulation: GoPro (immersive/distorted) · Fujifilm (authentic color) · disposable camera (nostalgic flash)
- Film stock: `1980s color film, slightly grainy` · `Cinematic color grading with muted teal tones`

**Text rendering (the headline capability):** quote the literal text; name the font per line. **"Text-first hack"**: settle the text content in conversation FIRST, then request the image containing that finalized text.

**Google's own stated limitation (verbatim):** *"Be aware of current limitations: text rendering, factual accuracy, and complex edits may need improvement."*

**Search grounding**: Nano Banana Pro can invoke `google_search` to ground infographics in real data — *"particularly valuable for weather visualizations, current events, or data-driven infographics."*

**Reference caps (Google API surface — informational only)**: NB2 = 10 object + 4 character + 3 style (14 total); NB Pro = 6 object + 5 character, consistency for up to 5 people; NB2 Lite = 14 object.

**Param caveat**: Higgsfield's `nano_banana_2_lite` `thinking[MINIMAL|HIGH]` — Google's own enum is `low`/`high`. The concept transfers; the token spelling does not.

**Evidence tier**: 1차 throughout.

### 3.3 OpenAI (`gpt_image_2`, `openai_hazel`)

**Official structure (1차, OpenAI Cookbook):** `background/scene → subject → key details → constraints`, with the intended use (ad / UI mock / infographic) stated up front to set polish level. Use labeled segments or line breaks for complex requests, not one dense paragraph.

**Length**: 32,000-char hard cap. No recommended length. Official advice: *"Long prompts can work well, but debugging is easier when you start with a clean base prompt and refine with small, single-change follow-ups."*

**Text rendering (1차):** literal text in **quotes or ALL CAPS**; specify font style, size, color, placement; **spell tricky words letter-by-letter** to improve character accuracy; use `quality: medium|high` for small text / dense layouts. OpenAI's own caveat: *"Although significantly improved, the model can still struggle with precise text placement and clarity."*

**Editing (1차):** *"Change only X"* + *"keep everything else the same."* Reference multiple inputs **by index and description** ("element A from Image 1 onto element B in Image 2").

**Do**: concrete materials/textures/medium; framing, viewpoint, lighting/mood; photography language for photorealism.
**Don't**: concept-art language for UI mockups; assume camera specs are literally simulated; overload one prompt.

**⚠ GAP — `openai_hazel` is undocumented under that name.** "Hazel" appears **nowhere** in OpenAI's own docs. OpenAI publishes only `gpt-image-1`, `gpt-image-1.5`, `gpt-image-1-mini`, `gpt-image-2`. A third-party tracker claims Hazel ≈ `gpt-image-1.5`; **this is unverified**. The skill will apply the GPT Image conventions to `openai_hazel` on a stated, flagged assumption — not as vendor-confirmed fact.

**Evidence tier**: 1차 for GPT Image. **Unverified assumption** for the Hazel mapping.

### 3.4 Seedream (`seedream_v5_pro`, `seedream_v5_lite`, `seedream_v4_5`) — ByteDance

**Official principles (1차, BytePlus ModelArk `.../1829186`), five stated:**
1. *"Use coherent natural language to describe the subject + action + environment"* — **not** a disconnected keyword list.
2. State the application context (logo vs. fine art vs. poster).
3. Use precise style keywords or reference images.
4. Put literal render-text in **double quotes**.
5. For editing, *"use concise, unambiguous instructions"*; avoid vague pronouns.

Seedream 3.0 guide adds: *"short prompts can also produce amazing results"*; self-written prompts often outperform AI-generated ones.

**Length**: no cap stated (explicitly confirmed absent).

**Editing exemplars (verbatim, 1차):**
- Add: *"Add matching silver earrings and a necklace to the girl in the image"*
- Delete: *"Remove the girl's hat."*
- Replace: *"Replace the largest bread man with a croissant man, keeping the action and expression unchanged."*
- Multi-image: *"Replace the subject in Image 1 with the subject from Image 2"* · *"Dress the character in Image 1 with the outfit from Image 2"* · *"Apply the style of Image 2 to Image 1."*

**Seedream 5.0 Pro exclusive (1차)**: interactive editing via **overlay markers** — coordinate points, doodles, sketches — for *"fine-grained operations such as object replacement and element placement."* Vendor states: *"Only dola-seedream-5-0-pro supports this capability."* (Not exposed through the MCP; noted as a platform-surface limitation.)

**Param caveat**: BytePlus enumerates Seedream 5.0 Pro at **1K/2K**; Higgsfield exposes `resolution[1k|1.5k|2k]`. The `1.5k` tier is Higgsfield's own layer, undocumented by ByteDance. Higgsfield's `quality[basic|high]` on Lite/4.5 likewise has no ByteDance counterpart.

**Evidence tier**: 1차. **2차/unverified**: the "Deep Thinking" reasoning branding for 5.0 (no dedicated official 5.0 prompt guide exists).

### 3.5 FLUX (`flux_2`, `flux_kontext`) — Black Forest Labs

**Official formula (1차, docs.bfl.ai):** `Subject + Action + Style + Context`
Full slot template: `[SUBJECT], [LOCATION], [STYLE], [CAMERA SETTINGS], [LIGHTING], [COLORS], [EFFECT], [ADDITIONAL ELEMENTS]` — explicitly framed as *"a prompt-building aid, not a rule."*

**Word order is load-bearing (verbatim):** *"FLUX.2 pays more attention to what comes first."* Priority: main subject → key action → critical style → essential context → secondary details.

**Length**: 10–30 words (explore) / **30–80 words — *"usually ideal for most projects"*** / 80–300+ (complex). Cap: 32K tokens (FLUX.2); 512 tokens (legacy Kontext).

**Text rendering**: quote the exact wording (`The text "OPEN" appears in red neon letters`); bind colors to objects by **hex code** (`the car in color #0047AB`).

**⚠ FLUX.2 does NOT support negative prompts** (see R1).

**Kontext editing convention (1차, verbatim exemplars):**
- `"Change the car color to red"` · `"Remove the object from her face"` · `"It's now snowing, everything is covered in snow"`
- Text edit: `Replace '[original text]' with '[new text]'`
- **Verb choice matters**: *"change"* preserves identity; *"transform"* without qualifiers signals a full identity change.
- Anchoring: *"Change the background to a beach while keeping the person in the exact same position, scale, and pose"* — a bare instruction unintentionally shifts subject position/scale/framing.

**Variant guidance**: `pro` = production general-purpose · `flex` = **typography / fine-detail specialist** (exposes steps/guidance in BFL's own API; not through the MCP) · `max` = highest editing consistency + strongest prompt-following. **Prompt craft does not differ structurally by variant** — only the quality ceiling and exposed knobs.

**Do**: name camera/lens/film stock (*"Shot on Fujifilm X-T5, 35mm f/1.4"*); prompt in the target market's native language for cultural authenticity; label each reference image's role ("subject from image 1, style from image 2").

**Evidence tier**: 1차 for formula / text / Kontext editing. **2차-adjacent** for the pro/flex/max feature split.

### 3.6 Recraft (`recraft_v4_1`)

**Official structure (1차, recraft.ai docs)** — "global to local", 8 steps: core concept → background/environment → subject framing/pose → physical attributes → secondary subjects & spatial relationships → lighting direction & behavior → camera/depth/contrast → mood & compositional resolution.

**Stated principle (verbatim):** *"Structured prompts don't make results 'better'. They make outcomes intentional, controllable, and repeatable."*

**Vector / logo / icon prompting (the `model_type` differentiator, 1차):**
- **Avoid texture/material language entirely** for vector work.
- Define: graphic type, shape logic & silhouette clarity, strict color palette, line discipline (*"consistent stroke, no texture"*), layout structure, explicit constraints (*"no gradients, no shadows"*).
- **Use designer-recognizable terms** — the model was trained on them: `contained mark` · `horizontal lockup` · `lettermark` · `negative space cutout` · `monoline style` · `ornate decorative border` · `serif letterforms`.
- Vendor warning (verbatim): *"general prompts like 'a logo for a coffee shop' will produce something, but it probably won't be what you want."*

**Exemplars (verbatim):**
- *"Minimalist [subject] logo centered in composition, circular icon with brand name integrated as negative space cutout"*
- *"Line art icon logo...simple outline..., consistent stroke width, monoline style, clean and minimal, works at small sizes"*

**Color palette**: combine prompt + explicit hex — *"a cityscape using yellow and blue as the primary colors, with deep blue (#1b027c) as the background and bright yellow (#f3e804) as the building accents."*

**⚠ Gap**: Recraft's exact `colors`/`background_color` API schema could not be confirmed from a vendor page (Swagger is JS-rendered). The MCP's declared `#RRGGBB` string format is the operative contract — another instance of "trust the live schema."

**Evidence tier**: 1차 for prompt structure and vector conventions. **Unverified** for the color param schema.

### 3.7 Marketing Studio image (`ms_image` / DTC Ads, `marketing_studio_image`) — Higgsfield

**This family is a WORKFLOW, not a prompt.** The prompt is secondary; the style/format selection is the dominant creative driver.

**Mandatory pre-call sequence (MCP surface, live-verified):**
1. `show_marketing_studio(action='list', type='image_style')` → 42 styles, each a UUID
2. **User picks a style by name.** The MCP schema states: *"Style is the dominant creative driver for ms_image output, so silently defaulting would produce a result the user didn't ask for."*
3. Only then `generate_image(model='ms_image', style_id=<uuid>, ...)`

`style_id` has **no default**; calling without it errors. Higgsfield's own agent docs echo the intent: *"always display the ad format list and let users pick by name rather than auto-selecting."*

**Optional, strictly opt-in (never inferred):** `brand_kit_id` (must be `status: completed`; built by fetching a real website URL — captures name, logo, hero images, colours, fonts, tone, products; 30–90s; failed kits are terminal) · `product_ids` (≤4) · `medias` (≤14).

**Evidence tier**: 1차 (Higgsfield official agent docs + live MCP).

---

## §4 — Per-Family Craft Notes (VIDEO, 8 families)

### 4.1 Veo (`veo3`, `veo3_1`, `veo3_1_lite`) — Google

**Official formula (1차, Google Cloud Blog, explicitly labeled "Core Prompt Formula"):**
`[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]`

Veo 3 (legacy, DeepMind guide) organizes around **7 elements**: shot framing & motion, style, lighting, character descriptions, location, action, dialogue.

**Audio syntax — the most valuable finding of this research (1차, verbatim):**

| Channel | Convention | Example |
|---|---|---|
| Dialogue | quotation marks | `A woman says, "We have to leave now."` |
| Sound effects | `SFX:` prefix | `SFX: thunder cracks in the distance` |
| Ambient | `Ambient noise:` prefix | `Ambient noise: the quiet hum of a starship bridge` |

DeepMind's legacy Veo 3 guide additionally uses a standalone `Audio:` block (`Audio: Crunchy, sugary typing sounds, delighted giggles.`) and a `Character: "line"` shorthand.

**Negative-prompt convention**: see R1. Verbatim: *"specify 'a desolate landscape with no buildings or roads' instead of 'no man-made structures'."*

**"Ingredients to Video" (reference consistency)**: up to **3** reference images; *"Preserve the subject's appearance in the output video."* Using references **forces duration to 8s** on Google's own API.

**First/last frame**: start image + `last_frame` — *"precise control over your shot's composition by letting you define the starting and ending frame."* Maps to the MCP's `start_image` / `end_image` roles on `veo3_1_lite`.

**Timestamp-segmented prompts** are demonstrated by Google for multi-beat shots (`[00:00-00:02] ...`), each beat carrying its own `SFX:`/`Emotion:` tag.

**⚠ Do NOT backfill Veo 3.1's richer conventions onto `veo3`.** The DeepMind Veo 3 guide does not address negative prompting or reference images at all, and its audio guidance is a single generic `Audio:` block. Stated explicitly by the researching agent as a caution.

**Evidence tier**: 1차 throughout.

### 4.2 Kling (`kling3_0`, `kling3_0_turbo`, `kling2_6`) — Kuaishou

**⚠ EVIDENCE CAVEAT: the entire `kling.ai` / `klingai.com` domain returned HTTP 446 (WAF/geo-block) to every direct fetch attempt.** Findings below are relayed through WebSearch's own crawl of the official pages — first-party content, but **not independently verified by direct fetch**. Tier: **1차-relayed**, one notch below the directly-fetched families.

**Official framework (relayed):** *"a useful prompt usually defines the **subject, action, setting, camera language, lighting, and atmosphere** in plain, readable language."* Kling's own text explicitly frames this as **a flexible writing framework, not a rigid formula** — the widely-quoted `Subject + Movement + Scene + Camera + Lighting + Atmosphere` "formula" is a third-party gloss.

**Length**: `negative_prompt` capped at **2,500 chars** (verbatim from the API field docs); `prompt` assumed symmetric.

**Negative prompts (relayed, verbatim):** *"It is recommended to supplement negative prompt via negative sentences within positive prompts."* — Kling recommends folding exclusions into the positive prompt **even though its own API exposes the field**. Since Higgsfield does not expose it, this is not a workaround; it is the vendor-preferred practice.

**Multi-shot**: Kling 3.0 supports *"highly flexible storyboard control"* / native multi-shot in one generation. **However**, Kling's native multi-shot is a separate UI/API mode with per-shot prompt fields, while Higgsfield exposes only a single flat `prompt`. Therefore any storyboard must be composed **inline in the one prompt string** using shot labels.

**Dialogue (relayed)**: 5 languages (zh/en/ja/ko/es) + dialects + mixed-language within one video. Multi-character structure: `<who is speaking> (<how things are said>) <what they say>`.

**Do**: concrete visible nouns and motion cues (`smoke drifting upward`); natural-language camera terms (close-up, low angle, slow push-in, tracking); embed exclusions as negative sentences inside the positive prompt.
**Don't**: abstract/internal-state language (*"magic"*, *"feels tense"*) without a visible correlate.

**⚠ Gap**: no official Kling statement on what to drop from the prompt when a `start_image` is supplied.

### 4.3 Seedance (`seedance_2_0`, `seedance_2_0_mini`, `seedance1_5`) — ByteDance

**The richest documented prompting system in the catalog, and the one where the platform guide is WRONG (see §1 Proof 3).**

**Official formula (1차, BytePlus ModelArk `.../2222480`):**
`Precise subject + action details + scene/environment + lighting & color tone + camera movement + visual style + image quality + constraints`
The guide explicitly frames prompts as **"engineering-style instructions" rather than creative writing.**

Seedance 1.5 Pro (`.../2168087`): `Subject + motion + environment + camera movement/cuts + aesthetic description + sound` (last four optional).

**⚠ TIMESTAMPS ARE UNSTABLE — official, verbatim:**
> *"The model's support for precise timing (such as 0–3 seconds) is unstable, and forcibly limiting duration may lead to abnormal generation results."*
> *"Do not impose strict limits on the duration of each segment; prioritize allowing the model to naturally generate the pacing."*

The official multi-shot convention is a **simple labeled shot list** — `Shot 1 / Shot 2 / Shot 3` — with **no** timestamps, **no** fixed beat count, and **no** header line declaring total duration/shot count/aspect ratio. (The "declare shot count + duration + ratio at the top" rule is a **Higgsfield-blog convention**, not ByteDance's.)

**@-mention reference system (1차, verbatim):**
- `Reference <Subject_N> in <Image_N> to generate...`
- `Reference <Action/Camera_movement/Style/Sound_effect> in <Video_N>`
- *"For simple scenarios with undefined subjects, each time the subject is mentioned, use `<Subject_N>@<Image_N>` to emphasize the binding relationship."*
- In practice (from the official case study), written as `@Image 1` / `@Video 1` / `@Audio 1` inline in prose, **each with an explicitly stated purpose** — "use the girl in @Image 1 **as the main character**", "use @Image 2 **as the dormitory scene style reference**", "refer to the camera movement in @Video 1".
- Chinese official manual confirms the identical pattern: 将视频@视频1 中的小猫作为主体1 ("designate the cat from @video1 **as subject 1**").
- **This is prompt TEXT, not an API field** — it transfers directly to Higgsfield's `prompt` string. Higgsfield's `medias[]` roles bind *which file* is Image 1 / Video 1 / Audio 1; the *purpose statement* still belongs in the prose.

**Bracket conventions (1차, "Special Formatting Standards"):**

| Channel | Delimiter |
|---|---|
| Music | `（parentheses）` |
| Sound effects | `<angle brackets>` |
| Dialogue | `{curly braces}` |
| Subtitles | `【square brackets】` |

Confirmed in the official exemplar: dialogue rendered as `{How did the exam go? Did you pass?}`.

**Character-drift avoidance (1차, verbatim):**
- *"Use 2–3 clear and stable static features (such as clothing, hairstyle, appearance, or category) to describe the subject."*
- *"Too Many Reference Characters: Limit to 4; generate in groups if needed."*
- Duplicated characters ← caused by multi-view reference images for one subject. Avoid.
- Recommended asset budget: 1–2 character + 1 scene + 1 camera-reference video + 1 audio. Maxing the slots causes *"feature prioritization confusion."*

**`generate_audio` vs `audio_references` (1차, API ref):** `generate_audio` = the model **synthesizes** new synchronized audio. `audio_references` = the user supplies a clip whose **timbre/style is referenced**. Constraint: *"Audio cannot be input alone; at least one reference video or image must be included."*

**Video extension**: use the phrase *"Extend `<Video_N>`"*, NOT "reference" language — the vendor explicitly warns "reference" causes misidentification.

**⚠ Gap (evidenced absence)**: the descriptive audio-quality keyword vocabulary (reverb / muffled / echoing / crunchy / metallic) that circulates widely appears in **no** ByteDance source. Explicitly searched and confirmed absent. Third-party only.

**Evidence tier**: 1차 (BytePlus EN + Volcengine ZH cross-confirmed).

### 4.4 Cinema Studio (`cinematic_studio_3_0`, `cinematic_studio_video_v2`, `cinematic_studio_video`, `cinematic_studio_2_5`) — Higgsfield

**Documented reference system (1차, higgsfield.ai/blog/cinema-studio-3.0)** — four layers:
1. Reference uploads tagged `@image_1`, `@image_2`, `@video`
2. Scene description with an explicit **numbered shot breakdown**
3. Technical specification block (camera movement, lighting, composition)
4. Character/environment consistency markers

**Length**: exemplars range 50 words (simple) → **500+ words** (complex multi-shot sequences). Note this **contradicts Higgsfield's own ~200-token general ceiling** (see R5). Reported, not reconciled.

**Motion transfer — documented literal syntax (verbatim):**
`"In @video change location to @image_1. [Genre/context description]."`
→ *"relights the subject accurately and copies the motion perfectly, no manual masking."*

**Empty-prompt placement (verbatim):** *"Leave the prompt empty. Select your character and your location. Cinema Studio handles the rest"* — for basic keyframes.

**Multi-character**: tag each distinctly (`@image_1`, `@image_2`, `@image_3`) in one prompt; the system *"places them together, assigns correct lighting, and holds every face consistent across cuts"* without a start frame.

**Continuation**: upload the previous video as context and write only the next beat.

**⚠ The `genre` / `multi_shots` / `speedramp` / `cfg_scale` / `preset_id` parameter enums are NOT in any static Higgsfield doc.** The vendor's own agent documentation instructs: **"When unsure, run `higgsfield model get <model>` and inspect the schema."** This is the vendor explicitly endorsing this SPEC's live-lookup design. The enums live only in the MCP (captured in `mcp-catalog-snapshot.md` §2).

**Exemplar (verbatim, abridged)**: *"Multi-shot editing, hotel corridor fight sequence. Shot 1: Telephoto lens. At the far end of a long, narrow luxury hotel corridor stands a young man in a dark tailored suit..."* (7 numbered shots, 500+ words).

**Evidence tier**: 1차 for structure/mechanics/exemplars; **none-found** for parameter enums (by vendor design).

### 4.5 Marketing Studio video (`marketing_studio_video`) — Higgsfield

**A workflow, not a prompt.** Prompt is optional for this model.

**26 preset modes** (not the 6 the current skill claims) — live-verified slugs: `ugc` · `ugc_gadget_saved_me` · `ugc_giant_figure` · `ugc_unboxing_virtual_try_on` · `ugc_unboxing_asmr` · `ugc_virtual_try_on_sneakers` · `couple_sharing_home` · `ugc_selfie_testimonial` · `ugc_direct_to_camera` · `ugc_secret_hack_reveal` · `crush_test` · `hypermotion_oj` · `camera_pov` · `classic_meets_modern` · `mess_to_fresh` · `mystery_box` · `product_showcase` · `reboxing` · `tv_spot` · `ugc_addiction` · `ugc_before_and_after` · `ugc_how_to` · `ugc_unboxing` · `ugc_virtual_try_on` · `virtual_try_on` · `wild_card`

**Composition rules (HARD, MCP schema + Higgsfield agent docs agree):**
- `hook_id` (the "what" — attention mechanic) and `setting_id` (the "where" — location/vibe) are **independent** of each other.
- Both are **MUTUALLY EXCLUSIVE with `ad_reference_id`**. Hook/setting compose from explicit building blocks; `ad_reference_id` recreates an existing video's scenario. Verbatim from Higgsfield's agent docs: *"When the user has selected an ad reference for the ad, do **not** also pass `--hook_id` or `--setting_id`."*
- Hooks/settings are gated to **5 slugs only**: `ugc`, `ugc_how_to`, `ugc_unboxing`, `product_review`, `ugc_virtual_try_on`. Other modes ignore or reject them.
- `product_ids` **must** be included whenever a hook is used ("they require product context").
- `ad_reference_id` does **NOT** auto-pull its linked avatar/product — they must be passed explicitly.
- Default aspect is landscape 16:9 → **pass `9:16` explicitly** for TikTok/Reels.

**Avatars**: `preset` (curated, no upload cost) vs `custom` (uploaded, has cost). For UGC modes an avatar is optional — *"the backend can synthesize a Soul Character automatically."*

**Exemplar — the vendor's own 10-word "Wild Card" prompt (verbatim):** *"You scan the fridge, get a recipe, cook a meal."*

**Evidence tier**: 1차.

### 4.6 Wan (`wan2_6`, `wan2_7`) — Alibaba Tongyi

**Unexpectedly the best-documented non-Higgsfield family.** Alibaba Cloud Model Studio publishes a full official prompt guide with **multiple named formulas** (1차, directly fetched).

| Scenario | Official formula |
|---|---|
| Basic | `Entity + Scene + Motion` |
| Advanced | `Entity(desc) + Scene(desc) + Motion(desc) + Aesthetic control + Stylization` |
| **Image-to-video** | **`Motion + Camera movement`** — *"Focus prompt on movement descriptions and specific camera directions rather than static elements."* |
| Sound (2.7/2.6) | `Entity + Scene + Motion + Sound description (voice / SFX / BGM)` |
| **Multi-shot (2.7/2.6)** | `Overall description + Shot number + Timestamp + Shot content` — numbered shots with explicit time ranges (`[0–3s]`) |
| Reference-to-video | `Reference identifier + Action + Scene + Lines + BGM`, using `"Image 1"` / `"Video 2"` identifiers, numbered per modality; nesting allowed ("Image 1 in Image 2") |

**Note the direct contradiction with Seedance**: Wan officially prescribes explicit timestamp ranges in multi-shot prompts; ByteDance officially warns that timestamps destabilize Seedance. **These are different models with opposite conventions.** This is exactly why per-family craft files are necessary and a single generic "video prompt formula" would be actively harmful.

**Audio suppression — literal phrases (1차):** `"No dialogue."` and `"No background music."`

**Camera-movement emotional intent (1차, verbatim):** Push-in → intimacy/tension · Pull-out → scale/isolation · Tracking → viewer alongside subject · Orbit → emphasizes subject importance · Fixed → stillness/focus.

**Official avoid-list (verbatim categories):** naming specific real people · rapid scene changes within one clip · demanding exact legible text · very long choreographed sequences · lip-synced dialogue to specific words.

**Length**: no cap stated; the guide deliberately declines to prescribe one.
**Negative prompts**: no convention documented at all — nothing to re-express.
**Deprecation**: *"Wan 2.7 no longer supports the `shot_type` parameter."*

**Evidence tier**: 1차, directly fetched and verified.

### 4.7 Gemini Omni Flash (`gemini_omni`) — Google

**Inverse philosophy from Veo (1차, verbatim):** *"Simple prompts work best for video editing. Overly descriptive prompts can lead to unintended changes."* For generation (not editing), describe camera movement, lighting, and mood.

**Reference syntax — exact inline tokens (1차):** `<FIRST_FRAME>` designates the opening frame; `<IMAGE_REF_N>` (0-indexed) marks style/subject references, composed inline in prose:
> *"in the style of `<IMAGE_REF_0>` a woman `<IMAGE_REF_1>` is walking"*

**⚠ KNOWN BROKEN, per Google itself (verbatim):** *"Video references up to 3 seconds in duration are accepted by the API schema but are not correctly processed by the model at this time."* The MCP exposes a `video_references` role on this model. **The skill must warn.**

**Audio**: plain descriptive language, **not** Veo's tagged syntax — *"Include calm background music"*, *"The audio is a low tinny radio broadcast in the background."*

**Timecode structure is supported**: `[0-3s] A person is walking / [3-6s] They stop and turn around / [6-10s] They start running`

**Duration ceiling**: Google's own is 10s — consistent with the MCP's `duration[4-10]`.

**Evidence tier**: 1차.

### 4.8 Grok (`grok_video`, `grok_video_v15`, `grok_image`) — xAI

**⚠ EVIDENCED ABSENCE — this is the headline finding for this family.**

Direct fetch of `docs.x.ai` (video generation, reference-to-video, image generation) found:
- **No prompt-structure formula**
- **No length recommendation** (only "a prompt that is too long" as an error condition, with no number)
- **No negative-prompt field or convention**
- **No mention of audio, dialogue, or sound design — anywhere**

This last point **directly contradicts the MCP catalog's own tagging** of `grok_video_v15` as having *"native audio direction."* xAI's published documentation says nothing about audio. Every claim about Grok's audio prompting technique circulating online traces to **third-party guides only** (Morphic, imagine.art, WaveSpeed, fal.ai, Artlist, Hedra, Scenario) — none of them xAI.

**The skill MUST NOT invent Grok audio conventions.** It falls back to R1–R5 + the observed official exemplars.

**Official exemplars (verbatim, docs.x.ai — plain single-sentence descriptions, no labeled components):**
- *"A glowing crystal-powered rocket launching from the red dunes of Mars, ancient alien ruins lighting up in the background as it soars into a sky full of unfamiliar constellations."*
- *"Timelapse of a flower blooming in a sunlit garden."*
- Image-to-video: *"Make the water crash down and slowly pan out the camera."*

**Reference syntax**: xAI uses `<IMAGE_2>` placeholders tied to its own `reference_images` array. **⚠ Higgsfield exposes only a single `start_image` role — the numbered-placeholder convention does NOT map cleanly and should not be assumed to work.**

**Evidence tier**: 1차 — an evidenced absence, directly verified.

### 4.9 MiniMax Hailuo (`minimax_hailuo`) — supplementary (out of the 15, but documented)

**Bracketed camera-command mini-language (1차, verbatim, platform.minimax.io):**

`[Truck left]` `[Truck right]` `[Pan left]` `[Pan right]` `[Push in]` `[Pull out]` `[Pedestal up]` `[Pedestal down]` `[Tilt up]` `[Tilt down]` `[Zoom in]` `[Zoom out]` `[Shake]` `[Tracking shot]` `[Static shot]`

- **Combination**: *"Multiple commands inside one `[]` take effect simultaneously"* — e.g. `[Pan left,Pedestal up]`. **Recommended max 3.**
- **Sequencing**: place commands in narrative order — *"...[Push in], then...[Push out]"*
- **Fallback**: *"Free-form descriptions also work, but explicit commands yield more accurate results."*
- Official exemplar: *"A man picks up a book [Pedestal up], then reads [Static shot]."*
- **Length cap**: 2,000 chars.

**⚠ SILENT-OVERRIDE HAZARD**: MiniMax's own API exposes `prompt_optimizer` (default **true**), which auto-rewrites the prompt and can smooth over precise manual camera commands. **Higgsfield does not expose this switch.** A user's precise camera direction may therefore be silently overridden with no way to disable it through the MCP. The skill must warn.

**Evidence tier**: 1차.

---

## §5 — Consolidated Gap Register

Gaps are recorded, not filled. Nothing below was invented.

| # | Family | Gap | Consequence for the skill |
|---|---|---|---|
| G1 | **Soul** | No official prompt formula exists (vendor is deliberately anti-formula) | Fall back to R1–R5 + Higgsfield general guidance. **Do not invent a Soul formula.** |
| G2 | **openai_hazel** | Model name absent from all OpenAI documentation | Apply GPT Image conventions on an explicitly stated, flagged assumption |
| G3 | **Kling** | Entire vendor domain WAF-blocked (HTTP 446) | Evidence tier lowered to 1차-relayed; flagged in the reference file |
| G4 | **Grok** | No prompt guidance, and **no audio documentation at all** despite the MCP tagging it "native audio" | Do not author Grok audio conventions. State the absence. |
| G5 | **Cinema Studio** | Parameter enums deliberately not published — vendor says query the schema at runtime | Confirms the design. Live lookup only. |
| G6 | **Seedance** | Audio-quality keyword vocabulary (reverb/muffled/echo) is third-party only | Omit, or mark clearly as unverified |
| G7 | **Recraft** | `colors`/`background_color` schema unconfirmed (JS-rendered Swagger) | Trust the live MCP schema (`#RRGGBB`) |
| G8 | **Veo 3 (legacy)** | Much thinner than 3.1; no negative-prompt or reference guidance | Do not backfill 3.1's conventions onto `veo3` |
| G9 | **Wan / MiniMax** | Higgsfield does not expose `prompt_extend` (Wan) / `prompt_optimizer` (MiniMax) | Warn: auto-optimization may silently override precise prompts |
| G10 | **Higgsfield internal** | ~200-token ceiling vs. its own 500+-word Cinema Studio exemplars | Report both; do not reconcile |

---

## §6 — Source Ledger (evidence tiers)

**1차, directly fetched and verified:**
Google DeepMind Veo prompt guide · Google Cloud Veo 3.1 + Nano Banana prompting guides · ai.google.dev (image-generation, imagen, veo, omni, gemini-3) · blog.google (Nano Banana Pro tips + launch) · OpenAI developers.openai.com image-generation guide + 2 cookbook prompting guides · docs.bfl.ai (FLUX.2 prompting, prompting summary, Kontext overview + image editing) · recraft.ai (logos-and-icons guide, prompt-engineering guide) · BytePlus ModelArk (Seedance 2.0 prompt guide, Seedance 1.5 Pro guide, Seedream 3.0/4.0-4.5 guides, Seedream 4.0-5.0 tutorial, Seedance 2.0 API ref, video-generation tutorial) · Volcengine (Seedance 2.0 ZH guide, Seedance 1.5 ZH mirror) · ByteDance Feishu official manual (partial) · Alibaba Cloud Model Studio (text-to-video prompt guide, use-video-generation) · GitHub Wan-Video/Wan2.2 README + Wan2.1 prompt_extend.py · docs.x.ai (video, video/generation, video/reference-to-video, images/generation) · platform.minimax.io (video-generation i2v + t2v) · **github.com/higgsfield-ai/skills** (`references/`: model-catalog, prompt-engineering, marketing-modes, marketing-avatars, marketing-products, marketing-dtc-ads, marketing-brand-kits, marketing-ad-references, marketing-setup-items) · higgsfield.ai (nano-banana-pro-prompt-guide, seedance-prompting-guide, cinema-studio-3.0, marketing-studio-video-1/-2, soul-cast-intro, Soul-ID article)

**1차-relayed (vendor page, blocked to direct fetch, content via WebSearch crawl):**
kling.ai prompt guide + API reference + Video 3.0 quickstart (HTTP 446, domain-wide block)

**Dead / thin:**
`docs.bfl.ai/guides/prompting_guide_kontext_i2i` (404, superseded) · higgsfield.ai `soul-intro` / `soul-cinema` / `marketing-studio/product` (resolved but carry no prompt-craft content) · three `docs.cloud.google.com` pages (200 but JS-rendered; body unretrievable) · Zhihu article (login wall)

**Explicitly NOT used as evidence (2차, listed for transparency only):**
fal.ai, imagine.art, Morphic, WaveSpeed, Artlist, Hedra, Scenario, explainx.ai, Runware, Cloudflare, hazelgen.org, WeShop AI, Cutout.pro, klingapi.com, kie.ai, Leonardo.ai, veed.io, LTX, Segmind, filmart.ai

---

## §7 — Design Implications (feeds plan.md)

1. **Two-layer skill architecture is mandatory, not stylistic.** Parameters must be live-queried; craft must be static and cited. Three independent proofs (§1).
2. **A single generic "video prompt formula" would be actively harmful.** Wan officially prescribes timestamps; ByteDance officially warns timestamps destabilize Seedance. Per-family files are required.
3. **R1–R5 belong in `media-higgsfield-core`** — they are multi-vendor-confirmed and family-independent.
4. **The Socratic interview must collect the slots the craft files actually consume**: subject, action, scene, camera, lighting/atmosphere, style, literal text (+font), audio/dialogue, references (+ each reference's *purpose*), shot count, aspect, duration, quality/budget tier.
5. **The skill must read back `adjustments`** from the MCP response and report server-substituted defaults (snapshot §5.1) — otherwise a user who asked for audio silently gets a silent video.
6. **Warnings the skill must carry**: `gemini_omni` video-references are known-broken (Google's own words) · `minimax_hailuo` may silently override camera commands · `ms_image` requires a style pick and must never auto-default · Grok has no documented audio conventions despite its catalog tag.
