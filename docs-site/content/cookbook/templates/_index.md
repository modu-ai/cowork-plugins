---
title: "템플릿 모음"
weight: 85
description: "재무 모델·이메일·엑셀·컴플라이언스 등 즉시 복사해 변형할 수 있는 실무 템플릿."
geekdocBreadcrumb: true
geekdocCollapseSection: true
---
복사 → 변형 → 즉시 활용. 각 템플릿은 관련 cowork-plugins 스킬과 함께 동작하도록 설계되어 있습니다.

```mermaid
flowchart LR
    A["템플릿 선택"] --> B["프롬프트로<br/>파라미터 입력"]
    B --> C["스킬 체인<br/>실행"]
    C --> D["ai-slop-reviewer<br/>검수"]
    D --> E["최종 산출물"]

    style A fill:#e6f0ff,stroke:#3070d0
    style E fill:#dff5dd,stroke:#3a8a3a,stroke-width:2px
```

## 템플릿 목록

- [컴플라이언스 체크리스트](./compliance/) — `moai-legal:compliance-check`
- [재무 모델링 템플릿](./financial/) — `moai-finance:financial-statements` + `moai-office:xlsx-creator`
- [엑셀 고급 기법](./excel/) — `moai-office:xlsx-creator`
- [이메일 마케팅 템플릿](./email/) — `moai-content:newsletter` + `moai-marketing:email-sequence`
