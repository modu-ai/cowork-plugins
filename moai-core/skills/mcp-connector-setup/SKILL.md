---
name: mcp-connector-setup
description: |
  [책임 경계] Drive·Notion·Higgsfield 3커넥터 인증·환경변수·트러블슈팅 가이드 전담. 페어 moai-commerce:commerce-morning-brief(MCP 매장 데이터 호출)와 명확히 구분 — 본 스킬은 커넥터 설치·인증 단계, 페어는 인증 이후 실제 MCP 호출 결과물.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "MCP 커넥터 연결", "Drive 인증 방법", "Notion Integration Token 어디서", "Higgsfield 키 발급", "Windows MAX_PATH 오류", "한글 파일명 30자 오류", "computer:// 링크 안 열려요", "커넥터 3개 연결 방법", "MCP 3커넥터 인증", "커넥터 오류 해결".
user-invocable: true
version: 2.27.0
---

# MCP 커넥터 셋업 가이드

## 개요

Drive·Notion·Higgsfield 3커넥터를 Cowork에 연결하는 단계별 가이드를 제공합니다. 인증 흐름, API 키 입력, 1회 호출 검증, 트러블슈팅까지 셋업 전 과정을 다룹니다.

**셋업 완료 체크리스트**
Drive·Notion·Higgsfield — 인증 성공 + 1회 호출 성공 (Drive: 폴더 list / Notion: 공유 페이지 read / Higgsfield: 모델 list)

---

## 트리거 키워드

MCP 커넥터 연결, Drive 인증, Notion Integration Token, Higgsfield API 키, 3커넥터 설치, computer:// 링크, MAX_PATH 오류, 한글 파일명 오류, OAuth redirect URI

---

## 워크플로우

### Step 1 — 사전 준비물

커넥터 연결 전에 아래 계정을 미리 생성해 두세요:
- Google 계정 (Drive)
- Notion 계정
- Higgsfield 계정 + 워크스페이스 크레딧 충전

> **[HARD] API 키 보안 수칙**: API 키는 본인이 직접 발급·보관합니다. 채팅 대화나 공유 문서에 키 원문을 붙여넣지 말고, 커넥터 설정 화면의 API Key 필드에만 입력하세요.

---

### Connector A — Google Drive

**목적**: Cowork 폴더 마운트 + 파일 접근 (drive.readonly, drive.file 권한)

**인증 방법**: Cowork 앱 → 커넥터 추가 → Google Drive → OAuth 로그인

**필수 권한**
- `drive.readonly` — 파일 읽기
- `drive.file` — Cowork가 생성한 파일 접근

**인증 단계**
1. Cowork 앱 → 설정 → MCP 커넥터 → Google Drive 선택
2. "Google 계정으로 연결" 클릭
3. Google OAuth 화면에서 계정 선택 + 권한 허용
4. 연결 완료 후 Drive 폴더 list 1회 호출로 검증

**1회 호출 검증**: 폴더 목록이 응답에 나타나면 성공

---

### Connector B — Notion

**목적**: 작업 결과물 Notion 페이지 읽기·쓰기

**인증 방법**: Cowork 앱 → 커넥터 추가 → Notion → OAuth 인증

**인증 단계**
1. Cowork 앱 → 설정 → MCP 커넥터 → Notion 선택
2. "Notion으로 연결" 클릭
3. Notion OAuth 화면에서 워크스페이스 선택 + 페이지 접근 권한 허용
4. 연결 완료 후 공유 페이지 read 1회 호출로 검증

**1회 호출 검증**: 공유 페이지 내용이 응답에 나타나면 성공

---

### Connector C — Higgsfield

**목적**: 광고 영상 생성 등 미디어 작업 (이미지·영상 생성 모델 호출)

**인증 방법**: API 키 방식 (OAuth 아님)

**사전 확인 사항**
- Higgsfield 워크스페이스 크레딧 충전 여부 확인 (잔액 부족 시 인증은 성공해도 생성 호출이 실패할 수 있음)
- 예상 사용량 가늠: 영상 1편(5-10초) 기준 크레딧 소모량을 미리 확인
- 비용 한도: 워크스페이스 설정에서 사용 한도를 지정해 예상 외 과금 방지

**인증 단계**
1. Cowork 앱 → 설정 → MCP 커넥터 → Higgsfield 선택
2. API Key 필드에 발급받은 키 입력 (발급처: higgsfield.ai → API Keys)
3. 연결 완료 후 모델 list 1회 호출로 검증

**1회 호출 검증**: 사용 가능한 모델 목록이 응답에 나타나면 성공

---

## 트러블슈팅

### T1 — Windows MAX_PATH 260자 초과 오류

**증상**: Cowork 폴더 마운트 실패, 경로 관련 오류 메시지

**원인**: Windows 기본 MAX_PATH 260자 제한. 한글 파일명이 포함된 긴 경로에서 자주 발생.

