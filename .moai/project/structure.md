---
title: 모두의 클로드 — 디렉토리 구조
description: monorepo의 디렉토리 구조, 모듈 경계, 주요 파일 위치
last_updated: 2026-07-09
---

# 모두의 클로드 디렉토리 구조

## 최상위 디렉토리 맵

```
.
├── .claude/                     # Claude Code 에이전트 및 규칙 (373 tracked files) + CLAUDE.md
├── .moai/                       # MoAI-ADK 설정 및 문서 (277 tracked files)
├── .claude-plugin/              # 플러그인 마켓플레이스 매니페스트
├── .github/                     # GitHub Actions 및 CI 설정 (3 tracked files)
├── .git_hooks/                  # 로컬 Git 훅 (2 tracked files)
├── plugins/                     # 4개 플러그인 소스 (1032 tracked files)
├── www/                         # Hugo 문서 사이트 (544 tracked files)
├── scripts/                     # 유틸리티 스크립트 (18 tracked files)
├── .gitignore                   # Git 무시 규칙
├── .mcp.json                    # MCP 서버 설정
├── CLAUDE.md                    # Claude Code 실행 지침 (24KB)
├── CHANGELOG.md                 # 변경 이력
├── Makefile                     # 로컬 빌드 대상
└── README.md                    # 프로젝트 소개 (stale — marketplace.json이 정본)
```

## 플러그인 디렉토리 구조 (1032 files)

### 공통 패턴: `plugins/{plugin-name}/`

```
plugins/
├── moai-coworker/               # 코워커 플러그인 (546 files)
│   ├── .claude-plugin/plugin.json  # 플러그인 메타데이터 (name, version, description)
│   ├── skills/                  # 193 스킬 (flat prefix-named dirs, no domain/ subdir)
│   │   ├── story-project/       # 창작 워크플로우
│   │   └── ... (business-*, commerce-*, marketing-*, etc.)
│   ├── .mcp.json                # MCP 서버 설정
│   └── ...
├── moai-designer/               # 디자이너 플러그인 (112 files)
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 11 스킬
│   ├── commands/                # 6 커맨드: brief, check, design, import, system, tokens
│   └── ...
├── moai-coder/                  # 코더 플러그인 (354 files)
│   ├── .claude-plugin/plugin.json
│   ├── skills/                  # 29 스킬
│   ├── commands/                # 14 커맨드
│   ├── agents/                  # 8 에이전트 (code-investigator + moai/ 7종: manager-spec, -develop, -docs, -git, plan-auditor, sync-auditor, builder-harness)
│   └── ...
└── moai-pm/                     # PM 플러그인 (17 files)
    ├── skills/
    │   └── project/             # /project 라우터 스킬
    └── ...
```

### SPEC 아티팩트 조직

**전체 SPEC 저장소**: `.moai/specs/`

```
.moai/specs/
├── SPEC-MOC-BOOTSTRAP-DESKTOP-001/
│   ├── spec.md                  # 요구사항 (GEARS 형식)
│   ├── plan.md                  # 구현 계획
│   ├── acceptance.md            # 수용 기준
│   └── progress.md              # 진행 상황
├── SPEC-MOC-PLUGIN-REMEDIATION-001/
│   ├── spec.md
│   ├── plan.md
│   ├── acceptance.md
│   └── progress.md
├── SPEC-MOC-PLUGIN-STORY-001/   # 진행 중
│   └── ...
├── SPEC-MOC-SITE-IA-001/        # 완료
│   └── ...
└── ...
```

## Claude Code 디렉토리 구조 (373 files)

> **주의**: CLAUDE.md는 repo root에 위치 (`.claude/` 내가 아님)

```
.claude/
├── agents/
│   └── moai/
│       ├── manager-spec.md      # 계획 단계 에이전트
│       ├── manager-develop.md   # 구현 단계 에이전트
│       ├── manager-docs.md      # 동기화 단계 에이전트
│       ├── manager-git.md       # PR 생성 에이전트
│       ├── plan-auditor.md      # 계획 검토 에이전트
│       ├── sync-auditor.md      # 동기화 검토 에이전트
│       └── builder-harness.md   # 하네스 구축 에이전트
├── commands/                    # 슬래시 커맨드 (thin wrapper)
│   └── moai/
│       ├── plan.md
│       ├── run.md
│       ├── sync.md
│       └── ...
├── skills/                      # 스킬 정의
│   └── moai/
│       ├── SKILL.md             # 마스터 스킬
│       └── workflows/           # 워크플로우 스킬
├── hooks/                       # 깃 훅 및 Claude Code 훅
│   └── moai/
│       ├── gateguard-fact-force.sh
│       ├── status-transition-ownership.sh
│       └── ...
├── rules/                       # 규칙 파일 (path-scoped)
│   └── moai/
│       ├── core/                # 핵심 규칙
│       ├── workflow/
│       ├── development/
│       ├── languages/            # 다국어 규칙
│       ├── quality/              # 품질 규칙
│       └── design/               # 설계 규칙
├── output-styles/              # 응답 형식 스타일
│   └── moai/
│       ├── moai.md
│       ├── moai-easy.md
│       └── einstein.md
└── settings.json               # Claude Code 설정
```

## MoAI-ADK 디렉토리 구조 (277 files)

