"""moai-youtube MCP 서버 — stdio 진입점.

YouTube Data API v3 · Live Streaming API · Analytics API 를 도구로 노출한다.

자격증명(`YOUTUBE_CLIENT_ID` / `YOUTUBE_CLIENT_SECRET` / `YOUTUBE_REFRESH_TOKEN`)이
없어도 **서버는 뜬다** — 각 도구가 `setup_required` 안내를 돌려줄 뿐이다. 기동에
실패하면 사용자는 원인 모를 연결 오류만 보게 되기 때문이다.

할당량 방어가 이 서버의 특징이다. 기본 한도는 하루 10,000 units인데 `search.list` 가
1회 100 units라 검색이 가장 빨리 한도를 태운다. 그래서 검색은 캐시를 강제하고,
내 채널 영상 목록은 검색이 아니라 업로드 재생목록(1 unit)으로 받는다. 모든 응답에
잔량 추정치를 함께 담는다.
"""

from __future__ import annotations

from typing import Any, Callable

from mcp.server.fastmcp import FastMCP
from moai_mcp_core import to_tool_result

from .client import YouTubeClient
from .config import load_config

_INSTRUCTIONS = (
    "YouTube 채널 운영 MCP. 라이브 방송(생성·스트림 연결·상태 전환·실시간 채팅), "
    "발행(업로드·메타데이터·썸네일·재생목록·자막·예약), 성과 조회(채널·영상·유입경로·"
    "시청 유지), 댓글 관리. 할당량이 하루 10,000 units로 제한되며 검색은 1회 100 units다 — "
    "검색은 꼭 필요할 때만 하고, 내 영상 목록은 youtube_list_my_videos 를 쓴다. "
    "사전 설정: YOUTUBE_CLIENT_ID · YOUTUBE_CLIENT_SECRET · YOUTUBE_REFRESH_TOKEN."
)

mcp: FastMCP = FastMCP("moai-youtube", instructions=_INSTRUCTIONS)

_client: YouTubeClient | None = None


def get_client() -> YouTubeClient:
    """클라이언트 싱글턴. 토큰 캐시와 할당량 원장을 프로세스 내에서 공유한다."""
    global _client
    if _client is None:
        _client = YouTubeClient(load_config())
    return _client


def reset_client(client: YouTubeClient | None = None) -> None:
    """테스트에서 클라이언트를 갈아 끼운다."""
    global _client
    _client = client


def _run(fn: Callable[[YouTubeClient], dict[str, Any]]) -> dict[str, Any]:
    """도구 본문을 실행하고 실패를 구조화된 응답으로 바꾼다.

    예외를 밖으로 던지면 서버가 죽는다 — 그러면 사용자는 원인을 알 수 없다.
    """
    try:
        client = get_client()
        result = fn(client)
        result.setdefault("ok", True)
        result["quota"] = client.quota()
        return result
    except Exception as exc:  # noqa: BLE001 — 모든 실패를 응답으로 변환하는 것이 목적
        return to_tool_result(exc)


