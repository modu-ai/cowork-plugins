"""korean-humanize 정량 메트릭 계산기 (v2.1 — post-editese + copy 확장).

v1.6 metrics.py의 8개 쉼표·명사화 지표 위에, 번역투/포스트-에디팅 문헌의
3축(simplification·normalisation·interference)과 T1~T8 직역체 신호 14종(v2.0),
그리고 카피 장르 번역투 신호 6종 A-20~A-25·I-7(v2.1 Group D)을 얹는다.
v2.1 출력은 v2.0 출력의, v2.0 출력은 v1.6 출력의 상위집합이다.

설계 원칙:
- 표준 라이브러리만 사용한다(json/re/os/sys/argparse/statistics).
  konlpy/bareun/mecab/spaCy/numpy/pandas 등 외부 패키지는 도입하지 않는다.
- v1.6 8개 함수는 metrics.py에서 그대로 재노출한다(시그니처·반환 보존, 회귀 안전).
  여기서 재정의하지 않는다.
- v2.0이 추가하는 14개 함수는 한자어 접미사 사전(-성/-적/-화/-도/-력/-감/-원),
  평서형 종결(-한다/-된다/-이다), 진행형(-고 있다), 이중 조사(-에서의 등) 등을
  정규식 + 사전으로 근사한다.
- v2.1이 추가하는 카피 장르 6개 함수(Group D)는 표층 정규식 + 사전 매칭의
  precision 우선 설계다 — 오탐(false positive)이 미탐보다 나쁘다는 원칙으로
  결정적 문맥 가드를 두고, 알려진 한계를 각 docstring에 기록한다.

언어 개념 출처(직접 인용):
- 3축 정의: Toral 2019 (arXiv:1907.00900) simplification/normalisation/interference,
  Baker 1993 normalisation, Toury 1995 law of interference.
- T1~T8 한국어 직역체 유형: 한국 번역학계의 번역투 분류(무정물 주어, 이중 피동,
  인칭 대명사 과다, 무정물 복수 -들, 좌향 관형절 중첩, light verb 직역,
  이중 조사, 진행형 1대1 매핑).
- A-20~A-25·I-7 카피 장르 신호: ai-tell-taxonomy.md v2.2~v2.5 카피 클러스터
  (한국어 카피 장르 실전 관찰) + content-copywriting/ai-tell-ko-copy-spec.md §1.

CLI:
    python metrics_v2.py --input run/01_input.txt \
        --genre essay --output run/00_metrics_v2.json
"""

from __future__ import annotations

import argparse
import difflib
from collections import Counter
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

VERSION = "v2.1"

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
# Group D: copy-genre 번역투 신호 — A-20~A-25 + I-7 (v2.1)
# ---------------------------------------------------------------------------
# 카피·마케팅·랜딩 장르에서 AI가 반복 생산하는 직역 신호를 표층 정규식 + 사전
# 매칭으로 근사한다. precision 우선 설계 — 오탐(false positive)이 미탐보다
# 나쁘다는 원칙에 따라 각 함수는 결정적 문맥 가드를 두고, 알려진 한계를
# docstring에 기록한다. 패턴 정의와 검출 임계의 출처는 ai-tell-taxonomy.md
# (A-20~A-25, I-7) + content-copywriting/ai-tell-ko-copy-spec.md §1.

# A-20 기계 동사 '굴러가다/굴리다' 활용형 표층 매칭. '굴러간'은 평서 종결
# '굴러간다'(간=가+ㄴ 융합 음절)를 잡기 위해 추가한다.
_ROLL_VERB = re.compile(r"굴러가|굴러간|굴러갑|굴리는|굴린다|굴려")
# A-20 문맥 가드 — 같은 문장에 기계·시스템 명사가 있어야 번역투로 본다
# (물리 맥락 "공이 굴러간다" 오탐 차단).
_COPY_TECH_NOUN = re.compile(
    r"자동화|시스템|워크플로우|봇|프로그램|앱|툴|기능|서비스|AI"
)
# A-20 '무엇으로 굴러가' 의문형(what runs it 직역) — 기계 명사 없이도 결정적.
_ROLL_INTERROGATIVE = re.compile(r"무엇으로\s*굴러가")

