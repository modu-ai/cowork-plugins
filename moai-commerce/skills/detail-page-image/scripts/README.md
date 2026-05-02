# detail-page-image scripts

> Pillow 단일 의존성으로 동작하는 합성/슬라이싱 스크립트.

## 의존성

```bash
pip install Pillow
# 또는
uv pip install Pillow
```

Python 3.10+ 권장.

## 1. compose.py — 13섹션 → 1080×12720 단일 PNG

13장의 섹션 PNG를 세로로 이어붙여 단일 합성본을 만듭니다.

### 입력 폴더 구조

```
sections/
├── 01_hero.png       (1080×1600 권장)
├── 02_pain.png       (1080×800)
├── 03_problem.png    (1080×800)
├── 04_story.png      (1080×1200)
├── 05_solution.png   (1080×800)
├── 06_how.png        (1080×900)
├── 07_proof.png      (1080×1420)
├── 08_authority.png  (1080×800)
├── 09_benefits.png   (1080×1200)
├── 10_risk.png       (1080×800)
├── 11_compare.png    (1080×800)
├── 12_filter.png     (1080×700)
└── 13_cta.png        (1080×900)
```

각 파일은 표준 너비(1080)와 정확한 높이가 아니어도 자동으로 비율 유지 + 중앙 크롭됩니다.

### 사용법

```bash
python compose.py \
    --sections-dir ./commerce-output/abc12345/sections/ \
    --output ./commerce-output/abc12345/combined.png
```

### 옵션

| 플래그 | 기본값 | 설명 |
|--------|--------|------|
| `--sections-dir` | (필수) | 13장의 PNG가 있는 폴더 |
| `--output` | (필수) | 출력 PNG 경로 |
| `--width` | 1080 | 표준 너비 |
| `--placeholder-color` | "40,40,40" | 누락 섹션 플레이스홀더 색 (R,G,B) |
| `--quiet` | False | 진행 로그 억제 |

### 출력

stdout에 단일 줄 JSON:
```json
{"combined": "/abs/.../combined.png", "size": "1080x12720", "size_matches_spec": true, "sections_used": [...], "failed_sections": []}
```

### 종료 코드

- `0`: 모든 섹션 정상 합성
- `2`: sections-dir 경로 오류
- `5`: 부분 성공 (일부 섹션이 플레이스홀더로 대체됨)

## 2. slice_bundle.py — 큰 번들 PNG → 섹션 PNG

이미지 생성기가 여러 섹션을 하나의 큰 번들로 만든 경우, Y 좌표로 잘라 개별 섹션 PNG로 분리합니다.

### 사용법

```bash
python slice_bundle.py \
    --bundle ./bundles/B2_OPENING.png \
    --output-dir ./sections/ \
    --slices "02_pain:0:800,03_problem:800:1600,04_story:1600:2800"
```

### 슬라이스 형식

`name:y_start:y_end` 콤마 구분. y_end는 exclusive.

### 옵션

| 플래그 | 기본값 | 설명 |
|--------|--------|------|
| `--bundle` | (필수) | 번들 PNG 경로 |
| `--output-dir` | (필수) | 출력 폴더 |
| `--slices` | (필수) | 슬라이스 정의 문자열 |
| `--target-width` | 1080 | 출력 너비 (자동 리사이즈) |
| `--quiet` | False | 진행 로그 억제 |

## 라이선스

MIT.