# ---------------------------------------------------------------------------
# 채널 · 조회
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_channel_profile(channel_id: str | None = None) -> dict[str, Any]:
    """채널 기본 정보와 누적 지표를 조회한다 (1 unit).

    Args:
        channel_id: 대상 채널. 생략하면 인증된 본인 채널.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        params: dict[str, Any] = {"part": "snippet,statistics,contentDetails"}
        target = channel_id or client.config.channel_id
        if target:
            params["id"] = target
        else:
            params["mine"] = "true"
        data = client.get("channels.list", "channels", params) or {}
        items = data.get("items") or []
        if not items:
            return {"ok": False, "error": "not_found", "message": "채널을 찾을 수 없습니다."}
        item = items[0]
        return {
            "channel_id": item.get("id"),
            "title": item.get("snippet", {}).get("title"),
            "description": item.get("snippet", {}).get("description"),
            "published_at": item.get("snippet", {}).get("publishedAt"),
            "statistics": item.get("statistics", {}),
        }

    return _run(run)


@mcp.tool()
def youtube_list_my_videos(max_results: int = 25, page_token: str | None = None) -> dict[str, Any]:
    """내 채널에 올린 영상 목록 (2 units).

    검색(100 units)이 아니라 업로드 재생목록을 통해 받는다 — 같은 결과를 50분의 1
    비용으로 얻는다. 남의 채널을 찾을 때만 youtube_search 를 쓴다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        playlist_id = client.uploads_playlist_id()
        data = (
            client.get(
                "playlistItems.list",
                "playlistItems",
                {
                    "part": "snippet,contentDetails",
                    "playlistId": playlist_id,
                    "maxResults": min(max(max_results, 1), 50),
                    "pageToken": page_token,
                },
            )
            or {}
        )
        videos = [
            {
                "video_id": item.get("contentDetails", {}).get("videoId"),
                "title": item.get("snippet", {}).get("title"),
                "published_at": item.get("contentDetails", {}).get("videoPublishedAt"),
            }
            for item in data.get("items", [])
        ]
        return {"videos": videos, "next_page_token": data.get("nextPageToken")}

    return _run(run)


@mcp.tool()
def youtube_video_details(video_ids: list[str]) -> dict[str, Any]:
    """영상의 메타데이터·통계·상태를 조회한다 (1 unit).

    Args:
        video_ids: 영상 ID 목록. 한 번에 여러 개를 넣어도 1 unit이다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        if not video_ids:
            return {"ok": False, "error": "invalid_input", "message": "video_ids 가 비었습니다."}
        data = (
            client.get(
                "videos.list",
                "videos",
                {"part": "snippet,statistics,status,contentDetails", "id": ",".join(video_ids)},
            )
            or {}
        )
        return {"videos": data.get("items", [])}

    return _run(run)


@mcp.tool()
def youtube_search(
    query: str,
    max_results: int = 10,
    channel_id: str | None = None,
    order: str = "relevance",
) -> dict[str, Any]:
    """유튜브 전체 검색 (100 units — 비쌉니다).

    같은 조건의 검색은 캐시에서 돌려주므로 반복 호출은 추가 비용이 없다. 내 채널
    영상을 찾는 것이라면 youtube_list_my_videos 를 쓰세요 — 50분의 1 비용입니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.search(
                {
                    "part": "snippet",
                    "q": query,
                    "maxResults": min(max(max_results, 1), 50),
                    "channelId": channel_id,
                    "order": order,
                    "type": "video",
                }
            )
            or {}
        )
        results = [
            {
                "video_id": item.get("id", {}).get("videoId"),
                "title": item.get("snippet", {}).get("title"),
                "channel_title": item.get("snippet", {}).get("channelTitle"),
                "published_at": item.get("snippet", {}).get("publishedAt"),
            }
            for item in data.get("items", [])
        ]
        return {"results": results}

    return _run(run)


