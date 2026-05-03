---
title: "스킬 개발 가이드"
weight: 10
description: "새로운 MoAI 스킬을 개발하는 방법과 규격 상세 안내"
geekdocBreadcrumb: true
---

# 스킬 개발 가이드

이 가이드는 MoAI Cowork Plugins용 새로운 스킬을 개발하는 방법을 상세히 안내합니다. v1.3.0 기준의 최신 규격을 따라 고품질의 스킬을 만들 수 있습니다.

## SKILL.md frontmatter 규격

### 카테고리 A: 슬래시 호출 스킬 (Tab 자동완성 대상)

`/skill-name` 형태로 Tab 자동완성하고 싶은 모든 스킬:

```yaml
---
name: <skill-name>
description: |
  스킬의 목적과 트리거 조건을 자연스러운 서술로 풍부하게 작성.
  "다음과 같은 요청 시 반드시 이 스킬을 사용하세요:" 블록으로
  트리거 키워드/문장을 구체적으로 나열.
user-invocable: true
---
```

**예시**:
```yaml
---
name: investor-relations
description: |
  투자자 관계 문서를 생성하는 전문 스킬입니다.
  시장 분석, 재무 모델, 성장 전략을 포함한 IR 자료를 작성합니다.
  
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "투자자 데크 만들어줘"
  - "IR 자료 작성해줘"
  - "시리즈 A 투유치 자료 준비해줘"
  - "투자자 브리핑 만들어줘"
user-invocable: true
---
```

### 카테고리 B: 모델 자동 호출 스킬 (체인 내부 호출만)

Tab 자동완성 불필요하고 모델이 문맥으로 자동 호출하는 스킬:

```yaml
---
name: <skill-name>
description: |
  서술형 설명 + 트리거 키워드.
---
```

**예시**:
```yaml
---
name: ai-slop-reviewer
description: |
  AI 생성 텍스트의 품질을 검수하고 개선하는 스킬입니다.
  전문적인 비즈니스 문서에 적합하도록 표현을 다듬습니다.
  
  트리키워드: AI 슬롭 검수, 품질 검수, 텍스트 개선
---
```

### [HARD] 금지 필드

다음 필드들은 **절대 사용할 수 없습니다**:

- `metadata:` 블록 전체 (version, status, updated, tags 포함)
- `keywords:` (비표준, 사용 금지)
- 본문 상단의 `> vX.Y.Z | ...` 식 버전 배너 라인

### Plugin 매니페스트

스킬이 포함된 플러그인의 `plugin.json`은 다음 필수 필드를 포함해야 합니다:

```json
{
  "name": "plugin-name",
  "version": "1.5.1",
  "description": "...",
  "author": { "name": "..." },
  "keywords": ["..."],
  "license": "MIT"
}
```

## 스킬 파일 구조

### 표준 구조

```
moai-*/skills/skill-name/
├── SKILL.md                   # 메인 스킬 파일 (500라인 이하)
├── modules/                   # 심화 모듈
│   ├── patterns.md           # 사용 패턴
│   └── examples.md           # 예시 코드
├── examples.md                # 복사-붙여넣기 준비된 코드
└── reference.md               # 참고 자료
```

### 파일 크기 제한

