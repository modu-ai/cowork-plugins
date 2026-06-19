---
name: spec-writer
description: |
  제품 기획 문서(PRD·기능 명세서)와 AI 도입 전략 보고서를 만들어 드립니다.
  다음과 같은 요청 시 사용하세요:
  - "PRD 작성해줘"
  - "기능 명세서 만들어줘"
  - "AI 도입 전략 보고서 써줘"
  - "제품 기능 우선순위 정리해줘"
  - "디지털 전환 로드맵 수립해줘"
  기획 의도와 요구사항을 검토 가능한 문서로 정리하고, ai-slop-reviewer·humanize-korean으로 마무리할 수 있습니다.
  [책임 경계] 정부·지원사업 신청서는 moai-business:kr-gov-grant, R&D·연구비 과제는 moai-research:grant-writer로 라우팅
user-invocable: true
version: 2.27.0
---

# 스펙 작성 (Spec Writer)

## 개요

제품 명세 및 전략 전문 스킬입니다. 프로덕트 매니저(PRD, 기능 명세, 우선순위 결정, 로드맵)와 AI 전략(AI/ML 도입 전략, 디지털 전환 로드맵)을 지원합니다.

> **지원사업·R&D 과제 신청서는 본 스킬 범위가 아닙니다.** 정부 일반 지원사업(창업·소상공인·중기 사업계획서·신청서)은 `moai-business:kr-gov-grant`, 학술/R&D·연구비 과제(NRF·IITP·KIAT)는 `moai-research:grant-writer`로 라우팅하세요.

## 트리거 키워드

PRD, 기능명세, 스펙, 제품 기획, AI 전략, 디지털전환, 프로덕트 매니저

## 워크플로우

### 전략 가이드 로드 및 실행

사용자 요청 수신 → 해당 전략 가이드 판별 → `references/{id}.md`(`product-manager` / `ai-strategy`) 로드 → 전략 가이드에 따라 실행 → 결과물 생성 후 사용자 검토 요청

복잡한 전략 판단 시 sequential-thinking MCP가 설치돼 있으면 `mcp__sequential-thinking__sequentialthinking`을 활용하고, 없으면 `ultrathink` 키워드 기반 심층 추론으로 대체합니다.

### 지원사업·R&D 과제 요청이 들어오면

정부 일반 지원사업(창업·소상공인·중기 사업계획서·신청서)은 `moai-business:kr-gov-grant`, 학술/R&D·연구비 과제(NRF·IITP·KIAT 양식)는 `moai-research:grant-writer`가 전담합니다. 본 스킬은 해당 요청을 두 스킬로 라우팅하고 신청서 작성 지침은 보유하지 않습니다.

## 사용 예시

- "신규 SaaS 서비스 PRD 작성해줘"
- "AI 기반 추천 시스템 도입 전략 보고서 써줘"
- "제품 기능 우선순위 정리해줘"
- "디지털 전환 로드맵 수립해줘"

## 출력 형식

- PRD (Product Requirements Document)
- 기능 명세서
- AI/ML 도입 전략 보고서
- 로드맵 및 마일스톤

## 주의사항

| 상황 | 해결 방법 |
|------|-----------|
| 이해관계자 요구사항 상충 | 우선순위 기준(비즈니스 임팩트 vs 개발 복잡도)으로 MoSCoW 분류를 도와드립니다 |
| 우선순위 기준 불명확 | RICE 스코어링 프레임워크로 기능 우선순위를 함께 설계합니다 |
| 기술 스펙 정의가 어려움 | 개발팀과의 협의 포인트를 비기능 요구사항 체크리스트로 제시합니다 |
| 지원사업·R&D 과제 신청서 요청 | `moai-business:kr-gov-grant`(정부 일반 지원사업) 또는 `moai-research:grant-writer`(R&D·연구비)로 라우팅합니다 |

## 2026 PRD 작성 트렌드

### AI 기반 PRD 작성 (2026 표준)

- **ChatPRD 활용**: 회의 메모·사용자 피드백 → 엔지니어 친화적 스펙 문서 자동 생성
- **AI 초안 생성**: Claude, GPT 등 LLM으로 PRD 초안 작성 후 PM이 검토·보완
- **프롬프트 설계**: "제품명, 사용자 문제, 해결 방안, 성공 지표"를 프롬프트에 포함

### PRD 필수 구성 요소 (한국 PM 표준)

| 항목 | 설명 |
|------|------|
| 배경 & 목적 | 왜 이 기능이 필요한가 (비즈니스 임팩트) |
| 사용자 스토리 | "사용자로서 나는 ~를 원한다. 왜냐면 ~" |
| 기능 요구사항 | 구체적인 기능 목록, 우선순위(Must/Should/Could) |
| 비기능 요구사항 | 성능, 보안, 접근성 기준 |
| UX 와이어프레임 | 레이아웃 초안 또는 참조 URL |
| 성공 지표(KPI) | 출시 후 측정할 지표 (DAU, 전환율, NPS 등) |
| 제외 범위 | 이번 출시에 포함하지 않는 것 |
| 일정 | MVP 출시일, 마일스톤 |

### 한국 PM 생태계

- **네카라쿠배**: 네이버·카카오·라인·쿠팡·배달의민족 PM 역량 기준 참조
- **애자일/스크럼**: 스프린트 단위 PRD 작성이 표준. 2주 스프린트 기준 기능 범위 정의
- **PM 커뮤니티**: 프로덕트 매니저 한국, PM 스터디 그룹, 링크드인 네트워크

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `moai-product:roadmap-manager` | 로드맵·마일스톤 관리 |
| `moai-product:ux-researcher` | UX 리서치 및 사용자 인터뷰 |
| `moai-legal:contract-review` | 법적 구속력 있는 계약·협약서 |

## 후처리 체인

PRD·AI 전략 보고서 같은 서술형 문서를 완성한 뒤에는 다음 체인으로 마무리합니다(표·수치 데이터는 제외, 본문 서술 부분에만 적용):

`moai-product:spec-writer → moai-core:ai-slop-reviewer → moai-content:humanize-korean`

- `moai-core:ai-slop-reviewer`: AI 특유의 상투적 표현·과장·군더더기를 점검하고 다듬습니다.
- `moai-content:humanize-korean`: 자연스러운 한국어 문장으로 최종 정제합니다.