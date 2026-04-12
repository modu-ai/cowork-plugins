# cowork-plugins

Claude Cowork 도메인 전문가 AI 마켓플레이스.

16개 독립 플러그인 64개 스킬로 비즈니스 전략, 마케팅, 법률, 재무, 인사, 콘텐츠, 운영, 교육, 라이프스타일, 제품, 고객지원, 문서생성, 데이터 분석, 연구/특허를 지원합니다.

## 플러그인 카탈로그

| 플러그인 | 설명 | 스킬 수 |
|---------|------|:-------:|
| [moai-core](./moai-core/) | 도메인 AI 라우터, 초기화, 자가학습 엔진 | 1 |
| [moai-business](./moai-business/) | 사업계획서, 시장조사, 재무모델, 투자제안서 | 4 |
| [moai-marketing](./moai-marketing/) | 기업/개인 브랜딩, SEO, SNS, 캠페인, 이메일 시퀀스, 퍼포먼스 | 7 |
| [moai-legal](./moai-legal/) | 계약서 검토, 컴플라이언스, NDA, 지적재산권 | 4 |
| [moai-finance](./moai-finance/) | 원천징수, 부가세, K-IFRS, 결산, 예산 분석 | 4 |
| [moai-hr](./moai-hr/) | 근로계약서, 4대보험, 채용, 성과평가 | 4 |
| [moai-content](./moai-content/) | 카드뉴스, 상세페이지, 랜딩페이지, 뉴스레터, 카피라이팅, 블로그, 소셜미디어 | 8 |
| [moai-operations](./moai-operations/) | 결재, 조달, SOP, 벤더 관리, 상태 보고 | 3 |
| [moai-education](./moai-education/) | 강의설계, 논문, 교육과정, 시험 출제 | 3 |
| [moai-lifestyle](./moai-lifestyle/) | 여행, 건강, 웨딩/이벤트 | 3 |
| [moai-product](./moai-product/) | PM 로드맵, UX 리서치, 스펙, AI 전략 | 3 |
| [moai-support](./moai-support/) | 티켓 분류, KB 문서, 에스컬레이션 | 4 |
| [moai-office](./moai-office/) | PPT, DOCX, XLSX, HWPX 문서 생성 | 4 |
| [moai-career](./moai-career/) | 커리어 준비 — 자기소개서, 이력서, 면접 코칭, 채용공고 분석 | 4 |
| [moai-data](./moai-data/) | 데이터 분석 — CSV/Excel 탐색, 공공데이터, 시각화 | 3 |
| [moai-research](./moai-research/) | 연구/특허 — 논문 검색, 특허 분석/출원, 연구비 신청 | 5 |

## 총 산출물

| 항목 | 수량 |
|------|:----:|
| 플러그인 | 16 |
| 스킬 | 64 |
| 레퍼런스 파일 | 167 |
| 에이전트 | 7 |
| MCP 서버 | 5 |
| 스크립트 | 16 |
| 템플릿 | 8 |

## 설치 방법

### Step 1: 마켓플레이스 추가

Claude Cowork에서 GitHub 레포 주소를 입력하여 플러그인 마켓플레이스를 추가합니다.

1. Claude Cowork 좌측 메뉴 > **사용자 지정** 클릭
2. 개인 플러그인 영역에서 **+** 버튼 클릭
3. **플러그인 생성** > **마켓플레이스 추가** 선택
4. URL 입력란에 아래 주소 입력 후 **동기화** 클릭:

```
modu-ai/cowork-plugins
```

![마켓플레이스 추가](docs/setup-1.png)
![URL 입력](docs/setup-2.png)

### Step 2: 플러그인 설치

동기화가 완료되면 16개 플러그인 목록이 표시됩니다.

1. **개인** 탭 선택 → **cowork-plugins** 마켓플레이스 확인
2. 원하는 플러그인 옆의 **+** 버튼으로 설치
3. **moai-core**를 반드시 먼저 설치 (라우터/오케스트레이터)
4. 이후 필요한 도메인 플러그인 추가 설치

![플러그인 목록](docs/setup-3.png)

### Step 3: 프로젝트 생성

플러그인 설치 후 Cowork 프로젝트를 생성합니다.

1. 좌측 메뉴 > **프로젝트** > **+ 새 프로젝트** 클릭
2. **처음부터 시작하기** 선택
3. 프로젝트 이름 입력 (예: "youtube 콘텐츠 기획")
4. 프로젝트 위치 선택 → **만들기** 클릭

![프로젝트 생성](docs/projec-1.png)
![프로젝트 설정](docs/projec-2.png)

### Step 4: `/moai init` 으로 초기화

프로젝트 생성 후 채팅창에서 MoAI를 초기화합니다.

