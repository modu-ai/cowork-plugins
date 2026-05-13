# moai-marketing — MCP 커넥터 가이드

cowork-plugins v2.5.0 신규. 본 플러그인은 메타 광고 분석(meta-ads-analyzer)에 필요한 2개 MCP 서버를 등록한다.

## 등록 MCP 서버 요약

| 이름 | 책임 | 유형 | 라이선스 | 필수 환경변수 |
|------|------|------|----------|---------------|
| `meta-ads` | Layer 1 — Meta Marketing API 원시 데이터 fetch | `http` (hosted) | Meta 약관 | `META_ACCESS_TOKEN` |
| `moai-ads-audit` | Layer 2 — 50-check audit + 가중치 스코어링 + 한국 벤치마크/컴플라이언스 | `stdio` (local uvx) | MIT | `MOAI_LOG_LEVEL` (선택) |

3-Layer 아키텍처:

- **Layer 1** (외부 MCP, 옵션): `meta-ads` — Meta 공식 또는 fallback (Adspirer · byadsco · pipeboard)
- **Layer 2** (자체 MCP, 필수): `moai-ads-audit` — audit 비즈니스 로직, .xlsx 입력 단독 모드도 항상 지원
- **Layer 3** (스킬): `moai-marketing:meta-ads-analyzer` — 사용자 톤·강도별 액션 옵션·4 출력 형식

`meta-ads` 비활성 환경에서도 `moai-ads-audit` 단독으로 .xlsx 보고서 업로드 모드 동작 (REQ-AUDIT-MCP-005).

---

## Meta Ads — `META_ACCESS_TOKEN` 발급

### Meta 공식 MCP (권장, 2026-04-29 출시)

1. Meta for Developers 페이지 접속: https://developers.facebook.com/
2. **My Apps** → **Create App** → "Business" 유형 선택
3. 앱 대시보드 → **Marketing API** 제품 추가
4. **Tools** → **Graph API Explorer** 진입
5. 권한 선택:
   - `ads_read` (필수 — audit 진단용)
   - `ads_management` (선택 — 광고 운영 자동화 시)
   - `business_management` (선택 — 비즈니스 매니저 계정 통합 시)
6. **Generate Access Token** → 사용자 본인 토큰 생성
7. 환경변수 등록:
   - macOS/Linux: `export META_ACCESS_TOKEN="EAA..."` (`.zshrc` / `.bashrc`)
   - 또는 `~/.claude/settings.json` `env` 블록에 등록

### Fallback 옵션 (Meta 공식 MCP 비활성 시)

| MCP | 유형 | URL | 인증 | 비고 |
|------|------|-----|------|------|
| Adspirer | hosted (유료) | https://adspirer.com | API 키 | 상용 안정성 |
| byadsco/meta-ads-mcp | self-hosted | https://github.com/byadsco/meta-ads-mcp | API 키 | 컴플라이언스 우선 |
| pipeboard | hosted (source-available) | https://mcp.pipeboard.co/meta-ads-mcp | API 키 | 커뮤니티 검증 |

비활성 환경에서는 `meta-ads-analyzer` 스킬이 `.xlsx` 보고서 업로드 모드로 fallback (REQ-META-ADS-001 v1 보고서 업로드 한정).

### 보안 권칙 (CLAUDE.local.md §6 HARD)

- 토큰을 코드·plugin.json·SKILL.md에 절대 하드코딩하지 않는다
- 토큰을 git에 commit하지 않는다 (`.gitignore` 확인 — `.env`, `.envrc`, `**/secrets/**`)
- 토큰을 로그·stdout에 노출하지 않는다 (`MOAI_LOG_LEVEL=DEBUG` 환경에서도 자동 마스킹, REQ-AUDIT-MCP-023)
- 토큰 갱신 주기: Meta 단기 토큰 60일 / 장기 토큰 시스템 사용자 발급 시 사실상 영구

---

## moai-ads-audit — 로컬 설치 및 환경변수

### 설치 (uvx 자동 처리)

`uvx`가 시스템에 설치되어 있어야 한다. 설치되어 있지 않다면:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

`.mcp.json`의 `meta-ads-audit` 항목이 `uvx --from /Users/goos/.../mcp-servers/moai-ads-audit moai-ads-audit-mcp` 명령으로 자동 실행한다. 첫 실행 시 uvx가 패키지를 isolated 가상환경에 설치한다.

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

# 3. Claude Code 재시작 후 MCP 도구 목록 확인
```

---

## Attribution

`moai-ads-audit` MCP 서버의 audit 방법론은 [`agricidaniel/claude-ads`](https://github.com/AgriciDaniel/claude-ads) v1.5.1 (MIT License, 4,815 stars, 2026-05-13 시점)의 50-check matrix·가중치 스코어링 공식·Quick Wins 로직을 한국 시장 7 변화 영역에 맞춰 차용했다.

전체 attribution 텍스트는 `.claude/rules/moai/NOTICE.md` §"agricidaniel/claude-ads (MIT)" 참조.

---

Version: 2.5.0
Last Updated: 2026-05-13