# ---------------------------------------------------------------------------
# 발행
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_upload_video(
    file_path: str,
    title: str,
    description: str = "",
    tags: list[str] | None = None,
    privacy: str = "private",
    category_id: str = "22",
    made_for_kids: bool = False,
) -> dict[str, Any]:
    """영상 파일을 업로드한다 (100 units).

    기본 공개 범위는 `private` 이다 — 실수로 공개되는 것보다 안전하다. 확인 후
    youtube_schedule_publish 나 youtube_update_metadata 로 공개한다.

    Args:
        file_path: 올릴 영상 파일 경로.
        privacy: private · unlisted · public.
        made_for_kids: 아동용 여부. 잘못 지정하면 댓글·알림이 제한된다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": made_for_kids,
            },
        }
        data = (
            client.resumable_upload(
                "videos.insert",
                "videos",
                file_path=file_path,
                metadata=body,
                params={"part": "snippet,status"},
                content_type="video/*",
            )
            or {}
        )
        return {
            "video_id": data.get("id"),
            "privacy": data.get("status", {}).get("privacyStatus"),
            "next_step": "썸네일(youtube_set_thumbnail)과 재생목록(youtube_add_to_playlist)을 이어서 처리하세요.",
        }

    return _run(run)


@mcp.tool()
def youtube_update_metadata(
    video_id: str,
    title: str | None = None,
    description: str | None = None,
    tags: list[str] | None = None,
    category_id: str | None = None,
) -> dict[str, Any]:
    """영상의 제목·설명·태그를 수정한다 (50 units).

    유튜브 API는 부분 수정을 지원하지 않아 기존 값을 먼저 읽어 병합한다. 그래서
    조회 1 unit이 추가로 든다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        current = client.get("videos.list", "videos", {"part": "snippet", "id": video_id}) or {}
        items = current.get("items") or []
        if not items:
            return {"ok": False, "error": "not_found", "message": f"영상을 찾을 수 없습니다: {video_id}"}

        snippet = dict(items[0].get("snippet", {}))
        if title is not None:
            snippet["title"] = title
        if description is not None:
            snippet["description"] = description
        if tags is not None:
            snippet["tags"] = tags
        if category_id is not None:
            snippet["categoryId"] = category_id

        client.put(
            "videos.update",
            "videos",
            params={"part": "snippet"},
            body={"id": video_id, "snippet": snippet},
        )
        return {"video_id": video_id, "updated": True}

    return _run(run)


@mcp.tool()
def youtube_set_thumbnail(video_id: str, file_path: str) -> dict[str, Any]:
    """맞춤 썸네일을 적용한다 (50 units).

    Args:
        file_path: 이미지 파일 경로. 축소 화면에서 문구가 읽히는지 먼저 확인하세요.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        client.media_upload(
            "thumbnails.set",
            "thumbnails/set",
            file_path=file_path,
            params={"videoId": video_id},
            content_type="image/png" if file_path.lower().endswith(".png") else "image/jpeg",
        )
        return {"video_id": video_id, "thumbnail_applied": True}

    return _run(run)


@mcp.tool()
def youtube_schedule_publish(video_id: str, publish_at: str) -> dict[str, Any]:
    """공개 예약을 건다 (50 units).

    Args:
        publish_at: RFC3339 시각 (예: `2026-08-20T19:00:00+09:00`). 사용자의 시간대로
            적었는지 반드시 확인하세요 — 가장 흔한 사고입니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        client.put(
            "videos.update",
            "videos",
            params={"part": "status"},
            body={
                "id": video_id,
                "status": {"privacyStatus": "private", "publishAt": publish_at},
            },
        )
        return {
            "video_id": video_id,
            "publish_at": publish_at,
            "note": "예약 공개는 비공개 상태로 대기하다 지정 시각에 공개됩니다.",
        }

    return _run(run)


# ---------------------------------------------------------------------------
# 재생목록
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_list_playlists(max_results: int = 25) -> dict[str, Any]:
    """내 재생목록 목록 (1 unit)."""

    def run(client: YouTubeClient) -> dict[str, Any]:
        params: dict[str, Any] = {
            "part": "snippet,contentDetails",
            "maxResults": min(max(max_results, 1), 50),
        }
        if client.config.channel_id:
            params["channelId"] = client.config.channel_id
        else:
            params["mine"] = "true"
        data = client.get("playlists.list", "playlists", params) or {}
        playlists = [
            {
                "playlist_id": item.get("id"),
                "title": item.get("snippet", {}).get("title"),
                "item_count": item.get("contentDetails", {}).get("itemCount"),
            }
            for item in data.get("items", [])
        ]
        return {"playlists": playlists}

    return _run(run)


