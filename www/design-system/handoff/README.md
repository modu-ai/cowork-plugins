# 모두의AI Design System

> 디자인 시스템 패키지 — 모두의AI 커뮤니티 플랫폼
> Source: Notion MoAI SNS 디자인 가이드라인 Ver 1.0 (2026-04-25)

---

## 1. 회사 / 제품 컨텍스트

**모두의AI (mo.ai.kr)** 는 한국의 AI 사용자가 모이는 커뮤니티 플랫폼이다. Agentic AI 정체성을 가지고 베타 테스터와 함께 만들어가는 **CX(Collective eXperience) 7원칙** 기반 운영을 신뢰의 핵심으로 내세운다. 영어로는 "Everyone's Artificial Intelligence".

핵심 가치:
- **모두를 위한 AI를, 모두와 함께** — 누구도 배제하지 않는 포용
- **검증된 한국어 AI 큐레이션** — 영어 80% 정보 시장에 한국어 깊이 분석
- **투명한 운영** — 매출·지표·실패 모두 공개
- **베타 테스터를 동료로** — 기여한 만큼 정식 출시 후 3개월~1년 무료

### 제품 표면 (1라운드 5페이지)
| 페이지 | 경로 | 목적 |
|---|---|---|
| 랜딩 | `/` | 5초 안에 "왜 베타에 합류해야 하는가" 답 |
| 모두의 프로젝트 허브 | `/projects` | 매출/지표/실패 투명 공개 |
| 베타 신청 | `/beta` | 5분 이내 신청 완료 |
| AI 뉴스 허브 | `/news` | 매일 1pick + 5~10건 큐레이션 |
| AI 아카데미 | `/academy` | 주말 14시간 워크플로우 완성 여정 |

### 6개 출시 예정 서비스
모두의 사주 · 바닐라 바게트 · 모두의 주식 · 포춘 테이블 · 모두의 데이트 · aStory

### Sources (이 시스템의 출처)
- 코드베이스 마운트: `design/` (read-only)
  - `design/system.md`, `design/spec.md`, `design/research.md`, `design/tokens.json`, `design/components.json`
  - `design/handoff/` — Master Brief, brand-voice, visual-identity, target-audience, prompts/
  - `design/handoff/assets/` — 9 logo variants + reference screenshots
- Notion MoAI SNS 디자인 가이드라인 Ver 1.0 (브랜드 SSOT, FROZEN)

---

## 2. CONTENT FUNDAMENTALS — 카피 작성 가이드

### Tone
**신뢰감 있고 전문적이며, 동시에 따뜻하고 포용적.** "모두의"라는 브랜드 코어가 모든 페이지에 1회 이상 자연스럽게 등장한다. 베타 테스터를 수동적 user가 아닌 "동료/주체"로 호명한다.

### Register
- **Formality**: 본문은 "~합니다" 존대. CTA·말풍선·이벤트 카피는 "~해보세요", "~할까요?" 친근체 혼용.
- **Seriousness**: 정보 전달은 진중. 마스코트와 함께 등장하는 카피는 위트 가능 (빈 상태/오류).
- **Tech jargon**: 첫 등장 시 한 번 풀어쓰기 — `에이전트(스스로 일하는 AI)`. 두 번째부터 약어 유지.

### "I" vs "You"
- **나/내가** — 사용자 정체성을 강조할 때: "**내가 만든** AI 워크플로우", "**나만의** 워크플로우 완성"
- **여러분/모두** — 호명할 때: "베타에 합류**하세요**"
- **우리** — 공동 주체로 묶을 때 (운영진+테스터): "**모두와 함께** 만듭니다"
- 직접적인 "당신" 호명 지양 (마케팅 슬랭처럼 들림)

### Casing & Punctuation
- 한글 본문은 모두 일반 케이스 — All-caps 한국어 금지
- 영문 약어/태그는 UPPER (`BETA`, `AI`, `CX`)
- 마침표 사용. 다만 짧은 CTA·태그는 마침표 생략 ("베타 신청하기 →")
- 큰 따옴표 `"..."`, 한국어 화살괄호 `《》`는 인용에만
- 화살표 `→` 적극 — CTA 끝, 흐름 표시

### Emoji?
- **본문/UI에서는 사용 금지** — 마스코트가 정서 앵커 역할을 대신함
- 댓글 길이 평균 50~120자, 사용자 댓글에서 이모지 사용률 30%로 관측되지만, 시스템 카피는 미사용
- 이모지 대신 **마스코트(`moai-logo-3`)** + lucide 아이콘으로 표현

