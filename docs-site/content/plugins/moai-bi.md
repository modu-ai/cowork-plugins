---
title: "moai-bi — BI 대시보드와 경영진 1pager"
weight: 90
description: "데이터 분석·BI 대시보드 설계·경영진 1pager 보고서 자동화. K-IFRS·KOSIS·DART 한국 통계 친화, moai-finance와 직접 체이닝됩니다."
geekdocBreadcrumb: true
tags: ["moai-bi"]
---

# moai-bi

> 경영진·이사회·투자자에게 보낼 1페이지 요약을 자동 생성하는 BI 플러그인입니다. 긴 분석·재무 보고를 What / So What / Now What 3-축 구조로 압축합니다.

## 무엇을 하는 플러그인인가

`moai-bi` (v1.8.0)는 한국 임원·이사회 표준에 맞춘 BI 자동화 플러그인입니다.

- **경영진 1pager**: 복잡한 분석·재무·운영 보고를 ≤500단어 1페이지로 변환
- **What / So What / Now What** 3-축 구조: 단순 요약이 아닌 **의사결정 옵션 + 권고안** 포함
- **K-IFRS 재무 지표 우선**: 매출·영업이익률·EBITDA·운전자본 등 한국 회계 기준
- **한국 통계 친화**: KOSIS·DART·공공데이터포털 데이터 직접 인용 가능

향후 KPI 트리, 코호트·퍼널 분석, BI 대시보드 설계, 변동분석(variance analysis) 스킬이 추가될 예정입니다 (v1.9.x 이후 로드맵).

## 설치

{{< tabs "install-bi" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-bi` 옆의 **+** 버튼을 눌러 설치합니다.
2. 재무 데이터를 자동 인용하려면 `moai-finance`도 함께 설치하면 체이닝이 매끄러워집니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-bi)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (1개 + 로드맵)

| 스킬 | 용도 | 대표 출력 |
|---|---|---|
| `executive-summary` | 경영진 1페이지 요약 자동 생성 | What/So What/Now What 3-축, 정량 수치 + 권고안 |

향후 추가 예정 (로드맵): `kpi-tree` · `cohort-analysis` · `funnel-analysis` · `dashboard-spec` · `variance-analysis`.

## 대표 체인

**긴 분석 보고서 → 경영진 1pager**

```text
(원본 분석 보고서) → executive-summary → docx-generator → ai-slop-reviewer
```

**재무 변동분석 → 이사회 자료**

```text
moai-finance:variance-analysis → executive-summary → pptx-designer → ai-slop-reviewer
```

**시장 조사 → 임원 보고**

```text
moai-business:market-analyst → executive-summary → docx-generator → ai-slop-reviewer
```

## 한국 임원 보고 특화

- **격식체 우선**: "~합니다" 종결, 이사회·감사 보고 어조에 맞춤
- **정량 우선**: 모든 주장에 수치·출처 결합 (서술형 형용사 최소화)
- **의사결정 옵션 명시**: A/B/C 옵션 + 각 옵션의 리스크·기대효과 요약
- **K-IFRS·DART**: 한국 회계 기준에 맞춘 재무 지표 표기

## 빠른 사용 예

```text
지난 분기 마케팅 성과 보고서(20페이지)를 임원용 1pager로 줄여줘.
- 형식: What/So What/Now What
- 종결: 격식체
- 핵심 수치 5개 + 의사결정 옵션 3가지 + 권고안
- 저장: 90_Output/exec-summary-Q1.docx
```

```text
> DART 공시한 우리 회사 분기 보고서를 이사회용 1페이지 자료로 만들어줘.
K-IFRS 기준 매출·영업이익률·운전자본 변동 강조.
```

## 다음 단계

- [`moai-finance`](../moai-finance/) — K-IFRS·세무 데이터 소스
- [`moai-business`](../moai-business/) — 시장조사·전략 보고서 체이닝
- [`moai-data`](../moai-data/) — CSV/Excel 데이터 분석 + 차트
- [`moai-pm`](../moai-pm/) — 주간보고 자동화

---

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [moai-bi 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-bi)
- KOSIS 국가통계포털, DART 전자공시시스템
