---
name: learning-material
description: |
  조사한 내용을 도식·차트·수식·코드 하이라이트가 들어간 단일 HTML 학습자료로 만들어 드립니다. 학습목표→핵심개념→도식→예제→복습으로 구조화해, 풍부한 설명과 시각화로 혼자서도 깊이 이해하게 돕습니다.
  다음과 같은 요청 시 사용하세요:
  - "방금 조사한 내용으로 HTML 학습자료 만들어줘"
  - "도식이랑 예제 들어간 공부 자료로 정리해줘"
  - "mermaid 다이어그램으로 개념 정리해줘"
  - "차트랑 코드 하이라이트 넣어서 학습자료 만들어줘"
  - "이 주제 시각적으로 풍부하게 설명 자료 만들어줘"
  - "브라우저에서 바로 보는 학습 노트 HTML로 만들어줘"
  학습 전용 렌더러로, html-report design-token·폰트를 공유해 시각 일관성을 유지하되 mermaid·ECharts·KaTeX·highlight.js·AOS를 콘텐츠가 쓸 때만 조건부 로딩합니다.
  [책임 경계] vs moai-content:html-report: 이 스킬=도식·차트·코드가 풍부한 학습자료(JS 라이브러리 허용), 저 스킬=0-JS 단일파일 업무 보고서.
user-invocable: true
version: 2.27.0
---

# 학습자료 렌더러 (Learning Material)

## 개요

`tutor-research`의 종합본(또는 임의의 학습 내용)을 받아, 학습에 최적화된 구조의 **단일 HTML 학습자료**로 렌더한다. mermaid 도식, ECharts 차트, KaTeX 수식, highlight.js 코드 하이라이트, AOS 스크롤 효과를 **콘텐츠가 실제로 쓸 때만** 주입한다(조건부 로딩 — 순수 텍스트 레슨은 JS 0). html-report의 디자인 토큰·폰트를 공유해 시각 일관성을 유지하지만, html-report의 0-JS 원칙은 건드리지 않는 별도 렌더러다.

## 트리거 키워드

학습자료, 공부 자료, 학습 노트, HTML 학습자료, 도식, 다이어그램, 시각화, 차트, 코드 하이라이트, 수식, 정리 자료

## 입력

| 인자 | 필수 | 설명 |
|------|------|------|
| `content` | ✓ | 학습 내용 (tutor-research 종합본 권장, 일반 Markdown도 가능) |
| `topic` | ✓ | 학습 주제 (제목·파일명에 사용) |
| `level` | — | 대상 수준 (입문/초급/중급/고급) — 설명 깊이 조정 |
| `output_path` | — | 기본값 `<cwd>/materials/<slug>-<YYYYMMDD>.html` |

## 학습자료 구조 (섹션)

학습 효과를 높이는 고정 골격을 따른다. 비어 있는 섹션은 생략한다.

1. **헤더** — 주제 · 대상 수준 · 생성일
2. **학습 목표** — 이 자료를 마치면 할 수 있는 것 (체크리스트)
3. **한눈에 보기 (도식)** — 개념 관계도/플로우/시퀀스 mermaid 도식
4. **핵심 개념** — 개념별 정의 + 풍부한 설명 + 필요 시 수식·차트
5. **예제·코드** — 단계별 예제, 코드 하이라이트, 주석
6. **자주 헷갈리는 점 / 비교** — A vs B 표, 흔한 실수
7. **복습 포인트** — 핵심 요약 + 자가 점검 질문
8. **더 알아보기 · 출처** — 다음 학습 + 검증된 출처 링크

상단에는 sticky **목차(TOC)**, 긴 섹션은 접기·펼치기를 둔다.

## HTML 렌더링 규격

### 자체 완결 단일 파일

- 외부 의존: 폰트 CDN + (콘텐츠가 쓸 때만) 라이브러리 CDN. 그 외 자산 인라인.
- `:root` 디자인 토큰은 `moai-content:html-report`의 `references/design-tokens.md`를 그대로 사용(Anthropic 영감 팔레트).
- 폰트는 explainer 매핑: 본문 Noto Sans KR · 제목 Noto Serif KR · 코드 JetBrains Mono (`references/cdn-libraries.md` 폰트 절 참조).
- `@media print` 블록 포함(인쇄·PDF 저장 대비).

### `<head>` 골격

