"""server.py 도우미 단위 테스트 — MCP 세션 기동 없이 함수 직접 호출.

검증:
  - 자격증명 미설정 시 ``_get_client()`` → ``None``, ``_setup_required_error()`` → setup_required dict
  - ``threads_publish_text`` 등 도구가 자격증명 없을 때 setup_required 에러 반환
    (FastMCP 의 ``@mcp.tool()`` 데코레이터는 원본 함수를 그대로 반환하므로 직접 호출 가능)
  - ``THREADS_PUBLISH_DELAY`` 환경변수 파싱 (기본 30, 테스트 0, 비정상값 폴백)
  - 자격증명이 있으면 싱글톤 클라이언트가 빌드되고 캐싱된다
"""

from __future__ import annotations

import os
import tempfile

import pytest

from moai_mcp_threads_poster import server


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """각 테스트마다 Threads/Instagram 자격증명/딜레이 환경변수를 비우고 싱글톤을 초기화.

    CLAUDE_PLUGIN_ROOT(스타일 프로필 기본 경로 해석용) 도 함께 정리한다.
    Instagram 자격증명(IG_ACCESS_TOKEN / IG_USER_ID) 과 IG 싱글톤도 정리.
    """
    for key in (
        "THREADS_ACCESS_TOKEN",
        "THREADS_USER_ID",
        "THREADS_PUBLISH_DELAY",
        "CLAUDE_PLUGIN_ROOT",
        "IG_ACCESS_TOKEN",
        "IG_USER_ID",
    ):
        monkeypatch.delenv(key, raising=False)
    server._reset_client_for_tests()
    server._reset_ig_client_for_tests()
    yield
    server._reset_client_for_tests()
    server._reset_ig_client_for_tests()


# --- 자격증명 게이트 -------------------------------------------------------------
def test_get_client_returns_none_when_creds_absent():
    assert server._get_client() is None


def test_load_credentials_returns_empty_when_unset():
    assert server._load_credentials() == ("", "")


def test_setup_required_error_shape():
    err = server._setup_required_error()
    assert err["error"] is True
    assert err["setup_required"] is True
    assert "THREADS_ACCESS_TOKEN" in err["message"]
    assert "THREADS_USER_ID" in err["message"]


# --- 도구 직접 호출 (creds 없음 → setup_required) ------------------------------
def test_publish_text_returns_setup_error_without_creds():
    out = server.threads_publish_text("안녕")
    assert out["setup_required"] is True
    assert out["error"] is True


def test_publish_image_returns_setup_error_without_creds():
    out = server.threads_publish_image("캡션", "https://example.com/p.png")
    assert out["setup_required"] is True


def test_publish_video_returns_setup_error_without_creds():
    out = server.threads_publish_video("", "https://example.com/v.mp4")
    assert out["setup_required"] is True


def test_get_profile_returns_setup_error_without_creds():
    out = server.threads_get_profile()
    assert out["setup_required"] is True


def test_refresh_token_returns_setup_error_without_creds():
    out = server.threads_refresh_token()
    assert out["setup_required"] is True


# --- 발행 지연 환경변수 ---------------------------------------------------------
def test_publish_delay_default_is_30():
    assert server._publish_delay_seconds() == 30.0


def test_publish_delay_reads_env(monkeypatch):
    monkeypatch.setenv("THREADS_PUBLISH_DELAY", "0")
    assert server._publish_delay_seconds() == 0.0


def test_publish_delay_invalid_falls_back_to_default(monkeypatch):
    monkeypatch.setenv("THREADS_PUBLISH_DELAY", "not-a-number")
    assert server._publish_delay_seconds() == 30.0


