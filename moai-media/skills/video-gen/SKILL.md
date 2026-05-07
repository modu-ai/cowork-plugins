---
name: video-gen
description: |
  통합 비디오 생성 스킬. 소스 이미지가 있는 시네마틱 모션 비디오는 Higgsfield DOP를,
  텍스트에서 비디오 생성이나 립싱크가 필요한 경우 fal.ai Kling 3.0을 사용합니다.
  브랜드 캐릭터가 포함된 비디오, 커스텀 모션 프리셋, 이미지-투-비디오 변환에 최적화되어 있습니다.

  다음과 같은 요청 시 이 스킬을 사용하세요:
  - "이 이미지로 비디오 만들어줘", "사진을 영상으로 변환"
  - "시네마틱한 모션 비디오 생성", "영화 같은 비디오 만들기"
  - "텍스트로 비디오 생성", "문장을 영상으로"
  - "브랜드 캐릭터가 나오는 비디오", "캐릭터 말하는 장면"
  - "립싱크 비디오", "입 모양 동기화"
  - "orbit 모션으로 줌인", "pan_left 카메라 움직임"
user-invocable: true
version: 2.1.0
---

# video-gen — 통합 비디오 생성 스킬

## 개요 (Overview)

AI 모델을 라우팅하여 최적의 비디오를 생성하는 통합 스킬입니다. 소스 이미지가 있는 시네마틱 비디오는 **Higgsfield DOP**를, 텍스트에서 비디오 생성이나 립싱크가 필요한 경우 **fal.ai Kling 3.0**을 사용합니다.

**핵심 특징:**
- **Higgsfield DOP** (1순위): 소스 이미지를 시네마틱 모션 비디오로 변환. 커스텀 모션 프리셋(slow_zoom, pan_left, orbit, tilt_up, dolly, static 등)과 브랜드 캐릭터 참조 지원
- **fal.ai Kling 3.0** (2순위): 텍스트-투-비디오(최대 15초), 이미지-투-비디오, 립싱크 기능

## 트리거 키워드 (Trigger Keywords)

이 스킬은 다음 상황에서 자동으로 호출됩니다:

- **이미지-투-비디오**: "이미지를 비디오로 변환", "사진에 움직임 추가", "정지 이미지를 영상으로"
- **시네마틱 모션**: "영화 같은 카메라 움직임", "orbit 줌", "pan left", "dolly shot"
- **텍스트-투-비디오**: "텍스트로 비디오 만들기", "문장을 영상으로 변환", "프롬프트로 비디오 생성"
- **캐릭터 비디오**: "브랜드 캐릭터가 나오는 비디오", "캐릭터 말하는 장면", "특정 인물 비디오"
- **립싱크**: "입 모양 동기화", "노래를 부르는 비디오", "말하는 동영상"
- **모션 프리셋**: "slow_zoom", "pan_left", "orbit", "tilt_up", "dolly", "static"

## 워크플로우 (Workflow)

### 1단계: 요구사항 분석

사용자 요청에서 다음을 확인합니다:
- 소스 이미지 존재 여부 (URL 또는 파일 경로)
- 모션 유형 (시네마틱, 텍스트 기반 생성, 립싱크)
- 브랜드 캐릭터 참조 필요성
- 비디오 길이 및 화면 비율

### 2단계: 모델 라우팅 결정

```
소스 이미지 있고 시네마틱 모션 원함?
  → 예: Higgsfield DOP (MCP: generate_video_dop)
  → 아니오 + 텍스트 프롬프트 있음: Kling Text-to-Video (fal.ai)
  → 아니오 + 립싱크 필요: Kling Image-to-Video (fal.ai)
```

### 3단계: 파라미터 구성

**Higgsfield DOP용 파라미터:**
- `image_url`: 소스 이미지 URL (필수)
- `prompt`: 모션 설명 (예: "카메라가 천천히 줌인하며 주변을 탐험")
- `motion_preset`: 모션 프리셋 (slow_zoom, pan_left, orbit, tilt_up, dolly, static 등)
- `character_id`: 브랜드 캐릭터 ID (선택, character-mgmt 스킬로 생성)
- `duration`: 비디오 길이 (초 단위, 기본값 5)
- `aspect_ratio`: 화면 비율 (16:9, 9:16, 1:1)
- `seed`: 재현성을 위한 시드 값 (선택)

**Kling용 파라미터:**
- `prompt`: 텍스트 프롬프트 또는 모션 설명
- `image_url`: 소스 이미지 URL (이미지-투-비디오 시)
- `duration`: 비디오 길이 (5초, 10초, 15초)
- `aspect_ratio`: 화면 비율

### 4단계: 생성 및 결과 전달

MCP 툴을 호출하여 비디오를 생성하고 결과 URL을 반환합니다.

## 사용 예시 (Usage Examples)

### 예시 1: 시네마틱 이미지-투-비디오 (Higgsfield DOP)

```
"이 제품 사진을 orbit 모션으로 5초짜리 비디오로 만들어줘."

→ Higgsfield DOP 호출:
  - image_url: (제품 사진 URL)
  - prompt: "카메라가 제품 주변을 천천히 회전하며 디테일을 보여줌"
  - motion_preset: "orbit"
  - duration: 5
  - aspect_ratio: "16:9"
```

