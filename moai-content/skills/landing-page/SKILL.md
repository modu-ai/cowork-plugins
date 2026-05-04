---
name: landing-page
description: >
  shadcn/ui 기반 고전환율 랜딩 페이지를 설계·생성해주는 스킬입니다.
  "랜딩 페이지 만들어줘", "세일즈 페이지 기획해줘", "원페이지 구성해줘"처럼 말하면 됩니다.
  코드 생성 전에 shadcn 테마 인터뷰(베이스 팔레트, 컬러 모드, 모서리 반경, 효과)를 먼저 묻고,
  Next.js 15 + Tailwind CSS v4 + shadcn/ui 스택으로 히어로부터 CTA까지 전환율 최적화
  랜딩 페이지 전체 구성, 디자인 토큰(OKLCH), Framer Motion 효과를 산출합니다.
user-invocable: true
version: 2.0.0
---

# 랜딩 페이지 (Landing Page)

## 개요

shadcn/ui 기반 고전환율 원페이지 랜딩 설계 전문 스킬입니다.
소크라테스식 테마 인터뷰로 사용자 의도에 맞는 디자인 시스템을 자동 선택하고,
히어로부터 최종 CTA까지 전환율 최적화된 랜딩 페이지를 설계·생성합니다.

지원 영역:
- shadcn/ui 기반 랜딩 페이지 전체 설계 (히어로~CTA)
- Next.js 15 + Tailwind CSS v4 + shadcn/ui 스택
- OKLCH 컬러 토큰 기반 Light/Dark 모드 동시 산출
- Framer Motion 인터랙션 프리셋 (페이드업·스크롤 리빌·패럴랙스)
- 제품·서비스 런칭, 이벤트, 리드 수집용 랜딩

## 트리거 키워드

랜딩페이지, 원페이지, 랜딩 페이지, 세일즈 페이지, 전환율, CTA, 히어로 섹션, 랜딩, shadcn 랜딩, shadcn ui

## 워크플로우

### 0단계: shadcn 테마 인터뷰 (HARD)

코드·디자인 스펙 산출 직전에 반드시 수행합니다.

```
Q1: 베이스 팔레트 선택
- Neutral (기본)
- Zinc
- Stone
- Slate

Q2: 컬러 모드 선택
- System+Toggle (기본)
- Light
- Dark
- Auto

Q3: 모서리 반경 선택
- Balanced 0.5rem (기본)
- Sharp
- Soft
- Pill

Q4: 효과 선택 (복수)
- Fade-up
- Scroll Reveal
- Parallax
- Chart
```

Chart 선택 시 Q5 차트 라이브러리 선택 (Recharts/Chart.js/Tremor/ECharts)

### 1단계: 목적 및 타겟 파악

- 전환 목표: 구매 / 회원가입 / 다운로드 / 문의 / 이벤트 참가
- 타겟 독자 (고통점, 니즈, 반대 의견)
- 제품·서비스 핵심 가치 제안 (Value Proposition) 1가지

### 2단계: 브랜드 컨텍스트 수집

- 브랜드 보이스 앵커 (형용사 3-5개)
- 주요 색상 (primary + accent)
- 타겟 독자 수준 (초등/고교/대학/전문가)
- CTA 전략 (1개? 2개? 3개?)
- 톤 예시 ("이런 느낌 좋아요" / "이런 건 싫어요")

### 3단계: 섹션 구성 (shadcn 블록 매핑)

```
[Hero]         → shadcn Hero 블록 + 히어로 이미지/Video
[Problem]      → Grid of Card (고통점 3~5)
[Solution]     → Feature list + Lucide 아이콘
[Social Proof] → Testimonial Card + Avatar + StarRating
[Features]     → Tabs or Accordion (Before/After)
[Pricing]      → shadcn Pricing 블록 (Most Popular 강조)
[FAQ]          → Accordion
[Final CTA]    → Button (size=lg) + Badge("14일 무료")
```

### 4단계: 전환율 최적화 체크리스트

- 헤드라인이 10초 내에 가치를 전달하는가?
- CTA 버튼이 스크롤 없이 보이는가? (Above the Fold)
- 텍스트 블록 없이 시각적으로 스캔 가능한가?
- 모바일에서도 CTA가 잘 보이는가?
- 후기가 구체적인가? (수치 포함)
- 반대 의견(FAQ)을 미리 해소하는가?

### 5단계: 카피 작성

- 전체 카피 작성 (섹션별)
- 헤드라인 후보 5가지 제시
- CTA 버튼 문구 후보 3가지 제시

### 6단계: 코드 생성 (shadcn 스택)

