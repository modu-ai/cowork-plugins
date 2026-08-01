---
name: design-tokens-transformer
description: |
  하나의 브랜드 토큰을 3계층(DTCG SSOT ↔ 원시 CSS 변수 ↔ semantic/shadcn 롤)으로 양방향 변환합니다.
  L1 DTCG(W3C `$value`/`$type`/`$description`)를 진실 원천으로 삼아 L2 CSS custom properties와 L3 Tailwind v4 `@theme` + `.dark` 전환 체계를 파생하고, 역방향(코드→DTCG)과 라운드트립 무결성 검사도 지원합니다.
  handoff 번들의 3계층 인코딩(02-tokens.json / colors_and_type.css / globals.css)을 자동 변환하는 파이프라인입니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "DTCG 토큰을 CSS 변수로 변환"
  - "디자인 토큰 3계층 매핑"
  - "shadcn semantic 롤 생성"
  - "Tailwind v4 @theme 토큰 만들어 줘"
  - "CSS 변수에서 DTCG SSOT 역추출"
  - "토큰 라운드트립 무결성 검사"
user-invocable: true
version: "1.0.0"
---

# design-tokens-transformer — 3계층 토큰 양방향 변환

## 개요

브랜드 토큰은 소비처마다 다른 형태를 요구합니다. 이 스킬은 **동일한 브랜드 진실(색·타이포·spacing·radius·shadow·motion)**을 3계층으로 인코딩·변환합니다. L1(DTCG)이 SSOT이고, L2/L3은 파생물이며, 역방향 추출과 라운드트립 검사로 계층 간 정합을 보장합니다.

> 이 SKILL.md는 3계층 스키마·양방향 변환 규칙·라운드트립 검사·사용 예시를 모두 포함합니다. 색·폰트 값은 브랜드 무관 플레이스홀더(`#RRGGBB`, `<BrandFont>`)로 표기하며, 실제 브랜드 값은 변환 입력(DTCG 소스)에서 주입됩니다.

## 트리거 키워드

DTCG 토큰 변환, 3계층 토큰 매핑, CSS custom properties 생성, shadcn semantic 롤, Tailwind v4 @theme, 토큰 라운드트립, design tokens transformer

## 3계층 모델

| 계층 | 형태 | 소비처 | 대표 파일(handoff.zip) |
|---|---|---|---|
| **L1 — DTCG SSOT** | W3C Design Tokens (`$value`/`$type`/`$description`), 계층적 그룹 | 브랜드 진실 원천 | `assets/round3/02-tokens.json` |
| **L2 — 원시 CSS 변수** | `--color-*` · `--neutral-50..950` · `--tracking-*` + self-host `@font-face` | 단일 파일 HTML 렌더 / 카드 | `colors_and_type.css` |
| **L3 — semantic/shadcn** | `--base-background` · `--base-primary` · `--base-ring` · `--base-sidebar-*` · `--base-chart-1..5` + Tailwind v4 `@theme` + `.dark` 전환 | 프로덕션 코드(shadcn 체계) | `assets/round3/globals.css` |

### L1 — DTCG SSOT 스키마

- W3C 포맷: 각 토큰은 `$value` / `$type` / `$description` 보유
- 계층적 그룹: `color.{brand,neutral,semantic,dark,gradient}` · `typography.{family,weight,size,lineHeight,letterSpacing}` · `spacing` · `radius` · `shadow` · `motion.{duration,easing}` · `container` · `logo`
- `$description`은 출처·의미를 기록 → 브랜드 진실 원천

**DTCG 그룹별 최소 토큰 세트**

