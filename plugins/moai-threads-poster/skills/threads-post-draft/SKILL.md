---
name: threads-post-draft
description: |
  주제를 Threads 게시글 초안으로 작성하고 발행 큐에 PENDING 상태로 등록합니다. 저장된 문체 프로필이 있으면 자동으로 적용합니다. 승인과 발행은 threads-schedule 스킬이 담당합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 주제로 Threads 포스트 작성해줘"
  - "Threads에 올릴 글 초안 만들어줘"
  - "이 뉴스를 Threads용으로 요약해줘"
  - "블로그 글을 Threads 포스트로 변환해줘"
  - "이번 주 Threads 포스트 3개 만들어줘" (분산 등록 — 여러 주제 한 번에)
  - "여러 주제 한 번에 초안 작성해줘" (분산 등록)
  - "내 문체로 초안 작성해줘" (저장된 프로필 자동 적용)
  [책임 경계] vs 형제 스킬: 초안 작성과 PENDING 등록(저장된 문체 프로필 적용 포함) 만 담당합니다. 문체 *분석·저장* 은 threads-style-learn, 멀티 채널(Facebook/X) 포맷은 threads-multichannel, 승인·예약·발행은 threads-schedule, 상태 조회는 threads-status, 이미지/비디오 발행은 MCP 도구(threads_publish_image, threads_publish_video)를 직접 사용하세요.
version: "1.0.0"
---

# Threads 초안 작성 (threads-post-draft)

## 개요

주제를 받아 Threads 최적화 초안을 작성하고 발행 큐에 **PENDING** 상태로 등록합니다. 이 스킬은 작성과 등록만 담당하며, 승인과 발행은 `threads-schedule` 스킬이 담당합니다.

## 트리거 키워드

Threads, 스레드, 초안, 작성, 등록, PENDING, 포스트, 게시글, 주제, 변환

## 워크플로우

### 0단계: 문체 적용 (있으면)

초안 작성 *전* 에 저장된 문체 프로필이 있는지 확인합니다:

```python
threads_style_load(path=None)
# → {path, exists: bool, profile: <markdown or None>}
```

- **프로필이 있으면** (`exists: True`): 반환된 마크다운의 차원(말투·문장 길이·오프닝·클로징·이모지·시그니처 구절 등) 을 아래 1단계 초안 작성에 반영합니다. 프로필은 `threads-style-learn` 스킬이 만들어 저장한 것입니다.
- **프로필이 없으면** (`exists: False`): 브랜드 톤이 지정됐으면 그것을, 아니면 합리적 기본 톤(캐주얼 대화체) 으로 작성합니다. 프로필 없어도 초안 작성은 정상 동작합니다.

> 프로필을 새로 만들거나 갱신하려면 `threads-style-learn` 스킬을 먼저 호출하세요.

### 1단계: 주제 분석 및 초안 작성

사용자의 주제/블로그 글/뉴스를 분석하여 Threads 최적화 초안을 작성합니다:

- **길이 제한**: 최대 500 UTF-8 바이트 (아래 바이트 계산 규칙 참조)
- **구조**: 짧은 문장, 대화 유도, 핵심 메시지 1-2개
- **톤**: 브랜드 톤 일치 (지정 시), 기본값은 캐주얼한 대화체
- **토픽 태그**: 선택사항, 최대 1개 (Threads 알고리즘 — 토픽 태그는 노출에 도움)
- **링크**: 선택사항, 최대 5개 (프리뷰 자동 생성)

### 2단계: MCP 도구 호출 — 큐 등록

작성한 초안을 `threads_queue_add` 도구로 큐에 등록합니다:

```python
threads_queue_add(
    media_type="TEXT",
    text="<작성한 초안>",
    scheduled_at=None  # 즉시 due, 또는 ISO-8601 시각 (선택)
)
```

- `media_type`: 이 스킬은 `"TEXT"` 전용 (이미지/비디오는 `threads_publish_image`, `threads_publish_video` 직접 호출)
- `text`: 500 UTF-8 바이트 이하 초안
- `scheduled_at`: 미지정 시 NULL = due 즉시 (승인 후 즉시 발행 가능 상태)

### 3단계: post_id 반환

도구 응답의 `post_id`를 사용자에게 알려줍니다. 이 ID는 `threads-schedule` 스킬에서 승인 시 사용합니다.

## 여러 주제를 한 번에 (분산 등록 / batch)

사용자가 **여러 주제**를 주거나 **"이번 주 분량"**을 요청하면, 초안을 하나씩 만든 뒤 `threads_queue_add_batch` 로 한 번에 등록합니다. 이 도구는 N 개의 초안을 베스트 슬롯(Asia/Seoul 12:00)에 자동 분산 예약합니다.

### 언제 단건 `threads_queue_add` vs batch `threads_queue_add_batch`?

| 상황 | 도구 |
|------|------|
| 주제 1개, 즉시/특정 시각 1건 | `threads_queue_add` (위 2단계) |
| 주제 2개 이상 · "이번 주 N개" · 한 주 분량 | `threads_queue_add_batch` (아래) |

### batch 호출

초안을 각각 작성한 뒤 한 리스트로 넘깁니다:

