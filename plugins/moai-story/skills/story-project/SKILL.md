---
name: story-project
description: |
  작품 유형을 파악해 웹툰·웹소설·영상(시놉시스·시나리오·콘티·프리비즈)·표지·IP 사업화 파이프라인으로 라우팅하는 moai-story 플러그인의 진입점 스킬. 사용자의 한마디 요청에서 장르를 분류해 알맞은 story-* 스킬 체인으로 안내한다. 출판 도서는 moai-writer로 분기한다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "웹툰 기획할래", "웹소설 연재하고 싶어"
  - "시나리오 작성", "시놉시스 써줘"
  - "콘티 만들어줘", "광고 스토리보드"
  - "캐릭터 시트", "책 표지 일러스트"
  - "프리비즈", "IP 피칭 문서"
version: "1.1.1"
---

# story-project

> moai-story 플러그인의 진입점. 사용자의 작품 의도를 분류해 알맞은 장르 파이프라인으로 라우팅한다. 어떤 스킬을 언제 호출할지 결정하는 라우터 역할을 수행한다.

## 1. 개요

사용자가 "작품을 만들고 싶다"고 할 때 가장 먼저 정할 것은 **무엇을 만들 것인가**이다. 이 스킬은 그 의도를 분류한 뒤 알맞은 story-* 스킬 체인으로 안내한다. 슬래시 명령 없이 자연어 요청만으로 라우팅이 동작한다.

## 2. 라우팅 로직

사용자 입력을 분류해 다음 파이프라인으로 안내한다. '소속 플러그인' 열은 진입 스킬이 어느 플러그인에 있는지를 나타낸다.

| 입력 의도 | 진입 스킬 | 소속 플러그인 | 후속 체인 |
|-----------|-----------|--------------|----------|
| 웹툰 기획·연재 | `story-webtoon-planner` | moai-story | → `story-character-sheet` → `story-webtoon-episode` → `story-webtoon-lettering` → `story-webtoon-art` → `story-webtoon-qc` |
| 웹소설 연재 | `story-webnovel-planner` | moai-story | → `story-webnovel-writer` |
| 드라마/영화 영상 | `story-synopsis` | moai-story | → `story-screenplay` → `story-conti` → `story-previz` |
| 광고 영상 | `story-conti` | moai-story | (광고 콘티 프리셋 내장) → `story-previz` |
| 표지·일러스트 | `story-cover-art` | moai-story | (단일) |
| IP 사업화·판권 | `story-ip-pitch` | moai-story | (단일) |
| 출판 도서 | `moai-writer:book-concept-planner` | moai-writer | moai-writer 미설치 시 Plugins에서 `moai-writer` Install(또는 `claude/codex plugin install moai-writer@moai-cowork`) 안내 후 진행 |

**규격·연재 관리 참조 (진입점이 아닌 상시 참조 허브):**

- 한국 웹툰 플랫폼 규격 문의(원고 규격·데뷔 경로·회차 분량 등) → `story-webtoon-spec`
- 다회차 연재 상태 관리(마스터 기획서·에피소드 현황표) → `story-series-bible`

**후속 검수 체인 (모든 산출물 공통):**

- AI 티 제거 검수 → `moai-coworker:ai-slop-reviewer` → `moai-writer:korean-humanize`

## 3. 워크플로우

### Step 1: 의도 분류
사용자 요청에서 장르 신호 키워드를 추출한다.

### Step 2: 확인
"선택하신 영역은 X입니다. Y 스킬로 진행합니다."로 의도를 확인한다.

### Step 3: 라우팅
알맞은 진입 스킬을 호출하고, 후속 체인을 순차 안내한다.

## 4. 주의사항

- 이미지 생성이 필요한 스킬(webtoon-art·conti·character-sheet·cover-art·previz)은 생성 실행·크레딧·모델 선택을 `moai-media`에 위임한다. 실행 전 사전 크레딧 고지가 선행된다.
- 한 요청에 두 영역이 섞이면 우선순위를 묻고 한쪽씩 진행한다.
- 출판 도서(book-*)는 moai-story가 아니라 `moai-writer` 소관이다. 미설치 시 설치를 안내한다.

## 5. 관련 스킬

- 전체 story-* 스킬 (위 라우팅 표 참조)
- 규격 SSOT: `story-webtoon-spec` · 연재 원장: `story-series-bible`
- 출판 도서: `moai-writer:book-concept-planner` 외 book-* 계열
