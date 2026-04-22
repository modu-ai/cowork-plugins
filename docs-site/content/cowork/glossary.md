---
title: "용어집"
weight: 35
description: "스킬·플러그인·체인·커넥터·MCP·서브에이전트 등 Cowork 핵심 용어 6종을 정리합니다."
geekdocBreadcrumb: true
---

# 용어집

> Cowork를 처음 쓸 때 가장 자주 혼동되는 6개 용어를 한 자리에 모았습니다.

{{< hint type="warning" >}}
v0.2 스켈레톤: 각 항목은 한두 줄 정의와 오개념 한 줄로 시작해 이후 예시·링크를 보강합니다.
{{< /hint >}}

## 학습 목표

- 스킬(skill)과 플러그인(plugin)의 관계를 한 문장으로 설명할 수 있습니다.
- 스킬 체인(chain)과 서브에이전트(subagent)의 차이를 구분할 수 있습니다.
- 커넥터(connector)와 MCP(Model Context Protocol)가 같은 개념인지 판별할 수 있습니다.

## 선수 지식

- [Cowork 소개](../intro/) — 가장 먼저 읽어야 할 페이지

## 핵심 용어 6종

### 스킬 (skill)

"이런 상황에서는 이렇게 해라"라는 절차적 지침 묶음입니다. 디렉터리 하나(`SKILL.md` + references)가 기본 단위입니다.

**오개념**: 스킬은 "기능"이 아닙니다. 기능을 수행하는 방법을 담은 지침서입니다.

### 플러그인 (plugin)

여러 스킬·커넥터·서브에이전트를 한 도메인으로 묶어 배포하는 단위입니다. `plugin.json` + `skills/*` + `.mcp.json`으로 구성됩니다.

**오개념**: 플러그인과 스킬은 1:1이 아닙니다. 플러그인 하나에 스킬이 1~10개 들어갑니다.

### 스킬 체인 (skill chain)

여러 스킬을 순서대로 엮어 한 요청을 처리하는 파이프라인입니다. 예: `strategy-planner → docx-generator → ai-slop-reviewer`.

**오개념**: 체인은 시스템이 자동으로 엮는 것이 아니라, 사용자 요청 문맥에 맞춰 Claude가 판단해 구성합니다.

### 커넥터 (connector)

Slack·Gmail·Notion 등 외부 서비스에 접근하는 인증·API 래퍼입니다. Cowork에서는 MCP로 구현됩니다.

### MCP (Model Context Protocol)

Anthropic이 정의한 커넥터 표준 프로토콜입니다. 커넥터는 구체적 구현, MCP는 규격이라고 보면 됩니다.

### 서브에이전트 (subagent)

긴 작업을 나눠 수행하기 위해 메인 세션이 별도 컨텍스트로 위임하는 하위 Claude 인스턴스입니다.

**오개념**: 서브에이전트는 스킬이 아닙니다. 스킬은 지침, 서브에이전트는 지침을 실행하는 주체입니다.

## 자가 점검

{{< hint type="note" >}}
- Q1. 스킬과 플러그인의 관계를 한 문장으로 설명하세요. (쉬움·이해)
- Q2. 체인 실행 중 `docx-generator`가 호출되지 않았다면 원인 후보 3가지는? (중간·적용)
- Q3. MCP와 커넥터는 같은 개념일까요, 아니면 다를까요? 근거와 함께 답하세요. (어려움·분석)
{{< /hint >}}

<details>
<summary>정답 보기</summary>

- A1. 플러그인은 여러 스킬을 한 도메인으로 묶어 배포하는 단위입니다.
- A2. (1) 요청에 트리거 키워드 부재 (2) 플러그인 미설치 (3) 상위 도메인 스킬에서 포맷 단계로 넘기지 못함
- A3. MCP는 프로토콜 규격이고, 커넥터는 그 규격을 따르는 구체 구현입니다. 동의어가 아닙니다.

</details>

## 다음 단계

- [스킬 사용법](../skills/) — 스킬 호출 방식과 자동 트리거 조건
- [플러그인 사용](../plugins/) — 플러그인 설치·업데이트 흐름
- [스킬 체이닝 가이드](../../cookbook/skill-chaining/) — 체인 설계 3원칙

---

### Sources

- [Claude Cowork 제품 페이지](https://claude.com/product/cowork)
- [Anthropic MCP 소개](https://www.anthropic.com/news/model-context-protocol)
- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
