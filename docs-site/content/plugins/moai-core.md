---
title: "moai-core — 프로젝트·라우터·AI 슬롭 + MCP 4커넥터 셋업"
weight: 20
description: "moai-core는 cowork-plugins의 기반 플러그인으로 프로젝트 초기화, AI 슬롭 검수, 피드백 허브, MCP 4커넥터 인증 가이드를 포함한 8개 핵심 스킬을 제공합니다."
geekdocBreadcrumb: true
tags: ["moai-core"]
---

# moai-core

> `cowork-plugins` 전체의 기반이 되는 코어 플러그인입니다. **다른 플러그인을 사용하기 전에 반드시 먼저 설치**하세요.

## 무엇을 하는 플러그인인가

`moai-core`를 한마디로 이해하려면 건물의 **기초공사·수도·전기 배선**을 떠올리면 됩니다. 콘텐츠를 만드는 플러그인, 사업·법무를 다루는 플러그인이 각 층의 방이라면, `moai-core`는 그 방들이 공통으로 쓰는 수도·전기·도면을 깔아두는 지하 인프라 층입니다. 그래서 다른 방을 꾸미기 전에 이 층부터 먼저 시공(설치)해야 합니다. 여기서 **인프라**(infrastructure)란 "각 방이 제 몫을 하려면 반드시 깔려 있어야 할 공용 바탕 시설"을 가리키는 말입니다.

이 인프라 층이 구체적으로 까는 것은 크게 세 가지입니다. 첫째, 프로젝트의 도면 역할을 하는 작업 지침서(`CLAUDE.md`)를 자동으로 그려주는 `/project` 마법사, 둘째, 완성된 글에서 기계적으로 튀어나오는 AI 특유 어투를 마지막 한 번 솎아내는 `ai-slop-reviewer`, 셋째, 외부 도구(Drive·Notion·Higgsfield·OpenAI)를 연결하는 발주 창구 겸 가이드인 `mcp-connector-setup`입니다. 이 세 가지가 자리잡아야 비로소 다른 플러그인이 만든 산출물이 안정적으로 흘러나옵니다.

`moai-core`는 `cowork-plugins` 마켓플레이스의 모든 도메인 플러그인이 공유하는 인프라를 제공합니다. 프로젝트별 작업 지침(`CLAUDE.md`)을 자동 생성하고 프로젝트 맞춤 에이전트까지 합성하는 `/project` 마법사, 모든 텍스트 산출물의 마지막 단계에서 AI 패턴을 다듬어주는 `ai-slop-reviewer`, 버그·기능 요청을 GitHub Issues로 바로 등록하는 `feedback` 스킬, Drive·Notion·Higgsfield·OpenAI **4커넥터 인증·환경변수·트러블슈팅 통합 가이드** `mcp-connector-setup`을 포함한 **총 8개 스킬**이 포함되어 있습니다.

`ai-slop-reviewer`는 모든 한국어 텍스트 산출물(블로그·뉴스레터·계약서·사업계획서·이메일 등)의 체인 마지막 단계에서 호출되어, 과장된 수식어·기계적 접속어·모호한 일반화 같은 AI 글쓰기 패턴을 진단하고 사람 톤으로 다듬어줍니다.

`/project` 한 번이면 설치된 `moai-*` 플러그인을 자동 감지해 산출물별 스킬 체인을 설계하고, **v2.21.0부터는 코디네이터 에이전트까지 동적 스캔**(`agents/*.md` frontmatter 인벤토리)해 멀티스텝 체인을 에이전트 우선으로 매핑합니다. 200라인 이내의 `CLAUDE.md`를 프로젝트 루트에 생성하고, 자격 조건을 갖춘 워크플로우에 한해 프로젝트 맞춤 sub-agent를 `.claude/agents/`에 합성합니다. (`/project init`은 레거시 별칭으로 계속 동작합니다.)

## 설치

