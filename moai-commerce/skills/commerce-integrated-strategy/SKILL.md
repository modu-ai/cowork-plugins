---
name: commerce-integrated-strategy
description: |
  [책임 경계] Day 2 산출물 ⑤~⑩ 전체를 종합하여 매출 향상 통합 전략 1장 + 실행 우선순위 Top 3 자동 생성. 페어 스킬 moai-research:strategy-planner와 명확히 구분 — 본 스킬은 이커머스 셀러 즉시 실행 전술(당일 데이터 기반), 페어는 중장기 사업 전략.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "오늘 배운 것 종합 전략으로 정리해줘", "통합 전략 뽑아줘", "실행 우선순위 정해줘", "매출 올리는 전략 1장", "지금 당장 해야 할 것 Top3", "ROAS 개선 전략", "채널별 매출 비교 분석", "오늘 모닝브리핑 요약"
  V6 ⑥ 통합 전략 도구 = MCP dashboard_morning_brief · sales_compare_channels · ad_roas_summary 3종 wrapper. (SPEC-COMMERCE-V6-003 §5.3 인용)
  ai-slop-reviewer 자동 체이닝 (전략 문서 텍스트 산출물).
user-invocable: true
version: 2.3.0
---

# 통합 전략 자동 생성 (Commerce Integrated Strategy)

## 개요

Day 2에서 생성한 산출물 ⑤(시장조사)~⑩(채널 메시지) 전체와 실시간 대시보드 데이터를 종합하여 이커머스 셀러가 즉시 실행 가능한 매출 향상 통합 전략 1장을 자동 생성하는 스킬입니다.

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3):
- `dashboard_morning_brief` — 오늘 주요 지표 요약 (매출·방문·전환)
- `sales_compare_channels` — 채널별 매출 비교 분석
- `ad_roas_summary` — 광고 채널별 ROAS 요약

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 위 3종 도구를 호출합니다. MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

**Day 2 시연 시점**: 7교시 (최종 통합 실습)

## 트리거 키워드

통합 전략, 실행 우선순위, 매출 향상 전략, Top 3 액션, 종합 리포트, 모닝 브리핑, 채널 매출 비교, ROAS 분석, 오늘 할 일, 이커머스 전략 1장, Day2 결산, 산출물 종합

## 워크플로우

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑤ 시장조사 결과 | 필수 | commerce-market-research 산출물 |
| ⑥ JTBD 9개 | 필수 | commerce-jtbd-persona --mode jtbd 산출물 |
| ⑦ 페르소나 3명 | 권장 | commerce-jtbd-persona --mode persona 산출물 |
| ⑧ 상세페이지 카피 | 선택 | detail-page-copy 산출물 |
| ⑨ 상품명 3안 | 권장 | commerce-product-naming 산출물 |
| ⑩ 채널 메시지 15종 | 필수 | commerce-channel-message 산출물 |

### MCP 호출 순서

```
1. dashboard_morning_brief()
   → 오늘 주요 지표: 매출, 방문자, 전환율, 장바구니 이탈

2. sales_compare_channels(period="today")
   → 채널별 매출 비교: 스마트스토어 vs 쿠팡 vs 자사몰

3. ad_roas_summary(period="today", channels=["naver", "kakao", "meta"])
   → 광고 채널별 ROAS + 개선 기회

4. 종합 분석:
   Day2 산출물 ⑤~⑩ + 실시간 데이터 교차 → 우선순위 Top 3 선정
```

### ai-slop-reviewer 자동 체이닝 (HARD)

전략 1장 생성 직후 `moai-core:ai-slop-reviewer`를 자동 체인합니다.

검수 항목:
- 전략 문서 AI 패턴 제거 ("시너지", "혁신적 접근" 등 클리셰)
- 구체 수치·실행 근거 없는 추상 전략 문구 수정
- 실행 가능한 한국 이커머스 셀러 언어로 조정

---

## 사용 예시

