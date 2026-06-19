---
name: project
description: |
  Cowork 프로젝트 초기화와 작업 지침(CLAUDE.md) 자동 생성 스킬.
  사용자의 업무 워크플로우를 인터뷰하고, 설치된 27개 moai 플러그인을 기반으로
  **스킬 체이닝 워크플로우**가 포함된 CLAUDE.md를 생성합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "새 프로젝트 시작", "Cowork 프로젝트 초기 설정", "CLAUDE.md 만들어줘" — 서브커맨드 없이 bare `/project`가 초기화 기본 동작
  - "/project", "/project resume", "/project catalog", "/project status", "/project apikey", "/project doctor", "/project feedback"
  - "/project init", "/project init resume" — 레거시 별칭으로 계속 인식 (각각 bare `/project`, `/project resume`와 동일)
  - "이 프로젝트에 어울리는 워크플로우 설계해줘"
  - "도메인 라우팅 설정", "플러그인 연결", "API 키 등록", "환경 진단"
  - "이어서 진행", "설치 완료", "다시 진행" — 설치 완료 후 재개 요청
  - 사업계획, 마케팅, 계약서, 세무, 인사, 콘텐츠, 운영, PM 등
    자연어 요청이 들어왔을 때 적합한 도메인 플러그인으로 라우팅해야 할 때

  이 스킬은 **이름·회사 같은 글로벌 프로필을 재질문하지 않습니다.**
  프로젝트마다 "이번에 뭘 할 건지, 어떻게 처리하고 싶은지"만 인터뷰해서
  스킬 체인(예: strategy-planner → docx-generator → ai-slop-reviewer)을 설계하고
  누락 플러그인을 자동 감지해 설치 안내 후 사용자 확인을 받은 뒤 CLAUDE.md를 최적화합니다.
user-invocable: true
version: 2.27.0
---

# project — Cowork 프로젝트 초기화 & 스킬 체이닝 워크플로우 설계

사용자는 이 프로젝트에서 무엇을 할지 말해주면 됩니다. 나머지(플러그인 선택, 스킬 체인 설계, 산출물 규칙, 검수 파이프라인)는 MoAI가 설계·정리합니다.

## 개요

이 스킬은 Claude Cowork 사용자가 프로젝트를 시작할 때 **최적의 워크플로우를 자동으로 설계**하고, 프로젝트 루트에 `CLAUDE.md`를 생성합니다.

**핵심 기능**:
- 3단계 소크라테스 인터뷰로 프로젝트 맥락 수집
- 설치된 27개 moai 플러그인 자동 감지 (Bash + system reminder 교차 검증)
- 산출물별 **스킬 체인 설계** (예: 블로그 = blog → ai-slop-reviewer)
- **Gap Detection**: 누락 플러그인/스킬 자동 감지 → 설치 안내 → 재개
- CLAUDE.md 템플릿 기반 자동 생성
- 필수 API 키 선택적 등록 안내

**현재 동작 요약**:
- 서브커맨드 없이 bare `/project`가 초기화 기본 동작 (Phase 1-8). `/project init`은 레거시 별칭으로 계속 인식.
- 글로벌 프로필 시스템 없음 — 이름·회사·역할을 프로젝트마다 재질문하지 않음.
- 스킬 체이닝 기반 워크플로우 설계 + CLAUDE.md 외부 템플릿화.
- office/web 스킬 우선 + AI 슬롭 후처리 HARD 규칙 고정.
- Phase 2 Inventory(Bash + system reminder 교차 검증) + Phase 4 Gap Detection(누락 감지 → 설치 안내 → 재개).

## 트리거 키워드

이 스킬은 다음 상황에서 자동으로 호출됩니다:

**초기화 요청**:
- "새 프로젝트 시작", "Cowork 프로젝트 초기 설정" — 서브커맨드 없이 bare `/project`가 초기화 기본 동작
- "/project", "/project init"(레거시 별칭), "CLAUDE.md 만들어줘", "프로젝트 설정 도와줘"
- "이어서 진행", "설치 완료", "다시 진행" — 설치 완료 후 재개 트리거 (`/project resume`, 레거시 `/project init resume`)

**워크플로우 설계**:
- "이 프로젝트에 어울리는 워크플로우 설계해줘"
- "어떤 스킬을 쓸지 추천해줘", "스킬 체인 만들어줘"

**상태 확인·관리**:
- "/project catalog", "/project status", "/project apikey", "/project doctor", "/project feedback"
- "설치된 플러그인 목록", "API 키 확인", "환경 진단"

