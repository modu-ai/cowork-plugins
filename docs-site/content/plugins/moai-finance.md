---
title: "moai-finance — 세무·결산·K-IFRS"
weight: 130
description: "3.3% 원천징수·부가세·홈택스·K-IFRS·예실 분석을 다루는 한국 세무·회계 6개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-finance"]
---

# moai-finance

> 한국 세법·회계 기준 6개 스킬을 제공합니다.

```mermaid
flowchart LR
    subgraph 세무회계["세무·회계"]
        A["tax-helper<br/>원천징수·부가세"]
        B["financial-statements<br/>K-IFRS 재무제표"]
        C["close-management<br/>결산·정산"]
    end
    subgraph 분석["분석·조회"]
        D["variance-analysis<br/>예실 분석"]
        E["court-auction-search<br/>법원경매"]
        F["korean-stock-search<br/>KRX 시세"]
    end
    style A fill:#e6f0ff,stroke:#3070d0
    style F fill:#e6ffec,stroke:#30a050
```

## 무엇을 하는 플러그인인가

`moai-finance` (v1.5.0)는 프리랜서 3.3% 원천징수, 종합소득세·부가가치세 신고, 홈택스 절차, K-IFRS 재무상태표·손익계산서·현금흐름표 작성, 월·분기·연간 결산과 4대보험 정산, 예산 대비 실적 분석까지 한국 기준 재무·세무 실무를 자동화합니다. 2026년 K-IFRS 제1118호 변경사항과 4대보험 요율·노동법 최신값이 반영되어 있습니다.

## 설치

{{< tabs "install-finance" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-finance` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (6개)

| 스킬 | 용도 |
|---|---|
| `tax-helper` | 3.3% 원천징수, 종합소득세, 부가가치세, 홈택스 절차 |
| `financial-statements` | K-IFRS 재무상태표·손익계산서·현금흐름표 |
| `close-management` | 월·분기·연간 결산, 4대보험 정산, 급여 마감 |
| `variance-analysis` | 예산 대비 실적, 매출·비용·이익 분산, KPI 추적 |
| `court-auction-search` (v2.0.0 신규) | 대법원 법원경매정보 매각공고·사건번호 단건 조회 |
| `korean-stock-search` (v2.0.0 신규) | KRX 상장 종목 검색·기본정보·일별 시세 |

## 한국 기준 최신화

- **2026년 K-IFRS 제1118호** 변경사항 반영
- **4대보험 요율·노동법** 최신값
- 홈택스 신고 일정 자동 안내

## 대표 체인

**월말 결산**

```text
close-management → xlsx-creator(결산표) → docx-generator(결산 보고서)
```

**예실 분석 보고**

```text
variance-analysis → xlsx-creator → docx-generator → ai-slop-reviewer
```

## 빠른 사용 예

```text
> 프리랜서 3.3% 원천징수 영수증 12장 합계 계산해줘. 종합소득세 예상 세액도.
```

```text
> 이번 분기 재무상태표 K-IFRS 기준으로 엑셀로 만들어줘.
```

## v2.0.0 신규 — `court-auction-search` (법원경매 매각공고)

대법원이 운영하는 공식 **법원경매정보**(`courtauction.go.kr`)의 매각공고와 사건정보를 read-only로 조회합니다. 자산 처분·경매 투자·실사 검토에 사용합니다.

### Throttling — 매우 중요

사이트는 자동화 호출에 매우 민감해 **빠른 연속 조회 시 IP가 약 1시간 차단**될 수 있습니다.

- 호출 간 최소 **2초** 지연
- 기본 세션 budget **10회**
- 차단 발생 시 자동 retry 금지(차단 연장 위험), 즉시 멈추고 사용자에게 안내

### Honest framing (사용자에게 항상 알려야 할 사실)

1. 데이터는 **공고 시점 기준**이며 정정·취하·연기로 변경될 수 있습니다.
2. **실제 입찰 전에는 법원 원문을 재확인**해야 합니다.
3. 본 스킬은 **read-only**입니다. 입찰서 자동 작성·자동 제출은 절대 미지원.

### 데이터 출처와 크롤링 윤리 (HARD)

법원경매정보 사이트(`courtauction.go.kr`)는 **공식 공개 OpenAPI를 제공하지 않습니다**. 본 스킬은 사이트 내부 WebSquare JSON XHR endpoint를 직접 호출하는 방식이며, 사이트 공개 데이터를 사용자가 브라우저에서 보는 형태로 가공해 돌려줍니다.

- 호출은 read-only이며 **사이트 부하를 주지 않도록** 호출 간 2초 지연 + 세션당 10회 budget을 강제합니다.
- 자동화 호출이 부담스러우면 사이트 운영기관(법원행정처) 문의 후 사용을 권장합니다.
- 한국 등기 관련 공식 OpenAPI가 필요하면 [등기정보광장 (data.iros.go.kr)](https://data.iros.go.kr)을 참고하세요(다른 도메인 — 등기 데이터, 경매 아님).

### 출처 어트리뷰션

본 스킬은 **NomaDamas/k-skill** (MIT) 의 `court-auction-notice-search`를 cowork에 포팅했습니다. 데이터는 [대법원 법원경매정보](https://www.courtauction.go.kr) 사이트의 공개 정보입니다.

## v2.0.0 신규 — `korean-stock-search` (KRX 시세)

KRX(한국거래소) 상장 종목 검색·기본정보·일별 시세를 조회합니다. moai-business의 DART(공시)를 보완하는 시세 데이터로 활용합니다.

### 지원 시장

KOSPI · KOSDAQ · KONEX

### 사용 측 준비

- **사용자 측 `KRX_API_KEY` 발급 불필요** — NomaDamas hosted 프록시가 보유
- self-host가 필요하면 `KSKILL_PROXY_BASE_URL`로 대체

### 데이터 갱신과 보유 기간

- **갱신 주기**: 일 1회 (영업일 하루 뒤 13시 이후 갱신, 예: 금요일 데이터는 차주 월요일)
- **데이터 보유 기간**: 2010년 이후
- **실시간 호가·체결 미제공** — 일별 snapshot만 제공

### Disclaimer (HARD)

본 스킬은 **read-only 조회 전용**이며 **투자 자문이 아닙니다**. 답변 말미에 "KRX 공식 데이터 기준 / 투자 조언 아님" 고지를 항상 남깁니다.

### 출처 어트리뷰션

본 스킬은 **NomaDamas/k-skill** (MIT) 의 `korean-stock-search`를 cowork에 포팅했습니다. 원 저작자 설계 참고는 [`jjlabsio/korea-stock-mcp`](https://github.com/jjlabsio/korea-stock-mcp) 이며, 공식 데이터 출처는 [KRX Open API](https://openapi.krx.co.kr) 입니다.

## 다음 단계

- [`moai-office`](../moai-office/) — 결산표·보고서 포맷
- [`moai-operations`](../moai-operations/) — 운영 지표 결합

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-finance 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)
- [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) — MIT — `court-auction-notice-search`, `korean-stock-search` 원본 (v2.0.0)
- [jjlabsio/korea-stock-mcp](https://github.com/jjlabsio/korea-stock-mcp) — MIT — KRX MCP 설계 참고
- [대법원 법원경매정보](https://www.courtauction.go.kr) — 공식 데이터 출처
- [KRX Open API](https://openapi.krx.co.kr) — 공식 데이터 출처
