---
name: threads-schedule
description: |
  PENDING 상태의 Threads 포스트를 검토하고 승인한 뒤 발행 예약 시간을 설정합니다. 사용자의 승인을 거쳐야만 PENDING → APPROVED로 상태를 변경합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 포스트 승인해줘"
  - "PENDING 포스트 뭐야?"
  - "내일 아침 9시에 발행하게 예약해줘"
  - "이번 주 포스트들 미리 승인해줘"
  [책임 경계] vs 형제 스킬: 승인·예약만 담당합니다. 초안 작성은 threads-post-draft, 상태 조회는 threads-status, 실제 발행은 세션 안에서 threads_queue_publish_due 도구가 담당합니다. (자동 백그라운드 발행은 없습니다 — 발행하려면 세션을 켜야 합니다.)
version: "1.0.0"
---

# Threads 승인 및 예약 (threads-schedule)

## 개요

PENDING 상태의 포스트를 검토하고 사용자 승인을 받은 뒤 **APPROVED** 상태로 변경하며 발행 예약 시간을 설정합니다. APPROVED 포스트는 `scheduled_at` 에 도달한 뒤 세션 안에서 `threads_queue_publish_due` 로 발행합니다.

> **주의**: launchd/cron 기반 자동 발행은 제거되었습니다. 발행하려면 반드시 **세션을 켜고** `threads_queue_publish_due` 를 호출해야 합니다. 베스트 프랙티스는 주 3-5회 화/수/목 발행 — `threads_queue_add_batch` 로 분산 예약하면 이 케이던스가 자동 적용됩니다.

## 트리거 키워드

Threads, 승인, 예약, PENDING, APPROVED, 발행 시간, 스케줄, 승인审查, 확인

## 워크플로우

### 1단계: PENDING 포스트 조회

`threads_queue_list(status="PENDING")` 또는 `threads_queue_get(post_id)`로 대상 포스트를 조회합니다:

```python
# 전체 PENDING 목록
threads_queue_list(status="PENDING", limit=50)

# 특정 포스트 상세
threads_queue_get(post_id=123)
```

### 2단계: 초안 검토 및 사용자 승인

조회된 초안을 사용자에게 보여주고 승인을 받습니다:

- **HARD 규칙**: 자동 승인 금지 — 반드시 사용자 확인 필요 ("자동 아닌 자율")
- 수정 요청 시: 초안 변경 후 `threads_queue_add`로 재등록 요청
- 거부 시: 포스트를 큐에서 삭제 (또는 `threads_queue_list`로 상태만 확인)

### 3단계: 승인 처리 — PENDING → APPROVED

사용자 승인 후 `threads_queue_approve` 도구를 호출합니다:

```python
threads_queue_approve(
    post_id=123,
    scheduled_at=None  # 즉시 due, 또는 ISO-8601 시각 (선택)
)
```

- `post_id`: 조회된 포스트 ID
- `scheduled_at`:
  - 미지정(`None`) = 현재 시각으로 예약 (즉시 due, `threads_queue_publish_due` 호출 시 즉시 발행)
  - ISO-8601 시각 = 특정 시각 예약 (예: `"2025-01-15T09:00:00+09:00"`)
  - 이미 예약된 시각을 덮어쓰려면 명시적으로 전달

### 4단계: 발행 경로 안내

APPROVED 포스트의 발행은 **세션 안에서** 이루어집니다 (자동 백그라운드 발행 없음):

- **분산 예약(권장)**: 초안 여러 개는 `threads_queue_add_batch(cadence="weekly_3")` 로 화/수/목 12:00 슬롯에 미리 분산 — 아래 "분산 발행" 섹션 참고.
- **세션 발행**: `scheduled_at` 도달 후 세션 안에서 `threads_queue_publish_due(limit=10)` 호출 → 실제 발행.
- **발행 결과**: `threads_queue_list(status="PUBLISHED")` 또는 `threads-status` 스킬로 확인.

## 분산 발행 (distributed publishing)

승인된 초안 N 개를 `threads_queue_add_batch` 로 한 번에 예약하면, 베스트 슬롯(Asia/Seoul 12:00)에 하루 1건씩 자동 분산됩니다. 이 모델의 전체 흐름:

```
초안 N개 (PENDING)
   │  threads_queue_add_batch(cadence="weekly_3", approve=True)
   ▼
APPROVED + 화/수/목 12:00 예약  ── (세션 안에서 scheduled_at 도달) ──> threads_queue_publish_due ──> PUBLISHED
```

