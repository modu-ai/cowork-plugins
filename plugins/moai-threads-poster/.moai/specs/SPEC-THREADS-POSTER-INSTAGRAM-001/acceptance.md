---
id: SPEC-THREADS-POSTER-INSTAGRAM-001
title: "Instagram Graph API support for moai-threads-poster — Acceptance Criteria"
version: "0.1.0"
status: draft
created: 2026-08-05
updated: 2026-08-05
author: manager-spec
priority: P1
phase: "v1.1.0 target"
module: "plugins/moai-threads-poster"
lifecycle: spec-anchored
tier: M
tags: "instagram, graph-api, facebook-login, mcp, sqlite-queue, social-poster, platform-dispatch"
---

> **Project-level AC format deviation (declared once at top).** This
> Python/pytest plugin uses BDD **Given/When/Then** as its acceptance-criterion
> format — the native pytest-bdd shape that maps 1:1 to pytest fixtures. The
> GEARS-bearing artifact for this SPEC is `spec.md §B` (requirements, all 24
> REQs GEARS-labeled); acceptance criteria here are BDD scenarios that are
> mechanically testable (each `Then` maps to a pytest assertion). Declaring
> this once at the top avoids rewriting all 33 existing ACs into GEARS "shall"
> form — the substance and testability are unchanged, only the format
> declaration was missing.

# Acceptance Criteria — SPEC-THREADS-POSTER-INSTAGRAM-001

Each criterion is observable and maps to one or more REQ IDs in `spec.md`.
Quality-gate evidence MUST be verbatim command output (per
verification-claim-integrity doctrine) — summarized claims are rejected.

## §D. Acceptance Criteria Matrix

### AC-M1 — Queue platform migration (REQ-INST-011, REQ-INST-012, REQ-INST-013)

**AC-M1-1 — Idempotent column add**
- **Given** a DB file produced by the prior (Threads-only) version (no
  `platform` column),
- **When** the new `Queue(db_path)` constructor opens it,
- **Then** `PRAGMA table_info(posts)` includes a `platform` column with type
  `TEXT` and default `'threads'`, and opening the same DB again does NOT
  raise (the migration is idempotent — the PRAGMA guard prevents a duplicate
  ALTER).

**AC-M1-2 — Back-compat (no data loss)**
- **Given** a pre-migration DB with N existing Threads rows,
- **When** the new `Queue` opens it,
- **Then** all N rows are present, every row has `platform='threads'`, and
  `queue.list()` returns all N rows in the same order as before.

**AC-M1-3 — enqueue platform parameter**
- **Given** a `Queue` instance,
- **When** `queue.enqueue("IMAGE", image_url="...", platform="instagram")`
  is called,
- **Then** the returned row has `platform='instagram'`, and
  `queue.list(platform='instagram')` includes it while
  `queue.list(platform='threads')` does not.

**AC-M1-4 — Unknown platform rejected**
- **Given** a `Queue` instance,
- **When** `queue.enqueue("IMAGE", image_url="...", platform="tiktok")` is
  called,
- **Then** a `ValueError` is raised mentioning the allowed values
  (`threads`, `instagram`).

**AC-M1-5 — Existing queue tests stay green (back-compat at API surface)**
- **Given** the existing `tests/test_queue.py` (unchanged),
- **When** `uv run pytest tests/test_queue.py -q` runs,
- **Then** all existing tests pass — proving `enqueue` / `list` / `due` /
  `approve` / `mark_published` / `mark_failed` retain byte-identical
  behavior when called without the new `platform` parameter.

### AC-M2 — InstagramClient (REQ-INST-001, REQ-INST-003, REQ-INST-004, REQ-INST-005, REQ-INST-006, REQ-INST-007, REQ-INST-008, REQ-INST-021, REQ-INST-024)

**AC-M2-1 — Constructor mirrors ThreadsClient shape**
- **Given** `InstagramClient(access_token="...", ig_user_id="...", client=fake_httpx_client)`,
- **When** constructed,
- **Then** the instance exposes `create_container`, `publish`,
  `get_container_status`, `wait_until_finished`, `get_profile`,
  `refresh_token`, `get_publish_limit`, `comments_list`, `comments_reply`,
  `comments_hide`, `insights`, `close`, `__enter__`, `__exit__` — and does
  NOT close the injected client on `close()`.

