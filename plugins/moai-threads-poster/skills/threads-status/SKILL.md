---
name: threads-status
description: |
  Threads 발행 큐의 상태를 조회합니다. PENDING/APPROVED/PUBLISHED/FAILED 포스트 목록과 단일 포스트 상세를 읽기 전용으로 제공합니다.
  다음과 같은 요청 시 사용하세요:
  - "뭐가 대기중이야?"
  - "이번 주 뭐 올라갔어?"
  - "실패한 거 있어?"
  - "이 포스트 상태는?"
  - "큐에 얼마나 쌓여있어?"
  [책임 경계] vs 형제 스킬: 읽기 전용 조회만 담당합니다. 초안 작성은 threads-post-draft, 승인·예약은 threads-schedule, 발행은 세션 안에서 threads_queue_publish_due 도구가 담당합니다. 이 스킬은 절대 쓰기/승인/발행을 하지 않습니다.
version: "1.0.0"
---

# Threads 상태 조회 (threads-status)

## 개요

Threads 발행 큐의 상태를 **읽기 전용**으로 조회합니다. PENDING/APPROVED/PUBLISHED/FAILED 포스트 목록과 단일 포스트 상세를 제공하며, 큐 건강 상태와 통계를 확인할 수 있습니다.

> **예약 포스트(APPROVED + 미래 `scheduled_at`)**: `threads_queue_add_batch` 등으로 분산 예약된 포스트들은 `scheduled_at` 이 도달한 뒤 세션 안에서 `threads_queue_publish_due` 로 flush 됩니다. 자동 백그라운드 발행(launchd) 은 없으므로, 예약 분량이 쌓여 있으면 세션을 켜고 `threads_queue_publish_due` 를 한 번 호출해 한꺼번에 발행하세요.

## 트리거 키워드

상태, 조회, 목록, 확인, PENDING, APPROVED, PUBLISHED, FAILED, 대기, 발행 완료, 실패, 큐

## 워크플로우

### 1단계: 질문 유형 판별

사용자의 자연어 질문을 적절한 상태 필터와 조회 도구로 매핑합니다:

| 질문 유형 | 상태 필터 | 도구 |
|----------|----------|------|
| "뭐가 대기중이야?" | `status="PENDING"` | `threads_queue_list` |
| "승인된 거 뭐야?" | `status="APPROVED"` | `threads_queue_list` |
| "이번 주 뭐 올라갔어?" | `status="PUBLISHED"` | `threads_queue_list` |
| "실패한 거 있어?" | `status="FAILED"` | `threads_queue_list` |
| "전체 목록" | `status=None` (미지정) | `threads_queue_list` |
| "이 포스트 상태는?" | (post_id 지정) | `threads_queue_get` |
| "큐에 얼마나 쌓여있어?" | `status=None` + 통계 | `threads_queue_list` |

### 2단계: 조회 도구 호출

**목록 조회**:

```python
# PENDING 포스트 전체
threads_queue_list(status="PENDING", limit=50)

# 발행 완료 (최근 10개)
threads_queue_list(status="PUBLISHED", limit=10)

# 전체 (미지정 시 전체 상태)
threads_queue_list(limit=100)
```

**단일 포스트 상세**:

```python
# post_id로 상세 조회
threads_queue_get(post_id=123)
```

### 3단계: 결과 정리 및 요약

조회된 결과를 사용자에게 보기 좋게 정리합니다:

- **목록**: 포스트 ID, 상태, 미디어 타입, 예약 시각, 발행 시각/에러 메시지
- **단일 포스트**: 전체 row 데이터 (text, image_url, video_url 등)
- **통계**: 상태별 개수, 가장 오래된 포스트, 큐 건강 상태

## 출력 형식

### 목록 조회 (PENDING 예시)

```markdown
## PENDING 포스트 목록 (3건)

| ID | 상태 | 미디어 타입 | 생성 시각 | 예약 시각 |
|----|------|-----------|----------|----------|
| 123 | PENDING | TEXT | 2025-01-14 15:30 | NULL (due 즉시) |
| 124 | PENDING | IMAGE | 2025-01-14 16:00 | 2025-01-15 09:00 |
| 125 | PENDING | TEXT | 2025-01-14 16:30 | 2025-01-20 10:00 |

**다음 단계**: `threads-schedule` 스킬로 승인 및 예약 설정
```

### 단일 포스트 상세

```markdown
## 포스트 상세 (ID: 123)

**상태**: PENDING
**미디어 타입**: TEXT
**생성 시각**: 2025-01-14T15:30:00+09:00
**예약 시각**: NULL (due 즉시)

**초안 내용**:
```
<text 내용>
```

**승인**: `threads_queue_approve(post_id=123)` 로 승인 가능
```

### 통계 요약

```markdown
## 큐 상태 요약

| 상태 | 개수 |
|------|------|
| PENDING | 3 |
| APPROVED | 5 |
| PUBLISHED | 142 |
| FAILED | 1 |

**건강 상태**:
- 최근 발행 성공률: 99.3% (142/143)
- 실패 1건: post_id=98, HTTP 613 rate limit (24시간 후 재시도 권장)
- 가장 오래된 PENDING: post_id=123 (2시간 경과, 승인 대기)

**권장 작업**:
- PENDING 3건: `threads-schedule` 스킬로 승인
- FAILED 1건: 24시간 후 재시도 또는 포기
```

## 주의사항

| 상황 | 대응 |
|------|------|
| post_id 없음 에러 | `threads_queue_list()`로 ID 재확인 |
| 빈 목록 | 해당 상태의 포스트 없음 안내 |
| limit 초과 요청 | limit 100 이내로 조정 권장 |
| 쓰기/승인/발행 시도 | 금지 — 읽기 전용 스킬 (`threads-schedule`, `threads-post-draft` 사용) |

## References

| 파일 | 로드 조건 |
|------|-----------|
| references/queue-states.md | 상태별 의미·전이·에러 케이스 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `threads-post-draft` | PENDING 포스트 생성 |
| `threads-schedule` | APPROVED로 승인·예약 |

## 이 스킬을 사용하지 말아야 할 때

- 초안 작성: `threads-post-draft` 스킬 사용
- 승인/예약: `threads-schedule` 스킬 사용
- 발행: 세션 안에서 `threads_queue_publish_due` 도구 사용

---

## 읽기 전용 보장

이 스킬은 **절대 쓰기/승인/발행을 하지 않습니다**:

- ✅ 조회만: `threads_queue_list`, `threads_queue_get`
- ❌ 하지 않음: `threads_queue_add`, `threads_queue_approve`, `threads_queue_publish_due`

큐 상태 확인에만 사용하세요. 수정은 형제 스킬에 위임하세요.
