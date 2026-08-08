"""Verify category-dispatch tools delegate correctly to ImwebClient."""

from __future__ import annotations

import pytest


class _FakeClient:
    def __init__(self):
        self.calls = []

    def request(self, method, path, **kwargs):
        self.calls.append({"method": method, "path": path, **kwargs})
        return {"ok": True}

    def list_all_pages(self, path, **kwargs):
        return {"paginated": True, "path": path, **kwargs}


def _patch(monkeypatch, module):
    fake = _FakeClient()
    monkeypatch.setattr(module, "get_client", lambda: fake)
    return fake


def test_simple_get_dispatch(monkeypatch):
    import moai_mcp_imweb.tools.order as o

    fake = _patch(monkeypatch, o)
    o.imweb_order(action="read_all_parcel_company_list")
    assert fake.calls[-1] == {"method": "GET", "path": "/orders/parcel-company-list"}


def test_path_params_dispatch(monkeypatch):
    import moai_mcp_imweb.tools.order as o

    fake = _patch(monkeypatch, o)
    o.imweb_order(action="read_one_order_by_order_no", params={"orderNo": "ORD123"})
    c = fake.calls[-1]
    assert c["method"] == "GET"
    assert c["path"] == "/orders/{orderNo}"
    assert c["path_params"] == {"orderNo": "ORD123"}


def test_query_params_dispatch(monkeypatch):
    import moai_mcp_imweb.tools.order as o

    fake = _patch(monkeypatch, o)
    o.imweb_order(action="read_all_order", params={"page": 1, "limit": 50})
    c = fake.calls[-1]
    assert c["method"] == "GET" and c["path"] == "/orders"
    assert c["params"] == {"page": 1, "limit": 50}


def test_body_dispatch(monkeypatch):
    import moai_mcp_imweb.tools.product as p

    fake = _patch(monkeypatch, p)
    p.imweb_product(action="create_product_images", body=p.CreateProductImagesBody(images=["u1", "u2"]))
    c = fake.calls[-1]
    assert c["method"] == "POST" and c["path"] == "/products/{prodNo}/images"
    assert c["json_body"] == {"images": ["u1", "u2"]}


def test_paginate_routes_to_list_all_pages(monkeypatch):
    import moai_mcp_imweb.tools.order as o

    fake = _patch(monkeypatch, o)
    r = o.imweb_order(action="read_all_order", params={"orderSectionStatus": "SHIPPING_COMPLETE"}, paginate=True)
    assert r["paginated"] is True
    assert r["path"] == "/orders"
    # paginate must NOT also call request()
    assert fake.calls == []


def test_path_plus_body_dispatch(monkeypatch):
    import moai_mcp_imweb.tools.product as p

    fake = _patch(monkeypatch, p)
    p.imweb_product(
        action="create_product_images",
        params={"prodNo": 123},
        body=p.CreateProductImagesBody(images=["url"]),
    )
    c = fake.calls[-1]
    assert c["method"] == "POST" and c["path"] == "/products/{prodNo}/images"
    assert c["path_params"] == {"prodNo": 123}
    assert c["json_body"] == {"images": ["url"]}


def test_invalid_action_raises(monkeypatch):
    import moai_mcp_imweb.tools.order as o

    _patch(monkeypatch, o)
    with pytest.raises(KeyError):
        o.imweb_order(action="__nonexistent_action__")
