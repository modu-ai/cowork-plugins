# moai-commerce

> 한국 이커머스 풀세트 자동화 플러그인 — **모두의 커머스 3일 마스터 캠프** 전용 V6 6도구 + 상세페이지·이미지·사진 + 채널 가이드 5종 + 통합 마케팅 전략·카피·라이브 커머스 + **식약처 안전(MFDS)**

[![버전](https://img.shields.io/badge/version-2.8.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-MIT-green)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-35-success)](#스킬-카탈로그-35종)

> **v2.8.0 Wave 4 신규 7** — `commerce-review-aggregator`(멀티채널 리뷰 4단 분석), `commerce-voc-triage`(KTAS 5단계 VOC), `commerce-subscription-strategist`(구독 5가지 질문 + 4 모델), `commerce-influencer-collab`(5 티어 + 뒷광고 회피), `commerce-early-fan-builder`(충성 100명 부트스트랩 30일), `commerce-trend-namer`(데이터랩 트렌드 변환), `commerce-season-calendar`(30+ 시즌 이벤트)
>
> **v2.7.0 Wave 3 신규 3** — `commerce-promotion-planner`(3대 프로모션 기획법 + 명목·스토리·혜택 3종 세트), `commerce-repurchase-timer`(골든타임 3구간 + 리드 스코어링 + 리텐션 cohort), `commerce-product-image-pipeline`(character-mgmt → image-gen → video-gen → channel-ad-packager 4단계 오케스트레이터)
>
> **v2.6.0 Wave 1 신규 3** (vault grounding) — `commerce-marketing-compliance-kr`(정통망법 광고·정보성 메시지 자동 게이트), `commerce-push-planner`(앱 푸시 4원칙 + 한국 30+ 브랜드 레퍼런스), `commerce-ltv-cac-architect`(CAC→LTV 6대 지표 + 광고 의존도 30%→11~15% 6개월 로드맵)
>
> **v2.4.0 신규 3 + 강화 6** — `coupang-ad-optimizer`(쿠팡 광고 풀세트 최적화, 한국 셀러 6개월 실전 노하우), `commerce-margin-calculator`(마진·엔드 ROAS 자동 계산), `commerce-automation-audit`(6대 영역 자동화 진단·로드맵) + `commerce-product-naming`/`detail-page-copy`/`commerce-jtbd-persona`/`commerce-channel-message`/`commerce-integrated-strategy`/`commerce-market-research` 6개 강화

## 개요

`moai-commerce`는 월 매출 100만~10억 스마트스토어·자사몰 셀러를 위한 풀 사이클 자동화 플러그인입니다. **v2.3.0부터** "모두의 커머스 3일 마스터 캠프" 21세션·18개 산출물 데이터 체인을 자연어 한 줄 입력으로 자동 호출합니다.

- **Day 1 셋업 (2)**: 매장 운영 데이터 1줄 통합 (`commerce-morning-brief`, `commerce-order-summary`)
- **Day 2 V6 6도구 (6)**: V6 7교시 구조 1:1 매핑 wrapper — 시장조사·JTBD·페르소나·상품명·NCM 메시지·통합 전략
- **상세페이지 (3)**: 13섹션 감정여정 카피 + 1080×12720 합성 PNG + 사진 사전 분석
- **채널 가이드 (5)**: 쿠팡·네이버·D2C(카페24/아임웹/메이크샵)·크라우드펀딩·큐레이션
- **마케팅·전략 (3)**: 통합 전략·광고/CRM 카피·라이브 커머스 스크립트
- **안전 (1)**: 식약처(MFDS) 의약품·식품 통합 조회

합성 로직은 Pillow 단일 의존성으로 자체 구현되어 외부 패키지 설치가 필요하지 않습니다. V6 6도구와 Day1 셋업 스킬은 **MoAI-Commerce MCP Phase 1**(v2.4.0 출시 예정)을 호출합니다.

## 스킬 카탈로그 (35종)

### v2.8.0 Wave 4 신규 7 — 한국 D2C 풀스택 완결

| 스킬 | 역할 |
|------|------|
| [commerce-review-aggregator](./skills/commerce-review-aggregator/SKILL.md) | 멀티채널 리뷰 통합 분석 (네이버·쿠팡·자사몰·YouTube·인스타) → 감정·키워드·인사이트·액션플랜 4단 분석. 우선순위 액션 5개 자동 추출 |
| [commerce-voc-triage](./skills/commerce-voc-triage/SKILL.md) | VOC 3축 분류(고객 핏·빈도·핵심 가치 관련성) + KTAS 응급실 5단계 매핑 + 처리 시한·응답 템플릿. 우선순위 점수 = 3축 곱 |
| [commerce-subscription-strategist](./skills/commerce-subscription-strategist/SKILL.md) | 구독 비즈니스 5가지 질문 자기진단 + 4 모델(소비재·경험·관계·맞춤) + 한국 시장 적합성 진단 + 락인·이탈 방지 메시지 매트릭스 |
| [commerce-influencer-collab](./skills/commerce-influencer-collab/SKILL.md) | 5 인플루언서 티어(메가·매크로·마이크로·나노·메가나노) + 뒷광고 회피 체크리스트(표시광고법) + UGC 리그램 가이드 + 5축 굿즈 기획 |
| [commerce-early-fan-builder](./skills/commerce-early-fan-builder/SKILL.md) | 충성 100명 부트스트랩 5원칙(광고 0원·1:1 손편지·UGC·비공개 채널·추천) + 30일 로드맵 + 100→1만 전환 시나리오. 블랭크·강아지 가방 케이스 |
| [commerce-trend-namer](./skills/commerce-trend-namer/SKILL.md) | 네이버 데이터랩 트렌드 → 상품명 변형 3안 + 해시태그 30개 + 블로그 제목 3안 자동 변환 |
| [commerce-season-calendar](./skills/commerce-season-calendar/SKILL.md) | 한국·글로벌 30+ 시즌 이벤트(설날·추석·블프·솽스이·발렌타인) + 카테고리별 매출 피크 매핑 + 분기 캠페인 사전 준비 계획 |

### v2.7.0 Wave 3 신규 3 — 프로모션·재구매·이미지 파이프라인

| 스킬 | 역할 |
|------|------|
| [commerce-promotion-planner](./skills/commerce-promotion-planner/SKILL.md) | 3대 프로모션 기획법(이슈화·얼리버드·한정) 전담. 브랜드 단계(신생/스몰/중대형) + 목표(인지도/충성고객/즉각매출) → 명목·스토리·혜택 3종 세트 + 벤치마킹 케이스 3개 + 실무 체크리스트 6항목 + 노션 템플릿 페이지 구조 자동 생성. 비플레인 '듣보잡' 12배 매출 케이스 실전 매뉴얼 |
| [commerce-repurchase-timer](./skills/commerce-repurchase-timer/SKILL.md) | 재구매 타이밍 엔진. 골든타임 3구간(리마인드 0.8T / 데드라인 1.1T / 휴면 1.5T) + 구간별 메시지 톤·채널 + 리드 스코어링 8개 행동 + 리텐션 차트 cohort 가이드. 화장품·면도기·콘택트렌즈·반려동물·영양제·향수 등 10 카테고리 표준 주기 매트릭스 |
| [commerce-product-image-pipeline](./skills/commerce-product-image-pipeline/SKILL.md) | 상품 이미지·영상 풀스택 파이프라인 오케스트레이터. character-mgmt → image-gen(Soul) → video-gen(DOP) → media-channel-ad-packager 4단계 체인 자동 호출. 자연어 한 줄로 이미지 5~10장 + 영상 5~10초 + 채널 3개 변환 산출 |

### v2.6.0 Wave 1 신규 3 — vault grounding 한국 CRM·LTV·법규

| 스킬 | 역할 |
|------|------|
| [commerce-marketing-compliance-kr](./skills/commerce-marketing-compliance-kr/SKILL.md) | 정통망법 광고/정보성 메시지 자동 게이트. 6대 점검(광고성 판정·옵트인·야간 발송·(광고) 표기·무료 수신거부·발신자 정보). 모든 채널(SMS/LMS/MMS·이메일·앱푸시·카톡 친구톡/알림톡·텔레마케팅) 발송 전 의무 통과. **과태료 회피 ROI: 1회 위반 최대 3,000만 원 + 1년 이하 징역** |
| [commerce-push-planner](./skills/commerce-push-planner/SKILL.md) | 앱 푸시 전용 4원칙(왜/언제/누구에게/어떻게) + Timely·Personal·Actionable 3요소 + 카피 변형 3안(오늘만 vs 매일 / 누구나 vs 너에게만 / 숫자·게이미피케이션·브랜딩) + 한국 30+ 브랜드 레퍼런스(토스·배민·오늘의집·쿠팡·에이블리·지그재그·29CM·인프런·야놀자·퍼블리·넷플릭스·듀오링고 등). 클릭률 예측 가이드 |
| [commerce-ltv-cac-architect](./skills/commerce-ltv-cac-architect/SKILL.md) | CAC→재구매율→구매주기→ARPU→공헌이익→LTV 6대 지표 연결 모델 + LTV/CAC ratio·Payback·광고 의존도 진단 + 광고비 30%→11~15% 6단계 로드맵(Month 1~6) + 한국 D2C 카테고리별 벤치마크(화장품·식품·패션·가전·펫·구독 SaaS) |

### v2.4.0 신규 3 — 캠프 후속 인사이트 통합

| 스킬 | 역할 |
|------|------|
| [coupang-ad-optimizer](./skills/coupang-ad-optimizer/SKILL.md) | 쿠팡 광고 풀세트 최적화. 3 캠페인 유형(AI스마트/매출최적화/수동키워드) 자동 분류 + 검색영역 vs 비검색영역 매출 분리(CPM 167배 차이) + 엔드 ROAS 자동 계산 + 자동규칙 3종 + 상품별 의사결정 분기. **한국 셀러 6개월 실전 노하우(월매출 7천→3.6억, 광고비 30%→11.2%) wrapper** |
| [commerce-margin-calculator](./skills/commerce-margin-calculator/SKILL.md) | 상품별 마진·엔드 ROAS·손익분기 광고비 자동 계산. 채널별 수수료(스마트스토어 5.94%/쿠팡 10~12%/카페24 2~3%/아임웹 0~2.5%) + 부가세·결제 수수료·쿠폰 자동 반영. 시크릿팡 마진계산기 차용 + AI 챗봇 차별화 |
| [commerce-automation-audit](./skills/commerce-automation-audit/SKILL.md) | 6대 영역(A~F) 진단 + 자동화 3분류(반복형/판단형/창의형) + 우선순위 점수((빈도×시간×오류비용)÷복잡도) + 3 Phase 로드맵(Quick Wins/Core/AI Enhancement) + 5대 KPI + HITL Golden Rule(80% 자동화 + 10배 검수). "커머스 업무 자동화" 24p 풀세트 wrapper |

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

- **v2.8.0** (2026-05-16): "Wave 4 — 한국 D2C 풀스택 완결" — 신규 7 (`commerce-review-aggregator`·`commerce-voc-triage`·`commerce-subscription-strategist`·`commerce-influencer-collab`·`commerce-early-fan-builder`·`commerce-trend-namer`·`commerce-season-calendar`). vault-ecom.md §A-3 MED 5 + LOW 2 명세 구현. 총 28 → **35 스킬**
- **v2.7.0** (2026-05-16): "Wave 3 — 프로모션·재구매·이미지 파이프라인" — 신규 3 (`commerce-promotion-planner` 3대 프로모션·`commerce-repurchase-timer` 골든타임 3구간·`commerce-product-image-pipeline` 4단계 오케스트레이터). 총 25 → **28 스킬**
- **v2.6.0** (2026-05-16): "Wave 1 vault grounding" — 신규 3 (`commerce-marketing-compliance-kr` 정통망법 게이트·`commerce-push-planner` 앱 푸시 4원칙·`commerce-ltv-cac-architect` LTV 수익 구조 설계). vault 1,329 노트 기반 한국 CRM·LTV·법규 통합. 총 22 → **25 스킬**
- **v2.4.0** (2026-05-12): "캠프 후속 인사이트 통합본" — 신규 3 (`coupang-ad-optimizer`·`commerce-margin-calculator`·`commerce-automation-audit`) + 강화 6 (`product-naming`·`detail-page-copy`·`jtbd-persona`·`channel-message`·`integrated-strategy`·`market-research`). 한국 셀러 본인 노하우 3개 문서 + 광고 심리학 완전판 통합. 총 19 → **22 스킬**
- **v2.3.0** (2026-05-12): "모두의 커머스 3일 마스터 캠프" 통합본 — V6 6도구 5신규 + `detail-page-copy` 강화 + Day1 셋업 2신규. 총 11 → **19 스킬**. `commerce-market-research` · `commerce-jtbd-persona` · `commerce-product-naming` · `commerce-channel-message` · `commerce-integrated-strategy` · `commerce-morning-brief` · `commerce-order-summary` 추가
- **v2.0.0** (2026-05-04): `mfds-safety` 추가 (식약처 의약품·식품 안전 통합). 11 스킬
- **v1.x**: 13섹션 상세페이지 + 채널 가이드 5종 + 라이브 커머스 + 마케팅

자세한 변경 내역: [CHANGELOG.md](../CHANGELOG.md)

## 라이선스

MIT — 자유롭게 사용·수정·재배포 가능.
