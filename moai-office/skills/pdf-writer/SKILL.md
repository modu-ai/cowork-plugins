---
name: pdf-writer
description: |
  어떤 콘텐츠든 PDF 파일로 만들어 드립니다 — 스타일이 입혀진 HTML 리포트는 디자인을 그대로 보존해
  변환하고, Markdown·구조화 JSON·일반 텍스트는 자동 서식으로 렌더합니다. weasyprint 단일 엔진으로
  풀 CSS를 충실히 렌더하며, 번들 Noto Sans CJK 폰트를 임베딩해 한국어·일본어·중국어 글리프 깨짐을
  근본 차단합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "PDF로 만들어줘", "PDF로 생성해줘", "PDF로도 생성해줘", "PDF로 저장해줘", "PDF로 출력해줘", "PDF로 뽑아줘"
  - "이거 PDF로", "이 리포트 PDF로", "이 보고서 PDF로 변환해줘", "HTML을 PDF로", "HTML 리포트를 PDF로"
  - "PDF로 변환해줘", "문서 PDF 파일 생성", "보고서 PDF로 저장해줘", "계획서 PDF 파일"
  - "한글 PDF 만들어줘", "한국어 PDF", "일본어 PDF", "중국어 PDF", "다국어 PDF", "CJK PDF"
  - "한글 깨짐 없는 PDF", "한자 깨짐 없는 PDF", "폰트 임베딩 PDF"
  - "Markdown을 PDF로", "JSON 입력으로 PDF 문서 생성"
  PDF 생성·변환 요청 시 weasyprint를 직접 설치·호출하거나 Claude 기본 도구로 처리하지 말고,
  반드시 이 스킬(scripts/render_pdf.py)을 사용하세요. 이 스킬이 내부적으로 weasyprint를
  올바른 CJK 폰트 설정과 함께 호출합니다.
user-invocable: true
version: 2.27.0
---

# PDF 생성기 (pdf-writer)

## 개요

**weasyprint 단일 엔진**으로 모든 입력을 PDF로 렌더합니다. 입력 형태와 무관하게
`입력 → HTML → weasyprint → PDF` 한 경로로 통일되어, 다음 두 시나리오를 모두 충실히 처리합니다.

1. **스타일이 입혀진 HTML 리포트** (예: `moai-content:html-report`·`moai-content:html-slide` 산출물,
   또는 사용자가 만든 디자인 HTML) → **자체 CSS를 그대로 렌더해 화면 디자인을 보존**합니다.
   2열 카드 그리드·커스텀 색·웹폰트 등 모던 CSS 레이아웃이 깨지지 않습니다.
2. **Markdown · 구조화 JSON · 일반 텍스트** → 기본 문서 서식(A4·표·제목 스타일)을 적용해 렌더합니다.

CJK(한·중·일) 글리프는 번들 **Noto Sans CJK** 폰트를 `@font-face`로 임베딩해 깨짐을 차단하며,
시스템에 `Noto Sans CJK KR`이 설치돼 있으면 fontconfig가 자동 폴백합니다.

> **왜 weasyprint 단일 엔진인가**: weasyprint는 풀 CSS(레이아웃·색·웹폰트·표)를 충실히 렌더합니다.
> "이 HTML 리포트를 디자인 그대로 PDF로"가 가장 흔한 요청이며, 이 경로가 그 요구를 정확히 만족합니다.
> 좌표 기반 저수준 렌더링(예: PyMuPDF insert_text)은 모던 CSS 레이아웃을 재현하지 못하므로 사용하지 않습니다.

## 워크플로우

```
0. [폰트 확인]  → assets/fonts/ 에 Noto Sans CJK OTF 4종 존재 확인, 누락 시 download_fonts.py 자동 호출
1. [입력 감지]  → HTML(완성 문서) / Markdown / JSON / Text 자동 감지
2. [HTML 빌드]  → 완성 HTML은 그대로, 그 외는 HTML로 변환 (+ 기본 문서 CSS)
3. [폰트 주입]  → Noto Sans CJK @font-face CSS 결합 (CJK 깨짐 방지)
4. [렌더]       → weasyprint HTML.write_pdf() 로 A4 PDF 생성
5. [자체 검수]  → 산출 PDF 재확인 (페이지 수·CJK 표시·플레이스홀더 잔존)
```

