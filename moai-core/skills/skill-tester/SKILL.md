---
name: skill-tester
description: |
  스킬 품질 자동 검증 도구. 생성된 스킬의 테스트 케이스를 실행하고 baseline 대비 개선을 측정합니다.
  A/B 테스트, 회귀 테스트, 체인 테스트 + 4차원 스코어링 루브릭을 단일 스킬에 내장하여 self-contained로 동작합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "스킬 테스트해줘", "스킬 검증", "skill-tester"
  - "이 스킬 품질 확인해줘", "A/B 테스트"
  - "스킬 회귀 테스트", "스킬 체인 테스트"
  - "스킬 루브릭 스코어링", "4차원 평가"
  - skill-builder Phase 5 이후 검증이 필요할 때
  - /harness 커맨드의 test 단계로 진입할 때
user-invocable: true
version: 2.0.0
---

# Skill Tester — 스킬 품질 검증 도구 (루브릭 + 체인 내장)

> moai-core | revfactory/harness 테스트 방법론 기반
> single source of truth for: 4차원 스코어링 루브릭, 스킬 체인 검증 프로토콜

## 개요

skill-builder로 생성된 스킬 또는 기존 스킬의 품질을 검증합니다. harness의 A/B 테스트 방법론을 구현하여 baseline(스킬 없음)과 with-skill(스킬 사용)을 비교하며, **4차원 스코어링 루브릭**과 **체인 검증 프로토콜**을 본문에 직접 포함하여 별도 rules 파일 참조 없이 단독으로 동작합니다.

## 트리거 키워드

스킬 테스트 검증 A/B 테스트 baseline 회귀 테스트 체인 테스트 skill-tester 품질 측정 루브릭 스코어링 4차원 평가

## 워크플로우

```
1. [로드]    → 대상 스킬의 tests/test-cases.yaml 로드
2. [선택]    → 테스트 모드 선택 (A/B | 회귀 | 체인 | 루브릭 단독)
3. [실행]    → 테스트 프롬프트를 Claude Code에 실행
4. [측정]    → 토큰 사용량, 출력 품질, 시간 측정
5. [스코어]  → 4차원 루브릭 가중 평균 산출
6. [비교]    → baseline vs with-skill 결과 비교
7. [보고]    → 스코어 리포트 생성
```

## 실행 규칙

### 테스트 모드

#### Mode 1: A/B 테스트 (신규 스킬 검증)

skill-builder Phase 5에서 사용하는 기본 모드입니다.

**절차:**

1. **Baseline 실행**: 스킬 없이 동일 프롬프트를 Claude Code에 실행
2. **With-Skill 실행**: 스킬 로드 후 동일 프롬프트 실행
3. **비교 측정**:

| 메트릭 | 측정 방법 | 개선 기준 |
|--------|----------|-----------|
| 토큰 사용량 | input + output 토큰 | -10% 이상 감소 |
| 출력 품질 | 루브릭 스코어 | +0.15 이상 향상 |
| 정확성 | assertion 통과율 | 80% 이상 |
| 완전성 | 필수 출력 포함 여부 | 100% |

**샘플 사이즈 가이드:**

| 예상 개선율 | 최소 샘플 수 |
|-------------|------------|
| >= 20% | 2-3회 |
| 10-20% | 3-5회 |
| < 10% | 5회 이상 |

#### Mode 2: 회귀 테스트 (기존 스킬 수정 후)

스킬 수정 시 기존 테스트 케이스가 여전히 통과하는지 확인합니다.

**절차:**

1. 수정 전 마지막 테스트 결과를 baseline으로 로드
2. 수정 후 동일 테스트 케이스 재실행
3. 비교: 기존 통과 항목이 미통과로 변경되면 regression

**회귀 판정:**

| 변화 | 판정 |
|------|------|
| 기존 통과 → 여전히 통과 | PASS |
| 기존 통과 → 미통과 | REGRESSION (수정 롤백 필요) |
| 기존 미통과 → 통과 | IMPROVEMENT |
| 새로운 테스트 추가 | INFO (비교 불가) |

