# moai-threads-poster 스킬 (M3 + 문체 학습 + 멀티 채널)

이 플러그인은 Threads(Meta) 발행 큐를 구동하는 5개의 스킬을 제공합니다. 문체 학습 → 초안 작성(문체 적용) → 멀티 채널 포맷 → 승인 → 발행/복붙 의 파이프라인으로 Threads에 포스팅하고 Facebook·X 용 텍스트를 준비합니다.

## 스킬 목록

### 0. threads-style-learn (문체 학습)
과거 Facebook/Threads 포스팅 3-10개를 분석해 **문체 프로필** 을 저장합니다. 저장된 프로필은 `threads-post-draft` 가 초안 작성 시 자동으로 적용합니다.

**책임**: 문체 분석 + 프로필 *저장* 만 담당합니다. 초안 작성·발행은 하지 않습니다.
**MCP 도구**: `threads_style_save(profile_markdown, path=<optional>)` (자격증명 불필요 — 로컬 파일 I/O)
**관련 스킬**: 저장된 프로필 적용은 `threads-post-draft`

### 1. threads-post-draft (초안 작성)
주제를 받아 Threads 최적화 초안을 작성하고 발행 큐에 **PENDING** 상태로 등록합니다. 저장된 문체 프로필이 있으면 자동으로 적용합니다.

**책임**: 초안 작성(프로필 적용) + PENDING 등록만 담당합니다. 승인·발행은 하지 않습니다.
**MCP 도구**: `threads_style_load(path=<optional>)` (0단계) → `threads_queue_add(media_type="TEXT", text=<draft>, scheduled_at=<optional>)`
**관련 스킬**: 문체 분석은 `threads-style-learn`, 초안 승인은 `threads-schedule`, 멀티 채널은 `threads-multichannel`, 상태 조회는 `threads-status`

### 2. threads-multichannel (멀티 채널 포맷)
하나의 텍스트를 Threads(직접 발행) / Facebook(복붙) / X(free=280자 분할·premium=단일) 용으로 각각 포맷합니다. **발행은 하지 않습니다** — Facebook·X 출력은 사용자가 직접 복붙합니다.

**책임**: *포맷만* 담당합니다. Threads 발행·승인, Facebook/X 발행은 하지 않습니다.
**MCP 도구**: `threads_format_multi_channel(text, x_tier="free"|"premium", channels=<optional>)`
**관련 스킬**: 초안 작성은 `threads-post-draft`, Threads 승인은 `threads-schedule`

### 3. threads-schedule (승인·예약)
PENDING 상태의 포스트를 검토하고 사용자 승인을 받은 뒤 **APPROVED** 상태로 변경하며 발행 예약 시간을 설정합니다.

**책임**: 승인·예약만 담당합니다. 초안 작성·발행은 하지 않습니다.
**MCP 도구**: `threads_queue_approve(post_id, scheduled_at=<ISO-8601 or omit>)`, `threads_queue_get`, `threads_queue_list(status="PENDING")`
**HARD 규칙**: 사용자 승인 없이 자동 승인 금지 ("자동 아닌 자율")
**관련 스킬**: 초안 작성은 `threads-post-draft`, 상태 조회는 `threads-status`, 발행은 `threads_queue_publish_due` 도구

### 4. threads-status (조회)
Threads 발행 큐의 상태를 **읽기 전용**으로 조회합니다. PENDING/APPROVED/PUBLISHED/FAILED 포스트 목록과 단일 포스트 상세를 제공합니다.

**책임**: 읽기 전용 조회만 담당합니다. 쓰기/승인/발행은 하지 않습니다.
**MCP 도구**: `threads_queue_list(status=..., limit=...)`, `threads_queue_get(post_id)`
**관련 스킬**: 초안 작성은 `threads-post-draft`, 승인·예약은 `threads-schedule`

