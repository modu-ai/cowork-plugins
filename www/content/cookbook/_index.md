---
title: "쿡북 홈"
weight: 1
description: "Cowork와 moai 플러그인을 실제 업무에 엮는 쿡북 — 시나리오·체인·프롬프트를 한곳에서."
geekdocBreadcrumb: true
tags: [cookbook]
date: 2026-08-07T00:00:00+09:00
lastmod: 2026-08-07T00:00:00+09:00
---

# Cowork 쿡북

> Claude Cowork와 moai 플러그인을 **실제 업무에 어떻게 엮는지** 시나리오 묶음으로 정리한 쿡북입니다.

## 새로 나온 코워크 프로젝트

기능 하나를 소개하는 레시피를 넘어, 전문가 AI 직원 여러 명을 릴레이로 조합해 **실제 문제 하나를 끝까지 해결하는 여정**을 담은 프로젝트 모음이 추가되었습니다. 창업 타당성 검증, 스마트스토어 런칭, 계약서 리스크 보고, 이직 준비 4주 플랜까지 — 구체적인 인물의 문제 상황에서 출발해 어느 직원의 어느 스킬을 어떤 순서로 투입하는지 따라갑니다.

{{< icon arrow-right >}} **[코워크 프로젝트 (12개 프로젝트 레시피)](./projects/)** — 창업·운영 · 마케팅·콘텐츠 · 사무·문서 · 사람·커리어

## 사용 방식

**핵심 원칙**: 사용자가 짧은 한 줄 요청 → 시스템이 AskUserQuestion으로 맥락 수집 → 스킬 체이닝 자동 일괄 처리. 사용자가 매번 긴 옵션 프롬프트를 작성하지 않습니다.

## 한 줄이 산출물이 되기까지

고급 레스토랑에 앉은 것과 같습니다. 손님은 "오늘 해산물 코스로 부탁해"라는 한 줄만 말하면, 웨이터가 "알러지 있으세요? 매운 정도는?"처럼 필요한 질문만 골라 묻고, 그 답을 주방으로 넘깁니다. 주방은 재료 손질 → 조리 → 플레이팅을 차례로 진행해 완성된 요리를 내옵니다. 손님이 레시피를 외우거나 주방 순서를 직접 지시할 필요가 없습니다.

쿡북도 같은 구조로 돌아갑니다. **AskUserQuestion**이란 시스템이 사용자에게 맥락을 물어보는 구조화된 질문 상자입니다 — 선택지가 함께 나오는 작은 팝업이라고 생각하면 됩니다. **스킬 체이닝**이란 여러 전문 스킬을 순서대로 이어 파이프라인(한 방향으로 흘러가는 작업 연결선)을 만드는 방식입니다. 사용자는 "블로그 글 써줘"라는 한 줄만 던지면, 시스템이 독자·분량·말투를 AskUserQuestion으로 묻고, 그 답을 받아 내용 생성 → 검수 → 파일 변환이 차례로 이어지며 최종 산출물이 완성됩니다.

핵심은 사용자가 매번 긴 옵션 프롬프트를 외워 쓰지 않아도 된다는 점입니다. 시스템이 필요한 순간에 필요한 질문만 골라 묻기 때문에, 초보자도 전문가처럼 정교한 산출물을 얻을 수 있습니다.

```mermaid
flowchart TD
   U["사용자 한 줄 요청<br/>'해산물 코스로 부탁해'"] --> W{"AskUserQuestion<br/>맥락 수집"}
   W -- "알러지? 매운 정도?" --> K["주방 — 스킬 체인<br/>재료손질 → 조리 → 플레이팅"]
   K --> P["완성된 산출물<br/>(파일 · 문서)"]

   style U fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style W fill:#e6e6e6,stroke:#757575,color:#09110f
   style K fill:#e8f1ec,stroke:#265240,color:#09110f
   style P fill:#d6e7de,stroke:#3d7d5f,stroke-width:2px,color:#09110f
```

```mermaid
flowchart TD
   A["1. 한 줄 자연어 요청"] --> B["2. AskUserQuestion"] --> C["3. 스킬 체이닝"] --> D["4. 산출물"]
   style A fill:#fbf0dc,stroke:#c47b2a
   style C fill:#e8f1ec,stroke:#265240
```


