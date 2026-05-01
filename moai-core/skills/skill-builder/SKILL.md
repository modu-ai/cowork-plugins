---
name: skill-builder
description: |
  6-Phase 스킬 생성 워크플로우. revfactory/harness 방법론을 기반으로 체계적으로 새 스킬을 생성합니다.
  요구사항 분석부터 최종 검증까지 전체 생명주기를 관리합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "새 스킬 만들어줘", "스킬 생성", "skill-builder"
  - "이 기능 스킬로 만들고 싶어", "스킬 제작"
  - "Vibe 스킬 추가", "새 플러그인 스킬"
  - skill-template으로 시작한 스킬의 체계적 생성이 필요할 때
  - /harness 커맨드의 new 단계로 진입할 때
user-invocable: true
---

# Skill Builder — 6-Phase 스킬 생성 워크플로우

> moai-core | revfactory/harness 방법론 기반 스킬 생성

## 개요

harness 오픈소스의 6-Phase 스킬 생성 워크플로우를 MoAI cowork-plugins 컨텍스트에 맞게 변환한 스킬입니다. 수작업 스킬 작성의 품질 편차를 줄이고, 체계적인 생성 프로세스를 통해 일관된 품질의 스킬을 생산합니다.

> **이름 이력**: v1.3.x까지 `skill-forge`로 제공되던 스킬이 v1.5.x에서 `skill-builder`로 이름 변경되었습니다. 별칭은 유지되지 않으며 모든 참조는 `skill-builder`로 갱신해야 합니다.

## 트리거 키워드

스킬 생성 스킬 제작 skill-builder 새 스킬 만들기 스킬 추가 신규 스킬 harness 워크플로우

## 워크플로우

```
Phase 1: Requirements → 사용자 의도 분석, 트리거 키워드 정의
Phase 2: Architecture → 에이전트 패턴 선택 (6종 중 매핑)
Phase 3: Skill Draft  → skill-template 기반 SKILL.md 초안 생성
Phase 4: Test Gen     → 테스트 프롬프트 2-3개 + 기대 출력 정의
Phase 5: Validation   → 4차원 루브릭 스코어링 (skill-tester 본문 §스코어링 루브릭)
Phase 6: Review       → 품질 게이트 통과 확인, 파일 배치
```

## 실행 규칙

### Phase 1: Requirements (요구사항 분석)

사용자의 자연어 요청에서 스킬 요구사항을 추출합니다.

**필수 수집 항목:**

| 항목 | 질문 | 예시 |
|------|------|------|
| 목적 | "이 스킬이 해결할 문제는?" | "영업 제안서를 자동 생성하고 싶다" |
| 타겟 플러그인 | "어느 플러그인에 배치할까?" | moai-business |
| 입력 | "사용자가 무엇을 입력하나?" | 회사명, 타겟 산업, 제품 정보 |
| 출력 | "어떤 산출물을 기대하나?" | 제안서 DOCX 파일 |
| 복잡도 | "스킬이 얼마나 복잡한가?" | Standard (50-150줄) |

**출력물:** 요구사항 문서 (인메모리, AskUserQuestion으로 확인)

### Phase 2: Architecture (아키텍처 선택)

6개 에이전트 패턴 중 최적 패턴을 선택합니다.

| 패턴 | 적용 시나리오 | 스킬 예시 |
|------|-------------|-----------|
| Pipeline | 순차 처리, 각 단계 출력이 다음 입력 | docx-generator, blog |
| Fan-out/Fan-in | 병렬 분석 후 결과 통합 | ux-designer, market-analysis |
| Expert Pool | 다 도메인 전문 지식 결합 | consulting-brief, startup-launchpad |
| Producer-Reviewer | 생성 + 품질 검토 순환 | sales-playbook, copywriting |
| Supervisor | 다수 전문 스킬 오케스트레이션 | ai-diagnostic, project |
| Hierarchical Delegation | 복잡 작업 계층적 분해 | startup-launchpad |

**선택 기준:** 스킬의 워크플로우 단계 수, 병렬성 여부, 품질 검증 필요성을 기준으로 판단합니다.

**출력물:** 선택된 패턴 + 근거 (1-2문장)

### Phase 3: Skill Draft (스킬 초안 생성)

`skill-template` 템플릿을 기반으로 SKILL.md 초안을 생성합니다.

**필수 적용:**

1. skill-template의 필수 섹션 구조 사용
2. Frontmatter는 `name`, `description`만 포함 (metadata 금지)
3. 트리거 키워드는 기존 73개 스킬과 중복되지 않도록 검사
4. 사용 예시 최소 2개 포함
5. 관련 스킬 섹션에 before/after/alternative 관계 명시

