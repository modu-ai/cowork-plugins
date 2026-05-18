# Gemini 3 Pro Image — Parameter Cheatsheet

Google AI Studio / Vertex AI / Gemini API에서 사용하는 파라미터.

## 모델 선택

| 모델 ID | 별명 | 용도 |
|---|---|---|
| `gemini-3-pro-image-preview` (권장) | Nano Banana Pro | 최종 납품, 고품질, 4K, 복잡 구도 |
| `gemini-3.1-flash-image-preview` | Nano Banana 2 | 초안, A/B, 비용 효율, 1K-2K |

## aspect_ratio

| 값 | 용도 | 두 모델 지원 |
|---|---|---|
| `1:1` (권장) | SNS 정사각 | ✅ Pro · ✅ Flash |
| `16:9` | 와이드, 유튜브 | ✅ · ✅ |
| `9:16` | 릴스·쇼츠 | ✅ · ✅ |
| `4:5` | 인스타 피드 | ✅ · ✅ |
| `5:4` | 인스타 가로 | ✅ · ✅ |
| `3:2` | 사진 표준 | ✅ · ✅ |
| `2:3` | 책 표지 | ✅ · ✅ |
| `4:3` | TV 클래식 | ✅ · ✅ |
| `3:4` | 모바일 세로 | ✅ · ✅ |
| `21:9` | 시네마틱 울트라와이드 | ✅ · ✅ |
| `1:4`·`4:1`·`1:8`·`8:1` | 극단 비율 (배너·스트립) | ❌ Pro · ✅ Flash 전용 |

## resolution

| 값 | 픽셀 어림 | Pro | Flash |
|---|---|---|---|
| `512` (0.5K) | 약 0.5K | ❌ | ✅ |
| `1K` (권장 초안) | 약 1024 | ✅ | ✅ |
| `2K` (권장 production) | 약 2048 | ✅ | ✅ |
| `4K` | 약 4096 | ✅ | ✅ |

## mode (Google AI Studio UI 선택지)

| 모드 | 동작 | 권장 |
|---|---|---|
| `Fast` (Gemini 3.1 Flash Image) | 빠른 추론, 적은 latency | 초안 탐색, A/B |
| `Thinking` (Gemini 3 Pro Image) | reasoning 추가, 정확도 우선 | 최종 production, 복잡 구도, 텍스트 정확도 |

## reference images

- 최대 **14개** 첨부 가능.
- 지원 MIME: `image/png`, `image/jpeg`, `image/webp`, `image/heic`, `image/heif`.
- 권장 사용:
  - 1번째: 메인 스타일·미학 방향
  - 2번째: 캐릭터·핵심 피사체 (있는 경우)
  - 3번째: 구도·레이아웃 영감
  - 4-8번째: 부수적 스타일·색감·무드
  - 9-14번째: 추가 디테일 (적게 쓸수록 좋음)

상세는 `references/reference-images.md`.

## Search Grounding

데이터 시각화·인포그래픽·지도·통계 그래프에 활성화 권장. Gemini가 Google Search를 사용해 사실 데이터를 가져옴.

활성화 방법 (Google AI Studio):
- "Use Google Search" 체크박스 활성화
- 프롬프트에 "based on current 2026 data" 같은 시간 명시 권장

주의: 결과는 항상 별도 검증. 모델이 정보를 잘못 해석할 수 있음.

## 토큰 제한

| 모델 | 입력 토큰 | 출력 토큰 |
|---|---|---|
| Gemini 3 Pro Image | 65,536 | 32,768 |
| Gemini 3.1 Flash Image | 131,072 | 32,768 |

긴 텍스트 + 다중 reference 이미지를 함께 사용할 때 토큰 budget 주의.

## API 호출 예 (Python · Vertex AI)

```python
from vertexai.preview.generative_models import GenerativeModel, Part

model = GenerativeModel("gemini-3-pro-image-preview")
response = model.generate_content(
    [
        "<5-component 프롬프트>",
        Part.from_uri("gs://bucket/ref1.png", mime_type="image/png"),
        Part.from_uri("gs://bucket/ref2.png", mime_type="image/png"),
    ],
    generation_config={
        "aspect_ratio": "1:1",
        "resolution": "2K",
    },
)
```

## SynthID 워터마크

- 모든 출력 이미지에 **자동 imperceptible 워터마크 삽입** (Google 정책).
- 워터마크 비활성화 불가.
- SynthID 검증 도구로 "Gemini로 생성·편집됐는지" 판별 가능.
- 상업적 사용 가능 (유료 사용자).

## 비용 (Vertex AI 기준, 2026.04)

상세 가격은 공식 가격 페이지 확인. 일반적으로:
- Flash: Pro 대비 약 절반 비용
- Thinking Mode: 추가 reasoning 토큰 비용 발생
- Reference 이미지: 입력 토큰에 포함

## 출처

- [Google AI for Developers — Gemini 3 Pro Image Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Google Cloud Documentation — Gemini 3 Pro Image (Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- [Google AI Studio — Gemini 3 Pro Image](https://aistudio.google.com/models/gemini-3-pro-image)