```
.moai/
├── config/                      # 설정 (27개 section yaml)
│   ├── sections/
│   │   ├── cache.yaml, constitution.yaml, context.yaml, db.yaml, design.yaml
│   │   ├── feedback.yaml, git-convention.yaml, git-strategy.yaml, handoff.yaml
│   │   ├── harness.yaml, interview.yaml, language.yaml, llm.yaml, lsp.yaml, mx.yaml
│   │   ├── observability.yaml, project.yaml, quality.yaml, ralph.yaml, research.yaml
│   │   ├── security.yaml, state.yaml, statusline.yaml, sunset.yaml, system.yaml, user.yaml, workflow.yaml
│   └── evaluator-profiles/
├── specs/                       # SPEC 문서 저장소
│   └── SPEC-{DOMAIN}-{NUM}/
│       ├── spec.md
│       ├── plan.md
│       ├── acceptance.md
│       └── progress.md
├── project/                     # 프로젝트 문서 (deliverable)
│   ├── product.md              # 제품 개요
│   ├── structure.md            # 이 파일
│   ├── tech.md                 # 기술 스택
│   ├── codemaps/
│   │   ├── overview.md
│   │   ├── modules.md
│   │   ├── dependencies.md
│   │   ├── entry-points.md
│   │   └── data-flow.md
│   ├── brand/
│   │   ├── target-audience.md
│   │   ├── visual-identity.md
│   │   └── brand-voice.md
│   └── db/
│       ├── schema.md
│       ├── migrations.md
│       └── ...
├── docs/                        # 문서 및 참고
│   ├── MCP_OAUTH_SETUP.md
│   ├── agent-lint.md
│   └── generic-patterns-guide.md
├── reports/                     # 보고서 및 분석
│   ├── design-moai-plugin-v2-2026-07-08.md
│   └── ... (세션별 보고서)
├── state/                       # 런타임 상태
│   ├── active-sessions.json
│   ├── context-usage.json
│   └── ...
└── logs/                        # 추적 및 로그
    ├── trace-*.jsonl
    └── ...
```

## 웹사이트 디렉토리 구조 (544 files)

```
www/
├── hugo.toml                    # Hugo 설정 (version SSOT: 2.27.0)
├── vercel.json                  # Vercel 배포 설정
├── content/                     # Markdown 콘텐츠
│   ├── _index.md                # 홈페이지
│   ├── getting-started/         # 4개 가이드
│   ├── chat/                    # Chat 섹션 (8개)
│   ├── cowork/                  # Cowork 섹션 (20개)
│   ├── design/                  # Design 섹션 (11개)
│   ├── code/                    # Code 섹션 (3개)
│   ├── cli/                     # CLI 축 (22개)
│   ├── help/                    # 도움말 및 Office (11개)
│   ├── cookbook/                # 쿡북 및 트랙 (39개)
│   ├── plugins/                 # 플러그인 카탈로그 (5개)
│   └── releases/                # 릴리스 노트 (38개)
├── data/
│   ├── menu/
│   │   └── main.yaml            # 2축 IA 네비게이션 (데스크탑 + CLI)
│   └── ...
├── layouts/                     # Hugo 레이아웃 템플릿
├── assets/                      # CSS/SCSS 자산
├── static/                      # 정적 자산 (이미지 등)
├── themes/
│   └── hugo-geekdoc/            # vendored 테마 (FROZEN)
├── design-system/               # 13개 HTML 참고 (standalone)
└── scripts/
    └── check-links.mjs          # 내부 링크 검증 (Node.js ESM)
```

## 스크립트 디렉토리 (18 files)

```
scripts/
├── ci-mirror/                   # 로컬 CI 미러
│   ├── run.sh                   # CI 명령어 실행
│   └── ... (Go/Python/Shell 검증)
└── ...
```

## 모듈 경계

### 플러그인 모듈 경계
- **moai-coworker**: 실무(8 도메인) + 창작(4 분야) 전담
- **moai-designer**: 디자인 토큰 + Claude Design 연동 전담
- **moai-coder**: MoAI-ADK SPEC/DDD/TDD 전담
- **moai-pm**: 프로젝트 초기화 및 진입 라우팅 전담

### Claude Code 모듈 경계
- **agents/moai**: 7개 에이전트 (manager 4 + auditor 2 + builder 1; Explore는 Anthropic 내장이라 파일 없음)
- **rules/moai**: 규칙 문서 (core, workflow, development, languages, quality, design)
- **skills/moai**: 워크플로우 스킬 (plan, run, sync, project, harness, ...)
- **hooks/moai**: 깃/Claude Code 훅 (gateguard, quality gate, MX tag, ...)

### 웹사이트 IA 경계
- **Desktop axis**: 비개발자 학습 경로 (Chat → Cowork → Design → Code)
- **CLI axis**: 개발자용 5섹션 (시작하기·개념·일상·MoAI-ADK·레퍼런스)
- **Shared bottom**: 도움말·쿡북·트랙·릴리스 (양쪽 공유)

### 설정 파일 계층
- **Project-level** (`.claude/settings.json`, `.moai/config/`): 프로젝트별 규칙·설정
- **User-level** (`~/.claude/settings.json`, 메모리): 사용자 개인 선호도
- **System-level** (Claude Code builtin): 애플리케이션 기본값

---

**마지막 갱신**: 2026-07-09  
**추적 파일**: 2,258개  
**총 크기**: ~267MB (전체, www/themes 포함)
