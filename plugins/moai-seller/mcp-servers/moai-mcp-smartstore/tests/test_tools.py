"""도구(call 헬퍼) 동작 검증 — 미설정 안전 응답 + 모의 클라이언트 라우팅."""
from __future__ import annotations

from typing import Any

import pytest

from moai_mcp_smartstore import tools as tools_pkg
from moai_mcp_smartstore.tools import _common
from moai_mcp_smartstore.tools import products as products_tools


class _FakeClient:
    def __init__(self, response: Any):
        self._response = response
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, path: str, *, params=None, json=None) -> Any:
        self.calls.append((method, path, {"params": params, "json": json}))
        return self._response


@pytest.fixture
def clean_env(monkeypatch):
    """자격증명 환경변수 전부 제거."""
    for k in (
        "NAVER_COMMERCE_CLIENT_ID",
        "NAVER_COMMERCE_CLIENT_SECRET",
        "NAVER_COMMERCE_ACCOUNT_ID",
        "NAVER_COMMERCE_TYPE",
        "NAVER_COMMERCE_BASE_URL",
        "NAVER_COMMERCE_TIMEOUT",
    ):
        monkeypatch.delenv(k, raising=False)
    # 싱글톤 클라이언트 초기화
    _common.get_client.__wrapped__ if hasattr(_common.get_client, "__wrapped__") else None
    import moai_mcp_smartstore.client as client_mod

    client_mod.reset_client()
    yield monkeypatch
    client_mod.reset_client()


def test_config_status_unconfigured(clean_env):
    from moai_mcp_smartstore.tools.auth import smartstore_config_status

    status = smartstore_config_status()
    assert status["configured"] is False
    assert status["client_id_set"] is False
    # 비밀키 원문 노출 금지
    assert "client_secret" not in status


def test_tool_returns_not_configured_without_credentials(clean_env):
    """자격증명 미설정 시 도구는 예외 대신 안전한 not_configured dict 반환."""
    result = products_tools.category_list()
    assert result["ok"] is False
    assert result["error"] == "not_configured"
    assert "message" in result


def test_tool_routes_through_client_when_configured(clean_env, monkeypatch):
    """자격증명 설정 + 모의 클라이언트 주입 시 도구가 클라이언트로 라우팅된다."""
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_ID", "cid")
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_SECRET", "$2b$10$abcdefghijklmnopqrstuvwxyz012345")
    monkeypatch.setenv("NAVER_COMMERCE_TYPE", "SELF")

    fake = _FakeClient({"categories": [{"id": 1}]})
    monkeypatch.setattr(_common, "get_client", lambda: fake)

    result = products_tools.category_list()
    assert result["ok"] is True
    assert result["endpoint"] == "GET /v1/categories"
    assert result["data"] == {"categories": [{"id": 1}]}
    assert fake.calls == [("GET", "/v1/categories", {"params": None, "json": None})]


def test_tool_swallows_api_error_into_dict(clean_env, monkeypatch):
    """API 에러는 예외 전파 대신 ok=False dict 로 변환된다."""
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_ID", "cid")
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_SECRET", "$2b$10$abcdefghijklmnopqrstuvwxyz012345")

    from moai_mcp_smartstore.errors import ApiError

    class _ErrClient:
        def request(self, *a, **k):
            raise ApiError(500, "boom")

    monkeypatch.setattr(_common, "get_client", lambda: _ErrClient())

    result = products_tools.category_list()
    assert result["ok"] is False
    assert result["error"] == "ApiError"
    assert result["status"] == 500


def test_stats_invalid_dataset_rejected(clean_env, monkeypatch):
    """stats 도구는 허용 dataset 외 값을 클라이언트 호출 없이 거부한다."""
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_ID", "cid")
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_SECRET", "$2b$10$abcdefghijklmnopqrstuvwxyz012345")

    from moai_mcp_smartstore.tools.stats import stats_marketing

    result = stats_marketing("ch-1", "not-a-real-dataset")
    assert result["ok"] is False
    assert result["error"] == "invalid_dataset"


def test_stats_valid_dataset_routes(clean_env, monkeypatch):
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_ID", "cid")
    monkeypatch.setenv("NAVER_COMMERCE_CLIENT_SECRET", "$2b$10$abcdefghijklmnopqrstuvwxyz012345")

    from moai_mcp_smartstore.tools.stats import stats_marketing

    fake = _FakeClient({"rows": []})
    monkeypatch.setattr(_common, "get_client", lambda: fake)
    result = stats_marketing("ch-1", "all-daily", {"startDate": "2024-01-01"})
    assert result["ok"] is True
    assert fake.calls[0][1] == "/v1/bizdata-stats/channels/ch-1/marketing/all-daily"
