---
name: higgsfield-video
description: >
  Higgsfield MCP를 호출해 영상을 생성합니다. "Higgsfield로 영상 만들어 줘", "Veo 3로",
  "Sora 2로", "Kling 3로", "DOP 카메라 워크", "말하는 머리 영상"이라고 말하면 자동 호출됩니다.
  Sora 2·Veo 3/3.1·Kling 3·Seedance·Minimax Hailuo·Wan·Image2Video·Infinite Talk 등
  31 영상 모델을 자연어 요청 한 줄로 선택·생성합니다. 카메라 무브먼트(DOP), 캐릭터 일관성,
  립싱크(Speak), 다양한 입력(text-to-video, image-to-video) 모두 지원. 비동기 잡 폴링까지 처리.
user-invocable: true
version: 2.13.0
---

# Higgsfield 영상 생성 (higgsfield-video)

## 개요

Higgsfield MCP의 `generate_video`·`generate_video_dop` 도구를 호출해 영상을 생성하는 스킬입니다. 31개 영상 모델 중 사용자 의도에 가장 적합한 것을 선택하고, 모션·카메라 무브먼트·캐릭터 일관성·립싱크까지 통합 처리합니다.

## 트리거 키워드

Higgsfield 영상, Sora 2, Veo 3, Veo 3.1, Kling 3, Kling 2.6, Seedance, Minimax Hailuo, Wan 영상, DOP 카메라 워크, Speak 말하는 머리, Infinite Talk, image2video, AI 영상 생성, 광고 영상, 시네마틱 영상

## 전제 — MCP 등록

`moai-media` 플러그인 설치 시 `.mcp.json`이 Higgsfield MCP를 자동 등록합니다 (이미지 스킬과 공유). 첫 호출 직전 Cowork에서 OAuth 인증 1회.

## 31 영상 모델 — 카테고리별 정리

### A. 일반 시네마틱 (text-to-video, image-to-video)

| 모델 | 강점 | 길이 | 적합 시점 |
|---|---|---|---|
| **Sora 2 (sora2-video)** ★ | 사실적·자연스러운 동작 | ~10s | 일반 광고·내러티브 |
| **Veo 3** | 고품질·다양한 톤 | ~8s | 마케팅·브랜드 영상 |
| **Veo 3.1** | Veo 3 개선판 | ~8s | Veo 3보다 새로움 (우선 시도) |
| **Kling 3 / kling/kling2-6** | 인물·캐릭터 모션 정교 | ~10s | 인물 중심·표정 강조 |
| **Seedance** | 빠르고 저비용 | ~5s | 빠른 시안·반복 시도 |
| **Minimax Hailuo** | 카메라 무브먼트 | ~6s | 트래킹·줌·팬 |
| **Wan 2.2 / 2.5 / 2.6** | 중국 최신 모델 | ~5-8s | 다양한 톤 실험 |

### B. 카메라 디렉팅 (DOP)

Higgsfield 자체의 **DOP (Director of Photography)** 모델은 카메라 무브먼트를 정밀 제어합니다.

| 모션 ID 카테고리 | 종류 |
|---|---|
| 줌 | Slow Zoom In/Out · Fast Zoom |
| 팬 | Pan Left/Right · Pan Up/Down |
| 트래킹 | Track In/Out · Side Track · Orbit |
| 돌리 | Dolly In/Out · Pedestal Up/Down |
| 특수 | Bullet Time · Rotation · Tilt |

상세 모션 ID는 [`references/dop-motions.md`](./references/dop-motions.md).

### C. 인물·캐릭터 (Speak·Character)

| 모델 | 역할 |
|---|---|
| **Speak (infinite-talk)** | 말하는 머리·립싱크 — 인물 이미지 + 음성 → 입 동작 영상 |
| **Image2Video** | 정적 이미지 → 자연스러운 모션 |
| **Character (Soul 영상 변형)** | 캐릭터 일관성 유지 (custom_reference_id) |

## 워크플로우

### 1단계 — 의도·길이·용도 파악

| 항목 | 자동 추론 |
|---|---|
| **길이** | "짧게"·"5초" → Seedance / "광고"·"10초" → Sora·Veo / "릴스"·"숏폼"·"15초" → Sora 2 |
| **용도** | 광고 · SNS · 내러티브 · 시연·튜토리얼 · 인물 발화 |
| **입력** | text-to-video · image-to-video · 인물 사진 + 스크립트 |
| **카메라 워크** | 정적 · DOP 무브먼트 · 핸드헬드 시뮬레이션 |

부족하면 AskUserQuestion 1라운드.

### 2단계 — 모델 자동 선택

