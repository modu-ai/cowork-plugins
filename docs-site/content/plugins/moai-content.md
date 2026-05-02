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
인스타그램 6슬라이드 카드뉴스로 정부 지원금 신청 방법 만들어줘.
```

## 다음 단계

- [`moai-media`](../moai-media/) — 이미지·영상 동시 생성
- [`moai-marketing`](../moai-marketing/) — SEO 감사·캠페인 기획과 결합

---

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [moai-content 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-content)
