---
description: 디자인 카피 AI 슬롭 감사 → 검수 보고서 + 대안 (영문·한국어 패턴 사전)
argument-hint: "[검수할 카피 텍스트 또는 파일 경로]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Audit design copy for AI slop and return a review report with alternatives.

Use Skill("design-slop-check") with arguments: $ARGUMENTS

The anti-slop pattern dictionary is owned by Skill("design-copywriting") (generation-time avoidance).

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > 이 디자인 카피 AI 티 나는지 검수해줘
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
