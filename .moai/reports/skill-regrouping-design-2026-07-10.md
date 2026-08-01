# 스킬 재그룹핑 + 플러그인 분리 설계서 — 모두의클로드 플러그인 패밀리 v6.1 → v6.2

> 작성: 2026-07-10 · MoAI Orchestrator
> 전제: v6.1.0 실측 (15종 플러그인 · 233 스킬) 기반 그룹핑 정합성 감사
> 성격: **설계서(계획)** — 본 문서는 이관 실행 전 결정용. 승인 후 별도 위임으로 실행.

---

## 0. 배경 및 목표

`expert-plugin-expansion-plan-2026-07-09.html` 갱신 과정에서 15개 플러그인 233개 스킬을 전수 실측한 결과, 두 부류의 그룹핑 문제를 식별했다.

1. **접두사-소속 불일치**: 스킬의 접두사(prefix)가 속한 플러그인 도메인과 어긋남
2. **플러그인 비대 + 도메인 혼재**: 단일 플러그인이 여러 이질적 도메인을 담아 스킬 탐색·유지보수가 모놀리스화

본 설계서는 사용자가 선택한 4개 후보(A·B·C·D)에 대해 이관 대상 스킬 명단·신규 플러그인 구조·기존 플러그인 슬림 결과·영향 범위·이관 순서·검증 게이트를 정의한다.

**원칙**: 스킬 총수(233)는 불변 — 이 설계는 재배치만 다룬다. 신규 플러그인은 기존 패밀리의 2-에이전트 표준(worker + read-only auditor)을 따른다(`expert-plugin-expansion-plan` §04 설계 원칙).

---

## 1. A — 소속 재검토 (실측 결과: 정정 대상 축소)

> 사용자 선택 A는 "명백한 정정 대상"이었으나, 실측 결과 **대부분 정상 구조**로 판명. 본 절은 실측 근거를 기록한다.

### A-1. `design-system-library` 중복 → 정상 (수정 불필요)

| 위치 | 파일 수 | 역할 |
|---|---|---|
| `moai-designer/skills/design-system-library/` | **90 파일** | 정본(canonical) — 실제 토큰·컴포넌트 정의·샘플 |
| `moai-officer/skills/office-design-system-library/` | **1 파일** | 포인터 — "정본은 moai-design에 있음"을 명시하는 thin wrapper |

officer 스킬 본문이 명시적으로 "본 스킬은 moai-design 플러그인의 정본을 가리키는 포인터입니다"라고 서술하며, "cowork 중복 사본은 경계 계약(산출물=coworker, 체계=design)에 따라 제거됨"이라고 기록. **이미 의도적으로 설계된 포인터 구조**이므로 중복 제거 대상이 아니다.

### A-2. `office-korean-spell-check` → rename 옵션 (이관 아님)

- **현재**: `moai-writer/skills/office-korean-spell-check/` (writer에 존재, office 접두사)
- **실측 맥락**: writer 내부에서 `book-*` 8개 스킬이 워크플로우 참조(원고 작성 → 맞춤법 검사). writer-director 에이전트·README·book 스킬들이 참조.
- **officer 이관 시 위험**: book 저작 워크플로우의 맞춤법 검사 단계가 끊김.
- **권장**: officer 이관 **불가**. 접두사만 정리 — `office-korean-spell-check` → `korean-spell-check` (무접두사) 또는 `writer-korean-spell-check`.
- **참조 갱신**: rename 시 writer 내부 10개 파일 참조 일괄 치환(writer-director, README, book-* 8).

### A 요약
| 항목 | 조치 | 범위 |
|---|---|---|
| design-system-library | 수정 없음 | — |
| korean-spell-check | rename(옵션) | writer 내부 참조 ~10건 |

---

## 2. B — moai-story 신설 (story 13 스킬 분리)