@mcp.tool()
def youtube_create_playlist(
    title: str, description: str = "", privacy: str = "public"
) -> dict[str, Any]:
    """재생목록을 만든다 (50 units).

    시리즈 하나에 재생목록 하나를 1:1로 대응시키고, 순서는 시청 순서(입문 → 심화)로
    두는 것이 좋습니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.post(
                "playlists.insert",
                "playlists",
                params={"part": "snippet,status"},
                body={
                    "snippet": {"title": title, "description": description},
                    "status": {"privacyStatus": privacy},
                },
            )
            or {}
        )
        return {"playlist_id": data.get("id"), "title": title}

    return _run(run)


@mcp.tool()
def youtube_add_to_playlist(
    playlist_id: str, video_id: str, position: int | None = None
) -> dict[str, Any]:
    """영상을 재생목록에 넣는다 (50 units)."""

    def run(client: YouTubeClient) -> dict[str, Any]:
        snippet: dict[str, Any] = {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id},
        }
        if position is not None:
            snippet["position"] = position
        data = (
            client.post(
                "playlistItems.insert",
                "playlistItems",
                params={"part": "snippet"},
                body={"snippet": snippet},
            )
            or {}
        )
        return {"playlist_item_id": data.get("id"), "playlist_id": playlist_id, "video_id": video_id}

    return _run(run)


# ---------------------------------------------------------------------------
# 라이브 방송
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_create_broadcast(
    title: str,
    scheduled_start: str,
    description: str = "",
    privacy: str = "private",
    enable_chat: bool = True,
    made_for_kids: bool = False,
) -> dict[str, Any]:
    """라이브 방송을 만든다 (50 units).

    이것은 방송 "예약"이지 송출 시작이 아니다. 다음 순서로 진행한다.
    create_broadcast → bind_stream → transition(testing) → transition(live).

    Args:
        scheduled_start: RFC3339 시각. 사용자의 시간대로 적었는지 확인하세요.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.post(
                "liveBroadcasts.insert",
                "liveBroadcasts",
                params={"part": "snippet,status,contentDetails"},
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "scheduledStartTime": scheduled_start,
                    },
                    "status": {
                        "privacyStatus": privacy,
                        "selfDeclaredMadeForKids": made_for_kids,
                    },
                    "contentDetails": {
                        "enableAutoStart": False,
                        "enableAutoStop": False,
                        "enableLiveChat": enable_chat,
                    },
                },
            )
            or {}
        )
        return {
            "broadcast_id": data.get("id"),
            "live_chat_id": data.get("snippet", {}).get("liveChatId"),
            "scheduled_start": scheduled_start,
            "next_step": "인코더 스트림을 youtube_bind_stream 으로 연결한 뒤 testing → live 로 전환하세요.",
        }

    return _run(run)


@mcp.tool()
def youtube_bind_stream(broadcast_id: str, stream_id: str) -> dict[str, Any]:
    """방송에 인코더 스트림을 연결한다 (50 units).

    Args:
        stream_id: 유튜브 스튜디오에서 만든 스트림의 ID (스트림 키가 아닙니다).
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        client.post(
            "liveBroadcasts.bind",
            "liveBroadcasts/bind",
            params={"id": broadcast_id, "streamId": stream_id, "part": "id,contentDetails"},
        )
        return {"broadcast_id": broadcast_id, "stream_id": stream_id, "bound": True}

    return _run(run)


@mcp.tool()
def youtube_transition_broadcast(broadcast_id: str, status: str) -> dict[str, Any]:
    """방송 상태를 전환한다 (50 units).

    Args:
        status: `testing`(미리보기) · `live`(송출 시작) · `complete`(종료).
            testing 을 건너뛰고 바로 live 로 가지 마세요 — 소리·화면을 확인할
            마지막 기회입니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        allowed = {"testing", "live", "complete"}
        if status not in allowed:
            return {
                "ok": False,
                "error": "invalid_input",
                "message": f"status 는 {sorted(allowed)} 중 하나여야 합니다.",
            }
        data = (
            client.post(
                "liveBroadcasts.transition",
                "liveBroadcasts/transition",
                params={
                    "id": broadcast_id,
                    "broadcastStatus": status,
                    "part": "id,status",
                },
            )
            or {}
        )
        result = {
            "broadcast_id": broadcast_id,
            "status": data.get("status", {}).get("lifeCycleStatus", status),
        }
        if status == "complete":
            result["next_step"] = (
                "다시보기 제목·설명을 정리하고 챕터를 넣으세요. 라이브 제목 그대로 두면 검색에서 묻힙니다."
            )
        return result

    return _run(run)


