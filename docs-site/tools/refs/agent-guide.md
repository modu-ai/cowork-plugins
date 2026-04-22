# 섹션 저자 에이전트 작업 가이드

이 파일은 cowork/plugins/cookbook 섹션을 작성하는 에이전트가 참조하는 단일 진실(single source of truth)입니다.

---

## 1. 작업 개요

- **소스(읽기)**: `MoAI-Cowork-Plugins/docs-site-nextra-archive-20260423/pages/<section>/*.mdx`
- **출력(쓰기)**: `MoAI-Cowork-Plugins/cowork-plugins/docs-site/content/<section>/*.md`
- **방식**: 각 MDX 파일을 **개별로 읽고**, 본문 텍스트를 발췌·재구성해 Hugo Markdown으로 신규 저작. 기계적 1:1 변환 아님.
- **언어**: 모든 본문은 한국어 경어체. 전문용어는 한국어(영문) 병기 — 스킬(skill), 플러그인(plugin), 워크플로우(workflow).

## 2. Hugo Markdown front matter 규약

각 페이지 상단에 다음 YAML 필수:

```yaml
---
title: "한국어 페이지 제목"
weight: 10               # _meta.json 등장 순서 × 10
description: "검색·OG에 노출될 한 문장 요약 (~80자)"
geekdocBreadcrumb: true
---
```

선택 필드: `geekdocHidden: true`(메뉴 숨김), `geekdocAlign: center`(홈 등), `tags: [...]`.

## 3. weight 산정 규칙

`_meta.json`에 등장하는 순서대로 10씩 증가:
- 첫 페이지(또는 index/_index.md) → 10
- 두 번째 → 20
- separator는 weight를 점프(+5)시키되 본인은 페이지가 아니므로 weight 부여 X

cookbook 섹션은 `_meta.json`이 v0.2 신규 페이지(best-practices, automation-recipes, ai-employee-*, track-*)를 포함하지 않습니다. **신규 페이지는 동일 카테고리의 마지막 page weight + 10 위치에 추가**합니다.

## 4. Nextra 컴포넌트 → Geekdoc 숏코드 매핑

| Nextra | Geekdoc 대체 | 비고 |
|---|---|---|
| `<Callout type="info">...</Callout>` | `{{< hint type="note" >}}...{{< /hint >}}` | type: note/important/tip/caution/warning |
| `<Callout type="warning">` | `{{< hint type="warning" >}}` | |
| `<Callout type="error">` | `{{< hint type="danger" >}}` | |
| `<Steps>### 1. ...### 2. ...</Steps>` | 일반 ordered list `1. ...\n2. ...` | Geekdoc은 자동 번호 매김 |
| `<Tabs items={['a','b']}><Tab>...</Tab></Tabs>` | `{{< tabs "id" >}}{{< tab "a" >}}...{{< /tab >}}{{< tab "b" >}}...{{< /tab >}}{{< /tabs >}}` | id는 페이지 내 고유 |
| `<Cards><Card title="x" href="/y" />` | 일반 마크다운 링크 리스트 또는 `{{< columns >}}...{{< column >}}...` | Geekdoc은 카드 숏코드 없음, 링크 박스로 대체 |
| `<details><summary>...</summary>...</details>` | 동일 (HTML 그대로 사용 가능) | |
| `import { ... } from 'nextra/components'` | **삭제** | 라인 자체 제거 |
| `import Image from ...` | 마크다운 `![alt](path)` | |
| MDX 변수 `{constant}` | 텍스트로 풀어쓰기 | |
| `<details>` 접기 | 그대로 사용 가능 | 자가 채점 정답 등에 활용 |

### 코드 블록
- Nextra: ` ```bash filename="..." copy ` → Hugo: ` ```bash {title="..."} ` (Geekdoc은 title 지원)
- 언어 명시 필수

## 5. 페이지 구조 템플릿

### `/cowork/*` 템플릿