```
/moai init
```

1. **Phase 1**: 분야 선택 (비즈니스/마케팅/관리/기술 중 택 1)
2. **Phase 2**: 설치된 플러그인 중 주로 사용할 플러그인 선택 (복수 선택 가능)
3. **Phase 3**: 커넥터 연결 + API 키 등록 (선택)
4. **Phase 4**: 프로젝트 맞춤형 CLAUDE.md 자동 생성

![MoAI 초기화](docs/projec-3.png)

약 3분 내 완료. 이후 자연어로 요청하면 자동 라우팅됩니다:

```
"사업계획서 써줘"        → moai-business
"PPT 만들어줘"           → moai-office
"계약서 검토해줘"        → moai-legal
"세금 계산해줘"          → moai-finance
"카드뉴스 만들어줘"      → moai-content
"데이터 분석해줘"        → moai-data
"특허 찾아줘"            → moai-research
```

## 플러그인 상세 소개

### moai-core — 오케스트레이터

자연어 요청을 분석하여 16개 도메인 플러그인 중 적합한 스킬로 자동 라우팅합니다. `/moai init`으로 프로젝트를 초기화하고, `/moai catalog`으로 설치된 스킬 목록을 조회합니다.

- 소크라테스 인터뷰로 사용자 의도를 정확히 파악한 뒤 계획을 수립하고 실행합니다
- 산출물 품질 검증 루프(파일 유효성 → 내용 완전성 → AI 슬롭 검수)를 자동 수행합니다
- 공유 에이전트: `quality-evaluator` (전 플러그인에서 호출 가능)

---

### moai-business — 비즈니스 전략

| 스킬 | 기능 |
|------|------|
| strategy-planner | 사업계획서, 스타트업 런처, 비즈니스 모델 캔버스, SWOT/Porter 분석 |
| market-analyst | 시장조사(TAM/SAM/SOM), 경쟁사 분석, 가격 전략 |
| investor-relations | 투자 제안서(IR), 재무모델, 매출 예측 |
| daily-briefing | 일일 비즈니스 브리핑, 시장 동향 요약 |

DART MCP 서버로 기업 공시/재무제표를 실시간 조회합니다.

---

### moai-marketing — 마케팅

| 스킬 | 기능 |
|------|------|
| brand-identity | 기업 브랜딩 풀 파이프라인 — 네이밍, 슬로건, 톤앤매너, 비주얼 가이드 |
| personal-branding | 개인 브랜딩 — 자기 분석, 포지셔닝, 채널별 콘텐츠 전략 |
| sns-content | 네이버 블로그, 인스타그램, 카카오 채널 최적화 콘텐츠 |
| campaign-planner | A/B 테스트, 그로스 해킹, 인플루언서 전략, CRM |
| seo-audit | 네이버/구글/AI검색(GEO) 통합 SEO 감사, C-Rank 개선 |
| email-sequence | 정보통신망법 준수 이메일 시퀀스, 드립 캠페인 |
| performance-report | 마케팅 성과 대시보드, KPI 리포트 |

---

### moai-legal — 법률

| 스킬 | 기능 |
|------|------|
| contract-review | 계약서 위험 조항 검토 (민법/상법 기반) |
| compliance-check | 개인정보보호법, ESG, 규제 컴플라이언스 점검 |
| legal-risk | 법적 리스크 분석, 쟁점 정리 |
| nda-triage | NDA/비밀유지계약서 초안 및 검토 |

korean-law MCP로 법령/판례를 실시간 검색합니다.

---

### moai-finance — 재무/세무

| 스킬 | 기능 |
|------|------|
| tax-helper | 3.3% 원천징수, 부가세, 종합소득세, 홈택스 신고 안내 |
| financial-statements | K-IFRS 재무제표 분석, 재무비율 계산 |
| close-management | 월/분기/연 결산 체크리스트, 마감 관리 |
| variance-analysis | 예산 대비 실적 분석, 차이 원인 진단 |

---

### moai-hr — 인사/노무

| 스킬 | 기능 |
|------|------|
| employment-manager | 근로계약서, 4대보험, 연차/퇴직금 계산 |
| people-operations | 온보딩 프로세스, 조직 관리, 인사 규정 |
| draft-offer | 오퍼 레터, 채용 공고(JD) 작성 |
| performance-review | 성과 평가 양식, MBO/OKR 설계 |

---

### moai-content — 콘텐츠

