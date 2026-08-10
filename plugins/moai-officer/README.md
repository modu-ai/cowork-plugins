# 사무관 (moai-officer)

사무 문서 전담 AI 코워커입니다. 한국형 오피스 문서(HWPX·DOCX·XLSX·PPTX·PDF)와 HTML 리포트/슬라이드 생성, 공문서 파싱, 노션 템플릿·생산성 루틴까지 문서 생산 스킬 13종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> **분리 안내**: 공공데이터 조회·데이터 분석·시각화(11종)는 `moai-analyst` 플러그인으로, 라이프스타일·자기계발 루틴(7종)은 `moai-coworker`의 general/생활 도메인으로 분리되었습니다.

**이런 분께 추천**: 사무직 · 기획자 · 자영업 운영자

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-officer`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-officer@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-officer@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 13종

호출 형식: `/moai-officer:office-<스킬명>` — 예: `/moai-officer:doc-hwp`. 자연어 요청("주간 보고서 HWPX로 만들어줘")으로도 자동 매칭됩니다.

### 문서 생성·파싱 (8종)

| 스킬 | 역할 |
|------|------|
| `doc-hwp` | 아래아한글(.hwpx) 공문서·기안서·품의서·보고서 작성, HWP→HWPX 변환 |
| `doc-docx` | 워드(.docx) 보고서·계약서·제안서·공문서 생성 |
| `doc-xlsx` | 엑셀(.xlsx) KPI 대시보드·매출 분석표·예산표·간트차트 생성 |
| `doc-pptx` | 파워포인트(.pptx) 발표 슬라이드 디자인 |
| `doc-pdf` | HTML/Markdown/JSON/텍스트 → PDF 변환 (디자인 보존) |
| `doc-html-report` | 마크다운 보고서 → 단일 파일 HTML 리포트 |
| `doc-html-slide` | 자체 완결형 단일 파일 HTML 슬라이드 덱 (인라인 SVG 인포그래픽) |
| `doc-reader` | 한국 공문서(HWP·HWPX·PDF·XLSX·DOCX) 마크다운 파싱 — kordoc MCP |

### 문서 지원·생산성 (5종)

| 스킬 | 역할 |
|------|------|
| `doc-design-library` | 75개 브랜드 디자인 시스템 토큰을 HTML 산출물에 적용 (정본은 moai-designer) |
| `doc-notion-template` | 노션 업무관리·목표·회고 템플릿 구조 설계 |
| `setup-mcp-connector` | Drive·Notion·Higgsfield 커넥터 인증·환경변수 가이드 |
| `productivity-time` | 하루·주간 시간 설계 (블록식스·우선순위) |
| `productivity-briefing` | 업계 뉴스·시장 동향·오늘 할 일 아침 브리핑 |

## MCP 연동 1종

플러그인 루트 `.mcp.json`에 1개 MCP 서버가 선언되어 있습니다.

| 서버 | 역할 | 키 발급 | 비고 |
|------|------|---------|------|
| `kordoc` | 한국 공문서 파서 — HWP·HWPX·PDF·XLSX·DOCX → Markdown, 표 재현·양식 채우기·OCR (8도구) | 불필요 | Node.js 18+ 필요, `npx -y kordoc mcp` 자동 실행. 라이브 스킬: `doc-reader` |

> 공공데이터 MCP(korean-stats KOSIS · archhub 건축물대장 · dart 전자공시)는 `moai-analyst` 플러그인으로 이관되었습니다.

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `doc-producer` | worker | 보고서·슬라이드·양식 문서·공문서 파싱 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → office-* 문서 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 공공데이터 조사는 moai-analyst의 data-analyst로, 라이프스타일·자기계발은 moai-coworker로 인계. 문서 내 수치는 출처 인용 필수, 조회 실패 시 `[NOT_FOUND]` 명시 |
| `data-auditor` | read-only audit | 오피스 문서·포함 수치·표/차트-원데이터 정합·공문서 규격·계산을 회의적으로 재검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음. 공공데이터 출처 중심 감사는 moai-analyst의 data-provenance-auditor로 인계 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
