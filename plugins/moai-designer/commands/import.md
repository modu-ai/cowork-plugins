---
description: Claude Design → Claude Code 핸드오프 번들(.zip 또는 붙여넣기 프롬프트+URL) import 및 분석
argument-hint: "[번들 .zip 경로 또는 번들 URL]"
allowed-tools: Skill
---
<!-- source-spec: docs/plugin-family-design/03-moai-design-processing.md §5.1 -->

Import and analyze a Claude Design handoff bundle (README-first, defensive glob).

Use Skill("design-workflow") with arguments: $ARGUMENTS

Then Skill("design-handoff-reader") to summarize the bundle and emit the paste-ready Claude Code instruction.
