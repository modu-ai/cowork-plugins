# Changelog

모든 주목할 만한 변경사항은 이 파일에 기록됩니다.

형식: [Keep a Changelog 1.1.0](https://keepachangelog.com/ko/1.1.0/) · 버저닝: [Semantic Versioning 2.0.0](https://semver.org/lang/ko/)

## 버전 통일 원칙 (HARD)

아래 209개 지점의 버전 표기는 **항상 완전히 동일**합니다 (v2.11.1+ `hugo.toml` SSOT 별도 추적):
- `.claude-plugin/marketplace.json` (`metadata.version`) × 1
- `<plugin>/.claude-plugin/plugin.json` (`version`) × 28 (v2.20.0+)
- `<plugin>/skills/<skill>/SKILL.md` (`version:` frontmatter) × 176 (v2.25.0: stub 2개 제거)
- `docs-site/hugo.toml` (`[params] version`) × 1 (v2.11.1+ SSOT, 좌측 사이드바·footer 자동 반영)

상세 정책: `CLAUDE.local.md` § 1 참조.

## [2.27.0] - 2026-06-19

MINOR. **design-system-library 56 → 75종 확장 (getdesign.md 74종 컬렉션 통합)**. `테마_컴포넌트_쇼케이스_전체.html`의 getdesign.md 74종 컬렉션에서 19개 신규 브랜드(airbnb·airtable·apple·binance·bmw·bmw-m·bugatti·cal·dell-1996·hp·linear.app·nintendo-2001·stripe·supabase·vercel·voltagent·warp·webflow·wired)를 design-system-library에 추가. html-slide·html-report의 design_system 선택지가 75종으로 확장, 강연/발표 맥락 추천 가이드(비개발자·라이트 안전) 반영. 28 플러그인 / 176 스킬 유지. 동기화 2.26.0 → 2.27.0. 기능적 비파괴. Breaking change 없음.

### Added
- **19개 신규 디자인 시스템** (design-system-library/systems/) — `테마_컴포넌트_쇼케이스_전체.html`에서 토큰 추출. light 10개(airbnb·airtable·apple·cal·dell-1996·hp·nintendo-2001·stripe·webflow·wired) + dark 9개(binance·bmw·bmw-m·bugatti·linear.app·supabase·vercel·voltagent·warp). frontmatter(colors/typography/rounded) 형식으로 design_system 파라미터 즉시 소비 가능.

### Changed
- **html-slide·html-report design_system 75종화** — 테마별 적합 슬라이드 추천표에 강연 맥락 가이드(비개발자 청중·프로젝터 → 라이트 안전) 추가. design-system-links.md getdesign.md 매핑 74종 확장. registry.md 75개 카탈로그(light 48/dark 25/warm 2) 재분류. design-system-library SKILL·README·claude-design-system-prep·pptx-chaining 56→75 정합.
- 19개 신규 시스템은 경량 토큰(⚙️ 표기) — 풍부한 브랜드 분석·typography 스케일은 추후 보강.

## [2.26.0] - 2026-06-19

MINOR. **Cowork 베스트프랙티스 정렬 — 매니페스트 현대화 + orphan 스킬 발견성 개선**. Claude Cowork 공식 플러그인 모델(Connectors·Instructions·Skills 3-Level) 대비 갭을 진단하고 저위험 고수익 개선을 적용했습니다. 28 플러그인에 한글 `displayName`을 추가해 Cowork `/plugin` UI 가독성을 높이고, orphan 스킬 12개를 commerce 코디네이터에 매핑했습니다. 28 플러그인 / 176 스킬 유지. 동기화 2.25.0 → 2.26.0. 기능적 비파괴. Breaking change 없음.

### Added
- **28개 plugin.json 한글 `displayName`** — Cowork `/plugin` 피커·마켓플레이스 UI에서 한글 역할명 표시(moai-business→"비즈니스 전략"·moai-commerce→"한국 이커머스" 등). 공식 plugins-reference `displayName` 필드(v2.1.143+) 채택.
- **moai-media `defaultEnabled: false`** — 외부 API 키(Higgsfield OAuth·ElevenLabs) 의존 플러그인을 신규 설치 시 비활성 상태로 배포(공식 v2.1.154+). 기존 사용자는 활성 상태 유지(호환).
- **skill-only 플러그인 4개 설계 노트** — moai-bi·moai-lifestyle·moai-pm·moai-tutor README에 "코디네이터 없이 스킬 직접 호출 전용(의도적 설계)" 명시.

### Changed
- **commerce 코디네이터 2개 orphan 스킬 매핑** — `commerce-launch-coordinator`에 marketplace-*(coupang·naver·d2c·curation·crowdfunding)·coupang-ad-optimizer·live-commerce·season-calendar, `commerce-growth-analyst`에 early-fan-builder·influencer-collab·voc-triage·morning-brief 참조 추가. 발견성(자동 호출 강화) 개선.

## [2.25.0] - 2026-06-19

MINOR. **28 플러그인 전수 품질 감사 + pdf-writer weasyprint 재작성 + 리다이렉트 stub 2개 제거**. 사용자가 "PDF로 생성"을 요청해도 `moai-office:pdf-writer`가 발동하지 않던 근본 원인(CJK 전문가 프레이밍에 치우친 트리거 + PyMuPDF의 HTML 충실도 한계)을 해소하고, 28개 플러그인의 스킬·에이전트·커넥터 지침을 전수 감사해 끊긴 교차참조·dead-reference·미번들 MCP 호출·노후 사실·중복 스킬을 정정했습니다. 리다이렉트 stub 2개 제거로 178 → **176 스킬**. 28 플러그인 유지 · 동기화 2.24.1 → 2.25.0. 기능적 비파괴(스킬 트리거·문서 정확도 개선). Breaking change 없음.

### Added
- `moai-office/skills/pdf-writer/scripts/render_pdf.py` — weasyprint 단일 엔진 PDF 렌더러(HTML/Markdown/JSON/Text → HTML → weasyprint). 스타일 HTML 리포트의 디자인을 그대로 보존하며 번들 Noto Sans CJK를 `@font-face`로 임베딩해 한·중·일 글리프 깨짐 방지.

### Changed
- **pdf-writer weasyprint 단일 엔진 재작성** — PyMuPDF 좌표 기반 렌더링을 폐기하고 weasyprint 풀 CSS 충실 렌더로 통일. 트리거를 일반 표현("PDF로 만들어줘"·"이 리포트 PDF로"·"HTML을 PDF로"·"PDF로도 생성")으로 대폭 보강 + "weasyprint를 직접 설치·호출하지 말고 이 스킬 사용" 포지셔닝 명시.
- **산출물 스킬 발동 포지셔닝 강화** — office(docx·pptx·xlsx·hwpx) "Claude 기본 생성 대신 이 스킬 사용" 추가, media(higgsfield-image/video) 생성 포지셔닝, html-report·html-slide → pdf-writer PDF 핸드오프 신설.
- **딥 콘텐츠 감사 정정(26 플러그인)** — Core Web Vitals FID→INP(2024-03 공식 대체), G마켓/옥션 운영사 이베이코리아→지마켓(2021 신세계), Mermaid bar→xychart-beta, 나라장터 ActiveX→웹표준(2024 차세대), 자살예방·정신건강 위기상담 1577-0199→109(2024 통합), sequential-thinking MCP 호출 12곳을 미설치 시 일반 추론 fallback으로 완화. 세법·개인정보보호법 과징금·4대보험 요율·웨딩 의무화·ESG 공시 등 미검증 도메인 수치는 공식 출처 참조로 완화(verification-claim-integrity 준수 — 새 수치 단정 회피).
- **deprecated/dead 참조 정정** — `moai-content:social-media`(deprecated) 참조 7곳 → `moai-marketing:sns-content`, dead reference(realtime-patterns.md·python-docx-patterns.md·init-protocol.md) 정정, 끊긴 cross-ref 5곳(`moai-media:image-gen`→`higgsfield-image` 등) 수정.
- **31 코디네이터 에이전트 정합** — 전 플러그인 번들 코디네이터 `model: sonnet → inherit`(메인 세션 사용자 선택 모델 승계) + 역할별 `effort`(low 3·medium 14·high 13·xhigh 1). `/project` 생성 에이전트 기본 tools에서 Bash 제거(Cowork-safe).

### Removed
- **리다이렉트 stub 2개 제거** — `moai-core:ai-diagnostic`(→`moai-business:ai-diagnostic`), `moai-education:course-curriculum-design`(→`moai-education:course-operations-manual`). user-invocable 리다이렉트 전용 스킬로 `/ai-diagnostic` 이름 충돌·카운트 부풀림 유발. 178 → 176 스킬 + 참조·README·router·docs-site·NOTICE 전 지점 cascade 정합.

### Fixed
- 오탈자 — 실간→실시간, 체이션→리텐션, 국세천→국세청, 선행연조사→선행연구 조사. `book-publisher-matcher` 중첩 코드펜스 렌더링 깨짐, design `registry.md` 휘도 카운트(33/13→38/16), `claude-design-prompt-builder` "전부 포함" 과장 등 내부 모순 정정.

## [2.24.1] - 2026-06-17

PATCH. **보안 의존성 fix + docs-site 정리**. moai-ads-audit MCP 서버의 Python transitive 의존성 취약점(Dependabot 15 alerts) 해소 — pyproject.toml에 보안 constraints 추가 + uv.lock 갱신(4패키지 fix 버전). docs-site 부채 정리: moai-education course-curriculum-design(rename 스템) → course-operations-manual 정식 이름 통일; moai-media/agents media-production-pipeline 이미지 백엔드 정책 반영. 28 플러그인 / 178 스킬 유지 · 동기화 2.24.0 → 2.24.1. 기능적 비파괴. Breaking change 없음.

### Fixed
- **moai-ads-audit MCP 보안 의존성 fix** — Dependabot 15 alerts(PyJWT·starlette·cryptography·python-multipart, 5 high·5 medium·5 low, 전부 fix available) 해소. pyproject.toml 보안 constraints 추가 + uv.lock 갱신(cryptography v48.0.0→49.0.0, pyjwt v2.12.1→2.13.0, python-multipart v0.0.28→0.0.32, starlette v1.0.0→1.3.1). 취약 패키지는 mcp SDK의 transitive 의존성.

### Changed
- docs-site `moai-education`: `course-curriculum-design`(rename 스템) → `course-operations-manual` 정식 이름으로 통일(표 중복 행 제거 + 본문/mermaid 참조 일괄 변경)
- `moai-media/agents/media-production-pipeline.md`: 이미지 백엔드 정책(Higgsfield + codex) 반영, 허용 백엔드 명시

## [2.24.0] - 2026-06-17

MINOR. **`html-slide` 신규 스킬 (moai-content) — 단일 파일 HTML 슬라이드 덱 + 편집 가능 PPTX + 인라인 SVG 인포그래픽 + getdesign.md 미리보기**. 발표용 슬라이드 덱을 브라우저에서 바로 열리는 단일 파일·자체 완결형 HTML로 생성합니다. 인포그래픽(차트·다이어그램·KPI)은 한국어 숫자·라벨이 100% 정확한 인라인 SVG로 직접 렌더링, 실사 히어로 이미지는 Higgsfield MCP 또는 codex(gpt-image-2)로 생성합니다. design-system-library 56개 브랜드 토큰 중 테마 선택 시 각 토큰별 getdesign.md 상세 페이지 링크로 미리보기 제공. 편집 가능 PPTX는 pptx-designer(moai-office) 체이닝으로 산출(deck.json 원고 → pptxgenjs OOXML 직접 생성). 28 플러그인(유지) · 177 → 178 스킬(+html-slide 1개) · 동기화 2.23.0 → 2.24.0. 기능적 비파괴. Breaking change 없음.

### Added
- **`html-slide` 신규 스킬 (moai-content)** — 단일 파일 무의존 HTML 슬라이드 덱(자체 vanilla JS 런타임, 16:9, `?print-pdf` 인쇄 모드, speaker notes, 0의존, file:// 즉시 오픈). 인포그래픽은 LLM 직접 인라인 SVG(한국어 숫자/라벨 100% 정확). 이미지 백엔드: Higgsfield MCP(기본) + codex(gpt-image-2, 공식 추가 2026-06-17). design-system-library 56 브랜드 토큰 + getdesign.md 링크 미리보기. 편집 가능 PPTX는 pptx-designer 체이닝(deck.json 원고 SSOT → OOXML). 스킬 파일 9개(SKILL.md + references 6 + samples 2).
- **이미지 백엔드 정책 변경** — Higgsfield MCP 단일에서 Higgsfield + codex(gpt-image-2) 복수로 확장(GOOS 결정 2026-06-17). codex exec 내장 image_gen이 gpt-image-2를 ChatGPT OAuth 구독 한도로 호출(API 키 불필요). antigravity(agy -p)는 OAuth 브라우저·quota·CI 무인 불가로 비권장 문서화. 그 외 외부 이미지 백엔드(MCP·API·게이트웨이)는 사용하지 않습니다.

### Changed
- docs-site 스킬 카운트 177 → 178 (`_index.md` 5곳, cookbook 6종, `plugins/moai-content.md`)
- docs-site 부채 정리: `moai-business`(ai-diagnostic)·`moai-education`(course-operations-manual) 표 누락 스킬 추가; `moai-content` media-production/social-media 레거시 정체 메모 정확화(social-media=DEPRECATED 흡수, media-production=분리 별칭)
- `moai-content` 스킬 수 14 → 15 (html-slide)
- `evaluation-protocol.md` 볼드+괄호 한글 렌더링 버그 정정(CLAUDE.local.md §10-5)

## [2.23.0] - 2026-06-16

MINOR. **`drawio-diagram` 스킬 제거 (moai-content)** — `viewer-static.min.js` CDN 렌더링이 drawio XML마다 불안정(검증 21개 중 2개만 성공)하여 스킬 가치를 훼손합니다. 배포용 스킬에서 제거하고 다이어그램은 **mermaid(인라인, 안정)**로 통일했습니다. 로컬 문서 정교 도식은 draw.io desktop CLI(로컬 전용)로 SVG 생성. 28 플러그인(유지) · 178 → 177 스킬 · 동기화 2.22.0 → 2.23.0. 기능적 비파괴(기존 플러그인·스킬·인터페이스 무변경). Breaking change 없음.

### Removed
- **`drawio-diagram` 스킬 제거 (moai-content)** — `viewer-static.min.js` CDN 렌더링이 drawio XML마다 불안정(검증 21개 중 2개만 성공)하여 스킬 가치를 훼손합니다. 배포용 스킬에서 제거하고, 다이어그램은 **mermaid(인라인, 안정)**를 기본으로 통일했습니다. docs-site 등 로컬 문서의 정교 도식은 **draw.io desktop CLI(`brew install --cask drawio`, 로컬 전용)**로 SVG를 생성해 마크다운 이미지로 인라인 사용합니다(CLAUDE.local.md §10-6). **28 플러그인 유지 · 178 → 177 스킬**. `moai-tutor:learning-material`의 ```drawio` 블록 지원도 제거(mermaid로 수렴).

## [2.22.0] - 2026-06-16

MINOR. **`design-system-library` 신규 스킬(moai-design) — 56개 글로벌 브랜드 디자인 시스템 → Tailwind Play CDN + shadcn vanilla HTML**. HTML 보고서·랜딩·문서에 즉시 적용 가능한 브랜드 디자인 시스템 라이브러리를 추가했습니다. 28 플러그인(유지) · 177 → 178 스킬(+design-system-library 1개) · 동기화 2.21.0 → 2.22.0. 기능적 비파괴(기존 플러그인·스킬·인터페이스 무변경). Breaking change 없음.

### Added

- **`design-system-library` 신규 스킬 (moai-design)** — Claude·ClickHouse·Clay 기본 3테마 + 글로벌 56종 브랜드(Notion·Linear·Stripe·Vercel·Figma·Sentry·Raycast·Mintlify 등) 디자인 시스템 토큰(색·타이포·radius·spacing·컴포넌트)을 단일 진실 원천(single source of truth)으로 보관. 두 소비 경로: (1) `html-report`에 `design_system` 파라미터로 시스템 선택 → Tailwind Play CDN config + shadcn vanilla 컴포넌트로 단일 파일 HTML 렌더, (2) Claude Design 핸드오프 시 `claude-design-system-prep`가 DESIGN.md 합성 소스로 사용. 핵심 원칙: 라이브러리는 데이터 SSOT(렌더 로직은 소비자 html-report 소유), Tailwind Play CDN으로 외부 빌드 없이 브랜드 토큰 적용(인터넷 필요), shadcn 컴포넌트는 React가 아닌 vanilla HTML/CSS로 재현, 기존 html-report 0의존 템플릿 유지(design_system 미지정 시 하위 호환). 56개 중 48종 휘도 기반 분류(light 33·dark 13·warm 2) 완료, 8종(theverge·tesla·starbucks·spotify·mastercard·lovable·lamborghini·kraken) colors 구조 후속 보완 예정.

### Changed

- **스킬 카운트 177 → 178** — `design-system-library` 1개 신규(moai-design 5 → 6 스킬). 플러그인 28개 유지.
- **전체 버전 동기화 2.21.0 → 2.22.0** — marketplace.json + 28 plugin.json + 178 SKILL.md (208개 지점) + hugo.toml SSOT.

### Fixed

- 해당 없음.

### Removed

- 해당 없음.

## [2.21.0] - 2026-06-16

MINOR. **`drawio-diagram` 신규 스킬(moai-content) + `humanize-korean` 한국적 정서·결 K 카테고리 강화 + `/project` agent-aware 강화**. 콘텐츠·문서 작업의 도식 역량을 강화하고 한국적 정서 윤문 지식을 보강하며, `/project`가 코디네이터 에이전트까지 활용하도록 확장했습니다. 28 플러그인(유지) · 173 → 177 스킬(+drawio-diagram 1개) · 동기화 2.20.0 → 2.21.0. 기능적 비파괴(기존 플러그인·스킬·인터페이스 무변경). Breaking change 없음.

### Added

- **`drawio-diagram` 신규 스킬 (moai-content)** — 자연어를 편집 가능한 `.drawio` XML + 단일 HTML(draw.io CDN 뷰어 `viewer-static.min.js`, Apache-2.0) 두 산출물로 렌더. 6 프리셋(erd·uml-class·sequence·architecture·ml-pipeline·flowchart). CLI 설치 불필요(브라우저 즉시 열람, 폴백 시 XML 텍스트 보존). `html-report` 디자인 토큰·폰트 공유. 영감 출처 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)(MIT) → 자체 재구현(CLI 의존 제거, CDN 뷰어 전환).
- **`humanize-korean` 한국적 정서·결 K 카테고리 (taxonomy v2.1)** — 기존 A~J 음성(제거) 축에 **K 양성(지향) 축** 4종 추가: K-1 정서온도·K-2 절제·곡언·K-3 구어 호흡·여백·K-4 정서 아크. 본진 신규 E-8(다어절 띄어쓰기 기계적 균일성, S2)·E-7 보강(3단계 화계 framework)·머리말 모델별 번역투 시그니처 힌트. scholarship 섹션 KatFish 2025·LREAD 2026·translationese 2026 + caveat C7. 학술 근거 Park & Han 2026 LREAD(arXiv:2601.19913)·translationese(arXiv:2602.16469) 교차. 전부 자체저작·학술원전 직접 인용. **AC-003 A~J 10 유지(K는 양성 축 추가), 메트릭·테스트·baseline 무변경**(parity 안전).
- **`/project` agent-aware 강화 (moai-core)** — `/project init`이 스킬뿐 아니라 **코디네이터 에이전트**까지 활용하도록 강화. Phase 2 에이전트 인벤토리(설치된 플러그인 `agents/*.md` 동적 스캔) + Phase 3 코디네이터 우선 + 기존 에이전트 우선(stale 정정) + CLAUDE.md.tmpl §5.4 에이전트 체인 슬롯. 신규 `references/core/agent-catalog.md`(코디네이터 SSOT). +167/-27 (7 파일).

### Changed

- **스킬 카운트 173 → 177** — `drawio-diagram` 1개 신규(moai-content 14 → 15 스킬). 플러그인 28개 유지.
- **전체 버전 동기화 2.20.0 → 2.21.0** — marketplace.json + 28 plugin.json + 177 SKILL.md (206개 지점) + hugo.toml SSOT.
- **`moai-tutor:learning-material` drawio 연동** — ` ```drawio ` 블록 인식해 draw.io 뷰어 조건부 임베드(`references/cdn-libraries.md` §6 신규). mermaid는 유지.
- 루트 README·docs-site 카탈로그에 drawio-diagram 추가, 배지(177 스킬)·플러그인 스킬 수 표 갱신.
- **기존 부채 정합 — 5개 플러그인 README 스킬 테이블** — 게이트 4(스킬 테이블 실측 일치) 28/28 플러그인 달성. moai-business(`ai-diagnostic` 추가), moai-commerce(삭제 스킬 잔재 6행 제거 + `marketplace-coupang-ads` 추가), moai-education(`course-curriculum-design` rename stub 추가), moai-marketing(`meta-ads-manager` 추가), moai-media(`higgsfield-image`·`higgsfield-video` 추가). 각 플러그인 README 스킬 수 배지·도입부 카운트를 실측에 정합.

### Fixed

- 해당 없음.

### Removed

- 해당 없음.

---

## [2.20.0] - 2026-06-16

MINOR. **학습자 전용 `moai-tutor` 플러그인 신규 (3 스킬)**. 가르치는 사람(moai-education)과 분리된 **배우는 사람(학습자·수강생)** 도메인을 신설했습니다. 학습 질문을 context7(공식 문서)+웹검색(최신 정보)으로 **병렬** 조사·교차검증하고, mermaid 도식·차트·수식·코드 하이라이트가 **조건부로** 들어간 단일 HTML 학습자료를 자동 생성합니다. claude code·cowork·영어 등 어떤 주제든 스스로 깊이 학습하는 워크플로우입니다. 27 → 28 플러그인, 173 → 176 스킬, 동기화 2.19.0 → 2.20.0. 기능적 비파괴(기존 플러그인·스킬·워크플로우 무변경). 아울러 저장소 라이선스를 **MIT → NC-ND 1.0**으로 전환하고, `moai-content:humanize-korean`을 MIT 차용 의존 없이 **100% 자체 저작으로 재생성**(검증된 구조 보존 + 표현 전면 자체 저작, 기능 동등성 유지)했습니다.

### Added

- **`moai-tutor` 신규 플러그인 (3 스킬)** — 학습자 본인이 쓰는 개인 AI 튜터 도메인.
  - `learning-project` — 학습 목표·수준 진단, 단계별 로드맵(Bloom 6단계 골격), 진도 추적 + 학습 전용 `CLAUDE.md` 스캐폴딩. tutor-research·learning-material 체인의 출발점.
  - `tutor-research` — 질문을 리서치 축으로 분해해 context7(라이브러리·SDK·CLI 공식 문서)과 WebSearch(최신 트렌드·튜토리얼·비교)를 **한 턴에 병렬** 실행, 출처 교차검증 후 learning-material 입력 규격 종합본 생성. 광범위 주제는 `/deep-research` 제안. GLM 백엔드 웹 도구 라우팅 준수.
  - `learning-material` — 학습목표·핵심개념·도식·예제·복습 구조의 단일 HTML 학습자료 렌더러. `moai-content:html-report` 디자인 토큰·폰트 공유(html-report의 0-JS 원칙은 별도 보존).
- **context7 MCP 번들** — `moai-tutor/.mcp.json`에 context7(`alwaysLoad`)을 번들해 설치 시 라이브러리·SDK 공식 문서 조회가 함께 활성화됩니다. 별도 API 키 불필요(npx 자동 설치).
- **CDN 라이브러리 스택 SSOT** (`moai-tutor/skills/learning-material/references/cdn-libraries.md`) — 2026 영역별 최고 라이브러리 큐레이션: Mermaid v11(MIT)·Apache ECharts v5(Apache-2.0)·highlight.js v11(BSD-3)·KaTeX v0.16(MIT)·AOS v2(MIT) + 경량/고급 대안. 콘텐츠가 실제 쓸 때만 주입하는 **조건부 로딩** 규칙, 메이저 버전 핀, 오프라인 폴백, 라이선스 안전(CDN 런타임 로딩은 재배포 아님) 명시.

### Changed

- **라이선스 전환 MIT → NC-ND 1.0** — 루트 `LICENSE`를 비상업·변경금지(Non-Commercial No-Derivatives) 1.0으로 전환. 종전 MIT 릴리스는 `LICENSE.MIT`로 보존(해당 릴리스에 한해 계속 유효), 제3자 구성요소(Apache/MIT/OFL)는 `NOTICE.md`로 격리(LICENSE 제7조). 전체 plugin.json 28개 `license: LicenseRef-MoAI-NC-ND-1.0`.
- **`moai-content:humanize-korean` 라이선스 안전 자체 재생성** — MIT 차용 의존(코드·예문·산문) 100% 제거. 검증된 구조(10대 카테고리 A~J·S1/S2/S3 심각도·CLI·등급 로직)는 보존하되 메트릭 알고리즘(metrics.py·metrics_v2.py)·테스트·taxonomy 예문·scholarship 산문·파생 룰북·SKILL.md 출처표시를 전면 자체 저작. 한국 번역학계 8유형 번역투 계보 + 학술 원전(KatFish·Toral 2019 arXiv:1907.00900) 직접 인용 기반. 기능 동등성 잠금(동일 risk_band·메트릭 값 byte-identical, 28 테스트 PASS, RiskBandRegression 영구 가드). 스킬 전체가 NC-ND 하에 편입.
- 전체 버전 동기화 2.19.0 → 2.20.0 (marketplace.json + 28 plugin.json + 176 SKILL.md).
- 루트 README·`marketplace.json` 카탈로그에 moai-tutor 추가, 배지(28 플러그인 · 176 스킬) 및 총 산출물 표 갱신.

### Migration

- 신규 플러그인 추가만 있고 기존 플러그인·스킬·워크플로우는 변경되지 않습니다(기능적 비파괴). `/plugin marketplace update cowork-plugins`로 마켓플레이스를 갱신한 뒤 `moai-tutor`를 설치하면 됩니다.

## [2.19.0] - 2026-06-15

MINOR. **humanize-korean v2.0.0 포팅 + Cowork-safe 플러그인 코디네이터 31종 선별 재도입**. 두 갈래 통합 릴리스입니다. ① `moai-content:humanize-korean`을 upstream [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) v1.6.1 → v2.0.0으로 정렬(한국 번역학계 8유형 번역투 계보 + 신규 패턴 4 + post-editese 14메트릭). ② v2.18.0에서 제거했던 번들 에이전트를, 에이전트 도구 동작 실측 리포트(플러그인 서브에이전트는 Cowork에서 Read/Grep/Glob/Write/Edit/WebSearch 동작·Bash/WebFetch 미동작)를 근거로 **Cowork-safe 형태로 선별 재도입**(24 플러그인 31개). `/project` Agent Synthesis와 공존(플러그인 번들 = 마켓플레이스 기본 제공, /project = 사용자 프로젝트 맞춤). 27 플러그인 / 173 스킬 유지, 동기화 2.18.0 → 2.19.0. 기능적 비파괴.

### Added

- **Cowork-safe 플러그인 코디네이터 sub-agent 31개** (`moai-*/agents/*.md`, 24 플러그인) — 멀티스텝 체인·배치·QA가 필요한 고가치 스킬 클러스터에만 선별 부착. 모든 에이전트는 `tools: Read, Grep, Glob, Write, Edit, WebSearch`(Bash·WebFetch 배제 — Cowork 서브에이전트 미지원)이며, 텍스트 산출 체인은 `moai-core:ai-slop-reviewer → moai-content:humanize-korean`으로 마감(§3-2). 분포: commerce 4 · marketing 3 · business·content 2 · 그 외 18 플러그인 1개씩. (단일 스킬 plugin bi·lifestyle·pm은 의도적 제외.)
- **humanize-korean 신규 패턴 4종** — `A-16` 영어 대명사 직역 [S1] · `A-18` 관계절 좌향 수식 [S2] · `A-19` 이중 조사 결합 [S2] · `E-7` 청자 경어법 일관성 손실 [S2 estimated]. `A-17`(무정물 '-들' 부착)은 hold(외부 회차 양성 0건 → v2.1 재평가).
- **post-editese 메트릭 레이어** — `references/metrics_v2.py`(번역투 14개 정량 신호, simplification·normalisation·interference 3축, metrics.py import 상위집합, stdlib only) + `references/baseline_v2.json`(5장르 placeholder 임계값) + `references/scholarship.md`(한국 번역학계 8유형 + 국제 이론 Baker·Toury·Toral + caveat 6건).
- humanize-korean tests에 v2.0 스모크 테스트 9종 추가(총 22 테스트 PASS).

### Changed

- **humanize-korean 분류 체계 v1.6 → v2.0** — `ai-tell-taxonomy.md` 머리말에 8유형 번역투 계보 통합, 보강 4패턴(`A-15` 사역·인지 동사 3축 처방 · `A-7` light verb construction · `F-4` 영어 명사화 접미사 4종 · `E-2` 진행형 '~고 있다' 처방). `quick-rules.md`·`rewriting-playbook.md`(PE 통합 체크리스트 15항목)·`SKILL.md`(attribution v2.0.0 ⭐2.9k, Phase 2 옵션 post-editese 레이어, 런타임 배너 정리) 동기화.
- 전체 버전 동기화 2.18.0 → 2.19.0 (marketplace.json + 27 plugin.json + 173 SKILL.md).

### Fixed

- humanize-korean `tests/test_metrics.py` 경로 복구 — v1.6.1 verbatim 포팅 시 upstream 레이아웃(`.claude/skills/...`)이 cowork 레이아웃(`moai-content/skills/...`)으로 적응되지 않아 `import metrics` 실패하던 사전 결함을 수정(이제 22 테스트 전부 실행·통과).
- 재검수 보강 — 코디네이터 3종의 deprecated/rename stub 참조 정정(education-course-builder·content-publishing-pipeline·commerce-growth-analyst), humanize-korean metrics_v2 관계절·by-passive 탐지 정확도 수정(F1·F2, 회귀 테스트 2종 추가 24 PASS), 문서 일관성(strict-pipeline-spec·scholarship·SKILL 배너).

### Migration

- v2.18.0의 `/project` Agent Synthesis는 그대로 유지됩니다. 이번 플러그인 번들 에이전트는 마켓플레이스 기본 제공 코디네이터로, 사용자 프로젝트 맞춤 에이전트와 공존합니다.
- 플러그인 에이전트는 Cowork에서 자동 노출됩니다(설치 버전 갱신 후). 셸 실행·웹페이지 fetch가 필요한 작업은 부모 세션이 담당합니다.
- 적용: `/plugin marketplace update cowork-plugins`.

## [2.18.0] - 2026-06-15

MINOR. **Cowork 에이전트 모델 전환 — 플러그인 번들 코디네이터 제거 + `/project` 맞춤 에이전트 생성 + project 스킬 현대화**. v2.17.0의 플러그인 번들 코디네이터 sub-agent를 전면 제거하고, `/project`가 사용자 워크플로우에 맞춘 전담 에이전트를 직접 생성하는 Agent Synthesis 모델로 일원화했습니다. **27 플러그인 / 173 스킬 유지**, 동기화 201지점 2.17.0 → 2.18.0. 기능적 비파괴 — 기존 스킬 체인은 자연어 인라인 호출로 동일 결과.

### Added

- **`/project` Agent Synthesis (Phase 3.5)** — 초기화 인터뷰에서 자격 워크플로우(고정 다단계 + 비우회 게이트 / 병렬 fan-out / 빈번 반복)에 한해 사용자 프로젝트 `.claude/agents/<name>.md`에 맞춤 sub-agent를 생성합니다. 신규 `agent.md.tmpl` 템플릿(`description:` 블록 스칼라). 프로젝트 에이전트는 플러그인 번들보다 우선순위가 높고 Cowork이 자동 로드하며, 디스크 직접 작성이므로 **새 세션에서 활성화**됩니다.

### Changed

- **moai-core:project 스킬 현대화** — 카운트 정합 22 → 27 플러그인 / 143 → 173 스킬. Phase 2 인벤토리 화이트리스트를 하드코딩에서 **동적 도출**로 전환(신규 5개 플러그인 moai-comms·moai-design·moai-productivity·moai-public-data·moai-wealth 스킬이 런타임에 필터링되던 버그 해소). router 27개 라우팅 재작성. 폐기된 harness 모듈·글로벌 프로필(`{user_name}`) 잔재 제거.
- **커맨드 표면 단순화** — bare `/project`가 초기화 기본 동작으로 승격. `/project init`·`/project init resume`은 레거시 별칭으로 계속 인식(비파괴), `/project resume` 신설.
- 전체 버전 동기화 2.17.0 → 2.18.0 (marketplace.json + 27 plugin.json + 173 SKILL.md + hugo.toml). 201지점.
- marketplace.json 플러그인 description에서 제거된 에이전트 언급(slop-reviewer·doc-qa·research-scout) 정리.

### Removed

- **플러그인 번들 코디네이터 sub-agent 14개 전면 제거** — `moai-*/agents/*.md` 14개 + `agents/` 폴더 제거(v2.17.0의 코디네이터 11종 + 미문서화 3종). 우선순위 최하위·설치 버전 게이트·orchestrator 중복이라는 구조적 약점으로 `/project` Agent Synthesis로 대체. 파이프라인 로직(finance 병렬 조립·commerce 7단계+컴플라이언스 게이트)은 Phase 3.5 자격 예시로 보존.

### Fixed

- book·commerce 코디네이터 frontmatter YAML 파싱 오류 — 인라인 `description:`의 콜론+공백이 YAML 매핑으로 파싱되던 문제(제거 전 복구, 패턴은 `agent.md.tmpl` 블록 스칼라로 재발 방지).
- moai-office 5개 SKILL.md(docx·pptx·xlsx·hwpx·pdf)의 삭제된 `doc-qa` 에이전트 자동 실행 안내 → 인라인 자체검수 안내로 정정.

### Migration

- 기존에 플러그인 코디네이터를 자연어로 호출하던 워크플로우는 **동일 스킬 체인을 자연어로 요청하면 같은 결과**를 얻습니다(orchestrator 인라인 라우팅).
- 전담 에이전트가 반복적으로 필요하면 `/project`로 프로젝트 맞춤 에이전트를 생성하세요(생성 후 **새 세션**에서 활성화).
- 적용: `/plugin marketplace update cowork-plugins`.

## [2.17.0] - 2026-06-14

MINOR. **Cowork-fit 재설계 — moai-public-data 신규 + Cowork 코디네이터 11종 + 매니페스트 정직화**. taxonomy·체이닝·매니페스트·이미지 정책을 4축으로 재설계하되 별칭·스텁으로 호환을 유지했습니다. **26 → 27 플러그인, 170 → 173 스킬**, 동기화 지점 198 → 201. Breaking change 없음 — 기존 워크플로우 그대로 동작(별칭·스텁 호환).

### Added

- **`moai-public-data` 신규 플러그인 (4 스킬)** — 한국 공공데이터 조회 단일 도메인. `korean-stock-search`(KRX 상장종목·시세), `court-auction-search`(대법원 법원경매 매각공고), `real-estate-search`(국토부 실거래가/전월세), `public-data`(공공데이터포털/KOSIS 통계). 흩어져 있던 공공데이터 조회 스킬을 한곳으로 모았으며, 기존 위치(moai-finance·moai-business·moai-data)는 별칭·스텁으로 호환 유지.
- **Cowork 코디네이터 서브에이전트 11종** — 멀티 스킬 파이프라인을 한 번에 실행하는 Cowork 전용 서브에이전트: `commerce-launch`(커머스 런칭), `detail-page-orchestrator`(상세페이지), `book-manuscript`(도서 원고), `business-plan`(사업계획서), `hiring`(채용), `legal-review`(법무 검토), `meta-ads`(메타 광고), `media-pipeline`(미디어 파이프라인), `ticket-triage-batch`(티켓 일괄 분류), `ux-audit`(UX 감사), `finance-report-assembler`(재무 보고 조립). Cowork에서는 코디네이터 한 번으로, Chat에서는 개별 스킬을 인라인 호출해 동일 결과.
- **WordPress 발행 커넥터 wiring** — `blog`·`newsletter` 스킬에 WordPress.com 발행 커넥터 연결.

### Changed

- **체이닝·트리거 표준화** — 60종+ 스킬에 `ai-slop → humanize` 체이닝을 표준 적용하고, description+trigger를 자연어 트리거 STANDARD로 일괄 정리.
- **taxonomy 정리** — moai-commerce 35 → 30 스킬로 머지(중복 제거), 보수적 rename(별칭 유지로 기존 호출 호환), `grant` 소유 경계 명확화, `ai-diagnostic` moai-core → moai-business 이동, `travel-planner` 분해, media-production split(`content-calendar` + `youtube-podcast-planner`).
- **매니페스트 정직화** — 실제 보유 스킬만 노출하도록 정정: moai-pm(`weekly-report`만), moai-sales(`proposal-writer`만), moai-bi(`executive-summary`만).
- 전체 버전 동기화 2.16.0 → 2.17.0 (marketplace.json + 27 plugin.json + 173 SKILL.md + hugo.toml). 동기화 지점 198 → 201.
- 루트 README 카탈로그(+moai-public-data 행, pm·sales·bi 범위 정정)·배지(Plugins 27 / Skills 173)·v2.17.0 하이라이트 추가, marketplace.json `plugins[]` +1 등록.
- docs-site: moai-public-data 플러그인 페이지 + 릴리스 v2.17 페이지 + 메뉴·홈 카운트 동기화.

### Removed

- `mcp-connector-setup`의 **Connector D(OpenAI/GPT Image 2) 제거** — 이미지 생성은 Higgsfield 단일 정책으로 통일.

### Migration

- `/plugin marketplace update cowork-plugins`로 신규 moai-public-data 플러그인·코디네이터 자동 노출. **Breaking change 없음 — 기존 워크플로우 그대로 동작**(rename은 별칭, relocation은 스텁으로 호환). 공공데이터 스킬을 기존 경로로 호출하던 경우에도 그대로 동작하며, 신규 통합 위치는 `moai-public-data`입니다.

---

## [2.16.0] - 2026-06-13

MINOR. **개인·일잘러 도메인 3종 신규 — moai-wealth · moai-productivity · moai-comms**. 사용자 실무 지식 데이터(vault) 2,219개 노트 전수 분석으로 커버리지 공백 3종을 식별·충전. **23 → 26 플러그인, 152 → 170 스킬**, 동기화 지점 176 → 198. Breaking change 없음.

### Added

- **`moai-wealth` 신규 플러그인 (6 스킬)** — 개인 재무·재테크. `wealth-roadmap`(재테크 로드맵 — 현황 진단·종잣돈 4단계·자산 배분), `household-budget`(가계부·소비관리 — 통장 쪼개기·50/30/20·소비 회고), `invest-primer`(투자 입문 — 분산·장기·리스크·자산군·초보 포트폴리오·투자 사기 회피), `insurance-fit`(보험 설계 — 필요 보험 진단·과보험 점검·생애주기 리모델링), `personal-tax-saver`(근로자 연말정산 절세 — 소득공제 vs 세액공제·연금저축/IRP·환급 극대화), `econ-literacy`(경제지표 읽기 — 금리·환율·물가·GDP를 내 돈 관점으로). 법인 세무(moai-finance)와 분리된 개인 자산관리 도메인.
- **`moai-productivity` 신규 플러그인 (7 스킬)** — 자기관리·생산성. `retro-builder`(회고 — KPT·연간·키워드), `goal-planner`(목표관리 — 12주·만다라트·개인 OKR), `time-system`(시간관리 — 블록식스·덩어리 시간·우선순위), `habit-routine`(습관·루틴 설계), `self-care`(번아웃·자기돌봄), `notion-template-kit`(노션 올인원 템플릿), `weekly-report`(직장 주간업무보고). 개인 자기관리 특화(팀 PM은 moai-product).
- **`moai-comms` 신규 플러그인 (5 스킬)** — 직장 커뮤니케이션·소프트스킬. `report-speak`(보고·설명의 기술 — 두괄식·핵심 요약), `meeting-facilitator`(회의 진행·퍼실리테이션), `feedback-loop`(피드백 주고받기), `conflict-handler`(갈등·소통빌런 대응·정중한 거절), `negotiation-1on1`(1:1 면담·설득·협상). moai-hr(공식 성과평가)·moai-content(문서 작성)와 구분되는 대인 커뮤니케이션 실전.

### Changed

- 전체 버전 동기화 2.15.0 → 2.16.0 (marketplace.json + 26 plugin.json + 170 SKILL.md + hugo.toml). 동기화 지점 176 → 198.
- 루트 README 카탈로그(+3행)·배지(Plugins 26 / Skills 170)·v2.16.0 하이라이트 추가, marketplace.json `plugins[]` +3 등록.
- docs-site: moai-wealth·moai-productivity·moai-comms 플러그인 페이지 + 릴리스 v2.16 페이지 + 메뉴·홈 카운트 동기화.

### Migration

- `/plugin marketplace update cowork-plugins`로 신규 3 플러그인 자동 노출. 기존 워크플로우·플러그인 그대로 동작. 신규 도메인(개인 재무·자기관리·직장 커뮤니케이션)은 기존 23개 플러그인과 중복 없음.

---

## [2.15.0] - 2026-05-30

MINOR. **Meta 공식 광고 커넥터 라이브 운영 + NotebookLM 슬라이드 프롬프트 신규 2 스킬**. 23 플러그인 유지, **150 → 152 스킬**. Breaking change 없음.

### Added

- **`meta-ads-manager`** 스킬 신규 (moai-marketing) — Meta 공식 **Ads AI Connectors**(OAuth 커넥터, `mcp.facebook.com/ads`, 2026-04-29 오픈 베타)에 연결해 캠페인·광고세트·광고를 자연어로 생성·수정·예산조정·온오프. 신규 리소스 **PAUSED 기본** + 쓰기·결제 동작 사용자 승인. 권한 등급 read-only/read+write/financial. 보고서 분석(`meta-ads-analyzer`)과 페어 분리.
- **`notebooklm-slide-prompt`** 스킬 신규 (moai-office) — Google NotebookLM Video Overview·슬라이드 생성을 위한 한국어 소스 정리·대본·구조 설계 + 슬라이드별 나노바나나(Gemini 3 Pro Image) 5-Component 이미지 프롬프트. NotebookLM 공식 4축 매핑 + 49 시각 스타일 라이브러리. PPTX 파일 생성(`pptx-designer`)과 페어 분리.

### Changed

- `moai-marketing` MCP `meta-ads` 인증을 정적 `META_ACCESS_TOKEN` Bearer → **Meta Business OAuth 2.0 커넥터 흐름**으로 정정 (라이브 검증: RFC 9728 protected-resource discovery + RFC 6750 Bearer, scope `ads_management ads_read catalog_management business_management pages_show_list`). 정적 토큰은 개발 환경 fallback으로 강등.
- 전체 버전 동기화 2.14.1 → 2.15.0 (marketplace.json + 23 plugin.json + 152 SKILL.md).
- docs-site: meta-ads-manager 사용법(광고 트랙 시나리오 ⑤ + 커넥터 등록 가이드) + notebooklm-slide-prompt 사용법 추가, hugo.toml SSOT·릴리스 페이지 v2.15.0.

### Removed

- `moai-marketing/CONNECTORS.md`에서 서드파티 오픈소스 Meta Ads MCP fallback 3종(Adspirer · byadsco/meta-ads-mcp · pipeboard) 제거 — Meta 공식 커넥터로 단일화. 자체 `moai-ads-audit` MCP(한국 50-check audit)는 유지.

### Migration

- `/plugin marketplace update cowork-plugins`로 신규 2 스킬 자동 노출. Meta 광고 운영은 Claude 커넥터에 `https://mcp.facebook.com/ads` 등록 후 OAuth 로그인(앱 생성 불필요). 기존 워크플로우 그대로 동작.

---

## [2.14.1] - 2026-05-26

PATCH (v2.15.0에 집약). **`moai-office`에 NotebookLM 슬라이드 데크 프롬프트 빌더 신규**. 강연·강의·세미나 본문 마크다운을 입력받아 (A) NotebookLM Studio에 그대로 붙여 넣을 슬라이드 데크 생성 프롬프트와 (B) 슬라이드별 나노바나나(Gemini 3 Pro Image) 5-Component 이미지 프롬프트를 동시 산출하는 prompt-builder. NotebookLM 공식 4축(Format `Detailed Deck` / `Presenter Slides`, Length `short`/`default`/`long`, Output language, Prompt 6블록) 정확 매핑 + DeepMind 공식 5-Component(Style·Subject·Setting·Action·Composition) + 시리즈 일관성 태그 자동 생성. 23 플러그인 유지, **150 → 151 스킬**, 동기화 지점 175 → **176**. Breaking change 없음.

### Added

#### moai-office (5 → 6 스킬)

- [`notebooklm-slide-prompt`](./moai-office/skills/notebooklm-slide-prompt/) — NotebookLM Studio 슬라이드 데크 + 나노바나나 이미지 프롬프트 빌더
  - **입력**: 강연·강의·세미나 본문 마크다운 (도입→핵심→데모→정리 4블록 권장)
  - **산출 Part A**: NotebookLM Studio 4축 입력값 + Prompt 6블록(청중·1순위 메시지·구조·톤·강조 슬라이드·금지)
  - **산출 Part B**: 슬라이드별 5-Component 이미지 프롬프트 (보통 5~8 슬라이드: 표지·섹션 구분·Must-Have·정리)
  - **시리즈 일관성**: 모든 슬라이드 이미지에 동일 `series`·`palette`·`lighting` 태그 자동 부여
  - **세이프티**: 실존 인물·저작권 캐릭터·브랜드 로고 직접 묘사 금지 자동 가드
  - **체이닝**: `notebooklm-slide-prompt → moai-core:ai-slop-reviewer` 권장 (텍스트 산출물)
  - **49 시각 스타일 라이브러리 내장** ([`references/slide-style-library.md`](./moai-office/skills/notebooklm-slide-prompt/references/slide-style-library.md)) — 8 카테고리 × 49 스타일:
    - A. 모던 웹·기술 UI (8): 벤토 그리드·뉴 모피즘·글래스 모피즘 3D·SaaS 대시보드·아이소메트릭 플랫·모던 다크 모드 등
    - B. 비즈니스·코퍼레이트 (10): 비즈니스 미니멀·뉴스레터 에디토리얼·프리미엄 컨설팅·데이터 스토리텔링·스위스 그리드 등
    - C. 교육·학습·매뉴얼 (7): 칠판 스타일·일본 만화 튜토리얼·스케치노트·화이트보드 전략·포스트잇 문제 해결맵 등
    - D. 레트로·복고·팝아트 (7): DOS 터미널·복셀 아트·레트로 팝 아트·빈티지 액션 코믹스·도트 픽셀 아트 등
    - E. 시네마틱·SF·다이내믹 (4): 네온 사이버펑크·역동 애니메이션·시네마틱 우주 SF·볼드 타이포그래피
    - F. 일러스트·예술·핸드메이드 (8): 바우하우스·식물학 일러스트·로코코·페이퍼 컷아웃·디지털 마인드맵 등
    - G. 라이프스타일·캐주얼 (4): 클레이 애니메이션·카와이 파스텔·Before/After·듀오톤 그래픽
    - H. 한국형 편집 디자인 (1): 포털형 카드 매거진
    - 발표 키워드 → 스타일 자동 매칭 규칙(10 키워드), 시리즈 일관성 가드, 안티패턴 5종 내장
  - **공식 출처**: [NotebookLM Slide Deck](https://support.google.com/notebooklm/answer/16757456) · [DeepMind Gemini Image Prompt Guide](https://deepmind.google/models/gemini-image/prompt-guide/) · [Nano Banana Pro 발표](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
  - **참고**: 49 스타일 분류는 공개된 옵시디언 publish 자료(이커머스 클래스 · 노트북 LM 슬라이드 가이드북)를 참고해 카테고리·매칭 규칙·일관성 가드를 재구성

### Changed

- 루트 `README.md` — 버전 배지(v2.14.0 → v2.14.1), 스킬 카운트(150 → 151), v2.14.1 하이라이트 섹션 신규 + v2.14.0 details 이동, moai-office 카탈로그 행(5 → 6 스킬)
- `moai-office/README.md` — 소개 문구에 NotebookLM 슬라이드 데크 프롬프트 빌더 추가, 스킬 테이블에 notebooklm-slide-prompt 행 신설
- 버전 통일: marketplace.json + 23 plugin.json + **151 SKILL.md** = **176 동기화 지점**

### Migration

- 사용자 조치 없음. `/plugin marketplace update cowork-plugins`로 신규 스킬 자동 노출.
- 호출 예: `"S0 도입 본문을 NotebookLM 슬라이드 프롬프트로 만들어줘"` 또는 `"본문을 15장 Presenter Slides로, 시각은 미니멀 등각 다이어그램으로"`.
- 실제 이미지 생성은 별도 단계 (Gemini 앱·Google AI Studio·Vertex AI·moai-media:higgsfield-image 중 택1).

## [2.14.0] - 2026-05-25

MINOR. **Anthropic 공식 발표(2026-04-17) 정합성 보완** — Claude Design 관련 docs 5페이지와 moai-design 스킬 2종에 (A) 음성·비디오·셰이더·3D 코드 기반 프로토타입 카테고리, (B) Canva 네이티브 파트너십 워크플로우, (C) 통합 빌더 단기 로드맵, (D) Brilliant·Datadog 공식 도입 사례를 정확히 반영. 부수적으로 루트 README 카탈로그에서 누락되어 있던 moai-book·moai-design 두 행 정정. 23 플러그인·150 스킬 유지, 동기화 지점 175. Breaking change 없음.

### Added

#### docs-site (claude-design 섹션)

- `getting-started/_index.md` — Hello World 6번째 예시 "코드 기반 인터랙티브 프로토타입 (셰이더·3D·웹 오디오)" 추가. 인터랙티브 HTML+JS 출력 vs 독립 .mp4 미지원 경계 명시
- `use-cases/_index.md` — 디자이너 섹션에 "프론티어 미디어 프로토타입" 시나리오 추가
- `best-practices/_index.md` — "공식 도입 사례 — 왜 이 원칙들이 작동하는가" 섹션 신규 (Brilliant Olivia Xu·Datadog Aneesh Kethini 인용)
- `limitations/_index.md` — "향후 로드맵 — Anthropic 공식 단기 (2026-04-17 발표 명시)" 섹션 신규. 통합 빌더 "coming weeks" 원문 인용. 기존 "추정" 섹션과 명확히 분리
- `_index.md` (Claude Design root) — "한눈에 보기" 출력 형식에 **Canva(네이티브 파트너십)** 강조

#### moai-design 스킬

- `claude-design-prompt-builder/SKILL.md` — 10대 패턴 표 다음에 **"보조 패턴 — 프론티어 미디어 프로토타입"** 섹션 신규. WebGL 셰이더·Three.js 3D·Web Audio API·캔버스 애니메이션 4영역 권장 ROLE(Pixar·Disney Research·Ableton·Stripe)·CONSTRAINTS. 11번째 정식 패턴은 아니며 명시적 미디어 키워드에만 활성화
- `claude-design-handoff-reader/SKILL.md` — 4단계에 **"두 경로 분기"** 표 신규. Claude Code 빌드 경로(스킬 1차 목적) vs Canva 마케팅 후속 경로(Anthropic ↔ Canva 공식 파트너십) 명확 분리. 두 경로 동시 진행 시 일관성 깨짐 경고

#### docs-site (릴리스)

- `content/releases/v2.14.md` (신규) — v2.14.0 릴리스 노트
- `data/menu/main.yaml` — 릴리스 메뉴 v2.14.0 추가

### Changed

- `limitations/_index.md` — #4 "3D · 음성 · 비디오 초기 단계" → "코드 기반 프로토타입 — 공식 지원 vs 실제 한계"로 재작성. Anthropic 공식 명시 vs 사용자 보고 한계를 표로 구분 (WebGL 셰이더·Three.js 3D·Web Audio API 공식 지원 / 독립 .mp4 미지원)
- `export-handoff/_index.md` — Canva 섹션을 "Canva — 네이티브 통합 (공식 파트너십)"로 확장. Canva CEO Melanie Perkins 인용 + 마케팅 후속 편집 워크플로우 mermaid 추가
- `best-practices/_index.md` Sources — Anthropic 공식 출시 공지 URL 최상단 추가 (Brilliant·Datadog·Canva 인용 원문)
- `marketplace.json metadata.description` — v2.14.0 헤드라인 추가
- `content/plugins/_index.md` — v2.14 업데이트 노트 + 헤더 카운트 표기 갱신
- 루트 `README.md` — v2.14.0 하이라이트 섹션 신규, 카탈로그 표 누락 행 2개 정정 (moai-book·moai-design 추가, 21→23행), 총 산출물·기술 특징의 outdated 카운트(22·143·v2.11.0) 정정
- 전체 marketplace.json + plugin.json + SKILL.md + hugo.toml 일괄 2.13.0 → 2.14.0 (175 지점)

### Migration

Breaking change 없음. 기존 워크플로우 그대로 동작. moai-design을 활용 중인 사용자는 업데이트 후 `claude-design-prompt-builder`·`claude-design-handoff-reader` 본문에서 새 섹션을 확인하세요.

```bash
/plugin marketplace update cowork-plugins
```

### 동기화 지점 카운트

| 범주 | 지점 수 | 변화 |
|---|---|---|
| marketplace.json | 1 | 유지 |
| plugin.json | 23 | 유지 |
| SKILL.md frontmatter | 150 | 유지 |
| hugo.toml SSOT | 1 | 유지 |
| **합계** | **175** | 유지 |

### Sources

- [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs) — 2026-04-17 공식 출시 공지
  · 원문 인용: *"code-based prototypes including those with audio, video, shaders, and 3D"*
  · 원문 인용: *"Over the coming weeks, we'll make it easier to build integrations with Claude Design"*
  · Brilliant Olivia Xu · Datadog Aneesh Kethini · Canva CEO Melanie Perkins 공식 인용
- [Using Claude Design for prototypes and UX (Anthropic Tutorial)](https://claude.com/resources/tutorials/using-claude-design-for-prototypes-and-ux)

## [2.13.0] - 2026-05-20

MINOR. **moai-media에 Higgsfield MCP 직접 호출 신규 2 스킬 — higgsfield-image · higgsfield-video** (higgsfield.ai 공식 페이지 명시 모델 기준). 23 플러그인 유지, 148 → 150 스킬, 동기화 지점 173 → 175. Breaking change 없음.

### Added (moai-media:higgsfield-image)

- SKILL.md — higgsfield.ai 공식 11 이미지 모델 자동 선택·호출
  · Soul 계열: Soul · Soul 2.0 · Soul Cinema
  · Nano Banana 계열: Nano Banana · Nano Banana Pro
  · GPT Image 계열: GPT Image · GPT Image 2
  · 기타: Seedream 4.0 · Flux Kontext · Wan 2.2 Image · Wan 2.5
- 모델 선택 키워드 매칭 (**글자·카드뉴스→GPT Image 2 1순위·Nano Banana Pro 보조**, 시네마틱→Soul Cinema·Soul 2.0, 사진→Flux Kontext, 아트→Seedream 4.0 등)
- 파라미터 자동 설계 (width_and_height·quality·batch_size·style·seed·custom_reference_id)
- 비율 자동 매핑 (인스타·스토리·블로그·인쇄)
- 캐릭터 일관성 — Soul Characters reference 패턴
- 비동기 잡 폴링 (queued → in_progress → completed/failed/nsfw)
- references/model-guide.md — 11 모델별 강점·약점·예시 프롬프트·비교 매트릭스

### Added (moai-media:higgsfield-video)

- SKILL.md — higgsfield.ai 공식 11 영상 모델 + 6 비디오 프리셋 자동 선택·호출
  · 일반 영상: Sora 2 · Google Veo 3 · Kling 2.1 Master · Kling 2.5 Turbo · Kling 3.0 · Seedance 2.0 · Seedance Pro · MiniMax Hailuo 02 · Wan 2.5
  · 시네마틱: Cinema Studio 3.5
  · 캐릭터 일관성: Kling Avatars 2.0
  · 비디오 프리셋: UGC · Unboxing · Product review · Hyper motion · TV spot · Wild Card
- 입력 유형별 분기 (text-to-video / image-to-video / 캐릭터 시리즈)
- 모델·프리셋 자동 매칭 (시네마틱→Cinema Studio 3.5+TV spot, 빠른 시안→Kling 2.5 Turbo+UGC, 액션→Seedance Pro+Hyper motion 등)
- 길이·비율 자동 (16:9·9:16·1:1·4:5)
- 비동기 잡 폴링 (10-90초, 모델별)
- references/dop-motions.md — 6 프리셋 사용 가이드·모델별 톤 변경·호출 예시

### Added (docs-site)

- content/releases/v2.13.md (신규) — v2.13.0 릴리스 노트
- data/menu/main.yaml — 릴리스 메뉴 v2.13.0 추가
- content/releases/_index.md — mermaid 흐름도 v2.13 추가, 카드 설명·호환성 메모

### Changed

- marketplace.json metadata.description — v2.13.0 highlights 추가
- marketplace.json metadata.version — 2.12.3 → 2.13.0
- marketplace.json plugins[].moai-media description — Higgsfield 직접 호출 명시
- moai-media/.claude-plugin/plugin.json description·keywords — Higgsfield 키워드 확장
- 전체 plugin.json + SKILL.md + hugo.toml SSOT = 175 지점 2.12.3 → 2.13.0
- docs-site content/_index.md, plugins/_index.md — 148 → 150 스킬 카운트 갱신

### Migration

기존 워크플로우 그대로 동작. moai-media를 이미 활성화한 사용자는 업데이트 후 추가 작업 불필요. Higgsfield 첫 사용 시 Cowork → 설정 → MCP → Higgsfield → Connect로 OAuth 1회 인증.

```bash
/plugin marketplace update cowork-plugins
```

### Sources

- [Higgsfield 공식 사이트](https://higgsfield.ai) — 공식 11 이미지 + 11 영상 모델 + 30+ 광고
- [Higgsfield MCP](https://higgsfield.ai/mcp) — hosted MCP 안내
- [Higgsfield Skills](https://higgsfield.ai/skills) — 6 비디오 프리셋 (UGC·Unboxing·Product review·Hyper motion·TV spot·Wild Card)

## [2.12.3] - 2026-05-20

PATCH. **moai-content:card-news 콘텐츠 정련**. 23 플러그인·148 스킬 유지, 동기화 지점 173. Breaking change 없음.

### Changed (moai-content:card-news)

- 10 구성 패턴 작명 정리 — A·B 듀얼 선택·순차 빌드·체크박스 점검·궁금증 해소·함정 회피·첫 발 가이드·개념 사전·페인 → 솔루션·실전 사례·즉시 활용 키트
- 5 디자인 톤 명명 정리 — Soft Cream·Claude Modern·Corporate Trust·Playful Pop·Bold Dark
- 8단계 워크플로우 정립 (주제 파악 → 패턴 선택 → 본문 골격 → 톤 → 통합 프롬프트 → 이미지 위임 → 카피 검수 → 채널 산출)

### Added

- 채널별 캡션 가이드 (인스타·스레드·카카오 채널·페이스북)
- 분량별 확장 가이드 (4장·7장·10장 시리즈)
- 시리즈 운영 규칙 (톤앤매너 통일·페이지 번호·마스코트)

### 버전 동기화

- marketplace.json + 23 plugin.json + 148 SKILL.md + hugo.toml = 173 지점 2.12.2 → 2.12.3

## [2.12.2] - 2026-05-20

PATCH. **moai-content:card-news 보강** — 10 구성 패턴·통합 프롬프트·디자인 톤 추가. 23 플러그인·148 스킬 유지, 동기화 지점 173. Breaking change 없음.

### Added (moai-content:card-news)

- references/prompt-templates.md (신규) — 10 패턴 본문 골격 + 통합 프롬프트 + 꿀팁
- SKILL.md 본문 — 10 구성 패턴 자동 선택 + 5 디자인 톤 + 통합 프롬프트
- Claude 톤 변형 (Anthropic Orange #d97757 + Light Beige #faf9f5 + Pretendard)

### Changed

- marketplace.json + 23 plugin.json + 148 SKILL.md + hugo.toml = 173 지점 2.12.1 → 2.12.2
- docs-site: releases/v2.12.2.md 신규 · releases/_index.md · data/menu/main.yaml

## [2.12.1] - 2026-05-20

PATCH. **moai-office docx-generator·pptx-designer 모던 디자인 시스템 대형 보강**. Claude 브랜드 톤(Anthropic Orange #d97757, Light Beige #faf9f5, Dark #141413) 기반 색·타이포·간격·구조 패턴 내장. 23 플러그인·148 스킬 유지, 동기화 지점 173. Breaking change 없음.

### Added (moai-office:docx-generator)

- references/modern-design-system.md — Claude 톤 색 팔레트·타이포 페어링·간격 토큰
- references/modern-templates.md — 6대 모던 템플릿 (공문서·기업 보고서·계약서·제안서·기획서·사업계획서) + 각 팔레트 변형
- references/qa-checklist.md — 10단계 자동·시각 검수 (placeholder·헤딩 위계·표 보더·폰트·색 대비·AI 슬롭)
- SKILL.md 본문 — 모던 디자인 패턴 6종 (Executive Summary Box·Pull Quote·Stat Callout·Comparison Table·Sidebar Note·Section Divider) + python-docx 코드 패턴

### Added (moai-office:pptx-designer)

- references/curated-palettes.md — **10 큐레이션 팔레트** (Claude Classic·Coral·Mono·Blue Calm·Green Earth·Korean Brick·Navy·Sage·Dark Editorial·High Contrast Bold)
- references/slide-archetypes.md — **9 비즈니스 슬라이드 아키타입** (Title·Agenda·Problem·Solution·Features·Stats·Team·CTA·Closing) + 시퀀스 조합 예시
- references/typography-pairings.md — **5 폰트 페어링** (Modern·Editorial·Bold Heading·Classic·Tech) + 사이즈 위계·라이선스 메모
- references/qa-checklist.md — 자동 (5단계) + 시각 (5단계) 검수 + LibreOffice CLI 변환·Claude Code subagent 검수
- SKILL.md 본문 — HTML-First 옵션 + 다중 산출물 (PPTX·PDF·JPEG·발표자 노트·편집 가이드)

### Changed

- marketplace.json + 23 plugin.json + 148 SKILL.md + hugo.toml SSOT = 173 지점 모두 2.12.0 → 2.12.1 일괄 bump
- docs-site/content/releases/_index.md + data/menu/main.yaml — v2.12.1 추가, v2.12.0 보존

### Fixed

해당 없음 (PATCH 콘텐츠 보강만)

### Removed

해당 없음

## [2.12.0] - 2026-05-20

MINOR. **신규 플러그인 `moai-design` — Claude Design(claude.ai/design) 보조 풀스택 5 스킬 + docs-site 클로드 디자인 섹션 10페이지 동시 신설**. 22 → 23 플러그인, 143 → 148 스킬, 동기화 지점 167 → 173. Breaking change 없음.

### Added (신규 플러그인: moai-design — 5 스킬)

- `moai-design/.claude-plugin/plugin.json` — Cowork 마켓플레이스 등록
- `moai-design/README.md` — 플러그인 사용 가이드
- **`claude-design-brief`** — Claude Design 6요소 브리프(Project·Audience·Pages·Tone·Reference·Constraints) 자동 채움. 자연어 한 줄 입력 → AskUserQuestion으로 누락 요소 보완 → AI 슬롭 회피 블록 자동 포함된 복붙용 프롬프트 생성
- **`claude-design-system-prep`** — 브랜드 자산 5종(코드·디자인·브랜드·실물·사전 빌트인) → DESIGN.md 합성. 색 팔레트·타이포·컴포넌트·voice·레이아웃 자동 추출. Claude Design 업로드 가이드 동봉
- **`claude-design-prompt-builder`** — 시니어 UX 10 패턴(IA·리서치·디자인 시스템·카피·온보딩·휴리스틱·대시보드·접근성·폼·테스트) 중 자동 선택 + ROLE·GOAL·CONSTRAINTS·OUTPUTS 자동 채움. 사용자는 CONTEXT만 보완
- **`claude-design-handoff-reader`** — Claude Code 핸드오프 번들(README·design-tokens.json·components.json·layout-hierarchy.json·chat-history.md) 분석. 컴포넌트 트리·토큰·디자인 결정 맥락·구현 우선순위 + Claude Code 지시 1줄 자동 생성
- **`claude-design-slop-check`** — 영문(Reimagine your·Unleash your potential 등 Tier 1 11개·Tier 2 5개) + 한국어(혁신적인·차세대·재정의하는 등 Tier 1 9개·Tier 2 5개) 슬롭 패턴 검수. moai-content:humanize-korean 체이닝 권장

### Added (docs-site 클로드 디자인 섹션 10페이지)

코워크와 플러그인 사이 top-level 섹션 신설:

- `docs-site/content/claude-design/_index.md` — 학습 경로 허브 (123줄)
- `docs-site/content/claude-design/getting-started/_index.md` — 입력 4종·6요소 템플릿·Hello World 5종·30분 워크플로우 (197줄)
- `docs-site/content/claude-design/design-system/_index.md` ★ — 자산 5종·6단계 셋업·Figma·GitHub·CSS 토큰·멀티 시스템·Published 토글 (273줄)
- `docs-site/content/claude-design/refinement/_index.md` — 4가지 조작·컨텍스트 누적·AI 슬롭 회피·시니어 UX 10 패턴 (213줄)
- `docs-site/content/claude-design/collaboration/_index.md` — Org-scoped 공유·3권한·그룹 대화·데이터 거버넌스·DPA·GDPR (191줄)
- `docs-site/content/claude-design/export-handoff/_index.md` — 6 출력 형식·핸드오프 번들 내부 구조·양방향 우회 (237줄)
- `docs-site/content/claude-design/use-cases/_index.md` — 5 역할 워크플로우·Brilliant·Datadog·Canva 사례·한국 SaaS·D2C·어드민 시나리오 (254줄)
- `docs-site/content/claude-design/best-practices/_index.md` — 10대 원칙·통합 프롬프트 템플릿·보안·조직 운영 체크리스트 (253줄)
- `docs-site/content/claude-design/pricing-limits/_index.md` — 별도 쿼터·RBAC 4단계·도입 결정 체크리스트·한국 결제 메모 (210줄)
- `docs-site/content/claude-design/limitations/_index.md` — Research Preview 9 제한·향후 로드맵 추정·v0·Lovable·Bolt 비교·도입 부적합 7조건 (225줄)
- `docs-site/layouts/partials/menu.html` — `palette` 아이콘 SVG 추가

### Added (docs-site 인덱스 갱신)

- `docs-site/content/plugins/moai-design.md` — moai-design 플러그인 상세 페이지
- `docs-site/content/releases/v2.12.md` — v2.12.0 릴리스 노트

### Changed

- `marketplace.json` `metadata.description` — v2.12.0 highlights 추가, plugins[] 배열에 moai-design
- `marketplace.json` `metadata.version`: 2.11.1 → 2.12.0
- 모든 `plugin.json` `version`: 2.11.1 → 2.12.0 (22 → 23 파일)
- 모든 `SKILL.md` `version` frontmatter: 2.11.1 → 2.12.0 (143 → 148 파일)
- `docs-site/hugo.toml` `[params] version`: 2.11.1 → 2.12.0, `releaseDate`: 2026-05-20
- `docs-site/data/menu/main.yaml` — 플러그인 카탈로그에 "클로드 디자인 보조" 추가, 릴리스 메뉴에 v2.12.0 추가
- `docs-site/content/_index.md` — 22 → 23 플러그인, 143 → 148 스킬 카운트 갱신
- `docs-site/content/plugins/_index.md` — 카탈로그 메인 표·도메인별 섹션·v2.12 hint·NEW 표시 + Sources 링크 갱신
- `docs-site/content/releases/_index.md` — mermaid 흐름도 + 최신 릴리스 카드 + 호환성 메모

### Fixed

해당 없음 (MINOR 신규 추가만)

### Removed

해당 없음

### Migration

기존 워크플로우는 그대로 동작. moai-design 플러그인은 마켓플레이스에서 별도 활성화가 필요. 기존 디자인 인접 스킬(`moai-product:ux-designer`·`moai-product:ux-researcher`·`moai-marketing:brand-identity` 등)은 그대로 유지.

```bash
/plugin marketplace update cowork-plugins
# moai-design 활성화는 마켓플레이스에서 +
```

## [2.11.1] - 2026-05-18

PATCH. **v2.11.0 후속 정정 — fal-ai 완전 제거 + project 스킬 Phase 2/4/Re-entry 추가 + hugo.toml SSOT 도입 + 홈 v2.10 카드 라벨 정정**. 22 플러그인 유지, 143 스킬 유지, 동기화 지점 167(166 + hugo.toml). Breaking change 없음.

### Added (project 스킬 — `/project init` 흐름 강화)

- `/project init` Phase 2 Inventory 구체 메커니즘 — `~/.claude/plugins/` 에서 **cowork-plugins 22 화이트리스트만** 필터링한 후 각 플러그인의 모든 `SKILL.md` 완전 스캔. 다른 마켓플레이스 출처 플러그인은 인벤토리에서 완전 제외
- `/project init` Phase 4 Gap Detection — 체인 설계의 각 스킬이 inventory에 있는지 검증. 누락 발견 시 AskUserQuestion 4 옵션(설치 안내·제외·대체·중단) 제시 + `.moai/cache/init-progress.json` 진행 상태 저장
- `/project init resume` 커맨드 신규 — 사용자가 누락 플러그인 설치 완료 후 `/project init resume` 또는 자연어 "이어서 진행" 발화 시 진행 상태 복원 + Phase 4부터 재검증
- `docs-site/hugo.toml` SSOT — `[params] version` 단일 갱신으로 좌측 사이드바·footer·version-badge.html 모든 표시 위치 자동 반영

### Fixed (fal-ai 완전 제거 + 카드 라벨 정정)

- **fal-ai MCP 완전 제거** — 9 파일 32건 (CHANGELOG·README·docs-site/_index·releases/_index·v2.11·v2.7·v2.6·v1.2·moai-marketing). 이미지·영상 직접 생성은 **Higgsfield MCP 단일 통합**으로 환원. 음성은 ElevenLabs MCP. 번들 MCP는 higgsfield+elevenlabs 2종만
- 홈 페이지 "최근 릴리스" 두 번째 카드가 v2.11.0으로 잘못 라벨링되어 있던 것 → v2.10.0(moai-book 신규 8 스킬)로 정정. 첫 카드 v2.11.0 + 두 번째 v2.10.0 + 세 번째 v2.9.0 순서 정상
- 좌측 사이드바 상단 "MoAI-Cowork 문서 v2.10.0" 표기가 v2.11.0로 갱신되지 않던 문제 — hugo.toml SSOT 누락이 원인이었음. SSOT 한 줄 갱신으로 모든 표시 위치 자동 반영
- 릴리스 노트 v2.11.md Hugo shortcode escape — backtick 안 `{{< terminal >}}`이 Hugo에 의해 shortcode로 해석되어 빌드 실패하던 문제. `{{</* terminal */>}}` literal escape로 정정
- 메뉴 yaml에 v2.11.x 항목 누락 + isNew 마커가 v2.10에 남아있던 것 정정

### Changed (메모리 정책)

- `feedback_fal_ai_deprecated.md` — "fal-ai MCP 사용 금지, Higgsfield 단일 통합" 강한 정책 확정
- `feedback_version_bump_docs_checklist.md` — vX.Y.Z bump 시 `hugo.toml [params] version` SSOT를 게이트 0(1순위)로 명시. docs-site 5 지점 + 8 검증 게이트 명세
- 메모리 `feedback_terminal_prompt_first_line.md`, `feedback_tilde_strikethrough_ban.md`는 v2.11.0에서 이미 등록됨

### Removed (academy handoff 정리 — v2.11.0 누락분 보강)

- `academy-moai-cowork-handoff.md` 파일 삭제 — academy 외부 사이트(academy.mo.ai.kr)가 강의 안내를 담당하므로 저장소 내부 핸드오프 문서 불필요. v2.11.0에서 강의 컨텍스트 제거 작업의 마무리

### Migration

- 사용자 영향 없음 — 기존 워크플로우 그대로 동작
- 이미지·영상 직접 생성을 fal-ai로 호출하던 사용자: **Higgsfield MCP**로 환원 (`higgsfield.soul.*`·`higgsfield.dop.*`·`higgsfield.speak.*`·`higgsfield.character.*`)
- 음성은 ElevenLabs MCP 그대로
- `/project init`을 다시 실행하면 Phase 2 Inventory + Phase 4 Gap Detection이 자동 활성화되어 누락 플러그인 발견 시 설치 안내 제공

## [2.11.0] - 2026-05-18

MINOR. **moai-media 16→4 스킬 정리 + 22 플러그인 페이지 책임 경계 재정렬 + docs-site 일관성 정리**. 22 플러그인 유지, **155 → 143 스킬**, 동기화 지점 178 → **166**. Breaking change 없음.

### Removed (moai-media 12 스킬 정리)

이미지·영상·음성 직접 호출 스킬 12개를 제거. 해당 영역은 **Higgsfield MCP + ElevenLabs MCP**가 직접 지원하므로 wrapper 스킬을 정리해 책임 경계를 명확히 함.

- 제거된 스킬: `nano-banana`, `image-gen`, `video-gen`, `speech-video`, `character-mgmt`, `media-moodboard`, `media-gpt-image2-builder`, `media-model-router`, `media-channel-ad-packager`, `media-ai-disclosure`, `media-canva-magic-layer` (이미지·영상 직접 생성은 Higgsfield MCP 단일 통합으로 환원)
- 유지: `gpt-image-2-prompt`, `gemini-3-image-prompt`, `midjourney-v8-prompt` (프롬프트 텍스트 빌더 3종) + `audio-gen` (ElevenLabs MCP 래퍼 1종)
- moai-media 정체성 재정의: **이미지 프롬프트 텍스트 빌더 + ElevenLabs 음성**. 실제 이미지·영상 생성은 Higgsfield MCP / ChatGPT / Google AI Studio / Discord 직접 호출로 환원

### Changed (플러그인 페이지 책임 경계 재정렬)

- **moai-commerce 페이지** — 35 스킬 도메인 카탈로그(시장조사·JTBD·페르소나·상품명·통합전략 등 9 카테고리)로 재작성
- **moai-media 페이지** — 이미지 프롬프트 빌더 3종 + audio-gen 4 스킬로 재작성. Higgsfield MCP 단일 통합
- **moai-education 페이지** — 강사·교수·교사 교육 콘텐츠 풀스택으로 재정의. `course-curriculum-design`은 1일~16주 모든 코스 형식 지원, `course-followup-sequence`는 코스 종료 후 D+1·D+3·D+7·D+14·D+30 후기 자산화로 일반화
- **moai-bi 페이지** — `executive-summary`의 산출물을 `html-report` 중심으로 재정의. 단일 HTML 파일에 이미지·CSS·JS 모두 인라인 + pdf/docx/pptx/hwpx 변환은 옵션
- **moai-career 페이지** — 한국 취준생·재직자 2026 채용 데이터 반영(팀핏 면접·핀셋 채용·AI 진정성·4 플랫폼 MAU·헤드헌터 5축·NCS·블라인드)

### Fixed (docs-site 일관성 정리)

- 물결 `~` strikethrough 사고 정정 — 266+ 파일 1,000+ 위치
- mermaid 가로(LR) → 세로(TD) 변환 — 67 파일 77 블록 모바일 가독성 개선
- 터미널 prompt shortcode 통일 (`{{< terminal >}}`) — 첫 행만 `>`, 이어지는 줄 들여쓰기
- hugo.toml SSOT 도입 — 좌측 사이드바·footer·badge 자동 반영
- 삭제 페이지 정리 — `cookbook/ai-employee-design` 등 + 메뉴·링크 정리

### Migration

- **Breaking change 없음** — 기존 워크플로우 그대로 동작
- moai-media 12 스킬 제거 — 해당 영역은 **Higgsfield MCP·ElevenLabs MCP**를 직접 사용. 외부 MCP는 v2.6.0부터 번들되어 있어 사용자 측 추가 작업 없음
- 이미지 프롬프트 빌더 3종(`gpt-image-2-prompt`·`gemini-3-image-prompt`·`midjourney-v8-prompt`)·음성 `audio-gen`: 변경 없음

### 동기화 지점 (166)

| 범주 | 경로 | 개수 |
|---|---|---|
| 마켓플레이스 | `.claude-plugin/marketplace.json` | 1 |
| 플러그인 매니페스트 | `<plugin>/.claude-plugin/plugin.json` | 22 |
| 스킬 frontmatter | `<plugin>/skills/<skill>/SKILL.md` | 143 (moai-media 16→4 = -12) |

## [2.10.0] - 2026-05-17

MINOR. **신규 플러그인 moai-book 도입 — 한국 출판사 제출용 원고 집필 풀스택 8 스킬** — 도서 컨셉서부터 출판사 매칭·본문 집필·퇴고까지 8 단계 워크플로우를 단일 플러그인에 통합. 실용서·인문·기술·소설 4 장르 자동 분기. KPIPA·국립국어원·도서정가제·교보문고·알라딘 베스트셀러 + 30+ 한국 출판사 라이브러리 + 자비 출판 5 플랫폼(부크크·텀블벅·인디고·카카오 브런치북·출판사 자비) 내장. **21 → 22 플러그인 · 147 → 155 스킬 · 동기화 지점 169 → 178**.

### Added (신규 1 플러그인 + 8 스킬, moai-book)

- `moai-book:book-concept-planner` — 도서 컨셉서. 의도파악 → 리서치 → 인사이트 도출 3단계 워크플로우. 한 줄(15자)/30자/300자 요약 + USP 3축 + 시장 포지셔닝 매트릭스 + 자비 vs 출판사 투고 의사결정 + 4 장르 프리셋. KPIPA·교보문고·국립국어원 공식 출처 11회 인용. 409 lines.

- `moai-book:book-target-reader` — 타깃 독자 페르소나. 4축 카드(인구통계·라이프스타일·정체성·소비신호) + JTBD 3 차원(기능적·감정적·사회적) + 페인포인트 강도×빈도 매트릭스 4 분면(긴급·핵심·잠재·희귀) + 독서 행동 7항목 + 5인 인터뷰 검증. 한국 KPIPA 국민독서실태조사 인용. 355 lines.

- `moai-book:book-outline-designer` — 목차 설계. 부·장·꼭지 3 레벨 트리 + 분량 배분(200자 원고지) + 5요소 챕터 시놉시스(도입·약속·본문요약·사례·연결) + 페르소나 여정 4단계 검증(1부 끝·중반·마지막 부) + 분량 폭주·부족 검출 + 4 장르 분기. 352 lines.

- `moai-book:book-author-bio` — 저자 약력. 3 신뢰 신호(권위·공감·변화) + 3 길이 약력(50자·200자·500자) + 저자의 말 4단 구조(도입·공감·약속·초대 500-800자) + 신뢰 신호 매트릭스 5 영역 + SNS 채널별(인스타·브런치·링크드인·유튜브·X·카카오) + 페르소나 시뮬레이션. 387 lines.

- `moai-book:book-proposal-writer` — 출판사 투고 제안서. 출판기획서 5섹션 + 샘플 챕터 + 마케팅 플랜 5 카테고리(SNS·강연·언론·북클럽·이벤트) 3 패키지 = A4 12-20장. 출간 전·직후·후 3 단계 마케팅 타임라인(D-90·D+30·D+90) + 거절 신호 사전 검출(USP 약함·타깃 모호·분량 불균형 등) + 4 장르 × 10 출판사 양식 가이드. 501 lines.

- `moai-book:book-publisher-matcher` — 한국 출판사 매칭. 4 차원 평가(장르 적합도 40% · 규모 25% · 계약 조건 20% · 투고 채널 15%) + Top 5 우선순위 추천 + 거절 후 차순위 시나리오(D-0·D+14·D+45·D+90) + 30+ 한국 출판사 라이브러리(IT·실용·인문·문학·아동 + 자비 출판 5 플랫폼) + 협상 포인트 7 체크리스트(인세·선인세·계약기간·전자책·해외판권 등). 446 lines.

- `moai-book:book-chapter-writer` — 챕터 본문 집필. 꼭지 단위 5 요소(훅 10%·본문 70%·클라이맥스 10%·정리 5%·연결 5%) + 4 장르 문체 프리셋(실용·인문·기술·소설) + 200자 원고지 매수 자동 카운트 + 인용 5 유형 + 도표·코드·이미지 자리표시 + 한국 출판사 8곳 어미·문체 컨벤션. 382 lines.

- `moai-book:book-revision-coach` — 퇴고·교열 7 단계 점검(어법·문체·논리·인용·분량·시각자료·일관성) + 4 장르 문체 일관성 검증 + 분량 ±20% 검증 + 인용 5 유형 정합성 + 6 일관성 차원(어미·시점·인물·용어·표기·분량) + 4 체인 검수 순서(korean-spell-check → book-revision-coach → humanize-korean → ai-slop-reviewer). 420 lines.

### 풀 워크플로우 (8 스킬 체이닝)

```
book-concept-planner (컨셉서)
  → book-target-reader (페르소나·JTBD)
  → book-outline-designer (목차·시놉시스)
  → book-author-bio (저자 약력·저자의 말)
  → book-proposal-writer (출판 제안서)
  → book-publisher-matcher (출판사 매칭 Top 5)
  → book-chapter-writer (본문 챕터 집필)
  → book-revision-coach (퇴고 7 단계)
  → moai-content:korean-spell-check (정밀 맞춤법)
  → moai-content:humanize-korean (AI 티 정밀 윤문, 필수)
  → moai-core:ai-slop-reviewer (최종 검수, 필수)
