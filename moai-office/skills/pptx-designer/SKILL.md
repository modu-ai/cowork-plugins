---
name: pptx-designer
description: |
  발표용 파워포인트(.pptx) 슬라이드를 디자인해 바로 열리는 파일로 만들어 드립니다 — 사내 보고, 투자 피칭, 교육자료, 컨퍼런스 키노트까지.
  다음과 같은 요청 시 사용하세요:
  - "발표자료 PPT로 만들어줘"
  - "파워포인트 슬라이드 디자인해줘"
  - "보고서를 발표용 PPT로 만들어줘"
  - "투자 피칭 덱 15장 만들어줘"
  - "임원 보고용 슬라이드 격식 있게"
  - "신입사원 교육자료 PPT"
  - "제품 데모 슬라이드 깔끔하게 디자인해줘"
  한국형 폰트·색 팔레트 디자인 시스템과 비즈니스 슬라이드 구성안을 적용해 슬라이드를 만들고, 카피는 AI 슬롭 검수로 다듬을 수 있습니다.
  발표자료를 .pptx 파일로 만들 때는 Claude 기본 생성 대신 이 스킬을 사용하세요.
  [책임 경계] vs moai-office:notebooklm-slide-prompt: 이 스킬=지금 바로 열리는 .pptx 파일, 저 스킬=NotebookLM에 넣을 슬라이드 생성 프롬프트.
user-invocable: true
version: 2.27.0
---

# PPT 디자이너 (PPTX Designer)

## 개요

발표용 슬라이드를 디자인하고 생성합니다. **Claude 브랜드 톤 10 큐레이션 팔레트**(AI 슬롭 회피용)와
**9가지 비즈니스 슬라이드 아키타입**, **자동 QA 검수 파이프라인**, **HTML-First 옵션**을 제공합니다.
4가지 생성 방식을 지원합니다: (1) pptxgenjs 직접, (2) HTML-First 후 export, (3) NotebookLM, (4) 마크다운 원고.

## 트리거 키워드

PPT, 파워포인트, 발표자료, 슬라이드, 프레젠테이션, 보고서, 기안서, 피칭 덱, 데모덱, 컨퍼런스 자료

## 디자인 시스템 — Claude Modern Deck Theme

상세 토큰은 `references/curated-palettes.md`·`references/typography-pairings.md` 참고.

### 10 큐레이션 팔레트 — 한눈에

| # | 팔레트 | 주색 | 보조 | 배경 | 용도 |
|---|---|---|---|---|---|
| 1 | **Claude Classic** | Orange `#d97757` | Blue `#6a9bcc` | Beige `#faf9f5` | 일반 비즈니스·신뢰 |
| 2 | **Claude Coral** | Crail `#c15f3c` | Pampas `#f4f3ee` | White | 적극적 마케팅·캠페인 |
| 3 | **Claude Mono** | Dark `#141413` | Mid Gray | White | 격식·논문·법적 |
| 4 | **Claude Blue Calm** | Blue `#6a9bcc` | Mid | Beige | 데이터·금융·차분한 |
| 5 | **Claude Green Earth** | Green `#788c5d` | Olive | Beige | 지속가능·헬스케어 |
| 6 | **Korean Brick** | 한국 적갈색 `#a04a3a` | Beige | Cream | 한국 전통·B2B |
| 7 | **Korean Navy** | Deep Navy `#1d3557` | Gold `#c9a961` | White | 격식 발표·임원 보고 |
| 8 | **Korean Sage** | 청록 `#5a8a85` | Beige | Cream | 헬스·웰니스·교육 |
| 9 | **Dark Editorial** | Orange | Mid | Dark `#1a1a1a` | 다크 모드·테크·하이엔드 |
| 10 | **High Contrast Bold** | Black | Orange Pop | White | 임팩트 키노트·이벤트 |

### 9가지 비즈니스 슬라이드 아키타입

