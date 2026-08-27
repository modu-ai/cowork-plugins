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
version: "1.2.0"
---

# Instagram 포스트 작성·직접 발행 (instagram-post)

## 개요

주제를 받아 Instagram 최적화 초안(캡션 + 미디어) 을 작성하고, **발행 전에 캡션의 한국어 품질을 감사한 뒤**, 감사를 통과한 최종본을 사용자가 승인하면 **즉시** Graph API 로 발행합니다. 이 스킬은 `instagram_publish_image` / `instagram_publish_video` / `instagram_publish_reel` 도구를 호출합니다.

발행은 공개된 사업 계정에 되돌릴 수 없이 나가는 일입니다. 맞춤법이 틀렸거나 AI 티가 나는 캡션이 한 번 올라가면 그대로 남습니다 — 그래서 감사가 선택이 아니라 필수 단계입니다.

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

### 2단계: 한국어 감사 3단 (발행 전 필수)

캡션을 사용자에게 보여주기 **전에** ⟨한국어 감사 3단⟩을 통과시킨다. 순서는 고정이다:

```
  moai-coworker:ai-slop-reviewer     1차 일반 슬롭 정리
→ moai-writer:korean-spell-check     2차 맞춤법 — 제안 수집 (미공개 정보가 섞였으면 건너뜀)
→ moai-writer:korean-humanize        3차 정밀 윤문 + 맞춤법 반영 + Phase 6 최종 검수
```

- **[HARD] 감사가 승인보다 앞이다.** 승인 뒤에 캡션을 고치면 사용자가 승인한 글과 발행되는 글이 달라진다. 사용자는 **발행될 바로 그 캡션**을 보고 승인해야 한다.
- **[HARD] `korean-humanize`가 마지막이다.** Phase 6 최종 검수가 판정한 **바로 그 산출물**이 발행된다.
- **[HARD] 장르는 `카피`다.** SNS 캡션은 산문이 아니라 카피다. 산문 기준을 들이대면 정상적인 리라이트가 변경률 게이트에 걸려 중단된다.
- **[HARD] 판정이 `hold_and_report`면 발행하지 않는다.** 사유를 그대로 보여주고 1단계로 돌아간다.
- **[HARD] 감사 뒤에 캡션 길이를 다시 센다.** 감사가 문장을 고치므로 2200자 판정은 **최종본** 기준이다.
- 해시태그는 감사 대상이 아니다(고유명사·태그 문자열). 캡션 본문만 태운다.

`korean-spell-check`는 원문을 외부 서비스(`nara-speller.co.kr`)로 보낸다. Instagram 캡션은 어차피 공개될 글이라 보통은 문제가 없다. 다만 **아직 공개되지 않은 정보**(미발표 출시일·비공개 실적·계약 상대방)가 섞였다면 이 단계를 건너뛴다 — 생략해도 `korean-humanize`가 맞춤법을 함께 본다.

### 3단계: 최종본 확인 (승인 게이트)

감사를 통과한 **최종본**을 사용자에게 보여주고 승인을 받는다. **승인 없이는 발행하지 않는다** ("자동 아닌 자율").

- **[HARD] 승인은 사용자에게 승인서를 그대로 보여주고 명시적 응답을 받는다.** 대화체로 "괜찮으세요?"라고 묻지 않는다 — 발행은 되돌릴 수 없으므로 사용자가 명시적으로 고르게 한다.
- **[HARD] 실제로 넘어가는 인자를 전부 보여준다.** 요약이 아니라 다음을 그대로 제시한다:

  | 보여줄 것 | 왜 |
  |---|---|
  | 감사를 통과한 캡션 전문 + 최종 글자 수 | 발행될 문장 그 자체 |
  | 미디어 타입 (IMAGE / VIDEO / REEL) | 어느 도구가 호출되는지 결정 |
  | `image_url` / `video_url` **원문 그대로** | 어떤 이미지·영상이 올라가는지 |
  | 릴이면 `share_to_feed` 값 | `True`면 **피드에도** 공유된다 — 요약에 묻히면 사용자가 모른 채 승인한다 |
  | 발행 계정 (`instagram_get_profile` 의 username) | 여러 계정을 쓰는 경우 오발행 방지 |
  | 해시태그 목록 | |
  | 감사 3단 결과 한 줄 | 무엇이 바뀌었는지 |

- 사용자가 수정을 요청하면 1단계로 돌아가 다듬고, **감사 3단을 다시 통과시킨 뒤** 재승인을 받는다.
- 사용자가 승인하면 4단계로 간다.

선택지는 「이대로 발행」 / 「수정 요청」 / 「발행 취소」로 구성한다.

### 4단계: 즉시 발행 (승인 시)

승인된 초안을 미디어 타입에 맞춰 즉시 발행한다:

```python
instagram_publish_image(text="<캡션>", image_url="https://example.com/photo.jpg")
# → {media_id, container_id, permalink_hint, platform: "instagram"}
```

