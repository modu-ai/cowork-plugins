---
name: project-remediation-001-verdict
description: SPEC-MOC-PLUGIN-REMEDIATION-001 plan-audit — iter1 PASS-WITH-DEBT 0.83, iter2 FAIL 0.74+STOP, iter3 PASS 0.88 (false-pass class eliminated everywhere, mechanically re-verified vs HEAD)
type: project
metadata:
  type: project
---

## iter-3 verdict (2026-07-02, FINAL) — PASS 0.88 (regression recovered)

**Verdict: PASS** (Tier L threshold 0.85; harmonic aggregate ≈0.88). iter-2 0.74 → iter-3 0.88 = **+0.14, no regression** (LEAN STOP clause does NOT fire). Per-dim: Clarity 0.90 / Completeness 0.85 / **Testability 0.85** (recovered from 0.52) / Traceability 0.95. MP-1..4 all PASS (REQ-REM-001..024 seq clean 24↔24; 24 valid GEARS; frontmatter 12 canonical fields; MP-4 N/A single-domain Korean). D7 refs all exist, none retired/superseded (COWORK-002 implemented, DESIGN/BOOTSTRAP/SITE-IA draft). D8 syscall=0.

**Mechanical false-pass class ELIMINATED EVERYWHERE (exhaustive HEAD sweep, verified myself, not trusted from §D.8.10):** ran EVERY `≥1` addition-predicate against HEAD 6d78fbf. All show not-yet-done (0): 001 0/0/0 (OLD 에서.*로=6); 002 all 5 files 0/0/0 (was single 대시); 003 heading 0 (OLD 슬라이드|genre=5); 004 0/0/0 (OLD 5,1); 005 0 + awk-heading exists L87 (OLD 에서.*로=3); 013 all 8=0; 014-wiring project router=0 (OLD recursive=6 peripheral); 019 pointer 0 + systems STILL-FULL (OLD 참조=6); 020 0/0 (OLD=2); 021 0/0 (OLD 에서.*로|slop=5); 024 §E.2-scoped 0 (OLD file-wide=2). 5 HEAD-absent literals + 카피 전용 게이트 all grep -rl=0 tree-wide (implementer must author verbatim). Defect preds all discriminate ≥1 on HEAD: 008 1/1; 009 all 12 literals; 010 집중력200=1 + density 33/33/25/20; 011 boilerplate 50 files (NOT vacuous); 012 41/10; 015 72; 016 8; 017 stale 3 + GHOST-PRESENT.

**Residual run-phase debts (bounded literal-authoring / reviewer-judgment, NOT structural, NOT must-pass):** (1) literal-exactness — 6 exact strings must be authored verbatim (§D.6 discloses + recommends). (2) AC-010(4 report skills)+AC-012 `<baseline` density satisfiable by single-dash removal — SHOULD-PASS, backstopped by EC-6 + P4 lint. (3) Tier-L 5-artifact set folded to 3+progress (design/research folded into §A.2/A.3/§F, extractable). (4) specific literals only catch enumerated slop; new slop guarded only by P4 lint CI (AC-022). All disclosed. **No scope-reduction needed** — the 24-REQ/6-M Tier-L structure is sound; the iter-1→2 regression was purely predicate-discrimination, now resolved.

---

## iter-2 verdict (2026-07-02) — FAIL 0.74 + STOP signal

**Verdict: FAIL** (Tier L threshold 0.85; harmonic aggregate ≈0.74). **STOP emitted** — iter2 (0.74) < iter1 (0.83) per LEAN regression clause. The drop is NOT SPEC degradation — the iter-2 SPEC genuinely fixed all 5 iter-1-flagged defects — it is newly-surfaced *pre-existing* defects my under-audited iter-1 missed. Per-dim: Clarity 0.88 / Completeness 0.82 / Testability **0.52** / Traceability 0.90. MP-1..4 all PASS (REQ 001-024 seq clean; GEARS valid; frontmatter canonical 12-field; MP-4 N/A single-domain).

**iter-1 regression items — ALL RESOLVED:** AC-004 (hardened copy-only STAGE `카피 전용 게이트`, HEAD 0/0/0 — discriminating); AC-005 (title-rule descriptor inside 6-block template awk-range, HEAD 0, broad `에서.*로` OR dropped); AC-009 (all 7 sources, 12 exemplary-slop literals, each ≥1 on HEAD→0); AC-012 (exemption `grep -vE "대시|❌|✅|나쁜 예|좋은 예"`, additions auto-exempt, HEAD 41/10==baseline); Unwanted→Ubiquitous relabel (006/007/015/023 genuinely negative).

