---
id: SPEC-MOC-PM-REDESIGN-001
title: "moai-pm project 스킬 재설계 — Fable 5 행동 패턴 증류 + 4-표면 셋업 프로토콜 재설계"
version: "0.1.0"
status: completed
created: 2026-07-09
updated: 2026-07-09
author: Goos Kim
priority: P1
phase: "moai-pm v0.3.0"
module: "plugins/moai-pm/skills/project"
lifecycle: spec-anchored
tags: "plugin, pm, hub-router, claudemd, redesign, fable5-distill"
tier: M
partially_superseded_by: [SPEC-MOC-PM-ADVISORS-001]
---

# SPEC-MOC-PM-REDESIGN-001: moai-pm project 스킬 재설계

> **Tier**: M (Standard)
> **Scope**: PM 공통 계층(claudemd-generator + CLAUDE.md.tmpl) + 3개 분기(cowork/coder/designer setup) + 체인 실행·맥락 규칙 보조 파일 — 총 9개 markdown 파일 재설계
> **Pattern Source**: 공개 유출된 Claude Fable 5 시스템 프롬프트(`https://raw.githubusercontent.com/asgeirtj/system_prompts_leaks/main/Anthropic/claude-fable-5.md`)에서 행동 패턴을 **증류(재표현)** — 원문 비수록, URL 출처 주석만 남김
> **User-approved decisions**: (1) 패턴 증류(원문 복사 아님), (2) 4-표면 전체 범위, (3) 기존 셋업 프로토콜 전면 재설계(증분 패치 아님)

---

## 1. 개요 (Overview)

### 1.1 배경

moai-pm `project` 스킬(v0.2.0)은 4-plugin 허브 라우터로서 코워커·디자이너·코더 분기의 셋업 프로토콜을 위임 실행하고 프로젝트 CLAUDE.md를 생성한다. 현재 생성되는 CLAUDE.md와 셋업 프로토콜에는 다음 행동 규칙 공백이 있다:

1. **요청 평가 순서 부재** — 단순 질문에도 체인·파일 생성이 과잉 트리거될 수 있는 판단 기준 공백
2. **파일 생성 판단 기준 부재** — 짧은 답변으로 충분한 요청에 오피스 파일을 만들거나, 장문 산출물을 일괄 생성해 품질이 저하되는 공백
3. **저작권 가드 부재** — content-* 체인이 외부 자료를 인용·요약할 때의 인용 한도·재표현 원칙 부재 (법적 위험)
4. **검색 스케일링 부재** — 외부 사실 확인 시 요청 복잡도에 비례한 도구 호출 규모 기준 부재
5. **맥락 적용 규칙 부재** — 수집된 프로젝트 맥락(.moai/context.md, CLAUDE.md 프로젝트 개요)의 선택적·자연스러운 적용 규칙과 메타 코멘터리 금지 부재
6. **톤 규칙 부재** — 생성된 CLAUDE.md가 런타임 산출물의 과잉 포맷팅·과잉 설명을 통제하지 않음

Claude Fable 5 시스템 프롬프트(공개 유출본)는 위 6개 공백에 대응하는 검증된 행동 패턴을 담고 있다. 본 SPEC은 그 패턴을 **원문 복사 없이 증류**하여 4개 표면(공통 계층 + 3 분기)에 재설계 반영한다.

### 1.2 목표

- **G1**: 공통 계층(claudemd-generator.md + CLAUDE.md.tmpl)에 요청 평가 사다리·파일 생성 기준·맥락 적용 규칙·톤 규칙을 신설 — 모든 생성 CLAUDE.md가 상속
- **G2**: 코워커 분기 재설계 — 인터뷰 + 수집 맥락 분석 + 스킬 체이닝 + 도구 사용을 종합해, 런타임에 워크플로우 체인·스킬 호출로 작업을 라우팅하는 CLAUDE.md 생성. content 체인에 저작권 가드 HARD 블록 신설
- **G3**: 코더 분기 재설계 — 대상 프로젝트에 MoAI-ADK 3.0 정본 baseline(.claude/ rules·agents·hooks·commands + .moai/ config·specs + CLAUDE.md)을 `moai-coder:moai-workflow-project` 정본 템플릿으로 설치·구성
- **G4**: 디자이너 분기 — DESIGN.md 합성 5-Phase 플로우를 보존하면서 공통 패턴(파일 생성 기준·맥락 적용) 흡수
- **G5**: 체인 실행 규칙(execution-protocol)에 검색 스케일링 신설, 맥락 수집 규칙(context-collector)에 맥락 적용·메타 코멘터리 금지 신설

