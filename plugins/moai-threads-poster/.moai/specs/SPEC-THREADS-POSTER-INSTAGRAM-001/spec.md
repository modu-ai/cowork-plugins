---
id: SPEC-THREADS-POSTER-INSTAGRAM-001
title: "Instagram Graph API support for moai-threads-poster (Option A — Threads + Instagram integrated social poster)"
version: "0.1.0"
status: completed
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

# SPEC-THREADS-POSTER-INSTAGRAM-001 — Instagram Graph API support

## §A. Overview

### A.1 Problem

`moai-threads-poster` currently publishes only to Threads (Meta). The user
operates an Instagram presence alongside Threads and wants one plugin that
orchestrates both surfaces from a unified approval queue, sharing the existing
manual-approval cadence, SQLite queue, and bilingual skill ecosystem.

### A.2 Solution (Option A — integrated, NOT a separate plugin)

Extend the existing `moai-threads-poster` plugin to also drive the Instagram
Graph API. Two architectural commitments are LOCKED by the user and not
re-litigated in this SPEC:

1. **Unified approval queue + `platform` field.** Instagram scheduling reuses
   the existing SQLite queue (`queue.py`). A new `platform` column discriminates
   Threads vs Instagram rows. `instagram_schedule` enqueues with
   `platform='instagram'`; the runner dispatches to the right API client per
   row.
2. **Facebook Login auth path for Instagram.** Instagram Graph API uses
   `graph.facebook.com` with a Facebook Page access token (NOT the Threads
   OAuth2 flow). Credentials arrive via `IG_ACCESS_TOKEN` + `IG_USER_ID` env
   vars, distinct from the Threads pair.

### A.3 Why Option A (integrated) over a separate `moai-instagram-poster` plugin

- One approval queue, one cadence, one bilingual skill ecosystem.
- Threads and Instagram share the same 2-stage publish model (create container
  → publish) and near-identical client shapes — code reuse is high.
- The manual-approval model (no launchd/cron, no auto-publish) is identical and
  must NOT drift between two plugins.

## §B. Requirements (GEARS notation)

> Subject is generalized per GEARS (`<subject>` = the named component), not
> hardcoded to "the system". Each REQ is independently testable.

### B.1 Credentials & auth path

**REQ-INST-001 (Ubiquitous).** The `moai-threads-poster` plugin shall accept
`IG_ACCESS_TOKEN` and `IG_USER_ID` environment variables as the Instagram
Graph API credentials, distinct from the Threads credentials
(`THREADS_ACCESS_TOKEN` / `THREADS_USER_ID`).

**REQ-INST-002 (Capability gate).** Where the Instagram credentials are
absent, the Instagram MCP tools shall return a structured `setup_required`
error dict (mirroring `_setup_required_error`) WITHOUT crashing the MCP server.

**REQ-INST-003 (Ubiquitous).** The `InstagramClient` shall use
`https://graph.facebook.com/v23.0` (Facebook Login for Business host) as its
default base URL, distinct from the Threads `graph.threads.com` host. The v23.0
version is pinned per the 2026-06-30 Meta docs verification recorded in §E and
is re-verified at run-phase per `acceptance.md` §D.4 (live-version verification
is a run-phase task; the pinned version is NOT changed here).

### B.2 Publishing model

**REQ-INST-004 (Ubiquitous).** The `InstagramClient` shall publish images and
videos via the 2-stage container→publish flow:
- Stage 1: `POST /{ig-user-id}/media` → returns `creation_id` (container).
- Stage 2: `POST /{ig-user-id}/media_publish` with `creation_id` → returns
  `media_id` (published post).

This mirrors the Threads 2-stage pattern (`create_container` → `publish`).

**REQ-INST-005 (Event-detected).** When `media_type=IMAGE` is submitted, the
`InstagramClient` shall accept JPEG only and reject PNG with a clear
`ValueError` — Instagram differs from Threads (which allows JPEG/PNG).

