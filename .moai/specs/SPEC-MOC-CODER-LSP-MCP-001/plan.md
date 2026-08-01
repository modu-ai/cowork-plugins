---
id: SPEC-MOC-CODER-LSP-MCP-001
document: plan
version: "0.2.0"
status: completed
created: 2026-07-10
updated: 2026-07-11
---

# Plan — SPEC-MOC-CODER-LSP-MCP-001

## §A Context

Tier M expansion of `plugins/moai`: `.lsp.json` 5→12 language coverage with a mandated binary-verification step, non-blocking install guidance (init-time + SessionStart advisory), a verified extensible dev-MCP catalog with survey-driven project `.mcp.json` generation, and survey-parameterized meta-harness templates (settings.json + hooks) targeting the user's project. All design decisions FINAL per 2-round Socratic interview.

Run-phase implementation agents: **model=sonnet, effort=xhigh** — milestones are independent and file-ownership-separated.

## §B Known Issues

- No install-missing guidance exists today; missing LSP binaries degrade silently.
- `.lsp.json` loader capability envelope is unverified: whether the plugin LSP loader supports per-language `initializationOptions` (needed by some candidate servers, e.g. jdtls) is unknown — M1 verifies before entry authoring.
- Several candidate servers have contested maintenance/licensing states (C#, Kotlin) — verification is a REQUIREMENT (REQ-L-003), not a nicety.

## §C Pre-flight (M1 detail — verification-first)

For EACH of the 7 new language entries + 5 catalog server entries, verify against official documentation (Context7 first, WebFetch fallback) and record to `progress.md §E.2`:

1. Exact binary name + launch args (stdio mode flags, e.g. `--stdio`).
2. Install command per platform (brew/npm/pip/gem; macOS-first + cross-platform notes).
3. Maintenance state (esp. C# server choice; kotlin-language-server status).
4. For MCP entries: transport (remote URL vs local stdio), auth model (OAuth vs key), the supabase dev/test-only warning wording, railway npm-shim status.
5. `.lsp.json` loader capabilities: schema fields the coder plugin loader actually honors (read the loader source / template SSOT) — determines whether complex servers (jdtls) fit the flat command/args schema or need a wrapper script.
6. Baseline snapshots: `sha256sum` of the 5 existing gate scripts (REQ-L-008 byte-unchanged gate), current marketplace `moai` version.

## §D Constraints

- Write scope: `plugins/moai/**`, `.moai/specs/SPEC-MOC-CODER-LSP-MCP-001/**`. **NO direct `.claude-plugin/marketplace.json` write** — the `moai` plugin-entry version bump is handed to SPEC-MOC-PM-ADVISORS-001 M5 (the single cross-SPEC owner of the shared `marketplace.json` edit; see §H). No `www/**`, no `plugins/moai-pm/**` (sibling SPEC ownership).
- Existing 5 gate scripts byte-unchanged; existing 5 `.lsp.json` entries preserved unless M1 verification finds a defect (then: blocker report, not silent edit).
- Credentials: no real values anywhere; placeholder + `.env` guidance pattern only.
- Pathspec-scoped commits (parallel-session working tree, 29 uncommitted files).
- No time estimates; priority labels only.

## §E Self-Verification

Run-phase completion requires executing every command in `acceptance.md §D` with verbatim evidence in `progress.md §E.2`/`§E.3`. Key gates: `.lsp.json` jq schema pass over required key set, `.mcp.json` still context7-only, catalog jq validation + supabase warning grep, advisory hook `bash -n` + forced-missing-PATH exit-0 test, gate-script sha256 equality vs M1 baseline.

## §F Milestones

| M | Priority | Scope | File ownership (write) | Depends on |
|---|----------|-------|------------------------|------------|
| M1 | High | Verification pass (§C): per-server binary/args/install/maintenance verification; loader capability check; baselines (gate sha256, marketplace version) | `.moai/specs/SPEC-MOC-CODER-LSP-MCP-001/progress.md` only | — |
| M2 | High | `.lsp.json` expansion 5→12 using ONLY M1-verified invocations; existing 5 entries preserved | `plugins/moai/.lsp.json` | M1 |
| M3 | High | Install guidance: per-language install-command reference (12 languages, macOS-first + cross-platform notes) + SessionStart advisory gate (new script, always exit 0) + `hooks.json` additive registration | `plugins/moai/references/lsp-install-guide.md` (or M1-confirmed references path), `plugins/moai/hooks/gates/<new-advisory>.sh`, `plugins/moai/hooks/hooks.json` | M1 |
| M4 | High | Dev-MCP catalog (declarative JSON, 6 entries per REQ-C-003, extensible schema) + project `.mcp.json` generation template + `.env` credentials guidance | `plugins/moai/references/dev-mcp-catalog.json` + `plugins/moai/references/mcp-gen-template.json` — BOTH pinned under `references/`, disjoint from M5's `templates/` (final catalog path recorded to progress.md; the `references/` home is the contract-default per sibling `design.md §H`) | M1 |
| M5 | Medium | Meta-harness templates: project `.claude/settings.json` template (permissions allowlist + hooks registration) + project hook templates parameterized by survey (toolchain quality gate) | `plugins/moai/templates/**` (M5's sole write subtree; disjoint from M4's `references/`) | M1 |
| M6 | Medium | Docs touch (README note for new coverage), HAND the `moai` marketplace entry-delta to SPEC-1 M5 (record the delta in progress.md — NO direct `marketplace.json` write), self-verification batch over all ACs | `plugins/moai/README.md`, progress.md | M2, M3, M4, M5 |

M2/M3/M4/M5 are mutually independent after M1 under the following **pinned, file-granular disjoint write ownership** (no two milestones write the same file):
- **M2** → `plugins/moai/.lsp.json`
- **M3** → `plugins/moai/references/lsp-install-guide.md`, `plugins/moai/hooks/gates/<advisory>.sh`, `plugins/moai/hooks/hooks.json`
- **M4** → `plugins/moai/references/dev-mcp-catalog.json`, `plugins/moai/references/mcp-gen-template.json`
- **M5** → `plugins/moai/templates/**`

M4's `.mcp.json` generation template is pinned to `references/mcp-gen-template.json` (NOT under `templates/`), so M4 and M5 never write the same subtree — the parallelizability claim holds. M3 and M4 both create files under `references/` but to distinct enumerated filenames (no shared file). No milestone touches `marketplace.json` (handed to SPEC-1 M5 per §D/§H).

## §G Anti-Patterns (run-phase)

- Writing an `.lsp.json` entry from memory/training data without the M1 verification record — violates REQ-L-003 and verification-claim integrity (§1.1 surface 3).
- Modifying any existing gate script "while in the area" — REQ-L-008 byte-unchanged.
- Emitting blocking JSON or non-zero exit from the advisory hook under ANY branch — REQ-L-007.
- Embedding a sample API key / token (even fake-looking) in catalog or templates — placeholders must be structurally non-secret (`${VAR}` / `<YOUR_KEY>` forms).
- Hardcoding catalog knowledge into generator logic (violates REQ-C-004 data-only extensibility).
- Editing `plugins/moai-pm/**` (sibling SPEC ownership).
- Directly writing `.claude-plugin/marketplace.json` (single owner is SPEC-1 M5 — F12; hand the `moai` entry-delta instead).
- Landing M4's `.mcp.json` generation template under `plugins/moai/templates/**` (collides with M5 write ownership — pin it to `plugins/moai/references/mcp-gen-template.json`).

## §H Cross-References

- SPEC-MOC-PM-ADVISORS-001 `design.md §H` — interface contract: catalog default path `plugins/moai/references/dev-mcp-catalog.json`; if M4 finalizes a different path, record it in progress.md §E.2 AND notify the sibling SPEC's run agent via the orchestrator.
- **Marketplace single-owner (F12):** `.claude-plugin/marketplace.json` is edited by SPEC-MOC-PM-ADVISORS-001 M5 ONLY (both the `moai-pm` and `moai` entries). This SPEC's M6 records the required `moai` entry-delta (target version) in progress.md §E.2 and hands it to the sibling via the orchestrator; this SPEC performs NO direct marketplace.json write. Baseline observed 2026-07-11: `.metadata.version` = `6.2.0`, `moai` entry = `1.0.0`. Ordering: SPEC-1 M5 must run AFTER this SPEC's M6 delta is recorded (or the orchestrator serializes the two final-docs milestones).
- `acceptance.md` — AC matrix (M6 input).
- Soft ordering: this SPEC's M4 (catalog) should land before the sibling SPEC's M3 finalizes its catalog reference; parallel execution acceptable with the contracted path.

## §I Candidate Server Table (input to REQ-L-004 — candidates, not final)

Run-phase M1 verifies exact binary + launch args against official docs (REQ-L-003) before writing each `.lsp.json` entry; the table below is advisory input, superseded by the M1 `verified:` record.

| Language | Candidate server binary | Notes / verification focus |
|----------|-------------------------|----------------------------|
| Java | `jdtls` | Launcher-script complexity; workspace dir + JAVA_HOME; flat-schema fit (open risk #4) |
| C/C++ | `clangd` | Stable; confirm `--stdio`-equivalent flags |
| C# | actively-maintained server (OmniSharp / `csharp-ls` / Roslyn-based) | Maintenance + redistribution/licensing state differ — verify current, possibly user decision (open risk #2) |
| PHP | `intelephense` or `phpactor` | intelephense free-tier vs paid; phpactor free alternative (open risk #5) |
| Kotlin | `kotlin-language-server` | Community maintenance uncertain; check JetBrains official LSP status (open risk #3) |
| Ruby | `ruby-lsp` or `solargraph` | Confirm current recommended server + stdio flags |
| HTML/CSS | `vscode-html-language-server` family | May ship separate html/css binaries → key count 12 or 13 (open risk #1) |

## Open design risks (identified at plan-phase; NOT resolved here)

1. **HTML/CSS entry split**: official marketplace treats HTML/CSS as one language slot, but the vscode server family ships separate html/css binaries — the `.lsp.json` key count may be 12 or 13. ACs check the required key SET, not an exact count; final split is a run-phase M1 decision.
2. **C# server choice**: OmniSharp vs `csharp-ls` vs the Roslyn-based language server — maintenance and redistribution/licensing states differ and change; requires fresh verification, possibly a user decision if all candidates carry caveats.
3. **Kotlin server maintenance**: community `kotlin-language-server` maintenance status is uncertain; JetBrains' official LSP story may have changed — verify at M1.
4. **jdtls launch complexity**: jdtls typically needs a launcher script, workspace dir, and JAVA_HOME; may not fit the flat `command`/`args` schema — may force a wrapper-script pattern the current loader may not support (M1 loader capability check gates this).
5. **PHP intelephense licensing**: free tier vs paid features; phpactor as free alternative — choice may need user input if functional deltas matter.
6. **Advisory noise**: the SessionStart advisory fires every session while a binary is missing; no suppression/cool-down mechanism is specified — potential UX irritation accepted for now, flagged for follow-up.
7. **Catalog path contract fragility**: the sibling SPEC embeds a fallback summary of this catalog; any post-landing catalog schema change breaks the fallback silently (no schema-version handshake specified).
8. **Loader schema unknowns**: whether the plugin LSP loader honors fields beyond the observed 5-entry schema (e.g., `initializationOptions`, env injection) is unverified — could constrain which servers are wireable at all.
