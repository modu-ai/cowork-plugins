# draw.io CDN 뷰어 임베드 SSOT

`moai-content:drawio-diagram`이 `.drawio` XML을 **단일 HTML로 렌더**하는 방식의 단일 진실(SSOT). 로컬 설치 없이 브라우저에서 동작한다.

---

## 핵심 원칙

1. **CDN 뷰어 단일** — draw.io 정적 뷰어 `viewer-static.min.js` 하나만 로드(자체 완결형 번들).
2. **인라인 XML** — 다이어그램은 `data-mxgraph` 속성에 인라인 임베드(외부 파일 참조 불필요).
3. **폴백 우선** — 뷰어가 차단·실패해도 `.drawio` XML 원문이 `<details>`로 보존돼 정보 손실 0.
4. **토큰 공유** — 헤더·캡션·여백은 html-report `:root` 디자인 토큰을 그대로 사용.
5. **라이선스 안전** — CDN 런타임 로딩(브라우저 직접 로드)은 저장소 NC-ND와 무관. 뷰어는 Apache-2.0.

---

## 1. 뷰어 스크립트 (CDN)

```html
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
```

- **메이저 핀 없음** — draw.io 뷰어는 롤링 무버전 URL이다. 임의 버전 경로(`viewer@5` 등)를 지어내지 않는다.
- **오프라인 자체 호스팅**(선택): `viewer-static.min.js`는 의존성 번들이라 파일을 내려받아 로컬 경로로 교체하면 완전 오프라인 동작. 기본은 CDN.

## 2. 임베드 컨테이너

```html
<div class="mxgraph"
     style="max-width:100%;border:1px solid #D1CFC5;border-radius:12px;"
     data-mxgraph="{JSON — 아래 §3}">
</div>
```

- 클래스는 반드시 `mxgraph`(뷰어가 이 클래스를 스캔).
- `data-mxgraph`의 JSON 안 따옴표는 `&quot;`로 HTML 이스케이프한다(속성값 파싱 안전).

## 3. data-mxgraph JSON 구성 (검증된 키)

```json
{
  "highlight": "#D97757",
  "nav": true,
  "resize": true,
  "toolbar": "zoom layers lightbox",
  "edit": "_blank",
  "lightbox": false,
  "xml": "<mxfile>…전체 .drawio XML…</mxfile>"
}
```

| 키 | 값 | 의미 |
|----|----|------|
| `xml` | 문자열 | 인라인 다이어그램(전체 `<mxfile>…`). `url`보다 우선 |
| `toolbar` | `pages\|zoom\|layers\|lightbox` 조합 | 표시할 툴바 도구 |
| `nav` | `true\|false` | 폴더/페이지 네비게이션 |
| `resize` | `true\|false` | 컨테이너 크기 자동 맞춤 |
| `highlight` | 색상 | 마우스오버 강조색(html-report clay 권장) |
| `lightbox` | `false\|"open"` | 클릭 시 전체화면 라이트박스 |
| `edit` | `_blank` 등 | 편집 버튼 대상(생략 시 비표시) |
| `zoom`/`center`/`page` | 값 | 초기 배율·중앙정렬·페이지 |

키 전체 목록은 draw.io 공식 [Embed HTML options](https://www.drawio.com/docs/reference/embed-html-options/) 참조.

---

## 4. 단일 HTML 래퍼 (html-report 토큰 공유)

`.drawio` XML을 받아 아래 골격에 임베드한다. `<head>`는 html-report explainer 폰트 매핑을 따른다.

```html
<!doctype html><html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title><topic> — 다이어그램</title>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&display=swap">
<style>
  :root{
    --ivory:#FAF9F5; --paper:#FFFFFF; --slate:#141413; --clay:#D97757;
    --oat:#E3DACC; --g300:#D1CFC5; --g500:#87867F;
    --sans:"Noto Sans KR",system-ui,sans-serif; --serif:"Noto Serif KR",ui-serif,Georgia,serif;
  }
  body{margin:0;background:var(--ivory);color:var(--slate);font-family:var(--sans);}
  .wrap{max-width:980px;margin:0 auto;padding:32px 20px;}
  h1{font-family:var(--serif);font-weight:700;}
  .caption{color:var(--g500);font-size:.9rem;margin:.5rem 0 1.5rem;}
  .src{color:var(--g500);font-size:.8rem;border-top:1px solid var(--g300);margin-top:24px;padding-top:12px;}
  details{margin-top:16px;} summary{cursor:pointer;color:var(--g500);}
  pre{background:var(--paper);border:1px solid var(--g300);border-radius:8px;padding:12px;overflow:auto;font-size:.78rem;}
</style>
</head><body>
<div class="wrap">
  <h1><topic></h1>
  <p class="caption"><프리셋> · 생성일 <YYYY-MM-DD></p>

  <div class="mxgraph" style="max-width:100%;border:1px solid var(--g300);border-radius:12px;"
       data-mxgraph="{&quot;highlight&quot;:&quot;#D97757&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;xml&quot;:&quot;…이스케이프된 .drawio XML…&quot;}">
  </div>

  <!-- 폴백: 뷰어 차단·실패 시 원본 XML 보존 -->
  <details>
    <summary>다이어그램 소스 (.drawio XML)</summary>
    <pre><code>&lt;mxfile&gt;…&lt;/mxfile&gt;</code></pre>
  </details>

  <p class="src">렌더: draw.io viewer-static.min.js (Apache-2.0) · 편집: app.diagrams.net에서 .drawio 열기</p>
</div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</body></html>
```

### XML 이스케이프 규칙 (HARD)

`data-mxgraph`는 HTML 속성값이고 그 안에 또 XML이 들어가므로 **이중 이스케이프**가 필요하다.

1. `.drawio` XML 안의 `"`(따옴표) → JSON 문자열로서 `\"` 또는 속성 안에서 `&quot;`
2. XML의 `<`,`>`,`&`는 JSON 문자열 값 안에서는 그대로 둬도 되지만, `data-mxgraph` **속성 전체**를 작은따옴표로 감싸면 내부 큰따옴표 처리가 단순해진다.

**권장**: 속성을 작은따옴표로 감싸고 JSON 내부는 표준 `"` 사용 — `data-mxgraph='{"xml":"<mxfile>…</mxfile>","nav":true}'`. 폴백 `<details><pre>`에는 `<`,`>`,`&`를 `&lt;`,`&gt;`,`&amp;`로 이스케이프한 동일 XML을 넣는다.

---

## 5. learning-material 임베드 모드

`moai-tutor:learning-material`이 ` ```drawio ` 펜스 블록을 만나면, 블록 안 mxGraph XML을 위 컨테이너 `xml` 키에 넣고 뷰어 스크립트를 1회 주입한다(조건부 로딩). 학습자료 1개 파일에 mermaid·drawio가 함께 있을 수 있다. 상세는 learning-material의 `references/cdn-libraries.md` drawio 행 참조.

---

## 출처·라이선스

- **뷰어**: draw.io `viewer-static.min.js` — Apache-2.0. 공식 임베드 규격 [drawio.com/docs/reference/embed-html-options](https://www.drawio.com/docs/reference/embed-html-options/).
- **개념 출처**: [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)(MIT, © 2026). 원본의 CLI-export 방식을 CDN 뷰어로 대체한 것이 본 스킬의 핵심 재구현이다.
