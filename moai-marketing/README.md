# moai-marketing

마케팅 플러그인 — 네이버/카카오 SEO, **한국 3채널 + 글로벌 4채널 SNS 통합**(v2.3.0), 캠페인 기획, 이메일 시퀀스, 퍼포먼스 리포트, **광고 심리학 완전판**(v2.4.0).

[![버전](https://img.shields.io/badge/version-2.4.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-10-success)](#스킬)

> **v2.4.0 신규 2 + 강화 2** — `landing-page-conversion-audit`(랜딩 6섹션 진단 + CTR/CVR 분기 + 불안해소 문구 처방), `pixel-audit`(메타·구글 픽셀 + CAPI + Lookalike 씨앗 품질) + `campaign-planner`/`sns-content` 광고 심리학 완전판 통합(6 방아쇠·8 편향·PAS·후크 6종·채널별 심리 매트릭스)

국내 플랫폼(네이버 블로그, 카카오 채널, 인스타그램)과 글로벌 플랫폼(스레드·X·링크드인·유튜브 쇼츠) 특성에 맞춘 콘텐츠 전략과 퍼포먼스 마케팅을 지원합니다. 2026년 네이버 C-Rank, GEO(생성형 검색 최적화) 등 최신 알고리즘을 반영합니다.

> **v2.3.0 책임 정리 (Track C 페어 정리)**
> - **`sns-content` 확장** — `moai-content:social-media`를 흡수해 한국 3채널(인스타·네이버 블로그·카카오) + 글로벌 4채널(스레드·X·링크드인·유튜브 쇼츠) **단일 진입점**이 되었습니다. 두 모드 모두 본 스킬에서 자동 라우팅합니다.
> - **`campaign-planner` 책임 분리** — "이커머스 상세페이지 제작·AI 이미지 생성" 책임이 제거되었습니다. 상세페이지 카피는 `moai-commerce:detail-page-copy`, 상세페이지 합성 이미지는 `moai-commerce:detail-page-image`, AI 이미지·영상은 `moai-media:*` 스킬을 사용하세요. 본 스킬은 캠페인 단위 전술(1~3개월)에만 집중합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [brand-identity](./skills/brand-identity/) | 기업 브랜딩 풀 파이프라인. 네이밍, 슬로건, 톤앤매너, 비주얼 가이드라인 [책임 경계: 기업 브랜드 전략] | 4 | ✅ |
| [personal-branding](./skills/personal-branding/) | 개인 브랜딩. 자기 분석, 포지셔닝, 콘텐츠 전략, 채널별 최적화 [책임 경계: 개인 브랜드 전략] | 3 | ✅ |
| [sns-content](./skills/sns-content/) | **🆕 확장 v2.3.0** — 한국 3채널(인스타·네이버 블로그·카카오) + 글로벌 4채널(스레드·X·링크드인·유튜브 쇼츠) 통합 단일 진입점. `moai-content:social-media`를 흡수 (v2.5.0까지 stub 호환) | 6 | ✅ |
| [campaign-planner](./skills/campaign-planner/) | **🔄 책임 분리 v2.3.0** — 마케팅 캠페인 기획·A/B 테스트·인플루언서·CRM·고객 여정(1~3개월 전술). 상세페이지·이미지 책임은 moai-commerce/moai-media로 이관 | 9 | ✅ |
| [seo-audit](./skills/seo-audit/) | 네이버/구글/AI 검색(GEO) 통합 SEO 감사, 키워드 분석, C-Rank 개선 | 0 | ✅ |
| [email-sequence](./skills/email-sequence/) | 정보통신망법 준수 이메일 시퀀스, 드립 캠페인, 온보딩/재활성화 | 0 | ✅ |
| [performance-report](./skills/performance-report/) | GA4/메타/네이버/카카오모먼트 채널별 ROAS 분석, KPI 대시보드 [책임 경계: 마케팅 채널 성과] | 0 | ✅ |
| [target-script](./skills/target-script/) | 타겟 오디언스 분석 + 채널별 메시징 스크립트 자동 생성 (인스타·블로그·이메일·LinkedIn) | 1 | ✅ |
| [landing-page-conversion-audit](./skills/landing-page-conversion-audit/) | **🆕 v2.4.0** — 랜딩페이지 6섹션 구조 진단 + 진단 분기(CTR↓→광고 / CVR↓→랜딩 / 장바구니↓→결제) + 빠른 처방 3종(불안해소 문구 +10~20% / 메시지 일치 / 간편결제). 자료 4 §9 wrapper | 0 | ✅ |
| [pixel-audit](./skills/pixel-audit/) | **🆕 v2.4.0** — 메타·구글 픽셀 설치 검증 + 3종 실수 점검(구매자 미제외/이벤트 파라미터 미설정/CAPI 미설치) + 1st Party 데이터 활용 + Lookalike 씨앗 품질(VIP 상위 20% 권장) | 0 | ✅ |

## sns-content 채널 매트릭스 (v2.3.0)

| 모드 | 채널 | 톤 가이드 | 길이 가이드 |
|------|------|----------|-------------|
| **한국 3채널** | 인스타그램 | 친근·이모지 활용 | 캡션 150자, 해시태그 10~15개 |
|  | 네이버 블로그 | 정보·SEO 키워드 | 본문 1500~3000자, C-Rank 최적화 |
|  | 카카오 채널 | 직관·짧은 CTA | 메시지 90자, 알림톡 변수 ${name} |
| **글로벌 4채널 (v2.3.0 신규)** | Threads (스레드) | 캐주얼·대화형 | 500자, 4~5개 연속 포스트 |
|  | X (Twitter) | 임팩트·헤드라인 | 280자, 스레드(threadcrop) |
|  | LinkedIn | 전문·인사이트 | 1300자, Hook + 본문 + CTA |
|  | YouTube Shorts | 60초 영상 스크립트 | 영상 60초 + 캡션 100자 |

## 책임 경계 (Track C 페어 정리, v2.3.0)

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| **광고 카피 (일반)** | `moai-content:copywriting` |
| **이커머스 광고·톡톡·푸시 카피** | `moai-commerce:commerce-copywriting` |
| **상세페이지 카피 (13섹션)** | `moai-commerce:detail-page-copy` |
| **상세페이지 합성 이미지 (1080×12720)** | `moai-commerce:detail-page-image` |
| **AI 이미지·영상 생성** | `moai-media:*` (image-gen·video-gen·media-gpt-image2-builder 등) |
| **이커머스 V6 6도구 (시장조사·JTBD·상품명·NCM 메시지)** | `moai-commerce:commerce-*` |
| **사업·OKR·BMC 단위 전략(1~5년)** | `moai-business:strategy-planner` |
| **개인 브랜드 콘텐츠 채널 전략** | `moai-marketing:personal-branding` (이 플러그인) |
| **기업 브랜드 네이밍·슬로건·톤앤매너** | `moai-marketing:brand-identity` (이 플러그인) |
| **캠페인 단위 전술 (A/B·인플루언서·CRM, 1~3개월)** | `moai-marketing:campaign-planner` (이 플러그인) |

## 사용 예시

```
인스타그램용 브랜드 아이덴티티 카피 5개 만들어줘. 20-30대 여성 타깃, 친근한 톤.
```

```
LinkedIn 포스팅 만들어줘. B2B SaaS 창업자, 시드 라운드 클로징 후기 1300자.
```
→ `sns-content` (글로벌 4채널 모드, v2.3.0+)

```
유튜브 쇼츠 60초 스크립트 + 캡션 써줘. 개발자 취업 채널.
```
→ `sns-content` (글로벌 4채널 모드)

```
네이버 블로그 SEO 최적화 전략 세워줘. 키워드는 "재테크 방법"이야.
```
→ `seo-audit` + `sns-content` (한국 3채널 모드)

```
이번 달 마케팅 성과 보고서 만들어줘. GA4 + 네이버 광고 데이터 기준.
```
→ `performance-report`

```
인플루언서 A/B 테스트 캠페인 3개월 기획해줘.
```
→ `campaign-planner` (전술 1~3개월)

## 변경 이력

- **v2.4.0** (2026-05-12): 광고 심리학 완전판 통합 — 신규 2 (`landing-page-conversion-audit` 랜딩 6섹션 진단 + `pixel-audit` 픽셀·Lookalike 검증) + 강화 2 (`campaign-planner` 6 방아쇠·8 편향·PAS·후크 6종·영상 30초·타겟 온도 × 동기 매트릭스 + `sns-content` 채널별 심리·메타 학습 48~72h). 8 → **10 스킬**. 자료 4 "온라인 광고의 심리학" 13장 376줄 통합
- **v2.3.0** (2026-05-12): Track C 페어 정리 — `sns-content` 한국 3채널 + 글로벌 4채널 통합 단일 진입점화(`moai-content:social-media` 흡수), `campaign-planner` 책임 분리(상세페이지·이미지 책임을 moai-commerce/moai-media로 이관). 15개 페어 description [책임 경계] 명시. 8 스킬 유지
- **v2.0.0** (2026-05-04): cowork v2.0.0 — Breaking change 없음

## 설치

Settings > Plugins > cowork-plugins에서 `moai-marketing` 선택

## 참고자료

| 항목 | URL |
|------|-----|
| [네이버 서치어드바이저](https://searchadvisor.naver.com/) | 네이버 SEO |
| [카카오 비즈니스](https://business.kakao.com/) | 카카오 채널 마케팅 |
| [Google Search Console](https://search.google.com/search-console) | 구글 SEO |
| [Threads API](https://developers.facebook.com/docs/threads) | Threads 발행 |
| [X (Twitter) API](https://developer.twitter.com/) | X 스레드 |
| [LinkedIn Marketing](https://business.linkedin.com/marketing-solutions) | LinkedIn 마케팅 |
