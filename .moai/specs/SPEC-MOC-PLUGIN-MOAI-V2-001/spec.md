---
id: SPEC-MOC-PLUGIN-MOAI-V2-001
title: "moai 플러그인 v2 — 개명(moai-coder→moai) + 2계층 재구조화 + 스캐폴드 완성"
version: "0.1.3"
status: completed
created: 2026-07-09
updated: 2026-07-09
author: Goos Kim
priority: P1
phase: "plugin-v2 P2 (rename + restructure + scaffold)"
module: "plugins/moai"
lifecycle: spec-anchored
tags: "moai, plugin, rename, two-layer, scaffold, hooks-dispatch, marketplace, web-tier, korean"
related_specs: [SPEC-MOC-BOOTSTRAP-DESKTOP-001, SPEC-MOC-PLUGIN-REMEDIATION-001]
tier: L
---

# SPEC-MOC-PLUGIN-MOAI-V2-001 — moai 플러그인 v2 (개명 + 2계층 재구조화 + 스캐폴드 완성)

## HISTORY

- **2026-07-09** 최초 작성 (manager-spec, plan-phase iteration 1, Tier L, 5-artifact). 설계 정본 `design-moai-plugin-v2-2026-07-08.md`(D-1~D-5 사용자 확정)와 v1 보고서(템플릿 인벤토리·P0-1~5 실측 정본)를 원천으로 v2 로드맵 **P2 단계(본 저장소 소관분)** 를 SPEC화. 설계 문서의 수치를 신뢰하지 않고 HEAD를 직접 실측(research.md §E): plugin.json `{name: "moai-coder", version: "3.1.0"}`, rules 61파일(플러그인 루트 — P0-1 FAIL 죽은 페이로드), output-styles 2파일(einstein.md·moai.md, frontmatter `name: MoAI` — 설계 문서의 "3종"과 상이, moai-easy.md는 vendor 미포함), hooks = hooks.json(20 이벤트) + 스크립트 24종(handle-* 21 + 순수 bash 게이트 4), commands 14(파리티 13 + claude-agentic-coding 1), agents 8, skills 팩 32, `templates/`·`scripts/` 부재, 잔존 `moai-coder` 참조 = plugins/ 34곳(11파일) + marketplace.json 2곳 + .claude/agents/harness/ 1곳 + www/content/plugins/ 12곳(`moai-code` 구명칭). git 전략은 사용자 확정: **main 직접 푸시(Hybrid Trunk)** — Tier L 기본 PR 라우팅 명시적 override(plan.md §D). SPEC ID 정규 regex 통과(`SPEC | MOC | PLUGIN | MOAI | V2 | 001 → PASS`).
- **2026-07-09** plan-phase iteration 1.1 (manager-spec, DP 해소 반영). 사용자 확정 2건 반영: **DP-1 = `"1.0.0"` 리셋**(제시 3옵션 외 사용자 override — 개명 = 마켓플레이스 신규 플러그인 정체성 → clean-slate 버저닝; v2 §9.4 "ADK SSOT 재정렬"안 대체. REQ-MV2-001·§A.2·AC-MV2-001b 리터럴·§D.1 시나리오 1·EC-4·design §G 갱신), **DP-2 = ① gateguard-fact-force vendor 채택**(SPEC 기본값 확인, REQ-MV2-009 SHOULD 등급 유지 — plan.md §H RESOLVED 표기). frontmatter 0.1.0→0.1.1.
- **2026-07-09** re-baseline census to HEAD `6f92d86` (parallel-session race absorbed — 커밋 "fix(plugins): 스킬 감사 14건 처리", plugins/ 80파일). 전 census 명령 재실측: `moai-coder` 참조 plugins/ **35곳/12파일**(+moai-pm `diagnostic-protocol.md` 신규), moai-designer `agents/` 디렉토리 제거(coder agents 8 무영향), www plugins 구명칭 **17곳**(최초 12는 2파일만 합산한 census 결함 — chat 3·cowork 1·design 1 추가 발견), 루트 README 정확 **5곳**. 최초 census 계수 결함 2건 동시 정정: skills 팩 **29**(32는 ls alias 아티팩트 — `moai` 팩 포함 find 재실측), handle-* **20**(21은 오계수; 총 .sh 24 = 20 + 게이트 4). plugin.json(moai-coder/3.1.0)·marketplace(4종/5.0.0)·commands 14·agents 8·rules 61·output-styles 2·이벤트 20·validate PASS ×2·총 354파일 등 잔여 기준선 불변 확인. AC-MV2-001d/005a/005b/005c·§D.6·plan M3/M5·research §E 갱신. frontmatter 0.1.1→0.1.2.
- **2026-07-09** plan-phase iteration 1.2 (manager-spec, plan-audit iter-1 FAIL 0.88 — 6결함 전부 해소). **D1(major)**: progress.md §E.2 placeholder가 센티넬 리터럴 `P0-8-verdict:`를 포함해 AC-MV2-006c baseline이 1로 자기통과 → placeholder에서 리터럴 제거 + predicate 행 선두 `^` 앵커 이중 방어 + REQ-MV2-021에 line-anchored 명문화 + §D.6 행/요약 재실측 복원. **D2(major)**: EC-6의 `claude.mo.ai.kr`=0 서브-predicate가 오전제(루트 CLAUDE.md 실측 0회)로 vacuous → 철회하고 ADK 원천 경로 명시 parity-source 마커(`parity-source: internal/template/templates/CLAUDE.md`)를 유일 기계 판별자로 격상(루트 parity-source 0 실측 — naive 복사 판별 성립). **D3(major)**: plan M5 www 스코프 2/5파일 → 5파일 전부 열거. **D4(minor)**: REQ-MV2-015/019/021에 GEARS `shall` 키워드 삽입, REQ-MV2-020은 SHOULD 등급 정합으로 `should`로 정렬. **D5(minor)**: §D.6 CLAUDE_CODE_REMOTE 행 스코프를 dispatch.sh 한정으로 정정(플러그인 전체는 문서 참조 1건 병기). **D6(minor)**: AC-MV2-004c를 3-토큰 스칼라 predicate(`grep -rlE + wc -l`)로 재작성. frontmatter 0.1.2→0.1.3.

