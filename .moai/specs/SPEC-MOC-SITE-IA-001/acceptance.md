# SPEC-MOC-SITE-IA-001 — 수용 기준 (acceptance.md)

모든 수용 기준은 **기계 검증 가능**해야 한다(Hugo 빌드 exit code, grep 매치, 디렉토리/파일 존재, 링크 검사 카운트, 페이지 수 delta). 아래 명령의 `cd` 기준은 `/Users/goos/MoAI/claude.mo.ai.kr`이며, hugo 명령은 `www/`에서 실행한다.

---

## §A. Given-When-Then 시나리오

### GWT-1 — 데스크탑 방문자의 축 진입 (R1)
- **Given** 사이트가 데스크탑/CLI 2축으로 재편되었고,
- **When** 비개발자 방문자가 좌측 메뉴 최상단을 본다면,
- **Then** 데스크탑 축(🖥️)이 먼저 나타나고 그 하위가 시작하기 → CHAT → COWORK → DESIGN → CODE → 🧩 MoAI 플러그인 순서로, 학습 난이도 상승 경로를 그대로 내비게이션으로 제공한다.

### GWT-2 — 개발자의 CLI 심화 진입 (R4)
- **Given** `/cli/` prefix 하 5 섹션이 신규 생성되었고,
- **When** 개발자가 `/cli/`로 진입한다면,
- **Then** 시작하기 → 핵심 개념 → 일상 사용 → MoAI-ADK → 레퍼런스 순으로 입문자 톤 재저작 콘텐츠를 만나고, MoAI-ADK 섹션에서 PLAN→RUN→SYNC stateDiagram과 데스크탑↔CLI 브리지 내러티브를 확인한다.

### GWT-3 — 구 링크 보존 (R2/R3/R5/R7)
- **Given** `claude-design/`·구 `plugins/`·`office/` 경로가 이동/폐기되었고,
- **When** 기존 inbound 링크로 구 URL에 접근한다면,
- **Then** `aliases:` 리다이렉트로 새 정본 경로로 이동하며 404가 발생하지 않고, `hugo --gc --minify` 빌드가 exit 0(보조 sub-check)이며, 전용 링크체커(`www/scripts/check-links.mjs`)가 broken internal link 0을 확인한다(권위 검출 — hugo exit 0 단독은 broken-link 증거 아님).

### GWT-4 — DESIGN 중복 해소 (R2)
- **Given** `design/`·`claude-design/` 근중복 섹션이 있었고,
- **When** DESIGN 병합이 완료된다면,
- **Then** `content/claude-design/` 디렉토리는 존재하지 않고, DESIGN은 데스크탑 축 하 단일 섹션으로만 나타난다.

### GWT-5 — 플러그인 문서 현행화 (R3, GATED)
- **Given** SPEC-MOC-PLUGIN-REMEDIATION-001이 완료되어 remediated 플러그인 상태가 확정되었고,
- **When** `plugins/` 섹션이 4 카테고리(chat/cowork/design/code)로 재작성된다면,
- **Then** chat은 문서 허브(A안)로, cowork/design/code는 공통 스켈레톤(intro→install diagram→top-5 skills→full index→recipe links)으로 렌더되고, 내용은 `.claude-plugin/marketplace.json`의 3 플러그인 현실과 일치한다.

### GWT-6 — per-page 콘텐츠 규약 (R6)
- **Given** 콘텐츠 제작 규약이 정립되었고,
- **When** 본 SPEC이 신규/재작성한 in-scope 페이지를 검사한다면,
- **Then** 각 페이지는 prose-first 구조 + 최소 1개 mermaid + 하단 출처 인용 블록을 가지며, 축에 맞는 톤(데스크탑=비개발자 은유 / CLI=친화적 기술 용어)을 사용한다.

---

## §B. 수용 기준 매트릭스 (AC-IA-001 ~ 024)

