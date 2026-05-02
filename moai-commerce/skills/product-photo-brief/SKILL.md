---
name: product-photo-brief
description: >
  사용자가 제공한 상품 사진을 분석하여 ProductDNA를 추출하고, 13섹션 상세페이지에 부족한 컷을 식별,
  추가 촬영을 위한 구체적인 브리프를 작성해주는 스킬입니다.
  "상품 사진 분석해줘", "촬영 브리프 만들어줘", "부족한 컷 알려줘", "어떤 사진이 더 필요해?"처럼 말하면 됩니다.
  형태·소재·색상·시그니처 앵글·포지셔닝(mass/premium_indie/luxury)을 추출하고,
  13섹션별 사용 가능한 컷 매핑 + 추가 촬영 권장 리스트를 산출합니다.
user-invocable: true
---

# 상품 사진 사전 브리프 (Product Photo Brief)

## 개요

상세페이지 제작에 앞서 사용자의 상품 사진을 분석하고 부족한 컷을 식별하는 스킬입니다.
13섹션 상세페이지 각 섹션에 어떤 사진이 필요한지 매핑하고,
이미 있는 컷과 추가로 촬영해야 할 컷을 명확히 구분합니다.

## 트리거 키워드

상품 사진 분석, 촬영 브리프, 부족한 컷, 사진 평가, 제품 사진, 상품 DNA,
ProductDNA, 사진 점검, 추가 촬영, 어떤 사진이 더 필요

## 워크플로우

### 1단계: 사진 분석 (Vision)

사용자가 제공한 1~14장의 사진을 분석하여 다음을 추출:

#### 물리적 특성 (Physical)
- form: 상품 형태 (병/박스/원통/평면 등)
- dimensions_hint: 크기 추정 (대략)
- colors: 대표 색상 1~3개
- material: 주 소재
- texture_keywords: 질감 키워드 (매트/광택/우드/메탈/패브릭)
- signature_angle: 가장 잘 표현되는 각도
- surface_details: 표면 디테일 (로고/엠보싱/라벨 등)

#### 포지셔닝 (Positioning)
- tier: mass / premium_indie / luxury
- price_tier_hint: 추정 가격대
- tone: 어조 앵커
- brand_archetype: 브랜드 원형 (Sage/Innocent/Hero 등)

#### 팔레트 (Palette)
- primary: 대표 색상
- secondary, accent
- background: 배경 톤

### 2단계: 13섹션 컷 매핑

각 섹션에 어떤 컷이 사용 가능한지 매핑합니다:

```
섹션 1 Hero        : ✅ 시그니처 컷 (있음) / ❌ 추가 촬영 필요
섹션 4 Story       : ⚠️ Before/After 페어 필요
섹션 5 Solution    : ✅ 스튜디오 뷰티샷 (있음)
섹션 7 Proof       : ❌ 리뷰어 사용 컷 부족 — 라이프스타일 컷 필요
섹션 8 Authority   : ❌ 창업자/전문가 포트레이트 필요
섹션 9 Benefits    : ⚠️ 라이프스타일 컷 1장 추가 권장
섹션 11 Compare    : ⚠️ Without/With 페어 권장
...
```

### 3단계: 추가 촬영 브리프 작성

부족한 컷마다 구체적 브리프 생성:

```
[추가 촬영 #1: Authority 섹션용 창업자 포트레이트]
구도: 3/4 크롭, 약간 우측 향함
배경: 디새튜레이트 톤 (스튜디오 회색 또는 작업실 분위기)
라이팅: 웜 키 라이트 + 약한 백라이트
표정: 자신감 있고 따뜻한 느낌
프레임: 가슴 ~ 머리 위
복장: 브랜드 톤에 맞는 캐주얼 또는 스마트
의도: "이 분이 만든 것"이라는 신뢰 형성

[추가 촬영 #2: Compare 섹션용 Before 컷]
구도: 좌측 절반 (수직 분할 합성용)
무드: 답답함, 무드 다운 (실제 고통 상황 연출)
모델: 30~40대 직장인 (운동 후 답답함, 통화 중 답답함 등)
표정: 약간의 불편함
배경: 어두운 사무실, 지하철 등
의도: After 컷과 직접 대비
```

