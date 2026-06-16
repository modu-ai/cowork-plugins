---
title: "moai-public-data — 한국 공공·데이터 조회"
weight: 220
description: "KRX 종목 시세·법원경매·국토부 실거래가·공공데이터포털/KOSIS 통계를 한 플러그인에서 조회합니다. 모두 read-only이며 별도 API 키 발급이 필요 없습니다."
geekdocBreadcrumb: true
tags: ["moai-public-data"]
---

# moai-public-data

> 한국의 공공·시세 데이터를 별도 API 키 없이 조회하는 4개 스킬 묶음입니다.

```mermaid
flowchart LR
    subgraph 시세["시세·자산"]
        A["korean-stock-search<br/>KRX 종목 시세"]
        B["court-auction-search<br/>법원경매"]
        C["real-estate-search<br/>실거래가"]
    end
    subgraph 통계["공공 통계"]
        D["public-data<br/>공공데이터포털·KOSIS"]
    end
    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style C fill:#e6f0ef,stroke:#144a46,color:#09110f
    style D fill:#fbf0dc,stroke:#c47b2a,color:#09110f
```

## 무엇을 하는 플러그인인가

`moai-public-data`는 흩어져 있던 한국 공공·시세 조회 기능을 조회 전담 플러그인 하나로 모은 것입니다. KRX 상장 종목의 일별 시세, 대법원 법원경매 매각공고, 국토교통부 실거래가, 공공데이터포털·KOSIS 통계를 자연어로 조회합니다.

## 이 플러그인으로 무엇을 할 수 있나

공공기관의 자료는 흩어져 있습니다. KRX(한국거래소)의 시세, 법원의 경매 공고, 국토부의 실거래가, 통계청의 인구·경제 자료가 각기 다른 사이트에 나뉘어 있고, 하나하나 들어가 회원가입하고 이용 절차를 밟아야 자료가 보입니다. 도서관에 비유하면 여러 공공기관이 각각 다른 도서관인 셈입니다. 한 도서관에서 주식 시세를 찾고, 또 다른 도서관에 가서 부동산 실거래가를 찾고, 또 다른 도서관에서 통계 자료를 찾아야 합니다. 도서관마다 회원가입하고 출입증(API 키, 컴퓨터 프로그램이 자료를 요청할 때 쓰는 열쇠)을 받아야 하는 번거로움이 매번 반복됩니다.

이 플러그인은 그 과정을 '통합 안내 데스크'로 바꿔줍니다. 여러 도서관에 일일이 출입증을 받아 다닐 필요 없이, 한곳의 안내 데스크에 자연어로 "잠실 아파트 실거래가 찾아줘"라고 물으면 데스크 직원이 알아서 해당 도서관에 가서 자료를 찾아옵니다. 여기서 안내 데스크 역할을 하는 것이 프록시(사용자 대신 외부 자료를 찾아 전달해 주는 중계 서비스)입니다. 사용자는 API 키를 직접 발급받거나 MCP 서버(외부 데이터를 연결해 주는 별도 프로그램)를 설치할 필요 없이, 한 번에 자연어로 질문하면 답을 받습니다.

```mermaid
flowchart LR
    U["사용자 자연어 요청"] --> P["이 플러그인<br/>(프록시 안내 데스크)"]
    P --> K1["KRX<br/>주식 시세"]
    P --> K2["법원<br/>경매 공고"]
    P --> K3["국토부<br/>실거래가"]
    P --> K4["통계청<br/>공공 통계"]
    K1 --> R["정리된 결과 반환"]
    K2 --> R
    K3 --> R
    K4 --> R

    style U fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style P fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style R fill:#e6f0ef,stroke:#144a46,color:#09110f
```

- **별도 API 키 불필요** — 프록시 경유 호출이라 사용자가 KRX·실거래가 API 키를 발급하거나 MCP 서버를 설치할 필요가 없습니다
- **read-only 조회** — 데이터를 수정·발송하지 않는 조회 전용. 시세는 일별 snapshot이며 실시간 호가·체결은 제공하지 않습니다

{{< hint type="caution" >}}
**조회 면책 고지**: 본 플러그인의 시세·통계 조회 결과는 정보 제공 목적이며, 투자 자문이 아닙니다. 실시간 호가·체결은 제공하지 않습니다. 실제 거래·투자·입찰 결정은 공식 출처와 전문가 확인을 거치세요.
{{< /hint >}}

## 설치