| 스킬 | 기능 |
|------|------|
| card-news | AI 이미지(Nano Banana) 기반 인스타 캐러셀 제작 |
| product-detail | 전환율 극대화 상세페이지 — 네이버/쿠팡/카카오 규격 |
| landing-page | 고전환율 랜딩 페이지 설계, CTA 최적화 |
| copywriting | 마케팅 카피, 헤드라인, 광고 문구, 비주얼 스토리텔링 |
| newsletter | 뉴스레터 기획~발행, 구독자 확보, 오픈율 최적화 |
| media-production | 유튜브 스크립트, Remotion 영상, 팟캐스트 기획 |
| blog | SEO 블로그 글 작성, 시리즈 기획, 내부 링크 전략 |
| social-media | 멀티 채널 소셜 콘텐츠, 캘린더, 해시태그 전략 |

WordPress/Canva 커넥터로 직접 발행 가능합니다.

---

### moai-operations — 운영

| 스킬 | 기능 |
|------|------|
| process-manager | 결재 프로세스 설계, 나라장터 조달, SOP 작성 |
| vendor-manager | 벤더 평가, 발주/구매 관리, 계약 조건 검토 |
| status-reporter | KPI 보고서, 주간/월간 상태 보고 |

---

### moai-education — 교육/연구

| 스킬 | 기능 |
|------|------|
| curriculum-designer | 온라인/오프라인 강의 설계, 커리큘럼 개발 |
| research-assistant | 문헌 검토, 리서치 보고서, 데이터 수집/분석 |
| assessment-creator | 시험 문제 출제, 자격증 대비, 평가 루브릭 |

---

### moai-lifestyle — 라이프스타일

| 스킬 | 기능 |
|------|------|
| travel-planner | 여행 일정 설계, 맛집/숙소 추천, 예산 계획 |
| wellness-coach | 식단 설계, 운동 프로그램, 건강 관리 |
| event-planner | 웨딩/세미나/이벤트 기획, 체크리스트, 타임라인 |

---

### moai-product — 제품/혁신

| 스킬 | 기능 |
|------|------|
| spec-writer | PRD/기능명세서 작성, 스프린트 플래닝 |
| roadmap-manager | 제품 로드맵, 마일스톤 관리, 릴리스 계획 |
| ux-researcher | UX 리서치, 페르소나 설계, 사용성 테스트 |

---

### moai-support — 고객지원

| 스킬 | 기능 |
|------|------|
| ticket-triage | CS 티켓 자동 분류, 우선순위 지정 |
| draft-response | 고객 응대 초안 작성 (격식/캐주얼 톤) |
| kb-article | Knowledge Base 문서 작성, FAQ 정리 |
| escalation-manager | 에스컬레이션 판단, 상위 레벨 보고서 |

---

### moai-office — 문서 생성

| 스킬 | 기능 |
|------|------|
| hwpx-writer | 한글(HWPX) 공문서/보고서 생성, 양식 채우기 (python-hwpx) |
| docx-generator | Word(DOCX) 보고서/계약서/제안서 생성 |
| pptx-designer | PPT 발표자료 디자인 (pptxgenjs, Pretendard 폰트) |
| xlsx-creator | Excel 데이터 표/차트/수식/조건부 서식 (openpyxl) |

Word/PPT/Excel/한글 생성 요청 시 Claude 기본 도구 대신 이 플러그인을 우선 사용합니다.

---

### moai-career — 커리어

| 스킬 | 기능 |
|------|------|
| resume-builder | 자기소개서/이력서/CV 작성, 산업별 맞춤 |
| interview-coach | 면접 예상 질문, 모의면접, STAR 기법 코칭 |
| job-analyzer | 채용공고(JD) 분석, 역량 매칭, 지원 전략 |
| portfolio-guide | 포트폴리오 구성, 프로젝트 어필 포인트 정리 |

---

### moai-data — 데이터 분석

| 스킬 | 기능 |
|------|------|
| data-explorer | CSV/Excel 프로파일링, 이상값 탐지, 상관 분석 |
| data-visualizer | Mermaid/Chart.js 차트, HTML 대시보드, PPT/Word 변환 |
| public-data | 공공데이터포털/KOSIS 통계 실시간 조회 |

Airtable/Google Sheets 커넥터로 데이터를 직접 분석합니다.

---

### moai-research — 연구/특허

| 스킬 | 기능 |
|------|------|
| paper-search | RISS/KCI/DBpia/Google Scholar 논문 통합 검색 |
| paper-writer | 학술 논문 구조화 작성 (APA/KCI/IEEE 포맷) |
| patent-search | KIPRIS Plus 특허/실용신안/디자인/상표 검색 |
| patent-analyzer | 특허 맵, 선행기술 조사, FTO 분석, 출원서 초안 |
| grant-writer | NRF/IITP/KIAT 연구비 신청서 작성 |

---

## 에이전트 공유 호출

플러그인 간 에이전트를 공유 호출할 수 있습니다:

| 에이전트 | 소속 | 공유 대상 |
|---------|------|----------|
| quality-evaluator | moai-core | 전 플러그인 |
| market-researcher | moai-business | moai-product 등 |
| content-creator | moai-marketing | moai-business 등 |
| compliance-checker | moai-legal | moai-finance, moai-hr 등 |
| korean-tone-reviewer | moai-hr | moai-support, moai-business 등 |
| document-generator | moai-office | moai-business, moai-legal 등 |
| format-converter | moai-office | 전 플러그인 |

## 기술 특징

**Anthropic 공식 스킬 가이드 준수**
- 모든 64개 스킬에 [What]+[When]+[Triggers] 구조의 description 적용
- Negative triggers로 불필요한 스킬 로딩 방지
- 인라인 폴백과 에러 핸들링 내장

**Agency 패턴 적용 (moai-content/landing-page)**
- JSON 카피 계약 기반 자동화된 페이지 생성
- 디자인 시스템 스펙과 브랜드 컨텍스트 템플릿
- 평가 체크리스트와 A/B 테스트 가이드

**2026년 최신 법규/시장 데이터 반영**
- 개정 개인정보보호법, 근로기준법, 세법 변경사항
- 네이버 C-Rank, GEO, 카카오모먼트 등 플랫폼 알고리즘
- K-IFRS 제1118호, 4대보험 요율, 최저임금 기준

## 오픈소스 및 참고자료

### Python 라이브러리
| 패키지 | 용도 | 라이센스 | 플러그인 |
|--------|------|---------|---------|
| [python-hwpx](https://github.com/airmang/python-hwpx) | HWPX 문서 생성/편집 | Custom (비상업) | moai-office |
| [openpyxl](https://openpyxl.readthedocs.io/) | Excel(XLSX) 생성/편집 | MIT | moai-office |
| [python-docx](https://python-docx.readthedocs.io/) | Word(DOCX) 생성/편집 | MIT | moai-office |
| [python-pptx](https://python-pptx.readthedocs.io/) | PPT(PPTX) 생성/편집 | MIT | moai-office |
| [olefile](https://olefile.readthedocs.io/) | HWP 바이너리 추출 | BSD | moai-office |
| [lxml](https://lxml.de/) | XML 파싱 | BSD | moai-office |

### JavaScript/TypeScript
| 패키지 | 용도 | 라이센스 | 플러그인 |
|--------|------|---------|---------|
| [pptxgenjs](https://gitbrent.github.io/PptxGenJS/) | PPT 슬라이드 생성 | MIT | moai-office |
| [Remotion](https://www.remotion.dev/) | 영상 제작 프레임워크 | Business Source | moai-content |
| [Deno](https://deno.land/) | TypeScript 런타임 | MIT | moai-office |

### MCP 서버 (커스텀)
| 서버 | 소스 | 용도 | 플러그인 |
|------|------|------|---------|
| [DART-mcp-server](https://github.com/snaiws/DART-mcp-server) | 오픈소스 | 기업 공시 조회 | moai-business |
| [korean-law-mcp](https://korean-law-mcp.fly.dev/) | 커뮤니티 | 법령/판례 검색 | moai-legal |
| [WordPress MCP](https://mcp.wordpress.com/) | 공식 | 블로그 발행 | moai-content |

### 공공 API
| API | URL | 용도 | 플러그인 |
|-----|-----|------|---------|
| DART OpenAPI | [opendart.fss.or.kr](https://opendart.fss.or.kr/) | 기업 공시/재무제표 | moai-business |
| 공공데이터포털 | [data.go.kr](https://www.data.go.kr/) | 공공데이터 조회 | moai-data |
| KOSIS | [kosis.kr](https://kosis.kr/) | 통계청 데이터 | moai-data |
| KIPRIS Plus | [plus.kipris.or.kr](https://plus.kipris.or.kr/) | 특허 검색 | moai-research |
| KCI | [kci.go.kr](https://www.kci.go.kr/) | 논문 검색 | moai-research |
| 국가법령정보 | [law.go.kr](https://www.law.go.kr/) | 법령/판례 | moai-legal |
| Nano Banana | [ai.google.dev](https://ai.google.dev/) | AI 이미지 생성 | moai-content |

### 표준 및 규격
| 표준 | 설명 |
|------|------|
| [OWPML (KS X 6101)](https://www.hancom.com/support/downloadCenter/hwpOwpml) | 개방형 워드프로세서 마크업 언어 (HWPX 기반) |
| [OOXML (ISO/IEC 29500)](https://www.iso.org/standard/71691.html) | Office Open XML (DOCX/PPTX/XLSX 기반) |
| [ODF](https://www.oasis-open.org/) | Open Document Format (HWPX manifest 기반) |

## 라이선스

MIT
