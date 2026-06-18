# moai-bi

> 경영진용 1-pager 핵심 요약(executive summary) 작성 — K-IFRS·KOSIS·DART 한국 통계 친화

[![Version](https://img.shields.io/badge/Version-2.10.0-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

K-IFRS·KOSIS·DART 친화적 한국 통계 환경에서 경영진이 5분 안에 의사결정할 수 있는 1페이지 핵심 요약을 만듭니다. 산출물은 다른 플러그인의 변환 스킬로 체이닝합니다 — 단일 HTML은 `moai-content:html-report`로, 결재·이사회·공공기관 제출용은 `moai-office:*` 변환 스킬로 분기합니다.

> **설계 노트**: 코디네이터 에이전트(agent) 없이 스킬 직접 호출 전용 플러그인입니다 — 단일 목적 유틸리티로 `/executive-summary` 또는 자연어로 바로 사용하세요. 코디네이터 부재는 미완이 아니라 의도적 설계입니다.

## 스킬 카탈로그

| 스킬 | 설명 | 후속 체인 |
|---|---|---|
| [executive-summary](./skills/executive-summary/SKILL.md) | C-level 1pager (≤500단어, What/So What/Now What) | `moai-content:html-report` / `moai-office:*` |

## 산출물 변환 (다른 플러그인 체이닝)

executive-summary는 1pager 마크다운을 생성하고, 최종 산출물 포맷은 아래 변환 스킬로 체이닝합니다.

| 출력 | 사용처 | 변환 체인 |
|---|---|---|
| HTML 단일 파일 | 카톡 공유·이메일 첨부·오프라인 열람 | `executive-summary → moai-content:html-report` |
| PDF | 결재·인쇄·서명 | `... → moai-content:html-report → moai-office:pdf-writer` |
| DOCX | 편집·수정·재배포 | `... → moai-content:html-report → moai-office:docx-generator` |
| PPTX | 이사회 슬라이드 1매 | `... → moai-content:html-report → moai-office:pptx-designer` |
| HWPX | 한국 공공기관 제출 | `... → moai-content:html-report → moai-office:hwpx-writer` |

## 시작하기

```bash
/plugin marketplace update cowork-plugins
```

```
이 분기 변동분석 보고서를 임원 1pager 만들어서 카톡으로 보낼 수 있게 해줘.
→ executive-summary 가 ≤500단어 1pager 마크다운 생성
→ moai-content:html-report 로 단일 HTML 렌더링 → 1개 .html 파일
```

## 대표 워크플로우 체인

```
재무 → 카톡 공유
  moai-finance:variance-analysis → executive-summary → moai-core:ai-slop-reviewer → moai-content:html-report

재무 → 이사회 슬라이드
  moai-finance:variance-analysis → executive-summary → moai-content:html-report → moai-office:pptx-designer

재무 → 결재용 PDF
  moai-finance:variance-analysis → executive-summary → moai-content:html-report → moai-office:pdf-writer

주간 → C-level HTML
  moai-pm:weekly-report → executive-summary → moai-content:html-report

주간 → 공공기관 hwpx
  moai-pm:weekly-report → executive-summary → moai-content:html-report → moai-office:hwpx-writer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 팀 단위 주간 (6섹션 상세) | `moai-pm:weekly-report` |
| 전략 본문 (요약 아닌 상세) | `moai-business:strategy-planner` |
| 재무 분석 (변동·예측) | `moai-finance:variance-analysis` |
| 단일 HTML 렌더링 (범용) | `moai-content:html-report` |

## 한국 BI 환경 친화

- K-IFRS 재무 지표 우선 표기 (영업이익률·EBITDA·CAGR)
- KOSIS·한국은행 ECOS·DART 인용 가능
- 격식체 보고 ("~로 판단됩니다", "~를 권고드립니다")

## 라이선스

MIT
