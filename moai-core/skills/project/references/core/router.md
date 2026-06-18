# router.md — 자연어 → 플러그인 라우팅 프로토콜

## 개요
사용자의 자연어 요청을 분석하여 **27개 플러그인** 중 적합한 플러그인을 고르고, 해당 플러그인의 **스킬(또는 스킬 체인)** 으로 라우팅하는 프로토콜.
플러그인 → 스킬(또는 스킬 체인) 모델로 동작한다. 별도의 실행 모듈 계층은 없으며, 각 플러그인의 `skills/` 안 SKILL.md가 곧 실행 단위다.

---

## 1. 라우팅 흐름

```
사용자 자연어 요청
    ↓
[1단계] 프로젝트 컨텍스트 확인
    ├── 프로젝트 CLAUDE.md의 "워크플로우 체인" / .moai/config 에 정의된 산출물 체인 있음
    │       → 해당 스킬 체인으로 직접 실행
    └── 없음 → [2단계]로
    ↓
[2단계] 키워드 매칭
    ├── 매칭 1개 → 해당 플러그인 트리거 → 적합 스킬 선택
    ├── 매칭 2개+ → [3단계] 모호성 해소
    └── 매칭 0개 → [4단계] 폴백
    ↓
[3단계] 모호성 해소
    AskUserQuestion (1질문, 후보 플러그인 4개 이내) ✅
    ↓
[4단계] 폴백
    AskUserQuestion으로 카테고리 직접 질문
```

---

## 2. 요청 분석

### 2.1 자연어 파싱
사용자 입력에서 다음을 추출:
- **핵심 동사**: 작성, 분석, 계획, 검토, 만들어, 생성, 계산 등
- **도메인 키워드**: 아래 §3 키워드 매핑 테이블 참조
- **산출물 유형**: PPT, 한글문서, 카드뉴스, 영상, 보고서 등
- **명시적 도구·포맷**: HWPX, PPTX, Higgsfield, NotebookLM 등

### 2.2 우선순위 규칙
1. **프로젝트 체인 정의** → CLAUDE.md/.moai 에 명시된 산출물 체인 (최우선)
2. **산출물 유형** → 해당 산출물을 만드는 스킬이 있는 플러그인
3. **도메인 키워드** → 키워드 매핑 테이블
4. **핵심 동사** → 범용 매핑

---

## 3. 키워드 → 플러그인 매핑 테이블

