---
name: commerce-jtbd-persona
description: |
  [책임 경계] 1스킬 2모드 — `--mode jtbd`: JTBD 9개 + 시장 매칭 우선순위 자동 도출 / `--mode persona`: 리뷰·Q&A 분석 기반 페르소나 3명 자동 생성. 페어 스킬 moai-domain-copywriting과 명확히 구분 — 본 스킬은 고객 분석(Why), 페어는 카피 작성(What).
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "JTBD 분석해줘", "고객이 왜 사는지 분석", "구매 동기 9개 뽑아줘", "페르소나 만들어줘", "타겟 고객 프로필 생성", "리뷰 분석해서 페르소나", "고객 여정 분석", "구매결정요인 뽑아줘"
  V6 ② 고객분석 도구 = MCP review_list_naver · review_list_cafe24 · qna_list_cafe24 3종 wrapper + ⑤ 시장조사 입력 연계. (SPEC-COMMERCE-V6-003 §5.3 인용)
  ai-slop-reviewer 자동 체이닝 (--mode persona 텍스트 산출물).
user-invocable: true
version: 2.3.0
---

# JTBD + 페르소나 분석 (Commerce JTBD & Persona)

## 개요

V6 ② 고객분석 도구를 감싸는 1스킬 2모드 스킬입니다. 이커머스 셀러가 고객의 구매 동기(JTBD)와 구체적인 페르소나를 데이터 기반으로 자동 생성합니다.

**V6 ↔ MCP 매핑** (SPEC-COMMERCE-V6-003 §5.3):
- `review_list_naver` — 네이버 쇼핑 리뷰 수집
- `review_list_cafe24` — 카페24 자사몰 리뷰 수집
- `qna_list_cafe24` — 카페24 Q&A 수집
- + ⑤ 시장조사 결과 (commerce-market-research 산출물) 입력 연계

**MCP 백엔드**: 본 스킬은 MoAI-Commerce MCP Phase 1 (SPEC-COMMERCE-MCP-002)의 위 3종 도구를 호출합니다. MCP 미출시 시점에는 강사 본인 워크스페이스 사전 녹화 영상 5분으로 시연 대체 (PDF §4 운영 노트 §S4 인용).

**Day 2 시연 시점**: 2교시 11:20–11:30 (JTBD), 3교시 13:25–13:50 (페르소나)

## 트리거 키워드

JTBD, 고객 동기, 구매 이유, 잡스 투 비 던, 기능적 동기, 감성적 동기, 사회적 동기, 페르소나, 타겟 고객 프로필, 리뷰 분석, 구매결정요인, 고객 여정, 니즈 분석, 불만 분석

## 모드 선택

| 모드 | 플래그 | 시연 교시 | 핵심 산출물 |
|------|--------|----------|-----------|
| JTBD 도출 | `--mode jtbd` | Day2 2교시 | JTBD 9개 + 시장 매칭 우선순위 |
| 페르소나 생성 | `--mode persona` | Day2 3교시 | 페르소나 3명 (8필드) |

모드 미지정 시: `--mode jtbd` 먼저 실행 후 `--mode persona` 연속 실행 권장.

---

## 워크플로우 — mode=jtbd

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑤ 시장조사 결과 | 필수 | commerce-market-research 산출물 .md 파일 경로 |
| 상품 정보 | 필수 | 상품명, USP, 카테고리 |
| 채널 | 선택 | 스마트스토어, 쿠팡 (기본값: 전체) |

### MCP 호출 순서 (mode=jtbd)

```
⑤ 시장조사 결과 로드 (입력)
  ↓
분석: 기능적 동기 3개 (Functional Job)
      감성적 동기 3개 (Emotional Job)
      사회적 동기 3개 (Social Job)
  ↓
시장 매칭: 각 JTBD × 시장조사 키워드 교차 → 우선순위 1축 산출
```

---

## 워크플로우 — mode=persona

### 입력 슬롯

| 항목 | 필수 여부 | 예시 |
|------|----------|------|
| ⑥ JTBD 9개 | 필수 | mode=jtbd 산출물 |
| 쇼핑몰 URL / 상품 ID | 권장 | 네이버 스마트스토어 또는 카페24 상품 URL |
| 리뷰 최소 건수 | 자동 | 10건 (부족 시 fallback 자동 적용) |

### MCP 호출 순서 (mode=persona)

```
1. review_list_naver(product_url or search_keyword, min=10)
   → 네이버 리뷰 수집

2. review_list_cafe24(product_id, min=10)
   → 카페24 리뷰 수집

3. qna_list_cafe24(product_id)
   → Q&A 수집 (구매 전 불안·질문 패턴)

4. ⑥ JTBD 교차 분석
   → 리뷰+Q&A × JTBD → 페르소나 군집 3개 분류
```

### Fallback 규칙 (REQ-V6-010)

**리뷰 10건 미만 시 자동 적용:**

```
WHILE 본인 상품 리뷰 < 10건:
  → 같은 카테고리 상위 노출 상품 1개의 리뷰 10건으로 대체
  → 출력 시 "(대체 데이터: {상품명} 리뷰 기반)" 명시
```

