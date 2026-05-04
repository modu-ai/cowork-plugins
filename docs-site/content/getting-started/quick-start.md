---
title: "빠른 시작"
weight: 30
description: "modu-ai/cowork-plugins 마켓플레이스 등록부터 첫 스킬 체인 실행까지 약 10분 완성 가이드"
geekdocBreadcrumb: true
---
`modu-ai/cowork-plugins` 마켓플레이스를 Claude Cowork에 등록하고 첫 스킬 체인을 실행하기까지의 전체 흐름을 정리한 페이지입니다. 처음부터 끝까지 약 **10분** 소요됩니다.

## 사전 체크

- [Cowork 설치](../install/) 완료
- 작업할 **로컬 폴더** 하나 준비 (Windows에서는 짧은 경로를 권장합니다)

## 전체 흐름

1. **마켓플레이스 등록**

   Cowork **좌측 사이드바 → 사용자 지정(Customize) → 개인 플러그인 → 플러그인 추가 → 마켓플이스 추가**에서 다음 URL을 입력합니다.

   {{< terminal title="claude — cowork" >}}
> modu-ai/cowork-plugins
   {{< /terminal >}}

   동기화가 끝나면 21개 플러그인 목록이 표시됩니다.

2. **`moai-core` 설치**

   {{< hint type="warning" >}}
   **반드시 `moai-core`부터** 설치합니다. 여기에 `/project init` 마법사와 모든 텍스트 체인에 필요한 `ai-slop-reviewer`가 포함되어 있습니다.
   {{< /hint >}}

   `moai-core` 옆의 **+** 버튼을 클릭하면 설치가 완료됩니다.

3. **도메인 플러그인 선택**

   이번에 진행할 작업에 맞춰 플러그인을 추가합니다. 예시는 다음과 같습니다.

   - 사업계획서 → `moai-business`, `moai-office`
   - 블로그 발행 → `moai-content`, `moai-media`
   - 계약서 검토 → `moai-legal`, `moai-office`
   - 이미지 생성 → `moai-media` (+ `GEMINI_API_KEY` 필요)

   21개 모두를 한 번에 설치할 필요는 없습니다.

4. **프로젝트 생성 및 `/project init`**

   Cowork에서 좌측 사이드바 **프로젝트** 섹션의 **+ 새 프로젝트**를 눌러 프로젝트를 만들고, 프로젝트 설정 화면에서 **작업 폴더 연결** 항목에 앞서 준비한 로컬 폴더를 지정합니다. 프로젝트·폴더 개념이 낯설다면 [프로젝트와 메모리](../../cowork/projects-memory/) 페이지를 먼저 참고하세요. 이후 대화창에 다음을 입력합니다.

   {{< terminal title="claude — cowork" >}}
> /project init
   {{< /terminal >}}

   `moai-core:project` 스킬이 실행되어 **7단계 흐름**(Interview → Detect → Chain → Confirm → Generate → APIKey → First Run)을 진행합니다. 자세한 내용은 [moai-core 상세](../../plugins/moai-core/)에서 확인할 수 있습니다. 약 3~5분 안에 프로젝트용 `CLAUDE.md`가 루트에 생성됩니다.

