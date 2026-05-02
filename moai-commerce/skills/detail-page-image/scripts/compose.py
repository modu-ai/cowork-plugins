#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
13섹션 상세페이지 세로 합성 스크립트 (1080×12720 단일 PNG 생성).

라이선스: MIT
의존성: Pillow only
사용법:
    python scripts/compose.py \
        --sections-dir ./commerce-output/abc/sections/ \
        --output ./commerce-output/abc/combined.png
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("[error] Pillow가 필요합니다: pip install Pillow\n")
    sys.exit(1)

# 13섹션 정의 (감정여정 기반 한국 이커머스 상세페이지 표준)
SECTIONS = [
    {"number": 1,  "name": "01_hero",      "label": "Hero (긴급성 헤더)",        "height": 1600},
    {"number": 2,  "name": "02_pain",      "label": "Pain (공감)",                "height": 800},
    {"number": 3,  "name": "03_problem",   "label": "Problem (문제 정의)",        "height": 800},
    {"number": 4,  "name": "04_story",     "label": "Story (Before→After)",       "height": 1200},
    {"number": 5,  "name": "05_solution",  "label": "Solution (솔루션 소개)",      "height": 800},
    {"number": 6,  "name": "06_how",       "label": "How It Works (작동 방식)",    "height": 900},
    {"number": 7,  "name": "07_proof",     "label": "Social Proof (사회적 증거)",  "height": 1420},
    {"number": 8,  "name": "08_authority", "label": "Authority (권위/전문성)",    "height": 800},
    {"number": 9,  "name": "09_benefits",  "label": "Benefits (혜택)",             "height": 1200},
    {"number": 10, "name": "10_risk",      "label": "Risk Removal (리스크 제거)",  "height": 800},
    {"number": 11, "name": "11_compare",   "label": "Before/After Final (최종 대비)", "height": 800},
    {"number": 12, "name": "12_filter",    "label": "Target Filter (타겟 필터)",   "height": 700},
    {"number": 13, "name": "13_cta",       "label": "Final CTA (최종 CTA)",       "height": 900},
]

DEFAULT_WIDTH = 1080
TOTAL_HEIGHT = sum(s["height"] for s in SECTIONS)  # 12720

logger = logging.getLogger("compose")


def parse_color(s: str) -> tuple[int, int, int]:
    """'R,G,B' 형식 문자열을 RGB 튜플로 변환."""
    parts = [int(x.strip()) for x in s.split(",")]
    if len(parts) != 3 or any(not 0 <= p <= 255 for p in parts):
        raise ValueError(f"색상 형식이 잘못되었습니다: {s} (예: '40,40,40')")
    return tuple(parts)  # type: ignore[return-value]


def resize_section(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """섹션 이미지를 비율 유지 + 중앙 크롭 방식으로 목표 크기에 맞춥니다."""
    w, h = img.size
    if w == target_width and h == target_height:
        return img

    scale = max(target_width / w, target_height / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - target_width) // 2
    top = (new_h - target_height) // 2
    return img.crop((left, top, left + target_width, top + target_height))


def compose_vertical(
    sections_dir: Path,
    output_path: Path,
    width: int = DEFAULT_WIDTH,
    placeholder_color: tuple[int, int, int] = (40, 40, 40),
) -> dict:
    """13장의 섹션 이미지를 세로로 이어붙여 단일 합성 PNG를 만듭니다."""
    images: list[Image.Image] = []
    failed_sections: list[str] = []
    used_paths: list[str] = []

    for section in SECTIONS:
        name = section["name"]
        target_h = section["height"]
        path = sections_dir / f"{name}.png"

        if path.exists():
            try:
                img = Image.open(path).convert("RGB")
                img = resize_section(img, width, target_h)
                used_paths.append(str(path))
                logger.info("로드: %s (%dx%d)", name, img.size[0], img.size[1])
            except Exception as exc:
                logger.warning("로드 실패 %s: %s — 플레이스홀더 사용", name, exc)
                img = Image.new("RGB", (width, target_h), placeholder_color)
                failed_sections.append(name)
        else:
            logger.warning("누락: %s — 플레이스홀더 사용", path.name)
            img = Image.new("RGB", (width, target_h), placeholder_color)
            failed_sections.append(name)

        images.append(img)

    total_height = sum(img.size[1] for img in images)
    combined = Image.new("RGB", (width, total_height))

    y = 0
    for img in images:
        combined.paste(img, (0, y))
        y += img.size[1]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.save(output_path, "PNG", quality=95)
    logger.info("합성 완료: %s (%dx%d)", output_path, width, total_height)

    return {
        "combined": str(output_path),
        "size": f"{width}x{total_height}",
        "expected_size": f"{width}x{TOTAL_HEIGHT}",
        "size_matches_spec": total_height == TOTAL_HEIGHT,
        "sections_used": used_paths,
        "failed_sections": failed_sections,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="13섹션 상세페이지를 1080×12720 단일 PNG로 합성합니다."
    )
    parser.add_argument(
        "--sections-dir",
        required=True,
        type=Path,
        help="13장의 섹션 PNG가 들어 있는 폴더 (01_hero.png ~ 13_cta.png)",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="합성 결과 PNG 출력 경로 (예: combined.png)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_WIDTH,
        help="출력 너비 (기본 1080)",
    )
    parser.add_argument(
        "--placeholder-color",
        type=str,
        default="40,40,40",
        help="누락된 섹션의 플레이스홀더 색상 (기본 '40,40,40')",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="진행 로그 억제",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.quiet else logging.INFO,
        format="%(message)s",
    )

    if not args.sections_dir.exists() or not args.sections_dir.is_dir():
        sys.stderr.write(f"[error] sections-dir가 존재하지 않습니다: {args.sections_dir}\n")
        return 2

    placeholder = parse_color(args.placeholder_color)

    result = compose_vertical(
        sections_dir=args.sections_dir,
        output_path=args.output,
        width=args.width,
        placeholder_color=placeholder,
    )

    import json
    print(json.dumps(result, ensure_ascii=False))

    return 5 if result["failed_sections"] else 0


if __name__ == "__main__":
    sys.exit(main())
