---
name: project
description: |
  Cowork 프로젝트 초기화와 작업 지침(CLAUDE.md) 자동 생성 스킬.
  사용자의 업무 워크플로우를 인터뷰하고, 설치된 22개 moai-* 플러그인을 기반으로
  **스킬 체이닝 워크플로우**가 포함된 CLAUDE.md를 생성합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "/project init", "/project init resume", "/project catalog", "/project status", "/project apikey"
  - "새 프로젝트 시작", "Cowork 프로젝트 초기 설정", "CLAUDE.md 만들어줘"
  - "이 프로젝트에 어울리는 워크플로우 설계해줘"
  - "도메인 라우팅 설정", "플러그인 연결", "API 키 등록"
  - "이어서 진행", "설치 완료", "다시 진행" — init 재개 요청
  - 사업계획, 마케팅, 계약서, 세무, 인사, 콘텐츠, 운영, PM 등
    자연어 요청이 들어왔을 때 적합한 도메인 플러그인으로 라우팅해야 할 때

  이 스킬은 **이름·회사 같은 글로벌 프로필을 재질문하지 않습니다.**
  프로젝트마다 "이번에 뭘 할 건지, 어떻게 처리하고 싶은지"만 인터뷰해서
  스킬 체인(예: strategy-planner → docx-generator → ai-slop-reviewer)을 설계하고
  누락 플러그인을 자동 감지해 설치 안내 후 사용자 확인을 받은 뒤 CLAUDE.md를 최적화합니다.
user-invocable: true
version: 2.12.1
---

# project — Cowork 프로젝트 초기화 & 스킬 체이닝 워크플로우 설계

사용자는 이 프로젝트에서 무엇을 할지 말해주면 됩니다. 나머지(플러그인 선택, 스킬 체인 설계, 산출물 규칙, 검수 파이프라인)는 MoAI가 설계·정리합니다.

## 개요

이 스킬은 Claude Cowork 사용자가 프로젝트를 시작할 때 **최적의 워크플로우를 자동으로 설계**하고, 프로젝트 루트에 `CLAUDE.md`를 생성합니다.

**핵심 기능**:
- 3단계 소크라테스 인터뷰로 프로젝트 맥락 수집
- 설치된 22개 moai 플러그인 자동 감지 (Bash + system reminder 교차 검증)
- 산출물별 **스킬 체인 설계** (예: 블로그 = blog → ai-slop-reviewer)
- **Gap Detection**: 누락 플러그인/스킬 자동 감지 → 설치 안내 → Re-entry 재개
- CLAUDE.md 템플릿 기반 자동 생성
- 필수 API 키 선택적 등록 안내

**v1.3.0 주요 변경**:
- 글로벌 프로필 시스템 제거 (이름·회사·역할 재질문 않음)
- 스킬 체이닝 기반 워크플로우 설계 도입
- CLAUDE.md 외부 템플릿화
- office/web 스킬 우선 + AI 슬롭 후처리 HARD 규칙 고정

**v2.11.0 변경**:
- Phase 2 Inventory 구체 메커니즘 도입 (Bash + system reminder 교차 검증)
- Phase 4 Gap Detection 신규 — 누락 플러그인/스킬 자동 감지 + 설치 안내 + Re-entry
- moai-media 7 스킬 → 4 스킬 (Higgsfield·ElevenLabs MCP가 직접 지원하는 스킬 제거)
- 17 플러그인 → 22 플러그인 (moai-book·moai-bi·moai-pm·moai-sales·moai-commerce 추가)
- `/project init resume` 커맨드 신규 — 누락 플러그인 설치 후 재개

## 트리거 키워드

이 스킬은 다음 상황에서 자동으로 호출됩니다:

**초기화 요청**:
- "/project init", "/project init resume", "새 프로젝트 시작", "Cowork 프로젝트 초기 설정"
- "CLAUDE.md 만들어줘", "프로젝트 설정 도와줘"
- "이어서 진행", "설치 완료", "다시 진행" — init 재개 트리거

**워크플로우 설계**:
- "이 프로젝트에 어울리는 워크플로우 설계해줘"
- "어떤 스킬을 쓸지 추천해줘", "스킬 체인 만들어줘"

**상태 확인**:
- "/project catalog", "/project status", "/project apikey"
- "설치된 플러그인 목록", "API 키 확인"