| 그룹 | 최소 토큰 | 비고 |
|---|---|---|
| `color.brand` | primary, ink, background (+ primary-hover/active, surface) | 주색·본문색·배경 3종이 필수 하한 |
| `color.neutral` | 50·100·200·300·400·500·600·700·800·900·950 | 11단계 휘도 스케일 |
| `color.semantic` | success, warning, danger, info | 상태색 4종 |
| `color.dark` | background, surface, primary, foreground, border | 다크 오버라이드 최소셋 |
| `color.gradient` | signature (+ soft/dark 파생) | 시그니처 자산 |
| `typography.family` | sans (+ latin/mono/serif) | 본문 폰트 필수 |
| `typography.weight` | regular(400), bold(700) (+ medium/semibold/black) | fontWeight |
| `typography.size` | xs…6xl + display | rem/clamp |
| `typography.lineHeight` | tight, normal (+ snug/relaxed) | number |
| `typography.letterSpacing` | display, heading, body, caption | 한국어 자간 인코딩 |
| `spacing` | 0…32 (4px 베이스 스텝) | dimension |
| `radius` | none, sm, md, lg, full (+ xl/pill) | dimension |
| `shadow` | sm, md, lg (+ xs/xl/signature) | shadow |
| `motion.duration` | fast, normal (+ instant/slow/page) | duration |
| `motion.easing` | default (+ bounce/smooth) | cubicBezier |
| `container`·`logo` | (선택) 브레이크포인트·자산 경로 | logo는 `asset` 타입 |

**`$type` 허용값**

| `$type` | 값 형태 | 표준 |
|---|---|---|
| `color` | hex · `rgb()` · `oklch()` | W3C |
| `dimension` | rem · px · em · `clamp()` | W3C |
| `fontFamily` | 폰트 스택 문자열 | W3C |
| `fontWeight` | 100–900 정수 | W3C |
| `number` | 단위 없는 수(line-height 등) | W3C |
| `duration` | `150ms` · `0.4s` | W3C |
| `cubicBezier` | `cubic-bezier(…)` | W3C |
| `shadow` | box-shadow 문자열/객체 | W3C(composite) |
| `gradient` | `linear-gradient(…)` 문자열 | W3C(composite) — 번들은 문자열 축약형 사용 |
| `asset` | 파일 경로 | 번들 확장(비표준) — 로고 등 자산 |

