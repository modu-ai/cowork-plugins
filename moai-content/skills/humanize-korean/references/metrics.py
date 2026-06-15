"""humanize-korean 정량 메트릭 계산기 (v1.6 호환).

이 스킬이 한국어 텍스트의 "AI 티" 정량 신호를 한 번의 호출로 산출하기 위해
쓰는 측정 모듈이다. 외부 형태소 분석기 없이 정규식과 한자어 접미사 사전으로
형태소 분석을 근사한다. 산출된 수치는 윤문 단계가 텍스트의 위험도를 빠르게
가늠하는 수치 기준으로 쓰인다 — 최종 판정은 윤문 단계의 몫이다.

설계 원칙:
- 표준 라이브러리만 사용한다(json/re/math/os/sys/argparse/collections).
  konlpy/bareun/mecab/spaCy/numpy/pandas 등 외부 패키지는 도입하지 않는다.
- 문장 분리와 어절 토큰화는 한 번만 수행해 `_Document` 모델에 담아 두고
  각 지표 함수가 이를 재사용한다.

언어 개념 출처(직접 인용):
- 쉼표 포함률·쉼표 사용량·연결어미+쉼표·쉼표 구간 길이 등 쉼표 계열 지표는
  KatFish(Park et al.) 한국어 인간/LLM 대조 코퍼스의 측정 항목을 그대로
  쓴다. 한자어 명사화(-성/-적/-화) 밀도, 어휘 다양성(TTR)도 같은 계열이다.

CLI:
    python metrics.py --input run/01_input.txt \
        --genre essay --output run/00_metrics.json
"""

from __future__ import annotations

import argparse
import json
import math  # noqa: F401  (재보정 시 표준편차 계산에 사용 — API 호환 유지)
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Optional

# ---------------------------------------------------------------------------
# 모듈 상수
# ---------------------------------------------------------------------------

VERSION = "v1.6"

# 연결어미 음절 집합. 어절 끝에서 다음 연결로 이어주는 어미들이다.
# 정규식에서 교대 패턴 대신 음절열 목록을 join 해 표현한다.
_CONNECTIVE_SYLLABLES = ("고", "며", "지만", "면서", "아서", "어서")
_CONNECTIVE_ALT = "|".join(_CONNECTIVE_SYLLABLES)

# 연결어미 직후에 쉼표가 따라오는 위치(어미 + 선택적 공백 + 쉼표).
_CONNECTIVE_COMMA = re.compile(rf"(?:{_CONNECTIVE_ALT})[ \t]*,")

# 연결어미가 어절 경계(공백·문장부호·문자열 끝)에서 끝나는 위치. 분모 산정용.
_CONNECTIVE_AT_BOUNDARY = re.compile(rf"(?:{_CONNECTIVE_ALT})(?=[\s,.!?、。]|$)")

# 어절 분할 — 연속 공백(스페이스/탭/개행)으로 자른다.
_WHITESPACE_RUN = re.compile(r"[ \t\r\n\f\v]+")

# 문장 종결 부호 뒤를 문장 경계로 본다. 한국어는 세미콜론을 거의 안 쓰므로 제외.
_SENTENCE_TERMINATOR = re.compile(r"(?<=[.!?。])\s+")

# 어절 양끝의 문장부호를 떼어내는 패턴(길이/접미사 판정 정확도용).
# 하이픈은 문자 클래스 끝에 두어 리터럴로 처리한다(이스케이프 불필요).
_EDGE_PUNCT = re.compile(r"[.,!?;:()\[\]{}\"'`~、。“”‘’-]+")

# 한자어 명사화 접미사 — 어절 마지막 글자가 이 중 하나면 후보로 본다.
_SINO_NOMINALIZER = frozenset(("성", "적", "화"))

# 한자어 접미사 오탐 차단 목록(-성/-적/-화로 끝나는 듯하나 명사화가 아닌 어절).
_SINO_FALSE_POSITIVES = frozenset({"있는화", "되는화", "맞아", "와서"})

