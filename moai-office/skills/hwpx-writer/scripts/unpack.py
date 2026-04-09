"""HWPX 파일 언패킹 도구

HWPX 파일(ZIP 아카이브)을 디렉토리로 풀어서 XML 편집이 가능하게 합니다.

Usage:
    python unpack.py <hwpx_file> <output_dir>

Examples:
    python unpack.py document.hwpx unpacked/
"""

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom


def pretty_print_xml(xml_file: Path) -> None:
    """XML 파일을 들여쓰기하여 읽기 쉽게 정리합니다."""
    try:
        content = xml_file.read_text(encoding='utf-8')
        dom = minidom.parseString(content)
        pretty = dom.toprettyxml(indent='  ', encoding='utf-8')
        xml_file.write_bytes(pretty)
    except Exception:
        pass  # 바이너리 또는 파싱 불가 파일은 건너뜀


def unpack(input_file: str, output_directory: str) -> tuple[bool, str]:
    """HWPX 파일을 디렉토리로 언패킹합니다.

    Returns:
        (success, message)
    """
    input_path = Path(input_file)
    output_path = Path(output_directory)

    if not input_path.exists():
        return False, f"Error: {input_file} 파일이 존재하지 않습니다"

    if input_path.suffix.lower() != '.hwpx':
        return False, f"Error: {input_file}는 .hwpx 파일이 아닙니다"

    try:
        output_path.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(input_path, 'r') as zf:
            zf.extractall(output_path)

        # XML 파일 정리 (pretty print)
        xml_files = list(output_path.rglob('*.xml')) + list(output_path.rglob('*.hpf'))
        for xml_file in xml_files:
            pretty_print_xml(xml_file)

        file_count = sum(1 for _ in output_path.rglob('*') if _.is_file())
        xml_count = len(xml_files)

        return True, (
            f"Unpacked {input_file} → {output_directory}\n"
            f"  총 {file_count}개 파일 (XML {xml_count}개)"
        )

    except zipfile.BadZipFile:
        return False, f"Error: {input_file}는 유효한 HWPX(ZIP) 파일이 아닙니다"
    except Exception as e:
        return False, f"Error: 언패킹 실패 - {e}"


def main():
    parser = argparse.ArgumentParser(description="HWPX 파일을 디렉토리로 언패킹합니다")
    parser.add_argument("hwpx_file", help="HWPX 파일 경로")
    parser.add_argument("output_directory", help="출력 디렉토리 경로")
    args = parser.parse_args()

    success, message = unpack(args.hwpx_file, args.output_directory)
    print(message)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
