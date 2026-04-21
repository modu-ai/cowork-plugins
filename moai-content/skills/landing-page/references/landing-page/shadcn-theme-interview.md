# shadcn/ui 테마 인터뷰 프로토콜 (v1.4.0)

HTML·웹 산출물을 생성하기 전, MoAI 오케스트레이터가 **AskUserQuestion** 도구로 shadcn/ui 기반 테마·효과를 사용자에게 물어봅니다. 본 문서는 인터뷰 설계도이자 구현 계약서입니다.

> Source of truth: https://ui.shadcn.com/docs/theming · https://ui.shadcn.com/docs/skills

---

## 1. 원칙 (HARD)

- [HARD] HTML/웹 산출물을 생성하는 모든 스킬(`landing-page`, `product-detail`, `data-visualizer`)은 코드 생성 전에 **이 인터뷰를 먼저 실행**한다.
- [HARD] 사용자가 명시적으로 다른 프레임워크를 지정하지 않는 한 기본 스택은 **shadcn/ui + Tailwind CSS v4 + React/Next.js**다.
- [HARD] 모든 색상 토큰은 **OKLCH 포맷**으로 `:root` + `.dark` 블록에 출력한다.
- [HARD] AskUserQuestion 호출 규칙을 따른다:
  - 질문·헤더·옵션에 이모지 금지
  - 옵션은 2~4개 (최대 4개)
  - 한 번에 최대 4개 질문
  - `conversation_language`(Korean) 기준 한글 문구 사용
- [HARD] 질문은 **소크라테스식**으로 설계한다 — 목적·상황·제약을 먼저 드러내고 선택지를 비교 가능하게 제시한다.

---

## 2. 기본 인터뷰 (4문항 · 1회 호출)

아래는 AskUserQuestion payload의 설계 명세다. 실제 호출 시에는 스킬이 요청받은 페이지 유형(랜딩/상세/대시보드)에 맞춰 `question` 문구를 약간 조정할 수 있다.

### Q1. 베이스 팔레트

- **header**: `Base palette`
- **question**: `어떤 분위기의 베이스 팔레트로 제작할까요? (shadcn/ui 공식 베이스 컬러)`
- **options**:
  1. `Neutral — 순수 그레이, 범용 (Recommended)` · Description: `어떤 브랜드에도 어울리는 중립 팔레트. 콘텐츠가 주인공이 되는 깨끗한 화면.`
  2. `Zinc — 쿨 그레이, SaaS·테크` · Description: `푸른 기운의 쿨 그레이. SaaS·개발자·B2B 제품에 최적.`
  3. `Stone — 따뜻한 베이지` · Description: `따뜻한 베이지-그레이. 브랜드·웰빙·럭셔리 톤에 적합.`
  4. `Slate — 블루 그레이, 금융·기업` · Description: `깊이 있는 블루 그레이. 금융·컨설팅·엔터프라이즈 톤.`

> 대안 팔레트(Rose / Blue / Green / Orange / Red / Violet / Yellow / Mauve / Olive / Mist / Taupe)는 사용자가 "Other"로 응답하거나 브랜드 컨텍스트에 명시된 경우에만 적용한다.

### Q2. 컬러 모드

- **header**: `Color mode`
- **question**: `라이트/다크 모드 전략은 어떻게 할까요?`
- **options**:
  1. `System + Toggle (Recommended)` · Description: `OS 설정을 따르면서도 헤더에 수동 토글 제공. 접근성·사용자 선호 모두 충족.`
  2. `Light only` · Description: `밝은 테마 전용. 랜딩·영업 페이지에서 가장 안전한 선택.`
  3. `Dark only` · Description: `어두운 테마 전용. 크리에이티브·게임·기술 제품의 강렬한 몰입감.`
  4. `Auto (system)` · Description: `OS 설정만 따라가고 토글은 제공하지 않음. UI를 최소화하고 싶을 때.`