# 기본 어휘 사전 — baseline 파일이 제공하지 않을 때의 폴백.
_DEFAULT_CONCLUSION_PIVOTS = ["결론적으로", "따라서", "이를 통해", "그러므로"]
_DEFAULT_SAFE_HEDGES = ["양쪽 모두", "두 가지 모두", "장점도 있지만", "신중하게", "균형"]


# ---------------------------------------------------------------------------
# 텍스트 모델 — 문장/어절 분할을 한 번만 계산해 재사용한다
# ---------------------------------------------------------------------------


@dataclass
class _Document:
    """원문 한 편의 분할 결과를 담는 경량 컨테이너."""

    raw: str
    sentences: list[str]


def _split_into_sentences(text: str) -> list[str]:
    """종결 부호 + 개행을 모두 문장 경계로 보고 평탄화한다."""
    stripped = text.strip()
    if not stripped:
        return []
    collected: list[str] = []
    for chunk in _SENTENCE_TERMINATOR.split(stripped):
        for line in chunk.split("\n"):
            line = line.strip()
            if line:
                collected.append(line)
    return collected


def _word_units(fragment: str) -> list[str]:
    """공백 기준 어절 리스트."""
    return [w for w in _WHITESPACE_RUN.split(fragment.strip()) if w]


def _bare_word(word: str) -> str:
    """어절 양끝 문장부호를 제거한 표층형."""
    return _EDGE_PUNCT.sub("", word)


def _model(text: str) -> _Document:
    return _Document(raw=text, sentences=_split_into_sentences(text))


# ---------------------------------------------------------------------------
# 8개 지표 함수 — 모두 raw text를 받아 동일 인터페이스를 유지한다
# ---------------------------------------------------------------------------


def comma_inclusion_rate(text: str) -> float:
    """쉼표를 1개 이상 포함한 문장의 비율(0~1)."""
    sentences = _model(text).sentences
    if not sentences:
        return 0.0
    has_comma = [s for s in sentences if "," in s]
    return len(has_comma) / len(sentences)


def comma_usage_rate(text: str) -> float:
    """문장당 평균 쉼표 개수."""
    sentences = _model(text).sentences
    if not sentences:
        return 0.0
    total_commas = sum(s.count(",") for s in sentences)
    return total_commas / len(sentences)


def ending_comma_rate(text: str) -> float:
    """연결어미 위치 중 직후에 쉼표가 붙은 비율.

    분모는 어절 경계에서 끝나는 연결어미 전체 개수,
    분자는 그중 쉼표가 따라오는 개수. 분모가 0이면 0.0.
    """
    if not text.strip():
        return 0.0
    boundary_hits = _CONNECTIVE_AT_BOUNDARY.findall(text)
    if not boundary_hits:
        return 0.0
    comma_hits = _CONNECTIVE_COMMA.findall(text)
    return len(comma_hits) / len(boundary_hits)


def comma_segment_length(text: str) -> float:
    """쉼표로 나뉜 구간들의 평균 어절 수.

    쉼표 없는 문장은 문장 전체를 한 구간으로 본다.
    """
    sentences = _model(text).sentences
    segment_word_counts: list[int] = []
    for sentence in sentences:
        if "," not in sentence:
            segment_word_counts.append(len(_word_units(sentence)))
            continue
        for piece in sentence.split(","):
            piece = piece.strip()
            if piece:
                segment_word_counts.append(len(_word_units(piece)))
    if not segment_word_counts:
        return 0.0
    return sum(segment_word_counts) / len(segment_word_counts)


def conclusion_pivot_count(text: str, lexicon: Optional[list[str]] = None) -> int:
    """결론 전환 어휘의 등장 횟수 합."""
    words = lexicon if lexicon else _DEFAULT_CONCLUSION_PIVOTS
    return sum(text.count(term) for term in words)


def safe_balance_count(text: str, lexicon: Optional[list[str]] = None) -> int:
    """안전 균형형 hedging 어휘의 등장 횟수 합."""
    words = lexicon if lexicon else _DEFAULT_SAFE_HEDGES
    return sum(text.count(term) for term in words)


