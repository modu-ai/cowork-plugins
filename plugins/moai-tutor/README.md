# 튜터 (moai-tutor)

교육 전담 AI 코워커입니다. 커리큘럼 설계·학습 자료·평가 문항 제작·강좌 운영 같은 강사 실무와 논문 검색·작성·연구 보조 같은 학술 워크플로우까지 스킬 11종을 하나의 플러그인으로 제공합니다. 강사와 학습자 양쪽을 모두 지원하며, 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> 이 플러그인의 스킬들은 moai-coworker에서 이관되었습니다.

**이런 분께 추천**: 강사·교수·교사 · 교육 기획자 · 대학원생·연구자 · 독학 학습자

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-tutor`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-tutor@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-tutor@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 11종

호출 형식: `/moai-tutor:education-<스킬명>` — 예: `/moai-tutor:education-curriculum-designer`. 자연어 요청("Python 입문 8주 커리큘럼 짜줘")으로도 자동 매칭됩니다.

### 교육 설계·운영 (6종)

| 스킬 | 역할 |
|------|------|
| `education-curriculum-designer` | 주차별 목차·학습 목표·평가 방법이 담긴 커리큘럼 설계 |
| `education-learning-material` | 도식·차트·수식·코드가 들어간 단일 HTML 학습자료 제작 |
| `education-assessment-creator` | 정답·해설 포함 시험 문제지·모의고사·오답 분석표 |
| `education-course-operations-manual` | 강의·연수·워크숍 운영 매뉴얼 (시간표·체크리스트·Plan B) |
| `education-course-followup-sequence` | 강의 후 30일 수강생 후기 요청 카피 5종 (D+1~D+30) |
| `education-learning-project` | 독학용 학습 프로젝트 셋업 (로드맵·진도 추적·학습 CLAUDE.md) |

### 학술·연구 (5종)

| 스킬 | 역할 |
|------|------|
| `education-paper-search` | RISS·KCI·DBpia·Google Scholar 논문 통합 검색 + 서지 정리 |
| `education-paper-writer` | 학술 논문 초안 작성 + APA·KCI·IEEE 참고문헌 자동 생성 |
| `education-research-assistant` | 문헌 검토 보고서·연구 계획서·참고문헌 목록 |
| `education-grant-writer` | NRF·IITP·KIAT 등 정부 연구비 신청서 초안 |
| `education-tutor-research` | 학습 질문에 대한 병렬 웹 조사 + 출처 검증 학습 근거 종합 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `curriculum-designer` | worker | 커리큘럼·학습자료·평가·운영 매뉴얼·논문 산출물을 만드는 실무 에이전트. 백워드 설계(목표 → 평가 → 수업)로 동작하며 인용 실존 검증·저작권 준수를 강제 |
| `assessment-auditor` | read-only audit | 문항 정답·해설을 직접 재풀이하고 목표-평가 정렬과 인용 실존을 회의적으로 검증하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