| 키워드 | 플러그인 |
|--------|---------|
| project, 초기화, 라우팅, 슬롭검수, 피드백, 커넥터 | moai-core |
| 사업계획, 스타트업, 창업, 시장조사, 투자, IR, 피칭, 소상공인, 정부지원사업, 상권분석 | moai-business |
| 마케팅, SEO, SNS, 광고, 캠페인, 이메일, 랜딩 전환, 픽셀, 메타광고, 네이버, 카카오, 브랜딩 | moai-marketing |
| 법률, 계약서, NDA, 컴플라이언스, 개인정보, 약관, 법인등기 | moai-legal |
| 세금, 부가세, 홈택스, 3.3%, 종소세, 결산, 재무제표, 변동분석 | moai-finance |
| 인사, 노무, 채용, 면접, 4대보험, 퇴직금, 근로계약, 성과평가 | moai-hr |
| 블로그, 카드뉴스, 뉴스레터, 랜딩페이지, 상세페이지, 카피, 콘텐츠, HTML 리포트, 윤문 | moai-content |
| 운영, 프로세스, SOP, 상태보고, 벤더, 조달 | moai-operations |
| 강의, 교육, 커리큘럼, 워크숍, 연수, 시험출제, 교육과정 | moai-education |
| 여행, 건강, 웰니스, 이벤트, 웨딩 | moai-lifestyle |
| 제품, PM, UX, 로드맵, 스펙, PRD | moai-product |
| 고객지원, CS, 티켓, 응대, VOC, KB, 에스컬레이션 | moai-support |
| PPT, 한글, hwpx, Word, docx, Excel, xlsx, PDF, 발표자료, 문서 | moai-office |
| 이력서, 자기소개서, 자소서, 면접, 취업, 포트폴리오, 채용공고 | moai-career |
| 데이터, CSV, 분석, 차트, 시각화, 대시보드, 공공데이터 | moai-data |
| 주식 시세, KRX, 법원경매, 실거래가, 부동산 조회, 공공데이터 조회 | moai-public-data |
| 논문, 특허, KIPRIS, 연구비, 선행기술, 학술, 출원 | moai-research |
| 이미지, 영상, 음성, TTS, 더빙, Higgsfield, 이미지 프롬프트, Soul, Kling | moai-media |
| 이커머스, 상세페이지, 쇼핑몰, 스마트스토어, 쿠팡, 네이버 커머스, 런칭, 상품명, 마켓플레이스 | moai-commerce |
| BI, 임원보고, 경영진 요약, 1pager | moai-bi |
| 주간보고, WBR, 업무보고, 프로젝트 관리 | moai-pm |
| 영업, 제안서, RFP, B2B, 견적 | moai-sales |
| 출판, 원고, 단행본, 책 쓰기, 챕터, 출간, 전자책 | moai-book |
| 디자인, Claude Design, 브랜드 비주얼, design-brief | moai-design |
| 재테크, 가계부, 투자 입문, 종잣돈, 보험, 자산배분, 소비관리 | moai-wealth |
| 회고, 목표관리, OKR, 시간관리, 습관, 루틴, 만다라트, 노션 템플릿 | moai-productivity |
| 보고, 회의, 퍼실리테이션, 피드백, 갈등, 협상, 회의록, 소통 | moai-comms |

---

## 4. 플러그인 상세 키워드

> 각 키워드는 해당 플러그인의 **실제 스킬명**으로 라우팅된다. 산출물 마무리 단계에서는 `moai-core:ai-slop-reviewer`(+ 한국어는 `moai-content:humanize-korean`) 체인을 권장한다.

### moai-core
| 키워드 | 스킬 |
|--------|------|
| 프로젝트 초기화, project init | project |
| AI 슬롭 검수, 후처리 | ai-slop-reviewer |
| 피드백, 이슈 제출 | feedback |
| MCP 커넥터 등록 | mcp-connector-setup |
| 스킬 제작·템플릿·테스트 | skill-builder, skill-template, skill-tester |

### moai-business
| 키워드 | 스킬 |
|--------|------|
| 사업계획, 창업, MVP | startup-launchpad |
| 시장조사, TAM/SAM, 경쟁분석 | market-analyst |
| IR, 투자, 피칭 | investor-relations |
| 전략, OKR, 컨설팅 | strategy-planner, consulting-brief |
| 정부지원사업 | kr-gov-grant |
| 소상공인, 상권분석 | sbiz365-analyst |
| AI 진단, 점검 | ai-diagnostic |
| 부동산 조회 | real-estate-search |
| 영업 플레이북, 데일리 브리핑 | sales-playbook, daily-briefing |

### moai-marketing
| 키워드 | 스킬 |
|--------|------|
| SNS 콘텐츠 | sns-content |
| SEO 진단 | seo-audit |
| 캠페인 기획 | campaign-planner |
| 이메일 시퀀스 | email-sequence |
| 랜딩 전환 진단 | landing-page-conversion-audit |
| 픽셀 점검 | pixel-audit |
| 메타광고 운영·분석 | meta-ads-manager, meta-ads-analyzer |
| 브랜딩, 퍼스널 브랜딩 | brand-identity, personal-branding |
| 성과 리포트, 타겟 스크립트 | performance-report, target-script |

