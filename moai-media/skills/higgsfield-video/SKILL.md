---
name: higgsfield-video
description: |
  Higgsfield MCP 기반 AI 영상을 자연어 요청 한 줄로 생성합니다.
  다음과 같은 요청 시 사용하세요:
  - "Higgsfield 영상 만들어줘"
  - "Veo 3로 영상"
  - "Sora 2로 영상 만들어"
  - "Kling 3.0으로 영상"
  - "Seedance Pro로 영상 생성"
  - "Cinema Studio 3.5로 시네마틱 영상"
  - "UGC 광고 영상 만들어줘"
  - "캐릭터 일관성 있는 아바타 영상"
  Seedance 2.0·Seedance Pro·Cinema Studio 3.5·Kling 2.1 Master·Kling 2.5 Turbo·Kling 3.0·Kling Avatars 2.0·MiniMax Hailuo 02·Google Veo 3·Sora 2·Wan 2.5 11개 공식 영상 모델과 6가지 비디오 프리셋(UGC·Unboxing·Product review·Hyper motion·TV spot·Wild Card), 캐릭터 일관성(Kling Avatars 2.0), 비동기 잡 폴링까지 처리한 완성 영상을 산출합니다.
  실제 영상 생성 요청 시 Higgsfield MCP가 연결돼 있으면 이 스킬을 사용하세요.
user-invocable: true
version: 2.27.0
---

# Higgsfield 영상 생성 (higgsfield-video)

## 개요

Higgsfield MCP의 영상 생성 도구를 호출하는 스킬입니다. 공식 11개 영상 모델 중 사용자 의도에 가장 적합한 것을 선택하고, 비디오 프리셋·캐릭터 일관성·비동기 잡 폴링까지 통합 처리합니다.

## 트리거 키워드

Higgsfield 영상, Sora 2, Google Veo 3, Kling 2.1 Master, Kling 2.5 Turbo, Kling 3.0, Kling Avatars 2.0, Seedance 2.0, Seedance Pro, Cinema Studio 3.5, MiniMax Hailuo 02, Wan 2.5, UGC 영상, Unboxing 영상, Product review, AI 영상 생성, 광고 영상

## 전제 — MCP 등록

`moai-media` 플러그인 설치 시 `.mcp.json`이 Higgsfield MCP를 자동 등록합니다 (이미지 스킬과 공유). 첫 호출 직전 Cowork에서 OAuth 인증 1회.

## 공식 11개 영상 모델 — 한눈에

