# moai-finance 커넥터 가이드

## 법원경매정보 (courtauction.go.kr, v2.0.0+)

대법원이 운영하는 공식 법원경매정보 사이트의 매각공고와 사건정보를 read-only로 조회합니다. 자산 처분·경매 투자·실사 검토에 활용합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (사이트는 공개 데이터)
- Node.js 환경 (사이트 내부 WebSquare JSON XHR 직접 호출)
- `rebrowser-playwright` 또는 `playwright-core` (선택, 차단·5xx 시 fallback)

### Throttling — 매우 중요

사이트는 자동화 호출에 매우 민감합니다.

- 호출 간 **최소 2초** 지연
- 기본 세션 호출 budget **10회**
- 16회/30초 정도면 IP가 **약 1시간 차단**됩니다
- 차단 발생 시 자동 retry 금지(차단 연장 위험), 즉시 멈추고 사용자에게 안내

### 환경변수

본 커넥터는 환경변수를 요구하지 않습니다.

### 활용 스킬

- `court-auction-search`: 매각공고 조회·사건번호 단건 조회
- `financial-statements`: 경매 투자 타당성 분석
- `variance-analysis`: 감정평가액 vs 최저매각가 분석

---

## KRX (한국거래소) — k-skill-proxy 경유, v2.0.0+

KRX 상장 종목 검색·기본정보·일별 시세를 NomaDamas의 hosted 프록시(`k-skill-proxy.nomadamas.org`) 경유로 조회합니다. moai-business의 DART(공시) 데이터를 보완하는 시세 데이터로 활용합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (프록시가 키를 보유)
- 인터넷 연결만 있으면 동작

### 환경변수 (선택)

```
KSKILL_PROXY_BASE_URL=https://k-skill-proxy.nomadamas.org   # 기본값. self-host 시 변경
```

### Self-host 시 추가 설정 (운영 측)

```
KRX_API_KEY=발급받은_KRX_OpenAPI_키
```

발급: [KRX Open API](https://openapi.krx.co.kr/contents/OPP/MAIN/main/index.cmd) 회원가입 후 신청.

### 제공 데이터

| 시장 | 종목 검색 | 기본정보 | 일별 시세 |
|---|---|---|---|
| KOSPI | ✅ | ✅ | ✅ |
| KOSDAQ | ✅ | ✅ | ✅ |
| KONEX | ✅ | ✅ | ✅ |

read-only 일별 snapshot. **실시간 호가·체결은 미제공**.

### 활용 스킬

- `korean-stock-search`: 종목 검색·기본정보·일별 시세
- `variance-analysis`: 시세 변동 분석
- `investor-relations` (moai-business): IR 자료 작성 시 KRX 공식 시세
- `executive-summary` (moai-bi): 경영진 1pager 시세 요약

### Disclaimer (HARD)

본 커넥터는 **read-only 조회 전용**이며 **투자 자문이 아닙니다**. 답변 말미에 "KRX 공식 데이터 기준 / 투자 조언 아님" 고지를 항상 남깁니다.
