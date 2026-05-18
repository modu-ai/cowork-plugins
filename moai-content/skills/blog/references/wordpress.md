# WordPress SEO 최적화 가이드

> moai-content | blog 참조 가이드 | 2026 기준

## 개요

WordPress는 전 세계 웹사이트의 약 43%를 구동하는 CMS로, 플러그인 생태계를 통해 강력한 SEO 환경을 구축할 수 있습니다. 이 가이드는 한국 기업 블로그 운영에 최적화된 설정을 안내합니다.

---

## 1. SEO 플러그인 선택

### Yoast SEO vs RankMath 비교

| 기능 | Yoast SEO | RankMath |
|------|-----------|----------|
| 무료 기능 | 기본 SEO | 다중 키워드, 스키마 |
| 사용 편의성 | 초보자 친화적 | 중급자 이상 권장 |
| 구글 서치 콘솔 연동 | 유료 | 무료 |
| AI 기능 | 유료 | 무료 포함 |
| 한국어 지원 | 양호 | 양호 |

**권장**: 소규모 블로그 → Yoast SEO Free, 성장 단계 → RankMath Pro

---

## 2. 필수 플러그인 구성

### 성능·SEO 스택

- [ ] **SEO**: RankMath 또는 Yoast SEO
- [ ] **캐싱**: WP Super Cache 또는 W3 Total Cache
- [ ] **이미지 최적화**: Imagify 또는 ShortPixel
- [ ] **보안**: Wordfence Security (한국 표적 공격 방어)
- [ ] **백업**: UpdraftPlus (주 1회 자동 백업)
- [ ] **소셜 공유**: Social Warfare 또는 Monarch

---

## 3. SEO 설정 체크리스트

### 기본 SEO 설정

- [ ] 퍼머링크 구조: `/%postname%/` (포스트 이름 방식)
- [ ] XML 사이트맵 생성 및 구글 서치 콘솔 제출
- [ ] robots.txt 설정 (wp-admin, wp-login 차단)
- [ ] SSL 인증서 설치 및 HTTPS 리다이렉트
- [ ] 구글 애널리틱스 4 연동

### 글별 SEO 작성

- [ ] 포커스 키워드 설정 (RankMath: 5개, Yoast: 1개 무료)
- [ ] SEO 제목 60자 이내
- [ ] 메타 설명 150-160자
- [ ] 이미지 alt 텍스트 키워드 포함
- [ ] 내부 링크 최소 3개

---

## 4. 페이지 속도 최적화

구글은 페이지 속도를 순위 요인으로 사용합니다.

### Core Web Vitals 목표

| 지표 | 목표 | 의미 |
|------|------|------|
| LCP | 2.5초 미만 | 최대 콘텐츠 로딩 시간 |
| FID/INP | 200ms 미만 | 사용자 입력 반응 시간 |
| CLS | 0.1 미만 | 레이아웃 이동 안정성 |

### 속도 개선 액션

1. 이미지 WebP 변환 + 지연 로딩 설정
2. CSS/JS 파일 최소화 (Autoptimize 플러그인)
3. CDN 적용 (Cloudflare 무료 플랜 권장)
4. 한국 호스팅 사용 시 국내 서버 위치 확인

---

## 5. 콘텐츠 최적화 체크리스트

- [ ] H1 태그는 글당 1개만 사용
- [ ] 이미지 파일명 영문 키워드로 저장 (seo-guide.jpg)
- [ ] 외부 링크는 신뢰할 수 있는 출처로만 연결
- [ ] 발행 전 모바일 미리보기 확인
- [ ] 목차(Table of Contents) 플러그인으로 긴 글 구조화
