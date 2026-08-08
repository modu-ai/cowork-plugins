"""YouTubeClient — 할당량 연동·검색 캐시·search 회피."""

from __future__ import annotations

import httpx
import pytest

from conftest import Recorder, make_client
from moai_mcp_core import QuotaExhausted, SetupRequired


def test_호출하면_할당량이_깎인다(config):
    rec = Recorder({"/videos": httpx.Response(200, json={"items": []})})
    client = make_client(config, rec)

    client.get("videos.list", "videos", {"part": "snippet", "id": "v1"})
    assert client.ledger.used == 1

    client.search({"part": "snippet", "q": "고양이"})
    assert client.ledger.used == 101


def test_같은_검색은_캐시에서_돌려주고_비용을_안_쓴다(config):
    """할당량 절약의 핵심. search 는 1회 100 units다."""
    calls = {"n": 0}

    def search_handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json={"items": [{"id": {"videoId": "v1"}}]})

    rec = Recorder({"/search": search_handler})
    client = make_client(config, rec)

    first = client.search({"part": "snippet", "q": "고양이"})
    second = client.search({"part": "snippet", "q": "고양이"})

    assert first == second
    assert calls["n"] == 1  # 실제 호출은 한 번
    assert client.ledger.used == 100  # 두 번 썼다면 200이었을 것


def test_조건이_다른_검색은_따로_호출한다(config):
    calls = {"n": 0}

    def search_handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json={"items": []})

    rec = Recorder({"/search": search_handler})
    client = make_client(config, rec)
    client.search({"q": "고양이"})
    client.search({"q": "강아지"})
    assert calls["n"] == 2


def test_한도를_넘길_호출은_아예_보내지_않는다(config):
    """호출하고 실패하는 것보다 안 하는 게 낫다 — 실패해도 할당량은 소모된다."""
    config = type(config)(**{**config.__dict__, "daily_limit": 50})
    rec = Recorder()
    client = make_client(config, rec)

    with pytest.raises(QuotaExhausted) as err:
        client.search({"q": "고양이"})  # 100 units > 50

    assert rec.paths() == []  # 네트워크로 나가지 않았다
    assert err.value.to_dict()["error"] == "quota_exhausted"


def test_내_영상_목록은_search_를_쓰지_않는다(config):
    """search(100) 대신 channels+playlistItems(2) 로 같은 결과를 얻는다."""
    rec = Recorder(
        {
            "/channels": httpx.Response(
                200,
                json={"items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UU_test"}}}]},
            ),
            "/playlistItems": httpx.Response(200, json={"items": []}),
        }
    )
    client = make_client(config, rec)

    playlist_id = client.uploads_playlist_id()
    client.get("playlistItems.list", "playlistItems", {"playlistId": playlist_id})

    assert playlist_id == "UU_test"
    assert client.ledger.used == 2  # search 였다면 100
    assert "/youtube/v3/search" not in rec.paths()


def test_None_파라미터는_보내지_않는다(config):
    """유튜브 API는 빈 파라미터를 오류로 본다."""
    rec = Recorder({"/videos": httpx.Response(200, json={})})
    client = make_client(config, rec)
    client.get("videos.list", "videos", {"part": "snippet", "pageToken": None})

    query = rec.requests[-1].url.params
    assert "part" in query
    assert "pageToken" not in query


def test_자격증명이_없으면_setup_required(unconfigured):
    rec = Recorder()
    client = make_client(unconfigured, rec)

    with pytest.raises(SetupRequired) as err:
        client.get("videos.list", "videos", {"id": "v1"})

    result = err.value.to_dict()
    assert result["error"] == "setup_required"
    assert "YOUTUBE_CLIENT_ID" in result["details"]["missing_env"]
    assert rec.paths() == []  # 네트워크로 나가지 않았다


def test_분석_api는_다른_주소로_나가고_할당량을_안_쓴다(config):
    rec = Recorder({"analytics.test": httpx.Response(200, json={"rows": []})})
    client = make_client(config, rec)

    client.get(
        "analytics.query",
        "reports",
        {"ids": "channel==UC_test"},
        base=config.analytics_base,
    )

    assert client.ledger.used == 0
    assert "analytics.test" in str(rec.requests[-1].url)


def test_업로드는_2단계로_진행된다(config, tmp_path):
    """세션을 열고(Location) 파일을 올린다 — 큰 파일이 중간에 끊겨도 처음부터가 아니다."""
    video = tmp_path / "clip.mp4"
    video.write_bytes("영상바이트".encode() * 10)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "POST":
            return httpx.Response(200, headers={"Location": "https://upload.test/session/1"})
        return httpx.Response(200, json={"id": "vid_new"})

    rec = Recorder({"upload.test": handler})
    client = make_client(config, rec)

    result = client.resumable_upload(
        "videos.insert",
        "videos",
        file_path=str(video),
        metadata={"snippet": {"title": "제목"}},
        params={"part": "snippet"},
    )

    assert result["id"] == "vid_new"
    assert client.ledger.used == 100
    methods = [r.method for r in rec.requests if "upload.test" in str(r.url)]
    assert methods == ["POST", "PUT"]


def test_없는_파일을_올리려_하면_명확히_알려준다(config):
    rec = Recorder()
    client = make_client(config, rec)

    from moai_mcp_core import UpstreamError

    with pytest.raises(UpstreamError) as err:
        client.resumable_upload(
            "videos.insert", "videos", file_path="/없는/경로.mp4", metadata={}
        )
    assert "찾을 수 없습니다" in err.value.message
    assert client.ledger.used == 0
