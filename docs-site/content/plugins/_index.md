---
title: "플러그인 카탈로그"
weight: 1
description: "modu-ai/cowork-plugins 마켓플레이스의 17개 플러그인·73개 스킬을 도메인별로 정리한 카탈로그입니다."
geekdocBreadcrumb: true
geekdocCollapseSection: false
---

# `cowork-plugins` 카탈로그

[`modu-ai/cowork-plugins`](https://github.com/modu-ai/cowork-plugins)는 한국 업무 환경에 맞춰 설계된 **17개 플러그인 · 73개 스킬**의 커뮤니티 마켓플레이스입니다. 사업계획·IR·마케팅·법무·세무·HR·카드뉴스·PPT·이미지 생성 등 도메인별로 묶여 있습니다.

{{< hint type="note" >}}
**v1.5.0 업데이트 (2026-04-21)**: `moai-business`에 **소상공인365 상권분석(`sbiz365-analyst`)** 과 **정부지원사업 통합(`kr-gov-grant`)** 스킬 2종이 추가되었습니다. 자세한 내용은 [`moai-business`](./moai-business/) 페이지를 확인하세요.
{{< /hint >}}

## 전제 조건

- Claude Desktop 앱 + Cowork 모드 진입 완료 → [Cowork 설치](../../cowork/install/)
- 마켓플레이스 설치 절차는 [빠른 시작](./quick-start/) 참고
- **`moai-core`는 가장 먼저 설치**해야 합니다 — `/project init` 마법사와 `ai-slop-reviewer`가 여기에 들어 있습니다

## 도메인별 플러그인

### 코어

- [`moai-core`](./moai-core/) — 프로젝트 초기화, 자연어 라우터, AI 슬롭 검수, 피드백 허브

### 콘텐츠·오피스·미디어

- [`moai-content`](./moai-content/) — 블로그·카드뉴스·랜딩·뉴스레터·상세페이지·SNS 콘텐츠
- [`moai-office`](./moai-office/) — PPTX·DOCX·XLSX·HWPX 문서 자동 생성
- [`moai-media`](./moai-media/) — 이미지(나노바나나·Ideogram), 영상(Kling), 음성(ElevenLabs)

### 경영·전략·제품

- [`moai-business`](./moai-business/) — 사업계획서, IR 덱, 시장조사, 일간 브리핑, 상권분석, 정부지원사업
- [`moai-marketing`](./moai-marketing/) — 브랜드 아이덴티티, SEO, SNS 캠페인, 퍼포먼스 리포트
- [`moai-product`](./moai-product/) — PRD·기능 명세, 로드맵, UX 리서치

### 운영·지원·HR

- [`moai-operations`](./moai-operations/) — SOP, 조달, 벤더 평가, 주간 상태 보고
- [`moai-support`](./moai-support/) — 고객 티켓 분류·응답, 지식베이스, 에스컬레이션
- [`moai-hr`](./moai-hr/) — 채용, 근로계약, 평가, 원격 근무 정책

### 법무·재무

- [`moai-legal`](./moai-legal/) — 계약서 검토, NDA, 컴플라이언스, IP 리스크
- [`moai-finance`](./moai-finance/) — 세무, 결산, K-IFRS 재무제표, 예실 분석

### 데이터·연구·교육

- [`moai-data`](./moai-data/) — CSV 탐색, 공공데이터, 데이터 시각화
- [`moai-research`](./moai-research/) — 논문, 특허(KIPRIS), 연구비 신청
- [`moai-education`](./moai-education/) — 커리큘럼, 리서치 보조, 시험 출제

### 커리어·라이프

- [`moai-career`](./moai-career/) — 자기소개서, 이력서, 면접 코칭, 포트폴리오
- [`moai-lifestyle`](./moai-lifestyle/) — 여행, 웰니스, 이벤트·웨딩 기획

## 한 눈에 보는 스킬 수 (v1.5.0)

"대표 스킬 (일부)"는 각 플러그인에서 가장 자주 호출되는 스킬을 발췌한 것입니다. 전체 스킬 목록은 플러그인 이름을 클릭해 상세 페이지에서 확인하세요.

| 플러그인 | 스킬 수 | 대표 스킬 (일부) |
|---|---|---|
| [moai-core](./moai-core/) | 3 | project, ai-slop-reviewer, feedback |
| [moai-content](./moai-content/) | 8 | blog, card-news, landing-page, copywriting +4종 |
| [moai-office](./moai-office/) | 4 | pptx-designer, docx-generator, xlsx-creator, hwpx-writer |
| [moai-media](./moai-media/) | 5 | nano-banana, ideogram, kling, elevenlabs, fal-gateway |
| [moai-business](./moai-business/) | 6 | strategy-planner, market-analyst, investor-relations, sbiz365-analyst, kr-gov-grant +1종 |
| [moai-marketing](./moai-marketing/) | 7 | brand-identity, seo-audit, campaign-planner, sns-content +3종 |
| [moai-product](./moai-product/) | 3 | spec-writer +2종 |
| [moai-operations](./moai-operations/) | 3 | status-reporter +2종 |
| [moai-support](./moai-support/) | 4 | ticket-triage +3종 |
| [moai-hr](./moai-hr/) | 4 | recruiter +3종 |
| [moai-legal](./moai-legal/) | 4 | contract-review, nda-triage, compliance-check, legal-risk |
| [moai-finance](./moai-finance/) | 4 | tax-helper, financial-statements, close-management, variance-analysis |
| [moai-data](./moai-data/) | 3 | data-explorer +2종 |
| [moai-research](./moai-research/) | 5 | paper-search, paper-writer, grant-writer +2종 |
| [moai-education](./moai-education/) | 3 | curriculum-designer +2종 |
| [moai-career](./moai-career/) | 4 | job-analyzer, interview-coach +2종 |
| [moai-lifestyle](./moai-lifestyle/) | 3 | travel-planner +2종 |

전체 **73개** 스킬 (v1.5.0 기준, `moai-business`에 2개 신규 추가).

## 다음 단계

- [빠른 시작](./quick-start/) — 마켓플레이스 추가 → 플러그인 설치 → 첫 체인
- [`moai-core`](./moai-core/) — 반드시 가장 먼저 설치
- [Cowork 플러그인 사용](../../cowork/plugins/) — Cowork 환경 통합 가이드

---

### Sources

- [modu-ai/cowork-plugins](https://github.com/modu-ai/cowork-plugins)
- [cowork-plugins README](https://raw.githubusercontent.com/modu-ai/cowork-plugins/main/README.md)
