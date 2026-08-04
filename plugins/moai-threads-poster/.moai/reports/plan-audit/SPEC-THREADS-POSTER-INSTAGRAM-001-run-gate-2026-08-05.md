# Plan Audit Gate Report — SPEC-THREADS-POSTER-INSTAGRAM-001

**Audit date:** 2026-08-05
**Auditor:** plan-auditor (independent, adversarial — M1 Context Isolation applied; author reasoning ignored)
**Tier:** M (declared by orchestrator; frontmatter `tier:` field absent — see D4)
**PASS threshold:** 0.80 (Tier M)
**Iteration:** 1 (run-gate stream — run-gate-2026-08-05)

---

## Verdict

```
VERDICT: FAIL
AGGREGATE_SCORE: 0.83
DIMENSIONS: req=0.85 ac=0.85 consistency=0.80 scope=0.90 risk=0.75
```

The aggregate (0.83) clears the Tier M threshold (0.80). The FAIL is driven by a single must-pass firewall finding (MP-2: acceptance criteria are not in GEARS/EARS format). The underlying substance of the SPEC is strong; the blocker is a format-compliance gap with a cheap remediation path.

---

## Must-Pass Results

- **[PASS] MP-1 REQ number consistency.** `spec.md` REQ-INST-001 through REQ-INST-024, sequential, no gaps, no duplicates (24 unique IDs, verified `grep -oE 'REQ-INST-[0-9]{3}' spec.md | sort -u`). Zero-padding consistent.

- **[FAIL] MP-2 EARS/GEARS format compliance.** acceptance.md contains 33 acceptance criteria; **all 33 use Given/When/Then format, zero use a GEARS "shall" pattern** (`grep -cE '\bshall\b' acceptance.md` = 0; `grep -cE '^\s*-?\s*\*\*Given\*\*' acceptance.md` = 33). MP-2 requires every AC to match one of the five GEARS patterns (Ubiquitous / Event-driven / State-driven / Where / Unwanted) or legacy EARS equivalents. Given/When/Then is none of these. The M3 rubric explicitly classifies Given/When/Then as a non-GEARS format (Score 0.50 band). **This is the sole driver of the FAIL verdict.** See Defect D1 for the nuance (testability is HIGH; this is format-only) and the cheap remediation.

- **[PASS] MP-3 YAML frontmatter validity.** All three artifacts carry the canonical 12 fields with correct types and no rejected snake_case aliases: `id`, `title`, `version: "0.1.0"` (quoted semver), `status: draft`, `created: 2026-08-05`, `updated: 2026-08-05`, `author: manager-spec`, `priority: P1`, `phase: "v1.1.0 target"`, `module: "plugins/moai-threads-poster"`, `lifecycle: spec-anchored`, `tags: "..."`. No `created_at` / `updated_at` / `labels` / `spec_id` aliases. (The optional `tier:` field is absent — see D4, a SHOULD not a MUST.)

- **[N/A] MP-4 Section 22 language neutrality.** Single-language SPEC (Python plugin). Auto-passes.

