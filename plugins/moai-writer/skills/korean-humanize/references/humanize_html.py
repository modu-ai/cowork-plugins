"""korean-humanize HTML 카피 일괄 윤문기 (humanize_html v1.0).

AI 틱 카피 치환 쌍(before/after)을 HTML 파일에 일괄 적용한다 — 한국어
텍스트 표면만 건드리고 마크업은 바이트 단위로 보존한다. 절차의 출처는
content-copywriting/ai-tell-ko-copy-spec.md §4(작업 절차 5단계 일괄 적용 +
6단계 검증) + §5(주의사항: head 메타 누락 방지·HTML 문법 우선).

치환 대상 표면(§5 "head 메타 누락" 방지를 위해 body 텍스트만이 아니라
메타 표면까지 포함한다):
- 일반 텍스트 노드 (<script>/<style>/<code>/<pre> 내용은 통째로 제외)
- <title> 텍스트 (일반 텍스트 노드 경로로 처리)
- <meta name="description" content="…">
- <meta property="og:description"|"og:title" content="…">
- <script type="application/ld+json"> 내부 JSON의 문자열 값
  (JSON 파싱 → 문자열 값만 치환 → ensure_ascii=False 재직렬화)

설계 — 위치 기반 splice(마크업 바이트 보존):
    html.parser.HTMLParser는 문서를 재구성할 때 속성 따옴표·공백·엔티티를
    정규화해 버리므로 재구성 방식으로는 "비텍스트 바이트 보존"을 보장할 수
    없다. 그래서 파서는 치환 가능한 표면의 위치(span)를 찾는 데만 쓴다 —
    getpos()의 (행, 열)을 절대 오프셋으로 환산해 각 표면의 [start, end)
    구간을 수집한 뒤, 원문 문자열에 구간별 치환 결과를 splice 한다.
    치환 구간 밖의 바이트는 원문 그대로 이어 붙이므로 태그·속성·공백·주석·
    DOCTYPE이 바이트 단위로 보존된다. convert_charrefs=False로 파싱해
    엔티티(&amp; 등)를 독립 토큰으로 두고 절대 건드리지 않는다.

알려진 한계(precision 우선 — 오치환보다 미치환이 낫다):
- 엔티티로 분절된 텍스트 노드("굴러&amp;가는")는 분절 조각 단위로만 매칭
  하므로 엔티티를 가로지르는 before 패턴은 치환되지 않는다(미치환 감수).
- meta content 속성 값 안의 리터럴 'content=' 문자열은 속성 경계 탐지를
  교란할 수 있다(meta 태그에서는 사실상 발생하지 않는 형태).
- JSON-LD는 문자열 값 변경이 있을 때만 재직렬화한다(무변경이면 바이트
  보존). 재직렬화 시 JSON 내부 공백 서식은 표준형(indent=2)으로 바뀐다 —
  태그 시퀀스와 문자열 외 값은 보존된다.

치환 규칙 JSON 형식(ordered list, longest-before-first로 적용):
    [{"before": "굴러가는 자동화", "after": "작동하는 AI 코워커"},
     {"before": "굴러가[는고]", "after": "작동하는", "regex": true}]
    regex 항목이 아니면 순수 리터럴 부분 문자열 치환이다(기본).

검증(§4 6단계 내장):
- 잔재 카운트: 치환 후 문서의 치환 가능 표면에서 before 패턴 재검색
  (skip 태그 내부 디코이는 표면이 아니므로 잔재로 세지 않는다)
- 태그 시퀀스 전후 비교(구조 불변 확인)
- stdout JSON 요약: replacements_applied / residuals / tag_balance_ok /
  changed_nodes

CLI:
    python3 humanize_html.py --input page.html --replacements map.json \
        --output out.html [--check-only]
    --check-only는 쓰기 없이 before 패턴 존재 카운트만 보고한다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Any, Optional

# 내용을 통째로 건너뛰는 태그 — 코드·스타일·서식 보존 블록.
_SKIP_TAGS = frozenset({"script", "style", "code", "pre"})

# meta content 속성 값의 raw 구간을 태그 원문에서 찾는 패턴.
_CONTENT_ATTR = re.compile(
    r"""content\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE
)

# 치환 대상 meta 식별자 — (속성 이름, 소문자 값).
_META_NAME_TARGETS = frozenset({"description"})
_META_PROPERTY_TARGETS = frozenset({"og:description", "og:title"})

_JSONLD_TYPE = "application/ld+json"


def _line_start_offsets(raw: str) -> list[int]:
    """각 행의 시작 절대 오프셋 목록 — getpos() (행, 열) → 오프셋 환산용."""
    offsets = [0]
    for idx, ch in enumerate(raw):
        if ch == "\n":
            offsets.append(idx + 1)
    return offsets


