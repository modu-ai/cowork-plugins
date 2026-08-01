---
name: story-cover-art
description: |
  표지·썸네일 스킬 — 단행본 인쇄 표지 / 웹툰 썸네일·타이틀 카드 / 웹소설 표지 3분기로 구도·시선 유도·제목 자리를 설계한다. 규격 수치는 story-webtoon-spec 허브를, 폰트 라이선스는 moai-designer를 참조한다. 생성 실행·크레딧은 moai-media에 위임한다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "책 표지", "단행본 표지", "웹툰 썸네일", "타이틀 카드", "웹소설 표지"
  - "표지 구도", "표지 시안", "커버 아트"
  - "썸네일 가독성", "모바일 표지"
version: "1.0.0"
---

# story-cover-art: 표지·썸네일

표지와 썸네일의 **구도·시선 유도·제목 자리**를 설계하는 스킬이다. 용도 3분기(단행본 인쇄 표지 / 웹툰 썸네일·타이틀 카드 / 웹소설 표지)로 규격과 우선순위가 다르다. **생성 실행·크레딧은 하지 않는다** — `moai-media`에 위임한다.

## 1. 개요

표지는 **무엇을 보여줄지(주 인물·분위기·핵심 소품)**와 **어떻게 시선을 끌지(구도·대비·제목 자리)**가 클릭률·구매율을 결정한다. 용도에 따라 규격과 가독 우선순위가 달라진다 — 단행본은 인쇄 해상도·제본 여백, 썸네일은 모바일 축소 가독이 최우선.

## 2. 이 스킬이 하지 않는 것

- **이미지 생성·크레딧 고지·모델 선택 안 함** — `moai-media:media-higgsfield-core` 계약에 위임(§4-생성 실행).
- **폰트 라이선스 판정 안 함** — 무료 상업용 한글 폰트 판정은 `moai-designer` 소유. 참조만 한다.
- **규격 수치 단정 안 함** — 썸네일·표지 비율·최소 크기는 `story-webtoon-spec` 허브 참조.
- **타이포그래피 조판 안 함** — 제목 자리만 잡고, 실제 폰트·조판은 편집·디자인 단계(`moai-designer`).

## 3. 사전 확인

- `references/cover-composition.md` — 구도·시선 유도·대비·제목 자리·모바일 축소 가독 우선순위.
- `${CLAUDE_PLUGIN_ROOT}/skills/story-webtoon-spec/references/thumbnail-cover-specs.md` — 썸네일·타이틀 카드·표지 비율·최소 크기.
- `moai-designer:design-system-library/references/korean-design-systems.md` — 무료 상업용 한글 폰트 판정(제목 폰트 선택 시).

## 4. 워크플로우

### Step 1 — 용도 분기 판정

**단행본 인쇄 표지 / 웹툰 썸네일·타이틀 카드 / 웹소설 표지** 중 무엇인지 먼저 정한다. 규격·가독 우선순위가 갈린다.

| 용도 | 규격 기준 | 최우선 |
|------|-----------|--------|
| 단행본 인쇄 표지 | 인쇄 해상도·제본 여백 | 인쇄 품질·앞뒤·책등 |
| 웹툰 썸네일·타이틀 카드 | `thumbnail-cover-specs.md` 비율·최소 크기 | 모바일 축소 가독 |
| 웹소설 표지 | `thumbnail-cover-specs.md` 비율 | 목록 축소 시 인물·제목 식별 |

### Step 2 — 콘셉트 확정

주제·분위기·타깃 독자·핵심 인물/소품을 정한다. 인물 일관성이 필요하면 `story-character-sheet`의 참조·앵커를 프롬프트에 반영.

### Step 3 — 구도·시선 유도 설계

`cover-composition.md`로 구도(삼분할·중앙·대각선)·시선 유도·대비를 설계한다. **제목·저자명 자리를 미리 비워 둔다**(Step 5).

### Step 4-생성 실행 — moai-media 위임

표지 프롬프트의 실제 생성·업스케일·비용 프리플라이트·모델 선택은 `moai-media:media-higgsfield-core` 계약(`models_explore` 라이브 조회 + `get_cost` 사전 고지)에 위임한다.

> moai-media 미설치 시: 완성 표지 프롬프트를 텍스트로 출력하고 Higgsfield 웹(https://higgsfield.ai)에서 직접 생성하도록 안내한다.

### Step 5 — 제목 자리 가이드 인계

제목·저자명이 들어갈 자리를 별도 메모로 남긴다(폰트·조판은 편집 단계). 폰트 선택 시 무료 상업용 여부는 `moai-designer:design-system-library`에서 확인하도록 인계한다.

## 5. 출력 형식

```markdown
## 표지 설계 — [작품] ([용도])
> 규격: [thumbnail-cover-specs 참조값] / 최우선: [모바일 가독 등]

### 콘셉트
- 주 인물·분위기·핵심 소품

### 구도
- 구도 유형 / 시선 유도 / 대비 포인트
- 제목 자리: [상단/하단/좌측 등] — 비워 둠

### 생성 프롬프트
[복붙 프롬프트 — 내용물 가드 포함]
```
→ 생성 실행: `moai-media:media-higgsfield-core` 위임.

## 6. 주의사항

- **AI 생성물 표시 의무 확인** — AI 생성 이미지·표지를 상업 플랫폼에 제출·게시할 때 AI 생성물 표시 의무를 확인한다(상세는 `moai-lawyer`의 AI 관련 체크리스트 참조).
- **생성 전 비용 고지·승인.** `moai-media`의 `get_cost` 결과를 사용자에게 고지하고 승인받은 뒤 생성한다.
- **용도별 최우선 다름** — 썸네일은 모바일 축소 가독, 단행본은 인쇄 해상도·여백.
- **제목 자리 미리 확보** — 인물·소품이 제목 영역을 침범하지 않게.
- **스타일 참조 시 내용물 가드** — 스타일만 참조하고 피사체를 베끼지 않도록 `story-webtoon-art/references/style-anchor.md`의 가드 문구를 재사용.
- **규격·폰트 수치 지어내지 않음** — 규격은 spec 허브, 폰트 라이선스는 designer.

## 7. 관련 스킬

### Before
- `story-character-sheet` — 인물 참조·일관성 앵커
- `story-webtoon-spec` — 썸네일·표지 규격

### After
- `story-webnovel-writer` / `story-webtoon-episode` — 본편(표지는 부가 산출)

### 위임
- `moai-media:media-higgsfield-core` — 생성 실행·업스케일·비용·모델
- `moai-designer:design-system-library` — 무료 상업용 폰트 판정
- `moai-lawyer` — AI 생성물 표시 의무 체크리스트

## 8. References

| 파일 | 로드 조건 |
|------|-----------|
| `references/cover-composition.md` | 구도·시선 유도·제목 자리·모바일 가독이 필요할 때 |
| `../story-webtoon-spec/references/thumbnail-cover-specs.md` | 썸네일·표지 비율·최소 크기 확인 |
| `moai-designer:design-system-library/references/korean-design-systems.md` | 무료 상업용 한글 폰트 판정 |
| `../story-webtoon-art/references/style-anchor.md` | 내용물 가드 문구 재사용 |

## 9. 출처

- 구도·시선 유도·모바일 가독 우선순위: 표지 디자인 실무 관행(references에 정리).
- 규격 수치: `story-webtoon-spec` 허브. 폰트 라이선스: `moai-designer`.
- 생성·비용·모델: `moai-media:media-higgsfield-core` 라이브 계약.
