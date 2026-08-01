---
id: SPEC-MOC-PLUGIN-STORY-001
title: "moai-story 플러그인 신설 + 패밀리 v4 재배치"
version: "0.1.0"
status: superseded
created: 2026-07-06
updated: 2026-07-09
author: GOOS
priority: P1
phase: "v4.0.0"
module: "plugins/moai-story"
lifecycle: spec-anchored
tags: "plugin,story,higgsfield,cowork,v4"
depends_on: ["SPEC-MOC-FAMILY-DRIFT-001"]
---

# SPEC-MOC-PLUGIN-STORY-001: moai-story 플러그인 신설 + 패밀리 v4 재배치

> **Tier**: L (Large)
> **Complexity**: 신규 플러그인 1개(21스킬) + 기존 플러그인 1개 메이저 업데이트 + marketplace 4엔트리 + 문서 갱신
> **Design Source**: [05-family-redesign-v2.md](../../../docs/plugin-family-design/05-family-redesign-v2.md) §3 moai-story 플러그인 설계
> **Predecessor**: SPEC-MOC-FAMILY-DRIFT-001 (기반 정리 완료 후 진입)

---

## 1. 개요 (Overview)

### 1.1 배경

**작가 도메인 공백 해소**: cowork 179개 스킬 전수 스캔 결과, 창작 영역은 출판 파이프라인(`book-*` 8종)만 존재한다. 웹툰·웹소설·시나리오·콘티 영역이 완전히 비어 있다.

**Higgsfield 생태계 성숙**: 공식 호스티드 MCP(`mcp.higgsfield.ai`)가 존재하고, 웹툰(AI Anime Generator + Soul ID) · 콘티(Popcorn/Shots) · 시네마틱(DoP + Cinema Studio 3.5) · 광고(Marketing Studio/Ads 2.0) 등 작가 용도별 모델이 정확히 매핑된다.

**청중 분리 원칙**: 작가는 실무자·디자이너·개발자와 구분되는 네 번째 청중이다. 단일 전담 플러그인(moai-story)으로 네임스페이스·독립 활성화·독립 버저닝·독립 릴리스를 제공한다.

### 1.2 목표

1. **moai-story 플러그인 신설**: 21스킬(이관 8 + 신규 13) + Higgsfield MCP 연동
2. **cowork v4.0.0 마이그레이션**: book-* 8스킬 제거 + higgsfield MCP 제거 + 메이저 범프
3. **`.claude-plugin/marketplace.json` 갱신**: 4플러그인 엔트리 최신화
4. **www 문서 갱신**: 패밀리 4플러그인 구성 + 마이그레이션 안내

### Out of Scope — sibling plugin internals

- moai-design · moai-code의 내부 변경 없음 (위생 스윕만은 DRIFT-001에서 이미 수행 예정)

### Out of Scope — Higgsfield MCP self-vendoring

- 공식 호스티드 MCP 채택, 자체 벤더링은 향후 전환 경로로만 문서화 (본 SPEC 구현 범위 아님)

### Out of Scope — cowork split

- 공식 문서상 기술적 근거 없음, `claude plugin details` 실측 후 재판단

---

## 2. REQUIREMENTS (GEARS)

### REQ-STORY-001: moai-story 플러그인 구조

**The plugin SHALL** provide the following structure:

- **plugin.json**: `name: "story"`, `displayName: "MoAI Story"`, `version: "0.1.0"`, `category: "작가·콘텐츠"`, `author: "modu-ai"`
- **설명**: "작가와 콘텐츠 비즈니스를 위한 플러그인 — 출판 기획·집필부터 웹툰·웹소설·드라마/영화 시나리오·광고/영상 콘티까지. Higgsfield 최신 모델로 캐릭터 일관성 작화·콘티·프리비즈를 생성."
- **디렉토리 구조**: `plugins/moai-story/` = `.claude-plugin/plugin.json` + `.mcp.json` + `skills/` (cowork와 같은 스킬 중심 구조)

**Rationale**: 스킬 중심 구조는 cowork와의 일관성을 유지하고, 에이전트/명령 파일이 없으므로 진입점도 스킬이 담당한다.

### REQ-STORY-002: 이관 스킬 8종 (cowork → story)

**The plugin SHALL** migrate the following 8 book-* skills from cowork preserving the chain:

1. `book-concept-planner`
2. `book-target-reader`
3. `book-outline-designer`
4. `book-chapter-writer`
5. `book-revision-coach`
6. `book-author-bio`
7. `book-proposal-writer`
8. `book-publisher-matcher`

**The plugin SHALL** modify `book-revision-coach` to fallback to own revision procedure when cowork is not installed (sole body text change required for this skill).

**Rationale**: 출판 파이프라인 체인을 보존하고, story 단독 설치 사용자를 위한 폴백을 제공한다.

### REQ-STORY-003: 신규 스킬 13종 (story-*)

**The plugin SHALL** provide the following 13 new story-* skills:

| # | 스킬 | 영역 | Higgsfield |
|---|------|------|:---:|
| 1 | `story-project` | 진입점 — 작품 유형 파악 → 장르 파이프라인 라우팅 | — |
| 2 | `story-webtoon-planner` | 웹툰 기획: 세계관·캐릭터·시즌/회차·플랫폼 문법 | — |
| 3 | `story-webtoon-episode` | 웹툰 회차 대본: 컷 분할·대사·연출·말칸 | — |
| 4 | `story-webtoon-art` | 웹툰 작화: 패널 이미지, 캐릭터 일관성 | ✅ |
| 5 | `story-webnovel-writer` | 웹소설 연재: 플랫폼 문법·절단 설계 | — |
| 6 | `story-synopsis` | 시놉시스: 로그라인·기획의도·인물·회차 구성 | — |
| 7 | `story-screenplay` | 시나리오: 씬 넘버·지문·대사, 표준 포맷 | — |
| 8 | `story-conti` | 콘티/스토리보드: 씬 → 프레임 시퀀스 | ✅ |
| 9 | `story-ad-conti` | 광고 콘티: 제품/브랜드 스토리보드 | ✅ |
| 10 | `story-character-sheet` | 캐릭터 시트: 설정 + 비주얼 + Soul ID 훈련 | ✅ |
| 11 | `story-cover-art` | 표지/일러스트: 인쇄 해상도 | ✅ |
| 12 | `story-previz` | 시네마틱 프리비즈: 카메라 무빙 | ✅ |
| 13 | `story-ip-pitch` | IP 사업화: 피칭 문서·판권 제안 | — |

**Rationale**: 7종 텍스트 스킬은 Higgsfield 없이 완결 동작하고, 6종 생성형 스킬은 MCP 연동 시에만 생성 실행한다 (7 + 6 = 13종 신규 스킬 정합).

### REQ-STORY-004: Higgsfield MCP 연동

**The plugin SHALL** configure `.mcp.json` as follows:

```json
{
  "mcpServers": {
    "higgsfield": {
      "type": "url",
      "url": "https://mcp.higgsfield.ai/mcp",
      "timeout": 120000,
      "headers": { "User-Agent": "MoAI-Story/0.1.0" }
    }
  }
}
```

**The plugin SHALL** use OAuth authentication (one-time via Claude connector, no API key management).

**The plugin SHALL** provide prompt-only fallback when MCP is disconnected: output complete prompt for Higgsfield web paste (cowork media-* pattern).

**The plugin SHALL** embed model routing table in generation skill bodies:

| 용도 | 1순위 모델 |
|------|-----------|
| 웹툰/만화 패널 | AI Anime Generator + Soul ID |
| 콘티 프레임 시퀀스 | Popcorn (8프레임) |
| 멀티 앵글 탐색 | Shots (9앵글 그리드) |
| 광고 콘티/영상 | Marketing Studio · Ads 2.0 · Seedance 2.0 |
| 캐릭터 일관성 | Soul ID |
| 표지/일러스트 | Soul 2.0 (+ 업스케일) |
| 시네마틱 프리비즈 | DoP + Cinema Studio 3.5 |

**Rationale**: OAuth는 자격증명을 Higgsfield 서버에 보관하여 API 키 관리 불필요, MCP 미연결 시 프롬프트 온리 폴백으로 사용성 확보.

### REQ-STORY-005: 크레딧 고지 의무화

**The plugin SHALL** mandate pre-generation credit estimate + user confirmation in all 6 generation skill bodies (story-webtoon-art, story-conti, story-ad-conti, story-character-sheet, story-cover-art, story-previz).

**Rationale**: 사용자의 Higgsfield 크레딧 소진(이미지 2크레딧~, 영상 수십 크레딧)을 사전에 고지하여 예상치 지출 방지.

### REQ-STORY-006: cowork v4.0.0 마이그레이션

**cowork plugin SHALL** update to version 4.0.0 with the following changes:

1. **스킬 제거**: Remove book-* 8 skills (179 → 171 skills)
2. **MCP 제거**: Remove higgsfield entry from `.mcp.json` (9 → 8 servers)
3. **버전 범프**: 3.0.0 → 4.0.0 (skill removal = breaking, semver major)
4. **3점 동기화**: plugin.json 4.0.0 = all 171 skills SKILL.md 4.0.0 (marketplace plugin entry는 version 미기재 per NFR-STORY-003; marketplace catalog `metadata.version`만 3.0.0 → 4.0.0 승격)
5. **공지**: CHANGELOG + www docs with "publication/creative skills moved to moai-story, install with `/plugin install story`" migration guide

**Rationale**: book-* 이관은 breaking change이므로 메이저 범프가 필요하고, 3점 동기화 HARD 규칙을 준수한다.

### REQ-STORY-007: `.claude-plugin/marketplace.json` 4엔트리 갱신

**The `.claude-plugin/marketplace.json` SHALL** update all 4 plugin entries after story creation. Plugin entries carry `{name, source, description, displayName, category}` ONLY — NO `version` field per plugin entry (per NFR-STORY-003 / DRIFT-001 D14). Catalog-level `metadata.version` bumps `3.0.0 → 4.0.0` as the single version-advancement signal.

