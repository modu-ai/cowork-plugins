---
title: "moai-lifestyle — 여행·웨딩·건강"
weight: 180
description: "여행 일정·이벤트·웨딩 기획·웰니스를 다루는 개인 일상 3개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-lifestyle"]
---

# moai-lifestyle

> 개인 일상과 이벤트 기획을 위한 3개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-lifestyle` (v1.5.0)는 여행 일정·맛집·숙소·예산 계획과 부동산 수익률·사이드 프로젝트 검토, 행사·워크샵·웨딩 준비와 예산·타임라인, 운동 루틴·식단·육아·시니어 케어 플랜까지 개인 일상 영역을 자동화합니다.

## 설치

{{< tabs "install-lifestyle" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-lifestyle` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-lifestyle)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `travel-planner` | 여행 일정·맛집·숙소·예산, 부동산 수익률, 사이드 프로젝트 |
| `event-planner` | 행사·워크샵·웨딩 준비, 예산·타임라인 |
| `wellness-coach` | 운동 루틴, 식단, 육아, 시니어 케어 |

## 대표 체인

**여행 일정표**

```text
travel-planner → xlsx-creator(예산표) → docx-generator(일정표)
```

**이벤트 기획**

```text
> event-planner → docx-generator(기획서) → xlsx-creator(체크리스트)
```

**웰니스 플랜**

```text
wellness-coach → docx-generator(월간 플랜) → ai-slop-reviewer
```

## 빠른 사용 예

```text
제주 3박 4일 가족 여행(아이 7세) 일정 짜줘. 예산 150만원, 렌트카 포함.
```

```text
> 50명 규모 회사 워크샵 하루 프로그램 기획해줘. 팀빌딩 위주.
```

## 다음 단계

- [`moai-business`](../moai-business/) — 부업·사이드 프로젝트 기획
- [`moai-finance`](../moai-finance/) — 개인 재무

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-lifestyle 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-lifestyle)