**GEARS Behavior Anchors** — 각 AC를 spec.md §B의 해당 REQ-IA-XXX SHALL 문장에 anchor (iter-2 D3 fix). 범주 라벨(Ubiquitous / Event-driven / Where / Unwanted behavior)은 spec.md §B의 REQ 헤더 라벨과 정확히 정렬.

- **AC-IA-001** (REQ-IA-001, Ubiquitous) — **Behavior:** The menu SSOT (`www/data/menu/main.yaml`) **SHALL** organize top-level navigation into exactly two usage-environment axes — a Desktop axis (🖥️) and a Claude Code CLI axis (⌨️) — followed by a shared bottom area containing 도움말 · 쿡북 · 릴리스.
- **AC-IA-002** (REQ-IA-002, Ubiquitous) — **Behavior:** The Desktop axis **SHALL** present its product sections in ascending learning-difficulty order: 시작하기 → CHAT → COWORK → DESIGN → CODE → 🧩 MoAI 플러그인.
- **AC-IA-003** (REQ-IA-003, Ubiquitous) — **Behavior:** The CLI axis **SHALL** present exactly these sections in order: 시작하기 → 핵심 개념 → 일상 사용 → MoAI-ADK → 레퍼런스.
- **AC-IA-004** (REQ-IA-004, Ubiquitous) — **Behavior:** The menu SSOT **SHALL** carry machine-detectable axis-group markers (emoji-prefixed group boundaries and/or YAML comment separators) so that the two axes and the shared bottom area are distinguishable by a grep on `www/data/menu/main.yaml`.
- **AC-IA-005** (REQ-IA-005, Event-driven) — **Behavior:** **When** the DESIGN section is consolidated, the site **SHALL** merge `content/design/` and `content/claude-design/` into a single DESIGN section positioned under the Desktop axis.
- **AC-IA-006** (REQ-IA-006, Event-driven) — **Behavior:** **When** a `design/` or `claude-design/` page path is removed or relocated by the merge, the site **SHALL** provide a Hugo `aliases:` redirect entry from each old path to its new canonical path.
- **AC-IA-007** (REQ-IA-007, Event-driven) — **Behavior:** **When** the `plugins/` section is rewritten, the site **SHALL** replace the obsolete 25-plugin topology with exactly 4 plugin categories aligned to the site product axes: chat, cowork, design, code.
- **AC-IA-008** (REQ-IA-008, Where) — **Behavior:** **Where** the plugin category is `chat`, the site **SHALL** render it as a "Chat에서 스킬·플러그인 활용" documentation hub promoted from the existing `content/chat/skills-plugins.md`, and **SHALL NOT** describe a built chat plugin.
- **AC-IA-009** (REQ-IA-009, Ubiquitous) — **Behavior:** Each built-plugin category page (cowork, design, code) **SHALL** follow the common skeleton in this fixed order: intro prose → install diagram → top-5 skills → full skill index → recipe links.
- **AC-IA-010** (REQ-IA-010, Event-driven) — **Behavior:** **When** the old 33 plugin pages are archived, the site **SHALL** provide an `aliases:` redirect for every removed/relocated old plugin path so that no previously-published `/plugins/...` URL 404s.
- **AC-IA-011** (REQ-IA-011, Where) — **Behavior:** **Where** the remediated plugin state is available (SPEC-MOC-PLUGIN-REMEDIATION-001 completed), the plugin category pages **SHALL** reflect current marketplace reality as recorded in `.claude-plugin/marketplace.json` (3 plugins: moai-cowork / moai-code / moai-design).
- **AC-IA-012** (REQ-IA-012, Ubiquitous) — **Behavior:** The CLI axis content **SHALL** live under a new `/cli/` URL prefix, which **SHALL NOT** collide with the existing Desktop `/code` section.
- **AC-IA-013** (REQ-IA-013, Ubiquitous) — **Behavior:** The CLI axis **SHALL** be produced by porting AND rewriting (not raw port) the `moai-adk-go/docs-site/content/ko` sources into beginner Korean prose per the REQ-IA-013 section mapping.
- **AC-IA-014** (REQ-IA-014, Ubiquitous) — **Behavior:** The MoAI-ADK CLI section **SHALL** include a mermaid `stateDiagram` depicting the SPEC lifecycle PLAN → RUN → SYNC.
- **AC-IA-015** (REQ-IA-015, Ubiquitous) — **Behavior:** The CLI axis **SHALL** include a bridge narrative "데스크탑에서 플러그인으로 시작 → CLI에서 바이너리로 심화" that reuses the moai-code Tier 1~3 table to cross-link the Desktop CODE section and the CLI MoAI-ADK section.
- **AC-IA-016** (REQ-IA-016, Event-driven) — **Behavior:** **When** the help area is consolidated, the site **SHALL** fold `content/office/` (2p) under the shared 도움말 area, **while** keeping `content/cookbook/` (39p) and `content/releases/` (38p) as-is, and **SHALL** provide an `aliases:` redirect for the relocated office paths.
- **AC-IA-017** (REQ-IA-017, Event-driven) — **Behavior:** **When** the cookbook/tracks menu overlap is de-duplicated, the menu SSOT **SHALL** present each track exactly once.
- **AC-IA-018** (REQ-IA-018, Ubiquitous) — **Behavior:** Each content page authored or rewritten under this SPEC **SHALL** be prose-first (why → when → how narrative), using tables and lists as support only, not as the primary body.
- **AC-IA-019** (REQ-IA-019, Ubiquitous) — **Behavior:** Each content page authored or rewritten under this SPEC **SHALL** contain at least one mermaid diagram (flowchart/journey for concepts, sequenceDiagram for procedures, stateDiagram for lifecycles).
- **AC-IA-020** (REQ-IA-020, Ubiquitous) — **Behavior:** Each content page authored or rewritten under this SPEC **SHALL** end with a source-citation block, and the existing `content/help/source-index.md` index **SHALL** be extended to cover both axes (Desktop + CLI), removing its current "개발자/CLI·SDK 영역은 다루지 않습니다" limitation.
- **AC-IA-021** (REQ-IA-021, Where) — **Behavior:** **Where** a page belongs to the Desktop axis, its tone **SHALL** use non-developer metaphor vocabulary; **where** a page belongs to the CLI axis, its tone **SHALL** use precise technical terms expressed in friendly prose.
- **AC-IA-022** (REQ-IA-022, Ubiquitous) — **Behavior:** The site **SHALL** preserve existing section URLs and treat the MENU reorganization (2-axis grouping) as the primary structural change; the only new URL prefix introduced by this SPEC **SHALL** be `/cli/`.
- **AC-IA-023** (REQ-IA-023, Unwanted behavior) — **Behavior:** The site **SHALL NOT** break any existing internal link; **when** any path is removed or relocated, an `aliases:` redirect **SHALL** preserve the old URL; **when** the site is built, the dedicated internal-link checker (`www/scripts/check-links.mjs`) **SHALL** report zero broken internal links.
- **AC-IA-024** (REQ-IA-024, Ubiquitous) — **Behavior:** Each content page authored or rewritten under this SPEC **SHALL** carry an `ia_in_scope: true` frontmatter marker so that the in-scope page set is mechanically enumerable via `grep -rl '^ia_in_scope: true'`; the wholly-new `content/cli/**` section **SHALL** be 100% marked.

