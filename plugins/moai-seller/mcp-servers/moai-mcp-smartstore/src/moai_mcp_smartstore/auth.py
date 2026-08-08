"""
네이버 커머스 API 인증 전자서명 생성.

커머스API는 인증 토큰 발급 시 client_secret 원문을 직접 전송하지 않고,
bcrypt 전자서명(signature)을 전달한다. client_secret 자체가 bcrypt salt 로
사용된다.

전자서명 생성 규격 (공식 인증 문서 기준):
    1. password = client_id + "_" + timestamp
    2. hashed    = bcrypt.hashpw(password, client_secret)
    3. signature = base64.standard_b64encode(hashed)

timestamp 는 밀리초 단위 Unix 시간이며, 토큰 발급 시점 기준 5분간 유효하다.

공식 문서: https://apicenter.commerce.naver.com/docs/auth
"""
from __future__ import annotations

import base64

import bcrypt

__all__ = ["generate_signature"]


def generate_signature(client_id: str, client_secret: str, timestamp_ms: int) -> str:
    """인증 전자서명 생성.

    Args:
        client_id: 애플리케이션 ID.
        client_secret: 애플리케이션 시크릿 (bcrypt salt 로 사용).
        timestamp_ms: 밀리초 단위 Unix timestamp.

    Returns:
        base64 인코딩된 bcrypt 전자서명 문자열.
    """
    password = f"{client_id}_{timestamp_ms}".encode("utf-8")
    salt = client_secret.encode("utf-8")
    hashed = bcrypt.hashpw(password, salt)
    return base64.standard_b64encode(hashed).decode("utf-8")
