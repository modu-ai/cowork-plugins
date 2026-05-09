# Design Tokens — html-report

`moai-content:html-report`의 CSS 변수 계약 단일 진실(SSOT).
모든 모드 템플릿은 이 문서의 토큰을 그대로 사용해야 합니다.

---

## 팔레트

Anthropic 영감 팔레트. `/tmp/html-eff/` 10개 샘플의 공통 추출값.

| CSS 변수 | 헥스 값 | 용도 |
|----------|---------|------|
| `--ivory` | `#FAF9F5` | 페이지 배경 (warm off-white) |
| `--paper` | `#FFFFFF` | 카드·패널·테이블 배경 |
| `--slate` | `#141413` | 본문 텍스트 (warm near-black) |
| `--clay` | `#D97757` | 강조·링크·clay accent (terracotta) |
| `--clay-d` | `#B85C3E` | clay hover / 고위험 표시 |
| `--oat` | `#E3DACC` | 보조 배경·구분선·차트 기본 막대 |
| `--olive` | `#788C5D` | 긍정 신호·보조 강조 (sage green) |

### 그레이 스케일

| CSS 변수 | 헥스 값 | 용도 |
|----------|---------|------|
| `--g100` | `#F0EEE6` | 테이블 헤더 배경·연한 배경 |
| `--g300` | `#D1CFC5` | 테두리·구분선 |
| `--g500` | `#87867F` | 보조 텍스트·레이블 |
| `--g700` | `#3D3D3A` | 중간 강도 텍스트·저자명 |

---

## 폰트 변수 계약

```css
:root {
  --sans:  "Pretendard", system-ui, -apple-system, "Segoe UI", sans-serif;
  --serif: "Pretendard", ui-serif, Georgia, "Times New Roman", serif;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
```

모드별 override 예시 (plan 모드):
```css
:root {
  --serif: "Noto Serif KR", ui-serif, Georgia, serif;
}
```

---

## 레이아웃 토큰

| CSS 변수 | 값 | 용도 |
|----------|-----|------|
| `--max-width` | `860px` | 보고서 컨테이너 (report / status / financial) |
| `--max-width-wide` | `1120px` | 인덱스·대시보드 (index 참조 전용) |
| `--radius-panel` | `12px` | 카드·차트 패널 border-radius |
| `--radius-row` | `8px` | 테이블 행 border-radius |
| `--border` | `1.5px solid var(--g300)` | 표준 테두리 |
| `--body-lh` | `1.6` | 본문 line-height |
| `--heading-ls` | `-0.01em` | 제목 letter-spacing |

---

## `:root` 전체 선언 (복사·붙여넣기 기준)

```css
:root {
  /* 팔레트 */
  --ivory:  #FAF9F5;
  --paper:  #FFFFFF;
  --slate:  #141413;
  --clay:   #D97757;
  --clay-d: #B85C3E;
  --oat:    #E3DACC;
  --olive:  #788C5D;

  /* 그레이 스케일 */
  --g100: #F0EEE6;
  --g300: #D1CFC5;
  --g500: #87867F;
  --g700: #3D3D3A;

  /* 폰트 */
  --sans:  "Pretendard", system-ui, -apple-system, sans-serif;
  --serif: "Pretendard", ui-serif, Georgia, serif;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", monospace;

  /* 레이아웃 */
  --max-width:    860px;
  --radius-panel: 12px;
  --radius-row:   8px;
  --border:       1.5px solid var(--g300);
}
```

---

## 인쇄 토큰 (`@media print` 패턴)

모든 템플릿에 다음 `@media print` 블록을 포함해야 합니다.

```css
@media print {
  body {
    background: white;
    color: black;
    padding: 0;
    font-size: 12pt;
  }
  .page {
    max-width: none;
  }
  a[href]::after {
    content: " (" attr(href) ")";
    font-size: 10pt;
    color: #555;
  }
  h1, h2, h3 {
    page-break-after: avoid;
  }
  table, figure, .chart-panel {
    page-break-inside: avoid;
  }
  .no-print {
    display: none !important;
  }
  /* 테두리·배경색 인쇄 보존 */
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
```

---

## 접근성: 명도 대비 검증표 (WCAG AA ≥ 4.5:1)

| 전경색 | 배경색 | 대비 비율 | AA 통과 |
|--------|--------|-----------|---------|
| `--slate` `#141413` | `--ivory` `#FAF9F5` | 17.9:1 | ✓ |
| `--slate` `#141413` | `--paper` `#FFFFFF` | 18.1:1 | ✓ |
| `--slate` `#141413` | `--g100` `#F0EEE6` | 16.2:1 | ✓ |
| `--g700` `#3D3D3A` | `--ivory` `#FAF9F5` | 8.6:1 | ✓ |
| `--g700` `#3D3D3A` | `--paper` `#FFFFFF` | 8.8:1 | ✓ |
| `--g500` `#87867F` | `--ivory` `#FAF9F5` | 3.7:1 | ✗ (보조 텍스트 전용, 14px+ 대형 텍스트 AA 통과) |
| `--clay` `#D97757` | `--ivory` `#FAF9F5` | 3.2:1 | ✗ (장식용·배경용으로만 사용) |
| `--paper` `#FFFFFF` | `--clay` `#D97757` (배경) | 3.2:1 | ✗ (텍스트 비사용 — 배경 accent 전용) |

**규칙**:
- `--g500`은 보조 레이블(`font-size: 11–12px`)에만 허용 (큰 글씨 AA 통과)
- `--clay`는 강조선·배경 accent·링크 색상에만 사용. 클레이 배경 위 흰 텍스트 금지
- 본문 텍스트(`font-size: 14–16px`)는 반드시 `--slate` 또는 `--g700` 사용

---

## 컴포넌트별 색상 규칙

### 메트릭 카드 (stat-card)
- 배경: `--paper`
- 테두리: `var(--border)`
- 경고 카드: `border-left: 4px solid var(--clay)`
- 숫자: `font-family: var(--serif); color: var(--slate)`
- 레이블: `color: var(--g500); text-transform: uppercase`
- 긍정 델타: `color: var(--olive)`
- 중립 델타: `color: var(--g500)`

### Shipped 테이블
- 테이블 배경: `--paper`
- 헤더 배경: `--g100`
- 행 구분선: `--g100`
- PR 링크: `color: var(--clay)`
- 저자: `color: var(--g700)`

### 리스크 점 색상 (Risk Dot)
- 낮음(Low): `background: var(--olive)`
- 보통(Med): `background: var(--clay)`
- 높음(High): `background: var(--clay-d)` (`#B85C3E`)

### Velocity SVG 막대
- 일반 막대: fill `var(--oat)` (`#E3DACC`)
- 피크 막대: fill `var(--clay)` (`#D97757`)
- 그리드라인 (major): stroke `var(--g300)` (`#D1CFC5`)
- 그리드라인 (minor): stroke `var(--g100)` (`#F0EEE6`)
- 텍스트: fill `var(--g500)` (`#87867F`), font-family system-ui (SVG 내 CSS 변수 미지원)

### Carryover 패널
- 배경: `--oat`
- 항목 구분선: `rgba(20, 20, 19, 0.08)` (--slate 8% alpha)
- 태그 배경: `--ivory`, 텍스트: `--g700`
- 본문: `color: var(--g700)`

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-05-09 | 1.0.0 | Wave 1 초기 작성 (`status` 모드 기준) |