| # | 아키타입 | 사용 시점 | 구조 |
|---|---|---|---|
| 1 | **Title (표지)** | 첫 슬라이드 | 큰 제목 + 부제 + 발표자·날짜·로고 |
| 2 | **Agenda (목차)** | 두 번째 | 섹션 리스트 + 페이지 번호 또는 진행 표시 |
| 3 | **Problem (문제 정의)** | 본문 시작 | 현황·페인포인트·임팩트 |
| 4 | **Solution (해법)** | 문제 다음 | 우리의 접근·핵심 차별화 |
| 5 | **Features (기능·차별점)** | 솔루션 상세 | 3-6 그리드 + 아이콘 + 짧은 설명 |
| 6 | **Stats (통계 강조)** | 데이터 페이지 | 큰 숫자 3-4개 + 짧은 라벨 |
| 7 | **Team (팀 소개)** | 후반부 | 사진·역할·핵심 경력 |
| 8 | **CTA (행동 요청)** | 클로징 전 | 강조 박스 + 1개 액션 + 연락처 |
| 9 | **Closing (마무리·Q&A)** | 마지막 | 감사·연락처·QR (옵션) |

상세 와이어프레임은 `references/slide-archetypes.md` 참고.

### 타이포그래피 페어링 (5조합)

| 페어링 | 한국 | 영문 | 적합 |
|---|---|---|---|
| Modern | Pretendard | Inter | 일반 비즈니스 (권장) |
| Editorial | Pretendard | Lora (Serif Italic for quotes) | 매거진·발표·인용 강조 |
| Bold Heading | Pretendard ExtraBold | Poppins ExtraBold | 임팩트·이벤트 |
| Classic | 맑은 고딕 | Georgia | 격식·논문·법적 |
| Tech | Pretendard | JetBrains Mono (모노) | 개발자·테크 컨퍼런스 |

## 워크플로우

### 1단계: 생성 방식 선택

| 방식 | 추천 시점 |
|---|---|
| **pptxgenjs 직접** (권장) | .pptx 파일 직접 생성, 가장 빠름 |
| **HTML-First** | 시각 검토 후 export, 디자이너·디자인 검수 필요 시 |
| **NotebookLM** | NotebookLM 환경에서 슬라이드 생성 |
| **마크다운 원고만** | 텍스트만 작성 (사용자가 직접 디자인) |

### 2단계: 팔레트·페어링 선택

사용자에게 다음을 확인합니다 (AskUserQuestion):

- 톤 (Anthropic Orange 기본, Korean Navy 격식, Coral 적극, Mono 격식 등)
- 슬라이드 수 (3분 5-7장, 10분 10-15장, 30분 20-30장)
- 청중 (임원·고객·개발자·일반 대중)

### 3단계: 아키타입 시퀀스 구성

청중·길이에 맞춰 아키타입을 시퀀스합니다.

```
10분 사내 발표 (10-15장):
Title → Agenda → Problem → Solution → Features (3-6 그리드) →
Stats → Closing

30분 외부 피치 (20-30장):
Title → Agenda → Problem (2-3p) → Solution (3p) → Features (4-5p) →
Stats (2p) → Team → CTA → Closing → Q&A

3분 짧은 데모 (5-7장):
Title → Problem → Solution + Demo → Stats → Closing
```

### 4단계: 디자인 시스템 적용

선택된 팔레트의 색·폰트·간격을 슬라이드 마스터에 적용:

```javascript
import PptxGenJS from "pptxgenjs";

const pptx = new PptxGenJS();

// Claude Classic 팔레트
const colors = {
  primary: "D97757",   // Orange
  secondary: "6A9BCC", // Blue
  bg: "FAF9F5",        // Beige
  surface: "FFFFFF",
  ink: "141413",
  mid: "B0AEA5",
};

// 16:9 (1920×1080)
pptx.layout = "LAYOUT_WIDE";

// 슬라이드 마스터 정의
pptx.defineSlideMaster({
  title: "MASTER_SLIDE",
  background: { color: colors.bg },
  objects: [
    { rect: { x: 0, y: 0, w: "100%", h: 0.06, fill: { color: colors.primary } } },
    { text: {
      text: "© 2026",
      options: { x: 0.3, y: 7.1, w: 2, h: 0.3, fontSize: 9, color: colors.mid, fontFace: "Pretendard" }
    }},
    { text: {
      text: "{slide_num}",
      options: { x: 12.5, y: 7.1, w: 0.5, h: 0.3, fontSize: 9, color: colors.mid, align: "right" }
    }},
  ],
});

// Title 슬라이드
const titleSlide = pptx.addSlide({ masterName: "MASTER_SLIDE" });
titleSlide.addText("2026 Q1 사업 보고", {
  x: 0.8, y: 2.5, w: 11.4, h: 1.5,
  fontSize: 56, bold: true, color: colors.ink, fontFace: "Pretendard"
});
```