class _SpanCollector(HTMLParser):
    """치환 가능한 표면의 (start, end, kind) 구간만 수집하는 파서.

    kind ∈ {"text", "attr", "jsonld"}. 문서를 재구성하지 않는다 — 치환은
    humanize_html()이 원문 문자열에 위치 기반 splice로 적용한다.
    """

    def __init__(self, raw: str) -> None:
        super().__init__(convert_charrefs=False)
        self._raw = raw
        self._line_offsets = _line_start_offsets(raw)
        self.spans: list[tuple[int, int, str]] = []
        self._skip_depth = 0
        self._in_jsonld = False

    def _abs(self) -> int:
        line, col = self.getpos()
        return self._line_offsets[line - 1] + col

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        tag = tag.lower()
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
            if tag == "script" and self._is_jsonld(attrs):
                self._in_jsonld = True
        if tag == "meta":
            self._collect_meta_span(attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag == "script":
            self._in_jsonld = False

    def handle_data(self, data: str) -> None:
        if not data:
            return
        start = self._abs()
        end = start + len(data)
        if self._raw[start:end] != data:
            return  # 위치 추적 불일치 — 보수적으로 건너뜀(오치환보다 미치환)
        if self._in_jsonld:
            self.spans.append((start, end, "jsonld"))
        elif self._skip_depth == 0:
            self.spans.append((start, end, "text"))

    @staticmethod
    def _is_jsonld(attrs: list[tuple[str, Optional[str]]]) -> bool:
        for key, value in attrs:
            if key.lower() == "type" and (value or "").strip().lower() == _JSONLD_TYPE:
                return True
        return False

    def _collect_meta_span(self, attrs: list[tuple[str, Optional[str]]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        name_hit = attr_map.get("name", "").lower() in _META_NAME_TARGETS
        prop_hit = attr_map.get("property", "").lower() in _META_PROPERTY_TARGETS
        if not (name_hit or prop_hit) or "content" not in attr_map:
            return
        raw_tag = self.get_starttag_text()
        if not raw_tag:
            return
        match = _CONTENT_ATTR.search(raw_tag)
        if not match:
            return
        group = 1 if match.group(1) is not None else 2
        tag_start = self._abs()
        self.spans.append(
            (tag_start + match.start(group), tag_start + match.end(group), "attr")
        )


def _collect_spans(raw: str) -> list[tuple[int, int, str]]:
    """표면 span을 수집·정렬하고 인접한 jsonld 조각을 병합한다."""
    collector = _SpanCollector(raw)
    collector.feed(raw)
    collector.close()
    merged: list[tuple[int, int, str]] = []
    for span in sorted(collector.spans):
        if (
            merged
            and span[2] == "jsonld"
            and merged[-1][2] == "jsonld"
            and merged[-1][1] == span[0]
        ):
            merged[-1] = (merged[-1][0], span[1], "jsonld")
        else:
            merged.append(span)
    return merged


def _sorted_rules(replacements: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """치환 규칙을 검증하고 longest-before-first로 정렬한다.

    Python sort는 안정적이므로 before 길이가 같은 항목은 입력 순서를
    보존한다(ordered list 계약).
    """
    rules: list[dict[str, Any]] = []
    for entry in replacements:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("before"), str)
            or not isinstance(entry.get("after"), str)
        ):
            raise ValueError("각 치환 항목은 {'before': str, 'after': str} 형태여야 합니다")
        if not entry["before"]:
            raise ValueError("'before'는 빈 문자열일 수 없습니다")
        rules.append(entry)
    return sorted(rules, key=lambda rule: len(rule["before"]), reverse=True)


def _apply_rules(segment: str, rules: list[dict[str, Any]]) -> tuple[str, int]:
    """한 표면 조각에 규칙을 순서대로 적용한다. (결과, 치환 횟수) 반환."""
    applied = 0
    for rule in rules:
        if rule.get("regex"):
            segment, count = re.subn(rule["before"], rule["after"], segment)
        else:
            count = segment.count(rule["before"])
            if count:
                segment = segment.replace(rule["before"], rule["after"])
        applied += count
    return segment, applied


def _apply_rules_jsonld(segment: str, rules: list[dict[str, Any]]) -> tuple[str, int]:
    """JSON-LD 조각의 문자열 값에만 규칙을 적용한다.

    파싱 불가 JSON이거나 변경이 없으면 원문 바이트를 그대로 돌려준다.
    변경이 있으면 ensure_ascii=False + indent=2로 재직렬화한다.
    """
    try:
        parsed = json.loads(segment)
    except (json.JSONDecodeError, ValueError):
        return segment, 0
    counter = [0]

    def _walk(node: Any) -> Any:
        if isinstance(node, str):
            replaced, count = _apply_rules(node, rules)
            counter[0] += count
            return replaced
        if isinstance(node, list):
            return [_walk(item) for item in node]
        if isinstance(node, dict):
            return {key: _walk(value) for key, value in node.items()}
        return node

    transformed = _walk(parsed)
    if counter[0] == 0:
        return segment, 0
    return json.dumps(transformed, ensure_ascii=False, indent=2), counter[0]


def _json_strings(node: Any) -> list[str]:
    """JSON 트리의 모든 문자열 값을 평탄화 — 잔재 카운트용."""
    if isinstance(node, str):
        return [node]
    if isinstance(node, list):
        collected: list[str] = []
        for item in node:
            collected.extend(_json_strings(item))
        return collected
    if isinstance(node, dict):
        collected = []
        for value in node.values():
            collected.extend(_json_strings(value))
        return collected
    return []


def _replaceable_surfaces(html_text: str) -> list[str]:
    """문서에서 치환 가능한 표면 문자열 목록을 추출한다(잔재 카운트 분모)."""
    surfaces: list[str] = []
    for start, end, kind in _collect_spans(html_text):
        segment = html_text[start:end]
        if kind == "jsonld":
            try:
                parsed = json.loads(segment)
            except (json.JSONDecodeError, ValueError):
                continue
            surfaces.extend(_json_strings(parsed))
        else:
            surfaces.append(segment)
    return surfaces


def count_patterns(html_text: str, rules: list[dict[str, Any]]) -> dict[str, int]:
    """치환 가능 표면에서 각 before 패턴의 출현 수를 센다.

    skip 태그(<script>/<style>/<code>/<pre>) 내부는 표면이 아니므로 세지
    않는다 — 잔재 0은 "치환했어야 할 곳에 남은 패턴이 없다"는 뜻이다.
    """
    surfaces = _replaceable_surfaces(html_text)
    counts: dict[str, int] = {}
    for rule in rules:
        before = rule["before"]
        if rule.get("regex"):
            pattern = re.compile(before)
            counts[before] = sum(len(pattern.findall(s)) for s in surfaces)
        else:
            counts[before] = sum(s.count(before) for s in surfaces)
    return counts


class _TagSequenceCollector(HTMLParser):
    """태그 시퀀스만 수집 — 전후 구조 불변 검증용."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.events: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        self.events.append(("start", tag))

    def handle_endtag(self, tag: str) -> None:
        self.events.append(("end", tag))


def _tag_sequence(html_text: str) -> list[tuple[str, str]]:
    collector = _TagSequenceCollector()
    collector.feed(html_text)
    collector.close()
    return collector.events


def humanize_html(
    raw: str, replacements: list[dict[str, Any]]
) -> tuple[str, dict[str, Any]]:
    """HTML 원문에 치환 규칙을 적용하고 (결과 문자열, 검증 요약)을 반환한다.

    요약 dict:
    - ``replacements_applied``: 전체 치환 횟수
    - ``residuals``: 치환 후 표면에 남은 before 패턴별 카운트
    - ``tag_balance_ok``: 전후 태그 시퀀스 동일 여부
    - ``changed_nodes``: 내용이 실제로 바뀐 표면(노드) 수
    """
    rules = _sorted_rules(replacements)
    parts: list[str] = []
    cursor = 0
    applied_total = 0
    changed_nodes = 0
    for start, end, kind in _collect_spans(raw):
        parts.append(raw[cursor:start])
        segment = raw[start:end]
        if kind == "jsonld":
            new_segment, count = _apply_rules_jsonld(segment, rules)
        else:
            new_segment, count = _apply_rules(segment, rules)
        applied_total += count
        if new_segment != segment:
            changed_nodes += 1
        parts.append(new_segment)
        cursor = end
    parts.append(raw[cursor:])
    result = "".join(parts)

    summary = {
        "replacements_applied": applied_total,
        "residuals": count_patterns(result, rules),
        "tag_balance_ok": _tag_sequence(raw) == _tag_sequence(result),
        "changed_nodes": changed_nodes,
    }
    return result, summary


def check_patterns(raw: str, replacements: list[dict[str, Any]]) -> dict[str, Any]:
    """--check-only 보고 — 치환 없이 before 패턴 존재 카운트만 계산한다."""
    rules = _sorted_rules(replacements)
    counts = count_patterns(raw, rules)
    return {
        "check_only": True,
        "patterns_present": counts,
        "total_hits": sum(counts.values()),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="korean-humanize HTML 카피 일괄 윤문기"
    )
    parser.add_argument("--input", required=True, help="입력 HTML 파일 경로")
    parser.add_argument(
        "--replacements", required=True, help="치환 쌍 JSON 파일 경로(ordered list)"
    )
    parser.add_argument(
        "--output", default=None, help="출력 HTML 경로(--check-only가 아니면 필수)"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="치환·쓰기 없이 before 패턴 존재 카운트만 보고",
    )
    args = parser.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as handle:
        raw = handle.read()
    with open(args.replacements, "r", encoding="utf-8") as handle:
        replacements = json.load(handle)
    if not isinstance(replacements, list):
        print("replacements JSON은 {before, after} 객체의 배열이어야 합니다", file=sys.stderr)
        return 2

    if args.check_only:
        print(json.dumps(check_patterns(raw, replacements), ensure_ascii=False, indent=2))
        return 0

    if not args.output:
        parser.error("--output은 --check-only가 아닐 때 필수입니다")

    result, summary = humanize_html(raw, replacements)
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(result)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["tag_balance_ok"] else 1


if __name__ == "__main__":
    sys.exit(_main())
