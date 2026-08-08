# 자체 제작 MCP — 작명 통일 · 공통 코어 통합 설계서

> 작성 2026-08-08 · 정본. 자체 제작 MCP 서버의 이름 규칙과 코드 통합 방향을 확정한다. 원칙 요약본은 `CLAUDE.local.md`
> §자체 제작 MCP 작명·구조 규칙 / §범용성 원칙에 있고, 이 문서가 근거와 상세를 담는다.

## 1. 전수조사 결과 (실측)

`plugins/*/.mcp.json` 전부와 `plugins/*/mcp-servers/` 를 실측했다.

### 1-1. 자체 제작 서버

| 서버 키 | 소속 플러그인 | 모듈 | 등록 도구 | 코드량 |
|---|---|---|---|---|
| `moai-mcp-smartstore` | moai-seller | `moai_mcp_smartstore` | 93 | 1,323줄 |
| `moai-mcp-imweb` | moai-seller | `moai_mcp_imweb` | 10 | 1,650줄 |
| `moai-mcp-cafe24` | moai-seller | `moai_mcp_cafe24` | 4(디스패치형) | 3,133줄 |
| `moai-mcp-threads-poster` | moai-threads-poster | `moai_mcp_threads_poster` | 17 | 1,625줄 |

디렉터리·배포 패키지·엔트리포인트는 모두 서버 키와 같은 문자열이다(§2). 최초 조사 시점에는
`moai-<서비스>` / `moai-<서비스>-mcp` 가 섞여 있었고 threads-poster는 3축이 어긋나 있었는데,
2026-08-08 전면 개명으로 다섯 서버 모두 정합 상태가 되었다.

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
| `.mcp.json` 서버 키 | `moai-mcp-<서비스>` | `moai-mcp-imweb` |
| 디렉터리 | `mcp-servers/moai-mcp-<서비스>` | `mcp-servers/moai-mcp-imweb` |
| 배포 패키지명 | `moai-mcp-<서비스>` | `moai-mcp-imweb` |
| 파이썬 모듈 | `moai_mcp_<서비스>` | `moai_mcp_imweb` |
| 엔트리포인트 | `moai-mcp-<서비스>` | `moai-mcp-imweb` |

**다섯 축이 같은 문자열**이다(모듈만 밑줄 표기). 접두어를 `moai-mcp-` 로 잡은 이유는 공유
코어가 `moai-mcp-core` 이기 때문이다 — 코어와 서버가 한 계열로 읽힌다. `-mcp` 를 뒤에 붙이던
옛 형태(`moai-imweb-mcp` 꼴)는 폐기했다.

`<서비스>`는 **연동 대상 서비스 이름**이다(플러그인 이름이 아니다). 한 플러그인이 서버를
여러 개 가질 수 있기 때문이다 — `moai-seller`가 smartstore·imweb·cafe24 셋을 갖는 것처럼.

### 2-1. 전면 개명 결과 (2026-08-08)

| 서비스 | 옛 이름 (서버키 / 패키지·EP / 모듈) | 새 이름 |
|---|---|---|
| imweb | `moai-imweb` / `moai-imweb-mcp` / `moai_imweb` | `moai-mcp-imweb` / `moai_mcp_imweb` |
| cafe24 | `moai-cafe24` / `moai-cafe24-mcp` / `moai_cafe24` | `moai-mcp-cafe24` / `moai_mcp_cafe24` |
| smartstore | `moai-smartstore` / `moai-smartstore-mcp` / `moai_smartstore` | `moai-mcp-smartstore` / `moai_mcp_smartstore` |
| threads-poster | `moai-threads-poster` / `threads-poster-mcp` / `threads_poster` | `moai-mcp-threads-poster` / `moai_mcp_threads_poster` |

**서버 키가 바뀌면 도구 네임스페이스도 바뀐다** (`mcp__moai-smartstore__*` →
`mcp__moai-mcp-smartstore__*`). `.mcp.json` 은 플러그인에 동봉돼 함께 갱신되므로 사용자가 할
일은 없다. 환경변수 이름은 그대로다.

## 3. 통합 설계 — 서버 병합이 아니라 코어 추출

### 3-1. 근거 (실측)

`moai-mcp-imweb/_base.py`와 `moai-mcp-cafe24/_base.py`를 대조한 결과, 두 서버가 **같은 구조를 각자
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
  moai-mcp-smartstore  moai-mcp-imweb  moai-mcp-cafe24  moai-mcp-threads-poster