- **[N/A] MP-5 D7 cross-SPEC reconciliation.** No external SPEC IDs referenced anywhere in spec.md / plan.md / acceptance.md (`grep -oE 'SPEC-([A-Z][A-Z0-9]+-)+[0-9]+'` returns only the SPEC's own ID). The verification verb has nothing to reconcile.

- **[N/A] MP-6 D8 cross-platform discipline.** No `syscall` substring anywhere in the three artifacts (Python plugin; the syscall build-tag concern is Go-specific). Auto-passes.

- **[PASS (with caveat)] MP-7 clarification gate.** `grep -rn '\[NEEDS CLARIFICATION'` matches `plan.md:260`. Substantively this is a **negative assertion** — the marker text reads `[NEEDS CLARIFICATION: none at plan time]`, i.e. the author is affirming there are no open plan-phase clarifications (endpoint-verification items are explicitly deferred to run-phase as @MX:TODO markers). This is the opposite of an unresolved topic blocking the plan. Judged NOT an unresolved marker per MP-7's intent ("unresolved `[NEEDS CLARIFICATION: <topic>]` markers"). The literal-token grep would flag it; the substance does not. See D5 (SHOULD — rephrase to remove the false-positive grep hit).

---

## Dimension Scores

| Dimension | Score | Band | Evidence |
|-----------|-------|------|----------|
| 1. Requirements quality (GEARS modality, unambiguous) | 0.85 | high | spec.md §B REQ-INST-001..024 all carry explicit GEARS modality labels (Ubiquitous / Capability gate / Event-detected / State-driven). REQ-INST-009 corrects the scheduling premise prominently. Minor: some implementation symbols (`InstagramClient`, `_container_call`, `_process`) leak into REQs — acceptable for a plugin-scoped SPEC mirroring an existing codebase's naming. |
| 2. Acceptance-criterion testability | 0.85 | high | Every P0 AC has a concrete mechanical verification path (pytest assertion, `httpx.MockTransport` URL/params inspection, `PRAGMA table_info`, registry enumeration, `grep -rn` for forbidden tokens, version-string comparison). The 134-test baseline is correctly deferred to run-phase observation (§D.3.1) per verification-claim-integrity. Gap: `instagram_queue_publish_due` has no AC (D2). |
| 3. Internal consistency | 0.80 | good | LOCKED decisions #1–3 reflected consistently: no-server-side-scheduling (spec §B.3/§E/§H, plan §B/AP-1, AC-M3-9/AC-M4-2); unified queue + platform column (spec REQ-INST-011..015, plan M1/M3.a, AC-M1-*); Facebook Login auth (spec REQ-INST-003/§D, plan M2 D2/D3, AC-M2-3/AC-M4-5). No substantive contradictions. Drifts: v23.0 trailing slash (D6); publish-due tool in spec+plan but not AC (D2); `tier:` field absent (D4). |
| 4. Scope discipline | 0.90 | high | §H Out of Scope is exemplary — 10 `### Out of Scope — <topic>` H3 sub-headings, each with specific `-` bullets (Threads behavior, Carousel, Stories/Live/Shopping, auto-publish, server-side scheduling, container 24h EXPIRY, personal accounts, cross-posting, web UI, cowork-level migration). Milestone decomposition M1→M4+Sync covers all 24 REQs. Deferred-to-run-phase items (comments/insights endpoints, API version) are explicitly flagged with @MX:TODO + §D.4 forward-looking gate. |
| 5. Risk coverage | 0.75 | moderate | Concern A (version drift): covered by §D.4 run-phase gate but spec hardcodes v23.0 in a REQ without rationale. Concern B (publish-due AC gap): real hole — D2. Concern C (client_resolver back-compat): handled implicitly at runner level (AC-M3-6) but the call-site migration + creds-absent failure path are under-specified — D3. Concern D (AC testability): PASS — all P0 ACs mechanically verifiable. REQ-INST-008 (private-URL rejection) and REQ-INST-017 (PPA error) have thin/no AC coverage — D8. |

---

## Defects Found

### MUST (blocking — drives FAIL verdict)

**D1 — MP-2 AC format non-compliance.** `acceptance.md` (all sections §D) — All 33 acceptance criteria use Given/When/Then BDD format; none use a GEARS/EARS "shall" pattern. MP-2 requires every AC to match one of the five GEARS patterns.
- **Severity:** MUST (MP-2 must-pass firewall)
- **Nuance (important for the orchestrator's gating decision):** This is a **format-conformance** defect, NOT a testability defect. The Given/When/Then ACs are highly mechanically testable (dimension 2 scores 0.85) — they map 1:1 to pytest fixtures and are arguably MORE directly automatable than EARS prose. The SPEC's REQUIREMENTS (spec.md §B) ARE in proper GEARS notation. The defect is narrowly that the ACs use a different structured format than MP-2 mandates.
- **Required fix (cheapest first):** Add a one-line deviation note at the top of `acceptance.md` declaring that this SPEC uses BDD Given/When/Then as its accepted AC format (a project-level deviation for this Python/pytest plugin), and that the GEARS-bearing artifact is `spec.md` §B. This takes one line and changes zero test substance. Alternative (heavier): rewrite all 33 ACs in GEARS "The `<subject>` shall ..." form. Alternative (orchestrator-level): waive MP-2 for this plugin-local SPEC with a recorded rationale.
- **Why FAIL regardless of cheap fix:** The doctrine binds MP-2 as must-pass; this auditor cannot self-waive. The orchestrator and user own the waiver decision.

### SHOULD (does not independently force FAIL, but should be fixed before run-phase)

**D2 — `instagram_queue_publish_due` has no acceptance criterion (orchestrator concern B — CONFIRMED).** `plan.md:338` (M3 D7) + `acceptance.md` AC-M3-1 — plan.md M3 D7 lists `instagram_queue_publish_due(limit=10)` as a deliverable tool, and M3 D8 recommends option (a) ("parallel tools") which PUBLISHES this tool. Yet AC-M3-1's required-tools enumeration omits it. Verified mention counts: `spec.md`=1, `plan.md`=2, `acceptance.md`=0. The publish-due flow is the **actual publishing mechanism** (the critical path per REQ-INST-009/022 — the queue holds intent, this tool triggers publication). An implemented deliverable on the critical path with no matching AC is a testability gap.
- **Severity:** SHOULD
- **Required fix:** Either (a) add `instagram_queue_publish_due` to AC-M3-1's required-tools list with a corresponding Given/When/Then (or GEARS) criterion verifying it processes due Instagram rows; OR (b) finalize M3 D8's decision in the plan body (not just "recommended") and add the corresponding AC for whichever option is chosen.

**D3 — `client_resolver` back-compat under-specified at the call site (orchestrator concern C — PARTIALLY ADDRESSED).** `plan.md` M3.a D1 (L291-296) — The plan specifies the `client_resolver` injection at the `_process` runner level and AC-M3-6 covers runner-level Threads-only back-compat with the default resolver. However, the plan does NOT explicitly specify: (i) how the EXISTING `threads_queue_publish_due` MCP tool call site (which today passes a single ThreadsClient) constructs/passes the default resolver after the refactor; and (ii) the failure path — what happens when a due Instagram row exists but `IG_ACCESS_TOKEN`/`IG_USER_ID` are absent (does the resolver return None, raise, surface `setup_required`, or skip-with-message?). "Default resolver reads env + builds both singletons lazily" implies lazy-on-demand construction (so Threads-only queues never trigger IG-client construction), but the creds-absent failure path for a mixed queue is unstated.
- **Severity:** SHOULD (the single biggest M3 risk per the orchestrator; the safety net exists at the runner level via AC-M3-6 but the call-site + failure-path specification is thin)
- **Required fix:** Add an explicit bullet under M3.a covering: (1) the `threads_queue_publish_due` call-site migration (it now constructs / relies on the default `client_resolver`); (2) the creds-absent failure path for a due Instagram row — recommend "skip the Instagram row, record a setup_required message in the batch `messages` list, continue processing Threads rows" (mirroring AC-M3-2's non-crashing setup_required pattern).

**D4 — `tier:` frontmatter field absent (drift from declared Tier M).** All three artifacts — The artifact set is Tier M (3 files: spec.md + plan.md + acceptance.md; no design.md / research.md), and the orchestrator declares Tier M (PASS threshold 0.80). But the frontmatter omits the optional `tier:` field. Per `.claude/rules/moai/development/spec-frontmatter-schema.md`: "When `tier:` is absent, the SPEC is treated as Tier L for backward compat." Tier L's threshold is 0.85. This creates a threshold-ambiguity: the orchestrator applies 0.80, but a lint-era or future re-audit reading the frontmatter alone would apply 0.85.
- **Severity:** SHOULD
- **Required fix:** Add `tier: M` to all three artifacts' frontmatter so the declared tier is mechanical/explicit.

**D5 — `[NEEDS CLARIFICATION: none at plan time]` triggers the MP-7 grep (false positive).** `plan.md:260` — The literal token `[NEEDS CLARIFICATION` is present, which the MP-7 verification grep (`grep -rn '\[NEEDS CLARIFICATION'`) matches. Substantively the marker is a NEGATIVE assertion: the author affirms there are no open plan-phase clarifications, and endpoint-verification items are explicitly deferred to run-phase as @MX:TODO markers (M2 D7). Judged NOT an unresolved marker per MP-7's intent — but a downstream mechanical auditor or lint rule will flag it.
- **Severity:** SHOULD (documentation hygiene; false-positive risk for downstream mechanical checks)
- **Required fix:** Rephrase to remove the literal `[NEEDS CLARIFICATION` prefix, e.g. "**No plan-phase clarifications.** Endpoint-verification items are run-phase tasks recorded in M1 §Verification and the `@MX:TODO` markers, not plan-phase blockers."

### NICE (non-blocking; tracked for polish)

**D6 — v23.0 URL trailing-slash drift.** `spec.md:68` (`https://graph.facebook.com/v23.0/` with trailing slash) vs `plan.md:190` (`https://graph.facebook.com/v23.0` no slash). AC-M2-3 checks `req.url.host` only, so no test breakage today, but the spec↔plan URL string should match exactly to avoid a future AC tightening the assertion to the full URL.

**D7 — v23.0 version rationale absent (orchestrator concern A — CONFIRMED as minor tension).** `spec.md` REQ-INST-003 (L67-69) + `plan.md` M2 D2 (L190-192) — The version is pinned to v23.0 consistently across both artifacts (no v23/v26 disagreement between spec and plan), but spec.md hardcodes v23.0 as the REQ-INST-003 default base URL while plan.md says "Pin to the API version verified at M2 run-phase time" — a mild spec↔plan tension (spec fixes it; plan defers it). No rationale is given for why v23.0 specifically (vs e.g. the v26.0 the orchestrator notes is current in official docs examples). The §E "verified 2026-06-30 update" provenance is stated but the version-selection reasoning is not. acceptance.md §D.4 provides a run-phase drift safety net (implementer returns a blocker if the version has drifted; orchestrator re-delegates a spec amendment).
- **Disposition:** Not blocking — the §D.4 forward-looking gate is the correct safety net for API-version drift. Recommend adding a one-line rationale to REQ-INST-003 ("v23.0 per the 2026-06-30 Meta docs verification recorded in §E; re-verify at run-phase per acceptance.md §D.4").

**D8 — REQ-INST-008 and REQ-INST-017 have thin AC coverage.** spec.md REQ-INST-008 ("Private/signed URLs shall be rejected with a clear error before the API call where detectable") has no explicit AC exercising the private-URL rejection (the "where detectable" hedge is also mildly imprecise). spec.md REQ-INST-017 (PPA-not-completed error) has no explicit AC surfacing the PPA setup_required error. Both are covered INDIRECTLY (REQ-INST-024's error shape is tested by AC-M2-9; the personal-account case by AC-M3-11), but the specific behaviors lack dedicated edge-case ACs.
- **Required fix:** Consider adding EC entries (P2) for private-URL rejection and PPA-error surfacing.

---

## Concern Disposition (orchestrator's four flagged concerns)

| Concern | Verdict | Disposition |
|---------|---------|-------------|
| **A** — Graph API version drift (v23.0 vs v26.0) | **CONFIRMED (minor / NICE)** | Version is consistent across spec/plan (both v23.0 — no internal disagreement). The tension is that spec hardcodes v23.0 in a REQ while plan defers "pin to run-phase." Rationale for v23.0 specifically is absent. Covered by acceptance.md §D.4 run-phase drift gate. NOT blocking. Live-version verification is a run-phase responsibility (this auditor has no web tools and did not attempt it). See D7. |
| **B** — `instagram_queue_publish_due` AC gap | **CONFIRMED (SHOULD)** | Verified directly: `plan.md` mentions the tool twice (M3 D7 + D8 discussion), `acceptance.md` mentions it zero times. AC-M3-1's required-tools list omits it. The publish-due flow is the critical-path publishing mechanism. See D2. |
| **C** — `threads_queue_publish_due` / `client_resolver` back-compat | **PARTIALLY ADDRESSED (SHOULD)** | Runner-level back-compat IS covered (AC-M3-6 Threads-only default-resolver test; AC-M3-5 mixed-queue dispatch test; M3.a D1 "default resolver ... lazily"). The GAP is at the call-site level: the plan does not spell out how the existing `threads_queue_publish_due` tool constructs/passes the resolver, nor the creds-absent failure path for a due Instagram row. See D3. |
| **D** — AC testability for P0 criteria | **PASS** | Every P0 AC (AC-M1-1, M1-2, M1-5, M2-1..M2-9, M3-1, M3-3, M3-4, M3-5, M3-6, M3-9, M3-10, M4-6) has a concrete mechanical verification path: pytest assertion, MockTransport URL/params inspection, PRAGMA check, registry enumeration, `grep -rn` for forbidden tokens, or version-string comparison. No aspirational prose without a verifiable predicate. (AC-M3-6's "byte-identical" phrasing is slightly aspirational but is immediately sharpened to a concrete assertion: "same `published`/`failed`/`skipped` counts, same `mark_published` calls" — testable.) |

---

## Chain-of-Verification Pass (M6 self-critique)

Second-look re-read of every section. Defects newly surfaced in the second pass:

- **D4 (tier field)** — caught in second pass, not first. The first pass verified all 12 required fields present but did not check the optional `tier:` field against the declared Tier M. Added.
- **D8 (REQ-INST-008 / REQ-INST-017 AC coverage)** — caught in second pass during the full REQ→AC traceability walk. Added.
- Confirmed in second pass: REQ numbering re-checked end-to-end (001→024, no gaps). Traceability re-walked for every REQ — all 24 have at least indirect AC coverage (REQ-INST-010 via AC-M4-3 config note; REQ-INST-008/017 are the thinnest, see D8). No additional cross-REQ contradictions found beyond the publish-due gap (D2).
- The Out of Scope section re-checked for specificity — confirmed 10 H3 sub-headings, each with concrete `-` bullets (not just presence). SC-6 genuinely PASS, not rubber-stamped.

First pass was substantially thorough; second pass added D4 and D8.

---

## Recommendation

**If the orchestrator enforces strict MP-2 (doctrine default):** the FAIL stands. Cheapest remediation is the one-line deviation note at the top of `acceptance.md` (D1 fix option 1) + the SHOULD fixes (D2 add the publish-due AC; D3 spell out the call-site + failure path; D4 add `tier: M`; D5 rephrase the NEEDS CLARIFICATION line). None of these require touching implementation substance. Re-audit scope is narrow: confirm the acceptance.md header note + the new AC + the plan M3.a bullet + the frontmatter `tier: M` + the rephrased L260.

**If the orchestrator waives MP-2 for this plugin-local Python/pytest SPEC** (reasonable judgment call — Given/When/Then is the native pytest-bdd format and the REQs are GEARS-compliant): record the waiver rationale in the run-gate decision, and the remaining SHOULD findings (D2, D3, D4, D5) become the fix-before-run-phase list. The aggregate 0.83 clears the Tier M 0.80 threshold on the substance.

Either path, the four orchestrator-flagged concerns are disposed as above (A: minor/covered, B: confirmed, C: partially-addressed, D: pass).
