# GPT-image-2 — 6-Block Prompt Structure

OpenAI Cookbook이 권장하는 6개의 building block. 각 block은 한 절(clause) 단위이며, 자연스러운 영문 단락 1개로 이어 씁니다. 키워드 나열형은 GPT-image-2가 정확도를 잃습니다.

## 1. Subject

**무엇을 그릴 것인가** — 한 문장 안에 형태·재질·고유 특징을 압축.

예:
- "A matte black ceramic coffee mug with a subtle ridge texture"
- "A 30-year-old Korean woman wearing a beige trench coat and small gold earrings"
- "A hand-drawn watercolor illustration of a sleeping fox curled in autumn leaves"

체크리스트:
- [ ] 색·재질·형태 형용사 ≥ 2개
- [ ] 분류 가능한 명사 (mug · woman · fox 등) 1개
- [ ] 모호한 단어 회피 (예: "thing", "object", "item")

## 2. Action

**무엇을 하고 있는가** — 정적 장면이면 위치·배치 동사 사용 ("sitting on", "leaning against", "floating above").

예:
- "sitting on a wet slate countertop next to a folded linen napkin"
- "reading a leather-bound notebook with a fountain pen resting on the spine"
- "curled in a tight crescent shape, tail brushing the paws"

체크리스트:
- [ ] 동사 1개
- [ ] 인접 소품·상호작용 ≥ 1개

## 3. Scene

**어디에 있는가 + 시간·공기감** — 장소 + 시간대 + 분위기.

예:
- "in a minimalist Scandinavian kitchen at sunrise"
- "inside a corner seat of a brick-walled Seoul cafe in late afternoon"
- "on a forest floor scattered with red and gold maple leaves, foggy autumn morning"

체크리스트:
- [ ] 장소 (room · street · forest 등)
- [ ] 시간대 (sunrise · golden hour · late afternoon 등)
- [ ] 공기감 (foggy · crisp · humid 등)

## 4. Composition

**카메라가 어떻게 보는가** — 앵글 + 렌즈 + 심도.

예:
- "three-quarter angle, 50mm lens, shallow depth of field"
- "eye-level medium shot, 85mm lens, subject sharp, background blurred"
- "top-down flat lay, 35mm lens, all elements in focus"

체크리스트:
- [ ] 앵글 (eye-level · 3/4 · top-down · low-angle 등)
- [ ] 렌즈 (24mm · 35mm · 50mm · 85mm · 100mm macro 등)
- [ ] 심도 (shallow · deep · medium DOF)

## 5. Lighting

**빛이 어떻게 떨어지는가** — 광원 + 방향 + 톤.

예:
- "soft directional window light, cool morning tone, gentle rim highlight"
- "warm golden hour backlight casting long shadows"
- "three-point studio softbox setup, evenly lit, neutral 5500K"

체크리스트:
- [ ] 광원 (window · sun · softbox · neon · candle 등)
- [ ] 방향 (side · back · front · top)
- [ ] 톤 (warm · cool · neutral · golden 등)

## 6. Style & Text Constraints

**어떤 시각 언어인가 + 화면 내 글자**

예:
- "editorial product photography, natural film grain"
- "anime studio cel-shading, thick line art, flat colors"
- "muted Scandinavian palette, matte finish, no glossy highlights"

이미지 내 텍스트가 있을 때:
- `The mug has "MONDAY" printed in thin uppercase sans-serif on the side, perfectly legible. Verbatim — no extra characters, no substitutions.`
- 한글 텍스트도 동일하게 따옴표 + 폰트 + 위치 + verbatim 지시.

체크리스트:
- [ ] 매체·장르 (editorial · cinematic · anime · 3D render 등)
- [ ] 마감 형용사 (matte · glossy · film grain · clean digital)
- [ ] 텍스트는 따옴표 + verbatim 지시 의무

## 완성 단락 예시

```
A matte black ceramic coffee mug with a subtle ridge texture,
sitting on a wet slate countertop next to a folded linen napkin,
in a minimalist Scandinavian kitchen at sunrise, three-quarter
angle, 50mm lens, shallow depth of field, soft directional
window light, cool morning tone, gentle rim highlight, editorial
product photography, natural film grain. The mug has "MONDAY"
printed in thin uppercase sans-serif on the side, perfectly
legible. Verbatim — no extra characters, no substitutions.
```

## 출처

- [OpenAI Cookbook — image-gen-models-prompting-guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [i-scoop — Prompting gpt-image-2 like a pro](https://www.i-scoop.eu/prompting-gpt-image-2-like-a-pro-guide/)
