# Badge — shadcn vanilla

shadcn `Badge`를 React 없이 **vanilla HTML + Tailwind token class**로 재현합니다. 토큰 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md) §1·§3 참조.

## 변형

### default (neutral)

```html
<span class="inline-flex items-center rounded-full bg-surface-card px-3 py-1 text-xs font-medium text-ink">Badge</span>
```

### primary (강조)

```html
<span class="inline-flex items-center rounded-full bg-primary px-3 py-1 text-xs font-semibold uppercase tracking-wider text-white">New</span>
```

### success / warning / error (시맨틱)

```html
<span class="inline-flex items-center rounded-full bg-success/15 px-3 py-1 text-xs font-medium text-success">Active</span>
<span class="inline-flex items-center rounded-full bg-warning/15 px-3 py-1 text-xs font-medium text-warning">Pending</span>
<span class="inline-flex items-center rounded-full bg-error/15 px-3 py-1 text-xs font-medium text-error">Failed</span>
```

### outline

```html
<span class="inline-flex items-center rounded-full border border-hairline px-3 py-1 text-xs font-medium text-muted">v2.22</span>
```

## 토큰 메모

- 시맨틱 배지는 `bg-<semantic>/15`(15% alpha) + `text-<semantic>` 조합으로 부드러운 틴트. `success` / `warning` / `error` 토큰이 없는 시스템은 `primary` 또는 `accent-*`로 대체.
- 다크 테마 시스템에서 neutral 배지는 `bg-surface-card`(다크 카드 색) + `text-on-dark`로 자동 어울림.