### 선호 어휘 (적극 사용)
- "모두의" · "함께 만드는" · "베타 테스터" · "Loop" · "에이전트"
- "집단경험" / "CX (Collective eXperience)" · "고객 만족"
- "오픈 프로젝트" · "기여도" · "기여한 만큼"
- "AI 워크플로우" · "검증된" · "출시 6개월"

### 금지 어휘
- 마케팅 슬랭: 혁신적인, leverage, 솔루션, Game-changing, Cutting-edge, Next-level, Disruptive
- 절대형: 절대로, 유일한, 최고의, AI의 모든 것
- 자기계발 톤: "당신의 잠재력을 깨우는…"
- FOMO: "지금 안 하면 평생 후회"
- 인터넷 밈: 핵개꿀 등 (브랜드 격 손상)

### Vibe — 구체 예시
> "모두를 위한 AI를, **모두와 함께** 만듭니다."
> "베타 테스터의 한마디가 다음 버전이 됩니다."
> "주말 14시간, 나만의 **AI 워크플로우 완성**."
> "출시 6개월 후, 데이터로 다시 묻습니다."
> "기여한 만큼 무료로 누리세요. 최대 1년."
> "AI는 단 하나, 고객 만족에만 집중합니다."

### Channel-Specific
| 위치 | 톤 |
|---|---|
| 랜딩 히어로 | 카피 압축 + 굵기 대비 |
| CTA 버튼 | 동사 시작, 친근체 ("베타 신청하기") |
| 빈 상태 | 마스코트 + 위트 ("아직 비어 있어요. 첫 글의 주인공이 되세요.") |
| 에러 | 사과 + 책임 ("잠시 멈췄습니다. 곧 정상으로 돌아가요. (코드: 502)") |
| 모더레이션 | 단호하지만 정중 ("이 글은 가이드 5번을 위반해 가려졌습니다.") |
| 결제 | 투명, 비교 가능 ("월 9,900원. 7일 무료. 언제든 해지.") |

---

## 3. VISUAL FOUNDATIONS

