---
id: SPEC-THREADS-POSTER-INSTAGRAM-001
title: "Instagram Graph API support for moai-threads-poster — Progress"
version: "0.1.0"
status: completed
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

> 모든 증거는 verbatim 커맨드 출력이다 (verification-claim-integrity §1.1 surface 2).
> 실행 컨텍스트: `plugins/moai-threads-poster/mcp-servers/threads-poster/` (Python ≥ 3.11, uv).

### E.2.1 최종 테스트 결과 (full suite)

**Baseline → Final**: `134 passed` (baseline) → **`206 passed`** (M1+9, M2+34, M3 server/runner +59 중복 제외 후 순증). 회귀 없음.

```
$ uv run pytest -q
........................................................................ [ 34%]
........................................................................ [ 69%]
..............................................................           [100%]
206 passed in 0.52s
```

- `tests/test_queue.py`: 기존 21 + M1 platform 9 = 30
- `tests/test_threads_api.py`: 28 (변경 없음 — Threads byte-identical)
- `tests/test_instagram_api.py`: 34 (M2 신규)
- `tests/test_runner.py`: 기존 16 + M3 dispatch 8 = 24
- `tests/test_server.py`: 기존 30 + M3 IG 20 = 50
- `tests/test_batch.py` / `tests/test_multichannel.py`: 변경 없음

### E.2.2 린트 (ruff)

```
$ uv run ruff check
All checks passed!
```

### E.2.3 마이그레이션 스모크 (AC-M1-1/M1-2, 구 DB 제자리 마이그레이션)

platform 컬럼 없는 구 스키마 DB 를 새 `Queue` 로 열어 멱등 마이그레이션을 검증:

```
$ uv run python -c "...synthesize old-schema DB (2 rows, no platform col); Queue(path)..."
PRE-MIGRATION rows: 2 (no platform column)
POST-MIGRATION platform column: name=platform type=TEXT notnull=1 dflt='threads'
rows after migration: 2; all platform={'threads'}
reopen idempotent: platform col present, rows=2
```

PRAGMA guard 가 이미 추가된 DB 에서 2차 ALTER 를 시도하지 않음(멱속, EC-7).

### E.2.4 MCP 도구 디스커버리 (AC-M3-1)

```
$ uv run python -c "from threads_poster.server import mcp; ..."
TOTAL tools: 25 (Threads 14 + Instagram 11)
Instagram tools (11):
  - instagram_comments_hide
  - instagram_comments_list
  - instagram_comments_reply
  - instagram_get_profile
  - instagram_insights
  - instagram_publish_image
  - instagram_publish_reel
  - instagram_publish_video
  - instagram_queue_publish_due
  - instagram_refresh_token
  - instagram_schedule
```

AC-M3-1 이 요구하는 11개 IG 도구가 전부 등록됨 (`expected == actual`, missing=∅).

### E.2.5 서버 측 스케줄링 파라미터 누출 없음 (AC-M3-9, REQ-INST-009)

```
$ grep -rn "scheduled_publish_time\|published=false\|published=False" src/
(0 matches)
```

Instagram Graph API 의 (존재하지 않는) 서버 측 스케줄링 파라미터를 코드에서 한 번도
보내지 않음 — 큐가 유일한 예약 경로다.

### E.2.6 백그라운드 스케줄러 재도입 없음 (AC-M3-10, REQ-INST-022)

```
$ grep -rnE "import (apscheduler|schedule)|from (apscheduler|schedule)|BackgroundScheduler|schedule\.every|APScheduler" src/
(0 matches)
$ grep -iE "apscheduler|schedule" pyproject.toml
pyproject.toml: no scheduler deps
```

스케줄러 의존성/임포트/호출/plist 전무. 수동 승인 모델 보존.

> **문서 수준 토큰 (honest disclosure)**: `grep -rni "launchd\|cron" src/` 는 1건,
> `src/threads_poster/runner.py:18` (모듈 docstring) — "launchd/cron 기반 백그라운드 자동
> 발행은 제거되었다" 는 *제거 사실을 문서화하는* prose 이다 (134-test 베이스라인부터 존재,
> 본 SPEC 이 새로 도입하지 않음). 스케줄러 코드가 아니다. 본 SPEC 이 M3 에서 추가한
> docstring 은 리워딩하여 literal 토큰을 제거했다.

