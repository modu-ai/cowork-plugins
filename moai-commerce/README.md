# moai-commerce

> 한국 이커머스 풀세트 자동화 플러그인 — **모두의 커머스 3일 마스터 캠프** 전용 V6 6도구 + 상세페이지·이미지·사진 + 채널 가이드 5종 + 통합 마케팅 전략·카피·라이브 커머스 + **식약처 안전(MFDS)**

[![버전](https://img.shields.io/badge/version-2.4.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-22-success)](#스킬-카탈로그-22종)

> **v2.4.0 신규 3 + 강화 강화** — `coupang-ad-optimizer`(쿠팡 광고 풀세트 최적화, 정해준 강사 6개월 노하우), `commerce-margin-calculator`(마진·엔드 ROAS 자동 계산), `commerce-automation-audit`(6대 영역 자동화 진단·로드맵) + `commerce-product-naming`/`detail-page-copy`/`commerce-jtbd-persona`/`commerce-channel-message`/`commerce-integrated-strategy`/`commerce-market-research` 6개 강화

## 개요

`moai-commerce`는 월 매출 100만~10억 스마트스토어·자사몰 셀러를 위한 풀 사이클 자동화 플러그인입니다. **v2.3.0부터** "모두의 커머스 3일 마스터 캠프"(정해준 강사) 21세션·18개 산출물 데이터 체인을 자연어 한 줄 입력으로 자동 호출합니다.

- **Day 1 셋업 (2)**: 매장 운영 데이터 1줄 통합 (`commerce-morning-brief`, `commerce-order-summary`)
- **Day 2 V6 6도구 (6)**: V6 7교시 구조 1:1 매핑 wrapper — 시장조사·JTBD·페르소나·상품명·NCM 메시지·통합 전략
- **상세페이지 (3)**: 13섹션 감정여정 카피 + 1080×12720 합성 PNG + 사진 사전 분석
- **채널 가이드 (5)**: 쿠팡·네이버·D2C(카페24/아임웹/메이크샵)·크라우드펀딩·큐레이션
- **마케팅·전략 (3)**: 통합 전략·광고/CRM 카피·라이브 커머스 스크립트
- **안전 (1)**: 식약처(MFDS) 의약품·식품 통합 조회

합성 로직은 Pillow 단일 의존성으로 자체 구현되어 외부 패키지 설치가 필요하지 않습니다. V6 6도구와 Day1 셋업 스킬은 **MoAI-Commerce MCP Phase 1**(v2.4.0 출시 예정)을 호출합니다.

## 스킬 카탈로그 (22종)

### v2.4.0 신규 3 — 캠프 후속 인사이트 통합

| 스킬 | 역할 |
|------|------|
| [coupang-ad-optimizer](./skills/coupang-ad-optimizer/SKILL.md) | 쿠팡 광고 풀세트 최적화. 3 캠페인 유형(AI스마트/매출최적화/수동키워드) 자동 분류 + 검색영역 vs 비검색영역 매출 분리(CPM 167배 차이) + 엔드 ROAS 자동 계산 + 자동규칙 3종 + 상품별 의사결정 분기. **정해준 강사 본인 6개월 노하우(월매출 7천→3.6억, 광고비 30%→11.2%) wrapper** |
| [commerce-margin-calculator](./skills/commerce-margin-calculator/SKILL.md) | 상품별 마진·엔드 ROAS·손익분기 광고비 자동 계산. 채널별 수수료(스마트스토어 5.94%/쿠팡 10~12%/카페24 2~3%/아임웹 0~2.5%) + 부가세·결제 수수료·쿠폰 자동 반영. 시크릿팡 마진계산기 차용 + AI 챗봇 차별화 |
| [commerce-automation-audit](./skills/commerce-automation-audit/SKILL.md) | 6대 영역(A~F) 진단 + 자동화 3분류(반복형/판단형/창의형) + 우선순위 점수((빈도×시간×오류비용)÷복잡도) + 3 Phase 로드맵(Quick Wins/Core/AI Enhancement) + 5대 KPI + HITL Golden Rule(80% 자동화 + 10배 검수). 정해준 강사 "커머스 업무 자동화" 24p 풀세트 wrapper |

### 기존 19종 (v2.3.0 + v2.4.0 강화)

### Day 1 셋업 (2) — 매장 데이터 1줄 통합 (v2.3.0 신규)

| 스킬 | 역할 |
|------|------|
| [commerce-morning-brief](./skills/commerce-morning-brief/SKILL.md) | MCP `dashboard_morning_brief` → 어제 주문·신규 문의·트렌드·ROAS 4영역 1줄 통합 |
| [commerce-order-summary](./skills/commerce-order-summary/SKILL.md) | MCP `order_summary_today` → 스마트스토어 + 카페24 + 아임웹 채널 통합 신규 주문 1줄 |

### Day 2 V6 6도구 (5 신규 + 1 강화) — V6 7교시 구조 1:1 매핑 (v2.3.0)

| 스킬 | V6 매핑 | MCP 호출 | 산출물 |
|------|---------|----------|--------|
| [commerce-market-research](./skills/commerce-market-research/SKILL.md) | ① 시장조사 | `trend_search`·`trend_shopping_categories`·`trend_shopping_keywords`·`keyword_for_product_idea` | 거시·경쟁·검색 3축 시장 리포트 1장 |
| [commerce-jtbd-persona](./skills/commerce-jtbd-persona/SKILL.md) | ② 고객분석 | `review_list_naver`·`review_list_cafe24`·`qna_list_cafe24` | `--mode jtbd`: JTBD 9개 / `--mode persona`: 페르소나 3명 8필드 (리뷰 10건 미만 시 fallback) |
| [detail-page-copy](./skills/detail-page-copy/SKILL.md) **강화** | ③ 상세페이지 | — | 기본 13섹션 + `--mode diagnose`: 7단계 진단 점수 / `--mode copy`: 페르소나 2세트 카피(비율 25/50/25 강제) |
| [commerce-product-naming](./skills/commerce-product-naming/SKILL.md) | ④ 상품명 | `keyword_search_volume`·`keyword_related`·`keyword_bulk_research` | 상품명 3안(검색·CTR·브랜드) + 스마트스토어/쿠팡/네이버쇼핑 25자·금지어 검증 |
| [commerce-channel-message](./skills/commerce-channel-message/SKILL.md) | ⑤ 채널별 메시지 | `keyword_seasonal_calendar`·`ad_keyword_performance` | NCM(Need→Channel→Moment→Message→CTA) 검색·광고·CRM × 5종 = 15종 |
| [commerce-integrated-strategy](./skills/commerce-integrated-strategy/SKILL.md) | ⑥ 통합 전략 | `dashboard_morning_brief`·`sales_compare_channels`·`ad_roas_summary` | 매출 향상 전략 1장 + 실행 우선순위 Top 3 |

### 상세페이지 (2) — Day 3 합성·사진

| 스킬 | 역할 |
|------|------|
| [detail-page-image](./skills/detail-page-image/SKILL.md) | 13섹션 이미지 프롬프트 → `moai-media:nano-banana` 호출 → Pillow 1080×12720 합성 |
| [product-photo-brief](./skills/product-photo-brief/SKILL.md) | 상품 사진 사전 분석 + ProductDNA 추출 + 부족한 컷 식별 + 추가 촬영 브리프 |

### 채널 가이드 (5)

| 스킬 | 역할 |
|------|------|
| [marketplace-coupang](./skills/marketplace-coupang/SKILL.md) | 쿠팡 정책 + 검색최적화 + 우수상품 + 로켓배송 가이드 |
| [marketplace-naver](./skills/marketplace-naver/SKILL.md) | 네이버 스마트스토어 + 11번가/G마켓/옥션 오픈마켓 가이드 |
| [marketplace-d2c](./skills/marketplace-d2c/SKILL.md) | 자사몰(D2C) — 카페24 + 아임웹 + 메이크샵 운영 가이드 |
| [marketplace-crowdfunding](./skills/marketplace-crowdfunding/SKILL.md) | 크라우드펀딩 — 와디즈 + 텀블벅 프로젝트 기획·심사·운영 |
| [marketplace-curation](./skills/marketplace-curation/SKILL.md) | 큐레이션 — 카카오 메이커스 + 무신사 + 29CM 입점 제안 |

### 마케팅·전략·안전 (4)

| 스킬 | 역할 |
|------|------|
| [commerce-strategy](./skills/commerce-strategy/SKILL.md) | 통합 전략 — 채널 믹스, 가격, 프로모션 캘린더, 리텐션, KPI |
| [commerce-copywriting](./skills/commerce-copywriting/SKILL.md) | 광고·톡톡·푸시·이메일 카피 (`ai-slop-reviewer` 자동 체이닝) |
| [live-commerce](./skills/live-commerce/SKILL.md) | 네이버·카카오·그립·쿠팡 라이브 커머스 가이드 + 30/60분 스크립트 |
| [mfds-safety](./skills/mfds-safety/SKILL.md) | 식약처(MFDS) 의약품·식품 안전 통합 — e약은요·건강기능식품 인정현황·검사부적합·회수. red flag 시 응급 안내 우선 (v2.0.0+) |

## 표준 워크플로우 (3일 캠프 기준)

```
Day 1: 셋업 + 시장 진단
  commerce-morning-brief → commerce-order-summary → commerce-market-research
       ↓
Day 2: V6 6도구 (Why → What → Channel)
  commerce-jtbd-persona(JTBD 9) → commerce-jtbd-persona(페르소나 3) → detail-page-copy(--mode diagnose)
       → commerce-product-naming(3안) → commerce-channel-message(NCM 15종) → commerce-integrated-strategy
       ↓
Day 3: 산출물 합성 (moai-media 연계)
  product-photo-brief → detail-page-copy(--mode copy) → detail-page-image
       → moai-media:* (이미지·영상·음성) → live-commerce(선택)
       ↓
채널 운영:
  marketplace-{coupang|naver|d2c|crowdfunding|curation} → commerce-copywriting → mfds-safety(헬스/F&B)
```

## 13섹션 감정여정 구조 (`detail-page-copy` 기본 모드)

| # | 섹션 | 높이(px) | 역할 |
|---|------|---------|------|
| 1 | Hero | 1600 | 긴급성 헤더 + 메인 이미지 |
| 2 | Pain | 800 | 공감 — "이런 고민 있으신가요?" |
| 3 | Problem | 800 | 문제 정의 |
| 4 | Story | 1200 | Before→After 스토리 |
| 5 | Solution | 800 | 솔루션 소개 |
| 6 | How | 900 | 작동 방식 시각화 |
| 7 | Proof | 1420 | 사회적 증거 (리뷰/수치) |
| 8 | Authority | 800 | 권위/전문성 |
| 9 | Benefits | 1200 | 핵심 혜택 |
| 10 | Risk | 800 | 리스크 제거 (보증/환불) |
| 11 | Compare | 800 | 최종 Before/After |
| 12 | Filter | 700 | 타겟 필터링 |
| 13 | CTA | 900 | 최종 구매 유도 |

합계: **1080 × 12720 픽셀**

## 채널 분류

| 분류 | 채널 | 적합 |
|------|------|------|
| 오픈마켓 | 쿠팡 / 네이버 스마트스토어 / 11번가 / G마켓 / 옥션 | 트래픽 확보, 신규 매출 |
| 자사몰(D2C) | 카페24 / 아임웹 / 메이크샵 | 브랜드 통제, LTV 운영 |
| 크라우드펀딩 | 와디즈 / 텀블벅 | 신상 사전판매·검증 |
| 큐레이션 | 카카오 메이커스 / 무신사 / 29CM | 브랜드 가치, 한정 운영 |
| 라이브 커머스 | 네이버 쇼핑라이브 / 카카오 / 그립 / 쿠팡 라이브 | 실시간 전환, 인플루언서 |

> **참고**: 티몬·위메프는 큐텐 인수 후 2024년 미정산 사태로 회생절차에 진입하여 본 가이드 대상에서 제외되었습니다.

## 사용 예시

```
"내 카테고리 시장조사 해줘"                                # → commerce-market-research
"리뷰 분석해서 페르소나 만들어줘"                            # → commerce-jtbd-persona --mode persona
"현재 상세페이지 진단해줘"                                  # → detail-page-copy --mode diagnose
"키워드 넣어서 상품명 3안 만들어줘 — 무선이어폰, ANC, 30시간"  # → commerce-product-naming
"검색·광고·CRM 채널별로 메시지 15종 뽑아줘"                   # → commerce-channel-message
"오늘 배운 것 종합 전략으로 1장 정리해줘"                     # → commerce-integrated-strategy
"무선 이어폰 상세페이지 13섹션 카피 + 합성 이미지 만들어줘"   # → detail-page-copy → detail-page-image
"신상 패션 와디즈 펀딩 기획 + 영상 시놉시스"                  # → marketplace-crowdfunding
"네이버 쇼핑라이브 60분 스크립트 — 무선이어폰 3종"            # → live-commerce
"건강식품 식약처 검사부적합 이력 확인"                        # → mfds-safety
```

## MCP 의존성 (v2.3.0)

V6 6도구와 Day1 셋업 스킬은 **MoAI-Commerce MCP Phase 1**(34종 도구)을 호출합니다. v2.3.0 출시 시점에는 MCP 서버가 아직 미출시이므로 다음 중 하나로 대체합니다:

- **옵션 A**: 사전 녹화 영상 5분 (PDF §S4 운영 노트)
- **옵션 B**: 강사 본인 워크스페이스에서 라이브 호출

**v2.4.0 출시 예정** — `cowork-plugins/mcp-servers/moai-commerce/` monorepo에 Python(uvx) 기반 MCP 서버 구현. 광고 운영 4종(meta ads · tiktok ads · 네이버 광고 · 카카오 모먼트) + Phase 1 34종 + Higgsfield MCP 통합.

## 의존성

- **필수**: Pillow (Python 이미지 라이브러리) — `detail-page-image` 합성 단계
- **권장**: `moai-media` 플러그인 — 13섹션 이미지·Day 3 광고 영상·음성 생성
- **권장(v2.3.0+)**: `moai-core:mcp-connector-setup` — Drive·Notion·Higgsfield·OpenAI 4커넥터 인증 가이드
- **선택**: `codex` CLI ≥0.124.0 + ChatGPT OAuth — `detail-page-copy` 보조 분석

## 관련 플러그인

- `moai-media` — Day 3 AI 모델 6스킬(GPT Image 2·Kling 3·Veo 3·Seedance 라우터·캔바 매직 레이어·AI 표기)
- `moai-content` — 카드뉴스·블로그·랜딩·상세페이지(코드, shadcn/ui)
- `moai-marketing` — `sns-content` 한국 3채널 + 글로벌 4채널, `campaign-planner`(중장기 캠페인 기획, 상세페이지 책임은 본 플러그인으로 이관)
- `moai-education` — `course-followup-sequence` 강의 후 30일 자산화

## 변경 이력

- **v2.4.0** (2026-05-12): "캠프 후속 인사이트 통합본" — 신규 3 (`coupang-ad-optimizer`·`commerce-margin-calculator`·`commerce-automation-audit`) + 강화 6 (`product-naming`·`detail-page-copy`·`jtbd-persona`·`channel-message`·`integrated-strategy`·`market-research`). 정해준 강사 본인 노하우 3개 문서 + 광고 심리학 완전판 통합. 총 19 → **22 스킬**
- **v2.3.0** (2026-05-12): "모두의 커머스 3일 마스터 캠프" 통합본 — V6 6도구 5신규 + `detail-page-copy` 강화 + Day1 셋업 2신규. 총 11 → **19 스킬**. `commerce-market-research` · `commerce-jtbd-persona` · `commerce-product-naming` · `commerce-channel-message` · `commerce-integrated-strategy` · `commerce-morning-brief` · `commerce-order-summary` 추가
- **v2.0.0** (2026-05-04): `mfds-safety` 추가 (식약처 의약품·식품 안전 통합). 11 스킬
- **v1.x**: 13섹션 상세페이지 + 채널 가이드 5종 + 라이브 커머스 + 마케팅

자세한 변경 내역: [CHANGELOG.md](../CHANGELOG.md)

## 라이선스

MIT — 자유롭게 사용·수정·재배포 가능.
