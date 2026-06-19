---
name: higgsfield-image
description: |
  Higgsfield MCP 기반 AI 이미지를 자연어 요청 한 줄로 생성합니다.
  다음과 같은 요청 시 사용하세요:
  - "Higgsfield로 이미지 만들어 줘"
  - "Soul 2.0으로 이미지"
  - "Nano Banana Pro로 카드뉴스 이미지"
  - "AI 이미지 생성해줘"
  - "Seedream 4.0으로 이미지"
  - "시네마틱 키 비주얼 만들어줘"
  - "캐릭터 일관성 있는 시리즈 이미지"
  - "4K 이미지 생성"
  Soul·Soul 2.0·Soul Cinema·Nano Banana·Nano Banana Pro·GPT Image·GPT Image 2·Seedream 4.0·Flux Kontext·Wan 2.2 Image·Wan 2.5 11개 공식 이미지 모델과 캐릭터 일관성(Soul Characters), 스타일 프리셋, 해상도(720p/1080p/2K/4K), 시드 고정, 비동기 잡 폴링까지 처리한 완성 이미지를 산출합니다.
  실제 이미지 생성 요청 시 Higgsfield MCP가 연결돼 있으면 이 스킬을 사용하세요 (프롬프트만 필요하면 moai-media의 *-prompt 스킬).
user-invocable: true
version: 2.27.0
---

# Higgsfield 이미지 생성 (higgsfield-image)

## 개요

Higgsfield MCP의 이미지 생성 도구를 호출하는 스킬입니다. 사용자 자연어 요청에서 주제·용도·청중을 추출하고, 공식 11개 이미지 모델 중 가장 적합한 것을 선택해 자동으로 생성합니다.

## 트리거 키워드

Higgsfield 이미지, Soul, Soul 2.0, Soul Cinema, Nano Banana, Nano Banana Pro, GPT Image, GPT Image 2, Seedream 4.0, Flux Kontext, Wan 2.2 Image, Wan 2.5, AI 이미지 생성, 시네마틱 이미지, 캐릭터 일관성, 4K 이미지

## 전제 — MCP 등록

`moai-media` 플러그인 설치 시 `.mcp.json`이 Higgsfield MCP를 자동 등록합니다.

```json
{
  "higgsfield": {
    "type": "http",
    "url": "https://mcp.higgsfield.ai/mcp"
  }
}
```

첫 호출 직전 Cowork에서 OAuth 인증을 1회 완료해야 합니다 (`moai-media/CONNECTORS.md` 참고).

## 공식 11개 이미지 모델 — 한눈에

