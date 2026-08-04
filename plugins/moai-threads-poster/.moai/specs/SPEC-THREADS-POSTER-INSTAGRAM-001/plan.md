---
id: SPEC-THREADS-POSTER-INSTAGRAM-001
title: "Instagram Graph API support for moai-threads-poster — Implementation Plan"
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

# Implementation Plan — SPEC-THREADS-POSTER-INSTAGRAM-001

> **Milestone presentation order.** Per the decision-reversibility rule,
> milestones below are ordered with the highest-change-likelihood decisions
> FIRST (data-model → new type interface → user-facing surface → mechanical),
> so human review focuses where it matters. Implementation dependency order
> is noted per milestone; it coincidentally flows M1 → M2 → M3 → M4 → Sync.

## §A. Context

Plugin-local SPEC at
`plugins/moai-threads-poster/.moai/specs/SPEC-THREADS-POSTER-INSTAGRAM-001/`.
All source/config/skills under `plugins/moai-threads-poster/` (the plugin
owns its own `.moai/specs/`). Two design decisions LOCKED upstream (user):
unified queue with `platform` column; Facebook Login auth. See `spec.md` §A.2.

This plan mirrors the existing Threads source patterns EXACTLY — the
implementer (manager-develop, run-phase) MUST read these files before coding:
`threads_api.py`, `queue.py`, `server.py`, `runner.py`,
`tests/test_threads_api.py`, `pyproject.toml`, `config/threads.yaml`,
`.mcp.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
and one existing skill (e.g. `skills/threads-post-draft/SKILL.md`).

## §B. Known Issues & Pre-verified Facts

- **Scheduling correction.** The Instagram Graph API has NO server-side
  scheduling parameter. The queue is the only scheduling path. This is NOT a
  gap to fill — it is documented in `spec.md` §B.3 (REQ-INST-009) and must be
  surfaced in user-facing docs and the `instagram:` config section.
- **Comments/Insights endpoints NOT verified.** This plan states the
  REQUIREMENT (capabilities gated on `manage_comments` / `manage_insights`)
  but does NOT bake endpoint paths. Run-phase MUST verify against current
  Meta docs before implementing those client methods (see M1 §Verification).
- **marketplace.json stale description.** The existing `moai-threads-poster`
  row in `.claude-plugin/marketplace.json` still says "macOS launchd 매일 자동
  발행" (launchd was removed). The sync-phase refreshes this description.
- **Personal-account edge.** The API rejects personal accounts at publish
  time; the plugin surfaces this as a clear error rather than pre-checking
  account type (no cheap pre-check exists).

## §C. Pre-flight (run-phase kickoff checks)

1. `cd plugins/moai-threads-poster/mcp-servers/threads-poster && uv run pytest -q`
   — capture the baseline test count (the mission brief says "existing 134
   tests" but per verification-claim-integrity the implementer MUST re-count
   at run-phase start; the acceptance criterion uses the observed baseline,
   not a number from the plan).
2. `uv run ruff check` — confirm clean baseline.
3. Re-verify Instagram Graph API facts against the official Meta doc (the
   `spec.md` §E facts were verified 2026-06-30; run-phase confirms they have
   not drifted). Specifically re-verify: 2-stage publish paths, JPEG-only
   constraint, REELS params, container status values, rate-limit endpoint.
4. Read `queue.py` line 67-98 (`_migrate`) — confirm the idempotent
   `CREATE TABLE IF NOT EXISTS` pattern and the line-71 comment anticipating
   `ALTER TABLE` column adds.
5. Read `runner.py` `_process` + `_container_call` — design the
   platform-dispatch extension (M3).

## §D. Constraints

- No new dependencies (httpx already present).
- Bilingual Korean+English docstrings; `code_comments: ko`.
- No launchd/cron/auto-publish (manual-approval invariant — REQ-INST-022).
- Threads-existing behavior unchanged byte-identically (REQ-INST-023).
- `ruff check` clean with existing config (no new ruff block).
- Python ≥ 3.11.
- Surgical scope (CLAUDE.md §7 Rule 2 / Rule 5).
- SQLite `ALTER TABLE ADD COLUMN` has no `IF NOT EXISTS` — the migration MUST
  guard via `PRAGMA table_info(posts)`.

## §E. Self-Verification (manager-develop §E mirror)

Run-phase must produce a §E self-verification block with verbatim command
output for at least:

- `uv run pytest -q` (full suite, post-implementation)
- `uv run ruff check`
- `uv run pytest tests/test_instagram_api.py -q` (new client tests)
- `uv run pytest tests/test_queue.py -q` (migration tests including back-compat)
- A migration smoke check on a fixture "old" DB: open pre-migration DB →
  confirm `platform` column present and existing rows have
  `platform='threads'`.
- MCP tool discovery: `uv run python -c "from threads_poster.server import mcp; print(sorted(t.name for t in mcp._tool_manager._tools.values()))"`
  (or equivalent) — confirm all new Instagram tools are registered.

## §F. Milestones

### M1 — Queue platform migration (HIGHEST reversibility risk — schema)

**Why review this first:** a schema migration deployed against existing user
DBs is the hardest decision to reverse. Get the column type, default, and
migration guard right before anything else.

**Goal.** Add `platform TEXT NOT NULL DEFAULT 'threads'` to the `posts`
table via an idempotent migration; thread `platform` through `enqueue` /
`list` / `due`; preserve back-compat.

**Files.**
- `mcp-servers/threads-poster/src/threads_poster/queue.py`
- `mcp-servers/threads-poster/tests/test_queue.py` (new migration tests)

**Key design decisions.**
- **D1 (column & default).** `platform TEXT NOT NULL DEFAULT 'threads'`. The
  default makes existing rows auto-migrate to `platform='threads'` on first
  open — no backfill SQL needed. NOT NULL + default = safe for all
  subsequent inserts.
- **D2 (idempotent guard).** SQLite `ALTER TABLE ADD COLUMN` lacks
  `IF NOT EXISTS`. The migration MUST inspect
  `PRAGMA table_info(posts)` and only emit
  `ALTER TABLE posts ADD COLUMN platform TEXT NOT NULL DEFAULT 'threads'`
  when the `platform` column is absent. This is the canonical SQLite
  idempotent-add pattern.
- **D3 (`enqueue` signature).** Add `platform: str = "threads"` keyword
  parameter. Validate against `_VALID_PLATFORMS = {"threads", "instagram"}`
  (raise `ValueError` on unknown). Default keeps existing Threads callers
  byte-identical.
- **D4 (`list` / `due` filter).** Add optional `platform: Optional[str] = None`
  parameter to both. When provided, filter by `WHERE platform = ?`. When
  `None`, return all platforms (preserves existing behavior for callers that
  don't care).
- **D5 (`mark_published` / `mark_failed` unchanged).** Platform is fixed at
  enqueue time and never changes — no platform parameter on terminal-state
  transitions.
- **D6 (state-machine doc update).** Update the module docstring
  "상태 머신" block to note the `platform` axis. Update the line-71 comment
  to reference the now-implemented ALTER-TABLE migration.

**Back-compat test (load-bearing — implements REQ-INST-012).**
1. Create a DB with the OLD schema (synthesize a fixture SQL or use a
   checked-in `.data/queue.v1.db` fixture).
2. Insert N rows with the old INSERT (no `platform` column).
3. Open with the new `Queue(db_path)` constructor.
4. Assert: `PRAGMA table_info(posts)` now includes `platform`; all N rows
   have `platform='threads'`; row count is N (no loss); `list()` returns
   them; `due()` returns them as before.

**Implementation dependency.** None — M1 can proceed first. M3 (runner
dispatch) depends on M1; M3 (tools) depends on M1.

**Test strategy.**
- New `test_queue_platform_migration.py` (or appended to `test_queue.py`):
  back-compat scenario above; `enqueue(platform='instagram')` round-trip;
  `list(platform='instagram')` filter; `due(platform='threads')` filter;
  `ValueError` on unknown platform.
- Re-run existing `test_queue.py` unchanged → must stay green (proves
  back-compat at the API surface).

**Risks.**
- Existing user DBs in the wild — the migration MUST be truly idempotent
  (the PRAGMA guard is the safety net).
- `due()` platform filter interaction with the `_clock` injection — keep
  the existing clock-injection pattern intact.

---

### M2 — InstagramClient (new type interface)

**Why review this second:** the public method surface of a new client is a
high-churn decision (method names, kwargs, error shape) that downstream code
(M3 tools, skills) depends on.

**Goal.** Build `InstagramClient` in `instagram_api.py` mirroring the
`ThreadsClient` shape but adapted to the Facebook Login host, JPEG-only
images, REELS, and mandatory container-status polling for video/Reels.

**Files.**
- `mcp-servers/threads-poster/src/threads_poster/instagram_api.py` (NEW)
- `mcp-servers/threads-poster/tests/test_instagram_api.py` (NEW)

**Key design decisions.**
- **D1 (class shape — mirror ThreadsClient).** Same constructor pattern:
  `InstagramClient(access_token, ig_user_id, *, base_url=DEFAULT_BASE_URL,
  client=None)`. Same `_owns_client` flag, same `close()` /
  `__enter__` / `__exit__` lifecycle. Same `httpx.Client` injection for tests.
- **D2 (DEFAULT_BASE_URL).** `https://graph.facebook.com/v23.0` (Facebook
  Login for Business host, NOT `graph.threads.com`). Pin to the API version
  verified at M2 run-phase time.
