---
id: SPEC-MOC-SITE-IA-001
title: "모두의 클로드 사이트 정보 구조 2축 재편 (데스크탑/CLI) + DESIGN 병합 + 플러그인 문서 현행화 + CLI 축 신규 콘텐츠"
version: "0.1.0"
status: completed
created: 2026-07-02
updated: 2026-07-06
author: manager-spec
priority: P1
phase: "v2.28.0"
module: "www"
lifecycle: spec-anchored
tier: L
tags: "www, hugo, information-architecture, menu, cli-docs, design-merge, plugin-docs, korean"
depends_on: [SPEC-MOC-PLUGIN-REMEDIATION-001]
related_specs: [SPEC-MOC-BOOTSTRAP-DESKTOP-001]
---

# SPEC-MOC-SITE-IA-001 — 사이트 정보 구조(IA) 2축 재편

## HISTORY

- **2026-07-02** 최초 작성 (manager-spec, plan-phase iteration 1). `www/` Hugo 사이트(theme hugo-geekdoc, 한국어 학습 허브, `geekdocMermaid = true` 확인)를 "사용 환경(데스크탑 vs Claude Code CLI)" 2축으로 재편하는 IA SPEC. 실측 기준선(2026-07-02): 콘텐츠 178 md 파일 / 11 flat 섹션, 메뉴 SSOT `www/data/menu/main.yaml`(플랫 top-level), 버전 SSOT `www/hugo.toml` params.version = `2.27.0`. `design/`(11p)·`claude-design/`(10p) `_index.md` 두 파일 각 ~17.9KB 근중복 확인 → 병합 대상. `plugins/`(33p)는 obsolete 25-플러그인 토폴로지를 문서화 → 현행 마켓플레이스(`.claude-plugin/marketplace.json`, 3 플러그인 v0.1.0)로 재작성 대상. `/cli/` 경로 부재 확인(→ `/code`와 무충돌). CLI 축 소스 `/Users/goos/moai/moai-adk-go/docs-site/content/ko`(13 한국어 섹션) 실측 확인. 본 SPEC은 `www/**`만 소유하며 `plugins/**` 소스는 SPEC-MOC-PLUGIN-REMEDIATION-001 / SPEC-MOC-BOOTSTRAP-DESKTOP-001 소관이다(§E Out of Scope). R3(플러그인 문서)는 remediated 상태를 반영해야 하므로 REMEDIATION-001 완료 후 착수(§C 시퀀싱, plan.md §F M5 gate).

---

## §A. 배경 및 목적 (Background)

### A.1 비즈니스 맥락

`모두의 클로드`(claude.mo.ai.kr) 사이트는 스스로를 "10~60대 비개발자 입문자를 위한 한국어 학습 허브"로 규정한다. 현재 콘텐츠는 11개 **평면(flat) 섹션**으로 나열되어 있어, 방문자가 "나는 무엇으로 시작해야 하는가"를 판단하기 어렵다. 실제 사용자는 크게 두 부류다 — (1) **데스크탑 앱**(Claude Desktop/웹)으로 시작하는 비개발자, (2) **Claude Code CLI/바이너리**로 심화하는 개발자. 본 SPEC은 이 두 부류를 사이트 최상위 정보 구조의 1차 분기축으로 승격시켜, 방문자가 자신의 사용 환경에 맞는 학습 경로로 즉시 진입하도록 재편한다.

동시에 사이트에는 세 가지 구조적 부채가 누적되어 있다: (a) `design/`·`claude-design/` 근중복 섹션, (b) 현재 마켓플레이스와 불일치하는 obsolete `plugins/` 문서 33p, (c) 얇은 CLI 축 콘텐츠(개발자 대상 심화 경로 부재). 본 SPEC은 IA 재편과 함께 이 세 부채를 해소한다.

### A.2 현재 상태 실측 (2026-07-02)