```markdown
---
title: "..."
weight: NN
description: "..."
---

# 한국어 제목

> 한 줄 요약(소스 페이지 인트로 발췌·정제)

## 핵심 개념
(본문 핵심 — 발췌·재서술. 마케팅 톤 제거, 사실 위주)

## 따라하기 (해당 페이지에 있을 때만)
1. ...
2. ...

{{< hint type="note" >}}
주의/팁 박스
{{< /hint >}}

## 자주 겪는 이슈
- ...

## 다음 단계
- [관련 페이지](../another/)

---
### Sources
- [공식 문서 제목](URL)
```

### `/plugins/*` 템플릿

```markdown
---
title: "moai-XXX — 한 줄 정체성"
weight: NN
description: "..."
---

# moai-XXX

> 한 줄 정체성 + 대표 사용처

## 무엇을 하는 플러그인인가
(2-3 문단)

## 설치
{{< tabs "install" >}}
{{< tab "마켓플레이스 (권장)" >}}
1. `/plugin marketplace add modu-ai/cowork-plugins`
2. `/plugin install moai-XXX`
{{< /tab >}}
{{< tab "수동" >}}
GitHub 저장소 클론 후 `~/.claude/plugins/`에 배치
{{< /tab >}}
{{< /tabs >}}

## 핵심 스킬
| 스킬 | 용도 | 자동 호출 트리거 |
|---|---|---|
| `skill-name` | ... | "예시 요청문" |

## 빠른 사용 예
(자연어 요청문 1-2개 + 예상 산출물 한 줄)

## 대표 체인
- `skill-A → skill-B → ai-slop-reviewer`

## API 키 (필요한 경우)
| 변수 | 용도 | 발급처 |
|---|---|---|

## 다음 단계
- [관련 쿡북](../../cookbook/...)

---
### Sources
- [GitHub 저장소](https://github.com/modu-ai/cowork-plugins/tree/main/moai-XXX)
```

### `/cookbook/*` 템플릿

```markdown
---
title: "..."
weight: NN
description: "..."
---

# 한국어 제목

> 시나리오 한 줄 요약

## 대상 독자

## 사전 준비
- 설치된 플러그인: ...
- 필요한 API 키: ...

## 스킬 체인
```
skill-A → skill-B → moai:ai-slop-reviewer
```

## 단계별 실행

### 1. ...
프롬프트 예시:
```
(복붙 가능한 자연어 요청)
```
예상 산출물: ...

### 2. ...

## 산출물 점검 체크리스트
- [ ] ...
- [ ] AI 슬롭 검수 통과

## 자주 겪는 이슈

## 응용 변형

---
### Sources
- ...
```

## 6. 작업 절차

각 MDX 파일에 대해:

1. `Read` 도구로 MDX 원본을 처음부터 끝까지 읽는다
2. **발췌**: 본문에서 사실(facts)·예시·체인·인용을 추출. AI 슬롭 표현, 중복, 마케팅 톤은 버림
3. **재구성**: 위 템플릿에 맞춰 한국어 경어체로 재서술. 출처 URL은 Sources에 보존
4. Geekdoc 숏코드 적용 — Nextra import 라인 제거, `<Callout>`/`<Tabs>`/`<Steps>` 변환
5. `Write` 도구로 출력 경로에 저장
6. 다음 파일로

## 7. 절대 규칙 (HARD)

- 새 정보 **창작 금지** — 원본에 없는 사실은 추가하지 않음. 보강 필요한 자리는 `<!-- TODO: 보강 -->` 주석으로 남김
- 모든 외부 링크는 원본 그대로 유지(URL은 그대로 옮김)
- 한국어 경어체 일관성 (`~합니다`, `~입니다`)
- 코드 블록은 언어 명시
- weight 값 누락 금지 (사이드바 정렬용)
- 한 페이지당 H1(`#`)은 정확히 1개

## 8. 출력 후 자가 점검

- [ ] front matter 4필드(title, weight, description, geekdocBreadcrumb) 채움
- [ ] H1 한 개
- [ ] Sources 섹션 존재(원본에 출처가 있었던 경우)
- [ ] Nextra import 라인이 본문에 남아있지 않음
- [ ] 깨진 인라인 JSX 토큰(`<Tab>`, `<Card>` 등) 없음
