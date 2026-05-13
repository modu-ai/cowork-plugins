# moai-ads-audit-mcp

Meta 광고 audit 전담 MCP 서버 — `agricidaniel/claude-ads` v1.5.1 방법론 한국 시장 특화.

> **Attribution**: Methodology adapted from [`agricidaniel/claude-ads`](https://github.com/AgriciDaniel/claude-ads) v1.5.1 under MIT License.
> See `.claude/rules/moai/NOTICE.md` §"agricidaniel/claude-ads (MIT)" for full attribution details.
> 직접 코드 복사가 아닌 audit checklist 구조·가중치 스코어링 공식·Quick Wins 로직 방법론만 차용.

## 개요

3-Layer 아키텍처의 Layer 2 구성요소:

| Layer | 컴포넌트 | 역할 |
|-------|---------|------|
| Layer 1 | Meta 공식 MCP / Adspirer / byadsco (외부, 선택) | 원시 데이터 추출 |
| **Layer 2 (본 MCP)** | `moai-ads-audit-mcp` | audit 실행·가중치 스코어링 |
| Layer 3 | `meta-ads-analyzer` 스킬 (SPEC-META-ADS-001) | 사용자 친화 보고서 생성 |

## 설치 및 실행

```bash
# uvx로 직접 실행
uvx moai-ads-audit-mcp

# 버전 확인
uvx moai-ads-audit-mcp --version

# 개발 환경
pip install -e ".[dev]"
pytest tests/
```

## 환경변수

Layer 1 외부 MCP와 연동 시 필요 (REQ-AUDIT-MCP-002: 환경변수만 사용):

```bash
# Meta Marketing API 액세스 토큰 (Layer 1 MCP 활성 시)
export META_ADS_ACCESS_TOKEN="${META_ADS_ACCESS_TOKEN}"

# Layer 1 외부 MCP API 키 (Adspirer 등)
export ADSPIRER_API_KEY="${ADSPIRER_API_KEY}"
```

자격증명은 반드시 환경변수로 주입. 코드·manifest에 하드코딩 절대 금지.
자세한 발급 절차는 `CONNECTORS.md` 참조.

## 도구 10종

| # | 도구 이름 | 상태 | REQ |
|---|----------|------|-----|
| 1 | `audit_meta_account` | 구현 완료 (v1, Pixel 카테고리만) | REQ-AUDIT-MCP-006 |
| 2 | `audit_pixel_capi` | 구현 완료 | REQ-AUDIT-MCP-007 |
| 3 | `audit_creative_diversity` | 라운드 4 예정 | REQ-AUDIT-MCP-008 |
| 4 | `audit_account_structure` | 라운드 4 예정 | REQ-AUDIT-MCP-009 |
| 5 | `audit_audience_targeting` | 라운드 4 예정 | REQ-AUDIT-MCP-010 |
| 6 | `audit_andromeda_emq` | 라운드 4 예정 | REQ-AUDIT-MCP-011 |
| 7 | `calculate_health_score` | 구현 완료 | REQ-AUDIT-MCP-012 |
| 8 | `generate_quick_wins` | 라운드 4 예정 | REQ-AUDIT-MCP-013 |
| 9 | `apply_korean_benchmarks` | 라운드 4 예정 | REQ-AUDIT-MCP-014 |
| 10 | `apply_korean_compliance` | 라운드 4 예정 | REQ-AUDIT-MCP-015 |

## 가중치 스코어링 공식

claude-ads v1.5.1 원전 인용 (NOTICE.md §"Weighted Scoring Algorithm"):

```
S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100
```

| Severity | 배수 | 카테고리 | 가중치 |
|---------|------|---------|-------|
| Critical | 5.0× | Pixel/CAPI | 30% |
| High | 3.0× | Creative | 30% |
| Medium | 1.5× | Account Structure | 20% |
| Low | 0.5× | Audience | 20% |

등급: A(90+) / B(75-89) / C(60-74) / D(40-59) / F(<40)

## 한국 시장 특화

- **8 카테고리 벤치마크**: 식품/음료·패션/뷰티·건강기능식품/의료·IT/디지털·가정용품/생활·교육/지식·서비스/B2B·기타
- **5개 규제 검사**: PIPA·정보통신망법·전자상거래법·표시광고법·식약처 광고 심의
- **한국어 출력**: 모든 audit 결과·시정 가이드

## 라이선스

MIT License. See `NOTICE` in `.claude/rules/moai/NOTICE.md` for third-party attributions.
