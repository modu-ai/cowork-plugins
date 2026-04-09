# MoAI Core Protocol — v0.3.0 인덱스

## 개요
MoAI-Cowork v0.3.0의 핵심 프로토콜 10개 파일 인덱스.
v0.2.0 대비 변경: 11개 스킬 그룹 → 14개 독립 플러그인 아키텍처로 전환.
모든 파일은 한국어로 작성. 4계층 아키텍처 반영.

**버전**: v0.3.0
**생성일**: 2026-04-09

---

## 10개 파일 목록

### 1. router.md — 자연어 → 플러그인 라우팅 프로토콜
사용자의 자연어 요청을 분석하여 **14개 독립 플러그인** 중 적합한 플러그인으로 라우팅.
키워드 매핑, 모호성 해소, 복합 요청 분기.

### 2. init-protocol.md — /moai init 전체 플로우
5단계 Phase: 프로필 감지 → 기본 프로필 → 카테고리 선택 → 하네스 선택 → CLAUDE.md 생성.
rules/ 제거, CLAUDE.md에 모든 내용 통합.

### 3. context-collector.md — 맥락 수집 프로토콜
맥락 충분성 등급 (A/B/C), 모호성 감지, AskUserQuestion 전략.

### 4. profile-manager.md — 글로벌 프로필 관리
/mnt/.auto-memory/moai-profile.md 중심. 개인 + 회사 프로필 CRUD.

### 5. claudemd-generator.md — CLAUDE.md 생성 프로토콜
하네스 레퍼런스 기반 맞춤형 CLAUDE.md 자동 생성. 하네스 전체 복사 원칙.

### 6. execution-protocol.md — 하네스 실행 프로토콜
플러그인 트리거 → 레퍼런스 로드 → 산출물 생성 → 검토.

### 7. evaluation-protocol.md — 평가 프로토콜
5개 차원 평가: 정확성, 완전성, 실용성, 톤 적합성, 도메인 적합성.

### 8. evolution-protocol.md — 자기학습 진화 프로토콜
Self-Refine 사이클: 반성 → 피드백 → 패턴 → 업데이트 → 학습.

### 9. diagnostic-protocol.md — 진단 프로토콜
/moai doctor, /moai status 명령어. 환경 상태 진단.

### 10. .mcp.json — sequential-thinking MCP 설정
복잡 작업, --deepthink 시 mcp__sequential-thinking__sequentialthinking 호출.

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
| 라우팅 단위 변경 | 11개 스킬 그룹 → 14개 독립 플러그인 |
| router.md | 14 plugin 매핑 테이블로 재작성 |
| 아키텍처 | 5계층 플러그인 구조 반영 |

## 14개 플러그인 목록

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
| moai-schedules | 스케줄, 예약, 자동실행 |

## 4계층 아키텍처 (업데이트)

```
계층 0: auto-memory (글로벌) — 프로필, 하네스 이력
계층 1: 플러그인 (read-only) — 14개 플러그인 + 레퍼런스 + 스크립트
계층 2: .claude/CLAUDE.md (자동 로딩) — 맞춤형 페르소나 + 워크플로우
계층 3: .moai/ (R/W) — 도메인 맥락, 진화 데이터
계층 4: auto-memory 학습 — 세션 간 피드백 누적
```
