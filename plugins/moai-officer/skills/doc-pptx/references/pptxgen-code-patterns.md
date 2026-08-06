# PptxGenJS 네이티브 요소 상세 코드 패턴

> 이 파일은 ppt-design-system 스킬의 참조 자료입니다.
> SKILL.md에서 `@${CLAUDE_SKILL_DIR}/references/pptxgen-code-patterns.md`로 자동 로드됩니다.

## PptxGenJS 네이티브 요소 상세 가이드

### 1. addTable() — 테이블

표 형식 데이터는 **반드시** `addTable()`을 사용합니다.

#### 테이블 스타일 상수

```javascript
// ===== 테이블 공통 스타일 =====
const TABLE_STYLE = {
  // 헤더 셀 (다크 배경)
  header: {
    bold: true,
    fill: { color: COLORS.bg_dark },
    color: COLORS.text_on_dark,
    fontFace: 'Pretendard',
    fontSize: 11,
    align: 'center',
    valign: 'middle'
  },
  // 일반 셀
  cell: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    valign: 'middle'
  },
  // 숫자 셀 (우측 정렬)
  cellRight: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    align: 'right',
    valign: 'middle'
  },
  // 짝수행 배경 (zebra stripe)
  cellAlt: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    fill: { color: COLORS.bg_secondary },
    valign: 'middle'
  },
  // 합계/소계 행
  cellTotal: {
    bold: true,
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_primary,
    border: [{ type: 'solid', pt: 1.5, color: COLORS.text_primary }, null, null, null],
    valign: 'middle'
  }
};

// 테이블 공통 옵션
const TABLE_OPTIONS = {
  x: 0.6,
  y: 1.8,  // 제목 바 아래
  w: 12.13,
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
  autoPage: false,
  margin: [5, 8, 5, 8]  // 셀 내부 여백 [top, right, bottom, left] pt
};
```

#### 테이블 헬퍼 함수

```javascript
/**
 * 디자인 시스템 적용된 테이블 추가
 * @param {Slide} slide
 * @param {string[]} headers - 헤더 텍스트 배열
 * @param {Array<Array<string|{text,options}>>} dataRows - 데이터 행 배열
 * @param {object} opts - 추가 옵션 (x, y, w, colW, rowH 등)
 */
function addStyledTable(slide, headers, dataRows, opts = {}) {
  const rows = [];

  // 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: { ...TABLE_STYLE.header }
  })));

  // 데이터 행 (zebra stripe 자동 적용)
  dataRows.forEach((row, i) => {
    const isAlt = i % 2 === 1;
    const baseStyle = isAlt ? TABLE_STYLE.cellAlt : TABLE_STYLE.cell;
    rows.push(row.map(cell => {
      if (typeof cell === 'string') {
        return { text: cell, options: { ...baseStyle } };
      }
      // {text, options} 객체인 경우 스타일 병합
      return { text: cell.text, options: { ...baseStyle, ...cell.options } };
    }));
  });

  slide.addTable(rows, {
    ...TABLE_OPTIONS,
    ...opts
  });
}

/**
 * colspan을 활용한 제목 행 포함 테이블
 */
function addTitledTable(slide, tableTitle, headers, dataRows, opts = {}) {
  const colCount = headers.length;
  const rows = [];

  // 테이블 제목 행 (colspan 병합)
  rows.push([{
    text: tableTitle,
    options: {
      colspan: colCount,
      bold: true,
      fill: { color: COLORS.bg_dark },
      color: COLORS.text_on_dark,
      fontFace: 'Pretendard',
      fontSize: 13,
      align: 'center',
      valign: 'middle'
    }
  }]);

  // 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: {
      bold: true,
      fill: { color: COLORS.bg_secondary },
      color: COLORS.text_primary,
      fontFace: 'Pretendard',
      fontSize: 11,
      align: 'center',
      valign: 'middle'
    }
  })));

  // 데이터 행
  dataRows.forEach((row, i) => {
    const isAlt = i % 2 === 1;
    rows.push(row.map(cell => {
      const base = isAlt
        ? { ...TABLE_STYLE.cellAlt }
        : { ...TABLE_STYLE.cell };
      if (typeof cell === 'string') return { text: cell, options: base };
      return { text: cell.text, options: { ...base, ...cell.options } };
    }));
  });

  slide.addTable(rows, { ...TABLE_OPTIONS, ...opts });
}
```