**REQ-INST-006 (Event-detected).** When `media_type=REELS` is submitted, the
`InstagramClient` shall create the container with `media_type=REELS` +
`video_url` and the optional `share_to_feed` flag, then poll the container
status before publishing.

**REQ-INST-007 (Event-detected).** When `media_type=VIDEO` or `media_type=REELS`
is created, the `InstagramClient` shall poll
`GET /{container-id}?fields=status_code` approximately once per minute for up
to 5 minutes until the status is `FINISHED` before calling `media_publish`.
The poller shall surface `EXPIRED` / `ERROR` as `InstagramAPIError` and retry
`IN_PROGRESS`.

**REQ-INST-008 (Ubiquitous).** The `InstagramClient` shall require media URLs
(`image_url` / `video_url`) to be publicly reachable — Meta fetches (cURLs)
the media server-side. Private/signed URLs shall be rejected with a clear
error before the API call where detectable.

### B.3 Scheduling — THE CORRECTION (prominent)

> **This requirement corrects the user's initial premise.** The premise was
> that Instagram, like some other social APIs, exposes a server-side
> scheduling parameter. **It does NOT.** The Instagram Graph API offers no
> `scheduled_publish_time` parameter and no `published=false + timestamp`
> mode. Scheduling is therefore purely client-side.

**REQ-INST-009 (Ubiquitous — scheduling correction).** The plugin shall NOT
send any server-side scheduling parameter to the Instagram Graph API. The
unified SQLite queue is the ONLY scheduling path: a scheduled Instagram post
holds *intent* (caption + media_url + scheduled time) in the queue; at the
scheduled time the runner creates the container and immediately publishes
(container lifetime is seconds, so the 24h container EXPIRY is a non-issue).

**REQ-INST-010 (Ubiquitous — 24h container EXPIRY, documented as non-issue).**
The plugin shall document that container `EXPIRED` (24h) is only relevant
when a container is held; because the queue holds *intent* (not containers)
and the runner creates+publishes within seconds at the scheduled time, the
24h EXPIRY does not affect this design.

### B.4 Unified queue + platform dispatch

**REQ-INST-011 (Ubiquitous — schema migration).** The unified SQLite queue
(`queue.py`) shall add a `platform TEXT NOT NULL DEFAULT 'threads'` column
to the `posts` table via an idempotent migration. Because SQLite
`ALTER TABLE ADD COLUMN` has no `IF NOT EXISTS`, the migration shall inspect
`PRAGMA table_info(posts)` and only add the column when absent.

**REQ-INST-012 (Ubiquitous — back-compat invariant).** Opening an existing
DB file produced by the prior (Threads-only) version shall migrate in place:
the `platform` column appears, all pre-existing rows have `platform='threads'`,
and no row is lost or altered except for the new column default.

**REQ-INST-013 (Capability gate).** The `Queue.enqueue` method shall accept
an optional `platform` parameter (default `'threads'`). The `Queue.list` and
`Queue.due` methods shall accept an optional `platform` filter.

**REQ-INST-014 (Ubiquitous — runner dispatch).** The runner `_process` loop
(`runner.py`) shall resolve the platform-appropriate client per due post:
`ThreadsClient` for `platform='threads'`, `InstagramClient` for
`platform='instagram'`. A single `_process` invocation shall handle a mixed
queue (Threads + Instagram rows in the same batch).

**REQ-INST-015 (Ubiquitous — publish flow mapping).** The runner's
`_container_call` helper (or its platform-aware successor) shall map each
post's `media_type` to the correct client kwargs for BOTH platforms, with
Instagram REELS routed through the REELS+polling path and Threads REELS
remaining Threads-scoped (Threads has no REELS — Instagram-only concept).

### B.5 Account-type constraint

**REQ-INST-016 (State-driven).** While a personal Instagram account is
connected (the API returns an error indicating personal-account scope), the
plugin shall reject publishing and surface a clear error: "Instagram
Professional (Business or Creator) account required — the Graph API does not
support personal accounts."

