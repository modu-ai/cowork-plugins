---
title: "계정 관리"
weight: 30
description: "로그인부터 이메일 변경, 세션 보안, 데이터 내보내기, 계정 삭제까지 Claude 계정 관리의 모든 것을 안내합니다."
geekdocBreadcrumb: true
---

집 열쇠를 잘 챙기고, 누가 우리 집에 드나드는지 살피고, 필요하면 자물쇠를 바꾸는 일—Claude 계정 관리도 이와 비슷합니다. 어떻게 로그인하는지, 어떤 기기에서 내 계정이 열려 있는지, 내 대화 기록을 어떻게 백업하는지, 그리고 더 이상 쓰지 않을 때 어떻게 깨끗이 정리하는지를 알아 두면 안심하고 Claude를 쓸 수 있습니다.

이 페이지에서는 로그인 방법부터 이메일 변경, 활성 세션 관리, 데이터 내보내기, 계정 삭제까지 계정과 관련된 일들을 차근차근 정리했습니다. 필요한 항목만 골라서 읽으셔도 됩니다.

## 로그인하기

Claude는 비밀번호를 따로 만들지 않습니다. 대신 두 가지 방식 중 하나로 로그인합니다.

| 로그인 방식 | 동작 방식 |
|---|---|
| **Google로 계속하기** | Google 계정 정보를 입력해 바로 로그인 |
| **이메일로 계속하기** | 이메일로 보안 로그인 링크를 받아 인증 |

이메일 로그인을 선택하면 `@mail.anthropic.com`에서 **'Secure link to log in to Claude.ai'**라는 제목의 메일이 도착합니다. 이 메일 안의 링크가 곧 열쇠입니다.

1. Claude 로그인 페이지로 이동합니다.
2. **'Continue with Google'** 또는 **'Continue with email'** 중 하나를 선택합니다.
3. 이메일 방식이라면 이메일 주소를 입력하고 **'Continue with email'**을 누릅니다.
4. 받은 편지함에서 보안 로그인 링크 메일을 확인합니다.
5. **같은 기기**에서 로그인한다면, 링크를 클릭하면 자동으로 로그인됩니다.
6. **다른 기기**에서 링크를 열었다면 인증 코드가 표시됩니다. 이 코드를 원래 기기에 입력해 로그인을 마칩니다.

로그인은 웹 브라우저, 데스크톱 앱, 모바일 앱 모두에서 가능합니다.

{{< hint type="note" >}}
로그인 메일이 보이지 않으면 스팸·정크 메일함을 확인하세요. `@mail.anthropic.com` 도메인을 안전한 주소로 등록(화이트리스트)해 두면 다음부터 메일이 잘 도착합니다.
{{< /hint >}}

{{< hint type="warning" >}}
현재 비밀번호를 직접 만드는 기능은 지원되지 않습니다. 또한 OAuth 토큰과 구독 자격 증명은 유료 구독자에게만 제공되며 외부 도구를 연동하려면 Claude Console이나 클라우드 제공업체에서 발급한 API 키를 사용해야 합니다.
{{< /hint >}}

## 전화번호 인증

새 계정을 만들 때는 전화번호 인증이 **반드시** 필요하며 건너뛸 수 없습니다.

1. 지원되는 지역에서 전화번호를 입력합니다.
2. 문자 메시지로 6자리 인증 코드를 받습니다.
3. 화면에 코드를 입력합니다.
4. **Verify code** 버튼을 눌러 완료합니다.

| 사용할 수 없는 번호 유형 |
|---|
| VoIP 서비스 |
| Google Voice |
| 앱 기반 번호 |
| 유선 전화(landline) |
| 문자 수신이 불가능한 모든 서비스 |

{{< hint type="warning" >}}
한 번 인증한 전화번호는 **변경할 수 없습니다.** 또한 이미 다른 계정에 연결된 번호는 지원팀에 연결 해제를 요청하기 전까지 재사용할 수 없습니다. 코드가 5분 안에 도착하지 않으면 번호를 다시 확인하고 재시도하세요.
{{< /hint >}}