**참조:** `moai-core/skills/skill-tester/SKILL.md` §스코어링 루브릭 (품질 기준 single source)
**참조:** `moai-core/skills/skill-template/SKILL.md` (템플릿)

**출력물:** `<target-plugin>/skills/<skill-name>/SKILL.md` 초안

### Phase 4: Test Generation (테스트 생성)

스킬 검증용 테스트 케이스를 생성합니다.

**테스트 구성:**

```yaml
tests:
  - name: "happy-path"
    prompt: "<대표적인 사용 프롬프트>"
    expected_output:
      format: "<출력 형식>"
      contains: ["<필수 포함 내용>"]
      not_contains: ["<금지 내용>"]

  - name: "edge-case"
    prompt: "<경계 조건 프롬프트>"
    expected_output:
      handles_gracefully: true
      fallback_behavior: "<설명>"

  - name: "complex-input"
    prompt: "<복잡한 입력 프롬프트>"
    expected_output:
      completeness: "모든 요구사항 충족"
```

**출력물:** `<skill-dir>/tests/test-cases.yaml`

### Phase 5: Validation (품질 검증)

4차원 루브릭으로 스킬을 평가합니다.

| 차원 | 가중치 | 평가 |
|------|--------|------|
| Correctness | 30% | 목적 달성 여부 |
| Completeness | 25% | 에지 케이스 커버 |
| Clarity | 25% | 사용자 이해 가능성 |
| Efficiency | 20% | 토큰 대비 품질 |

**통과 기준:** 가중 평균 >= 0.70, 모든 차원 >= 0.50

**미달 시:** Phase 3으로 돌아가서 부족한 차원을 보완합니다. 최대 3회 반복.

**참조:** `moai-core/skills/skill-tester/SKILL.md` §스코어링 루브릭 (anchor 점수표 + 평가 절차)

### Phase 6: Review (최종 검토)

배포 전 최종 체크리스트를 실행합니다.

**체크리스트:**

- [ ] Frontmatter 형식 준수 (name, description만, metadata 없음)
- [ ] 필수 섹션 모두 존재 (개요, 트리거, 워크플로우, 예시, 출력, 주의사항, 관련 스킬)
- [ ] 트리거 키워드가 기존 스킬과 중복되지 않음
- [ ] plugin.json 버전이 업데이트 필요한 경우 안내
- [ ] 스킬 체인 관계가 CLAUDE.local.md §3-3과 일치 (해당 시)
- [ ] 테스트 케이스가 생성됨
- [ ] 루브릭 스코어 0.70 이상 통과

**배치:** `<target-plugin>/skills/<skill-name>/SKILL.md` 에 최종 파일을 배치합니다.

## 사용 예시

**예시 1: 신규 스킬 생성**
> "moai-business에 영업 제안서 자동 생성 스킬을 만들어줘. 회사명과 타겟 기업 입력하면 제안서 DOCX가 나오게"

**예시 2: Vibe 갭 스킬 생성**
> "skill-builder로 moai-product에 UX 디자인 분석 스킬을 만들어줘. Vibe Designing 기능 참고해서"

## 출력 형식

| 산출물 | 위치 | 설명 |
|--------|------|------|
| SKILL.md | `<plugin>/skills/<name>/SKILL.md` | 완성된 스킬 정의 |
| test-cases.yaml | `<plugin>/skills/<name>/tests/` | 테스트 케이스 |
| score-report | 인메모리 | 루브릭 스코어 보고서 |

## 주의사항

- 기존 스킬 수정이 아닌 **신규 스킬 생성**에만 사용합니다
- 플러그인 디렉토리(`moai-*`)가 존재하는지 사전 확인이 필요합니다
- 스킬 생성 후 plugin.json 버전 bump는 릴리스 절차(CLAUDE.local.md §1)에서 일괄 처리합니다
- 트리거 키워드 중복 시 기존 스킬의 description을 확인하여 명확히 구분해야 합니다

## 관련 스킬

| 스킬 | 관계 | 설명 |
|------|------|------|
| skill-template | before | 템플릿 구조를 제공하는 기반 스킬 |
| skill-tester | after | 생성된 스킬의 테스트 실행 + 루브릭 스코어링 |
| ai-slop-reviewer | after | 스킬 본문의 AI 패턴 검수 (선택) |

## 관련 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/harness` | new→test→review 자동 연쇄 (이 스킬 + skill-tester + ai-slop-reviewer 오케스트레이션) |

---

Version: 1.5.x (renamed from skill-forge)
Source: revfactory/harness 6-Phase workflow (Apache 2.0) + MoAI adaptation
Last Updated: 2026-05-01
