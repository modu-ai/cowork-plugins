---
id: SPEC-MOC-PM-REDESIGN-001
title: "moai-pm project 스킬 재설계 — 인수 조건"
version: "0.1.0"
status: draft
created: 2026-07-09
updated: 2026-07-09
author: Goos Kim
priority: P1
phase: "moai-pm v0.3.0"
module: "plugins/moai-pm/skills/project"
lifecycle: spec-anchored
tags: "plugin, pm, hub-router, claudemd, redesign, acceptance"
---

# SPEC-MOC-PM-REDESIGN-001 — acceptance.md

기준 디렉토리: `plugins/moai-pm/skills/project/` (이하 `$SK`). 모든 grep은 저장소 루트에서 실행.

## §D AC 매트릭스 (기계 검증)

| AC | REQ | 검증 명령 | 기대값 |
|----|-----|-----------|--------|
| AC-PMR-001 | REQ-PMR-001 | `grep -c "요청 평가" $SK/references/templates/CLAUDE.md.tmpl` | ≥ 1 (사다리 3단계: 대화→스킬→파일 순서 문구 동반) |
| AC-PMR-002 | REQ-PMR-002 | `grep -c "파일 생성 기준" $SK/references/templates/CLAUDE.md.tmpl` | ≥ 1 (반복 생성: 개요→섹션 문구 동반) |
| AC-PMR-003 | REQ-PMR-007 | `grep -c "인용·저작권 가드" $SK/references/core/cowork-setup.md && grep -c "인용·저작권 가드" $SK/references/templates/CLAUDE.md.tmpl && grep -c "15단어" $SK/references/templates/CLAUDE.md.tmpl` | 각 ≥ 1 (tmpl 표면 heading 포함 — 가사·시 재현 금지 문구 동반) |
| AC-PMR-004 | REQ-PMR-012 | `grep -riE "severe violation\|displacive\|Never reproduce" $SK/ \| wc -l` | = 0 (원문 고유 리터럴 부재) |
| AC-PMR-005 | REQ-PMR-011 | `grep -rl "system_prompts_leaks" $SK/ \| wc -l` **AND** `grep -rn "system_prompts_leaks" $SK/ \| grep -v '<!--' \| wc -l` | 파일 수 ≥ 3 **AND** 비주석 매치 = 0 (주석 형식 기계 검증) |
| AC-PMR-006 | REQ-PMR-008 | `grep -c "검색 스케일링" $SK/references/core/execution-protocol.md` | ≥ 1 (1회/3-5회/5-10회 토큰 동반) |
| AC-PMR-007a | REQ-PMR-003 | `grep -c "맥락 적용" $SK/references/templates/CLAUDE.md.tmpl` | ≥ 1 (메타 코멘터리 금지 문구 동반 — M1 표면) |
| AC-PMR-007b | REQ-PMR-003 | `grep -c "맥락 적용 규칙" $SK/references/core/context-collector.md` | ≥ 1 (메타 코멘터리 금지 문구 동반 — M5 표면) |
| AC-PMR-008 | NFR-PMR-003 | `grep -c "{user_name}" $SK/references/templates/CLAUDE.md.tmpl` | = 0 (회귀 가드) |
| AC-PMR-009 | NFR-PMR-007 | `grep -c "general-ai-slop-reviewer" $SK/references/templates/CLAUDE.md.tmpl && grep -c "general-humanize-korean" $SK/references/core/cowork-setup.md` | 각 ≥ 1 |
| AC-PMR-010 | NFR-PMR-008 | `for f in cowork coder designer; do grep -c "/project resume" $SK/references/core/$f-setup.md; done` | 각 ≥ 1 |
| AC-PMR-011 | REQ-PMR-009 | `grep -c "moai-workflow-project" $SK/references/core/coder-setup.md && grep -c "적용하지 않는다" $SK/references/core/coder-setup.md` | 각 ≥ 1 (.claude/ + .moai/ 구조 항목 동반 — 두-템플릿 분리 명문) |
| AC-PMR-012 | REQ-PMR-010 | `grep -c "DESIGN.md" $SK/references/core/designer-setup.md && grep -c "파일 생성 기준" $SK/references/core/designer-setup.md` | DESIGN.md ≥ 3, 기준 ≥ 1 (5-Phase 골격 유지) |
| AC-PMR-013 | REQ-PMR-013 | `grep -c 'version: "0.3.0"' $SK/SKILL.md` | = 1 |
| AC-PMR-014 | REQ-PMR-005, NFR-PMR-002 | `wc -l < $SK/references/templates/CLAUDE.md.tmpl` + generator 예산 표 합계 확인 | 템플릿 ≤ 150라인, 예산 표 합계 ≤ 200 명시 |
| AC-PMR-015 | NFR-PMR-002 | `grep -c "10개" $SK/references/core/claudemd-generator.md` | ≥ 1 (체인 최대 10 invariant 문구 보존) |
| AC-PMR-016 | NFR-PMR-005 | `grep -cE "4질문|4옵션" $SK/references/core/init-protocol.md` | ≥ 1 (AskUserQuestion 제약 표 보존 — 본 파일은 무변경 표면이므로 baseline 동일) |
| AC-PMR-017 | REQ-PMR-012 | `grep -rniE "skill pre-read|스킬 사전 로드|커넥터 opt-in|토큰 예산 관리" $SK/ \| wc -l` | = 0 (제외 패턴 비흡수 — 명칭 리터럴 기준; 개념 잔여는 §D.4 residual/D9 참조) |
| AC-PMR-018 | REQ-PMR-004 | `grep -c "톤 규칙" $SK/references/templates/CLAUDE.md.tmpl` | ≥ 1 (프로즈 기본·응답 깊이 비례 문구 동반) |

