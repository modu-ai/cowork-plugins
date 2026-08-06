---
name: design-handoff
description: "/design Path A 워크플로의 Claude Design 핸드오프 패키지 전문가. 붙여넣기 바로 쓰는 claude.com Design 세션용 5파일 핸드오프 번들(prompt/context/references/acceptance/checklist)을 조립합니다. 브랜드 미비 폴백과 섹션 재생성을 처리합니다."

  Use for /design Path A design handoff: assembling the 5-file Claude
  Design package (prompt, context, references, acceptance, checklist),
  brand-voice context, and paste-ready claude.com session bundles.
user-invocable: false
version: "1.1.0"
---

> ⚠️ **개발 런타임 전용** — 이 스킬은 MoAI-ADK(Claude Code) 환경을 전제한다. Claude Cowork(Desktop)에서는 `.moai/config` 의존으로 동작하지 않을 수 있다. Desktop 사용자는 `moai-designer:design-handoff-reader`를 사용한다.

<!-- Verifies: prompt.md is paste-ready (no MoAI tokens) -->
<!-- Verifies: Brand voice integrated when present; graceful default when absent -->
<!-- Verifies: Handoff exit AskUserQuestion with 3 options -->

<!-- @MX:ANCHOR: [AUTO] 5-section prompt.md template structure — canonical definition -->
<!-- @MX:REASON: Consumed by every /design Path A handoff execution (high fan_in). Structural changes affect user trust — prompt.md is pasted directly into external claude.com Design session. -->

# Design Handoff Domain Specialist

Assembles the 5-file Claude Design handoff package for the `/design` Path A workflow (the handoff-deliverable step). The package is designed for paste-and-go use in the external claude.com Design product.

## Quick Reference

The handoff package lives at `.moai/design/handoff/`:

| File | Purpose | Paste target |
|------|---------|-------------|
| `prompt.md` | Master prompt — paste directly into claude.com Design | Yes (primary) |
| `context.md` | Extended context for reference during design session | Optional supplement |
| `references.md` | Visual reference URLs and design inspiration sources | Referenced in prompt |
| `acceptance.md` | Design acceptance criteria (WCAG, responsive, brand) | Referenced in prompt |
| `checklist.md` | Pre-paste self-check before using in claude.com Design | Human review tool |

Key guarantees:

- [HARD] `prompt.md` contains NO MoAI-specific tokens (no `SPEC-`, `.moai/`, `manager-`, internal skill names)
- [HARD] Brand voice integrated when `.moai/project/brand/brand-voice.md` exists
- [HARD] Brand-absent fallback: `Brand Voice (default — please customize)` placeholder section
- [HARD] Handoff exits with AskUserQuestion offering 3 options (a/b/c per the relevant requirement)
- [HARD] All 5 files produced regardless of brand context availability

---

## Handoff Package Assembly

### Input

- Bundle summary from `design-handoff-reader` (the preceding Path A step) — what the user wants designed, target users, value propositions
- Brief from `design-brief` when the request originates from a design brief (Lean Canvas / evaluation context)
- Optional: `.moai/project/brand/brand-voice.md` (brand context)
- Optional: `.moai/project/brand/visual-identity.md` (design tokens, colors)

### Step 0: Brand Context Detection

Before writing any file, check brand context:

```
IF .moai/project/brand/brand-voice.md exists AND is non-empty:
  Load brand voice → use in Brand Voice section of prompt.md
  SET brand_present = true
ELSE:
  Use default brand voice placeholder
  SET brand_present = false
  Note: will include AskUserQuestion offer to run brand interview
```

### Step 1: Assemble prompt.md

<!-- @MX:WARN: [AUTO] prompt.md template — output pasted into external claude.com Design session -->
<!-- @MX:REASON: Changes to this template affect what users paste into claude.com. Structural changes can break user's design sessions. Validate against current claude.com Design prompt guidelines before modifying. -->

`prompt.md` MUST follow this exact 5-section structure:

1. **Goal** — 2-3 sentences describing what needs to be designed, target users, top 3 value propositions from the bundle summary / brief UVP
2. **References** — 3-5 URLs to existing products with style notes, plus key aesthetic direction
3. **Brand Voice** — Two branches (brand_present vs brand_absent), see decision below
4. **Acceptance Criteria** — Concise non-negotiable requirements list (5-8 items)
5. **Out of Scope** — Explicit exclusions (3-5 items)

#### Section 3 — Brand Voice Decision Tree

- Branch A (`brand_present = true`): Extract personality + voice guidelines + color palette + typography from brand-voice.md and visual-identity.md
- Branch B (`brand_present = false`): Emit `## 3. Brand Voice (default — please customize)` header with explicit placeholder + instructions to either edit or run brand interview

