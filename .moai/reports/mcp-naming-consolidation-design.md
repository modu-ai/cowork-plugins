# 자체 제작 MCP — 작명 통일 · 공통 코어 통합 설계서

> 작성 2026-08-08 · 정본. 자체 제작 MCP 서버의 이름 규칙과 코드 통합 방향, 그리고 신규
> `moai-youtube` 서버의 구현 계약을 확정한다. 원칙 요약본은 `CLAUDE.local.md`
> §자체 제작 MCP 작명·구조 규칙 / §범용성 원칙에 있고, 이 문서가 근거와 상세를 담는다.

## 1. 전수조사 결과 (실측)

`plugins/*/.mcp.json` 전부와 `plugins/*/mcp-servers/` 를 실측했다.

### 1-1. 자체 제작 서버

| 서버 키 | 소속 플러그인 | 디렉터리 | 배포 패키지 | 모듈 | 엔트리포인트 | 등록 도구 | 코드량 |
|---|---|---|---|---|---|---|---|
| `moai-smartstore` | moai-seller | `moai-smartstore` | `moai-smartstore-mcp` | `moai_smartstore` | `moai-smartstore-mcp` | 93 | 1,323줄 |
| `moai-imweb` | moai-seller | `moai-imweb` | `moai-imweb-mcp` | `moai_imweb` | `moai-imweb-mcp` | 10 | 1,650줄 |
| `moai-cafe24` | moai-seller | `moai-cafe24` | `moai-cafe24-mcp` | `moai_cafe24` | `moai-cafe24-mcp` | 4(디스패치형) | 3,133줄 |
| `moai-threads-poster` | moai-threads-poster | `threads-poster` ❌ | `moai-threads-poster-mcp` | `threads_poster` ❌ | `threads-poster-mcp` ❌ | 17 | 1,625줄 |

커머스 3종은 5축이 이미 정합하다. **어긋난 것은 threads-poster의 3축**(디렉터리·모듈·엔트리포인트)뿐이다.

### 1-2. 제3자 서버 (이름 변경 대상 아님)

| 서버 키 | 소속 | 출처 |
|---|---|---|
| `higgsfield` | media · designer · story | Higgsfield AI 원격 MCP |
| `ElevenLabs` | media | ElevenLabs 공식 MCP |
| `meta-ads` · `wordpress` · `typefully` · `post-bridge` | marketer | 각 서비스 공식/상용 원격 MCP |
| `dart` · `kordoc` · `korean-stats` · `archhub` | accountant · officer · analyst · coworker | chrisryugj, MIT 오픈소스 |
| `context7` | 저장소 루트(개발용) | Upstash 공식 |

제3자 서버는 **원저작자 이름을 그대로 유지**한다. 개명하면 출처 추적이 끊긴다. 대신 온라인
문서의 오픈소스 크레딧 페이지(`www/content/plugins/open-source.md`)에 전부 등재한다.

## 2. 작명 규칙 (5축)

| 축 | 규칙 | 예 |
|---|---|---|
| `.mcp.json` 서버 키 | `moai-<서비스>` | `moai-youtube` |
| 디렉터리 | `mcp-servers/moai-<서비스>` | `mcp-servers/moai-youtube` |
| 배포 패키지명 | `moai-<서비스>-mcp` | `moai-youtube-mcp` |
| 파이썬 모듈 | `moai_<서비스>` | `moai_youtube` |
| 엔트리포인트 | `moai-<서비스>-mcp` | `moai-youtube-mcp` |

`<서비스>`는 **연동 대상 서비스 이름**이다(플러그인 이름이 아니다). 한 플러그인이 서버를
여러 개 가질 수 있기 때문이다 — `moai-seller`가 smartstore·imweb·cafe24 셋을 갖는 것처럼.

### 2-1. threads-poster 정합 작업

| 축 | 현재 | 변경 후 | 단계 |
|---|---|---|---|
| 서버 키 | `moai-threads-poster` | (동일) | — |
| 디렉터리 | `mcp-servers/threads-poster` | `mcp-servers/moai-threads-poster` | 1단계 |
| 엔트리포인트 | `threads-poster-mcp` | `moai-threads-poster-mcp` | 1단계 |
| 배포 패키지 | `moai-threads-poster-mcp` | (동일) | — |
| 모듈 | `threads_poster` | `moai_threads_poster` | 2단계(코어 추출과 함께) |

모듈 개명은 `import` 경로와 테스트 파일 전체가 걸린다. 디렉터리·엔트리포인트는 외부 계약
(`.mcp.json`)만 바꾸면 되므로 먼저 처리하고, 모듈은 코어 추출 작업에서 같이 옮긴다.

## 3. 통합 설계 — 서버 병합이 아니라 코어 추출

### 3-1. 근거 (실측)

`moai-imweb/_base.py`와 `moai-cafe24/_base.py`를 대조한 결과, 두 서버가 **같은 구조를 각자
복제**하고 있었다.