# A-21 문장 끝 '(으)로(+조사)' 어절 — 영어 명사종결(into/as one X) 직역.
_RO_ENDING = re.compile(r"^[가-힣]+(?:으로|로)(?:도|만|는)?$")
# A-21 오탐 차단 — '-로'로 끝나지만 명사종결이 아닌 부사·방향어 폐쇄 목록.
_RO_ADVERB_EXCEPTIONS = frozenset({
    "정말로", "실제로", "때때로", "때로는", "대체로", "함부로", "제대로",
    "별도로", "주로", "스스로", "서로", "그대로", "바로", "절대로", "진짜로",
    "새로", "저절로", "참으로", "진실로", "홀로", "억지로", "다음으로",
    "처음으로", "첫째로", "둘째로", "셋째로", "끝으로",
    "앞으로", "뒤로", "위로", "아래로", "안으로", "밖으로", "옆으로",
})
# A-21 '이/가 됩니다' 앞의 추상명사 사전(흐름·구조·결과 계열).
_ABSTRACT_BECOME_NOUNS = frozenset({
    "흐름", "구조", "결과", "상태", "시작", "하나", "현실", "일상", "기준",
    "표준", "중심", "미래", "무기", "자산", "습관", "기회", "힘",
})
# A-21 추상명사 접미사 — '-성/-화/-력'으로 끝나는 명사도 추상으로 본다.
# ('-원'은 회사원·공무원 등 사람 명사 오탐이 커서 의도적으로 제외한다.)
_ABSTRACT_BECOME_SUFFIX = ("성", "화", "력")

# A-22 '나 대신/나와 함께 … 일하-' 직역(works for/with me). 12자 이내 전방 탐색.
_BENEFACTIVE = re.compile(
    r"(?:나\s*대신|나와\s*함께|날\s*대신|저\s*대신).{0,12}?(?:일하|일합|일해)"
)

# I-7 1인칭 공식 주어(당사는/저희는/폐사는 …) + 격식 종결 어미.
_FORMAL_FIRST_PERSON = re.compile(r"당사는|당사가|저희는|저희가|폐사는")
_FORMAL_POLITE_TAILS = ("드리겠습니다", "드립니다", "합니다", "입니다")

# A-25 3인칭 기술 주어 토큰 + 2인칭 호회 토큰.
_THIRD_PERSON_TECH_SUBJECTS = (
    "자동화가", "시스템이", "AI가", "서비스가",
    "기술이", "플랫폼이", "솔루션이", "기능이",
)
_SECOND_PERSON_TOKENS = re.compile(r"여러분|당신|고객님")
_POLITE_DECLARATIVE_TAILS = ("합니다", "입니다")


def mechanical_verb_calque_count(text: str) -> int:
    """A-20: 기계 동사 직역 '굴러가다/굴리다' 개수.

    같은 문장 안에 기계·시스템 명사(자동화·시스템·워크플로우·봇·프로그램·앱·
    툴·기능·서비스·AI)가 있을 때만 '굴러가/굴러간/굴리-' 활용형을 센다 —
    물리 맥락("공이 굴러간다")은 세지 않는다(precision 가드). '무엇으로
    굴러가' 의문형(what runs it 직역)은 기계 명사 없이도 결정적이므로
    별도로 센다.

    알려진 한계: 표층 매칭이라 기계 명사가 이웃 문장에만 있는 경우는
    놓친다(미탐 감수 — precision 우선).
    """
    if not text.strip():
        return 0
    hits = 0
    for sentence in _segment_sentences(text):
        if _COPY_TECH_NOUN.search(sentence):
            hits += len(_ROLL_VERB.findall(sentence))
        else:
            hits += len(_ROLL_INTERROGATIVE.findall(sentence))
    return hits


