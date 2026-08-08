"""도구 표면 — 라이브 순서·안전 기본값·오류를 응답으로 변환."""

from __future__ import annotations

import httpx
import pytest

from conftest import Recorder, make_client
from moai_mcp_youtube import server


@pytest.fixture(autouse=True)
def _isolate(config):
    """각 테스트가 자기 클라이언트를 쓰도록 싱글턴을 비운다."""
    yield
    server.reset_client(None)


def _install(config, routes) -> Recorder:
    rec = Recorder(routes)
    server.reset_client(make_client(config, rec))
    return rec


def test_모든_응답에_할당량_잔량이_담긴다(config):
    _install(config, {"/channels": httpx.Response(200, json={"items": [{"id": "UC_test"}]})})
    result = server.youtube_channel_profile()
    assert result["ok"] is True
    assert result["quota"]["remaining"] < result["quota"]["daily_limit"]


def test_자격증명이_없으면_안내를_돌려주고_죽지_않는다(unconfigured):
    _install(unconfigured, {})
    result = server.youtube_channel_profile()
    assert result["ok"] is False
    assert result["error"] == "setup_required"
    assert "YOUTUBE_CLIENT_ID" in result["details"]["missing_env"]


def test_업로드_기본_공개범위는_private(config, tmp_path):
    """실수로 공개되는 것보다 비공개가 안전하다."""
    video = tmp_path / "clip.mp4"
    video.write_bytes(b"x")

    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            import json

            captured.update(json.loads(request.content))
            return httpx.Response(200, headers={"Location": "https://upload.test/s/1"})
        return httpx.Response(200, json={"id": "v1", "status": {"privacyStatus": "private"}})

    _install(config, {"upload.test": handler})
    result = server.youtube_upload_video(file_path=str(video), title="제목")

    assert result["video_id"] == "v1"
    assert captured["status"]["privacyStatus"] == "private"


def test_라이브_방송_생성은_채팅_id를_돌려준다(config):
    """이 id 가 있어야 실시간 채팅 도구를 쓸 수 있다."""
    _install(
        config,
        {
            "/liveBroadcasts": httpx.Response(
                200, json={"id": "b1", "snippet": {"liveChatId": "chat1"}}
            )
        },
    )
    result = server.youtube_create_broadcast(title="방송", scheduled_start="2026-08-20T19:00:00+09:00")
    assert result["broadcast_id"] == "b1"
    assert result["live_chat_id"] == "chat1"
    assert "bind_stream" in result["next_step"]


def test_방송_상태_전환_순서를_지원한다(config):
    _install(
        config,
        {
            "/liveBroadcasts/transition": lambda r: httpx.Response(
                200,
                json={
                    "id": "b1",
                    "status": {"lifeCycleStatus": r.url.params.get("broadcastStatus")},
                },
            )
        },
    )
    assert server.youtube_transition_broadcast("b1", "testing")["status"] == "testing"
    assert server.youtube_transition_broadcast("b1", "live")["status"] == "live"

    done = server.youtube_transition_broadcast("b1", "complete")
    assert done["status"] == "complete"
    assert "다시보기" in done["next_step"]  # 종료 후 정리를 안내한다


def test_잘못된_전환_상태는_거부한다(config):
    rec = _install(config, {})
    result = server.youtube_transition_broadcast("b1", "시작")
    assert result["ok"] is False
    assert result["error"] == "invalid_input"
    assert rec.paths() == []  # 네트워크로 나가지 않았다


def test_잘못된_댓글_처리_상태는_거부한다(config):
    rec = _install(config, {})
    result = server.youtube_moderate_comment("c1", action="삭제")
    assert result["ok"] is False
    assert rec.paths() == []


def test_메타데이터_수정은_기존_값을_보존한다(config):
    """유튜브 API는 부분 수정을 지원하지 않는다 — 병합하지 않으면 설명이 날아간다."""
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "snippet": {
                                "title": "옛 제목",
                                "description": "지키고 싶은 설명",
                                "tags": ["기존태그"],
                                "categoryId": "22",
                            }
                        }
                    ]
                },
            )
        import json

        captured.update(json.loads(request.content))
        return httpx.Response(200, json={})

    _install(config, {"/videos": handler})
    server.youtube_update_metadata("v1", title="새 제목")

    assert captured["snippet"]["title"] == "새 제목"
    assert captured["snippet"]["description"] == "지키고 싶은 설명"
    assert captured["snippet"]["tags"] == ["기존태그"]


def test_없는_영상_수정은_친절하게_실패한다(config):
    _install(config, {"/videos": httpx.Response(200, json={"items": []})})
    result = server.youtube_update_metadata("없는id", title="제목")
    assert result["ok"] is False
    assert result["error"] == "not_found"


def test_내_영상_목록은_업로드_재생목록을_경유한다(config):
    rec = _install(
        config,
        {
            "/channels": httpx.Response(
                200,
                json={"items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UU1"}}}]},
            ),
            "/playlistItems": httpx.Response(
                200,
                json={
                    "items": [
                        {
                            "contentDetails": {"videoId": "v1", "videoPublishedAt": "2026-08-01"},
                            "snippet": {"title": "첫 영상"},
                        }
                    ]
                },
            ),
        },
    )
    result = server.youtube_list_my_videos()

    assert result["videos"][0]["video_id"] == "v1"
    assert result["quota"]["used"] == 2  # search 였다면 100
    assert not any("search" in p for p in rec.paths())


def test_검색은_반복해도_추가_비용이_없다(config):
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json={"items": []})

    _install(config, {"/search": handler})
    server.youtube_search("고양이")
    second = server.youtube_search("고양이")

    assert calls["n"] == 1
    assert second["quota"]["used"] == 100


def test_상대_서버_오류도_응답으로_돌려준다(config):
    """예외를 던지면 서버가 죽고 사용자는 원인을 모른다."""
    _install(config, {"/channels": httpx.Response(403, text="forbidden")})
    result = server.youtube_channel_profile()
    assert result["ok"] is False
    assert result["error"] == "upstream_error"
    assert result["details"]["status"] == 403


def test_분석_도구는_할당량을_쓰지_않는다(config):
    _install(config, {"analytics.test": httpx.Response(200, json={"rows": [[1, 2]]})})
    result = server.youtube_channel_report("2026-08-01", "2026-08-07")
    assert result["ok"] is True
    assert result["quota"]["used"] == 0


def test_도구가_모두_등록되어_있다():
    """FastMCP 에 실제로 붙었는지 확인한다."""
    import asyncio

    names = {t.name for t in asyncio.run(server.mcp.list_tools())}
    expected = {
        "youtube_channel_profile",
        "youtube_list_my_videos",
        "youtube_video_details",
        "youtube_search",
        "youtube_upload_video",
        "youtube_update_metadata",
        "youtube_set_thumbnail",
        "youtube_schedule_publish",
        "youtube_list_playlists",
        "youtube_create_playlist",
        "youtube_add_to_playlist",
        "youtube_create_broadcast",
        "youtube_bind_stream",
        "youtube_transition_broadcast",
        "youtube_list_broadcasts",
        "youtube_read_live_chat",
        "youtube_send_live_chat",
        "youtube_moderate_live_chat",
        "youtube_list_comments",
        "youtube_reply_comment",
        "youtube_moderate_comment",
        "youtube_channel_report",
        "youtube_video_report",
        "youtube_traffic_sources",
        "youtube_audience_retention",
        "youtube_list_captions",
        "youtube_upload_caption",
        "youtube_quota_status",
    }
    assert expected <= names
