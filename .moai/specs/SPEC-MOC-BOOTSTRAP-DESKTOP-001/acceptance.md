# SPEC-MOC-BOOTSTRAP-DESKTOP-001 — 수용 기준 (acceptance.md)

> 모든 AC는 기계 검증 가능해야 한다(파일 존재 / grep / diff / 카운트). 각 predicate는 **판별력(discrimination)** 을 가져야 한다: NET-NEW 게이트는 HEAD(구현 전)에서 실패하고 run-phase 후 통과해야 하며, PRESERVE 제약은 회귀 가드로 명시 라벨한다. 전체 HEAD pre-state 증명은 §D.6 참조.

## §D.0 판별 모델 (Discrimination Model)

본 SPEC은 **이미 존재하는 파일에 순증(net-new) 동작을 추가**한다. 따라서 AC를 세 유형으로 분리해 각 predicate가 무엇을 검증하는지 명확히 한다. 이는 iter-2 FAIL(Testability 0.52) 근본원인 — `≥1`/존재 predicate가 HEAD에서 자기통과(self-pass)하여 판별력 0 — 을 해소한다.

| 유형 | 정의 | HEAD 기대 | 통과 조건 |
|------|------|-----------|-----------|
| **NET-NEW 게이트** | run-phase가 새로 만드는 동작. HEAD-absent 리터럴/센티넬로 검증. | **0 (부재)** | run-phase 후 ≥1 |
| **RUNTIME 행위** | 두 진입점의 실제 실행 산출물 비교. 하네스 없이는 실행 불가 → 자기통과 불가. | 실행 불가 | 하네스 실행 후 diff/grep 통과 |
| **PRESERVE 제약** | 기존 메커니즘을 깨지 않아야 함(회귀 가드). HEAD 자기통과가 **정상이자 의도**. | ≥ baseline | 회귀 없음(count ≥ HEAD baseline) |
| **D1-GATED** | 사용자 정책 결정(D1) 후에만 값 일치 기대. | 불일치(정상) | D1 결정 후 정규화 리터럴 일치 |
| **OPTION** | R5 채택 시에만 적용. | 부재 | 채택 시 리터럴 존재 |

## §D. 수용 기준 매트릭스 (AC Matrix)

