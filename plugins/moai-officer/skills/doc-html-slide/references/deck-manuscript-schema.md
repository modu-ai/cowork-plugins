# deck.json — 슬라이드 원고 SSOT 스키마

`deck.json`은 doc-html-slide의 **단일 진실 원천(Single Source of Truth)**입니다. HTML 렌더와 doc-pptx PPTX 렌더 양쪽이 같은 원고를 소비합니다. 픽셀→OOXML 역매핑이 아니라 **원고→객체 직접 생성**이 "편집 가능 PPTX"의 보증 기구입니다.

## 최상위 구조

```json
{
  "meta": {
    "title": "2026년 하반기 사업 전략",
    "design_system": "claude",
    "aspect_ratio": "16:9",
    "locale": "ko",
    "presenter": "김모AI",
    "date": "2026-06-17",
    "slide_count": 8
  },
  "slides": [ { ... }, { ... } ]
}
```

## 슬라이드 객체 스키마

```json
{
  "id": "s3",
  "layout": "data-chart",
  "layout_key": "stats",
  "title": "분기별 매출 추이",
  "subtitle": "전년 동기 대비 +34%",
  "bullets": ["B2B SaaS 매출 1,234억", "신규 고객 217% 증가"],
  "chart": {
    "type": "bar",
    "data": { "labels": ["Q1","Q2","Q3","Q4"], "values": [320, 480, 610, 920], "unit": "억 원" }
  },
  "image": {
    "backend": "higgsfield",
    "prompt": "abstract ascending bar chart hero, warm coral palette",
    "path": "assets/hero-q3.png"
  },
  "svg": "<svg viewBox='0 0 1280 720'>...</svg>",
  "notes": "이 슬라이드에서는 Q3 성장의 핵심 요인인 엔터프라이즈 확장을 강조합니다."
}
```

### 필드 규약

| 필드 | 필수 | 설명 |
|------|------|------|
| `id` | ✓ | 슬라이드 고유 식별자 (`s1`, `s2`...) |
| `layout` | ✓ | HTML 렌더 레이아웃 키 (아래 카탈로그) |
| `layout_key` | ✓ | doc-pptx 9 아키타입 매핑 (아래 매핑 표) |
| `title` | ✓ | 슬라이드 헤드라인 (한국어 권장) |
| `subtitle` | — | 부제·보조 카피 |
| `bullets` | — | 불릿 포인트 배열 (50단어 이하 권장) |
| `icons` | 배열 (선택) | 아이콘 슬롯. `bullets`와 **같은 순서·같은 개수**. 각 항목은 `{icon, icon_reason}`. 아이콘을 쓰지 않는 레이아웃은 생략 |
| `chart` | — | 차트 데이터 (type + data). SVG로 렌더 + doc-pptx 네이티브 차트로 매핑 |
| `image` | — | 비트맵 이미지 (backend + prompt + path). SVG 불가능한 실사·히어로만 |
| `svg` | — | 인라인 SVG 직접 저작 (인포그래픽). chart와 병용 가능 |
| `notes` | — | 발표자 노트 (speaker notes) |

## HTML 레이아웃 카탈로그 (`layout`)

| layout | 용도 | 핵심 요소 |
|--------|------|-----------|
| `title` | 표지 | 큰 제목 + 부제 + 발표자·날짜 |
| `agenda` | 목차 | 섹션 리스트 + 진행 표시 |
| `section` | 섹션 구분자 | 큰 섹션 번호 + 제목 |
| `single-message` | 핵심 메시지 1개 | 큰 문장 + 보조 설명 |
| `data-chart` | 데이터 시각화 | 차트 SVG + KPI + 인사이트 |
| `comparison` | 비교 (A vs B) | 2-3단 비교 카드 |
| `timeline` | 타임라인 | 수평/수직 마일스톤 |
| `quote` | 인용구 | 큰 인용문 + 출처 |
| `features-grid` | 기능 그리드 | 3-6 카드 + 아이콘 (아이콘 슬롯은 아래 §아이콘 슬롯 계약 준수) |
| `stats` | 통계 강조 | 큰 숫자 3-4개 |
| `cta` | 행동 요청 | 강조 박스 + 액션 |
| `closing` | 마무리·Q&A | 감사 + 연락처 |

## 아이콘 슬롯 계약

[HARD] 아이콘을 두는 슬롯은 `icon`과 **`icon_reason`을 함께** 적는다. `icon_reason`은 "왜 이 문구에 이 아이콘인가"를 한 줄로 적는 필드이며, 비어 있으면 루브릭 #33 hard-fail이다.

슬라이드의 `icons` 배열에 슬롯 순서대로 적는다 — `bullets`와 같은 순서다.

