# 🧵 moai-threads-poster

Threads(Meta) · Instagram 자동 포스팅 전담 플러그인 — Claude Code 에서 MCP 도구로 텍스트·이미지·비디오를 발행합니다.

> **현재 상태**: MCP 서버 + Threads/Instagram API 클라이언트 + 5개 스킬(초안 작성·문체 학습·멀티 채널·Instagram 발행·댓글 관리). 세션 안에서 **직접 발행** (draft → 승인 → 즉시 게시). 예약·정기 발행은 Claude Cowork 이 담당합니다.

## 범위

- **MCP 서버** (`mcp-servers/moai-mcp-threads-poster/`) — stdio 트랜스포트, 17개 도구 노출 (Threads 직접 발행·조회 5종 + Instagram 발행·조회·댓글·인사이트 8종 + 문체 프로필 2종 + 멀티 채널 포맷 1종 + IG 토큰 갱신 1종).
- **Threads API 클라이언트** — `ThreadsClient` (2단계 발행: container 생성 → publish).
- **Instagram API 클라이언트** — `InstagramClient` (Facebook Login for Business, JPEG-only, VIDEO/REELS 컨테이너 폴링).
- **스킬 5종** — 초안 작성(문체 적용) · 문체 학습 · 멀티 채널 포맷 · Instagram 포스트 발행 · Instagram 댓글 관리.
- **문체 학습** — 과거 포스팅으로 문체 프로필을 분석해 저장, 초안 작성에 자동 적용.
- **멀티 채널 배포** — `threads_format_multi_channel` 로 하나의 텍스트를 Threads/Facebook/X 용으로 각각 포맷.

## 설치 (플러그인 등록)

`.claude-plugin/marketplace.json` entry 가 플러그인을 가리킨다. 데스크톱 앱(Claude Cowork·ChatGPT Work)에서는 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에 `modu-ai/moai-cowork`를 추가한 뒤 목록에서 **Install**로 활성화한다. 터미널을 쓴다면 `claude plugin install moai-threads-poster@moai-cowork`(Claude Cowork CLI) 또는 `codex plugin add moai-threads-poster@moai-cowork`(ChatGPT Work CLI). 자격증명(토큰) 발급 절차는 **[`mcp-servers/moai-mcp-threads-poster/CONNECTORS.md`](mcp-servers/moai-mcp-threads-poster/CONNECTORS.md)** 참조.

## 환경변수

| 변수 | 필수 | 설명 |
|---|---|---|
| `THREADS_ACCESS_TOKEN` | 예 (Threads 발행 시) | Threads 장기 액세스 토큰 (60일) |
| `THREADS_USER_ID` | 예 (Threads 발행 시) | Threads 사용자 ID |
| `THREADS_PUBLISH_DELAY` | 아니오 | container 생성 → publish 사이 대기(초, 기본 30). 테스트 시 `0` |
| `IG_ACCESS_TOKEN` | 예 (Instagram 발행 시) | Facebook Page 장기 액세스 토큰 |
| `IG_USER_ID` | 예 (Instagram 발행 시) | Instagram Professional 계정 ID |

Threads 자격증명과 Instagram 자격증명은 *독립적*이다 — Threads-only 세션은 IG 환경변수를 읽지 않는다.

## 로컬 서버 단독 실행

```bash
cd plugins/moai-threads-poster/mcp-servers/moai-mcp-threads-poster
export THREADS_ACCESS_TOKEN=... THREADS_USER_ID=...
uv run moai-mcp-threads-poster   # stdio MCP 서버 기동
```

## 발행 워크플로 (직접 발행 모델)

> **큐·예약·승인 상태머신은 없습니다.** 세션 안에서 초안을 작성해 사용자에게 보여드리고, 승인하면 즉시 Graph API 로 발행합니다. 예약·정기 발행(예: 매주 수요일 12시)은 Claude Cowork 이 담당합니다.

### 플로우

1. **주제 → 초안** — `threads-post-draft` 스킬이 저장된 문체를 적용해 초안을 작성해 사용자에게 보여준다.
2. **승인** — 사용자가 초안을 확인하고 승인하면 발행으로 간다 (승인 없이는 발행하지 않는다 — "자동 아닌 자율").
3. **즉시 발행** — `threads_publish_text` / `threads_publish_image` / `threads_publish_video` 로 Graph API 에 바로 게시. 결과(`media_id`, `permalink`) 를 즉시 반환한다.