## 승인 기반 플로우 + 문체 학습 + 멀티 채널 (Approval Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│          moai-threads-poster — 문체 학습 → 작성 → 멀티 채널 → 승인 → 발행    │
└─────────────────────────────────────────────────────────────────────────────┘

  [과거 포스팅 3-10개]
         │  threads_style_save  (threads-style-learn · 자격증명 불필요)
         ▼
  ┌──────────────────┐
  │ style-profile.md │  (.data/ 에 영구 저장 — gitignored)
  │  (문체 프로필)   │
  └────────┬─────────┘
           │ threads_style_load  (threads-post-draft 의 0단계가 자동 호출)
           ▼
  ┌─────────────────┐  threads_queue_add / add_batch  ┌──────────────┐
  │  사용자 주제    │ ────────────────────────────────> │   PENDING     │
  │  + 문체 적용    │  (threads-post-draft)             │   (초안)     │
  └─────────────────┘                                   └──────┬───────┘
                                                                │
                              ┌─────────────────────────────────┘
                              │  (선택) 멀티 채널 포맷
                              ▼
                    threads_format_multi_channel  (threads-multichannel)
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
         ┌──────────┐  ┌──────────┐  ┌──────────────┐
         │ Threads  │  │ Facebook │  │ X (free/prem)│
         │ ≤500B    │  │ 복붙용    │  │  분할/단일    │
         └────┬─────┘  └────┬─────┘  └──────┬───────┘
              │             │               │
   queue 도구 │      사용자 복붙      사용자 복붙
   (직접발행) │      (API 발행 불가)   (트윗 체인)
              ▼
                                                  ┌──────────────────┐
                                                  │  사용자 검토     │
                                                  │  (자동 아님!)    │
                                                  └────────┬─────────┘
                                                  승인?  │  거부?
                                             ┌─────────────┴─────────────┐
                                             ▼                           ▼
                              threads_queue_approve                   수정/삭제
                              또는 add_batch(approve=True)
                              (threads-schedule)
                                             │
                                             ▼
                                     ┌──────────────┐
                                     │   APPROVED   │
                                     │ + 예약 시각  │  (분산: 화/수/목 12:00)
                                     └──────┬───────┘
                                            │  (세션 안에서 scheduled_at 도달)
                                            ▼
                               threads_queue_publish_due
                               (세션 안 수동 flush — 자동 백그라운드 발행 없음)
                                            │
                                   ┌────────┴─────────┐
                                   ▼                  ▼
                             ┌──────────┐        ┌──────────┐
                             │ PUBLISHED│        │  FAILED  │
                             └──────────┘        └──────────┘
```

> **핵심 분기**: Threads 는 *직접 발행* (queue 도구 → 승인 → publish_due). Facebook·X 는 *복붙용 텍스트만* (본 플러그인이 발행하지 않음 — `threads_format_multi_channel` 이 포맷만 제공).

## 각 단계별 MCP 도구

| 단계 | 상태 전이 | MCP 도구 | 스킬 |
|------|----------|----------|------|
| 문체 학습 (최초 1회/갱신) | (파일 I/O) | `threads_style_save` / `threads_style_load` | `threads-style-learn` |
| 초안 작성 (1건) | 없음 → PENDING | `threads_style_load` → `threads_queue_add` | `threads-post-draft` |
| 초안 작성 (여러건/분산) | 없음 → PENDING/APPROVED | `threads_style_load` → `threads_queue_add_batch` | `threads-post-draft` |
| 멀티 채널 포맷 | (변화 없음) | `threads_format_multi_channel` | `threads-multichannel` |
| 승인 | PENDING → APPROVED | `threads_queue_approve` | `threads-schedule` |
| 조회 | (변화 없음) | `threads_queue_list`, `threads_queue_get` | `threads-status` |
| 발행 | APPROVED → PUBLISHED/FAILED | `threads_queue_publish_due` | (세션 안 수동 flush) |

## 사용 예시

### 예시 1: 단일 포스트 작성·승인·발행

```markdown
사용자: "최신 AI 뉴스로 Threads 포스트 작성해줘"

→ threads-post-draft: 초안 작성 + PENDING 등록 (post_id: 123)

사용자: "승인할게"

→ threads-schedule: post_id 123 승인 + 예약 설정 (APPROVED)

→ (세션 안에서) threads_queue_publish_due: scheduled_at 도달 시 발행

사용자: "발행 결과는?"

→ threads-status: PUBLISHED 상태로 확인 (media_id, permalink)
```

### 예시 2: 일일 큐 건강 확인

```markdown
사용자: "뭐가 대기중이야?"

