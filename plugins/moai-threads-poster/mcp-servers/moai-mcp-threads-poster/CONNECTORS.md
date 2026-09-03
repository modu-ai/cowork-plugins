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

## 자격증명을 어디에 넣는가 (2026-09-03 갱신)

셸 환경변수만으로는 부족하다. **Claude 데스크톱·Codex CLI·Codex 데스크톱은 `.mcp.json` 의
`${KEY}` 를 확장하지 않고 문자열 그대로 서버에 넘긴다**(실측). 그래서 이 서버는 값을
아래 순서로 해석한다 — `moai_mcp_core/credentials.py`.

1. 실제 값이 든 환경변수 (자리표시자·빈 값은 없는 것으로 본다)
2. `~/.moai/mcp/threads.json` — Windows 는 `C:\Users\<사용자>\.moai\mcp\threads.json`
3. 없으면 기본값

파일 형식은 키와 값을 짝지은 JSON 객체 하나다:

```json
{
  "THREADS_ACCESS_TOKEN": "<LONG_LIVED_TOKEN>",
  "THREADS_USER_ID": "<THREADS_USER_ID>",
  "IG_ACCESS_TOKEN": "<선택: 인스타 동시 발행용>",
  "IG_USER_ID": "<선택: 인스타 계정 ID>"
}
```

Claude 에서는 `.claude-plugin/plugin.json` 의 `userConfig` 선언에 따라 앱이 입력 폼을 띄우고
민감 항목을 키체인에 보관한다. 두 경로를 같이 써도 되며, 환경변수 쪽이 우선한다.

아래 환경변수 안내는 **개발 중 셸에서 직접 넣을 때**의 참고다.

## 8. 환경변수 설정

**macOS / Linux** — 셸 프로필(`~/.zshrc` / `~/.bashrc`)에:

```bash
export THREADS_ACCESS_TOKEN="<LONG_LIVED_TOKEN>"
export THREADS_USER_ID="<THREADS_USER_ID>"
export THREADS_PUBLISH_DELAY="30"   # 선택: 발행 전 대기(초), 기본 30
```

**Windows** — PowerShell 프로필(`$PROFILE`)에, 또는 영구 설정하려면 `setx`:

```powershell
$env:THREADS_ACCESS_TOKEN = "<LONG_LIVED_TOKEN>"
$env:THREADS_USER_ID = "<THREADS_USER_ID>"
$env:THREADS_PUBLISH_DELAY = "30"   # 선택: 발행 전 대기(초), 기본 30
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
| HTTP 613 `rate limit` | 24시간 250 포스트 초과 | 24시간 후 재시도 |
| `text exceeds 500-byte` | 본문 500 UTF-8 바이트 초과 | 본문 줄이기 (이모지·한글은 멀티바이트) |
| 이미지/비디오 400 | URL 이 비공개 또는 스펙 초과 | 공개 URL 확인 (이미지 ≤8MB JPEG/PNG, 비디오 ≤1GB MOV/MP4 ≤5분) |

---

# Instagram 연동 가이드 (Facebook Login for Business)

Instagram Graph API 는 Threads 와 다른 인증 경로를 쓴다 — **Facebook Login for Business** 로
Facebook Page 장기 액세스 토큰을 발급받아 `graph.facebook.com` 호스트를 호출한다 (Threads 의
`graph.threads.com` OAuth2 흐름과 상이). 자격증명은 Threads 쌍과 *독립적인* `IG_ACCESS_TOKEN` /
`IG_USER_ID` 환경변수로 전달한다.

> **Instagram Professional(Business 또는 Creator) 계정만 지원.** Personal 계정은 Graph API 로
> 발행할 수 없다. 발급 전에 Instagram 계정을 Professional 로 전환해야 한다.

> **스케줄링 참고 (REQ-INST-009)**: Instagram Graph API 는 서버 측 스케줄링 파라미터가 없다.
> 본 플러그인은 `instagram_publish_image/video/reel` 로 세션 안에서 즉시 발행만 한다.
> 예약·정기 발행은 Claude Cowork 이 담당한다 (백그라운드 자동 발행 없음).

공식 문서: <https://developers.facebook.com/docs/instagram-api> (Content Publishing 섹션).

## I-1. 사전 요구사항

- **uv** 설치 (위 1절 참조).
- **Instagram Professional 계정** (Business 또는 Creator). Personal 은 불가.
- **Facebook Page** — Instagram 계정이 해당 Page 에 연결되어 있어야 한다.
- Threads 연동과 *같은 Meta App* 을 재사용해도 되고, 별도 App 을 만들어도 된다.

## I-2. 필요 권한(permissions)

Meta App 에 다음 권한을 추가한다 (App Review 필요):

| 권한 | 용도 |
|---|---|
| `instagram_basic` | 기본 베이스라인 |
| `instagram_content_publish` | 2단계 발행(container → media_publish) |
| `pages_read_engagement` | 발행에 필요 |
| `pages_show_list` | Page 해석(setup) |
| `manage_comments` | 댓글 모더레이션(`instagram_comments_*`) — 선택 |
| `manage_insights` | 인사이트(`instagram_insights`) — 선택 |

## I-3. Facebook Login for Business 로 장기 Page 토큰 발급

1. Meta App 대시보드 → **Facebook Login for Business** 제품 추가(없으면).
2. 유효한 OAuth 리다이렉트 URI 등록.
3. 브라우저 인가 흐름으로 사용자 액세스 토큰을 발급받는다 (`pages_show_list`,
   `pages_read_engagement`, `instagram_basic`, `instagram_content_publish` 스코프 포함).
4. 단기 사용자 토큰을 **장기 Page 액세스 토큰**으로 교환한다:

```bash
# 1) 단기 사용자 토큰 → 장기 사용자 토큰 (60일)
curl "https://graph.facebook.com/v23.0/oauth/access_token" \
  -d "grant_type=fb_exchange_token" \
  -d "client_id=<APP_ID>" \
  -d "client_secret=<APP_SECRET>" \
  -d "fb_exchange_token=<SHORT_USER_TOKEN>"

