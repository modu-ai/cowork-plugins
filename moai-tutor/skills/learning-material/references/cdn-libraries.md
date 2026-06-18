# 학습자료 CDN 라이브러리 스택 (2026 큐레이션 SSOT)

`moai-tutor:learning-material`이 생성하는 HTML 학습자료에서 사용하는 CDN 라이브러리의 **단일 진실(SSOT)**. 영역별 최고 수준 라이브러리를 선정하고, CDN URL·초기화 스니펫·조건부 로딩 규칙을 정의한다.

---

## 핵심 원칙

1. **조건부 로딩** — 콘텐츠가 실제로 쓰는 라이브러리만 주입한다. 순수 텍스트·표 자료는 JS 0.
2. **메이저 핀** — CDN URL은 메이저 버전만 고정(`@11`, `@5`, `@0.16`, `@2`)한다. 패치 버전을 지어내지 않는다(반환각).
3. **폴백 우선** — 라이브러리가 로드되지 않아도(오프라인·CDN 차단) 본문·코드·표는 정상 표시되어야 한다.
4. **라이선스 안전** — CDN 런타임 로딩은 저장소 NC-ND 라이선스와 무관하다(재배포가 아니라 사용자 브라우저가 직접 로드). 각 라이브러리의 OSS 라이선스(MIT/Apache-2.0/BSD)는 런타임 사용에 제약이 없다.

---

## 큐레이션 표

| 영역 | 채택(기본) | 라이선스 | 선정 근거 | 대안(opt-in) |
|------|-----------|----------|-----------|--------------|
| 다이어그램 | **Mermaid v11** | MIT | 텍스트→플로우·시퀀스·클래스·간트·ER 표준. 학습 개념 시각화에 최적. 정교 수동 레이아웃이 필요한 도식도 mermaid로 우선 표현 | — |
| 차트 | **Apache ECharts v5** | Apache-2.0 | 대용량·인터랙티브·미려, canvas+SVG, 풍부한 차트 유형 | Chart.js v4 (경량·입문) |
| 코드 하이라이트 | **highlight.js v11** | BSD-3 | zero-config 자동 언어 감지, 190+ 언어, 브라우저 동작 | Prism.js v1 (줄번호·복사 버튼 플러그인) |
| 수식 | **KaTeX v0.16** | MIT | 동기 렌더·레이아웃 시프트 0·경량. 수식 즉시 표시 | MathJax 3 (고급 LaTeX·MathML 접근성) |
| 스크롤 효과 | **AOS v2** | MIT | HTML 속성만으로 fade/slide, ~13KB, 정적 HTML 친화 | GSAP v3 +ScrollTrigger (2026 완전 무료, 시네마틱) |

선정 근거 출처는 문서 하단 **출처** 절 참조.

---

## 폰트 (항상 로드)

explainer 매핑 — 한국어 학습 가독성 우선. `moai-content:html-report` `references/fonts.md`와 동일 정책.

```html
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap">
```

```css
:root {
  --sans:  "Noto Sans KR", system-ui, -apple-system, sans-serif;  /* 본문 */
  --serif: "Noto Serif KR", ui-serif, Georgia, serif;             /* 제목·강조 */
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", monospace;  /* 코드 */
}
```

라이선스: Noto(OFL-1.1), JetBrains Mono(Apache-2.0). 폰트 CDN 불가 시 시스템 폰트 폴백 스택으로 정상 표시.

---

## 1. Mermaid v11 — 다이어그램

콘텐츠에 ` ```mermaid ` 블록이 있을 때만 주입.

```html
<pre class="mermaid">
flowchart TD
  A[질문] --> B[병렬 리서치]
  B --> C[학습자료]
</pre>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict" });
</script>
```

- 적합 도식: flowchart(개념 흐름), sequenceDiagram(상호작용), classDiagram(구조), gantt(학습 일정), mindmap(개념 지도)
- 폴백: 로드 실패 시 `<pre>` 안의 mermaid 소스가 텍스트로 보임 → 정보 손실 없음

## 2. Apache ECharts v5 — 차트

데이터·수치 시각화가 있을 때만 주입.

```html
<div id="chart1" style="width:100%;height:360px"></div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
  echarts.init(document.getElementById("chart1")).setOption({
    xAxis: { type: "category", data: ["1주", "2주", "3주"] },
    yAxis: { type: "value" },
    series: [{ type: "line", data: [10, 40, 90] }]
  });