| 사용자 표현 | 자동 모델 |
|---|---|
| "사실적", "자연스러운", "일반 광고" | Sora 2 또는 Veo 3.1 |
| "고품질 브랜드 영상" | Veo 3.1 |
| "인물 표정·연기 중요" | Kling 3 |
| "빠르게 여러 시안" | Seedance (저비용) |
| "카메라 트래킹·줌" | DOP + 적절한 base 모델 |
| "말하는 머리·립싱크" | Speak (infinite-talk) |
| "이 사진을 움직이게" | Image2Video |
| "캐릭터 시리즈 영상" | Soul image + image2video |
| "실험적·다양한 톤" | Wan 2.6 또는 Seedream |

### 3단계 — 입력 준비

#### Text-to-video
프롬프트만 필요. 모델이 첫 프레임부터 자체 생성.

#### Image-to-video
시작 이미지 필요. 시작 프레임이 결과 톤을 강하게 좌우.

```
[권장] higgsfield-image (Soul·Cinema Studio)로 정적 이미지 → image2video
```

#### Speak (말하는 머리)
인물 이미지 1장 + 음성 파일 또는 텍스트 스크립트. 음성은 `moai-media:audio-gen` (ElevenLabs)로 먼저 생성 후 사용.

### 4단계 — 파라미터 설계

#### 공통 파라미터

| 파라미터 | 값 |
|---|---|
| `prompt` | 영상의 행동·분위기·디테일 묘사 |
| `quality` | `turbo` (빠름·저렴) · `standard` · `high` |
| `aspect_ratio` | `16:9` · `9:16` (릴스·숏폼) · `1:1` · `4:5` |
| `duration_seconds` | 모델별 다름 (5-15초) |
| `seed` | 재현용 |

#### Image-to-video 추가

| 파라미터 | 값 |
|---|---|
| `image_url` 또는 `input_images[]` | 시작 이미지 URL |
| `motion_id` | DOP 사용 시 카메라 무브먼트 ID |

#### DOP 추가

```
generate_video_dop({
  input_image_url: "...",
  prompt: "...",
  motions: [
    { id: "slow_zoom_in", strength: 0.7 },
    { id: "pan_right", strength: 0.3 }
  ]
})
```

### 5단계 — MCP 호출

```
ToolSearch(query: "select:mcp__higgsfield__generate_video")

mcp__higgsfield__generate_video({
  image_url: "[시작 이미지 URL]",
  motion_id: "[카메라 모션 또는 자동]",
  prompt: "[행동·분위기 묘사]",
  quality: "standard"
})
```

DOP가 필요하면 `generate_video_dop` 도구로 분기.

### 6단계 — 비동기 잡 폴링

영상 생성은 이미지보다 오래 걸립니다. 5-30초 (모델별 다름).

| 상태 | 평균 시간 |
|---|---|
| queued | 잔액 정상 시 즉시 |
| in_progress | Sora 2/Veo: 20-60초 · Seedance: 5-15초 · Speak: 30-90초 |
| completed | 영상 URL 수령 |
| failed | 프롬프트·모델 호환성 문제 |
| nsfw | 콘텐츠 필터링 |

긴 영상(15초)은 1-2분도 정상.

### 7단계 — 결과 검수·반복

| 사용자 반응 | 후속 행동 |
|---|---|
| "좋다" | 다운로드·SNS 업로드 |
| "동작이 부자연스럽다" | Kling 3 또는 Veo 3.1로 모델 변경 |
| "카메라 워크 더" | DOP로 재생성 |
| "더 빠르게 / 짧게" | duration 단축 + Seedance로 |
| "음성 추가" | audio-gen (ElevenLabs) → 외부 편집 도구 |

## 사용 예시

### 예시 1 — 30초 광고 영상 (시네마틱)

```
요청: "신제품 가죽 지갑 광고 영상, 시네마틱, 8초"

플로우:
1. higgsfield-image (Cinema Studio)로 시작 이미지 1장 생성
2. higgsfield-video → image_url + Veo 3.1
3. prompt: "Slow camera pan revealing leather wallet on dark wood,
   warm light, depth of field, cinematic"
4. 8초 영상 수령
```

### 예시 2 — 릴스용 숏폼 (9:16)

```
요청: "5초 인스타 릴스 영상, 활기찬 톤, 음악과 어울리는"

자동 선택: Seedance (빠르고 저비용)
aspect_ratio: 9:16
duration: 5s
quality: turbo
```

### 예시 3 — 말하는 머리 (CEO 인사 영상)

```
요청: "CEO 신년 인사 영상 15초, 정면 샷 + 친근한 톤"

플로우:
1. higgsfield-image (Soul)로 CEO 정면 이미지 1장
2. audio-gen (ElevenLabs)로 한국어 TTS 15초
3. higgsfield-video → Speak (infinite-talk)
   - 이미지 + 음성 파일 → 립싱크 영상
4. 15초 영상 수령
```

### 예시 4 — DOP 카메라 디렉팅