```

각 서버는 자기 도메인(엔드포인트 매핑·도구 정의)만 갖는다. 서버 개수·`.mcp.json` 구조·
사용자가 보는 환경변수는 **지금 그대로** 유지된다 — 통합은 내부 코드 층에서만 일어난다.

### 3-4. 이관 결과 (2026-08-08 실측으로 계획 수정)

당초 계획은 자체 제작 서버 4종을 모두 코어로 옮기는 것이었다. **실제 코드를 읽어 보니
그 가정이 틀렸다** — 인증 모델이 서버마다 근본적으로 다르다.

| 서버 | 인증 모델 | 토큰 저장 | 코어 적합 | 상태 |
|---|---|---|---|---|
| `moai-mcp-imweb` | OAuth2 refresh_token (camelCase 키 + Basic 병행) | 파일 | 적합 | **이관 완료** |
| `moai-mcp-cafe24` | OAuth2 refresh_token (리프레시 회전) | 파일 | 적합 | **이관 완료** |
| `moai-mcp-smartstore` | `client_credentials` + bcrypt 전자서명 | **메모리 전용** | 부적합 | 현행 유지 |
| `moai-mcp-threads-poster` | Meta 장기 토큰 **연장**(`th_refresh_token` / `fb_exchange_token`) | **환경변수** | 부적합 | 현행 유지 |

**왜 뒤 둘은 옮기지 않는가.** 코어의 `OAuth2Refresher` 는 리프레시 그랜트를 전제한다.
스마트스토어는 매 호출마다 전자서명을 새로 만들어 `client_credentials` 로 토큰을 받고
메모리에만 들고 있으며, Threads/인스타그램은 표준 OAuth2가 아니라 Meta 고유의 장기
토큰 연장 엔드포인트를 쓴다. **둘 다 파일 영속화가 없어 `TokenStore` 로 걷어낼 중복도
없다.** 이들을 코어에 태우려면 호출자가 하나뿐인 모드를 코어에 새로 파야 하는데, 그것은
공통화가 아니라 과잉 추상화다(constitution §Enforce Simplicity).

남은 공통화 여지는 **HTTP 재시도·백오프·오류 매핑**뿐이고, 두 서버 모두 자기 요청 루프가
정상 동작 중이다. 이득 대비 회귀 위험이 커서 지금은 손대지 않는다. 두 서버의 요청 루프를
어차피 고쳐야 할 일이 생기면 그때 코어 `HttpClient` 로 옮긴다.

각 이관의 완료 조건은 해당 서버의 기존 테스트 통과였고, 실제로 그렇게 검증했다
(imweb 기존 19 → 27, cafe24 0 → 9 신규).

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

### 4-1. `moai-mcp-core` 배치 — **B안(vendor 복제) 확정**

플러그인은 각자 독립 설치되므로 `plugins/_shared/`를 런타임에 서로 참조할 수 없다. 두 안을
검토한 뒤 **B안(vendor 복제)** 을 채택했다(2026-08-08 결정).

| 안 | 방식 | 장점 | 단점 | 판정 |
|---|---|---|---|---|
| A. PyPI 배포 | PyPI에 올리고 각 서버가 의존성으로 선언 | 중복 0, 버전 관리 명확 | 배포 파이프라인 필요, 오프라인 설치 불가 | 기각 |
| B. vendor 복제 | 각 서버 `src/` 아래에 코어를 복제하고 스크립트로 동기화 | **설치 즉시 작동**(현행 정책 유지) | 복제본 존재, 동기화 누락 위험 | **채택** |

채택 사유: 이 마켓플레이스의 사용자는 비개발자다. PyPI 의존은 네트워크·인증·버전 충돌이라는
실패 지점을 사용자에게 떠넘긴다. 현행 정책("PyPI 불필요, 설치 즉시 작동")을 유지한다.

#### vendor 동기화 계약

B안의 유일한 위험은 **복제본 드리프트**다. 이를 기계적으로 막는다.

| 항목 | 값 |
|---|---|
| 정본 위치 | `plugins/_shared/moai-mcp-core/moai_mcp_core/` |
| 복제 위치 | 각 서버의 `src/moai_mcp_core/` |
| 동기화 도구 | `scripts/sync-mcp-core.py` |
| 복제본 표시 | 각 복제 파일 첫 줄에 자동 생성 배너 — 직접 수정 금지 |
| 드리프트 검사 | `python3 scripts/sync-mcp-core.py --check` (종료코드 1이면 불일치) |
| 서버 pyproject | `packages = ["src/moai_mcp_<서비스>", "src/moai_mcp_core"]` |

**정본만 고친다.** 복제본을 직접 수정하면 다음 동기화에서 덮어써진다. 커밋 전에 `--check`를
돌려 불일치를 잡는다.

#### 코어 모듈 구성

| 모듈 | 책임 |
|---|---|
| `tokenstore.py` | 토큰 영속화 — `~/.moai/mcp/<서비스>-tokens.json`, 쓰기 불가 시 인메모리 폴백 |
| `auth.py` | OAuth2 access/refresh 갱신, 리프레시 토큰 회전 대응, 만료 선반영 |
| `http.py` | httpx 래퍼 — 타임아웃·재시도·백오프·429 대응·401 시 1회 재인증 |
| `cache.py` | 읽기 응답 TTL 캐시 (할당량 절약) |
| `errors.py` | 예외 → MCP 구조화 오류 응답 매핑 |

## 6. 참고 자료

- [YouTube Live Streaming API](https://developers.google.com/youtube/v3/live/getting-started)

## 7. 유튜브 서버 — 철회 기록 (2026-08-08)

`moai-mcp-youtube` 서버와 유튜버 플러그인을 만들었다가 **배포 전에 철회**했다.

철회 사유: 유튜브 연동은 Google Cloud 프로젝트 생성 → API 두 종 활성화 → 동의 화면
권한 등록 → OAuth 클라이언트 발급 → 브라우저 동의 → 인증 코드를 토큰으로 교환, 여섯
단계를 사용자가 직접 밟아야 한다. 이 마켓플레이스의 대상은 비개발자이고, 그 절차는
감당할 수 있는 수준을 넘는다. 자동화할 수도 없다 — 브라우저 동의는 본인이 해야 한다.

남긴 것: `moai-mcp-core` 공통 코어는 아임웹·카페24가 쓰고 있어 그대로 유지한다.
MCP 안내 문서(개요·설치·문제 해결)도 다른 서버에 그대로 적용되므로 유지한다.

같은 판단이 필요한 다음 연동을 위해: **인증 절차가 여섯 단계를 넘고 브라우저 동의가
끼면, 비개발자용 연동으로는 부적합하다.** 붙이기 전에 이 기준으로 먼저 걸러야 한다.