- **D3 (auth convention).** `access_token` as a query/form parameter (NOT a
  Bearer header) — the Facebook Login path uses the same convention as the
  Threads OAuth2 path. This is why the existing `threads_api.py` puts
  `access_token` in `params`, and `InstagramClient` follows suit.
- **D4 (error class).** `InstagramAPIError(RuntimeError)` with identical
  surface to `ThreadsAPIError`: `status`, `body`, `error_message`,
  `error_type`, `error_code`. Body parsed from the standard
  `{"error": {"message", "type", "code"}}` shape. Mirroring enables a shared
  `_error_dict` wrapper in the MCP layer.
- **D5 (validation helpers).**
  - `_validate_media_type(media_type)` — allowed set `{"IMAGE", "VIDEO",
    "REELS"}`. NO `TEXT` (Instagram has no text-only post via this API;
    captions ride on media). NO `CAROUSEL` (out of scope).
  - `_validate_image_jpeg(image_url)` — JPEG-only enforcement. URL suffix
    check is a heuristic; the API is the final authority. Surface a clear
    `ValueError` on `.png` URL suffixes (the most common user mistake given
    Threads allows PNG).
- **D6 (methods — published surface).**
  - `create_container(media_type, *, text=None, image_url=None,
    video_url=None, share_to_feed=None)` → `creation_id: str`.
    Paths: `POST /{ig-user-id}/media`. REELS accepts `share_to_feed`.
  - `publish(creation_id)` → `media_id: str`.
    Path: `POST /{ig-user-id}/media_publish`.
  - `get_container_status(creation_id)` → `str` ∈ {EXPIRED, ERROR,
    FINISHED, IN_PROGRESS, PUBLISHED}.
    Path: `GET /{creation_id}?fields=status_code`.
  - `wait_until_finished(creation_id, *, poll_interval=60.0, timeout=300.0)
    -> str` — polls `get_container_status` ~once/min up to 5 min. Raises
    `InstagramAPIError` on `EXPIRED`/`ERROR`. Returns on `FINISHED`.
    `IN_PROGRESS` keeps polling.
  - `get_profile()` → dict (account health check / who-am-I).
    Path: `GET /{ig-user-id}?fields=username,id,followers_count,media_count`
    (fields to be verified at run-phase).
  - `refresh_token()` — long-lived Page token refresh (path to be verified
    at run-phase; Facebook Page tokens use a different refresh flow than
    Threads `th_refresh_token`).
  - `get_publish_limit()` → dict (24h quota remaining).
    Path: `GET /{ig-user-id}/content_publishing_limit`.
