# moai-threads-poster 스킬 (직접 발행 + 문체 학습 + 멀티 채널)

이 플러그인은 Threads(Meta) · Instagram 으로 직접 발행하는 5개의 스킬을 제공합니다. 문체 학습 → 초안 작성(문체 적용) → 승인 → 즉시 발행, 그리고 Facebook·X 용 텍스트 준비(복붙) 의 파이프라인으로 운영합니다.

> **직접 발행 모델.** 큐·예약·승인 상태머신은 없습니다. 세션 안에서 초안을 작성해 사용자에게 보여드리고, 승인하면 즉시 Graph API 로 발행합니다. 예약·정기 발행(예: 매주 수요일 12시)은 Claude Cowork 이 담당합니다.

## 스킬 목록

### 0. threads-style-learn (문체 학습)
과거 Facebook/Threads 포스팅 3-10개를 분석해 **문체 프로필** 을 저장합니다. 저장된 프로필은 `threads-post-draft` 가 초안 작성 시 자동으로 적용합니다.

**책임**: 문체 분석 + 프로필 *저장* 만 담당합니다. 초안 작성·발행은 하지 않습니다.
**MCP 도구**: `threads_style_save(profile_markdown, path=<optional>)` (자격증명 불필요 — 로컬 파일 I/O)
**관련 스킬**: 저장된 프로필 적용은 `threads-post-draft`

### 1. threads-post-draft (초안 작성·직접 발행)
주제를 받아 Threads 최적화 초안을 작성해 사용자에게 보여드리고, 승인하면 즉시 발행합니다. 저장된 문체 프로필이 있으면 자동으로 적용합니다.

**책임**: 초안 작성(프로필 적용) + 승인 시 즉시 발행을 담당합니다. 예약·정기 발행은 하지 않습니다.
**MCP 도구**: `threads_style_load(path=<optional>)` (0단계) → `threads_publish_text(text=<draft>)` (승인 시)
**관련 스킬**: 문체 분석은 `threads-style-learn`, 멀티 채널은 `threads-multichannel`

### 2. threads-multichannel (멀티 채널 포맷)
하나의 텍스트를 Threads(직접 발행) / Facebook(복붙) / X(free=280자 분할·premium=단일) 용으로 각각 포맷합니다. **발행은 하지 않습니다** — Facebook·X 출력은 사용자가 직접 복붙하고, Threads 출력은 승인 시 즉시 발행합니다.

**책임**: *포맷만* 담당합니다. Threads 발행·Facebook/X 발행은 하지 않습니다.
**MCP 도구**: `threads_format_multi_channel(text, x_tier="free"|"premium", channels=<optional>)`
**관련 스킬**: 초안 작성·발행은 `threads-post-draft`, 문체 분석은 `threads-style-learn`

### 3. instagram-post (Instagram 포스트 작성·직접 발행)
주제를 받아 Instagram 최적화 초안(이미지/비디오/릴) 을 작성해 사용자에게 보여드리고, 승인하면 즉시 발행합니다.

**책임**: Instagram 초안 작성 + 승인 시 즉시 발행을 담당합니다.
**MCP 도구**: `instagram_publish_image` / `instagram_publish_video` / `instagram_publish_reel` (승인 시)
**관련 스킬**: 댓글 관리는 `instagram-comments`, 문체 분석은 `threads-style-learn`

### 4. instagram-comments (Instagram 댓글 관리)
발행된 Instagram 미디어의 댓글을 조회·답글·숨김 처리합니다.

**책임**: 댓글 모더레이션만 담당합니다. 발행은 하지 않습니다.
**MCP 도구**: `instagram_comments_list` / `instagram_comments_reply` / `instagram_comments_hide`
**관련 스킬**: 포스트 발행은 `instagram-post`

## 직접 발행 플로우 (Direct-Publish Flow)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│      moai-threads-poster — 문체 학습 → 작성 → 승인 → 즉시 발행 / 복붙        │
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
  ┌─────────────────┐  threads_publish_text/image/video    ┌──────────────┐
  │  사용자 주제    │ ───────────────────────────────────> │  즉시 발행    │
  │  + 문체 적용    │  (threads-post-draft · 승인 후)       │ (Graph API)  │
  └─────────────────┘                                       └──────────────┘
           │
           │  (선택) 멀티 채널 포맷
           ▼
 threads_format_multi_channel  (threads-multichannel)
           │
   ┌───────┼───────┐
   ▼       ▼       ▼
 ┌──────┐ ┌──────┐ ┌────────────┐
 │Threads│ │Facebook│ │X(free/prem)│
 │≤500B │ │복붙용 │ │ 분할/단일  │
 └──┬───┘ └──┬───┘ └─────┬─────┘
    │        │           │
 즉시 발행  사용자 복붙  사용자 복붙
 (Graph API) (API 발행 불가) (트윗 체인)
```

> **핵심 분기**: Threads 는 *즉시 직접 발행* (승인 → publish). Facebook·X 는 *복붙용 텍스트만* (본 플러그인이 발행하지 않음 — `threads_format_multi_channel` 이 포맷만 제공). 예약·정기 발행은 Claude Cowork 이 담당합니다.

## 각 단계별 MCP 도구

| 단계 | MCP 도구 | 스킬 |
|------|----------|------|
| 문체 학습 (최초 1회/갱신) | `threads_style_save` / `threads_style_load` | `threads-style-learn` |
| Threads 초안 작성·발행 | `threads_style_load` → `threads_publish_text` | `threads-post-draft` |
| Instagram 초안 작성·발행 | `instagram_publish_image/video/reel` | `instagram-post` |
| 멀티 채널 포맷 | `threads_format_multi_channel` | `threads-multichannel` |
| Instagram 댓글 관리 | `instagram_comments_list/reply/hide` | `instagram-comments` |

## 사용 예시

### 예시 1: 단일 포스트 작성·발행

```markdown
사용자: "최신 AI 뉴스로 Threads 포스트 작성해줘"