#### 테이블 사용 예시

```javascript
// ===== 매출 계획표 =====
addTitledTable(slide, '2026년 매출 계획표',
  ['구분', 'Q1', 'Q2', 'Q3', 'Q4', '연간 합계'],
  [
    ['온라인',
     { text: '120M', options: { align: 'right' } },
     { text: '150M', options: { align: 'right' } },
     { text: '180M', options: { align: 'right' } },
     { text: '200M', options: { align: 'right' } },
     { text: '650M', options: { align: 'right', bold: true } }],
    ['오프라인',
     { text: '80M', options: { align: 'right' } },
     { text: '90M', options: { align: 'right' } },
     { text: '100M', options: { align: 'right' } },
     { text: '110M', options: { align: 'right' } },
     { text: '380M', options: { align: 'right', bold: true } }],
  ],
  { colW: [2, 1.8, 1.8, 1.8, 1.8, 2.5] }
);

// ===== 일정표/시간표 =====
addStyledTable(slide,
  ['교시', '시간', '과목', '내용', '비고'],
  [
    ['1', '09:00~09:50', 'Excel 기초', '데이터 정리 자동화', '이론'],
    ['2', '10:00~10:50', 'Excel 분석', 'KPI 대시보드 설계', '이론+실습'],
    ['3', '11:00~11:50', 'PPT 생성', '슬라이드 자동 변환', '이론'],
  ],
  { colW: [1, 2.2, 2.5, 4, 1.8], rowH: [0.45, 0.4, 0.4, 0.4] }
);

// ===== 비교표 (스펙/기능 비교) =====
addStyledTable(slide,
  ['기능', 'Free', 'Pro', 'Enterprise'],
  [
    ['스킬 수', '12개', { text: '24개', options: { bold: true, color: COLORS.accent_blue } }, '무제한'],
    ['지원', '커뮤니티', '이메일', { text: '전담 매니저', options: { bold: true } }],
    ['가격', '무료', '월 9,900원', '문의'],
  ]
);
```

### 2. addChart() — 차트

수치 데이터의 추이/비교/비율은 **반드시** `addChart()`를 사용합니다.

#### 차트 스타일 상수

```javascript
// ===== 차트 공통 스타일 =====
const CHART_STYLE = {
  // 공통 기본값
  base: {
    showTitle: true,
    titleFontFace: 'Pretendard',
    titleFontSize: 14,
    titleColor: COLORS.text_primary,
    showLegend: true,
    legendFontFace: 'Pretendard',
    legendFontSize: 9,
    legendColor: COLORS.text_secondary,
    catAxisLabelFontFace: 'Pretendard',
    catAxisLabelFontSize: 10,
    catAxisLabelColor: COLORS.text_tertiary,
    valAxisLabelFontFace: 'Pretendard',
    valAxisLabelFontSize: 10,
    valAxisLabelColor: COLORS.text_tertiary,
  },
  // 차트 색상 팔레트 (최대 6색)
  colors: [
    COLORS.accent_blue,     // 4A7BF7
    COLORS.accent_cyan,     // 00D4AA
    COLORS.accent_yellow,   // FFB020
    COLORS.accent_red,      // FF6B6B
    COLORS.accent_purple,   // 8B5CF6
    '38BDF8'                // 라이트 블루 (6번째)
  ]
};
```

#### 차트 유형별 사용 기준

| 데이터 유형 | 차트 유형 | PptxGenJS 상수 |
|------------|----------|---------------|
| 항목별 크기 비교 | 세로 막대 | `pptx.charts.BAR` |
| 시계열 추이/변화 | 꺾은선 | `pptx.charts.LINE` |
| 전체 대비 비율 (5개 이하) | 원형 | `pptx.charts.PIE` |
| 전체 대비 비율 (중앙 KPI) | 도넛 | `pptx.charts.DOUGHNUT` |
| 추이 + 누적량 | 영역 | `pptx.charts.AREA` |
| 다차원 항목 비교 | 방사형 | `pptx.charts.RADAR` |
| 두 변수 간 관계 | 산점도 | `pptx.charts.SCATTER` |
| 세 변수 관계 | 버블 | `pptx.charts.BUBBLE` |