**도메인 라우팅** (자연어 → 플러그인):
- 사업계획, 스타트업, 투자, IR → `moai-business`
- 마케팅, SEO, SNS, 브랜드 → `moai-marketing`
- 계약서, 법률, NDA → `moai-legal`
- 세금, 부가세, 홈택스 → `moai-finance`
- 채용, 면접, 4대보험 → `moai-hr`
- 블로그, 카드뉴스, 뉴스레터 → `moai-content`
- PPT, 한글, Word, Excel → `moai-office`
- 이미지 프롬프트, 음성, TTS → `moai-media`
- 이커머스, 상세페이지, 쇼핑몰 → `moai-commerce`
- 원고, 출판, 전자책 → `moai-book`
- BI 리포트, 임원 보고 → `moai-bi`
- 프로젝트 관리, 주간보고 → `moai-pm`
- 영업, 제안서, 견적서 → `moai-sales`

## 워크플로우

### /project init — 새 워크플로우 생성

```
Phase 1: Interview (최대 3질문)
  ① 이 프로젝트에서 어떤 일을 하시나요?
  ② 주로 만드는 산출물은 무엇인가요? (블로그/사업계획서/계약서/…)
  ③ 특별히 지키고 싶은 톤·형식·제약이 있나요?

Phase 2: Inventory (cowork-plugins 마켓플레이스 스킬만 인벤토리 구성)
  - 소스 A: Bash로 `~/.claude/plugins/` 안에서 **modu-ai/cowork-plugins 마켓플레이스 출처 플러그인만** 필터링
    · 필터링 규칙: 디렉토리명이 `moai-*` 패턴이면서, 그 안의 `.claude-plugin/plugin.json`이 cowork-plugins 22 플러그인 화이트리스트에 포함되는 경우만 인정
    · 22 플러그인 화이트리스트: moai-core, moai-business, moai-marketing, moai-legal, moai-finance,
      moai-hr, moai-content, moai-operations, moai-education, moai-lifestyle, moai-product,
      moai-support, moai-office, moai-career, moai-data, moai-research, moai-media,
      moai-commerce, moai-book, moai-bi, moai-pm, moai-sales
    · 위 22개 외 다른 출처 플러그인(예: 사용자가 별도 마켓플레이스에서 설치한 플러그인)은 인벤토리에서 **완전 제외**
  - 필터링된 각 cowork 플러그인 안의 **모든 SKILL.md** 완전 스캔
    · 명령: `find ~/.claude/plugins/<plugin>/skills -maxdepth 2 -name SKILL.md`
    · 각 SKILL.md frontmatter에서 `name` 필드 추출 → 인벤토리에 등록
  - 소스 B: 현재 세션 system reminder "user-invocable skills" 목록 (cowork-plugins 출처만 필터)
  - 두 소스 교차 검증 → 활성 스킬 인벤토리 구성
  - .moai/cache/inventory.json에 저장 (스킬명 → cowork 플러그인 매핑)

Phase 3: Chain Design (핵심)
  - 산출물별 스킬 체인 설계
  - 예: 사업계획서 = strategy-planner → docx-generator → ai-slop-reviewer
  - 예: 블로그 발행 = blog → ai-slop-reviewer
  - 텍스트 산출물 체인은 항상 ai-slop-reviewer로 종료

Phase 4: Gap Detection (누락 감지 — 신규)
  - Phase 3 체인의 각 스킬이 Phase 2 inventory에 있는지 검증
  - 누락 스킬 발견 시:
    · 누락 스킬 → 소속 플러그인 매핑 표 생성
    · .moai/cache/init-progress.json에 진행 상태 저장 (Phase 1-3 결과)
    · AskUserQuestion 4 옵션 제시:
      1. (권장) 설치 안내 + 완료 후 재개 — 설치 명령 표시 후 대기
      2. 누락 스킬 제외하고 진행 — 해당 체인 단계 생략
      3. 대체 스킬로 변경 — 인벤토리에서 유사 스킬 추천
      4. 중단
  - 모두 설치됨 → Phase 5로 진행

Phase 5: Confirm
  - AskUserQuestion으로 체인 설계 승인 요청
  - 수정 / 승인 / 취소 선택지 제공

Phase 6: Generate CLAUDE.md
  - references/templates/CLAUDE.md.tmpl 기반 생성
  - Interview 결과를 페르소나·워크플로우 섹션에 주입
  - 승인된 스킬 체인을 "워크플로우" 섹션에 명시
  - office/web/ai-slop HARD 규칙 고정 포함
  - 최대 200라인

Phase 7: API Key (필요 시)
  - 선택된 플러그인이 요구하는 API 키만 선택적으로 등록 안내

Phase 8: First Run
  - 첫 작업 예시 3개를 스킬 체인 기반으로 동적 생성 후 안내
```

