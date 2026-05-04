---
name: fal-gateway
description: |
  fal.ai 1000+ AI 모델 유니버설 게이트웨이. 전용 스킬(image-gen, video-gen, audio-gen)이 없는 모델은 이 스킬을 통해 호출합니다.
  "Flux", "Recraft", "Hailuo", "Luma", "Pika", "MiniMax Music", "fal.ai", "1000개 모델" 요청 시 사용.
user-invocable: true
version: 2.0.0
---

# fal-gateway

## 개요

**fal.ai**의 1000개 이상의 AI 모델을 호출하는 유니버설 게이트웨이 스킬입니다. moai-media 플러그인의 전용 스킬(image-gen, video-gen, audio-gen)이 커버하지 않는 모델들을 이 스킬을 통해 사용할 수 있습니다. 이미지 생성(Flux, Recraft, SD 3.5), 비디오 생성(Hailuo, Luma, Pika), 오디오 생성(MiniMax Music) 등 다양한 최신 모델을 단일 인터페이스로 제공합니다.

### 왜 fal-gateway가 필요한가요?

- **모델 다양성**: 1000+ 모델, 매주 신규 모델 추가
- **전용 스킬과의 차별화**: Ideogram, Kling, ElevenLabs는 전용 스킬로 분리
- **폴백 메커니즘**: 전용 스킬이 지원하지 않는 모델의 마지막 수단
- **통합 인터페이스**: fal.ai key 하나로 모든 모델 접근

---

## 트리거 키워드

다음 요청 시 이 스킬을 사용하세요:

### 이미지 생성 (전용 스킬 미지원 모델)

- **Flux 시리즈**: "Flux 1.1 Pro", "Flux Ultra", "Flux Realism"
- **Recraft**: "Recraft V3", "Recraft Vector", "디자인 일러스트"
- **Stable Diffusion**: "SD 3.5", "Stable Diffusion XL"
- **스타일 기반**: "포토리얼리즘", "패션 일러스트", "벡터 아트"

### 비디오 생성 (전용 스킬 미지원 모델)

- **Hailuo**: "Hailuo AI", "Hailuo Standard/Pro"
- **Luma**: "Luma Ray3", "Luma Dream Machine"
- **Pika**: "Pika 2.2", "Pika Labs"
- **기타**: "MiniMax 비디오", "Fal 비디오"

### 오디오 생성 (전용 스킬 미지원 모델)

- **음악 생성**: "MiniMax Music", "AI 음악", "배경음악"
- **효과음**: "Stable Audio", "사운드 이펙트"

### 직접 언급

- "fal.ai 모델 사용", "Fal 플랫폼", "fal-ai 모델"

---

## 워크플로우

### 1. 모델 선택 및 호출

```
1. 사용자 요청 분석 (이미지/비디오/오디오, 스타일)
2. 라우팅 테이블 확인 (전용 스킬 vs fal-gateway)
3. 적합한 fal.ai 모델 선택
4. 모델별 파라미터 구성
5. fal.ai API 호출 → 결과 반환
```

### 2. 라우팅 결정 트리

```
┌─────────────────────────────────────────┐
│         사용자 요청 수신                 │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │   도메인 판별     │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
이미지?        비디오?        오디오?
    │             │             │
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│전용 스킬│   │전용 스킬│   │전용 스킬│
│(image-gen)│ │(video-gen)│ │(audio-gen)│
└────────┘   └────────┘   └────────┘
    │             │             │
    NO            NO            NO
    │             │             │
    └─────────────┴─────────────┘
                  │
            ┌─────┴─────┐
            │fal-gateway│
            └───────────┘
```

### 3. 모델별 파라미터 구성

각 모델의 고유 파라미터를 자동으로 매핑:
- 이미지: `prompt`, `negative_prompt`, `aspect_ratio`, `num_images`
- 비디오: `prompt`, `duration`, `aspect_ratio`, `fps`
- 오디오: `prompt`, `duration`, `instruments`, `genre`

---

## 사용 예시

### 예시 1: Flux 1.1 Pro로 하이퀄리티 이미지 생성

```
"Flux 1.1 Pro로 사이버펑크 도시 이미지 만들어줘.
네온 조명, 비오는 밤, 2048x2048 해상도."
→ 모델: flux-1.1-pro
→ 파라미터: aspect_ratio="1:1", num_inference_steps=50
→ 출력: 1024x1024 PNG
```