**REQ-INST-017 (Event-detected).** When the connected Instagram account is a
Professional account but has not completed Page Publishing Authorization (PPA),
the plugin shall surface a clear `setup_required`-style error directing the
user to complete PPA in Meta Business Suite before retrying.

### B.6 Comments & Insights (requirement stated; endpoint verification deferred)

**REQ-INST-018 (Capability gate — comments).** Where the user has granted the
`manage_comments` permission, the plugin shall expose comment moderation MCP
tools: `instagram_comments_list` (list comments on a media object),
`instagram_comments_reply` (reply to a comment), and
`instagram_comments_hide` (hide a comment).

**REQ-INST-019 (Capability gate — insights).** Where the user has granted the
`manage_insights` permission, the plugin shall expose insights MCP tools:
`instagram_insights` returning account-level and media-level insights.

> **Endpoint verification deferred to run-phase.** This SPEC states the
> REQUIREMENT (the user-facing capability and permission gating) but does
> NOT assert exact endpoint paths (e.g. `/{ig-media-id}/comments`,
> `/insights`) as fact. Run-phase (manager-develop) MUST verify the current
> endpoint paths and parameter names against the official Meta "Instagram
> Graph API Reference" before implementation. The plan.md M1 milestone
> records this as a run-phase verification task.

### B.7 Rate limit & profile

**REQ-INST-020 (Event-detected).** When the Instagram 24h publish count
approaches the limit (100 posts/24h; 50 on `media_publish`), the plugin shall
surface remaining quota via `GET /{ig-user-id}/content_publishing_limit` and
the runner shall stop the batch when the limit is reached (skipping remaining
rows), mirroring the Threads 24h-limit guard.

**REQ-INST-021 (Ubiquitous).** The `InstagramClient` shall expose
`get_profile` (account health check / who-am-I) and `refresh_token` (long-lived
Page token refresh) methods mirroring the Threads client surface, so the MCP
layer can offer symmetric profile/refresh tools.

### B.8 Manual-approval model preserved

**REQ-INST-022 (Ubiquitous — preserved invariant).** The plugin shall preserve
the manual-approval publishing model: NO launchd, NO cron, NO auto-publish.
Instagram scheduling means the queue holds intent; actual publishing happens
via the session-driven `instagram_queue_publish_due` MCP tool (or the unified
`threads_queue_publish_due` tool when it dispatches across platforms) invoked
by the user at/after the scheduled time.

**REQ-INST-023 (Ubiquitous — surgical scope).** The plugin shall NOT modify
Threads-existing behavior. Existing Threads rows, Threads tools, Threads
tests, and Threads skills continue to work byte-identically after the
migration (the only Threads-side change is the additive `platform` column
defaulting to `'threads'`).

### B.9 Error model

**REQ-INST-024 (Ubiquitous).** The `InstagramClient` shall raise
`InstagramAPIError(RuntimeError)` with `status` / `error_message` /
`error_type` / `error_code` fields parsed from the response body, mirroring
the `ThreadsAPIError` shape so the MCP `_error_dict` wrapper works
generically.

## §C. User stories

- **US-1 (Solo creator, dual platform).** "I post to Threads AND Instagram.
  I want one approval queue: I draft a caption + image once, pick the platform,
  approve, and the runner publishes to the right surface."
- **US-2 (Scheduling).** "I want to schedule an Instagram Reel for Wednesday
  12:00 Seoul. At 12:00 I open my session, hit publish-due, and it goes out —
  no background daemon, no surprise auto-publish."
- **US-3 (Moderation).** "After publishing, I want to list comments on my
  Instagram post, reply to one, and hide a spam comment — all from the same
  MCP server."
- **US-4 (Insights).** "I want to pull reach/impressions for my last Instagram
  post to decide whether to boost it."
- **US-5 (Back-compat).** "I have 6 months of Threads posts in my queue DB. I
  upgrade to the Instagram-enabled version. All my Threads rows still work and
  the queue UI now shows a `platform` field."

