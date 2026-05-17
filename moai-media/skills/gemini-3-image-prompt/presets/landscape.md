# Preset: 풍경·환경 (Landscape)

배경 이미지, 공간 사진, 시네마틱 배경, 여행 컷, 자연·도시 풍경.

## Round 2 슬롯 정의

### Q1 — 장소·계절

| 옵션 | 예시 매핑 |
|---|---|
| 가을 단풍 숲 (권장) | "an autumn maple forest, ground covered in red and gold leaves, mist between trunks" |
| 겨울 도시 거리 | "a snow-dusted city street at dawn, glowing storefront windows, soft footprints" |
| 여름 해변 | "a tropical beach at midday, turquoise water, fine white sand, scattered palm fronds" |
| 봄 한강 산책로 | "the Han River walkway in spring, cherry blossom trees in full bloom, soft pink petals on the path" |

### Q2 — 분위기·시간대

| 옵션 | 예시 매핑 |
|---|---|
| 골든아워 일출 (권장) | "golden hour at sunrise, warm orange light, long shadows, soft mist" |
| 블루아워 일몰 직후 | "blue hour just after sunset, cool deep blue sky, lit windows providing warmth" |
| 한낮 맑음 | "midday clear blue sky, sharp shadows, vibrant saturated colors" |
| 흐림·안개 | "overcast and foggy, diffused light, muted palette, atmospheric depth" |

### Q3 — 시점·구도

| 옵션 | 예시 매핑 |
|---|---|
| 와이드 파노라마 (권장) | "wide panoramic composition, horizon at the lower third, vast sky" |
| 탑다운 항공샷 | "top-down aerial view, drone perspective, all elements in geometric pattern" |
| 일점투시 길 | "single-point perspective down a path or street, vanishing point centered" |
| 클로즈업 디테일 | "close-up detail of a natural element (leaf, stone, water surface), shallow DOF" |

### Q4 — 강조 요소

| 옵션 | 예시 매핑 |
|---|---|
| 인물 실루엣 (권장) | "a small silhouetted figure walking through the scene, providing scale" |
| 빛줄기·God Rays | "visible god rays streaming through trees or clouds, atmospheric haze" |
| 반사·물 | "still water surface reflecting the scene perfectly, doubling the composition" |
| 단독 자연 요소 | "scene without people or man-made elements, pure nature" |

## 모델별 어조 변환 가이드

### GPT-image-2 (자연어 단락)
```
<Q1> <Q2>, <Q3 composition>, <Q4>, 24mm wide-angle lens, deep
depth of field, cinematic landscape photography, natural film
grain.
```

### Gemini 3 Pro Image (5-component)
```
<Q1>. <Q3 composition>. <Q2 lighting/mood>. Cinematic landscape
photography. <Q4>.
```

### Midjourney v8.1 (키워드+파라미터)
```
<Q1 키워드>, <Q2 키워드>, <Q3 키워드>, <Q4 키워드>, 24mm wide-angle,
deep DOF, cinematic landscape --ar [Round 3] --style raw --hd --q 4 --s 300
```

## 화면비 권장

| 화면비 | 추천 시나리오 |
|---|---|
| 16:9 | 시네마틱 와이드, 유튜브 썸네일, 노트북 배경 |
| 21:9 (Gemini만) | 울트라와이드 영화 어조 |
| 9:16 | 모바일 락스크린, 릴스 배경 |
| 1:1 | SNS 정사각 |

## 자주 쓰이는 보조 키워드

대기·날씨:
- mist · fog · haze · clouds · clear · stormy · drizzle

조명 어조:
- volumetric light · god rays · backlight · sidelight · rim light · ambient

스타일 어조:
- cinematic · documentary · National Geographic · Wes Anderson · Studio Ghibli
- 4K nature · landscape masterpiece · award-winning photography