### Color Vibe
**모아이 그린(#3d7d5f — 마스코트 스웨터 그린) 단일 코어.** 캐릭터 일러스트의 잉크(#060606)·스톤 그레이(#9fa0a0)·라이트(#e6e6e6)와 한 팔레트. 마젠타·퍼플·오렌지 그라디언트는 정체성 훼손이라 명시적으로 금지. 시그니처 그라디언트(`135deg, #3d7d5f → #09110f`)는 헤더, 1차 CTA, 디바이더, 카드 hover 등 일관 사용. 한 화면에 4종 이상 컬러 토큰 동시 사용 금지. **#000000 절대 사용 금지** (대신 `#09110f`).

### Type
**Pretendard** 단일 한글 폰트 + Inter(라틴 보조) + JetBrains Mono(코드). 9 weights(Thin 100 ~ Black 900) self-host (`fonts/Pretendard-*.otf`). 핵심은 **한 문장 안에서 굵기 대비** — 도입부 Regular/Medium, 핵심 키워드 Bold/Black. Notion 자간 규칙 엄수: 메인 타이틀 `-0.05em ~ -0.075em`, 본문 `-0.025em ~ -0.05em`.

### Backgrounds
- **풀 블리드 이미지 사용 안 함**. 페이지 배경은 단색 `#f3f3f3`만.
- **그라디언트는 시그니처 한 종류만** — 헤더, 풀-CTA 섹션, 디바이더, 카드 hover.
- **카드 hover 글로우** — `shadow.signature`(청록 글로우)
- 그라디언트 **soft variant** (`rgba 알파`) — 베타 혜택 카드 같은 미묘한 톤 영역
- **반복 패턴/텍스처 미사용** (Notion 가이드 정신 — 시각 노이즈 방지)

### Animation
- **빠르고 짧은 ease-out 기본** — `150ms~250ms` `cubic-bezier(0.4,0,0.2,1)`
- **마스코트만 bounce** — `cubic-bezier(0.34, 1.56, 0.64, 1)` (등장, 마우스오버 흔들림)
- **페이지 전환 smooth** — `cubic-bezier(0.16,1,0.3,1)` 600ms
- **페이드 + 작은 translateY** 기본 (>4px 이동 지양)
- `prefers-reduced-motion: reduce`에서 모든 transition 1ms

### Hover States
- **버튼 (primary)**: `shadow.signature` (청록 글로우) 추가, 색은 변하지 않음
- **버튼 (secondary)**: 배경 → primary, 텍스트 → 흰색
- **버튼 (ghost)**: 배경 brightness(0.97)
- **카드**: `translateY(-2px)` + `shadow.md`, 강조 카드는 `shadow.signature`
- 링크: 밑줄 X, opacity 변화 또는 색 → primary

### Press States
- **버튼**: `transform: translateY(1px)` (살짝 가라앉음). 색은 `--color-primary-active` (#265240)
- **카드**: 의도된 press 상태 없음 (전체 카드 클릭 영역은 cursor:pointer)

### Borders
- 기본 `1px solid #d4d4d4` (`--border-1`)
- 강조 outline `1.5px solid #bcbcbc`
- 포커스 ring `0 0 0 3px rgba(61,125,95,0.12)` + `2px solid var(--color-primary)`
- **둥근 보더 + 좌측 컬러 액센트 카드** 패턴은 사용하지 않음 (AI 슬롭)

### Shadow System
- **Outer only** — inner shadow 미사용
- 5단계 + signature: xs(2px) / sm(4px) / md(12px) / lg(24px) / xl(48px) / signature(32px 청록 글로우)
- 모두 `rgba(9,17,15,X)` (검정 대신 ink)
- **그라디언트 + shadow 동시 적용 금지** — 시각 노이즈 (FROZEN rule)

### Protection Gradients vs Capsules
- 그라디언트 위 텍스트는 항상 흰색 (검정 텍스트 금지 — WCAG AA 위반)
- 텍스트 보호용 protection gradient는 사용 안 함 (이미지 위 텍스트 패턴이 없음)
- **Pill capsule** — CTA primary, 태그, 배지에 사용 (radius `pill`/32px 또는 `full`)

### Layout Rules
- **Grid**: 12 컬럼 (≥1024px), 4 컬럼 (<768px)
- **Container max-width**: 1440px (`2xl`); 콘텐츠 영역 1024px (`lg`) 권장
- **Gutter**: 32 / 24 / 16 px (desktop / tablet / mobile)
- **Vertical rhythm**: 섹션 간 80 / 64 / 48 px
- **Sticky elements**: 헤더(top, 64px), 모바일 sticky CTA (베타 신청)
- **Section alternating**: light 모드 `#f3f3f3 ↔ #ffffff`, dark 모드 `#0e1513 ↔ #1a1f1d`

### Transparency & Blur
- **Header**: `background: rgba(243,243,243, 0.85)` + `backdrop-filter: blur(12px)` (sticky)
- **Modal scrim**: `rgba(9,17,15, 0.5)` (블러 없음)
- **Glassy cards 사용 안 함** — 청록 정체성과 충돌

### Imagery Vibe
- 마스코트 외 일러스트 사용 시 **모두의 청록 톤만** (멀티컬러 금지)
- 사진은 **그레이스케일 + 청록 오버레이**로 의도 가공
- 카드 이미지 비율: 4:5 또는 1:1 (한국 SNS 친화)
- 히어로 이미지: 16:9 또는 21:9
- **스톡 일러스트 (unDraw, Storyset 등) 사용 금지** — 마스코트로 대체

### Corner Radii
- `none(0)` — 셀, 풀-블리드
- `sm(4px)` — input, 작은 chip
- `md(8px)` — 카드, 버튼 기본
- `lg(16px)` — 큰 카드, 모달
- `xl(24px)` — hero 카드
- `pill(32px)` — CTA pill, 태그
- `full(9999px)` — 아바타, 원형 버튼

### Cards
- **Surface**: `#ffffff`, `radius lg(16px)`, `padding 6(24px)`, `shadow.sm`, `border 1px #d4d4d4`
- **Hover**: `translateY(-2px)`, `shadow.md`
- **Elevated**: `shadow.lg`, no border
- **Outline**: `border 1.5px #bcbcbc`, no shadow
- **Gradient**: `signature gradient` 배경, 흰 텍스트, 강조용

---

## 4. ICONOGRAPHY

### Icon Library
**Lucide Icons** (`lucide-react` 또는 lucide CDN, MIT 라이선스).
- Stroke-width: `1.75` 기본, 강조 시 `2`
- 색상: `currentColor` (텍스트와 동조). 강조 아이콘만 `--color-primary`
- 사이즈: 16 / 20 / 24 / 32 px (sm / md / lg / xl)

원본 코드베이스에서 자체 아이콘 폰트/스프라이트는 사용하지 않으며, Lucide를 표준으로 채택. 본 시스템의 모든 UI 컴포넌트는 CDN Lucide(`https://unpkg.com/lucide@latest`)를 사용한다. **Substitution flag: 없음** (Lucide가 원본 명시).

### Logo & Mascot
원본 9종 PNG 모두 `/assets/`에 복사 완료:

| 변형 | 파일 | 용도 |
|---|---|---|
| 가로형 | `assets/moai-logo-4.png` | **헤더** (≥1024px), max-h 32px |
| 가로형 다크 | `assets/moai-logo-4-WH.png` | 다크 배경/그라디언트 위 |
| 정사각 풀 | `assets/moai-logo-1.png` | OG, 푸터, 카드 헤더 |
| 정사각 다크 | `assets/moai-logo-1-WH.png` | 다크 정사각 |
| **마스코트** | `assets/characters/MoAI-Mascot-*.png` | **모아이 석상 캐릭터 포즈 6종**. 히어로, 빈 상태, 404/500 |
| 카드 그라디언트 | `assets/moai-logo-2.png` | 인스타 카드 |
| 카드 모노 | `assets/moai-logo-2-1.png` | 모노톤 카드 |

규칙: 헤더 max-h `32px` desktop / `28px` mobile. 클리어스페이스 `16px` 이상. **마스코트는 데이터 표·폼·결제 화면 등장 금지** — 정서적 영역에서만.

### SVG vs PNG
- **로고/마스코트**: PNG (원본 자산). SVG 변환 시 디테일 손실 우려라 PNG 유지.
- **UI 아이콘**: Lucide SVG via CDN (인라인 변환).

### Emoji
**UI 카피에서 미사용** — 마스코트가 정서 앵커. 사용자 댓글에는 자유.

### Unicode 아이콘
화살표 `→ ← ↑ ↓` 적극 사용 (CTA 끝, 흐름 표시). 그 외 `⌘ ⇧ Ctrl` 등 키 표기는 단축키 도움말에서만.

---

## 5. Index — 파일 매니페스트

### Root
- `README.md` — 본 문서
- `SKILL.md` — Claude Skill / Agent Skill 매니페스트
- `colors_and_type.css` — 모든 CSS 변수 + 시맨틱 타입 클래스
- `assets/` — 9 logo PNG + 2 color guide refs + 2 typography refs
- `assets/characters/` — MoAI-Mascot 캐릭터 포즈 일러스트 6종 (PNG)

### MoAI-Mascot — 캐릭터 일러스트
모아이 석상 캐릭터. 그린(#3d7d5f) 스웨터. 정서적 표면(히어로·빈 상태·온보딩·404)에서만 사용, 데이터 표·폼·결제 화면 금지.
- `MoAI-Mascot-Thinking` — 턱을 괸 생각하는 포즈 (로딩·고민 상태)
- `MoAI-Mascot-Pointing` — 손가락으로 가리키기 (안내·CTA)
- `MoAI-Mascot-Searching` — 돋보기로 탐색 (검색·빈 결과)
- `MoAI-Mascot-Teaching` — 지시봉으로 설명 (튜토리얼·온보딩)
- `MoAI-Mascot-Explaining` — 두 손 벌려 안내 (환영·설명)
- `MoAI-Mascot-Coffee` — 커피 한 잔 (여유·성공 상태)

캐릭터 팔레트(테마 소스): 잉크 `#060606` · 스톤 그레이 `#9fa0a0` · 그린 `#3d7d5f` · 라이트 `#e6e6e6`
- `preview/` — Design System tab 카드들 (HTML)
- `ui_kits/` — 제품 surface별 UI kit (각 폴더에 README + index.html + JSX)

### Components — 문서 / 다이어그램
- `DocPage` — 온라인 문서 컴포넌트 (페이지형 문서 셸, a4/letter/legal, 화면 연속 시트 + 인쇄 페이지네이션)
- `MermaidDiagram` — Mermaid 다이어그램 요소 (mermaid.js 로드, 모아이 그린 + 무채색 테마)

### UI Kits
- `ui_kits/website/` — `mo.ai.kr` 마케팅 사이트 (랜딩 / 베타 신청 / 뉴스 허브)

### Reference Source (read-only mount)
- `design/handoff/00-MASTER-BRIEF.md` — 통합 브리프
- `design/handoff/01-brand-voice.md` ~ `08-components.json`
- `design/system.md` / `spec.md` / `research.md` / `tokens.json` / `components.json`

---

## 6. Caveats & Substitutions

- **Pretendard**: `fonts/Pretendard-{Thin,ExtraLight,Light,Regular,Medium,SemiBold,Bold,ExtraBold,Black}.otf` self-hosted (9 weights, 100~900). `@font-face`로 `colors_and_type.css` 상단에서 로드.
- **Inter / JetBrains Mono**: Google Fonts CDN.
- **Lucide Icons**: CDN. 원본 코드베이스에서 명시한 표준이라 substitution 아님.
- **마스코트 PNG**: 원본 9종 그대로 복사. SVG 변환 안 함.

---

_Last updated: 2026-04-25_