- **SKILL.md**: 500라인 이하 (필수)
- **modules/**: 무제한 확장 가능
- **examples.md**: 복사-붙여넣기 준비된 코드
- **reference.md**: 외부 참고 자료

## 스킬 본문 구조

### 1. 역할 정의 (Role Definition)

스킬의 핵심 역할과 책임을 명확히 정의합니다:

```markdown
## 역할

이 스킬은 [특정 도메인]의 [특정 작업]을 수행하는 전문가입니다. 
[주요 책임]과 [핵심 능력]을 바탕으로 [목표]를 달성합니다.

### 전문성

- 도메인 1: [설명]
- 도메인 2: [설명]  
- 도메인 3: [설명]
```

### 2. 워크플로우 단계 (Workflow Steps)

작업을 수행하는 구체적인 단계를 설명합니다:

```markdown
## 워크플로우

### 1단계: [단계 이름]
- 입력: [필요한 정보]
- 처리: [수행할 작업]
- 출력: [생성될 결과]

### 2단계: [단계 이름]
- 입력: [이전 단계의 출력]
- 처리: [수행할 작업]
- 출력: [생성될 결과]
```

### 3. 입력/출력 정의 (Input/Output)

스킬의 입출력 형식과 구조를 명시합니다:

```markdown
## 입력/출력

### 입력
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| title | string | O | 문서 제목 |
| content | string | O | 주요 내용 |
| style | string | X | 작성 스타일 |

### 출력
| 필드 | 타입 | 설명 |
|------|------|------|
| document | string | 생성된 문서 |
| metadata | object | 메타데이터 정보 |
```

### 4. 사용 예시 (Examples)

실제 사용 예시를 구체적으로 제공합니다:

```markdown
## 사용 예시

### 기본 사용
```text
> "투자자용 IR 덱 만들어줘"
→ 스킬 실행 → IR 덱 생성 완료
```

### 상세한 사용
```text
> "우리 SaaS의 Series A용 IR 덱 작성해줘.
타깃 고객은 한국 중소제조업체야.
주요 경쟁사는 A, B, C 회사야.
```
→ 시장 분석, 재무 모델, 성장 전략 포함한 IR 덱 생성
```
```

### 5. 고급 패턴 (Advanced Patterns)

심화 사용자를 위한 고급 사용법:

```markdown
## 고급 패턴

### 체인 사용
다른 스킬과 조합하여 사용할 수 있습니다:

```
> "사업계획서 작성해줘"
→ strategy-planner → pptx-designer → ai-slop-reviewer
```

### 커스터마이징
환경 변수를 설정하여 기능을 확장할 수 있습니다:

```bash
export STRATEGY_API_KEY="your-api-key"
export TEMPLATE_STYLE="modern"
```
```

## 스킬 개발 절차

### 1. 아이디어 구상

- 해결할 문제 정의
- 목표 사용자 파악
- 핵심 기능 결정
- 차별화 요소 확인

### 2. 프론트매터 작성

```yaml
---
name: skill-name
description: |
  스킬의 목적과 트리거 조건을 자연스러운 서술로 작성.
  "다음과 같은 요청 시 반드시 이 스킬을 사용하세요:" 블록으로
  트리거 키워드/문장을 구체적으로 나열.
user-invocable: true
---
```

### 3. 본문 작성

- 역할 정의 작성
- 워크플로우 설계
- 입력/출력 정의
- 사용 예시 개발
- 고급 패턴 추가

### 4. 모듈 분리

500라인을 초과하는 경우 모듈로 분리:

```markdown
# modules/patterns.md

## 고급 사용 패턴

### 패턴 1: [패턴 이름]
- 설명: [패턴 설명]
- 예시: [사용 예시]
```

### 5. 테스트 작성

```bash
# 기능 테스트
go test ./moai-*/skills/skill-name/...

# 예시 테스트
go test -run Example ./moai-*/skills/skill-name/...
```

### 6. 문서화

- `examples.md`에 복사-붙여넣기 준비된 코드 추가
- `reference.md`에 참고 자료 링크 추가
- README.md에 스킬 소개 추가

## 품질 검증

### 스킬 품질 체크리스트

- [ ] frontmatter 규격 준수
- [ ] 트리거 키워드 포함
- [ ] 역할 정명확하게 정의
- [ ] 워크플로우 단계별 설명
- [ ] 입력/출력 명확히 정의
- [ ] 실제 사용 예시 포함
- [ ] 500라인 이하 (SKILL.md)
- [ ] 오류 처리 구현
- [ ] 테스트 케이스 작성
- [ ] 모든 문장 한국어 작성

### 자동 검증 스크립트

```bash
# 스킬 유효성 검사
./scripts/skill-lint.sh moai-business/skills/investor-relations

# 모든 스�일 일괄 검사
find moai-*/skills/ -name "SKILL.md" -exec ./scripts/skill-lint.sh {} \;
```

## 스킬 테스팅

### 단위 테스트

```go
// skills/investor-relations/test.go
package main

