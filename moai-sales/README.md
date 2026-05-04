# moai-sales

> 한국 B2B 영업 워크플로우 자동화 — 제안서·견적서·콜드메일·후속 시퀀스

[![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

한국 B2B SaaS·중소기업 영업 환경에 특화된 cowork 플러그인입니다. 국세청 표준 양식·한국 비즈니스 관행(격식체, 결재선, VAT 명시)을 기본값으로 반영합니다.

## 스킬 카탈로그 (v2.0.0 기준)

| 스킬 | 설명 | 첫 출시 |
|---|---|---|
| [proposal-writer](./skills/proposal-writer/SKILL.md) | 한국 B2B 제안서 본문 자동 생성 (12섹션 + Three C's) | ✅ v2.0.0 |

## 시작하기

```bash
/plugin marketplace update cowork-plugins
```

설치 후:
```
B2B 영업 제안서 만들어줘
→ proposal-writer 호출

[ABC물류 RFP 답변 초안 만들어줘]
→ proposal-writer 가 12섹션 본문 + 컴플라이언스 체크리스트 생성
```

## 주요 워크플로우 체인

```
B2B 영업 제안서 (PDF)
  market-analyst → proposal-writer → ai-slop-reviewer → docx-generator

B2B 영업 슬라이드
  market-analyst → proposal-writer → ai-slop-reviewer → pptx-designer

견적서 분리 발행
  proposal-writer → quote-generator → xlsx-creator
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 정부 지원사업 신청서 | `moai-business/kr-gov-grant` |
| 투자자 IR 자료 | `moai-business/investor-relations` |
| 사업계획서 (전사 전략) | `moai-business/strategy-planner` |
| 마케팅 다회차 메일 | `moai-marketing/email-sequence` |

## 한국 시장 컴플라이언스

- **국세청 전자세금계산서**: 모든 가격 섹션에 VAT 별도/포함 명시 강제
- **NDA 처리**: 고객사 비밀 정보 포함 시 `moai-legal/nda-triage` 체이닝 권고
- **AI Slop 후처리**: 모든 텍스트 산출물 마지막 단계에 `moai-core/ai-slop-reviewer` 강제 (CLAUDE.local.md §3-2)

## 출처 및 베스트 프랙티스

- [HubSpot RFP Agent (Breeze)](https://knowledge.hubspot.com/ai-tools/set-up-and-use-the-request-for-proposal-rfp-agent)
- [Inventive AI — Top 15 RFP Software 2026](https://www.inventive.ai/blog-posts/top-rfp-software-use)
- [GPTfy — Salesforce RFP AI 5-Phase](https://gptfy.ai/blog/improve-rfp-in-salesforce-with-ai)
- [국세청 전자세금계산서](https://www.nts.go.kr/nts/cm/cntnts/cntntsView.do?mi=2460&cntntsId=7786)
- [Mordor Intelligence — 한국 B2B SaaS 2026-2031](https://www.mordorintelligence.kr/industry-reports/b2b-saas-market)

## 라이선스

MIT
