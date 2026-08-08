# moai-mcp-cafe24

> 카페24(Cafe24) 쇼핑몰 **Admin API + Analytics API** 전 기능을 다루는 MCP(Model Context Protocol) 서버.
> **526개 도구** · 선언적 엔드포인트 레지스트리 기반 동적 등록 · OAuth2 자동 갱신 · 이중 레이트리밋 준수.

## 개요

카페24 쇼핑몰의 운영/관리/분석 전 도메인을 하나의 MCP 서버로 다룹니다. 공식 REST API 문서
(`developers.cafe24.com`)의 두 서피스를 통합 커버합니다:

| 서피스 | 호스트 | 도메인 | 도구 수 |
|---|---|---|---|
| **Admin API** | `https://{mall_id}.cafe24api.com/api/v2/admin/` | 19 카테고리 (상점·상품·주문·회원·게시판·디자인·프로모션·앱·상품분류·판매분류·공급사·배송·매출통계·개인화정보·개인정보·적립금·알림·번역·접속통계) | 502 |
| **Analytics API** | `https://ca-api.cafe24data.com` | 방문자·매출·광고·키워드·방문경로 통계 | 24 |

**카테고리별 도구 수:** analytics 24 · analytics_admin 1 · application 19 · category 18 ·
collection 15 · community 23 · customer 21 · design 8 · mileage 8 · notification 12 ·
order 105 · personal 5 · privacy 6 · product 80 · promotion 32 · salesreport 5 ·
shipping 14 · store 102 · supply 19 · translation 9 — **합계 526**.

## 아키텍처: 선언적 레지스트리

300+ 엔드포인트를 일일이 함수로 작성하는 대신, 각 API 연산을 `Endpoint` 데이터 레코드로
선언하고 `_dispatch`가 시작 시 각 레코드를 typed FastMCP 도구로 컴파일합니다.

```
src/moai_mcp_cafe24/
  _base.py        # 환경설정(env 자격증명 + 토큰 영속화) + 싱글톤 클라이언트
  auth.py         # OAuth2 refresh (refresh-token 회전)
  client.py       # 이중 서피스 HTTP + 버전헤더 + Leaky Bucket/Usage 레이트리밋 + 401재시도 + 페이지네이션
  registry.py     # Endpoint/Param 스키마 + 전역 REGISTRY
  _app.py         # 공유 FastMCP 인스턴스
  server.py       # 엔트리포인트 (레지스트리 → 도구 컴파일 → run)
  tools/
    _dispatch.py          # Endpoint → typed 도구 동적 등록
    analytics_data.py     # cafe24data 24 엔드포인트
    {product,order,store,...}.py  # Admin 19 도메인
```

모든 도구는 명명된·타입화된 매개변수 + 자동 독스트링을 갖습니다(범용 blob 아님).

## 인증 (OAuth2)

카페24는 OAuth2 `authorization_code` 플로우를 사용합니다. access_token(2시간) + refresh_token(2주).
**refresh_token은 갱신마다 회전** — 기존 토큰 무효화, 새 토큰 반환(자동 영속화).

### 1회성 토큰 발급 절차

1. **개발자센터 앱 생성** — developers.cafe24.com 로그인 → Apps → 개발정보에서
   `client_id` / `client_secret` / Redirect URL 확보. 필요 `scope` 지정
   (예: `mall.read_product mall.write_product mall.read_order ...`).
2. **인증코드 발급** (웹브라우저에서만 — cURL 불가):
   ```
   https://{mall_id}.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={redirect_uri}&scope={scope}
   ```
   → 리다이렉트 URL로 `code={authorize_code}` 수신(1분간 유효, 재사용 불가).
3. **토큰 교환** — `code`를 access/refresh 토큰으로 교환 (개발자센터 "Get Access Token" 예시 참조).
4. 발급받은 `access_token` / `refresh_token`을 `.mcp.json` env에 설정.

만료 시 MCP 서버가 자동으로 refresh_token으로 갱신합니다(401 → 1회 refresh+재시도).
refresh_token 자체가 만료(2주)되면 위 절차를 다시 밟아야 합니다.

## 설치

```bash
# uv 필수 (없으면): curl -LsSf https://astral.sh/uv/install.sh | sh
cd plugins/moai-seller/mcp-servers/moai-mcp-cafe24
uv sync
```

소스는 플러그인에 자체 vendor — PyPI 게시 불필요, 설치 즉시 작동.

## 환경변수

