# moai-bi

> 비즈니스 인텔리전스·리포트 풀스택 — **기본 출력은 단일 HTML 파일**(이미지·CSS·JS 인라인, 카톡 즉시 공유 가능)

[![Version](https://img.shields.io/badge/Version-2.10.0-blue.svg)]() [![Skills](https://img.shields.io/badge/Skills-1-green.svg)]() [![License](https://img.shields.io/badge/License-MIT-orange.svg)]()

K-IFRS·KOSIS·DART 친화적 한국 통계 환경에서 경영진이 5분 안에 의사결정할 수 있는 1페이지 보고를 만듭니다. **기본 출력은 `moai-content:html-report`로 단일 HTML 파일** — 카톡·이메일에 그대로 첨부해 즉시 공유합니다. 결재·이사회·공공기관 제출용은 pdf/docx/pptx/hwpx로 변환 분기합니다.

## 핵심 컨셉: 단일 HTML = 카톡 즉시 확인

| 출력 | 사용처 | 변환 체인 |
|---|---|---|
| **HTML 단일 파일** (기본) | 카톡 공유·이메일 첨부·오프라인 열람 | `executive-summary → html-report` |
| PDF | 결재·인쇄·서명 | `... → html-report → pdf-writer` |
| DOCX | 편집·수정·재배포 | `... → html-report → docx-generator` |
| PPTX | 이사회 슬라이드 1매 | `... → html-report → pptx-designer` |
| HWPX | 한국 공공기관 제출 | `... → html-report → hwpx-writer` |

**왜 단일 HTML인가**: 이미지(base64/SVG)·CSS(`<style>`)·JS(`<script>`)를 전부 인라인해 외부 의존성 0. 한국어 폰트 CDN 단일 예외만 허용. 파일 1개로 모든 디바이스에서 동일 렌더링.

## 스킬 카탈로그 (v2.10.0 기준)

| 스킬 | 설명 | 기본 출력 |
|---|---|---|
| [executive-summary](./skills/executive-summary/SKILL.md) | C-level 1pager (≤500단어, What/So What/Now What) | html-report (mode=status) 단일 HTML |

## 시작하기

```bash
/plugin marketplace update cowork-plugins
```

```
이 분기 변동분석 보고서를 임원 1pager 만들어서 카톡으로 보낼 수 있게 해줘.
→ executive-summary 가 ≤500단어 1pager 마크다운 생성
→ html-report (mode=status)로 단일 HTML 렌더링 → 1개 .html 파일
```

## 대표 워크플로우 체인

```
재무 → 카톡 공유 (기본)
  variance-analysis → executive-summary → ai-slop-reviewer → html-report (mode=status)

재무 → 이사회 슬라이드
  variance-analysis → executive-summary → html-report → pptx-designer

재무 → 결재용 PDF
  variance-analysis → executive-summary → html-report → pdf-writer

주간 → C-level HTML
  weekly-report → executive-summary → html-report (mode=status)

주간 → 공공기관 hwpx
  weekly-report → executive-summary → html-report → hwpx-writer
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 팀 단위 주간 (6섹션 상세) | `moai-pm/weekly-report` |
| 전략 본문 (요약 아닌 상세) | `moai-business/strategy-planner` |
| 재무 분석 (변동·예측) | `moai-finance/variance-analysis` |
| 단일 HTML 렌더링 (범용) | `moai-content/html-report` (본 플러그인이 기본 사용) |

## 한국 BI 환경 친화

- K-IFRS 재무 지표 우선 표기 (영업이익률·EBITDA·CAGR)
- KOSIS·한국은행 ECOS·DART 인용 가능
- 격식체 보고 ("~로 판단됩니다", "~를 권고드립니다")
- 한국어 가독성 폰트(Pretendard) 인라인 적용

## 라이선스

MIT
