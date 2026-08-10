---
title: "설치와 관리"
weight: 10
description: "마켓플레이스 등록 → 필요한 코워커 설치 → 확인 → 업데이트·비활성화·제거, 그리고 MCP 자격증명 준비까지 따라 하기."
geekdocBreadcrumb: true
date: 2026-08-07T00:00:00+09:00
lastmod: 2026-08-10T00:00:00+09:00
---

플러그인 설치는 크게 두 단계입니다. 먼저 **마켓플레이스를 한 번 등록**하고(어느 가게에서 물건을 받아올지 Claude 또는 ChatGPT에게 알려 주는 일), 그다음 **필요한 코워커 플러그인만 골라 설치**합니다. 마켓플레이스 등록은 컴퓨터당 한 번이면 되고 이후에는 설치·업데이트·제거만 반복하면 됩니다.

이 페이지는 **Claude Cowork 또는 ChatGPT Work 데스크톱 앱**을 쓴다는 전제로 안내합니다. 두 앱이 같은 마켓플레이스를 공유하므로, 어느 쪽이든 편한 앱으로 등록하면 됩니다. 모든 단계는 앱 안에서 마우스 클릭으로 진행합니다 — 터미널은 필요하지 않습니다.

## 1. 마켓플레이스 등록

### Claude Cowork 앱에서 등록

Claude Cowork 앱의 설정(또는 플러그인) 화면에서 마켓플레이스 주소를 추가합니다.

1. 앱을 열고 **Settings** (또는 **Plugins**) 메뉴로 이동
2. **Marketplace** 섹션에서 **+** 로 저장소를 추가하고 `modu-ai/moai-cowork` 입력 후 **Add**

{{< screenshot-request "Claude Cowork 앱의 설정(또는 플러그인) 화면 — 마켓플레이스에서 + 로 저장소를 추가하고 modu-ai/moai-cowork를 입력해 추가 버튼을 누르는 화면" >}}

등록이 완료되면 **moai-cowork** 마켓플레이스가 목록에 보이고, 이제 이 가게의 플러그인 목록을 앱에서 볼 수 있습니다.

### ChatGPT Work 앱에서 등록

ChatGPT Work 앱(데스크톱)에서도 같은 마켓플레이스를 등록할 수 있습니다.

1. Work 모드로 진입
2. **Plugins** 메뉴 열기
3. **Marketplace**에서 **+** 로 저장소를 추가하고 `modu-ai/moai-cowork` 입력

{{< screenshot-request "ChatGPT Work 앱, Work 모드 → Plugins 메뉴 — 마켓플레이스에서 + 로 저장소를 추가하고 modu-ai/moai-cowork를 입력하는 화면" >}}

`modu-ai/moai-cowork`는 GitHub 저장소 주소의 줄임 표기입니다. 추가가 끝나면 이제 해당 앱이 이 가게의 플러그인 목록을 알게 됩니다.

> **잘 안 될 때** — 추가 후 목록이 비어 있다면 앱을 껐다가 다시 켜보세요. 네트워크 오류가 나오면 GitHub 접속이 가능한 환경인지 (회사 프록시 등) 확인하세요.

## 2. 코워커 설치

### 앱 UI에서 설치

마켓플레이스 등록 후에는 Plugins 화면에서 코워커를 선택하고 설치할 수 있습니다.

1. **Plugins** 메뉴 열기
2. **moai-cowork** 마켓플레이스에서 원하는 코워커 선택 (예: `moai-marketer`, `moai-seller`, `moai-coworker`)
3. **+** 또는 **Install** 선택

{{< screenshot-request "Claude Cowork 또는 ChatGPT Work 앱의 Plugins 화면 — moai-cowork 마켓플레이스의 코워커 목록에서 moai-marketer를 선택하고 + 버튼을 누르는 화면" >}}

전부 설치할 필요는 없습니다. 지금 필요한 직무만 골라 설치하세요. 어떤 코워커가 있는지는 [플러그인 설치·운용 개요](../)의 코워커 표를, 각 코워커가 무엇을 하는지는 [에이전트 팀 소개](/moai-agents/)를 참고하세요.

> **추천 설치 순서** — 먼저 `moai-pm` (진입 허브) 과 `moai-coworker` (범용 실무 코어) 를 설치한 뒤, 진행할 작업에 맞는 직무 코워커를 추가하세요. 설치 직후 목록에 보이지 않으면 앱을 재시작해 보세요. 마켓플레이스 등록 (1단계) 을 건너뛴 경우에도 코워커가 보이지 않습니다.

## 3. 설치 확인

### 앱 UI에서 확인

Plugins 화면에서 설치된 코워커 목록을 확인할 수 있습니다. 방금 설치한 코워커가 **enabled** (활성화) 상태로 보이면 성공입니다. 코워커 카드를 누르면 버전·포함된 스킬·MCP 서버 등 상세 정보도 함께 볼 수 있습니다.

