---
name: pdf-writer
description: |
  한국어·일본어·중국어·영어 다국어 PDF 파일을 깨짐 없이 생성합니다. PyMuPDF + Noto Sans CJK
  번들 폰트 조합으로 CJK(한중일) 글리프 누락 문제를 근본 해결하며, Markdown·구조화 JSON·HTML·일반 텍스트
  4종 입력을 모두 지원합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "한글 PDF 만들어줘", "한국어 PDF 생성해줘"
  - "일본어 PDF", "중국어 PDF", "다국어 PDF", "CJK PDF"
  - "Markdown을 PDF로 변환해줘", "마크다운 PDF 출력"
  - "한글 깨짐 없는 PDF", "한자 깨짐 없는 PDF", "폰트 임베딩 PDF"
  - "보고서 PDF로 저장해줘", "계획서 PDF 파일 생성"
  - "PyMuPDF로 PDF 만들어줘", "Noto Sans CJK PDF"
  - "JSON 입력으로 PDF 문서 생성", "HTML을 PDF로"
  PDF 생성 요청 시 Claude 기본 도구 대신 이 스킬을 우선 사용하세요.
user-invocable: true
version: 2.1.0
---

# PDF 생성기 (pdf-writer)

## 개요

PyMuPDF + Noto Sans CJK 번들 폰트 조합으로 **한·중·일·영 다국어 PDF**를 깨짐 없이 생성합니다.
Noto Sans CJK는 Google·Adobe 합작 오픈소스 폰트로 한국어(Hangul), 일본어(Hiragana/Katakana/Kanji),
중국어 간체(Simplified)·번체(Traditional), 라틴 문자를 단일 폰트 패밀리에서 모두 커버합니다.
Markdown, 구조화 JSON, HTML, 일반 텍스트 4종 입력을 지원하며, A4 규격에 폰트를 자동 서브셋 임베딩합니다.

## 트리거 키워드

한글 PDF 한국어 PDF 일본어 PDF 중국어 PDF 다국어 PDF CJK PDF Markdown PDF PDF 변환 한글 깨짐 한자 깨짐 폰트 임베딩 PyMuPDF Noto Sans CJK 보고서 PDF 계획서 PDF JSON PDF HTML PDF

## 워크플로우

```
0. [폰트 확인]  → assets/fonts/ 에 OTF 4종 존재 확인, 누락 시 download_fonts.py 자동 호출
1. [입력 감지]  → 입력 포맷 자동 감지 (Markdown / JSON / HTML / Text)
2. [파싱]       → 포맷별 파서로 구조 추출 (제목/본문/표/이미지)
3. [레이아웃]   → A4 페이지 여백·폰트 크기·행간 계획
4. [렌더링]     → PyMuPDF insert_font + insert_text / Story API로 렌더
5. [폰트 임베딩]→ Noto Sans CJK .otf를 PDF에 서브셋 임베딩
6. [저장]       → .pdf 파일 저장
```

### 0단계: 폰트 자동 보장 (스킬 진입점)

```python
import subprocess, sys
from pathlib import Path

SKILL_ROOT = Path(__file__).parent
DOWNLOADER = SKILL_ROOT / "scripts" / "download_fonts.py"

def ensure_fonts():
    """폰트 4종 OTF 존재 검증, 누락 시 자동 다운로드."""
    result = subprocess.run(
        [sys.executable, str(DOWNLOADER), "--check"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        # 누락 weight 발견 → 다운로드 실행
        dl = subprocess.run([sys.executable, str(DOWNLOADER)], text=True)
        if dl.returncode != 0:
            raise RuntimeError(
                "Noto Sans CJK 폰트 다운로드 실패. "
                "네트워크 연결 또는 GitHub 접근을 확인하세요."
            )

ensure_fonts()  # PDF 생성 작업 직전 호출
```

다운로드는 첫 실행 시 1회(약 64MB, 네트워크 속도에 따라 10~60초)만 발생하며, 이후 실행에서는 `--check`가 즉시 통과합니다.

### 1단계: 입력 감지 및 파싱

