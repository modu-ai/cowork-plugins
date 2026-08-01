---
name: bootstrap-desktop-001-verdict-iter2
description: plan-auditor iter-2 verdict for SPEC-MOC-BOOTSTRAP-DESKTOP-001 — FAIL 0.73 (harmonic) / 0.76 (avg), STOP signal (score regression vs iter-1 0.77)
type: project
---

# SPEC-MOC-BOOTSTRAP-DESKTOP-001 — plan-auditor iter-2 verdict

Verdict: **FAIL** — aggregate 0.73 (harmonic, skeptical-stance) / 0.76 (simple avg). Tier M PASS threshold = 0.80. **STOP signal** raised (score not higher than iter-1 0.77 → LEAN score-regression clause).

**Why:** 3 of 7 mandatory ACs (AC-BD-001, AC-BD-006 always-deterministic part, AC-BD-008) are mechanical false-passes — their `≥1`/existence predicates self-pass against current HEAD pre-implementation, giving zero discriminating power. iter-2 fixed REQ-BD-007 traceability (explicit deferral, verified) and the D4 non-existent-path premise (`plugins/moai-cowork/commands/` confirmed absent), but the AC-BD-006 "hardening" traded non-determinism for vacuousness (always-deterministic component all self-passes; the R4 release-checklist deliverable is not discriminatingly tested — broad `SSOT` grep matches 63 unrelated lines, 0 precise `release-checklist`/`일괄 bump` matches). AC-BD-001 skill-profile grep matches only the SPEC's own artifacts (0 non-SPEC matches) and the skill-profile artifact path is left undefined, so it cannot be a hard gate.

**How to apply:** On iter-3, require manager-spec to (a) give AC-BD-001 a discriminating predicate with a concrete skill-profile artifact path, (b) give AC-BD-006 a specific sentinel for the unified release-checklist line (not a broad `SSOT` grep), (c) give AC-BD-008 a concrete reverse-edit-trace grep pattern. Because the score regressed, prefer scope-reduction: carve R4 (version-SSOT unification) into its own SPEC and either specify or defer R1's skill-profile artifact. Must-pass firewall: MP-1 PASS, MP-2 PASS (13/14 GEARS; REQ-BD-007 deferred), MP-3 PASS (canonical 12-field per project SSOT — NOT the generic created_at/labels set), MP-4 N/A. D7 PASS (all referenced SPECs exist, none retired/superseded). D8 auto-PASS (no syscall).

Per-dimension: Clarity 0.85 / Completeness 0.88 / Testability 0.52 / Traceability 0.80.

Related: [[project_moc_v3_epic_specs_iter2_blocked]] (Epic tracker).
