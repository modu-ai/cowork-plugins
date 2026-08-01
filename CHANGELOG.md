# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed — SPEC-MOC-PM-ADVISORS-001

moai-pm plugin redesign — the single `project` skill is replaced by **two dedicated advisor skills**: `goose` (Desktop super-advisor, `/goose --project` — every Claude Cowork task except development) and `moai` (dev-project init advisor, `/moai --project` — moai-adk v3.0 philosophy: SPEC plan/run/sync, TRUST 5, DDD/TDD). Four tracked drift lines in the legacy skill are closed in-flight during migration rather than copied forward.

**BREAKING** — the `/project` invocation surface is retired. Entry is now `/goose --project` (Desktop) or `/moai --project` (development); `moai-pm` bumps MAJOR (`0.4.0` → `1.0.0`) accordingly. `/moai --project` (flag, moai-pm) and `/moai project` (space-subcommand, coder plugin) are distinct entry points — neither shadows the other.

**Core deliverables**:
- **M2** — `plugins/moai-pm/skills/goose/` (13 files: `SKILL.md` with the 6 canonical H2 anchors in order — Socratic Interview → Plugin Inventory Scan → Custom Agent & Skill-Chain Design → Generation Targets → Recursive Self-Improvement → Desktop Parity Constraints — plus 11 `references/*.md` and `references/templates/CLAUDE.md.tmpl` preserving all 8 `## N. … (HARD)` blocks). Generates `CLAUDE.md` (≤200 lines) + `.claude/agents/` + `.moai/` scaffold; custom agents are synthesized from interview context, never copied from prebuilt plugin agents (AC-PMA-001/004/004b/005/005b/006/014/019)
- **M3** — `plugins/moai-pm/skills/moai/` (8 files: `SKILL.md` with 5 canonical H2 anchors + 7 `references/*.md`). Carries the `## LSP Presence Check` and `## MCP Survey` sections consuming the sibling SPEC-MOC-CODER-LSP-MCP-001 catalog, explicit-namespace routing (`moai-pm:moai` vs `moai:moai`), and a degraded guidance-only fallback (`references/mcp-fallback-summary.md`) when the coder plugin is absent (AC-PMA-007/018/020/021/022)
- **M4** — legacy `plugins/moai-pm/skills/project/` removed in full (15 tracked files); repo-wide sweep of all 4 tracked drift patterns across `plugins/moai-pm/` → 0 matches (AC-PMA-002/003/013)
- **M5** — `plugins/moai-pm/README.md` full rewrite as a 2-skill entry (18-plugin roster table with per-employee entry-skill column, command-surface disambiguation callout); marketplace + plugin.json version lockstep (AC-PMA-008/009)

**Drift closed during migration** (fixed in-flight, not copied-then-patched): (1) `4-plugin` / `27-plugin` hardcoded counts replaced by citations of `.claude-plugin/marketplace.json` as the roster authority; (2) the heavy Self-Refine evolution model (`evolution-protocol.md`, `metrics.csv`, forced scoring) dropped in favour of the single simplified self-improvement model; (3) custom-agent generation restored as a first-class Phase 7 in the goose setup canon (was API-key-only); (4) `story-*` / `book-*` skill-prefix ownership corrected to `moai-story` (AC-PMA-015/016).

**Verification**: 21/21 machine-gate AC PASS + 3/3 structural-review AC cited + 4/4 Given-When-Then scenarios PASS (24 AC total per `acceptance.md`; evidence in SPEC `progress.md` §E.2/§E.3, disk-only per repo `.moai/` gitignore convention). Run-phase commits: `f98b010` (M1+M2) → `a02314a` (M3) → `8f3b13a` (M4) → `0539fd6` (M5).

**Key files**:
- `plugins/moai-pm/skills/goose/` (new — 13 files, Desktop super-advisor)
- `plugins/moai-pm/skills/moai/` (new — 8 files, dev-init advisor)
- `plugins/moai-pm/skills/project/` (removed — 15 files)
- `plugins/moai-pm/README.md` (2-skill rewrite)
- `.claude-plugin/marketplace.json` (`moai-pm` `0.4.0` → `1.0.0` MAJOR; `moai` `1.0.0` → `1.1.0` MINOR — the sibling SPEC-MOC-CODER-LSP-MCP-001 handed delta, single-owner here)
- `plugins/moai-pm/.claude-plugin/plugin.json` (`1.0.0`) + `plugins/moai/.claude-plugin/plugin.json` (`1.1.0` — version field only, D1 lockstep exception)

