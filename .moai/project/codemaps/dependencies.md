---
title: 모두의 클로드 — 의존성 관계
description: 모듈 간 의존성, 외부 통합, 데이터 흐름
last_updated: 2026-07-09
---

# 모두의 클로드 의존성 관계

## 모듈 간 의존성

### 플러그인 의존성

```
moai-pm (router)
  ├── → moai-coworker (skill invocation)
  ├── → moai-designer (skill invocation)
  ├── → moai-coder (skill invocation)
  └── → /moai:project scaffold
       (generates .claude/ + .moai/ for all plugins)

moai-coworker
  ├── depends on: .moai/config (language.yaml, quality.yaml)
  ├── depends on: CLAUDE.md (project root — rules)
  └── independent skill execution

moai-designer
  ├── depends on: Claude Design system (external)
  ├── depends on: design-system configuration
  └── independent skill execution

moai-coder
  ├── depends on: .moai/specs/ (SPEC repository)
  ├── depends on: CLAUDE.md (agent definitions)
  ├── depends on: .claude/agents/ (8 agents)
  ├── depends on: .claude/rules/ (quality rules)
  ├── depends on: .claude/skills/ (skill catalog)
  ├── depends on: .moai/config/ (project config)
  └── depends on: context7 MCP (documentation)
```

### 에이전트 의존성

```
Orchestrator (main thread, CLAUDE.md)
  ├── uses: manager-spec → SPEC 생성
  ├── uses: plan-auditor → 검토
  ├── uses: manager-develop → 구현
  ├── uses: manager-docs → 동기화
  ├── uses: sync-auditor → 최종 검토
  ├── uses: manager-git → PR 생성
  ├── optional: builder-harness → 하네스
  └── optional: Explore → 분석

manager-spec
  ├── reads: .moai/config/ (language, project context)
  ├── reads: existing SPEC files (references)
  └── writes: .moai/specs/SPEC-ID/

manager-develop
  ├── reads: .moai/specs/SPEC-ID/ (requirements)
  ├── reads: .moai/config/ (quality gates, constitution)
  ├── reads: CLAUDE.md (rules)
  ├── reads: .claude/rules/ (domain rules)
  └── writes: implementation code

manager-docs
  ├── reads: .moai/specs/SPEC-ID/ (completed work)
  ├── reads: implementation results
  ├── reads: .moai/config/ (version SSOT)
  ├── writes: CHANGELOG.md
  ├── writes: README.md
  ├── writes: frontmatter updates
  └── writes: PR

plan-auditor & sync-auditor
  ├── reads: all project artifacts (SPEC, code, results)
  └── produces: verification matrix
```

## 마켓플레이스 의존성

```
.claude-plugin/marketplace.json (manifest)
  ├── declares: moai-coworker (source: ./plugins/moai-coworker)
  ├── declares: moai-designer (source: ./plugins/moai-designer)
  ├── declares: moai-coder (source: ./plugins/moai-coder)
  ├── declares: moai-pm (source: ./plugins/moai-pm)
  └── metadata: {version: 5.0.0, license, language}
       (↓ registered in Claude Code Marketplace)
       v Claude Code Marketplace (modu-ai/claude)
         (↓ user installs)
         Claude Code plugin cache
```

## 웹사이트 의존성

```
www/content/ (Markdown)
  ├── references: .moai/project/product.md (product info)
  ├── references: .moai/project/tech.md (tech stack)
  ├── imports: plugin metadata (moai-coworker, etc.)
  └── (↓ Hugo build)
      www/public/ (HTML)
        (↓ Vercel)
        https://claude.mo.ai.kr/

www/themes/hugo-geekdoc/ (vendored, FROZEN)
  ├── provides: layout templates
  ├── provides: CSS/JS assets
  └── no updates (locked to v0.x)

www/data/menu/main.yaml (navigation)
  └── defines: 2-axis IA (Desktop + CLI)
      (↓ Hugo shortcodes)
      rendered navigation on every page
```

## MCP 서버 의존성

### 설정: .mcp.json

```json
{
  "mcpServers": {
    "context7": {
      "command": "/bin/bash",
      "args": ["-l", "-c", "exec npx -y @upstash/context7-mcp@latest"],
      "alwaysLoad": true
    }
  },
  "staggeredStartup": {
    "enabled": true,
    "delayMs": 500
  }
}
```

### 사용 그래프

