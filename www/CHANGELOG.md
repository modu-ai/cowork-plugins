# 모두의 코워크 문서 사이트 — Changelog

## v4.0.2 (2026-07-16) — 로고 전면 교체 + 무채색 테마 완성

### Changed

- **로고 전면 교체** — 코랄 계열 기존 헤더 로고(`logo-1line-tight.png`) 제거. 헤더를 **모아이 마스코트 아이콘(`moai-logo-3`) + "모두의 코워크" 텍스트**(HTML/Pretendard) 구성으로 재구성. 파비콘도 모아이 마스코트로 교체. 홈 hero의 코랄 크리처(`logo-creature.png`) 제거.
- **무채색 테마 정제** — neutral 스케일을 순수 무채색(zip achromatic, hue 0%)으로 정제(warm 뉘앙스 `#1a1f1d`/`#0e1513`/`#09110f` → 순수 무채색). `--color-ink #060606`, `--color-bg #f4f4f4`, 시그니처 그라디언트 끝 `#060606`. **모아이 그린(`#3d7d5f`)은 CTA·링크·active 포인트로 유지**(zip "무채색 베이스 + 그린 포인트" 체계).
- 참고용 `assets/css/moai-brand.scss` 토큰 동기화(primary-hover/active, neutral).

### Removed

- 기존 코랄 헤더 로고(`logo-1line-tight.png`) 참조.
- 홈 hero 크리처 이미지(`logo-creature.png`).

## v4.0.1 (2026-07-16) — 디자인 시스템 모아이 그린 복귀

### Changed

- **디자인 시스템: Claude 코랄 → 모아이 그린(#3d7d5f) 전면 전환.** 2026-06-23 Claude warm editorial(코랄) 결정을 뒤집고, `ai-design-system.zip`(Claude Design 핸드오프) 기준 모아이 그린 브랜드로 복귀.
  - 운영 CSS(`www/static/moai-brand.css`) 하드코딩 코랄 `rgba(204,120,92,*)` 47건 → 그린 `rgba(61,125,95,*)`로 일괄 전환. `:root` 토큰은 이미 그린 기반이었음.
  - `design-system/` 카탈로그 13종: 코랄→그린 + warm cream 배경→zip 무채색/잉크 톤 정리.
  - 홈(`content/_index.md`) 제품 카드 아이콘 4색(코랄/노랑/베이지) → 모아이 그린 명도 톤으로 통일(zip "한 화면 4종 이상 컬러 토큰 금지" 준수).
  - 참고용 `assets/css/moai-brand.scss` 토큰 동기화.

### Added

- **Pretendard self-host** — CDN(orioncactus/pretendard) 제거, 직접 설치(`www/static/fonts/Pretendard-*.otf`, 9 weights 100~900). `@font-face`로 운영 CSS에서 로드. 외부 의존도 제거.
- **마스코트 6종** — ai-design-system.zip 캐릭터(Thinking·Pointing·Searching·Teaching·Explaining·Coffee) 추가. `mascot.html` partial이 6종 variant 지원. 홈(explaining)/404(searching)/빈 결과(searching)/푸터(coffee)에 용도별 배치. 기존 3종(main/global/alt) 하위호환 유지.
- zip 에셋(로고 9종) `www/static/logos/` 추가.

### Removed

- Pretendard CDN `<link>` 제거(`layouts/partials/head/custom.html`).

### 결정 기록

2026-06-23 "Claude warm editorial(코랄)" 브랜드 결정 → 2026-07-16 ai-design-system.zip 핸드오프 도입으로 **모아이 그린 복귀**. 사유: zip 디자인 시스템이 FROZEN 규칙(단일 시그니처 청록 그라디언트, 무채색 배경, 마스코트 정서 앵커)으로 일관된 그린 브랜드를 요구.

## v4.0.0 (2026-07-07)

### Added

- **moai-story 플러그인 신설** — 작가·콘텐츠 비즈니스 도메인 전용 플러그인. 출판·웹툰·웹소설·시나리오·콘티·캐릭터·표지·프리비즈·IP 사업화 21개 스킬 + Higgsfield MCP 연동.
- [플러그인 카탈로그](./plugins/index.md)에 moai-story 섹션 추가.
- [cowork v4.0.0 마이그레이션 가이드](./plugins/migration.md) 신설.
- [Higgsfield MCP 설정 가이드](./plugins/higgsfield-setup.md) 신설.

### Changed

- cowork v3.0.0 → v4.0.0 (breaking): 출판(book-*) 스킬 8종이 moai-story로 이관. 스킬 수 179 → 171.
- 마켓플레이스 `metadata.version` 3.0.0 → 4.0.0 (catalog 단일 version 지점).

### Migration

기존 book-* 스킬 사용자는 `/plugin install story`로 moai-story를 설치하세요. 상세 절차는 마이그레이션 가이드를 참고.
