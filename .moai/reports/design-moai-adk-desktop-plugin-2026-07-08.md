# moai-adk → Claude Desktop Code 플러그인화: 제약 분석 및 상세 설계

> **[SUPERSEDED by `design-moai-plugin-v2-2026-07-08.md`]** — D-1~D-4 확정 + 환경 매트릭스 개정(Web=repo-커밋 기반)으로 v2가 설계 정본. 본 문서는 템플릿 인벤토리(§3)·P0 실측 증거(§9)의 원천 기록으로 유지.

- 작성: 2026-07-08 (session 8f3b6245)
- 조사 원천: moai-adk-go 템플릿 전수 분석 + Claude Code 공식 문서 검증 + 본 저장소 선행 자산(moai-coder v3.1.0) 분석
- 지위: 설계 보고서 (SPEC 아님 — SPEC화는 후속 결정)

---

## 1. 요약 (TL;DR)

1. **템플릿의 91%는 그대로 플러그인화 가능**하다. moai-adk-go 임베디드 템플릿 432파일 중 ~394파일(스킬 240·룰 61·에이전트 7·커맨드 13·output-style 3 등)은 `moai` 바이너리와 무관한 순수 프롬프트 자산이다. 바이너리 의존은 ~34파일(8%)로, 전부 훅 래퍼(32) + statusline(1) + `iggda-phase-driver`(1)에 집중되어 있다.
2. **Claude Desktop Code 탭은 플러그인을 공식 지원**한다(GUI 설치 + `/plugin`). 단, **클라우드 세션은 Bash/MCP/LSP/외부 바이너리가 전부 차단**되므로 훅·git·바이너리 기반 기능은 로컬 세션 전용이다.
3. **플러그인이 실을 수 없는 것**: `CLAUDE.md`, 프로젝트 `settings.json`(권한·훅 등록), rules(미문서화), output-styles(미문서화), statusline(미문서화). 이들은 **스캐폴드 명령(`/moai:project`)이 사용자 프로젝트에 생성**하는 방식으로 전달해야 한다 — 기존 `SPEC-MOC-BOOTSTRAP-DESKTOP-001`의 "명령은 둘, 정본은 하나" 설계와 일치.
4. **백지 설계가 아니다**: `plugins/moai-coder` v3.1.0이 이미 무설치 포트로 존재하고 마켓플레이스(`moai-claude`)도 살아 있다. 본 설계는 **2계층 아키텍처(플러그인 네이티브 / 스캐폴드 페이로드)로의 재구조화 + 이연된 스캐폴드·parity 도구의 완성**이 핵심이다.
5. **최우선 권고**: ① 런타임 미확인 항목(P0 체크리스트 7종) 검증 → ② moai-adk-go에 `moai plugin export`(vendor-sync 실체화) 신설 → ③ moai-coder 2계층 재구조화 + `/moai:project` 스캐폴드 완성.

---

## 2. 제약사항 조사 결과 (공식 문서 검증)

### 2.1 플러그인이 실을 수 있는 것 / 없는 것

| 구성요소 | 플러그인 배포 | 비고 |
|---|---|---|
| commands (`commands/*.md`) | ✅ | `/<plugin>:<cmd>` 네임스페이스. flat 파일만(서브디렉토리는 이름에 미반영) |
| agents (`agents/*.md`) | ✅ | YAML frontmatter 포함 전체 지원 |
| skills (`skills/<name>/SKILL.md`) | ✅ | 세션 시작 시 메타데이터 자동 로드, `/<plugin>:<skill>` |
| hooks (`hooks/hooks.json`) | ✅ | 27개 이벤트 전부 지원. JSON 전용. `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`(영속), `$CLAUDE_PROJECT_DIR` 사용 가능 |
| MCP 서버 (`.mcp.json`) | ✅ | 클라우드 세션 제외 |
| LSP 서버 (`.lsp.json`) | ✅ | 클라우드 세션 제외 |
| 실행 파일 (`bin/`) | ✅ | **Bash 도구 PATH에 자동 등록** — 부트스트랩 스크립트 배포 가능 |
| 백그라운드 모니터 (`monitors/monitors.json`) | ✅ | 선택적 활용 |
| 기본 settings (`settings.json`) | △ | 문서화된 키는 `agent`, `subagentStatusLine` 수준. permissions 배포는 미문서화 |
| `CLAUDE.md` / 프로젝트 메모리 | ❌ | 프로젝트 소유 — 스캐폴드로만 전달 가능 |
| 프로젝트 `settings.json` (권한·훅 등록·env) | ❌ | 플러그인이 덮어쓸 수 없음 |
| output-styles | ❌(미문서화) | **P0 런타임 검증 필요** — 현행 moai-coder가 동봉 중이나 로드 근거 없음 |
| statusline | ❌(미문서화) | Tier-3(바이너리) 전용으로 분류 |
| rules (`.claude/rules/`) | ❌(미문서화) | **P0 런타임 검증 필요** — 동상 |

