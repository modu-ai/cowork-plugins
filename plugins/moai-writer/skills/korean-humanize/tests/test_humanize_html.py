"""korean-humanize HTML 카피 일괄 윤문기(humanize_html.py) 자체 테스트.

Python 표준 라이브러리(unittest)만으로 실행한다. 픽스처 HTML은 인라인
문자열이며, 카피 치환이 텍스트 표면(본문 텍스트 노드·<title>·meta
description·og:*·JSON-LD 문자열 값)에만 닿고 <script>/<style>/<code>/<pre>
내용과 마크업 바이트는 그대로 보존되는지 검증한다.

검증 범위:
- 텍스트 표면 6종 치환 (body 텍스트·title·meta description·og:title·
  og:description·JSON-LD 문자열 값)
- skip 태그(<script>/<style>/<code>/<pre>) 내부 디코이 패턴 불가침
- 무매칭 규칙 → 입력과 바이트 동일(비텍스트 바이트 보존의 강한 검증)
- 태그 시퀀스 전후 동일(tag_balance_ok)
- 잔재(residual) 보고 — 치환 후에도 남는 before 패턴 카운트
- longest-before-first 적용 순서 + regex 규칙
- CLI: --check-only(쓰기 없음) / 전체 실행(--output 기록 + stdout JSON 요약)
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest

_TEST_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.abspath(os.path.join(_TEST_DIR, ".."))
_REFERENCES = os.path.join(_SKILL_ROOT, "references")
sys.path.insert(0, _REFERENCES)

import humanize_html  # noqa: E402  (sys.path 조작 의도적)

# 픽스처 — 치환 대상 카피가 텍스트 표면 6종에 배치되고, skip 태그 4종에는
# 절대 치환되면 안 되는 디코이 패턴이 들어 있다.
_FIXTURE_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<title>말 한마디에 굴러가는 자동화</title>
<meta charset="utf-8">
<meta name="description" content="자동화가 나 대신 일합니다. 더는 혼자가 아닙니다.">
<meta property="og:title" content="굴러가는 자동화">
<meta property="og:description" content="네 가지가 한 흐름으로 손발을 맞춥니다">
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "Course", "name": "굴러가는 자동화", "description": "자동화가 나 대신 일합니다"}
</script>
<style>
.hero { background: url("굴러가는 자동화.png"); }
</style>
</head>
<body>
<h1>말 한마디에 <strong>굴러가는 자동화</strong></h1>
<p>자동화가 나 대신 일합니다. 더는 혼자가 아닙니다.</p>
<pre>더는 혼자가 아닙니다 — pre 블록 보존</pre>
<code>replace("굴러가는 자동화", "x")</code>
<script>
console.log("굴러가는 자동화");
</script>
</body>
</html>
"""

_RULES = [
    {"before": "굴러가는 자동화", "after": "작동하는 AI 코워커"},
    {"before": "자동화가 나 대신 일합니다", "after": "AI 코워커가 대신 일해 줍니다"},
    {"before": "더는", "after": "이제는"},
    {"before": "한 흐름으로 손발을 맞춥니다", "after": "한 번에 맞물려 움직입니다"},
]


