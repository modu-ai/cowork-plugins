# 법무 담당 (moai-lawyer)

법무 전담 AI 코워커입니다. 계약 검토·NDA 트리아지·컴플라이언스 점검·법령/판례 리서치·특허 검색/분석·식약처 안전 기준 등 법무 실무 스킬 10종과 국가법령정보 MCP(korean-law) 연동을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

**이런 분께 추천**: 1인 사업자 · 스타트업 운영자 · 법무 담당자 없는 소규모 팀

> ⚠️ **법률 자문이 아닙니다.** 본 플러그인의 모든 산출물은 참고 자료이며 변호사의 법률 자문을 대체하지 않습니다. 계약 체결·소송 등 구속력 있는 의사결정 전에는 반드시 변호사와 상담하세요.

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-lawyer`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-lawyer@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-lawyer@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 10종

호출 형식: `/moai-lawyer:legal-<스킬명>` — 예: `/moai-lawyer:legal-contract-review`. 자연어 요청("이 계약서 검토해줘")으로도 자동 매칭됩니다.

### 계약·문서 검토 (2종)

| 스킬 | 역할 |
|------|------|
| `legal-contract-review` | 계약서·이용약관·개인정보처리방침 분석/작성 — 민법·상법 기반 10대 리스크 패턴 + 수정 권고안 |
| `legal-nda-triage` | NDA(비밀유지계약서) 신속 검토 — 조항별 위험도 평가 + 수정 권고안 |

### 컴플라이언스·리스크 (2종)

| 스킬 | 역할 |
|------|------|
| `legal-compliance-check` | 규제 준수 점검·내부 감사·ESG 보고·인허가 서류 — 갭 분석 + 시정 계획 |
| `legal-legal-risk` | 기업 법적 리스크 분석·IP 전략 — 리스크 매트릭스 + 대응 액션 플랜 |

### 법령·판례 리서치 (1종)

| 스킬 | 역할 |
|------|------|
| `legal-law-research` | 법령·판례·행정규칙·조약·해석례 원문 조회 + 인용 검증(환각방지)·판례 생사 확인·행위시법 판단 (korean-law MCP) |

### 특허 (2종)

| 스킬 | 역할 |
|------|------|
| `legal-patent-search` | KIPRIS Plus 특허·실용신안·디자인·상표 검색 + 출원 현황 정리 |
| `legal-patent-analyzer` | 특허 동향 보고서·선행기술 조사·FTO(침해 가능성) 분석·출원서 초안 |

### 행정·안전 기준 (2종)

| 스킬 | 역할 |
|------|------|
| `legal-mfds-safety` | 식약처(MFDS) 의약품·식품 공식 안전 정보 조회 (인정현황·회수·판매중지 등) |
| `legal-iros-registry-automation` | 인터넷등기소(IROS) 등기부등본 일괄 발급 보조 — 열람·저장·종합 리포트 |

## MCP 연동: korean-law (국가법령정보)

플러그인 루트 `.mcp.json`에 법제처 국가법령정보 MCP 서버가 선언되어 있습니다. 법령·판례·행정규칙·자치법규·조약·해석례 조회에 더해, LLM 환각방지 인용 검증(`verify_citations`), 판례 생사 확인(`cite_check`), 행위시법 판단(`applicable_law`)을 제공합니다.

| 서버 | 출처 | 필요 환경변수 | 비고 |
|------|------|---------------|------|
| `korean-law` | 법제처 42개 API → 9개 도구 (hosted, `mcp.gomdori.app/law`) | `KOREAN_LAW_OC` | 법제처 Open API OC 키 — 사용자마다 발급 필수 |

**OC 키 발급**: [law.go.kr](https://www.law.go.kr) 국가법령정보 Open API에서 무료로 발급합니다 (회원가입 → Open API 신청 → OC 값 확인). 발급받은 값을 환경변수 `KOREAN_LAW_OC`로 설정하세요 — 파일에 키를 적지 않습니다.

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `legal-researcher` | worker | 계약 검토·컴플라이언스·법령/판례 리서치·특허 분석 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → legal-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 모든 법령·판례 인용은 korean-law MCP로 검증하며, 산출물에 "법률 자문 아님" 고지를 항상 포함 |
| `risk-auditor` | read-only audit | 인용 실존·판례 생사·리스크 등급 논리·누락 쟁점·고지 문구를 회의적으로 재검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 이관 안내

본 플러그인의 법무 스킬은 기존 통합 플러그인(moai-coworker)의 legal 카테고리에서 전담 플러그인으로 이관되었습니다. 기존 `moai-lawyer:legal-*` 호출 경로 대신 `moai-lawyer:legal-*` 네임스페이스를 사용하세요.

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
