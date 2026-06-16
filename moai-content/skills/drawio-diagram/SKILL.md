---
name: drawio-diagram
description: |
  자연어 설명을 편집 가능한 draw.io(.drawio) 다이어그램으로 만들고, 설치 없이 브라우저에서 바로 열리는 단일 HTML로 렌더해 드립니다. ERD·UML 클래스·시퀀스·아키텍처·ML 파이프라인·플로우차트를 mermaid보다 풍부한 셰이프·레이아웃·클라우드 아이콘으로 그립니다.
  다음과 같은 요청 시 사용하세요:
  - "이 시스템 아키텍처 draw.io 다이어그램으로 그려줘"
  - "ERD / 클래스 다이어그램 / 시퀀스 다이어그램 만들어줘"
  - "이 흐름을 편집 가능한 다이어그램으로 그려서 HTML로 보여줘"
  - "mermaid로는 부족한 정교한 도식이 필요해"
  - "AWS / 클라우드 아키텍처 도식 그려줘"
  - "학습용으로 개념 구조도를 편집 가능한 그림으로 만들어줘"
  .drawio XML(편집용) + draw.io CDN 뷰어를 임베드한 단일 HTML(즉시 열람)을 함께 산출합니다. 로컬 설치 불필요. moai-content:html-report의 design-token·폰트를 공유하고, moai-tutor:learning-material에서 mermaid 보완용으로 조건부 임베드됩니다.
  [책임 경계] vs mermaid: 빠른 텍스트 기반 플로우·시퀀스는 mermaid, 정교한 셰이프·클라우드 아이콘·편집 가능한 산출물이 필요하면 이 스킬.
user-invocable: true
version: 2.21.0
---

# drawio-diagram — 편집 가능한 draw.io 다이어그램 렌더러

## 개요

`moai-content:drawio-diagram`은 자연어 설명(또는 구조화된 명세)을 받아 **두 가지 산출물**을 만든다.

1. **`.drawio` 파일** — draw.io 웹/데스크톱에서 그대로 열어 추가 편집 가능한 mxGraph XML
2. **단일 `.html` 파일** — draw.io CDN 뷰어(`viewer-static.min.js`, Apache-2.0)를 임베드해 **설치 없이 브라우저에서 즉시** 도식을 보여주는 자체 완결형 HTML

mermaid가 텍스트→자동 레이아웃으로 빠른 플로우·시퀀스에 강하다면, 이 스킬은 **정교한 셰이프·수동 레이아웃·클라우드 아이콘·편집 가능한 원본**이 필요할 때 쓴다. html-report/learning-material의 디자인 토큰·폰트를 공유해 Cowork 산출물 전반과 시각 일관성을 유지한다.

> **렌더링 철학**: 원본 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)(MIT)은 PNG export에 draw.io 데스크톱 CLI 설치가 필요하다. 이 스킬은 **CLI 의존을 제거**하고 `.drawio` XML을 브라우저 CDN 뷰어로 렌더한다 — Cowork 관리 환경에서 추가 설치 없이 동작한다. 자세한 출처·라이선스는 아래 §출처·라이선스 참조.

## 트리거 키워드

draw.io, drawio, 다이어그램, 도식, 아키텍처, ERD, 클래스 다이어그램, 시퀀스 다이어그램, 플로우차트, UML, 구조도, 시스템도, 편집 가능한 그림, 클라우드 아키텍처

## 입력

| 인자 | 필수 | 설명 |
|------|------|------|
| `description` | ✓ | 그릴 내용의 자연어 설명 또는 구조화된 명세(노드·관계·그룹) |
| `preset` | — | `erd` \| `uml-class` \| `sequence` \| `architecture` \| `ml-pipeline` \| `flowchart` (생략 시 내용으로 자동 판별) |
| `topic` | — | 제목·파일명에 사용 |
| `output_path` | — | 기본값 `<cwd>/diagrams/<slug>-<YYYYMMDD>.html` (`.drawio`는 같은 경로에 동시 생성) |

## 6개 프리셋

각 프리셋은 셰이프·레이아웃·시맨틱 색상 규칙을 정의한다. 상세 mxGraph XML 패턴은 [`references/presets.md`](references/presets.md)가 단일 진실(SSOT)이다.

| 프리셋 | 용도 | 핵심 셰이프 |
|--------|------|-------------|
| `erd` | 엔티티-관계 (DB 스키마) | 테이블 셰이프, PK/FK 행, 1:N 관계 엣지 |
| `uml-class` | 클래스 다이어그램 | 3-구획 클래스 박스(이름·속성·메서드), 상속·연관 |
| `sequence` | 시퀀스 (상호작용) | 라이프라인, 활성 막대, 동기/비동기 메시지 |
| `architecture` | 시스템·클라우드 아키텍처 | 그룹 컨테이너, 컴포넌트, 클라우드 셰이프 라이브러리 |
| `ml-pipeline` | ML/딥러닝 파이프라인 | 데이터·전처리·모델·평가 스테이지 흐름 |
| `flowchart` | 프로세스 플로우차트 | 시작/끝, 처리, 판단 다이아몬드, 분기 |

## 산출물

`<cwd>/diagrams/` 아래에 **두 파일**을 같은 slug로 생성한다.

- `<slug>-<YYYYMMDD>.drawio` — 편집용 원본 (draw.io에서 열기)
- `<slug>-<YYYYMMDD>.html` — 브라우저 즉시 열람용 (CDN 뷰어 임베드)