## 어디서 시작하나요?

- **역할이 명확하면 → [실전 트랙](./tracks/)** — 11개 트랙 + 부록 (문서·콘텐츠·광고·이커머스·마케팅·HR·운영·법무·재무·데이터·프로덕트)
- **구체적 시나리오를 찾는다면 → 아래 쿡북 목록**
- **개념부터 익힌다면 → [스킬 체이닝 가이드](/cookbook/skill-chaining/)**

## 공통 포맷 (모든 쿡북 항목)

각 예제는 다음 구성으로 제공합니다.

- **사용자 입력** — 한 줄 자연어 요청 ({{< icon circle-check >}} 권장 패턴)
- **시스템 인터뷰** — AskUserQuestion이 묻는 항목
- **자동 체인** — 시스템이 호출하는 스킬 순서 (mermaid)
- **산출물** — 최종 결과물 미리보기
- **변형 시나리오** — 한 줄 요청 변경으로 다른 결과 얻기
- **자주 겪는 이슈** — 실패 케이스와 우회법

## 같은 틀로 읽는 법

요리책의 레시피 한 페이지를 상상하면 됩니다. 각 쿡북 예제는 동일한 6단 레시피 틀을 따릅니다. **사용자 입력**은 요리 주문(한 줄), **시스템 인터뷰**는 웨이터의 확인 질문, **자동 체인**은 조리 순서도, **산출물**은 완성 사진, **변형 시나리오**는 같은 레시피로 다른 맛 내는 팁, **자주 겪는 이슈**는 "소금 너무 많이 넣었을 때 대처법" 같은 실패 대응서입니다.

매 예제마다 이 틀이 고정되어 있어, 한 번 익숙해지면 어떤 예제든 같은 자리에서 같은 정보를 찾을 수 있습니다. 산출물을 확인하고 싶으면 항상 네 번째 단락을 보면 되고, 실패했을 때 대처법이 필요하면 항상 마지막 단락을 보면 됩니다.

```mermaid
flowchart TD
   R["레시피 한 페이지<br/>(모든 쿡북 예제 공통)"]
   R --> S1["① 사용자 입력<br/>요리 주문 (한 줄)"]
   R --> S2["② 시스템 인터뷰<br/>웨이터 확인 질문"]
   R --> S3["③ 자동 체인<br/>조리 순서도"]
   R --> S4["④ 산출물<br/>완성 사진"]
   R --> S5["⑤ 변형 시나리오<br/>다른 맛 내는 팁"]
   R --> S6["⑥ 자주 겪는 이슈<br/>실패 대응서"]

   style R fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style S1 fill:#e6e6e6,stroke:#757575,color:#09110f
   style S2 fill:#e6e6e6,stroke:#757575,color:#09110f
   style S3 fill:#e8f1ec,stroke:#265240,color:#09110f
   style S4 fill:#d6e7de,stroke:#3d7d5f,color:#09110f
   style S5 fill:#e6e6e6,stroke:#757575,color:#09110f
   style S6 fill:#e6e6e6,stroke:#757575,color:#09110f
```

## 먼저 읽으면 좋은 글

- [스킬 체이닝 가이드](/cookbook/skill-chaining/) — 쿡북 전반에서 공통으로 쓰는 체인 패턴 입문
- [플러그인 빠른 시작](../plugins/install/) — 마켓플레이스 등록부터 첫 호출까지

## 예제 목록

- [베스트 프랙티스](./best-practices/) — Cowork 핵심 기능·프롬프트 5원칙·실전 TOP 10
- [자동화 레시피](./automation-recipes/) — Schedule·Dispatch 본부별 자동화 레시피
- [블로그 파이프라인](/cookbook/blog-pipeline/) — 초안→검수→썸네일
- [주간 보고서 자동화](./report-automation/) — 상태 집계→XLSX→DOCX
- [마케팅 트랙](/cookbook/tracks/track-marketing/) — 브랜딩·SEO·캠페인 8주
- [문서 트랙](/cookbook/tracks/track-documents/) — Office 산출물 자동화 8주
- [데이터 트랙](/cookbook/tracks/track-data/) — 분석·공공데이터 8주
- [사업계획서 자동화](./business-plan/) — 전략→산업분석→PPT
- [IR 덱 제작](./ir-deck/) — 투자자 관점 슬라이드
- [계약서 검토 리포트](./contract-review/) — NDA 트리아지·리스크 점검
- [트러블슈팅](./troubleshooting/) — 체인 실패 진단·재시도