- OAuth2 `access_token` + `refresh_token`, HTTP 401 시 자동 재발급
- 갱신 토큰을 **동일 규칙**으로 영속화: `~/.moai/mcp/<서비스>-tokens.json`
- 쓰기 불가 경로면 인메모리 폴백 (주석 문구까지 유사)
- 의존성 동일: `mcp>=1.2.0` · `httpx>=0.27.0` · `anyio>=4.0.0`

### 3-2. 왜 서버를 합치지 않는가

커머스 3종을 `moai-commerce-mcp` 하나로 병합하는 안은 기각한다.

- 스마트스토어만 쓰는 사용자도 도구 107개를 전부 로드하게 된다(컨텍스트 낭비).
- 환경변수 13개가 한 서버에 섞여, 하나만 연결한 사용자에게도 전부 요구하는 것처럼 보인다.
- 한 채널의 API 장애·인증 만료가 다른 채널 도구까지 끌고 죽는다.
- 플러그인 경계와 어긋난다 — 유튜브·Threads는 셀러 소속이 아니다.

### 3-3. 채택안 — `moai-mcp-core` 공유 라이브러리

```
plugins/_shared/mcp-core/            # 신규 (위치는 4-1에서 확정)
  moai_mcp_core/
    auth.py       OAuth2 클라이언트 자격증명 · authorization_code · 리프레시 회전
    tokenstore.py ~/.moai/mcp/<서비스>-tokens.json 영속화 + 인메모리 폴백 (pathlib)
    http.py       httpx 클라이언트 · 재시도 · 타임아웃 · 레이트리밋 백오프
    errors.py     공통 예외 → MCP 오류 응답 매핑
    cache.py      읽기 응답 TTL 캐시 (쿼터 절약)
        ↑ 의존
  moai-smartstore   moai-imweb   moai-cafe24   moai-threads-poster   moai-youtube
```

각 서버는 자기 도메인(엔드포인트 매핑·도구 정의)만 갖는다. 서버 개수·`.mcp.json` 구조·
사용자가 보는 환경변수는 **지금 그대로** 유지된다 — 통합은 내부 코드 층에서만 일어난다.

### 3-4. 이관 순서 (역순 위험 회피)

1. `moai-mcp-core` 를 신설하고, 가장 최근에 만든 `moai-cafe24`의 `_base`/`auth`/`client`를 원본으로 삼아 일반화한다.
2. `moai-imweb` 을 코어로 전환한다(구조가 가장 가까워 검증이 쉽다).
3. `moai-threads-poster` 를 코어로 전환하면서 모듈명을 `moai_threads_poster`로 개명한다.
4. `moai-smartstore` 를 전환한다(bcrypt 전자서명이라는 고유 인증이 있어 마지막).
5. `moai-youtube` 는 **처음부터 코어 위에** 올린다.

각 단계는 해당 서버의 기존 테스트가 통과하는 것을 완료 조건으로 한다.

## 4. 범용성 제약 (OS × 런타임)

`CLAUDE.local.md` §범용성 원칙의 MCP 적용분이다.

- `.mcp.json` `command`는 `uv`·`uvx`·`npx`만 쓴다. `/bin/bash`·`sh -c` 금지(Windows에 없다).
- `args`에 셸 연산자(`&&`·`|`·`>`·`~`)를 넣지 않는다.
- 경로는 `${CLAUDE_PLUGIN_ROOT}` + 상대경로로 조립한다.
- 서버 코드의 파일 접근은 `pathlib.Path` + `encoding="utf-8"`. 토큰·캐시는 `Path.home()/".moai"/"mcp"`.
- 플러그인은 `.claude-plugin/plugin.json`과 `.codex-plugin/plugin.json`을 쌍으로 갖고, `.mcp.json`은 양쪽이 공유한다.

**현재 상태**: 플러그인 `.mcp.json` 전부가 이 제약을 만족한다(검사 무매치).
저장소 루트 `.mcp.json`의 `context7`만 `/bin/bash -l -c`를 쓰는데, 이는 **개발자 저장소 전용**
설정으로 사용자에게 배포되지 않는다. 배포 대상이 되면 `npx`로 바꾼다.

### 4-1. `moai-mcp-core` 배치 미결 사항

플러그인은 각자 독립 설치되므로 `plugins/_shared/`를 서로 참조할 수 없다. 두 가지 중 하나를
코어 추출 착수 시 결정한다.

| 안 | 방식 | 장점 | 단점 |
|---|---|---|---|
| A. PyPI 배포 | `moai-mcp-core`를 PyPI에 올리고 각 서버가 의존성으로 선언 | 중복 0, 버전 관리 명확 | 배포 파이프라인 필요, 오프라인 설치 불가 |
| B. vendor 복제 | 각 서버 `src/` 아래에 코어를 복제하고 스크립트로 동기화 | 설치 즉시 작동(현행 정책 유지) | 복제본 존재, 동기화 누락 위험 |

