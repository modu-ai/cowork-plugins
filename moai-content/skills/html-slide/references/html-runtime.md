# HTML 덱 런타임 — 자체 vanilla JS (0의존)

html-slide의 단일 `.html` 파일에 인라인되는 **자체 제작 vanilla JS 덱 런타임**입니다. 외부 프레임워크(reveal.js/Marp/Spectacle) 없이 `file://`로 즉시 오픈되는 것이 원칙입니다. html-report의 0의존 원칙을 슬라이드 시퀀스로 확장합니다.

## 핵심 기능

- **16:9 고정 캔버스** — 뷰포트에 맞춰 스케일 (1280×720 기준)
- **키보드 내비게이션** — `←`/`→`/`Space`/`PageUp`/`PageDown` 슬라이드 이동, `Home`/`End` 처음/끝
- **풀스크린** — `F` 키 또는 클릭 시 Fullscreen API
- **`?print-pdf` 인쇄 모드** — URL 해시로 각 슬라이드를 인쇄 페이지로 강제 개행, Chrome "PDF로 저장" 연동
- **speaker notes 토글** — `S` 키로 발표자 노트 표시/숨김
- **progress bar** — 하단 진행률 표시
- **슬라이드 카운터** — `3 / 8` 표시

## 런타임 골격 (인라인 `<script>`)

```html
<script>
(function () {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  let current = 0;
  const progress = document.getElementById('progress');
  const counter = document.getElementById('counter');
  const isPrint = location.search.includes('print-pdf');

  function show(i) {
    current = Math.max(0, Math.min(i, total - 1));
    slides.forEach((s, idx) => s.classList.toggle('active', idx === current));
    if (progress) progress.style.width = ((current + 1) / total * 100) + '%';
    if (counter) counter.textContent = (current + 1) + ' / ' + total;
    if (!isPrint) location.hash = current + 1;
  }

  function next() { show(current + 1); }
  function prev() { show(current - 1); }

  if (!isPrint) {
    document.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next(); break;
        case 'ArrowLeft':  case 'PageUp':   e.preventDefault(); prev(); break;
        case 'Home': show(0); break;
        case 'End':  show(total - 1); break;
        case 'f': case 'F':
          if (!document.fullscreenElement) document.documentElement.requestFullscreen();
          else document.exitFullscreen();
          break;
        case 's': case 'S':
          document.body.classList.toggle('show-notes');
          break;
      }
    });
    const hash = parseInt(location.hash.slice(1), 10);
    if (!isNaN(hash)) show(hash - 1); else show(0);
  } else {
    // print-pdf 모드: 모든 슬라이드 표시, 페이지 분할
    slides.forEach(s => s.classList.add('active', 'print-page'));
  }
})();
</script>
```

## CSS 골격 (`?print-pdf` 포함)

```css
.slide { display: none; width: 1280px; height: 720px; position: relative; }
.slide.active { display: flex; }
body { margin: 0; background: #000; overflow: hidden; }

/* 중앙 정렬 + 스케일 */
#deck { display: flex; align-items: center; justify-content: center; min-height: 100vh; }

/* speaker notes (기본 숨김) */
.slide .notes { display: none; }
body.show-notes .slide.active .notes {
  display: block; position: fixed; bottom: 0; left: 0; right: 0;
  background: rgba(0,0,0,0.85); color: #fff; padding: 1rem; font-size: 18px;
}

/* progress bar */
#progress { position: fixed; top: 0; left: 0; height: 4px; background: var(--clay,#cc785c); z-index: 999; }
#counter { position: fixed; top: 12px; right: 16px; color: #fff; font-size: 14px; z-index: 999; }

/* ?print-pdf 인쇄 모드 — 각 슬라이드 1페이지 */
@media print {
  .slide { display: flex !important; page-break-after: always; }
  #progress, #counter { display: none; }
}
```

## 16:9 반응형 스케일

뷰포트 크기에 맞춰 1280×720 캔버스를 비율 유지 스케일:

```css
.slide-wrap {
  width: 1280px; height: 720px;
  transform: scale(var(--scale, 1));
  transform-origin: center center;
}
```

```js
function fit() {
  const sx = window.innerWidth / 1280;
  const sy = window.innerHeight / 720;
  document.documentElement.style.setProperty('--scale', Math.min(sx, sy));
}
window.addEventListener('resize', fit); fit();
```

## 인쇄(PDF) 워크플로우

1. 완성된 `.html`을 Chrome/Edge에서 오픈
2. URL에 `?print-pdf` 추가 (예: `file:///...deck.html?print-pdf`)
3. 각 슬라이드가 1페이지로 강제 개행
4. `Ctrl/Cmd+P` → "PDF로 저장" → 16:9 페이지 PDF 산출

> 이 경로는 **PDF** 산출입니다. 편집 가능 **PPTX**는 pptx-designer 체이닝으로 산출합니다 (`references/pptx-chaining.md`).

## 브라우저 호환성

표준 Web API만 사용: `Fullscreen API`, `KeyboardEvent`, `location.hash`, CSS `@media print`, `transform: scale()`. Chrome/Edge/Firefox/Safari 최신 버전에서 동작. 샘플 `samples/deck-sample.html`로 다중 브라우저 시각 검수를 권장.
