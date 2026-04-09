"""레거시 바이너리 HWP(.hwp) 파일 텍스트 추출 도구

HWP 5.x 바이너리 형식 파일에서 텍스트를 추출합니다.
OLE2 Compound Document 구조를 파싱하여 BodyText 스트림에서 단락 텍스트를 추출합니다.

의존성: pip install olefile --break-system-packages

Usage:
    python extract_hwp.py <hwp_file> [options]

Examples:
    python extract_hwp.py document.hwp
    python extract_hwp.py document.hwp --format json
    python extract_hwp.py document.hwp --output extracted.txt
"""

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

try:
    import olefile
except ImportError:
    print("Error: olefile 패키지가 필요합니다. 설치: pip install olefile --break-system-packages", file=sys.stderr)
    sys.exit(1)


def extract_text_from_hwp(hwp_path: str) -> dict:
    """HWP 바이너리 파일에서 텍스트를 추출합니다.

    Args:
        hwp_path: HWP 파일 경로

    Returns:
        {"file": str, "paragraphs": list[str], "preview": str|None}
    """
    path = Path(hwp_path)
    if not path.exists():
        return {"error": f"파일이 존재하지 않습니다: {hwp_path}"}

    if not olefile.isOleFile(str(path)):
        return {"error": f"유효한 HWP(OLE2) 파일이 아닙니다: {hwp_path}"}

    ole = olefile.OleFileIO(str(path))

    result = {
        "file": hwp_path,
        "paragraphs": [],
        "preview": None,
    }

    try:
        # 압축 여부 확인
        file_header = ole.openstream("FileHeader").read()
        is_compressed = bool(file_header[36] & 1)

        # PrvText (미리보기 텍스트) 추출 시도
        try:
            prv_data = ole.openstream("PrvText").read()
            result["preview"] = prv_data.decode('utf-16-le', errors='replace').strip('\x00').strip()
        except Exception:
            pass

        # BodyText 스트림에서 텍스트 추출
        text_parts = []
        for stream in ole.listdir():
            stream_path = "/".join(stream)
            if not stream_path.startswith("BodyText/"):
                continue

            data = ole.openstream(stream_path).read()
            if is_compressed:
                try:
                    data = zlib.decompress(data, -15)
                except Exception:
                    pass

            # HWP 레코드 파싱
            i = 0
            while i < len(data) - 4:
                header = struct.unpack_from('<I', data, i)[0]
                tag_id = header & 0x3FF
                size = (header >> 20) & 0xFFF

                if size == 0xFFF:
                    if i + 4 < len(data) - 4:
                        size = struct.unpack_from('<I', data, i + 4)[0]
                        i += 8
                    else:
                        break
                else:
                    i += 4

                if i + size > len(data):
                    break

                # HWPTAG_PARA_TEXT = 67
                if tag_id == 67:
                    record_data = data[i:i + size]
                    text = _extract_para_text(record_data)
                    if text.strip():
                        text_parts.append(text.strip())

                i += size

        result["paragraphs"] = text_parts

    finally:
        ole.close()

    return result


def _extract_para_text(record_data: bytes) -> str:
    """HWP 단락 레코드에서 UTF-16LE 텍스트를 추출합니다."""
    text = ""
    j = 0
    while j < len(record_data) - 1:
        char_code = struct.unpack_from('<H', record_data, j)[0]
        if char_code == 0:
            break
        elif char_code < 32:
            # 확장 컨트롤 문자 (16바이트 차지)
            if char_code in (1, 2, 3, 11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23):
                j += 16
                continue
            elif char_code == 9:  # tab
                text += "\t"
            elif char_code == 10:  # line break
                text += "\n"
            elif char_code == 24:  # hyphen
                text += "-"
            elif char_code == 30:  # nbsp
                text += " "
        elif 0xD800 <= char_code <= 0xDFFF:
            # 서로게이트 쌍 건너뜀
            pass
        else:
            try:
                text += chr(char_code)
            except (ValueError, OverflowError):
                pass
        j += 2
    return text


def main():
    parser = argparse.ArgumentParser(description="레거시 HWP 바이너리 파일에서 텍스트를 추출합니다")
    parser.add_argument("hwp_file", help="HWP 파일 경로")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="출력 형식 (기본: text)"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="출력 파일 경로 (미지정 시 stdout)"
    )
    args = parser.parse_args()

    result = extract_text_from_hwp(args.hwp_file)

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        lines = []
        for para in result["paragraphs"]:
            lines.append(para)
        output = "\n".join(lines)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"추출 완료: {len(result['paragraphs'])}개 단락 → {args.output}")
    else:
        print(output)
        print(f"\n[총 {len(result['paragraphs'])}개 단락, {sum(len(p) for p in result['paragraphs'])}자]",
              file=sys.stderr)


if __name__ == "__main__":
    main()