```

### 한국 출판 컨텍스트 (2026 기준)

- **KPIPA 통계**: 한국 출판 시장 데이터·국민독서실태조사·표준 양식
- **국립국어원**: 한글 맞춤법·외래어 표기법·우리말 우선 가이드
- **도서정가제**: 신간 18개월 정가 + 최대 10% 가격할인 + 5% 적립
- **베스트셀러 차트**: 교보문고·알라딘·예스24 3사 통합 권장
- **한국 출판사 30+**: IT(한빛미디어·인사이트·제이펍·길벗 IT) · 실용(웅진·다산북스·길벗·메가스터디북스) · 인문(민음사·문학동네·창비·휴머니스트·은행나무·돌베개) · 문학(민음사·문학동네·창비·문학과지성사·자음과모음) · 아동(비룡소·사계절·창비 어린이)
- **신인 등단 경로**: 문학동네신인상·창비신인상·민음 신인 발굴 + 한국출판문화상·한국과학기술도서상
- **자비 출판 5 대안**: 부크크(POD)·텀블벅 출판 펀딩·인디고·카카오 브런치북·출판사 자비

### Quality

- 8 스킬 4차원 루브릭 자가 평가: 가중 평균 **0.85** (통과 기준 0.70 ✅)
- ai-slop 자체 검수: 8 스킬 모두 **APPROVE**
- frontmatter v2.0.0 정책 준수 (metadata 블록 0건, version 단일 필드)
- vault 외부 참고 자료 원문 비유·표현 직접 인용 0건 (자체 재구성)
- 4 장르 자동 분기 검증 (실용·인문·기술·소설)
- tests/test-cases.yaml: 스킬당 6-9 케이스, 총 60+ test cases

### 동기화 지점 (178)

| 범주 | 경로 | 개수 |
|---|---|---|
| 마켓플레이스 | `.claude-plugin/marketplace.json` | 1 |
| 플러그인 매니페스트 | `<plugin>/.claude-plugin/plugin.json` | 22 (moai-book 신규 1 추가) |
| 스킬 frontmatter | `<plugin>/skills/<skill>/SKILL.md` | 155 (moai-book 신규 8 추가) |

## [2.9.0] - 2026-05-17

MINOR. **Wave 5 — moai-media 이미지 프롬프트 빌더 3종 신설** — GPT-image-2(OpenAI), Gemini 3 Pro Image(Google Nano Banana Pro), Midjourney v8.1 공식 프롬프트 가이드를 그대로 적용한 빌더 스킬 3종. AskUserQuestion 프리셋(제품샷·인물·일러스트·풍경) + 미세조정 라운드로 컨텍스트를 수집하고, 동일 입력을 3개 모델별 어조(6-Block / 5-component / 키워드+`--파라미터`)로 동시 변환해 복붙 가능한 텍스트로 출력. 144 → **147 스킬**, 동기화 지점 166 → **169**.

### Added (신규 3 스킬, moai-media)

- `moai-media:gpt-image-2-prompt` — OpenAI GPT-image-2 전용 프롬프트 빌더. [OpenAI Cookbook](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) 공식 6-Block 구조(Subject·Action·Scene·Composition·Lighting·Style&Text). 편집 시 Change/Preserve/Constraints 2열 로직(`references/editing-patterns.md`). 텍스트 verbatim·ALL CAPS·다국어(한·일·중·힌·벵골) 규칙(`references/text-rendering.md`). 4 프리셋 × 4 슬롯 + 3개 모델 동시 출력. 페어: 기존 `media-gpt-image2-builder`(광고 5장 자동 생성)와 책임 분리 — 본 스킬은 프롬프트 텍스트만.

- `moai-media:gemini-3-image-prompt` — Google Gemini 3 Pro Image (Nano Banana Pro) 전용 프롬프트 빌더. [Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview) 5-component 구조(영문 문장형, Creative Director 어조). 카메라 하드웨어 지정(Fujifilm·GoPro·iPhone 등). Reference image 14 슬롯 전략(`references/reference-images.md`). Search Grounding 활성화 가이드(`references/search-grounding.md`). Thinking vs Fast mode 권장. SynthID 워터마크 안내. 페어: 기존 `nano-banana`(실제 API 호출)와 책임 분리.

- `moai-media:midjourney-v8-prompt` — Midjourney v8.1 (2026.03 Alpha) 전용 프롬프트 빌더. [Midjourney Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List) 기반 키워드+`--파라미터` 구조. `--sref`/`--oref`/`--cw`/`--p` 3대 reference 시스템 deep dive(`references/style-references.md`). 6대 비용·동작 함정 자동 검사(`references/cost-traps.md`) — `--hd --q 4` 16x cost, `--cw 100` 상속 함정, `--cref` deprecation 자동 교체. Midjourney 공식 API 자동화 제한 명시. 페어: Discord/web alpha에서 직접 실행.

### Skill 공통 사양 (3개 동일)

- AskUserQuestion 라운드 ≤ 3, 질문 ≤ 7 (프리셋 + 미세조정 + 화면비·텍스트·고급옵션)
- 출력: 3개 모델 프롬프트 코드블록 + 권장 파라미터 + 한국어 해설 + 페어 스킬 안내
- 책임 경계: **프롬프트 텍스트 산출 전용** (실제 이미지 생성은 페어 스킬 호출)
- 4 프리셋 (제품샷·인물·일러스트·풍경) × 4 슬롯 공유 — 모델별 어조 변환만 다름
- references 4개 + presets 4개 + tests/test-cases.yaml 5-6 케이스 + 회귀 베이스라인
- 루브릭 자가 평가: 0.805 - 0.815 (통과 기준 0.70 ✅)

### 트리거 키워드 (책임 경계)

| 본 스킬 | vs 기존 스킬 |
|---|---|
| "GPT 이미지 프롬프트" | `media-gpt-image2-builder`(GPT 5장 자동 생성)와 분리 — "프롬프트" 명시 |
| "Gemini 이미지 프롬프트", "나노바나나 프롬프트" | `nano-banana`(Gemini 직접 호출)와 분리 — "프롬프트" 명시 |
| "미드저니 프롬프트", "MJ 프롬프트" | (기존 MJ 스킬 없음) — 신규 도메인 |

### 동기화 지점 (+3)

- `.claude-plugin/marketplace.json` × 1
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 147 (Wave 5 신규 3 + 누적)
- 총 **169 지점** 동일 버전 (v2.9.0) 유지

### Migration

- Breaking change 없음
- moai-media 사용자: Wave 5 신규 3 스킬 자동 사용. 별도 설정 없음
- 본 빌더 출력 프롬프트는 OpenAI/Google/Midjourney 공식 가이드 형식이므로 외부 도구(ChatGPT 웹, Google AI Studio, Discord `/imagine`, Sora 등) 호환

### 공식 출처 (각 SKILL.md `## 출처` 섹션에 markdown hyperlink 명시)

