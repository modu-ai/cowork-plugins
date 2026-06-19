---
name: gpt-image-2-prompt
description: |
  OpenAI GPT-image-2 모델 전용 이미지 프롬프트 텍스트 빌더. 사용자 자연어 한 줄 + AskUserQuestion 프리셋·미세조정 라운드로 컨텍스트를 수집하고, OpenAI Cookbook 공식 6-Block 구조(Subject·Action·Scene·Composition·Lighting·Style&Text)에 매핑해 ChatGPT·OpenAI API에 복붙 가능한 프롬프트를 출력합니다. 보너스로 같은 입력에 대한 Gemini 3 Pro Image · Midjourney v8.1 프롬프트도 함께 생성해 모델 간 비교·이식이 즉시 가능합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "GPT 이미지 프롬프트 만들어줘", "ChatGPT 이미지 프롬프트"
  - "GPT-image-2 프롬프트", "gpt image 2 프롬프트 작성"
  - "OpenAI 이미지 프롬프트", "GPT용 이미지 프롬프트 빌더"
  - "/gpt-image-2-prompt" (직접 호출)

  이미지 자동 생성은 페어 스킬 higgsfield-image(Higgsfield MCP)를 사용하세요. 본 스킬은 프롬프트 텍스트 산출 전용입니다.
user-invocable: true
version: 2.27.0
---

# GPT-image-2 Prompt Builder — 6-Block 구조 + 3-모델 동시 출력

> moai-media | 이미지 프롬프트 빌더 (텍스트 산출 전용)

## 개요

OpenAI GPT-image-2 모델은 자연어를 art-director 어조로 이해하는 reasoning-driven 이미지 모델입니다. 본 스킬은 사용자 한 줄 요청을 OpenAI Cookbook이 권장하는 **6-Block 구조**(Subject → Action → Scene → Composition → Lighting → Style & Text Constraints)로 풀어 써서 ChatGPT 또는 OpenAI API에 그대로 복붙할 수 있는 프롬프트를 출력합니다.

특히 본 스킬은:

- **3개 모델 동시 출력**: GPT-image-2 메인 프롬프트와 함께 동일한 의도를 Gemini 3 Pro Image(5-component)와 Midjourney v8.1(키워드+`--파라미터`) 어조로도 변환해 한 화면에 제공합니다.
- **프리셋 + 미세조정**: 4개 프리셋(제품샷·인물·일러스트·풍경)으로 학습 곡선을 낮추고, 프리셋별 3-4개 미세조정 질문으로 디테일을 확보합니다.
- **텍스트 verbatim 보장**: 이미지에 들어갈 글자는 따옴표·ALL CAPS·verbatim 지시로 GPT-image-2의 95%+ 텍스트 렌더링 정확도를 활용합니다.

본 스킬은 **프롬프트 텍스트만** 산출합니다. 사용자가 원하는 도구(ChatGPT 웹, Sora, OpenAI Playground 등)에서 직접 복붙해 사용하거나, **Higgsfield MCP**(Soul) 직접 호출로 이미지를 생성합니다.

## 트리거 키워드

GPT 이미지 프롬프트 ChatGPT 이미지 프롬프트 GPT-image-2 프롬프트 OpenAI 이미지 프롬프트 gpt image 2 프롬프트 GPT용 이미지 프롬프트 빌더 OpenAI 이미지 만들기

## 워크플로우

```
사용자 자연어 한 줄
    ↓
[Round 1] AskUserQuestion — 프리셋 선택 (제품샷·인물·일러스트·풍경)
    ↓
[Round 2] AskUserQuestion — 프리셋별 미세조정 (3~4 슬롯)
    ↓
[Round 3] AskUserQuestion — 화면비 + 이미지 내 텍스트 유무
    ↓
[내부] 슬롯 → 6-Block 매핑 (Subject·Action·Scene·Composition·Lighting·Style&Text)
    ↓
[내부] 같은 슬롯 → Gemini 5-component 변환 + MJ 키워드+파라미터 변환
    ↓
출력: 3개 모델 프롬프트 코드블록 + 권장 파라미터 + 한국어 해설
```

## 실행 규칙

### Round 1 — 프리셋 선택 (필수)

`AskUserQuestion`을 호출해 4개 프리셋 중 1개를 선택받습니다.

| 프리셋 | 적용 케이스 | references |
|---|---|---|
| 제품샷 (권장) | 커머스 상품 사진, 패키지 컷, 보석·시계 클로즈업 | `presets/product-shot.md` |
| 인물·캐릭터 | 인물 포트레이트, 페르소나 일러스트, 광고 모델 | `presets/portrait.md` |
| 일러스트·아트 | 카드뉴스 일러스트, 책 표지, 컨셉 아트 | `presets/illustration.md` |
| 풍경·환경 | 배경 이미지, 공간 사진, 시네마틱 배경 | `presets/landscape.md` |

선택 결과는 Round 2의 질문 세트를 결정합니다.

### Round 2 — 프리셋별 미세조정 (3-4 질문)

