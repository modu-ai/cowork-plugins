---
title: "moai-finance — 세무·결산·K-IFRS"
weight: 130
description: "3.3% 원천징수·부가세·홈택스·K-IFRS·예실 분석을 다루는 한국 세무·회계 4개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-finance"]
---

# moai-finance

> 한국 세법·회계 기준 4개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-finance` (v1.5.0)는 프리랜서 3.3% 원천징수, 종합소득세·부가가치세 신고, 홈택스 절차, K-IFRS 재무상태표·손익계산서·현금흐름표 작성, 월·분기·연간 결산과 4대보험 정산, 예산 대비 실적 분석까지 한국 기준 재무·세무 실무를 자동화합니다. 2026년 K-IFRS 제1118호 변경사항과 4대보험 요율·노동법 최신값이 반영되어 있습니다.

## 설치

{{< tabs "install-finance" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-finance` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `tax-helper` | 3.3% 원천징수, 종합소득세, 부가가치세, 홈택스 절차 |
| `financial-statements` | K-IFRS 재무상태표·손익계산서·현금흐름표 |
| `close-management` | 월·분기·연간 결산, 4대보험 정산, 급여 마감 |
| `variance-analysis` | 예산 대비 실적, 매출·비용·이익 분산, KPI 추적 |

## 한국 기준 최신화

- **2026년 K-IFRS 제1118호** 변경사항 반영
- **4대보험 요율·노동법** 최신값
- 홈택스 신고 일정 자동 안내

## 대표 체인

**월말 결산**

```text
close-management → xlsx-creator(결산표) → docx-generator(결산 보고서)
```

**예실 분석 보고**

```text
variance-analysis → xlsx-creator → docx-generator → ai-slop-reviewer
```

## 빠른 사용 예

```text
프리랜서 3.3% 원천징수 영수증 12장 합계 계산해줘. 종합소득세 예상 세액도.
```

```text
이번 분기 재무상태표 K-IFRS 기준으로 엑셀로 만들어줘.
```

## 다음 단계

- [`moai-office`](../moai-office/) — 결산표·보고서 포맷
- [`moai-operations`](../moai-operations/) — 운영 지표 결합

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-finance 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)
