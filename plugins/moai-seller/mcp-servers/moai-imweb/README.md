# moai-imweb MCP

아임웹(Imweb) OPEN API **v3** 를 MCP(Model Context Protocol) 도구로 노출하는 서버.
쇼핑몰 운영 전 도메인 **136개 엔드포인트** 를 **8개 카테고리 도구** 로 제공합니다
(smartstore "83 API → 15 도구" 와 같은 압축 설계).

- **스펙 SSOT**: `https://developers-docs.imweb.me/reference/openapi.json` (OAS 3.1.0)
- **API 서버**: `https://openapi.imweb.me`
- **인증**: OAuth2 authorizationCode + JWT access token (자동 갱신)
- **구현**: Python + [FastMCP](https://github.com/modelcontextprotocol/python-sdk), uv 기반

> 인증·자격증명 발급 절차는 [`CONNECTORS.md`](./CONNECTORS.md) 참고.

---

## 도구 설계 — 카테고리 디스패치

도메인(카테고리)당 **1개 도구**. 각 도구는 `action` 파라미터로 해당 도메인의
엔드포인트를 디스패치합니다. 8개 도구 = 8개 MCP 스키마만 로드되어 가볍고, LLM 이
도구를 선택하기 쉽습니다.

```python
imweb_<category>(
    action: Literal[...],   # 도메인 내 엔드포인트 키 (operationId 스네이크)
    params: dict | None,    # path + query 파라미터
    body:   dict | None,    # POST/PATCH/PUT 요청 본문
    paginate: bool = False  # list 계열 GET 전체 페이지 자동 집계
) -> dict
```

## 도구 목록 (8)

| 도구 | action 수 | 범위 |
|---|---:|---|
| `imweb_order` | 44 | 주문 조회·배송처리·송장·취소·교환·반품 (주문/섹션/섹션아이템) |
| `imweb_product` | 31 | 상품 조회·등록·수정(가격·재고·옵션·배송·SEO·이미지) |
| `imweb_member_info` | 19 | 회원·그룹·등급 조회·수정·일괄변경 |
| `imweb_community` | 17 | Q&A·구매평(커서기반) 조회·등록·수정·삭제·답글 |
| `imweb_promotion` | 14 | 적립금(조회·지급/차감)·쿠폰(생성·발급·일괄·등급/그룹별) |
| `imweb_site_info` | 6 | 사이트 정보·메뉴·유닛·연동(완료/해제/수정) |
| `imweb_script` | 4 | 스크립트 CRUD |
| `imweb_payment` | 1 | 무통장 입금 수동 확인 |

> OAuth2 인증 엔드포인트 2개(`authorize`/`token`)는 MCP 도구로 노출하지 **않습니다** —
> 인증은 환경변수 + 내부 자동 갱신으로 처리합니다(`CONNECTORS.md`).

각 도구의 docstring 에 해당 도메인의 **전체 action 목록**(method·path·요약)과
각 action 의 **요청 본문(Body) Pydantic 모델**이 한국어 필드 설명과 함께 inputSchema 에
포함되어 있어, MCP 클라이언트가 별도 문서 없이도 action 을 선택하고 본문을 구성할 수
있습니다. description 은 2KB 이하로 간결하게 유지하고 본문 구조는 inputSchema 가 전달합니다.

## 설치

`.mcp.json`(`plugins/moai-seller/.mcp.json`)에 등록:

```jsonc
"moai-imweb": {
  "command": "uv",
  "args": ["run", "--directory", "${CLAUDE_PLUGIN_ROOT}/mcp-servers/moai-imweb", "moai-imweb-mcp"],
  "env": {
    "IMWEB_CLIENT_ID":     "${IMWEB_CLIENT_ID}",
    "IMWEB_CLIENT_SECRET": "${IMWEB_CLIENT_SECRET}",
    "IMWEB_ACCESS_TOKEN":  "${IMWEB_ACCESS_TOKEN}",
    "IMWEB_REFRESH_TOKEN": "${IMWEB_REFRESH_TOKEN}",
    "IMWEB_UNIT_CODE":     "${IMWEB_UNIT_CODE}"
  }
}
```

사전 요구: **uv** (`curl -LsSf https://astral.sh/uv/install.sh | sh`). PyPI 게시 불필요 —
소스를 플러그인에 vendor 했으므로 `uv run` 이 즉시 작동합니다.

## 자격증명

[`CONNECTORS.md`](./CONNECTORS.md) 의 1~5단계:
1. 아임웹 개발자센터 앱 등록 → `clientId` / `clientSecret` / `siteCode` / `redirectUri`
2. 브라우저로 `/oauth2/authorize` → authorization code
3. `POST /oauth2/token` (`grantType=authorization_code`) → `accessToken` / `refreshToken`
4. `.mcp.json` env 에 4종 토큰 설정

이후 access token 만료 시 서버가 refresh token 으로 **자동 갱신**합니다.

## 사용 예 (MCP 클라이언트 관점)

```
# 주문 목록 (배송완료, 최근 50건)
imweb_order(action="read_all_order", params={"orderSectionStatus":"SHIPPING_COMPLETE","page":1,"limit":50})

# 주문 전체 페이지 자동 집계
imweb_order(action="read_all_order", params={"orderSectionStatus":"SHIPPING_COMPLETE"}, paginate=True)

# 상품 등록
imweb_product(action="create_product", body={"prodName":"테스트 상품","price":10000,...})

# 주문 송장 등록
imweb_order(action="create_order_invoice", params={"orderNo":"ORD123"}, body={"deliveryCompany":"CJ","invoiceNo":"..."})

# 구매평 답글 등록
imweb_community(action="create_site_review_answer", body={"reviewNo":1,"content":"감사합니다"})
```

## 도구 재생성 (스펙 변경 시)

아임웹 API 가 업데이트되면 스펙을 갱신하고 도구를 재생성합니다:

```bash
cd mcp-servers/moai-imweb
curl -sL https://developers-docs.imweb.me/reference/openapi.json -o tools/openapi.json
python3 tools/_generator.py      # src/moai_imweb/tools/*.py 재생성 (카테고리 디스패치)
uv run pytest -q                 # 회귀 검증
```

생성기는 `tools/_generator.py`, SSOT 스펙은 `tools/openapi.json`. 생성된
`src/moai_imweb/tools/*.py` 는 **수동 편집 금지** — 재생성 시 덮어쓰입니다.

## 아키텍처

```
src/moai_imweb/
  _app.py        # FastMCP 인스턴스 (도구 등록 공유 객체)
  _base.py       # 설정(env) + ImwebClient 싱글톤 + 토큰 영속화
  auth.py        # OAuth2 refresh_token 갱신 (camelCase/snake 양쪽 대응)
  client.py      # HTTP: Bearer 주입 · 401 자동재발급 · 에러 매핑 · list_all_pages
  server.py      # 진입점(tools import 로 등록 트리거 → stdio run)
  tools/*.py     # 생성된 8 카테고리 도구 (_OPS 디스패치 테이블 + 도구 함수)
tools/
  _generator.py  # OpenAPI → 카테고리-디스패치 도구 생성기
  openapi.json   # SSOT 스펙 (재생성 입력)
tests/           # client/auth/tools/generator 단위 테스트 (19)
```

## 라이선스

Apache-2.0 (모두의 코워크 플러그인 패밀리).
