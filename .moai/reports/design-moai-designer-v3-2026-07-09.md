# MoAI Designer 플러그인 재설계 v3 — 청사진

- 작성: 2026-07-09 (session 4fd44ef5)
- 입력 자료: `handoff.zip` (MoAI 자체 디자인 시스템 Claude Design design-sync 번들, 128파일/18MB, `/tmp/handoff-20260709/`)
- 선행: `design-moai-plugin-v2-2026-07-08.md` (4-plugin 패밀리 V2). 본 문서는 moai-designer 단일 플러그인의 **재설계 청사진**.

---

## 1. 사용자 결정 (4축, 2026-07-09 확정)

| 축 | 결정 |
|---|---|
| zip 활용 | **A — 파이프라인 실증** (cd-system-prep/cd-handoff-reader로 zip 처리, www 코드 변경 없음) |
| 정체성 | **zip의 구성(구조·패턴)을 참고해 새 DESIGN.md 요소 제작** (v1.0/v3.0 내용물 그대로 변환 X) |
| 업로드 | **C — 자동 우선 + 수동 폴백** (DesignSync MCP 자동, 인증/실패 시 수동 산출) |
| 깊이 | **B — 플러그인 전면 재설계** (아키텍처 재검토 + 스킬 재편) |

---

## 2. handoff.zip 3계층 토큰 아키텍처 — 새 DESIGN.md 요소의 참고 청사진