#### Mode 3: 체인 테스트 (스킬 조합 검증)

여러 스킬이 순차적으로 연결되는 체인을 테스트합니다. CLAUDE.local.md §3-3에 정의된 모든 체인이 검증 대상입니다.

##### 3-1. Chain Definition Format

```yaml
chain:
  name: "blog-publishing"
  description: "Blog post creation → AI slop review → optional media generation"
  steps:
    - skill: "moai-content:blog"
      output_type: "markdown"
      provides: ["blog_draft"]
    - skill: "moai-core:ai-slop-reviewer"
      input_from: ["blog_draft"]
      output_type: "markdown"
      provides: ["reviewed_draft"]
    - skill: "moai-media:nano-banana"
      input_from: ["reviewed_draft"]
      output_type: "image_url"
      optional: true
      provides: ["cover_image"]
```

##### 3-2. Test Design Rules

**Happy Path Test** — 전체 체인을 대표 입력으로 실행하고 다음을 검증:
- 각 단계 출력이 다음 단계 입력 스키마와 호환
- 최종 출력이 문서화된 기대치와 일치
- 단계 간 데이터 손실 없음

**Failure Propagation Test** — 각 단계 실패를 시뮬레이션:
- 체인이 우아하게 정지하는가?
- 어느 단계가 실패했는지 사용자에게 전달되는가?
- 실패 지점에서 재개 가능한가?

**Optional Step Test** — 선택적 단계가 있는 체인:
- 선택 단계를 건너뛰어도 체인이 완료되는가
- 선택 단계가 실패해도 체인이 완료되는가
- 선택 단계 출력 없이도 결과가 유의미한가

**Output Compatibility Test** — 각 단계 경계에서:
- 출력 스키마가 다음 단계 기대 입력과 일치
- 언어 일관성 (한국어 출력 → 한국어 입력)
- 형식 일관성 (markdown → markdown)

##### 3-3. Test Case Template

```markdown
## Chain Test: <chain-name>

### TC-1: Happy Path
- Input: <대표 프롬프트>
- Expected Step 1 output: <설명>
- Expected Step 2 output: <설명>
- Expected Final output: <설명>
- Pass criteria: 모든 단계가 기대 출력 생성, 최종 결과 사용 가능

### TC-2: Step <N> Failure
- Input: <단계 N 실패 유발 프롬프트>
- Expected behavior: <체인 정지 / 건너뜀 / 재시도>
- Pass criteria: 사용자에게 전달, 데이터 손실 없음

### TC-3: Optional Step Skip
- Input: <선택 단계 트리거 없는 프롬프트>
- Expected behavior: <선택 단계 없이 체인 완료>
- Pass criteria: 최종 출력이 선택 단계 기여 없이도 유의미함
```

##### 3-4. Known Chains (CLAUDE.local.md §3-3 매핑)

| Chain | Steps | Status |
|-------|-------|--------|
| 사업계획서(PPT) | strategy-planner → pptx-designer → ai-slop-reviewer | 검증 대상 |
| 블로그 발행 | blog → ai-slop-reviewer → (optional) nano-banana | 검증 대상 |
| 제품 랜딩 | copywriting → landing-page → ai-slop-reviewer | 검증 대상 |

##### 3-5. 회귀 통합

체인 내 어떤 스킬이 수정되면:
1. 해당 스킬을 포함하는 모든 체인 테스트 재실행
2. 단계 경계 출력 호환성 집중 검증
3. 출력 스키마 변경 시 다운스트림 스킬 동반 갱신

#### Mode 4: 루브릭 단독 (Standalone Scoring)

특정 스킬의 SKILL.md 본문만으로 4차원 스코어링을 수행합니다. A/B 비교 없이 절대 평가가 필요할 때 사용합니다.

### 스코어링 루브릭 (4차원 가중 평균)

> 모든 스킬(신규/수정)은 **출시 전 본 루브릭으로 스코어링되어야 합니다**.

#### 차원 정의

