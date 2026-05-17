# Preset: 제품샷 (Product Shot)

커머스 상품, 패키지 컷, 보석·시계 클로즈업, 식음료 컷 등 단일 또는 그룹 제품 사진.

## Round 2 슬롯 정의

`AskUserQuestion` 4 라운드. 각 질문에 4 옵션 + Other.

### Q1 — 제품·소재

| 옵션 | 예시 매핑 |
|---|---|
| 매트 블랙 (권장) | "matte black ceramic with subtle ridge texture" |
| 무광 우드 | "natural walnut wood, hand-rubbed finish" |
| 폴리시드 메탈 | "polished stainless steel, mirror-like reflection" |
| 유광 세라믹 | "glossy white ceramic with soft sheen" |

### Q2 — 배경·표면

| 옵션 | 예시 매핑 |
|---|---|
| 젖은 슬레이트 (권장) | "wet slate countertop, subtle water droplets" |
| 베이지 리넨 | "folded beige linen fabric, soft wrinkles" |
| 화이트 스튜디오 | "seamless white studio backdrop, infinity curve" |
| 우드 트레이 | "raw oak wood tray, visible grain" |

### Q3 — 조명·시간대

| 옵션 | 예시 매핑 |
|---|---|
| 창문 사이드 일출 (권장) | "soft directional window light at sunrise, cool morning tone" |
| 스튜디오 소프트박스 | "three-point softbox setup, evenly lit, neutral 5500K" |
| 골든아워 백라이트 | "warm golden hour backlight, long shadows" |
| 드라마틱 키아로스쿠로 | "high-contrast chiaroscuro lighting, single hard light source" |

### Q4 — 카메라 앵글·렌즈

| 옵션 | 예시 매핑 |
|---|---|
| 3/4 앵글 50mm (권장) | "three-quarter angle, 50mm lens, shallow depth of field" |
| 탑다운 35mm 플랫레이 | "top-down flat lay, 35mm lens, all elements in focus" |
| 매크로 100mm | "macro shot, 100mm lens, extremely shallow DOF" |
| 로우앵글 24mm | "low-angle hero shot, 24mm wide lens, dramatic perspective" |

## Composition 보너스 슬롯 (선택)

- 화면 내 텍스트 (Round 3에서 처리)
- 강조 컬러 액센트 (Round 4 추가 옵션)
- 그림자 강도 (soft · medium · hard)

## 모델별 어조 변환 가이드

### GPT-image-2 (자연어 단락)
```
A <Q1> <product>, <Q4 동작>, <Q2 배경>, in a <scene>,
<Q4 composition>, <Q3 lighting>, editorial product
photography, natural film grain. [Round 3 텍스트]
```

### Gemini 3 Pro Image (5-component 영문 문장)
```
<Q1+product> resting in <Q2 background>. <Q4 composition>.
<Q3 lighting>. Editorial product photography. [Round 3 텍스트]
```

### Midjourney v8.1 (키워드+파라미터)
```
<Q1>, <product>, <Q2>, <Q3>, <Q4 키워드>, editorial product
photography, natural film grain --ar [Round 3] --style raw --hd --q 4 --s 250
```

## 자주 쓰이는 보조 키워드

스타일:
- editorial · commercial · advertising · catalog · lifestyle

매체 어조:
- film grain · natural · clean digital · matte finish · glossy

브랜드 톤:
- Apple-clean · Aesop-warm · Muji-neutral · Glossier-pastel