@mcp.tool()
def youtube_list_broadcasts(status: str = "upcoming", max_results: int = 10) -> dict[str, Any]:
    """내 방송 목록 (1 unit).

    Args:
        status: `upcoming` · `active` · `completed`.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.get(
                "liveBroadcasts.list",
                "liveBroadcasts",
                {
                    "part": "snippet,status",
                    "broadcastStatus": status,
                    "broadcastType": "all",
                    "maxResults": min(max(max_results, 1), 50),
                },
            )
            or {}
        )
        broadcasts = [
            {
                "broadcast_id": item.get("id"),
                "title": item.get("snippet", {}).get("title"),
                "scheduled_start": item.get("snippet", {}).get("scheduledStartTime"),
                "live_chat_id": item.get("snippet", {}).get("liveChatId"),
                "status": item.get("status", {}).get("lifeCycleStatus"),
            }
            for item in data.get("items", [])
        ]
        return {"broadcasts": broadcasts}

    return _run(run)


# ---------------------------------------------------------------------------
# 실시간 채팅
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_read_live_chat(
    live_chat_id: str, max_results: int = 50, page_token: str | None = None
) -> dict[str, Any]:
    """실시간 채팅을 읽는다 (1 unit).

    질문은 오는 대로 답하지 말고 구간 단위로 모아서 답하는 편이 진행에 낫습니다.
    `next_page_token` 을 다음 호출에 넘기면 이어서 읽습니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.get(
                "liveChatMessages.list",
                "liveChat/messages",
                {
                    "liveChatId": live_chat_id,
                    "part": "snippet,authorDetails",
                    "maxResults": min(max(max_results, 1), 200),
                    "pageToken": page_token,
                },
            )
            or {}
        )
        messages = [
            {
                "message_id": item.get("id"),
                "author": item.get("authorDetails", {}).get("displayName"),
                "is_moderator": item.get("authorDetails", {}).get("isChatModerator"),
                "text": item.get("snippet", {}).get("displayMessage"),
                "published_at": item.get("snippet", {}).get("publishedAt"),
            }
            for item in data.get("items", [])
        ]
        return {
            "messages": messages,
            "next_page_token": data.get("nextPageToken"),
            "polling_interval_ms": data.get("pollingIntervalMillis"),
        }

    return _run(run)


@mcp.tool()
def youtube_send_live_chat(live_chat_id: str, text: str) -> dict[str, Any]:
    """실시간 채팅에 메시지를 보낸다 (50 units).

    사용자의 채널 이름으로 나갑니다. 보내기 전에 문구를 확인받으세요.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.post(
                "liveChatMessages.insert",
                "liveChat/messages",
                params={"part": "snippet"},
                body={
                    "snippet": {
                        "liveChatId": live_chat_id,
                        "type": "textMessageEvent",
                        "textMessageDetails": {"messageText": text},
                    }
                },
            )
            or {}
        )
        return {"message_id": data.get("id"), "sent": True}

    return _run(run)


@mcp.tool()
def youtube_moderate_live_chat(message_id: str) -> dict[str, Any]:
    """실시간 채팅 메시지를 삭제한다 (50 units).

    악성 메시지에는 논쟁하지 말고 바로 지우는 편이 낫습니다 — 방송 중 해명은
    판을 키웁니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        client.call(
            "liveChatMessages.insert",  # 삭제도 쓰기 단가로 계산한다
            "DELETE",
            "liveChat/messages",
            params={"id": message_id},
        )
        return {"message_id": message_id, "deleted": True}

    return _run(run)


