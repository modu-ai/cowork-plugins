---
title: "moai-wealth — 개인 재무·재테크"
weight: 210
description: "재테크 로드맵·가계부·투자 입문·보험 설계·연말정산 절세·경제지표 읽기까지 직장인 개인 자산관리 6개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-wealth"]
---

# moai-wealth

> 직장인·1인 가구·사회초년생의 개인 자산관리 6개 스킬을 제공합니다.

```mermaid
flowchart LR
    subgraph 설계["계획·진단"]
        A["wealth-roadmap<br/>재테크 로드맵"]
        B["household-budget<br/>가계부·예산"]
    end
    subgraph 운용["투자·보장"]
        C["invest-primer<br/>투자 입문"]
        D["insurance-fit<br/>보험 설계"]
    end
    subgraph 절세이해["절세·이해"]
        E["personal-tax-saver<br/>연말정산 절세"]
        F["econ-literacy<br/>경제지표 읽기"]
    end
    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style C fill:#e6f0ef,stroke:#144a46,color:#09110f
    style E fill:#fbf0dc,stroke:#c47b2a,color:#09110f
```

## 무엇을 하는 플러그인인가

`moai-wealth`는 종잣돈 모으기부터 자산 배분, 투자 입문, 보험 점검, 연말정산 환급 극대화, 경제지표를 내 돈 관점에서 읽는 법까지 직장인의 개인 자산관리 전반을 돕습니다. 통장 쪼개기·50/30/20 예산 같은 실천 가능한 프레임과 생애주기별 보험·투자·은퇴 관점이 2026년 한국 기준으로 반영되어 있습니다.

법인·사업자 세무(3.3% 원천징수·부가세·종합소득세)와 K-IFRS 재무제표는 [`moai-finance`](../moai-finance/)가 맡고, 개인 자산관리는 `moai-wealth`로 역할이 분리됩니다.

{{< hint type="caution" >}}
**개인 재무 면책 고지**: 본 플러그인은 일반적인 재무 정보·교육 목적이며, 공인 투자·세무 자문을 대체하지 않습니다. 구체적 투자·세무 결정은 자격을 갖춘 전문가와 상담하세요. 투자에는 원금 손실 위험이 따릅니다.
{{< /hint >}}

## 설치

{{< tabs "install-wealth" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-wealth` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-wealth)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (6개)

| 스킬 | 용도 |
|---|---|
| `wealth-roadmap` | 재무 현황 진단 → 목표 설정 → 종잣돈 단계 → 자산 배분 → 자동화. 재테크 시작 로드맵 |
| `household-budget` | 통장 쪼개기, 가계부 작성, 50/30/20 예산, 소비 회고 루틴, 새는 돈 찾기 |
| `invest-primer` | 분산·장기·리스크 원칙, 자산군(주식·ETF·부동산·채권) 입문, 초보 포트폴리오, 투자 사기 회피 |
| `insurance-fit` | 필요한 보험 진단(실손·암·종신·연금), 과보험 점검, 생애주기별 보험 리모델링 |
| `personal-tax-saver` | 근로자 연말정산 절세 — 소득공제 vs 세액공제, 항목별 공제 전략, 환급 극대화 |
| `econ-literacy` | 금리·환율·물가·GDP·고용 지표를 내 자산 관점에서 읽기, 경기 사이클 이해 |

## 한국 개인 재무 환경 특화

- **2026년 기준** 연말정산 공제 항목·한도, 금융소득 과세 반영
- **통장 쪼개기·50/30/20** 등 실천 가능한 예산 프레임
- **생애주기별** 보험·투자·은퇴 설계 관점
- **경제지표를 내 돈 관점**에서 해석 (금리 상승 → 대출·예금 영향 등)

## 대표 체인

**재테크 첫걸음 풀 코스**

```text
wealth-roadmap(목표·진단) → household-budget(예산 시스템) → invest-primer(투자 시작)
```

**생애주기 자산 점검**

```text
wealth-roadmap(현황 진단) → insurance-fit(보험 리모델링) → econ-literacy(시장 환경 읽기)
```

**연말 머니 정산**

```text
household-budget(소비 회고) → personal-tax-saver(연말정산 절세) → wealth-roadmap(내년 목표)
```

## 사용 예시

{{< terminal title="claude — cowork" >}}
> 사회초년생인데 재테크 어떻게 시작해야 할지 로드맵 짜줘
{{< /terminal >}}

→ `wealth-roadmap` 자동 호출 → AskUserQuestion(소득·목표·기간) → 재무 현황 진단 → 종잣돈 단계 → 자산 배분 → 자동화 5단계 로드맵.

{{< terminal title="claude — cowork" >}}
> 월급 280만원인데 통장 쪼개기랑 예산 배분 어떻게 하지?
{{< /terminal >}}

→ `household-budget` 자동 호출 → 50/30/20 예산 + 통장 4분할 + 소비 회고 루틴.

{{< terminal title="claude — cowork" >}}
> 연말정산 환급 더 받으려면 12월 전에 뭘 챙겨야 해?
{{< /terminal >}}

→ `personal-tax-saver` 자동 호출 → 소득공제 vs 세액공제 진단 → 항목별 공제 전략 → 환급 극대화 체크리스트.

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 법인·사업자 세무(3.3%·부가세·종소세) | [`moai-finance`](../moai-finance/) `tax-helper` |
| K-IFRS 재무제표·법인 결산 | [`moai-finance`](../moai-finance/) `financial-statements` |
| 주식 종목 시세 조회(KRX) | [`moai-finance`](../moai-finance/) `korean-stock-search` |
| 개인 목표·습관·회고 관리 | [`moai-productivity`](../moai-productivity/) `goal-planner` |

## 다음 단계

- [`moai-finance`](../moai-finance/) — 법인 세무·결산·재무제표
- [`moai-productivity`](../moai-productivity/) — 개인 목표·습관·자기관리

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-wealth 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-wealth)
- [홈택스 연말정산 간소화](https://www.hometax.go.kr/) — 국세청
- [금융감독원 파인](https://fine.fss.or.kr/) — 금융상품·보험 비교
