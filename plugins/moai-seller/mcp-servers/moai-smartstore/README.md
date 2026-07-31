# moai-smartstore-mcp

네이버 커머스(스마트스토어) 전 도메인 운영/관리 MCP 서버 — 네이버 커머스 API 센터의 공식 API 를 MCP(Model Context Protocol) 도구로 노출하여, Cowork/Claude Code 환경에서 상품·주문·정산·문의·물류·판매자정보·커머스솔루션·통계 운영을 자연어로 수행.

> **공식 문서**: https://apicenter.commerce.naver.com — 인증·전자서명 규격은 공식 인증 문서(https://apicenter.commerce.naver.com/docs/auth)를 따른다.

## 개요

9개 도메인(~140 엔드포인트)을 **90개 MCP 도구**로 래핑. 전체 도구 목록은 `manifest.json` 또는 `moai-smartstore-mcp` 실행 후 `tools/list` 로 확인.

| 도메인 | 도구 예시 |
|-------|----------|
| 인증 | `smartstore_test_connection`, `smartstore_config_status` |
| 상품 | `product_search`, `product_create`, `product_update_stock`, `product_change_status`, `category_list` … |
| 주문 | `order_list_product_orders`, `order_changed_product_orders`, `order_dispatch`, `order_return_approve` … |
| 정산 | `settlement_daily`, `settlement_case`, `vat_daily` … |
| 문의 | `qna_list`, `qna_answer`, `customer_inquiry_answer` … |
| 물류/N배송 | `logistics_companies`, `sku_list`, `sku_get` … |
| 판매자정보 | `seller_account`, `seller_channels`, `addressbook_list` … |
| 커머스솔루션 | `solution_subscription_get`, `solution_approve` … |
| 통계 | `stats_marketing`, `stats_sales`, `stats_shopping`, `stats_customer_status` … |

## 실 API 연동 검증 (2026-07-10)

실 자격증명(SELF 타입 앱)으로 **read-only GET** 호출만 수행해 종단간 연동을 검증했다.
쓰기(POST/PUT/PATCH/DELETE) 도구는 테스트에서 **0건 호출**했다.

- **인증**: OAuth2 토큰 발급 성공 — bcrypt 전자서명(`$2a$04$` 형식 진짜 salt)이 bcrypt 5.x 에서 정상 동작.
- **MCP stdio E2E**: 서버 spawn → `initialize` 핸드셰이크(MCP v1.28.1) → `call_tool("category_list")` → **5,827개 실제 카테고리 반환**(패션의류 등).
- **실데이터 반환 그룹**: 상품(카테고리·원산지·공지), 정산(daily), 문의(Q&A 10건, `maskedWriterId` 로 개인정보 마스킹).

> ⚠️ 자격증명은 `.env`/코드/로그에 하드코딩하지 말고 **인라인 환경변수**로만 주입하고,
> 테스트 후 네이버 커머스 API 센터에서 **시크릿 재발급(rotate)** 한다.

## API 그룹별 승인 현황

네이버 커머스 API 는 **API 그룹별로 사전 사용신청(스코프 승인)** 이 필요하다. 앱 등록만으로는
전 그룹이 열리지 않는다. 아래 표는 2026-07-10 SELF 앱으로 실측한 결과.

**상태 판별 키**: 토큰 발급이 성공한 뒤 —
`403 GW.AUTHN` = 해당 그룹 **미승인**(사용신청 필요) / `400 (필수 파라미터 누락)` = **승인됨**(파라미터만 맞추면 됨, 403 과 혼동 금지) / `200` = 정상.