핵심 구조 제약:
- `.claude-plugin/` 안에는 `plugin.json`만. 나머지 디렉토리는 전부 플러그인 루트 레벨.
- 설치 시 플러그인은 `~/.claude/plugins/cache/`로 **복사**됨(심링크 아님). `../` 외부 참조는 복사되지 않음 → 모든 페이로드는 플러그인 트리 내부에 있어야 함.
- 명시적 용량 제한은 미문서화. 대형 트리는 clone/캐시 비용으로만 부담.

### 2.2 Claude Desktop Code 환경 매트릭스

| 기능 | CLI | Desktop 로컬 세션 | Desktop 클라우드 세션 |
|---|---|---|---|
| 플러그인 설치/로드 | ✅ `/plugin` | ✅ GUI(+ → Plugins → Add plugin) + `/reload-plugins` | ✅ (로드 자체는 가능) |
| Bash / 외부 바이너리 | ✅ | ✅ (로컬 머신 환경 그대로) | ❌ |
| MCP | ✅ | ✅ | ❌ |
| LSP | ✅ | ✅ | ❌ |
| hooks 실행 | ✅ | ✅ (CLI와 동일 발화) | ❌ 사실상 불가 (셸 실행 불가) |
| git / worktree | ✅ | ✅ (세션별 자동 worktree 격리) | △ (제한적) |
| skills / agents / commands | ✅ | ✅ | ✅ |

시사점: **Desktop 로컬 세션은 CLI와 실질 동등**하다(로컬 머신에서 실행, 샌드박스 없음, `moai` 바이너리가 설치되어 있으면 훅에서 그대로 실행 가능). 설계상 진짜 하한선은 **클라우드 세션**이며, 이때는 프롬프트 자산(스킬·에이전트·커맨드)만 동작한다.

### 2.3 배포·업데이트 제약

- 버전 해석 우선순위: `plugin.json version` → 마켓 엔트리 `version` → git commit SHA.
- 서드파티 마켓플레이스 자동 업데이트 **기본 비활성** → 사용자에게 `/plugin marketplace update moai-claude` 안내 필요.
- `version` 명시 = 고정(pin). bump 전까지 업데이트 미전파.
- 관리형 배포: `extraKnownMarketplaces` + `enabledPlugins`로 팀 기본 설정 가능.

---

## 3. moai-adk-go 템플릿 분석

### 3.1 인벤토리 (총 432파일)

임베디드 루트: `internal/template/embed.go` (`//go:embed all:templates` + `catalog.yaml`).

| 영역 | 파일수 | 내용 |
|---|---|---|
| `.claude/skills/` | 240 | 28팩. `moai` 오케스트레이터 팩(46, `workflows/{plan,run,sync,project}` 프롬프트 본문 포함)이 핵심 |
| `.claude/rules/moai/` | 61 | core 10 · development 15 · workflow 17 · languages 16 · design 1 · quality 1 |
| `.claude/hooks/moai/` | 38 | `handle-*.sh.tmpl` 32(바이너리 래퍼) + standalone `.sh` 6(그중 5개는 순수 bash) |
| `.claude/commands/moai/` | 13 | 전부 `Use Skill("moai") with arguments: <sub> $ARGUMENTS` thin wrapper |
| `.claude/agents/moai/` | 7 | manager-spec/develop/docs/git + plan/sync-auditor + builder-harness |
| `.claude/output-styles/moai/` | 3 | moai.md, moai-easy.md, einstein.md |
| `.claude/settings.json.tmpl` | 1 | 훅 32종 등록 + statusline + permissions(`Bash(moai:*)`) + env/model |
| `.moai/config/` | 38 | sections 29(그중 `.tmpl` 7) + astgrep-rules 5 + evaluator-profiles 4 |
| `.moai/` 기타 | 22 | project/db 7, evolution 5, docs 3, 골격 디렉토리들 |
| 루트 | 9 | `CLAUDE.md`(24.8KB), `.mcp.json.tmpl`, `.gitignore`, `.claudeignore`, `.github/` 3, `.git_hooks/` 2 |