상세 프로토콜: `references/core/init-protocol.md`

### /project init resume — 설치 완료 후 재개

```
진입 패턴:
  - "/project init resume" 명시적 커맨드
  - "이어서 진행", "설치 완료", "다시 진행" 자연어 발화

재개 흐름:
  1. .moai/cache/init-progress.json 로드 (Phase 1-3 결과 복원)
  2. Phase 2 Inventory 재실행 (설치 여부 재확인)
  3. Phase 4 Gap Detection 재검증
  4. 누락 0건 → Phase 5 Confirm으로 진행
  5. 여전히 누락 → AskUserQuestion 4 옵션 재제시
```

### 스킬 체인 설계 원칙

**체인 구성 요소**:
1. **기획·분석 스킬** — strategy-planner, market-analyst, ux-researcher
2. **생성·제작 스킬** — blog, copywriting, card-news, spec-writer
3. **포맷 변환 스킬** — docx-generator, pptx-designer, xlsx-creator, hwpx-writer, landing-page
4. **미디어 스킬** (선택) — `gpt-image-2-prompt`·`gemini-3-image-prompt`·`midjourney-v8-prompt`(이미지 프롬프트 빌더), `audio-gen`(ElevenLabs MCP TTS·보이스 클로닝·다국어 더빙). 이미지·영상 실제 렌더링은 **Higgsfield MCP**(Soul·DOP·말하는머리·캐릭터) 단일 통합으로 직접 호출.
5. **후처리 스킬** — `ai-slop-reviewer` (텍스트 산출물 체인의 **필수 마지막 단계**)

**체인 표기 규약** (CLAUDE.md에 기록될 형식):
```
[산출물명]
  요청 예시: "..."
  체인: skill-A → skill-B → skill-C → ai-slop-reviewer
  입력/출력: A가 받는 입력과 C가 내는 출력 형식을 한 줄로 기록
  제외 조건: 스킵해야 할 상황 명시 (예: 데이터 시각화는 ai-slop 생략)
```

**체인 실행 계약**:
- 각 단계 스킬은 다음 스킬이 소비 가능한 **구조화된 출력**을 반환
- 사용자 확인 없이 체인 전체를 한 번에 실행
- 각 단계 완료 시 요약을 보고
- 마지막 단계가 `ai-slop-reviewer`인 경우 **진단 → 수정 → 주요 변경사항** 3블록 출력

## 사용 예시

### 예시 1: 스타트업 창업 프로젝트

```
사용자: "새 스타트업 프로젝트 시작할게"

Phase 1 Interview:
  Q1: "이 프로젝트에서 어떤 일을 하시나요?"
  A1: "교육 스타트업으로 사업계획서와 IR 자료를 만들어야 해"

  Q2: "주로 만드는 산출물은 무엇인가요?"
  A2: "사업계획서(DOCX), 피칭덱(PPT), 블로그 포스트"

  Q3: "특별히 지키고 싶은 톤·형식이 있나요?"
  A3: "전문적인 비즈니스 톤, 데이터 기반 근거 강조"

Phase 3 Chain Design:
  사업계획서: strategy-planner → docx-generator → ai-slop-reviewer
  피칭덱: investor-relations → pptx-designer → ai-slop-reviewer
  블로그: blog → ai-slop-reviewer

Phase 6 Generate CLAUDE.md:
  - 페르소나: 교육 스타트업 창업자, 비즈니스 톤, 데이터 기반
  - 워크플로우: 위 3개 체인 포함
  - HARD 규칙: office 스킬 우선 + ai-slop 후처리
```

### 예시 2: 마케팅 팀 콘텐츠 프로젝트

```
사용자: "마케팅 채널용 콘텐츠 만드는 프로젝트야"

Phase 1 Interview:
  Q1: "이 프로젝트에서 어떤 일을 하시나요?"
  A1: "블로그, 카드뉴스, 뉴스레터를 매주 만들어"

  Q2: "주로 만드는 산출물은 무엇인가요?"
  A2: "블로그 포스트, 인포그래픽(이미지), 뉴스레터"

  Q3: "특별히 지키고 싶은 톤·형식이 있나요?"
  A3: "친근하고 활기찬 톤, 이모지 적극 활용"

Phase 3 Chain Design:
  블로그: blog → ai-slop-reviewer
  카드뉴스: card-news → ai-slop-reviewer
  뉴스레터: newsletter → ai-slop-reviewer

Phase 6 Generate CLAUDE.md:
  - 페르소나: 마케팅 팀, 친근한 톤, 이모지 활용
  - 워크플로우: 위 3개 체인 포함
  - HARD 규칙: content 스킬 우선 + ai-slop 후처리
```

