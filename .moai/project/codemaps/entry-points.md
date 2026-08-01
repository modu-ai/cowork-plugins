---
title: 모두의 클로드 — 진입점
description: 사용자 진입점, 커맨드, 웹 경로, 마켓플레이스
last_updated: 2026-07-09
---

# 모두의 클로드 진입점

## 사용자 설치 경로

### 1단계: 플러그인 설치
```bash
# Claude Code에서:
/plugin marketplace add modu-ai/claude

# 또는 수동 경로:
Claude Desktop
  → Marketplace
     → Search "moai-claude"
        → Install
```

**결과**: 4개 플러그인이 claude plugin cache에 설치됨
- moai-coworker (193 skills)
- moai-designer (11 skills + 6 commands)
- moai-coder (29 skills + 8 agents)
- moai-pm (1 skill: /project)

---

### 2단계: 프로젝트 초기화 (선택)
```bash
# Claude Code에서:
/project

# 출력:
✓ CLAUDE.md 스캐폴드 (project root)
✓ .moai/config/ 설정 생성
✓ .moai/specs/ SPEC 저장소 초기화
```

**결과**: 프로젝트가 T2 수준으로 upgrade (로컬 Claude Code 사용 준비 완료).

**미래 계획 (v2)**: .claude/settings.json 마켓 선언 자동 추가 및 Web 세션 활성화 지원

---

## 4개 플러그인 진입점

### 모이-코워커
**진입**: 자연어 요청 (자동 라우팅)
```
사용자: "마케팅 캠페인 기획서 작성해줄래?"
  ↓ (coworker 자동 매칭)
→ skills/marketing-campaign-planner/ 스킬 호출
  ↓
→ 캠페인 기획서 생성
```

**직접 커맨드**:
- `/story-project [웹툰명]` → 창작 워크플로우
- 일반 도메인 스킬: 자동 활성화 (컨텍스트 기반)

### 모이-디자이너
**진입**: 자연어 또는 커맨드
```
사용자: "브랜드 디자인 시스템 만들어줄래?"
  ↓ (designer 자동 인식)
→ Claude Design 연동
  ↓
→ DESIGN.md + 디자인 토큰 생성
```

**직접 커맨드** (6개 독립 명령):
- `/brief` — 브리프 작성
- `/check` — 디자인 검증
- `/design` — 디자인 생성 (Path A/B 라우터)
- `/import` — 디자인 임포트
- `/system` — 디자인 시스템 관리
- `/tokens` — 디자인 토큰 관리

### 모이-코더
**진입**: `/moai:plan`, `/moai:run`, `/moai:sync`
```
사용자: "/moai:plan 로그인 기능 추가"
  ↓
→ manager-spec: SPEC 생성
  ├── GEARS 형식 요구사항
  ├── .moai/specs/SPEC-ID/ 저장
  └── plan-auditor: 검토

사용자: "/moai:run SPEC-MOC-AUTH-001"
  ↓
→ manager-develop: 구현
  ├── DDD/TDD 순환
  ├── 품질 게이트 검증
  └── progress.md 갱신

사용자: "/moai:sync SPEC-MOC-AUTH-001"
  ↓
→ manager-docs: 동기화
  ├── CHANGELOG 생성
  ├── README 갱신
  └── PR 생성
```

### 모이-PM
**진입**: `/project` 명령
```
/project
  ├── --cowork     → Cowork 스캐폴드
  ├── --designer   → Design 시스템 초기화
  ├── --code       → SPEC 체계 초기화
  └── (default)    → 프로젝트 스캐폴드 (.claude/ + .moai/)
```

---

## 웹 명령어 진입점

### /moai 마스터 커맨드
```bash
/moai plan "user story"           # → SPEC 생성
/moai run SPEC-ID                 # → 구현 시작
/moai sync SPEC-ID                # → 문서 동기화
/moai review                       # → 코드 검토
/moai harness [setup|status]      # → 하네스 관리
/moai project [--code|--designer|--cowork]  # → 프로젝트 초기화
/moai loop [frequency] [command]  # → 반복 실행
/moai clean                        # → 죽은 코드 제거
/moai mx                           # → @MX 태그 추가
/moai gate                         # → 품질 게이트 실행
/moai codemaps                     # → 아키텍처 맵 생성
/moai feedback                     # → 피드백 수집
```

### 슬래시 커맨드 (Domain-specific)
```
/brief                              # moai-designer (브리프 작성)
/check                              # moai-designer (디자인 검증)
/design                             # moai-designer (디자인 생성)
/import                             # moai-designer (디자인 임포트)
/system                             # moai-designer (디자인 시스템 관리)
/tokens                             # moai-designer (디자인 토큰 관리)

/story-project [name]              # moai-coworker (창작 워크플로우)
```

