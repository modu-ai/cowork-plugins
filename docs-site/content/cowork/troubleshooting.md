---
title: "트러블슈팅"
weight: 105
description: "Cowork 사용 중 자주 마주치는 폴더 권한, Windows 경로, 로그인, 파일 누락, computer:// 오류를 한 페이지로 정리합니다."
geekdocBreadcrumb: true
---

# Cowork 트러블슈팅

> Cowork 자체(앱·폴더·로그인·파일 시스템) 단계에서 자주 발생하는 문제를 모았습니다. 플러그인·체인 단계의 트러블슈팅은 [쿡북 — 트러블슈팅](../../cookbook/troubleshooting/)을 참고하세요.

## 1. 설치·로그인

### 1-1. 앱 설치 후 Cowork 모드가 보이지 않음

- Claude Desktop 앱 버전이 Cowork 지원 버전인지 확인합니다.
- 앱을 종료한 뒤 재실행합니다 (메뉴 막대 → Quit).
- 로그인 계정이 Cowork 사용 가능한 요금제(Free 포함, 일부 지역 제한)인지 확인합니다.

### 1-2. 로그인 후 빈 화면 또는 무한 로딩

- 시스템 시간이 정확한지 확인합니다 (NTP 동기화).
- VPN/프록시를 일시 해제합니다.
- 캐시를 삭제합니다: macOS는 `~/Library/Application Support/Claude/`, Windows는 `%APPDATA%\Claude\`의 `Cache`/`Code Cache` 폴더.

## 2. 작업 폴더·파일 시스템

### 2-1. 폴더가 비어 보이거나 파일이 안 잡힘

- 작업 폴더 권한을 확인합니다 — Cowork는 사용자가 명시적으로 선택한 폴더만 읽고 쓸 수 있습니다.
- 폴더 안에 `.DS_Store`, `Thumbs.db` 외에 실제 파일이 있는지 확인합니다.
- 폴더를 다시 선택해 캐시를 갱신합니다 (우측 상단 폴더 아이콘).

### 2-2. Windows에서 파일이 저장되지 않음 (MAX_PATH)

Windows는 기본 경로 길이 한계가 260자입니다. 한글 폴더명·긴 파일명이 결합되면 쉽게 초과합니다.

- 작업 폴더를 `C:\w\` 같은 짧은 경로로 옮깁니다.
- 파일명을 한글 단어 1~2개(예: `보고서.docx`)로 유지합니다.
- 그래도 안 되면 그룹 정책에서 `LongPathsEnabled = 1`을 설정합니다 (관리자 권한 필요).

### 2-3. macOS에서 파일을 못 찾음

- 폴더 권한 다이얼로그가 떴을 때 **허용**을 선택했는지 확인합니다.
- 시스템 환경설정 → 개인정보 보호 → 파일 및 폴더에서 Claude 항목의 폴더 권한을 확인합니다.

## 3. `computer://` 링크가 안 열림

`computer://`는 Cowork가 로컬 파일 경로를 대화창에서 열 수 있도록 만든 링크 프로토콜입니다.

- 첫 클릭 시 OS의 "기본 앱 선택" 다이얼로그가 뜹니다 — Claude Desktop 앱을 선택합니다.
- macOS에서 작동하지 않으면 `Launch Services` 캐시를 초기화합니다:
  ```bash
  /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user
  ```
- Windows에서 작동하지 않으면 레지스트리 `HKCR\computer`가 등록되어 있는지 확인합니다 — 앱 재설치로 복구됩니다.
- 폴더 탐색기에서 직접 파일을 열어도 같은 결과를 얻을 수 있습니다.

## 4. 산출물 품질 문제

### 4-1. 결과가 너무 길거나 부정확함

요청에 제약 조건을 명시합니다.

- "한 페이지로 줄여줘"
- "숫자만 정확히 뽑아줘"
- "주요 5개만 표로 정리"

### 4-2. AI 어투가 남음

마지막에 `moai-core:ai-slop-reviewer`를 호출하지 않은 경우입니다. 후속 요청으로 명시합니다.

```text
방금 결과물을 ai-slop-reviewer로 한 번 더 다듬어줘.
```

### 4-3. 한글 폰트가 깨진 PPT/Word

`moai-office`가 설치돼 있는지 확인합니다. Python 의존성 누락 시에도 발생할 수 있습니다.

```bash
pip install python-docx python-pptx openpyxl
```

(HWPX는 별도 패키지가 필요합니다 — `moai-office` 페이지 참고)

## 5. 스킬·플러그인이 자동으로 호출 안 됨

- `moai-core`가 설치돼 있는지 확인합니다 (라우터가 여기 들어 있음).
- 해당 도메인 플러그인이 설치돼 있는지 확인합니다 (`/plugin installed`로 점검).
- 요청문에 트리거 키워드가 있는지 확인합니다 — 각 플러그인 페이지의 "자동 호출 트리거" 표 참조.
- 그래도 안 호출되면 슬래시로 직접 부릅니다: `/blog`, `/contract-review` 등 (스킬에 `user-invocable: true`가 있는 경우).

## 6. 그래도 해결이 안 될 때

- 같은 증상의 [자주 묻는 질문](../faq/)부터 확인합니다.
- 플러그인·체인 레이어 문제라면 [쿡북 — 트러블슈팅](../../cookbook/troubleshooting/)으로 이동합니다.
- 그래도 막히면 [GitHub Issues](https://github.com/modu-ai/cowork-plugins/issues)에 증상·OS·앱 버전·플러그인 목록을 함께 등록해 주세요.

---

### Sources
- [Claude Cowork 지원 문서](https://support.claude.com)
- [modu-ai/cowork-plugins Issues](https://github.com/modu-ai/cowork-plugins/issues)
