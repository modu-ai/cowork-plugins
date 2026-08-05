---
name: instagram-post
description: |
  주제를 Instagram 게시글(이미지/비디오/릴) 초안으로 작성해 발행 큐에 PENDING 으로 등록하거나 즉시 발행합니다. Instagram 은 서버 측 스케줄링을 지원하지 않으므로 예약은 큐에 intent 를 보관하고 예정 시각에 사용자가 발행 트리거를 당기는 모델입니다. 저장된 문체 프로필이 있으면 자동 적용합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 주제로 Instagram 포스트 작성해줘"
  - "인스타에 올릴 이미지 캡션 써줘"
  - "이 영상 인스타 릴로 올려줘" (share_to_feed)
  - "인스타에 비디오 게시해줘"
  - "이 뉴스를 Instagram 용으로 요약해줘"
  - "수요일 12시에 인스타 예약해줘" (큐 등록 — 예정 시각에 사용자가 발행)
  [책임 경계] vs 형제 스킬: Instagram 이미지/비디오/릴 *초안·예약·즉시 발행* 만 담당합니다. 댓글 관리는 instagram-comments 스킬, Threads 발행은 threads-* 스킬, 멀티 채널 포맷은 threads-multichannel 스킬을 사용하세요. Instagram 큐 상태 조회는 threads_queue_list / threads_queue_get 도구를 사용하세요.
version: "1.0.0"
---

# Instagram 포스트 작성·발행 (instagram-post)

## 개요

주제를 받아 Instagram 최적화 초안(캡션 + 미디어) 을 작성하고, **즉시 발행** 하거나 **예약 큐에 등록** 합니다. 이 스킬은 Instagram Graph API(Facebook Login for Business) 를 통해 `instagram_publish_image` / `instagram_publish_video` / `instagram_publish_reel` / `instagram_schedule` 도구를 호출합니다.

> **Instagram Professional(Business 또는 Creator) 계정만 지원** 됩니다. Personal 계정은 Graph API 로 발행할 수 없습니다.

## 핵심: Instagram 은 서버 측 스케줄링이 없다 (REQ-INST-009)

다른 소셜 API 와 달리 **Instagram Graph API 는 `scheduled_publish_time` 이나 `published=false + timestamp` 같은 서버 측 스케줄링 파라미터를 제공하지 않습니다.** 따라서:

- **예약** = 발행 큐에 *intent*(캡션 + 미디어 URL + 예정 시각) 를 `platform='instagram'` 으로 **보관만** 한다 (`instagram_schedule`). API 는 일절 호출하지 않는다.
- **발행** = 예정 시각이 도래한 뒤, 사용자가 세션에서 `instagram_queue_publish_due` 도구를 호출할 때 비로소 container 생성 → publish 가 일어난다.
- **백그라운드 자동 발행(launchd/cron/daemon) 은 없다.** "수요일 12시에 예약" 은 큐에 해당 시각의 intent 를 넣어둔 상태이고, 수요일 12시 이후에 사용자가 세션을 열어 발행 트리거를 당겨야 실제 게시된다.

이 모델은 Threads 플러그인의 "수동 승인 + 분산 등록" 모델과 동일하며, 두 플랫폼이 하나의 통합 큐를 공유한다 (`platform` 컬럼으로 구분).

## 트리거 키워드

Instagram, 인스타, 인스타그램, 릴, REEL, 캡션, 이미지 발행, 비디오 발행, 예약

## 워크플로우

### 0단계: 문체 적용 (있으면)

초안 작성 *전* 에 `threads_style_load` 로 저장된 문체 프로필을 확인한다 (Threads 스킬이 저장한 프로필을 Instagram 캡션에도 재사용). 프로필이 있으면 그 차원(말투·문장 길이·오프닝·이모지·시그니처) 을 캡션에 반영한다.

### 1단계: 미디어 타입 결정 + 캡션 작성

| 미디어 | 도구 | 비고 |
|---|---|---|
| 이미지 | `instagram_publish_image` / `instagram_schedule(media_type="IMAGE")` | **JPEG-only** (PNG 거부됨 — Threads 와 상이) |
| 비디오 | `instagram_publish_video` / `instagram_schedule(media_type="VIDEO")` | 공개 URL, container 폴링 후 발행 |
| 릴 | `instagram_publish_reel` / `instagram_schedule(media_type="REELS")` | `share_to_feed=True` (기본) 면 피드에도 공유 |

- **캡션**: Instagram 캡션은 2200자 권장(해시태그 포함). 핵심 메시지는 첫 2줄에.
- **해시태그**: 5-15개 권장. 본문과 분리해 마지막에 배치하거나 첫 댓글로.
- **이미지 URL**: 반드시 **공개 접근 가능** 해야 한다 (Meta 가 서버에서 cURL 로 가져간다). 비공개/서명 URL 은 거부된다.

