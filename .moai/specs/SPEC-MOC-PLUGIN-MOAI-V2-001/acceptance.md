# SPEC-MOC-PLUGIN-MOAI-V2-001 — 수용 기준 (acceptance)

## §D.0 판별 모델 (Discrimination Model)

본 SPEC은 **행위 보존 재구조화**(rename + move + 참조 갱신)이므로 predicate를 4유형으로 분류하고, 전 predicate를 HEAD `6f92d86`(2026-07-09 재기준선 — 병렬 세션 커밋 흡수)에서 실측했다(§D.6):

- **NET-NEW 게이트**: HEAD에 부재한 지정 산출물/센티넬(예: `plugins/moai`, `dispatch.sh`, `63028`, `P0-8-verdict:`). HEAD에서 FAIL/0 → run 후 PASS/≥1. 자기통과 불가.
- **REMOVAL 게이트**: HEAD에 존재하는 것의 소거(예: `plugins/moai-coder`, `moai-coder` 참조 35곳, handle-* 20종). HEAD에서 FAIL/≥N → run 후 PASS/0.
- **PRESERVE 회귀 가드**: HEAD에서 이미 PASS하며 **self-pass가 의도된** characterization(인벤토리 패리티, 이벤트 집합, marketplace validate). DDD의 behavior-preservation 계약 그 자체 — 명시 라벨로 구분.
- **RUNTIME 행위**: 실행해야만 판정 가능(scaffold dry-run/병합/백업, plugin validate, P0-8). empty-vs-empty false-pass 방지를 위해 비어있지 않음(non-empty) 가드 동반.

**자기참조 트랩 회피**: 어떤 predicate도 `.moai/**`를 grep하지 않는다(본 SPEC 문서·역사 보고서가 `moai-coder`를 정당 언급). stale-ref 스윕은 live tree(plugins/ · www/content/plugins/ · 루트 README.md · .claude-plugin/ · .claude/agents/harness/ 특정 파일)로 한정하며, `.claude/agent-memory/**`는 제외한다. `grep -E "moai-cowork\b"`류 word-boundary는 `moai-coworker`에 매치하지 않음을 확인했다(EC-1).

## §D. 수용 기준 매트릭스 (AC Matrix)

