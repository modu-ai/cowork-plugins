# Button — shadcn vanilla

shadcn `Button`(variant: default / secondary / ghost / destructive)를 React 없이 **vanilla HTML + Tailwind token class**로 재현합니다. 토큰 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md) §1·§3 참조.

## 변형

### default (primary CTA)

```html
<button class="inline-flex h-10 items-center rounded-md bg-primary px-5 text-sm font-medium text-white hover:bg-primary-active focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-canvas">
  Action
</button>
```

### secondary

```html
<button class="inline-flex h-10 items-center rounded-md border border-hairline bg-canvas px-5 text-sm font-medium text-ink hover:bg-surface-card">
  Secondary
</button>
```

### ghost

```html
<button class="inline-flex h-10 items-center rounded-md px-5 text-sm font-medium text-ink hover:bg-surface-card">
  Ghost
</button>
```

### destructive

```html
<button class="inline-flex h-10 items-center rounded-md bg-error px-5 text-sm font-medium text-white hover:opacity-90">
  삭제
</button>
```

### pill (일부 브랜드 — starbucks · mastercard · lovable 등 full-radius)

```html
<button class="inline-flex h-10 items-center rounded-full bg-primary px-6 text-sm font-medium text-white hover:bg-primary-active">
  주문하기
</button>
```

## 토큰 메모

- `bg-primary` / `hover:bg-primary-active` — CTA 기본 쌍. 다크 테마(clickhouse)에서는 primary가 electric yellow, text는 canvas(near-black)가 되어야 가독성 확보 → 그 시스템에선 `text-ink`(=white 정의) 대신 명시적 대비 색 사용.
- `focus-visible:ring-*` — 키보드 접근성. ring 색은 `primary` 권장.
- pill 브랜드는 시스템 frontmatter `rounded.pill` / `rounded.full` 토큰이 있을 때만 `rounded-full` 사용(자동 매핑은 §1.3).
