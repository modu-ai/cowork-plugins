---
name: midjourney-v8-prompt
description: |
  Midjourney v8.1 (2026.03 Alpha) 전용 이미지 프롬프트 빌더. 사용자 자연어 한 줄 + AskUserQuestion 프리셋·미세조정으로 컨텍스트를 수집해 Midjourney 공식 Parameter List 기반 키워드+`--파라미터` 형식으로 변환합니다. Discord `/imagine` 또는 alpha.midjourney.com에 그대로 복붙 가능. `--sref`/`--oref`/`--cw`/`--p`/`--hd`/`--q 4`/`--style raw`/`--no`/`--c`/`--s` 모두 지원. 보너스로 GPT-image-2(6-Block) · Gemini 3 Pro Image(5-component) 프롬프트도 동시 출력합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "미드저니 프롬프트 만들어줘", "MJ 프롬프트"
  - "Midjourney 프롬프트", "/imagine 프롬프트 작성"
  - "Midjourney v8 프롬프트", "미드저니 8.1 프롬프트"
  - "--sref 프롬프트", "--oref 프롬프트", "스타일 코드 프롬프트"
  - "/midjourney-v8-prompt" (직접 호출)

  Midjourney는 공식 API 자동화가 제한적이므로 본 스킬은 프롬프트 텍스트만 산출하고, 실제 생성은 사용자가 Discord 또는 web alpha에서 직접 실행합니다.
user-invocable: true
version: 2.27.0
---

# Midjourney v8.1 Prompt Builder — 키워드+파라미터 + 3-모델 동시 출력

> moai-media | 이미지 프롬프트 빌더 (텍스트 산출 전용)

## 개요

Midjourney v8 Alpha (2026.03.17 출시) 및 v8.1 (2026.03.21 announce)은 5배 빠른 생성, native 2K (`--hd`), extra coherence (`--q 4`), 개선된 텍스트 렌더링, `--stylize` 1000까지 권장, 새로운 `--sv 7` Style Reference·Moodboards 모델을 도입했습니다. 본 스킬은 사용자 한 줄 요청을 Midjourney 공식 Parameter List 기반 구조로 변환합니다:

```
[subject], [scene keywords], [composition], [lighting], [style]
--ar W:H --style raw --hd --q 4 --s 0~1000
[--sref CODE|URL --sw N] [--oref URL --cw 0~100]
[--p PROFILE] [--no NEGATIVE] [--c 0~100]
```

특히 본 스킬은:

- **3개 모델 동시 출력**: Midjourney 메인 + GPT-image-2(6-Block) + Gemini 3 Pro Image(5-component)
- **프리셋 + 미세조정**: 4 프리셋 × 4 슬롯
- **함정 경고 자동화**: `--cw 100` 기본값 함정, `--hd` + `--q 4` + `--sref` = 4x cost, `--cref` deprecated
- **Personalization 통합**: `--p PROFILE_ID` 또는 `--profile PROFILE_ID` 안내
- **Style Code 라이브러리**: `--sref CODE` 자주 쓰이는 코드 참조

## 트리거 키워드

미드저니 프롬프트 MJ 프롬프트 Midjourney 프롬프트 imagine 프롬프트 Midjourney v8 미드저니 8.1 sref 프롬프트 oref 프롬프트 스타일 코드 프롬프트 personalization 프로파일

## 워크플로우

```
사용자 자연어 한 줄
    ↓
[Round 1] AskUserQuestion — 프리셋 선택
    ↓
[Round 2] AskUserQuestion — 프리셋별 미세조정 (3~4 슬롯)
    ↓
[Round 3] AskUserQuestion — 화면비 + 텍스트 + 고급 옵션(--sref·--oref·--p·--no)
    ↓
[내부] 슬롯 → 키워드 콤마 + --파라미터 매핑
    ↓
[내부] 같은 슬롯 → GPT 6-Block + Gemini 5-component 변환
    ↓
[내부] 함정 검사 (--cw 100·4x cost·v8 비호환 옵션)
    ↓
출력: 3개 모델 프롬프트 + 비용 경고 + 한국어 해설
```

## 실행 규칙

### Round 1 — 프리셋 선택 (필수)

`presets/`의 4개 프리셋 (제품샷·인물·일러스트·풍경) 중 선택. gpt-image-2-prompt와 동일한 슬롯 데이터를 공유합니다.

### Round 2 — 프리셋별 미세조정 (3-4 질문)

`presets/<name>.md` 슬롯 정의를 따릅니다.

### Round 3 — 화면비 + 텍스트 + 고급 옵션

#### Q1 — 화면비 (`--ar`)

