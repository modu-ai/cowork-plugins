# Gemini 3 Pro Image — 5-Component Prompt Structure

Google AI for Developers 공식 권장 구조. 각 component는 영문 문장 1-2개로 끝나며, **마침표로 구분**합니다. 키워드 콤마 나열은 동작하지만 품질이 떨어집니다. 어조는 **Creative Director가 장면을 지시하는 톤**.

```
[Subject + Adjectives] doing [Action] in [Location/Context].
[Composition/Camera Angle/Lens/Hardware].
[Lighting/Atmosphere].
[Style/Media].
[Specific Constraint/Text]
```

## Component 1 — [Subject + Adjectives] doing [Action] in [Location]

한 문장에 3가지를 압축:
- Subject + 형용사 (재질·색·고유 특징)
- Action (정적이면 위치 동사: resting · sitting · floating)
- Location (장소 + 시간대 + 공기감)

예:
- "A matte black ceramic coffee mug with subtle ridge texture sitting on a wet slate countertop in a minimalist Scandinavian kitchen at sunrise."
- "A 30-year-old Korean woman in a beige trench coat reading a leather notebook in a brick-walled Seoul cafe in the late afternoon."

## Component 2 — Composition / Camera

Gemini는 **하드웨어 지정**을 지원합니다 (Creative Director의 특별한 도구):

| 하드웨어 | 시각적 DNA |
|---|---|
| DSLR 50mm | 깨끗·중성·표준 (기본) |
| Fujifilm X-T5 | 따뜻한 색감, film simulation |
| Sony A7 IV | 모던 미러리스, 자연색 |
| Hasselblad | 미디엄 포맷, 럭셔리·고급 |
| GoPro HERO12 | 광각, 액션·몰입, 약간 distortion |
| Disposable film camera | 거친 입자, nostalgic flash, raw 무드 |
| iPhone 15 Pro | computational photography, 깨끗 디지털 |
| Polaroid SX-70 | 즉석사진 어조, 부드러운 광 |

추가:
- 앵글: eye-level · low-angle · top-down · three-quarter · over-the-shoulder
- 렌즈: 24mm wide · 35mm · 50mm · 85mm · 100mm macro · 200mm telephoto
- 심도: shallow · medium · deep

예:
- "Three-quarter angle, shot on a Fujifilm X-T5 with a 50mm lens, shallow depth of field."
- "Top-down flat lay captured on an iPhone 15 Pro, all elements in focus."

## Component 3 — Lighting / Atmosphere

Google 공식 가이드의 "Direct the scene like a Creative Director" 원칙:
- 스튜디오 setup: "three-point softbox setup, evenly illuminating the product"
- 드라마틱 효과: "Chiaroscuro lighting with harsh, high contrast"
- 자연광: "Golden hour backlighting creating long shadows"
- 인공광: "Neon-lit alleyway, deep magenta and cyan rim light"

예:
- "Soft directional window light at sunrise, cool morning tone, gentle rim highlight."
- "Chiaroscuro lighting with a single hard light source from the left, deep shadows on the right."

## Component 4 — Style / Media

매체·장르를 명시:
- Photography: editorial · commercial · documentary · candid · lifestyle · advertising · catalog
- Illustration: watercolor · vector flat · pen and ink · digital paint · Studio Ghibli-style · Pixar-style
- 3D: octane render · cinema 4D · unreal engine · blender stylized
- Fine art: oil painting · charcoal sketch · Klimt-inspired · Rothko-style

예:
- "Editorial product photography, natural film grain."
- "Hand-drawn watercolor illustration, soft washes, visible paper texture."

## Component 5 — Specific Constraint / Text

이미지 내 텍스트가 있을 때만 작성. 없으면 생략 가능.

예:
- "The mug displays \"MONDAY\" in thin uppercase sans-serif, perfectly legible."
- "A billboard in the background reads \"신선한 시작\" in bold Hangul serif."

text-first 패턴 (텍스트가 길거나 복잡할 때):
- 먼저 모델과 대화로 카피를 다듬는다.
- 확정된 카피를 verbatim으로 넣는다.

## 완성 단락 예시

```
A matte black ceramic coffee mug with subtle ridge texture
sitting on a wet slate countertop in a minimalist Scandinavian
kitchen at sunrise. Three-quarter angle, shot on a Fujifilm X-T5
with a 50mm lens, shallow depth of field. Soft directional
window light, cool morning tone, gentle rim highlight. Editorial
product photography, natural film grain. The mug displays
"MONDAY" in thin uppercase sans-serif on the side, perfectly
legible.
```

## 권장하지 않는 어조

```
matte black mug, MONDAY text, slate, sunrise, 50mm
```

위는 키워드 나열형 (MJ 어조). Gemini는 동작하지만 reasoning이 제대로 안 됨. 반드시 문장형으로.

## 출처

- [Google AI for Developers — Gemini 3 Pro Image Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Google Cloud Blog — Ultimate Prompting Guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Atlabs AI — Ultimate Nano Banana Pro Prompting Guide 2026](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