현행 정책("PyPI 불필요, 설치 즉시 작동")과의 정합만 보면 B가 유리하다. 결정은 사용자 승인
사항으로 남긴다.

## 5. `moai-youtube` 서버 구현 계약 (2단계 착수용)

풀세트 범위 — YouTube Data API v3 + Live Streaming API + Analytics API 읽기.

### 5-1. 배치

| 항목 | 값 |
|---|---|
| 소속 플러그인 | `moai-youtuber` |
| 서버 키 | `moai-youtube` |
| 디렉터리 | `plugins/moai-youtuber/mcp-servers/moai-youtube` |
| 배포 패키지 · 엔트리포인트 | `moai-youtube-mcp` |
| 모듈 | `moai_youtube` |
| 기동 | `uv run --directory ${CLAUDE_PLUGIN_ROOT}/mcp-servers/moai-youtube moai-youtube-mcp` |

### 5-2. 인증

Data API의 업로드·수정, Live Streaming 전체, Analytics 조회는 **API 키로 불가능**하고 OAuth2
사용자 동의가 필요하다. 따라서 OAuth2 authorization_code + refresh token 자동 갱신을 기본으로
한다(`moai-imweb`·`moai-cafe24`와 같은 패턴).

| 환경변수 | 용도 | 필수 |
|---|---|---|
| `YOUTUBE_CLIENT_ID` | Google Cloud OAuth 클라이언트 | 필수 |
| `YOUTUBE_CLIENT_SECRET` | 〃 | 필수 |
| `YOUTUBE_REFRESH_TOKEN` | 최초 동의 후 발급 | 필수 |
| `YOUTUBE_CHANNEL_ID` | 기본 대상 채널 | 선택 |
| `YOUTUBE_API_KEY` | 공개 데이터 읽기 전용 경로 | 선택 |

필요 스코프: `youtube.readonly` · `youtube.upload` · `youtube.force-ssl`(라이브 채팅·댓글) ·
`yt-analytics.readonly`.

### 5-3. 도구 묶음 (초안)

| 묶음 | 도구 | 근거 API |
|---|---|---|
| 채널·조회 | `channel_profile` · `list_my_videos` · `video_details` · `search_videos` | Data v3 |
| 발행 | `upload_video` · `update_video_metadata` · `set_thumbnail` · `set_publish_schedule` | Data v3 |
| 재생목록 | `list_playlists` · `create_playlist` · `add_to_playlist` · `reorder_playlist` | Data v3 |
| 라이브 | `create_broadcast` · `bind_stream` · `transition_broadcast` · `list_broadcasts` · `end_broadcast` | Live Streaming |
| 라이브 채팅 | `read_live_chat` · `send_live_chat` · `moderate_live_chat` | Live Streaming |
| 댓글 | `list_comments` · `reply_comment` · `moderate_comment` | Data v3 |
| 분석 | `channel_report` · `video_report` · `traffic_source_report` · `audience_retention` | Analytics |
| 캡션 | `list_captions` · `upload_caption` | Data v3 |

### 5-4. 쿼터 방어 (필수 설계)

기본 할당량은 하루 10,000 units다. `search.list`가 **1회 100 units**여서 하루 100회면 소진되고,
`videos.list`는 1 unit이다. 업로드는 2025-12-04 개정으로 약 1,600 → 약 100 units로 내려가,
이제 쿼터를 가장 빨리 태우는 것은 업로드가 아니라 **검색**이다.

- `search_videos`는 TTL 캐시를 강제하고, 캐시 미스일 때만 호출한다.
- 채널 자기 영상 목록은 `search`가 아니라 `playlistItems.list`(업로드 재생목록, 1 unit)로 받는다.
- 모든 도구 응답에 소모 units를 함께 반환해 사용자가 잔량을 인지하게 한다.
- 일일 누적이 임계에 닿으면 도구가 실패 대신 **경고 + 캐시 응답**을 돌려준다.

### 5-5. 라이브 방송 순서 (도구 호출 체인)

```
create_broadcast (제목·시작시각·공개범위)
    → bind_stream (인코더 스트림 키 연결)
    → transition_broadcast: testing → live
    → read_live_chat / send_live_chat (방송 중)
    → transition_broadcast: complete
    → update_video_metadata (다시보기 제목·설명·챕터)
```

## 6. 참고 자료

- [YouTube Data API 개요](https://developers.google.com/youtube/v3/getting-started)
- [YouTube Live Streaming API](https://developers.google.com/youtube/v3/live/getting-started)
- [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- 공식 MCP 부재 확인: [YouTube MCP: No Official Server, Community Ones Work](https://www.usecarly.com/blog/youtube-mcp/) · [YouTube MCP Server Comparison 2026](https://www.ekamoira.com/blog/youtube-mcp-server-comparison-2026-which-one-should-you-use)
- 쿼터 단가: [YouTube API Pricing 2026](https://www.blotato.com/blog/youtube-api-pricing)