def abstract_noun_ending_count(text: str) -> int:
    """A-21: 추상명사 종결구 문장 개수(문장당 최대 1회).

    다음 중 하나면 그 문장을 센다:
    - 문장(또는 종결 부호 없는 헤드라인 줄 — 분할기가 줄 단위도 문장으로
      본다)의 마지막 어절이 '(으)로(+도/만/는)'로 끝나고 부사 예외 목록
      (정말로·바로·앞으로 …)에 들지 않는 경우
    - 문장이 '추상명사 + 이/가 됩니다'로 끝나는 경우(추상명사 사전 또는
      -성/-화/-력 접미사)

    알려진 한계: 부사 예외는 폐쇄 목록이라 목록 밖의 '-로' 부사는 오탐
    가능하고, '-원' 등 사람 명사 접미사는 오탐 방지를 위해 추상 접미사에서
    제외했다(미탐 감수 — precision 우선).
    """
    if not text.strip():
        return 0
    matched = 0
    for sentence in _segment_sentences(text):
        words = _clean_words(sentence)
        if not words:
            continue
        final = words[-1]
        # (a) '(으)로' 명사종결 — 종결 부호 유무와 무관.
        if (
            len(final) >= 2
            and final not in _RO_ADVERB_EXCEPTIONS
            and _RO_ENDING.match(final)
        ):
            matched += 1
            continue
        # (b) '추상명사 + 이/가 됩니다' 종결.
        if final == "됩니다" and len(words) >= 2:
            prev = words[-2]
            if len(prev) >= 2 and prev[-1] in ("이", "가"):
                noun = prev[:-1]
                if noun in _ABSTRACT_BECOME_NOUNS or (
                    len(noun) >= 2 and noun[-1] in _ABSTRACT_BECOME_SUFFIX
                ):
                    matched += 1
    return matched


def benefactive_calque_count(text: str) -> int:
    """A-22: 대행·협업 동사 직역 '나 대신/나와 함께 (…) 일하-' 개수.

    '나 대신·나와 함께·날 대신·저 대신'이 같은 문장 안 12자 이내에서
    '일하/일합/일해'로 이어지는 경우만 센다(works for/with me 직역).

    알려진 한계: 한국어 어순을 따라 전방(주어→동사) 방향만 본다 —
    역순 배치는 놓친다(미탐 감수 — precision 우선).
    """
    if not text.strip():
        return 0
    return sum(len(_BENEFACTIVE.findall(s)) for s in _segment_sentences(text))


def sentence_initial_deuneun_count(text: str) -> int:
    """A-24: 문장 첫 어절이 정확히 '더는'인 문장 개수.

    영어 no longer 직역의 시그니처는 문두 '더는'이다("이제는"이 자연).
    문장 중간의 '더는'("우리는 더는 기다리지 않는다")은 자연 한국어일 수
    있으므로 세지 않는다. 분할기가 줄바꿈도 문장 경계로 보므로 종결 부호
    없는 헤드라인 줄의 문두 '더는'도 잡는다.
    """
    if not text.strip():
        return 0
    matched = 0
    for sentence in _segment_sentences(text):
        words = _split_words(sentence)
        if words and _clean_word(words[0]) == "더는":
            matched += 1
    return matched


def first_person_formal_count(text: str) -> int:
    """I-7: 1인칭 공식 주어 + 격식 종결 조합 문장 개수.

    '당사는/당사가/저희는/저희가/폐사는'을 포함하면서 문장 끝 어절이
    '합니다/입니다/드립니다/드리겠습니다'로 끝나는 문장을 센다. I-7의
    시그니처는 두 조건의 조합 밀도이므로 둘 다 요구한다 — "그는
    회사원입니다"처럼 공식 주어가 없는 격식 문장은 세지 않는다.
    """
    if not text.strip():
        return 0
    matched = 0
    for sentence in _segment_sentences(text):
        if not _FORMAL_FIRST_PERSON.search(sentence):
            continue
        tail = _final_word(sentence)
        if tail and any(tail.endswith(end) for end in _FORMAL_POLITE_TAILS):
            matched += 1
    return matched