### moai-legal
| 키워드 | 스킬 |
|--------|------|
| 계약서 검토 | contract-review |
| NDA 검토 | nda-triage |
| 컴플라이언스 | compliance-check |
| 법률 리스크 | legal-risk |
| 법인등기 자동화 | iros-registry-automation |

### moai-finance
| 키워드 | 스킬 |
|--------|------|
| 세금, 부가세, 3.3%, 종소세 | tax-helper |
| 결산 | close-management |
| 재무제표 | financial-statements |
| 변동분석 | variance-analysis |
| 주식 시세 조회 | korean-stock-search |
| 법원경매 조회 | court-auction-search |

### moai-hr
| 키워드 | 스킬 |
|--------|------|
| 근로계약, 4대보험, 퇴직금 | employment-manager |
| 채용 서류 검토 | resume-screener |
| 오퍼레터 | draft-offer |
| 성과평가 | performance-review |
| 인사 운영 | people-operations |

### moai-content
| 키워드 | 스킬 |
|--------|------|
| 블로그 | blog |
| 카드뉴스 | card-news |
| 뉴스레터 | newsletter |
| 랜딩페이지 | landing-page |
| 상세페이지 | detail-page-planner, product-detail |
| 카피 | copywriting |
| 소셜 미디어 | social-media |
| 콘텐츠 캘린더 | content-calendar |
| HTML 리포트 | html-report |
| 유튜브·팟캐스트 기획 | youtube-podcast-planner |
| 한국어 윤문·맞춤법 | humanize-korean, korean-spell-check |
| 미디어 제작 | media-production |

### moai-operations
| 키워드 | 스킬 |
|--------|------|
| 운영 프로세스, SOP | process-manager |
| 상태보고 | status-reporter |
| 벤더·조달 관리 | vendor-manager |

### moai-education
| 키워드 | 스킬 |
|--------|------|
| 강의 운영매뉴얼 | course-operations-manual |
| 후기 시퀀스 | course-followup-sequence |
| 교육과정 설계 | curriculum-designer |
| 시험출제, 평가 | assessment-creator |
| 교육 리서치 | research-assistant |

### moai-lifestyle
| 키워드 | 스킬 |
|--------|------|
| 여행 | travel-planner |
| 건강, 웰니스 | wellness-coach |
| 이벤트, 웨딩 | event-planner |

### moai-product
| 키워드 | 스킬 |
|--------|------|
| 로드맵 | roadmap-manager |
| 제품 스펙, PRD | spec-writer |
| UX 디자인 | ux-designer |
| UX 리서치 | ux-researcher |

### moai-support
| 키워드 | 스킬 |
|--------|------|
| 티켓 분류 | ticket-triage |
| 응답 초안 | draft-response |
| KB 문서 | kb-article |
| 에스컬레이션 | escalation-manager |

### moai-office
| 키워드 | 스킬 |
|--------|------|
| PPT, 발표자료 | pptx-designer |
| 한글, hwpx | hwpx-writer |
| Word, docx | docx-generator |
| Excel, xlsx | xlsx-creator |
| PDF | pdf-writer |
| NotebookLM 슬라이드 프롬프트 | notebooklm-slide-prompt |

### moai-career
| 키워드 | 스킬 |
|--------|------|
| 이력서, 자기소개서 | resume-builder |
| 면접 코칭 | interview-coach |
| 채용공고 분석 | job-analyzer |
| 포트폴리오 | portfolio-guide |

### moai-data
| 키워드 | 스킬 |
|--------|------|
| CSV/Excel 탐색 | data-explorer |
| 차트, 시각화, 대시보드 | data-visualizer |
| 공공데이터 | public-data |

### moai-public-data
| 키워드 | 스킬 |
|--------|------|
| 주식 시세, KRX | korean-stock-search |
| 법원경매 | court-auction-search |
| 부동산 실거래가 | real-estate-search |
| 공공데이터 조회 | public-data |