| 항목 | 실측값 | 함의 |
|------|--------|------|
| 콘텐츠 md 파일 총계 | 178 (`find content -name '*.md'`) | 재편 대상 규모 |
| flat 섹션 | 11 (getting-started 4 / chat 8 / cowork 20 / design 11 / claude-design 10 / code 3 / plugins 33 / help 9 / office 2 / cookbook 39 / releases 38) | 최상위 축 부재 → 2축 재편 필요 (R1) |
| 메뉴 SSOT | `www/data/menu/main.yaml` (`geekdocMenuBundle = true`, top-level 평면 나열) | 재편 1차 대상 (R1, R7) |
| 버전 SSOT | `www/hugo.toml` `params.version = "2.27.0"` | 본 SPEC은 버전 bump 비대상(§E) |
| Mermaid | `geekdocMermaid = true`, 178p 중 139p가 이미 ```mermaid``` 포함(39p gap) | per-page 다이어그램 원칙(R6)의 기준선 |
| aliases 선례 | 10p가 이미 `aliases:` frontmatter 사용 | 리다이렉트(R2/R3/R7) 구현 선례 존재 |
| DESIGN 병합 상태 | **HEAD 실측: 흡수+alias 이미 완료** — `content/design/`가 `/claude-design/*` alias 10개 전부 + 고유 `official-quickstart.md`를 이미 보유. `content/claude-design/`(10p)는 미삭제 근중복만 잔존(고유 콘텐츠 없음) | R2 잔여 = **`content/claude-design/` 디렉토리 삭제만** (재병합·재alias 불필요) (R2) |
| plugins 문서 | 33p, obsolete 25-플러그인 토폴로지 | 현행 3-플러그인 마켓플레이스로 재작성 (R3) |
| 현행 마켓플레이스 | `.claude-plugin/marketplace.json`: 3 플러그인(moai-cowork / moai(=moai-code) / design(=moai-design)), v0.1.0 | R3 진실 소스 |
| cookbook/tracks 중복 | 메뉴 "쿡북"과 "실전 트랙"이 track-* 항목 중복 나열 | de-dup (R5) |
| `/cli/` 경로 | 부재 (`ls content/cli` → No such file) | `/code`와 무충돌, 신규 prefix 안전 (R4) |
| CLI 축 소스 | `/Users/goos/moai/moai-adk-go/docs-site/content/ko` 13 섹션(getting-started 11 / core-concepts 7 / claude-code 28 / workflow-commands 6 / quality-commands 4 / worktree 4 / advanced 18 / cost-optimization 1 / multi-llm 3 / guides 3 / db 5 / contributing 1 / utility-commands 7) | R4 포팅 원천 |
| source-index | `help/source-index.md` — 69 문서/15 페이지, "개발자/CLI·SDK 영역은 다루지 않습니다" 명시 | R4/R6에서 CLI 축까지 확장 |

### A.3 해결할 과제

1. **최상위 축 부재**: 11개 평면 섹션이 사용 환경 구분 없이 나열 → 데스크탑/CLI 2축 + 공통 하단(도움말·쿡북·릴리스)으로 재편 (R1).
2. **DESIGN 중복**: `design/`·`claude-design/` 근중복 → 병합(흡수 + alias 10)은 HEAD에서 이미 완료됨; R2 잔여 = `content/claude-design/` 디렉토리 삭제만 (R2).
3. **플러그인 문서 노후화**: obsolete 33p → 현행 4 카테고리(chat/cowork/design/code)로 재작성 + 아카이브 + alias (R3). remediated 플러그인 상태 반영 필요(REMEDIATION-001 의존).
4. **CLI 축 콘텐츠 부재**: 개발자 심화 경로 부재 → `/cli/` prefix 하 5 섹션 신규 콘텐츠(~25-30p) 포팅·재저작 (R4).
5. **help/office 산재 + tracks 중복**: `office/`(2p) 통합, cookbook/tracks 메뉴 중복 정리 (R5).
6. **콘텐츠 품질 규약 미표준화**: prose-first, per-page mermaid, 출처 인용 블록, 이중 톤 원칙 부재 → 페이지 제작 규약 정립 (R6).
7. **링크 파손 위험**: 섹션 재편 시 기존 inbound 링크 파손 위험 → 메뉴 재편을 1차 수단으로 삼고 alias로 방어 (R7).

---

## §B. 요구사항 (Requirements) — GEARS Format

