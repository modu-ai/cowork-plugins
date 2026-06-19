---
name: gemini-3-image-prompt
description: |
  Google Gemini 3 Pro Image (a.k.a. Nano Banana Pro) 전용 이미지 프롬프트 빌더. 사용자 자연어 한 줄 + AskUserQuestion 프리셋·미세조정으로 컨텍스트를 수집해 Google AI Developers 공식 가이드의 5-component 구조([Subject+Adj] doing [Action] in [Location]. [Composition]. [Lighting]. [Style]. [Constraint/Text])로 변환합니다. Google AI Studio · Vertex AI · Gemini 앱에 그대로 복붙 가능. 보너스로 GPT-image-2(6-Block) · Midjourney v8.1(키워드+파라미터) 프롬프트도 동시 출력해 모델 간 비교·이식이 가능합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Gemini 이미지 프롬프트 만들어줘", "나노바나나 프롬프트"
  - "Nano Banana Pro 프롬프트", "Gemini 3 Pro Image 프롬프트"
  - "Google AI Studio 이미지 프롬프트", "Vertex AI 이미지 프롬프트"
  - "/gemini-3-image-prompt" (직접 호출)

  이미지 자동 생성은 페어 스킬 higgsfield-image(Higgsfield MCP, Nano Banana Pro 포함)를 사용하세요. 본 스킬은 프롬프트 텍스트 산출 전용입니다.
user-invocable: true
version: 2.27.0
---

# Gemini 3 Pro Image Prompt Builder — 5-Component + 3-모델 동시 출력

> moai-media | 이미지 프롬프트 빌더 (텍스트 산출 전용)

## 개요

Gemini 3 Pro Image (Nano Banana Pro)는 Google DeepMind의 reasoning-driven 이미지 생성·편집 모델로, **Thinking Mode**, **Perfect Text Rendering**, **Search Grounding** (Google Search 연동), **Few-Shot Design** (최대 14개 reference 이미지)을 지원합니다. 자연어 프롬프트 어조는 **Creative Director가 장면을 지시하는 톤**이 가장 잘 동작합니다.

본 스킬은 사용자 한 줄 요청을 Google AI for Developers 공식 가이드의 5-component 구조로 변환합니다:

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera]. [Lighting/Atmosphere]. [Style/Media].
[Specific Constraint/Text]
```

각 component는 영문 문장으로 끝나며 마침표로 구분합니다. 키워드 나열식은 동작하지만 결과 품질이 떨어집니다.

특히 본 스킬은:

- **3개 모델 동시 출력**: Gemini 5-component 메인 + GPT-image-2(6-Block) + Midjourney v8.1(키워드+파라미터)
- **프리셋 + 미세조정**: 4개 프리셋(제품샷·인물·일러스트·풍경) × 4 슬롯
- **Thinking vs Fast 모드 안내**: 복잡 구도·텍스트는 Thinking, 빠른 탐색은 Fast (Gemini 3.1 Flash Image)
- **카메라 하드웨어 지정**: GoPro · Fujifilm · disposable · iPhone 등 시각적 DNA를 결정하는 하드웨어 지시

페어 스킬 `higgsfield-image`(Higgsfield MCP — Nano Banana Pro 포함 11개 이미지 모델)가 실제 이미지를 생성하고, 본 스킬은 **프롬프트 텍스트만** 산출합니다.

## 트리거 키워드

Gemini 이미지 프롬프트 나노바나나 프롬프트 Nano Banana Pro 프롬프트 Gemini 3 Pro Image 프롬프트 Google AI Studio 이미지 Vertex AI 이미지 프롬프트 SynthID

## 워크플로우

```
사용자 자연어 한 줄
    ↓
[Round 1] AskUserQuestion — 프리셋 선택 (제품샷·인물·일러스트·풍경)
    ↓
[Round 2] AskUserQuestion — 프리셋별 미세조정 (3~4 슬롯)
    ↓
[Round 3] AskUserQuestion — 화면비 + 이미지 내 텍스트 유무 + 카메라 하드웨어(선택)
    ↓
[내부] 슬롯 → 5-component 매핑
    ↓
[내부] 같은 슬롯 → GPT 6-Block + MJ 키워드+파라미터 변환
    ↓
