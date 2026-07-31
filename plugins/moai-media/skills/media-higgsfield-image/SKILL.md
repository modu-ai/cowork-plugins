---
name: media-higgsfield-image
description: |
  Higgsfield MCP 기반 AI 이미지를 자연어 요청 한 줄로 생성합니다. 모델·파라미터를 하드코딩하지 않고
  라이브 카탈로그(models_explore)를 조회해 호출하므로, 카탈로그가 바뀌어도 드리프트 없이 동작합니다.
  다음과 같은 요청 시 사용하세요:
  - "Higgsfield로 이미지 만들어 줘"
  - "Soul로 인물 이미지"
  - "Nano Banana Pro로 카드뉴스 이미지"
  - "AI 이미지 생성해줘"
  - "시네마틱 키 비주얼 만들어줘"
  - "캐릭터 일관성 있는 시리즈 이미지"
  - "DTC 광고 이미지(Marketing Studio)"
  Soul·Nano Banana·GPT Image·Seedream·FLUX·Recraft·Marketing Studio 등 계열의 프롬프트 크래프트는
  references/prompt-craft/*.md에 출처와 함께 큐레이션돼 있고, 실제 파라미터(모델 id·해상도·비율·비용)는
  런타임에 라이브 조회합니다. 프롬프트만 필요하면 moai-coworker의 *-prompt 스킬을 사용하세요.
version: "1.0.0"
---

# Higgsfield 이미지 생성 (media-higgsfield-image)

> `moai-media` | 라이브 카탈로그 기반 이미지 생성 (코어: `media-higgsfield-core`)

## 개요

Higgsfield MCP의 이미지 생성 도구를 호출하는 스킬입니다. 사용자 자연어 요청에서 의도를 추출하고, 계열 크래프트로 후보를 좁힌 뒤, **파라미터는 라이브 카탈로그에서 조회**해 생성합니다. 이전 스킬이 갖고 있던 하드코딩 모델 표·파라미터 표는 제거되었습니다 — 그 표들은 라이브 스키마와 어긋나 실패하는 호출을 낳았습니다.

핵심 설계는 코어 스킬 `media-higgsfield-core`에 있습니다:
- 호출 계약: `../media-higgsfield-core/references/call-schema.md`
- 라이브 조회 프로토콜: `../media-higgsfield-core/references/catalog-protocol.md`
- 공통 규칙 R1–R5: `../media-higgsfield-core/references/universal-rules.md`
- 잡·비용·리드백: `../media-higgsfield-core/references/job-lifecycle.md`

## 트리거 키워드

Higgsfield 이미지, Soul, Nano Banana, Nano Banana Pro, GPT Image, Seedream, FLUX, Recraft, Marketing Studio, DTC 광고 이미지, AI 이미지 생성, 시네마틱 이미지, 캐릭터 일관성

## 계열 크래프트 (references/prompt-craft/)

각 파일은 벤더 공식 문서 기반이며 출처·Evidence tier를 답니다. 파라미터가 아니라 **프롬프트 크래프트**만 다룹니다.

| 파일 | 계열 |
|---|---|
| `references/prompt-craft/soul.md` | Soul (공식 프롬프트 공식 부재 → R1–R5 폴백) |
| `references/prompt-craft/nano-banana.md` | Nano Banana (Google 5-part 공식) |
| `references/prompt-craft/openai.md` | GPT Image (openai_hazel 매핑은 unverified) |
| `references/prompt-craft/seedream.md` | Seedream (ByteDance 5원칙) |
| `references/prompt-craft/flux.md` | FLUX (어순 load-bearing, 부정 프롬프트 없음) |
| `references/prompt-craft/recraft.md` | Recraft (global-to-local, 벡터/로고) |
| `references/prompt-craft/marketing-studio.md` | Marketing Studio / DTC Ads (style 선택 워크플로) |

## 워크플로우 (REQ-010 흐름)

### 1단계 — 의도 파악 → 후보 좁히기

사용자 요청에서 subject·용도·톤·리터럴 텍스트 등 슬롯을 수집(→ core `interview-schema.md`)하고, 계열 크래프트로 **후보 모델을 좁힙니다**. 이 단계는 후보를 좁힐 뿐 파라미터를 단정하지 않습니다. 슬롯이 부족하면 스킬은 blocker 보고를 반환하고, 오케스트레이터가 사용자에게 확인합니다(스킬은 사용자에게 직접 질문하지 않음).

후보 좁히기 힌트(파라미터가 아니라 계열 선택 힌트):

| 사용자 표현 | 후보 계열 |
|---|---|
| "글자 정확하게", "포스터", "카드뉴스" | GPT Image 또는 Nano Banana Pro |
| "시네마틱", "인물 디테일", "캐릭터 일관성" | Soul |
| "사진처럼", "사실적", "제품 샷" | FLUX |
| "예술적", "독특한 톤" | Seedream |
| "로고", "아이콘", "벡터" | Recraft |
| "DTC 광고", "제품 광고 포맷" | Marketing Studio (ms_image) |

### 2단계 — 라이브 조회 (models_explore)

`models_explore(action:'get')`로 좁힌 후보 모델의 **실제 제약**(aspect_ratios·모델별 파라미터·media role)을 조회합니다. 범위 밖 모델(예: `z_image`, `grok_image`)이면 계열 크래프트가 없다는 것을 명시하고 **live lookup**으로 제약만 가져와 R1–R5를 적용합니다. Marketing Studio 계열이면 `show_marketing_studio`로 스타일 목록을 가져옵니다.

### 3단계 — 비용 프리플라이트 (get_cost)

같은 파라미터에 `get_cost: true`를 넣어 `credits`를 확인합니다(크레딧 0 소모). 응답의 `adjustments`가 있으면 서버가 채운 기본값이므로 리드백해 둡니다. 잔액 정지 규칙은 core `job-lifecycle.md`.

### 4단계 — 생성 (generate_image)

조회된 값으로만 실제 `generate_image`를 호출합니다. namespace는 런타임 해석(→ core `call-schema.md`). 참조 이미지는 `media_id`/`job_id`로만 전달합니다(URL 거부).

### 5단계 — 폴링·리드백

`job_status`로 `completed`까지 폴링하고, 결과 URL과 함께 반환된 `adjustments`를 사용자에게 보고합니다 — 요청과 다르게 서버가 치환한 것이 있으면 숨기지 않습니다.

## Marketing Studio (ms_image) 하드 규칙

`ms_image`는 `style_id`에 기본값이 없어 스타일 없이는 오류입니다. 반드시 `show_marketing_studio`로 스타일 목록을 보여주고 사용자가 이름으로 고르게 한 뒤 생성합니다. 스타일을 자동 기본값으로 채우지 않습니다(→ `references/prompt-craft/marketing-studio.md`).

## 범위 밖 모델 폴백 (live lookup)

15개 크래프트 계열에 없는 모델을 요청하면, 계열 특화 크래프트가 없다는 사실을 명시하고 `models_explore`로 제약을 **live lookup**한 뒤 공통 규칙 R1–R5를 적용합니다. 계열 파일이 없다고 모델을 못 쓰는 것은 아니지만, 그 사실을 사용자에게 알립니다.

## 출력 형식

```
## Higgsfield 이미지 생성 결과
- 모델: [models_explore로 확인한 실제 id]
- 프롬프트: [계열 크래프트로 조립된 최종 프롬프트]
- 비율: [라이브 aspect_ratios 중 선택]
- 비용: [get_cost가 반환한 credits]
- Job ID / 결과 URL: [job_status completed]
- 서버 조정(adjustments): [있으면 그대로 보고]
```

## 주의사항

- 프롬프트는 계열 크래프트(references/prompt-craft/)의 벤더 공식 컨벤션을 따릅니다.
- 제외 표현은 긍정 장면 묘사로(R1). 리터럴 텍스트는 따옴표+폰트로(R3).
- 모델 id·파라미터를 추측하지 않습니다 — 언제나 `models_explore`로 확인합니다.
- nsfw·초상권·저작권 침해 소지 콘텐츠는 생성하지 않습니다.

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:media-higgsfield-core` | 코어: 호출 계약·라이브 조회·공통 규칙 |
| `moai-media:media-higgsfield-video` | 후속: 이미지를 영상으로 |
| `moai-media:media-gemini-3-image-prompt` | 대안: 프롬프트만 산출 (외부 도구) |
| `moai-media:media-gpt-image-2-prompt` | 대안: 외부 ChatGPT 사용 |
| `moai-marketer:content-card-news` | 후속: 이미지를 카드뉴스에 배치 |

## 출처

- [Higgsfield Skills (공식 agent 문서)](https://github.com/higgsfield-ai/skills)
- [Higgsfield MCP](https://higgsfield.ai/mcp)
- 계열별 프롬프트 크래프트 출처는 각 `references/prompt-craft/*.md`의 Evidence tier·출처 참조.
- 라이브 카탈로그: 런타임 `models_explore` (스냅샷은 plan 단계 증거 기준선일 뿐 런타임 계약 아님).
