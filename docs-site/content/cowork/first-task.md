---
title: "첫 작업 실행하기"
weight: 30
description: "데스크톱 폴더의 CSV를 요약해 Word 파일로 저장하는 5분 시나리오로 Cowork 사용법을 익힙니다."
geekdocBreadcrumb: true
---
> 설치를 마쳤다면 5분 안에 첫 결과물을 만들어 봅니다. 이번 예시는 데스크톱 폴더의 CSV를 간단히 요약해 Word 파일로 저장하는 흐름입니다.

## 준비물

- Claude Desktop 앱 + Cowork 모드 진입 완료
- 요약하고 싶은 CSV·Excel·TXT 파일 1개. 샘플이 없다면 Cowork에 `테스트용 sales.csv 하나 만들어줘 — 2026년 1~6월 월별 매출·상위 5개 제품`이라고 먼저 요청해서 생성하세요.
- 작업 전용으로 사용할 짧은 경로의 로컬 폴더

## 작업 흐름

```mermaid
flowchart LR
    A["① 폴더 선택"] --> B["② 요청 입력"]
    B --> C["③ 파일 분석·집계"]
    C --> D["④ 초안 작성"]
    D --> E["⑤ DOCX 저장"]
    E --> F["⑥ 결과 확인·후속"]

    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style F fill:#e6f0ef,stroke:#144a46,color:#09110f
```

## 단계별 진행

1. **작업 폴더 선택** — 우측 상단의 "폴더 선택"을 눌러 파일이 들어 있는 폴더를 지정합니다. Cowork는 선택된 폴더의 파일만 읽고 쓸 수 있습니다.
2. **요청 입력** — 대화 창에 한 문장으로 요청을 씁니다. **본 문서의 모든 사용자 입력은 `> ` prefix와 함께 표기**합니다(실제 입력 시 `>` 제외 — [표기 규약](../skills/#스킬-호출-방식)).

   {{< terminal title="claude — cowork" >}}
> "sales.csv 파일을 요약해서 한 페이지 분량의 Word 보고서로 저장해줘. 월별 매출 추이와 상위 3개 제품을 표로 정리하고, 마지막에 제안 2가지를 추가해."
   {{< /terminal >}}

3. **Cowork의 실행 과정 관찰**
   - 파일을 읽고 구조를 파악합니다.
   - 필요하면 Python 코드로 집계를 수행합니다.
   - 본문 초안을 작성합니다.
   - 초안을 DOCX로 저장하고, 파일 링크를 대화창에 내어줍니다.

4. **결과 확인** — Cowork가 대화창에 돌려주는 `computer://...` 링크를 클릭하면 저장된 Word 파일이 열립니다. `computer://`는 Cowork가 로컬 파일 경로를 대화창에서 바로 열 수 있도록 사용하는 링크 프로토콜이며, 폴더 탐색기에서 직접 열어도 같은 파일입니다.
5. **후속 요청** — "표 디자인을 더 세련되게 바꿔줘", "상위 5개로 늘려서 다시 저장해줘" 같은 자연스러운 후속 요청으로 반복 작업을 이어갈 수 있습니다.

## 자주 겪는 이슈

- **파일을 못 찾습니다**: 폴더를 다시 선택하거나, 파일명이 한글·특수문자로 길지 않은지 확인합니다.
- **결과물이 열리지 않습니다 (Windows)**: 경로가 260자를 초과할 수 있습니다. 작업 폴더를 `C:\w\` 같은 짧은 경로로 옮겨봅니다.
- **결과가 너무 길거나 부정확합니다**: "한 페이지로 줄여줘", "숫자만 정확히 뽑아줘"처럼 제약 조건을 명시하면 품질이 올라갑니다.

## 더 효율적으로 쓰려면

- 반복되는 요청은 [프로젝트와 메모리](../projects-memory/)에 맥락을 고정합니다.
- 정형화된 절차는 [스킬 사용법](../skills/)으로 묶어둡니다.
- 한국어 실무 양식·톤이 필요하면 [플러그인 카탈로그](../../plugins/)에서 `cowork-plugins`를 설치합니다.

## 다음 단계

- [프로젝트와 메모리](../projects-memory/)
- [플러그인 사용](../plugins/)
- [쿡북 — 스킬 체인 설계](../../cookbook/skill-chaining/)

---

### Sources

- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190)
- [Organize your tasks with projects in Claude Cowork](https://support.claude.com/en/articles/14116274)
