---
name: commerce-detail-page-image
description: >
  한국 이커머스 상세페이지 13섹션 이미지를 자동 생성하고 1080×12720 단일 PNG로 합성하는 스킬입니다.
  "상세페이지 이미지 만들어줘", "13섹션 합성 이미지", "상폐 이미지", "1080 12720 합성"처럼 말하면 됩니다.
  commerce-detail-page-copy의 13섹션 카피와 사용자 상품 사진을 받아 섹션별 이미지 프롬프트를 작성하고,
  moai-media:media-higgsfield-image(Nano Banana Pro 등 11개 모델)로 13장의 이미지를 생성한 뒤
  Pillow로 1080×12720 세로 합성 PNG를 직접 조립합니다(합성 로직은 이 문서에 인라인 코드로 포함).
  외부 패키지는 Pillow 하나만 필요합니다.
version: "1.0.0"
---

# 상세페이지 이미지 합성 (Detail Page Image Composer)

## 개요

13섹션 감정여정 상세페이지 이미지를 생성하고 세로 합성 PNG로 만드는 스킬입니다.
moai-media:media-higgsfield-image를 백엔드로 사용하여 카테고리별 비주얼 톤이 일관된 13장의 섹션 이미지를 만들고,
Pillow 단일 의존성으로 1080×12720 단일 합성 이미지를 산출합니다.

## 트리거 키워드

상세페이지 이미지, 상폐 이미지, 13섹션 이미지, 1080 12720, 상세페이지 합성, 상품 상세 이미지,
combined.png, 상폐 합성본, 이커머스 이미지 합성

## 사전 조건

1. **Pillow 설치**: `pip install Pillow` 또는 `uv pip install Pillow`
   - Python 3.10+ 환경
   - 다른 의존성 없음 (NumPy 불필요)

2. **moai-coworker 플러그인 활성화**: 13섹션 이미지 생성에 media-higgsfield-image 사용
   - 또는 사용자가 별도로 13장의 섹션 이미지를 준비해서 폴더 경로 제공

3. **상품 사진 1-14장**: 실제 상품 레퍼런스 (옵션이지만 권장)

## 워크플로우

### 1단계: 입력 수집

다음을 확보합니다:
- 13섹션 카피 JSON (`commerce-detail-page-copy` 스킬 출력)
- 상품 사진 1-14장 경로
- 카테고리 (electronics/fashion/food/beauty/home/supplement/pet/kids/handmade/general)
- ProductDNA (선택, `commerce-product-photo-brief` 스킬 출력)
- 출력 디렉토리 (기본: `./commerce-output/{job_id}/`)

### 2단계: 13섹션 이미지 프롬프트 생성

각 섹션의 카피와 카테고리 비주얼 브리프를 합쳐 media-higgsfield-image 프롬프트를 작성합니다.
`references/image-prompts.md` 참조 (섹션별 비주얼 언어, 합성 가이드).

각 섹션은 고유한 비주얼 언어를 가집니다:
- **Hero**: cinematic_product_portrait — 풀블리드 + 드라마틱 림라이트
- **Pain**: emotional_photography_no_product — 어두운 톤, 상품 미노출
- **Problem**: clinical_infographic — 깔끔한 인포그래픽
- **Story**: editorial_split_before_after — Before/After 좌우 분할
- **Solution**: product_beauty_shot — 스튜디오 뷰티샷
- **How**: illustrated_step_sequence — 3단계 일러스트
- **Proof**: magazine_spread — 매거진 스프레드
- **Authority**: portrait_with_quote — 인물 포트레이트 + 인용
- **Benefits**: icon_grid_with_lifestyle — 아이콘 그리드 + 라이프스타일
- **Risk**: document_with_seal — 문서·인증 스타일
- **Compare**: split_screen_vs — 50/50 분할 비교
- **Filter**: checklist_visual — 체크리스트 시각화
- **CTA**: urgent_product_reveal — 긴급성 + 가격 강조

### 3단계: 이미지 생성 (moai-media:media-higgsfield-image)

생성 전략:
- 각 섹션 너비: **1080px**
- 섹션별 높이: `references/sections-spec.md` 표 참조 (Hero 1600-Filter 700)
- 카테고리 비주얼 브리프(electronics/fashion/...) 모든 프롬프트에 주입
- 상품 레퍼런스 사진을 media-higgsfield-image의 image-to-image 모드로 전달

생성 결과를 `output_dir/{job_id}/sections/01_hero.png` 부터 `13_cta.png` 까지 저장.

생성 실패 시: 해당 섹션은 다크 플레이스홀더(40,40,40)로 채워 합성을 진행합니다.

### 4단계: 1080×12720 합성 (Pillow 인라인 조립)

