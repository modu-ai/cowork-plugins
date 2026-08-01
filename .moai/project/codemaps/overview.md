---
title: 모두의 클로드 — 아키텍처 개요
description: 전체 아키텍처, 설계 패턴, 시스템 경계
last_updated: 2026-07-09
---

# 모두의 클로드 아키텍처 개요

## 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│ Claude Code 클라이언트 (Desktop, Web, CLI)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Project-scope Layer (.claude/ + .moai/)                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ CLAUDE.md (규칙 + 에이전트 정의)                        │ │
│  │ .claude/agents (8개 에이전트)                           │ │
│  │ .claude/rules (core + workflow + development)         │ │
│  │ .moai/config (설정 + language.yaml)                    │ │
│  │ .moai/specs (SPEC plan → run → sync)                  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  Plugin Layer (marketplace)                               │
│  ┌────────────────┬────────────────┬────────────────┬───┐ │
│  │ moai-coworker  │ moai-designer  │ moai-coder     │PM │ │
│  │ 193 skills     │ 11 skills      │ 29 skills      │   │ │
│  │ 8 domains      │ 6 commands     │ 14 commands    │   │ │
│  │ + creativity   │ + GAN loop     │ + 8 agents     │   │ │
│  └────────────────┴────────────────┴────────────────┴───┘ │
│                          ↓                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ claude plugin marketplace add modu-ai/claude       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 문서 웹사이트 (https://claude.mo.ai.kr/)                      │
├─────────────────────────────────────────────────────────────┤
│ Hugo 정적 생성 (0.160.1)                                     │
│  → Desktop axis (비개발자): Chat → Cowork → Design → Code  │
│  → CLI axis (개발자): 시작·개념·일상·MoAI-ADK·레퍼런스      │
│  → Shared: 도움말·쿡북·트랙·릴리스 (228 페이지)              │
└─────────────────────────────────────────────────────────────┘
```

## 3계층 설계

### Layer 1: 플러그인 네이티브 (현재 플러그인명: moai-coder, moai-designer 등)
**위치**: `plugins/moai-{coworker|designer|coder|pm}/`

> **미래 계획 (v2 재설계)**: 플러그인명 변경 예정 (moai-coder → moai 등)

**책임**:
- 스킬 정의 및 도메인별 전문성 제공
- 에이전트 및 커맨드 라우팅
- MCP 통합 (context7 on-demand)
- 훅 및 품질 게이트 정의
- 플러그인별 고유 기능 제공

**특징**:
- **마켓플레이스 배포**: moai-claude 번들을 통해 4개 플러그인 함께 설치 (마켓플레이스 정책상 별도 개별 설치 불가)
- **독립 버전 관리**: 플러그인별 독립 버전 관리 (coworker 5.0.0 ≠ designer 0.2.0 ≠ coder 3.1.0)

### Layer 2: 스캐폴드 페이로드 (`/moai:project` 생성)
**위치**: 프로젝트 루트 (`.claude/`, `.moai/`)

**책임**:
- 프로젝트 전용 규칙 및 헌법 (CLAUDE.md, rules/)
- 설정 (language.yaml, quality.yaml, etc.)
- SPEC 문서 저장소 및 진행 추적
- 프로젝트 브랜딩 및 메모리

**특징**:
- **일회성 생성**: `/moai:project` 명령이 한 번에 생성 (현재 구현)
- **Web 활성화 예정 (v2)**: 미래에 `.claude/settings.json` 마켓 선언이 Web/원격 세션에서 플러그인 활성화 예정
- **사용자 설정 병합**: 기존 프로젝트 설정 보존하며 병합

### Layer 3: 모이 바이너리 (T3 전용)
**위치**: `~/.local/bin/moai` (설치 시)

**책임**:
- statusline 렌더링
- 세션 레지스트리
- 하네스 학습 및 버전 관리
- SPEC 감시 및 lint
- 진단(doctor) 헬스 체크 — 프로젝트 상태 검증

**특징**:
- **CLI·Desktop 전용**: Web 세션에서는 설치 불가
- **선택 사항**: 없어도 플러그인 기능 동작 (T1/T2 티어)

## SPEC 기반 개발 워크플로우

```
User Request
    ↓
[Plan] /moai:plan "description"
├── manager-spec 분석
├── GEARS 형식 요구사항 생성
├── .moai/specs/SPEC-ID/ 문서화
└── Output: spec.md, plan.md, acceptance.md
    ↓
[Plan Audit] plan-auditor 독립 검토
    ↓
[Run] /moai:run SPEC-ID
├── manager-develop ANALYZE·PRESERVE·IMPROVE
├── DDD/TDD 순환 (cycle_type)
├── 품질 게이트 검증 (TRUST 5)
└── Output: 구현된 코드 + progress.md
    ↓
[Sync] /moai:sync SPEC-ID
├── manager-docs 문서 동기화
├── CHANGELOG 자동 생성
├── README 갱신
└── Output: PR + merge
    ↓
[Sync Audit] sync-auditor 최종 검토
```

## 설계 패턴

### 1. 플러그인 라우팅 패턴
```
자연어 입력
    ↓
[모이-PM의 /project]
    ├── --cowork → moai-coworker 초기화
    ├── --designer → moai-designer 초기화
    ├── --code → moai-coder 초기화
    └── (기본) → 프로젝트 스캐폴드
```

### 2. 에이전트 위임 패턴
```
Orchestrator (main thread)
    ├── Context-First Discovery (AskUserQuestion)
    ├── Agent(manager-spec) → SPEC 생성
    ├── Agent(plan-auditor) → 독립 검토
    ├── Agent(manager-develop) → 구현
    ├── Agent(manager-docs) → 동기화
    └── Agent(manager-git) → PR 생성
```

### 3. 계층 간 메시지 전달
```
Layer 1 (Plugin)
    ↓ [skill 호출]
Orchestrator + Project Config (Layer 2)
    ↓ [SPEC ID + context]
Layer 3 (moai CLI, optional)
    ↓ [statusline, session registry]
```

## 시스템 경계

### 경계 1: 플러그인 경계
- **moai-coworker**: 실무 8 도메인 + 창작 4 분야 (독립 실행 가능)
- **moai-designer**: 디자인 토큰 + Claude Design (독립 실행 가능)
- **moai-coder**: SPEC/DDD/TDD 개발 (독립 실행 가능)
- **moai-pm**: 진입 라우터 (다른 플러그인 호출)

### 경계 2: 세션 경계
```
┌─────────────────────────────────────────────────────┐
│ CLI 세션 (로컬)                                      │
│  → 모든 기능 (T3 포함) + 바이너리 설치 가능          │
├─────────────────────────────────────────────────────┤
│ Desktop 로컬 세션                                    │
│  → 모든 기능 (T1/T2 + T3 선택) + 훅 동작            │
├─────────────────────────────────────────────────────┤
│ Web/원격 세션 (claude.ai/code)                       │
│  → T2까지 (프로젝트 커밋 필수) + 훅 제한            │
│  → 바이너리 설치 불가                               │
└─────────────────────────────────────────────────────┘
```

### 경계 3: 설정 계층
```
System Defaults (Claude Code)
    ↓ override
User Settings (~/.claude/)
    ↓ override
Project Settings (.claude/ + .moai/)
    ↓ Final Config
```

## 핵심 설계 결정

### 1. 4-플러그인 패밀리 (vs 단일 통합)
**이유**: 도메인 특화 가능, 사용자가 필요한 것만 선택, 병렬 업데이트

### 2. SPEC-First 워크플로우 (vs 즉석 코딩)
**이유**: 요구사항 명확화, 품질 보증, 추적 가능한 변경 이력

### 3. 계층적 Tier 설계 (T1/T2/T3)
**이유**: 사용자 진입 진입로 낮춤, Web 지원 점진적 확대, 바이너리 의존성 최소화

### 4. Slim-Scaffold (vs Full-Scaffold)
**이유**: 프로젝트 크기 축소, Web 세션 지원 단순화, 사용자 정의 보존

---

**마지막 갱신**: 2026-07-09  
**활발한 개발 상태**: moai v2 재설계 진행 중  
**Total System Files**: 2,258 tracked
