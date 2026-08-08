"""moai-cafe24 테스트 공통 픽스처."""

from __future__ import annotations

import pytest

from moai_cafe24._base import Cafe24Config


@pytest.fixture
def cfg(tmp_path) -> Cafe24Config:
    return Cafe24Config(
        mall_id="testmall",
        client_id="cid",
        client_secret="csec",
        access_token="tok",
        refresh_token="rtok",
        api_version="2026-03-01",
        shop_no=1,
        timeout=10.0,
        token_file=tmp_path / "cafe24-tokens.json",
        request_delay=0.0,
    )