| 플러그인 엔트리 name | 스킬 | MCP | 비고 |
|---------|:---:|:---:|-----|
| moai-cowork | 171 | 8 | v4.0.0 breaking (book-* 이관) |
| moai-code | unchanged | unchanged | 기존 유지 |
| moai-design | unchanged | unchanged | 기존 유지 |
| moai-story | 21 | 1 | 신규 추가 |

**Rationale**: 패밀리 구성 변경(4플러그인)을 marketplace 메타데이터에 반영한다. plugin entry의 `version` 필드는 이중 기재 함정(공식 문서화된 `metadata.version` 단일 지점 정책)이므로 기재하지 않는다.

### REQ-STORY-008: www 문서 갱신

**The www documentation SHALL** update plugin family documentation with:

1. 4 plugins overview (new moai-story added)
2. cowork v4.0.0 migration guide
3. story installation guide (`/plugin install story`)
4. Higgsfield OAuth setup guide

**Rationale**: 사용자에게 패밀리 구성 변경과 마이그레이션 경로를 안내한다.

### REQ-STORY-009: 스킬 위생 기준 준수

**All 21 skills SHALL** comply with official hygiene standards:

- 3인칭 관점
- "무엇을/언제" 명시
- 한국어 트리거 용어
- SKILL.md < 500줄
- 참조 1단계 준수

**Rationale**: 진행 중인 한국어 슬롭 전수조사(`project_plugin_korean_slop_audit.md` P0~P4)와 통합 실행하여 중복 스윕을 방지한다. 동 조사에서 열거된 P0 반패턴을 스킬 본문 위생의 기준선으로 삼는다: (a) 1인칭 화법(`저는~`, `제가~`, `우리는~`, `내가~`), (b) AI-tell 문구(`종합적으로 볼 때`, `한 가지 분명한 것은`, `핵심적인 점은`), (c) 미번역 영어 누수(untranslated English leak). 각 스킬 SKILL.md는 이 기준선 3종에 대해 기계적 grep 검증 0 매치를 만족해야 한다.

---

## 3. Non-Functional Requirements

### NFR-STORY-001: 토큰 비용 제어

MCP 지연 로딩으로 토큰 비용을 완화하며, MCP를 story 플러그인에만 배선하여 비용 부담을 story 설치자로 한정한다.

### NFR-STORY-002: MCP 미연결 폴백

MCP 미연결 시 프롬프트 온리 모드로 강등되어 완결 동작을 보장한다.

### NFR-STORY-003: 버전 정책 준수

plugin.json 단일 지점에 버전을 명시하고, marketplace entry에는 version을 기재하지 않는다 (공식 문서화된 이중 기재 함정 회피, DRIFT-001 D14 확정).

---

## 4. Dependencies

| SPEC | 관계 | 상태 |
|------|------|------|
| SPEC-MOC-FAMILY-DRIFT-001 | 선행 | `in-progress` 이상이면 진입 허용. sync-phase는 untracked-edits 정책으로 의도적 생략(DRIFT-001 `status: completed` 전환 없음). M0 게이트는 `grep '^status:' ... → in-progress OR completed`로 허용. |

---

## 5. Risks & Mitigations

| Risk | 영향 | 완화 대책 |
|------|------|----------|
| Higgsfield rate limit 미문서화 | 생성 지연 | 방어적 재시도 안내를 스킬 본문에 의무화 |
| Higgsfield 도구 표면 변경 | 모델 탐색 실패 | 모델명 하드코딩 대신 "용도 기술 → 도구 탐색" 방식으로 서술 |
| 서드파티 모델 수급 변동 (예: Sora 2) | 라우팅 실패 | 라우팅 표에서 1순위 배제하고 대안 안내 |

---

## HISTORY

- **0.1.0** (2026-07-06): 최초 작성 — Tier L plan-phase 산출물 4종 (spec/plan/acceptance/design) 작성 완료. 설계 정본 `docs/plugin-family-design/05-family-redesign-v2.md` §3 기반.
- **0.1.0 (rev 2026-07-07)**: plan-auditor iter-1 FAIL (score 0.73, Tier L threshold 0.85) 차단 — 14 audit defects (3 BLOCKING + 7 SHOULD-FIX + 4 MINOR) 정정. 주요 정정: (1) marketplace plugin entry `version` 필드 제거(D1, NFR-STORY-003 정합), (2) 생성형 스킬 수 5→6 정정(D2), (3) M0 게이트 DRIFT-001 `in-progress` 허용(D3), (4) plugin name `moai-X` 정규화(D4), (5) `.claude-plugin/marketplace.json` 경로 정정(D5), (6) cowork 스킬 수 177/169 → 179/171 정정(D6), (7) `.mcp.json` 단일 canonical shape로 통일(D7), (8) 위생 AC 기계적 grep 패턴화(D8), (9) NFR-STORY-001 AC 추가(D9), (10) AC-STORY-006 grep 구문 수정(D10), (11) M6 완료 조건 구체화(D11), (12) Out of Scope canonical H3 + HISTORY 섹션 추가(D12), (13) REQ-STORY-009 Korean-slop baseline 명시(D13), (14) `author: "modu-ai"` REQ-STORY-001에 추가(D14).
