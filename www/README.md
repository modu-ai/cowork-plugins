# 모두의 코워크 — 한국어 문서 사이트

`claude.mo.ai.kr` — Claude의 4가지 제품(Chat · Cowork · Design · Code) 활용 완전 가이드. 10~60대 비개발자 입문자를 위한 한국어 학습 허브.

## 기술 스택

- **Hugo** v0.160.1 (extended)
- **테마**: [Geekdoc](https://github.com/thegeeklab/hugo-geekdoc) (Hugo Module)
- **폰트**: Pretendard(self-host, 9 weights — `static/fonts/`) + Goorm Sans Code(CDN)
- **디자인 시스템**: 모두의AI Design System — 모아이 그린(`#3d7d5f`) 시그니처 + 마스코트 6종. `ai-design-system.zip`(Claude Design 핸드오프) 기반. 운영 CSS = `static/moai-brand.css`(단일 진실 소스).
- **호스팅**: Vercel
- **도메인**: claude.mo.ai.kr

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
www/
├── hugo.toml             # 사이트 설정 (제목: 모두의 코워크, baseURL: claude.mo.ai.kr)
├── go.mod                # Hugo 모듈 (Geekdoc 테마)
├── vercel.json           # Vercel 빌드 설정
├── content/              # 마크다운 콘텐츠 (176+ 페이지)
│   ├── _index.md         # 홈
│   ├── getting-started/  # 시작하기 (5)
│   ├── guide/            # 4-트랙 가이드
│   │   ├── chat/         # Chat 트랙 — Claude Desktop App
│   │   ├── cowork/       # Cowork 트랙 — Claude Cowork
│   │   ├── design/       # Design 트랙 — Claude Design
│   │   └── code/         # Code 트랙 — Claude Code
│   ├── moai-agents/      # 18 AI 직원
│   ├── plugins/          # 플러그인 카탈로그
│   ├── cookbook/         # 쿡북 · 실전 트랙
│   ├── help/             # 도움말
│   ├── releases/         # 릴리스 노트
│   └── cli/              # CLI (개발자용)
├── data/
│   ├── menu/main.yaml    # 목차 SSOT (3축: 데스크탑·CLI·공통하단)
│   └── menu/extra.yaml   # 헤더/외부 링크
├── layouts/partials/     # 커스텀 헤더/푸터
├── assets/               # SCSS, 이미지
├── static/               # 정적 파일
└── themes/               # Geekdoc 테마
```

## 4트랙 구조

| 트랙 | 제품 | 공식 자료 기반 |
|------|------|----------------|
| **Chat** | Claude Desktop App | support.claude.com (KO + EN) |
| **Cowork** | Claude Cowork | support.claude.com/ko (핵심 15개 KO 문서) |
| **Design** | Claude Design | support.claude.com (핵심 3개 KO 문서) |
| **Code** | Claude Code | code.claude.com/docs (KO 일부) |

목차는 `data/menu/main.yaml`이 SSOT입니다. 3개 축(🖥️ 데스크탑 · ⌨️ CLI · 🧩 공통 하단)으로 구성되며, 데스크탑 축이 학습 난이도 순(Chat → Cowork → Design → Code)으로 정렬됩니다.

## Vercel 배포 절차

1. Vercel 콘솔에서 신규 프로젝트 생성 → `modu-ai/moai-cowork` 연결
2. **Root Directory**: `www`
3. **Framework Preset**: `Hugo` (자동 감지)
4. **Build Command**: `hugo --gc --minify` (vercel.json에서 자동 적용)
5. **Output Directory**: `public`
6. **Environment Variables**: vercel.json에서 자동 적용 (HUGO_VERSION=0.160.1)
7. 배포 후 **Domains**에서 `claude.mo.ai.kr` 추가, DNS CNAME 레코드 등록

## 콘텐츠 작성 규약

- 본문은 한국어 경어체
- 전문용어는 한국어(영문) 병기: 스킬(skill), 플러그인(plugin)
- 슬러그는 영문 케밥케이스 (`first-task`, `live-artifacts`)
- 페이지 하단에 `Sources` 섹션 필수 (외부 인용 시)
- AI 슬롭 검수: 본문 작성 후 `moai:ai-slop-reviewer` 통과 권장

## 라이선스

[Apache License 2.0](../LICENSE) — 상업적 사용·수정·재배포 자유. 산출물은 이용자 소유([LICENSE-OUTPUT.md](../LICENSE-OUTPUT.md)).