---

## §A. 배경 및 목적 (Background)

### A.1 비즈니스 맥락

`plugins/moai-coder`(v3.1.0)는 MoAI-ADK 방법론의 무설치 포트 1차 구현이다. 2026-07-08 확정된 v2 설계(D-1~D-5)는 다음을 요구한다:

1. **D-1 개명**: `moai-coder` → `moai`. 커맨드 네임스페이스 `/moai:plan`이 moai-adk-go 템플릿 UX와 완전 파리티가 되고, 브랜딩은 `displayName: "코더"`로 유지된다(name=네임스페이스, displayName=UI 표기 분리).
2. **D-2 Slim-Scaffold 2계층**: Claude Code가 플러그인에서 로드하는 것(commands·agents·skills·hooks·output-styles·.mcp.json)은 플러그인 네이티브(Layer 1)에, 프로젝트에 있어야만 효력이 생기는 것(CLAUDE.md·rules·settings·`.moai` 골격)은 `templates/` 스캐폴드 페이로드(Layer 2)에 배치한다. 현행 플러그인 루트의 rules 61파일은 **P0-1 실측 FAIL(미로드 죽은 페이로드)** 로 확정되어 Layer 2로 이동해야 한다. output-styles는 **P0-2 실측 PASS(네임스페이스 셀렉터 `moai:MoAI` 필수)** 로 Layer 1 잔류가 확정되었다.
3. **Web 지원의 열쇠 = repo 커밋**: Web(claude.ai/code·Desktop 원격)은 repo에 커밋된 `.claude/settings.json` 선언(`extraKnownMarketplaces` + `enabledPlugins`)만 인식한다. 따라서 스캐폴드가 프로젝트 settings.json에 이 선언을 **보존 병합**하는 것이 T2 티어(CLI·Desktop·Web 전부 도달)의 신규 핵심 책무다.

