# init-protocol.md — /project init 전체 플로우 (v1.3)

## 개요

`/project init`은 Claude Cowork 프로젝트를 초기화하고, 사용자의 업무 워크플로우를 인터뷰한 뒤, **스킬 체이닝 기반 CLAUDE.md**를 생성한다.

**v1.3 핵심 변경 (v1.2 대비):**
- `/moai init` → `/project init` 커맨드 변경
- **글로벌 프로필 시스템 전면 제거** (이름·회사·역할 재질문 없음)
- Phase 0 (프로필 감지) 삭제
- Phase 1 (프로필 수집) → Phase 1 (워크플로우 인터뷰)로 교체
- Phase 3 (스킬 체인 설계) 신규 추가
- CLAUDE.md에 office/web 스킬 우선 규칙 + AI 슬롭 후처리 규칙 HARD로 고정 포함

---

## 전체 플로우

```
/project init
    ↓
Phase 1: 워크플로우 인터뷰 (최대 3질문)
    ↓
Phase 2: 설치된 플러그인 자동 감지 + 매칭
    ↓
Phase 3: 스킬 체인 설계 (산출물별 파이프라인)
    ↓
Phase 4: 설계 확인 (AskUserQuestion)
    ↓
Phase 5: CLAUDE.md 생성 (CLAUDE.md.tmpl 기반, ≤ 200라인)
    ↓
Phase 6: API 키 / 커넥터 (필요한 경우만)
    ↓
Phase 7: 첫 실행 안내 (스킬 체인 기반 예시 3개)
```

총 소요 시간: **2-3분**. AskUserQuestion 최대 6회.

---

## Phase 1: 워크플로우 인터뷰

사용자의 **이 프로젝트 맥락**만 수집한다. 이름·회사·역할 같은 **글로벌 프로필 정보는 묻지 않는다**.

### 1-1. 업무 유형

AskUserQuestion (1질문, 4옵션, multiSelect)

```
"이 프로젝트에서 어떤 일을 하시나요? (복수 선택 가능)"

☐ 사업 기획·전략 — 사업계획서, 시장조사, IR, 투자제안서
☐ 콘텐츠 제작 — 블로그, 카드뉴스, 뉴스레터, SNS, 카피
☐ 문서·행정 — PPT, 한글, Word, Excel, 공문, 계약서
☐ 제품·연구 — PM 문서, UX 리서치, 논문, 특허, 데이터 분석
+ Other (직접 입력)
```

### 1-2. 주요 산출물

AskUserQuestion (1질문, 자유입력 + 예시 4개)

```
"주로 만드는 산출물은 무엇인가요? 구체적으로 적어주세요.
 예: '사업계획서 PPT, 투자자용 IR 덱, 언론 보도자료'
     '주 2회 블로그, 카드뉴스, 인스타 릴스 스크립트'
     '계약서 검토, 근로계약서, NDA 초안'
     'Series A 피칭 자료, 시장 분석 리포트'"

+ Other (자유 입력)
```

### 1-3. 톤·형식 제약 (선택)

AskUserQuestion (1질문, 4옵션)

```
"특별히 지키고 싶은 톤이나 형식 제약이 있나요?"

○ 공식·격식체 유지 (관공서·기업 보고)
○ 캐주얼·대화체 (SNS·블로그·콘텐츠)
○ 산업별 전문 용어 사용 (법률·의료·금융·기술)
○ 제약 없음 — 그때그때 지정
+ Other (직접 입력)
```

**수집 결과는 메모리에 임시 저장**되며, Phase 5에서 CLAUDE.md에 직접 기록된다.
별도 `moai-profile.md`를 생성하지 않는다.

---

## Phase 2: 설치된 플러그인 자동 감지

```
Cowork에 설치된 moai-* 플러그인을 자동 스캔:

installed_plugins = scan_installed_moai_plugins()

Phase 1 답변 기반 매칭:
- "사업 기획·전략" → moai-business, moai-finance (우선)
- "콘텐츠 제작" → moai-content, moai-marketing, moai-media
- "문서·행정" → moai-office, moai-legal, moai-hr
- "제품·연구" → moai-product, moai-research, moai-data
```