→ threads-status: PENDING 포스트 3건 목록 출력

사용자: "전부 승인할게"

→ threads-schedule: 3건 연속 승인 (각각 APPROVED)

사용자: "지금 발행해줘"

→ threads_queue_publish_due: 3건 즉시 발행

사용자: "실패한 거 있어?"

→ threads-status: FAILED 상태 0건 확인
```

## 발행 전 설정 (최초 1회)

이 스킬들을 사용하려면 Threads OAuth 자격증명이 필요합니다. 최초 1회 설정:

```bash
# 환경변수 설정
export THREADS_ACCESS_TOKEN="<장기 토큰(60일)>"
export THREADS_USER_ID="<Threads 사용자 ID>"

# 선택: 발행 전 대기 시간(초), 기본 30초
export THREADS_PUBLISH_DELAY="30"
```

발급 절차: `mcp-servers/threads-poster/CONNECTORS.md` 참조 (브라우저 인가 → 단기 토큰 → 장기 토큰 교환)

**동작 확인**: `threads_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.

## 관련 MCP 도구 (전체 14종)

### 즉시 발행 도구 (M1)
- `threads_publish_text`: 텍스트 게시
- `threads_publish_image`: 이미지 게시
- `threads_publish_video`: 비디오 게시
- `threads_get_profile`: 프로필 조회 (health check)
- `threads_refresh_token`: 장기 토큰 수동 갱신

### 큐 관리 도구 (M2 + 분산 등록)
- `threads_queue_add`: 큐에 PENDING 포스트 추가 (단건)
- `threads_queue_add_batch`: 초안 여러 개를 베스트 슬롯에 분산 등록 (batch)
- `threads_queue_approve`: PENDING → APPROVED 승인
- `threads_queue_list`: 큐 목록 조회
- `threads_queue_get`: 단일 포스트 상세
- `threads_queue_publish_due`: due 큐 수동 처리 (세션 안 발행)

### 문체 프로필 도구 (자격증명 불필요 — 로컬 파일 I/O)
- `threads_style_save`: 문체 프로필 마크다운 저장
- `threads_style_load`: 저장된 문체 프로필 조회 (없으면 exists=False)

### 멀티 채널 포맷 도구 (발행 안 함 — 포맷만)
- `threads_format_multi_channel`: Threads/Facebook/X 용 텍스트 포맷 (X free=280자 분할·premium=단일)

## 주의사항

| 항목 | 내용 |
|------|------|
| **자동 승인 금지** | `threads-schedule` 스킬은 반드시 사용자 승인을 받아야 합니다 ("자동 아닌 자율") |
| **읽기 전용 준수** | `threads-status` 스킬은 조회만 하며, 절대 쓰기/승인/발행을 하지 않습니다 |
| **바이트 제한** | Threads 텍스트는 500 UTF-8 바이트 제한 (ASCII 1B, 한글 3B, 이모지 4B) |
| **레이트 리밋** | 24시간 250 포스트 제한 (초과 시 HTTP 613) |
| **토큰 만료** | 장기 토큰(60일) 만료 시 `threads_refresh_token`으로 갱신 |

## Cross-References

- **M1 (MCP 서버)**: `mcp-servers/threads-poster/src/threads_poster/server.py` — 도구 정의
- **M2 (큐/러너)**: `mcp-servers/threads-poster/src/threads_poster/queue.py`, `runner.py` — SQLite 발행 큐
- **M3 (스킬)**: `skills/threads-post-draft/`, `skills/threads-schedule/`, `skills/threads-status/` — 현재 위치
- **M4 (스케줄러)**: 제거됨 — 수동 승인 모델로 전환 (launchd 자동 발행 폐기). 발행은 세션 안 `threads_queue_publish_due` 로.
- **분산 등록**: `threads_queue_add_batch` (server.py) · 케이던스 기준값 `config/threads.yaml`
- **M5 (마켓플레이스)**: `.claude-plugin/marketplace.json` entry 등록

## 버전

- moai-threads-poster: 1.0.0 (수동 승인 + 분산 등록 모델)
- 스킬 버전: 각 `SKILL.md` frontmatter `version: "1.0.0"`

---

**문의**: 모두의 AI · MoAI 프로젝트