{{< screenshot-request "앱의 Plugins 화면 — 설치된 코워커 목록에서 moai-seller가 enabled 상태로 보이고, 카드를 눌러 버전·스킬·MCP 서버 상세 정보가 펼쳐진 화면" >}}

> **잘 안 될 때** — Plugins 화면에 코워커가 보이는데 Claude Cowork 또는 ChatGPT Work 세션 안에서 스킬이 동작하지 않으면, 실행 중이던 세션을 종료하고 새로 시작해 보세요. 플러그인은 세션 시작 시점에 로드됩니다.

## 4. 업데이트·비활성화·제거

### 앱 UI에서 관리

Plugins 화면에서 각 코워커별로 업데이트·비활성화·제거를 할 수 있습니다.

- **업데이트**: 코워커 카드의 **Update** 버튼
- **비활성화/활성화**: **Enable/Disable** 토글
- **제거**: **Remove** 버튼

{{< screenshot-request "앱의 Plugins 화면 — 설치된 코워커 카드에서 Update/Disable/Remove 버튼이 보이는 화면" >}}

비활성화는 설치를 유지한 채 로드만 막는 것이라, 여러 코워커를 설치해 두고 프로젝트에 따라 켜고 끄는 운용에 좋습니다. 제거 후에도 마켓플레이스 등록은 남아 있으므로 언제든 다시 설치할 수 있습니다.

> **잘 안 될 때** — 업데이트 후 동작이 이상하면 앱에서 버전이 실제로 올라갔는지 확인하고, 세션을 재시작하세요. 문제가 계속되면 제거 후 재설치가 가장 확실한 초기화입니다.

## 5. MCP 자격증명 준비 (외부 서비스 연동 코워커)

일부 코워커는 외부 서비스에 직접 접속해 일합니다. 이런 연동을 **MCP** (Model Context Protocol — Claude가 외부 서비스의 도구를 표준 방식으로 부르는 규약) 라고 부르는데, 외부 서비스 계정의 **API 자격증명** (아이디·비밀키 등) 을 환경변수로 준비해 줘야 실제로 동작합니다.

| 코워커 | 연동 서비스 | 준비물 |
|------|------------|--------|
| `moai-seller` | 네이버 스마트스토어 | 커머스API센터 애플리케이션 ID·시크릿 등 환경변수 |
| `moai-seller` | 카페24 | 개발자센터 앱 클라이언트 ID·시크릿 등 환경변수 |
| `moai-seller` | 아임웹 | OPEN API 키 발급 후 환경변수 |
| `moai-marketer` | Meta Ads | Meta 비즈니스 계정 인증 |
| `moai-marketer` | 게시 채널 (post-bridge·typefully·wordpress) | 각 서비스 계정 연결 |
| `moai-media` | Higgsfield·ElevenLabs | Higgsfield OAuth ([설정 가이드](higgsfield-setup/))·ElevenLabs API 키 |
| `moai-story` | Higgsfield | Higgsfield OAuth ([설정 가이드](higgsfield-setup/)) |
| `moai-designer` | Higgsfield | Higgsfield OAuth ([설정 가이드](higgsfield-setup/)) |
| `moai-analyst` | KOSIS·DART·공공데이터포털 | 각 공공 API 키 환경변수 |
| `moai-lawyer` | 국가법령정보 | 공공 API 키 환경변수 |
| `moai-officer` | kordoc | 로컬 처리 (별도 자격증명 없음) |

자격증명이 없어도 플러그인의 일반 스킬 (상세페이지 작성, 캠페인 기획 등) 은 그대로 쓸 수 있습니다. 연동 도구를 쓰려는 시점에 해당 서비스의 개발자센터에서 키를 발급받아 환경변수로 넣어 주면 됩니다 — 구체적인 변수 이름과 발급 절차는 각 코워커 카드의 상세 정보와 코워커별 문서를 참고하세요. **API 키는 비밀번호와 같습니다.** 채팅창이나 문서에 붙여 넣지 말고, 환경변수나 셸 설정 파일로만 관리하세요.

## 다음 단계

설치가 끝났다면, 이 코워커들이 실제로 어떻게 일하는지 — 일하는 에이전트와 검수하는 에이전트가 왜 나뉘어 있는지 — 를 [전문가 에이전트 이해](../agents/)에서 이어서 읽으세요.

---

### Sources

- Claude Code 플러그인 공식 문서: <https://code.claude.com/docs/en/plugins>
- OpenAI 플러그인 빌드 가이드: <https://developers.openai.com/plugins/build/plugins>
- OpenAI 플러그인 사용 가이드: <https://learn.chatgpt.com/docs/plugins?surface=app>
- OpenAI 서브에이전트 설정: <https://learn.chatgpt.com/docs/agent-configuration/subagents>
- 마켓플레이스 진실 원본: [`/.claude-plugin/marketplace.json`](https://github.com/modu-ai/moai-cowork/blob/main/.claude-plugin/marketplace.json)