```python
threads_queue_add_batch(
    posts=[
        {"media_type": "TEXT", "text": "<첫째 초안>"},
        {"media_type": "TEXT", "text": "<둘째 초안>"},
        {"media_type": "TEXT", "text": "<셋째 초안>"},
    ],
    cadence="weekly_3",   # 화/수/목 12:00 분산 (기본). weekly_5(월-금) · manual 도 가능
    approve=False,        # 기본 PENDING. 이 호출 안에서 이미 검토했다면 True → APPROVED
)
```

- `posts`: 초안 dict 리스트 (≥1). `media_type` 생략 시 `TEXT`.
- `cadence`:
  - `weekly_3` (기본) — 화·수·목 12:00 (Asia/Seoul) 피크 슬롯에 하루 1건씩 분산
  - `weekly_5` — 월-금 12:00 에 하루 1건씩
  - `manual` — 예약 시각 없이(NULL) 등록, 호출자/승인자가 나중에 `threads_queue_approve(scheduled_at=...)` 로 지정
- `approve=True` 면 PENDING 게이트를 건너뛰고 바로 `APPROVED` 로 예약(같은 호출에서 이미 초안을 검토했을 때만).

### batch 결과 해석

```python
{
  "count": 3,
  "post_ids": [11, 12, 13],
  "schedules": [
    {"post_id": 11, "scheduled_at": "2026-08-11T12:00:00+09:00"},  # 화
    {"post_id": 12, "scheduled_at": "2026-08-12T12:00:00+09:00"},  # 수
    {"post_id": 13, "scheduled_at": "2026-08-13T12:00:00+09:00"},  # 목
  ],
  "cadence": "weekly_3"
}
```

**주의**: 승인과 실제 발행은 여전히 분리돼 있습니다. `approve=False` 로 등록했으면 `threads-schedule` 스킬로 승인해야 하고, 발행은 세션 안에서 `threads_queue_publish_due` 로 해야 합니다 (자동 백그라운드 발행은 없습니다).

## 바이트 계산 규칙 (500 UTF-8 바이트 제한)

Threads 텍스트 제한은 **문자 수가 아니라 UTF-8 바이트 수**입니다:

| 문자 타입 | 바이트 수 | 예시 |
|----------|----------|------|
| ASCII (영문, 숫자, 공백, 일반 기호) | 1바이트 | `A`, `1`, ` `, `?` |
| 한글 (가-힣) | 3바이트 | `한`, `글`, `🇰🇷` (국기 깃발 이모지 제외) |
| 이모지 (대부분) | 4바이트 | `😀`, `🎉`, `🔥` |
| 국기 깃발 이모지 (🇰🇷, 🇺🇸) | 8바이트 | 두 개의 regional indicator로 구성 |

**계산 예시**:
- `"안녕하세요!"` = 한글 5글자 × 3바이트 + `!` 1바이트 = **16바이트**
- `"Hello! 😀"` = ASCII 7글자 × 1바이트 + 이모지 4바이트 = **11바이트**
- `"🇰🇷 Korea"` = 국기 8바이트 + 공백 1바이트 + ASCII 5바이트 = **14바이트**

**초안 작성 시 바이트 계산**:
초안을 작성한 후, 클로드에게 "이 초안 몇 바이트야?"라고 물어보면 UTF-8 바이트 수를 계산해 드립니다.

## 출력 형식

```markdown
## 초안 (PENDING 등록 완료)

<작성한 초안>

**바이트 수**: N / 500
**토픽 태그**: (선택사항) #태그이름
**링크**: (선택사항) URL

**큐 등록 정보**:
- post_id: N
- status: PENDING
- scheduled_at: NULL (due 즉시)

**다음 단계**: `threads-schedule` 스킬로 승인 후 발행 예약을 설정하세요.
```

## 주의사항

| 상황 | 대응 |
|------|------|
| 500바이트 초과 시 | 초안을 줄이거나 두 개의 포스트로 분할 제안 |
| 토픽 태그 2개 이상 요청 시 | 1개만 권장 (Threads 알고리즘) |
| 링크 6개 이상 요청 시 | 5개로 제한 (Threads 규격) |
| 이미지/비디오 포함 요청 시 | `threads_publish_image`, `threads_publish_video` 도구 직접 호출 제안 |
| 브랜드 톤 미지정 시 | 업종·타겟 기반 캐주얼 톤 초안 제안 후 확인 |

## References

| 파일 | 로드 조건 |
|------|-----------|
| references/threads-spec.md | Threads 규격·바이트 계산·토픽 태그·링크 제한 확인 시 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `threads-style-learn` | 문체 분석·저장 (이 스킨이 초안 작성 시 자동 적용) |
| `threads-multichannel` | 초안을 Threads/Facebook/X 용으로 멀티 채널 포맷 |
| `threads-schedule` | PENDING 포스트 승인·예약 설정 |
| `threads-status` | 큐 상태 조회 (PENDING/APPROVED/PUBLISHED/FAILED) |
| `moai-marketer:content-sns-content` | 브랜드 톤 가이드·채널별 최적화 패턴 |

## 이 스킬을 사용하지 말아야 할 때

- 이미지/비디오 포스트 발행: MCP 도구 `threads_publish_image`, `threads_publish_video` 직접 호출
- PENDING 포스트 승인: `threads-schedule` 스킬 사용
- 큐 상태 조회: `threads-status` 스킬 사용
- 즉시 발행(승인 없이): MCP 도구 `threads_publish_text` 직접 호출

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