출력: 3개 모델 프롬프트 코드블록 + 권장 파라미터 + 한국어 해설
```

## 실행 규칙

### Round 1 — 프리셋 선택 (필수)

`AskUserQuestion`을 호출해 4개 프리셋 중 1개를 선택받습니다.

| 프리셋 | 적용 케이스 | references |
|---|---|---|
| 제품샷 (권장) | 커머스 상품, 패키지 컷, 보석·시계 클로즈업 | `presets/product-shot.md` |
| 인물·캐릭터 | 인물 포트레이트, 페르소나, 광고 모델 | `presets/portrait.md` |
| 일러스트·아트 | 카드뉴스 일러스트, 책 표지, 컨셉 아트 | `presets/illustration.md` |
| 풍경·환경 | 배경 이미지, 시네마틱 배경, 여행 컷 | `presets/landscape.md` |

### Round 2 — 프리셋별 미세조정 (3-4 질문)

`presets/<name>.md`의 슬롯 정의를 따릅니다. 본 스킬의 presets/는 gpt-image-2-prompt와 동일한 슬롯 데이터를 사용하지만, 모델별 어조 변환 가이드는 Gemini Creative Director 어조로 자동 변환됩니다.

### Round 3 — 화면비 + 텍스트 + 카메라 하드웨어(선택)

| 화면비 | Gemini 매핑 | 용도 |
|---|---|---|
| 1:1 (권장) | `aspect_ratio="1:1"` | SNS 정사각, 일반 |
| 16:9 | `"16:9"` | 와이드, 유튜브 |
| 9:16 | `"9:16"` | 릴스·쇼츠 |
| 4:5 | `"4:5"` | 인스타 피드 |
| 21:9 | `"21:9"` | 시네마틱 울트라와이드 (Gemini 전용) |

Gemini는 추가로 `3:2`, `2:3`, `3:4`, `4:3`, `5:4`를 지원합니다. Gemini 3.1 Flash Image는 `1:4`, `4:1`, `1:8`, `8:1`도 추가 지원.

**카메라 하드웨어 옵션** (Gemini Creative Director 어조의 핵심):

| 옵션 | 시각적 DNA |
|---|---|
| 기본 (DSLR 50mm) | 깨끗·중성·표준 |
| Fujifilm X-T5 | 따뜻한 색감, film simulation 어조 |
| GoPro HERO12 | 광각, 액션·몰입감, 약간 distortion |
| Disposable film camera | 거친 입자, nostalgic flash, raw 무드 |
| iPhone 15 Pro | 깨끗 디지털, computational photography |

### 내부 처리 — 슬롯 → 5-Component 매핑

```
Component 1 — [Subject + Adjectives] doing [Action] in [Location]
Component 2 — [Composition/Camera Angle/Lens/Hardware]
Component 3 — [Lighting/Atmosphere]
Component 4 — [Style/Media]
Component 5 — [Specific Constraint/Text]
```

각 component는 영문 문장 1-2개. 마침표로 구분. 상세 규칙은 `references/prompt-blocks.md`.

### 내부 처리 — GPT 6-Block + MJ 변환

페어 스킬 gpt-image-2-prompt / midjourney-v8-prompt와 동일 로직.

### 출력 — 3개 모델 코드블록

```markdown
## 🎨 생성된 프롬프트 (3개 모델)

### 1) Gemini 3 Pro Image — Nano Banana Pro (메인)
```
<5-component 영문 문장>
```
**권장 파라미터**: `aspect_ratio=1:1`, `resolution=2K`, `mode=Thinking`
**Reference 이미지**: 최대 14개 첨부 가능 (`references/reference-images.md`)
**Search Grounding**: 데이터 시각화·지도·통계 그래프는 활성화 권장

### 2) GPT-image-2 — OpenAI ChatGPT / API
```
<6-Block 자연어 단락>
```
**권장 파라미터**: `quality=medium`, `size=1024x1024`, `moderation=auto`

### 3) Midjourney v8.1
```
<키워드, 키워드, ... --ar 1:1 --style raw --hd --q 4 --s 300>
```

### 📝 한국어 해설
- Gemini는 Creative Director 어조에 가장 잘 반응합니다 (chiaroscuro · golden hour backlighting · three-point softbox 등)
- Thinking Mode는 복잡 구도·텍스트·데이터 시각화에 유리, latency 증가
- 모든 출력 이미지에 SynthID 워터마크 자동 삽입 (imperceptible)

