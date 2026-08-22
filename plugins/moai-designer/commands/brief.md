---
description: 6요소 Claude Design 브리프 빌더 (Project·Audience·Pages·Tone·Reference·Constraints)
argument-hint: "[자연어 한 줄 디자인 요청]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Use Skill("design-brief") with arguments: $ARGUMENTS

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > 디자인 브리프 만들어줘 — 프로젝트·대상·페이지·톤·레퍼런스·제약 6가지로
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
