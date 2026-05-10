---
title: "문서 트랙"
weight: 70
description: "Word·PPT·Excel·PDF·한글(HWPX)을 넘나드는 문서 업무를 Cowork로 옮기는 경로."
geekdocBreadcrumb: true
tags: [cookbook, documents]
---

# 트랙 — 문서 자동화

> Word·PPT·Excel·PDF·한글(HWPX)을 넘나드는 문서 업무를 Cowork로 옮기는 경로를 정리합니다. 각 포맷마다 적합한 스킬과 회피해야 할 함정을 함께 다룹니다.

## 트랙 지도

```mermaid
flowchart LR
    Need[업무 필요] --> Choice{출력 형식}
    Choice -->|보고서·제안서·계약서| Docx[moai-office docx-generator]
    Choice -->|발표·피치덱| Pptx[moai-office pptx-designer]
    Choice -->|표·대시보드·재무모델| Xlsx[moai-office xlsx-creator]
    Choice -->|기안서·관공서 제출| Hwpx[moai-office hwpx-writer]
    Choice -->|폼 작성·병합·추출| Pdf[anthropic-skills pdf]

    Docx --> Review[anthropic-skills ai-slop-reviewer]
    Pptx --> Review
    Hwpx --> Review
    Review --> Out[최종 산출물]
{{< terminal title="claude — cowork" >}}

> ## Word (DOCX) — 가장 많이 쓰는 포맷

### 적합한 업무

- 주간·월간 보고서
- 제안서·사업계획서
- 계약서·약관 초안
- 정부 지원사업 신청서

### 추천 스킬

1순위 — `anthropic-skills:docx` (Anthropic 공식)
2순위 — `moai-office:docx-generator` (한국 양식 최적화)

### 실무 흐름

```text
(예시 지시)
D:/Input/Q2-sales-raw.xlsx를 분석해서
Q2 매출 보고서를 Word로 작성해줘.

- 상단 임원 요약 (3줄)
- 제품별 섹션 (5개 제품)
- 각 섹션에 전년 동기 대비 그래프 삽입
- 부록: 원본 데이터 테이블
- 저장 경로: 90_Output/Q2-sales-report.docx
{{< /terminal >}}

### 자주 걸리는 지점

**표 서식이 깨짐.** Word 표는 스킬이 자동 생성하지만 너무 많은 열은 페이지를 벗어납니다. 6열 이내로 유지하거나 가로 방향 페이지를 지시하세요.

**한글 글꼴이 깨짐.** 서버에 맑은고딕이 없는 경우. SKILL.md에 "기본 글꼴 = 나눔고딕" 지시를 추가하세요.

**목차 미생성.** 수동으로 "목차 포함"이라고 명시해야 Heading 1·2 기준 TOC가 삽입됩니다.

## PowerPoint (PPTX)

### 적합한 업무

- 주간 KPI 대시보드
- IR 피치덱
- 임원 보고·경영 전략
- 교육·세미나 자료

### 추천 스킬

1순위 — `anthropic-skills:pptx`
2순위 — `moai-office:pptx-designer` (Pretendard + 명조 한국형 디자인)

### 실무 흐름

{{< terminal title="claude — cowork" >}}
> (예시)
Q2 매출 데이터를 분석해서 임원 대상 PPT 7장을 만들어줘.

- 1장: 타이틀 + 요약 수치 3개
- 2장: 전년 동기 비교 (막대 그래프)
- 3~5장: 제품군 A / B / C 섹션
- 6장: 리스크·이슈
- 7장: 다음 분기 전망 + 제언
- 테마: 화이트 배경, 포인트 컬러 코랄
- 저장: 90_Output/Q2-review.pptx
{{< /terminal >}}

### 자주 걸리는 지점

**이미지가 들어가지 않음.** PPT 스킬은 이미지를 별도로 지정해야 삽입합니다. `moai-media:nano-banana`로 먼저 이미지를 만들고 경로를 전달하세요.

**슬라이드 수가 폭주.** "5~7장"이라고 상한을 지정하지 않으면 15장 이상으로 부풀어 오릅니다.

**글머리표 중복.** 한 슬라이드에 5개 이하 Bullet으로 제한하지 않으면 가독성이 무너집니다.

## Excel (XLSX)

### 적합한 업무

- 재무 모델·예산 시트
- KPI 대시보드
- 데이터 정제·피벗
- 간트차트

### 추천 스킬

1순위 — `anthropic-skills:xlsx`
2순위 — `moai-office:xlsx-creator` (한국 비즈니스 서식 최적화)

### 실무 흐름