def second_person_appeal_ratio(text: str) -> dict[str, Any]:
    """A-25 신호: 3인칭 설명체 밀도 vs 2인칭 호회 부재.

    반환 dict:
    - ``third_person_declarative``: 3인칭 기술 주어(자동화가·시스템이·AI가 …)
      를 포함하고 '합니다/입니다'로 끝나는 문장 수
    - ``second_person_tokens``: 2인칭 호회 토큰(여러분·당신·고객님) 등장 횟수
    - ``appeal_absent``: 3인칭 서술 2문장 이상 + 2인칭 0회
      (taxonomy A-25 검출 임계 "문단 2회+ 이면서 2인칭 호회 0회")

    알려진 한계: 호소성(헤드라인/CTA) vs 정보성(FAQ/사양) 구간 분류는 하지
    않고 문서 전체를 한 덩어리로 본다 — 정보성 문서는 appeal_absent가
    참이어도 교정 대상이 아닐 수 있다(최종 판정은 윤문 단계의 몫).
    """
    third_person = 0
    for sentence in _segment_sentences(text):
        if not any(subj in sentence for subj in _THIRD_PERSON_TECH_SUBJECTS):
            continue
        tail = _final_word(sentence)
        if tail and any(tail.endswith(end) for end in _POLITE_DECLARATIVE_TAILS):
            third_person += 1
    second_person = len(_SECOND_PERSON_TOKENS.findall(text)) if text.strip() else 0
    return {
        "third_person_declarative": third_person,
        "second_person_tokens": second_person,
        "appeal_absent": third_person >= 2 and second_person == 0,
    }


# 카피 신호 가중치 — _INTERFERENCE_WEIGHTS와 같은 방식(성분별 기여를 [0,1]로
# 클리핑해 합산). 가중치는 taxonomy 심각도(S1 > S2)와 검출 임계("1회 결정적",
# "2회+")를 반영한 휴리스틱이며, calibration된 baseline이 없다 — baseline_v2
# placeholder 정책과 같은 정직한 미보정 상태다(정밀 보정은 별도 회차).
_COPY_INTERFERENCE_WEIGHTS = {
    "A20_mechanical_verb_per_1k": 0.5,     # S1 — 기계 맥락 1회로 결정적
    "A21_abstract_ending_per_1k": 0.5,     # S1 — 문서 2회 초과 시 강화
    "A22_benefactive_per_1k": 0.4,         # S2 — 2회+ 가산
    "A24_deuneun_initial_per_1k": 0.4,     # S2 — 문두 1회+ 가산
    "I7_first_person_formal_per_1k": 0.3,  # S2 — 3회+ 또는 종결 70%+ 가산
    "A25_appeal_absent": 1.0,              # S2 — bool 신호(0 또는 1)
}


# ---------------------------------------------------------------------------
# v2.4 신규 — 실증 대조 코퍼스에서 판별력이 확인된 지표 4종
# (근거: references/empirical-validation.md)
# ---------------------------------------------------------------------------

# C-8 대구. 두 계열을 각각 잡는다.
#
# (a) 부정-긍정 대구 "A가 아니라 B" — 실측 최강 신호.
#     `아니라는`(관형형)은 대구가 아니므로 제외한다: "문제가 아니라는 점"은
#     평범한 서술이지 이항 대립이 아니다. 뒤에 실제 대립항이 와야 대구다.
# (b) 원형 대칭 대구 "A인가, B인가" — taxonomy가 C-8 본문으로 정의한 형태.
#     (a)만 세면 고전형을 전부 놓치고, 그 상태로 전량 삭제해도 전멸 게이트가
#     통과한다. 실제로 그 구멍이 감사에서 재현됐다.
#
# 제외한 것: "이기 이전에 / 되기 이전에"는 시간 표현("문제가 되기 이전에
# 예방한다")과 구분되지 않아 뺐다. 모호한 신호를 세는 것보다 안 세는 편이 낫다.
_ANTITHESIS_NEG_RE = re.compile(r"(?:가|이)\s*아니라(?![는니])\s*\S")
_ANTITHESIS_CMP_RE = re.compile(r"(?:이기|라기)보다\s*\S")
_ANTITHESIS_SYM_RE = re.compile(r"[가-힣]인가[,?]?\s+\S{1,14}?인가")

