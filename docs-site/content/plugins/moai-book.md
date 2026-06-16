---
title: "moai-book — 한국 출판사 제출용 원고 풀스택"
weight: 190
description: "도서 컨셉서·타깃 독자·목차·저자 약력·출판 제안서·출판사 매칭·본문 집필·퇴고까지 8 스킬. 실용서·인문·기술·소설 4 장르 자동 분기. KPIPA·국립국어원·도서정가제·30+ 한국 출판사 라이브러리 + 자비 출판 5 플랫폼 내장."
geekdocBreadcrumb: true
tags: ["moai-book"]
---

# moai-book

> 한 줄 자연어 한 마디로 컨셉서 → 페르소나 → 목차 → 저자 약력 → 출판 제안서 → 출판사 매칭 → 본문 집필 → 퇴고까지 8 단계 풀스택을 처리합니다. 실용서·인문·기술·소설 4 장르 자동 분기, 한빛·길벗·웅진·민음사·문학동네·창비·다산북스·휴머니스트 등 한국 주요 출판사 컨벤션 내장. 

```mermaid
flowchart TD
    A["1. concept-planner<br/>컨셉서·USP·포지셔닝"] --> B["2. target-reader<br/>페르소나·JTBD"]
    B --> C["3. outline-designer<br/>3 레벨 목차"]
    C --> D["4. author-bio<br/>저자 약력·저자의 말"]
    D --> E["5. proposal-writer<br/>출판 제안서 A4 12~20장"]
    E --> F["6. publisher-matcher<br/>30+ 출판사 Top 5"]
    F --> G["7. chapter-writer<br/>본문 챕터 집필"]
    G --> H["8. revision-coach<br/>퇴고 7 단계"]
    H --> I["moai-content:korean-spell-check<br/>→ humanize-korean<br/>→ moai-core:ai-slop-reviewer"]
    style A fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style G fill:#e6f0ef,stroke:#144a46,color:#09110f
    style I fill:#dceee9,stroke:#2a8a8c,color:#09110f
```

## 무엇을 하는 플러그인인가

`moai-book`은 한국 출판사 제출용 원고를 처음부터 끝까지 책임지는 풀스택 플러그인입니다. 도서 컨셉서·타깃 독자 페르소나·목차 설계·저자 약력·출판 제안서·출판사 매칭·본문 챕터·퇴고 — 8 단계가 단일 플러그인 안에서 체이닝됩니다.

### 이 플러그인으로 무엇을 할 수 있나

책 한 권을 완성하는 과정을 풀코스 요리로 생각하면 이해하기 쉽습니다. 8개 스킬은 요리의 처음부터 끝까지를 책임지는 주방의 보조 요리사들입니다. ①`book-concept-planner`는 "무슨 요리를 낼지" 메뉴를 기획하고, ②`book-target-reader`는 "누가 먹을지" 손님을 분석하고, ③`book-outline-designer`는 조리 순서인 레시피를 설계합니다. 이어서 ④`book-author-bio`가 셰프 소개를, ⑤`book-proposal-writer`가 식당 입점 제안서를, ⑥`book-publisher-matcher`가 어느 식당(출판사)에 입점할지 추천합니다. 그런 뒤 ⑦`book-chapter-writer`가 실제로 조리를 시작하고(원고지 분량만큼 글을 쓰고), ⑧`book-revision-coach`가 맛을 보며 플레이팅을 교정합니다.

핵심은 앞 단계의 산출물이 곧 다음 단계의 재료라는 점입니다. 메뉴를 정하지 않고 손님 분석만 하면 엉뚱한 요리가 나오듯, ①을 건너뛰고 ⑦부터 본문을 쓰면 방향을 잃은 원고가 됩니다. 그래서 8단계는 정해진 순서대로 한 단계씩 이어받아야 합니다. 마지막에는 `humanize-korean`과 `ai-slop-reviewer`가 붙어 "기계 냄새"를 빼는 마지막 손질을 합니다 — AI가 만든 요리 특유의 균일한 맛(뻔한 문장 길이, 과도한 접속사, 결론형 마무리 남발)을 사람 손맛으로 바로잡는 단계입니다.