**도메인 라우팅** (자연어 → 플러그인, 27개 전체):
- 사업계획, 시장조사, IR, 소상공인, 정부지원 → `moai-business`
- SEO, SNS, 캠페인, 이메일, 랜딩진단, 메타광고 → `moai-marketing`
- 계약서, 개인정보, NDA, 법인등기 → `moai-legal`
- 세무, 결산, 재무제표, 변동분석 → `moai-finance`
- 근로계약, 4대보험, 채용, 성과평가 → `moai-hr`
- 블로그, 카드뉴스, 랜딩/상세, 뉴스레터, 카피, HTML, 한국어 윤문 → `moai-content`
- 운영, SOP, 벤더관리 → `moai-operations`
- 강의운영매뉴얼, 후기시퀀스, 교육과정, 평가 → `moai-education`
- 여행, 웰니스, 이벤트 → `moai-lifestyle`
- PM, UX, 로드맵, 스펙 → `moai-product`
- 티켓, 응대, KB, 에스컬레이션 → `moai-support`
- PPT, DOCX, XLSX, HWPX, PDF, NotebookLM → `moai-office`
- 이력서, 자소서, 면접, 포트폴리오 → `moai-career`
- CSV/Excel, 시각화, 공공데이터 → `moai-data`
- 한국 공공데이터 조회(주식·경매·부동산) → `moai-public-data`
- 논문, 특허, 연구비 → `moai-research`
- AI 이미지, 영상, 음성 → `moai-media`
- 한국 이커머스 풀세트 → `moai-commerce`
- 경영진 1pager 요약 → `moai-bi`
- 주간 업무보고 → `moai-pm`
- B2B 제안서, RFP → `moai-sales`
- 한국 출판 원고 풀스택 → `moai-book`
- Claude Design 보조 → `moai-design`
- 개인 재무, 재테크 → `moai-wealth`
- 회고, 목표, 시간, 습관 → `moai-productivity`
- 직장 커뮤니케이션, 보고, 회의, 피드백 → `moai-comms`
- 초기화, 라우팅, AI 슬롭 검수, 피드백, MCP 커넥터 → `moai-core`

## 워크플로우

### 커맨드 표면

init 서브커맨드는 생략 가능 — bare `/project`가 초기화 기본 동작입니다. (`/project init`은 레거시 별칭으로 계속 인식)

| 커맨드 | 동작 |
|--------|------|
| `/project` (서브커맨드 없이) | 초기화 워크플로우 실행 (Phase 1-8). **PRIMARY 기본 동작.** |
| `/project resume` | 설치 완료 후 재개 (구 `/project init resume`) |
| `/project catalog` | 플러그인·스킬 카탈로그 |
| `/project status` | 현재 설정 상태 |
| `/project apikey` | API 키 관리 |
| `/project doctor` | 환경 진단 |
| `/project feedback` | GitHub 이슈 등록 |

**LEGACY 별칭** (계속 인식, 비파괴): `/project init` ≡ bare `/project`; `/project init resume` ≡ `/project resume`.

### /project — 초기화(새 워크플로우 생성)

> 진입점은 서브커맨드 없는 bare `/project`입니다. `/project init`은 레거시 별칭으로 동일하게 동작합니다.

