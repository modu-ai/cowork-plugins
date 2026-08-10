---
title: "대화 관리"
weight: 40
description: "대화 삭제·이름변경·공유, 시크릿 대화, 그리고 검색과 메모리로 이전 맥락을 이어가는 방법을 정리했어요."
geekdocBreadcrumb: true
date: 2026-08-07T00:00:00+09:00
lastmod: 2026-08-10T00:00:00+09:00
---

Claude와 대화를 나누다 보면 채팅 목록이 점점 쌓입니다. 책상 위에 메모지가 늘어나는 것과 비슷해요. 어떤 메모는 잘 보이게 이름을 붙여 두고 싶고, 어떤 건 정리해서 버리고 싶고, 또 어떤 건 동료에게 그대로 보여 주고 싶죠.

이 글에서는 대화를 깔끔하게 관리하는 법을 다룹니다. 대화 이름 바꾸기와 삭제, 다른 사람과 공유하기, 기록을 남기지 않는 시크릿(Incognito) 대화, 그리고 Claude가 지난 대화를 기억하고 검색하도록 돕는 방법까지 차례대로 살펴볼게요.

## 대화 이름 바꾸기와 삭제하기

대화는 자동으로 제목이 붙지만 직접 알아보기 쉬운 이름으로 바꾸거나 더 이상 필요 없는 대화를 지울 수 있습니다. 이 기능은 Claude Free와 Claude Pro에서 사용할 수 있어요.

### 하나씩 이름 바꾸거나 삭제하기

1. 관리하고 싶은 대화로 이동합니다.
2. 화면 위쪽의 **대화 이름**을 클릭합니다.
3. 표시되는 메뉴에서 **이름 바꾸기(Rename)** 또는 <strong>삭제(Delete)</strong>를 선택합니다.

### 여러 대화를 한 번에 삭제하기

대화가 많이 쌓였다면 사이드바에서 여러 개를 골라 한꺼번에 지울 수 있습니다.

1. 왼쪽 사이드바의 **Chats**(채팅 목록)로 이동합니다.
2. 삭제할 대화 위에 마우스를 올리면 나타나는 **선택 체크박스**를 클릭합니다.
3. 지우려는 대화를 모두 체크합니다.
4. **Delete Selected**(선택 항목 삭제) 버튼을 눌러 삭제를 확정합니다.

{{< hint type="note" >}}
여기서 안내하는 방법은 Claude Free와 Claude Pro 기준이에요. Claude for Work나 Claude API에서는 절차가 다를 수 있습니다.
{{< /hint >}}

## 대화 공유하기

마음에 드는 답변이나 작업 결과를 다른 사람에게 보여 주고 싶을 때, 링크 하나로 대화를 공유할 수 있습니다. 모든 대화는 기본적으로 비공개이고 공유는 직접 켜야만 작동해요.

### 공유 링크 만들기

1. 채팅 화면 **오른쪽 위의 공유(Share) 버튼**을 클릭합니다.
2. 팝업 메뉴에서 **Share**를 눌러 공유 가능한 링크를 만듭니다.

### 공유 해제하기

1. 다시 **Share 메뉴**로 들어갑니다.
2. **공개 범위(Visibility) 드롭다운**을 엽니다.
3. <strong>Public(공개)</strong>에서 <strong>Private(비공개)</strong>로 바꾸면 링크가 비활성화됩니다.

### 공유한 대화 한곳에서 관리하기

공유한 대화의 제목, 날짜, 링크를 한 화면에서 확인하고 개별적으로 접근을 취소할 수 있습니다.

1. <strong>Settings(설정) > Privacy(개인정보)</strong>로 이동합니다.
2. **Shared chats**(공유된 대화) 항목에서 **Manage**(관리)를 클릭합니다.
3. 목록을 살펴보고 필요 없는 공유 링크의 접근을 취소합니다.

공유에는 알아 두면 좋은 점이 몇 가지 있어요.