See [5-section prompt template + brand branches detail](references/prompt-template.md) for verbatim section templates.

#### Prohibited Content in prompt.md

[HARD] The following MUST NOT appear anywhere in prompt.md:

- References to `SPEC-` identifiers (e.g., `SPEC-AUTH-001`)
- References to `.moai/` paths (e.g., `.moai/design/`, `.moai/project/`)
- References to internal skill / agent names (e.g., `manager-spec`, `design-brief`, `design-handoff-reader`)
- References to internal workflow step identifiers
- References to MoAI-specific commands (e.g., `/design`, `/moai plan`)
- Internal implementation details (file structures, Go code, database schemas)

The prompt must read as if written by a human product designer with no knowledge of MoAI's internal structure.

### Steps 2-5: Supporting Files

| Step | File | Purpose |
|------|------|---------|
| 2 | references.md | Competitor analysis + visual inspiration + UX pattern references (3-5 URLs from the bundle's Sources). Falls back to instructional note when URLs are scarce. |
| 3 | acceptance.md | Accessibility (WCAG 2.1 AA), Responsiveness (375/768/1280px), Brand Alignment, Content Completeness, Technical Constraints |
| 4 | context.md | Extended context — NOT for pasting into Claude Design. Full brief summary, roadmap context, research findings, brand context |
| 5 | checklist.md | Human self-check before pasting prompt.md: content review, MoAI-internal cleanup (auto-verified), scope verification, session readiness |

See [supporting files templates](references/supporting-files.md) for verbatim references.md, acceptance.md, context.md, and checklist.md templates.

---

## Handoff Exit: AskUserQuestion

After all 5 files are written, the skill MUST surface an AskUserQuestion (with ToolSearch preload) presenting 3 options:

```
ToolSearch(query: "select:AskUserQuestion")
AskUserQuestion({
  questions: [{
    question: "핸드오프 패키지가 준비되었습니다. 다음 단계를 선택하세요.",
    header: "Design 핸드오프 완료",
    options: [
      {
        label: "Claude Design 세션 시작 (권장)",
        description: "prompt.md를 claude.com Design에 복사해 붙여넣고 디자인 세션을 시작합니다. context.md/references.md는 보조 자료로 함께 엽니다."
      },
      {
        label: "수동 검토",
        description: "핸드오프 파일을 직접 검토하고 필요한 경우 편집합니다. .moai/design/handoff/ 디렉토리를 확인하세요. 준비가 되면 prompt.md를 Claude Design에 붙여넣으세요."
      },
      {
        label: "핸드오프 패키지 재생성",
        description: "prompt.md 또는 다른 파일에 수정이 필요한 경우 어떤 부분을 변경할지 알려주세요. 해당 파일만 재생성합니다."
      }
    ]
  }]
})
```

For non-Korean conversation_language, translate option labels and descriptions accordingly.

---

## Works Well With

- `design-brief`: Produces the design brief (Lean Canvas + value propositions) consumed as primary input when the request originates from a brief
- `design-system-prep` / `design-system-library`: Provides reference URLs and visual inspiration for the references.md Sources
- `design-handoff-reader`: Preceding Path A step — summarizes the imported bundle into the inputs this skill consumes
- `design-workflow`: Downstream consumer of the `.moai/design/handoff/` directory after the user completes the external Claude Design session (Path A handler)

---

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "Including SPEC-AUTH-001 in prompt.md helps the designer understand scope" | prompt.md is for claude.com Design, not MoAI. SPEC IDs are internal. Use the Out of Scope section to describe scope boundaries in plain English. |
| "I should skip checklist.md — it's obvious" | Checklist.md prevents the most common error: pasting a prompt with placeholder Brand Voice. It takes 30 seconds to complete and saves a bad design session. |
| "references.md is optional if research had no URLs" | references.md is always produced. When URLs are scarce, include a note asking the user to add their own. An empty references file is worse than one with instructions. |
| "If brand is absent, skip the Brand Voice section" | Brand Voice section is always present. Brand-absent path produces an explicit placeholder with instructions — clearer than a missing section. |

## Verification

- [ ] All 5 files produced: prompt.md, context.md, references.md, acceptance.md, checklist.md
- [ ] prompt.md has exactly 5 sections (Goal, References, Brand Voice, Acceptance, Out of Scope)
- [ ] prompt.md contains no SPEC- identifiers
- [ ] prompt.md contains no .moai/ path references
- [ ] prompt.md contains no internal skill/agent names or /design references
- [ ] Brand-absent path includes "Brand Voice (default — please customize)" header in prompt.md
- [ ] context.md includes note that it is NOT for pasting into Claude Design
- [ ] Handoff exit AskUserQuestion called with exactly 3 options
