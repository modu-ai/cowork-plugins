---
name: commerce-local-inventory-search
description: |
  한국 오프라인 커머스 재고·매장·상품 조회 전담 스킬입니다. 다이소, GS25, CU, 세븐일레븐, 이마트24, 롯데마트, 올리브영에서 상품을 찾거나 근처 매장 재고를 확인해야 할 때 사용하세요. upstream daiso CLI와 공개 MCP endpoint를 사용하며, 구매·예약·결제·로그인 자동화는 하지 않습니다.
user-invocable: true
version: 2.10.0
---

# 로컬 커머스 재고 조회 (Commerce Local Inventory Search)

## 개요

한국 오프라인 커머스의 상품, 매장, 재고를 `daiso` CLI로 조회하는 스킬입니다.
사용자가 "근처 다이소 재고", "GS25 콜라 있는 매장", "올리브영 선크림 재고"처럼 물으면 먼저 공개 조회를 수행하고, 결과를 매장명·주소·가격·재고 중심으로 짧게 정리합니다.

upstream은 `hmmhmmhm/daiso-mcp`와 npm package `daiso`입니다. 이 스킬은 코드를 vendoring하지 않고 CLI와 공개 MCP endpoint 사용법만 안내합니다.

## 트리거 키워드

다이소 재고, 다이소 상품, GS25 재고, CU 재고, 세븐일레븐 재고, 이마트24 상품, 롯데마트 상품, 올리브영 재고, 근처 매장, 편의점 재고, 매장 검색, 상품 위치, 오프라인 재고 조회, `daiso`, `daiso-mcp`

## 책임 경계

| 항목 | 처리 |
| --- | --- |
| 상품 검색 | 상품명, 가격, ID, 후보 정리 |
| 매장 검색 | 지역 키워드 기준 매장명, 주소, store code 정리 |
| 재고 확인 | 상품과 위치가 모두 있을 때 재고 조회 |
| 진열 위치 | 다이소 상품 ID와 매장 코드가 있을 때 display location 조회 |
| 구매·예약·결제 | 자동화하지 않음 |
| 로그인 세션 | 요구하지 않음 |

## 사전 조건

- Node.js 20 이상 권장
- `npx` 사용 가능
- 인터넷 연결
- 반복 사용 시 `npm install -g daiso`

빠른 상태 확인:

```bash
npx --yes daiso health
npx --yes daiso url
```

MCP endpoint:

```text
https://mcp.aka.page
```

## 워크플로우

### 1. 서비스와 의도 분류

사용자 요청에서 서비스와 목적을 먼저 분리합니다.

| 요청 | 우선 명령 |
| --- | --- |
| "다이소 수납박스 찾아줘" | `products` |
| "강남역 다이소 매장" | `stores` |
| "강남역 다이소에 수납박스 있나" | `products` 후 `inventory` |
| "GS25 콜라 재고" | `gs25-inventory` |
| "올리브영 명동 선크림 재고" | raw `get /api/oliveyoung/inventory` |
| "롯데마트 강변점 콜라" | `lottemart-products` |

상품과 위치가 모두 있으면 상품 검색만 하지 말고 재고 조회까지 진행합니다. 위치가 없으면 바로 묻습니다.

```text
어느 지역이나 매장을 기준으로 볼까요? 예: 강남역, 명동, 코엑스
```

### 2. 다이소 조회

```bash
npx --yes daiso products 수납박스 --json
npx --yes daiso stores 강남역 --limit 5 --json
npx --yes daiso inventory 1034604 --keyword 강남역 --json
npx --yes daiso display-location 1034604 04515 --json
```

상품명이 주어졌고 상품 ID가 없으면 `products` 결과에서 가장 관련 있는 후보 2개에서 3개를 먼저 제시합니다. 사용자가 고르면 `inventory`로 이어갑니다.

### 3. 편의점 조회

```bash
npx --yes daiso gs25-products 콜라 --limit 10 --json
npx --yes daiso gs25-stores 강남 --limit 10 --json
npx --yes daiso gs25-inventory 오감자 --storeKeyword 강남 --storeLimit 10 --json
npx --yes daiso seveneleven-products 삼각김밥 --size 10 --json
npx --yes daiso seveneleven-stores "안산 중앙역" --limit 10 --json
npx --yes daiso get /api/seveneleven/inventory --keyword 핫식스 --storeKeyword "안산 중앙역" --storeLimit 10 --json
npx --yes daiso get /api/cu/inventory --keyword 생수 --storeKeyword 강남 --storeLimit 10 --json
```

편의점 재고는 변동이 빠릅니다. 최종 답변에는 조회 시각과 변동 가능성을 함께 적습니다.

### 4. 마트·H&B 조회

```bash
npx --yes daiso emart24-products 커피 --pageSize 10 --json
npx --yes daiso lottemart-products 콜라 --storeName 강변점 --area 서울 --json
npx --yes daiso get /api/oliveyoung/stores --keyword 명동 --limit 5 --json
npx --yes daiso get /api/oliveyoung/products --keyword 선크림 --size 5 --json
npx --yes daiso get /api/oliveyoung/inventory --keyword 선크림 --storeKeyword 명동 --size 5 --json
```

올리브영과 일부 공개 endpoint는 간헐적인 5xx나 빈 응답이 날 수 있습니다. 한두 번 재시도한 뒤에도 실패하면 실패한 서비스와 명령을 그대로 보고합니다.

### 5. 응답 형식

응답은 길게 늘리지 않고 필요한 필드만 정리합니다.

```text
기준: GS25 강남
상품: 오감자

1. GS25 강남○○점
   주소: ...
   재고: ...

2. GS25 ...
   주소: ...
   재고: ...

재고는 조회 시점 기준이라 방문 전 매장 확인이 필요합니다.
```

## 사용 예시

```text
사용자: 강남역 근처 다이소 수납박스 재고 찾아줘
실행:
1. npx --yes daiso products 수납박스 --json
2. npx --yes daiso inventory <productId> --keyword 강남역 --json
```

```text
사용자: 명동 올리브영에 선크림 있나 봐줘
실행:
npx --yes daiso get /api/oliveyoung/inventory --keyword 선크림 --storeKeyword 명동 --size 5 --json
```

```text
사용자: 강남 GS25 오감자 재고
실행:
npx --yes daiso gs25-inventory 오감자 --storeKeyword 강남 --storeLimit 10 --json
```

## 실패 처리

- `npx`가 없으면 MCP endpoint `https://mcp.aka.page`와 대응 API path를 안내합니다.
- network 오류는 한 번 재시도하고, 같은 오류면 실패한 서비스와 명령을 보고합니다.
- 결과가 없으면 더 넓은 키워드나 가까운 지역을 제안합니다.
- 구매, 예약, 결제, 로그인 자동화는 요청받아도 진행하지 않습니다.

## 출처

- upstream repo: `https://github.com/hmmhmmhm/daiso-mcp`
- npm package: `https://www.npmjs.com/package/daiso`
- MCP endpoint: `https://mcp.aka.page`
