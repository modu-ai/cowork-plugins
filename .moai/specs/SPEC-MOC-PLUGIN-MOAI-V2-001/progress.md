# SPEC-MOC-PLUGIN-MOAI-V2-001 — 진행 상황 (progress)

## §E.1 Plan-phase Audit-Ready Signal

```yaml
plan_status: audit-ready
plan_complete_at: 2026-07-09T05:10:22Z
plan_audit: "iter-1 FAIL 0.88 (6결함) → iter-2 PASS 0.97 (잔존 0) — .moai/reports/plan-audit/SPEC-MOC-PLUGIN-MOAI-V2-001-2026-07-09.md"
artifacts: [spec.md, plan.md, acceptance.md, design.md, research.md, progress.md]
tier: L
open_decisions: []  # DP-1("1.0.0" 리셋)·DP-2(gateguard vendor) 모두 2026-07-09 사용자 확정 — plan.md §H
census_head: 6f92d86
```

## §G IGGDA Kickoff Predicate

- (a) 의도 명확성 100%: PASS — 설계 v2 결정 레지스터 D-1~D-5 + DP-1/DP-2 + Tier/Git 전략 전부 사용자 확정
- (b) plan-auditor PASS: PASS — iter-2 0.97 (임계 0.85)
- (c) Tier S/M: **FAIL — Tier L**
- (d) 위험 키워드/파괴 범위: 해당 없음 (단 (c) 선행 실패)
- 판정: **explicit-gate** (Implementation Kickoff Approval은 차단형 AskUserQuestion으로 진행)
- 평가 시각: 2026-07-09T05:10:22Z
- Implementation Kickoff Approval: **승인** (2026-07-09) — "Mode 5 순차 M1→M6" 차단 AskUserQuestion 응답

## §F Phase 0.95 Mode Selection

```yaml
# Input parameters (collected 2026-07-09, pre-flight 드리프트 0)
tier: L
scope_files: "100+ (M1 git mv 트리 ~354 + M2 rules 61 + config ≥27 + CLAUDE.md + settings + M3 dispatch+gates + M4 scaffold + M5 다수 문서)"
domain_count: 6   # hooks(sh) / templates(md+yaml) / scripts(sh) / manifests(json) / docs(README+www) / config(yaml)
file_language_mix: "markdown + shell + yaml + json (컴파일 없음, 코딩-헤비 아님 — restructuring)"
concurrency_benefit: LOW   # M1 개명이 M2~M6 전부의 전제(plugins/moai/ 경로), 강한 순차 의존
agent_teams_prereqs:
  env_var: "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 (설정됨)"
  harness_level: "thorough 여부 무관 — Mode 5 선택에 영향 없음"
  team_enabled: "무관 — Mode 5 선택"
implementation_kickoff_approval: "승인 — Mode 5 순차 M1→M6 (2026-07-09 explicit-gate 차단 AskUserQuestion)"
```

Mode evaluation (6 modes):

| Mode | Selected? | Rationale |
|---|---|---|
| 1 trivial | No | Tier L + 6 마일스톤, 단순 typo 아님 |
| 2 background | No | Write 작업 다수 (background-write 제한) |
| 3 agent-team | No | restructuring + 순차 의존; team 오버헤드 불필요 |
| 4 parallel | No | M1 개명이 M2-M6 전제 → 병렬화 불가 |
| 5 sub-agent | **Yes (선택)** | 마일스톤별 순차 위임. 코딩-헤비 아닌 restructuring이나 순차 의존이 결정적 |
| 6 workflow | No | 다규칙/의존성 작업 — Mode 6은 단일 기계 변환만 허용; Anthropic 병렬화 경고 |

Decision: sub-agent

Justification: 본 SPEC은 행위 보존 재구조화(rename + move + 참조 갱신)로 코딩-헤비가 아니지만, M1(개명)이 M2~M6 전부의 경로 전제(plugins/moai/)라 강한 순차 의존이 존재. Anthropic 코딩-병렬화 경고("대부분의 코딩 작업은 연구보다 진정 병렬화 가능한 작업이 적다")와 마일스톤 순차 의존성이 일치 → Mode 5(순차 sub-agent)가 안전한 기본값. 마일스톤별 manager-develop 위임 + Hybrid Trunk main-direct push로 단일 에이전트 컨텍스트 한계 회피하면서 각 마일스톤 AC 검증.

## §E.2 Run-phase Evidence

### M1 — 개명 + 마켓 갱신 (AC-MV2-001a·b·c·d)

**Claim**: `plugins/moai-coder/` → `plugins/moai/` 개명 완료(git mv 354 entries rename), manifest·marketplace 갱신(name=`moai`·version=`"1.0.0"` DP-1·source=`./plugins/moai`·톰스톤 0), Layer-1 인벤토리 보존.

**Evidence (verbatim AC outputs, 2026-07-09)**:

AC-MV2-001a (NET-NEW+REMOVAL):
```
$ test -d plugins/moai && test ! -d plugins/moai-coder; echo "exit=$?"
exit=0
```

AC-MV2-001b (NET-NEW):
```
$ jq -r '.name, .displayName, .version' plugins/moai/.claude-plugin/plugin.json
moai
코더
1.0.0
```

AC-MV2-001c (NET-NEW+REMOVAL):
```
$ jq -r '.plugins[].name' .claude-plugin/marketplace.json
moai-coworker
moai-designer
moai
moai-pm
$ jq '.plugins | length' .claude-plugin/marketplace.json
4
$ jq -r '.plugins[] | select(.name=="moai") | .source' .claude-plugin/marketplace.json
./plugins/moai
$ jq '.plugins[] | select(.name=="moai-coder")' .claude-plugin/marketplace.json | wc -l
0
```
→ 4-plugin 유지, `moai` 포함, `moai-coder` 톰스톤 0 (REQ-MV2-003 PASS).

