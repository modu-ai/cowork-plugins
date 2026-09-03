# CONNECTORS — 네이버 커머스(스마트스토어) MCP 인증

이 문서는 `moai-mcp-smartstore` 가 네이버 커머스 API 에 인증하기 위한 자격증명 발급·주입 절차를 설명한다.

## 사전 준비 — 자격증명 발급

1. **네이버 커머스 API 센터 가입** — https://apicenter.commerce.naver.com
2. **애플리케이션 등록** — 어드민 도구에서 애플리케이션 생성 후 아래 3가지 발급:
   - `client_id` — 애플리케이션 ID
   - `client_secret` — 애플리케이션 시크릿. **이 값 자체가 bcrypt salt** 로 사용된다(`$2a$10$...` 형식).
   - `account_id` — 판매자 계정 ID (`type=SELLER` 인증 시 필수)
3. **사용 권한 그룹** — 애플리케이션에 필요한 도메인(상품/주문/정산/...) 권한 부여.
4. **API데이터솔루션(통계) 사용 신청** — 통계 도구(`stats_*`)는 별도 사용 신청이 선행되어야 한다.

> 상세 가입/등록 절차는 공식 커머스API 소개·인증 문서 참고:
> https://apicenter.commerce.naver.com/docs/introduction · https://apicenter.commerce.naver.com/docs/auth

## 자격증명 주입 [HARD 보안 수칙]

자격증명은 코드·manifest·로그·채팅에 **하드코딩 절대 금지**. 아래 두 경로 중 하나로만 넣는다.

### 경로 1 — 자격증명 파일 (모든 실행 환경 공통, 권장)

`~/.moai/mcp/smartstore.json` (Windows: `C:\Users\<사용자>\.moai\mcp\smartstore.json`):

```json
{
  "NAVER_COMMERCE_CLIENT_ID": "<애플리케이션 ID>",
  "NAVER_COMMERCE_CLIENT_SECRET": "<애플리케이션 시크릿(bcrypt salt)>",
  "NAVER_COMMERCE_ACCOUNT_ID": "<판매자 계정 ID>",
  "NAVER_COMMERCE_TYPE": "SELF"
}
```

### 경로 2 — Claude 앱 입력 폼

`.claude-plugin/plugin.json` 의 `userConfig` 선언에 따라 Claude 데스크톱·CLI 가 플러그인을
켤 때 입력 폼을 띄우고, 민감 항목은 키체인에 보관한다. 값은 `${user_config.<KEY>}` 로
`.mcp.json` env 에 주입된다.

> **`.mcp.json` env 에 `${NAVER_COMMERCE_CLIENT_ID}` 같은 셸 변수 보간을 쓰지 말 것.**
> Claude 데스크톱·Codex CLI·Codex 데스크톱은 이 자리표시자를 확장하지 않고 문자열 그대로
> 서버에 넘긴다(2026-09-03 실측). 서버는 그런 값을 '설정되지 않음' 으로 판정하고 위 파일로
> 넘어간다 — `moai_mcp_core/credentials.py` 참조.

### 개발 중 환경변수로 넣기

셸에서 직접 export 한 값이 있으면 그것이 위 두 경로보다 우선한다.

**macOS / Linux**:

```bash
export NAVER_COMMERCE_CLIENT_ID="<애플리케이션 ID>"
export NAVER_COMMERCE_CLIENT_SECRET="<애플리케이션 시크릿(bcrypt salt)>"
export NAVER_COMMERCE_ACCOUNT_ID="<판매자 계정 ID>"   # type=SELLER 시 필수
export NAVER_COMMERCE_TYPE="SELF"                       # SELF(기본) | SELLER
# 선택
export NAVER_COMMERCE_BASE_URL="https://api.commerce.naver.com/external"
export NAVER_COMMERCE_TIMEOUT="30"
```

**Windows** (PowerShell):