### 세션 단위 한계 (솔직 안내)

- **launchd 자동 발행은 없습니다.** `scheduled_at` 이 도래해도 세션이 꺼져 있으면 발행되지 않습니다.
- 발행하려면 세션을 켜고 `threads_queue_publish_due` 를 호출해야 합니다. 예약된 포스트가 여러 개 쌓여 있으면 한 번의 호출로 모두 flush 됩니다.
- 케이던스(주 3-5회 화/수/목)는 "언제 올리면 좋은가"의 가이드이지 자동 트리거가 아닙니다. 값은 `config/threads.yaml` 참조.

## 예약 시간 설정 가이드

### scheduled_at 예시

| 요청 | scheduled_at 값 | 설명 |
|------|-----------------|------|
| "지금" | `None` (미지정) | 현재 시각으로 due (즉시 발행 가능) |
| "내일 아침 9시" | `"2025-01-15T09:00:00+09:00"` | 내일 오전 9시 (KST) |
| "다음 주 월요일 10시" | `"2025-01-20T10:00:00+09:00"` | 다음 주 월요일 오전 10시 |
| "이번 달 말 30일 오후 6시" | `"2025-01-30T18:00:00+09:00"` | 1월 30일 오후 6시 |

### ISO-8601 형식 (한국 시간)

```
YYYY-MM-DDTHH:MM:SS+09:00
│   │   │ │   │  │   │
│   │   │ │   │  │   └─ 한국 시간 (UTC+9)
│   │   │ │   │  └───── 초 (선택)
│   │   │ │   └─────── 분
│   │   │ └────────── 시
│   │   └──────────── 날짜 구분자 (T)
│   └──────────────── 날짜 (DD)
└───────────────────── 월 (MM)
```

## 출력 형식

```markdown
## 승인 완료 (APPROVED)

**포스트 ID**: N
**상태**: PENDING → APPROVED
**승인 시각**: 2025-01-14T15:30:00+09:00

**예약 시각**:
- scheduled_at: 2025-01-15T09:00:00+09:00 (내일 아침 9시)

**발행 경로**:
1. 세션 발행: `threads_queue_publish_due(limit=10)` 도구로 `scheduled_at` 도달 포스트 flush (세션 안에서만)

**다음 단계**:
- 발행 결과 확인: `threads-status` 스킬 또는 `threads_queue_list(status="PUBLISHED")`
- 다른 PENDING 포스트: `threads_queue_list(status="PENDING")`로 확인
```

## 주의사항

| 상황 | 대응 |
|------|------|
| post_id 없음 에러 | `threads_queue_list(status="PENDING")`로 ID 재확인 |
| 초안 수정 요청 시 | `threads_queue_add`로 수정된 초안 재등록 후 재승인 |
| 예약 시각 과거 | 현재 시각 이후의 시각으로 재설정 요청 |
| 사용자 승인 없이 자동 승인 | 금지 — HARD 규칙 위반 |
| 이미 APPROVED된 포스트 | 상태 변화 없음 (idempotent) |

## References

| 파일 | 로드 조건 |
|------|-----------|
| references/approval-flow.md | 승인 플로우·상태 전이·에러 케이스 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `threads-post-draft` | PENDING 포스트 생성 |
| `threads-status` | 발행 결과 조회 (PUBLISHED/FAILED) |

## 이 스킬을 사용하지 말아야 할 때

- 초안 작성: `threads-post-draft` 스킬 사용
- 상태 조회: `threads-status` 스킬 사용
- 즉시 발행(승인 없이): MCP 도구 `threads_publish_text` 직접 호출
- 발행 결과 조회: `threads-status` 스킬 사용

---

## 발행 전 설정 (최초 1회)

이 스킬을 사용하려면 Threads OAuth 자격증명이 필요합니다. 최초 1회 설정:

```bash
# 환경변수 설정
export THREADS_ACCESS_TOKEN="<장기 토큰(60일)>"
export THREADS_USER_ID="<Threads 사용자 ID>"

# 선택: 발행 전 대기 시간(초), 기본 30초
export THREADS_PUBLISH_DELAY="30"
```

발급 절차: `mcp-servers/threads-poster/CONNECTORS.md` 참조 (브라우저 인가 → 단기 토큰 → 장기 토큰 교환)

**동작 확인**: `threads_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.
