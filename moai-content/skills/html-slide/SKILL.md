---
name: html-slide
description: |
  발표용 슬라이드 덱을 브라우저에서 바로 열리는 단일 파일·자체 완결형(self-contained) HTML로 만들어 드립니다. 인포그래픽(차트·다이어그램·KPI)은 한국어 숫자·라벨이 100% 정확한 인라인 SVG로 직접 렌더링하고, 실사 히어로·일러스트 이미지는 Higgsfield MCP 또는 codex(gpt-image-2)로 생성합니다. 필요 시 pptx-designer 체이닝으로 PowerPoint에서 편집 가능한 .pptx까지 병행 산출합니다.
  다음과 같은 요청 시 사용하세요:
  - "발표 슬라이드 HTML로 만들어줘"
  - "키노트 덱 단일 HTML 파일로 렌더해줘"
  - "사업계획서 슬라이드 10장, 브라우저에서 바로 열리게"
  - "데이터 시각화 인포그래픽 슬라이드 HTML로"
  - "슬라이드 만들고 PPTX로도 저장해줘"
  - "투자 피칭 덱 인터랙티브 HTML로"
  - "발표 자료를 HTML 슬라이드 + 편집 가능 PPTX 둘 다"
  design-system-library 75개 브랜드 토큰 중 테마를 골라 적용하고, 각 토큰별 getdesign.md 상세 페이지 링크로 미리보기를 제공합니다.
  PDF 배포본이 필요하면 브라우저 `?print-pdf` 인쇄 모드를 쓰거나, 생성한 HTML을 moai-office:pdf-writer로 넘겨 변환하세요 (weasyprint를 직접 설치·호출하지 말 것).
  [책임 경계] vs moai-office:pptx-designer: 이 스킬=브라우저에서 바로 열리는 단일 .html 슬라이드 덱(편집 가능 .pptx는 pptx-designer 체이닝으로 산출). vs moai-office:notebooklm-slide-prompt: 저 스킬=NotebookLM 입력용 프롬프트(파일 생성 없음). vs moai-content:html-report: 저 스킬=연속 스크롤 문서/보고서(슬라이드 덱이 아님).
user-invocable: true
version: 2.27.0
---

# html-slide — 단일 파일 HTML 슬라이드 덱 생성기

## 목적과 범위

`moai-content:html-slide`는 발표용 슬라이드 덱을 **단일 파일·자체 완결형 HTML**로 만듭니다. 이웃 스킬 `html-report`의 "0의존·인라인 SVG·design-system-library 토큰 계약" 아키텍처를 계승하되, 연속 스크롤 문서가 아닌 **16:9 슬라이드 시퀀스 + 자체 vanilla JS 덱 런타임**(키보드 내비게이션·풀스크린·`?print-pdf` 인쇄 모드·speaker notes 토글)을 제공합니다.

**핵심 원칙**:
- 단일 `.html` 파일 — 외부 빌드 단계·런타임 SPA 의존 없이 `file://`로 즉시 오픈
- 인포그래픽은 LLM이 인라인 SVG로 직접 저작 — 한국어 숫자·라벨 100% 정확, 확대 선명, 재현 가능
- 실사·일러스트 이미지는 Higgsfield MCP 또는 codex(gpt-image-2)로 생성 — 허용 백엔드만 사용 (`references/image-backend-policy.md`)
- design-system-library 75개 브랜드 토큰 적용 — 각 토큰별 getdesign.md 상세 페이지 링크 제공
- 편집 가능 PPTX 산출은 `pptx-designer`(moai-office) 체이닝으로 위임 — 자체 구현하지 않음(중복·책임 모호화 방지)

**원고 SSOT**: 모든 덱은 구조화 원고 `deck.json`(title/bullets/chart-data/image-path/layout-key/notes)을 단일 진실 원천으로 둡니다. HTML 렌더와 (체이닝 시) pptx-designer PPTX 렌더 양쪽이 같은 원고를 소비합니다 — 픽셀→OOXML 역매핑이 아니라 원고→객체 직접 생성이 "편집 가능 PPTX"의 보증 기구입니다.

