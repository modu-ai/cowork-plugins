---
id: SPEC-MOC-PM-REDESIGN-001
title: "moai-pm project 스킬 재설계 — 구현 계획"
version: "0.1.0"
status: draft
created: 2026-07-09
updated: 2026-07-09
author: Goos Kim
priority: P1
phase: "moai-pm v0.3.0"
module: "plugins/moai-pm/skills/project"
lifecycle: spec-anchored
tags: "plugin, pm, hub-router, claudemd, redesign, plan"
---

# SPEC-MOC-PM-REDESIGN-001 — plan.md

## §A Context

- **재설계 baseline**: moai-pm `project` 스킬 v0.2.0 (허브 라우터 + 3분기 셋업 프로토콜 + CLAUDE.md.tmpl). 전 파일 실측 완료(2026-07-09).
- **패턴 소스**: Fable 5 시스템 프롬프트 유출본 — WebFetch로 6개 패턴 섹션(Search Scaling / Copyright / File Creation / Request Evaluation / Memory / Tone) 분석 완료. 증류 결과는 spec.md §1.3 P1-P6.
- **쓰기 표면**: `plugins/moai-pm/skills/project/**` 9개 파일 (아래 §F 파일 설계). 형제 플러그인·런타임 코드 불변.
- **선행 SPEC 의존 없음** (`depends_on` 비움). 병렬 세션 race 주의 — 커밋은 pathspec 한정.

## §B Known Issues (baseline 실측)

1. `SKILL.md` 4-plugin 표에 코워커 스킬 수 `192` 하드코딩 흔적 — init-protocol.md는 `193`/`234` 스냅샷 표기. 카운트 표기가 파일 간 불일치(동적 도출 원칙과 긴장). 재설계 시 "스냅샷" 표기로 통일하거나 제거(NFR-PMR-004).
2. `execution-protocol.md`에 검증 깊이 사다리(QUICK/NORMAL/DEEP)는 있으나 "몇 번 검색할 것인가"(스케일링) 축 부재 — P1이 채운다.
3. `CLAUDE.md.tmpl` §6 실행 플로우에 요청 평가 순서(대화→스킬→파일)가 없음 — 스킵 조건만 존재. P4가 채운다.
4. 저작권·인용 규칙이 전 표면에 전무 — content/book/story 체인의 법적 공백. P2가 채운다.
5. `context-collector.md`는 수집만 다루고 **적용** 규칙이 없음 — P5가 채운다.
6. cowork-setup Phase 3 체인 설계가 인터뷰 답변→프리셋 매칭으로 직행 — 수집 맥락 분석 근거가 설계에 기록되지 않음(REQ-PMR-006).

## §C Pre-flight

- [x] SPEC ID 충돌 없음 (`.moai/specs/` 5개 기존 SPEC과 비충돌)
- [x] SPEC ID regex self-check PASS (`SPEC ✓ | MOC ✓ | PM ✓ | REDESIGN ✓ | 001 ✓`)
- [x] baseline 9개 파일 전체 Read 완료
- [x] 패턴 소스 WebFetch + 6패턴 추출 완료
- [ ] run-phase 진입 전: Implementation Kickoff 승인 (HUMAN GATE)

## §D Constraints

- spec.md §2.6 불변식 NFR-PMR-001..008 전부 유지 (재설계는 "전면"이되 불변식은 회귀 금지)
- 원문 15단어+ 연속 인용 금지 — 모든 패턴은 한국어 재표현 (REQ-PMR-012)
- 출처는 HTML 주석 1줄 형식만 (REQ-PMR-011)
- 사용자 표면 한국어 전용, 파일 인코딩 UTF-8/LF
- 우선순위 라벨만 사용, 시간 예측 금지

## §E Self-Verification (run-phase 종료 시 실행)

acceptance.md §D AC 매트릭스의 기계 검증(grep/wc) 배치를 단일 턴 병렬 Bash로 실행하고, Claim/Evidence/Baseline/Gaps/Residual-risk 5섹션 보고로 제출한다. 핵심 배치:

```bash
# 1) 신규 규칙 블록 존재 (canonical heading grep — tmpl 5종 + 분기 표면)
grep -l "요청 평가" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl
grep -l "파일 생성 기준" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl
grep -l "톤 규칙" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl
grep -l "인용·저작권 가드" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl
grep -l "인용·저작권 가드" plugins/moai-pm/skills/project/references/core/cowork-setup.md
grep -l "검색 스케일링" plugins/moai-pm/skills/project/references/core/execution-protocol.md
grep -l "맥락 적용 규칙" plugins/moai-pm/skills/project/references/core/context-collector.md
# 2) 원문 leak 리터럴 0건 + 출처 주석 형식(비주석 매치 0)
grep -riE "severe violation|displacive|Never reproduce" plugins/moai-pm/skills/project/ | wc -l   # 0
grep -rn "system_prompts_leaks" plugins/moai-pm/skills/project/ | grep -v '<!--' | wc -l          # 0
# 3) 불변식 회귀 가드
grep -c "{user_name}" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl          # 0
grep -c "general-ai-slop-reviewer" plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl  # ≥1
grep -c "/project resume" plugins/moai-pm/skills/project/references/core/coder-setup.md           # ≥1
# 4) 템플릿 라인 예산
wc -l < plugins/moai-pm/skills/project/references/templates/CLAUDE.md.tmpl                        # ≤150
```

## §F Milestones (우선순위 기반 — 시간 예측 없음)

### M1 (P0): 공통 계층 재설계

| 파일 | 변경 |
|------|------|
| `references/templates/CLAUDE.md.tmpl` | 신규 규칙 블록 **5종** 삽입 — 전부 HARD 고정(200라인 초과 시 축소 대상 아님, 축소는 체인만): `요청 평가 사다리`(~6라인) · `파일 생성 기준`(~8라인) · `맥락 적용 규칙`(~5라인) · `톤 규칙`(~5라인) · `인용·저작권 가드`(~6라인). **판단 계층 순서(§J R2 결정 인코딩)**: `파일 생성 기준`은 office 스킬 우선 표(§3)의 상위 판단으로 배치 — ① 파일을 만들지 결정(파일 생성 기준) → ② 만들기로 했으면 office 스킬 사용(office 우선 표). 기존 HARD 블록(§3 office 우선, §4 ai-slop) 보존. 출처 주석 1줄. 템플릿 정적 라인 ≤ 150 |
| `references/core/claudemd-generator.md` | §2.1 라인 예산 표 재배분(여유분 59 → 신규 블록 ~30 배정, 잔여 ~29), §6 검증 체크리스트에 신규 블록 5종 확인 항목 추가, 출처 주석 |

완료 조건: AC-PMR-001/002/004/007a/008/018 GREEN + AC-PMR-005 공통분 GREEN — 공통분 정의: 공통 계층 2파일(tmpl·generator) 각각 출처 주석 1줄 존재(파일 수 = 2); 전체 ≥ 3 파일 임계는 M2 이후 충족한다.

### M2 (P0): 코워커 분기 재설계

| 파일 | 변경 |
|------|------|
| `references/core/cowork-setup.md` | 전면 재설계: Phase 3 체인 설계에 **수집 맥락 분석 입력** 명시(인터뷰+인벤토리+맥락분석 → 체인, Phase 5 확인 요약에 설계 근거 기록), `인용·저작권 가드` HARD 블록 신설(content/book/story 체인 적용), 역할 감지·8-Phase 골격·체인 프리셋·ai-slop 종료 보존, 출처 주석 |
| `references/core/execution-protocol.md` | `검색 스케일링` 섹션 신설(§6-4 검증 깊이 사다리와 교차 참조: QUICK↔1회, NORMAL↔3-5회, DEEP↔5-10회+ 정렬), §전체 실행 플로우에 요청 평가 사다리 정합 1줄, 출처 주석 |

완료 조건: AC-PMR-003/006/009 GREEN + 8-Phase 골격 회귀 없음.

### M3 (P1): 코더 분기 재설계

| 파일 | 변경 |
|------|------|
| `references/core/coder-setup.md` | 전면 재설계: Phase 3 정본 스캐폴드를 MoAI-ADK 3.0 baseline 설치 명세로 강화(.claude/ rules·agents·hooks·commands + .moai/ config·specs + CLAUDE.md — `moai-coder:moai-workflow-project` 정본 템플릿 위임 명시), **두-템플릿 분리** 명문화("PM 공통 CLAUDE.md.tmpl은 코더 분기에는 적용하지 않는다"), 5-Phase 골격·Gap Detection·resume 보존 |

완료 조건: AC-PMR-010/011 GREEN.

### M4 (P1): 디자이너 분기 재설계