- **D7 (comments + insights methods — REQUIREMENT stated, endpoint deferred).**
  Methods `comments_list(media_id)`, `comments_reply(comment_id, text)`,
  `comments_hide(comment_id)`, `insights(metric, period, ...)` — the method
  NAMES and capability gates are part of this SPEC (REQ-INST-018/019), but
  the endpoint paths MUST be verified at run-phase against current docs
  before implementation. Record a `@MX:TODO` per method until verified.
- **D8 (bilingual docstrings).** Korean+English docstrings matching the
  `threads_api.py` cadence exactly (Korean line, English clarification in
  parens).

**Test strategy (mirror `test_threads_api.py`).**
- `httpx.MockTransport(handler)` + `httpx.Client(transport=...)` injected as
  `client=`. Assert on `req.url.path` + `dict(req.url.params)` — same pattern.
- Cases: create_container IMAGE happy path; IMAGE with `.png` URL →
  `ValueError`; VIDEO creates container; REELS creates with `share_to_feed`;
  `wait_until_finished` returns on first `FINISHED`; `wait_until_finished`
  raises on `EXPIRED`; `wait_until_finished` polls then succeeds on
  `IN_PROGRESS` → `FINISHED`; `publish` returns `media_id`; non-2xx →
  `InstagramAPIError` with parsed fields; empty token/id → `ValueError` in
  constructor; injected client is NOT closed by `close()`.
