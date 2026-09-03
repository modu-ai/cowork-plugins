# 아임웹(Imweb) 연동 가이드 — `moai-imweb` MCP

아임웹 OPEN API v3 는 **OAuth2 authorizationCode** 흐름으로 인증합니다. 이 MCP 서버는
사용자가 (브라우저로) 최초 1회 발급받은 **access token / refresh token** 을 환경변수로
받아 사용하며, access token 이 만료되면 **refresh token 으로 자동 갱신**합니다.

> 서버가 브라우저 인가를 대신 수행하지 않습니다. 최초 1회는 아래 절차대로 수동 발급이
> 필요합니다. 이후에는 `.mcp.json` env 만 세팅하면 됩니다.

---

## 1. 사전 요구사항

- **uv** 설치: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  (`uv run --directory ./mcp-servers/moai-mcp-imweb moai-mcp-imweb` 실행에 필요)
- 아임웹 계정 (계정이 소유한 사이트를 테스트 사이트로 사용)

## 2. 앱 등록 — 자격증명 발급

1. 아임웹 **개발자센터** 에 접속해 우측 상단 **[시작하기]** → 아임웹 계정으로 로그인.
2. 이용약관 · 개인정보처리방침 동의.
3. **앱 등록**: 앱 이름, **redirect URI**(예: `https://localhost/callback`), 사용 scope 선택.
4. 등록 완료 시 다음 값을 받는다 — 메모해 둘 것:
   - `clientId` (클라이언트 ID)
   - `clientSecret` (클라이언트 시크릿)
   - `siteCode` (연동할 테스트 사이트 코드)
   - `redirectUri` (등록한 리다이렉트 URI)

> 참고: 아임웹 정책상 **특정 고객/사이트 전용 서비스는 승인되지 않으며**, 연동된 테스트
> 사이트에 한해 API 호출이 가능합니다. 앱스토어 노출을 위해서는 아임웹과의 제휴 계약이
> 필요합니다.

## 3. 최초 1회 — authorization code 발급 (브라우저)

아래 URL 을 브라우저로 열고, 아임웹 계정으로 로그인하여 동의하면 `redirectUri` 로
`code=...` 쿼리 파라미터가 전달됩니다.

```
https://openapi.imweb.me/oauth2/authorize?
  responseType=code
  &clientId=<CLIENT_ID>
  &redirectUri=<REDIRECT_URI>
  &scope=site-info:read site-info:write member-info:read member-info:write product:read product:write order:read order:write community:read community:write promotion:read promotion:write payment:read payment:write script:read script:write statistics:read
  &state=<RANDOM_STRING>
  &siteCode=<SITE_CODE>
```

- `scope` 는 **공백으로 구분** (URL 인코딩 시 `%20`).
- `state` 는 CSRF 방지용 임의 문자열.
- 리다이렉트된 URL 에서 `?code=XXXXX` 의 `XXXXX` 가 **authorization code**.

## 4. access token / refresh token 발급

authorization code 로 토큰을 교환합니다 (POST, `application/x-www-form-urlencoded`):

```bash
curl -X POST https://openapi.imweb.me/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grantType=authorization_code" \
  --data-urlencode "code=<AUTHORIZATION_CODE>" \
  --data-urlencode "clientId=<CLIENT_ID>" \
  --data-urlencode "clientSecret=<CLIENT_SECRET>" \
  --data-urlencode "redirectUri=<REDIRECT_URI>" \
  --data-urlencode "siteCode=<SITE_CODE>"
```

응답에서 `accessToken` / `refreshToken` (또는 `access_token` / `refresh_token`) 획득.

> 아임웹은 camelCase 를 일관되게 사용합니다(`/oauth2/authorize` 파라미터가 모두
> camelCase). 본 MCP 서버는 응답 키를 camelCase · snake_case 양쪽으로 모두 허용합니다.

## 자격증명을 어디에 넣는가 (2026-09-03 갱신)

셸 환경변수만으로는 부족하다. **Claude 데스크톱·Codex CLI·Codex 데스크톱은 `.mcp.json` 의
`${KEY}` 를 확장하지 않고 문자열 그대로 서버에 넘긴다**(실측). 그래서 이 서버는 값을
아래 순서로 해석한다 — `moai_mcp_core/credentials.py`.

1. 실제 값이 든 환경변수 (자리표시자·빈 값은 없는 것으로 본다)
2. `~/.moai/mcp/imweb.json` — Windows 는 `C:\Users\<사용자>\.moai\mcp\imweb.json`
3. 없으면 기본값