**예시 JSON (브랜드 무관 — 플레이스홀더)**

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "<브랜드> Design Tokens — <출처 가이드라인> 흡수",
  "$version": "1.0.0",
  "$updatedAt": "YYYY-MM-DD",
  "color": {
    "brand": {
      "primary": { "$value": "#RRGGBB", "$type": "color",
        "$description": "<출처> 명시 — 브랜드 주색. 타이틀/CTA/아이콘" },
      "ink":     { "$value": "#RRGGBB", "$type": "color",
        "$description": "본문 텍스트 — #000 대체" }
    },
    "neutral": { "500": { "$value": "#RRGGBB", "$type": "color" } }
  },
  "typography": {
    "letterSpacing": {
      "display-tight": { "$value": "-0.075em", "$type": "dimension",
        "$description": "히어로 강조" },
      "body":          { "$value": "-0.025em", "$type": "dimension" }
    }
  }
}
```

`$description`은 **출처·의미(provenance)**를 각인하는 자리다 — 값이 어느 가이드라인/시스템에서 왔는지 토큰에 기록해 L1을 진실 원천으로 만든다.

### L2 — 원시 CSS 변수 스키마

- `--color-primary` / `--color-ink` / `--color-bg` / `--color-surface`
- `--neutral-50` … `--neutral-950` (휘도 스케일)
- `--tracking-display-tight` 등 자간 변수(한국어 자간 규칙 인코딩)
- self-host `@font-face` (브랜드 폰트) + CDN 보조 폰트

**CSS 변수 네이밍 규칙**

| 카테고리 | 접두 토큰 | 예 |
|---|---|---|
| 색 역할 | `--color-<역할>` | `--color-primary`·`--color-ink`·`--color-bg`·`--color-surface` |
| 휘도 스케일 | `--neutral-<50..950>` | `--neutral-500` |
| 전경 | `--fg-<1..3>`·`--fg-on-primary` | 본문/보조/플레이스홀더 |
| 보더 | `--border-<1\|2\|strong>`·`--border-focus-ring` | |
| 그라디언트 | `--gradient-<이름>` (+`-soft`/`-dark`) | `--gradient-signature` |
| 폰트/굵기 | `--font-<sans\|latin\|mono>`·`--fw-<regular..black>` | |
| 자간 | `--tracking-<역할>` | `--tracking-body` |
| 크기/행간 | `--text-<xs..6xl\|display>`·`--lh-<tight..relaxed>` | |
| 간격/모서리/그림자 | `--space-<0..32>`·`--radius-<none..full>`·`--shadow-<xs..xl\|signature>` | |
| 모션/컨테이너 | `--duration-<…>`·`--easing-<…>`·`--container-<sm..2xl>` | |

- 다크모드: L2는 `[data-theme="dark"]` 스코프에서 값만 재정의(변수명 동일).
- 별칭(`bg`←background, `fw`←weight, `tracking`←letterSpacing, `space`←spacing, `lh`←lineHeight)은 표에 등록된 것만 사용 — 임의 축약 금지.

**`@font-face` 블록 템플릿 (self-host)**

```css
/* 굵기 1개당 @font-face 1개 반복 */
@font-face {
  font-family: "<BrandFont>";
  font-weight: 400;                 /* 각 굵기별로 반복 (100~900) */
  font-style: normal;
  font-display: swap;               /* FOIT 방지 */
  src: url("./fonts/<BrandFont>-Regular.otf") format("opentype");
}
/* 보조 라틴/모노 폰트는 CDN @import */
@import url("https://fonts.googleapis.com/css2?family=<Latin>:wght@400;600;700&display=swap");
```

**자간 변수 매핑표 (한국어 타이포 인코딩)**

| 자간 변수 | 값 | 적용 | 명명(−N) |
|---|---|---|---|
| `--tracking-display-tight` | -0.075em | 히어로 대형 강조 | −75 |
| `--tracking-display` | -0.05em | 메인 타이틀 | −50 |
| `--tracking-heading` | -0.05em | H1–H4 | −50 |
| `--tracking-body` | -0.025em | 본문 | −25 |
| `--tracking-body-tight` | -0.05em | 밀집 본문 | −50 |
| `--tracking-caption` | 0 | 캡션/라벨 | 0 |

패턴(값은 브랜드마다 조정): 텍스트가 클수록 음의 자간을 강하게 준다 — 한국어 대형 타이포는 글자 사이 공백이 과해 보이므로 조이고, 캡션·소형 텍스트는 0으로 둔다. `−25/−50/−75` 명명은 `-0.025/-0.05/-0.075em`의 축약이다.

### L3 — semantic/shadcn 롤 스키마

- `--base-*` 의미 롤: `background`/`foreground`/`card`/`popover`/`surface`/`muted`/`primary`/`secondary`/`accent`/`destructive`/`border`/`input`/`ring`/`border-strong`/`chart-1..5`/`sidebar-*`
- Tailwind v4 `@theme` + `@layer base/utilities`
- `.dark` 클래스 → CSS 변수 전환으로만 다크모드 (`[HARD] dark:` Tailwind 유틸리티 직접 사용 금지)

**`--base-*` → shadcn 컴포넌트 롤 매핑표**

| `--base-*` 롤(쌍) | shadcn 소비 컴포넌트 | 파생 원천(L2) |
|---|---|---|
| `background`/`foreground` | body·페이지 루트 | `--color-bg`/`--color-ink` |
| `card`/`card-foreground` | Card·Dialog | surface/ink |
| `popover`/`popover-foreground` | Popover·Dropdown·Tooltip | surface/ink |
| `primary`/`primary-foreground` | Button(default)·Tabs active | brand.primary/white |
| `secondary`/`secondary-foreground` | Button(secondary)·Badge | neutral-100/ink |
| `muted`/`muted-foreground` | Skeleton·disabled·보조 텍스트 | neutral-100/neutral-600 |
| `accent`/`accent-foreground` | hover 배경·Calendar | accent/white |
| `destructive`/`destructive-foreground` | Button(destructive)·Alert | semantic.danger/white |
| `border`·`input`·`ring` | 전역 보더·Input 테두리·포커스 링 | neutral-200·neutral-200·primary |
| `chart-1..5` | Recharts·데이터 시각화 | primary/warning/success/info/danger |
| `sidebar-*` | Sidebar 전용 롤 세트 | surface/ink/primary/muted 미러 |

**`@theme` 블록 템플릿 (Tailwind v4)**

```css
@import 'tailwindcss';

