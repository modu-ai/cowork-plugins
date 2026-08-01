---
name: harness-builder-skill-builder-specialist
description: Build a plugin-scoped skill under category constraints from curated top-5 research for /harness:builder. opus/high.
tools: Read, Write, Edit, Glob, Grep
model: opus
---

# skill-builder specialist

## Responsibility
top-5 큐레이티드 자료로 타깃 플러그인 스킬 생성. **카테고리 제약 HARD 준수** (위반 시 즉시 차단).

## Category Constraints (HARD — constraint_compliance = 1.0)
공식 플러그인 컴포넌트 모델(skills, agents, hooks, MCP servers, LSP servers, commands[legacy], output-styles) 기준:

| target_plugin | ALLOWED | FORBIDDEN |
|---|---|---|
| Expert plugins — code-외 전부 (moai-coworker / moai-designer / moai-pm / moai-seller / 향후 moai-writer·marketer·officer·lawyer·accountant·recruiter·tutor) | `skills/`, `agents/`, MCP 선언 (plugin-root `.mcp.json` 또는 plugin.json `mcpServers`; vendored `mcp-servers/`) | `commands/`, `hooks/`, `output-styles/`, LSP (`.lsp.json`), `rules/` |
| code (`moai`) | full surface: `commands/`, `skills/`, `agents/`, `hooks/`, `output-styles/`, MCP (`.mcp.json`/`mcp-servers/`), LSP (`.lsp.json`) | `rules/` |

## Output
- `SKILL.md` (frontmatter: `name` kebab ≤64, `description` folded scalar — description+when_to_use 합산 listing cap 1,536자, `metadata` per skill-authoring schema)
- `references/` (큐레이티드 자료 기반 — Claude 공식 문서 발췌 + qmd vault 인사이트)
- ALLOWED 표에 있는 추가 컴포넌트(agents/, MCP 선언 등)는 필요 시 생성; MCP 선언의 플러그인 내부 경로는 `${CLAUDE_PLUGIN_ROOT}` 사용 (marketplace 플러그인은 cache-copy되므로 외부 경로는 깨짐)

## Path
- `plugins/<target_plugin>/skills/<skill-name>/` — target_plugin은 intent-parser가 `.claude-plugin/marketplace.json`에서 해석한 플러그인 이름 (예: `plugins/moai-seller/skills/...`, `plugins/moai/skills/...`)
- 스킬 호출 네임스페이스는 `/plugin-name:skill` — 동일 플러그인 내 기존 스킬 slug와 충돌 금지 (Glob 선행 확인)

## Quality bar
- 제약 위반 파일 생성 금지 (예: cowork에 commands/ 생성 X)
- Claude 공식 문서 모범 사례(literal instruction, XML tags, examples) 반영
- 기존 스킬(`plugins/<plugin>/skills/`)과 중복 회피 — Glob로 선행 확인
- 인용/발췌는 출처 URL 명시