- **GPT-image-2**: [OpenAI Cookbook](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide), [openai-cookbook GitHub](https://github.com/openai/openai-cookbook/blob/main/examples/multimodal/image-gen-models-prompting-guide.ipynb)
- **Gemini 3 Pro Image**: [Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image-preview), [Google DeepMind](https://deepmind.google/models/gemini-image/pro/), [Google Cloud Blog Nano Banana guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana), [Vertex AI docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image)
- **Midjourney v8.1**: [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List), [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference), [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference), [Character Reference (deprecated)](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)

---

## [2.8.0] - 2026-05-16

MINOR. **Wave 4 — moai-commerce 한국 D2C 풀스택 완결** — moai-commerce 신규 7 스킬 (MED 5 + LOW 2). 137 → **144 스킬**, 동기화 지점 159 → **166**. (iii) Wave 1-4 결정 완결.

### Added (신규 7 스킬, moai-commerce)

- `moai-commerce:commerce-review-aggregator` — 멀티채널 리뷰 통합 분석. 네이버 스마트스토어·쿠팡·자사몰·YouTube·인스타그램 5채널 → 감정·키워드·인사이트·액션플랜 4단 분석. 채널별 수집 가이드(API·CSV·Graph API). 미리캔버스 PPT 자동화. vault-ecom.md §A-3 MED-1.

- `moai-commerce:commerce-voc-triage` — VOC 우선순위 판별. 3축 분류(고객 핏 ×1-3 / 빈도 ×1-3 / 핵심 가치 관련성 ×1-3) + 우선순위 점수(3축 곱) + KTAS 응급실 5단계 매핑(Level 1 즉시 <1시간 / Level 5 비응급 <1주). 등급별 응답 톤·내용 가이드. vault-ecom.md §A-3 MED-2.

- `moai-commerce:commerce-subscription-strategist` — 구독 비즈니스 모델 설계. 5가지 질문 자기진단(소비 빈도·가격 예측·락인 가치·이탈 방지·시장 검증) + 4 구독 모델 분류(소비재 오이식스 / 경험 VIPS / 관계 쿠팡 로켓와우 / 맞춤 필리) + 한국 시장 적합성 4단계 진단 + 락인 vs 이탈 방지 메시지 매트릭스 6단계. vault-ecom.md §A-3 MED-3.

- `moai-commerce:commerce-influencer-collab` — 인플루언서·UGC 협업 가이드. 5 티어(메가 100만+ / 매크로 10-100만 / 마이크로 1-10만 / 나노 1천-1만 / 메가나노 1천 이하) × 협업 비용·전환율 매트릭스 + 뒷광고 회피 체크리스트 6항목(표시광고법 + 공정위 가이드, 과태료 5,000만원 회피) + UGC 리그램 가이드 + 5축 굿즈 기획(시즌 한정·얼리버드·VIP·인증샷·콜라보). vault-ecom.md §A-3 MED-4.

- `moai-commerce:commerce-early-fan-builder` — 신생 브랜드 충성 100명 부트스트랩. 5원칙(광고 0원·1:1 손편지·UGC 100%·비공개 채널·추천 시스템) + 30일 로드맵(시드 50명 → 100명 → 락인 → 추천) + 100명→1만명 전환 시나리오 + 핵심 지표(재구매율 80%+·평균 10명 추천·LTV/CAC ratio 3+). 블랭크·강아지 가방 케이스. vault-ecom.md §A-3 MED-5.

- `moai-commerce:commerce-trend-namer` — 네이버 데이터랩 트렌드 변환. 카테고리별 급상승 검색어·시즌 트렌드 수집 → 상품명 변형 3안 + 해시태그 세트 30개(카테고리 5·트렌드 10·브랜드 5·일반 10) + 블로그 제목 SEO 3안(C-Rank 친화). vault-ecom.md §A-3 LOW-1.

- `moai-commerce:commerce-season-calendar` — 연간 시즌 캘린더. 한국·글로벌 30+ 시즌 이벤트(1분기 설날·발렌타인·졸업입학 / 2분기 가정의 달·여름 / 3분기 휴가·추석 / 4분기 빼빼로·블프·솽스이·크리스마스) + 카테고리별 매출 피크 매핑(화장품·식품·의류·반려동물·여행) + 분기 캠페인 사전 준비 계획(D-30/D-60/D-90/D-120). vault-ecom.md §A-3 LOW-2.

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 144 (Wave 4 신규 7 + 누적)
- 총 **166 지점** 동일 버전 (v2.8.0) 유지

### Migration

- Breaking change 없음
- moai-commerce 사용자: Wave 4 신규 7 스킬 자동 사용. 별도 설정 없음
- `commerce-review-aggregator` 채널별 API 키 필요 (네이버 커머스·쿠팡 윙·카페24·YouTube·Instagram Graph)

### Wave 1-4 누적 결과 ((iii) 결정 완결)

- 마켓플레이스 130 → **144 스킬** (+14, 누적 14주 작업)
- moai-commerce 22 → **35 스킬** (+13)
- moai-media 13 → **13 스킬** (정리만, Quick Wins 6 + 안 C 책임 명확화 3)
- 어트리뷰션 정책 변경: 정승우님 자료 출처 모두 제거 (내용 보존)
- vault grounding: 1,329 노트 기반 한국 D2C·CRM·LTV·법규 풀스택

### 후속 (별도 결정)

- Wave 5 후보: moai-marketing 보강 또는 moai-content 신규
- 또는 사용자 검증 사이클 (실제 사용 → 보강·정정)

---

## [2.7.0] - 2026-05-16

MINOR. **Wave 3 — 프로모션·재구매·이미지 파이프라인** — moai-commerce 신규 3 스킬. 134 → **137 스킬**, 동기화 지점 156 → **159**.

### Added (신규 3 스킬, moai-commerce)

- `moai-commerce:commerce-promotion-planner` — 3대 프로모션 기획법(이슈화·얼리버드·한정) 전담. 브랜드 단계(신생/스몰/중대형) × 목표(인지도/충성고객/즉각매출) 매트릭스 + 명목·스토리·혜택 3종 세트(HARD) + 벤치마킹 케이스 3개(명목·스토리·혜택 각 1개) + 실무 체크리스트 6항목 + 노션 템플릿 페이지 구조(1-8 섹션) 자동 생성. 비플레인 '듣보잡' 스몰 D2C 12배 매출 케이스 실전 매뉴얼. vault-ecom.md §A-3 HIGH-4 명세 구현. 페어 분리: integrated-strategy=전체 매출 전략, 본 스킬=단일 프로모션 기획서.

- `moai-commerce:commerce-repurchase-timer` — 재구매 타이밍 엔진. 골든타임 3구간 모델(리마인드 0.8T / 데드라인 1.1T / 휴면 1.5T) + 구간별 메시지 톤·채널 매핑(앱 푸시·카톡 친구톡·이메일) + 인센티브 강도(0-5% / 10-15% / 25-40%+사은품) + 리드 스코어링 8개 행동(구매 후 7일 재방문 +10 / 후기 작성 +25 / 친구 초대 +30 / 미접속 60일 -20 / 수신거부 -100) + 리텐션 차트 cohort 분석 가이드(M+1·M+3·M+12 해석 기준) + 한국 10 카테고리 표준 주기 매트릭스(화장품·면도기·콘택트렌즈·반려동물·영양제·잉크·향수 등). vault-ecom.md §A-3 HIGH-5 명세 구현.

- `moai-commerce:commerce-product-image-pipeline` — 상품 이미지·영상 풀스택 파이프라인 오케스트레이터. character-mgmt → image-gen(Soul) → video-gen(DOP) → media-channel-ad-packager 4단계 체인 자동 호출. 3 시나리오(신규 D2C 캐릭터 없음 / 브랜드 마스코트 보유 / 모델 캐릭터 = 가상 인플루언서) + 이미지 5축(Hero·Lifestyle·Detail·Use-case·Result) + 영상 모션 프리셋 자동 선택(스킨케어=slow_zoom / 패션=pan_left / 식품=orbit) + 채널 변환(메타·네이버 GFA·카카오) + media-ai-disclosure 자동 체인 + 비용 추정(₩2,300-4,000/상품 1건). audit §6 안 C 권장 #7 구현. 페어 분리: detail-page-image=13섹션 합성 PNG 1장 / media-model-router=광고 영상 라우팅 / 본 스킬=풀스택 체인 오케스트레이션.

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 137 (신규 3 + 누적)
- 총 **159 지점** 동일 버전 (v2.7.0) 유지

### Migration

- Breaking change 없음
- moai-commerce 사용자: Wave 3 신규 3 스킬 자동 사용 가능. 별도 설정 없음
- `commerce-product-image-pipeline` 사용 시 Higgsfield API 필요

### 후속 예정

- Wave 4 (v2.8.0 예상): commerce MED/LOW 7 (review·voc·subscription·influencer·early-fan·trend-namer·season-calendar) — 신규 7

---

## [2.6.1] - 2026-05-16

PATCH. **Wave 2 보강 3 + Higgsfield 안 C 정리** — 신규 스킬 0, 보강 3, 책임 경계 명확화 3. 134 스킬 유지, 동기화 지점 156 동일.

### Added (보강만, 새 섹션 추가)

**moai-commerce 보강 3** (vault-ecom §A-4)

- `moai-commerce:commerce-channel-message` — 'AARRR 단계별 한국 30+ 브랜드 메시지 풀스택' 섹션 추가. Acquisition(토스·당근·29CM·듀오링고·인프런 등) · Activation(배민·쿠팡·야놀자·클래스101·카카오뱅크 등) · Retention(오프린트미·퍼블리·콜린스·인프런·야놀자·넷플릭스·라운즈·듀오링고·리멤버 등) · Revenue(에이블리·지그재그·무신사·올웨이즈·쿠팡이츠 등) · Referral(토스·당근·우버이츠·카카오페이·야놀자 등) 5단계 × 5-9 브랜드. 3요소 체크리스트(Timely·Personal·Actionable) + 단계별 발송 빈도 권장. vault 1,329 노트 기반 한국 브랜드 풀스택.
- `moai-commerce:commerce-product-naming` — '6질문 상품 파악 프레임 + 데이터랩 트렌드 워크플로우' 섹션 추가. 6질문(Primary Buyer·Motive·Search Intent·USP·Channel-Fit·Seasonality) + 네이버 데이터랩 4단계(트렌드·연관키워드·인구통계·시즌) + 통합 체크리스트(4개 이상 PASS) + MD 11년차 인사이트.
- `moai-commerce:commerce-market-research` — '시장 세분화 + USP 추출 프로세스 (MD 11년차 관점)' 섹션 추가. 4축 세분화(인구·심리·행동·맥락) + 5축 평가(시장크기·성장률·경쟁·진입비용·강점) + USP 3 차별 축(What·How·Why) + 검증 질문 + 다운스트림 일관성 매핑(USP → naming → message → detail-page → campaign).

### Changed (책임 경계 명확화, audit §6 안 C 권장)

**moai-media 2 SKILL.md**

- `moai-media:media-model-router`:
  - description 'Higgsfield MCP 단일 통합' 명시
  - 카테고리 매트릭스 아래 '백엔드 매핑' 표 추가 (HIGH-1 audit 결과 영상 모델 MCP 호출 경로 명확화)
- `moai-media:video-gen`:
  - description '(범용·단순 영상 전용)' 명시
  - '광고 영상 + 카테고리 자동 라우팅이 필요하면 페어 스킬 media-model-router 사용' 안내 추가
  - (HIGH-2 audit Higgsfield 영상 책임 중복 정리)

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 134 (v2.6.0 유지)
- 총 **156 지점** 동일 버전 (v2.6.1) 유지

### Migration

- Breaking change 없음 — 모든 변경이 새 섹션 추가 또는 description 정리
- moai-media 사용자: `media-model-router` 영상 모델 요청 시 Higgsfield MCP로 단일 통합. 추가 설정 없음

### 후속 예정

- Wave 3 (v2.7.0 예상): 신규 2 (`commerce-promotion-planner`·`commerce-repurchase-timer`) + `commerce-product-image-pipeline` 신규
- Wave 4 (v2.8.0 예상): commerce MED/LOW 7 (review·voc·subscription·influencer·early-fan·trend-namer·season-calendar)

---

## [2.6.0] - 2026-05-16

MINOR. **Wave 1 vault grounding 한국 CRM·LTV·법규 통합본** — vault 1,329 노트 + Higgsfield MCP audit + 어트리뷰션 정책 변경. **신규 3 스킬 + Higgsfield Quick Wins 6 + 어트리뷰션 정리**. 130 → **134 스킬**, 동기화 지점 152 → **156**.

### Added (신규 3 스킬, moai-commerce)

- `moai-commerce:commerce-marketing-compliance-kr` — 한국 정통망법 광고·정보성 메시지 자동 게이트. 6대 점검(광고성 판정·옵트인·야간 발송 21시-익일 8시 차단·(광고) 표기 위치·무료 수신거부 명시·발신자 정보) + BLOCK/PASS 판정 + 위반 조항(제50조 1·3·4항, 제76조) + 구체 fix 가이드 + 채널별 베스트/워스트 패턴 카탈로그. 과태료 위험: 1회 위반 최대 3,000만 원 + 책임자 1년 이하 징역. vault-ecom.md §A-3 HIGH-2 명세 구현.

- `moai-commerce:commerce-push-planner` — 앱 푸시 전용 기획 스킬. 4원칙(왜/언제/누구에게/어떻게) + Timely·Personal·Actionable 3요소 자가 점검 + 카피 변형 3안(오늘만 vs 매일 / 누구나 vs 너에게만 / 숫자 vs 게이미피케이션 vs 브랜딩) + 한국 30+ 브랜드 레퍼런스(토스·배민·오늘의집·쿠팡·에이블리·지그재그·29CM·인프런·야놀자·퍼블리·넷플릭스·듀오링고 등) + 클릭률 예측 가이드. 페어 분리: commerce-channel-message는 카톡/SMS/이메일, 본 스킬은 앱 푸시 전용. vault-ecom.md §A-3 HIGH-3 명세 구현.

- `moai-commerce:commerce-ltv-cac-architect` — 고객 단위 수익 구조 설계. CAC→재구매율→구매주기→ARPU→공헌이익→LTV 6대 지표 연결 모델 + LTV/CAC ratio(<1 손실, 1-3 손익분기, 3-5 건강, ≥5 우수) + Payback Period + 광고 의존도 진단(30%+ 위험 → 11-15% 정상) + 손익분기 ROAS 자동 + 채널·세그먼트별 재구매율 분해 + 광고 의존도 탈출 6단계 로드맵(Month 1-6) + 한국 D2C 카테고리별 벤치마크(화장품·식품·패션·가전·펫·구독 SaaS). 페어 분리: commerce-margin-calculator는 단품 마진, 본 스킬은 고객 1명 평생 수익. vault-ecom.md §A-3 HIGH-1 명세 구현.

### Changed (Higgsfield Quick Wins 6, moai-media)

audit `research-2026-05-16/higgsfield-audit.md` §7 즉시 자동 수정 후보 적용:

- `character-mgmt`:
  - MCP 설정 `"command": "uvx"` + `"args": ["higgsfield-mcp"]` → `"command": "higgsfield-mcp"` (CONNECTORS.md pip install 정책과 일치)
  - "베타 기간 무료" stale → "공식 사이트 요금제 확인 (higgsfield.ai)"
- `video-gen`: MCP 툴명 `generate_video_dop` → `higgsfield.generate_video_dop` (네임스페이스 통일)
- `speech-video`: MCP 툴명 `generate_speech_video` → `higgsfield.generate_speech_video`

### Changed (어트리뷰션 정책 변경, refactor)

GOOS 결정으로 정승우님 자료 공식 어트리뷰션을 모두 제거. 출처 클로즈만 제거하고 내용·구조·버전 표기는 그대로 보존하여 사용자 경험 무변동.

- `NOTICE.md`: "정승우님 자료 (Course Material — Permitted Use)" 섹션 전체 + 다른 섹션 내 잔여 언급 3건 제거. moai-cowork 자체 제작 교재 섹션은 유지
- moai-commerce 9 SKILL.md 자료 N §M 인용 + 정승우님 노하우 표현 출처만 제거 (channel-message·automation-audit·product-naming·detail-page-copy·market-research·integrated-strategy·jtbd-persona·coupang-ad-optimizer·commerce-margin-calculator)
- moai-marketing 5 파일 자료 4 §M 인용 + 정승우님 자료 4 풀명 출처만 제거 (sns-content·pixel-audit·campaign-planner·landing-page-conversion-audit·meta-ads-analyzer/references/D.md)
- 2 README(moai-commerce·moai-marketing) 카탈로그 설명 일반화 (정승우님 → 한국 셀러 실전 노하우)

처리 패턴 (GOOS 컨펌): 출처 클로즈만 제거 / 버전 클로즈·헤더 텍스트 유지 / frontmatter description 출처 부분만 제거 일반화. Wave 1.5 commit 552d3a4(어트리뷰션 추가)의 forward fix.

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 134 (신규 3 + 누적)
- 총 **156 지점** 동일 버전 (v2.6.0) 유지

### Migration

- Breaking change 없음
- 정승우님 자료를 직접 참조하던 외부 사용자: 본 버전부터 어트리뷰션 없음. 자체 NOTICE 작성 시 cowork-plugins MIT 라이선스 + 본 리포 출처만 표기 가능
- Higgsfield MCP 사용자: `character-mgmt` MCP 설정 자동 업데이트. `pip install higgsfield-mcp` 확인 필요
- moai-commerce 사용자: Wave 1 신규 3 스킬 자동 사용 가능. 별도 설정 없음

### 후속 예정

- Wave 2: commerce 보강 3(channel-message·product-naming·market-research) + Higgsfield 안 C 정리(model-router·video-gen)
- Wave 3: 신규 2(promotion-planner·repurchase-timer) + product-image-pipeline
- Wave 4: commerce MED/LOW 7(review·voc·subscription·influencer·early-fan·trend-namer·season-calendar)

---

## [2.5.0] - 2026-05-13

MINOR. **메타 광고 audit 3-Layer 인프라 출시** — Layer 3 신규 분석 스킬 1종(`meta-ads-analyzer`, .xlsx 보고서 1-6개 → 9 분석 모듈 + 4D 교차 + 강도별 액션 옵션 + 4 출력 형식) + Layer 2 자체 MCP 서버 신규 1종(`moai-ads-audit-mcp`, claude-ads v1.5.1 MIT 방법론 한국 시장 7 변화 영역 특화 + 10 도구 중 3 도구 + 50/50 pytest pass). 129 → **130 스킬**, 동기화 지점 151 → **152**.

### Added (신규 1 스킬)

**moai-marketing 신규 1**

- `moai-marketing:meta-ads-analyzer` — 메타 광고관리자 `.xlsx` 보고서 1-6개 업로드 → 상품 관여도·운영 철학 반영 진단. 9 분석 모듈(퍼널·KPI·차원·매트릭스·누수·라이프사이클·학습·예산·시뮬레이션) + 4D 교차(광고×지면×연령×성별) + 3 사용자 그룹 톤(인하우스/대행사/소규모, 명시 입력) + 4 출력 형식(HTML/DOCX/PPTX/MD, cowork 공용 디자인 토큰 적용 — `--ivory`/`--paper`/`--slate`/`--clay`/`--clay-d`/`--oat`/`--olive`) + 강도별 액션 옵션(🟢🟡🔴 보수/중도/적극) + claude-ads v1.5.1 (MIT, 4,815 stars) 50-check 매트릭스 한국 시장 매핑. SKILL.md + references A-K 11개 부록 = 12파일 1,829줄. ai-slop-reviewer 자동 체이닝.

### Added (신규 인프라)

**자체 MCP 서버 1종 (cowork-plugins monorepo 첫 MCP 패키지)**

- `mcp-servers/moai-ads-audit/` — Meta Ads audit 전담 자체 MCP 서버 (Python uvx, MIT, v0.1.0). claude-ads v1.5.1 (MIT) 방법론 차용 + 한국 시장 7 변화 영역(벤치마크·8 산업 카테고리·5 규제·5 사용자 그룹·표현 스타일·4 출력 형식·4D 분석) 특화. 가중치 스코어링 공식(`S_total = Σ(C_pass × W_sev × W_cat) / Σ(C_total × W_sev × W_cat) × 100`) + Severity 5.0/3.0/1.5/0.5 + 카테고리 가중치 30/30/20/20 + A-F 등급 + **43 unique check matrix**(Pixel/CAPI 10 + Creative 12 + Account 10 + Audience 7 + Andromeda 4) + 한국 벤치마크 8 카테고리(식품/음료·패션/뷰티·건강기능식품·IT/디지털·가정용품·교육·B2B·기타) + 5 규제(PIPA·ITNA·전상법·표시광고법·식약처). 우선 구현 도구 3종(`audit_meta_account`·`audit_pixel_capi`·`calculate_health_score`). **50/50 pytest pass**. 총 3,813줄(Python+테스트+manifest+문서).

**MCP 등록 인프라**

- `moai-marketing/.mcp.json` 신규 — 2개 MCP 등록 (`meta-ads` hosted at `mcp.facebook.com/ads` + `moai-ads-audit` local stdio via uvx)
- `moai-marketing/CONNECTORS.md` 신규 — `META_ACCESS_TOKEN` 발급 절차 + Layer 1 fallback 옵션 (Adspirer/byadsco/pipeboard) + 10 도구 명세

### 차용 (Attribution)

- [agricidaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) v1.5.1 (MIT, 4,815 stars, 2026-05-13 시점) — Meta 광고 audit 50-check matrix·가중치 스코어링 공식·Quick Wins 로직·EMQ tiered targets·A-F 등급 임계값
- 전체 attribution: `NOTICE.md` §"agricidaniel/claude-ads (MIT)"
- Korean Market Adaptation 7 영역 한국 시장 1차 시민 변환

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 130 (신규 1 포함)
- 총 **152 지점** 동일 버전 (v2.5.0) 유지

### Migration

- Breaking change 없음 — 기존 워크플로우 그대로 동작
- 신규 스킬 호출 예시: "메타 광고 보고서 분석해줘", "케어밀 보고서 진단", "ROAS 낮은 이유", "지면별 분석", "Audience Network 진단"
- MCP 서버 활성화: Claude Code 재시작 시 `moai-marketing/.mcp.json` 자동 인식. Meta 공식 MCP는 OAuth(`META_ACCESS_TOKEN`) 필요. 비활성 환경에서는 `.xlsx` 업로드 fallback 자동 동작 (REQ-AUDIT-MCP-005)
- v2.4.0과의 관계: 본 v2.5.0은 v2.4.0의 로컬 5 커밋(`5922342`·`1a08357`·`e6363f5`·`db260f7`·`99db972`) 위에 누적. v2.4.0은 별도 release 없이 v2.5.0 통합 release로 발행 예정 (GOOS 명시 컨펌 후, 메모리 `feedback_v240_push_confirm.md` 유지)

### 후속 (v2.5.x 또는 v2.6.0 예정)

- `moai-ads-audit-mcp` 잔여 7 도구 구현 (audit_creative_diversity · audit_account_structure · audit_audience_targeting · audit_andromeda_emq · generate_quick_wins · apply_korean_benchmarks · apply_korean_compliance)
- 한국 벤치마크 8 카테고리 수치 정식 검증 출처 확정 (현재 v0.1.0 placeholder, SPEC §7 OQ4)
- claude-ads 50 vs 43 check 차이 7 항목 추가 검토 (SPEC §7 OQ3)
- 표본 부족 셀 마스킹 기준 N값 통일 (SPEC §7.2 미결정)
- v2 단계: TikTok·Naver·Kakao audit 확장
- v3 단계: SaaS UI·다국어·상시 대시보드

## [2.4.0] - 2026-05-12

MINOR. **moai-commerce·moai-marketing 인사이트 통합** — 정승우님 본인 노하우 3개 문서(쿠팡 매출 9배 비법 전자책 126p + 커머스 업무 자동화 24p + 커머스 매출향상 AI 활용 26p) + 광고 심리학 완전판(13장 376줄)을 분석해 **13건(신규 5 + 강화 8)** 통합. 124 → **129 스킬**, 동기화 지점 146 → 151.

### Added (신규 5 스킬)

**moai-commerce 신규 3**

- `moai-commerce:coupang-ad-optimizer` — 쿠팡 광고 풀세트 최적화. 3 캠페인 유형(AI스마트/매출최적화/수동키워드) 자동 분류 + 검색영역 vs 비검색영역 매출 분리 분석(CPM 167배 차이) + 엔드 ROAS(본전 ROAS) 자동 계산 + 자동규칙 3종 가이드(골든타임/350%이상 증액/100%미만 알림) + 상품별 의사결정 분기(ROAS·CTR·CVR). 정승우님 본인 6개월 노하우(월매출 7천→3.6억, 광고비 30%→11.2%) wrapper.
- `moai-commerce:commerce-margin-calculator` — 상품별 마진·엔드 ROAS·손익분기 광고비 자동 계산. 채널별 수수료(스마트스토어 5.94% / 쿠팡 10-12% / 카페24 2-3% / 아임웹 0-2.5%) + 부가세 10% + 결제 수수료 + 쿠폰 자동 반영. 시크릿팡 마진계산기 차용 + AI 챗봇 자연어 입력 차별화.
- `moai-commerce:commerce-automation-audit` — 6대 영역(A 상품운영 / B 가격&프로모션 / C 주문&정산 / D 재고&물류 / E 마케팅&고객 / F 데이터&경영) 진단 + 자동화 3분류(반복형/판단형/창의형) + 우선순위 점수((빈도×시간×오류비용)÷복잡도) + 3 Phase 로드맵(Quick Wins/Core/AI Enhancement) + 5대 KPI + HITL Golden Rule(80% 자동화 + 10배 검수). 정승우님 "커머스 업무 자동화" 24p 풀세트 wrapping.

**moai-marketing 신규 2**

- `moai-marketing:landing-page-conversion-audit` — 랜딩페이지 6섹션(히어로·공감·증명·사회증거·CTA·FAQ) 진단 + 진단 분기(CTR↓→광고 / CVR↓→랜딩 / 장바구니↓→결제) + 빠른 처방 3종(불안해소 문구 +10-20% / 메시지 일치 / 간편결제). 자료 4 §9 wrapper.
- `moai-marketing:pixel-audit` — 메타·구글 픽셀 설치 검증 + 3종 실수 점검(구매자 미제외/이벤트 파라미터 미설정/CAPI 미설치) + 1st Party 데이터 활용 진단 + Lookalike 씨앗 품질 평가(VIP 상위 20% 권장). 자료 4 §5 wrapper.

### Changed (강화 8 스킬)

**moai-commerce 강화 4**

- `commerce-product-naming` 강화 — 공식 4요소 명시 `[브랜드]+[카테고리]+[키워드]+[차별점]` + 매핑 3안 카테고리 명확화(검색 최적화/CTR 최적화/브랜드 강화) + 금지 키워드 9종(최저가·1위·베스트·재입고·인기상품·정품·당일배송·무료배송·특가) + 주의사항 4종(검색어 과다·경쟁사 도용·길이 초과·과장) + 적용 예시 2종(화장품·가전제품)
- `detail-page-copy` 강화 — 7단계 + 25/50/25 비율 가이드 보강 + 좋은/피해야 할 예시 가이드 + PAS 카피 공식 매핑(7단계 ↔ Problem-Agitate-Solution) + 혜택 언어 3단계 변환법(기능→변화→감정)
- `commerce-jtbd-persona` 강화 — JTBD 3분류 카테고리별 예시(다이어트 가루 9개) + 심리적 필요 4종 촉발 패턴(보상심리·불안해소·지루함·사회적자극) + 타겟 온도 4단계 메타데이터(콜드/웜/핫/슈퍼)
- `commerce-channel-message` 강화 — 6 심리 방아쇠(신뢰·손실회피·사회증거·인지쉬움·정체성·앵커링) + 채널별 심리 상태 매트릭스(메타·구글·네이버·카카오·쿠팡) + 인지 편향 8종(프레이밍·후광·타협·현재·매몰비용·제로리스크·선택과부하·디폴트·단순노출)
- `commerce-integrated-strategy` 강화 — 자동화 4단계 프로세스(나열→분류→점수→결정) + 3 Phase 로드맵 + HITL Golden Rule
- `commerce-market-research` 강화 — 포지셔닝 5축(품질/가성비/전문성/편의성/가치관) + 새 카테고리 창출 vs 기존 카테고리 경쟁 분석 + 6대 영역 진단 통합

**moai-marketing 강화 2**

- `campaign-planner` 강화 — 광고 심리학 완전판 통합(성과 공식 + 3 동기 + 6 방아쇠 + 8 편향 + PAS + 후크 6종 + 영상 30초 구조 + 타겟 온도 4단계 × 동기 매트릭스 + 1st Party + LTV/CAC + 단계별 예산 배분)
- `sns-content` 강화 — 채널별 심리 상태 매트릭스 + 메타 학습 기간 48-72시간 가이드 + iOS 14 이후 CAPI·GA4 교차 검증

### 인사이트 원전 (Attribution)

- 정승우님 "쿠팡 매출 9배 올려준 광고관리 비법" 전자책 (126p, 본인 6개월 노하우)
- 정승우님 "커머스 업무 자동화 기획" (24p, 6대 영역 + 자동화 프레임워크)
- 정승우님 "커머스 매출향상을 위한 AI 활용 전략" (26p, JTBD + 페르소나 + 상세페이지 + 상품명)
- "온라인 광고의 심리학" (DOCX, 13장 376줄 완본, 성과 공식 + 심리 방아쇠 + 인지 편향)
- 시크릿팡 마진계산기 로직 참고 (https://secretpang.kr/?ref=pdf)

### 후속 (v2.5.0 예정)

- Track A MoAI-Commerce MCP 서버 (광고 4종 + Phase 1 34종 + Higgsfield 통합)

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21
- `<plugin>/skills/<skill>/SKILL.md` × 129 (신규 5 포함)
- 총 **151 지점** 동일 버전 (v2.4.0) 유지

### Migration

- Breaking change 없음 — 기존 워크플로우 그대로 동작
- 신규 5 스킬은 필요할 때 자연어로 호출 ("쿠팡 광고 분석해줘", "마진 계산해줘", "자동화 진단해줘", "랜딩 진단해줘", "픽셀 점검")

## [2.3.0] - 2026-05-12

MINOR. **moai-commerce에 시장조사·JTBD·상품명·채널 메시지·통합전략 등 17 신규 스킬 + moai-education 2 신규 스킬 + Track C 책임 경계 정리**. 124 → 141 스킬, 동기화 지점 146.

### Added (신규 17 스킬)

**moai-commerce 도메인 확장 (5 신규)**

- `moai-commerce:commerce-market-research` — trend_search · trend_shopping_categories · trend_shopping_keywords · keyword_for_product_idea 4종 MCP 호출 → 거시·경쟁·검색 3축 시장 1장 리포트
- `moai-commerce:commerce-jtbd-persona` — 1스킬 2모드. `--mode jtbd` (기능·감성·사회 각 3개 = JTBD 9개) / `--mode persona` (review_list_naver·review_list_cafe24·qna_list_cafe24 → 페르소나 3명 8필드). 본인 리뷰 10건 미만 시 fallback 자동 적용
- `moai-commerce:commerce-product-naming` — keyword_search_volume·keyword_related·keyword_bulk_research → 상품명 3안 (검색·CTR·브랜드) + 스마트스토어/쿠팡/네이버쇼핑 25자·금지어 검증
- `moai-commerce:commerce-channel-message` — keyword_seasonal_calendar·ad_keyword_performance + NCM 프레임워크 (Need→Channel→Moment→Message→CTA) → 검색·광고·CRM × 5종 = 15종 메시지 (채널별 다른 표현 강제)
- `moai-commerce:commerce-integrated-strategy` — dashboard_morning_brief·sales_compare_channels·ad_roas_summary → 매출 향상 전략 1장 (실행 우선순위 Top 3)

**moai-media 도메인 확장 (6 신규, v2.11.0에서 일부 정리)**

- `moai-media:media-moodboard` — 페르소나·카피·카테고리 → 색팔레트 3종 + 톤 키워드 5개 + 레퍼런스 이미지 5장
- `moai-media:media-gpt-image2-builder` — 자연어 한 줄 → 8단계 프롬프트 자동 리라이팅 → GPT Image 2 호출
- `moai-media:media-model-router` — 카테고리 매트릭스 자동 라우팅 (의류=Kling 3 / 뷰티=Veo 3 / 건강식품=Kling 3 / 생활용품=Seedance). Higgsfield 동시 호출 비용 폭증 방지 위해 시차 호출 (5분 간격)
- `moai-media:media-channel-ad-packager` — 메인 영상 + 보조 영상 + 채널 메시지 → 메타 1:1·9:16 / 네이버 GFA 길이 / 카카오 알림톡 변수 / 카카오모먼트 1:1·16:9 채널별 자동 변환
- `moai-media:media-ai-disclosure` — 광고심의·소비자보호법 대비 "AI 생성" 메타데이터·워터마크 자동 부착 (캔바 매직 레이어 수정 후에도 표기 유지)
- `moai-media:media-canva-magic-layer` — 합성 PNG → 카피만 분리 → 시즌 재사용 5단계 가이드 (GPT Image 2 재호출 대비 90% ↓)

**moai-core·moai-commerce 셋업/일일 운영 (3 신규)**

- `moai-core:mcp-connector-setup` — Drive · Notion · Higgsfield · OpenAI 4커넥터 인증 가이드 + 트러블슈팅
- `moai-commerce:commerce-morning-brief` — dashboard_morning_brief MCP → 어제 주문·신규 문의·트렌드·ROAS 1개 호출 통합 1줄
- `moai-commerce:commerce-order-summary` — order_summary_today MCP → 스마트스토어 + 카페24 + 아임웹 채널 통합 신규 주문 1줄

**moai-education 활성화 (2 신규, 0 → 2 스킬)**

- `moai-education:course-followup-sequence` — 코스 종료 후 D+1·D+3·D+7·D+14·D+30 후기 카피 5종 + 30일 자산화 시퀀스 + SUNO BGM·MCP Phase 1 직접 호출 가이드
- `moai-education:course-curriculum-design` — 1일~16주 코스 운영 매뉴얼 자동 생성 (표준 시간표·강사·조교 동선·사전 준비물·Plan B 시나리오 5건+)

### Changed (6 강화 + Track C 정리)

- **`moai-commerce:detail-page-copy` 강화** — 기존 13섹션 모드 하위 호환 유지. 신규 `--mode diagnose` (7단계 진단 점수, 단계별 개선 제안) + `--mode copy` (페르소나 2세트 카피, 비율 25/50/25 강제)
- **Track C 페어 정리 — 통합 1건**: `moai-content:social-media` → `moai-marketing:sns-content` 흡수 (글로벌 4채널 모드 추가: 스레드·X·링크드인·유튜브 쇼츠). social-media는 deprecate stub + 리디렉션 안내. 한국 3채널 모드(인스타·네이버 블로그·카카오)는 유지
- **Track C 페어 정리 — 책임 분리 1건**: `moai-marketing:campaign-planner`의 "이커머스 상세페이지 제작 · AI 이미지 생성" 책임 제거. 상세페이지 카피는 detail-page-copy, 상세페이지 합성 이미지는 detail-page-image, AI 이미지·영상은 moai-media:* 사용 안내로 이관
- **Track C 페어 정리 — description [책임 경계] 명확화 15건**: copywriting/commerce-copywriting (Pair 1), product-detail/detail-page-copy (Pair 2), personal-branding/brand-identity (Pair 5), target-script (Pair 6), performance-report/executive-summary (Pair 7), market-analyst/sbiz365-analyst (Pair 8), daily-briefing (Pair 9), landing-page (Pair 10) + sns-content·campaign-planner

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21 (version)
- `<plugin>/skills/<skill>/SKILL.md` × 124 (version, 신규 17 포함)
- 총 **146 지점** 동일 버전 (v2.3.0) 유지

### Migration

- 기존 `/social-media` 호출 코드는 v2.5.0까지 deprecate stub으로 유지. `/sns-content` 사용 권장
- 기존 `/campaign-planner` 호출 시 "상세페이지 만들어줘"는 더 이상 routing되지 않음. `/detail-page-copy` 또는 `/detail-page-image` 직접 호출
- `moai-education`이 0 스킬에서 2 스킬로 활성화됨 — Cowork에서 플러그인 설치 시 자동 사용 가능

## [2.2.1] - 2026-05-11

PATCH. docs-site에서 Hugo 템플릿 변수가 마크다운 파일 내에서 치환되지 않는 버그를 수정했습니다.

### Fixed

- **변수 치환 버그** — 마크다운 파일 내 HTML에서 `{{ site.Params.version }}`이 렌더링되지 않는 문제 수정
  - **Shortcodes 도입**: `version.html`, `release-date.html` 생성
  - **_index.md 수정**: `{{ site.Params.version }}` → `{{< version >}}`, `{{ site.Params.releaseDate | replace "-" "." }}` → `{{< release-date >}}`
  - **Partial 추가**: `version-badge.html` 컴포넌트
  - 헤더 버전이 정상적으로 "v2.2.1"로 노출됨

### Changed

- docs-site/content/_index.md: Hugo shortcodes로 변수 참조 방식 변경
- docs-site/layouts/shortcodes/: version, release-date shortcodes 추가
- docs-site/layouts/partials/: version-badge partial 추가

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21 (version)
- `<plugin>/skills/<skill>/SKILL.md` × 108 (version)
- 총 **130 지점** 동일 버전 유지

---

## [2.2.0] - 2026-05-09

MINOR. 마크다운 보고서를 단일 파일 HTML로 변환하는 `moai-content:html-report` 스킬을 신규 도입했습니다. Thariq Shihipar의 "unreasonable effectiveness of HTML" 사상을 기반으로, **외부 의존성 0개**(한글 웹폰트 CDN 1개만 예외)로 12-25KB 산출물을 생성합니다. 6개 보고서 모드(status/incident/plan/explainer/financial/pr) + 6개 통합 테스트(executive-summary/financial-statements/sbiz365-analyst/daily-briefing 등 4종)를 포함합니다. 마켓플레이스 스킬 107 → **108개**, 플러그인은 21개 유지. Breaking change 없음.

### Added

- **`moai-content:html-report`** — 마크다운 보고서를 단일 파일·자체 완결형 HTML로 변환하는 터미널 렌더러. Thariq HTML-effectiveness 아키텍처 기반, 외부 JS/CSS 프레임워크 의존성 0.
  - **6개 보고서 모드**: status (주간 현황 / 태스크 리스트), incident (포스트모템 / 우발 대응), plan (구현 계획 / 사업 계획), explainer (기능 설명 / 개념 해설), financial (재무 보고 / 수익 동향), pr (PR 서사 / 관계자 알림)
  - **인라인 SVG + vanilla JS** — 12-25KB 산출물, 페이지 로딩 거의 무영향. `<script>`, 이벤트 핸들러, 차트·테이블 인터랙션은 모두 inline.
  - **한글 폰트 매핑** — Pretendard (기본), Noto Serif KR (serif mode), Noto Sans KR (sans), 조선일보명조 (조선일보 수거), KoPubWorld 명조, JetBrains Mono (코드 블록). 모드별 자동 선택 또는 `font_stack` 오버라이드.
  - **인쇄 친화** — `@media print` 자동 적용, 페이지 나누기 최적화, 하이퍼링크 유지.
  - **CSS 변수 계약** — `--ivory`, `--slate`, `--clay`, `--oat`, `--olive`, `--sans`, `--serif`, `--mono` 8개. 모드별 기본값 포함.
  - **P1 컨슈머 4종 호환성 검증** — executive-summary, financial-statements, sbiz365-analyst, daily-briefing 모두 4/5 호환성 통과.
  - **6개 템플릿** + **6개 통합 테스트** + **design-tokens.md** (CSS 변수 명세) + **fonts.md** (폰트 매핑·CDN)
  - **옵션**: `mode`, `slug`, `output_path`, `font_stack`, `dark_mode`
- **권장 체인** — 텍스트 산출물: `[텍스트 스킬] → moai-core:ai-slop-reviewer → moai-content:humanize-korean → moai-content:html-report mode=<X>`
- **README attribution** — moai-content/README.md에 Thariq Shihipar "unreasonable effectiveness of HTML" 아이디어 출처 표기.

### Changed

- README.md: Version 배지 2.1.0 → **2.2.0**, Skills 배지 107 → **108**, v2.2.0 하이라이트 섹션 추가, 영문 description "21 plugins · 108 skills" 갱신
- moai-content/README.md: 10개 → **11개** 스킬 표기, html-report 행 추가, 텍스트·영상·보고서 표현 갱신
- moai-content/.claude-plugin/plugin.json: description·keywords에 html-report·마크다운·보고서·렌더러·리포트 추가
- .claude-plugin/marketplace.json: `metadata.version` 2.1.0 → **2.2.0**, moai-content description 갱신, 마켓플레이스 description "html-report 신규" 표기
- 전 SKILL.md `version: 2.1.0` → `version: 2.2.0` (108개, html-report 포함, Cowork 자동 업데이트 감지)
- 전 plugin.json `version` → 2.2.0 (21개)

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21 (version)
- `<plugin>/skills/<skill>/SKILL.md` × 108 (version, +1 신규 html-report 포함)
- 총 **130 지점** 동일 버전 유지

### Migration

- 사용자 조치: `/plugin marketplace update cowork-plugins` 후 플러그인 상세 재진입
- Breaking change 없음 — 기존 워크플로우 그대로 동작
- 보고서 산출물이 필요할 때 `html-report`를 자연어로 호출하면 됩니다("주간 보고서 HTML로", "재무제표 HTML 변환" 등)

## [2.1.0] - 2026-05-07

MINOR. 한국어 AI 티 정밀 윤문 도입 — [`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai) v1.6.1 (MIT, ⭐937 stars) Fast 모드 단일 스킬 변형을 `moai-content:humanize-korean`으로 포팅했습니다. 기존 `moai-core:ai-slop-reviewer`는 그대로 유지되며, 권장 체인은 `… → ai-slop-reviewer (1차 일반) → humanize-korean (2차 한국어 정밀)` 입니다. 마켓플레이스 카운트 106 → **107 스킬**, 플러그인은 그대로 21개. Breaking change 없음.

### Added

- **`moai-content:humanize-korean`** — 한국어 AI 티 정밀 윤문 스킬. 10대 카테고리 × 40+ 패턴 SSOT(`ai-tell-taxonomy.md` 40KB)를 S1/S2/S3 심각도로 분류하여 수술적 윤문. **의미 100% 보존 가드**(고유명사·수치·날짜·인용 변경 금지, 변경률 30% 경고 / 50% 강제 중단), **자체검증 6항**, **A/B/C/D 등급 자동 판정**. Python 표준 라이브러리만 쓰는 `metrics.py`(외부 의존 없음)로 사전·사후 정량 메트릭 측정.
  - 카테고리: A 번역투('-를 통해'/'-에 있어서'/이중 피동), B 영어 인용 과다, C 구조 패턴(이모지·콜론 부제·연결어미 쉼표), D AI 관용구(결론적으로/시사하는 바·hype 어휘·결말 공식), E 리듬 균일성, F 한자어 -성/-적/-화 밀도, G hedging, H 문두 접속사 남발, I 형식명사 과다, J 시각 장식 남용
  - 산출물: `_workspace/{run_id}/{01_input.txt, 00_metrics.json, final.md, summary.md, 06_metrics_after.json}`
  - 옵션: 장르(칼럼/리포트/블로그/공적), 강도(보수/기본/적극), 최소심각도(S1/S2/S3)
  - 권장 체인: `… → moai-core:ai-slop-reviewer → moai-content:humanize-korean`
- **`references/strict-pipeline-spec.md`** — 원본의 7인 에이전트 Strict 5인 파이프라인 명세 보존(향후 독립 플러그인·Agent Teams 모드 확장 시 참조). 현재 스킬에서는 미사용.
- **README attribution** — 루트 README.md와 `moai-content/README.md`에 [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) (MIT License, ⭐937) 출처 표기.

### Changed

- README.md: Version 배지 2.0.0 → **2.1.0**, Skills 배지 106 → **107**, v2.1.0 하이라이트 섹션 추가, 영문 description "21 plugins · 107 skills"로 갱신
- moai-content/README.md: 9개 → 10개 스킬 표기, humanize-korean 행 추가
- moai-content/.claude-plugin/plugin.json: description·keywords에 humanize-korean·한국어윤문·AI티제거·humanize 추가
- .claude-plugin/marketplace.json: `metadata.version` 2.0.0 → **2.1.0**, moai-content description 갱신, 마켓플레이스 description 한 줄 갱신
- 전 SKILL.md `version: 2.0.0` → `version: 2.1.0` (107개, Cowork 자동 업데이트 감지)
- 전 plugin.json `version` → 2.1.0 (21개)

### 동기화 지점

- `.claude-plugin/marketplace.json` × 1 (metadata.version)
- `<plugin>/.claude-plugin/plugin.json` × 21 (version)
- `<plugin>/skills/<skill>/SKILL.md` × 107 (version, +1 신규 humanize-korean 포함)
- 총 **129 지점** 동일 버전 유지

### Migration

- 사용자 조치: `/plugin marketplace update cowork-plugins` 후 플러그인 상세 재진입
- Breaking change 없음 — 기존 워크플로우 그대로 동작
- 한국어 텍스트 산출물에서 더 정밀한 윤문이 필요할 때 `humanize-korean`을 자연어로 호출하면 됩니다("AI 티 없애줘", "사람이 쓴 것처럼 윤문해줘", "한글 AI 윤문" 등)

### Attribution

- [`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai) v1.6.1 (MIT License, ⭐937 stars) — taxonomy(40KB SSOT)·rewriting-playbook·quick-rules·metrics.py·baseline.json·web-service-spec·test_metrics.py 모두 원본 그대로 보존. SKILL.md만 cowork v2.0+ frontmatter 정책(version 단일 필드, metadata 블록 금지, user-invocable)과 단일 스킬 워크플로(에이전트 호출 제거)에 맞춰 재작성.
- 원본 라이선스(MIT)는 cowork-plugins MIT와 호환되며, 추가 의무 없음. NOTICE는 README attribution으로 대체(사용자 결정).

## [2.0.0] - 2026-05-04

MAJOR. 한국 B2B 시장 특화 강화 릴리스 — `NomaDamas/k-skill` (MIT) 한국 특화 스킬 6종을 cowork에 포팅했습니다. 인터넷등기소 등기부등본 일괄 발급, 국토부 실거래가, 식약처 의약품·식품 안전, 법원경매 매각공고, KRX 시세, 바른한글 맞춤법 검수까지 — 한국 시장에서 즉시 ROI가 발생하는 도메인 특화 스킬을 한꺼번에 도입했습니다. 마켓플레이스 카운트 100 → **106 스킬**, 플러그인은 그대로 21개.

### Added

- **`moai-legal:iros-registry-automation`** — 대법원 인터넷등기소(IROS) 법인·부동산 등기부등본 일괄 발급 보조. 로그인·결제는 사용자가 브라우저에서 직접 처리하고, 본 스킬은 장바구니 담기·결제 후 열람·저장·종합 리포트 생성을 보조합니다. 원 저작자 `challengekim/iros-registry-automation` (MIT) 참고. 실사·법무 검토·법인 일괄 관리에 핵심.
- **`moai-business:real-estate-search`** — 국토교통부(MOLIT) 실거래가/전월세 조회. 아파트·오피스텔·연립다세대·단독다가구·상업업무용 매매·전월세 시세를 NomaDamas k-skill-proxy 경유로 조회. 사용자 측 API 키 불필요. 원 저작자 참고: `tae0y/real-estate-mcp`.
- **`moai-commerce:mfds-safety`** — 식품의약품안전처(MFDS) 의약품·식품 안전 통합 체크. e약은요·안전상비의약품·건강기능식품 원료 인정현황·개별인정형·품목제조 신고·검사부적합·회수·판매중지를 통합 조회. 증상·복용/섭취 상황 인터뷰 우선, red flag 시 119·응급실 안내. 헬스/F&B 커머스 상품 검수 핵심.
- **`moai-finance:court-auction-search`** — 대법원 법원경매정보(`courtauction.go.kr`) 매각공고 조회. 매각기일·법원·기일/기간 입찰 기준 조회 + 사건번호 단건 조회. read-only, IP 차단 방지를 위해 호출당 약 2초 지연. 자산 처분·경매 투자·실사에 활용.
- **`moai-finance:korean-stock-search`** — KRX(한국거래소) 상장 종목 검색·기본정보·일별 시세. NomaDamas k-skill-proxy 경유로 사용자 KRX_API_KEY 발급 불필요. moai-business의 DART(공시)를 보완하는 시세 데이터.
- **`moai-content:korean-spell-check`** — 바른한글(구 부산대 맞춤법/문법 검사기) 표면을 이용한 한국어 최종 검수. 국립국어원 계열 규칙 반영. AI 패턴 검수(`ai-slop-reviewer`) 직후의 마지막 단계로 권장. 비상업·저빈도 사용 정책 명시.
- **NOTICE.md** — `NOTICE.md`에 NomaDamas/k-skill MIT attribution 섹션 추가. 6개 포팅 스킬과 원 저작자 링크 보존.
- **CONNECTORS.md 신규/확장** — `moai-commerce/CONNECTORS.md` 신규(MFDS), `moai-finance/CONNECTORS.md` 신규(법원경매·KRX), `moai-business/CONNECTORS.md`에 MOLIT 실거래가 섹션 추가, `moai-legal/CONNECTORS.md`에 IROS 섹션 추가.

### Changed

- **마켓플레이스 description 갱신** — v2.0.0 한국 특화 6종 도입 사실을 marketplace.json에 반영. 스킬 카운트 100 → 106.
- **버전 통일 22지점** — marketplace.json + 21개 plugin.json 모두 `2.0.0`으로 동기화.

### Migration

- **사용자 측 영향 없음 (Breaking change 아님)** — 신규 스킬 6종 추가일 뿐 기존 스킬·체인은 그대로 동작합니다.
- **MAJOR bump 사유**: 한국 B2B 시장 특화 도메인 도입은 cowork 정체성의 단계적 변화이므로 1.x → 2.x로 표기. 기능 호환성 손실은 없습니다.
- **k-skill-proxy 의존 명시** — `real-estate-search`, `mfds-safety`, `korean-stock-search`는 NomaDamas 운영 hosted 프록시 경유. self-host가 필요하면 `KSKILL_PROXY_BASE_URL` 환경변수로 대체 가능.
- **사용자 측 시크릿** — 신규 6종 모두 사용자 측 API 키 발급 불필요. self-host 시에만 운영 측에서 `DATA_GO_KR_API_KEY`, `FOODSAFETYKOREA_API_KEY`, `KRX_API_KEY` 발급.

### 출처 및 어트리뷰션

- 소스 리포지토리: [`NomaDamas/k-skill`](https://github.com/NomaDamas/k-skill) (MIT)
- 통합 어트리뷰션: `NOTICE.md` § NomaDamas k-skill (MIT)
- 원 저작자 보존:
  - `challengekim/iros-registry-automation` (iros)
  - `tae0y/real-estate-mcp` (real-estate)
  - `jjlabsio/korea-stock-mcp` (korean-stock)

## [1.8.1] - 2026-05-02

PATCH. 정합성 동기화 릴리스 — 신규 플러그인 `moai-bi`·`moai-pm`·`moai-sales` 3종을 marketplace에 정식 등록하고, 온라인 문서·SKILL 내부 stale 참조를 일괄 정리했습니다. 신규 스킬 추가는 없습니다(다음 MINOR에서 추가 예정).

### Added

- **마켓플레이스 등록 +3** — `moai-bi`(BI 대시보드·경영진 1pager), `moai-pm`(주간보고·OKR), `moai-sales`(B2B 영업·제안서) 3개 플러그인이 marketplace.json `plugins[]`에 정식 추가됨. 마켓플레이스 카운트 18 → **21 플러그인**.
- **신규 docs 페이지 3종** — `docs-site/content/plugins/{moai-bi,moai-pm,moai-sales}.md` 작성. 카탈로그에서 클릭 시 더 이상 404가 발생하지 않음.
- **`docs-site/content/cowork/constraints.md` 신설** — 요금제·세션·플러그인·커넥터·Team/Enterprise 거버넌스 시스템 한도 한 페이지(Cowork 사용자 관점, 개발자용 Claude Code 개념 분리).
- **`docs-site/content/cowork/troubleshooting.md` 전면 확장** — 6 섹션 → 10 섹션, 빠른 진단표 + 설치/폴더/스킬 호출/플러그인 설치/커넥터/세션/권한/프록시 종합.
- **`docs-site/content/cookbook/legal-nda-batch.md` 신설** — NDA 일괄 검토 파이프라인 레시피(영업비밀보호법 §2 적용 명시).
- **`docs-site/content/plugins/moai-commerce.md` 신설** — v1.8.0의 11스킬·8채널 풀세트 카탈로그 페이지.

### Changed

- **README** — Plugins 배지 18 → **21**, 한국어/영문 intro 문장 동기화.
- **marketplace.json metadata.description** — "18 플러그인, 100 스킬" → **"21 플러그인, 100 스킬"**, bi/pm/sales 추가 안내.
- **`moai-media` plugin.json description** — Kling/Ideogram/ElevenLabs stale 표기 제거 → 실제 7스킬 기준 갱신.
- **`moai-media/README.md` 전면 재작성** — 5스킬 카탈로그(kling/ideogram/elevenlabs/nano-banana) → **6스킬 카탈로그**(nano-banana/image-gen/video-gen/audio-gen/speech-video/character-mgmt), 마이그레이션 안내 추가.
- **`moai-core/skills/project/SKILL.md`·`init-protocol.md`** — 미디어 스킬 매핑·API 키 안내를 7스킬 기준으로 갱신, kling→video-gen·elevenlabs→audio-gen 워크플로우 매핑.
- **`moai-commerce/skills/{detail-page-image,live-commerce}/SKILL.md`** — `moai-media:ideogram`/`moai-media:kling` 호출 안내를 `nano-banana`(한국어 타이포 SOTA)·`video-gen`으로 재정렬.
- **`moai-content/skills/landing-page/SKILL.md`** — 이미지 생성 스킬 안내에서 `ideogram` 제거.
- **`moai-media/skills/{nano-banana,image-gen}/SKILL.md`** — 관련 스킬 목록을 실재하는 7스킬 기준으로 갱신.
- **`docs-site/content/cowork/faq.md` Q9** — 1M 컨텍스트 사실 추가, Claude Code CLI 명령(`/clear`) 표현을 Cowork 자연어 안내로 교체.
- **여러 cookbook/plugins 페이지** — 제거된 스킬 `kling`·`ideogram`·`elevenlabs` 직접 호출 표기를 실제 스킬명으로 일괄 정정 (skill-chaining, blog-pipeline, track-marketing, plugins/moai-content, plugins/moai-media).

### Fixed

- **Claude Cowork ↔ Claude Code 개념 혼재 제거** — 사용자 문서 `cowork/constraints.md`·`troubleshooting.md`에 `SLASH_COMMAND_TOOL_CHAR_BUDGET`·`run_in_background`·`/clear`·`.mcp.json` JSON 편집 등 개발자 CLI 개념이 다수 섞여 있던 것을 발견·전면 재작성. 향후 재발 방지를 위한 19개 금지 토큰 자동 검사 메모리 등록.

### Migration

사용자 측 갱신:

```text
/plugin marketplace update cowork-plugins
```

이후 좌측 사이드바 → 사용자 지정 → 마켓플레이스 → cowork-plugins에서 `moai-bi`·`moai-pm`·`moai-sales` 신규 항목 확인 후 필요한 것만 설치하세요. 기존 17개 플러그인은 그대로 동작합니다 (Breaking change 없음).

### 동기화 지점 (22)

- `.claude-plugin/marketplace.json` × 1
- `moai-{bi,business,career,commerce,content,core,data,education,finance,hr,legal,lifestyle,marketing,media,office,operations,pm,product,research,sales,support}/.claude-plugin/plugin.json` × 21

## [1.8.0] - 2026-05-01

MINOR. **`moai-commerce` 5 → 11 스킬 대폭 확장** — 한국 이커머스 풀세트로 진화. 자사몰(D2C) + 크라우드펀딩 + 큐레이션 + 라이브 커머스 + 통합 마케팅 전략·카피까지 한 플러그인에서 처리합니다. 큐텐 사태로 사실상 폐업한 티몬·위메프는 가이드에서 제외되었습니다.

### Highlights

- **`moai-commerce` 6 신규 스킬**:
  - **`marketplace-d2c`** — 카페24·아임웹·메이크샵 자사몰 빌더 통합 가이드(도메인·결제·배송·SEO·광고 채널 연동·D2C 운영 전략).
  - **`marketplace-crowdfunding`** — 와디즈·텀블벅 크라우드펀딩 프로젝트 기획·심사·운영(영상 시놉시스, 리워드 5단계 가격 구성, 메이커 등록).
  - **`marketplace-curation`** — 카카오 메이커스·무신사·29CM 큐레이션 채널 입점 제안(브랜드 소개서, 시너지 평가, MD 협업).
  - **`commerce-strategy`** — 통합 마케팅 전략(채널 믹스, 3단계 가격 구조, 시즌 프로모션 캘린더, 리텐션 자동화, KPI 대시보드).
  - **`commerce-copywriting`** — 이커머스 특화 광고·톡톡·푸시·이메일 카피(채널별 길이 제약, A/B 옵션 3개, ai-slop 자동 체이닝).
  - **`live-commerce`** — 네이버·카카오·그립·쿠팡 라이브 커머스 채널 가이드 + 30/60분 진행 스크립트(오프닝→상품→채팅→마감 카운트다운).
- **`marketplace-naver` 정정** — 티몬·위메프 가이드 제거(큐텐 인수 후 2024년 미정산 사태로 회생절차 진입). 미정산 피해 셀러를 위한 archive 안내 표기.
- 마켓플레이스 카운트 18 플러그인, 94 → **100 스킬**.

### Added

- `moai-commerce/skills/marketplace-d2c/SKILL.md` + `references/{cafe24.md, imweb.md, d2c-strategy.md}` + `tests/test-cases.yaml`.
- `moai-commerce/skills/marketplace-crowdfunding/SKILL.md` + `references/{wadiz.md, tumblbug.md}` + `tests/test-cases.yaml`.
- `moai-commerce/skills/marketplace-curation/SKILL.md` + `references/{kakao-makers.md, musinsa.md, 29cm.md}` + `tests/test-cases.yaml`.
- `moai-commerce/skills/commerce-strategy/SKILL.md` + `references/{channel-mix.md, pricing.md, promotion.md, retention.md, kpi.md}` + `tests/test-cases.yaml`.
- `moai-commerce/skills/commerce-copywriting/SKILL.md` + `references/{ad-copy.md, talk-copy.md, push-copy.md, email-sequence.md}` + `tests/test-cases.yaml`.
- `moai-commerce/skills/live-commerce/SKILL.md` + `references/{naver-shoppinglive.md, kakao-shoppinglive.md, grip.md, coupang-live.md, live-script.md}` + `tests/test-cases.yaml`.

### Changed

- `moai-commerce/skills/marketplace-naver/SKILL.md` — 티몬·위메프 언급 제거, archive 안내 추가.
- `moai-commerce/skills/marketplace-naver/references/openmarket-common.md` — 티몬·위메프 표·정산·후기·시즌 칸 모두 제거. 큐텐 사태 archive 표기.
- `moai-commerce/README.md` — 11 스킬 카탈로그(상세페이지 3 / 채널 가이드 5 / 마케팅 3) + 표준 워크플로우 확장 + 채널 분류 표.
- `.claude-plugin/marketplace.json` — `metadata.version` 1.7.0 → 1.8.0, `metadata.description` "94 스킬" → "100 스킬", moai-commerce description 11 스킬 반영.
- 모든 `<plugin>/.claude-plugin/plugin.json` (21개) — `version` 1.7.0 → 1.8.0 일괄 동기화.
- `README.md` (루트) — Version 배지 1.7.0→1.8.0, Skills 94→100, v1.8.0 하이라이트 섹션 신설, moai-commerce 카탈로그 행 11 스킬로 갱신.

### Removed

- `marketplace-naver` 가이드에서 티몬·위메프 모든 운영 항목(이미지 규격·상품명·후기·시즌·정산) 제거. 본 채널은 큐텐 인수 후 2024년 미정산 사태로 사실상 폐업·회생절차에 진입했습니다.

### Migration

- 사용자 측 캐시 갱신: `/plugin marketplace update cowork-plugins` 실행 후 신규 스킬 활성화.
- 기존 워크플로우 영향 없음. Breaking change 없음. 기존 5개 스킬은 그대로 동작합니다.
- 티몬·위메프 운영 가이드를 참고하던 사용자: 채널 폐업으로 인해 가이드를 갱신하지 않습니다. 미정산 피해 셀러는 [중소벤처기업부 피해 지원](https://www.mss.go.kr) 또는 회생법원 공지 참조.

## [1.7.0] - 2026-05-01

MINOR. **신규 플러그인 `moai-commerce` 추가 — 한국 이커머스 상세페이지(상폐) 자동화**가 핵심입니다. 13섹션 감정여정 카피 생성, 1080×12720 단일 PNG 자동 합성, 쿠팡·네이버·오픈마켓 가이드를 한 번의 자연어 호출로 완성합니다.

### Highlights

- **`moai-commerce` 신규 플러그인 신설** — 한국 이커머스 상세페이지 자동화 도메인 진입. 5개 스킬 + Pillow 자체 합성 스크립트 + 채널별 마켓 가이드 + 사진 촬영 브리프 풀세트 제공.
- **`detail-page-copy`** — 13섹션 감정여정(Hero→Pain→Problem→Story→Solution→How→Proof→Authority→Benefits→Risk→Compare→Filter→CTA) 카피 생성. 10개 카테고리(electronics/fashion/food/beauty/home/supplement/pet/kids/handmade/general) 어조 가이드. **출력 직전 ai-slop-reviewer 자동 체이닝** (HARD 규칙 준수).
- **`detail-page-image`** — 13섹션 이미지 프롬프트 생성 → `moai-media:nano-banana` 호출 → **Pillow 단일 의존성으로 1080×12720 세로 합성 PNG 산출**. 외부 패키지 설치 불필요. 부분 실패 시 다크 플레이스홀더 자동 대체(exit code 5).
- **`marketplace-coupang` / `marketplace-naver`** — 쿠팡 + 네이버 스마트스토어 + 11번가/G마켓/옥션/티몬/위메프 채널별 정책·검색 키워드·금지문구·우수상품 기준 적용.
- **`product-photo-brief`** — 상품 사진 1-14장 분석 → ProductDNA(physical/positioning/palette) 추출 → 13섹션별 사용 가능 컷 매핑 → 부족한 컷 우선순위별 추가 촬영 브리프 자동 생성.
- 마켓플레이스 카운트 17 → **18 플러그인**, 89 → **94 스킬**.

### Added

- `moai-commerce/.claude-plugin/plugin.json` — 신규 플러그인 매니페스트.
- `moai-commerce/README.md` — 5개 스킬 카탈로그 + 표준 워크플로우 + 13섹션 구조 표.
- `moai-commerce/skills/detail-page-copy/SKILL.md` — 13섹션 카피 + ai-slop 체이닝 스킬.
- `moai-commerce/skills/detail-page-copy/references/13-sections.md` — 섹션별 카피 가이드 (헤드라인 길이·금지 표현·예시 포함).
- `moai-commerce/skills/detail-page-copy/references/category-briefs.md` — 10개 카테고리 어조·키워드·금지 표현표.
- `moai-commerce/skills/detail-page-copy/tests/test-cases.yaml` — happy/edge/failure 3건.
- `moai-commerce/skills/detail-page-image/SKILL.md` — 이미지 프롬프트 + Pillow 합성 워크플로우 스킬.
- `moai-commerce/skills/detail-page-image/scripts/compose.py` — 13섹션 → 1080×12720 세로 합성 (Pillow 단일 의존성).
- `moai-commerce/skills/detail-page-image/scripts/slice_bundle.py` — 큰 번들 PNG → Y좌표 슬라이싱.
- `moai-commerce/skills/detail-page-image/scripts/README.md` — 스크립트 사용법.
- `moai-commerce/skills/detail-page-image/references/sections-spec.md` — 13섹션 높이 스펙 표 + 마켓별 권장 크기 비교.
- `moai-commerce/skills/detail-page-image/references/image-prompts.md` — 섹션별 비주얼 언어 + nano-banana 프롬프트 패턴.
- `moai-commerce/skills/detail-page-image/tests/test-cases.yaml` — happy/edge/failure 3건.
- `moai-commerce/skills/marketplace-coupang/SKILL.md` — 쿠팡 정책·SEO 가이드 스킬.
- `moai-commerce/skills/marketplace-coupang/references/coupang-guidelines.md` — 이미지 규격·금지문구·우수상품 기준·로켓배송 vs 판매자배송·정산.
- `moai-commerce/skills/marketplace-coupang/tests/test-cases.yaml` — happy/edge/failure 3건.
- `moai-commerce/skills/marketplace-naver/SKILL.md` — 네이버 스마트스토어 + 오픈마켓 통합 가이드 스킬.
- `moai-commerce/skills/marketplace-naver/references/naver-smartstore.md` — 스마트스토어 SEO·톡톡 운영·후기 정책.
- `moai-commerce/skills/marketplace-naver/references/openmarket-common.md` — 11번가/G마켓/옥션/티몬/위메프 채널별 정책 비교.
- `moai-commerce/skills/marketplace-naver/tests/test-cases.yaml` — happy/edge/failure 3건.
- `moai-commerce/skills/product-photo-brief/SKILL.md` — 사진 분석 + 추가 촬영 브리프 스킬.
- `moai-commerce/skills/product-photo-brief/references/photo-checklist.md` — 13섹션 컷 우선순위 + 카테고리별 필수 컷.
- `moai-commerce/skills/product-photo-brief/tests/test-cases.yaml` — happy/edge/failure 3건.

### Changed

- `.claude-plugin/marketplace.json` — `metadata.version` 1.6.0 → 1.7.0, `metadata.description` "17 플러그인 86 스킬" → "18 플러그인 94 스킬", `plugins[]` 배열에 `moai-commerce` 항목 추가.
- 모든 `<plugin>/.claude-plugin/plugin.json` (21개) — `version` 1.6.0 → 1.7.0 일괄 동기화.
- `README.md` (루트) — Version 배지 1.6.0→1.7.0, Plugins 17→18, Skills 85→94, v1.7.0 하이라이트 섹션 신설, 카탈로그 테이블에 `moai-commerce` 행 추가, "총 산출물" 표 갱신.
- `CHANGELOG.md` 버전 통일 원칙 — 18 → **19개 지점** (plugin.json 17 → 18로 확장).

### Migration

- 사용자 측 캐시 갱신: Claude Cowork에서 `/plugin marketplace update cowork-plugins` 실행 후 `moai-commerce` 활성화.
- `detail-page-image` 스킬 사용 시: `pip install Pillow` (또는 `uv pip install Pillow`) 한 번 실행 필요. 다른 의존성 없음.
- 기존 워크플로우 영향 없음. Breaking change 없음.

## [1.6.0] - 2026-05-01

MINOR. **`skill-forge` → `skill-builder` 이름 변경 + `skill-tester` self-contained 화 + `moai-office`에 `pdf-writer` 신규 스킬 추가**가 핵심입니다. PDF 생성 시 한·중·일·영 다국어 글리프 깨짐 문제를 PyMuPDF + Noto Sans CJK 자동 다운로드 조합으로 근본 해결합니다.

### Highlights

- **`skill-forge` → `skill-builder` 이름 변경 (Breaking for direct skill-name references)** — 의미 불명확한 forge 어휘를 표준 builder로 전환. 별칭은 유지되지 않으며 모든 트리거·문서 참조가 `skill-builder`로 즉시 대체되었습니다. 외부 사용자가 `skill-forge`를 슬래시 커맨드로 직접 호출하던 경우 `skill-builder`로 변경 필요.
- **`skill-tester` 단독 self-contained 화** — 4차원 스코어링 루브릭(Correctness 30 / Completeness 25 / Clarity 25 / Efficiency 20)과 체인 검증 프로토콜을 `skill-tester` SKILL.md 본문에 직접 흡수. 이제 `skill-tester` 한 번 로드로 모든 평가 기준이 즉시 가용 — single source of truth 선언.
- **`moai-office:pdf-writer` 신규 스킬** — PyMuPDF + Noto Sans CJK(KR 변형) 조합으로 한·중·일·영 다국어 PDF를 깨짐 없이 생성. Markdown / 구조화 JSON / HTML / 일반 텍스트 4종 입력 지원, A4 규격 + 서브셋 임베딩. 폰트 64MB는 저장소에 포함하지 않고 최초 실행 시 `scripts/download_fonts.py`가 `notofonts/noto-cjk` 공식 저장소에서 자동 다운로드(SIL OFL 1.1).

### Added

- `moai-core/skills/skill-builder/SKILL.md` — `skill-forge`에서 이름 변경된 6-Phase 생성 스킬. 트리거 키워드 `skill-builder`, `harness 워크플로우` 추가.
- `moai-core/skills/skill-tester/SKILL.md` § 스코어링 루브릭 (4차원 anchor 점수표, Tier별 통과 기준, anti-pattern audit 체크리스트) + § Mode 3 체인 테스트 (Chain Definition Format, 4가지 Test Design Rule, Known Chains 매핑) 본문 직접 포함.
- `moai-office/skills/pdf-writer/SKILL.md` — 한·중·일·영 다국어 PDF 생성 스킬. 트리거 키워드: `한글 PDF`, `한국어 PDF`, `일본어 PDF`, `중국어 PDF`, `다국어 PDF`, `CJK PDF`, `Markdown PDF`, `PyMuPDF`, `Noto Sans CJK` 등 13종.
- `moai-office/skills/pdf-writer/scripts/download_fonts.py` — 표준 라이브러리만 사용하는 폰트 자동 다운로드 스크립트. `--check` / 기본 / `--force` 3가지 모드, OTF 매직바이트 무결성 검증.
- `moai-office/skills/pdf-writer/tests/test-cases.yaml` — 5건 테스트 케이스(happy path / JSON+표 / 한영 혼용 / 일반 텍스트 / **한·중·일·영 4언어 혼용**).
- `moai-office/skills/pdf-writer/assets/fonts/{LICENSE.txt, README.md, .gitignore}` — SIL OFL 1.1 라이선스 전문 + 출처·갱신 절차 문서화 + .otf/.ttf/.ttc 제외 규칙.

### Changed

- 18지점 버전 동시 bump: `marketplace.json` × 1 + `plugin.json` × 17 모두 1.5.1 → **1.6.0**.
- `moai-core/skills/skill-forge/` 디렉토리 삭제, `moai-core/skills/skill-builder/`로 대체.
- `docs-site/content/releases/v1.5.md`, `docs-site/content/plugins/moai-core.md`, `docs-site/content/plugins/_index.md` — `skill-forge` → `skill-builder` 표기 일괄 갱신.
- `README.md` — Skills 배지 73 → **85** (skill-builder rename + pdf-writer 추가 반영), v1.6.0 하이라이트 섹션 갱신.
- `.claude-plugin/marketplace.json` — `moai-office` description에 PDF 추가.
- `moai-office/README.md` — 헤더 설명 갱신(+PDF), 스킬 테이블에 `pdf-writer` 행 추가, 의존성 표에 PyMuPDF + Noto Sans CJK 추가.

### Removed

- `moai-core/skills/skill-forge/` 전체 (디렉토리 rename으로 대체).

### Migration

- `skill-forge`를 직접 호출하던 사용자/에이전트 → `skill-builder`로 변경 필요.
- 외부 사용자는 `/plugin marketplace update cowork-plugins` 후 플러그인 상세 재진입.
- `pdf-writer` 최초 사용 시 64MB(Noto Sans CJK 4 weight) 자동 다운로드가 1회 발생합니다. 네트워크 미연결 환경은 사전에 `python3 moai-office/skills/pdf-writer/scripts/download_fonts.py` 수동 실행으로 캐싱 가능.

## [1.5.1] - 2026-04-23

PATCH 릴리스. **저장소 위생 강화 + 한국어 문서 사이트 정식 안내**가 핵심입니다. 스킬·플러그인 수 변경 없음 (73 / 17 그대로), Breaking change 없음.

### Highlights

- **한국어 문서 사이트 [`cowork.mo.ai.kr`](https://cowork.mo.ai.kr/) 정식 오픈 안내** — Hugo + Geekdoc로 구축된 한국어 문서 사이트가 v1.5.0 코드와 함께 배포되어 정식 운영 중. 루트 README에 배지·하이라이트 링크를 추가했습니다. Cookbook 28편(블로그 파이프라인, 사업계획서, 계약서 검토, IR 덱, 리포트 자동화, 스킬 체이닝, 트랙별 가이드 등) + Cowork 입문/FAQ/용어집 수록.
- **저장소 위생 강화 (CRITICAL)** — `.gitignore`에 maintainer workspace 차단 블록을 추가했습니다. 정비자(maintainer)의 개인 작업 환경(`CLAUDE.md`, `CLAUDE.local.md`, `.mcp.json`, `.claude/`, `.moai/`)이 의도치 않게 공개 마켓플레이스에 유출되는 사고를 원천 차단합니다. 특히 `CLAUDE.local.md`에는 정비자 이메일과 GitHub Release 자동화 스크립트가 포함되어 있어 단 한 번의 `git add -A` 사고로 유출될 수 있었습니다.

### Changed

- `README.md` — Version 배지 1.5.0 → 1.5.1, 신규 `Docs` 배지(`cowork.mo.ai.kr`) 추가, v1.5.1 하이라이트 섹션 신설.
- `.gitignore` — 최하단에 "Maintainer Workspace (NOT distributed)" 블록 추가 (5개 패턴: `CLAUDE.md`, `CLAUDE.local.md`, `.mcp.json`, `.claude/`, `.moai/`).
- 18지점 버전 동시 bump: `marketplace.json` × 1 + `plugin.json` × 17 모두 1.5.0 → **1.5.1**.

### Fixed

- `git status`에 영구 노출되던 untracked 4건(`.claude/`, `.moai/`, `CLAUDE.md`, `.mcp.json`)을 ignore 처리하여 워크플로우 노이즈 제거.
- `.gitignore`에 `CLAUDE.local.md` 패턴 누락으로 인한 잠재적 개인정보 유출 위험 해소.

### Removed

해당 없음.

### Migration

- 기존 v1.5.0 사용자는 별도 마이그레이션 불필요.
- 사용자 측 캐시 갱신: `/plugin marketplace update cowork-plugins` 후 플러그인 상세 재진입.
- 본 저장소를 fork·clone하여 기여하는 분은 `git pull` 후 워킹 트리의 `.claude/`·`.moai/`·`CLAUDE.md`·`.mcp.json`·`CLAUDE.local.md`가 자동으로 ignore됩니다(이미 commit된 적 없으므로 손실 없음).

## [1.5.0] - 2026-04-21

공식 MINOR 릴리스. **moai-business 플러그인에 소상공인·창업자 실무 지원 스킬 2종을 추가**하여 총 스킬 개수가 71 → 73으로 확장됩니다. 두 스킬 모두 Category A(`user-invocable: true`)로 슬래시 명령 자동완성을 지원하고, 사용자 언어의 트리거가 풍부해 자연어로도 자동 호출됩니다.

### Highlights

- **소상공인365 상권분석 자동화** — `bigdata.sbiz.or.kr` PDF 한 장을 첨부하면 4문 인터뷰 후 창업 타당성 100점 평가 + 9섹션 DOCX 보고서를 자동 생성합니다.
- **정부지원사업 통합 도우미** — K-Startup, BIZINFO, 중기부, 창진원, 문체부, 농식품부 등 주요 공고를 한 번에 탐색하고 사업계획서 초안까지 작성합니다.
- **Anthropic 공식 스킬 우선순위 반영** — 두 스킬 모두 DOCX/XLSX 생성 시 `anthropic-skills:docx` · `anthropic-skills:xlsx` 우선, AI 슬롭 검수도 `anthropic-skills:ai-slop-reviewer` 우선 정책을 내장했습니다.

### Added

- **`moai-business/skills/sbiz365-analyst/`** 신규 스킬 (Category A) — 소상공인365 PDF 기반 상권 트렌드 분석 + 창업 타당성 종합 보고서.
  - Step 0-5 워크플로우: PDF 확인 → 4문 AskUserQuestion(업종·목적·예산·중점) → PDF 데이터 추출 → 5대 분석(유동인구·매출·경쟁·입지·타당성) → 9섹션 DOCX → AI 슬롭 검수.
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

공식 MINOR 릴리스. v1.1.0-v1.1.3의 점진적 변경을 안정 버전으로 집약하여 배포.

### Highlights

- **신규 플러그인 `moai-media`** — AI 미디어 스튜디오 (이미지·영상·음성 통합)
- **Google Nano Banana 공식 전환** — Imagen 4 → Gemini 3 Image Preview (Pro + 2 체제)
- **영상 단일화** — 숏폼·립싱크 커버 (이후 Higgsfield MCP로 통합)
- **음성은 ElevenLabs 공식 MCP** — TTS, 32개 언어 더빙, ConvAI
- **전 저장소 버전 통일 88 지점** → **1.2.0**

### Added

- 플러그인 `moai-media` (5 스킬)
  - [`nano-banana`](moai-media/skills/nano-banana/SKILL.md): Google Gemini 3 Image Preview 공식 2종 (`gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`)
  - [`ideogram`](moai-media/skills/ideogram/SKILL.md): Ideogram 3.0 한국어 타이포
  - [`kling`](moai-media/skills/kling/SKILL.md): Kling 3.0 숏폼 영상 (립싱크·다국어)
  - [`elevenlabs`](moai-media/skills/elevenlabs/SKILL.md): ElevenLabs 공식 MCP (TTS·음성복제·더빙·ConvAI)
- 번들 MCP 서버 (`moai-media/.mcp.json`)
  - `elevenlabs` (local stdio via `uvx elevenlabs-mcp`)
- API 키 통합 지원
  - `GEMINI_API_KEY` (nano-banana 전용 + 레거시 `NANO_BANANA_API_KEY` 호환)
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
- v1.0.x 잔존 로컬 태그 (v1.1.0-v1.3.0) — marketplace 버전 체계와 불일치하여 정리

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
  - 결과: 이미지는 `nano-banana` (Gemini) / `ideogram`, 영상은 `kling` 단독
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
- 숏폼·릴스·쇼츠: Kling 영상 모델 (이후 Higgsfield MCP로 통합)
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
  - [`moai-media/skills/kling/`](moai-media/skills/kling/SKILL.md): Kling 3.0 (숏폼 영상, 다국어 립싱크)
  - [`moai-media/skills/elevenlabs/`](moai-media/skills/elevenlabs/SKILL.md): ElevenLabs 공식 MCP (TTS, 음성복제, 32개 언어 더빙, ConvAI)
- **MCP 서버 자동 등록** — `moai-media/.mcp.json`에 사전 구성
  - `elevenlabs` (local stdio MCP via `uvx elevenlabs-mcp`, `ELEVENLABS_API_KEY` 주입)
- **API 키 신규 지원**: `ELEVENLABS_API_KEY` (기존 `NANO_BANANA_API_KEY` 유지)
- **4K 이미지 해상도** 지원 (`image_size="4K"`, Nano Banana Ultra 전용)
- **14종 화면비 지원** (1:1부터 21:9까지, Gemini 3 Image Preview 기본 스펙)
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

---

[이전 버전 없음 — v1.0.0이 최초 공개 릴리스입니다.]
