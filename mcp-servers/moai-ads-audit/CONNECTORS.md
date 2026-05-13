# CONNECTORS — moai-ads-audit-mcp 연결 가이드

> **Attribution**: Methodology adapted from [`agricidaniel/claude-ads`](https://github.com/AgriciDaniel/claude-ads) v1.5.1 under MIT License.
> See `.claude/rules/moai/NOTICE.md` §"agricidaniel/claude-ads (MIT)".

## 환경변수 발급 절차

모든 자격증명은 환경변수 `${VAR_NAME}` 구문으로만 주입 (REQ-AUDIT-MCP-002 HARD).
코드·manifest·SKILL.md·plugin.json 어디에도 하드코딩 절대 금지.

### 1. Meta 광고관리자 API 토큰 (`META_ADS_ACCESS_TOKEN`)

Layer 1 외부 MCP (Meta 공식 `mcp.facebook.com/ads`) 또는 Adspirer 연동 시 필요.
본 MCP v1은 `.xlsx` 단독 모드가 기본 — Layer 1 MCP 없이도 동작 (REQ-AUDIT-MCP-005).

**발급 절차:**

1. [Meta for Developers](https://developers.facebook.com/) → 앱 생성 또는 기존 앱 선택
2. 앱 대시보드 → 도구 → 그래프 API 탐색기
3. **사용자 액세스 토큰** 생성 (광고 계정 권한: `ads_read`, `ads_management`)
4. 장기 토큰으로 교환 (단기 토큰은 60분 만료):
   ```
   GET https://graph.facebook.com/oauth/access_token
     ?grant_type=fb_exchange_token
     &client_id={APP_ID}
     &client_secret={APP_SECRET}
     &fb_exchange_token={SHORT_TOKEN}
   ```
5. 환경변수 설정:
   ```bash
   export META_ADS_ACCESS_TOKEN="EAAxxxx..."
   ```

**보안 주의:**
- 토큰을 로그·stdout에 절대 출력하지 말 것 (REQ-AUDIT-MCP-023)
- `.env` 파일에 저장 시 `.gitignore`에 반드시 포함
- 토큰 노출 시 즉시 [앱 대시보드](https://developers.facebook.com/)에서 무효화

### 2. Meta 공식 MCP (`mcp.facebook.com/ads`)

2026-04-29 출시. OAuth 기반 사용자 본인 인증.

**연동 방식 (Layer 1 옵션):**
```json
{
  "mcpServers": {
    "meta-ads": {
      "type": "http",
      "url": "https://mcp.facebook.com/ads",
      "headers": {
        "Authorization": "Bearer ${META_ADS_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 3. Adspirer MCP (대안 Layer 1)

**환경변수:** `ADSPIRER_API_KEY`

발급: [Adspirer 공식 사이트](https://adspirer.com/) → API 키 발급

```bash
export ADSPIRER_API_KEY="${ADSPIRER_API_KEY}"
```

### 4. .xlsx 단독 모드 (Layer 1 없이)

Layer 1 외부 MCP 없이도 Meta 광고관리자에서 직접 내보낸 `.xlsx` 보고서로 audit 가능.

**Meta 광고관리자 보고서 내보내기:**

1. [광고관리자](https://www.facebook.com/adsmanager/) → 보고서
2. 분석 기간 설정 → 열 맞춤 (12 필수 컬럼 포함)
3. 분류: 광고·노출 위치·연령·성별 (선택)
4. 내보내기 → Excel (.xlsx)
5. 저장 경로를 `xlsx_path` 파라미터로 전달

**12 필수 컬럼:**

| 한국어 | 영어 |
|--------|------|
| 보고 시작 | Reporting starts |
| 보고 종료 | Reporting ends |
| 광고 이름 | Ad name |
| 노출 위치 | Placement |
| 연령 | Age |
| 성별 | Gender |
| 지출 금액 | Amount spent |
| 링크 클릭 | Link clicks |
| CTR | CTR (link CTR) |
| CPC | CPC |
| 구매 | Purchases |
| 구매 전환값 | Purchase conversion value |
| 구매 ROAS | Purchase ROAS |

## moai-marketing/.mcp.json 등록 예시 (Track C-1, 별도 작업)

```json
{
  "mcpServers": {
    "moai-ads-audit": {
      "$comment": "Meta 광고 audit 전담 MCP. META_ADS_ACCESS_TOKEN 필요 (Layer 1 MCP 연동 시).",
      "command": "/bin/bash",
      "args": ["-l", "-c", "exec uvx moai-ads-audit-mcp"],
      "env": {
        "META_ADS_ACCESS_TOKEN": "${META_ADS_ACCESS_TOKEN}"
      }
    }
  }
}
```

## 보안 체크리스트

- `grep -rE "(EAA|EAAB|sk-)[A-Za-z0-9_-]{20,}" .` 검색 시 매치 0건 확인
- `.xlsx` 보고서 파일을 저장소에 커밋하지 말 것 (PIPA)
- Meta 광고관리자 UI에서 최소 권한 원칙 적용 (`ads_read` 우선)