5. **첫 요청**

   이제 자연어로 요청하면 `moai-core`의 라우터가 적합한 스킬을 자동으로 호출합니다. **본 문서의 모든 사용자 입력은 `> ` prefix와 함께 표기**합니다(실제 입력 시 `>` 제외 — [표기 규약](../../cowork/skills/#스킬-호출-방식)).

   {{< terminal title="claude — cowork" >}}
> "우리 SaaS의 Series A용 IR 덱 초안 만들어줘. 타깃 고객은 한국 중소제조업체야."
   {{< /terminal >}}

   체인 예시: `investor-relations → pptx-designer → ai-slop-reviewer`

6. **산출물 확인**

   PPTX 파일이 작업 폴더에 저장되고, 대화창에 **진단 → 수정 → 주요 변경사항** 3블록의 AI 슬롭 검수 리포트가 함께 표시됩니다.

## API 키·커넥터 등록 (선택)

일부 플러그인은 외부 서비스 키가 필요합니다.

| 플러그인 | 필요한 키·커넥터 |
|---|---|
| `moai-media` | `GEMINI_API_KEY`, `FAL_KEY`, `ELEVENLABS_API_KEY` |
| `moai-business` (DART 공시 연동) | DART MCP |
| `moai-data` | 공공데이터포털·KOSIS API 키 |
| `moai-content:blog` (WordPress 자동 업로드) | WordPress MCP |

키는 프로젝트 루트의 `.moai/credentials.env`에 저장됩니다. 절대 외부 저장소에 커밋하지 마세요.

## 잘 안 될 때

- **스킬이 자동으로 호출되지 않을 때**: `moai-core`가 설치돼 있는지, `/project init`이 실행됐는지 확인합니다.
- **Word·PPT 파일이 깨질 때**: `moai-office`가 설치돼 있는지, Python 의존성(`python-docx`, `python-hwpx` 등)이 갖춰졌는지 확인합니다.
- **AI 슬롭 검수가 실행되지 않을 때**: 요청에 "빠르게"라는 표현이 포함되면 검수가 스킵될 수 있습니다. "검수까지 돌려줘"라고 명시하세요.

## 주요 스킬 카탈로그 (106개)

### moai-core (핵심 유틸리티)
- **ai-slop-reviewer**: 모든 텍스트 산출물의 AI 패턴 검수 및 개선
- **project**: 프로젝트 초기화 및 문서 생성
- **feedback**: 사용자 피드백 수집 및 GitHub 이슈 생성

### moai-content (콘텐츠 생성)
- **blog**: 블로그 포스팅 생성
- **card-news**: 뉴스 카드 생성
- **copywriting**: 마케팅 카피 작성
- **landing-page**: 랜딩 페이지 생성
- **newsletter**: 뉴스레터 생성
- **product-detail**: 제품 상세페이지 작성
- **social-media**: SNS 콘텐츠 생성

### moai-business (비즈니스)
- **daily-briefing**: 일간 브리핑 생성
- **investor-relations**: 투자자 관계 문서 생성
- **market-analyst**: 시장 분석 보고서 작성
- **strategy-planner**: 전략 계획 수립
- **sbiz365-analyst**: 소상공인365 상권분석
- **kr-gov-grant**: 정부지원사업 통합 지원

### moai-office (오피스 문서)
- **docx-generator**: Word 문서 생성
- **pptx-designer**: PowerPoint 디자인
- **xlsx-creator**: Excel 생성
- **hwpx-writer**: 한글 문서 작성

### moai-legal (법률)
- **compliance-check**: 규정 준수 검사
- **contract-review**: 계약서 검토
- **legal-risk**: 법적 위험 평가
- **nda-triage**: NDA 우선순위 분류

### moai-finance (재무)
- **close-management**: 마감 관리
- **financial-statements**: 재무제표 생성
- **tax-helper**: 세무 도우미
- **variance-analysis**: 분석 차이

### moai-marketing (마케팅)
- **brand-identity**: 브랜드 정체성 생성
- **campaign-planner**: 캠페인 기획
- **email-sequence**: 이메일 시퀀스 작성
- **performance-report**: 성과 보고서
- **personal-branding**: 개인 브랜딩
- **seo-audit**: SEO 감사
- **sns-content**: SNS 콘텐츠
- **target-script**: 타겟 스크립트 생성

### moai-education (교육)
- **assessment-creator**: 평가 문제 생성
- **curriculum-designer**: 커리큘럼 설계
- **research-assistant**: 연구 보조

### moai-media (미디어)
- **image-gen**: 이미지 생성
- **video-gen**: 비디오 생성
- **nano-banana**: 이미지 생성 (Nano Banana Pro)

### moai-product (제품)
- **ux-designer**: UX 디자인

## 다음 단계

- [moai-core 상세](../../plugins/moai-core/)
- [moai-content 상세](../../plugins/moai-content/)
- [Cowork 플러그인 사용](../../cowork/plugins/) — Cowork 환경 통합 가이드

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [Use plugins in Claude Cowork](https://support.claude.com/en/articles/13837440)