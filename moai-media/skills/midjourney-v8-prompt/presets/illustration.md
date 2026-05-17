# Preset: 일러스트·아트 (Illustration)

카드뉴스 일러스트, 책 표지, 컨셉 아트, 브랜드 캐릭터, 인포그래픽용 일러스트.

## Round 2 슬롯 정의

### Q1 — 주제·소재

| 옵션 | 예시 매핑 |
|---|---|
| 동물·자연 (권장) | "a sleeping fox curled in autumn leaves, bushy tail wrapped around its paws" |
| 인물·캐릭터 | "a young illustrator at a wooden desk, surrounded by books and a single lamp" |
| 사물·정물 | "a still life of a coffee cup, an open notebook, and a brass fountain pen" |
| 추상·상징 | "an abstract composition of geometric shapes representing growth and renewal" |

### Q2 — 그림체·매체

| 옵션 | 예시 매핑 |
|---|---|
| 수채화 (권장) | "hand-drawn watercolor illustration, soft washes, visible paper texture" |
| 플랫 디지털 | "flat vector illustration, clean shapes, minimal shading, modern editorial style" |
| 펜&잉크 | "pen and ink line drawing, crosshatched shading, vintage book plate aesthetic" |
| 디지털 페인팅 | "digital painting, painterly brushstrokes, Studio Ghibli-inspired warm tones" |

### Q3 — 색감·무드

| 옵션 | 예시 매핑 |
|---|---|
| 가을 따뜻 (권장) | "warm autumn palette — burnt orange, mustard yellow, deep red, dusty olive" |
| 파스텔 부드러움 | "soft pastel palette — blush pink, mint, lavender, cream" |
| 모노톤 | "monochromatic grayscale, ink black on cream paper" |
| 비비드 컨트라스트 | "high-contrast vivid palette — electric blue, magenta, lime green" |

### Q4 — 구도·시점

| 옵션 | 예시 매핑 |
|---|---|
| 정면 클로즈업 (권장) | "centered close-up composition, subject filling 70% of the frame" |
| 와이드 환경 | "wide environmental shot, subject small within a detailed scene" |
| 탑다운 플랫 | "top-down flat composition, isometric or perfectly orthogonal" |
| 사선·동적 | "dynamic diagonal composition, off-center subject, sense of motion" |

## 모델별 어조 변환 가이드

### GPT-image-2 (자연어 단락)
```
<Q2> of <Q1>, <Q4 composition>, <Q3 palette>, soft natural
lighting integrated into the illustration style, no photographic
elements.
```

### Gemini 3 Pro Image (5-component)
```
<Q1> rendered in <Q2 style>. <Q4 composition>. <Q3 palette>.
Illustrated, not photographic.
```

### Midjourney v8.1 (키워드+파라미터)
```
<Q2 매체 키워드>, <Q1 키워드>, <Q4 키워드>, <Q3 팔레트 키워드>,
illustration not photograph --ar [Round 3] --style raw --s 400
```

(MJ는 일러스트 스타일에서 `--style raw`를 빼고 default style을 쓰는 게 더 자유로운 결과를 내기도 합니다. 사용자 선택.)

## 자주 쓰이는 보조 키워드

매체별 어조:
- watercolor: paper texture · wet-on-wet · soft edges · visible brushstrokes
- vector: clean shapes · solid fills · minimal gradients · editorial flat
- ink: crosshatch · stippling · vintage plate · woodcut feel
- digital paint: painterly · Studio Ghibli · Pixar · Klimt-inspired

분위기:
- whimsical · serene · melancholic · dreamy · bold · playful

## 브랜드 캐릭터 일관성

여러 장에 같은 캐릭터를 등장시킬 때:

- GPT-image-2: 첫 장을 reference로 업로드 후 편집 모드 (Image 1: character reference) 사용. Preserve에 "character's face, body proportions, outfit, color scheme" 명시.
- Gemini 3 Pro Image: reference 이미지 첨부 가능 (최대 14장). "Maintain the exact character design from the reference."
- Midjourney v8.1: `--oref <URL>` + `--cw 30~60` (얼굴 위주, 의상까지 따라가려면 `--cw 100`).
