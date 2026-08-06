---
name: story-webtoon-art
description: |
  웹툰 작화 프롬프트 조립 스킬 — 화풍 앵커를 고정하고, 컷별 복붙 프롬프트를 조립하고, 첨부 이미지 서수를 1:1로 매핑하고, 멀티 이미지 세션 컨텍스트를 관리한다. 스타일 참조에서 피사체가 새어 그려지는 것을 내용물 가드로 막는다. 생성 실행·크레딧·모델 선택은 moai-media에 위임한다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "웹툰 작화 프롬프트", "컷 프롬프트 조립"
  - "화풍 통일", "스타일 앵커", "참조 이미지 첨부 순서"
  - "캐릭터 일관성 프롬프트", "첨부 서수 매핑"
  - "멀티 컷 세션", "여러 컷 연속 생성"
version: "1.1.0"
---

# story-webtoon-art: 작화 프롬프트 조립

컷 대본을 받아 **작화 프롬프트를 조립**하는 스킬이다. "무엇을 어떻게 그리라고 지시할 것인가"에 집중한다 — 화풍 앵커 고정, 컷별 복붙 프롬프트, 첨부 이미지 서수 매핑까지. **생성 실행·검수·비용은 하지 않는다**: 생성은 `moai-media`, 검수는 `story-webtoon-qc`가 맡는다.

## 1. 개요

이 스킬은 **프롬프트를 만드는 데까지만** 책임진다. 화풍을 컷마다 흔들리지 않게 앵커로 고정하고, 컷 지시를 복붙 가능한 프롬프트로 조립하고, 첨부할 참조 이미지의 순서를 서수로 못박는다. 실제 이미지 생성·모델 선택·크레딧 고지는 `moai-media`가 라이브 조회로 처리한다.

## 2. 이 스킬이 하지 않는 것

- **이미지 생성·크레딧 고지·모델 선택 안 함** — `moai-media:media-higgsfield-core` 계약에 위임(§4-생성 실행).
- **검수(QC) 안 함** — 산출 이미지의 결함 판정·일관성 위반 검수는 `story-webtoon-qc` 소관.
- **말풍선·서체·SFX 스니펫 안 만듦** — `story-webtoon-lettering`이 소유. 이 스킬은 그 스니펫을 프롬프트에 삽입만 한다.
- **모델 프롬프트 문법 안 소유** — 미드저니 sref·모델 파라미터, Gemini, GPT-image 등 벤더별 문법은 `moai-media`가 소유한다. 이 스킬은 가져오지 않는다(포팅 시 media 계열과 충돌).

## 3. 사전 확인

- `${CLAUDE_PLUGIN_ROOT}/skills/story-webtoon-spec/references/manuscript-specs.md` — 세로 스크롤 캔버스 규격·색공간(sRGB). 프롬프트에 원고 규격을 반영할 때 참조.
- `${CLAUDE_PLUGIN_ROOT}/skills/story-webtoon-lettering/references/balloon-dictionary.md` — 대사 포함 분기면 컷별 말풍선 스니펫을 여기서 가져와 삽입.

## 4. 워크플로우

### Step 1 — 화풍 앵커 고정

시리즈 화풍을 7토큰(팔레트·기법·윤곽선·색면·텍스처·무드·폰트무드)으로 분해해 영어 STYLE 블록으로 만든다. **내용물 가드 문장은 절대 생략하지 않는다** — 없으면 스타일 참조 속 얼굴·집·풍경까지 베껴 그린다. 상세·복붙 템플릿은 `references/style-anchor.md`.

> 화풍 앵커(7토큰 인스턴스)는 이 스킬이 시리즈별로 보유한다. 아트 스타일 토큰 레지스트리 자체는 `moai-designer`가 소유하며, 이 스킬은 추출 절차로 시리즈 앵커만 갖는다.

### Step 2 — 컷별 프롬프트 조립

컷 대본(`story-webtoon-episode`)의 각 컷을 복붙 프롬프트로 옮긴다.

- **한국어 프롬프트 본문 + 영어 STYLE 블록** 혼용 — 본문은 한국어로 장면·화각·인물·동작을, STYLE 블록만 영어로 박으면 화풍이 또렷이 잡힌다.
- 캐릭터 고정 외형·색·일관성 앵커를 **매 컷 반복 명시**(색 표류 방지).
- 대사 포함이면 컷 묘사 아래에 `💬 [lettering 스니펫] + 위치 + 한국어 대사`를 삽입.

### Step 3 — 첨부 서수 1:1 매핑

참조 이미지(캐릭터 ref·스타일 그리드·직전 컷)를 순서대로 첨부하고, 프롬프트 첫 문단에서 "N번째 이미지는 X입니다"로 1:1 매핑한다.

- **헤더 첨부 순서 ↔ 코드블록 서수가 개수·순서·이름까지 글자 그대로 일치**해야 한다.
- 캐릭터는 각각 개별 서수로 — 뭉뚱그리기 금지("첫 이미지들은 인물·고양이" ❌).
- 첨부 개수는 컷마다 다르다 — 실제 첨부한 것만 실제 순서대로 다시 센다. 동적 서수 계산·자기검증 4줄은 `references/reference-ordinal.md`.

