---
name: html-report
description: |
  마크다운 보고서를 단일 파일·자체 완결형 HTML로 렌더링하는 터미널 스킬입니다.
  Thariq Shihipar의 "unreasonable effectiveness of HTML" 사상 기반 — 외부 JS·CSS 프레임워크
  의존성 0, 한국어 가독성을 위한 폰트 CDN 단일 예외 허용.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "보고서 HTML로", "주간 보고서 HTML 파일로 만들어줘", "단일 파일 HTML 렌더"
  - "status report html", "재무제표 HTML 출력", "보고서를 하나의 HTML 파일로"
  - "프린트 가능한 HTML 보고서", "이메일에 임베드할 HTML 리포트"
  - "현황 보고 HTML", "인시던트 리포트 HTML", "사업계획서 HTML"
  - "html-report mode=status", "html-report mode=financial", "html-report mode=plan"

user-invocable: true
version: 2.2.1
---

# html-report — 단일 파일 HTML 보고서 렌더러

## 목적과 범위

`moai-content:html-report`는 cowork 텍스트 산출 파이프라인의 **터미널 렌더러**입니다.
`moai-bi:executive-summary`, `moai-finance:financial-statements`, `moai-business:sbiz365-analyst` 등이 생성한 마크다운 보고서를 **단일 파일·자체 완결형(self-contained) HTML**로 변환합니다.

**핵심 원칙 (Thariq 사상)**:
- 외부 JS 라이브러리(Chart.js, D3, htmx) 0 의존
- 외부 CSS 프레임워크(Tailwind, Bootstrap) 0 의존
- 인라인 SVG로 차트 직접 렌더링
- 한국어 가독성을 위한 폰트 CDN 단일 예외 허용

**이 스킬은 마크다운 출력을 대체하지 않습니다.** 마크다운은 단일 진실(source of truth)로 유지되며, HTML 렌더링은 추가 분기로만 작동합니다.

---

## 입력

| 인자 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `markdown` | ✓ | — | 변환할 마크다운 본문 |
| `mode` | ✓ | — | `status` \| `incident` \| `plan` \| `explainer` \| `financial` \| `pr` |
| `slug` | — | 제목에서 자동 생성 | 출력 파일명 prefix |
| `output_path` | — | `<cwd>/reports/<slug>-<YYYYMMDD>.html` | 출력 경로 |
| `font_stack` | — | 모드별 기본값 | 폰트 매핑 오버라이드 |

---

## 출력

단일 `.html` 파일 (`<cwd>/reports/<slug>-<YYYYMMDD>.html`):
- 크기: ≤ 50KB (폰트 CDN 트래픽 제외, 본문 압축 전 기준)
- 외부 의존성: 폰트 CDN `<link>` 1건 + `preconnect` 2건 (한국어 폰트)
- 자체 완결형: 브라우저에서 바로 열기 가능, 이메일 첨부·오프라인 사용 가능

---

## 6개 모드

### 구현된 모드 (Wave 1 + Wave 2)

| 모드 | 구조 섹션 | 대상 스킬 |
|------|-----------|-----------|
| **`status`** | 메트릭 카드 4개 · 하이라이트 · 완료 테이블 · Velocity SVG 막대 차트 · Carryover | `moai-bi:executive-summary`, `moai-business:daily-briefing` |
| **`incident`** | TL;DR 다크 배너 · 타임라인 · 로그 발췌 `<details>` · 코드 diff 패널 · 영향 테이블 · 액션 체크리스트 | `moai-legal:compliance-check` |
| **`plan`** | 요약 KPI 스트립 · 마일스톤 수직 타임라인 · 데이터 플로우 SVG · 슬라이스 테이블 · 리스크 그리드 · 성공 지표 | `moai-business:sbiz365-analyst` |
| **`explainer`** | 사이드 네비 · `<details>` 접이식 단계 · 탭 코드 블록(vanilla JS) · FAQ 아코디언 · 콜아웃 박스 | `moai-research:*`, `moai-education:*` |
| **`financial`** | KPI 카드 4개 · 손익계산서 테이블(항목/당기/전기/증감/증감률) · Variance SVG 수평 막대 차트 · 주석 패널 | `moai-finance:financial-statements` |
| **`pr`** | TL;DR · PR 메타 행(파일수·+/−·브랜치) · Before/After 2단 카드 · 파일 투어 `<details>` · 핵심 포인트 · 테스트 체크리스트 · 롤아웃 단계 | `moai-business:investor-relations` |