### 3.2 바이너리 커플링 분류

| 분류 | 파일수 (비율) | 내용 | 플러그인화 판정 |
|---|---|---|---|
| (a) 바이너리 독립 | ~394 (91%) | 스킬·룰·에이전트·커맨드·output-style·CLAUDE.md·config yaml·순수 bash 훅 5종 | **그대로 이식 가능** |
| (b) 바이너리 의존 | ~34 (8%) | `handle-*.sh` 32(`moai hook <event>`), `status_line.sh`(`moai statusline`), `iggda-phase-driver.sh`(`moai spec audit`) | 드롭 or detect-and-degrade 재설계 |
| (c) 하이브리드 | ~2 (1%) | `settings.json.tmpl`(훅 등록만 죽음, permissions/env/outputStyle 유효), `system/project.yaml.tmpl`(버전 스탬프) | 축소판 재구성 |

바이너리를 실행하지 않는 standalone 훅 5종(포팅 가능한 게이트 자산): `gateguard-fact-force.sh`, `status-transition-ownership.sh`, `sync-phase-quality-gate.sh`, `team-ac-verify.sh`, `iggda-audit-preservation-guard.sh`.

프롬프트 자산 내 `moai` CLI **언급**(실행 아닌 지시문)은 스킬 ~26곳 + 룰 ~30곳 + CLAUDE.md 2곳 — 무설치 배포 시 문구 정비 대상(Tier-3 조건부 문구로 전환).

### 3.3 렌더링·업데이트 메커니즘과 시사점

- Go `text/template`(strict, `missingkey=error`), `.tmpl` 55개(커맨드 13 + 훅 래퍼 32 + settings + mcp + statusline + config 7). 컨텍스트: `ProjectName`, `Version`, `Platform`(windows 분기 30회), `ConversationLanguage`(ko/en/ja/zh 다국어 블록 16회), `HookOptIn`, `ResolvedMoaiPath` 등.
- `moai update`의 보존 규칙: `isMoaiManaged`(`.claude/{skills,rules,commands,output-styles,hooks}/moai*` 등 → 덮어씀) vs `isUserOwnedNamespace`(`harness-*`, `agents/local/` 등 → 절대 보존). **스캐폴드 업데이트 설계에 그대로 이식할 목록.**
- `catalog.yaml`: 팩 단위 tier + version + SHA-256 — **plugin export의 parity manifest 원천으로 재사용 가능.**
- 시사점: 플러그인은 Go 렌더러가 없으므로 `.tmpl`의 Go 조건문(플랫폼·언어)은 **export 빌드 시점에 해소**하고, 프로젝트별 가변값만 단순 토큰(`{{PROJECT_NAME}}` 등)으로 남겨 스캐폴드 시 치환해야 한다.

---

## 4. 선행 자산 현황 (기준선)

### 4.1 이미 있는 것

- **마켓플레이스**: `.claude-plugin/marketplace.json` — `moai-claude`(owner modu-ai), 4 플러그인(coworker 5.0.0 / designer 0.2.0 / **coder 3.1.0** / pm 0.2.0).
- **plugins/moai-coder = 무설치 포트 1차 구현**: commands 14(파리티 13 + 비파리티 1), agents 8, skills 29팩/241파일, hooks.json + 스크립트 24(19이벤트, `${CLAUDE_PLUGIN_ROOT}`, fail-open), rules 61, output-styles 2, `.mcp.json` 정적 렌더. `parity-source: …@b8354304c` 마커 체계.
- **설계 계약(SPEC-MOC-BOOTSTRAP-DESKTOP-001)**: `/moai:project` ↔ `moai init` 동일 트리(유일 차이 `system.yaml` `version: "plugin-deployed vX.Y.Z"`), Tier 1 플러그인 단독 ≈ 방법론 90% / Tier 2 git / Tier 3 바이너리, vendor-sync는 정본→플러그인 단방향, 바이너리 감지 시 Tier-3 승격 안내(session-start 훅, fail-open).

