---
id: SPEC-MOC-BOOTSTRAP-DESKTOP-001
title: "모두의 클로드 — 부트스트랩 아키텍처 + moai-code Desktop Edition 승격 (명령은 둘, 정본은 하나)"
version: "0.4.0"
status: superseded
created: 2026-07-02
updated: 2026-07-09
author: manager-spec
priority: P1
phase: "v3.0.0"
module: "plugins/moai-code"
lifecycle: spec-anchored
tags: "moai-code, moai-cowork, bootstrap, desktop-edition, parity, version-stamp, no-install, korean"
related_specs: [SPEC-MOC-PLUGIN-CODE-001, SPEC-MOC-PLUGIN-CODE-002, SPEC-MOC-PLUGIN-COWORK-002, SPEC-MOC-PLUGIN-REMEDIATION-001]
tier: M
---

# SPEC-MOC-BOOTSTRAP-DESKTOP-001 — 부트스트랩 아키텍처 + moai-code Desktop Edition 승격

## HISTORY

- **2026-07-02** 최초 작성 (manager-spec, plan-phase iteration 1, Tier M). "명령은 둘, 정본은 하나(two commands, one canonical template)" 부트스트랩 아키텍처와 "moai-code = moai-adk Desktop Edition" 승격을 정의한다. 설계 문서의 자산 주장을 신뢰하지 않고 3개 트리(`plugins/moai-cowork/`, `plugins/moai-code/`, `moai-adk-go/internal/template/templates/`)를 직접 실측했다. 핵심 실측 결과(§A.2): (1) `/project init`은 이미 moai-cowork `skills/project/SKILL.md`에서 bare `/project`의 **레거시 별칭**으로 존재하며 소크라테스 인터뷰 + `CLAUDE.md` 생성은 이미 동작한다 — 본 SPEC은 이를 재정의하지 않고 폴더 규약 스캐폴드 + 스킬 프로파일 산출물만 순증(net-new)으로 추가한다. (2) moai-code 13개 명령 파일 전부가 `<!-- parity-source: internal/template/templates/... @ b1ff846c4 -->` 프로버넌스 주석을 이미 보유 → R2/R4 패리티 계약의 기존 메커니즘. (3) 무설치 훅 패턴(`무설치 자기완결 훅` 주석 + parity-source + fail-open `exit 0`)이 이미 존재 → R3는 신규 발명이 아니라 재사용. (4) 버전 스탬프는 `pkg/version/version.go`(바이너리, `v3.0.0-rc6`) → `{{.Version}}` → `.moai/config/sections/system.yaml`로 흐르며, `hugo.toml` L50-54의 ⚠️SSOT 주석 블록이 R4가 미러링할 패턴이다. `moai doctor`는 이미 존재 → R2 승격 경로 유효. SPEC ID는 제안값 `SPEC-MOC-BOOTSTRAP-DESKTOP-001`을 유지한다(정규 regex `^SPEC(-[A-Z][A-Z0-9]*)+-\d{3}$` 통과, `SPEC-MOC-*` 패밀리 접두사 부합, 단일 플러그인 SPEC이 아닌 교차-플러그인 아키텍처 SPEC임을 중간 세그먼트로 구분).
- **2026-07-02** plan-phase iteration 2 (manager-spec, AC 하드닝). plan-auditor iter-1 FAIL 0.77 near-miss 해소: (1) **AC-BD-006 비결정성 제거** — 4개 위치 리터럴 문자열 동등 비교는 결정적으로 통과 불가(실측: `pkg/version/version.go`=`v3.0.0-rc6` v-접두 pre-release, `system.yaml.tmpl`=`{{.Version}}` 템플릿 플레이스홀더, 두 `plugin.json`=`0.1.0`)임을 확인하고, 정규화 규칙(리딩 `v`·`-rcN`/pre-release 접미사 제거 후 concrete 리터럴 3곳 비교 + tmpl은 플레이스홀더 토큰 존재 검증)으로 재작성. 항상-결정적 부분(위치 4곳 + SSOT 라인 + 플레이스홀더)과 D1-게이트 부분(정규화 리터럴 일치)을 분리(EC4 정합). (2) **REQ-BD-007 이연** — 대응 AC 없는 doctor 드리프트-리포트/승격 REQ를 §E 명시 이연(out-of-AC-scope) 노트로 이동, EC2를 전방 참조로 재표기, §D.4 DoD·§D.5 추적성에 이연 명시. (3) **D4 공유 파일 경계** — `skills/project/SKILL.md` 공유: 본 SPEC=진입(스캐폴드+레거시 별칭, AC-BD-001), REMEDIATION-001=본문 라우팅 리메디에이션(AC-REM-016). 실측 확인: `plugins/moai-cowork/commands/` 부재(진입점은 skill), spec/acceptance에 잘못된 `moai-cowork/commands/` 참조 없음.
- **2026-07-02** plan-phase iteration 3 (manager-spec, 체계적 AC 판별력 하드닝 — FINAL). plan-auditor iter-2 FAIL 0.73(회귀, Testability 0.52) 근본원인 해소: **NET-NEW 동작을 기존 파일에 추가하는 SPEC인데 여러 AC가 HEAD에서 이미 존재하거나 SPEC 자기텍스트를 grep하여 자기통과(self-pass)** 하던 문제를 전수 스윕으로 교정. 전체 `≥1`/존재 predicate를 HEAD(6d78fbf)에서 실측하고 self-passer를 판별 유형으로 재분류(§D.0 판별 모델 + §D.6 판별 증명 신설). 핵심 교정: (1) **AC-BD-001** — repo-root `test -f ./CLAUDE.md`(자기통과) 삭제 + `.moai/` skill-profile grep(18매치 전부 SPEC 자기텍스트) 제거 → 지정 산출물 경로 `.moai/skill-profile.yaml`(HEAD=0) + 폴더-스캐폴드 센티넬(HEAD=0)의 NET-NEW 게이트로 교체. REQ-BD-002(c)에 정확 경로 명문화 + EC6(글로벌 `moai-profile.md` 금지와 구분). CLAUDE.md 생성·별칭은 PRESERVE 회귀 가드로 분리(001c). (2) **AC-BD-006** — 브로드 `SSOT` grep(HEAD 63개 무관 자기통과, 정밀 `일괄 bump`/`release-checklist`=0) → 지정 net-new 센티넬 `VERSION-SSOT` 라인(HEAD=0)으로 교체. 4곳 존재 grep은 정보용 pre-flight로 강등, `{{.Version}}` 플레이스홀더는 PRESERVE로 라벨. REQ-BD-011에 센티넬 명문화. (3) **AC-BD-008** — 사전존재 parity-source 마커(12/36 자기통과) + 미지정 "역방향 편집 흔적" → PRESERVE 회귀 가드(마커 ≥baseline) + 구체 orphan-edit grep(parity-source 없는 편집 명령 파일=0) 문서화 불변식으로 재정의. REQ-BD-014에 mechanical-gate 아닌 불변식임을 명시. (4) **AC-BD-005** — fail-open `exit 0`(자기통과) PRESERVE 회귀 가드로 라벨, 바이너리 탐지 분기(HEAD=0)를 NET-NEW 게이트로 분리(005a/b). (5) **AC-BD-004** — 브로드 "Tier N" 매칭을 net-new `Desktop Edition` 리터럴(HEAD=0)로 고정해 보강. 결과: NET-NEW 게이트 6개 전부 HEAD=0(자기통과 predicate 0건). 편집 범위: acceptance.md(전면 재작성) + spec.md(REQ-BD-002(c)/011/014 명문화 + frontmatter + HISTORY). plugins/**·www/**·internal/** 무수정.

---

## §A. 배경 및 목적 (Background)

### A.1 비즈니스 맥락

"모두의 클로드"는 청중별 분리 3-플러그인 패밀리(`moai-cowork` / `moai-design` / `moai-code`)를 단일 마켓플레이스(`modu-ai/claude`, `.claude-plugin/marketplace.json`)로 배포한다. 본 SPEC은 개별 플러그인의 스킬 내용이 아니라, **두 진입점이 하나의 정본에서 파생된다**는 교차-플러그인 부트스트랩 아키텍처와 moai-code의 "Desktop Edition" 위상 승격을 정의한다.

핵심 서사 둘:

1. **명령은 둘, 정본은 하나** — 사용자 부트스트랩 진입점은 둘이다: 비개발자용 `/project init`(moai-cowork)와 무설치 개발용 `/moai:project`(moai-code). 두 진입점이 만드는 프로젝트 골격의 정본(SSOT)은 하나다: `internal/template/templates/`(go:embed 정본). 정본→플러그인 방향의 vendor-sync만 허용되며 그 역방향은 금지한다.
2. **moai-code = moai-adk Desktop Edition** — moai-code는 `moai` CLI 바이너리 없이 Claude Code/Desktop에서 MoAI-ADK 방법론의 ~90%(Tier 1)를 제공하고, git(Tier 2)·바이너리(Tier 3)가 있을 때 점진적으로 능력이 확장된다. 설치는 올인원이되, "필요한 것만"은 **설치 시점이 아니라 프로젝트 시점**에 스킬 프로파일로 조준된다.

### A.2 현재 상태 실측 (Ground-Truth, 2026-07-02)

설계 문서의 주장을 신뢰하지 않고 직접 조사한 결과:

- **`/project init` = 레거시 별칭.** `plugins/moai-cowork/skills/project/SKILL.md`는 bare `/project`가 초기화 기본 동작이며 `/project init`은 그 레거시 별칭임을 명시한다. 소크라테스 인터뷰(비개발자 어휘) + 플러그인 인벤토리 + 스킬 체인 설계 + `CLAUDE.md` 생성 + Gap Detection이 **이미 동작**한다. moai-cowork에는 `commands/` 디렉터리가 없고 진입점은 스킬(`skills/project/`)이다.
- **parity-source 프로버넌스.** `plugins/moai-code/commands/*.md` 13개 중 12개(harness 제외)가 `<!-- parity-source: internal/template/templates/.claude/commands/moai/<cmd>.md.tmpl @ b1ff846c4 -->` 주석을 보유. 각 명령은 얇은 래퍼로 `Skill("moai")`에 서브커맨드를 위임한다(예: `/moai:project` → `Skill("moai") project $ARGUMENTS`).
- **무설치 훅 패턴.** `plugins/moai-code/hooks/moai/handle-session-start.sh` 등은 `# moai-code 무설치 자기완결 훅` + parity-source + `cat >/dev/null 2>&1 || true; exit 0`(fail-open)로 구성. 바이너리 셸아웃을 제거한 무설치 대체 패턴이 이미 존재.
- **버전 스탬프 흐름.** 바이너리 정본 `pkg/version/version.go`(`Version = "v3.0.0-rc6"`) → `internal/template/templates/.moai/config/sections/system.yaml.tmpl`의 `version: "{{.Version}}"` / `template_version: "{{.Version}}"` 주입. 별도 `.moai/version` 파일은 없다. 플러그인 버전은 `moai-cowork`/`moai-code` 각각의 `.claude-plugin/plugin.json`에 `"version": "0.1.0"`. 마켓플레이스는 `.claude-plugin/marketplace.json` `metadata.version: "0.1.0"`. 표시용 SSOT 주석 패턴은 `www/hugo.toml` L50-54(⚠️ SSOT — 두 줄만 갱신하면 자동 반영, 릴리스 시 marketplace.json + plugin.json + SKILL.md 일괄 bump).
- **승격 경로.** `moai doctor`(`internal/cli/doctor*.go`, `session doctor`)가 이미 존재 → 바이너리 설치 후 드리프트 탐지·승격 안내의 착지점.

### A.3 목표 (Goals)

1. 비개발자 부트스트랩(`/project init`)이 폴더 규약 + `CLAUDE.md` + **지속되는 스킬 프로파일 산출물**을 생성하게 한다(순증 범위).
2. `/moai:project`(무설치)와 `moai init`(바이너리)의 출력 트리 **패리티 계약**을 문서화하고 기계 검증 가능하게 한다.
3. moai-code의 **Tier 1~3 능력 표**를 공표하고, 세션 시작 시 바이너리 탐지→승격 안내 1줄 / 부재 시 훅 무음 fail-open을 규정한다.
4. 4개 위치 **버전 스탬프 단일 릴리스-체크리스트 라인**을 hugo.toml SSOT-주석 패턴으로 통합하고, 플러그인 버전을 바이너리 v3.0.x 라인에 바인딩한다.
5. (SHOULD) moai-code 표시명 변경 옵션을 plan.md에 제시한다(기본값 = 유지).

---

## §B. GEARS 요구사항 (Requirements)

> 표기: GEARS(현행). `<subject>`는 일반화됨(the skill / the command / the release process / the orchestrator 등). **shall / When / While / Where**는 GEARS 키워드.

### R1 — `/project init` 비개발자 부트스트랩 (moai-cowork)

- **REQ-BD-001 (Ubiquitous).** The moai-cowork `/project` skill shall continue to provide a `/project init` bootstrap entry (현재 bare `/project`의 레거시 별칭) that runs a Socratic interview in **non-developer vocabulary** covering: 프로젝트 유형 → 주 업무 → 산출물 형태.
- **REQ-BD-002 (Event-driven).** **When** the `/project init` interview reaches sufficient context, the skill shall generate three artifacts: (a) 폴더 규약 스캐폴드(folder-convention scaffold), (b) 프로젝트 `CLAUDE.md` 지침 파일(기존 동작 유지 — `skills/project/SKILL.md` §"1. CLAUDE.md 구조"에 이미 정의됨, 순증 아님), (c) 스킬 프로파일 산출물 — 이 프로젝트가 주로 쓰는 스킬을 명시 열거한 지속(persisted) 파일로, **지정 경로 `.moai/skill-profile.yaml`** 에 기록한다(net-new). 이 산출물은 **프로젝트 스킬-선택 CONFIG**이며, SKILL.md §"2. moai-profile.md 생성 금지"가 금지하는 **글로벌 사용자 프로필**(`moai-profile.md`)과 별개다(acceptance.md EC6). 사용자 개인정보는 여전히 프로젝트 `CLAUDE.md` 한 곳에만 기록된다.
- **REQ-BD-003 (Ubiquitous).** The skill-profile artifact shall aim Claude의 스킬 선택을 프로파일된 스킬로 조준(project-level "필요한 것만") 하되, 설치는 올인원 상태로 유지한다(설치 시점 축소 아님).
- **REQ-BD-004 (Ubiquitous, 하위 호환).** The skill shall keep bare `/project`와 `/project init`을 등가 진입점으로 유지하여 기존 사용자 트리거를 깨지 않는다(순증만 허용).

### R2 — `/moai:project` ↔ `moai init` 출력 패리티 (moai-code · 정본)

- **REQ-BD-005 (Ubiquitous).** The plugin command `/moai:project`(바이너리 없음) and the binary `moai init` shall produce the **same `.claude/` + `.moai/` file tree**(파일 집합 동일).
- **REQ-BD-006 (Event-driven).** **When** `/moai:project` generates the tree, the command shall stamp `.moai/config/sections/system.yaml`의 `version` 필드를 리터럴 `"plugin-deployed vX.Y.Z"` 마커로 기입한다(바이너리의 `{{.Version}}` 주입을 무설치 환경에서 대체하는, 계약상 유일한 값 발산 지점).
- **REQ-BD-007 — 이연됨(DEFERRED → §E, out-of-AC-scope).** doctor 드리프트 보고/승격 동작(후속 `moai` 바이너리 설치가 `plugin-deployed` 마커를 탐지하면 `moai doctor`가 드리프트를 보고하고 바이너리 관리 트리로의 승격을 제안)은 후속 SPEC 소관이다. 본 SPEC의 **어떤 AC로도 검증하지 않으며**, 이연 근거는 §E "범위 제외 — moai 바이너리 소스 변경"에 기록한다. EC2(acceptance.md)는 이 동작의 전방 참조(forward-looking, 통과 게이트 아님)일 뿐이다.

### R3 — Desktop Edition 능력 Tier (moai-code)

- **REQ-BD-008 (Ubiquitous).** moai-code shall publish a Tier 1~3 능력 표: Tier 1(플러그인 단독) = `/moai:plan→run→sync` 워크플로우 + SPEC 템플릿 + 13개 명령 ≈ 방법론 90%; Tier 2(플러그인 + git) = branch/worktree 흐름(git CLI); Tier 3(플러그인 + moai 바이너리) = 네이티브 훅 강제(품질 게이트·Stop 훅) + LSP 진단 게이트 + 세션 레지스트리 + cg/glm 비용 모드.
- **REQ-BD-009 (Event-driven).** **When** a session starts, moai-code shall detect the `moai` 바이너리 and, **Where** the binary is present, display a 1줄 승격 안내(promotion notice).
- **REQ-BD-010 (Event-driven, 원치 않는 동작 방지).** **When** the `moai` 바이너리 is absent, moai-code hooks shall fail open silently(기존 무설치 자기완결 훅 패턴 재사용 — 사용자 흐름 차단·에러 노출 금지).

### R4 — 버전 스탬프 규약

- **REQ-BD-011 (Ubiquitous).** The release process shall unify the version across **4 locations** — 템플릿 정본(`pkg/version/version.go` → `system.yaml.tmpl {{.Version}}`) + `plugins/moai-cowork/.claude-plugin/plugin.json` + `plugins/moai-code/.claude-plugin/plugin.json` + 바이너리(`pkg/version/version.go`) — into a single 릴리스-체크리스트 라인, `www/hugo.toml` L50-54의 ⚠️SSOT 주석 패턴을 미러링하여. **The unified checklist line shall carry the net-new sentinel marker `VERSION-SSOT`** (지정 리터럴, HEAD 부재) — 예: `⚠️ VERSION-SSOT — 릴리스 버전 4개 위치 일괄 bump 체크리스트`. 이 센티넬이 AC-BD-006c의 판별 predicate이며, 브로드 `SSOT` 문자열(무관 매칭 다수)이 아니다.
- **REQ-BD-012 (Ubiquitous).** The plugin version shall be bound to the binary v3.0.x 라인(3.0.x ↔ 3.0.x) so that "동일 방법론, 두 배포 형태"가 버전 표기 자체로 표현된다.

### R5 — 표시명 (SHOULD, 기본값 = 유지)

- **REQ-BD-013 (Where, 능력 게이트 · SHOULD).** **Where** the display-name change 옵션이 채택되면, the marketplace.json + plugin.json `displayName` for moai-code shall read `"MoAI Code — moai-adk Desktop Edition"`. 기본값은 현행 `"MoAI Code"` 유지이며, plan.md §F에 옵션으로 제시한다.

### 교차 제약 (Vendor-sync 방향)

- **REQ-BD-014 (Ubiquitous, 방향 제약).** The template SSOT(`internal/template/templates`) shall be the 유일 정본; plugin trees shall receive a vendor-sync copy on release. The sync 방향 shall be **정본 → 플러그인** only; the plugin trees shall not be edited as the source of truth. `parity-source` 마커가 프로버넌스를 기록한다. 본 제약은 **net-new 작업이 아니라 문서화 불변식(documented invariant)** 이다 — parity-source 마커는 이미 존재(실측: commands 12/moai-code 36). 따라서 AC-BD-008은 mechanical-gate가 아닌 **회귀 가드**로 검증한다: (a) 마커 count가 baseline 이상 유지되고, (b) 편집된 명령 파일이 parity-source 마커를 잃지 않는다(orphan-edit=0). "역방향 편집 흔적"은 이 orphan-edit grep으로 구체화한다.

---

## §C. 제약 (Constraints)

- **C1.** 본 SPEC은 **SPEC 산출물만** 작성한다. 구현 금지(run-phase 소관).
- **C2.** 정본 = `internal/template/templates`. 동기화 방향은 정본→플러그인 단방향으로만 인코딩하며 역방향을 서술하지 않는다(REQ-BD-014).
- **C3.** 수용 기준은 기계 검증 가능해야 한다: `/moai:project` vs `moai init` 출력 트리 diff 패리티, 4개 위치 버전 스탬프 grep, 명령/스킬 파일 존재, Tier 표 존재, 세션-시작 훅 바이너리 탐지 + fail-open, parity-source 마커 존재.
- **C4.** 최소주의(minimal). 과설계 금지 — 기존 메커니즘(레거시 `/project init`, parity-source 주석, 무설치 훅, hugo.toml SSOT 주석) 재사용을 우선한다.
- **C5.** 값 발산 예외는 REQ-BD-006 버전 스탬프 라인 하나로 한정한다. 그 외 파일 집합·내용은 패리티를 유지한다.

---

## §D. 성공 기준 (Success Criteria, 요약)

상세 Given-When-Then과 임계값은 `acceptance.md`에 있다. 요약:

1. `/project init`이 폴더 스캐폴드(신규) + 지정 경로 `.moai/skill-profile.yaml`(신규) 산출을 지시하고, `CLAUDE.md` 생성·레거시 별칭을 유지한다(AC-BD-001a/b NET-NEW, 001c PRESERVE).
2. `/moai:project`와 `moai init`의 파일 집합이 동일하다(버전 스탬프 라인 제외, non-empty 가드)(AC-BD-002 RUNTIME).
3. 무설치 배포 트리의 `system.yaml` version이 `plugin-deployed vX.Y.Z` 마커를 갖는다(AC-BD-003 NET-NEW, `plugin-deployed` 리터럴 HEAD 부재).
4. moai-code에 `Desktop Edition` Tier 1~3 능력 표가 존재하고(AC-BD-004 NET-NEW), 세션-시작 훅이 바이너리 탐지 분기(신규, 005a)를 추가하며 fail-open을 유지한다(005b PRESERVE).
5. 4개 위치 버전이 지정 `VERSION-SSOT` 센티넬 라인으로 통합된다(AC-BD-006c NET-NEW); 값 일치는 D1 결정 후 정규화 비교(AC-BD-006d D1-GATED, EC4).

각 AC의 판별 유형과 HEAD pre-state 증명은 acceptance.md §D.0 판별 모델 + §D.6 판별 증명 참조.

---

## §E. 범위 제외 (Out of Scope / 명시적 exclusions)

본 절은 본 SPEC이 **다루지 않는 것(what NOT to build)** 을 명시하며, out of scope 항목은 다른 SPEC 또는 run-phase 소관이다.

### Out of Scope — moai-cowork 스킬 내용

- `plugins/moai-cowork/skills/**`의 스킬 본문·목록·품질(179개 스킬)은 `SPEC-MOC-PLUGIN-REMEDIATION-001` 소관이며 본 SPEC은 이를 수정하지 않는다. 본 SPEC은 `skills/project/`의 진입 동작(폴더 스캐폴드 + 스킬 프로파일 순증)만 다룬다.
- **공유 파일 경계(shared-file boundary) — `plugins/moai-cowork/skills/project/SKILL.md`.** 이 파일은 두 SPEC이 공유한다(진입점은 스킬이다 — `plugins/moai-cowork/commands/` 디렉터리는 **존재하지 않는다**, §A.2 실측). **본 SPEC(SPEC-MOC-BOOTSTRAP-DESKTOP-001)은 진입(ENTRY) 동작을 소유한다**: `/project init` 폴더 스캐폴드 생성 + 레거시 bare-`/project` 별칭 유지(AC-BD-001). **`SPEC-MOC-PLUGIN-REMEDIATION-001`은 본문 내용(BODY-content) 리메디에이션을 소유한다**: `project` 라우팅이 27-플러그인 토폴로지가 아니라 단일 `moai-cowork` 아키텍처를 겨냥하도록 하는 본문 수정(AC-REM-016). 본 SPEC의 predicate(AC-BD-001)는 REMEDIATION의 본문-리메디에이션 라인(라우팅 토폴로지·retired-topology 제거)을 주장(claim)하지 않으며, 역으로 REMEDIATION의 predicate(AC-REM-016)는 진입 스캐폴드/별칭 동작을 주장하지 않는다. 같은 파일을 편집하더라도 검증 대상 라인이 분리된다.

### Out of Scope — moai-design 스킬 내용

- `plugins/moai-design/skills/**`는 리메디에이션 SPEC 소관. 본 SPEC은 3-플러그인 마켓 구조를 전제로만 참조할 뿐 design 플러그인 내용을 변경하지 않는다.

### Out of Scope — www 문서 사이트

- `www/**`(Hugo 사이트, IA, 페이지 콘텐츠)는 `SPEC-MOC-SITE-IA-001` 소관. 본 SPEC은 `www/hugo.toml`의 SSOT-주석 **패턴만 참조**하며 www 콘텐츠·구조를 변경하지 않는다.

### Out of Scope — 구현 (implementation)

- 본 SPEC은 plan-phase 산출물(spec/plan/acceptance/progress)만 생성한다. `/project init` 스캐폴드 로직, 패리티 하네스, Tier 표, 버전 스탬프 리팩터의 실제 코드 작성은 run-phase 소관이다.

### Out of Scope — moai 바이너리 소스 변경

- `moai-adk-go`의 바이너리 소스(버전 상수 읽기 이외)는 변경하지 않는다. `moai doctor` 승격 로직의 신규 구현은 본 SPEC 범위 밖이며(기존 `doctor` 착지점만 지정), 필요 시 별도 SPEC으로 이연한다.
- **REQ-BD-007 이연 근거(DEFERRED, out-of-AC-scope).** §B R2에서 이연된 REQ-BD-007(doctor 드리프트 보고 + `plugin-deployed` 마커 탐지 시 승격 제안; EC2 시나리오)은 본 SPEC의 어떤 AC로도 검증하지 않는다. 이유: (1) doctor 드리프트-리포트 동작은 바이너리 소스 변경을 수반하는 후속(follow-up) 기능으로, C1("SPEC 산출물만 작성")과 본 절("바이너리 소스 미변경") 범위 밖이다. (2) 본 SPEC은 무설치 배포 트리에 `plugin-deployed vX.Y.Z` 마커를 **기입**하는 계약(REQ-BD-006 → AC-BD-003)까지만 소유한다 — 그 마커를 나중에 **소비**하는 doctor 승격 로직은 별도 SPEC의 착지점이다. 따라서 §D.5 추적성에서 REQ-BD-007은 "대응 AC 없음(의도적 이연)"으로 기록되며, DoD(§D.4)는 REQ-BD-007 AC 커버리지를 주장하지 않는다.

### Out of Scope — 바이너리 의존 훅 전수 목록 확정

- 무설치 대체가 필요한 바이너리 의존 훅의 정확한 전수 인벤토리는 `SPEC-MOC-PLUGIN-CODE-002`(스크립트 기반 기계적 재감사) 소관이다. 본 SPEC은 세션-시작 훅의 fail-open 패턴 재사용(REQ-BD-010)만 규정하고 정확한 카운트 주장을 하지 않는다.

---

## §F. 참조 (Cross-References)

- 정본 템플릿: `/Users/goos/moai/moai-adk-go/internal/template/templates/`
- 바이너리 버전: `/Users/goos/moai/moai-adk-go/pkg/version/version.go`
- moai-cowork 진입 스킬: `plugins/moai-cowork/skills/project/SKILL.md`
- moai-code 명령/훅: `plugins/moai-code/commands/*.md`, `plugins/moai-code/hooks/moai/handle-session-start.sh`
- 마켓플레이스: `.claude-plugin/marketplace.json`
- SSOT-주석 패턴: `www/hugo.toml` L50-54
- 형제 SPEC: `SPEC-MOC-PLUGIN-CODE-001`(무설치 골격), `SPEC-MOC-PLUGIN-CODE-002`(바이너리 의존 재감사), `SPEC-MOC-PLUGIN-COWORK-002`(Cowork Desktop 완료)
