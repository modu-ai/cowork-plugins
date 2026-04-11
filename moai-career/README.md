# moai-career

커리어 준비 플러그인 — 자기소개서, 이력서, 면접 코칭, 채용공고 분석, 포트폴리오.

대학생과 취준생을 위한 취업 준비 도구입니다. 2026년 채용 시장 트렌드(스킬 기반 채용, AI면접 확대, 팀핏 평가)를 반영하여 자소서 작성부터 면접 대비까지 커리어 준비 전 과정을 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [resume-builder](./skills/resume-builder/) | STAR 기법 자소서, ATS 최적화 이력서, 영문 CV, 블라인드 채용 대응 | 2 | ✅ |
| [interview-coach](./skills/interview-coach/) | AI면접/역량면접/PT면접/토론면접 대비, 모의 면접 루프, 답변 코칭 | 2 | ✅ |
| [job-analyzer](./skills/job-analyzer/) | JD 분석, 역량 매칭, 기업 리서치, 지원 전략 수립 | 1 | ✅ |
| [portfolio-guide](./skills/portfolio-guide/) | 개발/디자인/마케팅/기획 분야별 포트폴리오, 프로젝트 기술서 | 1 | ✅ |

## 공유 에이전트

| 에이전트 | 소속 | 용도 |
|---------|------|------|
| quality-evaluator | moai-core | 산출물 품질 PASS/FAIL 판정 |
| korean-tone-reviewer | moai-hr | 직급별 경어 사용 및 비즈니스 톤 적절성 검토 |

## 사용 예시

```
삼성전자 DX부문 소프트웨어 엔지니어 자소서 써줘. 컴공 전공, 인턴 경험 있어.
```

```
카카오 백엔드 개발자 면접 예상 질문 10개 뽑아주고, 모의 면접도 해줘.
```

```
이 채용공고 분석해줘. [공고 텍스트 붙여넣기] 내 경험이랑 매칭도 해줘.
```

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-career` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/moai-cowork-plugins)
