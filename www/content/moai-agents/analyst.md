---
title: "「데이터 애널리스트」 — 공공데이터·데이터 분석 담당"
weight: 7
description: "부동산·경매·주식·KOSIS·건축물대장·DART 공공데이터 조회와 데이터 시각화를 담당하는 데이터 분석 AI 직원."
aliases: ["/agent-teams/analyst/"]
---

"이 동네 아파트 시세와 최근 경매 이력 알 수 있을까?" 같은 질문은 정보가 흩어져 있어 직접 모으기 어렵습니다. 데이터 애널리스트는 공공데이터와 통계를 모아 한눈에 정리해 주는 직원입니다. 동네 복지센터의 베테랑 정보 담당자처럼, 어느 기관에서 무엇을 가져와야 하는지 알고 있습니다.

스킬은 7종입니다. 공공데이터 계열(office-public-data-\*)은 부동산·법원 경매·한국 주식·건축물대장·DART 전자공시 조회를, 데이터 계열(office-data-\*)은 데이터 프로파일링·시각화를 다룹니다. 이전 버전에서 사무관(문서·오피스)으로부터 데이터 도메인이 분리되어 신설되었습니다. korean-stats(KOSIS 통계)·archhub(건축물대장)·dart(전자공시) 세 개의 MCP(클로드가 외부 서비스와 연결되는 표준 통로)가 연동됩니다.

공공데이터는 숫자와 출처가 중요한 만큼, 출처와 계산을 검증하는 검수 직원이 붙어 있습니다.

```mermaid
flowchart LR
   A["요청<br/>(이 동네 경매 이력 알려줘)"] --> B["스킬 매칭"]
   B --> C["data-analyst<br/>데이터 조회·시각화"]
   C --> D["data-provenance-auditor<br/>출처·수치 검증"]
   D --> E["산출물<br/>(조사 노트·차트)"]
```

## 스킬 카탈로그

office-data-\* / office-public-data-\* / office-finance-\* 계열 공공데이터·시각화 스킬의 전체 목록입니다.

{{< employee-skills "moai-analyst" >}}

## 에이전트

**data-analyst**(실행 직원)가 공공데이터를 조회·시각화하고, **data-provenance-auditor**(검수 직원)가 읽기 전용으로 출처와 수치를 독립 검증합니다. "시세가 올랐다"는 주장을 그대로 믿지 않고 근거 데이터를 따져 보는 역할입니다.

{{< employee-agents "moai-analyst" >}}

## 대표 시나리오 3선

**1. 부동산 시세·경매 조사.** "이 주소 건축물대장이랑 최근 경매 이력 확인해줘"라고 하면 `office-building-ledger-search`와 `office-public-data-court-auction-search`가 공공데이터를 조회해 조사 노트로 정리합니다.

**2. KOSIS 통계 시각화.** "우리 지역 인구 추이를 KOSIS에서 찾아서 차트로 만들어줘"라고 하면 korean-stats MCP가 통계를 조회하고 `office-data-visualizer`가 차트로 시각화합니다.

**3. 기업 공시 분석.** "이 회사 최근 DART 공시 요약해줘"라고 하면 dart MCP로 전자공시를 조회해 요약합니다.

**잘 안 될 때** — 공공데이터 조회가 실패하면 해당 API 키(공공데이터포털·KOSIS·DART 등) 등록 여부를 먼저 확인하세요.

## MCP 연동

- **korean-stats** — KOSIS 국가통계 검색·조회·시계열 분석. KOSIS API 키가 필요할 수 있습니다.
- **archhub** — 건축물대장 조회. 공공데이터포털 API 키가 필요합니다.
- **dart** — 전자공시(DART) 기업 공시 조회. OpenDART API 키가 필요합니다.
