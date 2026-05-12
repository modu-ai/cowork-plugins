---
name: real-estate-search
description: |
  국토교통부(MOLIT) 실거래가 신고 데이터를 기반으로 한국 아파트·오피스텔·연립다세대·
  단독다가구·상업업무용 부동산의 실거래가와 전월세 시세를 조회합니다.
  k-skill-proxy.nomadamas.org 경유로 호출하므로 사용자는 별도 API 키가 필요 없습니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "잠실 리센츠 2024년 매매 실거래가 찾아줘", "강남구 아파트 실거래가"
  - "마포구 아파트 전세 실거래", "성수동 오피스텔 월세 실거래"
  - "용산구 상업업무용 건물 거래내역", "강남구 연립다세대 매매"
  - "부동산 실거래가 조회", "MOLIT 실거래가 데이터", "국토부 실거래"
  - "전월세 시세", "전세 보증금 추이", "월세 평균"
  - 단지명 + 거래년월 + 평형 조합으로 시세 분석 요청 시
user-invocable: true
version: 2.4.0
---

# 한국 부동산 실거래가 조회

국토교통부(MOLIT) 실거래가 신고 데이터를 기반으로 매매·전월세 실거래를 조회합니다. 사업·투자 분석, 입지 검토, 자산 평가에 활용합니다.

> 본 스킬은 [`tae0y/real-estate-mcp`](https://github.com/tae0y/real-estate-mcp) (MIT)를 NomaDamas k-skill-proxy 경유로 단순화한 가이드입니다.

## When to use / When not to use

**사용**: 실거래가/전월세 조회, 단지별 시세 추이, 평형별 가격 분포, 지역별 시세 비교.

**사용 금지**: 해외 부동산, 호가/매물 비교(실거래 아님), 세금·등기·중개 법률 자문, 청약홈 분양/당첨 조회.

## Inputs

- `q`: 지역명 (region-code endpoint, 예: `"서울 강남구"`)
- `lawd_cd`: 5자리 법정동 코드 (transaction endpoint, 예: `"11680"`)
- `deal_ymd`: 6자리 거래년월 YYYYMM (예: `"202403"`)
- `num_of_rows`: 조회 건수 (기본 100, 최대 1000)

## Prerequisites

사용자 측 필수 시크릿 **없음**. 인터넷 연결만 있으면 동작합니다.

- `KSKILL_PROXY_BASE_URL` (선택): self-host 프록시 사용 시. 비우면 기본 hosted `https://k-skill-proxy.nomadamas.org` 사용.
- 운영 측 `DATA_GO_KR_API_KEY`는 프록시 서버 환경에만 둡니다.

## Supported endpoints

### 지역코드 조회

```
GET /v1/real-estate/region-code?q={지역명}
```

### 실거래가/전월세 조회

```
GET /v1/real-estate/:assetType/:dealType?lawd_cd={코드}&deal_ymd={년월}
```

| assetType | dealType | 설명 |
|---|---|---|
| `apartment` | `trade` | 아파트 매매 |
| `apartment` | `rent` | 아파트 전월세 |
| `officetel` | `trade` | 오피스텔 매매 |
| `officetel` | `rent` | 오피스텔 전월세 |
| `villa` | `trade` | 연립다세대 매매 |
| `villa` | `rent` | 연립다세대 전월세 |
| `single-house` | `trade` | 단독/다가구 매매 |
| `single-house` | `rent` | 단독/다가구 전월세 |
| `commercial` | `trade` | 상업업무용 매매 |

`commercial/rent`는 미지원.

## Examples

```bash
# 지역코드 조회
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/real-estate/region-code' \
  --data-urlencode 'q=강남구'

# 아파트 매매 실거래가
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/real-estate/apartment/trade' \
  --data-urlencode 'lawd_cd=11680' \
  --data-urlencode 'deal_ymd=202403'

# 오피스텔 전월세
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/real-estate/officetel/rent' \
  --data-urlencode 'lawd_cd=11680' \
  --data-urlencode 'deal_ymd=202403'
```

## Response shape

매매:

```json
{
  "items": [
    {
      "name": "래미안 퍼스티지",
      "district": "반포동",
      "area_m2": 84.99,
      "floor": 12,
      "price_10k": 245000,
      "deal_date": "2024-03-15",
      "build_year": 2009,
      "deal_type": "중개거래"
    }
  ],
  "summary": {
    "median_price_10k": 230000,
    "min_price_10k": 180000,
    "max_price_10k": 310000,
    "sample_count": 42
  }
}
```

전월세는 동일 구조 + `deposit_10k`, `monthly_rent_10k`, `contract_type`. 가격 단위는 만원 (245000 = 24억 5천만원).

## Response policy

- `region-code`로 행정구역 코드를 먼저 확인한 뒤 자산 타입별 endpoint로 조회합니다.
- 사용자가 동·건물명·연월을 덜 줬으면 지역, 단지명, 기준 월을 먼저 보강합니다.
- **실거래가와 호가를 섞어 말하지 않습니다**. 본 스킬은 국토교통부 신고 데이터입니다.
- 답변 말미에 출처(국토교통부 실거래가 신고)를 남깁니다.

## 응답 컴팩트 규칙

- 지역명 + 자산 타입 + 거래년월
- summary.sample_count
- 중위값/최소/최대
- 상위 3-5건 대표 거래 (이름·면적·층·가격·날짜)
- 전월세면 보증금 + 월세 요약

## Failure modes

- `lawd_cd` 또는 `deal_ymd` 형식 오류 → 400
- 프록시 서버에 `DATA_GO_KR_API_KEY` 없음 → 503
- upstream MOLIT API 오류 → 502 + `molit_api_XXX`
- 데이터 없음 → 빈 `items` 배열

## 관련 스킬 체이닝

- **before**: `moai-data:public-data` — 인구·가구 통계로 입지 분석 보조
- **after**: `moai-business:market-analyst` — 시세 데이터 기반 시장 분석
- **after**: `moai-business:investor-relations` → `moai-office:pptx-designer` — 투자 IR 자료
- **after**: `moai-content:landing-page` — 부동산 마케팅 페이지 데이터 입력

## Done when

- 자산 타입에 맞는 endpoint를 선택했다.
- 필요시 `region-code`로 지역코드를 먼저 확인했다.
- 실거래가·전월세 결과를 조회하고 요약했다.
- 출처(국토교통부 실거래가 신고)를 남겼다.