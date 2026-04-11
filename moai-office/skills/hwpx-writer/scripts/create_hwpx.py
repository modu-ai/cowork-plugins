"""HWPX 파일 생성 도구 (python-hwpx 기반)

python-hwpx 라이브러리를 사용하여 유효한 HWPX 파일을 생성합니다.
라이브러리가 없으면 설치 안내를 출력합니다.

의존성: pip install python-hwpx
GitHub: https://github.com/airmang/python-hwpx

Usage:
    python create_hwpx.py --output <output.hwpx> --title "제목" --body "본문"
    python create_hwpx.py --output <output.hwpx> --paragraphs "단락1" "단락2"
    python create_hwpx.py --output <output.hwpx> --input-file content.txt

Examples:
    python create_hwpx.py --output report.hwpx --title "월간 보고서" --body "내용입니다."
    python create_hwpx.py --output letter.hwpx --paragraphs "안녕하세요." "감사합니다."
"""

import argparse
import sys
from pathlib import Path

# python-hwpx 의존성 확인 + lxml 호환 패치
try:
    from hwpx import HwpxDocument
    # lxml 호환 패치: ensure_run_style()에서 ET.SubElement 타입 불일치 수정
    try:
        import lxml.etree as _lxml_ET
        import hwpx.oxml.document as _oxdoc
        _oxdoc.ET = _lxml_ET
    except ImportError:
        pass
    HAS_HWPX = True
except ImportError:
    HAS_HWPX = False


def create_hwpx_with_library(
    output_path: str,
    paragraphs: list[str],
    title: str = "",
) -> tuple[bool, str]:
    """python-hwpx 라이브러리로 유효한 HWPX 파일을 생성합니다."""
    out = Path(output_path)
    if out.suffix.lower() != '.hwpx':
        return False, "Error: 출력 파일은 .hwpx 확장자여야 합니다"

    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        doc = HwpxDocument.new()

        if title:
            doc.add_paragraph(title)
        for p in paragraphs:
            doc.add_paragraph(p)

        doc.save_to_path(str(out))

        size_kb = out.stat().st_size / 1024
        total = len(paragraphs) + (1 if title else 0)
        return True, f"Created {output_path}\n  {total}개 단락, {size_kb:.1f} KB (python-hwpx)"

    except Exception as e:
        return False, f"Error: HWPX 생성 실패 - {e}"


