# project Core Protocol — 인덱스

## 개요

Cowork 프로젝트 초기화 + 스킬 체이닝 워크플로우 설계 스킬(`/project`)의 핵심 프로토콜 파일 인덱스.

**현재 상태 요약:**
- 진입점은 서브커맨드 없는 bare `/project`(초기화 기본 동작, Phase 1-8). `/project init`은 레거시 별칭으로 계속 인식.
- Phase 2 Inventory(Bash + system reminder 교차 검증) + Phase 4 Gap Detection(누락 감지 → 설치 안내 → 재개).
- 설치 완료 후 재개는 `/project resume`(구 `/project init resume` 별칭).
- 글로벌 프로필 시스템 없음 (`profile-manager.md` 삭제) — 이름·회사·역할을 프로젝트마다 묻지 않음.
- 스킬 체이닝 기반 워크플로우 설계(Phase 3) + CLAUDE.md 외부 템플릿화.
- HARD 규칙: office/web 스킬 우선 + AI 슬롭 후처리 고정 포함.

---

## 파일 목록 (10개)

### 1. router.md — 자연어 → 플러그인 라우팅
27개 플러그인 키워드 매핑, 모호성 해소, 복합 요청 분기.

### 2. init-protocol.md — bare `/project` 전체 플로우 (레거시 별칭 `/project init`)
Phase 1 인터뷰 → Phase 2 Inventory → Phase 3 체인 설계 → Phase 4 Gap Detection → Phase 5 확인 → Phase 6 CLAUDE.md 생성 → Phase 7 API 키 → Phase 8 안내.
Gap Detection 알고리즘, Re-entry 흐름, inventory.json·init-progress.json 스키마 포함.

### 3. context-collector.md — 맥락 수집 프로토콜
맥락 충분성 등급(A/B/C), 모호성 감지, AskUserQuestion 전략.

### 4. claudemd-generator.md — CLAUDE.md 생성 프로토콜
`references/templates/CLAUDE.md.tmpl` 변수 치환 규칙, 200라인 예산, HARD 규칙 고정 블록.

### 5. execution-protocol.md — 스킬 체인 실행 프로토콜
플러그인 트리거 → 체인 순차 실행 → 단계별 요약 → ai-slop-reviewer 종료.

### 6. evaluation-protocol.md — 평가 프로토콜
5개 차원 평가: 정확성, 완전성, 실용성, 톤 적합성, 도메인 적합성.

### 7. evolution-protocol.md — 자기학습 진화 프로토콜
Self-Refine 사이클: 반성 → 피드백 → 패턴 → 업데이트 → 학습.

### 8. diagnostic-protocol.md — 진단 프로토콜
`/project doctor`, `/project status` 커맨드. 환경 상태 진단.

### 9. quality-evaluator.md — 품질 자동 평가
산출물 품질 자동 검증, AI 슬롭 체크리스트 포함.

### 10. agent-catalog.md — 코디네이터 에이전트 인지 & 체인 설계
31개 코디네이터 에이전트 동적 인벤토리(Phase 2 `agents_available`), 코디네이터 우선 체인 설계(Phase 3), 기존 우선 에이전트 생성(Phase 3.5 Step 0), 도메인 매핑·Cowork 제약·체인 표기 규약 SSOT.

### (삭제됨) profile-manager.md
**전면 제거됨**. 이름·회사·역할을 프로젝트마다 묻지 않는 정책으로 전환.

---

## templates/

- `CLAUDE.md.tmpl` — `/project init` Phase 6에서 로드되는 CLAUDE.md 생성 템플릿.

---

## 파일 간 의존성

```
router.md → init-protocol.md → context-collector.md
                ↓
    claudemd-generator.md (templates/CLAUDE.md.tmpl 로드)
                ↓
    execution-protocol.md → evaluation-protocol.md
                ↓
    evolution-protocol.md ← diagnostic-protocol.md ← quality-evaluator.md
```

---

## 스킬 체이닝 핵심 원칙

1. 텍스트 산출물 체인은 **반드시 `ai-slop-reviewer`로 종료**한다.
2. 체인은 [기획/분석 → 생성 → 포맷 변환 → 검수] 구조를 기본으로 한다.
3. 비텍스트 산출물(차트·데이터·숫자·음성)은 ai-slop 단계를 생략한다.
4. 체인 정의는 `/project init` Phase 3에서 생성되어 CLAUDE.md에 기록된다.
5. DOCX/PPTX/XLSX/HWPX/HTML 포맷은 Claude 기본 artifacts가 아닌 **moai-office/moai-content 스킬 우선**.
6. **Gap Detection**: Phase 4에서 체인의 각 스킬을 Inventory와 대조해 누락 플러그인을 자동 감지하고, 설치 안내 후 Re-entry로 재개한다.
7. **코디네이터 우선 (agent-aware)**: 체인 설계 시 매칭되는 기존 코디네이터 에이전트를 우선 활용하고(`agent-catalog.md`), 없을 때만 인라인 스킬 체인 또는 신규 에이전트 생성으로 내려간다.

---

## 27개 플러그인 목록 (moai-core 오케스트레이터 + 26 도메인 플러그인)

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

**합계: 27 플러그인, 173 스킬**

---

## 2계층 아키텍처

```
계층 1: 플러그인 (Read-Only) — 27개 플러그인 (moai-core + 26 도메인 플러그인) + 스킬
         ↑ Phase 2 Inventory: Bash ~/.claude/plugins/ + system reminder 교차 검증
         ↑ Phase 4 Gap Detection: 체인 스킬 ↔ Inventory 대조 → 누락 감지 → 설치 안내
계층 2: ./CLAUDE.md (자동 로딩) — 프로젝트별 맞춤형 페르소나 + 스킬 체인 정의
         + ./.moai/ — 설정, 컨텍스트, API 키
         + .moai/cache/inventory.json — 활성 스킬 인벤토리
         + .moai/cache/init-progress.json — Re-entry 재개 상태
         + auto-memory — Claude 자율 저장 (세션 간 학습 누적)

❌ 제거됨: 글로벌 프로필 계층 (moai-profile.md, [MoAI 프로필])
```
