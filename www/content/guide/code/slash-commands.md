---
title: "필수 슬래시 명령"
weight: 93
---

# 필수 슬래시 명령

세션 안에서 `/`로 시작하는 명령입니다. 비개발자가 우선 알면 좋은 5개입니다.

## 5개 핵심 명령

- `/init` — CLAUDE.md 초기화. 프로젝트 처음 시작할 때
- `/clear` — 컨텍스트 비우기. 대화가 길어져 새 시작이 필요할 때
- `/compact` — 컨텍스트 요약/압축. 대화를 유지하되 분량을 줄일 때
- `/diff` — 변경사항 보기. 뭘 바꿨는지 확인할 때
- `/cost` — 비용 확인. 얼마나 썼는지 볼 때

## 초보자가 가장 많이 쓰는 순서

`/init`(시작) → 작업 → `/cost`(확인) → `/clear`(정리)

## 더 보기

`/` 입력 시 전체 목록이 자동 완성으로 뜹니다. 자주 쓰는 것들:

- `/help` — 도움말
- `/model` — 모델 전환 (Opus·Sonnet·Haiku)
- `/agents` — 서브에이전트 관리
- `/permissions` — 권한 규칙
- `/mcp` — MCP 서버 설정
- `/config` — 전체 설정

## Sources

- [Commands (slash commands)](https://code.claude.com/docs/en/commands)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