# ---------------------------------------------------------------------------
# 댓글
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_list_comments(video_id: str, max_results: int = 20, page_token: str | None = None) -> dict[str, Any]:
    """영상의 댓글을 읽는다 (1 unit)."""

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.get(
                "commentThreads.list",
                "commentThreads",
                {
                    "part": "snippet",
                    "videoId": video_id,
                    "maxResults": min(max(max_results, 1), 100),
                    "order": "time",
                    "pageToken": page_token,
                },
            )
            or {}
        )
        comments = []
        for item in data.get("items", []):
            top = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
            comments.append(
                {
                    "comment_id": item.get("snippet", {}).get("topLevelComment", {}).get("id"),
                    "author": top.get("authorDisplayName"),
                    "text": top.get("textOriginal"),
                    "like_count": top.get("likeCount"),
                    "published_at": top.get("publishedAt"),
                    "reply_count": item.get("snippet", {}).get("totalReplyCount"),
                }
            )
        return {"comments": comments, "next_page_token": data.get("nextPageToken")}

    return _run(run)


@mcp.tool()
def youtube_reply_comment(parent_comment_id: str, text: str) -> dict[str, Any]:
    """댓글에 답글을 단다 (50 units).

    사용자의 이름으로 나갑니다. 등록 전에 반드시 문구를 확인받으세요.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.post(
                "comments.insert",
                "comments",
                params={"part": "snippet"},
                body={"snippet": {"parentId": parent_comment_id, "textOriginal": text}},
            )
            or {}
        )
        return {"comment_id": data.get("id"), "replied": True}

    return _run(run)


@mcp.tool()
def youtube_moderate_comment(comment_id: str, action: str = "rejected") -> dict[str, Any]:
    """댓글을 숨기거나 공개한다 (50 units).

    Args:
        action: `rejected`(숨김) · `published`(공개) · `heldForReview`(검토 보류).
            협박·허위사실처럼 법적 다툼 소지가 있으면 지우기 전에 화면을 먼저
            보존하세요 — 삭제하면 신고 자료가 사라집니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        allowed = {"rejected", "published", "heldForReview"}
        if action not in allowed:
            return {
                "ok": False,
                "error": "invalid_input",
                "message": f"action 은 {sorted(allowed)} 중 하나여야 합니다.",
            }
        client.post(
            "comments.setModerationStatus",
            "comments/setModerationStatus",
            params={"id": comment_id, "moderationStatus": action},
        )
        return {"comment_id": comment_id, "moderation_status": action}

    return _run(run)


# ---------------------------------------------------------------------------
# 분석 (Analytics API — Data API 할당량을 쓰지 않는다)
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_channel_report(
    start_date: str,
    end_date: str,
    metrics: str = "views,estimatedMinutesWatched,averageViewDuration,subscribersGained",
    dimensions: str | None = "day",
) -> dict[str, Any]:
    """채널 성과를 기간별로 조회한다 (할당량 무료).

    Args:
        start_date: `YYYY-MM-DD`.
        end_date: `YYYY-MM-DD`.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = client.get(
            "analytics.query",
            "reports",
            {
                "ids": f"channel=={client.config.channel_id or 'MINE'}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
                "dimensions": dimensions,
            },
            base=client.config.analytics_base,
        )
        return {"report": data}

    return _run(run)


@mcp.tool()
def youtube_video_report(
    video_id: str,
    start_date: str,
    end_date: str,
    metrics: str = "views,estimatedMinutesWatched,averageViewPercentage,likes,comments",
) -> dict[str, Any]:
    """영상 한 편의 성과 (할당량 무료)."""

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = client.get(
            "analytics.query",
            "reports",
            {
                "ids": f"channel=={client.config.channel_id or 'MINE'}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": metrics,
                "filters": f"video=={video_id}",
            },
            base=client.config.analytics_base,
        )
        return {"video_id": video_id, "report": data}

    return _run(run)


@mcp.tool()
def youtube_traffic_sources(start_date: str, end_date: str, video_id: str | None = None) -> dict[str, Any]:
    """유입 경로 구성 (할당량 무료).

    노출이 부족한지, 클릭이 부족한지 가르는 첫 단서입니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        params = {
            "ids": f"channel=={client.config.channel_id or 'MINE'}",
            "startDate": start_date,
            "endDate": end_date,
            "metrics": "views,estimatedMinutesWatched",
            "dimensions": "insightTrafficSourceType",
            "sort": "-views",
        }
        if video_id:
            params["filters"] = f"video=={video_id}"
        data = client.get("analytics.query", "reports", params, base=client.config.analytics_base)
        return {"report": data}

    return _run(run)