### 4단계: 컷 우선순위

추가 촬영 컷을 비용·난이도·임팩트 기준으로 우선순위 부여:

| 우선순위 | 컷 | 임팩트 | 촬영 난이도 |
|---------|-----|------|----------|
| 🔴 필수 | 시그니처 뷰티샷 | 매우 높음 | 중 (스튜디오) |
| 🟡 권장 | Before/After 페어 | 높음 | 중 |
| 🟢 선택 | 디테일 클로즈업 | 중 | 낮음 |

## 출력 형식

```json
{
  "product_dna": {
    "physical": {
      "form": "원통형 보틀",
      "dimensions_hint": "높이 약 18cm",
      "colors": ["amber", "matte black"],
      "material": "유리 + 무광 캡",
      "texture_keywords": ["matte", "glass"],
      "signature_angle": "정면 약간 위에서",
      "surface_details": ["엠보싱 로고", "라벨 미니멀"]
    },
    "positioning": {
      "tier": "premium_indie",
      "price_tier_hint": "3~5만원대",
      "tone": "차분, 고급, 신뢰",
      "brand_archetype": "Sage"
    },
    "palette": {
      "primary": "amber #C18841",
      "secondary": "matte black #1A1A1A",
      "background": "warm cream #F5F0E8"
    }
  },
  "available_cuts": {
    "01_hero": "✅",
    "02_pain": "N/A — 이 섹션은 상품 노출 X",
    "04_story": "❌ Before/After 페어 필요",
    "05_solution": "✅",
    "07_proof": "❌ 리뷰어 사용 컷 부족",
    "08_authority": "❌",
    "09_benefits": "⚠️ 라이프스타일 1장 추가 권장",
    "11_compare": "⚠️ Without 컷 필요",
    "13_cta": "✅ Hero 재사용 가능"
  },
  "additional_shots_required": [
    {
      "priority": "필수",
      "section": "08_authority",
      "shot_id": "authority_founder_portrait",
      "brief": {
        "composition": "3/4 크롭, 약간 우측 향함",
        "background": "디새튜레이트 회색",
        "lighting": "웜 키 라이트 + 약한 백라이트",
        "expression": "자신감 + 따뜻함",
        "frame": "가슴 ~ 머리 위",
        "intent": "신뢰 형성"
      }
    },
    {
      "priority": "권장",
      "section": "04_story + 11_compare",
      "shot_id": "before_after_pair",
      "brief": {
        "before_mood": "답답함, 무드 다운",
        "after_mood": "밝고 만족",
        "composition": "동일 구도 (좌우 분할 합성용)",
        "model": "30~40대 직장인"
      }
    }
  ],
  "shoot_recommendation_summary": "필수 2컷 + 권장 3컷 = 5컷 추가 촬영 시 13섹션 풀세트 가능"
}
```

## 사용 예시

- "상품 사진 5장 첨부 — 분석해줘 (electronics 카테고리)"
- "이 화장품 사진들로 상세페이지 만들기 충분한지 봐줘"
- "어떤 사진이 더 필요한지 촬영 브리프 만들어줘"
- "신상품 발매 전에 어떤 컷을 더 찍어야 할까?"

## 관련 스킬

- `moai-commerce:detail-page-copy` — 13섹션 카피 (이 스킬의 ProductDNA 활용)
- `moai-commerce:detail-page-image` — 이미지 생성·합성
- `moai-media:nano-banana` — 부족한 컷을 AI로 생성하고 싶을 때 (실사 촬영 대체)
- `moai-content:landing-page` — 웹용 상세페이지

## 이 스킬을 사용하지 말아야 할 때

- 카피만 필요할 때: `detail-page-copy` 사용
- 이미지 생성: `moai-media:nano-banana` 사용
- 마켓 등록 가이드: `marketplace-coupang` 또는 `marketplace-naver`

## 주의사항

- AI 분석은 사진의 시각적 특성에 한정됩니다. 실제 소재·치수는 사용자 확인 필수.
- ProductDNA의 tier/tone 추정은 가설이므로 사용자가 검토·수정 가능.
- 추가 촬영 브리프는 일반 가이드이며, 실제 촬영 환경·예산에 따라 조정 필요.
