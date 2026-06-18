#!/usr/bin/env python3
"""pdf-writer — weasyprint 기반 다국어(CJK) PDF 렌더러.

입력(HTML / Markdown / JSON / Text) → HTML → weasyprint → PDF.

설계 원칙
- 단일 엔진(weasyprint)으로 모든 입력을 처리한다. 스타일이 입혀진 HTML 리포트는
  풀 CSS를 그대로 충실히 렌더하고(html-report·html-slide 산출물의 디자인 보존),
  Markdown/JSON/Text는 HTML로 변환한 뒤 동일 경로로 렌더한다.
- 번들 Noto Sans CJK OTF를 @font-face로 임베딩해 한·중·일 글리프 깨짐을 방지한다.
  시스템에 "Noto Sans CJK KR"가 있으면 fontconfig가 자동 폴백하므로,
  HTML이 자체 폰트를 지정해도 CJK는 안전하게 표시된다.

사용:
    python3 render_pdf.py --in report.html  --out report.pdf
    python3 render_pdf.py --in report.md    --out report.pdf
    python3 render_pdf.py --in data.json     --out report.pdf
    echo "본문" | python3 render_pdf.py --out out.pdf      # stdin(Text)
"""
from __future__ import annotations

import argparse
import html as _html
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = SKILL_ROOT / "assets" / "fonts"

# 번들 Noto Sans CJK를 @font-face로 등록 (weight별). 파일이 없으면 시스템 폰트로 폴백.
def _font_face_css() -> str:
    weights = {300: "Light", 400: "Regular", 500: "Medium", 700: "Bold"}
    rules = []
    for weight, name in weights.items():
        otf = FONT_DIR / f"NotoSansCJK-{name}.otf"
        if otf.exists():
            rules.append(
                "@font-face{font-family:'Noto Sans CJK';"
                f"font-weight:{weight};font-style:normal;"
                f"src:url('file://{otf}');}}"
            )
    return "\n".join(rules)


# Markdown/JSON/Text 입력에만 적용하는 기본 문서 스타일.
# (이미 스타일이 입혀진 완성 HTML에는 적용하지 않고 그대로 렌더한다.)
BASE_CSS = """
@page { size: A4; margin: 20mm; }
html { font-family: 'Noto Sans CJK', 'Noto Sans CJK KR', 'Noto Sans KR', sans-serif;
       font-size: 11pt; line-height: 1.65; color: #1a1a1a; }
h1 { font-size: 20pt; font-weight: 700; margin: 0 0 12px; }
h2 { font-size: 15pt; font-weight: 700; margin: 22px 0 8px; border-bottom: 1px solid #e5e5e5; padding-bottom: 4px; }
h3 { font-size: 12.5pt; font-weight: 500; margin: 16px 0 6px; }
p, li { font-size: 11pt; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; }
th, td { border: 1px solid #d0d0d0; padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #f5f5f5; font-weight: 700; }
code { font-family: 'Noto Sans CJK', monospace; background: #f4f4f4; padding: 1px 4px; border-radius: 3px; }
img { max-width: 100%; }
"""


def _is_full_html(raw: str) -> bool:
    low = raw.lower()
    return "<html" in low or "<!doctype html" in low or "<body" in low


def md_to_html(text: str) -> str:
    """Markdown → HTML. python-markdown이 있으면 사용, 없으면 최소 폴백."""
    try:
        import markdown  # type: ignore

        body = markdown.markdown(
            text, extensions=["tables", "fenced_code", "toc", "sane_lists"]
        )
    except ImportError:
        # 의존성 없는 최소 폴백: 단락만 분리.
        paras = [f"<p>{_html.escape(p)}</p>" for p in text.split("\n\n") if p.strip()]
        body = "\n".join(paras)
    return f"<article>{body}</article>"


