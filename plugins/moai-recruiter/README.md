# 인사·채용 담당 (moai-recruiter)

인사·채용 전담 AI 직원입니다. 채용 공고 분석, 이력서 스크리닝, 오퍼레터·근로계약서, 성과평가, People Ops 등 고용주 편 채용 실무 스킬 6종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다. 구직자 편(이력서·포트폴리오·면접 준비)은 `moai-career`(커리어코치)로 분리되었습니다.

**이런 분께 추천**: 채용 담당자 · 인사 실무자 · 직원을 채용하는 1인 사업자

## 설치

Claude Code에서 두 단계로 설치합니다:

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-recruiter@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-recruiter
```

## 스킬 6종

호출 형식: `/moai-recruiter:business-<스킬명>` — 예: `/moai-recruiter:business-resume-screener`. 자연어 요청("이 채용공고 분석해줘")으로도 자동 매칭됩니다.

| 스킬 | 역할 |
|------|------|
| `business-employment-manager` | 채용 공고(JD) 작성 · 면접 설계 · 평가 기준 · 온보딩 등 채용 프로세스 전반 관리 |
| `business-resume-screener` | NCS 기반 이력서·자소서 적합성 평가(인간 검토 보조 — 자동 합격/거절 없음, 보호 정보 마스킹) |
| `business-draft-offer` | 오퍼레터·근로계약서 작성 (근로기준법 준수 · 연봉 구조 · 4대보험 공제 · 스톡옵션 조항) |
| `business-performance-review` | MBO·OKR·KPI 성과평가 체계 설계 · 360도 평가 · 피드백 면담 스크립트 |
| `business-people-operations` | 원격·하이브리드 근무 정책 · 협업 도구 선정 · 직원 경험 설계 |
| `business-job-analyzer` | 채용공고(JD) 분해 · 기업 리서치 · 오퍼 검증 |

> 구직자용 스킬 3종(`business-resume-builder`·`business-interview-coach`·`business-portfolio-guide`)은 `moai-career`(커리어코치)로 이관되었습니다.

## 사람인 채용검색 연동 (Saramin PlayMCP)

이 플러그인은 자체 MCP 서버를 포함하지 않습니다. 다만 **claude.ai 커넥터**에서 카카오 PlayMCP를 등록하면 사람인 채용검색 도구(공고 검색·직무 카테고리·기업 정보·지역/지하철 코드 조회 등)를 함께 사용할 수 있습니다.

- 등록 위치: claude.ai → 설정 → 커넥터 → PlayMCP 추가
- 연동 후 `business-job-analyzer` 등의 스킬과 조합해 실시간 공고 기반 분석이 가능합니다

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `recruiter` | worker | 채용 공고 분석·이력서 빌드/스크리닝·면접 코칭·평가·People Ops 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → business-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 차별 금지(보호 속성 평가 기준 배제)·개인정보 최소 수집/마스킹·평가 근거 명시·채용 시장 데이터 출처 인용을 HARD 규칙으로 준수 |
| `screening-auditor` | read-only audit | 평가 기준의 직무 관련성, 차별 소지 표현, 스크리닝 판정-근거 정합성, 개인정보 노출을 회의적으로 검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 이관 안내

이 스킬들은 기존 `moai-coworker` 플러그인의 business 카테고리에서 인사·채용 도메인만 분리해 이관한 것입니다. moai-coworker의 구 경로로 호출하던 워크플로우는 `moai-recruiter:` 네임스페이스로 갱신하세요.

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