### 2.1 근거
writer 플러그인은 현재 **스토리텔링(story)** + **출판(book)** 두 이질적 산업을 한 플러그인에 담고 있다. story 계열(웹툰·웹소설·시나리오·IP 파생)은 영상/웹툰 IP 콘텐츠 도메인이며, book 계열(단행본 집필·출판 기획)은 전통 출판 도메인이다. 결이 다르므로 story를 독립 직원으로 분리. **기억메모리 `project_moc_plugin_family_redesign_v2`에 이미 moai-story 신설이 계획(D9-D14)되어 있어 본 설계는 그 실행안.**

### 2.2 이관 대상 (story 13, 실측)
```
story-ad-conti, story-character-sheet, story-conti, story-cover-art,
story-ip-pitch, story-previz, story-project, story-screenplay,
story-synopsis, story-webnovel-writer, story-webtoon-art,
story-webtoon-episode, story-webtoon-planner
```

### 2.3 신규 플러그인 구조 — `moai-story`
| 요소 | 내용 |
|---|---|
| name / version | `moai-story` / `0.1.0` |
| Worker 에이전트 | `story-director` (스토리 창작 루프 실행) |
| Auditor 에이전트 | `story-continuity-auditor` (캐릭터·플롯·설정 연속성 검증) |
| Skills | story 13 (위 명단) |
| 커넥터(선택) | 웹툰/웹소설 플랫폼 연동 가이드 (자격증명 무번들 원칙) |
| README | 창작 워크플로우 + 카테고리 매핑 |

### 2.4 writer 슬림 결과
- **분리 전**: 23 스킬 (story 13 + book 8 + general-humanize-korean + office-korean-spell-check)
- **분리 후**: **10 스킬** (book 8 + general-humanize-korean + korean-spell-check)
- writer는 "출판·텍스트 다듬기" 도메인으로 명확화

### 2.5 영향
- writer 내부 story 참조 갱신 (writer-director, README, story 스킬간 참조)
- `moai-pm` 라우팅 플래그 추가: `--story`
- marketplace.json 등록 (15 → 16종)
- www 카탈로그 반영

---

## 3. C — officer 분할 (비대 31 스킬 해소)

### 3.1 근거
`moai-officer`는 31 스킬로 패밀리 최대 규모이며, 세 이질적 도메인이 혼재: (1) 문서 작성(본연), (2) 공공/금융 데이터 조회·분석, (3) 라이프스타일·자기계발. 문서 작성 도메인만 남기고 데이터·라이프스타일을 분리.

### 3.2 C-1. moai-analyst 신설 (data/public-data 11 스킬)

이관 대상 (11, 실측):
```
office-data-explorer, office-data-public-data, office-data-visualizer,
office-public-data-court-auction-search, office-public-data-korean-stock-search,
office-public-data-public-data, office-public-data-real-estate-search,
office-finance-court-auction-search, office-finance-korean-stock-search,
office-building-ledger-search, office-business-real-estate-search
```

신규 구조 — `moai-analyst`:
| 요소 | 내용 |
|---|---|
| name / version | `moai-analyst` / `0.1.0` |
| Worker | `data-analyst` (데이터 조회·시각화 루프) |
| Auditor | `data-provenance-auditor` (출처·신뢰성 검증) |
| Skills | data 11 (위 명단) |
| 커넥터 | 공공데이터 API 연동 (이미 office-* 에 존재) |

> 참고: HTML §05의 officer 행이 이미 auditor 이름으로 `data-auditor`를 예상하고 있어 네이밍 일관성 확보.

### 3.3 C-2. 라이프스타일 7 스킬 — 두 옵션

이관 대상 (7, 실측):
```
general-event-planner, general-self-care, general-travel-planner, general-wellness-coach,  (general 4)
office-goal-planner, office-habit-routine, office-retro-builder                           (office 3)
```

