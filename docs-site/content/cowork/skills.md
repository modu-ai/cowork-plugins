---
title: "스킬 사용법"
weight: 60
description: "스킬이 어떻게 자동 트리거되는지, 디렉터리 구조와 호출 방식 3가지를 정리합니다."
geekdocBreadcrumb: true
---
> 스킬(skill)은 "이런 요청이 오면 이렇게 처리해라"라는 절차적 지침 묶음입니다. 프롬프트 엔지니어링을 파일 하나로 저장해둔 것이라고 생각하면 쉽습니다.

## 스킬 트리거 흐름

```mermaid
flowchart TD
    A["사용자 자연어 요청"] --> B{"description<br/>매칭"}
    B -- 일치 --> C["스킬 자동 호출"]
    B -- 불일치 --> D["Claude 기본 응답"]
    C --> E["스킬 본문 실행"]
    E --> F["결과물 반환"]

    style A fill:#eaeaea,stroke:#6e6e6e,color:#09110f
    style C fill:#e6f0ef,stroke:#144a46,color:#09110f
    style F fill:#d6ebe7,stroke:#1c7c70,color:#09110f
```

## 언제 트리거되나

각 스킬의 `description` 필드에 트리거 조건이 쓰여 있습니다. Cowork가 사용자의 요청을 읽고, 일치하는 스킬이 있으면 자동으로 호출합니다.

예시:

- "블로그 글 써줘" → `moai-content:blog`
- "계약서 검토해줘" → `moai-legal:contract-review`
- "사업계획서 만들어줘" → `moai-business:strategy-planner`

## 스킬의 구조

```text
skill-name/
  SKILL.md               # 본체 (YAML frontmatter + 본문)
  references/            # 상세 참고 문서
  scripts/               # (선택) 실행 스크립트
  assets/                # (선택) 이미지·템플릿
```

`SKILL.md`는 다음 구조를 따릅니다.

```yaml
---
name: skill-name
description: >
  [무엇을 하는지] + [언제 쓰는지] + [트리거 키워드]
user-invocable: true
---

(본문: 절차, 규칙, 예시)
```

## 스킬 호출 방식

### 1. 자연어 요청 (권장)

사용자는 그냥 자연어로 요청합니다. Cowork가 맥락을 읽고 적합한 스킬을 자동 호출합니다.

{{< hint type="note" >}}
**문서 표기 규약**: 본 문서 전반에서 **사용자가 Cowork에 입력하는 모든 것**(자연어 지시·슬래시 명령·마켓플레이스 URL 등)은 macOS 터미널 스타일 박스 안에 `> ` prefix와 함께 표기합니다.

| 종류 | 문서 표기 | 실제 입력 |
|---|---|---|
| 슬래시 명령 | `> /project init` | `/project init` |
| 자연어 지시 | `> "블로그 글 써줘"` | `블로그 글 써줘` |
| 마켓플레이스 URL | `> modu-ai/cowork-plugins` | `modu-ai/cowork-plugins` |

`>`는 문서에서 "이건 사용자 입력"이라는 시각적 표식이며, **실제 대화창에 입력할 때는 `>`를 빼고 본문만** 입력하면 됩니다.
{{< /hint >}}

### 2. 슬래시 호출

특정 스킬을 명시적으로 부르고 싶으면 대화창에 `/`를 입력해 나타나는 목록에서 스킬을 선택합니다. 스킬의 frontmatter에 `user-invocable: true`가 설정된 스킬만 Tab 자동완성과 `/skill-name` 호출을 지원합니다.

{{< terminal title="claude — cowork" >}}
> /blog
  /contract-review
{{< /terminal >}}

{{< hint type="note" >}}
자연어 요청이 가장 안정적입니다. 슬래시 호출은 스킬별로 지원 여부가 다르고, 호출 가능 목록은 Cowork의 `/` 자동완성에서 직접 확인하는 게 가장 정확합니다.
{{< /hint >}}

### 3. 체이닝

여러 스킬을 연결해 파이프라인을 구성합니다. 자세한 설계 방법은 [쿡북 — 스킬 체인 설계](../../cookbook/skill-chaining/)에서 다룹니다.

## 제공된 스킬 활용하기

modu-ai/cowork-plugins 마켓플레이스는 21개 플러그인 안에 144개 스킬을 묶어 제공합니다. 사용자는 스킬을 직접 만들 필요 없이 — 자연어 한 줄로 GOAL을 던지면 시스템이 적합한 스킬을 자동으로 선택·체이닝합니다.

- **카테고리별 스킬 모음**: 콘텐츠·디자인·재무·법무·운영·마케팅·이커머스 등 21개 플러그인 ([플러그인 카탈로그](../../plugins/))
- **체인 예시 12종**: 자주 쓰는 스킬 조합 ([쿡북 — 스킬 체인 설계](../../cookbook/skill-chaining/))
- **트랙별 시나리오**: 본부·업무 영역별 한 줄 요청 → 자동 체인 ([쿡북 트랙](../../cookbook/tracks/))

## 다음 단계

- [플러그인 사용](../plugins/)
- [쿡북 — 스킬 체인 설계](../../cookbook/skill-chaining/)
- [쿡북 — 트랙별 시나리오](../../cookbook/tracks/)

---

### Sources

- [Use Skills in Claude](https://support.claude.com/en/articles/12512180)
- [modu-ai/cowork-plugins 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
