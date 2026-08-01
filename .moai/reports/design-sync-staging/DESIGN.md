# 모두의AI Design System

> 이 문서는 claude.ai/design 업로드용 디자인 시스템 정의다. 모델이 읽고 새 페이지를 생성할 때
> 따라야 할 **지시서**로 작성했다(마케팅 카피 아님). 모든 값은 이 스테이징 폴더의 원천 파일에서
> 도출했으며, 원천이 없는 값은 "미확정"으로 명시했다 — 임의 생성한 값은 없다.
>
> 정체성 기준: **MASTER-BRIEF v3.0 (2026-04-26)**. v1.0(마스코트·CX 7원칙·베타·6서비스)은 폐기됨.
> 자세한 제외 항목은 §6·§9 참조.
>
> 원천 파일: `tokens/02-tokens.json`(L1 DTCG SSOT) · `tokens/colors_and_type.css`(L2) ·
> `tokens/globals.css`(L3 shadcn/Tailwind v4) · `assets/*.png`(로고).

---

## 1. Brand voice & personality

형용사: **신뢰감 있는 · 전문적인 · 따뜻한 · 포용적인 · 명료한 · 큐레이션 중심의 · 실용적인**

모두의AI는 한국어 AI 뉴스 매체이자 AI 아카데미 학습 플랫폼이다. 매일 09:00 KST에 AI 뉴스를
큐레이션하고, 깊이 있는 AI 활용 강좌를 제공한다. 두 서비스(AI 뉴스 매체 + AI 아카데미)만 운영하는
단순한 정체성을 가지며, 전문성과 신뢰를 유지하되 초심자도 배제하지 않는 따뜻한 톤을 지향한다.
디자인은 이 이중 성격(전문성 ↔ 포용성)을 청록 코어 컬러와 한국어 자간 규칙, 굵기 대비로 표현한다.

(출처: `assets/round3/00-MASTER-BRIEF-v3.md` §0·§1.3)

---

## 2. Color palette

> 모든 hex는 원천 파일에서 그대로 옮겼다. `neutral`·`semantic`·`dark`·`gradient`는 L1 DTCG(SSOT)에
> 존재하지만, **11단계 `primary` 스케일과 `accent` 스케일은 L3 `globals.css`에만 존재**하고 L1 DTCG에는
> 없다 — 아래 표의 "출처" 열에 명시했다(§5 계층 드리프트 참조).

### Primary scale (50–950) — 출처: `tokens/globals.css` @theme (L3 전용, DTCG 미수록)

| 단계 | HEX | 의미 |
|---|---|---|
| primary/50 | `#e8f0ef` | 최연한 청록 틴트 (배경 강조) |
| primary/100 | `#c8dad7` | 연한 틴트 |
| primary/200 | `#a0c0bc` | |
| primary/300 | `#6f9d97` | |
| primary/400 | `#3a7873` | |
| **primary/500** | `#22938a` | **다크모드 주색** (라이트 primary +25% 명도) |
| **primary/600** | `#144a46` | **라이트모드 주색** — CTA·타이틀·아이콘 (Notion 명시) |
| primary/700 | `#0e3835` | hover |
| primary/800 | `#0a2825` | active/press |
| primary/900 | `#06171a` | |
| primary/950 | `#09110f` | ink와 동일 |

