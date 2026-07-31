---
title: 모두의 클로드 — 제품 개요
description: 모두의 클로드 monorepo의 제품 정의, 대상 사용자, 핵심 기능, 로드맵
last_updated: 2026-07-09
---

# 모두의 클로드 제품 개요

## 프로젝트 정의

**모두의 클로드**(modu-ai/claude)는 Claude Code 플러그인 마켓플레이스를 통해 배포되는 4개의 AI 직원 플러그인 패밀리이다. 실무, 디자인, 개발, 프로젝트 관리에 특화된 AI 동료들을 Claude Desktop에서 자연어로 활용할 수 있는 통합 플랫폼이다 (웹 세션 지원은 v2 재설계 계획).

- **프로젝트명**: 모두의 클로드 (modu-ai/claude)
- **배포 원천**: Claude Code 플러그인 마켓플레이스 (`moai-claude`, v5.0.0)
- **설치 명령**: `claude plugin marketplace add modu-ai/claude`
- **라이선스**: Apache-2.0 (산출물은 이용자 소유 — LICENSE-OUTPUT.md)
- **언어**: 한국어(ko)
- **활발한 개발 상태**: 예. 현재 4-플러그인 재설계 및 moai 플러그인 v2 대개명 진행 중

## 4-플러그인 AI 직원 패밀리

### 1. 모이-코워커 (moai-coworker)
- **버전**: 5.0.0
- **파일 수**: 546개
- **스킬 수**: 193개 (통합·올인원)
- **전문 분야**: 실무(사업·이커머스·마케팅·콘텐츠·법률·재무·HR·교육·미디어) + 콘텐츠 창작(웹툰·웹소설·시나리오·출판)
- **표시명**: 코워커
- **대상 사용자**: 실무 종사자, 콘텐츠 작가, 1인 창작자
- **특징**: 자연어 요청 시 도메인별 매칭 스킬이 자동 호출. story-project 스킬이 창작 워크플로우 라우팅

### 2. 모이-디자이너 (moai-designer)
- **버전**: 0.2.0
- **파일 수**: 112개
- **기능**: 11개 스킬 + 6개 커맨드 (에이전트는 2026-07-09 스킬 감사에서 제거됨)
- **전문 분야**: Claude Design 연동, 디자인 토큰(DTCG), DESIGN.md, 브랜드 시스템, GAN 품질 루프
- **표시명**: 디자이너
- **대상 사용자**: 브랜드 디자이너, 크리에이터
- **특징**: 브리프부터 핸드오프까지 한 번에 처리. 자연어 또는 design-* 스킬 호출로 동작

### 3. 모이-코더 (moai-coder)
- **버전**: 3.1.0
- **파일 수**: 354개
- **기능**: 29개 스킬 + 14개 커맨드 + 8개 에이전트 + 훅 + rules + output-styles
- **특징**: MoAI-ADK SPEC plan/run/sync 개발 방법론, DDD/TDD, 품질 게이트, 문서 동기화
- **표시명**: 코더
- **대상 사용자**: 개발자, 기술 창업자
- **특징**: moai CLI 무설치로 Claude Code/Desktop에서 동작. 비개발자와 개발자 모두 자연어로 개발 가능

### 4. 모이-PM (moai-pm)
- **버전**: 0.2.0
- **파일 수**: 17개
- **기능**: 1개 skill `/project` 라우터
- **전문 분야**: 프로젝트 초기화 허브
- **표시명**: PM
- **대상 사용자**: 비개발자, 프로젝트 시작자
- **특징**: `/project --cowork` / `--designer` / `--code` 플래그로 4개 AI 직원의 진입 라우팅. 비개발자도 자연어 한마디로 프로젝트 시작 가능

## 문서 사이트

**웹사이트**: https://claude.mo.ai.kr/ ("모두의 클로드", ko-KR)

### 2축 IA 구조
- **데스크탑 축** (비개발자용): 비개발자를 위한 학습 경로 시작하기 → Chat → Cowork → Design → Code → MoAI 플러그인 (학습 난이도 상승)
- **CLI 축** (개발자용): 5개 섹션 — 시작하기·핵심 개념·일상 사용·MoAI-ADK·레퍼런스

### 공통 하단 섹션
- 도움말 (Office 통합 포함)
- 쿡북 (39개 파일)
- 실전 트랙
- 릴리스 (38개 버전 문서)

### 콘텐츠 현황
- 총 228개 빌드 페이지
- CLI 22개, Cowork 20개, Design 11개, Help 11개, Chat 8개, 외 다수
- Hugo extended 0.160.1, theme hugo-geekdoc (vendored), Vercel 배포

## 핵심 기능

