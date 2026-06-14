# moai-wealth

개인 재무·재테크 플러그인 — 재테크 로드맵, 가계부·소비관리, 투자 입문, 보험 설계, 연말정산 절세, 경제지표 읽기.

직장인·1인 가구·사회초년생의 **개인 자산관리** 전반을 돕습니다. 종잣돈 모으기부터 자산 배분, 투자 입문, 보험 점검, 연말정산 환급 극대화, 경제지표를 내 돈 관점에서 읽는 법까지 2026년 한국 기준으로 안내합니다. **법인·사업자 세무는 `moai-finance`**, 개인 자산관리는 `moai-wealth`로 역할이 분리됩니다.

> **면책 고지**: 본 플러그인은 일반적인 재무 정보·교육 목적이며, 공인 투자·세무 자문을 대체하지 않습니다. 구체적 투자·세무 결정은 자격을 갖춘 전문가와 상담하세요.

## 스킬

| 스킬 | 설명 | 상태 |
|------|------|:----:|
| [wealth-roadmap](./skills/wealth-roadmap/) | 재무 현황 진단 → 목표 설정 → 종잣돈 단계 → 자산 배분 → 자동화. 재테크 시작 로드맵 | ✅ |
| [household-budget](./skills/household-budget/) | 통장 쪼개기, 가계부 작성, 50/30/20 예산, 소비 회고 루틴, 새는 돈 찾기 | ✅ |
| [invest-primer](./skills/invest-primer/) | 분산·장기·리스크 원칙, 자산군(주식/ETF/부동산/채권) 입문, 초보 포트폴리오, 투자 사기 회피 | ✅ |
| [insurance-fit](./skills/insurance-fit/) | 필요한 보험 진단(실손·암·종신·연금), 과보험 점검, 생애주기별 보험 리모델링 | ✅ |
| [personal-tax-saver](./skills/personal-tax-saver/) | 근로자 연말정산 절세 — 소득공제 vs 세액공제, 항목별 공제 전략, 환급 극대화 | ✅ |
| [econ-literacy](./skills/econ-literacy/) | 금리·환율·물가·GDP·고용 지표를 내 자산 관점에서 읽기, 경기 사이클 이해 | ✅ |

## 사용 예시

```
사회초년생인데 재테크 어떻게 시작해야 할지 로드맵 짜줘
```

```
월급 280만원인데 통장 쪼개기랑 예산 배분 어떻게 하지?
```

```
연말정산 환급 더 받으려면 12월 전에 뭘 챙겨야 해?
```

## 주요 워크플로우 체인

```
재테크 첫걸음 풀 코스
  wealth-roadmap(목표·진단) → household-budget(예산 시스템) → invest-primer(투자 시작)

생애주기 자산 점검
  wealth-roadmap(현황 진단) → insurance-fit(보험 리모델링) → econ-literacy(시장 환경 읽기)

연말 머니 정산
  household-budget(소비 회고) → personal-tax-saver(연말정산 절세) → wealth-roadmap(내년 목표)
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 법인·사업자 세무(3.3%·부가세·종소세) | `moai-finance/tax-helper` |
| K-IFRS 재무제표·법인 결산 | `moai-finance/financial-statements` |
| 주식 종목 시세 조회(KRX) | `moai-finance/korean-stock-search` |
| 개인 목표·습관·회고 관리 | `moai-productivity/goal-planner` |

## 한국 개인 재무 환경 특화

- **2026년 기준** 연말정산 공제 항목·한도, 금융소득 과세 반영
- **통장 쪼개기·50/30/20** 등 실천 가능한 예산 프레임
- **생애주기별** 보험·투자·은퇴 설계 관점
- **경제지표를 내 돈 관점**에서 해석 (금리↑ → 대출·예금 영향 등)

## 설치

Settings > Plugins > cowork-plugins에서 `moai-wealth` 선택

## 참고자료

| 항목 | URL |
|------|-----|
| [홈택스 연말정산 간소화](https://www.hometax.go.kr/) | 국세청 |
| [금융감독원 파인](https://fine.fss.or.kr/) | 금융상품·보험 비교 |