| AC | REQ | 검증 명령 (기계 검증) | 통과 기준 |
|----|-----|----------------------|-----------|
| AC-IA-001 | REQ-IA-001 | `grep -nE '데스크탑|CLI 축|공통|shared' www/data/menu/main.yaml` | 데스크탑 축·CLI 축·공통 하단 3개 그룹 마커 모두 매치 |
| AC-IA-002 | REQ-IA-002 | `www/data/menu/main.yaml`에서 데스크탑 축 하위 순서 확인 | 시작하기→CHAT→COWORK→DESIGN→CODE→MoAI 플러그인 순서 |
| AC-IA-003 | REQ-IA-003 | 메뉴 CLI 축 하위 항목 확인 | 시작하기·핵심 개념·일상 사용·MoAI-ADK·레퍼런스 5개 존재 |
| AC-IA-004 | REQ-IA-004 | `grep -cE '# ===|🖥️|⌨️' www/data/menu/main.yaml` | 축 마커 grep count ≥ 2 |
| AC-IA-005 | REQ-IA-005 | `ls -d www/content/claude-design 2>&1` | "No such file" (디렉토리 폐기됨) |
| AC-IA-006 | REQ-IA-006 | 병합 회귀 가드(반드시 삭제 신호와 AND — 단독 alias 카운트는 HEAD에서 이미 10이라 판별력 0): (a) alias 커버리지 보존 `grep -rhE '^aliases:' www/content/design --include='*.md' \| grep -oE '/claude-design/[A-Za-z0-9/_-]*' \| sort -u \| wc -l` (≥ 10) **AND** (b) 판별 신호 = `content/claude-design/` 삭제 `test ! -d www/content/claude-design && echo DELETED` (AC-IA-005와 동일 판별축) | (a) 커버리지 ≥ 10 **AND** (b) `content/claude-design/` 부재. HEAD 실측: `design/`는 이미 `/claude-design/*` alias 10 + 고유 `official-quickstart.md` 흡수 완료, `claude-design/` 미삭제(dir 존재) → 판별력은 (b)에서 나옴. 잔여 무파손은 AC-IA-023 링크체커 교차 |
| AC-IA-007 | REQ-IA-007 | `find www/content/plugins -maxdepth 1 -type d` | chat/cowork/design/code 4 카테고리 디렉토리 |
| AC-IA-008 | REQ-IA-008 | `grep -il '스킬·플러그인 활용\|문서 허브' www/content/plugins/chat/_index.md` + chat 카테고리에 plugin.json 참조 부재 | chat=문서 허브, 빌드 플러그인 서술 없음 |
| AC-IA-009 | REQ-IA-009 | `www/content/plugins/cowork/_index.md`·`plugins/design/_index.md`·`plugins/code/_index.md` 각각에 5개 스켈레톤 앵커 grep(`intro`/`install`/`top`/`index`/`recipe` 상당 헤딩). 경로는 **플러그인 카테고리 페이지**로 스코프(데스크탑 제품 섹션 `content/{cowork,design,code}` 아님 — HEAD 실측상 후자는 스켈레톤 앵커 0이라 오검증 위험은 없으나 경로 모호성 제거) | 3 플러그인 카테고리 `_index.md` 모두 5-섹션 스켈레톤 (HEAD: 카테고리 페이지 부재 → 판별) |
| AC-IA-010 | REQ-IA-010 | `grep -rhE '^aliases:' www/content/plugins --include='*.md' \| grep -oE '/plugins/[A-Za-z0-9/_-]*' \| sort -u \| wc -l` | **≥ 33** (= 아카이브되는 구 plugins 페이지 baseline; 2026-07-02 실측 33 md = 구 URL별 per-page alias 커버리지). 구 URL이 신규 4-카테고리에서 동일 경로로 live 유지되면 그 수만큼 차감 가능; 최종 무파손은 AC-IA-023 링크체커가 권위 검출 (M5 게이트: REMEDIATION-001 완료 후 검증) |
| AC-IA-011 | REQ-IA-011 | `ls .moai/specs/SPEC-MOC-PLUGIN-REMEDIATION-001/` 완료 확인 후 카테고리 내용이 marketplace.json 3 플러그인과 일치 | REMEDIATION-001 완료 전에는 M5 미착수(게이트) |
| AC-IA-012 | REQ-IA-012 | (a) `ls -d www/content/cli` (존재, exit 0); (b) `grep -rnE 'url:[[:space:]]*/code' www/content/cli --include='*.md'` — **매치 0건 = PASS, 1건 이상 = FAIL** (`\|\| true` 제거: 매치가 실패를 유발해야 함); (c) 권위 검출(EC-5): `cd www && hugo --gc --minify` 가 중복 URL을 빌드 에러로 표면화 | `content/cli/` 존재 AND `/cli`↔`/code` URL 무충돌(grep 매치 0 AND hugo exit 0) |
| AC-IA-013 | REQ-IA-013 | CLI 5 섹션 `_index.md` 존재 + 원문 복붙 아님(재저작) 육안/샘플 확인 | 5 섹션 매핑 반영, raw port 아님 |
| AC-IA-014 | REQ-IA-014 | `grep -rl 'stateDiagram' www/content/cli` | MoAI-ADK 섹션에 PLAN→RUN→SYNC stateDiagram 1개 이상 |
| AC-IA-015 | REQ-IA-015 | `grep -rl '바이너리로 심화\|Tier 1\|Tier 2\|Tier 3' www/content/cli` | 브리지 내러티브 + Tier 1~3 표 재사용 흔적 |
| AC-IA-016 | REQ-IA-016 | `ls -d www/content/office 2>&1` 이동 확인 + help 하 통합 + alias | office 도움말 통합 + alias; cookbook/releases 유지 |
| AC-IA-017 | REQ-IA-017 | `grep -c 'track-marketing' www/data/menu/main.yaml` 등 track 항목 | 각 track 메뉴 1회만(중복 제거) |
| AC-IA-018 | REQ-IA-018 | (a) in-scope 집합 비어있지 않음 `grep -rl '^ia_in_scope: true' www/content --include='*.md' \| wc -l` (≥ 1 — HEAD=0이면 아래 (b)가 vacuous 통과하므로 반드시 선행 가드); (b) in-scope 집합(REQ-IA-024 마커)의 각 페이지에서 두 번째 `---`(프론트매터 종료) 이후 첫 비어있지 않은 본문 라인이 표(`\|`)·코드펜스(` ``` `)로 시작하지 않는지 집계(prose-first 기계 근사) | **(a) in-scope 집합 ≥ 1** AND (b) 표/코드펜스가 첫 본문 블록인 페이지 0; 정성 최종판정은 sync-auditor 표본 보완(§B 하단 주석) |
| AC-IA-019 | REQ-IA-019 | in-scope 집합 = `grep -rl '^ia_in_scope: true' www/content --include='*.md'` (REQ-IA-024 마커). mermaid 누락 = `comm -23 <(grep -rl '^ia_in_scope: true' www/content --include='*.md' \| sort) <(grep -rl '```mermaid' www/content --include='*.md' \| sort) \| wc -l` | in-scope 집합 비어있지 않음(≥ 1) **AND** mermaid 누락 0 (집합차 = mermaid 미보유 in-scope 페이지 = 0) |
| AC-IA-020 | REQ-IA-020 | (a) source-index CLI 축 확장 — (a1) 제한 문구 제거 `grep -cE '다루지 않' www/content/help/source-index.md` (→ 0; HEAD=4로 판별) AND (a2) `/cli/` 경로 참조 존재 `grep -cE '/cli/' www/content/help/source-index.md` (≥ 1; HEAD=0로 판별. **`CLI` 문자열 grep 금지** — 기존 "개발자/CLI·SDK … 다루지 않음" 문장과 매치되어 자기통과하므로 반드시 `/cli/` 리터럴 사용); (b) in-scope 출처 블록 커버리지 — **in-scope 집합 ≥ 1** AND `comm -23 <(grep -rl '^ia_in_scope: true' www/content --include='*.md' \| sort) <(grep -rlE '^#{2,4}[[:space:]]*(Sources\|출처\|참고)' www/content --include='*.md' \| sort) \| wc -l` (→ 0) | (a1) 제한 문구 0 AND (a2) `/cli/` 참조 ≥ 1 AND (b) in-scope 집합 비어있지 않음 AND 출처 블록 누락 0 |
| AC-IA-021 | REQ-IA-021 | 데스크탑/CLI 표본 페이지 톤 육안 확인 | 축별 이중 톤 준수 |
| AC-IA-022 | REQ-IA-022 | `find www/content -maxdepth 1 -type d` 신규 prefix 목록 | 신규 top-level prefix는 `cli`만 |
| AC-IA-023 | REQ-IA-023 | (a) 빌드 sub-check (**단독으로는 broken-link 증거 아님**): `cd www && hugo --gc --minify` → exit 0; (b) 권위 broken-link 검증: 신규 전용 링크체커 `node www/scripts/check-links.mjs www/public` → exit 0 AND `broken internal links: 0` 출력. 근거: hugo.toml `refLinksErrorLevel` 미설정 + 콘텐츠 `ref`/`relref` 미사용 → hugo가 내부 링크를 무검증하므로 exit 0 = 무파손 아님; `check-docs-health.mjs`는 링크체커 아님(카운트 검사기) | (a) hugo build exit 0 **AND** (b) 전용 링크체커 broken internal link 0 (두 sub-check 별개) |
| AC-IA-024 | REQ-IA-024 | (a) 마커 집합 비어있지 않음: `grep -rl '^ia_in_scope: true' www/content --include='*.md' \| wc -l` (≥ 1); (b) 전량-신규/재작성 트리 floor 가드 — 신규 `content/cli/**` AND 재작성 플러그인 카테고리 `content/plugins/{chat,cowork,design,code}/**` 전 페이지 마킹: `comm -23 <(find www/content/cli www/content/plugins/chat www/content/plugins/cowork www/content/plugins/design www/content/plugins/code -name '*.md' 2>/dev/null \| sort) <(grep -rl '^ia_in_scope: true' www/content/cli www/content/plugins/chat www/content/plugins/cowork www/content/plugins/design www/content/plugins/code --include='*.md' 2>/dev/null \| sort) \| wc -l` (→ 0); (c) 부분-재작성 트리(병합 DESIGN 등 — 흡수만 되고 미변경 페이지가 있어 전량 floor 가드가 부적절)는 manager-develop가 §plan E6에서 실제 재작성 페이지 마커 완전성 자기검증(marker-escape로 AC-018/019/020 우회 방지) | (a) ≥ 1 AND (b) cli+플러그인 카테고리 마킹 누락 0 AND (c) DESIGN 등 부분-재작성 트리 E6 자기검증 보고 |

> **AC-IA-018/021 정성 항목 주석**: prose-first·톤은 완전 기계화가 어려운 정성 기준이다. AC-IA-018은 in-scope 마커 집합(REQ-IA-024)을 iterate하여 각 페이지 첫 본문 블록이 표/코드펜스로 시작하지 않는지 기계 근사하고, AC-IA-021(톤)은 축별 금칙어/권장어 grep으로 보조하되 최종 판정은 sync-auditor 표본 확인으로 보완한다. must-pass는 AC-IA-023(빌드 exit 0 + 전용 링크체커 broken 0)·AC-IA-005/006/007/010/012(구조 delta + per-page alias 커버리지)·AC-IA-001(2축)·AC-IA-019/024(in-scope mermaid + 마커)이다.
>
> **iter-3 판별력 강화 주석**: in-scope 마커 집합을 iterate하는 AC(AC-IA-018/019/020(b)/024)는 마커 집합이 비어 있으면(HEAD 실측=0) `comm`/집계가 vacuous하게 0을 반환해 자기통과한다. 이를 막기 위해 AC-IA-018/019/020(b)/024는 모두 **"in-scope 집합 ≥ 1" 선행 가드**를 둔다. 또한 AC-IA-006(alias 카운트=10, HEAD 불변)·AC-IA-020(a)(`CLI` 문자열이 기존 제한 문장에 이미 존재)는 단독으로 자기통과하므로 각각 삭제 신호 AND(AC-006)·제한문구 제거 + `/cli/` 리터럴 AND(AC-020a)로 재구성했다.

---

## §C. Edge Cases

- **EC-1 — REMEDIATION-001 미완료**: M5 착수 시 게이트 미충족 → manager-develop는 blocker report 반환, M1~M4·M6 선행 완료 후 M5만 대기.
- **EC-2 — claude-design 고유 콘텐츠 손실**: 병합 시 `claude-design/`에만 있던 페이지(예: official-quickstart)가 `design/`에 흡수되지 않으면 링크 파손 → 흡수 매트릭스 + alias로 방어(AC-IA-006).
- **EC-3 — 구 plugins 경로 다수 alias**: 33p 각각 alias 필요 → 아카이브 정책(이동 vs 삭제) 사용자 확인 필요 시 blocker report(B11).
- **EC-4 — Tier 1~3 표 미확정**: BOOTSTRAP-DESKTOP-001의 Tier 표가 미확정이면 M4 브리지 내러티브 보류 → blocker report.
- **EC-5 — /cli 하위 slug가 /code와 우연 충돌**: `hugo` 빌드가 중복 URL을 에러로 표면화 → AC-IA-023이 포착.
- **EC-6 — mermaid 문법 오류**: geekdoc은 렌더 시점 검증이 약함 → 빌드는 통과하나 렌더 깨짐 가능 → 표본 렌더 확인을 M6 체크에 포함.

---

## §D. Quality Gates (must-pass)

1. `cd www && hugo --gc --minify` → **exit 0** (AC-IA-023 sub-check a — 단독으로 broken-link 증거 아님).
2. 전용 링크체커 `node www/scripts/check-links.mjs www/public` → broken internal link **0** (AC-IA-023 sub-check b — 권위 검출).
3. 2축 메뉴 마커 grep 통과 (AC-IA-001/004).
4. `content/claude-design/` 부재 + per-page alias 커버리지 ≥ 10 (AC-IA-005/006).
5. `content/plugins/` 4 카테고리 + 구 경로 per-page alias 커버리지 ≥ 33 (AC-IA-007/010).
6. `content/cli/` 존재 + `/cli`↔`/code` URL 무충돌(grep 매치 0) + 신규 prefix는 `cli`만 (AC-IA-012/022).
7. in-scope 페이지 mermaid 누락 0 (AC-IA-019).
8. in-scope 페이지 `ia_in_scope: true` 마커 식별 + 신규 `content/cli/**` 전 페이지 마킹 (AC-IA-024).

## §E. Definition of Done

- [ ] REQ-IA-001..024 전부 대응 AC 통과(또는 게이트 항목 EC-1/EC-4 blocker로 명시적 보류).
- [ ] `hugo --gc --minify` green(보조 sub-check) + 전용 링크체커(`www/scripts/check-links.mjs`) broken link 0(권위 검출).
- [ ] 메뉴 2축 + 공통 하단 재편 완료, 데스크탑/CLI 순서 규약 준수.
- [ ] DESIGN 병합 + claude-design 폐기 + alias.
- [ ] plugins 4 카테고리 재작성(REMEDIATION-001 완료 시) + 구 경로 alias.
- [ ] `/cli/` 5 섹션 신규 콘텐츠(재저작) + stateDiagram + 브리지 내러티브.
- [ ] office 도움말 통합 + tracks 중복 제거.
- [ ] source-index CLI 축 확장.
- [ ] in-scope 페이지 `ia_in_scope: true` 마커 + per-page mermaid + 출처 블록 + 이중 톤.
- [ ] `www/**` 외 트리 무변경(scope discipline).
- [ ] Conventional Commits + `🗿 MoAI` trailer, 버전 SSOT 불변.
