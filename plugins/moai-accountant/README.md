# 재무·세무 담당 (moai-accountant)

재무·세무 전담 AI 직원입니다. 재무제표 작성·결산 관리·차이 분석·IR 같은 사업 재무 실무와 연말정산·세금·가계 예산·투자 입문 같은 개인 재무까지 스킬 11종을 하나의 플러그인으로 제공합니다. OpenDART 전자공시 MCP 연동으로 공시 데이터에 근거한 분석을 수행하며, 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> 이 플러그인의 스킬들은 moai-coworker에서 이관되었습니다.

**이런 분께 추천**: 사업자 · 재무 담당자 · 개인 재테크 입문자

> ※ 본 플러그인의 산출물은 세무사·회계사 자문을 대체하지 않는 참고 자료입니다.

## 설치

Claude Code에서 두 단계로 설치합니다:

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-accountant@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-accountant
```

## 스킬 11종

호출 형식: `/moai-accountant:finance-<스킬명>` — 예: `/moai-accountant:finance-tax-helper`. 자연어 요청("연말정산 환급 늘리는 법 알려줘")으로도 자동 매칭됩니다.

### 사업 재무 (5종)

| 스킬 | 역할 |
|------|------|
| `finance-financial-statements` | 재무상태표·손익계산서·현금흐름표 작성 (K-IFRS 대응) |
| `finance-close-management` | 월말·분기·연간 결산 체크리스트 + 급여·4대보험 정산 |
| `finance-variance-analysis` | 예산 대비 실적 차이 분석 + 수익성 개선 권고 |
| `finance-investor-relations` | IR 피치덱 + 3개년 재무 모델·밸류에이션 |
| `finance-tax-helper` | 종합소득세·부가세·3.3% 원천징수 등 한국 세법 안내 |

### 개인 재무 (6종)

| 스킬 | 역할 |
|------|------|
| `finance-personal-tax-saver` | 연말정산 소득·세액공제 절세 전략 |
| `finance-household-budget` | 통장 쪼개기·50/30/20 예산·가계부·소비 회고 |
| `finance-wealth-roadmap` | 재무 진단 → 목표 → 종잣돈 → 자산 관리 로드맵 |
| `finance-invest-primer` | 투자 입문 원칙·자산군·초보 포트폴리오 |
| `finance-insurance-fit` | 필요 보험 진단 + 과보험·중복 리모델링 |
| `finance-econ-literacy` | 금리·환율·물가 등 경제지표를 '내 돈' 관점으로 해설 |

## MCP 연동 1종

플러그인 루트 `.mcp.json`에 OpenDART 전자공시 MCP 서버가 선언되어 있습니다. 자격증명은 **환경변수로만** 설정하세요(파일에 키를 적지 않습니다).

| 서버 | 플랫폼 | 필요 환경변수 | 비고 |
|------|--------|---------------|------|
| `dart` | OpenDART 전자공시 (83 API → 15 도구, XBRL 계산 검증 포함) | `DART_API_KEY` | 키 발급: opendart.fss.or.kr 회원가입 → 인증키 신청(무료, 일 20,000건). 사전 설치: Node.js 20.19+ |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `finance-analyst` | worker | 재무제표·결산·차이 분석·IR·절세 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → finance-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 모든 수치에 출처(공시·원장·세법 조항) 인용, 추정치 라벨링 |
| `close-auditor` | read-only audit | 계정 대사·세액 계산·밸류에이션을 회의적으로 재검산하는 감사 에이전트. 출처 없는 수치와 과세 연도 오적용을 reject하며 증거 기반 PASS/FAIL 판정만 반환 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
