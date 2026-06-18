# moai-tutor

학습자·수강생 전용 **개인 AI 튜터** — 내 학습 프로젝트를 직접 만들고, 질문하면 최신 정보를 병렬로 조사해, 도식·차트·수식·코드가 들어간 HTML 학습자료를 자동으로 만들어 줍니다.

[![버전](https://img.shields.io/badge/version-2.20.0-blue)](../CHANGELOG.md)
[![라이선스](https://img.shields.io/badge/license-NC--ND--1.0-blue)](../LICENSE)
[![스킬](https://img.shields.io/badge/skills-3-success)](#스킬)

claude code·claude cowork 사용법, 영어, 프로그래밍 개념 등 **어떤 주제든** 스스로 깊이 학습할 수 있게 돕습니다. moai-education이 가르치는 사람(강사·교수·교사)을 위한 도구라면, moai-tutor는 **배우는 사람**을 위한 도구입니다.

> **설계 노트**: 코디네이터 에이전트(agent) 없이 스킬 직접 호출 전용 플러그인입니다 — `/learning-project`·`/tutor-research`·`/learning-material` 또는 자연어로 바로 사용하세요. 학습자가 단계별로 능동적으로 학습하도록 설계됐습니다 (코디네이터 부재는 의도적).

## 스킬

| 스킬 | 설명 | 상태 |
|------|------|:----:|
| [learning-project](./skills/learning-project/) | 내 학습 프로젝트 초기화 — 학습 목표·수준 진단, 단계별 로드맵, 진도 추적, 학습 전용 CLAUDE.md 자동 생성 | ✅ |
| [tutor-research](./skills/tutor-research/) | 질문 → context7(공식 문서) + 웹검색(최신 정보)을 **병렬**로 조사·교차검증해 신뢰할 수 있는 학습 근거를 종합 | ✅ |
| [learning-material](./skills/learning-material/) | 리서치 종합 → 학습목표·핵심개념·도식·예제·복습으로 구조화한 **단일 HTML 학습자료** 생성. mermaid·ECharts·KaTeX·highlight.js·AOS 조건부 로딩 | ✅ |

## 사용 예시

```
claude code 서브에이전트 공부할 학습 프로젝트 만들어줘. 입문 수준이고 하루 1시간.
```
→ `learning-project`

```
claude cowork의 Skills와 Sub-agents 차이를 최신 정보로 조사해서 알려줘
```
→ `tutor-research`

```
방금 조사한 내용으로 도식이랑 예제 들어간 HTML 학습자료 만들어줘
```
→ `learning-material`

```
영어 가정법 과거완료, 도표와 예문으로 정리한 학습자료로 만들어줘
```
→ `tutor-research` → `learning-material`

## 주요 워크플로우 체인

```
개인 학습 풀 사이클
  learning-project(로드맵·CLAUDE.md)
    ↓ (학습 중 궁금한 점이 생길 때마다)
  tutor-research(context7 + 웹검색 병렬 조사)
    ↓
  learning-material(도식·차트·코드 HTML 학습자료)
    ↓ (반복 — 로드맵의 다음 단계로)
  learning-project 진도 갱신

단발성 학습자료
  tutor-research(주제 조사) → learning-material(HTML)

코드·라이브러리 학습
  tutor-research(context7 공식 문서 중심) → learning-material(코드 하이라이트 + 시퀀스 도식)
```

## 다른 플러그인과의 경계

| 비슷해 보이지만 다른 영역 | 사용해야 할 스킬 |
|---|---|
| 강사가 만드는 강의 커리큘럼·학습 목표 설계 | `moai-education:curriculum-designer` |
| 시험·평가 문제 출제 | `moai-education:assessment-creator` |
| 학술 논문·문헌 검토 리서치 | `moai-education:research-assistant` |
| 업무용 보고서를 0-JS 단일 HTML로 렌더 | `moai-content:html-report` |
| 내 학습용 프로젝트·로드맵 만들기 | `learning-project` (이 플러그인) |
| 학습 질문을 최신 정보로 병렬 조사 | `tutor-research` (이 플러그인) |
| 도식·차트가 들어간 학습자료 HTML | `learning-material` (이 플러그인) |

## MCP·CDN 라이브러리

- **context7 MCP**: `tutor-research`의 공식 문서 조회 축. 플러그인에 번들(`.mcp.json`)되어 설치 시 함께 활성화됩니다. 별도 API 키가 필요 없습니다.
- **웹검색**: `tutor-research`의 최신 정보 축. Claude의 기본 WebSearch 도구를 사용합니다.
- **CDN 라이브러리 스택**: `learning-material`이 생성하는 HTML은 콘텐츠가 실제로 쓸 때만 라이브러리를 주입합니다(조건부 로딩). 큐레이션 목록·CDN URL·로딩 규칙은 [references/cdn-libraries.md](./skills/learning-material/references/cdn-libraries.md) 참조.

## 설치

Settings > Plugins > cowork-plugins에서 `moai-tutor` 선택

## 참고자료

- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
