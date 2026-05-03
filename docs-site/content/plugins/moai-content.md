---
title: "moai-content — 블로그·카드뉴스·랜딩"
weight: 30
description: "한국 콘텐츠·마케팅 실무에 최적화된 블로그·카드뉴스·랜딩페이지·뉴스레터 등 8개 스킬 묶음입니다."
geekdocBreadcrumb: true
tags: ["moai-content"]
---

# moai-content

> 한국 마케팅·콘텐츠 실무에 최적화된 8개 스킬을 제공합니다. 네이버 블로그·티스토리·인스타그램·LinkedIn·카카오 채널까지 플랫폼별 알고리즘 차이를 반영합니다.

## 무엇을 하는 플러그인인가

`moai-content` (v1.5.0)는 한국 디지털 마케팅 채널의 실제 운영 노하우를 반영해 설계된 텍스트 콘텐츠 생성 플러그인입니다. 단순히 글을 만드는 데 그치지 않고, 네이버 C-Rank·D.I.A. 알고리즘이나 인스타그램의 카드뉴스 길이 기준 등 채널별 베스트 프랙티스를 본문 구조에 반영합니다.

블로그 포스트·카드뉴스·랜딩페이지·뉴스레터·상세페이지·SNS·카피라이팅·미디어 기획까지 8개 스킬이 도메인별로 분리되어 있어, 필요한 채널만 선택해 호출할 수 있습니다.

별도 API 키 없이 사용 가능하며, WordPress 자동 업로드를 원하면 WordPress MCP 연결이 필요합니다.

## 설치

{{< tabs "install-content" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `moai-core` 설치 후 `moai-content` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-content)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬

| 스킬 | 용도 | 대표 출력 |
|---|---|---|
| `blog` | 네이버·티스토리·브런치·WordPress·Ghost 블로그 포스트 | 플랫폼별 SEO 최적화 본문 |
| `card-news` | 인스타그램·페이스북 카드뉴스·캐러셀 | 슬라이드별 카피 + 이미지 프롬프트 |
| `landing-page` | 단독 전환 목적 랜딩 페이지 | HTML (Tailwind) + 카피 |
| `product-detail` | 네이버 스마트스토어·쿠팡 상세페이지 | 상세 HTML + 이미지 프롬프트 |
| `newsletter` | 이메일 뉴스레터 (stibee·mailchimp 스타일) | HTML + 제목 A/B 안 |
| `copywriting` | 광고 헤드라인·슬로건·CTA | 3~5개 대안 카피 |
| `social-media` | 릴스·쇼츠·스레드·X·LinkedIn 포스트 | 플랫폼별 버전 |
| `media-production` | 유튜브·팟캐스트 기획, 콘텐츠 캘린더 | 기획서·큐시트 |
| `korean-spell-check` (v2.0.0 신규) | 바른한글(부산대) 한국어 맞춤법·띄어쓰기 최종 검수 | 원문/교정안/이유 |

## 한국 시장 특화 포인트

- 네이버 **C-Rank·D.I.A. 알고리즘**을 반영한 본문 구조
- **GEO(생성형 검색 최적화)** 시대에 맞춘 FAQ·스키마 마크업 권장
- 인스타그램 **2026년 알고리즘** 변화 대응 캐러셀 길이 기준
- 네이버 블로그·티스토리의 **SEO 점수** 체크포인트 내장

## 대표 체인

**블로그 발행 파이프라인**

```text
blog → ai-slop-reviewer → (선택) moai-media:nano-banana
```

**쇼핑몰 상세페이지**

```text
product-detail → moai-media:nano-banana → ai-slop-reviewer
```

**카드뉴스 시리즈**

```text
card-news → moai-media:nano-banana → ai-slop-reviewer
```

## 빠른 사용 예

```text
네이버 블로그에 '프리랜서 3.3% 원천징수' 주제로 2000자 분량 글 써줘.
키워드는 '원천징수 신고', '종합소득세'.
```

```text
> 인스타그램 6슬라이드 카드뉴스로 정부 지원금 신청 방법 만들어줘.
```

## v2.0.0 신규 — `korean-spell-check` (한국어 맞춤법 검수)

부산대학교 인공지능연구실과 ㈜나라인포테크가 공동 개발한 **바른한글** 공개 검사 표면을 이용해 한국어 문장을 최종 검수합니다. 2024년 10월 기존 "부산대학교 한국어 맞춤법 검사기"에서 **바른한글**로 정식 리브랜딩되었으며, 구 도메인 `speller.cs.pusan.ac.kr`은 폐기되고 [`nara-speller.co.kr`](https://nara-speller.co.kr/speller/)로 통합되었습니다. 블로그·뉴스레터·카피·계약서 등 텍스트 산출물의 마지막 단계에서 사용합니다.

### 권장 체인 위치 — `ai-slop-reviewer` 직후

```text
{콘텐츠 생성 스킬} → ai-slop-reviewer → korean-spell-check → 사용자 최종 검토
```

`ai-slop-reviewer`는 AI 패턴(과한 형용사·반복·번역체)을 검수하고, `korean-spell-check`는 규칙 기반 띄어쓰기·맞춤법을 잡습니다 — 차원이 다릅니다.

### Policy first

- 공개 웹 검사기(`nara-speller.co.kr`)는 **비상업·저빈도** 사용 정책을 명시합니다.
- 본 스킬은 **사용자 주도 최종 검수**용이며, 대량 배치·SaaS 백엔드 연동·상업 서비스 무단 재판매에는 사용하지 않습니다.
- 1500자 청크 분할 + 청크 간 1초 휴지로 conservative 호출.

### 출처 어트리뷰션

본 스킬은 **NomaDamas/k-skill** (MIT) 의 `korean-spell-check`를 cowork에 포팅했습니다.

- **공개 검사 표면**: [바른한글 (nara-speller.co.kr)](https://nara-speller.co.kr/speller/) — 신버전(권장)
- **이전 버전 (form POST 자동화 호환)**: [old_speller](https://nara-speller.co.kr/old_speller/)
- **개발 주체**: 부산대학교 인공지능연구실 + ㈜나라인포테크 공동 개발 (1991년 권혁철 교수 시작, 2001년 웹 서비스 개시, 2024-10 리브랜딩)
- 한컴오피스 한글 2018부터 내장 검사기로 채택, 잡코리아·사람인 취업 포털 탑재

## 다음 단계

- [`moai-media`](../moai-media/) — 이미지·영상 동시 생성
- [`moai-marketing`](../moai-marketing/) — SEO 감사·캠페인 기획과 결합

---

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [moai-content 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-content)
- [NomaDamas/k-skill](https://github.com/NomaDamas/k-skill) — MIT — `korean-spell-check` 원본 (v2.0.0)
- [바른한글 (nara-speller.co.kr)](https://nara-speller.co.kr) — 공개 검사 표면
