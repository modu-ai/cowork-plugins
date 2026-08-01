# SPEC-MOC-PLUGIN-MOAI-V2-001 — 구현 계획 (plan)

## §A. 컨텍스트 (Context)

v2 설계 로드맵 **P2 단계**의 본 저장소 소관분: 개명(moai-coder→moai) + 2계층 재구조화 + 훅 통합 + scaffold.sh/`/moai:project` 완성 + 참조 갱신 + 검증. 행위 보존 재구조화가 지배적이므로 **cycle_type=ddd**(ANALYZE-PRESERVE-IMPROVE)로 수행한다:

- **ANALYZE**: research.md §E의 HEAD 인벤토리 실측(2026-07-09, `census_head: 6f92d86` 재기준선)이 characterization 기준선이다 — commands 14 · agents 8 · skills 29 · output-styles 2 · rules 61 · hooks 24스크립트(handle-* 20 + 게이트 4)/20이벤트 · 참조 census.
- **PRESERVE**: 각 마일스톤의 PRESERVE AC(인벤토리 패리티, git rename 검출, 이벤트 집합 동일성)가 characterization test 역할.
- **IMPROVE**: 마일스톤 단위 점진 변환 + 커밋. 실패 시 해당 마일스톤 단위 revert.

## §B. 알려진 이슈 / 실측 발견 (Known Issues)

1. **output-styles 2종 vs 설계 문서 3종**: v1/v2 문서는 3종(moai·moai-easy·einstein)을 기술하나 플러그인 vendor는 2종(moai.md·einstein.md)만 보유. moai-easy.md 추가 vendor는 P1 export 소관 — 본 SPEC은 현행 2종 보존만 계약한다(스코프 확장 금지).
2. **게이트 5종 vs 플러그인 4종**: v1의 순수 bash 게이트 5종 중 `gateguard-fact-force.sh`는 플러그인에 미vendor. M3에서 ADK 템플릿에서 vendor(SHOULD).
3. **www 카탈로그는 두 세대 전 명칭**: `moai-coder`가 아닌 `moai-code`를 사용(17곳 — `www/content/plugins/**` 전 하위: _index 4·code/_index 8·chat/_index 3·cowork/_index 1·design/_index 1). REQ-MV2-019는 두 구명칭 모두 소거한다.
4. **`.claude/agents/harness/harness-builder-skill-builder-specialist.md:26`**: 이 저장소 하네스 에이전트가 `plugins/moai-coder/skills/` 경로를 참조 — M5 갱신 대상(유일한 .claude/ 잔존 참조, agent-memory 제외).
5. **ADK 버전 rc 드리프트 (해소됨)**: SSOT `v3.0.0-rc8`(2026-07-09). DP-1이 고정 리터럴 `"1.0.0"` 리셋으로 사용자 확정(2026-07-09)되어 plugin.json 버전은 ADK SSOT에 비연동 — ADK 드리프트는 AC-MV2-001b에 더 이상 영향 없음(acceptance.md EC-4 해소 주석).
6. **HEAD `6f92d86` 재기준선 (2026-07-09)**: 병렬 세션 커밋("fix(plugins): 스킬 감사 14건", plugins/ 80파일)을 흡수해 전 census 재실측. 델타: `moai-coder` 참조 35곳/12파일(+`diagnostic-protocol.md`), moai-designer `agents/` 제거(coder agents 8 무영향·본 SPEC AC 무영향). 최초 census 계수 결함 정정 2건: skills 팩 **29**(구 32는 ls 아티팩트), handle-* **20**(구 21은 오계수). run 착수 전 §C.3 재실측으로 추가 드리프트 감지 시 blocker→AC 갱신.

## §C. Pre-flight (착수 전 확인, informational)

1. `git status --short plugins/ | head` — 병렬 세션 오염 없음 확인(Pre-Spawn Sync Check는 오케스트레이터 소관).
2. `claude plugin validate ./plugins/moai-coder && claude plugin validate .claude-plugin/marketplace.json` — HEAD 기준선 PASS 재확인(회귀 가드 anchor).
3. research.md §E 인벤토리 수치 재실측(rules 61 · hooks 24/20 · 참조 35/17/2/1, 기준 `census_head: 6f92d86`) — 드리프트 시 acceptance.md §D.6 갱신 후 착수. (구 항목 "ADK 버전 재확인"은 DP-1 고정 리터럴 확정으로 불필요 — §B.5.)

## §D. 제약 (Constraints — plan)

