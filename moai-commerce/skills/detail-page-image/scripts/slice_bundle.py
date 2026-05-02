#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
번들 PNG → 섹션 PNG 슬라이싱 스크립트.

큰 번들 이미지를 Y 좌표로 잘라 개별 섹션 PNG로 분리하고
표준 너비(1080)로 리사이즈합니다.

라이선스: MIT
의존성: Pillow only
사용법:
    python scripts/slice_bundle.py \
        --bundle ./bundles/B2_OPENING.png \
        --output-dir ./sections/ \
        --slices "02_pain:0:800,03_problem:800:1600,04_story:1600:2800"
"""
from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("[error] Pillow가 필요합니다: pip install Pillow\n")
    sys.exit(1)

logger = logging.getLogger("slice_bundle")


@dataclass
class SectionSlice:
    """섹션 슬라이스 정의: 이름과 Y 좌표 범위 [y_start, y_end)."""
    name: str
    y_start: int
    y_end: int  # exclusive

    def __post_init__(self) -> None:
        if self.y_end <= self.y_start:
            raise ValueError(
                f"슬라이스 {self.name}: y_end({self.y_end})는 y_start({self.y_start})보다 커야 합니다"
            )


def parse_slices(spec: str) -> list[SectionSlice]:
    """'name:y0:y1,name:y0:y1' 형식 문자열을 SectionSlice 리스트로 변환."""
    slices: list[SectionSlice] = []
    for entry in spec.split(","):
        parts = entry.strip().split(":")
        if len(parts) != 3:
            raise ValueError(f"슬라이스 형식이 잘못되었습니다: '{entry}' (예: '02_pain:0:800')")
        name = parts[0].strip()
        y_start = int(parts[1])
        y_end = int(parts[2])
        slices.append(SectionSlice(name=name, y_start=y_start, y_end=y_end))
    return slices


def slice_and_resize(
    bundle_png: Path,
    slices: list[SectionSlice],
    output_dir: Path,
    target_width: int = 1080,
) -> list[Path]:
    """번들 이미지를 슬라이스 정의에 따라 잘라 개별 섹션 PNG로 저장합니다."""
    if not slices:
        return []
    output_dir.mkdir(parents=True, exist_ok=True)

    out_paths: list[Path] = []
    with Image.open(bundle_png) as bundle:
        bundle_rgb = bundle.convert("RGB")
        bw, bh = bundle_rgb.size

        for s in slices:
            if s.y_end > bh:
                raise ValueError(
                    f"슬라이스 {s.name}: y_end {s.y_end}가 번들 높이 {bh}를 초과합니다"
                )

            # Y 좌표로 잘라낸다
            crop = bundle_rgb.crop((0, s.y_start, bw, s.y_end))

            # 너비만 리사이즈 (높이는 슬라이스 그대로 유지)
            if bw != target_width:
                slice_h = s.y_end - s.y_start
                crop = crop.resize((target_width, slice_h), Image.LANCZOS)

            out_path = output_dir / f"{s.name}.png"
            crop.save(out_path, "PNG")
            out_paths.append(out_path)
            logger.info("슬라이스 저장: %s -> %s", s.name, out_path)

    return out_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="번들 PNG를 Y 좌표로 잘라 개별 섹션 PNG로 저장합니다."
    )
    parser.add_argument("--bundle", required=True, type=Path, help="번들 PNG 경로")
    parser.add_argument("--output-dir", required=True, type=Path, help="섹션 PNG 출력 폴더")
    parser.add_argument(
        "--slices",
        required=True,
        type=str,
        help='슬라이스 정의 문자열 (예: "02_pain:0:800,03_problem:800:1600")',
    )
    parser.add_argument("--target-width", type=int, default=1080, help="출력 너비 (기본 1080)")
    parser.add_argument("--quiet", action="store_true", help="진행 로그 억제")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(message)s",
    )

    if not args.bundle.exists():
        sys.stderr.write(f"[error] 번들 파일이 없습니다: {args.bundle}\n")
        return 2

    slices = parse_slices(args.slices)
    out_paths = slice_and_resize(
        bundle_png=args.bundle,
        slices=slices,
        output_dir=args.output_dir,
        target_width=args.target_width,
    )

    import json
    print(json.dumps({"sections": [str(p) for p in out_paths]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
