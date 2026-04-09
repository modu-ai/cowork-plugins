#!/usr/bin/env python3
"""
Nano Banana Pro Image Generator (v3.0.0 - Imagen 4 + Surrogate Safe Patch)
Google Imagen API를 이용한 이미지 생성 스크립트

[v3.0.0 변경사항]
- Imagen 3 → Imagen 4 모델 전환 (Imagen 3 서비스 종료)
- sampleCount → numberOfImages 파라미터 변경
- 4:5 비율 → 3:4 자동 전환 (Imagen 4 미지원)
- imageSize 파라미터 추가
- 타임아웃 60초 → 90초
- API 키 하드코딩 제거 (환경변수/파일 로드)

[v2.2.1 패치 유지]
- sanitize_text(): 프롬프트 내 단독 서로게이트 문자(U+D800~U+DFFF) 자동 제거
- safe_json_encode(): ensure_ascii=False + 서로게이트 이스케이프 제거

사용법:
  python generate_image.py "<프롬프트>" <저장경로.png> [aspect_ratio] [model]

예시:
  python generate_image.py "A peaceful morning desk setup..." slide_01.png 3:4
  python generate_image.py "..." cover.png 1:1 nano-banana-2

aspect_ratio 선택:
  3:4   → 인스타그램 세로형 카드뉴스 (기본값, 구 4:5 대체)
  1:1   → 정사각형 (1080×1080)
  9:16  → 스토리/릴스 세로형
  4:3   → 가로형
  16:9  → 와이드 가로형

model 선택:
  nano-banana-pro  → imagen-4.0-generate-001  (고품질, 기본값)
  nano-banana-2    → imagen-4.0-fast-generate-001 (빠른 생성)
  nano-banana-ultra → imagen-4.0-ultra-generate-001 (최고 품질)
"""

import sys
import json
import base64
import urllib.request
import urllib.error
import os
import re
from pathlib import Path

# ── API 설정 ──────────────────────────────────────────────────────────────────

