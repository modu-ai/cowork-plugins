---
title: "비용·사용량"
weight: 99
---

# 비용·사용량

## 과금

- **Pro/Max 구독** — claude.ai와 사용량 한도를 **공유**합니다. claude.ai에서 대화하면 Code 사용량도 같이 줄어듭니다 (같은 쿼터에서 차감).
- **API 키** — 토큰당 종량 과금.

## `/cost`

세션 비용을 실시간으로 확인합니다. 세션 누적 비용과 토큰 수를 보여줍니다.

## 절감 팁

- 모델/effort를 작업에 맞게 선택 (단순 작업은 Sonnet/Haiku)
- `/compact`로 컨텍스트 압축
- prompt caching 활용 (API 사용 시)

## API 과금 상세

API 키 사용 시 입력·출력 토큰 단가가 다릅니다. prompt caching으로 반복 프롬프트 비용을 크게 줄일 수 있습니다.

## Sources

- [Costs](https://code.claude.com/docs/en/costs)
- [How do usage and length limits work?](https://support.claude.com/en/articles/11647753)
