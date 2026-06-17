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
flowchart TD
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
```

## 문서 자동화는 조립 라인입니다

문서 자동화 트랙을 처음 보면 "문서 하나 만들면 되지 왜 Word·PPT·Excel·한글·PDF 다섯 갈래로 갈라져 있나?"라는 의문이 듭니다. 이유는 목적이 다르기 때문입니다. 인쇄소에 비유하면 이해가 쉽습니다. 손님이 원고를 들고 오면 직원이 먼저 "이걸 뭘로 만들 거냐" 묻습니다. 보고서면 워드 인쇄기로, 발표 자료면 슬라이드 인쇄기로, 표면 엑셀 인쇄기로 찍습니다. 기계가 다르듯 만드는 스킬도 다릅니다. 같은 원고라도 "읽는 글"인지, "보여주는 발표"인지, "계산하는 표"인지에 따라 어울리는 결과물이 갈립니다.

각 기계로 찍어낸 뒤에는 마지막으로 교정 전문가(`ai-slop-reviewer`)가 맞춤법과 어투를 점검합니다. AI가 만든 글은 어딘가 기계적이라 사람이 쓴 것처럼 다듬는 단계가 필요하기 때문입니다. 점검이 끝나면 최종 산출물을 봉투에 넘겨줍니다. 즉 문서 자동화는 "원본 재료 → 목적에 맞는 기계 선택 → 인쇄 → 교정 → 납품"의 조립 라인(순서대로 흘러가는 작업 흐름)입니다. 다섯 포맷은 서로 경쟁하는 게 아니라, 각자 다른 목적에 대응하는 전용 기계일 뿐입니다.

```mermaid
flowchart LR
    In["원본 재료<br/>(데이터 · 원고)"] --> Pick{"목적이 무엇인가"}
    Pick -->|읽는 글| W["Word<br/>(docx-generator)"]
    Pick -->|보여주는 발표| P["PPT<br/>(pptx-designer)"]
    Pick -->|계산하는 표| X["Excel<br/>(xlsx-creator)"]
    Pick -->|관공서 제출| H["한글<br/>(hwpx-writer)"]
    Pick -->|편집 불가 배포| F["PDF<br/>(pdf)"]
    W --> Q["교정<br/>(ai-slop-reviewer)"]
    P --> Q
    H --> Q
    X --> Out["최종 산출물<br/>(90_Output)"]
    F --> Out
    Q --> Out

    style In fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style Pick fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style W fill:#e6f0ef,stroke:#144a46,color:#09110f
    style P fill:#e6f0ef,stroke:#144a46,color:#09110f
    style X fill:#e6f0ef,stroke:#144a46,color:#09110f
    style H fill:#e6f0ef,stroke:#144a46,color:#09110f
    style F fill:#e6f0ef,stroke:#144a46,color:#09110f
    style Q fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style Out fill:#eaeaea,stroke:#6e6e6e,color:#09110f
```

```mermaid
flowchart LR
    IN["원본 재료<br/>데이터·원고·템플릿<br/>(D:/Input, Drive)"]

    PICK{"목적 분기<br/>이걸 뭘로 만들 거냐?"}

    W["Word — 읽는 글<br/>docx-generator"]
    P["PPT — 보여주는 발표<br/>pptx-designer"]
    H["한글 — 관공서 제출<br/>hwpx-writer"]
    X["Excel — 계산하는 표<br/>xlsx-creator"]
    F["PDF — 편집 불가 배포<br/>pdf"]

    REV["ai-slop-reviewer<br/>어투·표현 다듬기<br/>(텍스트 산출물만)"]
    SKIP["Excel·PDF<br/>어투 없음 → 검수 생략"]

    OUT["최종 산출물<br/>90_Output / 배포 폴더"]

    IN -->|"스테이지 1 → 2"| PICK

    PICK -->|"텍스트형"| W
    PICK -->|"텍스트형"| P
    PICK -->|"텍스트형"| H
    PICK -->|"숫자·배포형"| X
    PICK -->|"숫자·배포형"| F

    W -->|"검수"| REV
    P -->|"검수"| REV
    H -->|"검수"| REV
    X -.->|"생략"| SKIP
    F -.->|"생략"| SKIP

    REV ==>|"납품"| OUT
    SKIP -.->|"납품"| OUT