### 4.2 갭·부채

| # | 갭 | 영향 |
|---|---|---|
| G1 | `/moai:project` 스캐폴드 로직·parity 하네스 **미구현**(SPEC 이연) | Tier-1 온보딩 미완 — 프로젝트 귀속 자산(CLAUDE.md·rules·config) 전달 불가 |
| G2 | vendor-sync 도구 `scripts/render-templates.sh` **부재**(phantom 참조) | 정본→플러그인 동기화가 수작업, 드리프트 누적 |
| G3 | rules/output-styles를 플러그인 최상위에 동봉 | 공식 미지원 컴포넌트 — **로드되지 않는 죽은 페이로드**일 가능성 (P0 검증) |
| G4 | 커맨드가 비정규 `Skill("moai")` 참조 | 플러그인 네임스페이스에서 해석 실패 가능 (P0 검증) |
| G5 | 버전 드리프트: 마켓 5.0.0 vs coder 3.1.0, designer/pm은 SSOT 체크리스트 밖 | 업데이트 전파·신뢰성 훼손 |
| G6 | `moai doctor`의 `plugin-deployed` 마커 인식(REQ-BD-007) 이연 | Tier-3 승격 경로 미완 |
| G7 | www 카탈로그가 구 토폴로지(3-plugin+story) 기술 | 사용자 안내 불일치 |

---

## 5. 상세 설계

### 5.1 아키텍처: 2계층 (플러그인 네이티브 / 스캐폴드 페이로드)

```
┌────────────────────────────────────────────────────────────┐
│ Layer 1 — 플러그인 네이티브 (Claude Code가 직접 로드)          │
│  commands 13 · agents 7 · skills 28팩 · hooks.json+dispatch │
│  · .mcp.json · bin/moai-install(옵션)                        │
│  → 설치 즉시 어느 저장소에서든 동작 (스캐폴드 불필요)            │
├────────────────────────────────────────────────────────────┤
│ Layer 2 — 스캐폴드 페이로드 (templates/, 로더는 읽지 않음)      │
│  CLAUDE.md · rules 61 · output-styles 3 ·                   │
│  settings.project.json(축소판) · .moai 골격+config 29+docs    │
│  → /moai:project 가 사용자 프로젝트에 생성 (프로젝트 귀속 자산)  │
└────────────────────────────────────────────────────────────┘
```

원칙: **Claude Code가 플러그인에서 로드하는 것은 플러그인에, 프로젝트에 있어야만 효력이 생기는 것은 스캐폴드에.** 중복 배치(현행 rules/output-styles 최상위 동봉)는 제거한다.

### 5.2 컴포넌트 매핑 테이블 (템플릿 → 목적지)