| AC | 유형 | REQ | M | 검증 명령 (기대값) |
|---|---|---|---|---|
| AC-MV2-001a | NET-NEW+REMOVAL | 001 | M1 | `test -d plugins/moai && test ! -d plugins/moai-coder` (exit 0) |
| AC-MV2-001b | NET-NEW | 001 | M1 | `jq -r '.name, .displayName, .version' plugins/moai/.claude-plugin/plugin.json` → `moai` / `코더` / `1.0.0`(DP-1 확정 2026-07-09 — 버전 리셋) |
| AC-MV2-001c | NET-NEW+REMOVAL | 002·003 | M1 | `jq -r '.plugins[].name' .claude-plugin/marketplace.json` → 정확히 4개, `moai` 포함, `moai-coder` 0; `jq -r '.plugins[] \| select(.name=="moai") \| .source'` → `./plugins/moai` |
| AC-MV2-001d | PRESERVE | 008 | M1 | `ls plugins/moai/commands/*.md \| wc -l`=14; `find plugins/moai/agents -type f \| wc -l`=8; `ls -d plugins/moai/skills/*/ \| wc -l`=29; `ls plugins/moai/output-styles/`={einstein.md, moai.md}; `test -f plugins/moai/.mcp.json` (기준선: research.md §E — self-pass 의도됨) |
| AC-MV2-002a | NET-NEW+REMOVAL | 005 | M2 | `find plugins/moai/templates/claude/rules/moai -type f \| wc -l`=61 AND `test ! -d plugins/moai/rules` |
| AC-MV2-002b | PRESERVE | 005 | M2 | `git diff --stat -M100 <M1커밋>..<M2커밋> -- 'plugins/moai/rules' 'plugins/moai/templates/claude/rules'` → 61건 전부 rename(R100), 내용 변경 라인 0 (git mv 전제 — plan §D) |
| AC-MV2-002c | NET-NEW | 007a | M2 | `test -f plugins/moai/templates/CLAUDE.md` AND `grep -c 'parity-source: internal/template/templates/CLAUDE.md' plugins/moai/templates/CLAUDE.md` ≥1 (EC-6: ADK 원천 경로 명시 parity-source 마커가 유일한 기계 판별자 — 루트 CLAUDE.md는 parity-source 0 실측) |
| AC-MV2-002d | NET-NEW | 007b | M2 | `jq -r '.outputStyle' plugins/moai/templates/claude/settings.project.json`=`moai:MoAI`; `jq '.extraKnownMarketplaces["moai-claude"]' ...` ≠ null; `jq '.enabledPlugins["moai@moai-claude"]' ...`=`true` |
| AC-MV2-002e | NET-NEW | 007c | M2 | `find plugins/moai/templates/moai/config/sections -name '*.yaml' \| wc -l` ≥27 |
| AC-MV2-002f | PRESERVE | 006 | M2 | `ls plugins/moai/output-styles/ \| wc -l`=2 AND `grep -c '^name: MoAI' plugins/moai/output-styles/moai.md`=1 (셀렉터 `moai:MoAI` 계약 — self-pass 의도됨) |
| AC-MV2-003a | NET-NEW | 009 | M3 | `test -f plugins/moai/hooks/dispatch.sh && bash -n plugins/moai/hooks/dispatch.sh` (exit 0) |
| AC-MV2-003b | REMOVAL | 009 | M3 | `find plugins/moai/hooks -name 'handle-*.sh' \| wc -l`=0 |
| AC-MV2-003c | NET-NEW+PRESERVE | 009·012 | M3 | `jq -r '(.hooks // .) \| .. \| .command? // empty' plugins/moai/hooks/hooks.json \| grep -vc 'dispatch.sh'`=0 AND 이벤트 키 집합 = research.md §E의 20종과 동일 (`jq -r '(.hooks // .) \| keys[]' \| sort` diff 0) |
| AC-MV2-003d | NET-NEW | 010·011·012 | M3 | `grep -c 'CLAUDE_CODE_REMOTE' plugins/moai/hooks/dispatch.sh` ≥1 AND `grep -c 'command -v moai' plugins/moai/hooks/dispatch.sh` ≥1 AND 최종 fail-open `exit 0` 존재 (`tail -5 ... \| grep -c 'exit 0'` ≥1) |
| AC-MV2-003e | NET-NEW | 009 | M3 | `ls plugins/moai/hooks/gates/*.sh \| wc -l` ≥4 (DP-2 채택 시 ≥5), 각 파일 `bash -n` exit 0 |
| AC-MV2-004a | NET-NEW | 013 | M4 | `test -x plugins/moai/scripts/scaffold.sh && bash -n plugins/moai/scripts/scaffold.sh` (exit 0) |
| AC-MV2-004b | RUNTIME | 013 | M4 | 임시 디렉토리에서 `scaffold.sh --dry-run` exit 0 AND 생성 계획 출력 ≥1줄(non-empty 가드) AND 임시 디렉토리 파일 생성 0 (`find <tmp> -type f \| wc -l`=0) |
| AC-MV2-004c | RUNTIME | 013 | M4 | 임시 디렉토리 실행 후: `CLAUDE.md` 존재, `.claude/rules/moai` 61파일, `.moai/config/sections` ≥27 yaml, `grep -rlE '\{\{(PROJECT_NAME\|VERSION\|DATE)\}\}' <tmp> \| wc -l`=0 (iter-1 D6 수정: 3개 토큰 전부 + `wc -l` 스칼라 판정 — 구 `grep -rc`는 파일별 카운트 출력이라 비스칼라) |
| AC-MV2-004d | RUNTIME | 014 | M4 | 사전 seed `.claude/settings.json`=`{"model":"opus"}` 후 실행 → `jq -r '.model'`=`opus`(보존) AND 3키(outputStyle/extraKnownMarketplaces/enabledPlugins) 추가됨 |
| AC-MV2-004e | RUNTIME | 013 | M4 | 동일 디렉토리 2회차 실행 → `.moai-backups/` 하위 백업 엔트리 ≥1 |
| AC-MV2-004f | NET-NEW | 016 | M4 | `grep -rn '63028' plugins/moai/ \| wc -l` ≥1 (완료 메시지/워크플로우 안내 — HEAD 0) |
| AC-MV2-004g | NET-NEW | 015 | M4 | `grep -rn 'scaffold.sh' plugins/moai/skills/ \| wc -l` ≥1 (/moai:project 배선 — HEAD 0) |
| AC-MV2-005a | REMOVAL | 017 | M5 | `grep -rn 'moai-coder' plugins/ --include='*.md' --include='*.json' --include='*.sh' --include='*.yaml' \| wc -l`=0 (HEAD 35 — 6f92d86, 12파일) |
| AC-MV2-005b | REMOVAL+NET-NEW | 019 | M5 | `grep -rEn 'moai-code\b\|moai-coder\b' www/content/plugins/ \| wc -l`=0 (HEAD 17 — 6f92d86, 5파일) AND `grep -rn 'moai@moai-claude' www/content/plugins/ \| wc -l` ≥1 (HEAD 0) |
| AC-MV2-005c | REMOVAL+NET-NEW | 018 | M5 | `grep -cE 'moai-cowork\b\|moai-code\b\|moai-design\b\|moai-coder\b' README.md`=0 (HEAD 5) AND `moai-coworker`·`moai-designer`·`moai-pm`·`moai@moai-claude` 각 ≥1 |
| AC-MV2-005d | NET-NEW | 004 | M5 | `grep -c '재설치' plugins/moai/README.md` ≥1 (HEAD 0 — 구 README 기준) |
| AC-MV2-005e | REMOVAL | 017 | M5 | `grep -rn 'plugins/moai-coder' .claude/agents/harness/ \| wc -l`=0 (HEAD 1); `grep -rn 'moai-coder' .claude-plugin/ \| wc -l`=0 (HEAD 2 — 001c와 동일 파일, 교차 확인) |
| AC-MV2-005f | NET-NEW (SHOULD) | 020 | M5 | `grep -l 'Skill("moai:moai")' plugins/moai/commands/*.md \| wc -l` ≥13 (HEAD 0) — SHOULD: 미달 시 FAIL 아닌 debt 기록 |
| AC-MV2-006a | RUNTIME | 022 | M6 | `claude plugin validate ./plugins/moai` exit 0 (SHOULD: `--strict`도 exit 0) |
| AC-MV2-006b | PRESERVE(RUNTIME) | 022 | M6 | `claude plugin validate .claude-plugin/marketplace.json` exit 0 (HEAD에서 이미 PASS — 회귀 가드, self-pass 의도됨) |
| AC-MV2-006c | RUNTIME+NET-NEW | 021 | M6 | `awk '/^## §E.2/,/^## §E.3/' .moai/specs/SPEC-MOC-PLUGIN-MOAI-V2-001/progress.md \| grep -c '^P0-8-verdict:'` ≥1 (HEAD 0 — iter-1 D1 수정: placeholder에서 센티넬 리터럴 제거 + 행 선두 `^` 앵커 이중 방어; awk 범위 한정으로 acceptance.md 자기텍스트 매치 차단) |
| AC-MV2-006d | PRESERVE(RUNTIME) | 022 | M6 | `find plugins/moai -name '*.sh' -exec bash -n {} +` exit 0; `cd www && hugo --gc --minify` exit 0; `node www/scripts/check-links.mjs` exit 0 (www 콘텐츠 수정에 대한 회귀 가드) |

