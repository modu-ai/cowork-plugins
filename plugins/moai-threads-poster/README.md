# 🧵 moai-threads-poster

Threads(Meta) 자동 포스팅 전담 플러그인 — Claude Code 에서 MCP 도구로 Threads 계정에 텍스트·이미지·비디오를 발행합니다.

> **현재 상태**: MCP 서버 + Threads API 클라이언트 + SQLite 발행 큐 + 5개 스킬(초안 작성·승인·조회·문체 학습·멀티 채널) + 분산 등록(batch). Threads 직접 발행 + Facebook·X 복붙용 텍스트 제공. 수동 승인 기반 발행 모델.

## 범위

- **MCP 서버** (`mcp-servers/threads-poster/`) — stdio 트랜스포트, 14개 도구 노출 (즉시 발행 5종 + 큐 관리 6종 + 문체 프로필 2종 + 멀티 채널 포맷 1종).
- **Threads API 클라이언트** — `ThreadsClient` (2단계 발행: container 생성 → publish).
- **SQLite 발행 큐** — PENDING → APPROVED → PUBLISHED 상태 머신 + 24h 레이트리밋 가드.
- **스킬 5종** — 초안 작성(문체 적용) · 승인/예약 · 상태 조회 · 문체 학습 · 멀티 채널 포맷.
- **분산 등록(batch)** — `threads_queue_add_batch` 로 여러 초안을 베스트 슬롯에 자동 분산.
- **문체 학습** — 과거 포스팅으로 문체 프로필을 분석해 저장, 초안 작성에 자동 적용.
- **멀티 채널 배포** — `threads_format_multi_channel` 로 하나의 텍스트를 Threads/Facebook/X 용으로 각각 포맷.

## 설치 (플러그인 등록)

`.claude-plugin/marketplace.json` entry 가 플러그인을 가리킨다. Claude Code 의 `/plugin` 명령으로 활성화. 자격증명(토큰) 발급 절차는 **[`mcp-servers/threads-poster/CONNECTORS.md`](mcp-servers/threads-poster/CONNECTORS.md)** 참조.

## 환경변수

| 변수 | 필수 | 설명 |
|---|---|---|
| `THREADS_ACCESS_TOKEN` | 예 | Threads 장기 액세스 토큰 (60일) |
| `THREADS_USER_ID` | 예 | Threads 사용자 ID |
| `THREADS_PUBLISH_DELAY` | 아니오 | container 생성 → publish 사이 대기(초, 기본 30). 테스트 시 `0` |

## 로컬 서버 단독 실행

```bash
cd plugins/moai-threads-poster/mcp-servers/threads-poster
export THREADS_ACCESS_TOKEN=... THREADS_USER_ID=...
uv run threads-poster-mcp   # stdio MCP 서버 기동
```

## 발행 워크플로 (수동 승인 + 분산 등록)

> **launchd 자동 발행은 제거되었습니다.** 세션 단위로 동작하는 cowork 의 스케줄링 모델 · write-금지 cadence-bridge 원칙과 충돌하기 때문입니다. 발행하려면 **세션을 켜고 승인**해야 합니다.

**베스트 프랙티스**: 주 3-5회, 화·수·목 요일에 게시. 피크 슬롯은 수요일 12:00-14:00 (Asia/Seoul). 자세한 케이던스 값은 [`config/threads.yaml`](config/threads.yaml).

### 플로우

1. **주제 수집 → 초안** — `threads-post-draft` 스킬 (또는 `threads_queue_add`) 로 큐에 `PENDING` 등록.
2. **승인** — 사용자가 초안을 확인하고 승인하면 `PENDING → APPROVED`.
3. **분할 등록(batch)** — `threads_queue_add_batch(posts=[...], cadence="weekly_3")` 로 승인된 초안 N 개를 화/수/목 12:00 슬롯에 자동 분산 예약.
4. **(세션에서) 발행** — 예약 시각이 도래한 포스트를 `threads_queue_publish_due` 로 발행. 상태는 `threads-status` 스킬로 확인.

```
승인된 초안 N개 ──threads_queue_add_batch(cadence="weekly_3")──> 화 12:00 / 수 12:00 / 목 12:00 ...
                                                                 │
                                 (세션 안에서) threads_queue_publish_due ──> PUBLISHED
```

### CLI 수동 킥 (선택)

발행 큐 runner CLI 는 여전히 셸에서 수동 1회 킥용으로 사용 가능 (`--once`, `--dry-run`). 단 launchd/cron 연동은 더 이상 없습니다.

```bash
uv run --directory plugins/moai-threads-poster/mcp-servers/threads-poster threads-poster-runner --once <post_id>
```

## 문체 학습 + 멀티 채널 배포

이 플러그인은 Threads 발행 외에 **문체 학습**과 **Facebook·X 용 텍스트 제공** 기능을 함께 제공합니다. 핵심 분기:

| 채널 | 직접 발행? | 설명 |
|------|-----------|------|
| **Threads** | 예 (MCP 도구) | 큐 등록 → 승인 → `threads_queue_publish_due` 로 직접 발행 |
| **Facebook** | **아니오** (복붙) | 개인 계정은 API 발행이 정책상 불가 → 복붙용 텍스트만 제공 |
| **X (free)** | **아니오** (복붙) | 280자 제한 → `1/`·`2/` 번호 트윗 체인으로 자동 분할, 복붙용 제공 |
| **X (premium)** | **아니오** (복붙) | 25,000자 단일 문자열 그대로, 복붙용 제공 |

### 1. 문체 학습 (`threads-style-learn` 스킬)

과거 Facebook/Threads 포스팅 3-10개를 붙여넣으면 말투·문장 길이·오프닝·클로징·이모지 빈도·시그니처 구절 등을 분석해 **문체 프로필** 을 저장합니다(`threads_style_save`). 저장된 프로필은 이후 `threads-post-draft` 스킬이 초안 작성 시 자동으로 불러와(`threads_style_load`) 적용합니다. 프로필은 `.data/style-profile.md` (gitignored) 에 저장됩니다. **Threads 자격증명 불필요** — 로컬 파일 I/O 만 합니다.

### 2. 초안 작성 (문체 자동 적용)

`threads-post-draft` 스킬은 작성 전 `threads_style_load` 로 프로필을 확인하고, 있으면 그 문체로 초안을 씁니다. 프로필이 없어도 합리적 기본 톤으로 동작합니다.

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
#     "note": "Threads 출력은 queue 도구로... FB·X 출력은 *복붙용*...",
#   }
```

- **Threads 출력** → `threads_queue_add` / `threads_queue_add_batch` 로 큐에 넘겨 직접 발행.
- **Facebook·X 출력** → 사용자가 직접 복붙. 이 플러그인은 Facebook/X 로 **발행하지 않습니다**.

> **X tier 차이**: 무료 tier 는 트윗당 280자라 긴 글이 `1/`·`2/` 번호 트윗 체인으로 자동 분할됩니다. X Premium(유료) 은 25,000자까지 한 트윗으로 올릴 수 있어 단일 문자열로 반환됩니다. 어느 쪽이든 *복붙용* 입니다 — 발행은 사용자가 합니다.

## 로드맵 (M1 → M5)

- **M1**: MCP 서버 + API 클라이언트
- **M2**: 발행 큐 + 재시도/레이트리밋(250/24h)
- **M3**: 발행 스킬 (콘텐츠 작성 → 게시 한 번에)
- **M4**: 제거됨 — 수동 승인 모델로 전환 (launchd 자동 발행 폐기)
- **M5**: 마켓플레이스 등록

---

라이선스: Apache-2.0 · 작성자: 모두의 AI
