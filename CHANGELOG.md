# Changelog

모든 주목할 만한 변경사항은 이 파일에 기록됩니다.

형식: [Keep a Changelog 1.1.0](https://keepachangelog.com/ko/1.1.0/) · 버저닝: [Semantic Versioning 2.0.0](https://semver.org/lang/ko/)

## 버전 통일 원칙 (HARD)

아래 130개 지점의 버전 표기는 **항상 완전히 동일**합니다 (v2.0.0부터 SKILL.md frontmatter `version:` 복구):
- `.claude-plugin/marketplace.json` (`metadata.version`) × 1
- `<plugin>/.claude-plugin/plugin.json` (`version`) × 21
- `<plugin>/skills/<skill>/SKILL.md` (`version:` frontmatter) × 108 (v2.0.0+ 정책)

상세 정책: `CLAUDE.local.md` § 1 참조.

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
- moai-content/README.md: 10개 → **11개** 스킬 표기, html-report 행 추가, 텍스트~영상~보고서 표현 갱신
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
  - 카테고리: A 번역투(~를 통해/~에 있어서/이중 피동), B 영어 인용 과다, C 구조 패턴(이모지·콜론 부제·연결어미 쉼표), D AI 관용구(결론적으로/시사하는 바·hype 어휘·결말 공식), E 리듬 균일성, F 한자어 -성/-적/-화 밀도, G hedging, H 문두 접속사 남발, I 형식명사 과다, J 시각 장식 남용
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
- **NOTICE.md** — `.claude/rules/moai/NOTICE.md`에 NomaDamas/k-skill MIT attribution 섹션 추가. 6개 포팅 스킬과 원 저작자 링크 보존.
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
- 통합 어트리뷰션: `.claude/rules/moai/NOTICE.md` § NomaDamas k-skill (MIT)
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
- **`moai-media/README.md` 전면 재작성** — 5스킬 카탈로그(kling/ideogram/elevenlabs/nano-banana/fal-gateway) → **7스킬 카탈로그**(nano-banana/image-gen/video-gen/audio-gen/speech-video/character-mgmt/fal-gateway), 마이그레이션 안내 추가.
- **`moai-core/skills/project/SKILL.md`·`init-protocol.md`** — 미디어 스킬 매핑·API 키 안내를 7스킬 기준으로 갱신, kling→video-gen·elevenlabs→audio-gen 워크플로우 매핑.
- **`moai-commerce/skills/{detail-page-image,live-commerce}/SKILL.md`** — `moai-media:ideogram`/`moai-media:kling` 호출 안내를 `nano-banana`(한국어 타이포 SOTA)·`video-gen`·`fal-gateway`로 재정렬.
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
- **`product-photo-brief`** — 상품 사진 1~14장 분석 → ProductDNA(physical/positioning/palette) 추출 → 13섹션별 사용 가능 컷 매핑 → 부족한 컷 우선순위별 추가 촬영 브리프 자동 생성.
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

---

[이전 버전 없음 — v1.0.0이 최초 공개 릴리스입니다.]
