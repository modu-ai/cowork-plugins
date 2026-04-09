# moai-content

크리에이티브 콘텐츠 플러그인 — 카드뉴스, 랜딩페이지, 뉴스레터, 카피라이팅, 블로그, 소셜미디어, 미디어 프로덕션.

7개 스킬로 텍스트부터 영상까지 콘텐츠 제작 전 과정을 커버합니다. Agency 패턴(JSON 카피 계약, 디자인 시스템 스펙, 평가 체크리스트)이 적용된 landing-page 스킬을 포함합니다. Post-Bridge, Typefully, WordPress MCP 연동으로 멀티채널 발행을 자동화합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [card-news](./skills/card-news/) | AI 이미지 생성 기반 인스타 캐러셀 제작. 잡지 SOP, AI 글쓰기 방지 기법 | 4 | ✅ |
| [landing-page](./skills/landing-page/) | 고전환율 랜딩 페이지 설계. CTA 최적화, Agency 디자인 원칙 적용 | 6 | ✅ |
| [copywriting](./skills/copywriting/) | 마케팅 카피, 헤드라인, CTA, 광고 캠페인, 비주얼 스토리텔링 | 3 | ✅ |
| [newsletter](./skills/newsletter/) | 뉴스레터 기획~발행, 구독자 확보 전략, 오픈율 최적화 | 1 | ✅ |
| [media-production](./skills/media-production/) | Remotion 영상, 유튜브 프로덕션, 팟캐스트, 전자책 출판 | 9 | ✅ |
| [blog](./skills/blog/) | 네이버/티스토리/브런치/WordPress/Ghost 6개 플랫폼 최적화 포스팅 | 0 | ✅ |
| [social-media](./skills/social-media/) | 인스타/스레드/X/링크드인/유튜브쇼츠/카카오/네이버 7개 플랫폼 콘텐츠 | 0 | ✅ |

## MCP 커넥터

| 서버 | 용도 |
|------|------|
| post-bridge | 블로그/SNS 멀티채널 게시 자동화 |
| typefully | 트위터/X 스레드 예약 발행 |
| wordpress | WordPress REST API 직접 게시 |

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

Settings > Plugins > moai-cowork-plugins에서 `moai-content` 선택
