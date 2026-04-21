---
name: landing-page
description: >
  shadcn/ui 기반 고전환율 랜딩 페이지를 설계·생성해주는 스킬입니다.
  "랜딩 페이지 만들어줘", "세일즈 페이지 기획해줘", "원페이지 구성해줘"처럼 말하면 됩니다.
  코드 생성 전에 소크라테스식 테마 인터뷰(베이스 팔레트, 컬러 모드, 모서리 반경, 효과)를
  먼저 묻고, Next.js 15 + Tailwind CSS v4 + shadcn/ui 스택으로 히어로부터 CTA까지
  전환율 최적화 랜딩 페이지 전체 구성, 디자인 토큰(OKLCH), Framer Motion 효과를 산출합니다.
user-invocable: true
---

# 랜딩 페이지 (Landing Page)

> moai-content | shadcn/ui 기반 랜딩 페이지 전문 스킬 · v1.4.0에서 shadcn/ui 기본 스택으로 전환

## 지원 영역

- shadcn/ui 기반 고전환율 원페이지 랜딩 설계 (히어로~CTA 전체 섹션)
- 소크라테스식 테마 인터뷰로 사용자 의도에 맞는 디자인 시스템 자동 선택
- 디자인 원칙 적용 (Above the Fold, 시각적 계층, F-패턴)
- CTA 버튼 문구 및 배치 최적화
- 제품·서비스 런칭, 이벤트, 리드 수집용 랜딩 페이지
- OKLCH 컬러 토큰 기반 Light/Dark 모드 동시 산출
- Framer Motion 인터랙션 프리셋(페이드업·스크롤 리빌·패럴랙스)
- Recharts/Chart.js 데이터 섹션(선택 시)

## 기본 스택 (v1.4.0)

| 레이어 | 기본값 | 비고 |
|--------|-------|------|
| 프레임워크 | Next.js 15 App Router + React 19 | 단일 HTML 모드는 Tailwind CDN 경량 |
| 스타일 | Tailwind CSS v4 (CSS Variables) | `@theme` 블록 자동 생성 |
| UI 컴포넌트 | **shadcn/ui** (Radix 기반) | 공식 블록 Hero/Features/Pricing/FAQ 활용 |
| 아이콘 | Lucide React | `shadcn add <block>` 호환 |
| 애니메이션 | Framer Motion | 인터뷰 Q4 선택 시 포함 |
| 폰트 | Pretendard (KR) + Inter (EN) | `next/font` 최적화 |
| 차트 | Recharts | 인터뷰 Q5에서 선택 시 |

> 사용자가 다른 프레임워크를 명시적으로 요청한 경우(Framer/Webflow/Wix 등) 해당 플랫폼 지시에 맞춰 재산출한다.

## 레퍼런스 가이드

- `references/landing-page/shadcn-theme-interview.md` — **[v1.4.0 신규] shadcn 테마 인터뷰 프로토콜 + CSS 변수 템플릿**
- `references/landing-page/guide.md` — 랜딩 페이지 빌더 가이드
- `references/landing-page/design-principles.md` — 디자인 토큰 및 원칙
- `references/landing-page/brand-context-template.md` — 브랜드 컨텍스트 사전 수집
- `references/landing-page/copywriting-rules.md` — 카피 안티패턴 및 규칙
- `references/landing-page/evaluation-checklist.md` — 평가 체크리스트
- `references/landing-page/ab-testing-guide.md` — A/B 테스트 가이드

## 트리거 키워드

랜딩페이지, 원페이지, 랜딩 페이지, 세일즈 페이지, 전환율, CTA, 히어로 섹션, 랜딩, shadcn 랜딩, shadcn ui

## 사용 예시

- "SaaS 제품 랜딩 페이지 구성해줘"
- "이벤트 참가 신청 랜딩 만들어줘"
- "무료 체험 유도 세일즈 페이지 기획해줘"
- "앱 다운로드 랜딩 페이지 카피 써줘"
- "B2B 서비스 리드 수집 랜딩 설계해줘"
- "shadcn 스타일로 깔끔한 원페이지 만들어줘"

---

## 실행 워크플로우

### [HARD] 0단계: shadcn 테마 인터뷰

코드·디자인 스펙 산출 **직전에 반드시 수행**한다. MoAI 오케스트레이터가 `AskUserQuestion`으로 다음 4개 질문을 한 번에 제시한다(복수 선택 포함).

1. **Q1 베이스 팔레트** — Neutral(기본) / Zinc / Stone / Slate
2. **Q2 컬러 모드** — System+Toggle(기본) / Light / Dark / Auto
3. **Q3 모서리 반경** — Balanced 0.5rem(기본) / Sharp / Soft / Pill
4. **Q4 효과(multiSelect)** — Fade-up / Scroll Reveal / Parallax / Chart