```

## Word (DOCX) — 가장 많이 쓰는 포맷

### 적합한 업무

- 주간·월간 보고서
- 제안서·사업계획서
- 계약서·약관 초안
- 정부 지원사업 신청서

### 스킬은 왜 1순위와 2순위 두 개인가

각 포맷 아래에는 스킬이 보통 두 개 나옵니다. 양복 맞춤에 비유하면 이유가 보입니다. 1순위인 Anthropic 공식 스킬은 대량 생산되는 기성 정장입니다. 어디서든 잘 맞고 호환성이 확실하지만, 한국 몸매에는 살짝 헐렁할 수 있습니다. 반면 2순위인 `moai-office` 스킬은 한국 재단사가 맞춘 정장입니다. 맑은고딕 글꼴, 한국 비즈니스 서식, 정부 양식에 딱 맞지만 해외 표준 호환성은 기성보다 떨어질 수 있습니다.

따라서 기준은 "이 문서를 어디에 제출하느냐"입니다. 글로벌 고객사나 외국 바이어에게 보낼 자료라면 기성 정장 같은 공식 스킬이 무난합니다. 국내 공문, 정부 지원사업 신청서, 사내 보고서라면 한국 재단사가 맞춘 `moai-office` 스킬이 서식과 글꼴에서 훨씬 자연스럽습니다. 이 원리는 아래 Word뿐 아니라 PPT·Excel·한글 섹션에서도 그대로 적용됩니다. 두 스킬은 경쟁이 아니라 제출처가 다른 정장이라고 생각하면 됩니다.

```mermaid
flowchart TD
    Task["문서 제출처가 어디인가"]
    Task -->|해외 · 글로벌 고객| O["1순위 — anthropic-skills<br/>(기성 정장 · 호환성 우선)"]
    Task -->|국내 공문 · 정부 양식 · 사내| M["2순위 — moai-office<br/>(한국 서식 · 글꼴 최적화)"]
    O --> R["해당 포맷 산출물"]
    M --> R

    style Task fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style O fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style M fill:#e6f0ef,stroke:#144a46,color:#09110f
    style R fill:#eaeaea,stroke:#6e6e6e,color:#09110f
