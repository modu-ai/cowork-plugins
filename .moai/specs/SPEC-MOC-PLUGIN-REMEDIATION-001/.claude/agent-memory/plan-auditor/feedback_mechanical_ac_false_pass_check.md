---
name: mechanical-ac-false-pass-check
description: When auditing predicate-based ACs, run the predicate against the PRE-remediation tree — if it already passes, the AC cannot verify its REQ (false-PASS)
metadata:
  type: feedback
---

When a SPEC claims "every AC is a re-runnable mechanical predicate", DO NOT stop at "is it a grep command?". Run each predicate against the CURRENT (pre-remediation) tree. If a `≥1` presence-grep already returns `≥1` before any work is done, the AC has zero discriminating power — it will report PASS regardless of whether the REQ's deliverable exists.

**Why:** In SPEC-MOC-PLUGIN-REMEDIATION-001 (Tier L, release-blocking) three MUST-PASS ACs self-passed pre-remediation:
- `에서.*로` is natural Korean word co-occurrence (텍스트**에서** … 글쓰기**로**), so `grep -c "에서.*로"` returned 6 on the unmodified file — the "transition-formula descriptor present" clause is un-verifiable. Same broad-OR made AC-REM-005 (notebooklm) already return 3.
- AC-REM-004 grepped `카피|copy` (already 5) + `ai-slop-reviewer|humanize-korean` (already referenced at L280) — both halves passed before the required "copy-only stage" was added.

**How to apply:** For every `≥1` addition-predicate AC, execute it against HEAD before scoring. Flag any that already pass. Prefer: (a) specific literal descriptors over broad regex that matches incidental language, (b) structural/stage markers over keyword presence, (c) AND-semantics over OR when multiple distinct additions are required. Defect-predicates (`→0`) are naturally immune (a defect that is already absent is a true pass), so this check targets addition-predicates specifically. Related: [[project_remediation_001_verdict]].

**iter-2 escalation (2026-07-02):** the fix must GENERALIZE across ALL addition-predicates, not just the specifically-flagged ones. In REMEDIATION-001 iter-2, manager-spec hardened only the 5 named ACs (004/005/009/010/012) and left the SAME false-pass class in 6 others — AC-003 (`슬라이드|genre`=5, matches `--genre` flags), AC-019 (`참조`=6), AC-020 (=2), AC-021 (`slop` matches `ai-slop-reviewer`, `에서` incidental =5), AC-001-clause-c (`에서.*로`=6 in a MUST-PASS), AC-014-clause-wiring (term already present). Two audit lessons: (1) an OR predicate containing a substring that appears in a common on-tree token (`slop`⊂`ai-slop-reviewer`, `에서`=Korean postposition, `genre`=CLI flag, `참조`/`personal`=ubiquitous) is almost always a self-pass — grep the token file-wide on HEAD first. (2) When an author fixes flagged instances but not the class, that is the Opus "does not silently generalize" behavior — the auditor MUST enumerate the FULL predicate set every iteration, never trust that a prior-iter fix covered siblings.
