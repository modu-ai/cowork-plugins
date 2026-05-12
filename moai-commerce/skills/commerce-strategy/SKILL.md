---
name: commerce-strategy
description: >
  한국 이커머스 통합 마케팅 전략을 설계하는 스킬입니다.
  "커머스 전략 짜줘", "채널 믹스 추천", "가격 전략", "프로모션 기획", "리텐션 전략", "이커머스 KPI"처럼 말하면 됩니다.
  채널 믹스(마켓플레이스+자사몰+큐레이션 비중 결정), 가격 전략, 프로모션 캘린더,
  재구매 리텐션 자동화, KPI 대시보드 설계까지 통합 가이드합니다.
  단계별(런칭/성장/안정) 전략 차이도 명시합니다.
user-invocable: true
version: 2.3.0
---

# 이커머스 통합 전략 (Commerce Strategy)

## 개요

이 스킬은 한국 이커머스 사업자가 **여러 채널을 어떻게 조합하고, 어떤 가격·프로모션·리텐션 전략으로 운영할지** 통합 설계합니다.
신생 브랜드 런칭부터 안정기 LTV 극대화까지 단계별로 다른 전략을 제공합니다.

## 트리거 키워드

이커머스 전략, 커머스 전략, 채널 믹스, 채널 전략, 가격 전략, 프로모션 캘린더,
리텐션, 재구매율, LTV, AOV, 이커머스 KPI, 광고 ROAS, CRM, 마케팅 자동화

## 워크플로우

### 1단계: 사업 단계 진단

| 단계 | 매출 규모 | 핵심 질문 |
|------|---------|---------|
| 런칭 (0~6개월) | 0~월 1천만 | 어디서 첫 매출? 트래픽 확보? |
| 성장 (6~24개월) | 월 1천~3억 | 채널 다각화? 광고 ROI? |
| 안정 (24개월+) | 월 3억+ | LTV·재구매? 브랜드 자산? |

### 2단계: 채널 믹스 결정

사업 단계 + 카테고리 + 자원에 맞춰 채널 비중을 정합니다. `references/channel-mix.md` 참조.

### 3단계: 가격 전략

`references/pricing.md` 참조. 핵심:
- 정가·할인가·프로모션가 3단계
- 채널별 가격 정책
- 가격 정합성 (마켓 간 가격차 허용 범위)

### 4단계: 프로모션 캘린더

`references/promotion.md` 참조. 한국 이커머스 시즌:
- 1월: 신년·설
- 5월: 가정의달
- 8월: 휴가
- 9~10월: 추석
- 11월 11일: 빼빼로데이·광군제·블프
- 12월: 크리스마스·연말

### 5단계: 리텐션 자동화

`references/retention.md` 참조. 핵심:
- 첫 구매 후 7일/14일/30일/60일 자동 트리거
- 적립금·등급제
- 이메일·알림톡 시퀀스

### 6단계: KPI 대시보드

`references/kpi.md` 참조. 핵심:
- 매주: 신규 가입·신규 구매·재구매·AOV·ROAS
- 매월: LTV·등급 분포·이메일 효율
- 분기: 채널별 매출 기여도, 반품률, NPS

## 출력 형식

```json
{
  "business_stage": "런칭 | 성장 | 안정",
  "channel_mix": {
    "마켓플레이스": "60%",
    "자사몰": "30%",
    "크라우드펀딩": "10%",
    "rationale": "런칭기 트래픽 확보를 위해 마켓 비중 높임"
  },
  "pricing": {
    "list_price": 149000,
    "discount_price": 119000,
    "promotion_price": 99000,
    "channel_policies": {
      "쿠팡": "정가 -20%",
      "스마트스토어": "정가 -15%",
      "자사몰": "정가 -10% + 적립금 5%"
    }
  },
  "promotion_calendar": [
    {"month": 5, "event": "가정의달", "discount": "20%", "channels": ["all"]},
    {"month": 11, "event": "빼빼로·블프", "discount": "30%", "channels": ["all"]},
    {"month": 12, "event": "크리스마스", "discount": "15%", "channels": ["자사몰"]}
  ],
  "retention_flow": [
    {"trigger": "첫 구매 +7d", "channel": "이메일", "content": "사용 가이드"},
    {"trigger": "첫 구매 +14d", "channel": "알림톡", "content": "후기 작성 적립"},
    {"trigger": "첫 구매 +30d", "channel": "이메일", "content": "재구매 쿠폰"},
    {"trigger": "첫 구매 +60d", "channel": "알림톡", "content": "추천 상품"}
  ],
  "kpi_targets": {
    "weekly": ["신규 가입", "전환율", "ROAS", "AOV"],
    "monthly": ["LTV(90d)", "재구매율(30d)", "이메일 오픈율"],
    "quarterly": ["채널별 매출 기여도", "반품률", "NPS"]
  },
  "ad_budget_allocation": {
    "naver_search": "40%",
    "meta_ads": "30%",
    "kakao_moment": "20%",
    "google_ads": "10%"
  }
}
```

## 사용 예시

- "신생 비건 화장품 브랜드 런칭 전략 짜줘"
- "월 1천만원 매출인데 채널 다각화 전략 추천"
- "광고비 월 500만원, 어떻게 분배할까?"
- "재구매율 어떻게 올릴까 — 현재 15%"
- "11월 빼빼로 + 블프 캠페인 기획"

## 관련 스킬

- `moai-commerce:commerce-copywriting` — 광고·이메일·푸시 카피
- `moai-commerce:detail-page-copy` — 상세페이지 카피
- `moai-commerce:marketplace-coupang/naver/d2c/curation/crowdfunding` — 채널별 운영
- `moai-marketing:campaign-planner` — 캠페인 기획
- `moai-marketing:performance-marketing` — 성과 마케팅 전반
- `moai-business:strategy-planner` — 사업 전략 (상위 레벨)

## 이 스킬을 사용하지 말아야 할 때

- 단일 채널 등록 가이드: `marketplace-*` 스킬 직접 사용
- 카피 작성: `commerce-copywriting` 또는 `detail-page-copy`
- 일반 사업 전략: `moai-business:strategy-planner`

## 주의사항

- 전략은 가설. 실제 운영 데이터로 매주 검증·조정 필요.
- 광고비는 **반드시 사업비 절반 이하**로 시작. 100% 광고에 의존하면 ROAS 폭락 시 즉사.
- 가격 인하 프로모션은 단발성으로. 지속적 할인은 브랜드 가치 훼손.