| AC | 대응 REQ | 유형 | 검증 방법 | HEAD pre-state | 통과 조건 |
|----|----------|------|-----------|----------------|-----------|
| AC-BD-001a | REQ-BD-002(c), REQ-BD-003 | NET-NEW 게이트 | grep `skill-profile.yaml` in SKILL.md + runtime `test -f P/.moai/skill-profile.yaml` | **0** (SKILL.md에 부재) | SKILL.md가 `.moai/skill-profile.yaml` 산출을 지시 ≥1; 생성된 프로젝트 P에 파일 존재 |
| AC-BD-001b | REQ-BD-002(a) | NET-NEW 게이트 | grep 폴더-스캐폴드 센티넬 in SKILL.md | **0** (부재) | SKILL.md가 폴더 규약 스캐폴드 생성 동작을 지시 ≥1 |
| AC-BD-001c | REQ-BD-001, REQ-BD-002(b), REQ-BD-004 | PRESERVE 제약 | grep 회귀 가드(레거시 별칭 + CLAUDE.md 구조 헤딩) | ≥ baseline(별칭 14, CLAUDE.md 헤딩 1) | bare `/project` ≡ `/project init` 유지 + `### 1. CLAUDE.md 구조` 유지(회귀 없음) |
| AC-BD-002 | REQ-BD-005 | RUNTIME 행위 | 트리 diff(버전 라인 제외) + non-empty 가드 | 실행 불가(하네스 필요) | `/moai:project` 파일 집합 = `moai init` 파일 집합(양쪽 non-empty) |
| AC-BD-003 | REQ-BD-006 | NET-NEW 게이트 + RUNTIME | grep `plugin-deployed` in moai-code + runtime grep P/system.yaml | **0** (`plugin-deployed` 리터럴 부재) | `/moai:project`가 `plugin-deployed vX.Y.Z` 기입 지시 ≥1; 생성 트리 system.yaml version = 마커 |
| AC-BD-004 | REQ-BD-008 | NET-NEW 게이트 | grep `Desktop Edition` 센티넬 + 3 Tier 행 구조 | **0** (`Desktop Edition` 부재; 지정 파일 Tier 행 0) | moai-code 공표 문서에 `Desktop Edition` + Tier 1/2/3 표(3행) 존재 |
| AC-BD-005a | REQ-BD-009 | NET-NEW 게이트 | grep 바이너리 탐지 분기 in 세션-시작 훅 | **0** (부재) | 세션-시작 훅에 `command -v moai`/승격 분기 ≥1 |
| AC-BD-005b | REQ-BD-010 | PRESERVE 제약 | grep fail-open `exit 0` 회귀 가드 | ≥ baseline(=1) | 무설치 fail-open `exit 0` 유지(회귀 없음) |
| AC-BD-006a | REQ-BD-011 | 정보용(비게이트) | grep 4개 위치 존재 | 4곳 모두 존재(자기통과 by design) | (게이트 아님) 버전 스탬프 표면 확인용 pre-flight |
| AC-BD-006b | REQ-BD-011 | PRESERVE 제약 | grep `{{.Version}}` 플레이스홀더 유지 | 존재(자기통과 정상) | tmpl은 리터럴 아닌 `{{.Version}}` 플레이스홀더 유지 |
| AC-BD-006c | REQ-BD-011 | NET-NEW 게이트 | grep 지정 `VERSION-SSOT` 센티넬 라인 | **0** (센티넬 부재; 정밀 `일괄 bump`/`release-checklist` 0) | moai-code에 지정 SSOT 체크리스트 센티넬 라인 존재 ≥1 |
| AC-BD-006d | REQ-BD-012 | D1-GATED | 정규화 후 concrete 리터럴 3곳 일치 | 불일치(정상, pre-D1) | D1 결정 후 정규화 리터럴 3곳 일치 |
| AC-BD-007 | REQ-BD-013 | OPTION | grep displayName 리터럴 | **0** (신규 리터럴 부재; 현행 "MoAI Code") | (채택 시) displayName = "MoAI Code — moai-adk Desktop Edition" |
| AC-BD-008 | REQ-BD-014 | PRESERVE 제약(문서화 불변식) | parity-source 마커 회귀 가드 + orphan-edit 탐지 grep | 마커 12(commands)/36(total), orphan 0 | 마커 count ≥ baseline + parity-source 없는 편집된 명령 파일(orphan) = 0 |

> **판별 요약**: NET-NEW 게이트 6개(001a·001b·003·004·005a·006c)는 HEAD에서 **모두 0(부재)** — 자기통과 불가, 판별력 有. RUNTIME 1개(002)는 하네스 없이 실행 불가. PRESERVE 제약 4개(001c·005b·006b·008)와 정보용 1개(006a)는 **회귀 가드/pre-flight로 명시 라벨**되어 자기통과가 정상. D1-GATED(006d)·OPTION(007)은 조건부. spec.md §E 공유 파일 경계: AC-BD-001*은 `skills/project/SKILL.md`의 **진입 동작만** 주장하며 `### 도메인 플러그인 (27개)` 라우팅 본문(REMEDIATION-001 AC-REM-016 소관)은 주장하지 않는다.

## §D.1 Given-When-Then 시나리오

