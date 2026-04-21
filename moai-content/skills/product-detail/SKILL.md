---
name: product-detail
description: >
  shadcn/ui 기반 제품·서비스 상세 페이지를 전환율 극대화 전략으로 설계·생성하는 스킬입니다.
  "상세페이지 만들어줘", "제품 페이지 기획", "쇼핑몰 상세 설계", "상세페이지 디자인" 등
  전자상거래 및 SaaS 제품의 상세 페이지 제작 요청 시 사용합니다.
  코드 생성 전에 소크라테스식 테마 인터뷰(베이스 팔레트·컬러 모드·모서리 반경·효과)를
  먼저 묻고, 네이버 스마트스토어/쿠팡/카카오 커머스 규격에 맞춰 HTML 또는
  Next.js+shadcn/ui React 컴포넌트를 산출합니다.
  블로그 글, SNS 포스팅, 랜딩 페이지(단독 전환 목적)에는 이 스킬을 사용하지 마세요.
user-invocable: true
---

# 상세 페이지 (Product Detail)

> moai-content | shadcn/ui 기반 제품/서비스 상세 페이지 전문 스킬 · v1.4.0에서 shadcn/ui 기본 스택 전환

## 지원 영역

- 이커머스 상세 페이지 설계 (네이버 스마트스토어, 쿠팡, 카카오 커머스)
- SaaS 제품 상세 페이지 (가격 플랜, 기능 비교, 데모 CTA)
- 서비스 소개 페이지 (컨설팅, 교육, 구독 서비스)
- 모바일 퍼스트 상세 페이지 (375px 기준 숏폼 스타일)
- 전환율 최적화 카피 + 디자인 시스템 + HTML/React 코드 생성
- shadcn/ui 컴포넌트 기반 테마 일관성 (Light/Dark 동시 산출)

## 기본 스택 (v1.4.0)

| 레이어 | 기본값 | 비고 |
|--------|-------|------|
| 자사몰·SaaS | Next.js 15 + Tailwind v4 + shadcn/ui | Radix 접근성 자동 확보 |
| 스마트스토어·쿠팡 | 단일 HTML + Tailwind CDN + shadcn CSS 변수 | 플랫폼 업로드 규격 준수 |
| 아이콘 | Lucide React | 또는 SVG inline |
| 차트(가격 비교 등) | Recharts | 인터뷰 Q5에서 선택 시 |

## 레퍼런스 가이드

- `../landing-page/references/landing-page/shadcn-theme-interview.md` — **[v1.4.0 신규] shadcn 테마 인터뷰 프로토콜 (공용 레퍼런스)**
- `references/product-detail/structure-guide.md` -- 페이지 구조 및 디자인 시스템 가이드
- `references/product-detail/conversion-formulas.md` -- 전환율 극대화 공식 및 체크리스트
- `references/product-detail/platform-specs.md` -- 플랫폼별 규격 (스마트스토어, 쿠팡, 카카오)
- `references/product-detail/section-templates.md` -- 섹션별 HTML/React 템플릿

## 트리거 키워드

상세페이지, 제품 페이지, 상세 설계, 쇼핑몰 상세, 제품 상세, 스마트스토어 상세, 쿠팡 상세, 카카오 상세, 상품 설명, 제품 소개 페이지, 상세 기획, 제품 기획, 상품 페이지, 상세 디자인, 제품 설명 페이지

## 사용 예시

- "스마트스토어 가습기 상세페이지 만들어줘"
- "쿠팡에 올릴 화장품 상세 페이지 기획해줘"
- "SaaS 제품 상세 페이지 React로 만들어줘"
- "카카오 선물하기용 상품 상세 설계해줘"
- "건강식품 상세페이지 카피 + 디자인 + 코드 전부 만들어줘"
- "기존 상세페이지 전환율 개선해줘"
- "모바일 전용 상세페이지 숏폼 스타일로 만들어줘"

## 독립 실행 워크플로우

참조 가이드(`references/`)를 사용할 수 없는 경우 다음 단계로 실행한다.

### [HARD] 0단계: shadcn 테마 인터뷰

코드·디자인 스펙 산출 **직전에 반드시 수행**한다. MoAI 오케스트레이터가 `AskUserQuestion`으로 다음 4개 질문을 한 번에 제시한다.

1. **Q1 베이스 팔레트** — Neutral(기본) / Zinc / Stone / Slate
2. **Q2 컬러 모드** — System+Toggle(기본) / Light / Dark / Auto
3. **Q3 모서리 반경** — Balanced 0.5rem(기본) / Sharp / Soft / Pill
4. **Q4 효과(multiSelect)** — Fade-up / Scroll Reveal / Parallax / Chart