산출물 구성:
1. `components.json` — shadcn CLI 초기화 설정
2. `app/globals.css` — OKLCH CSS 변수 `:root` + `.dark`
3. `tailwind.config.ts` — v4 토큰 매핑
4. `app/page.tsx` — 섹션 조립
5. `components/sections/*.tsx` — 섹션별 컴포넌트
6. `components/ui/*` — 사용된 shadcn 컴포넌트 목록
7. (옵션) `components/motion/*.tsx` — Framer Motion 래퍼
8. `README-setup.md` — 설치 명령

## 사용 예시

- "SaaS 제품 랜딩 페이지 구성해줘"
- "이벤트 참가 신청 랜딩 만들어줘"
- "무료 체험 유도 세일즈 페이지 기획해줘"
- "앱 다운로드 랜딩 페이지 카피 써줘"
- "B2B 서비스 리드 수집 랜딩 설계해줘"
- "shadcn 스타일로 깔끔한 원페이지 만들어줘"

## 출력 형식

### 카피 JSON 구조

```json
{
  "page_type": "landing",
  "theme": {
    "system": "shadcn/ui",
    "base": "neutral",
    "mode": "system+toggle",
    "radius": "0.5rem",
    "effects": ["fade-up", "scroll-reveal"],
    "chart_lib": null
  },
  "sections": [
    {
      "id": "hero",
      "shadcn_block": "hero-01",
      "headline": "헤드라인",
      "subheadline": "서브헤드라인",
      "cta_primary": "CTA 텍스트",
      "cta_secondary": null,
      "visual_direction": "제품 사용 장면 이미지"
    },
    {
      "id": "problem",
      "shadcn_block": "feature-grid",
      "headline": "고통점 섹션 제목",
      "body": "고통점 설명",
      "items": ["고통점1", "고통점2", "고통점3"]
    }
  ],
  "metadata": {
    "tone_profile": "신뢰+권위",
    "reading_level": "고교",
    "word_count": 0,
    "cta_count": 0
  }
}
```

### 코드 산출물

- `components.json` — shadcn 설정
- `app/globals.css` — CSS 변수
- `app/page.tsx` — 메인 페이지
- `components/sections/*.tsx` — 섹션 컴포넌트
- `README-setup.md` — 설치 가이드

## 주의사항

### 핵심 규칙: 카피 무결성

디자인/개발 단계에서 카피 텍스트를 수정하지 않습니다.
- 원본 카피를 그대로 구현
- 텍스트 수정이 필요하면 카피 작성 단계로 반려
- 줄바꿈, 강조, 순서 변경만 허용 (내용 변경 금지)

### AI 생성 콘텐츠 주의

AI가 생성한 랜딩 페이지 카피는 사실 확인 후 사용하세요.
사용자 수, 만족도, 수상 이력 등 실증적 주장은 반드시 데이터를 확인하세요.

### 문제 해결

- **플랫폼 규격 변경**: 노코드 툴(Webflow, Framer, Wix)의 UI 및 기능은 수시로 변경됩니다. 구현 방향은 참고용으로 활용하세요.
- **shadcn 버전 충돌**: shadcn CLI v4 기준으로 산출. 구 버전 프로젝트는 `pnpm dlx shadcn@latest init`으로 마이그레이션 후 적용하세요.
- **브랜드 가이드 미제공**: shadcn 베이스 팔레트를 그대로 적용하고 결과를 보여준 뒤 사용자가 정제를 요청하면 `--primary` 오버라이드만 추가합니다.
- **이미지 생성 실패**: 이 스킬은 텍스트 카피와 디자인 방향을 제공합니다. 실제 이미지는 `moai-media:nano-banana`(한국어 타이포 SOTA)·`moai-media:image-gen`(일반 이미지)·`moai-media:fal-gateway`(Flux·Ideogram 등) 또는 Unsplash·Pexels를 활용하세요.
- **A/B 테스트 필요**: AI가 생성한 랜딩 페이지 카피의 최적안은 실제 트래픽 테스트로만 확인 가능합니다. 헤드라인과 CTA를 중심으로 A/B 테스트를 진행하세요.

## 관련 스킬

- `product-detail` — 제품 상세 페이지 (이커머스)
- `social-media` — 소셜미디어 콘텐츠
- `copywriting` — 광고 카피 단독 작성
- `blog` — SEO 블로그 포스팅

## 이 스킬을 사용하지 말아야 할 때

- 블로그 포스팅: `blog` 스킬 사용
- SNS 포스팅: `social-media` 스킬 사용
- 이메일 뉴스레터: `newsletter` 스킬 사용
- 제품 상세페이지: `product-detail` 스킬 사용
- 데이터 대시보드: `data-visualizer` 스킬 사용
- 멀티 페이지 웹사이트: 별도 웹 에이전트 필요