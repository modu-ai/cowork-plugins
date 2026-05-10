---
name: court-auction-search
description: |
  대법원 법원경매정보(courtauction.go.kr) 부동산 매각공고를 매각기일·법원·기일/기간
  입찰 기준으로 조회하고, 각 공고를 사건번호·용도·주소·감정평가액·최저매각가로
  펼쳐서 보여줍니다. 법원사무소 코드와 사건번호로 단건 직접 조회도 지원합니다.
  read-only이며 IP 차단 방지를 위해 호출당 약 2초 지연을 둡니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "오늘 어디서 부동산 경매 열려?", "내일 매각공고 보여줘"
  - "서울중앙지방법원 2026-04-27 매각공고", "기일입찰만 보여줘"
  - "사건번호 2024타경100001 진행 상황 알려줘"
  - "법원 경매 매각공고", "courtauction.go.kr", "경매 사건 검색"
  - "감정평가액 최저매각가", "매각기일별 결과", "유찰 횟수"
  - 자산 처분·경매 투자·실사 검토 시
user-invocable: true
version: 2.2.1
---

# 법원경매 매각공고 조회

대법원이 운영하는 공식 **법원경매정보**(`courtauction.go.kr`)의 매각공고와 사건정보를 JSON으로 변환해 돌려줍니다. 자산 처분·경매 투자·실사 검토에 사용합니다.

> 본 스킬은 NomaDamas k-skill `court-auction-notice-search` (MIT)를 cowork에 포팅했습니다. 공식 OPEN API가 없어 사이트 내부 WebSquare JSON XHR endpoint를 직접 호출합니다.

## Mandatory honest framing — 사용자에게 항상 알려야 할 사실

1. 데이터는 법원경매정보 사이트의 공개 정보를 그대로 옮긴 것이며 **실제 입찰 전에는 법원 원문을 재확인**해야 합니다.
2. 사이트는 자동화 호출에 매우 민감해서 **빠른 연속 조회 시 IP가 1시간 차단**될 수 있습니다.
3. 가격(감정평가액·최저매각가)·매각기일·매각장소는 **공고 시점 기준**이며 정정·취하·연기로 변경될 수 있습니다 (`correctionCount`, `cancellationCount` 참고).
4. 본 스킬은 **read-only**입니다. 입찰 자체는 자동화하지 않습니다.

## Throttling — 매우 중요

- 호출 간 **최소 2초** 지연 (기본). 더 늘리려면 `--min-delay-ms 3000`.
- 기본 세션 호출 budget **10회**. 초과 시 새 세션 또는 `maxCallsPerSession` 명시 증가.
- 차단(`data.ipcheck === false`)을 만나면 `BLOCKED` 에러를 즉시 throw하고 멈춥니다 (자동 retry 금지 — 차단 연장 위험).
- 차단된 IP는 **약 1시간 후** 자연 복구. 그 사이에는 다른 IP/네트워크에서 작업하거나 사용자가 브라우저로 사이트에 접속해서 차단 해제 화면을 거칩니다.

## When to use / When not to use

**사용**: 매각공고 일자별 조회, 사건번호 단건 조회, 법원사무소 코드표 조회, 매각공고 펼치기.

**사용 금지**: 동산(자동차·중기) 경매(v1 범위 밖), 자유 조건검색(지역·용도·가격대·면적·유찰횟수), 날짜별 전체 법원 일정 한 번에, 매각물건 사진 URL, 매각물건명세서·현황조사서·감정평가서 PDF 다운로드, **입찰서 자동 작성·자동 제출 (절대 미지원)**.

## Inputs

- `date`: 매각기일 월(`YYYYMM`/`YYYY-MM`) 또는 특정일(`YYYYMMDD`/`YYYY-MM-DD`). 필수.
- `courtCode`: 법원사무소코드 (예: `B000210` = 서울중앙지방법원). 비우면 전체.
- `bidType`: `date`(기일입찰, 000331) | `period`(기간입찰, 000332) | 빈값(둘 다).
- `caseNumber`: 사건번호. `2024타경100001` 권장. `2024-100001`도 정규화.

## Endpoints (사이트 내부 직접 호출)

- `POST /pgj/pgj143/selectRletDspslPbanc.on` — 매각공고 목록
- `POST /pgj/pgj143/selectRletDspslPbancDtl.on` — 매각공고 상세 (사건/물건 펼치기)
- `POST /pgj/pgj15A/selectAuctnCsSrchRslt.on` — 사건 단건 조회
- `POST /pgj/pgjComm/selectCortOfcCdLst.on` — 법원사무소코드 전체

