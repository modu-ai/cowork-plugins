# Tailwind Play CDN 매핑 규칙

`design-system-library`의 YAML design token을 **Tailwind Play CDN inline config** + **shadcn vanilla 컴포넌트**로 변환하는 단일 진실 매핑 규칙.

> 단일 파일 HTML 산출물을 전제로 합니다. React·빌드 단계 없이 CDN runtime + vanilla 마크업으로 브랜드 토큰을 적용합니다.

---

## 1. YAML 토큰 → Tailwind config 매핑표

각 시스템의 `systems/<name>.md` frontmatter(`colors:` / `typography:` / `rounded:` / `spacing:`)를 아래 규칙으로 `tailwind.config.theme.extend` 객체로 변환합니다.

### 1.1 colors

| YAML 토큰 | Tailwind config 키 | 용도 |
|-----------|-------------------|------|
| `colors.canvas` | `colors.canvas` | 페이지 배경 |
| `colors.surface-soft` | `colors.surface.soft` | 섹션 구분 배경 |
| `colors.surface-card` | `colors.surface.card` | 카드 배경 |
| `colors.surface-dark` | `colors.surface.dark` | 다크 패널 (다크 테마 캔버스) |
| `colors.ink` | `colors.ink` | 본문 텍스트 (라이트 테마) |
| `colors.on-dark` | `colors.on.dark` | 다크 테마 본문 |
| `colors.primary` | `colors.primary` | 강조·CTA |
| `colors.primary-active` | `colors.primary.active` | CTA hover/active |
| `colors.body` / `body-strong` | `colors.body` / `colors.body.strong` | 본문 단계 |
| `colors.muted` / `muted-soft` | `colors.muted` / `colors.muted.soft` | 보조 텍스트 |
| `colors.hairline` | `colors.hairline` | 1px 테두리 |
| `colors.success` / `warning` / `error` | `colors.success` / `warning` / `error` | 시맨틱 |
| `colors.accent-*` | `colors.accent.<name>` | 브랜드 보조 강조 |

### 1.2 typography → fontFamily + fontSize

| YAML 토큰 | Tailwind config 키 |
|-----------|-------------------|
| `typography.display-*.fontFamily` | `fontFamily.display` (display 중복 시 첫 번째) |
| `typography.body-md.fontFamily` | `fontFamily.sans` |
| `typography.code.fontFamily` | `fontFamily.mono` |
| `typography.display-*.fontSize` | `fontSize.display.xl/lg/md/sm` |
| `typography.*.letterSpacing` | `letterSpacing` (display 음수 추적 보존) |

### 1.3 rounded → borderRadius

| YAML | Tailwind |
|------|----------|
| `rounded.xs/sm/md/lg/xl` | `borderRadius.xs/sm/md/lg/xl` (값 그대로) |
| `rounded.pill` / `rounded.full` | `borderRadius.full: 9999px` |

### 1.4 spacing → spacing

| YAML | Tailwind |
|------|----------|
| `spacing.xxs..xxl` | `spacing.xxs..xxl` |
| `spacing.section` | `spacing.section` (섹션 간격 96px) |

---

## 2. Tailwind Play CDN 통합 패턴

단일 파일 HTML의 `<head>`에 다음 3블록을 배치합니다.

```html
<head>
  <!-- (A) Tailwind Play CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- (B) 브랜드 토큰 → tailwind.config 주입 -->
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '<primary>',
            canvas:  '<canvas>',
            ink:     '<ink>',
            hairline:'<hairline>',
            surface: { card: '<surface-card>', dark: '<surface-dark>' },
            /* …시스템 토큰 그대로… */
          },
          fontFamily: {
            display: ['<display-font>', 'serif'],
            sans:    ['<body-font>', 'sans-serif'],
            mono:    ['JetBrains Mono', 'ui-monospace', 'monospace'],
          },
          borderRadius: { md: '8px', lg: '12px', xl: '16px' },
          spacing:      { section: '96px' },
          letterSpacing:{ tight: '-0.02em' },
        }
      }
    }
  </script>

  <!-- (C) 웹폰트 (브랜드 폰트) -->
  <link rel="stylesheet" href="<font-cdn>">
</head>
```

