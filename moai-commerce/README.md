# moai-commerce

> 한국 이커머스 풀세트 자동화 플러그인 — 상세페이지 카피·이미지·사진 + 채널 가이드 8종 + 통합 마케팅 전략·카피·라이브 커머스

## 개요

`moai-commerce`는 한국 이커머스 사업자를 위한 풀 사이클 자동화 플러그인입니다.
상품 사진과 핵심 정보를 제공하면 **13섹션 감정여정 상세페이지**부터 **채널별 입점·운영 가이드**, **마케팅 전략·카피**, **라이브 커머스 진행 스크립트**까지 한 번에 산출합니다.

합성 로직은 Pillow 단일 의존성으로 자체 구현되어 있어 외부 패키지 설치가 필요하지 않습니다.

## 스킬 카탈로그 (11종)

### 상세페이지 (3)

| 스킬 | 역할 |
|------|------|
| [detail-page-copy](./skills/detail-page-copy/SKILL.md) | 13섹션 감정여정 카피 생성 (Hero→Pain→…→CTA) + ai-slop-reviewer 자동 체이닝 |
| [detail-page-image](./skills/detail-page-image/SKILL.md) | 13섹션 이미지 프롬프트 → moai-media:nano-banana 호출 → Pillow 1080×12720 합성 |
| [product-photo-brief](./skills/product-photo-brief/SKILL.md) | 상품 사진 사전 분석 + ProductDNA 추출 + 부족한 컷 식별 + 추가 촬영 브리프 |

### 채널 가이드 (5)

| 스킬 | 역할 |
|------|------|
| [marketplace-coupang](./skills/marketplace-coupang/SKILL.md) | 쿠팡 정책 + 검색최적화 + 우수상품 + 로켓배송 가이드 |
| [marketplace-naver](./skills/marketplace-naver/SKILL.md) | 네이버 스마트스토어 + 11번가/G마켓/옥션 오픈마켓 가이드 |
| [marketplace-d2c](./skills/marketplace-d2c/SKILL.md) | 자사몰(D2C) — 카페24 + 아임웹 + 메이크샵 운영 가이드 |
| [marketplace-crowdfunding](./skills/marketplace-crowdfunding/SKILL.md) | 크라우드펀딩 — 와디즈 + 텀블벅 프로젝트 기획·심사·운영 |
| [marketplace-curation](./skills/marketplace-curation/SKILL.md) | 큐레이션 — 카카오 메이커스 + 무신사 + 29CM 입점 제안 |

### 마케팅 (3)

| 스킬 | 역할 |
|------|------|
| [commerce-strategy](./skills/commerce-strategy/SKILL.md) | 통합 전략 — 채널 믹스, 가격, 프로모션 캘린더, 리텐션, KPI |
| [commerce-copywriting](./skills/commerce-copywriting/SKILL.md) | 광고·톡톡·푸시·이메일 카피 (ai-slop 자동 체이닝) |
| [live-commerce](./skills/live-commerce/SKILL.md) | 네이버·카카오·그립·쿠팡 라이브 커머스 가이드 + 30/60분 스크립트 |

## 표준 워크플로우

```
┌─ [1] product-photo-brief         — 상품 사진 분석 + 추가 촬영 브리프
│       ↓
├─ [2] detail-page-copy             — 13섹션 카피 생성 (+ ai-slop 검수)
│       ↓
├─ [3] detail-page-image            — 섹션별 이미지 + 1080×12720 합성
│       ↓
├─ [4] commerce-strategy            — 채널 믹스·가격·프로모션·리텐션 전략
│       ↓
├─ [5] marketplace-{coupang|naver|d2c|crowdfunding|curation}
│       — 채널별 입점·등록·운영 가이드
│       ↓
├─ [6] commerce-copywriting         — 광고·톡톡·푸시·이메일 카피
│       ↓
└─ [7] live-commerce                — 라이브 커머스 (선택)
```

## 13섹션 감정여정 구조

| # | 섹션 | 높이(px) | 역할 |
|---|------|---------|------|
| 1 | Hero | 1600 | 긴급성 헤더 + 메인 이미지 |
| 2 | Pain | 800 | 공감 — "이런 고민 있으신가요?" |
| 3 | Problem | 800 | 문제 정의 |
| 4 | Story | 1200 | Before→After 스토리 |
| 5 | Solution | 800 | 솔루션 소개 |
| 6 | How | 900 | 작동 방식 시각화 |
| 7 | Proof | 1420 | 사회적 증거 (리뷰/수치) |
| 8 | Authority | 800 | 권위/전문성 |
| 9 | Benefits | 1200 | 핵심 혜택 |
| 10 | Risk | 800 | 리스크 제거 (보증/환불) |
| 11 | Compare | 800 | 최종 Before/After |
| 12 | Filter | 700 | 타겟 필터링 |
| 13 | CTA | 900 | 최종 구매 유도 |

합계: **1080 × 12720 픽셀**

## 채널 분류

| 분류 | 채널 | 적합 |
|------|------|------|
| 오픈마켓 | 쿠팡 / 네이버 스마트스토어 / 11번가 / G마켓 / 옥션 | 트래픽 확보, 신규 매출 |
| 자사몰(D2C) | 카페24 / 아임웹 / 메이크샵 | 브랜드 통제, LTV 운영 |
| 크라우드펀딩 | 와디즈 / 텀블벅 | 신상 사전판매·검증 |
| 큐레이션 | 카카오 메이커스 / 무신사 / 29CM | 브랜드 가치, 한정 운영 |
| 라이브 커머스 | 네이버 쇼핑라이브 / 카카오 / 그립 / 쿠팡 라이브 | 실시간 전환, 인플루언서 |

> **참고**: 티몬·위메프는 큐텐 인수 후 2024년 미정산 사태로 회생절차에 진입하여 본 가이드 대상에서 제외되었습니다.

## 사용 예시

```
"무선 이어폰 상세페이지 만들어줘 — ANC, 30시간 배터리, 직장인 타겟. 사진 5장 첨부."
"비건 스킨케어 상폐 부탁해 — beauty 카테고리, 쿠팡 등록용."
"신생 패션 브랜드 자사몰 + 무신사 입점 전략 짜줘"
"신상품 와디즈 펀딩 기획 + 영상 시놉시스 부탁"
"네이버 쇼핑라이브 60분 스크립트 — 무선이어폰 3종"
"월 1천만원 매출 브랜드 채널 다각화 전략 + 광고 ROAS 추천"
"카트 이탈 회복 이메일 시퀀스 3건"
```

## 의존성

- **필수**: Pillow (Python 이미지 라이브러리) — `detail-page-image` 합성 단계
- **권장**: `moai-media` 플러그인 — 13섹션 이미지 생성 시 nano-banana 활용
- **선택**: `codex` CLI ≥0.124.0 + ChatGPT OAuth — `detail-page-copy`에서 보조 분석에 사용 가능 (없어도 동작)

## 라이선스

MIT — 자유롭게 사용·수정·재배포 가능.
