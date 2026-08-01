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

# ACCEPTANCE CRITERIA

## AC-STORY-001: moai-story 플러그인 구조

**Given**: moai-story 플러그인 디렉토리가 생성됨

**When**: plugin.json과 .mcp.json이 작성됨

**Then**:

- [ ] `plugins/moai-story/.claude-plugin/plugin.json` 존재
- [ ] plugin.json에 `name: "story"` 포함
- [ ] plugin.json에 `displayName: "MoAI Story"` 포함
- [ ] plugin.json에 `version: "0.1.0"` 포함
- [ ] plugin.json에 `category: "작가·콘텐츠"` 포함
- [ ] plugin.json description에 "작가와 콘텐츠 비즈니스를 위한 플러그인" 포함
- [ ] `plugins/moai-story/.mcp.json` 존재
- [ ] .mcp.json에 higgsfield 서버 URL `https://mcp.higgsfield.ai/mcp` 포함
- [ ] `plugins/moai-story/skills/` 디렉토리 존재
- [ ] `claude plugin validate plugins/moai-story` 통과

---

## AC-STORY-002: 이관 스킬 8종 (cowork → story)

**Given**: cowork 플러그인에 book-* 8스킬이 존재함

**When**: 이관 작업이 수행됨

**Then**:

- [ ] `plugins/moai-story/skills/book-concept-planner/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-target-reader/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-outline-designer/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-chapter-writer/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-revision-coach/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-author-bio/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-proposal-writer/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/book-publisher-matcher/SKILL.md` 존재
- [ ] `plugins/moai-cowork/skills/book-concept-planner/` 부재
- [ ] `plugins/moai-cowork/skills/book-target-reader/` 부재
- [ ] `plugins/moai-cowork/skills/book-outline-designer/` 부재
- [ ] `plugins/moai-cowork/skills/book-chapter-writer/` 부재
- [ ] `plugins/moai-cowork/skills/book-revision-coach/` 부재
- [ ] `plugins/moai-cowork/skills/book-author-bio/` 부재
- [ ] `plugins/moai-cowork/skills/book-proposal-writer/` 부재
- [ ] `plugins/moai-cowork/skills/book-publisher-matcher/` 부재
- [ ] `book-revision-coach/SKILL.md`에 cowork 미설치 시 폴백 절차 안내 포함
  - 안내 내용: "moai-cowork 플러그인이 설치된 경우... 미설치 시 본 스킬의 자체 퇴고 절차를 따릅니다."

---

## AC-STORY-003: 신규 스킬 13종 (story-*)

**Given**: moai-story 플러그인 스캐폴딩 완료

**When**: 신규 스킬 작성이 수행됨

**Then**:

- [ ] `plugins/moai-story/skills/story-project/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-webtoon-planner/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-webtoon-episode/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-webtoon-art/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-webnovel-writer/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-synopsis/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-screenplay/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-conti/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-ad-conti/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-character-sheet/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-cover-art/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-previz/SKILL.md` 존재
- [ ] `plugins/moai-story/skills/story-ip-pitch/SKILL.md` 존재
- [ ] **3인칭 관점 (P0 anti-pattern 1인칭 화법 부재)**: `grep -rn '저는\|제가\|우리는\|내가' plugins/moai-story/skills/*/SKILL.md` 결과 0 매치 (exit 1)
- [ ] **"무엇을/언제" 명시**: `grep -L '무엇을\|언제' plugins/moai-story/skills/*/SKILL.md` 결과 0행 (모든 스킬이 둘 중 하나 이상 포함)
- [ ] **한국어 트리거 용어**: 각 SKILL.md frontmatter `description` 필드에 한국어 토큰 1개 이상 — `for f in plugins/moai-story/skills/*/SKILL.md; do awk '/^---$/{n++; next} n==1 && /^description:/' "$f" | grep -qE '[가-힣]'; done` 모든 파일 exit 0 (21개 모두 한국어 description; ND7 정정: 기존 글로브 awk는 파일 경계마다 `n`을 리셋하지 않아 파일 #1의 description만 읽음 → per-file 루프로 block-aware 검증. 대체 형태: `awk 'FNR==1{n=0} /^---$/{n++; next} n==1 && /^description:/' <glob>`)
- [ ] 각 SKILL.md이 500줄 이내 — `find plugins/moai-story/skills -name SKILL.md -exec sh -c 'test $(wc -l < "$1") -le 500' _ {} \;` 모두 exit 0
- [ ] `find plugins/moai-story/skills -type d -mindepth 1 -maxdepth 1 | wc -l` 출력이 21

---

## AC-STORY-004: Higgsfield MCP 연동

**Given**: moai-story 플러그인 설치됨

**When**: .mcp.json이 로드됨

**Then**:

- [ ] `plugins/moai-story/.mcp.json`에 다음 canonical shape 포함:
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
- [ ] MCP 서버 URL이 정확히 `https://mcp.higgsfield.ai/mcp`
- [ ] type이 `"url"` (NOT `"http"`)
- [ ] `timeout` 필드 존재 (120000)
- [ ] `headers.User-Agent` 필드 존재 (`MoAI-Story/0.1.0`)

**Given**: 생성형 스킬 6종 (story-webtoon-art, story-conti, story-ad-conti, story-character-sheet, story-cover-art, story-previz)

**When**: 해당 스킬이 실행됨

**Then**:

- [ ] 각 스킬 본문에 크레딧 고지 문구 포함
- [ ] 각 스킬 본문에 사용자 확인 절차 포함
- [ ] 각 스킬 본문에 모델 라우팅 표 포함

**Given**: MCP 연결 실패

**When**: 생성형 스킬이 실행됨

**Then**:

- [ ] 스킬이 프롬프트 온리 폴백 모드로 동작
- [ ] 폴백 안내: "Higgsfield 웹에 프롬프트를 붙여넣으세요" 유사 메시지 포함

---

## AC-STORY-005: 크레딧 고지 의무화

**Given**: 생성형 스킬 6종

**When**: 스킬 본문을 검사

**Then**:

- [ ] `story-webtoon-art/SKILL.md`에 크레딧 고지 포함
- [ ] `story-conti/SKILL.md`에 크레딧 고지 포함
- [ ] `story-ad-conti/SKILL.md`에 크레딧 고지 포함
- [ ] `story-character-sheet/SKILL.md`에 크레딧 고지 포함
- [ ] `story-cover-art/SKILL.md`에 크레딧 고지 포함
- [ ] `story-previz/SKILL.md`에 크레딧 고지 포함
- [ ] 고지 내용: "이 작업은 Higgsfield 크레딧을 소모합니다..." 유사 메시지

---

## AC-STORY-006: cowork v4.0.0 마이그레이션

**Given**: cowork v3.0.0 설치됨

**When**: v4.0.0 마이그레이션 수행됨

**Then**:

- [ ] `plugins/moai-cowork/.claude-plugin/plugin.json` version이 `"4.0.0"`
- [ ] `find plugins/moai-cowork/skills -type d -mindepth 1 -maxdepth 1 | wc -l` 출력이 171 (relative check: post-migration expected = pre-migration count − 8)
- [ ] `grep -rl 'book-concept-planner' plugins/moai-cowork/skills/` 결과 없음 (모든 book-* 제거됨 — `-r` 재귀 + `-l` 파일명 출력, 인용부호 정상 종료)
- [ ] `plugins/moai-cowork/.mcp.json`에 higgsfield 엔트리 부재
- [ ] `grep -L 'version:.*4\.0\.0' plugins/moai-cowork/skills/*/SKILL.md | wc -l` 출력이 0 (4.0.0 미포함 SKILL.md 없음 → 171개 모두 4.0.0; ND4 정정: `grep -c|wc -l`은 파일 수를 세어 false-positive; ND6 정정: `"version":"4.0.0"` 공백-없음 리터럴은 무효 YAML이라 pyyaml 오류 → 유효 YAML `version: "4.0.0"` frontmatter + grep 패턴 완화 `'version:.*4\.0\.0'`)
- [ ] `plugins/moai-cowork/CHANGELOG.md`에 v4.0.0 섹션 존재
- [ ] CHANGELOG.md에 "book-* 스킬 moai-story로 이관" 안내 포함
- [ ] CHANGELOG.md에 "`/plugin install story`" 마이그레이션 가이드 포함

---

## AC-STORY-007: `.claude-plugin/marketplace.json` 4엔트리 갱신

**Given**: `.claude-plugin/marketplace.json` 파일 존재

**When**: 4엔트리 갱신 수행됨

**Then**:

- [ ] `cat .claude-plugin/marketplace.json | jq '.plugins | length'` 출력이 4
- [ ] `.claude-plugin/marketplace.json` plugins[0].name이 "moai-cowork"
- [ ] `.claude-plugin/marketplace.json` plugins[0].description에 171 skills 언급 (book-* 이관 후)
- [ ] `.claude-plugin/marketplace.json` plugins[0].description에 "moai-story" 마이그레이션 안내 포함
- [ ] `.claude-plugin/marketplace.json` plugins[1].name이 "moai-code" (canonical re-index — 기존 유지)
- [ ] `.claude-plugin/marketplace.json` plugins[2].name이 "moai-design" (canonical re-index — 기존 유지)
- [ ] `.claude-plugin/marketplace.json` plugins[3].name이 "moai-story" (신규 추가 4번째 엔트리)
- [ ] `.claude-plugin/marketplace.json` plugins[3].displayName이 "MoAI Story"
- [ ] `.claude-plugin/marketplace.json` plugins[3].description에 21 skills 언급
- [ ] `.claude-plugin/marketplace.json` plugins[3].description에 Higgsfield 언급
- [ ] `.claude-plugin/marketplace.json` `metadata.version`이 `"4.0.0"` (catalog 단일 version 지점 — D1 정합)
- [ ] `jq '.plugins[].version' .claude-plugin/marketplace.json` 출력이 모두 `null` (plugin entry는 version 필드 미기재 per NFR-STORY-003 / D14)
- [ ] `claude plugin validate . --strict` 통과

---

## AC-STORY-008: www 문서 갱신

**Given**: www 문서 디렉토리 존재

**When**: 문서 갱신 수행됨

**Then**:

- [ ] `www/plugins/index.md`에 moai-story 섹션 존재
- [ ] index.md에 4 플러그인 모두 개요 포함
- [ ] `www/plugins/migration.md` 존재 (또는 업데이트됨)
- [ ] migration.md에 cowork v4.0.0 마이그레이션 가이드 포함
- [ ] migration.md에 `/plugin install story` 설치 안내 포함
- [ ] `www/plugins/higgsfield-setup.md` 존재
- [ ] higgsfield-setup.md에 OAuth 인증 절차 포함
- [ ] `www/CHANGELOG.md`에 v4.0.0 섹션 존재
- [ ] CHANGELOG.md에 moai-story 신설 언급
- [ ] Hugo 빌드 성공 (`cd www && npm run build`)

---

## AC-STORY-009: 스킬 위생 기준 준수 (기계적 grep)

**Given**: 21개 story 스킬

**When**: 위생 기준 기계적 검사 수행

**Then** (각 항목은 tester가 verbatim 실행 가능한 grep/lint 명령):

- [ ] **3인칭 관점 (P0 anti-pattern 1인칭 화법 부재)**: `grep -rn '저는\|제가\|우리는\|내가' plugins/moai-story/skills/*/SKILL.md` 결과 0 매치 (exit code 1)
- [ ] **"무엇을/언제" 명시**: `grep -L '무엇을\|언제' plugins/moai-story/skills/*/SKILL.md` 결과 0행 (모든 SKILL.md가 둘 중 하나 이상 포함)
- [ ] **AI-tell 문구 부재 (P0 anti-pattern)**: `grep -rnE '종합적으로 볼 때|한 가지 분명한 것은|핵심적인 점은|결론적으로' plugins/moai-story/skills/*/SKILL.md` 결과 0 매치
- [ ] **한국어 트리거 용어 포함**: 각 SKILL.md의 frontmatter `description` 필드에 한국어 토큰 1개 이상 — `awk '/^---$/{n++; next} n==1 && /^description:/' plugins/moai-story/skills/*/SKILL.md | grep -E '[가-힣]'` 매치 (모든 스킬)
- [ ] **SKILL.md 500줄 이내**: `find plugins/moai-story/skills -name SKILL.md -exec sh -c 'test $(wc -l < "$1") -le 500' _ {} \;` 모든 파일 exit 0
- [ ] **markdown 구조 (H2 섹션 ≥ 2개)**: `for f in plugins/moai-story/skills/*/SKILL.md; do test "$(grep -c '^## ' "$f")" -ge 2; done` 모든 파일 exit 0
- [ ] **frontmatter parse**: 각 SKILL.md가 `---` 로 시작하고 두 번째 `---` 에서 닫힘 — `for f in plugins/moai-story/skills/*/SKILL.md; do awk '/^---$/{c++; if(c==2){found=1; exit}} END{exit !found}' "$f"; done` 모두 exit 0 (ND8 정정: 기존 `END{exit 1}`는 awk `exit`가 END 블록을 실행하므로 앞선 `c==2 exit 0`을 override하여 항상 exit 1 되는 결함 → `found` 플래그로 override 해소)

> **잔여 주관적 판단 (sync-phase human review)**: 스킬 본문의 자연스러운 문체 품질, 장르 전문 용어의 적절성 등은 기계적 grep로 검증 불가 — 본 AC의 기계적 검사 7종 PASS 후 sync-phase에서 사용자 최종 리뷰로 처리한다.

---

## AC-STORY-010: 3점 동기화 준수

**Given**: cowork v4.0.0

**When**: 버전 일괄 검사

**Then**:

- [ ] `grep 'version:.*4\.0\.0' plugins/moai-cowork/.claude-plugin/plugin.json` 결과 1건 (ND6 정정: 무효 YAML 리터럴 `"version":"4.0.0"` 대신 유효 YAML `version: "4.0.0"` + 패턴 완화 `'version:.*4\.0\.0'`)
- [ ] `grep -L 'version:.*4\.0\.0' plugins/moai-cowork/skills/*/SKILL.md | wc -l` 결과 0 (4.0.0 미포함 SKILL.md 없음; ND4 정정; ND6 정정: 동일 패턴 완화)
- [ ] 모든 스킬 버전이 plugin.json 버전과 일치

---

## AC-STORY-011: 종합 검증

**Given**: 모든 구현 완료

**When**: 릴리스 전 검증

**Then**:

- [ ] `claude plugin validate . --strict` 통과 (전체 마켓 루트 + 4 플러그인)
- [ ] `claude plugin details`로 4 플러그인 모두 정보 조회 가능
- [ ] moai-story 스킬 카운트: 21
- [ ] moai-cowork 스킬 카운트: 171 (post-migration expected)
- [ ] `.claude-plugin/marketplace.json` 4엔트리 정합
- [ ] www 문서 빌드 성공
- [ ] Git 상태 정상 (no uncommitted changes in critical files)

---

## AC-STORY-012: 토큰 비용 제어 (NFR-STORY-001)

**Given**: moai-story 신설 + cowork v4.0.0 마이그레이션 완료 후

**When**: higgsfield MCP 서버 위치 기계적 검사 수행

**Then**:

- [ ] `find plugins -name '.mcp.json' -not -path '*/node_modules/*' -exec grep -l 'higgsfield' {} \;` 출력이 정확히 1행: `plugins/moai-story/.mcp.json` (higgsfield는 moai-story에만 존재)
- [ ] `grep -L 'higgsfield' plugins/moai-cowork/.mcp.json` 매치 1행 (cowork .mcp.json에는 higgsfield 없음 — 부재 확인)
- [ ] `jq '.mcpServers | keys | length' plugins/moai-cowork/.mcp.json` 값이 11 (higgsfield 제거 후 12 → 11 — cowork MCP가 한국 MCP 통합 커밋으로 12개까지 증가, higgsfield 제거 후 11개; ND5 정정: 기존 "9 → 8"은 stale 기대값)
- [ ] `jq '.mcpServers | keys | length' plugins/moai-story/.mcp.json` 값이 1 (higgsfield만 단일 배선)
- [ ] cowork plugin token budget에서 higgsfield 도구 표면(수십 개 도구)이 제거되어 비용 부담이 story 설치자로만 한정됨

---

## AC Summary Table

| AC ID | REQ ID | Milestone | Priority |
|-------|--------|-----------|----------|
| AC-STORY-001 | REQ-STORY-001 | M1 | P0 |
| AC-STORY-002 | REQ-STORY-002 | M2 | P0 |
| AC-STORY-003 | REQ-STORY-003 | M3 | P0 |
| AC-STORY-004 | REQ-STORY-004 | M1, M3 | P0 |
| AC-STORY-005 | REQ-STORY-005 | M3 | P1 |
| AC-STORY-006 | REQ-STORY-006 | M4 | P0 |
| AC-STORY-007 | REQ-STORY-007 | M5 | P0 |
| AC-STORY-008 | REQ-STORY-008 | M6 | P1 |
| AC-STORY-009 | REQ-STORY-009 | M3 | P1 |
| AC-STORY-010 | NFR-STORY-003 | M4 | P0 |
| AC-STORY-011 | — | All | P0 |
| AC-STORY-012 | NFR-STORY-001 | M4, M1 | P0 |

**Total ACs**: 12
**P0 ACs**: 9
**P1 ACs**: 3

### REQ/NFR → AC Traceability

| REQ/NFR | AC | Mechanical verification |
|---------|-----|-------------------------|
| REQ-STORY-001 | AC-STORY-001 | `claude plugin validate plugins/moai-story` exit 0 |
| REQ-STORY-002 | AC-STORY-002 | 8개 SKILL.md 존재 + `book-revision-coach` 폴백 안내 |
| REQ-STORY-003 | AC-STORY-003 | 13개 story-* SKILL.md 존재 + grep 0 매치 |
| REQ-STORY-004 | AC-STORY-004 | `.mcp.json` canonical shape jq 파싱 |
| REQ-STORY-005 | AC-STORY-005 | 6개 생성형 스킬 크레딧 고지 포함 |
| REQ-STORY-006 | AC-STORY-006 | plugin.json version 4.0.0 + 스킬 카운트 171 |
| REQ-STORY-007 | AC-STORY-007 | `.claude-plugin/marketplace.json` 4엔트리 + `metadata.version` 4.0.0 |
| REQ-STORY-008 | AC-STORY-008 | Hugo 빌드 성공 + www 파일 존재 |
| REQ-STORY-009 | AC-STORY-009 | grep 0 매치 + frontmatter 파싱 + H2 섹션 카운트 |
| NFR-STORY-001 | AC-STORY-012 | higgsfield MCP가 moai-story에만 존재 |
| NFR-STORY-002 | AC-STORY-004 | MCP 미연결 폴백 안내 (story 본문 검사) |
| NFR-STORY-003 | AC-STORY-007, AC-STORY-010 | plugin entry version 부재 (`jq` all null) + plugin.json/SKILL.md 3점 동기화 |
