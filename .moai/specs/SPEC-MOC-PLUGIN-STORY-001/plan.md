---
id: SPEC-MOC-PLUGIN-STORY-001
title: "moai-story 플러그인 신설 + 패밀리 v4 재배치"
version: "0.1.0"
status: in-progress
created: 2026-07-06
updated: 2026-07-07
author: GOOS
priority: P1
phase: "v4.0.0"
module: "plugins/moai-story"
lifecycle: spec-anchored
tags: "plugin,story,higgsfield,cowork,v4"
depends_on: ["SPEC-MOC-FAMILY-DRIFT-001"]
---

# IMPLEMENTATION PLAN

## Milestone Overview (Tier L)

| Milestone | 목표 | 주요 작업 | Est. Files |
|-----------|------|-----------|------------|
| M0 | Pre-flight | DRIFT-001 완료 확인, precond verify | — |
| M1 | moai-story 스캐폴딩 | plugin.json + .mcp.json + skills/ 디렉토리 구조 | 3 |
| M2 | 이관 스킬 8종 복사 | cowork book-* → story 이관 + book-revision-coach 폴백 수정 | 8 |
| M3 | 신규 스킬 13종 작성 | story-project + story-webtoon-* 5종 + story-* 7종 | 13 |
| M4 | cowork v4.0.0 마이그레이션 | 스킬 제거 + MCP 제거 + 버전 범프 + 3점 동기화 | plugin.json + .mcp.json |
| M5 | `.claude-plugin/marketplace.json` 갱신 | 4엔트리 최신화 | 1 |
| M6 | www 문서 갱신 | 패밀리 개요 + 마이그레이션 가이드 + Higgsfield OAuth | 3~5 |

---

## M0: Pre-flight Verification

**목표**: DRIFT-001 run-phase 완료 상태 확인 및 사전 전제 검증

### 작업 항목

- [ ] DRIFT-001 spec.md status가 `in-progress` OR `completed`인지 확인 (sync-phase는 untracked-edits 정책으로 의도적 생략됨 — `completed` 요구 불필요)
- [ ] Git 상태 정상 (0 0 divergence) 확인
- [ ] `.claude-plugin/marketplace.json` 현재 상태 백업

### 검증 명령어

```bash
grep '^status:' .moai/specs/SPEC-MOC-FAMILY-DRIFT-001/spec.md
git rev-list --count --left-right origin/main...HEAD
cp .claude-plugin/marketplace.json .claude-plugin/marketplace.json.backup
```

### 완료 조건

- DRIFT-001 run-phase complete (`status: in-progress` 이상; sync-phase는 untracked-edits 정책으로 의도적 생략)
- Git clean 상태
- 백업 완료

---

## M1: moai-story 플러그인 스캐폴딩

**목표**: moai-story 플러그인의 기본 구조 생성

### 작업 항목

- [ ] `plugins/moai-story/.claude-plugin/plugin.json` 생성
  - name: "story"
  - displayName: "MoAI Story"
  - version: "0.1.0"
  - category: "작가·콘텐츠"
  - description: 설계 §3.1 명시
- [ ] `plugins/moai-story/.mcp.json` 생성
  - higgsfield 서버: https://mcp.higgsfield.ai/mcp
- [ ] `plugins/moai-story/skills/` 디렉토리 생성
- [ ] `plugins/moai-story/.claudeignore` 생성 (cowork 참조)

### 파일 구조

```
plugins/moai-story/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── .claudeignore
└── skills/
    ├── story-project/
    ├── book-concept-planner/     # M2에서 이관
    └── ...
```

### 완료 조건

- plugin.json 유효성 (`claude plugin validate plugins/moai-story`)
- .mcp.json 형식 검증
- skills/ 디렉토리 존재

---

## M2: 이관 스킬 8종 복사 (cowork → story)

**목표**: cowork의 book-* 8스킬을 story로 이관

### 작업 항목