- Comments/insights methods: unit-test the public surface with mocked
  transport using PLACEHOLDER paths; mark with a clearly labeled
  `@pytest.mark.skip(reason="endpoint path pending run-phase verification")`
  OR test against a documented assumption and revisit at run-phase. Either
  way the test file documents which endpoints are verified vs pending.

**Implementation dependency.** None. M3 (tools) and the runner-dispatch
extension depend on M2.

**No plan-phase clarifications.** Endpoint-verification items are run-phase
tasks recorded in M1 §Verification and the `@MX:TODO` markers, not plan-phase
blockers.

**Risks.**
- JPEG validation by URL suffix is a heuristic — document it as a
  fast-fail convenience, not a substitute for API-level rejection.
- The `wait_until_finished` poller introduces wall-clock time in tests;
  inject a fake sleeper (callable) to keep tests deterministic. Pattern:
  `wait_until_finished(creation_id, *, sleeper=time.sleep, ...)`.

---

### M3 — MCP tools + runner platform dispatch (user-facing surface)

**Why review this third:** the MCP tool NAMES and the dispatch behavior are
user-facing — renaming a tool after release breaks callers.

**Goal.** Add Instagram MCP tools to `server.py`; extend the runner
`_process` loop to dispatch per-platform; add a `_get_ig_client()` singleton.

**Files.**
- `mcp-servers/threads-poster/src/threads_poster/server.py`
- `mcp-servers/threads-poster/src/threads_poster/runner.py`
- `mcp-servers/threads-poster/tests/test_server.py`
- `mcp-servers/threads-poster/tests/test_runner.py`

**Key design decisions.**

#### M3.a — Runner platform dispatch (runner.py)