| 옵션 | 내용 | 장단 |
|---|---|---|
| **C-2a (권장)** | coworker `general`로 회수 | 직원 수 증가 없음, 범용 코어에 자연스럽게 귀속. 7개로 독립 플러그인은 과소 |
| C-2b | `moai-life` 신설 (자기계발·라이프스타일 전담) | 도메인 명확화, 직원 +1. 다만 7개 규모는 독립 플러그인 임계치 미달 |

### 3.4 officer 슬림 결과
- **분리 전**: 31 스킬
- **분리 후**: **13 스킬** (문서 작성 중심)
  ```
  office-docx-generator, office-hwpx-writer, office-pdf-writer, office-pptx-designer,
  office-xlsx-creator, office-html-report, office-html-slide, office-document-reader,
  office-design-system-library(pointer), office-mcp-connector-setup, office-notion-template-kit,
  office-time-system, office-daily-briefing
  ```
- officer는 "사무 문서 생산" 도메인으로 명확화

### 3.5 영향 (C 전체)
- officer 내부 data/life 참조 갱신
- `moai-pm` 라우팅: `--analyst` 추가 (C-2b 시 `--life` 추가)
- marketplace.json: 15 → 16(analyst) 또는 17(analyst+life)종
- www 카탈로그

---

## 4. D — moai-media 신설 (media 9 스킬 분리)

### 4.1 근거
`moai-marketer` 내 media 9종(이미지·영상·오디오 생성)은 마케팅 외에도 writer(표지·삽화)·officer(프레젠테이션)·story(커버아트)에서 범용으로 쓰이는 **생성 도구 모음**이다. 특정 직군(marketer)에 종속시키기보다 범용 미디어 생성 직원으로 독립시키면 교차 사용이 자연스럽다.

### 4.2 이관 대상 (media 9, 실측)
```
media-asset-production, media-audio-gen, media-codex-image,
media-gemini-3-image-prompt, media-gpt-image-2-prompt, media-higgsfield-image,
media-higgsfield-video, media-midjourney-v8-prompt, media-notebooklm-slide-prompt
```

### 4.3 신규 플러그인 구조 — `moai-media`
| 요소 | 내용 |
|---|---|
| name / version | `moai-media` / `0.1.0` |
| Worker | `media-producer` (멀티모달 생성 루프) |
| Auditor | `media-brand-auditor` (브랜드 정합·저작권·품질 검증) |
| Skills | media 9 (위 명단) |
| 커넥터 | Higgsfield/Midjourney 등 OAuth 가이드 (자격증명 무번들) |

> 설계 참고: media는 "도구 모음" 성격이 강해 2-에이전트 표준보다 경량화할 수 있으나, 패밀리 일관성을 위해 표준 유지를 권장(Auditor는 저작권/브랜드 위주).

### 4.4 marketer 슬림 결과
- **분리 전**: 28 스킬 (content 8 + marketing 11 + media 9)
- **분리 후**: **19 스킬** (content 8 + marketing 11)
- marketer는 "마케팅 기획·콘텐츠" 도메인으로 명확화

### 4.5 영향
- marketer 내부 media 참조 갱신
- `moai-pm` 라우팅: `--media` 추가
- marketplace.json: +1종
- media 스킬이 marketer content/marketing과 연계하므로 **경계 계약** 정의 필요 (예: media는 생성만, 카피/전략은 marketer) — design-system-library 포인터 패턴 참고 가능

---

## 5. 통합 영향 요약

### 5.1 플러그인 수 변동
| 시나리오 | 플러그인 수 | 비고 |
|---|---|---|
| 현재 (v6.1.0) | 15 | — |
| + B (story) | 16 | |
| + C-1 (analyst) + C-2a (회수) | 17 | life는 coworker 회수 |
| + C-1 + C-2b (life 신설) | 18 | life 독립 |
| + D (media) | 18~19 | 위 시나리오에 +1 |

**권장 조합(B+C-2a+D)**: 15 → **18종** (story·analyst·media 신설, life는 coworker 회수). 스킬 총수 233 불변.

