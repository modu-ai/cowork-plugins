# moai-business

비즈니스 전략·창업 플러그인 — 사업계획서, 시장조사, 재무모델, 투자제안서, **소상공인 상권분석**, **정부지원사업 통합**, **국토부 실거래가** (v2.0.0 신규).

창업 초기 린 캔버스부터 Series B IR 자료, TAM/SAM/SOM 시장 분석, 재무 시뮬레이션을 거쳐 v1.5.0부터는 **소상공인365 상권분석 PDF → 창업타당성 보고서**와 **K-Startup·BIZINFO·중기부 정부지원사업 탐색·신청서 작성**까지 범위를 넓혔습니다. **v2.0.0부터** `real-estate-search`로 국토교통부 실거래가/전월세 데이터(아파트·오피스텔·빌라·단독·상업용)를 NomaDamas hosted proxy 경유로 조회합니다(API 키 불필요). DART 공시 데이터 연동으로 실시간 기업 정보를 활용합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [strategy-planner](./skills/strategy-planner/) | 사업계획서, 린 캔버스, SWOT, OKR, Blue Ocean 전략 수립 | 5 | ✅ |
| [market-analyst](./skills/market-analyst/) | TAM/SAM/SOM 산출, 경쟁사 분석, 고객 세그멘테이션, 가격 전략 | 3 | ✅ |
| [investor-relations](./skills/investor-relations/) | IR 덱, 피칭 자료, 매출 예측, 손익분석, 현금흐름 모델 | 2 | ✅ |
| [daily-briefing](./skills/daily-briefing/) | 업계 뉴스, 시장 동향, 경쟁사 모니터링, KPI 대시보드 브리핑 | 0 | ✅ |
| [sbiz365-analyst](./skills/sbiz365-analyst/) | 소상공인365 PDF 분석 → 4축 100점 창업타당성 평가 + 9섹션 DOCX 보고서 | 4 | ✅ |
| [kr-gov-grant](./skills/kr-gov-grant/) | K-Startup·BIZINFO·중기부·IITP·문체부·농식품부 정부지원사업 통합 (탐색·작성·검토·일정 4 MODE) | 1 | ✅ |
| [consulting-brief](./skills/consulting-brief/) | McKinsey/BCG/Bain Major 3 컨설팅 펌 표준 인게이지먼트 브리프 (목표·범위·산출물·일정·리스크) | 1 | ✅ |
| [sales-playbook](./skills/sales-playbook/) | 영업 플레이북 자동 생성 (타겟 산업·ICP·콜드 콘택트·반론 대응·후속 시퀀스) | 1 | ✅ |
| [startup-launchpad](./skills/startup-launchpad/) | 스타트업 종합 패키지 — 아이디어→사업계획서→피치덱→재무 모델→3년 예산까지 한 번에 | 1 | ✅ |
| [real-estate-search](./skills/real-estate-search/) | 국토교통부(MOLIT) 실거래가/전월세 — 아파트·오피스텔·빌라·단독·상업용 (k-skill-proxy 경유, v2.0.0+) | 0 | ✅ |

## MCP 커넥터

| 서버 | 용도 |
|------|------|
| dart | 금융감독원 DART 공시 데이터 API (`DART_API_KEY` 필요) |

## 사용 예시

```
스타트업 사업계획서 초안 작성해줘. 타깃은 B2B SaaS, 시리즈 A 준비 중이야.
```

```
우리 경쟁사 세 곳 분석해서 포지셔닝 맵 만들어줘
```

```
매일 아침 업계 뉴스 브리핑 만들어줘
```

```
소상공인365에서 내려받은 홍대 상권분석 PDF 첨부. 카페 창업 검토 중, 예산 5천만원.
```

```
예비창업자 AI 교육 서비스 창업 준비 중. 받을 수 있는 정부지원사업 3개 추천해줘.
```

```
예비창업패키지 신청서 초안 써줘. 업종 AI 교육, 팀원 3명, 목표 자금 1억.
```

## 설치

Settings > Plugins > cowork-plugins에서 `moai-business` 선택

## 참고자료

| 항목 | URL | 용도 |
|------|-----|------|
| [DART-mcp-server](https://github.com/snaiws/DART-mcp-server) | 오픈소스 MCP | 전자공시 조회 |
| [DART OpenAPI](https://opendart.fss.or.kr/) | 공식 API | 기업 공시/재무제표 |
| [dartpoint-mcp](https://github.com/dartpointai/dartpoint-mcp) | 대안 MCP | 기업 분석 리포트 |
| [소상공인365 빅데이터 포털](https://bigdata.sbiz.or.kr) | 공식 데이터 | 상권분석 PDF 원본 (sbiz365-analyst 입력) |
| [K-Startup (창업진흥원)](https://www.k-startup.go.kr) | 공식 공고 | 예비창업패키지·초기창업패키지·TIPS 등 |
| [BIZINFO (중소벤처기업부)](https://www.bizinfo.go.kr) | 공식 공고 | 중소기업·소상공인 지원사업 통합 검색 |
| [나라장터 (조달청)](https://www.g2b.go.kr) | 공식 입찰 | 공공조달·정부사업 참여 |
