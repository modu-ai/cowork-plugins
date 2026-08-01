---
id: SPEC-MOC-PM-ADVISORS-001
document: acceptance
version: "0.2.0"
status: completed
created: 2026-07-10
updated: 2026-07-11
---

# Acceptance — SPEC-MOC-PM-ADVISORS-001

All commands run from repo root `/Users/goos/MoAI/claude.mo.ai.kr`. "expect: no matches" means grep exit code 1. Evidence (verbatim output) is recorded in `progress.md §E.2`.

## §D AC Matrix

| AC | Requirement | Verification command | Pass condition |
|----|-------------|----------------------|----------------|
| AC-PMA-001 | REQ-G-001, REQ-M-001, REQ-R-006 | `test -f plugins/moai-pm/skills/goose/SKILL.md && test -f plugins/moai-pm/skills/moai/SKILL.md && test ! -e plugins/moai-pm/skills/project && echo PASS \|\| echo FAIL` | `PASS` |
| AC-PMA-002 | REQ-R-003 (single evolution model) | `grep -rn "metrics.csv\|Self-Refine\|self-refine" plugins/moai-pm/` | no matches |
| AC-PMA-003 | REQ-R-005 (prefix ownership) | `grep -rn "moai-coworker:story-\|moai-coworker:book-" plugins/moai-pm/` | no matches |
| AC-PMA-004 | REQ-G-008 (Desktop parity — all 3 classes named) | `grep -q "^## Desktop Parity Constraints" plugins/moai-pm/skills/goose/SKILL.md && for c in hooks LSP output-styles; do grep -q "$c" plugins/moai-pm/skills/goose/SKILL.md \|\| echo "MISSING:$c"; done` | heading present AND zero `MISSING:` lines (each of `hooks` / `LSP` / `output-styles` literally named in the prohibition section) |
| AC-PMA-004b | REQ-G-008 (negative — goose emits NO hooks/LSP artifact) | `grep -cE '\.lsp\.json\|hooks/' plugins/moai-pm/skills/goose/SKILL.md plugins/moai-pm/skills/goose/references/claudemd-generator.md 2>/dev/null \| awk -F: '{s+=$2} END{print s+0}'` | `0` — goose never names a `.lsp.json` file or a `hooks/` directory as a generation target (the Desktop-parity prohibition is worded in prose class names `hooks`/`LSP`/`output-styles`, never the artifact-path tokens `.lsp.json` / `hooks/`) |
| AC-PMA-005 | REQ-G-005a (HARD blocks preserved, exact) | `test "$(grep -cE '^## .*\(HARD\)' <goose Desktop CLAUDE.md template path recorded in progress.md §E.2 by M1>)" -eq 8 && echo PASS \|\| echo FAIL` | `PASS` — exactly the 8 `## N. … (HARD)` H2 blocks preserved. Baseline is the FIXED literal 8 (measured from source `skills/project/references/templates/CLAUDE.md.tmpl` at M1 via the same pattern: `grep -cE '^## .*\(HARD\)'` → 8), NOT a runtime-recomputed count. The source uses parenthesized `(HARD)`; `grep -c '\[HARD\]'` on the source is 0 and MUST NOT be used |
| AC-PMA-005b | REQ-G-005b (line-budget overflow policy retained) | `G=plugins/moai-pm/skills/goose/references/claudemd-generator.md; grep -qiE "라인 예산\|line budget\|예산\|budget" "$G" && grep -qiE "체인\|chain" "$G" && grep -qiE "축소\|shrink\|shrunk\|shrank" "$G" && grep -qE "NFR-PMR-002\|200" "$G" && echo PASS \|\| echo FAIL` | `PASS` — the goose claudemd-generator variant retains: the line-budget table (KO `라인 예산` / EN `line budget`), a chain reference (`체인`/`chain`), a shrink-stem reference (`축소`/`shrink`/`shrunk`, tense-independent — the shrink-chains-only rule), and the ≤200 / NFR-PMR-002 invariant |
| AC-PMA-006 | REQ-G-006 (4 triggers documented — English tokens) | `for t in "repeated correction" "chain failure" "/project evolve" "inventory drift"; do grep -q -- "$t" plugins/moai-pm/skills/goose/SKILL.md \|\| echo "MISSING: $t"; done` | no `MISSING` lines (note `/project evolve` is single-slash; `//project` is a defect) |
| AC-PMA-007 | REQ-M-005 (namespace documented) | `grep -q "moai-pm:moai" plugins/moai-pm/skills/moai/SKILL.md && grep -q "moai:moai" plugins/moai-pm/skills/moai/SKILL.md && echo PASS \|\| echo FAIL` | `PASS` |
| AC-PMA-008 | REQ-D-001 (README 2-skill entry) | `grep -q -- "/goose" plugins/moai-pm/README.md && grep -q -- "--project" plugins/moai-pm/README.md && echo PASS \|\| echo FAIL` | `PASS` |
| AC-PMA-009 | REQ-D-002 (marketplace bump) | `jq -r '.plugins[] \| select(.name=="moai-pm") \| .version' .claude-plugin/marketplace.json` | value ≠ M1 baseline (observed baseline 2026-07-10 = `0.4.0`; run-phase M5 bumps it) |
| AC-PMA-010 | REQ-D-003 (www target list recorded) | `grep -c "www/" .moai/specs/SPEC-MOC-PM-ADVISORS-001/progress.md` | ≥ 1 |
| AC-PMA-011 | REQ-R-001 (link integrity) | `for s in goose moai; do grep -oE '\]\((references/[^)#]+)\)' plugins/moai-pm/skills/$s/SKILL.md \| sed -E 's/\]\((.*)\)/\1/' \| while read -r f; do test -f "plugins/moai-pm/skills/$s/$f" \|\| echo "BROKEN: $s/$f"; done; done` | no `BROKEN` lines |
| AC-PMA-012 | REQ-X-001, REQ-X-002 (language + boundary documented) | `for s in goose moai; do grep -q "conversation_language" plugins/moai-pm/skills/$s/SKILL.md && grep -q "AskUserQuestion" plugins/moai-pm/skills/$s/SKILL.md \|\| echo "MISSING: $s"; done` | no `MISSING` lines |
| AC-PMA-013 | REQ-R-002 (drift-line closure) | Re-run the M1-captured drift greps (exact patterns recorded in progress.md §E.2) against migrated content | all M1-captured drift patterns → no matches in `plugins/moai-pm/` |
| AC-PMA-017 | REQ-M-009 (legacy subcommand destinations) | `for c in resume catalog status apikey doctor feedback evolve; do grep -qE "^\\\| $c \\\|" .moai/specs/SPEC-MOC-PM-ADVISORS-001/design.md \|\| echo "MISSING:$c"; done` | no `MISSING` lines — every one of the 7 legacy subcommands has a `\| <token> \|` destination row in design.md §F.1 (verifiable at plan-time against design.md) |
| AC-PMA-018 | REQ-M-008 (command-surface disambiguation) | `grep -q -- "/moai project" plugins/moai-pm/skills/moai/SKILL.md && grep -q -- "/moai --project" plugins/moai-pm/skills/moai/SKILL.md && grep -q -- "Skill(\"moai:moai\")" plugins/moai-pm/skills/moai/SKILL.md && echo PASS \|\| echo FAIL` | `PASS` — moai SKILL.md documents BOTH the coder subcommand `/moai project` (with its `Skill("moai:moai")` dispatch) and the new `/moai --project` flag, as distinct surfaces |
| AC-PMA-019 | REQ-G-007 (self-improvement guardrail) | `grep -q "CLAUDE.md" plugins/moai-pm/skills/goose/SKILL.md && grep -qE '\.claude/agents' plugins/moai-pm/skills/goose/SKILL.md && grep -qE '≤ ?3\|최대 3\|3 files\|3개' plugins/moai-pm/skills/goose/SKILL.md && echo PASS \|\| echo FAIL` | `PASS` — the goose `## Recursive Self-Improvement` guardrail names the ONLY-modifiable set (`CLAUDE.md` + `.claude/agents/`) and the ≤3-files-per-improvement cap |
| AC-PMA-020 | REQ-M-003 (moai generation targets) | `for t in "CLAUDE.md" ".claude/agents" ".claude/skills" "settings.json" "hooks" ".mcp.json"; do grep -q -- "$t" plugins/moai-pm/skills/moai/SKILL.md \|\| echo "MISSING:$t"; done` | no `MISSING` lines — moai `## Generation Targets` lists all 6 target classes |
| AC-PMA-021 | REQ-M-004 (LSP presence check) | `grep -qE "^## LSP Presence Check" plugins/moai-pm/skills/moai/SKILL.md && grep -q "LSP" plugins/moai-pm/skills/moai/SKILL.md && echo PASS \|\| echo FAIL` | `PASS` — moai SKILL.md carries the `## LSP Presence Check` anchor consuming SPEC-MOC-CODER-LSP-MCP-001 guidance |
| AC-PMA-022 | REQ-M-007 (Claude Code runtime assumption) | `grep -qiE "Claude Code (runtime\|런타임)" plugins/moai-pm/skills/moai/SKILL.md && echo PASS \|\| echo FAIL` | `PASS` — moai SKILL.md states its generated artifacts assume the Claude Code runtime (hooks/LSP valid), the inverse of goose's Desktop-parity prohibition |