Q4에서 `Chart`가 선택되면(가격 비교 차트·스펙 비교 등) Q5(Recharts/Chart.js/Tremor/ECharts)를 추가 호출한다.

상세 설계·예외 처리는 `../landing-page/references/landing-page/shadcn-theme-interview.md` 참조.

Fallback(인터뷰 생략) 기본값: `Neutral + System+Toggle + 0.5rem + Fade-up`. 적용 시 응답 상단에 고지한다.

플랫폼별 기본값 조정:
- 네이버 스마트스토어·쿠팡: 단일 HTML 모드로 산출하되 shadcn CSS 변수는 인라인으로 주입
- 자사몰·SaaS: Next.js + shadcn/ui 전체 스택 기본 적용

### 사전 수집: 제품 정보 체크리스트

작업 시작 전 아래 항목을 확인한다. 미제공 항목은 일반 베스트 프랙티스를 적용한다.

필수 항목:
- [ ] 제품/서비스명
- [ ] 카테고리 (뷰티, 전자제품, 식품, 의류, SaaS 등)
- [ ] 핵심 셀링 포인트 3가지 (Feature-Advantage-Benefit)
- [ ] 가격 및 할인 정보
- [ ] 타겟 고객 (연령, 성별, 라이프스타일)
- [ ] 판매 플랫폼 (스마트스토어, 쿠팡, 카카오, 자사몰)

권장 항목:
- [ ] 제품 이미지 (메인, 상세, 사용 장면)
- [ ] 고객 후기/평점 데이터
- [ ] 경쟁 제품 대비 차별점
- [ ] 배송/반품 정책
- [ ] 인증/수상 내역
- [ ] 브랜드 컬러 및 폰트 가이드

### 1단계: 제품 분석 및 타겟 파악

제품 분석:
- 카테고리별 업계 평균 전환율 확인 (뷰티 1.5~2.5%, 전자 0.8~1.5%)
- FAB(Feature-Advantage-Benefit) 변환표 작성
- 경쟁 제품 대비 차별화 포인트 3가지 도출

타겟 분석:
- 페르소나 1개 정의 (이름, 나이, 직업, 고통점)
- 구매 결정 요인 우선순위 (가격/품질/브랜드/후기/배송)
- 구매 여정에서 가장 높은 이탈 지점 파악

### 2단계: 페이지 구조 설계

2026 트렌드를 반영한 구조를 설계한다:
- 숏폼 스타일: 1스크롤 1메시지 원칙 (한 화면에 하나의 핵심 메시지만 배치)
- 모바일 퍼스트: 375px 기준 설계 후 데스크톱 확장
- 동영상 우선: 제품 소개 30초 영상을 히어로에 배치
- 인터랙티브 요소: 360도 제품 뷰, 터치 스와이프 갤러리

필수 섹션 8개:
```
[1] 히어로/메인 이미지 갤러리 (제품 사진 + 영상)
[2] 제품 기본 정보 (가격, 재고, 평점, 옵션 선택)
[3] 탭 메뉴 (상세정보 | 후기 | FAQ)
[4] 상세정보 탭 (기능 목록, 스펙 테이블, 배송/반품)
[5] 후기 섹션 (평점 분포, 필터, 이미지 후기)
[6] FAQ 아코디언
[7] 관련 제품 추천
[8] 최종 CTA (장바구니 + 바로구매)
```

상세 구조: `references/product-detail/structure-guide.md`

### 3단계: 섹션별 카피 작성

AIDA 공식 적용:
- Attention(0~3초): 숫자/형용사 + 핵심 benefit 헤더
- Interest(3~15초): 고객 pain point 공감 + 해결책 제시
- Desire(15~40초): 5감 시나리오 + 라이프스타일 연결
- Action(40~60초): 긴급성 + 사회적 증명 + CTA

FAB 공식 적용:
- 모든 기능(Feature)을 이점(Advantage)으로 변환
- 모든 이점을 고객 혜택(Benefit)으로 변환
- 혜택 중심으로 카피 작성 (기능 나열 금지)

심리 트리거 체크리스트:
- [ ] 스카시티(한정성): 수량/시간 제한 표시
- [ ] 사회적 증명: 판매량, 평점, 전문가 추천
- [ ] 긴급성: 카운트다운, 재고 경고
- [ ] 권위성: 인증, 수상, 특허
- [ ] 가격 심리: 앵커링, 손실회피

상세 공식: `references/product-detail/conversion-formulas.md`

### 4단계: 디자인 시스템 정의 (shadcn 토큰 기반)

색상 (shadcn OKLCH 변수 매핑):
- `--primary` → CTA 버튼, 구매 유도 지점 (0단계 Q1 선택 base 기반)
- `--destructive` → 할인율·한정수량 배지 (빨강 계열 oklch)
- `--muted-foreground` → 보조 정보 (평점 텍스트, 배송 안내)
- `--background` / `--card` → 섹션 배경 위계
- 브랜드 컬러 오버라이드 시 `--primary`, `--accent`, `--ring`만 교체

