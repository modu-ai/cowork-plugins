---
title: "moai-legal — 계약·NDA·컴플라이언스"
weight: 120
description: "대한민국 민법·상법 기준의 계약서 검토·NDA·컴플라이언스·법적 리스크 4개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-legal"]
---

# moai-legal

> 법무 실무를 위한 4개 스킬을 제공합니다. 대한민국 민법·상법 기준으로 설계됐습니다.

## 무엇을 하는 플러그인인가

`moai-legal` (v1.5.0)는 계약서·이용약관·개인정보처리방침·SLA 리스크 분석, NDA 빠른 검토, 규제 준수·내부 감사·ESG 보고, 기업 법적 리스크 매트릭스 및 IP 포트폴리오 분석까지 법무팀의 1차 스크리닝을 자동화합니다. korean-law MCP와 연동하면 국가법령정보센터·판례 검색을 체인에 포함시킬 수 있습니다.

## 설치

{{< tabs "install-legal" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-legal` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-legal)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 |
|---|---|
| `contract-review` | 계약서·이용약관·개인정보처리방침·SLA 10대 리스크 분석 |
| `nda-triage` | 비밀유지계약(NDA) 빠른 검토·위험 조항 식별 |
| `compliance-check` | 규제 준수 점검, 내부 감사, ESG 보고 |
| `legal-risk` | 기업 법적 리스크 매트릭스, IP 포트폴리오 분석 |

## 선택 연동

- **korean-law MCP** — 국가법령정보센터, 판례 검색
- `moai-office` — 최종 DOCX·HWPX 저장

## 대표 체인

**NDA 빠른 검토**

```text
nda-triage → docx-generator(수정본) → ai-slop-reviewer
```

**계약서 정식 리뷰**

```text
contract-review → legal-risk(영향도 평가) → docx-generator
```

**분기 컴플라이언스 감사**

```text
compliance-check → docx-generator(보고서)
```

## 주의

{{< hint type="warning" >}}
법률 자문의 **최종 결정**은 반드시 변호사가 검토해야 합니다. 이 플러그인은 초안 작성·리스크 1차 스크리닝용입니다. [Cowork 안전 사용](../../cowork/safety/)을 참고하세요.
{{< /hint >}}

## 빠른 사용 예

```text
상대측에서 보낸 NDA 검토해줘. 우리에게 불리한 조항 위주로.
```

```text
개인정보처리방침을 2026년 기준으로 업데이트해줘.
```

## 다음 단계

- [`moai-finance`](../moai-finance/) — 재무·세무 결합
- [Cowork 커넥터와 MCP](../../cowork/connectors-mcp/) — korean-law MCP 설정

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [moai-legal 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-legal)