| 템플릿 자산 | 목적지 | 처리 방식 |
|---|---|---|
| skills 28팩 (240) | 플러그인 `skills/` | 그대로. 커맨드의 스킬 참조는 정규화(`Skill("<ns>:moai")`) |
| commands 13 | 플러그인 `commands/` | thin wrapper 유지. `.tmpl` 다국어 블록은 export 시 해소 |
| agents 7 | 플러그인 `agents/moai/` | 그대로 |
| hooks: 순수 bash 게이트 5 | 플러그인 `hooks/gates/` | `hooks.json`으로 이벤트 연결, `$CLAUDE_PROJECT_DIR` 기준 동작 |
| hooks: 바이너리 래퍼 32 | 플러그인 `hooks/dispatch.sh` **1개로 통합** | 바이너리 감지 → `exec moai hook <event>`; 부재 → 게이트 실행 or `exit 0` |
| `iggda-phase-driver.sh` | 플러그인 hooks (조건부) | `moai spec audit` 부재 시 auto-advance 생략(현행 fallback 유지) |
| `.mcp.json.tmpl` | 플러그인 `.mcp.json` | 정적 렌더 (기적용) |
| statusline (`status_line.sh`) | **배포 안 함** | Tier-3 승격 시 `moai update`가 생성 |
| `CLAUDE.md` | `templates/CLAUDE.md` | 스캐폴드 + 단순 토큰 치환 |
| rules 61 | `templates/claude/rules/moai/` | 스캐폴드 → 프로젝트 `.claude/rules/moai/` |
| output-styles 3 | `templates/claude/output-styles/moai/` | 스캐폴드 + `settings.project.json`의 `outputStyle` 지정 |
| `settings.json.tmpl` | `templates/claude/settings.project.json` | **훅 등록 32종 + statusline 제거**, permissions(`Bash(moai:*)` 제외)/env/outputStyle/model 유지 |
| `.moai/config` 29 + docs + project/db + evolution 골격 | `templates/moai/` | 스캐폴드. `.tmpl` 7종은 export 시 단순 토큰형으로 변환 |
| `.github/`, `.git_hooks/` | `templates/`(옵션) | git 사용 프로젝트에만 스캐폴드(질문 게이트) |

### 5.3 캐퍼빌리티 티어 (기존 Tier 체계 확장)

| Tier | 환경 | 제공 능력 |
|---|---|---|
| **T0** | Desktop 클라우드 세션 | 스킬·에이전트·커맨드만. PLAN›RUN›SYNC 방법론 프롬프트 동작, 훅 게이트·git·MCP 없음 — 품질 게이트는 모델 자율 수행으로 강등 |
| **T1** | 무설치 로컬 (CLI/Desktop 로컬) | T0 + hooks(순수 bash 게이트) + MCP(context7) + git 직접 명령. 방법론 ≈ 90% |
| **T2** | T1 + 스캐폴드 완료 | + CLAUDE.md 헌법 + rules + output-style(MoAI 페르소나) + `.moai` config/specs 체계 — **실질 완전체** |
| **T3** | + `moai` 바이너리 | + statusline·세션 레지스트리·harness 학습·`spec audit`·LSP 게이트·doctor·update |

### 5.4 훅 설계

- **단일 디스패처**: `hooks.json`의 각 이벤트 → `${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.sh <event>`. 현행 24개 스크립트 → 1 디스패처 + 5 게이트로 축소.
- 디스패처 로직: ① `command -v moai` 성공 → `exec moai hook <event>` (T3 자동 활성) ② 부재 → 이벤트에 매핑된 순수 bash 게이트 실행 ③ 매핑 없음 → `exit 0` (fail-open, 침묵).
- 상태 기록: 플러그인 영속 상태는 `${CLAUDE_PLUGIN_DATA}`, 프로젝트 상태는 `$CLAUDE_PROJECT_DIR/.moai/`(스캐폴드된 경우만).
- session-start: 바이너리 존재 + 프로젝트 `system.yaml`의 `plugin-deployed` 마커 감지 시 1줄 Tier-3 승격 안내(현행 REQ-BD-009/010 유지).

### 5.5 스캐폴드 설계 (`/moai:project`)

- **실행 주체**: `moai` 스킬의 project 워크플로우. 오케스트레이터가 AskUserQuestion으로 프로젝트명·언어·git 전략 수집 → **번들 스크립트 `scripts/scaffold.sh` 1회 실행**(cp + sed 토큰 치환)으로 결정론적 생성. LLM이 파일을 개별 복사하지 않는다(토큰·오류 절감).
- 토큰 치환: `{{PROJECT_NAME}}`, `{{LANGUAGE}}`, `{{VERSION}}`, `{{DATE}}` 수준의 단순 문자열만. Go 조건문은 export 시 이미 해소됨.
- 멱등성·안전: `--dry-run` 지원, 기존 파일은 `.moai-backups/`로 백업 후 갱신, `isUserOwnedNamespace` 목록(harness-* 등) 절대 보존 — 바이너리 `moai update`의 보존 규칙을 그대로 이식.
- 버전 마커: `system.yaml` `version: "plugin-deployed v<plugin.json version>"` — 바이너리 doctor의 승격 감지 접점(G6 해소 전제).
- T0(클라우드) 폴백: Bash 불가 시 최소 세트(CLAUDE.md + config 핵심)만 Write 도구로 생성하고 제약 고지.
- 업데이트: `/moai:project --update` → 동일 스크립트가 managed 네임스페이스만 갱신. 프로젝트 `template_version` vs 플러그인 버전 비교 후 diff 요약 제시.