> 본 절의 `<subject>`는 문맥에 따라 "the menu SSOT"(메뉴 정본 `www/data/menu/main.yaml`), "the site"(빌드 산출물 전체), "the DESIGN section", "the plugins section", "the CLI axis content", "the content page"(개별 페이지)로 표기한다. GEARS 키워드(**SHALL** / **When** / **While** / **Where** / **SHALL NOT**)와 식별자·URL·파일 경로·프론트매터 키는 영어 그대로 유지한다.

### R1 — 2축 정보 구조

#### REQ-IA-001 — 최상위 2축 + 공통 하단 (Ubiquitous)

The menu SSOT (`www/data/menu/main.yaml`) **SHALL** organize top-level navigation into exactly two usage-environment axes — a Desktop axis (🖥️ 비개발자용) and a Claude Code CLI axis (⌨️ 개발자용) — followed by a shared bottom area containing 도움말 · 쿡북 · 릴리스.

#### REQ-IA-002 — 데스크탑 축 순서 (Ubiquitous)

The Desktop axis **SHALL** present its product sections in ascending learning-difficulty order: 시작하기 → CHAT → COWORK → DESIGN → CODE → 🧩 MoAI 플러그인, and this order **SHALL** double as the onboarding narrative (CHAT→COWORK→DESIGN→CODE = 학습 난이도 상승 경로).

#### REQ-IA-003 — CLI 축 섹션 (Ubiquitous)

The CLI axis **SHALL** present exactly these sections in order: 시작하기 → 핵심 개념 → 일상 사용 → MoAI-ADK → 레퍼런스.

#### REQ-IA-004 — 축 시각 마커 (Ubiquitous)

The menu SSOT **SHALL** carry machine-detectable axis-group markers (emoji-prefixed group boundaries and/or YAML comment separators) so that the two axes and the shared bottom area are distinguishable by a grep on `www/data/menu/main.yaml`. (구체적 geekdoc 표현은 run-phase 재량 — 본 요구는 WHAT 수준.)

### R2 — DESIGN 섹션 병합

#### REQ-IA-005 — design + claude-design 단일화 (Event-driven)

**When** the DESIGN section is consolidated, the site **SHALL** merge `content/design/` and `content/claude-design/` (near-duplicate `_index.md` 확인됨) into a single DESIGN section positioned under the Desktop axis.

#### REQ-IA-006 — 제거 경로 alias (Event-driven)

**When** a `design/` or `claude-design/` page path is removed or relocated by the merge, the site **SHALL** provide a Hugo `aliases:` redirect entry from each old path to its new canonical path (기존 10p `aliases:` 선례와 동일 방식).

### R3 — 플러그인 문서 현행화 (4 카테고리)

#### REQ-IA-007 — obsolete 토폴로지 → 4 카테고리 (Event-driven)

**When** the `plugins/` section is rewritten, the site **SHALL** replace the obsolete 25-plugin topology with exactly 4 plugin categories aligned to the site product axes: chat, cowork, design, code.

#### REQ-IA-008 — chat 카테고리는 문서 허브(A안) (Where)

**Where** the plugin category is `chat`, the site **SHALL** render it as a "Chat에서 스킬·플러그인 활용" documentation hub promoted from the existing `content/chat/skills-plugins.md`, and **SHALL NOT** describe a built chat plugin (챗 플러그인은 제작 대상이 아님).

#### REQ-IA-009 — built-plugin 공통 스켈레톤 (Ubiquitous)

Each built-plugin category page (cowork, design, code) **SHALL** follow the common skeleton in this fixed order: intro prose → install diagram → top-5 skills → full skill index → recipe links.

#### REQ-IA-010 — 구 33p 아카이브 + alias (Event-driven)

**When** the old 33 plugin pages are archived, the site **SHALL** provide an `aliases:` redirect for every removed/relocated old plugin path so that no previously-published `/plugins/...` URL 404s.

#### REQ-IA-011 — remediated 상태 게이트 (Where)

**Where** the remediated plugin state is available (SPEC-MOC-PLUGIN-REMEDIATION-001 completed), the plugin category pages **SHALL** reflect current marketplace reality as recorded in `.claude-plugin/marketplace.json` (3 plugins: moai-cowork / moai-code / moai-design). **While** REMEDIATION-001 is not complete, the built-plugin category pages **SHALL NOT** be finalized (dependency gate — plan.md §F M5).

