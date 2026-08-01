---
id: SPEC-MOC-HIGGSFIELD-PROMPT-001
title: "Acceptance criteria — Higgsfield prompt-craft skills"
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
tags: "higgsfield, mcp, prompt-craft, media, skills, acceptance"
---

# acceptance.md — SPEC-MOC-HIGGSFIELD-PROMPT-001

## §A — Purpose

Every criterion below is either (a) a shell command with a stated expected output, or (b) an observable MCP artifact (job ID, result URL, credit figure) recorded verbatim in `progress.md` §E.2. There are no judgment-only criteria in the closure gate.

The ACs are built on a **pinned-literal registry** (§C). The literals are fixed at plan time, not recomputed at run time — a run-phase agent cannot satisfy an AC by choosing a pattern that happens to match whatever it wrote. Each literal check is paired with a stated broken-fixture failure mode so the check is demonstrably non-vacuous.

## §B — Verification environment

```bash
cd /Users/goos/MoAI/claude.mo.ai.kr
SK=plugins/moai-media/skills
CORE=$SK/media-higgsfield-core
IMG=$SK/media-higgsfield-image
VID=$SK/media-higgsfield-video
```

> **Shell-portability contract (HARD).** The three-directory set is expressed as the glob `"$SK"/media-higgsfield-*` in every command below, NOT as a space-joined `ALL="$CORE $IMG $VID"` string. Reason: the run-phase shell is **zsh** (`$0=/bin/zsh`), and zsh does NOT word-split an unquoted `$ALL` — `grep -rn X $ALL` collapses to one bogus path, exits non-zero, and matches **nothing**, silently FALSE-PASSING every drift-sweep AC (AC-004 etc.). The glob `"$SK"/media-higgsfield-*` expands to the same 3 directories as separate args in **both** bash and zsh (verified). Command-substitution word-splitting is likewise avoided (`find … -exec … {} +` and `grep -rl … | while read` instead of `awk … $(find …)`).

Live-MCP criteria (AC-025 … AC-028) require an authenticated Higgsfield MCP session. The tool namespace is registration-dependent and MUST be resolved at run time (`mcp__higgsfield__*` or `mcp__claude_ai_higgsfield__*`).

---

## §C — Pinned-Literal Registry

### C.1 — Required literals (run-phase MUST author these exact strings)

| # | Literal (exact / case-insensitive as noted) | Must appear in | Fails if… |
|---|---|---|---|
| L1 | `models_explore` | all 3 `SKILL.md` | a skill asserts parameters instead of querying them |
| L2 | `get_cost` | `$IMG/SKILL.md`, `$VID/SKILL.md`, `$CORE/references/job-lifecycle.md` | preflight step omitted → user spends blind |
| L3 | `adjustments` | `$IMG/SKILL.md`, `$VID/SKILL.md`, `$CORE/references/job-lifecycle.md` | server-substituted defaults go unreported |
| L4 | `credits_exact` | `$CORE/references/job-lifecycle.md` | the `credits` vs `credits_exact` rule is missing |
| L5 | `mcp__higgsfield__` **and** `mcp__claude_ai_higgsfield__` **and** `namespace` | `$CORE/references/call-schema.md` | one namespace is hard-coded as the only form |
| L6 | `Evidence tier:` | each of the 15 prompt-craft files | an uncited/untiered craft claim |
| L7 | `no official prompt formula` (ci) | `$IMG/references/prompt-craft/soul.md` | the evidenced absence is papered over |
| L8 | `no audio documentation` (ci) | `$VID/references/prompt-craft/grok.md` | Grok's undocumented "native audio" tag is treated as real |
| L9 | `openai_hazel` **and** `unverified` | `$IMG/references/prompt-craft/openai.md` | an unverified model mapping is presented as fact |
| L10 | each rule **defined** as a bold label `**R1 …**` .. `**R5 …**` (NOT a bare mention) | `$CORE/references/universal-rules.md` | the universal rules are incomplete, or merely mentioned without definition |
| L11 | `live lookup` | `$IMG/SKILL.md`, `$VID/SKILL.md` | the out-of-scope-model fallback is unstated |
| L12 | `unstable` | `$VID/references/prompt-craft/seedance.md` | ByteDance's timestamp warning is dropped → the platform-vs-vendor conflict is lost |
| L13 | `Timestamp` (ci) | `$VID/references/prompt-craft/wan.md` | Wan's timestamped multi-shot formula is dropped → ditto |
| L14 | `per-family` | `$VID/SKILL.md` | the no-generic-formula rule is unstated |
| L15 | `not correctly processed by the model at this time` | `$VID/references/prompt-craft/gemini-omni.md` | Google's own known-broken warning is dropped |
| L16 | `prompt_optimizer` | `$VID/SKILL.md` | the MiniMax silent-override hazard is unwarned |
| L17 | `ad_reference_id` **and** `mutually exclusive` (ci) | `$VID/references/prompt-craft/marketing-studio.md` | a call that will be rejected is documented as valid |
| L18 | `style_id` **and** `no default` (ci) **and** `show_marketing_studio` | `$IMG/references/prompt-craft/marketing-studio.md` | `ms_image` silently auto-defaults a style |
| L19 | `do not exist` (ci) | `$CORE/references/call-schema.md` | the anti-pattern section is absent, making the §C.2 exemption a loophole |

