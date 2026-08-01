---
title: "심화 — MCP·서브에이전트·스킬·훅"
weight: 102
---

# 심화 — MCP·서브에이전트·스킬·훅

## MCP (Model Context Protocol)

외부 도구·데이터베이스·API를 연결합니다. `claude mcp add`로 추가합니다.

**예**: 데이터베이스 MCP를 추가하면 Claude가 직접 쿼리를 실행해 데이터를 읽습니다.

## 서브에이전트 (Sub-agents)

전문화된 보조 에이전트에 작업을 위임합니다.

**예**: 코드 리뷰를 서브에이전트에 맡기면, 부모 컨텍스트를 보존하면서 깊은 리뷰를 수행합니다. 서브에이전트는 사용자에게 직접 질문할 수 없습니다.

## 스킬 (Skills)

상황에 맞춰 Claude가 자동 호출하는 확장 능력(`SKILL.md`). progressive disclosure로 토큰을 아껴 씁니다.

## 훅 (Hooks)

라이프사이클 시점에 자동 실행합니다.

**예**:
- `PostToolUse` — 파일 저장 후 자동 포맷팅
- `PreToolUse` — `.env` 파일 읽기 차단

## Sources

- [MCP](https://code.claude.com/docs/en/mcp)
- [Sub-agents](https://code.claude.com/docs/en/sub-agents)
- [Skills](https://code.claude.com/docs/en/skills)
- [Hooks](https://code.claude.com/docs/en/hooks)