### R4 — CLI 축 신규 콘텐츠

#### REQ-IA-012 — `/cli/` prefix 무충돌 (Ubiquitous)

The CLI axis content **SHALL** live under a new `/cli/` URL prefix, which **SHALL NOT** collide with the existing Desktop `/code` section.

#### REQ-IA-013 — 포팅+재저작 매핑 (Ubiquitous)

The CLI axis **SHALL** be produced by porting AND rewriting (not raw port) the `moai-adk-go/docs-site/content/ko` sources into beginner Korean prose, per this section mapping:

| CLI 축 섹션 | 원천 (moai-adk-go docs-site ko) | 보강 소스 |
|-------------|--------------------------------|-----------|
| 시작하기 | getting-started | Claude Code 공식 문서(code.claude.com/docs) |
| 핵심 개념 | core-concepts + claude-code | 공식 문서 |
| 일상 사용 | claude-code + utility-commands | 공식 문서 |
| MoAI-ADK | workflow-commands + quality-commands + worktree | — |
| 레퍼런스 | advanced + cost-optimization + multi-llm + guides | — |

#### REQ-IA-014 — SPEC 라이프사이클 stateDiagram (Ubiquitous)

The MoAI-ADK CLI section **SHALL** include a mermaid `stateDiagram` depicting the SPEC lifecycle PLAN → RUN → SYNC.

#### REQ-IA-015 — 브리지 내러티브 + Tier 표 재사용 (Ubiquitous)

The CLI axis **SHALL** include a bridge narrative "데스크탑에서 플러그인으로 시작 → CLI에서 바이너리로 심화" that reuses the moai-code Tier 1~3 table (defined in SPEC-MOC-BOOTSTRAP-DESKTOP-001) to cross-link the Desktop CODE section and the CLI MoAI-ADK section.

### R5 — help / office 통합 및 tracks 중복 제거

#### REQ-IA-016 — office → 도움말 통합 (Event-driven)

**When** the help area is consolidated, the site **SHALL** fold `content/office/` (2p) under the shared 도움말 area, **while** keeping `content/cookbook/` (39p) and `content/releases/` (38p) as-is, and **SHALL** provide an `aliases:` redirect for the relocated office paths.

#### REQ-IA-017 — cookbook/tracks 메뉴 중복 제거 (Event-driven)

**When** the cookbook/tracks menu overlap is de-duplicated, the menu SSOT **SHALL** present each track exactly once (현재 "쿡북"·"실전 트랙" 두 메뉴 그룹이 track-* 항목을 중복 나열).

### R6 — 콘텐츠 제작 규약 (per-page contract)

#### REQ-IA-018 — prose-first (Ubiquitous)

Each content page authored or rewritten under this SPEC **SHALL** be prose-first (why → when → how narrative), using tables and lists as support only, not as the primary body.

#### REQ-IA-019 — per-page mermaid (Ubiquitous)

Each content page authored or rewritten under this SPEC **SHALL** contain at least one mermaid diagram: flowchart/journey for concepts, sequenceDiagram for procedures, stateDiagram for lifecycles.

#### REQ-IA-020 — 출처 인용 블록 + source-index 확장 (Ubiquitous)

Each content page authored or rewritten under this SPEC **SHALL** end with a source-citation block, and the existing `content/help/source-index.md` index **SHALL** be extended to cover both axes (Desktop + CLI), removing its current "개발자/CLI·SDK 영역은 다루지 않습니다" limitation.

#### REQ-IA-021 — 이중 톤 (Where)

**Where** a page belongs to the Desktop axis, its tone **SHALL** use non-developer metaphor vocabulary; **where** a page belongs to the CLI axis, its tone **SHALL** use precise technical terms expressed in friendly prose.

#### REQ-IA-024 — in-scope 페이지 마커 (Ubiquitous)

> **번호 순서 주석 (appended REQ)**: REQ-IA-024는 의미상 R6(콘텐츠 제작 규약)에 속하므로 R6 블록(REQ-IA-018~021) 끝에 배치했으나, 번호는 R7의 REQ-IA-022/023이 먼저 부여된 뒤 추가되어 문서 순서상 022/023보다 앞에 온다. 이는 의도된 배치이며 번호 누락·중복이 아니다(plan-audit MP-1: 001~024 연속·중복 없음 확인).