Q4에서 `Chart`가 선택된 경우 Q5(Recharts/Chart.js/Tremor/ECharts)를 추가 호출한다.

상세 질문 payload·예외 처리·Fallback 기본값은 `references/landing-page/shadcn-theme-interview.md` 참조.

Fallback 조건(인터뷰 생략):
- 사용자가 "그냥 기본", "빠르게", "--quick"으로 지정
- 동일 세션에서 이미 테마 선택 완료
- 프로토타입·샘플 목적임이 명시됨

Fallback 기본값: `Neutral + System+Toggle + 0.5rem + Fade-up`. 적용 시 응답 상단에 알림을 고지한다.

### 1단계: 목적 및 타겟 파악

- 전환 목표: 구매 / 회원가입 / 다운로드 / 문의 / 이벤트 참가
- 타겟 독자 (고통점, 니즈, 반대 의견)
- 제품·서비스 핵심 가치 제안 (Value Proposition) 1가지

### 2단계: 브랜드 컨텍스트 수집

- [ ] 브랜드 보이스 앵커 (형용사 3-5개: 예: "신뢰, 전문, 따뜻한")
- [ ] 주요 색상 (primary + accent 최소)
- [ ] 타겟 독자 수준 (초등/고교/대학/전문가)
- [ ] CTA 전략 (1개? 2개? 3개?)
- [ ] 톤 예시 ("이런 느낌 좋아요" / "이런 건 싫어요" 각 1-2개)

상세 템플릿: `references/landing-page/brand-context-template.md`

브랜드 컬러가 이미 있는 경우: 0단계에서 선택된 shadcn base를 뉴트럴 스캐폴드로 사용하고 `--primary`, `--accent`, `--ring`만 브랜드 컬러(OKLCH 변환)로 오버라이드한다.

### Hero-First 원칙

히어로 섹션이 전체 페이지 톤을 결정합니다. 이후 모든 섹션은 히어로의 디자인 언어(색상, 타이포, 모션)를 따릅니다.

히어로 허용: 브랜드명 1개 + 헤드라인 1줄 + 서브헤드라인 1문장 + CTA 1-2개 + 지배적 이미지
히어로 금지: 통계 나열, 기능 목록, 가격표, 소셜 미디어 아이콘, 네비게이션 외 링크

### CTA 전략 (목적별 결정)

| 페이지 유형 | CTA 수 | 배치 |
|------------|--------|------|
| 단일 제품 선택 | 1개 | 히어로만 |
| 장문 세일즈 페이지 | 3개 | 히어로 + 중간 + 하단 |
| 리드 생성 | 2개 | 폼 제출 + 보조 CTA |
| 이벤트 등록 | 2개 | 히어로 + 하단 |

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

각 블록은 `shadcn add <block-name>` 또는 공식 블록 카탈로그 참고로 설치 가능한 구조로 산출한다.

### 4단계: 전환율 최적화 체크리스트

- [ ] 헤드라인이 10초 내에 가치를 전달하는가?
- [ ] CTA 버튼이 스크롤 없이 보이는가? (Above the Fold)
- [ ] 텍스트 블록 없이 시각적으로 스캔 가능한가?
- [ ] 모바일에서도 CTA가 잘 보이는가?
- [ ] 후기가 구체적인가? (수치 포함)
- [ ] 반대 의견(FAQ)을 미리 해소하는가?
- [ ] Light/Dark 모드에서 모두 가독성 확보되는가? (shadcn 토큰 준수)

### 5단계: 카피 작성

- 전체 카피 작성 (섹션별)
- 헤드라인 후보 5가지 제시
- CTA 버튼 문구 후보 3가지 제시

카피 JSON 구조는 아래 "카피 출력 형식" 섹션 참조.

### 6단계: 코드 생성 (shadcn 스택)

산출물 구성:

1. `components.json` — shadcn CLI 초기화 설정 (인터뷰 Q1 base 반영)
2. `app/globals.css` — OKLCH CSS 변수 `:root` + `.dark`
3. `tailwind.config.ts` / `@theme` — v4 토큰 매핑
4. `app/page.tsx` — 섹션 조립
5. `components/sections/*.tsx` — 섹션별 컴포넌트 (Hero, Features, Pricing, FAQ 등)
6. `components/ui/*` — 사용된 shadcn 컴포넌트 목록 (Button, Card, Accordion 등)
7. (옵션) `components/motion/*.tsx` — Framer Motion 래퍼
8. `README-setup.md` — 설치 명령 (`pnpm dlx shadcn init`, `shadcn add button card accordion …`)