| 차원 | 가중치 | 핵심 질문 |
|------|--------|----------|
| Correctness (정확성) | 30% | 출력이 의도한 목적을 달성하는가? |
| Completeness (완전성) | 25% | 에지 케이스와 일반 변형을 다루는가? |
| Clarity (명확성) | 25% | 사용자가 이해하고 결과를 활용할 수 있는가? |
| Efficiency (효율성) | 20% | 출력 품질 대비 토큰 사용량이 적정한가? |

#### Correctness — 30%

| 점수 | 설명 |
|------|------|
| 1.0 | 명시된 목적을 사실 오류 없이 완전히 달성. 모든 스킬 내 예시가 정확한 결과 산출. |
| 0.75 | 목적 달성하나 형식·스타일에서 경미한 편차. 사실 오류 없음. |
| 0.50 | 목적 대부분 달성하나 1-2개 핵심 측면 누락 또는 경미한 부정확성. |
| 0.25 | 목적 일부만 다룸. 큰 격차 또는 오류 존재. |

#### Completeness — 25%

| 점수 | 설명 |
|------|------|
| 1.0 | 문서화된 모든 use case 처리. 에지 케이스 커버. 에러 경로 문서화. 적용 안 될 때 대체 스킬 명시. |
| 0.75 | 핵심 use case 처리. 대부분 에지 케이스 커버. 에러 처리 존재하나 불완전. |
| 0.50 | 주요 use case 동작. 에지 케이스 미커버. 에러 처리 최소. |
| 0.25 | happy path만 동작. 에지 케이스 처리 없음. 에러 시 silent failure. |

#### Clarity — 25%

| 점수 | 설명 |
|------|------|
| 1.0 | 재독 없이 실행 가능. 워크플로우 명확. 출력 형식 예측 가능. 예시가 복사·붙여넣기 사용 가능. |
| 0.75 | 1회 독해 후 이해. 1-2 단계에서 미세한 모호성. 예시는 유용하나 변형 필요. |
| 0.50 | 섹션 재독 필요. 일부 단계 해석 여지. 예시는 있으나 추상적. |
| 0.25 | 워크플로우 혼란. 단계 해석 여지 큼. 구체적 예시 없음. |

#### Efficiency — 20%

| 점수 | 설명 |
|------|------|
| 1.0 | 출력 품질 대비 토큰 사용 최적. 중복 지시 없음. 점진적 공개 잘 활용. 필요할 때만 로드. |
| 0.75 | 토큰 사용 합리적. 경미한 중복 가능. 점진적 공개 대체로 효과적. |
| 0.50 | 토큰 사용 필요 대비 높음. 일부 섹션 단축 가능. 점진적 공개 미활용. |
| 0.25 | 과도한 토큰 사용. 보일러플레이트 大. 점진적 공개 부재. |

#### 통과 기준

- **최저 통과**: 가중 평균 >= 0.70
- **단일 차원 floor**: 어떤 차원도 0.50 미만이면 hard fail
- **신규 스킬**: 첫 평가에서 >= 0.75 필요

#### 가중 점수 계산

```
score = (correctness * 0.30) + (completeness * 0.25) + (clarity * 0.25) + (efficiency * 0.20)
```

#### 평가 절차

1. **Self-evaluation**: 스킬 작성자가 본 루브릭으로 self-score
2. **Peer evaluation**: 두 번째 평가자가 독립 스코어링 (Complex tier 권장)
3. **Gap resolution**: 차원별 점수 차이 > 0.15 시 토론·해결
4. **Final score**: 모든 평가자 평균

#### 스킬 Tier 통합

| 스킬 Tier | 필요 점수 | 평가 |
|-----------|-----------|------|
| Simple (<50줄) | >= 0.70 | Self-evaluation |
| Standard (50-150줄) | >= 0.70 | Self + 권장 peer |
| Complex (150줄+) | >= 0.75 | Self + 필수 peer |

#### Anti-Pattern Checks (boundary-verification 통합)

통과 점수 확정 전 다음을 확인:

- [ ] 다른 스킬이 커버하는 기능과 중복하지 않음
- [ ] 폐기된 필드/패턴 참조 없음
- [ ] 설정 가능해야 할 값이 하드코딩되지 않음
- [ ] 예시 출력이 실제(real)이며 fabricated 아님
- [ ] 트리거가 명확한 우선순위 없이 다른 스킬과 중첩되지 않음