{{< tabs "install-public-data" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-public-data` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-public-data)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬 (4개)

| 스킬 | 용도 |
|---|---|
| `korean-stock-search` | KRX(한국거래소) 상장 종목 검색 + 종목 기본정보·일별 시세 조회 (read-only 일별 snapshot) |
| `court-auction-search` | 대법원 법원경매정보 부동산 매각공고를 매각기일·법원·기준으로 조회. 사건번호 단건 직접 조회 지원 |
| `real-estate-search` | 국토교통부 실거래가로 아파트·오피스텔·연립다세대·단독다가구·상업업무용 매매·전월세 시세 조회 |
| `public-data` | 공공데이터포털(data.go.kr)·KOSIS 통계청 실시간 통계 조회·분석 |

## 한국 공공 데이터 특화

주식과 부동산 시세에는 두 종류가 있습니다. 생중계 영상처럼 매 순간 변하는 가격이 있고, 하루를 정리한 인화 사진처럼 마감 시점의 가격이 있습니다. 이 플러그인은 '인화 사진'을 찾아볼 수 있지만 '생중계'는 제공하지 않습니다.

실시간 호가(지금 당장 매수·매도 주문이 걸려 있는 가격)와 체결(방금 거래가 성사된 가격)은 매 초 변하는 생중계에 해당합니다. 초단타 매매를 하려면 이 생중계가 필수지만, 이 플러그인은 그 실시간 흐름을 다루지 않습니다. 대신 일별 snapshot(하루 거래가 끝난 마감 시점의 가격표)을 조회합니다. "지난 한 달 삼성전자 일별 시세가 어땠나" 같은 질문에는 답하지만, "지금 당장 호가창이 어떻게 되나" 같은 질문은 이 플러그인의 영역 밖입니다. 같은 이유로 부동산 실거래가도 '오늘 당장의 시세'가 아니라 '최근에 실제로 거래된 가격 기록'을 보여줍니다.

- **국토부 실거래가** — 단지·면적·거래유형(매매/전세/월세)별 시세
- **법원경매** — 사건번호·용도·주소·감정평가액·최저매각가
- **KRX 종목** — 종목 기본정보 + 일별 시세 snapshot
- **공공데이터포털·KOSIS** — 인구·경제·산업 통계 직접 조회

## 대표 체인

**부동산 조사 + 보고**

```text
real-estate-search(실거래가 조회) → moai-content:html-report(단일 HTML 보고서)
```

**통계 조회 + 시각화**

```text
public-data(KOSIS 통계 조회) → moai-data:data-visualizer(차트) → moai-content:html-report
```

**경매 물건 검토**

```text
court-auction-search(매각공고 조회) → real-estate-search(주변 시세 비교)
```

## 사용 예시

{{< terminal title="claude — cowork" >}}
> 잠실 리센츠 2024년 매매 실거래가 찾아줘
{{< /terminal >}}

→ `real-estate-search` 자동 호출 → 국토부 실거래가 조회 → 면적·층·거래일별 매매가 정리.

{{< terminal title="claude — cowork" >}}
> 삼성전자 최근 일별 시세 조회해줘
{{< /terminal >}}

→ `korean-stock-search` 자동 호출 → KRX 종목 검색 → 종목 기본정보 + 일별 snapshot 시세.

{{< terminal title="claude — cowork" >}}
> 강남구 아파트 경매 매각공고 보여줘
{{< /terminal >}}

→ `court-auction-search` 자동 호출 → 매각기일·법원 기준 공고 조회 → 사건번호·감정평가액·최저매각가 정리.

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 개인 자산관리·재테크 로드맵 | [`moai-wealth`](../moai-wealth/) `wealth-roadmap` |
| 법인 세무·K-IFRS 재무제표 | [`moai-finance`](../moai-finance/) `financial-statements` |
| CSV 탐색·자체 데이터 분석 | [`moai-data`](../moai-data/) `data-explorer` |
| 조회한 데이터를 차트로 시각화 | [`moai-data`](../moai-data/) `data-visualizer` |

## 다음 단계

- [`moai-data`](../moai-data/) — 조회 데이터의 탐색·시각화
- [`moai-wealth`](../moai-wealth/) — 개인 자산관리·재테크
- [`moai-finance`](../moai-finance/) — 법인 세무·재무제표

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-public-data 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-public-data)
- [국토교통부 실거래가 공개시스템](https://rt.molit.go.kr/)
- [대법원 법원경매정보](https://www.courtauction.go.kr/) · [공공데이터포털](https://www.data.go.kr/) · KOSIS 국가통계포털
