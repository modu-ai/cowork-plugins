# 한글 서체 — 한 원고 = 한 서체

> AI 작화에서 한글 서체가 컷마다 흔들리는 것은 한국 창작자의 1순위 품질 문제다. 이 문서는 **스킬이 서체를 결정하고, 전 회차에 통일 적용**하는 규칙을 제공한다. 사용자에게 서체를 묻지 않는다.

## 1. 한 원고 = 한 서체 (핵심 규칙)

- 원고 톤에 맞춰 **정자 고딕** 또는 **정자 명조** 중 하나를 스킬이 정한다.
- 정한 서체를 **전 회차·전 페이지에 동일 적용**한다. 회차마다 서체를 바꾸지 않는다.
- 본문(말풍선 대사)에는 **개성 서체·손글씨체 금지** — 가독·통일 우선.

## 2. 무드 매핑

| 서체 | 무드 | 적합 장르 |
|------|------|-----------|
| 정자 고딕 (sans-serif) | 밝음·명료·현대 | 일상·코미디·액션 |
| 정자 명조 (serif) | 차분·감성·무게 | 드라마·감성·시대물 |

## 3. 프롬프트 못박기 문구

- 고딕: `clean upright Korean Gothic sans-serif, even stroke weight, no handwriting / rounded / decoration, identical typeface on every page`
- 명조: `clean upright Korean Myeongjo serif, even stroke weight, no handwriting / decoration, identical typeface on every page`

### 직전 페이지 첨부 시 (필수)

이전 회차·이전 페이지를 참조로 첨부할 때는 **"글씨체도 동일"을 명시적으로** 박는다.

> `keep the SAME typeface as the attached previous page` — 안 그러면 "산세리프"처럼 느슨하게 받아들여 굵기·둥글림이 페이지마다 흔들린다.

## 4. 텍스트 요소별 서체 매핑

> 말풍선 본문뿐 아니라 다른 텍스트 요소도 서체를 지정하면 정확도가 오른다(안 하면 흔들림). 본문은 §1~3 규칙, 나머지는 아래 기본값을 프롬프트에 영어로 박는다.

| 텍스트 요소 | 기본 서체(프롬프트에 박기) |
|------------|---------------------------|
| 말풍선 본문·나레이션 | §1~3 서체 규칙(정자 고딕/명조 — 원고 통일) |
| SFX 효과음 | `sfx-dictionary.md` L1~L16 (별도 팔레트) |
| 타이틀·제목 | 무드별 — `Korean rounded cute` / `retro signboard` / `brush` 등 |
| 배경 텍스트(간판·표지판) | `Korean retro vintage signboard lettering` 등 상황별 |
| 화면·디지털(폰·모니터) | `Korean LCD` / `LED dot-matrix` / `glitch` / `terminal` |

> ★ **본문에는 개성 서체 금지**(가독·통일 우선) — 개성 서체는 타이틀·SFX·배경·화면 요소용.

## 5. 폰트 라이선스

한글 서체의 상업 사용 라이선스(웹툰 배포·유료 연재 포함)는 별도로 확인해야 한다. 서체 라이선스 목록은 `moai-designer:design-system-library`의 `references/korean-design-systems.md`를 참조한다.

## 출처

- 핵심 자산: aitoon 연출·기획 시스템(내부 자산 이식, 세로 스크롤·한국 플랫폼 맥락으로 조정).
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