> `brand.primary`(#144a46)·`primary-hover`(#0e3835)·`primary-active`(#0a2825)는 L1 DTCG에도 존재한다
> (`02-tokens.json` color.brand). 나머지 스케일 단계는 L3에서만 정의된다.

### Neutral scale (50–950) — 출처: `tokens/02-tokens.json` color.neutral + `colors_and_type.css`

| 단계 | HEX | 비고 |
|---|---|---|
| neutral/50 | `#f3f3f3` | = 페이지 배경 |
| neutral/100 | `#eaeaea` | muted/secondary surface |
| neutral/200 | `#d4d4d4` | border/input |
| neutral/300 | `#bcbcbc` | border-strong |
| neutral/400 | `#959595` | placeholder |
| neutral/500 | `#6e6e6e` | caption |
| neutral/600 | `#4c4c4c` | muted-foreground |
| neutral/700 | `#2e2e2e` | |
| neutral/800 | `#1a1f1d` | = 다크 surface |
| neutral/900 | `#0e1513` | = 다크 배경 |
| neutral/950 | `#09110f` | = ink |

> neutral 스케일은 다크모드 표면 색과 값을 공유한다(800=다크 surface, 900=다크 bg, 950=ink). 우연이 아니라
> 단색 청록-그레이 축으로 라이트/다크를 통일한 설계다.

### Brand core (변경 금지 3색 + surface) — 출처: `02-tokens.json` color.brand + MASTER-BRIEF §1.1

| 역할 | HEX | 용도 |
|---|---|---|
| primary | `#144a46` | 어두운 청록. CTA·카테고리 칩·강조 텍스트·아이콘 |
| ink (foreground) | `#09110f` | 본문 텍스트. **#000000 사용 금지** |
| background | `#f3f3f3` | 페이지 기본 배경. **#ffffff로 대체 금지** |
| surface | `#ffffff` | 카드/모달 배경 (배경 대비 +1단계 명도) |

### Secondary · Accent — 출처: `tokens/globals.css` @theme (L3 전용)

| 역할 | HEX | 비고 |
|---|---|---|
| accent/400 | `#d99a3f` | warm amber (L3 전용) |
| accent/500 | `#c47b2a` | = semantic warning 값과 동일 |
| accent/600 | `#a36322` | |
| secondary | `#eaeaea` | = neutral/100 (light gray surface) |

### Semantic — 출처: `02-tokens.json` color.semantic + `colors_and_type.css` + `globals.css`

| 상태 | HEX |
|---|---|
| success | `#1c7c70` |
| warning | `#c47b2a` |
| danger / error | `#c44a3a` |
| info | `#2a8a8c` |

### Dark overrides — 출처: `02-tokens.json` color.dark + `colors_and_type.css` [data-theme=dark] + `globals.css` .dark

| 역할 | HEX / 값 |
|---|---|
| background | `#0e1513` |
| surface | `#1a1f1d` |
| primary | `#22938a` (라이트 +25% 명도, AA 통과) |
| primary-hover | `#2bafa3` |
| foreground | `#e8eae9` |
| muted-foreground | `#a8aeac` |
| border | `rgba(255,255,255,0.08)` |
| border-strong | `rgba(255,255,255,0.16)` |
| chart-1..5 | `#22938a` · `#d99a3f` · `#2bafa3` · `#58c4b9` · `#d96b5b` (전반 명도 상향) |

### Signature asset (브랜드 코어) — 출처: `02-tokens.json` color.gradient + `colors_and_type.css`

```css
/* 라이트 */
--gradient-signature:      linear-gradient(135deg, #144a46 0%, #09110f 100%);
--gradient-signature-soft: linear-gradient(135deg, rgba(20,74,70,0.08) 0%, rgba(9,17,15,0.04) 100%);
/* 다크 */
--gradient-signature(.dark): linear-gradient(135deg, #22938a 0%, #144a46 100%);
```
사용처: Editor's Pick 풀-블리드 배경, AI 아카데미 섹션 배경, 1차 CTA, 시그니처 디바이더, 카드 hover.

---

## 3. Typography

출처: `tokens/colors_and_type.css`(@font-face + 요소 스타일) · `02-tokens.json` typography ·
`tokens/globals.css` @theme(폰트 스택) · MASTER-BRIEF §1.2.

### Families

| 역할 | 폰트 | 로딩 방식 |
|---|---|---|
| Display / Heading / Body (sans) | `Pretendard Variable` → `Pretendard` fallback | jsDelivr CDN `pretendard@v1.3.9` dynamic-subset(globals.css) + self-host `@font-face` 100~900(colors_and_type.css) |
| Latin 보조 | `Inter Variable` → `Inter` | fontsource self-host + Google Fonts `@import`(colors_and_type.css) |
| Mono | `JetBrains Mono Variable` → `JetBrains Mono` | fontsource self-host + Google Fonts `@import` |
| Serif (L3 전용) | `Pretendard Variable` / `Noto Serif KR` | globals.css `--font-serif` |

### Weights (fontWeight)

400 regular · 500 medium · 600 semibold · 700 bold · 900 black.
(self-host `@font-face`는 100~900 전 굵기 정의; DTCG는 400/500/600/700/900 노출.)

### Size / lineHeight scale

| size | rem | | lineHeight | number |
|---|---|---|---|---|
| xs | 0.75 | | tight | 1.05 |
| sm | 0.875 | | snug | 1.25 |
| base | 1 | | normal | 1.5 |
| lg | 1.125 | | relaxed | 1.75 |
| xl | 1.25 | | | |
| 2xl | 1.5 | | | |
| 3xl | 1.875 | | | |
| 4xl | 2.25 | | | |
| 5xl | 3 | | | |
| 6xl | 3.75 | | | |
| display | `clamp(2.25rem, 4.5vw, 4rem)` | | | |

### Letter-spacing rules (한국어 자간 — Notion 규칙)

| 역할 | 값 |
|---|---|
| display-tight (히어로 강조) | `-0.075em` |
| display (메인 타이틀) | `-0.05em` |
| heading (h1~h4) | `-0.05em` |
| body (본문) | `-0.025em` |
| body-tight (밀집 본문) | `-0.05em` |
| caption (라벨) | `0` |

원칙: 텍스트가 클수록 음의 자간을 강하게 준다(한국어 대형 타이포는 글자 공백이 과해 보이므로 조인다).
`word-break: keep-all`을 본문에 적용한다(globals.css @layer base).

### Weight-contrast pattern

한 문장 안에서 도입부/보조는 Regular(400)·Medium(500)로, 핵심 메시지는 Bold(700)·Black(900)로 대비를
주어 시각적 리듬을 만든다. 적용 예(실제 Hero 카피): "오늘의 AI를, **5분이면 따라잡습니다**."

### 요소 매핑 (colors_and_type.css)

| 요소 | size | weight | letter-spacing | line-height |
|---|---|---|---|---|
| `.display` / `h1.display` | display | black(900) | display-tight | tight(1.05) |
| `h1` | 4xl | bold(700) | display(-0.05em) | 2.5rem |
| `h2` | 3xl | bold(700) | heading | 2.25rem |
| `h3` | 2xl | semibold(600) | heading | 2rem |
| `h4` | xl | semibold(600) | heading | 1.75rem |
| `p` / `.body` | base | regular(400) | body(-0.025em) | normal(1.5) |
| `.caption` | xs | medium(500) | caption(0) | 1rem |

---

## 4. Spacing / Radius / Shadow / Motion

출처: `02-tokens.json` + `colors_and_type.css`. **Radius·Motion은 L2↔L3 값이 다르다 — §5 계층 드리프트 필독.**

### Spacing (4px 베이스)

`0 · 1(0.25rem) · 2(0.5) · 3(0.75) · 4(1) · 5(1.25) · 6(1.5) · 8(2) · 10(2.5) · 12(3) · 16(4) · 20(5) · 24(6) · 32(8rem)`

### Radius

| 토큰 | L1/L2 (`02-tokens.json`·`colors_and_type.css`) | L3 (`globals.css` @theme) |
|---|---|---|
| xs | (없음) | `0.25rem` (4px) |
| sm | `4px` | `0.5rem` (8px) |
| md | `8px` | `0.75rem` (12px) |
| lg | `16px` | `1rem` (16px) |
| xl | `24px` | `1.5rem` (24px) |
| pill | `32px` | `2rem` (32px) |
| full | `9999px` | `9999px` |

> **드리프트 경고**: L2 `sm=4px`지만 L3 `sm=8px`(=L2 md). L3는 `xs=4px`를 신설하고 sm/md를 한 단계씩
> 밀었다. 컴포넌트 레시피(§8)는 의미 역할(card=lg, CTA=pill)로 참조하므로 실사용 영향은 없으나, 원시 px를
> 하드코딩하지 말 것.

### Shadow (ink 기반 rgba(9,17,15,α))

`xs(0 1px 2px /.04) · sm(0 2px 4px /.06) · md(0 4px 12px /.08) · lg(0 8px 24px /.10) · xl(0 16px 48px /.12)`
`signature: 0 8px 32px rgba(20,74,70,0.20)` — **hover 상태 전용**(임의 사용 금지).

### Motion

| duration | 값 | | easing | 값 |
|---|---|---|---|---|
| instant | 75ms | | default / ease-out | `cubic-bezier(0.4, 0, 0.2, 1)` |
| fast | 150ms | | bounce / spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` |
| normal (L3: base) | 250ms | | smooth | `cubic-bezier(0.16, 1, 0.3, 1)` |
| slow | 400ms | | | |
| page (L3: slower) | 600ms | | | |

> L3는 `base`(=normal 250ms)·`slower`(=page 600ms)·`spring`(=bounce)·`ease-in-out`(값은 ease-out과 동일)
> 별칭을 추가했다. L2는 `--easing-*`, L3는 `--ease-*` 접두를 쓴다(같은 값, 다른 변수명).

---

## 5. Token 3-layer mapping

3계층 인코딩(변환·검증은 `moai-designer:design-tokens-transformer` 소관). L1이 SSOT, L2/L3은 파생.

- **L1 — DTCG SSOT**: `tokens/02-tokens.json` — `$value`/`$type`/`$description`, `color.{brand,neutral,semantic,dark,gradient}` · `typography.*` · `spacing`/`radius`/`shadow`/`motion`/`container`/`logo`.
- **L2 — 원시 CSS 변수**: `tokens/colors_and_type.css` — `--color-*`/`--neutral-*`/`--tracking-*`/`--space-*` + self-host `@font-face`.
- **L3 — semantic/shadcn**: `tokens/globals.css` — `--base-*`(shadcn 롤) + Tailwind v4 `@theme` + `.dark` 전환.

### 계층 매핑표 (L1 그룹 경로 → L2 변수 → L3 롤)

| L1 DTCG 경로 | 값 | L2 변수 (`colors_and_type.css`) | L3 롤 (`globals.css`) |
|---|---|---|---|
| `color.brand.primary` | `#144a46` | `--color-primary` | `--base-primary` · `--base-ring` · `--base-sidebar-primary` · `--base-chart-1` |
| `color.brand.primary-hover` | `#0e3835` | `--color-primary-hover` | (`--color-primary-700`) |
| `color.brand.ink` | `#09110f` | `--color-ink` · `--fg-1` | `--base-foreground` · `--base-card-foreground` · `--base-popover-foreground` |
| `color.brand.background` | `#f3f3f3` | `--color-bg` | `--base-background` |
| `color.brand.surface` | `#ffffff` | `--color-surface` | `--base-card` · `--base-popover` · `--base-surface` · `--base-sidebar` |
| `color.neutral.100` | `#eaeaea` | `--neutral-100` | `--base-muted` · `--base-secondary` · `--base-sidebar-accent` |
| `color.neutral.200` | `#d4d4d4` | `--neutral-200` · `--border-1` | `--base-border` · `--base-input` |
| `color.neutral.600` | `#4c4c4c` | `--neutral-600` · `--fg-2` | `--base-muted-foreground` |
| `color.semantic.success` | `#1c7c70` | `--color-success` | `--base-success` · `--base-chart-3` |
| `color.semantic.warning` | `#c47b2a` | `--color-warning` | `--base-warning` · `--base-accent` · `--base-chart-2` |
| `color.semantic.danger` | `#c44a3a` | `--color-danger` | `--base-destructive` · `--base-error` · `--base-chart-5` |
| `color.semantic.info` | `#2a8a8c` | `--color-info` | `--base-info` · `--base-chart-4` |
| `color.gradient.signature` | `linear-gradient(135deg,#144a46,#09110f)` | `--gradient-signature` | `--gradient-signature` (`.bg-gradient-signature` 유틸) |
| `typography.family.sans` | Pretendard 스택 | `--font-sans` | `--font-sans` (@theme) |
| `typography.letterSpacing.body` | `-0.025em` | `--tracking-body` | `--tracking-body` (:root) |
| `spacing.6` | `1.5rem` | `--space-6` | (Tailwind spacing) |
| `radius.lg` | `16px` | `--radius-lg` | `--radius-lg` (`1rem`) |
| `shadow.signature` | `0 8px 32px rgba(20,74,70,.20)` | `--shadow-signature` | `--shadow-signature` · `.shadow-signature` |
| `motion.duration.fast` | `150ms` | `--duration-fast` | `--duration-fast` (@theme) |

### 계층 드리프트 (L1↔L3 불일치 — 도출 시 관측된 실제 값)

1. **primary 11단계 스케일**: L3 `globals.css`에만 존재. L1 DTCG는 `brand.primary`+hover/active만 보유 → L1로 역추출 시 나머지 8단계는 "L3 파생, DTCG 미수록"으로 표기해야 함.
2. **accent 스케일(`#d99a3f/#c47b2a/#a36322`)**: L3 전용. L1에는 별도 accent 그룹이 없고 `semantic.warning`(#c47b2a)만 있음.
3. **radius sm/md 시프트**: L2 sm=4px vs L3 sm=8px (§4 표). L3가 xs=4px 신설 후 한 단계 밀림.
4. **motion 별칭**: L3가 base/slower/spring/ease-in-out 별칭 추가, 접두도 `--easing-*`(L2)→`--ease-*`(L3).

라운드트립 무결성 검사(L1→L2→L3→L1')는 위 4개 드리프트를 불일치로 보고할 것이므로, 재파생 전 L1을 SSOT로
갱신해야 한다.

---

## 6. FROZEN Rules

원천이 명시적으로 선언한 규칙만 인코딩한다(임의 창작 금지). 출처: `colors_and_type.css` 주석 ·
`globals.css` `[HARD]` 주석 · `02-tokens.json` `$description` · MASTER-BRIEF §1.1·§6.

1. **코어 3색 + surface 변경 금지**: primary `#144a46`, ink `#09110f`, background `#f3f3f3`, surface `#ffffff`. 신규 색상 도입 금지(semantic success/warning/danger/info 4종만 예외). (출처: MASTER-BRIEF §6.3, `colors_and_type.css` L29 "변경 금지")
2. **`#000000` 사용 금지**: 본문 텍스트는 반드시 ink `#09110f`. (출처: MASTER-BRIEF §1.1·§6.6, `02-tokens.json` brand.ink `$description`)
3. **페이지 배경 `#ffffff` 금지**: 페이지 배경은 `#f3f3f3`, `#ffffff`는 surface(카드/모달) 전용. (출처: MASTER-BRIEF §1.1, `colors_and_type.css` L34)
4. **시그니처 그라디언트 단일 정의**: `linear-gradient(135deg, #144a46 0%, #09110f 100%)`. 임의 각도·스톱 신설 금지. (출처: MASTER-BRIEF §6.3, `02-tokens.json` gradient.signature)
5. **Letter-spacing 규칙 준수**: display -0.075em, heading -0.05em, body -0.025~-0.05em, caption 0. (출처: MASTER-BRIEF §1.2·§6.4)
6. **다크모드는 `.dark` 클래스 → CSS 변수 재정의로만** `[HARD]`. `dark:` Tailwind 유틸리티 직접 사용 금지. 다크 primary = `#22938a`. (출처: `globals.css` L24·L294 `[HARD]`, MASTER-BRIEF §6.6)
7. **shadow-signature는 hover 상태 전용**. (출처: `colors_and_type.css` L143, `02-tokens.json` shadow.signature `$description`)
8. **WCAG 2.2 AA** — 본문 ≥ 4.5:1, 큰 텍스트 ≥ 3:1. 팔레트에서 계산한 실측 대비(WCAG 상대휘도 공식):
   - ink `#09110f` on background `#f3f3f3` → **약 17.2:1** (AAA)
   - primary `#144a46` on background `#f3f3f3` → **약 9.0:1** (AAA)
   - `#ffffff` on primary `#144a46` (CTA 텍스트) → **약 10.0:1** (AAA)
   - 다크: primary `#22938a` on background `#0e1513` → **약 4.9:1** (AA 통과, 큰 텍스트/UI)
   - 다크: foreground `#e8eae9` on background `#0e1513` → **약 15.3:1** (AAA)
   > 위 수치는 원천 hex에서 WCAG 공식으로 계산한 값이며 토큰 파일에 저장된 값이 아니다(계산 출처 표기).
9. **메뉴 3개 고정**: 홈 / AI 뉴스 / AI 아카데미. 항목 추가 금지. (출처: MASTER-BRIEF §6.5·§4)
10. **Illustration/mascot policy (v3.0)**: 마스코트 전면 제거. 이미지 부재·빈 상태·로딩·404는 마스코트가 아닌
    **텍스트 + lucide 아이콘**으로 처리. (출처: MASTER-BRIEF §6.1·§6.7)
    > v1.0의 마스코트 사용 규칙("정서 화면 허용")은 폐기됨 — §9·아래 제외 목록 참조.

---

## 7. Voice & copy patterns

출처: MASTER-BRIEF §1.3(브랜드 보이스 v3).

- **선호 어휘**: "오늘의", "5분이면", "AI 워크플로우", "큐레이션", "한 줄 요약", "전문가의 분석", "한국어로", "강의에서 만나요"
- **금지 어휘(마케팅 슬랭)**: "혁신적인", "leverage", "솔루션", "Game-changing", "Cutting-edge", "절대로", "유일한", "최고의"
- **격식 레지스터**: 본문은 "~합니다" 존대. CTA·말풍선은 "~해보세요", "~할까요?" 친근체 혼용.
- **이모지 정책**: 원천(MASTER-BRIEF·04-brand-voice.md)에 명시 없음 → **미확정**. 확정 전에는 UI 카피에 이모지
  사용을 보류한다(본 DESIGN.md 자체도 무이모지).

---

## 8. Component recipes

v3.0에서 유효한 컴포넌트만 수록한다(제외 컴포넌트는 하단 목록). 스니펫은 하드코딩 hex 대신 **L2 토큰 변수**
(`colors_and_type.css`에 실재하는 `var(--…)`)를 참조한다. 원천: `03-components.json` + `globals.css`.

```css
/* Primary CTA — pill + 시그니처 그라디언트 (Button.primary) */
padding: var(--space-3) var(--space-6);
border-radius: var(--radius-pill);
background: var(--gradient-signature);
color: var(--fg-on-primary);
font-weight: var(--fw-bold);
letter-spacing: var(--tracking-body);
transition: all var(--duration-fast) var(--easing-default);
/* hover: box-shadow: var(--shadow-signature);  active: transform: translateY(1px) */

/* Secondary button (Button.secondary) */
background: transparent;
color: var(--color-primary);
border: 1px solid var(--color-primary);
border-radius: var(--radius-md);
/* hover: background: var(--color-primary); color: var(--fg-on-primary) */

/* Card — surface (Card.surface) */
background: var(--color-surface);
border-radius: var(--radius-lg);
padding: var(--space-6);
border: 1px solid var(--neutral-200);
box-shadow: var(--shadow-sm);
transition: all var(--duration-normal) var(--easing-default);
/* hover: box-shadow: var(--shadow-md); transform: translateY(-2px) */

/* Sticky NavBar (glassy) — 메뉴 3개 고정 */
position: sticky; top: 0; height: 64px;
backdrop-filter: blur(12px);
background: color-mix(in srgb, var(--color-bg) 85%, transparent);
border-bottom: 1px solid var(--neutral-200);
/* slots: 로고(logo-4, 28px) · 홈/AI 뉴스/AI 아카데미 · 검색(⌘K)+다크 토글+로그인 */

/* NewsCard (NewsCard) */
background: var(--color-surface);
border-radius: var(--radius-lg);
padding: var(--space-4);
/* image 4:5 or 1:1 · 카테고리 칩 = var(--gradient-signature-soft) · 제목 h3 2줄 clamp · AI 요약 1줄 · 출처+시각 */

/* EditorPick — 풀-블리드 그라디언트 (EditorPick) */
background: var(--gradient-signature);
color: var(--fg-on-primary);
border-radius: var(--radius-xl);
padding: var(--space-8);
/* image 16:9 */

/* CourseCard (CourseCard) */
background: var(--color-surface);
border-radius: var(--radius-lg);
padding: var(--space-6);
/* thumbnail · 난이도 배지 · 제목 · 수강자수 · 강사 아바타 · CTA */

/* Input (Input) */
background: var(--color-surface);
color: var(--color-ink);
border: 1px solid var(--neutral-300);
border-radius: var(--radius-md);
padding: var(--space-3) var(--space-4);
letter-spacing: var(--tracking-body);
/* focus: border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--border-focus-ring) */

/* Empty state (v3.0) — 마스코트 금지, 텍스트 + lucide 아이콘 */
text-align: center;
padding: var(--space-16) var(--space-6);
/* lucide 아이콘(primary 색) + 헤드라인 + 보조 카피 + CTA. 마스코트 이미지 사용 금지 */

/* Section eyebrow */
font-family: var(--font-mono);
font-size: var(--text-xs);
font-weight: var(--fw-semibold);
color: var(--color-primary);
letter-spacing: 0.08em;
text-transform: uppercase;

/* Signature divider (Divider.signature) */
height: 2px;
background: var(--gradient-signature);
/* 양 끝에 circle 8px (white, 1px outline) 마커 */
```

**제외된 v1.0 컴포넌트 (03-components.json에 있으나 v3.0 미사용)**: `CXSeven`(CX 7원칙 인포그래픽),
`BetaForm`(베타 신청 스테퍼), `ServiceCard`(출시 예정 6서비스 카드), `DashboardCard`(모두의 프로젝트 허브),
`Hero`의 mascot 슬롯, `EmptyState`의 mascot 슬롯, `Footer`의 "CX 7원칙 요약"·"운영진 SNS 카드" 슬롯,
`Badge`의 `beta` variant, `page-templates`의 `Landing`/`ProjectsHub`/`BetaApply`.

---

## 9. Asset index

로고 변형 매트릭스. 파일명은 `assets/` 실제 파일 + `preview/logos.html`·`preview/mascots.html`의
`@dsCard`·라벨과 대조 검증했다. **마스코트 변형(logo-3/5/6)은 파일은 존재하나 v3.0 정체성에서 제거되어
"미사용"이다** — 업로드 후 마스코트로 해석하지 말 것.

| 파일 | 락업 | 배경 | 의도된 용도 | v3.0 상태 |
|---|---|---|---|---|
| `moai-logo-4.png` | 가로형(horizontal) | light | 헤더·네비 (로고 28px 높이) | **사용** |
| `moai-logo-4-WH.png` | 가로형 화이트 녹아웃 | dark / gradient | 어두운·그라디언트 배경 위 헤더 | **사용** |
| `moai-logo-1.png` | 정사각(square) | light | 파비콘·앱 아이콘·소셜 프로필 | **사용** |
| `moai-logo-1-WH.png` | 정사각 화이트 녹아웃 | dark / gradient | 어두운 배경 위 정사각 | **사용** |
| `moai-logo-2.png` | 카드 그라디언트 락업 | light / gradient | 카드·공유 이미지 (보조) | 사용(보조) |
| `moai-logo-2-1.png` | 카드 모노 락업 | 임의 | 단색 카드·워터마크 (보조) | 사용(보조) |
| `moai-logo-2-mono.png` | 카드 모노 (e-ink 1비트) | e-ink / 흑백 | e-ink·흑백 인쇄 템플릿 전용 | 사용(특수 매체) |
| `moai-logo-3.png` | 마스코트 메인 ('ㄹ' 로봇 머리+안테나) | soft | (v1.0) 히어로·빈상태·404 | **v3.0 미사용 — 정체성 제거** |
| `moai-logo-5.png` | 마스코트 alt | soft | (v1.0) 마스코트 대체 | **v3.0 미사용** |
| `moai-logo-6.png` | 글로벌 마스코트 | soft | (v1.0) 글로벌 마스코트 | **v3.0 미사용** |

> DTCG `logo` 그룹(`02-tokens.json`)은 header=logo-4, header-dark=logo-4-WH, square=logo-1,
> square-dark=logo-1-WH, mascot=logo-3, mascot-alt=logo-5, global-mascot=logo-6, card=logo-2,
> card-mono=logo-2-1로 매핑한다. mascot 3종은 위 표대로 v3.0에서 미사용이다.
>
> **미제공 변형**: SVG 벡터 로고는 번들에 없음(PNG만) → "미제공"으로 표기(임의 생성 금지).
> 폰트 바이너리는 라이선스 이유로 스테이징 제외(§10 / UPLOAD-GUIDE.md 참조).

---

## 10. Upload guide

업로드 우선순위: **DESIGN.md → tokens/(L1 DTCG → L2 CSS → L3 globals) → assets/ 로고 변형 → 참고 자산**.
실제 업로드 절차·수동/자동 경로는 `moai-designer:design-sync-upload` 소관이며, 이 스테이징 폴더의
`UPLOAD-GUIDE.md`에 THIS 번들 기준으로 상세히 기재했다(대상 프로젝트 id, `/design-login` 전제, 분석 대기
시간, Published 토글, 폰트 라이선스 제외 사유 포함).

Published 토글: 업로드 → 5–15분 분석 대기 → 테스트 프롬프트로 검증(브랜드 일치) → 일치 시 ON, 어긋나면
Remix 또는 자산 추가.

---

_생성: cd-system-prep 파이프라인 (수동 폴백 경로). 정체성 기준 MASTER-BRIEF v3.0. 모든 값은
`tokens/`·`assets/` 원천 파일 추적 가능._
