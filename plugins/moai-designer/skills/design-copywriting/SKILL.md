---
name: design-copywriting
description: "마케팅·제품 텍스트의 브랜드 정합 카피라이팅 전문가. 브랜드 보이스, AI 특유 어조 배제 규칙, 구체적 숫자, 다운스트림 에이전트 소비를 위한 JSON 섹션 구조를 보장합니다. 히어로, 기능, 소셜 증명, CTA, 푸터 섹션을 A/B 변형 출력으로 다룹니다."

  Use for brand-aligned marketing and product copy: headlines, CTAs,
  microcopy, taglines, value propositions, marketing-landing-page and footer copy,
  with anti-AI-slop rules and concrete-number enforcement.
user-invocable: false
version: "1.1.0"
---

> ⚠️ **개발 런타임 전용** — 이 스킬은 MoAI-ADK(Claude Code) 환경을 전제한다. Claude Cowork(Desktop)에서는 `.moai/config` 의존으로 동작하지 않을 수 있다. Desktop 사용자는 `moai-marketer:content-copywriting`을 사용한다.

# design-copywriting

Brand-aligned content-copywriting skill for marketing and product websites. Absorbed from the retired v2.x `*-copywriting` capability (per the content-copywriting absorption policy) at v3.2.0. Enforces anti-AI-slop rules, requires brand voice context, and outputs structured JSON per section.

---

## Quick Reference

### Entry Conditions

Before generating copy, verify all three conditions are met:

1. Brand voice context is loaded: `.moai/project/brand/brand-voice.md` exists or is provided inline.
2. Target page or section scope is explicitly stated (landing page, about, pricing, etc.).
3. Anti-AI-slop checklist is active (see below).

If `brand-voice.md` does not exist, stop and instruct the user to run the brand interview via `/design` (Path B brand-interview).

### Output Format

All copy output is structured JSON with the following top-level sections:

```
{
  "page_type": "<landing|about|services|pricing|contact>",
  "sections": {
    "hero": { "primary": {...}, "variant_a": {...} },
    "problem": { "primary": {...}, "variant_a": {...} },
    "solution": { "primary": {...}, "variant_a": {...} },
    "features": { "primary": {...}, "variant_a": {...} },
    "cta": { "primary": {...}, "variant_a": {...} },
    "pricing": { "primary": {...}, "variant_a": {...} }
  },
  "metadata": {
    "tone_profile": "<string>",
    "word_count": <number>,
    "reading_level": "<string>"
  }
}
```

Each section must include at least one A/B variant (`variant_a`). The `primary` field is the recommended default.

---

## Implementation Guide

### Section Structure

**hero**: The first visible block. Subject must be the reader outcome, not the company name.
- `headline`: Max 12 words. Present tense. Outcome-first.
- `subheadline`: One sentence. Expands the headline mechanism. Max 25 words.
- `cta_primary`: Verb + noun. Max 5 words. ("Start your free trial", "See how it works")
- `cta_secondary`: Optional. Softer alternative. ("Learn more", "Watch demo")

**problem**: Acknowledges the reader's pain point before proposing a solution.
- `headline`: Frame the cost of the status quo. Specific, not abstract.
- `body`: 2-3 sentences. Use second-person ("you", "your team").

**solution**: Introduces your product or service as the answer.
- `headline`: Direct claim with mechanism. ("We automate X so you can Y.")
- `body`: 3-4 sentences. State what it is, how it works, and one concrete outcome.

**features**: Scannable list of capabilities.
- Each feature: `title` (max 5 words) + `description` (max 2 sentences) + optional `metric`.
- Maximum 6 features per section.

**cta**: Final conversion prompt.
- `headline`: Urgency or clarity without manipulation. Avoid "limited time" cliches.
- `button_text`: Same rules as hero `cta_primary`.
- `supporting_text`: Trust signal (money-back guarantee, no credit card, etc.)

**pricing**: Only include if explicitly requested in scope.
- `headline`: Framing statement. ("Simple pricing. No surprises.")
- Plans array: `name`, `price`, `billing_period`, `highlights` (max 5 bullet strings).

---

### Anti-AI-Slop Checklist

Every piece of generated copy must pass this checklist before delivery:

**Forbidden patterns** — Reject any copy containing:
- Exclamation marks used more than once per section
- "In today's fast-paced world" or equivalent opening
- "Cutting-edge", "state-of-the-art", "revolutionary", "game-changing"
- "Leverage" as a verb (replace with "use", "apply", "deploy")
- "Seamless", "frictionless", "best-in-class" without quantified evidence
- Passive voice where active is grammatically equivalent
- Filler clauses: "at the end of the day", "the fact of the matter is"
- Generic benefits without concrete mechanism ("helps you succeed")
- Third-person self-reference in hero section ("Our company believes...")

**Required patterns** — Every section must have:
- At least one concrete number, percentage, or time reference
- Reader-centric framing (subject is "you" or reader outcome, not "we")
- Active voice for all capability claims
- Specificity: replace "grow your business" with a measurable outcome

**Tone calibration** — Load from `brand-voice.md`:
- Respect the tone spectrum defined (e.g., "playful" vs "authoritative")
- Match vocabulary preferences (avoid jargon if `jargon_level: low`)
- Preserve brand-specific terminology exactly as defined

---

### A/B Variant Rules

Each section must include one alternative version (`variant_a`) that differs in:
- Headline framing angle (problem-first vs. solution-first)
- CTA verb choice
- Tone register (slightly more or less formal)

