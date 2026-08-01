---
title: "Claude 알아보기"
weight: 10
description: "Claude가 무엇이고 어디서·어떻게 쓸 수 있는지 — 접근 방법, 인터페이스, 학습 데이터까지 한눈에 살펴봅니다."
geekdocBreadcrumb: true
---

Claude는 Anthropic이 만든 AI 어시스턴트입니다. 검색창에 키워드를 넣고 결과 목록을 뒤지는 것과 달리, Claude에게는 평소 사람에게 말하듯 부탁하면 됩니다. "이 보고서를 세 줄로 요약해 줘", "친구에게 보낼 안부 메시지 초안을 써 줘", "이 사진 속 그래프가 무슨 뜻이야?" — 이렇게 자연스럽게 물어보면 Claude가 곧바로 답하고 마음에 안 드는 부분은 그 자리에서 다시 고쳐 줍니다.

이 글에서는 Claude를 어디서 만날 수 있는지, 어떤 일을 시킬 수 있는지, 그리고 알아 두면 좋은 몇 가지 특성을 정리했습니다. 처음 Claude를 써 보는 분이라면 이 페이지부터 천천히 읽어 보세요.

## Claude로 무엇을 할 수 있나요

Claude는 한 가지만 잘하는 도구가 아니라, 글·학습·코드·번역·이미지까지 폭넓게 도와주는 다재다능한 조수에 가깝습니다. 대표적인 활용 분야는 다음과 같습니다.

| 분야 | 할 수 있는 일 | 예시 |
|---|---|---|
| **글쓰기·창작** | 문자, 이메일, 시나리오, 소설 등 다양한 글의 초안 작성 | "정중하면서도 친근한 사과 이메일을 써 줘" |
| **학습·교육** | 요리, 프로그래밍 개념, 역사 등 여러 주제를 쉽게 설명 | "초보자에게 변수가 뭔지 설명해 줘" |
| **요약** | 기사, 뉴스, 문서, 대화, 책의 핵심 정리 | "이 긴 문서를 한 문단으로 요약해 줘" |
| **코딩 도움** | 옆자리 짝꿍 프로그래머처럼 코드 작성·수정 지원 | "CSV에서 특정 열만 뽑는 코드를 보여 줘" |
| **브레인스토밍·분석** | 다양한 관점 제시와 추천 | "이 아이디어의 장단점을 정리해 줘" |
| **번역** | 여러 언어 간 번역 | "이 문단을 자연스러운 한국어로 번역해 줘" |
| **이미지 해석** | 차트 분석, 사진 내용 설명 | "이 그래프에서 무엇을 읽을 수 있어?" |

코딩의 경우 Python을 가장 능숙하게 다루며 주요 프로그래밍 언어 대부분을 지원합니다. 번역은 포르투갈어, 프랑스어, 독일어에서 특히 강합니다.

{{< hint type="note" >}}
Claude는 학습 데이터 구성상 영어에서 가장 높은 성능을 보입니다. 한국어를 포함한 다른 언어도 충분히 잘 다루지만 매우 까다로운 작업에서는 영어로 시켰을 때와 약간 차이가 날 수 있습니다.
{{< /hint >}}

## 어디서 Claude를 쓸 수 있나요

Claude는 하나의 화면에만 묶여 있지 않습니다. 웹, 데스크톱 앱, 모바일 앱 등 상황에 맞는 방식으로 접속할 수 있습니다. 공식 인터페이스는 다음 다섯 가지입니다.

| 인터페이스 | 설명 | 접속처 |
|---|---|---|
| **Claude Chat (웹)** | 브라우저에서 바로 사용 | claude.ai |
| **Claude for iOS** | 애플 기기용 네이티브 앱 | App Store |
| **Claude for Android** | 안드로이드용 네이티브 앱 | Google Play |
| **Claude Desktop** | Mac·Windows용 데스크톱 앱 | claude.ai/download |
| **Claude Console·API** | 개발자를 위한 프로그래밍 방식 접속 | platform.claude.com |

