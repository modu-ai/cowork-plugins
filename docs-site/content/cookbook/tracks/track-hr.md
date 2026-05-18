---
title: "HR·커리어 트랙"
weight: 26
description: "인사 담당자와 구직자를 위한 채용·평가·온보딩·자기소개서 워크플로우. moai-hr 5스킬 + moai-career 4스킬을 한 줄 요청으로 자동 처리."
geekdocBreadcrumb: true
---

> **대상**: 인사 담당자, HR 매니저, 구직자, 취준생, 경력 전환자
> **전제**: moai-core · moai-hr 또는 moai-career 활성화
> **소요**: 시나리오당 약 3-10분

## 무엇을 할 수 있나

```mermaid
flowchart LR
    subgraph HR["채용 측 (moai-hr)"]
        H1["draft-offer<br/>채용공고·JD"]
        H2["resume-screener<br/>이력서 분류"]
        H3["employment-manager<br/>온보딩"]
        H4["performance-review<br/>인사평가"]
        H5["people-operations<br/>HR 정책"]
    end
    subgraph Career["구직 측 (moai-career)"]
        C1["resume-builder<br/>이력서"]
        C2["interview-coach<br/>면접 대비"]
        C3["job-analyzer<br/>JD 분석"]
        C4["portfolio-guide<br/>포트폴리오"]
    end
    HR <--> Career
```

## 한 줄 요청 예시 4종

| # | 한 줄 요청 (HR 또는 구직자) | 자동 체인 |
|---|---|---|
| 1 | "데이터분석가 채용공고 + JD 만들어줘" | draft-offer → docx-generator → ai-slop |
| 2 | "이력서 50개 분류해줘" | resume-screener → 등급별 분류 → docx |
| 3 | "데이터분석가 이력서 + 포트폴리오 만들어줘" | resume-builder → portfolio-guide → ai-slop |
| 4 | "내일 네이버 면접 대비 시켜줘" | job-analyzer → interview-coach → 모의 Q&A |

---

## 시나리오 ① 채용공고 + JD 작성 (HR, 약 5분)

### 사용자 입력

{{< terminal title="claude — cowork" >}}
> 데이터분석가 채용공고 만들어줘
{{< /terminal >}}

### 시스템 인터뷰

1. **레벨**: 신입 · 주니어 (1-3년) · 시니어 (5년+) · 매니저
2. **고용형태**: 정규직 · 계약직 · 인턴 · 프리랜서
3. **연봉 범위**: 공개 / 비공개 / "협의"
4. **필수 스킬**: SQL / Python / Tableau / R 등
5. **회사 특징**: 원격 / 출퇴근 / 하이브리드, 복지 강조

### 자동 체인

`draft-offer` → `docx-generator` → `ai-slop-reviewer`

### 산출물

- 한국 채용 시장 표준 양식 채용공고 (1페이지)
- 직무 기술서(JD) 1-2페이지
- 채용 채널 추천 (사람인·잡코리아·원티드·링크드인)

---

## 시나리오 ② 이력서 50개 일괄 분류 (HR, 약 10분, 배치 패턴)

### 사용자 입력

{{< terminal title="claude — cowork" >}}
> ./resumes/ 폴더 데이터분석가 이력서 50개 분류해줘
{{< /terminal >}}

### 시스템 인터뷰

1. **JD 첨부** (또는 자동 호출): 매칭 기준
2. **분류 등급**: A (면접 즉시) / B (검토) / C (보류) / D (거절)
3. **출력 형식**: 표 + 등급별 요약 DOCX
4. **개인정보 보호**: 이름 마스킹 여부 (HARD)

### 자동 체인

`resume-screener` (이력서 50개 × JD 매칭) → 등급별 분류 → `docx-generator` → `ai-slop-reviewer`

### 산출물

- 등급별 분류표 + 핵심 요약 (역량·경력·교육·자격증)
- A 등급 면접 질문 자동 생성 (`interview-coach` 자동 체인)
- 거절 사유 표준 메시지

