# SPEC-MOC-PLUGIN-MOAI-V2-001 — 리서치 (research)

## §A. 원천 문서 지위

| 문서 | 지위 | 본 SPEC에서의 역할 |
|---|---|---|
| `.moai/reports/design-moai-plugin-v2-2026-07-08.md` | **설계 정본** (D-1~D-5 사용자 확정) | 아키텍처·개명·환경 매트릭스·로드맵의 SSOT |
| `.moai/reports/design-moai-adk-desktop-plugin-2026-07-08.md` | SUPERSEDED — 단 §3(템플릿 인벤토리)·§3.2(바이너리 커플링)·§9(P0-1~5 실측 증거)는 **원천 기록 정본** | P0 증거·인벤토리 인용처 |
| `.moai/project/{product,structure,tech}.md` (2026-07-09) | 현재 상태 ground truth (감사 완료) | 저장소 구조·버전 SSOT 위치·툴체인 |

## §B. P0-1~5 런타임 검증 증거 (v1 §9, 2026-07-08 실측, Claude Code 2.1.204)

캐너리 플러그인 + 로컬 디렉토리 마켓 + 헤드리스 `claude -p --model haiku` 프로브. 본 SPEC 설계 결정에 직결:

| 항목 | 판정 | 본 SPEC 반영 |
|---|---|---|
| P0-1 플러그인 `rules/` 로드 | **FAIL (미로드)** — 캐너리 토큰 부재 2회 교차 + plugin details에 Rules 카테고리 자체 없음. 죽은 페이로드 확정 | rules 61 → `templates/` 이동 (REQ-MV2-005) |
| P0-2 플러그인 `output-styles/` | **PASS — 단 네임스페이스 셀렉터 필수** (`"플러그인명:frontmatter name"`). bare name·slug는 무경고 무시 | output-styles 네이티브 잔류 + 스캐폴드는 `"moai:MoAI"` 포인터 1줄 (REQ-MV2-006·014) |
| P0-3 비정규 `Skill("...")` 해석 | **PASS** — 이름 유일 시 무네임스페이스 호출 동작. 충돌 시 미검증 | 정규화 MUST→SHOULD 하향 (REQ-MV2-020); 충돌 케이스는 P0-8로 이관 |
| P0-4 plugin `settings.json` `agent` 키 | **PASS** — 메인 스레드 페르소나 활성화 실동작 | D-5 opt-in 설계로 관리 — 본 SPEC 미동봉 (Out of Scope) |
| P0-5 hooks + `${CLAUDE_PLUGIN_DATA}` | **PASS** — SessionStart 매 세션 발화, 데이터 영속. 단 **uninstall 시 삭제** | 영속 상태는 프로젝트 `.moai/` 우선 (design §E) |

부수 발견(v1 §9): directory-source 마켓은 런타임이 소스 경로에서 로드(라이브 편집 반영) / commands는 내부적으로 Skills로 인벤토리화 / project-scope 설치도 user-level `installed_plugins.json` 등록 / uninstall이 캐시 사본 잔류(orphan).

## §C. 환경 매트릭스 프로버넌스 + R9 경고