### §D.1 리뷰 검증 (기계 grep 불가 — diff 리뷰로 판정)

| AC | 내용 | 판정 방법 |
|----|------|-----------|
| AC-PMR-R01 | 신규 하드코딩 카운트 도입 금지 (NFR-PMR-004) | 재설계 diff에서 신규 숫자 스킬/플러그인 카운트가 "스냅샷·동적 도출" 표기 없이 등장하면 FAIL |
| AC-PMR-R02 | 원문 재표현 품질 | P1-P6 각 블록이 원문 문장 구조를 따라가지 않는 독자적 한국어 문장인지 대조 리뷰 |
| AC-PMR-R03 | 8-Phase(cowork)·5-Phase(coder/designer) 골격 보존 | 재설계 후 Phase 열거가 baseline 골격과 1:1 대응하는지 확인 |
| AC-PMR-R04 | Phase 3 체인 설계에 맥락 분석 근거 기록 (REQ-PMR-006) | cowork-setup Phase 3→5 흐름에 "설계 근거(맥락 출처)" 기록 지점 존재 확인 |
| AC-PMR-R05 | P3↔office 우선 판단 계층 순서 (REQ-PMR-002, plan §J R2) | tmpl에서 `파일 생성 기준` 블록이 office 스킬 우선 표의 **상위 판단**으로 명시되는지 확인 — "① 파일을 만들지 결정 → ② 만들면 office 스킬 사용" 순서 문구 존재 |

## §D.2 Given-When-Then 시나리오

### S1 — 코워커 셋업 E2E (REQ-PMR-001/002/004/006/007)

- **Given** 신규 프로젝트 디렉토리 + moai-coworker 설치 상태
- **When** `/project --cowork`로 8-Phase를 완주하면
- **Then** 생성된 `./CLAUDE.md`는 (a) 200라인 이내, (b) 요청 평가 사다리·파일 생성 기준·맥락 적용 규칙·톤 규칙·인용·저작권 가드 5블록 포함, (c) 체인 ≤ 10개 + 텍스트 체인 ai-slop 종료, (d) Phase 5 확인 요약에 체인 설계의 맥락 근거가 표시된다

### S2 — 코더 셋업 E2E (REQ-PMR-009)

- **Given** 개발 프로젝트(언어·프레임워크 답변 가능 상태) + moai-coder 설치 상태
- **When** `/project --code`로 5-Phase를 완주하면
- **Then** MoAI-ADK 3.0 정본 baseline(.claude/ rules·agents·hooks·commands + .moai/ config·specs + CLAUDE.md)이 `moai-coder:moai-workflow-project` 정본 템플릿 경로로 설치·안내되고, PM 공통 CLAUDE.md.tmpl은 사용되지 않는다