AC-MV2-001d (PRESERVE — self-pass 의도됨):
```
$ find plugins/moai/commands -name '*.md' | wc -l          → 14
$ find plugins/moai/agents -type f | wc -l                 → 8
$ ls -d plugins/moai/skills/*/ | wc -l                     → 29
$ find plugins/moai/output-styles -maxdepth 1 -type f | wc -l → 2 (einstein.md, moai.md)
$ test -f plugins/moai/.mcp.json && echo ".mcp.json present" → .mcp.json present
```
→ commands 14 · agents 8 · skills 29 · output-styles 2 · .mcp.json — 기준선(research.md §E, census_head 6f92d86)과 동일(PRESERVE characterization).

Regression guard (PRESERVE-RUNTIME):
```
$ claude plugin validate ./plugins/moai; echo "exit=$?"
✔ Validation passed with warnings
exit=0
$ claude plugin validate .claude-plugin/marketplace.json; echo "exit=$?"
✔ Validation passed with warnings
exit=0
```

**Baseline-attribution**: 기준선 HEAD cdbc808(병렬 세션 SPEC-MOC-PM-REDESIGN-001 plan-phase — plugins/ 비중첩 확인). rename 전 인벤토리(14/8/29/2/.mcp.json)는 §C.3 pre-flight에서 캡처, rename 후 상기 Evidence와 동일(PRESERVE 회귀 가드 통과). marketplace validate HEAD에서 PASS → rename 후에도 PASS(라벨된 self-pass).

**Gaps**: `P0-8-verdict:` 센티넬 라인 — M6 소관(AC-MV2-006c). M1 범위 외; 의도적으로 미기록(NET-NEW 판별력 보존 — acceptance.md §D.6). `claude plugin validate --strict`(SHOULD) 미실행 — M6 소관.

**Residual-risk**: 본 저장소 T3 공존 typed-name 충돌(P0-8) 실측은 M6. M1은 개명 + manifest 갱신만 수행; 플러그인 본문(스킬·커맨드)의 잔존 `moai-coder` 참조 35곳(12파일)은 M5 소관(AC-MV2-005a) — M1에서는 스코프 외.


### M2 — 2계층 재배치 (AC-MV2-002a·b·c·d·e·f)

**Claim**: rules 61파일 `rules/moai/` → `templates/claude/rules/moai/` 이동(git mv, R100 0-content-change), ADK 정본 CLAUDE.md vendor + parity-source 마커, settings.project.json Web-activation 3키, `.moai/config/sections` ≥27 yaml vendor + 최소 토큰화, output-styles 2종 플러그인 네이티브 보존.

**Evidence (verbatim AC outputs, 2026-07-09)**:

AC-MV2-002a (NET-NEW+REMOVAL):
```
$ find plugins/moai/templates/claude/rules/moai -type f | wc -l
61
$ test ! -d plugins/moai/rules; echo "exit=$?"
exit=0
```

AC-MV2-002b (PRESERVE — git mv R100 rename detection, self-pass 의도됨):
```
$ git diff --stat -M100 56f9e09..ad86a50 -- 'plugins/moai/rules' 'plugins/moai/templates/claude/rules'
61 files changed, 0 insertions(+), 0 deletions(-)
$ git diff -M100 --summary (...) | grep -c '^ rename'
61   (전부 100% similarity)
$ git diff --numstat -M100 (...) | awk '{a+=$1;d+=$2} END{print a,d}'
0 0   (content-change 라인 0)
```
주: M2 커밋 전 staged-diff로 캡처 — e6b8507(BOOTSTRAP 병렬 세션)이 `plugins/moai/rules` 0파일 터치(비중첩 확인) → post-commit `56f9e09..ad86a50` diff와 동일.

AC-MV2-002c (NET-NEW — EC-6 ADK 정본 판별):
```
$ test -f plugins/moai/templates/CLAUDE.md; echo "exit=$?"
exit=0
$ grep -c 'parity-source: internal/template/templates/CLAUDE.md' plugins/moai/templates/CLAUDE.md
1
$ wc -l plugins/moai/templates/CLAUDE.md
321 plugins/moai/templates/CLAUDE.md   (ADK 정본 319행 + 증명 마커 2행)
$ grep -c 'claude.mo.ai.kr' plugins/moai/templates/CLAUDE.md
0   (anti-pattern 가드: 루트 CLAUDE.md 프로젝트 고유 참조 부재 → ADK 정본 확인)
```
→ parity-source 마커가 유일 기계 판별자(acceptance.md EC-6). ADK 원천 `/Users/goos/moai/moai-adk-go/internal/template/templates/CLAUDE.md`에서 vendor.

AC-MV2-002d (NET-NEW — Web-activation 3키):
```
$ jq -r '.outputStyle' plugins/moai/templates/claude/settings.project.json
moai:MoAI
$ jq '.extraKnownMarketplaces["moai-claude"]' plugins/moai/templates/claude/settings.project.json
{
  "source": "github://modu-ai/claude"
}   (≠ null)
$ jq '.enabledPlugins["moai@moai-claude"]' plugins/moai/templates/claude/settings.project.json
true
$ jq empty plugins/moai/templates/claude/settings.project.json; echo "exit=$?"
exit=0   (valid JSON)
```

AC-MV2-002e (NET-NEW — config sections ≥27 + 최소 토큰화):
```
$ find plugins/moai/templates/moai/config/sections -name '*.yaml' | wc -l
27   (≥27 PASS)
$ grep -c '{{PROJECT_USER_NAME}}' plugins/moai/templates/moai/config/sections/user.yaml
1
$ grep -c '{{PROJECT_NAME}}' plugins/moai/templates/moai/config/sections/project.yaml
1
$ grep -c '{{DATE}}' plugins/moai/templates/moai/config/sections/project.yaml
1
```
토큰화 범위(REQ-MV2-007(c)): 프로젝트-변수 값만 → `{{PROJECT_USER_NAME}}`·`{{PROJECT_NAME}}`·`{{DATE}}`(scaffold.sh M4 3토큰과 일치). 방법론 기본값(development_mode·quality 임계·harness level 등)은 리터럴 보존. 절대경로/머신고유값 0건(사전 스캔 확인). 원천 `.moai/config/sections/` 원본은 무수정(C-2 단방향 vendor).