폰트:
- 본문: Pretendard 400 (16px/1.6)
- 제목: Pretendard 700 (24~32px)
- 가격: Pretendard 800 (28~36px, `--primary` 색상)
- 할인가: `line-through` + `text-muted-foreground`

레이아웃:
- 모바일: 1컬럼, 좌우 패딩 16px
- 태블릿(768px~): 2컬럼 그리드
- 데스크톱(1024px~): 최대 860px 콘텐츠 영역 (스마트스토어 기준)

컴포넌트 매핑:
- 옵션 선택 → shadcn `Select` 또는 `ToggleGroup`
- 탭 메뉴 → shadcn `Tabs`
- 후기 카드 → shadcn `Card` + `Avatar` + `StarRating`
- FAQ → shadcn `Accordion`
- 장바구니/바로구매 → shadcn `Button` (variant: default / secondary)
- 배지 → shadcn `Badge` (variant: destructive for 할인)

### 5단계: 코드 생성

출력 형식 선택:
- **HTML 패키지**(스마트스토어/쿠팡 업로드용): `index.html` + `style.css`(shadcn CSS 변수 인라인) + `script.js`
- **React/Next.js**(자사몰/SaaS): 컴포넌트 분리 (ProductImage, ProductInfo, TabMenu, Reviews, FAQ) + `components.json` + `app/globals.css`

플랫폼별 규격 적용:
- 스마트스토어: 860px 폭, 이미지 기반 상세 (HTML 모드)
- 쿠팡: 780px 폭, 최대 9장 이미지 (HTML 모드)
- 카카오: 모바일 최적화, 375px 기준
- 자사몰: 반응형 자유 설계 (Next.js + shadcn 모드)

상세 규격: `references/product-detail/platform-specs.md`
코드 템플릿: `references/product-detail/section-templates.md`

### 6단계: QA 체크리스트

기능 검증:
- [ ] 이미지 갤러리 스와이프/줌 정상 작동
- [ ] 옵션 선택 시 가격 변동 반영
- [ ] 탭 전환 정상 작동
- [ ] FAQ 아코디언 열기/닫기
- [ ] CTA 버튼 클릭 이벤트 연결
- [ ] 모든 링크 정상 작동 (404 없음)

반응형 검증:
- [ ] 모바일(375px) 레이아웃 정상
- [ ] 태블릿(768px) 레이아웃 정상
- [ ] 데스크톱(1280px) 레이아웃 정상
- [ ] CTA 버튼이 모든 해상도에서 가시적

성능 검증:
- [ ] 이미지 전체 용량 2MB 이하
- [ ] 개별 이미지 500KB 이하
- [ ] JavaScript 번들 100KB 이하
- [ ] Lighthouse Performance >= 80
- [ ] Lighthouse Accessibility >= 80
- [ ] WebP 포맷 사용 여부

콘텐츠 검증:
- [ ] 카피 무결성 (원본 대비 변경 없음)
- [ ] 오탈자 없음
- [ ] 가격 정보 정확성
- [ ] 법적 필수 표기 포함 (원산지, 제조사, 유통기한 등)
- [ ] 과대광고 표현 없음 (식약법, 의료법 준수)

## 플랫폼별 규격 요약

| 플랫폼 | 이미지 폭 | 메인 이미지 | 최대 이미지 수 | 특이사항 |
|--------|----------|-----------|--------------|---------|
| 스마트스토어 | 860px | 860x860px | 제한 없음 | 이미지 기반 상세, SEO 중요 |
| 쿠팡 | 780px | 780x780px | 9장 | 로켓배송 뱃지, 검색 알고리즘 |
| 카카오 | 375px | 750x750px | 제한 없음 | 선물하기 규격, 모바일 전용 |
| 자사몰 | 자유 | 자유 | 자유 | 반응형 필수, Schema.org |

상세 규격: `references/product-detail/platform-specs.md`

## 카피 출력 형식 (JSON 구조)

카피 작성 결과는 구조화된 형식으로 산출한다. 0단계 인터뷰 결과는 `theme` 블록에 포함한다.

