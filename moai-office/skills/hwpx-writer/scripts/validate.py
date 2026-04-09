"""HWPX 파일 유효성 검사 도구

HWPX 파일의 구조와 XML 유효성을 검사합니다.

Usage:
    python validate.py <hwpx_file>

Examples:
    python validate.py document.hwpx
    python validate.py output.hwpx --verbose
"""

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# 필수 파일 목록
REQUIRED_FILES = [
    'mimetype',
    'META-INF/manifest.xml',
    'Contents/content.hpf',
    'Contents/header.xml',
]

EXPECTED_MIMETYPE = 'application/hwp+zip'

NS = {
    'hp': 'http://www.hancom.co.kr/hwpml/2011/paragraph',
    'hs': 'http://www.hancom.co.kr/hwpml/2011/section',
    'hh': 'http://www.hancom.co.kr/hwpml/2011/head',
    'hc': 'http://www.hancom.co.kr/hwpml/2011/core',
}


class ValidationResult:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, msg: str):
        self.errors.append(f"[ERROR] {msg}")

    def add_warning(self, msg: str):
        self.warnings.append(f"[WARN]  {msg}")

    def add_info(self, msg: str):
        self.info.append(f"[INFO]  {msg}")

    def summary(self, verbose: bool = False) -> str:
        lines = []

        if self.errors:
            lines.append("=== Errors ===")
            lines.extend(self.errors)

        if self.warnings:
            lines.append("=== Warnings ===")
            lines.extend(self.warnings)

        if verbose and self.info:
            lines.append("=== Info ===")
            lines.extend(self.info)

        if self.is_valid:
            lines.append(f"\n✓ Validation PASSED ({len(self.warnings)} warnings)")
        else:
            lines.append(f"\n✗ Validation FAILED ({len(self.errors)} errors, {len(self.warnings)} warnings)")

        return '\n'.join(lines)


def validate_hwpx(hwpx_path: str, verbose: bool = False) -> ValidationResult:
    """HWPX 파일의 유효성을 검사합니다."""
    result = ValidationResult()
    path = Path(hwpx_path)

    # 1. 파일 존재 확인
    if not path.exists():
        result.add_error(f"파일이 존재하지 않습니다: {hwpx_path}")
        return result

    # 2. ZIP 아카이브 확인
    if not zipfile.is_zipfile(path):
        result.add_error(f"유효한 ZIP 아카이브가 아닙니다: {hwpx_path}")
        return result

    try:
        with zipfile.ZipFile(path, 'r') as zf:
            namelist = zf.namelist()

            # 3. 필수 파일 존재 확인
            for req in REQUIRED_FILES:
                if req in namelist:
                    result.add_info(f"필수 파일 존재: {req}")
                else:
                    result.add_error(f"필수 파일 누락: {req}")

            # 4. mimetype 확인
            if 'mimetype' in namelist:
                mimetype = zf.read('mimetype').decode('utf-8').strip()
                if mimetype == EXPECTED_MIMETYPE:
                    result.add_info(f"mimetype 정상: {mimetype}")
                else:
                    result.add_error(f"mimetype 불일치: '{mimetype}' (기대값: '{EXPECTED_MIMETYPE}')")

            # 5. 섹션 파일 확인
            sections = [n for n in namelist if n.startswith('Contents/section') and n.endswith('.xml')]
            if sections:
                result.add_info(f"섹션 파일 {len(sections)}개: {', '.join(sections)}")
            else:
                result.add_error("섹션 파일(Contents/sectionN.xml)이 없습니다")

            # 6. 각 XML 파일 파싱 확인
            xml_files = [n for n in namelist if n.endswith('.xml') or n.endswith('.hpf')]
            parse_ok = 0
            parse_fail = 0

            for xml_file in xml_files:
                try:
                    with zf.open(xml_file) as f:
                        ET.parse(f)
                    parse_ok += 1
                except ET.ParseError as e:
                    result.add_error(f"XML 파싱 오류 - {xml_file}: {e}")
                    parse_fail += 1

            result.add_info(f"XML 파싱 결과: {parse_ok}개 성공, {parse_fail}개 실패")

            # 7. 섹션 내 텍스트 존재 확인
            total_paragraphs = 0
            total_text_length = 0
            for sec_file in sections:
                try:
                    with zf.open(sec_file) as f:
                        tree = ET.parse(f)
                        root = tree.getroot()

                    p_count = 0
                    for t_elem in root.iter(f'{{{NS["hp"]}}}t'):
                        if t_elem.text:
                            total_text_length += len(t_elem.text)
                    for p_elem in root.iter(f'{{{NS["hp"]}}}p'):
                        p_count += 1
                        total_paragraphs += 1

                    result.add_info(f"{sec_file}: {p_count}개 단락")
                except Exception as e:
                    result.add_warning(f"{sec_file} 분석 실패: {e}")

            result.add_info(f"총 {total_paragraphs}개 단락, 텍스트 {total_text_length}자")

            if total_paragraphs == 0:
                result.add_warning("문서에 텍스트 단락이 없습니다")

            # 8. content.hpf와 섹션 매칭 확인
            if 'Contents/content.hpf' in namelist:
                try:
                    with zf.open('Contents/content.hpf') as f:
                        hpf_tree = ET.parse(f)
                        hpf_root = hpf_tree.getroot()

                    # section href 추출
                    hpf_sections = []
                    for elem in hpf_root.iter():
                        if 'section' in elem.tag.lower():
                            href = elem.get('href', '')
                            if href:
                                hpf_sections.append(href)

                    for href in hpf_sections:
                        if href in namelist:
                            result.add_info(f"content.hpf 참조 일치: {href}")
                        else:
                            result.add_error(f"content.hpf에서 참조하는 파일 누락: {href}")

                except Exception as e:
                    result.add_warning(f"content.hpf 분석 실패: {e}")

            # 9. 전체 파일 목록
            result.add_info(f"전체 파일 수: {len(namelist)}")

    except Exception as e:
        result.add_error(f"파일 처리 오류: {e}")

    return result