핵심 실행은 번들 스크립트 한 줄로 끝납니다:

```bash
# HTML 리포트를 디자인 그대로 PDF로 (가장 흔한 케이스)
python3 moai-office/skills/pdf-writer/scripts/render_pdf.py --in report.html --out report.pdf

# Markdown / JSON / Text → PDF
python3 moai-office/skills/pdf-writer/scripts/render_pdf.py --in doc.md   --out doc.pdf
python3 moai-office/skills/pdf-writer/scripts/render_pdf.py --in data.json --out doc.pdf
```

`scripts/render_pdf.py`가 입력 종류를 자동 감지하고, 완성 HTML은 자체 CSS를 보존한 채 렌더하며,
Markdown/JSON/Text는 기본 서식 + Noto Sans CJK를 적용합니다.

### 0단계: 폰트 자동 보장 (스킬 진입점)

```python
import subprocess, sys
from pathlib import Path

SKILL_ROOT = Path(__file__).parent
DOWNLOADER = SKILL_ROOT / "scripts" / "download_fonts.py"

def ensure_fonts():
    """Noto Sans CJK OTF 4종 존재 검증, 누락 시 자동 다운로드."""
    if subprocess.run([sys.executable, str(DOWNLOADER), "--check"]).returncode != 0:
        if subprocess.run([sys.executable, str(DOWNLOADER)]).returncode != 0:
            raise RuntimeError("Noto Sans CJK 폰트 다운로드 실패. 네트워크/GitHub 접근 확인 필요.")

ensure_fonts()  # PDF 생성 직전 호출
```

다운로드는 최초 1회(약 64MB)만 발생하며, 이후 `--check`가 즉시 통과합니다. 시스템에
`Noto Sans CJK KR`이 이미 있으면 폰트가 없어도 weasyprint가 자동 폴백하므로 CJK는 안전하게 표시됩니다.

### 1~4단계: weasyprint 렌더링 핵심 코드

`scripts/render_pdf.py`의 핵심은 다음과 같습니다 (전체 구현은 스크립트 참조):

```python
from weasyprint import HTML, CSS
from pathlib import Path

FONT_DIR = Path("moai-office/skills/pdf-writer/assets/fonts")

# 번들 Noto Sans CJK를 @font-face로 등록 (weight별)
FONT_FACE = "".join(
    f"@font-face{{font-family:'Noto Sans CJK';font-weight:{w};"
    f"src:url('file://{FONT_DIR}/NotoSansCJK-{n}.otf');}}"
    for w, n in {300: "Light", 400: "Regular", 500: "Medium", 700: "Bold"}.items()
    if (FONT_DIR / f"NotoSansCJK-{n}.otf").exists()
)

# (A) 완성 스타일 HTML → 자체 CSS 보존, CJK 폰트만 보강
HTML(string=styled_html, base_url=".").write_pdf("out.pdf", stylesheets=[CSS(string=FONT_FACE)])

# (B) Markdown/JSON/Text에서 만든 HTML → 기본 문서 CSS + 폰트
HTML(string=plain_html, base_url=".").write_pdf("out.pdf", stylesheets=[CSS(string=FONT_FACE + BASE_CSS)])
```

`BASE_CSS`는 `@page { size:A4; margin:20mm }` + 본문/제목/표 스타일로, `font-family`에
`'Noto Sans CJK'`를 지정해 CJK가 항상 임베딩 폰트로 렌더되게 합니다.

## 의존성

```bash
pip install weasyprint   # 핵심 렌더링 엔진 (풀 CSS → PDF)
pip install markdown     # Markdown → HTML 변환 (선택, 없으면 최소 폴백)
```

> weasyprint는 시스템 라이브러리 `cairo` / `pango` / `gdk-pixbuf`를 사용합니다. 대부분의
> Cowork 샌드박스 및 Linux/macOS 환경에 기본 포함돼 있어 `pip install weasyprint`만으로 동작합니다.

## 입력 포맷 명세

### 완성 HTML (디자인 보존)

`<html>`·`<body>`·`<!doctype html>` 신호가 있으면 **완성 문서로 간주**하여 자체 `<style>`·CSS를
그대로 렌더합니다. `moai-content:html-report`·`moai-content:html-slide` 산출물을 그대로 넘기면
화면과 동일한 디자인의 PDF가 나옵니다.

