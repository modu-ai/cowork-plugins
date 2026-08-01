---
title: "모범 사례"
weight: 101
---

# 모범 사례

## CLAUDE.md 최적화

명확하고 구체적인 규칙을 적으세요:
```markdown
- 커밋 전 npm test 실행
- 한국어 주석
- src/ 아래에만 코드
```

## Claude를 협력자로

- **구체적으로 물어보기** — "개선해줘"보다 "이 함수의 중복 로직 빼줘"
- **맥락 주기** — 목적·제약을 함께 설명
- **결과 검증** — Claude의 출력을 직접 확인

## 4단계 워크플로우

Explore → Plan → Implement → Commit. 한 번에 끝내려 하지 말고 단계별로.

## 컨텍스트 관리

- `/compact` — 대화 유지하며 분량 축소
- `/clear` — 새 시작이 필요할 때

## 훅으로 자동화

반복 작업(포맷팅 등)은 훅으로 자동화하세요.

## Sources

- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code: Best practices for agentic coding (Boris Cherny)](https://www.anthropic.com/engineering)
