# moai-threads-poster MCP

Threads(Meta) Graph API 자동 포스팅 MCP 서버. Claude Code 의 stdio MCP 서버로 실행되며,
텍스트·이미지·비디오 2단계 발행(`create container` → `publish`)을 도구로 노출한다.

## 도구 (5)

| 도구 | 설명 |
|---|---|
| `threads_publish_text` | 텍스트 스레드 발행 (500 UTF-8 바이트 제한) |
| `threads_publish_image` | 이미지(JPEG/PNG, ≤8MB) 발행 |
| `threads_publish_video` | 비디오(MOV/MP4, ≤1GB, ≤5분) 발행 |
| `threads_get_profile` | 프로필 조회 — health check / who-am-I |
| `threads_refresh_token` | 장기 액세스 토큰(60일) 수동 갱신 |

## 자격증명 발급 절차

**[CONNECTORS.md](CONNECTORS.md)** 참조 — Meta App 생성, Threads 사용 사례 연결, 인가 코드 교환,
단기 → 장기 토큰 변환, 테스터 초대까지의 1회性 수동 설정.

## 환경변수

| 변수 | 필수 | 기본 | 설명 |
|---|---|---|---|
| `THREADS_ACCESS_TOKEN` | 예 | — | Threads 장기 액세스 토큰 |
| `THREADS_USER_ID` | 예 | — | Threads 사용자 ID |
| `THREADS_PUBLISH_DELAY` | 아니오 | `30` | container 생성 → publish 대기(초). 테스트 시 `0` |

## 개발

```bash
cd plugins/moai-threads-poster/mcp-servers/threads-poster
uv sync                    # 의존성 설치
uv run pytest              # 테스트 실행
uv run threads-poster-mcp  # stdio MCP 서버 기동
```

## 구조

```
src/threads_poster/
  __init__.py        # 패키지 루트
  threads_api.py     # ThreadsClient — 순수 HTTP 클라이언트 (httpx 주입 가능)
  server.py          # FastMCP 서버 + 5개 도구 + main()
tests/
  test_threads_api.py  # ThreadsClient 단위 테스트 (MockTransport, 네트워크 없음)
  test_server.py       # server 도우미/도구 단위 테스트
```

---

라이선스: Apache-2.0 · 버전: 0.1.0