| 그룹 | 상태 | 비고 |
|---|---|---|
| 상품 (products) | ✅ 승인·실데이터 | `category_list`, `product_origin_areas`, `seller_notices` 200 |
| 정산 (settlement) | ✅ 승인·실데이터 | `settlement_daily` 200 (elements + pagination) |
| 문의 (inquiries) | ✅ 승인·실데이터 | `qna_list` 200 (10건, `fromDate`/`toDate` ISO-8601 필수) |
| 주문 (orders) | ✅ 승인됨 | `order_changed_product_orders` 400(파라미터) — 도구 문서 이슈는 [알려진 이슈](#알려진-이슈) 참조 |
| 통계 (stats) | ⚠️ 별도 신청 | **API 데이터솔루션** 제품의 별도 사용신청이 선행 필요 (일반 API 그룹 승인과 상이) |
| 판매자정보 (seller) | ❌ 미승인 | `seller_account` 403 → 사용신청 필요 |
| 물류 (logistics) | ❌ 미승인 | `logistics_companies` 403 → 사용신청 필요 |
| 커머스솔루션 (solutions) | ❌ 미승인 | `solution_*` 403 → 사용신청 필요 |

사용신청은 [apicenter.commerce.naver.com](https://apicenter.commerce.naver.com) 에서 각 API 그룹별로 진행한다.

## 설치 및 실행

```bash
# uvx로 직접 실행
uvx moai-smartstore-mcp

# 버전 확인
uvx moai-smartstore-mcp --version

# 개발 환경
pip install -e ".[dev]"
pytest tests/
```

플러그인 vendor 모델 — `uv run --directory ./mcp-servers/moai-smartstore moai-smartstore-mcp` 로 end-user 기동 시 `.venv` 가 자동 생성된다(gitignored).

## 환경변수

자격증명은 반드시 환경변수로 주입. 코드·manifest·로그에 하드코딩 절대 금지.

```bash
export NAVER_COMMERCE_CLIENT_ID="<애플리케이션 ID>"
export NAVER_COMMERCE_CLIENT_SECRET="<애플리케이션 시크릿(bcrypt salt)>"
export NAVER_COMMERCE_ACCOUNT_ID="<판매자 계정 ID>"   # type=SELLER 시 필수
export NAVER_COMMERCE_TYPE="SELF"                       # SELF(기본) | SELLER
```

발급 절차는 `CONNECTORS.md` 참고.

## 인증

OAuth2 Client Credentials Grant + bcrypt 전자서명.

- 전자서명 = `base64(bcrypt(client_id + "_" + timestamp, client_secret))`
- timestamp 는 밀리초 단위, 5분 유효.
- `client_secret` 자체가 bcrypt salt 로 사용된다 — 운영 시크릿은 `bcrypt.gensalt()` 로 만들어진 **진짜 bcrypt salt**다. 공식 문서 예시의 placeholder(`$2a$10$abcdefghijklmnopqrstuv`)는 bcrypt 5.x 가 "Invalid salt" 로 거부하므로 테스트에서도 `gensalt()` 결과를 써야 한다(`tests/test_auth.py` 참조).
- **401** + `GW.AUTHN` 응답 시 토큰 만료로 간주해 자동 재발급 후 1회 재시도.
- **403** + `GW.AUTHN` 은 토큰 만료가 **아니다** — [API 그룹 미승인](#api-그룹별-승인-현황)을 의미한다. 자격증명 교체가 아니라 사용신청으로 해결한다.

## 사용 예 (MCP 클라이언트 관점)

```
# 카테고리 전체 조회 (참조 데이터, 파라미터 불필요)
category_list()

# 상품 검색 (POST /v1/products/search — 본문 조건)
product_search(body={"keyword": "티셔츠", "size": 20})

# 상품 주문 변경 피드 (OMS/CRM 동기화, ISO-8601)
order_changed_product_orders(params={"lastChangedFrom": "2026-07-01T00:00:00+09:00"})

# 상품 Q&A 미답변 모니터링 (fromDate/toDate ISO-8601 필수)
qna_list(params={"fromDate": "2026-07-01T00:00:00+09:00", "toDate": "2026-07-09T23:59:59+09:00"})

# 일별 정산
settlement_daily(params={"startDate": "2026-07-01", "endDate": "2026-07-09"})

# 판매자 계정 정보 (그룹 승인 필요)
seller_account()
```

> 쓰기 도구(`product_create`, `order_dispatch`, `qna_answer`, `order_return_approve` 등)는 운영
> 데이터를 변경하므로 신중하게 사용한다.

## 알려진 이슈

1. **`scripts/check_auth.py` ImportError (Python 3.14)** — line 20 `from pathlib import AnyPath` 가
   실패(`AnyPath` 미존재). `pathlib.Path` 로 수정 필요. 현재 실인증 검증은 `NaverCommerceClient`
   코드 경로를 직접 사용하는 우회로 수행됨.
2. **`order_changed_product_orders` 도구 문서 불일치** — docstring 의 params 예시는
   `fromDateString` 이나 실제 API 가 요구하는 필수 필드는 `lastChangedFrom`(ISO-8601)이다.
   도구 메타데이터 정정 필요.

## 아키텍처

```
src/moai_smartstore/
  __main__.py    # 진입점(--version 처리 후 stdio run)
  server.py      # FastMCP 인스턴스(mcp 공유 객체)
  auth.py        # bcrypt 전자서명 generate_signature
  client.py      # NaverCommerceClient: 토큰 발급/캐싱 · 401 GW.AUTHN 재시도 · 도메인 호출
  config.py      # Config.from_env() — 환경변수 주입, is_configured 검증
  errors.py      # AuthError / ApiError
  tools/
    _common.py   # call() 헬퍼 — 자격증명 검증 + API 호출 + 안전한 dict 래핑
    auth.py      # 인증/설정 도구 (test_connection, config_status)
    products.py  # 상품·카테고리·공지 (가장 큼)
    orders.py    # 주문·클레임(취소/반품/교환)
    settlement.py# 정산·VAT
    inquiries.py # Q&A·고객문의
    logistics.py # 물류사·출고지·SKU
    seller.py    # 판매자정보·주소록·오늘출발
    solutions.py # 커머스솔루션 구독/승인
    stats.py     # 통계(API데이터솔루션 — 별도 사용신청)
scripts/
  check_auth.py  # 실인증 검증 스크립트(현재 ImportError — 알려진 이슈 #1)
tests/           # auth/client/server/tools 단위 테스트 (27건 PASS)
```

## 라이선스

Apache-2.0 (모두의 코워크 플러그인 패밀리).
