---
title: "Chat·Cowork·Design과의 차이"
weight: 91
---

# Chat·Cowork·Design과의 차이

Claude의 네 제품은 각기 다른 일을 합니다.

## 네 제품 비교

| 제품 | 주요 용도 | 입력 | 출력 | 파일 접근 |
|------|----------|------|------|-----------|
| Chat | 대화 Q&A | 텍스트 | 대화 | 없음 |
| Cowork | 지식작업 자율 실행 | 결과물 설명 | Office 파일 | 폴더 범위 |
| Design | 디자인 생성 | 디자인 설명 | 디자인 산출물 | 제한 |
| Code | 코드 작업 | 코드 요청 | 코드 변경 | 코드베이스 |

## Code만의 특징 — 에이전트 루프

Code는 **읽기 → 추론 → 도구호출 → 관찰**을 반복하며 자율으로 작동합니다. 예: "이 버그 고쳐줘"라고 하면, 코드를 읽고 원인을 추론하고 파일을 편집한 뒤 결과를 보여줍니다.

## 언제 Code를 쓰나요

- 코드베이스를 이해하거나 설명받을 때
- 버그를 찾고 고칠 때
- 테스트·문서를 작성할 때
- Git 커밋·PR을 자동화할 때

## Sources

- [Claude Code 개요 (KO)](https://code.claude.com/docs/ko/overview)
- [Common workflows](https://code.claude.com/docs/en/common-workflows)