```
Phase 1: Interview (최대 3질문)
  ① 이 프로젝트에서 어떤 일을 하시나요?
  ② 주로 만드는 산출물은 무엇인가요? (블로그/사업계획서/계약서/…)
  ③ 특별히 지키고 싶은 톤·형식·제약이 있나요?

Phase 2: Inventory (cowork-plugins 마켓플레이스 스킬만 인벤토리 구성)
  - 소스 A: Bash로 `~/.claude/plugins/` 안에서 **modu-ai/cowork-plugins 마켓플레이스 출처 플러그인만** 필터링
    · 필터링 규칙: 디렉토리명이 `moai-*` 패턴이면서, 그 안의 `.claude-plugin/plugin.json`이 cowork-plugins 27 플러그인 화이트리스트에 포함되는 경우만 인정
    · 27 플러그인 화이트리스트: moai-core, moai-business, moai-marketing, moai-legal, moai-finance,
      moai-hr, moai-content, moai-operations, moai-education, moai-lifestyle, moai-product,
      moai-support, moai-office, moai-career, moai-data, moai-public-data, moai-research, moai-media,
      moai-commerce, moai-bi, moai-pm, moai-sales, moai-book, moai-design, moai-wealth,
      moai-productivity, moai-comms
    · 위 27개 외 다른 출처 플러그인(예: 사용자가 별도 마켓플레이스에서 설치한 플러그인)은 인벤토리에서 **완전 제외**
  - 필터링된 각 cowork 플러그인 안의 **모든 SKILL.md** 완전 스캔
    · 명령: `find ~/.claude/plugins/<plugin>/skills -maxdepth 2 -name SKILL.md`
    · 각 SKILL.md frontmatter에서 `name` 필드 추출 → 인벤토리에 등록
  - 소스 B: 현재 세션 system reminder "user-invocable skills" 목록 (cowork-plugins 출처만 필터)
  - 두 소스 교차 검증 → 활성 스킬 인벤토리 구성
  - 에이전트 인벤토리: 각 플러그인 agents/*.md 동적 스캔 → agents_available (코디네이터, Cowork 전용)
  - .moai/cache/inventory.json에 저장 (스킬명·에이전트명 → cowork 플러그인 매핑)

Phase 3: Chain Design (핵심) — 코디네이터 우선(agent-aware)
  - 코디네이터 우선: 매칭 코디네이터 에이전트가 있으면 우선 추천, 없으면 인라인 스킬 체인
  - 예: 사업계획서 = business-plan-coordinator(에이전트) / 폴백 strategy-planner → pptx-designer → ai-slop-reviewer
  - 예: 블로그 발행 = blog → ai-slop-reviewer (단순 — 코디네이터 불요)
  - 텍스트 산출물 체인은 항상 ai-slop-reviewer로 종료 (코디네이터가 내부 처리 시 중복 금지)

Phase 3.5: Agent Synthesis (선택 — 기존 코디네이터가 없을 때만 신규 생성)
  - Step 0: 매칭되는 기존 코디네이터가 있으면 그것을 쓰고 신규 생성 안 함
  - 자격 워크플로우(고정 파이프라인+게이트 / 병렬 fan-out / 고빈도 반복) 중 기존 미커버만 후보
  - AskUserQuestion(multiSelect)로 선택 → ./.claude/agents/<name>.md 생성
  - 자격 체인 0건이거나 "생성 안 함" 선택 시 건너뜀 (additive)
  - 디스크 작성 에이전트는 새 세션(또는 /reload-plugins)에서 활성화

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

### /project resume — 설치 완료 후 재개

> 구 `/project init resume`의 레거시 별칭으로 계속 인식됩니다.

```
진입 패턴:
  - "/project resume" 명시적 커맨드 (레거시 별칭 "/project init resume"도 인식)
  - "이어서 진행", "설치 완료", "다시 진행" 자연어 발화

재개 흐름:
  1. .moai/cache/init-progress.json 로드 (Phase 1-3 결과 복원)
  2. Phase 2 Inventory 재실행 (설치 여부 재확인)
  3. Phase 4 Gap Detection 재검증
  4. 누락 0건 → Phase 5 Confirm으로 진행
  5. 여전히 누락 → AskUserQuestion 4 옵션 재제시
