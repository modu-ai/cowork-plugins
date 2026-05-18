---
title: "moai-education — 강사·교수·교사 교육 콘텐츠 풀스택"
weight: 160
description: "강사·교수·교사가 운영하는 강의·수업·연수·워크숍·정규 강좌의 커리큘럼·출제·학술 리서치·운영 매뉴얼·후기 자산화 5개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-education"]
---

# moai-education

> 강사·교수·교사를 위한 **교육 콘텐츠 풀스택 5개 스킬**. 커리큘럼 설계부터 시험 출제, 학술 리서치, 강의·수업·연수·워크숍 운영 매뉴얼, 수강 후 후기 자산화까지 한 플러그인에서 처리합니다.

```mermaid
flowchart TD
    subgraph 설계["강의 설계 (3)"]
        A["curriculum-designer<br/>강의 목차 설계"]
        B["assessment-creator<br/>시험·모의고사 출제"]
        C["research-assistant<br/>학술 리서치"]
    end
    subgraph 운영["강의 운영·자산화 (2)"]
        D["course-curriculum-design<br/>운영 매뉴얼·시간표·동선"]
        E["course-followup-sequence<br/>30일 후기 자산화"]
    end
    A --> B
    D --> E
    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style D fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style E fill:#fbf0dc,stroke:#c47b2a,color:#09110f
```

## 무엇을 하는 플러그인인가

`moai-education`은 강사·교수·교사가 운영하는 모든 교육 활동을 자동화합니다. 강의 목차·학습 목표·역량 갭 분석, 시험·퀴즈·모의고사, 자격증·공무원 시험 대비, 학술 리서치·문헌 검토·논문 구조부터 **단기 특강·사내 연수·다일 워크숍·정규 학기 강좌의 운영 실무 매뉴얼**(시간표·강사 동선·D-N 사전 준비물·환경 체크리스트·리스크 Plan B), **수강 후 30일 후기 자산화 시퀀스**(D+1·D+3·D+7·D+14·D+30 카피 5종)까지 교육 콘텐츠 제작과 운영 전반을 커버합니다.

대상 사용자:
- 온·오프라인 강의를 운영하는 강사·프리랜서 강사
- 대학·대학원 수업을 진행하는 교수·시간강사
- 학교·학원 수업을 운영하는 교사·학원 강사
- 사내 연수·집체교육을 운영하는 HRD 담당자
- 평생교육원·HRD-Net·K-MOOC 운영자

## 설치

{{< tabs "install-education" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-education` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-education)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (5개)

### 강의 설계·시험 출제·학술 리서치 (3)

| 스킬 | 용도 |
|---|---|
| `curriculum-designer` | 온라인·오프라인 강의 목차·학습 목표·역량 갭 분석, 외국어 학습 전략 |
| `assessment-creator` | 시험·퀴즈·모의고사, 자격증·공무원 대비 |
| `research-assistant` | 학술 리서치, 문헌 검토, 논문 구조 |

### 강의·연수 운영 실무 (2)

| 스킬 | 용도 | 출력 |
|---|---|---|
| `course-curriculum-design` | 일자별 시간표(1일·다일·주간 모드 지원) + 강사·조교 동선표 + D-N 사전 준비물 메일 + 환경·설비 체크리스트 + 리스크 Plan B 5건+ | `moai-office:docx-generator` 자동 체이닝 → Word(.docx) |
| `course-followup-sequence` | 강의 종료 후 30일 후기 카피 5종(D+1·D+3·D+7·D+14·D+30) + 인센티브·자산화 시퀀스 | 후기 카피 5종 + 발송 가이드 |

## 대표 체인

**강의 커리큘럼 + 교안**

```text
curriculum-designer → docx-generator → pptx-designer → ai-slop-reviewer
```

**자격증 모의고사 키트**

```text
assessment-creator → xlsx-creator(문제지) → docx-generator(해설)
```

**강의·연수·워크숍 운영 풀 사이클**

```text
[D-N]   course-curriculum-design → moai-office:docx-generator(.docx 운영 매뉴얼)
[D-7]   사전 준비물 안내 메일 발송 (course-curriculum-design --output prep-mail)
[D-1]   course-curriculum-design (시간표·동선표 출력)
[D+0]   강의 진행 (1일 특강·다일 워크숍·8/16주 정규 강좌)
[D+1~D+30]  course-followup-sequence → moai-content:copywriting
              → ai-slop-reviewer → moai-content:korean-spell-check
```

## 빠른 사용 예 (한 줄 요청 + 시스템 자동 인터뷰)

> 매번 옵션을 직접 작성할 필요 없습니다. 짧은 한 줄로 요청하면 시스템이 강의 형식·일수·대상·운영 인력을 인터뷰로 수집합니다.

{{< terminal title="claude — cowork" >}}
> "ChatGPT 실무 활용" 8주 과정 커리큘럼 짜줘
{{< /terminal >}}

→ 시스템 인터뷰: 수준·시수·대상·산출물 → `curriculum-designer` 자동 호출

{{< terminal title="claude — cowork" >}}
> 정보처리기사 실기 모의고사 50문항 + 해설 만들어줘
{{< /terminal >}}

→ `assessment-creator` 자동 호출

{{< terminal title="claude — cowork" >}}
> 사내 AI 활용 2일 워크숍 운영 매뉴얼 만들어줘
{{< /terminal >}}

→ 시스템 인터뷰: 일수·세션 수·운영 인력·사전 안내 시점 → `course-curriculum-design` 자동 호출

{{< terminal title="claude — cowork" >}}
> 강의 끝났어, D+1 후기 카피 만들어줘
{{< /terminal >}}

→ 시스템 인터뷰: 강의명·발송 채널·인센티브 → `course-followup-sequence` 자동 호출

## 다음 단계

- [`moai-research`](../moai-research/) — 학술 리서치 결합
- [`moai-content`](../moai-content/) — 강의 홍보 콘텐츠 + 후기 카피 후처리
- [`moai-office`](../moai-office/) — Word·PPT·Excel 최종 산출물
- [`moai-media`](../moai-media/) — 강의 홍보 영상·이미지 생성

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-education 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-education)