### 시나리오 1 — `/project init` 순증 (AC-BD-001a/b/c)
- **Given** moai-cowork가 설치된 신규 프로젝트 루트에서
- **When** 사용자가 `/project init`(또는 bare `/project`)를 실행하고 비개발자 어휘 인터뷰(유형→업무→산출물)를 완료하면
- **Then** (a) 폴더 규약 스캐폴드가 생성되고, (b) 프로젝트 `CLAUDE.md`가 생성되며, (c) 지정 경로 `.moai/skill-profile.yaml`에 스킬 프로파일 산출물이 지속(persist)된다.
- **검증**:
```bash
CW_SKILL=plugins/moai-cowork/skills/project/SKILL.md

# AC-BD-001a — NET-NEW 게이트: 지정 산출물 경로 .moai/skill-profile.yaml (HEAD=0)
#   판별: SKILL.md가 이 정확한 경로의 산출을 지시하는가. HEAD에는 부재(0).
grep -c "skill-profile.yaml" "$CW_SKILL"                 # HEAD=0 → run-phase 후 ≥1 (PASS)
#   런타임(생성된 프로젝트 P, 임시 디렉터리 — 레포의 .moai/ 아님):
#   test -f "$P/.moai/skill-profile.yaml"                 # 생성 트리에 파일 존재
#   주의: .moai/skill-profile.yaml = 프로젝트 스킬-선택 CONFIG.
#   SKILL.md L379 "moai-profile.md 생성 금지"(글로벌 사용자 프로필)와 별개 산출물.

# AC-BD-001b — NET-NEW 게이트: 폴더 규약 스캐폴드 지시 센티넬 (HEAD=0)
grep -ciE "폴더 규약 스캐폴드|folder-convention scaffold" "$CW_SKILL"   # HEAD=0 → 후 ≥1 (PASS)

# AC-BD-001c — PRESERVE 제약(회귀 가드, NOT 신규 작업): 하위 호환 + CLAUDE.md 생성 유지
grep -ciE "레거시 별칭|bare .?/project|/project init" "$CW_SKILL"       # baseline 14, ≥14 유지
grep -c "^### 1\. CLAUDE.md 구조" "$CW_SKILL"                            # baseline 1, ≥1 유지
#   ↑ 이 두 grep의 HEAD 자기통과는 의도된 것 — 기존 CLAUDE.md 생성·별칭을 PRESERVE 검증.
```
> **공유 파일 경계**: 위 verification은 `skills/project/SKILL.md`의 **진입 동작**(폴더 스캐폴드·`CLAUDE.md`·`.moai/skill-profile.yaml`·레거시 별칭)만 주장한다. `project` 라우팅 토폴로지 본문(`### 도메인 플러그인 (27개)` → 단일 `moai-cowork`)은 `SPEC-MOC-PLUGIN-REMEDIATION-001` AC-REM-016 소관이며 AC-BD-001*은 이를 주장하지 않는다(spec.md §E 공유 파일 경계 참조). `plugins/moai-cowork/commands/`는 존재하지 않으므로 진입점 검증은 `skills/project/SKILL.md`를 대상으로 한다.

### 시나리오 2 — `/moai:project` ↔ `moai init` 파일-집합 패리티 (AC-BD-002, AC-BD-003)
- **Given** 동일 빈 디렉터리 두 곳(A, B)에서
- **When** A에 `moai init`을, B에 `/moai:project`(무설치)를 실행하면
- **Then** `.claude/` + `.moai/` 파일 집합이 동일하고, 유일한 값 발산은 `system.yaml`의 version 라인(A=실버전, B=`plugin-deployed vX.Y.Z`)이다.
- **검증**:
```bash
# AC-BD-002 — RUNTIME 행위(하네스 필요 → 자기통과 불가). non-empty 가드로 빈-vs-빈 거짓통과 차단.
CNT_A=$(cd A && find .claude .moai -type f | wc -l)
CNT_B=$(cd B && find .claude .moai -type f | wc -l)
[ "$CNT_A" -gt 10 ] && [ "$CNT_B" -gt 10 ] || { echo "FAIL: 빈 트리(하네스 미실행)"; exit 1; }
diff <(cd A && find .claude .moai -type f | sort) \
     <(cd B && find .claude .moai -type f | sort)   # 출력 없음 = PASS

# AC-BD-003 — NET-NEW 게이트: plugin-deployed 마커 (HEAD=0)
#   판별(정적): /moai:project 명령/스킬이 plugin-deployed 기입을 지시하는가. HEAD 부재(0).
grep -rc "plugin-deployed" plugins/moai-code/ | grep -v ':0' | wc -l   # HEAD=0 → 후 ≥1 (PASS)
#   런타임: 생성 트리 값 발산 1지점 확인
grep '^\s*version:' B/.moai/config/sections/system.yaml   # → "plugin-deployed vX.Y.Z"
grep '^\s*version:' A/.moai/config/sections/system.yaml   # → 실제 바이너리 버전
```

