# soul-vs-elements.md — 경로 판정 규칙 (SSOT)

> `media-higgsfield-identity` | Soul Character와 Reference Element 중 무엇을 쓸지 가르는 규칙.
> 모델 목록과 제약은 저술 시점의 라이브 스키마 관측이며, 실제 호출 직전에는 코어의 `catalog-protocol.md`에 따라 재확인한다.

**Evidence tier:** 1차 (라이브 MCP tool schema 관측 — `show_characters` / `show_reference_elements`)

---

## 1. 두 경로의 본질적 차이

Soul은 **한 사람의 얼굴을 전용 모델로 학습**한다. 그래서 identity 충실도가 높지만, 학습된 것이 "그 한 사람"이므로 한 장면에 하나만 놓을 수 있고, 그 학습 결과를 이해하는 모델도 soul 계열로 한정된다.

Element는 **참조 이미지를 프롬프트에 주입**한다. 학습이 없으므로 즉시 만들어지고, 주입 슬롯을 여러 개 둘 수 있으며, 사람이 아닌 대상(제품·배경·소품)도 담을 수 있다. 대신 identity 충실도는 전용 학습보다 낮다.

이 차이가 아래 모든 규칙의 원인이다.

---

## 2. 판정 규칙 (우선순위 순)

위에서부터 평가하고, 처음 걸리는 항목에서 멈춘다.

| # | 조건 | 판정 | 이유 |
|---|---|---|---|
| 1 | 한 컷에 인물·대상이 2개 이상 | **Element** | Soul은 한 생성에 `soul_id` 1개만 허용 — 구조적으로 불가능 |
| 2 | 대상이 사람이 아님 (제품·배경·소품·로고) | **Element** | Soul은 얼굴 학습 모델 |
| 3 | 사용자가 soul 계열이 아닌 모델을 지목 | **Element** | Soul은 `soul_2`·`soul_cinematic` 전용 |
| 4 | 보유 이미지가 1장 | **Element** | Soul 학습 최소 5장 |
| 5 | 즉시 결과를 요구 | **Element** | Soul 학습 약 10분 |
| 6 | "학습"·"훈련"·"디지털 트윈"·"identity" 명시 | **Soul** | 사용자가 학습 경로를 선택함 |
| 7 | 같은 사람 사진 5장 이상 + 단독 컷 목적 | **Soul** | 학습 요건 충족 + Soul 제약에 걸리지 않음 |
| 8 | 그 외 전부 | **blocker** | 판정 근거 부족 — 오케스트레이터가 사용자에게 확인 |

8번이 이 파일의 핵심이다. 애매한 요청을 Soul로 흘려보내면 사용자는 10분과 크레딧을 쓰고 나서야 "2인 컷은 안 된다"를 알게 된다.

---

## 3. Soul 제약

| 제약 | 값 |
|---|---|
| 학습 이미지 수 | 5~20장 (권장 8~12) |
| 학습 시간 | 약 10분, 비차단 |
| 한 생성당 개수 | **1개** |
| 사용 가능 모델 | `soul_2` (Soul V2), `soul_cinematic` (Soul Cinema) |
| 타입 파라미터 | `soul_2` / `soul_cinematic` / `soul`(레거시) |
| 계정 요건 | 유료 플랜(Basic 이상) |
| 이미지 입력 형태 | `media_id` UUID · 완료된 이미지 잡 ID · https URL. **로컬 경로 불가** |

`soul_2`와 `soul_cinematic` 모두 `params.soul_id`를 선택적 파라미터로 선언한다. 즉 soul_id 없이도 그 모델은 동작하며, soul_id를 넣었을 때만 학습된 identity가 반영된다.

---

## 4. Element 제약과 지원 모델

| 제약 | 값 |
|---|---|
| 생성 방식 | 동기 (즉시 반환) |
| 입력 | `medias[]` — `{id, url, type}`, `type`은 `media_input` 또는 `image_job` |
| 카테고리 | `auto`(기본, 서버 분류) · `character` · `environment` · `prop` |
| 이름 | 32자 이내, 생략 시 서버 자동 부여 (워크스페이스 내 유일) |
| 한 프롬프트당 개수 | 제한 없음 (다중 배치 가능) |
| URL 요건 | https만. 사설/루프백 호스트는 거부 |

**사용법:** `generate_image` / `generate_video`의 `params.prompt` 안에 `<<<element_id>>>`를 넣는다. 백엔드가 해당 이미지를 주입하고 프롬프트를 `@element_name` 형태로 재작성한다.

**지원 모델 (저술 시점 관측):**

| 종류 | 모델 |
|---|---|
| 이미지 | `nano_banana_2`(Nano Banana Pro), `nano_banana_flash`(Nano Banana 2), `gpt_image_2`, `seedream_v4_5`, `seedream_v5_lite`, `cinematic_studio_2_5` |
| 영상 | Cinema Studio Video 2 / 3.0, `seedance_2_0`, `kling3_0` |

**Soul 전용 모델(`soul_2`·`soul_cinematic`)에는 Element가 적용되지 않는다.** 두 목록은 교집합이 없다 — 이것이 경로를 처음에 갈라야 하는 실질적 이유다.

---

## 5. 안티패턴

- **애매한 채로 학습 제출** — 판정 규칙 8번을 무시하고 Soul을 시작하는 것. 되돌릴 수 없다.
- **2인 컷을 Soul 두 번 호출로 우회** — 한 생성에 soul_id는 1개다. 두 번 호출해도 한 이미지에 두 사람이 들어가지 않는다.
- **Soul을 Nano Banana·Seedream에 전달** — 무시되거나 오류. 그 모델들은 Element 경로다.
- **로컬 파일 경로를 `medias`에 직접 전달** — 거부된다. 업로드 3단계(`media_upload` → 바이트 PUT → `media_confirm`)를 먼저 거친다.
- **`<<<id>>>` 문법을 사용자에게 노출** — 내부 메커니즘이다. 결과 보고에는 넣지 않는다.