---

## 3. shadcn vanilla 컴포넌트 매핑표

shadcn UI 컴포넌트를 React 없이 Tailwind utility class로 재현한 참조 마크업. 토큰은 위 config에서 정의된 색/폰트/radius 키를 사용합니다.

### 3.1 Card (shadcn `Card`)

```html
<!-- shadcn: <Card /> -->
<div class="rounded-lg border border-hairline bg-surface-card p-8">
  <div class="mb-2 text-sm font-medium uppercase tracking-wide text-muted">Label</div>
  <h3 class="font-display text-2xl tracking-tight text-ink">Card Title</h3>
  <p class="mt-2 text-body">Body content…</p>
</div>
```

### 3.2 Button (shadcn `Button` variant)

```html
<!-- default (primary) -->
<button class="inline-flex h-10 items-center rounded-md bg-primary px-5 text-sm font-medium text-white hover:bg-primary-active">
  Action
</button>

<!-- secondary -->
<button class="inline-flex h-10 items-center rounded-md border border-hairline bg-canvas px-5 text-sm font-medium text-ink">
  Secondary
</button>

<!-- ghost -->
<button class="inline-flex h-10 items-center rounded-md px-5 text-sm font-medium text-ink hover:bg-surface-card">
  Ghost
</button>
```

### 3.3 Badge (shadcn `Badge`)

```html
<!-- default -->
<span class="inline-flex items-center rounded-full bg-surface-card px-3 py-1 text-xs font-medium text-ink">Badge</span>
<!-- primary -->
<span class="inline-flex items-center rounded-full bg-primary px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white">New</span>
```

### 3.4 Table (shadcn `Table`)

```html
<div class="w-full overflow-x-auto rounded-lg border border-hairline">
  <table class="w-full text-sm">
    <thead class="bg-surface-card text-left text-muted">
      <tr><th class="px-4 py-3 font-medium">Header</th></tr>
    </thead>
    <tbody class="divide-y divide-hairline">
      <tr class="text-ink"><td class="px-4 py-3">Cell</td></tr>
    </tbody>
  </table>
</div>
```

### 3.5 Alert / Callout (shadcn `Alert`)

```html
<div class="flex gap-3 rounded-lg border border-hairline bg-surface-card p-4">
  <div class="text-primary">●</div>
  <div>
    <div class="font-medium text-ink">Notice</div>
    <div class="text-sm text-body">Alert body…</div>
  </div>
</div>
```

### 3.6 Stat / Metric (보고서 특화)

```html
<div class="rounded-lg border border-hairline bg-canvas p-6">
  <div class="font-display text-4xl tracking-tight text-primary">2.8k+</div>
  <div class="mt-1 text-xs uppercase tracking-wider text-muted">Metric label</div>
</div>
```

---

## 4. 기본 3테마 구체적 config

### 4.1 claude (warm editorial — light)

```js
tailwind.config = {
  theme: { extend: {
    colors: {
      primary: '#cc785c',          // coral
      'primary-active': '#a9583e',
      canvas:  '#faf9f5',          // cream
      ink:     '#141413',          // warm near-black
      body:    '#3d3d3a',
      muted:   '#6c6a64',
      hairline:'#e6dfd8',
      surface: { card:'#efe9de', dark:'#181715' },
    },
    fontFamily: {
      display: ['Copernicus','Tiempos Headline','Cormorant Garamond','serif'],
      sans:    ['StyreneB','Inter','sans-serif'],
      mono:    ['JetBrains Mono','ui-monospace','monospace'],
    },
    borderRadius: { md:'8px', lg:'12px', xl:'16px' },
    letterSpacing:{ display:'-0.01em' },
  }}
}
```
특징: serif display + warm cream. 본문은 `text-ink` on `bg-canvas`.

