---
description: Threads 발행 플로우 — 주제 수집 → 초안 작성 → 승인 → 즉시 발행
argument-hint: "[주제 또는 자연어 요청]"
allowed-tools: Skill
---

`/threads-post` — 주제를 주면 초안 작성부터 즉시 발행까지 한 흐름으로 진행합니다. **승인 없이는 발행되지 않습니다.**

> 큐·예약·승인 상태머신은 없습니다. 세션 안에서 초안을 보여드리고 승인하면 즉시 Graph API 로 발행합니다. 예약·정기 발행(예: 매주 수요일 12시)은 Claude Cowork 에게 맡기세요.

1. **주제 수집** — `$ARGUMENTS` 가 비어 있으면 AskUserQuestion 으로 주제·톤·포맷(TEXT / IMAGE / VIDEO) 을 묻는다.
2. **Skill("threads-post-draft")** — 주제 → 초안 작성 (저장된 문체 자동 적용). 초안을 사용자에게 보여준다.
3. **승인 게이트** — 초안을 사용자에게 보여주고 승인을 받는다. 승인 없이는 발행되지 않는다 ("자동 아닌 자율"). 수정 요청 시 2단계로 돌아가 다듬는다.
4. **즉시 발행** — 승인된 초안을 `threads_publish_text` (또는 이미지/비디오는 `threads_publish_image` / `threads_publish_video`) 로 즉시 발행. 결과(`media_id`, `permalink`) 를 반환한다.

주의: 자격증명(`THREADS_ACCESS_TOKEN`, `THREADS_USER_ID`) 이 없으면 발행 단계에서 `setup_required` 스킵된다 (서버는 크래시하지 않는다). 발급 절차는 `mcp-servers/threads-poster/CONNECTORS.md`.
