# moai-finance

재무/세무 플러그인 — 3.3% 원천징수, 부가세, 홈택스, K-IFRS, 연말정산, **법원경매 매각공고**·**KRX 시세** (v2.0.0 신규).

국내 세법 체계에 맞춘 세무 상담부터 K-IFRS 기준 재무제표 작성, 결산 관리, 예산 분석까지 재무 실무 전반을 지원합니다. 2026년 최신 4대보험 요율과 세법 변경사항을 반영합니다. **v2.0.0부터** `court-auction-search`(대법원 법원경매정보 매각공고·사건번호 단건 조회)와 `korean-stock-search`(KRX 상장 종목·일별 시세)를 도입해 자산 처분·경매 투자·IR 작성을 보조합니다(KRX 데이터는 일 1회 갱신, 실시간 호가·체결 미제공).

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [tax-helper](./skills/tax-helper/) | 3.3% 원천징수, 종합소득세, 부가가치세, 홈택스 신고 절차 안내 | 2 | ✅ |
| [financial-statements](./skills/financial-statements/) | K-IFRS 기준 재무상태표/손익계산서/현금흐름표, 주석 공시, 재무비율 분석 | 3 | ✅ |
| [close-management](./skills/close-management/) | 월말/분기/연간 결산, 급여 정산, 4대보험 정산, 세무 일정 관리 | 4 | ✅ |
| [variance-analysis](./skills/variance-analysis/) | 예산 대비 실적 분산 분석, 매출/비용/이익 항목별 원인 분석, KPI 추적 | 0 | ✅ |
| [court-auction-search](./skills/court-auction-search/) | 대법원 법원경매정보 매각공고·사건번호 단건 조회 (read-only, 2초 throttle, v2.0.0+) | 0 | ✅ |
| [korean-stock-search](./skills/korean-stock-search/) | KRX 상장 종목 검색·기본정보·일별 시세 (k-skill-proxy 경유, v2.0.0+) | 0 | ✅ |

## 사용 예시

```
프리랜서 디자이너에게 200만원 지급할 때 3.3% 원천징수 어떻게 처리해?
```

```
K-IFRS 기준으로 분기 재무제표 만들어줘
```

```
2분기 영업이익이 목표 대비 15% 미달했어. 원인 분석 보고서 써줘.
```

## 주요 워크플로우 체인

```
월말 결산 풀 사이클
  close-management(결산 일정·체크리스트) → financial-statements(K-IFRS 재무제표) → docx-generator

분기 변동분석 + 임원 1pager
  variance-analysis(예산 vs 실적) → moai-bi/executive-summary → pptx-designer

세무 신고 가이드
  tax-helper(원천징수·VAT·종소세) → docx-generator(신고 가이드)

연말정산 풀 패키지
  tax-helper(연말정산 가이드) → moai-hr/draft-offer(원천징수 영수증) → xlsx-creator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| BI 대시보드·임원 1pager | `moai-bi/executive-summary` |
| K-IFRS 공시 자료(DART) 분석 | `moai-business/market-analyst` |
| 4대보험 가입·계산 | `moai-hr/draft-offer` |
| 견적서·세금계산서 | `moai-sales/proposal-writer` (예정 quote-generator) |

## 한국 세무·재무 환경 특화

- **2026년 4대보험 요율** 자동 적용 (국민연금 9% / 건강보험 7.09% / 고용보험 1.8% / 산재보험 업종별)
- **K-IFRS 1019(Lease)·1115(Revenue)** 신규 기준 반영
- **홈택스 신고 절차** 화면 단계별 가이드
- **3.3% 원천징수 자동 계산** + 사업소득·기타소득 구분
- **연말정산 13월의 월급** 자동 시뮬레이션

## 설치

Settings > Plugins > cowork-plugins에서 `moai-finance` 선택

## 참고자료

| 항목 | URL |
|------|-----|
| [홈택스](https://www.hometax.go.kr/) | 국세청 세금 신고/조회 |
| [K-IFRS 공시](https://www.kasb.or.kr/) | 한국회계기준원 |