import "testing"

func TestIRDeckGeneration(t *testing.T) {
    input := map[string]interface{}{
        "title": "Series A IR Deck",
        "content": "SaaS platform for Korean SMEs",
    }
    
    expected := "IR Deck"
    result, err := generateIRDeck(input)
    
    if err != nil {
        t.Errorf("Error generating IR deck: %v", err)
    }
    
    if result.Title != expected {
        t.Errorf("Expected %s, got %s", expected, result.Title)
    }
}
```

### 통합 테스트

```bash
# 체인 테스트
moai-test run chain:investor-relations-pptx-review

# 성능 테스트
moai-test run performance:investor-relations
```

## 배포 절차

### 1. 플러그인 매니페스트 업데이트

```json
{
  "name": "moai-business",
  "version": "1.5.1",
  "description": "비즈니스 전문 스킬 플러그인",
  "skills": ["investor-relations", "market-analyst", ...]
}
```

### 2. 버전 동기화

```bash
# 버전 업데이트 (18개 지점)
NEW="1.5.1"
sed -i '' -E 's/"version": *"[0-9]+\.[0-9]+\.[0-9]+"/"version": "'$NEW'"/' .claude-plugin/marketplace.json
find . -path "*/.claude-plugin/plugin.json" -exec sed -i '' -E 's/"version": *"[0-9]+\.[0-9]+\.[0-9]+"/"version": "'$NEW'"/' {} +
```

### 3. CHANGELOG 업데이트

```markdown
## [1.5.1] - 2026-05-01

### Added
- investor-relations: 투자자 관계 문서 생성 스킬
- market-analyst: 시장 분석 보고서 작성 스킬

### Changed
- 기존 스킬 성능 개선
- 사용자 인터페이스 개선
```

### 4. 테스트 실행

```bash
# 전체 테스트
./scripts/skill-test-runner.sh

# 릴리스 전 검증
moai:review
```

## 관련 스킬

### 기존 스킬 참조

유사한 기능을 가진 기존 스킬을 참고하여 개선점을 파악하세요:

- [strategy-planner](../plugins/moai-business/strategy-planner/): 전략 계획 수립
- [pptx-designer](../plugins/moai-office/pptx-designer/): 프레젠테이션 디자인
- [ai-slop-reviewer](../plugins/moai-core/ai-slop-reviewer/): AI 텍스트 검수

### 스킬 체인 예시

새로운 스킬이 어떻게 체인에서 사용될 수 있는지 예시를 제공하세요:

```markdown
## 체인 사용 예시

### 사업계획서 체인
```
strategy-planner → investor-relations → pptx-designer → ai-slop-reviewer
```

### 블로그 체인
```
blog → ai-slop-reviewer → (선택) nano-banana
```
```

## 자주 묻는 질문

### Q: 스킬 이름을 어떻게 정해야 하나요?

A: 명확하고 직관적인 이름을 사용하세요. 동사 형태로 (예: `investor-relations`, `market-analyst`)

### Q: user-invocable을 어떻게 설정하나요?

A: 사용자가 직접 호출할 스킬은 `true`, 내부적으로만 사용할 스킬은 생략하세요.

### Q: 예시 코드는 몇 개를 포함해야 하나요?

A: 최소 2개 이상의 실제 사용 예시를 포함하세요. 기본 사용과 상세한 사용을 모두 포함하는 것이 좋습니다.

### Q: 모듈은 언제 분리하나요?

A: SKILL.md가 500라인을 초과할 때 modules/ 디렉토리로 분리하세요.

### Sources
- GitHub 저장소: [https://github.com/modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- 스킬 테스트 도구: [https://github.com/modu-ai/cowork-plugins/tree/main/moai-core/skills/skill-tester](https://github.com/modu-ai/cowork-plugins/tree/main/moai-core/skills/skill-tester)
- 품질 가이드: [https://github.com/modu-ai/cowork-plugins/tree/main/.claude/rules/harness/quality/skill-scoring-rubric.md](https://github.com/modu-ai/cowork-plugins/tree/main/.claude/rules/harness/quality/skill-scoring-rubric.md)