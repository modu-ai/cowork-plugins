---
name: media-higgsfield-assets
description: |
  Higgsfield MCP에서 이미지·영상 이외의 생성과 후처리를 다룹니다. 3D 메시(GLB) 생성·리깅·애니메이션,
  오디오(효과음·앰비언스·음악·TTS), 완성 영상의 바이럴 점수 분석, 그리고 업스케일·리프레임·아웃페인팅·
  배경 제거 같은 기존 에셋 후처리가 범위입니다.
  다음과 같은 요청 시 사용하세요:
  - "이 사진을 3D 모델로 만들어줘", "GLB로 뽑아줘", "캐릭터 리깅해줘"
  - "효과음 만들어줘", "배경음악 깔아줘", "이 대본 한국어로 읽어줘"
  - "이 광고 영상 훅이 괜찮은지 점수 내줘", "바이럴 가능성 분석"
  - "이 이미지 4K로 키워줘", "세로 영상으로 리프레임", "배경 지워줘", "캔버스 넓혀줘"
  모델 id·파라미터는 하드코딩하지 않고 models_explore로 라이브 조회합니다. 새 이미지·영상을 처음부터
  만드는 요청은 media-higgsfield-image / media-higgsfield-video를 사용하세요.
version: "1.1.0"
---

# Higgsfield 에셋·후처리 (media-higgsfield-assets)

> `moai-media` | 3D · 오디오 · 영상 분석 · 후처리 (코어: `media-higgsfield-core`)

## 개요

`media-higgsfield-image`와 `media-higgsfield-video`가 "새 이미지·영상 만들기"를 담당한다면, 이 스킬은 **그 바깥의 네 영역**을 담당한다: 3D 에셋, 오디오, 완성 영상 분석, 그리고 이미 있는 에셋의 후처리.

호출 계약·비용 프리플라이트·namespace 해석은 코어를 따른다:
- 호출 계약: `../media-higgsfield-core/references/call-schema.md`
- 라이브 조회: `../media-higgsfield-core/references/catalog-protocol.md`
- 잡·비용·리드백: `../media-higgsfield-core/references/job-lifecycle.md`

## 트리거 키워드

3D, GLB, 메시, 리깅, 스켈레톤, 3D 모델링, 텍스처, PBR, 효과음, SFX, 앰비언스, 배경음악, BGM, 내레이션, TTS, 음성 합성, 보이스, 바이럴 예측, 훅 점수, 영상 분석, 업스케일, 4K, 리프레임, 아웃페인팅, 배경 제거, 누끼

## 네 영역과 진입점

| 영역 | 하는 일 | 상세 |
|---|---|---|
| 3D | 이미지·텍스트 → GLB 메시, 리깅, 애니메이션 | `references/3d.md` |
| 오디오 | 효과음·앰비언스·음악·TTS | `references/audio.md` |
| 분석 | 완성 영상의 주의·훅·리텐션 점수 | `references/analysis.md` |
| 후처리 | 업스케일·리프레임·아웃페인팅·배경 제거·모션 | 아래 §후처리 |

## 워크플로우

코어의 REQ-010 흐름을 그대로 따른다. 영역만 다를 뿐 순서는 같다.

1. **의도 → 영역·후보 좁히기.** 위 표에서 영역을 고르고, 해당 참조 파일로 후보 모델을 좁힌다. 파라미터를 단정하지 않는다.
2. **라이브 조회.** `models_explore(action:'get')`로 실제 제약을 가져온다. 3D·오디오는 모델별 파라미터 편차가 이미지·영상보다 크므로 이 단계를 건너뛰면 거의 실패한다.
3. **비용 프리플라이트.** `get_cost: true`로 `credits` 확인. 3D의 텍스처·리깅·애니메이션은 각각 추가 비용이므로, 옵션을 켠 상태의 비용을 확인한다.
4. **생성.** 조회된 값으로만 호출.
5. **폴링·리드백.** `job_status`로 완료까지. `adjustments`가 있으면 사용자에게 보고한다.

## 후처리 (기존 에셋 변형)

새로 만들지 않고 이미 있는 에셋을 바꾸는 경우다. 각 작업에는 전용 도구가 있으므로, 같은 결과를 생성 모델로 재현하려 하지 않는다 — 전용 도구가 더 싸고 결과가 안정적이다.

| 요청 | 전용 도구 |
|---|---|
| 해상도 키우기 (이미지) | 이미지 업스케일 |
| 해상도 키우기 (영상) | 영상 업스케일 |
| 캔버스 넓히기 / 크롭 해제 | 아웃페인팅 |
| 영상 비율 변경 (가로↔세로) | 리프레임 |
| 배경 제거 / 투명 배경 | 배경 제거 |
| 모션 이식 / 리캐스트 / 퍼펫 | 모션 컨트롤 |

입력은 코어 규칙과 동일하게 `media_id` 또는 이전 잡의 `job_id`로 전달한다. 날것의 URL은 거부된다.

## 출력 형식

```
## Higgsfield 에셋 생성 결과
- 영역: [3D | 오디오 | 분석 | 후처리]
- 모델·도구: [models_explore로 확인한 실제 id]
- 적용 옵션: [텍스처·리깅·애니메이션 / 포맷·샘플레이트 / 등]
- 비용: [get_cost가 반환한 credits]
- Job ID / 결과 URL: [job_status completed]
- 서버 조정(adjustments): [있으면 그대로 보고]
```

## 주의사항

- 3D의 `enable_animation`은 `enable_rigging`을 요구하고, 텍스처 관련 옵션은 `should_texture`를 요구한다. 의존 관계를 어기면 오류다(→ `references/3d.md`).
- 리깅은 인간형(humanoid)에 맞춰져 있다. 동물·사물은 리깅 결과가 나쁠 수 있으며, 그 사실을 미리 알린다.
- 일부 오디오 모델은 라이브 스키마에 **게임 파이프라인 전용**으로 선언돼 있다. 범용 요청에 기본값으로 고르지 않는다(→ `references/audio.md`).
- 영상 분석은 미디어를 만들지 않고 **텍스트 리포트**를 반환한다. 생성 결과물을 기대하게 두지 않는다.
- 모델 id·파라미터를 추측하지 않는다 — 언제나 `models_explore`로 확인한다.
- 타인의 목소리를 동의 없이 복제하지 않는다.

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:media-higgsfield-core` | 코어: 호출 계약·비용·namespace |
| `moai-media:media-higgsfield-image` | 선행: 3D 입력용 이미지 생성 |
| `moai-media:media-higgsfield-video` | 선행: 분석·후처리 대상 영상 생성 |
| `moai-media:media-higgsfield-explainer` | 후속: 오디오·클립을 설명 영상으로 조립 |
| `moai-media:media-audio-gen` | 대안: ElevenLabs 기반 TTS·더빙 |
| `moai-marketer:marketing-performance-report` | 후속: 분석 점수를 성과 리포트에 반영 |

## 출처

- [Higgsfield Skills (공식 agent 문서)](https://github.com/higgsfield-ai/skills) — `higgsfield-generate` v0.12.0 (MIT). 영역 구분과 바이럴 분석 해석 기준의 근거.
- 라이브 MCP 스키마 관측 (`models_explore` type=3d / type=audio) — 모델 목록·파라미터·의존 관계·게임 파이프라인 한정 표기의 근거. **Evidence tier: 1차.**
- 실제 파라미터는 런타임 `models_explore`가 유일한 진실원이다. 참조 파일의 값은 저술 시점 스냅샷이다.