- [ ] `plugins/moai-cowork/skills/book-concept-planner/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-target-reader/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-outline-designer/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-chapter-writer/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-revision-coach/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-author-bio/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-proposal-writer/` → `plugins/moai-story/skills/`
- [ ] `plugins/moai-cowork/skills/book-publisher-matcher/` → `plugins/moai-story/skills/`
- [ ] `book-revision-coach/SKILL.md` 수정: cowork 미설치 시 폴백 절차 추가

### 폴백 절차 (book-revision-coach)

SKILL.md에 다음 내용 추가:

> **참고**: moai-cowork 플러그인이 설치된 경우 `office-korean-spell-check` → `general-humanize-korean` → `general-ai-slop-reviewer` 체인을 자동 연계합니다. 미설치 시 본 스킬의 자체 퇴고 절차를 따릅니다.

### 완료 조건

- 8개 스킬 디렉토리 복사 완료
- 각 스킬의 SKILL.md 존재
- book-revision-coach 폴백 안내 추가됨

---

## M3: 신규 스킬 13종 작성

**목표**: story-* 신규 스킬 13종 작성

### M3-A: 진입점 (1종)

- [ ] `story-project/` — 작품 유형 파악 → 장르 파이프라인 라우팅 (cowork /project 패턴)

### M3-B: 웹툰 영역 (3종)

- [ ] `story-webtoon-planner/` — 세계관·캐릭터·시즌/회차·플랫폼 문법
- [ ] `story-webtoon-episode/` — 컷 분할·대사·연출·말칸 배치
- [ ] `story-webtoon-art/` — 패널 이미지 (Higgsfield: AI Anime Generator + Soul ID, 크레딧 고지 포함)

### M3-C: 웹소설 영역 (1종)

- [ ] `story-webnovel-writer/` — 연재 집필, 플랫폼 문법(문피아/카카오페이지), 절단 설계

### M3-D: 시나리오 영역 (2종)

- [ ] `story-synopsis/` — 로그라인·기획의도·인물소개·회차/막 구성
- [ ] `story-screenplay/` — 씬 넘버·지문·대사, 한국 방송/영화 표준 포맷

### M3-E: 콘티 영역 (2종)

- [ ] `story-conti/` — 씬 → 프레임 시퀀스 (Higgsfield: Popcorn/Shots, 크레딧 고지 포함)
- [ ] `story-ad-conti/` — 제품/브랜드 광고 스토리보드 (Higgsfield: Marketing Studio/Ads 2.0, 크레딧 고지 포함)

### M3-F: 캐릭터/일러스트 영역 (2종)

- [ ] `story-character-sheet/` — 설정 + 비주얼 + Soul ID 훈련 가이드 (Higgsfield: Soul ID, 크레딧 고지 포함)
- [ ] `story-cover-art/` — 표지/일러스트 (Higgsfield: Soul 2.0 + 업스케일, 크레딧 고지 포함)

### M3-G: 프리비즈/사업화 영역 (2종)

- [ ] `story-previz/` — 카메라 무빙 지정 숏 (Higgsfield: DoP + Cinema Studio 3.5, 크레딧 고지 포함)
- [ ] `story-ip-pitch/` — 피칭 문서, 판권/2차 저작 제안서

### 각 스킬 구조

```
story-*/
├── SKILL.md          # 3인칭, 무엇을/언제, 한국어 트리거, < 500줄
└── skill.yaml         # name, description, triggers (ko)
```

### 위생 기준 준수 확인사항

- [ ] 3인칭 관점 ("당신은...~합니다")
- [ ] "무엇을/언제" 명시
- [ ] 한국어 트리거 용어 포함
- [ ] SKILL.md < 500줄
- [ ] 참조 1단계 준수

### 완료 조건

- 13개 스킬 디렉토리 생성 완료
- 각 스킬 SKILL.md 작성 완료
- 위생 기준 모두 통과

---

## M4: cowork v4.0.0 마이그레이션

**목표**: cowork에서 story로의 이관을 반영한 v4.0.0 릴리스

### 작업 항목

- [ ] `plugins/moai-cowork/skills/`에서 book-* 8종 제거 (179 → 171 skills)
- [ ] `plugins/moai-cowork/.mcp.json`에서 higgsfield 엔트리 제거 (9 → 8 servers)
- [ ] `plugins/moai-cowork/.claude-plugin/plugin.json` 업데이트
  - version: "3.0.0" → "4.0.0"
  - description: book-* 이관 안내 추가