### 5.2 스킬 재배치 총괄
| 출발 | 도착 | 스킬 수 |
|---|---|---|
| writer → moai-story | story 계열 | 13 |
| officer → moai-analyst | data 계열 | 11 |
| officer → coworker (general) | 라이프스타일 | 7 (C-2a) |
| marketer → moai-media | media 계열 | 9 |
| writer 잔류 | book + 텍스트 | 10 |
| officer 잔류 | 문서 작성 | 13 |
| marketer 잔류 | content + marketing | 19 |

### 5.3 공통 갱신 항목 (각 분리마다)
- 신규 플러그인: `plugin.json` + 2 에이전트 + skills/ 이동 + `README.md`
- 기존 플러그인: `plugin.json` version bump (0.1.0 → 0.2.0 minor), 내부 참조 grep·치환
- `moai-pm`: `/project` 라우팅 플래그 확장 + 라우터 스킬 갱신
- `.claude-plugin/marketplace.json`: 신규 플러그인 등록, version 6.1.0 → 6.2.0
- www 카탈로그(있을 시) 동기화
- 본 설계서 + `expert-plugin-expansion-plan` HTML 갱신(선택)

---

## 6. 이관 순서 + 검증 게이트

이관은 의존성이 가장 낮은 것부터 순차 실행(각 단계 독립 게이트 통과 후 다음).

### 순서
1. **A-2 rename** (korean-spell-check) — 가장 작음, 독립
2. **B moai-story** — writer 내부 종속, writer 단독 영향
3. **D moai-media** — marketer 내부 종속, marketer 단독 영향
4. **C-1 moai-analyst + C-2** — officer 영향, 가장 많은 스킬 이동

### 게이트 (각 단계마다 4중, 기존 계획서 §09 재사용)
1. 스킬 로드 스모크 — 신규 플러그인 skills/ 전수 SKILL.md 파싱
2. 에이전트 스폰 카나리아 — worker + auditor 정상 기동
3. cross-reference grep 0건 — 기존 플러그인에 이관 스킬 잔류 참조 없음
4. `marketplace.json` validate — 구성 정합

### 후행
- 4단계 전부 완료 후 marketplace version 6.2.0 범프
- www 카탈로그 동기화
- HTML 보고서 v6.2 반영

---

## 7. 위험 및 완화

| 위험 | 완화 |
|---|---|
| story/media 스킬이 타 플러그인과 기능 중복(예: media vs marketer 썸네일) | 경계 계약 문서화 (design-system-library 포인터 패턴 참고) |
| rename(korean-spell-check) 시 기존 참조 깨짐 | writer 내부 10건 사전 grep → 일괄 치환 → 게이트 #3 검증 |
| C-2 라이프스타일 7개 독립 플러그인 과소 | C-2a(coworker 회수) 권장 — 직원 수 억제 |
| 분리 후 pm 라우팅 플래그 폭증 | 플래그 → 카테고리 매핑 테이블로 관리(pm 스킬 갱신) |
| 일괄 실행 시 장애 범위 확대 | 4단계 순차 실행 + 단계별 게이트로 부분 합격 허용 |

---

## 8. 결정 대기 항목 (사용자)

1. **실행 범위**: B/C/D 전체 실행 vs 일부만
2. **C-2 선택**: C-2a(coworker 회수, 권장) vs C-2b(moai-life 신설)
3. **A-2 rename**: 진행 vs 유지
4. **실행 주체**: 위임(manager-develop/builder-harness) vs 오케스트레이터 직접 — 다수 파일 생성(플러그인 3개×구조)이므로 **위임 권장**
5. **HTML 보고서 갱신**: 본 설계 v6.2 반영 여부

> 본 설계서는 실행 전 결정용. 승인 후 위임으로 이관 실행 → 게이트 검증 → v6.2 마무리.
