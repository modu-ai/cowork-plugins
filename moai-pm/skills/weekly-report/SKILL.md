---
name: weekly-report
description: |
  한국 팀의 주간 비즈니스 리뷰(WBR) 보고서 자동 생성 스킬입니다.
  일일 노트·완료 태스크·KPI 데이터를 입력받아 임원/팀 두 버전(격식체/구어체)으로 작성합니다.
  Notion·Linear·Asana·Slack MCP가 가용하면 자동 데이터 fetch, 없어도 자유 텍스트 입력 fallback.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "주간보고 작성", "WBR 준비", "이번 주 한 일 정리"
  - "주간 회의 자료", "위클리 리포트", "주간 업무 보고"
  - "임원 주간보고", "팀 주간보고"
user-invocable: true
version: 2.2.1
---

# Weekly Report — 한국 팀 주간보고(WBR) 자동 생성

> moai-pm | 한국 주간보고 문화 + 글로벌 베스트 프랙티스

## 개요

월요 오전 WBR(Weekly Business Review) 또는 금요 마무리 보고용 주간 리포트를 자동 작성합니다. 한국 직장 문화에서 정착된 6섹션 표준(KPI / Done / In Progress / Plan / Risks / Decisions)을 기본으로 하며, 임원용 1pager와 팀 내부 상세 두 버전을 동시 생성합니다.

## 트리거 키워드

주간보고 WBR 위클리 리포트 주간 회의자료 주간 업무보고 weekly report 임원 주간보고 팀 주간보고

## 워크플로우

### 1단계: 데이터 소스 자동 감지 (3-tier fallback)

| Tier | 소스 | 동작 |
|---|---|---|
| 1 | Notion·Linear·Asana MCP 가용 | 데이터베이스/이슈 자동 fetch |
| 2 | CSV/JSON 업로드 | 외부 도구 export 파싱 |
| 3 | 자유 텍스트 메모 | 사용자가 정리한 내용 그대로 활용 |

MCP 가용 시 자동 우선 활용. 사용자가 명시적으로 텍스트 입력 시 그대로 처리.

### 2단계: 6섹션 본문 생성 (한국 WBR 표준)

| # | 섹션 | 내용 |
|---|---|---|
| 1 | 이번 주 핵심 (KPI) | 사전 정의된 지표 달성치·목표 대비 % |
| 2 | 완료 (Done) | PR·티켓·기능 단위, 임팩트 정량 |
| 3 | 진행 중 (In Progress) | 다음 주 완료 예정 항목·진행률 |
| 4 | 차주 계획 (Plan) | priority labels (P0/P1/P2) — 시간 단위 추정 금지 |
| 5 | 이슈·리스크 | 외부 의존성, 일정 압박, 기술 부채 |
| 6 | 의사결정 요청 | 임원/PM 결정 필요 항목 + 옵션 |

### 3단계: 톤 자동 적용

사용자가 톤을 지정하지 않으면 대상별 자동 매핑:

- **임원 보고**: 격식체 ("~합니다", "~로 판단됩니다")
- **팀 내부 (Slack 등)**: 해요체 ("~했어요", "~할 예정이에요")
- **혼합**: 두 버전 동시 출력

### 4단계: 임원 1pager 별도 생성 (선택)

≤ 250 단어로 압축:
- KPI 헤드라인 1줄
- 완료 핵심 3개 (각 1줄, 정량)
- 리스크 1개
- 의사결정 요청 1-2개

### 5단계: 후처리 가이드

- **executive-summary**: 1pager를 더 압축된 C-level 보고로 변환
- **ai-slop-reviewer**: 격식체 톤 검수 (CLAUDE.local.md §3-2)
- **pptx-designer**: 슬라이드 발표 자료로 출력

## 출력 형식

