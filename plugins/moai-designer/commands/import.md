---
description: Claude Design → Claude Code 핸드오프 번들(.zip 또는 붙여넣기 프롬프트+URL) import 및 분석
argument-hint: "[번들 .zip 경로 또는 번들 URL]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Import and analyze a Claude Design handoff bundle (README-first, defensive glob).

Use Skill("design-workflow") with arguments: $ARGUMENTS

Then Skill("design-handoff-reader") to summarize the bundle and emit the paste-ready Claude Code instruction.

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > Claude Design 핸드오프 받아서 읽어줘
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