| 항목 | 동작 방식 |
|---|---|
| 공유 시점 | 공유한 순간의 대화 내용이 그대로 캡처됩니다(스냅샷). |
| 이후 메시지 | 공유한 뒤에 주고받은 메시지는 다시 공유하기 전까지 포함되지 않습니다. |
| 첨부 파일 | 공유 스냅샷에 포함되지 않고 비공개로 남습니다. |
| MCP 도구 호출 데이터 | 원본 데이터는 공유 스냅샷에서 숨겨집니다. |

### 요금제별 공유 범위

| 요금제 | 공유 범위 |
|---|---|
| Free · Pro · Max | 누구나 볼 수 있도록 **공개 공유** 가능 |
| Team · Enterprise | **같은 조직 구성원에게만** 공유 가능(공개 공유 불가) |

{{< hint type="warning" >}}
새 메시지를 주고받았다면 공유 링크는 자동으로 갱신되지 않아요. 최신 내용을 보여 주려면 대화를 **다시 공유**해야 합니다.
{{< /hint >}}

## 기록을 남기지 않는 시크릿 대화

남에게 보여 주고 싶지 않거나 기록으로 남기고 싶지 않은 대화가 있죠. 시크릿(Incognito) 대화는 채팅 기록에 저장되지 않고 모델 학습에도 사용되지 않는 일시적인 대화입니다.

### 시크릿 대화 시작하기

1. 프로젝트 밖에서 **새 대화**를 시작합니다.
2. 오른쪽 위의 **유령(ghost) 아이콘**을 클릭해 시크릿 모드를 켭니다.
3. 화면 왼쪽 위에 **검은 테두리**와 **'Incognito chat'** 라벨이 보이면 켜진 거예요.
4. 평소처럼 대화하면 됩니다. 기록에 저장되거나 학습에 쓰이지 않아요.

### 알아 둘 점

| 항목 | 내용 |
|---|---|
| 저장 여부 | 채팅 기록에 저장되지 않고 검색도 되지 않습니다. |
| 학습 사용 | 모든 요금제(Free·Pro·Max·Team·Enterprise)에서 모델 학습에 쓰이지 않습니다. |
| 메모리 | 시크릿 대화에서는 Claude의 메모리 기능이 작동하지 않습니다. |
| 보관 | 채팅 기록·메모리에 저장되지 않는 임시 대화이며, 한 번 닫으면 다시 열 수 없습니다(Enterprise는 조직 정책에 따름). |
| 사용 범위 | 단독 대화에서만 쓸 수 있고, 프로젝트 안에서는 사용할 수 없습니다. |

{{< hint type="warning" >}}
시크릿 대화는 한 번 닫으면 다시 열 수 없고 일반 대화로 바꾸거나 따로 저장할 수도 없어요. 프로필 정보와 개인 설정은 그대로 유지됩니다.
{{< /hint >}}

{{< hint type="note" >}}
Team·Enterprise에서는 시크릿 대화라도 조직의 데이터 내보내기나 컴플라이언스 API 대상에 포함될 수 있습니다.
{{< /hint >}}

## 검색과 메모리로 이전 맥락 이어가기

지난주에 Claude와 나눈 이야기를 다시 떠올리고 싶을 때가 있죠. Claude에는 이전 대화를 활용하는 두 가지 기능이 있습니다. 하나는 지난 대화를 찾아 주는 **채팅 검색**, 다른 하나는 대화 요점을 기억하는 **메모리**예요.

### 채팅 검색과 메모리 비교

| 구분 | 채팅 검색(Chat Search) | 메모리(Memory) |
|---|---|---|
| 하는 일 | "전에 [주제]에 대해 뭐라고 얘기했지?"처럼 자연스럽게 물으면 지난 대화에서 찾아 줌 | 업무 맥락을 카테고리별 항목으로 기억해 두고 대화에 활용 |
| 갱신 주기 | 물어볼 때마다 검색 | 대화 중 실시간으로 읽고 쓰고 갱신 |
| 사용 가능 요금제 | Pro·Max·Team·Enterprise(유료) | 모든 요금제(무료·유료) |

### 검색·메모리 설정하기

