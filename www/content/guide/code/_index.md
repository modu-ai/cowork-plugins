---
title: "Code"
weight: 40
description: "Claude Code — AI와 함께 코딩하는 새로운 방법. 처음 시작하는 분을 위한 한국어 가이드."
geekdocBreadcrumb: false
geekdocCollapseSection: false
aliases: ["/code/"]
---

## Claude Code란? — "코딩 어시스턴트" 같은 개념

Claude Code는 Claude와 함께 직접 코드를 작성하고 실행할 수 있는 환경입니다. 코드를 입력하면 Claude가 파일을 읽고, 수정하고, 결과를 보여줍니다.

### 누가 쓰나요?

- 개발자 — 기존 프로젝트 구조를 유지하면서 빠르게 기능 추가
- 스타트업 프로덕션팀 — 작은 스크립트부터 풀스택 서비스까지 빠르게 만들기
- 초보자 — "이 버튼을 누르면 동작하게 해 줄 수 있나요?" 수준의 자연어로 요청 가능
- 마이그레이션 담당자 — 기존 코드를 한 프레임워크에서 다른 프레임워크로 변환

### 뭘 만들 수 있나요?

| 만들기 | 예시 |
|---|---|
| 웹 사이트 | React/Next.js 프로젝트, 랜딩 페이지 |
| 백엔드 서비스 | Python FastAPI, Node.js Express 서버 |
| 모바일 앱 | React Native, Flutter 앱 |
| CLI 도구 | Go, Python 커맨드라인 도구 |
| 데이터 처리 | Python 데이터 분석 스크립트 |

## Claude Code 작동 흐름

```mermaid
flowchart LR
   A["사용자<br/>요청을 입력"] --> B["Claude Code<br/>프로젝트 파일 읽음"]
   B --> C["Claude<br/>변경사항 제안"]
   C --> D["사용자<br/>결과 확인"]
   D --> E["로컬에서<br/>테스트 실행"]

   style A fill:#e6e6e6,stroke:#757575,color:#09110f
   style C fill:#fbf0dc,stroke:#c47b2a,color:#09110f
   style E fill:#d6e7de,stroke:#3d7d5f,color:#09110f
```

사용자가 자연스러운 언어로 요청하면 Claude Code는 프로젝트의 파일을 읽고, 필요한 변경사항을 자동으로 적용합니다. 결과는 로컬 환경에서 바로 테스트할 수 있습니다.

## 시작하기

다음 단계로 진행하세요:

1. **[설치하기](./install.md)** — Claude Code를 설치하고 시작하는 방법
2. **[첫 작업 실행](./first-task.md)** — 첫 번째 프로젝트 생성해 보기
3. **[주요 기능 살펴보기](../chat/features.md)** — Claude와 대화하는 방법 (기본 패턴은 같습니다)

## 핵심 특징

| 특징 | 설명 |
|---|---|
| 자동 파일 탐색 | 프로젝트 구조를 자동으로 이해 |
| 로컬 실행 | 변경사항을 로컬 컴퓨터에서 즉시 테스트 |
| 기존 코드 존중 | 브랜딩, 폴더 구조, 코딩 규칙 자동 감지 및 유지 |
| 자연어 지시 | "이 함수를 더 빠르게" 같은 자연어로도 동작 |

---

### 다음 페이지

- **[설치하기](./install.md)** — 설치 방법 (macOS / Windows)
