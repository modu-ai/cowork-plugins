# 인라인 SVG 인포그래픽 패턴

html-slide의 인포그래픽(차트·다이어그램·KPI·타임라인)은 **LLM이 인라인 SVG로 직접 저작**합니다. AI 래스터 이미지로 우회하지 않습니다 — 한국어 숫자·라벨이 100% 정확해야 하고, 확대해도 선명하며, 소스 텍스트 변경 시 동일 결과가 재현되어야 하기 때문입니다.

## 왜 SVG인가 (AI 래스터가 아닌)

| 축 | 인라인 SVG (코드 렌더) | AI 래스터 (GPT Image/Nano Banana) |
|----|------------------------|------------------------------------|
| 한국어 숫자·라벨 정확도 | ✅ 100% (텍스트 노드) | ⚠️ 변동 (95%+ 주장, 오류 빈번) |
| 확대 선명도 | ✅ 벡터 (무한 확대) | ❌ 래스터 (뭉개짐) |
| 재현성 | ✅ 100% (소스 동일=결과 동일) | ❌ 비결정적 |
| 오타 수정 | ✅ 소스 1줄 | ❌ 전체 재생성 |
| 브랜드 토큰 정합 | ✅ CSS 변수 주입 | ⚠️ 프롬프트로 유도 (불확실) |

→ 인포그래픽은 **무조건 SVG**. AI 래스터는 히어로·실사 일러스트처럼 "정확한 텍스트가 필요 없는 장식 영역"에만 (`references/image-backend-policy.md`).

## 한국어 렌더 규칙 (필수)

```svg
<text font-family="Pretendard, 'Noto Sans KR', sans-serif"
      text-anchor="middle" dominant-baseline="central">
  1,234억 원
</text>
```

1. **font-family 명시** — `Pretendard, 'Noto Sans KR', sans-serif`. 시스템 폰트만 쓰면 OS별 폴백으로 깨짐
2. **text-anchor** — `start`/`middle`/`end`로 수평 정렬
3. **dominant-baseline** — `central`/`hanging`/`alphabetic`로 수직 정렬
4. **숫자는 그룹화** — 단위(억 원, %)는 별도 `<tspan>`으로 크기/색 차등
5. **design_system 토큰 주입** — `fill="var(--primary)"` 등 CSS 변수로 브랜드 색 정합

## 패턴 1: KPI 카드 (큰 숫자 + 라벨)

```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(140,280)">
    <text font-family="Pretendard" font-size="180" font-weight="800"
          fill="var(--primary, #cc785c)" text-anchor="middle">920</text>
    <text y="60" font-family="Pretendard" font-size="32" fill="var(--ink, #141413)"
          text-anchor="middle">분기 매출 (억 원)</text>
    <text y="110" font-family="Pretendard" font-size="24" fill="#788C5D"
          text-anchor="middle">▲ 전년 대비 +34%</text>
  </g>
</svg>
```

## 패턴 2: 막대 차트 (수직)

```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <!-- 축 -->
  <line x1="200" y1="600" x2="1100" y2="600" stroke="var(--g300)" stroke-width="2"/>
  <!-- 막대 (값: 320, 480, 610, 920 → max 1000 기준 스케일) -->
  <g fill="var(--primary, #cc785c)">
    <rect x="280"  y="504" width="120" height="96"  rx="4"/>
    <rect x="500"  y="456" width="120" height="144" rx="4"/>
    <rect x="720"  y="417" width="120" height="183" rx="4"/>
    <rect x="940"  y="324" width="120" height="276" rx="4"/>
  </g>
  <!-- 값 라벨 -->
  <g font-family="Pretendard" font-size="28" font-weight="700" fill="var(--ink)" text-anchor="middle">
    <text x="340" y="484">320</text>
    <text x="560" y="436">480</text>
    <text x="780" y="397">610</text>
    <text x="1000" y="304">920</text>
  </g>
  <!-- X축 라벨 -->
  <g font-family="Pretendard" font-size="24" fill="var(--g500)" text-anchor="middle">
    <text x="340"  y="640">Q1</text>
    <text x="560"  y="640">Q2</text>
    <text x="780"  y="640">Q3</text>
    <text x="1000" y="640">Q4</text>
  </g>
</svg>
```

## 패턴 3: 도넛 차트 (비율)

도넛은 `stroke-dasharray`로 세그먼트를 그립니다 (반지름 r=120, 둘레=2πr≈754).

```svg
<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(300,300) rotate(-90)">
    <circle r="120" fill="none" stroke="var(--g100)" stroke-width="60"/>
    <!-- 60% (primary) -->
    <circle r="120" fill="none" stroke="var(--primary)" stroke-width="60"
            stroke-dasharray="452 754" stroke-dashoffset="0"/>
    <!-- 25% (secondary) -->
    <circle r="120" fill="none" stroke="var(--secondary)" stroke-width="60"
            stroke-dasharray="188 754" stroke-dashoffset="-452"/>
  </g>
  <text x="300" y="295" font-family="Pretendard" font-size="56" font-weight="800"
        fill="var(--ink)" text-anchor="middle">60%</text>
  <text x="300" y="335" font-family="Pretendard" font-size="22" fill="var(--g500)"
        text-anchor="middle">B2B SaaS</text>
</svg>
```

> `stroke-dasharray="<세그먼트길이> <둘레>"`, `stroke-dashoffset`은 이전 세그먼트 누적 길이의 음수. 비율% × 둘레(754) = 세그먼트 길이.

## 패턴 4: 타임라인 (수평 마일스톤)

```svg
<svg viewBox="0 0 1280 400" xmlns="http://www.w3.org/2000/svg">
  <line x1="140" y1="200" x2="1140" y2="200" stroke="var(--g300)" stroke-width="3"/>
  <g>
    <circle cx="240"  cy="200" r="14" fill="var(--primary)"/>
    <text x="240"  y="160" font-family="Pretendard" font-size="22" font-weight="700"
          fill="var(--ink)" text-anchor="middle">2026 Q1</text>
    <text x="240"  y="250" font-family="Pretendard" font-size="18" fill="var(--g500)"
          text-anchor="middle">MVP 런칭</text>
  </g>
  <!-- 추가 마일스톤... -->
</svg>
```

## 패턴 5: 비교 카드 (A vs B)

2-3개 카드를 `<g transform="translate(x,y)">`로 배치. 각 카드는 헤더 배경(`<rect>`) + 항목 리스트(`<text>`).

## design_system 토큰 주입

모든 SVG는 `fill`/`stroke`에 CSS 변수를 사용합니다. `<style>` 블록에서 design-system-library 토큰을 `:root`에 선언:

```css
:root {
  --primary: #cc785c;   /* claude coral */
  --secondary: #6a9bcc;
  --ink: #141413;
  --g100: #f0eee6;
  --g300: #d1cfc5;
  --g500: #87867f;
}
```

design_system 변경 시 이 블록만 교체하면 모든 인포그래픽이 브랜드 재정렬됩니다. 시스템별 정확 토큰값은 `design-system-library/systems/<name>.md`에서 로드.

## 검수 체크리스트

- [ ] 모든 `<text>`에 `font-family`, `text-anchor`, `dominant-baseline` 명시
- [ ] 숫자·단위 정확 (원고 deck.json의 chart.data와 일치)
- [ ] 한국어 글리프 깨짐 없음 (폰트 CDN 로드 확인)
- [ ] 색 대비 4.5:1 이상 (WCAG AA)
- [ ] design_system 토큰 변수 사용 (하드코딩 색 아님)
- [ ] viewBox 비율 16:9 (1280×720) 또는 1:1 (1080×1080)