## 이메일 주소 변경

아쉽지만 기존 계정의 이메일 주소를 직접 바꾸는 기능은 지원되지 않습니다. 원하는 이메일로 쓰려면 **새 계정을 만드는 방식**을 따라야 합니다. 절차는 다음과 같습니다.

1. 유료 플랜을 쓰고 있다면 **설정 > Billing**에서 구독을 취소합니다. 추가 청구를 피하려면 다음 결제일 **최소 24시간 전**에 취소하세요.
2. 새 계정에서 전화번호를 다시 쓰고 싶다면, 설정에서 전화번호 연결을 해제합니다.
3. 보존할 내용이 있다면 데이터 내보내기로 대화를 백업합니다.
4. **설정 > Account**에서 **'Delete Account'**를 눌러 기존 계정을 삭제합니다.
5. 원하는 이메일 주소로 새 Claude 계정을 만듭니다.

{{< hint type="warning" >}}
계정 삭제는 영구적이며 되돌릴 수 없습니다. 저장된 모든 대화와 기록이 사라지므로 삭제 전에 반드시 데이터를 내보내세요. 만약 기존 이메일에 접근할 수 없는 상황이라면, 접근 가능한 다른 이메일로 지원팀에 연락해 도움을 받으세요.
{{< /hint >}}

## 활성 세션 관리

내 계정이 지금 어떤 기기와 브라우저에서 열려 있는지 한눈에 보고 모르는 접속을 직접 끊을 수 있습니다. 공용 PC를 썼거나 누군가 무단으로 접속했을지 걱정될 때 특히 유용합니다.

각 세션에는 다음 정보가 표시됩니다.

| 표시 항목 | 내용 |
|---|---|
| 기기/브라우저 | 접속한 기기와 브라우저 종류 |
| 운영 체제 | 해당 기기의 OS |
| 위치 | IP 기반 대략적인 지역 |
| 마지막 활동 | 가장 최근 사용 시각 |

지금 사용 중인 세션에는 **현재(Current)** 배지가 붙습니다.

### 세션 하나씩 끊기

1. 왼쪽 아래의 프로필 아이콘을 클릭합니다.
2. **설정 > Account**로 이동합니다.
3. **Active sessions** 영역까지 내려갑니다.
4. 각 세션의 기기·위치·마지막 활동을 살펴봅니다.
5. 끊고 싶은 세션 옆의 점 3개 메뉴(⋮)를 누릅니다.
6. **Terminate**를 선택하고 확인 창에서 한 번 더 확인합니다.

종료된 세션의 기기는 다시 로그인해야 계정에 접근할 수 있습니다.

### 모든 세션에서 한 번에 로그아웃

기기를 분실했거나 한꺼번에 정리하고 싶다면 모든 활성 세션을 동시에 끊을 수 있습니다.

