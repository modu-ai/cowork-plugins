---
name: media-higgsfield-video
description: |
  Higgsfield MCP 기반 AI 영상을 자연어 요청 한 줄로 생성합니다. 모델·파라미터를 하드코딩하지 않고
  라이브 카탈로그(models_explore)를 조회해 호출하므로, 카탈로그가 바뀌어도 드리프트 없이 동작합니다.
  다음과 같은 요청 시 사용하세요:
  - "Higgsfield 영상 만들어줘"
  - "Veo로 영상"
  - "Kling으로 영상"
  - "Seedance로 다이내믹 영상"
  - "Cinema Studio로 시네마틱 영상"
  - "Marketing Studio UGC 광고 영상"
  - "AI 영상 생성"
  Veo·Kling·Seedance·Cinema Studio·Marketing Studio·Wan·Gemini Omni·Grok 등 계열의 프롬프트 크래프트는
  references/prompt-craft/*.md에 출처와 함께 큐레이션돼 있고(계열마다 규칙이 다름 — 범용 공식 없음),
  실제 파라미터(모델 id·해상도·비율·길이·비용)는 런타임에 라이브 조회합니다.
version: "1.2.0"
---

# Higgsfield 영상 생성 (media-higgsfield-video)

> `moai-media` | 라이브 카탈로그 기반 영상 생성 (코어: `media-higgsfield-core`)

## 개요

Higgsfield MCP의 영상 생성 도구를 호출하는 스킬입니다. 사용자 의도로 계열 후보를 좁힌 뒤 **파라미터는 라이브 카탈로그에서 조회**해 생성합니다. 이전 스킬의 하드코딩 모델·프리셋 표는 제거되었습니다 — 그 표들은 라이브 스키마와 어긋나 실패하는 호출을 낳았습니다.

핵심 설계는 코어 스킬 `media-higgsfield-core`에 있습니다: 호출 계약(`call-schema.md`), 라이브 조회(`catalog-protocol.md`), 공통 규칙 R1–R5(`universal-rules.md`), 잡·비용·리드백(`job-lifecycle.md`).

## 계열 크래프트 (references/prompt-craft/) — 계열마다 규칙이 다르다

각 파일은 벤더 공식 문서 기반이며 출처·Evidence tier를 답니다.

| 파일 | 계열 |
|---|---|
| `references/prompt-craft/veo.md` | Veo (오디오 문법 SFX:/Ambient noise:) |
| `references/prompt-craft/kling.md` | Kling (유연 프레임워크, 1차-relayed) |
| `references/prompt-craft/seedance.md` | Seedance (타임스탬프 unstable — 라벨 샷 리스트) |
| `references/prompt-craft/cinema-studio.md` | Cinema Studio (4계층 참조, enum 라이브 조회) |
| `references/prompt-craft/marketing-studio.md` | Marketing Studio (hook/setting↔ad_reference 상호배타) |
| `references/prompt-craft/wan.md` | Wan (Timestamp 멀티샷 — Seedance와 정반대) |
| `references/prompt-craft/gemini-omni.md` | Gemini Omni (편집은 단순 프롬프트) |
| `references/prompt-craft/grok.md` | Grok (오디오 문서 부재 — 지어내지 않음) |

카메라 디렉팅·Marketing Studio 슬러그 참고: `references/dop-motions.md`.

## 범용 비디오 공식은 없다 — per-family 라우팅

**단일 범용 비디오 프롬프트 공식을 쓰지 않는다.** 벤더마다 컨벤션이 정반대이기 때문이다: Wan은 멀티샷에 명시적 Timestamp를 처방하지만 ByteDance는 Timestamp가 Seedance를 불안정하게 만든다고 경고한다. 이 둘을 하나로 통합하는 것은 correctness 회귀다. 따라서 스킬은 대상 계열의 `prompt-craft/` 파일로 **per-family(계열별)** 라우팅하여 그 계열의 벤더 공식 컨벤션을 적용한다.

## 워크플로우 (REQ-010 흐름)

### 1단계 — 의도 파악 → 후보 좁히기

사용자 요청에서 subject·action·scene·camera·audio·references(+각 용도)·shot count·duration 등 슬롯을 수집(→ core `interview-schema.md`)하고 계열 후보를 좁힙니다. 후보를 좁힐 뿐 파라미터를 단정하지 않습니다. 슬롯이 부족하면 blocker 보고를 반환하고 오케스트레이터가 확인합니다(스킬은 사용자에게 직접 질문하지 않음).

| 사용자 표현 | 후보 계열 |
|---|---|
| "사실적", "오디오 있는 영상" | Veo |
| "인물·표정·스토리보드" | Kling |
| "다이내믹 모션·멀티샷" | Seedance 또는 Wan |
| "영화 룩·모션 전이" | Cinema Studio |
| "UGC·DTC 광고 영상" | Marketing Studio |
| "이미지 편집·간단 참조" | Gemini Omni |
| "Grok 영상" | Grok |

### 2단계 — 라이브 조회 (models_explore)

`models_explore(action:'get')`로 좁힌 후보의 실제 제약(aspect_ratios·durations·media role·모델별 param)을 조회합니다. 범위 밖 모델이면 계열 크래프트가 없다는 것을 명시하고 **live lookup**으로 제약만 가져와 R1–R5를 적용합니다. Marketing Studio 계열이면 `show_marketing_studio`로 preset/hook/setting을 조회합니다.

### 3단계 — 비용 프리플라이트 (get_cost)

같은 파라미터에 `get_cost: true`를 넣어 `credits`를 확인합니다(크레딧 0). `adjustments`가 있으면 서버가 채운 기본값이므로 리드백해 둡니다(예: 오디오를 요청했는데 `generate_audio: false`로 치환됐다면 보고). 잔액 정지 규칙은 core `job-lifecycle.md`.

### 4단계 — 승인 게이트 (크레딧 소진 전)

`get_cost`는 비용을 **조회**할 뿐 승인을 받지 않습니다. 크레딧이 실제로 나가기 전 마지막 정지선이며, 코어 §유료 생성 승인 게이트를 그대로 따릅니다 — 프롬프트 전문·모델 id·입력 미디어·확정 옵션·길이·생성 개수·`adjustments`·견적 크레딧·잔액을 보여주고 승인을 받습니다.

- **[HARD] 3단계에서 확보한 `adjustments`를 여기서 보여줍니다.** 3단계의 예(오디오를 요청했는데 `generate_audio: false`로 치환)가 바로 이 게이트가 필요한 이유입니다 — 오디오 없는 영상에 영상 값 크레딧을 낸 뒤에 알게 되면 늦습니다.
- 위 §위험 블록에 해당하는 모델(`gemini_omni` video-references·`minimax_hailuo` 카메라 명령)이면 **그 경고를 승인 화면에 함께 띄웁니다.** 알려진 위험을 아는 채로 돈을 쓸지 사용자가 고르게 합니다.
- 이 스킬은 사용자에게 직접 묻지 않으므로, 게이트에 도달하면 blocker로 반환하고 오케스트레이터가 `AskUserQuestion`으로 묻습니다.

### 5단계 — 생성 (generate_video)

승인된 값으로만 실제 `generate_video`를 호출합니다. namespace는 런타임 해석. 참조 미디어는 `media_id`/`job_id`로만 전달합니다.

- **[HARD] 실패해도 새 잡을 만들지 않습니다.** 애매하게 실패하면 반환된 job ID를 `job_status`로 먼저 확인하고, ID조차 없으면 **생성 이력 조회 도구가 실제로 노출돼 있는지 먼저 확인합니다** — 코어 계약에 있는 것은 `job_status`·`job_display`뿐입니다. 없으면 사용자에게 Higgsfield 대시보드 확인을 요청합니다. 없다는 것이 확인된 뒤에만 다시 호출합니다. 영상은 이미지보다 단가가 높아 중복 비용이 큽니다.

### 6단계 — 폴링·리드백

`job_status`로 `completed`까지 폴링하고, 결과 URL과 함께 반환된 `adjustments`를 사용자에게 보고합니다.

## 위험 블록 (반드시 경고)

이 세 가지는 계열 크래프트가 벤더 근거로 확인한 위험이다. 스킬은 해당 모델 사용 시 사용자에게 경고한다:

- **`gemini_omni` video-references는 known-broken** — Google 자신의 말: *"...are not correctly processed by the model at this time."* API가 받아들여도 모델이 제대로 처리하지 못한다(→ `prompt-craft/gemini-omni.md`).
- **`minimax_hailuo`는 카메라 명령을 조용히 덮어쓸 수 있다** — MiniMax 자체 API의 `prompt_optimizer`(기본 true)가 프롬프트를 자동 재작성해 정밀한 수동 카메라 명령을 뭉갤 수 있다. **Higgsfield는 이 스위치를 노출하지 않으므로** MCP로는 끌 수 없다. 정밀 카메라 디렉팅이 무시될 수 있음을 경고한다.
- **Grok은 오디오 컨벤션이 문서화돼 있지 않다** — 카탈로그가 "native audio"로 태깅해도 xAI 공식 문서엔 오디오 언급이 없다. Grok 오디오 문법을 지어내지 않는다(→ `prompt-craft/grok.md`).

## 범위 밖 모델 폴백 (live lookup)

계열 크래프트에 없는 모델을 요청하면, 계열 특화 크래프트가 없다는 사실을 명시하고 `models_explore`로 제약을 **live lookup**한 뒤 공통 규칙 R1–R5를 적용합니다.

## 출력 형식

```
## Higgsfield 영상 생성 결과
- 모델: [models_explore로 확인한 실제 id]
- 프롬프트: [계열 크래프트로 조립된 최종 프롬프트]
- 비율·길이: [라이브 aspect_ratios·durations 중 선택]
- 비용: [get_cost가 반환한 credits]
- Job ID / 결과 URL: [job_status completed]
- 서버 조정(adjustments): [있으면 그대로 보고]
```

## 주의사항

- 프롬프트는 대상 계열의 `prompt-craft/` 벤더 공식 컨벤션을 따릅니다 — 범용 공식을 쓰지 않습니다.
- image-to-video는 시작 이미지가 담은 정적 정보를 빼고 motion + camera로 시작합니다(R2). 시작 이미지는 `media-higgsfield-image`로 먼저 생성할 수 있습니다.
- 모델 id·파라미터를 추측하지 않습니다 — 언제나 `models_explore`로 확인합니다.
- nsfw·초상권·저작권 침해 소지 콘텐츠는 생성하지 않습니다.

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:media-higgsfield-core` | 코어: 호출 계약·라이브 조회·공통 규칙 |
| `moai-media:media-higgsfield-image` | 선행: 시작 이미지 생성 |
| `moai-media:media-audio-gen` | 보조: 영상용 음성·BGM |

## 출처

- [Higgsfield Skills (공식 agent 문서)](https://github.com/higgsfield-ai/skills)
- [Higgsfield MCP](https://higgsfield.ai/mcp)
- 계열별 프롬프트 크래프트 출처는 각 `references/prompt-craft/*.md`의 Evidence tier·출처 참조.
- 라이브 카탈로그: 런타임 `models_explore` (스냅샷은 plan 단계 증거 기준선일 뿐 런타임 계약 아님).