- [ ] cowork 스킬 171종 각 SKILL.md version 업데이트 to "4.0.0"
- [ ] `plugins/moai-cowork/CHANGELOG.md`에 v4.0.0 섹션 추가
  - book-* 스킬 moai-story로 이관 안내
  - `/plugin install story` 마이그레이션 가이드

### 버전 3점 동기화 확인

```bash
# plugin.json 버전
grep '"version"' plugins/moai-cowork/.claude-plugin/plugin.json

# 스킬 버전 일괄 확인
grep -h '"version":' plugins/moai-cowork/skills/*/SKILL.md | sort | uniq -c
```

### 완료 조건

- plugin.json version: 4.0.0
- 171개 스킬 모두 SKILL.md version: 4.0.0
- .mcp.json에서 higgsfield 제거됨
- CHANGELOG.md 업데이트됨

---

## M5: `.claude-plugin/marketplace.json` 4엔트리 갱신

**목표**: marketplace 메타데이터를 패밀리 v4 구성으로 최신화

### 작업 항목

- [ ] `.claude-plugin/marketplace.json` 백업 (이미 M0에서 수행)
- [ ] `metadata.version` 범프: `"3.0.0" → "4.0.0"` (catalog 단일 version 지점 — plugin entry 자체는 version 미기재 per NFR-STORY-003 / DRIFT-001 D14)
- [ ] moai-cowork 엔트리 업데이트
  - description: 171 skills + migration guide (version은 plugin.json에만 존재)
- [ ] moai-story 엔트리 추가 (신규 4번째)
  - name: "moai-story"
  - source: "./plugins/moai-story"
  - displayName: "MoAI Story"
  - description: 21 skills + Higgsfield integration
  - category: "작가·콘텐츠"
- [ ] moai-design / moai-code 엔트리 확인 (변경 없음, 단 name이 정확히 `moai-design` / `moai-code`인지 실측)

### `.claude-plugin/marketplace.json` 구조 (canonical 4엔트리 — version 필드 없음)

```json
{
  "name": "moai-claude",
  "metadata": {
    "version": "4.0.0",
    ...
  },
  "plugins": [
    {
      "name": "moai-cowork",
      "source": "./plugins/moai-cowork",
      "displayName": "MoAI Cowork",
      "category": "통합·올인원",
      "description": "171 skills — /project natural-language routing. Publication skills (book-*) moved to moai-story v4.0.0; install with `/plugin install story`."
    },
    {
      "name": "moai-code",
      "source": "./plugins/moai-code",
      "displayName": "MoAI Code",
      "category": "개발·무설치",
      "description": "..."
    },
    {
      "name": "moai-design",
      "source": "./plugins/moai-design",
      "displayName": "MoAI Design",
      "category": "디자인",
      "description": "..."
    },
    {
      "name": "moai-story",
      "source": "./plugins/moai-story",
      "displayName": "MoAI Story",
      "category": "작가·콘텐츠",
      "description": "21 skills for writers and content creators — /story:* for genre pipeline. Higgsfield MCP integration for webtoon, continuity, and cinematic previz."
    }
  ]
}
```

### 완료 조건

- `.claude-plugin/marketplace.json` 유효성 (`claude plugin validate . --strict`)
- `jq '.plugins | length'` 출력 4
- `jq '.plugins[].version'` 출력이 모두 `null` (plugin entry version 미기재 — D1 정합)
- `jq '.metadata.version'` 출력이 `"4.0.0"`
- canonical re-index: `[0]=moai-cowork, [1]=moai-code, [2]=moai-design, [3]=moai-story`

---

## M6: www 문서 갱신

**목표**: 패밀리 v4 구성과 마이그레이션 경로를 문서화

### 작업 항목

- [ ] `www/plugins/index.md` 업데이트
  - 4 플러그인 개요 (moai-story 추가)
  - 각 플러그인 대상 청중 명시