| 화면비 | `--ar` | 용도 |
|---|---|---|
| 1:1 (권장) | `--ar 1:1` | SNS 정사각 |
| 16:9 | `--ar 16:9` | 와이드, 유튜브 |
| 9:16 | `--ar 9:16` | 릴스·쇼츠 |
| 4:5 | `--ar 4:5` | 인스타 피드 |
| 3:2 | `--ar 3:2` | 사진 표준 |
| 2:3 | `--ar 2:3` | 책 표지 |

#### Q2 — 화질·스타일 (`--hd`, `--q`, `--style`, `--s`)

| 옵션 | 동작 | 비용 |
|---|---|---|
| 기본 | 표준 화질·자동 스타일 | 1x |
| `--style raw` | 자연색·photographic, 모델 개입 최소 | 1x |
| `--hd` | native 2K | 4x |
| `--q 4` | extra coherence | 4x |
| `--hd --q 4` | 둘 다 | **16x** ⚠️ |
| `--s 0~1000` | stylize (default 100) | 동일 |

**비용 주의**: `--hd` + `--q 4` + `--sref`/moodboard 조합은 **각각 4x** 비용 (곱연산). 자세한 함정은 `references/cost-traps.md`.

#### Q3 — 텍스트 (이미지 내 글자가 있을 때)

Midjourney v8은 텍스트 렌더링이 V6/V7보다 개선됐지만 GPT/Gemini만큼 정확하지 않음. 권장:

- 텍스트는 따옴표로 정확히: `"MONDAY"`
- 짧은 단어/단문 위주 (긴 문장은 깨질 위험)
- 영문이 한글보다 안정적

#### Q4 — 고급 옵션 (선택)

`AskUserQuestion`으로 추가 옵션 선택:

| 옵션 | 사용 | 메모 |
|---|---|---|
| Style Reference (`--sref`) | 특정 스타일 코드 또는 reference URL | 4x cost, `--sw 0~1000` 함께 |
| Omni Reference (`--oref`) | 캐릭터·객체 일관성 | 2x cost, `--cw 0~100` 함정 (default 100) |
| Personalization (`--p`) | 사용자 학습 프로파일 | 사전 setup 필요 (40 ratings 시작, 200 stable, 2000 max) |
| Negative (`--no`) | 제외할 요소 | 예: `--no people, --no text` |
| Chaos (`--c 0~100`) | 결과 다양성 | 시안용 |

상세 사용법은 `references/style-references.md`.

### 내부 처리 — 키워드 콤마 + --파라미터 매핑

```
[subject], [scene keywords], [composition keywords],
[lighting keywords], [style/medium keywords] --ar W:H
--style raw --hd --q 4 --s 250
```

`references/prompt-blocks.md`의 키워드 분류 가이드를 참조.

### 내부 처리 — 함정 검사

본 스킬은 출력 전에 다음을 자동 검사하고 경고를 한국어 해설에 포함:

1. `--cw` 미지정 시 → "Default 100. 얼굴만 가져오려면 `--cw 20~40`" 안내
2. `--hd --q 4 --sref` 조합 → "각 4x cost, 총 64x GPU 시간" 경고
3. v8 비호환 옵션 (`--cref`, V6 specific 등) → 자동 제거 또는 deprecated 메모
4. `--sref random` → 결과 재현 불가, 코드 확인 안내

### 출력 — 3개 모델 코드블록

```markdown
## 🎨 생성된 프롬프트 (3개 모델)

### 1) Midjourney v8.1 (메인)
```
<subject>, <scene>, <composition>, <lighting>, <style>
--ar 1:1 --style raw --hd --q 4 --s 300
```
**비용 추정**: `--hd` 4x × `--q 4` 4x = 16x GPU 시간 (relax 모드 권장)
**Personalization 활용**: `--p YOUR_PROFILE_ID` 추가 시 일관된 스타일

### 2) GPT-image-2 — OpenAI ChatGPT / API
```
<6-Block 자연어 단락>
```
**권장 파라미터**: `quality=medium`, `size=1024x1024`

### 3) Gemini 3 Pro Image — Nano Banana Pro
```
<5-component 영문 문장>
```
**권장 파라미터**: `aspect_ratio=1:1`, `resolution=2K`, `mode=Thinking`

### 📝 한국어 해설
- Midjourney v8은 키워드 콤마 + `--파라미터` 어조에 최적화
- 텍스트 정확도: GPT/Gemini > MJ. 긴 글자는 GPT 권장
- `--cw 100` 함정: reference 이미지의 조명·스타일까지 상속됨

### 🔗 페어 스킬
- `gpt-image-2-prompt` — GPT 어조 (sibling)
- `gemini-3-image-prompt` — Gemini 어조 (sibling)
- Midjourney 실행은 Discord `/imagine` 또는 alpha.midjourney.com에서 직접
```

