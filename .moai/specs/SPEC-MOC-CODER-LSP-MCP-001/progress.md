# Progress — SPEC-MOC-CODER-LSP-MCP-001

## §E.1 Plan-phase Audit-Ready Signal

- 2026-07-10: plan-phase artifact set authored by manager-spec (Tier M: spec.md, plan.md, acceptance.md, progress.md). Frontmatter `status: draft`. SPEC ID self-check: `SPEC-MOC-CODER-LSP-MCP-001` → regex PASS. Design decisions FINAL per 2-round Socratic interview; open design risks recorded in plan.md (8 items), unresolved by design. Interface contract with SPEC-MOC-PM-ADVISORS-001: catalog default path `plugins/moai/references/dev-mcp-catalog.json`.
- 2026-07-11 (iter-2, version 0.2.0): plan-auditor PASS-WITH-DEBT 0.81 hardening. Re-baselined §A.1 against committed `e06086c` tree (`.lsp.json` 5 flat keys go/python/rust/swift/typescript; `.mcp.json` context7-only; 5 gate scripts; `references/` absent, `templates/` present). Fixes F8-F13: F8 REQ-L-004 reworded as GEARS (candidate enumeration → plan.md §I table); F9 REQ-C-002 reworded to template+catalog deliverable + AC-CLM-013 deterministic instantiation gate; F10 AC-CLM-006 mechanized (synthetic SessionStart stdin, `"decision"`/`"block"` count == 0), AC-CLM-009/010/012 tightened; F11 M4 generation-template pinned to `plugins/moai/references/mcp-gen-template.json` (disjoint from M5 `templates/`); F12 marketplace.json single cross-SPEC owner = SPEC-1 M5 (baseline `.metadata.version` 6.2.0, `moai` entry 1.0.0), this SPEC hands the delta; F13 Out-of-Scope languages heading (elixir/scala/r/flutter). AC set now 13 machine gates.

## §F Phase 0.95 Mode Selection

