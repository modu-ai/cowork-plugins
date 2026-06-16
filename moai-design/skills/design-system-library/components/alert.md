# Alert / Callout — shadcn vanilla

shadcn `Alert`를 React 없이 **vanilla HTML + Tailwind token class**로 재현합니다. 보고서·문서에서 주의·안내·경고를 전달합니다. 토큰 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md) §1·§3 참조.

## 변형

### info / default

```html
<div class="flex gap-3 rounded-lg border border-hairline bg-surface-card p-4">
  <div class="text-primary" aria-hidden="true">●</div>
  <div>
    <div class="font-medium text-ink">안내</div>
    <div class="text-sm text-body">이 보고서는 2026-06-16 기준입니다.</div>
  </div>
</div>
```

### success

```html
<div class="flex gap-3 rounded-lg border border-success/30 bg-success/10 p-4">
  <div class="text-success" aria-hidden="true">✓</div>
  <div>
    <div class="font-medium text-ink">복구 완료</div>
    <div class="text-sm text-body">14:02 KST 모든 서비스 정상.</div>
  </div>
</div>
```

### warning

```html
<div class="flex gap-3 rounded-lg border border-warning/30 bg-warning/10 p-4">
  <div class="text-warning" aria-hidden="true">▲</div>
  <div>
    <div class="font-medium text-ink">주의</div>
    <div class="text-sm text-body">에러율이 임계치(0.5%)에 근접했습니다.</div>
  </div>
</div>
```

### error / destructive

```html
<div role="alert" class="flex gap-3 rounded-lg border border-error/40 bg-error/10 p-4">
  <div class="text-error" aria-hidden="true">✕</div>
  <div>
    <div class="font-medium text-ink">장애</div>
    <div class="text-sm text-body">결제 게이트웨이 502 — 즉시 조사 필요.</div>
  </div>
</div>
```

## 토큰 메모

- 시맨틱 variant는 `border-<semantic>/30` + `bg-<semantic>/10` 틴트 조합. `success`/`warning`/`error` 토큰이 없는 시스템은 `primary` 또는 `accent-*`로 대체(info variant처럼).
- 다크 테마 시스템에서 `text-ink`가 white이므로 제목은 그대로 가독성 유지.
- `role="alert"`은 error variant에만 — 스크린리더 즉시 알림.
- 아이콘은 `aria-hidden="true"`로 장식 표시(의미는 텍스트가 전달).
