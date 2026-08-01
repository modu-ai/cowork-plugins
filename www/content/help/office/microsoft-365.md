---
title: "Microsoft 365 연동"
weight: 10
description: "Excel·Word·PowerPoint·Outlook에서 Claude를 바로 사용하고, M365 앱 사이를 오가며 작업하고 받아쓰기로 입력하는 법을 안내합니다."
geekdocBreadcrumb: true
aliases: ["/office/microsoft-365/"]
---

매일 쓰는 엑셀이나 워드 창을 떠나지 않고도 옆자리 동료에게 "이 표 좀 봐 줄래?", "이 보고서 톤만 다듬어 줘"라고 부탁하듯 Claude에게 일을 맡길 수 있다면 어떨까요? Claude의 Microsoft 365 추가 기능(add-in)은 바로 그런 경험을 제공합니다. Excel, Word, PowerPoint, Outlook 안에 Claude를 사이드바로 띄워 두고 평소 작업 흐름을 끊지 않으면서 질문하고 수정하고 정리할 수 있습니다.

이 추가 기능들은 Pro, Max, Team, Enterprise 요금제에서 사용할 수 있으며 일부는 아직 베타 단계입니다. 각 앱에서 어떤 일을 할 수 있는지, 어떻게 설치하는지, 그리고 무엇을 주의해야 하는지 차근차근 살펴보겠습니다.

## 한눈에 보는 Office 추가 기능

| 앱 | 주요 역할 | 상태 | 요금제 |
|---|---|---|---|
| **Excel** | 워크북 분석, 셀 단위 인용, 수식 보존 수정, 재무 모델 작성 | 정식 | Pro · Max · Team · Enterprise |
| **PowerPoint** | 템플릿 기반 슬라이드 생성, 특정 슬라이드 수정, 차트·다이어그램 작성 | 정식 | Pro · Max · Team · Enterprise |
| **Word** | 인용 기반 문서 Q&A, 변경 내용 추적 편집, 템플릿 채우기 | 베타 | Pro · Max · Team · Enterprise |
| **Outlook** | 메일 분류·초안 작성, 스레드 요약, 일정 조율, 회의 브리핑 | 베타 | Pro · Max · Team · Enterprise |

{{< hint type="note" >}}
네 가지 추가 기능 모두 채팅 기록은 브라우저에 로컬로만 저장되어 기기 간에 동기화되지 않습니다. 입력과 출력 데이터는 백엔드에서 30일 이내에 자동 삭제됩니다.
{{< /hint >}}

## Excel에서 Claude 사용하기

Excel용 Claude는 워크북에 대해 질문하면 **셀 단위 인용**과 함께 답해 주는 추가 기능입니다. 어떤 셀을 근거로 답했는지 짚어 주기 때문에 신뢰하고 확인하기 좋습니다. 가정값을 바꿔도 기존 수식·의존 관계·서식은 그대로 보존하면서 결과를 다시 계산해 주고 오류를 찾아내거나 재무 모델을 만드는 일도 도와줍니다.

### 무엇을 할 수 있나요

- 워크북에 대해 질문하고 셀 단위 인용으로 근거 확인
- 수식, 셀 의존 관계, 기존 서식을 보존하면서 가정값 수정
- 오류 식별 및 재무 모델 작성
- 정렬, 필터링, 조건부 서식, 데이터 유효성 검사 등 Excel 기본 기능 활용
- Claude 설정에서 외부 도구 커넥터와 스킬(Skills) 연동

### 지원 환경

| 항목 | 내용 |
|---|---|
| 지원 플랫폼 | 웹, Windows(빌드 16.0.13127.20296 이상), Mac(버전 16.46 이상, 빌드 21011600 이상), iPad(버전 2.51 이상) |
| 지원 파일 형식 | `.xlsx`, `.xlsm` |
| 미지원 | Excel 2016/2019(영구 라이선스), Android 기기 |

### 설치 방법

개인 사용자라면 다음과 같이 설치합니다.

1. Microsoft Marketplace의 **Claude for Microsoft 365** 항목으로 이동합니다.
2. **Get it now(지금 받기)** 버튼을 클릭합니다.
3. Excel을 열고 추가 기능을 활성화합니다.
4. Claude 계정으로 로그인합니다.

관리자가 조직 전체에 배포하는 경우는 다음과 같습니다.

1. Microsoft 365 관리 센터에 접속합니다.
2. 설정에서 **Let users access the Office Store(사용자가 Office 스토어에 접근하도록 허용)**를 켭니다.
3. **Integrated apps > Add-ins**에서 배포하거나 커스텀 매니페스트 XML 파일을 업로드합니다.