### C.2 — Forbidden literals

| # | Literal | Forbidden in | Exemption |
|---|---|---|---|
| F1 | `sora_2` | all 3 skill trees | none |
| F2 | `veo_3`, `kling_2_5_turbo`, `kling_2_1_master`, `kling_avatars_2_0`, `seedance_pro`, `cinema_studio_3_5`, `minimax_hailuo_02`, `wan_2_5`, `soul_2_0`, `seedream_4_0`, `wan_2_2_image` | all 3 skill trees | none — every one is an invented ID |
| F3 | `width_and_height`, `duration_seconds`, `image_url`, `enhance_prompt`, `style_strength`, `custom_reference_id`, `image_reference_url` | all 3 skill trees | **only** as PROSE in `$CORE/references/call-schema.md`'s anti-pattern section (L19 proves it exists). NEVER inside a fenced code block there — a call example must not smuggle a retired param (§D.3 (5b) enforces this) |
| F4 | `batch_size` with no `ms_image` within ±3 lines (proximity-scoped, not line-scoped) | all 3 skill trees | none — `batch_size` is valid only on `ms_image` |
| F5 | `negative_prompt` **inside a fenced code block** | all 3 skill trees | none. Prose discussion of a vendor's own field (Kling has one; FLUX.2 has none) is permitted — a *call example* carrying one is not. |
| F6 | Bracket-enum parameter notation (`resolution[`, `duration[`, `quality[`, `variant[`, `mode[`, `genre[`, `aspect_ratio[`) | the 3 `SKILL.md` files | permitted in craft references, where a vendor-vs-platform enum caveat is legitimate documentation (e.g. Higgsfield `thinking[MINIMAL\|HIGH]` vs Google `low`/`high`). Forbidden in a SKILL.md, where it can only be a copied parameter table. |

> **Why F6 exists.** The snapshot is a complete, well-formatted model table — precisely the shape of the defect being removed. F6 is the tripwire that fires the moment it is copied into a call path.

---

## §D — Acceptance Criteria Matrix

