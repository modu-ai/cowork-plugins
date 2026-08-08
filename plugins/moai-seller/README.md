# 셀러 (moai-seller)

이커머스 셀러 전담 AI 코워커입니다. 스마트스토어·아임웹·카페24 MCP 연동과 상세페이지·마켓플레이스·광고·CRM 등 커머스 실무 스킬 31종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다. VOC 분류(`cs-voc-triage`)와 채널 메시지(`cs-channel-message`)는 `moai-cs`(CS매니저)로 이관되었습니다.

**이런 분께 추천**: 온라인 셀러 · 이커머스 운영자 · 1인 브랜드 대표

## 설치

Claude Code에서 두 단계로 설치합니다:

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-seller@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-seller
```

## 스킬 31종

호출 형식: `/moai-seller:commerce-<스킬명>` — 예: `/moai-seller:commerce-detail-page-planner`. 자연어 요청("우리 제품 상세페이지 기획해줘")으로도 자동 매칭됩니다.

### 상세페이지 (7종)

| 스킬 | 역할 |
|------|------|
| `commerce-detail-page-planner` | 상세페이지 구조·설득 흐름 기획 |
| `commerce-detail-page-copy` | 상세페이지 카피라이팅 |
| `commerce-detail-page-image` | 상세페이지 이미지 구성 설계 |
| `commerce-product-detail` | 상품 상세 정보 구성 |
| `commerce-product-naming` | 상품명·검색 키워드 네이밍 |
| `commerce-product-image-pipeline` | 상품 이미지 제작 파이프라인 |
| `commerce-product-photo-brief` | 상품 촬영 브리프 작성 |

### 마켓플레이스 (5종)

| 스킬 | 역할 |
|------|------|
| `commerce-marketplace-naver` | 네이버 스마트스토어 입점·운영 |
| `commerce-marketplace-coupang` | 쿠팡 입점·운영 |
| `commerce-marketplace-crowdfunding` | 와디즈 등 크라우드펀딩 론칭 |
| `commerce-marketplace-curation` | 큐레이션 커머스(카카오 등) 입점 |
| `commerce-marketplace-d2c` | 자사몰(D2C) 구축·운영 전략 |

### 광고·프로모션 (8종)

| 스킬 | 역할 |
|------|------|
| `commerce-marketplace-coupang-ads` | 쿠팡 광고 운영 |
| `commerce-marketplace-naver-ads` | 네이버 검색광고(쇼핑검색·파워링크·브랜드검색·GFA) 운영 |
| `commerce-coupang-ad-optimizer` | 쿠팡 광고 최적화 |
| `commerce-promotion-planner` | 프로모션·할인 기획 |
| `commerce-live-commerce` | 라이브커머스 기획·운영 |
| `commerce-influencer-collab` | 인플루언서 협업 설계 |
| `commerce-early-fan-builder` | 초기 팬덤 구축 |
| `commerce-season-calendar` | 시즌·이벤트 캘린더 운영 |

### CRM·구독 (2종)

| 스킬 | 역할 |
|------|------|
| `commerce-repurchase-timer` | 재구매 주기 기반 리텐션 설계 |
| `commerce-subscription-strategist` | 구독 모델 전략 |

> 채널 메시지(`cs-channel-message`)·VOC 분류(`cs-voc-triage`)는 `moai-cs`(CS매니저)로 이관되었습니다.

### 전략·분석 (9종)

| 스킬 | 역할 |
|------|------|
| `commerce-integrated-strategy` | 커머스 통합 전략 수립 |
| `commerce-market-research` | 시장·경쟁 조사 |
| `commerce-jtbd-persona` | JTBD 기반 고객 페르소나 |
| `commerce-ltv-cac-architect` | LTV/CAC 단위경제 설계 |
| `commerce-margin-calculator` | 마진·손익 계산 |
| `commerce-morning-brief` | 셀러 모닝 브리프 |
| `commerce-automation-audit` | 운영 자동화 진단 |
| `commerce-message-compliance-kr` | 정통망법 메시지 발송 규제(스팸) 게이트 |
| `commerce-ad-claim-compliance-kr` | 표시광고법·식약처·전상법 광고 문구 검증 게이트 |

## MCP 연동 3종

플러그인 루트 `.mcp.json`에 3개 커머스 MCP 서버가 선언되어 있습니다. 자격증명은 **환경변수로만** 설정하세요(파일에 키를 적지 않습니다).

| 서버 | 플랫폼 | 필요 환경변수 | 상태 |
|------|--------|---------------|------|
| `moai-smartstore` | 네이버 스마트스토어 (9 영역 90 도구) | `NAVER_COMMERCE_CLIENT_ID`, `NAVER_COMMERCE_CLIENT_SECRET`, `NAVER_COMMERCE_ACCOUNT_ID`, `NAVER_COMMERCE_TYPE` | ⚠️ 소스 복원 대기 — 선언은 유지되어 있으나 `mcp-servers/moai-smartstore` 소스 디렉토리 복원 전까지 기동 불가 |
| `moai-imweb` | 아임웹 OPEN API v3 (136 엔드포인트 → 8 카테고리 도구) | `IMWEB_CLIENT_ID`, `IMWEB_CLIENT_SECRET`, `IMWEB_ACCESS_TOKEN`, `IMWEB_REFRESH_TOKEN`, `IMWEB_UNIT_CODE` | 정상 (vendored) |
| `moai-cafe24` | 카페24 Admin API 19 도메인 + Analytics | `CAFE24_MALL_ID`, `CAFE24_CLIENT_ID`, `CAFE24_CLIENT_SECRET`, `CAFE24_ACCESS_TOKEN`, `CAFE24_REFRESH_TOKEN` | 정상 (vendored) |

- 사전 설치: `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- 자격증명 발급 절차: 각 서버 디렉토리의 `CONNECTORS.md` / `README.md` 참고
- 경로는 `${CLAUDE_PLUGIN_ROOT}` 기준이므로 marketplace 설치(캐시 복사) 환경에서도 동작합니다

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `listing-builder` | worker | 상세페이지·리스팅·광고·CRM 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → commerce-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 외부 발신·플랫폼 상태 변경은 사용자 승인 없이 절대 수행하지 않음 |
| `margin-auditor` | read-only audit | 마진 계산·리스팅·캠페인 플랜을 회의적으로 재검산하는 감사 에이전트. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
