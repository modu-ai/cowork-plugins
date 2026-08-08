"""Shared fixtures for moai-imweb tests."""

from __future__ import annotations

import pytest

from moai_mcp_imweb._base import ImwebConfig


@pytest.fixture
def cfg() -> ImwebConfig:
    return ImwebConfig(
        api_base="https://openapi.imweb.me",
        client_id="cid",
        client_secret="csec",
        access_token="tok",
        refresh_token="rtok",
        unit_code="KRW",
        timeout=10.0,
        token_file=None,
        request_delay=0.0,
    )
