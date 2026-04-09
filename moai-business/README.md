# moai-business

비즈니스 전략 플러그인 — 사업계획서, 시장조사, 재무모델, 투자제안서.

창업 초기 린 캔버스부터 Series B IR 자료, TAM/SAM/SOM 시장 분석, 재무 시뮬레이션까지 비즈니스 의사결정 전반을 지원합니다. DART 공시 데이터 연동으로 실시간 기업 정보를 활용합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [strategy-planner](./skills/strategy-planner/) | 사업계획서, 린 캔버스, SWOT, OKR, Blue Ocean 전략 수립 | 5 | ✅ |
| [market-analyst](./skills/market-analyst/) | TAM/SAM/SOM 산출, 경쟁사 분석, 고객 세그멘테이션, 가격 전략 | 3 | ✅ |
| [investor-relations](./skills/investor-relations/) | IR 덱, 피칭 자료, 매출 예측, 손익분석, 현금흐름 모델 | 2 | ✅ |
| [daily-briefing](./skills/daily-briefing/) | 업계 뉴스, 시장 동향, 경쟁사 모니터링, KPI 대시보드 브리핑 | 0 | ✅ |

## 에이전트

| 에이전트 | 모델 | 역할 |
|---------|:----:|------|
| market-researcher | Sonnet | DART/KOSIS/네이버 데이터랩 기반 시장 데이터 자율 수집. moai-product 등에서 공유 호출 |

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

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-business` 선택
