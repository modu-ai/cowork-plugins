# 큐 상태 상세 (Queue States)

## 상태 전이 그래프

```
       threads_queue_add
              ↓
           PENDING ←→ threads_queue_get
              ↓
       threads_queue_approve
              ↓
          APPROVED ←→ threads_queue_get
              ↓
    threads_queue_publish_due
              ↓
      ┌─────┴─────┐
      ↓           ↓
  PUBLISHED   FAILED
      ↓           ↓
   완료      에러 확인
```

## 상태별 상세

| 상태 | 의미 | 지속 기간 | 다음 상태 | 조회 도구 |
|------|------|----------|----------|----------|
| PENDING | 초안 작성 완료, 승인 대기 | 사용자 승인까지 | APPROVED (승인) | `threads_queue_list(status="PENDING")` |
| APPROVED | 사용자 승인 완료, 예약 시각 대기 | 예약 시각까지 | PUBLISHED (성공), FAILED (실패) | `threads_queue_list(status="APPROVED")` |
| PUBLISHED | 발행 성공 | 영구 | 없음 (완료) | `threads_queue_list(status="PUBLISHED")` |
| FAILED | 발행 실패 (에러) | 영구 | 없음 (수동 재시도) | `threads_queue_list(status="FAILED")` |

## 에러 상태(FAILED) 원인별 분류

| 에러 타입 | HTTP 코드 | 원인 | 해결 |
|----------|----------|------|------|
| `text exceeds 500-byte` | 400 | 텍스트 500바이트 초과 | 초안 줄이기 |
| `OAuthException` | 190 | 토큰 만료 | `threads_refresh_token`로 갱신 |
| `rate limit` | 613 | 24시간 250 포스트 초과 | 24시간 후 재시도 |
| `permission` | 4/10 | 스코프 부족/테스터 미등록 | `threads_basic`, `threads_content_publish` 스코프 확인 |
| `setup_required` | - | 자격증명 미설정 | `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID` 환경변수 설정 |

## 조회 패턴

### 1. 일일 큐 건강 확인

```python
# 전체 상태 개수
threads_queue_list(status=None, limit=1000)

# 출력 예시
# PENDING: 3, APPROVED: 5, PUBLISHED: 142, FAILED: 1
```

### 2. 승인 대기 목록

```python
# PENDING 전체 (가장 오래된 것부터)
threads_queue_list(status="PENDING", limit=50)
```

### 3. 발행 완료 내역 (최근 7일)

```python
# PUBLISHED 최근 50개
threads_queue_list(status="PUBLISHED", limit=50)
```

### 4. 실패 내역 분석

```python
# FAILED 전체
threads_queue_list(status="FAILED", limit=100)

# 단일 실패 포스트 상세
threads_queue_get(post_id=98)
```

## 읽기 전용 보장

이 스킬(`threads-status`)은 조회만 수행합니다:

| 도구 | 용도 | threads-status |
|------|------|-----------------|
| `threads_queue_list` | 목록 조회 | ✅ 사용 |
| `threads_queue_get` | 단일 조회 | ✅ 사용 |
| `threads_queue_add` | PENDING 등록 | ❌ 형제 스킬(`threads-post-draft`) |
| `threads_queue_approve` | APPROVED 승인 | ❌ 형제 스킬(`threads-schedule`) |
| `threads_queue_publish_due` | 발행 실행 | ❌ 스케줄러 또는 수동 |
| `threads_publish_*` | 즉시 발행 | ❌ MCP 도구 (직접 호출) |