```html
<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title><topic> — 학습자료</title>
<!-- 폰트 (항상) -->
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap">
<!-- 조건부 라이브러리: 콘텐츠가 쓸 때만 (아래 조건부 로딩 규칙) -->
<style>:root{ /* design-tokens.md 팔레트 + explainer 폰트 override */ } /* 학습 레이아웃 CSS */</style>
</head>
```

### 조건부 로딩 규칙 (HARD)

콘텐츠 분석 후, 실제로 등장하는 요소에 해당하는 라이브러리만 주입한다. CDN URL·초기화 스니펫·대안은 [`references/cdn-libraries.md`](./references/cdn-libraries.md)가 단일 진실(SSOT)이다.

| 콘텐츠에 있으면 | 주입 라이브러리 | 비고 |
|----------------|-----------------|------|
| ` ```mermaid ` 블록 | **Mermaid v11** (ESM) | `<pre class="mermaid">`로 변환 후 init |
| 데이터·수치 시각화 | **ECharts v5** | `<div>` + init 스크립트. 경량 필요 시 Chart.js v4 |
| `$…$` / `$$…$$` 수식 | **KaTeX v0.16** + auto-render | CSS+JS+auto-render 3종 |
| 코드 블록(` ```lang `) | **highlight.js v11** | 테마 CSS + JS + `hljs.highlightAll()` |
| 단계적 등장 효과 | **AOS v2** | `data-aos` 속성 + init. 과용 금지 |

순수 텍스트·표만 있는 자료는 어떤 JS도 주입하지 않는다. 라이브러리가 로드되지 않아도(오프라인) 본문·코드·표는 정상 표시되도록 폴백을 둔다(도식은 mermaid 소스가 `<pre>`로 보임).

### mermaid 통합(예)

```html
<pre class="mermaid">flowchart TD; A[질문]-->B[병렬 리서치]; B-->C[학습자료]</pre>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "neutral" });
</script>
```

전체 CDN URL·초기화 스니펫(ECharts/KaTeX/highlight.js/AOS/대안)은 `references/cdn-libraries.md` 참조.

## 출력

- 단일 `.html` 학습자료 (`<cwd>/materials/<slug>-<YYYYMMDD>.html`)
- 브라우저에서 바로 열람·인쇄·PDF 저장 가능
- 사용한 라이브러리·출처를 자료 하단에 명시

## 사용 예시

**예시 1**: "방금 조사한 서브에이전트 내용으로 HTML 학습자료 만들어줘"
→ 시퀀스 도식(mermaid) + 코드 하이라이트 + 복습 질문 포함 HTML

**예시 2**: "영어 가정법, 표랑 예문으로 학습자료 만들어줘"
→ 규칙 비교 표 + 예문 + 복습 (JS 미주입 — 순수 텍스트·표)

**예시 3**: "이 데이터 추이를 차트로 보여주는 학습자료로 만들어줘"
→ ECharts 라인 차트 + 해설 + 핵심 개념

## 주의사항

- **조건부 로딩 준수** — 안 쓰는 라이브러리는 절대 주입하지 않는다(불필요한 무게·외부 의존 방지).
- **CDN URL은 references/cdn-libraries.md를 인용** — 임의 버전·URL을 지어내지 않는다(메이저 핀: `@11`, `@5`, `@0.16`, `@2`).
- **접근성**: 본문 대비 WCAG AA 유지(design-tokens.md 대비표), 도식·차트에 대체 텍스트·캡션 제공.
- **html-report를 오염시키지 않는다** — 이 렌더러는 별도이며, 업무 보고서는 0-JS인 html-report를 사용한다.
- 학습 내용의 정확성은 입력(tutor-research 출처)에 의존한다. 출처 미검증 내용은 자료에 "확인 필요"로 표기한다.

## 관련 스킬

- **moai-tutor:tutor-research**: 이 스킬의 입력 종합본을 만든다
- **moai-tutor:learning-project**: 생성된 자료를 materials/에 보관하고 진도를 갱신한다
- **참고**: `references/cdn-libraries.md` — CDN 라이브러리 스택 SSOT

## 이 스킬을 사용하지 말아야 할 때

- **0-JS 단일파일 업무 보고서**(현황·재무·인시던트·PR) → `moai-content:html-report`
- **발표용 슬라이드** → `moai-office:pptx-designer`
- **인쇄·제출용 문서(.docx)** → `moai-office:docx-generator`