**SURVIVING/NEW defects — same mechanical-false-pass class §D.8 claims to have eliminated but applied narrowly (only 004/005/009/010/012):**
- **AC-003 (SHOULD) FULL self-pass**: `grep -c "슬라이드\|카피 장르\|genre"` = **5** on HEAD (matches `--genre` CLI flags) → zero discriminating power.
- **AC-019 (SHOULD) FULL self-pass**: pointer predicate = **6** on HEAD (`참조` incidental) + design canonical already exists; cowork copy is still a full 180-line skill w/ samples/+systems(78) — dedup undetectable. AC-010 subsumes into this false-pass AC.
- **AC-020 (SHOULD) FULL self-pass**: = **2** on HEAD (`책임 경계` + `moai-cowork:personal-branding` row already present).
- **AC-021 (SHOULD) FULL self-pass**: OR = **5** on HEAD (`slop` matches `ai-slop-reviewer` L245/251; `에서` matches incidental L25/100/144).
- **AC-001(c) (MUST-PASS release-blocking) vacuous clause**: 3rd sub-predicate `에서.*로` = **6** on HEAD — pattern-(c) "A에서 B로" registration unverifiable (conjunction still fails on HEAD via 대시=0, so not a full self-pass, but the release-blocking gate can't confirm pattern c).
- **AC-014(wiring) vacuous clause**: `grep -rc "moai-workflow-design"` ≥1 already on HEAD → wiring verification vacuous (advisory `<baseline` clause still discriminates).

**Lesser:** AC-002 verifies only `대시` (1 of REQ-002's 3 patterns); AC-017 phantom-dir `find -type d -empty` over-reaches (7 empty dirs, only 1 is REQ-017's ghost); AC-008 `grep -c " — "` not scoped to title fields as prose claims.

**Recommendation:** systematic re-audit of EVERY `≥1` addition-predicate against HEAD (the fix must generalize, not whack-a-mole per flagged AC) — repair AC-003/019/020/021 to structural/defect predicates, AC-001(c)/014(wiring) to discriminating clauses. OR scope-reduce (split 24-REQ/6-milestone Tier-L into gate-structure + decontamination + rename/dedup + lint-CI sub-SPECs). Do NOT grant PASS-WITH-DEBT a 2nd time on a regressing score.

---

## iter-1 verdict (below — retained)


SPEC-MOC-PLUGIN-REMEDIATION-001 (Korean-slop plugin remediation, Tier L, release-blocking) iteration-1 verdict: **PASS-WITH-DEBT, score 0.83** (Tier-L clean-PASS threshold 0.85). All 4 plan-auditor MUST-PASS (MP-1 REQ seq, MP-2 GEARS, MP-3 frontmatter, MP-4 N/A) hold.

**Why:** Requirements / evidence-integrity / scope / sequencing are genuinely strong — every spot-checked defect (pdf-writer moai-office L56/59/60/95, humanize-korean moai-content L73/89/170, newsletter:35, live-commerce:79 "집중력 200%", detail-page-copy 13-sections:38, deck-sample.json, ai-slop-reviewer 대시=0) was confirmed real at the exact claimed location, and count-drift (cowork 177, deprecated-ns now 72 vs plan 68 vs audit 78) is handled by predicate-based ACs by design. The debt is concentrated in the AC layer: BLOCKING-DEBT — MUST-PASS release-blocking AC-REM-004 & 005 self-pass pre-remediation (see [[mechanical-ac-false-pass-check]]); SHOULD-FIX — AC-009/010 under-cover their REQ (commerce-channel-message 46 em-dashes, executive-summary/pm-weekly 33 each go unchecked), AC-012 grep contradicts its own EC-3 exemption and conflicts with the dash-descriptor insertion required by REQ-001/002.

**How to apply:** On iteration 2 regression check, verify these are RESOLVED: (1) AC-004 asserts a copy-only STAGE marker not keyword presence; (2) AC-005 drops the broad `에서.*로` OR clause / uses literal descriptor; (3) AC-009/010 enumerate all REQ-listed sources (per-file defect→0), not 1-2 sample strings; (4) AC-012 encodes the negative-example exemption or is re-baselined. If unchanged across iters → stagnation flag. MINOR (need not block): SPEC excludes two non-existent paths (plugins/moai-cowork/commands, internal/template/templates absent in this repo); four REQs labeled "(Unwanted)" are actually Ubiquitous positive `SHALL rewrite/repair`.
