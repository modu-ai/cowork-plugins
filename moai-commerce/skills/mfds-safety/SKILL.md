---
name: mfds-safety
description: |
  식품의약품안전처(MFDS) 공식 OpenAPI를 k-skill-proxy 경유로 조회해 의약품과 식품의
  공식 안전 정보를 확인합니다. 의약품(e약은요·안전상비의약품)과 식품(건강기능식품 원료
  인정현황·개별인정형·품목제조 신고·검사부적합·회수·판매중지)을 통합 조회합니다.

  사용자가 증상·복용/섭취 상황을 말하면 절대 단정하지 않고 인터뷰로 먼저 되묻습니다.
  red flag 발견 시 119·응급실·의료진 안내가 우선합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "타이레놀이랑 판콜 같이 먹어도 돼?", "이 약 부작용 알려줘"
  - "임산부 감기약", "아이 해열제 복용량", "고령자 복용 주의사항"
  - "이 김밥 회수 이력 있어?", "차전자피 먹어도 되나"
  - "건강기능식품 1일 섭취량", "MFDS 공식 정보", "식약처 부적합"
  - "의약품 안전 체크", "식품 안전 체크", "회수·판매중지 식품 검색"
  - 헬스/F&B 커머스에서 상품 안전성 확인 시
user-invocable: true
---

# MFDS 의약품·식품 안전 체크 (통합)

식품의약품안전처(MFDS) 공식 OpenAPI를 통해 의약품과 식품의 안전 정보를 확인합니다. 헬스·F&B 커머스 상품 검수, 소비자 안전 안내, 회수·부적합 이력 확인에 사용합니다.

> 본 스킬은 NomaDamas k-skill의 `mfds-drug-safety` + `mfds-food-safety` (MIT)를 통합 정리했습니다.

## Mandatory interview first — red flag 우선

증상·복용/섭취 상황이 언급되면 결론을 말하기 전에 **반드시 먼저 되묻습니다**.

권장 첫 질문:
- 누가 (본인/아이/임산부/고령자), 무엇을 언제 얼마나, 같이 먹은 음식·술·약, 현재 증상, 기저질환·알레르기
- **red flag**: `호흡곤란`, `의식저하`, `입술·혀 붓기`, `심한 발진`, `혈변`, `심한 탈수`, `심한 복통/고열`, `지속되는 구토/흉통`

red flag 가 하나라도 있으면 **API 조회보다 즉시 119·응급실·의료진 연결**을 우선 안내합니다.

## When to use

**의약품**:
- "이 약이랑 이 약 같이 먹어도 되니?"
- "타이레놀 먹는 중인데 판콜 같이 먹어도 돼?"
- "두드러기가 있는데 이 약 계속 먹어도 되나?"
- 식약처 공식 약 정보로 효능·주의사항 확인

**식품**:
- "이 음식 먹어도 괜찮니?" → 건강기능식품 원료 인정현황 + 검사부적합
- "차전자피 1일 섭취량 알려줘" → 기능성 원료 인정현황
- "이 김밥 먹고 배 아픈데 회수 이력 있어?" → 회수·부적합 목록
- 헬스/F&B 커머스에서 신상품 안전성 확인

## When not to use

- 진단·처방·복용 지시
- 식중독 진단, 섭취 허가/금지 최종 판정
- red flag 또는 고위험군의 응급 상황 (의료진 우선)

## Prerequisites

사용자 측 필수 시크릿 **없음**.

- `KSKILL_PROXY_BASE_URL` (선택): self-host 시
- 운영 측: `DATA_GO_KR_API_KEY` (의약품 + 부적합), `FOODSAFETYKOREA_API_KEY` (건강기능식품 + 회수 live) — 프록시 서버에만 둡니다
- `FOODSAFETYKOREA_API_KEY` 발급: `https://www.foodsafetykorea.go.kr` 회원가입 → OpenAPI 이용신청. 키 1개로 I-0040, I-0050, I0030, I0490, I2620 모두 사용