## §D.1 Given-When-Then 시나리오

### 시나리오 1 — 개명 마이그레이션 (AC-MV2-001a~d)

- **Given** HEAD에 `plugins/moai-coder/`(v3.1.0, 인벤토리 = research.md §E)가 존재하고 `plugins/moai/`는 부재하다.
- **When** M1이 `git mv` + plugin.json/marketplace.json 갱신을 수행한다.
- **Then** `plugins/moai/` manifest가 `{name: "moai", displayName: "코더", version: "1.0.0"}`이고, marketplace는 4-plugin(톰스톤 0)이며, Layer 1 인벤토리(14/8/29/2/.mcp.json)는 개명 전과 동일하다.

### 시나리오 2 — 2계층 재배치 (AC-MV2-002a~f)

- **Given** rules 61파일이 플러그인 루트 `rules/moai/`(P0-1 FAIL 죽은 페이로드)에 있고 `templates/`가 부재하다.
- **When** M2가 rules를 `templates/claude/rules/moai/`로 `git mv`하고 CLAUDE.md·settings.project.json·`.moai` 골격을 ADK 정본에서 vendor한다.
- **Then** templates에 61+1+1+≥27 산출물이 존재하고, rules 이동은 100% rename(내용 무변경)이며, settings.project.json이 Web 활성화 3키를 선언하고, output-styles 2종은 플러그인 네이티브로 잔류한다.