| 파일 | 변경 |
|------|------|
| `references/core/designer-setup.md` | DESIGN.md 합성 5-Phase 플로우 보존 + 파일 생성 기준(P3)·맥락 적용 규칙(P5)을 분기 산출물 규칙(§3)에 흡수, 출처 주석 |

완료 조건: AC-PMR-012 GREEN.

### M5 (P1): 맥락 규칙 + 허브 정합 + 자체 검증

| 파일 | 변경 |
|------|------|
| `references/core/context-collector.md` | `맥락 적용 규칙` 섹션 신설(선택 적용 + 메타 코멘터리 금지 문구 목록), §5 저장·추적과 연결 |
| `SKILL.md` | version `0.2.0 → 0.3.0`, 상세 프로토콜 표에 신규 규칙 블록 반영, 카운트 표기 스냅샷 통일(§B-1), 허브 라우터 원칙 문구 보존 |
| `references/core/INDEX.md` | 재설계 파일 색인 갱신 |

완료 조건: AC-PMR-007b/013/014/015/016/017 GREEN + §E 검증 배치 전체 GREEN.

## §G Anti-Patterns (run-phase 금지)

- 원문 문장 직역 이식 (재표현 원칙 위반 — AC-PMR-004가 잡는다)
- 신규 규칙 블록을 스킬 상세로 비대화 (CLAUDE.md는 규칙 요약만, 상세는 런타임 스킬 로드 — NFR-PMR-002)
- 형제 플러그인 파일 수정 (쓰기 표면 이탈)
- 신규 하드코딩 카운트 도입 (NFR-PMR-004)
- "전면 재설계" 명분으로 불변식 삭제 (Gap Detection·resume·역할 감지·ai-slop 종료는 보존 대상)
- plan-phase에서 MX 태그 삽입 (식별만 — 아래 §H)

## §H MX 태그 후보 (식별만 — run-phase에서 생성)

| 후보 위치 | 태그 | 근거 |
|-----------|------|------|
| `CLAUDE.md.tmpl` HARD 규칙 블록(office 우선 + ai-slop + 저작권 가드) | `@MX:ANCHOR` | 모든 생성 CLAUDE.md가 상속하는 불변 계약 (high fan-in) |
| `claudemd-generator.md` §2.1 라인 예산 표 | `@MX:ANCHOR` | 200라인 불변식의 증명 지점 |
| `cowork-setup.md` 인용·저작권 가드 블록 | `@MX:WARN` (+ `@MX:REASON`: 법적 위험 영역 — 완화 시 저작권 노출) | 위험 구역 |
| `execution-protocol.md` 검색 스케일링 | `@MX:NOTE` | 검증 깊이 사다리와의 교차 참조 의도 기록 |

## §I Cross-References

- spec.md §1.3 (P1-P6 증류 표) · §2.6 (불변식) · §3 (Out of Scope)
- acceptance.md §D (AC 매트릭스 + GWT 시나리오)
- `.claude/rules/moai/development/spec-frontmatter-schema.md` (frontmatter SSOT)
- 패턴 출처(재표현): `https://raw.githubusercontent.com/asgeirtj/system_prompts_leaks/main/Anthropic/claude-fable-5.md`

## §J Risks

| # | 위험 | 완화 |
|---|------|------|
| R1 | 신규 블록이 200라인 예산을 침식해 체인 슬롯 축소 | M1에서 예산 표 선재배분 + 템플릿 ≤150라인 AC로 상한 고정 |
| R2 | consumer 전제 패턴이 Claude Code 맥락에서 오작동 (예: 파일 생성 기준이 오피스 스킬 우선 규칙과 충돌) | P3 기준을 office 스킬 우선 표의 상위 판단으로 배치("파일을 만들지 결정" → "만들면 office 스킬 사용") — §F M1 tmpl 행에 인코딩 + AC-PMR-R05 리뷰 AC로 검증화 |
| R3 | 전면 재설계 중 불변식 회귀(resume·Gap·역할 감지 누락) | AC-PMR-008..010 회귀 가드 grep + §G 금지 목록 |
| R4 | 병렬 세션이 plugins/moai-pm을 동시 수정 | run-phase 진입 시 pre-spawn sync check + pathspec 커밋 |
| R5 | 유출본 출처의 평판·라이선스 논란 | 원문 비수록 + 재표현 + 주석 1줄 한정(사용자 승인 결정 1) — 잔여 위험은 수용 |
