---
name: setup-mcp-connector
description: |
  [책임 경계] Drive·Notion·Higgsfield 3커넥터 인증·환경변수·트러블슈팅 가이드 전담. 페어 moai-seller:commerce-morning-brief(MCP 매장 데이터 호출)와 명확히 구분 — 본 스킬은 커넥터 설치·인증 단계, 페어는 인증 이후 실제 MCP 호출 결과물.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "MCP 커넥터 연결", "Drive 인증 방법", "Notion Integration Token 어디서", "Higgsfield 키 발급", "Windows MAX_PATH 오류", "한글 파일명 30자 오류", "computer:// 링크 안 열려요", "커넥터 3개 연결 방법", "MCP 3커넥터 인증", "커넥터 오류 해결".
version: "1.1.1"
---

# MCP 커넥터 셋업 가이드

## 개요

Drive·Notion·Higgsfield 3커넥터 + 한국 공공데이터·문서·법령 **5 MCP**(kordoc·dart·korean-stats·archhub·**korean-law**)를 Cowork에 연결하는 단계별 가이드를 제공합니다. 인증 흐름, API 키 입력, 1회 호출 검증, 트러블슈팅까지 셋업 전 과정을 다룹니다.

**셋업 완료 체크리스트**
- Drive·Notion·Higgsfield — 인증 성공 + 1회 호출 성공 (Drive: 폴더 list / Notion: 공유 페이지 read / Higgsfield: 모델 list)
- kordoc — Node.js 18+ 확인 + 1회 문서 파싱 성공 (키 불필요)
- dart(korean-dart-mcp) — Node.js 20.19+ + OpenDART 키 + 1회 공시 검색 성공
- korean-stats — 1회 자연어 통계 조회 성공 (키 불필요, 공용키 hosted)
- archhub — 1회 건축물 종합카드 조회 성공 (키 불필요, 공용키 hosted)
- korean-law — 법제처 OC 키 + 1회 법령 검색 성공 (law.go.kr 무료 발급, 사용자마다 키 필요)

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

## 한국 공공데이터·문서·법령 MCP (5종)

Cowork 플러그인은 한국 공공데이터·공문서·법령 처리를 위한 5개 MCP를 추가로 지원합니다. 각 MCP의 사전 준비와 1회 호출 검증을 다룹니다. chrisryugj 제작 5개 MCP는 모두 MIT 라이선스입니다.

### Connector D — kordoc (한국 공문서 파서)

**목적**: HWP 3.0/5.x·HWPX·HWPML·PDF·XLSX·DOCX → 마크다운 변환. 표 완벽 재현, 신구대조표, 양식 자동 채우기, DRM 배포용 복호화, OCR 연동. `moai-officer:doc-reader` 스킬이 호출.

**사전 준비물**: **API 키 불필요**. Node.js 18+만 필요.

**설치 단계**
1. Node.js 18+ 설치 확인: `node --version` (v18 이상이어야 함)
2. `.mcp.json`에 이미 등록됨(`command: npx`, `args: ["-y", "kordoc", "mcp"]`)
3. 첫 호출 시 npm이 kordoc 패키지를 다운로드(약 10-30초), 이후 캐시 적중

**1회 호출 검증**: 임의 HWP/PDF 파일로 `parse_document` 호출 → 마크다운 응답이 오면 성공

> Windows 환경에서 한컴 오피스가 설치된 경우 DRM 배포용 HWP/HWPX COM fallback이 추가로 동작합니다(선택).

---

### Connector E — dart / korean-dart-mcp (OpenDART 전자공시)

**목적**: OpenDART 83개 API를 15 도구로 압축. 공시·재무·지분·XBRL(`markdown_full` 전체 계정 + 계산 검증) + 버핏급 애널리스트 프레임(`insider_signal`·`disclosure_anomaly`·`buffett_quality_snapshot`) + HWP/PDF 첨부 마크다운화(kordoc 엔진) + 90일 자동분할. 회사명/종목코드/corp_code 자동 해결(SQLite FTS, 첫 기동 시 11.6만건 덤프 약 5-10초).

**사전 준비물**
- **Node.js 20.19+** (LTS 권장) — `node --version`으로 확인
- **OpenDART 인증키**(40자, 무료, 일 20,000건)

**인증 키 발급 절차**
1. https://opendart.fss.or.kr 접속 → 회원가입
2. 로그인 후 인증키 신청 → 이메일로 40자 인증키 즉시 수신
3. 환경변수 `DART_API_KEY`에 등록

