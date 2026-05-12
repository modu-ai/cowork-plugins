---
name: executive-summary
description: |
  [책임 경계] 임원/이사회 1페이지 요약 (≤500단어, McKinsey Pyramid — What/So What/Now What 구조).
  페어 moai-marketing:performance-report와 체이닝 관계 — 본 스킬은 임원 압축 요약, 페어는 마케팅 풀 리포트(전체).
  입력 가능: performance-report 출력 · moai-finance (financial-statements, variance-analysis) · moai-pm:weekly-report · 외부 보고서.
  복잡한 분석·재무·운영 보고를 경영진 1페이지(≤500단어) 요약으로 변환합니다.
  Bezos 6-Pager 아닌 한국 임원/이사회 표준에 맞춘 What/So What/Now What 구조,
  K-IFRS 재무 지표 우선, 정량 수치 + 의사결정 옵션 + 권고안.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "경영진 보고", "이사회 자료", "임원 1pager"
  - "C레벨 요약", "executive summary 작성", "임원 보고서 요약"
  - "긴 보고서 1페이지로 줄여줘", "경영진용 핵심 요약"
user-invocable: true
version: 2.3.0
---

# Executive Summary — 경영진 1페이지 요약

> moai-bi | What / So What / Now What 3-축 구조

## 개요

10-50페이지짜리 분석·재무·운영 보고서를 C-level이 5분 안에 의사결정할 수 있는 1페이지로 변환합니다. moai-finance(financial-statements, variance-analysis), moai-pm(weekly-report), 외부 보고서 모두 입력 가능합니다.

핵심 원칙: **결론부터** (McKinsey Pyramid). 근거는 그 다음, 데이터는 부록.

## 트리거 키워드

경영진 보고 이사회 자료 임원 1pager C레벨 요약 executive summary 임원 보고서 1페이지 요약 경영 핵심 요약

## 워크플로우

### 1단계: 입력 자료 분석

다음 중 하나 이상:
- 원본 보고서 (PDF/Markdown/DOCX) — 10-50p
- 재무제표 + 변동분석 결과 (`moai-finance` 출력)
- 주간/월간 운영 보고 (`moai-pm/weekly-report` 출력)
- 외부 분석 (시장조사·컨설팅 보고서)

### 2단계: 6섹션 1pager 구조

| # | 섹션 | 분량 | 내용 |
|---|---|---|---|
| 1 | 헤드라인 | 1줄 | 가장 중요한 한 메시지 (의사결정 핵심) |
| 2 | What | 3 bullet | 무슨 일이 일어났나 (정량) |
| 3 | So What | 3 bullet | 사업 임팩트 (원·% 단위) |
| 4 | Now What | 2-3 옵션 + 권고 1개 | 의사결정 옵션과 권고안 |
| 5 | Risks | 1-2 bullet | 핵심 리스크 |
| 6 | Next Review | 1줄 | 다음 리뷰 시점·지표 |

전체 ≤ 500단어. 자동 글자수 검증.

### 3단계: K-IFRS 재무 지표 우선

재무 보고 압축 시 다음 지표 우선 노출:

- 매출 / 영업이익 / 영업이익률
- EBITDA / EBITDA 마진
- CAGR (3년 / 5년)
- 운전자본 / 부채비율 / 유동비율
- 핵심 사업부 별 기여도

비재무 지표:
- North Star (회사 핵심)
- 활성 고객·이탈률·LTV/CAC

### 4단계: 의사결정 옵션 작성 (Now What)

각 옵션은 다음 형식:

```
옵션 A: [의사결정 항목]
  - 기대 효과: ...
  - 비용·리스크: ...
  - 결정 시한: P0/P1/P2 (시간 추정 금지)

권고: 옵션 X — 근거: ...
```

권고 없는 옵션 나열은 금지 (경영진 판단 부담 증가).

### 5단계: 톤·서식

- 격식체 ("~로 판단됩니다", "~를 권고드립니다")
- 정량 수치 강조 (굵은 글씨)
- 모든 수치에 출처 인라인 표기 또는 [추정] 태그
- 색깔 신호 활용 시 (Green/Yellow/Red) — 이유 한 줄 명시

## 출력 형식

