# 한국어 폰트 정책 — html-report

`moai-content:html-report`의 한국어 웹폰트 CDN URL, 라이선스, preconnect 패턴 SSOT.

---

## 폰트 정책 근거

Thariq 사상은 JS/CSS CDN의 환각·런타임 비결정 문제를 차단하는 것이 목적입니다.
폰트 CDN은 다음 이유로 이 우려에 해당하지 않습니다:

1. **LLM 환각 위험 없음** — 폰트 `<link>`는 정적 URL, 클래스명·API가 없음
2. **런타임 비결정 없음** — 폰트는 시각 자산, JS 실행 결과가 아님
3. **오프라인 폴백** — 폰트 CDN 불가 시 시스템 폰트 폴백 스택으로 정상 표시
4. **한국어 필수성** — 시스템 폰트만으로는 OS별 불일치(macOS/Windows/iOS) 발생

---

## 모드별 폰트 매핑 표

| 모드 | sans (본문) | serif (제목·강조) | mono (코드·태그) | CDN 출처 |
|------|-------------|-------------------|------------------|---------|
| `status` | Pretendard | Pretendard 700 | JetBrains Mono | jsdelivr + Google |
| `financial` | Pretendard | Pretendard 700 | JetBrains Mono | jsdelivr + Google |
| `pr` | Pretendard | Pretendard 700 | JetBrains Mono | jsdelivr + Google |
| `incident` | Pretendard | Pretendard 700 | JetBrains Mono | jsdelivr + Google |
| `plan` | Pretendard | Noto Serif KR | JetBrains Mono | jsdelivr + Google |
| `explainer` | Noto Sans KR | Noto Serif KR | JetBrains Mono | Google |
| `editorial` | Pretendard | 조선일보명조 | JetBrains Mono | jsdelivr + noonfonts |
| `legal` | KoPubWorld Batang | KoPubWorld Batang Bold | JetBrains Mono | jsdelivr (noonfonts) |

---

## CDN URL 및 라이선스

### Pretendard
- **라이선스**: OFL-1.1 (SIL Open Font License)
- **CDN**: jsDelivr (GitHub 미러, pinned v1.3.9)
- **URL**: `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css`
- **포함 웨이트**: 100~900 (Variable Font)
- **preconnect 호스트**: `https://cdn.jsdelivr.net`

### Noto Serif KR + Noto Sans KR (Google Fonts)
- **라이선스**: OFL-1.1
- **CDN**: Google Fonts API
- **URL (결합)**: `https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap`
- **preconnect 호스트**: `https://fonts.googleapis.com`, `https://fonts.gstatic.com`

### JetBrains Mono (Google Fonts)
- **라이선스**: Apache 2.0 — cowork-plugins MIT와 호환
- **CDN**: Google Fonts API
- **URL**: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap`
- **preconnect 호스트**: `https://fonts.googleapis.com`, `https://fonts.gstatic.com`

### 조선일보명조 (Chosunilbo Myungjo)
- **라이선스**: 무료 (개인·상업 사용 허용 — 조선일보 운영, 재배포는 원본 파일 직접 참조 권장)
- **CDN (참고용)**: `https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2105_2@1.0/Chosunilbomyungjo.woff`
- **주의**: 라이선스 최신 여부는 사용 전 직접 확인 권장. self-host 대안 가능.
- **preconnect 호스트**: `https://cdn.jsdelivr.net`

### KoPubWorld Batang (한국출판인회의)
- **라이선스**: OFL-style (무료 배포, 개인·상업 사용 허용 — 한국출판인회의)
- **CDN (참고용)**: `https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_two@1.0/KoPubWorldBatangLight.woff`
- **웨이트**: Light (400), Medium (500) — Bold 별도 URL 확인 필요
- **주의**: 공식 배포처(https://www.kopus.org/biz-electronic-font2/) 직접 self-host 권장
- **preconnect 호스트**: `https://cdn.jsdelivr.net`

---

## preconnect 패턴

### status / financial / pr / incident 모드 (Pretendard + JetBrains Mono)

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap">
```

### plan 모드 (Pretendard + Noto Serif KR + JetBrains Mono)

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap">
```

### explainer 모드 (Noto Sans KR + Noto Serif KR + JetBrains Mono)

```html
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Noto+Serif+KR:wght@400;700&family=JetBrains+Mono:wght@400;500&display=swap">
```

### editorial 모드 (Pretendard + 조선일보명조 + JetBrains Mono)

```html
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2105_2@1.0/Chosunilbomyungjo.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap">
```

조선일보명조는 woff 파일 직접 참조. `@font-face` 인라인 선언 방식으로 대체 가능:

```css
@font-face {
  font-family: "Chosunilbo Myungjo";
  src: url("https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2105_2@1.0/Chosunilbomyungjo.woff") format("woff");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

---

## CSS 변수 오버라이드 패턴

모드별 폰트 적용은 `:root`의 `--sans`, `--serif`, `--mono` 오버라이드로 처리합니다.

```css
/* status / financial / pr / incident 기본 */
:root {
  --sans:  "Pretendard", system-ui, -apple-system, sans-serif;
  --serif: "Pretendard", ui-serif, Georgia, serif;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", monospace;
}

/* plan 모드 override */
:root {
  --serif: "Noto Serif KR", ui-serif, Georgia, serif;
}

/* explainer 모드 override */
:root {
  --sans:  "Noto Sans KR", system-ui, sans-serif;
  --serif: "Noto Serif KR", ui-serif, Georgia, serif;
}

/* editorial 모드 override */
:root {
  --serif: "Chosunilbo Myungjo", "조선일보명조", ui-serif, serif;
}

/* legal 모드 override */
:root {
  --sans:  "KoPubWorld Batang", "KoPubWorld Batang Light", ui-serif, serif;
  --serif: "KoPubWorld Batang", ui-serif, serif;
}
```

---

## font-display: swap 일관 적용

Google Fonts URL에 `&display=swap`을 항상 포함합니다.
Pretendard (jsdelivr CSS)와 KoPubWorld (직접 woff)는 `@font-face`의 `font-display: swap`으로 처리됩니다.

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-05-09 | 1.0.0 | Wave 1 초기 작성 — 6개 폰트 매핑, CDN URL, preconnect 패턴 |