### Test Case Format

각 스킬의 `tests/test-cases.yaml` 파일 형식:

```yaml
skill: <skill-name>
version: 1.0.0
test_cases:
  - id: TC-001
    name: "happy-path"
    prompt: |
      <사용자 프롬프트>
    assertions:
      - type: contains
        value: "<출력에 포함되어야 할 문자열>"
      - type: not_contains
        value: "<출력에 포함되지 않아야 할 문자열>"
      - type: format
        value: "<markdown|json|text|html>"
    quality_threshold:
      correctness: 0.75
      completeness: 0.70
      clarity: 0.70
      efficiency: 0.60

  - id: TC-002
    name: "edge-case"
    prompt: |
      <경계 조건 프롬프트>
    assertions:
      - type: handles_gracefully
        value: true
```

### Score Report Format

테스트 완료 후 생성되는 리포트:

```markdown
## Skill Test Report: <skill-name>

### Summary
- Mode: A/B Test
- Date: YYYY-MM-DD
- Result: PASS / FAIL

### Scores

| Dimension | Baseline | With-Skill | Delta |
|-----------|----------|------------|-------|
| Correctness | 0.65 | 0.85 | +0.20 |
| Completeness | 0.60 | 0.80 | +0.20 |
| Clarity | 0.70 | 0.80 | +0.10 |
| Efficiency | 0.75 | 0.80 | +0.05 |
| **Weighted** | **0.67** | **0.81** | **+0.14** |

### Token Usage
- Baseline: XXXX tokens
- With-Skill: XXXX tokens
- Delta: -XX%

### Assertions
- TC-001: PASS (3/3 assertions)
- TC-002: PASS (2/2 assertions)

### Anti-Pattern Audit
- [x] 중복 없음
- [x] 하드코딩 없음
- [x] 모든 예시 real

### Recommendation
<APPROVE for release / NEEDS revision on [dimension]>
```

## 사용 예시

**예시 1: 신규 스킬 A/B 테스트**
> "skill-tester로 sales-playbook 스킬 A/B 테스트해줘"

**예시 2: 회귀 테스트**
> "blog 스킬 수정했는데 회귀 테스트해줘"

**예시 3: 체인 테스트**
> "blog → ai-slop-reviewer 체인 테스트 실행해줘"

**예시 4: 루브릭 단독 평가**
> "kr-gov-grant 스킬을 4차원 루브릭으로만 평가해줘"

## 출력 형식

| 산출물 | 형식 | 설명 |
|--------|------|------|
| Score Report | 마크다운 | 4차원 루브릭 스코어 + assertion 결과 + anti-pattern audit |
| Test Results | YAML | 테스트 케이스별 상세 결과 |

## 주의사항

- A/B 테스트는 동일 모델, 동일 조건에서 실행해야 합니다
- 토큰 사용량은 `/cost` 명령으로 확인합니다
- 자동화된 CI 통합은 추후 Phase 4에서 구현 예정입니다
- 테스트 프롬프트에 민감 정보(실제 고객명 등)를 포함하지 마세요
- 본 SKILL.md는 4차원 루브릭과 체인 프로토콜의 **single source**입니다. `.claude/rules/harness/quality/` 의 동명 파일은 redirect stub이며 본문은 여기를 참조합니다.

## 관련 스킬

| 스킬 | 관계 | 설명 |
|------|------|------|
| skill-builder | before | 스킬 생성 후 테스트 실행 |
| skill-template | before | 템플릿 기반 스킬 구조 정의 |
| ai-slop-reviewer | alternative | 텍스트 품질 검수 (비기능적) |

## 관련 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/harness` | new→test→review 자동 연쇄에서 본 스킬을 test 단계로 호출 |

---

Version: 1.5.x (rubric + chain-testing internalized)
Source: revfactory/harness skill-testing-guide + qa-agent-guide + Pipeline pattern (Apache 2.0) + MoAI adaptation
Last Updated: 2026-05-01