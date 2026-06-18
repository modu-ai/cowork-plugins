# moai-education

강사·교수·교사 교육 콘텐츠 풀스택 — 커리큘럼 설계, 시험 출제, 학술 리서치, **강의·수업·연수·워크숍 운영 매뉴얼**, **수강 후 30일 후기 자산화 시퀀스**.

[![버전](https://img.shields.io/badge/version-2.10.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-5-success)](#스킬)

온라인 강의 제작부터 학술 논문 작성, 자격증 시험 대비, 강의·연수 운영 실무, 강의 후 후기 자산화까지 강사·교수·교사가 운영하는 교육 활동 전반을 지원합니다.

## 스킬

| 스킬 | 설명 | 상태 |
|------|------|:----:|
| [curriculum-designer](./skills/curriculum-designer/) | 강의 목차 설계, 학습 목표 정의, 역량 갭 분석, 외국어 학습 전략 | ✅ |
| [research-assistant](./skills/research-assistant/) | 데이터 수집/분석, 학술 논문 초안, 연구 설계, 인용/참고문헌 관리 | ✅ |
| [assessment-creator](./skills/assessment-creator/) | 시험 문제 출제, 기출 분석, 자격증 모의고사, 학습 평가 설계 | ✅ |
| [course-operations-manual](./skills/course-operations-manual/) | 강의·수업·연수·워크숍 운영 매뉴얼 자동 생성. 일자별 시간표 + 강사·조교 동선 + D-N 사전 준비물 + 환경·설비 체크리스트 + 리스크 매트릭스 + Plan B 5건+. `moai-office:docx-generator` 자동 체이닝으로 Word(.docx) 출력 (구 `course-curriculum-design`) | ✅ |
| [course-followup-sequence](./skills/course-followup-sequence/) | 강의 종료 후 30일 follow-up 시퀀스. 후기 카피 5종(D+1·D+3·D+7·D+14·D+30) + 인센티브·자산화 가이드. 체인: copywriting → ai-slop-reviewer → korean-spell-check | ✅ |

## 사용 예시

```
파이썬 입문 8주 온라인 강의 커리큘럼 설계해줘. 비개발자 대상.
```
→ `curriculum-designer`

```
"생성형 AI의 교육적 활용" 주제 논문 리서치 계획 세워줘
```
→ `research-assistant`

```
정보처리기사 실기 모의고사 10문제 만들어줘
```
→ `assessment-creator`

```
사내 AI 활용 2일 워크숍 운영 매뉴얼 만들어줘 — 강사·조교 동선·Plan B 포함
```
→ `course-operations-manual`

```
강의 종료 후 D+1·D+3·D+7·D+14·D+30 후기 시퀀스 카피 만들어줘
```
→ `course-followup-sequence`

## 주요 워크플로우 체인

```
온라인 강의 풀 패키지
  curriculum-designer(목차) → assessment-creator(시험·평가)
    → pptx-designer(강의 슬라이드) → ai-slop-reviewer

학술 논문 작성
  research-assistant(데이터 수집·인용) → moai-research/paper-writer
    → docx-generator → ai-slop-reviewer

자격증 시험 대비
  assessment-creator(기출 분석·모의고사) → docx-generator → ai-slop-reviewer

강의·연수·워크숍 운영 풀 사이클
  course-operations-manual(D-N 운영 매뉴얼) → moai-office:docx-generator(.docx)
    ↓ (D-7 사전 안내)
  사전 준비물 메일 발송 (course-operations-manual --output prep-mail)
    ↓ (D-1 리허설)
  course-operations-manual(시간표·동선표 출력)
    ↓ (D+0 강의·수업 실행)
  강의 진행
    ↓ (D+1 ~ D+30)
  course-followup-sequence(5종 후기 카피)
    → moai-content:copywriting → ai-slop-reviewer → korean-spell-check
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 학술 논문 본문 작성(KCI/IEEE 포맷) | `moai-research:paper-writer` |
| 연구비 신청서(NRF/IITP) | `moai-research:grant-writer` |
| 특허 검색·FTO 분석 | `moai-research:patent-search` |
| 사내 HR 교육·온보딩 체크리스트 | `moai-hr:employment-manager` |
| 어린이 발달 가이드 | `moai-lifestyle:wellness-coach` |
| 학습 목표·역량 갭 중심 교육과정 설계 | `curriculum-designer` (이 플러그인) |
| 강의·연수·워크숍 운영 실무 매뉴얼 | `course-operations-manual` (이 플러그인) |
| 일반 마케팅·광고 카피 | `moai-content:copywriting` |
| 강의 후 수강생 후기 자산화 시퀀스 | `course-followup-sequence` (이 플러그인) |

## 한국 교육 환경 특화

- **블룸 분류법 기반 학습 목표**: 6단계 인지·정의·심동 영역 매칭
- **K-MOOC·HRD-Net 양식 호환**: 정부 지원 교육과정 신청 양식
- **NCS 직무능력 매핑**: 강의 학습 목표를 국가직무능력표준에 연결
- **자격증 한국형 출제 패턴**: 정보처리기사·SQLD·ADsP 등 기출 분석 반영
- **운영 매뉴얼 실무 자동화**: 강사·조교 동선표, D-N 사전 준비물 메일, 리스크 Plan B 매트릭스 5건+

## 설치

Settings > Plugins > cowork-plugins에서 `moai-education` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