1. Claude에서 <strong>Settings(설정) > Memory(메모리)</strong>를 엽니다.
2. 채팅 검색은 **'Search and reference chats'** 토글로 켜고 끕니다(Pro 이상).
3. 메모리는 **'Generate memory from chats'** 토글로 켜고, <strong>'View and edit memory'</strong>를 눌러 저장된 내용을 확인하고 편집합니다.
4. Enterprise는 **Organization settings(조직 설정) > Capabilities**에서 조직 전체 정책을 관리합니다.

### Claude가 기억하는 것과 기억하지 않는 것

| 기억하는 것 | 기억하지 않는 것 |
|---|---|
| 업무 맥락과 역할 | 시크릿 대화 |
| 소통 방식 선호 | 사용자가 제외한 정보 |
| 기술·코딩 선호 | 삭제한 대화 |
| 프로젝트 세부 정보 | — |

메모리는 프로젝트마다 별도의 공간으로 관리되고 웹·Claude Desktop·모바일 앱에서 모두 작동합니다.

{{< hint type="warning" >}}
메모리 초기화는 되돌릴 수 없어요. 또한 조직 단위로 메모리를 끄면 모든 사용자의 메모리 데이터가 자동으로, 영구적으로 삭제됩니다.
{{< /hint >}}

{{< hint type="note" >}}
채팅 검색은 Free 요금제에서는 쓸 수 없고 Enterprise에서 고객 관리형 암호화 키를 사용하는 경우에도 이용할 수 없습니다.
{{< /hint >}}

## Fable 5에서 요청이 막혔을 때 모델이 바뀌는 이유

가장 성능이 높은 **Claude Fable 5**를 쓰다 보면, 가끔 응답 모델이 자동으로 바뀔 수 있어요. Fable 5는 생명과학·사이버보안 같은 민감 분야에서 강력한 능력을 가진 만큼, 안전을 위해 일부 요청을 차단하거나 덜 강력한 모델로 넘겨주는(폴백) 보호 장치를 함께 운영하기 때문이에요.

차단은 주로 **생물·화학·생명과학 관련 질의**와 **공격적 사이버 보안 기법** 같은 영역에서 일어납니다. 이때 막힌 요청은 같은 대화에서 더 안전하게 처리되는 Opus 모델로 다시 실행돼요 — 생물·화학·생명과학 요청은 **Opus 5**로, 공격적 사이버보안 요청은 **Opus 4.8**로 폴백됩니다. 전환 후에는 대화의 나머지 부분도 Opus로 진행되며, 언제든 모델 선택기에서 Fable 5로 직접 돌아갈 수 있어요.

자동 전환은 Fable 5를 처음 선택할 때 기본으로 켜지며, 끄려면 다음과 같이 합니다.

1. <strong>Settings(설정) > Capabilities(기능)</strong>로 이동합니다(Claude Code에서는 **Config > MODEL & OUTPUT**).
2. **'Switch models when a message is flagged'** 토글을 끕니다. 자동 전환을 끄면 차단된 요청은 모델을 바꾸지 않고 대화가 일시 정지돼요.

{{< hint type="note" >}}
이 자동 전환은 Fable 5를 쓸 수 있는 모든 환경(claude.ai·데스크톱·모바일·API 등)에서 같은 방식으로 작동합니다. 사이버보안 작업에 정당한 방어 목적이 있다면 Opus 대상의 **Cyber Verification Program(CVP)** 을 신청해 보호 장치의 영향을 줄일 수 있어요.
{{< /hint >}}

## 다음 단계

- **[개인화 설정](/help/personalization/)** — Claude를 내 스타일에 맞게 조정하기
- **[요금제와 결제](/help/plans-billing/)** — 요금제별로 쓸 수 있는 기능 비교

## 원문 출처

- [How can I delete or rename a conversation?](https://support.claude.com/en/articles/8230524-how-can-i-delete-or-rename-a-conversation)
- [Share and unshare chats](https://support.claude.com/en/articles/10593882-share-and-unshare-chats)
- [Using incognito chats](https://support.claude.com/en/articles/12260368-using-incognito-chats)
- [Use Claude's chat search and memory to build on previous context](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context)
- [Why Claude switched models in your conversation with Fable 5](https://support.claude.com/en/articles/15363606-why-claude-switched-models-in-your-conversation-with-fable-5)