### moai-research
| 키워드 | 스킬 |
|--------|------|
| 논문 검색 | paper-search |
| 논문 작성 | paper-writer |
| 특허 검색 | patent-search |
| 특허 분석 | patent-analyzer |
| 연구비, 과제 신청서 | grant-writer |

### moai-media
| 키워드 | 스킬 |
|--------|------|
| AI 이미지 생성 | higgsfield-image |
| AI 영상 생성(Kling 모델 포함) | higgsfield-video |
| 음성, TTS, 더빙 | audio-gen |
| 이미지 프롬프트 빌더 | gemini-3-image-prompt, gpt-image-2-prompt, midjourney-v8-prompt |

### moai-commerce
| 키워드 | 스킬 |
|--------|------|
| 상품명, 상세페이지 카피 | commerce-product-naming, detail-page-copy |
| 상세페이지 이미지·상품 사진 | detail-page-image, product-photo-brief, commerce-product-image-pipeline |
| 마켓플레이스(네이버·쿠팡·D2C·크라우드펀딩) | marketplace-naver, marketplace-coupang, marketplace-d2c, marketplace-crowdfunding, marketplace-curation |
| 쿠팡 광고 | coupang-ad-optimizer, marketplace-coupang-ads |
| 시장조사, JTBD 페르소나 | commerce-market-research, commerce-jtbd-persona |
| 통합 전략, 시즌 캘린더, 프로모션 | commerce-integrated-strategy, commerce-season-calendar, commerce-promotion-planner |
| 마진·LTV·구독 | commerce-margin-calculator, commerce-ltv-cac-architect, commerce-subscription-strategist, commerce-repurchase-timer |
| 초기 팬·인플루언서·채널 메시지 | commerce-early-fan-builder, commerce-influencer-collab, commerce-channel-message |
| 라이브 커머스 | live-commerce |
| VOC, 운영 자동화 진단, 모닝 브리프 | commerce-voc-triage, commerce-automation-audit, commerce-morning-brief |
| 식약처·마케팅 표시 컴플라이언스 | mfds-safety, commerce-marketing-compliance-kr |

### moai-bi
| 키워드 | 스킬 |
|--------|------|
| 경영진 1pager 요약 | executive-summary |

### moai-pm
| 키워드 | 스킬 |
|--------|------|
| 주간 업무보고, WBR | weekly-report |

### moai-sales
| 키워드 | 스킬 |
|--------|------|
| B2B 제안서, RFP 대응 | proposal-writer |

### moai-book
| 키워드 | 스킬 |
|--------|------|
| 책 컨셉 기획 | book-concept-planner |
| 목차 설계 | book-outline-designer |
| 챕터 집필 | book-chapter-writer |
| 퇴고 코칭 | book-revision-coach |
| 출간 제안서 | book-proposal-writer |
| 저자 소개, 타깃 독자 | book-author-bio, book-target-reader |
| 출판사 매칭 | book-publisher-matcher |

### moai-design
| 키워드 | 스킬 |
|--------|------|
| design-brief 작성 | claude-design-brief |
| 디자인 시스템 준비 | claude-design-system-prep |
| 프롬프트 빌더 | claude-design-prompt-builder |
| 핸드오프 리더 | claude-design-handoff-reader |
| 디자인 슬롭 점검 | claude-design-slop-check |

### moai-wealth
| 키워드 | 스킬 |
|--------|------|
| 가계부, 소비관리 | household-budget |
| 투자 입문 | invest-primer |
| 재무 로드맵, 종잣돈 | wealth-roadmap |
| 보험 | insurance-fit |
| 절세 | personal-tax-saver |
| 경제 리터러시 | econ-literacy |

### moai-productivity
| 키워드 | 스킬 |
|--------|------|
| 회고 | retro-builder |
| 목표관리, OKR, 만다라트 | goal-planner |
| 시간관리 | time-system |
| 습관, 루틴 | habit-routine |
| 노션 템플릿 | notion-template-kit |
| 주간 회고/계획 | weekly-report |
| 셀프케어 | self-care |