```
주제 ──threads-post-draft(문체 적용)──> 초안 ──사용자 승인──> threads_publish_text ──> PUBLISHED
```

Instagram 도 같은 모델이다 — `instagram-post` 스킬이 초안을 작성해 보여드리고, 승인하면 `instagram_publish_image/video/reel` 로 즉시 발행한다.

## 문체 학습 + 멀티 채널 배포

이 플러그인은 Threads·Instagram 발행 외에 **문체 학습**과 **Facebook·X 용 텍스트 제공** 기능을 함께 제공합니다. 핵심 분기:

| 채널 | 직접 발행? | 설명 |
|------|-----------|------|
| **Threads** | 예 (MCP 도구) | 초안 작성 → 승인 → `threads_publish_*` 로 즉시 발행 |
| **Instagram** | 예 (MCP 도구) | 초안 작성 → 승인 → `instagram_publish_*` 로 즉시 발행 (Professional 계정만) |
| **Facebook** | **아니오** (복붙) | 개인 계정은 API 발행이 정책상 불가 → 복붙용 텍스트만 제공 |
| **X (free)** | **아니오** (복붙) | 280자 제한 → `1/`·`2/` 번호 트윗 체인으로 자동 분할, 복붙용 제공 |
| **X (premium)** | **아니오** (복붙) | 25,000자 단일 문자열 그대로, 복붙용 제공 |

### 1. 문체 학습 (`threads-style-learn` 스킬)

과거 Facebook/Threads 포스팅 3-10개를 붙여넣으면 말투·문장 길이·오프닝·클로징·이모지 빈도·시그니처 구절 등을 분석해 **문체 프로필** 을 저장합니다(`threads_style_save`). 저장된 프로필은 이후 `threads-post-draft` 스킬이 초안 작성 시 자동으로 불러와(`threads_style_load`) 적용합니다. 프로필은 `.data/style-profile.md` (gitignored) 에 저장됩니다. **Threads 자격증명 불필요** — 로컬 파일 I/O 만 합니다.

### 2. 초안 작성 (문체 자동 적용)

`threads-post-draft` 스킬은 작성 전 `threads_style_load` 로 프로필을 확인하고, 있으면 그 문체로 초안을 씁니다. 프로필이 없어도 합리적 기본 톤으로 동작합니다. 초안을 사용자에게 보여드리고 승인하면 즉시 발행합니다.

### 3. 멀티 채널 포맷 (`threads-multichannel` 스킬)

작성된 초안을 `threads_format_multi_channel(text, x_tier="free"|"premium")` 로 세 채널용으로 한 번에 포맷합니다:

```python
threads_format_multi_channel(
    text="오늘 점심에 먹은 김치찌개가 진짜 맛있었습니다. ...",
    x_tier="free",  # 무료=280자 분할 / "premium"=25,000자 단일
)
# → {
#     "threads": {"text": "오늘 점심에 ...", "bytes": 412, "max_bytes": 500},
#     "facebook": "오늘 점심에 ...",                       # 복붙용 문자열
#     "x": ["1/ 오늘 점심에 ...", "2/ ...", "3/ ..."],    # free → 분할 리스트
#     "note": "Threads 출력은 threads_publish_text 로 직접 발행하세요. FB·X 출력은 *복붙용*...",
#   }
```

- **Threads 출력** → 승인 시 `threads_publish_text` 등으로 즉시 발행.
- **Facebook·X 출력** → 사용자가 직접 복붙. 이 플러그인은 Facebook/X 로 **발행하지 않습니다**.

> **X tier 차이**: 무료 tier 는 트윗당 280자라 긴 글이 `1/`·`2/` 번호 트윗 체인으로 자동 분할됩니다. X Premium(유료) 은 25,000자까지 한 트윗으로 올릴 수 있어 단일 문자열로 반환됩니다. 어느 쪽이든 *복붙용* 입니다 — 발행은 사용자가 합니다.

---

라이선스: Apache-2.0 · 작성자: 모두의 AI
