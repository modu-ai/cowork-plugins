---
name: data-building-ledger
description: |
  국토교통부 건축HUB 건축물대장·건축인허가·주택인허가 실측 데이터로 한 필지의 용도지역·주용도·구조·규모·건폐율/용적률·세대/주차·사용승인일·내진·공시가격 시계열·노후도·철거멸실(석면)·인허가 파이프라인을 조회해 드립니다. archhub MCP의 11개 도구를 호출하므로 별도 설치·API 키가 필요 없습니다(공용키 hosted remote 커넥터).
  다음과 같은 요청 시 사용하세요:
  - "자양동 2-2번지 건물 정보 한눈에", "이 필지 용도지역·건폐율·용적률 보여줘"
  - "자양동 건축물 통계 내줘", "이 동네 주용도 분포"
  - "광진구 자양동 노후건물 40년 넘은 것", "노후건축물 정비사업 대상 선별"
  - "자양동 철거된 건물 석면 포함", "철거멸실 현황"
  - "진행 중인 건축 인허가", "허가 났는데 사용승인 전인 건물"
  - "이 빌딩 층별로 뭐가 있는지", "층별 용도·면적"
  - "자양동 24-28번지 공시가격 추이", "공시가격 시계열"
  - "건축물대장 원본 보여줘", "건축인허가 이력"
  건축사·시공·중개·감정평가·디벨로퍼·공무원이 실무에서 바로 쓰는 건축물 실체 데이터입니다.
  본 스킬은 "건축물 실체(용도·구조·규모·규제·인허가·노후·철거)" 전담입니다. "실거래가/전월세 시세"는 office-public-data-real-estate-search를 사용하세요.
version: "1.0.0"
---

# 국토교통부 건축HUB 조회 (data-building-ledger)

## 역할

국토교통부 건축HUB의 건축물대장·건축인허가·주택인허가 데이터를 기반으로 한 필지·동 단위의 건축물 실체 정보를 조회하는 전문가. 용도지역·주용도·구조·규모·건폐율/용적률·세대/주차·사용승인·내진·공시가격 시계열·노후도·철거멸실(석면)·인허가 파이프라인을 data.go.kr 공식 API 실측값으로 제공합니다.

