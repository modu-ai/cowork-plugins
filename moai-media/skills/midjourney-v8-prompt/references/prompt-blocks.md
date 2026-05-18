# Midjourney v8.1 — Keyword + Parameter Structure

Midjourney는 키워드 콤마 + `--파라미터` 구조에 최적화. 자연어 문장도 동작하지만 키워드형이 더 일관된 결과를 냅니다.

## 표준 구조

```
[subject], [scene/setting], [composition], [lighting], [style/medium]
--ar W:H [--style raw] [--hd] [--q 4] [--s 0~1000]
[--sref CODE_or_URL --sw 0~1000 --sv 7]
[--oref URL --cw 0~100]
[--p PROFILE_ID]
[--no NEGATIVE_LIST]
[--c 0~100]
```

## Block 1 — Subject

가장 먼저 등장. 핵심 명사 + 형용사 2-3개.

예:
- `matte black ceramic coffee mug, ridge texture, MONDAY text`
- `30-year-old Korean woman, beige trench coat, gold earrings`
- `sleeping fox, autumn leaves, bushy tail`

## Block 2 — Scene / Setting

장소 + 시간대 + 공기감.

예:
- `wet slate countertop, Scandinavian kitchen, sunrise`
- `brick-walled Seoul cafe, late afternoon`
- `autumn maple forest, misty morning`

## Block 3 — Composition

앵글 + 렌즈 + 심도. MJ는 짧은 키워드를 잘 따름.

예:
- `three-quarter angle, 50mm, shallow DOF`
- `eye-level, 85mm portrait, blurred background`
- `top-down flat lay, 35mm, deep focus`

## Block 4 — Lighting

광원 + 방향 + 톤.

예:
- `soft window light, sunrise, cool tones, rim highlight`
- `chiaroscuro, single hard light from left, deep shadows`
- `golden hour backlight, warm tones, long shadows`

## Block 5 — Style / Medium

매체·장르·photographer reference.

예:
- `editorial product photography, film grain`
- `Annie Leibovitz portrait, cinematic`
- `Studio Ghibli illustration, hand-painted backgrounds`
- `anime cel-shading, thick lines, flat colors`

## 파라미터 순서 (관례)

```
--ar [필수]
--style raw [선택, photographic용]
--hd [선택, 2K 필요 시, 4x cost]
--q 4 [선택, coherence 필요 시, 4x cost]
--s [선택, default 100, 0~1000]
--sref [선택, 4x cost, --sw·--sv 동반]
--oref [선택, 2x cost, --cw 동반]
--p [선택, profile 사용 시]
--no [선택, 제외 요소]
--c [선택, 시안 다양성]
```

## 완성 프롬프트 예시

### 예 1 — 제품샷 1:1

```
matte black ceramic coffee mug, ridge texture, "MONDAY" text,
wet slate countertop, Scandinavian kitchen, sunrise window
light, three-quarter angle, 50mm, shallow DOF, editorial product
photography, film grain --ar 1:1 --style raw --hd --q 4 --s 250
```

비용: 4x (--hd) × 4x (--q 4) = **16x GPU 시간**

### 예 2 — 인물 9:16 캐릭터 일관성

```
30-year-old Korean woman, beige trench coat, gold earrings,
reading laptop, brick-walled Seoul cafe, late afternoon, warm
window light, eye-level, 85mm portrait, shallow DOF, editorial
candid --ar 9:16 --style raw --oref https://example.com/ref.jpg
--cw 40 --s 200
```

비용: 2x (--oref). `--cw 40`으로 얼굴만 따라가고 의상·배경은 새로.

### 예 3 — 일러스트 + Style Reference

```
watercolor illustration, sleeping fox, autumn leaves, soft
washes, paper texture, warm autumn palette, centered close-up
--ar 4:5 --sref 1234567890 --sw 300 --s 500
```

비용: 4x (--sref). `--sv 7` default 적용.

## v8 권장 베이스라인

| 케이스 | 권장 기본 |
|---|---|
| 제품샷 사진 | `--style raw --hd --q 4 --s 250` |
| 인물 사진 | `--style raw --s 200` (또는 --hd 추가) |
| 일러스트 | `--s 500` (raw 없이) |
| 풍경·시네마틱 | `--style raw --hd --q 4 --s 300` |
| 빠른 탐색 | 기본만 (--ar만) |

## 출처

- [Midjourney Documentation — Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Blake Crosley — Midjourney V8.1 + V7 Reference](https://blakecrosley.com/guides/midjourney)
- [ArtPromptHQ — Ultimate Midjourney Prompt Packs Guide](https://www.artprompthq.com/blog/ultimate-midjourney-prompt-packs-parameters-settings/)