- **CLI·Desktop 로컬 열**: 로컬 실측(P0 프로브 + 사용자 보고) — 고신뢰.
- **Web 열 (claude.ai/code·Desktop 원격)**: 공식 문서(`code.claude.com/docs/en/claude-code-on-the-web`) + 커뮤니티 이슈(#63028 웹 첫 세션 inactive, #25086 settings.local.json enabledPlugins 무시) 근거 — **본 머신에서 실행 불가, 저신뢰(R9)**. v1 §2.2("클라우드 세션 Bash/MCP 불가")와 신규 보고("웹 훅은 샌드박스 VM 실행") 사이의 표면상 충돌 해석: 차단되는 것은 **로컬 머신 자원·stdio 영속화·바이너리 설치**이며 VM 내 셸 실행 자체는 가능. 최종 확정은 **P0-w 사용자 실측**(Out of Scope — 사용자 게이트).
- 설계상 안전 장치: Web 셀이 문서와 다르게 동작해도 훅은 fail-open, settings 선언은 무해한 JSON — 실패-안전 구성(v2 §11 R9).

## §D. 잔여 검증 항목 배치

| 항목 | 내용 | 배치 |
|---|---|---|
| P0-6 | Desktop GUI 설치 E2E (+→Plugins→moai-claude→`/reload-plugins`) | 사용자 수행 대기 — Out of Scope |
| P0-w | Web 실측 (T2 커밋 repo → 자동 활성·#63028 재현·훅 발화·`$CLAUDE_CODE_REMOTE`) | 사용자 수행 대기 — Out of Scope |
| **P0-8** | T3 공존 typed-name 충돌 (`/moai:plan` 프로젝트 커맨드 vs 플러그인 `moai:plan`; 스킬 `moai` vs `moai:moai`) | **본 SPEC M6 (REQ-MV2-021)** — 본 저장소가 자연 테스트베드(`.claude/commands/moai/` 13 + `.claude/skills/moai` 보유). 결과는 progress.md §E.2 `P0-8-verdict:` 센티넬로 기록. 대응 구현(비활성 안내)은 P3 |

## §E. HEAD 실측 정본 (2026-07-09 — acceptance.md §D.6의 원천)

```yaml
census_head: 6f92d86   # "fix(plugins): 스킬 감사 14건 처리" — 병렬 세션 커밋 흡수 재기준선 (2026-07-09)
```

> **재기준선 노트**: 최초 census(pre-6f92d86 working tree) 대비 델타 = `moai-coder` 참조 34→**35**곳(11→**12**파일, moai-pm `diagnostic-protocol.md` 추가), moai-designer `agents/` 디렉토리 제거(3 에이전트 — 본 SPEC AC 무영향). 동시에 최초 census의 계수 결함 2건 정정: **skills 팩 29**(구 32는 `ls` alias가 `total`/`.`/`..`를 포함한 아티팩트 — `find -mindepth 1 -maxdepth 1 -type d` 재실측, `moai` 오케스트레이터 팩 존재 확인), **handle-* 20**(구 21은 오계수 — 총 .sh 24 = handle-* 20 + 게이트 4), **www plugins 구명칭 17곳**(구 12는 `_index.md`·`code/_index.md` 2파일만 합산한 결함 — 전 하위 파일 재실측).

### E.1 플러그인 인벤토리 (`plugins/moai-coder/`)

- plugin.json: `{name: "moai-coder", displayName: "코더", version: "3.1.0"}`
- commands: 14 (파리티 13 — 전부 `Skill("moai")` 참조 — + claude-agentic-coding.md 1)
- agents: 8 / skills 팩: **29**(`moai` 오케스트레이터 팩 포함 — find 실측) / rules: `rules/moai/` **61파일** / output-styles: **2**(einstein.md, moai.md — moai.md frontmatter `name: MoAI`) / `.mcp.json` 존재 / 총 파일 **354**
- hooks: `hooks.json` **20 이벤트**(SessionStart·PreCompact·SessionEnd·PreToolUse·PostToolUse·Stop·SubagentStop·PostToolUseFailure·SubagentStart·UserPromptSubmit·TeammateIdle·TaskCompleted·ConfigChange·StopFailure·PostCompact·InstructionsLoaded·CwdChanged·FileChanged·PermissionDenied·PermissionRequest) + 스크립트 **24**(handle-* **20** + 게이트 4: iggda-audit-preservation-guard·status-transition-ownership·sync-phase-quality-gate·team-ac-verify)
- `templates/`·`scripts/` 부재. `scaffold.sh`·`63028`·`재설치` grep 각 0.

### E.2 참조 census (`moai-coder` 리터럴)

- plugins/ 전체: **35곳 / 12파일** — moai-coder 자체 3파일 8곳(plugin.json 1·README 5·claude-agentic-coding.md 2) + moai-designer 스킬 2파일 2곳(moai-domain-copywriting·moai-workflow-gan-loop) + moai-pm 7파일 25곳(README 2·SKILL.md 3·references/core/{router 1, INDEX 1, coder-setup 7, init-protocol 10, diagnostic-protocol 1})
- `.claude-plugin/marketplace.json`: 2곳 (name + source)
- `.claude/` (agent-memory 제외): **1곳** — `.claude/agents/harness/harness-builder-skill-builder-specialist.md:26`
- www/content/plugins/: `moai-coder` 0, **구구명칭 `moai-code` 17곳**(_index.md 4 · code/_index.md 8 · chat/_index.md 3 · cowork/_index.md 1 · design/_index.md 1); `moai@moai-claude` 0
- 루트 README.md: 구 토폴로지 stale 정확 **5곳** (moai-cowork L14·23·33, moai-code L34, moai-design L35)
- moai-designer `agents/` 디렉토리: **제거됨**(6f92d86 — 구 3 에이전트. moai-coder agents 8과 무관, 본 SPEC AC 무영향)

### E.3 버전·검증 기준선

- ADK SSOT: `/Users/goos/moai/moai-adk-go/pkg/version/version.go` → `Version = "v3.0.0-rc8"` → 정규화 `3.0.0` (당시 DP-1 기본값 — 이후 사용자 확정으로 `"1.0.0"` 리셋 채택, plan.md §H)
- 마켓 metadata.version `5.0.0` / coder `3.1.0` / coworker `5.0.0` / designer·pm `0.2.0` (G5 드리프트 — 전면 정렬은 P4) — 6f92d86 재실측에서도 불변
- `claude plugin validate ./plugins/moai-coder` → **exit 0 (HEAD PASS)**; `claude plugin validate .claude-plugin/marketplace.json` → **exit 0 (HEAD PASS)** — AC-MV2-006b PRESERVE 라벨 근거 (6f92d86에서 재확인)
- `claude` CLI 가용 (`~/.local/bin/claude`), `plugin validate --strict` 옵션 존재
- quality.yaml `development_mode: "ddd"` — run-phase cycle_type 일치

### E.4 regex 안전성 검증

- `grep -E "moai-cowork\b"` → `moai-coworker` 비매치, `moai-code\b` → `moai-coder` 비매치 (word-boundary 확인 — EC-1)

## §F. Sources

- v1 보고서 Sources 6종 (code.claude.com/docs: plugins·plugin-marketplaces·discover-plugins·hooks-guide·desktop·skills)
- code.claude.com/docs/en/claude-code-on-the-web — Web 세션 repo-커밋 기반 로딩·샌드박스
- github.com/anthropics/claude-code issues #42142 · **#63028**(웹 첫 세션 플러그인 inactive) · #25086
- 본 저장소 HEAD 실측 (§E, 2026-07-09) + v1 §9 P0 실측 (2026-07-08, CC 2.1.204)
