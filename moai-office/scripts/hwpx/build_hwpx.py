"""
HWPX 문서 생성 스크립트

OWPML(KS X 6101) 표준 기반 HWPX 파일을 생성합니다.
HWPX = ZIP 아카이브 (XML + 리소스 파일 포함)

사용법:
    python build_hwpx.py --template base --output output.hwpx --data data.json

의존성:
    pip install python-hwpx lxml
"""

import argparse
import json
import os
import sys
from pathlib import Path

# HWPX 기본 구조
HWPX_STRUCTURE = {
    "Contents": {
        "content.hpf": None,  # OPF 매니페스트
        "header.xml": None,   # 문서 헤더
        "section0.xml": None, # 본문 섹션
    },
    "META-INF": {
        "container.xml": None,  # OCF 컨테이너
        "manifest.xml": None,   # 매니페스트
    },
    "mimetype": "application/hwp+zip",
    "version.xml": None,
}

# 템플릿 경로
TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "hwpx"

TEMPLATES = {
    "base": "base.md",
    "gonmun": "gonmun.md",
    "report": "report.md",
    "minutes": "minutes.md",
    "proposal": "proposal.md",
}


def load_template_spec(template_name: str) -> str:
    """템플릿 스펙 파일을 로드합니다."""
    if template_name not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        print(f"오류: '{template_name}' 템플릿을 찾을 수 없습니다.")
        print(f"사용 가능한 템플릿: {available}")
        sys.exit(1)

    spec_path = TEMPLATE_DIR / TEMPLATES[template_name]
    if not spec_path.exists():
        print(f"오류: 템플릿 스펙 파일이 없습니다: {spec_path}")
        sys.exit(1)

    return spec_path.read_text(encoding="utf-8")


def create_section_xml(data: dict, template_name: str) -> str:
    """본문 섹션 XML을 생성합니다."""
    title = data.get("title", "제목 없음")
    body_paragraphs = data.get("paragraphs", [])

    paragraphs_xml = ""
    for para in body_paragraphs:
        text = para.get("text", "")
        style = para.get("style", "본문")
        paragraphs_xml += f"""
        <hp:p>
            <hp:run>
                <hp:secPr>
                    <hp:style val="{style}"/>
                </hp:secPr>
                <hp:t>{text}</hp:t>
            </hp:run>
        </hp:p>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<hp:sec xmlns:hp="http://www.hancom.co.kr/hwpml/2016/HwpDoc">
    <hp:p>
        <hp:run>
            <hp:secPr><hp:style val="제목"/></hp:secPr>
            <hp:t>{title}</hp:t>
        </hp:run>
    </hp:p>
    {paragraphs_xml}
</hp:sec>"""


def build_hwpx(template_name: str, data: dict, output_path: str) -> None:
    """HWPX 파일을 생성합니다."""
    import zipfile

    spec = load_template_spec(template_name)

    section_xml = create_section_xml(data, template_name)

    header_xml = """<?xml version="1.0" encoding="UTF-8"?>
<hp:head xmlns:hp="http://www.hancom.co.kr/hwpml/2016/HwpDoc">
    <hp:docSetting>
        <hp:paperSize width="59528" height="84188"/>
        <hp:paperMargin left="8504" right="8504" top="5668" bottom="4252"
                        header="4252" footer="4252" gutter="0"/>
    </hp:docSetting>
    <hp:fontfaces>
        <hp:fontface lang="Korean" name="맑은 고딕"/>
        <hp:fontface lang="Latin" name="Pretendard"/>
    </hp:fontfaces>
</hp:head>"""

    container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="Contents/content.hpf" media-type="application/hwp+zip"/>
    </rootfiles>
</container>"""

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mimetype", "application/hwp+zip")
        zf.writestr("META-INF/container.xml", container_xml)
        zf.writestr("Contents/header.xml", header_xml)
        zf.writestr("Contents/section0.xml", section_xml)

    print(f"HWPX 생성 완료: {output_path}")
    print(f"템플릿: {template_name}")
    print(f"파일 크기: {os.path.getsize(output_path):,} bytes")


def main():
    parser = argparse.ArgumentParser(description="HWPX 문서 생성기")
    parser.add_argument("--template", default="base", choices=TEMPLATES.keys(),
                        help="사용할 템플릿 (기본: base)")
    parser.add_argument("--output", default="output.hwpx",
                        help="출력 파일 경로 (기본: output.hwpx)")
    parser.add_argument("--data", default=None,
                        help="입력 데이터 JSON 파일 경로")
    parser.add_argument("--title", default=None,
                        help="문서 제목 (--data 없을 때 사용)")

    args = parser.parse_args()

    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "title": args.title or "새 문서",
            "paragraphs": [
                {"text": "본문 내용을 입력하세요.", "style": "본문"}
            ],
        }

    build_hwpx(args.template, data, args.output)


if __name__ == "__main__":
    main()