### 2단계: 즉시 발행 vs 예약

**즉시 발행** — 당장 게시:

```python
instagram_publish_image(text="<캡션>", image_url="https://example.com/photo.jpg")
# → {media_id, container_id, permalink_hint, platform: "instagram"}
```

```python
instagram_publish_reel(text="<캡션>", video_url="https://example.com/reel.mp4", share_to_feed=True)
# REELS/VIDEO 는 container 가 FINISHED 될 때까지 폴링 후 발행된다.
```

**예약(큐 등록)** — intent 보관, 예정 시각에 사용자가 발행:

```python
instagram_schedule(
    media_type="IMAGE",                    # IMAGE | VIDEO | REELS (TEXT 불가)
    text="<캡션>",
    image_url="https://example.com/photo.jpg",
    scheduled_at="2026-08-12T12:00:00+09:00",  # 예정 시각 (Asia/Seoul)
)
# → {post_id, status: "PENDING", platform: "instagram", scheduled_at: ...}
```

예약 row 는 PENDING 이므로, 발행 가능 상태(APPROVED) 로 만들려면 승인이 필요하다:

```python
threads_queue_approve(post_id=<위 post_id>, scheduled_at="2026-08-12T12:00:00+09:00")
```

### 3단계: 예정 시각 도래 후 발행

예약 시각이 지난 뒤, 사용자가 세션에서:

```python
instagram_queue_publish_due(limit=10)
# → due Instagram row 들을 container 생성 → (VIDEO/REELS 폴링) → publish.
#   {published, failed, skipped, messages}
```

이것이 Instagram 의 **유일한 발행 트리거** 다. 자동 백그라운드 발행은 없다.

> IG 자격증명이 미설정이어도 이 도구는 크래시하지 않는다 — 각 due row 를 `setup_required` 스킵하고 정상 반환한다. 자격증명을 설정한 뒤 다시 호출하면 발행된다.

## 주의사항

| 상황 | 대응 |
|------|------|
| 이미지가 PNG | JPEG 로 변환 후 재시도 (`.png` URL 은 빠른 실패) |
| 미디어 URL 이 비공개 | 공개 URL 사용 (Meta 가 서버에서 fetch) |
| `setup_required` 에러 | `IG_ACCESS_TOKEN`, `IG_USER_ID` 환경변수 설정 (CONNECTORS.md 참조) |
| Personal 계정 오류 | Instagram Professional(Business/Creator) 계정만 지원 — 계정 전환 필요 |
| HTTP 24h 한도 (100건) | `instagram_queue_publish_due` 가 한도 도달 시 남은 IG row 를 스킵한다 |
| REELS 예약 시 `share_to_feed` | 현재 예약 큐가 이 값을 보관하지 않는다 (@MX:DEBT) — 즉시 발행(`instagram_publish_reel`) 에서만 적용 |

## 출력 형식

```markdown
## Instagram 포스트 (발행/예약 완료)

<캡션>

**미디어**: IMAGE / VIDEO / REEL — <URL>
**해시태그**: # ... 

**결과**:
- (즉시 발행) media_id: ... · permalink: https://www.instagram.com/p/.../
- (예약) post_id: ... · status: PENDING · platform: instagram · scheduled_at: ...

**다음 단계**: (예약 시) 예정 시각 도래 후 `instagram_queue_publish_due` 로 발행.
```

## 발행 전 설정 (최초 1회)

Instagram 자격증명(Threads 와 별개) 이 필요하다:

```bash
export IG_ACCESS_TOKEN="<Facebook Page 장기 액세스 토큰>"
export IG_USER_ID="<Instagram Professional 계정 ID>"
```

발급 절차(Meta App → Facebook Login → 장기 Page 토큰 → IG_USER_ID 해석) 는 `mcp-servers/threads-poster/CONNECTORS.md` 의 Instagram 섹션 참조.

**동작 확인**: `instagram_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `instagram-comments` | 발행 후 댓글 관리 (목록/답글/숨김) |
| `threads-post-draft` | Threads 용 초안 작성 (같은 통합 큐 공유) |
| `threads-style-learn` | 문체 프로필 분석·저장 (본 스킬이 초안에 적용) |

## 이 스킬을 사용하지 말아야 할 때

- 댓글 관리: `instagram-comments` 스킬 사용
- Threads 발행: `threads-*` 스킬 / 도구 사용
- 큐 상태 조회: `threads_queue_list` / `threads_queue_get` 도구 사용