{{< tabs "install-core" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. Cowork에서 `modu-ai/cowork-plugins` 마켓플레이스를 추가합니다.
2. `moai-core` 옆의 **+** 버튼을 눌러 설치합니다.
{{< /tab >}}
{{< tab "수동" >}}
[GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-core)를 클론한 뒤 `~/.claude/plugins/`에 배치합니다.
{{< /tab >}}
{{< /tabs >}}

## 완성된 공구 진열대 vs 공구를 만드는 작업장

8개 스킬 표를 한 번에 펼쳐 보면 "내가 지금 뭘 써야 하지?" 하고 망설이게 됩니다. 그래서 이 표를 읽기 전에 먼저 **공장** 하나를 떠올려 보세요. 공장에는 두 구역이 있습니다. 하나는 완성된 망치·드라이버·펜치를 진열해 둔 **완제품 진열대**이고, 다른 하나는 그 공구를 직접 깎아 만드는 **작업장**입니다.

`moai-core`의 8개 스킬도 똑같이 두 갈래로 나뉩니다. `project`·`ai-slop-reviewer`·`feedback`·`mcp-connector-setup`은 진열대 위에 올라온 **바로 집어 쓰는 완성된 공구**입니다 — "프로젝트 세팅해줘", "AI 티 고쳐줘", "버그 신고할게"라고 말하면 즉시 작동합니다. 반면 `skill-builder`·`skill-template`·`skill-tester`는 공구를 깎아 만드는 **작업장 도구**입니다. 이 셋은 새 스킬을 만들거나 고칠 때만 찾는, 이른바 **메타 스킬(meta-skill)** — 도구를 다루는 도구를 뜻합니다.

핵심은 **일반 사용자는 진열대만 둘러봐도 충분**하다는 점입니다. 평소에는 `project`로 도면을 깔고 `ai-slop-reviewer`로 마무리 다듬기를 반복하면 됩니다. 작업장(`skill-builder` 일가)은 "기존 스킬에 없는 새로운 일이 생겼다, 내가 직접 스킬 하나 더 만들어야겠다"는 날이 오기 전까지는 굳이 열어볼 필요가 없습니다. 즉, 이 표를 읽을 때 진열대 영역(바로 쓰는 스킬)과 작업장 영역(메타 스킬)을 구분해서 보면, 어디서부터 시작할지 막막하지 않습니다.

```mermaid
flowchart LR
    subgraph Shelf["① 완제품 진열대 (바로 집어 쓰는 스킬)"]
        S1["project<br/>도면 깔기"]
        S2["ai-slop-reviewer<br/>마무리 다듬기"]
        S3["feedback<br/>버그 신고"]
        S4["mcp-connector-setup<br/>외부 연결"]
    end

    subgraph Workshop["② 공구 제작 작업장 (메타 스킬)"]
        W1["skill-builder<br/>새 공구 깎기"]
        W2["skill-template<br/>공구 설계도"]
        W3["skill-tester<br/>공구 시험"]
    end

    User(["일반 사용자"]) --> Shelf
    Workshop -. 필요할 때만 .-> Shelf

    style Shelf fill:#e6f0ef,stroke:#144a46,color:#09110f
    style Workshop fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style User fill:#eaeaea,stroke:#6e6e6e,color:#09110f
```

## 핵심 스킬 (8개)

| 스킬 | 용도 | 자동 호출 트리거 |
|---|---|---|
| `project` | 프로젝트 초기화·맞춤 에이전트 합성·상태·API 키·카탈로그 관리 (`/project`, `/project status`, `/project apikey`, `/project catalog`; `/project init`은 레거시 별칭) | "프로젝트 초기화", "CLAUDE.md 만들어줘", "전담 에이전트로 만들어줘" |
| `ai-slop-reviewer` | 텍스트 산출물의 AI 패턴 진단·수정 | "AI 티 나는 부분 고쳐줘", "사람이 쓴 것처럼 수정해줘" |
| `feedback` | 버그 리포트·기능 요청을 GitHub Issues로 자동 등록 | "/project feedback", "버그 신고", "기능 요청" |
| `ai-diagnostic` | AI 시스템 진단, 성능 모니터링, 오류 분석 | "AI 동작이 이상해", "성능 체크해줘" |
| `mcp-connector-setup` | Drive·Notion·Higgsfield·OpenAI **4커넥터** 인증·환경변수·트러블슈팅. Windows MAX_PATH·한글 파일명 30자·`computer://` 링크 오류 대응. 셋업 완료 체크리스트(4커넥터 인증 + 1회 호출 성공) | "MCP 커넥터 연결", "Drive 인증 방법", "Higgsfield 키 발급", "Windows MAX_PATH 오류" |
| `skill-builder` | 새 스킬 생성, 기존 스킬 수정, 스킬 템플릿 관리 (v1.5.x: skill-forge 후속) | "새 스킬 만들어줘", "스킬 템플릿 제공해줘", "/harness" |
| `skill-template` | 스킬 구조 템플릿, 프롬프트 엔지니어링 가이드 | "스킬 구조 알려줘", "템플릿 참고할게" |
| `skill-tester` | 스킬 테스트, 검증, 품질 보증 | "이 스킬 테스트해줘", "검증 프로세스 설계해줘" |

## `/project` 흐름

### 프로젝트에 딱 맞는 전담 에이전트를 만들어주는 기능

**서브에이전트**(sub-agent)란 AI가 스스로 불러 쓰는 "작업 담당 조수"입니다. 블로그를 쓰는 스킬 하나, 발표자료를 만드는 스킬 하나처럼 단일 일을 하는 도구를 넘어, "사업계획서를 완성해 줘"처럼 여러 단계를 묶어 한 번에 끝내는 역할을 합니다.

`moai-core`의 `/project` 마법사는 **"이 프로젝트에선 어떤 산출물을, 얼마나 자주 만드나"**를 몇 가지 질문으로 파악한 뒤, 설치된 `moai-*` 플러그인에 이미 딸려 온 담당 조수(코디네이터 에이전트)가 있는지 먼저 살핍니다. 있으면 그것을 그대로 씁니다. 예컨대 "사업계획서 만들어줘"라고 하면 `moai-business` 플러그인에 들어있는 `business-plan-coordinator`가 기획→시장분석→검수→발표자료까지 알아서 엮어 줍니다.

문제는 **기존 조수가 아무도 담당하지 않는 일**입니다. 이때 v2.21.0부터는 그 빈자리를 채우는 전담 에이전트를 새로 짜서 `.claude/agents/` 폴더에 기록합니다. 단, 무조건 만드는 게 아니라 (1) 반드시 거쳐야 할 정해진 단계가 있거나, (2) 여러 결과물을 동시에 찍어내야 하거나, (3) 사용자가 매일처럼 반복하는 일일 때만 만듭니다. 그냥 한두 단계짜리 단순 작업은 굳이 에이전트를 새로 만들지 않고, 기존 스킬 몇 개를 차례로 부르는 것으로 충분하다고 판단합니다.

핵심은 **"있는 것부터 쓰고, 정말 비어 있는 자리만 새로 합성한다"**는 절제입니다. 덕분에 프로젝트마다 "이 팀은 재무 리포트를 주로 뽑으니까 재무 담당 조수를 한 명 더 두자" 식으로 맞춤 인력을 배치하는 효과를 얻으면서도, 에이전트가 불필요하게 늘어나는 혼란은 막습니다. 새로 합성된 에이전트는 다음 세션(또는 `/reload-plugins`)부터 "재무 리포트 조립해 줘" 같은 자연어 한 줄로 바로 불러 쓸 수 있습니다.

```mermaid
flowchart TD
    A["① Interview<br/>업무 맥락 수집"] --> B["② Detect<br/>플러그인 감지"]
    B --> C["③ Chain Design<br/>체인 설계"]
    C --> CA["③·5 Agent Synthesis<br/>맞춤 에이전트 합성"]
    CA --> D["④ Confirm<br/>승인"]
    D --> E["⑤ Generate<br/>CLAUDE.md 생성"]
    E --> F["⑥ APIKey<br/>키 등록"]
    F --> G["⑦ First Run<br/>첫 작업 예시"]

    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style CA fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style G fill:#e6f0ef,stroke:#144a46,color:#09110f
```

1. **Interview** — 최대 3개 질문으로 이번 프로젝트의 업무 맥락 수집 (이름·회사는 묻지 않음)
2. **Detect** — 설치된 `moai-*` 플러그인 자동 감지 (화이트리스트 동적 도출)
3. **Chain Design** — 산출물별 스킬 체인 설계 (예: 사업계획서 → `strategy-planner → docx-generator → ai-slop-reviewer`)
4. **Agent Synthesis (Phase 3.5)** — 고정 다단계·병렬 fan-out·빈번 반복 등 자격 조건을 갖춘 워크플로우에 한해 프로젝트 맞춤 sub-agent를 `.claude/agents/`에 합성 (새 세션에서 활성화, 플러그인 번들보다 우선순위 높음)
5. **Confirm** — AskUserQuestion으로 체인·에이전트 설계 최종 승인
6. **Generate** — `CLAUDE.md` 자동 생성 (200라인 이내)
7. **APIKey** — 선택된 플러그인이 요구하는 키만 프로젝트 격리 저장
8. **First Run** — 첫 작업 예시 3개 제안


![moai-core-subagent-synthesis](/diagrams/moai-core-subagent-synthesis.svg)

## `ai-slop-reviewer` 이해하기

왜 이 스킬이 체인의 **맨 마지막**에 와야 할까요? **출간 전 원고교정 편집자**를 떠올리면 됩니다. 원고가 아무리 잘 쓰였어도 기계적으로 반복되는 수식어와 늘어진 접속어는 마지막 한 번 더 솎아내야 비로소 "사람이 쓴 듯한" 문장이 됩니다. 냄비에 재료를 다 넣고 끓인 뒤, 마지막에 불을 줄여 거품을 걷어내는 것과 같습니다 — 거품(AI 패턴)을 걷어내야 맑고 깔끔한 국물(완성된 글)이 되듯, 이 검수가 빠지면 산출물 표면에 기계적인 티가 그대로 남게 됩니다.

그래서 순서가 중요합니다. 글이 다 쓰이기도 전에 검수를 끼워 넣으면 검수할 원문 자체가 없고, 포맷 변환 전에 검수하면 나중에 형식이 바뀌면서 다시 AI 어투가 스며들 수 있습니다. 글의 내용과 형식이 모두 완성된 **가장 마지막 한 번**에 통과시켜야 효과가 남습니다.

AI가 작성한 글에는 공통된 패턴이 있습니다.

- 과장된 수식어("혁신적인", "획기적인", "업계 최고의")
- 기계적 접속어("첫째", "둘째", "마지막으로"가 과하게 반복)
- 모호한 일반화("많은 사람들은…")
- 불필요한 요약 반복

`ai-slop-reviewer`는 이러한 패턴을 **진단**하고, **수정 텍스트**를 제시하며, **주요 변경사항**을 리포트로 남깁니다. `cowork-plugins`의 모든 텍스트 스킬 체인은 이 단계로 종료하는 것이 권장됩니다.

## 산출물 파이프라인에서의 위치

`moai-core`가 전체 산출물 흐름의 어디에 서 있는지 한눈에 보려면 **요리 스튜디오의 공용 설비**를 떠올리면 됩니다. 각 분야 플러그인(moai-business·moai-content·moai-legal 등)이 메뉴를 만드는 주방이라면, `moai-core`는 레시피 북(`project`), 맛 점검역(`ai-slop-reviewer`), 식자재 발주 창구(`mcp-connector-setup`)를 갖춘 중앙 지원 구역입니다. 주방에서 요리가 다 나와도 마지막엔 반드시 맛 점검역이 한 번 더 기계적 맛(AI 티)을 솎아내야 완성된 산출물이 됩니다.

아래 그림은 산출물이 도메인 스킬(내용 만들기)에서 포맷 스킬(형식 갖추기)을 거쳐, 마지막으로 `moai-core`의 품질 스킬(기계적 어투 솎아내기) 단계로 흘러들어 완성되는 과정을 보여줍니다.

```mermaid
flowchart LR
    subgraph Domain["① 도메인 스킬 (내용 만들기)"]
        D1["moai-business"]
        D2["moai-content"]
        D3["moai-legal"]
    end

    subgraph Format["② 포맷 스킬 (형식 갖추기)"]
        F1["docx-generator"]
        F2["pptx-designer"]
        F3["xlsx-creator"]
    end

    subgraph Core["③ moai-core (품질·지원)"]
        C1["project<br/>작업 지침서 생성"]
        C2["ai-slop-reviewer<br/>AI 어투 솎아내기"]
        C3["mcp-connector-setup<br/>외부 도구 연결"]
    end

    Domain --> Format
    Format --> C2
    C1 -. 지침서 제공 .-> Domain
    C3 -. 키·연결 .-> Domain

    style Domain fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style Format fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style Core fill:#e6f0ef,stroke:#144a46,color:#09110f
```

그림에서 실선은 산출물이 실제로 흘러가는 방향(내용 → 형식 → 품질 점검)이고, 점선은 `moai-core`가 앞단계에 **지원**으로 끼워 넣는 것 — 작업 지침서(`project`)와 외부 연결(`mcp-connector-setup`)을 미리 깔아두는 역할입니다. 이렇게 보면 왜 이 스킬들이 한 플러그인에 묶였는지, 그리고 다른 플러그인의 결과물 품질을 어떻게 떠받치는지가 한눈에 드러납니다.

## 대표 체인

```text
(도메인 스킬)
  → (포맷 변환 스킬, 예: docx-generator)
  → ai-slop-reviewer   ← 필수
```

코드·데이터·차트 같은 **비텍스트 산출물**은 `ai-slop-reviewer`를 스킵합니다.

## 빠른 사용 예

```text
/project
```

```text
이 블로그 글에서 AI 티 나는 부분 고쳐줘.
```

```text
MCP 커넥터 4개 연결 방법 알려줘 — Drive·Notion·Higgsfield·OpenAI
```
→ `mcp-connector-setup` 🆕

## `mcp-connector-setup`

Drive·Notion·Higgsfield·OpenAI 4커넥터를 Cowork에 연결하는 단계별 가이드입니다. 커넥터별 인증 절차·환경변수 설정·트러블슈팅을 한 곳에서 다루며, 셋업 완료 체크리스트는 **4커넥터 모두 인증 성공 + 1회 호출 성공**입니다.

## 왜 '커넥터'를 연결해야 할까

커넥터라는 단어가 처음이면 **레스토랑의 외부 발주 전화선**을 떠올리세요. 주방(moai 스킬)이 Google Drive에 있는 문서를 읽어 오거나 Higgsfield에서 이미지를 찍어 내려면, 그 외부 서비스에 "주문 전화"를 걸 수 있는 전화선과 인증된 전화번호가 미리 깔려 있어야 합니다. 전화선이 안 깔리면 아무리 주방이 뛰어나도 외부 식자재를 당겨올 수 없습니다.

여기서 두 낯선 용어가 등장합니다. **MCP**(Model Context Protocol)는 그 전화선 규격, 즉 "AI가 외부 도구와 통신하는 표준 연결 방식"입니다. **커넥터**는 그 규격에 맞춰 깔은 전화선 한 가닥 — Drive 선, Notion 선, Higgsfield 선, OpenAI 선 4가닥입니다. 그리고 **API 키**(또는 OAuth 토큰)는 "이 전화를 걸 권리가 있는, 인증된 전화번호" 역할을 합니다.

`mcp-connector-setup`은 바로 이 **전화선 4가닥을 설치하고 인증된 전화번호를 등록해 주는 통신 설치 가이드**입니다. 각 커넥터가 어떤 인증을 요구하는지, 환경변수(설정값)를 어디에 적어 넣어야 하는지, 선이 안 깔리거나 번호가 만료됐을 때(트러블슈팅) 어떻게 고치는지를 차례로 안내합니다. 4가닥이 모두 연결되고 한 번씩 "여보세요" 호출이 성공해야 셋업이 끝난 것으로 봅니다.

```mermaid
flowchart LR
    subgraph Kitchen["주방 (moai 스킬)"]
        K1["문서 읽기"]
        K2["이미지 생성"]
        K3["음성·영상 생성"]
    end

    Setup["mcp-connector-setup<br/>통신 설치 가이드"]

    subgraph Lines["외부 발주 전화선 (MCP 커넥터)"]
        L1["Drive 선<br/>(문서·파일)"]
        L2["Notion 선<br/>(메모·DB)"]
        L3["Higgsfield 선<br/>(이미지·영상)"]
        L4["OpenAI 선<br/>(텍스트·추론)"]
    end

    Keys["API 키 · OAuth<br/>(인증된 전화번호)"]

    Setup --> Lines
    Keys -. 등록 .-> Lines
    Kitchen ==>|주문 전화| Lines

    style Kitchen fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style Setup fill:#fbf0dc,stroke:#c47b2a,color:#09110f
    style Lines fill:#e6f0ef,stroke:#144a46,color:#09110f
    style Keys fill:#eaeaea,stroke:#6e6e6e,color:#09110f
```

**트러블슈팅 커버리지**:
- Windows MAX_PATH (260자 제한) 오류
- 한글 파일명 30자 초과 오류
- `computer://` 링크가 열리지 않는 경우
- API 키 만료·rate limit·OAuth 토큰 갱신
- Higgsfield Secret Key 발급 절차 (워크스페이스 사전 비용 충전 1.5배 권장)

## 다음 단계

- [빠른 시작](../quick-start/) — 실제 프로젝트 초기화 전 과정
- [Cowork 플러그인 사용](../../cowork/plugins/)

---

### Sources

- [modu-ai/cowork-plugins README](https://github.com/modu-ai/cowork-plugins)
- [moai-core 디렉터리](https://github.com/modu-ai/cowork-plugins/tree/main/moai-core)