전체 코드 패턴은 `references/pptxgen-code-patterns.md` (기존 자료, 612줄) + `references/slide-archetypes.md`.

### 5단계: QA 자동 검수

`references/qa-checklist.md`의 자동 검수 + 시각 검수:

**자동 검수 (코드)**:
1. 빈 플레이스홀더 0건
2. 텍스트 overflow 검출 (슬라이드 영역 초과)
3. 색 대비 4.5:1 이상
4. 폰트 화이트리스트 검증
5. 슬라이드 마스터 일관 적용

**시각 검수 (슬라이드 → 이미지 변환)**:
1. LibreOffice로 PDF/JPEG 변환 후 시각 확인
2. 겹친 요소·잘린 텍스트·중첩 확인
3. 색 일관성 (한 팔레트 안에서만)
4. AI 슬롭 카피 검출 (`moai-design:claude-design-slop-check` 체이닝)
5. 청중·톤 적합성 (사람 검수)

### 6단계: 출력

| 형식 | 사용 시점 |
|---|---|
| `.pptx` | 주 산출물 (PowerPoint·Keynote 호환) |
| `.pdf` 백업 | 폰트 깨짐 방지·외부 발송 |
| `.jpg/.png` 미리보기 | 시각 확인·SNS 공유 |
| 슬라이드별 가이드 `.md` | 발표자 노트·편집 가이드 |

## 사용 예시

- "3분기 사업 성과 보고서를 10슬라이드 PPT로, Claude Classic 톤" → Title/Agenda/Problem/Solution/Stats/Closing 시퀀스
- "스타트업 시드 피칭 덱 15슬라이드, 임팩트 톤" → High Contrast Bold 팔레트 + 모든 아키타입 활용
- "신입사원 온보딩 교육자료" → Korean Sage 팔레트 + 차분한 톤
- "테크 컨퍼런스 키노트" → Dark Editorial 팔레트 + Tech 페어링
- "내부 임원 보고용" → Korean Navy 팔레트 + 격식
- "B2B 제품 데모" → Claude Classic + Feature Grid 강조

## 출력 형식

### pptxgenjs 직접 방식
- 파일 형식: `.pptx` (PowerPoint 2007+ 호환)
- 슬라이드 크기: 16:9 (1920×1080) 또는 4:3 (1024×768)
- 폰트: Pretendard (한국 본문) + Inter (영문)
- 색 인코딩: sRGB

### HTML-First 방식
- 중간 산출물: `slides.html` (시각 검토용)
- 최종: `.pptx` 또는 `.pdf` export
- 검토 후 수정·재export 가능

### NotebookLM 방식
- `slides.md` (마크다운 원고) + `style-prompt.txt` (NotebookLM 입력용)

### 마크다운 원고 방식
- `.md` (각 슬라이드 = `##` 제목)
- Figma·Canva·PowerPoint 등에서 수동 디자인 가능

## 주의사항

### Claude 톤 사용 규칙

- 한 덱에 1개 팔레트만 — 슬라이드마다 색 바꾸기 금지
- Primary 색은 헤딩·핵심 강조에만 (본문 도배 금지)
- 각 슬라이드 최대 3색 (Primary + Secondary + Neutral)
- 한국 청중 발표는 한국 폰트(Pretendard·맑은 고딕) 필수

### 슬라이드 수 가이드

| 발표 시간 | 슬라이드 수 | 아키타입 권장 시퀀스 |
|---|---|---|
| 3분 | 5-7장 | Title · Problem · Solution · Stats · Closing |
| 10분 | 10-15장 | + Agenda · Features · CTA |
| 30분 | 20-30장 | + 본문 다중 · Team · 상세 데이터 |
| 60분 | 40-50장 | + 세부 사례·시연·Q&A 준비 |