- **git 전략 (사용자 확정 2026-07-09)**: **main 직접 푸시 (Hybrid Trunk, 1인 OSS 관행)** — Tier L 기본 PR 라우팅(manager-git 경유)을 **명시적으로 override**한다. manager-git PR 단계 생략. 마일스톤 단위 conventional commit(`feat|refactor|docs(SPEC-MOC-PLUGIN-MOAI-V2-001): M<N> ...`) 후 push. force-push·`--no-verify` 금지.
- **development_mode**: `ddd`(quality.yaml 실측 일치). 디렉토리 이동은 `git mv` 사용(rename 검출 100% 보장 — AC-MV2-002b의 기계 검증 전제).
- **편집 경계**: `plugins/**`, `.claude-plugin/marketplace.json`, `README.md`(루트), `www/content/plugins/**`, `.claude/agents/harness/harness-builder-skill-builder-specialist.md`, 본 SPEC 디렉토리(progress.md). 그 외 `.moai/**`·역사 기록물 무수정(C-5).
- **manager-develop frontmatter 권한**: `draft → in-progress` 전환 + `updated` 갱신만 허용. spec/plan/acceptance 본문 수정 필요 시 blocker 반환 → manager-spec 재위임(D-NEW-1).

## §E. 자기 검증 (Self-Verification, plan-phase)

- SPEC ID regex self-check: `SPEC | MOC | PLUGIN | MOAI | V2 | 001 → PASS` (spec.md HISTORY 기록).
- frontmatter 12필드 canonical + `tier: L` + `related_specs` — snake_case alias 0.
- Out of Scope: `### Out of Scope — <topic>` H3 6개 + `-` 불릿 충족(OutOfScopeRule).
- AC 판별력: 전 predicate HEAD 실측 완료(acceptance.md §D.6) — NET-NEW 게이트 전부 HEAD FAIL/0, PRESERVE는 명시 라벨(self-pass 의도됨), 자기참조 트랩 회피(`.moai/**` grep 없음).

## §F. 마일스톤 (Milestones, 우선순위 기반 — 시간 추정 없음)

> 순서 근거: M1을 선행해 이후 모든 작업이 `plugins/moai/` 경로에서 1회만 수행되게 한다(경로 이중 터치 방지). M2~M4는 상호 독립(파일 스코프 비중첩)이나 순차 커밋을 기본으로 한다. M5는 M1 확정 명칭에 의존, M6은 전체에 의존.