→ threads-post-draft: 초안 작성 (저장된 문체 자동 적용) → 사용자에게 보여드림

사용자: "좋아, 올려줘"

→ threads_publish_text: 즉시 발행 → media_id, permalink 반환
```

### 예시 2: 멀티 채널 배포

```markdown
사용자: "이 초안 Threads, Facebook, X 용으로 포맷해줘"

→ threads-multichannel: 세 채널용 텍스트를 한 번에 포맷
   - Threads 용: 승인 시 threads_publish_text 로 즉시 발행 가능
   - Facebook/X 용: 복붙용 텍스트 블록 제공 (본 스킬은 발행 안 함)
```

### 예시 3: Instagram 릴 발행

```markdown
사용자: "이 영상 인스타 릴로 올려줘"

→ instagram-post: 캡션 작성 → 사용자에게 보여드림 → 승인 시 instagram_publish_reel 즉시 발행
```

## 발행 전 설정 (최초 1회)

이 스킬들을 사용하려면 Threads OAuth 자격증명이 필요합니다. 최초 1회 설정:

**macOS / Linux** (bash·zsh):

```bash
export THREADS_ACCESS_TOKEN="<장기 토큰(60일)>"
export THREADS_USER_ID="<Threads 사용자 ID>"
export THREADS_PUBLISH_DELAY="30"   # 선택: 발행 전 대기 시간(초), 기본 30초
```

**Windows** (PowerShell):

```powershell
$env:THREADS_ACCESS_TOKEN = "<장기 토큰(60일)>"
$env:THREADS_USER_ID = "<Threads 사용자 ID>"
$env:THREADS_PUBLISH_DELAY = "30"   # 선택: 발행 전 대기 시간(초), 기본 30초
```


발급 절차: `mcp-servers/moai-mcp-threads-poster/CONNECTORS.md` 참조 (브라우저 인가 → 단기 토큰 → 장기 토큰 교환)

Instagram 발행에는 추가로 `IG_ACCESS_TOKEN` / `IG_USER_ID` 가 필요합니다 (CONNECTORS.md 의 Instagram 섹션).

**동작 확인**: `threads_get_profile` / `instagram_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.

## 관련 MCP 도구 (전체 17종)

### Threads 직접 발행·조회 도구
- `threads_publish_text`: 텍스트 게시
- `threads_publish_image`: 이미지 게시
- `threads_publish_video`: 비디오 게시
- `threads_get_profile`: 프로필 조회 (health check)
- `threads_refresh_token`: 장기 토큰 수동 갱신

### Instagram 직접 발행·조회 도구
- `instagram_publish_image` / `instagram_publish_video` / `instagram_publish_reel`: 즉시 2단계 발행
- `instagram_get_profile` / `instagram_refresh_token`
- `instagram_comments_list` / `instagram_comments_reply` / `instagram_comments_hide`: 댓글 모더레이션
- `instagram_insights`: 인사이트 조회

### 문체 프로필 도구 (자격증명 불필요 — 로컬 파일 I/O)
- `threads_style_save`: 문체 프로필 마크다운 저장
- `threads_style_load`: 저장된 문체 프로필 조회 (없으면 exists=False)

### 멀티 채널 포맷 도구 (발행 안 함 — 포맷만)
- `threads_format_multi_channel`: Threads/Facebook/X 용 텍스트 포맷 (X free=280자 분할·premium=단일)

## 주의사항

| 항목 | 내용 |
|------|------|
| **승인 없이 발행 금지** | 초안을 사용자에게 보여드리고 승인한 뒤에 발행합니다 ("자동 아닌 자율") |
| **바이트 제한** | Threads 텍스트는 500 UTF-8 바이트 제한 (ASCII 1B, 한글 3B, 이모지 4B) |
| **레이트 리밋** | Threads 24시간 250 포스트 제한 (초과 시 HTTP 613) |
| **토큰 만료** | 장기 토큰(60일) 만료 시 `threads_refresh_token`으로 갱신 |
| **예약·정기 발행** | 본 플러그인 범위 밖 — Claude Cowork 이 담당 |

## Cross-References

- **MCP 서버**: `mcp-servers/moai-mcp-threads-poster/src/moai_mcp_threads_poster/server.py` — 도구 정의 (직접 발행 모델)
- **API 클라이언트**: `mcp-servers/moai-mcp-threads-poster/src/moai_mcp_threads_poster/threads_api.py`, `instagram_api.py`
- **스킬**: `skills/threads-post-draft/`, `skills/threads-multichannel/`, `skills/instagram-post/`, `skills/instagram-comments/`, `skills/threads-style-learn/` — 현재 위치 (5종)
- **마켓플레이스**: `.claude-plugin/marketplace.json` entry 등록

## 버전

- moai-threads-poster: 1.2.0 (직접 발행 모델 — 큐·스케줄러 제거)
- 스킬 버전: 각 `SKILL.md` frontmatter `version`

---

**문의**: 모두의 AI · MoAI 프로젝트
