---
name: commerce-channel-message
description: |
  [책임 경계] NCM 프레임워크(Need→Channel→Moment→Message→CTA) 기반 검색·광고·CRM 채널별 메시지 15종 자동 생성. 페어 스킬 moai-domain-copywriting과 명확히 구분 — 본 스킬은 채널 분기 메시지(채널별 다른 표현), 페어는 단일 목적 광고 카피.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "채널별 메시지 만들어줘", "검색광고 카피 15종", "CRM 메시지 뽑아줘", "채널 메시지 분기", "스마트스토어 배너 카피", "쿠팡 광고 문구", "카카오 알림톡 문구", "SNS 광고 카피 5종", "NCM 프레임워크 적용"
  V6 ⑤ 채널별 메시지 도구 = MCP keyword_seasonal_calendar · ad_keyword_performance 2종 wrapper. (SPEC-COMMERCE-V6-003 §5.3 인용)
  ai-slop-reviewer 자동 체이닝 (텍스트 메시지 15종 산출물).
user-invocable: true
version: 2.3.0
---

# 채널별 메시지 자동 생성 (Commerce Channel Message)

## 개요

JTBD와 페르소나를 기반으로 NCM 프레임워크(Need → Channel → Moment → Message → CTA)에 따라 검색·광고·CRM 3개 채널 × 5종 = 총 15종 메시지를 채널별 다른 표현으로 자동 생성하는 스킬입니다.

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3):
- `keyword_seasonal_calendar` — 계절·시즌별 키워드 캘린더 (Moment 결정)
- `ad_keyword_performance` — 광고 키워드 성과 데이터 (CTA 최적화)

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 위 2종 도구를 호출합니다. MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

**Day 2 시연 시점**: 6교시 16:10–16:55

## 트리거 키워드

채널 메시지, NCM 프레임워크, 검색광고 카피, 배너 광고 문구, CRM 메시지, 카카오 알림톡, 이메일 제목, SNS 광고 카피, 채널별 문구, 광고 카피 분기, 시즌 메시지, 고객 접점 메시지, 15종 카피

## NCM 프레임워크

| 단계 | 설명 | 입력 소스 |
|------|------|----------|
| **N** — Need | 고객의 핵심 니즈 정의 | ⑥ JTBD 9개 |
| **C** — Channel | 메시지 전달 채널 선택 | 우선 채널 입력 |
| **M** — Moment | 최적 접촉 시점 | MCP keyword_seasonal_calendar |
| **M** — Message | 채널별 맞춤 메시지 작성 | JTBD + 페르소나 |
| **CTA** | 채널별 행동 유도 문구 | MCP ad_keyword_performance |

**핵심 제약 (REQ-V6-013 HARD)**: 같은 니즈라도 채널별 반드시 다른 표현으로 분기.

---

## 워크플로우

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑥ JTBD 결과 | 필수 | commerce-jtbd-persona --mode jtbd 산출물 |
| ⑦ 페르소나 | 권장 | commerce-jtbd-persona --mode persona 산출물 |
| 우선 채널 | 필수 | 검색광고, 배너광고, CRM (최소 1개 선택) |
| 시즌/시기 | 선택 | "봄 시즌", "연말 프로모션" (기본값: 현재 월) |

### MCP 호출 순서

```
1. keyword_seasonal_calendar(category, current_month)
   → 현재 시즌 핵심 키워드 + 접촉 최적 시점

2. ad_keyword_performance(product_keywords[], channel)
   → 채널별 광고 키워드 성과 → CTA 문구 최적화 힌트

3. NCM 매핑:
   [N] JTBD 우선순위 1위 니즈 선정
   [C] 채널 3개 분류: 검색(네이버/쿠팡) / 광고(배너/SNS) / CRM(카카오/이메일/SMS)
   [M] seasonal_calendar 기반 최적 시점 설정
   [M] 채널별 다른 표현으로 메시지 5종씩 작성
   [CTA] ad_keyword_performance 기반 채널별 CTA 최적화
```

### ai-slop-reviewer 자동 체이닝 (HARD)

메시지 15종 생성 직후 `moai-core:ai-slop-reviewer`를 자동 체인합니다.

검수 항목:
- AI 패턴 메시지 ("혁신적인", "놀라운", "최고의" 클리셰) 제거
- 채널별 자연스러운 어체 맞춤 (검색: 키워드형 / CRM: 대화형 / SNS: 임팩트형)
- 실제 이커머스 광고 어체로 조정