```powershell
$env:NAVER_COMMERCE_CLIENT_ID = "<애플리케이션 ID>"
$env:NAVER_COMMERCE_CLIENT_SECRET = "<애플리케이션 시크릿(bcrypt salt)>"
$env:NAVER_COMMERCE_ACCOUNT_ID = "<판매자 계정 ID>"   # type=SELLER 시 필수
$env:NAVER_COMMERCE_TYPE = "SELF"                      # SELF(기본) | SELLER
# 선택
$env:NAVER_COMMERCE_BASE_URL = "https://api.commerce.naver.com/external"
$env:NAVER_COMMERCE_TIMEOUT = "30"
```

| 변수 | 필수 | 설명 |
|------|------|------|
| `NAVER_COMMERCE_CLIENT_ID` | O | 애플리케이션 ID |
| `NAVER_COMMERCE_CLIENT_SECRET` | O | 애플리케이션 시크릿 (bcrypt salt) |
| `NAVER_COMMERCE_ACCOUNT_ID` | type=SELLER 시 O | 판매자 계정 ID |
| `NAVER_COMMERCE_TYPE` | – | `SELF`(스토어 운영자 본인) \| `SELLER`(솔루션 개발자가 판매자 대행) |
| `NAVER_COMMERCE_BASE_URL` | – | API 게이트웨이(기본: 운영 URL) |
| `NAVER_COMMERCE_TIMEOUT` | – | HTTP 타임아웃 초(기본 30) |

### type 선택 기준

- **`SELF`** — 스토어 운영자가 **본인 스토어**를 직접 관리. `account_id` 불필요. (대부분의 셀러 자동화)
- **`SELLER`** — 솔루션 개발사가 **특정 판매자 계정**을 대행. `account_id` 필수.

## 인증 흐름 (본 MCP가 자동 처리)

1. 전자서명 생성: `signature = base64(bcrypt(client_id + "_" + timestamp_ms, client_secret))`
2. 토큰 발급: `POST /v1/oauth2/token` (form-encoded) → `access_token` + `expires_in`
3. 도메인 API 호출: `Authorization: Bearer {access_token}` 헤더 자동 주입
4. 토큰 만료(401 + `GW.AUTHN`) 감지 → 자동 재발급 후 1회 재시도

timestamp 는 밀리초 단위, 발급 시점 기준 5분 유효. 토큰은 만료 직전 자동 갱신(캐시).

## 연결 검증

```bash
# 1) 환경변수 설정 후 stdio 서버 기동
uvx moai-mcp-smartstore

# 2) MCP 클라이언트(Cowork/Claude)에서 첫 호출로 인증 검증
#    smartstore_test_connection  → GET /v1/seller/account 1회 호출
#    smartstore_config_status    → 자격증명 설정 상태(로컬, 비밀키 원문 제외)
```

`smartstore_test_connection` 이 `{"ok": true, "data": {계정 정보}}` 를 반환하면 인증·연결 성공.

## cowork 통합 등록

`plugins/moai-seller/.mcp.json` 의 `mcpServers` 에 stdio 서버로 등록:

```json
{
  "moai-smartstore": {
    "command": "uvx",
    "args": ["moai-mcp-smartstore"],
    "env": {
      "NAVER_COMMERCE_CLIENT_ID": "${NAVER_COMMERCE_CLIENT_ID}",
      "NAVER_COMMERCE_CLIENT_SECRET": "${NAVER_COMMERCE_CLIENT_SECRET}",
      "NAVER_COMMERCE_ACCOUNT_ID": "${NAVER_COMMERCE_ACCOUNT_ID}",
      "NAVER_COMMERCE_TYPE": "${NAVER_COMMERCE_TYPE}"
    }
  }
}
```

> 패키지가 PyPI 미배포 상태면 로컬 경로 실행으로 대체:
> `"command": "<venv>/bin/moai-mcp-smartstore"` 또는 `"command": "python", "args": ["-m", "moai_mcp_smartstore"]`.

## 보안 수칙 (HARD)

- API 키는 본인이 직접 발급·보관. 채팅·공유문서에 원문 붙여넣기 금지.
- `client_secret` 을 AI 도구 프롬프트에 입력 금지 (공식 AI 활용가이드 권고).
- `.env` 파일은 `.gitignore` 필수. 저장소 커밋 금지.
- 본 MCP는 `smartstore_config_status` 등 어떤 경로로도 비밀키 원문을 노출하지 않는다.