@mcp.tool()
def youtube_audience_retention(video_id: str, start_date: str, end_date: str) -> dict[str, Any]:
    """시청 유지 곡선 (할당량 무료).

    어느 지점에서 이탈이 급증하는지 특정할 때 씁니다. 초반 이탈과 중간 이탈은
    처방이 다릅니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = client.get(
            "analytics.query",
            "reports",
            {
                "ids": f"channel=={client.config.channel_id or 'MINE'}",
                "startDate": start_date,
                "endDate": end_date,
                "metrics": "audienceWatchRatio,relativeRetentionPerformance",
                "dimensions": "elapsedVideoTimeRatio",
                "filters": f"video=={video_id};audienceType==ORGANIC",
            },
            base=client.config.analytics_base,
        )
        return {"video_id": video_id, "retention": data}

    return _run(run)


# ---------------------------------------------------------------------------
# 자막
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_list_captions(video_id: str) -> dict[str, Any]:
    """영상에 등록된 자막 트랙 목록 (50 units)."""

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = client.get("captions.list", "captions", {"part": "snippet", "videoId": video_id}) or {}
        tracks = [
            {
                "caption_id": item.get("id"),
                "language": item.get("snippet", {}).get("language"),
                "name": item.get("snippet", {}).get("name"),
                "is_auto": item.get("snippet", {}).get("trackKind") == "ASR",
            }
            for item in data.get("items", [])
        ]
        return {"captions": tracks}

    return _run(run)


@mcp.tool()
def youtube_upload_caption(
    video_id: str, file_path: str, language: str = "ko", name: str = ""
) -> dict[str, Any]:
    """자막 파일을 등록한다 (400 units — 이 서버에서 가장 비쌉니다).

    Args:
        file_path: SRT 또는 SBV 자막 파일 경로.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        data = (
            client.resumable_upload(
                "captions.insert",
                "captions",
                file_path=file_path,
                metadata={
                    "snippet": {"videoId": video_id, "language": language, "name": name}
                },
                params={"part": "snippet"},
                content_type="application/octet-stream",
            )
            or {}
        )
        return {"caption_id": data.get("id"), "video_id": video_id, "language": language}

    return _run(run)


# ---------------------------------------------------------------------------
# 운영
# ---------------------------------------------------------------------------


@mcp.tool()
def youtube_quota_status() -> dict[str, Any]:
    """오늘 남은 할당량 추정치를 확인한다 (무료).

    정확한 값은 Google Cloud 콘솔이 정본입니다. 여기 숫자는 이 서버가 센 추정치로,
    같은 계정을 다른 도구가 함께 쓰고 있으면 실제 잔량은 더 적습니다.
    """

    def run(client: YouTubeClient) -> dict[str, Any]:
        return {"configured": client.config.configured}

    return _run(run)


def main() -> None:
    """stdio MCP 서버를 기동한다."""
    mcp.run()


if __name__ == "__main__":
    main()