- **D1 (`_process` gains a client-resolver).** Add an injected
  `client_resolver: Callable[[str, dict], Client]` parameter (where the str
  is the row's `platform` and dict is the row). The resolver returns the
  appropriate client (`ThreadsClient` or `InstagramClient`). Default resolver
  reads env + builds both singletons lazily. This is the minimum-coupling
  design — `_process` stays platform-agnostic.
- **D1.a (call-site migration + creds-absent failure path).** Two explicit
  consequences of the lazy-resolver design that the M3 implementer MUST honor:
  - **(a) `threads_queue_publish_due` call-site migration.** The existing
    `threads_queue_publish_due` MCP tool today passes a single `ThreadsClient`
    directly into `_process`. After the refactor it constructs (or relies on)
    the **default `client_resolver`** instead of passing a raw client.
    Because the resolver builds singletons **lazily**, a Threads-only queue
    NEVER triggers `InstagramClient` construction — `IG_ACCESS_TOKEN` /
    `IG_USER_ID` are never read when no Instagram row is due. This preserves
    byte-identical Threads behavior (REQ-INST-023) and keeps the Threads
    tool's startup footprint unchanged.
  - **(b) Creds-absent failure path for a due Instagram row.** When a due
    row has `platform='instagram'` but `IG_ACCESS_TOKEN` / `IG_USER_ID` are
    absent, the resolver SHALL NOT raise. Instead it **skips** that Instagram
    row, records a `setup_required` message in the batch `messages` list
    (mirroring AC-M3-2's non-crashing `setup_required` pattern), and
    **continues** processing the remaining Threads rows in the same batch.
    The batch does NOT abort; the skipped Instagram row remains in the queue
    for a later run once credentials are provided. The same skip-and-continue
    rule applies when `instagram_queue_publish_due` is invoked without IG
    credentials (every due Instagram row is skipped with one
    `setup_required` message per row; the tool returns normally).
- **D2 (`_container_call` becomes platform-aware).** Today `_container_call`
  maps a row to `ThreadsClient.create_container` kwargs. Extend it to branch
  on `post["platform"]`:
  - `threads` → existing mapping (TEXT/IMAGE/VIDEO), calls
    `ThreadsClient.create_container`.
  - `instagram` → IMAGE/VIDEO/REELS mapping, calls
    `InstagramClient.create_container`. For VIDEO/REELS, call
    `client.wait_until_finished(container_id)` between create and publish.
- **D3 (publish call polymorphism).** Both clients expose
  `publish(creation_id) -> media_id` with the same signature, so the
  `media_id = client.publish(container_id)` line in `_process` works for
  both. The container-creation step is the one that diverges (REELS,
  JPEG-only, polling) — isolated in `_container_call`.
- **D4 (permalink hint).** Threads uses
  `https://www.threads.net/@<username>/post/{media_id}`. Instagram should
  use `https://www.instagram.com/p/{media_id}` (the slug-based URL — final
  form to be confirmed, since IG uses a shortcode, not the raw media_id;
  mark with `@MX:TODO` if the permalink assembly needs the shortcode from
  the publish response).
- **D5 (rate-limit guard).** Threads uses `RATE_LIMIT_24H = 250` and
  `queue.published_in_last_24h()`. Instagram uses 100/24h with a separate
  quota endpoint (`get_publish_limit`). Extend the rate-limit check to be
  platform-aware: for `instagram` rows, consult `get_publish_limit()` (with
  a short cache to avoid hammering the endpoint); for `threads`, keep the
  existing count-based guard.

#### M3.b — MCP tools (server.py)

- **D6 (`_get_ig_client()` singleton).** Mirror `_get_client()` exactly:
  lazy singleton reading `IG_ACCESS_TOKEN` + `IG_USER_ID`; `None` if
  absent; `_reset_ig_client_for_tests()` hook. A separate
  `_ig_setup_required_error()` (or a parameterized factory) emits the
  Instagram setup-required message.
- **D7 (new tools — published names).**
  - `instagram_publish_image(text, image_url)` — immediate publish.
  - `instagram_publish_video(text, video_url)` — immediate publish (with
    polling).
  - `instagram_publish_reel(text, video_url, share_to_feed=True)` — REELS.
  - `instagram_schedule(media_type, text, image_url, video_url,
    scheduled_at, share_to_feed=None)` — enqueue with
    `platform='instagram'`.
  - `instagram_queue_publish_due(limit=10)` — process due Instagram rows.
    (Or extend the existing `threads_queue_publish_due` to dispatch across
    platforms — see D8.)
  - `instagram_comments_list(media_id)` — REQ-INST-018.
  - `instagram_comments_reply(comment_id, text)` — REQ-INST-018.
  - `instagram_comments_hide(comment_id)` — REQ-INST-018.
  - `instagram_insights(...)` — REQ-INST-019.
  - `instagram_get_profile()`.
  - `instagram_refresh_token()`.
- **D8 (unified vs separate publish_due).** Two options:
  (a) keep `threads_queue_publish_due` Threads-only and add a parallel
  `instagram_queue_publish_due`; (b) make `threads_queue_publish_due`
  dispatch across platforms (it iterates `queue.due()` which is now
  platform-tagged) and rename/re-document it as the unified publish-due.
  **Decision (recommended): (a) — parallel tools.** Rationale: surgical
  scope (REQ-INST-023) — keeping `threads_queue_publish_due` Threads-only
  preserves byte-identical Threads behavior; the Instagram tool is additive.
  The unified dispatch lives in the runner (`_process`), shared by both
  tools via the `client_resolver` injection.
- **D9 (error wrapping).** Reuse the existing `_error_dict(exc)` — it works
  generically because `InstagramAPIError` mirrors `ThreadsAPIError` shape
  (both are `RuntimeError` subclasses with `__str__`).

**Test strategy.**
- `test_server.py`: each new Instagram tool has at least one happy-path
  test with a mocked `_get_ig_client()` returning a stub client, plus a
  setup-required test (no env) returning the structured error. Reuse the
  monkeypatch-singleton pattern.
- `test_runner.py`: `_process` with a mixed queue (Threads + Instagram
  rows), inject a fake `client_resolver` returning fake clients, assert
  each row hit the right client's `create_container` + `publish`. Assert
  Instagram VIDEO/REELS rows triggered `wait_until_finished`. Assert the
  Threads-only path still works when the queue has only Threads rows
  (back-compat).

**Implementation dependency.** M3 depends on M1 (queue has `platform`) and
M2 (InstagramClient exists).

**Risks.**
- Tool-name collisions / namespace pollution — the `instagram_*` prefix
  keeps the two surfaces cleanly separated.
- The dispatch path is the one place a Threads regression could slip in —
  the back-compat test (M3 `test_runner.py` Threads-only queue) is the
  safety net.

---

### M4 — Skills + config + docs + version bumps (mechanical)

**Why review this last:** these are mostly mechanical additions and version
bumps; churn risk is low.

**Goal.** Add the 2 Instagram skills, the `instagram:` config section, the
CONNECTORS.md Instagram section, the `.mcp.json` IG env vars, and bump the
plugin version 1.0.0 → 1.1.0 in lockstep with the marketplace entry.

**Files.**
- `plugins/moai-threads-poster/skills/instagram-post/SKILL.md` (NEW)
- `plugins/moai-threads-poster/skills/instagram-comments/SKILL.md` (NEW)
- `plugins/moai-threads-poster/config/threads.yaml` (add `instagram:` section)
- `plugins/moai-threads-poster/mcp-servers/threads-poster/CONNECTORS.md`
  (add Instagram Facebook Login section)
- `plugins/moai-threads-poster/.mcp.json` (add IG env vars)
- `plugins/moai-threads-poster/.claude-plugin/plugin.json` (version 1.1.0)
- `/Users/goos/MoAI/moai-cowork/.claude-plugin/marketplace.json`
  (`moai-threads-poster` row → 1.1.0 + description refresh — sync-phase
  boundary; see Sync)

**Key design decisions.**
- **D1 (skill 1 — `instagram-post`).** Draft + publish/schedule flow.
  Frontmatter matches `threads-post-draft/SKILL.md` conventions (name,
  description with trigger examples, version, responsibility boundary).
  Covers: drafting an Instagram caption, calling `instagram_schedule` /
  `instagram_publish_image` / `instagram_publish_video` /
  `instagram_publish_reel`. Documents the scheduling correction prominently.
- **D2 (skill 2 — `instagram-comments`).** Comment moderation flow: list,
  reply, hide. Documents the `manage_comments` permission gate.
- **D3 (`config/threads.yaml` `instagram:` section).** Documents:
  - cadence note (Instagram peak times differ slightly from Threads; reuse
    the weekly_3/weekly_5 cadences);
  - **the scheduling correction** (no API-native scheduling → queue is the
    only path) — prominent;
  - the 24h container EXPIRY non-issue note;
  - the JPEG-only note;
  - the `IG_ACCESS_TOKEN` / `IG_USER_ID` env-var pointers (mirror the
    existing Threads credential note).
- **D4 (`CONNECTORS.md` Instagram section).** Documents the Facebook Login
  for Business flow: Meta App → FB Login → long-lived Page access token →
  resolve `IG_USER_ID` via `GET /me/accounts?fields=instagram_business_account`
  → complete PPA if prompted. Mirrors the Threads OAuth2 6-step section's
  level of detail.
- **D5 (`.mcp.json`).** Add `"IG_ACCESS_TOKEN": "${IG_ACCESS_TOKEN}"` and
  `"IG_USER_ID": "${IG_USER_ID}"` to the existing `env` block — same `${VAR}`
  interpolation pattern as the Threads vars.
- **D6 (version bump — 3-axis rule).** Per CLAUDE.local.md versioning:
  - `plugins/moai-threads-poster/.claude-plugin/plugin.json`: `1.0.0` →
    `1.1.0` (MINOR = feature add).
  - `.claude-plugin/marketplace.json` `moai-threads-poster` row: `1.0.0` →
    `1.1.0` IN LOCKSTEP (the sync rule — these two MUST match).
  - ONLY this plugin bumps. The other 16 plugins and the moai-cowork
    version are untouched.

**Test strategy.**
- No unit tests for skills/config/docs (declarative content).
- Manual smoke: start the MCP server with `IG_ACCESS_TOKEN`/`IG_USER_ID`
  unset, confirm `instagram_*` tools return `setup_required`; with both
  set (test fixture), confirm `instagram_get_profile` calls the API.
- Plugin metadata: assert `plugin.json` version == `marketplace.json`
  moai-threads-poster row version (1.1.0 == 1.1.0) — a one-line CI-grade
  check or a manual grep.

**Implementation dependency.** M4 depends on M3 (tools exist for skills to
call) and M1 (queue has `platform` for the scheduling flow).

**Risks.**
- Version-sync drift between `plugin.json` and `marketplace.json` — the
  most common versioning mistake per CLAUDE.local.md. The acceptance
  criterion makes this explicit.

---

### Sync-phase (separate later phase — `/harness:www-docs`)

**Note:** the sync-phase is NOT part of the run-phase M1-M4 delivery. It is
recorded here for handoff; it executes after the run-phase PR merges.

**Scope.**
- `www/content/moai-agents/threads-poster.md` — add an Instagram section
  and update the MCP tool table (route via `/harness:www-docs`, not this
  SPEC).
- `.claude-plugin/marketplace.json` `metadata.description` — refresh the
  stale "17-plugin" string (now reflects the IG-enabled plugin count) and
  remove the "macOS launchd 매일 자동 발행" stale claim (launchd was
  removed in a prior release).
- **OPEN QUESTION for user decision (do NOT decide unilaterally):** the
  plugin `displayName` is currently "🧵 스레드 포스터" ("Threads Poster").
  With Instagram support, should it broaden to e.g. "소셜 포스터" ("Social
  Poster")? This is a user-facing branding decision — surface via
  `AskUserQuestion` in the sync phase, do NOT decide in this plan.

## §G. Anti-Patterns (do NOT)

- **AP-1: Server-side scheduling parameter.** Do NOT add
  `scheduled_publish_time` / `published=false` to any Instagram API call —
  the API does not support it (REQ-INST-009). The queue is the only path.
- **AP-2: `IF EXISTS` on SQLite ALTER.** Do NOT assume SQLite supports
  `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` — it does NOT. Use the PRAGMA
  guard.
- **AP-3: Single shared client.** Do NOT merge Threads and Instagram into
  one client class. Two distinct hosts, two distinct auth flows, two
  distinct media-type sets (Threads allows PNG, IG does not; IG has REELS,
  Threads does not). Keep them separate; the dispatch layer is the join.
- **AP-4: Threads behavior drift.** Do NOT "improve" Threads code while
  adding Instagram. Surgical scope (REQ-INST-023).
- **AP-5: Asserting IG comment/insight endpoint paths as fact.** Do NOT
  hardcode `/insights` or `/{media-id}/comments` paths without run-phase
  verification (M1 §Verification, M2 D7).
- **AP-6: launchd/cron reintroduction.** Do NOT add any background
  scheduler (REQ-INST-022).
- **AP-7: Version-bump only one file.** Do NOT bump `plugin.json` without
  the matching `marketplace.json` bump (CLAUDE.local.md sync rule).
- **AP-8: Pre-checking personal-account type.** Do NOT add a startup
  account-type probe — surface the API's publish-time rejection as a clear
  error instead (REQ-INST-016).

## §H. Cross-References

- `spec.md` (this SPEC) — requirements, scheduling correction, verified IG
  facts, exclusions.
- `acceptance.md` (this SPEC) — per-milestone Given-When-Then + quality gates.
- `progress.md` (this SPEC) — §E skeleton (run-phase evidence goes there).
- Existing source patterns (read before implementing):
  `threads_api.py`, `queue.py`, `server.py`, `runner.py`,
  `tests/test_threads_api.py`.
- CLAUDE.local.md "디자인 시스템 규칙" — N/A for this SPEC (no www CSS
  changes in run-phase; the sync-phase www-docs update routes through
  `/harness:www-docs`).
- CLAUDE.local.md "버저닝 규칙" — 3-axis versioning; M4 D6 applies the
  plugin-axis bump.