```

### 추천 스킬

1순위 — `anthropic-skills:docx` (Anthropic 공식)
2순위 — `moai-office:docx-generator` (한국 양식 최적화)

### 실무 흐름

{{< terminal title="claude — cowork (예시 지시)" >}}
> D:/Input/Q2-sales-raw.xlsx를 분석해서
> Q2 매출 보고서를 Word로 작성해줘.
>
> - 상단 임원 요약 (3줄)
> - 제품별 섹션 (5개 제품)
> - 각 섹션에 전년 동기 대비 그래프 삽입
> - 부록: 원본 데이터 테이블
> - 저장 경로: 90_Output/Q2-sales-report.docx
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

{{< terminal title="claude — cowork (예시)" >}}
> Q2 매출 데이터를 분석해서 임원 대상 PPT 7장을 만들어줘.
>
> - 1장: 타이틀 + 요약 수치 3개
> - 2장: 전년 동기 비교 (막대 그래프)
> - 3-5장: 제품군 A / B / C 섹션
> - 6장: 리스크·이슈
> - 7장: 다음 분기 전망 + 제언
> - 테마: 화이트 배경, 포인트 컬러 코랄
> - 저장: 90_Output/Q2-review.pptx
{{< /terminal >}}

### 자주 걸리는 지점

**이미지가 들어가지 않음.** PPT 스킬은 이미지를 별도로 지정해야 삽입합니다. `moai-media:higgsfield-image`로 먼저 이미지를 만들고 경로를 전달하세요.

**슬라이드 수가 폭주.** "5-7장"이라고 상한을 지정하지 않으면 15장 이상으로 부풀어 오릅니다.

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

{{< terminal title="claude — cowork (예시)" >}}
> D:/Input/raw-transactions.csv(5만건)를 분석해서
> 월별·카테고리별 피벗을 만들어줘.
>
> - 시트 1: 원본 데이터 (필터만 적용)
> - 시트 2: 월별 합계 피벗 + 스파크라인
> - 시트 3: 카테고리별 Top 10
> - 시트 4: 조건부 서식 (상위 10% 녹색, 하위 10% 빨강)
> - 저장: 90_Output/finance-pivot.xlsx
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

{{< terminal title="claude — cowork (예시)" >}}
> 중소기업청 지원사업 신청서 초안을 한글 문서로 만들어줘.
>
> - 양식: 2026년 디지털 전환 지원사업 공식 양식
> - 1페이지: 기업 개요 (사업자등록번호·주소·대표자)
> - 2-3페이지: 사업 계획 (추진 배경·목표·예산)
> - 4페이지: 기대 효과 (정량·정성 지표)
> - 저장: 90_Output/grant-application.hwpx
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

{{< terminal title="claude — cowork (예시)" >}}
> D:/Contracts/에 있는 40페이지짜리 계약서 PDF를
> 열어서 다음 작업을 해줘:
>
> 1. 모든 텍스트 추출 (OCR 필요 시 수행)
> 2. "책임 제한·지체상금·해지 조건" 조항 하이라이트
> 3. 리스크 조항 요약을 별도 Word 보고서로 생성
> 4. 원본 PDF + 요약 Word를 묶어서
>    90_Output/contract-review-YYYY-MM-DD.zip으로 압축
{{< /terminal >}}

### 자주 걸리는 지점

**스캔 PDF OCR 정확도.** 저해상도 스캔은 오인식이 많습니다. 300dpi 이상 권장.

**폼 필드가 자동 채워지지 않음.** 일부 PDF는 필드가 이미지로 렌더링되어 있어 자동 입력 불가. 이런 경우는 [PDF Tools MCP](https://github.com/modelcontextprotocol/servers)의 `bulk_fill_from_csv`로 우회하세요.

## 왜 품질 검수는 텍스트 산출물에만 붙는가

앞선 흐름도를 보면 Word·PPT·한글은 `ai-slop-reviewer` 검수 노드를 거치지만, Excel과 PDF는 건너뜁니다. 종합 체크리스트도 "텍스트만 검수"라고 적혀 있습니다. 이유가 있습니다. `ai-slop-reviewer`는 교정 교사처럼 "문장의 어투와 표현"만 점검합니다. 사람이 쓴 것처럼 자연스러운지, AI 특유의 딱딱한 말투(예컨대 "~입니다~합니다" 반복, 과도한 존댓말, 기계적인 접속사)는 없는지 살핍니다. 그래서 문장이 중심인 보고서·제안서, 발표 자료, 공문에만 필요합니다.

반면 숫자 덩어리인 재무모델(Excel)이나 편집 불가 최종 배포본(PDF)에는 어투가 없습니다. 산술 문제지에 맞춤법 검사를 돌릴 필요가 없는 것과 같습니다. 이 원리를 모르면 Excel까지 검수를 걸어 시간을 낭비하거나, 반대로 Word 검수를 빼먹어 AI 특유의 기계적 글이 그대로 배포됩니다. 검수가 붙는 포맷과 빠지는 포맷을 구분하는 기준은 "이 산출물에 문장이 중심인가, 아니면 숫자·배포가 중심인가" 한 가지입니다.

```mermaid
flowchart TD
    Made["포맷별 산출물 완성"]
    Made --> Kind{"문장이 중심인가"}
    Kind -->|"예 — Word·PPT·한글"| Rev["ai-slop-reviewer 검수<br/>(어투 · 표현 다듬기)"]
    Kind -->|"아니요 — Excel·PDF"| Skip["검수 생략<br/>(어투 검사할 게 없음)"]
    Rev --> Final["최종 산출물"]
    Skip --> Final

    style Made fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style Kind fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style Rev fill:#e6f0ef,stroke:#144a46,color:#09110f
    style Skip fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style Final fill:#eaeaea,stroke:#6e6e6e,color:#09110f
```

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