# 철칙 #4 게이트 임계 — change_rate() 반환값과 직접 비교한다.
CHANGE_RATE_WARN = 0.30
CHANGE_RATE_ABORT = 0.50

# 장문 기준 글자 수. E-1의 실체("장문 부재")를 재는 문턱.
LONG_SENTENCE_CHARS = 100

# final.md 말미의 메타데이터 주석 블록 — 변경률 비교 전에 제거한다.
# **완결된 종단 블록만** 제거한다. 예전에는 마커부터 파일 끝까지 무조건 잘랐는데,
# 그러면 본문 중간에 마커를 하나 끼워 넣는 것만으로 그 뒤의 모든 변경이
# 변경률 계산에서 사라진다(감사에서 재현됨). 닫는 `-->`까지 갖춘 채
# 파일 끝에 있는 블록만 제거한다 — 그 외에는 본문으로 취급해 그대로 잰다.
_SUMMARY_BLOCK_RE = re.compile(
    r"\n*<!--\s*HUMANIZE-SUMMARY\b.*?-->\s*$", re.DOTALL)

# 마크업 전용 줄 / 줄머리 장식 — ignore_markup 모드에서 벗긴다.
_MARKUP_ONLY_LINE_RE = re.compile(
    r"^\s*(?:```.*|~~~.*|-{3,}|\*{3,}|={3,}|\|[\s:|-]*)\s*$"
)
_MARKUP_PREFIX_RE = re.compile(r"^\s*(?:#{1,6}\s+|>\s?|[-*+]\s+|\d{1,3}[.)]\s+)")


def antithesis_count(text: str) -> int:
    """C-8 부정-긍정 대구 개수. 실측 최강 신호(AI 5.8 vs 사람 0.6, 9.2배).

    **절대치로 판정하지 않는다.** 대구는 사람 글에도 흔한 정상 수사다.
    이 값의 용도는 두 가지다 — (a) 반복(3회 이상) 탐지, (b) 윤문 뒤
    ``before >= 5 AND after == 0``인 '전멸' 판정. 문자 diff가 못 보는
    구조 편집을 잡는 앵커다(verify_gates.py P2축).
    """
    if not text.strip():
        return 0
    return (len(_ANTITHESIS_NEG_RE.findall(text))
            + len(_ANTITHESIS_CMP_RE.findall(text))
            + len(_ANTITHESIS_SYM_RE.findall(text)))


def antithesis_rate(text: str) -> float:
    """C-8 부정 대구가 전체 문장에서 차지하는 비율. baseline 대비 z 산출용.

    ``antithesis_count``는 순수 개수이며 전멸 판정(P2축)에 쓴다. 문서 길이에
    무관한 비교가 필요한 z-score는 이 비율을 쓴다 — 개수와 비율을 같은
    baseline 셀에 물리면 짧은 글이 과대 평가된다.
    """
    sents = _segment_sentences(text)
    if not sents:
        return 0.0
    hit = sum(1 for s in sents if (_ANTITHESIS_NEG_RE.search(s)
                                   or _ANTITHESIS_CMP_RE.search(s)
                                   or _ANTITHESIS_SYM_RE.search(s)))
    return hit / len(sents)