파일 형식은 키와 값을 짝지은 JSON 객체 하나다:

```json
{
  "IMWEB_CLIENT_ID": "<클라이언트 ID>",
  "IMWEB_CLIENT_SECRET": "<클라이언트 시크릿>",
  "IMWEB_ACCESS_TOKEN": "<최초 발급 access token>",
  "IMWEB_REFRESH_TOKEN": "<최초 발급 refresh token>",
  "IMWEB_UNIT_CODE": "<유닛 코드>"
}
```

Claude 에서는 `.claude-plugin/plugin.json` 의 `userConfig` 선언에 따라 앱이 입력 폼을 띄우고
민감 항목을 키체인에 보관한다. 두 경로를 같이 써도 되며, 환경변수 쪽이 우선한다.

아래 환경변수 안내는 **개발 중 셸에서 직접 넣을 때**의 참고다.

## 5. `.mcp.json` env 설정

`plugins/moai-seller/.mcp.json` 의 `moai-imweb.env` 에 값을 채웁니다(값은 `${VAR}` 보간으로
셸 환경변수에서 읽어도 됩니다):

```jsonc
"env": {
  "IMWEB_CLIENT_ID":     "<CLIENT_ID>",
  "IMWEB_CLIENT_SECRET": "<CLIENT_SECRET>",
  "IMWEB_ACCESS_TOKEN":  "<ACCESS_TOKEN>",
  "IMWEB_REFRESH_TOKEN": "<REFRESH_TOKEN>",
  "IMWEB_UNIT_CODE":     "KRW"           // 선택: 다중 통화 사이트의 기본 unit 코드
}
```

선택 항목:
- `IMWEB_API_BASE` — 기본 `https://openapi.imweb.me`
- `IMWEB_TOKEN_FILE` — 토큰 영속화 경로(기본 `~/.moai/mcp/imweb-tokens.json`). 갱신된
  토큰을 디스크에 저장해 재시작 후에도 유지.
- `IMWEB_REQUEST_DELAY` — 요청 간 최소 간격(초, 기본 0). rate limit 회피용.

## 6. 자동 갱신 동작

- 모든 API 호출에 `Authorization: Bearer <access_token>` 주입.
- 응답이 `401` 이면(토큰 만료), 서버가 **1회** `POST /oauth2/token`
  (`grantType=refresh_token`) 으로 access token 을 재발급 후 원래 요청을 재시도.
- 갱신된 토큰은 `IMWEB_TOKEN_FILE`(지정 시) 에 저장.
- refresh token 까지 만료되면 갱신 실패 → 위 3~4단계를 다시 수행해 새 토큰을 발급.

## 7. 사용 가능한 scope (18)

`<domain>:read` / `<domain>:write` 쌍:

| 도메인 | read | write |
|---|---|---|
| site-info | 사이트 정보 조회 | 연동 정보·완료 처리 |
| member-info | 회원·그룹·등급 조회 | 회원 정보 수정·일괄변경 |
| product | 상품 조회 | 상품 등록·수정 |
| order | 주문 조회 | 주문 처리·송장·취소·교환·반품 |
| promotion | 적립금·쿠폰 조회 | 쿠폰 발급·적립금 지급/차감 |
| community | Q&A·구매평 조회 | 답변·구매평 등록/수정 |
| payment | 결제 정보 조회 | 무통장 입금 수동 확인 |
| script | 스크립트 조회 | 스크립트 등록·수정·삭제 |
| statistics | 통계 조회 | 통계 연동 |

## 8. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `토큰 갱신 불가` 에러 | client_id/secret/refresh_token 누락 | `.mcp.json` env 4종 모두 설정 |
| `토큰 갱신 실패` 반복 | refresh_token 만료 | 3~4단계 재수행으로 토큰 재발급 |
| `403` / scope 오류 | 등록한 scope 부족 | 앱 등록 시 누락된 scope 추가 후 재동의 |
| `GW.AUTHN` 401 지속 | access·refresh 동시 만료 | 토큰 재발급 |
| 페이징 누락 | `page`/`limit` 미지정 | 기본 단일 페이지; `imweb_*_list` 계열에 `page`/`limit` 전달 |

---

버전: 0.1.0 · 문의: 아임웹 고객지원 · API 스펙 SSOT: `https://developers-docs.imweb.me/reference/openapi.json`