---

## 시나리오 ③ 이력서 + 포트폴리오 자동 생성 (구직자, 약 8분)

### 사용자 입력

{{< terminal title="claude — cowork" >}}
> 데이터분석가 이력서 만들어줘
{{< /terminal >}}

### 시스템 인터뷰

1. **목표 포지션**: 회사·JD URL 첨부 가능
2. **경력 데이터**: GitHub · LinkedIn · CSV · 자유 텍스트
3. **이력서 유형**: 국문 / 영문 CV / 둘 다
4. **분량**: 1페이지 / 2페이지 / ATS 최적화
5. **포트폴리오 동시 작성**: 예/아니오

### 자동 체인

`resume-builder` (KKK-STAR 프레임워크 + ATS 최적화) → `portfolio-guide` → `ai-slop-reviewer` → `humanize-korean`

### 산출물

- 국문/영문 이력서 (워드+PDF)
- 포트폴리오 가이드 (GitHub README · Notion · PDF)
- ATS 호환성 점수

---

## 시나리오 ④ 면접 대비 — 모의 Q&A (구직자, 약 7분)

### 사용자 입력

{{< terminal title="claude — cowork" >}}
> 내일 네이버 데이터분석가 면접 대비 시켜줘
{{< /terminal >}}

### 시스템 인터뷰

1. **JD URL** 또는 회사·포지션
2. **면접 유형**: 1차 (실무) / 2차 (역량) / 임원
3. **본인 이력서 첨부** (선택)
4. **약점·우려 질문** (선택)

### 자동 체인

`job-analyzer` (JD 분석) → `interview-coach` (예상 질문 15-20개 + 모범 답안 가이드 + STAR 기법) → 모의 면접 Q&A 라이브

### 산출물

- 예상 질문 15-20개 (기술·인성·상황 분류)
- 각 질문별 답변 가이드 (STAR 구조)
- 본인 이력서 약점 보완 답변

---

## AskUserQuestion 표준 슬롯 (HR 트랙 공통)

| 슬롯 | 예시 값 |
|---|---|
| 포지션·레벨 | 신입·주니어·시니어·매니저 |
| 고용 형태 | 정규·계약·인턴·프리랜서 |
| 회사 단계 | 스타트업·중견·대기업·외국계 |
| 개인정보 처리 | 마스킹 / 익명 / 실명 (HARD) |
| 출력 형식 | DOCX · PDF · ATS 호환 텍스트 |

---

## 자주 묻는 질문

### Q. 이력서 분류 시 개인정보 보호는?

기본값으로 **이름 마스킹** + 학력·경력만 자동 추출. AskUserQuestion에서 명시 변경 가능. 처리 후 원본은 보관하지 않음.

### Q. ATS(이력서 자동 분류 시스템) 최적화란?

지원사 인사팀이 사용하는 ATS가 키워드 매칭으로 이력서를 1차 분류합니다. `resume-builder`는 JD 키워드를 자동 매핑해 매칭률을 높입니다.

### Q. 한국 + 영문 동시 작성 가능?

예. AskUserQuestion에서 "둘 다" 선택 시 자동 병렬 생성. 톤·형식 차이 자동 적용 (한국 격식체 vs 영문 Action verb 시작).

---

## 다음 단계

- **[사용 패턴 가이드](../../../cowork/patterns/)**
- **[운영 트랙](../track-operations/)** — HR 외 운영팀 워크플로우
- **[moai-hr 플러그인](../../../plugins/moai-hr/)** — 5스킬
- **[moai-career 플러그인](../../../plugins/moai-career/)** — 4스킬

---

### Sources

- [moai-hr · moai-career 디렉터리](https://github.com/modu-ai/cowork-plugins)
- 한국 채용 시장 표준 양식 (사람인·잡코리아·원티드)
- STAR 기법 (Situation·Task·Action·Result) 면접 답변 구조