{{< hint type="warning" >}}
WEBSERVICE, STOCKHISTORY, IMPORTDATA, INDIRECT, IMAGE, FILES 같은 일부 함수는 실행 전에 사용자 확인을 요청합니다. 또한 데이터 테이블, 매크로, VBA 같은 고급 기능은 지원되지 않습니다.
{{< /hint >}}

## PowerPoint에서 Claude 사용하기

PowerPoint용 Claude는 발표 자료를 만드는 과정을 도와줍니다. 기존 템플릿을 바탕으로 새 슬라이드를 만들고, 특정 슬라이드만 골라 수정하며, 자연어 설명만으로 전체 덱 구조를 생성할 수 있습니다. 글머리 기호를 다이어그램이나 PowerPoint 기본 차트로 바꿔 주는 것도 강점입니다.

### 무엇을 할 수 있나요

- 기존 템플릿에서 새 슬라이드 만들기
- 특정 슬라이드만 골라 정밀하게 수정하기
- 자연어 설명으로 전체 덱 구조 생성하기
- 글머리 기호를 다이어그램과 PowerPoint 기본 차트로 변환하기
- 커넥터로 다른 도구의 맥락을 가져오고 활성화한 스킬 자동 적용하기

### 설치 방법

1. Microsoft Marketplace에서 **Claude for PowerPoint**를 찾아 **Get it now**를 클릭합니다.(개인 설치)
2. 관리자 배포는 **Microsoft 365 관리 센터 > Settings > Integrated apps > Add-ins**에서 Claude for PowerPoint를 추가합니다.
3. 또는 PowerPoint 추가 기능 설정에서 커스텀 매니페스트 XML 파일을 업로드합니다.
4. 관리자는 **Settings > Org Settings > User owned apps and services**에서 **Let users access the Office Store**를 켜야 합니다.
5. 웹·Windows·Mac에서 PowerPoint를 열고 추가 기능 메뉴로 이동합니다.(Mac은 **Tools > Add-ins**, Windows는 **Home > Add-ins**)
6. 사이드바에서 커넥터, 설정, 지시문(Instructions) 입력란을 사용합니다.

{{< hint type="warning" >}}
관찰 가능성(observability)과 감사 기능(auditability)은 Free·Pro·Max·Team 요금제에서는 제공되지 않습니다. 지원 환경은 PowerPoint 웹, Windows(빌드 16.0.13127.20296 이상), Mac(버전 16.46 이상)이며 PowerPoint 2016/2019(영구·볼륨 라이선스)와 iPad·Android에서는 사용할 수 없습니다.
{{< /hint >}}

## Word에서 Claude 사용하기 (베타)

Word용 Claude는 문서 작업에 Claude를 붙여 주는 추가 기능으로, 현재 베타 단계입니다. 문서에 대해 질문하면 해당 섹션을 인용해 답하고 텍스트를 고칠 때는 모든 수정이 Word의 **변경 내용 추적(tracked changes)**으로 표시되어 검토 창에서 그대로 확인하고 수락하거나 거절할 수 있습니다.

### 무엇을 할 수 있나요

- 섹션 인용과 함께 문서 Q&A
- 변경 내용 추적으로 표시되는 텍스트 편집
- 댓글 스레드 작성
- 템플릿 채우기
- 의미 기반(semantic) 문서 탐색

### 지원 환경과 설치

지원 플랫폼은 Word 웹, Windows(Microsoft 365 버전 2205 / 빌드 15202.10000 이상), Mac(버전 16.61 / 빌드 22040100 이상)입니다. Word 2016/2019, iPad, Android에서는 사용할 수 없습니다.

1. Microsoft Marketplace에서 **'Claude by Anthropic for Word'**를 검색합니다.
2. **Get it now**를 클릭해 설치합니다.
3. 관리자는 **Microsoft 365 관리 센터 > Settings > Integrated apps**에서 배포하거나 admin.microsoft.com에서 커스텀 매니페스트 XML을 업로드합니다.
4. Word 문서를 열고 추가 기능 메뉴로 이동합니다.(Mac은 **Tools > Add-ins**, Windows는 **Home > Add-ins**)
5. 수정 사항은 수락·거절하기 전에 Word 기본 검토 창에서 변경 내용을 확인합니다.

{{< hint type="note" >}}
Word용 Claude는 Excel·PowerPoint용 Claude와 맥락을 공유해 앱 사이를 오가며 데이터를 통합할 수 있습니다. 자세한 내용은 아래 'Microsoft 365 앱 간 작업하기'를 참고하세요.
{{< /hint >}}

## Outlook에서 Claude 사용하기 (베타)

Outlook용 Claude는 메일 관리, 초안 작성, 일정 조율, 첨부 문서 분석을 도와주는 베타 추가 기능입니다. 받은 편지함을 분류하고, 답장·전달 초안을 만들고, 긴 스레드를 인용과 함께 요약하며, 참석자 일정을 확인해 회의 시간을 제안하고 회의 브리핑까지 만들어 줍니다.