### 시나리오 3 — Tier 표 + 세션-시작 배선 (AC-BD-004, AC-BD-005a/b)
- **Given** moai-code 플러그인이 설치된 세션에서
- **When** 세션이 시작되면
- **Then** 바이너리 존재 시 1줄 승격 안내가 표시되고, 부재 시 훅은 무음 fail-open하며, moai-code는 `Desktop Edition` Tier 1~3 능력 표를 공표한다.
- **검증**:
```bash
HOOK=plugins/moai-code/hooks/moai/handle-session-start.sh

# AC-BD-004 — NET-NEW 게이트: Desktop Edition 센티넬 + 3 Tier 행 (HEAD=0)
#   판별: 브로드 "Tier N" 매칭이 아니라 net-new "Desktop Edition" 리터럴(HEAD 전무=0)로 고정.
grep -rc "Desktop Edition" plugins/moai-code/ | grep -v ':0' | wc -l   # HEAD=0 → 후 ≥1 (PASS)
#   구조 확인: 공표 문서(README 또는 output-style)에 3 Tier 행
grep -ciE "Tier 1|Tier 2|Tier 3" plugins/moai-code/README.md plugins/moai-code/output-styles/*.md   # 후 ≥3

# AC-BD-005a — NET-NEW 게이트: 바이너리 탐지 분기 (HEAD=0)
grep -ciE "command -v moai|which moai|승격|promotion" "$HOOK"          # HEAD=0 → 후 ≥1 (PASS)

# AC-BD-005b — PRESERVE 제약(회귀 가드, NOT 신규 작업): fail-open exit 0 유지
grep -c "exit 0" "$HOOK"                                                # baseline 1, ≥1 유지
#   ↑ HEAD 자기통과(=1)는 의도된 것 — 기존 무설치 fail-open 패턴 PRESERVE 검증.
```

### 시나리오 4 — 버전 스탬프 SSOT 통합 (AC-BD-006a/b/c/d)
- **Given** 릴리스 준비 상태에서
- **When** 릴리스-체크리스트의 단일 버전 라인을 갱신하면
- **Then** 4개 위치가 지정 SSOT 센티넬 라인으로 통합되고, 정규화 후 서로 일치한다(D1 결정 후).
- **검증**:
```bash
CW=plugins/moai-cowork/.claude-plugin/plugin.json
CD=plugins/moai-code/.claude-plugin/plugin.json
BIN=/Users/goos/moai/moai-adk-go/pkg/version/version.go
TMPL=/Users/goos/moai/moai-adk-go/internal/template/templates/.moai/config/sections/system.yaml.tmpl

# AC-BD-006a — 정보용(비게이트): 4개 위치 존재 확인(pre-flight, 자기통과 by design)
grep '"version"' "$CW"; grep '"version"' "$CD"; grep 'Version =' "$BIN"; grep 'version:' "$TMPL"

# AC-BD-006b — PRESERVE 제약: tmpl은 플레이스홀더 유지(리터럴 값 금지)
grep -qF '{{.Version}}' "$TMPL" && echo "placeholder 유지 OK"          # baseline 존재, 유지

# AC-BD-006c — NET-NEW 게이트: 지정 VERSION-SSOT 센티넬 라인 (HEAD=0)
#   판별: 브로드 "SSOT" grep(HEAD 63개 무관 매칭)이 아니라 정밀 net-new 센티넬.
#   run-phase가 hugo.toml ⚠️SSOT 패턴을 미러링해 배치할 지정 마커:
#     "⚠️ VERSION-SSOT — 릴리스 버전 4개 위치 일괄 bump 체크리스트"
grep -rc "VERSION-SSOT" plugins/moai-code/ | grep -v ':0' | wc -l      # HEAD=0 → 후 ≥1 (PASS)
grep -riE "일괄 bump|release.?checklist|릴리스.?체크리스트" plugins/moai-code/ | wc -l   # HEAD=0 → 후 ≥1

# AC-BD-006d — D1-GATED(EC4): 정규화 후 concrete 리터럴 3곳 일치
norm() { sed -E 's/^v//; s/-rc[0-9]+$//; s/-[A-Za-z0-9.]+$//'; }
V_CW=$(grep '"version"' "$CW"  | grep -oE '[0-9]+\.[0-9]+\.[0-9]+[A-Za-z0-9.-]*' | norm)
V_CD=$(grep '"version"' "$CD"  | grep -oE '[0-9]+\.[0-9]+\.[0-9]+[A-Za-z0-9.-]*' | norm)
V_BIN=$(grep 'Version =' "$BIN" | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+[A-Za-z0-9.-]*' | norm)
[ "$V_CW" = "$V_CD" ] && [ "$V_CD" = "$V_BIN" ] && echo "정규화 리터럴 일치" || echo "diverge (pre-D1 정상)"
#   현재 실측: version.go=v3.0.0-rc6→정규화 3.0.0; plugin.json 2곳=0.1.0 → D1 미결이라 불일치가 정상.
```