### Step 4 — 멀티 이미지 세션 컨텍스트 관리

여러 컷을 한 세션에서 연속 생성할 때 컨텍스트를 절약한다.

- **텍스트 체크포인트 인계** — 확정된 컷을 텍스트 요약으로 넘겨 비전 재분석을 줄인다.
- **의심 컷만 crop** — 전체를 매번 비전 분석하지 않고 의심 컷만 잘라 확인한다.
- 천장은 페이지 수가 아니라 **비전 분석 횟수**다. 상세는 `references/context-budget.md`.

### Step 4-생성 실행 — moai-media 위임

조립된 프롬프트의 실제 생성·비용 프리플라이트·모델 선택은 `moai-media:media-higgsfield-core` 계약(`models_explore` 라이브 조회 + `get_cost` 사전 고지)에 위임한다.

> moai-media 미설치 시: 완성된 컷 프롬프트를 텍스트로 출력하고 Higgsfield 웹(https://higgsfield.ai)에서 직접 생성하도록 안내한다(첨부 순서 배너 포함).

## 5. 출력 형식

각 컷 프롬프트는 첨부 순서 배너 → 서수 매핑 문단 → 본문 → STYLE 블록 순으로 조립한다.

```
⚠️ 이 프롬프트는 참조 이미지를 함께 첨부해야 작동합니다.
   첨부 순서: ① 캐릭터A ref → ② 스타일 그리드 → (연속 시) ③ 직전 컷 결과

첫 번째 이미지는 [캐릭터A] 인물 참조입니다.
두 번째 이미지는 스타일 참조입니다 — 색·질감·화풍만 참조, 그 속 인물·사물·풍경은 베끼지 마세요.
[캐릭터A 고정 외형·색·앵커 한 줄]을 매 컷 같게 유지.

[한국어 본문 — 장면 / 화각 / 인물 / 동작 / 방향 고정]
💬 [lettering 스니펫] (대사 포함 분기면)

=== STYLE (match the ATTACHED reference image; use ONLY its palette/texture/technique,
and IGNORE its subject matter — faces, houses, landscapes, animals. Do NOT copy any of those objects) ===
- Palette / Technique / Linework / Color fill / Texture / Mood: [7토큰]
```

→ 생성 실행: `moai-media:media-higgsfield-core` 위임.

## 6. 주의사항

- **AI 생성물 표시 의무 확인** — AI 생성 이미지를 상업 플랫폼에 제출·게시할 때 AI 생성물 표시 의무를 확인한다(상세는 `moai-lawyer`의 AI 관련 체크리스트 참조).
- **내용물 가드 절대 생략 금지** — STYLE 블록의 `IGNORE its subject matter` 문구가 빠지면 스타일 참조 속 피사체가 베껴진다.
- **첨부 서수는 매번 계산.** 인물이 늘면 뒤 서수가 밀린다 — 고정 서수 하드코딩 금지.
- **색·외형은 매 컷 반복 명시.** 참조에만 있고 프롬프트에 없으면 컷마다 색이 바뀐다.
- **크레딧·모델을 지어내지 않는다** — moai-media가 조회한다.
- **검수는 여기서 안 한다** — 산출 후 `story-webtoon-qc`로 넘긴다.

## 7. 관련 스킬

### Before
- `story-webtoon-episode` — 컷 대본
- `story-character-sheet` — 캐릭터 참조·일관성 앵커
- `story-webtoon-lettering` — 컷별 말풍선·SFX 스니펫

### After
- `story-webtoon-qc` — 산출 이미지 결함·일관성 검수
- `story-series-bible` — 완성 회차 상태 갱신

### 위임
- `moai-media:media-higgsfield-core` — 생성 실행·비용 프리플라이트·모델 선택

## 8. References

| 파일 | 로드 조건 |
|------|-----------|
| `references/style-anchor.md` | 화풍 7토큰 분해·영어 앵커 블록·내용물 가드가 필요할 때 |
| `references/reference-ordinal.md` | 첨부 서수 1:1 매핑·동적 계산·자기검증이 필요할 때 |
| `references/context-budget.md` | 멀티 이미지 세션 컨텍스트 절약·crop 검수가 필요할 때 |
| `../story-webtoon-spec/references/manuscript-specs.md` | 캔버스 규격·색공간 확인 |
| `../story-webtoon-lettering/references/balloon-dictionary.md` | 대사 포함 시 말풍선 스니펫 삽입 |

## 9. 출처

- 스타일 7토큰·내용물 가드·첨부 서수 매핑·멀티 이미지 세션 관리: aitoon-comic(내부 자산 이식).
- 생성·비용·모델: `moai-media:media-higgsfield-core` 라이브 계약.
- 벤더 프롬프트 문법: `moai-media` 소유(이 스킬은 참조만).
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