# 2) 장기 사용자 토큰 → 장기 Page 토큰 (Page 권한이 포함된 비만료 토큰)
curl "https://graph.facebook.com/v23.0/me/accounts?access_token=<LONG_USER_TOKEN>"
# → { "data": [ { "access_token": "<PAGE_LONG_TOKEN>", "id": "<PAGE_ID>", ... } ] }
```

`PAGE_LONG_TOKEN` 이 **`IG_ACCESS_TOKEN`** 이다 (Instagram 발행에 쓰이는 것은 Page 토큰이다).

> Graph API 버전 `v23.0` 은 2026-06-30 기준 pin 값이다 (런타임에 중앙화된
> `GRAPH_API_VERSION` 상수로 관리 — 버전 drift 시 해당 상수 한 줄만 수정).

## I-4. `IG_USER_ID` 해석 (instagram_business_account)

Instagram 계정 ID 는 Page 에서 조회한다:

```bash
curl "https://graph.facebook.com/v23.0/me/accounts?fields=instagram_business_account&access_token=<PAGE_LONG_TOKEN>"
# → { "data": [ { "instagram_business_account": { "id": "<IG_USER_ID>" }, "id": "<PAGE_ID>" } ] }
```

여기서 `instagram_business_account.id` 가 **`IG_USER_ID`** 다 (API 경로의 `/{ig-user-id}/...` 에
쓰인다). 이 값은 Instagram Professional 계정만 반환된다 (Personal 은 필드가 비었다 → 계정 전환 필요).

## I-5. PPA (Page Publishing Authorization) — 필요 시

Meta 정책에 따라 발행 전 **Page Publishing Authorization** 완료가 요구될 수 있다. PPA 미완료 시
발행이 거부되며, 이 경우 Meta Business Suite 에서 PPA 를 완료한 뒤 재시도한다.

## I-6. 환경변수 설정

**macOS / Linux**:

```bash
export IG_ACCESS_TOKEN="<PAGE_LONG_TOKEN>"
export IG_USER_ID="<instagram_business_account ID>"
```

**Windows** (PowerShell):

```powershell
$env:IG_ACCESS_TOKEN = "<PAGE_LONG_TOKEN>"
$env:IG_USER_ID = "<instagram_business_account ID>"
```

`.mcp.json` 의 `env` 블록이 `${IG_ACCESS_TOKEN}` / `${IG_USER_ID}` 보간으로 서버에 전달한다.

## I-7. 동작 확인 (smoke test)

```
instagram_get_profile
```

→ `{ "username": "...", "id": "...", "followers_count": N, "media_count": N }` 가 돌아오면 연동 성공.

## I-8. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| `setup_required` 에러 | `IG_ACCESS_TOKEN`/`IG_USER_ID` 미설정 | 두 환경변수 export (Threads 쌍과 별개) |
| Personal 계정 오류 | Personal 계정은 Graph API 미지원 | Instagram Professional(Business/Creator) 로 전환 |
| `instagram_business_account` 가 비었음 | Page-IG 연결 안 됨 | Meta Business Suite 에서 Instagram 을 Page 에 연결 |
| PPA 미완료 오류 | Page Publishing Authorization 필요 | Meta Business Suite 에서 PPA 완료 후 재시도 |
| 이미지 PNG 거부 | Instagram 은 JPEG-only | JPEG 변환 후 재시도 (Threads 와 상이) |
| HTTP 24h 한도 | 100건/24h (media_publish 50) 초과 | 24h 후 재시도 |

---

버전: 0.2.0 · API SSOT: Threads <https://developers.facebook.com/docs/threads> · Instagram <https://developers.facebook.com/docs/instagram-api> · 문의: 모두의 AI
