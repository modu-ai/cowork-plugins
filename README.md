# cowork-plugins

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Cowork](https://img.shields.io/badge/Claude-Cowork-blueviolet)](https://claude.ai)
[![Version](https://img.shields.io/badge/Version-1.6.0-blue)](CHANGELOG.md)
[![Plugins](https://img.shields.io/badge/Plugins-17-blue)](.claude-plugin/marketplace.json)
[![Skills](https://img.shields.io/badge/Skills-85-green)](.claude-plugin/marketplace.json)
[![Docs](https://img.shields.io/badge/Docs-cowork.mo.ai.kr-orange)](https://cowork.mo.ai.kr/)
[![shadcn/ui](https://img.shields.io/badge/UI-shadcn/ui-black)](https://ui.shadcn.com/)

**Claude Cowork 도메인 전문가 AI 마켓플레이스**

자연어 한 줄이면 사업계획서, 계약서 검토, 세금 계산, PPT 제작, 데이터 분석, 특허 검색, **AI 이미지·영상·음성 생성**, **shadcn/ui 기반 랜딩·상세 페이지 제작**, **소상공인 상권분석·정부지원사업 신청**까지 — 17개 독립 플러그인과 84개 전문 스킬이 업무를 대신합니다. 모든 텍스트 산출물은 **`ai-slop-reviewer`가 AI 패턴을 검수**하여 사람이 쓴 것처럼 자연스럽게 다듬어 드립니다.

> *Domain expert AI marketplace for [Claude Cowork](https://claude.ai). 17 plugins · 85 skills covering business strategy, marketing, legal, finance, HR, content, operations, education, lifestyle, product, support, document generation (DOCX/PPTX/XLSX/HWPX/**multilingual PDF**), data analysis, research/patents, **AI media production (image/video/voice)**, **shadcn/ui-based web landing/detail pages**, **small-business commercial-area analysis & Korean government grant applications**, and automatic AI-slop detection for every text deliverable.*

**🆕 v1.6.0 하이라이트**
- **`moai-office:pdf-writer` 신규 스킬** — PyMuPDF + Noto Sans CJK로 **한·중·일·영 4개 언어 PDF**를 깨짐 없이 생성. Markdown / 구조화 JSON / HTML / 일반 텍스트 4종 입력 지원. 폰트 64MB는 저장소 미포함, 최초 실행 시 `notofonts/noto-cjk` 공식 저장소에서 자동 다운로드(SIL OFL 1.1)
- **`skill-forge` → `skill-builder` 이름 변경** — 의미 명확화. 별칭 없이 즉시 대체. 외부에서 `skill-forge`를 직접 호출하던 경우 `skill-builder`로 변경 필요
- **`skill-tester` self-contained 화** — 4차원 스코어링 루브릭(Correctness/Completeness/Clarity/Efficiency) + 체인 검증 프로토콜을 SKILL.md 본문에 흡수. 한 번 로드로 모든 평가 기준 즉시 가용
- README Skills 배지 73 → **85** (skill-builder + pdf-writer 반영)
- [릴리스 노트](https://github.com/modu-ai/cowork-plugins/releases/tag/v1.6.0) · [한국어 문서 사이트](https://cowork.mo.ai.kr/)

**v1.5.1 하이라이트**
- **한국어 문서 사이트 정식 오픈** — [cowork.mo.ai.kr](https://cowork.mo.ai.kr/) (Hugo + Geekdoc). Cookbook 28편 + Cowork 입문/FAQ/용어집 수록
- **저장소 위생 강화** — `.gitignore`에 maintainer workspace 차단 블록 추가
- [릴리스 노트](https://github.com/modu-ai/cowork-plugins/releases/tag/v1.5.1) · [한국어 문서 사이트](https://cowork.mo.ai.kr/)

**v1.5.0 하이라이트**
- **`moai-business`에 소상공인·창업자용 스킬 2종 추가** — 스킬 수 71 → **73**, Breaking change 없음
- **`sbiz365-analyst`** — [소상공인365 빅데이터 포털](https://bigdata.sbiz.or.kr) PDF를 분석해 **4축 100점 창업타당성 평가(성장성 30·경쟁도 25·수요 적합도 25·재무 타당성 20)** 와 9섹션 Word(.docx) 보고서 자동 생성
- **`kr-gov-grant`** — K-Startup · BIZINFO · 중기부 · IITP · 문체부 · 농식품부 공고를 **4 MODE(탐색·작성·검토·일정)** 로 통합. 8 신청자 유형 × 7 지원 목적 = 56개 매칭 조합 제공
- `moai-research:grant-writer`(학술·R&D)와 `moai-business:kr-gov-grant`(창업·사업화) **명확히 분리** — 요청 키워드로 자동 라우팅
- [릴리스 노트](https://github.com/modu-ai/cowork-plugins/releases/tag/v1.5.0) · [moai-business 가이드 (온라인 문서)](https://github.com/modu-ai/cowork-plugins/tree/v1.5.0/moai-business)

**이전 릴리스 하이라이트**
- **v1.4.0** — shadcn/ui HTML/웹 산출물 기본 스택(Next.js 15 + Tailwind v4), 소크라테스식 테마 인터뷰, OKLCH CSS 변수 기본, Recharts·Chart.js·Tremor·ECharts 4택 1
- **v1.3.0** — `/moai` → `/project` 커맨드 전환, `ai-slop-reviewer` 도입, 스킬 체이닝 기반 `/project init`, SKILL.md `metadata` 블록 제거

---

## 목차

- [플러그인 카탈로그](#플러그인-카탈로그)
- [총 산출물](#총-산출물)
- [설치 방법](#설치-방법)
- [플러그인 상세 소개](#플러그인-상세-소개)
- [스킬 간 공유 기능](#스킬-간-공유-기능)
- [기술 특징](#기술-특징)
- [오픈소스 및 참고자료](#오픈소스-및-참고자료)
- [기여 가이드](#기여-가이드)
- [문의 및 지원](#문의-및-지원)
- [라이선스](#라이선스)

## 플러그인 카탈로그

| 플러그인 | 설명 | 스킬 수 |
|---------|------|:-------:|
| [moai-core](./moai-core/) | 프로젝트 초기화(`/project init`) + 스킬 체이닝 라우터 + AI 슬롭 검수 + 피드백 | 3 |
| [moai-business](./moai-business/) | 사업계획서, 시장조사, 재무모델, 투자제안서, **소상공인 상권분석**, **정부지원사업 통합** | 6 |
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
| [moai-office](./moai-office/) | PPT, DOCX, XLSX, HWPX, PDF 문서 생성 | 5 |
| [moai-career](./moai-career/) | 커리어 준비 — 자기소개서, 이력서, 면접 코칭, 채용공고 분석 | 4 |
| [moai-data](./moai-data/) | 데이터 분석 — CSV/Excel 탐색, 공공데이터, 시각화 | 3 |
| [moai-research](./moai-research/) | 연구/특허 — 논문 검색, 특허 분석/출원, 연구비 신청 | 5 |
| [moai-media](./moai-media/) 🆕 | AI 미디어 스튜디오 — Nano Banana 이미지, Kling 영상, ElevenLabs 음성, fal.ai 게이트웨이 | 5 |

## 총 산출물

| 항목 | 수량 |
|------|:----:|
| 플러그인 | 17 |
| 스킬 | 84 |
| 레퍼런스 파일 | 180 |
| 에이전트 | 0 |
| MCP 서버 | 7 (`fal-ai`, `elevenlabs` 추가) |
| 스크립트 | 16 |
| 템플릿 | 8 |

## 설치 방법

### Step 1: 마켓플레이스 추가

Claude Cowork에서 GitHub 레포 주소를 입력하여 플러그인 마켓플레이스를 추가합니다.

1. Claude Cowork **좌측 사이드바 > 사용자 지정(Customize)** 클릭
2. **개인 플러그인** 영역에서 **+** 버튼 클릭
3. **플러그인 추가 > 마켓플레이스 추가** 선택
4. URL 입력란에 아래 주소 입력 후 **동기화** 클릭:

```
modu-ai/cowork-plugins
```

![마켓플레이스 추가](docs/setup-1.png)
![URL 입력](docs/setup-2.png)

### Step 2: 플러그인 설치

동기화가 완료되면 17개 플러그인 목록이 표시됩니다.

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

### Step 4: `/project init` 으로 초기화

프로젝트 생성 후 채팅창에서 MoAI를 초기화합니다.

```
/project init
```

1. **Phase 1**: 분야 선택 (비즈니스/마케팅/관리/기술 중 택 1)
2. **Phase 2**: 설치된 플러그인 중 주로 사용할 플러그인 선택 (복수 선택 가능)
3. **Phase 3**: 커넥터 연결 + API 키 등록 (선택)
4. **Phase 4**: 프로젝트 맞춤형 CLAUDE.md 자동 생성

![MoAI 초기화](docs/projec-3.png)

약 3분 내 완료. 이후 자연어로 요청하면 자동 라우팅됩니다:

```
"사업계획서 써줘"        → Skill(strategy-planner) 자동실행
"PPT 만들어줘"           → Skill(pptx-designer) 자동실행
"계약서 검토해줘"        → Skill(contract-review) 자동실행
"세금 계산해줘"          → Skill(tax-helper) 자동실행
"카드뉴스 만들어줘"      → Skill(card-news) 자동실행
"데이터 분석해줘"        → Skill(data-explorer) 자동실행
"특허 찾아줘"            → Skill(patent-search) 자동실행
```

## 플러그인 상세 소개

### moai-core — 오케스트레이터 + 검수 엔진

자연어 요청을 분석하여 16개 도메인 플러그인 중 적합한 스킬로 자동 라우팅합니다. `/project init`으로 워크플로우를 인터뷰하여 **스킬 체인 기반 CLAUDE.md**를 생성하고, `/project catalog`로 설치된 스킬 목록을 조회합니다.

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| project | 프로젝트 초기화 | `/project init` — 워크플로우 인터뷰 → 스킬 체인 설계 → CLAUDE.md 생성, `/project catalog/status/apikey/feedback` |
| ai-slop-reviewer | AI 슬롭 검수 | Claude가 생성한 텍스트의 기계적 패턴(금지어, 획일적 문장 길이, AI식 도입/결말, 수동태 남용)을 진단·수정. **모든 텍스트 산출물 체인의 필수 마지막 단계** |
| feedback | 피드백 | 버그/기능 요청을 GitHub Issues에 자동 등록 (`/project feedback`) |

- 소크라테스 인터뷰로 사용자 의도를 정확히 파악한 뒤 스킬 체인 계획을 수립·확인·실행합니다
- 산출물 품질 검증 루프(파일 유효성 → 내용 완전성 → **AI 슬롭 검수**)를 자동 수행합니다
- CLAUDE.md에 "문서 생성 우선순위(moai-office/content 우선)" + "AI 슬롭 후처리" HARD 규칙을 고정 주입합니다

---

### moai-business — 비즈니스 전략 · 창업

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| strategy-planner | 전략 플래너 | 사업계획서, 스타트업 런처, 비즈니스 모델 캔버스, SWOT/Porter 분석 |
| market-analyst | 시장 분석가 | 시장조사(TAM/SAM/SOM), 경쟁사 분석, 가격 전략 |
| investor-relations | 투자자 관계 | 투자 제안서(IR), 재무모델, 매출 예측 |
| daily-briefing | 일일 브리핑 | 일일 비즈니스 브리핑, 시장 동향 요약 |
| sbiz365-analyst 🆕 | 소상공인 상권분석 | 소상공인365 PDF → 4축 100점 평가 + 9섹션 창업타당성 DOCX 보고서 |
| kr-gov-grant 🆕 | 정부지원사업 통합 | K-Startup·BIZINFO·중기부 등 공고 탐색·신청서 작성·검토·마감 관리 (4 MODE) |

DART MCP 서버로 기업 공시/재무제표를 실시간 조회합니다. `kr-gov-grant`는 창업·사업화·수출·시설 지원사업 전담 — 학술·R&D 연구과제는 `moai-research:grant-writer`를 사용하세요.

---

### moai-marketing — 마케팅

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| brand-identity | 브랜드 아이덴티티 | 기업 브랜딩 풀 파이프라인 — 네이밍, 슬로건, 톤앤매너, 비주얼 가이드 |
| personal-branding | 퍼스널 브랜딩 | 개인 브랜딩 — 자기 분석, 포지셔닝, 채널별 콘텐츠 전략 |
| sns-content | SNS 콘텐츠 | 네이버 블로그, 인스타그램, 카카오 채널 최적화 콘텐츠 |
| campaign-planner | 캠페인 플래너 | A/B 테스트, 그로스 해킹, 인플루언서 전략, CRM |
| seo-audit | SEO 감사 | 네이버/구글/AI검색(GEO) 통합 SEO 감사, C-Rank 개선 |
| email-sequence | 이메일 시퀀스 | 정보통신망법 준수 이메일 시퀀스, 드립 캠페인 |
| performance-report | 성과 리포트 | 마케팅 성과 대시보드, KPI 리포트 |

---

### moai-legal — 법률

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| contract-review | 계약서 검토 | 계약서 위험 조항 검토 (민법/상법 기반) |
| compliance-check | 컴플라이언스 점검 | 개인정보보호법, ESG, 규제 컴플라이언스 점검 |
| legal-risk | 법적 리스크 | 법적 리스크 분석, 쟁점 정리 |
| nda-triage | NDA 검토 | NDA/비밀유지계약서 초안 및 검토 |

korean-law MCP로 법령/판례를 실시간 검색합니다.

---

### moai-finance — 재무/세무

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| tax-helper | 세금 도우미 | 3.3% 원천징수, 부가세, 종합소득세, 홈택스 신고 안내 |
| financial-statements | 재무제표 분석 | K-IFRS 재무제표 분석, 재무비율 계산 |
| close-management | 결산 관리 | 월/분기/연 결산 체크리스트, 마감 관리 |
| variance-analysis | 차이 분석 | 예산 대비 실적 분석, 차이 원인 진단 |

---

### moai-hr — 인사/노무

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| employment-manager | 고용 관리 | 근로계약서, 4대보험, 연차/퇴직금 계산 |
| people-operations | 인사 운영 | 온보딩 프로세스, 조직 관리, 인사 규정 |
| draft-offer | 채용 공고 | 오퍼 레터, 채용 공고(JD) 작성 |
| performance-review | 성과 평가 | 성과 평가 양식, MBO/OKR 설계 |

---

### moai-content — 콘텐츠

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| card-news | 카드뉴스 | AI 이미지(Nano Banana) 기반 인스타 캐러셀 제작 |
| product-detail | 상세페이지 | 전환율 극대화 상세페이지 — 네이버/쿠팡/카카오 규격 |
| landing-page | 랜딩페이지 | 고전환율 랜딩 페이지 설계, CTA 최적화 |
| copywriting | 카피라이팅 | 마케팅 카피, 헤드라인, 광고 문구, 비주얼 스토리텔링 |
| newsletter | 뉴스레터 | 뉴스레터 기획~발행, 구독자 확보, 오픈율 최적화 |
| media-production | 미디어 제작 | 유튜브 스크립트, Remotion 영상, 팟캐스트 기획 |
| blog | 블로그 | SEO 블로그 글 작성, 시리즈 기획, 내부 링크 전략 |
| social-media | 소셜미디어 | 멀티 채널 소셜 콘텐츠, 캘린더, 해시태그 전략 |

WordPress/Canva 커넥터로 직접 발행 가능합니다.

---

### moai-operations — 운영

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| process-manager | 프로세스 관리 | 결재 프로세스 설계, 나라장터 조달, SOP 작성 |
| vendor-manager | 벤더 관리 | 벤더 평가, 발주/구매 관리, 계약 조건 검토 |
| status-reporter | 상태 보고 | KPI 보고서, 주간/월간 상태 보고 |

---

### moai-education — 교육/연구

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| curriculum-designer | 커리큘럼 설계 | 온라인/오프라인 강의 설계, 커리큘럼 개발 |
| research-assistant | 리서치 보조 | 문헌 검토, 리서치 보고서, 데이터 수집/분석 |
| assessment-creator | 평가 출제 | 시험 문제 출제, 자격증 대비, 평가 루브릭 |

---

### moai-lifestyle — 라이프스타일

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| travel-planner | 여행 플래너 | 여행 일정 설계, 맛집/숙소 추천, 예산 계획 |
| wellness-coach | 웰니스 코치 | 식단 설계, 운동 프로그램, 건강 관리 |
| event-planner | 이벤트 플래너 | 웨딩/세미나/이벤트 기획, 체크리스트, 타임라인 |

---

### moai-product — 제품/혁신

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| spec-writer | 스펙 작성 | PRD/기능명세서 작성, 스프린트 플래닝 |
| roadmap-manager | 로드맵 관리 | 제품 로드맵, 마일스톤 관리, 릴리스 계획 |
| ux-researcher | UX 리서치 | UX 리서치, 페르소나 설계, 사용성 테스트 |

---

### moai-support — 고객지원

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| ticket-triage | 티켓 분류 | CS 티켓 자동 분류, 우선순위 지정 |
| draft-response | 응대 초안 | 고객 응대 초안 작성 (격식/캐주얼 톤) |
| kb-article | KB 문서 | Knowledge Base 문서 작성, FAQ 정리 |
| escalation-manager | 에스컬레이션 | 에스컬레이션 판단, 상위 레벨 보고서 |

---

### moai-office — 문서 생성

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| hwpx-writer | 한글 문서 | 한글(HWPX) 공문서/보고서 생성, 양식 채우기 (python-hwpx) |
| docx-generator | 워드 문서 | Word(DOCX) 보고서/계약서/제안서 생성 |
| pptx-designer | PPT 디자인 | PPT 발표자료 디자인 (pptxgenjs, Pretendard 폰트) |
| xlsx-creator | 엑셀 생성 | Excel 데이터 표/차트/수식/조건부 서식 (openpyxl) |
| pdf-writer | PDF 생성 | 한·중·일·영 다국어 PDF 생성 (PyMuPDF + Noto Sans CJK 자동 다운로드) |

Word/PPT/Excel/한글/PDF 생성 요청 시 Claude 기본 도구 대신 이 플러그인을 우선 사용합니다.

---

### moai-career — 커리어

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| resume-builder | 이력서 작성 | 자기소개서/이력서/CV 작성, 산업별 맞춤 |
| interview-coach | 면접 코치 | 면접 예상 질문, 모의면접, STAR 기법 코칭 |
| job-analyzer | 채용 분석 | 채용공고(JD) 분석, 역량 매칭, 지원 전략 |
| portfolio-guide | 포트폴리오 가이드 | 포트폴리오 구성, 프로젝트 어필 포인트 정리 |

---

### moai-data — 데이터 분석

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| data-explorer | 데이터 탐색 | CSV/Excel 프로파일링, 이상값 탐지, 상관 분석 |
| data-visualizer | 데이터 시각화 | Mermaid/Chart.js 차트, HTML 대시보드, PPT/Word 변환 |
| public-data | 공공데이터 | 공공데이터포털/KOSIS 통계 실시간 조회 |

Airtable/Google Sheets 커넥터로 데이터를 직접 분석합니다.

---

### moai-research — 연구/특허

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| paper-search | 논문 검색 | RISS/KCI/DBpia/Google Scholar 논문 통합 검색 |
| paper-writer | 논문 작성 | 학술 논문 구조화 작성 (APA/KCI/IEEE 포맷) |
| patent-search | 특허 검색 | KIPRIS Plus 특허/실용신안/디자인/상표 검색 |
| patent-analyzer | 특허 분석 | 특허 맵, 선행기술 조사, FTO 분석, 출원서 초안 |
| grant-writer | 연구비 신청 | NRF/IITP/KIAT 연구비 신청서 작성 |

### moai-media 🆕 — AI 미디어 스튜디오

| 스킬 | 한글명 | 기능 |
|------|--------|------|
| nano-banana | 나노바나나 | Google Gemini Nano Banana Pro + 2 이미지 생성 (한국어 텍스트 SOTA) |
| ideogram | 아이디오그램 | Ideogram 3.0 한국어 타이포그래피 특화 이미지 (fal.ai) |
| kling | 클링 | Kling 3.0 숏폼 영상 (릴스·쇼츠·틱톡·립싱크, fal.ai) |
| elevenlabs | 일레븐랩스 | AI 음성·TTS·32개 언어 더빙 (공식 MCP) |
| fal-gateway | 팔게이트웨이 | Flux·Recraft·Hailuo·Luma·Pika·MiniMax Music 1000+ 모델 통합 (fal.ai) |

**사용 API 키 3종**: `GEMINI_API_KEY`(Nano Banana), `FAL_KEY`(fal.ai), `ELEVENLABS_API_KEY`.
**번들 MCP 2종**: `fal-ai`(hosted HTTP), `elevenlabs`(local stdio via `uvx`).

---

## 스킬 간 공유 기능

각 스킬의 references에 전문 기능이 포함되어 있으며, CLAUDE.md 생성 시 순차/병렬 실행 지시가 자동으로 작성됩니다.

| 기능 | 소속 스킬 | 공유 대상 |
|------|----------|----------|
| 품질 검증 (PASS/FAIL) | moai-core/project | 전 플러그인 |
| 시장 데이터 수집 | moai-business/market-analyst | moai-product 등 |
| 콘텐츠 생성 | moai-marketing/sns-content | moai-business 등 |
| 컴플라이언스 체크 | moai-legal/compliance-check | moai-finance, moai-hr 등 |
| 경어/톤 검토 | moai-hr/employment-manager | moai-support, moai-business 등 |
| 문서 변환 | moai-office/hwpx-writer | 전 플러그인 |

## 기술 특징

**Anthropic 공식 스킬 가이드 준수**
- 모든 84개 스킬에 [What]+[When]+[Triggers] 구조의 description 적용
- Negative triggers로 불필요한 스킬 로딩 방지
- 인라인 폴백과 에러 핸들링 내장

**Agency 패턴 적용 (moai-content/landing-page)**
- JSON 카피 계약 기반 자동화된 페이지 생성
- 디자인 시스템 스펙과 브랜드 컨텍스트 템플릿
- 평가 체크리스트와 A/B 테스트 가이드

**shadcn/ui 기본 스택 (v1.4.0 신규)**
- `landing-page` / `product-detail` / `data-visualizer` 3개 스킬이 shadcn/ui + Tailwind CSS v4 + OKLCH 토큰을 기본 채택
- 코드 생성 직전 소크라테스식 4문항 인터뷰로 테마·효과·차트 라이브러리 자동 선택
- Light/Dark 모드 동시 산출, 단일 HTML 모드에서도 CSS 변수 인라인 주입
- 공용 레퍼런스: [`moai-content/skills/landing-page/references/landing-page/shadcn-theme-interview.md`](./moai-content/skills/landing-page/references/landing-page/shadcn-theme-interview.md)

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
| Nano Banana | [ai.google.dev/gemini-api/docs/image-generation](https://ai.google.dev/gemini-api/docs/image-generation) | AI 이미지 생성 | moai-content |

### 영감 및 원작

본 프로젝트는 아래 프로젝트에서 영감을 받아 제작되었습니다.

| 프로젝트 | 작성자 | 설명 |
|---------|--------|------|
| [harness-100](https://github.com/revfactory/harness-100) | 황민호(Minho Hwang) | Claude Cowork용 하네스 100개 오픈소스. 본 프로젝트의 하네스 설계 패턴과 구조에 핵심 참고자료로 활용 |
| [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | Anthropic | 공식 11개 지식 노동 플러그인 (Productivity·Sales·Customer Support·PM·Marketing·Legal·Finance·Data·Enterprise Search·Bio Research·Cowork Plugin Management). 플러그인 구조와 스킬 포맷 표준 참고 |

### 표준 및 규격
| 표준 | 설명 |
|------|------|
| [OWPML (KS X 6101)](https://www.hancom.com/support/downloadCenter/hwpOwpml) | 개방형 워드프로세서 마크업 언어 (HWPX 기반) |
| [OOXML (ISO/IEC 29500)](https://www.iso.org/standard/71691.html) | Office Open XML (DOCX/PPTX/XLSX 기반) |
| [ODF](https://www.oasis-open.org/) | Open Document Format (HWPX manifest 기반) |

## 기여 가이드

새 플러그인이나 스킬 추가에 관심이 있다면 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고해 주세요.

버그 리포트나 기능 제안은 [GitHub Issues](https://github.com/modu-ai/cowork-plugins/issues)에 등록해 주세요.

## 문의 및 지원

- GitHub Issues: [modu-ai/cowork-plugins/issues](https://github.com/modu-ai/cowork-plugins/issues)
- Email: email@mo.ai.kr

## 라이선스

[MIT](LICENSE)