def hanja_nominalizer_density(text: str) -> float:
    """-성/-적/-화로 끝나는 한자어 명사화 어절의 토큰 밀도(0~1).

    어절은 양끝 문장부호를 떼어낸 표층형으로 본다. 길이가 2자 미만이거나
    오탐 목록에 들면 세지 않는다.
    """
    words = [w for w in (_bare_word(t) for t in _word_units(text)) if w]
    if not words:
        return 0.0
    matched = 0
    for word in words:
        if len(word) < 2:
            continue
        if word in _SINO_FALSE_POSITIVES:
            continue
        if word[-1] in _SINO_NOMINALIZER:
            matched += 1
    return matched / len(words)


def lexical_diversity(text: str) -> float:
    """어절 기준 type-token ratio(고유 어절 수 / 전체 어절 수)."""
    words = [w for w in (_bare_word(t) for t in _word_units(text)) if w]
    if not words:
        return 0.0
    return len(set(words)) / len(words)


# ---------------------------------------------------------------------------
# baseline 로드 + z-score 근사
# ---------------------------------------------------------------------------


def _baseline_beside_module() -> str:
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(module_dir, "baseline.json")


def _read_baseline(path: Optional[str]) -> dict[str, Any]:
    resolved = path or _baseline_beside_module()
    with open(resolved, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _genre_cells(
    baseline: dict[str, Any], genre: str
) -> tuple[dict[str, Any], Optional[str]]:
    """요청 장르의 지표 셀(전역 평균으로 결측 보강)과 폴백 경고를 돌려준다."""
    by_genre = baseline.get("genres", {}) or {}
    requested = by_genre.get(genre)
    warning: Optional[str] = None
    if requested is None:
        warning = f"baseline_genre_null:{genre}->essay"
        requested = by_genre.get("essay") or {}
    global_avg = baseline.get("global_average", {}) or {}
    merged: dict[str, Any] = {}
    for key in set(requested.keys()) | set(global_avg.keys()):
        cell = requested.get(key) or global_avg.get(key)
        if cell:
            merged[key] = cell
    return merged, warning


def _z_against_means(
    value: float, human: Optional[float], ai: Optional[float], *, scale_to_percent: bool
) -> Optional[float]:
    """인간/AI 평균 두 값만으로 z-score를 근사한다.

    공개된 코퍼스는 지표별 평균 2개만 제공하므로, 인간-AI 격차의 절반을
    표준편차 1-sigma 대용으로 삼는다. 양의 z는 AI에 가깝다는 뜻이다.
    `scale_to_percent`가 참이면 측정값(0~1)을 백분율로 환산해 비교한다.
    """
    if human is None or ai is None:
        return None
    measured = value * 100 if scale_to_percent else value
    sigma = abs(ai - human) / 2.0
    if sigma == 0:
        return 0.0
    return (measured - human) / sigma


def _grade_band(
    z_scores: dict[str, Optional[float]], lexicon_counts: dict[str, int]
) -> tuple[str, int]:
    """z-score와 어휘 카운트를 합산해 위험 등급(low/medium/high)을 정한다."""
    points = 0
    for key in ("comma_inclusion_rate", "ending_comma_rate", "comma_segment_length"):
        z = z_scores.get(key)
        if z is not None and z > 1.0:
            points += 2
    diversity_z = z_scores.get("lexical_diversity")
    if diversity_z is not None and diversity_z < -1.0:
        points += 1
    if lexicon_counts.get("conclusion_pivot_count", 0) >= 2:
        points += 1
    if lexicon_counts.get("safe_balance_count", 0) >= 2:
        points += 1
    hanja_z = z_scores.get("hanja_nominalizer_density")
    if hanja_z is not None and hanja_z > 1.0:
        points += 1
    if points >= 6:
        return "high", points
    if points >= 4:
        return "medium", points
    return "low", points


def _matched_terms(text: str, lexicon: list[str]) -> list[str]:
    return [term for term in lexicon if term in text]


# ---------------------------------------------------------------------------
# 공개 진입점
# ---------------------------------------------------------------------------


def compute_all(
    text: str,
    genre: str = "essay",
    baseline_path: Optional[str] = None,
) -> dict[str, Any]:
    """한 편의 문서에 대해 8개 지표 + z-score + 위험 등급을 산출한다."""
    baseline = _read_baseline(baseline_path)
    cells, fallback_warning = _genre_cells(baseline, genre)
    lexicons = baseline.get("lexicons", {}) or {}
    pivot_lexicon = lexicons.get("conclusion_pivot") or list(_DEFAULT_CONCLUSION_PIVOTS)
    hedge_lexicon = lexicons.get("safe_balance") or list(_DEFAULT_SAFE_HEDGES)

    metrics: dict[str, Any] = {
        "comma_inclusion_rate": comma_inclusion_rate(text),
        "comma_usage_rate": comma_usage_rate(text),
        "ending_comma_rate": ending_comma_rate(text),
        "comma_segment_length": comma_segment_length(text),
        "conclusion_pivot_count": conclusion_pivot_count(text, pivot_lexicon),
        "safe_balance_count": safe_balance_count(text, hedge_lexicon),
        "hanja_nominalizer_density": hanja_nominalizer_density(text),
        "lexical_diversity": lexical_diversity(text),
    }

    # 쉼표 포함률·연결어미 쉼표율은 baseline 셀이 백분율 단위이므로 환산해 비교.
    z_scores: dict[str, Optional[float]] = {}
    percent_flags = {
        "comma_inclusion_rate": True,
        "comma_usage_rate": False,
        "ending_comma_rate": True,
        "comma_segment_length": False,
    }
    for key, as_percent in percent_flags.items():
        cell = cells.get(key)
        if cell:
            z_scores[key] = _z_against_means(
                metrics[key], cell.get("human"), cell.get("ai"), scale_to_percent=as_percent
            )
        else:
            z_scores[key] = None

    # 한자어 명사화 밀도: 코퍼스가 문서당 12회를 S2 강신호로 본다는 점에 착안해
    # 밀도 0.06(인간)·0.12(AI)를 근사 기준으로 삼아 백분율 환산값을 비교한다.
    z_scores["hanja_nominalizer_density"] = _z_against_means(
        metrics["hanja_nominalizer_density"] * 100, 6.0, 12.0, scale_to_percent=False
    )
    # 어휘 다양성도 전용 셀이 없으므로 한국어 에세이 통상치 0.65(인간)·0.55(AI)를
    # 임시 기준으로 둔다(AI가 토큰을 약간 더 반복하는 경향).
    z_scores["lexical_diversity"] = _z_against_means(
        metrics["lexical_diversity"], 0.65, 0.55, scale_to_percent=False
    )

    lexicon_counts = {
        "conclusion_pivot_count": int(metrics["conclusion_pivot_count"]),
        "safe_balance_count": int(metrics["safe_balance_count"]),
    }
    risk_band, risk_score = _grade_band(z_scores, lexicon_counts)

    report: dict[str, Any] = {
        "version": VERSION,
        "genre": genre,
        "char_count": len(text),
        "metrics": metrics,
        "z_scores": z_scores,
        "risk_band": risk_band,
        "risk_score": risk_score,
        "evidence": {
            "conclusion_pivots": _matched_terms(text, pivot_lexicon),
            "safe_balances": _matched_terms(text, hedge_lexicon),
        },
    }
    if fallback_warning:
        report["warning"] = fallback_warning
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="humanize-korean v1.6 메트릭 러너")
    parser.add_argument("--input", required=True, help="입력 텍스트 파일 경로")
    parser.add_argument("--genre", default="essay", help="essay/poetry/abstract/...")
    parser.add_argument("--output", default=None, help="출력 JSON 경로(선택)")
    parser.add_argument("--baseline", default=None, help="baseline JSON 경로 재정의")
    args = parser.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as handle:
        text = handle.read()

    report = compute_all(text, genre=args.genre, baseline_path=args.baseline)

    if args.output:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)

    print(report["risk_band"])
    return 0


if __name__ == "__main__":
    sys.exit(_main())