### Q3. 모서리 반경 (Radius)

- **header**: `Radius`
- **question**: `컴포넌트 모서리 반경은 어느 정도로 할까요? (--radius 토큰)`
- **options**:
  1. `Balanced 0.5rem (Recommended)` · Description: `shadcn 기본값. 어떤 분위기에도 무난.`
  2. `Sharp 0rem` · Description: `각진 모서리. 전문·테크·아카이브 느낌.`
  3. `Soft 0.75rem` · Description: `부드럽고 친근. 컨슈머·B2C·교육·웰빙 톤.`
  4. `Pill 1rem+` · Description: `완전 둥근 플레이풀 감성. 라이프스타일·게임·커뮤니티.`

### Q4. 인터랙션 & 효과 (multiSelect)

- **header**: `Effects`
- **multiSelect**: `true`
- **question**: `어떤 모션·인터랙션 효과를 포함할까요? (복수 선택 가능)`
- **options**:
  1. `Framer Motion 페이드업` · Description: `히어로·섹션 진입 시 자연스러운 fade-up. 전환율 상승에 가장 기여도가 높음.`
  2. `스크롤 리빌 (Scroll reveal)` · Description: `스크롤하면서 카드·이미지가 등장. 롱폼 페이지에 적합.`
  3. `패럴랙스 배경` · Description: `히어로 배경 레이어 이동. 비주얼 임팩트가 필요한 브랜드 페이지.`
  4. `차트·대시보드` · Description: `Recharts·Chart.js·Tremor로 데이터 시각화 섹션 포함. 데이터 스토리텔링 페이지에 필수.`

---

## 3. 조건부 후속 질문 (Q5) — 차트 선택 시

Q4에서 `차트·대시보드`가 선택된 경우에만 AskUserQuestion을 한 번 더 호출한다.

- **header**: `Chart stack`
- **question**: `차트/대시보드는 어떤 라이브러리로 구현할까요?`
- **options**:
  1. `Recharts (Recommended)` · Description: `shadcn/ui Chart 컴포넌트의 공식 기반. React·타입 안전·반응형. 대부분의 B2B 대시보드에 최적.`
  2. `Chart.js` · Description: `Canvas 기반, 풍부한 플러그인. HTML 단독 페이지(React 없음)에서 가장 가벼움.`
  3. `Tremor` · Description: `KPI 카드·AreaChart·BarChart 프리셋. 마케팅·영업 대시보드에 빠르게 완성도를 내고 싶을 때.`
  4. `ECharts` · Description: `지도·Sankey·TreeMap 등 고난도 시각화. 탐색형 분석 화면에서 진가 발휘.`

---

## 4. 인터뷰 결과 → Design Spec 주입

선택 결과는 기존 `design-spec.yaml`의 `theme` 섹션에 다음 형식으로 주입한다.

```yaml
design-spec:
  version: "1.4.0"
  theme:
    system: "shadcn/ui"
    base: "neutral"            # Q1: neutral | zinc | stone | slate | rose | ...
    mode: "system+toggle"      # Q2: system+toggle | light | dark | auto
    radius: "0.5rem"           # Q3
    effects:                   # Q4 (multi)
      - "fade-up"
      - "scroll-reveal"
    chart_lib: "recharts"      # Q5 (조건부): recharts | chartjs | tremor | echarts | null
    css_vars_format: "oklch"   # HARD: 항상 oklch
    tailwind_version: "v4"
  # ... 기존 color_tokens, typography, spacing 등은 shadcn 베이스로 재산출
```

---

## 5. 산출물 기본 스택

모든 HTML/웹 스킬은 별도 지정이 없으면 다음 스택으로 출력한다:

| 항목 | 기본값 |
|------|-------|
| 프레임워크 | Next.js 15 (App Router) + React 19 |
| 스타일 | Tailwind CSS v4 (CSS variables 모드) |
| 컴포넌트 | shadcn/ui (Radix 기반) |
| 아이콘 | Lucide React |
| 애니메이션 | Framer Motion (선택 시) |
| 폰트 | Pretendard (KR) + Inter (EN) |
| 차트 | Recharts (선택 시) |

