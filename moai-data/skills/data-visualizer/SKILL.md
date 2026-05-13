---
name: data-visualizer
description: >
  shadcn/ui 기반 데이터 시각화와 차트·대시보드를 생성하는 스킬입니다.
  '차트 만들어줘', '그래프 그려줘', '시각화해줘', '대시보드 만들어줘'라고 요청할 때 사용하세요.
  HTML 대시보드 생성 전에 소크라테스식 테마 인터뷰(베이스 팔레트·컬러 모드·모서리 반경·효과)를
  먼저 묻고, Mermaid / Recharts / Chart.js / Tremor / ECharts 중 적합한 스택으로
  인터랙티브 대시보드를 제작합니다. moai-office로 PPT/Word 변환도 지원합니다.
user-invocable: true
version: 2.5.0
---

# 데이터 시각화 (Data Visualizer)

> moai-data | shadcn/ui 기반 차트·대시보드 전문 스킬 · v1.4.0에서 shadcn/ui 기본 테마 전환

## 역할

데이터를 시각적으로 표현하는 전문가. Mermaid, Recharts/Chart.js, Tremor 기반 HTML 대시보드를 생성하고 PPT/Word로 변환합니다. HTML 산출물은 shadcn/ui OKLCH 토큰을 기본 테마로 사용합니다.

## 시각화 전략 (자동 판단)

### 방식 1: Mermaid 다이어그램 (간단 차트)
- pie chart, bar chart, flowchart, gantt
- Cowork Artifacts에서 직접 렌더링
- 빠르고 가벼움, 별도 파일 불필요
- 테마 인터뷰 **생략 가능** (Mermaid 기본 스타일 사용)

### 방식 2: shadcn 기반 HTML·React 대시보드 (상세 분석)
- **기본값**: Next.js 15 + Tailwind v4 + shadcn/ui + **Recharts**
- 단일 HTML 파일 모드: Tailwind CDN + shadcn CSS 변수 인라인 + Chart.js
- KPI 카드, 라인/막대/파이/도넛/레이더/버블 차트
- 필터, 호버 툴팁, 줌, 다크 모드 자동 지원
- Cowork Artifacts에서 렌더링 가능
- **테마 인터뷰 필수**

### 방식 3: 마크다운 테이블 (텍스트 기반)
- 간단한 비교표, 순위표
- 별도 파일 불필요
- 테마 인터뷰 생략

---

## [HARD] HTML 대시보드 생성 시 shadcn 테마 인터뷰

HTML·React 대시보드(방식 2)를 산출할 때는 **코드 생성 직전에** MoAI 오케스트레이터가 `AskUserQuestion`으로 다음 4개 질문을 제시합니다.

1. **Q1 베이스 팔레트** — Neutral(기본) / Zinc / Stone / Slate
2. **Q2 컬러 모드** — System+Toggle(기본) / Light / Dark / Auto
3. **Q3 모서리 반경** — Balanced 0.5rem(기본) / Sharp / Soft / Pill
4. **Q4 차트 라이브러리** — Recharts(기본) / Chart.js / Tremor / ECharts

> 대시보드 스킬은 Q4 옵션 자체가 차트 스택이므로 랜딩/상세와 달리 multiSelect를 사용하지 않습니다.

상세 질문 payload·Fallback 기본값은 `../../../moai-content/skills/landing-page/references/landing-page/shadcn-theme-interview.md` (공용 레퍼런스) 참조.

Fallback(인터뷰 생략) 기본값: `Neutral + System+Toggle + 0.5rem + Recharts`. 적용 시 응답 상단에 고지합니다.

### 라이브러리 선택 가이드

| 상황 | 권장 라이브러리 | 이유 |
|------|---------------|------|
| React/Next.js + B2B 대시보드 | **Recharts** | shadcn 공식 Chart 컴포넌트 기반, 타입 안전 |
| 단일 HTML(React 없음) | **Chart.js** | CDN 한 줄로 시작, Canvas 기반 가벼움 |
| KPI·영업 대시보드 빠른 산출 | **Tremor** | AreaChart/BarChart 프리셋 풍부 |
| 지도·Sankey·TreeMap | **ECharts** | 고난도 시각화 커버리지 |

---

## 판단 기준

| 조건 | 방식 | 테마 인터뷰 |
|------|------|---------|
| 데이터 5행 이하 | 마크다운 테이블 | 생략 |
| 단순 비율/분포 | Mermaid pie/bar | 생략 |
| 시계열/트렌드 (React) | Recharts 선 차트 | 필수 |
| 시계열/트렌드 (HTML) | Chart.js 선 차트 | 필수 |
| 다차원 비교 | Recharts 레이더/버블 | 필수 |
| 대시보드·KPI | Tremor + shadcn Card | 필수 |
| 지도·복합 시각화 | ECharts | 필수 |
| 인터랙티브 필요 | HTML/React 대시보드 | 필수 |

---

## PPT/Word 변환 플로우

사용자가 "PPT로 만들어줘" 요청 시:
1. HTML·React 차트 → 스크린샷/이미지 추출
2. 데이터 테이블 + 차트 이미지 → `moai-office:pptx-designer`로 전달
3. PPT 슬라이드 생성

Word 보고서 요청 시:
1. 차트 이미지 + 분석 텍스트 → `moai-office:docx-generator`로 전달
2. Word 문서 생성 (차트 임베드)

---

## 산출물

- Mermaid 다이어그램 (인라인)
- **shadcn 기반 HTML 대시보드** (OKLCH 테마, 다크 모드 지원)
- Recharts/Chart.js/Tremor/ECharts HTML·React 파일 (인터랙티브)
- 마크다운 보고서 (테이블 + 인사이트)

### HTML 대시보드 필수 구성

1. `index.html` — 또는 Next.js `app/page.tsx`
2. `styles.css` — shadcn OKLCH CSS 변수 `:root` + `.dark` 블록 (인라인 또는 별도)
3. 차트 스크립트 — 선택된 라이브러리의 CDN 또는 npm 모듈
4. 다크 모드 토글 — 인터뷰 Q2가 `system+toggle`인 경우
5. `README-setup.md` — React 모드일 경우 shadcn 컴포넌트 설치 명령

---

## 실행 규칙

1. 사용자 요청 수신 → 시각화 방식 자동 판단
2. **방식 2(HTML·React) 선택 시 shadcn 테마 인터뷰 실행** (HARD)
3. 데이터 구조 확인 → 부적합 시 `moai-data:data-explorer` 권유
4. 차트 산출 후 사용자 검토 요청

## 이 스킬을 사용하지 말아야 할 때
- **데이터 탐색/프로파일링** → `moai-data:data-explorer` 사용
- **공공데이터 조회** → `moai-data:public-data` 사용
- **랜딩 페이지 내 차트 섹션** → `moai-content:landing-page`에서 Q4 효과 선택 시 통합 산출
- **상세페이지 내 가격 비교 차트** → `moai-content:product-detail`에서 직접 처리