### 🔗 페어 스킬 (실제 이미지 생성)
- `higgsfield-image` — Higgsfield MCP 직접 호출 (Nano Banana Pro 포함, 실제 이미지 생성)
- `gpt-image-2-prompt` — GPT 어조 프롬프트 빌더 (sibling)
- `midjourney-v8-prompt` — MJ 어조 프롬프트 빌더 (sibling)
```

### 텍스트-우선 (Text-First) 워크플로우

이미지에 들어갈 텍스트가 길거나 복잡할 때 Google이 공식 권장하는 2-step 패턴:

1. 먼저 모델과 대화로 텍스트 컨셉을 다듬는다 ("이런 분위기에 어울리는 짧은 카피 추천해줘").
2. 그 다음 확정된 텍스트를 이미지 프롬프트에 verbatim으로 넣는다.

본 스킬은 Round 3에서 텍스트 길이가 30자 이상이면 Text-First 패턴을 사용하라고 자동 권고합니다.

## 사용 예시

**예시 1: 제품샷**
> "Gemini 이미지 프롬프트, 매트 블랙 머그 'MONDAY' 글자 들어간 제품샷"

→ Round 1: 제품샷 → Round 2: 머그/슬레이트/창문/3-4분 → Round 3: 1:1 + verbatim "MONDAY" + Fujifilm → Gemini 메인 + GPT + MJ 동시 출력.

**예시 2: 인포그래픽 (Search Grounding)**
> "나노바나나 프롬프트로 2026년 한국 SNS 사용자 수 비교 인포그래픽"

→ 일러스트 프리셋 선택 → Round 2 슬롯 → Search Grounding 활성화 안내 + Thinking Mode 권장.

**예시 3: 시네마틱 풍경 21:9**
> "Gemini 3 Pro Image 시네마틱 풍경 프롬프트, 한강 일몰 21:9"

→ 풍경 프리셋 → Round 2 → 21:9 + GoPro 와이드 → Gemini만 21:9 지원 메모.

## 출력 형식

| 산출물 | 형식 | 설명 |
|---|---|---|
| Gemini 3 Pro Image 프롬프트 | 영문 5-component 단락 | Google AI Studio / Vertex AI / Gemini 앱 복붙 |
| GPT-image-2 프롬프트 | 영문 6-Block 자연어 단락 | ChatGPT / API 복붙 |
| Midjourney v8.1 프롬프트 | 키워드 + `--파라미터` | Discord `/imagine` 또는 alpha.midjourney.com |
| 권장 파라미터 | 모델별 aspect/quality/mode | API/UI 설정 시 함께 입력 |
| 한국어 해설 | 마크다운 | 어조 차이·Thinking 모드·SynthID·비용 주의 |

## 주의사항

- 본 스킬은 **프롬프트 텍스트만** 출력합니다. 실제 이미지 생성은 페어 스킬을 사용하세요.
- Gemini 3 Pro Image의 모든 출력에는 SynthID 워터마크가 imperceptible하게 삽입됩니다 (Google 정책, 변경 불가).
- Thinking Mode는 latency가 증가하지만, 복잡 구도·다중 객체·데이터 시각화·정확한 텍스트가 필요할 때 필수입니다.
- Search Grounding으로 사실 기반 인포그래픽을 생성하더라도, 결과는 항상 별도 검증 필요 (모델이 정보를 잘못 해석할 가능성).
- 입력 토큰: Gemini 3 Pro Image 65,536 tokens, Flash 131,072 tokens. 출력 토큰: 32,768 (둘 다).
- Reference 이미지 첨부 시 첫 2-3개에 핵심 요소(스타일·캐릭터·구도)를 배치하고, 나머지는 부수적 스타일로 사용 권장.
- 마스킹 편집·낮↔밤 변환·다중 이미지 블렌딩은 가끔 비자연스럽거나 아티팩트 발생.

## 관련 스킬

| 스킬 | 관계 | 설명 |
|---|---|---|
| gpt-image-2-prompt | sibling | 동일 입력으로 GPT 6-Block 어조 프롬프트 |
| midjourney-v8-prompt | sibling | 동일 입력으로 MJ 키워드+파라미터 프롬프트 |
| higgsfield-image | after | Higgsfield MCP 직접 호출로 실제 이미지 생성 (Nano Banana Pro 포함) |

## 출처

1차 권장 출처 (공식):

- [Google AI for Developers — Gemini 3 Pro Image Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Google DeepMind — Gemini 3 Pro Image product page](https://deepmind.google/models/gemini-image/pro/)
- [Google Cloud Documentation — Gemini 3 Pro Image (Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- [Google Cloud Blog — Ultimate Prompting Guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Google AI Studio — Gemini 3 Pro Image (Nano Banana Pro)](https://aistudio.google.com/models/gemini-3-pro-image)

업계 참고:

- [Atlabs AI — Ultimate Nano Banana Pro Prompting Guide 2026](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
- [WaveSpeed Blog — Google Nano Banana Pro: Complete Guide for 2026](https://wavespeed.ai/blog/posts/google-nano-banana-pro-complete-guide-2026/)
- [Medium — Testing Gemini 3 Pro Image](https://medium.com/google-cloud/testing-gemini-3-pro-image-f585236ae411)

위 출처를 기반으로 5-component 구조, Thinking/Fast 모드 권장, aspect_ratio 범위, 14 reference images, SynthID 정책, 65K/32K 토큰 제한, Search Grounding 활용을 도출했습니다.