Each content page authored or rewritten under this SPEC **SHALL** carry an `ia_in_scope: true` frontmatter marker, so that the "authored or rewritten under this SPEC" page set referenced by REQ-IA-018/019/020 is mechanically enumerable via `grep -rl '^ia_in_scope: true' www/content --include='*.md'`. This marker is the concrete in-scope manifest that turns the per-page contracts (prose-first / per-page mermaid / 출처 인용 블록) into deterministic pass/fail checks — without it, "각 in-scope 페이지"는 미정의 집합이 되어 AC-IA-018/019/020 검증이 불가능하다. The wholly-new `content/cli/**` section **SHALL** be 100% marked (verification floor: AC-IA-024).

### R7 — URL 전략 및 링크 보존

#### REQ-IA-022 — 메뉴 재편 우선 + 단일 신규 prefix (Ubiquitous)

The site **SHALL** preserve existing section URLs and treat the MENU reorganization (2-axis grouping) as the primary structural change; the only new URL prefix introduced by this SPEC **SHALL** be `/cli/`.

#### REQ-IA-023 — 링크 무파손 (Unwanted behavior)

The site **SHALL NOT** break any existing internal link; **when** any path is removed or relocated (R2/R3/R5), an `aliases:` redirect **SHALL** preserve the old URL. **When** the site is built (`hugo --gc --minify`), the build **SHALL** complete with zero errors — but a clean `hugo` exit code alone is **NOT** accepted as broken-link proof (hugo.toml sets no `refLinksErrorLevel` and the content uses no `ref`/`relref` shortcodes, so Hugo build-time validates no internal link). Therefore this SPEC **SHALL** deliver a dedicated internal-link checker committed under `www/scripts/` (e.g. `www/scripts/check-links.mjs`, reusing the existing Node toolchain — the existing `check-docs-health.mjs` is a count checker, NOT a link checker, and is mis-pathed for this repo) that scans the built `www/public/` HTML tree, resolves every internal link (pretty-URL directories → `index.html`, alias redirect stubs, anchors stripped) against the file tree, and reports **zero broken internal links**. The `hugo` build exit-0 check and the dedicated-link-checker check are two SEPARATE sub-checks (acceptance.md AC-IA-023).

---

## §C. 설계 결정 요약 (Design Decisions — WHAT/WHY 수준)

> 본 절은 구현(HOW: 파일별 편집 계획, geekdoc 템플릿 세부)이 아니라 관찰 가능한 결정과 근거만 기록한다. 세부 실행 순서는 plan.md, 검증 기준은 acceptance.md 소관.