```
"/commerce-integrated-strategy — Day2 산출물 전체 첨부"
→ 오늘 매출 현황 + 채널 비교 + ROAS + ⑤~⑩ 종합
   실행 우선순위 Top 3: 1) 검색 키워드 조정 2) CRM 발송 3) 상품명 변경
   → ai-slop-reviewer 자동 검수 후 최종 전략 1장 출력

"/commerce-integrated-strategy Top3 지금 당장 해야 할 것만"
→ 간소화 모드: 실행 우선순위 Top 3 + 각 실행 방법 1줄씩
```

## 출력 형식

```markdown
# 📈 {상품명} 통합 전략 1장

**생성일**: {날짜} | **기준 데이터**: Day2 산출물 ⑤~⑩ + 실시간 대시보드

---

## 오늘의 현황 요약 (대시보드)

| 지표 | 오늘 | 전일 대비 | 평가 |
|------|------|----------|------|
| 매출 | {금액} | +/-{%} | ↑/↓ |
| 방문자 | {명} | +/-{%} | ↑/↓ |
| 전환율 | {%} | +/-{%} | ↑/↓ |
| ROAS (전체) | {배수} | — | 양호/개선필요 |

## 채널별 매출 비교

| 채널 | 매출 | 점유율 | ROAS |
|------|------|--------|------|
| 스마트스토어 | — | —% | — |
| 쿠팡 | — | —% | — |
| 자사몰 | — | —% | — |

---

## Day2 산출물 종합 분석

### ⑤ 시장조사 핵심 시사점
- 기회: {⑤에서 식별한 기회}
- 위협: {⑤에서 식별한 위협}

### ⑥⑦ JTBD·페르소나 핵심 인사이트
- 메인 구매 동기: {F1/E1/S1}
- 메인 페르소나 구매결정요인: {구매결정요인 Top 3}

### ⑨ 상품명 권장안
- 확정 권장: {검색형/CTR형/브랜드형} — {이유}

### ⑩ 채널 메시지 즉시 적용 우선순위
- 1순위: {채널} — {이유}
- 2순위: {채널} — {이유}

---

## 🎯 실행 우선순위 Top 3

### #1 {실행 항목} — 즉시 실행 가능
**What**: {구체 실행 내용}
**Why**: {데이터 근거}
**How**: {실행 방법 1줄}

### #2 {실행 항목} — 이번 주 내
**What**: {구체 실행 내용}
**Why**: {데이터 근거}
**How**: {실행 방법 1줄}

### #3 {실행 항목} — 이번 달 내
**What**: {구체 실행 내용}
**Why**: {데이터 근거}
**How**: {실행 방법 1줄}

---

> ai-slop-reviewer 검수 완료 | 변경 {N}건
```

## 합격 기준

PDF §5.5 ⑪ 합격 기준:

- **오늘의 모든 산출물 요약**: ⑤~⑩ 핵심 인사이트 각각 1줄 이상
- **실시간 데이터 반영**: 대시보드 수치 포함 (MCP 데이터 또는 대체 시연 데이터)
- **실행 우선순위 Top 3**: 구체 실행 내용 + 데이터 근거 + 실행 방법
- **ai-slop-reviewer 검수 흔적**: 마지막 줄에 검수 완료 표기

## 관련 스킬

체이닝 순서: `commerce-channel-message` → **commerce-integrated-strategy** (Day 2 최종)

- `commerce-market-research` — ⑤ 시장조사 (입력)
- `commerce-jtbd-persona` — ⑥⑦ JTBD+페르소나 (입력)
- `detail-page-copy` — ⑧ 상세페이지 카피 (입력)
- `commerce-product-naming` — ⑨ 상품명 (입력)
- `commerce-channel-message` — ⑩ 채널 메시지 (입력, 이전 단계)
- `moai-core:ai-slop-reviewer` — 전략 문서 AI 검수 (자동 체인)

## 이 스킬을 사용하지 말아야 할 때

- **중장기 사업 전략 (분기·연간)**: `moai-research:strategy-planner` 사용
- **IR 덱·투자 유치 전략**: `moai-office:pptx-designer` + 별도 사업기획 스킬 사용
- **광고 캠페인 집행 계획**: 광고 플랫폼 직접 관리 (본 캠프 외 영역, PDF §1.3)
- **특정 스킬 단독 산출물만 필요**: 해당 스킬 직접 호출 (통합 불필요)
