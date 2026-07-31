---
title: 모두의 클로드 — 기술 스택
description: 기술 스택, 프레임워크 선택 근거, 개발 환경, 빌드 및 배포 설정
last_updated: 2026-07-09
---

# 모두의 클로드 기술 스택

## 핵심 기술 선택

### 프로젝트 유형
**컴파일 불필요**: 모든 소스는 마크다운, YAML/TOML/JSON, Bash 쉘 스크립트, 단일 Node.js ESM 스크립트로 구성. Go/Python/TypeScript 컴파일 소스 없음.

### 이유
- **신속한 배포**: 소스 컴파일 없이 깃 푸시 → 자동 배포
- **저장소 투명성**: 모든 소스를 직접 검토 가능
- **낮은 의존성**: 런타임 라이브러리 최소화

## 콘텐츠 계층

### Markdown + YAML/TOML/JSON
- **CLAUDE.md** (24KB): Claude Code 실행 지침 및 규칙 SSOT
- **SPEC 문서**: GEARS 형식 요구사항 (spec.md, plan.md, acceptance.md)
- **Hugo 콘텐츠**: 웹사이트 페이지 (www/content/)
- **설정**: 프로젝트·사용자 설정 (yaml, json, toml)

### Hugo 정적 사이트 생성기
- **버전**: 0.160.1 (www/vercel.json에 고정)
- **테마**: hugo-geekdoc (vendored, 수정 불가 FROZEN)
- **언어**: Go 템플릿
- **하이라이팅**: tokyonight-night 스타일
- **빌드 명령**: `hugo --gc --minify --enableGitInfo=false`
- **출력**: `public/` 디렉토리
- **기능**:
  - CJK 언어 지원 (hasCJKLanguage: true)
  - 검색 인덱싱 (SEARCH output format)
  - RSS 피드
  - Sitemap 생성

### Node.js 유틸리티
- **내부 링크 검증**: www/scripts/check-links.mjs (ESM)
- **런타임**: Node.js (버전 제약 없음)
- **목적**: Hugo 빌드 후 내부 링크 검증

