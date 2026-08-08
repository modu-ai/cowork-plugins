"""
인증 전자서명(generate_signature) 테스트.

공식 인증 문서(https://apicenter.commerce.naver.com/docs/auth) 예시의
salt 값 `$2a$10$abcdefghijklmnopqrstuv` 은 bcrypt 5.x 가 "Invalid salt" 로
거부하는 비실용 placeholder 다. (관측 검증: bcrypt.gensalt() 로 생성된 진짜
salt 만 수용.) 반면 운영 환경에서 네이버가 발급하는 client_secret 은
bcrypt.gensalt() 로 만들어진 진짜 bcrypt salt 이므로 본 구현은 정상 동작한다.

따라서 본 테스트는:
  - 진짜 bcrypt salt 로 알고리즘 정확성을 검증하고,
  - 문서 예시 salt 가 bcrypt 5.x 에서 거부됨을 명시해 재현 함정을 기록한다.

공식 문서: https://apicenter.commerce.naver.com/docs/auth
"""
import base64

import bcrypt

from moai_mcp_smartstore.auth import generate_signature

# 테스트용 진짜 bcrypt salt (운영 client_secret 과 동일 형식).
_SALT = bcrypt.gensalt(rounds=10).decode("utf-8")
_CLIENT_ID = "aaaabbbbcccc"
_TIMESTAMP = 1643961623299


def test_signature_decodes_to_bcrypt_format_with_matching_salt():
    """서명은 base64 로 디코딩되어 진짜 bcrypt 해시($2)여야 하며, salt 접두사가 입력 salt 와 일치해야 한다."""
    sig = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    decoded = base64.standard_b64decode(sig).decode("utf-8")
    assert decoded.startswith("$2")
    # bcrypt 해시의 앞 29자는 "$2b$10$<22-char-salt>" — 입력 salt 접두사와 동일.
    assert decoded[: len(_SALT)] == _SALT


def test_signature_equals_direct_bcrypt_computation():
    """generate_signature 결과는 bcrypt+base64 직접 계산과 정확히 일치해야 한다."""
    password = f"{_CLIENT_ID}_{_TIMESTAMP}".encode("utf-8")
    expected = base64.standard_b64encode(
        bcrypt.hashpw(password, _SALT.encode("utf-8"))
    ).decode("utf-8")
    assert generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP) == expected


def test_signature_deterministic_for_fixed_salt():
    """동일 입력 → 동일 서명 (bcrypt 고정 salt 는 결정론적)."""
    a = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    b = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    assert a == b


def test_signature_changes_with_timestamp():
    a = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    b = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP + 1)
    assert a != b


def test_signature_changes_with_client_id():
    a = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    b = generate_signature("xxxxxxxxxxxx", _SALT, _TIMESTAMP)
    assert a != b


def test_signature_verifies_against_bcrypt_checkpw():
    """서명(디코딩 결과)은 bcrypt.checkpw 로 동일 password 검증에 통과해야 한다."""
    import pytest  # noqa

    sig = generate_signature(_CLIENT_ID, _SALT, _TIMESTAMP)
    decoded = base64.standard_b64decode(sig)
    password = f"{_CLIENT_ID}_{_TIMESTAMP}".encode("utf-8")
    assert bcrypt.checkpw(password, decoded)


def test_official_doc_example_salt_is_rejected_by_bcrypt5():
    """공식 문서 예시 salt 는 bcrypt 5.x 에서 Invalid salt 로 거부됨(재현 함정 기록).

    운영 client_secret 은 gensalt() 로 만들어진 진짜 salt 이므로 본 구현은 정상.
    """
    with pytest.raises(ValueError):
        bcrypt.hashpw(b"x", b"$2a$10$abcdefghijklmnopqrstuv")


# pytest 는 파일 하단에서 import (위 test_official_doc_example_salt_is_rejected_by_bcrypt5 사용)
import pytest  # noqa: E402