| AC | Criterion | REQ | Severity | Verification |
|---|---|---|---|---|
| **AC-HGF-001** | `media-higgsfield-core` exists: `SKILL.md` + exactly the 5 named references | REQ-001 | BLOCKER | §D.3 (1) |
| **AC-HGF-002** | Image skill carries exactly 7 named prompt-craft files; `references/model-guide.md` no longer exists | REQ-031, D-3 | BLOCKER | §D.3 (2) |
| **AC-HGF-003** | Video skill carries exactly 8 named prompt-craft files; `references/dop-motions.md` still exists **and was modified** | REQ-032 | BLOCKER | §D.3 (3) |
| **AC-HGF-004** | Zero occurrences of any invented model ID (F1, F2) | REQ-050 | BLOCKER | §D.3 (4) |
| **AC-HGF-005** | Retired parameter names (F3): (5a) zero outside `call-schema.md`; (5b) zero inside any fenced code block in `call-schema.md`; the anti-pattern section itself must exist (L19) | REQ-051 | BLOCKER | §D.3 (5) |
| **AC-HGF-006** | Every `batch_size` occurrence has `ms_image` within ±3 lines (F4, proximity-scoped) | REQ-051 | MAJOR | §D.3 (6) |
| **AC-HGF-007** | No bracket-enum parameter table in any `SKILL.md` (F6) | REQ-003, REQ-004 | BLOCKER | §D.3 (7) |
| **AC-HGF-008** | No `negative_prompt` inside any fenced code block (F5) | REQ-030 (R1) | MAJOR | §D.3 (8) |
| **AC-HGF-009** | All 3 `SKILL.md` name `models_explore`; image + video name `get_cost` (L1, L2) | REQ-012, REQ-020 | BLOCKER | §D.3 (9) |
| **AC-HGF-010** | `call-schema.md` names **both** namespaces and the runtime-resolution rule (L5) | REQ-015 | MAJOR | §D.3 (10) |
| **AC-HGF-011** | `adjustments` read-back present in image + video `SKILL.md` and `job-lifecycle.md`; `credits_exact` rule present (L3, L4) | REQ-021, REQ-022 | BLOCKER | §D.3 (11) |
| **AC-HGF-012** | Flow ordering in image + video `SKILL.md`: first `models_explore` precedes first `get_cost`, which precedes first `generate_*` | REQ-010 | MINOR (advisory) | §D.3 (12) |
| **AC-HGF-013** | All 15 prompt-craft files contain ≥1 `https://` citation | REQ-033 | BLOCKER | §D.3 (13) |
| **AC-HGF-014** | All 15 prompt-craft files contain the literal `Evidence tier:` (L6) | REQ-033 | BLOCKER | §D.3 (14) |
| **AC-HGF-015** | `soul.md` states the absence (L7) **and** carries no `**Official formula` / `## Official formula` label | REQ-034 | BLOCKER | §D.3 (15) |
| **AC-HGF-016** | `grok.md` states the audio absence (L8) **and** carries no `**Official formula` / `## Official formula` label | REQ-034, REQ-042 | BLOCKER | §D.3 (16) |
| **AC-HGF-017** | `openai.md` flags the `openai_hazel` mapping as `unverified` (L9) | REQ-034 | MAJOR | §D.3 (17) |
| **AC-HGF-018** | `universal-rules.md` defines R1–R5 as bold rule labels — not bare mentions (L10) | REQ-030 | BLOCKER | §D.3 (18) |
| **AC-HGF-019** | Image + video `SKILL.md` state the out-of-scope-model `live lookup` fallback (L11) | REQ-035 | MAJOR | §D.3 (19) |
| **AC-HGF-020** | The Wan↔Seedance contradiction survives: `seedance.md` carries `unstable`, `wan.md` carries `Timestamp`, video `SKILL.md` carries `per-family` and routes to per-family `prompt-craft/` files (L12, L13, L14). The "no single generic-formula section" check is inspection-only (§D.5) — Korean prose defeats an English-heading grep | REQ-036 | BLOCKER | §D.3 (20) + §D.5 |
| **AC-HGF-021** | `gemini-omni.md` carries Google's verbatim broken-references warning (L15) | REQ-042 | MAJOR | §D.3 (21) |
| **AC-HGF-022** | Video `SKILL.md` carries the MiniMax silent-override hazard (L16) | REQ-042 | MAJOR | §D.3 (22) |
| **AC-HGF-023** | Video `marketing-studio.md` carries the `ad_reference_id` mutual-exclusion rule (L17) | REQ-041 | MAJOR | §D.3 (23) |
| **AC-HGF-024** | Image `marketing-studio.md` carries the `ms_image` style-pick rule (L18) | REQ-040 | MAJOR | §D.3 (24) |
| **AC-HGF-025** | `get_cost: true` preflight returns a `credits` figure for ≥1 image model **and** ≥1 video model, and **consumes zero credits** (balance identical before/after the sweep) | REQ-020, REQ-060 | BLOCKER | §D.4 (E1) |
| **AC-HGF-026** | One real image generated: job polled to `completed`, result URL returned | REQ-060 | BLOCKER | §D.4 (E2) |
| **AC-HGF-027** | One real video generated: job polled to `completed`, result URL returned | REQ-060 | BLOCKER | §D.4 (E3) |
| **AC-HGF-028** | Total E2E spend ≤ 10 credits, computed as `balance_before − balance_after`, reported, and reconciling with the sum of the reported `credits` figures | REQ-061 | BLOCKER | §D.4 (E4) |

---

## §D.1 — Severity classification

