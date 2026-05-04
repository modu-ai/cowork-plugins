# moai-pm

> 한국 팀의 프로젝트 관리·주간보고·OKR·회고 자동화

[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

월요 WBR·금요 마무리·분기 OKR·KPT 회고 등 한국 직장 문화에 정착된 프로젝트 관리 의례를 자동화합니다. Notion·Linear·Asana·Slack MCP가 가용하면 자동 활용, 없어도 자유 텍스트 입력으로 동작합니다.

## 스킬 카탈로그 (v2.0.0 기준)

| 스킬 | 설명 | 출시 |
|---|---|---|
| [weekly-report](./skills/weekly-report/SKILL.md) | 한국 WBR 6섹션 주간보고 + 임원 1pager | ✅ v2.0.0 |

## 시작하기

```bash
/plugin marketplace update cowork-plugins
```

```
주간보고 만들어줘
→ weekly-report 호출, 6섹션 표준 + 임원 1pager 두 버전 출력
```

## 주요 워크플로우 체인

```
주간보고 → C-level 1pager
  standup-summarizer → weekly-report → executive-summary

발표 슬라이드
  weekly-report → ai-slop-reviewer → pptx-designer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 일간 보고 | `moai-business/daily-briefing` |
| 분기 회고 | (예정) `moai-pm/retro-facilitator` |
| C-level 1pager | `moai-bi/executive-summary` |

## MCP 통합 (이미 가용)

- Notion · Linear · Asana — 데이터베이스/이슈 자동 fetch
- Slack — 스탠드업 노트 import (예정 스킬)
- Gmail — 주간보고 발송 (예정 스킬)

## 라이선스

MIT