class HumanizeHtmlTransformTests(unittest.TestCase):
    """humanize_html() 직접 호출 — 치환·보존·검증 요약."""

    def setUp(self) -> None:
        self.result, self.summary = humanize_html.humanize_html(_FIXTURE_HTML, _RULES)

    def test_body_text_and_title_replaced(self) -> None:
        self.assertIn("<title>말 한마디에 작동하는 AI 코워커</title>", self.result)
        self.assertIn("<strong>작동하는 AI 코워커</strong>", self.result)
        self.assertIn(
            "<p>AI 코워커가 대신 일해 줍니다. 이제는 혼자가 아닙니다.</p>", self.result
        )

    def test_meta_and_og_attributes_replaced(self) -> None:
        self.assertIn(
            'content="AI 코워커가 대신 일해 줍니다. 이제는 혼자가 아닙니다."', self.result
        )
        self.assertIn('property="og:title" content="작동하는 AI 코워커"', self.result)
        self.assertIn(
            'property="og:description" content="네 가지가 한 번에 맞물려 움직입니다"',
            self.result,
        )

    def test_jsonld_string_values_replaced(self) -> None:
        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>', self.result, re.S
        )
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        self.assertEqual(data["name"], "작동하는 AI 코워커")
        self.assertEqual(data["description"], "AI 코워커가 대신 일해 줍니다")
        # 문자열 값만 치환 — 구조 키·비대상 값은 보존.
        self.assertEqual(data["@context"], "https://schema.org")
        self.assertEqual(data["@type"], "Course")

    def test_skip_tags_untouched(self) -> None:
        # <script>/<style>/<code>/<pre> 내부 디코이는 바이트 그대로.
        self.assertIn('console.log("굴러가는 자동화");', self.result)
        self.assertIn('.hero { background: url("굴러가는 자동화.png"); }', self.result)
        self.assertIn('replace("굴러가는 자동화", "x")', self.result)
        self.assertIn("<pre>더는 혼자가 아닙니다 — pre 블록 보존</pre>", self.result)

    def test_tag_sequence_preserved(self) -> None:
        self.assertTrue(self.summary["tag_balance_ok"])
        self.assertEqual(
            humanize_html._tag_sequence(_FIXTURE_HTML),
            humanize_html._tag_sequence(self.result),
        )

    def test_summary_counts(self) -> None:
        # title 1 + meta desc 2(장문 1 + 더는 1) + og:title 1 + og:desc 1
        # + JSON-LD 2(name + description) + <strong> 1 + <p> 2 = 10회 치환.
        self.assertEqual(self.summary["replacements_applied"], 10)
        # 변경 노드: title/meta desc/og:title/og:desc/JSON-LD/strong/p = 7.
        self.assertEqual(self.summary["changed_nodes"], 7)

    def test_all_residuals_zero_after_full_pass(self) -> None:
        # 치환 가능한 표면에서는 잔재 0 — skip 태그 디코이는 표면이 아니다.
        for before, count in self.summary["residuals"].items():
            self.assertEqual(count, 0, msg=before)

    def test_no_match_rules_return_byte_identical_document(self) -> None:
        result, summary = humanize_html.humanize_html(
            _FIXTURE_HTML, [{"before": "존재하지않는패턴", "after": "x"}]
        )
        self.assertEqual(result, _FIXTURE_HTML)
        self.assertEqual(summary["replacements_applied"], 0)
        self.assertEqual(summary["changed_nodes"], 0)
        self.assertEqual(summary["residuals"]["존재하지않는패턴"], 0)

    def test_residual_reporting_counts_leftovers(self) -> None:
        # after가 before를 포함하면 잔재로 다시 잡혀야 한다(검증 메커니즘 자체 검증).
        _, summary = humanize_html.humanize_html(
            _FIXTURE_HTML, [{"before": "흐름", "after": "흐름새"}]
        )
        self.assertGreaterEqual(summary["residuals"]["흐름"], 1)

    def test_longest_before_first_ordering(self) -> None:
        # 입력 순서가 짧은 규칙 먼저여도 긴 before가 우선 적용된다.
        rules = [
            {"before": "더는", "after": "XX"},
            {"before": "더는 혼자가 아닙니다", "after": "이제는 혼자가 아닙니다"},
        ]
        result, _ = humanize_html.humanize_html(_FIXTURE_HTML, rules)
        self.assertIn("이제는 혼자가 아닙니다", result)
        self.assertNotIn("XX 혼자가 아닙니다", result)

    def test_regex_rule(self) -> None:
        result, summary = humanize_html.humanize_html(
            _FIXTURE_HTML, [{"before": r"굴러가[는고]", "after": "작동하는", "regex": True}]
        )
        self.assertIn("<title>말 한마디에 작동하는 자동화</title>", result)
        self.assertGreater(summary["replacements_applied"], 0)
        # regex 규칙도 skip 태그는 불가침.
        self.assertIn('console.log("굴러가는 자동화");', result)


class HumanizeHtmlCliTests(unittest.TestCase):
    """CLI(_main) — --check-only와 전체 실행."""

    def _run_main(self, argv: list[str]) -> tuple[int, str]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = humanize_html._main(argv)
        return code, buffer.getvalue()

    def test_check_only_reports_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "page.html")
            rules_path = os.path.join(tmp, "map.json")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write(_FIXTURE_HTML)
            with open(rules_path, "w", encoding="utf-8") as handle:
                json.dump(_RULES, handle, ensure_ascii=False)
            code, stdout = self._run_main(
                ["--input", src, "--replacements", rules_path, "--check-only"]
            )
            self.assertEqual(code, 0)
            report = json.loads(stdout)
            self.assertTrue(report["check_only"])
            # title·og:title·<strong>·JSON-LD name 4곳 — skip 태그 디코이 제외.
            self.assertEqual(report["patterns_present"]["굴러가는 자동화"], 4)
            self.assertGreater(report["total_hits"], 0)
            # --check-only는 어떤 파일도 쓰지 않는다.
            self.assertEqual(
                sorted(os.listdir(tmp)), sorted(["map.json", "page.html"])
            )

    def test_cli_full_run_writes_output_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "page.html")
            rules_path = os.path.join(tmp, "map.json")
            dst = os.path.join(tmp, "out.html")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write(_FIXTURE_HTML)
            with open(rules_path, "w", encoding="utf-8") as handle:
                json.dump(_RULES, handle, ensure_ascii=False)
            code, stdout = self._run_main(
                ["--input", src, "--replacements", rules_path, "--output", dst]
            )
            self.assertEqual(code, 0)
            summary = json.loads(stdout)
            self.assertTrue(summary["tag_balance_ok"])
            self.assertEqual(summary["replacements_applied"], 10)
            with open(dst, "r", encoding="utf-8") as handle:
                out = handle.read()
            self.assertIn("작동하는 AI 코워커", out)
            self.assertIn('console.log("굴러가는 자동화");', out)


if __name__ == "__main__":
    unittest.main()