### Bash 쉘 스크립트
- **CI 미러**: scripts/ci-mirror/run.sh (로컬 검증)
- **훅**: .claude/hooks/moai/*.sh (깃 훅 및 Claude Code 훅)
- **배포**: 플러그인 내 setup/cleanup 스크립트

## 웹 플랫폼 통합

### 배포: Vercel
- **Git Integration**: claude.mo.ai.kr 저장소 자동 감시
- **빌드 설정** (vercel.json):
  ```json
  {
    "framework": "hugo",
    "buildCommand": "hugo --gc --minify --enableGitInfo=false",
    "outputDirectory": "public"
  }
  ```
- **리다이렉트**:
  - cowork.mo.ai.kr → claude.mo.ai.kr (301)
  - /claude-design/* → /design/* (301)
- **보안 헤더**: 자동 추가 (X-Frame-Options, X-Content-Type-Options, Referrer-Policy)

### 도메인 및 HTTPS
- **기본 도메인**: https://claude.mo.ai.kr/
- **HTTPS**: Vercel 자동 관리

### 빌드 성능
- **Page 수**: ~228개 (모든 섹션 포함)
- **출력 크기**: 공개되지 않음 (Vercel 기본값)

## MCP 통합

### .mcp.json 설정
```json
{
  "mcpServers": {
    "context7": {
      "alwaysLoad": true,
      "command": "/bin/bash",
      "args": ["-l", "-c", "exec npx -y @upstash/context7-mcp@latest"]
    }
  }
}
```

### 지원 MCP 서버
- **context7**: 공식 라이브러리 문서 조회 (alwaysLoad: true, .mcp.json에 정의됨)
- **GLM 백엔드** (moai glm 모드):
  - zai-mcp-server (비전)
  - web_search_prime (웹 검색)
  - web_reader (웹 읽기)

## 버전 SSOT 위치

### 마켓플레이스 메타데이터
```json
// .claude-plugin/marketplace.json
"metadata": {
  "version": "5.0.0",   // ← 마켓 메타 버전 (모든 플러그인 공통)
  "language": "ko",
  "license": "Apache-2.0"
}
```

### 플러그인별 버전
```json
// plugins/moai-coworker/.claude-plugin/plugin.json
{ "version": "5.0.0" }   // ← 코워커

// plugins/moai-designer/.claude-plugin/plugin.json
{ "version": "0.2.0" }   // ← 디자이너

// plugins/moai-coder/.claude-plugin/plugin.json
{ "version": "3.1.0" }   // ← 코더

// plugins/moai-pm/.claude-plugin/plugin.json
{ "version": "0.2.0" }   // ← PM
```

### 웹사이트 버전
```toml
// www/hugo.toml
[params]
  version = "2.27.0"     // ← 웹사이트 릴리스 번호
  releaseDate = "2026-06-19"
```

### CHANGELOG
```markdown
// CHANGELOG.md
## [Unreleased]
```
(세부 버전 헤딩은 Conventional Commits 기반 자동 생성)

## 설정 소유권

### Claude Code 설정
- **.claude/settings.json** (프로젝트): 권한(permissions), 훅(hooks), outputStyle
- **~/.claude/settings.json** (사용자): 테마, 모델, 글꼴
- **내부 기본값**: Claude Code 애플리케이션

### MoAI-ADK 설정
- **.moai/config/sections/** (27개 yaml): 프로젝트 규칙
  - cache.yaml, constitution.yaml, context.yaml, db.yaml, design.yaml, feedback.yaml, git-convention.yaml, git-strategy.yaml, handoff.yaml, harness.yaml, interview.yaml, language.yaml, llm.yaml, lsp.yaml, mx.yaml, observability.yaml, project.yaml, quality.yaml, ralph.yaml, research.yaml, security.yaml, state.yaml, statusline.yaml, sunset.yaml, system.yaml, user.yaml, workflow.yaml
- **.moai/config/evaluator-profiles/**: 평가자 역할 정의
- **선행 순서**: user → language → quality → ... (문서 참고)

### 깃 설정
- **.gitignore**: tracked files 제외 (generated, caches, secrets)
- **Conventional Commits**: 커밋 메시지 규칙 (feat, fix, docs, chore, ...)
- **언어**: 한국어 제목, 영어 본문 권장

## 로컬 개발 환경

### 요구사항
- **Git**: 최신 버전
- **Hugo extended**: 0.160.1 (정확히)
- **Node.js**: 14+ (link-checker용)
- **Bash**: 4+ (스크립트 호환성)
- **Claude Code**: 최신 버전 권장

### 로컬 빌드
```bash
# 웹사이트 빌드
cd www && hugo --gc --minify

# 링크 검증
node scripts/check-links.mjs

# 플러그인 검증
./scripts/ci-mirror/run.sh
```

### Makefile 대상
```bash
make help              # 대상 목록
make ci-local         # 로컬 CI 실행 (lint + vet + test)
make pr-merge PR=123  # GitHub PR 자동 병합 활성화
```

## 의존성 관리

### 외부 패키지 (최소화 원칙)
- **Hugo 테마**: hugo-geekdoc (vendored, 업데이트 불가)
- **폰트**: 구름 산스 코드 (SIL OFL) — code/mono 유일 추천
- **CDN 예외**: 한국어 가독성을 위한 폰트 CDN만 허용

### 설치 불필요
- MCP 서버는 `npx` (npx @upstash/context7-mcp) 형태로 on-demand 설치
- 플러그인 자산은 모두 repo 내 포함 (외부 다운로드 불필요)

## 보안 및 라이선스

### 라이선스
- **프로젝트 전체**: Apache-2.0
  - NC: 비상업적 사용 (Non-Commercial)
  - ND: 파생 금지 (No Derivatives)

### 민감 데이터
- **세션 상태**: .moai/state/ (버전 제어 제외)

### 보안 헤더 (vercel.json)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- Referrer-Policy: strict-origin-when-cross-origin

## CI/CD 파이프라인

### GitHub Actions
- **.github/workflows/label-sync.yml**: 라벨 동기화만 (build/test/deploy 없음)

### Vercel 자동 배포
1. `git push` → GitHub
2. Vercel 감지 → Hugo 빌드 자동 실행
3. `public/` 배포 → claude.mo.ai.kr 온라인

### 로컬 검증
```bash
./scripts/ci-mirror/run.sh
```
(실제 CI는 Vercel에서 수행)

## 프로토콜 및 표준

### 커밋 메시지
```
<type>(SPEC-ID or scope): <description>

<body>

<footer>
```
- **타입**: feat, fix, docs, chore, refactor, test, security
- **SPEC 추적**: 모든 커밋이 SPEC-ID 참조 권장
- **Co-Authored-By**: user.name이 비어있으면 생략

### 문서 형식
- **Markdown**: CommonMark + Hugo 확장 (shortcodes, etc.)
- **YAML**: 2-space indent
- **JSON**: no comments (설정용)
- **TOML**: Hugo 표준

### 응답 스타일
- **MoAI 스타일** (기본): 구조화된 보고서, 마크다운 테이블
- **MoAI-Easy 스타일**: 간소화된 응답
- **Einstein 스타일**: 시각적·상징적 강조

---

**마지막 갱신**: 2026-07-09  
**Hugo 버전**: 0.160.1 (pinned)  
**Node.js 버전**: 14+ (flexible)  
**배포 플랫폼**: Vercel