---

## 입력

| 인자 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `topic` / 자연어 주제 | ✓ | — | 덱 주제·대상 청중·발표 목적 |
| `design_system` | — | `claude` | `claude` \| `clickhouse` \| `clay` 또는 [`design-system-library`](../../../moai-design/skills/design-system-library/SKILL.md)의 75개 시스템. 지정 시 Tailwind Play CDN + shadcn vanilla 컴포넌트로 해당 브랜드 토큰 적용. 각 토큰별 getdesign.md 미리보기 링크는 [`references/design-system-links.md`](references/design-system-links.md) |
| `slide_count` / 발표 시간 | — | 주제에서 추천 | 3분=5-7장 · 10분=10-15장 · 30분=20-30장 |
| `aspect_ratio` | — | `16:9` | `16:9`(프로젝터 표준) \| `1:1`(소셜/카드뉴스) |
| `locale` | — | `ko` | `ko` \| `en` — 헤드라인·카피 언어 |
| `image_backend` | — | `higgsfield` | `higgsfield`(Higgsfield MCP, 기본) \| `codex`(gpt-image-2, ChatGPT 구독 한도) \| `svg-only`(이미지 없이 SVG 장식만) |
| `export_pptx` | — | `false` | `true` 시 pptx-designer 체이닝으로 편집 가능 .pptx 병행 산출 |
| `output_path` | — | `<cwd>/reports/<slug>-slides-<YYYYMMDD>.html` | 출력 경로 |

---

## 출력

- **주 산출물**: 단일 `.html` 파일 (`<cwd>/reports/<slug>-slides-<YYYYMMDD>.html`)
  - 자체 완결형: 브라우저에서 바로 열기 가능, 이메일 첨부·오프라인 사용 가능
  - 외부 의존: design_system 지정 시 폰트 CDN + Tailwind Play CDN, 미지정 시 폰트 CDN 1건만
- **병행 산출물** (`export_pptx: true` 시): 편집 가능 `.pptx` (pptx-designer 체이닝)
- **원고**: `deck.json` (HTML·PPTX 양쪽 공통 소스, 산출 디렉토리에 보존)

---

## 핵심 워크플로우 (9단계)

### 1. 컨텍스트 수집
`AskUserQuestion`으로 design_system(75 시스템, 기본 `claude`)·발표 시간(슬라이드 수)·이미지 필요 여부·PPTX 산출 여부를 확인합니다. design_system 선택 시 [`references/design-system-links.md`](references/design-system-links.md)의 getdesign.md 링크로 각 토큰 상세 페이지를 안내해 사용자가 미리보기로 확인할 수 있게 합니다. **강연/발표 맥락** — 비개발자 청중 다수·주간·프로젝터 환경에서는 라이트 테마(claude·notion·apple·stripe·mintlify)가 안전합니다. 다크는 발표 공간을 어둡게 조절할 수 있을 때만 권장.

### 2. 원고 SSOT 구축 (핵심)
`deck.json` 원고를 먼저 작성합니다 — title/bullets/chart-data/image-path/layout-key/notes. 이 원고가 HTML 렌더와 pptx-designer PPTX 렌더 양쪽의 공통 소스입니다. 스키마: [`references/deck-manuscript-schema.md`](references/deck-manuscript-schema.md). layout-key는 pptx-designer 9 아키타입(Title/Agenda/Problem/Solution/Features/Stats/Team/CTA/Closing)에 정합시킵니다.

### 3. 인포그래픽 = 인라인 SVG 직접 생성
차트·다이어그램·KPI 카드·타임라인은 LLM이 인라인 SVG로 직접 작성합니다. 한국어 숫자·라벨 100% 정확을 위해 비트맵 이미지로 우회하지 않습니다. 패턴 라이브러리: [`references/inline-svg-infographics.md`](references/inline-svg-infographics.md).

