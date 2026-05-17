# GPT-image-2 — Text Rendering Rules

GPT-image-2는 이미지 내 텍스트 정확도가 95%+로 업계 SOTA입니다. 다만 정확도를 끌어올리려면 다음 4개 규칙을 지켜야 합니다.

## Rule 1 — Verbatim 따옴표

정확히 들어갈 문자열을 영문/한글 모두 **큰따옴표 안에** 적습니다. 모델은 따옴표 내용을 "이 글자를 그대로 써라"로 해석합니다.

```
The mug has "MONDAY" printed in thin uppercase sans-serif on the side.

The poster reads "서울의 봄" in bold serif typeface across the top half.
```

## Rule 2 — 폰트·무게·정렬 명시

폰트 패밀리 이름까지 지정할 필요는 없지만, 다음 4개 속성은 명시:

| 속성 | 예 |
|---|---|
| 무게 | thin · light · regular · medium · bold · black |
| 자형 | sans-serif · serif · slab-serif · monospace · handwritten · brush |
| 정렬 | left · center · right · justified |
| 색 | white · matte black · #8B0000 · gold foil |

```
"FRESH START" in bold sans-serif, white, centered at the bottom third.

"신선한 시작" in light serif, deep charcoal, left-aligned along the
left margin.
```

## Rule 3 — Verbatim 지시 명시

모델이 텍스트를 살짝 바꿔서 그릴 위험이 있을 때 (특히 브랜드명·고유명사) 다음 문구를 추가:

```
Verbatim — no extra characters, no substitutions, no spelling drift.
```

또는 특이 단어는 한 자씩 풀어서:

```
Spell it letter-by-letter: M-O-N-D-A-Y. No drift.
```

## Rule 4 — ALL CAPS 보정

소문자보다 ALL CAPS가 정확도가 더 높습니다. 대소문자가 중요한 경우만 소문자 사용. 일반 광고 카피·헤드라인은 ALL CAPS 권장.

권장:
```
"MONDAY"     ← 정확도 높음
```

주의 필요:
```
"Monday"     ← 가끔 "MONDAY"로 자동 변환됨
```

## 다국어 텍스트

GPT-image-2는 다음 비라틴 스크립트를 지원합니다 (95%+ 정확도):

- 한국어 (한글)
- 일본어 (히라가나, 가타카나, 한자)
- 중국어 (간체, 번체)
- 힌디어 (데바나가리)
- 벵골어
- 아랍어 (RTL 처리 가능)

다국어 사용 시 다음 추가 지시 권장:

```
Korean text "서울의 봄" in bold modern sans-serif (e.g.,
Pretendard-style), centered. Render every Hangul syllable
accurately, no character drift.
```

## 빈도 높은 실패 시나리오

| 증상 | 원인 | 대응 |
|---|---|---|
| 글자가 깨짐 | 폰트 무게 미지정 + 작은 사이즈 | 무게·크기 명시 + `perfectly legible` 추가 |
| 한 글자가 틀림 | verbatim 미명시 | "Verbatim — no extra characters" 추가 |
| 위치가 다름 | 위치 지시 누락 | "at the bottom third" · "along the left margin" 등 명시 |
| 색이 다름 | 색 미지정 | `in white` · `in matte black` 등 명시 |
| ALL CAPS가 무시됨 | 강조 부족 | 따옴표 안 텍스트를 ALL CAPS로 + "exactly as written" |

## 완성 예시

```
The poster reads "신선한 시작" in bold serif, deep charcoal,
centered across the top third. Below it, a smaller subline reads
"FRESH START" in thin sans-serif, light gray, centered. Render
both lines verbatim — no extra characters, no substitutions, no
spelling drift. Render every Hangul syllable accurately.
```

## 출처

- [OpenAI Cookbook — image-gen-models-prompting-guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide)
- [Imagine.art — GPT Image 2 Prompt Guide + 70 Prompts](https://www.imagine.art/blogs/gpt-image-2-prompt-guide)
