# moai-bi

> 데이터 분석·BI 대시보드 설계·경영진 1pager 자동화

[![Version](https://img.shields.io/badge/Version-1.8.1-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

K-IFRS·KOSIS·DART 친화적 한국 통계 환경에서 경영진이 5분 안에 의사결정할 수 있는 1페이지 보고를 만듭니다. moai-finance와 직접 체이닝하여 재무 데이터를 임원 관점으로 재구성합니다.

## 스킬 카탈로그 (v1.8.1 기준)

| 스킬 | 설명 | 출시 |
|---|---|---|
| [executive-summary](./skills/executive-summary/SKILL.md) | C-level 1pager (≤500단어, What/So What/Now What) | ✅ v1.6.0 |
| dashboard-designer | BI 대시보드 설계서 (Tableau/Looker/Metabase 입력) | ⏸️ v1.9+ |
| kpi-tree | North Star → 하위 지표 트리 분해 | ⏸️ v1.9+ |
| cohort-analyzer | 코호트 리텐션 분석 보고 | ⏸️ v1.9+ |
| funnel-analyzer | 전환 깔때기 + 드롭오프 진단 | ⏸️ v1.9+ |

## 시작하기

```bash
/plugin marketplace update cowork-plugins
```

```
이 분기 변동분석 보고서를 임원 1pager로
→ executive-summary 가 ≤500단어 1pager + 의사결정 옵션·권고 출력
```

## 주요 워크플로우 체인

```
재무 → 경영진 보고
  variance-analysis → executive-summary → pptx-designer

주간 → C-level
  weekly-report → executive-summary
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 팀 단위 주간 (6섹션 상세) | `moai-pm/weekly-report` |
| 전략 본문 (요약 아닌 상세) | `moai-business/strategy-planner` |
| 재무 분석 (변동·예측) | `moai-finance/variance-analysis` |

## 한국 BI 환경 친화

- K-IFRS 재무 지표 우선 표기 (영업이익률·EBITDA·CAGR)
- KOSIS·한국은행 ECOS·DART 인용 가능
- 격식체 보고 ("~로 판단됩니다", "~를 권고드립니다")

## 라이선스

MIT