### 1.3 증류 패턴 6종 (P1-P6)

| # | 패턴 | 원 섹션 | 반영 표면 |
|---|------|---------|-----------|
| P1 | 검색 스케일링 (단일 사실 1회 / 비교·검증 3-5회 / 심층 5-10회+, 확립 개념 검색 생략, 최신성 민감 정보 필수 검색) | Search Scaling | execution-protocol.md + CLAUDE.md.tmpl 실행 플로우 |
| P2 | 인용·저작권 가드 (인용 15단어 미만·출처당 1회, 가사·시 전문 재현 금지, 원문 대체 요약 금지, 기본은 재표현) | Copyright | cowork-setup.md content 체인 + CLAUDE.md.tmpl HARD 블록 |
| P3 | 파일 생성 기준 (독립 산출물·장문 → 파일, 지식 답변·단문 → 대화; 장문은 개요→섹션→검토 반복 생성) | File Creation | CLAUDE.md.tmpl + cowork/designer 분기 산출물 규칙 |
| P4 | 요청 평가 사다리 (대화형 답변 → 스킬/도구 → 파일 생성 순서 판단; 라우팅 과정 서술 금지) | Request Evaluation | claudemd-generator 공통 계층 + CLAUDE.md.tmpl |
| P5 | 맥락 적용 규칙 (수집 맥락의 선택적·자연스러운 적용, 검색·회수 기계 서술 금지) | Memory System | context-collector.md + CLAUDE.md.tmpl 프로젝트 맥락 섹션 |
| P6 | 톤 규칙 (프로즈 기본·불릿/볼드 남용 금지, 응답 깊이 ∝ 요청 깊이, 과잉 설명·과잉 되묻기 회피) | Tone & Formatting | CLAUDE.md.tmpl |

**명시 제외 패턴** (MoAI-ADK가 이미 더 잘 다루거나 consumer claude.ai 전제): 토큰 예산 관리, 스킬 사전 로드(skill pre-read), MCP 커넥터 opt-in, artifacts 윈도 세부, consumer 메모리 시스템 기제. §3 Out of Scope 참조.

---

## 2. REQUIREMENTS (GEARS)

### 2.1 공통 계층 (G1)

#### REQ-PMR-001: 요청 평가 사다리 (P4)

**The claudemd-generator SHALL** inject a request-evaluation ladder under the canonical heading `요청 평가 사다리` into every generated CLAUDE.md, ordered as:

1. 대화형 답변으로 충분한가 → 프로즈로 답하고 종료 (체인 미기동)
2. 설치된 스킬/도구가 범주 적합한가 → 해당 스킬 체인 실행
3. 파일 산출물 요청 신호가 있는가 ("파일로", "저장해줘", 오피스 포맷 지정 등) → 파일 생성

**The generated CLAUDE.md SHALL NOT** instruct runtime to narrate the routing decision (선택하고 산출한다 — 도구 선택 과정을 사용자에게 서술하지 않는다).

**Rationale**: 단순 조회에 체인·파일이 과잉 기동하는 것을 판단 순서로 차단한다. execution-protocol.md의 기존 "단순 요청 원칙"과 정합.

#### REQ-PMR-002: 파일 생성 기준 (P3)

**The generated CLAUDE.md SHALL** contain file-creation criteria under the canonical heading `파일 생성 기준`:

- 파일 생성 대상: 독립 산출물(보고서·계약서 초안·기획서 등), 오피스 포맷(DOCX/PPTX/XLSX/HWPX), 대화 밖에서 사용할 결과물, 수정·반복 대상 산출물
- 대화 응답 대상: 지식 질문 답변, 짧은 목록·표, 간단 설명, 조회·요약 응답
- 장문 산출물은 일괄 생성하지 않고 반복 생성한다: 개요 → 섹션별 작성 → 검토 → 마무리
- 단문 산출물은 한 번에 생성한다

**Rationale**: 파일 과잉 생성과 장문 일괄 생성 품질 저하를 동시에 막는다. 임계값 수치는 원문 그대로 옮기지 않고 산출물 유형 기준으로 재표현한다.

#### REQ-PMR-003: 맥락 적용 규칙 (P5)

