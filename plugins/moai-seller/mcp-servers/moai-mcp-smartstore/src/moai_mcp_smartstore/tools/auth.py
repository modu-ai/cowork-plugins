"""인증/연결 진단 도구."""
from __future__ import annotations

from ..server import mcp
from ._common import call, config_status


@mcp.tool()
def smartstore_test_connection() -> dict:
    """네이버 커머스 API 인증·연결을 검증한다.

    GET /v1/seller/account 를 1회 호출해 토큰 발급 → Bearer 인증 → 도메인 API 응답
    전체 흐름이 정상 동작하는지 확인한다. 자격증명 연동 후 첫 1회 호출 검증용.

    Returns:
        {"ok": true, "data": {계정 정보}} 또는 {"ok": false, "error": ...}
    """
    return call("GET", "/v1/seller/account", endpoint="GET /v1/seller/account")


@mcp.tool()
def smartstore_config_status() -> dict:
    """네이버 커머스 API 자격증환경변수 설정 상태를 반환한다 (API 미호출, 비밀키 원문 제외).

    Returns:
        {"configured": bool, "type": "SELF"|"SELLER", "base_url": str,
         "account_id_set": bool, "client_id_set": bool}
    """
    return config_status()
