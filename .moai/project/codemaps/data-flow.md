---
title: 모두의 클로드 — 데이터 흐름
description: 콘텐츠 파이프라인, 플러그인 배포, SPEC 생명주기
last_updated: 2026-07-09
---

# 모두의 클로드 데이터 흐름

## 콘텐츠 파이프라인 (문서 사이트)

```
Author
  ├── www/content/
  │   ├── {section}/*.md (Markdown)
  │   └── data/menu/main.yaml (navigation)
  │        ↓
  ├── Hugo Build (0.160.1)
  │   ├── markdownlib 렌더링
  │   ├── go 템플릿 적용 (hugo-geekdoc 테마)
  │   ├── asset minification (--minify)
  │   └── output: www/public/ (HTML)
  │        ↓
  ├── Vercel Deployment
  │   ├── 보안 헤더 추가 (X-Frame-Options, X-Content-Type-Options, Referrer-Policy)
  │   ├── 리다이렉트 규칙 적용 (vercel.json)
  │   └── https://claude.mo.ai.kr/
  │        ↓
  └── 사용자 브라우징 (읽기 전용)
```

### 데이터 흐름 세부
1. **작성**: 작자가 `www/content/cowork/intro.md` 작성
2. **Git**: `git push origin main` → GitHub
3. **Vercel 감시**: GitHub 푸시 이벤트 감시
4. **빌드**: `hugo --gc --minify --enableGitInfo=false`
5. **배포**: `www/public/` → Vercel CDN
6. **Live**: https://claude.mo.ai.kr/cowork/ 즉시 업데이트

> **주의**: `node scripts/check-links.mjs`는 로컬 수동 검증 단계이며, Vercel 빌드 파이프라인의 일부가 아님

---

## 플러그인 배포 흐름

```
Plugin Source Code
  └── plugins/{plugin-name}/
       ├── .claude-plugin/plugin.json  (플러그인 메타데이터)
       ├── skills/
       ├── commands/
       ├── agents/
       ├── hooks/
       │   └── hooks.json
       └── .mcp.json
            ↓
        .claude-plugin/
         marketplace.json
          ├── declares: moai-coworker
          ├── declares: moai-designer
          ├── declares: moai-coder
          └── declares: moai-pm (버전 SSOT는 각 plugin.json)
            ↓
        Claude Code Marketplace registration
         (git repository → marketplace API)
          └── moai plugin export
               └── generates marketplace PR
            ↓
        (Auto-merge or manual)
         modu-ai/claude repo
          (marketplace registry)
            ↓
        Claude Code 클라이언트
         /plugin marketplace search "moai-claude"
          ├── discover modu-ai/claude entry
          └── install → plugin cache
            ↓
        Claude Code Session
         모든 4개 플러그인 로드 (T1 레벨, 로컬/Desktop)
         
> **참고**: Web 세션 지원은 향후 계획 (v2 재설계)
  설정 메커니즘 미구현
```

### 버전 관리
```
Plugin Version Updates:
  moai-coworker: 5.0.0 ← 193 skills, coworker vX.Y.Z 독립
  moai-designer: 0.2.0 ← 11 skills, designer vX.Y.Z 독립
  moai-coder: 3.1.0    ← 29 skills, coder vX.Y.Z 독립
  moai-pm: 0.2.0       ← 1 skill, pm vX.Y.Z 독립

Marketplace Metadata:
  .claude-plugin/marketplace.json
   → metadata.version: 5.0.0 (마켓 번들 버전, 참고용)

Website Version:
  www/hugo.toml
   → params.version: 2.27.0 (웹사이트 릴리스, 독립)

CHANGELOG:
  CHANGELOG.md
   → 모든 버전 통합 기록 (feat, fix, docs 등)
```

---

## SPEC 생명주기

### 전체 생명주기 (plan → run → sync)

