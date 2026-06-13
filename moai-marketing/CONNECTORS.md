# moai-marketing — MCP 커넥터 가이드

본 플러그인은 메타 광고 운영·분석에 필요한 2개 MCP 서버를 등록한다.

## 등록 MCP 서버 요약

| 이름 | 책임 | 유형 | 라이선스 | 인증 |
|------|------|------|----------|------|
| `meta-ads` | Layer 1 — Meta 공식 Ads AI Connectors (라이브 운영 + Marketing API 데이터 fetch) | `http` (hosted) | Meta 약관 | Meta Business OAuth 2.0 |
| `moai-ads-audit` | Layer 2 — 50-check audit + 가중치 스코어링 + 한국 벤치마크/컴플라이언스 | `stdio` (local uvx) | MIT | `MOAI_LOG_LEVEL` (선택) |

3-Layer 아키텍처:

- **Layer 1** (공식 MCP): `meta-ads` — Meta 공식 **Ads AI Connectors** (`https://mcp.facebook.com/ads`)
- **Layer 2** (자체 MCP): `moai-ads-audit` — audit 비즈니스 로직, `.xlsx` 입력 단독 모드도 항상 지원
- **Layer 3** (스킬):
  - `moai-marketing:meta-ads-manager` — 공식 MCP 기반 **라이브 운영**(캠페인·광고세트·광고 생성·수정·예산·온오프)
  - `moai-marketing:meta-ads-analyzer` — 보고서 **분석·진단**(`.xlsx` 1-6개 → 9 모듈·4D 교차·🟢🟡🔴 액션)

`meta-ads` 비활성 환경에서도 `moai-ads-audit` 단독으로 `.xlsx` 보고서 업로드 모드 동작 (REQ-AUDIT-MCP-005).

---

## Meta Ads — 공식 커넥터 연결

Meta 공식 **Meta Ads AI Connectors**(한글: Meta 광고 AI 커넥터, 2026-04-29 오픈 베타)는 Ads MCP 서버 + Ads CLI로 구성된다. AI 에이전트(Claude 등)를 사용자의 Meta 광고 계정에 연결해 자연어로 광고를 생성·관리·분석한다. 공식 안내: <https://www.facebook.com/business/help/1456422242197840>.

### OAuth 2.0 커넥터 (1차 · 권장)

공식 기본 인증 경로다. 앱 생성·앱 심사·토큰 수동 복사가 **필요 없다**. 클라이언트(Claude)가 Meta Business OAuth 로그인을 브라우저에서 수행하고 액세스 토큰을 자동 발급한다.

- **엔드포인트**: `https://mcp.facebook.com/ads`
- **표준**: RFC 9728 Protected Resource Metadata + RFC 6750 Bearer
- **OAuth scope**: `ads_management ads_read catalog_management business_management pages_show_list`

#### A. Claude Cowork / Desktop (비개발자 1차 경로)

1. Settings → Connectors → **Add custom connector**
2. 이름 입력 + URL `https://mcp.facebook.com/ads` 입력 후 Add
3. 브라우저가 열리며 **Meta Business OAuth 로그인** 진행 (필요 시 2FA)
4. 공유할 광고 계정·페이지 선택 + 권한 등급 선택 (read-only로 시작 권장 → 필요 시 read+write/financial)
5. "내 광고 계정 목록 보여줘" 등 자연어 프롬프트로 연결 검증. 쓰기·재무 동작은 매번 사용자 승인. 권한 철회는 Meta Business Suite에서.

#### B. Claude Code (`.mcp.json`)

정적 Authorization 헤더를 넣지 않는다. OAuth 커넥터 흐름이 인증을 처리한다.

```json
{
  "mcpServers": {
    "meta-ads": {
      "type": "http",
      "url": "https://mcp.facebook.com/ads"
    }
  }
}
```

### 정적 토큰 (Fallback · 강등)

OAuth가 불가한 개발 환경 **전용 fallback**이다. 개발자/시스템 사용자 토큰을 Graph API Explorer에서 발급한다.

1. <https://developers.facebook.com/> → **My Apps** → **Create App** ("Business" 유형)
2. 앱 대시보드 → **Marketing API** 제품 추가 → **Graph API Explorer**
3. 권한 선택: `ads_read`(필수) · `ads_management`(선택) · `business_management`(선택)
4. **Generate Access Token** → `export META_ACCESS_TOKEN="EAA..."` (`.zshrc`/`.bashrc` 또는 `~/.claude/settings.json` env)