### moai-comms
| 키워드 | 스킬 |
|--------|------|
| 보고, 발표 화법 | report-speak |
| 회의 퍼실리테이션, 회의록 | meeting-facilitator |
| 피드백 | feedback-loop |
| 갈등 | conflict-handler |
| 협상, 1on1 | negotiation-1on1 |

---

## 5. 모호성 해소

키워드 매칭 결과 후보가 2개 이상일 때:

### 5.1 자동 해소
- 산출물 유형이 명시되면 해당 산출물을 만드는 스킬 우선
- 예: "인스타 카드뉴스 만들어줘" → moai-content:card-news

### 5.2 사용자 확인
AskUserQuestion (1질문, 후보 플러그인 최대 4개) ✅

```
"어떤 작업을 원하시나요?"
○ {후보1 플러그인명} — {설명}
○ {후보2 플러그인명} — {설명}
+ Other
```

---

## 6. 복합 요청 처리

사용자 요청이 2개+ 플러그인 또는 스킬에 걸칠 때:

### 6.1 순차 처리 (스킬 체인)
```
"사업계획서 쓰고 PPT로 만들어줘"
→ moai-business:startup-launchpad → moai-office:pptx-designer → moai-core:ai-slop-reviewer
```

### 6.2 병렬 처리
```
"인스타 카드뉴스랑 블로그 포스트 만들어줘"
→ moai-content:card-news + moai-content:blog
   (각각 마무리 단계에 ai-slop-reviewer 적용)
```

### 6.3 심층 분석 판단
복합 요청이거나 2개+ 플러그인이 관여하면:
→ ultrathink(심층 분석)으로 최적 스킬 체인 경로를 결정

### 6.4 검증 깊이 연동

라우팅과 함께 **검증 깊이 등급**도 정한다 (상세: execution-protocol.md §6-4):
- 법률·계약·NDA·개인정보·세무·재무·정부지원·공고·의료·규제 키워드, 또는 2개+ 플러그인 체인 → **DEEP** (근거 게이트 + 면책 + 전달 전 확인)
- 일반 산출물(보고서·카피·문서) → **NORMAL** (근거 게이트 활성)
- 단순 조회·요약 → **QUICK** (근거 게이트 스킵)

키워드는 seed일 뿐이며, 트리거 단어 없이 표현된 고위험 요청도 맥락으로 DEEP 판단한다.

### 6.5 코디네이터 에이전트 우선 라우팅 (agent-aware)

플러그인 라우팅 후, 요청이 특정 도메인의 다단계 워크플로우면 **매칭되는 코디네이터 에이전트로 우선 위임**한다 (상세: `agent-catalog.md`):
- 매칭 코디네이터 존재 + 워크플로우 일치 → 코디네이터 에이전트 호출 (예: "사업계획서 만들어줘" → `business-plan-coordinator`)
- 매칭 없음 / 단순 1-2단계 → 인라인 스킬 체인
- 코디네이터는 Cowork 서브에이전트 전용 (Bash·WebFetch 미동작 — 해당 단계는 부모 세션이 수행)

---

## 7. 폴백 전략

| 상황 | 대응 |
|------|------|
| 키워드 매칭 0개 | AskUserQuestion으로 카테고리 직접 질문 |
| 플러그인 트리거 실패 | moai-core가 직접 적합 스킬을 탐색하여 실행 |
| 적합 스킬 단정 어려움 | 후보 스킬을 AskUserQuestion으로 제시 후 선택 |

---

## 8. 버전 정보

27개 플러그인 / 173 스킬 단위 라우팅. **플러그인 → 스킬(또는 스킬 체인) 모델**.
키워드 매칭으로 플러그인을 고르고, 해당 플러그인의 실제 스킬명으로 라우팅한다. 별도의 실행 모듈 계층은 없다.