**해결 방법**
1. 폴더를 드라이브 루트 가까운 위치로 이동 (예: `C:\cowork\` 또는 `D:\cw\`)
2. 한글 파일명 30자 룰: 폴더명·파일명을 30자 이내로 유지
3. 필요 시 Windows Registry로 MAX_PATH 제한 해제 (관리자 권한 필요)

**해결이 어려운 경우 (대체 경로)**: 위 방법으로 해결되지 않으면 로컬 폴더 마운트 대신 Google Drive 커넥터(Connector A)로 파일에 접근하는 임시 경로를 사용할 수 있습니다.

---

### T2 — `computer://` 링크 안 열림

**증상**: Cowork가 제공하는 `computer://` 링크를 클릭해도 열리지 않음

**해결 방법**
1. Chrome 시크릿 모드로 재시도
2. 브라우저 기본 프로토콜 핸들러 확인 (설정 → 기본 앱 → 링크 처리)
3. Cowork 앱 재시작 후 재시도

---

### T3 — OAuth 인증 실패 (Drive·Notion)

**증상**: OAuth 화면에서 "접근 거부" 또는 redirect 오류

**해결 방법**
1. Chrome 시크릿 모드에서 재시도 (캐시된 세션 충돌 방지)
2. Google 계정이 workspace 계정인 경우: 관리자 승인이 필요할 수 있음
3. OAuth redirect URI 문제: Cowork 앱 버전 업데이트 후 재시도
4. 팝업 차단 해제 확인 (브라우저 설정 → 팝업 허용)

---

### T4 — API 키 인증 실패 (Higgsfield)

**증상**: "Invalid API key" 또는 "Unauthorized" 오류

**해결 방법**
1. API 키 앞뒤 공백 없이 정확히 복사·붙여넣기 확인
2. Higgsfield: 워크스페이스 충전 여부 확인 (잔액 부족 시 인증 실패)
3. 키 재발급 후 재시도

---

## 슬래시 커맨드 등록 안내

커넥터 셋업을 마친 뒤, 프로젝트 CLAUDE.md에 아래와 같은 슬래시 커맨드를 등록하면 자주 쓰는 스킬을 빠르게 호출할 수 있습니다:

```markdown
## 슬래시 커맨드

- `/morning-brief` — 아침 브리핑 (commerce-morning-brief)
- `/detail-copy` — 상세페이지 카피 (detail-page-copy)
- `/channel-msg` — 채널 메시지 (commerce-channel-message)
```

프로젝트 폴더의 `CLAUDE.md`에 위 블록을 붙여넣어 등록합니다.

---

## 사전 점검 체크리스트 (`--check` 옵션)

사전 준비물 기준으로 3커넥터 가입·인증 상태를 체크하는 옵션입니다.

```
/mcp-connector-setup --check
```

출력 예시:
```
[✅] Google Drive — 계정 확인 완료
[✅] Notion — 계정 확인 완료
[⚠️] Higgsfield — 워크스페이스 크레딧 충전 미확인 (충전 후 재시도)
```

---

## 사용 예시

**예시 1**
> "Drive MCP 연결하는 방법 알려줘"

→ Connector A (Google Drive) 인증 단계 제공 + 1회 호출 검증 안내

**예시 2**
> "Windows에서 Cowork 마운트가 안 돼요"

→ T1 (MAX_PATH 오류) 해결 방법 제공 + 대체 경로 안내

---

## 출력 형식

- 단계별 인증 가이드 (Markdown)
- 트러블슈팅 해결 방법 (번호 목록)
- `--check` 옵션: 3커넥터 상태 체크리스트 (`.md` 파일 저장 가능)

---

## 셋업 완료 체크리스트

| 커넥터 | 인증 방법 | 1회 호출 검증 |
|--------|-----------|---------------|
| Google Drive | OAuth (drive.readonly, drive.file) | 폴더 list 응답 |
| Notion | OAuth (워크스페이스 연결) | 공유 페이지 read 응답 |
| Higgsfield | API Key | 모델 list 응답 |

3커넥터 모두 인증 성공 + 1회 호출 성공이면 셋업이 완료된 것입니다.

---

## 관련 스킬

- `moai-commerce:commerce-morning-brief` — 인증 완료 후 매장 데이터 아침 브리핑 + 신규 주문 통합 요약 (주문 요약 모드)
- `moai-media:higgsfield-image` / `moai-media:higgsfield-video` — Higgsfield 커넥터 인증 완료 후 이미지·영상 생성

---

## 이 스킬을 사용하지 말아야 할 때

- 이미 3커넥터가 모두 연결된 경우 → `moai-commerce:commerce-morning-brief` 직접 호출 (전체 브리핑 또는 주문 요약 모드)
- MCP 호출 결과물(아침 브리핑·주문 요약) 생성이 목적인 경우 → `moai-commerce` 스킬 사용
- Cowork 앱 설치 자체가 안 되는 경우 → Cowork 공식 지원 채널 문의 (본 스킬 범위 외)
- 광고 플랫폼 커넥터 (Meta 광고 등) 연결 → `moai-marketing:meta-ads-manager` 스킬 참조