### 예시 3: 법무 계약서 검토 프로젝트

```
사용자: "계약서 검토 및 작성 프로젝트야"

Phase 1 Interview:
  Q1: "이 프로젝트에서 어떤 일을 하시나요?"
  A1: "NDA, 근로계약서, 서비스 계약서를 검토하고 작성해"

  Q2: "주로 만드는 산출물은 무엇인가요?"
  A2: "계약서 초안(DOCX), 계약서 검토 보고서"

  Q3: "특별히 지키고 싶은 톤·형식이 있나요?"
  A3: "법률적 정확성, 명확한 조항, 리스크 명시"

Phase 3 Chain Design:
  NDA 작성: nda-triage → docx-generator → ai-slop-reviewer
  계약서 검토: contract-review → ai-slop-reviewer
  근로계약서: labor-contract → docx-generator → ai-slop-reviewer

Phase 6 Generate CLAUDE.md:
  - 페르소나: 법무 담당자, 법률적 정확성, 리스크 명시
  - 워크플로우: 위 3개 체인 포함
  - HARD 규칙: legal 스킬 우선 + ai-slop 후처리
```

## 출력 형식

### 1. CLAUDE.md 구조

`/project init`이 생성하는 CLAUDE.md의 구조:

```markdown
# 프로젝트 이름

## 프로젝트 개요
- 사용자: [사용자 이름]
- 목적: [인터뷰에서 수집한 목적]
- 주요 산출물: [산출물 목록]

## 워크플로우
[산출물별 스킬 체인 테이블]

## HARD 규칙
1. 문서·콘텐츠 생성 우선순위
2. AI 슬롭 후처리
3. 실행 플로우 (Interview → Plan → Confirm → Execute)

## 참고 자료
[프로젝트 관련 링크]
```

### 2. 스킬 체인 테이블 예시

```markdown
## 워크플로우

| 산출물 | 요청 예시 | 체인 | 입출력 | 제외 조건 |
|--------|----------|------|--------|----------|
| 사업계획서 | "교육 스타트업 사업계획서 작성해줘" | strategy-planner → docx-generator → ai-slop-reviewer | 마켓 분석 → DOCX | - |
| 블로그 | "AI 툴 소개 블로그 포스트 작성해줘" | blog → ai-slop-reviewer | 주제 → Markdown | 데이터 시각화 필요 시 |
| 피칭덱 | "투자자 피칭용 PPT 만들어줘" | investor-relations → pptx-designer → ai-slop-reviewer | IR 요약 → PPTX | - |
```

### 3. AskUserQuestion 확인 예시

```markdown
Phase 5: 스킬 체인 설계 확인

다음 워크플로우로 CLAUDE.md를 생성합니다:

[사업계획서]
  체인: strategy-planner → docx-generator → ai-slop-reviewer
  설명: 시장 분석 후 DOCX 형식 사업계획서 생성, AI 슬롭 검수

[블로그]
  체인: blog → ai-slop-reviewer
  설명: 블로그 포스트 작성 후 AI 슬롭 검수

[피칭덱]
  체인: investor-relations → pptx-designer → ai-slop-reviewer
  설명: IR 자료 기반 PPTX 생성, AI 슬롭 검수

Options:
  1. 승인하고 CLAUDE.md 생성 (권장)
  2. 체인 수정
  3. 취소
```

## 주의사항

### 1. 글로벌 프로필 질문 금지

v1.3.0부터 **이름·회사·역할을 재질문하지 않습니다**.

- ❌ "이름이 뭐예요?", "어떤 회사에서 일하세요?", "직무가 무엇인가요?"
- ✅ "이 프로젝트에서 어떤 일을 하시나요?", "주로 만드는 산출물은 무엇인가요?"

필요하면 사용자가 CLAUDE.md를 직접 편집합니다.

### 2. moai-profile.md 생성 금지

**글로벌 프로필 저장 파일(`moai-profile.md`)을 생성하지 않습니다.**

모든 사용자 정보는 **이 프로젝트의 CLAUDE.md 한 곳에만** 기록됩니다.

### 3. AI 슬롭 후처리 필수