### 예시 2: Recraft V3로 벡터 일러스트 생성

```
"Recraft V3로 SaaS 제품 설명용 일러스트 5장 만들어줘.
스타일: 플랫 디자인, 파스텔 톤, 기술 테마."
→ 모델: recraft-v3
→ 파라미터: style="vector", num_images=5
→ 출력: SVG 파일 5개 (스케일 가능)
```

### 예시 3: Hailuo Pro로 10초 비디오 생성

```
"Hailuo Pro로 드론 샷 풍경 비디오 만들어줘.
알프스 산맥, 일출, 10초, 16:9."
→ 모델: hailuo-pro
→ 파라미터: duration=10, aspect_ratio="16:9"
→ 출력: 1920x1080 MP4 (30fps)
```

### 예시 4: MiniMax Music으로 배경음악 생성

```
"MiniMax Music으로 유튜브 Vlog용 배경음악 만들어줘.
장르: Lo-fi, 길이: 3분, 분위기: 차분한 오후."
→ 모델: minimax-music
→ 파라미터: duration=180, genre="lo-fi", mood="chill"
→ 출력: MP3 (320kbps)
```

---

## 출력 형식

### 이미지 생성

| 모델 | 해상도 | 포맷 | 가격 |
|------|--------|------|------|
| Flux 1.1 Pro | 1024x1024 | PNG | $0.04/장 |
| Flux Ultra | 2048x2048 | PNG | $0.06/장 |
| Recraft V3 | 1024x1024 | SVG | $0.04-0.08/장 |
| SD 3.5 | 1024x1024 | PNG | $0.04/장 |

### 비디오 생성

| 모델 | 해상도 | 초당 가격 | 특징 |
|------|--------|-----------|------|
| Hailuo Standard | 720p | $0.045/초 | 빠름, 컨셉 검증 |
| Hailuo Pro | 1080p | $0.08/초 | 고품질 |
| Luma Ray3 | 1080p | $0.32/MP | 프레임 단위 |
| Pika 2.2 | 1080p | ~$0.05/5초 | 다양한 스타일 |

### 오디오 생성

| 모델 | 길이 | 가격 | 특징 |
|------|------|------|------|
| MiniMax Music | 최대 5분 | $0.035/곡 | 가사/악기 선택 |
| Stable Audio | 최소 30초 | $0.02/클립 | 효과음 |

---

## 주의사항

### API 키 필수

**FAL_KEY** 환경변수가 필요합니다.