**인증 단계**
1. 발급받은 40자 키를 `${CLAUDE_PLUGIN_DATA}/moai-credentials.env`의 `DART_API_KEY` 항목에 입력
2. 첫 기동 시 corp_code 덤프(11.6만건, 약 5-10초) 대기
3. 1회 호출 검증으로 `resolve_corp_code("삼성전자")` → corp_code 반환 확인

**1회 호출 검증**: 회사명으로 corp_code가 반환되면 성공

> **대안 — setup 마법사**: `npx -y korean-dart-mcp setup` 실행 시 대화형 마법사가 키 입력부터 클라이언트 설정 파일 자동 패치까지 처리(macOS/Linux/Windows 공용). Windows는 `cmd /c npx` 래핑 자동 적용.

> **주의**: 첫 기동에 5-10초가 걸리는 corp_code 덤프 다운로드 중이므로 timeout 여유를 두세요. `MODULE_NOT_FOUND` 에러 시 `npm uninstall -g korean-dart-mcp` 후 `npx -y korean-dart-mcp@latest setup`으로 재시도.

---

### Connector F — korean-stats (KOSIS 국가데이터처 통계)

**목적**: KOSIS 통계를 자연어 한 줄로 조회. 14도구, 92 키워드 + 100+ 자연어 별칭, 17 시도 + 230+ 자치구·시군 라우팅, 시계열 추세/순위, 출처(통계표 ID) 자동 인용, 추계/잠정치 구분. `moai-analyst:data-public`가 자연어 조회 우선 라우팅.

**사전 준비물**: **API 키 불필요**. 공용키가 탑재된 remote 커넥터(URL만 등록).

**설치 단계**
1. `.mcp.json`에 이미 등록됨(`type: http`, `url: https://mcp.gomdori.app/stats`)
2. 인터넷 연결만 있으면 바로 사용

**1회 호출 검증**: `quick_stats("광진구 고용률")` → 통계 수치 + 출처(통계표 ID) 응답 시 성공

> 자치구 단위 데이터가 KOSIS에 없으면 임의로 광역시도 값을 자치구 값인 척 답하지 않고 명시적으로 "광역시도 데이터로 대체했다"고 안내합니다. 동명 중복(부산 중구 vs 서울 중구)은 광역시를 같이 말해야 정확히 구분됩니다.

---

### Connector G — archhub (국토교통부 건축HUB)

**목적**: 건축물대장·건축인허가·주택인허가 + 법정동코드 + 한 필지 종합카드·층별 구성·동 단위 통계·노후건축물·철거멸실(석면)·인허가 파이프라인·공시가격 시계열. 11도구. `moai-analyst:data-building-ledger` 스킬이 호출.

**사전 준비물**: **API 키 불필요**. 공용키가 탑재된 remote 커넥터(URL만 등록).

**설치 단계**
1. `.mcp.json`에 이미 등록됨(`type: http`, `url: https://mcp.gomdori.app/archhub`)
2. 인터넷 연결만 있으면 바로 사용

**1회 호출 검증**: `find_region("광진구 자양동")` → sigungu_code/bdong_code 반환 후 `building_profile` 호출 → 종합카드 응답 시 성공

> archhub는 `[NOT_FOUND]`(데이터 없음)·`[EXTERNAL_API_ERROR]`(upstream 오류) 프리픽스로 환각을 차단합니다. data.go.kr 공식 API 실측값만 제공하며, 소유자 정보(개인정보)·위반건축물 조회는 범위 밖입니다.

---

### Connector H — korean-law (법제처 국가법령정보)

**목적**: 국가법령정보(법제처) 법령·판례·행정규칙·자치법규·조약·해석례(국세청) 원문 조회 + LLM 환각방지 인용검증(`verify_citations`) + 판례 생사(`cite_check`) + 행위시법(`applicable_law`) + 조문 영향그래프(`impact_map`). 42개 API → 9 도구. `moai-lawyer:legal-law-research` 스킬이 호출.

**사전 준비물**: **법제처 Open API OC 키(사용자마다 발급 필수, 공용키 아님 — stats/archhub와 상이)**. Node.js 불필요(hosted).

**발급 절차**
1. law.go.kr(또는 법제처 Open API 신청 페이지) 접속 → 회원가입·로그인
2. Open API 사용 신청 → 신청서 작성
3. OC 키 즉시 발급(무료)

