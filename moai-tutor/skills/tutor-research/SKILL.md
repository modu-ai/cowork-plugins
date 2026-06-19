---
name: tutor-research
description: |
  학습 질문을 받으면 공식 문서(context7)와 웹검색을 동시에 병렬로 조사해, 출처가 검증된 최신 학습 근거를 종합해 드립니다. 개인 튜터가 자료를 미리 조사해 오는 역할입니다.
  다음과 같은 요청 시 사용하세요:
  - "claude cowork의 Skills와 Sub-agents 차이를 최신 정보로 조사해줘"
  - "이 개념 정확한 최신 내용으로 알려줘"
  - "여러 자료 병렬로 조사해서 가르쳐줘"
  - "context7로 공식 문서랑 웹 최신 내용 같이 찾아줘"
  - "React 19 use훅 공식 문서 기준으로 설명 준비해줘"
  - "튜터처럼 이 주제 깊이 조사해줘"
  질문을 리서치 축으로 분해해 context7(라이브러리·SDK·CLI 공식 문서)과 WebSearch(최신 트렌드·튜토리얼·비교)를 병렬 실행하고, 출처를 교차검증한 뒤 learning-material로 넘길 종합본을 만듭니다.
  [책임 경계] vs moai-education:research-assistant: 이 스킬=개인 학습용 최신 정보 빠른 조사, 저 스킬=학술 논문용 문헌 검토와 인용 관리.
user-invocable: true
version: 2.27.0
---

# 튜터 리서치 (Tutor Research)

## 개요

학습 질문을 받아 **여러 경로를 병렬로 조사**해 신뢰할 수 있는 최신 학습 근거를 종합한다. 두 축을 동시에 가동한다: ① **context7 MCP** — 라이브러리·SDK·프레임워크·CLI의 버전별 공식 문서, ② **WebSearch** — 최신 변경사항·튜토리얼·개념 비교·실무 사례. 출처를 교차검증해 환각을 차단하고, `learning-material`이 바로 쓸 수 있는 구조화된 종합본을 만든다.

## 트리거 키워드

조사, 리서치, 최신 정보, 공식 문서, context7, 병렬 조사, 정확한 내용, 알려줘, 비교, 차이, 어떻게 동작

## 워크플로우

### 1단계: 질문 분석 → 리서치 축 도출

질문을 답하기 위한 하위 축으로 분해한다.

- **공식 문서 축(context7 대상)**: 특정 라이브러리·SDK·도구·API가 등장하는가? (예: React 19, Next.js, claude code CLI, FastAPI) → resolve-library-id 대상 추출
- **최신 정보 축(WebSearch 대상)**: 개념·트렌드·비교·"언제 무엇을 쓰나"·최근 변경 → 검색 쿼리 2-4개
- **코드베이스 축(선택, Explore)**: 사용자 프로젝트 내부 코드를 학습 대상에 포함하는 경우

### 2단계: 병렬 리서치 실행

[HARD] 독립적인 조사는 **한 턴에 병렬로** 실행한다(직렬 금지). 오케스트레이터는 다음을 동시에 호출한다.

- context7: `resolve-library-id` → `get-library-docs` (해당 라이브러리·토픽)
- WebSearch: 도출한 쿼리 2-4개
- (광범위 주제일 때) `Agent(Explore)` 또는 `Agent(general-purpose)` 리서처를 하위 축마다 **병렬 fan-out** — 각 에이전트가 한 축을 맡아 조사 결과를 반환

광범위·다면적 주제(소스 교차검증이 핵심)일 때는 번들된 `/deep-research <질문>` 워크플로우를 제안할 수 있다. 단, 토큰 비용이 단발 검색보다 크다는 점을 먼저 알린다.

```
[한 턴 안에서 병렬 호출]
  ├─ context7: get-library-docs(<라이브러리>, topic=<핵심 토픽>)
  ├─ WebSearch: "<주제> 2026 최신"
  ├─ WebSearch: "<개념 A> vs <개념 B> 차이 언제 사용"
  └─ (선택) Agent(Explore): 사용자 프로젝트 내 관련 코드 패턴
```

