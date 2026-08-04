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

from threads_poster import server


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """각 테스트마다 Threads 자격증명/딜레이/큐 환경변수를 비우고 싱글톤을 초기화.

    M2 큐 싱글톤과 큐 DB 환경변수(THREADS_POSTER_DB / CLAUDE_PLUGIN_ROOT) 도 함께
    정리한다 — 기존 M1 테스트에는 영향을 주지 않는다(additive).
    """
    for key in (
        "THREADS_ACCESS_TOKEN",
        "THREADS_USER_ID",
        "THREADS_PUBLISH_DELAY",
        "THREADS_POSTER_DB",
        "CLAUDE_PLUGIN_ROOT",
    ):
        monkeypatch.delenv(key, raising=False)
    server._reset_client_for_tests()
    server._reset_queue_for_tests()
    yield
    server._reset_client_for_tests()
    server._reset_queue_for_tests()


@pytest.fixture
def queue_db(tmp_path, monkeypatch):
    """M2 큐 도구 테스트용: DB 를 tmp_path 로 격리하고 큐 싱글톤을 초기화.

    autouse _clean_env(THREADS_POSTER_DB 삭제) 보다 나중에 설정되어 안전하게
    tmp 경로를 가리킨다.
    """
    db = tmp_path / "queue.db"
    monkeypatch.setenv("THREADS_POSTER_DB", str(db))
    server._reset_queue_for_tests()
    yield db
    server._reset_queue_for_tests()


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


# === M2: 큐 관리 도구 (additive) =================================================
def test_queue_add_returns_id_and_pending(queue_db):
    out = server.threads_queue_add("TEXT", text="안녕")
    assert "post_id" in out
    assert isinstance(out["post_id"], int)
    assert out["status"] == "PENDING"
    assert out["media_type"] == "TEXT"
    assert out["scheduled_at"] is None


def test_queue_approve_flips_status_to_approved(queue_db):
    added = server.threads_queue_add("TEXT", text="hi")
    pid = added["post_id"]
    out = server.threads_queue_approve(pid)
    assert out["status"] == "APPROVED"
    assert out["approved_at"] is not None
    # scheduled_at 기본 = now (즉시 due)
    assert out["scheduled_at"] is not None


def test_queue_approve_with_explicit_schedule(queue_db):
    added = server.threads_queue_add("TEXT", text="hi")
    out = server.threads_queue_approve(added["post_id"], scheduled_at="2099-01-01T00:00:00")
    assert out["scheduled_at"] == "2099-01-01T00:00:00"


def test_queue_approve_missing_post_returns_error(queue_db):
    out = server.threads_queue_approve(99999)
    assert out["error"] is True
    assert out["not_found"] is True


def test_queue_list_and_get_roundtrip(queue_db):
    added = server.threads_queue_add("TEXT", text="first")
    pid = added["post_id"]
    listed = server.threads_queue_list()
    assert listed["count"] >= 1
    detail = server.threads_queue_get(pid)
    assert detail["id"] == pid
    assert detail["text"] == "first"


def test_queue_get_missing_returns_not_found(queue_db):
    out = server.threads_queue_get(99999)
    assert out["error"] is True
    assert out["not_found"] is True


def test_queue_add_rejects_bad_media_type(queue_db):
    out = server.threads_queue_add("GIF")
    assert out["error"] is True
    assert "media_type" in out["message"]


def test_queue_publish_due_requires_creds(queue_db):
    """큐 수동 발행 도구는 자격증명이 필요하다 — setup_required 에러."""
    out = server.threads_queue_publish_due()
    assert out["setup_required"] is True


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