AC-MV2-002f (PRESERVE — output-styles 플러그인 네이티브 잔류, self-pass 의도됨):
```
$ find plugins/moai/output-styles -maxdepth 1 -type f | wc -l
2   (einstein.md, moai.md)
$ grep -c '^name: MoAI' plugins/moai/output-styles/moai.md
1
```
→ 셀렉터 `moai:MoAI` 계약(research.md §B P0-2) 보존 — M2에서 output-styles 무편집.

**Baseline-attribution**: 기준선 HEAD e6b8507(M1 완료 후 + BOOTSTRAP 병렬 세션 비중첩 커밋). rules 61파일은 M1 커밋 56f9e09에서 `plugins/moai/rules/moai/`에 존재 → M2 git mv로 `templates/claude/rules/moai/` 이동(R100, 0 content-change). CLAUDE.md·settings·config는 HEAD에서 부재(NET-NEW) → M2 산출. output-styles 2종은 M1 기준선과 동일(PRESERVE 회귀 가드).

**Gaps**: scaffold.sh 산출(`{{TOKEN}}` 치환·백업·settings 병합)은 M4 소관(AC-MV2-004a~g) — M2는 템플릿 페이로드 준비까지만. settings.project.json의 `extraKnownMarketplaces` source 포맷(`github://modu-ai/claude`)은 M4 scaffold·P0-w(Web 실측)에서 런타임 검증 대기 — 본 SPEC Out of Scope이나 포맷 적합성은 사용자 실측에 귀속.

**Residual-risk**: templates/CLAUDE.md는 ADK 정본의 스냅샷 — ADK 원본이 갱신되면 templates 사본은 stale(drift 위험). 다만 parity-source 마커가 원천 경로를 명시해 추적 가능. config sections 토큰화는 최소 3종(`{{PROJECT_NAME}}`·`{{VERSION}}`(미사용)·`{{DATE}}` + `{{PROJECT_USER_NAME}}`) — M4 scaffold.sh가 3토큰(PROJECT_NAME/VERSION/DATE)을 치환하므로 `{{PROJECT_USER_NAME}}`은 scaffold 후 리터럴 잔류 가능(M4에서 토큰 세트 확장 여부 소관).


### M3 — 훅 통합 (AC-MV2-003a·b·c·d·e)

**Claim**: hooks 24스크립트(handle-* 20 + 게이트 4) → 단일 `hooks/dispatch.sh` + `hooks/gates/` 5종(기존 4 이관 + gateguard vendor DP-2)로 통합. hooks.json 20 이벤트 전부 dispatch.sh 라우팅, handle-* 20종 삭제, `$CLAUDE_CODE_REMOTE` 분기 + `command -v moai` T3 자동활성 + fail-open(exit 0 전 경로). event 집합 20종 보존(PRESERVE).

**Evidence (verbatim AC outputs, 2026-07-09)**:

AC-MV2-003a (NET-NEW — dispatch.sh 존재 + lint):
```
$ test -f plugins/moai/hooks/dispatch.sh && bash -n plugins/moai/hooks/dispatch.sh; echo "exit=$?"
exit=0
```

AC-MV2-003b (REMOVAL — handle-* 20종 소거):
```
$ find plugins/moai/hooks -name 'handle-*.sh' | wc -l
0
```

AC-MV2-003c (NET-NEW+PRESERVE — 전 이벤트 dispatch.sh 라우팅 + 이벤트 집합 보존):
```
$ jq -r '(.hooks // .) | .. | .command? // empty' plugins/moai/hooks/hooks.json | grep -vc 'dispatch.sh'
0   (20개 command 전부 dispatch.sh — dispatch.sh 외 참조 0)
$ jq -r '(.hooks // .) | if type=="object" then (if has("hooks") then (.hooks|keys[]) else keys[] end) else . end' plugins/moai/hooks/hooks.json | sort > /tmp/m3_events_after.txt
$ diff /tmp/m3_events_before.txt /tmp/m3_events_after.txt
(빈 diff = 이벤트 키 집합 20종 동일 — PRESERVE 회귀 가드 통과)
```
이벤트 키 20종(동일): ConfigChange, CwdChanged, FileChanged, InstructionsLoaded, PermissionDenied, PermissionRequest, PostCompact, PostToolUse, PostToolUseFailure, PreCompact, PreToolUse, SessionEnd, SessionStart, Stop, StopFailure, SubagentStart, SubagentStop, TaskCompleted, TeammateIdle, UserPromptSubmit.

AC-MV2-003d (NET-NEW — dispatch.sh 분기 마커):
```
$ grep -c 'CLAUDE_CODE_REMOTE' plugins/moai/hooks/dispatch.sh
3   (≥1 — Web/remote 분기 + 주석)
$ grep -c 'command -v moai' plugins/moai/hooks/dispatch.sh
1   (≥1 — T3 자동활성 프로브)
$ tail -5 plugins/moai/hooks/dispatch.sh | grep -c 'exit 0'
1   (≥1 — 최종 fail-open exit 0)
```

AC-MV2-003e (NET-NEW — gates ≥5 + lint, DP-2 gateguard vendor 채택):
```
$ ls plugins/moai/hooks/gates/*.sh | wc -l
5
$ for f in plugins/moai/hooks/gates/*.sh; do bash -n "$f" || echo "FAIL $f"; done
(전부 OK — gateguard-fact-force, iggda-audit-preservation-guard, status-transition-ownership, sync-phase-quality-gate, team-ac-verify)
```
gates/ 5종 = 기존 4종(git mv R100 content-intact) + gateguard-fact-force.sh(DP-2 vendor, 원천 `moai-adk-go/internal/template/templates/.claude/hooks/moai/gateguard-fact-force.sh`).