Do not generate more than two variants unless the scope explicitly requires it.

---

### Brand Voice Integration

Load `.moai/project/brand/brand-voice.md` and apply:

1. `tone`: Overall register. If missing, default to "confident and direct".
2. `vocabulary_preferences`: Preferred and avoided terms. Enforce strictly.
3. `audience_familiarity`: Determines assumed knowledge level. Adjust jargon accordingly.
4. `example_phrases`: Use as stylistic anchors. Mimic sentence rhythm, not content.

If any `_TBD_` markers are present in `brand-voice.md`, stop and request completion before proceeding.

---

### Integration with design-brand-system

When both content-copywriting and design work are in scope (path B of `/moai design`):

1. Complete copy sections first and output structured JSON.
2. Pass the JSON copy output to `design-brand-system` as the content contract.
3. Design tokens and layout must accommodate copy length constraints (headline character counts, CTA button text length).

---

## Advanced Patterns

### Reading Level Targeting

Adjust copy complexity to the target audience's reading level:

- Technical audience (B2B SaaS developers): Grade 10-12. Allow domain terminology.
- Business audience (SMB owners): Grade 8-10. Avoid acronyms without expansion.
- Consumer audience (general public): Grade 6-8. Short sentences, concrete imagery.

Include the calculated reading level in the output metadata `reading_level` field using the Flesch-Kincaid grade level scale.

### Microcopy Guidelines

Form labels, error messages, and UI strings follow stricter rules:
- Labels: noun phrases, 1-3 words, no punctuation
- Placeholders: example values, not instructions ("jane@company.com" not "Enter email")
- Error messages: what went wrong + how to fix it, no blame language
- Success messages: confirm the action, state the next step

### Social Proof Integration

When testimonials or case study data are available in brand context:
- Quote exactly, do not paraphrase customer quotes
- Include company name, role, and metric (where permitted)
- Place after the problem section (reaffirms pain) or after features (reaffirms solution)

---

## Anti-Slop Pattern Dictionary (absorbed from design-slop-check)

This dictionary is the canonical anti-AI-slop reference for the design pipeline. It was
absorbed from the `design-slop-check` skill per `docs/plugin-family-design/03-moai-design-processing.md`
§3.3 — content-copywriting is the canonical owner (proactive avoidance at generation time), while
`design-slop-check` remains a downstream QA gate that references this dictionary. Reject or flag
copy matching these patterns before delivery, and replace with concrete numbers / reader
outcomes.

### English clichés (Tier 1 — almost always slop)

- "Reimagine your [X]"
- "Unleash your [X]" / "Unleash the power of [X]"
- "Empower your team to [X]"
- "Transform the way you [X]"
- "Supercharge your [X]"
- "Revolutionize [X]"
- "Next-generation [X]"
- "Cutting-edge [X]"
- "Powered by AI"
- "Built for the future of [X]"
- "Where [X] meets [Y]" (marketing headlines especially)

### English suspicious phrases (Tier 2 — context-dependent)

- "Game-changing", "Best-in-class"
- "Seamlessly", "Effortlessly", "Intuitively"
- "Leverage", "Synergy"
- "World-class", "State-of-the-art"
- "[X], simplified" / "[X], reimagined" / "[X], unleashed"

### Korean clichés (Tier 1 — 거의 항상 슬롭)

- "혁신적인 [X]"
- "차세대 [X]"
- "재정의하는 [X]"
- "새로운 패러다임"
- "AI 기반의 [X]"
- "한 차원 높은 [X]"
- "지금까지 없던 [X]"
- "당신의 [X]를 변화시킬"
- "이제는 [X]의 시대"

### Korean suspicious phrases (Tier 2 — 문맥 확인 필요)

- "원활하게", "손쉽게", "직관적으로"
- "최고의", "최첨단의"
- "강력한", "막강한"
- "한 번에", "단숨에"
- "더 이상 [X]에 시달리지 마세요"

### Copy-structure anti-patterns

- **A B C D adjective enumeration**: "Faster. Smarter. Better. Simpler." — meaningless adjective list (형용사 나열)
- **Colon-then-emphasis**: "[Headline]: The X that finally Y"
- **Unquantified statistics**: "Trusted by thousands of customers" (no concrete number)
- **Needless negation → affirmation**: "No more [X]. Just [Y]."

Downstream chaining note: for Korean output, an optional post-processing pass via a humanizer
skill (e.g. `moai-domain-humanize`) may follow — this is an optional refinement, not a hard
dependency.

---

## Works Well With

- `design-brand-system`: Visual design must accommodate copy constraints
- `design-iteration-loop`: GAN loop evaluates copy quality in Design Quality and Completeness dimensions
- `expert-frontend`: Receives the JSON copy output for implementation
- 카피 정확도 셀프체크: 본 스킬의 brand-voice 정렬 체크리스트로 카피 정확도를 검증합니다. MoAI harness(`moai`)의 `sync-auditor`가 함께 설치된 환경에서는 해당 agent로 평가를 보강할 수 있습니다.

---

## 관련 스킬

| 단계 | 스킬 | 용도 |
|---|---|---|
| Post-검수 | `moai-coworker:ai-slop-reviewer` | AI 슬롭 검수 (필수) |
| Post-검수 | `moai-writer:korean-humanize` | 한국어 AI 티 제거 (슬롭 검수 다음, 필수) |

---

Source: Absorbed from the retired v2.x `*-copywriting` capability v3.2.0 per the content-copywriting absorption policy.
REQ coverage: (internal provenance omitted)
Version: 0.1.0
