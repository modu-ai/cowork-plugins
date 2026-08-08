# 유튜브 연동 — 자격증명 발급 절차

유튜브는 API 키만으로는 부족합니다. 업로드·라이브 방송·성과 조회·댓글 관리는 모두
**"내 계정으로 행동한다"** 는 뜻이라, 본인이 한 번 동의를 해 줘야 합니다. 그 동의의
결과물이 **리프레시 토큰**이고, 한 번 받으면 계속 쓸 수 있습니다.

한 번만 하면 되는 일이고, 순서대로 따라오시면 됩니다.

## 1. Google Cloud 프로젝트 만들기

1. [Google Cloud 콘솔](https://console.cloud.google.com/)에 유튜브 채널 계정으로 로그인
2. 상단의 프로젝트 선택 → **새 프로젝트** → 이름은 아무거나 (예: `내채널-mcp`)
3. 만든 프로젝트가 선택된 상태인지 확인

## 2. 필요한 API 켜기

**API 및 서비스 → 라이브러리** 에서 아래 둘을 찾아 각각 **사용** 을 누릅니다.

- `YouTube Data API v3` — 업로드·메타데이터·재생목록·댓글·라이브 방송
- `YouTube Analytics API` — 성과 조회

## 3. 동의 화면 설정

**API 및 서비스 → OAuth 동의 화면**

1. 사용자 유형은 **외부** 선택 (본인만 쓸 것이라도 외부입니다)
2. 앱 이름·지원 이메일만 채우면 됩니다
3. **범위(scope)** 단계에서 아래 넷을 추가합니다

```
https://www.googleapis.com/auth/youtube.readonly
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube.force-ssl
https://www.googleapis.com/auth/yt-analytics.readonly
```

`youtube.force-ssl` 이 댓글과 실시간 채팅에 필요합니다. 빠뜨리면 그 도구들만 권한
오류가 납니다.

4. **테스트 사용자** 에 본인 구글 계정을 추가합니다

앱을 게시(검수 요청)할 필요는 없습니다. 테스트 사용자로 남겨 두면 됩니다. 다만 이
상태에서는 리프레시 토큰이 **일주일 뒤 만료**되므로, 계속 쓰시려면 나중에 앱을
'프로덕션'으로 전환하세요(검수 없이 전환만 해도 만료가 풀립니다).

## 4. OAuth 클라이언트 만들기

**API 및 서비스 → 사용자 인증 정보 → 사용자 인증 정보 만들기 → OAuth 클라이언트 ID**

- 애플리케이션 유형: **데스크톱 앱**
- 만들고 나면 **클라이언트 ID** 와 **클라이언트 보안 비밀번호** 가 나옵니다. 이 둘을
  복사해 두세요 (`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`).

## 5. 리프레시 토큰 받기

브라우저에서 한 번 동의하고 그 결과를 토큰으로 바꾸는 단계입니다.

### 5-1. 동의 주소 열기

아래 주소의 `클라이언트ID` 자리에 4단계에서 받은 값을 넣고 브라우저에서 엽니다.
(한 줄로 붙여서 입력하세요.)

```
https://accounts.google.com/o/oauth2/v2/auth
  ?client_id=클라이언트ID
  &redirect_uri=http://localhost
  &response_type=code
  &access_type=offline
  &prompt=consent
  &scope=https://www.googleapis.com/auth/youtube.readonly%20https://www.googleapis.com/auth/youtube.upload%20https://www.googleapis.com/auth/youtube.force-ssl%20https://www.googleapis.com/auth/yt-analytics.readonly
```

`access_type=offline` 과 `prompt=consent` 가 리프레시 토큰을 받는 열쇠입니다. 빼면
액세스 토큰만 나오고 하루도 못 갑니다.

### 5-2. 코드 꺼내기

동의하면 `http://localhost/?code=4/0Ax...` 처럼 **접속 실패 화면**으로 넘어갑니다.
정상입니다. 주소창의 `code=` 뒤부터 `&` 앞까지가 인증 코드입니다.

### 5-3. 코드를 토큰으로 바꾸기

터미널에서 아래를 실행합니다. 세 자리(`클라이언트ID`·`시크릿`·`인증코드`)를 바꿔 넣으세요.

**macOS**

```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d client_id=클라이언트ID \
  -d client_secret=시크릿 \
  -d code=인증코드 \
  -d grant_type=authorization_code \
  -d redirect_uri=http://localhost
```

**Windows (PowerShell)**

```powershell
curl.exe -s -X POST https://oauth2.googleapis.com/token `
  -d client_id=클라이언트ID `
  -d client_secret=시크릿 `
  -d code=인증코드 `
  -d grant_type=authorization_code `
  -d redirect_uri=http://localhost
```

응답의 `refresh_token` 값이 우리가 찾던 것입니다. 인증 코드는 **한 번만** 쓸 수 있으니,
실패하면 5-1부터 다시 하세요.

## 6. 채널 ID 확인 (선택)

유튜브 스튜디오 → 설정 → 채널 → 고급 설정에 있습니다. `UC` 로 시작합니다.
지정하지 않아도 인증된 계정의 채널로 동작하지만, 계정에 채널이 여러 개면 지정하는
편이 안전합니다.

## 7. 값 넣기

`.mcp.json` 의 `env` 또는 시스템 환경변수에 넣습니다.

```
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
YOUTUBE_CHANNEL_ID=UC...      (선택)
```

## 8. 연결 확인 — 실제 API를 한 번 불러 봅니다

값을 넣었으면 **Claude/ChatGPT에 붙이기 전에 터미널에서 먼저 확인**하는 편이 좋습니다.
어디서 막혔는지 훨씬 명확하게 알려 주기 때문입니다.

`<플러그인경로>` 는 이 플러그인이 설치된 위치입니다
(보통 `~/.claude/plugins/moai-youtuber`).

**macOS**

```bash
cd <플러그인경로>/mcp-servers/moai-mcp-youtube

export YOUTUBE_CLIENT_ID="붙여넣기"
export YOUTUBE_CLIENT_SECRET="붙여넣기"
export YOUTUBE_REFRESH_TOKEN="붙여넣기"

uv run python -m moai_mcp_youtube.selftest
```

**Windows (PowerShell)**

```powershell
cd <플러그인경로>\mcp-servers\moai-mcp-youtube

$env:YOUTUBE_CLIENT_ID="붙여넣기"
$env:YOUTUBE_CLIENT_SECRET="붙여넣기"
$env:YOUTUBE_REFRESH_TOKEN="붙여넣기"

uv run python -m moai_mcp_youtube.selftest
```

**읽기만 합니다.** 아무것도 올리거나 바꾸지 않고, 할당량은 3 units 안쪽만 씁니다.

정상이면 이렇게 나옵니다.

```
유튜브 연결 확인을 시작합니다 (읽기 전용, 약 3 units 소모)

1) 자격증명 확인
  [OK] 세 값이 모두 설정돼 있습니다

