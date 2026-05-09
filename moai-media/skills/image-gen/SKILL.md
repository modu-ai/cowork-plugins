---
name: image-gen
description: >
  통합 AI 이미지 생성 스킬로 Higgsfield Soul(시네마틱/제품 사진), fal.ai(Flux/ Ideogram/Recraft),
  Gemini Direct를 상황별 최적 모델로 자동 라우팅합니다.
  '이미지 생성', '카드뉴스 이미지', '제품 사진', '썸네일 만들어줘', '포스터 디자인',
  '/moai-media image-gen'으로 호출하세요.
  제품 사진·편집 스타일은 Higgsfield Soul, 한글 타이포그래피는 Ideogram 또는 Gemini,
  포토리얼리즘은 Flux, 벡터/로고는 Recraft를 자동 선택합니다.
user-invocable: true
version: 2.2.0
---

# Image Gen — 통합 AI 이미지 생성

## 개요

**image-gen**은 moai-media 플러그인의 **통합 이미지 생성 스킬**입니다. 사용자의 요구 사항을 분석하여 최적의 AI 모델로 자동 라우팅합니다.

- **Higgsfield Soul** (기본): 시네마틱 이미지, 제품 사진, 편집 스타일. 15+ 스타일 프리셋 지원.
- **fal.ai 모델**: Flux 1.1 Pro(포토리얼리즘), Ideogram 3.0(한글 타이포), Recraft V3(벡터/로고).
- **Gemini Direct**: 한글 타이포그래피 특수 케이스.

## 트리거 키워드

이 스킬은 다음과 같은 요청 시 자동으로 호출됩니다:

- "이미지 생성해줘", "이미지 만들어줘"
- "카드뉴스 이미지", "인스타 썸네일"
- "제품 사진", "상세페이지 배너"
- "포스터 디자인", "광고 크리에이티브"
- "로고 만들어줘", "벡터 아이콘"
- "시네마틱 이미지", "영화 같은 사진"
- "/moai-media image-gen" (직접 호출)

## 워크플로우

### 1단계: 사용자 요구 분석

사용자 프롬프트에서 다음을 식별합니다:
- **텍스트 포함 여부**: 한글/영문 타이포그래피가 있는지
- **스타일**: 시네마틱, 제품 사진, 편집, 포토리얼리즘, 벡터/로고
- **화면비**: 1:1, 3:4, 9:16, 16:9 등

### 2단계: 모델 라우팅

| 상황 | 최적 모델 | 라우팅 기준 |
|---|---|---|
| **한글 대형 타이포** | Ideogram 3.0 (fal.ai) 또는 Gemini Direct | 텍스트가 이미지의 30% 이상을 차지 |
| **시네마틱/제품 사진** | **Higgsfield Soul** (기본) | product_photography, cinematic, editorial 스타일 |
| **포토리얼리즘 일반** | Flux 1.1 Pro (fal.ai) | 일반적인 사진现实主义 |
| **벡터/로고** | Recraft V3 (fal.ai) | 로고, 아이콘, 벡터 그래픽 |
| **한글 소형 타이포** | Gemini Direct | 텍스트가 10% 미만인 경우 |
| **기본** | **Higgsfield Soul** | 명시적 스타일 지정 없음 |

### 3단계: 이미지 생성

선택된 모델의 MCP 툴 또는 Python 스크립트를 호출합니다.

## 사용 예시

### 예시 1: 시네마틱 제품 사진 (Higgsfield Soul)

```
"프리미엄 커피 머신 제품 사진, 편집지 스타일, 부드러운 조명, 미니멀 배경"
→ Higgsfield Soul, style_preset: product_photography
```

### 예시 2: 카드뉴스 제목 (Ideogram 3.0)

```
"'2025년 봄 트렌드'라는 한글 제목, 파스텔 톤 배경, 인스타그램 세로"
→ Ideogram 3.0 via fal.ai, aspect_ratio: 3:4
```

### 예시 3: 브랜드 로고 (Recraft V3)