## §D. Permissions, env vars, account type

### D.1 Required Facebook Login permissions

- `instagram_basic` (required baseline)
- `instagram_content_publish` (required for publishing)
- `pages_read_engagement` (required for publishing)
- `manage_comments` (required for comment moderation tools — REQ-INST-018)
- `manage_insights` (required for insights tools — REQ-INST-019)
- `pages_show_list` (required for Page resolution during setup)

### D.2 Environment variables

| Variable | Purpose | Required |
|---|---|---|
| `IG_ACCESS_TOKEN` | Facebook Page access token (long-lived) for Instagram Graph API | yes (for IG tools) |
| `IG_USER_ID` | Instagram Professional account ID (the `ig-user-id` in API paths) | yes (for IG tools) |

These augment (do not replace) the existing Threads env vars.

### D.3 Account type

**Instagram Professional (Business OR Creator) account ONLY.** Personal
accounts cannot use the Graph API — stated explicitly in tool docstrings,
the `setup_required` error, and CONNECTORS.md.

### D.4 PPA (Page Publishing Authorization)

May be required by Meta after permission grant. If publishing fails with a
PPA indicator, surface a clear setup-required error directing the user to
complete PPA in Meta Business Suite.

## §E. Verified Instagram Graph API facts (baked in; do NOT diverge)

Source: official Meta "Content Publishing" documentation, verified
2026-06-30 update. These are FACTS baked into this SPEC; implementers MUST
NOT assert any endpoint or parameter not listed here as fact without
re-verification.

1. **2-stage publish.** `POST /{ig-user-id}/media` (create container) →
   `POST /{ig-user-id}/media_publish` with `creation_id`. Same shape as Threads.
2. **Reels.** `media_type=REELS` + `video_url` (+ optional `share_to_feed`).
3. **Images: JPEG only.** NOT PNG — differs from Threads.
4. **Public media URLs.** Meta fetches `image_url`/`video_url` server-side;
   both must be public.
5. **Account: Professional only** (Business OR Creator). Personal unsupported.
6. **Rate limit.** 100 posts/24h; 50 on the `media_publish` endpoint. Check
   via `GET /{ig-user-id}/content_publishing_limit`.
7. **Container status.** `GET /{container-id}?fields=status_code` →
   `EXPIRED` / `ERROR` / `FINISHED` / `IN_PROGRESS` / `PUBLISHED`. Video/Reel
   publishing MUST poll (~once/min, ≤5 min) until `FINISHED`.
8. **NO server-side scheduling parameter.** No `scheduled_publish_time`; no
   `published=false + timestamp`. Scheduling is purely client-side. (See
   §B.3 REQ-INST-009 — this corrects the initial premise.)
9. **Container 24h expiry.** `EXPIRED` after 24h. Only relevant if a container
   is held; this design holds intent in the queue (not containers), so it is
   a non-issue (REQ-INST-010).
10. **PPA may be required.** Page Publishing Authorization can block
    publishing until completed.
11. **Comments** (permission `manage_comments`) and **Insights** (permission
    `manage_insights`): the REQUIREMENT is stated in this SPEC
    (REQ-INST-018 / REQ-INST-019). Exact endpoint paths are NOT asserted as
    fact — run-phase must verify against current docs.

## §F. Non-functional constraints

- **No new dependencies.** `httpx` already present; no new PyPI packages.
- **Bilingual Korean+English docstrings** (per existing code style; see
  `threads_api.py`).
- **Code comments in Korean** per `.moai/config/sections/language.yaml`
  `code_comments: ko`.
- **Lint clean.** `ruff check` clean with the project's existing ruff config
  (no new ruff config block).
- **Test coverage.** New modules ≥ 85% coverage (per project default).
- **Surgical scope.** Threads-existing behavior unchanged byte-identically
  (REQ-INST-023).
- **Python ≥ 3.11** (per existing `pyproject.toml`).