1. 웹 브라우저에서 [claude.ai](https://claude.ai)에 로그인합니다.
2. 왼쪽 아래 이니셜을 클릭합니다.
3. 드롭다운에서 **'Settings'**를 선택합니다.
4. **'Account'** 섹션으로 이동합니다.
5. **'Log Out'** 버튼을 누릅니다.
6. 확인 창에서 한 번 더 확인합니다.

웹 세션은 28일간 유지되며 활동이 있을 때마다 한 시간 단위로 갱신됩니다.

{{< hint type="note" >}}
모든 세션 로그아웃 기능은 현재 **웹 버전(claude.ai)에서만** 제공되며 iOS·Android 모바일 앱에서는 지원되지 않습니다. Claude Code 인증 토큰은 별도로 **설정 > Claude Code**에서 휴지통 아이콘으로 개별 삭제할 수 있습니다.
{{< /hint >}}

{{< hint type="tip" >}}
모르는 기기나 의심스러운 위치가 보이면 즉시 해당 세션을 종료하세요. 위치는 IP 기반의 대략적인 값이라 정확하지 않을 수 있지만 낯선 접속이라면 끊어 두는 편이 안전합니다.
{{< /hint >}}

### 세션 보안 설정(관리자 전용)

조직 단위로 세션 최대 유지 기간을 정해 일정 기간이 지나면 다시 로그인하도록 강제할 수 있습니다. 이 기능은 **Enterprise 플랜의 Admin·Owner와 Console Admin**만 사용할 수 있습니다.

| 구분 | 설정 경로 | 선택 가능한 기간 |
|---|---|---|
| Enterprise Admin | Organization settings > Organization and access > Session security | 1일, 7일, 14일, 28일 |
| Console Admin | Settings > Organization and access > Session security | 1일, 3일, 7일 |

원하는 기간을 고른 뒤 **Enable**을 눌러 적용합니다. 해제하려면 **Shortened session length** 옆의 **Disable**을 선택합니다.

{{< hint type="warning" >}}
설정을 적용하는 순간, 선택한 기간보다 오래된 기존 세션은 즉시 만료됩니다. 여러 조직에 속한 사용자라면 가장 **짧은** 기간 설정이 모든 멤버십에 일괄 적용됩니다.
{{< /hint >}}

## 데이터 내보내기

대화 기록과 계정 정보를 파일로 백업할 수 있습니다. 계정을 옮기거나 삭제하기 전, 또는 그냥 기록을 보관하고 싶을 때 사용하세요. Free·Pro·Max 플랜에서 모두 가능합니다.

1. Claude 웹 앱 또는 Claude Desktop에서 왼쪽 아래 이니셜을 클릭합니다.
2. 메뉴에서 **Settings**를 선택합니다.
3. **Privacy** 섹션으로 이동합니다.
4. **Export data** 버튼을 누릅니다.
5. 등록된 이메일 주소로 다운로드 링크가 도착하면 확인합니다.
6. 로그인을 유지한 상태에서 링크 만료(24시간) 전에 파일을 내려받습니다.

내보낸 파일에는 대화 데이터와 계정 정보가 담깁니다.

{{< hint type="warning" >}}
다운로드 링크는 24시간 후 만료되며 다운로드하는 동안에는 로그인을 유지해야 합니다. 내보낸 데이터는 다른 개인 계정으로 가져오기(import)할 수 없습니다. 이 기능은 모바일 앱(iOS·Android)에서는 제공되지 않습니다. Team·Enterprise 사용자가 조직 데이터를 내보내려면 Primary Owner 권한이 필요합니다.
{{< /hint >}}

## 계정 삭제

계정을 영구히 지우고 싶다면 다음 순서를 따릅니다.

1. Claude 계정에 로그인합니다.
2. 왼쪽 아래 이니셜 또는 이름을 클릭합니다.
3. **'Settings'**를 선택합니다.
4. **'Account'** 섹션으로 이동합니다.
5. Pro·Max 구독이 있다면 먼저 **Billing**에서 구독을 취소하고 현재 결제 기간이 끝날 때까지 기다립니다.
6. **'Delete account'** 버튼을 누릅니다.
7. 지원팀 연락이 필요하다는 안내가 뜨면, 지원팀에 요청해 삭제를 마칩니다.

{{< hint type="warning" >}}
계정 삭제는 영구적이며 복구할 수 없고 저장된 모든 대화가 사라집니다. 필요한 내용은 삭제 전에 데이터 내보내기로 백업하세요. 같은 이메일에 여러 계정이 연결되어 있다면, 어느 계정을 삭제할지 지정해야 합니다.
{{< /hint >}}

## 대화를 볼 수 있는 사람

민감한 정보를 입력해도 괜찮은지 궁금할 수 있습니다. 모델 개선에 동의한 경우, 모델 학습에 관여하는 **소수의 Anthropic 인력**만 대화를 볼 수 있습니다. 이때도 데이터는 자동으로 사용자 식별 정보와 분리되며 민감한 정보는 자동 도구로 필터링·가려집니다.

- 대화 데이터는 오직 Claude 개선에만 쓰이며 제3자에게 판매하거나 마케팅에 사용하지 않습니다.
- 안전 분류기가 유해 콘텐츠를 감지하기 위해 대화를 표시할 수 있습니다.
- 개인정보 설정은 계정에서 언제든 조정할 수 있습니다.
- 시크릿(incognito) 채팅은 모델 개선 설정과 무관하게 항상 학습 대상에서 제외됩니다.
- 이 내용은 Claude Free·Pro·Max 및 Claude Code 같은 소비자 플랜에 적용됩니다.

{{< hint type="warning" >}}
주민등록번호·신용카드·은행 계좌 같은 금융 정보, 건강·의료 기록, 비밀번호, 기밀 문서는 입력하지 않는 것이 좋습니다. 안전 분류기는 개인정보 설정과 무관하게 신뢰·안전 모델을 위해 대화를 표시할 수 있습니다.
{{< /hint >}}

## 지원받기

계정 문제로 도움이 필요할 때, 받을 수 있는 지원은 플랜과 권한에 따라 다릅니다.

| 사용자 유형 | 지원 범위 |
|---|---|
| Pro·Max 사용자 | 문서, Fin 챗봇, 메신저를 통한 사람 지원 |
| Team·Enterprise Owner | 전체 지원 + 사람 지원 받을 멤버 지정 가능 |
| Console Admin | 전체 지원 |
| Team·Enterprise 일반 멤버 | Fin 챗봇만 이용(사람 지원은 Owner를 통해 요청) |
| Free 사용자 | 문서와 Fin 챗봇, 사람 지원은 셀프서비스가 불가능한 계정 삭제에 한함 |

1. Claude 계정에 로그인합니다.
2. 왼쪽 아래 이니셜 또는 이름을 클릭합니다.
3. **'Get help'**를 선택합니다.
4. 자료를 검색하거나 Fin 챗봇과 대화합니다.
5. 사람 지원이 필요하면 **'Send us a message'**를 눌러 문의합니다.
6. 안내에 따라 상세 내용을 입력하면, 필요 시 이메일로 답변을 받습니다.

{{< hint type="note" >}}
전화나 실시간 채팅 지원은 제공되지 않으며 주요 연락 방법은 이메일입니다. 로그인이 불가능하다면 Help Center의 메시지 아이콘으로 계정 삭제·데이터 내보내기·구독 관련 지원을 받을 수 있습니다(계정 확인 절차가 필요합니다).
{{< /hint >}}

## 다음 단계

- **[요금제와 결제](../plans-billing/)** — 플랜별 차이와 구독 취소·청구 관리
- **[개인화 설정](../personalization/)** — 내 스타일에 맞게 Claude 조정하기
- **[대화 관리](../conversations/)** — 대화 정리·검색·보관
- **[문제 해결](../troubleshooting/)** — 자주 겪는 문제와 해결 방법

## 원문 출처

- [Log in to your Claude account](https://support.claude.com/en/articles/13189465-log-in-to-your-claude-account)
- [Verify your phone number](https://support.claude.com/en/articles/8287232-verify-your-phone-number)
- [How do I change the email address associated with my account?](https://support.claude.com/en/articles/8452276-how-do-i-change-the-email-address-associated-with-my-account)
- [How do I log out of all active sessions?](https://support.claude.com/en/articles/10310342-how-do-i-log-out-of-all-active-sessions)
- [Managing your active sessions](https://support.claude.com/en/articles/13124001-managing-your-active-sessions)
- [Configuring session security settings](https://support.claude.com/en/articles/13163631-configuring-session-security-settings)
- [Export your Claude data](https://support.claude.com/en/articles/9450526-export-your-claude-data)
- [How can I delete my Claude account?](https://support.claude.com/en/articles/9028421-how-can-i-delete-my-claude-account)
- [Who can view my conversations?](https://support.claude.com/en/articles/8325621-i-would-like-to-input-sensitive-data-into-my-chats-with-claude-who-can-view-my-conversations)
- [How to get support](https://support.claude.com/en/articles/9015913-how-to-get-support)