</script>
```

- 경량 대안(Chart.js v4): `https://cdn.jsdelivr.net/npm/chart.js@4` — 작은 데이터셋·입문용
- 폴백: 차트 영역에 데이터 표를 함께 제공해 로드 실패 시에도 수치 확인 가능

## 3. highlight.js v11 — 코드 하이라이트

코드 블록(` ```lang `)이 있을 때만 주입. 공식 npm CDN 패키지는 `@highlightjs/cdn-assets`.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```

- 자동 언어 감지(zero-config). 명시하려면 `<pre><code class="language-python">…</code></pre>`
- 대안(Prism.js): 줄 번호·복사 버튼·diff가 필요할 때 `https://cdn.jsdelivr.net/npm/prismjs@1/...`
- 폴백: 로드 실패 시 `<pre><code>`가 mono 폰트 평문으로 표시 → 코드 가독성 유지

## 4. KaTeX v0.16 — 수식

`$…$`(인라인) / `$$…$$`(블록) 수식이 있을 때만 주입.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});"></script>
```

- 동기 렌더로 레이아웃 시프트 없음. 경량
- 대안(MathJax 3): 고급 LaTeX·MathML 접근성이 필요할 때 `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`
- 폴백: 로드 실패 시 LaTeX 소스가 평문으로 보임

## 5. AOS v2 — 스크롤 효과 (선택)

단계적 등장 효과로 학습 흐름을 강조하고 싶을 때만. **과용 금지** — 학습 집중을 방해하지 않는 선에서.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2/dist/aos.css">
<script src="https://cdn.jsdelivr.net/npm/aos@2/dist/aos.js"></script>
<script>AOS.init({ duration: 500, once: true });</script>
<!-- 사용: <section data-aos="fade-up"> … </section> -->
```

- 고급 대안(GSAP v3 +ScrollTrigger): 시네마틱 시퀀스가 필요할 때. 2026년 Webflow 인수로 완전 무료.
  `https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js` + `https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js`
- 폴백: 로드 실패 시 효과 없이 정상 표시(`once:true`로 콘텐츠는 항상 보임)

---

## 조건부 로딩 결정 표

| 콘텐츠 신호 | 주입 | 비주입 시 |
|-------------|------|-----------|
| ` ```mermaid ` | Mermaid | — |
| 수치 데이터·추이 | ECharts (또는 Chart.js) | 표만 |
| ` ```lang ` 코드 블록 | highlight.js | mono 평문 |
| `$…$` / `$$…$$` | KaTeX | — |
| 등장 효과 요청 | AOS (또는 GSAP) | 정적 |
| 순수 텍스트·표만 | (없음 — JS 0) | — |

---

## 출처

- [10 Best JavaScript Charting Libraries in 2026 (FusionCharts)](https://www.fusioncharts.com/blog/best-javascript-charting-libraries/)
- [The Best JavaScript Chart Libraries for 2026 (Databrain)](https://www.usedatabrain.com/blog/javascript-chart-libraries)
- [Shiki vs Prism vs highlight.js 2026 (PkgPulse)](https://www.pkgpulse.com/guides/shiki-vs-prismjs-vs-highlightjs-syntax-highlighting-2026)
- [Comparing web code highlighters (chsm.dev)](https://chsm.dev/blog/2025/01/08/comparing-web-code-highlighters)
- [Best JavaScript Scroll Animation & Scrollytelling Libraries 2026 (Medium)](https://sajanmangattu.medium.com/best-javascript-scroll-animation-scrollytelling-libraries-2026-5d63f67a1dca)
- [Scroll Animation Tools 2026 (cssauthor)](https://cssauthor.com/scroll-animation-tools/)
- [KaTeX vs MathJax: Web Math Rendering (BigGo)](https://biggo.com/news/202511040733_KaTeX_MathJax_Web_Rendering_Comparison)
- [KaTeX 공식](https://katex.org/) · [Mermaid 공식](https://mermaid.js.org/) · [Apache ECharts 공식](https://echarts.apache.org/) · [highlight.js 공식](https://highlightjs.org/)

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-06-16 | 2.20.0 | 초기 큐레이션 — Mermaid·ECharts·highlight.js·KaTeX·AOS 5종 + 폰트·조건부 로딩 규칙 |