### §D.1 Structural-review ACs (not fully greppable)

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-PMA-014 | REQ-G-004 (user-custom agents, never prebuilt copies) | Reviewer reads `## Custom Agent & Skill-Chain Design`: the design procedure derives agents from interview context; contains an explicit prohibition on copying prebuilt plugin agents |
| AC-PMA-015 | REQ-R-004 (Phase 7 restored) | Goose setup canon (migrated cowork-setup successor) contains the custom-agent generation phase in its phase sequence |
| AC-PMA-016 | REQ-X-003 (anti-slop chain preserved) | Migrated references retain the anti-AI-slop post-processing chain sections wherever the source canon mandated them (M1 records which source files carry them) |

## Given-When-Then Scenarios

### S1 — Goose canonical flow order (structural)

- **Given** the authored `plugins/moai-pm/skills/goose/SKILL.md`
- **When** the six canonical H2 anchors (design.md §A.1) are extracted in file order: `grep -n "^## Socratic Interview\|^## Plugin Inventory Scan\|^## Custom Agent & Skill-Chain Design\|^## Generation Targets\|^## Recursive Self-Improvement\|^## Desktop Parity Constraints" plugins/moai-pm/skills/goose/SKILL.md`
- **Then** all six anchors are present, in exactly that order (interview → inventory scan → design → generation → self-improvement → parity).