# --- 자격증명 있을 때 클라이언트 빌드 + 싱글톤 캐싱 ------------------------------
def test_get_client_builds_and_caches_when_creds_present(monkeypatch):
    monkeypatch.setenv("THREADS_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("THREADS_USER_ID", "UID")
    server._reset_client_for_tests()
    client = server._get_client()
    assert client is not None
    # 싱글톤 캐시: 두 번째 호출은 같은 인스턴스
    assert server._get_client() is client


def test_partial_creds_token_only_still_none(monkeypatch):
    monkeypatch.setenv("THREADS_ACCESS_TOKEN", "tok")
    # THREADS_USER_ID 만 빠진 경우 → None
    server._reset_client_for_tests()
    assert server._get_client() is None


# === 문체 프로필 도구 (style profile — additive) ==================================
# threads_style_save / threads_style_load 는 Threads 자격증명 불필요한 로컬 파일 I/O.
# 테스트는 반드시 tmp 경로(path= 명시 or CLAUDE_PLUGIN_ROOT=tmp) 를 써서 실제 플러그인
# .data/ 에 쓰지 않도록 한다. _clean_env(autouse) 가 CLAUDE_PLUGIN_ROOT 를 지우므로,
# 기본 경로 테스트는 명시적으로 CLAUDE_PLUGIN_ROOT 를 tmp 로 재설정한다.


def test_style_save_explicit_path_writes_file(tmp_path):
    p = tmp_path / "profile.md"
    out = server.threads_style_save("# 내 문체\n- 톤: 캐주얼", path=str(p))
    assert out["saved"] is True
    assert out["path"] == str(p)
    assert out["chars"] == len("# 내 문체\n- 톤: 캐주얼")
    assert p.read_text(encoding="utf-8") == "# 내 문체\n- 톤: 캐주얼"


def test_style_save_creates_missing_parent_dirs(tmp_path):
    # .data/ 디렉토리가 없어도 생성한다.
    p = tmp_path / "sub" / ".data" / "style-profile.md"
    out = server.threads_style_save("문체 프로필", path=str(p))
    assert out["saved"] is True
    assert p.exists()
    assert p.read_text(encoding="utf-8") == "문체 프로필"


def test_style_save_default_path_uses_claude_plugin_root(tmp_path, monkeypatch):
    # CLAUDE_PLUGIN_ROOT 를 tmp 로 잡으면 기본 경로가 그 아래로 해석된다.
    root = tmp_path / "pluginroot"
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(root))
    out = server.threads_style_save("- 톤: 반말", path=None)
    assert out["saved"] is True
    # 경로가 tmp root 아래 .data/style-profile.md
    assert str(root) in out["path"]
    assert out["path"].endswith("style-profile.md")
    assert os.path.exists(out["path"])
    # 실제 플러그인 .data/ 를 건드리지 않았는지 확인 (tmp 밖에 파일이 생기지 않음).
    assert os.path.dirname(out["path"]).startswith(str(tmp_path))


def test_style_save_rejects_non_string_profile():
    out = server.threads_style_save(12345, path="/tmp/whatever.md")  # type: ignore[arg-type]
    assert out["error"] is True
    assert "must be str" in out["message"]


def test_style_load_returns_exists_false_when_absent(tmp_path):
    p = tmp_path / "nope.md"
    out = server.threads_style_load(path=str(p))
    assert out["exists"] is False
    assert out["profile"] is None
    assert out["path"] == str(p)


def test_style_load_reads_back_what_was_saved(tmp_path):
    p = tmp_path / "profile.md"
    server.threads_style_save("# 스타일\n- 시그니처: ~~~", path=str(p))
    out = server.threads_style_load(path=str(p))
    assert out["exists"] is True
    assert out["profile"] == "# 스타일\n- 시그니처: ~~~"
    assert out["path"] == str(p)


def test_style_save_then_load_roundtrip_default_path(tmp_path, monkeypatch):
    # 기본 경로로 save → load 라운드트립 (CLAUDE_PLUGIN_ROOT=tmp).
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path / "pluginroot"))
    saved = server.threads_style_save("라운드트립 본문", path=None)
    assert saved["saved"] is True
    loaded = server.threads_style_load(path=None)
    assert loaded["exists"] is True
    assert loaded["profile"] == "라운드트립 본문"
    assert loaded["path"] == saved["path"]


def test_style_tools_do_not_require_threads_creds():
    # 자격증명 없이도 (autouse _clean_env 가 비움) 에러 없이 동작해야 한다.
    # setup_required 게이트를 거치지 않는다.
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "x.md")
        out = server.threads_style_save("hi", path=p)
        assert out["saved"] is True
        out2 = server.threads_style_load(path=p)
        assert out2["exists"] is True


# === M3: Instagram MCP 도구 (SPEC-THREADS-POSTER-INSTAGRAM-001) ====================
# AC-M3-1..M3-12: IG 싱글톤, setup_required, 즉시 발행 도구(image/video/reel),
# 댓글·인사이트 도구, threads 도구 보존.


class StubInstagramClient:
    """테스트용 InstagramClient stub — HTTP 없이 호출을 기록한다."""

    def __init__(self):
        self.calls: list[tuple] = []

    def create_container(self, media_type, **kwargs):
        # 실제 InstagramClient 의 JPEG-only 검증을 흉내내어 서버 에러 처리를 시험한다.
        image_url = kwargs.get("image_url")
        if (
            media_type == "IMAGE"
            and image_url
            and image_url.lower().split("?", 1)[0].endswith(".png")
        ):
            raise ValueError(
                "Instagram 은 PNG 를 지원하지 않습니다 — JPEG 만 허용됩니다 "
                "(Instagram is JPEG-only; PNG is not supported)."
            )
        self.calls.append(("create_container", media_type, kwargs))
        return "IGC"

    def publish(self, creation_id):
        self.calls.append(("publish", creation_id))
        return "IGM"

    def wait_until_finished(self, creation_id, **kwargs):
        self.calls.append(("wait_until_finished", creation_id))
        return "FINISHED"

    def get_profile(self):
        self.calls.append(("get_profile",))
        return {"username": "goos", "id": "IGID", "followers_count": 1}

    def refresh_token(self):
        self.calls.append(("refresh_token",))
        return "newtok"

    def get_publish_limit(self):
        return {"data": [{"quota_usage": 0, "config": {"quota_total": 100}}]}

    def comments_list(self, media_id):
        self.calls.append(("comments_list", media_id))
        return {"data": []}

    def comments_reply(self, comment_id, text):
        self.calls.append(("comments_reply", comment_id, text))
        return {"id": "c"}

    def comments_hide(self, comment_id):
        self.calls.append(("comments_hide", comment_id))
        return {"hidden": True}

    def insights(self, *a, **kw):
        self.calls.append(("insights", a, kw))
        return {"data": []}

    def close(self):
        pass


