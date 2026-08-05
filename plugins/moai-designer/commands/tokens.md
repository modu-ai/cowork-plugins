---
description: 브랜드 자산 → DESIGN.md + DTCG 디자인 토큰(색·타이포·spacing·radii·shadows) 합성
argument-hint: "[브랜드 자산 경로 또는 URL]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Synthesize brand assets into DESIGN.md, then derive the DTCG design token set.

Use Skill("design-system-prep") with arguments: $ARGUMENTS

Then Skill("moai-domain-brand-design") to produce the WCAG 2.1 AA-compliant tokens.
