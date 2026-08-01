---
id: SPEC-MOC-CODER-LSP-MCP-001
document: acceptance
version: "0.2.1"
status: completed
created: 2026-07-10
updated: 2026-07-11
---

# Acceptance — SPEC-MOC-CODER-LSP-MCP-001

All commands run from repo root `/Users/goos/MoAI/claude.mo.ai.kr`. "expect: no matches" = grep exit 1. Evidence recorded verbatim in `progress.md §E.2`. Paths marked `<M1-confirmed>` use the final paths recorded by M1/M4 in progress.md §E.2 (defaults shown).

## §D AC Matrix

| AC | Requirement | Verification command | Pass condition |
|----|-------------|----------------------|----------------|
| AC-CLM-001 | REQ-L-001 (12-language coverage) | `jq -r 'keys[]' plugins/moai/.lsp.json \| sort` then `for k in go python rust swift typescript java php kotlin ruby; do jq -e --arg k "$k" 'has($k)' plugins/moai/.lsp.json >/dev/null \|\| echo "MISSING: $k"; done` plus presence check for C/C++ key (`cpp` or `c`), C# key (`csharp`), and HTML/CSS key(s) (`html` and/or `css`) per M1 split decision | no `MISSING`; all 12 coverage areas keyed; total keys 12 or 13 per M1 decision recorded in progress.md |
| AC-CLM-002 | REQ-L-002 (schema conformance) | `jq -e 'to_entries \| all(.value \| has("command") and has("args") and has("extensionToLanguage") and .restartOnCrash == true and .maxRestarts == 3)' plugins/moai/.lsp.json` | `true` |
| AC-CLM-003 | REQ-L-001 (existing 5 preserved) | `for k in go python rust swift typescript; do jq -r --arg k "$k" '.[$k].command' plugins/moai/.lsp.json; done` | `gopls`, `pyright-langserver`, `rust-analyzer`, `sourcekit-lsp`, `typescript-language-server` (unless M1 defect record justifies a change, cited in progress.md) |
| AC-CLM-004 | REQ-L-003 (verification evidence exists) | `grep -c "verified:" .moai/specs/SPEC-MOC-CODER-LSP-MCP-001/progress.md` | ≥ 7 (one `verified:` evidence line per new language entry, each citing the official source consulted) |
| AC-CLM-005 | REQ-L-005 (install guidance coverage) | `grep -c "^### " plugins/moai/references/lsp-install-guide.md` (`<M1-confirmed path>`) | ≥ 12 (one H3 per language) AND `grep -q "brew install" <same file>` |
| AC-CLM-006 | REQ-L-006/007 (advisory hook non-blocking, mechanized) | `H=plugins/moai/hooks/gates/<M1-confirmed advisory script>; bash -n "$H"; OUT=$(printf '{"hook_event_name":"SessionStart"}' \| PATH=/usr/bin:/bin bash "$H" 2>/dev/null); RC=$?; echo "exit=$RC db=$(printf '%s' "$OUT" \| grep -cE '"decision"\|"block"')"` | `bash -n` clean AND output is exactly `exit=0 db=0` — the hook exits 0 under stripped PATH (missing binaries simulated) AND emits **zero** occurrences of `"decision"` or `"block"` in stdout (fed a synthetic SessionStart stdin payload). Both conditions decided by the single printed line |
| AC-CLM-007 | REQ-L-008 (existing gates byte-unchanged) | `sha256sum plugins/moai/hooks/gates/*.sh plugins/moai/hooks/dispatch.sh` compared against M1 baseline in progress.md §E.2 (new advisory script excluded) | all 5 gate scripts + dispatch.sh hashes equal baseline |
| AC-CLM-008 | REQ-C-001 (plugin .mcp.json context7-only) | `jq -r '.mcpServers \| keys \| join(",")' plugins/moai/.mcp.json` | `context7` |
| AC-CLM-009 | REQ-C-003/004 (catalog content + declarative extensibility) | `C=plugins/moai/references/dev-mcp-catalog.json; jq -e '.' "$C" >/dev/null && test "$(jq -r '.servers[].name' "$C" \| sort \| paste -sd, -)" = "claude-in-chrome,neon,playwright,railway,supabase,vercel" && jq -e '.servers \| all(has("name") and (has("transport") or has("type")))' "$C"` | JSON valid AND name set == exactly the 6 (`claude-in-chrome,neon,playwright,railway,supabase,vercel`) AND every entry is declarative — has `name` + a `transport`/`type` field (data-only; no executable-code key). Final exit 0 / `true` decides PASS |
| AC-CLM-010 | REQ-C-003 (supabase warning + chrome guidance-only, mechanized) | `C=plugins/moai/references/dev-mcp-catalog.json; W=$(jq -r '.servers[] \| select(.name=="supabase") \| .warning' "$C"); printf '%s' "$W" \| grep -qiE 'dev\|test' && printf '%s' "$W" \| grep -qiE 'prod' && test "$(jq -r '.servers[] \| select(.name=="claude-in-chrome") \| .entry_type' "$C")" = "guidance-only" && echo PASS \|\| echo FAIL` | `PASS` — supabase `.warning` is non-empty AND names both `dev`/`test` AND `prod`(uction) (encoding "dev/test only, never production"); claude-in-chrome `.entry_type == "guidance-only"` (pinned schema field/value; generates NO server entry) |
| AC-CLM-011 | REQ-C-005 (no credentials anywhere) | `grep -rInE "(api[_-]?key\|token\|secret\|password)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}" plugins/moai/references/ plugins/moai/templates/ 2>/dev/null` | no matches (placeholders like `${NEON_API_KEY}` / `<YOUR_KEY>` are permitted; long literal values are not) |
| AC-CLM-012 | REQ-H-001/002 (meta-harness templates, mechanized) | `S=plugins/moai/templates/claude/settings.project.json; jq -e '.' "$S" >/dev/null && grep -q "permissions" "$S"; for t in $(find plugins/moai/templates -name '*hook*.sh' 2>/dev/null); do bash -n "$t" \|\| echo "SYNTAX:$t"; done; echo "targethooks=$(grep -rlE 'plugins/moai/hooks/' plugins/moai/templates/ 2>/dev/null \| wc -l \| tr -d ' ')"` | settings template (`templates/claude/settings.project.json`) valid JSON with a `permissions` allowlist; zero `SYNTAX:` lines (all hook templates pass `bash -n`); `targethooks=0` — no meta-harness template writes into `plugins/moai/hooks/` (M5 targets the USER project, never the plugin's own hooks) |
| AC-CLM-013 | REQ-C-002 (template instantiation deterministic) | `T=plugins/moai/references/mcp-gen-template.json; OUT=$(<instantiate T with fixed selection playwright+neon via the M4 dry-run harness — jq/sed, recorded in progress.md>); printf '%s' "$OUT" \| jq -e '.' >/dev/null && test "$(printf '%s' "$OUT" \| jq -r '.mcpServers \| keys \| join(",")')" = "neon,playwright" && test "$(printf '%s' "$OUT" \| grep -cInE '(api[_-]?key\|token\|secret)[\"'"'"']?\s*[:=]\s*[\"'"'"'][A-Za-z0-9_-]{16,}')" -eq 0 && echo PASS \|\| echo FAIL` | `PASS` — the instantiated `.mcp.json` parses as JSON; `.mcpServers \| keys` == exactly `neon,playwright` (claude-in-chrome guidance-only → excluded); zero credential literals (only `${VAR}` / `<YOUR_KEY>` placeholders permitted) |

> **AC-CLM-013 instantiation-harness note (reproducibility).** The "M4 dry-run harness" referenced in the AC-CLM-013 command is a jq/sed transform that (1) reads the delivered `plugins/moai/references/mcp-gen-template.json`, (2) keeps ONLY the fixed selection `playwright` + `neon` (`claude-in-chrome` excluded as guidance-only), and (3) emits a `.mcp.json` object whose `.mcpServers` keys are exactly `neon,playwright` carrying only `${VAR}` / `<YOUR_KEY>` placeholders (zero credential literals). The concrete command is schema-dependent — M4 finalizes the template schema, then MUST record the verbatim reproducible command (harness form + fixed input selection + expected output) in `progress.md §E.2` so AC-CLM-013 is re-runnable byte-for-byte at verification time. Illustrative form (final jq path keys depend on the M4 schema): `jq --argjson sel '["playwright","neon"]' '<select servers whose name ∈ $sel; emit {mcpServers: …}>' plugins/moai/references/mcp-gen-template.json`.

## Given-When-Then Scenarios

### S1 — Missing LSP binary at session start (simulated)

- **Given** a project containing `.go` files and a shell whose `PATH` excludes `gopls` (simulate: `PATH=/usr/bin:/bin`)
- **When** the SessionStart advisory gate runs
- **Then** it emits an advisory naming the language and binary with an install-guidance pointer, AND exits 0, AND emits no blocking JSON (AC-CLM-006 command is the executable form of this scenario).

### S2 — Survey-driven .mcp.json generation (structural template test)

- **Given** the generation template and a simulated survey selection of `playwright` + `neon`
- **When** the template is instantiated with that selection (run-phase provides the instantiation harness — jq/sed dry-run acceptable)
- **Then** the produced `.mcp.json` parses as valid JSON, contains exactly `playwright` and `neon` under `mcpServers`, contains NO entry for `claude-in-chrome` (guidance-only), and contains no credential literal — only `.env` placeholder references.

### S3 — Edge: all declared servers present

- **Given** a PATH containing every declared server binary
- **When** the SessionStart advisory gate runs
- **Then** it is silent (no advisory output) and exits 0.

### S4 — Edge: user selects zero MCP servers

- **Given** a survey selecting no servers
- **When** generation runs
- **Then** the generated `.mcp.json` is either omitted or contains an empty `mcpServers` object (documented choice in the template), and never emits catalog defaults uninvited.

## Quality Gate Criteria

- AC-CLM-001..013 executed with verbatim evidence in progress.md §E.2; every new `.lsp.json` entry backed by an M1 `verified:` line citing its official source (no unverified-invocation writes — verification-claim-integrity §1.1 surface 3).
- Existing gate scripts + dispatch.sh byte-identical to baseline (AC-CLM-007).
- Write set ⊆ plan.md §D scope (verify via `git status --porcelain`).
- No git push; pathspec-scoped commits.

## Definition of Done

1. 13/13 AC machine gates PASS with evidence.
2. All 4 GWT scenarios exercised (S1/S3 executable; S2/S4 template dry-run — S2 is the GWT form of AC-CLM-013) and recorded.
3. Final catalog path + schema field names + HTML/CSS split decision recorded in progress.md §E.2 (interface handoff to SPEC-MOC-PM-ADVISORS-001).
4. Open risks (plan.md) re-stated with run-phase status; still-open items carried to sync report.