zip은 **동일 브랜드 토큰(#144a46/#09110f/#f3f3f3 + 시그니처 그라디언트)**을 3계층으로 인코딩. 이 계층화가 새 DESIGN.md 생성 스킬의 구조적 모델.

### Layer 1 — DTCG SSOT (`assets/round3/02-tokens.json`)
- W3C Design Tokens 포맷 (`$value` / `$type` / `$description`)
- 계층적 그룹: `color.{brand,neutral,semantic,dark,gradient}` · `typography.{family,weight,size,lineHeight,letterSpacing}` · `spacing` · `radius` · `shadow` · `motion.{duration,easing}` · `container` · `logo`
- 각 토큰에 `$description` (출처/의미) → 브랜드 진실 원천
- `$updatedAt: 2026-04-25`, "Notion 가이드라인 Ver 1.0"

### Layer 2 — 원시 CSS 변수 (`colors_and_type.css`)
- `--color-primary` / `--color-ink` / `--color-bg` / `--color-surface` / `--neutral-50..950` / `--tracking-display-tight(-0.075em)` ...
- self-host `@font-face` Pretendard 9 weights + Inter/JetBrains Mono CDN
- 용도: Claude Design 카드 / 단일 파일 HTML 렌더

### Layer 3 — Semantic/shadcn (`assets/round3/globals.css` + `round3/styles.css`)
- `--base-*` 의미 롤: `background` / `foreground` / `card` / `popover` / `surface` / `muted` / `primary` / `secondary` / `accent` / `destructive` / `border` / `input` / `ring` / `border-strong` / `chart-1..5` / `sidebar-*`
- Tailwind v4 `@theme` + `@layer base/utilities`
- `.dark` 클래스 → CSS 변수 전환으로만 다크모드 (`[HARD] dark: Tailwind 유틸리티 직접 사용 금지`)
- 용도: www 프로덕션 코드 소비 (shadcn 체계)

### FROZEN 규칙 인코딩 (각 계층 코멘트/규칙)
- `#000000` 절대 금지 → `#09110f` (ink)
- 마젠타/퍼플/오렌지 그라디언트 금지 → 시그니처 청록 단일
- 그라디언트 + shadow 동시 적용 금지 (시각 노이즈)
- 풀 블리드 이미지 배경 금지 → `#f3f3f3` 단색
- All-caps 한국어 금지 · 영문 약어 UPPER 허용
- 마스코트 데이터 표/폼/결제 화면 금지 — 정서 영역 한정
- 둥근 보더 + 좌측 컬러 액센트 카드 패턴 금지 (AI 슬롭)
- Inter/Roboto/Arial 본문 금지 → Pretendard
- 한국어 자간: 디스플레이 -75 / 헤딩 -50 / 본문 -25 / 캡션 0
- 이모지 금지 (마스코트가 정서 앵커)

### DESIGN.md = SKILL.md 패턴 (번들 최상위 `project/SKILL.md`)
8섹션: (1) README 통독 (2) Tokens 항상 import (3) FROZEN Rules (4) 한국어 카피 7가지 (5) 컴포넌트 레시피 5종 (6) UI Kits (7) Lucide+Logo 사용 (8) 변경 프로세스.
→ DESIGN.md 자체가 "에이전트가 디자인할 때 따르는 스킬"로 설계됨.

### 정체성 충돌 (drift — 구성 참고 시 유의)
- `landing.html`(website kit) = **v1.0**: CX7원칙 + 베타 CTA + 6서비스 + 마스코트 + "모두를 위한 AI" + 메뉴 5개
- `round3/` 6페이지 = **v3.0**: 뉴스/아카데미 2서비스, 메뉴 3개, 마스코트 제거
- 시각 토큰(3색/그라디언트/자간)은 양쪽 공통 FROZEN — 카피/정체성만 상이
- **처리**: 내용물(v1/v3 카피) 그대로 복사 X. 3계층 구조 + FROZEN 패턴만 새 DESIGN.md 요소의 청사진으로 차용.

---

## 3. 새 DESIGN.md 생성 요소 (cd-system-prep 진화)

기존 cd-system-prep DESIGN.md 템플릿(6섹션: voice/color/typo/spacing/components/constraints) → **zip 구성 기반 강화 템플릿**:

1. **Brand voice & personality** — 형용사 5-7 + 한 문단 (기존 유지)
2. **Color palette** — primary 스케일(50-950) + semantic + **시그니처 자산(그라디언트) 명시**
3. **Typography** — family/weight/size/lineHeight/**letter-spacing(자간 규칙)** + 굵기 대비 패턴
4. **Spacing / Radius / Shadow / Motion** — 체계적 스케일 (zip 4섹션 대응)
5. **Token 3계층 매핑** — DTCG SSOT / CSS 변수 / semantic 롤 (zip L1-L3 대응) ← **신규**
6. **FROZEN Rules** — 명시적 금지 + 자간 + WCAG + 마스코트 정책 ← **신규 (zip 패턴 차용)**
7. **Voice & 카피 패턴** — 선호/금지 어휘, 존대/친근체, 이모지 정책 ← **강화**
8. **컴포넌트 레시피** — 자주 쓰는 N개 CSS 스니펫 (Primary CTA / Card / Sticky nav / Empty state / Eyebrow) ← **신규**
9. **자산 인덱스** — 로고 변형 매트릭스(가로/정사각/마스코트/WH) + 용도 ← **신규**
10. **업로드 가이드** — DesignSync 자동 / 수동 양경로 ← **강화**

---

## 4. 스킬 재편 (전면 재설계)

### 네임스페이스 정정 (전역, HARD)
`moai-design:` → `moai-designer:` (기존 스킬 본문/관련 스킬 참조 전수). 사용자 발화 "moai-cowork:design-system-library"도 정정 대상(실제는 moai-designer 소속).

### 4클러스터 재편 (초안 — builder-harness 정제)

| 클러스터 | 스킬 | 비고 |
|---|---|---|
| **Input/분석** | `cd-handoff-reader` (번들→토큰 추출) · `cd-system-prep` **진화** (자산→DESIGN.md, 새 템플릿) | 핵심 파이프라인 |
| **Library/토큰** | `design-system-library` (75 브랜드 유지) · **신설 `design-tokens-transformer`** (DTCG↔CSS↔shadcn 3계층 변환) | zip L1-L3 변환 자동화 |
| **Output/업로드** | **신설 `design-sync-upload`** (DesignSync 자동 + 수동 폴백) · `moai-domain-design-handoff` | Q3=C 양경로 |
| **Workflow/프롬프팅** | `moai-workflow-design` (Path A/B) · `cd-brief` · `cd-prompt-builder` · `cd-slop-check` · `moai-workflow-gan-loop` · `moai-domain-brand-design` · `moai-domain-copywriting` | 기존 유지 |

### 커맨드
`/design` (통합 진입) · `/tokens` · `/import` · **`/upload` (신규)** · `/brief` · `/check` · `/system`

---

## 5. 위임 계획

| 단계 | 위임처 | 범위 |
|---|---|---|
| 구조 재설계 | `builder-harness` | 스킬 이동/이름/신규 스캐폴드, plugin.json, 커맨드 디스패치, 네임스페이스 정정. body는 구조+핵심절차만 (body 본문 작성은 builder-harness 범위 밖 — metadata 전문) |
| 핵심 body 콘텐츠 | `general-purpose` (또는 직접) | 3개 핵심 스킬 도메인 body: cd-system-prep 진화 템플릿, design-tokens-transformer 절차, design-sync-upload 절차 |
| 파이프라인 실증 | 오케스트레이터 직접 | zip → DESIGN.md 산출 |
| DesignSync 업로드 | 오케스트레이터 직접 | /design-login 의존 |

---

## 6. 제약 / 검증

- **www 코드 변경 금지** (Q1=A)
- 기존 스킬 역할 보존 (재편이지 삭제 아님)
- 검증: zip 파이프라인 실증 산출물(DESIGN.md) 품질 · 네임스페이스 정정 grep · marketplace.json 정합 · 스킬 로드

---

## Sources

- `handoff.zip` 내: `project/SKILL.md` · `project/README.md` · `project/colors_and_type.css` · `project/assets/round3/{globals.css,02-tokens.json,03-components.json,00-MASTER-BRIEF-v3.md}` · `project/ui_kits/website/landing.html` · `project/_ds_manifest.json`
- 기존: `plugins/moai-designer/skills/{cd-system-prep,design-system-library,moai-workflow-design,cd-handoff-reader}/SKILL.md` · `.claude-plugin/marketplace.json` · `design-moai-plugin-v2-2026-07-08.md`
