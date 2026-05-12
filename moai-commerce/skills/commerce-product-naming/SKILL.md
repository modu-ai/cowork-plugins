---
name: commerce-product-naming
description: |
  [책임 경계] 상품명 3안 자동 생성 + 플랫폼 검증 (스마트스토어·쿠팡·네이버쇼핑 25자·금지어). 페어 스킬 moai-domain-copywriting과 명확히 구분 — 본 스킬은 상품 등록용 상품명(SEO 최적화), 페어는 광고·마케팅 카피.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "상품명 뽑아줘", "상품명 3개 안 만들어줘", "키워드 넣어서 상품명", "스마트스토어 상품명 최적화", "쿠팡 상품명 금지어 체크", "검색 최적화 상품명", "브랜드 상품명 후보", "CTR 높은 상품명"
  V6 ④ 상품명 도구 = MCP keyword_search_volume · keyword_related · keyword_bulk_research 3종 wrapper. (SPEC-COMMERCE-V6-003 §5.3 인용)
  공식 4요소: [브랜드] + [카테고리] + [키워드] + [차별점(선택)]. 3안 매핑 카테고리: 검색 최적화 / CTR 최적화 / 브랜드 강화.
  금지 키워드 9종: 최저가·1위·베스트·재입고·인기상품·정품·당일배송·무료배송·특가.
  ai-slop-reviewer 체이닝 제외 (검증 룰 통과 데이터 스킬).
  v2.4.0 강화 (자료 1 정해준 강사 강의 자료 §4 상품명 전략 반영).
user-invocable: true
version: 2.4.0
---

# 상품명 자동 생성 (Commerce Product Naming)

## 개요

JTBD와 상품 정보를 기반으로 이커머스 플랫폼 최적화 상품명 3안(검색형·CTR형·브랜드형)을 자동 생성하고, 스마트스토어·쿠팡·네이버쇼핑 길이 규정 및 금지어 통과 여부를 자동 검증하는 스킬입니다.

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3):
- `keyword_search_volume` — 키워드 월간 검색량 조회
- `keyword_related` — 연관 키워드 확장
- `keyword_bulk_research` — 복수 키워드 일괄 조사 (검색량, 경쟁도, CPC)

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 위 3종 도구를 호출합니다. MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

**Day 2 시연 시점**: 5교시 15:25–16:00

## 트리거 키워드

상품명, 상품명 생성, 키워드 상품명, SEO 상품명, 스마트스토어 상품명, 쿠팡 상품명, 네이버쇼핑 상품명, 금지어 체크, 25자 제한, 검색 최적화, CTR 상품명, 브랜드 상품명, 상품명 후보

## 워크플로우

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑥ JTBD 결과 | 권장 | commerce-jtbd-persona --mode jtbd 산출물 |
| 상품 정보 | 필수 | 상품명(임시), USP, 카테고리, 소재/성분 |
| 우선 채널 | 필수 | 스마트스토어 / 쿠팡 / 네이버쇼핑 / 자사몰 |
| 브랜드명 | 선택 | 브랜드명 포함 여부 |

### MCP 호출 순서

```
1. keyword_search_volume(candidate_keywords[])
   → 후보 키워드 검색량 순위 확인

2. keyword_related(top_keyword)
   → 상위 키워드 연관어 확장 (롱테일 발굴)

3. keyword_bulk_research(candidate_list)
   → 일괄: 검색량·경쟁도·CPC → 3안 선정 근거 데이터
```

### 상품명 공식 (자료 1 §4)

```
[브랜드명] + [카테고리] + [키워드] + [차별점](선택)
   ↑         ↑           ↑          ↑
  TM       카테고리명    주요 검색어   용량·색상·인증 등
  브랜드     주요 검색어   차별화 요소  고객 니즈 직결
  인지도     포함        강조        충족
```

**적용 예시**:

