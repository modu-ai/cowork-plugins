---
title: "스킬과 플러그인"
weight: 45
description: "스킬과 플러그인으로 Claude의 능력을 확장하기 — 사용·제작·디렉터리 탐색까지 한국어로 안내합니다."
geekdocBreadcrumb: true
aliases: ["/chat/skills-plugins/"]
---

스마트폰을 처음 샀을 때는 기본 앱만 있지만 필요에 따라 사진 편집 앱이나 가계부 앱을 설치하면서 점점 나에게 딱 맞는 도구가 되어갑니다. Claude의 **스킬**과 **플러그인**도 비슷합니다. 기본 Claude만으로도 충분히 똑똑하지만 엑셀 문서를 더 잘 만들거나 회사의 브랜드 규칙을 자동으로 적용하거나 자주 하는 작업을 반복 처리하도록 능력을 덧붙일 수 있습니다.

이 페이지에서는 스킬이 무엇인지, 어떻게 켜고 쓰는지, 직접 만드는 방법, 그리고 플러그인과 함께 한곳에서 둘러보는 디렉터리까지 차근차근 살펴봅니다. 어렵게 들릴 수 있지만 대부분 클릭 몇 번이면 끝나니 부담 갖지 않으셔도 됩니다.

## 스킬이란 무엇인가요

스킬(Skill)은 Claude가 특정 작업을 더 잘 처리하도록 도와주는 **지침·스크립트·자료가 담긴 폴더**입니다. 필요할 때만 관련 정보를 불러와 사용하기 때문에(점진적 공개 방식), 한꺼번에 많은 내용을 떠안지 않고도 전문적인 작업을 깔끔하게 처리할 수 있습니다.

스킬은 **모든 요금제(Free, Pro, Max, Team, Enterprise)**에서 쓸 수 있으며 코드 실행 기능이 켜진 계정에서 작동합니다.

### 스킬의 4가지 종류

| 종류 | 누가 만드나요 | 예시 |
|---|---|---|
| **Anthropic 스킬** | Anthropic이 직접 제작·관리 | Excel·Word·PowerPoint·PDF 문서 생성 강화 |
| **커스텀 스킬** | 사용자 또는 조직이 직접 제작 | 브랜드 가이드 적용, 회의록 정리, 데이터 분석 자동화 |
| **조직 제공 스킬** | 조직이 구성원 전체에게 배포 | Team·Enterprise 전용 공용 스킬 |
| **파트너 스킬** | Notion, Figma, Atlassian 등 파트너 제공 | 외부 서비스 연동 작업 |

### 스킬로 할 수 있는 일

- 브랜드 가이드라인을 적용해 일관된 문서 만들기
- 정해진 양식의 안내문·공지문 자동 작성
- 회의록을 구조화해 정리
- JIRA·Asana에 작업(태스크) 생성
- 데이터 분석 실행
- 개인 업무 흐름 자동화

{{< hint type="note" >}}
스킬을 쓰려면 **코드 실행(Code execution) 기능**이 켜져 있어야 합니다. 또한 조직 제공 스킬은 Team·Enterprise 요금제에서만 사용할 수 있습니다.
{{< /hint >}}

### 비슷한 기능과 무엇이 다른가요

| 기능 | 역할 | 차이점 |
|---|---|---|
| **스킬** | 특정 작업을 잘 처리하도록 능력 확장 | 작업 중심, 필요할 때 자동 활성화 |
| **Projects** | 자주 쓰는 지식을 저장 | 고정된 배경 지식 제공 |
| **MCP(커넥터)** | 외부 서비스와 연결 | 데이터 연동 중심 |
| **맞춤 지침** | Claude의 전반적 말투·태도 설정 | 넓고 일반적인 지침 |

## 스킬 켜고 사용하기

스킬은 한 번 켜두면 **따로 불러내지 않아도** Claude가 요청 내용을 보고 알아서 적절한 스킬을 적용합니다. 예를 들어 "이 데이터로 엑셀 표를 만들어 줘"라고 하면 Excel 스킬이 자동으로 작동하는 식입니다.

### 개인 사용자(Free·Pro·Max) 설정 방법

