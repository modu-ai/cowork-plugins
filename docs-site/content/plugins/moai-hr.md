---
title: "moai-hr — 채용·근로·평가"
weight: 110
description: "한국 노동법·4대보험을 반영한 채용·근로계약·성과평가·원격근무 4개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-hr"]
---

# moai-hr

> 한국 노동법·4대보험을 반영한 4개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-hr` (v1.5.0)는 채용공고(JD) 작성, 면접 질문 설계, 신입 온보딩, 채용 제안서·근로계약서, MBO·OKR·KPI 기반 성과평가, 원격·하이브리드 근무 정책까지 HR 전 영역을 커버합니다. 2026년 기준 4대보험 요율과 근로기준법 조항을 계약서 템플릿에 반영하며, 스톡옵션 부여계약서 표준 조항도 포함됩니다.

## 설치

{{< tabs "install-hr" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-hr` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-hr)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `employment-manager` | JD 작성, 면접 질문, 신입 온보딩, 멘토링 |
| `draft-offer` | 채용 제안서·근로계약서 (연봉·4대보험·스톡옵션) |
| `performance-review` | MBO·OKR·KPI, 360도 평가, 피드백 면담 스크립트 |
| `people-operations` | 원격·하이브리드 근무 정책, 협업 도구, 직원 경험 |

## 한국 실무 반영

- 2026년 기준 **4대보험 요율** 자동 반영
- **근로기준법** 조항 기반 계약서 템플릿
- **스톡옵션 부여계약서** 표준 조항 포함

## 대표 체인

**신규 입사자 패키지**

```text
employment-manager(JD) → draft-offer → docx-generator → ai-slop-reviewer
```

**분기 성과평가 운영**

```text
performance-review → docx-generator(면담 스크립트)
```

## 빠른 사용 예

```text
> 시니어 백엔드 개발자 채용 JD 만들어줘. 연봉 밴드 5500~7500만.
```

```text
> 수습 3개월 끝나는 직원에게 근로계약서 업데이트 초안 만들어줘.
```

## 다음 단계

- [`moai-finance`](../moai-finance/) — 급여 정산
- [`moai-legal`](../moai-legal/) — 근로계약 검토

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-hr 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-hr)
