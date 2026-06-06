---
title: "SNS 최적화 가이드"
weight: 70
description: "인스타·LinkedIn·X·카카오·네이버 등 채널별 톤·해시태그·발행 시점을 moai-content:social-media와 moai-marketing:sns-content로 운영."
geekdocBreadcrumb: true
---
> 채널마다 사람이 다르고, 사람이 다르면 톤·길이·해시태그도 달라야 합니다. cowork-plugins의 SNS 스킬은 7개 채널의 알고리즘·관습을 미리 알고 있어 동일 메시지를 채널별로 자동 변형합니다.

```mermaid
flowchart TD
    A["sns-content<br/>콘텐츠 달력"] --> B["social-media<br/>채널별 변형"]
    B --> C{"포맷"}
    C -- "카드뉴스" --> D["card-news"]
    C -- "텍스트" --> E["ai-slop-reviewer"]
    A -. "브랜드 가이드" .-> F["brand-identity"]

    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style E fill:#e6f0ef,stroke:#144a46,color:#09110f
```

## 사용 스킬

| 스킬 | 커버 채널 |
|---|---|
| `moai-content:social-media` | 인스타·스레드·X·LinkedIn·유튜브 쇼츠·카카오·네이버 7개 |
| `moai-content:card-news` | 인스타 카드뉴스·캐러셀 |
| `moai-marketing:sns-content` | 콘텐츠 달력·브랜드 보이스 가이드 |
| `moai-marketing:brand-identity` | 톤앤매너·비주얼 가이드라인 |

## 채널별 권장 패턴

| 채널 | 톤 | 길이 | 해시태그 | 최적 시간(KST) |
|---|---|---|---|---|
| 인스타 | 감성·시각 | 짧음 | 5-10개 | 19-21시 |
| LinkedIn | 전문·인사이트 | 중간(3-5문단) | 3-5개 | 평일 8-10시 |
| X (구 트위터) | 짧고 즉답 | 280자 + 스레드 | 1-2개 | 출근 시간 + 점심 |
| 카카오 채널 | 친근·정보 | 중간 | 0-1개 | 평일 12-13시 |
| 네이버 블로그 | SEO 친화 | 길게(2000자+) | 키워드 자연 삽입 | 오전 |
| 스레드(Threads) | 인스타 + X 사이 | 짧음 | 적게 | 인스타와 동일 |
| 유튜브 쇼츠 | 첫 3초 후킹 | 15-60초 | 자막 + 1-3 해시 | 18-22시 |

## 워크플로우 예시 — 한 메시지, 5개 채널 동시 발행

{{< terminal title="claude — cowork" >}}
> 이번 주 신제품 출시 메시지를 인스타·LinkedIn·X·카카오·네이버 5개 채널로 변형해줘.
> 각 채널 톤·해시태그·길이에 맞춰. 인스타는 카드뉴스 5장 슬라이드도 함께.
{{< /terminal >}}

체인:
1. `sns-content` (메시지 코어)
2. `social-media` (채널 변형)
3. `card-news` (카드 디자인)
4. `ai-slop-reviewer` (검수)

## 콘텐츠 달력

채널이 많아질수록 "오늘 뭘 올릴까"를 매일 고민하는 시간이 늘어납니다. 월간 달력으로 발행 리듬을 미리 고정해 두면 그 고민이 사라집니다.

{{< terminal title="claude — cowork" >}}
> 다음 달 SNS 콘텐츠 달력 만들어줘. 인스타 주 5회, LinkedIn 주 3회, X 주 7회.
> 시즌 이슈(추석·할로윈) 반영, 채널별 톤 가이드 포함.
{{< /terminal >}}

## 한국 SNS 특이점

한국 SNS를 운영할 때는 채널별로 다른 네 가지 특성을 염두에 둬야 합니다. 네이버 블로그는 SNS로 분류되지만 실제로는 검색 노출 비중이 큰 반(半) 검색 채널로, 키워드 최적화 없이는 트래픽을 기대하기 어렵습니다. 카카오 채널 친구는 광고 동의를 받은 CRM 자산이기 때문에 마케팅 동의를 반드시 별도로 받아야 합니다 ([컴플라이언스 체크리스트](../../templates/compliance/)). 같은 9:16 세로 영상이라도 인스타 릴스와 유튜브 쇼츠는 알고리즘이 다릅니다. 쇼츠는 첫 3초 후킹이 핵심이고, 릴스는 전체적인 시각 톤이 더 중요합니다. LinkedIn의 경우 한국 계정에서도 영문과 한글을 함께 작성할 때 영문 우선으로 작성하면 도달이 더 유리합니다.

## 자주 겪는 실수

모든 채널에 동일한 콘텐츠를 그대로 올리는 것이 가장 큰 실수입니다. 자동 변형 없이 인스타 글을 LinkedIn에 그대로 게시하면 톤이 맞지 않아 양쪽 채널 모두에서 어색해집니다. 해시태그를 30개씩 다는 것도 역효과입니다. 인스타에서는 5~10개가 가장 효과적이며, 30개는 스팸 신호로 인식될 수 있습니다. 알고리즘은 조용히 바뀌기 때문에 분기 1회 채널별 트렌드를 점검하지 않으면 이미 효과 없는 방식을 계속 반복하게 됩니다 ([SEO 감사](../content-marketing/)).

## 다음 단계

- [콘텐츠 마케팅 전략](../content-marketing/)
- [이메일 마케팅 템플릿](../../templates/email/)
- [트랙 — 마케팅](../../tracks/track-marketing/)

---

### Sources

- moai-content 플러그인 [`social-media`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-content/skills/social-media/SKILL.md), [`card-news`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-content/skills/card-news/SKILL.md)
- moai-marketing 플러그인 [`sns-content`](https://github.com/modu-ai/cowork-plugins/blob/main/moai-marketing/skills/sns-content/SKILL.md)
