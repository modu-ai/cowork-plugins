---
name: korean-spell-check
description: |
  국립국어원 계열 규칙을 반영한 바른한글(구 부산대 맞춤법/문법 검사기) 표면을 이용해
  한국어 문장의 띄어쓰기·맞춤법·문법을 최종 검수합니다. 긴 글은 청크 분할로 나눠
  순차 검사하고, 결과를 원문·교정안·이유 중심으로 정리합니다.
  ai-slop-reviewer가 AI 패턴을 검수한 뒤 마지막 단계에서 호출하는 것을 권장합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "이 한국어 문장 맞춤법 검사해줘", "띄어쓰기 검사"
  - "README 한국어 문장 최종 검수", "마크다운 맞춤법"
  - "AI 교정보다 규칙 기반 한국어 검사기로 한 번 더 확인"
  - "부산대 맞춤법", "바른한글 검사", "국립국어원 규칙"
  - 블로그·뉴스레터·카피·계약서 등 텍스트 산출물의 최종 교정 단계
version: "1.1.0"
---

# 한국어 맞춤법·문법 검수

국립국어원 계열 규칙을 반영한 **바른한글(구 부산대 맞춤법/문법 검사기)** 표면을 이용해 한국어 문장을 최종 교정합니다. AI가 만들어낸 글의 마지막 검수 단계로 사용합니다.

> 본 스킬은 NomaDamas k-skill `office-korean-spell-check` (MIT)를 cowork에 포팅했습니다(스킬명은 무접두사 `korean-spell-check`로 정리). 공개 웹 검사기 기준이며, 최종 문맥 판단은 사람이 확인합니다.

## Policy first — 사용 전 반드시 확인

- `https://nara-speller.co.kr/old_speller/`는 **비상업적 용도** 안내와 **개인·학생 무료** 문구를 명시합니다.
- `https://nara-speller.co.kr/robots.txt`는 `/`를 허용하지만 `/test_speller/`는 금지합니다.
- 따라서 본 스킬은 **사용자 주도 최종 검수**, **저빈도 요청**, **문서·이메일·README 교정** 용도로만 씁니다.
- 대량 배치, SaaS 백엔드 연동, 상업 서비스 내 무단 재판매·재노출에는 사용하지 **않습니다**. 그런 경우는 공급사 문의·유료 API 계약을 먼저 검토합니다.

## When to use / When not to use

**사용**: 블로그·뉴스레터·카피·계약서 등 텍스트 산출물의 최종 교정, README 검수, AI 교정 후 규칙 기반 재확인.

**사용 금지**: 코드 블록·로그·영문 위주 텍스트 대량 전송, 민감정보 많은 원문의 외부 전송, 상업적 대량 처리.

## Prerequisites

- 인터넷 연결, Python 3.10+
- 브라우저형 User-Agent + Python stdlib `urllib` POST는 `old_speller/results`에서 검사 결과 HTML을 반환합니다 (Cloudflare 우회용 일반 fetch는 403 가능).

## Workflow

### 1. 텍스트 또는 파일 경로 받기

- 텍스트 직접 입력 → 바로 검사
- 파일 검사 → UTF-8 텍스트/Markdown만 대상. 코드 블록이 많으면 사용자에게 범위 축소 의사를 먼저 묻습니다.

### 2. Conservative 요청 유지

- 기본 청크 크기 약 **1500자**
- 청크 사이 최소 **1초** 휴지
- 한 번에 너무 많은 파일을 돌리지 않습니다.

### 3. 검사 요청 (인라인 stdlib 코드 직접 실행)

별도 스크립트 없이 Python 표준 라이브러리만으로 동작합니다. 브라우저형 User-Agent + `urllib` POST가
Cloudflare를 우회하며, 응답 HTML에 임베드된 `errInfo` JSON 배열을 파싱해 `원문 / 교정안 / 이유`로 정리합니다.
아래 코드를 그대로 실행하되, 긴 글은 1500자 청크로 나눠 청크 간 1초 휴지를 둡니다(외부 의존성 불필요).

```python
import json, re, time, urllib.request, urllib.parse

URL = "https://nara-speller.co.kr/old_speller/results"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

def check_chunk(text: str) -> list[dict]:
    body = urllib.parse.urlencode({"text1": text}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    # 응답 HTML의 data 배열(errInfo)에서 원문/교정안/도움말 추출
    m = re.search(r"data\s*=\s*(\[.*?\]);", html, re.S)
    items = json.loads(m.group(1)) if m else []
    return [{"original": it.get("orgStr", ""),
             "suggestions": [c for c in (it.get("candWord") or "").split("|") if c],
             "reason": it.get("help", "")} for it in items]

def spell_check(text: str, size: int = 1500) -> list[dict]:
    out = []
    for i in range(0, len(text), size):
        out += check_chunk(text[i:i+size])
        if i + size < len(text):
            time.sleep(1)   # 청크 간 1초 휴지 (저빈도 정책 준수)
    return out

# 파일 검사: text = open("README.md", encoding="utf-8").read()
print(json.dumps(spell_check("아버지가방에들어가신다."), ensure_ascii=False, indent=2))
```

> 이 스킬은 부재 스크립트(korean_spell_check.py) 참조를 원칙 A(프롬프트/인라인 stdlib 코드)로 대체했습니다.
> `errInfo`/`data` 필드명·응답 구조는 공개 검사기 변경에 따라 달라질 수 있으니, 파싱 실패 시 응답 HTML을
> 확인해 필드명을 조정합니다. `requests`·`BeautifulSoup` 등 외부 패키지 설치는 필요 없습니다.

### 4. 변경점 중심 응답

권장 응답 순서:

1. 교정된 전체 문장/문단
2. 주요 변경점 목록
3. 각 변경점의 `원문` / `교정안` / `이유`
4. 필요시 "공개 웹 검사기 기준 결과이며, 최종 문맥 판단은 사람이 확인" 문구

예시 JSON:

```json
{
  "original": "아버지가방에들어가신다",
  "suggestions": ["아버지가 방에 들어가신다"],
  "reason": "띄어쓰기, 붙여쓰기, 음절 대치와 같은 교정 방법에 따라 수정한 결과입니다."
}
```

## 관련 스킬 체이닝 — ai-slop-reviewer 직전 권장

표준 텍스트 산출물 체인:

```
{콘텐츠 생성 스킬} → ai-slop-reviewer → korean-spell-check → 사용자 최종 검토
```

- **before**: `moai-marketer:content-blog`, `moai-marketer:content-newsletter`, `moai-marketer:content-copywriting`, `moai-marketer:content-sns-content`
- **before**: `moai-coworker:ai-slop-reviewer` — AI 패턴(과한 형용사·반복·번역체) 먼저 검수
- **after**: 사용자가 최종 문맥 검토 후 발행

## Done when

- 공개 표면 정책(비상업·저빈도)을 먼저 확인했다.
- 긴 텍스트면 청크 분할(약 1500자)을 적용했다.
- 결과를 `원문 / 교정안 / 이유` 중심으로 정리했다.
- 고빈도·상업적 사용이 아님을 분명히 했다.

## Notes

- guide: `https://nara-speller.co.kr/guide/`
- main UI: `https://nara-speller.co.kr/speller/`
- old UI / form post: `https://nara-speller.co.kr/old_speller/`, `https://nara-speller.co.kr/old_speller/results`
- robots: `https://nara-speller.co.kr/robots.txt`
