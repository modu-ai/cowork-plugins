# Tabs — shadcn vanilla

shadcn `Tabs` / `TabsList` / `TabsTrigger` / `TabsContent`를 React 없이 재현합니다. 두 패턴 — (A) 의존성 0 `<details>` 폴백, (B) vanilla JS ARIA 탭. 토큰 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md) §1·§3 참조.

## (A) `<details>` 폴백 — JS 불필요

아코디언형. 단일 파일에서 가장 단순하고 접근성이 기본 보장됩니다.

```html
<details class="rounded-lg border border-hairline bg-surface-card" open>
  <summary class="cursor-pointer list-none px-5 py-4 font-medium text-ink marker:hidden">
    개요 <span class="float-right text-muted">▾</span>
  </summary>
  <div class="border-t border-hairline px-5 py-4 text-body">
    첫 번째 패널 내용.
  </div>
</details>
<details class="mt-2 rounded-lg border border-hairline bg-surface-card">
  <summary class="cursor-pointer list-none px-5 py-4 font-medium text-ink marker:hidden">
    상세 <span class="float-right text-muted">▾</span>
  </summary>
  <div class="border-t border-hairline px-5 py-4 text-body">
    두 번째 패널 내용.
  </div>
</details>
```

## (B) ARIA 탭 (vanilla JS) — 동시 노출 불가, 한 패널만

```html
<div class="rounded-lg border border-hairline bg-surface-card">
  <div role="tablist" class="flex gap-1 border-b border-hairline p-1" aria-label="보고서 섹션">
    <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1"
            class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white">요약</button>
    <button role="tab" id="tab-2" aria-selected="false" aria-controls="panel-2" tabindex="-1"
            class="rounded-md px-4 py-2 text-sm font-medium text-muted hover:text-ink">지표</button>
  </div>
  <div role="tabpanel" id="panel-1" aria-labelledby="tab-1" class="p-5 text-body">
    요약 패널.
  </div>
  <div role="tabpanel" id="panel-2" aria-labelledby="tab-2" class="hidden p-5 text-body">
    지표 패널.
  </div>
</div>

<script>
  document.querySelectorAll('[role="tab"]').forEach((tab) => {
    tab.addEventListener('click', () => {
      const list = tab.closest('[role="tablist"]');
      list.querySelectorAll('[role="tab"]').forEach((t) => {
        const sel = t === tab;
        t.setAttribute('aria-selected', sel);
        t.classList.toggle('bg-primary', sel);
        t.classList.toggle('text-white', sel);
        t.classList.toggle('text-muted', !sel);
        t.tabIndex = sel ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls'))
                .classList.toggle('hidden', !sel);
      });
    });
  });
</script>
```

## 토큰 메모

- 선택 탭은 `bg-primary text-white`, 비선택은 `text-muted` → `text-ink` hover.
- `<details>` 패턴은 `0-JS` 산출물(html-report 기본 템플릿)과 호환. ARIA 탭은 CDN 환경(html-report design_system 지정 시)에서만.
- 키보드 접근성: ARIA 탭은 좌우 화살표로 탭 전환 권장(WAI-ARIA Authoring Practices).