[higgsfield.ai 공식 페이지](https://higgsfield.ai) 명시 기준 (2026-05).

### 일반 영상 (text-to-video / image-to-video)

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Sora 2** ★ | 사실적·자연스러운 동작 | 일반 광고·내러티브 |
| **Google Veo 3** | 고품질·다양한 톤 | 마케팅·브랜드 영상 |
| **Kling 2.1 Master** | 인물·캐릭터 모션 (1세대 Master) | 인물 중심 |
| **Kling 2.5 Turbo** | 빠른 처리·중간 품질 | 빠른 시안·반복 |
| **Kling 3.0** ★ | Kling 최신·고품질 | 인물·표정 강조 |
| **Seedance 2.0** | 다이내믹 모션 | 댄스·액션·생동감 |
| **Seedance Pro** ★ | Seedance 고품질 변형 | 광고·고품질 모션 |
| **MiniMax Hailuo 02** | 카메라 무브먼트 정교 | 트래킹·줌·팬 |
| **Wan 2.5** | 다양한 톤·중국 최신 | 실험적·신규 톤 |

### 시네마틱 영화 룩

| 모델 | 강점 |
|---|---|
| **Cinema Studio 3.5** ★ | 영화 그레이딩·필름 룩·카메라 디렉팅 |

### 인물·캐릭터 일관성

| 모델 | 강점 |
|---|---|
| **Kling Avatars 2.0** | 캐릭터 일관성 영상·아바타 시리즈 |

## 6가지 비디오 프리셋

[higgsfield.ai/skills](https://higgsfield.ai/skills) 공식 비디오 프리셋:

| 프리셋 | 용도 |
|---|---|
| **UGC** | 일반 사용자 콘텐츠 톤 (자연스러움) |
| **Unboxing** | 언박싱·제품 개봉 |
| **Product review** | 제품 리뷰 (특징 강조) |
| **Hyper motion** | 빠른 모션·다이내믹 |
| **TV spot** | 광고 TV 톤 (시네마틱) |
| **Wild Card** | 실험적·창의적 자유 톤 |

프리셋을 지정하면 적절한 모델이 자동 선택되고 시네마틱 설정이 적용됩니다.

## 워크플로우

### 1단계 — 의도·길이·용도 파악

| 항목 | 자동 추론 |
|---|---|
| **길이** | "짧게"·"5초" → Kling 2.5 Turbo·Seedance / "광고"·"8-10초" → Veo 3·Sora 2 |
| **용도** | 광고 · SNS · 내러티브 · 시연·튜토리얼 · 인물 발화 |
| **입력** | text-to-video · image-to-video · 캐릭터 시리즈 |
| **프리셋** | UGC·Unboxing·Product review·Hyper motion·TV spot·Wild Card |

부족하면 AskUserQuestion 1라운드.

### 2단계 — 모델·프리셋 자동 선택

| 사용자 표현 | 자동 |
|---|---|
| "사실적", "자연스러운", "일반 광고" | Sora 2 또는 Google Veo 3 |
| "고품질 브랜드 영상" | Google Veo 3 |
| "인물 표정·연기 중요" | Kling 3.0 또는 Kling 2.1 Master |
| "빠르게 여러 시안" | Kling 2.5 Turbo (Turbo 처리) |
| "다이내믹 모션·댄스" | Seedance 2.0 또는 Seedance Pro |
| "광고 고품질" | Seedance Pro · Cinema Studio 3.5 · Google Veo 3 |
| "카메라 무브먼트 정교" | MiniMax Hailuo 02 |
| "영화 룩·필름 그레이딩" | Cinema Studio 3.5 |
| "캐릭터 시리즈·아바타" | Kling Avatars 2.0 |
| "실험적·새로운 톤" | Wan 2.5 |
| "언박싱·리뷰" | Product review·Unboxing 프리셋 |
| "UGC 톤 자연스럽게" | UGC 프리셋 |
| "광고 TV 스팟" | TV spot 프리셋 + Cinema Studio 3.5 |
| "역동적·빠른 변화" | Hyper motion 프리셋 |

### 3단계 — 입력 준비

#### Text-to-video
프롬프트만 필요.

#### Image-to-video
시작 이미지 필요. 시작 프레임이 결과 톤을 좌우합니다.

```
[권장] higgsfield-image (Soul 2.0·Soul Cinema·Flux Kontext)로 시작 이미지 → image-to-video
```

#### 캐릭터 시리즈
- Kling Avatars 2.0 사용
- 사전에 인물 reference 등록

### 4단계 — 파라미터 설계

#### 공통 파라미터

| 파라미터 | 값 |
|---|---|
| `prompt` | 행동·분위기·디테일 묘사 |
| `model` | 모델 식별자 (예: `sora_2`, `veo_3`, `kling_3_0`, `seedance_pro`) |
| `preset` | UGC · Unboxing · Product review · Hyper motion · TV spot · Wild Card |
| `quality` | `turbo` (빠름·저렴) · `standard` · `high` |
| `aspect_ratio` | `16:9` · `9:16` (릴스·숏폼) · `1:1` · `4:5` |
| `duration_seconds` | 모델별 다름 (5-15초) |
| `seed` | 재현용 |

#### Image-to-video 추가

| 파라미터 | 값 |
|---|---|
| `image_url` 또는 `input_images[]` | 시작 이미지 URL |

### 5단계 — MCP 호출

```
ToolSearch(query: "select:mcp__higgsfield__generate_video")

mcp__higgsfield__generate_video({
  model: "veo_3",
  prompt: "[행동·분위기 묘사]",
  aspect_ratio: "16:9",
  duration_seconds: 8,
  quality: "standard",
  preset: "TV spot",   // 옵션
  image_url: "..."     // image-to-video 시
})
```

모델 식별자는 공식 페이지에서 underscore_separated 형식 (예: `sora_2`, `veo_3`, `kling_3_0`, `kling_2_5_turbo`, `seedance_pro`, `cinema_studio_3_5`).

### 6단계 — 비동기 잡 폴링

영상은 이미지보다 오래 걸립니다.

| 상태 | 평균 시간 |
|---|---|
| `queued` | 잔액 정상 시 즉시 |
| `in_progress` | Sora 2/Veo: 20-60초 · Kling Turbo: 10-25초 · Cinema Studio·Seedance Pro: 30-90초 |
| `completed` | 영상 URL 수령 |
| `failed` | 프롬프트·모델 호환성 문제 |
| `nsfw` | 콘텐츠 필터링 |

긴 영상(15초)은 1-2분도 정상.

### 7단계 — 결과 검수·반복

| 사용자 반응 | 후속 행동 |
|---|---|
| "좋다" | 다운로드·SNS 업로드 |
| "동작 부자연" | Kling 3.0 또는 Veo 3로 모델 변경 |
| "톤이 약하다" | Cinema Studio 3.5 + TV spot 프리셋 |
| "더 빠르게 / 짧게" | duration 단축 + Kling 2.5 Turbo 또는 Seedance |
| "음성 추가" | `audio-gen` (ElevenLabs) → 외부 편집 |

## 사용 예시

### 예시 1 — 8초 광고 영상 (시네마틱)

```
요청: "신제품 가죽 지갑 광고 영상, 시네마틱 톤, 8초"

플로우:
1. higgsfield-image (Soul Cinema)로 시작 이미지 1장
2. higgsfield-video
   - model: cinema_studio_3_5 또는 veo_3
   - preset: TV spot
   - image_url: 1번 결과
   - duration: 8s
   - aspect_ratio: 16:9
   - quality: high
3. 60초 대기 → 8초 영상
```

### 예시 2 — 릴스용 숏폼 (UGC)

```
요청: "5초 인스타 릴스 영상, 자연스럽게"

자동: model: kling_2_5_turbo (빠름·저비용)
preset: UGC
aspect_ratio: 9:16
duration: 5s
quality: turbo
```

### 예시 3 — 캐릭터 시리즈 영상

```
요청: "브랜드 마스코트가 점프하는 5초 영상"

자동: model: kling_avatars_2_0
입력: 마스코트 이미지 reference
duration: 5s
```

### 예시 4 — 제품 언박싱 영상

```
요청: "신제품 언박싱 영상 10초"

자동: model: seedance_pro (제품 광고 적합)
preset: Unboxing
duration: 10s
```

### 예시 5 — 다이내믹 댄스 영상

```
요청: "댄스 영상 짧게, 빠른 모션"

자동: model: seedance_pro
preset: Hyper motion
duration: 5s
quality: standard
```

### 예시 6 — 카메라 트래킹 영상

```
요청: "제품을 회전하면서 보여주는 영상"

자동: model: minimax_hailuo_02 (카메라 무브먼트 정교)
duration: 6s
```

## 출력 형식

```
## Higgsfield 영상 생성 결과

### 호출 정보
- 모델: [예: veo_3]
- 프리셋: [TV spot 등 또는 없음]
- 입력: text-to-video / image-to-video
- 길이·비율·품질: [duration · aspect_ratio · quality]
- Job ID: [Higgsfield job ID]
- 소요 시간: [실제]

### 결과
- 영상 URL: [Higgsfield CDN]
- 다운로드 경로: [로컬]
- 썸네일: [첫 프레임]

### 검수
- 모션 자연스러움·의도 부합·길이·비율: [점수]

### 후속 추천
- 음성 추가 → audio-gen
- 편집·자막 → 외부 도구
- 시리즈 영상 → 같은 모델·다른 입력
```

## 비용 관리

| 모델 | 상대 비용 |
|---|---|
| Kling 2.5 Turbo | 가장 저렴·빠름 |
| Seedance 2.0 / Wan 2.5 | 저렴 |
| Kling 2.1 Master / MiniMax Hailuo 02 | 중간 |
| Google Veo 3 | 중간-비쌈 |
| Sora 2 | 비쌈 |
| Kling 3.0 | 비쌈 |
| Seedance Pro / Cinema Studio 3.5 | 비쌈 |
| Kling Avatars 2.0 | 비쌈 (특수) |

워크스페이스 잔액: `higgsfield.ai → Billing`.

## 주의사항

### Do

- 첫 시도는 **Kling 2.5 Turbo**로 빠른 시안 확보 → Veo 3·Sora 2로 본 생성
- Image-to-video는 시작 이미지 품질이 결과를 좌우 → `higgsfield-image` 우선
- 광고용은 TV spot 프리셋 + 16:9
- 릴스·숏폼은 9:16 + UGC 또는 Hyper motion 프리셋
- 캐릭터 시리즈는 Kling Avatars 2.0 사용

### Don't

- 한 영상에 너무 복잡한 동작 요청
- 10초 이상 영상에서 급격한 변화
- nsfw·민감 콘텐츠
- 초상권 침해 가능한 영상
- 저작권 있는 캐릭터·로고

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| "Not connected" | OAuth 미인증 | Cowork → 설정 → MCP → Higgsfield → Connect |
| `queued` 멈춤 | 잔액 부족 | higgsfield.ai/billing 충전 |
| `failed` (image-to-video) | 시작 이미지 URL 오류 | higgsfield-image로 새 이미지 생성 후 재시도 |
| 결과 부자연 | 모델 부적합 | Sora 2 ↔ Veo 3 ↔ Kling 3.0 교체 |
| 영상이 너무 짧음 | duration 미지정 | duration_seconds 명시 |
| 비용 예상보다 큼 | 비싼 모델 사용 | Kling 2.5 Turbo로 우선 탐색 |
| 프리셋 효과 안 보임 | model과 호환 안 됨 | 프리셋만 단독 사용 또는 권장 모델 |

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:higgsfield-image` | 선행: 시작 이미지·캐릭터 reference 생성 |
| `moai-media:audio-gen` | 보조: 영상에 추가할 음성·BGM 생성 |
| `moai-content:landing-page` | 후속: 영상을 랜딩에 배치 |
| `moai-marketing:campaign-planner` | 보조: 캠페인 단위 영상 시리즈 |
| `moai-commerce:detail-page-image` | 보조: 상세페이지 영상 |
| `moai-commerce:live-commerce` | 보조: 라이브 커머스 |

## References

- [`references/dop-motions.md`](./references/dop-motions.md) — 비디오 프리셋·카메라 디렉팅 가이드
- [Higgsfield 공식 사이트](https://higgsfield.ai) — 모델 11종 목록
- [Higgsfield MCP 안내](https://higgsfield.ai/mcp)
- [Higgsfield Skills](https://higgsfield.ai/skills) — 비디오 프리셋 6종

## 모델 목록 출처

본 스킬의 11개 영상 모델과 6개 비디오 프리셋은 **[higgsfield.ai 공식 사이트](https://higgsfield.ai)** 명시 기준입니다 (2026-05). 모델·프리셋은 Higgsfield 정책에 따라 추가·변경될 수 있습니다.
