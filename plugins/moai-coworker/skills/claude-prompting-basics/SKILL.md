---
name: claude-prompting-basics
description: 비개발자를 위한 Claude 대화 모범 사례 — 명확한 지시, 맥락 제공, 예시 활용, XML 태그 구조화. Claude 공식 프롬프트 엔지니어링 가이드 기반. "Claude한테 어떻게 물어봐야 잘 답해줘?" 질문에 즉시 활용.
version: "1.0.0"
metadata:
  category: cowork
  status: active
  updated: 2026-07-09
  tags: "prompting, claude, beginner, non-dev"
  source: "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices"
---

# claude-prompting-basics — 비개발자용 Claude 대화 가이드

> cowork 플러그인 스킬 — `skills/` 카테고리만 사용 (commands/·agents/ 없음).

## 핵심 6원칙 (Claude 공식)

1. **명확하고 직접적으로** — Claude를 '맥락 없는 똑똑한 새 동료'로 대해. 원하는 출력 형식·제약을 직접 명시. "도움말 만들어줘" (X) → "초보용 5단계 설치 도움말, 단계당 2문장, 이모지 1개" (O).
2. **맥락·동기 추가** — *왜* 중요한지 설명하면 Claude가 올바르게 일반화. "소리 내어 읽을 거니 줄임표 금지" > "줄임표 금지".
3. **예시로 보여주기 (multishot)** — 3–5개 잘 만든 예시가 형식·톤·구조를 가장 안정적으로 유도. `<example>` 태그로 감싸. 긍정 예시가 부정 지시보다 강하다.
4. **XML 태그로 구조화** — 혼합 프롬프트는 `<instructions>`, `<context>`, `<input>`, `<output_format>` 태그로 나누면 Claude가 헷갈리지 않음.
5. **역할 부여** — 시스템 프롬프트에 한 문장 역할("너는 10년 차 카피라이터야")로 톤·행동 집중.
6. **긴 자료는 상단에** — 20k+ 토큰 입력은 데이터를 **상단**에, 질문·지시는 **하단**에 배치 (품질 ~30% 향상).

## 비개발자 실전 치트키

| 이런 요청은 | 이렇게 바꾸세요 |
|---|---|
| "글 써줘" | "50대 주부 대상 건강보험 블로그 글, 3문단, 핵심 혜택 1개" |
| "잘 만들어줘" (모호) | 원하는 형식의 예시 1개를 직접 보여주기 |
| "~하지 마" (부정) | "~하게 써" (긍정) — 부정 지시는 잘 안 지켜짐 |
| "더 좋게" (평가어) | 구체 기준("초등 5학년이 이해 가능하게, 문장당 25자 이내") |

## 자주 묻는 질문

**Q: Claude가 너무 길게 써요**
→ 출력 형식 명시: "3문단, 문장당 25자 이내" 또는 "한 슬라이드당 핵심 1줄".

**Q: 내 뉘앙스가 안 살아요**
→ 역할 + 예시 2–3개 제공. "이런 톤으로: [예시1] [예시2]".

**Q: 거짓말(할루시네이션)해요**
→ "모르면 모른다고 해. 추측하지 마" + 확인 가능한 출처 요청.

## 참고

- Claude 공식 프롬프트 엔지니어링 가이드: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- 본 스킬은 `/harness:plugin` 하네스(skill-builder)가 Claude 공식 문서 기반으로 생성한 cowork 플러그인 스킬입니다.
