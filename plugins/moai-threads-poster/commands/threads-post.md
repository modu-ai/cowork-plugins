---
description: Threads 발행 플로우 — 주제 수집 → 초안 → 승인 → 분산 등록(batch) → 세션에서 발행
argument-hint: "[주제 또는 자연어 요청]"
allowed-tools: Skill
---

`/threads-post` — 주제를 주면 초안 작성부터 분산 등록·발행까지 한 흐름으로 진행합니다. **승인 없이는 발행되지 않습니다.**

> 자동 백그라운드 발행(launchd) 은 제거되었습니다. 발행하려면 **세션을 켜고** `threads_queue_publish_due` 를 호출해야 합니다.

1. **주제 수집** — `$ARGUMENTS` 가 비어 있으면 AskUserQuestion 으로 주제·톤·포맷(TEXT / IMAGE / VIDEO) 을 묻는다. 여러 주제가 주어지면 한 번에 분산 등록한다.
2. **Skill("threads-post-draft")** — 주제 → 초안 작성, 큐에 `PENDING` 으로 등록.
3. **승인 게이트** — 초안을 사용자에게 보여주고 승인을 받는다. 승인 없이는 발행되지 않는다.
4. **분할 등록(batch)** — 승인된 초안을 `threads_queue_add_batch` 로 화/수/목 피크 슬롯에 분산 예약(`cadence="weekly_3"`, 기본). 한 주 치를 한 번에 예약할 때 특히 유용하다.
5. **(세션에서) publish_due** — 예약 시각이 도래한 포스트를 `threads_queue_publish_due` 로 발행. 상태 조회는 Skill("threads-status").

주의: 자격증명(`THREADS_ACCESS_TOKEN`, `THREADS_USER_ID`) 이 없으면 발행 단계에서 스킵된다. 발급 절차는 `mcp-servers/threads-poster/CONNECTORS.md`.
