# 버전 업데이트 핸드오프

## 개요

docs-site의 버전 정보는 이제 **Git 태그를 단일 소스**로 관리합니다. 모든 버전 참조가 `site.Params.version`을 사용하도록 통합되었습니다.

## 자동화 현황

### ✅ 자동 관리됨

| 위치 | 소스 | 업데이트 방법 |
|---|---|---|
| `hugo.toml` `params.version` | Git 태그 | GitHub Actions 자동 업데이트 |
| `hugo.toml` `releaseDate` | 현재 날짜 | GitHub Actions 자동 업데이트 |
| `site-header.html` 헤더 버전 | `site.Params.version` | 자동 참조 (하드코딩 제거됨) |
| `_index.md` eyebrow | `site.Params.version` | 자동 참조 (하드코딩 제거됨) |
| `_index.md` 최신 릴리스 | `site.Params.version` | 자동 참조 (하드코딩 제거됨) |

### ⚠️ 수동 관리 필요

| 위치 | 관리 방법 |
|---|---|
| Git 태그 (`vX.Y.Z`) | `git tag vX.Y.Z && git push origin vX.Y.Z` |
| CHANGELOG.md | 릴리스 시 수동 업데이트 |
| `_index.md` 타임라인 | 최신 2개 릴리스만 표시하도록 수동 유지 |

---

## 워크플로우: 자동 업데이트

### 트리거 조건

다음 경로에서 변경이 있으면 자동 실행됩니다:
- `docs-site/**`
- `CHANGELOG.md`

또는 GitHub Actions UI에서 **수동 실행** 가능합니다.

### 실행 단계

1. **최신 Git 태그 추출**: `git describe --tags --abbrev=0`
2. **CHANGELOG.md 검증**: Git 태그와 CHANGELOG 버전 일치 확인
3. **hugo.toml 업데이트**: `version`과 `releaseDate` 자동 갱신
4. **변경사항 커밋**: 변경 있으면 자동 커밋/푸시

### 확인 방법

```bash
# 1. 최신 태그 확인
git describe --tags --abbrev=0
# 출력: v2.2.0

# 2. CHANGELOG.md 최신 버전 확인
grep -m1 "^## \[" CHANGELOG.md
# 출력: ## [2.2.0] - 2026-05-09

# 3. hugo.toml 버전 확인
grep "^version = " docs-site/hugo.toml
# 출력: version = "2.2.0"

# 4. 로컬에서 빌드 테스트
cd docs-site && hugo server
# 브라우저에서 헤더 버전 확인
```

---

## 수동 업데이트 절차 (자동화 실패 시)

### 1. Git 태그 생성

```bash
# 1. 버전 bump 완료 후
git tag -a vX.Y.Z -m "vX.Y.Z — 릴리스 요약"
git push origin vX.Y.Z
```

### 2. CHANGELOG.md 업데이트

```bash
# CHANGELOG.md에 섹션 추가
## [X.Y.Z] - YYYY-MM-DD

### Added
- 신규 스킬/기능

### Changed
- 기존 스킬 변경

### Fixed
- 버그 수정
```

### 3. docs-site 버전 동기화

```bash
# 3-1. hugo.toml 업데이트
VERSION="X.Y.Z"
DATE=$(date +%Y-%m-%d)
sed -i "s/^version = .*/version = \"$VERSION\"/" docs-site/hugo.toml
sed -i "s/releaseDate = .*/releaseDate = \"$DATE\"/" docs-site/hugo.toml

# 3-2. 검증
grep -A 1 "^\[params\]" docs-site/hugo.toml | grep version
```

### 4. 커밋 & 푸시

```bash
git add docs-site/hugo.toml CHANGELOG.md
git commit -m "chore(docs): vX.Y.Z — 버전 동기화"
git push
```

---

## 문제 해결 가이드

### 문제: 헤더 버전이 구버전으로 나옴

**원인**: 브라우저 캐시 또는 CDN 지연 반영

**해결**:
1. 하드 리프레시: `Ctrl+Shift+R` (Win) / `Cmd+Shift+R` (Mac)
2. 캐시 클리어 후 재접속
3. Vercel 배포 확인: `vercel list`

```bash
# Vercel 최근 배포 확인
vercel list docs-site
```

### 문제: GitHub Actions가 실행되지 않음

**원인**: 워크플로우 경로 조건 불일치

**해결**:
```bash
# 수동 실행
gh workflow run docs-site-sync.yml
```

### 문제: 버전 갱신 후 404 발생

**원인**: hugo.toml 문법 오류

**해결**:
```bash
# 문법 검증
hugo config
# 빌드 테스트
hugo --gc --minify
```

### 문제: Git 태그와 CHANGELOG 버전 불일치

**원인**: CHANGELOG.md 업데이트 누락

**해결**:
1. CHANGELOG.md 최신 섹션 확인
2. Git 태그와 버전 일치하도록 수정
3. `git tag -f vX.Y.Z`로 태그 강제 업데이트 (주의 필요)

---

## 체크리스트: 릴리스 배포 전

```
[ ] Git 태그 생성: git tag vX.Y.Z && git push origin vX.Y.Z
[ ] CHANGELOG.md 업데이트: ## [X.Y.Z] 섹션 추가
[ ] marketplace.json 버전 bump: metadata.version
[ ] 모든 plugin.json 버전 bump: version
[ ] 모든 SKILL.md frontmatter 버전 bump: version: X.Y.Z
[ ] docs-site/hugo.toml 자동 업데이트 확인 (GitHub Actions)
[ ] 로컬 빌드 테스트: hugo server
[ ] 헤더 버전 확인: 브라우저에서 docs-site 접속
[ ] Vercel 배포 확인: vercel list
[ ] 운영 환경 확인: curl https://cowork.mo.ai.kr
```

---

## 다음 세션 시작 가이드

이 문서를 읽고 다음 단계를 진행하세요:

1. **버전 확인**: `git describe --tags --abbrev=0`
2. **자동화 확인**: GitHub Actions가 hugo.toml을 업데이트했는지 확인
3. **로컬 테스트**: `cd docs-site && hugo server`
4. **배포**: GitHub Actions가 자동으로 배포됨

---

## 참고: 파일 구조

```
docs-site/
├── hugo.toml (params.version, params.releaseDate) ← GitHub Actions 관리
├── layouts/
│   └── partials/
│       └── site-header.html ({{ site.Params.version }}) ← 자동 참조
├── content/
│   ├── _index.md ({{ site.Params.version }}) ← 자동 참조
│   ├── releases/
│   │   ├── v2.2.md
│   │   └── v2.1.md
│   └── cookbook/
└── vercel.json (빌드 설정)
```

---

마지막 업데이트: 2026-05-11 (v2.2.0)