## §D.2 엣지 케이스 (Edge Cases)

- **EC1.** 사용자가 인터뷰를 중단/재개(`/project resume`) — `.moai/skill-profile.yaml`이 부분 상태로 손상되지 않아야 한다.
- **EC2 (전방 참조 / forward-looking, AC 미게이트).** `moai init`이 후속 실행되어 `plugin-deployed` 마커를 만나는 경우 — `moai doctor`가 드리프트를 보고하고 파괴적 덮어쓰기 없이 승격을 제안. 이 동작은 §B R2에서 **이연된 REQ-BD-007**(spec.md §E "범위 제외 — moai 바이너리 소스 변경" 참조)에 해당하며, 본 SPEC의 **어떤 AC로도 검증하지 않는다**(후속 SPEC 소관). 통과 게이트가 아니라 미래 방향 기록이다.
- **EC3.** git·바이너리 부재 환경 — Tier 1 기능만 노출, Tier 2/3 배선은 무음(에러/차단 금지).
- **EC4.** 버전 정책 미결(D1) 상태 — 버전 라인은 현행값 유지. AC-BD-006c(NET-NEW 센티넬)는 D1과 무관하게 판별하며, AC-BD-006d(정규화 리터럴 일치)만 D1 정책 결정(플러그인 `0.1.0` → `3.0.x` 바인딩) 후 재검증한다.
- **EC5.** Windows — 세션-시작 훅 바이너리 탐지가 POSIX 전용이면 Windows에서 무음 fail-open으로 안전 저하.
- **EC6 (skill-profile ↔ global-profile 구분).** 지정 산출물 `.moai/skill-profile.yaml`은 **프로젝트 스킬-선택 CONFIG**로, SKILL.md L379 `### 2. moai-profile.md 생성 금지`가 금지하는 **글로벌 사용자 프로필**(`moai-profile.md`)과 별개다. run-phase는 둘을 혼동해서는 안 된다: 사용자 개인정보는 여전히 프로젝트 CLAUDE.md 한 곳에만, 스킬-선택 조준은 `.moai/skill-profile.yaml`에.

## §D.3 품질 게이트 (Quality Gate)

- 정본→플러그인 단방향 규약 위반 0건(AC-BD-008 orphan-edit grep = 0).
- 패리티 diff: 버전 라인 외 파일-집합 불일치 0건(AC-BD-002, non-empty 가드 통과 전제).
- verification-claim-integrity 준수: 바이너리 의존 훅 전수 카운트를 추정으로 주장하지 않음(CODE-002 이연).
- **판별력 게이트**: 모든 NET-NEW 게이트(001a·001b·003·004·005a·006c)가 HEAD에서 0(부재)임을 §D.6 증명으로 확인 — 자기통과 predicate 0건.