- [ ] `www/plugins/migration.md` 생성 (또는 기존 파일 업데이트)
  - cowork v4.0.0 마이그레이션 가이드
  - `/plugin install story` 설치 안내
  - book-* 스킬 사용자 액션 플랜
- [ ] `www/plugins/higgsfield-setup.md` 생성
  - OAuth 1회 인증 절차
  - Claude 커넥터 설정 방법
  - 크레딧 소진 안내
- [ ] `www/CHANGELOG.md`에 v4.0.0 섹션 추가
  - moai-story 신설
  - cowork v4.0.0 breaking change

### 마이그레이션 가이드 내용

```markdown
# Cowork v4.0.0 Migration Guide

v4.0.0에서 publication/creative skills (book-*)가 moai-story 플러그인으로 이관되었습니다.

## 영향 범위

- 제거된 스킬: book-concept-planner, book-target-reader, book-outline-designer, book-chapter-writer, book-revision-coach, book-author-bio, book-proposal-writer, book-publisher-matcher (8종)
- cowork 스킬 수: 179 → 171

## 마이그레이션 절차

1. moai-story 플러그인 설치
   ```
   /plugin install story
   ```

2. Higgsfield OAuth 1회 인증 (생성형 스킬 사용 시)

3. 기존 book-* 스킬은 story에서 동일하게 사용 가능
```

### 완료 조건

- www 문서 Hugo 빌드 성공 (`cd www && npm run build` exit 0)
- 링크 깨짐 없음 (`find www/public -name '*.html' | xargs grep -l 'class="dead-link"'` 결과 0건)
- 문서 정확성 기계적 체크:
  - `grep -c '^## ' www/plugins/index.md` ≥ 4 (4플러그인 섹션 존재)
  - `grep -F '/plugin install story' www/plugins/migration.md` 매치 1건 이상 (마이그레이션 안내 존재)
  - `grep -F 'OAuth' www/plugins/higgsfield-setup.md` 매치 1건 이상 (OAuth 인증 절차 존재)
  - `ls www/plugins/migration.md www/plugins/higgsfield-setup.md www/CHANGELOG.md` 3파일 존재

---

## Post-Implementation

### 검증 명령어

```bash
# 플러그인 유효성 검증
claude plugin validate . --strict

# 스킬 카운트 확인
find plugins/moai-story/skills -type d -mindepth 1 -maxdepth 1 | wc -l   # 21
find plugins/moai-cowork/skills -type d -mindepth 1 -maxdepth 1 | wc -l  # 171

# 3점 동기화 확인 (plugin.json + SKILL.md; marketplace entry는 version 미기재 per D14)
grep '"version":"4.0.0"' plugins/moai-cowork/.claude-plugin/plugin.json
grep -c '"version":"4.0.0"' plugins/moai-cowork/skills/*/SKILL.md

# .claude-plugin/marketplace.json 검증
cat .claude-plugin/marketplace.json | jq '.plugins | length'  # 4
jq '.plugins[].version' .claude-plugin/marketplace.json       # all null (per D1)
jq '.metadata.version' .claude-plugin/marketplace.json        # "4.0.0"

# Hugo 빌드 확인
cd www && npm run build
```

### 릴리스 체크리스트

- [ ] moai-story plugin.json 유효
- [ ] moai-story .mcp.json 형식 검증
- [ ] 21개 story 스킬 위생 기준 통과
- [ ] book-* 8스킬 이관 완료
- [ ] book-revision-coach 폴백 안내 추가됨
- [ ] cowork v4.0.0 3점 동기화 완료
- [ ] cowork higgsfield MCP 제거됨
- [ ] `.claude-plugin/marketplace.json` 4엔트리 정합
- [ ] www 문서 빌드 성공
- [ ] CHANGELOG 업데이트됨

---

## Estimated Complexity

- M0: Trivial (verification only)
- M1: Low (scaffolding, ~3 files)
- M2: Low (copy 8 directories, 1 text edit)
- M3: High (13 skills × ~200 lines each = ~2,600 lines)
- M4: Medium (version bump + sync + changelog)
- M5: Medium (marketplace 4 entries)
- M6: Medium (www docs ~3-5 files)

**Total Est. Files Modified/Created**: ~30-40 files