- **D1 — 2축을 메뉴 재편으로 표현 (코드/URL 변경 최소화)**: geekdoc `data/menu/main.yaml` 정본을 재정렬하고 축 마커를 추가하는 것이 1차 수단. 섹션 디렉토리 URL은 그대로 두어 링크 파손 표면을 최소화(R7). 근거: A.2 실측에서 178p 중 대부분이 안정적 URL을 이미 보유.
- **D2 — DESIGN은 `design/`로 수렴, `claude-design/` 폐기+alias (흡수는 HEAD에서 이미 완료)**: `design/`이 정본이며 `claude-design/` 고유 콘텐츠(`official-quickstart.md`) 흡수 + `/claude-design/*` → `design/*` alias 10개 부여가 이미 완료된 상태(HEAD 6d78fbf 실측). 따라서 **run-phase 잔여 = `content/claude-design/` 디렉토리 삭제 + 삭제 후 링크체커 회귀 확인**뿐이며, 재흡수·재alias는 불필요(중복 작업 금지).
- **D3 — 플러그인 chat 카테고리는 "문서 허브"(A안)**: 챗 전용 플러그인은 존재하지 않으므로(REQ-IA-008), 기존 `chat/skills-plugins.md`를 승격한 활용 허브로 표현. cowork/design/code 3종만 실제 빌드 플러그인 문서.
- **D4 — CLI 축은 `/cli/` 신규 prefix (기존 `/code` 데스크탑 섹션과 공존)**: `/code`(데스크탑 CODE 제품)와 `/cli`(개발자 바이너리 심화)는 의미가 다른 별개 섹션. 실측상 `/cli` 부재 확인 → 무충돌.
- **D5 — CLI 콘텐츠는 재저작(raw port 금지)**: moai-adk-go docs-site는 개발자 문체. 본 사이트 톤(입문자 친화)으로 재작성하며, 브리지 내러티브로 데스크탑↔CLI를 연결(REQ-IA-015).
- **D6 — R3는 REMEDIATION-001 이후 착수**: 플러그인 문서는 remediated 소스 상태를 반영해야 하므로 순서 의존(§C 시퀀싱 = plan.md §F M5 gate). M1/M2/M4는 이 의존과 무관하게 선행 가능.
- **D7 — per-page mermaid는 in-scope 페이지에 우선 적용**: 기존 39p mermaid gap의 전면 소급은 본 SPEC 범위 밖(§E). 본 SPEC은 신규/재작성 페이지에 대해 규약을 강제하고, 기존 gap은 후속 정리 항목으로 기록.
- **D8 — in-scope 페이지는 `ia_in_scope: true` 마커로 식별 (REQ-IA-024)**: R6 per-page 규약(prose-first / mermaid / 출처 블록)의 "각 in-scope 페이지"를 기계 검증 가능한 집합으로 만들기 위해, 본 SPEC이 신규/재작성하는 모든 페이지 프론트매터에 `ia_in_scope: true`를 부여한다. 검증은 `grep -rl '^ia_in_scope: true'`로 집합을 구성한 뒤 각 규약을 iterate(AC-IA-018/019/020/024). manifest 파일 대신 per-page 마커를 택한 이유: 페이지 생성/삭제와 마커가 항상 동기화되어 별도 목록 드리프트가 없고, 신규 `content/cli/**` 전량 마킹을 floor 가드로 강제할 수 있음.
- **D9 — 링크 무파손은 전용 링크체커로 검증 (hugo exit 0 불충분, REQ-IA-023)**: hugo.toml에 `refLinksErrorLevel` 미설정 + 콘텐츠가 `ref`/`relref` 숏코드 미사용이므로 `hugo --gc --minify` exit 0은 내부 링크 무파손을 증명하지 못한다(SPEC-MOC-PLUGIN-REMEDIATION-001 plan-audit에서 확인된 testability gap). 따라서 `www/public/` 빌드 산출 HTML을 스캔하는 전용 링크체커(`www/scripts/check-links.mjs`, 기존 Node 툴체인 재사용 — lychee/htmltest 신규 설치 대신 최소 스코프 택일)를 신규 산출물로 커밋하고 권위 검출기로 삼는다. 기존 `check-docs-health.mjs`는 스킬/플러그인 카운트 검사기이지 링크체커가 아니며 이 저장소에서 CONTENT 경로가 불일치(참조 금지). hugo build exit 0은 별도 보조 sub-check로 유지.

---

## §D. 성공 기준 요약 (Success Criteria)

전체 기계 검증 가능한 수용 기준은 `acceptance.md` (AC-IA-001 ~ AC-IA-024) 참조. 핵심 게이트:

- `hugo --gc --minify` exit 0 (REQ-IA-023 보조 sub-check — 단독으로 broken-link 증거 아님).
- 전용 링크체커(`www/scripts/check-links.mjs`, 신규 산출물)로 broken internal link 0건 (REQ-IA-023 권위 검출).
- 메뉴 2축 마커 grep 확인 (REQ-IA-001/004).
- DESIGN 병합 후 `content/claude-design/` 디렉토리 부재 + 제거 경로별 per-page alias 커버리지 ≥ 10 (REQ-IA-005/006).
- `plugins/` 4 카테고리 존재 + 구 경로별 per-page alias 커버리지 ≥ 33 (REQ-IA-007/010).
- `content/cli/` 신규 존재 + `/cli`↔`/code` URL 무충돌(grep 매치 0) (REQ-IA-012).
- in-scope 페이지가 `ia_in_scope: true` 마커로 식별 + 신규 `content/cli/**` 전량 마킹 (REQ-IA-024).
- in-scope 페이지 per-page mermaid 누락 0 (REQ-IA-019).
- source-index가 CLI 축 포함으로 확장 (REQ-IA-020).