선택된 프리셋의 `presets/<name>.md`에 정의된 질문 세트를 `AskUserQuestion`으로 순회합니다. 각 질문은 4 옵션 + Other이며, 첫 번째 옵션에 `(권장)` 라벨을 표시합니다.

**제품샷 예시:**
1. 제품·소재 (예: 매트 블랙 세라믹 머그, 우드 트레이 + 가죽 노트북 슬리브)
2. 배경·표면 (예: 젖은 슬레이트 카운터, 베이지 리넨, 화이트 스튜디오)
3. 조명·시간대 (예: 창문 사이드 라이트 일출, 스튜디오 소프트박스, 골든아워)
4. 카메라 앵글·렌즈 (예: 3/4 앵글 50mm, 탑다운 35mm, 매크로 100mm)

다른 프리셋의 슬롯은 `presets/portrait.md`, `presets/illustration.md`, `presets/landscape.md`에서 정의됩니다.

### Round 3 — 화면비 + 텍스트 (1-2 질문)

| 화면비 옵션 | 용도 | 모델별 매핑 |
|---|---|---|
| 1:1 (권장) | SNS 정사각, 일반 | GPT `1024x1024`, Gemini `1:1`, MJ `--ar 1:1` |
| 16:9 | 유튜브 썸네일, 와이드 | GPT `1536x864`, Gemini `16:9`, MJ `--ar 16:9` |
| 9:16 | 인스타 릴스·쇼츠 | GPT `768x1344`, Gemini `9:16`, MJ `--ar 9:16` |
| 4:5 | 인스타 피드 | GPT `1024x1280`, Gemini `4:5`, MJ `--ar 4:5` |

이미지 내 텍스트가 있으면 별도 질문으로 정확한 문자열을 받습니다 (verbatim 보존을 위해).

### 내부 처리 — 슬롯 → 6-Block 매핑

수집된 슬롯을 OpenAI Cookbook의 6-Block 어조로 자연어 단락 1개로 풀어 씁니다. 키워드 나열식이 아닌 **art-director가 설명하는 어조**가 필수입니다. 상세 규칙은 `references/prompt-blocks.md`를 참조합니다.

| Block | 슬롯 매핑 | 어조 예 |
|---|---|---|
| Subject | 프리셋의 핵심 소재 슬롯 | "A matte black ceramic coffee mug with subtle ridge texture" |
| Action | 동작·배치 (없으면 정적) | "sitting on a wet slate countertop next to a folded linen napkin" |
| Scene | 배경·맥락 슬롯 | "in a minimalist Scandinavian kitchen at sunrise" |
| Composition | 앵글·렌즈 슬롯 | "three-quarter angle, 50mm lens, shallow depth of field" |
| Lighting | 조명 슬롯 | "soft directional window light, cool morning tone" |
| Style & Text | 스타일 + Round 3 텍스트 | "editorial product photography, natural film grain. The mug has \"MONDAY\" printed in thin uppercase sans-serif on the side, perfectly legible." |

텍스트 verbatim 규칙은 `references/text-rendering.md`에 정리되어 있습니다.

### 내부 처리 — Gemini 5-component 변환

동일 슬롯을 Gemini 3 Pro Image의 5-component 영문 문장형으로 변환합니다 (각 component는 마침표로 구분, Creative Director 어조).

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera]. [Lighting/Atmosphere]. [Style/Media].
[Specific Constraint/Text]
```

### 내부 처리 — Midjourney v8 키워드+파라미터 변환

동일 슬롯을 콤마 구분 키워드 + `--파라미터` 형식으로 변환합니다.

```
[subject], [scene keywords], [composition], [lighting], [style] --ar W:H --style raw --hd --q 4 --s 0~1000 [--sref CODE|URL --sw N] [--oref URL --cw 0~100] [--p PROFILE] [--no NEGATIVE]
```

파라미터 사용 가이드는 `references/parameter-cheatsheet.md`에 정리. 특히 `--cw 100`(기본값) 함정과 `--hd --q 4 --sref`의 4x cost 주의사항을 사용자에게 고지합니다.

### 출력 — 3개 모델 코드블록 + 한국어 해설 + 페어 스킬 안내

```markdown
## 🎨 생성된 프롬프트 (3개 모델)

### 1) GPT-image-2 — OpenAI ChatGPT / API
```
<6-Block 자연어 단락>
```
**권장 파라미터**: `quality=medium`, `size=1024x1024`, `moderation=auto`
**편집 시**: `references/editing-patterns.md`의 Change/Preserve/Constraints 2열 로직 적용

### 2) Gemini 3 Pro Image — Nano Banana Pro
```
<5-component 영문 문장>
```
**권장 파라미터**: `aspect_ratio=1:1`, `resolution=2K`, `mode=Thinking`

### 3) Midjourney v8.1
```
<키워드, 키워드, ... --ar 1:1 --style raw --hd --q 4 --s 300>
```
**비용 주의**: `--hd` + `--q 4` 조합은 4x GPU 시간

### 📝 한국어 해설
- 3개는 같은 장면이지만 어조가 다릅니다 (자연어 단락 / 5-component 문장 / 키워드+파라미터)
- 텍스트 정확도: GPT 95%+, Gemini 우수, MJ V8에서 개선됨

