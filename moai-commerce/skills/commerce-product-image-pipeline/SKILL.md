---
name: commerce-product-image-pipeline
description: |
  [책임 경계] 상품 이미지·영상 풀스택 파이프라인 오케스트레이터. character-mgmt → image-gen(Soul) → video-gen(DOP) → media-channel-ad-packager 체인을 단일 자연어 입력으로 자동 호출. 한국 이커머스 셀러가 "상품 이미지·영상 만들어줘" 한 줄로 풀세트 산출.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "상품 이미지 만들어줘", "상품 영상 풀세트", "이미지부터 영상까지 한 번에", "상세페이지 이미지·영상 묶음", "비건 세럼 이미지·영상 패키지", "캐릭터 + 이미지 + 영상 한 번에", "이커머스 비주얼 파이프라인", "Higgsfield 풀세트 호출".
  4단계 체인: ① character-mgmt (선택, 브랜드 캐릭터 일관성) → ② image-gen (상품 이미지 5~10장) → ③ video-gen (시네마틱 영상 5~10초) → ④ media-channel-ad-packager (메타·네이버·카카오 채널 규격 변환).
  페어 스킬 detail-page-image(13섹션 합성 PNG)와 명확히 구분 — 본 스킬은 모델 체인 오케스트레이션, 페어는 단일 합성.
  ai-slop-reviewer 체이닝 제외 (이미지·영상 산출물).
  v2.7.0 신규.
user-invocable: true
version: 2.6.1
---

# 상품 이미지·영상 풀스택 파이프라인 (Product Image Pipeline)

## 개요

한국 이커머스 셀러가 "비건 세럼 이미지·영상 만들어줘" 같은 자연어 한 줄로 **캐릭터 일관성부터 채널별 패키징까지 4단계 체인**을 자동 호출하는 오케스트레이터 스킬입니다.

**책임 한 줄**: 상품 정보 + 카테고리 + 채널 입력 → character-mgmt(선택) → image-gen → video-gen → channel-ad-packager 4단계 체인 자동 실행 → 채널별 풀세트 산출물 반환.

**vs detail-page-image**: 페어 스킬은 13섹션 합성 PNG 1장 산출. 본 스킬은 **상품 이미지 5~10장 + 영상 5~10초 + 채널별 변환** 풀세트.

**vs media-model-router**: media-model-router는 광고 영상 1편 자동 라우팅. 본 스킬은 **이미지부터 영상까지 풀스택 체인** 오케스트레이션.

## 4단계 파이프라인

```
[Step 1] character-mgmt (선택, 권장)
   └─ 브랜드 마스코트 또는 모델 캐릭터 등록·재사용
   └─ 다음 단계에 character_id 전달 (일관성 확보)
   ↓
[Step 2] image-gen (Soul 모델)
   └─ 상품 이미지 5~10장 생성
   └─ Hero(1) · Lifestyle(2) · Detail(2) · Use-case(2) · Result(1~2) 5축
   ↓
[Step 3] video-gen (DOP 모델)
   └─ 시네마틱 영상 5~10초 (이미지 → 영상 변환)
   └─ orbit / pan_left / slow_zoom 모션 프리셋 적용
   └─ character_id 전달 (Step 1 사용 시)
   ↓
[Step 4] media-channel-ad-packager
   └─ 메타 (피드·릴스·스토리) / 네이버 GFA / 카카오 (친구톡·BizBoard)
   └─ 각 채널 규격 자동 변환 (해상도·길이·자막)
   └─ media-ai-disclosure 자동 체인 (AI 표기)
```

## 입력 슬롯

| 항목 | 필수 | 예시 |
|------|------|------|
| 상품 정보 | 필수 | "비건 세럼 50ml, 한국 농가 직거래, 30일 환불" |
| 카테고리 | 필수 | 스킨케어·식품·패션·반려동물·가전 등 |
| 캐릭터 사용 | 선택 | `사용 (character_id 필요)` / `미사용 (제품 단독)` |
| 채널 (1~3개) | 필수 | 메타·네이버 GFA·카카오 친구톡·카카오 BizBoard·쿠팡 |
| 톤·무드 | 권장 | 미니멀·따뜻함·프리미엄·활기참 등 |
| 영상 길이 | 권장 | 5초 (Instagram Story) / 10초 (Reel) / 15초 (TVC) |