```mermaid
flowchart LR
    S1["① 컨셉<br/>메뉴 기획"] --> S2["② 독자<br/>손님 분석"]
    S2 --> S3["③ 목차<br/>레시피 설계"]
    S3 --> S4["④ 약력<br/>셰프 소개"]
    S4 --> S5["⑤ 제안서<br/>입점 제안"]
    S5 --> S6["⑥ 매칭<br/>식당 선택"]
    S6 --> S7["⑦ 집필<br/>실제 조리"]
    S7 --> S8["⑧ 퇴고<br/>맛보기·교정"]
    S8 --> PP["후처리<br/>humanize-korean<br/>ai-slop-reviewer<br/>기계 냄새 제거"]

    style S1 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style S2 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style S3 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style S7 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style S8 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style PP fill:#dceee9,stroke:#2a8a8c,color:#09110f
```

실용서·인문·기술서·소설 **4 장르 자동 분기**가 모든 스킬에 내장되어 있어, 장르를 한 번만 지정하면 이후 단계는 그 장르의 한국 출판사 컨벤션(어미·시점·문체·인용 패턴·표기 규칙)을 자동으로 따릅니다.

한국출판문화산업진흥원(KPIPA) 국민독서실태조사, 국립국어원 한글 맞춤법·외래어 표기법, 도서정가제(신간 18개월 정가 + 최대 10% + 5% 적립), 교보문고·알라딘·예스24 베스트셀러 통합 차트가 데이터 소스로 통합되어 있습니다.

## 설치