1. [fal.ai](https://fal.ai/dashboard/keys) 가입
2. Dashboard → API Keys → Create Key
3. `.env` 또는 시스템 환경변수에 등록:
   ```bash
   export FAL_KEY="your_fal_key_here"
   ```
4. 신규 가입 시 $5 무료 크레딧 제공

### 요금 안내

- **종량제**: 모델 실행 시에만 과금
- **무료 크레딧**: 신규 가입 $5 (약 125장 Flux 이미지)
- **예산 알림**: Dashboard에서 일일/월간 한도 설정 가능

### 전용 스킬과의 중복 방지

**fal-gateway를 호출하기 전에 먼저 확인하세요:**

| 기능 | 전용 스킬 | fal-gateway |
|------|-----------|-------------|
| Ideogram 3.0 (이미지) | ✅ image-gen | ❌ |
| Kling 3.0 (비디오) | ✅ video-gen | ❌ |
| ElevenLabs (오디오) | ✅ audio-gen | ❌ |
| Flux, Recraft, SD 3.5 | ❌ | ✅ fal-gateway |
| Hailuo, Luma, Pika | ❌ | ✅ fal-gateway |
| MiniMax Music | ❌ | ✅ fal-gateway |

**결정 규칙**: 전용 스킬이 해당 모델을 지원하면 → 전용 스킬 우선
 fal-gateway는 전용 스킬이 없는 모델만 호출

### 모델 업데이트 주기

- **주간 추가**: 매주 5-10개 신규 모델
- **모델 폐기**: 드물게 발생 (사전 공지)
- **버전 관리**: 모델명에 버전 포함 (예: flux-1.1-pro)

### 속도 및 큐

- **클라우드 실행**: 평균 5-30초 (모델/해상도 따름)
- **동기 vs 비동기**: 긴 작업은 비동기 권장
- **큐 대기**: 수요가 많을 시 지연 발생 가능

---

## 관련 스킬

### 전용 스킬 (우선 사용)

- **image-gen**: Ideogram 3.0, DALL-E 3, Midjourney (직접 지원)
- **video-gen**: Kling 3.0, Runway Gen-3 (직접 지원)
- **audio-gen**: ElevenLabs TTS, 보이스 클로닝, 더빙

### 보완 스킬

- **character-mgmt**: Higgsfield 캐릭터 생성 (fal.ai와 호환)
- **moai-content:blog**: 텍스트 → 이미지/비디오 프롬프트 변환

---

## MCP 서버 설정

이 스킬은 **fal.ai MCP** (HTTP hosted)를 사용합니다.

```json
{
  "fal-ai": {
    "type": "http",
    "url": "https://fal.ai",
    "headers": {
      "Authorization": "Key ${FAL_KEY}"
    }
  }
}
```

MCP 서버 등록 절차: `moai-media/CONNECTORS.md` 참조.

---

## 모델 카탈로그 (일부)

### 인기 이미지 모델

| 모델명 | 범주 | 해상도 | 가격 | 특징 |
|--------|------|--------|------|------|
| flux-1.1-pro | 포토리얼리즘 | 1024x1024 | $0.04 | 자연스러운 텍스처 |
| flux-ultra | 하이엔드 | 2048x2048 | $0.06 | 최고 품질 |
| recraft-v3 | 디자인 | 1024x1024 | $0.04-0.08 | SVG/벡터 지원 |
| sd3.5 | 스타일 다양성 | 1024x1024 | $0.04 | 커스텀 모델 |
| ideogram-v2-3 | 텍스트 렌더링 | 1024x1024 | $0.04 | 정확한 타이포그래피 |

### 인기 비디오 모델

| 모델명 | 범주 | 해상도 | 가격 | 특징 |
|--------|------|--------|------|------|
| hailuo-standard | 일반 비디오 | 720p | $0.045/초 | 빠름, 컨셉용 |
| hailuo-pro | 고품질 | 1080p | $0.08/초 | 디테일 강화 |
| luma-ray3 | 시네마틱 | 1080p | $0.32/MP | 영화 같은 품질 |
| pika-2.2 | 스타일 다양성 | 1080p | ~$0.05/5초 | 애니메이션, 레트로 |

### 인기 오디오 모델

| 모델명 | 범주 | 길이 | 가격 | 특징 |
|--------|------|------|------|------|
| minimax-music | 음악 생성 | 최대 5분 | $0.035/곡 | 가사, 악기 선택 |
| stable-audio | 효과음 | 최소 30초 | $0.02/클립 | 사운드 디자인 |

전체 카탈로그: [fal.ai/models](https://fal.ai/models)

---

## 라우팅 테이블 (참고용)

내부 라우팅 로직을 이해하면 더 효율적으로 사용할 수 있습니다.

### 이미지 요청 라우팅

```
IF 요청에 "Ideogram", "typography", "text rendering"
    → image-gen (Ideogram 3.0)
ELSE IF 요청에 "DALL-E", "Midjourney"
    → image-gen (직접 지원)
ELSE IF 요청에 "Flux", "Recraft", "SD 3.5"
    → fal-gateway
ELSE
    → fal-gateway (Flux 1.1 Pro 기본)
```

### 비디오 요청 라우팅

```
IF 요청에 "Kling", "Chinese video"
    → video-gen (Kling 3.0)
ELSE IF 요청에 "Runway", "Gen-3"
    → video-gen (Runway Gen-3)
ELSE IF 요청에 "Hailuo", "Luma", "Pika"
    → fal-gateway
ELSE
    → fal-gateway (Hailuo Standard 기본)
```

### 오디오 요청 라우팅

```
IF 요청에 "TTS", "voice", "speech", "ElevenLabs"
    → audio-gen
ELSE IF 요청에 "music", "song", "melody"
    → fal-gateway (MiniMax Music)
ELSE IF 요청에 "sound effect", "SFX"
    → fal-gateway (Stable Audio)
ELSE
    → audio-gen (기본 TTS)
```