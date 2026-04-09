"""HWPX 텍스트 추출 도구

HWPX 파일에서 텍스트를 추출합니다.

Usage:
    python extract_text.py <hwpx_file> [options]

Examples:
    python extract_text.py document.hwpx
    python extract_text.py document.hwpx --section 0
    python extract_text.py document.hwpx --format json
"""

import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# OWPML 네임스페이스
NS = {
    'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph',
    'hs': 'http://www.hancom.co.kr/hwpml/2011/section',
    'hh': 'http://www.hancom.co.kr/hwpml/2011/head',
    'hc': 'http://www.hancom.co.kr/hwpml/2011/core',
}

HP_T = f'{{{NS["hp"]}}}t'
HP_P = f'{{{NS["hp"]}}}p'


def list_sections(hwpx_path: str) -> list[str]:
    """HWPX 파일 내 섹션 파일 목록을 반환합니다."""
    sections = []
    with zipfile.ZipFile(hwpx_path, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('Contents/section') and name.endswith('.xml'):
                sections.append(name)
    sections.sort()
    return sections


def extract_from_section(hwpx_path: str, section_file: str) -> list[str]:
    """특정 섹션에서 단락별 텍스트를 추출합니다."""
    paragraphs = []
    with zipfile.ZipFile(hwpx_path, 'r') as zf:
        with zf.open(section_file) as f:
            tree = ET.parse(f)
            root = tree.getroot()

    for p_elem in root.iter(HP_P):
        para_text = []
        for t_elem in p_elem.iter(HP_T):
            if t_elem.text:
                para_text.append(t_elem.text)
        if para_text:
            paragraphs.append(''.join(para_text))

    return paragraphs


def extract_all(hwpx_path: str, section_index: int | None = None) -> dict:
    """HWPX 파일에서 전체 또는 특정 섹션의 텍스트를 추출합니다."""
    sections = list_sections(hwpx_path)

    if section_index is not None:
        target = f'Contents/section{section_index}.xml'
        if target not in sections:
            return {"error": f"Section {section_index} not found. Available: {sections}"}
        sections = [target]

    result = {
        "file": hwpx_path,
        "sections": []
    }

    for sec_file in sections:
        paragraphs = extract_from_section(hwpx_path, sec_file)
        result["sections"].append({
            "file": sec_file,
            "paragraphs": paragraphs
        })

    return result


def main():
    parser = argparse.ArgumentParser(description="HWPX 파일에서 텍스트를 추출합니다")
    parser.add_argument("hwpx_file", help="HWPX 파일 경로")
    parser.add_argument(
        "--section", type=int, default=None,
        help="특정 섹션 번호만 추출 (예: 0, 1, 2)"
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="출력 형식 (기본: text)"
    )
    args = parser.parse_args()

    path = Path(args.hwpx_file)
    if not path.exists():
        print(f"Error: {args.hwpx_file} 파일이 존재하지 않습니다.", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() != '.hwpx':
        print(f"Error: {args.hwpx_file}는 .hwpx 파일이 아닙니다.", file=sys.stderr)
        sys.exit(1)

    result = extract_all(args.hwpx_file, section_index=args.section)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for sec in result["sections"]:
            print(f"--- {sec['file']} ---")
            for para in sec["paragraphs"]:
                print(para)
            print()


if __name__ == "__main__":
    main()
