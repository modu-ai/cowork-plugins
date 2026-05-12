---
name: commerce-market-research
description: |
  [책임 경계] 카테고리 시장조사 1장 자동 생성 — 거시·경쟁·검색 3축 리포트. 페어 스킬 moai-research:grant-writer와 명확히 구분 — 본 스킬은 이커머스 셀러 카테고리 진입 판단, 페어는 정책자금 리서치.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "내 카테고리 시장조사 해줘", "경쟁사 동향 알아봐줘", "이 카테고리 진입 검토해줘", "분기 시장 트렌드 뽑아줘", "신상품 카테고리 분석", "쇼핑 트렌드 리서치", "키워드 시장 규모 알아봐줘", "카테고리 기회·위협 분석"
  V6 ① 시장조사 도구 = MCP trend_search · trend_shopping_categories · trend_shopping_keywords · keyword_for_product_idea 4종 wrapper. (SPEC-COMMERCE-V6-003 §5.3 인용)
  ai-slop-reviewer 체이닝 제외 (수치·표 데이터 스킬).
user-invocable: true
version: 2.3.0
---

# 카테고리 시장조사 (Commerce Market Research)

## 개요

이커머스 셀러가 특정 카테고리에 진입하거나 상품을 기획할 때 필요한 거시·경쟁·검색 3축 시장조사 1장 리포트를 자동 생성하는 스킬입니다.

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3):
- `trend_search` — 거시 트렌드 데이터
- `trend_shopping_categories` — 쇼핑 카테고리 성장률
- `trend_shopping_keywords` — 카테고리 핵심 키워드 트렌드
- `keyword_for_product_idea` — 상품 기획 키워드 아이디어

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 위 4종 도구를 호출합니다. MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

**Day 2 시연 시점**: 1교시 10:35–10:55

## 트리거 키워드

시장조사, 카테고리 분석, 경쟁사 동향, 트렌드 리서치, 쇼핑 트렌드, 카테고리 진입, 시장 규모, 키워드 기회, 거시 분석, 경쟁 강도, 상품 기획 리서치, 카테고리 성장률

## 워크플로우

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| 카테고리 | 필수 | "비건 스킨케어", "반려견 간식", "남성 운동복" |
| 가격대 | 권장 | "1~3만원", "5만원 이상" |
| 채널 | 권장 | 스마트스토어, 쿠팡, 자사몰 |
| 기간 | 선택 | "최근 3개월", "1년" (기본값: 최근 3개월) |

### MCP 호출 순서

```
1. trend_search(category, period)
   → 거시 트렌드: 검색량 증감률, 시즌성 패턴

2. trend_shopping_categories(category)
   → 쇼핑 카테고리 성장률, 경쟁 밀도

3. trend_shopping_keywords(category, top_n=20)
   → 상위 20 키워드 + 트렌드 방향

4. keyword_for_product_idea(category, price_range, channel)
   → 상품 기획 기회 키워드 10개
```

### 합격 기준 (PDF §5.5 ⑤ 직접 인용)

| 기준 | 설명 |
|------|------|
| 3축 완성 | 거시·경쟁·검색 각 축 모두 포함 |
| 기회 1줄 | "기회: {구체 기회}" 명시 |
| 위협 1줄 | "위협: {구체 위협}" 명시 |
| 추정 표시 | MCP 데이터 기반이 아닌 추정치는 "(추정)" 명시 |

## 사용 예시

```
"비건 스킨케어 카테고리 시장조사 해줘 — 쿠팡, 1~3만원대"
→ 거시(뷰티 트렌드 성장률) · 경쟁(비건 스킨케어 카테고리 밀도) · 검색(상위 키워드 20개) 3축 리포트 1장 출력

"반려견 간식 시장 분석해줘"
→ 펫푸드 트렌드 + 카테고리 성장률 + 간식 키워드 기회·위협 리포트

"남성 운동복 신상품 기획 위한 시장조사"
→ 스포츠웨어 트렌드 + 경쟁 강도 + 상품 기획 키워드 10개
```

## 출력 형식

```markdown
# 📊 {카테고리} 시장조사 리포트

**조사 기간**: {기간} | **채널**: {채널} | **생성일**: {날짜}

---

## 1. 거시 트렌드 축

| 지표 | 현황 | 전기 대비 |
|------|------|----------|
| 검색량 증감률 | +23% | ↑ 상승세 |
| 시즌 패턴 | 봄·여름 집중 | 4~8월 피크 |
| 거시 키워드 | {상위 3개} | — |

**추정 포함 여부**: {있음/없음} — (추정) 표기 항목: {목록}

---

## 2. 경쟁 분석 축

| 지표 | 현황 | 평가 |
|------|------|------|
| 카테고리 밀도 | 상/중/하 | {설명} |
| 상위 노출 브랜드 | {3~5개} | — |
| 평균 판매가 | {가격대} | — |
| 리뷰 평균 수 | {수치} (추정) | — |

---

## 3. 검색 키워드 축

| 순위 | 키워드 | 트렌드 방향 | 경쟁 강도 |
|------|--------|-----------|----------|
| 1 | {키워드} | ↑/↓/→ | 상/중/하 |
| 2 | {키워드} | ↑/↓/→ | 상/중/하 |
| ... | ... | ... | ... |

**상품 기획 기회 키워드**: {10개 목록}

---

## 결론

**기회**: {구체적 기회 1줄}
**위협**: {구체적 위협 1줄}
**권장 포지셔닝**: {포지셔닝 제안}

> 다음 단계: `commerce-jtbd-persona --mode jtbd`로 JTBD 9개 자동 도출
```

## 합격 기준

PDF §5.5 ⑤ 시장조사 합격 기준:

- **거시·경쟁·검색 3축** 모두 포함
- **기회 1줄 + 위협 1줄** 명시 (구체 수치 또는 근거 포함)
- **추정 표시** 명시 — MCP 실측 데이터와 추정치를 명확히 구분
- **상품 기획 키워드** 최소 5개 이상

## 관련 스킬

체이닝 순서: **commerce-market-research** → `commerce-jtbd-persona --mode jtbd` → `commerce-jtbd-persona --mode persona` → `detail-page-copy --mode diagnose/copy` → `commerce-product-naming` → `commerce-channel-message` → `commerce-integrated-strategy`

- `commerce-jtbd-persona` — 시장조사 결과를 입력으로 JTBD 9개 도출 (다음 단계)
- `commerce-product-naming` — 키워드 기반 상품명 3안 생성
- `commerce-integrated-strategy` — 모든 산출물 종합 전략 1장

## 이 스킬을 사용하지 말아야 할 때

- **정책자금·보조금 리서치**: `moai-research:grant-writer` 사용
- **경쟁사 SNS/콘텐츠 분석**: `moai-content:social-media` 사용
- **특허·기술 동향 리서치**: 별도 전문 리서치 스킬 사용
- **광고 성과 분석 (ROAS)**: `commerce-integrated-strategy` 사용 (MCP dashboard_morning_brief 포함)
