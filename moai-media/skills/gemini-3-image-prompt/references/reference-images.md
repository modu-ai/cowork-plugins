# Gemini 3 Pro Image — Reference Image Strategy (Up to 14)

Gemini 3 Pro Image는 한 프롬프트에 **최대 14개의 reference 이미지**를 첨부할 수 있습니다. Few-Shot Design 패러다임으로, 브랜드 일관성·캐릭터 일관성·스타일 전이에 강력합니다.

## 핵심 원칙

**적을수록 좋다.** 14개 슬롯이 있다고 모두 채우면 모델이 어떤 reference를 우선 따라야 할지 혼란스러워합니다. 권장:

- 단순 스타일 전이: 1-2개
- 브랜드 캐릭터 + 스타일: 3-4개
- 복잡 캠페인 (캐릭터 + 환경 + 색 팔레트 + 텍스처): 5-8개
- 14개 가까이 사용: 광고 시리즈처럼 매우 복잡한 case에서만

## 슬롯 전략 (권장 순서)

| 슬롯 | 역할 | 예시 |
|---|---|---|
| 1번째 (필수) | **메인 스타일·미학** | 전체 그림체·매체·톤을 결정하는 이미지 |
| 2번째 | **캐릭터·핵심 피사체** | 일관성을 유지할 인물·캐릭터·제품 |
| 3번째 | **구도·레이아웃** | 카메라 앵글·여백·구성 영감 |
| 4-5번째 | **색 팔레트·무드** | 컬러 가이드 보드 |
| 6-8번째 | **부수적 스타일** | 텍스처·디테일·소품 |
| 9-14번째 | **추가 디테일** | 매우 specific한 부분만 (드물게 사용) |

## 프롬프트에서 reference 참조 방법

Gemini는 reference 이미지를 "Image 1", "Image 2" 등의 라벨로 자동 인식. 프롬프트에서 명시적으로 참조하면 정확도 향상:

```
Using the attached reference images:
- Image 1: main style reference — soft watercolor illustration aesthetic.
- Image 2: character reference — preserve the woman's face, hair, and outfit.
- Image 3: composition reference — three-quarter angle with subject off-center.

Generate <component 1>. <component 2>. <component 3>. <component 4>.
```

## 자주 쓰이는 패턴

### 패턴 A — 브랜드 캐릭터 일관성

```
Image 1: brand mascot reference (front view).
Image 2: brand color palette swatches.

Generate the same mascot in a new scene: <subject doing action in
location>. <composition>. <lighting>. <style>. Maintain the
mascot's exact face, body proportions, and color scheme from
Image 1. Use only the colors shown in Image 2.
```

### 패턴 B — 제품 + 스타일 전이

```
Image 1: product reference — sneaker side view, all logos and
colorways visible.
Image 2: lifestyle scene reference — wet city street at night,
neon reflections.

Generate the sneaker from Image 1 placed in a similar wet city
street setting as Image 2. <composition>. <lighting matching
Image 2>. Cinematic product photography. Maintain exact logo
placement and colorway from Image 1.
```

### 패턴 C — 시리즈 일관성 (광고 캠페인 5장)

```
Image 1: master style reference (mood + palette + lighting).
Image 2: model reference (face + outfit).
Image 3: typography reference (Hangul serif headline style).
Image 4: brand element reference (logo + tagline placement).

Generate scene 3 of 5 in the campaign series: <subject doing
action in location>. Match Image 1 style. Use the same model
as Image 2. Place a Hangul headline reading "<text>" in the
typography style of Image 3. Position the logo from Image 4 in
the top-right corner.
```

## 캐릭터·인물 일관성 팁

- 같은 인물을 여러 장에 등장시킬 때 첫 장의 frontal portrait를 reference 1번 슬롯에 고정.
- 프롬프트에 "preserve the face, hair, expression, and outfit from Image 1" 명시.
- 의상이 다를 경우 "same person, different outfit: <new outfit>" 형식.
- Gemini는 GPT-image-2의 Preserve list 어조를 그대로 이해합니다.

## 한계와 회피 방법

| 한계 | 회피 |
|---|---|
| Reference 14개 채우면 우선순위 혼란 | 핵심 3-5개로 제한 |
| 작은 얼굴은 detail loss 가능 | reference에 얼굴 클로즈업 추가 |
| 마스킹 편집 가끔 unnatural | 단순 교체·합성으로 분할 |
| 낮↔밤 변환 artifact | 단계적 변환 (낮 → 황혼 → 밤) |
| 다중 이미지 블렌딩 disjointed | reference 슬롯 명시적 분리 |

## 출처

- [Google AI for Developers — Gemini 3 Pro Image Preview (Reference Images)](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Google Cloud Blog — Ultimate Prompting Guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Atlabs AI — Ultimate Nano Banana Pro Prompting Guide](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