| Severity | Meaning | Closure effect |
|---|---|---|
| **BLOCKER** | The defect this SPEC exists to remove is still present, or the deliverable is absent. | SPEC cannot close. No PASS-WITH-DEBT. |
| **MAJOR** | A stated requirement is unmet but the core design holds. | May close as PASS-WITH-DEBT **only** with the debt named in `progress.md` §E.3 and a follow-up recorded. |
| **MINOR (advisory)** | Structural/ordering heuristic. Prone to benign false failure. | Never blocks. Report the result; do not chase it. |

---

## §D.2 — Traceability (REQ → AC)

| REQ | Covered by |
|---|---|
| REQ-001 core is SSOT | AC-001 |
| REQ-002 two axes | AC-004, AC-005, AC-007, AC-009, AC-013, AC-014 (jointly) |
| REQ-003 / REQ-004 no hard-coded params or catalog table | AC-004, AC-005, AC-007 |
| REQ-010 runtime flow | AC-009, AC-012 |
| REQ-011 orchestrator-only interview | — *indirect, §D.5* |
| REQ-012 live constraint fetch | AC-009 |
| REQ-013 nested `params{}` | — *indirect, §D.5* |
| REQ-014 media_id not URL | AC-005 (`image_url` ban) |
| REQ-015 namespace resolution | AC-010 |
| REQ-020 get_cost preflight | AC-009, AC-025 |
| REQ-021 `credits` not `credits_exact` | AC-011 |
| REQ-022 `adjustments` read-back | AC-011 |
| REQ-023 balance halt | — *indirect, §D.5* |
| REQ-030 universal rules | AC-008, AC-018 |
| REQ-031 / REQ-032 craft file sets | AC-002, AC-003 |
| REQ-033 citation + evidence tier | AC-013, AC-014 |
| REQ-034 evidenced absences | AC-015, AC-016, AC-017 |
| REQ-035 out-of-scope fallback | AC-019 |
| REQ-036 no generic video formula | AC-020 |
| REQ-040 ms_image style pick | AC-024 |
| REQ-041 marketing_studio_video composition | AC-023 |
| REQ-042 hazard warnings | AC-016, AC-021, AC-022 |
| REQ-050 / REQ-051 drift elimination | AC-004, AC-005, AC-006 |
| REQ-060 / REQ-061 E2E | AC-025, AC-026, AC-027, AC-028 |

---

## §D.3 — Verification commands

```bash
cd /Users/goos/MoAI/claude.mo.ai.kr
SK=plugins/moai-media/skills
CORE=$SK/media-higgsfield-core
IMG=$SK/media-higgsfield-image
VID=$SK/media-higgsfield-video
# NOTE: the 3-directory set is the GLOB "$SK"/media-higgsfield-* (expands to core+image+video
# in BOTH bash and zsh). A space-joined ALL="$CORE $IMG $VID" is NOT used — zsh does not
# word-split it, which would silently FALSE-PASS every drift sweep. See §B portability contract.

# (1) AC-HGF-001 — core skill structure. Expect: 5 names, exactly.
ls $CORE/SKILL.md && ls $CORE/references/ | sort
# expect: call-schema.md catalog-protocol.md interview-schema.md job-lifecycle.md universal-rules.md

# (2) AC-HGF-002 — image craft set = 7; model-guide.md gone.
ls $IMG/references/prompt-craft/ | sort | tr '\n' ' '
# expect: flux.md marketing-studio.md nano-banana.md openai.md recraft.md seedream.md soul.md
test ! -f $IMG/references/model-guide.md && echo "model-guide.md removed: PASS"

# (3) AC-HGF-003 — video craft set = 8; dop-motions.md preserved AND modified during THIS SPEC.
ls $VID/references/prompt-craft/ | sort | tr '\n' ' '
# expect: cinema-studio.md gemini-omni.md grok.md kling.md marketing-studio.md seedance.md veo.md wan.md
test -f $VID/references/dop-motions.md && echo "dop-motions.md preserved: PASS"
# D4 fix: HEAD~1 assumes the file changed in the immediately-preceding commit, but milestones
# use per-M commits. Instead assert a commit of THIS SPEC touched the file (SPEC ID in subject).
git log --oneline -- $VID/references/dop-motions.md | grep -c 'SPEC-MOC-HIGGSFIELD-PROMPT-001'
# expect: ≥1 (a commit of this SPEC modified dop-motions.md — proves updated, not left stale)

# (4) AC-HGF-004 — invented model IDs. Expect: 0 lines.
grep -rnE 'sora_2|veo_3|kling_2_5_turbo|kling_2_1_master|kling_avatars_2_0|seedance_pro|cinema_studio_3_5|minimax_hailuo_02|wan_2_5|soul_2_0|seedream_4_0|wan_2_2_image' "$SK"/media-higgsfield-*

# (5) AC-HGF-005 — retired params. Two-part (D5 fix): (5a) none outside call-schema.md;
#     (5b) none inside a fenced code block IN call-schema.md (a call example must not smuggle them).
# (5a) Expect: 0 lines.
grep -rnE 'width_and_height|duration_seconds|image_url|enhance_prompt|style_strength|custom_reference_id|image_reference_url' "$SK"/media-higgsfield-* \
  | grep -v 'media-higgsfield-core/references/call-schema.md'
# (5b) Expect: 0 lines. (awk carries a per-file fence reset — D6.)
awk 'FNR==1{b=0} /^```/{b=!b; next} b && /width_and_height|duration_seconds|image_url|enhance_prompt|style_strength|custom_reference_id|image_reference_url/{print FILENAME":"FNR": "$0}' \
  $CORE/references/call-schema.md