| 분류 | 브랜드 | 카테고리 | 키워드 | 차별점 | 결과 |
|------|--------|----------|--------|--------|------|
| 화장품 | 네이처리퍼블릭 | 알로에 | 수딩젤 | 대용량 | 네이처리퍼블릭 알로에 수딩젤 대용량 |
| 가전제품 | 삼성전자 | 냉장고 | 비스포크 | 4도어 | 삼성전자 비스포크 냉장고 4도어 |
| 식품 (검색형) | (무농약) | 국내산 유기농 귀리 100% | 슈퍼푸드 그래놀라 시리얼 | — | [무농약] 국내산 유기농 귀리 100% 슈퍼푸드 그래놀라 시리얼 |
| 식품 (CTR형) | (다이어트 필수) | 한국산 오트밀 그래놀라 | 체중관리 시리얼 | 아침대용 | [다이어트 필수] 한국산 오트밀 그래놀라 체중관리 시리얼 아침대용 |
| 식품 (브랜드형) | (HACCP인증) | 국내농가 직거래 친환경 유기농 귀리 | 그래놀라 | 450g | [HACCP인증] 국내농가 직거래 친환경 유기농 귀리 그래놀라 450g |

### 상품명 3안 생성 로직 (매핑 카테고리)

| 3안 유형 | 매핑 카테고리 | 핵심 전략 | 우선 타겟 |
|---------|--------------|----------|----------|
| **검색형** | 검색 최적화 | 월간 검색량 상위 키워드 2~3개 조합 | 신규 셀러·신상품 초기 노출 |
| **CTR형** | CTR 최적화 | 브래킷[]표시·후킹 수식어 + 니즈 직접 표현 | 노출은 충분, 클릭률 개선 필요 |
| **브랜드형** | 브랜드 강화 | 브랜드명·인증·원산지 강조 | 충성 고객 타겟·재구매 유도 |

### 플랫폼 검증 (REQ-V6-012)

| 플랫폼 | 최대 길이 | 금지어 카테고리 | 검증 결과 |
|--------|----------|----------------|---------|
| 스마트스토어 | 100자 (권장 25자 이내) | 최저가·공식·정품·1+1(단독표기) 등 | PASS/FAIL |
| 쿠팡 | 100자 (권장 25자 이내) | 최대할인·독점·공짜·무료배송(단독) 등 | PASS/FAIL |
| 네이버쇼핑 | 40자 | 허위·과장·최저가 등 | PASS/FAIL |

**제약 (REQ-V6-012 HARD)**: 핵심 키워드 포함 25자 이내 권장 + 금지어 통과 필수.

### 금지 키워드 9종 (자료 1 §4) — 모든 플랫폼 공통

다음 키워드는 검색엔진·플랫폼 정책에 의해 제한되거나 페널티를 받을 수 있습니다:

| 분류 | 금지 키워드 |
|------|------------|
| **순위·평가성** | 최저가, 1위, 베스트, 인기상품 |
| **재고·물류성** | 재입고, 당일배송, 무료배송, 특가 |
| **품질 단정성** | 정품 |

> **예외**: 위 키워드가 **사실에 기반한 인증·실측 결과**일 경우(예: 공정거래위원회 가격비교 1위 인증, 공식 인증 정품 마크 첨부)에는 사용 가능합니다. 단, 객관적 증명자료가 없으면 금지.

### 상품명 주의사항 4종 (자료 1 §4)

| 주의사항 | 설명 | 영향 |
|---------|------|------|
| **검색어 과다 삽입** | 같은 검색어를 반복적으로 넣어 부자연스럽게 만드는 것 | 검색 결과에 오히려 부정적 영향 |
| **경쟁사 상품명 도용** | 경쟁사의 고유 상품명·등록 상표 무단 사용 | 법적 문제 (상표권 침해) |
| **길이 제한 초과** | 너무 긴 상품명은 모바일에서 잘리고 가독성↓ | 플랫폼별 제한 길이 준수 필수 |
| **과장된 표현** | 객관적으로 증명할 수 없는 "완벽한·최고의" 등 | 소비자 신뢰도 저하 + 광고심의 위반 |

---

## 사용 예시