| M | 제목 | 우선순위 | 파일 스코프 (구체) | 종료 기준 (AC) |
|---|---|---|---|---|
| M1 | 개명 + 마켓 갱신 | High | `git mv plugins/moai-coder plugins/moai`; `plugins/moai/.claude-plugin/plugin.json`(name·displayName·version=`"1.0.0"` — DP-1 확정); `.claude-plugin/marketplace.json`(엔트리 name/source, 톰스톤 없음) | AC-MV2-001a·b·c·d |
| M2 | 2계층 재배치 | High | `git mv plugins/moai/rules/moai plugins/moai/templates/claude/rules/moai` + `rules/` 제거; `templates/CLAUDE.md`(ADK 정본 vendor + parity-source); `templates/claude/settings.project.json`(3키); `templates/moai/config/sections/*.yaml`(≥27, `{{TOKEN}}` 형태) — ADK 정본 위치: `/Users/goos/moai/moai-adk-go/internal/template/templates/` | AC-MV2-002a~f |
| M3 | 훅 통합 | High | `plugins/moai/hooks/dispatch.sh`(신규); `hooks/gates/*.sh`(기존 4종 이관 + gateguard-fact-force vendor SHOULD); `hooks/hooks.json`(20 이벤트 전부 dispatch.sh 라우팅); `hooks/moai/handle-*.sh` 20종 삭제 | AC-MV2-003a~e |
| M4 | scaffold.sh + /moai:project | High | `plugins/moai/scripts/scaffold.sh`(신규 — cp+sed·--dry-run·백업·user-owned 보존·settings 보존 병합·#63028 안내); `skills/moai/workflows/project*` 또는 `skills/moai-workflow-project/`에 scaffold.sh 배선 | AC-MV2-004a~g |
| M5 | 참조 갱신 | Medium | `plugins/moai-pm/`(README + skills/project 6파일 — SKILL.md·router·INDEX·coder-setup·init-protocol·diagnostic-protocol); `plugins/moai-designer/skills/`(2파일); `plugins/moai/README.md`(개명 반영 + `재설치` 공지); 루트 `README.md`(4-plugin 현행 토폴로지); `www/content/plugins/{_index,code/_index,chat/_index,cowork/_index,design/_index}.md`(17 참조 5파일 전부 — §B.3, iter-1 D3 수정); `.claude/agents/harness/harness-builder-skill-builder-specialist.md`; (SHOULD) 커맨드 13종 `Skill("moai:moai")` 정규화 | AC-MV2-005a~f |
| M6 | 검증 + P0-8 실측 | Medium | 파일 수정 없음(검증 전용). P0-8 실측(본 저장소 T3 공존: 헤드리스 `claude -p` 프로브로 `/moai:plan` typed-name 해석 확인) → `progress.md §E.2`에 `P0-8-verdict:` 기록; `claude plugin validate` ×2; `bash -n` 전수; `cd www && hugo --gc --minify`; `node www/scripts/check-links.mjs` | AC-MV2-006a~d |

## §G. 안티패턴 (Anti-Patterns to Avoid)

- 본 저장소 루트 `CLAUDE.md`를 `templates/CLAUDE.md`로 복사 — 정본은 ADK 템플릿(EC-6). 루트 CLAUDE.md는 이 프로젝트 전용 지침이다.
- `.moai/**`를 stale-ref 스윕 대상에 포함 — SPEC 자기텍스트·역사 보고서가 `moai-coder`를 정당하게 언급(자기참조 트랩, C-5).
- handle-* 스크립트를 dispatch.sh와 병존 — 죽은 코드 + 이중 발화 위험. M3에서 완전 제거.
- 훅에 blocking(exit 2) 도입 — fail-open 위반(C-3).
- marketplace.json에 `moai-coder` 톰스톤 엔트리 유지 — 카탈로그 오염(REQ-MV2-003).
- 스킬 본문 리라이트·기능 추가 — 행위 보존 위반(C-1). 참조 치환만.
- plain `mv` 사용 — `git mv`로 rename 검출 보장(AC-MV2-002b 전제).
- 시간 추정 기입 — 우선순위 라벨만.

## §H. 사용자 결정 (RESOLVED — 2026-07-09 사용자 확정)

| # | 결정 | 확정값 (2026-07-09) |
|---|---|---|
| DP-1 | plugin.json `version` 재정렬 값 | **`"1.0.0"` 리셋** — 제시 3옵션(①`"3.0.0"` ADK SSOT 정규화 ②`"3.1.0"` 유지 ③`"4.0.0"` major 신호) 전부가 아닌 사용자 override. 근거: 개명 = 마켓플레이스 신규 플러그인 정체성 → clean-slate 버저닝. 반영: REQ-MV2-001·spec §A.2·AC-MV2-001b 리터럴 `1.0.0`·§D.1 시나리오 1·EC-4 해소·design §G |
| DP-2 | gateguard-fact-force.sh vendor 여부 | **① vendor 채택**(SPEC 기본값 확인) — REQ-MV2-009의 SHOULD 등급 유지, hooks/gates 5종 목표 |

두 항목 모두 사용자 확정 완료 — run-phase Implementation Kickoff에서 추가 결정 불필요.

## §MX. MX 태그 계획 (run-phase 생성 시 부착)

| 대상 | 태그 | 근거 |
|---|---|---|
| `plugins/moai/hooks/dispatch.sh` — 이벤트 라우팅 진입점 | `@MX:ANCHOR` | hooks.json 20 이벤트 전부가 fan-in하는 불변 계약(이벤트명→게이트 매핑 + fail-open) |
| `plugins/moai/hooks/dispatch.sh` — `$CLAUDE_CODE_REMOTE` 분기 + 최종 `exit 0` | `@MX:WARN` + `@MX:REASON` | 분기 오류 시 Web 세션 전체 훅이 바이너리 프로브에 낭비되거나(성능) exit≠0으로 사용자 흐름 차단(치명) |
| `plugins/moai/scripts/scaffold.sh` — 토큰 치환·산출 매니페스트 | `@MX:ANCHOR` | 결정론 생성 계약({{TOKEN}} 집합 + 산출 트리)이 /moai:project와 T2 티어의 전제 |
| `plugins/moai/scripts/scaffold.sh` — settings.json 보존 병합 + 백업/`--dry-run`/user-owned 보존 | `@MX:WARN` + `@MX:REASON` | 사용자 settings 파괴 위험 구역 — 덮어쓰기 금지 불변식(REQ-MV2-014) |

## §I. 교차 참조

- spec.md §B(요구사항)·§E(Out of Scope) / acceptance.md §D(AC 매트릭스)·§D.6(판별 증명) / design.md(설계 증류) / research.md §E(HEAD 실측 정본)
- `.claude/rules/moai/development/spec-frontmatter-schema.md` § Status Transition Ownership Matrix
- 설계 정본: `.moai/reports/design-moai-plugin-v2-2026-07-08.md` §4~§9