**The generated CLAUDE.md and context-collector.md SHALL** define context-application rules under the canonical heading `맥락 적용 규칙`:

- 수집된 프로젝트 맥락(CLAUDE.md 프로젝트 개요 + `.moai/context.md`)은 현재 요청과 관련 있을 때만 선택적으로 적용한다
- 적용 시 태생적으로 아는 것처럼 자연스럽게 반영한다
- **SHALL NOT**: 맥락 회수를 메타 서술하는 문구("저장된 맥락에 따르면", "제가 기억하기로는", "프로젝트 개요를 보니" 류)를 산출물·응답에 사용하지 않는다
- 일반 지식 질문에는 프로젝트 맥락을 억지로 결부하지 않는다

**Rationale**: 맥락 기계 서술은 산출물 품질과 몰입을 해친다. 재진입(resume) 세션에서 특히 빈발하는 결함.

#### REQ-PMR-004: 톤 규칙 (P6)

**The generated CLAUDE.md SHALL** contain tone rules under the canonical heading `톤 규칙`:

- 프로즈 기본 — 불릿·번호 목록·볼드는 구조가 필수이거나 사용자가 요청할 때만
- 응답 깊이는 요청 깊이에 비례한다 (짧은 질문에 장문 설명 금지, 과잉 설명 회피)
- 텍스트 대화에서 불필요한 되묻기를 회피한다; 구조화 질문은 AskUserQuestion으로 수행한다 (1라운드 4질문 이내 — NFR-PMR-005와 정합)

**Rationale**: 생성 CLAUDE.md가 런타임 산출물의 AI-슬롭성 과잉 포맷팅을 통제한다. 기존 ai-slop 후처리(사후 검수)와 상보적인 사전 통제.

#### REQ-PMR-005: 200라인 예산 재배분

**The claudemd-generator SHALL** re-allocate the 200-line budget table to fund the new common rule blocks (요청 평가 사다리 + 파일 생성 기준 + 맥락 적용 규칙 + 톤 규칙 + 인용·저작권 가드) from the existing 여유분, keeping 합계 ≤ 200라인 and 체인 최대 10개 invariant.

**Rationale**: NFR-PMR-002 불변식을 라인 예산 수준에서 증명 가능하게 유지한다.

### 2.2 코워커 분기 (G2)

#### REQ-PMR-006: 코워커 셋업 재설계 — 맥락 분석 기반 체인 설계

**The cowork-setup protocol SHALL** redesign the 8-Phase workflow so that:

- Phase 1 인터뷰와 Phase 2 인벤토리 결과에 더해, **수집된 프로젝트 맥락 분석 단계**가 Phase 3 체인 설계의 명시적 입력이 된다 (어떤 맥락 근거로 어떤 체인을 설계했는지 Phase 5 확인 요약에 기록)
- 생성되는 CLAUDE.md는 런타임에 작업을 **워크플로우 체인과 스킬 호출로 라우팅**한다 (산출물 요청 → 체인 매칭 → 순차 실행 → ai-slop 종료)
- 역할 자동 감지(실무 동료 / 글쓰기 작가 모자 교체)와 8-Phase 골격(인터뷰→인벤토리→체인설계→Gap→확인→CLAUDE.md→API키→첫실행)은 보존한다

**Rationale**: 사용자 승인 결정 3 — 코워커 분기의 핵심 요구는 "인터뷰 + 맥락 분석 + 스킬 체이닝 + 도구 사용 → 런타임 라우팅 CLAUDE.md"다.

#### REQ-PMR-007: 인용·저작권 가드 (P2)

**When** 코워커 체인이 외부 자료(기사·서적·가사·시 등)를 인용하거나 요약할 때, **the generated CLAUDE.md and cowork-setup content-chain rules SHALL** enforce under the canonical heading `인용·저작권 가드`:

- 직접 인용은 원문 15단어 미만, 출처당 최대 1회
- 가사·시는 한 줄도 전문 재현하지 않는다
- 원문의 구조·서사 흐름을 대체하는 요약(원문을 대신 소비하게 만드는 요약)을 생성하지 않는다
- 기본 동작은 자기 문장으로의 완전 재표현이다 (인용은 고유하게 표현된 통찰에 한정된 예외)

**Rationale**: content-*·book-*·story-* 체인의 법적 위험 차단. HARD 블록으로 고정 포함된다.

#### REQ-PMR-008: 검색 스케일링 (P1)

