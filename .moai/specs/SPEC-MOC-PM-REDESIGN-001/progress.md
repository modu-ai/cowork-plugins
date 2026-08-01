# SPEC-MOC-PM-REDESIGN-001 — progress.md

## §E.1 Plan-phase Audit-Ready Signal

```yaml
plan_status: audit-ready
plan_complete_at: 2026-07-09
plan_audit_iter1: "PASS-WITH-DEBT 0.83 — D1-D8·D10 applied 2026-07-09, D9 documented debt (acceptance §D.4 residual)"
tier: M
artifacts: [spec.md, plan.md, acceptance.md, progress.md]
requirements: 13 REQ + 8 NFR
ac_count: 19 mechanical + 5 review + 5 GWT
```

## §E.2 Run-phase Evidence

기준 디렉토리 `$SK` = `plugins/moai-pm/skills/project`. 모든 검증은 M5 완료 시점 tree에서 단일 배치로 실측(2026-07-09). 실행 위치: agent worktree(branch `worktree-agent-a192327e4b947ff63`, base 56f9e09).

### 기계 AC 매트릭스 (19건)

| AC | 검증 명령 (요약) | Actual Output | Status |
|----|------------------|---------------|--------|
| AC-PMR-001 | `grep -c "요청 평가" $SK/references/templates/CLAUDE.md.tmpl` | `3` (사다리 3단: 대화→스킬→파일 + 서술 금지 문구 동반) | PASS |
| AC-PMR-002 | `grep -c "파일 생성 기준" …tmpl` | `2` (개요→섹션별 반복 생성 문구 동반) | PASS |
| AC-PMR-003 | cowork 가드 / tmpl 가드 / tmpl 15단어 | `5` / `2` / `1` (가사·시 재현 금지 문구 동반) | PASS |
| AC-PMR-004 | leak 리터럴 `severe violation\|displacive\|Never reproduce` | `0` | PASS |
| AC-PMR-005 | 출처 주석 파일 수 / 비주석 매치 | `6` (≥3) / `0` | PASS |
| AC-PMR-006 | `grep -c "검색 스케일링" …execution-protocol.md` | `2` (1회/3-5회/5-10회+ 토큰 동반) | PASS |
| AC-PMR-007a | `grep -c "맥락 적용" …tmpl` | `2` (메타 코멘터리 금지 문구 동반) | PASS |
| AC-PMR-007b | `grep -c "맥락 적용 규칙" …context-collector.md` | `2` (금지 문구 목록 5종 동반) | PASS |
| AC-PMR-008 | `grep -c "{user_name}" …tmpl` | `0` | PASS |
| AC-PMR-009 | tmpl slop / cowork humanize | `6` / `2` | PASS |
| AC-PMR-010 | `/project resume` cowork/coder/designer | `2` / `1` / `1` | PASS |
| AC-PMR-011 | coder `moai-workflow-project` / `적용하지 않는다` | `11` / `2` (.claude/.moai 구조 항목 동반) | PASS |
| AC-PMR-012 | designer `DESIGN.md` / `파일 생성 기준` | `18` (≥3) / `2` | PASS |
| AC-PMR-013 | `grep -c 'version: "0.3.0"' $SK/SKILL.md` | `1` | PASS |
| AC-PMR-014 | tmpl `wc -l` / 예산 표 합계 명시 | `147` (≤150) / `≤ 200` 명시 4곳 | PASS |
| AC-PMR-015 | generator `10개` | `3` | PASS |
| AC-PMR-016 | init-protocol `4질문\|4옵션` | `2` (무변경 표면 — baseline 동일) | PASS |
| AC-PMR-017 | 제외 패턴 명칭 리터럴 | `0` | PASS |
| AC-PMR-018 | tmpl `톤 규칙` | `2` (프로즈 기본·응답 깊이 비례 동반) | PASS |

### 리뷰 AC (5건 — diff 리뷰 판정)

| AC | 판정 | 근거 |
|----|------|------|
| AC-PMR-R01 | PASS | 신규 숫자 카운트 도입 0건. 기존 스냅샷 표기(192/11/28/1·232)는 SKILL.md·INDEX.md에서 "(스냅샷)" 헤더 + 실측 정본(Phase 2 인벤토리) 주석으로 통일 |
| AC-PMR-R02 | PASS | P1-P6 전 블록 독자적 한국어 문장 — 원문 영어 구조 추종 없음(leak 리터럴 0 + 15단어+ 연속 인용 없음, 전 블록 재표현) |
| AC-PMR-R03 | PASS | cowork 8-Phase 열거(인터뷰→인벤토리→체인설계→Gap→확인→CLAUDE.md→API키→첫실행) 1:1 보존, coder/designer 5-Phase 열거 보존(grep 실측 각 1) |
| AC-PMR-R04 | PASS | cowork-setup §2-1 기록 규칙("체인별 설계 근거 1줄") + Phase 3 표("입력 3종 종합") + Phase 5 표("설계 근거 표시") — Phase 3→5 흐름에 근거 기록 지점 존재 |
| AC-PMR-R05 | PASS | tmpl §4 "판단 계층: ① 파일을 만들지 먼저 결정한다 → ② 만들기로 했으면 §5 표의 office 스킬을 사용한다" — office 우선 표(§5)의 상위 판단으로 명시 |

### 불변식 NFR-PMR-001..008 (8건)

