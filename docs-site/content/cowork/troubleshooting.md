---
title: "트러블슈팅"
weight: 120
description: "Claude Cowork 사용 중 자주 마주치는 문제(앱·로그인·폴더·플러그인·커넥터·세션·산출물)를 한 페이지로 정리합니다."
geekdocBreadcrumb: true
---

# Cowork 트러블슈팅

> Claude Cowork(Claude Desktop 앱의 Cowork 모드)에서 자주 발생하는 문제를 모았습니다. 스킬 체인 단계의 트러블슈팅은 [쿡북 — 트러블슈팅](../../cookbook/troubleshooting/), 시스템 한도 설명은 [제약과 한도](../constraints/)를 함께 보세요.

## 빠른 진단표

| 증상 | 점프 |
|---|---|
| 앱·로그인 문제 | [§1](#1-설치로그인) |
| 폴더·파일 시스템 | [§2](#2-작업-폴더파일-시스템) |
| `computer://` 안 열림 | [§3](#3-computer-링크가-안-열림) |
| 산출물 품질 | [§4](#4-산출물-품질-문제) |
| 스킬·플러그인 자동 호출 안 됨 | [§5](#5-스킬플러그인이-자동으로-호출-안-됨) |
| 플러그인 설치·업데이트 실패 | [§6](#6-플러그인-설치업데이트-실패) |
| 커넥터·MCP 연결 실패 | [§7](#7-커넥터mcp-연결-실패) |
| 세션·대화 끊김 | [§8](#8-세션대화-끊김) |
| 권한·인증 충돌 | [§9](#9-권한인증-충돌) |
| 회사 프록시·방화벽 | [§10](#10-회사-프록시방화벽) |

## 1. 설치·로그인

### 1-1. Claude Desktop 앱에 Cowork 메뉴가 안 보임

- 앱 버전이 Cowork 지원 버전인지 확인합니다. 메뉴 → "About Claude"에서 버전 확인 후 [공식 다운로드 페이지](https://support.claude.com/en/articles/10065433)에서 최신 빌드로 갱신
- 앱을 완전 종료 후 재실행 (메뉴 막대 → Quit, Windows는 시스템 트레이 → 종료)
- 로그인 계정의 요금제가 Cowork를 지원하는지 확인 — Pro·Max·Team·Enterprise. Free는 원칙적으로 미지원이며, 지역에 따라 순차 출시
- Team·Enterprise 사용자는 관리자가 Admin Settings → Capabilities에서 **Cowork를 활성화**했는지 확인

### 1-2. 로그인 후 빈 화면 또는 무한 로딩

- 시스템 시간이 정확한지 확인 (NTP 동기화) — 시계 오차로 OAuth 토큰이 거부될 수 있음
- VPN/프록시를 일시 해제하고 재시도
- 앱 캐시 삭제:
  - macOS: `~/Library/Application Support/Claude/`의 `Cache`/`Code Cache` 폴더 삭제
  - Windows: `%APPDATA%\Claude\`의 `Cache`/`Code Cache` 폴더 삭제
- 그래도 안 되면 앱 재설치 — 작업 폴더와 메모리는 보존됩니다 (계정 동기화)

## 2. 작업 폴더·파일 시스템

### 2-1. 폴더가 비어 보이거나 파일이 안 잡힘

- 작업 폴더 권한을 확인 — Cowork는 사용자가 명시적으로 선택한 폴더만 읽고 쓸 수 있습니다
- 폴더 안에 `.DS_Store`/`Thumbs.db` 외에 실제 파일이 있는지 확인
- 우측 상단 **폴더 아이콘**을 다시 눌러 폴더를 재선택 — 캐시 갱신
- macOS: 시스템 환경설정 → 개인정보 보호 → **파일 및 폴더**에서 Claude 항목의 폴더 권한 확인
- Windows: 파일 탐색기에서 해당 폴더 우클릭 → 속성 → 보안 탭에서 권한 확인

### 2-2. Windows에서 파일이 저장되지 않음 (MAX_PATH)

Windows는 기본 경로 길이 한계가 260자입니다. 한글 폴더명·긴 파일명이 결합되면 쉽게 초과합니다.

- 작업 폴더를 `C:\w\` 같은 짧은 경로로 옮깁니다
- 파일명을 한글 단어 1~2개(예: `보고서.docx`)로 유지
- 그래도 안 되면 그룹 정책에서 `LongPathsEnabled = 1`을 설정 (관리자 권한 필요, 모든 앱 호환은 아님)

### 2-3. macOS에서 파일을 못 찾음

- 폴더 권한 다이얼로그가 떴을 때 **허용**을 선택했는지 확인
- 시스템 환경설정 → 개인정보 보호 → 파일 및 폴더 → Claude 항목 토글 다시 켜기
- 외장 디스크의 경우 디스크 마운트 상태 확인

## 3. `computer://` 링크가 안 열림

`computer://`는 Cowork가 로컬 파일 경로를 대화창에서 열 수 있도록 만든 링크 프로토콜입니다.

- 첫 클릭 시 OS의 "기본 앱 선택" 다이얼로그가 뜹니다 — Claude Desktop 앱을 선택
- macOS에서 작동하지 않으면 Launch Services 캐시를 초기화:
  ```bash
  /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
  ```
- Windows에서 작동하지 않으면 레지스트리 `HKCR\computer`가 등록되어 있는지 확인 — 앱 재설치로 복구
- 폴더 탐색기에서 직접 파일을 열어도 같은 결과를 얻을 수 있습니다

## 4. 산출물 품질 문제

### 4-1. 결과가 너무 길거나 부정확함

요청에 제약 조건을 명시합니다.

- "한 페이지로 줄여줘"
- "숫자만 정확히 뽑아줘"
- "주요 5개만 표로 정리"

### 4-2. AI 어투가 남음

체인 마지막에 `moai-core:ai-slop-reviewer`가 호출되지 않은 경우입니다. 후속 메시지로 명시합니다.

{{< terminal title="claude — cowork" >}}
"방금 결과물을 ai-slop-reviewer로 한 번 더 다듬어줘."
{{< /terminal >}}

### 4-3. 한글 폰트가 깨진 PPT/Word

- `moai-office` 플러그인이 설치되어 있는지 확인 — 좌측 사이드바 → 사용자 지정 → 설치 목록
- 시스템에 한국어 폰트(Pretendard, Noto Sans KR, 맑은 고딕)가 설치되어 있는지 확인 — 일부 PPT/HWPX는 시스템 폰트를 임베드
- HWPX(한글)는 별도 의존성이 필요 — `moai-office` 페이지의 안내 참고
- PDF는 `moai-office:pdf-writer`가 Noto Sans CJK를 자동 다운로드하므로 별도 폰트 설치 불필요

## 5. 스킬·플러그인이 자동으로 호출 안 됨

증상이 가장 흔한 영역이라 원인을 4가지로 분리해 점검합니다.

### 5-1. 트리거 키워드가 약함

스킬은 자연어 요청과 SKILL 설명의 매칭으로 호출됩니다. 요청문에 도메인 키워드를 명시하는 것이 가장 확실합니다.

- "사업계획서", "NDA 검토", "카드뉴스" 같은 **도메인 키워드**를 포함
- 그래도 안 되면 명시적 호출: "**반드시 strategy-planner 스킬을 사용해서 만들어줘**"
- 일부 스킬은 슬래시로 직접 부를 수 있음 — 좌측 명령 팔레트에 노출되는 경우

### 5-2. moai-core가 미설치

`moai-core`에는 도메인 라우터·AI 슬롭 검수기가 포함됩니다. 다른 플러그인만 설치하고 라우터가 없으면 자동 체이닝이 약해집니다.

- 사용자 지정 → 설치 목록에서 **moai**(코어)가 활성화되어 있는지 확인
- 누락되어 있다면 설치 후 새 대화에서 다시 시도

### 5-3. 같은 이름의 스킬이 여러 곳에 있음

여러 마켓플레이스를 추가했거나 조직(enterprise)·개인(personal)·프로젝트 레벨에 동일 이름 스킬이 있으면 한쪽이 가려질 수 있습니다.

- 사용자 지정 → 설치 목록에서 동일 이름 중복 확인
- 명시적으로 부르려면 "moai-content의 blog 스킬로 작성해줘"처럼 **플러그인 이름**을 같이 명시

### 5-4. 요청문이 너무 짧거나 모호

"이거 정리해줘"처럼 맥락이 부족하면 라우터가 어느 도메인 스킬을 부를지 결정하지 못합니다.

- **무엇을(주제) + 어디에(채널·포맷) + 누구를 위해(독자)** 세 요소를 포함
- 예: "네이버 블로그에 30대 직장인 대상 노션 활용법 2500자 글 써줘"

## 6. 플러그인 설치·업데이트 실패

### 6-1. 마켓플레이스 추가가 안 됨

- 마켓플레이스 URL 형식 확인 — 커뮤니티는 보통 `org/repo` 형식 (예: `modu-ai/cowork-plugins`)
- 회사 네트워크에서 GitHub가 차단된 경우 — IT 팀에 `github.com` 접근 요청 ([§10](#10-회사-프록시방화벽))
- Team·Enterprise: 관리자가 마켓플레이스 추가를 제한했을 수 있음 — 관리자에게 승인 요청

### 6-2. 설치 후 슬래시 명령·기능이 안 보임

- **앱을 완전 종료 후 재실행** — 일부 플러그인은 재기동 후 활성화
- 마켓플레이스 갱신: 사용자 지정 → 마켓플레이스 → cowork-plugins 옆 **갱신** 버튼
- 신규 버전이 적용되지 않으면 **플러그인 상세 페이지에 재진입**해 새 버전이 표시되는지 확인

### 6-3. 신버전 출시 후 신규 스킬이 안 나옴

cowork-plugins는 커뮤니티 마켓플레이스이므로 자동 업데이트가 OFF입니다. 사용자 측에서 직접 갱신해야 합니다.

{{< terminal title="claude — cowork" raw="true" >}}
사용자 지정 → 마켓플레이스 → cowork-plugins → 갱신
{{< /terminal >}}

그래도 신규 스킬이 안 나타나면 해당 플러그인을 **삭제 후 재설치**합니다.

## 7. 커넥터·MCP 연결 실패

### 7-1. 내장 커넥터(Google Drive·Gmail 등) 인증 실패

- OAuth 인증 창이 팝업 차단으로 닫힌 경우 — 브라우저 팝업 허용 후 재시도
- 회사 SSO 환경에서 Google Workspace 권한이 제한된 경우 — IT 관리자에게 Cowork 앱 승인 요청
- 토큰 만료: 커넥터 설정에서 **재인증** 또는 **연결 해제 → 재연결**

### 7-2. 사용자 지정 MCP 서버 추가 시 "연결 실패"

- MCP 서버 URL이 외부 접근 가능한지 확인 (curl/브라우저로 헬스체크)
- 인증 헤더 형식이 맞는지 확인 — 서비스 제공자 문서 참고
- HTTPS 인증서가 유효한지 확인 — 자체 서명 인증서는 차단될 수 있음
- 처음 보는 MCP는 **신뢰 출처에서만** 추가 ([제약과 한도 §5-2](../constraints/#5-커넥터와-mcp))

### 7-3. 커넥터가 응답하지 않음 (타임아웃)

- 큰 데이터 요청은 페이지 단위로 분할 — "Drive에서 이번 주 파일 10개만"
- 커넥터를 잠시 비활성화 후 재활성화로 세션 재시작
- 같은 서비스 커넥터를 여러 개 활성화한 경우 한쪽만 켜고 시도

## 8. 세션·대화 끊김

### 8-1. 긴 작업 중 응답이 자주 멈춤

대화가 길어지면 자동 압축이 발동해 일부 디테일이 요약됩니다. 압축 후에 결과 품질이 떨어지는 느낌이라면 다음을 시도하세요.

- **핵심 결과물(중간 파일·결정사항)을 작업 폴더에 저장**한 뒤 새 대화 시작
- 새 대화 시작 시 작업 폴더와 프로젝트 메모리가 그대로 유지되므로 맥락 손실 최소
- 1M 토큰 컨텍스트 모델이 가용한 플랜(Max/Team/Enterprise)이라면 더 긴 세션 가능

### 8-2. 자동 압축 후 결과 품질이 떨어짐

- 압축은 디테일을 요약하므로 정확도가 중요한 작업(법률 검토, 재무 계산)에는 압축 발생 전에 새 대화로 이전
- 자주 쓰는 지침은 [프로젝트와 메모리](../projects-memory/)에 고정해 매번 새 대화에서도 일관성 유지

### 8-3. 같은 프롬프트인데 다른 결과

- 모델은 비결정적이므로 동일 입력에도 결과가 약간 달라집니다
- 결과 일관성이 중요하면 **출력 형식을 명세**: "표 컬럼은 항상 [이름, 역할, 비고] 순서"
- 프로젝트 메모리에 출력 표준을 명시해두면 변동성이 줄어듭니다

## 9. 권한·인증 충돌

### 9-1. 로그인 상태인데 "다시 로그인하세요" 반복

- 캐시 손상 가능성 — 앱 캐시(§1-2)를 삭제 후 재로그인
- 동일 계정으로 여러 디바이스에 로그인한 경우 일부 환경에서 토큰 충돌 — 다른 디바이스에서 로그아웃 후 재시도
- macOS Keychain에 잔존 자격증명이 있을 수 있음 — 키체인 접근에서 "Claude" 항목 정리 후 재로그인

### 9-2. Team·Enterprise: 일부 기능이 회색 처리

조직 정책에 의해 비활성된 상태입니다. 가능한 항목:

- 특정 플러그인·커넥터 화이트리스트
- 외부 마켓플레이스 추가 금지
- 컴퓨터 사용(Computer Use) 비활성
- 데이터 export 제한

해결: 관리자에게 정책 변경 요청 또는 개인 계정에서 작업

## 10. 회사 프록시·방화벽

### 10-1. 회사 네트워크에서 Cowork 연결 실패

회사 네트워크에서 다음 도메인에 대한 HTTPS 접근이 필요합니다. IT 팀에 화이트리스트 등록을 요청하세요.

- `claude.ai`
- `api.anthropic.com`
- `support.claude.com`
- 사용 중인 마켓플레이스 호스팅 도메인 (커뮤니티 마켓플레이스는 보통 `github.com`)

### 10-2. TLS 검사 프록시(Zscaler·CrowdStrike) 환경

회사 루트 인증서가 OS의 신뢰 저장소에 등록되어 있어야 안정 동작합니다. IT 팀이 표준 절차를 안내해 줄 것입니다.

### 10-3. VPN 강제 환경에서 OAuth 콜백 실패

내장 커넥터 인증 시 OAuth 리다이렉트가 차단될 수 있습니다. IT 팀에 OAuth 도메인 허용을 요청하거나, VPN 일시 해제 후 인증 → 재연결을 시도하세요.

## 그래도 해결이 안 될 때

- 같은 증상의 [자주 묻는 질문](../faq/)부터 확인
- 시스템 한도(컨텍스트, 플랜 가용성, 권한 정책 등) 의심 시 [제약과 한도](../constraints/) 참조
- 플러그인·체인 레이어 문제라면 [쿡북 — 트러블슈팅](../../cookbook/troubleshooting/)으로 이동
- Anthropic 공식 지원: [support.claude.com](https://support.claude.com)
- 커뮤니티 마켓플레이스 이슈: [modu-ai/cowork-plugins Issues](https://github.com/modu-ai/cowork-plugins/issues) — 증상·OS·앱 버전·플러그인 목록을 함께 등록

---

### Sources

- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190)
- [Install Claude Desktop](https://support.claude.com/en/articles/10065433)
- [Use Cowork on Team and Enterprise plans](https://support.claude.com/en/articles/13455879)
- [Use plugins in Claude Cowork](https://support.claude.com/en/articles/13837440)
- [Manage plugins for your organization](https://support.claude.com/en/articles/13837433)
- [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166)
- [Use connectors to extend Claude's capabilities](https://support.claude.com/en/articles/11176164)
- [Customize Cowork with plugins (blog)](https://claude.com/blog/cowork-plugins)
- [Cowork research preview 공지](https://claude.com/blog/cowork-research-preview)
- [1M Context GA 공지](https://claude.com/blog/1m-context-ga)
- [Anthropic 지원센터](https://support.claude.com)
- [modu-ai/cowork-plugins Issues](https://github.com/modu-ai/cowork-plugins/issues)
