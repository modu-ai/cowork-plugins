---
title: 모두의 클로드 — 모듈 설명
description: 각 모듈의 책임, 공개 인터페이스, 플러그인 네임스페이스
last_updated: 2026-07-09
---

# 모두의 클로드 모듈 설명

## 플러그인 모듈

### 모이-코워커 (moai-coworker) — 546 files, 193 skills

**책임**: 실무 및 창작 도메인 전문성 제공

**8개 실무 도메인**:
- **business**: 사업 전략, 마켓 분석
- **commerce**: 이커머스, 제품 관리
- **marketing**: 마케팅 전략, 캠페인
- **content**: 콘텐츠 작성, SEO
- **legal**: 계약 검토, 법률 조언
- **finance**: 재무 분석, 예산
- **hr**: 인사 정책, 채용
- **education**: 교육 콘텐츠, 커리큘럼

**4개 창작 분야** (story-project 스킬):
- **웹툰**: 시나리오, 캐릭터 설정
- **웹소설**: 장편 스토리 구성
- **시나리오**: 영화/드라마 각본
- **출판**: 책 편집, 표지 디자인

**공개 인터페이스**:
- 자연어 요청 → 도메인별 매칭 스킬 자동 호출
- `/story-project [작품명]` → 창작 워크플로우
- 도메인 스킬은 컨텍스트 기반으로 조용히 선택됨

---

### 모이-디자이너 (moai-designer) — 112 files

**책임**: 디자인 시스템 및 브랜드 설계 전담

**주요 기능**:
- Claude Design 시스템 연동
- 디자인 토큰(DTCG) 관리
- DESIGN.md 자동 생성
- 브랜드 가이드라인 생성
- GAN 품질 루프 (반복 개선)

**커맨드** (6개 독립 명령):
- `/brief` — 브리프 작성
- `/check` — 디자인 검증
- `/design` — 디자인 생성 (Path A/B 라우터)
- `/import` — 디자인 임포트
- `/system` — 디자인 시스템 관리
- `/tokens` — 디자인 토큰 관리

**공개 인터페이스**:
- 자연어 "브리프 작성" → 디자인 시스템 자동 생성
- 각 커맨드 (`/brief`, `/check`, `/system` 등) 직접 호출
- DESIGN.md 파일 자동 생성

---

### 모이-코더 (moai-coder) — 354 files

**책임**: 개발 방법론(SPEC/DDD/TDD) 전담. **플러그인 명칭 변경 예정 (v2)**: "moai-coder" → "moai" (현재는 moai-coder)

**8개 에이전트** (code-investigator + moai/ 7종):
1. manager-spec: SPEC 생성 (plan phase)
2. manager-develop: 구현 (run phase)
3. manager-docs: 문서 동기화 (sync phase)
4. manager-git: PR 생성
5. plan-auditor: 계획 검토
6. sync-auditor: 동기화 검토
7. builder-harness: 하네스 구축
8. code-investigator: 코드베이스 조사 (agents/ 최상위)

**14개 커맨드**:
- `/moai:plan` — SPEC 생성
- `/moai:run` — 구현 시작
- `/moai:sync` — 문서 동기화
- `/moai:review` — 코드 검토
- 외 10개

**29개 스킬**:
- moai-workflow-spec: SPEC 저작
- moai-workflow-ddd: DDD 패턴
- moai-workflow-testing: 테스트 전략
- moai-foundation-*: 핵심 원칙
- 외 25개

**공개 인터페이스** (현재):
- `/moai plan "description"` 또는 `/moai:plan` → SPEC 생성
- `/moai run SPEC-ID` 또는 `/moai:run` → 구현 시작
- `/moai sync SPEC-ID` 또는 `/moai:sync` → 동기화
- Skill("moai-foundation-core") 등 기초 스킬 호출

**고유 기능**:
- GEARS 형식 요구사항 (vs EARS 레거시)
- TRUST 5 품질 게이트 (Tested/Readable/Unified/Secured/Trackable)
- 자동 CHANGELOG 생성
- SPEC 진행 추적 (progress.md)

---

### 모이-PM (moai-pm) — 17 files

**책임**: 프로젝트 초기화 및 4개 플러그인 진입 라우팅

**1개 스킬** (`/project`):
- `/project --cowork` → moai-coworker 초기화 (Cowork 스캐폴드)
- `/project --designer` → moai-designer 초기화 (Design 시스템)
- `/project --code` → moai-coder 초기화 (SPEC 체계)
- `/project` (기본) → 프로젝트 스캐폴드 (`.claude/` + `.moai/`)

**공개 인터페이스**:
- `/project` 한 명령 → 4개 진입 옵션
- 비개발자 친화적 자연어 라우팅

---

## Claude Code 모듈

### CLAUDE.md (24KB) — 실행 지침 SSOT

**책임**: Claude Code 클라이언트의 규칙 및 지침 정의

