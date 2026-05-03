# moai-business 커넥터 가이드

## DART (금융감독원 전자공시시스템)

기업 공시 데이터를 조회하여 시장 분석, 경쟁사 분석, 재무 모델링에 활용합니다.

### API 키 발급

1. [DART Open API](https://opendart.fss.or.kr) 접속
2. 회원가입 (공인인증서 불필요, 이메일 인증만)
3. 마이페이지 > 인증키 신청
4. 발급된 인증키 복사

### 환경변수 설정

```
DART_API_KEY=발급받은_인증키
```

### 제공 데이터

| API | 용도 |
|-----|------|
| 공시 검색 | 사업보고서, 분기보고서, 주요사항보고서 |
| 기업 개황 | 회사명, 업종, 대표자, 설립일, 상장일 |
| 재무제표 | 재무상태표, 손익계산서, 현금흐름표 |
| 지분 공시 | 최대주주, 임원 지분 변동 |
| 배당 정보 | 배당금, 배당률, 배당 성향 |

### 요율 제한

- 일 10,000건 (무료)
- 분당 600건
- 초과 시 429 에러 반환

### 활용 스킬

- `strategy-planner`: 경쟁사 재무 분석, 시장 규모 추정
- `market-analyst`: 산업 동향, 기업 비교 분석
- `investor-relations`: IR 자료의 재무 데이터 검증

---

## MOLIT 실거래가 (k-skill-proxy 경유, v2.0.0+)

국토교통부 부동산 실거래가/전월세 신고 데이터를 NomaDamas의 hosted 프록시(`k-skill-proxy.nomadamas.org`) 경유로 조회합니다.

### 사용 측 준비

- **사용자 측 시크릿 불필요** (프록시가 키를 보유)
- 인터넷 연결만 있으면 동작

### 환경변수 (선택)

```
KSKILL_PROXY_BASE_URL=https://k-skill-proxy.nomadamas.org   # 기본값. self-host 시 변경
```

### Self-host 시 추가 설정 (운영 측)

self-host 프록시를 운영하려면 프록시 서버 환경에 다음 키를 등록합니다.

```
DATA_GO_KR_API_KEY=발급받은_공공데이터포털_키
```

발급: [공공데이터포털](https://www.data.go.kr) 회원가입 → 활용신청 → 자동승인. 일 1,000회(개발계정).

### 활용 스킬

- `real-estate-search`: 아파트·오피스텔·빌라·단독·상업용 매매·전월세 시세
- `market-analyst`: 부동산 시세 데이터 기반 시장 분석
- `investor-relations`: 부동산 자산 실거래가 IR 자료
