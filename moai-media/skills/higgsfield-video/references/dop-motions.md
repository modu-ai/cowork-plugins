# Higgsfield 영상 프리셋·카메라 디렉팅 가이드

[higgsfield.ai/skills](https://higgsfield.ai/skills) 명시 기준 (2026-05).

Higgsfield 공식 자료에는 6가지 **비디오 프리셋**과 모델 11종이 공개되어 있습니다. 일부 커뮤니티 MCP 구현체에는 추가 카메라 모션 도구(DOP)가 존재하지만, **공식 페이지에는 별도 모델로 명시되어 있지 않습니다**. 본 가이드는 공식 프리셋·모델 중심으로 카메라 디렉팅을 다룹니다.

## 6가지 공식 비디오 프리셋

| 프리셋 | 용도 | 적합 모델 |
|---|---|---|
| **UGC** | 일반 사용자 콘텐츠 톤 — 자연스러움 | Kling 2.5 Turbo · Seedance 2.0 |
| **Unboxing** | 언박싱·제품 개봉 | Seedance Pro · Google Veo 3 |
| **Product review** | 제품 리뷰 (특징 강조) | Seedance Pro · Cinema Studio 3.5 |
| **Hyper motion** | 빠른 모션·다이내믹 | Seedance Pro · Seedance 2.0 |
| **TV spot** | 광고 TV 톤 (시네마틱) | Cinema Studio 3.5 · Google Veo 3 |
| **Wild Card** | 실험적·창의적 자유 톤 | Wan 2.5 · Kling 3.0 |

## 프리셋 사용 가이드

### UGC

```
preset: "UGC"
권장: 자연스러운 손이 흔들리는 듯한 핸드헬드 톤
적합: 인스타 릴스·틱톡·자연스러운 소셜
```

### Unboxing

```
preset: "Unboxing"
권장: 위에서 내려보는 시점 + 천천히 줌인 + 제품 노출
적합: 신제품 출시·이커머스 첫 인상
```

### Product review

```
preset: "Product review"
권장: 다각도 회전 + 디테일 클로즈업 + 사용 시연
적합: 제품 페이지·광고 첫 30초
```

### Hyper motion

```
preset: "Hyper motion"
권장: 빠른 컷·역동적 카메라·시각적 임팩트
적합: 댄스·액션·게임 마케팅·이벤트
```

### TV spot

```
preset: "TV spot"
권장: 영화적 그레이딩·시네마틱 카메라·내러티브
적합: 브랜드 광고·TV CM·고급 캠페인
```

### Wild Card

```
preset: "Wild Card"
권장: AI 자율 — 실험적·창의적 접근
적합: 무드보드·아트워크·새로운 시도
```

## 모델 선택 → 카메라 디렉팅

| 사용자 의도 | 권장 모델 | 권장 프리셋 |
|---|---|---|
| 시네마틱 광고 | Cinema Studio 3.5 또는 Google Veo 3 | TV spot |
| 빠른 SNS 시안 | Kling 2.5 Turbo | UGC |
| 다이내믹 모션 | Seedance Pro | Hyper motion |
| 제품 회전 노출 | MiniMax Hailuo 02 또는 Seedance Pro | Product review |
| 언박싱 | Seedance Pro | Unboxing |
| 인물 캐릭터 시리즈 | Kling Avatars 2.0 | (프리셋 없이) |
| 실험적·창의적 | Wan 2.5 | Wild Card |

## 영상 길이·비율 조합

| 채널 | 비율 | 길이 | 권장 모델·프리셋 |
|---|---|---|---|
| 인스타 피드 (16:9) | 16:9 | 6-15s | Veo 3 · Sora 2 · Cinema Studio 3.5 + TV spot |
| 인스타 릴스·스토리 | 9:16 | 5-9s | Kling 2.5 Turbo · Seedance 2.0 + UGC |
| 페북·유튜브 | 16:9 | 10-15s | Veo 3 · Sora 2 + TV spot |
| 카카오 채널 | 9:16 또는 1:1 | 5-10s | Kling 2.5 Turbo + UGC |
| 트위터·X | 16:9 | 5-10s | Veo 3 · Kling 3.0 |
| 광고 LP 임베드 | 16:9 | 8-12s | Cinema Studio 3.5 + TV spot |

## 결과 톤 변경 — 모델 교체 가이드

같은 프롬프트·이미지로 톤이 다르면:

| 현재 결과 | 원하는 변화 | 다음 모델 |
|---|---|---|
| 너무 평면적 | 더 시네마틱 | Cinema Studio 3.5 |
| 인물 표정 어색 | 자연스러운 표정 | Kling 3.0 |
| 너무 느림 | 빠른 모션 | Seedance Pro + Hyper motion |
| 톤이 너무 정형적 | 실험적 | Wan 2.5 + Wild Card |
| 광고 톤 부족 | 광고 같은 그레이딩 | Google Veo 3 + TV spot |

## 호출 예시

```javascript
// 기본 (text-to-video)
mcp__higgsfield__generate_video({
  model: "veo_3",
  prompt: "A luxury watch on dark velvet, slow rotation, warm light",
  aspect_ratio: "16:9",
  duration_seconds: 8,
  quality: "high",
  preset: "TV spot"
})

// Image-to-video
mcp__higgsfield__generate_video({
  model: "seedance_pro",
  image_url: "https://...",
  prompt: "Slow zoom in, revealing the product detail",
  aspect_ratio: "16:9",
  duration_seconds: 8,
  preset: "Product review"
})

// 캐릭터 시리즈
mcp__higgsfield__generate_video({
  model: "kling_avatars_2_0",
  prompt: "Mascot jumping with joy",
  aspect_ratio: "1:1",
  duration_seconds: 5
})
```

## 주의

- 모델·프리셋·식별자는 Higgsfield 업데이트에 따라 변할 수 있음
- 정확한 최신 식별자는 [공식 페이지](https://higgsfield.ai/mcp)에서 확인
- 커뮤니티 MCP 구현체에는 공식 외 추가 도구(예: DOP)가 있을 수 있지만, 본 가이드는 **공식 발표 모델·프리셋**만 다룹니다

## 출처

- [higgsfield.ai 공식 사이트](https://higgsfield.ai) — 영상 모델 11종
- [higgsfield.ai/skills](https://higgsfield.ai/skills) — 비디오 프리셋 6종
- [higgsfield.ai/mcp](https://higgsfield.ai/mcp) — MCP 통합 정보