## 산출 시나리오

### 시나리오 A: 신규 D2C 브랜드 (캐릭터 없음)

```
[Step 1] character-mgmt skip
[Step 2] image-gen:
   - Hero: 제품 단독 미니멀 샷 (1024×1024)
   - Lifestyle 2: 실제 사용 장면 (모델 손·테이블)
   - Detail 2: 매크로 클로즈업 (텍스처·라벨)
   - Use-case 2: 사용 순간 (얼굴·바를 때)
   - Result 1~2: 사용 후 결과 (Before/After 아닌 lifestyle)
[Step 3] video-gen:
   - Hero 이미지를 orbit 5초 시네마틱
   - 또는 lifestyle 이미지를 slow_zoom 10초
[Step 4] media-channel-ad-packager:
   - 메타 피드 1:1 / 메타 릴스 9:16 / 카카오 BizBoard 16:9
```

### 시나리오 B: 브랜드 마스코트 보유

```
[Step 1] character-mgmt:
   - 브랜드 마스코트 등록 (또는 기존 character_id 사용)
   - 다음 단계에 character_id 전달
[Step 2] image-gen with character_id:
   - 마스코트가 제품을 소개하는 이미지 (3D 캐릭터 + 제품)
   - 일관된 외형·복장·배경 유지
[Step 3] video-gen with character_id:
   - 마스코트 + 제품 등장 영상 (5~10초)
[Step 4] 채널 변환
```

### 시나리오 C: 모델 캐릭터 (가상 인플루언서)

```
[Step 1] character-mgmt:
   - 20대 후반 한국인 모델 캐릭터 등록
[Step 2] image-gen with character_id:
   - 모델이 제품 사용하는 이미지 5장
[Step 3] video-gen with character_id:
   - 모델 토킹 헤드 (speech-video 연동 가능)
   - 또는 모델 사용 장면 시네마틱
[Step 4] 채널 변환
```

## 출력 형식

```json
{
  "product": "비건 세럼 50ml",
  "category": "스킨케어",
  "character_used": true,
  "character_id": "characters/abc123",
  "pipeline_outputs": {
    "step_1_character": {
      "skip": false,
      "character_id": "characters/abc123",
      "type": "브랜드 마스코트 (Nova the Fox)"
    },
    "step_2_images": {
      "model": "Higgsfield Soul",
      "count": 7,
      "images": [
        {"type": "Hero", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Lifestyle-1", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Lifestyle-2", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Detail-1", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Detail-2", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Use-case", "url": "...", "aspect_ratio": "1:1"},
        {"type": "Result", "url": "...", "aspect_ratio": "1:1"}
      ]
    },
    "step_3_video": {
      "model": "Higgsfield DOP",
      "source_image": "Hero",
      "duration": 8,
      "motion_preset": "orbit",
      "url": "...",
      "character_id": "characters/abc123"
    },
    "step_4_channels": {
      "meta_feed": {"format": "1:1 1080×1080", "url": "..."},
      "meta_reel": {"format": "9:16 1080×1920", "url": "..."},
      "kakao_bizboard": {"format": "16:9 1280×720", "url": "..."}
    },
    "ai_disclosure": "AI 생성 표기 자동 부착 완료 (media-ai-disclosure)"
  },
  "total_assets": "이미지 7장 + 영상 1편 + 채널 변환 3개"
}
```

## 사용 예시