{{< terminal title="claude — cowork" >}}
> (예시)
D:/Input/raw-transactions.csv(5만건)를 분석해서
월별·카테고리별 피벗을 만들어줘.

- 시트 1: 원본 데이터 (필터만 적용)
- 시트 2: 월별 합계 피벗 + 스파크라인
- 시트 3: 카테고리별 Top 10
- 시트 4: 조건부 서식 (상위 10% 녹색, 하위 10% 빨강)
- 저장: 90_Output/finance-pivot.xlsx
{{< /terminal >}}

### 자주 걸리는 지점

**수식이 하드코딩됨.** "이 수식은 하드코딩되지 않고 셀 참조로" 명시하지 않으면 값만 채워지는 경우가 있습니다.

**차트가 별도 시트에 생성됨.** "임베드된 차트로 요약 시트에 포함"이라고 지시하세요.

**날짜 형식이 텍스트로 저장됨.** CSV 파싱 시 자주 발생. "date 컬럼은 날짜 형식으로" 명시.

## 한글 (HWPX)

### 적합한 업무

- 정부·공공기관 제출 문서
- 기안서·사내 공문
- 보조금 신청서
- 입찰 서류

### 추천 스킬

`moai-office:hwpx-writer` (Anthropic 공식 없음)

### 실무 흐름

{{< terminal title="claude — cowork" >}}
> (예시)
중소기업청 지원사업 신청서 초안을 한글 문서로 만들어줘.

- 양식: 2026년 디지털 전환 지원사업 공식 양식
- 1페이지: 기업 개요 (사업자등록번호·주소·대표자)
- 2~3페이지: 사업 계획 (추진 배경·목표·예산)
- 4페이지: 기대 효과 (정량·정성 지표)
- 저장: 90_Output/grant-application.hwpx
{{< /terminal >}}

### 자주 걸리는 지점

**한글 프로그램 설치 여부.** HWPX는 한컴오피스가 없어도 열람 가능하지만, 일부 양식은 HWP 전용입니다. 관공서에 HWP·HWPX 둘 다 허용되는지 먼저 확인하세요.

**표 정렬이 미묘하게 어긋남.** 한글 특유의 표 서식을 완벽 재현하긴 어렵습니다. 양식 제출 전 한컴오피스에서 열어 한 번 점검하세요.

## PDF

### 적합한 업무

- 최종 배포용 리포트 (편집 불가)
- 폼 양식 입력 (입사 지원서·계약서)
- 여러 PDF 병합 / 페이지 추출
- 스캔 PDF 텍스트 추출

### 추천 스킬

`anthropic-skills:pdf` (공식). `moai`에서는 대체 스킬을 제공하지 않습니다.

### 실무 흐름

```text
(예시)
D:/Contracts/에 있는 40페이지짜리 계약서 PDF를
열어서 다음 작업을 해줘:

1. 모든 텍스트 추출 (OCR 필요 시 수행)
2. "책임 제한·지체상금·해지 조건" 조항 하이라이트
3. 리스크 조항 요약을 별도 Word 보고서로 생성
4. 원본 PDF + 요약 Word를 묶어서
   90_Output/contract-review-YYYY-MM-DD.zip으로 압축
```

### 자주 걸리는 지점

**스캔 PDF OCR 정확도.** 저해상도 스캔은 오인식이 많습니다. 300dpi 이상 권장.

**폼 필드가 자동 채워지지 않음.** 일부 PDF는 필드가 이미지로 렌더링되어 있어 자동 입력 불가. 이런 경우는 [PDF Tools MCP](https://github.com/modelcontextprotocol/servers)의 `bulk_fill_from_csv`로 우회하세요.

## 트랙 종합 체크리스트

```
[ ] 출력 포맷 확정 후 적합 스킬 선택
[ ] 입력 경로·출력 경로를 절대 경로로 지정
[ ] 표·그래프·이미지 상한을 프롬프트에 명시
[ ] 한국어 글꼴·템플릿 양식 명시
[ ] 최종 산출물은 ai-slop-reviewer로 검수 (텍스트만)
[ ] 숫자·날짜 형식·수식은 검토 대상에서 제외
[ ] 민감 정보가 담긴 경우 별도 보안 폴더에 저장
```

## 다음 읽을거리

- [트랙 — 데이터 분석](../track-data/)
- [트랙 — 마케팅](../track-marketing/)
- [계약서 검토 리포트](../contract-review/)
- [사업계획서 자동화](../business-plan/)

---

### Sources
- [Anthropic Skills — Office](https://github.com/anthropics/anthropic-cookbook/tree/main/skills)
- [modu-ai/cowork-plugins — moai-office](https://github.com/modu-ai/cowork-plugins/tree/main/moai-office)