#### 차트 헬퍼 함수

```javascript
/**
 * 디자인 시스템 적용된 차트 추가
 * @param {Slide} slide
 * @param {object} pptx - PptxGenJS 인스턴스 (charts 참조용)
 * @param {string} type - 'BAR'|'LINE'|'PIE'|'DOUGHNUT'|'AREA'|'RADAR'|'SCATTER'
 * @param {Array} chartData - [{name, labels, values}]
 * @param {object} opts - 위치/크기/추가 옵션
 */
function addStyledChart(slide, pptx, type, chartData, opts = {}) {
  const typeMap = {
    BAR: pptx.charts.BAR,
    LINE: pptx.charts.LINE,
    PIE: pptx.charts.PIE,
    DOUGHNUT: pptx.charts.DOUGHNUT,
    AREA: pptx.charts.AREA,
    RADAR: pptx.charts.RADAR,
    SCATTER: pptx.charts.SCATTER,
    BUBBLE: pptx.charts.BUBBLE
  };

  const defaults = {
    x: 0.6, y: 1.8, w: 12.13, h: 5.0,
    ...CHART_STYLE.base,
    chartColors: CHART_STYLE.colors.slice(0, chartData.length || 6),
    ...opts
  };

  // 차트 유형별 기본값 추가
  if (type === 'BAR') {
    defaults.barGapWidthPct = 80;
    defaults.catAxisOrientation = 'minMax';
    defaults.valAxisOrientation = 'minMax';
  }
  if (type === 'LINE') {
    defaults.lineDataSymbol = 'circle';
    defaults.lineDataSymbolSize = 8;
    defaults.lineSmooth = false;
  }
  if (type === 'PIE' || type === 'DOUGHNUT') {
    defaults.showPercent = true;
    defaults.showLegend = true;
    defaults.legendPos = 'b';
    defaults.chartColors = CHART_STYLE.colors.slice(0, chartData[0]?.values?.length || 6);
  }

  slide.addChart(typeMap[type], chartData, defaults);
}
```

#### 차트 사용 예시

```javascript
// ===== 매출 추이 (꺾은선) =====
addStyledChart(slide, pptx, 'LINE',
  [{ name: '매출(억)', labels: ['1월','2월','3월','4월','5월','6월'],
     values: [12, 15, 18, 22, 25, 30] }],
  { x: 0.6, y: 1.8, w: 7, h: 4.5, title: '2026 상반기 매출 추이' }
);

// ===== 부서별 비교 (막대) =====
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '목표', labels: ['영업','마케팅','개발','인사'], values: [100, 80, 120, 50] },
    { name: '실적', labels: ['영업','마케팅','개발','인사'], values: [95, 85, 110, 48] }
  ],
  { x: 0.6, y: 1.8, w: 12.13, h: 5, title: '부서별 목표 대비 실적' }
);

// ===== 구성비 (원형) =====
addStyledChart(slide, pptx, 'PIE',
  [{ name: '점유율', labels: ['제품A','제품B','제품C','기타'],
     values: [45, 25, 20, 10] }],
  { x: 3, y: 1.5, w: 7, h: 5, title: '제품별 매출 구성비' }
);

// ===== 진행률 (도넛) =====
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행률', labels: ['완료','잔여'], values: [75, 25] }],
  { x: 4, y: 2, w: 5, h: 4, title: '프로젝트 진행률',
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
);
```

### 3. addImage() — 이미지

```javascript
// 파일 경로로 삽입
slide.addImage({
  path: '/path/to/image.png',
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// SVG → PNG 변환 후 삽입 (sharp 라이브러리)
const sharp = require('sharp');
const svgBuffer = Buffer.from(svgString);
const pngBuffer = await sharp(svgBuffer).png().toBuffer();
const base64 = pngBuffer.toString('base64');
slide.addImage({
  data: 'image/png;base64,' + base64,
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// 로고 삽입 (우측 하단)
slide.addImage({
  path: '/path/to/logo.png',
  x: 11.5, y: 6.8, w: 1.2, h: 0.5
});
```

