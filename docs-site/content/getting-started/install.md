---
title: "설치 가이드"
weight: 10
description: "Claude Desktop에 MoAI Cowork Plugins을 설치하는 전체 과정 단계별 안내"
geekdocBreadcrumb: true
---

# 설치 가이드

이 가이드는 MoAI Cowork Plugins을 Claude Desktop에 설치하는 전체 과정을 단계별로 상세히 안내합니다. 5분 이내에 모든 설치를 완료할 수 있습니다.

## 전체 설치 절차

### 1단계: Claude Desktop 다운로드

{{< hint "note" >}}
**시스템 요구사항**
- macOS 10.13 이상
- Windows 10 이상
- 8GB 이상 RAM
- 안정적인 인터넷 연결
{{< /hint >}}

공식 사이트에서 Claude Desktop을 다운로드합니다:

1. [claude.com/download](https://claude.com/download) 접속
2. 운영체제에 맞는 버전 다운로드
3. 다운로드된 파일 실행하여 설치 진행

### 2단계: Anthropic 계정 로그인

Claude Desktop을 실행하고 Anthropic 계정으로 로그인합니다:

1. Claude Desktop 애플리케이션 실행
2. 로그인 화면에서 Anthropic 계정 정보 입력
3. 2단계 인증이 설정된 경우 인증 코드 입력

{{< hint "warning" >}}
**중요**: 개인 계정 또는 조직 계정 모두 사용 가능하지만, 조직 계정의 경우 관리자 승인이 필요할 수 있습니다.
{{< /hint >}}

### 3단계: Cowork 모드 활성화

Cowork 모드를 활성화하여 플러그인 사용이 가능한 환경을 설정합니다:

1. Claude Desktop 왼쪽 사이바에서 **"Projects"** 선택
2. "Cowork mode"가 표시되지 않으면 설정 메뉴에서 활성화
3. Cowork 모드가 활성화되면 추가 기능 탭이 표시됩니다

### 4단계: 로컬 작업 폴더 연결

사용할 작업 폴더를 Claude Desktop에 연결합니다:

1. "Connect a local work folder" 버튼 클릭
2. 작업할 프로젝트 폴더 선택
3. 연결 확인 완료

{{< hint "tip" >}}
**팁**: 기존 프로젝트 폴더를 연결하거나 새로운 폴더를 생성하여 사용할 수 있습니다.
{{< /hint >}}

### 5단계: 마켓플레이스 추가

MoAI Cowork Plugins 마켓플레이스를 추가합니다:

1. 상단 메뉴에서 **"Marketplace"** 선택
2. "Add marketplace" 버튼 클릭
3. 마켓플레이스 URL 입력: `modu-ai/cowork-plugins`
4. 추가 확인

### 6단계: 필수 플러그인 설치

가장 먼저 `moai-core` 플러그인을 설치합니다:

1. 마켓플레이스에서 **"moai-core"** 검색
2. "Install" 버튼 클릭
3. 설치 완료까지 기다림

{{< hint "note" >}}
**필수 플러그인**: `moai-core`는 `/project init`과 `ai-slop-reviewer` 스킬을 포함한 핵심 기능을 제공하므로 반드시 먼저 설치해야 합니다.
{{< /hint >}}

## 설치 검증

설치가 완료되었는지 다음과 같이 확인합니다:

### 1. 플러그イン 목록 확인

1. Claude Desktop에서 **"Plugins"** 탭 선택
2. 설치된 플러그인 목록에서 `moai-core` 확인
3. 상태가 "Active"로 표시되는지 확인

### 2. 스킬 테스트

간단한 명령어로 설치를 테스트합니다:

1. Cowork 모드에서 채팅창 열기
2. `/project init` 입력 후 실행
3. 7단계 인터뷰가 정상적으로 진행되는지 확인

## 문제 해결

### 자주 발생하는 문제

**Q: 마켓플레이스가 표시되지 않아요**
A: Claude Desktop 최신 버전인지 확인하고, 인터넷 연결 상태를 점검하세요.

**Q: moai-core 설치 실패**
A: 조직 계정 사용 시 관리자 승인이 필요할 수 있습니다. 관리자에게 문의하세요.

**Q: `/project init` 명령어가 작동하지 않아요**
A: moai-core 플러그인이 먼저 설치되었는지 확인하세요. 설치 순서가 중요합니다.

**Q: 스킬 목록이 나타나지 않아요**
A: Claude Desktop을 재시작하거나, 캐시를 초기화해보세요.

### 고급 문제 해결

**네트워크 문제**
- 프록시 설정 확인
- 방화벽에서 Claude Desktop 허용 목록 추가
- DNS 캐시 재시도

**권한 문제**
- 작업 폴더 읽기/쓰기 권한 확인
- macOS 보안 설정에서 Claude Desktop 권한 부여
- Windows Defender 실행 허용

## 다음 단계

설치가 완료되었다면 이제 첫 작업을 진행할 준비가 되었습니다:

- [첫 작업 가이드](../first-task/) - 5분 만에 완료할 실습 예제
- [빠른 시작 가이드](../quick-start/) - 주요 스킬 빠르게 숙지하기

### Sources
- GitHub 저장소: [https://github.com/modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- Claude Desktop 다운로드: [https://claude.com/download](https://claude.com/download)
- 온라인 문서: [https://cowork.mo.ai.kr](https://cowork.mo.ai.kr)