**dispatch.sh event→gate 매핑 (인코딩된 라우팅)**:
- T3 경로(`command -v moai` 성공, `$CLAUDE_CODE_REMOTE != true`): PascalCase→kebab 변환 후 `exec moai hook <kebab>` — 20 이벤트 전부 매핑(PreCompact→`compact` 특수케이스 포함). T3에서 moai native가 전담, bash 게이트는 미실행(설계 의도 — T1/T2/Web 대비 fallback).
- Gate-only fallback(바이너리 부재 / Web remote): PostToolUse→`status-transition-ownership.sh`, Stop→`sync-phase-quality-gate.sh`, TaskCompleted→`team-ac-verify.sh`, PreToolUse→`gateguard-fact-force.sh`(DP-2 vendor). iggda-audit-preservation-guard.sh는 이벤트 매핑 없음(수동/orchestrator 검증배치 호출 전용 — 헤더 "Run: bash ..." 명시).
- 매핑 없는 16종 이벤트(SessionStart, PreCompact, SessionEnd, PostToolUseFailure, SubagentStart, SubagentStop, UserPromptSubmit, TeammateIdle, ConfigChange, StopFailure, PostCompact, InstructionsLoaded, CwdChanged, FileChanged, PermissionDenied, PermissionRequest) → 무음 `exit 0`(retired handle-* stub 동질 — stdin drain + fail-open).

**기능 smoke test (T3 환경 — 본 저장소 moai 바이너리 존재)**:
```
$ echo '{...PostToolUse...}' | bash dispatch.sh PostToolUse
{"hookSpecificOutput":{"hookEventName":"PostToolUse"}}   ← exec moai hook post-tool 정상 동작
$ CLAUDE_CODE_REMOTE=true bash dispatch.sh PostToolUse   ← gate-only 모드 분기 확인(status-transition-ownership 게이트 실행)
$ CLAUDE_CODE_REMOTE=true bash dispatch.sh SessionEnd < /dev/null; echo "exit=$?"
exit=0   ← 매핑 없음 → drain + fail-open
```

**Baseline-attribution**: 기준선 HEAD 3dfcc42(병렬 PM-REDESIGN 세션 커밋 흡수 — plugins/moai/ 비중첩 확인). M3 착수 전: handle-* 20 + 게이트 4 = .sh 24종, hooks.json 20 이벤트가 handle-*.sh(20)+게이트(2: status-transition PostToolUse, sync-phase Stop)로 분산. M3 후: dispatch.sh 1 + gates/ 5 = 구조 통합, 이벤트 집합 20종 불변(PRESERVE). 게이트 4종은 git mv R100(content-intact, 내부 로직 무편집 — B10). gateguard는 ADK 정본에서 vendor(DP-2, parity-source 동일 경로).

**Gaps**: 본 저장소 T3 환경에서 `exec moai hook` 경로가 바이너리 감지 시 게이트를 우회하는 것은 설계 의도(T3 native 전담)이나, moai native hook이 4 bash 게이트(status-transition-ownership 등)의 등가 기능을 포함하는지는 M6 런타임 검증(AC-MV2-006a~d) 소관. gateguard(PreToolUse→첫편집 조사 advisory)는 additive 동작 — 기존 handle-pre-tool.sh(pure stub) 대비 advisory 추가, 단 fail-open(exit 0) 불변. iggda-audit-preservation-guard.sh는 이벤트 매핑 없음(수동 호출 전용) — gates/에 존재하나 dispatch.sh 라우팅 미연결(현행 hooks.json에서도 미연결이었으므로 PRESERVE).

**Residual-risk**: dispatch.sh의 PascalCase→kebab 변환표는 moai 바이너리 서브커맨드 명명 규칙에 의존 — moai CLI가 서브커맨드명을 변경하면 변환표 갱신 필요(현재 20종 전부 ADK handle-*.sh.tmpl 원천과 교차 검증 완료). `$CLAUDE_CODE_REMOTE` 분기는 Web 세션에서 바이너리 프로브를 생략(REQ-MV2-011)하나, 실제 Web 환경($CLAUDE_CODE_REMOTE=true)에서의 게이트 동작 검증은 P0-w(사용자 수행, §E Out of Scope) 대기. 클라ude plugin validate exit 0(warnings = pre-existing command frontmatter 경고, M1 기준선과 동일 — 회귀 아님).

### M4 — scaffold.sh + /moai:project 배선 (AC-MV2-004a~g)

**Claim**: M4는 결정론적 cp+sed 스캐폴더(`plugins/moai/scripts/scaffold.sh`)를 신규 작성하고 `/moai:project` 스킬에 배선하여, Layer-2 템플릿 페이로드를 임의 타겟 프로젝트에 토큰 치환 + settings.json 보존 병합으로 전개한다. 7개 AC(004a~g) 전부 PASS.

**Evidence** (verbatim, 2026-07-09 임시 디렉토리 실측):

AC-MV2-004a (scaffold.sh 존재 + bash -n clean):
```
$ test -x plugins/moai/scripts/scaffold.sh && bash -n plugins/moai/scripts/scaffold.sh
test -x: PASS
bash -n exit code: 0
```

AC-MV2-004b (dry-run — 무기록 + 계획 출력 ≥1줄):
```
$ bash plugins/moai/scripts/scaffold.sh --dry-run --name test-project --version 0.1.0 --user testuser /tmp/m4_dry
scaffold.sh --dry-run (no files will be written)
  target:       /tmp/m4_dry
  project_name: test-project
  version:      0.1.0
  ...
  files planned: 90
---
  [copy] .../templates/CLAUDE.md -> /tmp/m4_dry/CLAUDE.md
  [merge] .../templates/claude/settings.project.json -> /tmp/m4_dry/.claude/settings.json
  ... (90 files listed)
---
dry-run complete.
$ echo $? → 0
$ bash plugins/moai/scripts/scaffold.sh --dry-run /tmp/m4_dry | wc -l → 191
$ find /tmp/m4_dry -type f | wc -l → 0
```

AC-MV2-004c (실제 실행 — Layer-2 트리 생성 + 토큰 치환 완료):
```
$ bash plugins/moai/scripts/scaffold.sh --name my-app --version 0.2.0 --user "Goos Kim" /tmp/m4_run
Done. copied: 89, merged: 1, backed up: 0.
$ test -f /tmp/m4_run/CLAUDE.md → PASS
$ find /tmp/m4_run/.claude/rules/moai -type f | wc -l → 61
$ find /tmp/m4_run/.moai/config/sections -name '*.yaml' | wc -l → 27
$ grep -rlE '\{\{(PROJECT_NAME|VERSION|DATE)\}\}' /tmp/m4_run | wc -l → 0
```
토큰 치환 확인: `project.yaml` → `name: "my-app"`, `user.yaml` → `name: "Goos Kim"`.

