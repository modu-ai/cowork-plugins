---
name: design-system-library
description: |
  75개 글로벌 브랜드 디자인 시스템(Claude · ClickHouse · Clay 포함)을 단일 파일 HTML 산출물에 적용합니다. 각 시스템의 토큰(색·타이포·radius·spacing·컴포넌트)을 Tailwind Play CDN config + shadcn 스타일 vanilla 컴포넌트로 변환해 렌더합니다.
  html-report · 랜딩 페이지 · 각종 문서 생성 시 design_system을 지정하면 해당 브랜드 무드가 즉시 적용됩니다. Claude Design 핸드오프 시에는 DESIGN.md 지침 소스로 제공됩니다.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude 스타일로 HTML 보고서 만들어줘"
  - "ClickHouse 다크 테마로 랜딩 만들어줘"
  - "Clay 디자인 시스템 적용해서 문서 생성"
  - "브랜드 디자인 시스템 골라서 HTML로"
  - "Notion / Linear / Stripe 스타일로 리포트"
  - "어두운 테마 / 따뜻한 화이트 테마로"
  - "Claude Design에 올릴 디자인 시스템 자료 정리"
user-invocable: true
version: 2.27.0
---

# design-system-library — 75개 브랜드 디자인 시스템 SSOT

## 목적과 범위

글로벌 브랜드 75종(56개 풍부 분석 + 19개 경량 토큰)의 디자인 시스템(token 기반 분석 결과)을 단일 진실 원천(single source of truth)으로 보관하고, HTML 산출물에 적용 가능한 형태로 제공합니다.

**두 가지 소비 경로**:
1. **html-report / HTML 문서 렌더** — `design_system` 파라미터로 시스템 선택 → Tailwind Play CDN config + shadcn vanilla 컴포넌트로 단일 파일 HTML 렌더
2. **Claude Design 핸드오프** — `claude-design-system-prep`가 본 라이브러리 시스템을 DESIGN.md 합성 소스로 사용 → `design-handoff`의 references/context에 지침 포함

**핵심 원칙**:
- 라이브러리는 데이터(token + 분석) SSOT — 렌더 로직은 소비자(html-report)가 소유
- Tailwind Play CDN으로 단일 파일·외부 빌드 없이 브랜드 토큰 적용 (인터넷 연결 필요)
- shadcn 컴포넌트는 React가 아닌 **vanilla HTML/CSS로 재현** (단일 파일·React 불필요)
- 기존 html-report 0의존 템플릿은 유지 — design_system 미지정 시 하위 호환

---

## 3개 기본 테마 (Default)

모든 HTML 산출물의 기본 선택지. 사용자가 명시하지 않아도 결과물 성격에 따라 자동 추천합니다.

| 테마 | 무드 | 캔버스 | 강조 | 폰트 | 적합 산출물 |
|------|------|--------|------|------|-------------|
| **`claude`** | warm editorial (default) | cream `#faf9f5` | coral `#cc785c` | Copernicus serif + StyreneB sans | 보고서·사업계획서·편집성 문서 |
| **`clickhouse`** | high-contrast engineering | near-black `#0a0a0a` | electric yellow `#faff69` | Inter 700 | 기술 리포트·데이터 대시보드·개발자 문서 |
| **`clay`** | playful B2B | cream `#fffaf0` | 6-color saturated cards (pink/teal/lavender/peach/ochre) | Plain Black/Inter | 랜딩·마케팅·제품 소개 |

상세 토큰: [`systems/anthropic-claude.md`](systems/anthropic-claude.md) · [`systems/clickhouse.md`](systems/clickhouse.md) · [`systems/clay.md`](systems/clay.md)

### 자동 추천 휴리스틱

| 산출물 | 추천 테마 |
|--------|-----------|
| 주간 현황·경영 요약·사업계획서 | `claude` (warm editorial) |
| 인시던트 리포트·데이터 리포트·API 문서 | `clickhouse` (다크 엔지니어링) |
| 랜딩·제품 소개·마케팅 원고 | `clay` (playful saturated) |
| 재무제표·법률 문서 | `claude` (편집성·신뢰) |

---

## 전체 75개 카탈로그

[`systems/registry.md`](systems/registry.md) 참조 — 분류(light/warm/dark) · 캔버스 · primary 색 · 폰트 · 무드 메타 포함.

전체 75개 시스템(56개 풍부 분석 + 19개 경량 토큰 ⚙️) — 각 `systems/<name>.md`에 토큰 보관, `registry.md`에 휘도 기반 분류(light 48 · dark 25 · warm 2)·메타 표기. 기본 3테마(claude/clickhouse/clay)는 Tailwind 매핑 검증 완료. 19개 경량(⚙️)은 `테마_컴포넌트_쇼케이스_전체.html`에서 추출 — 풍부한 분석·typography 스케일은 추후 보강.

---

## Tailwind Play CDN 통합

[`mapping/tailwind.md`](mapping/tailwind.md) 참조 — YAML design token → Tailwind CDN inline config 매핑 규칙 + shadcn vanilla 컴포넌트 변환표.

**핵심 패턴** (단일 파일 HTML 내):