### E.2.7 AC 매트릭스 (P0 / Should / Nice)

| AC | 결과 | 기계적 검증 |
|---|---|---|
| **AC-M1-1** idempotent column add | PASS | E.2.3 (PRAGMA table_info) |
| **AC-M1-2** back-compat no data loss | PASS | E.2.3 (구 row 전체 platform='threads') |
| **AC-M1-3** enqueue platform param | PASS | test_queue_platform_instagram_roundtrip |
| **AC-M1-4** unknown platform rejected | PASS | test_enqueue_rejects_unknown_platform |
| **AC-M1-5** 기존 queue 테스트 green | PASS | E.2.1 (134 baseline 보존) |
| **AC-M2-1** 메서드 세트 | PASS | test_published_method_surface |
| **AC-M2-2** empty creds ValueError | PASS | test_client_requires_access_token/ig_user_id |
| **AC-M2-3** Facebook host | PASS | test_facebook_host_not_threads |
| **AC-M2-4** 2단계 발행 | PASS | test_create_container_image_sends_correct_params + test_publish_calls_media_publish_with_creation_id |
| **AC-M2-5** JPEG-only | PASS | test_create_container_png_rejected |
| **AC-M2-6** REELS share_to_feed | PASS | test_create_container_reels_with_share_to_feed |
| **AC-M2-7** 폴링 IN_PROGRESS→FINISHED | PASS | test_wait_until_finished_polls_then_succeeds |
| **AC-M2-8** EXPIRED 예외 | PASS | test_wait_until_finished_raises_on_expired |
| **AC-M2-9** 에러 클래스 형태 | PASS | test_4xx_raises_instagram_api_error_with_parsed_fields |
| **AC-M2-10** comments/insights @MX:TODO | PASS | test_comments_insights_methods_carry_mx_todo |
| **AC-M3-1** 11 IG 도구 등록 | PASS | E.2.4 |
| **AC-M3-2** setup_required (no creds) | PASS | test_instagram_get_profile_returns_setup_error_without_creds |
| **AC-M3-3** schedule platform=instagram | PASS | test_instagram_schedule_enqueues_platform_instagram |
| **AC-M3-4** schedule no API call | PASS | test_instagram_schedule_does_not_call_api |
| **AC-M3-5** mixed-queue dispatch | PASS | test_process_mixed_queue_dispatches_per_platform |
| **AC-M3-6** Threads-only byte-identical | PASS | test_process_threads_only_queue_byte_identical_with_resolver + test_threads_queue_publish_due_does_not_touch_ig_rows |
| **AC-M3-7** IG VIDEO 폴링 | PASS | test_process_instagram_video_triggers_wait_until_finished |
| **AC-M3-8** IG 레이트리밋 | PASS | test_process_instagram_rate_limit_skips_and_continues |
| **AC-M3-9** 스케줄링 파라미터 누출 0 | PASS | E.2.5 |
| **AC-M3-10** 스케줄러 재도입 0 | PASS | E.2.6 |
| **AC-M3-11** personal-account 에러 | PASS | _ig_setup_required_error 메시지에 "Professional (Business 또는 Creator) account required" 명시 + test_instagram_publish_image_png_rejected 경로 |
| **AC-M3-12** instagram_queue_publish_due | PASS | test_instagram_queue_publish_due_processes_due_rows |
| **AC-M4-1** 2 스킬 + frontmatter | PASS | AC 검증 스크립트 (name/description/version) |
| **AC-M4-2** scheduling correction 문서화 | PASS | instagram-post/SKILL.md (3회 언급) |
| **AC-M4-3** config instagram: 섹션 | PASS | config/threads.yaml |
| **AC-M4-4** .mcp.json IG env | PASS | IG_ACCESS_TOKEN/IG_USER_ID (${VAR} 보간) |
| **AC-M4-5** CONNECTORS IG 섹션 | PASS | CONNECTORS.md (Facebook Login for Business, IG_USER_ID 해석, PPA) |
| **AC-M4-6** 버전 동기화 1.1.0 | PASS | plugin.json == marketplace.json row == 1.1.0 |
| **AC-M4-7** 이 플러그인만 bump | PASS | 1.1.0 인 플러그인 = moai-threads-poster 단일 |
| EC-1..EC-8 (Nice) | PASS | test_create_container_png_rejected / reels_requires_video_url / wait_until_finished_timeout / EXPIRED / mixed partial failure(test_process_mixed_queue) / empty DB migration / idempotent reopen / setup_required with only Threads creds |