```json
"bullets": ["단일 파일 HTML — 브라우저 즉시 오픈", "인라인 SVG 인포그래픽 — 한국어 100% 정확"],
"icons": [
  { "icon": "app-window",  "icon_reason": "'브라우저 즉시 오픈' — 창을 여는 행위" },
  { "icon": "bar-chart-3", "icon_reason": "'인포그래픽' — 수치를 그림으로 보여주는 산출물" }
]
```

이 필드는 서식이 아니라 **강제 장치**다. 아이콘은 레이아웃상 빈 자리로 보이기 때문에, 근거를 요구하지 않으면 손에 잡히는 몇 개를 돌려쓰게 된다 — 실제로 어떤 덱에서 아이콘 자리 169개에 고유 모양 11종만 쓰이고, "색이 흐려집니다"에 종이비행기, "박수는 한 번에 칩니다"에 원이 배정된 사례가 있다. 한 줄을 쓰게 하면 그 자리에서 어긋남이 드러난다.

세 가지를 지킨다:

- **문구의 동사에서 고른다.** 적는다 → 메모·연필, 멈춘다 → 정지·손, 견준다 → 저울·막대. 명사(주제어)가 아니라 그 슬롯이 시키는 **행동**에 맞춘다.
- **한 덱에서 같은 아이콘을 3회 넘게 쓰지 않는다.** 넘으면 그 아이콘이 의미를 잃는다.
- **상태·순서·범례처럼 일관된 표기로 반복할 때만** 슬롯에 `"icon_role": "status" | "nav" | "legend"` 를 선언하고 **6회까지** 쓴다. 이 세 값 외에는 쓰지 않으며, 선언해도 6회를 넘기지 못한다. 루브릭 #32와 같은 값이다.
- **마땅한 아이콘이 없으면 비운다.** 자리를 채우려고 무관한 모양을 넣지 않는다 — 빈 자리가 틀린 아이콘보다 낫다.
- **[HARD] `icon_reason`은 문구의 행동을 지목해야 한다.** "아이콘이 필요해서"·"어울려서"·아이콘 이름 되풀이("폴더라서")·문구 그대로 복사는 근거가 아니다. 루브릭 #33이 이 형태를 fail로 잡는다. 근거를 한 줄로 못 쓰겠으면 그건 맞는 아이콘이 아니라는 신호다 — 비운다.

## doc-pptx 아키타입 매핑 (`layout_key`)

HTML `layout` → doc-pptx 9 아키타입(Title/Agenda/Problem/Solution/Features/Stats/Team/CTA/Closing) 매핑:

| HTML layout | doc-pptx layout_key | 비고 |
|-------------|--------------------------|------|
| `title` | `title` | 표지 |
| `agenda` | `agenda` | 목차 |
| `section` | `agenda` | 섹션 구분자는 agenda 변형 |
| `single-message` | `problem` 또는 `solution` | 문맥에 따라 |
| `data-chart` | `stats` | chart-data는 네이티브 차트(addChart)로 |
| `comparison` | `features` | 비교 카드는 features 그리드 변형 |
| `timeline` | `features` | 마일스톤 = features 시퀀스 |
| `quote` | `solution` | 인용 = 핵심 메시지 변형 |
| `features-grid` | `features` | 1:1 매핑 |
| `stats` | `stats` | 1:1 매핑 |
| `cta` | `cta` | 1:1 매핑 |
| `closing` | `closing` | 1:1 매핑 |

> 매핑이 깔끔하지 않은 복잡한 인포그래픽(예: 다중 다이어그램)은 PPTX에서 비트맵 이미지로 삽입될 수 있습니다(편집 불가, 한계 명시). chart-data가 있으면 반드시 네이티브 차트로 매핑해 편집 가능성을 보존합니다.

## 편집 가능 PPTX 보증 원칙

1. **원고→객체 직접 생성**: doc-pptx의 pptxgenjs가 deck.json 원고를 OOXML 객체(addText/addChart/addImage/addShape)로 직접 생성 — 픽셀 역매핑이 아님
2. **chart-data 보존**: `chart` 필드가 있으면 doc-pptx 네이티브 차트로 재생성 → PowerPoint에서 데이터 편집 가능
3. **텍스트·불릿 보존**: title/bullets/notes는 텍스트 객체 → 편집 가능
4. **비트맵은 편집 불가**: image.path의 실사 이미지는 PPTX에서도 이미지 객체(편집 불가, 본질적 한계)
5. **한국어 폰트**: doc-pptx theme(headFontFace/bodyFontFace = Pretendard/맑은 고딕) + ea(east-asian) typeface 매핑