**When** 체인 실행이 외부 사실 확인(WebSearch/WebFetch)을 요구할 때, **the execution-protocol SHALL** scale tool calls under the canonical heading `검색 스케일링`:

- 단일 사실·시세·현직 확인: 1회 호출
- 비교·정책·검증 필요 주제: 3-5회
- 심층 리서치·다출처 종합: 5-10회+
- 확립된 개념·역사적 사실·불변 정의: 검색 생략
- 최신성이 결과를 좌우하는 정보(시세·인물 현직·미인지 제품): 반드시 검색

**Rationale**: execution-protocol §3.5 Layer 2.5 근거 게이트(출처 확인 의무)와 §6-4 검증 깊이 사다리에 "몇 번 찾을 것인가" 축을 보완한다.

### 2.3 코더 분기 (G3)

#### REQ-PMR-009: MoAI-ADK 3.0 정본 baseline 설치

**The coder-setup protocol SHALL** install/configure the MoAI-ADK 3.0 canonical baseline into the target project via `moai-coder:moai-workflow-project` canonical templates:

- `.claude/` — rules(moai core/workflow/development/language/design) + agents(8 retained) + hooks(품질 게이트) + commands(/moai 서브커맨드)
- `.moai/` — config/sections YAML + specs 디렉토리 구조
- `CLAUDE.md` — MoAI 오케스트레이터 실행 지침 (coder 정본)

**Where** PM 공통 템플릿(CLAUDE.md.tmpl)이 존재하더라도, **the coder-setup SHALL NOT** apply it to the coder branch — 코더 분기의 CLAUDE.md는 moai-coder 정본이 유일 소스다 (두-템플릿 분리 명시).

**Rationale**: 사용자 승인 결정 3 — 코더 분기의 핵심 요구는 MoAI-ADK 3.0 정본 설치·구성이다. 코워커용 체인 템플릿과 개발용 오케스트레이터 지침은 목적이 달라 혼합 시 양쪽 모두 오염된다.

### 2.4 디자이너 분기 (G4)

#### REQ-PMR-010: 디자이너 패턴 흡수 + DESIGN.md 플로우 보존

**The designer-setup protocol SHALL** preserve the DESIGN.md 합성 5-Phase flow (자산 인터뷰 → 설치 확인 → DESIGN.md 합성 → brand 스캐폴드 → 온보딩 안내) **and** absorb the common patterns:

- 파일 생성 기준(P3)을 디자이너 산출물 규칙에 반영 (DESIGN.md·visual-identity.md·tokens.json은 파일 산출물, 자산 분석 결과 요약은 대화 응답)
- 맥락 적용 규칙(P5)을 brand 컨텍스트(`.moai/project/brand/`) 사용 규칙에 반영

**Rationale**: 사용자 승인 결정 3 — 디자이너 분기는 패턴 흡수 대상이며 DESIGN.md 합성 플로우는 보존한다.

### 2.5 공통 (전 표면)

#### REQ-PMR-011: 출처 표기 (주석 전용)

**Where** a redesigned file carries a distilled pattern (P1-P6), **the file SHALL** cite the pattern source URL as an HTML comment only (`<!-- 패턴 출처(재표현): https://raw.githubusercontent.com/asgeirtj/system_prompts_leaks/main/Anthropic/claude-fable-5.md -->`), with no source text reproduced.

#### REQ-PMR-012: 원문 비수록 + 제외 패턴 비흡수

**The redesigned files SHALL NOT** reproduce Fable 5 source text verbatim (15단어 이상 연속 인용 금지 — 저작권 가드를 스스로에게도 적용한다). **The redesigned files SHALL NOT** absorb the excluded patterns: 토큰 예산 관리, 스킬 사전 로드(skill pre-read), MCP 커넥터 opt-in.

#### REQ-PMR-013: 허브 정합

**The hub SKILL.md SHALL** bump version `0.2.0 → 0.3.0`, align references to the redesigned protocols (신규 규칙 블록 존재를 상세 프로토콜 표에 반영), and preserve the hub-router principle (PM은 라우팅만 담당하고 구현하지 않는다). **The INDEX.md SHALL** be updated to reflect the redesigned files.

### 2.6 비기능 요구사항 (불변식 — 재설계 후에도 반드시 성립)