| 입력 포맷 | 감지 기준 | 파서 |
|-----------|-----------|------|
| Markdown | `#`, `**`, `-`, `` ` `` 패턴 존재 | `markdown` 라이브러리 → HTML 변환 후 BeautifulSoup |
| JSON | `{` 로 시작, `title`/`sections` 키 존재 | `json.loads()` |
| HTML | `<html>`, `<body>`, `<h1>` 태그 존재 | `BeautifulSoup` |
| Text | 위 조건 미해당 | 단락 분리 후 직접 삽입 |

### 2단계: 폰트 관리 — Noto Sans CJK 번들

폰트 파일은 스킬 디렉토리의 `assets/fonts/` 에 배치합니다.

```
moai-office/skills/pdf-writer/
└── assets/
    └── fonts/
        ├── NotoSansCJK-Regular.otf    # ~16MB, 한·중·일·영 통합
        ├── NotoSansCJK-Medium.otf
        ├── NotoSansCJK-Bold.otf
        └── NotoSansCJK-Light.otf
```

**파일 선택 가이드**:

| 파일 형태 | 권장 시나리오 | 비고 |
|-----------|--------------|------|
| `NotoSansCJKkr-*.otf` (또는 jp/sc/tc) | 단일 언어 우선 디자인 + 다국어 fallback | 16MB/weight, 가장 명확함 |
| `NotoSansCJK-*.ttc` (TTC 합본) | 4개 언어 디자인 변형 모두 보존 | 120MB/weight, fontindex 지정 필요 |
| `NotoSans*-*.otf` (언어 분리, KR/JP/SC/TC) | 언어별 폰트 자동 전환 | 여러 폰트 등록 필요, 로직 복잡 |

> **권장**: 대부분 케이스는 `NotoSansCJKkr-Regular.otf` + `NotoSansCJKkr-Bold.otf` 2개로 충분합니다.
> 한국어 변형(kr)은 한·중·일·영 글리프를 모두 포함하며, 한국어 디자인 선호가 우선 적용됩니다.

**폰트 라이선스 고지**: Noto Sans CJK는 **SIL Open Font License 1.1** 하에 배포됩니다.
상업적 사용 가능, 수정 배포 시 동일 라이선스 적용 필요.
공식 배포처: https://github.com/notofonts/noto-cjk/releases

**폰트 자동 다운로드**: 폰트 바이너리는 저장소에 포함되지 않으며, 스킬 최초 실행 시 자동 다운로드됩니다.

```
assets/fonts/
├── (NotoSansCJK-{Light,Regular,Medium,Bold}.otf)   # 자동 다운로드 (각 ~16MB, 총 ~64MB)
├── LICENSE.txt                                      # SIL OFL 1.1 전문 (저장소 포함)
├── README.md                                        # 출처·갱신 절차 (저장소 포함)
└── .gitignore                                       # *.otf/*.ttf/*.ttc 제외
```

**최초 실행 시 자동 다운로드 절차**:

```bash
# 1) 폰트 상태 확인 (다운로드 없이 점검만)
python3 moai-office/skills/pdf-writer/scripts/download_fonts.py --check

# 2) 누락 weight만 다운로드
python3 moai-office/skills/pdf-writer/scripts/download_fonts.py

# 3) 강제 재다운로드 (무결성 의심 시)
python3 moai-office/skills/pdf-writer/scripts/download_fonts.py --force
```

스킬 코드는 PDF 생성 직전 `--check` 모드로 폰트 존재를 검증하고, 누락 시 자동으로 다운로드를 호출하도록 작성합니다 (워크플로우 0단계 참조). 다운로드는 `urllib.request`만 사용하며 추가 의존성이 없습니다.

### 3단계: PyMuPDF 핵심 코드

```python
import pymupdf  # PyMuPDF 1.24+
from pathlib import Path

FONT_DIR = Path(__file__).parent / "assets" / "fonts"
FONTS = {
    "regular":  FONT_DIR / "NotoSansCJK-Regular.otf",
    "medium":   FONT_DIR / "NotoSansCJK-Medium.otf",
    "bold":     FONT_DIR / "NotoSansCJK-Bold.otf",
    "light":    FONT_DIR / "NotoSansCJK-Light.otf",
}

doc = pymupdf.open()
page = doc.new_page(width=595, height=842)  # A4 포인트 기준

# 핵심: insert_font로 CJK 폰트를 페이지에 등록
page.insert_font(fontname="notosans",      fontfile=str(FONTS["regular"]))
page.insert_font(fontname="notosans-bold", fontfile=str(FONTS["bold"]))

# 한·중·일·영 혼용 텍스트 삽입 — fontname은 위에서 등록한 별칭 사용
page.insert_text(
    point=(72, 100),
    text="안녕하세요. こんにちは。你好。Hello.",
    fontname="notosans",
    fontsize=11,
)

# 제목 (Bold)
page.insert_text(
    point=(72, 72),
    text="다국어 보고서 / 多言語レポート / 多语言报告",
    fontname="notosans-bold",
    fontsize=16,
)

doc.save("output.pdf")  # 폰트는 자동 서브셋 임베딩 (실제 사용 글리프만)
```

**TTC(합본) 사용 시 — 언어별 디자인 분기가 필요한 경우**:

```python
# NotoSansCJK-Regular.ttc 는 kr/jp/sc/tc 4개 face 를 포함
# fontindex로 face 를 선택 (0=jp, 1=kr, 2=sc, 3=tc — 릴리스에 따라 다를 수 있음)
page.insert_font(
    fontname="notosans-kr",
    fontfile=str(FONT_DIR / "NotoSansCJK-Regular.ttc"),
    fontindex=1,
)
page.insert_font(
    fontname="notosans-jp",
    fontfile=str(FONT_DIR / "NotoSansCJK-Regular.ttc"),
    fontindex=0,
)
```

**Markdown / HTML 렌더링 (Story API)**:

PyMuPDF 1.23+ 에서는 `pymupdf.Story`로 HTML 기반 레이아웃을 처리할 수 있습니다.

```python
# HTML 입력 → Story API 렌더링 (표, 목록, 이미지 포함)
story = pymupdf.Story(html=html_content, user_css="""
    body { font-family: notosans; font-size: 11pt; }
    h1   { font-size: 18pt; font-weight: bold; }
""")
story.place(mediabox=pymupdf.Rect(72, 72, 523, 770))
story.draw(page)
```

TextWriter API는 여러 스타일이 혼합된 단락 렌더링에 적합합니다:

```python
tw = pymupdf.TextWriter(page.rect)
tw.append((72, 200), "강조 텍스트", fontname="notosans-bold", fontsize=12)
tw.append((72, 220), "일반 텍스트", fontname="notosans", fontsize=11)
tw.write_text(page)
```

## 의존성

```bash
pip install pymupdf              # PyMuPDF 1.24+ (핵심 렌더링)
pip install markdown             # Markdown → HTML 변환
pip install beautifulsoup4 lxml  # HTML 파싱
```

> PyMuPDF는 `import pymupdf` (1.24+) 와 `import fitz` (구버전) 두 가지 네임스페이스를 지원합니다.
> 1.24 이상을 권장합니다.

## 입력 포맷 명세

### 구조화 JSON 스펙

```json
{
  "title": "문서 제목",
  "subtitle": "부제목 (선택)",
  "author": "작성자 (선택)",
  "date": "2024-01-01 (선택)",
  "sections": [
    {
      "heading": "섹션 제목",
      "level": 1,
      "body": "본문 텍스트 (마크다운 인라인 지원)",
      "table": {
        "headers": ["열1", "열2", "열3"],
        "rows": [
          ["데이터1", "데이터2", "데이터3"]
        ]
      },
      "image": {
        "path": "./assets/chart.png",
        "caption": "그림 1. 설명",
        "width": 400
      }
    }
  ],
  "page_settings": {
    "size": "A4",
    "margin_mm": 25,
    "font_size": 11
  }
}
```

### Markdown 입력 예시

```markdown
# 프로젝트 보고서

## 1. 개요
본 보고서는 ...

## 2. 결과
| 항목 | 수치 |
|------|------|
| 완료율 | 95% |
```

## 사용 예시

- "이 Markdown 내용을 한글 깨짐 없는 PDF로 만들어줘"
- "아래 JSON 구조로 분기 보고서 PDF를 생성해줘"
- "HTML 파일을 PDF로 변환해줘, Noto Sans CJK 폰트 사용"
- "한·일·중·영 혼용된 다국어 매뉴얼을 PDF로 출력해줘"
- "일반 텍스트 내용을 A4 PDF로 정리해줘"

## 출력 형식

- **파일 형식**: `.pdf` (ISO 32000 PDF 표준)
- **페이지 크기**: A4 (595 × 842 포인트, 210 × 297mm)
- **기본 여백**: 좌우 72pt (25.4mm), 상하 72pt
- **기본 폰트**: Noto Sans CJK Regular 11pt
- **제목 폰트**: Noto Sans CJK Bold 14~18pt
- **다국어 커버리지**: 한국어(Hangul), 일본어(Hiragana/Katakana/Kanji), 중국어 간체·번체, 라틴
- **폰트 임베딩**: 서브셋 임베딩 (실제 사용 글리프만, 파일 크기 최소화)
- **인코딩**: UTF-8 완전 지원

## 주의사항

### CJK 다국어 처리 핵심 주의점

| 항목 | 주의 내용 |
|------|-----------|
| 폰트 등록 타이밍 | `insert_font`는 `insert_text` **이전**에 반드시 호출 |
| fontname 일치 | `insert_font`의 `fontname`과 `insert_text`의 `fontname`이 **정확히 동일**해야 함 |
| CJK 글자폭 | Noto Sans CJK는 OpenType CJK 메트릭을 정확히 정의. PyMuPDF가 TTF/OTF 내장 메트릭을 그대로 사용 |
| 줄바꿈 | `insert_text`는 자동 줄바꿈 미지원. TextWriter 또는 Story API 사용 권장 |
| 이미지 임베딩 | `page.insert_image(rect, filename=...)` — 대용량 이미지는 메모리 주의, 300dpi 이하 권장 |
| 다중 페이지 | `doc.new_page()` 호출마다 폰트 재등록 필요 (`insert_font` per page) |
| 폰트 파일 크기 | OTF 1개 ≈ 16MB. 4 weight 번들 시 ~64MB. 저장소 용량 영향 검토 |
| 서브셋 임베딩 | `doc.save(..., garbage=4, deflate=True)` 권장 — 미사용 글리프 제거로 출력 PDF 크기 최소화 |

### 폰트 파일 무결성 확인

`assets/fonts/` 에 4종 OTF가 정상 존재해야 합니다 (각 약 16MB):

```bash
ls -lh moai-office/skills/pdf-writer/assets/fonts/
# NotoSansCJK-{Light,Regular,Medium,Bold}.otf 4개 + LICENSE.txt + README.md
```

번들이 손상되었거나 누락된 경우 `assets/fonts/README.md` 의 다운로드 경로에서 재취득하세요:
https://github.com/notofonts/noto-cjk

### 언어 디자인 우선순위

Noto Sans CJK는 4개 언어 변형(`kr`/`jp`/`sc`/`tc`)이 있으며, 같은 한자라도 디자인이 다를 수 있습니다.

- 한국어 우선 문서: `NotoSansCJKkr-*.otf` 사용 (한국식 한자 디자인)
- 일본어 우선 문서: `NotoSansCJKjp-*.otf` 사용 (일본식 한자 디자인)
- 중국어 우선 문서: `NotoSansCJKsc-*.otf` (간체) 또는 `NotoSansCJKtc-*.otf` (번체)
- 모든 언어를 단일 폰트로 처리: `kr` 변형이 무난 (커버리지 동일, 디자인은 한국어 우선)

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 한글/한자가 □□□로 표시 | 폰트 미등록 또는 fontname 불일치 | `insert_font` 호출 확인, fontname 철자 점검 |
| 일부 글자만 ??? 또는 공백 | 폰트가 해당 언어 글리프 미포함 | Noto Sans CJK 변형 확인 (kr 변형이 가장 광범위) |
| `ModuleNotFoundError: pymupdf` | PyMuPDF 미설치 | `pip install pymupdf` 실행 |
| `import fitz` 오류 (1.24+) | 네임스페이스 변경 | `import pymupdf as fitz` 또는 `import pymupdf` 사용 |
| 텍스트 잘림 | 페이지 경계 초과 | `insert_textbox` 또는 Story API로 자동 줄바꿈 처리 |
| 표가 페이지 경계에서 분리 | 단순 좌표 삽입 한계 | Story API + HTML 표 사용 권장 |
| 이미지 삽입 후 메모리 증가 | 고해상도 이미지 다수 | PIL로 리사이즈 후 삽입, 300dpi 이하 유지 |
| PDF 파일 크기 과대 | 폰트 풀임베딩 | `doc.save(..., garbage=4, deflate=True)` 서브셋 + 압축 |
| TTC 사용 시 잘못된 글리프 | fontindex 불일치 | NotoSansCJK ttc는 일반적으로 jp=0, kr=1, sc=2, tc=3 (릴리스별 확인) |

## 관련 스킬

| 스킬 | 관계 | 사용 시점 |
|------|------|-----------|
| `moai-content:blog` | before (콘텐츠 먼저 생성 후 PDF 변환) | 블로그 글을 PDF 리포트로 |
| `moai-content:landing-page` | before (랜딩 카피 생성 후 PDF 제안서로) | 제안서·브로셔 PDF 제작 |
| `moai-office:docx-generator` | alternative (Word 편집 가능 산출물 원할 때) | 수신자가 편집 가능한 파일 필요 시 |
| `moai-core:ai-slop-reviewer` | after (텍스트 산출물 AI 패턴 검수) | **모든 텍스트 PDF 생성 후 필수** (CLAUDE.local.md §3-2) |

## 기술 참조

- **PyMuPDF 공식 문서**: https://pymupdf.readthedocs.io/
- **PyMuPDF Story API**: https://pymupdf.readthedocs.io/en/latest/story.html
- **Noto Sans CJK GitHub**: https://github.com/notofonts/noto-cjk
- **Noto Sans CJK 릴리스 (otf 다운로드)**: https://github.com/notofonts/noto-cjk/releases
- **Noto 폰트 프로젝트**: https://fonts.google.com/noto
- **SIL OFL 1.1 라이선스**: https://openfontlicense.org/open-font-license-official-text/
- **PDF ISO 32000 표준**: https://opensource.adobe.com/dc-acrobat-sdk-docs/