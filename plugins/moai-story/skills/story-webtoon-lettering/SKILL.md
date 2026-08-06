---
name: story-webtoon-lettering
description: |
  세로 스크롤 웹툰의 식자 전담 스킬. 말풍선 종류를 고르고, 한 원고 = 한 서체를 스킬이 결정하고, 한국어 효과음(SFX) 스타일을 지정하고, 2패스 오버레이로 SFX를 안전하게 얹는 워크플로우를 제공한다. 말풍선·SFX 사전은 '사람이 읽는 설명'이 아니라 AI 이미지 프롬프트에 그대로 복붙하는 작동 토큰이다. AI 작화에서 한글 서체가 컷마다 흔들리는 1순위 품질 문제를 서체 통일 규칙으로 잡는다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "말풍선 어떤 걸 써", "외침 풍선", "생각 풍선 프롬프트", "말풍선 꼬리"
  - "효과음 스타일", "쾅 SFX 어떻게", "한글 의성어 글자 스타일"
  - "웹툰 서체 통일", "글씨체가 컷마다 달라", "한 원고 한 서체"
  - "SFX 나중에 얹기", "2패스로 효과음", "효과음만 추가"
  - "식자 어떻게", "타이틀 서체", "간판 글씨 서체"
  - (체인 중간 호출) story-webtoon-episode·art·qc가 말풍선·서체·SFX 규격을 확인하려 할 때
version: "1.1.0"
---

# story-webtoon-lettering: 세로 스크롤 웹툰 식자 허브

말풍선·서체·효과음을 담당하는 식자 전담 스킬이다. 여기서 나오는 영어 스니펫은 **해석하거나 번역하지 않고 그대로** AI 이미지 프롬프트에 복붙한다 — 이름 자체가 작동 토큰이다. episode(계획)·art(프롬프트 삽입)·qc(가독 판정) 세 스킬이 공유하는 허브다.

## 1. 이 스킬이 하는 일

1. **말풍선 선택** — 장면 감정 → 이름 고르기 → 스니펫 복붙. (`references/balloon-dictionary.md`)
2. **서체 결정** — 한 원고 = 한 서체. 스킬이 정하고 **사용자에게 묻지 않는다.** (`references/korean-lettering.md`)
3. **SFX 스타일 지정** — 한국어 의성어 → 글자스타일 × 효과 매핑. (`references/sfx-dictionary.md`)
4. **배치 검증** — 2패스 오버레이로 SFX를 안전하게 얹고 크기·위치를 통제한다. (`references/two-pass-overlay.md`)

## 2. 핵심 원칙 (짧고 항상 필요)

- **이름이 형태를 강제한다** — 이름 속 형태 단어("Spike")는 프롬프트로 못 뺀다. 빼고 싶으면 그 단어가 없는 이름을 쓴다.
- **과분류 금지** — 비슷한 건 큰 갈래로 수렴한다. 감정 라벨(분노·경악…)은 별도 항목을 만들지 않고 형태에 매핑한다.
- **꼬리 규칙** — 꼬리는 화자 입 쪽. **꼬리 없는 타입:** 생각(Aura·구름), 전자/전화, 나레이션 박스. **예외:** Held-Back Spike는 스파이크가 곧 꼬리(별도 꼬리 금지).
- **한 원고 = 한 서체** — 원고 톤에 맞춰 정자 고딕 또는 정자 명조를 **스킬이 정해 전 회차 동일 적용**한다. 본문에는 손글씨체·개성 서체 금지(가독·통일 우선).
- **2패스 = 제거는 위험, 추가는 안전** — 완성 원고를 두고 SFX만 오버레이로 얹는다. 재생성 위험을 피한다.

## 3. 글자 3분기 (원고 종류 판정)

식자 작업은 원고가 어느 분기인지부터 판정한다.

| 분기 | 뜻 | 이 스킬의 개입 |
|------|-----|----------------|
| **클린 원고** | 글자 없음 (말풍선·SFX 모두 없음) | 식자 안 함. 대사는 `references/dialogue-memo.md` 스크립트로 편집 도구에 인계 |
| **대사 포함** | 말풍선·대사까지 1패스 생성 | 말풍선 사전 + 서체 규칙 적용 |
| **큰 글씨 / SFX** | 대사 포함 위에 SFX를 2패스로 얹음 | SFX 사전 + 2패스 오버레이 적용 |