def long_sentence_rate(text: str) -> float:
    """E-1의 실체 — 100자 이상 장문이 전체 문장에서 차지하는 비율.

    **낮을수록 AI**다(AI 8.1 vs 사람 91.3, 1000문장당 11배 차이). 모델은
    짧은 문장만 찍어내고 긴 호흡을 만들지 못한다. 처방은 **인접 문장을
    잇는 것**이며, 길이를 채우려고 내용을 덧붙이는 것은 의미 드리프트다.
    """
    sents = _segment_sentences(text)
    if not sents:
        return 0.0
    return sum(1 for s in sents if len(s) >= LONG_SENTENCE_CHARS) / len(sents)


def geosida_rate(text: str) -> float:
    """I-1 `~것이다` 종결이 전체 문장에서 차지하는 비율.

    **낮을수록 AI**다(AI 20.4 vs 사람 43.0, 1000문장당 — 사람이 두 배).
    한국어 논설문의 일반 종결이지 AI 티가 아니다. 무조건 평서화 처방이
    이 측정으로 기각됐다(empirical-validation.md#기각). 남은 판정 대상은
    연속 3회 이상 남발뿐이다.
    """
    sents = _segment_sentences(text)
    if not sents:
        return 0.0
    # 종결 위치만 센다. "그것이다는 말은"처럼 문중에 박힌 것은 I-1이 아니다.
    hit = sum(1 for s in sents if re.search(r"것이[다]\s*[.!?]?\s*$", s))
    return hit / len(sents)


def strip_summary_block(text: str) -> str:
    """final.md 말미의 HUMANIZE-SUMMARY 주석 블록을 제거한다.

    블록을 떼면 그 앞의 구분 개행이 남는다. 그대로 두면 본문이 동일한데도
    변경률이 0이 아니게 되므로(실제로 9%가 잡혔다) 끝 공백까지 정리한다.
    """
    return _SUMMARY_BLOCK_RE.sub("", text).rstrip()


def _strip_markup(text: str) -> str:
    """마크업 전용 줄을 버리고 줄머리 장식을 벗긴다. 본문은 보존."""
    kept: list[str] = []
    for line in text.splitlines():
        if _MARKUP_ONLY_LINE_RE.match(line):
            continue
        kept.append(_MARKUP_PREFIX_RE.sub("", line))
    return "\n".join(kept)


def change_rate(before: str, after: str, ignore_markup: bool = False) -> float:
    """윤문 전후 문자 기반 변경률 — 철칙 #4 게이트의 단일 진실 원천.

    반환값 0.0(동일) ~ 1.0(전면 교체). 판정은 이 값을 ``CHANGE_RATE_WARN``
    (0.30 경고) / ``CHANGE_RATE_ABORT``(0.50 강제 중단)와 비교해 내린다.
    **에이전트의 눈대중 자가 산출을 대체한다.**

    ``ignore_markup=True``면 헤딩·불릿·표 구분선 같은 마크업을 벗기고
    비교한다 — 마크업 삭제가 본문 변경률을 부풀리는 경우의 교차 확인용.
    판정을 뒤집는 근거로 쓸 때는 두 수치를 모두 보고해야 한다.
    """
    before = strip_summary_block(before)
    after = strip_summary_block(after)
    if ignore_markup:
        before = _strip_markup(before)
        after = _strip_markup(after)
    if not before and not after:
        return 0.0
    return 1.0 - difflib.SequenceMatcher(None, before, after, autojunk=False).ratio()


def sentence_touch_rate(before: str, after: str) -> tuple[float, int, int]:
    """원문 문장 중 윤문본에 그대로 남지 않은 비율.

    **게이트가 아니라 보고용이다.** 정상적인 구조 편집도 문자 diff가
    거의 못 잡는 수준에서 문장을 많이 건드린다(실측: change_rate 2.77%
    뒤에 문장 터치율 29.7%가 은닉).
    """
    src = [re.sub(r"\s+", "", s) for s in _segment_sentences(strip_summary_block(before))]
    dst_list = [re.sub(r"\s+", "", s) for s in _segment_sentences(strip_summary_block(after))]
    if not src:
        return 0.0, 0, 0
    # 다중집합으로 센다. 집합을 쓰면 같은 문장이 둘 있다가 하나 지워져도
    # "그대로 있다"로 읽혀 삭제가 통째로 안 보인다.
    remaining = Counter(dst_list)
    touched = 0
    for s in src:
        if remaining.get(s, 0) > 0:
            remaining[s] -= 1
        else:
            touched += 1
    return touched / len(src), touched, len(src)


