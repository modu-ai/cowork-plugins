---
name: threads-post-draft
description: |
  주제를 Threads 게시글 초안으로 작성합니다. 저장된 문체 프로필이 있으면 자동으로 적용합니다. 초안을 사용자에게 보여드리고 승인하면 즉시 Graph API 로 발행합니다 — 큐·예약·상태머신 없이 세션 안에서 직접 발행합니다. 예약·정기 발행은 Claude Cowork 이 담당합니다.
  다음과 같은 요청 시 사용하세요:
  - "이 주제로 Threads 포스트 작성해줘"
  - "Threads에 올릴 글 초안 만들어줘"
  - "이 뉴스를 Threads용으로 요약해줘"
  - "블로그 글을 Threads 포스트로 변환해줘"
  - "내 문체로 초안 작성해줘" (저장된 프로필 자동 적용)
  - "이 초안 그대로 Threads에 올려줘" (승인 → 즉시 발행)
  [책임 경계] vs 형제 스킬: 초안 작성(저장된 문체 프로필 적용 포함) 과 즉시 발행만 담당합니다. 문체 *분석·저장* 은 threads-style-learn, 멀티 채널(Facebook/X) 포맷은 threads-multichannel, 이미지/비디오 발행은 MCP 도구(threads_publish_image, threads_publish_video)를 직접 사용하세요. 예약·정기 발행은 Claude Cowork 에게 맡깁니다.
version: "1.1.2"
---

# Threads 초안 작성·직접 발행 (threads-post-draft)

## 개요

주제를 받아 Threads 최적화 초안을 작성하고, 사용자에게 보여드린 뒤 승인하면 **즉시** Graph API 로 발행합니다. 큐·예약·승인 상태머신은 없습니다 — 세션 안에서 한 흐름으로 작성 → 확인 → 발행합니다.

> 예약·정기 발행(예: "매주 수요일 12시")은 Claude Cowork 이 담당합니다. 본 스킬은 즉시 발행만 합니다.

## 트리거 키워드

Threads, 스레드, 초안, 작성, 발행, 포스트, 게시글, 주제, 변환

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

### 2단계: 사용자에게 초안 보여주기 (승인 게이트)

작성한 초안을 사용자에게 보여드립니다. **승인 없이는 발행하지 않습니다** ("자동 아닌 자율").

- 초안 본문 + 바이트 수 + 토픽 태그/링크를 함께 알려드립니다.
- 사용자가 수정을 요청하면 1단계로 돌아가 다듬습니다.
- 사용자가 승인하면 3단계로 갑니다.

### 3단계: 즉시 발행 (승인 시)

승인된 초안을 `threads_publish_text` 도구로 **즉시** Graph API 발행합니다:

```python
threads_publish_text(text="<승인된 초안>")
# → {media_id, container_id, permalink_hint, note}
```

- 텍스트 전용 발행만 본 스킬이 담당합니다.
- 이미지/비디오 포스트는 `threads_publish_image(text, image_url)` / `threads_publish_video(text, video_url)` 도구를 직접 호출하세요.
- 자격증명(`THREADS_ACCESS_TOKEN`, `THREADS_USER_ID`) 이 미설정이면 `setup_required` 에러를 반환합니다 — 서버는 크래시하지 않습니다. 발급 절차는 `mcp-servers/moai-mcp-threads-poster/CONNECTORS.md` 참조.

> 발행은 세션 안에서 즉시 일어납니다. 백그라운드 자동 발행은 없습니다. 예약이 필요하면 Claude Cowork 에게 맡기세요.

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
## 초안 (검토 요청)

<작성한 초안>

**바이트 수**: N / 500
**토픽 태그**: (선택사항) #태그이름
**링크**: (선택사항) URL

→ 승인하시면 `threads_publish_text` 로 즉시 발행합니다. 수정이 필요하면 말씀해 주세요.
```

승인 후 발행이 끝나면:

```markdown
## 발행 완료

**media_id**: ...
**permalink**: https://www.threads.net/@<username>/post/<media_id>
```

## 주의사항

| 상황 | 대응 |
|------|------|
| 500바이트 초과 시 | 초안을 줄이거나 두 개의 포스트로 분할 제안 |
| 토픽 태그 2개 이상 요청 시 | 1개만 권장 (Threads 알고리즘) |
| 링크 6개 이상 요청 시 | 5개로 제한 (Threads 규격) |
| 이미지/비디오 포함 요청 시 | `threads_publish_image`, `threads_publish_video` 도구 직접 호출 제안 |
| 브랜드 톤 미지정 시 | 업종·타겟 기반 캐주얼 톤 초안 제안 후 확인 |
| `setup_required` 에러 | `THREADS_ACCESS_TOKEN`, `THREADS_USER_ID` 환경변수 설정 (CONNECTORS.md 참조) |
| 예약·정기 발행 요청 시 | Claude Cowork 에게 맡길 것을 안내 (본 스킬은 즉시 발행만) |

## References

| 파일 | 로드 조건 |
|------|-----------|
| references/threads-spec.md | Threads 규격·바이트 계산·토픽 태그·링크 제한 확인 시 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `threads-style-learn` | 문체 분석·저장 (이 스킨이 초안 작성 시 자동 적용) |
| `threads-multichannel` | 초안을 Threads/Facebook/X 용으로 멀티 채널 포맷 |
| `moai-marketer:content-sns-content` | 브랜드 톤 가이드·채널별 최적화 패턴 |

## 이 스킬을 사용하지 말아야 할 때

- 이미지/비디오 포스트 발행: MCP 도구 `threads_publish_image`, `threads_publish_video` 직접 호출
- Facebook/X 용 텍스트 포맷: `threads-multichannel` 스킬
- 문체 분석·저장: `threads-style-learn` 스킬
- 예약·정기 발행: Claude Cowork (본 플러그인은 즉시 발행만)

---

## 발행 전 설정 (최초 1회)

이 스킬을 사용하려면 Threads OAuth 자격증명이 필요합니다. 최초 1회 설정:

**토큰은 `.mcp.json`에 직접 쓰지 마세요.** `.mcp.json`은 저장소에 커밋되는 파일이라,
값을 그대로 넣으면 토큰이 git 이력·diff·배포 패키지에 남습니다. 이 파일에는 **참조만** 둡니다
(저장소의 `.mcp.json`이 이미 이 형태입니다).

```json
{
  "env": {
    "THREADS_ACCESS_TOKEN": "${THREADS_ACCESS_TOKEN}",
    "THREADS_USER_ID": "${THREADS_USER_ID}"
  }
}
```

실제 값은 **운영체제 환경변수**로만 넣습니다. 셸에 따라 형식이 다릅니다.

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

**동작 확인**: `threads_get_profile` 도구 호출 → 프로필 정보 반환되면 연동 성공.
