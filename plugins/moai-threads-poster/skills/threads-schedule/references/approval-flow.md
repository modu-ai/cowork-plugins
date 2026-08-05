# 승인 플로우 상세 (Approval Flow)

## 상태 전이 다이어그램

```
PENDING → APPROVED → PUBLISHED
             ↓
           FAILED (발행 실패)
```

## 상태별 의미

| 상태 | 의미 | 다음 단계 |
|------|------|-----------|
| PENDING | 초안 작성 완료, 승인 대기 | `threads_queue_approve`로 APPROVED로 전이 |
| APPROVED | 사용자 승인 완료, 예약 시각 대기 | 스케줄러 또는 `threads_queue_publish_due`로 PUBLISHED/FAILED로 전이 |
| PUBLISHED | 발행 성공 | 완료 |
| FAILED | 발행 실패 (에러) | 에러 확인 후 재시도 또는 포기 |

## 에러 케이스

| 에러 | 원인 | 해결 |
|------|------|------|
| `not_found` | post_id가 존재하지 않음 | `threads_queue_list(status="PENDING")`로 ID 재확인 |
| `setup_required` | 자격증명 미설정 | `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID` 환경변수 설정 |
| HTTP 400 `text exceeds 500-byte` | 텍스트 500바이트 초과 | 초안 줄이기 |
| HTTP 190 `OAuthException` | 토큰 만료 | `threads_refresh_token` 도구로 갱신 |
| HTTP 613 `rate limit` | 24시간 250 포스트 초과 | 24시간 후 재시도 |

## 승인 전용 체크리스트

- [ ] PENDING 포스트 내용 확인
- [ ] 사용자 승인 획득 (자동 아닌 자율)
- [ ] 예약 시각 설정 (즉시 due 또는 ISO-8601)
- [ ] `threads_queue_approve` 호출
- [ ] 발행 경로 안내 (자동/수동)