### S2 — MoAI degraded mode without coder plugin (structural)

- **Given** the authored `plugins/moai-pm/skills/moai/SKILL.md`
- **When** the `## Namespace & Routing` section is inspected
- **Then** it defines BOTH branches: coder-plugin-installed (route execution) and coder-plugin-absent (guidance-only + embedded catalog fallback), and the fallback branch never attempts execution routing. Grep gate: `grep -q "fallback" plugins/moai-pm/skills/moai/SKILL.md`.

### S3 — Edge: re-invocation on an already-initialized project

- **Given** a target project that already contains CLAUDE.md / `.moai/`
- **When** `/goose --project` or `/moai --project` is invoked again
- **Then** the SKILL.md flow mandates overwrite confirmation before touching existing artifacts (no silent overwrite). Grep gate: both SKILL.md files document the re-invocation/overwrite-confirmation behavior.

### S4 — Edge: interview stalls at grade C

- **Given** an interview topic that remains grade C after questioning
- **When** generation would otherwise begin
- **Then** the flow either blocks with an explicit ask or proceeds with assumptions documented into `.moai/context.md` — documented in the goose `## Socratic Interview` section.

## Quality Gate Criteria

- All 21 machine-gate ACs (AC-PMA-001..013, 004b, 005b, 017..022) executed with verbatim evidence in progress.md §E.2 (no claimed-not-run rows). Each command's exit status or numeric/`PASS`/`FAIL` output alone decides the row.
- Structural-review ACs (014-016) signed off with file+section citations.
- Zero writes outside §D-constraint scope (verify: `git status --porcelain` diff set ⊆ owned paths).
- No git push; commits pathspec-scoped.

## Definition of Done

1. AC matrix: 21/21 machine gates PASS + 3/3 structural reviews cited.
2. `skills/project/` fully removed including stray runtime artifacts.
3. progress.md §E.2/§E.3 populated by manager-develop with evidence.
4. Residual risks (plan.md §Open design risks) re-stated with run-phase status (resolved / still-open) — still-open items carried to sync report.
