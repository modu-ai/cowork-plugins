# 🎥 유튜버 (moai-youtuber)

유튜브 **채널 운영 전담** AI 코워커입니다. 라이브 방송을 켜고 끄는 일, 녹화본을 편집자에게
넘기는 일, 올리고 검색에 걸리게 만드는 일, 성과를 읽고 다음을 정하는 일, 댓글을 감당하는 일
— 채널을 굴리는 데 실제로 시간이 드는 작업을 맡습니다.

## 이 직원이 하지 않는 일

경계를 명확히 해 두었습니다. 겹치는 스킬을 만들지 않는 것이 이 패밀리의 원칙입니다.

| 필요한 일 | 담당 |
|---|---|
| 영상 한 편의 기획서·대본 | `moai-marketer:marketing-youtube-podcast-planner` |
| 처음부터 쓰는 숏폼 대본 | `moai-marketer:content-sns-content` |
| 썸네일 이미지·B롤·내레이션 **생성** | `moai-media` |
| 채널 브랜드 색·서체 규칙 | `moai-designer:design-brand-system` |
| 고객 문의·클레임 응대 체계 | `moai-cs` |
| 저작권 분쟁·법적 대응 | `moai-lawyer` |

## 스킬

| 스킬 | 하는 일 |
|---|---|
| `youtube-channel-ops` | 업로드 리듬·시리즈 포트폴리오·분기 목표 — 계속 낼 수 있는 구조 |
| `youtube-live-ops` | 라이브 방송 전 점검 · 큐시트 · 실시간 채팅 · 종료 후 다시보기 정리 |
| `youtube-production` | 촬영 세팅 점검 · 확보할 컷 목록 · 편집 지시서 |
| `youtube-thumbnail-title` | 제목과 썸네일을 한 묶음으로 설계 |
| `youtube-publish-ops` | 업로드 · 설명란 · 챕터 · 재생목록 · 자막 · 예약 발행 |
| `youtube-analytics-review` | 어느 단계에서 새는지 특정 → 다음 액션 하나 |
| `youtube-community-cs` | 댓글 분류 · 답글 초안 · 고정 댓글 · 커뮤니티 탭 |
| `youtube-shorts-repurpose` | 롱폼·라이브 다시보기에서 쇼츠 뽑기 |

## 대표 작업 흐름

```
채널 운영 체계 (youtube-channel-ops)
   ↓
편별 기획·대본 (moai-marketer)
   ↓
   ├─ 라이브 ─→ youtube-live-ops ─────────────┐
   └─ 녹화  ─→ youtube-production ────────────┤
                (인서트·효과음은 moai-media)   │
                                              ↓
                            youtube-thumbnail-title
                                              ↓
                              youtube-publish-ops
                                              ↓
                          youtube-analytics-review
                                              ↓
              youtube-community-cs · youtube-shorts-repurpose
```

`/project`로 프로젝트를 초기화하면 이 흐름이 프로젝트 맥락에 맞게 재설계되어
`CLAUDE.md` 워크플로우 표에 배선됩니다.

## MCP 연동 — `moai-youtube`

유튜브에는 Google이 관리하는 공식 MCP 서버가 없습니다. 그래서 YouTube Data API v3 +
Live Streaming API + Analytics API를 감싼 **자체 MCP 서버**를 함께 넣었습니다.

| 묶음 | 할 수 있는 일 |
|---|---|
| 라이브 | 방송 생성 · 스트림 연결 · 상태 전환 · 실시간 채팅 읽기/쓰기/관리 |
| 발행 | 업로드 · 메타데이터 · 썸네일 · 재생목록 · 자막 · 공개 예약 |
| 분석 | 채널·영상 지표 · 유입 경로 · 시청 유지 곡선 |
| 커뮤니티 | 댓글 조회 · 답글 · 숨김 처리 |

**할당량 방어가 들어 있습니다.** 유튜브 API는 하루 10,000 units인데 검색이 1회 100 units라
가장 빨리 한도를 태웁니다. 그래서 검색은 캐시를 강제하고, 내 영상 목록은 검색 대신 업로드
재생목록(2 units)으로 받습니다. 모든 응답에 잔량 추정치가 함께 담깁니다.

설정 방법은 [`mcp-servers/moai-mcp-youtube/CONNECTORS.md`](mcp-servers/moai-mcp-youtube/CONNECTORS.md),
서버 상세는 [`mcp-servers/moai-mcp-youtube/README.md`](mcp-servers/moai-mcp-youtube/README.md)를 보세요.

**연결하지 않아도 스킬은 작동합니다.** 자격증명이 없으면 각 도구가 설정 안내를 돌려주고,
점검표·큐시트·편집 지시서·설명란 원고·답글 초안까지는 그대로 만들어 드립니다. 실제 버튼을
누르는 단계는 유튜브 스튜디오에서 하실 수 있도록 순서를 안내합니다. 하지 않은 일을 했다고
보고하지 않습니다.

## 어디서 쓸 수 있나

macOS와 Windows, Claude Cowork(Desktop)와 ChatGPT Work(Codex) — 네 조합 모두에서 동일하게
동작합니다. Claude용 `.claude-plugin/plugin.json`과 Codex용 `.codex-plugin/plugin.json`을
쌍으로 두고, 스킬 본문은 양쪽이 공유합니다.

## 설치

`.claude-plugin/marketplace.json` 에 등록돼 있습니다. Claude Code에서 `/plugin` 명령으로
`moai-cowork` 마켓플레이스를 추가한 뒤 이 플러그인을 활성화하세요.

## 라이선스

Apache-2.0. 이 플러그인으로 만든 산출물의 권리는 전적으로 사용자에게 있습니다.