#### 모드별 입력 슬롯 요약

| 모드 | 주요 Mustache 슬롯 |
|------|-------------------|
| `status` | `{{title}}`, `{{#metrics}}`, `{{#highlights}}`, `{{#completed_rows}}`, `{{#chart_bars}}` |
| `incident` | `{{inc_id}}`, `{{severity}}`, `{{title}}`, `{{#tl_entries}}`, `{{#impact_rows}}`, `{{#actions}}` |
| `plan` | `{{title}}`, `{{#kpis}}`, `{{#milestones}}`, `{{diagram_svg}}`, `{{#slices}}`, `{{#risks}}`, `{{#metrics}}` |
| `explainer` | `{{title}}`, `{{lead}}`, `{{#steps}}`, `{{#config_tabs}}`, `{{#faq_items}}` |
| `financial` | `{{title}}`, `{{period}}`, `{{#kpis}}`, `{{#statement_rows}}`, `{{chart_height}}`, `{{#variance_bars}}` |
| `pr` | `{{pr_ref}}`, `{{title}}`, `{{author}}`, `{{branch}}`, `{{files_changed}}`, `{{additions}}`, `{{deletions}}`, `{{#focus_items}}`, `{{#test_items}}`, `{{#rollout_steps}}` |

---

## 한국어 폰트 정책

본 스킬은 한국어 가독성을 위해 **단일 폰트 CDN `<link>`를 유일한 외부 의존성**으로 허용합니다.

시스템 폰트만 사용하면 OS별 폴백(macOS: Apple SD Gothic Neo, Windows: Malgun Gothic)으로 일관성이 깨지므로, 폰트 CDN은 필수입니다.

### 모드별 폰트 매핑

| 모드 | sans (본문) | serif (제목) | mono (코드) |
|------|-------------|--------------|-------------|
| `status` / `financial` / `pr` | Pretendard | Pretendard 700 | JetBrains Mono |
| `incident` | Pretendard | Pretendard 700 | JetBrains Mono |
| `plan` | Pretendard | Noto Serif KR | JetBrains Mono |
| `explainer` | Noto Sans KR | Noto Serif KR | JetBrains Mono |
| `editorial` | Pretendard | 조선일보명조 | JetBrains Mono |
| `legal` | KoPubWorld Batang | KoPubWorld Batang Bold | JetBrains Mono |

상세 CDN URL 및 preconnect 패턴: [`references/fonts.md`](references/fonts.md)

---

## 디자인 토큰 (CSS 변수 계약)

모든 모드는 `:root`에 동일한 CSS 변수 8개를 선언합니다.

```css
:root {
  /* 팔레트 */
  --ivory: #FAF9F5;   /* 배경 warm off-white */
  --paper: #FFFFFF;   /* 카드·패널 배경 */
  --slate: #141413;   /* 본문 텍스트 warm black */
  --clay:  #D97757;   /* 강조·링크 terracotta */
  --clay-d:#B85C3E;   /* clay hover 상태 */
  --oat:   #E3DACC;   /* 보조 배경·구분선 light tan */
  --olive: #788C5D;   /* 보조 강조 sage green */

  /* 폰트 */
  --sans:  "Pretendard", system-ui, -apple-system, sans-serif;
  --serif: "Pretendard", ui-serif, Georgia, serif;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", monospace;

  /* 레이아웃 */
  --max-width:    860px;
  --radius-panel: 12px;
  --radius-row:   8px;
  --border:       1.5px solid var(--g300);
}
```

그레이 스케일: `--g100: #F0EEE6`, `--g300: #D1CFC5`, `--g500: #87867F`, `--g700: #3D3D3A`

상세 명도 대비 검증표 및 인쇄 토큰: [`references/design-tokens.md`](references/design-tokens.md)

---

## 체인 통합 권장

```
[텍스트 스킬] → moai-core:ai-slop-reviewer → moai-content:humanize-korean → moai-content:html-report (mode=X)
```

최소 체인 (빠른 렌더링):
```
[텍스트 스킬] → moai-content:html-report (mode=X)
```

---

## 사용 예시

**예시 1: 주간 현황 보고서**
```
moai-bi:executive-summary 결과 마크다운을 받아 상태 보고서로 렌더링해줘.
mode=status, 회사명: 한울 엔지니어링, 주차: 11
```

**예시 2: 재무제표 HTML 보고서**
```
financial-statements 결과를 HTML 보고서로 변환해줘.
mode=financial
```

