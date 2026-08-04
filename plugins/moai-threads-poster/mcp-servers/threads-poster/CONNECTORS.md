# Threads(Meta) 연동 가이드 — `moai-threads-poster` MCP

Threads 는 **OAuth 2.0** 으로 인증하며, 발행하려면 **장기 액세스 토큰(60일)** 이 필요하다.
본 MCP 서버는 사용자가 (브라우저로) 최초 1회 발급받은 장기 토큰을 환경변수로 받아 사용한다.

> 서버가 브라우저 인가를 대신 수행하지 않는다. 최초 1회는 아래 절차대로 수동 발급이 필요하다.
> 이후에는 `THREADS_ACCESS_TOKEN` / `THREADS_USER_ID` 환경변수만 세팅하면 된다.

---

## 1. 사전 요구사항

- **uv** 설치: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Meta 계정 + Threads 계정 (프로필은 공개 권장 — 토큰 갱신 기간 연장)
- 공식 문서: <https://developers.facebook.com/docs/threads>

## 2. Meta App 생성 — Threads 사용 사례

1. **Meta for Developers** (<https://developers.facebook.com/>) 접속 → **내 앱(My Apps)** → **앱 만들기(Create App)**.
2. 앱 유형은 **비즈니스(Business)** 권장. 앱 이름·연락처 이메일 입력 후 생성.
3. 앱 대시보드에서 **+ 제품/사용 사례 추가(Add Product / Use Case)** →
   **Threads** 사용 사례를 찾아 **설정(Set up)**.
4. Threads 설정 화면에서 **Threads API** 를 활성화하고 다음 값을 확보한다:
   - **App ID** (앱 ID)
   - **App Secret** (앱 시크릿 — 설정 → 기본 설정 에서 확인)
   - 필요 **권한(permissions)**: `threads_basic` (전 엔드포인트), `threads_content_publish` (발행)

> 앱이 **개발 모드(Development Mode)** 인 동안은 테스터로 등록된 Threads 계정만 API 호출 가능.
> 프로덕션 전면 공개는 Meta 앱 검수(App Review) 가 필요할 수 있다.

## 3. Threads 테스터 초대 (개발 모드)

1. 앱 대시보드 → **역할(Roles)** → **Threads 테스터(Threads Testers)** → **Threads 테스터 추가**.
2. Threads 사용자명(@username) 입력 → 초대 → 해당 계정에서 초대 수락.

## 4. 인가 코드 발급 (브라우저)

아래 URL 을 브라우저로 열고, 테스터 Threads 계정으로 로그인·동의하면
`redirect_uri` 로 `code=...` 가 전달된다.

```
https://www.threads.net/oauth/authorize
  ?client_id=<APP_ID>
  &redirect_uri=<REDIRECT_URI>
  &scope=threads_basic,threads_content_publish
  &response_type=code
```

- `redirect_uri` 는 앱 설정에 등록한 값과 정확히 일치해야 한다 (예: `https://localhost/callback`).
- `scope` 는 **쉼표로 구분** (Threads 전용 스코프 표기).
- 리다이렉트된 URL 의 `?code=XXXXX` 가 **인가 코드(authorization code)**.

## 5. 단기 액세스 토큰 발급 (1시간)

인가 코드를 단기 토큰으로 교환한다:

```bash
curl -X POST "https://api.threads.net/oauth/access_token" \
  -d "client_id=<APP_ID>" \
  -d "client_secret=<APP_SECRET>" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=<REDIRECT_URI>" \
  -d "code=<AUTHORIZATION_CODE>"
```

응답:

```json
{ "access_token": "<SHORT_LIVED_TOKEN>", "user_id": <THREADS_USER_ID> }
```

여기서 **`user_id` 가 `THREADS_USER_ID`** 다 (메모할 것).

## 6. 장기 액세스 토큰으로 교환 (60일)

단기 토큰(1h) 을 장기 토큰(60일) 로 변환한다:

```bash
curl "https://graph.threads.net/access_token"
  ?grant_type=th_exchange_token
  &client_secret=<APP_SECRET>
  &access_token=<SHORT_LIVED_TOKEN>
```

응답:

```json
{ "access_token": "<LONG_LIVED_TOKEN>", "token_type": "th_long_lived", "expires_in": 5184000 }
```

`expires_in` ≈ 5184000초(60일). 이 값이 `THREADS_ACCESS_TOKEN` 이다.

> **정책**: 단기 토큰 grant 는 **90일** 유효. 프로필이 공개면 장기 토큰을 60일 마다 갱신해
> 계속 연장할 수 있다. 비공개 프로필은 갱신이 제한될 수 있다.

## 7. (선택) 토큰 갱신 — 60일 연장

장기 토큰은 만료 전에 갱신하면 60일이 다시 연장된다. MCP 의 `threads_refresh_token`
도구를 호출하거나 아래 curl 직접 실행:

```bash
curl "https://graph.threads.net/refresh_access_token"
  ?grant_type=th_refresh_token
  &access_token=<LONG_LIVED_TOKEN>
```

## 8. 환경변수 설정

셸 프로필(`~/.zshrc` / `~/.bashrc`) 또는 Claude Code 환경에:

```bash
export THREADS_ACCESS_TOKEN="<LONG_LIVED_TOKEN>"
export THREADS_USER_ID="<THREADS_USER_ID>"
# 선택: 발행 전 대기(초), 기본 30
export THREADS_PUBLISH_DELAY="30"
```

`.mcp.json` 의 `env` 블록은 `${VAR}` 보간으로 이 환경변수를 서버에 전달한다.

## 9. 동작 확인 (smoke test)

서버가 도구를 노출하면 Claude Code 에서:

```
threads_get_profile
```

→ `{ "username": "...", "id": "...", "followers_count": N, ... }` 가 돌아오면 연동 성공.

## 10. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `setup_required` 에러 | 토큰/USER_ID 미설정 | `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID` export |
| HTTP 190 `OAuthException` | 토큰 만료 | `threads_refresh_token` 호출 후 토큰 갱신; 만료 시 4~6단계 재수행 |
| HTTP 4 / 10 `permission` | 스코프 부족 / 테스터 미등록 | `threads_content_publish` 스코프 + 테스터 초대 확인 |
| HTTP 613 `rate limit` | 24시간 250 포스트 초과 | 24시간 후 재시도 (M2 큐가 레이트리밋 관리 예정) |
| `text exceeds 500-byte` | 본문 500 UTF-8 바이트 초과 | 본문 줄이기 (이모지·한글은 멀티바이트) |
| 이미지/비디오 400 | URL 이 비공개 또는 스펙 초과 | 공개 URL 확인 (이미지 ≤8MB JPEG/PNG, 비디오 ≤1GB MOV/MP4 ≤5분) |

---

버전: 0.1.0 · API SSOT: <https://developers.facebook.com/docs/threads> · 문의: 모두의 AI