## §D.4 Definition of Done

- [ ] AC-BD-001a/b(NET-NEW), AC-BD-002(RUNTIME), AC-BD-003·004·005a(NET-NEW), AC-BD-006c(NET-NEW) 전부 PASS.
- [ ] PRESERVE 제약(AC-BD-001c·005b·006b·008) 회귀 없음(count ≥ HEAD baseline).
- [ ] AC-BD-006a 정보용 pre-flight 확인(게이트 아님); AC-BD-006d 정규화 리터럴 일치는 D1 결정 후 재검증(EC4).
- [ ] `/project init` 순증이 하위 호환을 깨지 않음(EC1·EC6 포함).
- [ ] `/moai:project` ↔ `moai init` 파일-집합 패리티(버전 라인 제외, non-empty 가드) 확인.
- [ ] moai-code `Desktop Edition` Tier 1~3 표 + 세션-시작 바이너리 탐지 분기(신규) + fail-open(유지) 배선.
- [ ] 4개 위치 버전 `VERSION-SSOT` 센티넬 라인 존재(신규); 값 일치는 D1 결정 후.
- [ ] AC-BD-007(displayName)은 R5 채택 시에만.
- [ ] 사용자 결정 D1(버전)·D2(표시명) 오케스트레이터 경유 확인 완료.
- [ ] **REQ-BD-007(doctor 드리프트 보고/승격) 이연 확인** — 본 SPEC의 AC로 검증하지 않음(spec.md §E 이연 근거 + EC2 전방 참조).

## §D.5 추적성 (Traceability)

REQ-BD-001 → AC-BD-001c / REQ-BD-002 → AC-BD-001a(c)·001b·001c / REQ-BD-003 → AC-BD-001a / REQ-BD-004 → AC-BD-001c / REQ-BD-005 → AC-BD-002 / REQ-BD-006 → AC-BD-003 / REQ-BD-008 → AC-BD-004 / REQ-BD-009 → AC-BD-005a / REQ-BD-010 → AC-BD-005b / REQ-BD-011 → AC-BD-006a·006b·006c / REQ-BD-012 → AC-BD-006d / REQ-BD-013 → AC-BD-007 / REQ-BD-014 → AC-BD-008.

**의도적 미커버(deferred, out-of-AC-scope)**: REQ-BD-007(doctor 드리프트 보고/승격) → **대응 AC 없음**. §B R2에서 §E로 이연됨(우발적 누락 아님). 근거: spec.md §E "범위 제외 — moai 바이너리 소스 변경". 시나리오는 EC2에 전방 참조로만 기록.

## §D.6 판별 증명 (Discrimination Proof — HEAD pre-state, 실측 2026-07-02)

모든 `≥1`/존재 predicate를 HEAD(6d78fbf)에서 실행한 결과. NET-NEW 게이트는 전부 **0(부재)** — 자기통과 불가·판별력 확보. PRESERVE/정보용은 자기통과가 **의도된** 것이며 회귀 가드/pre-flight로 명시 라벨.