{{< tabs "install-book" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-book` 옆의 **+** 버튼을 눌러 설치합니다.
2. 함께 권장: `moai-content` (정밀 윤문·맞춤법) — 퇴고 후처리 체인에 필수.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-book)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (8 단계 순서)

| 단계 | 스킬 | 용도 | 대표 출력 |
|---|---|---|---|
| 1 | `book-concept-planner` | 도서 컨셉서·USP 3축·시장 포지셔닝·자비 vs 투고 의사결정 | 한 줄(15자)/30자/300자 요약 + 포지셔닝 매트릭스 |
| 2 | `book-target-reader` | 타깃 독자 페르소나·JTBD 3 차원·페인포인트 매트릭스 | 4축 카드 + 페인 4 분면(긴급·핵심·잠재·희귀) + 5인 인터뷰 검증 |
| 3 | `book-outline-designer` | 부·장·꼭지 3 레벨 목차 + 5요소 챕터 시놉시스 | 200자 원고지 분량 배분 + 페르소나 여정 4단계 검증 |
| 4 | `book-author-bio` | 저자 약력·저자의 말·SNS 채널별 변형 | 3 신뢰 신호 + 3 길이(50·200·500자) + 저자의 말 500-800자 |
| 5 | `book-proposal-writer` | 출판사 투고 제안서 A4 12-20장 | 출판기획서 5섹션 + 샘플 챕터 + 마케팅 플랜 5 카테고리 |
| 6 | `book-publisher-matcher` | 30+ 한국 출판사 Top 5 우선순위 추천 | 4 차원 평가(장르 40%·규모 25%·계약 20%·채널 15%) + 차순위 시나리오 |
| 7 | `book-chapter-writer` | 챕터 본문 집필 — 꼭지 단위 5 요소 | 훅 10%·본문 70%·클라이맥스 10%·정리 5%·연결 5% + 200자 원고지 카운트 |
| 8 | `book-revision-coach` | 퇴고·교열 7 단계 점검 | 어법·문체·논리·인용·분량·시각자료·일관성 + 6 일관성 차원 |

## 4 장르 자동 분기

장르 자동 분기는 '같은 원고 내용이라도 장르별 스타일 템플릿을 찍어내 모양을 바꾸는' 기능입니다. 같은 반죽(원고 내용)에 실용서 템플릿을 찍으면 "번호 매김·체크리스트·짧은 단문" 모양으로 나오고, 소설 템플릿을 찍으면 "1·3인칭 시점·대사·장면 묘사" 모양으로 나옵니다. 장르를 한 번 고르면 그 템플릿이 8단계 전체에 일관되게 적용됩니다 — 매 단계마다 "이건 실용서니까 번호를 달아야지"를 다시 말해줄 필요가 없습니다.

아래 그림처럼 장르 하나가 선택되면 그 결정이 어미·시점·문체·인용 패턴·추천 출판사까지 한 번에 전파됩니다.

```mermaid
flowchart TD
    G{"장르 선택<br/>(1단계에서 1회)"}
    G -->|"실용서"| P1["번호 매김·체크리스트<br/>짧은 단문<br/>→ 웅진·다산북스·길벗"]
    G -->|"인문서"| P2["사색형 장문·고전 인용<br/>결론형 마무리<br/>→ 민음사·문학동네·창비"]
    G -->|"기술서"| P3["코드블록·도표·실습 단계<br/>정확한 용어<br/>→ 한빛·인사이트·제이펍"]
    G -->|"소설"| P4["1·3인칭 시점·대사·심리 묘사<br/>전개 곡선<br/>→ 민음사·문학동네·창비"]

    P1 --> ALL["8 단계 전체에 동일 템플릿 적용"]
    P2 --> ALL
    P3 --> ALL
    P4 --> ALL

    style G fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style P1 fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style P2 fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style P3 fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style P4 fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style ALL fill:#e6f0ef,stroke:#144a46,color:#09110f
```

| 장르 | 문체 프리셋 | 추천 출판사 |
|---|---|---|
| **실용서** | 명확한 단문·번호 매김·체크리스트·인용 ≥3종 | 웅진·다산북스·길벗·메가스터디북스 |
| **인문서** | 사색형 장문·인용·고전 참조·결론형 마무리 | 민음사·문학동네·창비·휴머니스트·은행나무·돌베개 |
| **기술서** | 코드블록·도표·정확한 용어·실습 단계 | 한빛미디어·인사이트·제이펍·길벗 IT |
| **소설** | 1·3인칭 시점·장면·대사·심리 묘사·전개 곡선 | 민음사·문학동네·창비·문학과지성사·자음과모음 |

## 한국 출판 컨텍스트 (2026 기준)

- **KPIPA**: 한국 출판 시장 데이터·국민독서실태조사·표준 양식
- **국립국어원**: 한글 맞춤법·외래어 표기법·우리말 우선 가이드
- **도서정가제**: 신간 18개월 정가 + 최대 10% 가격할인 + 5% 적립
- **베스트셀러 통합**: 교보문고·알라딘·예스24 3사 통합 권장
- **한국 출판사 30+**: IT(한빛·인사이트·제이펍·길벗 IT) · 실용(웅진·다산북스·길벗·메가스터디북스) · 인문(민음사·문학동네·창비·휴머니스트·은행나무·돌베개) · 문학(문학과지성사·자음과모음) · 아동(비룡소·사계절·창비 어린이)
- **신인 등단 경로**: 문학동네신인상·창비신인상·민음 신인 발굴 + 한국출판문화상·한국과학기술도서상
- **자비 출판 5 대안**: 부크크(POD)·텀블벅 출판 펀딩·인디고·카카오 브런치북·출판사 자비

## 대표 체인

출판에는 크게 두 길이 있습니다. 하나는 **투고**(출판사에 원고를 들고 가 심사받는 길)이고, 다른 하나는 **자비 출판**(내 돈으로 인쇄·유통을 감당하는 길)입니다. 식당에 비유하면, 투고는 유명 식당에 메뉴를 들고 가 입점 심사를 받는 것이고, 자비 출판(부크크·텀블벅)은 내 돈으로 포장마차를 차리는 것입니다. 식당은 "손맛이 나야 한다"는 깐깐한 기준을 적용하므로 기계적으로 찍어낸 듯한 원고는 바로 퇴짜를 맞고, 포장마차 직영은 심사는 느슨하지만 비용과 마케팅을 모두 내가 감당해야 합니다.

어느 길로 가든 원고의 마지막에는 반드시 `humanize-korean`과 `ai-slop-reviewer` 두 단계를 거쳐야 합니다. AI가 만든 글에는 기계 특유의 '티'가 남아 있습니다 — 문장 길이가 지나치게 균일하고, 접속사가 과도하고, 결론형 마무리가 반복되는 패턴입니다. 한국 출판 현실에서는 이런 기계적 어투가 잔존하면 출판사가 원고를 읽어보기도 전에 거절 사유로 삼습니다. 그래서 퇴고 다음에 사람 문장으로 윤문하는 단계와 최종 검수하는 단계가 필수로 붙습니다.

```mermaid
flowchart LR
    subgraph Path1["투고 풀스택 (출판사 심사)"]
        direction TB
        T1["8단계 원고"] --> T2["korean-spell-check"]
        T2 --> T3["humanize-korean<br/>AI 티 → 사람 문장"]
        T3 --> T4["ai-slop-reviewer<br/>최종 검수"]
        T4 --> T5["출판사 제출"]
    end

    subgraph Path2["자비 출판 (직영)"]
        direction TB
        J1["컨셉→목차→집필"] --> J2["revision-coach"]
        J2 --> J3["humanize-korean"]
        J3 --> J4["ai-slop-reviewer"]
        J4 --> J5["부크크·텀블벅"]
    end

    style T1 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style T3 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style T4 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style T5 fill:#dceee9,stroke:#2a8a8c,color:#09110f
    style J1 fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style J3 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style J4 fill:#e6f0ef,stroke:#144a46,color:#09110f
    style J5 fill:#dceee9,stroke:#2a8a8c,color:#09110f
```

두 길 모두 마지막 두 스킬(`humanize-korean` → `ai-slop-reviewer`)을 생략하면 '기계 냄새'가 남아 출판사 거절 또는 독자 이탈로 이어집니다.

**한국 출판사 투고 풀스택 (필수 후처리 포함)**

```text
book-concept-planner
  → book-target-reader
  → book-outline-designer
  → book-author-bio
  → book-proposal-writer
  → book-publisher-matcher
  → book-chapter-writer
  → book-revision-coach
  → moai-content:korean-spell-check
  → moai-content:humanize-korean       # AI 티 정밀 윤문 (필수)
  → moai-core:ai-slop-reviewer         # 최종 검수 (필수)
```

**자비 출판(부크크·텀블벅) 빠른 트랙**

```text
book-concept-planner
  → book-outline-designer
  → book-chapter-writer (반복)
  → book-revision-coach
  → moai-content:humanize-korean
  → moai-core:ai-slop-reviewer
```

**제안서만 작성(이미 본문 있음)**

```text
book-target-reader
  → book-author-bio
  → book-proposal-writer
  → book-publisher-matcher
```

## 사용 예시

{{< terminal title="claude — cowork" >}}
> AI 영어 회화 앱 운영 후기를 책으로 묶고 싶어. 30·40대 직장인 타깃.
{{< /terminal >}}

→ `book-concept-planner` 자동 호출 → AskUserQuestion(장르·자비/투고·분량) → 컨셉서·USP·포지셔닝 → `book-target-reader`로 이어짐.

{{< terminal title="claude — cowork" >}}
> 실용서 원고 다 썼는데 어느 출판사에 보내야 할지 모르겠어.
{{< /terminal >}}

→ `book-publisher-matcher` 자동 호출 → 장르·분량·저자 약력 입력 → 30+ 출판사 4차원 평가 → Top 5 + 차순위 시나리오.

## 주의·제한

- **이 플러그인은 한국 출판 시장에 특화**되어 있습니다. 해외 출판은 권장 출판사·도서정가제·KPIPA 통계 등 한국 컨텍스트가 적용되지 않으니 주의하세요.
- 8 스킬 모두 cowork-plugins frontmatter 정책 준수 (metadata 블록 0건, version 단일 필드).
- 외부 참고 자료 원문 비유·표현 직접 인용 0건 — 자체 재구성 후 한국 출판사 컨벤션으로 변환.
- 퇴고 단계에서 `moai-content:humanize-korean` + `moai-core:ai-slop-reviewer`는 **필수** — AI 티 잔존 시 출판사 거절 사유가 됩니다.
