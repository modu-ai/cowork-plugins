# moai-public-data

한국 공공·데이터 조회 전담 플러그인 — 주식/경매/부동산/공공데이터포털/KOSIS.

KRX 상장 종목 시세, 대법원 법원경매 매각공고, 국토교통부 실거래가, 공공데이터포털·KOSIS 통계를 한곳에서 실시간으로 조회합니다. 대부분 사용자 API 키 없이 동작하며(KRX·법원경매·실거래가는 프록시/공개 데이터), data.go.kr·KOSIS만 무료 키 등록이 필요합니다. 모두 read-only 조회 전용입니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [korean-stock-search](./skills/korean-stock-search/) | KRX 상장 종목 검색·기본정보·일별 시세 (k-skill-proxy 경유, 키 불필요) | 0 | ✅ |
| [court-auction-search](./skills/court-auction-search/) | 대법원 법원경매정보 매각공고·사건번호 단건 조회 (read-only, 2초 throttle) | 0 | ✅ |
| [real-estate-search](./skills/real-estate-search/) | 국토교통부(MOLIT) 실거래가/전월세 — 아파트·오피스텔·빌라·단독·상업용 (k-skill-proxy 경유, 키 불필요) | 0 | ✅ |
| [public-data](./skills/public-data/) | 공공데이터포털(data.go.kr)·KOSIS 통계청 실시간 조회 | 1 | ✅ |

## 커넥터

설정 절차는 [CONNECTORS.md](./CONNECTORS.md)를 참고하세요.

| 데이터 소스 | 사용자 키 | 비고 |
|------|:--------:|------|
| KRX (한국거래소) | 불필요 | k-skill-proxy가 키 보유 |
| 법원경매정보 (courtauction.go.kr) | 불필요 | 공개 데이터, 2초 throttle 필수 |
| 국토교통부 실거래가 (MOLIT) | 불필요 | k-skill-proxy가 키 보유 |
| 공공데이터포털 (data.go.kr) | DATA_GO_KR_API_KEY | 무료, 1,000회/일 |
| KOSIS 통계청 | KOSIS_API_KEY | 무료, 1,000회/일 |

## 주요 워크플로우 체인

```
부동산 입지 분석
  real-estate-search(실거래가) → public-data(인구·가구 통계) → moai-data:data-visualizer

경매 투자 타당성
  court-auction-search(매각공고) → real-estate-search(인근 실거래가) → moai-finance:financial-statements

IR 자료용 시세
  korean-stock-search(KRX 시세) → moai-business:investor-relations → moai-office:pptx-designer

공공데이터 → 정책 분석 보고
  public-data(KOSIS/data.go.kr fetch) → moai-data:data-explorer → moai-data:data-visualizer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 기업 공시·재무 분석(DART) | `moai-business` 플러그인 DART 연동 |
| 재무제표 분석(K-IFRS) | `moai-finance:financial-statements` |
| CSV/Excel 프로파일링 | `moai-data:data-explorer` |
| 차트·대시보드 시각화 | `moai-data:data-visualizer` |
| 상권분석(소상공인365) | `moai-business:sbiz365-analyst` |
| 시세 데이터 기반 시장 분석 | `moai-business:market-analyst` |

## 한국 데이터 환경 특화

- **KRX·법원경매·실거래가 키 불필요** — 사용자는 별도 발급 없이 바로 조회 (공개 데이터·프록시 경유)
- **공공데이터포털 + KOSIS** 직접 조회 (무료 키 등록 시)
- 모든 스킬은 **read-only 조회 전용** — 투자 자문·입찰 자동화 미지원
- 숫자는 한국식 단위(원, 억/만, 천단위 콤마)로 환산하고 원본도 유지

## 사용 예시

```
삼성전자 오늘 종가랑 거래량 알려줘. 시가총액도 같이.
```

```
잠실 리센츠 2024년 아파트 매매 실거래가 찾아서 평형별 중위값 비교해줘.
```

```
서울중앙지방법원 이번 달 부동산 경매 매각공고 보여줘. 기일입찰만.
```

```
KOSIS에서 최근 5년 한국 가구당 월평균 소비지출 통계 가져와줘.
```

## 설치

Settings > Plugins > cowork-plugins에서 `moai-public-data` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [KRX Open API](https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd) | 공식 API | KRX 시세 (운영 측) |
| [법원경매정보](https://www.courtauction.go.kr/) | 공식 사이트 | 매각공고·사건 조회 |
| [공공데이터포털](https://www.data.go.kr/) | 공식 API | 공공데이터 조회 |
| [KOSIS OpenAPI](https://kosis.kr/openapi/) | 공식 API | 통계청 데이터 |
| [korea-stock-mcp](https://github.com/jjlabsio/korea-stock-mcp) | 오픈소스 | KRX MCP 설계 참고 |
| [real-estate-mcp](https://github.com/tae0y/real-estate-mcp) | 오픈소스 | 실거래가 MCP 참고 |
| [data-go-mcp-servers](https://github.com/Koomook/data-go-mcp-servers) | 오픈소스 | 공공데이터 MCP |
