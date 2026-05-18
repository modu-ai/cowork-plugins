# project Core Protocol — v2.11.0 인덱스

## 개요

Cowork 프로젝트 초기화 + 스킬 체이닝 워크플로우 설계 스킬(`/project`)의 핵심 프로토콜 파일 인덱스.

**v2.11.0 주요 변경:**
- Phase 2 Inventory 구체 메커니즘 도입 (Bash + system reminder 교차 검증)
- Phase 4 Gap Detection 신규 — 누락 플러그인/스킬 자동 감지 + 설치 안내 + Re-entry
- `/project init resume` 커맨드 신규 — 설치 완료 후 재개 흐름
- moai-media 7 스킬 → 4 스킬 (Higgsfield·ElevenLabs MCP 직접 지원 반영)
- 17 플러그인 → 22 플러그인 (moai-book·moai-bi·moai-pm·moai-sales·moai-commerce 추가)

**v1.3.0 주요 변경 (기준선):**
- `/moai init` → `/project init` 커맨드 이름 변경
- **글로벌 프로필 시스템 제거** (`profile-manager.md` 삭제)
- 스킬 체이닝 기반 워크플로우 설계(Phase 3) 신규 도입
- CLAUDE.md 외부 템플릿화 (`references/templates/CLAUDE.md.tmpl`)
- HARD 규칙: office/web 스킬 우선 + AI 슬롭 후처리 고정 포함

**버전**: v2.11.0
**최종 업데이트**: 2026-05-18

---

## 파일 목록 (9개)

### 1. router.md — 자연어 → 플러그인 라우팅
22개 플러그인 키워드 매핑, 모호성 해소, 복합 요청 분기.

### 2. init-protocol.md — /project init 전체 플로우 (v2.11.0)
Phase 1 인터뷰 → Phase 2 Inventory → Phase 3 체인 설계 → Phase 4 Gap Detection → Phase 5 확인 → Phase 6 CLAUDE.md 생성 → Phase 7 API 키 → Phase 8 안내.
**신규**: Gap Detection 알고리즘, Re-entry 흐름, inventory.json·init-progress.json 스키마.

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

### (삭제됨) profile-manager.md
v1.3.0에서 **전면 제거**. 이름·회사·역할을 프로젝트마다 묻지 않는 정책으로 전환.

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
6. **Gap Detection (v2.11.0 신규)**: Phase 4에서 체인의 각 스킬을 Inventory와 대조해 누락 플러그인을 자동 감지하고, 설치 안내 후 Re-entry로 재개한다.

---

## 22개 플러그인 목록 (moai-core 오케스트레이터 + 21 도메인 플러그인)

| 플러그인 | 도메인 | 스킬 수 |
|---------|--------|--------|
| moai-core | 초기화, 라우팅, AI 슬롭 검수, 피드백 | 8 |
| moai-business | 비즈니스 전략, 스타트업, 시장조사 | 10 |
| moai-marketing | 마케팅, SEO, SNS, 광고 | 11 |
| moai-legal | 법률, 계약서, 컴플라이언스 | 5 |
| moai-finance | 재무, 세무, 부가세, 홈택스 | 6 |
| moai-hr | 인사, 노무, 채용, 퇴직금 | 5 |
| moai-content | 콘텐츠, 카드뉴스, 블로그, 뉴스레터, 랜딩 | 12 |
| moai-operations | 운영, 결재, 조달, SOP | 3 |
| moai-education | 교육, 커리큘럼, 평가 | 5 |
| moai-lifestyle | 여행, 건강, 웨딩, 이벤트 | 3 |
| moai-product | 제품, PM, UX, 로드맵 | 4 |
| moai-support | 고객지원, CS, 티켓 | 4 |
| moai-office | 문서, PPT, 한글, 엑셀, PDF | 5 |
| moai-career | 이력서, 면접, 포트폴리오, 취업 | 4 |
| moai-data | 데이터 분석, 공공데이터, 시각화 | 3 |
| moai-research | 논문, 특허, 연구비, 선행기술 | 5 |
| moai-media | 이미지 프롬프트 빌더, 음성(ElevenLabs MCP) | 4 |
| moai-commerce | 한국 이커머스 풀스택 | 35 |
| moai-book | 한국 출판사 제출용 원고 | 8 |
| moai-bi | 비즈니스 인텔리전스, HTML 리포트 | 1 |
| moai-pm | 프로젝트 관리, 주간보고 | 1 |
| moai-sales | 영업, 제안서 | 1 |

**합계: 22 플러그인, 143 스킬**

---

## 2계층 아키텍처 (v2.11.0)

```
계층 1: 플러그인 (Read-Only) — 22개 플러그인 (moai-core + 21 도메인 플러그인) + 스킬
         ↑ Phase 2 Inventory: Bash ~/.claude/plugins/ + system reminder 교차 검증
         ↑ Phase 4 Gap Detection: 체인 스킬 ↔ Inventory 대조 → 누락 감지 → 설치 안내
계층 2: ./CLAUDE.md (자동 로딩) — 프로젝트별 맞춤형 페르소나 + 스킬 체인 정의
         + ./.moai/ — 설정, 컨텍스트, API 키
         + .moai/cache/inventory.json — 활성 스킬 인벤토리
         + .moai/cache/init-progress.json — Re-entry 재개 상태
         + auto-memory — Claude 자율 저장 (세션 간 학습 누적)

❌ 제거됨: 글로벌 프로필 계층 (moai-profile.md, [MoAI 프로필])
```