```json
{
  "page_type": "product-detail",
  "platform": "smartstore|coupang|kakao|custom",
  "theme": {
    "system": "shadcn/ui",
    "base": "neutral",
    "mode": "system+toggle",
    "radius": "0.5rem",
    "effects": ["fade-up"],
    "chart_lib": null
  },
  "sections": [
    {
      "id": "hero",
      "headline": "10시간 지속 가습으로 아침 피부 촉촉",
      "subheadline": "초음파식 4.5L 대용량 가습기",
      "visual_direction": "제품 정면 + 미스트 연출 이미지"
    },
    {
      "id": "product-info",
      "price": "89,900",
      "original_price": "129,000",
      "discount_rate": "30%",
      "rating": "4.8",
      "review_count": "3,241",
      "options": ["화이트", "그레이", "민트"],
      "badges": ["무료배송", "당일출고"]
    },
    {
      "id": "detail-tab",
      "features": [
        {
          "feature": "초음파식 가습",
          "advantage": "전기료 월 3,000원",
          "benefit": "경제적으로 밤새 사용"
        }
      ],
      "specs_table": {},
      "shipping_info": "주문 후 1~2일 내 출고"
    },
    {
      "id": "reviews",
      "highlight_reviews": [],
      "rating_distribution": {}
    },
    {
      "id": "faq",
      "items": [
        {"q": "세척은 어떻게 하나요?", "a": "분리형 설계로 간편 세척"}
      ]
    },
    {
      "id": "related-products",
      "items": []
    },
    {
      "id": "final-cta",
      "headline": "지금 주문하면 내일 도착",
      "cta_primary": "장바구니 담기",
      "cta_secondary": "바로 구매하기",
      "urgency": "남은 재고 23개"
    }
  ],
  "metadata": {
    "tone_profile": "신뢰+실용",
    "reading_level": "고교",
    "word_count": 0,
    "image_count": 0,
    "target_platform": "smartstore"
  }
}
```

## 핵심 규칙: 카피 무결성

디자인/개발 단계에서 카피 텍스트를 수정하지 않는다.
- 원본 카피를 그대로 구현한다
- 텍스트 수정이 필요하면 카피 작성 단계(3단계)로 반려한다
- 줄바꿈, 강조, 순서 변경만 허용한다 (내용 변경 금지)

## 실행 규칙

1. 사용자 요청 수신 -- 상세 페이지 요청 확인
2. `references/product-detail/` 존재 시 로드 -- 가이드에 따라 실행
3. 판매 플랫폼 미지정 시 사용자에게 확인 (스마트스토어/쿠팡/카카오/자사몰)
4. **shadcn 테마 인터뷰 실행** (0단계, HARD) -- 코드 산출 직전
5. 제품 정보 체크리스트 확인 -- 필수 항목 미제공 시 질문
6. `--deepthink` 또는 복잡 작업 -- `mcp__sequential-thinking__sequentialthinking` 호출
7. 결과물 생성 후 `ai-slop-reviewer`로 카피 검수 (텍스트 산출물 한정)
8. 사용자 검토 요청

주의: AI가 생성한 상세 페이지 카피에 포함된 판매량, 평점, 고객 후기 등 실증적 주장은 반드시 실제 데이터로 교체한다. 허위 수치를 그대로 사용하면 전자상거래법 및 표시광고법 위반에 해당한다.

## 이 스킬을 사용하지 말아야 할 때

- **블로그 포스팅/리뷰 글**: SEO 블로그 글 작성은 `blog` 스킬이 더 적합하다.
- **SNS 포스팅**: 소셜미디어 콘텐츠는 `social-media` 스킬을 사용한다.
- **랜딩 페이지**: 리드 수집, 앱 다운로드 등 단독 전환 목적 페이지는 `landing-page` 스킬을 사용한다.
- **광고 카피 단독 작성**: 헤드라인/슬로건만 필요한 경우 `copywriting` 스킬이 더 적합하다.
- **카탈로그/리스트 페이지**: 다수 상품 목록 페이지는 이 스킬의 범위가 아니다.

## 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| 이미지가 플랫폼 규격 초과 | 해상도/용량 미확인 | `platform-specs.md` 참조, 이미지 리사이즈 |
| 모바일에서 레이아웃 깨짐 | 고정 폭 사용 | max-width + 퍼센트 기반 레이아웃 적용 |
| 전환율이 업계 평균 이하 | CTA 위치/문구 미최적화 | `conversion-formulas.md`의 A/B 테스트 항목 순서대로 개선 |
| 과대광고 경고 | 식약법/의료법 위반 표현 | `platform-specs.md`의 금지 표현 체크리스트 확인 |
| 페이지 로딩 느림 | 이미지 미최적화 | WebP 변환, 레이지 로딩, 500KB 이하/장 |
| 스마트스토어 SEO 미노출 | 키워드 전략 부재 | `platform-specs.md`의 카테고리 키워드 전략 적용 |
| React 컴포넌트 에러 | 상태 관리 누락 | `section-templates.md`의 React 템플릿 참조 |
| 탭 메뉴 미작동 | JavaScript 미연결 | `section-templates.md`의 탭 컴포넌트 코드 확인 |