### A.2 현재 상태 실측 요약 (Ground-Truth, 2026-07-09)

전체 실측 데이터는 research.md §E가 정본이다. SPEC 판단에 직결되는 핵심:

- 플러그인 루트에 `rules/moai/` 61파일 존재(죽은 페이로드), `templates/`·`scripts/` 부재, 스캐폴드 스크립트·`63028` 안내·`재설치` 공지 전부 부재(각 grep 0).
- hooks: `hooks.json` 20 이벤트가 24개 개별 스크립트로 분산(handle-* 20 + 게이트 4: iggda-audit-preservation-guard·status-transition-ownership·sync-phase-quality-gate·team-ac-verify). `dispatch.sh`·`$CLAUDE_CODE_REMOTE` 분기 부재.
- 참조 오염(HEAD `6f92d86` 재기준선): `moai-coder` 리터럴이 plugins/ 35곳(12파일), marketplace.json 2곳, `.claude/agents/harness/harness-builder-skill-builder-specialist.md` 1곳. www plugins 카탈로그는 구명칭(`moai-code` 위주)을 17곳에서 사용(G7 — _index 4·code 8·chat 3·cowork 1·design 1). 루트 README는 구 토폴로지(moai-cowork/moai-code/moai-design) 5곳(stale).
- 본 저장소 자체가 T3 프로젝트(`.claude/commands/moai/` 13 + `.claude/skills/moai` 보유) → P0-8(typed-name 충돌 실측)의 자연 테스트베드.
- ADK 버전 SSOT: `moai-adk-go/pkg/version/version.go` = `v3.0.0-rc8`(2026-07-09 실측). 플러그인 버전은 ADK 정규화값이 아닌 **`"1.0.0"` 리셋**으로 사용자 확정(DP-1 RESOLVED 2026-07-09 — plan.md §H).

### A.3 목표 (Goals)

