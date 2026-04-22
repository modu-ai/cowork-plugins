---
title: "프로젝트와 메모리"
weight: 50
description: "프로젝트로 대화 맥락을 묶고, 메모리로 반복 입력을 줄이는 Cowork의 컨텍스트 관리 방식을 설명합니다."
geekdocBreadcrumb: true
---

# 프로젝트와 메모리

> Cowork는 대화를 프로젝트로 묶고, 대화 사이에 걸쳐 유지해야 할 정보를 메모리에 저장합니다.

## 프로젝트

프로젝트는 "같은 맥락을 공유하는 대화 묶음"입니다. 각 프로젝트는 다음을 격리해서 관리합니다.

- 전용 작업 폴더
- 해당 폴더 안의 `CLAUDE.md` (프로젝트 작업 지침)
- 프로젝트 범위의 메모리
- 필요한 플러그인·커넥터 구성

한 프로젝트 안에서는 Cowork가 과거 대화의 핵심 사실을 자동으로 기억해, 매번 같은 맥락을 다시 입력하지 않아도 됩니다.

## 메모리

메모리는 `./memory/` 경로 아래 파일로 저장됩니다. 대화가 끝나도 남아, 같은 프로젝트의 다음 대화에서 자동으로 불러옵니다.

### 4가지 메모리 종류

- **user** — 사용자의 역할·선호·전문성 (예: "한국 스타트업 CFO, K-IFRS 익숙")
- **feedback** — "이렇게 해달라/하지 말아달라" 지침 (규칙 + 이유 + 적용 조건)
- **project** — 진행 중 일·이해관계자·마감일
- **reference** — 외부 시스템 위치 (예: "이슈는 Linear INGEST 프로젝트")

### 저장하지 않는 것

- 이미 코드·문서·커밋 로그로 복원 가능한 사실
- 일회성 대화 맥락
- 민감 정보(주민번호·계좌번호·비밀번호)

## 가져오기·내보내기

대화에 포함된 메모리는 설정에서 내보내기로 백업하고, 다른 프로젝트에 가져오기로 옮길 수 있습니다.

## 다음 단계

- [스킬 사용법](../skills/)
- [플러그인 사용](../plugins/)

---

### Sources

- [Organize your tasks with projects in Claude Cowork](https://support.claude.com/en/articles/14116274)
- [Import and export your memory from Claude](https://support.claude.com/en/articles/12123587)