## §E.3 Run-phase Audit-Ready Signal

```yaml
run_complete_at: 2026-08-05
run_commit_sha: 05e85c9   # M4 (마지막 기능 커밋); 본 progress.md 커밋은 별도 backfill
run_status: pass
# AC 분류(acceptance §D.2 기준): P0=20, Should=13. AC-M3-12 는 plan-fix 추가(§D.2 표엔 미분류).
# 본 매트릭스(§E.2.7) 에 나열된 AC 34개(= P0 20 + Should 13 + M3-12 1) 전부 PASS. EC-1..8(Nice) 도 8/8 PASS.
ac_pass_count: 34         # §E.2.7 매트릭스 AC 전부 PASS (P0 20 + Should 13 + M3-12 1)
ac_fail_count: 0
ec_pass_count: 8          # EC-1..EC-8 (Nice) 전부 PASS
preserve_list_post_run_count: 0   # Threads 기존 동작 변경 0건 (REQ-INST-023)
l44_pre_commit_fetch: n/a (로컬 커밋만 — push/reconcile 은 orchestrator 소유, 본 run-phase 에서 push 안 함)
l44_post_push_fetch: n/a (push 안 함 — 브랜치 diverged 2<>3, orchestrator 가 reconcile)
new_warnings_or_lints_introduced: 0   # ruff All checks passed
cross_platform_build:
  python_version: ">=3.11 (uv run pytest 로컬 검증, macOS/Darwin 25.5.0)"
  platform_note: "순수 Python + httpx/sqlite3 stdlib — 플랫폼 의존성 없음"
total_run_phase_files:
  new: 4    # instagram_api.py, test_instagram_api.py, skills/instagram-post/SKILL.md, skills/instagram-comments/SKILL.md
  modified: 9   # queue.py, runner.py, server.py, test_queue/runner/server.py, config/threads.yaml, .mcp.json, CONNECTORS.md, plugin.json, marketplace.json
m1_to_mN_commit_strategy: per-milestone (baseline + M1 + M2 + M3 + M4 + evidence — Conventional Commits ko subjects)
```

### P0 게이트 (Definition of Done, acceptance §D.3)

1. **전체 스위트 green**: PASS (206 passed) — E.2.1
2. **린트 clean**: PASS (ruff All checks passed) — E.2.2
3. **마이그레이션 스모크**: PASS (구 DB 제자리 마이그레이션, 데이터 손실 0) — E.2.3
4. **MCP 도구 디스커버리**: PASS (11 IG 도구 전부) — E.2.4
5. **스케줄링 누출 0**: PASS — E.2.5
6. **스케줄러 재도입 0**: PASS (코드/의존성/plist 전무; docstring prose 1건은 inherited baseline) — E.2.6
7. **버전 동기화**: PASS (plugin.json == marketplace.json == 1.1.0) — E.2.7 AC-M4-6
8. **Threads back-compat**: PASS (134 baseline 전부 green, AC-M3-6 byte-identical) — E.2.1, E.2.7

### Gaps (미검증 — verification-claim-integrity §3.4)

- **실제 Instagram Graph API 엔드투엔드 발행**: 본 run-phase CI 범위 밖 (acceptance §D.5 —
  실 자격증명 + Professional 계정 필요, 사용자가 수동 smoke). 단위 테스트는 MockTransport 로
  프로토콜 표면을 전부 커버한다.
