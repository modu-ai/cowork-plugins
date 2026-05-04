---
name: detail-page-copy
description: >
  한국 이커머스 상세페이지(상폐)를 위한 13섹션 감정여정 카피를 자동 생성하는 스킬입니다.
  "상세페이지 카피 써줘", "상폐 만들어줘", "이커머스 상세페이지 글 작성해줘", "쇼핑몰 상품 카피 만들어줘"처럼 말하면 됩니다.
  Hero → Pain → Problem → Story → Solution → How → Proof → Authority → Benefits → Risk → Compare → Filter → CTA
  순서로 구매 전환을 유도하는 심리 여정 카피를 섹션별로 구조화 JSON + 마크다운 미리보기로 산출합니다.
  카테고리(electronics/fashion/food/beauty/home/supplement/pet/kids/handmade/general)에 따라 어조와 키워드 전략이 달라집니다.
  출력 직전에 ai-slop-reviewer를 자동 호출하여 AI 패턴을 검수합니다.
user-invocable: true
version: 2.0.0
---

# 상세페이지 카피 (Detail Page Copy)

## 개요

이커머스 고전환 상세페이지를 위한 13섹션 감정여정 카피 생성 전문 스킬입니다.
소비자의 심리 여정(Pain 공감 → Problem 인식 → Solution 제시 → Proof 검증 → CTA 행동)을 따라
구매 결정을 자연스럽게 이끄는 카피를 자동으로 구성합니다.

지원 카테고리: electronics / fashion / food / beauty / home / supplement / pet / kids / handmade / general

## 트리거 키워드

상세페이지, 상폐, 이커머스 상세페이지, 쇼핑몰 카피, 상품 상세, 제품 상세페이지, 상품 설명 페이지,
detail page, 상세 카피, 온라인 쇼핑몰 상품 페이지, 감정여정 카피, 13섹션 상세페이지

## 필요 입력 정보

orchestrator가 사용자에게 다음 정보를 사전 수집합니다 (스킬 호출 전 AskUserQuestion 활용):

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| 상품명 | 필수 | "스마트워치 X200" |
| 카테고리 | 권장 | electronics, fashion, food, beauty, home, supplement, pet, kids, handmade, general |
| 핵심 USP | 필수 | "30시간 배터리 + ANC + IPX5 방수" |
| 타겟 고객 | 권장 | "20~40대 직장인, 운동 즐기는 분" |
| 가격대 | 선택 | "12만 9천원" |
| 브랜드 톤 | 선택 | "신뢰감 있고 전문적" / "젊고 활발하게" |
| 판매 채널 | 선택 | 쿠팡 / 스마트스토어 / 자사몰 / 범용 |
| 보증/AS 정책 | 선택 | "1년 무상 A/S" |

## 워크플로우

### 1단계: 상품 DNA 분석

입력된 상품 정보에서 다음을 추출합니다:

```
ProductDNA:
  physical:
    form: 상품 형태
    colors: 대표 색상
    material: 소재
    signature_angle: 대표 각도/뷰
  positioning:
    tier: mass / premium_indie / luxury
    tone: 어조 앵커 (신뢰/흥미/따뜻함/혁신)
    brand_archetype: 브랜드 원형
  palette:
    primary: 대표 색상
    background: 배경 색상
```

### 2단계: 카테고리 브리프 적용

카테고리별 비주얼·카피 원칙을 적용합니다 (`references/category-briefs.md` 참조):
- **electronics**: 정밀·혁신 어조, 스펙 중심, 기술 신뢰감
- **fashion**: 감성·라이프스타일, 여백 활용, 에디토리얼 톤
- **food**: 따뜻함·풍성함, 식감·향 묘사, 수제·자연 키워드
- **beauty**: 광채·클린뷰티, 성분 강조, 뷰티 루틴 연계
- **home**: 아늑함·의도적 삶, 인테리어 맥락, 감성 라이프스타일
- **supplement**: 신뢰·과학적 근거, 성분 명확화, 안전 보증
- **general**: 깔끔·범용, 제품 중심, 모던 미니멀

### 3단계: 13섹션 카피 생성