```markdown
# Executive Summary — [주제] (2026-05-01)

> 헤드라인: 결제 모듈 v2 도입으로 분기 매출 +8% 가속, 보안 감사 대응이 핵심 의사결정.

## What (지난 N주/분기)
- **매출 124억** (전기 대비 +8.1%, K-IFRS 기준 [DART 공시 인용])
- 결제 성공률 **94.2%** (직전 90.5%, 결제 v2 효과)
- 신규 고객 **320사** (목표 300사 대비 +6.7%)

## So What (사업 임팩트)
- 영업이익률 **18.2%** (직전 16.8%, +1.4pp) — 인건비 안정화
- LTV/CAC **3.6** (1년 전 2.9) — 건전 구조 강화
- 분기 EBITDA **22억** ([추정] 잠정치, 결산 후 확정)

## Now What (의사결정 옵션)

**옵션 A: 보안 감사 대응 — 외주 인력 채용**
  - 기대 효과: 6주 내 ISMS 인증 갱신
  - 비용: 8천만원 (분기 영업이익 -3.6%)
  - 시한: P0

**옵션 B: 내부 재배치**
  - 기대 효과: 8주 내 갱신
  - 비용: 인건비 무영향, 기능 출시 1건 지연
  - 시한: P0

**권고: 옵션 A** — 기능 출시 일정과 분리, 분기 매출 모멘텀 보존

## Risks
- ⚠️ SMS API 외부 의존성 지연 → 결제 흐름 영향 가능

## Next Review
- W20 (2주 후), KPI: 결제 성공률·보안 감사 진행률
```

## 사용 예시

**예시 1 — 변동분석 → 임원 1pager**
```
사용자: "이번 분기 변동분석 보고서를 임원 1pager로 만들어줘."
→ moai-finance/variance-analysis 결과 입력
→ executive-summary가 K-IFRS 지표 우선 + What/So What/Now What 출력
→ 후속: moai-office/pptx-designer로 슬라이드 1매
```

**예시 2 — 주간 → C-level**
```
사용자: "이번 주 weekly-report를 더 압축해서 C레벨 보고로."
→ 6섹션 주간보고 → 1pager 6섹션으로 재구조화
→ 의사결정 요청을 옵션 + 권고 형식으로 명시화
```

## 주의사항

- **500단어 한도 강제**: 초과 시 자동 압축 또는 사용자에게 우선순위 선택 요청
- **권고 없는 옵션 금지**: Now What은 반드시 권고안 1개 포함
- **시간 추정 금지**: "1주 후 완료", "3개월 내" 등은 priority labels (P0/P1/P2)로 변환
- **수치 출처 강제**: 모든 정량 데이터는 출처 인라인 명시 또는 `[추정]` 태그
- **헤드라인 의무**: 1줄 헤드라인 없으면 출력 차단 (경영진 5초 룰)

## 관련 스킬

**Before (입력 prep)**:
- `moai-finance/financial-statements` — 재무제표
- `moai-finance/variance-analysis` — 변동분석
- `moai-pm/weekly-report` — 주간보고
- (외부 보고서)

**After (출력 후처리)**:
- `moai-office/pptx-designer` — 이사회 슬라이드 1매
- `moai-office/docx-generator` — PDF 1pager
- `moai-core/ai-slop-reviewer` — 격식체·정량 출처 검수

**Alternative**:
- `moai-pm/weekly-report` — 팀 단위 주간 (1pager 아닌 6섹션)
- `moai-business/strategy-planner` — 전략 문서 (요약 아닌 본문)

## 관련 커맨드

- (CLAUDE.local.md §3-3 등록 체인)
  - 재무 → 경영진 보고: `variance-analysis → executive-summary → pptx-designer`
  - 주간 → C-level: `weekly-report → executive-summary`

## 출처

- McKinsey Pyramid Principle — 결론 → 근거 → 데이터
- Amazon 6-Pager — Bezos narrative 원칙 (참고, 본 스킬은 1-Pager 변형)
- [Mordor Intelligence — 한국 B2B SaaS 2026-2031](https://www.mordorintelligence.kr/industry-reports/b2b-saas-market) — 시장 데이터 인용 시
- K-IFRS 한국채택국제회계기준 — 재무 지표 표기
- 일반 BI 베스트 프랙티스 (Stephen Few, Edward Tufte) — 1pager 시각 디자인