```
moai-coder / manager-develop
  ├── → context7 MCP (library docs lookup)
  │    └── → @upstash/context7-mcp
  │         └── → Internet (library database)
  └── (optional) → web search / Claude Design docs

moai-designer
  └── → context7 MCP (design system docs)

CLI/Desktop local sessions
  └── → moai CLI (T3)
       └── → .moai/state/ (session registry, context cache)

Web/Remote sessions (claude.ai/code)
  └── → 향후 계획 (v2 재설계)
       └── → 플러그인 Web 활성화 메커니즘 (현재는 미구현)
```

## 설정 계층 의존성

```
Claude Code Default Settings (built-in)
  ↓ override
User Settings (~/.claude/settings.json)
  ├── theme, model, font preferences
  └── personal memories
  ↓ override
Project Settings (.claude/settings.json)
  ├── outputStyle: "MoAI"
  ├── permissions (allow/deny)
  ├── hooks (definitions)
  └── MCP server 통합 설정
  ↓ override
MoAI Config Sections (.moai/config/sections/)
  ├── language.yaml (conversation_language, code_comments)
  ├── quality.yaml (constitution.development_mode)
  ├── git-convention.yaml, git-strategy.yaml
  └── ... (27개 전체, 위 3개 포함)
```

## 버전 의존성

### SSOT 버전 관계

```
.claude-plugin/marketplace.json
  └── metadata.version = "5.0.0"  ← Master version
       ├── → plugins/moai-coworker/.claude-plugin/plugin.json: "5.0.0" (aligned)
       ├── → plugins/moai-designer/.claude-plugin/plugin.json: "0.2.0" (independent)
       ├── → plugins/moai-coder/.claude-plugin/plugin.json: "3.1.0" (independent)
       └── → plugins/moai-pm/.claude-plugin/plugin.json: "0.2.0" (independent)

www/hugo.toml
  └── params.version = "2.27.0"  ← Website release
       └── divorced from plugin versions (separate cadence)

CHANGELOG.md
  └── tracks all versions (plugins + website)
       └── per Conventional Commits
```

### 호환성 제약

- Hugo: 0.160.1 (pinned, no upgrades)
- Node.js: 14+ (flexible, no pinning)
- Claude Code: 최신 버전 권장 (내장 명령 및 기능 호환성)
- MCP servers: on-demand `npx` (auto-latest, can pin if needed)

## Git 워크플로우 의존성

```
User commits to main
  ↓ (git push)
GitHub repository
  ├── triggers: Vercel hook (www/ build)
  │    └── → Hugo build → HTML → deploy to claude.mo.ai.kr
  ├── triggers: GitHub Actions (label-sync only)
  │    └── → EndBug/label-sync
  └── CI/CD: moai plugin export (CI mirror, optional local)
       └── → plugins/ → marketplace.json → PR
```

## 외부 통합 서비스

### Vercel (배포)
```
claude.mo.ai.kr repo
  → Vercel git integration
     ├── build: hugo --gc --minify
     ├── output: public/
     └── deploy: https://claude.mo.ai.kr/
```

### GitHub (저장소 + PR)
```
Local git repo
  → git push origin main
     ├── PR creation (manager-git agent)
     ├── CI/CD (label-sync, moai export)
     └── merges to main
```

### Claude Code Marketplace
```
plugins/ source code
  → .claude-plugin/marketplace.json
     → Claude Code Marketplace (modu-ai/claude)
        → user: claude plugin marketplace add modu-ai/claude
           → Claude Code downloads & installs
              → plugin cache (user/project scope)
                 → Desktop/로컬 세션에서 플러그인 로드
                    (Web 세션 활성화는 향후 계획)
```

## 외부 라이브러리 의존성

### 최소 의존성 원칙
- **제로 npm/pip/go dependencies**: 모든 스크립트와 설정이 자체 포함
- **On-demand MCP**: `npx @upstash/context7-mcp` (설치 불필요)
- **Hugo 테마**: vendored (업데이트 불가, 안정성 우선)
- **폰트**: CDN 포인트 (구름 산스 코드, SIL OFL)

### 이유
- 배포 단순화 (바이너리 컴파일 불필요)
- 보안 (의존성 감시 최소화)
- Web 세션 호환성 (외부 설치 불가)

---

**마지막 갱신**: 2026-07-09  
**외부 서비스**: Vercel + GitHub + Claude Marketplace  
**MCP 서버**: context7 (on-demand)
