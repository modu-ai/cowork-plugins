---
name: media-higgsfield-identity
description: |
  Higgsfield MCP에서 재사용 가능한 인물·사물 일관성 참조를 만듭니다. Soul Character(학습형 identity 모델)와
  Reference Element(즉시 생성형 참조) 중 어느 쪽을 써야 하는지 판정하고, 선택된 경로로 생성·조회합니다.
  다음과 같은 요청 시 사용하세요:
  - "내 얼굴로 Soul 만들어줘", "디지털 트윈 학습시켜줘"
  - "이 캐릭터 계속 똑같이 나오게 해줘"
  - "나랑 친구 둘 다 나오는 이미지"
  - "이 제품을 여러 컷에 일관되게 넣어줘"
  - "학습해둔 캐릭터 목록 보여줘"
  Soul은 한 사람의 identity에 충실하지만 한 생성에 1개만·soul 계열 모델 전용이고, Element는 즉시 만들어지며
  한 프롬프트에 여러 개를 배치할 수 있고 사람이 아닌 대상도 됩니다. 이 분기를 잘못 고르면 되돌릴 수 없는
  학습 비용이 발생하므로, 경로가 불명확하면 생성하지 않고 blocker를 반환합니다.
version: "1.0.0"
---

# Higgsfield 일관성 참조 (media-higgsfield-identity)

> `moai-media` | Soul Character · Reference Element 판정과 생성 (코어: `media-higgsfield-core`)

## 개요

"같은 인물·같은 캐릭터·같은 제품이 여러 컷에 일관되게 나오게" 하는 두 가지 수단을 다룬다. 두 수단은 **대체재가 아니라 서로 다른 제약을 가진 별개 경로**이며, 잘못 고르면 학습 시간과 크레딧을 버린다.

호출 계약·namespace 런타임 해석·비용 프리플라이트는 코어를 따른다:
- 호출 계약: `../media-higgsfield-core/references/call-schema.md`
- 라이브 조회: `../media-higgsfield-core/references/catalog-protocol.md`
- 잡·비용·리드백: `../media-higgsfield-core/references/job-lifecycle.md`

## 트리거 키워드

Soul, Soul ID, 소울, 디지털 트윈, 캐릭터 학습, 얼굴 학습, identity, 캐릭터 일관성, Element, 레퍼런스 엘리먼트, 참조 요소, 재사용 캐릭터, 같은 인물, 같은 제품

## 두 경로 비교 (판정의 근거)

| 축 | Soul Character | Reference Element |
|---|---|---|
| 만드는 방법 | 5~20장 학습 (약 10분, 비차단) | 이미지 1장으로 즉시 생성 (동기) |
| 한 생성에 몇 개 | **1개만** | **여러 개** (`<<<id>>>` 다중 배치) |
| 대상 | 사람 1인 | 사람·환경·소품 모두 |
| 사용 가능 모델 | `soul_2`, `soul_cinematic` **전용** | Nano Banana 계열·GPT Image 2·Seedream·Cinema Studio·Seedance·Kling 등 |
| identity 충실도 | 높음 (전용 학습) | 보통 (참조 주입) |
| 되돌리기 | 학습 비용 발생 후 | 비용 거의 없음 |

상세 판정 규칙과 지원 모델 전체 목록은 `references/soul-vs-elements.md`.

## 판정 워크플로우

### 1단계 — 경로 판정 (생성보다 먼저)

아래 신호로 경로를 가른다. **어느 쪽도 확실하지 않으면 생성하지 않고 blocker를 반환**한다 — 오케스트레이터가 사용자에게 확인한다. 이 스킬은 사용자에게 직접 질문하지 않는다.

**Element로 확정되는 신호 (하나라도 걸리면 Element):**
- 한 컷에 인물/대상이 **2명 이상** ("나랑 친구", "두 사람이")
- 대상이 사람이 아님 (제품·소품·배경·로고)
- 가진 이미지가 **1장뿐**
- Nano Banana·Seedream·Kling·Cinema Studio 등 **soul 계열이 아닌 모델**을 지목
- "지금 바로", "빨리" 등 즉시성 요구

**Soul로 확정되는 신호:**
- "학습", "훈련", "디지털 트윈", "내 identity" 등 명시적 표현
- 같은 사람 사진 **5장 이상**을 제공했고 단독 컷이 목적

**양쪽 다 아니면 → blocker.** 애매한 상태로 Soul 학습을 시작하는 것이 이 스킬이 막으려는 실패다.

### 2단계-A — Soul 경로