2) 액세스 토큰 발급
  [OK] 토큰을 받았습니다

3) 채널 조회 (channels.list, 1 unit)
  [OK] 채널: 내 채널 이름
       구독자 1234 · 영상 56개

4) 내 영상 목록 (업로드 재생목록 경유, 2 units)
  [OK] 최근 영상 3개를 읽었습니다
       - 최근 영상 제목
...
연결 정상입니다.
```

**어느 단계에서 멈췄는지가 곧 원인입니다.**

| 멈춘 단계 | 원인 |
|---|---|
| 1) 자격증명 | 환경변수가 안 들어갔습니다. 같은 터미널 창에서 export 했는지 확인 |
| 2) 토큰 발급 | `access_type=offline`·`prompt=consent` 누락, 또는 동의 화면이 '테스트' 상태 |
| 3) 채널 조회 403 | YouTube Data API v3 가 꺼져 있거나 권한(scope) 부족 |
| 3) 채널 없음 | `YOUTUBE_CHANNEL_ID` 가 틀렸습니다. 비워 두면 인증 계정의 채널을 씁니다 |

여기까지 통과하면 Claude Cowork/ChatGPT Work에 붙였을 때도 동작합니다. 대화에서는
`youtube_channel_profile` 을 불러 다시 한 번 확인하시면 됩니다.

## 자주 막히는 곳

| 증상 | 원인과 해결 |
|---|---|
| `refresh_token` 이 응답에 없다 | `access_type=offline` 또는 `prompt=consent` 를 빠뜨렸습니다. 5-1부터 다시 |
| 일주일 뒤 갑자기 인증 실패 | 동의 화면이 '테스트' 상태입니다. '프로덕션'으로 전환하세요 |
| 댓글·채팅 도구만 권한 오류 | `youtube.force-ssl` 범위가 빠졌습니다. 3단계에서 추가 후 5단계 재실행 |
| `invalid_grant` | 인증 코드는 한 번만 쓸 수 있습니다. 5-1부터 다시 |
| 할당량이 금방 소진된다 | 검색이 1회 100 units입니다. `youtube_list_my_videos`(2 units)로 대체하세요 |

## 토큰은 어디에 저장되나

갱신된 토큰은 `~/.moai/mcp/youtube-tokens.json` 에 소유자 전용 권한으로 저장됩니다.
저장에 실패하는 환경이면 메모리에만 유지되고, 서버를 다시 켤 때 환경변수의 리프레시
토큰으로 복구합니다. 어느 쪽이든 서버는 멈추지 않습니다.

**이 파일과 자격증명을 저장소에 커밋하지 마세요.**
