---
name: story-webnovel-writer
description: |
  웹소설 회차 집필 스킬 — 한 회를 어떻게 쓰고 어디서 자를 것인가에 집중한다. 장르별 문법(현판·로판·무협·BL·미스터리)의 문단 길이·대사 비중·시점 관습·회귀/빙의/환생 클리셰 운용을 적용하고, 회차 절단(클리프행어) 강도를 등급으로 설계한다. 어느 플랫폼에 연재할지는 story-webnovel-planner에서 이미 확정된 것으로 본다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "웹소설 회차 집필", "웹소설 한 회 써줘"
  - "웹소설 절단", "클리프행어 설계", "회차 끝 어떻게"
  - "현판 문법", "로판 문법", "무협 클리셰", "회귀/빙의/환생"
  - "연참 주기", "회차 분량 조율"
version: "1.0.0"
---

# story-webnovel-writer: 웹소설 회차 집필

웹소설 **한 회를 완성**하는 스킬이다. 장르 문법을 적용해 회차 원고를 쓰고, 독자가 다음 회를 결제하도록 절단 지점을 설계한다. 플랫폼 판단은 `story-webnovel-planner`가 이미 끝냈다고 전제한다.

## 1. 개요

웹소설은 회차별 과금이 발생하므로 **한 회에 무엇을 담을지(밀도)**와 **어디서 자를지(절단)**가 곧 수익이다. 이 스킬은 장르 문법·절단 강도 두 축을 함께 다룬다.

## 2. 이 스킬이 하지 않는 것

- **플랫폼 선택 안 함** — 어느 플랫폼·결제 구조·독점 여부는 `story-webnovel-planner`가 확정. 이 스킬은 그 결정에 맞춰 분량·절단만 조율한다.
- **시리즈 전체 아크·상태 원장 안 만듦** — 마스터 기획서·회차 현황표는 `story-series-bible` 소관. 재호출 시 원장을 읽어 흐름을 복원한다.
- **외형 재나열 안 함** — 인물 시트는 `story-character-sheet`에. 본문에 캐릭터 외형을 나열하지 않는다(아래 §3 비주얼-서사 분리).
- **AI 슬롭 검수 자체 수행 안 함** — 완성 원고는 정규 검수 체인으로 넘긴다(§7 Post).

### 비주얼-서사 분리 원칙

회차 본문은 **이야기로 읽히게** 둔다. "은발에 왼쪽 눈 밑 점, 검은 코트를 입은 그는…" 식으로 외형을 매 등장마다 재나열하는 것은 AI 티가 가장 잘 드러나는 슬롭이다. 외형 정보는 `story-character-sheet`의 인물 시트에 모으고, 본문에서는 행동·감정·대사로 캐릭터를 드러낸다.

## 3. 사전 확인

- `${CLAUDE_PLUGIN_ROOT}/skills/story-webnovel-planner/references/webnovel-platforms.md` — 확정 플랫폼의 회차 분량·결제 단위(절단 리듬의 기준).
- `references/genre-craft.md` — 장르별 문법·클리셰 운용.
- `references/cliffhanger-grades.md` — 절단 강도 등급·연참 주기.
- `${CLAUDE_PLUGIN_ROOT}/skills/story-series-bible/references/recall-design.md` — 재호출 역산 설계 5원칙(원장을 다시 받아 특정 회를 쓸 때).

## 4. 워크플로우

### Step 1 — 회차 목표

이 회의 사건·감정 변화·이번 회 훅을 한 줄로 정한다. 재호출이면 먼저 `story-series-bible` 현황표를 읽고, `recall-design.md` 5원칙에 따라 "현황표에 있으니까"가 아니라 "전체 흐름상 지금 이게 필요하니까" 이 회를 설계한다.

### Step 2 — 장르 문법 적용

