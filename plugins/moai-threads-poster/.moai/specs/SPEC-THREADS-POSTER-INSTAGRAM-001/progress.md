---
id: SPEC-THREADS-POSTER-INSTAGRAM-001
title: "Instagram Graph API support for moai-threads-poster — Progress"
version: "0.1.0"
status: draft
created: 2026-08-05
updated: 2026-08-05
author: manager-spec
priority: P1
phase: "v1.1.0 target"
module: "plugins/moai-threads-poster"
lifecycle: spec-anchored
tags: "instagram, graph-api, facebook-login, mcp, sqlite-queue, social-poster, platform-dispatch"
---

# Progress — SPEC-THREADS-POSTER-INSTAGRAM-001

> This file is the §E evidence carrier. Plan-phase emits ONLY the §E.1
> signal and the §E.2–§E.4 placeholder headings. Run-phase (manager-develop)
> populates §E.2/§E.3; sync-phase (manager-docs) populates §E.4. Per the
> Forbidden-modifications matrix in the manager-spec body, this agent does
> NOT populate §E.2–§E.4 content at plan phase.

## §E.1 Plan-phase Audit-Ready Signal

- **Plan-phase artifacts emitted:** `spec.md`, `plan.md`, `acceptance.md`,
  `progress.md` (this file).
- **SPEC ID self-check:** `SPEC-THREADS-POSTER-INSTAGRAM-001` → `PASS`
  (canonical regex `^SPEC(-[A-Z][A-Z0-9]*)+-[0-9]{3}$`).
- **Frontmatter schema:** 12 canonical fields present across all four
  artifacts; `status: draft`; `created`/`updated: 2026-08-05`;
  `tags` comma-separated string; `version: "0.1.0"` quoted.
- **Out of Scope:** `spec.md` §H contains nine `### Out of Scope — <topic>`
  H3 sub-headings with `-` bullets (satisfies the `OutOfScopeRule` lint).
- **GEARS notation:** requirements use Ubiquitous / Capability-gate /
  Event-detected / State-driven patterns; no deprecated `IF/THEN` modality.
- **Scheduling correction:** documented prominently in `spec.md` §B.3
  (REQ-INST-009) — Instagram has NO server-side scheduling; queue is the
  only path.
- **Two LOCKED design decisions:** (1) unified queue + `platform` column;
  (2) Facebook Login auth path. Both reflected in spec.md and plan.md
  without re-litigation.
- **Open questions flagged for user decision (sync-phase, NOT plan-phase
  blockers):** plugin `displayName` broadening ("🧵 스레드 포스터" →
  "소셜 포스터"?) — recorded in `plan.md` Sync-phase; surfaced via
  AskUserQuestion at sync time, not decided unilaterally here.

## §E.2 Run-phase Evidence

_<pending run-phase>_ — populated by manager-develop with verbatim command
output (`uv run pytest -q`, `uv run ruff check`, migration smoke, MCP tool
discovery enumeration, grep evidence for AC-M3-9 / AC-M3-10).

## §E.3 Run-phase Audit-Ready Signal

_<pending run-phase>_ — populated by manager-develop once all P0
acceptance criteria hold with verbatim evidence.

## §E.4 Sync-phase Audit-Ready Signal

_<pending sync-phase>_ — populated by manager-docs after the sync-phase
deliverables (www/content/moai-agents/threads-poster.md Instagram section,
marketplace.json description refresh, displayName decision) are complete.