| # | 불변식 |
|---|--------|
| NFR-PMR-001 | 4-plugin 아키텍처(moai-pm/coworker/designer/coder) + 단일 `modu-ai/claude` 마켓플레이스 |
| NFR-PMR-002 | 생성 CLAUDE.md ≤ 200라인, 스킬 체인 최대 10개, 스킬 상세는 런타임 로드(복사 금지) |
| NFR-PMR-003 | 글로벌 프로필 질문 금지(이름·회사·역할) — 프로젝트 맥락만 수집 |
| NFR-PMR-004 | 플러그인/스킬 인벤토리 동적 도출 — 신규 하드코딩 카운트 도입 금지(기존 스냅샷 표기는 스냅샷임을 명시) |
| NFR-PMR-005 | AskUserQuestion 제약: 1라운드 ≤ 4질문, ≤ 4옵션, 첫 옵션 `(권장)` |
| NFR-PMR-006 | 스킬 사용자 표면 언어: 한국어 전용 (본 플러그인 패밀리 ko-only) |
| NFR-PMR-007 | 텍스트 산출물 체인은 `general-ai-slop-reviewer` 종료 + 한국어 최종본은 `general-humanize-korean` 2차 패스 |
| NFR-PMR-008 | Gap Detection + `/project resume` 재진입 플로우 보존 (3개 분기 모두) |

---

## 3. 제외 범위 (Out of Scope)

### Out of Scope — Fable 5 원문 vendoring

- 유출 시스템 프롬프트 원문(전문·부분)을 저장소에 수록하지 않는다. 라이선스·drift 위험 + consumer claude.ai 전제가 Claude Code에 전부 적용되지 않음. URL 출처 주석만 허용(REQ-PMR-011).

### Out of Scope — MoAI-ADK가 이미 더 잘 다루는 패턴

- 토큰 예산 관리(컨텍스트 윈도 관리 rule이 SSOT), 스킬 사전 로드(progressive disclosure가 담당), MCP 커넥터 opt-in(설치 플로우가 담당), consumer 메모리 시스템 기제, artifacts 윈도 세부. 이 패턴들은 증류 대상에서 명시 제외한다.

### Out of Scope — 형제 플러그인 스킬 본문

- `moai-coworker`/`moai-designer`/`moai-coder` 플러그인의 개별 스킬(SKILL.md·references) 본문은 수정하지 않는다. 본 SPEC의 쓰기 표면은 `plugins/moai-pm/skills/project/**` 로 한정된다.

### Out of Scope — 런타임 코드·훅·CLI

- Go 코드, hooks 스크립트, CLI 서브커맨드, marketplace.json 등 실행 계층 변경 없음. 순수 markdown 프로토콜/템플릿 재설계다.

### Out of Scope — MX 태그 생성

- MX 태그 후보는 plan.md에서 **식별만** 한다(run-phase에서 생성). plan-phase에서 태그를 파일에 삽입하지 않는다.

---

## 4. HISTORY

- **0.1.0 (rev 2026-07-09)**: plan-audit iter-1 PASS-WITH-DEBT 0.83 — 4 SHOULD-FIX + 5 MINOR 반영: (D1) AC-PMR-007을 표면별 007a(tmpl, M1)/007b(context-collector, M5)로 분리해 M1 게이트 역전 해소, (D2) frontmatter `tier: M` 명시(tier 부재 시 Tier L 기계 오분류 방지), (D3) REQ-PMR-004 톤 규칙 전용 AC-PMR-018 신설 + S1 헤더 REQ 목록 반영, (D4) P3↔office 우선 판단 계층 순서를 plan §F M1 행에 인코딩 + AC-PMR-R05 리뷰 AC 추가, (D5) 출처 주석 형식 검증 기계화(비주석 매치 = 0), (D6) AC-PMR-005 M1 공통분 임계 정의(2파일), (D7) 신규 블록 "5종 전부 HARD 고정" 단일 열거로 plan/acceptance 정렬, (D8) REQ-PMR-001 canonical heading `요청 평가 사다리` 고정, (D10) AC-PMR-003 tmpl 표면 grep 확장. (D9) AC-PMR-017 명칭-대-개념 잔여는 문서화 부채로 acceptance §D.4 residual에 기록.
- **0.1.0 (2026-07-09)**: 최초 작성 — Fable 5 패턴 증류 6종(P1-P6) + 4-표면 재설계 + 불변식 8종. 사용자 승인 결정 3건(증류·4-표면·전면 재설계) 반영. Tier M, 4 artifacts.
