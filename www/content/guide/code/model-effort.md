---
title: "모델·사고 레벨"
weight: 96
---

# 모델·사고 레벨

## 모델

- **Opus** — 가장 똑똑, 비용 높음
- **Sonnet** — 균형
- **Haiku** — 빠르고 저렴

`/model`로 전환합니다.

## 작업별 추천

| 작업 유형 | 추천 모델 / effort |
|-----------|-------------------|
| 단순 버그·질문 | Sonnet / medium |
| 복잡한 설계·추론 | Opus / high |
| 빠른 반복 작업 | Haiku / low |

## effort (사고 깊이)

`low` / `medium` / `high` / `max` — 복잡할수록 높게.

## 비용 절감

단순 작업은 Haiku/Sonnet + low effort로 비용을 크게 줄일 수 있습니다. `/model`로 상황마다 바꿔 쓰세요.

## adaptive thinking

Opus 4.7+는 사고 토큰을 스스로 할당합니다. 고정 토큰 예산을 직접 지정하지 않습니다.

## Sources

- [Settings](https://code.claude.com/docs/en/settings)
- [Costs](https://code.claude.com/docs/en/costs)
