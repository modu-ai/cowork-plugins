---
title: "재무 모델링 템플릿"
weight: 20
description: "3년 P&L · cash-flow · cohort · funding need 5개 시트 표준 재무 모델 템플릿."
geekdocBreadcrumb: true
---

# 재무 모델링 템플릿

> 투자 검토에서 통하는 재무 모델은 *복잡함이 아니라 검증 가능함*에서 신뢰를 얻습니다. 5개 시트, 가정과 결과의 명확한 분리, 가정을 바꾸면 결과가 자동으로 따라가는 구조 — 이 셋이면 충분합니다.

## 사용 스킬

| 스킬 | 역할 |
|---|---|
| `moai-finance:financial-statements` | K-IFRS 기준 재무상태표·손익계산서·현금흐름표 |
| `moai-finance:variance-analysis` | 예산 대비 실적 분산 분석 |
| `moai-finance:close-management` | 결산·급여 정산 |
| `moai-office:xlsx-creator` | 5개 시트 통합 모델 출력 |

## 5개 시트 표준 구조

### Sheet 1 — Assumptions

모든 가정 단가·증가율·전환율을 한 시트에 모읍니다. 다른 시트는 이 시트만 참조.

| 항목 | 단위 | 값 | 비고 |
|---|---|---|---|
| 평균 단가 (ARPU) | KRW | 50,000 | 월별 |
| 신규 고객 증가율 | % | 15 | 월별 MoM |
| Churn | % | 5 | 월별 |
| CAC | KRW | 80,000 | 마케팅·세일즈 합계 |
| 평균 인건비 | KRW | 5,500,000 | 월 1인당 |

### Sheet 2 — P&L (월별 36개월)

매출 → COGS → 매출총이익 → OpEx → EBITDA → 순이익. 모든 셀은 Sheet 1을 참조.

### Sheet 3 — Cash flow

영업·투자·재무 활동 3분류. 누적 현금잔고가 음수로 빠지지 않는지 확인.

### Sheet 4 — Cohort

월 가입 코호트별 누적 매출 + 리텐션. LTV 계산 근거.

### Sheet 5 — Funding need

자금 소요 + 사용 계획. 라운드별 (Pre-seed · Seed · Series A) 누적.

## 워크플로우 예시 — 36개월 모델 자동 생성

```
> "시리즈 A 투자 검토용 재무 모델 만들어줘. 36개월, 5개 시트(Assumptions/P&L/Cash/Cohort/Funding). 가정은 다음과 같음 — ARPU 50,000원, 신규 MoM 15%, Churn 5%, CAC 80,000원. xlsx 한 파일로 저장."
```

체인: `financial-statements` → `xlsx-creator`

## 가정 변경 테스트

투자자가 "Churn 7%로 가정하면?" 같은 질문을 던졌을 때 5초 안에 답할 수 있어야 합니다.

```
> "방금 만든 모델의 Assumptions 시트에서 Churn을 7%로 바꿔 결과 비교해줘. 기존(5%) vs 변경(7%) 상태에서 24개월 매출과 EBITDA를 표로 정리."
```

## K-IFRS 결산 보고

스타트업이 시리즈 A 이후 결산 보고서가 필수가 되면:

```
> "2026년 K-IFRS 기준 재무제표 만들어줘. 손익계산서·재무상태표·현금흐름표 풀 세트. 1년치 거래 데이터는 첨부 엑셀에."
```

## 자주 겪는 실수

- **Assumptions 시트를 만들지 않고 P&L에 숫자 직접 입력** — 가정 변경 시 일일이 고쳐야 합니다.
- **차트가 너무 많음** — 핵심 차트 3개만(매출 곡선, 현금잔고, 코호트). 나머지는 표.
- **연간 모델만 작성** — 시리즈 A에서는 월별 36개월이 표준입니다.

## 다음 단계

- [투자 유치 가이드](../../guides/funding/)
- [엑셀 고급 기법](../excel/)
- [트랙 — 재무](../../tracks/track-finance/)

---

### Sources

- moai-finance 플러그인 [`financial-statements`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-finance/skills/financial-statements/SKILL.md), [`variance-analysis`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-finance/skills/variance-analysis/SKILL.md)
- moai-office 플러그인 [`xlsx-creator`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-office/skills/xlsx-creator/SKILL.md)