1. `plugins/moai-coder/` → `plugins/moai/` 개명 마이그레이션 완료(plugin.json·marketplace.json 갱신, 톰스톤 없음, 재설치 공지).
2. 2계층 재구조화: rules 61 → `templates/claude/rules/moai/`, CLAUDE.md·settings.project.json·`.moai` 골격을 `templates/`에 배치, output-styles는 플러그인 네이티브 유지.
3. 훅 통합: 24 스크립트 → 단일 `hooks/dispatch.sh` + `hooks/gates/` 순수 bash 게이트, `$CLAUDE_CODE_REMOTE` 분기, fail-open 보존.
4. `scripts/scaffold.sh` + `/moai:project` 완성: 결정론적 스캐폴드(cp+sed 토큰 치환, `--dry-run`, 백업, user-owned 보존) + 프로젝트 settings.json 보존 병합(Web 활성화 열쇠 3키) + 첫 세션 불안정(#63028) 안내.
5. 참조 갱신: moai-pm 라우터, 4-README + 루트 README, www 카탈로그(plugins 섹션 한정), 커맨드 `Skill("moai")` 정규화(SHOULD).
6. 검증: P0-8 typed-name 충돌 실측 기록 + `claude plugin validate` 기계 검증.

본 작업은 **행위 보존 재구조화**(파일 이동/개명 + 참조 갱신)가 지배적이므로 run-phase는 `cycle_type=ddd`(ANALYZE-PRESERVE-IMPROVE)로 수행하며, characterization은 grep/ls/jq 인벤토리 패리티 검사로 구성한다(acceptance.md §D.0).

---

## §B. GEARS 요구사항 (Requirements)

> 표기: GEARS(현행). `<subject>`는 일반화됨(the plugin manifest / the marketplace catalog / the dispatcher / the scaffold script 등). **shall / When / While / Where**는 GEARS 키워드.

### R1 — 개명 마이그레이션 (moai-coder → moai)

- **REQ-MV2-001 (Ubiquitous).** The plugin tree shall reside at `plugins/moai/` with the manifest `plugins/moai/.claude-plugin/plugin.json` declaring `{"name": "moai", "displayName": "코더"}`, and the `version` field reset to the literal `"1.0.0"`(DP-1 사용자 확정 2026-07-09: 개명 = 마켓플레이스 신규 플러그인 정체성 → clean-slate 버저닝 — plan.md §H). 잔존 `plugins/moai-coder/` 트리는 존재하지 않아야 한다.
- **REQ-MV2-002 (Ubiquitous).** The marketplace catalog(`.claude-plugin/marketplace.json`) shall list the plugin entry as `{"name": "moai", "source": "./plugins/moai"}` (displayName `코더`·category 유지), keeping the 4-plugin family count.
- **REQ-MV2-003 (Unwanted).** The marketplace catalog shall **not** retain a `moai-coder` tombstone entry(카탈로그 오염 방지 — v2 §9.2).
- **REQ-MV2-004 (Event-driven).** **When** the rename lands, the plugin `README.md` shall carry a 1회성 **재설치 공지**(구 moai-coder 설치자는 자동 마이그레이션 없음 — 리터럴 `재설치` 포함, R8 완화).

### R2 — 2계층 재구조화 (Layer 1 / Layer 2)

- **REQ-MV2-005 (Ubiquitous).** The 61 rules files shall move from the plugin root `rules/moai/` to the scaffold payload `templates/claude/rules/moai/` **content-intact**(이동 전후 내용 무변경 — P0-1 FAIL 근거). The plugin root shall **not** retain a `rules/` directory.
- **REQ-MV2-006 (Ubiquitous).** The output-styles(현행 2파일: `einstein.md`·`moai.md`, frontmatter `name: MoAI`) shall remain plugin-native at `output-styles/`(P0-2 PASS 근거 — 스타일 본문 갱신이 마켓 업데이트로 즉시 전파).
- **REQ-MV2-007 (Ubiquitous).** The scaffold payload `templates/` shall contain at minimum: (a) `templates/CLAUDE.md` — ADK 템플릿 정본(`moai-adk-go internal/template/templates/CLAUDE.md`) 유래 + parity-source 프로버넌스 마커, **본 저장소 루트 CLAUDE.md 복사 금지**(acceptance.md EC-6); (b) `templates/claude/settings.project.json` — `"outputStyle": "moai:MoAI"` + `extraKnownMarketplaces`(`moai-claude` → github `modu-ai/claude`) + `enabledPlugins`(`"moai@moai-claude": true`) 선언 포함(Web 활성화 열쇠); (c) `templates/moai/config/sections/` — `.moai` 골격 config yaml ≥27종(프로젝트 가변값은 `{{TOKEN}}` 단순 토큰 형태).
- **REQ-MV2-008 (Unwanted).** The restructure shall **not** alter the Layer 1 inventory: commands 14 · agents 8 · skills 팩 29 · `.mcp.json`은 개명 전 인벤토리와 동일하게 보존된다(PRESERVE characterization — acceptance.md AC-MV2-001d, 기준선 HEAD `6f92d86`).

### R3 — 훅 통합 (dispatch.sh)

- **REQ-MV2-009 (Ubiquitous).** The hooks shall consolidate to a single dispatcher `hooks/dispatch.sh`: `hooks.json`의 모든 이벤트 command가 `${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.sh <event>`를 가리키고, 기존 handle-* 20 스크립트는 제거된다. 순수 bash 게이트 4종(iggda-audit-preservation-guard·status-transition-ownership·sync-phase-quality-gate·team-ac-verify)은 `hooks/gates/`로 이관되며, (SHOULD) ADK 템플릿의 `gateguard-fact-force.sh`를 5번째 게이트로 vendor한다.
- **REQ-MV2-010 (Event-driven).** **When** dispatch.sh receives an event, it shall: ① `moai` 바이너리 감지 성공 시 `exec moai hook <event>`(T3 자동 활성) ② 부재 시 이벤트에 매핑된 `hooks/gates/` 게이트 실행 ③ 매핑 없음 시 `exit 0`(무음 fail-open).
- **REQ-MV2-011 (Capability gate).** **Where** `$CLAUDE_CODE_REMOTE` is `true`(Web/원격 세션), dispatch.sh shall skip the binary probe entirely and enter gate-only mode(바이너리 설치 불가 확정 환경의 PATH 프로브 낭비 제거). 외부 호출 게이트는 네트워크 egress 정책 하에서 fail-open.
- **REQ-MV2-012 (Unwanted).** The hooks shall **not** block user flow on any failure path: 모든 종료 경로는 `exit 0`이며, `hooks.json`의 이벤트 집합(20종)은 통합 전과 동일하게 보존된다(PRESERVE).

### R4 — scaffold.sh + /moai:project 완성

- **REQ-MV2-013 (Ubiquitous).** The scaffold script `scripts/scaffold.sh` shall generate the Layer 2 payload deterministically: cp + sed 단순 토큰 치환(`{{PROJECT_NAME}}`·`{{VERSION}}`·`{{DATE}}` 수준), `--dry-run` 지원(파일 무기록 + 생성 계획 출력), 기존 파일은 `.moai-backups/`로 백업 후 갱신, user-owned 네임스페이스(`harness-*`, `agents/local/` 등) 절대 보존. LLM의 개별 파일 복사는 사용하지 않는다.
- **REQ-MV2-014 (Event-driven).** **When** scaffold.sh writes the project `.claude/settings.json`, it shall **preserve-merge**(기존 사용자 키 보존, 덮어쓰기 금지) the following three keys: `"outputStyle": "moai:MoAI"`, `extraKnownMarketplaces.moai-claude`, `enabledPlugins."moai@moai-claude": true`.
- **REQ-MV2-015 (Ubiquitous).** The `/moai:project` workflow(플러그인 `moai` 스킬의 project 워크플로우) shall wire a single scaffold.sh invocation(scaffold.sh 1회 실행 배선 — 스킬 본문에 scaffold.sh 호출 경로 명시).
- **REQ-MV2-016 (Event-driven).** **When** the scaffold completes, the completion message shall include the Web 첫 세션 불안정 안내(issue `#63028`: 마켓 clone이 세션 시작을 앞지르지 못하면 첫 클라우드 세션에서 inactive → 재접속 시 정상 — 리터럴 `63028` 포함).

### R5 — 참조 갱신

- **REQ-MV2-017 (Ubiquitous).** All live plugin-tree references to `moai-coder` shall update to `moai`: plugins/ 전체(moai-pm 라우터 6파일 · moai-designer 스킬 2파일 · 개명된 플러그인 자체 잔존 참조 포함) + `.claude/agents/harness/harness-builder-skill-builder-specialist.md`의 경로 참조. (역사 기록물 — `.moai/reports/`·`.moai/specs/`·CHANGELOG·agent-memory — 는 갱신 대상이 아니다.)
- **REQ-MV2-018 (Ubiquitous).** The root `README.md` shall describe the current 4-plugin topology(moai · moai-coworker · moai-designer · moai-pm): 구명칭(`moai-cowork`·`moai-code`·`moai-design`·`moai-coder`) 잔존 0.
- **REQ-MV2-019 (Ubiquitous).** The www plugins catalog(`www/content/plugins/**` 한정) shall describe the code plugin by its current name `moai`(설치: `moai@moai-claude`): 구명칭 `moai-code`·`moai-coder` 잔존 0. (www 전면 개편·타 플러그인 명칭 정비는 §E Out of Scope — P4.)
- **REQ-MV2-020 (Ubiquitous, SHOULD).** The 13 parity commands should normalize the skill reference `Skill("moai")` → `Skill("moai:moai")`(충돌 방어 — P0-3 PASS로 MUST가 아닌 SHOULD, 단 본 저장소 같은 T3 공존 프로젝트에서 결정론적 자기 참조를 보장; iter-1 D4 — shall/SHOULD 등급 긴장 해소로 modal을 should로 정렬).

### R6 — 검증

- **REQ-MV2-021 (Event-driven).** **When** run-phase reaches the verification milestone, the run-phase shall perform the P0-8 실측(T3 프로젝트 — 프로젝트 커맨드 `/moai:plan` + 스킬 `moai` — 과 플러그인 `moai:plan`·`moai:moai` 공존 시 typed-name 충돌·우선순위) in this repository, and shall record the result in `progress.md` `## §E.2 Run-phase Evidence` as the **행 선두(line-anchored)** 지정 센티넬 라인 `P0-8-verdict:` (승격 시 비활성 안내 문구 구현은 P3 — §E Out of Scope).
- **REQ-MV2-022 (Ubiquitous).** The renamed plugin shall pass machine validation: `claude plugin validate ./plugins/moai` exit 0(SHOULD: `--strict`), `claude plugin validate .claude-plugin/marketplace.json` exit 0(회귀 가드 — HEAD에서 이미 PASS), 모든 `plugins/moai/**/*.sh`는 `bash -n` clean.

---

## §C. 제약 (Constraints)

- **C-1 행위 보존**: Layer 1 자산(commands·agents·skills·output-styles·.mcp.json)의 내용 변경은 참조 갱신(R5)과 개명에 따른 명칭 치환으로 한정한다. 스킬 본문 리라이트·기능 추가 금지.
- **C-2 단방향 vendor**: `templates/` 페이로드의 정본은 moai-adk-go 임베디드 템플릿이다. 본 SPEC은 수동 vendor(parity-source 마커 스탬프)로 채우며, 자동화(`moai plugin export`)는 P1 소관(Out of Scope). 역방향(플러그인 → 정본) 편집 금지.
- **C-3 fail-open**: 훅의 어떤 경로도 사용자 흐름을 차단하지 않는다(exit 0). 블로킹 훅 도입 금지.
- **C-4 보존 병합**: scaffold의 settings.json 처리는 기존 사용자 설정을 절대 덮어쓰지 않는다.
- **C-5 범위 규율**: `.moai/specs/`·`.moai/reports/`·CHANGELOG·agent-memory 등 역사 기록물의 `moai-coder` 언급은 갱신하지 않는다(자기참조 트랩 — acceptance.md §D.0).
- **C-6 git**: main 직접 푸시(Hybrid Trunk, 사용자 확정). 마일스톤 단위 conventional commit + SPEC ID. force-push 금지.

---

## §D. 성공 기준 (Success Criteria, 요약)

정본은 acceptance.md AC 매트릭스. 요약:

1. 개명 완료: `plugins/moai` 존재 + `plugins/moai-coder` 부재 + manifest/marketplace jq 검증 + 4-plugin 유지 + 톰스톤 0 (AC-MV2-001).
2. 2계층: rules 61 이동(내용 무변경, git rename 검출 100%) + `templates/` 3대 페이로드 + settings.project.json 3키 + output-styles 잔류 (AC-MV2-002).
3. 훅: dispatch.sh + handle-* 0 + 게이트 ≥4 + `CLAUDE_CODE_REMOTE` 분기 + 20 이벤트 보존 (AC-MV2-003).
4. 스캐폴드: scaffold.sh 결정론 생성/dry-run/백업/보존 병합 런타임 검증 + `/moai:project` 배선 + `63028` 안내 (AC-MV2-004).
5. 참조: plugins/ `moai-coder` 0(HEAD 35) + www plugins `moai-code|moai-coder` 0(HEAD 17) + 루트 README 구명칭 0 + 재설치 공지 (AC-MV2-005).
6. 검증: plugin validate exit 0 + P0-8 `P0-8-verdict:` 기록 + bash -n/hugo/link-check clean (AC-MV2-006).

---

## §E. 범위 제외 (Out of Scope / 명시적 exclusions)

### Out of Scope — P1 vendor 파이프라인 (moai-adk-go)

- `moai plugin export` 서브커맨드 신설, parity manifest 자동 생성, CI 자동 PR job — moai-adk-go 저장소 소관(v2 로드맵 P1). 본 SPEC의 `templates/` 채움은 수동 vendor + parity-source 마커로 한정.
- moai-adk-go 저장소의 어떤 소스 변경도 본 SPEC 범위가 아니다.

### Out of Scope — P3 T3 승격 경로

- `moai doctor`의 `plugin-deployed` 마커 인식(REQ-BD-007 계열), `bin/moai-install` 원클릭 승격 래퍼, P0-8 결과에 따른 **플러그인 비활성 안내 문구 구현** — 후속 P3 소관. 본 SPEC은 P0-8 실측·기록까지만 수행한다.

### Out of Scope — P4 릴리스 엔지니어링

- 버전 SSOT 4-plugin 전면 정렬(coworker/designer/pm 포함), www 카탈로그 전면 개편(구 토폴로지 moai-cowork/moai-design/moai-story 명칭 정비 포함), 릴리스 재설치 공지 배포 캠페인. 본 SPEC의 www 갱신은 `www/content/plugins/**`의 code 플러그인 명칭에 한정(REQ-MV2-019).

### Out of Scope — D-5 opt-in persona 플러그인

- plugin `settings.json`의 `agent` 키 기반 메인 스레드 페르소나 별도 경량 플러그인 신설(D-5 확정: 기본 미동봉 + opt-in, P3 이후 검토).

### Out of Scope — 다국어 export

- ko 단일 export(D-4 확정). 언어별 plugin variant·언어중립 프롬프트는 후속.

### Out of Scope — 사용자 게이트 실측 (P0-6 · P0-w)

- Desktop GUI 설치 E2E(P0-6), Web 실측(P0-w: 플러그인 자동 활성·#63028 재현·훅 발화·`$CLAUDE_CODE_REMOTE` 확인) — GUI/Web 환경 필요, 사용자 수행 대기. 본 SPEC의 설계는 이 셀들이 실패해도 안전(fail-open, 무해한 JSON 선언)하도록 구성됨(R9).

---

## §F. 참조 (Cross-References)

- 설계 정본: `.moai/reports/design-moai-plugin-v2-2026-07-08.md` (D-1~D-5 확정, 환경 매트릭스 개정, 로드맵)
- 원천 기록: `.moai/reports/design-moai-adk-desktop-plugin-2026-07-08.md` (템플릿 인벤토리 §3, 바이너리 커플링 §3.2, P0-1~5 증거 §9)
- 선행 SPEC: `SPEC-MOC-BOOTSTRAP-DESKTOP-001` (부트스트랩 아키텍처·패리티 계약·버전 정규화 규칙), `SPEC-MOC-PLUGIN-REMEDIATION-001` (플러그인 참조 위생 선례)
- 프로젝트 문서: `.moai/project/{product,structure,tech}.md` (2026-07-09 갱신, 실측 감사 완료)
- 본 SPEC 아티팩트: plan.md(마일스톤·git 전략·MX 계획) · acceptance.md(AC 매트릭스·판별 증명) · design.md(설계 증류) · research.md(P0 증거·실측 정본)
