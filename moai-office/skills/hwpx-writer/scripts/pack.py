"""HWPX 파일 패킹 도구

언패킹된 디렉토리를 다시 HWPX 파일로 패킹합니다.

Usage:
    python pack.py <input_dir> <output_file>

Examples:
    python pack.py unpacked/ output.hwpx
"""

import argparse
import sys
import zipfile
from pathlib import Path
from xml.dom import minidom


def condense_xml(xml_file: Path) -> None:
    """XML 파일에서 불필요한 공백을 제거하여 크기를 줄입니다."""
    try:
        content = xml_file.read_text(encoding='utf-8')
        dom = minidom.parseString(content)

        for element in dom.getElementsByTagName('*'):
            # 텍스트 요소(hp:t)는 공백 보존
            if element.tagName.endswith(':t') or element.localName == 't':
                continue
            for child in list(element.childNodes):
                if (child.nodeType == child.TEXT_NODE
                        and child.nodeValue
                        and child.nodeValue.strip() == ''):
                    element.removeChild(child)
                elif child.nodeType == child.COMMENT_NODE:
                    element.removeChild(child)

        xml_file.write_bytes(dom.toxml(encoding='UTF-8'))
    except Exception as e:
        print(f"Warning: {xml_file.name} 압축 실패 - {e}", file=sys.stderr)


def pack(input_directory: str, output_file: str) -> tuple[bool, str]:
    """언패킹된 디렉토리를 HWPX 파일로 패킹합니다.

    Returns:
        (success, message)
    """
    input_dir = Path(input_directory)
    output_path = Path(output_file)

    if not input_dir.is_dir():
        return False, f"Error: {input_directory}는 디렉토리가 아닙니다"

    if output_path.suffix.lower() != '.hwpx':
        return False, f"Error: 출력 파일은 .hwpx 확장자여야 합니다"

    # 필수 파일 확인
    mimetype_path = input_dir / 'mimetype'
    if not mimetype_path.exists():
        return False, f"Error: {input_directory}/mimetype 파일이 없습니다. 유효한 HWPX 구조가 아닙니다."

    contents_dir = input_dir / 'Contents'
    if not contents_dir.is_dir():
        return False, f"Error: {input_directory}/Contents 디렉토리가 없습니다."

    try:
        # XML 파일 압축 (공백 제거)
        xml_files = list(input_dir.rglob('*.xml')) + list(input_dir.rglob('*.hpf'))
        for xml_file in xml_files:
            condense_xml(xml_file)

        # ZIP 생성
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # mimetype은 반드시 첫 번째, 비압축으로
            zf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

            for f in sorted(input_dir.rglob('*')):
                if f.is_file() and f.name != 'mimetype':
                    arcname = str(f.relative_to(input_dir))
                    zf.write(f, arcname)

        file_count = sum(1 for _ in input_dir.rglob('*') if _.is_file())
        size_kb = output_path.stat().st_size / 1024

        return True, (
            f"Packed {input_directory} → {output_file}\n"
            f"  {file_count}개 파일, {size_kb:.1f} KB"
        )

    except Exception as e:
        return False, f"Error: 패킹 실패 - {e}"


def main():
    parser = argparse.ArgumentParser(description="언패킹된 디렉토리를 HWPX 파일로 패킹합니다")
    parser.add_argument("input_directory", help="언패킹된 HWPX 디렉토리")
    parser.add_argument("output_file", help="출력 HWPX 파일 경로")
    args = parser.parse_args()

    success, message = pack(args.input_directory, args.output_file)
    print(message)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