# --- IG 자격증명 게이트 -----------------------------------------------------------
def test_ig_get_client_returns_none_when_creds_absent():
    assert server._get_ig_client() is None


def test_ig_setup_required_error_shape():
    err = server._ig_setup_required_error()
    assert err["error"] is True
    assert err["setup_required"] is True
    assert "IG_ACCESS_TOKEN" in err["message"]
    assert "IG_USER_ID" in err["message"]


def test_ig_get_client_builds_when_creds_present(monkeypatch):
    monkeypatch.setenv("IG_ACCESS_TOKEN", "tok")
    monkeypatch.setenv("IG_USER_ID", "IGID")
    server._reset_ig_client_for_tests()
    c1 = server._get_ig_client()
    assert c1 is not None
    # 싱글톤 캐시
    assert server._get_ig_client() is c1
    c1.close()


# --- 즉시 발행 도구 / setup_required (AC-M3-2, AC-M3-11) -------------------------
def test_instagram_get_profile_returns_setup_error_without_creds():
    out = server.instagram_get_profile()
    assert out["setup_required"] is True
    assert out["error"] is True


def test_instagram_publish_image_returns_setup_error_without_creds():
    out = server.instagram_publish_image("캡션", "https://example.com/p.jpg")
    assert out["setup_required"] is True


def test_instagram_publish_video_returns_setup_error_without_creds():
    out = server.instagram_publish_video("", "https://example.com/v.mp4")
    assert out["setup_required"] is True


def test_instagram_publish_reel_returns_setup_error_without_creds():
    out = server.instagram_publish_reel("캡션", "https://example.com/r.mp4")
    assert out["setup_required"] is True


def test_instagram_publish_image_happy_path_with_stub(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    out = server.instagram_publish_image("캡션", "https://example.com/p.jpg")
    assert out["media_id"] == "IGM"
    assert out["container_id"] == "IGC"
    assert "instagram.com" in out["permalink_hint"]
    # IMAGE 는 폴링 없이 create → publish
    names = [c[0] for c in stub.calls]
    assert "create_container" in names and "publish" in names
    assert "wait_until_finished" not in names


def test_instagram_publish_video_polls_before_publish(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    server.instagram_publish_video("캡션", "https://example.com/v.mp4")
    names = [c[0] for c in stub.calls]
    assert names.index("wait_until_finished") > names.index("create_container")
    assert names.index("publish") > names.index("wait_until_finished")


def test_instagram_publish_reel_passes_share_to_feed(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    server.instagram_publish_reel("캡션", "https://example.com/r.mp4", share_to_feed=True)
    create_call = [c for c in stub.calls if c[0] == "create_container"][0]
    assert create_call[1] == "REELS"
    # stub 읔 실제 클라이언트의 bool→"true" 변환 전 값을 기록한다 (전달 자체를 검증).
    assert create_call[2]["share_to_feed"] is True


def test_instagram_publish_image_png_rejected(monkeypatch):
    """EC-1: PNG URL 은 클라이언트가 ValueError → _error_dict 반환 (서버 크래시 없음)."""
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    out = server.instagram_publish_image("캡션", "https://example.com/p.png")
    assert out["error"] is True
    assert "JPEG" in out["message"]


def test_instagram_get_profile_happy_path(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    out = server.instagram_get_profile()
    assert out["username"] == "goos"


def test_instagram_refresh_token_happy_path(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    out = server.instagram_refresh_token()
    assert out["access_token"] == "newtok"


def test_instagram_comments_and_insights_tools_callable(monkeypatch):
    stub = StubInstagramClient()
    monkeypatch.setattr(server, "_get_ig_client", lambda: stub)
    assert server.instagram_comments_list("MID")["data"] == []
    assert server.instagram_comments_reply("CID", "답글")["id"] == "c"
    assert server.instagram_comments_hide("CID")["hidden"] is True
    assert "data" in server.instagram_insights()