### 구조화 JSON 스펙

```json
{
  "title": "문서 제목",
  "subtitle": "부제목 (선택)",
  "author": "작성자 (선택)",
  "date": "2026-01-01 (선택)",
  "sections": [
    {
      "heading": "섹션 제목",
      "level": 2,
      "body": "본문 텍스트 (마크다운 인라인 지원)",
      "table": { "headers": ["열1", "열2"], "rows": [["a", "b"]] },
      "image": { "path": "./chart.png", "caption": "그림 1" }
    }
  ]
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

- "이 HTML 리포트를 디자인 그대로 PDF로 만들어줘" → 완성 HTML 경로 (CSS 보존)
- "주간 보고서 Markdown을 한글 깨짐 없는 PDF로" → Markdown 경로 (기본 서식 + CJK)
- "아래 JSON 구조로 분기 보고서 PDF를 생성해줘" → JSON 경로
- "한·일·중·영 혼용 매뉴얼을 PDF로 출력해줘" → 다국어 임베딩

## 출력 형식

- **파일 형식**: `.pdf` (ISO 32000 PDF 표준)
- **페이지 크기**: A4 (210 × 297mm, 기본 여백 20mm) — 완성 HTML은 자체 `@page` 설정을 우선
- **폰트**: Noto Sans CJK (한국어·일본어·중국어 간체·번체·라틴 단일 패밀리 커버, 서브셋 임베딩)
- **인코딩**: UTF-8 완전 지원

## 자체 검수

PDF 생성 후 산출 `.pdf`를 다시 열어 **플레이스홀더 잔존·페이지 수 미달·CJK 인코딩 깨짐·디자인
누락**을 자체 점검하고, 문제가 있으면 자동 수정 후 재생성하며 최종 PASS/FAIL을 보고합니다.

## 문제 해결

| 증상 | 원인 | 해결 방법 |
|------|------|-----------|
| 한글/한자가 □□□ 또는 공백 | CJK 폰트 미해결 | `download_fonts.py` 실행으로 번들 OTF 확보, 또는 시스템 `Noto Sans CJK KR` 설치 |
| `ModuleNotFoundError: weasyprint` | weasyprint 미설치 | `pip install weasyprint` 실행 |
| `cannot load library 'libpango...'` | 시스템 라이브러리 부재 | (Debian/Ubuntu) `apt install libpango-1.0-0 libpangocairo-1.0-0`, (macOS) `brew install pango` |
| HTML 디자인이 PDF에서 깨짐 | 완성 HTML이 조각으로 오인됨 | 입력에 `<html>`/`<body>` 래퍼 포함, 또는 `--in *.html` 파일로 전달 |
| 웹폰트(CDN) 미적용 | 오프라인/CDN 차단 | HTML에 폰트를 인라인하거나 시스템 폰트로 대체 (오프라인 PDF는 CDN 의존 회피 권장) |
| 표가 페이지 경계에서 분리 | CSS 미지정 | `tr { page-break-inside: avoid; }` 추가 |

## 관련 스킬 / 핸드오프

| 스킬 | 관계 | 사용 시점 |
|------|------|-----------|
| `moai-content:html-report` | before (HTML 리포트 생성 → 이 스킬로 PDF 변환) | "리포트 만들고 PDF로도" 흐름 |
| `moai-content:html-slide` | before (HTML 슬라이드 생성 → PDF 변환) | 슬라이드 덱을 PDF 배포본으로 |
| `moai-office:docx-generator` | alternative (편집 가능한 Word 산출물) | 수신자가 편집 가능 파일 필요 시 |
| `moai-core:ai-slop-reviewer` | after (텍스트 산출물 AI 패턴 검수) | 텍스트 PDF 생성 전 원고 검수 |

## 기술 참조

- **weasyprint 공식 문서**: https://doc.courtbouillon.org/weasyprint/stable/
- **Noto Sans CJK GitHub**: https://github.com/notofonts/noto-cjk
- **Noto Sans CJK 릴리스 (otf 다운로드)**: https://github.com/notofonts/noto-cjk/releases
- **SIL OFL 1.1 라이선스**: https://openfontlicense.org/open-font-license-official-text/
- **PDF ISO 32000 표준**: https://opensource.adobe.com/dc-acrobat-sdk-docs/
