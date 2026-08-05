---
name: threads-multichannel
description: |
  하나의 텍스트를 Threads(직접 발행) / Facebook(복붙) / X(복붙, free=스레드 분할·premium=단일) 용으로 각각 포맷합니다. 발행은 하지 않고 포맷만 — Facebook·X 출력은 사용자가 직접 복붙합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 글 페이스북/엑스에도 올릴 수 있게 해줘"
  - "X 스레드로 쪼개줘" (무료 tier 280자 분할)
  - "트위터용 스레드 만들어줘"
  - "Facebook 이랑 X 용으로도 포맷해줘"
  - "이 초안 멀티 채널로 변환해줘"
  - "X premium 으로 한 번에 올릴 수 있게 해줘"
  [책임 경계] vs 형제 스킬: *포맷만* 담당합니다 — Facebook/X 로 발행하지 않습니다 (사용자가 복붙). Threads 큐 등록은 threads-post-draft, 승인·예약은 threads-schedule, 상태 조회는 threads-status 가 담당합니다.
version: "1.0.0"
---

# 멀티 채널 포맷 (threads-multichannel)

## 개요

하나의 원본 텍스트를 세 채널의 제약에 맞춰 각각 포맷합니다. **발행은 하지 않습니다** — 채널별로 출력을 만들어 사용자에게 전달합니다.

| 채널 | 제약 | 출력 | 발행 경로 |
|------|------|------|----------|
| **Threads** | 500 UTF-8 바이트 | 다듬은 텍스트 + 바이트 수 | 직접 발행 (queue 도구로 넘김) |
| **Facebook** | 글자 수 제한 없음 (개인 계정) | 대화체 텍스트 | **복붙 only** (API 발행 불가) |
| **X (free)** | 트윗당 280자 | `1/ `·`2/ ` 번호 트윗 리스트 | **복붙 only** |
| **X (premium)** | 25,000자 | 단일 문자열 | **복붙 only** |

> **왜 Facebook·X 는 복붙인가**: Facebook 개인 계정은 API 발행이 정책상 불가합니다. X 도 무료 tier 에선 트윗 체인을 직접 올리는 게 보통이고, 이 플러그인은 Threads API 만 직접 다룹니다. 그래서 Facebook·X 출력은 *사용자가 직접 복붙* 합니다 — 본 스킬은 텍스트를 준비만 해 드립니다.

## 트리거 키워드

멀티 채널, 페이스북, 엑스, 트위터, X, Facebook, 복붙, 스레드 분할, 280자, premium, 프리미엄, 무료, 채널별, 포맷

## 워크플로우

### 1단계: 원본 텍스트 + X tier 확인

원본 텍스트(초안) 와 사용자의 X tier 를 확인합니다:

- **원본**: `threads-post-draft` 로 작성한 초안, 또는 사용자가 직접 준 텍스트.
- **X tier**: 무료면 `"free"` (기본), 유료(X Premium) 면 `"premium"`. 모르면 기본 `"free"` 로.

> tier 확인이 애매하면 사용자에게 "X 가 무료입니까, 프리미엄입니까?" 만 물어봅니다. 무료=280자 분할, 프리미엄=25,000자 단일.

### 2단계: MCP 도구 호출 — 멀티 채널 포맷

```python
threads_format_multi_channel(
    text="<원본 텍스트>",
    x_tier="free",            # "free" (기본) 또는 "premium"
    channels=None,            # 기본 ["threads","facebook","x"]. 특정 채널만 원하면 리스트로.
)
```

반환 구조:
```python
{
  "channels": ["threads", "facebook", "x"],
  "x_tier": "free",
  "note": "Threads 출력은 queue 도구로... Facebook·X 출력은 *복붙용*...",
  "threads": {"text": "<≤500바이트 텍스트>", "bytes": 412, "max_bytes": 500},
  "facebook": "<복붙용 텍스트 문자열>",
  "x": ["1/ ...", "2/ ...", "3/ ..."],   # free → 리스트 / premium → 문자열
}
```

- `threads` 출력은 `threads_queue_add` / `threads_queue_add_batch` 에 바로 넘길 수 있는 형태다.
- `facebook` / `x` 출력은 *사용자에게 보여줄 복붙용* 이다 — 본 도구는 발행하지 않는다.
- X 가 `free` 면 `out["x"]` 가 리스트(각 트윗 ≤280자, 번호 붙음). `premium` 이면 문자열(≤25,000자).

### 3단계: 채널별 출력을 사용자에게 표시 (복붙 블록)

결과를 채널별로 **펜스드 코드 블록** 으로 나눠 보여줍니다. 각 블록 위에 한 줄 안내를 붙입니다:

```markdown
## Threads (직접 발행 — queue 도구로 넘기기)
<412 / 500 바이트>

\```
<threads.text>
\```

→ `threads_queue_add(media_type="TEXT", text="<위 텍스트>")` 로 큐에 등록 가능.

## Facebook (복붙해서 올리세요)

\```
<facebook 문자열>
\```

→ Facebook 개인 계정은 API 발행이 안 됩니다 — 위 텍스트를 복사해 직접 올려주세요.

## X (무료 tier — 트윗 체인, 복붙해서 올리세요)
3개 트윗:

\```
1/ <첫 트윗>
2/ <둘째 트윗>
3/ <셋째 트윗>
\```

→ 각 트윗을 순서대로 복붙해 스레드로 올려주세요 (280자 제한 자동 분할됨).
```

- Threads 만 따로 빼서 "이건 제가 발행해 드릴 수 있습니다" 라고 안내 (승인 절차: `threads-schedule`).
- Facebook·X 는 명시적으로 "복붙해서 올리세요" 라고 안내 — 본 스킬이 발행하지 않음을 분명히.

### 4단계 (선택): Threads 큐 등록

사용자가 원하면 `threads` 출력 텍스트를 큐에 등록합니다 (이건 발행이 아니라 PENDING 등록):

```python
threads_queue_add(media_type="TEXT", text=out["threads"]["text"])
```

Facebook·X 까지 한 번에 "올려달라" 고 하면 **거절** 합니다 — 본 스킬은 Facebook/X 발행을 하지 않습니다. 복붙 블록을 드린 것으로 끝입니다.

## 출력 형식 예시

```markdown
## 멀티 채널 포맷 완료

**원본**: <첫 30자>...
**X tier**: free (280자 분할)

---

### Threads (직접 발행 가능)
412 / 500 바이트

\```
오늘 점심에 먹은 김치찌개가 진짜 맛있었습니다. ...
\```

→ `threads_queue_add(media_type="TEXT", text="...")` 로 등록 가능. 승인은 threads-schedule.

---

### Facebook — 복붙해서 올리세요

\```
오늘 점심에 먹은 김치찌개가 진짜 맛있었습니다. ...
\```

(Facebook 개인 계정은 API 발행 불가 — 직접 올려주세요.)

---

### X (free, 3 트윗) — 복붙해서 올리세요

\```
1/ 오늘 점심에 먹은 김치찌개가 진짜 맛있었습니다. ...
2/ ...
3/ ...
\```

(각 트윗을 순서대로 올려 스레드를 만드세요.)
```

## 주의사항

| 상황 | 대응 |
|------|------|
| 사용자가 "Facebook/X 에 올려줘" | **거절** — 본 스킬은 포맷만. 복붙 블록 제공으로 끝. |
| X tier 를 모를 때 | "무료입니까 프리미엄입니까?" 만 질문 (기본 free) |
| 잘못된 x_tier (`"bogus"`) | 도구가 `error` dict 반환 — `free`/`premium` 만 허용 안내 |
| Threads 500바이트 초과 | 도구가 자동으로 단어 경계+말줄표로 다듬음 — "의미 보존 요약이 필요하면 원본을 먼저 줄여주세요" 안내 |
| 특정 채널만 원할 때 | `channels=["x"]` 처럼 지정 (나머지는 생략) |
| 원본이 아주 짧을 때 | X free 도 1 트윗, Threads 도 그대로 — 정상 |

## References

이 스킬은 참조 파일 없이 본 문서만으로 자족합니다. 채널 제약값(500바이트/280자/25000자) 은 `threads_format_multi_channel` 도구(`mcp-servers/threads-poster/src/threads_poster/server.py`) 에 하드코딩된 baseline 이다.

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `threads-post-draft` | 원본 초안 작성 (저장된 문체 적용) |
| `threads-style-learn` | 문체 프로필 분석·저장 |
| `threads-schedule` | Threads PENDING 초안 승인·예약 |
| `threads-status` | 큐 상태 조회 |

## 이 스킬을 사용하지 말아야 할 때

- Threads 초안 작성만: `threads-post-draft` 스킬
- Facebook/X 에 *자동 발행* — **불가**. 이 스킬은 복붙용 텍스트만 만든다.
- Threads 승인/예약: `threads-schedule` 스킬
- 큐 상태 조회: `threads-status` 스킬

---

## 발행 경로 요약

- **Threads**: 본 스킨 포맷 → `threads_queue_add` 등록 → `threads-schedule` 승인 → (세션 안) `threads_queue_publish_due` 발행.
- **Facebook**: 본 스킨 포맷 → **사용자가 직접 복붙** (API 발행 불가).
- **X**: 본 스킨 포맷(free 분할/premium 단일) → **사용자가 직접 복붙**.