단일 HTML 파일이 필요한 경우(스마트스토어 업로드·임시 공유): Tailwind CDN + shadcn CSS 변수 인라인 삽입 모드로 전환한다.

### 7단계: QA 테스트 (권장)

- [ ] 데스크톱(1280x720) + 모바일(375x667) 레이아웃 확인
- [ ] 모든 CTA 버튼 클릭 테스트
- [ ] 다크 모드 토글 동작 (인터뷰 Q2 선택값 기준)
- [ ] 전체 페이지 스크롤 검증 (깨지는 섹션 없음)
- [ ] Lighthouse 감사: Performance >= 80, Accessibility >= 90
- [ ] 모든 링크/폼 정상 작동 (404 없음)
- [ ] 카피 무결성 검증 (원본 대비 변경 없음)
- [ ] shadcn 토큰 준수 확인 (하드코딩된 색상 없음)

평가 상세: `references/landing-page/evaluation-checklist.md`

---

## 카피 출력 형식 (JSON 구조)

카피 작성 결과는 구조화된 형식으로 산출합니다:

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
      "body": null,
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

이 형식은 디자이너/개발자에게 기계적으로 파싱 가능한 입력을 제공합니다.

## 핵심 규칙: 카피 무결성

디자인/개발 단계에서 카피 텍스트를 수정하지 않습니다.
- 원본 카피를 그대로 구현
- 텍스트 수정이 필요하면 카피 작성 단계로 반려
- 줄바꿈, 강조, 순서 변경만 허용 (내용 변경 금지)

## 톤 프로파일 분석

카피 작성 시 톤 분석을 함께 출력합니다:
- **주요 감정**: (예: 신뢰, 권위, 호기심)
- **독자가 느낄 것**: 한 문장으로 요약
- **문장 평균 길이**: 20단어 이내 권장
- **피해야 할 것**: 과도한 감탄사, 기술 전문 용어

---

## 실행 규칙

1. 사용자 요청 수신 → 랜딩 페이지 요청 확인
2. **shadcn 테마 인터뷰 실행** (0단계, HARD)
3. `references/landing-page/guide.md` 존재 시 로드 → 가이드에 따라 실행
4. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
5. 코드 산출 후 `ai-slop-reviewer`로 카피 검수 (텍스트 산출물 한정)
6. 결과물 생성 후 사용자 검토 요청

⚠️ **AI 생성 콘텐츠 주의**: AI가 생성한 랜딩 페이지 카피는 사실 확인 후 사용하세요. 사용자 수, 만족도, 수상 이력 등 실증적 주장은 반드시 데이터를 확인하세요.

## 문제 해결

- **플랫폼 규격 변경**: 노코드 툴(Webflow, Framer, Wix)의 UI 및 기능은 수시로 변경됩니다. 구현 방향은 참고용으로 활용하세요.
- **shadcn 버전 충돌**: shadcn CLI v4 기준으로 산출. 구 버전 프로젝트는 `pnpm dlx shadcn@latest init`으로 마이그레이션 후 적용하세요.
- **브랜드 가이드 미제공**: shadcn 베이스 팔레트를 그대로 적용하고 결과를 보여준 뒤 사용자가 정제를 요청하면 `--primary` 오버라이드만 추가합니다.
- **이미지 생성 실패**: 이 스킬은 텍스트 카피와 디자인 방향을 제공합니다. 실제 이미지는 `moai-media:nano-banana`/`ideogram` 스킬 또는 Unsplash·Pexels를 활용하세요.
- **A/B 테스트 필요**: AI가 생성한 랜딩 페이지 카피의 최적안은 실제 트래픽 테스트로만 확인 가능합니다. 헤드라인과 CTA를 중심으로 A/B 테스트를 진행하세요.

## 이 스킬을 사용하지 말아야 할 때

- **블로그 포스팅**: SEO 블로그 글 작성은 `blog` 스킬이 더 적합합니다.
- **SNS 포스팅**: 소셜미디어 콘텐츠는 `social-media` 스킬을 사용하세요.
- **이메일 뉴스레터**: 구독자 대상 뉴스레터는 `newsletter` 스킬을 사용하세요.
- **광고 카피 단독 작성**: 헤드라인·슬로건만 필요한 경우 `copywriting` 스킬이 더 적합합니다.
- **제품 상세페이지**: 네이버/쿠팡/카카오 상세페이지는 `product-detail` 스킬을 사용하세요.
- **데이터 대시보드**: 차트·KPI 중심 화면은 `data-visualizer` 스킬을 사용하세요.
- **멀티 페이지 웹사이트**: 전체 웹사이트 설계는 별도 웹 에이전트나 개발자가 필요합니다.
