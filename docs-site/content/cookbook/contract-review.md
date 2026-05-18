---
title: "계약서 검토 리포트"
weight: 110
description: "상대측 계약서·NDA를 리스크 항목별로 표 정리 → 수정본 DOCX → 결재용 1페이지 요약까지."
geekdocBreadcrumb: true
tags: [cookbook, legal]
---
> **목표** — 상대측이 보낸 계약서·NDA를 **리스크 항목별로 표 정리** → 수정본 DOCX → 1페이지 결재용 요약까지 자동으로 만듭니다.

```mermaid
flowchart TD
    subgraph Fast["NDA 빠른 검토"]
        N["nda-triage"] --> D1["docx-generator"]
    end
    subgraph Full["일반 계약서 검토"]
        A["contract-review<br/>조항 분석"] --> B["legal-risk<br/>리스크 매트릭스"]
        B --> C["docx-generator<br/>수정본 DOCX"]
    end
    D1 --> R["ai-slop-reviewer"]
    C --> R
    R --> S["결재용 요약"]

    style Fast fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style Full fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style S fill:#e6f0ef,stroke:#144a46,color:#09110f
```

{{< hint type="danger" >}}
**법률 자문의 최종 결정은 반드시 변호사가 해야 합니다.** 이 파이프라인은 초안·1차 스크리닝·협상 포인트 정리용입니다. [Cowork 안전 사용](../../cowork/safety/) 참고.
{{< /hint >}}

## 대상 독자

계약서·NDA 1차 리뷰가 자주 필요한 사업개발·법무 담당자, 스타트업 대표.

## 사전 준비

- 플러그인: `moai-legal`, `moai-office`, `moai-core:ai-slop-reviewer`
- (선택) `korean-law` MCP — 조문·판례 레퍼런스 필요 시
- 입력: 계약서 원문 (PDF / DOCX / HWPX), **계약 유형**, **내 포지션**(을·발주·라이선시 등)

## 스킬 체인

```
contract-review → legal-risk → docx-generator → ai-slop-reviewer
```

(NDA 빠른 검토만 필요하면: `nda-triage → docx-generator → ai-slop-reviewer`)

## 사용 방식 — 한 줄 요청

> **사용자가 직접 스킬을 순서대로 호출하지 않습니다.** 짧은 한 줄을 입력하면 시스템이 AskUserQuestion으로 필요 정보를 묻고, 자동 체이닝으로 끝까지 처리합니다. ([4가지 사용 패턴](../../cowork/patterns/) 참조)

### 사용자 입력

{{< terminal title="claude — cowork" >}}
> 첨부 계약서 검토해서 위험도 + 1페이지 결재용 요약 만들어줘
{{< /terminal >}}

### 시스템 인터뷰 (AskUserQuestion)

1. **계약서 첨부 위치** (PDF/HWPX/DOCX)
2. **내 포지션**: 갑 (위탁자) / 을 (수탁자) / 양자
3. **관심사 우선순위**: 손해배상 상한 / 지재권 귀속 / 해지 조항 / 준거법·관할 / 기타
4. **출력 형식**: 리스크 표 / 매트릭스 / 수정안 DOCX / 1페이지 결재 요약 / 전부
5. **검토자 향후 사용**: 변호사 자문 전 1차 / 사내 결재용 / 협상용

### 자동 체인

```mermaid
flowchart TD
    A["원문 PDF/HWPX"] --> B["nda-triage<br/>(NDA인 경우)"]
    B --> C["contract-review<br/>조항별 리스크"]
    C --> D["legal-risk<br/>발생가능성·영향도 매트릭스"]
    D --> E["compliance-check<br/>규제 검증"]
    E --> F["docx-generator<br/>수정안 + 1페이지 요약"]
    F --> G["ai-slop-reviewer<br/>어투 정리"]
    style F fill:#fbf0dc,stroke:#c47b2a
```

### 산출물

- **리스크 표**: 조항 번호 · 요약 · 리스크 · 우리측 대응 (자동)
- **2×2 영향도 매트릭스**: 발생가능성 × 영향도. 상위 3개 협상 포인트 자동 표시
- **수정본 DOCX**: 원문 인용 + 수정안 + 근거 (조문·판례), 추적 변경 형식 표
- **1페이지 결재 요약**: 핵심 리스크 3개 + 권장 액션 + 승인 필요 사항
- **자동 면책 문구**: "본 보고서는 1차 검토 가이드이며 최종 법률자문은 변호사 검토를 거쳐야 합니다"

### 변형 시나리오 — 한 줄로 다양하게

| 한 줄 요청 | 자동 체인 분기 |
|---|---|
| "이 NDA 위험도만 알려줘" | nda-triage → legal-risk (요약만) |
| "조항별 표만 만들어줘" | contract-review → docx-generator |
| "협상용 수정안만 필요해" | contract-review → 수정안 DOCX |
| "경영진 결재용 1페이지" | 1페이지 요약만 |

## 자주 겪는 이슈

{{< hint type="warning" >}}
**이슈 1 — HWPX 원본이 깨짐.**
한글 파일은 `hwpx-writer`로 변환한 뒤 `contract-review`에 입력합니다. 표·각주가 있는 계약서는 특히 중요합니다.
{{< /hint >}}

{{< hint type="warning" >}}
**이슈 2 — 조항 번호가 틀리게 인용된다.**
스캔 PDF는 OCR 오류가 많습니다. 번호 인용은 최종 검토자가 반드시 크로스체크하세요.
{{< /hint >}}

{{< hint type="note" >}}
**이슈 3 — 판례 레퍼런스가 허구.**
`legal-risk`가 가상 판례를 만드는 경우가 있습니다. 국가법령정보센터에서 실제 존재하는지 확인하거나 `korean-law` MCP를 연결하세요.
{{< /hint >}}

## 응용 변형

- **대량 표준계약서 심사** — 같은 포맷 계약서가 월 수십 건이라면 슬래시 명령으로 묶어 `/contract-review` 하나로 실행합니다.
- **이력 관리** — 수정본마다 `xlsx-creator`로 차수별 변경점 표를 누적합니다.

---

### Sources
- [modu-ai/cowork-plugins › moai-legal](https://github.com/modu-ai/cowork-plugins)
- [국가법령정보센터](https://law.go.kr)