[higgsfield.ai](https://higgsfield.ai) 공식 페이지 기준 (2026-05).

### Soul 계열 (Higgsfield 자체) ★

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Soul** | 시네마틱 그레이딩·인물 디테일 (1세대) | 일반 시네마틱 |
| **Soul 2.0** | Soul 1의 개선판, 디테일·표현력 향상 | 인물 시리즈·신규 작업 권장 |
| **Soul Cinema** | 영화 룩 특화, 35mm·필름 그레이딩 | 광고 키 비주얼·영상 썸네일 |

Soul Characters 기능으로 캐릭터 reference 학습 → 시리즈 일관성.

### Nano Banana 계열 (Gemini 3 기반)

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Nano Banana** | 글자 렌더링·기본 품질 | 일반 SNS·인포그래픽 |
| **Nano Banana Pro** | 2K+ 해상도·일반 카드 톤 | 일반 SNS 카드·인쇄 보조 |

### GPT Image 계열 (OpenAI)

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **GPT Image** | OpenAI 1세대 이미지 모델 | 범용 |
| **GPT Image 2** ★ | OpenAI 개선판, **글자 렌더링 SOTA**·사실성·정확성↑ | **카드뉴스·포스터** ★·사실적 일러스트·제품 |

### Seedream

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Seedream 4.0** | 다양한 스타일·실험적 톤·아트워크 | 마케팅 비주얼·아트 |

### Flux 계열

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Flux Kontext** | 사진 같은 사실성·재질·조명 정교 | 제품 샷·풍경·인테리어 |

### Wan 계열 (중국 최신)

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Wan 2.2 Image** | 다양한 톤·실험적 표현 | 마케팅 톤 다양화 |
| **Wan 2.5** | Wan 2.2 개선판 | 최신 톤 |

상세 모델별 사용 패턴은 [`references/model-guide.md`](./references/model-guide.md).

## 워크플로우

### 1단계 — 의도 파악

사용자 한 줄 요청에서 다음을 추출:

- 주제 (예: "회의실에서 노트북 보는 30대 한국인 여성")
- 용도 (마케팅 키 비주얼 · SNS 카드 · 제품 샷 · 캐릭터 시리즈 · 발표 슬라이드)
- 청중 (B2B 임원 · 일반 대중 · 디자이너 · 개발자)
- 톤 (시네마틱 · 미니멀 · 다크 · 따뜻함 · 신뢰감)

부족하면 AskUserQuestion 1라운드.

### 2단계 — 모델 자동 선택

키워드 매칭. 매칭이 모호하면 후보 2-3개 제시.

| 사용자 표현 | 자동 선택 |
|---|---|
| "글자 정확하게", "포스터", "카드뉴스" | **GPT Image 2** (1순위) 또는 Nano Banana Pro (2K) |
| "시네마틱", "영화 룩" | Soul Cinema 또는 Soul 2.0 |
| "인물 디테일", "캐릭터" | Soul 2.0 (+ Soul Characters reference) |
| "사진처럼", "사실적", "제품 샷" | Flux Kontext (1순위) 또는 GPT Image 2 |
| "예술적", "독특한 톤", "아트워크" | Seedream 4.0 |
| "실험적", "새로운 톤" | Wan 2.5 |
| "범용·빠름" | GPT Image 또는 Nano Banana |

### 3단계 — 파라미터 설계

| 파라미터 | 값 | 권장 기본 |
|---|---|---|
| `prompt` | 텍스트 설명 (영문·한국어 OK) | 사용자 요청 + 모델별 톤 보정 |
| `width_and_height` | `1696x960`(16:9)·`1152x2048`(9:16)·`2048x1536`(4:3)·`1536x2048`(3:4)·`1024x1024`(1:1) | 용도별 자동 |
| `quality` | `720p` / `1080p` / `2K` / `4K` | 일반 `1080p` · 인쇄 `2K`·`4K` |
| `batch_size` | `1` / `4` | 1 (확정) / 4 (탐색·A/B) |
| `enhance_prompt` | true / false | true (기본) |
| `style_id` | 스타일 프리셋 UUID | 없으면 자동 |
| `style_strength` | 0.0-1.0 | 1.0 |
| `seed` | 1-1000000 | 미지정 (변형) / 고정 (재현) |
| `custom_reference_id` | Soul Characters reference UUID | 시리즈 일관성 |
| `image_reference_url` | 참고 이미지 URL | 옵션 |

### 4단계 — 비율 자동 매핑

| 용도 | 비율 | width_and_height |
|---|---|---|
| 인스타 피드 | 1:1 | `1024x1024` |
| 인스타 스토리·릴스 | 9:16 | `1152x2048` |
| 페이스북·트위터·블로그 | 16:9 | `1696x960` |
| 인쇄·포스터 (세로) | 3:4 | `1536x2048` |
| 인쇄·포스터 (가로) | 4:3 | `2048x1536` |

### 5단계 — MCP 호출

```
ToolSearch(query: "select:mcp__higgsfield__generate_image")

mcp__higgsfield__generate_image({
  prompt: "[모델별 톤 보정된 프롬프트]",
  model: "soul_2_0",  // 또는 "nano_banana_pro" 등
  width_and_height: "1696x960",
  quality: "1080p",
  enhance_prompt: true,
  batch_size: 1
})
```

모델 식별자는 공식 페이지에서 underscore_separated 형식 사용 (예: `soul_2_0`, `nano_banana_pro`, `seedream_4_0`, `flux_kontext`).

### 6단계 — 비동기 잡 폴링

Higgsfield는 **비동기 처리**. 호출 직후 job ID를 받고 상태 폴링:

| 상태 | 의미 |
|---|---|
| `queued` | 대기 중 (잔액 부족 시 길어짐) |
| `in_progress` | 처리 중 (이미지 5-15초) |
| `completed` | 완료 — `result` 필드에 이미지 URL |
| `failed` | 실패 (프롬프트·파라미터 문제) |
| `nsfw` | 콘텐츠 필터링 |

### 7단계 — 검수·변형

| 사용자 반응 | 후속 행동 |
|---|---|
| "좋다" | 저장·다운로드 |
| "이건 바꿔" | 같은 seed + 부분 수정 |
| "다른 방향" | seed 변경 + batch_size=4 |
| "사진 다른 스타일" | model 변경 (Flux Kontext ↔ Soul 2.0 등) |
| "같은 사람 다른 포즈" | Soul Characters reference UUID |

## 캐릭터 일관성 — Soul Characters

공식 Higgsfield 기능. Soul 또는 Soul 2.0과 결합:

```
1. 첫 호출 (Soul 2.0): 원하는 인물 1장 생성
2. Soul Characters에 reference 등록 → UUID 수령
3. 이후 호출: custom_reference_id 파라미터에 UUID 전달
4. 동일 인물 + 다른 포즈·배경·표정 생성
```

마케팅 캠페인·브랜드 캐릭터·시리즈 카드뉴스에 핵심.

## 사용 예시

### 예시 1 — 카드뉴스용 이미지 4종 (글자 정확)

```
요청: "스타트업 투자 카드뉴스 4장 이미지 만들어 줘 (글자 들어감)"

자동 선택: GPT Image 2 (글자 렌더링 SOTA) — 1순위
대안: Nano Banana Pro (2K, 보조)
비율: 1024x1024 (인스타 피드)
quality: 2K
batch_size: 4
```

### 예시 2 — 시네마틱 브랜드 키 비주얼

```
요청: "한국인 30대 여성 CEO가 회의실에서 노트북 보는 시네마틱 샷"

자동 선택: Soul 2.0 (인물 디테일) 또는 Soul Cinema (영화 룩)
비율: 1696x960 (16:9)
quality: 1080p
```

### 예시 3 — 캐릭터 시리즈

```
1차: Soul 2.0 → 인물 1장 → Soul Characters에 reference 저장
2차+: 같은 reference UUID로 동일 인물 다양한 포즈
```

### 예시 4 — 제품 사진 (사실적)

```
요청: "프리미엄 가죽 지갑 제품 샷, 흰 배경"

자동 선택: Flux Kontext (사진 사실성)
비율: 1024x1024
quality: 1080p
```

### 예시 5 — 광고 키 비주얼 (영화 톤)

```
요청: "신제품 광고 키 비주얼, 35mm 필름 룩"

자동 선택: Soul Cinema
비율: 1696x960
quality: 1080p
```

## 출력 형식

```
## Higgsfield 이미지 생성 결과

### 호출 정보
- 모델: [선택 모델, 예: soul_2_0]
- 프롬프트: [최종 프롬프트]
- 비율·해상도: [width_and_height · quality]
- Job ID: [Higgsfield job ID]

### 결과
- 이미지 URL: [Higgsfield CDN URL]
- 미리보기: ![](URL)
- 다운로드 경로: [로컬]

### 검수
- 텍스트 정확성·비율·해상도: [PASS]
- 의도 부합: [점수]

### 후속 추천
- 같은 seed로 부분 수정
- 다른 비율 변형
- Soul Characters reference 저장 (시리즈 작업 시)
```

## 비용 관리

- 모델별 크레딧 차등 (Soul Cinema·Pro급은 더 비쌈)
- `batch_size=4`는 크레딧 4배
- `quality=2K`·`4K`가 `1080p`보다 비쌈
- 워크스페이스 잔액: `higgsfield.ai → Billing`

## 주의사항

### Do

- 영문·한국어 프롬프트 모두 OK
- 첫 호출은 `batch_size=4`로 탐색 후 확정
- 캐릭터 시리즈는 Soul Characters reference로 일관성
- 인쇄·고품질은 `quality=2K` 이상

### Don't

- 200단어 초과 긴 프롬프트
- 모순된 요소 동시 요청 ("미니멀 + 화려한")
- nsfw·민감 콘텐츠
- 초상권 침해 가능한 인물 묘사
- 저작권 있는 캐릭터·로고 직접 묘사

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| "Not connected" | OAuth 미인증 | Cowork → 설정 → MCP → Higgsfield → Connect |
| `queued` 멈춤 | 잔액 부족 | higgsfield.ai → Billing 충전 |
| `failed` | 프롬프트·파라미터 오류 | 프롬프트 단순화·표준 width_and_height |
| `nsfw` | 콘텐츠 필터링 | 민감 요소 제거 |
| 결과 품질 낮음 | 모델 부적합 | 표 참고해서 다른 모델 |
| 한국어 결과 어색 | 모델 한국어 한계 | 영문 프롬프트 재시도 |

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:higgsfield-video` | 후속: 이미지를 영상으로 |
| `moai-media:gemini-3-image-prompt` | 대안: 프롬프트만 산출 (외부 도구) |
| `moai-media:gpt-image-2-prompt` | 대안: 외부 ChatGPT 사용 |
| `moai-content:card-news` | 후속: 이미지를 카드뉴스에 배치 |
| `moai-design:claude-design-system-prep` | 보조: 브랜드 톤 확정 |
| `moai-marketing:campaign-planner` | 보조: 캠페인 시리즈 이미지 |
| `moai-commerce:commerce-product-image-pipeline` | 보조: 이커머스 일괄 |

## References

- [`references/model-guide.md`](./references/model-guide.md) — 11 모델별 강점·약점·예시 프롬프트
- [Higgsfield 공식 사이트](https://higgsfield.ai) — 모델 목록 (이미지 11종 + 영상 11종 + 30+ 광고)
- [Higgsfield MCP 안내](https://higgsfield.ai/mcp)
- [Higgsfield Skills](https://higgsfield.ai/skills)

## 모델 목록 출처

본 스킬의 11개 이미지 모델 목록은 **[higgsfield.ai 공식 메인 페이지](https://higgsfield.ai)** 명시 기준입니다 (2026-05). 모델은 Higgsfield 정책에 따라 추가·변경될 수 있습니다.