```

### Phase 3.5 — Agent Synthesis (프로젝트 에이전트 생성)

Phase 3 체인 설계 직후, **전담 에이전트로 만들 가치가 있는데 매칭되는 기존 코디네이터가 없는** 워크플로우만 프로젝트 전용 서브에이전트(`./.claude/agents/<name>.md`)로 생성하는 선택 단계입니다. 각 도메인 플러그인은 코디네이터 에이전트(`<plugin>/agents/*.md`, 스냅샷 31개)를 번들하므로 **매칭 코디네이터가 있으면 그것을 우선 활용**하고(Phase 3 코디네이터 우선), Phase 3.5는 **커버되지 않는 워크플로우에만** 신규 생성합니다. 매핑·결정 규칙은 `references/core/agent-catalog.md`.

**자격 판정 규칙(Decision Rule)** — 다음 중 하나 이상을 만족할 때만 생성:
- (a) 고정 다단계 파이프라인 + 비우회 컴플라이언스/면책 게이트
- (b) 병렬 fan-out(여러 산출물 동시 생성 후 종합)
- (c) 사용자가 매우 자주 반복하는 동일 파이프라인

단일 스킬·단순 1-2단계 체인은 생성하지 않습니다(orchestrator 인라인 스킬체이닝으로 충분, 에이전트 남발 금지). 자격 체인이 0건이거나 사용자가 "생성 안 함"을 고르면 이 Phase는 건너뜁니다 — **bare `/project`는 에이전트를 하나도 생성하지 않아도 정상 동작합니다(additive)**.

⚠️ **활성화**: 디스크에 작성된 에이전트는 세션 시작 시 로드되므로, 생성 후 **새 세션(또는 `/reload-plugins`)에서 활성화**됩니다.

상세: `references/core/init-protocol.md` §Phase 3.5.

### 스킬 체인 설계 원칙

**코디네이터 우선 (agent-aware)**: 체인 설계 전, 매칭되는 기존 코디네이터 에이전트가 있으면 우선 실행기로 추천한다(상세: `references/core/agent-catalog.md`). 코디네이터가 없을 때만 아래 인라인 스킬 체인을 구성한다. 코디네이터·에이전트는 Cowork 서브에이전트 전용이다.

**체인 구성 요소**:
1. **기획·분석 스킬** — strategy-planner, market-analyst, ux-researcher
2. **생성·제작 스킬** — blog, copywriting, card-news, spec-writer
3. **포맷 변환 스킬** — docx-generator, pptx-designer, xlsx-creator, hwpx-writer, landing-page
4. **미디어 스킬** (선택) — `gpt-image-2-prompt`·`gemini-3-image-prompt`·`midjourney-v8-prompt`(이미지 프롬프트 빌더), `audio-gen`(ElevenLabs MCP TTS·보이스 클로닝·다국어 더빙). 이미지·영상 실제 렌더링은 **Higgsfield MCP**(Soul·DOP·말하는머리·캐릭터) 단일 통합으로 직접 호출.
5. **후처리 스킬** — `ai-slop-reviewer` (텍스트 산출물 체인의 **필수 마지막 단계**)

**체인 표기 규약** (CLAUDE.md에 기록될 형식 — 코디네이터가 있으면 `실행기: <coordinator>` + `폴백:` 인라인 체인을 함께 표기, 상세 `agent-catalog.md` §체인 표기 규약):
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

bare `/project`(레거시 별칭 `/project init`)가 생성하는 CLAUDE.md의 구조:

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

이 스킬은 **이름·회사·역할을 재질문하지 않습니다**.

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

### 도메인 플러그인 (27개)

| 플러그인 | 도메인 | 스킬 수 |
|---------|--------|--------|
| moai-core | 초기화·라우팅·AI 슬롭 검수·피드백·MCP 커넥터 | 8 |
| moai-business | 사업계획·시장조사·IR·소상공인·정부지원 | 11 |
| moai-marketing | SEO·SNS·캠페인·이메일·랜딩진단·메타광고 | 12 |
| moai-legal | 계약서·개인정보·NDA·법인등기 | 5 |
| moai-finance | 세무·결산·재무제표·변동분석 | 6 |
| moai-hr | 근로계약·4대보험·채용·성과평가 | 5 |
| moai-content | 블로그·카드뉴스·랜딩/상세·뉴스레터·카피·HTML·한국어 윤문 | 14 |
| moai-operations | 운영·SOP·벤더관리 | 3 |
| moai-education | 강의운영매뉴얼·후기시퀀스·교육과정·평가 | 6 |
| moai-lifestyle | 여행·웰니스·이벤트 | 3 |
| moai-product | PM·UX·로드맵·스펙 | 4 |
| moai-support | 티켓·응대·KB·에스컬레이션 | 4 |
| moai-office | PPT·DOCX·XLSX·HWPX·PDF·NotebookLM | 6 |
| moai-career | 이력서·자소서·면접·포트폴리오 | 4 |
| moai-data | CSV/Excel·시각화·공공데이터 | 3 |
| moai-public-data | 한국 공공데이터 조회(주식·경매·부동산) | 4 |
| moai-research | 논문·특허·연구비 | 5 |
| moai-media | AI 이미지·영상·음성 | 6 |
| moai-commerce | 한국 이커머스 풀세트 | 30 |
| moai-bi | 경영진 1pager 요약 | 1 |
| moai-pm | 주간 업무보고 | 1 |
| moai-sales | B2B 제안서·RFP | 1 |
| moai-book | 한국 출판 원고 풀스택 | 8 |
| moai-design | Claude Design 보조 | 5 |
| moai-wealth | 개인 재무·재테크 | 6 |
| moai-productivity | 회고·목표·시간·습관 | 7 |
| moai-comms | 직장 커뮤니케이션·보고·회의·피드백 | 5 |

**합계: 27 플러그인 / 173 스킬**

### 관련 프로토콜

상세 프로토콜은 `references/core/`를 참고하세요:

- `init-protocol.md` — bare `/project`(레거시 별칭 `/project init`) Phase 1-8 + Gap Detection + Re-entry 전체 플로우
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