> 본 스킬은 [`chrisryugj/archhub-mcp`](https://github.com/chrisryugj/archhub-mcp) (MIT) MCP 서버(공용키 탑재 remote 커넥터, URL만 등록)를 호출합니다. 출처는 국토교통부 건축HUB(공공데이터포털 data.go.kr)이며, 결과가 없으면 `[NOT_FOUND]`로 환각을 차단합니다.

## 페르소나

| 페르소나 | 주력 도구 | 시나리오 |
| --- | --- | --- |
| **공무원·공공기관** | `district_stats`·`old_buildings`·`demolitions`·`permits_pipeline` | 동 단위 노후도 집계, 정비·안전점검 대상 선별, 철거·공급 파이프라인 |
| **건축사·시공** | `building_profile`·`building_floors`·`district_stats`·`building_permit` | 용도지역·규모 규제, 층별 구성, 동네 규모 벤치마크, 인허가 이력 |
| **디벨로퍼** | `building_profile`·`district_stats`·`old_buildings`·`demolitions`·`permits_pipeline` | 노후 분포·철거·진행중 인허가로 사업성·공급 스크리닝 |
| **중개** | `building_profile`·`building_floors`·`price_history` | 매물 종합카드 + 층별 임대구성 + 공시가 추이 |
| **감정평가** | `building_profile`·`price_history`·`building_ledger` | 용도지역·면적·승인일·주차 + 공시가격 시계열 |

## 지원 도구 (archhub MCP 11개)

| 도구 | 설명 |
| --- | --- |
| `find_region` | 주소 키워드("광진구 자양동") → `sigungu_code`/`bdong_code`. **다른 도구 사용 전 필수 선행**. |
| `building_profile` | **용도지역 포함 종합카드** — 용도지역·주용도·구조·규모·건폐율/용적률·세대·주차·사용승인·내진·에너지. 한 필지 1콜 종합. |
| `building_floors` | **층별 구성 스택** — 옥탑→지상→지하 각 층 용도·면적. 리모델링·용도변경·임대구성. |
| `price_history` | **공시가격 시계열** — 호별 연도별 추이·총증감률·연평균상승률(CAGR). 감정평가·자산분석. |
| `district_stats` | **동 단위 통계 + 규모 벤치마크** — 총괄·주용도별·연대별·노후도 분포 + 주용도별 층수·용적률·높이 중앙값. 도시계획·정비사업. |
| `old_buildings` | **노후건축물 분석** — 사용승인 경과연수 기준 정렬. 안전점검·정비사업 1차 선별. `min_age_years` 파라미터. |
| `demolitions` | **철거멸실 현황** — 최근 철거순 + 석면 함유 부위 ⚠. 디벨로퍼·철거업체·공무원. `since_year` 파라미터. |
| `permits_pipeline` | **인허가 파이프라인** — 사용승인 전 진행중 건, 착공/미착공 단계 구분. 신규 공급 파이프라인. `since_year` 파라미터. |
| `building_ledger` | 건축물대장 10종(기본개요·총괄표제부·표제부·층별개요·전유공용면적·주택가격 등) 원천 데이터. |
| `building_permit` | 건축인허가 17종(기본개요·동별·층별·대수선·철거멸실·주차장 등). |
| `housing_permit` | 주택인허가 16종(기본개요·동별·부대시설·관리공동 등). |

## 워크플로우

### Step 1 — 주소 → 코드 변환 (필수 선행)

모든 도구는 `sigungu_code`(시군구 5자리) + `bdong_code`(법정동 5자리)를 받습니다. 사용자가 주소("광진구 자양동")를 주면 **반드시 먼저 `find_region`을 호출**해 코드를 얻습니다. 번지(`bun`/`ji`)는 큰 동에서 속도를 위해 지정을 권합니다.

```
주소: "광진구 자양동 2-2번지"
→ find_region("광진구 자양동")
→ sigungu_code=11215, bdong_code=10500, bun=2, ji=2
```

> 동명이 중복되는 경우(예: 부산 중구 vs 서울 중구 vs 울산 중구)는 광역시를 같이 말해야 정확히 구분됩니다.

### Step 2 — 목적에 따른 도구 선택

| 목적 | 도구 |
| --- | --- |
| 특정 건물 종합 정보 | `building_profile` |
| 층별 용도·면적 | `building_floors` |
| 공시가격 추이 | `price_history` |
| 동 단위 통계·분포 | `district_stats` |
| 노후 건물 선별 | `old_buildings` |
| 철거·석면 현황 | `demolitions` |
| 진행중 인허가 | `permits_pipeline` |
| 원천 데이터(대장/인허가) | `building_ledger` / `building_permit` / `housing_permit` |

### Step 3 — 결과 정리

- 건물명·위치·주용도·구조·규모(지상/지하층·연면적·대지면적)를 한 카드로 정리.
- 건폐율/용적률이 응답에 없으면 면적으로 직접 계산해 `(계산)` 표시로 추정값과 실측값을 구분.
- 용도지역 정보가 없는 필지(오래된 단독주택 등)는 해당 줄을 조용히 생략(임의 채움 금지).
- 공시가격은 **시세가 아님**을 명시(통상 시세의 60~70% 수준, 현실화율 정책 변동 포함). 증감률·CAGR을 실거래가 상승률로 해석하지 않도록 경고.
- 답변 말미에 출처(국토교통부 건축HUB, data.go.kr) 명시.

## 응답 컴팩트 규칙

- 주소 + sigungu/bdong 코드(처음 1회)
- 주용도·구조·규모(층수·연면적·대지면적)
- 건폐율·용적률·세대/주차·사용승인일
- 통계 호출 시: 총괄(동 수·연면적·평균 경과연수) + 상위 5개 주용도 + 연대별/노후도 분포 요약
- 노후/철거/인허가 목록: 상위 5-10건 + 전체 건수 표시

## 책임 분담 (중요)

본 스킬은 **"건축물 실체"** 전담입니다. **"실거래가/전월세 시세"**은 페어 스킬을 사용하세요.

| 작업 | 스킬 | 데이터 소스 |
| --- | --- | --- |
| 실거래가·전월세 시세 | `moai-analyst:office-public-data-real-estate-search` | 국토교통부 실거래가 신고 |
| **건축물 실체(용도·구조·규모·규제·인허가·노후·철거)** | **`moai-analyst:data-building-ledger` (본 스킬)** | 국토교통부 건축HUB |
| 인구·가구 통계 | `moai-analyst:office-public-data-public-data` | KOSIS |
| 법원 경매 매각공고 | `moai-analyst:office-public-data-court-auction-search` | 대법원 경매정보 |

## 이 스킬을 사용하지 말아야 할 때

- **실거래가·전월세 시세** → `moai-analyst:office-public-data-real-estate-search`
- **인구·고용·물가 등 통계** → `moai-analyst:office-public-data-public-data` (KOSIS 자연어 우선)
- **법원 경매 매각공고·감정평가액·최저매각가** → `moai-analyst:office-public-data-court-auction-search`
- **소유자·소유정보(개인정보)** → 건축HUB API에 소유자 필드가 없으므로 본 스킬 범위 밖(등기부등본 조회 권장)
- **위반건축물 조회** → 표제부/기본개요/총괄표제부 어디에도 위반건축물 필드가 없음(API 실측 확인) → 조회 불가
- **부동산 세금·법률 자문** → 세무사·법무사 전문가 안내

## Prerequisites

사용자 측 필수 시크릿 **없음**. API 키 발급 불필요.

- archhub MCP는 공용키가 탑재된 remote 커넥터(`https://archhub-mcp.fly.dev/mcp`)로, URL만 `.mcp.json`에 등록하면 바로 사용합니다.
- 인터넷 연결만 있으면 동작합니다.
- 로컬 실행(stdio)이 필요한 경우에만 `ARCHHUB_SERVICE_KEY`(data.go.kr 건축HUB 서비스 Decoding 인증키)가 필요합니다. 일반적인 사용은 remote 커넥터로 충분합니다.

## Failure modes

- `[NOT_FOUND]` — 해당 필지/동에 데이터 없음. 환각 차단(임의 답변 금지).
- `[EXTERNAL_API_ERROR]` — data.go.kr 업스트림 API 오류. 재시도 안내.
- 주소가 모호한 경우 → `find_region`이 sigungu/bdong을 못 찾으면 광역시도 컨텍스트를 보강해 재시도 요청.
- 큰 동(수천 건) → `old_buildings`·`district_stats`·`demolitions`·`permits_pipeline`은 전체를 받아 다소 느릴 수 있음. 번지(`bun`/`ji`) 지정 권장.

## 관련 스킬 체이닝

- **before**: `moai-analyst:office-public-data-real-estate-search` — 실거래가 시세로 입지 검토 선행
- **after**: `moai-consultant:consult-market` — 건축물 + 시세 데이터 기반 시장 분석
- **after**: `moai-analyst:office-public-data-court-auction-search` — 경매 매각공고와 건축물대장 교차 검토
- **after**: `moai-officer:doc-pdf` — 건축물 종합카드·통계 PDF 보고서 생성
- **after**: `moai-officer:doc-xlsx` — 노후건물·인허카 파이프라인 엑셀 정리
- **pair**: `moai-officer:setup-mcp-connector` — archhub MCP 사전 준비 가이드

## Done when

- 주소를 `find_region`으로 sigungu_code/bdong_code로 변환했다(번지가 있으면 bun/ji 포함).
- 요청 목적(종합카드·층별·통계·노후·철거·인허가·공시가)에 맞는 도구를 선택해 호출했다.
- 결과를 용도·구조·규모·건폐율/용적률·출처 포함으로 정리했다.
- 공시가격은 시세가 아님을 명시했다(price_history 호출 시).
- "건축물 실체 vs 실거래가 시세" 책임 분담을 지켰다(시세 요청은 real-estate-search로 라우팅).