별도 스크립트 없이, 아래 Pillow 코드를 그대로 실행해 13장을 세로로 이어붙입니다.
동작: (1) 01_hero~13_cta 순서 로드 → (2) 너비 1080으로 리사이즈(비율 유지 + 중앙 크롭) →
(3) 섹션별 표준 높이로 조정 → (4) 세로 스택 → (5) 누락 섹션은 `(40,40,40)` 다크 플레이스홀더로 대체.

```python
from PIL import Image
from pathlib import Path

WIDTH = 1080
# (파일명 슬러그, 표준 높이) — sections-spec.md 표와 동일
SECTIONS = [
    ("01_hero", 1600), ("02_pain", 800), ("03_problem", 900), ("04_story", 1000),
    ("05_solution", 1100), ("06_how", 1000), ("07_proof", 1100), ("08_authority", 900),
    ("09_benefits", 1000), ("10_risk", 800), ("11_compare", 900), ("12_filter", 700),
    ("13_cta", 900),
]
PLACEHOLDER = (40, 40, 40)

def fit(img, w, h):
    # 비율 유지 리사이즈 후 중앙 크롭으로 정확히 w×h 맞춤
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))

sections_dir = Path("./commerce-output/JOB_ID/sections")   # 실제 job_id로 치환
total_h = sum(h for _, h in SECTIONS)
canvas = Image.new("RGB", (WIDTH, total_h), PLACEHOLDER)
failed, y = [], 0
for slug, h in SECTIONS:
    p = sections_dir / f"{slug}.png"
    if p.exists():
        canvas.paste(fit(Image.open(p).convert("RGB"), WIDTH, h), (0, y))
    else:
        failed.append(slug)   # 누락 → 다크 플레이스홀더 그대로 유지
    y += h
canvas.save(sections_dir.parent / "combined.png")
print({"size": f"{WIDTH}x{total_h}", "failed_sections": failed})
```

높이 표준값은 `references/sections-spec.md`를, 섹션별 비주얼 언어는 `references/image-prompts.md`를 참조합니다.

### 5단계: 출력 보고

```json
{
  "job_id": "a1b2c3d4",
  "output_dir": "/abs/.../commerce-output/a1b2c3d4",
  "combined": "/abs/.../combined.png",
  "sections": [
    "/abs/.../sections/01_hero.png",
    "...",
    "/abs/.../sections/13_cta.png"
  ],
  "failed_sections": [],
  "elapsed_sec": 0,
  "size": "1080x12720"
}
```

`failed_sections`가 비어있지 않으면 사용자에게 다음을 안내:
- 어떤 섹션이 실패했는지
- 같은 `--output --job-id`로 재실행 시 자동 재개되는지 (재개는 사용자가 수동으로 해당 섹션만 재생성)

## 출력 파일 구조

```
./commerce-output/{job_id}/
├── analysis.json              # 13섹션 카피 + 프롬프트 + ProductDNA
├── sections/                   # 13장 섹션 (1080×가변)
│   ├── 01_hero.png            (1080×1600)
│   ├── 02_pain.png            (1080×800)
│   ├── ...
│   └── 13_cta.png             (1080×900)
└── combined.png                # 1080×12720 세로 합성본
```

## 합성 코드 조정 포인트

4단계 인라인 Pillow 코드에서 다음 값만 바꾸면 됩니다:

- `WIDTH`: 출력 너비 (기본 1080)
- `PLACEHOLDER`: 누락 섹션 색 (기본 `(40, 40, 40)`)
- `SECTIONS`: 섹션 순서·표준 높이 (기본 13섹션, `references/sections-spec.md`와 동일)
- `sections_dir`: 실제 job_id 경로로 치환

> 이 스킬은 부재 스크립트(compose.py) 참조를 원칙 A(프롬프트/인라인 코드 경로)로 대체했습니다 — 합성은 위 Pillow 코드를 직접 실행합니다.

## 사용 예시

- "이 카피 결과로 13섹션 이미지 합성해줘"
- "상품사진 5장으로 상세페이지 1080 12720 만들어줘"
- "electronics 카테고리, 무선 이어폰 상세페이지 이미지 풀세트"

## 관련 스킬

- `moai-seller:commerce-detail-page-copy` — 13섹션 카피 생성 (이 스킬 입력)
- `moai-seller:commerce-product-photo-brief` — 상품 사진 사전 분석
- 13섹션 이미지 생성 — **Higgsfield MCP**(Soul·시네마틱 이미지·캐릭터) 직접 호출
- `moai-seller:commerce-marketplace-coupang` — 채널별 이미지 규격 가이드

## 이 스킬을 사용하지 말아야 할 때

- 카피만 필요할 때: `commerce-detail-page-copy` 단독 사용
- 단일 상품 컷만 필요할 때: **Higgsfield MCP** 직접 호출
- 영상 생성: **Higgsfield MCP**(DOP·Soul) 직접 호출
- shadcn/ui 기반 웹 상세페이지: `moai-seller:commerce-product-detail`

## 라이선스

MIT.