단일 HTML 파일 산출이 필요한 경우(스마트스토어 업로드, 임시 공유용)에는 Tailwind CDN + shadcn/ui 스타일 변수만 인라인 삽입하는 경량 모드로 전환한다.

---

## 6. 필수 산출물 구성

인터뷰 완료 후 스킬은 다음 파일들을 함께 제공한다:

1. **`components.json`** — shadcn CLI 초기화 파일 (선택된 base, tailwind 설정 반영)
2. **`app/globals.css`** — OKLCH CSS 변수 `:root` + `.dark` 블록
3. **`tailwind.config.ts` 또는 `@theme` 블록** — Tailwind v4 토큰 매핑
4. **컴포넌트 파일들** — `shadcn add <component>` 호환 구조
5. **`README-setup.md`** — 설치·개발 서버 실행 안내, 필요한 shadcn 컴포넌트 목록
6. **(옵션) Framer Motion 래퍼** — 선택된 효과 프리셋

---

## 7. shadcn CSS 변수 출력 템플릿 (Neutral 예시)

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --radius: 0.5rem;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
}
```

각 베이스(Zinc/Stone/Slate/Rose/…)별 토큰 값은 [shadcn 공식 테마 문서](https://ui.shadcn.com/docs/theming)의 해당 프리셋을 그대로 사용한다. 스킬은 선택된 base 값을 그대로 `shadcn init --base-color <선택값>`에 전달할 수 있어야 한다.

---

## 8. 브랜드 컨텍스트와의 조화

사용자 프로젝트에 기존 브랜드 컬러가 있는 경우:

1. Q1에서 선택된 shadcn base를 **뉴트럴 스캐폴드**로 사용
2. `--primary`, `--accent`, `--ring` 세 토큰만 브랜드 컬러(oklch 변환)로 오버라이드
3. 나머지 semantic 토큰(`background`, `muted`, `border`)은 shadcn 베이스 유지
4. 결과: 브랜드 정체성 + shadcn의 접근성·일관성 동시 확보

---

## 9. 스킬별 적용 포인트

| 스킬 | 적용 시점 | 특이사항 |
|------|---------|--------|
| `landing-page` | 카피 수집 전/후 모두 가능하나 **코드 생성 직전 필수** | 섹션 템플릿을 shadcn 블록(Hero, Features, Pricing, FAQ)으로 맵핑 |
| `product-detail` | 플랫폼 선택 직후 | 스마트스토어/쿠팡용 HTML 단일 파일 모드에서도 CSS 변수는 shadcn 스펙 준수 |
| `data-visualizer` | 차트 방식 결정 후 | Q5에서 선택된 라이브러리가 대시보드 HTML의 기본 차트 라이브러리가 됨 |

---

## 10. Fallback — 인터뷰를 생략해야 할 때

아래 상황에서는 **인터뷰를 묻지 않고 기본값**(Neutral / System+Toggle / 0.5rem / fade-up)을 즉시 적용한다:

- 사용자가 `--quick` 또는 "빠르게"·"그냥 기본"이라고 명시
- 이전 대화에서 이미 테마 선택을 완료한 경우(동일 세션)
- 샘플·프로토타입 목적임이 명시된 경우
- MoAI 내부 워크플로우에서 자동 실행 중이고 사용자 응답을 기다리지 않는 컨텍스트

기본값을 적용할 때는 응답 상단에 `기본 테마를 적용했습니다 (neutral / system+toggle / 0.5rem / fade-up). 변경하려면 "테마 바꿔줘"라고 말해 주세요.`를 고지한다.

---

Version: 1.0.0 (신규 — v1.4.0 도입)
Last Updated: 2026-04-16
