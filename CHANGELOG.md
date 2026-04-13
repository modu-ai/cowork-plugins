# Changelog

모든 주목할 만한 변경사항은 이 파일에 기록됩니다.

형식: [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) · 버저닝: [Semantic Versioning](https://semver.org/lang/ko/)

버전 통일 원칙:
- `marketplace.json` (마켓플레이스 루트)
- `moai-core/.claude-plugin/plugin.json` (코어 플러그인)
- `moai-core/skills/moai/SKILL.md` (코어 스킬 metadata.version 및 본문 뱃지)

위 3곳의 버전은 항상 동일하게 유지합니다.

## [1.0.3] - 2026-04-14

### Fixed
- `/moai` 슬래시 자동완성이 Claude Code에 노출되지 않던 문제 수정
  - `moai-core/skills/moai/SKILL.md` frontmatter에 `user-invocable: true` 추가
  - 비표준 `keywords` 필드를 표준 `metadata.tags`로 이전
  - `metadata.version`, `status`, `updated` 메타데이터 추가

### Changed
- 버전 통일: marketplace / plugin.json / SKILL.md 모두 `1.0.3`
- 스킬 본문 뱃지 `v1.0.0` → `v1.0.3`

## [1.0.2] - 2026-04-12

### Added
- `feedback` 스킬: 버그/기능 요청 GitHub Issues 자동 등록
- pptx-designer NotebookLM 스타일 프롬프트 및 인포그래픽 선택 옵션

### Changed
- 퍼블릭 공개용 README 업데이트 (뱃지, 목차, 기여/문의 섹션)
- 스킬 테이블에 한글명 컬럼 추가 (전 플러그인 65개 스킬)

### Fixed
- API 키 vs Cowork 커넥터 혼동 방지 규칙 강화
- API 키 4개로 정리 (DART/KOSIS/KCI 통합, 네이버/구글 제거)
- 안내 목록 외 서비스(네이버 API 등) 안내 금지

## [1.0.1] - 2026-04-11

### Changed
- `init` 모든 질문을 `AskUserQuestion` 도구 사용으로 통일

## [1.0.0] - 2026-04-08

### Added
- 초기 마켓플레이스 공개 (16개 플러그인, 64개 스킬)
- `moai-core` 도메인 AI 라우터 + 자가학습 엔진
- 도메인별 플러그인: business, marketing, legal, finance, hr, content, operations, education, lifestyle, product, support, office, career, data, research
