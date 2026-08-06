---
name: instagram-comments
description: |
  Instagram 미디어의 댓글을 관리합니다 — 목록 조회, 답글 작성, 댓글 숨김. `manage_comments` 권한이 부여된 경우에만 동작합니다. 발행된 게시물의 댓글 모더레이션(응대/정리) 에 사용합니다.
  다음과 같은 요청 시 사용하세요:
  - "인스타 게시물 댓글 확인해줘"
  - "이 댓글에 답글 달아줘"
  - "스팸 댓글 숨겨줘"
  - "최근 포스트 댓글 정리해줘"
  - "특정 댓글 숨김 처리해줘"
  [책임 경계] vs 형제 스킬: Instagram 댓글 *조회/답글/숨김* 만 담당합니다. 포스트 발행은 instagram-post 스킬, 인사이트 조회는 instagram_insights 도구를 직접 사용하세요.
version: "1.0.0"
---

# Instagram 댓글 관리 (instagram-comments)

## 개요

발행된 Instagram 미디어의 댓글을 조회하고, 답글을 달고, 댓글을 숨긴다. 이 스킬은 Instagram Graph API 의 댓글 엔드포인트(`manage_comments` 권한 게이트) 를 통해 `instagram_comments_list` / `instagram_comments_reply` / `instagram_comments_hide` 도구를 호출한다.

> **권한**: 세 가지 도구 모두 Meta 앱에 `manage_comments` 권한이 부여되어 있어야 한다. 권한이 없으면 API 가 거부한다.

## 트리거 키워드

댓글, comment, 답글, reply, 숨김, hide, 모더레이션, 스팸, 정리

## 워크플로우

### 1단계: 댓글 목록 조회

특정 미디어(`media_id`) 의 댓글을 나열한다:

```python
instagram_comments_list(media_id="<미디어 ID>")
# → {"data": [{"id", "text", "username", "timestamp", "hidden": false}, ...]}
```

- `media_id` 는 `instagram_publish_image` 등 발행 도구가 반환한 `media_id` (또는 `instagram_insights` 로 조회한 미디어 ID).

### 2단계: 답글 작성

특정 댓글(`comment_id`) 에 답글을 단다:

```python
instagram_comments_reply(comment_id="<댓글 ID>", text="<답글 본문>")
# → {"id": "<새 답글 ID>"}
```

답글 본문도 저장된 문체 프로필을 반영해 작성한다 (있으면). 공격적/스팸 댓글에는 답글 대신 숨김을 권장.

### 3단계: 댓글 숨김

스팸/비난 댓글을 숨긴다 (삭제가 아님 — 작성자와 페이지 관리자만 안 보이거나, 정책에 따라 전체 숨김):

```python
instagram_comments_hide(comment_id="<댓글 ID>")
# → {"hidden": true}
```

숨김은 가역적이다 — Meta 정책에 따라 다시 보이게 할 수 있다.

## 주의사항

| 상황 | 대응 |
|------|------|
| `manage_comments` 권한 없음 | Meta 앱 검수(App Review) 로 권한 추가 필요 |
| `setup_required` 에러 | `IG_ACCESS_TOKEN` / `IG_USER_ID` 환경변수 설정 |
| Personal 계정 | Graph API 미지원 — Professional 계정 필요 |
| 엔드포인트 미검증 | comments 엔드포인트 경로는 run-phase 검증 대상(@MX:TODO) — 최초 사용 시 공식 문서로 경로 재확인 권장 |

## 출력 형식

```markdown
## 댓글 관리 결과

**미디어**: <media_id>
**댓글 수**: N

| 댓글 ID | 작성자 | 본문 | 상태 |
|---|---|---|---|
| ... | ... | ... | 표시/숨김 |

**조치**: (답글/숨김 내역)
```

## 발행 전 설정 (최초 1회)

Threads 와 동일한 Instagram 자격증명(`IG_ACCESS_TOKEN` / `IG_USER_ID`) 에 추가로 Meta 앱에 `manage_comments` 권한이 부여되어야 한다. 발급 절차는 `mcp-servers/threads-poster/CONNECTORS.md` 의 Instagram 섹션 참조.

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `instagram-post` | 포스트 발행 (댓글 관리 전에 발행이 선행) |

## 이 스킬을 사용하지 말아야 할 때

- 포스트 발행: `instagram-post` 스킬
- 인사이트 조회: `instagram_insights` 도구 직접 호출
- Threads 댓글: Threads API 는 본 플러그인 범위 밖