### 무엇을 할 수 있나요

- 메일 분류(triage) 및 답장·전달 초안 작성
- 인용과 함께 스레드 요약
- 참석자 가능 시간 확인 및 회의 시간 제안
- 회의 브리핑 생성
- 주제별로 지난 대화 검색
- 첨부 파일 분석(`.docx`, `.xlsx`, `.pptx`, `.pdf` 지원)

### 설치 방법

개인 사용자는 다음과 같이 설치합니다.

1. Microsoft AppSource에서 **'Claude by Anthropic for Outlook'**을 검색합니다.
2. **Get it now**를 클릭합니다.
3. Outlook을 열고 아무 메일이나 선택합니다.
4. **Claude 버튼**을 클릭한 뒤 Claude 계정으로 로그인합니다.

조직 배포는 다음과 같습니다.

1. 관리자가 **Microsoft 365 관리 센터 > Settings > Integrated apps > Add-ins**로 이동합니다.
2. 추가 기능을 배포하거나 `https://pivot.claude.ai/manifest-outlook.xml` 매니페스트를 업로드합니다.
3. 전역 관리자(Global Administrator)가 Mail.ReadWrite, Calendars.Read, People.Read, User.Read 범위에 대해 Microsoft Graph 동의를 부여합니다.

{{< hint type="warning" >}}
Claude는 메일을 절대 자동으로 발송하지 않습니다. 모든 초안은 보내기 전에 직접 검토해야 합니다. 외부·신뢰할 수 없는 발신자의 메일에는 프롬프트 인젝션(prompt injection) 위험이 있으니 주의하세요. Microsoft Graph 액세스 토큰은 브라우저 캐시에 남으며 Anthropic은 메일함 사본을 저장하지 않습니다.
{{< /hint >}}

## Microsoft 365 앱 간 작업하기

Claude는 Excel, PowerPoint, Word, Outlook을 **오가며** 데이터를 직접 옮기지 않고도 맥락을 조율할 수 있습니다. 예를 들어 Excel에서 데이터를 뽑아 PowerPoint 슬라이드를 채우거나, 스프레드시트 수치를 바탕으로 워드 메모 초안을 쓰거나, 첨부 파일이 포함된 Outlook 스레드를 통째로 불러올 수 있습니다.

### 사용하려면 무엇이 필요한가요

1. Microsoft Marketplace에서 네 가지 추가 기능을 모두 설치합니다.(Claude for Microsoft 365 + Claude for Outlook)
2. 각 추가 기능을 사용하기 전에 최소 한 번 활성화합니다.
3. 각 추가 기능의 **Settings(설정)**로 들어갑니다.
4. **Let Claude work across files(Claude가 파일 간에 작업하도록 허용)** 토글을 켭니다.
5. Team·Enterprise는 조직 관리자가 먼저 조직 설정에서 이 기능을 활성화해야 개별 구성원이 사용할 수 있습니다.

### 무엇을 할 수 있나요

- Excel에서 데이터를 추출해 PowerPoint 슬라이드 채우기
- Word 문서·차트 업데이트하기
- 문서를 요약해 프레젠테이션으로 만들기
- 스프레드시트 데이터로 메모 초안 쓰기
- 전체 스레드 기록과 첨부 파일이 포함된 Outlook 메일 열기

{{< hint type="warning" >}}
앱 간 작업에는 몇 가지 한계가 있습니다. Claude는 **현재 열려 있는 파일만** 읽고 쓸 수 있으며 파일을 스스로 생성·열기·닫기는 할 수 없습니다. 앱 간 세션 기록은 세션 사이에 보존되지 않고 추가 기능 데이터는 조직의 커스텀 보존 정책을 따르지 않습니다. 또한 이 활동은 Enterprise 감사 로그와 컴플라이언스 기능에서 제외됩니다. 유료 요금제가 필요하며 무료 요금제에서는 사용할 수 없습니다.
{{< /hint >}}

## 사내 인프라(서드파티 플랫폼)로 배포하기

조직은 Anthropic API에 직접 연결하는 대신, 기존 회사 인프라로 Office 추가 기능을 배포할 수 있습니다. 프롬프트가 조직의 시스템을 거치도록 라우팅해 보안을 유지하면서도 문서를 읽고 편집하는 기능을 제공합니다.

### 연결 경로

| 경로 | 비고 |
|---|---|
| LLM Gateway | LiteLLM, Portkey, Kong |
| AWS Bedrock Direct | — |
| Google Vertex AI Direct | 웹 검색은 Vertex AI 배포에서만 지원 |
| Azure AI Foundry Direct | 커스텀 배포 이름 미지원 |