1차 transport는 직접 HTTP, 차단·5xx 시에만 `rebrowser-playwright` 또는 `playwright-core` fallback.

## Workflow A — 매각공고 → 사건/물건 펼치기

1. 사용자에게 매각기일(YYYY-MM-DD)과 (선택) 법원·입찰구분을 받습니다.
2. `searchSaleNotices({ date, courtCode, bidType })` → 매각공고 카드 목록.
3. 카드 객체(또는 `raw`)를 그대로 `getSaleNoticeDetail(notice)`에 넘깁니다.
4. 응답의 `items[]`가 `caseNumber`, `usage`, `address`, `appraisedPrice`, `minimumSalePrice`, `remarks`를 가집니다.
5. 가격은 원 단위 정수. 사용자에게 보여줄 때는 한국식 천단위 콤마 + 억/만 단위 환산.

## Workflow B — 사건번호 단건 조회

1. 법원사무소코드 + 사건번호(예: `2024타경100001`)를 받습니다.
2. `getCaseByCaseNumber({ courtCode, caseNumber })` 호출.
3. `found:false / status:204` → 사건 미존재·비공개. 형식·법원 재확인.
4. `found:true` → `caseInfo`(사건명·접수일·청구액·재판부·진행상태), `items[]`(매각목적물·주소·배당요구종기), `schedule[]`(매각기일별 최저가·감정가·결과), `claimDeadline`, `relatedCases`, `stakeholders`.

## helper 실행

본 스킬은 npm 패키지 `court-auction-notice-search`(NomaDamas/k-skill 원본)를 호출하는 Node.js 예시 스크립트를 `scripts/court_auction_example.js`에 포함합니다. 직접 CLI 사용도 가능합니다.

```bash
# 사전 설치
npm i court-auction-notice-search

# 1. 법원사무소 코드표
court-auction-notice-search codes courts --pretty | head -40

# 2. 입찰구분 (정적 코드)
court-auction-notice-search codes bid-types --pretty

# 3. 매각공고 목록
court-auction-notice-search notices \
  --date 2026-04 --court-code B000210 --bid-type date --pretty

# 4. 사건번호 단건 조회
court-auction-notice-search case \
  --court-code B000210 --case-number "2024타경100001" --pretty

# 5. 통합 예시 (Node.js)
node scripts/court_auction_example.js
```

## Error handling

| 에러 코드 | 의미 | 대응 |
|---|---|---|
| `BLOCKED` | `data.ipcheck === false` | 1시간 대기 후 다른 IP에서 재시도 |
| `BUDGET_EXCEEDED` | 세션 budget 초과 | 의도적 안전장치. 필요시 `--max-calls 20` |
| `UPSTREAM_ERROR` | 사이트 일반 에러 | 세션 만료/잘못된 jdbnCd. warmup부터 재시작 |
| `NETWORK_ERROR` | 타임아웃·연결 실패 | 네트워크 점검 |
| `PLAYWRIGHT_UNAVAILABLE` | fallback 모듈 없음 | `npm i rebrowser-playwright` 또는 `playwright-core` |

## Response policy

- 첫 응답에 **IP 차단 위험**과 **"참고용·실제 입찰 전 법원 원문 재확인"** 고지를 답니다.
- 가격은 원 단위 정수 + 억/만 단위 환산을 같이 제시합니다.
- 차단 발생 시 자동 재시도하지 않고 즉시 멈추고 사용자에게 안내합니다.
- 작업 후 호출 budget 잔량을 사용자에게 알려 추가 호출 여지를 명시합니다.

## 관련 스킬 체이닝

- **before**: `moai-business:real-estate-search` — 매물 시세 비교 (인근 실거래가)
- **after**: `moai-finance:financial-statements` — 경매 투자 타당성 분석
- **after**: `moai-bi:executive-summary` — 경매 후보 1pager
- **after**: `moai-office:xlsx-creator` — 매각공고 일괄 엑셀화

## Done when

- IP 차단 위험과 "참고용·실제 입찰 전 법원 원문 재확인" 고지를 했다.
- 매각공고를 펼쳐서 `caseNumber/usage/address/appraisedPrice/minimumSalePrice` JSON을 돌려줬다.
- 사건번호 직접 조회시 `found:false`일 때 후속 조치를 안내했다.
- 차단 발생시 자동 재시도하지 않고 즉시 멈췄다.
- 호출 budget 잔량을 사용자에게 알렸다.