def create_hwpx_fallback(
    output_path: str,
    paragraphs: list[str],
    title: str = "",
    font: str = "함초롬돋움",
    font_size: int = 1000,
) -> tuple[bool, str]:
    """python-hwpx 미설치 시 내장 XML 템플릿으로 HWPX를 생성합니다.

    주의: 이 방식은 일부 한글 버전에서 호환성 문제가 발생할 수 있습니다.
    python-hwpx 설치를 강력히 권장합니다: pip install python-hwpx
    """
    import zipfile
    from xml.sax.saxutils import escape

    out = Path(output_path)
    if out.suffix.lower() != '.hwpx':
        return False, "Error: 출력 파일은 .hwpx 확장자여야 합니다"

    HP = 'http://www.hancom.co.kr/hwpml/2011/paragraph'
    HS = 'http://www.hancom.co.kr/hwpml/2011/section'
    HH = 'http://www.hancom.co.kr/hwpml/2011/head'
    HC = 'http://www.hancom.co.kr/hwpml/2011/core'

    def para(text, pr_id="0", char_id="0"):
        return f'    <hp:p paraPrIDRef="{pr_id}" styleIDRef="0"><hp:run charPrIDRef="{char_id}"><hp:t>{escape(text)}</hp:t></hp:run></hp:p>'

    parts = []
    if title:
        parts.append(para(title, "1", "1"))
    for p in paragraphs:
        parts.append(para(p))

    files = {
        'mimetype': 'application/hwp+zip',
        'version.xml': '<?xml version="1.0" encoding="UTF-8"?>\n<hv:HWPVersion xmlns:hv="urn:hancom:office:hwpml:version" major="1" minor="1" micro="0" buildNumber="0"/>',
        'META-INF/manifest.xml': f'<?xml version="1.0" encoding="UTF-8"?>\n<odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">\n  <odf:file-entry odf:full-path="/" odf:media-type="application/hwp+zip"/>\n  <odf:file-entry odf:full-path="version.xml" odf:media-type="text/xml"/>\n  <odf:file-entry odf:full-path="Contents/content.hpf" odf:media-type="text/xml"/>\n  <odf:file-entry odf:full-path="Contents/header.xml" odf:media-type="text/xml"/>\n  <odf:file-entry odf:full-path="Contents/section0.xml" odf:media-type="text/xml"/>\n</odf:manifest>',
        'Contents/content.hpf': f'<?xml version="1.0" encoding="UTF-8"?>\n<hc:package xmlns:hc="{HC}"><hc:head href="Contents/header.xml"/><hc:body><hc:section href="Contents/section0.xml"/></hc:body></hc:package>',
        'Contents/header.xml': f'''<?xml version="1.0" encoding="UTF-8"?>
<hh:head xmlns:hh="{HH}" xmlns:hp="{HP}">
  <hh:beginNum page="1" footnote="1" endnote="1"/>
  <hh:refList>
    <hh:fontfaces>
      <hh:fontface lang="HANGUL"><hp:font id="0" face="{escape(font)}" type="TTF"/></hh:fontface>
      <hh:fontface lang="LATIN"><hp:font id="0" face="{escape(font)}" type="TTF"/></hh:fontface>
      <hh:fontface lang="HANJA"><hp:font id="0" face="{escape(font)}" type="TTF"/></hh:fontface>
    </hh:fontfaces>
    <hh:borderFills>
      <hh:borderFill id="1">
        <hh:slash type="NONE"/><hh:backSlash type="NONE"/>
        <hh:leftBorder type="NONE" width="0.1mm" color="#000000"/>
        <hh:rightBorder type="NONE" width="0.1mm" color="#000000"/>
        <hh:topBorder type="NONE" width="0.1mm" color="#000000"/>
        <hh:bottomBorder type="NONE" width="0.1mm" color="#000000"/>
      </hh:borderFill>
    </hh:borderFills>
    <hh:charProperties>
      <hh:charPr id="0" height="{font_size}" textColor="#000000">
        <hp:fontRef hangul="0" latin="0" hanja="0"/>
        <hp:ratio hangul="100" latin="100" hanja="100"/>
        <hp:spacing hangul="0" latin="0" hanja="0"/>
        <hp:relSz hangul="100" latin="100" hanja="100"/>
        <hp:offset hangul="0" latin="0" hanja="0"/>
      </hh:charPr>
      <hh:charPr id="1" height="1600" textColor="#000000">
        <hp:fontRef hangul="0" latin="0" hanja="0"/>
        <hp:ratio hangul="100" latin="100" hanja="100"/>
        <hp:spacing hangul="0" latin="0" hanja="0"/>
        <hp:relSz hangul="100" latin="100" hanja="100"/>
        <hp:offset hangul="0" latin="0" hanja="0"/>
        <hp:bold value="true"/>
      </hh:charPr>
    </hh:charProperties>
    <hh:tabProperties><hh:tabPr id="0" autoTabLeft="0" autoTabRight="0"/></hh:tabProperties>
    <hh:paraProperties>
      <hh:paraPr id="0" align="BOTH"><hp:margin indent="0" left="0" right="0"/><hp:spacing lineSpacing="160" before="0" after="0" lineSpacingType="PERCENT"/></hh:paraPr>
      <hh:paraPr id="1" align="CENTER"><hp:margin indent="0" left="0" right="0"/><hp:spacing lineSpacing="160" before="0" after="200" lineSpacingType="PERCENT"/></hh:paraPr>
    </hh:paraProperties>
    <hh:styles><hh:style id="0" type="PARA" name="Normal" paraPrIDRef="0" charPrIDRef="0"/></hh:styles>
  </hh:refList>
</hh:head>''',
        'Contents/section0.xml': f'''<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="{HS}" xmlns:hp="{HP}">
  <hp:secPr textDirection="HORIZONTAL" spaceColumns="1134">
    <hp:pageSize width="59528" height="84188"/>
    <hp:pageMar left="4252" right="4252" top="5669" bottom="4252" header="4252" footer="4252"/>
  </hp:secPr>
{chr(10).join(parts)}
</hs:sec>'''
    }

    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('mimetype', files['mimetype'], compress_type=zipfile.ZIP_STORED)
            for name, content in files.items():
                if name != 'mimetype':
                    zf.writestr(name, content)

        size_kb = out.stat().st_size / 1024
        total = len(paragraphs) + (1 if title else 0)
        return True, (
            f"Created {output_path}\n"
            f"  {total}개 단락, {size_kb:.1f} KB (fallback 모드)\n"
            f"  [권장] pip install python-hwpx 설치 시 더 나은 호환성 제공"
        )
    except Exception as e:
        return False, f"Error: 파일 생성 실패 - {e}"


def create_hwpx(
    output_path: str,
    paragraphs: list[str],
    title: str = "",
    font: str = "함초롬돋움",
    font_size: int = 1000,
) -> tuple[bool, str]:
    """HWPX 파일을 생성합니다. python-hwpx 우선, 없으면 내장 폴백."""
    if HAS_HWPX:
        return create_hwpx_with_library(output_path, paragraphs, title)
    else:
        print("[참고] python-hwpx 미설치. 내장 폴백 모드로 생성합니다.", file=sys.stderr)
        print("[권장] pip install python-hwpx", file=sys.stderr)
        return create_hwpx_fallback(output_path, paragraphs, title, font, font_size)


def main():
    parser = argparse.ArgumentParser(description="HWPX 파일을 생성합니다 (python-hwpx 기반)")
    parser.add_argument("--output", "-o", required=True, help="출력 HWPX 파일 경로")
    parser.add_argument("--title", help="문서 제목")
    parser.add_argument("--body", help="본문 텍스트")
    parser.add_argument("--paragraphs", nargs="+", help="단락 목록")
    parser.add_argument("--input-file", help="단락이 줄로 구분된 텍스트 파일")
    parser.add_argument("--font", default="함초롬돋움", help="기본 글꼴 (기본: 함초롬돋움)")
    parser.add_argument("--font-size", type=int, default=1000,
                        help="글꼴 크기 (1/100 pt, 기본: 1000=10pt)")

    args = parser.parse_args()

    paragraphs = []
    if args.body:
        paragraphs.append(args.body)
    if args.paragraphs:
        paragraphs.extend(args.paragraphs)
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        paragraphs.append(line)
        except FileNotFoundError:
            print(f"Error: {args.input_file} 파일을 찾을 수 없습니다", file=sys.stderr)
            sys.exit(1)

    if not paragraphs and not args.title:
        print("Error: --title, --body, --paragraphs, --input-file 중 하나 이상 지정하세요",
              file=sys.stderr)
        sys.exit(1)

    success, message = create_hwpx(
        args.output,
        paragraphs,
        title=args.title or "",
        font=args.font,
        font_size=args.font_size,
    )
    print(message)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