`references/13-sections.md`의 각 섹션 규칙을 따라 카피를 작성합니다:

#### 섹션별 카피 요소

| # | 섹션 | 핵심 요소 |
|---|------|----------|
| 1 | **Hero** | 메인 헤드라인 (10초 내 가치 전달) + 서브카피 + CTA 버튼 문구 + 긴급성 뱃지 |
| 2 | **Pain** | 공감 헤드라인 + 고통점 4가지 (불릿) + 감정 연결 문구 |
| 3 | **Problem** | 반전 훅 헤드라인 + 근본 원인 3가지 (번호) + 전환 문구 |
| 4 | **Story** | Before 상태 묘사 + 전환점 레이블 + After 상태 + 증거 수치 |
| 5 | **Solution** | 상품명 + 한 줄 솔루션 + 타겟 핏 태그라인 |
| 6 | **How** | 작동 방식 3단계 (제목 + 짧은 설명) + 결과 하이라이트 |
| 7 | **Proof** | 통계 3개 + 리뷰어 인용 3개 + 에디토리얼 톤 소개 |
| 8 | **Authority** | 창업자/전문가 인용 + 이름 + 직함 + 자격 |
| 9 | **Benefits** | 혜택 6가지 (아이콘 + 레이블) + 보너스 항목 + 총 가치 표현 |
| 10 | **Risk** | 보증 헤드라인 + FAQ 5개 (Q&A) + 공식 문구 |
| 11 | **Compare** | Without 포인트 3개 vs With 포인트 3개 |
| 12 | **Filter** | 추천 대상 3개 + 비추천 대상 3개 |
| 13 | **CTA** | 최종 헤드라인 + 긴급성 카피 + 가격/혜택 표현 + CTA 버튼 + 마감 태그라인 |

### 4단계: ai-slop-reviewer 자동 체이닝 (HARD)

**모든 텍스트 카피 산출 직전에 `moai-core:ai-slop-reviewer`를 호출합니다.**

검수 항목:
- AI 특유 반복 표현 ("물론입니다", "훌륭한", "혁신적인" 등) 제거
- 과도한 형용사 클리셰 정제
- 한국어 이커머스 자연 어체로 조정
- 마케팅 과장 문구 사실 기반으로 수정

## 출력 형식

### 카피 JSON 구조