AC-MV2-004d (settings.json 보존 병합 — REQ-MV2-014):
```
$ echo '{"model":"opus"}' > /tmp/m4_merge/.claude/settings.json   # 사전 seed
$ bash plugins/moai/scripts/scaffold.sh --name merge-test /tmp/m4_merge
Done. copied: 89, merged: 1, backed up: 1.
$ jq -r '.model' /tmp/m4_merge/.claude/settings.json → opus              # 보존
$ jq -r '.outputStyle' ... → moai:MoAI                                   # 추가
$ jq -r '.extraKnownMarketplaces["moai-claude"].source' ... → github://modu-ai/claude  # 추가
$ jq -r '.enabledPlugins["moai@moai-claude"]' ... → true                 # 추가
```
최종 settings.json = `{"model":"opus","outputStyle":"moai:MoAI","extraKnownMarketplaces":{"moai-claude":{"source":"github://modu-ai/claude"}},"enabledPlugins":{"moai@moai-claude":true}}` — 사용자 키 보존 + 3키 additive 병합.

AC-MV2-004e (백업 — 동일 디렉토리 2회차 실행):
```
$ bash plugins/moai/scripts/scaffold.sh --name my-app /tmp/m4_run   # 2회차
Done. copied: 89, merged: 1, backed up: 90.
$ find /tmp/m4_run/.moai-backups -type f | wc -l → 90   # ≥1 PASS
```
백업 트리: `.moai-backups/20260709T160958/{CLAUDE.md, .claude/settings.json, .claude/rules/moai/**, .moai/config/sections/**}`.