### 시나리오 3 — 훅 통합 + Web 분기 (AC-MV2-003a~e)

- **Given** hooks.json 20 이벤트가 handle-* 20 + 게이트 4의 24 스크립트로 분산되어 있다.
- **When** M3가 dispatch.sh + gates/로 통합한다.
- **Then** 모든 이벤트 command가 dispatch.sh를 가리키고(이벤트 집합 20종 보존), handle-*은 0이며, dispatch.sh는 `$CLAUDE_CODE_REMOTE=true`면 바이너리 프로브 생략 → 게이트 전용, 바이너리 감지 시 `exec moai hook <event>`, 매핑 없으면 무음 `exit 0`(fail-open)이다.

### 시나리오 4 — 스캐폴드 보존 병합 (AC-MV2-004b~e)

- **Given** 임시 프로젝트 디렉토리에 사용자 소유 `.claude/settings.json`=`{"model":"opus"}`가 존재한다.
- **When** `scaffold.sh --dry-run` 후 실제 실행, 이어 2회차 실행을 수행한다.
- **Then** dry-run은 무기록 + 계획 출력, 실행은 Layer 2 트리 생성 + `{{TOKEN}}` 치환 완료 + `model: opus` 보존 + 3키 추가, 2회차는 `.moai-backups/` 백업을 남긴다.

### 시나리오 5 — P0-8 typed-name 충돌 실측 (AC-MV2-006c)

- **Given** 본 저장소는 T3 프로젝트(프로젝트 `.claude/commands/moai/` 13 + `.claude/skills/moai`)이며 개명된 플러그인 `moai`(커맨드 `moai:plan`, 스킬 `moai:moai`)가 공존한다.
- **When** M6가 헤드리스 프로브(`claude -p` 계열)로 `/moai:plan`·`Skill("moai")` 해석 우선순위를 실측한다.
- **Then** progress.md §E.2에 `P0-8-verdict:` 센티넬 라인 + 관찰 증거(verbatim)가 기록된다(안내 문구 구현은 P3 — 기록까지가 본 SPEC).

## §D.2 엣지 케이스 (Edge Cases)