### 4.2 clickhouse (high-contrast — dark)

```js
tailwind.config = {
  theme: { extend: {
    colors: {
      primary: '#faff69',          // electric yellow
      'primary-active': '#e6eb52',
      canvas:  '#0a0a0a',          // near-black
      ink:     '#ffffff',          // white type
      body:    '#cccccc',
      muted:   '#888888',
      hairline:'#2a2a2a',
      surface: { card:'#1a1a1a', elevated:'#242424' },
    },
    fontFamily: {
      display: ['Inter','sans-serif'],
      sans:    ['Inter','sans-serif'],
      mono:    ['JetBrains Mono','ui-monospace','monospace'],
    },
    borderRadius: { md:'8px', lg:'12px' },
    letterSpacing:{ display:'-0.02em' },
  }}
}
```
특징: dark canvas + yellow CTA. 본문은 `text-ink`(white) on `bg-canvas`(black). display weight 700.

### 4.3 clay (playful saturated — warm)

```js
tailwind.config = {
  theme: { extend: {
    colors: {
      primary: '#0a0a0a',          // dark navy CTA
      canvas:  '#fffaf0',          // cream
      ink:     '#0a0a0a',
      body:    '#3a3a3a',
      muted:   '#6a6a6a',
      hairline:'#e5e5e5',
      surface: { card:'#f5f0e0', soft:'#faf5e8' },
      brand: { pink:'#ff4d8b', teal:'#1a3a3a', lavender:'#b8a4ed',
               peach:'#ffb084', ochre:'#e8b94a' },
    },
    fontFamily: {
      display: ['Plain Black','Inter','sans-serif'],
      sans:    ['Inter','sans-serif'],
      mono:    ['JetBrains Mono','ui-monospace','monospace'],
    },
    borderRadius: { md:'12px', lg:'16px', xl:'24px' },
    letterSpacing:{ display:'-0.02em' },
  }}
}
```
특징: cream canvas + 6-color saturated feature cards. display weight 500 (rounded Plain Black). 카드 색 순환(pink→teal→lavender→peach→ochre).

---

## 5. 다크 vs 라이트 자동 처리

시스템의 `colors.canvas` 휘도에 따라 본문 텍스트 기본색을 자동 분기합니다:

```
canvas 휘도(luminance) < 0.3 → dark 테마: 본문 = on-dark(white), canvas = 배경
canvas 휘도 ≥ 0.3            → light 테마: 본문 = ink(near-black), canvas = 배경
```

- claude canvas `#faf9f5` → light → 본문 `text-ink`
- clay canvas `#fffaf0` → light → 본문 `text-ink`
- clickhouse canvas `#0a0a0a` → dark → 본문 `text-ink`(=white in this system's config)

> clickhouse는 `ink`가 white로 정의되어 있으므로 dark/light 모두 `text-ink` 사용 가능 — 시스템 내부에서 ink/on-dark가 통일됨.

---

## 6. 검증 체크리스트

매핑 적용 후 산출물이 통과해야 할 항목:

- [ ] `tailwind.config`에 시스템의 모든 `colors` 주요 키가 포함됨
- [ ] display 폰트가 serif(claude) / sans-700(clickhouse) / rounded-500(clay) 특성 반영
- [ ] borderRadius 값이 시스템 `rounded.md/lg/xl`과 일치
- [ ] 다크 시스템은 본문이 캔버스 위에서 가독성 확보(대비 ≥ 4.5:1)
- [ ] CDN script 1건 + config 1건 + 폰트 link — 단일 파일 완결
- [ ] shadcn vanilla 컴포넌트가 token class(canvas/ink/primary/hairline)만 사용

---

## 변경 이력

| 날짜 | 변경 |
|------|------|
| 2026-06-16 | 초기 작성. 기본 3테마(claude/clickhouse/clay) 매핑 검증. 56개 전체 시스템 registry 분류 완료 — 개별 config는 `systems/<name>.md` 토큰에 동일 규칙(§1) 적용 |
