# SPEC-MOC-BOOTSTRAP-DESKTOP-001 — 구현 계획 (plan.md)

> 상태: draft · Tier M · phase v3.0.0. 본 문서는 구현 접근·마일스톤·리스크를 기술한다(시간 추정 금지, 우선순위 기반).

## §A. 컨텍스트 (Context)

본 SPEC은 3개 트리를 소유 범위로 하되, 정본→플러그인 단방향 vendor-sync를 전제한다:

- `plugins/moai-cowork/skills/project/**` — `/project init` 순증(폴더 스캐폴드 + 스킬 프로파일 산출물)
- `plugins/moai-code/**` — 명령/훅/Tier 표/표시명/버전
- `internal/template/templates/**`(moai-adk-go) — 정본 SSOT(읽기·계획; 릴리스 시 vendor-sync 의무)

Tier M 판단 근거: 3개 트리·5개 요구사항 그룹이나, 대부분이 기존 메커니즘 재사용(레거시 `/project init`, parity-source 주석, 무설치 훅, hugo.toml SSOT 주석)이며 신규 발명이 적다. design.md/tasks.md가 필요한 Tier L 판단 밀도에는 못 미친다 → 4-파일 세트(spec/plan/acceptance/progress)로 충분.

## §B. 알려진 이슈 / 실측 발견 (Known Issues)

1. **`/project init`은 이미 레거시 별칭이다.** 재정의 시 기존 트리거 하위 호환을 깨면 안 된다(REQ-BD-004). 순증만 허용.
2. **버전 값 발산은 설계상 1지점.** `moai init`은 `{{.Version}}` 주입, `/moai:project`는 무설치라 리터럴 `plugin-deployed vX.Y.Z` 기입. 패리티 검증은 이 라인을 제외(modulo)해야 한다(AC-BD-002).
3. **플러그인 버전(0.1.0) ↔ 바이너리(v3.0.0-rc6) 불일치.** R4는 플러그인을 3.0.x로 이동시키는 정책 결정을 포함한다 — plan 승인 전 사용자 확인 필요(§F 옵션).
4. **moai-cowork에는 `commands/` 디렉터리가 없다.** 진입점은 스킬. `/project init` 순증은 `skills/project/SKILL.md` 확장으로 구현한다(신규 `commands/` 생성 아님).
5. **바이너리 의존 훅 전수 목록은 미확정** — CODE-002 소관. 본 SPEC은 fail-open 패턴 재사용만 다룬다.

## §C. Pre-flight (착수 전 확인, informational)

```bash
# 1) 정본 템플릿 존재
ls /Users/goos/moai/moai-adk-go/internal/template/templates/.claude/commands/moai/ | wc -l   # ~13 tmpl
# 2) parity-source 마커 카운트(정보용)
grep -l "parity-source" /Users/goos/MoAI/claude.mo.ai.kr/plugins/moai-code/commands/*.md | wc -l
# 3) 무설치 훅 fail-open 패턴 존재
grep -c "exit 0" /Users/goos/MoAI/claude.mo.ai.kr/plugins/moai-code/hooks/moai/handle-session-start.sh
# 4) 버전 위치 4곳 현재값
grep '"version"' /Users/goos/MoAI/claude.mo.ai.kr/plugins/moai-code/.claude-plugin/plugin.json
grep '"version"' /Users/goos/MoAI/claude.mo.ai.kr/plugins/moai-cowork/.claude-plugin/plugin.json
grep 'Version =' /Users/goos/moai/moai-adk-go/pkg/version/version.go
grep 'version:' /Users/goos/moai/moai-adk-go/internal/template/templates/.moai/config/sections/system.yaml.tmpl
```

## §D. 제약 (Constraints — plan)

- 시간 추정 금지, 우선순위(High/Medium/Low)만 사용.
- 정본→플러그인 단방향. 플러그인을 정본으로 편집 금지.
- 최소주의: 기존 메커니즘 재사용 우선.
- 모든 마일스톤은 기계 검증 가능한 AC로 종료한다.