@theme {
  --font-sans: "<BrandFont>", system-ui, sans-serif;
  --font-mono: "<Mono>", ui-monospace, monospace;

  --color-primary-50:  #RRGGBB;   /* … 950까지 11단계 */
  --color-primary-600: #RRGGBB;   /* 라이트 주색 */
  --color-primary-500: #RRGGBB;   /* 다크 주색 */
  --color-success: #RRGGBB; --color-warning: #RRGGBB;
  --color-danger:  #RRGGBB; --color-info:    #RRGGBB;

  --radius-sm: 0.5rem; --radius-lg: 1rem; --radius-full: 9999px;
  --duration-fast: 150ms; --ease-out: cubic-bezier(0.4, 0, 0.2, 1);
}

:root { /* --base-* 라이트 롤 바인딩 */ }
.dark { /* --base-* 다크 오버라이드 */ }
```

**`.dark` override 규칙**

- 다크모드는 **오직 `.dark` 클래스 → CSS 변수 재정의**로만. `dark:` Tailwind 유틸리티 직접 사용 금지(`[HARD]`).
- `primary`: 명도 상향(어두운 배경 대비 확보) — 라이트 hover 톤에 해당하는 밝은 값으로.
- `border`/`input`: 불투명 그레이 → 반투명 화이트 `rgba(255,255,255,0.06~0.16)`.
- `chart-1..5`: 전반 명도 상향.
- `gradient`: 밝은 스톱으로 교체.
- 오버라이드 대상만 재선언, 나머지는 `:root` 상속.

## 변환 절차 (스켈레톤)

### 정방향 — L1 → L2 → L3

1. **L1 로드·검증** — DTCG JSON 파싱, `$type`별 유효성 확인, 그룹 완결성 검사
2. **L1 → L2 파생** — brand/neutral/semantic 토큰을 `--color-*`/`--neutral-*`/`--tracking-*` CSS 변수로 평탄화, `@font-face`·CDN 폰트 블록 생성
   - 규칙: 그룹 카테고리를 접두 토큰으로, 마지막 1–2 세그먼트를 접미사로 매핑.
   - `color.brand.<x>`→`--color-<x>` (brand 제거) · `color.brand.background`→`--color-bg` (별칭)
   - `color.neutral.<n>`→`--neutral-<n>` · `color.semantic.<x>`→`--color-<x>` · `color.gradient.<x>`→`--gradient-<x>`
   - `typography.family.<x>`→`--font-<x>` · `weight.<x>`→`--fw-<x>` · `size.<x>`→`--text-<x>` · `lineHeight.<x>`→`--lh-<x>` · `letterSpacing.<x>`→`--tracking-<x>`
   - `spacing.<n>`→`--space-<n>` · `radius.<x>`→`--radius-<x>` · `shadow.<x>`→`--shadow-<x>` · `motion.duration.<x>`→`--duration-<x>` · `motion.easing.<x>`→`--easing-<x>`
   - 별칭(bg·fw·tracking·space·lh)은 표에 등록된 것만 — 유추 금지.
3. **L2 → L3 파생** — 원시 변수를 `--base-*` semantic 롤에 바인딩, `@theme` 등록, `.dark` override 세트 생성
   - brand.primary → `primary`·`ring`·`sidebar-primary`·`sidebar-ring`·`chart-1`
   - brand.ink → `foreground`·`card-foreground`·`popover-foreground` · brand.background → `background` · brand.surface → `card`·`popover`·`surface`·`sidebar`
   - neutral.100 → `muted`·`secondary`·`sidebar-accent` · neutral.200 → `border`·`input` · neutral.600 → `muted-foreground`
   - semantic: success→`success`+`chart-3` · warning→`warning`+`accent`+`chart-2` · info→`info`+`chart-4` · danger→`destructive`+`error`+`chart-5`
   - chart 파생: chart-1=primary · 2=warning|accent · 3=success · 4=info · 5=danger (상태색을 데이터 시리즈로 재사용해 팔레트 일관성 확보)
   - sidebar 파생: surface/ink/primary/muted를 미러 복제 → 사이드바가 본문과 같은 팔레트를 쓰되 독립 토글이 가능하도록 별도 롤로 둔다
4. **FROZEN 규칙 검증** — 소스가 선언한 금지값(예: `#000000` 금지 → ink 대체), 단일 시그니처 그라디언트, 자간 규칙 등을 각 계층 코멘트로 인코딩
   - 메커니즘: 소스 시스템이 선언한 금지 규칙을 각 계층의 네이티브 주석 문법으로 인코딩해 산출물에 주입한다. 변환기는 금지값을 스스로 만들지 않음 — 소스에 선언이 없으면 주입도 없다.
   - 주입 위치: L1 = 토큰 `$description` + 파일 최상위 `$description` / L2 = CSS 헤더 주석(`All tokens FROZEN per <출처>`) + 대체값 인라인 주석(`/* #000 대체 */`, `/* 변경 금지 */`) / L3 = 헤더 주석 + `[HARD]` 인라인(`[HARD] 다크모드는 .dark 클래스로만`).
   - 검증: 소스가 선언한 금지값(예: `#000000`)이 산출물에 유입됐는지만 대조.
   - worked example (특정 브랜드가 선언한 목록 — 보편 법칙 아님): `#000` 금지→ink 대체 · 임의 그라디언트 신설 금지 · 자간 규칙 준수 · `dark:` 유틸리티 금지. 다른 브랜드엔 다른 금지 목록이 온다.

