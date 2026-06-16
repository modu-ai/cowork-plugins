# Table — shadcn vanilla

shadcn `Table` / `TableHeader` / `TableBody` / `TableRow`를 React 없이 **semantic HTML + Tailwind token class**로 재현합니다. 토큰 규칙은 [`../mapping/tailwind.md`](../mapping/tailwind.md) §1·§3 참조.

## 기본

```html
<div class="w-full overflow-x-auto rounded-lg border border-hairline">
  <table class="w-full text-sm">
    <thead class="bg-surface-card text-left text-muted">
      <tr>
        <th class="px-4 py-3 font-medium">항목</th>
        <th class="px-4 py-3 font-medium">상태</th>
        <th class="px-4 py-3 text-right font-medium">값</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-hairline">
      <tr class="text-ink">
        <td class="px-4 py-3">API 응답시간</td>
        <td class="px-4 py-3"><span class="inline-flex items-center rounded-full bg-success/15 px-3 py-1 text-xs font-medium text-success">OK</span></td>
        <td class="px-4 py-3 text-right font-mono">142ms</td>
      </tr>
      <tr class="text-ink">
        <td class="px-4 py-3">에러율</td>
        <td class="px-4 py-3"><span class="inline-flex items-center rounded-full bg-warning/15 px-3 py-1 text-xs font-medium text-warning">Watch</span></td>
        <td class="px-4 py-3 text-right font-mono">0.4%</td>
      </tr>
    </tbody>
  </table>
</div>
```

## 변형

### 스트라이프 (가독성)

`tbody tr:nth-child(even)` 에 `bg-surface-soft/50`을 추가하면 줄무늬.

```html
<tbody class="divide-y divide-hairline [&_tr:nth-child(even)]:bg-surface-soft/50">
  ...
</tbody>
```

### 다크 테마

다크 시스템(clickhouse 등)은 `bg-surface-dark` 본문 + `text-on-dark` + `divide-hairline`(다크 hairline 토큰)로 자동 어울림.

## 토큰 메모

- `divide-hairline` — 행 구분선(브랜드 `hairline`).
- `bg-surface-card` — 헤더 배경. 다크 시스템에선 다크 카드 색.
- 숫자 열은 `font-mono` + `text-right` 권장(정렬 가독성).
- `[&_tr:nth-child(even)]:bg-surface-soft/50` — arbitrary variant로 스트라이프. alpha utility는 토큰 무관.
