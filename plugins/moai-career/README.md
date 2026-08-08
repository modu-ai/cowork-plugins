# 커리어코치 (moai-career)

구직자 편 커리어 코칭 전담 AI 코워커입니다. 자기소개서·이력서·경력기술서 작성, 분야별 포트폴리오 구성, 유형별 면접 준비까지 커리어 전환 실무 스킬을 하나의 플러그인으로 제공합니다. 인사채용(`moai-recruiter`, 고용주 편)과 구분되는 구직자 관점 플러그인이며, 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

**이런 분께 추천**: 이직 준비자 · 취업 준비생 · 주니어 직장인

## 설치

Claude Code에서 두 단계로 설치합니다:

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-career@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-career
```

## 스킬 5종

호출 형식: `/moai-career:<스킬명>` — 예: `/moai-career:career-resume`. 자연어 요청("자소서 써줘")으로도 자동 매칭됩니다.

| 스킬 | 역할 |
|------|------|
| `career-resume` | 자소서·이력서·경력기술서·영문 CV·링크드인 작성 (KKK-STAR 자소서 · USP+CAR 이력서 · ATS·블라인드·NCS 모드) |
| `career-portfolio` | 분야별(개발·디자인·마케팅·기획) 포트폴리오 구성 · 프로젝트 기술서 · 노션 포트폴리오 |
| `career-interview` | 유형별 면접 대비(AI 역량검사·BEI·PT·토론·임원·팀핏) + 모의 면접 루프 + 역질문 |
| `career-transition` | 이직·전직 전략 9단계(타이밍 진단→시장조사→경력 서사→연봉 협상→오프보딩) + 이직 전략 캔버스·연봉 협상 스크립트·인수인계 체크리스트 |
| `career-junior-onboarding` | 신입·주니어 첫 90일 온보딩 코칭(셀프 온보딩·질문 3요소·보고 기술·사수 없이 성장) + 90일 온보딩 플랜·질문 카드 템플릿 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `career-coach` | worker | 이력서·자소서·포트폴리오·면접 준비 산출물을 만드는 구직자 편 실무 에이전트. 목표 이해 → 계획 → business-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 경력 날조·수치 발명 금지(리프레이밍은 허용, 발명은 불허)·정직한 자기표현 코칭·개인정보 최소 기록·시장 데이터 출처 인용을 HARD 규칙으로 준수 |
| `resume-auditor` | read-only audit | 이력서 주장-실경력 정합성, 성과 수치 출처, 날짜/타임라인 일관성, 기만 코칭 여부를 회의적으로 검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 이관 안내

이 스킬들은 기존 `moai-recruiter` 플러그인에서 구직자용 스킬만 분리해 이관한 것입니다. moai-recruiter의 구 경로로 호출하던 워크플로우는 `moai-career:` 네임스페이스로 갱신하세요. 채용 담당자(고용주 편) 스킬은 `moai-recruiter`에 그대로 있습니다.

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