### 역방향 — L3/L2 → L1

1. **소스 계층 식별** — 입력이 CSS(L2) / globals.css(L3) 중 어느 것인지 판별
2. **토큰 추출** — CSS 변수·`@theme` 선언에서 값·의미 역추출
3. **DTCG 재구성** — 추출값을 계층적 그룹으로 재조립, `$description`은 best-effort 유도(원 출처 불명 시 명시)
   - 역매핑(정방향 표를 뒤집되 별칭 해소): `--color-primary`→`color.brand.primary` · `--color-bg`→`color.brand.background` · `--neutral-<n>`→`color.neutral.<n>` · `--color-success`류→`color.semantic.<x>` · `--gradient-<x>`→`color.gradient.<x>`
   - `--fw-<x>`→`typography.weight.<x>` · `--text-<x>`→`size.<x>` · `--tracking-<x>`→`letterSpacing.<x>` · `--space-<n>`→`spacing.<n>` · `--duration-<x>`→`motion.duration.<x>`
   - `--base-<role>`(L3)은 L2→L3 바인딩이라 L1 그룹에 직접 대응하지 않음 → 바인딩표(정방향 3단계) 역참조로 원천 토큰 복원.
   - `$description` 유도 정책: ① 선언 인접 인라인 주석을 승격 → ② 파일 헤더에서 출처(가이드라인/시스템명) 추출해 접두 → ③ 표준 토큰이면 카테고리 표준 설명 → ④ 모두 실패 시 창작 금지, `"출처 미상"` 명시.

### 라운드트립 무결성 검사

- L1 → L2 → L3 → (역) → L1' 왕복 후 L1 ≟ L1' 비교
- 색: hex 정규화 후 동등성, 타이포: family/weight/size 보존, 자간: 값 손실 없음
- 불일치 발견 시 계층·토큰 단위로 diff 리포트
**정규화 규칙 (비교 전 양쪽 값에 동일 적용)**

| 항목 | 정규화 | 예 |
|---|---|---|
| hex 대소문자 | 소문자 통일 | `#FFF`→`#fff` |
| 3자리 shorthand | 6자리 확장 | `#fff`→`#ffffff` |
| `rgb()`/`rgba()` | 정수 채널·알파 정규화, 필요 시 hex 변환 | `rgb(255,255,255)`→`#ffffff` |
| `oklch()` | 색공간 환산 후 비교(무손실 불가 시 허용 오차 명시) | `oklch(…)`↔hex |
| dimension | 단위 통일(rem 우선), `em` 자간 형태 보존 | `4px`↔`0.25rem` |
| 폰트 스택 | 공백·따옴표 정규화 후 순서 보존 비교 | |
| gradient | 각도·스톱·색 정규화(색은 위 hex 규칙) | |

