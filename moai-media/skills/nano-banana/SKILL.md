---
name: nano-banana
description: >
  Google Gemini API 기반 한글 타이포그래피 특화 이미지 생성 스킬입니다.
  한국어 텍스트 렌더링 품질이 SOTA 수준으로, 카드뉴스 제목·포스터·광고 크리에이티브에 최적.
  '나노바나나', '구글 이미지 생성', '한글 타이포 이미지', '카드뉴스 제목',
  '/moai-media nano-banana'으로 호출하세요.
  **일반 이미지 생성은 image-gen 스킬을 우선 사용하세요.** 본 스킬은 한글 텍스트 렌더링 특화 용도입니다.
user-invocable: true
version: 2.0.0
---

# Nano Banana — 한글 타이포그래피 특화 이미지 생성

## 개요

**Nano Banana**는 Google의 공식 AI 이미지 브랜드로, 2026년 Q1에 Imagen 4 계열에서 **Gemini 3 Image Preview 계열로 재정의**되었습니다.

본 스킬은 **한국어 텍스트 렌더링 품질이 업계 최고 수준(SOTA)**이어서, 카드뉴스 제목·포스터·광고 크리에이티브처럼 **글자가 중요한 이미지**에 특화되어 있습니다.

> **중요**: 일반적인 이미지 생성(배경, 풍경, 제품 사진 등)은 [`image-gen`](../image-gen/SKILL.md) 스킬을 사용하세요. 본 스킬은 한글 타이포그래피 특화 용도입니다.

### 언제 사용하나?

| 상황 | 권장 스킬 |
|---|---|
| **카드뉴스 제목 슬라이드** (큰 한글 헤드라인) | **nano-banana** ⭐ |
| **포스터·광고 크리에이티브** (한글 카피) | **nano-banana** ⭐ |
| **인스타 썸네일** (제목 텍스트 포함) | **nano-banana** ⭐ |
| **일반 배경·이미지** (텍스트 없음) | [`image-gen`](../image-gen/SKILL.md) |
| **시네마틱·제품 사진** | [`image-gen`](../image-gen/SKILL.md) |
| **영상 생성** | [`video-gen`](../video-gen/SKILL.md) (fal.ai Kling·Hailuo 백엔드) |

## 트리거 키워드

이 스킬은 다음과 같은 요청 시 자동으로 호출됩니다:

- "나노바나나", "구글 이미지 생성"
- "한글 타이포 이미지", "카드뉴스 제목"
- "텍스트 들어간 포스터", "광고 카피 이미지"
- "/moai-media nano-banana" (직접 호출)

## 워크플로우

### 1단계: 모델 선택

| Alias | 공식 모델 ID | 용도 | 해상도 | 비용/장 |
|---|---|---|---|---|
| **nano-banana-pro** (기본) | `gemini-3-pro-image-preview` | 최종 납품, 고품질 | 2K | $0.134 |
| **nano-banana-2** | `gemini-3.1-flash-image-preview` | 초안, A/B 테스트, 비용 효율 | 1K | $0.067 |

**공식 모델은 Pro와 2 두 가지뿐입니다.**

### 2단계: 프롬프트 작성 (한글 텍스트 렌더링)

한글 타이포그래피 품질을 높이는 팁:

- **텍스트는 큰따옴표로 감싸기**: `"완벽한 주말" 이라는 제목`
- **폰트 스타일 명시**: `깔끔한 고딕 폰트`, `진한 세리프`, `손글씨 느낌의 한글`
- **위치 지시**: `상단 중앙에 큰 글씨로`, `하단 우측 작게`
- **줄바꿈 지시**: `두 줄로 나눠서 중앙 정렬`
- **배경 분리**: `파스텔 배경, 텍스트는 검정색`

### 3단계: 화면비 선택

지원하는 14종 화면비:

| 용도 | 화면비 |
|---|---|
| 카드뉴스 (인스타 세로) | 3:4 |
| 인스타 피드 | 1:1 |
| 릴스/스토리 | 9:16 |
| 유튜브 썸네일 | 16:9 |
| 시네마틱 | 21:9 |
| 배너 | 8:1, 4:1 |

전체 목록: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`

### 4단계: 이미지 생성

CLI 또는 Python SDK로 호출합니다.

## 사용 예시

### 예시 1: 카드뉴스 제목 (Pro)

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  "'2025년 봄 트렌드'라는 한글 제목, 파스텔 톤 배경, 깔끔한 고딕 폰트, 상단 중앙" \
  output/slide_01.png 3:4 nano-banana-pro
```