> **GLM 백엔드 주의**: `moai glm` 또는 `moai cg`의 GLM 페인에서는 WebSearch·WebFetch가 z.ai MCP 도구로 라우팅된다. `.claude/rules/moai/core/glm-web-tooling.md`의 라우팅 표를 따른다.

### 3단계: 교차검증 + 종합

- **출처 검증**: WebSearch 결과 URL은 WebFetch로 실재·내용을 확인한 것만 인용한다. 검색 결과에 없는 URL은 생성하지 않는다(반환각 정책).
- **상충 처리**: 공식 문서와 웹 자료가 다르면 **공식 문서(context7)를 우선**하고, 웹 자료는 보조·맥락으로 표기한다. 버전 차이로 인한 상충은 버전을 명시한다.
- **수준 맞춤**: learning-project의 학습자 수준에 맞춰 용어 난이도를 조정한다(입문이면 전제 개념부터).

### 4단계: 종합본 출력 (learning-material 입력 규격)

`learning-material`이 바로 소비할 수 있는 구조화된 Markdown을 만든다.

```markdown
## 리서치 종합: <주제>
- 학습자 수준: <입문/초급/중급/고급>

### 핵심 개념 (요약)
- 개념 1 — 한 줄 정의 + 근거 출처
- ...

### 도식 후보 (mermaid 소스 초안)
- 개념 관계도 / 플로우 / 시퀀스 중 적합한 것 1-2개 초안

### 예제·코드 (출처·버전 표기)
- 공식 문서 기준 최소 예제

### 자주 헷갈리는 점 / 비교
- A vs B, 언제 무엇을 쓰나

### 출처
- 공식 문서: <context7 라이브러리·버전>
- 웹: <검증된 URL 목록>
```

## 산출물

- 구조화된 리서치 종합본 (Markdown, 출처 포함)
- mermaid 도식 소스 초안 (learning-material로 전달)
- 검증된 출처 목록 (공식 문서 + 웹 URL)

## 사용 예시

**예시 1**: "claude code 서브에이전트 동작 방식 최신 정보로 조사해줘"
→ context7(claude code docs) + WebSearch(최신 변경) 병렬 → 종합본 + 시퀀스 도식 초안

**예시 2**: "React 19 use 훅, 공식 문서 기준으로 설명 준비해줘"
→ context7(React 19) 중심 + WebSearch(실무 예) → 예제·비교 종합

**예시 3**: "영어 가정법 과거완료, 정확한 규칙과 예문 조사해줘"
→ WebSearch(문법 규칙·예문) 병렬 → 규칙 표 + 예문 종합 (라이브러리 무관 → context7 생략)

## 주의사항

- **출처 없는 단정 금지**: 확인되지 않은 내용은 "확인 필요"로 표기한다.
- **WebSearch 사용 시 Sources 섹션 필수** — 검증된 URL만 마크다운 링크로 포함한다.
- **context7 불가 시 폴백**: MCP가 응답하지 않으면 WebFetch로 공식 문서 사이트를 직접 조회한다.
- **사용자에게 직접 질문하지 않는다**: 추가 정보가 필요하면 종합본에 "확인 필요" 항목으로 남기고, 결정은 오케스트레이터가 AskUserQuestion으로 처리한다.

## 관련 스킬

- **moai-tutor:learning-project**: 마일스톤 핵심 질문이 이 스킬의 입력이 된다
- **moai-tutor:learning-material**: 이 스킬의 종합본을 도식·HTML 학습자료로 변환

## 이 스킬을 사용하지 말아야 할 때

- **학술 논문용 문헌 검토·인용 관리** → `moai-education:research-assistant`
- **시장·비즈니스 조사** → `moai-business:market-analyst`
- **깊은 다중 소스 교차검증 리포트(단일 질문, 비학습)** → 번들 `/deep-research` 워크플로우