1. **Settings(설정) > Capabilities(기능)**로 이동
2. **'Code execution and file creation'(코드 실행 및 파일 생성)** 켜기
3. **Customize(맞춤설정) > Skills(스킬)**로 이동
4. 원하는 스킬을 켜거나 끄기

### Team·Enterprise 설정 방법

1. 조직 소유자가 **Organization settings(조직 설정) > Skills**에서 코드 실행과 스킬 기능을 먼저 활성화
2. 구성원은 **Customize > Skills**에서 개인 설정 관리

### 기본 제공 Anthropic 스킬

- 향상된 **Excel** 스프레드시트 생성
- 전문적인 **Word** 문서 작성
- **PowerPoint** 프레젠테이션 생성
- **PDF** 생성 및 처리

{{< hint type="warning" >}}
스킬은 **신뢰할 수 있는 출처**에서만 설치하세요. 켜기 전에 스킬 내용을 살펴보고 특히 코드 의존성이나 외부 연결 부분을 확인하는 것이 안전합니다.
{{< /hint >}}

## 커스텀 스킬 직접 만들기

원하는 스킬이 없다면 직접 만들 수도 있습니다. 기본 스킬은 코딩 지식이 없어도 **마크다운(Markdown)** 으로 작성할 수 있습니다. 가장 중요한 건 `skill.md` 파일 하나입니다.

### 최소 구성 요건

`skill.md` 파일에 다음 정보를 YAML 형식으로 담아야 합니다.

| 항목 | 설명 | 제한 |
|---|---|---|
| **name** | 스킬 이름 | 최대 64자 |
| **description** | 스킬 설명 | 최대 200자 |

여기에 선택적으로 의존성(Dependencies), 지침이 담긴 본문, 참고 파일(REFERENCE.md 등), 실행 스크립트(Python, JavaScript/Node.js)를 더할 수 있습니다.

### 만드는 순서

1. 필수 정보(name, description)와 자세한 지침을 담아 `skill.md` 작성
2. 필요한 의존성·참고 파일·실행 스크립트 추가
3. 폴더 이름을 스킬 이름과 똑같이 맞추기
4. 스킬 폴더를 루트로 하는 **ZIP 파일** 만들기
5. 설명이 명확한지 확인하고 참조한 파일이 모두 들어 있는지 점검
6. 예시 프롬프트로 미리 테스트
7. **Customize > Skills** 메뉴에서 스킬 켜기
8. Claude가 스킬을 제대로 불러오는지 확인(생각 과정 표시에서 확인 가능)
9. Claude가 스킬을 잘 호출하지 않으면 description을 다듬어 다시 시도

```
skill.md (예시 구조)
---
name: meeting-notes
description: 회의 녹취를 표준 양식으로 정리합니다
---

회의 내용을 받으면 안건·결정사항·할 일로 나누어 정리하세요.
```

{{< hint type="tip" >}}
좋은 스킬은 **반복되는 구체적인 작업**을 명확한 지침과 예시로 다룹니다. 스킬끼리는 자동으로 조합되지만 서로를 직접 호출하도록 지정할 수는 없습니다.
{{< /hint >}}

{{< hint type="warning" >}}
스킬 안에 API 키·비밀번호 같은 민감한 정보를 **직접 적어두지 마세요.** 외부 서비스 연결이 필요하면 자격 증명을 끼워넣는 대신 MCP 커넥터를 사용하세요. 또한 API 스킬은 실행 중에 추가 패키지를 설치할 수 없으므로 의존성을 미리 모두 준비해야 합니다.
{{< /hint >}}

## 플러그인이란 무엇인가요

플러그인(Plugin)은 **스킬·커넥터·서브 에이전트를 하나로 묶은 패키지**입니다. 특정 역할이나 팀, 회사에 맞게 Claude를 한 번에 맞춤 설정할 수 있어, 여러 스킬을 따로 설치하는 대신 통째로 가져올 수 있습니다.

- 사용 가능 요금제: **유료 요금제(Pro, Max, Team, Enterprise)**
- 사용 위치: **웹 채팅, Claude Desktop(Chat 탭), Claude Cowork**

### 플러그인이 묶어주는 것들