### 🔗 실제 이미지 생성
- **Higgsfield MCP**(Soul) — 시네마틱 이미지·캐릭터 단일 통합 직접 호출
- ChatGPT 웹·Sora·OpenAI Playground 직접 복붙
```

### 편집 워크플로우 (선택)

사용자가 "이 이미지를 편집해달라"고 요청하면 Round 2 대신 편집 모드로 진입해 GPT-image-2의 두 열 로직을 적용합니다.

```
Change: <바꿀 요소를 한 문장으로>
Preserve: <face·pose·lighting·framing·background·geometry·text·layout 중 잠금할 항목 나열>
Constraints: <no extra objects, no redesign, no logo drift, no watermark>
```

상세는 `references/editing-patterns.md`.

## 사용 예시

**예시 1: 제품샷 한 줄 요청**
> "GPT용 이미지 프롬프트 만들어줘. 매트 블랙 머그 'MONDAY' 글자 들어간 제품샷"

→ Round 1: 제품샷 선택 → Round 2: 머그/슬레이트 카운터/창문 조명/3-4분 앵글 슬롯 입력 → Round 3: 1:1 + "MONDAY" verbatim → 3개 모델 프롬프트 출력.

**예시 2: 인스타 릴스용 인물 프롬프트**
> "ChatGPT 이미지 프롬프트, 30대 여성 카페에서 노트북 보는 라이프스타일 컷, 9:16"

→ Round 1: 인물 선택 → Round 2: 30대 여성/카페·소품/표정·동작/배경 → Round 3: 9:16 + 텍스트 없음 → 3개 모델 프롬프트 + Sora 영상 변환 힌트.

**예시 3: 편집 모드**
> "기존 머그 이미지에서 머그 색만 빨강으로 바꾸는 GPT 프롬프트"

→ 편집 모드 진입 → Change/Preserve/Constraints 슬롯 수집 → GPT-image-2 편집용 프롬프트만 출력 (Gemini·MJ는 편집 메커니즘이 달라 별도 안내).

## 출력 형식

| 산출물 | 형식 | 설명 |
|---|---|---|
| GPT-image-2 프롬프트 | 영문 자연어 단락 (1개) | ChatGPT / API `prompt` 필드 복붙 |
| Gemini 3 Pro Image 프롬프트 | 영문 5-component 단락 | Google AI Studio / Vertex AI `prompt` 필드 복붙 |
| Midjourney v8.1 프롬프트 | 키워드 + `--파라미터` | Discord `/imagine` 또는 alpha.midjourney.com 입력 |
| 권장 파라미터 표 | 모델별 quality/size/aspect | API 호출 시 함께 설정 |
| 한국어 해설 | 마크다운 | 어조 차이·텍스트 정확도·비용 주의 |

## 주의사항

- 본 스킬은 **프롬프트 텍스트만** 출력합니다. 실제 이미지 생성은 페어 스킬을 사용하세요.
- GPT-image-2 4K 출력은 OpenAI가 experimental로 분류합니다. 일반 production은 1024 또는 2K 권장.
- Midjourney `--cw 100`(기본) 함정: reference 이미지의 조명·스타일까지 상속되어 새 프롬프트와 충돌할 수 있습니다. 얼굴만 가져오려면 `--cw 0~30`.
- 텍스트가 있는 이미지에서 GPT-image-2는 한국어·일본어·중국어·힌디어·벵골어 등 비라틴 문자도 처리하지만, 정확도를 위해 **따옴표 + verbatim 지시 + 폰트 무게·색·위치** 명시 필수.
- 모든 프롬프트는 사용자의 책임 하에 사용되며, 본 스킬은 저작권·초상권·브랜드 사용에 대한 책임을 지지 않습니다.
- Gemini 3 Pro Image 출력에는 SynthID 워터마크가 imperceptible하게 삽입됩니다 (Google 정책).

## 관련 스킬

| 스킬 | 관계 | 설명 |
|---|---|---|
| gemini-3-image-prompt | sibling | 동일 입력으로 Gemini 어조 최적화 프롬프트 산출 |
| midjourney-v8-prompt | sibling | 동일 입력으로 MJ 키워드+파라미터 프롬프트 산출 |
| higgsfield-image | after | 생성된 프롬프트로 Higgsfield MCP 직접 이미지 생성 (GPT Image 2·Nano Banana Pro 포함) |

## 출처

1차 권장 출처 (공식):

- [OpenAI Cookbook — GPT Image Generation Models Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [openai/openai-cookbook GitHub — image-gen-models-prompting-guide.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)

업계 참고:

- [Atlabs AI — The Ultimate GPT Image 2 Prompting Guide (2026)](https://www.atlabs.ai/blog/the-ultimate-gpt-image-2-prompting-guide-how-to-use-openai%E2%80%99s-best-image-model-2026)

위 출처를 기반으로 6-Block 구조, quality/size 권장값, 편집 2열 로직, 텍스트 verbatim 규칙을 도출했습니다.
