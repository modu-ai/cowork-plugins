"""humanize-korean 정량 메트릭 계산기 (v2.0 — post-editese 확장).

v1.6 metrics.py의 8개 쉼표·명사화 지표 위에, 번역투/포스트-에디팅 문헌의
3축(simplification·normalisation·interference)과 T1~T8 직역체 신호 14종을
얹는다. v2.0 출력은 v1.6 출력의 상위집합이다.

설계 원칙:
- 표준 라이브러리만 사용한다(json/re/os/sys/argparse/statistics).
  konlpy/bareun/mecab/spaCy/numpy/pandas 등 외부 패키지는 도입하지 않는다.
- v1.6 8개 함수는 metrics.py에서 그대로 재노출한다(시그니처·반환 보존, 회귀 안전).
  여기서 재정의하지 않는다.
- v2.0이 추가하는 14개 함수는 한자어 접미사 사전(-성/-적/-화/-도/-력/-감/-원),
  평서형 종결(-한다/-된다/-이다), 진행형(-고 있다), 이중 조사(-에서의 등) 등을
  정규식 + 사전으로 근사한다.

언어 개념 출처(직접 인용):
- 3축 정의: Toral 2019 (arXiv:1907.00900) simplification/normalisation/interference,
  Baker 1993 normalisation, Toury 1995 law of interference.
- T1~T8 한국어 직역체 유형: 한국 번역학계의 번역투 분류(무정물 주어, 이중 피동,
  인칭 대명사 과다, 무정물 복수 -들, 좌향 관형절 중첩, light verb 직역,
  이중 조사, 진행형 1대1 매핑).

CLI:
    python metrics_v2.py --input run/01_input.txt \
        --genre essay --output run/00_metrics_v2.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from statistics import StatisticsError, fmean
from typing import Any, Optional

# ---------------------------------------------------------------------------
# v1.6 메트릭 모듈 임포트 (회귀 안전 — 시그니처 그대로 재노출)
# ---------------------------------------------------------------------------

# metrics_v2.py는 metrics.py와 같은 디렉터리(이 스킬의 references/)에 있다.
# 모듈 디렉터리를 sys.path 앞에 넣고 이름으로 임포트한다.
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
if _MODULE_DIR not in sys.path:
    sys.path.insert(0, _MODULE_DIR)

import metrics as _base  # noqa: E402  (sys.path 조작 의도적)

# v1.6 8개 지표 콜러블을 그대로 재노출. 시그니처·반환 형태가 동일하다.
comma_inclusion_rate = _base.comma_inclusion_rate
comma_usage_rate = _base.comma_usage_rate
ending_comma_rate = _base.ending_comma_rate
comma_segment_length = _base.comma_segment_length
conclusion_pivot_count = _base.conclusion_pivot_count
safe_balance_count = _base.safe_balance_count
hanja_nominalizer_density = _base.hanja_nominalizer_density
lexical_diversity = _base.lexical_diversity

# v1.6 분할 헬퍼 재사용 (내부 함수 — 읽기 전용으로만 쓴다).
_segment_sentences = _base._split_into_sentences
_split_words = _base._word_units
_clean_word = _base._bare_word

VERSION = "v2.0"

# ---------------------------------------------------------------------------
# v2.0 상수 — 접미사 / 어휘 사전
# ---------------------------------------------------------------------------

# 한자어 명사화 접미사 v2.0 — v1.6 3종 + 4종 보강. 어절 마지막 1글자 매칭.
_SINO_SUFFIX_V2 = ("성", "적", "화", "도", "력", "감", "원")

# 평서형 종결 어미 — normalisation 축. 문장 끝 어절의 어미를 본다.
_DECLARATIVE_TAIL = ("한다", "된다", "이다")

# 진행형 '~고 있다' 표층 매칭(종결/연결/관형형 폭넓게 캡처).
_PROGRESSIVE = re.compile(r"고\s*있(?:다|었|는|을|던|는다)")

# 이중 피동 표층 어휘. 단순 '되다'는 정상 표현이므로 제외하고, '되어진/여진/
# 혀진/려진' 류 중첩 피동만 등재한다.
_DOUBLE_PASSIVE_FORMS = (
    "되어진다",
    "되어졌다",
    "되어진",
    "되어지는",
    "여지다",
    "여진다",
    "여졌다",
    "여진",
    "잊혀진",
    "잊혀졌",
    "잊혀진다",
    "보여진다",
    "보여졌다",
    "보여진",
    "쓰여진다",
    "쓰여졌다",
    "쓰여진",
    "닫혀진",
    "열려진",
    "불려진",
    "놓여진",
)

# T2a '~에 의해 + 피동'. 피동 동사가 직후 12글자 안에 와야 매칭한다.
# 단순 '에 의해'는 자연 한국어이므로 제외. 한자어 피동은 '되-' 축약형
# (생성된·구성되는·제작되었다)이 가장 흔하고, '-아/어/여지다'(만들어진·끊어진)
# 계열도 행위자 피동에 포함한다. 비축약 '되다'·'받다'·'당하다'도 함께 본다.
_AGENT_PASSIVE = re.compile(
    r"에\s*의(?:해|하여)\s+\S{0,12}?"
    r"(?:"
    r"된다|된|될|되는|되어|되었|되며|되고|되다"
    r"|받는|받은|받을|받았|받아|받다"
    r"|당하|당한|당했|당할|당해"
    r"|[아어여]진|[아어여]졌|[아어여]지"
    r")"
)

# T3 인칭 대명사. 영어 he/she/it/they 1대1 매핑.
# '그' 단독은 지시사로도 흔하므로, 인칭 조사가 붙은 경우만 인칭으로 본다.
# 그녀/그들/그것은 거의 항상 인칭이므로 단독 매칭한다.
_PRONOUN = re.compile(
    r"(?:그녀(?:는|가|를|의|에게|와|도|만)?"
    r"|그것(?:은|이|을|의|에|에게)?"
    r"|그들(?:은|이|을|의|에게|과|도)?"
    r"|그(?:는|가|를|의|에게|와|도|만)(?=\s|[.,!?]|$))"
)

# T4 무정물·추상명사 + -들. 토큰 단위 매칭.
_INANIMATE_PLURAL = (
    "데이터들",
    "정보들",
    "결과들",
    "연구들",
    "아이디어들",
    "방법들",
    "문제들",
    "의견들",
    "시스템들",
    "기술들",
    "사실들",
    "사례들",
    "이론들",
    "개념들",
    "현상들",
    "특징들",
    "요소들",
    "원인들",
    "영향들",
    "변화들",
    "기능들",
    "조건들",
    "기준들",
    "관점들",
    "원리들",
)

# T6 light verb 직역 — have/make 류.
_LIGHT_VERB_LITERAL = (
    "가지고 있다",
    "가지고있다",
    "가지고 있는",
    "가지고있는",
    "가지고 있었",
    "가지고있었",
    "가지고 있으",
    "가지고있으",
    "갖고 있다",
    "갖고있다",
    "갖고 있는",
    "갖고있는",
    "을 가지다",
    "를 가지다",
    "을 가졌",
    "를 가졌",
    "을 가진다",
    "를 가진다",
    "을 만들다",
    "를 만들다",
    "을 만들었",
    "를 만들었",
    "을 만들어 낸",
    "를 만들어 낸",
    "을 만들어낸",
    "를 만들어낸",
    "회의를 가지",
    "회의를 가졌",
    "한번 봄을 가지",
    "결정을 내리",
    "결정을 내렸",
)

# T7 이중 조사. 단일 '~의'는 절대 매칭하지 않도록 6종만 등재한다.
_DOUBLE_PARTICLE = re.compile(r"(?:에서의|에로의|으로의|에의|으로부터의|로부터의)")

# 단락 분리 — 빈 줄 1개 이상.
_PARAGRAPH_BREAK = re.compile(r"\n\s*\n")

# 종결어미 표층 키 — 문장 끝 마지막 2음절(없으면 1음절)을 다양성 키로 쓴다.
_TAIL_TWO = re.compile(r"([가-힣]{2})[.!?]\s*$")
_TAIL_ONE = re.compile(r"([가-힣])[.!?]\s*$")

# 주제/주격/목적격 조사 음절 — 관형사형 어미와 동형이나 관형형이 아니므로
# relative_clause_nesting 판정에서 명시 제외한다(F1 오탐 차단).
_TOPIC_PARTICLE_TAIL = ("은", "는", "을", "를")


# ---------------------------------------------------------------------------
# v2.0 전용 헬퍼 (v1.6 헬퍼와 이름 충돌 없음)
# ---------------------------------------------------------------------------


def _segment_paragraphs(text: str) -> list[str]:
    stripped = text.strip()
    if not stripped:
        return []
    return [p.strip() for p in _PARAGRAPH_BREAK.split(stripped) if p.strip()]


def _final_word(sentence: str) -> str:
    words = _split_words(sentence)
    if not words:
        return ""
    return _clean_word(words[-1])


def _clean_words(text: str) -> list[str]:
    return [w for w in (_clean_word(t) for t in _split_words(text)) if w]


# ---------------------------------------------------------------------------
# Group A: simplification 축
# ---------------------------------------------------------------------------


def lexical_diversity_ttr(text: str) -> float:
    """어절 TTR — simplification 축. v1.6 lexical_diversity와 동일 계산."""
    return lexical_diversity(text)


def lexical_density(text: str) -> float:
    """내용어 비율 근사 — simplification 축.

    어절 마지막 글자가 v2.0 한자어 접미사(-성·-적·-화·-도·-력·-감·-원)이거나,
    동사/형용사 평서 종결(-한다·-된다·-이다·-했다·-였다·-었다·-답다·-스럽다·
    -롭다·-하다·-되다)로 끝나면 내용어로 센다. 기능어(조사·접속부사)는
    길이<2 가드와 작은 불용어 목록으로 거른다. 반환은 [0, 1].
    """
    words = _clean_words(text)
    if not words:
        return 0.0
    stopwords = {
        "그리고", "그러나", "하지만", "또한", "또는", "혹은", "즉", "예를", "예컨대",
        "이는", "이것은", "그것은", "그러므로", "따라서",
    }
    content_suffix = ("성", "적", "화", "도", "력", "감", "원")
    content_tail = (
        "한다", "된다", "이다", "했다", "였다", "었다",
        "답다", "스럽다", "롭다", "하다", "되다",
    )
    matched = 0
    for word in words:
        if len(word) < 2 or word in stopwords:
            continue
        if word[-1] in content_suffix:
            matched += 1
            continue
        if any(word.endswith(tail) for tail in content_tail):
            matched += 1
    return matched / len(words)


def ending_diversity(text: str) -> float:
    """종결어미 다양성 — 고유 종결 키 / 전체 종결 키 수.

    문장 끝 종결 부호 직전의 1~2음절을 종결 키로 본다. 값이 높을수록
    종결이 다양(인간형). 유효한 종결이 없으면 0.0.
    """
    keys: list[str] = []
    for sentence in _segment_sentences(text):
        m_two = _TAIL_TWO.search(sentence)
        if m_two:
            keys.append(m_two.group(1))
            continue
        m_one = _TAIL_ONE.search(sentence)
        if m_one:
            keys.append(m_one.group(1))
    if not keys:
        return 0.0
    return len(set(keys)) / len(keys)


# ---------------------------------------------------------------------------
# Group B: normalisation 축
# ---------------------------------------------------------------------------


def normalisation_score(text: str) -> float:
    """평서형(-한다/-된다/-이다) 집중도 — normalisation 축.

    문장 끝 어절이 세 평서 종결 중 하나로 끝나는 문장 비율. 높을수록(>0.7)
    정규화된 AI 문체, 매우 낮으면(<0.3) 비격식체나 혼합 문체일 때가 많다. [0,1].
    """
    sentences = _segment_sentences(text)
    if not sentences:
        return 0.0
    matched = 0
    for sentence in sentences:
        tail = _final_word(sentence)
        if tail and any(tail.endswith(end) for end in _DECLARATIVE_TAIL):
            matched += 1
    return matched / len(sentences)


def da_streak_rate(text: str) -> int:
    """길이 4 이상의 '-다' 연속 구간 개수 — T8a normalisation 신호.

    문장 끝 어절이 '다'로 끝나는 문장이 연달아 4개 이상 이어지면 한 구간으로
    센다. 반환은 구간 개수(누적 길이가 아니다). 균일한 '-다' 한 줄기는 1,
    종결이 다양하면 0.
    """
    streaks = 0
    run = 0
    for sentence in _segment_sentences(text):
        if _final_word(sentence).endswith("다"):
            run += 1
        else:
            if run >= 4:
                streaks += 1
            run = 0
    if run >= 4:
        streaks += 1
    return streaks


# ---------------------------------------------------------------------------
# Group C: interference 축 — T1~T8 신호
# ---------------------------------------------------------------------------


def inanimate_subject_rate(text: str) -> float:
    """T1: 무정물 주어 + 보편 동사 패턴 비율.

    근사: 문장 첫 어절(주어 추정)이 v2.0 한자어 접미사로 끝나거나 무정물·추상
    명사 목록에 들고, 뒤 어절 중 보편 인지/서술 동사(보여준다·시사한다·만든다·
    드러낸다·제시한다·나타낸다·증명한다·말해준다·의미한다·가져온다)가 있으면
    센다. 반환 = 해당 문장 수 / 전체 문장 수, [0, 1].
    """
    sentences = _segment_sentences(text)
    if not sentences:
        return 0.0
    inanimate_heads = (
        "연구", "데이터", "분석", "결과", "시스템", "기술", "사례",
        "현상", "이론", "정책", "보고서", "AI", "인공지능", "모델",
        "알고리즘", "변화", "위기", "혁신", "사회", "경제",
    )
    cognitive_verbs = (
        "보여준다", "보여줬다", "보여주는", "시사한다", "시사하는",
        "만든다", "만들어", "드러낸다", "드러냈다", "드러내는",
        "제시한다", "제시했다", "나타낸다", "나타냈다", "나타내는",
        "증명한다", "증명했다", "말해준다", "말해주는",
        "의미한다", "의미하는", "가져온다", "가져왔다", "가져오는",
    )
    matched = 0
    for sentence in sentences:
        words = _clean_words(sentence)
        if not words:
            continue
        head = words[0]
        stem = head
        for josa in ("은", "는", "이", "가", "도"):
            if head.endswith(josa) and len(head) > 1:
                stem = head[:-1]
                break
        head_is_inanimate = stem in inanimate_heads or (
            len(stem) >= 2 and stem[-1] in _SINO_SUFFIX_V2
        )
        if not head_is_inanimate:
            continue
        if any(any(verb in w for verb in cognitive_verbs) for w in words[1:]):
            matched += 1
    return matched / len(sentences)


def by_passive_count(text: str) -> int:
    """T2a: '~에 의해 + 피동 동사' 동시 출현 개수.

    단순 '에 의해'는 제외, 정규식이 잡는 '에 의해 ... 되/받/당하/지'만 센다.
    """
    if not text.strip():
        return 0
    return len(_AGENT_PASSIVE.findall(text))


def double_passive_count(text: str) -> int:
    """T2b: 이중 피동(잊혀지다·보여지다·되어진다·여지다·쓰여지다 …) 개수.

    표층형 사전 매칭. 단순 '되다'는 제외(자연 표현).
    """
    if not text.strip():
        return 0
    return sum(text.count(form) for form in _DOUBLE_PASSIVE_FORMS)


def pronoun_density(text: str) -> float:
    """T3: 단락별 인칭 대명사 밀도 평균.

    그/그녀/그것/그들(+조사 결합형)을 센다. 단독 '그'는 인칭 조사가 붙은
    경우만 센다(지시사 제거). 반환 = 단락별 (인칭 토큰 / 단락 어절) 평균. [0, 1].
    """
    paragraphs = _segment_paragraphs(text)
    if not paragraphs:
        return 0.0
    ratios: list[float] = []
    for paragraph in paragraphs:
        words = _clean_words(paragraph)
        if not words:
            continue
        hits = len(_PRONOUN.findall(paragraph))
        ratios.append(hits / len(words))
    if not ratios:
        return 0.0
    try:
        return fmean(ratios)
    except StatisticsError:
        return 0.0


def deul_overuse_rate(text: str) -> float:
    """T4: 무정물/추상명사 + '-들' 과용 비율.

    분자 = 무정물 복수 목록(데이터들·정보들·결과들 …)에 드는 토큰 수,
    조사가 한두 글자 붙은 형태도 함께 센다. 반환 = 분자 / 전체 어절. [0, 1].
    """
    words = _clean_words(text)
    if not words:
        return 0.0
    matched = 0
    for word in words:
        if word in _INANIMATE_PLURAL:
            matched += 1
            continue
        for base in _INANIMATE_PLURAL:
            if word.startswith(base) and len(word) - len(base) in (1, 2):
                tail = word[len(base):]
                if all("가" <= ch <= "힣" for ch in tail):
                    matched += 1
                    break
    return matched / len(words)


def _is_adnominal(word: str) -> bool:
    """어절이 관형사형 어미(종성 ㄴ/ㄹ)로 끝나는지 근사 판정한다.

    한국어 관형사형은 종성이 ㄴ/ㄹ 인 경우가 압도적이다(-ㄴ/-은/-던/-한/-된,
    -ㄹ/-을/-할/-될). 동형이의인 주제/주격/목적격 조사(은·는·을·를)는 관형형이
    아니므로 명시 제외한다. 형태소 분석기 없이 종성 분해로 근사하며, 동형인
    '은'(읽은 vs 책은)은 보수적으로 조사 쪽으로 분류해 오탐을 줄인다(precision 우선).
    """
    if len(word) < 2:
        return False
    last = word[-1]
    if last in _TOPIC_PARTICLE_TAIL:
        return False
    if not ("가" <= last <= "힣"):
        return False
    jongseong = (ord(last) - 0xAC00) % 28
    return jongseong in (4, 8)  # 종성 ㄴ(4) 또는 ㄹ(8) → 관형사형 어미 추정


def relative_clause_nesting(text: str) -> int:
    """T5: 좌향 관형절 중첩 깊이 3 이상인 문장의 개수.

    근사: 문장 안에서 관형사형 어미(종성 ㄴ/ㄹ)로 끝나고 바로 뒤에 한글 명사
    핵이 오는 어절을 센다. 주제/주격/목적격 조사(은·는·을·를)는 제외하므로
    주제어가 여럿인 문장이 관계절 중첩으로 오탐되지 않는다. 반환은 깊이 3 이상인
    문장 수(총 중첩 수가 아니다).
    """
    sentences = _segment_sentences(text)
    if not sentences:
        return 0
    matched_sentences = 0
    for sentence in sentences:
        words = [w for w in (_clean_word(e) for e in _split_words(sentence)) if w]
        depth = 0
        for i in range(len(words) - 1):  # 마지막 어절은 핵 명사 자리가 없음
            if not _is_adnominal(words[i]):
                continue
            head = words[i + 1]
            if head and "가" <= head[0] <= "힣":
                depth += 1
        if depth >= 3:
            matched_sentences += 1
    return matched_sentences


def have_make_literal_count(text: str) -> int:
    """T6: have/make light verb 직역 구문 개수.

    가지고 있다·갖고 있다·~을 가지다·~을 만들다·회의를 가지다·결정을 내리다 …
    """
    if not text.strip():
        return 0
    return sum(text.count(form) for form in _LIGHT_VERB_LITERAL)


def double_particle_count(text: str) -> int:
    """T7: 이중 조사(에서의·에로의·으로의·에의·으로부터의·로부터의) 개수.

    단일 '~의'는 정규식 구성상 절대 매칭되지 않는다(caveat #5 강제).
    """
    if not text.strip():
        return 0
    return len(_DOUBLE_PARTICLE.findall(text))


def progressive_aspect_rate(text: str) -> float:
    """T8b: 진행형 '~고 있다' 문장당 비율.

    반환 = 진행형 매칭 수 / 전체 문장 수. 표층형 매칭이라 모든 '~고 있다'가
    축약 가능한 것은 아니나, 비율이 높으면(>0.5) 1대1 매핑을 시사한다.
    """
    sentences = _segment_sentences(text)
    if not sentences:
        return 0.0
    hits = sum(len(_PROGRESSIVE.findall(s)) for s in sentences)
    return hits / len(sentences)


# ---------------------------------------------------------------------------
# === v2.0 INTERFERENCE INDEX ===
# T1~T8 가중 합성 신호.
# ---------------------------------------------------------------------------

# 각 신호의 [0,1] 환산 가중치. 합성은 z-score가 아니라 서술적 지표이며,
# baseline 보정은 compute_all_v2에서 별도로 수행한다.
_INTERFERENCE_WEIGHTS = {
    "T1_inanimate_subject_rate": 1.0,
    "T2a_by_passive_per_1k": 0.2,
    "T2b_double_passive_per_1k": 0.2,
    "T3_pronoun_density": 4.0,
    "T4_deul_overuse_rate": 4.0,
    "T5_nested_clause_count": 0.05,
    "T6_have_make_per_1k": 0.2,
    "T7_double_particle_per_1k": 0.5,
    "T8b_progressive_rate": 1.0,
}


def interference_index(text: str) -> dict[str, Any]:
    """T1~T8 가중 간섭 신호 — interference 축 합성.

    각 하위 신호 점수와 per-type 기여를 [0,1]로 단순 환산해 더한 weighted_total
    을 함께 돌려준다.
    """
    sentence_count = max(len(_segment_sentences(text)), 1)
    char_count = max(len(text), 1)
    components = {
        "T1_inanimate_subject_rate": inanimate_subject_rate(text),
        "T2a_by_passive_per_1k": by_passive_count(text) / char_count * 1000,
        "T2b_double_passive_per_1k": double_passive_count(text) / char_count * 1000,
        "T3_pronoun_density": pronoun_density(text),
        "T4_deul_overuse_rate": deul_overuse_rate(text),
        "T5_nested_clause_count": relative_clause_nesting(text),
        "T6_have_make_per_1k": have_make_literal_count(text) / char_count * 1000,
        "T7_double_particle_per_1k": double_particle_count(text) / char_count * 1000,
        "T8b_progressive_rate": progressive_aspect_rate(text),
    }
    weighted_total = 0.0
    for name, raw_value in components.items():
        scaled = raw_value * _INTERFERENCE_WEIGHTS[name]
        weighted_total += min(1.0, max(0.0, scaled))
    return {
        "components": components,
        "weighted_total": weighted_total,
        "n_sentences": sentence_count,
        "n_chars": char_count,
    }


# ---------------------------------------------------------------------------
# baseline + z-score (v2.0 확장)
# ---------------------------------------------------------------------------


def _baseline_v2_beside_module() -> str:
    return os.path.join(_MODULE_DIR, "baseline_v2.json")


def _read_baseline_v2(path: Optional[str]) -> dict[str, Any]:
    resolved = path or _baseline_v2_beside_module()
    if not os.path.exists(resolved):
        return {}
    with open(resolved, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _z_from_cell(value: float, cell_mean: float, cell_stdev: float) -> Optional[float]:
    if cell_stdev is None or cell_stdev <= 0:
        return None
    return (value - cell_mean) / cell_stdev


# ---------------------------------------------------------------------------
# 공개 진입점 — v2.0 상위집합
# ---------------------------------------------------------------------------


def compute_all_v2(
    text: str,
    genre: str = "essay",
    baseline_path: Optional[str] = None,
    baseline_v2_path: Optional[str] = None,
) -> dict[str, Any]:
    """v1.6 지표 + v2.0 post-editese + T1~T8 신호를 산출한다.

    v1.6 compute_all 결과에 다음을 더한다:
        - ``v2_metrics``: 신규 14개 지표 값
        - ``v2_interference_index``: T1~T8 합성 신호
        - ``v2_z_scores``: baseline_v2 대비 지표별 z(placeholder면 None)
        - ``v2_baseline_warnings``: baseline 셀이 `_placeholder: true`인 지표 키 목록
    """
    report = _base.compute_all(text, genre=genre, baseline_path=baseline_path)
    v2_metrics: dict[str, Any] = {
        "lexical_diversity_ttr": lexical_diversity_ttr(text),
        "lexical_density": lexical_density(text),
        "ending_diversity": ending_diversity(text),
        "normalisation_score": normalisation_score(text),
        "da_streak_rate": da_streak_rate(text),
        "inanimate_subject_rate": inanimate_subject_rate(text),
        "by_passive_count": by_passive_count(text),
        "double_passive_count": double_passive_count(text),
        "pronoun_density": pronoun_density(text),
        "deul_overuse_rate": deul_overuse_rate(text),
        "relative_clause_nesting": relative_clause_nesting(text),
        "have_make_literal_count": have_make_literal_count(text),
        "double_particle_count": double_particle_count(text),
        "progressive_aspect_rate": progressive_aspect_rate(text),
    }
    interference = interference_index(text)

    baseline_v2 = _read_baseline_v2(baseline_v2_path)
    cells: dict[str, Any] = {}
    if baseline_v2:
        by_genre = baseline_v2.get("genres", {}) or {}
        cells = by_genre.get(genre) or by_genre.get("essay") or {}

    z_scores: dict[str, Optional[float]] = {}
    placeholder_keys: list[str] = []
    for key, value in v2_metrics.items():
        cell = cells.get(key)
        if not cell:
            z_scores[key] = None
            continue
        if cell.get("_placeholder"):
            placeholder_keys.append(key)
        z_scores[key] = _z_from_cell(
            float(value), float(cell.get("mean", 0.0)), float(cell.get("stdev", 0.0))
        )

    report["version"] = VERSION
    report["v2_metrics"] = v2_metrics
    report["v2_interference_index"] = interference
    report["v2_z_scores"] = z_scores
    report["v2_baseline_warnings"] = placeholder_keys
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="humanize-korean v2.0 메트릭 러너")
    parser.add_argument("--input", required=True, help="입력 텍스트 파일 경로")
    parser.add_argument("--genre", default="essay", help="essay/news/blog/qa/dialogue")
    parser.add_argument("--output", default=None, help="출력 JSON 경로(선택)")
    parser.add_argument("--baseline", default=None, help="v1.6 baseline JSON 경로 재정의")
    parser.add_argument(
        "--baseline-v2", default=None, help="v2.0 baseline JSON 경로 재정의"
    )
    args = parser.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as handle:
        text = handle.read()

    report = compute_all_v2(
        text,
        genre=args.genre,
        baseline_path=args.baseline,
        baseline_v2_path=args.baseline_v2,
    )

    if args.output:
        out_dir = os.path.dirname(os.path.abspath(args.output))
        os.makedirs(out_dir, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)

    print(report["risk_band"])
    return 0


# ---------------------------------------------------------------------------
# v1.6 호환 별칭 — v2.0 출력은 v1.6 출력의 상위집합이다.
# ---------------------------------------------------------------------------
compute_all = compute_all_v2


if __name__ == "__main__":
    sys.exit(_main())