확정 장르의 문단 길이·대사 비중·시점 관습을 적용한다. 상세는 `references/genre-craft.md`. 회귀/빙의/환생 같은 클리셰는 독자가 기대하는 관습 문법이 있으므로, 뒤집더라도 그 관습을 알고 뒤집는다.

### Step 3 — 집필

- **밀도**: 확정 플랫폼의 회차 분량 관행에 맞춘다(수치는 planner 표 참조, 미확인이면 플래그 유지).
- **훅 배치**: 이번 회 훅을 회차 안에 자연스럽게 심는다. 훅 4유형(감정·궁금증·캐릭터·공감)은 `genre-craft.md`의 사이다/고구마 축과 결합한다.
- **비주얼-서사 분리**(§2) 준수.

### Step 4 — 절단 설계

회차 끝(또는 결제 단위 끝)에 다음 회를 부르는 절단을 배치한다. 절단 강도는 등급으로 조율한다(매 회 최강 절단은 피로를 부른다) — `references/cliffhanger-grades.md`. 기다무 플랫폼이면 대기 해제 지점과 절단을 맞춘다.

### Step 5 — 분량 조율

플랫폼 평균 분량 대비 과부족을 조정한다. 수치 기준은 planner 표를 따르고, 미확인이면 "확인 필요"로 둔 채 상대 조율만 한다.

## 5. 출력 형식

```markdown
# [작품제목] [N]화 — [회차 제목]

> 참조 기획서: [작품제목]_기획서.md
> 이번 회 훅: ___ / 절단 강도: [등급]

## 본문
(회차 원고 — 지문 + 대사, 외형 재나열 없이)

---
## 절단 메모
- 절단 지점: ___
- 다음 회로 넘기는 미끼(떡밥): ___
- (기다무 시) 대기 해제 지점 정렬: ___
```

## 6. 주의사항

- **외형 재나열 금지**(§2) — AI 슬롭 1순위.
- **매 회 최강 절단 금지** — 강도 등급으로 리듬을 준다(`cliffhanger-grades.md`).
- **재호출은 전체 흐름에서 역산** — 현황표 한 줄만 보고 기계적으로 다음 회를 쓰지 않는다(`recall-design.md`).
- **분량 수치는 planner 확정값** — 지어내지 않는다.

## 7. 관련 스킬

### Before
- `story-webnovel-planner` — 플랫폼·연재 구조 확정
- `story-series-bible` — 마스터 기획서·회차 현황표(재호출 시 필수)
- `story-character-sheet` — 인물 시트(외형은 여기, 본문 아님)

### After
- `story-series-bible` — 회차 현황표 갱신
- `story-cover-art` — 웹소설 표지(부가)
- `story-ip-pitch` — 웹툰화·드라마화(부가)
- `moai-writer:book-concept-planner` — 단행본 전환(단방향 인계)

### Post (검수 — 텍스트 산출물 정규 체인)
- `moai-coworker:ai-slop-reviewer` — AI 슬롭 검수 (필수)
- `moai-writer:korean-humanize` — AI 티 정밀 윤문 (필수)

> ⚠️ 웹소설 회차는 독자가 AI 티에 가장 민감한 장르다. 정규 체인은 **필수**.

## 8. References

| 파일 | 로드 조건 |
|------|-----------|
| `references/genre-craft.md` | 장르별 문법·클리셰·훅 4유형이 필요할 때 |
| `references/cliffhanger-grades.md` | 절단 강도 등급·연참 주기가 필요할 때 |
| `../story-webnovel-planner/references/webnovel-platforms.md` | 확정 플랫폼 회차 분량·결제 단위 확인 |
| `../story-series-bible/references/recall-design.md` | 재호출 시 역산 설계 |

## 9. 출처

- 비주얼-서사 분리·훅 4유형: aitoon-plot 기획 시스템(내부 자산 이식).
- 장르 문법·클리셰 운용: 한국 웹소설 연재 관행(references에 정리, 수치는 플랫폼 확인).
- 원작 카피라이터: **조남경** (https://www.facebook.com/Bmisty)