> ⚠️ OAuth 보호 엔드포인트(`mcp.facebook.com/ads`)는 일반 정적 Bearer를 거부할 수 있다(라이브 프로브에서 더미 Bearer는 403). **항상 OAuth 커넥터를 먼저** 사용하고, 정적 토큰은 우선순위가 낮은 fallback으로만 둔다.

### 보안 (MCP 키 관리 원칙)

- 토큰을 코드·plugin.json·SKILL.md에 절대 하드코딩하지 않는다
- 토큰을 git에 commit하지 않는다 (`.gitignore` 확인 — `.env`, `.envrc`, `**/secrets/**`)
- 토큰을 로그·stdout에 노출하지 않는다 (`MOAI_LOG_LEVEL=DEBUG` 환경에서도 자동 마스킹, REQ-AUDIT-MCP-023)
- 토큰 갱신 주기: Meta 단기 토큰 60일 / 시스템 사용자 장기 토큰 발급 시 사실상 영구

---

## moai-ads-audit — 로컬 설치 및 환경변수

### 설치 (uvx 자동 처리)

`uvx`가 시스템에 설치되어 있어야 한다. 설치되어 있지 않다면:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`.mcp.json`의 `moai-ads-audit` 항목이 `uvx --from /Users/goos/.../mcp-servers/moai-ads-audit moai-ads-audit-mcp` 명령으로 자동 실행한다. 첫 실행 시 uvx가 패키지를 isolated 가상환경에 설치한다.

### 환경변수 (선택)

| 변수 | 기본값 | 용도 |
|------|--------|------|
| `MOAI_LOG_LEVEL` | `INFO` | 로깅 수준 (DEBUG/INFO/WARNING/ERROR). DEBUG 시에도 자격증명·인구통계 raw 데이터는 자동 마스킹. |

### 도구 10종 (v0.1.0 — 우선 3종 구현)

| # | 도구 이름 | 책임 | v0.1.0 |
|---|----------|------|-------|
| 1 | `audit_meta_account` | 4 카테고리 합산 health score 진입점 | ✅ |
| 2 | `audit_pixel_capi` | Pixel/CAPI Health 10개 check (EMQ·dedup·AEM·키 파라미터) | ✅ |
| 3 | `audit_creative_diversity` | Creative Diversity & Fatigue 12개 check | ⏸ 라운드 4 |
| 4 | `audit_account_structure` | Account Structure 10개 check (Learning Limited·CBO/ABO) | ⏸ 라운드 4 |
| 5 | `audit_audience_targeting` | Audience & Targeting 7개 check | ⏸ 라운드 4 |
| 6 | `audit_andromeda_emq` | Andromeda & Platform 4개 check | ⏸ 라운드 4 |
| 7 | `calculate_health_score` | 가중치 공식 점수 + A-F 등급 | ✅ |
| 8 | `generate_quick_wins` | Critical/High + <15분 분류 | ⏸ 라운드 4 |
| 9 | `apply_korean_benchmarks` | 8 카테고리 한국 시장 벤치마크 비교 | ⏸ 라운드 4 |
| 10 | `apply_korean_compliance` | 5 규제 (PIPA·ITNA·전상법·표시광고법·식약처) | ⏸ 라운드 4 |

---

## 검증 (등록 후)

```
# 1. .mcp.json 문법 검사
python3 -c "import json; json.load(open('.mcp.json')); print('OK')"

# 2. moai-ads-audit-mcp 직접 호출 (--version)
uvx --from ./mcp-servers/moai-ads-audit moai-ads-audit-mcp --version
# 기대: moai-ads-audit-mcp 0.1.0

# 3. Claude Code 재시작 후 MCP 도구 목록 확인 (meta-ads 첫 호출 시 OAuth 로그인)
```

---

## Attribution

`moai-ads-audit` MCP 서버의 audit 방법론은 [`agricidaniel/claude-ads`](https://github.com/AgriciDaniel/claude-ads) v1.5.1 (MIT License)의 50-check matrix·가중치 스코어링 공식·Quick Wins 로직을 한국 시장 7 변화 영역에 맞춰 차용했다.

전체 attribution 텍스트는 `NOTICE.md` §"agricidaniel/claude-ads (MIT)" 참조.

`meta-ads` 커넥터는 Meta 공식 Ads AI Connectors를 사용하며, 서드파티 오픈소스 Meta Ads MCP는 사용하지 않는다.

---

Last Updated: 2026-05-30