### 예시 2: 텍스트-투-비디오 (Kling)

```
"해변에서 일몰을 배경으로 걷는 사람의 비디오를 만들어줘."

→ Kling Text-to-Video 호출:
  - prompt: "A person walking on a beach during sunset, cinematic lighting"
  - duration: 5
  - model: "fal-ai/kling-video/v3/text-to-video"
```

### 예시 3: 브랜드 캐릭터 비디오 (Higgsfield DOP + 캐릭터)

```
"우리 브랜드 마스코트가 wave 모션으로 인사하는 4초 비디오를 만들어줘."

→ Higgsfield DOP 호출:
  - image_url: (마스코트 이미지 URL)
  - prompt: "마스코트가 친근하게 손을 흔들며 인사함"
  - motion_preset: "dolly"
  - character_id: (character-mgmt 스킬로 생성된 캐릭터 ID)
  - duration: 4
  - aspect_ratio: "9:16"
```

### 예시 4: 립싱크 비디오 (Kling)

```
 "이 인물 사진으로 '안녕하세요'라고 말하는 립싱크 비디오를 만들어줘."

→ Kling Image-to-Video 호출:
  - image_url: (인물 사진 URL)
  - prompt: "Person saying '안녕하세요' with natural lip sync"
  - model: "fal-ai/kling-video/v3/image-to-video"
  - duration: 5
```

## 출력 형식 (Output Format)

### 성공 시

```markdown
## 비디오 생성 완료

**모델**: Higgsfield DOP / Kling 3.0
**길이**: 5초
**화면 비율**: 16:9
**모션 프리셋**: orbit

**비디오 URL**: [https://...]

**추가 작업**:
- 다른 모션 프리셋으로 재생성: `/video-gen [프리셋 이름]`
- 더 긴 비디오로 재생성: `/video-gen --duration 10`
- 브랜드 캐릭터 적용: 먼저 `/character-mgmt`로 캐릭터 생성 후 재시도
```

### 실패 시

```markdown
## 비디오 생성 실패

**오류**: [오류 메시지]

**해결 방법**:
- API 키 확인: `HIGGSFIELD_API_KEY`, `HIGGSFIELD_SECRET`, `FAL_KEY`
- 이미지 URL 확인: 공개적으로 접근 가능한 URL인지 확인
- 모션 프리셋 확인: 지원되는 프리셋 목록 참조
```

## 주의사항 (Cautions)

### API 키 필수

이 스킬을 사용하려면 다음 환경변수가 설정되어야 합니다:

- **Higgsfield**: `HIGGSFIELD_API_KEY`, `HIGGSFIELD_SECRET`
  - 발급처: Higgsfield 개발자 대시보드
  - MCP 설정: `moai-media/.mcp.json`에 `higgsfield` 서버로 등록

- **fal.ai**: `FAL_KEY`
  - 발급처: https://fal.ai/dashboard
  - MCP 설정: `moai-media/.mcp.json`에 `fal-ai` 서버로 등록

API 키 등록 절차: `moai-media/CONNECTORS.md` 참조

### 비용 참고

- **Higgsfield DOP**: 영상당 ~$0.10-0.30 (길이/품질에 따라 변동)
- **Kling Standard 5초**: ~$0.42
- **Kling Standard 10초**: ~$0.84
- **Kling Pro 10초**: ~$1.68

### 제한사항

- **Higgsfield DOP**: 이미지-투-비디오만 지원 (텍스트-투-비디오 불가). 소스 이미지가 반드시 필요합니다.
- **Kling Text-to-Video**: 최대 15초. 립싱크는 이미지-투-비디오 모델에서만 지원.
- **캐릭터 참조**: Higgsfield DOP만 지원. Kling은 캐릭터 ID를 사용할 수 없습니다.

### 모션 프리셋 목록 (Higgsfield DOP)

- `slow_zoom`: 천천히 줌인
- `pan_left`: 왼쪽으로 패닝
- `pan_right`: 오른쪽으로 패닝
- `tilt_up`: 위로 틸트
- `tilt_down`: 아래로 틸트
- `orbit`: 오빗 회전
- `dolly`: 돌리 이동
- `static`: 정적 (카메라 움직임 없음)

## 관련 스킬 (Related Skills)

- **character-mgmt**: 브랜드 캐릭터 생성 및 관리 (Higgsfield 캐릭터 ID 생성에 필요)
- **speech-video**: 텍스트를 말하는 "토킹 헤드" 비디오 생성 (Higgsfield speech-to-video)
- **image-gen**: 비디오 생성용 소스 이미지 생성 (fal.ai Imagen, Gemini 3)

## 기술 참고사항

- **MCP 툴**: `generate_video_dop` (Higgsfield), `fal-ai/kling-video/v3/*` (fal.ai)
- **지원 모델**: Higgsfield DOP (image-to-video), fal.ai Kling 3.0 (text-to-video, image-to-video)
- **최대 길이**: Higgsfield DOP (최대 10초), Kling (최대 15초)
- **지원 화면 비율**: 16:9 (가로), 9:16 (세로), 1:1 (정사각형)

---

버전: 1.0.0
최종 업데이트: 2026-04-30