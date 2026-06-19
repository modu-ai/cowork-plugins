# pptx-designer 체이닝 규약 — 편집 가능 PPTX 산출

html-slide는 편집 가능 `.pptx`를 **직접 생성하지 않습니다**. `moai-office:pptx-designer` 체이닝으로 위임합니다. pptx-designer가 이미 pptxgenjs + HTML-First + 9 아키타입 + QA 파이프라인을 보유하고 있어, html-slide가 자체 구현하면 중복·책임 모호화가 발생하기 때문입니다.

## 핵심 기구: 원고 → OOXML 객체 직접 생성

편집 가능 PPTX(PowerPoint에서 텍스트/셰이프/차트/이미지를 실제로 수정 가능)는 **OOXML 객체 기반**이어야 합니다. HTML 픽셀 렌더링을 OOXML로 역매핑하는 자동 변환은 근본적 손실이 큽니다.

따라서 html-slide가 산출한 `deck.json` 원고를 SSOT로 pptx-designer에 전달하면, pptx-designer의 pptxgenjs가 **원고 → OOXML 객체를 직접 생성**합니다:

```
deck.json 원고 ─┬─→ HTML 렌더 (html-slide)
                └─→ PPTX 렌더 (pptx-designer, pptxgenjs)
                      title/bullets  → addText    (텍스트 객체, 편집 가능)
                      chart.data     → addChart   (네이티브 차트, 데이터 편집 가능)
                      image.path     → addImage   (이미지 객체, 편집 불가 - 본질적 한계)
                      layout_key     → 9 아키타입 시퀀스
```

## 의존성 안내 (중요)

pptx-designer는 `moai-office` 플러그인에 있습니다. **html-slide 단독 설치 사용자가 `export_pptx: true`를 요청하면**:
- moai-office 미설치 시 → PPTX 산출은 **blocker**로 보고, 설치 안내 (`/plugin install moai-office` 또는 마켓플레이스에서 moai-office 플러그인 추가)
- html-slide는 HTML만 산출하고 PPTX는 차후 안내

SKILL.md "입력" 섹션의 `export_pptx` 설명과 1단계 AskUserQuestion에서 이 의존성을 사전 안내합니다.

## design_system 승계 매핑

html-slide의 design_system(75 시스템) → pptx-designer의 10 큐레이션 팔레트 자동 매핑 규약:

| html-slide design_system | pptx-designer 팔레트 | 근거 |
|--------------------------|----------------------|------|
| `claude` (기본) | Claude Classic (Orange #d97757 / Beige #faf9f5) | 동일 Anthropic warm editorial |
| `clickhouse` | Dark Editorial (Orange / Dark #1a1a1a) | 다크 기술 |
| `clay` | Claude Coral (Crail #c15f3c) | playful saturated |
| `notion` | Claude Classic (warm minimalism 유사) | 밝은 편집성 |
| `spotify`·`nike` | High Contrast Bold | 임팩트 |
| 그 외 75개 | Claude Classic (기본 폴백) + 시스템 primary 색을 pptx-designer primary에 주입 | design-system-library 토큰 우선 |

> 매핑이 완벽하지 않아도 pptx-designer가 자체 10팔레트로 일관된 PPTX를 산출합니다. design_system 토큰의 primary/canvas 색을 pptx-designer의 colors 객체에 주입해 최대한 브랜드 정합.

## chart-data → 네이티브 차트 매핑 (편집 가능성 보증)

`deck.json`의 `chart` 필드가 있으면 pptx-designer가 **네이티브 차트**로 생성합니다 (이미지가 아님):

| deck.json chart.type | pptxgenjs ChartType | 편집 가능 |
|----------------------|---------------------|-----------|
| `bar` | `pptx.ChartType.bar` | ✅ 데이터 편집 |
| `line` | `pptx.ChartType.line` | ✅ |
| `donut`/`pie` | `pptx.ChartType.pie` | ✅ |
| `kpi` | (텍스트 객체, addText) | ✅ |

**중요**: 인라인 SVG 인포그래픽 중 chart-data가 있는 것은 반드시 네이티브 차트로 매핑합니다. SVG를 이미지로 삽입하면 편집 불가 이미지가 되어 "편집 가능 PPTX" 목표에 위배됩니다.

## 비권장 변환 경로 (사용 금지)

HTML→PPTX 자동 변환기는 CSS 절대좌표/grid 레이아웃을 OOXML 객체로 온전히 매핑하지 못해 손실이 큽니다. 다음 경로는 **사용 금지**:

| 변환기 | 문제 |
|--------|------|
| Marp `--pptx` (기본값) | 슬라이드를 래스터 배경 이미지로 삽입 → 편집 불가 |
| Marp `--pptx-editable` | 실험 옵션, 브라우저+LibreOffice 의존, 낮은 재현도, 발표자 노트 미지원 (공식 비권장) |
| DeckTape | PDF 전용 (PPTX 생성 안 함) |
| Aspose `AddFromHtml` | 상용 + 낮은 충실도, HTML 1페이지=슬라이드 1개 매핑 |
| LibreOffice `--convert-to pptx` | CSS positioned 레이아웃 손실 |

유일한 신뢰 경로 = **deck.json 원고 SSOT에서 HTML·PPTX 병행 생성** (html-slide + pptx-designer 체이닝).

## 체이닝 호출 패턴

```
# 1. html-slide가 deck.json + deck.html 산출
# 2. 사용자가 export_pptx 요청 시 pptx-designer에 deck.json 전달
"pptx-designer 스킬로 이 deck.json 원고를 편집 가능 .pptx로 렌더해줘.
 design_system은 claude(Claude Classic 팔레트) 승계,
 chart.data는 네이티브 차트로 매핑."
# 3. pptx-designer가 pptxgenjs로 .pptx 산출 + QA
# 4. html-slide가 pptx-designer QA 결과를 통합 보고
```

## 한국어 폰트 처리

pptx-designer theme으로 한국어 표준 폰트 지정:
```javascript
pptx.theme = { headFontFace: 'Pretendard', bodyFontFace: 'Pretendard' };
// pptxgenjs는 폰트 임베딩 미지원 → 발표 PC에 Pretendard/맑은 고딕 권장
// 폰트 미설치 환경 대비 PDF 백업 산출 권장
```

python-pptx 경로(체이닝 스킬이 Python 사용 시)는 run.font.name + ea(east-asian) typeface XML을 함께 세팅해야 완벽 매핑됩니다.

## 편집 가능성 보증 범위

PowerPoint·Keynote·LibreOffice Impress·Google Slides(임포트)에서:
- ✅ 텍스트 (한국어 run) — 편집 가능
- ✅ 표·불릿 — 편집 가능
- ✅ 네이티브 차트 (chart-data) — 데이터 편집 가능
- ✅ Auto shapes (셰이프) — 편집 가능
- ⚠️ 비트맵 히어로 이미지 — 편집 불가 (이미지, PPTX 본질적 한계)
- ⚠️ 복잡한 인라인 SVG 다이어그램 (chart-data 없음) — 비트맵 이미지로 삽입 (편집 불가, 한계 명시)