## 사용 예시

**예시 1: 제품샷**
> "Midjourney 프롬프트, 매트 블랙 머그 'MONDAY' 글자 제품샷, 1:1, --hd"

→ Round 1: 제품샷 → Round 2: 머그/슬레이트/창문/3-4분 → Round 3: 1:1 + "MONDAY" + `--hd` 활성화 → 3개 모델 출력 + 4x cost 경고.

**예시 2: 캐릭터 일관성 (`--oref`)**
> "미드저니 프롬프트로 같은 캐릭터 다른 장면, --oref [URL] --cw 50"

→ 인물·캐릭터 프리셋 → Round 2 → Round 3에서 `--oref URL` + `--cw 50` 입력 → 출력에 `--oref` 워크플로우 한국어 해설 + `--cw` 가이드.

**예시 3: Style Reference**
> "MJ 프롬프트 --sref 1234567890 --sw 200"

→ Round 1·2 → Round 3에서 sref 코드 + sw 입력 → 출력에 4x cost 경고 + `--sv 7` default 메모.

## 출력 형식

| 산출물 | 형식 | 설명 |
|---|---|---|
| Midjourney v8.1 프롬프트 | 키워드 콤마 + `--파라미터` 한 줄 | Discord `/imagine` 또는 alpha.midjourney.com 입력 |
| GPT-image-2 프롬프트 | 영문 6-Block 자연어 단락 | ChatGPT / API 복붙 |
| Gemini 3 Pro Image 프롬프트 | 영문 5-component 단락 | Google AI Studio / Vertex AI 복붙 |
| 비용 추정 | 멀티플라이어 (예: 16x) | --hd·--q·--sref·--oref 조합 |
| 한국어 해설 | 마크다운 | 함정·--cw·--sv·-personalization |

## 주의사항

- 본 스킬은 **프롬프트 텍스트만** 출력합니다. 실제 이미지 생성은 Discord 또는 alpha.midjourney.com에서 직접 실행하세요 (Midjourney 공식 API 자동화 제한).
- `--cref` (V6 캐릭터 일관성)는 V7·V8에서 **deprecated**. `--oref`로 자동 교체됩니다.
- `--cw 100`(기본값) 함정: reference 이미지의 조명·스타일까지 상속되어 새 프롬프트와 충돌. 얼굴만 가져오려면 `--cw 20~40`.
- `--hd`·`--q 4`·`--sref`/moodboard 각각 4x cost. 조합 시 곱연산.
- `--oref`는 Fast Mode·Draft Mode·Conversational Mode·`--q 4`와 비호환.
- V8 Alpha 초기에는 Relax Mode 미지원이었으나, V8.1에서 점진적 추가. 비용 민감 시 Relax 가용 여부 확인.
- `--sref random`은 결과 재현 불가. 마음에 드는 결과가 나오면 실제 코드 확인·저장.
- Personalization (`--p`)은 40 ratings부터 시작, 200 ratings에서 stable, 2000 ratings까지 개선.
- 모든 출력 이미지는 사용자 책임으로 사용 (저작권·초상권·브랜드).

## 관련 스킬

| 스킬 | 관계 | 설명 |
|---|---|---|
| gpt-image-2-prompt | sibling | 동일 입력으로 GPT 6-Block 어조 프롬프트 |
| gemini-3-image-prompt | sibling | 동일 입력으로 Gemini 5-component 어조 프롬프트 |
| Higgsfield MCP (Soul) | alternative | API 자동 생성 (시네마틱 이미지·캐릭터 단일 통합, MJ는 미포함) |

## 출처

1차 권장 출처 (공식):

- [Midjourney Documentation — Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Midjourney Documentation — Style Reference (`--sref`)](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Documentation — Omni Reference (`--oref`)](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Midjourney Documentation — Character Reference (deprecated `--cref`)](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
- [Midjourney Documentation Hub](https://docs.midjourney.com/hc/en-us/categories/32013335627533-Documentation)

업계 참고:

- [Blake Crosley — Midjourney V8.1 + V7 Reference Guide](https://blakecrosley.com/guides/midjourney)
- [AI Tools DevPro — Midjourney 2026: v8 Specs Manual](https://aitoolsdevpro.com/ai-tools/midjourney-guide/)
- [ArtPromptHQ — Ultimate Midjourney Prompt Packs Guide](https://www.artprompthq.com/blog/ultimate-midjourney-prompt-packs-parameters-settings/)

위 출처를 기반으로 V8.1 파라미터, `--sref`/`--oref` 동작, `--cw` 함정, 4x cost 매트릭스, Personalization rating 단계, V8 비호환 옵션을 도출했습니다.