### 5.6 vendor-sync 파이프라인: `moai plugin export` 신설 (moai-adk-go)

phantom `render-templates.sh`(G2)를 Go 서브커맨드로 실체화:

```
moai plugin export --lang ko --out <dir>
  1. 임베디드 템플릿 로드 (fs.Sub)
  2. .tmpl 렌더: Platform/HookOptIn/언어 조건 해소, 프로젝트 가변값은 {{TOKEN}}으로 보존
  3. 훅 래퍼 32종 → hooks.json + dispatch.sh 생성 (5.4 설계)
  4. settings.json.tmpl → templates/claude/settings.project.json (훅 등록 제거판)
  5. rules/output-styles/CLAUDE.md/.moai → templates/ 스캐폴드 영역으로 배치
  6. plugin.json 생성 (version = 바이너리 버전 SSOT)
  7. parity manifest 출력: catalog.yaml 기반 팩별 SHA-256 + parity-source@commit 스탬프
```

- CI에서 실행 → 산출 트리를 claude.mo.ai.kr `plugins/moai-coder/`로 자동 PR(단방향 동기화 강제).
- parity 검증 하네스: export 산출물 vs 저장소 플러그인 트리의 SHA 비교 job — 드리프트를 CI에서 차단(G2·G5 동시 해소).

### 5.7 버전·업데이트 전략

- SSOT = moai-adk-go 바이너리 버전. `plugin.json version`은 export가 스탬프. 마켓 엔트리는 version 생략(plugin.json 우선 규칙 활용).
- 사용자 전파: 서드파티 마켓 자동 업데이트 기본 꺼짐 → README·session-start 안내에 `/plugin marketplace update moai-claude` 명시. 관리형 환경은 `extraKnownMarketplaces` 문서화.
- 스캐폴드 자산 갱신은 5.5의 `--update` 경로. 플러그인 네이티브 자산(스킬 등)은 마켓 업데이트만으로 즉시 반영 — **2계층 분리의 최대 이점**(프로젝트 재스캐폴드 빈도 최소화).

### 5.8 바이너리 승격 경로 (T3 Promotion)

- `bin/moai-install`(옵션): 공식 install.sh 안내형 래퍼. 플러그인 `bin/`은 Bash PATH에 등록되므로 Desktop 로컬에서 원클릭 승격 게이트 역할. 바이너리 자체 vendoring은 **하지 않는다**(멀티 플랫폼 × 수십 MB, 클라우드 세션 무용).
- 승격 후: `moai doctor`가 `plugin-deployed` 마커 감지(REQ-BD-007 구현 필요) → `moai update`로 정식 트리 전환 제안 → 사용자 선택으로 플러그인 유지(업데이트 채널) 또는 비활성(중복 목록 제거).

---

## 6. 리스크 & P0 런타임 검증 체크리스트

### 리스크 레지스터

| # | 리스크 | 심각도 | 완화 |
|---|---|---|---|
| R1 | 플러그인 동봉 rules/output-styles 미로드(죽은 페이로드) | 높음 | 스캐폴드로 이동(5.2). P0-1/2로 확정 |
| R2 | 플러그인 커맨드의 `Skill("moai")` 비정규 참조 해석 실패 | 높음 | 정규화 `Skill("<ns>:moai")` + P0-3 검증 |
| R3 | 스킬 이중 목록(플러그인+스캐폴드 동시 존재 시 세션 토큰 2배) | 중간 | 2계층 분리로 원천 차단; T3 승격 시 플러그인 비활성 안내 |
| R4 | 클라우드 세션 훅·git 불능 | 중간 | T0 티어 명시 + 기능 고지(침묵 강등 금지) |
| R5 | 버전 드리프트(마켓 5.0.0 vs coder 3.1.0) | 중간 | export 스탬프 + CI parity job |
| R6 | 다국어: 템플릿은 렌더 시 언어 선택, 플러그인은 정적 | 낮음 | 우선 ko 단일 export, 언어별 export는 후속(D-4) |
| R7 | plugin `settings.json`의 `agent` 키로 메인 스레드 페르소나 대체 가능성 | 기회 | P0-4로 확인 — 성립 시 output-style 스캐폴드 의존 완화 |

