---
title: "moai-product — PRD·로드맵·UX"
weight: 80
description: "PRD·기능 명세·로드맵·UX 리서치를 담당하는 제품 매니저용 3개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-product"]
---

# moai-product

> 제품 매니저를 위한 3개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-product` (v1.5.0)는 제품 기획·UX 리서치·로드맵 관리에 필요한 문서를 자동으로 작성하는 플러그인입니다. PRD와 기능 명세뿐 아니라 AI 전략 보고서·정부 R&D 신청서, 분기 로드맵, 페르소나, 유저빌리티 테스트 계획, VOC·NPS 분석까지 제품 팀의 주요 산출물을 커버합니다.

## 설치

{{< tabs "install-product" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-product` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-product)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `spec-writer` | PRD, 기능 명세, AI 전략 보고서, 정부 R&D 신청서 |
| `roadmap-manager` | 프로젝트 로드맵, 마일스톤, MOU 초안, ESG 감사 |
| `ux-researcher` | 페르소나, 유저빌리티 테스트 계획, VOC·NPS 분석 |

## 대표 체인

**PRD 작성**

```text
ux-researcher → spec-writer → docx-generator → ai-slop-reviewer
```

**분기 로드맵**

```text
roadmap-manager → xlsx-creator(간트) → pptx-designer
```

## 빠른 사용 예

```text
결제 모듈 리뉴얼 PRD 써줘. 대상 고객은 국내 전자상거래 소상공인.
```

```text
지난 분기 NPS 결과 50개 텍스트 응답 분석해서 개선 우선순위 뽑아줘.
```

## 다음 단계

- [`moai-business`](../moai-business/) — 사업 전략 연계
- [`moai-data`](../moai-data/) — 정량 리서치 결합

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-product 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-product)
