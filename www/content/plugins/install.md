---
title: "설치와 관리"
weight: 10
description: "마켓플레이스 등록 → 필요한 직원 설치 → 확인 → 업데이트·비활성화·제거, 그리고 MCP 자격증명 준비까지 따라 하기."
geekdocBreadcrumb: true
---

플러그인 설치는 크게 두 단계입니다. 먼저 **마켓플레이스를 한 번 등록**하고(어느 가게에서 물건을 받아올지 Claude에게 알려 주는 일), 그다음 **필요한 직원 플러그인만 골라 설치**합니다. 마켓플레이스 등록은 컴퓨터당 한 번이면 되고 이후에는 설치·업데이트·제거만 반복하면 됩니다.

이 페이지의 명령어는 모두 터미널(macOS의 "터미널" 앱, Windows의 PowerShell)에서 입력합니다. Claude Code가 이미 설치되어 있다는 전제로 진행합니다 — 아직이라면 [CLI 시작하기](/cli/start/)를 먼저 보고 오세요. Claude Desktop 앱을 쓰는 분도 같은 마켓플레이스를 앱의 플러그인 설정 화면에서 등록할 수 있으므로 아래 흐름을 그대로 참고하면 됩니다.

## 1. 마켓플레이스 등록

터미널에 아래 한 줄을 입력합니다.

```bash
claude plugin marketplace add modu-ai/moai-cowork
```

`modu-ai/moai-cowork`는 GitHub 저장소 주소의 줄임 표기입니다. 성공하면 "Added marketplace: moai-cowork" 같은 확인 메시지가 출력되고, 이제 Claude가 이 가게의 플러그인 목록을 알게 됩니다. 등록된 마켓플레이스는 다음 명령으로 확인할 수 있습니다.

```bash
claude plugin marketplace list
```

출력에 `moai-cowork`라는 이름과 플러그인 개수(18개)가 보이면 정상입니다.

{{< screenshot-request "터미널에서 claude plugin marketplace add modu-ai/moai-cowork 실행 후 성공 메시지와 marketplace list 출력이 보이는 화면" >}}

> **잘 안 될 때** — "command not found: claude"가 나오면 Claude Code 자체가 설치되지 않았거나 PATH에 없는 상태입니다. [CLI 설치 안내](/cli/start/)를 따라 Claude Code부터 설치하세요. 네트워크 오류가 나오면 GitHub 접속이 가능한 환경인지(회사 프록시 등) 확인하세요.

Claude Desktop 앱에서는 설정 → 플러그인(Plugins) 화면에서 마켓플레이스 주소로 `modu-ai/moai-cowork`를 추가하면 같은 결과를 얻습니다.

{{< screenshot-request "Claude Desktop 앱의 설정 > 플러그인 화면 — 마켓플레이스 추가 입력란과 등록된 moai-cowork 마켓플레이스가 보이는 화면" >}}

## 2. 필요한 직원만 설치

18개를 전부 설치할 필요는 없습니다. 지금 필요한 직무만 골라 설치하세요. 설치 명령의 형식은 `<플러그인 이름>@<마켓플레이스 이름>`입니다.

```bash
# 예: 마케터 채용
claude plugin install moai-marketer@moai-cowork

# 예: 이커머스 셀러 채용
claude plugin install moai-seller@moai-cowork

# 예: 실무 범용 코워커 채용
claude plugin install moai-coworker@moai-cowork
```

각 명령이 성공하면 "Installed plugin: moai-marketer" 형태의 메시지가 출력됩니다. 어떤 직원이 있는지는 [플러그인 설치·운용 개요](../)의 17-직원 표를, 각 직원이 무엇을 하는지는 [에이전트 팀 소개](/moai-agents/)를 참고하세요.

> **잘 안 될 때** — "Plugin not found"가 나오면 이름 철자(`moai-` 접두사 포함)와 `@moai-cowork` 접미사를 확인하세요. 마켓플레이스 등록(1단계)을 건너뛴 경우에도 같은 오류가 납니다.

## 3. 설치 확인

설치가 실제로 반영됐는지 두 가지 명령으로 확인합니다.

```bash
claude plugin list
```

설치된 플러그인 이름·버전·활성 상태가 표 형태로 출력됩니다. 방금 설치한 직원이 `enabled` 상태로 보이면 성공입니다.

```bash
claude plugin details moai-seller@moai-cowork
```

`details`는 특정 플러그인의 상세 정보 — 버전, 설명, 포함된 명령·에이전트·스킬 목록, MCP 서버 선언 — 를 보여 줍니다. 설치 직후 한 번 훑어보면 이 직원이 어떤 도구를 들고 왔는지 감이 잡힙니다.