```markdown
# 주간보고 — [팀명] (2026년 W18, 5/1~5/7)

## 1. 이번 주 핵심 (KPI)
- MAU: 12,450 (목표 12,000 대비 +3.8%)
- 신규 가입: 320 (목표 300 대비 +6.7%)

## 2. 완료 (Done)
- [Feature] 결제 페이지 v2 — PR #234 머지, 결제 성공률 +2.1pp
- [Bug] 로그인 500 에러 — 영향 사용자 ~30명, 핫픽스 배포

## 3. 진행 중 (In Progress)
- 알림 시스템 리팩토링 — 70% 완료, 차주 머지 목표

## 4. 차주 계획 (Plan)
- [P0] 결제 모듈 보안 감사 대응
- [P1] 마케팅 캠페인 페이지 제작
- [P2] 백엔드 의존성 업데이트

## 5. 이슈·리스크
- 외부 SMS API 응답 지연 → backup 채널 검토 필요
- 디자인팀 리소스 부족으로 차주 일부 작업 후순위

## 6. 의사결정 요청
- 보안 감사 대응 인력 추가 (옵션 A: 외주, B: 내부 재배치)
```

임원 1pager (≤ 250 단어):
```markdown
# Executive Brief — W18

**KPI**: MAU 12.4K (+3.8% vs 목표), 가입 320 (+6.7%)
**완료**: 결제 v2 머지(전환 +2.1pp) / 로그인 500 핫픽스 / 알림 70%
**리스크**: SMS API 지연 — 백업 채널 검토 중
**결정 요청**: 보안 감사 대응 — 외주 vs 내부 재배치
```

## 사용 예시

**예시 1 — Notion MCP 자동 fetch**
```
사용자: "이번 주 주간보고 만들어줘. 우리 팀 Notion DB 'Weekly Tasks' 참고."
→ Notion MCP로 W18 완료 태스크·진행 중 자동 수집
→ 6섹션 격식체 보고 + 임원 1pager 두 버전 출력
```

**예시 2 — 자유 텍스트 fallback (해요체)**
```
사용자: "이번 주 한 일 정리해줘. 결제 v2 머지했고, 로그인 버그 잡았고, 알림 리팩토링 70% 됐어."
→ 자유 텍스트 파싱 후 해요체 팀 내부 보고로 변환
```

## 주의사항

- **시간 추정 금지**: "다음 주 화요일까지 완료" 같은 직접 날짜·시간 추정은 priority labels로 변환
- **개인 평가 금지**: 팀원 개인 비난·칭찬은 본문에 자동 포함되지 않음 (필요 시 별도 1:1)
- **확인되지 않은 수치 금지**: KPI 데이터 출처(BI 도구·내부 DB) 명시 또는 [추정] 태그
- **NDA 정보 주의**: 외부 공유용 보고서 작성 시 회사 비밀 정보 자동 검사 (`moai-legal/nda-triage` 권고)

## 관련 스킬

**Before**:
- `moai-pm/standup-summarizer` — 일일 스탠드업 노트 누적
- (Notion·Linear·Asana MCP) — 자동 데이터 fetch

**After**:
- `moai-bi/executive-summary` — C-level 1pager로 더 압축
- `moai-core/ai-slop-reviewer` — AI 패턴 검수
- `moai-office/pptx-designer` — 발표 슬라이드 출력

**Alternative**:
- `moai-business/daily-briefing` — 일간 보고 (주간이 아닌 일일)
- `moai-pm/retro-facilitator` — 분기 회고 (주간이 아닌 분기)

## 관련 커맨드

- (CLAUDE.local.md §3-3 등록 체인)
  - 주간보고 → 임원 1pager: `standup-summarizer → weekly-report → executive-summary`
  - 발표 슬라이드: `weekly-report → ai-slop-reviewer → pptx-designer`

## 출처

- 글로벌 베스트 프랙티스: Notion AI WBR 템플릿 (KPI/Done/Plan/Risk 4섹션), Linear Cycles 1-2주 단위, Asana Status Updates (Green/Yellow/Red)
- 한국 직장 문화: 월요 오전 WBR, 금요 마무리 보고
- McKinsey Pyramid Principle (결론 → 근거 → 데이터)