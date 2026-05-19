---
name: commerce-review-aggregator
description: |
  [책임 경계] 멀티채널 리뷰 통합 분석 전담 — 네이버 스마트스토어·쿠팡·자사몰·YouTube·인스타그램 4채널 리뷰 수집 → 감정·키워드·인사이트·액션플랜 4단 분석. 페어 스킬 commerce-voc-triage(VOC 우선순위)와 명확히 구분 — 본 스킬은 리뷰 데이터 통합·분석, 페어는 VOC 처리 우선순위.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "리뷰 분석해줘", "수백 개 리뷰 정리", "감정 분석 리뷰", "쿠팡 리뷰 키워드", "리뷰 인사이트", "AI 리뷰 분석 자동화", "리뷰 액션플랜", "멀티채널 리뷰 통합".
  4단 분석: ① 감정(긍정·부정·중립 비율) ② 키워드(상위 20개) ③ 인사이트(제품·서비스 개선 포인트) ④ 액션플랜(우선순위 액션 5개).
  v2.8.0 신규.
user-invocable: true
version: 2.12.2
---

# 멀티채널 리뷰 통합 분석 (Commerce Review Aggregator)

## 개요

네이버 스마트스토어·쿠팡·자사몰·YouTube·인스타그램 등 멀티채널 리뷰를 통합 수집·분석하여 감정·키워드·인사이트·액션플랜 4단 분석 리포트를 자동 생성하는 전담 스킬입니다.

**책임 한 줄**: 상품 ID 또는 채널별 리뷰 데이터 입력 → 4단 분석 → 미리캔버스 PPT 자동화 출력.

## 4단 분석 프롬프트

### 1단: 감정 분석
- 긍정·부정·중립 비율 (% 단위)
- 강한 감정 표현 추출 ("완전 좋아요" / "정말 별로" 등)
- 시간별 감정 추이 (월별/분기별)

### 2단: 키워드 분석
- 상위 20개 키워드 추출 (빈도순)
- 긍정 키워드 vs 부정 키워드 분류
- 키워드별 빈도 + 대표 문장 1개

### 3단: 인사이트 도출
- 제품 강점 3개 (긍정 키워드 기반)
- 제품 약점 3개 (부정 키워드 기반)
- 서비스(배송·CS) 평가 별도 분리
- 경쟁사 언급 (있는 경우)

### 4단: 액션플랜 우선순위 5개
- 즉각 개선 (1주 내): 단순 정보 보강·CS 응답 개선
- 단기 개선 (1-3개월): 패키징·상세페이지 수정
- 중기 개선 (3-6개월): 제품 리뉴얼·신규 SKU 추가
- 장기 개선 (6개월+): 카테고리 확장·브랜드 전략
- 모니터링 항목: 지속 관찰 필요

## 채널별 수집 가이드

| 채널 | 수집 방법 | 비용 | 자동화 가능성 |
|------|----------|------|-------------|
| 네이버 스마트스토어 | API (네이버 커머스 API) | 무료 (인증 필요) | 자동화 가능 |
| 쿠팡 윙 | Wing API 또는 윙 대시보드 CSV | 무료 (셀러 한정) | 부분 자동화 |
| 자사몰 (카페24/아임웹) | API 또는 어드민 CSV | 무료 | 자동화 가능 |
| YouTube | YouTube Data API | 무료 (한도 내) | 자동화 가능 |
| 인스타그램 | Instagram Graph API (브랜드 계정만) | 무료 | 자동화 가능 |

## 출력 형식

```json
{
  "product": "비건 세럼 50ml",
  "total_reviews": 1247,
  "channels": {"smartstore": 580, "coupang": 412, "self_mall": 255},
  "sentiment": {"positive": 78, "negative": 12, "neutral": 10},
  "top_keywords": [
    {"keyword": "흡수력 좋음", "freq": 234, "polarity": "+"},
    {"keyword": "향이 별로", "freq": 87, "polarity": "-"}
  ],
  "insights": {
    "strengths": ["흡수력·발림성", "비건 인증 신뢰", "용기 디자인"],
    "weaknesses": ["향 호불호", "용량 부족 (50ml)", "가격 부담"],
    "service": "배송 빠름, CS 친절"
  },
  "action_plan": [
    {"priority": 1, "term": "즉각", "action": "상세페이지에 향 정보 보강 (라벤더 향)"},
    {"priority": 2, "term": "단기", "action": "100ml 대용량 SKU 추가"}
  ]
}
```

## 사용 예시

```
"/commerce-review-aggregator — 비건 세럼 50ml, 스마트스토어·쿠팡 통합"
→ 두 채널 리뷰 1,000+ 통합 → 4단 분석 → PPT 자동화
```

## 후속 체인 (텍스트 산출물 검수)

본 스킬의 4단 분석 인사이트·액션플랜·서비스 평가 텍스트는 `moai-core:ai-slop-reviewer`로 자동 후처리 체이닝됩니다 (CLAUDE.local.md §3-2 HARD). 사용자 응대·외부 보고서로 산출하는 모든 텍스트는 AI 슬롭 검수를 거칩니다.

```text
commerce-review-aggregator → ai-slop-reviewer → (선택) pptx-designer
```

## 관련 스킬

- `commerce-voc-triage` — VOC 우선순위 (페어)
- `commerce-channel-message` — 액션플랜 기반 메시지 작성
- `pptx-designer` — 분석 결과 PPT 자동화
- `ai-slop-reviewer` — 텍스트 산출물 AI 슬롭 검수 (자동 체인, HARD)

## SPEC

`.moai/specs/SPEC-REVIEW-AGG-001/spec.md` (v2.8.0 신규)
