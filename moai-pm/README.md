# moai-pm

> 한국 팀 주간업무보고(WBR) 작성 자동화

[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

한국 직장 문화에 정착된 주간업무보고(WBR) 작성을 자동화합니다. 6섹션 표준 보고와 임원용 1pager 두 버전을 출력하며, 격식체/구어체 톤 스위치를 지원합니다. 자유 텍스트 입력만으로 동작합니다.

## 스킬 카탈로그

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
  weekly-report → moai-bi:executive-summary

발표 슬라이드
  weekly-report → moai-core:ai-slop-reviewer → moai-office:pptx-designer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 일간 보고 | `moai-business:daily-briefing` |
| C-level 1pager | `moai-bi:executive-summary` |

## 라이선스

MIT
