---
description: 프로젝트 초기화 단일 진입점 — 소크라테스 인터뷰 후 커스텀 에이전트·스킬 체인·AGENTS.md 생성. update/evolve/doctor 하위 모드 지원
argument-hint: "[update|evolve|doctor] <자연어 지시>"
allowed-tools: Skill
---
<!-- moai-pm /project · 단일 진입점 (skills/project) · a2fc84b9 에서 rename 중 실수로 삭제되었던 것을 복원 -->

Use Skill("moai-pm:project") with arguments: $ARGUMENTS

---

> **ChatGPT Work(Codex)에서는** 슬래시 명령이 없습니다 — Codex 플러그인 규격은 `skills/`·`hooks/`·
> `.mcp.json`만 지원하고 `commands/`는 지원하지 않습니다. 기능은 그대로 있으니 자연어로 부르세요:
>
> > 새 프로젝트 시작해줘 — 지침이랑 에이전트 만들어줘
>
> 이 커맨드는 Claude Cowork 전용 단축키이며, 실제 일은 위 `Skill(...)`이 합니다.