# …and the exemption is not a loophole — the anti-pattern section must exist (L19):
grep -in 'do not exist' $CORE/references/call-schema.md   # expect: ≥1 match

# (6) AC-HGF-006 — every batch_size occurrence has ms_image within ±3 lines (D7: proximity, not line-scoped).
#     Expect: 0 lines. Catches a '## batch_size' heading whose ms_image context is on a nearby-but-not-same line.
grep -rlE 'batch_size' "$SK"/media-higgsfield-* | while IFS= read -r f; do
  awk 'NR==FNR{ if(/ms_image/) m[FNR]=1; next }
       /batch_size/{ ok=0; for(i=FNR-3;i<=FNR+3;i++) if(i in m) ok=1; if(!ok) print FILENAME":"FNR": "$0 }' "$f" "$f"
done

# (7) AC-HGF-007 — no bracket-enum parameter table in a SKILL.md. Expect: 0 lines.
grep -nE 'resolution\[|duration\[|quality\[|variant\[|mode\[|genre\[|aspect_ratio\[' \
  $CORE/SKILL.md $IMG/SKILL.md $VID/SKILL.md

# (8) AC-HGF-008 — no negative_prompt inside a fenced code block. Expect: 0 lines.
# (D6: per-file fence reset FNR==1{b=0}; portable file enumeration via -exec … {} +.)
find "$SK"/media-higgsfield-* -name '*.md' -exec \
  awk 'FNR==1{b=0} /^```/{b=!b; next} b && /negative_prompt/{print FILENAME":"FNR": "$0}' {} +

# (9) AC-HGF-009 — live-query + preflight present. Expect: no file listed.
grep -L 'models_explore' $CORE/SKILL.md $IMG/SKILL.md $VID/SKILL.md
grep -L 'get_cost'       $IMG/SKILL.md $VID/SKILL.md $CORE/references/job-lifecycle.md

# (10) AC-HGF-010 — namespace resolution. Expect: all three greps ≥1.
grep -c 'mcp__higgsfield__'           $CORE/references/call-schema.md
grep -c 'mcp__claude_ai_higgsfield__' $CORE/references/call-schema.md
grep -ci 'namespace'                  $CORE/references/call-schema.md

# (11) AC-HGF-011 — adjustments + credits rule. Expect: no file listed.
grep -L 'adjustments'   $IMG/SKILL.md $VID/SKILL.md $CORE/references/job-lifecycle.md
grep -L 'credits_exact' $CORE/references/job-lifecycle.md

# (12) AC-HGF-012 (advisory) — flow ordering.
for f in $IMG/SKILL.md $VID/SKILL.md; do
  a=$(grep -n 'models_explore' "$f" | head -1 | cut -d: -f1)
  b=$(grep -n 'get_cost'       "$f" | head -1 | cut -d: -f1)
  c=$(grep -nE 'generate_image|generate_video' "$f" | head -1 | cut -d: -f1)
  echo "$f: models_explore=$a get_cost=$b generate=$c"
done
# expect: a < b < c on both. Advisory — a prose overview mentioning generate_* early is a benign failure.

