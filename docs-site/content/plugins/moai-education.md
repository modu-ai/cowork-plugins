---
title: "moai-education — 커리큘럼·출제"
weight: 160
description: "강의 커리큘럼·시험 출제·학술 리서치를 담당하는 교육 실무 3개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-education"]
---

# moai-education

> 강의 설계부터 시험 출제까지 교육 실무 3개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-education` (v1.5.0)는 온라인 강의 목차·학습 목표·역량 갭 분석, 시험·퀴즈·모의고사, 자격증·공무원 시험 대비 문항, 학술 리서치·문헌 검토·논문 구조까지 교육 콘텐츠 제작 실무를 자동화합니다.

## 설치

{{< tabs "install-education" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-education` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-education)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `curriculum-designer` | 온라인 강의 목차·학습 목표·역량 갭 분석 |
| `assessment-creator` | 시험·퀴즈·모의고사, 자격증·공무원 대비 |
| `research-assistant` | 학술 리서치, 문헌 검토, 논문 구조 |

## 대표 체인

**강의 커리큘럼 + 교안**

```text
curriculum-designer → docx-generator → pptx-designer → ai-slop-reviewer
```

**자격증 모의고사 키트**

```text
assessment-creator → xlsx-creator(문제지) → docx-generator(해설)
```

**학습 리서치 보고서**

```text
research-assistant → paper-search → docx-generator → ai-slop-reviewer
```

## 빠른 사용 예

```text
"ChatGPT 실무 활용" 8주 과정 커리큘럼 짜줘. 시수 16시간, 중급자 대상.
```

```text
정보처리기사 실기 모의고사 50문항 + 해설 만들어줘.
```

## 다음 단계

- [`moai-research`](../moai-research/) — 학술 리서치 결합
- [`moai-content`](../moai-content/) — 강의 홍보 콘텐츠

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-education 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-education)