### 한 슬라이드 한 메시지

각 슬라이드 = 핵심 메시지 1개. 슬라이드당 텍스트 50단어 이하 권장. 상세 내용은 발표자 노트에.

### 텍스트 최소 사이즈

- 본문: 18pt 이상 (32-40 ft 거리 가독성)
- 캡션: 14pt 이상
- 제목: 32pt 이상 (강조 슬라이드는 56pt+)

### 차트·시각화 우선

데이터는 차트로 시각화 — 표·텍스트 나열보다 1000배 빠른 인지. Stats 아키타입 적극 활용.

### 이미지 저작권

무료 이미지 사이트(Unsplash, Pixabay) 또는 자체 제작·라이선스 보유 이미지만 사용. AI 생성 이미지는 사용 약관 확인.

### 한국 폰트 임베드

Pretendard·맑은 고딕은 상용·배포 자유. 발표 PC에 폰트 미설치 시 PDF 변환 권장.

## 문제 해결

| 상황 | 해결 |
|---|---|
| 파일 생성 실패 | `npm install pptxgenjs` 설치 |
| 폰트 깨짐 | PDF 변환 또는 발표 PC에 Pretendard 설치 |
| 색 대비 실패 | 본문 텍스트는 Ink Dark, 강조는 Primary만 |
| 슬라이드 overflow | 텍스트 50단어 이하·줄바꿈 명시 |
| 마스터 적용 안 됨 | `masterName: "MASTER_SLIDE"` 명시 |
| HTML-First 미리보기 안 됨 | 브라우저 새로고침·캐시 삭제 |
| NotebookLM 연동 | 마크다운+스타일 프롬프트 별도 제공 (수동 입력) |

## 관련 스킬 / 자체 검수

슬라이드 생성이 끝나면 산출된 .pptx 파일을 다시 열어 플레이스홀더 잔존·슬라이드 수 미달·한글 폰트·인코딩 깨짐·차트/이미지 깨짐을 **자체 검수**하고, 문제가 있으면 자동 수정 후 재생성하며 최종 PASS/FAIL 결과를 보고합니다(검수 항목은 `references/qa-checklist.md` 참고).

| 스킬 | 사용 시점 |
|---|---|
| `moai-office:docx-generator` | DOCX 문서 생성 (같은 Claude 톤 시스템 공유) |
| `moai-office:hwpx-writer` | 한컴 한글 문서 |
| `moai-office:xlsx-creator` | 엑셀 데이터 시트 (차트 데이터 소스) |
| `moai-office:pdf-writer` | 다국어 PDF 변환 |
| `moai-content:copywriting` | 슬라이드 카피 작성 |
| `moai-content:humanize-korean` | 한국어 카피 자연화 |
| `moai-design:claude-design-slop-check` | 슬라이드 카피 AI 슬롭 검수 |
| `moai-design:claude-design-prompt-builder` | Claude Design에 동시 시안 요청 시 |
| `moai-media:gemini-3-image-prompt` | 슬라이드 일러스트·배경 이미지 프롬프트 |

## 기술 참조

- **pptxgenjs 공식**: https://gitbrent.github.io/PptxGenJS/
- **Pretendard 폰트**: https://github.com/orioncactus/pretendard
- **Anthropic Brand Guidelines**: 본 스킬의 색·타이포는 Anthropic 공식 브랜드 기반
- **NotebookLM**: https://notebooklm.google.com/

## References

- `references/curated-palettes.md` — 10 큐레이션 팔레트 상세 (Claude 톤 변형 + 한국 톤 4종)
- `references/slide-archetypes.md` — 9가지 비즈니스 슬라이드 아키타입 와이어프레임
- `references/typography-pairings.md` — 5가지 폰트 페어링 + 사이즈 위계
- `references/qa-checklist.md` — 자동·시각 검수 10단계
- `references/pptxgen-code-patterns.md` — pptxgenjs 코드 패턴 (기존 자료, 612줄)
- `references/guide.md` — 디자인 시스템 빌더 가이드 (기존 자료, 12개 레이아웃)
- `references/report-generator.md` — 보고서 생성기 (기존 자료)