---

## 웹사이트 진입점 (www/)

### 홈페이지
```
https://claude.mo.ai.kr/
  └── 1x1 그리드 모듈 (개요)
       ├── Get Started
       ├── Desktop Plugins
       ├── Web Support
       └── Documentation
```

### Desktop 축 (비개발자)
```
https://claude.mo.ai.kr/
  ├── /getting-started/
  │   ├── install (Claude Desktop 설치)
  │   └── first-task
  ├── /chat/
  │   ├── first-chat
  │   ├── prompts
  │   ├── projects
  │   ├── search-research
  │   └── features
  ├── /cowork/
  │   ├── intro
  │   ├── setup
  │   ├── patterns
  │   └── ...
  ├── /design/
  │   ├── getting-started
  │   ├── design-system
  │   └── ...
  └── /code/
      ├── install
      └── first-task
```

### CLI 축 (개발자)
```
https://claude.mo.ai.kr/cli/
  ├── /cli/start/
  │   ├── install (moai CLI)
  │   └── first-spec
  ├── /cli/concepts/
  │   ├── spec-system
  │   ├── ddd-tdd
  │   ├── trust5
  │   └── harness
  ├── /cli/daily/
  │   ├── daily-flow
  │   ├── prompts
  │   ├── tokens-cost
  │   └── debugging
  ├── /cli/moai-adk/
  │   ├── bridge
  │   ├── workflow-commands
  │   └── quality-commands
  └── /cli/reference/
      ├── cli-reference
      ├── multi-llm
      └── advanced
```

### 공유 하단
```
https://claude.mo.ai.kr/
  ├── /help/
  │   ├── about-claude
  │   ├── plans-billing
  │   ├── office (Office 통합)
  │   └── ...
  ├── /cookbook/
  │   ├── skill-chaining
  │   ├── automation-recipes
  │   ├── blog-pipeline
  │   └── ... (39개 파일)
  ├── /cookbook/tracks/
  │   ├── track-data
  │   ├── track-documents
  │   └── ...
  └── /releases/
      ├── v2.27.0 (latest)
      ├── v2.26.0
      └── ... (38개 버전)
```

### 플러그인 카탈로그
```
https://claude.mo.ai.kr/plugins/
  ├── /plugins/chat (스킬·플러그인 활용)
  ├── /plugins/cowork (코워커)
  ├── /plugins/design (디자이너)
  └── /plugins/code (코더)
```

---

## Makefile 대상

```bash
make help              # 대상 목록 표시
make ci-local         # 로컬 CI 실행
make pr-merge PR=N    # GitHub PR 자동 병합 활성화
```

---

## Git 훅 진입점

### Pre-commit 훅
```bash
.git/hooks/pre-commit
  ├── (currently dormant — no-op)
  └── can be enabled for linting
```

### Claude Code 훅
```
.claude/settings.json
  ├── PreToolUse (Bash 위험 경고)
  ├── PostToolUse (상태 변경 감시)
  ├── Stop (세션 종료 전 검증)
  └── SessionStart (헬스 체크)
```

---

## 마켓플레이스 진입점

### Claude Code 공식 마켓플레이스
```
Claude Code
  → /plugin marketplace
     → Search "moai-claude"
        → Install
```

**마켓 엔트리**: `modu-ai/claude`
- **모든 플러그인 한번에 설치** (moai-coworker + moai-designer + moai-coder + moai-pm)
- 버전: 5.0.0
- 언어: 한국어 (ko)

### 개별 설치 불가능
- 마켓플레이스 정책상 4개 플러그인을 번들로 제공
- 각 플러그인은 독립 업데이트 가능 (plugin.json 버전 분리)

---

## 원격 세션 진입점 (Web)

### claude.ai/code 세션
```
https://claude.ai/code
  └── moai-claude 플러그인 Web 활성화 지원 계획 (v2 재설계)
       (현재는 미구현; .claude/settings.json 마켓 선언 메커니즘 개발 진행 중)
```

### 제약
- 바이너리 설치 불가 (T3 기능 제외)
- 훅 실행 제한 (Vercel 샌드박스)
- 프로젝트 커밋 필수 (T2 레벨)

---

## 환경 변수 진입점

### 중요 환경 변수
```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1   # Agent Teams 활성화
CLAUDE_CODE_REMOTE=true                   # Web 세션 감지 (자동)
CLAUDE_PLUGIN_DATA=$path                  # 플러그인 데이터 경로 (자동)
```

---

**마지막 갱신**: 2026-07-09  
**총 진입점**: 50+ (웹 경로 + 명령어 + 마켓플레이스)
