# MoAI Core Protocol — v1.0.0 인덱스

## 개요
MoAI-Cowork v1.0.0의 핵심 프로토콜 10개 파일 인덱스.
v0.2.0 대비 변경: 11개 스킬 그룹 → 16개 독립 플러그인 아키텍처로 전환.
모든 파일은 한국어로 작성. 3계층 아키텍처 반영.

**버전**: v1.0.0
**생성일**: 2026-04-10

---

## 10개 파일 목록

### 1. router.md — 자연어 → 플러그인 라우팅 프로토콜
사용자의 자연어 요청을 분석하여 **16개 독립 플러그인** 중 적합한 플러그인으로 라우팅.
키워드 매핑, 모호성 해소, 복합 요청 분기.

### 2. init-protocol.md — /moai init 전체 플로우 (v2.0)
5단계 Phase: 프로필 감지 → 빠른 프로필(1질문) → 플러그인 자동 감지 → 커넥터+API 키 → CLAUDE.md+첫 실행.
setup-cowork + claude-code-setup 패턴 융합. 맥락 수집은 Lazy Collection으로 이동.
~3분 내 완료. AskUserQuestion 최대 5회.

### 3. context-collector.md — 맥락 수집 프로토콜
맥락 충분성 등급 (A/B/C), 모호성 감지, AskUserQuestion 전략.

### 4. profile-manager.md — 글로벌 프로필 관리
Claude 메모리의 moai-profile.md 중심. 개인 + 회사 프로필 CRUD.

### 5. claudemd-generator.md — CLAUDE.md 생성 프로토콜
하네스 레퍼런스 기반 맞춤형 CLAUDE.md 자동 생성. 200라인 이내 맞춤형 CLAUDE.md 생성.

### 6. execution-protocol.md — 하네스 실행 프로토콜
플러그인 트리거 → 레퍼런스 로드 → 산출물 생성 → 검토.

### 7. evaluation-protocol.md — 평가 프로토콜
5개 차원 평가: 정확성, 완전성, 실용성, 톤 적합성, 도메인 적합성.

### 8. evolution-protocol.md — 자기학습 진화 프로토콜
Self-Refine 사이클: 반성 → 피드백 → 패턴 → 업데이트 → 학습.

### 9. diagnostic-protocol.md — 진단 프로토콜
/moai doctor, /moai status 명령어. 환경 상태 진단.

### 10. (예비)
딥씽킹(--deepthink)은 Claude 네이티브 추론으로 수행. 별도 MCP 불필요.

---

## 파일 간 의존성

```
router.md → init-protocol.md → profile-manager.md → context-collector.md
    ↓
claudemd-generator.md → execution-protocol.md → evaluation-protocol.md
    ↓
evolution-protocol.md ← diagnostic-protocol.md
```

## v0.2.0 대비 변경 항목

| 변경 사항 | 내용 |
|---------|------|
| 라우팅 단위 변경 | 11개 스킬 그룹 → 16개 독립 플러그인 |
| router.md | 16 plugin 매핑 테이블로 재작성 |
| 아키텍처 | 3계층 플러그인 구조 반영 |

## 16개 플러그인 목록

| 플러그인 | 도메인 |
|---------|--------|
| moai-core | 핵심 오케스트레이션, 라우팅, 프로필 |
| moai-business | 비즈니스 전략, 스타트업, 시장조사 |
| moai-marketing | 마케팅, SEO, SNS, 광고 |
| moai-legal | 법률, 계약서, 컴플라이언스 |
| moai-finance | 재무, 세무, 부가세, 홈택스 |
| moai-hr | 인사, 노무, 채용, 퇴직금 |
| moai-content | 콘텐츠, 카드뉴스, 블로그, 뉴스레터 |
| moai-operations | 운영, 결재, 조달, SOP |
| moai-education | 교육, 논문, 커리큘럼 |
| moai-lifestyle | 여행, 건강, 웨딩, 이벤트 |
| moai-product | 제품, PM, UX, 로드맵 |
| moai-support | 고객지원, CS, 티켓 |
| moai-office | 문서, PPT, 한글, 엑셀 |
| moai-career | 이력서, 면접, 포트폴리오, 취업 |
| moai-data | 데이터 분석, CSV/Excel, 공공데이터, 시각화 |
| moai-research | 논문, 특허, 연구비, 선행기술 조사 |

## 3계층 아키텍처 (v1.0.0)

```
계층 1: 플러그인 (Read-Only) — 16개 플러그인 + 레퍼런스 + 스크립트
계층 2: ./CLAUDE.md (자동 로딩, R/W) — 맞춤형 페르소나 + 워크플로우
계층 3: 프로젝트 데이터 (R/W)
  ├── .moai/ — 도메인 맥락, 진화 데이터, 설정
  └── Claude 메모리 (memory/) — 글로벌 프로필, API 키, 교차 프로젝트 데이터

+ auto-memory: Claude 자율 저장 (세션 간 학습 누적)
```