- **EC-1 word-boundary**: `moai-cowork\b`는 `moai-coworker`에, `moai-code\b`는 `moai-coder`에 매치하지 않음(HEAD에서 검증 완료). AC-MV2-005b/c의 regex 안전 전제.
- **EC-2 자기참조 트랩**: `.moai/specs/**`·`.moai/reports/**`·CHANGELOG·`.claude/agent-memory/**`의 `moai-coder` 언급은 역사 기록 — 스윕 제외(§D.0). 이를 갱신하는 run은 스코프 위반.
- **EC-3 gitignore 런타임 상태**: `plugins/**/.moai` 런타임 디렉토리는 gitignore 대상 — AC-MV2-005a는 `--include` 화이트리스트로 자산 파일만 검사.
- **EC-4 ADK SSOT 드리프트 (해소됨 — DP-1 확정 2026-07-09)**: DP-1이 고정 리터럴 `"1.0.0"` 리셋으로 사용자 확정되어 plugin.json 버전은 ADK SSOT에 비연동 — run 시점 `version.go` 드리프트는 AC-MV2-001b에 영향 없음. (본 EC는 이력 보존용으로 유지; blocker→AC-update 경로 불필요.)
- **EC-5 `--strict` validate 경고**: `claude plugin validate --strict`는 미인식 필드에 exit 1 가능 — 기본 AC는 non-strict exit 0(MUST), strict는 SHOULD. strict FAIL 시 사유를 progress.md에 기록.
- **EC-6 CLAUDE.md 정본 판별 (iter-1 D2 정정)**: 유일한 기계 판별자는 **ADK 원천 경로를 명시한 parity-source 마커**(`parity-source: internal/template/templates/CLAUDE.md` ≥1 — REQ-MV2-007(a) 지정 센티넬)다. 루트 CLAUDE.md 실측(6f92d86): `claude.mo.ai.kr` **0회** — 구 서브-predicate(`claude.mo.ai.kr`=0)는 오전제로 **철회**(naive 루트 복사도 0을 반환해 vacuous); `parity-source` **0회** — 따라서 경로 명시 마커 predicate가 naive 루트 복사를 실제로 판별. 의도적 위조 스탬프는 AC 방어 범위 밖(리뷰어 검토 몫).
- **EC-7 마켓 캐시 개명 잔재**: 로컬 `~/.claude/plugins/` 캐시의 구 moai-coder 사본은 본 저장소 밖 — AC 대상 아님. 재설치 공지(AC-MV2-005d)가 사용자측 완화.

## §D.3 품질 게이트 (Quality Gate)

- 언어 툴체인: 컴파일 없음 — `bash -n` 전수 + `claude plugin validate` + Hugo 빌드 + link-check가 본 프로젝트의 게이트(tech.md 정합).
- 훅 게이트: 마일스톤 커밋마다 `git status --short`로 편집 경계(plan §D) 준수 확인.
- 커버리지 개념 대응: RUNTIME AC(004b~e, 006a~d)가 실행 커버리지 역할 — 전부 verbatim 출력을 progress.md §E.2에 증거로 남긴다(verification-claim-integrity §3.2).

## §D.4 Definition of Done

1. AC-MV2-001a ~ 006d 전부 PASS(005f는 SHOULD — 미달 시 debt 기록으로 DoD 통과 가능).
2. 마일스톤별 conventional commit이 main에 존재(M1~M6, SPEC ID 포함) + push 완료(`git rev-list --count --left-right origin/main...HEAD` = `0 0`).
3. progress.md §E.2에 RUNTIME AC verbatim 증거 + `P0-8-verdict:` 기록, §E.3 run-phase audit-ready 신호 기입.
4. 판별 증명(§D.6)의 HEAD 수치와 run 후 수치가 전 행에서 예상 방향으로 이동(NET-NEW 0→≥1, REMOVAL N→0, PRESERVE 불변).

## §D.5 추적성 (Traceability)

| REQ | AC | Milestone |
|---|---|---|
| REQ-MV2-001 | 001a·001b | M1 |
| REQ-MV2-002·003 | 001c | M1 |
| REQ-MV2-004 | 005d | M5 |
| REQ-MV2-005 | 002a·002b | M2 |
| REQ-MV2-006 | 002f | M2 |
| REQ-MV2-007 | 002c·002d·002e | M2 |
| REQ-MV2-008 | 001d | M1 |
| REQ-MV2-009 | 003a·003b·003c·003e | M3 |
| REQ-MV2-010·011 | 003d | M3 |
| REQ-MV2-012 | 003c·003d | M3 |
| REQ-MV2-013 | 004a·004b·004c·004e | M4 |
| REQ-MV2-014 | 004d | M4 |
| REQ-MV2-015 | 004g | M4 |
| REQ-MV2-016 | 004f | M4 |
| REQ-MV2-017 | 005a·005e | M5 |
| REQ-MV2-018 | 005c | M5 |
| REQ-MV2-019 | 005b | M5 |
| REQ-MV2-020 (SHOULD) | 005f | M5 |
| REQ-MV2-021 | 006c | M6 |
| REQ-MV2-022 | 006a·006b·006d | M6 |

## §D.6 판별 증명 (Discrimination Proof — HEAD `6f92d86` 재기준선 실측 2026-07-09)

