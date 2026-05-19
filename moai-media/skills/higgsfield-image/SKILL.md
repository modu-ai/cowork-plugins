---
name: higgsfield-image
description: >
  Higgsfield MCP를 호출해 이미지를 생성합니다. "Higgsfield로 이미지 만들어 줘", "Soul 모델로",
  "Nano Banana로", "AI 이미지 생성"이라고 말하면 자동 호출됩니다. Soul·Nano Banana·Flux·
  Seedream·Cinema Studio 등 30+ 이미지 모델을 자연어 요청 한 줄로 선택·생성합니다.
  캐릭터 일관성(custom_reference_id), 스타일 프리셋, 해상도(720p/1080p/2K/4K), 시드 고정,
  비동기 잡 폴링까지 처리합니다. Higgsfield MCP가 등록되어 있어야 하며(자동), 첫 호출 시
  OAuth 인증 1회로 본인 Higgsfield 계정 사용.
user-invocable: true
version: 2.13.0
---

# Higgsfield 이미지 생성 (higgsfield-image)

## 개요

Higgsfield MCP의 `generate_image` 도구를 호출해 이미지를 생성하는 스킬입니다. 사용자 자연어 요청에서 주제·용도·청중을 추출하고, 30+ 이미지 모델 중 가장 적합한 것을 선택해 자동으로 생성합니다. 결과 검수와 변형(seed 변경·스타일 조정)까지 한 흐름에서 처리됩니다.

## 트리거 키워드

Higgsfield 이미지, Soul 모델, Nano Banana, Cinema Studio, Flux 이미지, Seedream, AI 이미지 생성, 시네마틱 이미지, 캐릭터 일관성, 4K 이미지

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

## 모델 선택 가이드 — 한눈에

| 모델 | 강점 | 적합 시점 |
|---|---|---|
| **Soul** ★ | 시네마틱·캐릭터 일관성·Higgsfield 자체 모델 | 인물 시리즈·브랜드 캐릭터·고품질 시네마틱 |
| **Nano Banana** | 텍스트 정확 렌더링 (Gemini 3 기반) | 카드뉴스·포스터·인포그래픽 (글자 핵심) |
| **Flux** | 사진 같은 사실적 일러스트 | 제품 샷·풍경·자연주의 톤 |
| **Seedream** | 다양한 스타일·실험적 톤 | 마케팅 비주얼·아트워크 |
| **Cinema Studio** | 영화 그레이딩·필름 룩 | 광고 키 비주얼·영상 썸네일 |

상세 모델별 사용 패턴은 [`references/model-guide.md`](./references/model-guide.md).

## 워크플로우

### 1단계 — 의도 파악

사용자 한 줄 요청에서 다음을 추출:

- 주제 (예: "회의실에서 노트북 보는 30대 한국인 여성")
- 용도 (마케팅 키 비주얼 · SNS 카드 · 제품 샷 · 캐릭터 시리즈 · 발표 슬라이드)
- 청중 (B2B 임원 · 일반 대중 · 디자이너 · 개발자)
- 톤 (시네마틱 · 미니멀 · 다크 · 따뜻함 · 신뢰감)

부족하면 AskUserQuestion 1라운드로 보완.

### 2단계 — 모델 자동 선택

위 표 기반 키워드 매칭. 매칭이 모호하면 사용자에게 후보 2-3개 제시.

| 사용자 표현 | 자동 선택 |
|---|---|
| "글자가 들어가는", "포스터" | Nano Banana |
| "시네마틱", "영화 같은" | Soul / Cinema Studio |
| "사진처럼", "사실적" | Flux |
| "예술적", "독특한 톤" | Seedream |
| "캐릭터 시리즈", "같은 인물" | Soul + custom_reference_id |

### 3단계 — 파라미터 설계

`generate_image` 호출 파라미터:

| 파라미터 | 값 | 권장 기본 |
|---|---|---|
| `prompt` | 텍스트 설명 (영문 + 한국어 OK) | 사용자 요청 + 모델별 톤 보정 |
| `width_and_height` | `1696x960`(16:9)·`1152x2048`(9:16)·`2048x1536`(4:3)·`1536x2048`(3:4)·`1024x1024`(1:1) | 용도에 맞춰 자동 |
| `quality` | `720p` / `1080p` | 1080p (인쇄·고해상도) / 720p (웹 미리보기) |
| `batch_size` | `1` / `4` | 1 (확정) / 4 (탐색·A/B) |
| `enhance_prompt` | true / false | true (기본 — 자동 보정) |
| `style_id` | 스타일 프리셋 UUID | 없으면 자동 |
| `style_strength` | 0.0-1.0 | 1.0 |
| `seed` | 1-1000000 | 미지정 (변형) 또는 고정값 (재현) |
| `custom_reference_id` | 캐릭터 reference UUID | 시리즈 일관성 시 |
| `custom_reference_strength` | 0.0-1.0 | 1.0 |
| `image_reference_url` | 참고 이미지 URL | 없음 (옵션) |

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
mcp__higgsfield__generate_image({
  prompt: "[모델별 톤 보정된 프롬프트]",
  width_and_height: "1696x960",
  quality: "1080p",
  enhance_prompt: true,
  batch_size: 1
})
```

호출 직전 ToolSearch로 MCP 도구 로드:
```
ToolSearch(query: "select:mcp__higgsfield__generate_image")
```

### 6단계 — 비동기 잡 폴링

Higgsfield는 **비동기 처리**. 호출 직후 job ID를 받고 상태가 변할 때까지 폴링:

| 상태 | 의미 |
|---|---|
| `queued` | 대기 중 (워크스페이스 잔액 부족 시 길어짐) |
| `in_progress` | 처리 중 (이미지는 보통 5-15초) |
| `completed` | 완료 — `result` 필드에 이미지 URL |
| `failed` | 실패 (프롬프트·파라미터 문제) |
| `nsfw` | 콘텐츠 필터링 |

처리 패턴:
```
Step 1: generate_image 호출 → job_id 수령
Step 2: 5초 간격으로 job 상태 폴링
Step 3: completed 시 이미지 URL 추출
Step 4: 결과 표시 + 사용자 검수
```

### 7단계 — 검수·변형

| 사용자 반응 | 후속 행동 |
|---|---|
| "좋다" | 결과 저장·다운로드 |
| "이건 어떻게 바꿔" | 같은 seed + 부분 프롬프트 수정 |
| "다른 방향으로" | seed 변경 + batch_size=4로 4종 후보 |
| "사진 다른 스타일로" | style_id 또는 모델 변경 |
| "같은 사람 다른 포즈" | custom_reference_id로 캐릭터 reference |

## 캐릭터 일관성 — Soul + Reference

같은 인물·캐릭터로 여러 이미지를 만들 때:

```
1. 첫 호출: 원하는 인물 1장 생성
2. 이미지 → create_character 도구로 reference UUID 생성
3. 이후 호출: custom_reference_id 파라미터에 UUID 전달
4. 동일 인물 + 다른 포즈·배경·표정 생성
```

이 패턴은 마케팅 캠페인·브랜드 캐릭터·시리즈 카드뉴스에 핵심.

## 사용 예시

### 예시 1 — 카드뉴스용 이미지 4종

```
요청: "스타트업 투자 카드뉴스 4장 이미지 만들어 줘 (글자 들어감)"

자동 선택: Nano Banana (글자 정확도)
비율: 1024x1024 (인스타 피드)
quality: 1080p
batch_size: 4
결과: 4종 변형 → 사용자가 1개 선택
```

### 예시 2 — 시네마틱 브랜드 키 비주얼

```
요청: "한국인 30대 여성 CEO가 회의실에서 노트북 보는 시네마틱 샷"

자동 선택: Soul (시네마틱)
비율: 1696x960 (16:9)
quality: 1080p
style: 시네마틱 그레이딩
결과: 1장 (확정)
```

### 예시 3 — 캐릭터 시리즈

```
1차 요청: "친근한 30대 한국 남성 일러스트, 흰 셔츠"
→ 1장 생성 → reference UUID 저장

2차 요청: "같은 사람이 노트북 보는 모습"
→ custom_reference_id 활용 → 동일 인물 다른 포즈

