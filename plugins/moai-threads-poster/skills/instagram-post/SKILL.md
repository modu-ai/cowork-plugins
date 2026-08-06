---
name: instagram-post
description: |
  주제를 Instagram 게시글(이미지/비디오/릴) 초안으로 작성해 즉시 발행합니다. 저장된 문체 프로필이 있으면 자동 적용합니다. 큐·예약·상태머신 없이 세션 안에서 직접 발행합니다. 예약·정기 발행은 Claude Cowork 이 담당합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 주제로 Instagram 포스트 작성해줘"
  - "인스타에 올릴 이미지 캡션 써줘"
  - "이 영상 인스타 릴로 올려줘" (share_to_feed)
  - "인스타에 비디오 게시해줘"
  - "이 뉴스를 Instagram 용으로 요약해줘"
  - "이 초안 인스타에 바로 올려줘" (승인 → 즉시 발행)
  [책임 경계] vs 형제 스킬: Instagram 이미지/비디오/릴 *초안 작성·즉시 발행* 만 담당합니다. 댓글 관리는 instagram-comments 스킬, Threads 발행은 threads-* 스킬, 멀티 채널 포맷은 threads-multichannel 스킬을 사용하세요. 예약·정기 발행은 Claude Cowork 에게 맡깁니다.
version: "1.1.0"
---

# Instagram 포스트 작성·직접 발행 (instagram-post)

## 개요

주제를 받아 Instagram 최적화 초안(캡션 + 미디어) 을 작성하고, 사용자에게 보여드린 뒤 승인하면 **즉시** Graph API 로 발행합니다. 이 스킬은 `instagram_publish_image` / `instagram_publish_video` / `instagram_publish_reel` 도구를 호출합니다.

> **Instagram Professional(Business 또는 Creator) 계정만 지원** 됩니다. Personal 계정은 Graph API 로 발행할 수 없습니다.

> 예약·정기 발행은 Claude Cowork 이 담당합니다. Instagram Graph API 자체가 서버 측 스케줄링 파라미터를 제공하지 않으므로, 본 스킬은 즉시 발행만 합니다.

## 트리거 키워드

Instagram, 인스타, 인스타그램, 릴, REEL, 캡션, 이미지 발행, 비디오 발행

## 워크플로우

### 0단계: 문체 적용 (있으면)

초안 작성 *전* 에 `threads_style_load` 로 저장된 문체 프로필을 확인한다 (Threads 스킬이 저장한 프로필을 Instagram 캡션에도 재사용). 프로필이 있으면 그 차원(말투·문장 길이·오프닝·이모지·시그니처) 을 캡션에 반영한다.

### 1단계: 미디어 타입 결정 + 캡션 작성

| 미디어 | 도구 | 비고 |
|---|---|---|
| 이미지 | `instagram_publish_image` | **JPEG-only** (PNG 거부됨 — Threads 와 상이) |
| 비디오 | `instagram_publish_video` | 공개 URL, container 폴링 후 발행 |
| 릴 | `instagram_publish_reel` | `share_to_feed=True` (기본) 면 피드에도 공유 |

- **캡션**: Instagram 캡션은 2200자 권장(해시태그 포함). 핵심 메시지는 첫 2줄에.
- **해시태그**: 5-15개 권장. 본문과 분리해 마지막에 배치하거나 첫 댓글로.
- **이미지 URL**: 반드시 **공개 접근 가능** 해야 한다 (Meta 가 서버에서 cURL 로 가져간다). 비공개/서명 URL 은 거부된다.

### 2단계: 사용자에게 초안 보여주기 (승인 게이트)

작성한 캡션과 미디어 URL 을 사용자에게 보여드린다. **승인 없이는 발행하지 않는다** ("자동 아닌 자율").

- 캡션 본문 + 미디어 타입 + 미디어 URL 을 함께 알려드린다.
- 사용자가 수정을 요청하면 1단계로 돌아가 다듬는다.
- 사용자가 승인하면 3단계로 간다.

### 3단계: 즉시 발행 (승인 시)

승인된 초안을 미디어 타입에 맞춰 즉시 발행한다:

```python
instagram_publish_image(text="<캡션>", image_url="https://example.com/photo.jpg")
# → {media_id, container_id, permalink_hint, platform: "instagram"}
```

```python
instagram_publish_reel(text="<캡션>", video_url="https://example.com/reel.mp4", share_to_feed=True)
# REELS/VIDEO 는 container 가 FINISHED 될 때까지 폴링 후 발행된다.
```

> 발행은 세션 안에서 즉시 일어난다. 백그라운드 자동 발행은 없다. 예약이 필요하면 Claude Cowork 에게 맡긴다.

## 주의사항

| 상황 | 대응 |
|------|------|
| 이미지가 PNG | JPEG 로 변환 후 재시도 (`.png` URL 은 빠른 실패) |
| 미디어 URL 이 비공개 | 공개 URL 사용 (Meta 가 서버에서 fetch) |
| `setup_required` 에러 | `IG_ACCESS_TOKEN`, `IG_USER_ID` 환경변수 설정 (CONNECTORS.md 참조) |
| Personal 계정 오류 | Instagram Professional(Business/Creator) 계정만 지원 — 계정 전환 필요 |
| 예약·정기 발행 요청 시 | Claude Cowork 에게 맡길 것을 안내 (본 스킬은 즉시 발행만) |

## 출력 형식

```markdown
## Instagram 포스트 (발행 완료)

<캡션>

**미디어**: IMAGE / VIDEO / REEL — <URL>
**해시태그**: # ...

**결과**:
- media_id: ... · permalink: https://www.instagram.com/p/.../
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
| `threads-post-draft` | Threads 용 초안 작성·발행 |
| `threads-style-learn` | 문체 프로필 분석·저장 (본 스킬이 초안에 적용) |

## 이 스킬을 사용하지 말아야 할 때

- 댓글 관리: `instagram-comments` 스킬 사용
- Threads 발행: `threads-*` 스킬 / 도구 사용
- 예약·정기 발행: Claude Cowork (본 플러그인은 즉시 발행만)