**인증**: 환경변수 `KOREAN_LAW_OC` 등록(`.mcp.json`의 `url: https://mcp.gomdori.app/law?oc=${KOREAN_LAW_OC}`에 보간). 또는 `${CLAUDE_PLUGIN_DATA}/moai-credentials.env`의 `KOREAN_LAW_OC` 항목에 입력.

**1회 호출 검증**: `search_law(query="근로기준법")` → 법령 검색 응답 시 성공

> **주의**: 공용키 모덜이 아님(사용자마다 OC 키). 사내망·폐쇄망에서 법제처 API 인증서 검증 이슈 시 `LAW_API_PROTOCOL=http` fallback. 라이브 스킬: `moai-lawyer:legal-law-research`.

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
- `/detail-copy` — 상세페이지 카피 (commerce-detail-page-copy)
- `/channel-msg` — 채널 메시지 (cs-channel-message)
```

프로젝트 폴더의 `CLAUDE.md`에 위 블록을 붙여넣어 등록합니다.

---

## 사전 점검 체크리스트 (`--check` 옵션)

사전 준비물 기준으로 3커넥터 + 5 MCP 가입·인증·사전준비 상태를 체크하는 옵션입니다.

```
/setup-mcp-connector --check
```

출력 예시:
```
[✅] Google Drive — 계정 확인 완료
[✅] Notion — 계정 확인 완료
[⚠️] Higgsfield — 워크스페이스 크레딧 충전 미확인 (충전 후 재시도)
[✅] kordoc — Node.js 18+ 확인 (키 불필요)
[⚠️] dart — OpenDART 키 미등록 (opendart.fss.or.kr 발급 필요)
[⚠️] dart — Node.js 20.19+ 미충족 (현재 v18.x)
[✅] korean-stats — 공용키 hosted (키 불필요)
[✅] archhub — 공용키 hosted (키 불필요)
[⚠️] korean-law — 법제처 OC 키 미등록 (law.go.kr 무료 발급, 사용자마다 키 필요)
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

| 커넥터 / MCP | 인증 방법 | 1회 호출 검증 |
|--------|-----------|---------------|
| Google Drive | OAuth (drive.readonly, drive.file) | 폴더 list 응답 |
| Notion | OAuth (워크스페이스 연결) | 공유 페이지 read 응답 |
| Higgsfield | API Key | 모델 list 응답 |
| kordoc | 키 불필요 (Node.js 18+) | parse_document 마크다운 응답 |
| dart (korean-dart-mcp) | OpenDART 키 (40자, 무료/일 20,000건) | resolve_corp_code 응답 |
| korean-stats | 공용키 hosted (키 불필요) | quick_stats 통계 수치 응답 |
| archhub | 공용키 hosted (키 불필요) | find_region + building_profile 응답 |
| korean-law | 법제처 OC 키 (무료, 사용자마다 발급) | search_law 법령 검색 응답 |

3커넥터 + 5 MCP 모두 인증 성공 + 1회 호출 성공이면 셋업이 완료된 것입니다.

---

## 관련 스킬

- `moai-seller:commerce-morning-brief` — 인증 완료 후 매장 데이터 아침 브리핑 + 신규 주문 통합 요약 (주문 요약 모드)
- `moai-media:media-higgsfield-image` / `moai-media:media-higgsfield-video` — Higgsfield 커넥터 인증 완료 후 이미지·영상 생성
- `moai-officer:doc-reader` — kordoc MCP 인증 완료 후 HWP/HWPX/PDF/XLSX/DOCX 파싱
- `moai-analyst:data-public` — korean-stats MCP 자연어 KOSIS 통계 우선 라우팅 + dart MCP 연계
- `moai-analyst:data-building-ledger` — archhub MCP 건축물대장·인허가 실체 데이터 조회
- `moai-lawyer:legal-law-research` — korean-law MCP 법령·판례·인용검증·행위시법 조회

---

## 이 스킬을 사용하지 말아야 할 때

- 이미 3커넥터가 모두 연결된 경우 → `moai-seller:commerce-morning-brief` 직접 호출 (전체 브리핑 또는 주문 요약 모드)
- MCP 호출 결과물(아침 브리핑·주문 요약) 생성이 목적인 경우 → `moai-seller` 스킬 사용
- Cowork 앱 설치 자체가 안 되는 경우 → Cowork 공식 지원 채널 문의 (본 스킬 범위 외)
- 광고 플랫폼 커넥터 (Meta 광고 등) 연결 → `moai-marketer:marketing-meta-ads-manager` 스킬 참조
