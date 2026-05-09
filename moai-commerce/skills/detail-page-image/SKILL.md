---
name: detail-page-image
description: >
  한국 이커머스 상세페이지 13섹션 이미지를 자동 생성하고 1080×12720 단일 PNG로 합성하는 스킬입니다.
  "상세페이지 이미지 만들어줘", "13섹션 합성 이미지", "상폐 이미지", "1080 12720 합성"처럼 말하면 됩니다.
  detail-page-copy의 13섹션 카피와 사용자 상품 사진을 받아 섹션별 이미지 프롬프트를 작성하고,
  moai-media:nano-banana(Gemini 3 Image)로 13장의 이미지를 생성한 뒤
  Pillow 기반 자체 합성 스크립트(scripts/compose.py)로 1080×12720 세로 합성 PNG를 만듭니다.
  외부 패키지 설치 불필요 — 합성 로직은 cowork에 자체 구현되어 있습니다.
user-invocable: true
version: 2.2.0
---

# 상세페이지 이미지 합성 (Detail Page Image Composer)

## 개요

13섹션 감정여정 상세페이지 이미지를 생성하고 세로 합성 PNG로 만드는 스킬입니다.
moai-media:nano-banana를 백엔드로 사용하여 카테고리별 비주얼 톤이 일관된 13장의 섹션 이미지를 만들고,
Pillow 단일 의존성으로 1080×12720 단일 합성 이미지를 산출합니다.

## 트리거 키워드

상세페이지 이미지, 상폐 이미지, 13섹션 이미지, 1080 12720, 상세페이지 합성, 상품 상세 이미지,
combined.png, 상폐 합성본, 이커머스 이미지 합성

## 사전 조건

1. **Pillow 설치**: `pip install Pillow` 또는 `uv pip install Pillow`
   - Python 3.10+ 환경
   - 다른 의존성 없음 (NumPy 불필요)

2. **moai-media 플러그인 활성화**: 13섹션 이미지 생성에 nano-banana 사용
   - 또는 사용자가 별도로 13장의 섹션 이미지를 준비해서 폴더 경로 제공

3. **상품 사진 1~14장**: 실제 상품 레퍼런스 (옵션이지만 권장)

## 워크플로우

### 1단계: 입력 수집

다음을 확보합니다:
- 13섹션 카피 JSON (`detail-page-copy` 스킬 출력)
- 상품 사진 1~14장 경로
- 카테고리 (electronics/fashion/food/beauty/home/supplement/pet/kids/handmade/general)
- ProductDNA (선택, `product-photo-brief` 스킬 출력)
- 출력 디렉토리 (기본: `./commerce-output/{job_id}/`)

### 2단계: 13섹션 이미지 프롬프트 생성

각 섹션의 카피와 카테고리 비주얼 브리프를 합쳐 nano-banana 프롬프트를 작성합니다.
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

### 3단계: 이미지 생성 (moai-media:nano-banana)

생성 전략:
- 각 섹션 너비: **1080px**
- 섹션별 높이: `references/sections-spec.md` 표 참조 (Hero 1600 ~ Filter 700)
- 카테고리 비주얼 브리프(electronics/fashion/...) 모든 프롬프트에 주입
- 상품 레퍼런스 사진을 nano-banana의 image-to-image 모드로 전달

생성 결과를 `output_dir/{job_id}/sections/01_hero.png` ~ `13_cta.png`에 저장.

생성 실패 시: 해당 섹션은 다크 플레이스홀더(40,40,40)로 채워 합성을 진행합니다.

### 4단계: 1080×12720 합성 (`scripts/compose.py`)

```bash
python scripts/compose.py \
  --sections-dir ./commerce-output/{job_id}/sections/ \
  --output ./commerce-output/{job_id}/combined.png
```

스크립트 동작:
1. 13장 섹션 PNG를 순서대로 로드
2. 각 섹션을 표준 너비 1080으로 리사이즈 (비율 유지 + 중앙 크롭)
3. 섹션별 표준 높이로 조정
4. 세로로 이어붙여 1080×12720 단일 PNG 생성
5. 누락된 섹션은 `(40,40,40)` 다크 플레이스홀더로 대체

상세 알고리즘은 `scripts/compose.py`와 `scripts/README.md` 참조.

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

## scripts/compose.py 사용법

자세한 사용법은 `scripts/README.md` 참조. 핵심 명령:

```bash
# 13장이 sections/ 폴더에 01_hero.png ~ 13_cta.png로 있을 때
python scripts/compose.py \
  --sections-dir ./commerce-output/abc12345/sections/ \
  --output ./commerce-output/abc12345/combined.png
```

옵션:
- `--width INT`: 출력 너비 (기본 1080)
- `--placeholder-color "R,G,B"`: 누락 섹션 플레이스홀더 색 (기본 "40,40,40")
- `--quiet`: 진행 로그 억제

## 사용 예시

- "이 카피 결과로 13섹션 이미지 합성해줘"
- "상품사진 5장으로 상세페이지 1080 12720 만들어줘"
- "electronics 카테고리, 무선 이어폰 상세페이지 이미지 풀세트"

## 관련 스킬

- `moai-commerce:detail-page-copy` — 13섹션 카피 생성 (이 스킬 입력)
- `moai-commerce:product-photo-brief` — 상품 사진 사전 분석
- `moai-media:nano-banana` — 13섹션 이미지 생성 백엔드 (한국어 타이포 SOTA)
- `moai-media:fal-gateway` — Ideogram·Recraft 등 fal.ai 모델 보조 활용
- `moai-commerce:marketplace-coupang` — 채널별 이미지 규격 가이드

## 이 스킬을 사용하지 말아야 할 때

- 카피만 필요할 때: `detail-page-copy` 단독 사용
- 단일 상품 컷만 필요할 때: `moai-media:nano-banana` 직접 호출
- 한국어 타이포 강조: `moai-media:nano-banana` (Gemini 3 Image, 한국어 타이포 SOTA)
- 영상 생성: `moai-media:video-gen` (fal.ai Kling·Hailuo 등 백엔드)
- shadcn/ui 기반 웹 상세페이지: `moai-content:product-detail`

## 라이선스

MIT.