**모든 텍스트 산출물 워크플로우의 마지막 단계**에 `ai-slop-reviewer` 스킬을 호출해 AI 패턴을 제거하고 인간적인 톤으로 검수합니다.

- 대상: 블로그, 뉴스레터, 카피, 사업계획서, 계약서·공문 초안, 제안서, 보고서, 이메일, 랜딩 카피, 사업보고, 특허 초안 등 **모든 텍스트 산출물**
- 제외: 코드, JSON/CSV 데이터, 차트·표, 단순 조회 응답, 숫자 리포트
- 산출 형식: 진단 요약 → 수정 텍스트 → 주요 변경사항

### 4. office/web 스킬 우선

DOCX/PPTX/XLSX/HWPX/HTML 포맷은 Claude 기본 artifacts가 아닌 **moai-office/moai-content 스킬 우선** 사용합니다.

해당 스킬이 설치되어 있으면 기본 artifacts로 직접 생성하지 않습니다.

### 5. 인터뷰는 프로젝트 맥락에만 집중

Interview는 **이번 프로젝트에서 뭘 어떻게 할지**에만 집중합니다.

개인적인 프로필(이름·회사·역할)은 프로젝트마다 반복해서 수집하지 않습니다.

### 6. CLAUDE.md 라인 수 제한

CLAUDE.md는 **최대 200라인**으로 생성합니다.

핵심 내용만 포함하고, 상세 내용은 참조 파일(`references/`)로 위임합니다.

## 관련 스킬

### 필수 스킬

- `moai-core:ai-slop-reviewer` — 모든 텍스트 산출물의 필수 마지막 단계
- `moai-core:feedback` — `/project feedback` 커맨드로 GitHub Issues 자동 등록

### 도메인 플러그인 (22개)

| 플러그인 | 도메인 | 스킬 수 |
|---------|--------|--------|
| moai-core | 초기화·라우팅·AI 슬롭 검수 | 8 |
| moai-business | 비즈니스 전략·시장조사 | 10 |
| moai-marketing | 마케팅·SEO·SNS·광고 | 11 |
| moai-legal | 법률·계약서·컴플라이언스 | 5 |
| moai-finance | 재무·세무·결산·분석 | 6 |
| moai-hr | 인사·노무·채용 | 5 |
| moai-content | 콘텐츠·블로그·뉴스레터·랜딩·HTML | 12 |
| moai-operations | 운영·SOP·조달 | 3 |
| moai-education | 강사·교수·교사 교육 콘텐츠 | 5 |
| moai-lifestyle | 여행·건강·이벤트 | 3 |
| moai-product | PM·UX·로드맵·스펙 | 4 |
| moai-support | 고객지원·티켓 | 4 |
| moai-office | 문서·PPT·한글·엑셀·PDF | 5 |
| moai-career | 한국 취준생·재직자 커리어 | 4 |
| moai-data | 데이터 분석·시각화·공공데이터 | 3 |
| moai-research | 논문·특허·연구비 | 5 |
| moai-media | 이미지 프롬프트 빌더 + 음성 | 4 |
| moai-commerce | 한국 이커머스 풀스택 | 35 |
| moai-book | 한국 출판사 제출용 원고 | 8 |
| moai-bi | 비즈니스 인텔리전스·HTML 리포트 | 1 |
| moai-pm | 프로젝트 관리·주간보고 | 1 |
| moai-sales | 영업·제안서 | 1 |

### 관련 프로토콜

상세 프로토콜은 `references/core/`를 참고하세요:

- `init-protocol.md` — /project init Phase 1-8 + Gap Detection + Re-entry 전체 플로우 (v2.11.0)
- `router.md` — 자연어 → 플러그인 라우팅
- `context-collector.md` — 맥락 수집 프로토콜
- `claudemd-generator.md` — CLAUDE.md 생성 프로토콜
- `execution-protocol.md` — 스킬 체인 실행 프로토콜
- `evaluation-protocol.md` — 평가 프로토콜
- `diagnostic-protocol.md` — 환경 상태 진단 프로토콜
- `quality-evaluator.md` — 품질 자동 평가

전체 인덱스: `references/core/INDEX.md`

---

## 저장 위치

- **프로젝트 작업 지침**: `./CLAUDE.md` (≤ 200라인)
- **프로젝트 설정**: `./.moai/config.json`
- **API 키**: `./.moai/credentials.env` (프로젝트 격리)
- **템플릿**: `references/templates/CLAUDE.md.tmpl`