| 구성 요소 | 설명 | 작동 범위 |
|---|---|---|
| **스킬** | 작업 능력 확장 | 모든 플랫폼 |
| **커넥터** | Google Drive·Gmail·Slack·DocuSign 등 연결 | 모든 플랫폼 |
| **후크·서브 에이전트** | 자동화·역할 분담 | Cowork 전용(채팅에서는 비활성) |

### 설치 방법

1. 사이드바에서 **Customize 메뉴** 열기
2. **Plugins(플러그인)** 탭 선택
3. **Browse plugins(플러그인 둘러보기)** 클릭
4. 원하는 플러그인에서 **Install(설치)** 클릭

{{< hint type="warning" >}}
플러그인에는 컴퓨터의 다른 프로그램과 **같은 권한으로 실행되는 로컬 MCP 서버**가 포함될 수 있습니다. 반드시 **신뢰할 수 있는 출처**의 플러그인만 설치하세요.
{{< /hint >}}

{{< hint type="note" >}}
Team·Enterprise 관리자는 플러그인을 조직 전체에 배포·관리할 수 있습니다. 관리자가 배포한 관리형 플러그인은 개별 사용자가 수정할 수 없습니다.
{{< /hint >}}

## 한곳에서 둘러보기 — 통합 디렉터리

스킬·커넥터·플러그인을 메뉴마다 따로 찾을 필요 없이, **하나의 디렉터리**에서 모두 둘러보고 설치·관리할 수 있습니다.

1. Claude 또는 Claude Desktop 실행
2. 왼쪽 사이드바에서 **Customize** 선택
3. **Skills · Connectors · Plugins** 중 원하는 탭 선택
4. **'+' 버튼** 클릭 후 **Browse(둘러보기)** 선택
5. 스킬은 **Install**(설치 시 기본으로 켜짐), 커넥터는 **Connect**(인증 진행), 플러그인은 **Install**

{{< hint type="note" >}}
설치한 스킬은 **읽기 전용**으로 표시됩니다. 수정하려면 사본을 내려받아야 합니다. 또한 Team·Enterprise 요금제에서는 조직이 공유한 스킬이 'Your organization' 탭에 함께 나타납니다.
{{< /hint >}}

## 금융 서비스 플러그인 (Cowork 전용)

Claude Cowork에서는 재무 모델링, 주식 리서치, 투자은행, 사모펀드, 자산관리 같은 전문 업무를 위한 **오픈소스 금융 서비스 플러그인**을 쓸 수 있습니다. 이 플러그인들은 **Claude Cowork 모드에서만** 작동합니다.

### 설치 순서

1. **Claude Desktop** 앱 열기
2. 상단 선택기에서 **Cowork 모드**로 전환
3. 왼쪽 사이드바에서 **Customize** 선택
4. **Browse plugins > Personal** 클릭
5. **Add marketplace from GitHub** 선택
6. 저장소 주소 입력: `https://github.com/anthropics/financial-services-plugins`
7. **Financial Analysis(재무 분석)** 플러그인을 가장 먼저 설치(필수 기반)
8. 업무에 맞는 추가 플러그인(투자은행, 주식 리서치, 사모펀드, 자산관리) 설치
9. 설치한 플러그인은 자동으로 작동하거나 `/` 명령으로 관련 스킬 호출

설치 후에는 `/comps`, `/dcf`, `/earnings`, `/one-pager`, `/ic-memo`, `/source`, `/client-review` 같은 스킬을 쓸 수 있습니다.

{{< hint type="warning" >}}
AI가 생성한 재무 분석은 의사결정에 사용하기 전에 **반드시 전문가의 검토**를 거쳐야 합니다. 또한 데이터 연동을 위해 각 금융 데이터 제공사의 별도 구독이나 API 키가 필요할 수 있습니다.
{{< /hint >}}

## 다음 단계

- **[Projects 기능](/guide/chat/projects/)** — 자주 쓰는 지식과 파일을 주제별로 모아두기
- **[주요 기능 살펴보기](/guide/chat/features/)** — 파일 첨부, 이미지 분석 등 기본 기능
- **[요금제와 결제](/help/plans-billing/)** — 요금제별로 쓸 수 있는 기능 확인하기

## 원문 출처

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Browse skills, connectors, and plugins in one directory](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory)
- [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Install financial services plugins](https://support.claude.com/en/articles/13851150-install-financial-services-plugins)