```
[사용자 입력]
  "로그인 OAuth 추가"
            ↓
[1단계: 계획 (Plan Phase)]
  사용자: /moai:plan "OAuth 로그인 기능"
            ↓
  manager-spec
    ├── 입력 분석 (자연어)
    ├── GEARS 형식 요구사항 생성
    ├── 수용 기준 정의 (Given-When-Then)
    └── .moai/specs/SPEC-MOC-AUTH-001/ 생성
         ├── spec.md (요구사항 + frontmatter)
         ├── plan.md (구현 계획 + 마일스톤)
         ├── acceptance.md (AC matrix)
         └── progress.md (§E.1 plan-audit-ready)
            ↓
  plan-auditor
    ├── 요구사항 명확성 검증
    ├── AC 수 확인
    └── 피드백 또는 승인
            ↓
[2단계: 구현 (Run Phase)]
  사용자: /moai:run SPEC-MOC-AUTH-001
            ↓
  manager-develop
    ├── SPEC 로드 (.moai/specs/SPEC-MOC-AUTH-001/)
    ├── DDD 순환: ANALYZE → PRESERVE → IMPROVE
    │   ├── M1: 초기 구조 (feature branch)
    │   ├── M2-M5: 점진적 구현
    │   └── M6: 최종 검증
    ├── 품질 게이트 (TRUST 5)
    │   ├── Tested: 커버리지 ≥90%
    │   ├── Readable: 코드 스타일 검증
    │   ├── Unified: 포맷 일관성
    │   ├── Secured: 보안 검사
    │   └── Trackable: 커밋 메시지
    └── progress.md 갱신
         └── §E.2 run-phase evidence
         └── §E.3 run-audit-ready
            ↓
[3단계: 동기화 (Sync Phase)]
  사용자: /moai:sync SPEC-MOC-AUTH-001
            ↓
  manager-docs
    ├── SPEC 완료 확인
    ├── API 문서 생성
    ├── architecture diagram 생성
    ├── CHANGELOG.md 갱신
    │   └── [Unreleased]
    │        ├── feat(SPEC-MOC-AUTH-001): OAuth 로그인
    │        ├── docs: API 문서
    │        └── fix(SPEC-MOC-AUTH-001): 보안 bug
    ├── README.md 갱신 (feature 목록)
    ├── frontmatter 갱신
    │   └── status: implemented → completed
    │   └── updated: {sync date}
    ├── progress.md 갱신
    │   └── §E.4 sync-audit-ready
    │   └── sync_commit_sha: {commit hash}
    └── PR 생성 + 병합
         └── (Tier 분류에 따라)
            ↓
  sync-auditor
    ├── 독립 품질 검증
    ├── 4차원 평가 (Function/Security/Craft/Consistency)
    └── PASS/FAIL 결과
            ↓
[완료]
  SPEC 상태: completed
  구현 코드: main에 병합
  문서: claude.mo.ai.kr 반영
  CHANGELOG: [5.0.1] 또는 [6.0.0]으로 태깅
```

### SPEC 파일 상태 전이

```
.moai/specs/SPEC-MOC-AUTH-001/spec.md
  ├── 생성 시: status: draft
  │            created: 2026-07-09
  │            updated: 2026-07-09
  │
  ├── 구현 시작: status: in-progress
  │              updated: 2026-07-10
  │
  └── 완료: status: completed
           updated: 2026-07-12
           (sync commit에 포함)

progress.md 진행 추적
  ├── §E.1 Plan-phase Audit-Ready Signal
  │    └── plan_status: audit-ready
  │    └── plan_complete_at: 2026-07-09T14:30:00Z
  │
  ├── §E.2 Run-phase Evidence
  │    └── M1, M2, ..., M6 진행 상황
  │    └── 커밋 SHA
  │
  ├── §E.3 Run-phase Audit-Ready Signal
  │    └── coverage: 92%
  │    └── lint: clean
  │    └── run_complete_at: 2026-07-11T10:00:00Z
  │
  └── §E.4 Sync-phase Audit-Ready Signal
       └── sync_commit_sha: abc123def456...
       └── sync_complete_at: 2026-07-12T16:45:00Z
       └── changelog_entry_position: [Unreleased]/feat
```

