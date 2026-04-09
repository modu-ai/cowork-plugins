"""HWPX 파일 생성 도구

텍스트 내용으로 새 HWPX 파일을 생성합니다.

Usage:
    python create_hwpx.py --output <output.hwpx> --title "제목" --body "본문"
    python create_hwpx.py --output <output.hwpx> --paragraphs "단락1" "단락2" "단락3"
    python create_hwpx.py --output <output.hwpx> --input-file content.txt

Examples:
    python create_hwpx.py --output report.hwpx --title "월간 보고서" --body "내용입니다."
    python create_hwpx.py --output letter.hwpx --paragraphs "안녕하세요." "본문입니다." "감사합니다."
    python create_hwpx.py --output doc.hwpx --input-file paragraphs.txt
"""

import argparse
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


# OWPML 네임스페이스
HP = 'http://www.hancom.co.kr/hwpml/2011/paragraph'
HS = 'http://www.hancom.co.kr/hwpml/2011/section'
HH = 'http://www.hancom.co.kr/hwpml/2011/head'
HC = 'http://www.hancom.co.kr/hwpml/2011/core'


def build_paragraph_xml(text: str) -> str:
    """단일 단락의 XML을 생성합니다."""
    safe_text = escape(text)
    return f'''    <hp:p xmlns:hp="{HP}">
      <hp:run>
        <hp:t>{safe_text}</hp:t>
      </hp:run>
    </hp:p>'''


def create_hwpx(
    output_path: str,
    paragraphs: list[str],
    font_hangul: str = "함초롬돋움",
    font_latin: str = "함초롬돋움",
    font_size: int = 1000,
) -> tuple[bool, str]:
    """HWPX 파일을 생성합니다.

    Args:
        output_path: 출력 파일 경로
        paragraphs: 단락 텍스트 목록
        font_hangul: 한글 기본 글꼴명
        font_latin: 영문 기본 글꼴명
        font_size: 글꼴 크기 (단위: 1/100 pt, 기본 1000 = 10pt)

    Returns:
        (success, message)
    """
    if not paragraphs:
        return False, "Error: 최소 한 개의 단락이 필요합니다"

    out = Path(output_path)
    if out.suffix.lower() != '.hwpx':
        return False, "Error: 출력 파일은 .hwpx 확장자여야 합니다"

    # 단락 XML 생성
    para_xml = '\n'.join(build_paragraph_xml(p) for p in paragraphs)

    mimetype = 'application/hwp+zip'

    version_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<hv:HWPVersion xmlns:hv="urn:hancom:office:hwpml:version"
  major="1" minor="0" micro="0" buildNumber="0"/>'''

    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<odf:manifest xmlns:odf="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
  <odf:file-entry odf:full-path="/" odf:media-type="application/hwp+zip"/>
  <odf:file-entry odf:full-path="version.xml" odf:media-type="text/xml"/>
  <odf:file-entry odf:full-path="Contents/content.hpf" odf:media-type="text/xml"/>
  <odf:file-entry odf:full-path="Contents/header.xml" odf:media-type="text/xml"/>
  <odf:file-entry odf:full-path="Contents/section0.xml" odf:media-type="text/xml"/>
</odf:manifest>'''

    content_hpf = f'''<?xml version="1.0" encoding="UTF-8"?>
<hc:package xmlns:hc="{HC}">
  <hc:head href="Contents/header.xml"/>
  <hc:body>
    <hc:section href="Contents/section0.xml"/>
  </hc:body>
</hc:package>'''

    header_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<hh:head xmlns:hh="{HH}" xmlns:hp="{HP}">
  <hh:fontfaces>
    <hh:fontface lang="HANGUL">
      <hp:font id="0" face="{escape(font_hangul)}" type="TTF"/>
    </hh:fontface>
    <hh:fontface lang="LATIN">
      <hp:font id="0" face="{escape(font_latin)}" type="TTF"/>
    </hh:fontface>
  </hh:fontfaces>
  <hh:charProperties>
    <hh:charPr id="0">
      <hp:fontRef hangul="0" latin="0"/>
      <hp:fontSize hangul="{font_size}" latin="{font_size}"/>
    </hh:charPr>
  </hh:charProperties>
</hh:head>'''

    section_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="{HS}" xmlns:hp="{HP}">
{para_xml}
</hs:sec>'''

    try:
        out.parent.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
            # mimetype은 첫 번째, 비압축
            zf.writestr('mimetype', mimetype, compress_type=zipfile.ZIP_STORED)
            zf.writestr('version.xml', version_xml)
            zf.writestr('META-INF/manifest.xml', manifest_xml)
            zf.writestr('Contents/content.hpf', content_hpf)
            zf.writestr('Contents/header.xml', header_xml)
            zf.writestr('Contents/section0.xml', section_xml)

        size_kb = out.stat().st_size / 1024
        return True, (
            f"Created {output_path}\n"
            f"  {len(paragraphs)}개 단락, {size_kb:.1f} KB"
        )

    except Exception as e:
        return False, f"Error: 파일 생성 실패 - {e}"


def main():
    parser = argparse.ArgumentParser(description="새 HWPX 파일을 생성합니다")
    parser.add_argument("--output", "-o", required=True, help="출력 HWPX 파일 경로")
    parser.add_argument("--title", help="문서 제목 (첫 번째 단락)")
    parser.add_argument("--body", help="본문 텍스트")
    parser.add_argument("--paragraphs", nargs="+", help="단락 목록")
    parser.add_argument("--input-file", help="단락이 줄로 구분된 텍스트 파일")
    parser.add_argument("--font", default="함초롬돋움", help="기본 글꼴 (기본: 함초롬돋움)")
    parser.add_argument("--font-size", type=int, default=1000, help="글꼴 크기 (1/100 pt, 기본: 1000=10pt)")

    args = parser.parse_args()

    # 단락 수집
    paragraphs = []

    if args.title:
        paragraphs.append(args.title)

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

    if not paragraphs:
        print("Error: --title, --body, --paragraphs, --input-file 중 하나 이상 지정하세요", file=sys.stderr)
        sys.exit(1)

    success, message = create_hwpx(
        args.output,
        paragraphs,
        font_hangul=args.font,
        font_latin=args.font,
        font_size=args.font_size,
    )
    print(message)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