### P0 런타임 검증 체크리스트 (Desktop 로컬 + CLI 각 1회)

1. 플러그인 `rules/`에 canary 규칙 삽입 → 세션에서 로드 여부 확인
2. 플러그인 `output-styles/` 인식 여부 (`/output-style` 목록 노출 확인)
3. 플러그인 커맨드에서 `Skill("moai")` vs `Skill("moai-coder:moai")` 해석 비교
4. 플러그인 `settings.json` `agent` 키 동작 (메인 스레드 에이전트 활성화)
5. `hooks.json` 이벤트 발화 + `${CLAUDE_PLUGIN_DATA}` 쓰기 지속성
6. Desktop GUI 설치 → `/reload-plugins` → 커맨드/스킬 가용성 E2E
7. 클라우드 세션에서 스킬·에이전트 가용 + Bash/MCP 차단 실측

---

## 7. 구현 로드맵 (우선순위 라벨)

| 단계 | 내용 | 소유 저장소 |
|---|---|---|
| **P0** | §6 런타임 검증 7종 → 설계 확정치 반영 | claude.mo.ai.kr (검증 프로젝트) |
| **P1** | `moai plugin export` + parity manifest + CI 동기화 job | moai-adk-go |
| **P2** | moai-coder 2계층 재구조화(rules/output-styles → templates/ 이동, 훅 디스패처 통합, 스킬 참조 정규화) + `scripts/scaffold.sh` + `/moai:project` 완성 | claude.mo.ai.kr |
| **P3** | Tier 감지·승격: doctor `plugin-deployed` 인식(REQ-BD-007), `bin/moai-install`, session-start 승격 안내 정비 | moai-adk-go + plugin |
| **P4** | 릴리스 엔지니어링: 버전 SSOT 체크리스트 4-plugin 전체 반영, www 카탈로그 동기화, README 설치 흐름(GUI) 갱신 | claude.mo.ai.kr |

---

## 8. 미결 결정사항 (사용자 결정 필요)

| # | 결정 | 옵션 | 권고 |
|---|---|---|---|
| D-1 | 플러그인 비히클/이름 | ① moai-coder 유지(가족 명명 일관, 커맨드는 `/moai-coder:plan`) ② `moai`로 개명(커맨드 `/moai:plan` — 템플릿 UX 완전 파리티) ③ moai-adk-go 저장소에 신규 플러그인 | ②를 우선 검토 — 단, 마켓 4-plugin 브랜딩(코더) 영향 확인 필요 |
| D-2 | 파리티 모델 | ① byte-parity(현행 SPEC REQ-BD-006: 스캐폴드가 432파일 전체 생성) ② Slim-Scaffold(본 설계 5.1: 프로젝트 귀속 자산만) | ② 권장 — R3(이중 목록) 원천 차단. SPEC 개정 수반 |
| D-3 | 배포 원천 | ① 현행 vendor(claude.mo.ai.kr에 export 산출물 PR) ② moai-adk-go를 직접 마켓 소스로 | ① 권장 — 단일 마켓 유지 |
| D-4 | 언어 전략 | ① ko 단일 export ② 언어별 plugin variant ③ 언어중립 프롬프트 | ① 선행, ③은 P4 이후 검토 |

---

## 9. P0 런타임 검증 결과 (2026-07-08 실측, Claude Code 2.1.204)

캐너리 플러그인 + 로컬 디렉토리 마켓 + 헤드리스 `claude -p --model haiku` 프로브로 P0-1~P0-5를 실측했다. (P0-6 Desktop GUI E2E, P0-7 클라우드 세션은 GUI 필요 — 사용자 수행 대기)