```json
{
  "product": {
    "name": "상품명",
    "category": "electronics",
    "usp": "핵심 USP",
    "target": "타겟 고객",
    "price": "가격대",
    "tier": "premium_indie"
  },
  "sections": [
    {
      "id": "hero",
      "label": "Hero (긴급성 헤더)",
      "headline": "메인 헤드라인",
      "subheadline": "서브카피",
      "cta": "CTA 버튼 문구",
      "badge": "긴급성 뱃지 문구"
    },
    {
      "id": "pain",
      "label": "Pain (공감)",
      "headline": "공감 헤드라인",
      "bullets": ["고통점1", "고통점2", "고통점3", "고통점4"],
      "bridge": "감정 연결 문구"
    },
    {
      "id": "problem",
      "label": "Problem (문제 정의)",
      "hook": "반전 훅 헤드라인",
      "causes": ["원인1", "원인2", "원인3"],
      "transition": "전환 문구"
    },
    {
      "id": "story",
      "label": "Story (Before→After)",
      "before": "Before 상태 묘사",
      "turning_point": "전환점 레이블",
      "after": "After 상태 묘사",
      "stat": "증거 수치"
    },
    {
      "id": "solution",
      "label": "Solution (솔루션 소개)",
      "product_name": "상품명",
      "one_liner": "한 줄 솔루션",
      "tagline": "타겟 핏 태그라인"
    },
    {
      "id": "how",
      "label": "How It Works (작동 방식)",
      "steps": [
        {"title": "1단계 제목", "desc": "설명"},
        {"title": "2단계 제목", "desc": "설명"},
        {"title": "3단계 제목", "desc": "설명"}
      ],
      "result": "결과 하이라이트"
    },
    {
      "id": "proof",
      "label": "Social Proof (사회적 증거)",
      "stats": ["통계1", "통계2", "통계3"],
      "reviews": [
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"},
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"},
        {"quote": "리뷰 인용", "reviewer": "리뷰어명"}
      ]
    },
    {
      "id": "authority",
      "label": "Authority (권위/전문성)",
      "quote": "전문가 인용",
      "name": "이름",
      "title": "직함",
      "credentials": "자격/경력"
    },
    {
      "id": "benefits",
      "label": "Benefits (혜택)",
      "items": [
        {"label": "혜택1", "desc": "설명"},
        {"label": "혜택2", "desc": "설명"},
        {"label": "혜택3", "desc": "설명"},
        {"label": "혜택4", "desc": "설명"},
        {"label": "혜택5", "desc": "설명"},
        {"label": "혜택6", "desc": "설명"}
      ],
      "bonus": "보너스 항목",
      "total_value": "총 가치 표현"
    },
    {
      "id": "risk",
      "label": "Risk Removal (리스크 제거)",
      "guarantee_headline": "보증 헤드라인",
      "faqs": [
        {"q": "질문1", "a": "답변1"},
        {"q": "질문2", "a": "답변2"},
        {"q": "질문3", "a": "답변3"},
        {"q": "질문4", "a": "답변4"},
        {"q": "질문5", "a": "답변5"}
      ]
    },
    {
      "id": "compare",
      "label": "Before/After Final (최종 대비)",
      "without": ["포인트1", "포인트2", "포인트3"],
      "with": ["포인트1", "포인트2", "포인트3"]
    },
    {
      "id": "filter",
      "label": "Target Filter (타겟 필터)",
      "recommend": ["추천 대상1", "추천 대상2", "추천 대상3"],
      "not_recommend": ["비추천 대상1", "비추천 대상2", "비추천 대상3"]
    },
    {
      "id": "cta",
      "label": "Final CTA (최종 CTA)",
      "headline": "최종 헤드라인",
      "urgency": "긴급성 카피",
      "price_display": "가격/혜택 표현",
      "cta_button": "CTA 버튼 문구",
      "closing": "마감 태그라인"
    }
  ],
  "slop_review": {
    "status": "passed",
    "changes_made": 0,
    "notes": "ai-slop-reviewer 검수 결과"
  }
}
```

### 마크다운 미리보기

JSON 출력 후, 사용자 확인용 마크다운 미리보기를 섹션별로 제공합니다.

## codex CLI 선택적 백엔드

`codex` CLI가 설치되어 있고 OAuth 세션이 활성화된 경우, 분석 단계에서 보조적으로 활용할 수 있습니다.
설치되지 않은 경우 Claude 자체로 카피를 완전히 생성합니다. 두 경우 모두 품질 차이 없습니다.

확인 명령: `codex --version` (없으면 Claude 단독 실행)

## 사용 예시

- "무선 이어폰 상세페이지 카피 써줘 — ANC 탑재, 30시간 배터리, 직장인 타겟"
- "비건 스킨케어 세트 상폐 만들어줘 — 카테고리 beauty"
- "수제 원목 도마 이커머스 상세페이지 — handmade 카테고리, 프리미엄 톤"
- "반려견 유산균 상세페이지 카피 — 수의사 추천 포인트 있음"

## 관련 스킬

- `moai-commerce:detail-page-image` — 생성된 카피를 기반으로 13섹션 이미지 합성
- `moai-commerce:marketplace-coupang` — 쿠팡 정책 적용 최적화
- `moai-commerce:marketplace-naver` — 스마트스토어/오픈마켓 최적화
- `moai-content:copywriting` — 일반 광고 카피
- `moai-content:product-detail` — shadcn/ui 기반 웹 상세페이지
- `moai-core:ai-slop-reviewer` — 텍스트 검수 (이 스킬에서 자동 호출)

## 이 스킬을 사용하지 말아야 할 때

- 랜딩 페이지(마케팅 원페이지): `moai-content:landing-page` 사용
- 블로그 포스팅: `moai-content:blog` 사용
- SNS 콘텐츠: `moai-content:social-media` 사용
- 이미지 합성만 필요할 때: `moai-commerce:detail-page-image` 직접 사용