### 4. 비트맵 이미지 생성 (필요 시) — 이미지 백엔드 정책
포토 히어로·일러스트 컨셉 등 SVG로 표현 불가능한 비트맵이 필요한 슬라이드만 이미지 백엔드로 생성합니다. 정책: [`references/image-backend-policy.md`](references/image-backend-policy.md).

| 백엔드 | 모델 | 인증 | 권장 용도 |
|--------|------|------|-----------|
| **`higgsfield`** (기본) | GPT Image 2·Nano Banana Pro·Soul 등 11종 | Higgsfield MCP(API 키) | 프로덕션·멱등·CI 무인 |
| **`codex`** (공식 추가 2026-06-17) | gpt-image-2 | codex CLI + ChatGPT OAuth(구독 한도, API 키 불필요) | 로컬·개발자·구독 한도 재사용 |
| `antigravity` | Imagen·Nano Banana (agy -p) | Google OAuth 브라우저 + 구독 quota | ⚠️ 비권장 — OAuth/quota/CI 무인 불가, 로컬 단발 프로토타입 only |
| `svg-only` | (이미지 없음) | — | 오프라인·비용 민감·빠른 폴백 |

> 위 4개 백엔드만 허용됩니다. 그 외 외부 이미지 백엔드(MCP·API·게이트웨이)는 사용하지 않습니다 — [`references/image-backend-policy.md`](references/image-backend-policy.md).

한국어 텍스트가 이미지에 들어가면 `moai-media:gpt-image-2-prompt`(6-Block 프롬프트 빌더)로 verbatim 지시 후 선택 백엔드로 생성합니다.

### 5. design-system-library 토큰 적용
design_system 지정 시 `systems/<name>.md` 토큰 → Tailwind Play CDN config + shadcn vanilla 컴포넌트로 렌더. 미지정 시 0의존 기본 템플릿. html-report와 동일 계약 재사용. 사용자가 getdesign.md 링크로 토큰을 미리 확인한 뒤 선택할 수 있습니다.

### 6. 단일 파일 HTML 덱 조립
16:9 슬라이드 컨테이너 + 자체 vanilla JS 덱 런타임(키보드 내비·풀스크린·`?print-pdf` 인쇄 모드·speaker notes 토글·progress bar)을 단일 `.html`로 산출. 런타임 구현: [`references/html-runtime.md`](references/html-runtime.md).

### 7. AI 슬롭 후처리 (의무)
모든 슬라이드 카피·speaker notes 텍스트에 `ai-slop-reviewer` → `humanize-korean` 체인 적용. CLAUDE.local.md §3-2 HARD 규칙.

### 8. PPTX 산출 (선택, export_pptx: true 시)
`deck.json` 원고를 `pptx-designer`(moai-office)에 전달하며 체이닝. pptx-designer가 pptxgenjs로 편집 가능 OOXML `.pptx` 생성(원고→객체 직접 생성). html-slide 자체는 PPTX 생성 로직을 구현하지 않습니다. 체이닝 규약: [`references/pptx-chaining.md`](references/pptx-chaining.md).

### 9. 자체 검수
단일 HTML 열기·`?print-pdf` 인쇄 미리보기·speaker notes 표시·이미지 broken link·한국어 폰트 렌더·이미지 백엔드 정책 준수(허용 백엔드만 사용)를 자체 검수 후 PASS/FAIL 보고. PPTX 체이닝 시 pptx-designer QA 결과 통합 보고.

---

## 디자인 시스템 적용 (`design_system` 파라미터)

`design_system` 입력으로 [`moai-design:design-system-library`](../../../moai-design/skills/design-system-library/SKILL.md)에서 브랜드 토큰을 로드해 **Tailwind Play CDN + shadcn vanilla 컴포넌트**로 렌더합니다. html-report와 동일한 두 렌더 엔진을 제공합니다.