| 항목 | 판정 | 핵심 증거 |
|---|---|---|
| P0-1 플러그인 `rules/` 로드 | **FAIL (미로드)** | 캐너리 토큰 컨텍스트 부재(2회 교차 확인) + `plugin details` 컴포넌트 인벤토리에 Rules 카테고리 자체가 없음. 캐시에는 파일 복사됨(죽은 페이로드 확정) |
| P0-2 플러그인 `output-styles/` | **PASS (단, 네임스페이스 셀렉터 필수)** | `outputStyle: "canary:Canary Style"`(플러그인:frontmatter name)만 적용됨. bare name·slug는 **경고 없이 무시** |
| P0-3 비정규 `Skill("canary-skill")` 해석 | **PASS** | 강제 리터럴 프로브에서 무네임스페이스 호출이 기계적으로 해석·실행됨. 모델은 기본적으로 자동 정규화(`canary:canary-skill`)해 호출. 이름 충돌 시 동작은 미검증 |
| P0-4 플러그인 `settings.json` `agent` 키 | **PASS** | 메인 스레드가 플러그인 에이전트로 활성화(토큰 8+회 재현, ablation 교차 확인) |
| P0-5 hooks + `${CLAUDE_PLUGIN_DATA}` | **PASS** | SessionStart가 headless 포함 매 세션 발화(15+ 세션 17라인 누적). 경로 `~/.claude/plugins/data/<plugin>-<market>/`, 세션 간 영속 — 단 **uninstall 시 삭제됨** |

부수 발견: ① directory-source 마켓은 캐시에 복사되지만 **런타임은 소스 경로에서 로드**(라이브 편집이 다음 세션 반영) ② commands는 내부적으로 Skills로 인벤토리화, `plugin details`에 컴포넌트별 토큰 비용 표시 ③ headless에서 슬래시 커맨드 동작(`/output-style`은 불가) ④ project-scope 설치도 user-level `installed_plugins.json`에 등록(projectPath 판별자) ⑤ uninstall이 캐시 사본은 남김(orphan).

### 설계 반영 델타

- **Δ1 (§5.1/5.2 수정)**: output-styles를 Layer 2(스캐폴드) → **Layer 1(플러그인 네이티브)으로 이동**. 스캐폴드는 프로젝트 `settings.json`에 `"outputStyle": "<플러그인명>:MoAI"` 한 줄만 기록하면 됨. 스타일 본문 갱신이 마켓 업데이트로 즉시 전파되는 이점.
- **Δ2 (G4/R2 하향)**: 비정규 `Skill("moai")` 참조는 이름이 유일한 한 동작함. 정규화는 충돌 방어 차원의 SHOULD로 하향(MUST 아님).
- **Δ3 (R7 확정 → 신규 옵션)**: 플러그인 `settings.json` `agent` 키가 실동작 확인됨. 스캐폴드 없이도(T0/T1) MoAI 오케스트레이터 페르소나를 메인 스레드에 심을 수 있음. 단 **플러그인이 켜진 모든 프로젝트의 메인 스레드를 점유**하므로 기본 동봉은 비권장 — 별도 opt-in(예: persona 전용 경량 플러그인 또는 설치 안내) 설계 필요. D-5 결정 항목으로 추가.
- **Δ4 (R1 확정)**: rules 스캐폴드 필수 — 설계 유지. 현행 moai-coder의 rules/ 동봉 61파일은 죽은 페이로드로 확정, templates/ 이동 대상.
- **Δ5 (§5.4 보강)**: `${CLAUDE_PLUGIN_DATA}`는 uninstall 시 소멸 → 영속이 필요한 상태(세션 추적 등)는 프로젝트 `.moai/` 우선, plugin data는 캐시성 상태만.

---

## Sources

- https://code.claude.com/docs/en/plugins.md — 플러그인 구성요소·plugin.json·디렉토리 규약
- https://code.claude.com/docs/en/plugin-marketplaces.md — marketplace.json 스키마·소스 유형·배포
- https://code.claude.com/docs/en/discover-plugins.md — 설치 UX·버전 해석·자동 업데이트
- https://code.claude.com/docs/en/hooks-guide.md — 훅 이벤트·실행 환경·타임아웃
- https://code.claude.com/docs/en/desktop.md — Desktop 로컬/클라우드/SSH 세션 능력 매트릭스
- https://code.claude.com/docs/en/skills.md — 스킬 자동 로드·네임스페이스
