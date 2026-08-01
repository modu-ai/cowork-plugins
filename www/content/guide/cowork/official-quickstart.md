---
title: "Cowork 공식 빠른 시작"
weight: 15
description: "Claude 공식 가이드 기준 — Cowork가 무엇이고, 어떻게 켜고, 무엇을 주의해야 하는지 핵심만 정리했습니다."
geekdocBreadcrumb: true
aliases: ["/cowork/official-quickstart/"]
---

채팅으로 Claude와 대화하는 것이 "옆에서 같이 의논하는" 방식이라면 Cowork는 "Claude에게 일을 통째로 맡기고 자리를 비웠다 돌아오면 결과물이 완성돼 있는" 방식에 가깝습니다. Claude Cowork는 Claude Desktop 앱 안에서 동작하는 **에이전트형 작업 환경**으로, 내 컴퓨터의 파일에 직접 접근하고, 여러 단계를 스스로 수행해, 서식이 갖춰진 문서·정리된 파일·조사 결과물까지 만들어 줍니다.

이 페이지는 Claude 공식 "Get started with Claude Cowork" 가이드를 한국어로 요약한 빠른 시작입니다. 더 자세한 한국어 안내는 [Cowork 소개](/guide/cowork/intro/)와 이어지는 페이지들을 참고하세요.

## Cowork가 하는 일

| 기능 | 설명 |
|---|---|
| **로컬 파일 접근** | 내 컴퓨터의 파일을 직접 읽고 수정 — 업로드·다운로드 없이 작업 |
| **다단계 작업** | 서브에이전트를 조율해 복잡한 여러 단계 작업을 자동 수행 |
| **전문 산출물 생성** | 수식이 포함된 Excel, PowerPoint, 서식 문서 등 완성형 결과물 |
| **장시간 작업** | 타임아웃 없이 오래 걸리는 작업도 수행 |
| **예약 작업** | 정기적으로 반복되는 작업을 예약 실행 (Cowork 고유 기능) |
| **문서 직접 편집** | "Edit with Claude"로 문서를 그 자리에서 수정 |
| **프로젝트** | 관련 작업을 묶어 지속적인 맥락으로 관리 |

## 누구를 위한 도구인가요

- **유료 구독자 전용**: Pro · Max · Team · Enterprise 플랜
- **데스크톱 사용자**: macOS 또는 Windows의 Claude Desktop 앱 (웹·모바일에서는 Cowork 작업 불가)
- 복잡한 워크플로를 다루는 지식 근로자

{{< hint type="note" >}}
Cowork는 **Claude Desktop 앱에서만** 동작합니다. Pro·Max 모바일 앱에서는 데스크톱이 활성 상태일 때 메시지 확인 정도만 가능합니다. 작업이 도는 동안에는 컴퓨터가 잠들지 않고 앱이 열려 있어야 합니다.
{{< /hint >}}

## Chat·Claude Code와 무엇이 다른가요

| 항목 | Claude Cowork |
|---|---|
| **실행 위치** | 터미널을 열지 않고 Claude Desktop 안에서 실행 |
| **작동 방식** | 에이전트 구조로 복잡한 워크플로를 자율적으로 수행 |
| **예약 실행** | 작업을 예약해 자동 실행 (Cowork만의 기능) |
| **사용량** | 일반 채팅보다 사용량을 더 많이 소비 |

## 시작하는 방법

1. **Claude Desktop 앱**을 엽니다.
2. 화면에서 **"Chat" / "Cowork"** 모드 선택 탭을 찾습니다.
3. **"Cowork"** 탭을 클릭해 작업(Tasks) 모드로 전환합니다.
4. Claude에게 시킬 **작업을 설명**합니다.
5. Claude가 제안한 **실행 계획을 검토**한 뒤 진행을 허용합니다.

### 전역 지침 설정하기 (선택)

매번 같은 규칙을 반복하지 않으려면 전역 지침을 정해 둘 수 있습니다.

1. **Settings > Cowork**로 이동합니다.
2. Global instructions 옆의 **"Edit"**를 클릭합니다.
3. 지침을 입력하고 **"Save"**를 누릅니다.

{{< hint type="tip" >}}
권한 모드는 **"Ask before acting"(행동 전 확인)** 또는 **"Act without asking"(확인 없이 실행)** 중에 고를 수 있습니다. 처음에는 확인 모드로 시작해 Claude의 작업 방식을 익힌 뒤 조정하는 것을 권합니다. 자세한 내용은 [폴더와 권한](/guide/cowork/permissions/)을 참고하세요.
{{< /hint >}}

## 안전하게 쓰기 위한 주의사항

Cowork는 컴퓨터를 직접 조작하고 인터넷에 접근하는 **에이전트형 특성상 고유한 위험**이 있습니다. 아래를 기억하세요.

- **파일 삭제 보호**: Claude가 파일을 지우려면 명시적인 **"Allow"** 확인이 필요합니다.
- **격리 실행이지만 실제 변경**: 코드는 격리된 VM에서 실행되지만 내 파일에 실제 변경을 만들 수 있습니다.
- **공유 제한**: 채팅·아티팩트 공유 기능은 제공되지 않습니다.
- **메모리 범위**: 메모리는 프로젝트 안에서만 유지되고 독립 세션 사이에는 이어지지 않습니다.
- **사용량**: 일반 채팅보다 사용량을 크게 소비하므로 **Settings > Usage**에서 사용량을 확인하세요.

{{< hint type="warning" >}}
규제·법률·의료처럼 사람의 최종 판단이 반드시 필요한 영역에서는 초안 작성 용도로만 쓰고 검토는 사람이 수행하세요. Team·Enterprise 관리자는 조직 설정에서 웹 검색을 비활성화할 수 있습니다. Cowork 세션은 Compliance API에 포함되지 않습니다.
{{< /hint >}}

## 자주 겪는 문제

| 증상 | 원인·해결 |
|---|---|
| "Setting up Claude's workspace" 표시 | 버전 업데이트 중 정상적으로 나타나는 메시지 |
| Windows: "VM service not running" | 재설치하거나 서비스를 수동으로 시작 |
| Windows: "EXDEV: cross-device link" | 저장 경로가 `C:\` 이외 드라이브일 때 발생 |

자세한 문제 해결은 [트러블슈팅](/guide/cowork/troubleshooting/)을 참고하세요.

## 다음 단계

- **[Cowork 소개](/guide/cowork/intro/)** — Cowork가 무엇이고 누구를 위한 도구인지 자세히
- **[설치와 요금제](/guide/cowork/install/)** — Mac·Windows 설치와 요금제 요건
- **[첫 작업 실행](/guide/cowork/first-task/)** — 5분 안에 첫 결과물 만들기
- **[예약 작업](/guide/cowork/schedule/)** — 반복 작업 자동 실행하기

## 원문 출처

- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
