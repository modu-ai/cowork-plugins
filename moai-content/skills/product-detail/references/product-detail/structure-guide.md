# 상세 페이지 구조 및 디자인 시스템 가이드

## 1. 기본 레이아웃

### 데스크톱 레이아웃 (1024px 이상)

```
+------------------------------------------------------------------+
| [로고]          [검색바]           [장바구니] [마이페이지]         |
+------------------------------------------------------------------+
|                                                                    |
|  +---------------------------+  +------------------------------+  |
|  |                           |  | 브랜드명                     |  |
|  |    이미지 갤러리           |  | 제품명 (H1)                  |  |
|  |    (메인 이미지)           |  | ★★★★★ 4.8 (3,241)          |  |
|  |                           |  |                              |  |
|  |    [썸네일] [썸네일] [영상] |  | ₩89,900  ~~₩129,000~~  30% |  |
|  |                           |  |                              |  |
|  +---------------------------+  | [옵션 선택 드롭다운]         |  |
|                                 | [수량 선택]                  |  |
|                                 |                              |  |
|                                 | [장바구니 담기] [바로구매]   |  |
|                                 +------------------------------+  |
|                                                                    |
+------------------------------------------------------------------+
| [상세정보]  [후기 3,241]  [FAQ]                                   |
+------------------------------------------------------------------+
|                                                                    |
|                    상세정보 콘텐츠 영역                            |
|              (이미지 기반 스크롤 콘텐츠)                          |
|                                                                    |
+------------------------------------------------------------------+
|                    관련 제품 추천 그리드                           |
|   [제품1]  [제품2]  [제품3]  [제품4]                              |
+------------------------------------------------------------------+
|                    최종 CTA 배너                                  |
|          "지금 주문하면 내일 도착"  [바로 구매하기]               |
+------------------------------------------------------------------+
```

### 모바일 레이아웃 (375px 기준)

```
+---------------------------+
| [뒤로] [검색] [장바구니]  |
+---------------------------+
|                           |
|   이미지 갤러리 (스와이프) |
|   [● ○ ○ ○ ○]           |
|                           |
+---------------------------+
| 브랜드명                  |
| 제품명 (H1)              |
| ★★★★★ 4.8 (3,241)      |
| ₩89,900  ~~₩129,000~~ 30%|
+---------------------------+
| [옵션 선택]              |
| [수량: - 1 +]            |
+---------------------------+
| [상세] [후기] [FAQ]      |
+---------------------------+
|                           |
|   숏폼 스타일 상세정보    |
|   (1스크롤 1메시지)       |
|                           |
+---------------------------+
| 관련 제품 (가로 스크롤)   |
+---------------------------+
|                           |
| 하단 고정 CTA 바          |
| [장바구니] [바로구매]     |
+---------------------------+
```

---

## 2. 필수 섹션 상세 (8개)

### 섹션 1: 히어로/메인 이미지 갤러리

목적: 제품의 첫인상을 결정한다. 3초 내에 시각적으로 제품을 이해시킨다.