1. **이미지 준비.** 로컬 경로는 받지 않는다. `media_upload` → 바이트 PUT → `media_confirm` 순서로 올려 `media_id` UUID를 얻는다. 완료된 이미지 잡 ID나 https URL도 허용된다.
2. **품질 점검.** 5~20장, 권장 8~12장. 각도·조명·표정·거리가 다양할수록 좋다. 상세 기준은 `references/training-photo-guide.md`. 기준 미달이면 학습을 제출하기 전에 사용자에게 알린다.
3. **타입 선택.** 다운스트림 용도로 정한다 — 정지 이미지는 `soul_2`, 시네마틱은 `soul_cinematic`.
4. **학습 제출.** `show_characters(action:'train', name, medias[])`. 비차단이며 약 10분 소요.
5. **상태 확인.** `show_characters(action:'status', soul_id)`. 폴링은 조용히 — 진행 상황을 반복 보고하지 않는다.
6. **인계.** 준비되면 `soul_id`를 `generate_image`의 `params.soul_id`로 넘긴다. 모델은 `soul_2` 또는 `soul_cinematic`.

기존 Soul을 찾을 때는 `show_characters(action:'list', status:'ready')`.

### 2단계-B — Element 경로

1. **이미지 준비.** Soul과 동일한 업로드 절차. `medias[]` 항목은 `{id, url, type}` 형태이며 `type`은 `media_input`(업로드) 또는 `image_job`(이전 생성).
2. **생성.** `show_reference_elements(action:'create', medias[])`. `category`는 기본 `auto`(서버 분류)로 두고, 사용자가 명시할 때만 `character`/`environment`/`prop`을 지정한다. `name`은 32자 이내이며 생략하면 서버가 자동 부여한다. 동기 반환이다.
3. **사용.** 반환된 element id를 `generate_image`/`generate_video`의 `params.prompt` 안에 `<<<element_id>>>` 형태로 끼워 넣는다. 한 프롬프트에 여러 개를 넣을 수 있다.
4. **조회.** `show_reference_elements(action:'list')` 또는 `action:'get'`.

> Element 사용 시 프롬프트에 들어가는 `<<<id>>>` 표기는 내부 메커니즘이다. 결과 보고에서 사용자에게 이 문법을 설명하지 않는다 — 사용자에게는 "그 캐릭터를 넣었다"로 충분하다.

## 비용·계정 전제

- Soul 학습은 **유료 플랜(Basic 이상)**을 요구한다. 무료 플랜이면 제출 전에 알린다.
- 학습 자체와 이후 생성은 별개 비용이다. 실제 생성 직전 `get_cost: true` 프리플라이트는 코어 규칙을 그대로 따른다.
- Element 생성은 학습이 없어 비용 부담이 작다.

## 출력 형식

```
## Higgsfield 일관성 참조 결과
- 선택 경로: [Soul | Element] — 판정 근거: [걸린 신호]
- 이름: [name]
- 참조 ID: [soul_id | element_id]
- 상태: [ready | training | 생성 완료]
- 사용 가능 모델: [경로별 제약]
- 다음 단계: [generate_image에 어떻게 넘기는지]
```

## 주의사항

- 경로가 애매하면 **생성하지 않는다.** Soul 학습은 시간과 크레딧을 쓰고 되돌릴 수 없다.
- 로컬 파일 경로를 `medias`에 그대로 넣지 않는다 — 반드시 업로드해 `media_id`를 얻는다(코어 `call-schema.md` §2와 동일 규칙).
- 한 생성에 `soul_id`는 1개다. 2인 이상 등장 요구를 Soul로 우회하려 하지 않는다.
- Soul을 soul 계열이 아닌 모델에 넘기지 않는다 — 무시되거나 오류가 된다.
- 학습 실패의 흔한 원인(사진 부족·단조로움·선글라스/모자 가림·단체 사진)은 `references/training-photo-guide.md`.
- 타인의 얼굴을 동의 없이 학습시키지 않는다. 초상권 확인은 사용자 책임이며, 요청이 제3자 인물로 보이면 그 사실을 짚는다.

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:media-higgsfield-core` | 코어: 호출 계약·비용·namespace |
| `moai-media:media-higgsfield-image` | 후속: 참조를 써서 이미지 생성 |
| `moai-media:media-higgsfield-video` | 후속: 참조를 써서 영상 생성 |
| `moai-story:story-character-sheet` | 선행: 무엇을 학습시킬지(각도·앵커) 설계 |
| `moai-designer:design-brand-visual` | 후속: 브랜드 모델·마스코트 일관성 |

## 출처

- [Higgsfield Skills (공식 agent 문서)](https://github.com/higgsfield-ai/skills) — `higgsfield-soul-id` 스킬 v0.12.0 (MIT). 학습 사진 기준·실패 원인은 이 문서 기반.
- 라이브 MCP 도구 스키마 관측 (`show_characters` / `show_reference_elements`) — Soul/Element 분기 규칙·지원 모델 목록·업로드 제약의 근거. **Evidence tier: 1차.**
- 공식 CLI 스킬에는 Element 경로와 분기 규칙이 없다. 그 부분은 MCP 스키마 관측이 유일 출처다.