```
"미니멀 로고, 서울 브랜드, 깔끔한 벡터 스타일, 블루와 화이트"
→ Recraft V3 via fal.ai
```

### 예시 4: 포토리얼리즘 풍경 (Flux Pro)

```
"서울 여의도 공원 봄 벚꽃, 해 질 녘, 따뜻한 조명"
→ Flux 1.1 Pro via fal.ai
```

## 출력 형식

### Higgsfield Soul (MCP)

MCP 툴: `higgsfield.generate_image_soul`

주요 파라미터:
- `prompt` (string): 이미지 설명
- `style_preset` (string): 스타일 프리셋 (product_photography, editorial, cinematic, abstract, minimalist 등 15+)
- `aspect_ratio` (string): 1:1, 3:4, 9:16, 16:9
- `num_images` (int): 생성할 이미지 수 (1-4)
- `seed` (int, optional): 재현성을 위한 시드 값

출력: 이미지 URL 배열

### fal.ai 모델 (MCP)

MCP 툴: `fal-ai.run_inference`

모델별 파라미터:
- **Ideogram 3.0**: `fal-ai/ideogram/v3` - prompt, rendering_speed (TURBO/DEFAULT/QUALITY), aspect_ratio
- **Flux 1.1 Pro**: `fal-ai/flux-pro/v1.1-ultra` - prompt, image_size, num_inference_steps
- **Recraft V3**: `fal-ai/recraft-v3` - prompt, style_vector, aspect_ratio

### Gemini Direct (Python 스크립트)

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  "프롬프트" output/image.png 3:4 nano-banana-pro
```

## 주의사항

### API 키 필수

이 스킬을 사용하려면 다음 API 키가 필요합니다:

| 서비스 | 환경변수 | 발급처 | 비용 |
|---|---|---|---|
| **Higgsfield** | `HIGGSFIELD_API_KEY`, `HIGGSFIELD_SECRET` | Higgsfield AI | ~$0.05-0.15/장 |
| **fal.ai** | `FAL_KEY` | [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) | 모델별 상이 |
| **Gemini** | `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key) | $0.067-0.134/장 |

### 비용 참고

| 모델 | 용도 | 이미지당 비용 |
|---|---|---|
| Higgsfield Soul | 시네마틱/제품 사진 | ~$0.05-0.15 |
| Ideogram 3.0 | 한글 타이포 | ~$0.03-0.08 |
| Flux 1.1 Pro | 포토리얼리즘 | ~$0.04 |
| Recraft V3 | 벡터/로고 | ~$0.02-0.05 |
| Gemini Pro | 한글 타이포 특수 | $0.134 (2K) |
| Gemini Flash | 한글 타이포 특수 | $0.067 (1K) |

### 사용 권장사항

- **대량 생성**: 비용 최적화를 위해 Gemini Flash 또는 Ideogram TURBO 모드 사용
- **최종 납품**: Higgsfield Soul QUALITY 또는 Ideogram QUALITY 모드 사용
- **A/B 테스트**: 저렴한 모델로 시안 후 최종본은 고가 모델로 생성

## 관련 스킬

- **nano-banana** (moai-media) — 한글 타이포그래피 특화 Gemini 3 Image 스킬
- **video-gen** (moai-media) — 통합 영상 생성 (이미지→영상, 텍스트→영상, fal.ai Kling·Hailuo 백엔드)
- **audio-gen** (moai-media) — TTS·음성 합성 (ElevenLabs MCP 사용)
- **speech-video** (moai-media) — 음성+영상 립싱크 결합
- **character-mgmt** (moai-media) — Higgsfield 캐릭터 관리 (브랜드 일관성)
- **fal-gateway** (moai-media) — Flux·Ideogram·Recraft 등 fal.ai 1000+ 모델 통합 진입점

## 참고 자료

- [Higgsfield AI 공식 문서](https://higgsfield.ai)
- [fal.ai 모델 카탈로그](https://fal.ai/models)
- [Gemini API Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)