```
요청: "제품을 360도 회전하면서 천천히 줌인하는 영상"

자동 선택: generate_video_dop
motions: [
  { id: "orbit_360", strength: 0.8 },
  { id: "slow_zoom_in", strength: 0.5 }
]
input_image_url: 제품 정사각 이미지
```

### 예시 5 — 캐릭터 시리즈 영상

```
요청: "브랜드 마스코트가 점프하는 5초 영상"

플로우:
1. higgsfield-image (Soul + reference)로 마스코트 정적 이미지
2. image2video로 점프 모션 추가
3. 5초 영상 수령
```

## 출력 형식

```
## Higgsfield 영상 생성 결과

### 호출 정보
- 모델: [선택 모델]
- 입력: text-to-video / image-to-video / speak
- 길이·비율·품질: [duration · aspect_ratio · quality]
- 카메라 워크: [DOP 모션 또는 정적]
- Job ID: [Higgsfield job ID]
- 소요 시간: [실제 처리 시간]

### 결과
- 영상 URL: [Higgsfield CDN URL]
- 다운로드 경로: [로컬 저장 시]
- 썸네일: [첫 프레임 이미지]

### 검수
- 모션 자연스러움: [점수]
- 의도 부합: [점수]
- 길이·비율: [PASS]

### 후속 추천
- 음성 추가 → audio-gen
- 편집·자막 → 외부 도구
- 시리즈 영상 → 같은 모델 + 다른 입력
```

## 비용 관리

| 모델 | 상대 비용 | 시간당 산출 |
|---|---|---|
| Seedance | 가장 저렴 | 5초/15-30크레딧 |
| Wan 2.2 | 저렴 | 5-8초/20-40 |
| Veo 3 / 3.1 | 중간 | 8초/40-80 |
| Sora 2 | 중간-비쌈 | 10초/60-120 |
| Kling 3 | 비쌈 | 10초/80-150 |
| Speak (infinite-talk) | 비쌈 | 15초/100-200 |
| DOP | base + 추가 | 모션 1개당 +20% |

워크스페이스 잔액: `higgsfield.ai → Billing`. 정확한 크레딧 단가는 Higgsfield 정책에 따라 변동.

## 주의사항

### Do

- 첫 시도는 **Seedance**로 빠르게 시안 확보 → 좋으면 Veo·Sora로 본 생성
- Image-to-video는 시작 이미지 품질이 결과를 좌우 — `higgsfield-image` (Soul·Cinema Studio) 권장
- DOP 모션은 0.5-0.8 strength가 자연스러움 (1.0은 과함)
- 광고용은 16:9 또는 9:16 (릴스) 고정 — 1:1은 인스타 피드만
- Speak 사용 전 음성을 `audio-gen`으로 먼저 생성

### Don't

- 한 영상에 너무 복잡한 동작 (3-4개 이상의 모션 + 카메라 워크) 요청 금지
- 10초 이상 영상에서 빠른 변화 요청 금지 — 모델이 자연스럽지 못함
- nsfw·민감 콘텐츠 — 필터링
- 다른 사람·유명인 초상권 침해 영상
- 저작권 있는 캐릭터·로고 직접 묘사

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| "Not connected" | OAuth 미인증 | Cowork → 설정 → MCP → Higgsfield → Connect |
| `queued`에서 멈춤 | 잔액 부족 | higgsfield.ai/billing 충전 |
| `failed` (image2video) | 시작 이미지 URL 오류 | higgsfield-image로 새 이미지 생성 후 재시도 |
| `failed` (DOP) | 모션 ID 잘못됨 | references/dop-motions.md의 표준 ID로 |
| 결과가 부자연스러움 | 모델 부적합 | Sora 2 ↔ Veo 3.1 ↔ Kling 3 교체 |
| 영상이 너무 짧음 | duration 미지정 | duration_seconds 명시 |
| Speak 입 동작 어색 | 음성 품질 낮음 | ElevenLabs로 고품질 음성 재생성 |
| 비용이 예상보다 큼 | 비싼 모델 사용 | Seedance로 우선 탐색 |

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:higgsfield-image` | 선행: 시작 이미지·캐릭터 reference 생성 |
| `moai-media:audio-gen` | 선행: Speak용 음성 또는 BGM 생성 |
| `moai-media:gemini-3-image-prompt` | 대안: 외부 도구용 프롬프트 |
| `moai-content:landing-page` | 후속: 영상을 랜딩에 배치 |
| `moai-marketing:campaign-planner` | 보조: 캠페인 단위 영상 시리즈 |
| `moai-commerce:detail-page-image` | 보조: 상세페이지 영상 |
| `moai-commerce:live-commerce` | 보조: 라이브 커머스 영상 |

## References

- [`references/dop-motions.md`](./references/dop-motions.md) — DOP 카메라 모션 ID 카탈로그·strength 가이드
- 공식 [Higgsfield MCP 페이지](https://higgsfield.ai/mcp)
- [Higgsfield AI 본사](https://higgsfield.ai)