| NFR | 검증 | Actual Output | Status |
|-----|------|---------------|--------|
| 001 4-plugin 허브 | SKILL.md 4-plugin 표 + PM 라우팅 원칙 | `PM은 구현하지 않는다` 1건 보존. 주의: 병렬 SPEC(56f9e09)이 moai-coder→moai 개명 — 4-plugin 구조 자체는 불변 | PASS |
| 002 ≤200라인·체인≤10 | generator 예산 표 합계 `≤ 200` + `10개` grep | 합계 ≤200 명시 + 10개 3건 + HARD 블록 축소 금지 명문 | PASS |
| 003 글로벌 프로필 금지 | `{user_name}` grep | `0` | PASS |
| 004 동적 인벤토리 | 신규 하드코딩 카운트 diff 리뷰 | 신규 0건 + 기존 카운트 "(스냅샷)" 명시 통일 | PASS |
| 005 AskUserQuestion 제약 | init-protocol `4질문\|4옵션` + tmpl 톤 규칙 "1라운드 4질문 이내" | `2` + 톤 규칙 정합 문구 | PASS |
| 006 ko-only | 재설계 전 파일 한국어 표면 유지 | 전 신규 블록 한국어 작성 | PASS |
| 007 ai-slop 종료 | tmpl slop 6 + cowork humanize 2 | ≥1 각각 | PASS |
| 008 Gap+resume 보존 | 3분기 `/project resume` | `2/1/1` | PASS |

### GWT 시나리오 논거 (S1-S5 — 프로토콜/생성 규칙 문면 검증)

- **S1**: tmpl 5블록 전부 존재(AC-001/002/003/007a/018) + 체인≤10·ai-slop 종료(NFR-002/007) + Phase 5 설계 근거 표시(R04) — 문면 충족. 런타임 E2E 실연은 residual.
- **S2**: coder-setup Phase 3 설치 명세(.claude/ rules·agents·hooks·commands + .moai/ config·specs + CLAUDE.md, `moai:moai-workflow-project` 위임) + Phase 3-1 두-템플릿 분리(AC-011) — 문면 충족.
- **S3**: tmpl §7 인용·저작권 가드(15단어 미만·출처당 1회·대체 요약 금지·재표현 기본) — 생성 CLAUDE.md 규칙 문면 충족.
- **S4**: tmpl §14 + context-collector §5-3 메타 코멘터리 금지 문구 목록 — 문면 충족.
- **S5**: tmpl §3 사다리 1단 종료 + execution-protocol §6-5 단일 사실 1회 — P1·P4 결합 문면 충족.

## §E.3 Run-phase Audit-Ready Signal

```yaml
run_complete_at: 2026-07-09
run_commit_sha: "3008716"
run_commits: ["c963698 (M1)", "cf80918 (M2)", "3b841cd (M3)", "24edefd (M4)", "3008716 (M5)"]
run_status: complete
ac_pass_count: 24  # 기계 19 + 리뷰 5
ac_fail_count: 0
preserve_list_post_run_count: 8  # NFR-PMR-001..008 전부 회귀 0
l44_pre_commit_fetch: not-applicable  # agent worktree 격리 실행(base 56f9e09), push 없음(오케스트레이터 지시)
l44_post_push_fetch: not-applicable  # push 미수행 — worktree branch 커밋만
new_warnings_or_lints_introduced: none  # markdown 전용 SPEC — 런타임 코드·훅 무변경
cross_platform_build:
  applicable: false  # Go 코드 변경 없음 (Out of Scope §3 — 순수 markdown 재설계)
total_run_phase_files: 11  # 스킬 9 (tmpl·generator·cowork·execution·coder·designer·context-collector·SKILL·INDEX) + spec.md frontmatter + progress.md
m1_to_mN_commit_strategy: "M1-M5 마일스톤별 분리 커밋, pathspec 한정(plugins/moai-pm + .moai/specs/SPEC-MOC-PM-REDESIGN-001), agent worktree branch, push 없음"
mx_tags_created: 4  # tmpl HARD @MX:ANCHOR / generator 예산표 @MX:ANCHOR / cowork 저작권 가드 @MX:WARN(+REASON) / execution 검색 스케일링 @MX:NOTE
deviation_notes:
  - "플러그인 개명(moai-coder→moai)이 병렬 SPEC-MOC-PLUGIN-MOAI-V2-001 M1(56f9e09)로 선착 — coder-setup 재작성 라인은 현행명 moai(:moai-workflow-project) 사용, 구명은 '(구 moai-coder)' 주석 보존. AC anchor(moai-workflow-project) 불변. SKILL.md·INDEX.md·router.md·init-protocol.md(×10)·diagnostic-protocol.md의 잔여 moai-coder 표기는 병렬 SPEC M5 sweep 소관이라 미변경 (sync-audit이 전수 열거로 확장)"
residual_risks:
  - "S1-S5 런타임 E2E 실연 미수행(문면 검증만 — acceptance §D.4 허용 residual)"
  - "AC-PMR-017 명칭 리터럴 기반 — 개념 잔여는 D9 문서화 부채(acceptance §D.4)"
```

## §E.4 Sync-phase Audit-Ready Signal

```yaml
sync_complete_at: 2026-07-09
sync_commit_sha: "fd8184d"
sync_status: complete
files_modified: 11  # plugins/moai-pm (SKILL.md + INDEX.md + tmpl + 6 setup protocols) + spec.md frontmatter + progress.md
documentation_sync:
  - "plugin.json version: 0.2.0 → 0.3.0"
  - "SKILL.md version already 0.3.0 (M5 authored)"
  - "README.md: no version/setup-flow changes required (4-plugin structure stable)"
version_sync_decisions:
  - "plugin.json: version bump 0.2.0 → 0.3.0 (SKILL.md canonical version)"
  - "README.md: skipped (user-facing 4-plugin structure unchanged)"
  - "marketplace.json: not present in this plugin (CHANGELOG-only emission deferred)"
artifacts_status_transition: "in-progress → implemented → completed (single sync commit)"
```