```html
<!-- 1. Tailwind Play CDN -->
<script src="https://cdn.tailwindcss.com"></script>
<!-- 2. 브랜드 토큰 → tailwind.config 주입 -->
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: { primary: '#cc785c', canvas: '#faf9f5', /* ... */ },
        fontFamily: { display: ['Copernicus', 'serif'], sans: ['StyreneB', 'Inter', 'sans-serif'] },
        borderRadius: { md: '8px', lg: '12px', xl: '16px' },
        spacing: { section: '96px', /* ... */ }
      }
    }
  }
</script>
<!-- 3. shadcn vanilla 컴포넌트 (utility class로 직접 마크업) -->
<div class="bg-canvas rounded-lg border border-hairline p-8">
  <h2 class="font-display text-3xl tracking-tight text-ink">...</h2>
</div>
```

---

## shadcn vanilla 컴포넌트

[`components/`](components/) — shadcn UI 컴포넌트를 React 없이 vanilla HTML + Tailwind utility로 재현한 참조 마크업.

| 컴포넌트 | shadcn 원본 | vanilla 매핑 |
|----------|-------------|--------------|
| Card | `Card` / `CardHeader` / `CardContent` | `div.rounded-lg.border.p-8` + token classes |
| Button | `Button` (variant: default/secondary/ghost) | `button.inline-flex.rounded-md.px-5.py-3` + variant class |
| Badge | `Badge` | `span.inline-flex.rounded-full.px-3.py-1.text-xs` |
| Table | `Table` / `TableHeader` / `TableRow` | semantic `table.thead.tbody.tr` + token borders |
| Tabs | `Tabs` / `TabsList` | `<details>` 또는 vanilla JS tab + token classes |
| Alert | `Alert` | `div.rounded-lg.border.p-4` + semantic color |

각 컴포넌트의 풀 마크업(변형·접근성 메모 포함)은 개별 파일 — [`card.md`](components/card.md) · [`button.md`](components/button.md) · [`badge.md`](components/badge.md) · [`table.md`](components/table.md) · [`tabs.md`](components/tabs.md) · [`alert.md`](components/alert.md). 토큰 매핑 규칙은 [`mapping/tailwind.md`](mapping/tailwind.md) §1·§3.

---

## 소비자 연동

### html-report (moai-content)

`moai-content:html-report`에 `design_system` 입력 파라미터 추가:
- 미지정 → 기존 0의존 템플릿 (Anthropic 영감 ivory/slate/clay, 하위 호환)
- `design_system: claude|clickhouse|clay|<75개 중>` → 본 라이브러리에서 토큰 로드 → Tailwind Play CDN + shadcn vanilla 렌더

체인 예시:
```
[텍스트 스킬] → ai-slop-reviewer → html-report (design_system: clickhouse)
```

### Claude Design 핸드오프 (moai-design)

`claude-design-system-prep`가 사용자가 지정한 시스템(또는 브랜드 무드 매칭)을 본 라이브러리에서 로드 → DESIGN.md 합성. `design-handoff`의 references.md / context.md에 design-system 지침으로 포함되어 claude.com Design 세션에 paste.

---

## 워크플로우

1. **시스템 선택** — 사용자 명시 또는 산출물 성격 기반 자동 추천(위 휴리스틱)
2. **토큰 로드** — `systems/<name>.md`의 YAML frontmatter(colors/typography/rounded/spacing/components) 파싱
3. **Tailwind config 생성** — `mapping/tailwind.md` 규칙으로 `tailwind.config` 객체 생성
4. **shadcn vanilla 매핑** — 산출물 구조 카드/버튼/테이블을 `components/` 참조 마크업으로 치환
5. **단일 파일 렌더** — CDN script + config + 마크업을 단일 `.html`로 출력

---

## 사용 예시

**예시 1: ClickHouse 다크 테마 기술 리포트**
```
결제 게이트웨이 502 장애를 ClickHouse 스타일 다크 테마로 인시던트 리포트 HTML로 만들어줘.
```

**예시 2: Claude warm 테마 사업계획서**
```
사업계획서를 Claude 디자인(warm cream + coral) HTML로 렌더해줘.
```

**예시 3: Clay playful 테마 랜딩**
```
신제품 랜딩 페이지를 Clay 스타일(컬러 카드)로 HTML로 만들어줘.
```

**예시 4: Claude Design 핸드오프용 시스템 정리**
```
Claude Design에 올릴 디자인 시스템 자료를 Linear 스타일 기반으로 정리해줘.
```

---

## 하지 않는 것

- 본 라이브러리는 렌더 로직을 소유하지 않습니다 — 렌더는 html-report가 담당
- React / Vue / 빌드 단계를 도입하지 않습니다 — 단일 파일·CDN·vanilla 고수
- 0의존 self-contained 출력을 요구하는 경우(이메일 첨부·오프라인·인쇄)는 기존 html-report 템플릿을 사용하세요 (design_system 미지정)
- 브랜드 저작권 — 각 시스템은 분석·참고용 token이며, 상용 사용 시 원본 브랜드 가이드라인을 준수해야 합니다

---

## 참고 문서

- [`systems/registry.md`](systems/registry.md) — 75개 전체 카탈로그 인덱스
- [`systems/anthropic-claude.md`](systems/anthropic-claude.md) · [`systems/clickhouse.md`](systems/clickhouse.md) · [`systems/clay.md`](systems/clay.md) — 기본 3테마 상세 토큰 (claude.md는 `CLAUDE.md` 자동 로드 회피를 위해 `anthropic-claude.md`로 명명)
- [`mapping/tailwind.md`](mapping/tailwind.md) — YAML 토큰 → Tailwind CDN config 매핑 규칙
- [`components/`](components/) — shadcn vanilla 컴포넌트 참조 마크업