## Workflow

### A. 의약품 안전 체크

1. 증상/복용 상황이 있으면 **인터뷰 먼저**.
2. red flag 하나라도 있으면 **즉시 응급 안내로 전환**.
3. 약 이름이 확인되면 `/v1/mfds/drug-safety/lookup` 으로 e약은요·안전상비의약품 조회.
4. 효능·사용법·주의사항·상호작용·이상반응·보관법을 짧게 정리.
5. "같이 먹어도 되나?"는 **공식 상호작용 문구만** 근거. 최종 판단은 약사·의료진.

### B. 식품 안전 체크

1. 증상/섭취 상황이 있으면 **인터뷰 먼저**.
2. red flag → **즉시 응급 안내**.
3. "이거 먹어도 되나?" 흐름:
   - `/v1/mfds/food-safety/product-report` → 건강기능식품 품목제조 신고사항(원재료·기능성·섭취 주의·기준규격, 고시형 원료 포함)
   - `/v1/mfds/food-safety/health-food-ingredient` → 기능성 원료 인정현황(개별인정형 1일 섭취량·주의사항)
   - `/v1/mfds/food-safety/inspection-fail` → 국내 검사부적합 이력
   - `/v1/mfds/food-safety/search` → 회수·부적합 공개 목록
4. 제품명·업체명·기능성·섭취량·주의사항·부적합 사유를 짧게 정리. **먹어도 되는지 단정하지 않습니다**.
5. 프록시가 `FOODSAFETYKOREA_API_KEY` 없이 동작하면 결과가 sample feed 기반일 수 있음을 warnings로 확인.

## Endpoints

| 카테고리 | Endpoint |
|---|---|
| 의약품 통합 | `GET /v1/mfds/drug-safety/lookup` |
| 식품 회수·부적합 | `GET /v1/mfds/food-safety/search` |
| 건강기능식품 원료 | `GET /v1/mfds/food-safety/health-food-ingredient` |
| 건강기능식품 품목제조 | `GET /v1/mfds/food-safety/product-report` |
| 검사부적합 | `GET /v1/mfds/food-safety/inspection-fail` |

## Official surfaces

- e약은요: `https://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList`
- 안전상비의약품: `https://apis.data.go.kr/1471000/SafeStadDrugService/getSafeStadDrugInq`
- 식품안전나라 (I-0040/I-0050/I0030/I0490/I2620): `https://www.foodsafetykorea.go.kr/api/openApiInfo.do`
- 부적합 식품: `https://apis.data.go.kr/1471000/PrsecImproptFoodInfoService03/getPrsecImproptFoodList01`

## Response policy

- 본 스킬은 **진단·처방·복용 지시**를 하지 않습니다.
- 공식 문서에 있는 효능·주의·상호작용·기능성 문구만 근거로 요약합니다.
- 상호작용 문구가 모호하거나 red flag 가 있으면 약사·의사 상담으로 넘깁니다.
- 증상이 있는 질문은 **인터뷰 없이 바로 답하지 않습니다**.
- 회수·부적합 결과가 sample feed면 그 사실을 명시합니다.

## 관련 스킬 체이닝

- **before**: `moai-commerce:commerce-strategy` — 헬스/F&B 신상품 기획 시 안전성 검토
- **after**: `moai-commerce:detail-page-copy` — 안전 정보 반영한 상세페이지 카피
- **after**: `moai-content:product-detail` — 안전성 안내 콘텐츠 작성

## Done when

- 증상 또는 복용/섭취 상황을 먼저 되물었다.
- red flag 여부를 확인했다.
- 프록시 route를 통해 공식 endpoint 조회 결과를 JSON으로 정리했다.
- 의약품: 제품명·업체명·효능·주의·상호작용 요약 / 식품: 제품명·업체명·기능성·섭취량·주의·부적합 사유 요약을 제공했다.
