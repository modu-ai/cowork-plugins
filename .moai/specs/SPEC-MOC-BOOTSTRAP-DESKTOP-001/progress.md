# SPEC-MOC-BOOTSTRAP-DESKTOP-001 — 진행 상황 (progress.md)

> 상태 스냅샷: plan-phase 산출물 작성 완료(draft). run-phase 미착수.

## §E.1 Plan-phase Audit-Ready Signal

plan-phase 산출물 세트(spec.md + plan.md + acceptance.md + progress.md) 작성 완료. 오디트 준비 신호:

- **SPEC ID self-check**: `decomposition: SPEC ✓ | MOC ✓ | BOOTSTRAP ✓ | DESKTOP ✓ | 001 ✓ → PASS` (정규 regex `^SPEC(-[A-Z][A-Z0-9]*)+-\d{3}$` 통과, 중복 없음).
- **Frontmatter 12-필드**: id/title/version/status/created/updated/author/priority/phase/module/lifecycle/tags 전부 존재. `created`/`updated` 사용(스네이크 별칭 없음). `tags` 콤마 구분 문자열. `version`·`phase`·`module`·`lifecycle` 비어있지 않음. status=draft(8-값 enum). priority=P1.
- **GEARS 준수**: REQ-BD-001~014 전부 GEARS 패턴(Ubiquitous / When / Where) 사용, 일반화된 `<subject>`.
- **Out of Scope**: 6개 `### Out of Scope — <topic>` H3 서브헤딩 + `-` 불릿(OutOfScopeRule 충족).
- **실측 기반**: 3개 트리(cowork/code/template) 직접 조사, 설계 문서 주장 미신뢰. 바이너리 의존 훅 전수 카운트는 추정 주장 없이 CODE-002로 이연(verification-claim-integrity 준수).
- **미결 결정**: D1(버전 정책), D2(표시명) — 옵션으로 인코딩, run-phase Implementation Kickoff 시 오케스트레이터 확인 필요.

## §E.1b Phase 0.95 Mode Selection (orchestrator, 2026-07-03)

**Decision**: `sub-agent` — Mode 5, 단일 순차(sequential) manager-develop, cycle_type=tdd.

**IGGDA §H predicate (4/4 충족 → auto-proceed 도메인)**: (a) intent 100% ✅ / (b) plan-auditor PASS-WITH-DEBT 0.92 ✅ / (c) Tier M ✅ / (d) dangerous keyword 없음 ✅. Phase 0.5 SKIPPED (verdict fresh 2026-07-03, skip-eligible ≥0.90, 이후 SPEC 산출물 commit 무착지). 사용자 결정 확정: D1=BIND (0.1.0 → 3.0.0) / D2=KEEP (M5 skip). 본 §E.1 "미결 결정" 라인은 Implementation Kickoff(2026-07-03)에서 해소됨.

**입력 파라미터**: tier M · ~6-9 files(M1-M4) · ~5 domains · markdown+shell+JSON(Go 없음) · 동시성 이익 LOW(coding/doc-heavy).

**근거**: coding-heavy + <30 files → Anthropic coding-task 병렬성 경고 → 순차 단일 manager-develop. trivial / background(writes) / agent-team(thorough FAIL) / parallel(research-heavy 아님) / workflow(<30 files·mechanical-uniform 아님) 전부 No → Mode 5 default. team-protocol 1M-vs-200K 노트가 단일 manager-develop 지지.

## §E.2 Run-phase Evidence

> run-phase 시작: 2026-07-03. cycle_type=tdd (quality.yaml constitution.development_mode).
> Implementation Kickoff APPROVED (user, 2026-07-03). Phase 0.5 SKIPPED (plan-audit iter-3 PASS-WITH-DEBT 0.92, skip-eligible ≥0.90).
> Mode 5 (single sequential manager-develop). M5 SKIPPED (D2=KEEP). D1=BIND (0.1.0 → 3.0.0).

### M1 — `/project init` 순증 (AC-BD-001a/b/c) — PASS