## §E. 자기 검증 (Self-Verification, plan-phase audit-ready 요약)

- SPEC ID pre-write self-check: `decomposition: SPEC ✓ | MOC ✓ | BOOTSTRAP ✓ | DESKTOP ✓ | 001 ✓ → PASS`
- 12 canonical frontmatter 필드 전부 존재, `created`/`updated` 사용(스네이크 별칭 없음), `tags` 콤마 문자열.
- Out of Scope: 6개 `### Out of Scope — <topic>` H3 서브헤딩 + `-` 불릿.
- 상세 audit-ready 신호는 `progress.md` §E.1 참조.

## §F. 마일스톤 (Milestones, 우선순위 기반)

### M1 — `/project init` 순증 (Priority High)
- `skills/project/SKILL.md`에 폴더 규약 스캐폴드 생성 + 스킬 프로파일 산출물(persisted) 생성 동작 추가.
- 하위 호환: bare `/project` ≡ `/project init` 유지.
- 종료 조건: AC-BD-001.

### M2 — 패리티 계약 문서화 + 검증 하네스 (Priority High)
- `/moai:project`와 `moai init`의 출력 트리 패리티 계약을 moai-code 문서에 명문화.
- 버전 스탬프 리터럴(`plugin-deployed vX.Y.Z`) 기입 동작(REQ-BD-006).
- 파일-집합 diff 하네스(버전 라인 제외).
- 종료 조건: AC-BD-002, AC-BD-003.

### M3 — Desktop Edition Tier 표 + 세션-시작 배선 (Priority High)
- moai-code에 Tier 1~3 능력 표 공표(README 또는 output-style).
- 세션-시작 훅: 바이너리 탐지 → 존재 시 1줄 승격 안내 / 부재 시 무음 fail-open(기존 패턴 재사용).
- 종료 조건: AC-BD-004, AC-BD-005.

### M4 — 버전 스탬프 SSOT 통합 (Priority Medium)
- 4개 위치 버전을 단일 릴리스-체크리스트 라인으로 통합(hugo.toml SSOT-주석 패턴 미러링).
- 플러그인 버전 ↔ 바이너리 v3.0.x 바인딩(사용자 결정 후).
- 종료 조건: AC-BD-006.

### M5 — (SHOULD) 표시명 옵션 (Priority Low)
- R5 표시명 변경은 옵션. 기본값 유지. 사용자 채택 시 marketplace.json + plugin.json displayName 갱신.
- 종료 조건: AC-BD-007(옵션 채택 시에만).

## §G. 안티패턴 (Anti-Patterns to Avoid)

- 플러그인 트리를 정본으로 취급해 역방향 편집(REQ-BD-014 위반).
- `/project init`을 신규 명령으로 중복 생성(레거시 별칭 존재 무시).
- 버전 스탬프 라인을 패리티 검증에 포함시켜 거짓 실패 유발.
- 바이너리 의존 훅 전수 카운트를 추정으로 주장(CODE-002 소관, verification-claim-integrity §1.1 surface 3 위반).
- 시간 추정 삽입.

## §H. 사용자 결정 필요 (Blockers → 오케스트레이터 경유)

- **D1 (R4 버전 정책):** 플러그인 버전을 0.1.0 → 3.0.x로 이동해 바이너리에 바인딩할지. 기본 제안 = 바인딩(REQ-BD-012). run-phase 착수 전 사용자 확인 권장.
- **D2 (R5 표시명):** moai-code displayName을 "MoAI Code — moai-adk Desktop Edition"으로 변경할지. 기본 = 유지.

> 두 결정은 SPEC 산출물 작성을 막지 않는다(옵션으로 인코딩됨). run-phase Implementation Kickoff 시점에 오케스트레이터가 AskUserQuestion으로 확인한다.

## §I. 교차 참조

- spec.md §B(요구사항), acceptance.md(§D AC 매트릭스), progress.md(§E audit 신호).
- 형제: SPEC-MOC-PLUGIN-CODE-001/002, SPEC-MOC-PLUGIN-COWORK-002.
