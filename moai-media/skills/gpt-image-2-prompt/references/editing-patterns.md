# GPT-image-2 — Edit 2-Column Logic

기존 이미지를 편집할 때 GPT-image-2는 **Change / Preserve / Constraints** 3-블록 구조를 권장합니다. 무엇을 잠그고 무엇을 풀지를 명시하지 않으면 얼굴·로고·텍스트·구도가 의도와 다르게 드리프트합니다.

## 기본 템플릿

```
Change: <바꿀 요소 1~3개를 명확히>
Preserve: <face, identity, pose, lighting, framing, background, geometry, text, layout 중 잠글 항목>
Constraints: <금지 사항>
```

세 줄을 **반드시** 단락 안에 명시. 자연어 흐름으로 풀어도 좋지만, 다음 키워드는 그대로 유지하면 model이 더 잘 따릅니다: `Change:` `Preserve:` `Constraints:`.

## Change — 변경할 요소

원칙:
- 한 번에 1-3개 변경. 4개 이상은 별도 호출로 분할.
- 변경 후 상태를 구체적으로 묘사 (단순 "make it red" 보다 "change mug body color to deep crimson (#8B0000), keep handle matte black").
- 텍스트 변경 시 새 텍스트를 따옴표로 verbatim 지정.

예:
- "Change: replace the white linen napkin with a striped beige-and-charcoal napkin. Keep the fold style identical."
- "Change: add a small steam wisp rising from the mug, soft and translucent, occupying the upper third."

## Preserve — 잠글 요소

GPT-image-2가 흔히 드리프트하는 카테고리:

| 카테고리 | Preserve 키워드 예 |
|---|---|
| 얼굴 | "face, identity, eye color, hairstyle" |
| 자세 | "pose, hand position, body angle" |
| 카메라 | "framing, camera angle, focal length" |
| 조명 | "lighting direction, color temperature, shadow placement" |
| 배경 | "background, all background elements, depth of field" |
| 텍스트 | "all existing text, font, position, color" |
| 기하 | "object dimensions, proportions, geometry" |

예:
- "Preserve: face, identity, pose, framing, lighting direction, all background elements, the mug shape and proportions."
- "Preserve: the model's hairstyle, expression, and outfit. The 'MONDAY' text on the mug stays exactly as is."

## Constraints — 금지

자주 쓰이는 금지 절:

- `no extra objects` — 새 소품 추가 금지
- `no redesign` — 전체 재디자인 금지 (지정한 변경만)
- `no logo drift` — 로고·브랜드 마크 변형 금지
- `no watermark` — 워터마크 추가 금지
- `no text substitution` — 텍스트 다른 문자로 대체 금지
- `no style change` — 스타일·매체 변경 금지

예:
- "Constraints: no extra objects, no redesign of the kitchen, no logo drift on the mug, no watermark."

## 완성 단락 예시

### 예 1 — 머그 색만 변경

```
Edit the existing image with these rules.

Change: change the mug body color from matte black to deep
crimson (#8B0000). Keep the matte finish and the subtle ridge
texture intact.

Preserve: face of the napkin fold, the slate countertop texture
and wetness, the window light direction and tone, the
three-quarter camera angle, the depth of field, the "MONDAY"
text in thin uppercase sans-serif on the mug side.

Constraints: no extra objects, no redesign of the kitchen, no
logo drift, no watermark, no text substitution.
```

### 예 2 — 인물 의상 교체 (멀티 레퍼런스)

```
Image 1: base portrait of a woman in a beige trench coat.
Image 2: reference jacket — black leather biker jacket, silver
zippers.

Edit Image 1 with these rules.

Change: replace the beige trench coat with the jacket shown in
Image 2 (black leather, silver zippers). Match the jacket fit
to the model's pose naturally.

Preserve: face, identity, hairstyle, makeup, gold earrings, the
exact pose and hand position, the eye-level camera angle, the
85mm shallow depth of field, the soft sidelight, the brick-walled
Seoul cafe background.

Constraints: no other clothing changes, no accessory drift, no
background modification, no watermark.
```

## 참조 이미지 라벨링

최대 16개. 항상 "Image N: <역할>"로 라벨하고 프롬프트에서 라벨로 호출합니다.

```
Image 1: base scene to preserve.
Image 2: jacket reference.
Image 3: boots reference.
```

## 자주 발생하는 실패와 대응

| 증상 | 원인 | 대응 |
|---|---|---|
| 얼굴이 약간 바뀜 | Preserve에 face 누락 | "Preserve: face, identity, eye color, hairstyle" 명시 |
| 텍스트가 사라짐 | Preserve에 text 누락 | 텍스트 verbatim + position 재명시 |
| 새 소품이 등장 | Constraints에 "no extra objects" 누락 | 추가 |
| 로고가 변형됨 | Constraints에 "no logo drift" 누락 | 추가 + Preserve에 brand 명시 |

## 출처

- [OpenAI Cookbook — image-gen-models-prompting-guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [Atlabs AI — The Ultimate GPT Image 2 Prompting Guide 2026](https://www.atlabs.ai/blog/the-ultimate-gpt-image-2-prompting-guide-how-to-use-openai%E2%80%99s-best-image-model-2026)