---

## §E. 범위 제외 (Out of Scope)

본 SPEC은 `www/**`(콘텐츠, `data/menu/main.yaml`, alias용 hugo 설정)만 소유한다. 다음 항목은 명시적으로 out of scope다.

### Out of Scope — 플러그인 소스 코드
- `plugins/**` 소스(스킬 본문, plugin.json, 에이전트 정의)는 본 SPEC이 수정하지 않는다. 소유: SPEC-MOC-PLUGIN-REMEDIATION-001 / SPEC-MOC-BOOTSTRAP-DESKTOP-001.
- 본 SPEC은 플러그인을 **문서화만** 하며, 플러그인 동작·구성을 변경하지 않는다.

### Out of Scope — 신규 플러그인 제작
- 챗 전용 플러그인 신규 제작은 대상이 아니다(REQ-IA-008: chat 카테고리는 문서 허브 A안).
- 마켓플레이스(`.claude-plugin/marketplace.json`) 엔트리 추가·수정은 대상이 아니다.

### Out of Scope — CLI 바이너리 및 툴링
- `moai-adk-go` 저장소의 코드·툴링·docs-site 원천 파일 수정은 대상이 아니다(읽기 전용 원천으로만 참조).
- Claude Code CLI 자체 동작 변경은 대상이 아니다.

### Out of Scope — 버전 bump 및 릴리스
- `www/hugo.toml` `params.version` 및 릴리스 노트 발행은 대상이 아니다(SSOT는 별도 릴리스 절차 소관).
- `releases/`(38p) 콘텐츠 재작성은 대상이 아니다(유지).

### Out of Scope — 테마/레이아웃 코드
- `www/themes/`, `www/layouts/`, `www/assets/` 등 geekdoc 테마·레이아웃·JS/CSS 코드 변경은 대상이 아니다.
- 다이어그램 렌더링 엔진 설정(`geekdocMermaid`)은 이미 활성 상태이므로 변경하지 않는다.

### Out of Scope — 기존 페이지 mermaid gap 전면 소급
- 기존 39p mermaid 미보유 페이지 전체에 대한 소급 다이어그램 추가는 대상이 아니다(REQ-IA-019는 본 SPEC이 신규/재작성하는 in-scope 페이지에만 적용). 기존 gap은 후속 정리 항목으로 기록.

---

## §F. 용어 및 참조 (Glossary & References)

- **데스크탑 축(Desktop axis)**: Claude Desktop/웹 앱 기반 비개발자 학습 경로 (시작하기·CHAT·COWORK·DESIGN·CODE·MoAI 플러그인).
- **CLI 축(Claude Code CLI axis)**: Claude Code 바이너리/CLI 기반 개발자 심화 경로 (`/cli/` prefix, 5 섹션).
- **공통 하단(shared bottom)**: 두 축이 공유하는 도움말·쿡북·릴리스.
- **A안(chat 문서 허브)**: 챗 플러그인을 제작하지 않고, 기존 `chat/skills-plugins.md`를 활용 허브로 승격하는 방식.
- **메뉴 SSOT**: `www/data/menu/main.yaml` (geekdoc `geekdocMenuBundle = true`).
- **버전 SSOT**: `www/hugo.toml` `params.version` (본 SPEC 비대상).

참조:
- 마켓플레이스 진실 소스: `.claude-plugin/marketplace.json` (3 플러그인, v0.1.0).
- CLI 축 원천: `/Users/goos/moai/moai-adk-go/docs-site/content/ko` (13 섹션).
- Claude Code 공식 문서: code.claude.com/docs (CLI 축 보강 소스).
- 의존 SPEC: SPEC-MOC-PLUGIN-REMEDIATION-001 (R3 게이트), SPEC-MOC-BOOTSTRAP-DESKTOP-001 (Tier 1~3 표 원천).
- GEARS 표기 규약: `.claude/skills/moai-workflow-spec/SKILL.md` § GEARS Format.