# (13) AC-HGF-013 — every craft file cites a URL. Expect: no file listed.
# (D1 fix: two explicit globs — a space-joined CRAFT var word-splits so /*.md attaches to only the
#  second token, leaving the 7 image craft files UNCHECKED. Each glob is expanded by the shell here.)
grep -L 'https://' "$IMG"/references/prompt-craft/*.md "$VID"/references/prompt-craft/*.md

# (14) AC-HGF-014 — every craft file declares its evidence tier. Expect: no file listed.
grep -L 'Evidence tier:' "$IMG"/references/prompt-craft/*.md "$VID"/references/prompt-craft/*.md

# (15) AC-HGF-015 — Soul: absence stated, no invented formula label.
grep -ci 'no official prompt formula' $IMG/references/prompt-craft/soul.md     # expect ≥1
# D2 fix: fabricated-formula detector. A fabrication presents an official formula as a heading or
# bold label; an honest absence carries a negation ("No Official Formula", "no official … formula").
# Match heading/bold lines that name an official formula, then SUBTRACT negated lines. Expect 0 lines.
grep -inE '^(#{1,6}|\*\*).*official( [a-z]+)? formula' $IMG/references/prompt-craft/soul.md \
  | grep -viE '\b(no|not|never|none|absent|without)\b'

# (16) AC-HGF-016 — Grok: audio absence stated, no invented formula label.
grep -ci 'no audio documentation' $VID/references/prompt-craft/grok.md          # expect ≥1
grep -inE '^(#{1,6}|\*\*).*official( [a-z]+)? formula' $VID/references/prompt-craft/grok.md \
  | grep -viE '\b(no|not|never|none|absent|without)\b'                          # expect 0 lines

# (17) AC-HGF-017 — Hazel assumption flagged.
grep -c 'openai_hazel' $IMG/references/prompt-craft/openai.md   # expect ≥1
grep -ci 'unverified'  $IMG/references/prompt-craft/openai.md   # expect ≥1

# (18) AC-HGF-018 — R1..R5 each DEFINED (bold rule label), not merely mentioned. Expect: 5.
# (D11 fix: the run-phase author writes each rule as a bold label `**R1 …**` .. `**R5 …**`
#  — a bare mention "see R3" does NOT match. Counting `\bR[1-5]\b` would false-pass on mentions.)
grep -oE '\*\*R[1-5]\b' $CORE/references/universal-rules.md | sort -u | wc -l

# (19) AC-HGF-019 — out-of-scope fallback stated. Expect: no file listed.
grep -Li 'live lookup' $IMG/SKILL.md $VID/SKILL.md

# (20) AC-HGF-020 — the vendor contradiction survives + per-family routing (D3 fix: no
#      language-brittle English heading negative — the "no generic formula" check moved to §D.5
#      inspection because skill prose is Korean. These positive + structural checks are language-robust).
grep -ci 'unstable'      $VID/references/prompt-craft/seedance.md  # expect ≥1 (ByteDance verbatim)
grep -ci 'timestamp'     $VID/references/prompt-craft/wan.md       # expect ≥1 (Alibaba multi-shot formula)
grep -ci 'per-family'    $VID/SKILL.md                             # expect ≥1 (L14)
grep -c  'prompt-craft/' $VID/SKILL.md                             # expect ≥1 (SKILL routes to per-family files, not one generic formula)

# (21) AC-HGF-021 — Google's own broken-references warning, verbatim.
grep -c 'not correctly processed by the model at this time' $VID/references/prompt-craft/gemini-omni.md  # expect ≥1

# (22) AC-HGF-022 — MiniMax silent-override hazard.
grep -c 'prompt_optimizer' $VID/SKILL.md    # expect ≥1

# (23) AC-HGF-023 — Marketing Studio video mutual exclusion.
grep -c  'ad_reference_id'    $VID/references/prompt-craft/marketing-studio.md   # expect ≥1
grep -ci 'mutually exclusive' $VID/references/prompt-craft/marketing-studio.md   # expect ≥1

# (24) AC-HGF-024 — ms_image style pick, never auto-defaulted.
grep -c  'style_id'               $IMG/references/prompt-craft/marketing-studio.md  # expect ≥1
grep -ci 'no default'             $IMG/references/prompt-craft/marketing-studio.md  # expect ≥1
grep -c  'show_marketing_studio'  $IMG/references/prompt-craft/marketing-studio.md  # expect ≥1
```

---

## §D.4 — Indirect verification (live MCP — recorded, not grepped)

These four cannot be verified by a shell command against the repo. Their evidence is the **verbatim MCP transcript**, recorded in `progress.md` §E.2. A claim without the transcript is an unobserved-verification claim and is rejected.

| # | AC | Required evidence in `progress.md` §E.2 |
|---|---|---|
| **E1** | AC-HGF-025 | `balance` before the preflight sweep. Then ≥1 image model and ≥1 video model called with `get_cost: true`, each with the returned `credits` value. Then `balance` again — **identical**. The unchanged balance IS the zero-credit proof. |
| **E2** | AC-HGF-026 | The `generate_image` call (model, params), the returned job ID, the `job_status` poll reaching `completed`, and the result URL. |
| **E3** | AC-HGF-027 | The `generate_video` call (model, params, duration), the job ID, the poll reaching `completed`, and the result URL. |
| **E4** | AC-HGF-028 | `balance_before` and `balance_after` for the whole run. Delta ≤ 10. The delta must reconcile with the sum of the reported `credits` figures — a discrepancy means the billing model is not what the snapshot recorded and MUST be reported, not smoothed over. |

Also recorded (not gated, but required for honesty): every `adjustments` object returned by any call, and whether the live catalog had drifted from `mcp-catalog-snapshot.md`. **Drift found here is not a failure — it is the design being confirmed.**

---

## §D.5 — Criteria verified by inspection only (stated, not gated)

These are real requirements with no honest mechanical check. They are surfaced here rather than hidden behind a grep that would only pretend to test them.

| REQ / AC | Why it is not (fully) gated | How it is checked |
|---|---|---|
| REQ-011 (orchestrator-only interview) | A skill *describing* an interview is indistinguishable by grep from a skill *invoking* `AskUserQuestion`; the qualitative flow cannot be grepped. But a literal invocation CAN be tripwired. | **Mechanical tripwire** (D10): `grep -rn 'AskUserQuestion(' "$SK"/media-higgsfield-*` → **expect 0** (a subagent must never invoke it). **Then qualitative**: read the interview section of each `SKILL.md` — it must define **slots to collect**, not tool calls. |
| REQ-013 (nested `params{}`) | Partially covered — the F3/F6 bans make a flat call hard to write. But a well-formed flat call using *correct* names would slip through. | Read one call example per `SKILL.md`; confirm the `params:` nesting. |
| REQ-023 (balance halt) | An unexercised error path. Forcing it would require deliberately overspending. | Read `job-lifecycle.md`; confirm the halt rule is stated. |
| AC-020 residual (no single generic video-formula section) | The skill prose is **Korean** (plan.md D-1), so a generic-formula heading like `## 범용 비디오 프롬프트 공식` evades an English-string negative grep. AC-020's mechanical part therefore proves the contradiction *positively* (seedance `unstable` + wan `Timestamp` + `per-family` + `prompt-craft/` routing); the *absence* of a generic section is inspection-only. | Read `$VID/SKILL.md`: confirm it routes to per-family craft files and presents **no** single unified "video prompt formula" section (in any language). This is AP-1, the SPEC's #1 named anti-pattern. |
| AC-015 / AC-016 residual (adversarial negation injection) | The D2 fabricated-formula grep subtracts lines carrying a negation word. An adversarial author could defeat it by inserting a stray "no" into a fabricated formula heading (e.g. `## Official Formula (no exceptions): …`). | Read `soul.md` / `grok.md`: confirm any "official formula" / "audio" heading is a genuine **absence statement**, not a fabrication wearing a negation word. The mechanical grep covers the realistic case; this covers the adversarial one. |

---

## §D.6 — Closure gates

The SPEC closes when **all of the following hold**:

1. Every **BLOCKER** AC is PASS (18 of them). No exceptions, no PASS-WITH-DEBT.
2. Every **MAJOR** AC is PASS, or is explicitly recorded as debt in `progress.md` §E.3 with a named follow-up.
3. The **MINOR** AC (AC-HGF-012) result is reported, whatever it is.
4. The §D.4 evidence table is populated with verbatim MCP transcripts — not summaries.
5. §D.5 inspection results are stated honestly, including any that failed.

---

## §D.7 — Known non-verifiable residuals (declare, do not hide)

| # | Residual | Why it survives |
|---|---|---|
| **N-1** | Only one MCP namespace will actually be exercised at E2E — whichever registration the session runs under. The other prefix remains **unverified in practice**. | Cannot run both registrations in one session. Record which one was used; do not claim both work. |
| **N-2** | Craft-file *correctness* (does a Veo prompt written per `veo.md` actually produce better output?) is not measured. The ACs verify **provenance and fidelity to the vendor's published convention**, not generation quality. | Quality measurement would require a controlled A/B against a scoring rubric — a different SPEC. |
| **N-3** | Only 2 of 60 models are exercised end-to-end. The other 58 are covered by the design (live query), not by a test. | 10-credit balance. This is a budget limit, not an oversight — say so. |
| **N-4** | The catalog may drift again the day after this SPEC closes. | That is the point. The SPEC's thesis is that drift is inevitable and must be absorbed by live query, not resisted by a table. A future drift that breaks nothing is the design working. |

---

## §E — Given–When–Then scenarios

### GWT-1 — The core defect is gone (the reason this SPEC exists)

> **Given** a user asks for a Higgsfield video and the assistant loads `media-higgsfield-video`,
> **When** the skill selects a model candidate,
> **Then** it calls `models_explore(action:'get')` for that model and derives duration, aspect ratio, and media roles from the live response — **and** no model ID, enum, or aspect table anywhere in the skill was the source of those values.
>
> *Verified by*: AC-HGF-004, AC-HGF-007, AC-HGF-009.
> *Broken-fixture check*: reinstating the old `sora_2` table fails AC-HGF-004 immediately.

### GWT-2 — Cost is never spent blind, and silent substitutions are surfaced

> **Given** a user requests a video with audio on `cinematic_studio_3_0`,
> **When** the skill prepares the call,
> **Then** it first issues `get_cost: true` (zero credits) and reports the `credits` figure; **and when** the response carries `adjustments` showing the server substituted `generate_audio: false`, the skill **reports that substitution to the user** rather than delivering a silent video the user believes has sound.
>
> *Verified by*: AC-HGF-011, AC-HGF-025.
> *This is not hypothetical* — `mcp-catalog-snapshot.md` §5.1 records exactly this `adjustments` payload from a live preflight.

### GWT-3 — Evidenced absence is stated, not filled

> **Given** a user asks for a Soul 2.0 image,
> **When** the skill loads `references/prompt-craft/soul.md`,
> **Then** the file states that **no official prompt formula exists** and that Higgsfield's design is deliberately anti-formula, and falls back to R1–R5 — **and** presents no invented "Soul formula".
>
> *Verified by*: AC-HGF-015.
> *Broken-fixture check*: adding a `**Official formula**:` label to `soul.md` fails AC-HGF-015's negative check.

### GWT-4 — The contradiction between vendors is preserved, not averaged

> **Given** a user requests a multi-shot video,
> **When** the target is Wan, **Then** the assembled prompt uses **explicit timestamp ranges** (Alibaba's official formula);
> **When** the target is Seedance, **Then** the assembled prompt uses a **bare labeled shot list with no timestamps** (ByteDance states timestamps destabilize the model).
>
> *Verified by*: AC-HGF-020.
> *This is the corollary made concrete*: any "unification" of these two into one video formula is a correctness regression, not a cleanup.

### GWT-5 — A model outside the 15 families still works

> **Given** a user requests `z_image` or `kling_omni_image` — models with no craft file,
> **When** the skill runs,
> **Then** it live-queries the catalog for constraints, applies the universal rules R1–R5, and **says explicitly** that no family-specific craft guidance exists for this model.
>
> *Verified by*: AC-HGF-019.
> *This is a stated scope boundary, not a gap* — see `spec.md` §F.

---

## §F — Definition of Done

- [ ] All 18 BLOCKER ACs PASS with verbatim command output cited.
- [ ] All MAJOR ACs PASS, or debt recorded with a follow-up.
- [ ] MINOR AC result reported.
- [ ] E2E: 1 image + 1 video generated, both `completed`, both result URLs recorded, spend ≤ 10 credits and reconciled.
- [ ] `progress.md` §E.2 carries the verbatim MCP transcripts (not summaries).
- [ ] `progress.md` §E.3 carries the run-phase audit-ready signal, including §D.5 inspection results and §D.7 residuals restated as observed.
- [ ] Commits pushed to `main` (main-direct route, no PR).
- [ ] No file outside `plugins/moai-media/skills/media-higgsfield-{core,image,video}/` and this SPEC's `progress.md` was modified.
