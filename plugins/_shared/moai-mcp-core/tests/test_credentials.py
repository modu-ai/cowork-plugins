"""자격증명 해석 테스트.

가장 중요한 케이스는 '확장되지 않은 자리표시자를 값으로 믿지 않는다' 이다. 실제 결함이
거기서 났고, 그 결함은 서버가 정상 기동하기 때문에 아무 신호도 내지 않았다.
"""

from __future__ import annotations

import json

import pytest

from moai_mcp_core.credentials import CredentialStore, is_unset, load


@pytest.fixture
def creds_file(tmp_path):
    def _write(payload: dict) -> "object":
        path = tmp_path / "svc.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    return _write


class TestIsUnset:
    @pytest.mark.parametrize(
        "value",
        [
            None,
            "",
            "   ",
            "${NAVER_COMMERCE_CLIENT_ID}",
            "${user_config.DART_API_KEY}",
            "  ${KEY}  ",
        ],
    )
    def test_미설정으로_본다(self, value):
        assert is_unset(value) is True

    @pytest.mark.parametrize(
        "value",
        [
            "real-key",
            "${incomplete",
            "prefix-${KEY}",  # 부분 치환 실패는 자리표시자가 아니라 이상한 값 — 그대로 통과시킨다
            "0",
        ],
    )
    def test_설정된_값으로_본다(self, value):
        assert is_unset(value) is False


class TestPrecedence:
    def test_환경변수가_파일을_이긴다(self, creds_file, monkeypatch):
        path = creds_file({"API_KEY": "from-file"})
        monkeypatch.setenv("API_KEY", "from-env")
        assert CredentialStore("svc", path=path).get("API_KEY") == "from-env"

    def test_자리표시자_환경변수는_파일에게_양보한다(self, creds_file, monkeypatch):
        path = creds_file({"API_KEY": "from-file"})
        monkeypatch.setenv("API_KEY", "${API_KEY}")
        assert CredentialStore("svc", path=path).get("API_KEY") == "from-file"

    def test_빈_환경변수는_파일에게_양보한다(self, creds_file, monkeypatch):
        # Claude 의 ${user_config.KEY} 는 미입력 시 빈 문자열로 치환된다(실측).
        path = creds_file({"API_KEY": "from-file"})
        monkeypatch.setenv("API_KEY", "")
        assert CredentialStore("svc", path=path).get("API_KEY") == "from-file"

    def test_둘_다_없으면_기본값(self, tmp_path, monkeypatch):
        monkeypatch.delenv("API_KEY", raising=False)
        store = CredentialStore("svc", path=tmp_path / "없는파일.json")
        assert store.get("API_KEY", "fallback") == "fallback"
        assert store.get("API_KEY") == ""


class TestFileHandling:
    def test_파일이_없어도_예외가_없다(self, tmp_path):
        store = CredentialStore("svc", path=tmp_path / "없음.json")
        assert store.get("ANY") == ""

    def test_손상된_JSON_은_없는_셈_친다(self, tmp_path, monkeypatch):
        path = tmp_path / "svc.json"
        path.write_text("{ 깨진 JSON", encoding="utf-8")
        monkeypatch.delenv("API_KEY", raising=False)
        assert CredentialStore("svc", path=path).get("API_KEY") == ""

    def test_객체가_아닌_JSON_은_없는_셈_친다(self, tmp_path, monkeypatch):
        path = tmp_path / "svc.json"
        path.write_text('["배열"]', encoding="utf-8")
        monkeypatch.delenv("API_KEY", raising=False)
        assert CredentialStore("svc", path=path).get("API_KEY") == ""

    def test_경로를_환경변수로_덮어쓴다(self, creds_file, monkeypatch):
        path = creds_file({"API_KEY": "from-override"})
        monkeypatch.setenv("SVC_CREDENTIALS_FILE", str(path))
        monkeypatch.delenv("API_KEY", raising=False)
        store = CredentialStore("svc", env_var="SVC_CREDENTIALS_FILE")
        assert store.get("API_KEY") == "from-override"

    def test_경로_덮어쓰기_변수가_자리표시자면_무시한다(self, monkeypatch):
        monkeypatch.setenv("SVC_CREDENTIALS_FILE", "${SVC_CREDENTIALS_FILE}")
        store = CredentialStore("svc", env_var="SVC_CREDENTIALS_FILE")
        assert store.path.name == "svc.json"


class TestReporting:
    def test_미설정_키를_보고한다(self, creds_file, monkeypatch):
        path = creds_file({"HAVE": "v"})
        monkeypatch.delenv("MISSING", raising=False)
        store = CredentialStore("svc", path=path)
        assert store.missing(["HAVE", "MISSING"]) == ["MISSING"]

    def test_안내문은_미설정_키와_경로를_담는다(self, creds_file, monkeypatch):
        path = creds_file({})
        monkeypatch.delenv("MISSING", raising=False)
        hint = CredentialStore("svc", path=path).setup_hint(["MISSING"])
        assert "MISSING" in hint
        assert str(path) in hint

    def test_전부_설정되면_안내문이_없다(self, creds_file):
        path = creds_file({"HAVE": "v"})
        assert CredentialStore("svc", path=path).setup_hint(["HAVE"]) == ""


def test_load_는_한번에_해석한다(creds_file, monkeypatch):
    path = creds_file({"A": "from-file", "B": "file-b"})
    monkeypatch.setenv("A", "from-env")
    monkeypatch.delenv("C", raising=False)
    assert load("svc", ["A", "B", "C"], path=path) == {
        "A": "from-env",
        "B": "file-b",
        "C": "",
    }
