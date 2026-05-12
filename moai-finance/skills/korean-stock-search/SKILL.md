---
name: korean-stock-search
description: |
  KRX(한국거래소) 상장 종목을 검색하고 종목 기본정보·일별 시세를 조회합니다.
  k-skill-proxy 경유로 호출하므로 사용자는 KRX_API_KEY 발급이나 별도 MCP 서버
  설치가 필요 없습니다. read-only 일별 snapshot이며 실시간 호가·체결은 제공하지
  않습니다. 투자 자문이 아닙니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "삼성전자 종목코드", "005930 기본정보", "SK하이닉스 시세"
  - "KOSDAQ 알테오젠 종가/거래량", "코스피 시가총액"
  - "주식 종목 검색", "KRX 상장 종목", "한국 주식 시세"
  - "20260408 종가", "어제 거래량", "전일 등락률"
  - moai-finance의 DART 공시 분석을 보완하는 KRX 시세 데이터 필요 시
user-invocable: true
version: 2.4.0
---

# KRX 한국 주식 검색·시세

KRX(한국거래소) 상장 종목 검색, 종목 기본정보, 일별 시세를 조회합니다. moai-business의 DART(공시)를 보완하는 시세 데이터로 활용합니다.

> 본 스킬은 NomaDamas k-skill `korean-stock-search` (MIT) 기반이며, upstream 설계 참고는 [`jjlabsio/korea-stock-mcp`](https://github.com/jjlabsio/korea-stock-mcp)입니다. `KRX_API_KEY`는 프록시 서버에서만 관리하므로 사용자 발급 불필요.

## When to use / When not to use

**사용**: 종목 검색(이름·코드), 종목 기본정보, 일별 종가·거래량·시가총액, KRX 공식 데이터 기반 단순 시세 조회.

**사용 금지**: 미국·일본·가상자산 등 비한국 주식, 실시간 체결·호가·분봉, 재무제표·공시 원문(→ DART MCP 사용), 투자 자문·매수 추천.

## Inputs

- `q`: 종목명/종목코드 검색어 (search endpoint)
- `market`: `KOSPI` | `KOSDAQ` | `KONEX`
- `code`: 종목코드 (보통 6자리, 예: `005930`)
- `bas_dd`: 기준일 `YYYYMMDD` (없으면 KST 오늘. 휴장일이면 최근 영업일로 재시도)
- `limit`: 검색 결과 수 (기본 10, 최대 20)

## Prerequisites

사용자 측 필수 시크릿 **없음**.

- `KSKILL_PROXY_BASE_URL` (선택): self-host 시
- 운영 측 `KRX_API_KEY`는 프록시 서버 환경에만 둡니다

## Endpoints

```
GET /v1/korean-stock/search?q={검색어}&bas_dd={YYYYMMDD}
GET /v1/korean-stock/base-info?market={KOSPI|KOSDAQ|KONEX}&code={코드}&bas_dd={YYYYMMDD}
GET /v1/korean-stock/trade-info?market={KOSPI|KOSDAQ|KONEX}&code={코드}&bas_dd={YYYYMMDD}
```

## Examples

```bash
# 종목 검색
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/korean-stock/search' \
  --data-urlencode 'q=삼성전자' --data-urlencode 'bas_dd=20260408'

# 종목 기본정보
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/korean-stock/base-info' \
  --data-urlencode 'market=KOSPI' --data-urlencode 'code=005930' \
  --data-urlencode 'bas_dd=20260408'

# 일별 시세
curl -fsS --get 'https://k-skill-proxy.nomadamas.org/v1/korean-stock/trade-info' \
  --data-urlencode 'market=KOSPI' --data-urlencode 'code=005930' \
  --data-urlencode 'bas_dd=20260408'
```

## Response shape

검색:

```json
{
  "items": [
    {
      "market": "KOSPI",
      "code": "005930",
      "standard_code": "KR7005930003",
      "name": "삼성전자",
      "english_name": "Samsung Electronics",
      "listed_at": "1975-06-11"
    }
  ]
}
```

일별 시세:

```json
{
  "item": {
    "market": "KOSPI",
    "code": "005930",
    "base_date": "20260408",
    "name": "삼성전자",
    "close_price": 84000,
    "change_price": 1000,
    "fluctuation_rate": 1.2,
    "open_price": 83000,
    "high_price": 84500,
    "low_price": 82800,
    "trading_volume": 12345678,
    "trading_value": 1030000000000,
    "market_cap": 500000000000000
  }
}
```

## Response policy

- 종목명이 모호하면 먼저 `search`로 시장/종목코드를 좁힌 뒤 `base-info`/`trade-info` 호출.
- 일부 시장 upstream이 실패하면 `upstream.degraded=true` + `failed_markets`를 보고 부분 장애를 함께 설명합니다.
- `trade-info`는 일별 snapshot이며 **실시간 호가·체결처럼 말하지 않습니다**.
- 휴장일·장마감 이전이면 해당 `bas_dd`에 데이터 없을 수 있어 최근 영업일로 재시도합니다.
- 숫자는 사람이 읽기 쉬운 단위(원, 주, 억/조)로 풀어주되 원본 숫자도 유지합니다.
- 답변 말미에 **"KRX 공식 데이터 기준 / 투자 조언 아님"**을 짧게 남깁니다.

## 응답 컴팩트 규칙

- 종목명 / 시장 / 종목코드
- 기준일
- 종가 / 등락률 / 거래량 / 시가총액
- 필요할 때만 상장일 / 상장주식수 / 액면가
- 여러 후보면 상위 3-5개만 보여주고 사용자가 고르게 합니다

## Failure modes

- `q`/`market`/`code`/`bas_dd` 형식 오류 → 400
- 프록시에 `KRX_API_KEY` 없음 → 503
- 일부 시장 upstream 실패 → 200 + `upstream.degraded=true` + `failed_markets`
- 모든 시장 upstream 실패 → 502
- 해당 기준일·시장에 종목 없음 → 404 `not_found`

## 관련 스킬 체이닝

- **before**: `moai-business:investor-relations` — IR 자료 작성 시 KRX 공식 시세 필요
- **before**: DART MCP (`moai-business/.mcp.json`) — 공시·재무 분석과 결합
- **after**: `moai-finance:variance-analysis` — 시세 변동 분석
- **after**: `moai-office:xlsx-creator` — 시세 데이터 엑셀화
- **after**: `moai-bi:executive-summary` — 경영진 1pager에 시세 요약

## Done when

- 검색어가 모호하면 `search`로 후보를 먼저 좁혔다.
- 필요시 `base-info`와 `trade-info`로 핵심 수치를 정리했다.
- 사용자가 `KRX_API_KEY` 없이도 조회 가능하다는 점을 유지했다.
- "KRX 공식 데이터 기준 / 투자 조언 아님"을 답변 말미에 남겼다.

## Notes

- 원본 참고: `https://github.com/jjlabsio/korea-stock-mcp`
- 공식 데이터 출처: KRX Open API (`https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd`)
- 본 스킬은 read-only 조회 전용입니다.