```python
instagram_publish_reel(text="<캡션>", video_url="https://example.com/reel.mp4", share_to_feed=True)
# REELS/VIDEO 는 container 가 FINISHED 될 때까지 폴링 후 발행된다.
```

**[HARD] 애매하게 실패하면 재시도하지 않는다.** Instagram 발행은 컨테이너 생성 → 발행 2단계이고, 릴·비디오는 컨테이너가 `FINISHED` 될 때까지 폴링한다. 타임아웃·응답 없음으로 끝나면 **1단계만 성공했을 수 있다** — 그대로 다시 호출하면 같은 글이 두 번 올라가거나 중복 컨테이너가 남는다.

**[HARD] 이 서버에는 발행 여부를 되물을 도구가 없다.** `instagram_get_profile`은 계정 정보만 반환하고, `instagram_insights`·`instagram_comments_list`는 조회하려면 이미 `media_id`가 있어야 하는데 애매한 실패에서는 그 값이 없다. 따라서 **사용자에게 Instagram 앱에서 직접 확인해 달라고 요청**하고, 올라가지 않았다는 확인을 받은 뒤에만 다시 발행한다. 스킬이 혼자 판단하지 않는다.

> 발행은 세션 안에서 즉시 일어난다. 백그라운드 자동 발행은 없다. 예약이 필요하면 Claude Cowork 에게 맡긴다.

## 주의사항

| 상황 | 대응 |
|------|------|
| 이미지가 PNG | JPEG 로 변환 후 재시도 (`.png` URL 은 빠른 실패) |
| 미디어 URL 이 비공개 | 공개 URL 사용 (Meta 가 서버에서 fetch) |
| `setup_required` 에러 | `IG_ACCESS_TOKEN`, `IG_USER_ID` 환경변수 설정 (CONNECTORS.md 참조) |
| Personal 계정 오류 | Instagram Professional(Business/Creator) 계정만 지원 — 계정 전환 필요 |
| 예약·정기 발행 요청 시 | Claude Cowork 에게 맡길 것을 안내 (본 스킬은 즉시 발행만) |
| 감사 3단에서 `hold_and_report` 판정 | 발행하지 않음. 사유를 그대로 보여주고 1단계로 복귀 |
| 캡션에 미공개 정보가 섞임 | `korean-spell-check` 생략 (외부 전송) — 생략 사실을 결과에 적음 |
| 발행 도구가 애매하게 실패 | 재시도 금지. 사용자에게 Instagram 앱 확인을 요청한 뒤 판단 |
| "감사 건너뛰고 바로 올려줘" 요청 | 건너뛰지 않음. 되돌릴 수 없는 공개 발행이라는 점을 알리고 감사 진행 |

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

**토큰은 `.mcp.json`에 직접 쓰지 않는다.** 이 파일은 저장소에 커밋되므로 값을 그대로 넣으면
토큰이 git 이력·diff·배포 패키지에 남는다. 파일에는 **참조만** 둔다.

```json
{
  "env": {
    "IG_ACCESS_TOKEN": "${IG_ACCESS_TOKEN}",
    "IG_USER_ID": "${IG_USER_ID}"
  }
}
```

실제 값은 운영체제 환경변수로만 넣는다.

**macOS / Linux**:

```bash
export IG_ACCESS_TOKEN="<Facebook Page 장기 액세스 토큰>"
export IG_USER_ID="<Instagram Professional 계정 ID>"
```

**Windows** (PowerShell):

```powershell
$env:IG_ACCESS_TOKEN = "<Facebook Page 장기 액세스 토큰>"
$env:IG_USER_ID = "<Instagram Professional 계정 ID>"
```

발급 절차(Meta App → Facebook Login → 장기 Page 토큰 → IG_USER_ID 해석) 는 `mcp-servers/moai-mcp-threads-poster/CONNECTORS.md` 의 Instagram 섹션 참조.

**동작 확인**: `instagram_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `instagram-comments` | 발행 후 댓글 관리 (목록/답글/숨김) |
| `threads-post-draft` | Threads 용 초안 작성·발행 |
| `threads-style-learn` | 문체 프로필 분석·저장 (본 스킬이 초안에 적용) |
| `moai-coworker:ai-slop-reviewer` | 감사 3단 1차 — 일반 AI 슬롭 정리 (발행 전 필수) |
| `moai-writer:korean-spell-check` | 감사 3단 2차 — 맞춤법·띄어쓰기 (미공개 정보 시 생략) |
| `moai-writer:korean-humanize` | 감사 3단 3차 — 정밀 윤문 + 최종 검수 (`장르: 카피`, 발행 전 필수·마지막) |

## 이 스킬을 사용하지 말아야 할 때

- 댓글 관리: `instagram-comments` 스킬 사용
- Threads 발행: `threads-*` 스킬 / 도구 사용
- 예약·정기 발행: Claude Cowork (본 플러그인은 즉시 발행만)