AC-MV2-004f (#63028 안내 — NET-NEW):
```
$ grep -rn '63028' plugins/moai/ | wc -l → 1
plugins/moai/scripts/scaffold.sh:176:Note (issue #63028): In the first cloud/web session ...
```

AC-MV2-004g (/moai:project 배선 — NET-NEW):
```
$ grep -rn 'scaffold.sh' plugins/moai/skills/ | wc -l → 2
plugins/moai/skills/moai-workflow-project/SKILL.md:59:### Layer-2 Scaffolding (scaffold.sh)
plugins/moai/skills/moai-workflow-project/SKILL.md:64:"${CLAUDE_PLUGIN_ROOT}/scripts/scaffold.sh" <target-dir>
```

scaffold.sh 토큰 세트: `{{PROJECT_NAME}}`, `{{VERSION}}`, `{{DATE}}`, `{{PROJECT_USER_NAME}}` (4종). settings.json 병합 전략: `jq -s '.[0] * .[1]'` 기존 타겟(`.[0]`) + 템플릿(`.[1]`) deep-merge — 기존 키 보존 + 템플릿 3키 additive (REQ-MV2-014). 결정론적 cp+sed만 사용(REQ-MV2-013, LLM 개별 파일 복사 금지). MX 태그: `@MX:ANCHOR`(토큰-셋 + 산출-트리 계약), `@MX:WARN`+`@MX:REASON`(settings 보존 병합 + 백업/dry-run/user-owned 보존 구역).

**Baseline-attribution**: 기준선 HEAD 7ff8c5f(M3 완료 후, PM-REDESIGN 병렬 세션 종료 — origin/main 동기 `0 0`). M4 착수 전: `plugins/moai/scripts/` 부재(NET-NEW), `scaffold.sh` skills 언급 0건(NET-NEW), `63028` plugins/moai/ 내 0건(NET-NEW). templates/ 페이로드(CLAUDE.md 321L + rules 61 + settings.project.json + config 27 yaml)는 M2 산출로 존재. M4 후: scaffold.sh 257L 신규(executable, bash -n clean), skills 내 `scaffold.sh` 언급 2건, `63028` 1건.

**Gaps**: 토큰 `{{VERSION}}`은 현재 템플릿에 리터럴로 미존재(design.yaml·go.md·cpp.md에 plain-text "VERSION"만) — scaffold.sh는 4토큰 전부 sed 치환을 수행하므로 VERSION은 no-op로 동작(AC-004c lingering-token grep은 PROJECT_NAME/VERSION/DATE 3종 → 0 유지). Web/원격 세션에서 settings.json 커밋 시 플러그인 자동 활성(T2 열쇠)의 런타임 검증은 P0-w(사용자 수행, §E Out of Scope) 대기. issue #63028 안내 문구의 실제 효과(재접속 시 inactive → active 전환)는 사용자 실측 귀속.

**Residual-risk**: scaffold.sh는 jq에 의존(merge 모드) — jq 미설치 환경에서는 exit 1(명시적 에러). macOS bash 3.2 호환(associative array 미사용). `sed_safely` 이스케이프(`\`·`&`·`|`)는 일반적인 프로젝트명/버전/날짜/사용자명에 충분하나, 토큰 값에 제어문자나 개행이 포함된 극단적 케이스는 미커버(현실적 사용 범위 외). dry-run은 jq 체크를 우회하지 않으나(dry-run은 jq 사용 안 함 → exit 0 보장).

### M5 — 참조 갱신 (moai-coder → moai 스윕 + www 카탈로그 + README 4-plugin 토폴로지 + 재설치 공지)

스코프: live tree 한정 리터럴 치환(`moai-coder`→`moai` 31건/12파일 + harness 1건) + www 카탈로그(`moai-code`→`moai` 17건/5파일 + install-id `moai@moai-claude` NET-NEW) + 루트 README 4-plugin 토폴로지 재작성 + `plugins/moai/README.md` 재설치 공지(NET-NEW) + 13 parity 커맨드 `Skill("moai")`→`Skill("moai:moai")` 정규화(SHOULD). C-1 행위보존: PM-REDESIGN v0.3.0 본문은 리터럴 치환만(재작성 금지). C-5 자기참조 트랩: `.moai/**`·CHANGELOG·agent-memory 스윕 제외.

파일별 스윕 전후(`moai-coder` hit 수):
| 파일 | before | after |
|------|--------|-------|
| plugins/moai/README.md | 5 | 0 |
| plugins/moai/commands/claude-agentic-coding.md | 2 | 0 |
| plugins/moai-pm/README.md | 2 | 0 |
| plugins/moai-pm/skills/project/SKILL.md | 3 | 0 |
| plugins/moai-pm/skills/project/references/core/router.md | 1 | 0 |
| plugins/moai-pm/skills/project/references/core/INDEX.md | 1 | 0 |
| plugins/moai-pm/skills/project/references/core/coder-setup.md | 3 | 0 |
| plugins/moai-pm/skills/project/references/core/diagnostic-protocol.md | 1 | 0 |
| plugins/moai-pm/skills/project/references/core/init-protocol.md | 10 | 0 |
| plugins/moai-designer/skills/moai-domain-copywriting/SKILL.md | 1 | 0 |
| plugins/moai-designer/skills/moai-workflow-gan-loop/SKILL.md | 1 | 0 |
| .claude/agents/harness/harness-builder-skill-builder-specialist.md | 1 | 0 |
| **plugins/ + harness 합계** | **31** | **0** |

AC-MV2-005a (plugins moai-coder 소거 — REMOVAL):
```
$ grep -rn 'moai-coder' plugins/ --include='*.md' --include='*.json' --include='*.sh' --include='*.yaml' | wc -l → 0
```

AC-MV2-005b (www 카탈로그 — REMOVAL + NET-NEW):
```
$ grep -rEn 'moai-code\b|moai-coder\b' www/content/plugins/ | wc -l → 0
$ grep -rn 'moai@moai-claude' www/content/plugins/ | wc -l → 1
```
www `moai-cowork`·`moai-design`·`moai-story` 타 플러그인 명칭은 OUT OF SCOPE(spec §E P4)로 미변경 보존.

AC-MV2-005c (루트 README 4-plugin 토폴로지 — REMOVAL + NET-NEW):
```
$ grep -cE 'moai-cowork\b|moai-code\b|moai-design\b|moai-coder\b' README.md → 0
$ grep -c 'moai-coworker' README.md → 3
$ grep -c 'moai-designer' README.md → 3
$ grep -c 'moai-pm' README.md → 3
$ grep -c 'moai@moai-claude' README.md → 1
```

AC-MV2-005d (재설치 공지 — NET-NEW):
```
$ grep -c '재설치' plugins/moai/README.md → 1
```
공지 문구는 `moai-coder` 리터럴을 포함하지 않음(AC-005a 회귀 방지) — "개명 전 이름" 우회 표현.

AC-MV2-005e (harness + claude-plugin — REMOVAL):
```
$ grep -rn 'plugins/moai-coder' .claude/agents/harness/ | wc -l → 0
$ grep -rn 'moai-coder' .claude-plugin/ | wc -l → 0   (M1에서 이미 clean, 회귀 가드)
```

AC-MV2-005f (Skill 자기참조 정규화 — NET-NEW SHOULD):
```
$ grep -l 'Skill("moai:moai")' plugins/moai/commands/*.md | wc -l → 13
$ grep -l 'Skill("moai")' plugins/moai/commands/*.md | wc -l → 0   (잔여 bare 참조 0)
```
13 parity 커맨드(plan/run/sync/project/fix/loop/clean/mx/review/codemaps/gate/harness/feedback) 전부 정규화 — T3 공존 저장소에서 결정론적 자기참조 보장. debt 없음(SHOULD 달성).

최종 live-tree 가드:
```
$ grep -rn 'moai-coder' plugins/ README.md www/content/plugins/ .claude/agents/harness/ --include='*.md' --include='*.json' --include='*.sh' --include='*.yaml' | wc -l → 0
```

**Baseline-attribution**: 기준선 HEAD 21fb72c(M4 scaffold.sh 완료, PM-REDESIGN 병렬 세션 종료 — sync 3dfcc42, origin/main 동기 `0 0`). M5 착수 전 HEAD 실측: plugins `moai-coder` 30건/11파일 + harness 1건, www `moai-code\b|moai-coder\b` 17건/5파일 + `moai@moai-claude` 0건, README 구명칭 5건, `재설치` 0건, `Skill("moai:moai")` 0건, `.claude-plugin/ moai-coder` 0건(M1 clean). M5 후: 전 predicate 예상 방향 이동(REMOVAL N→0, NET-NEW 0→≥1).

**Gaps**: www 타 플러그인 구명칭(`moai-cowork`·`moai-design`·`moai-story` → `moai-coworker`·`moai-designer` 등) 정정은 spec §E P4 OUT OF SCOPE — 본 M5는 `moai-code`/`moai-coder` 한정. PM-REDESIGN 파일 내 "(구 moai-coder)"→"(구 moai)" 등 역사 주석의 리터럴 치환 결과가 맥락상 다소 중복적("구 moai")이나 C-1(본문 재작성 금지) 우선 — 편집 보정은 후속 SPEC 소관. P0-8 typed-name 충돌 런타임 실측은 M6 소관(AC-MV2-006c).

**Residual-risk**: 재설치 공지가 `moai-coder` 리터럴을 회피하므로 과거 이름을 모르는 신규 사용자에게 맥락이 다소 추상적일 수 있음(개명 전 사용자층은 맥락 파악 가능). www `code/_index.md`의 GitHub 소스 경로(`plugins/moai-code/`→`plugins/moai/`)가 M1 개명과 정합하게 됐으나, 원격 GitHub 링크의 실제 경로 존재 여부는 push 후 원격 반영에 의존(본 저장소 로컬 경로는 정합). Hugo 빌드·link-check 회귀는 M6(AC-MV2-006d)에서 최종 검증.

### M6 — 검증 + P0-8 typed-name 실측 (AC-MV2-006a·b·c·d)

AC-MV2-006a (plugin validate — RUNTIME, REQ-MV2-022):
```
$ claude plugin validate ./plugins/moai; echo exit=$?
✔ Validation passed with warnings
exit=0
```
12개 커맨드(gate/fix/loop/codemaps/project/clean/mx/sync/run/plan/review/feedback) frontmatter 미비 경고(비엄격 → 경고만, MUST exit 0 만족).
```
$ claude plugin validate --strict ./plugins/moai; echo exit=$?
✘ Validation failed (--strict treats warnings as errors)
exit=1
```
EC-5 해당: `--strict`는 위 12건 frontmatter 경고를 오류로 취급 → exit 1. 비엄격 exit 0이 MUST AC이므로 AC-MV2-006a PASS; strict exit 1은 SHOULD 미달 → debt 기록(debt-1, 아래 Gaps).

AC-MV2-006b (marketplace validate — PRESERVE 회귀 가드, REQ-MV2-022):
```
$ claude plugin validate .claude-plugin/marketplace.json; echo exit=$?
✔ Validation passed with warnings
exit=0
```
3건 경고(metadata.language·license 미인식 필드 + moai-pm version 0.2.0 vs plugin.json 0.3.0 불일치). HEAD에서 이미 PASS 상태 유지 → 회귀 없음, PRESERVE 가드 만족.

AC-MV2-006c (P0-8 typed-name 충돌 실측 — RUNTIME+NET-NEW, REQ-MV2-021):

P0-8-verdict: indeterminate at probe layer — typed-name `moai` is shared by the project namespace (`.claude/commands/moai/` = 13 commands, exposed as `/moai:<cmd>`) AND the plugin namespace (`plugins/moai/commands/` = 14 commands for plugin name `moai`, exposed as `/moai:<cmd>`); 13 command names intersect (clean/codemaps/feedback/fix/gate/harness/loop/mx/plan/project/review/run/sync) so the typed name `/moai:plan` (and 12 siblings) is genuinely colliding. In THIS repo the `moai` plugin is declared in `.claude-plugin/marketplace.json` but NOT enabled (`enabledPlugins: null` in both settings.json and settings.local.json) and NOT installed at user scope (`claude plugin list` shows only gopls/pyright/rust-analyzer/swift LSP plugins), so only the project command is active at runtime here. The `claude -p '/moai:plan ...'` print-mode probe did not observably resolve slash-command dispatch (print mode emitted only permission/connector warnings, no command resolution surface); runtime precedence when BOTH project + plugin commands are active depends on Claude Code's project-vs-plugin resolution order which this probe could not mechanically disambiguate. Deactivation-guidance UI is P3 OUT OF SCOPE (spec §E) — recording the verdict is the M6 deliverable, not the UI.

관찰 증거(verbatim):
```
$ find .claude/commands/moai -maxdepth 1 -name '*.md' | wc -l → 13   (project namespace)
$ find plugins/moai/commands   -maxdepth 1 -name '*.md' | wc -l → 14   (plugin namespace; 14th = claude-agentic-coding)
$ comm -12 <project-cmds> <plugin-cmds>   → 13 공유 이름 (clean codemaps feedback fix gate harness loop mx plan project review run sync)
$ jq '.enabledPlugins' .claude/settings.json        → null   (플러그인 미활성)
$ jq '.enabledPlugins' .claude/settings.local.json  → null
$ claude plugin list                                 → moai 미포함 (user-scope gopls/pyright/rust/swift-lsp만)
$ head -1 plugins/moai/commands/plan.md             → <!-- parity-source: internal/template/templates/.claude/commands/moai/plan.md.tmpl @ b8354304c -->
$ head -1 .claude/commands/moai/plan.md             → ---   (프로젝트 직접 파일, frontmatter 시작)
$ echo '/moai:plan probe-p0-8' | timeout 45 claude -p --dangerously-skip-permissions
  ⚠ Permission mode forced to default ... ⚠ claude.ai connectors are disabled ...
  (print mode가 slash-command dispatch를 관측 가능하게 분해하지 못함 — runtime 우선순위 비결정적)
```

AC-MV2-006d (bash -n + hugo + link-check — PRESERVE 회귀 가드, REQ-MV2-022):
```
$ find plugins/moai -name '*.sh' -exec bash -n {} +; echo exit=$?
exit=0
```
7개 셸 스크립트 전수 합격(dispatch.sh + gates/ 5종[gateguard-fact-force, iggda-audit-preservation-guard, status-transition-ownership, sync-phase-quality-gate, team-ac-verify] + scripts/scaffold.sh).
```
$ (cd www && hugo --gc --minify); echo exit=$?
 Pages 228 | Static files 252 | Aliases 65   Total in 376 ms
hugo_exit=0
```
www 회귀 없음 — Hugo 빌드 정상(M5 www/content/plugins/** 수정 후에도 228 페이지 정상 생성).
```
$ node www/scripts/check-links.mjs; echo exit=$?
Scanned 241 HTML files, 31872 internal <a> links
broken internal links: 10
  cookbook/index.html -> ./track-marketing/
  cookbook/index.html -> ./track-documents/
  cookbook/index.html -> ./track-data/
  cookbook/tracks/track-marketing/index.html -> ./skill-chaining/
  cookbook/tracks/track-marketing/index.html -> ./blog-pipeline/
  tags/cookbook/page/2/index.html -> ../../cowork/troubleshooting/
  tags/cookbook/page/2/index.html -> ../../cowork/constraints/
  tags/cookbook/page/2/index.html -> ../skill-chaining/
  tags/cookbook/page/2/index.html -> ../../cowork/faq/
  tags/troubleshooting/index.html -> ../skill-chaining/
linkcheck_exit=1
```
MUST exit 0 미달 → **blocker (AC-006d link-check)**. 단, 기원 분석 결과 본 실패는 **pre-existing 부채**이며 본 SPEC 회귀가 아님:
```
$ git log --oneline 6f92d86..HEAD -- 'www/content/cookbook/**' 'www/content/tags/**' 'www/content/cowork/**'   → (empty — 본 SPEC run-phase가 해당 디렉토리 미수정)
$ git show 6f92d86:www/content/cookbook/_index.md | grep 'track-marketing\|track-documents\|track-data'
  99:- [마케팅 트랙](./track-marketing/) — 브랜딩·SEO·캠페인 8주
  100:- [문서 트랙](./track-documents/) — Office 산출물 자동화 8주
  101:- [데이터 트랙](./track-data/) — 분석·공공데이터 8주
```
10건 broken link는 전부 `cookbook/`·`tags/`·`cowork/` 영역(누락된 트랙/스킬 페이지)이며 M5가 수정한 `www/content/plugins/**` 외. 사전 run-phase 기준선(6f92d86)에 이미 동일 broken link 존재 → §D.6 "PASS (HEAD 추정 — pre-flight 재확인)"의 추정이 빗나간 사례 (실측 FAIL). 본 SPEC 스코프(plugins/) 밖 미해결 부채 — blocker 보고, orchestrator 최종 DoD 판단 대상.

**Baseline-attribution**: 기준선 HEAD 5037668(M5 완료, == origin/main, sync `0 0`). M6는 검증 전용(production 파일 수정 없음 — progress.md §E.2 기록이 유일 산출물). 사전 실측: `^P0-8-verdict:` 센티넬 §E.2 내 0건(NET-NEW), `claude plugin validate ./plugins/moai` 경로 존재(M1 개명 후). M6 후: non-strict validate exit 0(006a PASS), marketplace exit 0(006b PRESERVE), bash -n exit 0(006d PASS), hugo exit 0(006d PASS), link-check exit 1(006d pre-existing FAIL — blocker), `^P0-8-verdict:` 센티넬 §E.2 내 ≥1(006c NET-NEW 달성).

**Gaps**: (debt-1) `--strict` validate exit 1 — 12개 커맨드 파일의 YAML frontmatter 미비(EC-5 문서화된 SHOULD 미달; 비엄격 MUST는 PASS). 커맨드 frontmatter는 parity-source 주석 라인이 파일 최상단에 위치하여 `---` 블록이 첫 줄이 아닌 구조적 배치 — 후속 SPEC에서 frontmatter 우선순위 조정 가능. (blocker-1) link-check exit 1 — 10건 pre-existing broken link(cookbook/tags/cowork, 트랙·스킬 페이지 미작성). 본 SPEC 스코프(plugins/) 밖 → M6 검증 전용 스코프에서 수정 불가(scope 확장 금지, §D Constraints). orchestrator 최종 DoD에서 PASS-WITH-DEBT 판정 또는 별도 후속 SPEC 필요. (P0-8) runtime typed-name 우선순위 비결정적 — probe 층에서 분해 불가, 구조적 충돌(13 공유 이름)+enablement 실측(플러그인 미활성)만 확정.

**Residual-risk**: P0-8 verdict가 비결정적이므로, 향후 사용자가 `moai` 플러그인을 활성화(`enabledPlugins["moai@moai-claude"]=true`)하면 project `/moai:plan` vs plugin `/moai:plan` 중 어느 것이 선행하는지 runtime 검증이 별도 필요(안내 문구 구현은 P3). link-check 10건은 본 SPEC과 무관한 cookbook/cowork 콘텐츠 누락이나, DoD §D.4.1의 literal "AC-006d 전부 PASS" 요건과 충돌 → 최종 DoD check에서 pre-existing-debt-out-of-scope 인정 여부가 관건. `--strict` frontmatter 경고는 향후 커맨드 재구조 시 해소 가능.

## §E.3 Run-phase Audit-Ready Signal

```yaml
run_status: complete
run_complete_at: 2026-07-09T08:30:13Z
run_audit: "M1-M6 전 마일스톤 완료 + orchestrator 독립 재실측 6/6 PASS. AC-MV2-001a~005f 전 PASS; AC-006a/b/c PASS; AC-006d bash -n + hugo(228p) PASS, link-check PASS-WITH-DEBT (pre-existing cookbook/cowork/tags 부채 10건 — 본 SPEC 회귀 아님, git log 6f92d86..HEAD 미수정 입증). P0-8-verdict: probe 층 비결정적 정직 기록 (AC-006c 만족)."
run_debt:
  - "AC-006d link-check pre-existing (cookbook/cowork 콘텐츠 누락) — spec §E P4 Out-of-Scope 별도 SPEC"
  - "--strict validate exit 1 (EC-5, 12 커맨드 frontmatter 미비) — 후속 frontmatter 우선순위 SPEC"
  - "P0-8 typed-name 충돌 안내 문구 미구현 — P3 Out-of-Scope"
run_commits: ["56f9e09 M1 rename", "ad86a50 M2 two-layer", "7ff8c5f M3 hook consolidation", "21fb72c M4 scaffold", "5037668 M5 reference sweep", "6e0ccdc M6 verification+P0-8"]
parallel_session_absorbed: "SPEC-MOC-PM-REDESIGN-001 3-phase closed during run (moai-pm v0.3.0); M5 moai-pm 참조 갱신은 PM 재설계 결과 위에 치환-only 적용 (C-1)"
```

## §E.4 Sync-phase Audit-Ready Signal

```yaml
sync_status: complete
sync_complete_at: 2026-07-09T09:05:00Z
sync_commit_sha: 8cc0989c4872342c3d783245d2f5fa0700a21bd0
sync_audit: "CHANGELOG [Unreleased] + frontmatter completed (3-phase close in-progress→implemented→completed on single sync commit) + spec/plan/acceptance body untouched. link-check PASS-WITH-DEBT (10 pre-existing cookbook/cowork/tags — not a regression, git log 6f92d86..HEAD zero edits to those dirs). --strict EC-5 debt (12 command frontmatter gaps). P0-8 typed-name deactivation-guidance UI P3 out-of-scope."
frontmatter_status_transitions:
  spec_md: "in-progress -> completed (single sync commit, 3-phase close)"
  plan_md: "no frontmatter (markdown-only artifact)"
  acceptance_md: "no frontmatter (markdown-only artifact)"
  progress_md: "no frontmatter (markdown-only artifact)"
canary_compliance_check:
  changelog_entry_position: "top of [Unreleased] (newest SPEC entry)"
  duplicate_guard_grep: "grep -c 'SPEC-MOC-PLUGIN-MOAI-V2-001' CHANGELOG.md == 1 (pre-emit 0 -> post-emit 1)"
  ac_count_ssot: "32 AC rows in acceptance.md (001a-d=4, 002a-f=6, 003a-e=5, 004a-g=7, 005a-f=6, 006a-d=4)"
b12_self_test_a: "pre-emission grep returned 0 (no duplicate) — PASS"
b12_self_test_b: "AC count 32 matches acceptance.md SSOT — PASS"
b12_self_test_c: "all claimed file paths verified via ls/jq/find on main checkout — PASS"
```
