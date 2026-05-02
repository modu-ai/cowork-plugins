# moai-hr

인사/노무 플러그인 — 근로계약서, 4대보험, 채용 파이프라인, 성과평가, 연차/퇴직금.

근로기준법 및 4대보험 체계를 반영한 인사 실무 전반을 지원합니다. 2026년 기준 최저임금, 퇴직금 규정, 4대보험 요율을 반영합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [employment-manager](./skills/employment-manager/) | JD 작성, 면접 설계, 평가 기준, 온보딩 체크리스트, 멘토링 프로그램 | 2 | ✅ |
| [people-operations](./skills/people-operations/) | 원격/하이브리드 근무 정책, 협업 도구, 생산성 관리, 직원 경험 설계 | 1 | ✅ |
| [draft-offer](./skills/draft-offer/) | 채용 제안서, 근로계약서 초안, 연봉 구조 최적화, 4대보험 공제 계산, 스톡옵션 조항 | 0 | ✅ |
| [performance-review](./skills/performance-review/) | MBO/OKR/KPI 체계, 360도 평가 설계, 인사 고과, 피드백 면담 스크립트 | 0 | ✅ |
| [resume-screener](./skills/resume-screener/) | NCS 국가직무능력표준 기반 이력서·자기소개서 적합성 평가 (4축 점수·면접 추천 질문) | 1 | ✅ |

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

## 주요 워크플로우 체인

```
신규 채용 풀 사이클
  employment-manager(JD·면접 설계) → resume-screener(이력서 평가) → draft-offer(오퍼·근로계약서) → docx-generator

분기 성과평가
  performance-review(MBO/OKR/KPI) → docx-generator(평가지) → ai-slop-reviewer

원격 근무 정책 도입
  people-operations(정책 설계) → docx-generator(사내 가이드) → ai-slop-reviewer

연봉 협상·갱신
  draft-offer(연봉 구조 + 4대보험) → xlsx-creator(연봉 시뮬레이션) → docx-generator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 취준생 관점 자소서·이력서 | `moai-career/resume-builder` |
| 4대보험 요율 계산·세무 | `moai-finance/tax-helper` |
| 근로계약서 법적 검토 | `moai-legal/contract-review` |
| 사내 교육 커리큘럼 설계 | `moai-education/curriculum-designer` |

## 한국 노무·인사 환경 특화

- **2026년 4대보험 요율** 자동 적용 (국민연금/건강/고용/산재)
- **근로기준법·최저임금법** 위반 자동 경고 (계약서 검토 시)
- **NCS 직무능력표준** 기반 채용·평가 매핑
- **퇴직금 중간정산·DC형/DB형 IRP** 시뮬레이션
- **공유 에이전트**: `moai-hr/korean-tone-reviewer` — 직급별 경어·비즈니스 톤 자동 검토 (다른 플러그인에서도 호출 가능)

## 설치

Settings > Plugins > cowork-plugins에서 `moai-hr` 선택

## 참고자료

| 항목 | URL |
|------|-----|
| [고용노동부](https://www.moel.go.kr/) | 근로기준법, 4대보험 |
| [국민건강보험공단](https://www.nhis.or.kr/) | 4대보험 가입/조회 |
