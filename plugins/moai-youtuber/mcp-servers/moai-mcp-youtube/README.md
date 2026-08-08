# moai-youtube MCP 서버

YouTube Data API v3 · Live Streaming API · Analytics API 를 MCP 도구로 노출합니다.
유튜브에는 Google이 관리하는 공식 MCP 서버가 없어 직접 만들었습니다.

인증·재시도·오류 매핑은 공통 코어(`moai_mcp_core`)가 담당하고, 이 서버는 유튜브
고유의 **할당량 회계**와 엔드포인트 매핑만 갖습니다.

## 할당량이 이 서버의 설계를 규정합니다

기본 한도는 하루 10,000 units인데 단가가 균일하지 않습니다.

| 작업 | 단가 | 하루에 몇 번 |
|---|---:|---|
| `search.list` (검색) | 100 | 100회면 끝 |
| `videos.insert` (업로드) | 100 | — |
| `captions.insert` (자막) | 400 | 이 서버에서 가장 비쌈 |
| 쓰기 작업 대부분 | 50 | — |
| 조회 대부분 | 1 | 사실상 무제한 |
| Analytics API | 0 | Data API 할당량을 쓰지 않음 |

업로드는 2025-12-04 개정으로 약 1,600 → 약 100 units로 내려갔습니다. **이제 할당량을
가장 빨리 태우는 것은 업로드가 아니라 검색입니다.** 그래서 두 가지 방어를 넣었습니다.

- **검색 캐시 강제** — 같은 조건의 검색은 캐시에서 돌려주고 비용을 다시 청구하지 않습니다.
- **검색 회피 경로** — 내 채널 영상 목록은 `search`(100)가 아니라 업로드 재생목록을 통해
  `playlistItems.list`(1)로 받습니다. 같은 결과를 50분의 1 비용으로 얻습니다.

모든 도구 응답에 잔량 추정치가 함께 담깁니다. 다만 이 값은 **추정**입니다 — 같은 계정을
다른 도구가 함께 쓰고 있으면 실제 잔량은 더 적습니다. 정확한 값은 Google Cloud 콘솔이 정본입니다.

## 도구

| 묶음 | 도구 |
|---|---|
| 채널·조회 | `youtube_channel_profile` · `youtube_list_my_videos` · `youtube_video_details` · `youtube_search` |
| 발행 | `youtube_upload_video` · `youtube_update_metadata` · `youtube_set_thumbnail` · `youtube_schedule_publish` |
| 재생목록 | `youtube_list_playlists` · `youtube_create_playlist` · `youtube_add_to_playlist` |
| 라이브 | `youtube_create_broadcast` · `youtube_bind_stream` · `youtube_transition_broadcast` · `youtube_list_broadcasts` |
| 실시간 채팅 | `youtube_read_live_chat` · `youtube_send_live_chat` · `youtube_moderate_live_chat` |
| 댓글 | `youtube_list_comments` · `youtube_reply_comment` · `youtube_moderate_comment` |
| 분석 | `youtube_channel_report` · `youtube_video_report` · `youtube_traffic_sources` · `youtube_audience_retention` |
| 자막 | `youtube_list_captions` · `youtube_upload_caption` |
| 운영 | `youtube_quota_status` |

## 라이브 방송 순서

```
youtube_create_broadcast     방송 생성 (아직 송출 아님)
  → youtube_bind_stream      인코더 스트림 연결
  → youtube_transition_broadcast "testing"   미리보기 — 소리·화면 확인
  → youtube_transition_broadcast "live"      송출 시작
  → youtube_read_live_chat / youtube_send_live_chat
  → youtube_transition_broadcast "complete"  종료
  → youtube_update_metadata  다시보기 제목·설명·챕터 정리
```

`testing` 을 건너뛰고 바로 `live` 로 가지 마세요. 소리가 안 나가는지 확인할 마지막 기회입니다.

## 설정

| 환경변수 | 필수 | 설명 |
|---|---|---|
| `YOUTUBE_CLIENT_ID` | 필수 | Google Cloud OAuth 클라이언트 ID |
| `YOUTUBE_CLIENT_SECRET` | 필수 | 〃 시크릿 |
| `YOUTUBE_REFRESH_TOKEN` | 필수 | 최초 1회 동의 후 발급 |
| `YOUTUBE_CHANNEL_ID` | 선택 | 기본 대상 채널 |
| `YOUTUBE_DAILY_QUOTA` | 선택 | 일일 한도 (기본 10000). 상향 승인을 받았다면 조정 |
| `YOUTUBE_SEARCH_CACHE_TTL` | 선택 | 검색 캐시 수명(초, 기본 900) |
| `YOUTUBE_TOKEN_FILE` · `YOUTUBE_QUOTA_FILE` | 선택 | 저장 경로 재지정 |

발급 절차는 [`CONNECTORS.md`](CONNECTORS.md)를 보세요.

**자격증명이 없어도 서버는 뜹니다.** 각 도구가 `setup_required` 안내를 돌려줄 뿐입니다 —
기동에 실패하면 사용자는 원인 모를 연결 오류만 보게 되기 때문입니다.

## 개발

```bash
uv sync
uv run pytest -q
```

`src/moai_mcp_core/` 는 **자동 생성된 복제본**입니다. 고치려면 정본
(`plugins/_shared/moai-mcp-core/`)을 고치고 `python3 scripts/sync-mcp-core.py` 를 실행하세요.

## 참고

- [YouTube Data API](https://developers.google.com/youtube/v3/getting-started)
- [YouTube Live Streaming API](https://developers.google.com/youtube/v3/live/getting-started)
- [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- 설계 정본: `.moai/reports/mcp-naming-consolidation-design.md` §5