def validate_unpacked(unpacked_dir: str, verbose: bool = False) -> ValidationResult:
    """언패킹된 HWPX 디렉토리의 유효성을 검사합니다."""
    result = ValidationResult()
    dir_path = Path(unpacked_dir)

    if not dir_path.is_dir():
        result.add_error(f"디렉토리가 아닙니다: {unpacked_dir}")
        return result

    # 필수 파일 확인
    for req in REQUIRED_FILES:
        req_path = dir_path / req
        if req_path.exists():
            result.add_info(f"필수 파일 존재: {req}")
        else:
            result.add_error(f"필수 파일 누락: {req}")

    # mimetype 확인
    mimetype_path = dir_path / 'mimetype'
    if mimetype_path.exists():
        mimetype = mimetype_path.read_text(encoding='utf-8').strip()
        if mimetype != EXPECTED_MIMETYPE:
            result.add_error(f"mimetype 불일치: '{mimetype}'")

    # XML 파일 파싱 확인
    xml_files = list(dir_path.rglob('*.xml')) + list(dir_path.rglob('*.hpf'))
    for xml_file in xml_files:
        try:
            ET.parse(xml_file)
        except ET.ParseError as e:
            result.add_error(f"XML 파싱 오류 - {xml_file.relative_to(dir_path)}: {e}")

    result.add_info(f"XML 파일 {len(xml_files)}개 검사 완료")

    return result


def main():
    parser = argparse.ArgumentParser(description="HWPX 파일 유효성 검사")
    parser.add_argument(
        "path",
        help="HWPX 파일 또는 언패킹된 디렉토리 경로"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="상세 정보 출력"
    )
    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file() and path.suffix.lower() == '.hwpx':
        result = validate_hwpx(args.path, verbose=args.verbose)
    elif path.is_dir():
        result = validate_unpacked(args.path, verbose=args.verbose)
    else:
        print(f"Error: {args.path}는 .hwpx 파일 또는 디렉토리가 아닙니다", file=sys.stderr)
        sys.exit(1)

    print(result.summary(verbose=args.verbose))
    sys.exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