### S3 — 저작권 가드 런타임 (REQ-PMR-007)

- **Given** S1으로 생성된 CLAUDE.md가 로드된 세션
- **When** 사용자가 "이 기사 내용 그대로 실어서 블로그 써줘"라고 요청하면
- **Then** 산출물은 원문 15단어 미만 인용 최대 1회 + 나머지 전부 재표현이며, 원문 구조를 대체하는 요약을 만들지 않는다

### S4 — 맥락 메타 코멘터리 금지 (REQ-PMR-003)

- **Given** `.moai/context.md`에 프로젝트 맥락이 누적된 세션
- **When** 후속 산출물 요청이 들어오면
- **Then** 맥락은 자연스럽게 반영되고, "저장된 맥락에 따르면"·"제가 기억하기로는" 류의 회수 서술 문구가 응답·산출물에 나타나지 않는다

### S5 — 단순 조회 사다리 1단 종료 (REQ-PMR-001)

- **Given** S1으로 생성된 CLAUDE.md가 로드된 세션
- **When** "부가세 신고 기한 언제야?" 같은 단일 사실 질문이 들어오면
- **Then** 체인·파일 생성 없이 프로즈 답변으로 종료하고, 외부 확인이 필요하면 검색 1회로 스케일링된다 (P1·P4 결합)

## §D.3 엣지 케이스

| # | 케이스 | 기대 동작 |
|---|--------|-----------|
| E1 | 필요 플러그인 미설치 상태에서 분기 진입 | Gap Detection → 설치 안내 → `/project resume` 재개 (NFR-PMR-008, 3분기 공통) |
| E2 | 체인 11개+ 설계됨 | 상위 10개만 CLAUDE.md 기록, 나머지 `/project catalog` 유도 (NFR-PMR-002) |
| E3 | 비텍스트 산출물(차트·숫자·미디어) 체인 | ai-slop 종료 생략 규칙 유지 — 저작권 가드도 텍스트 인용 상황에만 발동 |
| E4 | DEEP 등급(법률·세무) 요청 + 외부 인용 동시 발생 | 검증 깊이 사다리(근거 게이트·면책)와 인용·저작권 가드가 중첩 적용 — 상호 배제 아님 |
| E5 | 생성 CLAUDE.md가 200라인 초과 | 체인 자동 축소(최대 10) 후 재검증 — 신규 규칙 블록 5종(요청 평가 사다리·파일 생성 기준·맥락 적용 규칙·톤 규칙·인용·저작권 가드)은 전부 HARD 고정으로 축소 대상 아님 (plan §F M1 열거와 동일) |
| E6 | 코더 분기에서 사용자가 "코워커식 체인 CLAUDE.md"를 요구 | 두-템플릿 분리 안내 + 필요 시 `--cowork` 분기 병행 제안 (REQ-PMR-009) |

## §D.4 품질 게이트 / Definition of Done

- [ ] §D AC 매트릭스 19건 전부 GREEN (단일 턴 병렬 Bash 배치, 증거 verbatim 첨부)
- [ ] §D.1 리뷰 AC 5건 판정 완료 (diff 리뷰 근거 기록)
- [ ] §D.2 시나리오 S1-S5 충족 논거 제시 (S1·S2는 프로토콜 문면 검증, S3-S5는 생성 CLAUDE.md 규칙 문면 검증 — 런타임 실연은 residual로 명시 가능)
- [ ] 불변식 NFR-PMR-001..008 회귀 0건
- [ ] 원문 leak 리터럴 0건 + 출처 주석 형식 준수
- [ ] MX 태그 후보 4건 생성(run-phase) 또는 미생성 사유 기록
- [ ] 검증 보고는 Claim/Evidence/Baseline/Gaps/Residual-risk 5섹션 형식

**Residual-risk (D9 문서화 부채, plan-audit iter-1)**: AC-PMR-017은 제외 패턴의 **명칭 리터럴** 기반 grep이다 — 제외 패턴(토큰 예산 관리·skill pre-read·MCP 커넥터 opt-in)이 다른 표현으로 개념 흡수되는 경우는 grep이 잡지 못한다. AC-PMR-R02 재표현 대조 리뷰 + plan-audit 개념 수준 검토로 보완하며, 잔여 위험으로 수용한다.