{{< screenshot-request "claude plugin details moai-seller@moai-cowork 실행 결과 — 버전·스킬·MCP 서버 목록이 출력된 터미널 화면" >}}

> **잘 안 될 때** — `list`에 플러그인이 보이는데 Claude Code 세션 안에서 스킬이 동작하지 않으면, 실행 중이던 세션을 종료하고 새로 시작해 보세요. 플러그인은 세션 시작 시점에 로드됩니다.

## 4. 업데이트·비활성화·제거

플러그인은 마켓플레이스에서 계속 개선됩니다. 관리 명령 세 가지만 기억하면 됩니다.

```bash
# 마켓플레이스 최신 정보 받아오기 + 플러그인 업데이트
claude plugin marketplace update moai-cowork
claude plugin update moai-seller@moai-cowork

# 잠시 쉬게 하기(삭제 없이 비활성화) / 다시 출근시키기
claude plugin disable moai-seller@moai-cowork
claude plugin enable moai-seller@moai-cowork

# 완전히 내보내기(제거)
claude plugin uninstall moai-seller@moai-cowork
```

비활성화(`disable`)는 설치는 유지한 채 로드만 막는 것이라, 여러 직원을 설치해 두고 프로젝트에 따라 켜고 끄는 운용에 좋습니다. 제거(`uninstall`) 후에도 마켓플레이스 등록은 남아 있으므로 언제든 다시 설치할 수 있습니다.

> **잘 안 될 때** — 업데이트 후 동작이 이상하면 `claude plugin details`로 버전이 실제로 올라갔는지 확인하고, 세션을 재시작하세요. 문제가 계속되면 `uninstall` 후 재설치가 가장 확실한 초기화입니다.

## 5. MCP 자격증명 준비 (외부 서비스 연동 직원)

일부 직원은 외부 서비스에 직접 접속해 일합니다. 이런 연동을 **MCP**(Model Context Protocol — Claude가 외부 서비스의 도구를 표준 방식으로 부르는 규약)라고 부르는데 외부 서비스 계정의 **API 자격증명**(아이디·비밀키 등)을 환경변수로 준비해 줘야 실제로 동작합니다.

| 직원 | 연동 서비스 | 준비물 |
|------|------------|--------|
| `moai-seller` | 네이버 스마트스토어 | 커머스API센터 애플리케이션 ID·시크릿 등 환경변수 |
| `moai-seller` | 카페24 | 개발자센터 앱 클라이언트 ID·시크릿 등 환경변수 |
| `moai-seller` | 아임웹 | OPEN API 키 발급 후 환경변수 |
| `moai-marketer` | Meta Ads | Meta 비즈니스 계정 인증 |
| `moai-marketer` | 게시 채널(post-bridge·typefully·wordpress) | 각 서비스 계정 연결 |
| `moai-media` | Higgsfield·ElevenLabs | Higgsfield OAuth([설정 가이드](higgsfield-setup/))·ElevenLabs API 키 |
| `moai-story` | Higgsfield | Higgsfield OAuth([설정 가이드](higgsfield-setup/)) |
| `moai-designer` | Higgsfield | Higgsfield OAuth([설정 가이드](higgsfield-setup/)) |
| `moai-analyst` | KOSIS·DART·공공데이터포털 | 각 공공 API 키 환경변수 |
| `moai-lawyer` | 국가법령정보 | 공공 API 키 환경변수 |
| `moai-officer` | kordoc | 로컬 처리(별도 자격증명 없음) |

자격증명이 없어도 플러그인의 일반 스킬(상세페이지 작성, 캠페인 기획 등)은 그대로 쓸 수 있습니다. 연동 도구를 쓰려는 시점에 해당 서비스의 개발자센터에서 키를 발급받아 환경변수로 넣어 주면 됩니다 — 구체적인 변수 이름과 발급 절차는 각 플러그인의 `details` 출력과 직원별 문서를 참고하세요. **API 키는 비밀번호와 같습니다.** 채팅창이나 문서에 붙여 넣지 말고, 환경변수나 셸 설정 파일로만 관리하세요.

## 다음 단계

설치가 끝났다면, 이 직원들이 실제로 어떻게 일하는지 — 일하는 에이전트와 검수하는 에이전트가 왜 나뉘어 있는지 — 를 [전문가 에이전트 이해](../agents/)에서 이어서 읽으세요.

---

### Sources

- Claude Code 플러그인 공식 문서: <https://code.claude.com/docs/en/plugins>
- 마켓플레이스 진실 원본: [`/.claude-plugin/marketplace.json`](https://github.com/modu-ai/moai-cowork/blob/main/.claude-plugin/marketplace.json)