### 4. addText() — 텍스트

```javascript
// 제목
slide.addText('슬라이드 제목', {
  x: 0.6, y: 0.65, w: 10, h: 0.6,
  fontSize: 28, fontFace: 'Pretendard', bold: true,
  color: COLORS.text_primary, charSpacing: -0.3
});

// 글머리 기호 목록 (bullet: true)
slide.addText([
  { text: '첫 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '두 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '하위 항목', options: { bullet: true, indentLevel: 1 } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 4,
  fontSize: 16, fontFace: 'Pretendard',
  color: COLORS.text_secondary,
  lineSpacingMultiple: 1.5,
  paraSpaceAfter: 6
});

// 번호 목록 (bullet: {type:'number'})
slide.addText([
  { text: '첫 번째 단계', options: { bullet: { type: 'number' } } },
  { text: '두 번째 단계', options: { bullet: { type: 'number' } } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 3,
  fontSize: 16, fontFace: 'Pretendard',
  color: COLORS.text_secondary
});

// 인용문 (명조체)
slide.addText('\u201C변화를 두려워하지 마세요\u201D', {
  x: 2, y: 3, w: 9, h: 1,
  fontSize: 22, fontFace: 'ChosunilboNM', italic: true,
  color: COLORS.text_tertiary, align: 'center'
});
```

### 5. addShape() — 장식/레이아웃 보조만

```javascript
// ✅ 올바른 사용: 배경 영역
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: { color: COLORS.bg_dark }
});

// ✅ 올바른 사용: 악센트 라인
slide.addShape('rect', {
  x: 0.6, y: 0.5, w: 1.2, h: 0.06,
  fill: { color: COLORS.accent_blue }
});

// ✅ 올바른 사용: 카드 배경 (둥근 모서리)
slide.addShape('roundRect', {
  x: 0.6, y: 1.8, w: 5.5, h: 3,
  rectRadius: 0.1,
  fill: { color: 'FFFFFF' },
  shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
});

// ✅ 올바른 사용: 구분선
slide.addShape('line', {
  x: 0.6, y: 4, w: 12.13, h: 0,
  line: { color: 'E2E8F0', width: 0.5 }
});

// ❌ 금지: 표 격자를 도형으로 그리기
// ❌ 금지: 막대 차트를 사각형으로 그리기
```

### 6. addNotes() — 발표자 노트

```javascript
slide.addNotes('이 슬라이드에서는 매출 추이를 설명합니다.\n핵심 포인트: Q3 성장률 40% 강조');
```

---

## PptxGenJS 코드 컨벤션

### 폰트 임베딩

```javascript
// Pretendard OTF 경로 (스킬 폴더 기준)
const FONT_DIR = path.join(__dirname, 'fonts');

// PptxGenJS에서 폰트 등록은 지원하지 않으므로
// 시스템에 Pretendard가 설치된 환경에서 다음과 같이 사용:
const FONTS = {
  title:    { fontFace: 'Pretendard', bold: true },   // ExtraBold/Black
  subtitle: { fontFace: 'Pretendard', bold: true },   // SemiBold/Bold
  body:     { fontFace: 'Pretendard', bold: false },   // Regular/Medium
  caption:  { fontFace: 'Pretendard', bold: false },   // Light/Regular
  serif:    { fontFace: 'ChosunilboNM', bold: false }, // 조선일보명조
  kpi:      { fontFace: 'Pretendard', bold: true },    // Black
  deco:     { fontFace: 'Pretendard', bold: false },   // Thin/ExtraLight (장식용)
};
```

### 슬라이드 생성 헬퍼