| `design_system` | 엔진 | 외부 의존 | 산출물 특성 |
|-----------------|------|-----------|-------------|
| **미지정** | 0의존 (기본 템플릿) | 폰트 CDN 1건만 | 오프라인·인쇄·이메일 첨부 가능 |
| **`claude` / `clickhouse` / `clay` / 75개** | Tailwind Play CDN | Tailwind CDN + 폰트 CDN | 브랜드 무드 적용, 인터넷 연결 필요 |

### 테마별 적합 슬라이드 (자동 추천)

| 발표 성격 | 추천 design_system |
|-----------|-------------------|
| 사업계획서·보고서·편집성 (기본) | `claude` (warm editorial, 크림+코랄) |
| 기술·데이터·엔지니어링·다크 프로젝터 | `clickhouse` (dark tech) |
| 제품 소개·SaaS·스타트업 | `notion`·`apple`·`stripe`·`mintlify` (light, 깔끔) |
| 마케팅·키노트·임팩트 | `spotify`·`nike`·`airbnb` (bold) |
| **비개발자 청중·주간·프로젝터 (라이트 안전)** | `claude`(기본) · `notion` · `apple` · `stripe` · `mintlify` |
| 다크 (방을 어둡게 조절 가능할 때) | `clickhouse` · `vercel` · `linear.app` · `supabase` · `binance` |

> **강연 추천** (getdesign.md 컬렉션 74종 쇼케이스 기준): 비개발자 청중(약 75%)·주간·프로젝터 환경에서는 **라이트가 안전**합니다. 현재 `claude`가 무난하고, 변화를 주고 싶으면 `notion`·`apple`·`stripe`·`mintlify`. 다크는 발표 공간을 어둡게 할 수 있을 때만 — `clickhouse`·`vercel`·`linear.app` 등. 전체 75개 중 19개(⚙️)는 경량 토큰이라 폰트가 시스템 산세리프 기반입니다.

### getdesign.md 미리보기 링크
각 design_system 값에 대해 [`references/design-system-links.md`](references/design-system-links.md)의 `https://getdesign.md/<slug>` 링크로 상세 페이지를 안내합니다. 사용자가 테마 선택 전 링크를 열어 팔레트·타이포그래피·무드를 직접 확인할 수 있습니다. 75개 시스템 전체 매핑표(저장소 시스템명 → getdesign.md slug)를 해당 파일에서 관리합니다.

---

## 체인 통합

```
[원고/콘텐츠 스킬] → moai-core:ai-slop-reviewer → moai-content:humanize-korean → moai-content:html-slide
                                                                            ↓ (export_pptx: true)
                                                                moai-office:pptx-designer
```

이미지 필요 시 분기:
```
html-slide → moai-media:higgsfield-image (Higgsfield MCP, 기본)
           → moai-media:gpt-image-2-prompt (한국어 verbatim 프롬프트 빌더) → higgsfield-image
           → codex exec "$imagegen ..." (image_backend: codex 시, 로컬)
```

design_system 적용은 design-system-library에서 자동 로드 — 별도 선행 스킬 호출 불필요.

---

## 사용 예시

**예시 1: 사업계획서 슬라이드 (기본 claude 테마)**
```
AI 슬라이드 스킬 스타트업 사업계획서 10장 슬라이드로 만들어줘. claude 테마로.
```

**예시 2: 데이터 인포그래픽 슬라이드 + PPTX**
```
3분기 매출 분석 슬라이드 HTML로 만들고, 편집 가능한 PPTX로도 저장해줘.
```

**예시 3: 다크 테마 기술 발표**
```
신규 API 아키텍처 기술 발표 15장, clickhouse 다크 테마로 슬라이드 HTML 만들어줘.
```

**예시 4: codex 백엔드 이미지**
```
제품 런칭 슬라이드 만들어줘. 히어로 이미지는 codex로 생성하고, notion 테마 적용.
```

**예시 5: 테마 미리보기 후 선택**
```
슬라이드 만들 건데, 디자인 토큰 후보들 getdesign.md 링크로 보여주고 내가 고를게.
```

---

## 하지 않는 것