| AC | predicate (요약) | HEAD 결과 | 판별? | 조치 |
|----|------------------|-----------|-------|------|
| AC-BD-001a | `grep -c skill-profile.yaml SKILL.md` | **0** | ✅ YES | 지정 산출물 경로 `.moai/skill-profile.yaml` (HEAD-absent 리터럴) |
| AC-BD-001b | `grep -ciE 폴더 규약 스캐폴드\|folder-convention scaffold SKILL.md` | **0** | ✅ YES | net-new 센티넬 문구 |
| AC-BD-001c | `grep -ciE 레거시 별칭\|/project init SKILL.md` | 14 (자기통과) | ⚙ PRESERVE | 회귀 가드로 라벨(≥14 유지); 신규 작업 아님 |
| AC-BD-001c | `grep -c '### 1\. CLAUDE.md 구조' SKILL.md` | 1 (자기통과) | ⚙ PRESERVE | CLAUDE.md 생성은 이미 동작 → 회귀 가드 |
| (구) AC-BD-001 | `test -f ./CLAUDE.md` (repo root) | 자기통과 | ❌→제거 | repo-root 자기통과 predicate 삭제, 런타임 P/ 체크로 대체 |
| (구) AC-BD-001 | `grep skill.?profile ./CLAUDE.md .moai/` | 18 (전부 SPEC 자기텍스트) | ❌→교체 | `.moai/` 자기참조 제거 → 특정 파일 grep(001a) |
| AC-BD-002 | 트리 diff(runtime A/B) | 실행 불가(하네스 필요) | ✅ RUNTIME | non-empty 가드 추가(빈-vs-빈 거짓통과 차단) |
| AC-BD-003 | `grep -rc plugin-deployed moai-code/` | **0** | ✅ YES | HEAD-absent 리터럴 `plugin-deployed` |
| AC-BD-004 | `grep -rc "Desktop Edition" moai-code/` | **0** | ✅ YES | 브로드 "Tier N" → net-new `Desktop Edition` 리터럴 고정 |
| (구) AC-BD-004 | `grep -ciE Tier 1\|2\|3 README+output-styles` | 0 (지정 파일) | ⚠ 취약 | 유지하되 `Desktop Edition` 센티넬로 보강(broad 매칭 회귀 방지) |
| AC-BD-005a | `grep -ciE command -v moai\|승격 HOOK` | **0** | ✅ YES | 바이너리 탐지 분기(신규) |
| AC-BD-005b | `grep -c "exit 0" HOOK` | 1 (자기통과) | ⚙ PRESERVE | fail-open 유지 회귀 가드로 라벨; 신규 작업 아님 |
| AC-BD-006a | 4개 위치 존재 grep | 4곳 존재(자기통과) | ⚙ 정보용 | 게이트에서 제외 → pre-flight로 강등 |
| AC-BD-006b | `grep -qF {{.Version}} tmpl` | 존재(자기통과) | ⚙ PRESERVE | 플레이스홀더 유지 제약으로 라벨 |
| (구) AC-BD-006c | `grep -riE SSOT\|일괄 bump\|release.?checklist moai-code/` | 63 (무관 자기통과) | ❌→교체 | 브로드 63 매칭 제거 |
| AC-BD-006c | `grep -rc "VERSION-SSOT" moai-code/` | **0** | ✅ YES | 지정 net-new 센티넬 라인 |
| AC-BD-006c | `grep -riE 일괄 bump\|release.?checklist\|릴리스.?체크리스트 moai-code/` | **0** | ✅ YES | 정밀 리터럴(브로드 SSOT 대체) |
| AC-BD-006d | 정규화 리터럴 3곳 일치 | 불일치(pre-D1 정상) | ✅ D1-GATED | EC4 게이트 |
| AC-BD-007 | `grep "MoAI Code — moai-adk Desktop Edition"` | **0** (현행 "MoAI Code") | ✅ OPTION | 채택 시 리터럴 |
| AC-BD-008 | `grep -rc parity-source moai-code/commands` | 12 (자기통과) | ⚙ PRESERVE | 회귀 가드(≥12) + orphan-edit grep |
| AC-BD-008 | parity-source 없는 편집 명령 파일(orphan) | 0 (현재 무orphan) | ⚙ 불변식 | 역방향 편집 방지 회귀 가드(문서화 불변식, spec.md §E) |

**결론**: NET-NEW 게이트 6개(001a·001b·003·004·005a·006c) + RUNTIME 1개(002) + D1-GATED(006d) + OPTION(007)이 판별 predicate. PRESERVE/정보용 5개(001c·005b·006a·006b·008)는 회귀 가드/pre-flight로 명시 라벨 — 자기통과가 의도된 것. 브로드-매칭/자기참조 self-passer 4개(repo-root CLAUDE.md, `.moai/` skill-profile, 브로드 SSOT 63, 브로드 Tier)는 제거·교체됨.
