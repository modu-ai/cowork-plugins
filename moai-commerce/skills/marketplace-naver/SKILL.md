---
name: marketplace-naver
description: >
  네이버 스마트스토어 + 11번가/G마켓/옥션 오픈마켓 정책·검색최적화 가이드 스킬입니다.
  "스마트스토어 등록", "네이버 쇼핑 SEO", "11번가 가이드", "옥션 등록", "오픈마켓 가이드"처럼 말하면 됩니다.
  detail-page-copy/detail-page-image 출력물을 4개 오픈마켓(네이버 스마트스토어 + 11번가 + G마켓 + 옥션) 정책에 맞게 검토하고,
  채널별 이미지 규격·검색태그·금지문구·톡톡 카피·후기 운영 가이드를 제공합니다.
user-invocable: true
version: 2.3.0
---

# 네이버 스마트스토어 + 오픈마켓 가이드

## 개요

네이버 스마트스토어와 11번가·G마켓·옥션 한국 주요 4개 오픈마켓의
공통/채널별 정책을 적용하는 가이드 스킬입니다.

> **중요**: 티몬·위메프는 큐텐(Qoo10) 인수 후 2024년 미정산 사태로 회생절차에 진입하여
> 본 가이드 대상에서 제외되었습니다. 인터파크커머스 등 후속 채널 동향은 별도 채널 가이드 추가 시 반영됩니다.

## 트리거 키워드

스마트스토어, 네이버 스마트스토어, 네이버 쇼핑, 톡톡, 11번가, G마켓, 옥션,
오픈마켓, 네이버 쇼핑 SEO, 스마트스토어 등록, 네이버 페이

## 워크플로우

### 1단계: 채널 확인

판매 채널 식별:
- **네이버 스마트스토어**: 검색·노출 강점, 톡톡 운영 필수
- **11번가**: 모바일 강점, 십일절 등 시즌 이벤트 활용
- **G마켓 / 옥션**: 동일 운영(이베이 코리아), 통합 등록 가능

### 2단계: 채널별 정책 적용

상세 가이드:
- 스마트스토어: `references/naver-smartstore.md`
- 오픈마켓 공통: `references/openmarket-common.md`

### 3단계: 검색 최적화

#### 네이버 쇼핑 SEO 핵심
- 상품명: 50자 이내, 핵심 키워드 앞쪽
- 카테고리 정확 선택 (검색 가중치 큼)
- 태그: 10~20개
- 후기 30건+ 4.5점+ 시 검색 우대

#### 오픈마켓 공통
- 11번가: "11번가 BEST", "오늘만 할인" 등 시즌 키워드 효과
- G마켓/옥션: "G마켓 단독", "옥션 G마켓 통합" 활용
- 통합 검색 시: 가격순 노출 비중이 큼 → 가격경쟁력 점검

### 4단계: 톡톡 카피 (스마트스토어 한정)

스마트스토어는 톡톡(채팅) 응대 카피가 중요합니다:
- 자동응답 메시지: 영업시간/배송/반품 정책
- FAQ 응답 템플릿
- 친근하지만 전문적인 톤 (반말 X, 과도한 이모지 X)

### 5단계: 후기 운영 가이드

- 후기 작성 유도 (포토 후기 100~500원 적립)
- 1~2점 후기 24시간 이내 응대
- 후기 조작 절대 금지 (네이버는 매우 엄격, 적발 시 영구 정지)

## 출력 형식

```json
{
  "channels": ["naver_smartstore", "11st", "gmarket"],
  "title_optimized": "50자 이내 상품명",
  "category_paths": {
    "naver_smartstore": "디지털/가전 > 음향가전 > 이어폰",
    "11st": "디지털/가전 > 이어폰/헤드폰",
    "gmarket": "디지털/가전 > 이어폰"
  },
  "search_tags": ["태그1", "태그2", "..."],
  "image_specs": {
    "naver_smartstore": "860~1000px 권장",
    "11st": "700~860px",
    "gmarket": "750~900px"
  },
  "talk_talk_template": {
    "greeting": "안녕하세요...",
    "out_of_hours": "영업시간 외 메시지",
    "shipping_inquiry": "...",
    "return_policy": "..."
  },
  "forbidden_phrases_found": [],
  "channel_specific_warnings": []
}
```

## 사용 예시

- "스마트스토어에 비건 화장품 등록 가이드 부탁해"
- "11번가 + G마켓 동시 등록할 건데 차이점 정리해줘"
- "네이버 쇼핑 검색 태그 추천해줘 — 무선이어폰"
- "톡톡 자동응답 템플릿 만들어줘"

## 관련 스킬

- `moai-commerce:detail-page-copy` — 카피 생성
- `moai-commerce:detail-page-image` — 이미지 합성
- `moai-commerce:marketplace-coupang` — 쿠팡 비교
- `moai-marketing:seo-naver-kakao` — 네이버 SEO 일반
- `moai-marketing:campaign-planner` — 시즌 캠페인 기획

## 이 스킬을 사용하지 말아야 할 때

- 쿠팡 가이드: `marketplace-coupang` 사용
- 자사몰(Cafe24/Shopify): 별도 가이드 필요
- 카카오쇼핑톡: `moai-marketing` 플러그인

## 주의사항

각 채널의 정책은 수시로 업데이트됩니다. 본 가이드는 일반적 기준이며, 실제 등록 전
공식 가이드를 확인하세요:

- 네이버 스마트스토어: https://sell.smartstore.naver.com
- 11번가: https://soffice.11st.co.kr
- G마켓/옥션 ESM PLUS: https://www.esmplus.com