앞의 네 가지는 일반 사용자를 위한 대화·앱 인터페이스이고 마지막 Console·API는 개발자가 프로그램에서 Claude를 호출하기 위한 통로입니다. 개발자용 API·Console에 대한 자세한 내용은 [platform.claude.com](https://platform.claude.com)에서 확인할 수 있습니다.

### 사용 조건

Claude를 쓰려면 두 가지 기본 조건을 만족해야 합니다.

- **연령**: 만 18세 이상
- **지역**: 지원되는 국가·지역에 위치 (2026년 3월 16일 기준 전 세계 약 195개 이상의 국가·지역에서 이용 가능)

## 처음 시작하는 방법

Claude와 친해지는 가장 빠른 길은 직접 말을 걸어 보는 것입니다. 다음 순서로 가볍게 시작해 보세요.

1. **간단한 질문부터** 시작합니다. 거창한 요청 대신 평소 궁금했던 것을 그대로 물어보세요.
2. **구체적으로** 부탁합니다. 원하는 톤, 길이, 형식을 함께 알려 주면 결과가 훨씬 좋아집니다.
3. **답변을 보고 다듬습니다.** "더 짧게", "좀 더 친근하게"처럼 그 자리에서 수정 요청을 이어 갈 수 있습니다.
4. **다양한 작업을 시도**하며 Claude가 어디까지 도와줄 수 있는지 직접 확인합니다.

화면에는 현재 사용 중인 모델이 표시되며 다른 모델로 바꿀 수도 있습니다. 입력창의 **+** 나 **/** 단축 메뉴로 추가 명령을 쓸 수 있고 답변의 깊이를 조절하는 노력 수준(effort)이나 확장 사고(extended thinking) 같은 옵션도 사용할 수 있습니다.

{{< hint type="tip" >}}
처음에는 결과가 기대와 다를 수 있습니다. Claude는 대화 문맥을 기억하므로 마음에 들 때까지 같은 채팅 안에서 계속 고쳐 달라고 부탁하는 것이 가장 좋은 사용법입니다.
{{< /hint >}}

## 요금제와 사용량

Claude는 무료로도 쓸 수 있고 더 많이 쓰고 싶다면 유료 구독으로 사용량을 늘릴 수 있습니다.

| 구분 | 내용 |
|---|---|
| **무료 플랜** | 세션 기반 사용량 제한이 있으며, 약 5시간마다 초기화됩니다. 사용할 수 있는 메시지 수는 그때그때 서비스 수요에 따라 달라집니다. |
| **유료 플랜** | 구독을 통해 더 많은 사용량을 확보할 수 있습니다. |

요금제와 사용량 한도에 대한 자세한 내용은 [요금제와 결제](/help/plans-billing/), [사용량 제한](/help/usage-limits/) 페이지에서 확인할 수 있습니다.

## 알아 두면 좋은 점

### 학습 데이터 기준 시점

Claude 모델은 각각 정해진 시점까지의 정보로 학습되어 있습니다. 그 시점 이후에 일어난 사건은 정확히 알지 못할 수 있습니다. 최신 뉴스나 사건을 물어볼 때는 이 점을 염두에 두세요.

| 모델 | 학습 데이터 기준 시점 |
|---|---|
| Claude Opus 4.8 / Opus 4.7 | 2026년 1월 |
| Claude Fable 5 | 2026년 1월 |
| Claude Sonnet 4.6 / Opus 4.6 | 2025년 8월 |
| Claude Haiku 4.5 | 2025년 7월 |
| Claude Opus 3 | 2023년 8월 |

### 대화 기록 가져오기

현재 다른 AI 서비스에서 만든 **대화 기록을 그대로 옮겨 오는 기능은 지원되지 않습니다**. (단, 경쟁 서비스의 메모리(기억) 가져오기는 지원됩니다.)

### 베타·리서치 프리뷰 기능

Anthropic은 정식 출시 전 단계의 기능을 미리 제공하기도 합니다. 두 종류로 나뉩니다.

- **리서치 프리뷰(Research Preview)**: 초기 단계 기능으로, 정식 출시 전에 크게 바뀌거나 중단될 수 있습니다.
- **베타(Beta)**: 일상적으로 쓸 만큼 안정적이지만 여전히 다듬어지는 중인 기능입니다.

Claude for Word(Word 플러그인), Claude in Chrome(브라우저 확장), GitHub 연동 등이 이러한 기능에 포함됩니다.

{{< hint type="warning" >}}
베타·리서치 프리뷰 기능은 경험·성능·안정성이 바뀔 수 있고 일부는 끝내 중단될 수 있습니다. 또한 사용할 수 있는 기능은 요금제마다 다르므로 쓰기 전에 내 플랜에서 지원되는지 확인하세요.
{{< /hint >}}

## 다음 단계

- **[첫 대화 시작하기](/guide/chat/first-chat/)** — Claude를 열고 처음 말을 거는 단계별 가이드
- **[Claude Chat 둘러보기](/guide/chat/)** — 대화형 AI로 할 수 있는 일 한눈에 보기
- **[요금제와 결제](/help/plans-billing/)** — 무료·유료 플랜 비교와 결제 안내

## 원문 출처

- [Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude)
- [What are some things I can use Claude for?](https://support.claude.com/en/articles/7996845-what-are-some-things-i-can-use-claude-for)
- [Where can I access Claude?](https://support.claude.com/en/articles/8461763-where-can-i-access-claude)
- [What interfaces can I use to access Claude?](https://support.claude.com/en/articles/8114487-what-interfaces-can-i-use-to-access-claude)
- [How up-to-date is Claude's training data?](https://support.claude.com/en/articles/8114494-how-up-to-date-is-claude-s-training-data)
- [Available beta and research preview features](https://support.claude.com/en/articles/14503520-available-beta-and-research-preview-features)