> 클린 원고는 완성본에서 말풍선을 제거해 되얻을 수 있다(원본 비율 유지). 대사 포함 ↔ 클린을 잇는 수정 안전망이다.

### 분기별 프롬프트 꼬리

| 분기 | 프롬프트 맨 끝에 박는 문구 |
|------|----------------------------|
| 클린 원고 | `no text, no speech balloons, no SFX anywhere` |
| 대사 포함 | `draw ONLY the specified 💬 balloons; no other text` |
| 큰 글씨 / SFX | (2패스) `keep the existing art & balloons 100% intact; add SFX only` |

## 4. 말풍선 빠른 참조 (자주 쓰는 코어)

전체 40여 종은 `references/balloon-dictionary.md`. 가장 자주 쓰는 코어만 인라인으로 둔다.

| 감정 | 이름 | 스니펫 |
|------|------|--------|
| 평범한 대사 | Normal Speech | `a normal speech balloon (smooth oval, small tail to mouth)` |
| 생각(기본) | Fine Spike Aura | `a "Fine Spike Aura" balloon (oval with a fine thin spiky aura outline, NO tail)` |
| 속삭임 | Whisper | `a WHISPER balloon (dashed/dotted outline)` |
| 외침·비명 | Loud Shout/Scream | `a loud scream balloon (sharp spiky burst)` |
| 놀람·경악 | Surprised/Shocked | `a "Surprised/Shocked" balloon (jagged burst outline)` |
| 억눌린 톤 | Held-Back Spike | `a "Held-Back Spike" balloon (angular polygon body; the single SPIKE serves AS the tail)` |
| 나레이션 | Narration Box | `a NARRATION BOX (rectangular caption box, no tail)` |
| 전화 너머 | Telephone/Electronic | `a TELEPHONE/ELECTRONIC balloon (rectangular zig-zag electronic outline)` |

## 5. 말풍선 선택

장면 감정을 정하고 사전에서 **이름**을 고른 뒤, 그 영어 스니펫을 해당 컷 프롬프트에 복붙한다. 코어(대사/생각·외침/감정·특수)와 확장(디지털·매체기기·환경·판타지)으로 나뉜다. **세로 스크롤 기준 위치 거동**(여백 띠 침범 규칙, 1화면 동시 노출 말풍선 수 상한)은 사전 안에 별도 절로 둔다.

→ 상세: `references/balloon-dictionary.md`

## 6. 서체 결정 (한 원고 = 한 서체)

- 정자 고딕(밝음·일상·코미디·액션) / 정자 명조(차분·감성·드라마·시대물) 중 원고 톤으로 **스킬이 결정**한다.
- 프롬프트 못박기: `clean upright Korean Gothic sans-serif, even stroke weight, identical typeface on every page` (명조면 `Myeongjo serif`).
- **직전 페이지 첨부 시 "글씨체도 동일"을 반드시 명시** — 안 하면 굵기·둥글림이 컷마다 흔들린다.
- 텍스트 요소별(말풍선 본문/SFX/타이틀/간판/디지털 화면) 서체 매핑 표를 함께 제공한다.

→ 상세: `references/korean-lettering.md`

## 7. SFX 스타일 지정

SFX는 조합형이다 — **소리(글자 내용) × 글자스타일(L1~L16) × 효과처리(E1~E10) × 배치**. 소리는 자유 입력, 스타일만 사전에서 고른다.

자주 쓰는 매핑(전체는 `references/sfx-dictionary.md`):

| 음 종류 | 스타일 | 효과 | 대표(한글) |
|---------|--------|------|-----------|
| 충격·타격 | L1 굵은블록 / L2 깨진 | E1 버스트 / E6 균열 | 쾅·콰직·퍽 |
| 동작·이동 | L4 기울어진 | E2 속도선 | 슈욱·타다닥 |
| 감정·심장 | L3 둥근 | E3 펄스링 | 두근·콩닥 |
| 붕괴·무너짐 | L11 해체·붕괴 | E6 균열 / E5 먼지 | 와르르·쿠구궁 |
| 화염·작열 | L15 화염 | E1 버스트 / E5 불티 | 화르륵·활활 |