**예시 3: 인시던트 리포트**
```
결제 게이트웨이 502 장애 내용을 정리해서 인시던트 리포트 HTML로 만들어줘.
mode=incident, severity=SEV-2
```

**예시 4: PR 설명 문서**
```
PR #312 실시간 알림 채널 통합 내용을 HTML 리뷰 문서로 만들어줘.
mode=pr
```

---

## 비-목표

- [HARD] 마크다운 기본 출력 대체 금지 — HTML은 추가 렌더링 분기
- [HARD] React / Vue / Tailwind CDN / Chart.js / D3 도입 금지
- [HARD] 빌드 단계(webpack, vite, esbuild) 도입 금지
- [HARD] `moai-office:pptx-designer`(슬라이드) 영역 침범 금지
- [HARD] `moai-data:data-visualizer`(독립 차트) 영역 침범 금지
- 멀티 파일 출력 금지 — 모든 산출물은 단일 `.html` 파일

---

## 참고 문서

### 설계 문서
- [`references/design-tokens.md`](references/design-tokens.md) — CSS 변수 계약·팔레트·접근성
- [`references/fonts.md`](references/fonts.md) — 폰트 매핑·CDN URL·preconnect 패턴

### 템플릿
- [`references/templates/status.html.tmpl`](references/templates/status.html.tmpl) — status 모드
- [`references/templates/incident.html.tmpl`](references/templates/incident.html.tmpl) — incident 모드
- [`references/templates/plan.html.tmpl`](references/templates/plan.html.tmpl) — plan 모드
- [`references/templates/explainer.html.tmpl`](references/templates/explainer.html.tmpl) — explainer 모드
- [`references/templates/financial.html.tmpl`](references/templates/financial.html.tmpl) — financial 모드
- [`references/templates/pr.html.tmpl`](references/templates/pr.html.tmpl) — pr 모드

### 샘플 출력
- [`references/samples/status-sample.html`](references/samples/status-sample.html) — status 모드 렌더링 예시
- [`references/samples/incident-sample.html`](references/samples/incident-sample.html) — incident 모드 렌더링 예시
- [`references/samples/plan-sample.html`](references/samples/plan-sample.html) — plan 모드 렌더링 예시
- [`references/samples/explainer-sample.html`](references/samples/explainer-sample.html) — explainer 모드 렌더링 예시
- [`references/samples/financial-sample.html`](references/samples/financial-sample.html) — financial 모드 렌더링 예시
- [`references/samples/pr-sample.html`](references/samples/pr-sample.html) — pr 모드 렌더링 예시

원본 사상: [Thariq Shihipar, "The Unreasonable Effectiveness of HTML"](https://thariqs.github.io/html-effectiveness/)

---

## P1 컨슈머 통합 (Wave 3 검증 완료)

4개 P1 컨슈머 스킬의 마크다운 출력을 html-report 템플릿으로 렌더링한 통합 테스트 결과입니다.

| 컨슈머 스킬 | 적합 모드 | 입력 파일 | 렌더링 출력 | 호환성 |
|-------------|-----------|-----------|-------------|--------|
| `moai-bi:executive-summary` | `status` | [`references/integration-tests/executive-summary-input.md`](references/integration-tests/executive-summary-input.md) | [`references/integration-tests/executive-summary-rendered.html`](references/integration-tests/executive-summary-rendered.html) | ★★★★☆ (4/5) |
| `moai-finance:financial-statements` | `financial` | [`references/integration-tests/financial-statements-input.md`](references/integration-tests/financial-statements-input.md) | [`references/integration-tests/financial-statements-rendered.html`](references/integration-tests/financial-statements-rendered.html) | ★★★★☆ (4/5) |
| `moai-business:sbiz365-analyst` | `plan` | [`references/integration-tests/sbiz365-analyst-input.md`](references/integration-tests/sbiz365-analyst-input.md) | [`references/integration-tests/sbiz365-analyst-rendered.html`](references/integration-tests/sbiz365-analyst-rendered.html) | ★★★★☆ (4/5) |
| `moai-business:daily-briefing` | `status` (daily variant) | [`references/integration-tests/daily-briefing-input.md`](references/integration-tests/daily-briefing-input.md) | [`references/integration-tests/daily-briefing-rendered.html`](references/integration-tests/daily-briefing-rendered.html) | ★★★★☆ (4/5) |

상세 호환성 분석: [`references/integration-tests/COMPATIBILITY.md`](references/integration-tests/COMPATIBILITY.md)