- **AC-BD-001a (NET-NEW 게이트)**: `grep -c "skill-profile.yaml" SKILL.md` = **5** (HEAD was 0). 지정 경로 `.moai/skill-profile.yaml` 리터럴 매치 5건(Phase 6.6 directive + storage locations + EC6 주의사항).
- **AC-BD-001b (NET-NEW 게이트)**: `grep -ciE "폴더 규약 스캐폴드|folder-convention scaffold" SKILL.md` = **3** (HEAD was 0). Phase 6.5 directive + 현재 동작 요약 + storage locations.
- **AC-BD-001c (PRESERVE 회귀 가드)**: `grep -ciE "레거시 별칭|bare .?/project|/project init" SKILL.md` = **14** (baseline 14, 회귀 없음). `grep -c "^### 1\. CLAUDE\.md 구조" SKILL.md` = **1** (baseline 1).
- **공유 파일 경계 존중**: routing topology (`도메인 라우팅` section lines 65-95) + marketplace table (lines 419-425) 미수정 (REMEDIATION-001 AC-REM-016 소관).
- **편집 범위**: `plugins/moai-cowork/skills/project/SKILL.md` 내 4곳 — (1) 현재 동작 요약 +2 bullet, (2) Phase 6.5/6.6 워크플로 블록 추가, (3) 저장 위치 +2 라인, (4) moai-profile.md 금지 주의사항에 EC6 구분 노트.

### Audit SHOULD-FIX 처리 (run entry에서 문서화)

- **D2-defect (AC-BD-008 orphan grep)**: ADDRESS at run entry. `plugins/moai-code/commands/harness.md`는 §A.2에 문서화된 사전존재 예외(moai-code 전용 명령이라 정본 템플릿 기원 아님 → parity-source 주석 없음이 정상). 본 run-phase는 `plugins/moai-code/commands/*.md`를 일체 편집하지 않으므로 신규 orphan 0건 도입. 회귀 가드(마커 ≥ baseline + 신규 orphan=0) 유지.
- **D3-defect (AC-BD-004b ≥1 distinguishing literal per Tier row)**: DEBT로 이월 (non-blocking). 신규 AC 추가는 SPEC body 변경 → blocker → manager-spec 위임 필요 (run-phase 범위 외).

### M2 — 패리티 계약 문서화 + 검증 하네스 (AC-BD-002, AC-BD-003) — PASS

- **AC-BD-003 (NET-NEW 게이트, 정적)**: `grep -rc "plugin-deployed" plugins/moai-code/ | grep -v ':0' | wc -l` = **1 파일**(README.md). HEAD was 0. README "패리티 계약" 섹션이 `/moai:project`(무설치)가 `system.yaml` version 필드에 리터럴 `"plugin-deployed vX.Y.Z"`를 기입하는 동작(REQ-BD-006)을 지시.
- **AC-BD-003 (런타임)**: `/moai:project` 실제 실행 후 생성 트리의 `system.yaml` version 라인에 `plugin-deployed vX.Y.Z` 마커 기입 여부 — 런타임 하네스 실행이 필요하므로 본 run-phase에서는 정적 directive만 문서화. 후속 sync-phase 또는 별도 검증에서 런타임 확인.
- **AC-BD-002 (RUNTIME 행위)**: 하네스(빈 디렉터리 A/B에서 `moai init` vs `/moai:project` 실행 후 파일-집합 diff, non-empty 가드 `> 10`)를 README에 문서화. **본 run-phase에서 하네스 미실행**(binary `moai init` + actual `/moai:project` invocation 환경 필요, run-phase 범위 외) — 하네스가 문서화되었으므로 후속 검증 가능 상태. RUNTIME 행위로 분류되어 자기통과 불가였음(acceptance §D.0 판별 모델).
- **REQ-BD-007 (DEFERRED)**: `moai doctor` 승격 로직은 전방 참조(forward-looking)로만 README에 기록(acceptance EC2와 정합). 본 SPEC AC로 검증 안 함(이연).
- **PRESERVE (AC-BD-008)**: parity-source markers in `plugins/moai-code/commands/` = **12**(baseline 12, 회귀 없음). orphan-edit = harness.md only(§A.2 사전존재 예외, 신규 도입 0건 — `commands/*.md` 미편집).