| Predicate | HEAD 실측값 | 판별? |
|---|---|---|
| `test -d plugins/moai` | 부재 (FAIL) | ✅ NET-NEW |
| `test ! -d plugins/moai-coder` | 존재 (FAIL) | ✅ REMOVAL |
| plugin.json jq (신경로) | 파일 부재 (FAIL) | ✅ NET-NEW |
| marketplace `moai` exact 엔트리 | 0 (`moai-coder`만 존재) | ✅ NET-NEW+REMOVAL |
| `templates/` 디렉토리 | 부재 (`ls` ABSENT 확인) | ✅ NET-NEW |
| `templates/claude/rules/moai` 61 | 0 (rules는 `rules/moai/` 61) | ✅ NET-NEW |
| `test ! -d plugins/moai/rules` | rules/ 존재 (FAIL, 경로 조정) | ✅ REMOVAL |
| `hooks/dispatch.sh` | 부재 | ✅ NET-NEW |
| `handle-*.sh` count | 20 | ✅ REMOVAL |
| `CLAUDE_CODE_REMOTE` grep (hooks/dispatch.sh 한정 — AC-MV2-003d 대상 파일) | 0 (dispatch.sh 부재. iter-1 D5 정정: 플러그인 전체 스코프로는 문서 참조 1건 존재 — skills/moai-foundation-cc/reference/claude-code-cli-reference-official.md:323 — AC 판별 무영향) | ✅ NET-NEW |
| settings.project.json 3키 | 파일 부재 | ✅ NET-NEW |
| `scripts/scaffold.sh` | scripts/ 부재 | ✅ NET-NEW |
| `63028` grep (plugin tree) | 0 | ✅ NET-NEW |
| `scaffold.sh` grep (skills/) | 0 | ✅ NET-NEW |
| `moai-coder` in plugins/ | 35 (12파일 — moai-pm 7 · designer 2 · coder 자체 3) | ✅ REMOVAL |
| `moai-code\b\|moai-coder\b` in www/content/plugins/ | 17 (_index 4 · code 8 · chat 3 · cowork 1 · design 1) | ✅ REMOVAL |
| `moai@moai-claude` in www/content/plugins/ | 0 | ✅ NET-NEW |
| 루트 README 구명칭 | 5 (L14·23·33·34·35) | ✅ REMOVAL |
| `재설치` in plugin README | 0 | ✅ NET-NEW |
| `plugins/moai-coder` in .claude/agents/harness/ | 1 | ✅ REMOVAL |
| `Skill("moai:moai")` in commands | 0 | ✅ NET-NEW (SHOULD) |
| `^P0-8-verdict:` in progress.md §E.2 (awk 한정 + 행 선두 앵커) | 0 (iter-1 D1 수정 후 재실측 — placeholder 센티넬 리터럴 제거; 수정 전에는 1로 자기통과였음) | ✅ RUNTIME+NET-NEW |
| `claude plugin validate ./plugins/moai` | 경로 부재 (FAIL) | ✅ RUNTIME |
| `claude plugin validate` marketplace | **PASS (HEAD)** | ⚠️ PRESERVE — 회귀 가드, self-pass 의도됨 (라벨) |
| Layer 1 인벤토리 14/8/29/2 | PASS (HEAD, 구경로) | ⚠️ PRESERVE — characterization, self-pass 의도됨 (라벨) |
| hooks.json 이벤트 20종 | PASS (HEAD) | ⚠️ PRESERVE — 집합 동일성 가드 (라벨) |
| output-styles `name: MoAI` | PASS (HEAD) | ⚠️ PRESERVE — 셀렉터 계약 가드 (라벨) |
| hugo 빌드·link-check | PASS (HEAD 추정 — pre-flight 재확인) | ⚠️ PRESERVE — www 회귀 가드 (라벨) |

NET-NEW/REMOVAL/RUNTIME 게이트 중 HEAD self-pass = **0건** (plan-audit iter-1 D1 수정 — progress.md placeholder 센티넬 제거 — 후 재실측으로 복원된 상태). PRESERVE 5건은 전부 의도된 self-pass로 명시 라벨됨(§D.0).
