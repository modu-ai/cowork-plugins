# 데이터 애널리스트 (moai-analyst)

데이터·공공데이터 분석 전담 AI 직원입니다. 데이터 프로파일링·시각화, 공공데이터 조회(부동산·경매·주식·KOSIS 통계·건축물대장·DART 전자공시) 스킬 7종과 KOSIS 통계·건축HUB·DART MCP 연동을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> **분리 안내**: 본 플러그인의 데이터·공공데이터 스킬들은 `moai-officer`에서 분리되었습니다(오피스 문서 생성 스킬은 moai-officer에 잔류). 신규 호출은 `moai-analyst:<스킬명>` 네임스페이스를 사용하세요.

**이런 분께 추천**: 데이터 애널리스트 · 사무직 · 기획자 · 자영업 운영자

## 설치

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-analyst@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-analyst
```

## 스킬 7종

호출 형식: `/moai-analyst:office-<스킬명>` — 예: `/moai-analyst:office-public-data-public-data`. 자연어 요청("지역별 인구통계 조회해줘", "이 CSV 분석해줘")으로도 자동 매칭됩니다.

### 공공데이터 조회 (6종)

| 스킬 | 역할 |
|------|------|
| `office-public-data-public-data` | 공공데이터포털(data.go.kr)·KOSIS 통계 정밀 조회·분석 — korean-stats MCP 우선 |
| `office-public-data-real-estate-search` | 국토교통부 실거래가·전월세 시세 조회 |
| `office-public-data-court-auction-search` | 대법원 법원경매 매각공고·사건번호 조회 |
| `office-public-data-korean-stock-search` | KRX 상장 종목 검색·기본정보·일별 시세 조회 |
| `office-building-ledger-search` | 건축물대장·건축인허가·공시가격·노후도 조회 — archhub MCP |
| `office-business-real-estate-search` | 상업업무용 부동산 실거래 조회 (→ real-estate-search 경유) |

### 데이터 분석·시각화 (3종)

| 스킬 | 역할 |
|------|------|
| `office-data-explorer` | CSV·Excel 데이터 프로파일링·품질 보고서 |
| `office-data-visualizer` | 인터랙티브 차트·대시보드(HTML) 생성 |
| `office-data-public-data` | 공공데이터 조회 라우터 (→ public-data-public-data 경유) |

### 조회 라우터 (2종 · 구명칭 호환)

| 스킬 | 역할 |
|------|------|
| `office-finance-court-auction-search` | 법원경매 조회 라우터 (→ public-data-court-auction-search 경유) |
| `office-finance-korean-stock-search` | 국내주식 조회 라우터 (→ public-data-korean-stock-search 경유) |

## MCP 연동 3종

플러그인 루트 `.mcp.json`에 3개 MCP 서버가 선언되어 있습니다. 자격증명은 **환경변수로만** 설정하세요(파일에 키를 적지 않습니다).

| 서버 | 역할 | 키 발급 | 비고 |
|------|------|---------|------|
| `korean-stats` | KOSIS 국가통계 조회 — 92 키워드·시도/시군구 라우팅·출처(통계표 ID) 자동 인용 (14도구) | 불필요 (공용키 hosted) | remote 커넥터, URL 등록만으로 동작 |
| `archhub` | 국토교통부 건축HUB — 건축물대장·인허가·공시가격·노후도 (11도구) | 불필요 (공용키 hosted) | hosted 장애 시 로컬 대체: `uvx --from git+https://github.com/chrisryugj/archhub-mcp archhub-mcp` + `ARCHHUB_SERVICE_KEY`(data.go.kr 건축HUB 활용신청) |
| `dart` | OpenDART 전자공시 — 공시·재무·지권·XBRL·HWP/PDF 첨부 마크다운화 (15도구) | 필요: [opendart.fss.or.kr](https://opendart.fss.or.kr) 회원가입 → 인증키 신청(이메일 즉시, 일 20,000건 무료) → `DART_API_KEY` 환경변수 | Node.js 20.19+ 권장 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `data-analyst` | worker | 공공데이터 조사·데이터 프로파일링·시각화 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → office-data-*/public-data-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 수치는 출처(통계표 ID·공시 번호·data.go.kr 데이터셋) 인용 필수, 조회 실패 시 `[NOT_FOUND]` 명시, 개인정보 마스킹 |
| `data-provenance-auditor` | read-only audit | 수치 출처(provenance)·표/차트-원데이터 정합·산술 재계산·개인정보 누출을 회의적으로 재검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
