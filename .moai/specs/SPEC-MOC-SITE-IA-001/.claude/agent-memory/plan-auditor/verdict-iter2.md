---
name: site-ia-001-verdict-iter2
description: plan-audit iter-2 verdict for SPEC-MOC-SITE-IA-001 — FAIL 0.84 near-miss (AC-006 self-passes at HEAD; stale R2 baseline). Improved from iter-1 0.83, no STOP.
metadata:
  type: project
---

SPEC-MOC-SITE-IA-001 plan-audit **iteration 2/3 → FAIL, aggregate 0.84** (harmonic; arith 0.853). Tier L threshold 0.85. Near-miss, improved from iter-1 0.83 → no STOP/regression.

**Why:** The mandatory addition-predicate discrimination check found **AC-IA-006 self-passes at current HEAD** (`grep -rhE '^aliases:' www/content/design | grep -oE '/claude-design/...' | sort -u | wc -l` = 10 ≥ 10 threshold, pre-implementation). Root cause: the DESIGN merge (R2) was already performed in commit 6d78fbf — `content/design/` already carries all 10 `/claude-design/*` aliases AND the unique `official-quickstart.md`; only `content/claude-design/` dir deletion remains. AC-006 is a SPEC-designated must-pass yet has zero discriminating power. Consequently the §A.2 / plan §A R2 baseline ("design≈claude-design → 병합 대상") is STALE, misleading run-phase scope.

Per-dimension: Clarity 0.80 (stale R2 baseline), Completeness 0.88 (all sections + 6 H3 Out-of-Scope; Tier-L design.md/research.md inlined per plan §H), Testability 0.73 (AC-006 non-discriminating must-pass + AC-024 floor guard covers only content/cli/**, escapable for rewritten plugins/DESIGN), Traceability 1.00 (24 REQ↔24 AC 1:1, D7 both refs draft/exist, D8 no syscall).

MP firewall: MP-1 PASS (REQ-IA-001..024, no gaps/dupes, 3-digit padding; 024 out-of-doc-order but complete), MP-2 PASS (all 24 REQs valid GEARS), MP-3 PASS (12 canonical fields, created/updated/tags per project SSOT), MP-4 N/A (single-project www docs).

Resolved from iter-1: D1 (AC-023 hugo-exit-0 demoted, check-links.mjs named run-phase deliverable — check-docs-health.mjs mis-path to docs-site/content confirmed), D3 (AC-012 `|| true` removed, grep-match FAILS), D4-enumeration (ia_in_scope marker, in-scope set=0 at HEAD discriminates). D2 only PARTIALLY resolved (AC-010 now discriminates=0 baseline 33 grounded; AC-006 still non-discriminating).

**How to apply:** iter-3 fix is narrow — (1) correct §A.2 + plan §A R2 baseline to state the design/claude-design merge is already done in design/ (aliases + official-quickstart present); remaining R2 work = delete content/claude-design/ only. (2) Reframe AC-IA-006 into a discriminating check: post-deletion regression guard (alias count stays ≥10 AFTER claude-design/ removed) cross-referenced to AC-005 (dir absence, which DOES discriminate) + AC-023 link checker — OR demote AC-006 from must-pass. (3) Optionally extend AC-024 floor guard beyond content/cli/** to all in-scope rewritten pages. When re-auditing www IA SPECs, always run every ≥N addition-predicate against HEAD first — pre-existing repo state (prior commits) can silently satisfy a "grounded" baseline.
