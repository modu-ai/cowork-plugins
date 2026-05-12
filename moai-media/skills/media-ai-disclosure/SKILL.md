---
name: media-ai-disclosure
description: |
  [책임 경계] 모든 AI 생성 미디어 산출물(이미지·영상)에 "AI 생성" 표기를 자동 부착하는 표기 전담 스킬. 페어 스킬 media-gpt-image2-builder·media-model-router(생성)와 명확히 구분 — 생성이 아닌 표기 부착 후처리 전담. moai-media 내 다른 스킬이 산출물 반환 직전 자동 체인.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "AI 생성 표기 달아줘", "AI 표기 부착", "광고심의 AI 표기", "메타데이터 AI 생성", "워터마크 달아줘".
  V6 Day3 S2~S7 모든 미디어 산출물 ⑬·⑭·⑮·⑯·⑰ 자동 체인 + S7 클로징 일괄 가이드 (SPEC §3.1, REQ-MEDIA-002·010·011).
version: 2.3.0
---

# media-ai-disclosure — AI 생성 표기 자동 부착

## 개요

**책임 한 줄**: Day 3 S2~S7에서 AI로 생성·가공된 모든 이미지·영상 산출물에 "AI 생성" 표기를 메타데이터·워터마크·캡션 3계층으로 자동 부착하는 표기 전담 스킬.

**V6 18 산출물 체인 위치**: 산출물 ⑬·⑭·⑮·⑯·⑰ 모두 자동 체인 (Day3 S2~S7 전 세션) — AI 생성 이미지·영상이 생성될 때마다 후처리로 자동 호출됨.

**법적 근거**: PDF §6.3 AI 표기 원칙 — "AI 생성 이미지·영상은 'AI 생성' 표기 의무 (광고심의·소비자보호법 대비)".

> **캔바 매직 레이어 수정 후에도 유지 (REQ-MEDIA-011 HARD)**: Canva 매직 레이어로 텍스트·카피를 수정해도 "AI 생성" 메타데이터 표기는 유지되어야 합니다. media-canva-magic-layer 스킬 완료 후 이 스킬을 재호출하여 표기 유지 확인.

## 트리거 키워드

- "AI 생성 표기", "AI 표기 달아줘"
- "광고심의 대비 표기", "소비자보호법 AI 표기"
- "워터마크 달아줘", "AI 워터마크"
- "메타데이터 표기", "AI generated 태그"
- (자동 체인 — 수동 호출 없이도 media-gpt-image2-builder·media-model-router 후 자동 실행)

## 워크플로우

### 입력 슬롯

| 슬롯 | 출처 | 설명 |
|------|------|------|
| `media_files` | 각 생성 스킬 산출물 | 이미지(JPG/PNG) 또는 영상(MP4) |
| `model_info` | 생성 스킬 메타데이터 | 사용된 AI 모델명 (GPT Image 2·Veo 3·Kling 3·Seedance 2.0 등) |
| `generated_at` | 시스템 | ISO-8601 생성 시각 |
| `product_name` | 생성 스킬 컨텍스트 | 상품명 (메타데이터 식별용) |

### 처리 흐름

**Step 1 — 메타데이터 삽입**

이미지 (PNG/JPG):
- EXIF 메타데이터: `ImageDescription`, `UserComment` 필드에 AI 생성 표기
- PNG 텍스트 청크: `tEXt` 청크에 AI 생성 JSON 삽입

```json
{
  "ai_generated": true,
  "model": "GPT Image 2",
  "generated_at": "2026-05-12T14:08:00+09:00",
  "product": "마스크팩",
  "disclosure_standard": "PDF §6.3 + 광고심의",
  "skill": "media-gpt-image2-builder"
}
```

영상 (MP4):
- QuickTime/MP4 메타데이터 태그: `comment`, `description` 필드
- 첫 프레임 + 마지막 프레임: "AI 생성" 자막 오버레이 (텍스트 번인)

**Step 2 — 시각적 워터마크 (선택적)**

| 옵션 | 위치 | 크기 | 내용 |
|------|------|------|------|
| 표준 | 우측 하단 | 최소 (이미지 크기의 5%) | "AI 생성" 회색 반투명 |
| 강조 | 좌측 상단 | 소형 배지 | "AI 생성" 흰색 + 회색 배경 |
| 생략 | — | — | 메타데이터만 (기본값) |

> 광고심의 가이드 기준: 메타데이터 표기 필수, 시각적 워터마크는 매체 가이드에 따라 선택.

**Step 3 — 캡션 안내문 자동 생성**

수강생 측 게시물 업로드 시 사용할 캡션 안내:

```
예시 캡션:
"이 이미지는 AI(GPT Image 2)로 생성되었습니다. #AI생성 #AIgenerated"

예시 캡션 (영상):
"이 광고 영상은 AI(Higgsfield Kling 3)로 제작되었습니다. #AI생성"
```

**Step 4 — 부착 완료 확인 리포트**

```json
{
  "disclosure_report": {
    "files_processed": 5,
    "metadata_attached": 5,
    "watermark_applied": 0,
    "caption_generated": true,
    "compliance": "PDF §6.3 + 광고심의·소비자보호법 대응 완료"
  }
}
```

### 합격 기준 (PDF §6.3 + §6.8 S7)

- 모든 AI 생성 산출물 메타데이터에 표기 부착 완료
- 이미지: EXIF/PNG 텍스트 청크에 ai_generated JSON 삽입
- 영상: 첫 프레임·마지막 프레임 "AI 생성" 자막 + 메타데이터 태그
- Canva 매직 레이어 수정 후에도 표기 유지 확인

## 사용 예시

### 예시 1: 이미지 5장 자동 체인

```
media-gpt-image2-builder 완료 → media-ai-disclosure 자동 체인
→ 5장 이미지 EXIF + PNG 텍스트 청크 메타데이터 삽입
→ 캡션: "이 이미지는 AI(GPT Image 2)로 생성되었습니다."
→ 부착 완료 리포트 반환
```

### 예시 2: 영상 3편 표기

```
media-model-router 완료 (메인⑮ + 보조⑯ 2컷) → media-ai-disclosure 자동 체인
→ 첫 프레임: "AI 생성 (Higgsfield Veo 3)" 자막 번인
→ 마지막 프레임: "AI 생성" 자막 번인
→ MP4 메타데이터 태그 삽입
→ 3편 부착 완료
```

### 예시 3: Canva 매직 레이어 수정 후 재확인

```
media-canva-magic-layer 완료 (텍스트 교체) → media-ai-disclosure 재호출
→ 수정된 파일 메타데이터 표기 유지 확인
→ 누락 시 재부착 (REQ-MEDIA-011 준수)
```

### 예시 4: S7 클로징 일괄 가이드

```
Day3 S7 종료 시점 → 수강생에게 일괄 안내:
"오늘 생성한 모든 광고 소재에 AI 생성 표기가 자동 부착되었습니다.
채널 업로드 시 캡션에 '#AI생성' 해시태그를 포함해주세요.
광고심의 제출 시 메타데이터 파일을 함께 제출하세요."
```

## 출력 형식

```json
{
  "disclosure": {
    "total_files": 8,
    "images": {
      "count": 5,
      "format": "EXIF + PNG tEXt 청크",
      "ai_generated_flag": true
    },
    "videos": {
      "count": 3,
      "format": "MP4 메타데이터 + 프레임 번인",
      "first_frame_tagged": true,
      "last_frame_tagged": true
    },
    "caption_template": "이 콘텐츠는 AI로 생성되었습니다. #AI생성 #AIgenerated",
    "compliance": "PDF §6.3 + 광고심의 + 소비자보호법 대응",
    "canva_safe": "매직 레이어 수정 후 재확인 권장 (REQ-MEDIA-011)"
  }
}
```

## 합격 기준

| 항목 | 기준 |
|------|------|
| 이미지 메타데이터 | EXIF/PNG 텍스트 청크 AI 생성 JSON 삽입 |
| 영상 메타데이터 | MP4 메타데이터 태그 + 첫/마지막 프레임 자막 |
| 캡션 안내 | 수강생 게시용 캡션 템플릿 생성 |
| Canva 호환 | 매직 레이어 수정 후 표기 유지 확인 절차 포함 |

> 출처: PDF §6.3 AI 표기 원칙 + §6.8 S7 합격 기준 직접 인용

## 관련 스킬

- **자동 체인 ← media-gpt-image2-builder** (산출물 ⑬ 이미지 5장)
- **자동 체인 ← media-model-router** (산출물 ⑮⑯ 영상)
- **재호출 ← media-canva-magic-layer** (매직 레이어 수정 후 표기 유지 확인)
- **최종 확인 ← media-channel-ad-packager** (.zip 패키지 전 전체 소재 표기 확인)

## 이 스킬을 사용하지 말아야 할 때

| 상황 | 대신 사용할 스킬 |
|------|----------------|
| 이미지 신규 생성 | `media-gpt-image2-builder` 또는 `image-gen` |
| 영상 신규 생성 | `media-model-router` 또는 `video-gen` |
| 채널별 패키징 | `media-channel-ad-packager` |
| 사람이 직접 만든 콘텐츠 표기 | 해당 없음 — AI 생성 콘텐츠 전용 |