## §G. References

- Official Meta "Instagram Graph API — Content Publishing" doc (verified
  2026-06-30). Run-phase: re-verify before implementation.
- Existing source files mirrored by this SPEC:
  - `mcp-servers/threads-poster/src/threads_poster/threads_api.py` (261L) —
    `ThreadsClient` / `ThreadsAPIError` pattern to mirror as
    `InstagramClient` / `InstagramAPIError`.
  - `queue.py` (309L) — `posts` schema + idempotent migration pattern; line 71
    comment already anticipates column-add via ALTER TABLE.
  - `server.py` (981L) — FastMCP tool registration + singleton
    `_get_client()` + `_setup_required_error` + `_error_dict` patterns.
  - `runner.py` (299L) — `_process` loop + `RATE_LIMIT_24H` guard; becomes
    platform-aware per REQ-INST-014.
- Versioning rule: `plugins/moai-threads-poster/.claude-plugin/plugin.json`
  1.0.0 → **1.1.0** (MINOR = feature add), in lockstep with the
  `.claude-plugin/marketplace.json` `moai-threads-poster` row (CLAUDE.local.md
  3-axis versioning rule).

## §H. Exclusions (Out of Scope)

### Out of Scope — Threads behavior changes

- This SPEC does NOT modify Threads-existing behavior. The Threads client,
  Threads tools, Threads tests, and Threads skills remain byte-identical
  except for the additive `platform` column defaulting to `'threads'`.
- No Threads bug fixes, refactors, or "while I'm here" cleanups.

### Out of Scope — Carousel / multi-item posts

- Instagram Carousel publishing (`children` / multiple `creation_id`s in one
  container) is out of scope. Single-image, single-video, and single-Reel
  publishing only. (Threads CAROUSEL is likewise already out of scope in the
  current Threads client.)

### Out of Scope — Stories, Live, Shopping tags

- Instagram Stories publishing, Instagram Live, product tagging in shop
  posts — none are exposed by this SPEC.

### Out of Scope — Automated/background publishing

- launchd/cron/daemon-based auto-publish is explicitly excluded
  (REQ-INST-022). The manual-approval model is preserved; the user must
  invoke the session-driven publish-due tool.

### Out of Scope — Server-side scheduling

- Server-side scheduling parameters are out of scope BECAUSE THEY DO NOT
  EXIST in the Instagram Graph API (REQ-INST-009). Any future Meta API
  change that introduces server-side scheduling would require a separate
  follow-up SPEC.

### Out of Scope — Container 24h EXPIRY handling

- Container `EXPIRED` recovery is out of scope: the queue holds intent, not
  containers (REQ-INST-010). Containers live seconds in this design.

### Out of Scope — Personal-account support

- Personal Instagram account support is out of scope — the API does not
  support it (REQ-INST-016). No fallback path for personal accounts.

### Out of Scope — Cross-posting orchestration

- "Post the same content to Threads AND Instagram in one action" (smart
  cross-posting) is out of scope. Each post row targets ONE platform. A
  future SPEC may add a cross-post orchestrator that enqueues two rows.

### Out of Scope — Web UI / dashboard

- No web UI, no dashboard, no status page. The MCP tools and skills remain
  the only surface.

### Out of Scope — moai-cowork-level SPEC migration

- This SPEC is plugin-local (`plugins/moai-threads-poster/.moai/specs/`).
  Migrating it to the cowork-level `.moai/specs/` is out of scope and would
  require a separate conventions decision.

---

## HISTORY

- **2026-08-05** — SPEC created (v0.1.0, status: draft). Two design decisions
  (unified queue + `platform` field; Facebook Login auth path) LOCKED by the
  user before plan-phase. Instagram Graph API facts verified against official
  Meta "Content Publishing" doc (2026-06-30 update). Scheduling correction
  documented (Instagram has NO server-side scheduling → queue is the only
  path). Comments/Insights endpoint paths deferred to run-phase verification.
