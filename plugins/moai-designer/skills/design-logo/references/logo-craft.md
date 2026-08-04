# logo-craft.md — recraft_v4_1 프롬프트 크래프트

> `design-logo` 참조 파일. 프롬프트를 조립할 때 연다.
> 생성 실행·비용·폴링은 `moai-media:media-higgsfield-core`에 위임한다. 이 파일은 프롬프트 크래프트만 다룬다.

## 핵심 원칙: 파라미터는 런타임 조회

모델 id·aspect_ratio·media role·컬러 파라미터는 **절대 하드코딩하지 않는다**. 생성 전 `models_explore(action:'get', model:'recraft_v4_1')`로 라이브 스키마를 확인한다 (→ `moai-media:media-higgsfield-core` 계약).

## Recraft 공식 프롬프트 6개 구성 요소

Recraft V4 공식 prompt engineering 가이드가 로고/벡터 작업을 위해 권장하는 뼈다. 프롬프트를 이 순서로 조립한다.

| # | 구성 요소 | 설명 |
|---|---|---|
| 1 | **Graphic type** | logo, icon set, symbol system, pictogram 중 명시 |
| 2 | **Shape logic** | geometry, symmetry, silhouette clarity 정의 |
| 3 | **Color system** | 엄격한 팔레트 (hex 병기) |
| 4 | **Line discipline** | 일관된 스트로크, 텍스처 회피 |
| 5 | **Layout structure** | centered, grid-based, scalable |
| 6 | **Constraints** | gradients, shadows 등 명시적 금지 |

Recraft V4는 "flat graphic logic"에서 비정상적으로 강하다. 표면 디테일보다 **구조적 정의**에 집중하고, 재질/질감/라이팅 묘사는 피한다.

## 디자이너 용어 사전 (recraft.md SSOT)

모델이 학습된 디자인 용어를 쓴다. 일상어("예쁜 로고")는 의도를 흐린다.

- `contained mark` — 정해진 영역 안에 담긴 마크
- `horizontal lockup` — 심볼+워드마크가 가로로 나란히
- `lettermark` — 글자 기반 마크
- `negative space cutout` — 여백이 형태를 만드는 기법
- `monoline style` — 일정한 굵기의 단일 선
- `ornate decorative border` — 화려한 장식 테두리
- `serif letterforms` — 세리프 글자 형태

## R1 — Negative prompt는 없다

Higgsfield MCP는 `negative_prompt`를 노출하지 않는다. 제외는 **긍정적 장면 묘사**로 바꾼다.
- ✗ "no gradients" → ✓ "flat solid fills only"
- ✗ "주황 쓰지 마" → ✓ "green and charcoal palette only"

## R3 — 리터럴 텍스트는 따옴표 + 폰트

워드마크/레터마크 텍스트는 따옴표로 감싸고 폰트를 함께 지정한다. 텍스트 렌더링의 단일 최고 레버리지 규칙.

> *"the word 'GLOW' in a geometric sans-serif font."*

## 컬러: 프롬프트 + hex 병기

> *"Strict two-tone palette only: deep saturated crimson for all characters and graphic elements on a soft warm cream background."*

> *"green and charcoal palette, deep green (#1b6e4a) with neutral charcoal (#2b2b2b)."*

정확한 색 파라미터 스키마는 unverified — `models_explore`로 라이브 확인 필수.

## 벡터 작업 금지 언어

texture, material, photographic, realistic, gradient, shadow, highlight, beveled edge, metallic effect. 벡터 로고는 "no texture, no gradients, consistent stroke, flat colors only"로 서술한다. (R1에 따라 이것도 긍정 서술 "flat solid fills only"로 바꾸는 것이 더 안전하다.)

## verbatim 예시

- *"Minimalist [subject] logo centered in composition, circular icon with brand name integrated as negative space cutout"*
- *"Line art icon logo...simple outline..., consistent stroke width, monoline style, clean and minimal, works at small sizes"*
- *"bold hand-drawn chunky wordmark with soft uneven strokes, rounded edges, imperfect spacing, and slightly irregular proportions"* (Recraft 공식)
- *"flat colors only — no gradients, shadows, or texture"* (Recraft 공식)

벤더 경고(verbatim): *"general prompts like 'a logo for a coffee shop' will produce something, but it probably won't be what you want."*

## 프롬프트 템플릿

```
[Graphic type] logo, [shape logic: silhouette/geometry/symmetry], [로고 타입: contained mark/lettermark/...],
[브랜드 마크 묘사 with negative space cutout/monoline style], [Color: palette + hex],
[Layout: centered/grid-based], flat solid fills only, consistent stroke, works at small sizes,
[워드마크면: the word 'NAME' in [font] font]
```

## 컨셉 탐색

로고는 한 방향이 아니라 여러 방향을 빠르게 탐색하는 것이 효과적이다. `count`(1-4)로 병렬 컨셉을 생성하고, 후보 중 가장 잠재력 있는 것을 고른 뒤 제약을 강화해 다듬는다.

## 출처
- Recraft — Practical Prompt Engineering: A Recraft V4 Guide — https://www.recraft.ai/blog/prompt-engineering-guide (WebFetch 검증)
- Recraft — AI Logo Maker Guide — https://www.recraft.ai/blog/ai-logo-maker-guide (WebFetch 검증)
- `moai-media:media-higgsfield-image` references/prompt-craft/recraft.md (SSOT, 1차 recraft.ai docs)
- `moai-media:media-higgsfield-core` references/universal-rules.md (R1-R5)