- 연속 스크롤 문서는 `moai-content:html-report`가 맡습니다 — 본 스킬은 슬라이드 시퀀스(16:9 페이지) 전용입니다.
- 편집 가능 .pptx 직접 생성은 하지 않습니다 — `pptx-designer`(moai-office) 체이닝으로 위임합니다.
- NotebookLM 입력용 프롬프트는 `moai-office:notebooklm-slide-prompt`가 맡습니다.
- React/Vue/webpack/vite 같은 빌드 단계·런타임 SPA 의존을 도입하지 않습니다 — `file://` 즉시 오픈이 원칙입니다.
- [`references/image-backend-policy.md`](references/image-backend-policy.md)의 허용 백엔드(Higgsfield MCP + codex)만 사용합니다. 그 외 외부 이미지 백엔드는 사용하지 않습니다.
- 여러 파일로 나누지 않습니다 — HTML 산출물은 단일 `.html` 파일입니다.

---

## 참고 문서

### 설계 문서
- [`references/deck-manuscript-schema.md`](references/deck-manuscript-schema.md) — deck.json SSOT 스키마 + pptx-designer 아키타입 매핑 규약
- [`references/html-runtime.md`](references/html-runtime.md) — 자체 vanilla JS 덱 런타임 (네비게이션·풀스크린·`?print-pdf`·speaker notes, 0의존)
- [`references/inline-svg-infographics.md`](references/inline-svg-infographics.md) — 인라인 SVG 인포그래픽 패턴 (차트·다이어그램·KPI, 한국어 숫자/라벨 정확 렌더)
- [`references/image-backend-policy.md`](references/image-backend-policy.md) — 이미지 백엔드 정책 (Higgsfield + codex 공식, antigravity 비권장, 허용 백엔드만)
- [`references/pptx-chaining.md`](references/pptx-chaining.md) — pptx-designer 체이닝 규약 (편집 가능 PPTX 보증 기구)
- [`references/design-system-links.md`](references/design-system-links.md) — 75개 시스템 → getdesign.md 링크 매핑표

### 샘플
- [`samples/deck-sample.json`](samples/deck-sample.json) — 8장 비즈니스 발표 원고 (deck.json SSOT)
- [`samples/deck-sample.html`](samples/deck-sample.html) — 완성 단일 파일 HTML 덱 (design_system: claude 적용)

### 이웃 스킬 (체이닝)
- [`moai-design:design-system-library`](../../../moai-design/skills/design-system-library/SKILL.md) — 75개 브랜드 토큰 SSOT
- [`moai-office:pptx-designer`](../../../moai-office/skills/pptx-designer/SKILL.md) — 편집 가능 .pptx 생성 (체이닝)
- [`moai-media:higgsfield-image`](../../../moai-media/skills/higgsfield-image/SKILL.md) — Higgsfield MCP 이미지 (기본 백엔드)
- [`moai-media:gpt-image-2-prompt`](../../../moai-media/skills/gpt-image-2-prompt/SKILL.md) — 한국어 verbatim 이미지 프롬프트 빌더
- [`moai-core:ai-slop-reviewer`](../../../moai-core/skills/ai-slop-reviewer/SKILL.md) → [`moai-content:humanize-korean`](../humanize-korean/SKILL.md) — 의무 후처리 체인

## 자체 검수

슬라이드 생성이 끝나면 산출된 단일 .html을 브라우저에서 열어 슬라이드 수·16:9 비율·네비게이션·`?print-pdf` 인쇄 모드·speaker notes·한국어 폰트 렌더·인포그래픽 SVG 정확도를 **자체 검수**하고, 이미지 백엔드 정책 준수(허용 백엔드만 사용)를 확인한 뒤 PASS/FAIL 결과를 보고합니다. PPTX 체이닝 시 pptx-designer QA(빈 플레이스홀더·overflow·색 대비 4.5:1) 결과를 통합 보고합니다. 문제가 있으면 자동 수정 후 재생성합니다.