```javascript
// 표준 제목 바 추가 함수
function addTitleBar(slide, title, subtitle = '') {
  // 얇은 accent 라인
  slide.addShape('rect', {
    x: 0.6, y: 0.5, w: 1.2, h: 0.06,
    fill: { color: COLORS.accent_blue }
  });
  // 제목
  slide.addText(title, {
    x: 0.6, y: 0.65, w: 10, h: 0.6,
    fontSize: 28, fontFace: 'Pretendard', bold: true,
    color: COLORS.text_primary, charSpacing: -0.3
  });
  // 부제목 (있을 경우)
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.6, y: 1.25, w: 10, h: 0.4,
      fontSize: 16, fontFace: 'Pretendard',
      color: COLORS.text_tertiary
    });
  }
}

// 카드 생성 함수 (장식용 - 데이터 표시 아님)
function addCard(slide, { x, y, w, h, title, body, accentColor }) {
  // 카드 배경
  slide.addShape('roundRect', {
    x, y, w, h, rectRadius: 0.1,
    fill: { color: 'FFFFFF' },
    shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
  });
  // 상단 accent 바
  slide.addShape('rect', {
    x: x + 0.02, y, w: w - 0.04, h: 0.06,
    fill: { color: accentColor || COLORS.accent_blue }
  });
  // 카드 제목
  slide.addText(title, {
    x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.35,
    fontSize: 16, fontFace: 'Pretendard', bold: true,
    color: COLORS.text_primary
  });
  // 카드 본문
  slide.addText(body, {
    x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.75,
    fontSize: 13, fontFace: 'Pretendard',
    color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, valign: 'top'
  });
}

// 페이지 번호 추가
function addPageNumber(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 12.0, y: 7.05, w: 1.0, h: 0.3,
    fontSize: 9, fontFace: 'Pretendard',
    color: COLORS.text_tertiary, align: 'right'
  });
}
```

## 실전 슬라이드 구성 패턴

### 패턴 A: 매출 보고 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '월별 매출 실적', '2026년 상반기');

// 상단: KPI 카드 3개 (addText + addShape)
// → KPI 숫자는 카드 형태 = addShape(배경) + addText(숫자)
['매출 합계|₩3.2B', '전년 대비|+18%', '목표 달성률|94%'].forEach((item, i) => {
  const [label, value] = item.split('|');
  addCard(slide, {
    x: 0.6 + i * 4.1, y: 1.6, w: 3.8, h: 1.2,
    title: label, body: value, accentColor: CHART_STYLE.colors[i]
  });
});

// 중단: 데이터 테이블 (addTable)
addStyledTable(slide, ['월','매출','비용','영업이익','이익률'], [...data],
  { y: 3.1, rowH: [0.4, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35] });
```

### 패턴 B: 비교 분석 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '경쟁사 비교 분석');

// 좌측: 비교 차트 (addChart)
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '자사', labels: ['가격','품질','서비스','인지도'], values: [85, 92, 88, 70] },
    { name: '경쟁A', labels: ['가격','품질','서비스','인지도'], values: [90, 80, 75, 85] }
  ],
  { x: 0.6, y: 1.6, w: 6.5, h: 5.2, title: '' }
);

// 우측: 비교표 (addTable)
addStyledTable(slide, ['항목','자사','경쟁A'],
  [['가격', '85', '90'], ['품질', '92', '80'], ['서비스', '88', '75']],
  { x: 7.5, y: 1.6, w: 5.2 }
);
```

### 패턴 C: 프로젝트 현황 대시보드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '프로젝트 현황 대시보드', '2026년 2월 기준');

// 좌측 상단: 진행률 도넛 (addChart)
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행', labels: ['완료','잔여'], values: [72, 28] }],
  { x: 0.6, y: 1.6, w: 4, h: 3, showTitle: false,
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
);

// 우측 상단: 주간 이슈 테이블 (addTable)
addStyledTable(slide, ['이슈','담당','상태','기한'],
  [['서버 지연', '김개발', '진행중', '2/20'],
   ['UI 버그', '박디자', '완료', '2/18']],
  { x: 5, y: 1.6, w: 7.7, rowH: [0.4, 0.35, 0.35] }
);

// 하단: 마일스톤 타임라인 (addTable로 구현 가능)
addStyledTable(slide, ['마일스톤','시작일','종료일','진행률','상태'],
  [['기획', '1/15', '2/10', '100%', '\u2705'],
   ['개발', '2/11', '4/30', '45%', '\uD83D\uDD27'],
   ['테스트', '5/1', '5/31', '0%', '\u23F3']],
  { x: 0.6, y: 5.0, w: 12.13, rowH: [0.4, 0.35, 0.35, 0.35] }
);
```

---