**moai-core는 항상 포함** (라우터 역할). 선택 UI에는 표시하지 않는다.

미설치 플러그인은 **안내만 하고 강제 설치하지 않는다**:

```
"추가로 이런 플러그인을 설치하면 도움이 됩니다:
 • moai-finance — 세무·부가세·K-IFRS
 Settings > Plugins 에서 설치 가능합니다."
```

---

## Phase 3: 스킬 체인 설계 (핵심 신규)

Phase 1-2 결과를 바탕으로 **산출물별 실행 체인**을 설계한다.

### 3-1. 체인 구성 규칙

각 산출물 체인은 다음 구조를 따른다:

```
[기획/분석 스킬] → [생성 스킬] → [포맷 변환 스킬 or 미디어 스킬] → ai-slop-reviewer
```

- 텍스트 산출물 체인은 **반드시 `ai-slop-reviewer`로 종료**
- 비텍스트(차트·데이터·숫자)는 ai-slop 단계 **생략**
- 체인이 단순하면 스킬 1-2개만으로도 OK

### 3-2. 체인 프리셋 테이블

| 산출물 | 권장 체인 |
|---|---|
| 사업계획서(Word) | `strategy-planner` → `market-analyst` → `docx-generator` → `ai-slop-reviewer` |
| 사업계획서(PPT) | `strategy-planner` → `pptx-designer` → `ai-slop-reviewer` |
| IR 피칭덱 | `investor-relations` → `pptx-designer` → `ai-slop-reviewer` |
| 시장조사 리포트 | `market-analyst` → `docx-generator` → `ai-slop-reviewer` |
| 블로그 포스트 | `blog` → `ai-slop-reviewer` → (선택) `nano-banana` |
| 카드뉴스 | `card-news` → `nano-banana` → `ai-slop-reviewer` |
| 뉴스레터 | `newsletter` → `ai-slop-reviewer` |
| 랜딩 페이지(HTML) | `copywriting` → `landing-page` → `ai-slop-reviewer` |
| SNS 콘텐츠 세트 | `sns-content` → `nano-banana` → `ai-slop-reviewer` |
| 이메일 시퀀스 | `email-sequence` → `ai-slop-reviewer` |
| 계약서 초안 | `contract-review` or `nda-triage` → `docx-generator` → `ai-slop-reviewer` |
| 컴플라이언스 체크 | `compliance-check` → `ai-slop-reviewer` |
| 부가세 신고 | `tax-helper` (숫자 산출물 — ai-slop 생략) |
| 재무제표 분석 | `financial-statements` → `xlsx-creator` (숫자 — ai-slop 생략) |
| 근로계약서 | `employment-manager` → `docx-generator` → `ai-slop-reviewer` |
| 채용 공고 | `draft-offer` → `ai-slop-reviewer` |
| 성과 평가서 | `performance-review` → `docx-generator` → `ai-slop-reviewer` |
| 이력서·자기소개서 | `resume-builder` → `ai-slop-reviewer` |
| 포트폴리오 | `portfolio-guide` → `landing-page` → `ai-slop-reviewer` |
| 논문 초안 | `paper-writer` → `docx-generator` → `ai-slop-reviewer` |
| 연구비 제안서 | `grant-writer` → `docx-generator` → `ai-slop-reviewer` |
| 특허 명세서 | `patent-analyzer` → `docx-generator` → `ai-slop-reviewer` |
| PPT 공문·기안 | `pptx-designer` → `ai-slop-reviewer` |
| 한글 공문 | `hwpx-writer` → `ai-slop-reviewer` |
| 데이터 시각화 | `data-visualizer` (차트 — ai-slop 생략) |
| UX 리서치 리포트 | `ux-researcher` → `docx-generator` → `ai-slop-reviewer` |
| 제품 SPEC | `spec-writer` → `ai-slop-reviewer` |
| 로드맵 | `roadmap-manager` → `pptx-designer` → `ai-slop-reviewer` |
| KB 문서 | `kb-article` → `ai-slop-reviewer` |
| CS 응대 초안 | `draft-response` → `ai-slop-reviewer` |
| 여행 일정표 | `travel-planner` → `docx-generator` → `ai-slop-reviewer` |
| 강의 커리큘럼 | `curriculum-designer` → `pptx-designer` → `ai-slop-reviewer` |
| 평가 문제지 | `assessment-creator` → `docx-generator` |
| 상세페이지 | `product-detail` → `ai-slop-reviewer` |
| 브랜드 아이덴티티 | `brand-identity` → `ai-slop-reviewer` |
| 캠페인 플랜 | `campaign-planner` → `pptx-designer` → `ai-slop-reviewer` |
| SEO 감사 | `seo-audit` → `ai-slop-reviewer` |
| 성과 리포트 | `performance-report` → `xlsx-creator` or `pptx-designer` |
| 일일 브리핑 | `daily-briefing` → `ai-slop-reviewer` |
| 영상 제작 | `video-gen` → (선택) `audio-gen` |
| TTS 더빙 | `audio-gen` (elevenlabs MCP — ai-slop 생략) |
| 립싱크 영상 | `speech-video` (음성+영상 결합) |