---

## 사용 예시

```
"/commerce-channel-message 비건 스킨케어, JTBD+페르소나 첨부, 검색+CRM 우선"
→ 검색광고 5종: 키워드 기반 헤드라인
   배너광고 5종: 비주얼 후킹 메시지
   CRM 5종: 카카오/이메일/SMS 맞춤 문구
   → ai-slop-reviewer 자동 검수

"/commerce-channel-message 반려견 관절 간식, 봄 시즌, 쿠팡 광고 우선"
→ 시즌 키워드 캘린더 반영 + 15종 분기 메시지
```

## 출력 형식

```json
{
  "product": "{상품명}",
  "season_moment": "{현재 시즌 + 최적 접촉 시점}",
  "ncm_framework": {
    "need": "{핵심 니즈 1줄}",
    "channels": ["검색", "광고", "CRM"],
    "moment": "{최적 접촉 시점}"
  },
  "messages": {
    "search": [
      {
        "id": "S1", "channel": "네이버 검색광고",
        "headline": "메시지 제목 (15자 이내)",
        "description": "설명 문구 (45자 이내)",
        "cta": "CTA 문구",
        "keyword_trigger": "타겟 키워드"
      },
      {"id": "S2", "channel": "쿠팡 검색광고", "...": "..."},
      {"id": "S3", "channel": "네이버쇼핑 검색", "...": "..."},
      {"id": "S4", "channel": "카카오 검색", "...": "..."},
      {"id": "S5", "channel": "구글 검색광고", "...": "..."}
    ],
    "ad": [
      {"id": "A1", "channel": "인스타그램 배너", "headline": "...", "body": "...", "cta": "..."},
      {"id": "A2", "channel": "페이스북 배너", "...": "..."},
      {"id": "A3", "channel": "카카오 배너", "...": "..."},
      {"id": "A4", "channel": "유튜브 인피드", "...": "..."},
      {"id": "A5", "channel": "스마트스토어 배너", "...": "..."}
    ],
    "crm": [
      {"id": "C1", "channel": "카카오 알림톡", "message": "...", "cta": "..."},
      {"id": "C2", "channel": "이메일 제목", "subject": "...", "preview": "..."},
      {"id": "C3", "channel": "SMS", "message": "...(90자 이내)"},
      {"id": "C4", "channel": "카카오 친구톡", "...": "..."},
      {"id": "C5", "channel": "앱 푸시", "title": "...", "body": "..."}
    ]
  },
  "channel_differentiation_check": "PASS — 3채널 표현 상이 확인",
  "slop_review": {
    "status": "passed",
    "changes_made": 2,
    "notes": "ai-slop-reviewer 검수: '놀라운 효과' → '피부과 내원 전에' 수정"
  }
}
```

## 합격 기준

PDF §5.5 ⑩ 합격 기준:

- **15종 완성**: 검색·광고·CRM 각 5종씩 총 15종
- **채널별 다른 표현**: 같은 니즈가 채널별 다른 방식으로 분기 (REQ-V6-013)
- **ai-slop-reviewer 검수 흔적**: slop_review 블록 포함
- **CTA 포함**: 각 메시지에 채널 특성에 맞는 행동 유도 문구

## 관련 스킬

체이닝 순서: `commerce-jtbd-persona --mode persona` → **commerce-channel-message** → `commerce-integrated-strategy`

- `commerce-jtbd-persona` — ⑥⑦ JTBD+페르소나 (이전 단계, Need 정의 입력)
- `commerce-product-naming` — ⑨ 확정 상품명 (메시지 내 상품명 활용)
- `commerce-integrated-strategy` — 채널 메시지 포함 전략 1장 종합 (다음 단계)
- `moai-content:social-media` — SNS 콘텐츠 단독 심화 작업

## 이 스킬을 사용하지 말아야 할 때

- **단일 채널 광고 카피만 필요**: `moai-domain-copywriting` 사용
- **상세페이지 카피**: `detail-page-copy` 사용
- **이메일 뉴스레터 본문**: `moai-content:blog` 또는 `moai-content:email` 사용
- **광고 실집행·캠페인 운영**: 광고 플랫폼 직접 관리 (본 캠프 외 영역, PDF §1.3)
