---
title: "메모리 — CLAUDE.md"
weight: 94
---

# 메모리 — CLAUDE.md

`CLAUDE.md`는 프로젝트의 **"규칙 노트"** — Claude가 매 세션마다 자동으로 읽는 지속 지침 파일입니다.

## 예시

```markdown
# 이 프로젝트

- 한국어 쇼핑몰 백엔드 (Node.js + Express)
- 커밋 전 반드시 테스트 실행 (npm test)
- src/ 아래에만 코드 작성
```

## 계층

- **루트 CLAUDE.md** — 프로젝트 전체 규칙
- **하위 디렉토리 CLAUDE.md** — 해당 디렉토리 국소 규칙
- **전역 `~/.claude/CLAUDE.md`** — 모든 프로젝트에 적용되는 개인 규칙

## 어떻게 만들나요

- `/init`으로 자동 생성 (코드베이스를 읽고 초안 작성)
- 또는 직접 텍스트 파일로 작성

## 무엇을 적나요

- 프로젝트 개요·목적
- 코딩/실행 규칙
- 디렉토리 구조 설명
- 자주 쓰는 명령

## Sources

- [Memory (CLAUDE.md)](https://code.claude.com/docs/en/memory)
- [Best practices](https://code.claude.com/docs/en/best-practices)