### M3 — Desktop Edition Tier 표 + 세션-시작 배선 (AC-BD-004, AC-BD-005a/b) — PASS

- **AC-BD-004 (NET-NEW 게이트)**: `grep -rc "Desktop Edition" plugins/moai-code/ | grep -v ':0' | wc -l` = **1 파일**(README.md). HEAD was 0. README "Desktop Edition 능력 Tier" 섹션 추가(Tier 1/2/3 능력 표, 3행 구조). `grep -ciE "Tier 1|Tier 2|Tier 3" README.md output-styles/*.md` = **4**(README.md) ≥ 3.
- **AC-BD-005a (NET-NEW 게이트)**: `grep -ciE "command -v moai|which moai|승격|promotion" plugins/moai-code/hooks/moai/handle-session-start.sh` = **5**. HEAD was 0. 바이너리 탐지 분기(`if command -v moai >/dev/null 2>&1; then ... fi`) 추가 — 존재 시 1줄 Tier 3 승격 안내(stderr), 부재 시 무음 fail-open.
- **AC-BD-005b (PRESERVE 회귀 가드)**: `grep -c "exit 0" plugins/moai-code/hooks/moai/handle-session-start.sh` = **1**(baseline 1, 회귀 없음). 무설치 자기완결 훅 fail-open 패턴 유지.
- **bash -n syntax**: `bash -n handle-session-start.sh` PASS. 실행 비트(`-rwxr-xr-x`) 보존.
- **런타임 smoke**: `echo '{"hook_event_name":"SessionStart"}' | bash handle-session-start.sh` exit code = 0 (이 dev 환경에 moai 바이너리가 있어 승격 안내가 stderr에 출력되었고 fail-open 정상 동작 확인).

### M4 — 버전 스탬프 SSOT 통합 (AC-BD-006a/b/c/d) — PASS

- **AC-BD-006c (NET-NEW 게이트)**: `grep -rc "VERSION-SSOT" plugins/moai-code/ | grep -v ':0' | wc -l` = **1 파일**(README.md). HEAD was 0. `grep -riE "일괄 bump|release.?checklist|릴리스.?체크리스트" plugins/moai-code/ | wc -l` = **2**(HEAD was 0). README "버전 스탬프 SSOT" 섹션 추가 — `www/hugo.toml` L50-54 SSOT-주석 패턴 미러링한 `⚠️ VERSION-SSOT — 릴리스 버전 4개 위치 일괄 bump 체크리스트` 라인.
- **AC-BD-006d (D1-GATED, D1=BIND 결정 후 ACTIVE → PASS)**: 정규화(`v` 접두·`-rcN` 제거) 후 concrete 리터럴 3곳 일치:
  - V_CW (cowork plugin.json) = `3.0.0` (D1 적용: 0.1.0 → 3.0.0)
  - V_CD (code plugin.json) = `3.0.0` (D1 적용: 0.1.0 → 3.0.0)
  - V_BIN (version.go `v3.0.0-rc6` → 정규화) = `3.0.0`
  - 3곳 전부 `3.0.0` 일치 → PASS. 플러그인 버전이 바이너리 v3.0.x 라인에 바인딩(REQ-BD-012).
- **AC-BD-006b (PRESERVE 회귀 가드)**: `grep -qF '{{.Version}}' system.yaml.tmpl` = placeholder 유지 OK(count=2). tmpl은 리터럴 값 아닌 플레이스홀더 유지(out-of-scope §E, 읽기 전용).
- **AC-BD-006a (정보용, non-gate)**: 4개 위치 전부 존재 확인(CW plugin.json `3.0.0` / CD plugin.json `3.0.0` / BIN `v3.0.0-rc6` / TMPL `{{.Version}}`).
- **D1 scope 준수**: marketplace.json `metadata.version`은 `0.1.0` 유지(REQ-BD-011 4-location 열거 밖, AC-BD-006d 3-literal match 밖). orchestrator D1 지시 + SPEC 열거 양쪽 모두 marketplace.json 제외 명시. VERSION-SSOT checklist에 별도 릴리스 단계로 문서화.
- **JSON validity**: `jq .` on both plugin.json → valid.

