# Claude Cowork 한국어 문서 사이트

`cowork.mo.ai.kr` — Claude Cowork와 `cowork-plugins` 17종의 한국어 사용자 가이드, 베스트 프랙티스, 쿡북.

## 기술 스택

- **Hugo** v0.160.1 (extended)
- **테마**: [Geekdoc](https://github.com/thegeeklab/hugo-geekdoc) (Hugo Module)
- **호스팅**: Vercel
- **도메인**: cowork.mo.ai.kr

## 로컬 실행

```bash
# 의존성(테마 모듈) 다운로드
hugo mod get -u

# 개발 서버
hugo server -D

# 프로덕션 빌드
hugo --gc --minify
```

## 디렉터리

```
docs-site/
├── hugo.toml             # 사이트 설정
├── go.mod                # Hugo 모듈 (Geekdoc 테마)
├── vercel.json           # Vercel 빌드 설정
├── content/
│   ├── _index.md         # 홈
│   ├── about.md          # 소개
│   ├── cowork/           # Cowork 공식 한글 가이드 (13)
│   ├── plugins/          # 플러그인 카탈로그 (20)
│   └── cookbook/         # 베스트 프랙티스 · 쿡북 (17)
├── layouts/partials/     # 커스텀 헤더/푸터
├── assets/               # SCSS, 이미지
├── static/               # 정적 파일
└── data/                 # 메뉴 등 데이터
```

## Vercel 배포 절차

1. Vercel 콘솔에서 신규 프로젝트 생성 → `modu-ai/cowork-plugins` 연결
2. **Root Directory**: `docs-site`
3. **Framework Preset**: `Hugo` (자동 감지)
4. **Build Command**: `hugo --gc --minify` (vercel.json에서 자동 적용)
5. **Output Directory**: `public`
6. **Environment Variables**: vercel.json에서 자동 적용 (HUGO_VERSION=0.160.1)
7. 배포 후 **Domains**에서 `cowork.mo.ai.kr` 추가, DNS CNAME 레코드 등록

## 콘텐츠 작성 규약

- 본문은 한국어 경어체
- 전문용어는 한국어(영문) 병기: 스킬(skill), 플러그인(plugin)
- 슬러그는 영문 케밥케이스 (`first-task`, `moai-content`)
- 페이지 하단에 `Sources` 섹션 필수 (외부 인용 시)
- AI 슬롭 검수: 본문 작성 후 `moai:ai-slop-reviewer` 통과 권장

## 라이선스

MIT (cowork-plugins 저장소와 동일)