3차 요청: "같은 사람이 발표하는 모습"
→ 같은 reference 재사용
```

### 예시 4 — 제품 사진 (사실적)

```
요청: "프리미엄 가죽 지갑 제품 샷, 흰 배경, 부드러운 조명"

자동 선택: Flux (사진 사실성)
비율: 1024x1024 (이커머스 정사각)
quality: 1080p
결과: 1장
```

## 출력 형식

```
## Higgsfield 이미지 생성 결과

### 호출 정보
- 모델: [선택 모델]
- 프롬프트: [최종 프롬프트]
- 비율·해상도: [width_and_height · quality]
- Job ID: [Higgsfield job ID]

### 결과
- 이미지 URL: [Higgsfield CDN URL]
- 미리보기: ![](URL)
- 다운로드 경로: [로컬 저장 시]

### 검수
- 텍스트 정확성: [PASS/WARN]
- 비율·해상도: [PASS]
- 의도 부합: [점수]

### 후속 추천
- 같은 seed로 부분 수정
- 다른 비율 변형
- 캐릭터 ref 저장 (시리즈 작업 시)
```

## 비용 관리

- 이미지 생성: 모델별 크레딧 차등 (Soul·Cinema Studio는 더 비쌈)
- `batch_size=4`는 크레딧 4배 소비
- `quality=1080p`이 `720p`보다 2-3배 비쌈
- 사용자 워크스페이스 잔액은 `higgsfield.ai → Billing`에서 확인

## 주의사항

### Do

- 영문+한국어 프롬프트 모두 OK — Soul·Nano Banana는 한국어 잘 이해
- 첫 호출은 `batch_size=4`로 탐색 후 좋은 것을 확정
- 캐릭터 시리즈는 reference UUID로 일관성 확보
- 마케팅·제품 샷은 `quality=1080p` 필수

### Don't

- 한 번에 너무 긴 프롬프트 (200단어 초과) — 모델이 핵심을 놓침
- 모순된 요소 동시 요청 (예: "미니멀 + 화려한")
- nsfw·민감 콘텐츠 — 필터링되어 실패
- 다른 사람 초상권 침해 가능한 인물 묘사
- 저작권 있는 캐릭터·로고 직접 묘사

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| "Not connected" | OAuth 미인증 | Cowork → 설정 → MCP → Higgsfield → Connect |
| `queued`에서 멈춤 | 워크스페이스 잔액 부족 | higgsfield.ai → Billing에서 충전 |
| `failed` | 프롬프트·파라미터 오류 | 프롬프트 단순화 또는 width_and_height 표준값으로 |
| `nsfw` | 콘텐츠 필터링 | 프롬프트에서 민감 요소 제거 |
| 결과 품질 떨어짐 | 모델 선택 잘못 | 표 참고해서 다른 모델로 재시도 |
| 한국어 결과 어색 | 모델 한국어 학습 한계 | 영문 프롬프트로 재시도 |

## 관련 스킬

| 스킬 | 시점 |
|---|---|
| `moai-media:higgsfield-video` | 후속: 이미지를 영상으로 (image2video) |
| `moai-media:gemini-3-image-prompt` | 대안: 프롬프트만 산출 (외부 도구 사용) |
| `moai-media:gpt-image-2-prompt` | 대안: ChatGPT 사용 |
| `moai-media:midjourney-v8-prompt` | 대안: Discord MJ 사용 |
| `moai-content:card-news` | 후속: 이미지를 카드뉴스에 배치 |
| `moai-design:claude-design-system-prep` | 보조: 브랜드 톤 확정 후 이미지 |
| `moai-marketing:campaign-planner` | 보조: 캠페인 단위 시리즈 이미지 |
| `moai-commerce:commerce-product-image-pipeline` | 보조: 이커머스 제품 이미지 일괄 |

## References

- [`references/model-guide.md`](./references/model-guide.md) — 30+ 이미지 모델별 강점·약점·예시 프롬프트
- 공식 [Higgsfield MCP 페이지](https://higgsfield.ai/mcp)
- 모회사 [Higgsfield AI](https://higgsfield.ai)
