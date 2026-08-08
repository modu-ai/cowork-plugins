# moai-mcp-core

자체 제작 MoAI MCP 서버들이 공유하는 코어입니다. OAuth2 갱신, 토큰 영속화, HTTP 재시도,
TTL 캐시, 오류 매핑 — 서버마다 따로 만들던 것을 한곳으로 모았습니다.

## 여기가 정본입니다

```
plugins/_shared/moai-mcp-core/moai_mcp_core/   ← 정본. 여기만 고칩니다
        ↓ scripts/sync-mcp-core.py
plugins/<플러그인>/mcp-servers/moai-<서비스>/src/moai_mcp_core/   ← 복제본
```

플러그인은 각자 독립 설치되므로 런타임에 `plugins/_shared/`를 참조할 수 없습니다. 그래서
**각 서버 안으로 복제**합니다. PyPI에 올리지 않는 이유는 사용자가 비개발자이기 때문입니다 —
네트워크·인증·버전 충돌이라는 실패 지점을 사용자에게 떠넘기지 않고, 설치 즉시 작동하게 합니다.

복제본 파일 첫 줄에는 자동 생성 배너가 붙습니다. **복제본을 직접 고치면 다음 동기화에서
덮어써집니다.**

```bash
python3 scripts/sync-mcp-core.py           # 정본 → 전체 서버로 복제
python3 scripts/sync-mcp-core.py --check   # 드리프트 검사 (불일치면 종료코드 1)
```

## 모듈

| 모듈 | 책임 |
|---|---|
| `tokenstore.py` | `~/.moai/mcp/<서비스>-tokens.json` 영속화. 쓰기 불가 시 인메모리 폴백 |
| `auth.py` | OAuth2 갱신, 리프레시 토큰 회전 대응, 만료 선반영 |
| `http.py` | 타임아웃·재시도·백오프·429 대응·401 시 1회 강제 재인증 |
| `cache.py` | 읽기 응답 TTL 캐시 — 성능이 아니라 **할당량 절약**이 목적 |
| `errors.py` | 예외 → MCP 구조화 오류 응답. 서버는 절대 죽지 않습니다 |

## 설계 원칙

**서버는 죽지 않습니다.** 자격증명이 없으면 `setup_required`, 한도에 걸리면 `rate_limited`를
구조화된 응답으로 돌려줍니다. 예상 못 한 예외도 `to_tool_result()`가 삼켜서 변환합니다.

**재시도는 의미 있을 때만.** 401은 토큰 갱신 후 한 번만(무한 루프 방지), 429는 `Retry-After`를
존중하고, 5xx는 지수 백오프 + 지터로 재시도합니다. 400은 재시도하지 않습니다 — 같은 요청은
같은 결과를 냅니다.

**macOS와 Windows에서 동일하게.** 경로는 `pathlib`으로만 조립하고, 파일 입출력은
`encoding="utf-8"`을 명시하며, 권한 제한(`chmod`)은 실패해도 넘어갑니다.

## 개발

```bash
uv sync
uv run pytest -q
```

정본을 고쳤으면 반드시 동기화하고 커밋하세요.

```bash
python3 scripts/sync-mcp-core.py
```

## 근거 문서

`.moai/reports/mcp-naming-consolidation-design.md` §3(통합 설계) · §4-1(vendor 동기화 계약).
