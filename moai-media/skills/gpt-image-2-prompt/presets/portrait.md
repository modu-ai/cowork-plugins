# Preset: 인물·캐릭터 (Portrait)

인물 포트레이트, 페르소나 일러스트, 광고 모델 컷, 라이프스타일 인물 사진.

## Round 2 슬롯 정의

### Q1 — 인물·연령대

| 옵션 | 예시 매핑 |
|---|---|
| 30대 한국 여성 (권장) | "a 30-year-old Korean woman with a clean center-parted bob, subtle makeup" |
| 20대 한국 남성 | "a 20-something Korean man with a soft fringe, light stubble" |
| 40대 직장인 (성별 선택) | "a 40-year-old professional in business casual" |
| 어린이·청소년 | "a 10-year-old child with a curious expression" |

(Other로 구체 연령·국적·성별 자유 입력 가능)

### Q2 — 의상·소품

| 옵션 | 예시 매핑 |
|---|---|
| 베이지 트렌치 (권장) | "wearing a beige trench coat over a white cotton tee, small gold earrings" |
| 미니멀 니트 | "wearing a chunky cream wool sweater, pearl studs" |
| 비즈니스 캐주얼 | "wearing a charcoal blazer over a light blue oxford shirt, no tie" |
| 액티브웨어 | "wearing a black cropped tank top and high-waist leggings" |

### Q3 — 표정·동작

| 옵션 | 예시 매핑 |
|---|---|
| 차분히 노트북 응시 (권장) | "looking down at a laptop with a quiet focused expression" |
| 밝은 미소 카메라 응시 | "smiling softly at the camera, eyes slightly squinted" |
| 옆모습 사색 | "in profile view, gaze drifting out of frame, contemplative" |
| 동작 중 (걷기·앉기) | "mid-stride walking toward the camera, natural arm swing" |

### Q4 — 배경·조명

| 옵션 | 예시 매핑 |
|---|---|
| 브릭월 서울 카페 (권장) | "in a corner seat of a brick-walled Seoul cafe, late afternoon, warm window light" |
| 미니멀 스튜디오 | "seamless gray studio backdrop, three-point softbox, neutral 5500K" |
| 도시 거리 (한강) | "Han River walkway, golden hour, soft backlight, bokeh skyline" |
| 자연·숲 | "forest path with dappled sunlight, soft side fill" |

## Composition 보너스 슬롯 (Q3·Q4와 함께 자동 결정)

- 앵글: eye-level (기본) · low-angle · over-the-shoulder · three-quarter
- 렌즈: 35mm (환경 포함) · 50mm (일반) · 85mm (얼굴 강조)
- 심도: shallow (인물 강조) · medium · deep (배경 활용)

## 모델별 어조 변환 가이드

### GPT-image-2 (자연어 단락)
```
<Q1>, <Q2>, <Q3>, in <Q4>, eye-level medium shot, 85mm lens,
shallow depth of field, soft directional light, editorial
portrait photography, natural film grain.
```

### Gemini 3 Pro Image (5-component)
```
<Q1+Q2> <Q3> in <Q4>. Eye-level medium shot, 85mm lens, shallow
depth of field. Soft directional light. Editorial portrait
photography.
```

### Midjourney v8.1 (키워드+파라미터)
```
<Q1>, <Q2 키워드>, <Q3 키워드>, <Q4 키워드>, 85mm portrait, shallow
DOF, natural light, editorial photography, film grain
--ar [Round 3] --style raw --hd --q 4 --s 200
```

## 초상권 주의

- 실존 인물·연예인 모방은 정책 위반 가능. 가상 페르소나로 한정.
- Midjourney `--oref` 사용 시 본인 또는 권한 있는 인물 사진만.
- GPT-image-2는 정책상 identity replication을 제한적으로 처리.

## 자주 쓰이는 보조 키워드

분위기:
- editorial · candid · documentary · cinematic · lifestyle

조명 어조:
- soft window · golden hour · blue hour · studio neutral · moody

색감:
- muted · warm · cool · desaturated · vibrant