**Residual**: (1) `moai/references/mcp-fallback-summary.md` is a static snapshot of the sibling's MCP catalog with **no automated sync mechanism** — flagged in-file as a driftable copy (open risk #1, still open); (2) `/moai` short-form dispatch ambiguity is mitigated by explicit-namespace documentation but remains **platform-defined** and outside this SPEC's control (open risk #3, still open); (3) shared-reference duplication across the two skills (`router.md`, `init-protocol.md`, `execution-protocol.md`, `claudemd-generator.md`) is realized as designed — per-skill adapted copies requiring manual sync on future changes (open risk #4, accepted); (4) runtime E2E of both skills not executed (static verification only); (5) `www/**` guide updates (REQ-D-003) handed to a follow-up — 8 target paths recorded in `progress.md` §E.4; (6) stray untracked runtime-artifact directories under the deleted `skills/project/` require a direct `rm -rf` on the main checkout (never git-tracked, outside commit scope).

### Added — SPEC-MOC-CODER-LSP-MCP-001

moai coder plugin expansion — `.lsp.json` grows from 5 to 13 language-server entries (12-language coverage; HTML/CSS split into separate servers), non-blocking LSP install guidance (install guide + SessionStart advisory hook), a verified declarative dev-service MCP catalog with a deterministic `.mcp.json` generation template, and survey-parameterized meta-harness templates (project settings allowlist + toolchain-auto-detecting quality-gate hook) targeting the user's project.

**Core deliverables**:
- **M2** — `plugins/moai/.lsp.json` 5→13 entries: java/jdtls, cpp/clangd, csharp/csharp-ls, php/phpactor, kotlin/kotlin-lsp (official JetBrains), ruby/ruby-lsp, html + css split via vscode-langservers-extracted; existing 5 entries (go/python/rust/swift/typescript) preserved byte-identical, all entries on the flat command/args/extensionToLanguage/restartOnCrash/maxRestarts schema (AC-CLM-001~004)
- **M3** — `plugins/moai/references/lsp-install-guide.md` (13 H3 sections, macOS-first brew + cross-platform apt/npm/pip/gem/dotnet) + `plugins/moai/hooks/gates/lsp-binary-advisory.sh` (SessionStart advisory — warns when a declared language matches project files but its binary is missing from PATH; always exits 0, never emits `decision`/`block` JSON) registered additively in `hooks.json`; existing 5 gate scripts + `dispatch.sh` byte-unchanged (AC-CLM-005~007)
- **M4** — `plugins/moai/references/dev-mcp-catalog.json` (6 declarative entries: playwright, supabase with dev/test-only production warning, vercel, neon, railway, claude-in-chrome as guidance-only; `$schema_version: "1.0.0"`; extensible as data-only change) + `plugins/moai/references/mcp-gen-template.json` (exact per-server `.mcp.json` fragments, zero credential literals — `${VAR}` placeholders only) (AC-CLM-008~011, AC-CLM-013)
- **M5** — meta-harness templates: `plugins/moai/templates/claude/settings.project.json` baseline permissions allowlist + `plugins/moai/templates/claude/hooks/quality-gate-hook.sh` (toolchain auto-detect go/node/python/rust, graceful degradation, always exit 0); targets the USER project exclusively, zero references into the plugin's own `hooks/` (AC-CLM-012)
- **M6** — `plugins/moai/README.md` code-intelligence section rewrite (5-server → 13-server/12-language table with per-language install one-liners) + dev-service MCP catalog cross-reference section

**Verification**: 13/13 AC PASS (evidence in SPEC progress.md §E.2, disk-only per repo `.moai/` gitignore convention). Run-phase commits: `71a17fa` (M2) → `67d7958` (M3) → `9d8abba` (M4) → `2567130` (M5) → `4c43718` (M6).

**Key files**:
- `plugins/moai/.lsp.json` (5→13 language-server entries)
- `plugins/moai/references/{lsp-install-guide.md, dev-mcp-catalog.json, mcp-gen-template.json}` (new)
- `plugins/moai/hooks/gates/lsp-binary-advisory.sh` (new) + `plugins/moai/hooks/hooks.json` (additive registration)
- `plugins/moai/templates/claude/settings.project.json` + `plugins/moai/templates/claude/hooks/quality-gate-hook.sh` (new meta-harness templates)
- `plugins/moai/README.md` (code-intelligence + MCP catalog sections)

**Residual**: (1) advisory hook fires every SessionStart with no cool-down/suppression — open risk #6, follow-up SPEC candidate; (2) `$schema_version` field added to catalog + template but no full schema handshake protocol with the sibling consumer SPEC — open risk #7 partially mitigated; (3) marketplace `moai` entry version delta 1.0.0→1.1.0 handed to SPEC-MOC-PM-ADVISORS-001 M5 (marketplace.json untouched by this SPEC); (4) M6 commit `4c43718` missing `🗿 MoAI` trailer (cosmetic).

### Added — SPEC-MOC-PLUGIN-MOAI-V2-001

moai plugin v2 — rename (`moai-coder` → `moai`, clean-slate version `1.0.0` per user decision DP-1), two-layer restructure (`rules/` → `templates/claude/`), single-dispatcher hook consolidation, and deterministic scaffolding via `/moai:project`. Establishes the Web-tier activation contract (marketplace + output-style selector + enabled-plugin) and completes the v2 redesign P2 phase for this repository's owned portion.

**Core deliverables**:
- **M1** — `git mv plugins/moai-coder → plugins/moai` + `plugin.json` (`name: moai`, `displayName: 코더`, `version: "1.0.0"`) + marketplace.json 4-plugin entry (moai-coder tombstone removed) (AC-MV2-001a/b/c/d)
- **M2** — two-layer restructure: `rules/moai/` → `templates/claude/rules/moai/` (61 files, 100% git rename R100, 0 content change) + ADK-upstream `templates/CLAUDE.md` (parity-source marker) + `templates/claude/settings.project.json` (Web-activation 3 keys: `outputStyle: moai:MoAI`, marketplace `moai-claude`, enabled `moai@moai-claude`) + `templates/moai/config/sections/*.yaml` (27 token-holders) (AC-MV2-002a~f)
- **M3** — hook consolidation: single `hooks/dispatch.sh` (fan-in for all 20 events, `$CLAUDE_CODE_REMOTE` branch + `command -v moai` T3 auto-activation + fail-open `exit 0`) + `hooks/gates/` 5 scripts (4 migrated + gateguard-fact-force vendor per DP-2); 20 `handle-*.sh` scripts removed (AC-MV2-003a~e)
- **M4** — `scripts/scaffold.sh` (deterministic cp+sed scaffolder, `--dry-run`, backup, user-owned preservation, settings.json merge preservation) wired into `/moai:project` skill; Layer-2 template payload deployable to arbitrary target projects (AC-MV2-004a~g)
- **M5** — reference sweep: `moai-coder` references in `plugins/` → 0 (was 35/12 files), `www/content/plugins/**` old-name (`moai-code`/`moai-coder`) → 0 (was 17/5 files) + `moai@moai-claude` added, root `README.md` 4-plugin topology, `plugins/moai/README.md` reinstall notice (AC-MV2-005a~f)
- **M6** — verification + P0-8 typed-name measurement: `claude plugin validate` ×2 PASS, `bash -n` 7 scripts PASS, Hugo build 228p PASS; P0-8 verdict recorded (probe-layer indeterminate — 13 project/plugin command names genuinely collide; deactivation-guidance UI is P3 out-of-scope) (AC-MV2-006a~d)

**Verification**: 32/32 AC PASS (AC-MV2-006d link-check PASS-WITH-DEBT — 10 pre-existing broken links in cookbook/cowork/tags, NOT a regression; `--strict` validate exit 1 is SHOULD debt EC-5). Run-phase commits: `56f9e09` (M1) → `ad86a50` (M2) → `7ff8c5f` (M3) → `21fb72c` (M4) → `5037668` (M5) → `6e0ccdc` (M6).

**Key files**:
- `plugins/moai/` (renamed from `plugins/moai-coder/`; manifest, templates/, hooks/, scripts/scaffold.sh)
- `plugins/moai/hooks/dispatch.sh` (new — single event dispatcher, `@MX:ANCHOR`)
- `plugins/moai/scripts/scaffold.sh` (new — deterministic Layer-2 scaffolder, `@MX:ANCHOR`)
- `plugins/moai/templates/{CLAUDE.md, claude/rules/moai/, claude/settings.project.json, moai/config/sections/}` (new two-layer payload)
- `.claude-plugin/marketplace.json` (moai entry replaces moai-coder tombstone)
- `www/content/plugins/{_index,code/_index,chat/_index,cowork/_index,design/_index}.md` (catalog rename)
- Root `README.md` (4-plugin topology)

**Residual debt**: (1) `--strict` plugin validate exit 1 — 12 command frontmatter gaps (EC-5, follow-up frontmatter SPEC); (2) www link-check 10 pre-existing broken links (cookbook/cowork/tags — separate SPEC); (3) P0-8 typed-name deactivation-guidance UI not implemented (P3 out-of-scope).

### Added — SPEC-MOC-BOOTSTRAP-DESKTOP-001

Bootstrap architecture + moai-code Desktop Edition capability elevation — defining two-entrypoint parity (`/project init` for non-developers, `/moai:project` for no-install developers) with single canonical source (`internal/template/templates/`). Version stamp SSOT established (4-location release checklist) and version bound from 0.1.0 → 3.0.0 per user decision D1.

**Core deliverables**:
- **M1** — `/project init` folder-convention scaffold + `.moai/skill-profile.yaml` persisted artifact (AC-BD-001a/b/c NET-NEW gates; skill-profile.yaml directive + Phase 6.5/6.6 workflow)
- **M2** — Parity contract documentation + `plugin-deployed vX.Y.Z` stamping directive (AC-BD-003 NET-NEW; parity between `/moai:project` and `moai init` documented)
- **M3** — Desktop Edition Tier 1-3 capability table + session-start binary detection branch + fail-open preservation (AC-BD-004/005a/b; Tier 1/2/3 structure + hook split)
- **M4** — VERSION-SSOT release checklist sentinel + D1 version bind 0.1.0 → 3.0.0 (AC-BD-006c NET-NEW, AC-BD-006d D1-GATED; 3-location normalized literal match)
- **M5** — SKIPPED per user decision D2=KEEP (displayName unchanged; AC-BD-007 OPTION not activated)

**Verification**:
- 11/12 static AC PASS (M1-M4 comprehensive; V12 RUNTIME AC-002/003-runtime documented as residual risk — require `/moai:project` plugin-command execution for full runtime verification, out of sync-phase scope)
- Preserved 4 invariants (legacy alias 14, CLAUDE.md heading 1, exit 0=1, {{.Version}}=2, parity-source markers=12)
- Version bind applied: moai-cowork/moai-code plugin.json both `3.0.0` (binds to binary v3.0.x line per REQ-BD-012)
- Run-phase commits: `e0b7b37` (M1) → `e43674e` (M2) → `22e09d4` (M3) → `570ed6b` (M4)

**Files modified**:
- `plugins/moai-cowork/skills/project/SKILL.md` (Phase 6.5/6.6 workflow, folder scaffold, skill-profile directive, EC6 distinction)
- `plugins/moai-code/README.md` (Desktop Edition Tier table, parity contract, VERSION-SSOT section)
- `plugins/moai-code/hooks/moai/handle-session-start.sh` (binary detection branch, Tier 3 promotion notice)
- `plugins/moai-cowork/.claude-plugin/plugin.json` (version `3.0.0`)
- `plugins/moai-code/.claude-plugin/plugin.json` (version `3.0.0`)

**Residual**: V12 RUNTIME AC (AC-BD-002, AC-BD-003-runtime) documented as residual risk — require `/moai:project` plugin-command execution in environment with `moai` binary available for full runtime verification.

### Added — SPEC-MOC-PLUGIN-REMEDIATION-001

Korean-slop remediation across 177 cowork + 11 design skills (gate structure, decontamination, namespace normalization, boundary dedup, lint CI), plus Phase A category-prefix rename of 150 skills (148 prefix-add + 2 body-rename, 26 no-op) per approved §D.9 mapping.

**Core deliverables**:
- P0 gate structure + P2 immediate-failure path repair (AC-001..007)
- P1 decontamination of 50 copy sources (slide/deck samples, commerce/newsletter boilerplate, dash-contrast headlines)
- P3 gate wiring (8 priority skills + project router)
- P2 bulk repair: 9 deprecated namespaces normalized across 70 files, project router rewritten for single-plugin architecture, stale refs repaired, ghost dir removed (AC-015..017)
- Phase A rename: 150 skills renamed with category prefixes (commerce-/content-/marketing-/media-/finance-/book-/legal-/education-/business-/office-/general-) — 0 dangling old-name references verified (AC-018)
- Phase B dedup: design-system-library cowork copy → pointer, brand-identity scope narrowed (AC-019..020)
- P4 re-occurrence prevention: skill-builder Korean authoring rules, lint CI script (korean-slop-lint.sh) with 4-class self-test, scope discipline (AC-021..024)

**Verification**:
- 24/24 AC PASS (all MUST-PASS + SHOULD-PASS criteria satisfied)
- AC-018 resolved via standalone-reference interpretation (§D.9.5): residual word-boundary matches are legitimate new-name substrings, URLs, genre enums, cross-plugin pointers — 0 actual dangling references
- Run-phase commits: `b7ca913` (M1) → `665bbb3` (M2-M5-Phase-B) → `f44bb47` (M5-Phase-A AC-018 rename)
- www/plugins/ re-sync required (owned by SPEC-MOC-SITE-IA-001 — REQ-REM-024)

**Files modified**: ~25-40 source files across plugins/moai-cowork/skills/, plugins/moai-design/skills/, scripts/, skill-builder/, marketplace.json, llms.txt (M1-M6 cumulative)

**Residual**: moai-core namespace flagged by AC-015 grep but exempt per plan.md §A.5 (separate SPEC ownership)

### Added — SPEC-MOC-SITE-IA-001

사이트 정보 구조(IA) 2축 재편 (데스크탱/CLI) + DESIGN 병합 완료 + 플러그인 문서 4 카테고리 현행화 + CLI 축 신규 콘텐츠 22페이지 + 내부링크 체커 도구 신규.

**Core deliverables**:
- **D₁ (M1+M2+M3)** — 메뉴 SSOT 2축 재편: 데스크탑 축(🖥️) / CLI 축(⌨️) / 공통 하단(도움말·쿡북·실전 트랙·릴리스). DESIGN 병합 완료(`claude-design/` 디렉토리 삭제 + alias 10건 보존). help/office 통합(office→도움말 2p 이동 + alias). cookbook/tracks 메뉴 중복 제거.
- **D₂ (M4)** — CLI 축 신규 콘텐츠 22페이지: 시작하기(3p) + 핵심 개념(5p) + 일상 사용(5p) + MoAI-ADK(4p) + 레퍼런스(4p) + `_index.md`(5p). moai-adk-go 원문을 입문자 친화적 한국어 prose-first로 재저작. PLAN→RUN→SYNC stateDiagram 포함.
- **D₃ (M5)** — 플러그인 문서 4 카테고리 재편: chat(문서 허브) / cowork(177스킬) / design(11스킬) / code(13명령+7에이전트+28스킬). marketplace.json 3 플러그인 현실 반영. 구 33 obsolete page → alias 리다이렉트(38건).
- **D₄ (M6)** — source-index CLI 축 확장("다루지 않" 제한 문구 제거 4→0건, `/cli/` 경로 참조 0→28건) + 전용 내부링크 체커(`www/scripts/check-links.mjs`) 신규.

**Verification**:
- 23/24 AC PASS (AC-IA-001..022, 024 — structural delta + per-page alias + Hugo build exit 0)
- AC-IA-023 PASS-WITH-DEBT — 전용 링크체커가 pre-existing broken internal links 10건 발견(cookbook 본문 상대경로 오타 5건 + Hugo taxonomy 렌더링 한계 5건, commit 6d78fbf부터 기원). **SPEC 산출 콘텐츠(cli/**, plugins/{chat,cowork,design,code}/**, help/source-index.md)에서 broken 0건** — 전부 out-of-scope PRESERVE 대상. 별도 후속 SPEC에서 정비.
- Hugo build: exit 0, 228 pages, 65 aliases, 392 ms (M6 finalization rebuild)
- 전용 링크체커: `node www/scripts/check-links.mjs www/public` → exit 1, `broken internal links: 10` (전부 pre-existing; SPEC-produced content 0건)

**Files modified**:
- `www/data/menu/main.yaml` (2축 재편 + axis 마커)
- `www/content/cli/**` (22 신규 페이지 — 5 섹션)
- `www/content/plugins/{_index,chat,cowork,design,code}/_index.md` (4 카테고리 재편 + 5 공통 스켈레톤)
- `www/content/help/source-index.md` (CLI 축 확장)
- `www/scripts/check-links.mjs` (신규 204행 Node script — AC-IA-023 권威 체커)
- `content/claude-design/` 디렉토리 삭제 (DESIGN 병합 완료)
- 구 33 plugin 페이지 → alias 리다이렉트 처리

**Run-phase commits**:
- D₁: `a803537`, `e50dc6e`, `d3d139e`
- D₂: `21e44dc`, `109dba7`, `4645bb2`, `4834643`, `f6c6750`, `12eaa8e`
- D₃: `637e1cd`, `aa35d8c`, `93c4871`, `4a56289`, `52d9072`, `5a37229`
- D₄: `7771497`, `2e7353c`, `c6c7aed` (이 커밋)

**Residual**: AC-IA-023 pre-existing broken internal links 10건 (cookbook 본문 5건 + Hugo taxonomy 5건) — 별도 후속 SPEC에서 정비. SPEC 산출 콘텐츠는 모든 내부링크 정상(0 broken).

### Added — SPEC-MOC-PLUGIN-STORY-001

moai-story 플러그인 신설 + 패밀리 v4 재배치 — 작가 도메인 전용 플러그인(21스킬: 이관 8 + 신규 13) + Higgsfield MCP 연동 + cowork v4.0.0 마이그레이션.

**Core deliverables**:
- **M1** — moai-story 스캐폴딩 (plugin.json v0.1.0, .mcp.json higgsfield canonical, skills/)
- **M2** — 이관 스킬 8종 복사 (cowork → story) + book-revision-coach fallback note
- **M3** — 신규 스킬 13종 작성 (story-*) + 위생 스윕프 (3rd-person/무엇을-언제/AI-tell across all 21)
- **M4** — cowork v4.0.0 마이그레이션 (book-* 8스킬 제거, higgsfield MCP 제거, 171 SKILL.md 4.0.0, CHANGELOG v4.0.0)
- **M5** — marketplace.json 4플러그인 엔트리 (moai-story 추가, metadata.version 4.0.0, per-entry version 미기재)
- **M5-fix** — moai-story author string→object 정정 (Claude Code plugin schema)
- **M6** — www 문서 갱신 (index/migration/higgsfield-setup/CHANGELOG + content/_index.md live-site update)

**Verification**:
- 10/12 AC PASS (AC-001~010 full/intent PASS; AC-011 PASS-WITH-DEBT --strict structural; AC-012 PASS-WITH-DEBT count drift ND5)
- ND debt: ND3/4/5/6/7/8 resolved (pre-fixed + sync-phase acceptance.md cleanup); ND1/2 resolved (plan-phase); ND9 residual (non-blocking, pre-existing warnings + SPEC-required category)
- DRIFT-001 depends_on noted: DRIFT-001 not yet created, but run-phase accepted `status: in-progress` per M0 gate policy; sync non-blocking
- Hugo build: exit 0, dead-link check 0
- Run-phase commits: `76741dc` (M1) → `105175e` (M2) → `cabbdb1` (M3) → `d1d5887` (M4) → `8629c5d` (M5) → `5dfe2d4` (M5-fix) → `11f7379` (M6)

**Files modified**:
- `plugins/moai-story/` (NEW PLUGIN — plugin.json, .mcp.json, skills/ 21개)
- `plugins/moai-cowork/` (v4.0.0 — 8 book-* 스킬 제거, higgsfield MCP 제거, 171 SKILL.md 4.0.0, CHANGELOG)
- `.claude-plugin/marketplace.json` (4플러그인 엔트리, metadata.version 4.0.0)
- `www/plugins/{index,migration,higgsfield-setup}.md` + `www/CHANGELOG.md` (문서 갱신)

**Residual**: ND9 — AC-STORY-011 `claude plugin validate . --strict` fails on pre-existing warnings (metadata.language, metadata.license) + SPEC-required category field (structural conflict); non-strict validate exits 0.

