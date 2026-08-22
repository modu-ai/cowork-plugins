---
description: 브랜드 자산 → DESIGN.md + DTCG 디자인 토큰(색·타이포·spacing·radii·shadows) 합성
argument-hint: "[브랜드 자산 경로 또는 URL]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Synthesize brand assets into DESIGN.md, then derive the DTCG design token set.

Use Skill("design-system-prep") with arguments: $ARGUMENTS

Then Skill("design-brand-system") to produce the WCAG 2.1 AA-compliant tokens.

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > 브랜드 디자인 토큰 만들어줘
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
