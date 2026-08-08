"""Unit tests for ImwebClient — header injection, param shaping, refresh, errors."""

from __future__ import annotations

import httpx
import pytest
import respx

from moai_mcp_imweb.client import ImwebApiError, ImwebClient

BASE = "https://openapi.imweb.me"


@respx.mock
def test_bearer_header_injected(cfg):
    respx.get(f"{BASE}/site-info").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = ImwebClient(cfg)
    client.request("GET", "/site-info")
    sent = respx.calls[0].request
    assert sent.headers["authorization"] == "Bearer tok"


@respx.mock
def test_params_drop_none_and_bool_to_yn(cfg):
    route = respx.get(f"{BASE}/orders").mock(return_value=httpx.Response(200, json={"ok": True}))
    client = ImwebClient(cfg)
    client.request("GET", "/orders", params={"page": 1, "limit": None, "isDeliveryHold": True, "isGift": False})
    # limit=None must be dropped; booleans become Y/N
    q = dict(respx.calls[0].request.url.params)
    assert "limit" not in q
    assert q["page"] == "1"
    assert q["isDeliveryHold"] == "Y"
    assert q["isGift"] == "N"
    assert route.called


@respx.mock
def test_path_params_substitution(cfg):
    respx.get(f"{BASE}/orders/ORD123").mock(return_value=httpx.Response(200, json={"ord": 1}))
    client = ImwebClient(cfg)
    out = client.request("GET", "/orders/{orderNo}", path_params={"orderNo": "ORD123"})
    assert out == {"ord": 1}
    assert str(respx.calls[0].request.url) == f"{BASE}/orders/ORD123"


@respx.mock
def test_post_json_body(cfg):
    respx.post(f"{BASE}/products").mock(return_value=httpx.Response(200, json={"created": True}))
    client = ImwebClient(cfg)
    out = client.request("POST", "/products", json_body={"prodName": "테스트"})
    import json

    body = json.loads(respx.calls[0].request.content)
    assert body == {"prodName": "테스트"}
    assert out == {"created": True}


@respx.mock
def test_401_triggers_refresh_and_retry(cfg, monkeypatch):
    # First call -> 401, second call -> 200.
    respx.get(f"{BASE}/site-info").mock(
        side_effect=[
            httpx.Response(401, json={"code": "GW.AUTHN", "message": "expired"}),
            httpx.Response(200, json={"ok": True}),
        ]
    )
    respx.post(f"{BASE}/oauth2/token").mock(
        return_value=httpx.Response(200, json={"access_token": "newtok", "refresh_token": "newrtok"})
    )
    client = ImwebClient(cfg)
    out = client.request("GET", "/site-info")
    assert out == {"ok": True}
    # The retried request must carry the refreshed token.
    assert respx.calls.last.request.headers["authorization"] == "Bearer newtok"
    assert client._access == "newtok"


@respx.mock
def test_non_2xx_raises_api_error_with_code(cfg):
    respx.get(f"{BASE}/products/999").mock(
        return_value=httpx.Response(404, json={"code": "GW.NOT_FOUND", "message": "상품 없음"})
    )
    client = ImwebClient(cfg)
    with pytest.raises(ImwebApiError) as exc:
        client.request("GET", "/products/{prodNo}", path_params={"prodNo": "999"})
    assert exc.value.status == 404
    assert exc.value.code == "GW.NOT_FOUND"
    assert "상품 없음" in exc.value.message


@respx.mock
def test_401_without_refresh_config_raises(cfg):
    # No client_id/secret/refresh_token => cannot refresh, must surface the 401.
    from dataclasses import replace

    no_refresh = replace(cfg, client_id="", client_secret="", refresh_token="")
    respx.get(f"{BASE}/site-info").mock(return_value=httpx.Response(401, json={"code": "GW.AUTHN"}))
    client = ImwebClient(no_refresh)
    with pytest.raises(ImwebApiError) as exc:
        client.request("GET", "/site-info")
    assert exc.value.status == 401