---

## 멀티-SPEC 오케스트레이션 흐름

```
Epic 개념 (여러 SPEC)
  ├── SPEC-MOC-AUTH-001 (OAuth 추가)
  │    ├── status: plan → in-progress → completed
  │    └── (3단계 plan-audit-run-sync-audit)
  │
  ├── SPEC-MOC-AUTH-002 (2FA 추가)
  │    ├── status: draft (아직)
  │    └── (SPEC-001 완료 후 시작)
  │
  ├── SPEC-MOC-SITE-IA-001 (사이트 구조 개선)
  │    ├── status: completed (이전 Epic)
  │    └── (다른 Epic, 병렬 진행 가능)
  │
  └── SPEC-MOC-PLUGIN-STORY-001 (story-project 스킬 추가)
       ├── status: in-progress (진행 중)
       └── (독립적으로 진행)

Session Handoff (컨텍스트 초과 시)
  SPEC-MOC-AUTH-001 (완료)
     ↓ (/clear 세션 저장)
  paste-ready resume message
   ├── ultrathink. SPEC-MOC-AUTH-002 진입
   ├── applied lessons: [AUTH-001의 교훈]
   ├── 전제 검증 (git status, 커밋 확인)
   ├── 실행: /moai:plan "2FA 추가"
   └── 머지 후: SPEC-MOC-AUTH-003 다음
     ↓ (사용자 paste → 다음 세션)
  새 세션이 SPEC-AUTH-002 이어받아 진행
```

---

## 메모리 및 설정 흐름

```
프로젝트 첫 실행
  user.yaml, language.yaml (defaults)
  ├── language: conversation_language = "en"
  ├── agent_prompt_language = "en" (항상)
  └── code_comments = "en"
       ↓
사용자가 /moai:project 실행
  스캐폴드 생성
  ├── .claude/settings.json (output-style + plugin선언)
  ├── .moai/config/sections/ (27개 yaml)
  │   └── language.yaml 재생성 (project values)
  ├── CLAUDE.md (규칙 정본, project root)
  ├── .claude/agents/ (8개 에이전트)
  ├── .moai/specs/ (SPEC 저장소)
  └── 사용자 메모리 생성
       └── ~/.claude/projects/{hash}/memory/
           ├── MEMORY.md (인덱스)
           └── project_* (프로젝트 메모리)
       ↓
에이전트가 스펙 처리
  각 에이전트 로드
  ├── .moai/config/sections/language.yaml 읽기
  │   └── conversation_language = "en"
  ├── CLAUDE.md 규칙 준수
  ├── project 메모리 상담
  └── 작업 수행
```

---

## 배포 체인

### 로컬 개발 → 라이브

```
로컬 에이전트 작업 (예: moai-coworker 스킬 추가)
  1. skills/<새-스킬-이름>/SKILL.md 작성 (flat 접두사 명명, 예: skills/marketing-campaign-planner/)
  2. git add, git commit (Conventional Commits)
  3. git push origin main → GitHub
       ↓
GitHub PR 또는 직접 push
  (자동 또는 수동)
  4. Vercel 감시 (github push event)
       ↓
플러그인 빌드 (optional, moai-adk-go 사용)
  5. moai plugin export → marketplace.json 갱신
  6. 마켓플레이스 PR 자동 제출
       ↓
마켓플레이스 병합
  (Tier 분류)
  7. modu-ai/claude repo 업데이트
       ↓
사용자 클라이언트
  (다음 세션 시)
  8. /plugin marketplace refresh
  9. moai-coworker 새 스킬 자동 로드
       ↓
완료: 새 스킬 사용 가능
```

---

**마지막 갱신**: 2026-07-09  
**주요 파이프라인**: 콘텐츠 (Hugo) / 플러그인 (배포) / SPEC (plan-run-sync)