### ai-slop-reviewer 자동 체이닝 (HARD)

mode=persona 산출물은 텍스트 페르소나 프로필이므로 `moai-core:ai-slop-reviewer`를 자동 체인합니다.

검수 항목:
- AI 특유 서술 패턴("~한 분", "~을 추구하는") 자연어화
- 페르소나 이름·직업 클리셰 제거
- 구체 수치 및 실제 행동 패턴 기반 서술로 조정

---

## 사용 예시

```
"/commerce-jtbd-persona --mode jtbd 비건 스킨케어 상품, 시장조사 결과 첨부"
→ 기능적(성분 안전성, 피부 개선, 흡수율) × 감성적(자기관리 만족감, 클린 라이프스타일, 죄책감 없는 소비) × 사회적(지속가능 소비 표현, 미닝아웃, 또래 추천) JTBD 9개 + 우선순위

"/commerce-jtbd-persona --mode persona"
→ 메인 페르소나: 박지연(32세, 직장인, ...) + 보조 1: ... + 보조 2: ...
→ 마지막에 ai-slop-reviewer 자동 검수

"/commerce-jtbd-persona 반려견 간식 — JTBD부터 페르소나까지 한 번에"
→ JTBD 9개 → 페르소나 3명 순차 실행
```

## 출력 형식

### mode=jtbd 출력

```json
{
  "mode": "jtbd",
  "product": "{상품명}",
  "jtbd": {
    "functional": [
      {"id": "F1", "job": "JTBD 내용", "market_keyword": "매핑 키워드", "priority": 1},
      {"id": "F2", "job": "...", "market_keyword": "...", "priority": 2},
      {"id": "F3", "job": "...", "market_keyword": "...", "priority": 3}
    ],
    "emotional": [
      {"id": "E1", "job": "...", "market_keyword": "...", "priority": 1},
      {"id": "E2", "job": "...", "market_keyword": "...", "priority": 2},
      {"id": "E3", "job": "...", "market_keyword": "...", "priority": 3}
    ],
    "social": [
      {"id": "S1", "job": "...", "market_keyword": "...", "priority": 1},
      {"id": "S2", "job": "...", "market_keyword": "...", "priority": 2},
      {"id": "S3", "job": "...", "market_keyword": "...", "priority": 3}
    ]
  },
  "market_match_priority": ["F1", "E2", "S1", "F2", "E1", "S3", "F3", "E3", "S2"]
}
```

### mode=persona 출력

```json
{
  "mode": "persona",
  "data_source": "본인 리뷰 {N}건 | 대체 데이터 여부: {없음/있음}",
  "personas": [
    {
      "role": "메인",
      "name": "이름",
      "age": 32,
      "job": "직업",
      "daily_life": "일상 묘사 (2~3문장)",
      "needs": "핵심 니즈",
      "frustrations": "주요 불만",
      "values": "가치관",
      "purchase_decision": "구매결정요인 (상위 3개)"
    },
    {
      "role": "보조1",
      "name": "...",
      "...": "..."
    },
    {
      "role": "보조2",
      "name": "...",
      "...": "..."
    }
  ],
  "slop_review": {
    "status": "passed",
    "changes_made": 0,
    "notes": "ai-slop-reviewer 검수 결과"
  }
}
```

## 합격 기준

PDF §5.5 ⑥⑦ 합격 기준:

**mode=jtbd (⑥)**:
- 기능·감성·사회 각 3개씩 총 9개 JTBD 완성
- 시장 기회 매칭 우선순위 1축 명시 (market_match_priority 배열)

**mode=persona (⑦)**:
- 페르소나 3명 (메인 1 + 보조 2)
- 8필드 모두 채움: 이름·나이·직업·일상·니즈·불만·가치관·구매결정요인
- ai-slop-reviewer 검수 흔적 (slop_review 블록)

## 관련 스킬

체이닝 순서: `commerce-market-research` → **commerce-jtbd-persona --mode jtbd** → **commerce-jtbd-persona --mode persona** → `detail-page-copy --mode copy` → `commerce-product-naming` → `commerce-channel-message`

- `commerce-market-research` — ⑤ 시장조사 1장 (이전 단계, mode=jtbd 입력)
- `detail-page-copy --mode copy` — ⑥⑦ 페르소나 기반 카피 2세트 생성
- `commerce-product-naming` — ⑥ JTBD 기반 상품명 3안
- `commerce-channel-message` — ⑥⑦ 기반 NCM 채널별 메시지 15종

## 이 스킬을 사용하지 말아야 할 때

- **카피 작성 (Why 아닌 What)**: `moai-domain-copywriting` 또는 `detail-page-copy` 사용
- **브랜드 아이덴티티 설계**: `moai-domain-brand-design` 사용
- **광고 타겟팅 설정 (실집행)**: 광고 플랫폼 직접 사용 (본 캠프 외 영역, PDF §1.3)
- **정성 인터뷰 / UX 리서치**: 별도 사용자 리서치 프로세스 활용