```
"/commerce-product-naming 비건 스킨케어 세럼, JTBD 결과 첨부, 스마트스토어 우선"
→ 검색형: "비건 세럼 수분 진정 50ml 무향 민감성"
   CTR형: "피부과 처방 없이 집에서 진정 — 비건 세럼"
   브랜드형: "클린루트 비건 세럼 히알루론산 나이아신아마이드"
   검증: 스마트스토어 PASS / 쿠팡 PASS / 네이버쇼핑 PASS

"/commerce-product-naming 반려견 관절 간식, 쿠팡 우선"
→ 3안 생성 + 플랫폼 금지어 검증
```

## 출력 형식

```json
{
  "product_base": "{임시 상품명}",
  "channel_priority": "스마트스토어",
  "keyword_data": {
    "top_search_volume": [
      {"keyword": "비건 세럼", "monthly_volume": 45000, "competition": "중"},
      {"keyword": "수분 세럼", "monthly_volume": 89000, "competition": "상"}
    ],
    "long_tail": ["민감성 비건 세럼", "무향 수분 세럼", "성분 깨끗한 세럼"]
  },
  "proposals": [
    {
      "type": "검색형",
      "name": "비건 세럼 수분 진정 50ml 무향 민감성",
      "length": 20,
      "core_keyword": "비건 세럼",
      "rationale": "월 검색량 45,000 상위 키워드 2개 조합",
      "validation": {
        "smartstore": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "coupang": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "naver_shopping": {"result": "PASS", "length_ok": true, "prohibited_words": []}
      }
    },
    {
      "type": "CTR형",
      "name": "피부과 없이 집에서 진정 비건 세럼 50ml",
      "length": 21,
      "core_keyword": "진정 세럼",
      "rationale": "후킹 수식어 + 니즈 직접 표현 → CTR 최적화",
      "validation": {
        "smartstore": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "coupang": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "naver_shopping": {"result": "PASS", "length_ok": true, "prohibited_words": []}
      }
    },
    {
      "type": "브랜드형",
      "name": "클린루트 비건세럼 히알루론산 나이아신아마이드",
      "length": 24,
      "core_keyword": "비건세럼",
      "rationale": "브랜드 인지도 + 성분 명시 → 충성 고객 타겟",
      "validation": {
        "smartstore": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "coupang": {"result": "PASS", "length_ok": true, "prohibited_words": []},
        "naver_shopping": {"result": "PASS", "length_ok": true, "prohibited_words": []}
      }
    }
  ],
  "recommended": "검색형",
  "recommendation_reason": "신규 셀러·신상품 초기 노출 최대화 권장"
}
```

## 합격 기준

PDF §5.5 ⑨ 합격 기준:

- **3안 유형** 모두 포함: 검색·CTR·브랜드형 각 1개
- **금지어 통과**: 3개 플랫폼 전체 PASS
- **25자 이내**: 핵심 키워드 포함 상태에서 권장 25자 이하
- **키워드 근거**: 검색량 데이터 기반 상품명 선정 근거 명시

## 관련 스킬

체이닝 순서: `commerce-jtbd-persona --mode jtbd` → **commerce-product-naming** → `commerce-channel-message` → `commerce-integrated-strategy`

- `commerce-jtbd-persona --mode jtbd` — ⑥ JTBD (이전 단계, 상품명 방향성 입력)
- `commerce-channel-message` — ⑨ 상품명 확정 후 채널별 메시지 15종 생성 (다음 단계)
- `commerce-integrated-strategy` — 상품명 포함 전략 1장 종합

## 이 스킬을 사용하지 말아야 할 때

- **광고 카피·헤드라인 생성**: `moai-domain-copywriting` 또는 `detail-page-copy` 사용
- **브랜드 네이밍 (회사명·서비스명)**: `moai-domain-brand-design` 사용
- **태그·검색어 등록 최적화**: 플랫폼별 SEO 스킬 (`commerce-marketplace-*`) 사용
- **도메인·앱 이름 생성**: 별도 네이밍 프로세스 활용