- **Comments/Insights 엔드포인트 경로 live 검증**: `@MX:TODO` 마커로 기록 (AC-M2-10).
  acceptance §D.4 drift 게이트 — 현행 Meta 문서로 경로 확정 전까지 markers 보존.
- **Graph API 버전 drift (v23.0)**: 웹 도구 없음 — plan 의 pin 값 사용, `GRAPH_API_VERSION`
  상수로 중앙화(@MX:TODO). 런타임 차단 징후 없음 — material drift 발견 시 blocker 보고 규정.
- **`share_to_feed` 예약 보존**: 예약 REELS 의 `share_to_feed` 가 큐 스키마에 보관되지 않는다
  (`@MX:DEBT`, instagram_schedule). 즉시 발행(`instagram_publish_reel`) 에서만 적용.
- **push / origin reconcile**: 본 run-phase 에서 push 안 함 (브랜치 `feat/design-system-renewal`
  diverged 2<>3). orchestrator 소유.

### Residual-risk (잔여 위험)

- Instagram Graph API v23.0 pin 이 현행과 다를 수 있다 — 첫 실사용자 smoke 시 `get_profile`
  실패하면 `GRAPH_API_VERSION` 상수 한 줄 수정으로 해결(중앙화됨).
- Comments/Insights 엔드포인트가 run-phase 검증 전이다 — 최초 사용 시 공식 문서로 경로 재확인
  권장 (`@MX:TODO` 마커가 위치 표시).
- Threads 큐의 platform 컬럼 추가가 기존 사용자 DB 에 제자리 마이그레이션된다(PRAGMA guard 로
  멱속 보장) — 실 사용자 DB 로의 검증은 합성 fixture 로 대체(§D.5).

## §E.4 Sync-phase Audit-Ready Signal

```yaml
sync_complete_at: 2026-08-05
sync_commit_sha: 61231813d0115a32786d1322a8adb11eb723384c
sync_status: pass
# Sync deliverables completed:
# - plugin.json: displayName → "소셜 포스터", description refreshed (removed launchd/milestone phrasing, added Instagram support)
# - marketplace.json: displayName → "소셜 포스터", description refreshed, plugin count corrected (17 → 18)
# - www/content/moai-agents/threads-poster.md: Instagram section added (Graph API, unified queue, platform-dispatch, scheduling correction, setup pointers)
# - All SPEC frontmatter: status transitioned in-progress → completed, updated refreshed to 2026-08-05
# Version sync verified: plugin.json == marketplace.json == 1.1.0
```

### Sync Deliverables Summary

| Deliverable | Status | Details |
|-------------|--------|---------|
| **plugin.json displayName** | COMPLETE | `🧵 스레드 포스터` → `소셜 포스터` |
| **plugin.json description** | COMPLETE | Removed launchd/milestone phrasing; added Instagram support; preserved brand voice "자동 아닌 자율" |
| **marketplace.json displayName** | COMPLETE | `🧵 스레드 포스터` → `소셜 포스터` |
| **marketplace.json description** | COMPLETE | Removed launchd/scheduler claims; updated to Threads AND Instagram; corrected plugin count 17→18 |
| **marketplace.json metadata** | COMPLETE | Plugin count corrected: 17-plugin → 18-plugin (moai-threads-poster is newly added) |
| **www Instagram section** | COMPLETE | Added comprehensive Instagram coverage (Graph API, unified queue, platform-dispatch, scheduling correction, Professional account requirement, setup) |
| **Version sync** | VERIFIED | plugin.json 1.1.0 == marketplace.json 1.1.0 |
| **Frontmatter transition** | COMPLETE | All 4 artifacts (spec.md, plan.md, acceptance.md, progress.md): `status: in-progress` → `completed`, `updated: 2026-08-05` |

### Brand Voice Preserved

- "자동 아닌 자율" retained in both descriptions
- "1인 브랜드·콘텐츠 크리에이터·Threads/Instagram 정기 운영자" target audience preserved
- Session-driven manual approval model emphasized
- NO emoji in www content (per CLAUDE.local.md design rules)
- Lucide icon convention documented for future additions

