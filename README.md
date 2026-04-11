# moai-cowork-plugins

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

### 방법 1: GitHub 레포 URL로 설치 (권장)

Claude Cowork에서 GitHub 레포 주소를 직접 입력하여 전체 마켓플레이스를 설치합니다.

1. **Claude Cowork** 실행
2. 좌측 메뉴 > **커스터마이즈** (Customize) > **Plugins**
3. **마켓플레이스 추가** (Add Marketplace) 클릭
4. 아래 GitHub 레포 URL 입력:
   ```
   https://github.com/modu-ai/moai-cowork-plugins
   ```
5. **추가** 클릭 → 16개 플러그인 목록 표시
6. 원하는 플러그인 선택 → **Install** 클릭
7. 설치 완료 후 `/moai init` 실행으로 초기 설정

### 방법 2: 개별 플러그인 로컬 업로드

특정 플러그인만 설치하려면 `.zip` 파일로 직접 업로드합니다.

1. [Releases](https://github.com/modu-ai/moai-cowork-plugins/releases)에서 원하는 플러그인 `.zip` 다운로드
2. Cowork > **커스터마이즈** > **Plugins** > **로컬 플러그인 업로드**
3. `.zip` 파일 선택 → **업로드**

### 필수 설치 순서

1. **moai-core** (필수, 오케스트레이터/라우터)
2. 필요한 도메인 플러그인 (moai-business, moai-office 등)
3. `/moai init` 실행 → 프로필 + 커넥터 + API 키 설정

### 첫 실행

설치 완료 후 아무 프로젝트 폴더에서:
```
/moai init
```
- Phase 1: 분야 선택 (1질문)
- Phase 2: 플러그인 선택 (multiSelect)
- Phase 3: 커넥터 + API 키 등록
- Phase 4: 맞춤형 CLAUDE.md 생성

약 3분 내 완료. 이후 자연어로 요청하면 자동 라우팅됩니다:
```
"사업계획서 써줘"        → moai-business
"PPT 만들어줘"           → moai-office
"계약서 검토해줘"        → moai-legal
"세금 계산해줘"          → moai-finance
"카드뉴스 만들어줘"      → moai-content
```

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
