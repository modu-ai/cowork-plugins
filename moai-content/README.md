# moai-content

크리에이티브 콘텐츠 플러그인 — 카드뉴스, **shadcn/ui 랜딩페이지**, **shadcn/ui 상세페이지**, 뉴스레터, 카피라이팅, 블로그, 소셜미디어, 미디어 프로덕션, **바른한글 맞춤법 검수** (v2.0.0), **한국어 AI 티 정밀 윤문 humanize-korean** (v2.1.0 신규).

10개 스킬로 텍스트부터 영상까지 콘텐츠 제작 전 과정을 커버합니다. v1.4.0부터 `landing-page`·`product-detail` 두 스킬이 **shadcn/ui + Tailwind CSS v4 + OKLCH 토큰**을 기본 스택으로 사용하고, 코드 생성 전 **소크라테스식 테마 인터뷰**(베이스 팔레트·컬러 모드·모서리 반경·효과)를 자동으로 실행합니다. **v2.0.0부터** `korean-spell-check`(부산대 AI연구실 + ㈜나라인포테크 공동 개발 **바른한글** 표면)으로 한국어 맞춤법·띄어쓰기를 최종 검수합니다 — `ai-slop-reviewer` 직후 체인 권장. **v2.1.0부터** `humanize-korean`([epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) MIT, ⭐937 Fast 모드 포팅)으로 10대 카테고리 × 40+ AI 티 패턴 SSOT를 정량 메트릭으로 정밀 윤문합니다 — 의미 100% 보존 가드(변경률 30/50%) + 자체검증 6항 + A/B/C/D 등급 자동 판정. Post-Bridge, Typefully, WordPress MCP 연동으로 멀티채널 발행을 자동화합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [card-news](./skills/card-news/) | AI 이미지 생성 기반 인스타 캐러셀 제작. 잡지 SOP, AI 글쓰기 방지 기법 | 4 | ✅ |
| [product-detail](./skills/product-detail/) | **shadcn/ui** 기반 전환율 극대화 상세페이지 빌더. 네이버/쿠팡/카카오 규격 + Next.js 자사몰 | 4 | ✅ |
| [landing-page](./skills/landing-page/) | **shadcn/ui** 기반 고전환율 랜딩 페이지. CTA 최적화, 소크라테스식 테마 인터뷰, Framer Motion | 7 | ✅ |
| [copywriting](./skills/copywriting/) | 마케팅 카피, 헤드라인, CTA, 광고 캠페인, 비주얼 스토리텔링 | 3 | ✅ |
| [newsletter](./skills/newsletter/) | 뉴스레터 기획~발행, 구독자 확보 전략, 오픈율 최적화 | 1 | ✅ |
| [media-production](./skills/media-production/) | Remotion 영상, 유튜브 프로덕션, 팟캐스트, 전자책 출판 | 9 | ✅ |
| [blog](./skills/blog/) | 네이버/티스토리/브런치/WordPress/Ghost 6개 플랫폼 최적화 포스팅 | 6 | ✅ |
| [social-media](./skills/social-media/) | 인스타/스레드/X/링크드인/유튜브쇼츠/카카오 7개 플랫폼 콘텐츠 | 7 | ✅ |
| [korean-spell-check](./skills/korean-spell-check/) | 바른한글(부산대) 한국어 맞춤법·띄어쓰기 최종 검수. ai-slop-reviewer 직후 체인 권장 (v2.0.0+) | 0 | ✅ |
| [humanize-korean](./skills/humanize-korean/) | **🆕 v2.1.0** — 한국어 AI 티 정밀 윤문 (10대 카테고리 × 40+ 패턴 SSOT, S1/S2/S3 심각도, A/B/C/D 등급, 변경률 30/50% 가드). [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) MIT ⭐937 Fast 모드 포팅 | 6 | ✅ |

## shadcn/ui 기본 스택 (v1.4.0 신규)

`landing-page`와 `product-detail` 스킬은 별도 지정이 없으면 다음 스택으로 산출합니다:

| 레이어 | 기본값 |
|--------|-------|
| 프레임워크 | Next.js 15 App Router + React 19 |
| 스타일 | Tailwind CSS v4 (CSS Variables 모드) |
| UI 컴포넌트 | **shadcn/ui** (Radix 기반) |
| 아이콘 | Lucide React |
| 애니메이션 | Framer Motion (선택 시) |
| 폰트 | Pretendard (KR) + Inter (EN) |
| 차트 | Recharts (선택 시) |

코드 생성 직전 `AskUserQuestion` 4문항 인터뷰 — (1) 베이스 팔레트(Neutral/Zinc/Stone/Slate) · (2) 컬러 모드(Light/Dark/System+Toggle/Auto) · (3) 모서리 반경(Sharp~Pill) · (4) 효과(Fade-up·Scroll Reveal·Parallax·Chart) — 를 실행합니다.

공용 레퍼런스: [`skills/landing-page/references/landing-page/shadcn-theme-interview.md`](./skills/landing-page/references/landing-page/shadcn-theme-interview.md)

## Cowork 커넥터

| 서비스 | 연결 | 용도 |
|--------|------|------|
| WordPress | Settings > Connectors > WordPress | 블로그 포스트 직접 발행/예약 |

네이버/티스토리/브런치/Ghost 등은 콘텐츠 생성까지만 지원합니다 (발행은 수동). 커넥터 설정 상세: [CONNECTORS.md](./CONNECTORS.md)

## 스크립트

| 파일 | 용도 |
|------|------|
| scripts/card-news/generate_image.py | AI 이미지 생성 (카드뉴스용) |

## 사용 예시

```
"AI로 돈 버는 법" 주제로 인스타 카드뉴스 10장 만들어줘
```

```
유튜브 채널 기획서 써줘. 개발자 취업 정보 채널, 구독자 10만 목표.
```

```
SaaS 제품 랜딩 페이지 만들어줘. 히어로 섹션부터 CTA까지.
```

## 설치

Settings > Plugins > cowork-plugins에서 `moai-content` 선택

## 오픈소스 및 참고자료

### MCP 서버
| 서버 | URL | 용도 |
|------|-----|------|
| WordPress | [mcp.wordpress.com](https://mcp.wordpress.com/mcp) | 블로그 발행 |
| Post-Bridge | [post-bridge.com](https://app.post-bridge.com/mcp) | 멀티플랫폼 발행 |
| Typefully | [typefully.com](https://api.typefully.com/mcp) | X/Twitter 스레드 |

### AI 이미지 생성
| 모델 | API | 문서 |
|------|-----|------|
| Nano Banana Pro | [ai.google.dev](https://ai.google.dev/gemini-api/docs/image-generation) | Imagen 4 고품질 |
| Nano Banana 2 | 동일 | Imagen 4 Fast (빠른 생성) |
| Nano Banana Ultra | 동일 | Imagen 4 Ultra (최고 품질) |

### 영상 제작
| 패키지 | URL | 용도 |
|--------|-----|------|
| [Remotion](https://www.remotion.dev/) | remotion.dev | React 기반 영상 프레임워크 |
| [Three.js](https://threejs.org/) | threejs.org | 3D 그래픽 |
| [ElevenLabs](https://elevenlabs.io/) | elevenlabs.io | AI 음성 합성 (TTS) |
