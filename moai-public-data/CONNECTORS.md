# moai-public-data 커넥터 가이드

한국 공공·데이터 조회 5개 소스의 설정 절차를 한곳에 모았습니다. 대부분 사용자 측 키가 필요 없고, data.go.kr·KOSIS만 무료 키 등록이 필요합니다. 모든 커넥터는 **read-only 조회 전용**입니다.

| 데이터 소스 | 활용 스킬 | 사용자 키 | 비고 |
|------|------|:--------:|------|
| KRX (한국거래소) | `korean-stock-search` | 불필요 | k-skill-proxy가 키 보유 |
| 법원경매정보 | `court-auction-search` | 불필요 | 공개 데이터, 2초 throttle 필수 |
| 국토교통부 실거래가 (MOLIT) | `real-estate-search` | 불필요 | k-skill-proxy가 키 보유 |
| 공공데이터포털 (data.go.kr) | `public-data` | DATA_GO_KR_API_KEY | 무료, 1,000회/일 |
| KOSIS 통계청 | `public-data` | KOSIS_API_KEY | 무료, 1,000회/일 |

---

## 1. KRX (한국거래소) — k-skill-proxy 경유

KRX 상장 종목 검색·기본정보·일별 시세를 NomaDamas의 hosted 프록시(`k-skill-proxy.nomadamas.org`) 경유로 조회합니다. moai-business의 DART(공시) 데이터를 보완하는 시세 데이터로 활용합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (프록시가 키를 보유)
- 인터넷 연결만 있으면 동작

### 환경변수 (선택)

```
KSKILL_PROXY_BASE_URL=https://k-skill-proxy.nomadamas.org   # 기본값. self-host 시 변경
```

### Endpoints

```
GET /v1/korean-stock/search?q={검색어}&bas_dd={YYYYMMDD}
GET /v1/korean-stock/base-info?market={KOSPI|KOSDAQ|KONEX}&code={코드}&bas_dd={YYYYMMDD}
GET /v1/korean-stock/trade-info?market={KOSPI|KOSDAQ|KONEX}&code={코드}&bas_dd={YYYYMMDD}
```

### Self-host 시 추가 설정 (운영 측)

```
KRX_API_KEY=발급받은_KRX_OpenAPI_키
```

발급: [KRX Open API](https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd) 회원가입 후 신청.

### Disclaimer (HARD)

read-only 일별 snapshot. **실시간 호가·체결은 미제공**이며 **투자 자문이 아닙니다**. 답변 말미에 "KRX 공식 데이터 기준 / 투자 조언 아님" 고지를 항상 남깁니다.

---

## 2. 법원경매정보 (courtauction.go.kr)

대법원이 운영하는 공식 법원경매정보 사이트의 매각공고와 사건정보를 read-only로 조회합니다. 공식 OPEN API가 없어 사이트 내부 WebSquare JSON XHR endpoint를 직접 호출합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (사이트는 공개 데이터)
- Node.js 환경 (npm 패키지 `court-auction-notice-search` 호출)
- `rebrowser-playwright` 또는 `playwright-core` (선택, 차단·5xx 시 fallback)

### 환경변수

본 커넥터는 환경변수를 요구하지 않습니다.

### Endpoints (사이트 내부 직접 호출)

```
POST /pgj/pgj143/selectRletDspslPbanc.on       — 매각공고 목록
POST /pgj/pgj143/selectRletDspslPbancDtl.on    — 매각공고 상세 (사건/물건 펼치기)
POST /pgj/pgj15A/selectAuctnCsSrchRslt.on      — 사건 단건 조회
POST /pgj/pgjComm/selectCortOfcCdLst.on        — 법원사무소코드 전체
```

### Throttling — 매우 중요 (HARD)

사이트는 자동화 호출에 매우 민감합니다.

- 호출 간 **최소 2초** 지연 (기본)
- 기본 세션 호출 budget **10회**
- 빠른 연속 조회 시 IP가 **약 1시간 차단**됩니다
- 차단(`data.ipcheck === false`) 발생 시 자동 retry 금지(차단 연장 위험), 즉시 멈추고 사용자에게 안내

### Disclaimer (HARD)