**AC-M2-2 — Empty credentials raise ValueError**
- **Given** an empty `access_token` or `ig_user_id`,
- **When** `InstagramClient(...)` is constructed,
- **Then** a `ValueError` is raised (mirroring `ThreadsClient`'s guard).

**AC-M2-3 — Facebook Login host**
- **Given** an `InstagramClient` with the default `base_url`,
- **When** any method makes an HTTP call,
- **Then** the request URL host is `graph.facebook.com` (NOT
  `graph.threads.com`) — asserted via `httpx.MockTransport` handler
  inspecting `req.url.host`.

**AC-M2-4 — 2-stage publish (IMAGE happy path)**
- **Given** a mocked transport that returns `{"id": "container-123"}` for
  `POST /{ig-user-id}/media` and `{"id": "media-456"}` for
  `POST /{ig-user-id}/media_publish`,
- **When** `client.create_container("IMAGE", image_url="https://example.com/x.jpg")`
  then `client.publish("container-123")`,
- **Then** the container-create request hits `POST /{ig-user-id}/media` with
  `media_type=IMAGE` + `image_url=...` + `access_token=...` in params, and
  the publish request hits `POST /{ig-user-id}/media_publish` with
  `creation_id=container-123`.

**AC-M2-5 — JPEG-only enforcement**
- **Given** an `image_url` ending in `.png`,
- **When** `client.create_container("IMAGE", image_url="https://x/y.png")`,
- **Then** a `ValueError` is raised mentioning JPEG-only (the heuristic
  fast-fail per plan.md M2 D5).

**AC-M2-6 — REELS path with share_to_feed**
- **Given** a mocked transport,
- **When** `client.create_container("REELS", video_url="https://x/v.mp4",
  share_to_feed=True)`,
- **Then** the request includes `media_type=REELS`, `video_url=...`, and
  `share_to_feed` in params.

**AC-M2-7 — wait_until_finished polls until FINISHED**
- **Given** a mocked transport that returns `IN_PROGRESS` on the first two
  `GET /{container-id}?fields=status_code` calls and `FINISHED` on the third,
  and a fake sleeper that records sleep calls,
- **When** `client.wait_until_finished("c-1", poll_interval=0, timeout=300,
  sleeper=fake_sleep)`,
- **Then** the method returns `"FINISHED"` after exactly 2 sleep calls.

**AC-M2-8 — wait_until_finished raises on EXPIRED**
- **Given** a mocked transport returning `EXPIRED`,
- **When** `client.wait_until_finished("c-1", ...)`,
- **Then** an `InstagramAPIError` is raised mentioning the EXPIRED status.

**AC-M2-9 — Error class shape**
- **Given** a mocked transport returning HTTP 403 with body
  `{"error": {"message": "perm", "type": "OAuthException", "code": 10}}`,
- **When** any client method is called,
- **Then** the raised `InstagramAPIError` has `.status == 403`,
  `.error_message == "perm"`, `.error_type == "OAuthException"`,
  `.error_code == 10` — mirroring `ThreadsAPIError`'s field set.

**AC-M2-10 — Comments/Insights methods exist; endpoint verification recorded**
- **Given** the `InstagramClient` source,
- **When** inspected,
- **Then** `comments_list`, `comments_reply`, `comments_hide`, `insights`
  methods are present AND each carries an `@MX:TODO` (or equivalent
  inline marker) recording that endpoint paths must be verified against
  current Meta docs at run-phase (per spec.md REQ-INST-018/019 + plan.md
  M2 D7). This criterion does NOT require the endpoints to be live-verified
  at plan time — it requires the verification debt to be RECORDED.

### AC-M3 — MCP tools + runner dispatch (REQ-INST-002, REQ-INST-009, REQ-INST-014, REQ-INST-015, REQ-INST-018, REQ-INST-019, REQ-INST-020, REQ-INST-022, REQ-INST-023)

**AC-M3-1 — All Instagram tools registered**
- **Given** the MCP server is imported,
- **When** the tool registry is enumerated,
- **Then** the following tool names are present:
  `instagram_publish_image`, `instagram_publish_video`,
  `instagram_publish_reel`, `instagram_schedule`,
  `instagram_queue_publish_due`, `instagram_comments_list`,
  `instagram_comments_reply`, `instagram_comments_hide`,
  `instagram_insights`, `instagram_get_profile`,
  `instagram_refresh_token`. (Each tool's docstring documents the
  scheduling correction per REQ-INST-009.)

**AC-M3-2 — Setup-required error (no IG creds)**
- **Given** the MCP server with `IG_ACCESS_TOKEN` / `IG_USER_ID` unset,
- **When** `instagram_get_profile()` is called,
- **Then** it returns a dict with `"error": True`, `"setup_required": True`,
  and a message mentioning `IG_ACCESS_TOKEN` / `IG_USER_ID` — and the server
  does NOT crash.

**AC-M3-3 — instagram_schedule enqueues with platform=instagram**
- **Given** a queue (test DB) and IG credentials set,
- **When** `instagram_schedule(media_type="IMAGE", image_url="https://x/y.jpg",
  scheduled_at="2026-08-10T12:00:00+09:00")` is called,
- **Then** the returned `post_id` resolves to a row with
  `platform='instagram'`, `status='PENDING'`,
  `scheduled_at='2026-08-10T12:00:00+09:00'`.

**AC-M3-4 — instagram_schedule does NOT call the API**
- **Given** a stub `InstagramClient` that records calls,
- **When** `instagram_schedule(...)` is called,
- **Then** the stub's `create_container` / `publish` are NEVER invoked —
  scheduling writes only to the local queue (REQ-INST-009).

**AC-M3-5 — Runner dispatch — mixed queue**
- **Given** a `Queue` with one Threads row (`platform='threads'`,
  `media_type='TEXT'`) and one Instagram row (`platform='instagram'`,
  `media_type='IMAGE'`), both APPROVED and due, and a fake
  `client_resolver` returning a `FakeThreadsClient` for `'threads'` and a
  `FakeInstagramClient` for `'instagram'`,
- **When** `_process(queue, resolver=..., delay=0)` runs,
- **Then** the Threads row's `create_container` is called on the
  `FakeThreadsClient`, the Instagram row's `create_container` is called on
  the `FakeInstagramClient`, both rows reach `PUBLISHED`, and neither fake
  client received a call meant for the other platform.

**AC-M3-6 — Runner dispatch — Threads-only queue back-compat**
- **Given** a `Queue` with only Threads rows (no `platform` column ever
  set explicitly, or all set to `'threads'`),
- **When** `_process` runs with the default resolver,
- **Then** behavior is byte-identical to the pre-change runner (assert:
  same `published`/`failed`/`skipped` counts, same `mark_published` calls).
  This is the load-bearing Threads back-compat test.

**AC-M3-7 — Instagram VIDEO/REELS triggers polling**
- **Given** a due Instagram VIDEO row and a `FakeInstagramClient` whose
  `wait_until_finished` returns immediately,
- **When** `_process` processes the row,
- **Then** `wait_until_finished` was called between `create_container` and
  `publish`.

**AC-M3-8 — Instagram 24h rate-limit guard**
- **Given** a `FakeInstagramClient.get_publish_limit()` returning a dict
  indicating 0 remaining posts,
- **When** `_process` encounters an Instagram row,
- **Then** the row is skipped (not published), the batch stops processing
  further Instagram rows, and the `messages` list records the rate-limit
  skip.

**AC-M3-9 — No server-side scheduling parameter leaked**
- **Given** the full `instagram_api.py` + `server.py` + `runner.py` source,
- **When** grepped for `scheduled_publish_time` or `published=false` or
  `published=False`,
- **Then** zero matches — confirming the scheduling correction is honored
  in code, not just docs (REQ-INST-009).

**AC-M3-10 — Manual-approval model preserved**
- **Given** the full source,
- **When** grepped for `launchd`, `cron`, `LaunchAgents`, `schedule.every`,
  `apscheduler`, `BackgroundScheduler`,
- **Then** zero matches — confirming no background scheduler was
  reintroduced (REQ-INST-022).

**AC-M3-11 — Personal-account error surfaces (non-crashing)**
- **Given** a mocked `InstagramClient.create_container` raising
  `InstagramAPIError(403, {"error": {"message": "...personal account..."}})`,
- **When** `instagram_publish_image(...)` is called,
- **Then** the returned dict has `"error": True` with a message that
  surfaces the API's rejection — the server does not crash, and the
  docstring / setup error text clearly states "Instagram Professional
  (Business or Creator) account required" (REQ-INST-016).

**AC-M3-12 — `instagram_queue_publish_due` processes due Instagram rows**
- **Given** a `Queue` with two Instagram rows — row A
  (`platform='instagram'`, status=APPROVED, `scheduled_at` = now, due) and
  row B (`platform='instagram'`, status=APPROVED, `scheduled_at` = +2h,
  NOT due) — `IG_ACCESS_TOKEN` / `IG_USER_ID` set, and a stub
  `InstagramClient` recording calls,
- **When** `instagram_queue_publish_due(limit=10)` is invoked,
- **Then** row A is processed (stub's `create_container` AND `publish` both
  called; row A reaches `PUBLISHED` via `mark_published`), row B is NOT
  touched (stub received zero calls for row B; row B remains pending with
  no `mark_published` / `mark_failed` call), and the returned `messages`
  list records exactly one published Instagram row. This verifies the
  publish-due flow is the session-driven publishing mechanism per
  REQ-INST-009 / REQ-INST-022 (the queue holds intent; this tool triggers
  actual publication at/after the scheduled time).

### AC-M4 — Skills + config + docs + version (REQ-INST-022, REQ-INST-023)

**AC-M4-1 — Two new skills present**
- **Given** the `plugins/moai-threads-poster/skills/` directory,
- **When** listed,
- **Then** `instagram-post/` and `instagram-comments/` subdirectories exist,
  each containing a `SKILL.md` with valid frontmatter (`name`, `description`,
  `version`) matching the conventions of the existing `threads-post-draft/SKILL.md`.

**AC-M4-2 — `instagram-post` SKILL documents the scheduling correction**
- **Given** the `instagram-post/SKILL.md` body,
- **When** read,
- **Then** it explicitly documents that Instagram has NO server-side
  scheduling and that the queue is the only scheduling path (per spec.md
  §B.3 REQ-INST-009).

**AC-M4-3 — `config/threads.yaml` instagram section**
- **Given** the `config/threads.yaml` file,
- **When** read,
- **Then** an `instagram:` top-level section is present documenting:
  (a) the scheduling correction (prominent), (b) JPEG-only note,
  (c) 24h container EXPIRY non-issue note, (d) `IG_ACCESS_TOKEN` /
  `IG_USER_ID` env-var pointers.

**AC-M4-4 — `.mcp.json` IG env vars**
- **Given** the `.mcp.json` env block,
- **When** read,
- **Then** `IG_ACCESS_TOKEN` and `IG_USER_ID` keys are present using the
  `${VAR}` interpolation pattern (matching the existing Threads keys).

**AC-M4-5 — CONNECTORS.md Instagram section**
- **Given** `mcp-servers/threads-poster/CONNECTORS.md`,
- **When** read,
- **Then** an Instagram Facebook Login for Business section is present and
  documents: Meta App creation, FB Login, long-lived Page access token,
  resolving `IG_USER_ID` via
  `GET /me/accounts?fields=instagram_business_account`, and the PPA note.

**AC-M4-6 — Version bump in lockstep**
- **Given** `plugins/moai-threads-poster/.claude-plugin/plugin.json` and
  the `moai-threads-poster` row in
  `/Users/goos/MoAI/moai-cowork/.claude-plugin/marketplace.json`,
- **When** their `version` fields are compared,
- **Then** both are exactly `"1.1.0"` (sync rule — both bump together from
  `1.0.0`).

**AC-M4-7 — Only this plugin bumps**
- **Given** the marketplace.json `plugins` array,
- **When** other plugin entries' versions are inspected,
- **Then** no other plugin entry changed version (3-axis rule: only the
  modified plugin bumps).

## §D.1 — Edge cases (minimum coverage)

- **EC-1 — PNG image on Instagram:** fast-fail `ValueError` with a clear
  message (AC-M2-5).
- **EC-2 — REELS without video_url:** `ValueError` from
  `create_container` validation.
- **EC-3 — Container stuck IN_PROGRESS for >5 min:**
  `wait_until_finished` raises `InstagramAPIError` on timeout (polling
  budget exhausted).
- **EC-4 — Container EXPIRED:** `wait_until_finished` raises
  `InstagramAPIError` with EXPIRED in the message.
- **EC-5 — Mixed-queue partial failure:** Threads row publishes
  successfully, Instagram row fails — the runner records `failed` for the
  IG row and `published` for the Threads row; one failure does not abort
  the other.
- **EC-6 — Migration on empty DB:** opening an empty (zero-row) DB with
  the new `Queue` adds the `platform` column cleanly; no errors.
- **EC-7 — Migration on a DB already migrated:** opening a DB that already
  has the `platform` column does NOT attempt a second ALTER (PRAGMA guard).
- **EC-8 — Instagram tool called with only Threads creds set:** returns
  `setup_required` (the two credential pairs are independent).

## §D.2 — Severity classification

| Severity | Criteria |
|---|---|
| **Must-pass (P0)** | AC-M1-1, AC-M1-2, AC-M1-5, AC-M2-1..AC-M2-9, AC-M3-1, AC-M3-3, AC-M3-4, AC-M3-5, AC-M3-6, AC-M3-9, AC-M3-10, AC-M4-6 |
| **Should-pass (P1)** | AC-M1-3, AC-M1-4, AC-M2-10, AC-M3-2, AC-M3-7, AC-M3-8, AC-M3-11, AC-M4-1..AC-M4-5, AC-M4-7 |
| **Nice-to-have (P2)** | EC-1..EC-8 (edge-case tests) |

A P0 failure blocks merge. A P1 failure requires an inline justification
and a follow-up issue. P2 failures are tracked but do not block.

## §D.3 — Quality gate (Definition of Done)

ALL of the following must hold with verbatim command output evidence
(`.moai/specs/SPEC-THREADS-POSTER-INSTAGRAM-001/progress.md` §E.2):

1. **Full test suite green.** `uv run pytest -q` exits 0. The baseline
   test count is captured at run-phase start (per verification-claim
   integrity; the mission brief's "existing 134" is treated as a hint,
   not a verified number — the run-phase §E block records the observed
   count before and after).
2. **Lint clean.** `uv run ruff check` exits 0 with no warnings.
3. **Migration smoke.** A demonstration (test or scripted) that opening
   a pre-migration DB fixture migrates cleanly with no data loss (AC-M1-2).
4. **MCP tool discovery.** A scripted enumeration of the MCP tool registry
   lists every Instagram tool named in AC-M3-1.
5. **No scheduling leak.** `grep -rn "scheduled_publish_time\|published=false\|published=False"
   plugins/moai-threads-poster/mcp-servers/threads-poster/src/` returns zero
   matches (AC-M3-9).
6. **No scheduler reintroduction.** `grep -rn "launchd\|cron\|LaunchAgents\|apscheduler\|
   BackgroundScheduler" plugins/moai-threads-poster/` returns zero matches
   (AC-M3-10).
7. **Version sync.** `plugin.json` and `marketplace.json` moai-threads-poster
   row versions are both exactly `"1.1.0"` (AC-M4-6).
8. **Threads back-compat.** `tests/test_threads_api.py`, the Threads-only
   `test_queue.py` scenarios, and `test_runner.py` Threads-only scenarios
   all pass unchanged (AC-M1-5, AC-M3-6).

## §D.4 — Forward-looking (run-phase) verification gates

- The implementer (manager-develop) MUST re-verify the Instagram Graph API
  facts (spec.md §E) against the current official Meta doc before
  implementing M2 endpoints. If any fact has drifted, the implementer
  returns a blocker report; the orchestrator re-delegates a spec.md
  amendment to manager-spec per the D-NEW-1 inline-fix pattern.
- The comments/insights endpoint paths MUST be verified before the
  `@MX:TODO` markers in AC-M2-10 are cleared.

## §D.5 — Indirect verification (where direct tests are insufficient)

- **End-to-end publish against the real Instagram Graph API** is NOT in
  scope for run-phase CI (it requires live credentials and a real
  Professional account). The acceptance strategy is: unit tests with
  mocked transport (AC-M2-*) cover the protocol surface; the first real
  publish is a manual smoke test the user performs after credential setup,
  guided by CONNECTORS.md (M4 D4).
- **Back-compat for in-the-wild user DBs** is verified via a synthesized
  pre-migration DB fixture (AC-M1-2), not by opening a real user DB.

## §D.6 — Closure gates

The SPEC is ready for `draft → in-progress` transition (owned by
manager-develop) when this acceptance.md is signed off by the user at the
Implementation Kickoff Approval gate. The SPEC is ready for
`in-progress → implemented` (owned by manager-docs) when all P0 criteria
hold with verbatim evidence in `progress.md` §E.2.
