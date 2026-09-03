---
title: "API 키 넣는 법"
weight: 15
description: "외부 서비스 연동에 필요한 API 키를 넣는 두 가지 방법 — 앱 입력창과 자격증명 파일. 네 실행 환경 어디에서든 같게 동작합니다."
geekdocBreadcrumb: true
date: 2026-09-03T00:00:00+09:00
lastmod: 2026-09-03T00:00:00+09:00
---

스마트스토어·카페24·DART처럼 **외부 서비스에 직접 접속하는 코워커**는 그 서비스의 API 키가 있어야 실제로 일합니다. 이 페이지는 그 키를 넣는 방법을 다룹니다.

키가 없어도 코워커의 일반 스킬(상세페이지 작성, 캠페인 기획 등)은 그대로 쓸 수 있습니다. 연동 도구를 쓰려는 시점에 넣으면 됩니다.

## 방법 1 — 앱 입력창 (Claude Cowork)

Claude Cowork 앱은 키가 필요한 코워커를 켤 때 **입력 폼을 띄웁니다**. 항목을 채우면 앱이 알아서 안전한 곳(맥 키체인 등)에 보관하고, 코워커가 일할 때 꺼내 씁니다.

- 나중에 바꾸려면 코워커의 설정 화면에서 다시 입력하면 됩니다.
- 비밀 항목은 입력할 때 가려지고, 채팅 기록에도 남지 않습니다.

가장 간편한 길이므로 Claude Cowork를 쓴다면 이 방법을 먼저 쓰세요.

## 방법 2 — 자격증명 파일 (양쪽 앱 공통)

ChatGPT Work 앱에는 아직 이런 입력 폼이 없습니다. 그래서 코워커들은 **파일에서도 키를 읽도록** 만들어져 있습니다.

키를 넣을 곳은 서비스마다 하나씩입니다.

```
~/.moai/mcp/<서비스이름>.json
```

Windows에서는 `C:\Users\사용자이름\.moai\mcp\<서비스이름>.json`입니다.

파일 내용은 **항목 이름과 값을 짝지은 목록** 하나뿐입니다. 예를 들어 DART(전자공시) 키는 이렇게 적습니다.

```json
{
  "DART_API_KEY": "여기에_발급받은_키"
}
```

스마트스토어처럼 항목이 여러 개인 서비스는 이렇게 이어 적습니다.

```json
{
  "NAVER_COMMERCE_CLIENT_ID": "애플리케이션 ID",
  "NAVER_COMMERCE_CLIENT_SECRET": "애플리케이션 시크릿",
  "NAVER_COMMERCE_TYPE": "SELF"
}
```

**직접 만들지 않아도 됩니다.** 코워커에게 "DART 키 넣어 줘" 하고 키를 알려 주면 이 파일을 대신 만들어 줍니다. 손으로 만들고 싶을 때를 위해 형식을 적어 둔 것입니다.

### 서비스 이름과 항목

| 코워커 | 서비스 이름(파일명) | 항목 |
|---|---|---|
| `moai-accountant` · `moai-analyst` · `moai-coworker` | `dart` | `DART_API_KEY` |
| `moai-media` | `elevenlabs` | `ELEVENLABS_API_KEY` |
| `moai-seller` (스마트스토어) | `smartstore` | `NAVER_COMMERCE_CLIENT_ID` · `NAVER_COMMERCE_CLIENT_SECRET` · `NAVER_COMMERCE_ACCOUNT_ID` · `NAVER_COMMERCE_TYPE` |
| `moai-seller` (아임웹) | `imweb` | `IMWEB_CLIENT_ID` · `IMWEB_CLIENT_SECRET` · `IMWEB_ACCESS_TOKEN` · `IMWEB_REFRESH_TOKEN` · `IMWEB_UNIT_CODE` |
| `moai-seller` (카페24) | `cafe24` | `CAFE24_MALL_ID` · `CAFE24_CLIENT_ID` · `CAFE24_CLIENT_SECRET` · `CAFE24_ACCESS_TOKEN` · `CAFE24_REFRESH_TOKEN` |
| `moai-threads-poster` | `threads` | `THREADS_ACCESS_TOKEN` · `THREADS_USER_ID` · `IG_ACCESS_TOKEN` · `IG_USER_ID` |

`moai-lawyer`(국가법령정보)는 방법 1만 지원합니다 — 키가 접속 주소 안에 들어가는 구조라 파일로는 대신할 수 없습니다.

Higgsfield·Meta Ads·Slack·WordPress·Typefully처럼 **로그인 방식(OAuth)** 인 서비스는 이 페이지와 무관합니다. 처음 쓸 때 브라우저 로그인 창이 뜨고, 키를 적을 일이 없습니다.

## 두 방법을 같이 써도 되나요

됩니다. 코워커는 **앱 입력창에 값이 있으면 그것을 먼저** 쓰고, 없을 때 파일을 봅니다. 그래서 Claude에서는 입력창으로, ChatGPT Work에서는 파일로 — 같은 컴퓨터에서 둘 다 채워 두면 어느 앱에서든 그대로 일합니다.

## 안전하게 다루기

- **API 키는 비밀번호와 같습니다.** 채팅창에 그대로 붙여 넣지 말고, 앱 입력창(가려집니다)이나 파일로만 넘기세요.
- 파일은 본인 계정의 홈 폴더 안에 있으며, 다른 사람과 공유되는 위치가 아닙니다.
- 키가 유출된 것 같으면 발급처(개발자센터)에서 **키를 폐기하고 새로 발급**받으세요. 파일만 지우는 것으로는 부족합니다.
- 키를 저장소(GitHub 등)에 올리지 마세요.

## 잘 안 될 때

**"자격증명이 설정되지 않았습니다"라고 나옵니다** — 항목 이름의 철자를 확인하세요. 위 표의 이름과 한 글자라도 다르면 못 읽습니다.

**키를 넣었는데도 인증에 실패합니다** — 발급처에서 키가 아직 살아 있는지, 필요한 권한(스코프)이 켜져 있는지 확인하세요. 스마트스토어·카페24는 서비스 쪽에서 별도 사용 신청이 필요한 기능이 있습니다.

**앱을 다시 켜야 하나요** — 네. 키를 새로 넣었으면 대화를 새로 시작하세요. 코워커는 일을 시작할 때 한 번 키를 읽습니다.

더 자세한 진단은 [연동이 안 될 때](../troubleshooting/)를 보세요.