**주요 섹션**:
1. **Core Identity**: MoAI 오케스트레이터 정의
2. **Request Processing**: 4단계 요청 처리 (Analyze→Route→Execute→Report)
3. **Agent Catalog**: 8개 에이전트 목록 및 선택 결정 트리
4. **SPEC Workflow**: plan/run/sync 3단계
5. **Quality Gates**: TRUST 5 프레임워크
6. **Safe Development**: 5가지 개발 안전장치
7. **User Interaction**: AskUserQuestion 채널 규칙
8. **Context Management**: 토큰 예산 관리
9. **Error Handling**: 에러 복구 흐름

**공개 인터페이스**:
- 모든 에이전트와 사용자가 읽고 준수
- 프로젝트 규칙의 불변 기준점

---

### .claude/agents/moai/ — 7개 에이전트 (+ Anthropic 내장 Explore)

**공개 인터페이스**: `Agent(agent_type)` 호출

| 에이전트 | 책임 | 사용 시점 |
|---------|------|---------|
| manager-spec | SPEC 생성 | `/moai:plan` 명령 |
| manager-develop | 구현 | `/moai:run` 명령 |
| manager-docs | 문서 동기화 | `/moai:sync` 명령 |
| manager-git | PR 생성 | sync 후 Tier L 또는 `--pr` |
| plan-auditor | 계획 검토 | plan 완료 후 자동 |
| sync-auditor | 동기화 검토 | sync 완료 후 자동 |
| builder-harness | 하네스 구축 | `/moai:harness` 명령 |
| Explore | 코드탐색 (builtin) | 읽기 전용 분석 |

---

### .claude/rules/moai/ — 규칙 문서

**구조**:
```
core/           — 핵심 규칙 (HARD)
  ├── moai-constitution.md
  ├── askuser-protocol.md
  ├── agent-common-protocol.md
  ├── verification-claim-integrity.md
  └── settings-management.md

workflow/       — 워크플로우 규칙
  ├── spec-workflow.md
  ├── session-handoff.md
  ├── context-window-management.md
  └── mx-tag-protocol.md

development/    — 개발 규칙
  ├── spec-frontmatter-schema.md
  ├── manager-develop-prompt-template.md
  ├── coding-standards.md
  ├── skill-authoring.md
  └── ... (11개 파일)

languages/      — 언어 규칙 (multi-language)

quality/        — 품질 규칙

design/         — 설계 규칙
```

**공개 인터페이스**: path-scoped 로드 (CLAUDE.md에서 cross-reference)

---

### .claude/skills/moai/ — 스킬 카탈로그

**구조**:
- SKILL.md: 마스터 스킬 (프론트페이지)
- references/: 외부 링크 및 레퍼런스
- team/: 팀 구성 및 역할 정의
- workflows/: 워크플로우 스킬

**선택 스킬**:
- moai-foundation-core: SPEC-First DDD 기초
- moai-foundation-quality: TRUST 5 품질 게이트
- moai-foundation-thinking: 창의적 사고 프레임워크
- moai-workflow-spec: GEARS 형식 저작
- moai-workflow-ddd: ANALYZE-PRESERVE-IMPROVE 순환

**공개 인터페이스**: 클릭 검색 + `Skill("moai")` 호출

---

### .claude/hooks/moai/ — 훅 스크립트

**책임**: 깃 커밋, Claude Code 세션 이벤트 검증

**주요 훅**:
- PreToolUse: 위험한 Bash 커맨드 경고
- PostToolUse: 상태 변경 감시 (파일쓰기·커밋)
- Stop: 세션 종료 전 최종 검증
- SessionStart: 세션 시작 시 헬스 체크

**공개 인터페이스**: `.claude/settings.json`에서 등록

---

## .moai/ 모듈

### .moai/config/ — 설정 계층

**27개 설정 섹션** (language.yaml, quality.yaml, git-convention.yaml, ...):
- 프로젝트 전용 규칙 정의
- 언어, 품질, git 규칙, LLM 파라미터 등
- 스캐폴드 시 `/moai:project`에서 자동 생성

**공개 인터페이스**: 에이전트가 로드하여 프로젝트 문화 적용

---

### .moai/specs/ — SPEC 저장소

**각 SPEC-ID 디렉토리**:
- spec.md: 요구사항 (GEARS 형식)
- plan.md: 구현 계획
- acceptance.md: 수용 기준
- progress.md: 진행 추적

**공개 인터페이스**: `/moai:run SPEC-ID` → 로드

---

### .moai/project/ — 프로젝트 문서 (이 파일들)

**8개 문서**:
- product.md, structure.md, tech.md
- codemaps/overview.md, modules.md, dependencies.md, entry-points.md, data-flow.md

**책임**: 에이전트 및 사용자 참고용 아키텍처 문서

---

## 웹사이트 모듈 (www/)

### content/ — Markdown 콘텐츠

**2축 구조**:
- Desktop axis (비개발자): /chat/, /cowork/, /design/, /code/
- CLI axis (개발자): /cli/start/, /cli/concepts/, /cli/daily/, /cli/moai-adk/, /cli/reference/
- Shared: /help/, /cookbook/, /releases/

**공개 인터페이스**: Hugo → HTML 변환 → https://claude.mo.ai.kr/

---

**마지막 갱신**: 2026-07-09
