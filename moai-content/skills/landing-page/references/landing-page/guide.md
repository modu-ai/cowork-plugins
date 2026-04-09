# 랜딩 페이지 빌더 (Landing Page Builder)

반응형 매력적인 랜딩 페이지를 AI와 함께 디자인하고 배포하는 스킬입니다.

## Overview

사용자의 프로덕트, 서비스, 캠페인을 대표하는 고성능 랜딩 페이지를 빠르게 제작합니다.
**SEO 최적화**, **모바일 반응형**, **전환율(CTA) 최적화**, **폴더 구조**까지 완성된 결과물을 제공합니다.

> **핵심**: 비개발자도 "초대형 배너가 있는 프로덕트 페이지 만들어줘"라고 말하면, 
> 바로 배포 가능한 Next.js 또는 HTML 코드를 받을 수 있어야 합니다.

---

## 지원 랜딩 페이지 유형

### 1. Product Launch (제품 출시)
```
특징:
- 히어로 섹션: 큰 텍스트 + CTA 버튼
- Feature Showcase: 3~4개 주요 기능 카드
- Testimonials: 사용자 후기
- Pricing: 가격표 또는 요금제
- FAQ: 자주 묻는 질문
- CTA Footer: 최종 행동 유도

최적 길이: 스크롤 1~2분 (Long-form)
타겟: B2C 제품, SaaS
```

### 2. Event/Webinar Signup
```
특징:
- 임팩트 있는 이벤트 타이틀
- 날짜/시간/장소 강조
- 연사/게스트 소개
- 일정 (Agenda)
- 신청 폼 (이메일, 이름 등)
- Early Bird 할인 배너

최적 길이: 스크롤 1분 (Medium-form)
타겟: 이벤트, 웨비나, 세미나
```

### 3. Service/Consultant
```
특징:
- 포트폴리오/case study
- 전문성 증명 (자격증, 경력)
- 서비스 패키지 (Basic/Pro/Premium)
- 상담 신청 폼
- 클라이언트 로고

최적 길이: 스크롤 2~3분 (Long-form)
타겟: 컨설턴트, 에이전시, 프리랜서
```

### 4. Lead Gen (리드 생성)
```
특징:
- 가치 제안 (Value Prop): 상단에 명확히
- 무료 리소스 강조 (e-book, 템플릿, 웨비나)
- Lead Form (이메일, 회사명, 담당자 등)
- Social Proof (베팅 로고, 통계)
- Trust Badges

최적 길이: 스크롤 1~2분 (Medium-form)
타겟: B2B SaaS, 온라인 코스, 이벤트 등록
```

### 5. Promotional Campaign
```
특징:
- 시간 제한 배너 (타이머)
- 할인/프로모션 강조
- 상품 이미지 또는 비디오
- 재고 부족 강조
- 사회적 증명 (실시간 구매 알림)

최적 길이: 스크롤 30초~1분 (Short-form)
타겟: 전자상거래, 시즌 할인, 플래시 세일
```

---

## 디자인 프로세스

### Step 1: 요구사항 확인

사용자에게 아래 5가지를 확인합니다:

| 항목 | 확인 사항 |
|------|----------|
| **목표** | 페이지 타입 (제품 론칭, 이벤트, 리드 생성 등) |
| **타겟 고객** | 누구에게 어필하는가? (B2C, B2B, 시니어, 젊은층 등) |
| **핵심 메시지** | 가장 강력한 가치 제안 (한 문장) |
| **CTA** | 최종 행동 (구매, 신청, 다운로드, 상담) |
| **브랜드** | 색상, 로고, 폰트, 이미지 가이드 |

### Step 2: 섹션 구조 설계

핵심 섹션 템플릿:

```
1. Hero (히어로)
   - 백그라운드: 이미지 또는 비디오
   - 텍스트: 제목(H1) + 부제목 + CTA

2. Value Props (가치 제안)
   - 3개 핵심 포인트 카드

3. Features/Demo (기능 소개)
   - 스크린샷 + 설명
   - 좌우 교대 배치

4. Social Proof (신뢰도)
   - 클라이언트 로고, 후기, 통계

5. Pricing (요금제) - 필요시
   - 3단 가격표
   - 인기 플랜 강조

6. CTA Section (최종 행동)
   - 큰 버튼 + 부제목

7. Footer (하단)
   - 링크, 연락처, 뉴스레터
```

### Step 3: 디자인 시스템 적용

- **색상**: 브랜드 Primary + Neutral (검은색/회색/흰색)
- **폰트**: 한글 (Pretendard), 영문 (Inter/SF Pro)
- **레이아웃**: 12열 그리드, 1200px 최대 너비
- **상호작용**: Hover 상태, 부드러운 스크롤, 모달

### Step 4: 코드 생성

```
html/
├── index.html (메인 페이지)
├── css/
│   ├── styles.css (전역 스타일)
│   └── responsive.css (모바일 반응형)
├── js/
│   ├── main.js (상호작용)
│   └── form.js (폼 처리)
└── assets/
    ├── images/
    └── icons/
```

또는 Next.js/React:

```
src/
├── components/
│   ├── Hero.tsx
│   ├── Features.tsx
│   ├── Testimonials.tsx
│   └── CTA.tsx
├── app.tsx (또는 index.tsx)
├── styles.module.css
└── public/
    └── assets/
```

---

## 절대 규칙 (Hard Rules)

### 1. 모바일 우선 (Mobile-First)
```
- 데스크톱 확대, 모바일 축소 금지
- 모바일(375px)부터 태블릿(768px), 데스크톱(1200px) 순
- 모든 텍스트 가독성 유지 (최소 16px)
```

### 2. SEO 필수 요소
```
<head>
  <title>명확한 제목 (50~60자)</title>
  <meta name="description" content="설명 (150~160자)">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="keywords" content="핵심 키워드 3~5개">
  <link rel="canonical" href="정규 URL">
</head>
```

### 3. CTA는 3개 이상
- 헤로: 주 CTA 1개
- 중간: 보조 CTA (리드 폼, 데모 신청)
- 하단: 최종 CTA (강조)

### 4. 성능 최적화
```
- 이미지: WebP 포맷, 최대 100KB
- 폰트: WOFF2, 한글만 로드 (subset)
- CSS/JS: 최소화 (minify)
- 무거운 이미지: Lazy Loading
```

### 5. 접근성 (Accessibility)
```
- 색상 대비: WCAG AA 이상
- 폼 라벨: 모두 <label> 태그
- 이미지: alt 텍스트 필수
- 키보드 네비게이션 지원
```

---

## 출력 형식

### HTML 패키지
```
zip 또는 폴더:
├── index.html
├── css/ (styles.css, responsive.css)
├── js/ (main.js, form.js)
├── assets/ (images/, icons/)
└── README.md (배포 가이드)
```

### Next.js / React
```
npm create-next-app@latest my-landing-page --typescript
(또는 React 프로젝트)

배포: Vercel, Netlify, GitHub Pages
```

---

## 워크플로우

```
요청 접수
↓
타입/타겟 확인 (5가지 항목)
↓
섹션 구조 제안 (사용자 승인)
↓
디자인 시스템 정의
↓
HTML/React 코드 생성
↓
배포 가이드 제공
```

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| 로딩 느림 | 이미지 용량 과다 | 이미지 최적화, WebP 변환 |
| 모바일 깨짐 | 반응형 설정 부족 | 미디어쿼리 추가, 플렉스박스 확인 |
| SEO 순위 낮음 | 메타 태그 부재 | Open Graph, Schema 마크업 추가 |
| 폼 제출 안 됨 | 백엔드 연동 누락 | Formspree, Netlify Forms 등 설정 |
| 글꼴 한글 깨짐 | 폰트 서브셋 미포함 | Pretendard 웹폰트 링크 확인 |