설치되지 않은 스킬은 체인에서 제외한다.

### 3-3. 체인 요약 포맷

Phase 4(확인 단계)에서 사용자에게 보여줄 요약:

```
이 프로젝트의 실행 체인 설계

[주 산출물 1] 사업계획서(PPT)
  체인: strategy-planner → pptx-designer → ai-slop-reviewer
  트리거 예시: "사업계획서 만들어줘"

[주 산출물 2] IR 피칭덱
  체인: investor-relations → pptx-designer → ai-slop-reviewer
  트리거 예시: "IR 자료 써줘"

[보조 산출물 3] 시장조사 리포트
  체인: market-analyst → docx-generator → ai-slop-reviewer
  트리거 예시: "시장조사 해줘"
```

---

## Phase 4: 설계 확인

AskUserQuestion (1질문, 3옵션)

```
"위 스킬 체인 설계로 CLAUDE.md를 생성하시겠습니까?"

○ 승인 — 이 설계로 생성 (권장)
○ 수정 — 체인 일부를 수정하고 싶음
○ 취소 — 초기화 중단
+ Other
```

"수정" 선택 시: 수정하고 싶은 체인을 자유입력으로 받아 Phase 3-2 테이블을 참조하여 재설계.

---

## Phase 5: CLAUDE.md 생성

`references/templates/CLAUDE.md.tmpl`을 로드하여 다음 변수를 치환한다:

| 변수 | 소스 |
|---|---|
| `{project_name}` | 현재 프로젝트 폴더명 |
| `{version}` | plugin.json의 moai-core version |
| `{date}` | 오늘 날짜 (YYYY-MM-DD) |
| `{installed_plugins}` | Phase 2에서 감지된 플러그인 리스트 |
| `{primary_deliverables}` | Phase 1-2 답변 요약 |
| `{project_purpose}` | Phase 1-2 답변에서 추출 |
| `{audience}` | Phase 1-2에서 추출 또는 "미지정" |
| `{tone_constraints}` | Phase 1-3 답변 |
| `{workflow_chains}` | Phase 3에서 설계된 체인 블록 (Markdown) |
| `{routing_summary}` | 사용하는 플러그인의 라우팅 키워드만 요약 |
| `{connectors_and_apikeys}` | Phase 6 결과 요약 |
| `{project_context_notes}` | 자유 메모 (초기값: 비어있음) |

### 생성 원칙

1. **≤ 200라인** — 하네스 상세 복사 금지
2. **스킬 체인은 최대 10개까지** 나열 (나머지는 catalog 참조)
3. **HARD 규칙 블록(office 우선, ai-slop 후처리)은 항상 포함**
4. **파일 인코딩**: UTF-8, LF, 한국어

상세: `references/core/claudemd-generator.md`

---