```
"/commerce-product-image-pipeline — 비건 세럼 50ml, 한국 농가 직거래, 스킨케어, 캐릭터 미사용, 메타 피드·릴스"
→ 4단계 자동 실행 → 이미지 7장 + 영상 1편 + 메타 피드·릴스 변환

"/commerce-product-image-pipeline — 반려견 간식, 마스코트 'Nova the Fox' 사용, 네이버 GFA 우선"
→ character-mgmt 호출 → 마스코트 + 제품 이미지·영상 → 네이버 GFA 변환

"/commerce-product-image-pipeline — 비건 세럼, 20대 한국 모델 사용, 토킹 헤드 포함, 메타 릴스"
→ character-mgmt 모델 등록 → image-gen + speech-video + video-gen → 릴스 변환
```

## 합격 기준

- 4단계 체인 모두 실행 (Step 1 선택적 skip)
- 이미지 5~10장 (Hero·Lifestyle·Detail·Use-case·Result 5축)
- 영상 5~10초 (시네마틱 모션 프리셋)
- 채널별 변환 완료 (선택한 1~3개 채널)
- media-ai-disclosure 자동 표기
- character_id 사용 시 일관성 검증 (선택적)

## 비용 추정

| 시나리오 | 단계 | 추정 비용 |
|---------|------|----------|
| 이미지 7장만 | image-gen Soul | ₩2,000~3,500 |
| + 영상 1편 (8초) | video-gen DOP | + ₩300~500 |
| + 채널 3개 변환 | media-channel-ad-packager | + ₩0 (Pillow 자체 처리) |
| + 캐릭터 등록 (최초 1회) | character-mgmt | + ₩0 (계정 플랜) |
| **총** | 풀세트 | **₩2,300~4,000 / 상품 1건** |

> 비용은 Higgsfield·fal.ai 종량제 기준. 실제 가격은 공식 사이트 확인 (higgsfield.ai · fal.ai/dashboard).

## 워크플로우

### Step 1: character-mgmt 의사결정

```
[Q1] 브랜드 마스코트 또는 모델 캐릭터를 이미 사용 중인가?
   ├─ 예 → 기존 character_id 입력 → Step 2 직진
   └─ 아니오 → [Q2]

[Q2] 일관된 캐릭터·모델로 시리즈 콘텐츠 만들 계획인가?
   ├─ 예 → character-mgmt 호출 → 신규 캐릭터 등록 (10~15분)
   └─ 아니오 → 제품 단독 이미지 모드 (Step 1 skip)
```

### Step 2~4: 자동 실행

- 카테고리에 따라 이미지 5축 (Hero·Lifestyle·Detail·Use-case·Result) 자동 분배
- 영상 모션 프리셋은 카테고리·톤에 따라 자동 선택 (스킨케어=slow_zoom / 패션=pan_left / 식품=orbit)
- 채널 변환은 각 채널 공식 규격 자동 적용

## 관련 스킬

체이닝 (본 스킬이 오케스트레이션):
- `character-mgmt` — Step 1 (선택)
- `image-gen` — Step 2 (Soul)
- `video-gen` — Step 3 (DOP)
- `media-channel-ad-packager` — Step 4
- `media-ai-disclosure` — Step 4 자동 체인

연계 (사용자가 별도 호출):
- `detail-page-image` — 13섹션 합성 PNG (페어, 다른 책임)
- `detail-page-copy` — 상세페이지 카피 (이미지·영상과 별도)
- `commerce-product-naming` — 상품명 (이미지 자막에 활용)

## 이 스킬을 사용하지 말아야 할 때

- **13섹션 합성 PNG 1장**: `detail-page-image` 사용
- **단일 이미지 생성**: `image-gen` 직접 호출
- **단일 영상 생성**: `video-gen` 직접 호출
- **광고 영상 카테고리 라우팅**: `media-model-router` 사용 (광고 전용)
- **이미지 이상의 AI 모델 (Flux·Recraft 등)**: `fal-gateway` 사용

## 참고 자료

- audit `research-2026-05-16/higgsfield-audit.md` §6 안 C 권장 #7
- moai-media 9 스킬 책임 매트릭스
- 한국 D2C 이커머스 표준 이미지 5축 (Hero·Lifestyle·Detail·Use-case·Result)

## SPEC

`.moai/specs/SPEC-PRODUCT-IMAGE-PIPELINE-001/spec.md` (v2.7.0 신규)
