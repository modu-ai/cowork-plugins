# moai-education

교육/연구 플러그인 — 강의설계, 커리큘럼 개발, 논문 리서치, 시험 문제 출제.

온라인 강의 제작부터 학술 논문 작성, 자격증 시험 대비까지 교육/연구 영역 전반을 지원합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [curriculum-designer](./skills/curriculum-designer/) | 강의 목차 설계, 학습 목표 정의, 역량 갭 분석, 외국어 학습 전략 | 3 | ✅ |
| [research-assistant](./skills/research-assistant/) | 데이터 수집/분석, 학술 논문 초안, 연구 설계, 인용/참고문헌 관리 | 3 | ✅ |
| [assessment-creator](./skills/assessment-creator/) | 시험 문제 출제, 기출 분석, 자격증 모의고사, 학습 평가 설계 | 1 | ✅ |

## 사용 예시

```
파이썬 입문 8주 온라인 강의 커리큘럼 설계해줘. 비개발자 대상.
```

```
"생성형 AI의 교육적 활용" 주제 논문 리서치 계획 세워줘
```

```
정보처리기사 실기 모의고사 10문제 만들어줘
```

## 주요 워크플로우 체인

```
온라인 강의 풀 패키지
  curriculum-designer(목차) → assessment-creator(시험·평가) → pptx-designer(강의 슬라이드) → ai-slop-reviewer

학술 논문 작성
  research-assistant(데이터 수집·인용) → moai-research/paper-writer → docx-generator → ai-slop-reviewer

자격증 시험 대비
  assessment-creator(기출 분석·모의고사) → docx-generator → ai-slop-reviewer

기업 교육 부트캠프
  curriculum-designer(8주 일정·블룸 분류) → assessment-creator(주차별 평가) → pptx-designer(주차별 슬라이드)
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 학술 논문 본문 작성(KCI/IEEE 포맷) | `moai-research/paper-writer` |
| 연구비 신청서(NRF/IITP) | `moai-research/grant-writer` |
| 특허 검색·FTO 분석 | `moai-research/patent-search` |
| 사내 HR 교육·온보딩 체크리스트 | `moai-hr/employment-manager` |
| 어린이 발달 가이드 | `moai-lifestyle/wellness-coach` |

## 한국 교육 환경 특화

- **블룸 분류법 기반 학습 목표**: 6단계 인지·정의·심동 영역 매칭
- **K-MOOC·HRD-Net 양식 호환**: 정부 지원 교육과정 신청 양식
- **NCS 직무능력 매핑**: 강의 학습 목표를 국가직무능력표준에 연결
- **자격증 한국형 출제 패턴**: 정보처리기사·SQLD·ADsP 등 기출 분석 반영

## 설치

Settings > Plugins > cowork-plugins에서 `moai-education` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
