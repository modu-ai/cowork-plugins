---
title: "자주 묻는 질문"
weight: 100
description: "Cowork를 2주 써본 사용자가 가장 자주 묻는 10가지 질문과 빠른 해결 단서를 모았습니다."
geekdocBreadcrumb: true
---

# 자주 묻는 질문

> Cowork를 2주 써본 뒤 가장 자주 올라오는 질문 10가지를 모았습니다.

{{< hint type="warning" >}}
v0.2 스켈레톤: 각 문항은 핵심 원인과 해결 키 한 줄로 시작합니다. 상세 해결법은 이후 보강합니다.
{{< /hint >}}

## 학습 목표

- 내 증상이 어떤 카테고리(설치·호출·산출물·성능)에 속하는지 분류할 수 있습니다.
- 해결 링크를 따라 5분 내 자체 해결을 시도할 수 있습니다.

## 선수 지식

- [설치와 요금제 요건](../install/)
- [첫 작업 실행하기](../first-task/)

## 설치·계정

### Q1. Claude Desktop에 Cowork 메뉴가 안 보입니다

Cowork는 현재 research preview 상태입니다. Claude 계정 종류(Free·Pro·Max·Team·Enterprise)와 지역에 따라 순차 제공 중입니다. [설치와 요금제 요건](../install/)에서 본인 플랜의 제공 상태를 확인하세요.

### Q2. 회사 계정에서 Cowork를 쓰고 싶습니다

Team·Enterprise의 경우 관리자가 Admin settings → Capabilities에서 Cowork 사용을 허용해야 합니다. [Team·Enterprise 관리](../enterprise/)를 참고하세요.

## 스킬·플러그인 호출

### Q3. 요청했는데 스킬이 자동 호출되지 않습니다

세 가지 원인을 순서대로 점검합니다.

1. 플러그인이 설치되었는가 (`/plugin` 슬래시 명령으로 확인)
2. 요청문에 스킬 트리거 키워드가 있는가 ([스킬 사용법](../skills/) 참고)
3. 상위 도메인 스킬에서 포맷 스킬로 명시적 인계가 일어났는가

### Q4. 플러그인 설치 후 업데이트는 어떻게 하나요

`/plugin marketplace update cowork-plugins`를 실행하면 최신 버전이 반영됩니다.

### Q5. 스킬 체인을 직접 설계하고 싶습니다

[스킬 체이닝 가이드](../../cookbook/skill-chaining/)의 3원칙(도메인 → 포맷 → 품질)을 먼저 읽고 쿡북 예제 중 자기 업무와 가까운 것을 복사·붙여넣기 후 변형하세요.

## 산출물·파일

### Q6. 생성된 DOCX/PPTX가 열리지 않습니다 (Windows)

대부분 MAX_PATH(260자) 제약 때문입니다. 파일을 짧은 경로(예: `C:\docs\`)로 복사해 열어보세요. [트러블슈팅](../../cookbook/troubleshooting/)을 참고하세요.

### Q7. 산출물에 AI 특유의 어투가 남아 있습니다

체인 마지막에 `ai-slop-reviewer`가 실행됐는지 확인하세요. 누락됐다면 "이 문서 AI 슬롭 검수해줘"라고 이어서 요청하면 됩니다.

## 성능·제한

### Q8. 긴 작업 중간에 컨텍스트가 끊깁니다

[프로젝트와 메모리](../projects-memory/) 사용을 권장합니다. 프로젝트 단위로 지침과 파일을 고정해두면 세션이 바뀌어도 일관성을 유지합니다.

### Q9. 한 세션에서 얼마나 많은 파일을 다룰 수 있나요

정확한 상한은 계정 유형에 따라 달라지며 수시로 조정됩니다. Anthropic 지원센터의 최신 정보를 확인하는 것이 확실합니다.

## 보안·감사

### Q10. 팀에서 쓸 때 로그·감사는 어떻게 확인하나요

Team·Enterprise 관리자 콘솔에서 사용 이력을 조회할 수 있습니다. 세부 항목은 [Team·Enterprise 관리](../enterprise/)와 [안전하게 사용하기](../safety/)를 함께 보세요.

## 자가 점검

{{< hint type="note" >}}
- Q. 위 10문항 중 본인이 방금 겪은 증상과 가장 유사한 것은? 해당 해결 링크를 끝까지 따라갔습니까? (쉬움·이해)
- Q. 내 요청이 자동 호출되지 않을 때 맨 먼저 점검해야 할 것은? (중간·적용)
{{< /hint >}}

## 다음 단계

- [트러블슈팅](../../cookbook/troubleshooting/) — 체인 실패 진단 패턴
- [안전하게 사용하기](../safety/) — 하지 말아야 할 5가지

---

### Sources

- [Claude 지원센터](https://support.claude.com)
- [Cowork research preview 공지](https://claude.com/blog/cowork-research-preview)