HTML은 자체 완결형이며 html-report 디자인 토큰을 공유한다(헤더·캡션·출처). 뷰어 임베드 규격·단일 HTML 래퍼·폴백은 [`references/cdn-viewer.md`](references/cdn-viewer.md) 참조.

## 작성 워크플로우

1. **이해** — 설명에서 노드·관계·그룹·계층을 추출. 모호하면 가정을 명시하고 진행.
2. **프리셋 선택** — 내용 성격으로 6 프리셋 중 선택(또는 사용자 지정).
3. **mxGraph XML 생성** — `references/presets.md` 패턴으로 `.drawio` XML 작성. 그리드 10px 정렬, 시맨틱 색상(html-report 팔레트) 적용.
4. **self-check** — 아래 규칙으로 구조 자가 점검 후 보정(최대 2회).
5. **HTML 렌더** — `.drawio` XML을 `references/cdn-viewer.md`의 단일 HTML 래퍼에 임베드.
6. **산출** — 두 파일 경로와 사용한 프리셋·뷰어 출처를 명시.

## self-check (구조 자가 점검)

PNG를 읽는 원본 방식 대신, **XML 구조**를 점검한다(브라우저 렌더 전 결함 예방).

- [ ] 모든 엣지의 `source`/`target`이 존재하는 `mxCell id`를 가리키는가 (dangling 엣지 0)
- [ ] 노드 `mxGeometry`가 겹치지 않는가 (같은 좌표·박스 중첩 검사)
- [ ] 라벨이 박스 폭을 넘지 않는가 (긴 라벨은 폭 확대 또는 줄바꿈)
- [ ] 그리드 10px 배수로 정렬됐는가 (`x`,`y`,`width`,`height`)
- [ ] 시맨틱 색상이 일관적인가 (같은 역할=같은 색)
- [ ] 루트 `mxCell id="0"`, `id="1"`(레이어)이 존재하고 모든 노드의 `parent`가 유효한가

결함 발견 시 좌표·폭·색상을 보정해 재생성한다. 2회 보정 후에도 남는 구조 문제는 자료에 "확인 필요"로 표기한다.

## 사용 예시

**예시 1**: "결제 시스템 마이크로서비스 아키텍처 draw.io로 그려줘"
→ `architecture` 프리셋. 그룹 컨테이너(게이트웨이·서비스·DB) + 컴포넌트 + 관계 엣지. `.drawio` + 단일 HTML 산출.

**예시 2**: "User-Order-Product ERD 만들어줘"
→ `erd` 프리셋. 3 테이블 셰이프(PK/FK 행) + 1:N 관계. 편집 가능한 `.drawio` 동시 생성.

**예시 3**: "트랜스포머 학습 파이프라인을 학습자료에 넣을 도식으로"
→ `ml-pipeline` 프리셋. learning-material이 `drawio` 블록으로 같은 HTML에 임베드(§관련 스킬).

## 주의사항

- **CDN URL은 references/cdn-viewer.md를 인용** — 임의 버전·경로를 지어내지 않는다.
- **존재하는 셰이프만 사용** — mxGraph 표준 스타일·검증된 셰이프 라이브러리만. 불확실한 스텐실 이름을 추측하지 않는다(빈 박스 방지). 미확인 셰이프는 표준 사각형으로 폴백.
- **폴백 보장** — 뷰어가 차단·실패해도 `.drawio` XML이 `<details>` 안에 텍스트로 보존돼 정보 손실 0.
- **접근성** — 도식에 제목·캡션·대체 설명을 제공. 색상에만 의존하는 구분 금지(라벨 병행).
- **편집은 사용자 몫** — `.drawio`는 draw.io 웹(app.diagrams.net)/데스크톱에서 추가 편집. 이 스킬은 초안·렌더까지.

## 관련 스킬

- **moai-content:html-report** — 디자인 토큰·폰트 SSOT(`references/design-tokens.md`·`references/fonts.md`)를 공유한다.
- **moai-tutor:learning-material** — 학습자료에 mermaid 보완용으로 이 스킬의 `.drawio` 도식을 조건부 임베드한다(`references/cdn-libraries.md`의 drawio 행).
- **보완 관계 vs mermaid** — 빠른 텍스트 플로우·시퀀스는 mermaid, 정교한 셰이프·편집 가능 원본은 이 스킬.

## 이 스킬을 사용하지 말아야 할 때

- **빠른 텍스트 기반 플로우·시퀀스·간단 ER** → mermaid(learning-material/html-report explainer)로 충분
- **데이터 수치 차트** → `moai-data:data-visualizer` 또는 ECharts
- **0-JS 업무 보고서** → `moai-content:html-report`
- **발표 슬라이드** → `moai-office:pptx-designer`

## 출처·라이선스

- **영감 출처**: [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) — MIT License, © 2026 Agents365-ai. 6 프리셋 구성·셰이프 해상·코드베이스 시각화 개념을 참고해 MoAI-Cowork 환경(CDN 뷰어·html-report 토큰 공유)에 맞게 재구현했다. MIT 라이선스 고지를 보존한다.
- **렌더 뷰어**: draw.io `viewer-static.min.js` — Apache-2.0. CDN 런타임 로딩(브라우저가 직접 로드)으로, 저장소 NC-ND 라이선스와 무관하다.
- **재구현 범위**: 본 스킬의 SKILL.md·presets.md·cdn-viewer.md 본문은 MoAI 자체 저작이며, 원본 코드를 그대로 복사하지 않았다. opt-in 코드베이스 시각화(`references/codebase-viz.md`)는 원본 스크립트 접근을 더 직접적으로 참조하므로 해당 문서에 별도 attribution을 둔다.