def _find_key_file():
    """MoAI-Cowork 환경의 키 파일 자동 탐색"""
    candidates = [
        Path(__file__).parent.parent.parent.parent / "00_Context" / ".nano-banana-api-key",
        Path.home() / ".nano-banana-api-key",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def load_api_key():
    """API 키 로드 (환경변수 > 파일 순서)"""
    key = os.environ.get("NANO_BANANA_API_KEY")
    if key:
        return key.strip()
    kf = _find_key_file()
    if kf:
        return kf.read_text().strip()
    return None


API_KEY = load_api_key() or ""

MODEL_MAP = {
    # Imagen 4 모델 (v3.0.0)
    "nano-banana-pro": "imagen-4.0-generate-001",
    "nano-banana-2":   "imagen-4.0-fast-generate-001",
    "nano-banana-ultra": "imagen-4.0-ultra-generate-001",
    # 단축 별칭
    "pro":   "imagen-4.0-generate-001",
    "fast":  "imagen-4.0-fast-generate-001",
    "ultra": "imagen-4.0-ultra-generate-001",
    # Imagen 3 하위호환 (자동 전환)
    "imagen-3.0-generate-002": "imagen-4.0-generate-001",
    "imagen-3.0-fast-generate-001": "imagen-4.0-fast-generate-001",
}

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={key}"

# Imagen 4 지원 비율
IMAGEN4_SUPPORTED_RATIOS = {"1:1", "3:4", "4:3", "9:16", "16:9"}

# 비율 자동 전환 매핑
RATIO_FALLBACK = {
    "4:5": "3:4",
    "5:4": "4:3",
}

QUALITY_PRESET = {
    "3:4":  {"aspectRatio": "3:4"},   # 인스타 카드뉴스 (구 4:5 대체)
    "1:1":  {"aspectRatio": "1:1"},   # ~1024×1024
    "9:16": {"aspectRatio": "9:16"},  # 스토리/릴스
    "16:9": {"aspectRatio": "16:9"},  # 와이드
    "4:3":  {"aspectRatio": "4:3"},   # 가로형
}

DEFAULT_TIMEOUT = 90  # v3.0: 90초


# ── 서로게이트 안전 처리 유틸리티 (v2.2.1 유지) ────────────────────────────────

def sanitize_text(text: str) -> str:
    """
    텍스트에서 단독 서로게이트 문자(U+D800~U+DFFF)를 제거합니다.
    'no low surrogate in string' API 오류 방지용.
    """
    if not text:
        return text
    return re.sub(r'[\ud800-\udfff]', '', str(text))


def safe_json_dumps(obj, **kwargs) -> str:
    """
    ensure_ascii=False + 서로게이트 이스케이프 제거.
    한글/이모지를 직접 UTF-8로 인코딩하여 서로게이트 페어 문제를 원천 방지.
    """
    kwargs.setdefault("ensure_ascii", False)
    result = json.dumps(obj, **kwargs)
    # 단독 high surrogate 이스케이프 제거
    result = re.sub(
        r'\\u[dD][89aAbB][0-9a-fA-F]{2}(?!\\u[dD][cCdDeEfF][0-9a-fA-F]{2})',
        '', result
    )
    # 단독 low surrogate 이스케이프 제거
    result = re.sub(
        r'(?<!\\u[dD][89aAbB][0-9a-fA-F]{2})\\u[dD][cCdDeEfF][0-9a-fA-F]{2}',
        '', result
    )
    return result


def safe_json_encode(obj) -> bytes:
    """객체를 안전한 UTF-8 JSON bytes로 변환."""
    return safe_json_dumps(obj).encode("utf-8")


# ── 비율 검증 ───────────────────────────────────────────────────────────────

def validate_ratio(aspect_ratio: str) -> str:
    """Imagen 4 지원 비율 검증 및 자동 전환"""
    if aspect_ratio in IMAGEN4_SUPPORTED_RATIOS:
        return aspect_ratio

    if aspect_ratio in RATIO_FALLBACK:
        new_ratio = RATIO_FALLBACK[aspect_ratio]
        print(f"[WARN] Imagen 4는 '{aspect_ratio}' 비율을 지원하지 않습니다. "
              f"'{new_ratio}'로 자동 전환합니다.", file=sys.stderr)
        return new_ratio

    print(f"[WARN] 미지원 비율 '{aspect_ratio}'. 기본값 '3:4'로 대체합니다.",
          file=sys.stderr)
    return "3:4"


# ── 이미지 생성 ───────────────────────────────────────────────────────────────

def generate_image(prompt: str, output_path: str,
                   aspect_ratio: str = "3:4",
                   model_alias: str = "nano-banana-pro") -> bool:
    """
    Imagen API로 이미지 생성 후 파일 저장.
    서로게이트 문자를 자동 제거하여 JSON 인코딩 오류를 방지합니다.
    성공 시 True, 실패 시 False 반환.
    """
    api_key = API_KEY or load_api_key()
    if not api_key:
        print("[ERROR] API 키가 없습니다. NANO_BANANA_API_KEY 환경변수를 설정하세요.",
              file=sys.stderr)
        return False

    # 프롬프트 안전 처리
    prompt = sanitize_text(prompt)

    # 모델 해석 (Imagen 3 → 4 자동 매핑 포함)
    model_id = MODEL_MAP.get(model_alias, model_alias)
    if model_alias in ("imagen-3.0-generate-002", "imagen-3.0-fast-generate-001"):
        print(f"[WARN] Imagen 3 '{model_alias}'은(는) 서비스 종료됨. "
              f"'{model_id}'로 자동 전환.", file=sys.stderr)

    url = BASE_URL.format(model=model_id, key=api_key)

    # v3.0: 비율 검증
    aspect_ratio = validate_ratio(aspect_ratio)
    ratio_params = QUALITY_PRESET.get(aspect_ratio,
                                       {"aspectRatio": aspect_ratio})

    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "numberOfImages": 1,  # v3.0: sampleCount → numberOfImages
            **ratio_params,
        }
    }

    body = safe_json_encode(payload)
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            data = json.loads(resp.read())

        predictions = data.get("predictions", [])
        if not predictions:
            print(f"[ERROR] 빈 응답: {safe_json_dumps(data)[:300]}",
                  file=sys.stderr)
            return False

        img_b64 = predictions[0].get("bytesBase64Encoded", "")
        if not img_b64:
            print(f"[ERROR] 이미지 데이터 없음. RAI 차단 여부: "
                  f"{predictions[0].get('raiFilteredReason', 'N/A')}",
                  file=sys.stderr)
            return False

        # 디렉토리 생성
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(img_b64))

        size_kb = os.path.getsize(output_path) // 1024
        print(f"[OK] {output_path} ({size_kb}KB, {aspect_ratio}, model={model_id})")
        return True

    except urllib.error.HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")[:300]
        print(f"[ERROR] HTTP {e.code}: {body_err}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(f"[ERROR] 네트워크 오류: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[ERROR] 예외 발생: {e}", file=sys.stderr)
        return False


def generate_batch(jobs: list, output_dir: str = ".") -> dict:
    """
    여러 이미지를 순차 생성.
    jobs: [{"prompt": "...", "filename": "slide_01.png", "ratio": "3:4"}, ...]
    반환: {"slide_01.png": True/False, ...}
    """
    results = {}
    total = len(jobs)
    for i, job in enumerate(jobs, 1):
        filename = job.get("filename", f"image_{i:02d}.png")
        path = os.path.join(output_dir, filename)
        ratio = job.get("ratio", "3:4")
        model = job.get("model", "nano-banana-pro")
        # 프롬프트 안전 처리
        prompt = sanitize_text(job["prompt"])
        print(f"[{i}/{total}] 생성 중: {filename} ({ratio})")
        results[filename] = generate_image(prompt, path, ratio, model)
    return results


if __name__ == "__main__":
    # ── CLI 모드 ──────────────────────────────────────────────────────────────
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    _prompt = sys.argv[1]
    _output = sys.argv[2]
    _ratio  = sys.argv[3] if len(sys.argv) > 3 else "3:4"
    _model  = sys.argv[4] if len(sys.argv) > 4 else "nano-banana-pro"

    success = generate_image(_prompt, _output, _ratio, _model)
    sys.exit(0 if success else 1)