### 1. 통합 AI 직원 시스템
- 4개 전문 플러그인이 Claude Desktop 한 곳에서 자연어 요청으로 동작
- 플러그인 간 협업 가능 (PM의 `/project` 명령이 다른 직원 스킬 호출)
- 프로젝트별 설정으로 필요한 직원만 활성화 가능

### 2. 개발 방법론 (MoAI-ADK)
- SPEC-First DDD 워크플로우 (plan → run → sync)
- TRUST 5 품질 게이트 (Tested, Readable, Unified, Secured, Trackable)
- 자동 문서 생성 및 CHANGELOG 동기화
- Git worktree 기반 병렬 개발 지원

### 3. 마켓플레이스 통합
- Claude Code 공식 마켓플레이스를 통한 원클릭 설치
- 플러그인 업데이트 자동 배포
- 로컬 Desktop·CLI 지원 (웹 세션(claude.ai/code) 지원은 v2 재설계 계획 — 미구현)

### 4. 프로젝트 초기화 자동화
- `/project` 명령으로 CLAUDE.md, rules, .moai 체계 자동 스캐폴드
- 프로젝트 설정 병합(기존 사용자 설정 보존)
- Web 세션 지원을 위한 settings.json 마켓 선언 자동 추가는 v2 재설계 계획 (미구현, `.moai/reports/design-moai-plugin-v2-2026-07-08.md` §7)

## 사용 사례

### 실무자/콘텐츠 작가
- 코워커를 통해 8개 도메인(사업, 마케팅, 콘텐츠 등)의 도메인 전문 스킬 활용
- story-project 스킬로 웹툰, 웹소설, 시나리오 창작 워크플로우 자동화

### 브랜드 디자이너
- Claude Design 연동으로 디자인 시스템 구축 및 관리
- 브리프부터 핸드오프까지 한 번에 처리

### 개발자
- SPEC plan/run/sync 3단계로 요구사항·구현·문서를 체계적으로 관리
- 품질 게이트 자동 검증
- 프로젝트별 규칙·설정·선호도 자동 적용

### 프로젝트 시작자
- `/project` 한 명령으로 프로젝트 기반 자동 구성
- 가이드 기반 진입으로 비개발자도 접근 가능

## 현재 궤도 및 로드맵

### 진행 중 작업 (2026-07-09)
1. **4-플러그인 재설계**: 플러그인 구조 및 기능 최적화
2. **moai 플러그인 v2 대개명**: 기존 "code" 플러그인을 "moai"로 개명, 커맨드 `/moai:plan·run·sync` 템플릿 파리티 확보
   - D-1: 플러그인 이름을 "moai"로 개명 (displayName은 "코더" 유지)
   - D-2: Slim-Scaffold 모델 채택 (프로젝트 귀속 자산만 스캐폴드)
   - D-3: 현행 vendor export 유지 (moai-adk-go → CI → 단일 마켓 `moai-claude`)
   - D-4: 한국어 단일 export (다국어는 후속)
   - D-5: 플러그인 내 `agent` 키 미동봉 (opt-in 진입 경로는 P3 이후 검토)

### 미래 계획 (P1 이후)
- 다국어 지원 확대 (영어, 일본어, 중국어)
- 웹 세션 첫 접속 안정성 개선 (Claude Code issue #63028 해결 대기)
- 추가 도메인 스킬 확충
- 엔터프라이즈 기능 강화

## 버전 SSOT 위치

| 항목 | 파일 | 필드 |
|------|------|------|
| 마켓플레이스 메타데이터 | .claude-plugin/marketplace.json | metadata.version |
| 개별 플러그인 버전 | plugins/moai-{coworker\|designer\|coder\|pm}/.claude-plugin/plugin.json | version |
| 웹사이트 버전 | www/hugo.toml | params.version |
| CHANGELOG | CHANGELOG.md | [Unreleased] 섹션 |

## 기술 스택 및 제약

### 컴파일되지 않은 리소스
- Markdown + YAML/TOML/JSON 설정
- Hugo Go 템플릿 HTML
- Bash 쉘 스크립트
- 단일 Node.js ESM 스크립트 (www/scripts/check-links.mjs)

### 배포 환경
- **웹사이트**: Vercel git integration, Hugo 빌드, 보안 헤더 자동 추가
- **플러그인**: Claude Code 마켓플레이스 자동 배포

### 품질 관리
- 로컬 CI 미러 (scripts/ci-mirror/)
- Git 훅 (효과적으로 no-op)
- Conventional Commits 기반 CHANGELOG 자동 생성

---

**마지막 갱신**: 2026-07-09  
**상태**: 활발히 개발 중 (moai v2 재설계 진행)