def copy_interference_index(text: str) -> dict[str, Any]:
    """A-20~A-25 + I-7 카피 번역투 가중 합성 신호.

    카운트 신호는 1천 자당 빈도로 정규화하고(A-25는 bool → 0/1), 각 성분을
    가중한 뒤 [0,1]로 클리핑해 합산한 weighted_total을 함께 돌려준다.
    가중치는 휴리스틱이다(미보정 — _COPY_INTERFERENCE_WEIGHTS 주석 참고).
    """
    sentence_count = max(len(_segment_sentences(text)), 1)
    char_count = max(len(text), 1)
    appeal = second_person_appeal_ratio(text)
    components = {
        "A20_mechanical_verb_per_1k": mechanical_verb_calque_count(text) / char_count * 1000,
        "A21_abstract_ending_per_1k": abstract_noun_ending_count(text) / char_count * 1000,
        "A22_benefactive_per_1k": benefactive_calque_count(text) / char_count * 1000,
        "A24_deuneun_initial_per_1k": sentence_initial_deuneun_count(text) / char_count * 1000,
        "I7_first_person_formal_per_1k": first_person_formal_count(text) / char_count * 1000,
        "A25_appeal_absent": 1.0 if appeal["appeal_absent"] else 0.0,
    }
    weighted_total = 0.0
    for name, raw_value in components.items():
        scaled = raw_value * _COPY_INTERFERENCE_WEIGHTS[name]
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
    """v1.6 지표 + v2.0 post-editese + T1~T8 신호 + v2.1 카피 신호를 산출한다.

    v1.6 compute_all 결과에 다음을 더한다:
        - ``v2_metrics``: 신규 14개 지표 값
        - ``v2_interference_index``: T1~T8 합성 신호
        - ``v2_z_scores``: baseline_v2 대비 지표별 z(placeholder면 None)
        - ``v2_baseline_warnings``: baseline 셀이 `_placeholder: true`인 지표 키 목록
        - ``v2_copy_metrics``: v2.1 카피 장르 신호 6종 원값(A-20~A-25·I-7)
        - ``v2_copy_interference_index``: 카피 번역투 가중 합성 신호

    카피 신호는 z-score를 산출하지 않는다 — baseline_v2의 copy 장르 셀은
    전부 `_placeholder: true`(미보정)이며, 원값 + 합성 신호만 보고한다.
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
        # v2.4 — 실증 대조 코퍼스에서 판별력이 확인된 지표
        "antithesis_count": antithesis_count(text),
        "antithesis_rate": antithesis_rate(text),
        "long_sentence_rate": long_sentence_rate(text),
        "geosida_rate": geosida_rate(text),
    }
    interference = interference_index(text)
    copy_metrics: dict[str, Any] = {
        "mechanical_verb_calque_count": mechanical_verb_calque_count(text),
        "abstract_noun_ending_count": abstract_noun_ending_count(text),
        "benefactive_calque_count": benefactive_calque_count(text),
        "sentence_initial_deuneun_count": sentence_initial_deuneun_count(text),
        "first_person_formal_count": first_person_formal_count(text),
        "second_person_appeal_ratio": second_person_appeal_ratio(text),
    }

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
    report["v2_copy_metrics"] = copy_metrics
    report["v2_copy_interference_index"] = copy_interference_index(text)
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="korean-humanize v2.1 메트릭 러너")
    parser.add_argument("--input", required=True, help="입력 텍스트 파일 경로")
    parser.add_argument(
        "--genre", default="essay", help="essay/news/blog/qa/dialogue/copy"
    )
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