def json_to_html(obj: dict) -> str:
    """구조화 JSON → HTML (title/subtitle/author/date/sections[heading,body,table])."""
    parts = []
    if obj.get("title"):
        parts.append(f"<h1>{_html.escape(str(obj['title']))}</h1>")
    if obj.get("subtitle"):
        parts.append(f"<p style='font-size:13pt;color:#666'>{_html.escape(str(obj['subtitle']))}</p>")
    meta = " · ".join(str(obj[k]) for k in ("author", "date") if obj.get(k))
    if meta:
        parts.append(f"<p style='color:#888'>{_html.escape(meta)}</p>")
    for sec in obj.get("sections", []):
        level = max(1, min(3, int(sec.get("level", 2))))
        if sec.get("heading"):
            parts.append(f"<h{level}>{_html.escape(str(sec['heading']))}</h{level}>")
        if sec.get("body"):
            parts.append(md_to_html(str(sec["body"])))
        tbl = sec.get("table")
        if tbl and tbl.get("headers"):
            head = "".join(f"<th>{_html.escape(str(h))}</th>" for h in tbl["headers"])
            rows = "".join(
                "<tr>" + "".join(f"<td>{_html.escape(str(c))}</td>" for c in row) + "</tr>"
                for row in tbl.get("rows", [])
            )
            parts.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")
        img = sec.get("image")
        if img and img.get("path"):
            cap = f"<figcaption>{_html.escape(str(img.get('caption','')))}</figcaption>" if img.get("caption") else ""
            parts.append(f"<figure><img src='{_html.escape(str(img['path']))}'>{cap}</figure>")
    return f"<article>{''.join(parts)}</article>"


def text_to_html(text: str) -> str:
    paras = [f"<p>{_html.escape(p)}</p>" for p in text.split("\n\n") if p.strip()]
    return f"<article>{''.join(paras)}</article>"


def build_html(raw: str) -> tuple[str, bool]:
    """입력을 HTML로 변환. 반환: (html, is_styled_full_doc)."""
    stripped = raw.lstrip()
    if _is_full_html(raw):
        return raw, True  # 이미 완성된 스타일 HTML → 그대로 렌더
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return json_to_html(json.loads(raw)), False
        except json.JSONDecodeError:
            pass
    if "<h1" in raw.lower() or "<table" in raw.lower() or "<p>" in raw.lower():
        return f"<article>{raw}</article>", False  # HTML 조각
    # 마크다운 신호(#, **, |, -)가 있으면 markdown, 아니면 plain text
    if any(sig in raw for sig in ("# ", "## ", "**", "\n- ", "\n| ")):
        return md_to_html(raw), False
    return text_to_html(raw), False


def render(raw: str, out_path: str) -> None:
    try:
        from weasyprint import HTML, CSS  # type: ignore
    except ImportError:
        sys.exit(
            "weasyprint 미설치. 설치: pip install weasyprint\n"
            "(시스템 라이브러리 cairo/pango 필요 — 대부분의 Cowork 샌드박스에 기본 포함)"
        )

    body_html, is_full = build_html(raw)
    font_css = _font_face_css()

    if is_full:
        # 완성 HTML: 자체 CSS를 그대로 쓰되, CJK 폰트 폴백만 @font-face로 보강.
        stylesheets = [CSS(string=font_css)] if font_css else []
        HTML(string=body_html, base_url=str(Path.cwd())).write_pdf(out_path, stylesheets=stylesheets)
    else:
        doc = f"<!DOCTYPE html><html lang='ko'><head><meta charset='utf-8'></head><body>{body_html}</body></html>"
        stylesheets = [CSS(string=font_css + BASE_CSS)]
        HTML(string=doc, base_url=str(Path.cwd())).write_pdf(out_path, stylesheets=stylesheets)


def main() -> None:
    ap = argparse.ArgumentParser(description="weasyprint 기반 다국어 PDF 렌더러")
    ap.add_argument("--in", dest="inp", help="입력 파일 (.html/.md/.json/.txt). 생략 시 stdin")
    ap.add_argument("--out", required=True, help="출력 .pdf 경로")
    args = ap.parse_args()

    if args.inp:
        raw = Path(args.inp).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    render(raw, args.out)
    print(f"✅ PDF 생성 완료: {args.out}")


if __name__ == "__main__":
    main()