| 변수 | 필수 | 설명 |
|---|---|---|
| `CAFE24_MALL_ID` | ✓ | 쇼핑몰 아이디 (Admin 호스트의 서브도메인) |
| `CAFE24_CLIENT_ID` | ✓ | 앱 client_id |
| `CAFE24_CLIENT_SECRET` | ✓ | 앱 client_secret |
| `CAFE24_ACCESS_TOKEN` | ✓ | access_token (2h, 자동갱신) |
| `CAFE24_REFRESH_TOKEN` | ✓ | refresh_token (2w, 회전) |
| `CAFE24_API_VERSION` | | API 버전 (기본 `2026-03-01` — 앱 기본값; `2025-09-01` 단종) |
| `CAFE24_SHOP_NO` | | 기본 멀티샵 번호 (기본 1) |
| `CAFE24_TIMEOUT` | | HTTP 타임아웃 초 (기본 30) |
| `CAFE24_REQUEST_DELAY` | | 요청 간 최소 대기 초 (기본 0, 옵션) |
| `CAFE24_TOKEN_FILE` | | 토큰 영속화 경로 (기본 `~/.moai/mcp/cafe24-tokens.json`) |

## .mcp.json 등록 (이미 플러그인에 반영됨)

```jsonc
"moai-cafe24": {
  "command": "uv",
  "args": ["run", "--directory", "./mcp-servers/moai-mcp-cafe24", "moai-mcp-cafe24"],
  "env": {
    "CAFE24_MALL_ID": "${CAFE24_MALL_ID}",
    "CAFE24_CLIENT_ID": "${CAFE24_CLIENT_ID}",
    "CAFE24_CLIENT_SECRET": "${CAFE24_CLIENT_SECRET}",
    "CAFE24_ACCESS_TOKEN": "${CAFE24_ACCESS_TOKEN}",
    "CAFE24_REFRESH_TOKEN": "${CAFE24_REFRESH_TOKEN}"
  }
}
```

## 도구 호출 패턴

모든 도구는 `cafe24_{category}_{operation}` 명명 규칙을 따릅니다.

```text
# 상품 목록 조회 (GET, 필터 + 페이지네이션)
cafe24_product_list(product_name="셔츠", limit=10, shop_no=1)

# 상품 상세 (경로 매개변수)
cafe24_product_get(product_no=128, embed="variants,inventories")

# 상품 생성 (body는 resource_key로 자동 래핑: {"product": {...}})
cafe24_product_create(body={"product_name": "티셔츠", "price": 10000, "supply_price": 7000})

# 다건 배송처리
cafe24_shipment_create_bulk(body=[{"order_id": "O1", "tracking_no": "...", "shipping_company_code": "kr.post", "status": "shipping"}])

# Analytics — mall_id는 config에서 자동 주입
cafe24_analytics_visitors_pageview(start_date="2026-01-01", end_date="2026-01-31")

# 전체 페이지 자동 수집 (offset 자동 증가)
cafe24_order_list(start_date="2026-01-01", end_date="2026-01-31", date_type="order_date", paginate=True)
```

**매개변수 규칙:**
- `{product_no}` 같은 경로 매개변수 → 필수 인수
- 선언된 query 매개변수 → 선택적 typed 인수
- 모든 도구 → `shop_no`(선택, 미제공시 config 기본값)
- POST/PUT 도구 → `body: dict` (dispatcher가 `{"<resource_key>": body}`로 래핑)
- 목록 도구 → `paginate: bool` / `max_pages: int` (offset 자동 페이지네이션)

**타입 강제:** bool → `T`/`F`, list → 콤마 조인, `None` → 자동 제거 (Cafe24 규칙).

## 레이트리밋

카페24는 두 가지 제한을 병용 — 본 서버가 모두 준수:

1. **Leaky Bucket (요청 수 제한)** — 쇼핑몰당 40건 버킷, 1초에 2씩 보충. 초과시 429.
2. **Usage 기반 (사용량 제한)** — `X-Cafe24-Call-Usage/Remain`, `X-Cafe24-Time-Usage/Remain`.
   100% 도달시 일시 차단.

`429` 발생 시 서버가 캡이 있는 지터 백오프(Usage Remain 힌트 우선)로 자동 재시도(최대 4회).
Analytics API는 별도 Token Bucket(IP/URL 기반).

## 검증

```bash
cd plugins/moai-seller/mcp-servers/moai-mcp-cafe24
uv run python -c "import moai_mcp_cafe24.server as s; print('tools:', s._TOOLS_REGISTERED)"
# tools: 526
```

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 401 반복 | access/refresh_token 만료 | README 인증 절차로 토큰 재발급 |
| 429 과다 | 레이트리밋 | `CAFE24_REQUEST_DELAY`로 요청 간격 조정, 자동 백오프는 이미 동작 |
| 422 필수누락 | body 필수값 누락 | 도구 독스트링의 description/notes 확인 |
| offset 한계(5000/15000) | 페이지네이션 상한 | cursor 매개변수(`since_product_no` 등) 사용 — 독스트링 notes 참고 |
| "특정 클라이언트만" API | 카페24 개발자센터 사전 승인 필요 | 해당 API는 승인된 앱에서만 호출 가능 |

## 라이선스

Apache-2.0 (모두의 코워크 플러그인의 일부).