## Phase 6: API 키 / 커넥터 (선택적)

Phase 2에서 선택된 플러그인이 API 키를 요구하면 등록 안내.

**API 키 목록 (6개):**

| # | 서비스 | 환경변수 | 용도 | 발급처 |
|---|--------|---------|------|--------|
| 1 | 공공데이터포털 | `DATA_GO_KR_API_KEY` | 공공데이터/KOSIS/KCI | data.go.kr |
| 2 | KIPRIS Plus | `KIPRIS_API_KEY` | 특허 검색 | plus.kipris.or.kr |
| 3 | 국가법령정보 | `KOREAN_LAW_OC` | 법령/판례 | law.go.kr |
| 4 | Google Gemini | `GEMINI_API_KEY` | Nano Banana 이미지 | ai.google.dev |
| 5 | fal.ai | `FAL_KEY` | fal-gateway (Flux·Recraft·Hailuo·Luma·Pika·MiniMax 등 1000+ 모델) | fal.ai |
| 6 | ElevenLabs | `ELEVENLABS_API_KEY` | audio-gen·speech-video (TTS/음성 합성, ElevenLabs MCP 사용) | elevenlabs.io |

선택된 플러그인과 무관한 키는 물어보지 않는다.
**저장 위치**: `./.moai/credentials.env` (프로젝트 격리).

**커넥터**: Cowork 공식 커넥터(Google Drive, Notion, Gmail, Slack 등)는 Settings > Connectors 안내만 제공. init은 OAuth에 관여하지 않는다.

---

## Phase 7: 첫 실행 안내

Phase 3에서 설계된 체인 중 상위 3개를 예시로 제시:

```
설정이 완료되었습니다. 바로 시작해 보세요.

1. 사업계획서 제작
   당신: "초기 스타트업 사업계획서 PPT로 만들어줘"
   → 체인: strategy-planner → pptx-designer → ai-slop-reviewer
   → 결과: .pptx 파일 + 진단·수정 리포트

2. 시장조사 리포트
   당신: "2025 K-뷰티 시장 리포트 써줘"
   → 체인: market-analyst → docx-generator → ai-slop-reviewer

3. 블로그 발행
   당신: "창업 인사이트 블로그 글 하나 써줘"
   → 체인: blog → ai-slop-reviewer

전체 플러그인/스킬 목록: /project catalog
현재 설정 상태: /project status
```

---

## /project apikey — API 키 관리

```
/project apikey
```

6개 API 키를 조회/변경/추가/삭제한다. (기존 /moai apikey와 동일한 동작, 커맨드 이름만 변경)

---

## AskUserQuestion 제약 준수 요약

| Phase | 질문 수 | 옵션 수 |
|-------|---------|---------|
| Phase 1-1 업무 유형 | 1 | 4 (multiSelect) |
| Phase 1-2 산출물 | 1 | 자유입력 |
| Phase 1-3 톤·제약 | 1 | 4 |
| Phase 4 설계 확인 | 1 | 3 |
| Phase 6 API 키 (조건부) | 1-2 | 최대 4 (multiSelect) |
| **합계** | **최대 6회** | 모두 ≤ 4 |

---

## v1.2 대비 변경 요약

| 항목 | v1.2 | v1.3 |
|------|------|------|
| 커맨드 | `/moai init` | `/project init` |
| 글로벌 프로필 | 이름·회사·역할 수집 및 글로벌 지침 저장 | **제거** |
| Phase 0 (프로필 감지) | 있음 | **삭제** |
| Phase 1 내용 | 프로필 수집 | 워크플로우 인터뷰 |
| 스킬 체인 설계 | 없음 | **Phase 3 신규** |
| CLAUDE.md 템플릿 | inline 하드코딩 | `templates/CLAUDE.md.tmpl` 외부 파일 |
| HARD 규칙(office·ai-slop) | 일부 산발적 | **템플릿 고정 블록** |
| moai-profile.md 생성 | 함 | **하지 않음** |
| AskUserQuestion 회수 | 최대 9회 | **최대 6회** |