- **생성 공식:** `이름 토큰 + 형태 묘사 + 소리별 컬러`. 이름만 주면 뭉개진다.
- **가독성 트레이드오프:** 파쇄·번개·비명은 강할수록 읽기 어렵다 → 감정 정점·짧은 효과음에만.
- L11은 **한글 자모 분리**를 전제한 파편 질감 레버(고딕=돌덩이/손글씨=잉크 방울)를 포함한다.

→ 상세: `references/sfx-dictionary.md`

## 8. 2패스 오버레이 워크플로우

1. **1패스** — 클린 원고 + 말풍선까지 생성(보존할 완성본).
2. **2패스** — 완성본을 첨부하고 **SFX만 추가.** "기존 그림·말풍선 100% 보존"을 못박는다.
3. 오타·실패 시 1패스 원본에서 2패스만 다시 돌린다.

함께 지키는 배치 규칙:

- **크기:** 소리 세기·거리로 정한다. 화면·컷 대비 과대 금지, 감정 정점 **1~2개만 집중**(모든 소리에 달지 않는다).
- **동재질 함정:** 물 위 물·불 위 불 SFX는 묻힌다 → 색 진하게 + 흰 테두리, 또는 배경 여백으로 이동.
- **매체 일치:** 유화·수채 등 페인팅 화풍에선 SFX를 매끈 벡터로 회귀시키는 관성이 있으니 "그림과 동일한 붓터치·질감으로"를 긍정 지시로 박는다.
- **세로 여백 띠 침범 금지:** SFX가 컷 사이 빈 띠나 아래 컷 그림을 덮지 않게 한다.

→ 상세: `references/two-pass-overlay.md`

## 9. 사용 패턴 (프롬프트에 박는 법)

각 컷 장면 묘사 아래에 `💬`로 **[사전 영어 스니펫] + 위치 한 줄 + 한국어 대사**를 적는다. 프롬프트 맨 끝의 클린 경고문은 **"지정된 💬 말풍선만 그리고 그 외 텍스트는 금지"**로 바꾼다.

```
- 컷4 (전폭):
  지우가 폰을 보고 흠칫 놀라는 상반신.
  💬 a "Surprised/Shocked" balloon (jagged burst outline), tail to her mouth — 지우 머리 위, "헉, 엄마?!"
```

## 10. 관련 스킬

| 관계 | 스킬 | 역할 |
|------|------|------|
| Before | `story-webtoon-episode` | 컷 대본에서 말풍선·SFX 자리를 미리 계획 |
| Post-참조 | `story-webtoon-art` | 작화 프롬프트에 스니펫 삽입 |
| Post-검수 | `story-webtoon-art` (qc 분기) | SFX 가독 판정 |
| 자매 허브 | `story-webtoon-spec` | 원고 규격·용어 사전 상호 참조 |
| 폰트 라이선스 | `moai-designer:design-system-library` | 한글 서체 라이선스는 이 스킬 참조 |

## 11. References

| 파일 | 로드 조건 |
|------|-----------|
| `references/balloon-dictionary.md` | 말풍선 종류 선택·꼬리·세로 배치가 필요할 때 |
| `references/sfx-dictionary.md` | 한국어 SFX 스타일 지정이 필요할 때 |
| `references/korean-lettering.md` | 서체 통일·요소별 서체 결정이 필요할 때 |
| `references/two-pass-overlay.md` | SFX를 2패스로 얹고 크기·배치를 통제할 때 |
| `references/dialogue-memo.md` | 클린 원고 분기에서 편집 도구로 넘길 대사 스크립트를 만들 때 |

## 출처

- 핵심 자산: aitoon 연출·기획 시스템(내부 자산 이식, 세로 스크롤·한국 플랫폼 맥락으로 조정).
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