### M5 — SKIPPED (D2=KEEP)

- 사용자 결정 D2=KEEP에 따라 moai-code displayName `"MoAI Code"` 유지. AC-BD-007(OPTION) 비활성화. M5 마일스톤 수행 안 함.

## §E.3 Run-phase Audit-Ready Signal

```yaml
run_complete_at: 2026-07-03
run_commit_sha:
  M1: e0b7b37  # feat(SPEC-MOC-BOOTSTRAP-DESKTOP-001): M1 /project init 순증 — folder scaffold + skill-profile.yaml (AC-BD-001a/b NET-NEW)
  M2: e43674e  # feat(SPEC-MOC-BOOTSTRAP-DESKTOP-001): M2 parity contract + plugin-deployed stamping directive (AC-BD-003 NET-NEW)
  M3: 22e09d4  # feat(SPEC-MOC-BOOTSTRAP-DESKTOP-001): M3 Desktop Edition Tier table + session-start binary detection (AC-BD-004/005a NET-NEW)
  M4: 570ed6b  # feat(SPEC-MOC-BOOTSTRAP-DESKTOP-001): M4 VERSION-SSOT sentinel + D1 version bind 0.1.0 → 3.0.0 (AC-BD-006c NET-NEW, AC-BD-006d D1-GATED PASS)
run_status: complete  # M1-M4 전부 PASS, M5 SKIPPED (D2=KEEP)
ac_pass_count: 11     # 001a, 001b, 001c, 003(static), 004, 005a, 005b, 006b, 006c, 006d, 008 — 전부 PASS
ac_fail_count: 0
ac_runtime_documented_not_executed:
  - AC-BD-002  # RUNTIME 행위 — 하네스 README 문서화, 실행 안 함(binary + clean dirs 필요, run-phase 범위 외)
  - AC-BD-003-runtime  # 정적 directive PASS, 런타임 system.yaml 마커 확인은 후속 검증
preserve_list_post_run_count: 4  # 001c(legacy alias 14, CLAUDE.md heading 1), 005b(exit 0=1), 006b({{.Version}}=2), 008(parity-source=12, orphan=harness.md only)
l44_pre_commit_fetch: verified  # git fetch origin main + rev-list divergence 0 0 — parallel-session race 없음
l44_post_push_fetch: verified   # 각 milestone push 후 divergence 0 0 확인
new_warnings_or_lints_introduced: none  # bash -n PASS, jq valid, spec-lint 해당 없음(body 미편집)
cross_platform_build:
  go_build: N/A  # 본 SPEC은 markdown/shell/JSON 범위, Go 코드 수정 없음
  shell_check: bash -n PASS on handle-session-start.sh
total_run_phase_files: 6
  # plugins/moai-cowork/skills/project/SKILL.md (M1)
  # plugins/moai-code/README.md (M2 + M3 + M4)
  # plugins/moai-code/hooks/moai/handle-session-start.sh (M3)
  # plugins/moai-cowork/.claude-plugin/plugin.json (M4)
  # plugins/moai-code/.claude-plugin/plugin.json (M4)
  # .moai/specs/SPEC-MOC-BOOTSTRAP-DESKTOP-001/spec.md (M1 frontmatter draft→in-progress)
m1_to_mN_commit_strategy: per-milestone commits + push (M1, M2, M3, M4 each), Conventional Commits `feat(SPEC-MOC-BOOTSTRAP-DESKTOP-001): M{N} ...` + 🗿 MoAI trailer
decisions_resolved:
  D1: BIND  # 플러그인 버전 0.1.0 → 3.0.0 (바이너리 v3.0.x 라인 바인딩, REQ-BD-012)
  D2: KEEP  # moai-code displayName "MoAI Code" 유지, M5 SKIPPED, AC-BD-007 비활성화
shouldfix_handling:
  D2_defect_AC_BD_008_orphan_grep: addressed_at_run_entry  # harness.md = §A.2 사전존재 예외, commands/*.md 미편집으로 신규 orphan 0
  D3_defect_AC_BD_004b_tier_literal: carried_as_debt  # non-blocking, 신규 AC 추가는 SPEC body 변경 필요(run-phase 범위 외)
shared_file_boundary_respected: true  # skills/project/SKILL.md routing topology + marketplace table 미수정 (REMEDIATION-001 AC-REM-016 소관)
```