### 예시 2: A/B 테스트 초안 (Flash)

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_image.py" \
  "'봄 신상품' 제목, 미니멀 배경, 화이트 폰트" \
  output/ab_test_01.png 1:1 nano-banana-2
```

### 예시 3: Python SDK (코드 내 호출)

```python
from google import genai

client = genai.Client()  # GEMINI_API_KEY 환경변수 자동 인식

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["'오늘의 인사이트'라는 한글 제목, 파스텔 배경, 상단 중앙"],
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
```

## 출력 형식

### CLI 출력

- 파일 경로: `output/<filename>.png`
- 해상도: Pro는 2K (~2048px), Flash는 1K (~1024px)

### Python SDK 출력

- `response.parts[].inline_data.data` (base64 인코딩된 이미지)
- PIL.Image 객체로 변환 가능: `part.as_image()`

### REST API 출력

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "data": "<base64 이미지 데이터>",
          "mimeType": "image/png"
        }
      }]
    }
  }]
}
```

## 주의사항

### API 키 필수

- 환경변수: **`GEMINI_API_KEY`** (권장)
- 레거시 호환: `NANO_BANANA_API_KEY`도 인식 (v1.0.x 사용자 무중단)
- 발급처: [ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)
- **Pay-as-you-go 결제 활성화 필수** (무료 티어에서 호출 불가)

### 비용 예시

| 시나리오 | 모델 | 해상도 | 비용 |
|---|---|---|
| 카드뉴스 10장 시리즈 (권장) | nano-banana-pro | 2K | $1.34 |
| A/B 초안 50장 | nano-banana-2 | 1K | $3.35 |
| 썸네일 100장 대량 | nano-banana-2 | 1K | $6.70 |

**월 예산 예시**: 포트폴리오 3 브랜드 × 주 1편 카드뉴스 × 한 달 = 약 $16

### 레거시 별칭 자동 승격

사용자 코드 무수정 보장을 위해 다음 별칭을 자동으로 새 모델 ID로 변환합니다:

- `imagen-4.0-*`, `imagen-3.0-*` → Pro 또는 2로 자동 전환
- `nano-banana`, `nano-banana-ultra`, `ultra` (v1.1.x 이전) → **Pro로 자동 승격**
- `cheap` → 2로 자동 승격

### 네이밍 컨벤션 주의

- **Python SDK**: snake_case (`response_modalities`, `image_config`, `aspect_ratio`, `image_size`, `inline_data`)
- **REST/JS SDK**: camelCase (`responseModalities`, `imageConfig`, `aspectRatio`, `imageSize`, `inlineData`)

## 관련 스킬

- **image-gen** (moai-media) — **일반 이미지 생성 전담** (본 스킬보다 우선 사용 권장)
- **fal-gateway** (moai-media) — fal.ai 1000+ 모델 통합 진입점 (Ideogram v3·Flux 등 대안 모델)
- **video-gen** (moai-media) — 이미지를 영상으로 변환 (fal.ai Kling·Hailuo 백엔드)
- **audio-gen** (moai-media) — TTS·음성 합성 (ElevenLabs MCP 사용, 이미지 + 내레이션 조합)
- **card-news** (moai-content) — 본 스킬 호출로 카드뉴스 이미지 생성

## 이관 이력

- **v1.3.0 (2026-04-30)**: 한글 타이포그래피 특화 스킬로 재정의. 일반 이미지 생성은 [`image-gen`](../image-gen/SKILL.md) 스킬로 이관.
- **v1.1.3 (2026-04-14)**: `nano-banana-ultra` 제거 → Pro + 2 단 두 가지만. 기존 별칭은 자동 승격.
- v1.1.2: `gemini-2.5-flash-image` 제거, 2종 체제 확립
- v1.1.1: `google-media` → `nano-banana` 개명 (image-only), Veo 3.1 → `kling` 이관
- v1.1.0: Imagen 4 → Gemini 3 Image Preview 마이그레이션

## 공식 참고 문서

- [Gemini API Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini 3 Pro Image Preview 모델 카드](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Gemini API 가격](https://ai.google.dev/gemini-api/docs/pricing)
- [Nano Banana Pro 공식 소개 블로그](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-3-pro-image-developers/)