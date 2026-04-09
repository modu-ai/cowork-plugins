# moai-hr

인사/노무 플러그인 — 근로계약서, 4대보험, 채용 파이프라인, 성과평가, 연차/퇴직금.

근로기준법 및 4대보험 체계를 반영한 인사 실무 전반을 지원합니다. 2026년 기준 최저임금, 퇴직금 규정, 4대보험 요율을 반영합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [employment-manager](./skills/employment-manager/) | JD 작성, 면접 설계, 평가 기준, 온보딩 체크리스트, 멘토링 프로그램 | 2 | ✅ |
| [people-operations](./skills/people-operations/) | 원격/하이브리드 근무 정책, 협업 도구, 생산성 관리, 직원 경험 설계 | 1 | ✅ |
| [draft-offer](./skills/draft-offer/) | 채용 제안서, 연봉 구조 최적화, 4대보험 공제 계산, 스톡옵션 조항 | 0 | ✅ |
| [performance-review](./skills/performance-review/) | MBO/OKR/KPI 체계, 360도 평가 설계, 인사 고과, 피드백 면담 스크립트 | 0 | ✅ |

## 에이전트

| 에이전트 | 모델 | 역할 |
|---------|:----:|------|
| korean-tone-reviewer | Haiku | 직급별 경어 사용 및 비즈니스 톤 적절성 검토. moai-support, moai-business 등에서 공유 호출 |

## 사용 예시

```
개발자 시니어 포지션 JD 작성해줘. 경력 5년 이상, 리모트 가능.
```

```
신입 온보딩 체크리스트 만들어줘. 입사 첫 주에 해야 할 것들 정리해줘.
```

```
OKR 기반 성과평가 체계 설계해줘. 분기별 리뷰 프로세스 포함.
```

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-hr` 선택