## 공통 원칙

- **텍스트 산출물은 무조건 `ai-slop-reviewer`로 마무리합니다.** 보고서·블로그·이메일·자소서·계약서 수정안이 모두 해당합니다.
- **숫자·차트·코드는 `ai-slop-reviewer`를 생략합니다.** 재무제표 엑셀, 차트 HTML, 스크립트는 검수 대상이 아닙니다.
- **포맷 변환은 `moai-officer`에 위임합니다.** 내용 생성 스킬은 초안만 만들고 `doc-docx` / `doc-xlsx` / `doc-pptx` / `doc-hwp`가 실제 파일을 만듭니다.
- **Windows 사용자는 파일명을 짧게 유지합니다.** MAX_PATH(260자) 제한 때문에 `보고서.docx`처럼 짧은 한글 이름을 권장합니다.

## 세 규칙이 지키는 것 — 맡은 일만 하게 하기

요리에 비유하면, 위 세 규칙은 모두 "맡은 일만 하게 하라"는 한 원칙에서 나옵니다.

첫째, 텍스트 산출물은 **ai-slop-reviewer**라는 맛보기 검수관을 반드시 거칩니다. AI가 쓴 글은 육수가 덜 우러난 듯한 기계적 어투가 남아 있어, 사람이 읽기 좋게 간을 다시 맞춰야 합니다. 보고서·블로그·이메일·자소서·계약서 수정안이 모두 이 단계를 거칩니다.

둋째, 숫자·차트·코드는 맛이 아니라 영양표 같은 것이라 검수할 어투가 없습니다. 재무제표나 차트에 "사람 냄새"를 넣을 필요가 없으므로 `ai-slop-reviewer`를 생략합니다.

셋째, 요리(내용 생성)와 플레이팅(포맷 변환)은 분업합니다. 내용 생성 스킬은 맛있는 요리 초안만 만들고, **moai-officer**의 `doc-docx` / `doc-xlsx` / `doc-pptx` / `doc-hwp`가 그릇에 담아 실제 파일로 완성합니다. 한 명이 요리와 플레이팅을 동시에 하면 둘 다 흐트러집니다.

```mermaid
flowchart TD
   REQ["자연어 요청"] --> DEC{"무엇을 만드나?"}

   DEC -- "글 · 텍스트" --> TXT["내용 생성 스킬<br/>(초안)"]
   TXT --> REV["ai-slop-reviewer<br/>맛보기 검수 (간 맞추기)"]
   REV --> FMT["moai-officer 포맷 변환<br/>(그릇에 담기)"]

   DEC -- "숫자 · 차트 · 코드" --> NUM["데이터 생성 스킬"]
   NUM --> FMT2["moai-officer 포맷 변환<br/>(검수 생략)"]

   FMT --> OUT["최종 산출물"]
   FMT2 --> OUT

   style REQ fill:#e6e6e6,stroke:#757575,color:#09110f
   style DEC fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style REV fill:#e8f1ec,stroke:#265240,color:#09110f
   style FMT fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style FMT2 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style OUT fill:#d6e7de,stroke:#3d7d5f,stroke-width:2px,color:#09110f
```

```mermaid
flowchart TD
   A["자연어 요청"] --> B{"스킬 라우터<br/>매칭"}
   B --> C["텍스트 생성<br/>스킬"]
   B --> D["포맷 변환<br/>moai-officer"]
   C --> E["ai-slop-reviewer<br/>후처리"]
   E --> D
   D --> F["최종 산출물"]

   style A fill:#e6e6e6,stroke:#757575,color:#09110f
   style F fill:#d6e7de,stroke:#3d7d5f,stroke-width:2px,color:#09110f
```

---

### Sources
- [modu-ai/moai-cowork](https://github.com/modu-ai/moai-cowork)
- [docs.claude.com — Cowork](https://docs.claude.com)