**diff 리포트 포맷**

```
## 라운드트립 diff (L1 vs L1')
| 왕복 | 토큰 경로 | 원본 | 왕복 후 | 판정 |
|---|---|---|---|---|
| L1→L2→L3→L1' | color.brand.primary | #RRGGBB | #RRGGBB | PASS |
| L1→L2→L3→L1' | typography.letterSpacing.body | -0.025em | -0.025em | PASS |
| L1→L2→L3→L1' | color.gradient.signature | linear-gradient(…) | (스톱 순서 상이) | FAIL |
정합: N PASS / M 불일치
```

## 출력 형식

```
## 토큰 변환 완료 (L{src} → L{dst})

### 변환 요약
- 입력 계층: L{n} ([파일])
- 출력 계층: L{m}
- 변환 토큰: 색 N · 타이포 N · spacing N · radius N · shadow N · motion N

### 생성 파일
- [출력 경로]

### 라운드트립 검사
- 왕복 정합: PASS / N개 불일치
- (불일치 시) 계층·토큰 단위 diff

### FROZEN 규칙 검증
- [위반 없음 / 위반 목록]
```

## 사용 예시

**예시 1 — DTCG → shadcn 정방향 (L1 → L3)**

```
입력: 02-tokens.json (L1 DTCG)
동작:
  1) color.brand.primary(#RRGGBB) → --color-primary → --base-primary/--base-ring/--base-chart-1
  2) @theme에 --color-primary-50..950 등록, :root에 --base-* 롤 바인딩
  3) .dark 오버라이드 세트 생성(primary 명도 상향, border 반투명 화이트)
출력: globals.css (@import tailwindcss + @theme + :root + .dark + @layer)
요약: 색 N · 자간 6 · radius 7 · shadow 6 / FROZEN 위반 0
```

**예시 2 — globals.css → DTCG 역추출 (L3 → L1)**

```
입력: globals.css (L3)
동작:
  1) @theme·:root·.dark 변수 선언 스캔
  2) --base-* 롤은 바인딩표 역참조로 원천 토큰 복원, --color-*/--neutral-*는 직접 역매핑
  3) 인접 주석에서 $description 유도, 불명은 "출처 미상"
출력: 02-tokens.json' (재구성 DTCG)
요약: 복원 토큰 N · $description 유도 N / 출처 미상 M
```

**예시 3 — 라운드트립 검사 (L1 → L2 → L3 → L1')**

```
입력: 02-tokens.json (L1)
동작: 정규화(hex 소문자·shorthand 확장·rgb→hex) 후 L1 ≟ L1'
출력: diff 리포트
결과: 12/13 PASS, 1 불일치(gradient 스톱 순서) → 계층·토큰 단위 표기
```

## 주의사항

### Do

- L1(DTCG)을 항상 SSOT로 취급 — L2/L3은 파생물, 수동 편집 시 L1부터 갱신 후 재파생
- 다크모드는 `.dark` 클래스 CSS 변수 전환으로만 — Tailwind `dark:` 유틸리티 직접 사용 금지
- 자간(letter-spacing) 값을 손실 없이 전 계층 보존 — 한국어 타이포 품질의 핵심

### Don't

- L2/L3만 수정하고 L1을 방치 금지 — 다음 재파생에서 덮어써짐
- `#000000` 등 FROZEN 금지값을 변환 산출물에 통과 금지
- 역추출 시 불명확한 `$description`을 임의 창작 금지 — 유도 불가 시 "출처 미상" 명시

## 관련 스킬

| 스킬 | 사용 시점 |
|---|---|
| `moai-designer:cd-handoff-reader` | 선행: 번들에서 3계층 토큰 소스 추출 |
| `moai-designer:cd-system-prep` | 선행: 자산→DESIGN.md 합성(토큰 원천) |
| `moai-designer:design-system-library` | 보조: 75개 브랜드 토큰을 변환 입력으로 |
| `moai-designer:design-sync-upload` | 후속: 변환된 토큰을 Claude Design에 업로드 |
