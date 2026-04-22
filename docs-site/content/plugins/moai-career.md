---
title: "moai-career — 이력서·면접·포트폴리오"
weight: 170
description: "자소서·이력서·면접 코칭·포트폴리오 구성을 담당하는 커리어 준비 4개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-career"]
---

# moai-career

> 자소서·이력서·면접·포트폴리오 4개 스킬을 제공합니다.

## 무엇을 하는 플러그인인가

`moai-career` (v1.5.0)는 STAR 기법 기반 자기소개서 작성, ATS(지원자 추적 시스템) 친화 이력서·영문 CV·링크드인 프로필, JD 분석과 기업 리서치·역량 매칭, AI·BEI·PT·토론·임원 유형별 면접 대비와 모의 면접, 개발·디자인·마케팅 포트폴리오 구성(GitHub·Behance·Notion 최적화)까지 취업·이직 전 주기를 지원합니다.

## 설치

{{< tabs "install-career" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-career` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-career)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `resume-builder` | STAR 기반 자소서, ATS 이력서, 영문 CV, 링크드인 |
| `job-analyzer` | JD 분석, 기업 리서치, 역량 매칭 |
| `interview-coach` | AI·BEI·PT·토론·임원 면접 유형별 대비, 모의 면접 |
| `portfolio-guide` | 개발·디자인·마케팅 포트폴리오 구성, GitHub·Behance·Notion 최적화 |

## 대표 체인

**지원 패키지 제작**

```text
job-analyzer → resume-builder → docx-generator → ai-slop-reviewer
```

**면접 준비 루프**

```text
job-analyzer → interview-coach(예상 질문) → interview-coach(모의)
```

**포트폴리오 업그레이드**

```text
portfolio-guide → docx-generator(프로젝트 기술서) → ai-slop-reviewer
```

## 빠른 사용 예

```text
첨부한 JD 분석해서 지원 자소서 4개 문항 1000자씩 써줘. 내 이력서는 /uploads/.
```

```text
PM 임원 면접 예상 질문 20개 + 모범 답변 뽑아줘.
```

## 다음 단계

- [`moai-marketing`](../moai-marketing/) — 퍼스널 브랜딩
- [`moai-content`](../moai-content/) — 링크드인 콘텐츠

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-career 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-career)