- Date: 2026-07-11. Inputs: tier=M, scope ~10 files (plugins/moai/** JSON+shell+md), domains=3 (LSP config / hooks / MCP catalog+templates), language mix = JSON/shell/markdown (no Go), concurrency benefit = LOW (coding-heavy, M2-M5 file-disjoint but single-agent sequential is safe per Anthropic coding-task parallelism caveat), Agent Teams prereqs = NOT met (team.enabled default false).
- Mode evaluation: trivial NO (semantic scope) / background NO (writes files) / agent-team NO (capability gate fails) / parallel NO (coding-heavy) / workflow NO (<30 files, non-uniform transforms) / **sub-agent SELECTED**.
- Decision: sub-agent
- Justification: Run-phase is implementation-heavy with a verification-first M1 that gates M2-M5; sequential single manager-develop spawn (cycle_type=tdd, model=sonnet, effort=xhigh per plan.md §A) is the safe default per the coding-task parallelism caveat. Plan Audit Gate re-executed this session: run-gate PASS 0.88 (report: .moai/reports/plan-audit/SPEC-MOC-CODER-LSP-MCP-001-2026-07-11.md). Implementation Kickoff Approval: obtained in prior session (sequential implementation approved, sonnet xhigh, SPEC-2→SPEC-1 order; session 02e7a29f) — this session resumes that confirmed work via paste-ready handoff.

## §E.2 Run-phase Evidence

### M1 — Pre-flight verification pass (2026-07-11)

**Method**: no `WebFetch`/`WebSearch` tool was available in this agent's tool set (attempted, returned `Error: No such tool available`); per the MCP Fallback Strategy, verification research was performed via `curl` (Bash) against official upstream sources (GitHub raw READMEs, GitHub REST API for repo maintenance metadata, npm/RubyGems/Homebrew registries, and vendor docs sites) — this is the documented WebFetch-fallback path, not a training-data recall. Every `verified:` line below cites the exact URL consulted this session.

#### Baselines (captured before any write)

```
$ sha256sum plugins/moai/hooks/gates/*.sh plugins/moai/hooks/dispatch.sh
ee4ca51a1562fc882db766c8d0da1353b6bbb0539c24e368e83bc9a682041170  plugins/moai/hooks/gates/gateguard-fact-force.sh
cf7ba742942a87746da51cb838566606257714c937d22170735c0e9254779bf3  plugins/moai/hooks/gates/iggda-audit-preservation-guard.sh
92b339e55125804d74e1e6a22607d207a6bbd7c7e2b7775967ad2d0f189cb206  plugins/moai/hooks/gates/status-transition-ownership.sh
8da0b2cfcce8ba01c1b56e2848a5316f9f507aaaf32b74b19ec8aea36f1649f1  plugins/moai/hooks/gates/sync-phase-quality-gate.sh
ca97e5229956bd946c4799a58aa58113cd6372fc0b626a14148d223152aff34f  plugins/moai/hooks/gates/team-ac-verify.sh
43986069f01a59b90f851d7c1cd5e445447b671126b2eee297613cdd7ecc1906  plugins/moai/hooks/dispatch.sh
```

Marketplace baseline (read-only; NOT written by this SPEC): `.metadata.version` = `6.2.0`; `moai` plugin entry `.version` = `1.0.0` (also confirmed in `plugins/moai/.claude-plugin/plugin.json`).

#### Loader capability finding (resolves open risk #4 + #8)

`plugins/moai/skills/moai-foundation-cc/reference/claude-code-plugins-official.md` (lines 258-290, a MoAI-maintained summary of `https://code.claude.com/docs/en/plugins-reference`) documents the `.lsp.json` schema envelope: required `command` + `extensionToLanguage`; **optional** `args`, `env`, `transport`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `shutdownTimeout`, `restartOnCrash`, `maxRestarts`, `loggingConfig`. The doc's example also shows `${CLAUDE_PROJECT_DIR}` variable substitution inside the `env` block (`"PYTHONPATH": "${CLAUDE_PROJECT_DIR}"`), corroborating the same substitution pattern already used in this plugin's `hooks.json` (`${CLAUDE_PLUGIN_ROOT}`) and `.mcp.json`. **Finding**: the flat `command`/`args` schema DOES support `env` and `initializationOptions` as optional fields, so `jdtls` (which needs `JAVA_HOME` + a per-workspace `-data` directory) fits the existing flat schema without a wrapper script. Concrete decision: `args: ["-data", "${CLAUDE_PROJECT_DIR}/.jdtls-workspace"]` supplies the workspace dir via the same `${CLAUDE_PROJECT_DIR}` substitution token already demonstrated in this plugin's `hooks.json`/`.mcp.json`. `JAVA_HOME` is deliberately NOT set via an `env` block — there is no verified evidence that `.lsp.json` supports generic `${VAR}`-style pass-through of arbitrary host env vars (only the two known Claude-specific tokens `${CLAUDE_PROJECT_DIR}` / `${CLAUDE_PLUGIN_ROOT}` are confirmed); asserting `"env": {"JAVA_HOME": "${JAVA_HOME}"}` would be an unverified substitution claim. Instead the java entry relies on standard child-process environment inheritance (the spawned `jdtls` process inherits the launching shell's `JAVA_HOME` automatically, per jdtls's own README: "This should either be set in the JAVA_HOME environment variable, or on the user's PATH") — the install guide (M3) documents this precondition explicitly. This resolves open risk #4 (jdtls launch complexity) and open risk #8 (loader schema unknowns) in favor of the flat schema, with the env-inheritance caveat recorded here rather than asserted as a config field.

**Schema-shape note (non-defect, no blocker)**: the reference doc's example wraps entries under a top-level `"lspServers": {...}` key, but the live committed `plugins/moai/.lsp.json` (5 entries: go/python/rust/swift/typescript) is a FLAT object with no wrapper key, and `acceptance.md` AC-CLM-001/002/003 are written against the flat top-level-key shape (`jq -r 'keys[]' plugins/moai/.lsp.json`). Since the AC matrix (the run-phase verification SSOT) and the live tree agree on the flat shape, and REQ-L-001 requires the 5 existing entries preserved unchanged, this is treated as an intentional/tolerated shape (not a REQ-L-003-class defect) — M2 continues the flat shape for the 8 new entries, consistent with AC-CLM-001/002/003 and the existing 5.

#### HTML/CSS split decision (resolves open risk #1)

`vscode-langservers-extracted` (npm, verified `https://registry.npmjs.org/vscode-langservers-extracted/latest`, v4.10.0) ships **separate** binaries per language: `vscode-html-language-server`, `vscode-css-language-server` (plus json/markdown/eslint, out of scope here). Confirmed via the authoritative `nvim-lspconfig` launch configs (`https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/html.lua` and `.../lsp/cssls.lua`): both require the `--stdio` flag. **Decision: SPLIT into two `.lsp.json` keys, `html` and `css`** — final key count = 13 (5 existing + 6 new single-language: java/cpp/csharp/php/kotlin/ruby + 2 split: html/css).

#### Per-server verification (`verified:` lines — AC-CLM-004, ≥7 required, 8 provided)

verified: java (jdtls) — source `https://raw.githubusercontent.com/eclipse-jdtls/eclipse.jdt.ls/master/README.md` + `https://formulae.brew.sh/api/formula/jdtls.json` (stable 1.60.0, deps openjdk+python@3.14) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/jdtls.lua`. Binary: `jdtls` (Python wrapper script bundled with brew formula `homebrew/core/jdtls`). Requires `JAVA_HOME` env (Java 21 minimum) and a per-workspace `-data <dir>` arg. Install: `brew install jdtls` (macOS); Linux — search distro package repos for `jdtls`/`eclipse.jdt.ls`, or manual download from `http://download.eclipse.org/jdtls/milestones/`.

verified: cpp (clangd) — source `https://clangd.llvm.org/` (via `https://raw.githubusercontent.com/llvm/llvm-project/main/clang-tools-extra/clangd/README.md`) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/clangd.lua` (confirms `cmd = { "clangd" }`, no flags — defaults to stdio). No standalone `clangd` brew formula exists (`formulae.brew.sh/api/formula/clangd.json` → 404); clangd ships inside the `llvm` brew formula (`formulae.brew.sh/api/formula/llvm.json` → stable 22.1.8). Install: `brew install llvm` then add `$(brew --prefix llvm)/bin` to PATH (macOS); `apt install clangd` (Debian/Ubuntu).

verified: csharp (csharp-ls) — source `https://raw.githubusercontent.com/razzmatazz/csharp-language-server/master/README.md` + GitHub API maintenance check (`api.github.com/repos/razzmatazz/csharp-language-server`: not archived, pushed 2026-07-10, MIT license) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/csharp_ls.lua` (confirms `cmd = { "csharp-ls" }`, no flags). Chosen over OmniSharp (`api.github.com/repos/OmniSharp/omnisharp-roslyn`: not archived but 404 open issues, less actively triaged) per REQ-L-004/open-risk-#2 — csharp-ls is MIT-licensed, actively maintained (pushed today), and purpose-built for LSP. Install: `dotnet tool install --global csharp-ls` (requires .NET 10 SDK; cross-platform).

verified: php (phpactor) — source `https://raw.githubusercontent.com/phpactor/phpactor/master/README.md` + `https://phpactor.readthedocs.io/en/master/usage/standalone.html` (exact install commands) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/phpactor.lua` (confirms `cmd = { "phpactor", "language-server" }`). Chosen over intelephense (npm `intelephense@1.18.5`, license "SEE LICENSE IN LICENSE.txt" — has a paid-tier license gate for premium features) per REQ-L-004/open-risk-#5 — phpactor is MIT-licensed (`api.github.com/repos/phpactor/phpactor`: not archived, pushed 2026-07-05) and fully free. Install (no brew formula — `formulae.brew.sh/api/formula/phpactor.json` → 404): `curl -Lo phpactor.phar https://github.com/phpactor/phpactor/releases/latest/download/phpactor.phar && chmod a+x phpactor.phar && mv phpactor.phar ~/.local/bin/phpactor`.

verified: kotlin (kotlin-lsp) — source `https://raw.githubusercontent.com/Kotlin/kotlin-lsp/main/README.md` + `https://raw.githubusercontent.com/Kotlin/kotlin-lsp/main/scripts/neovim.md` (confirms `--stdio` flag: `cmd = { "kotlin-ls", "--stdio" }`) + GitHub API (`api.github.com/repos/Kotlin/kotlin-lsp`: not archived, pushed 2026-07-10). **Updated finding vs plan.md §I**: JetBrains now ships an OFFICIAL Kotlin LSP (`Kotlin/kotlin-lsp`, "JetBrains official project" badge), superseding the community `fwcd/kotlin-language-server` cited in the candidate table (verified stale: `api.github.com/repos/fwcd/kotlin-language-server` last pushed 2025-06-02, >13 months old). Chosen: official `Kotlin/kotlin-lsp` (currently Alpha-state per its own README, but JetBrains-official and actively maintained beats a 13-month-stale community project) — resolves open risk #3. Install: `brew install JetBrains/utils/kotlin-lsp` (macOS tap); manual: download+chmod+symlink `kotlin-lsp.sh` (Linux/other).

verified: ruby (ruby-lsp) — source `https://raw.githubusercontent.com/Shopify/ruby-lsp/main/README.md` + `https://rubygems.org/api/v1/gems/ruby-lsp.json` (v0.26.10) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/ruby_lsp.lua` (confirms `cmd = { "ruby-lsp" }`, no flags — standalone executable, no `require` needed). Chosen over solargraph (also actively maintained, `api.github.com/repos/castwide/solargraph` pushed 2026-07-10) per plan.md §I — ruby-lsp is the Shopify-backed community-standard default. Install: `gem install ruby-lsp` (cross-platform).

verified: html+css (vscode-langservers-extracted) — source `https://registry.npmjs.org/vscode-langservers-extracted/latest` (v4.10.0, bin map confirms separate `vscode-html-language-server`/`vscode-css-language-server` binaries) + `https://raw.githubusercontent.com/neovim/nvim-lspconfig/master/lsp/html.lua` + `.../lsp/cssls.lua` (both confirm `--stdio` flag requirement). Install: `npm install -g vscode-langservers-extracted` (cross-platform).

#### MCP catalog verification (REQ-C-003, 6 entries)

verified: playwright — source `https://raw.githubusercontent.com/microsoft/playwright-mcp/main/README.md`. Standard config: `{"command": "npx", "args": ["@playwright/mcp@latest"]}` (local stdio, Node.js 18+). Matches REQ-C-003 exactly.

verified: supabase — source `https://raw.githubusercontent.com/supabase-community/supabase-mcp/main/README.md` + `https://supabase.com/docs/guides/ai-tools/mcp` (security-risks page). Remote HTTP `{"type": "http", "url": "https://mcp.supabase.com/mcp"}`, OAuth-based client login. Verbatim warning text located: *"Remember to never connect the MCP server to production data. Supabase MCP is only designed for development and testing purposes."* — satisfies the REQ-C-003 dev/test-only warning (contains both `dev`/`test` and `prod` tokens per AC-CLM-010).

verified: vercel — source `https://vercel.com/docs/mcp/vercel-mcp` (JSON-LD/body text confirmed via curl+regex-strip): *"Vercel MCP is Vercel's official MCP server. It's a remote MCP with OAuth ... available at: https://mcp.vercel.com"*. Matches REQ-C-003 exactly (remote, OAuth, HTTP transport).

verified: neon — source `https://raw.githubusercontent.com/neondatabase-labs/mcp-server-neon/main/README.md`. Remote OAuth: `{"type": "http", "url": "https://mcp.neon.tech/mcp"}`. **Updated finding vs REQ-C-003's local-npx alternative**: the local npm package `@neondatabase/mcp-server-neon` (checked `https://registry.npmjs.org/@neondatabase/mcp-server-neon/latest`, v0.6.5) is now marked **deprecated** by its own registry metadata: *"This package is deprecated. Use the remote MCP server at mcp.neon.tech instead."* Catalog entry therefore records remote-OAuth as the sole/primary transport and documents the local npx form as a deprecated fallback (not the recommended path) — satisfies REQ-C-003's intent (remote OAuth OR local npx) while reflecting the current-state deprecation.

verified: railway — source `https://docs.railway.com/ai/mcp-server` (fetched via curl, JSON-LD + body text). Remote: `https://mcp.railway.com` (OAuth, no local install required). Local: via Railway CLI (`railway setup agent` / `railway mcp install`), NOT via a standalone npm MCP package. Confirmed npm-shim deprecation directly: `https://registry.npmjs.org/@railway/mcp-server` → `"deprecated": "Deprecated compatibility shim for Railway MCP"` (v0.1.12). Matches REQ-C-003's npm-shim note exactly.

verified: claude-in-chrome — built into Claude Code (no external server binary/URL); REQ-C-003 requires `entry_type: "guidance-only"`, no server entry generated. No external verification needed (platform-native capability, not a 3rd-party service to verify against upstream docs).

#### Final catalog path (interface handoff — SPEC-MOC-PM-ADVISORS-001 `design.md §H`)

Confirmed at the sibling SPEC's contract-default path, no deviation: `plugins/moai/references/dev-mcp-catalog.json` (M4) + `plugins/moai/references/mcp-gen-template.json` (M4, generation template — pinned under `references/`, disjoint from M5's `templates/**`).

### M2 — `.lsp.json` expansion (2026-07-11)

13 keys total (5 existing preserved byte-identical + 8 new: java/cpp/csharp/php/kotlin/ruby/html/css). AC-CLM-001 PASS (13 keys, no MISSING), AC-CLM-002 PASS (`true`), AC-CLM-003 PASS (5 existing commands unchanged: `gopls`/`pyright-langserver`/`rust-analyzer`/`sourcekit-lsp`/`typescript-language-server`). Commit: `71a17fa`.

### M3 — Install guidance + SessionStart advisory hook (2026-07-11)

`plugins/moai/references/lsp-install-guide.md` (13 H3 sections, `brew install` present — AC-CLM-005 PASS). `plugins/moai/hooks/gates/lsp-binary-advisory.sh` (new, additive) — `bash -n` clean, mechanized test `exit=0 db=0` (AC-CLM-006 PASS). `hooks.json` registered the new hook additively in the existing `SessionStart` matcher block (2nd hooks[] entry); `dispatch.sh` line and the 5 existing gate scripts verified byte-identical to the M1 sha256 baseline (AC-CLM-007 PASS — `diff` against baseline: IDENTICAL). Manual GWT S1 check: with a stripped `PATH` and full `jq` available, the hook correctly emitted `[moai-lsp-advisory] css: ...` / `html: ...` (the two servers genuinely absent from this dev machine) to stderr only — non-blocking, exit 0. Commit: `67d7958`.

### M4 — Dev-MCP catalog + generation template (2026-07-11)

`plugins/moai/references/dev-mcp-catalog.json` (6 servers, declarative). AC-CLM-009 PASS (valid JSON; name set == `claude-in-chrome,neon,playwright,railway,supabase,vercel`; every entry has `name` + (`transport` or `type`)). AC-CLM-010 PASS (supabase `.warning` contains verbatim dev/test-only + never-production wording; claude-in-chrome `.entry_type == "guidance-only"`). `plugins/moai/references/mcp-gen-template.json` created (pinned under `references/`, disjoint from M5's `templates/**`). AC-CLM-011 PASS (`grep` credential-literal scan over `references/` + `templates/`: exit 1, no matches — only `${NEON_API_KEY}` placeholder present).

**AC-CLM-013 reproducible instantiation command** (recorded per acceptance.md's reproducibility note):
```bash
T=plugins/moai/references/mcp-gen-template.json
jq --argjson sel '["playwright","neon"]' \
  '{mcpServers: (.mcpServers | with_entries(select(.key as $k | $sel | index($k) != null)))}' \
  "$T"
```
Verbatim output:
```json
{
  "mcpServers": {
    "playwright": { "command": "npx", "args": ["-y", "@playwright/mcp@latest"] },
    "neon": { "type": "http", "url": "https://mcp.neon.tech/mcp" }
  }
}
```
`.mcpServers | keys | join(",")` == `neon,playwright` (sorted); zero credential literals (only the URL/command fragments, no secrets). AC-CLM-013 PASS. AC-CLM-008 re-verified unaffected: `plugins/moai/.mcp.json` `.mcpServers | keys` still == `context7` only.

### M5 — Meta-harness templates (2026-07-11)

`plugins/moai/templates/claude/settings.project.json` extended with a `permissions.allow` baseline allowlist (REQ-H-001). `plugins/moai/templates/claude/hooks/quality-gate-hook.sh` added — a toolchain-auto-detecting project Stop-hook template (go/node/python/rust marker-file detection, graceful degradation, always exits 0; manually smoke-tested: `exit=0`). AC-CLM-012 PASS: settings template valid JSON with `permissions` key present; zero `SYNTAX:` lines across all `*hook*.sh` templates; `targethooks=0` (no template references `plugins/moai/hooks/` — REQ-H-002 confirmed). Commit: `2567130`.

### M6 — Docs delta + marketplace handoff + full AC batch (2026-07-11)

`plugins/moai/README.md` §코드 인텔리전스 rewritten (5-server table → 13-server/12-language table with per-language install one-liners + pointers to the new install guide and advisory hook) + new §Dev-service MCP 카탈로그 section (catalog + gen-template cross-reference, credential-never-bundled note).

**Marketplace entry-delta handoff (NO direct `marketplace.json` write — F12/§H single-owner discipline)**: this SPEC recommends `moai` plugin entry version bump `1.0.0 → 1.1.0` (semver MINOR — new backward-compatible capability: 8 new LSP servers, 1 new additive SessionStart advisory hook, 1 new meta-harness template + settings extension, 1 new dev-MCP catalog + generation template; zero breaking changes to existing 5 LSP entries, zero changes to plugin `.mcp.json`, zero changes to existing gate scripts/dispatch.sh). `plugins/moai/.claude-plugin/plugin.json`'s own `.version` field was likewise NOT touched by this SPEC (left for SPEC-MOC-PM-ADVISORS-001 M5 to bump in lockstep with the marketplace.json entry, since the two are conventionally kept in sync in this repo). Baseline re-confirmed unchanged this session: `.metadata.version` = `6.2.0`, `moai` entry = `1.0.0`.

**Full AC-CLM-001..013 batch (final re-run, verbatim evidence)** — persisted to `.moai/state/verify/SPEC-MOC-CODER-LSP-MCP-001/full-ac-batch.log`:

| AC | Status | Key evidence line |
|----|--------|--------------------|
| AC-CLM-001 | PASS | 13 keys total, no `MISSING:`, cpp/csharp/html+css all present |
| AC-CLM-002 | PASS | `true` |
| AC-CLM-003 | PASS | `gopls`/`pyright-langserver`/`rust-analyzer`/`sourcekit-lsp`/`typescript-language-server` unchanged |
| AC-CLM-004 | PASS | `grep -c "verified:"` = 15 (≥7 required) |
| AC-CLM-005 | PASS | 13 H3 sections; `brew install` found |
| AC-CLM-006 | PASS | `bash -n` OK; `exit=0 db=0` |
| AC-CLM-007 | PASS | sha256 `diff` vs M1 baseline: IDENTICAL |
| AC-CLM-008 | PASS | `context7` (unaffected) |
| AC-CLM-009 | PASS | valid JSON; names == `claude-in-chrome,neon,playwright,railway,supabase,vercel`; declarative check `true` |
| AC-CLM-010 | PASS | `PASS` (supabase warning dev/test+prod tokens; claude-in-chrome `entry_type` == `guidance-only`) |
| AC-CLM-011 | PASS | grep exit=1 (no credential literals) |
| AC-CLM-012 | PASS | settings valid+`permissions` present; zero SYNTAX lines; `targethooks=0` |
| AC-CLM-013 | PASS | `PASS` (`neon,playwright` keys, zero credential literals) |

**13/13 AC machine gates PASS.**

**GWT scenarios**: S1 (missing-binary advisory) — executed manually with stripped PATH; correctly emitted advisories for the two genuinely-missing servers (css/html) on this dev machine, non-blocking, exit 0. S2 — this is the GWT form of AC-CLM-013, PASS. S3 (all-present silence) — verified by construction: `command -v` skip-continue logic confirmed no advisory for any of the 11 languages whose binaries ARE present on this dev machine. S4 (zero MCP selection) — the generation template's `with_entries(select(...))` jq pattern naturally produces `{"mcpServers": {}}` for an empty selection array (not executed as a separate AC, but the template mechanism trivially supports it — documented here per Definition of Done item 2).

**Open risks (plan.md, 8 items) — run-phase resolution status**:
1. HTML/CSS split — **RESOLVED**: split into `html`+`css` (13 keys total), M1 verified.
2. C# server choice — **RESOLVED**: `csharp-ls` chosen (MIT, actively maintained) over OmniSharp.
3. Kotlin server maintenance — **RESOLVED**: official JetBrains `Kotlin/kotlin-lsp` supersedes the stale community fork.
4. jdtls launch complexity — **RESOLVED**: fits the flat schema via `args: ["-data", ...]`; JAVA_HOME relies on shell inheritance (documented in the install guide), no wrapper script needed.
5. PHP intelephense licensing — **RESOLVED**: `phpactor` (MIT, free) chosen.
6. Advisory noise (no cool-down) — **STILL OPEN**, carried to sync report as a known limitation; no suppression mechanism implemented this SPEC (out of scope per acceptance.md; a future SPEC may add a cool-down).
7. Catalog path contract fragility (no schema-version handshake) — **PARTIALLY MITIGATED**: both `dev-mcp-catalog.json` and `mcp-gen-template.json` carry a `$schema_version: "1.0.0"` field; a full handshake protocol with the sibling SPEC's consumer is still open, carried to sync report.
8. Loader schema unknowns — **RESOLVED**: M1 confirmed the schema supports `env`/`initializationOptions`/etc. via the official plugin-docs reference.

## §E.3 Run-phase Audit-Ready Signal

```yaml
run_status: complete
run_complete_at: 2026-07-11
ac_pass_count: 13
ac_fail_count: 0
preserve_list_post_run_count: 5   # existing .lsp.json entries + 5 gate scripts/dispatch.sh, all byte-verified unchanged
new_warnings_or_lints_introduced: 0
total_run_phase_files: 8   # .lsp.json, lsp-install-guide.md, lsp-binary-advisory.sh, hooks.json, dev-mcp-catalog.json, mcp-gen-template.json, settings.project.json, quality-gate-hook.sh (+ README.md docs delta, progress.md/spec.md evidence — not counted as plugin deliverables)
m1_to_mN_commit_strategy: per-milestone commits (M2 71a17fa, M3 67d7958, M4 9d8abba, M5 2567130, M6 pending) pushed together at run-phase close
cross_platform_build:
  applicable: false   # no compiled binary in this SPEC's scope (JSON/shell/markdown only)
```

Write-scope verification (`git status --porcelain`, run from repo root): only `plugins/moai/**` files are tracked-modified by this SPEC; `.moai/specs/SPEC-MOC-CODER-LSP-MCP-001/**` is gitignored repo-wide (`**/.moai/` pattern) and therefore never appears in `git status` — SPEC evidence lives disk-only per this project's established convention, consistent with prior SPECs in this repo.

## §E.4 Sync-phase Audit-Ready Signal

```yaml
sync_complete_at: 2026-07-11
sync_commit_sha: 5b8a214
sync_status: complete
sync_route: Route A Hybrid Trunk (Tier M, single sync commit direct to main, no PR)
scope_summary: >
  Standard sync scope per user approval. Single sync commit (CHANGELOG.md only
  tracked — .moai/specs/** is repo-wide gitignored, all 4 SPEC artifacts edited
  disk-only). Frontmatter in-progress → completed on spec.md + plan.md +
  acceptance.md (updated: 2026-07-11 on all). CHANGELOG [Unreleased] entry
  inserted as the newest entry directly under the [Unreleased] header.
b12_self_test_a: "pre-emission grep -c 'SPEC-MOC-CODER-LSP-MCP-001' CHANGELOG.md == 0 (verified before drafting); post-edit count == 1 (single header line)"
b12_self_test_b: "AC count 13 in CHANGELOG matches acceptance.md SSOT (grep -cE '^\\| AC-CLM-[0-9]+ \\|' == 13)"
b12_self_test_c: "all claimed file paths verified via ls before commit: .lsp.json, references/{lsp-install-guide.md,dev-mcp-catalog.json,mcp-gen-template.json}, hooks/gates/lsp-binary-advisory.sh, hooks/hooks.json, templates/claude/settings.project.json, templates/claude/hooks/quality-gate-hook.sh, README.md"
changelog_entry_position: "newest-first — inserted directly under '## [Unreleased]', above SPEC-MOC-PLUGIN-MOAI-V2-001"
frontmatter_status_transitions:
  spec_md: "in-progress → completed (merged 3-phase close on sync commit)"
  plan_md: "draft → completed"
  acceptance_md: "draft → completed"
  progress_md: "§E.4 populated post-push (gitignored, no second commit needed)"
canary_compliance_check:
  applicable: false   # this SPEC defines no forward-looking policy that its own sync tests
residuals_carried:
  - "Open risk #6 — advisory hook fires every SessionStart with no cool-down/suppression; follow-up SPEC candidate"
  - "Open risk #7 — partially mitigated: $schema_version 1.0.0 on catalog + gen-template, but no full schema handshake protocol with the sibling consumer SPEC (SPEC-MOC-PM-ADVISORS-001)"
  - "marketplace.json moai entry version delta 1.0.0 → 1.1.0 handed to SPEC-MOC-PM-ADVISORS-001 M5 (not touched by this SPEC or this sync)"
  - "M6 run commit 4c43718 missing 🗿 MoAI trailer (cosmetic, history immutable)"
run_commit_range: 71a17fa (M2) → 67d7958 (M3) → 9d8abba (M4) → 2567130 (M5) → 4c43718 (M6)
worktree_note: sync executed in the main checkout (/Users/goos/MoAI/claude.mo.ai.kr), NOT an isolated agent worktree — no copy-back step required
```
