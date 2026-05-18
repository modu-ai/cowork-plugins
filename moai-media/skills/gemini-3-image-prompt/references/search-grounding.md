# Gemini 3 Pro Image — Search Grounding (Google Search 연동)

Gemini 3 Pro Image의 차별 기능 중 하나. 이미지 생성 도중 Google Search를 호출해 실시간 사실 데이터를 가져와 인포그래픽·지도·통계 그래프 같은 데이터 기반 이미지의 정확도를 끌어올립니다.

## 언제 사용하나

| 사용 케이스 | Search Grounding 효과 |
|---|---|
| 통계 인포그래픽 | "한국 2026 SNS 사용자 수" → 실시간 검색 결과 반영 |
| 지도·지리 다이어그램 | "서울 지하철 2호선 노선도" → 정확한 역 순서 |
| 시사 일러스트 | "2026년 4월 한국 경제 지표 시각화" → 최신 데이터 |
| 차트·그래프 | "2026 글로벌 AI 시장 규모 도넛 차트" → 출처 검증된 수치 |
| 다이어그램 (역사·과학) | "광합성 과정" → 과학 정확성 |

## 언제 사용하지 않나

| 케이스 | 이유 |
|---|---|
| 일반 제품샷·인물·풍경 | 사실 데이터 불필요, latency만 증가 |
| 일러스트·아트 | 창의성을 제약 |
| 텍스트 없는 이미지 | grounding이 영향 없음 |
| 가상 시나리오 | "2030년 화성 정착지" 같은 미래 가상 case는 grounding이 부적합 |

## 활성화 방법

### Google AI Studio (UI)
- Tools 패널에서 "Use Google Search" 체크박스 활성화.
- "Use Thinking Mode" 도 함께 활성화 권장 (정확도 시너지).

### Vertex AI (API)
```python
from vertexai.preview.generative_models import GenerativeModel, Tool, grounding

model = GenerativeModel("gemini-3-pro-image-preview")
response = model.generate_content(
    "<5-component 프롬프트>",
    tools=[Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())],
    generation_config={"aspect_ratio": "16:9"},
)
```

### Gemini App (consumer)
- 일부 버전에서 "Search context" 토글 제공. 기능 위치는 앱 업데이트에 따라 변동.

## 프롬프트 작성 팁

### 시간 명시
Search가 최신 자료를 가져올 수 있도록:

- ✅ "based on 2026 data"
- ✅ "as reported in Q1 2026"
- ✅ "current statistics from KOSIS as of 2026"
- ❌ "recent data" (모호)

### 출처 우선순위 제시
Gemini가 신뢰할 출처를 명시적으로 지시:

```
A donut chart showing global AI image generation model market
share in 2026. Prioritize data from Gartner, IDC, or Stanford
HAI reports. <composition>. <lighting>. <style>. Display the
percentages and model names verbatim from the source.
```

### 데이터 검증 요청
Gemini가 자신의 출력을 검증하도록 자기-참조 권유:

```
Cross-reference the percentages with at least two sources before
finalizing the visualization.
```

## 한계와 주의

- Search 결과는 **항상 별도 검증** 필요. 모델이 wiki·블로그 등 신뢰도 낮은 출처를 가져올 수 있음.
- 한국어 검색 결과는 영어보다 품질 편차 큼. 중요 데이터는 영어 키워드로 추가 검증.
- Search Grounding은 reasoning latency를 늘림 (기본 대비 30-60% 증가).
- 비용: 추가 reasoning 토큰 + Search API 호출. 비용 민감한 워크플로우에서는 사전 가격 확인.

## 완성 프롬프트 예

### 예 1 — 인포그래픽

```
A horizontal infographic showing the top 5 most-used SNS
platforms in South Korea in 2026 with percentage of users.
Wide composition with clean white background, captured in
flat editorial design style. Soft consistent lighting.
Modern infographic design, sans-serif typography. Each
platform displays its name in Korean and its market share
percentage verbatim from KOSIS 2026 statistics. Cross-reference
data with at least two reliable sources.
```

### 예 2 — 지도

```
A minimalist map of the Seoul Subway Line 2 (Loop Line). Top-
down view, simplified vector style. Soft pastel palette. Modern
transit map aesthetic. Each station name displayed in Korean
verbatim from the official Seoul Metro 2026 information.
Maintain the correct loop sequence and the inner-outer track
distinction.
```

## 출처

- [Google AI for Developers — Gemini 3 Pro Image Preview (Grounding)](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview)
- [Vertex AI — Grounding with Google Search](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- [Google Cloud Blog — Nano Banana prompting guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
