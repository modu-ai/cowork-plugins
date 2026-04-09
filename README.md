# moai-cowork-plugins

Claude Cowork 도메인 전문가 AI 마켓플레이스.

14개 독립 플러그인 52개 스킬로 비즈니스 전략, 마케팅, 법률, 재무, 인사, 콘텐츠, 운영, 교육, 라이프스타일, 제품, 고객지원, 문서생성, 스케줄 관리를 지원합니다.

## 플러그인 카탈로그

| 플러그인 | 설명 | 스킬 수 |
|---------|------|:-------:|
| [moai-core](./moai-core/) | 도메인 AI 라우터, 초기화, 자가학습 엔진 | 1 |
| [moai-business](./moai-business/) | 사업계획서, 시장조사, 재무모델, 투자제안서 | 4 |
| [moai-marketing](./moai-marketing/) | 네이버/카카오 SEO, SNS, 캠페인, 이메일 시퀀스, 퍼포먼스 | 5 |
| [moai-legal](./moai-legal/) | 계약서 검토, 컴플라이언스, NDA, 지적재산권 | 4 |
| [moai-finance](./moai-finance/) | 원천징수, 부가세, K-IFRS, 결산, 예산 분석 | 4 |
| [moai-hr](./moai-hr/) | 근로계약서, 4대보험, 채용, 성과평가 | 4 |
| [moai-content](./moai-content/) | 카드뉴스, 랜딩페이지, 뉴스레터, 카피라이팅, 블로그, 소셜미디어 | 7 |
| [moai-operations](./moai-operations/) | 결재, 조달, SOP, 벤더 관리, 상태 보고 | 3 |
| [moai-education](./moai-education/) | 강의설계, 논문, 교육과정, 시험 출제 | 3 |
| [moai-lifestyle](./moai-lifestyle/) | 여행, 건강, 웨딩/이벤트 | 3 |
| [moai-product](./moai-product/) | PM 로드맵, UX 리서치, 스펙, AI 전략 | 3 |
| [moai-support](./moai-support/) | 티켓 분류, KB 문서, 에스컬레이션 | 4 |
| [moai-office](./moai-office/) | PPT, DOCX, XLSX, HWPX 문서 생성 | 4 |
| [moai-schedules](./moai-schedules/) | 반복 업무 자동 실행 | 3 |
| [moai-career](./moai-career/) | 커리어 준비 — 자기소개서, 이력서, 면접 코칭, 채용공고 분석 | 4 |

## 총 산출물

| 항목 | 수량 |
|------|:----:|
| 플러그인 | 15 |
| 스킬 | 56 |
| 레퍼런스 파일 | 149 |
| 에이전트 | 7 |
| MCP 서버 | 5 |
| 스크립트 | 16 |
| 템플릿 | 8 |

## 설치

Claude Cowork에서 플러그인 설치:

1. Settings > Plugins에서 GitHub 저장소 URL 입력
2. 원하는 플러그인 선택하여 설치
3. `/moai init`으로 초기 설정

또는 `.plugin` 파일을 직접 설치:

1. [Releases](https://github.com/modu-ai/cowork-plugins/releases)에서 `moai-cowork.plugin` 다운로드
2. Claude Desktop > Cowork > 플러그인 관리 > **파일에서 설치**

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
- 모든 52개 스킬에 [What]+[When]+[Triggers] 구조의 description 적용
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

## 라이선스

MIT