기본 준비물은 Microsoft AppSource의 Claude 추가 기능, Entra ID가 포함된 Microsoft 365, 그리고 Microsoft Graph 관리자 동의입니다. 설치는 claude-in-office 플러그인을 설치하고, 대화형 설정 마법사로 연결 경로를 선택한 뒤, 생성된 매니페스트를 관리 센터에 업로드하고 Microsoft Graph 권한을 부여하는 순서로 진행됩니다.

{{< hint type="warning" >}}
LiteLLM 버전 1.82.7과 1.82.8에는 악성코드가 포함되어 있었습니다. 이 버전은 반드시 피하고 영향을 받은 자격 증명은 즉시 교체하세요. 서드파티 인프라로 배포할 경우 '앱 간 작업' 기능은 사용할 수 없습니다. 네트워크에서는 pivot.claude.ai, claude.ai, 그리고 제공자별 엔드포인트를 허용 목록에 추가해야 합니다.
{{< /hint >}}

## Office 에이전트에서 받아쓰기 사용하기

타이핑 대신 말로 프롬프트를 입력하고 싶다면 받아쓰기(dictation) 기능을 쓸 수 있습니다. Anthropic 인프라에서 실시간으로 음성을 텍스트로 옮겨 주며 말하는 동안 단어가 입력창에 그대로 나타납니다.

1. 채팅 입력창 오른쪽의 **마이크 아이콘**을 클릭합니다.(안내 문구가 'Listening...'으로 바뀌고 버튼이 파란색이 됩니다)
2. 프롬프트를 말합니다.
3. 다시 마이크 아이콘을 클릭해 멈추거나 **Enter** 키를 눌러 멈춤과 전송을 동시에 합니다.
4. 다른 마이크를 쓰려면 아이콘 위에 마우스를 올리고 드롭다운 화살표를 클릭합니다.

{{< hint type="note" >}}
받아쓰기는 Claude에 직접 로그인하는 조직에서만 사용할 수 있고 게이트웨이·Vertex AI·Bedrock 같은 서드파티 인증 환경에서는 제공되지 않습니다. 이 경우에는 운영체제나 Office 앱의 받아쓰기 기능을 대신 사용하세요. 음성은 Anthropic 인프라에서만 처리되고 저장되지 않으며 제3자에게 전송되지 않습니다.
{{< /hint >}}

## 안전하게 사용하기

네 가지 추가 기능 모두 비슷한 주의사항을 공유합니다. 아래 내용을 기억하면 더 안심하고 활용할 수 있습니다.

- **신뢰할 수 없는 파일 주의**: 외부에서 받은 스프레드시트·템플릿·문서·메일에는 프롬프트 인젝션 공격 위험이 있습니다.
- **사람의 검토는 필수**: 최종 고객 산출물, 감사가 중요한 계산, 소송 서류 등에는 사람이 직접 확인하지 않은 결과를 그대로 쓰지 마세요.
- **민감 데이터 신중히**: 규제 대상이거나 매우 민감한 데이터에는 적절한 통제 없이 사용하지 않는 것이 좋습니다.
- **판단을 대체하지 않기**: 디자인 감각이나 전문가의 판단을 대신하는 도구가 아니라, 그것을 돕는 도구로 활용하세요.

{{< hint type="tip" >}}
결과물을 마무리하기 전에는 항상 변경 내용을 검토하고 출력이 우리 조직의 방식·기준과 맞는지 확인하는 습관을 들이세요.
{{< /hint >}}

## 다음 단계

- **[Office 통합 개요](/help/office/)** — Office에서 Claude를 쓰는 전체 그림 살펴보기
- **[스킬과 플러그인](/guide/chat/skills-plugins/)** — Office 추가 기능과 함께 쓰는 스킬·커넥터 알아보기
- **[요금제와 결제](/help/plans-billing/)** — Pro·Max·Team·Enterprise 요금제 비교

## 원문 출처

- [Use Claude for Excel](https://support.claude.com/en/articles/12650343-use-claude-for-excel)
- [Use Claude for PowerPoint](https://support.claude.com/en/articles/13521390-use-claude-for-powerpoint)
- [Use Claude for Word](https://support.claude.com/en/articles/14465370-use-claude-for-word)
- [Use Claude for Outlook](https://support.claude.com/en/articles/14855664-use-claude-for-outlook)
- [Work across Microsoft 365 apps](https://support.claude.com/en/articles/13892150-work-across-microsoft-365-apps)
- [Use Claude for Microsoft 365 with third-party platforms](https://support.claude.com/en/articles/13945233-use-claude-for-microsoft-365-with-third-party-platforms)
- [Use dictation in Office agents](https://support.claude.com/en/articles/14479591-use-dictation-in-office-agents)