데이터는 공고 시점 기준이며 정정·취하·연기로 변경될 수 있습니다. **실제 입찰 전에는 법원 원문을 재확인**해야 합니다. 입찰 자동화는 절대 미지원입니다.

---

## 3. 국토교통부 실거래가 (MOLIT) — k-skill-proxy 경유

국토교통부 실거래가 신고 데이터로 아파트·오피스텔·연립다세대·단독다가구·상업업무용 부동산의 매매·전월세 시세를 조회합니다. NomaDamas hosted 프록시(`k-skill-proxy.nomadamas.org`) 경유.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (프록시가 키를 보유)
- 인터넷 연결만 있으면 동작

### 환경변수 (선택)

```
KSKILL_PROXY_BASE_URL=https://k-skill-proxy.nomadamas.org   # 기본값. self-host 시 변경
```

### Endpoints

```
GET /v1/real-estate/region-code?q={지역명}
GET /v1/real-estate/:assetType/:dealType?lawd_cd={5자리법정동코드}&deal_ymd={YYYYMM}
```

| assetType | dealType | 설명 |
|---|---|---|
| `apartment` | `trade` / `rent` | 아파트 매매 / 전월세 |
| `officetel` | `trade` / `rent` | 오피스텔 매매 / 전월세 |
| `villa` | `trade` / `rent` | 연립다세대 매매 / 전월세 |
| `single-house` | `trade` / `rent` | 단독/다가구 매매 / 전월세 |
| `commercial` | `trade` | 상업업무용 매매 (`rent` 미지원) |

### Self-host 시 추가 설정 (운영 측)

```
DATA_GO_KR_API_KEY=발급받은_공공데이터포털_키
```

(실거래가 upstream은 공공데이터포털 MOLIT API이며, 운영 프록시 측에만 둡니다.)

### Disclaimer (HARD)

국토교통부 신고 데이터이며 **실거래가와 호가를 섞어 말하지 않습니다**. 답변 말미에 출처(국토교통부 실거래가 신고)를 남깁니다. 가격 단위는 만원(예: `245000` = 24억 5천만원).

---

## 4. 공공데이터포털 (data.go.kr)

공공데이터포털의 각종 공공 API를 실시간 조회합니다.

### 사용 측 준비 (HARD — 키 필수)

1. [data.go.kr](https://www.data.go.kr/) 접속 → 회원가입
2. 개발계정 신청 → 활용신청 → 자동승인
3. 무료, **1,000회/일** (개발계정)

### 환경변수

```
DATA_GO_KR_API_KEY=발급받은_서비스키
```

키 입력 후 `${CLAUDE_PLUGIN_DATA}/moai-credentials.env`에 저장합니다.

### 호출 패턴

```
GET https://apis.data.go.kr/{기관코드}/{서비스명}?ServiceKey={키}&...
```

응답: JSON 또는 XML.

---

## 5. KOSIS 통계청

KOSIS(통계청) OpenAPI로 인구·경제·물가·고용 등 국가통계를 실시간 조회합니다.

### 사용 측 준비 (HARD — 키 필수)

1. [kosis.kr/openapi](https://kosis.kr/openapi/) 접속 → 회원가입
2. 인증키 신청 → 자동승인 즉시 발급
3. 무료, **1,000회/일**

### 환경변수

```
KOSIS_API_KEY=발급받은_인증키
```

키 입력 후 `${CLAUDE_PLUGIN_DATA}/moai-credentials.env`에 저장합니다.

### 호출 패턴

```
GET https://kosis.kr/openapi/Param/statisticsParameterData.do
  ?method=getList
  &apiKey={키}
  &itmId=T10
  &objL1=ALL
  &format=json
  &jsonVD=Y
  &prdSe=M
  &startPrdDe=202501
  &endPrdDe=202512
  &orgId=101
  &tblId=DT_1B04005N
```

응답 포맷: JSON, XML, SDMX.

### 주요 KOSIS 통계 분류

| 분류 | 예시 |
|------|------|
| 인구 | 인구총조사, 주민등록인구 |
| 경제 | GDP, 경제성장률 |
| 물가 | 소비자물가지수 |
| 고용 | 경제활동인구, 실업률 |