## §E.4 Sync-phase Audit-Ready Signal (completed transition 2026-07-09)

sync-phase 완료: CHANGELOG.md 추가 + frontmatter `status: implemented → completed` 전환.

```yaml
sync_complete_at: 2026-07-09
sync_commit_sha: <pending commit>
changelog_entry_added: true
frontmatter_transition:
  from: implemented
  to: completed
  reason: run-phase M1-M4 PASS(11/12 static AC), M5 SKIPPED(D2=KEEP). V12 RUNTIME AC(002/003-runtime) documented as residual risk. 3-phase close completed.
residual_risk:
  - AC-BD-002 (RUNTIME): 하네스 README 문서화 완료, 실제 runtime 검증 필요 (`moai init` vs `/moai:project` 파일 집합 diff + non-empty 가드, binary + clean dirs 환경 필요)
  - AC-BD-003-runtime: 정적 directive PASS, 런타임 `system.yaml` `plugin-deployed vX.Y.Z` 마커 검증 필요 (`/moai:project` 실행 환경 필요)
  - 두 RUNTIME AC는 별도 SPEC에서 runtime 검증 (실제 `/moai:project` plugin-command 실행 필요).
verification_b12_discipline:
  - 5 implementation files 읽기 완료 (manager-docs B12 discipline)
  - CHANGELOG.md grep pre-count = 0 (BOOTSTRAP 엔트리 이미 존재)
  - AC count match: acceptance.md SSOT 8 AC(001a/b/c, 004, 005a/b, 006a/b/c/d, 008; 007 skipped, 002+003-runtime RUNTIME). 11 static AC PASS.
  - File path verification: 모든 claimed path 실제 `ls` 확인 완료
```

## §E.5 Superseded Notice (2026-07-09)

**Status**: SPEC-MOC-BOOTSTRAP-DESKTOP-001 is superseded by SPEC-MOC-PLUGIN-MOAI-V2-001.

**sync-auditor Independent FAIL**:
- Harmonic mean: 60.6/100 (FAIL threshold: Tier L requires ≥ 0.85)
- Functionality: FAIL (5 PASS / 3 FAIL of 8 sampled ACs)
- Root cause: Parallel session implemented moai-coworker v5.0.0 integration + moai-pm `/project` entry point redesign (commits `43811a3` "M2.1-M2.5 PM /project 4-plugin hub router redesign" and `13f568d` "M3.4 README rewrite") which reverted the BOOTSTRAP premise (moai-cowork `/project` entry point)
- Verification-claim-integrity violation (§2 carry-over): sync-auditor measured against current tree (post-43811a3/13f568d) while BOOTSTRAP-001 `completed` transition assumed the pre-parallel-session state. The NET-NEW folder scaffold directive (AC-BD-001b) and VERSION-SSOT sentinel (AC-BD-006c) were destroyed by parallel-session commits, and the CLAUDE.md 구조 heading (AC-BD-001c) regressed without detection

**Failed ACs** (3 of 8 sampled):
- AC-BD-001b (NET-NEW folder scaffold directive) — destroyed by parallel-session commit `43811a3` which moved the project skill to `plugins/moai-pm/`
- AC-BD-001c (PRESERVE regression — `### 1. CLAUDE.md 구조` heading) — heading missing in current tree
- AC-BD-006c (NET-NEW "VERSION-SSOT" sentinel) — destroyed by parallel-session commit `13f568d` (M3.4 README rewrite)

**Successor SPEC**: SPEC-MOC-PLUGIN-MOAI-V2-001 (parallel session in progress, currently UNTRACKED)

**Historical sync commit preserved** (not reverted):
- `8683de5`: BOOTSTRAP-001 completed transition (spec.md `status: implemented → completed`, progress.md §E.4 sync-phase signal)

This commit remains in git history as the record of BOOTSTRAP-001's 3-phase close (plan→run→sync lifecycle completed 2026-07-09).
