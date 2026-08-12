---
title: "「스토리 크리에이터」 — 웹툰·웹소설·IP 창작 담당"
weight: 3
description: "웹툰·웹소설·시나리오·콘티·캐릭터 시트·표지·시네마틱 프리비즈·IP 피칭까지 스토리/IP 창작을 담당하는 AI 코워커."
aliases: ["/agent-teams/story/"]
date: 2026-08-07T00:00:00+09:00
lastmod: 2026-08-13T00:00:00+09:00
---

한 명의 창작자가 기획·원고·콘티·캐릭터·표지를 다 하는 건 현실적으로 벅찹니다. 스토리 크리에이터는 웹툰·웹소설·영상 시나리오 창작의 파이프라인을 한 코워커 안에 모아 둔 역할입니다. 출판사의 편집장 겸 기획자처럼, 장르와 단계에 맞춰 다음 작업을 이어갑니다.

스킬은 크게 기획·설계 두 계열로 나뉩니다. 기획 계열(story-synopsis·story-screenplay·story-webtoon-planner·story-project)은 줄거리·시나리오·에피소드 설계를 맡고, 설계 계열(story-webtoon-art·story-conti·story-character-sheet·story-cover-art·story-previz)은 작화·콘티·캐릭터 시트·표지·프리비즈의 사양과 프롬프트를 조립합니다. 이 설계 스킬들은 생성 직접 실행하지 않고 **생성 실행은 moai-media에 위임**합니다 — moai-media가 Higgsfield MCP를 구동해 크레딧 조회·모델 선택·이미지 생성을 마무리합니다. IP 사업화는 story-ip-pitch가 다룹니다. 이전 버전에서 작가(출판)로부터 스토리/IP 도메인이 분리되어 신설되었습니다.

장편일수록 설정 충돌이 문제인 만큼, 연재를 관통하는 설정(캐릭터·시점·사건) 일관성을 검수하는 코워커가 붙어 있습니다.

```mermaid
flowchart LR
   A["요청<br/>(웹툰 신작 기획해줘)"] --> B["스킬 매칭"]
   B --> C["story-director<br/>기획·원고·콘티·작화"]
   C --> D["story-continuity-auditor<br/>설정 일관성 검수"]
   D --> E["산출물<br/>(에피소드·콘티·작화)"]
```

## 스킬 카탈로그

story-* 계열 창작 스킬의 전체 목록입니다.

{{< employee-skills "moai-story" >}}

## 에이전트

**story-director**(실행 코워커)가 장르 파이프라인을 설계하고 기획·원고·콘티·작화를 이끌고, **story-continuity-auditor**(검수 코워커)가 캐릭터·시점·사건의 설정 일관성을 검수합니다.

{{< employee-agents "moai-story" >}}

## 대표 시나리오 3선

**1. 웹툰 에피소드 생성.** "로맨스 웹툰 1화 기획하고 콘티까지 만들어줘"라고 하면 `story-webtoon-planner`·`story-synopsis`로 에피소드를 설계하고 `story-conti`·`story-webtoon-art`로 콘티와 작화를 생성합니다. 한 회차가 지나는 파이프라인은 아래 흐름처럼 여러 스킬이 줄줄이 이어집니다. `story-series-bible`은 회차를 관통해 설정을 묶는 원장이고, `story-webtoon-spec`이 플랫폼별 칸 수·분할 규격을 깔아 줍니다.

```mermaid
flowchart TD
   WS["story-webtoon-spec<br/>플랫폼 사양(칸 수·분할)"] --> P
   SB["story-series-bible<br/>연재 설정 원장"] -. 설정 참조 .-> P
   P["story-webtoon-planner<br/>에피소드 기획"] --> E["story-webtoon-episode<br/>컷 대본"]
   SB -. 설정 참조 .-> E
   E --> L["story-webtoon-lettering<br/>대사·효과음 배치"]
   L --> ART["story-webtoon-art<br/>작화 프롬프트 조립"]
   ART --> QC["story-webtoon-qc<br/>연재 품질 검수"]
   QC -. 회차 누적 .-> SB
   ART -->|생성 위임| MM["moai-media<br/>Higgsfield MCP 구동"]
   classDef green fill:#e8f1ec,stroke:#3d7d5f,color:#265240
   classDef ledger fill:#d6e7de,stroke:#265240,color:#265240
   classDef media fill:#e6e6e6,stroke:#757575,color:#333
   class P,E,L,ART,QC green
   class SB,WS ledger
   class MM media
```

**2. 캐릭터 시트 + 시네마틱 프리비즈.** "주인공 캐릭터 시트랑 30초 티저 프리비즈 만들어줘"라고 하면 `story-character-sheet`와 `story-previz`가 Higgsfield MCP로 일관된 캐릭터 작화와 프리비즈를 만듭니다.

**3. 웹소설 연재.** "이 설정으로 웹소설 3회분 원고 써줘"라고 하면 `story-webnovel-writer`가 연재 원고를 작성합니다.

**잘 안 될 때** — 작화·프리비즈 생성 실패 시 프롬프트 온리 폴백으로 전환합니다. Higgsfield OAuth는 [설정 가이드](/plugins/higgsfield-setup/)를 참고하세요.

## MCP 연동

- **higgsfield** — 캐릭터 작화·콘티·표지·시네마틱 프리비즈 생성. Higgsfield OAuth 인증이 필요합니다 ([설정 가이드](/plugins/higgsfield-setup/)).