이미지 규격:
- 메인 이미지: 정사각형 (860x860px 스마트스토어 / 780x780px 쿠팡)
- 서브 이미지: 최소 5장 (정면, 후면, 측면, 디테일, 사용 장면)
- 포맷: WebP 우선, JPEG 폴백 (각 500KB 이하)
- 배경: 순백(#FFFFFF) 또는 라이트그레이(#F5F5F5)

동영상:
- 30초 이내 제품 소개 영상 (자동 재생 금지, 음소거 기본)
- 썸네일에 재생 아이콘 표시
- MP4 포맷, 10MB 이하

갤러리 동작:
- 데스크톱: 메인 이미지 + 하단 썸네일 네비게이션
- 모바일: 좌우 스와이프 + 인디케이터 점
- 줌: 데스크톱 호버 시 2배 확대, 모바일 핀치 투 줌
- 이미지 전환: 0.3초 페이드 또는 슬라이드 트랜지션

금지 사항:
- 텍스트가 과도하게 삽입된 이미지 (가독성 저하)
- 워터마크가 제품을 가리는 배치
- 저해상도 이미지 (최소 600x600px)
- 자동 재생 동영상 (사용자 경험 저하, 데이터 소모)

### 섹션 2: 제품 기본 정보

목적: 구매 결정에 필요한 핵심 정보를 한눈에 전달한다.

필수 요소:
- 브랜드명 (링크 연결)
- 제품명 (H1 태그, 60자 이내)
- 평점 + 리뷰 수 (별점 시각화 + 숫자)
- 판매가: 큰 폰트(28-36px), 볼드, Primary 색상
- 정가: 작은 폰트, 취소선, 회색 처리
- 할인율: 빨강 배경 배지 또는 빨강 텍스트
- 적립금/포인트 (해당 시)
- 배송 정보: 무료배송 여부, 예상 도착일

옵션 선택:
- 드롭다운 또는 버튼 그룹 (색상은 원형 스와치)
- 선택 시 가격 변동 즉시 반영
- 품절 옵션은 비활성화 + 취소선 처리
- 수량 선택: +/- 버튼 (최소 1, 최대 재고 수량)

CTA 버튼:
- 장바구니 담기: Secondary (테두리 버튼, 48px 높이)
- 바로 구매하기: Primary (채워진 버튼, 48px 높이, 굵은 글씨)
- 찜하기: 아이콘 버튼 (하트)
- 모바일: 하단 고정 바로 배치 (스크롤 시에도 항상 노출)

### 섹션 3: 탭 메뉴

목적: 상세정보, 후기, FAQ를 탭으로 분리하여 탐색 편의를 제공한다.

구현 규칙:
- 탭 3개 고정: [상세정보] [후기(건수)] [FAQ]
- 후기 탭에 리뷰 건수 표시 (예: "후기 3,241")
- 스티키 탭: 스크롤 시 상단에 고정 (position: sticky)
- 활성 탭: Primary 색상 밑줄 + 볼드 처리
- 비활성 탭: 회색 텍스트
- 탭 전환 시 스크롤 위치 유지 (페이지 점프 금지)
- 모바일: 탭 전체 폭 균등 분할 (33.33%)

접근성:
- role="tablist", role="tab", role="tabpanel" 적용
- aria-selected="true/false" 상태 관리
- 키보드 좌우 화살표로 탭 이동

### 섹션 4: 상세정보 탭

목적: 제품의 기능, 스펙, 정책을 상세히 전달한다. 가장 긴 섹션이다.

구성 순서:
```
4-1. 핵심 메시지 (숏폼 스타일, 1스크롤 1메시지)
4-2. 기능 목록 (아이콘 + 제목 + 설명)
4-3. 스펙 테이블 (2컬럼: 항목-값)
4-4. 사용 방법 / 성분표 (해당 시)
4-5. 배송 정보
4-6. 교환/반품 정책
4-7. 법적 필수 표기 (원산지, 제조사, 유통기한 등)
```

숏폼 스타일 상세 (2026 트렌드):
- 1스크롤 = 1메시지 원칙
- 각 메시지는 이미지(70%) + 텍스트(30%) 구성
- 텍스트는 2-3줄 이내 (모바일 기준)
- 배경색을 번갈아 사용하여 섹션 구분 (#FFFFFF / #F8F8F8)
- 숫자 강조: 핵심 수치를 48px 이상 큰 폰트로 표시

스펙 테이블:
- 짝수/홀수 행 배경색 구분
- 항목명: 볼드, 회색 배경
- 값: 기본 폰트
- 모바일: 2컬럼 유지 (항목 폭 40%, 값 폭 60%)

법적 필수 표기:
- 전자상거래법에 따른 상품 정보 고시
- 식품: 원재료, 영양정보, 유통기한, 보관방법
- 화장품: 전성분, 사용기한, 기능성 인증번호
- 전자제품: KC인증, 소비전력, A/S 정보

### 섹션 5: 후기 섹션

목적: 사회적 증명을 통해 구매 확신을 제공한다.

구성 요소:
- 평균 평점 (큰 숫자 + 별점)
- 평점 분포 바 차트 (5점-1점)
- 총 리뷰 수
- 필터: 전체 / 포토후기 / 별점별
- 정렬: 최신순 / 평점높은순 / 도움순

개별 후기 카드:
- 작성자명 (마스킹: 홍*동)
- 별점 (1-5)
- 작성일
- 구매 옵션 표시
- 후기 텍스트
- 후기 이미지 (있는 경우, 썸네일 3장까지)
- 도움됐어요 버튼 + 카운트

이미지 후기 강조:
- 상단에 "포토 후기" 가로 스크롤 갤러리 배치
- 이미지 클릭 시 라이트박스로 확대
- 포토 후기가 텍스트 후기보다 상위 노출

### 섹션 6: FAQ 아코디언

목적: 구매 전 의문점을 사전 해소하여 이탈을 방지한다.

필수 질문 카테고리 (최소 5개):
- 배송: "배송은 얼마나 걸리나요?"
- 교환/반품: "교환/반품 절차는 어떻게 되나요?"
- 제품 관련: "~와 호환되나요?" / "세척은 어떻게 하나요?"
- 가격/결제: "추가 비용이 있나요?"
- 보증: "A/S 기간은 얼마인가요?"

구현 규칙:
- 한 번에 하나만 열리는 아코디언 (배타적 열기)
- 열기/닫기 아이콘: + / - 또는 화살표
- 트랜지션: 0.3초 슬라이드다운
- 닫힌 상태: 질문만 표시 (한 줄)
- 열린 상태: 질문 + 답변 (답변에 링크 가능)
- 접근성: aria-expanded="true/false" 상태 관리

### 섹션 7: 관련 제품 추천

목적: 교차 판매(Cross-sell) 및 상향 판매(Up-sell)를 유도한다.

구성:
- 제목: "이 제품과 함께 많이 구매한 상품" 또는 "비슷한 상품"
- 카드 4개 (데스크톱), 2열 또는 가로 스크롤 (모바일)
- 카드 구성: 이미지 + 제품명 + 가격 + 평점

배치 규칙:
- 같은 카테고리 내 제품 우선
- 가격대가 유사한 제품 (현재 상품의 80-120%)
- 번들 제품이 있으면 "함께 구매 시 할인" 배너 추가

### 섹션 8: 최종 CTA

목적: 페이지 하단까지 스크롤한 사용자에게 마지막 전환 기회를 제공한다.

구성:
- 배경: Primary 색상 또는 그라데이션
- 헤드라인: 긴급성 메시지 ("지금 주문하면 내일 도착")
- 혜택 요약: 불릿 3개 이내
- CTA 버튼: 큰 사이즈 (56px 높이), 흰색 텍스트
- 보증 문구: "100% 환불 보증" / "무료 배송"

모바일 하단 고정 바:
- 높이 60px, 화면 하단 고정
- 구성: [장바구니 담기 (40%)] [바로 구매하기 (60%)]
- 배경: 흰색 + 상단 그림자
- 스크롤 시에도 항상 노출
- 상세정보 섹션 도달 전까지는 숨김 (상단에서는 비노출)

---

## 3. 모바일 반응형 규칙

### 브레이크포인트

```css
/* 모바일 (기본) */
/* 375px ~ 767px */

/* 태블릿 */
@media (min-width: 768px) { ... }

/* 데스크톱 */
@media (min-width: 1024px) { ... }

/* 대형 데스크톱 */
@media (min-width: 1440px) { ... }
```

### 모바일 우선 규칙

- 터치 타겟: 최소 44x44px (iOS HIG 기준)
- 좌우 패딩: 16px
- 섹션 간 간격: 24px
- 폰트 최소 크기: 14px (본문), 12px (캡션)
- 이미지: width: 100%, aspect-ratio 유지
- 가로 스크롤: 이미지 갤러리, 관련 제품에만 허용
- 세로 스크롤: 무한 스크롤 금지, 페이지네이션 사용

### 숏폼 스타일 섹션 (2026 트렌드)

- 각 섹션 높이: 100vh 또는 auto (콘텐츠에 따라)
- 한 화면에 하나의 핵심 메시지만 표시
- 스크롤 스냅: scroll-snap-type: y mandatory
- 배경 색상 번갈아 사용
- 텍스트 애니메이션: 스크롤 시 페이드인 (IntersectionObserver)
- 숫자 카운트업 애니메이션 (성능 지표 강조 시)

---

## 4. 디자인 시스템

### 색상 체계

```css
:root {
  /* Primary: 브랜드 메인 (CTA, 강조) */
  --color-primary: #FF6B35;
  --color-primary-hover: #E55A2B;
  --color-primary-light: #FFF3EE;

  /* Accent: 할인, 배지, 긴급성 */
  --color-accent: #FF0000;
  --color-accent-light: #FFF0F0;

  /* Neutral: 배경, 텍스트, 테두리 */
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #F8F8F8;
  --color-bg-tertiary: #F0F0F0;
  --color-text-primary: #1A1A1A;
  --color-text-secondary: #666666;
  --color-text-tertiary: #999999;
  --color-border: #E0E0E0;

  /* Semantic: 상태 표시 */
  --color-success: #00B894;
  --color-warning: #FDCB6E;
  --color-error: #E17055;
  --color-info: #74B9FF;

  /* 평점 */
  --color-star: #FFD700;
  --color-star-empty: #E0E0E0;
}
```

사용 규칙:
- CTA 버튼: `--color-primary` 배경 + 흰색 텍스트
- 할인가/배지: `--color-accent`
- 본문 텍스트: `--color-text-primary`
- 보조 텍스트: `--color-text-secondary`
- 배경 교차: `--color-bg-primary` / `--color-bg-secondary` 번갈아 사용

### 타이포그래피

```css
/* Pretendard 폰트 (한글 최적화) */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
  --font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;

  /* 폰트 크기 */
  --font-xs: 12px;     /* 캡션, 법적 표기 */
  --font-sm: 14px;     /* 보조 텍스트, 옵션 */
  --font-base: 16px;   /* 본문 */
  --font-lg: 18px;     /* 서브 제목 */
  --font-xl: 24px;     /* 섹션 제목 */
  --font-2xl: 32px;    /* 제품명 */
  --font-3xl: 36px;    /* 가격 */
  --font-4xl: 48px;    /* 숫자 강조 (숏폼) */

  /* 줄 높이 */
  --line-height-tight: 1.3;   /* 제목 */
  --line-height-normal: 1.6;  /* 본문 */
  --line-height-loose: 1.8;   /* 상세 설명 */

  /* 폰트 굵기 */
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
}
```

적용 규칙:
- 제품명(H1): `--font-2xl`, `--font-weight-bold`, `--line-height-tight`
- 가격: `--font-3xl`, `--font-weight-extrabold`, `--color-primary`
- 할인가(정가): `--font-lg`, `--font-weight-regular`, 취소선, 회색
- 섹션 제목: `--font-xl`, `--font-weight-bold`
- 본문: `--font-base`, `--font-weight-regular`, `--line-height-normal`
- 버튼 텍스트: `--font-base`, `--font-weight-semibold`

### 버튼 스타일

```css
/* Primary 버튼 (바로 구매하기) */
.btn-primary {
  background: var(--color-primary);
  color: #FFFFFF;
  font-size: var(--font-base);
  font-weight: var(--font-weight-semibold);
  height: 48px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}
.btn-primary:hover {
  background: var(--color-primary-hover);
}

/* Secondary 버튼 (장바구니 담기) */
.btn-secondary {
  background: var(--color-bg-primary);
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  height: 48px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.btn-secondary:hover {
  background: var(--color-primary-light);
}
```

### 간격 체계

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
}
```

적용 규칙:
- 섹션 간: `--space-2xl` (48px)
- 요소 간: `--space-md` (16px)
- 카드 내부: `--space-md` (16px)
- 버튼 내부: `--space-sm` (8px) 상하, `--space-lg` (24px) 좌우

---

## 5. SEO 및 구조화 데이터

### 메타태그

```html
<title>제품명 | 브랜드명 - 핵심 키워드</title>
<meta name="description" content="60~160자 제품 설명 (핵심 benefit 포함)">
<meta name="keywords" content="키워드1, 키워드2, 키워드3">

<!-- Open Graph -->
<meta property="og:type" content="product">
<meta property="og:title" content="제품명">
<meta property="og:description" content="제품 설명">
<meta property="og:image" content="메인 이미지 URL">
<meta property="og:url" content="제품 URL">
<meta property="product:price:amount" content="89900">
<meta property="product:price:currency" content="KRW">
```

### Schema.org Product (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "제품명",
  "image": ["이미지URL1", "이미지URL2"],
  "description": "제품 설명",
  "brand": {
    "@type": "Brand",
    "name": "브랜드명"
  },
  "offers": {
    "@type": "Offer",
    "url": "제품 URL",
    "priceCurrency": "KRW",
    "price": "89900",
    "availability": "https://schema.org/InStock",
    "seller": {
      "@type": "Organization",
      "name": "판매자명"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "3241"
  }
}
```

---

## 6. 접근성 규칙 (WCAG AA)

필수 준수 항목:
- 색상 대비: 텍스트/배경 명도 대비 4.5:1 이상
- 이미지 대체 텍스트: 모든 제품 이미지에 alt 속성 필수
- 키보드 탐색: Tab키로 모든 인터랙션 접근 가능
- 포커스 표시: 포커스 시 2px 아웃라인 (Primary 색상)
- ARIA 레이블: 아이콘 버튼에 aria-label 필수
- 탭 메뉴: role="tablist" / role="tab" / role="tabpanel"
- 아코디언: aria-expanded / aria-controls
- 라이브 영역: 가격 변동 시 aria-live="polite"
- 스크린리더: 할인율은 "30% 할인"으로 읽히도록 aria-label 설정

---

## 7. 성능 최적화

이미지:
- WebP 포맷 우선 (JPEG 대비 25-30% 용량 절감)
- 레이지 로딩: loading="lazy" (첫 화면 이미지 제외)
- srcset 반응형 이미지 (375w, 768w, 1024w)
- 이미지 CDN 사용 권장 (CloudFront, imgix 등)

코드:
- CSS: 크리티컬 CSS 인라인 + 나머지 비동기 로드
- JavaScript: 100KB 이하 번들 (미니파이 + 트리쉐이킹)
- 폰트: font-display: swap (FOIT 방지)
- 서드파티: GTM, GA4는 비동기 로드

측정 기준:
- LCP(Largest Contentful Paint): 2.5초 이내
- FID(First Input Delay): 100ms 이내
- CLS(Cumulative Layout Shift): 0.1 이하
- Lighthouse Performance: 80점 이상

---

## 8. 출력 구조

### HTML 패키지 (스마트스토어/쿠팡 업로드용)

```
product-detail/
  index.html          -- 전체 HTML (인라인 CSS/JS 포함)
  images/
    main-01.webp      -- 메인 이미지
    main-02.webp      -- 서브 이미지
    detail-01.webp    -- 상세 이미지
    detail-02.webp    -- 상세 이미지
  style.css           -- 스타일시트 (자사몰용)
  script.js           -- 인터랙션 (자사몰용)
```

스마트스토어/쿠팡 업로드 시:
- HTML + CSS를 하나의 파일로 인라인 처리
- JavaScript는 최소화 (플랫폼 에디터 제약)
- 이미지는 별도 업로드 후 URL 교체

### React/Next.js 출력 구조

```
components/
  ProductDetail/
    ProductDetail.tsx       -- 메인 컨테이너
    ProductImage.tsx        -- 이미지 갤러리
    ProductInfo.tsx         -- 기본 정보 + CTA
    TabMenu.tsx             -- 탭 메뉴
    DetailTab.tsx           -- 상세정보 탭
    ReviewSection.tsx       -- 후기 섹션
    FAQAccordion.tsx        -- FAQ 아코디언
    RelatedProducts.tsx     -- 관련 제품
    FinalCTA.tsx            -- 최종 CTA
    MobileBottomBar.tsx     -- 모바일 하단 고정 바
    product-detail.module.css  -- CSS 모듈
    types.ts                -- 타입 정의
```
