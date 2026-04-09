# router.md — 자연어 → 플러그인 라우팅 프로토콜

## 개요
사용자의 자연어 요청을 분석하여 14개 플러그인 중 적합한 플러그인으로 라우팅하는 프로토콜.
v0.3.0에서는 11개 스킬 그룹 대신 **14개 독립 플러그인** 단위로 라우팅하며, 플러그인 내부에서 하네스/실행 모듈을 선택한다.

---

## 1. 라우팅 흐름

```
사용자 자연어 요청
    ↓
[1단계] .moai/config.json 확인
    ├── 설치된 플러그인 있음 → 해당 플러그인으로 직접 실행
    └── 없음 → [2단계]로
    ↓
[2단계] 키워드 매칭
    ├── 매칭 1개 → 해당 플러그인 트리거
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
- **명시적 도구**: Remotion, HWPX, Imagen, pptxgenjs 등

### 2.2 우선순위 규칙
1. **도구 명시** → 해당 실행 모듈이 있는 플러그인 (최우선)
2. **산출물 유형** → 해당 실행 모듈이 있는 플러그인
3. **도메인 키워드** → 키워드 매핑 테이블
4. **핵심 동사** → 범용 매핑

---

## 3. 키워드 → 플러그인 매핑 테이블

| 키워드 | 플러그인 |
|--------|---------|
| moai, 모아이, 하네스, init, catalog, status, evolve | moai-core |
| 비즈니스, 전략, 사업계획, 스타트업, 창업, 시장조사, 투자, IR, 피칭, 재무모델 | moai-business |
| 마케팅, SEO, SNS, 광고, 블로그, 인스타, 브랜드, CRM, 그로스해킹 | moai-marketing |
| 법률, 계약서, 컴플라이언스, ESG, 지적재산, 특허, 이용약관, 개인정보처리방침 | moai-legal |
| 재무, 세무, 부가세, 홈택스, 3.3%, 종소세, 청구서, 인보이스, 보조금 | moai-finance |
| 인사, 노무, 채용, 퇴직금, 면접, 온보딩, JD | moai-hr |
| 콘텐츠, 카드뉴스, 블로그, 뉴스레터, 유튜브, 팟캐스트, 카피, 광고문구 | moai-content |
| 운영, 결재, 조달, SOP, 매뉴얼, 프로세스, 구매, 발주, 리스크 | moai-operations |
| 교육, 논문, 커리큘럼, 강의, 시험, 자격증, 어학, 리서치 | moai-education |
| 여행, 건강, 웨딩, 이벤트, 맛집, 식단, 운동, 육아, 부동산 | moai-lifestyle |
| 제품, PM, UX, 로드맵, PRD, 프로젝트 트래커, AI전략, 디지털전환 | moai-product |
| 고객지원, CS, 티켓, 응대, VOC, 피드백 분석 | moai-support |
| 문서, PPT, 한글, 엑셀, 보고서, 제안서, 발표자료, hwpx | moai-office |
| 스케줄, 예약, 자동실행, 알림, 반복 작업, 캘린더 | moai-schedules |

---

## 4. 플러그인 상세 키워드

### moai-core
- moai, 모아이, 하네스, init, catalog, status, evolve, profile, doctor

### moai-business
| 키워드 | 하네스 |
|--------|--------|
| 사업계획, 스타트업, 창업, MVP | harness/startup-launcher |
| 시장조사, TAM, SAM, 경쟁분석 | harness/market-research |
| 재무모델, 매출예측, 손익 | harness/financial-modeler |
| 가격전략, 프라이싱, 수익모델 | harness/pricing-strategy |
| 투자, 피칭, IR, 투자유치 | harness/investor-report |
| 경쟁사, 벤치마킹, 포지셔닝 | harness/competitive-analysis |
| 비즈니스 모델, 캔버스, 가치제안 | harness/business-model-canvas |
| 해외 진출, 신시장, GTM | harness/market-entry-strategy |
| 시나리오 플래닝, 불확실성 | harness/scenario-planner |
| SWOT, Porter, OKR, 전략 | harness/strategy-framework |

### moai-marketing
| 키워드 | 하네스 |
|--------|--------|
| SNS, 블로그, 인스타, 네이버, 카카오 | sns-content/guide |
| SEO, 검색엔진최적화 | harness/seo-strategy |
| AI 이미지, 나노바나나, Imagen | imagegen/guide |
| 상세페이지, 쿠팡, 스마트스토어 | product-detail/guide |
| 브랜드, 아이덴티티, CI, BI | harness/brand-identity |
| CRM, 고객관리, 리텐션, LTV | harness/crm-strategy |
| 그로스해킹, 바이럴, 리퍼럴 | harness/growth-hacking |
| 인플루언서, 협찬, 앰배서더 | harness/influencer-strategy |
| A/B 테스트, 실험 설계 | harness/ab-testing |
| 광고 캠페인, 미디어 플랜 | harness/advertising-campaign |

### moai-legal
| 키워드 | 하네스 |
|--------|--------|
| 계약서, 계약 검토, 위험 조항 | contract/guide |
| 컴플라이언스, 규제, 감사 | harness/compliance-checker |
| ESG, 지속가능성 보고 | harness/esg-reporting |
| 법률 리서치, 판례, 쟁점 | harness/legal-research |
| 지적재산, 특허, 상표 | harness/ip-portfolio |
| 인허가, 규제 서류 | harness/regulatory-filing |
| 이용약관, 개인정보처리방침 | harness/service-legal-docs |

### moai-finance
| 키워드 | 하네스 |
|--------|--------|
| 세금, 부가세, 3.3%, 종소세, 홈택스 | tax/guide |
| 청구서, 인보이스, 수금 | harness/invoice-mgmt |
| 보조금, 지원사업, 정부 보조 | harness/grant-writer |
| 수출입, 무역, 통관, HS코드 | harness/import-export |
| 공급망, SCM, 재고 | harness/supply-chain |

### moai-hr
| 키워드 | 하네스 |
|--------|--------|
| 채용, 면접, JD | harness/hiring-pipeline |
| 온보딩, 신입 교육 | harness/onboarding-system |
| 퇴직금, 퇴직, 4대보험 | harness/retirement-calc |
| 직급, 경어, 비즈니스 톤 | harness/tone-guide |

### moai-content
| 키워드 | 하네스 |
|--------|--------|
| 유튜브, 채널, 영상전략 | harness/youtube-production |
| 뉴스레터, 구독자, 메일링 | harness/newsletter-engine |
| 카드뉴스, 캐러셀, 인스타 카드 | card-news/guide |
| 카피, 광고 문구, 슬로건 | harness/copywriting |
| 팟캐스트, 오디오 콘텐츠 | harness/podcast-studio |
| 출판, 전자책, 원고 | harness/book-publishing |

### moai-operations
| 키워드 | 하네스 |
|--------|--------|
| 운영 매뉴얼, 프로세스 | harness/operations-manual |
| SOP, 매뉴얼, 절차서 | harness/sop-writer |
| 조달, 구매, 발주 | harness/procurement-docs |
| 결재, 기안, 품의 | harness/approval-workflow |
| 리스크, 위험 관리 | harness/risk-register |

### moai-education
| 키워드 | 하네스 |
|--------|--------|
| 강의, 커리큘럼, 온라인 교육 | harness/course-builder |
| 시험, 자격증, 수능, 기출 | harness/exam-prep |
| 논문, 학술, 리서치, 문헌검토 | harness/thesis-advisor |
| 학술 논문 작성, 피어 리뷰 | harness/academic-paper |
| 어학, 외국어, 언어학습, 회화 | harness/language-tutor |

### moai-lifestyle
| 키워드 | 하네스 |
|--------|--------|
| 여행, 맛집, 일정 | harness/travel-planner |
| 식단, 다이어트, 건강식 | harness/meal-planner |
| 운동, 피트니스, 헬스 | harness/fitness-program |
| 결혼, 웨딩, 스드메 | harness/wedding-planner |
| 이벤트, 행사, 세미나 | harness/event-organizer |
| 육아, 아이, 교육 | harness/parenting-guide |

### moai-product
| 키워드 | 하네스 |
|--------|--------|
| PM, 로드맵, PRD, 기능명세 | harness/product-manager |
| 프로젝트 트래커, 마일스톤 | harness/project-tracker |
| AI전략, 디지털전환, ML | harness/ai-strategy |
| UX, 유저빌리티, 페르소나 | harness/ux-research |

### moai-support
| 키워드 | 하네스 |
|--------|--------|
| CS, 고객 지원, 응대 | harness/customer-support |
| 티켓, 이슈 트래킹 | harness/ticket-system |
| VOC, 사용자 피드백 | harness/user-feedback-analysis |
| 피드백, 설문, NPS | harness/feedback-analyzer |

### moai-office
| 키워드 | 하네스 |
|--------|--------|
| PPT, 슬라이드, 발표자료 | ppt/guide |
| 한글, hwpx, 아래한글, 한컴 | hwpx/guide |
| 보고서, 주간보고, 기안서 | harness/report-generator |
| 제안서, 견적서, RFP | harness/proposal-writer |
| 회의록, 미팅노트, 안건 | harness/meeting-strategist |
| 엑셀, 스프레드시트 | harness/excel-automation |

### moai-schedules
| 키워드 | 하네스 |
|--------|--------|
| 스케줄, 일정, 예약 | harness/schedule-manager |
| 자동실행, 반복 작업 | harness/task-automation |
| 알림, 리마인더 | harness/reminder-system |
| 캘린더, 구글 캘린더 | harness/calendar-sync |

---

## 5. 모호성 해소

키워드 매칭 결과 후보가 2개 이상일 때:

### 5.1 자동 해소
- 산출물 유형이 명시되면 해당 실행 모듈 우선
- 예: "인스타 카드뉴스 만들어줘" → moai-content (card-news)

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

사용자 요청이 2개+ 플러그인에 걸칠 때:

### 6.1 순차 처리
```
"사업계획서 쓰고 PPT로 만들어줘"
→ moai-business (사업계획서) → moai-office (PPT 변환)
```

### 6.2 병렬 처리
```
"인스타 카드뉴스랑 블로그 포스트 만들어줘"
→ moai-content (카드뉴스) + moai-marketing (블로그)
```

### 6.3 --deepthink 판단
복합 요청이거나 2개+ 플러그인이 관여하면:
→ `mcp__sequential-thinking__sequentialthinking` 호출하여 최적 실행 경로 결정

---

## 7. 폴백 전략

| 상황 | 대응 |
|------|------|
| 키워드 매칭 0개 | AskUserQuestion으로 카테고리 직접 질문 |
| 플러그인 트리거 실패 | moai-core가 직접 하네스 레퍼런스 로드하여 실행 |
| 실행 모듈 없는 작업 | 하네스 전략 가이드만으로 실행 |

---

## 8. 버전 정보

**v0.3.0** (2026-04-09)
- 14개 독립 플러그인 단위 라우팅으로 전환 (11개 스킬 그룹 → 14 plugins)
- 플러그인별 키워드 매핑 테이블 분리
- 모호성 해소 및 폴백 전략 유지
