# prompts.md — 설명 영상 프롬프트 템플릿

> `media-higgsfield-explainer` | 스타일 키·클립·내레이션 템플릿.
> **1~3단계 진입 전에 읽는다.**

**Evidence tier:** 2차 (Higgsfield 공식 스킬 `higgsfield-video-explainer` v0.12.0, MIT — `references/prompts.md` 기반)

---

## 0. 언어 규칙

이미지·영상 프롬프트는 **전부 영어로** 쓴다. 내레이션만 사용자가 고른 언어로 쓴다. 아래 템플릿을 한국어로 번역해 쓰지 않는다 — 모델이 영어 프롬프트에 맞춰져 있다.

영상이 일관되게 보이는 이유는 두 가지뿐이다: **모든 클립에 붙는 하나의 스타일 키 이미지**, 그리고 **모든 클립 프롬프트에 똑같이 들어가는 하나의 STYLE 서술**. 둘 중 하나라도 흔들리면 스타일이 무너진다.

---

## 1. STYLE 서술

렌더 방식·팔레트·선의 성격·마감을 한 번 정하고, 반드시 아래 문구로 끝낸다.

```text
non-photorealistic, illustrated, not a photo, no live-action, no realism
```

예시:

- `flat 2D vector animation, bold clean outlines, solid vibrant flat fills, no shading, no gradients`
- `hand-inked black marker on off-white paper, solid jet-black fills, thin white scratch highlights, marker grain, strictly monochrome`
- `strict monochrome minimalism, black silhouettes on white void, high contrast, lots of negative space`
- `hand-painted storybook gouache, soft textures, warm muted palette, visible brush strokes`

---

## 2. 스타일 키 이미지

### 추상 스와치 (무인물 모드 기본)

```text
Pure {STYLE} STYLE REFERENCE plate. No characters, no faces, no people, no objects, no scene, no letters—an abstract style swatch only. A balanced arrangement that demonstrates the rendering grammar clearly: {line quality}, {fill behavior}, {highlight/edge behavior}, {texture/grain}. {palette constraint, with hex if strict}. High contrast, clean background, generous negative space. Flat, raw, hand-illustrated, non-photorealistic. No text, no logos, no watermark.
```

### 마스코트 키 (마스코트 모드)

```text
{STYLE}. Full-body character: {HOST}—a {species/persona} narrator, expressive, clear readable silhouette, looking at camera, centered, simple background. Recurring-character design. No text, no logos, no watermark.
```

### 참조 이미지를 받은 경우

아래 문구를 **그대로 앞에 붙이고** 스와치/마스코트 지시를 잇는다.

```text
Make an Animated Explainer. Take only the visual render style and color grading of the input image(s); mix the styles if there is more than one image. Never use the characters, inscriptions, etc. from the input image(s) unless the instructions below ask you to. Use only the render style, and follow the user's instructions below:
{raw user query / scene}
```

참조 이미지는 **스타일 기증자**일 뿐이다. 거기 있는 인물·글자·로고·사물을 가져오지 않는다.

---

## 3. 클립 블록 템플릿

```text
Block N
STYLE REFERENCE: Match the attached reference image EXACTLY. Replicate its look precisely: {STYLE tokens}. Every element below rendered in that identical style.
SCENE: {scene and one clear action matching Block N narration}.
MOTION: {camera move and animation behavior—slow push-in, drift, scale shock, hard contrast cut}.
AUDIO: {ambient SFX or music only—NO voice, dialogue, or narration}.
NEGATIVE: color drift, photorealism, 3D render, lip-sync, captions, on-screen text, logos, watermark{, plus style-specific bans}.
```

규칙:

- STYLE 토큰은 **모든 블록에 똑같이** 복사한다.
- 클립 오디오는 화면 안의 소리(디제틱)만. 등장인물은 말하지 않고 립싱크하지 않는다.
- 마스코트 모드: 1번 블록은 **입을 다문 채 제스처로** 인사, 마지막 블록은 손 흔들어 마무리, 중간 블록은 필요할 때만 같은 디자인으로 등장.
- 무인물 모드: 모든 블록이 해당 내레이션 비트의 양식화된 장면.
- 블록당 명확한 동작 **하나**.

예시:

```text
Block 4
STYLE REFERENCE: Match the attached reference image EXACTLY. Replicate its look precisely: strict monochrome minimalism, solid black silhouettes on an absolute white void, high contrast, lots of negative space, matte, non-photorealistic, illustrated, not a photo, no live-action, no realism. Every element below rendered in that identical style.
SCENE: A lone black silhouette slowly dissolves at the edges, crumbling into fine drifting sand that scatters into the white emptiness.
MOTION: Very slow push-in; the figure erodes grain by grain and particles drift sideways.
AUDIO: Low sustained drone and a soft whisper of falling sand—no voice.
NEGATIVE: color, gray midtones, photorealism, 3D render, lip-sync, captions, on-screen text, logos, watermark.
```

---

## 4. 내레이션 블록

클립 하나당 평문 한 줄. 약 8~9초, 보통 20~24단어. 모든 테이크를 9.5초 아래로 유지한다.

```text
Block 1
For four and a half thousand years, the pyramids of Egypt have stood against the desert, silent and immense.
Block 2
They rose along the Nile, the river that fed a civilization ruled by pharaohs believed to be living gods.
```

규칙:

- 타임코드·감정 지시·괄호 지문·무대 지시를 넣지 않는다.
- 숫자는 풀어 쓴다.
- 어휘와 구체적 디테일로 톤을 만든다.
- "이 영상에서는" 류의 표현을 쓰지 않는다.
- 주제형: 훅 → 블록마다 이해를 쌓고 → 마지막에 결론.
- 개인 이야기형: 사용자(또는 그 화자)를 주인공으로 유지하고 사실을 지어내지 않는다.

한국어 내레이션 주의: 20~24단어 기준은 영어 기준이다. 한국어는 어절 수가 다르므로 **단어 수가 아니라 낭독 시간(8~9초)** 을 기준으로 맞춘다.

---

## 5. 안티패턴

- **템플릿을 한국어로 번역해 프롬프트로 사용** — 이미지·영상 프롬프트는 영어다.
- **블록마다 STYLE 서술을 조금씩 바꿈** — 스타일이 흔들린다. 복사-붙여넣기가 정답이다.
- **클립 프롬프트에 대사·내레이션 삽입** — 목소리는 오디오 트랙에서만 온다.
- **참조 이미지의 인물·로고를 그대로 사용** — 스타일만 가져온다.
- **한 블록에 동작 여러 개** — 10초에 담기지 않는다.
- **클립 프롬프트에 자막 요청** — 자막은 조립 단계 옵션이다.
