# Changelog

모든 주목할 만한 변경사항은 이 파일에 기록됩니다.

형식: [Keep a Changelog 1.1.0](https://keepachangelog.com/ko/1.1.0/) · 버저닝: [Semantic Versioning 2.0.0](https://semver.org/lang/ko/)

## 버전 통일 원칙 (HARD)

아래 18개 지점의 버전 표기는 **항상 완전히 동일**합니다 (v1.3.0부터):
- `.claude-plugin/marketplace.json` (`metadata.version`) × 1
- `<plugin>/.claude-plugin/plugin.json` (`version`) × 17
- ~~`<plugin>/skills/<skill>/SKILL.md`~~ — **v1.3.0에서 제거** (metadata 블록 삭제, plugin.json 단일 소스)

상세 정책: `CLAUDE.local.md` § 1 참조.

## [1.5.0] - 2026-04-21

공식 MINOR 릴리스. **moai-business 플러그인에 소상공인·창업자 실무 지원 스킬 2종을 추가**하여 총 스킬 개수가 71 → 73으로 확장됩니다. 두 스킬 모두 Category A(`user-invocable: true`)로 슬래시 명령 자동완성을 지원하고, 사용자 언어의 트리거가 풍부해 자연어로도 자동 호출됩니다.

### Highlights

- **소상공인365 상권분석 자동화** — `bigdata.sbiz.or.kr` PDF 한 장을 첨부하면 4문 인터뷰 후 창업 타당성 100점 평가 + 9섹션 DOCX 보고서를 자동 생성합니다.
- **정부지원사업 통합 도우미** — K-Startup, BIZINFO, 중기부, 창진원, 문체부, 농식품부 등 주요 공고를 한 번에 탐색하고 사업계획서 초안까지 작성합니다.
- **Anthropic 공식 스킬 우선순위 반영** — 두 스킬 모두 DOCX/XLSX 생성 시 `anthropic-skills:docx` · `anthropic-skills:xlsx` 우선, AI 슬롭 검수도 `anthropic-skills:ai-slop-reviewer` 우선 정책을 내장했습니다.

### Added

- **`moai-business/skills/sbiz365-analyst/`** 신규 스킬 (Category A) — 소상공인365 PDF 기반 상권 트렌드 분석 + 창업 타당성 종합 보고서.
  - Step 0~5 워크플로우: PDF 확인 → 4문 AskUserQuestion(업종·목적·예산·중점) → PDF 데이터 추출 → 5대 분석(유동인구·매출·경쟁·입지·타당성) → 9섹션 DOCX → AI 슬롭 검수.
  - 4축 100점 평가 체계: 성장성(30) + 경쟁 적합도(25) + 수요 매칭도(25) + 재무 타당성(20).
  - `references/{analysis-guide, data-fields, feasibility-scoring, report-template}.md` 4종 레퍼런스 포함.
- **`moai-business/skills/kr-gov-grant/`** 신규 스킬 (Category A) — 대한민국 정부·공공기관 지원사업 통합 분석 및 신청서 작성.
  - 4 MODE 구조: ① 탐색·추천 / ② 신청서 초안 작성 / ③ 서류 검토 / ④ 일정 관리.
  - 8개 신청자 유형 × 7개 지원 카테고리(창업/소상공인/R&D/문화관광/농식품/사회적경제/지자체 등) 매핑 데이터베이스.
  - 예비창업패키지·TIPS·전통시장 활성화·중소기업 R&D·관광벤처 등 사업별 항목 구조 템플릿 탑재.
  - `references/programs.md` 상세 프로그램 카탈로그.

### Changed

- `moai-business/.claude-plugin/plugin.json`
  - `description` 갱신: "사업계획서, 시장조사, 재무모델, IR, 상권분석, 정부지원사업"으로 확장.
  - `keywords` 확장: 상권분석·창업타당성·소상공인365·정부지원사업·K-Startup·BIZINFO·창업지원·지원금 추가.
- `.claude-plugin/marketplace.json`
  - `metadata.description` 갱신: "71 스킬" → "73 스킬", v1.5.0 하이라이트 추가.
  - `moai-business` 엔트리 설명 갱신: 신규 스킬 범위 반영.
- `kr-gov-grant` vs `moai-research:grant-writer` 스코프 분리 명시 — 전자는 범용 지원사업 전반, 후자는 학술·연구 중심 NRF/IITP 과제.

### Notes

- 두 스킬 모두 `user-invocable: true` 플래그를 포함하여 `/sbiz365-analyst`, `/kr-gov-grant` 슬래시 자동완성이 활성화됩니다.
- 두 스킬의 텍스트 산출물(보고서·사업계획서·검토 피드백)은 모두 AI 슬롭 검수로 종료되며, Anthropic 공식 스킬이 있으면 우선 사용합니다.
- 사용자는 릴리스 후 `/plugin marketplace update cowork-plugins` 실행이 필요합니다.

---

## [1.4.0] - 2026-04-16

공식 MINOR 릴리스. **HTML·웹 산출물의 shadcn/ui 기본 스택 전환 + 소크라테스식 테마 인터뷰 도입**. 사용자가 코드 한 줄도 쓰지 않고도 자신의 브랜드·취향에 맞는 shadcn 베이스 팔레트·컬러 모드·모서리 반경·효과를 선택할 수 있도록 `AskUserQuestion` 흐름을 표준화.

### Highlights

- **shadcn/ui가 HTML/웹 산출물 기본 스택** — Next.js 15 + Tailwind v4 + shadcn/ui + Lucide + Framer Motion 조합이 기본.
- **소크라테스식 테마 인터뷰 공통 프로토콜** — 랜딩·상세·대시보드 3개 스킬이 동일한 4문항 질문 패턴 공유.
- **OKLCH CSS 변수 기본 출력** — Light/Dark 모드 동시 산출, shadcn 공식 `:root` + `.dark` 구조 준수.
- **Recharts/Chart.js/Tremor/ECharts 4택 1** — 차트·대시보드 산출 시 사용자가 직접 선택.

### Added

- **`moai-content/skills/landing-page/references/landing-page/shadcn-theme-interview.md`** 신규 레퍼런스 — shadcn 테마 인터뷰 프로토콜, AskUserQuestion payload 설계, OKLCH CSS 변수 템플릿, Fallback 기본값, 브랜드 컬러 오버라이드 가이드, 스킬별 적용 포인트 수록.
- `landing-page` 스킬: 실행 워크플로우에 **0단계 shadcn 테마 인터뷰(HARD)** 추가 — Q1 베이스 팔레트 / Q2 컬러 모드 / Q3 모서리 반경 / Q4 효과(multiSelect) / Q5 차트 라이브러리(조건부).
- `landing-page` 스킬: 섹션 구성을 shadcn 공식 블록(Hero / Features / Pricing / FAQ / Testimonial)에 매핑.
- `product-detail` 스킬: 0단계 shadcn 테마 인터뷰(HARD) 추가 — 플랫폼별 분기(스마트스토어·쿠팡은 단일 HTML 인라인, 자사몰·SaaS는 Next.js+shadcn) 명시.
- `product-detail` 스킬: shadcn 컴포넌트 매핑 섹션 신설 — Select/ToggleGroup/Tabs/Accordion/Badge/Button/Card 연결.
- `data-visualizer` 스킬: HTML·React 대시보드 산출 시 shadcn 테마 인터뷰(HARD) + 차트 라이브러리 선택 가이드 추가.
- 모든 카피 JSON 출력에 `theme` 블록 추가 (system, base, mode, radius, effects, chart_lib).

### Changed

- **기본 스타일 스택**: 3개 HTML/웹 스킬(`landing-page`, `product-detail`, `data-visualizer`) 모두 shadcn/ui를 기본값으로 채택. 별도 지정이 없으면 Next.js 15 + Tailwind v4 + shadcn/ui로 산출.
- `landing-page` description에 "shadcn/ui 기반"과 "소크라테스식 테마 인터뷰" 트리거 문구 명시.
- `product-detail` description에 동일한 shadcn 인터뷰 언급 추가.
- `data-visualizer` description에 Recharts/Chart.js/Tremor/ECharts 4택 1 문구 명시.
- `product-detail` 실행 규칙에 shadcn 테마 인터뷰 단계 삽입 (기존 6단계 → 8단계).
- `landing-page` 색상·타이포·컴포넌트 정의를 shadcn OKLCH 토큰(`--primary`, `--accent`, `--muted-foreground` 등)으로 표준화.
- 마켓플레이스 `description`에 v1.4.0 하이라이트 문구 추가.

### Migration

1. `/plugin marketplace update cowork-plugins`로 v1.4.0 갱신.
2. 기존 랜딩/상세/대시보드 프로젝트를 재생성하고 싶으면 다시 "랜딩 페이지 만들어줘" 등으로 호출 — 새 테마 인터뷰가 먼저 실행됨.
3. 인터뷰를 건너뛰고 기본값으로 빠르게 생성하려면 `--quick` 또는 "그냥 기본으로" 플래그를 사용.
4. 기존 Framer/Webflow/Wix 요청은 사용자가 명시적으로 지정하면 shadcn이 아닌 해당 플랫폼 스펙으로 자동 전환됨(동작 동일).
5. 브랜드 컬러가 이미 있는 경우: shadcn 베이스 팔레트를 뉴트럴 스캐폴드로 사용하고 `--primary`·`--accent`·`--ring` 세 토큰만 오버라이드 — 인터뷰 중 사용자가 브랜드 컨텍스트를 제시하면 자동 적용.


## [1.3.0] - 2026-04-14

### Added
- **`moai-core:ai-slop-reviewer` 스킬 신규 도입** — Claude가 생성한 텍스트의 AI 패턴(금지어, 획일적 문장 구조, AI식 도입/결말, 과도한 목록화, 수동태 남용 등)을 진단하고 인간적인 톤으로 수정. 모든 텍스트 산출물 워크플로우의 **필수 마지막 단계**.
- **스킬 체이닝 기반 `/project init` 워크플로우** — 사용자 업무 인터뷰 → 설치 플러그인 감지 → **산출물별 스킬 체인 설계** → 사용자 확인 → CLAUDE.md 생성. 40+ 산출물 프리셋 체인(사업계획서, IR 덱, 블로그, 랜딩, 계약서, 특허 등) 제공.
- CLAUDE.md 외부 템플릿화 — `moai-core/skills/project/references/templates/CLAUDE.md.tmpl` 도입. `{workflow_chains}`, `{primary_deliverables}`, `{tone_constraints}` 등 변수 슬롯 기반.
- HARD 규칙 블록 고정 포함 — 생성된 모든 CLAUDE.md에 "문서·콘텐츠 생성 우선순위(moai-office/content 우선)" + "AI 슬롭 후처리" 규칙이 강제 포함됨.

### Changed
- **커맨드 이름 변경**: `/moai` → `/project` (init, catalog, status, apikey, feedback 등 모든 서브커맨드).
  - **이유**: Claude Code 프로젝트 레벨 스킬(`.claude/skills/moai/`)이 플러그인 스킬을 shadowing하여 `/moai` Tab 자동완성이 동작하지 않던 문제 해소.
  - **사용자 영향**: 기존 `/moai init` 사용자는 `/project init`으로 변경 필요. `/plugin marketplace update cowork-plugins`로 갱신 후 적용.
- 스킬 폴더 이동: `moai-core/skills/moai/` → `moai-core/skills/project/`.
- 버전 단일 소스화 — SKILL.md `metadata:` 블록 전면 삭제, plugin.json `version` 필드가 유일한 버전 원천. 동기화 지점 88개 → **18개**로 축소.
- SKILL.md frontmatter 규격 단순화 — 슬래시 호출 스킬: `name` + `description` + `user-invocable: true`. 모델 자동 호출 스킬: `name` + `description`만. 그 외 필드 금지.
- `/project init` AskUserQuestion 회수 감소: 최대 9회 → **최대 6회**.

### Removed
- **글로벌 프로필 시스템 전면 제거**
  - `moai-core/skills/project/references/core/profile-manager.md` 삭제.
  - `moai-profile.md` 파일 생성 중단.
  - `[MoAI 프로필]` 글로벌 지침 텍스트 안내 제거.
  - `/project init` Phase 0 (프로필 감지), Phase 1 (이름/회사 수집) 삭제.
  - **이유**: 프로젝트마다 동일한 정보를 반복 질문하던 UX 문제 해소. 사용자 정보가 필요한 경우 CLAUDE.md 한 곳에 기록.
- SKILL.md `metadata:` 블록 (version/status/updated/tags) — 69개 파일에서 일괄 제거.

### Fixed
- `/moai` Tab 자동완성이 Claude Code 내부 `moai` 스킬과 충돌해 동작하지 않던 이슈 (커맨드 이름 변경으로 해결).

### Migration

1. `/plugin marketplace update cowork-plugins` 실행 후 플러그인 갱신.
2. 기존 사용하던 `/moai init`, `/moai catalog`, `/moai status`, `/moai apikey`, `/moai feedback` → `/project init` 등으로 교체.
3. 기존 프로젝트 CLAUDE.md의 `/moai ...` 참조를 `/project ...`로 바꾸거나, `/project init`을 다시 실행해 최신 템플릿으로 재생성 권장.
4. `[MoAI 프로필]` 글로벌 지침을 유지하고 싶은 경우: Cowork Settings > 글로벌 지침에 수동 보존(자동 참조는 중단됨). 불필요하면 제거해도 기능 영향 없음.


## 엔트리 템플릿

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 신규 기능/스킬/플러그인 추가 사항 (파일 경로 포함)

### Changed
- 기존 기능 동작/인터페이스 변경 사항 (이유 명시)

### Deprecated
- 다음 메이저 릴리스에서 제거 예정인 기능

### Removed
- 이번 릴리스에서 삭제된 기능/파일

### Fixed
- 버그 수정 내역 (증상 → 원인 → 해결)

### Security
- 보안 취약점 수정 (CVE 번호 있으면 명시)

### Breaking
- 사용자 조치 필요 사항 (마이그레이션 가이드 포함)

### Migration
- 업그레이드 절차 (필수 명령어, 설정 변경)
```

작성 규칙:
- 모든 항목은 **사용자가 체감할 변화** 기준으로 서술 (내부 리팩터는 생략 가능)
- 파일 경로는 백틱으로 감싸기: `moai-core/skills/moai/SKILL.md`
- 증상/원인/해결을 명확히 분리하여 기술
- 관련 커밋·이슈·PR 번호가 있으면 `(#123, abc1234)` 형식으로 부기

---

## [1.2.0] - 2026-04-14

공식 MINOR 릴리스. v1.1.0~v1.1.3의 점진적 변경을 안정 버전으로 집약하여 배포.

### Highlights

- **신규 플러그인 `moai-media`** — AI 미디어 스튜디오 (이미지·영상·음성 통합)
- **Google Nano Banana 공식 전환** — Imagen 4 → Gemini 3 Image Preview (Pro + 2 체제)
- **영상은 Kling 단일화** — fal.ai 기반 숏폼·립싱크 커버
- **음성은 ElevenLabs 공식 MCP** — TTS, 32개 언어 더빙, ConvAI
- **fal.ai 게이트웨이** — Flux·Recraft·Hailuo·Luma·Pika·MiniMax Music 1000+ 모델 단일 접점
- **전 저장소 버전 통일 88 지점** → **1.2.0**

### Added

- 플러그인 `moai-media` (5 스킬)
  - [`nano-banana`](moai-media/skills/nano-banana/SKILL.md): Google Gemini 3 Image Preview 공식 2종 (`gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`)
  - [`ideogram`](moai-media/skills/ideogram/SKILL.md): Ideogram 3.0 한국어 타이포 (fal.ai)
  - [`kling`](moai-media/skills/kling/SKILL.md): Kling 3.0 숏폼 영상 (fal.ai, 립싱크·다국어)
  - [`elevenlabs`](moai-media/skills/elevenlabs/SKILL.md): ElevenLabs 공식 MCP (TTS·음성복제·더빙·ConvAI)
  - [`fal-gateway`](moai-media/skills/fal-gateway/SKILL.md): fal.ai 1000+ 모델 통합 게이트웨이
- 번들 MCP 서버 2종 (`moai-media/.mcp.json`)
  - `fal-ai` (hosted HTTP MCP at `https://mcp.fal.ai/mcp`)
  - `elevenlabs` (local stdio via `uvx elevenlabs-mcp`)
- API 키 3종 통합 지원
  - `GEMINI_API_KEY` (nano-banana 전용 + 레거시 `NANO_BANANA_API_KEY` 호환)
  - `FAL_KEY` (ideogram / kling / fal-gateway 공유)
  - `ELEVENLABS_API_KEY` (elevenlabs)
- `moai-media/scripts/generate_image.py` v4.3 — Python 3.13+ 타입힌트, REST camelCase 준수, 서로게이트 sanitize
- 문서: `CLAUDE.local.md` § 4 MCP 번들 정책, § 5 외부 API 모델 ID 업데이트 정책
- 루트 `README.md` 전면 갱신 (17 플러그인 / 70 스킬 / moai-media 상세 섹션)

### Changed

- **공식 Nano Banana 2종 체제 확정**
  - `nano-banana-pro` → `gemini-3-pro-image-preview` (2K 기본, 텍스트 SOTA)
  - `nano-banana-2` → `gemini-3.1-flash-image-preview` (1K 기본, 비용 효율)
  - Ultra·cheap·2.5-flash 등 부가 별칭은 제거 → Pro/2로 자동 승격 (코드 무수정 호환)
- **API 호출 스펙** (공식 문서 `ai.google.dev/gemini-api/docs/image-generation` 100% 정합)
  - 엔드포인트 `:predict` → `:generateContent`
  - 페이로드 `numberOfImages` + top-level `aspectRatio` → `imageConfig.aspectRatio` + `imageSize`
  - REST 응답 `predictions[].bytesBase64Encoded` → `candidates[].content.parts[].inlineData.data`
  - 화면비 공식 14종 (`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`)
  - 해상도 `"512"` / `"1K"` / `"2K"` / `"4K"`
- `generate_image.py` 이관: `moai-content/scripts/card-news/` → `moai-media/scripts/`
  (v3.0 Imagen 4 → v4.3 Gemini 3 Image Preview)
- `moai-content/skills/card-news/SKILL.md`: 이미지 생성을 `moai-media/nano-banana` 위임 구조로 전환
- `moai-core/skills/moai/references/core/init-protocol.md`: API 키 테이블 4개 → 6개 확장
- `.claude-plugin/marketplace.json`: `moai-media` 엔트리 추가

### Removed

- Veo 3.1 관련 참조 (영상은 Kling 단일화)
- `gemini-2.5-flash-image` 모델 매핑
- `nano-banana-ultra` 별칭 및 `ULTRA_ALIASES` 상수
- `moai-content/scripts/card-news/` 디렉토리 (moai-media로 이관)
- v1.0.x 잔존 로컬 태그 (v1.1.0~v1.3.0) — marketplace 버전 체계와 불일치하여 정리

### Migration

v1.0.x 사용자 조치 3단계:

1. **마켓플레이스 새로고침**
   ```
   /plugin marketplace update cowork-plugins
   /plugin install moai-media@cowork-plugins
   ```

2. **Gemini API 업그레이드**
   - Pay-as-you-go 결제 활성화 필수 (Nano Banana Pro/2 Free Tier 불가)
   - `NANO_BANANA_API_KEY` 그대로 사용 가능 (자동 인식), 혹은 `GEMINI_API_KEY`로 재명명 권장

3. **신규 API 키 (선택, moai-media 전체 사용 시)**
   - `FAL_KEY` — [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) ($5 무료 크레딧)
   - `ELEVENLABS_API_KEY` — [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) (무료 10K char)
   - `uv` 설치 (ElevenLabs MCP용): `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Breaking

- **이미지 모델 ID 변경**: 기존 `imagen-4.0-*` 하드코딩은 Pro/2로 자동 승격되나, 장기적으로 `gemini-3-pro-image-preview` / `gemini-3.1-flash-image-preview` 직접 사용 권장
- **엔드포인트 변경**: 자체 스크립트를 복사·수정하여 사용하던 사용자는 `:predict` → `:generateContent` 및 페이로드 스키마 업데이트 필요 (참고: `moai-media/scripts/generate_image.py` v4.3)
- **무료 티어 불가**: Gemini 무료 키로 Nano Banana 호출하던 워크플로우는 Pay-as-you-go 전환 필요
- **`google-media` 스킬 경로 없음**: v1.1.0 잠깐 존재했던 `moai-media/skills/google-media/` 경로는 `nano-banana`로 개명됨 (v1.1.0 직후 설치한 극소수 사용자만 해당)

### 변경 이력 (v1.1.x 누적)

v1.2.0에 집약된 중간 릴리스:
- v1.1.0: moai-media 초기 릴리스 (6 스킬, google-media 포함)
- v1.1.1: google-media → nano-banana 개명, Veo 제거, 화면비 공식 14종 정정
- v1.1.2: Pro + 2 체제로 축약 (gemini-2.5-flash-image 제거)
- v1.1.3: nano-banana-ultra 제거, Ultra 별칭 자동 승격

---

## [1.1.3] - 2026-04-14

### Removed

- **`nano-banana-ultra` 별칭 제거** — 공식 라인업을 Pro + 2 **단 두 가지**로 최종 확정
- `ULTRA_ALIASES` 상수 및 `is_ultra` 분기 로직 삭제 (`scripts/generate_image.py`)
- 4K 해상도 자동 선택 로직 제거 — 필요 시 스크립트에서 `imageSize` 직접 지정
- `moai-content/skills/card-news/SKILL.md`의 Ultra 옵션 제거

### Changed

- **자동 승격 테이블 확장** (무수정 호환)
  - `"nano-banana-ultra"`, `"ultra"` → `gemini-3-pro-image-preview` (Pro로 승격)
  - `"nano-banana"`, `"cheap"` → Pro / 2로 승격 (v1.1.2 동일)
- 경고 메시지 개선: 제거된 별칭 사용 시 자동 전환 사실을 stderr로 명시
- `generate_image.py` v4.2 → v4.3 — MODEL_MAP·해상도 선택 로직 단순화
- `nano-banana` SKILL.md 비용 표 Pro/2 기준으로 재작성

### Migration

기존 `nano-banana-ultra` 호출 코드는 **무수정 작동** — 자동으로 Pro 2K로 처리되며 경고 출력. 4K가 필요하면 스크립트에서 `imageSize` 필드를 직접 `"4K"`로 수정.

---

## [1.1.2] - 2026-04-14

### Changed

- **`nano-banana` 스킬 공식 모델 2종 체제로 단순화**
  - 공식 라인업: `nano-banana-pro` (`gemini-3-pro-image-preview`) + `nano-banana-2` (`gemini-3.1-flash-image-preview`) **두 가지만**
  - `nano-banana-ultra`는 Pro의 4K 프리셋 (별도 모델 아님)
  - v1.1.1에서 도입한 `gemini-2.5-flash-image` (원조 Nano Banana) 제거 — 사용자 혼선 방지
- **레거시 별칭 자동 승격**
  - `"nano-banana"` 별칭 → `gemini-3-pro-image-preview` (v1.1.1에서는 `gemini-2.5-flash-image`)
  - `"cheap"` 별칭 → `gemini-3.1-flash-image-preview` (v1.1.1에서는 `gemini-2.5-flash-image`)
  - 사용자 코드 무수정 작동 보장
- **`image_size` 필수 적용** — 모든 요청에 `imageConfig.imageSize` 포함 (2.5-flash 미지원 케이스 삭제)
- **`generate_image.py` v4.1 → v4.2** — MODEL_MAP 정리, is_ultra 로직 단순화

### Fixed

- README 스킬 설명 "Pro/2/원조" → "Pro + 2, 2종만"으로 정확화
- SKILL.md 모델 카탈로그 표를 Pro/2/Ultra 3행으로 축소

### Migration

기존 사용자 조치 없음. `nano-banana` / `cheap` 별칭을 쓰던 코드는 그대로 작동 (자동 승격).

---

## [1.1.1] - 2026-04-14

### Changed

- **`moai-media` 스킬 구조 개편** (Google 공식 문서 재확인 반영)
  - `google-media` 스킬 → **`nano-banana`**로 개명 및 **이미지 전용**으로 스코프 축소
  - 영상 생성은 **`kling` 스킬로 단일화** — Veo 3.1 참조 모두 제거
  - 결과: 이미지는 `nano-banana` (Gemini) / `ideogram` (fal.ai), 영상은 `kling` 단독
- **Gemini 이미지 모델 카탈로그 공식화** (공식 문서 `ai.google.dev/gemini-api/docs/image-generation` 기준)
  - `gemini-2.5-flash-image` 모델 신규 추가 — 원조 Nano Banana, 최저가 **$0.039/img**
  - `nano-banana` 별칭 매핑: → `gemini-2.5-flash-image`
  - 모델 별 기본 해상도 자동 선택: Pro=2K, 2=1K, 원조=디폴트, Ultra=4K
- **공식 화면비 14종 리스트 재정의**
  - 구 리스트 (잘못됨): `9:21`, `3:5`, `2:1`, `1:2` 포함
  - 신 리스트 (공식): `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`
- **REST API 페이로드 정합화**
  - camelCase로 통일 (`responseModalities`, `imageConfig`, `aspectRatio`, `imageSize`) — 공식 REST 스펙 준수
  - 응답 파싱은 `inlineData` 우선, `inline_data` 폴백
  - `imageSize` 지원 값 공식화: `"512"`, `"1K"`, `"2K"`, `"4K"` (이전에 `"512"` 누락)
- **`generate_image.py` v4.0 → v4.1**
  - 위 변경사항 반영, MODEL_MAP에 `"nano-banana"` / `"cheap"` 별칭 추가
  - `gemini-2.5-flash-image`는 `image_size` 미지원 → 페이로드에서 생략 처리 로직 추가

### Fixed

- **공식 문서 불일치 수정** — 기존 v1.1.0에서 파생 지식 기반으로 작성한 화면비 리스트가 공식 스펙과 달랐음. WebFetch로 공식 문서 재확인 후 전면 정정.
- `moai-core/init-protocol.md`의 "moai-media/google-media 스킬" 참조를 `nano-banana`로 수정

### Removed

- `moai-media/skills/google-media/` 스킬 디렉토리 전체 (→ `nano-banana`로 개명)
- Veo 3.1 관련 모든 참조:
  - README.md 스킬 카탈로그·영상 선택 가이드
  - CONNECTORS.md API 설명
  - plugin.json keywords (`"veo"` 제거)
  - marketplace.json 플러그인 description
  - 기타 SKILL.md 크로스 레퍼런스
- `plugin.json` keywords에서 `"veo"` 제외

### Migration

v1.1.0에서 방금 설치한 사용자도 즉시 업데이트 필요:

```
/plugin marketplace update cowork-plugins
```

기존 `google-media` 호출 코드가 있다면 **`nano-banana`**로 경로 변경:
- 스킬 호출: `/moai-media google-media` → `/moai-media nano-banana`
- SKILL.md 참조: `moai-media/skills/google-media/` → `moai-media/skills/nano-banana/`

영상 생성이 필요하면 **`kling` 스킬** 사용:
- 숏폼·릴스·쇼츠: `fal-ai/kling-video/v3/text-to-video`
- 립싱크 프리미엄: Kling Pro 모드

### Breaking

- **스킬 경로 변경**: `moai-media/skills/google-media/` → `moai-media/skills/nano-banana/`
- **Veo 사용 불가**: v1.1.0에서 `veo-3.1-generate-preview` 호출하던 워크플로우는 `kling` 또는 외부 Veo 직접 호출로 마이그레이션 필요

---

## [1.1.0] - 2026-04-14

### Added

- **신규 플러그인 `moai-media`** — AI 미디어 스튜디오 (이미지·영상·음성 통합)
  - [`moai-media/skills/google-media/`](moai-media/skills/google-media/SKILL.md): Google Gemini 3 Image Preview + Veo 3.1 통합 스킬
    - Nano Banana Pro (`gemini-3-pro-image-preview`, 2K), Nano Banana 2 (`gemini-3.1-flash-image-preview`, 1K), Nano Banana Ultra (Pro + 4K)
    - Veo 3.1 Standard/Fast 영상 (최대 8초, 1080p, 오디오 자동 생성)
    - 단일 `GEMINI_API_KEY`로 이미지 + 영상 + 텍스트 모두 호출
  - [`moai-media/skills/ideogram/`](moai-media/skills/ideogram/SKILL.md): Ideogram 3.0 (한국어 타이포그래피 렌더링 업계 최고)
  - [`moai-media/skills/kling/`](moai-media/skills/kling/SKILL.md): Kling 3.0 (숏폼 영상, 다국어 립싱크, Veo 대비 1/5 가격)
  - [`moai-media/skills/elevenlabs/`](moai-media/skills/elevenlabs/SKILL.md): ElevenLabs 공식 MCP (TTS, 음성복제, 32개 언어 더빙, ConvAI)
  - [`moai-media/skills/fal-gateway/`](moai-media/skills/fal-gateway/SKILL.md): fal.ai 통합 MCP 게이트웨이 (Flux, Recraft, Hailuo, Luma, Pika, MiniMax Music 등 1000+ 모델)
- **MCP 서버 자동 등록** — `moai-media/.mcp.json`에 2종 사전 구성
  - `fal-ai` (hosted HTTP MCP at `https://mcp.fal.ai/mcp`, `FAL_KEY` 인증)
  - `elevenlabs` (local stdio MCP via `uvx elevenlabs-mcp`, `ELEVENLABS_API_KEY` 주입)
- **API 키 2종 신규 지원**: `FAL_KEY`, `ELEVENLABS_API_KEY` (기존 `NANO_BANANA_API_KEY` 유지)
- **4K 이미지 해상도** 지원 (`image_size="4K"`, Nano Banana Ultra 전용)
- **14종 화면비 지원** (1:1 ~ 21:9, Gemini 3 Image Preview 기본 스펙)
- [`moai-media/CONNECTORS.md`](moai-media/CONNECTORS.md): API 키·MCP·커넥터 통합 가이드

### Changed

- **Google "Nano Banana" 브랜드 재정의 반영** (2026 Q1 공식 공지 반영)
  - 모델 ID 매핑: `imagen-4.0-generate-001` → **`gemini-3-pro-image-preview`**
  - 모델 ID 매핑: `imagen-4.0-fast-generate-001` → **`gemini-3.1-flash-image-preview`**
  - 엔드포인트 변경: `:predict` → **`:generateContent`**
  - 파라미터 스키마: `numberOfImages` + top-level `aspectRatio` → **`imageConfig.aspect_ratio` + `imageSize`**
  - 응답 파싱: `predictions[].bytesBase64Encoded` → `candidates[].content.parts[].inline_data.data`
  - ⚠️ **유료 플랜 필수**: Nano Banana Pro/2 및 Veo 3.1은 무료 티어 호출 불가
- **`generate_image.py` 이관 및 v3.0.0 → v4.0.0 마이그레이션**
  - 경로: `moai-content/scripts/card-news/generate_image.py` → **`moai-media/scripts/generate_image.py`**
  - Gemini 3 Image Preview API 스키마로 전면 재작성
  - Python 3.13+ 스타일 (`from __future__ import annotations`, `TypedDict`, PEP 604 union types)
  - 환경변수 우선순위: `GEMINI_API_KEY` > `NANO_BANANA_API_KEY` (레거시 호환 유지)
  - 키 파일 탐색 확장: `~/.gemini-api-key` 추가, `moai-credentials.env`에서 두 키 모두 인식
  - 서로게이트 sanitize 로직 v3.0 수준 유지 (한국어·이모지 안전)
- `moai-content/skills/card-news/SKILL.md`: 이미지 생성 섹션을 **moai-media 플러그인 위임 구조**로 전환
  - API 키 안내를 `NANO_BANANA_API_KEY` → `GEMINI_API_KEY`로 업데이트 (레거시 변수명도 인식됨 명시)
  - 모델 옵션 문구에 실제 Gemini 3 Image Preview 모델 ID 부기
  - 스크립트 경로 참조: `scripts/card-news/generate_image.py` → `moai-media/scripts/generate_image.py`
- **전체 버전 bump 1.0.3 → 1.1.0** (87 지점)
  - marketplace.json × 1
  - plugin.json × 17 (기존 16 + 신규 moai-media)
  - SKILL.md × 70 (기존 65 + 신규 5)
- `.claude-plugin/marketplace.json`: `moai-media` 플러그인 엔트리 추가

### Migration

**v1.0.x 사용자 조치 사항**:

1. **Google API 키 업그레이드**
   - 환경변수를 `NANO_BANANA_API_KEY` → `GEMINI_API_KEY`로 변경 권장 (구 변수명도 인식됨)
   - Gemini API 콘솔에서 **Pay-as-you-go 결제 활성화** 필수 (Nano Banana Pro/2 무료 티어 불가)

2. **신규 API 키 발급 (moai-media 사용 시)**
   - [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) → `FAL_KEY`
   - [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) → `ELEVENLABS_API_KEY`

3. **`uv` 설치 (ElevenLabs MCP용)**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **플러그인 마켓플레이스 새로고침**
   ```
   /plugin marketplace update cowork-plugins
   /plugin install moai-media@cowork-plugins
   ```

### Breaking

- **`scripts/card-news/generate_image.py` 경로 이동** — `moai-content/scripts/` 경로를 직접 참조하던 외부 스크립트는 `moai-media/scripts/`로 경로 변경 필요
- **엔드포인트 변경** — 구 스크립트를 복사하여 자체 수정해 사용하던 사용자는 `:predict` → `:generateContent` 전환 및 페이로드 스키마 업데이트 필요 (v4.0.0 `generate_image.py` 참고)
- **무료 티어 불가** — 기존 Gemini API 무료 키로 Nano Banana 호출하던 워크플로우는 Pay-as-you-go 활성화 필요

### Removed

- `moai-content/scripts/card-news/generate_image.py` (moai-media로 이관)
- `moai-content/scripts/` 빈 디렉토리 제거

---

## [1.0.3] - 2026-04-14

### Added
- `CHANGELOG.md`: Keep a Changelog 형식 공식 도입 및 엔트리 템플릿 정의
- `CLAUDE.local.md`: 저장소 로컬 지침 신규 작성
  - 버저닝 정책 (HARD): 82개 지점 동기화 절차 및 검증 명령
  - 플러그인 컴포넌트 규격: SKILL.md `user-invocable` 필수 명시
  - 릴리스 후 사용자 안내 템플릿 (`/plugin marketplace update`)
  - 태그 히스토리 관리 규정

### Changed
- **전체 버전 통일 (82 지점)**: 모든 버전 표기를 `1.0.3`으로 강제 일치
  - `.claude-plugin/marketplace.json`: `metadata.version`
  - `moai-*/.claude-plugin/plugin.json` × 16: `version` 필드
  - `moai-*/skills/*/SKILL.md` × 65: `metadata.version` 필드
  - 이전 상태: 대부분 `1.0.0` 잔존, 일부 파일만 개별 bump되어 불일치 상태였음
- `moai-core/skills/moai/SKILL.md` 본문 뱃지: `v1.0.0` → `v1.0.3`

### Fixed
- **`/moai` 슬래시 자동완성 미작동 문제** (#user-report)
  - 증상: Claude Code에서 `/moai` 입력 후 Tab 눌러도 자동완성 목록에 노출되지 않음
  - 원인: `moai-core/skills/moai/SKILL.md` frontmatter에 `user-invocable: true` 플래그 누락.
    Claude Code는 이 플래그가 `true`인 스킬만 슬래시 메뉴에 사용자 호출 가능 항목으로 등록함
  - 추가 원인: 비표준 `keywords` 필드 사용 (Claude Code 스펙 미지원)
  - 해결:
    1. `user-invocable: true` 추가
    2. `keywords` → 표준 `metadata.tags`로 이전
    3. `metadata.version`/`status`/`updated` 메타데이터 완성
- `moai-core/skills/feedback/SKILL.md` 버전 필드가 `1.0.0`에 고정되어 다른 파일과 불일치하던 문제 수정

### Removed
- 불필요한 로컬 Git 태그 정리: `v1.1.0`, `v1.2.0`, `v1.3.0`
  - 사유: `marketplace.json` 버전(`1.0.x` 트랙)과 태그 체계(`v1.x.0`)가 어긋나 혼란 유발
  - 원격 태그 `v1.1.0`도 함께 삭제 (푸시 전 단일 상태로 정리)

### Migration
사용자 측에서 신버전 반영 필요:
```
/plugin marketplace update cowork-plugins
```
이후 플러그인 상세 화면 재진입 시 `1.0.3`으로 표시되며 `/moai<Tab>` 자동완성 활성화됨.

### Breaking
없음. Frontmatter 필드 추가·정규화만 수행하여 기존 동작은 완전 호환.

---

## [1.0.2] - 2026-04-12

### Added
- `moai-core/skills/feedback/`: 버그/기능 요청 GitHub Issues 자동 등록 스킬
- `moai-office/skills/pptx-designer/`: NotebookLM 스타일 프롬프트 + 인포그래픽 선택 옵션

### Changed
- `README.md`: 퍼블릭 공개용 개편 (뱃지, 목차, 기여/문의 섹션 추가)
- 전 플러그인 스킬 테이블에 한글명 컬럼 추가 (65개 스킬)

### Fixed
- API 키와 Cowork 커넥터 혼동 방지 규칙 강화 (init 플로우 전반)
- API 키 가이드를 4개로 정리: DART/KOSIS/KCI 통합, 네이버·구글 API 제거
- `init` 안내 목록 외 서비스(네이버 API 등) 언급 금지 규칙 추가

---

## [1.0.1] - 2026-04-11

### Changed
- `init` 플로우의 모든 사용자 질문을 `AskUserQuestion` 도구로 통일

---

## [1.0.0] - 2026-04-08

### Added
- 초기 마켓플레이스 공개: 16개 플러그인, 64개 스킬
- `moai-core`: 도메인 AI 라우터 + 자가학습 엔진 (`/project init`, `/project catalog`)
- 도메인 플러그인 15종:
  business, marketing, legal, finance, hr, content, operations,
  education, lifestyle, product, support, office, career, data, research
