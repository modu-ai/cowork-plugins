---
name: strategy-planner
description: >
  비즈니스 전략 기획 — 스타트업 런처, 비즈니스 모델 캔버스, 신시장 진출, 시나리오 플래닝, 전략 프레임워크 하네스. 사업계획서, 창업, 스타트업, 린 캔버스, MVP, SWOT, OKR, Blue Ocean.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 전략 플래너 (Strategy Planner)

> moai-business | 전략 기획 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| startup-launcher | 스타트업 런처 | 사업계획서, 린 캔버스, MVP 전략 |
| business-model-canvas | 비즈니스 모델 캔버스 | 9블록 캔버스, 가치 제안 설계 |
| market-entry-strategy | 신시장 진출 전략 | 해외 진출, 시장 진입 장벽, 파트너 전략 |
| scenario-planner | 시나리오 플래닝 | 미래 시나리오 분석, 불확실성 대응 |
| strategy-framework | 전략 프레임워크 | SWOT, Porter's 5F, Blue Ocean, OKR |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

사업계획서, 창업, 스타트업, 린 캔버스, MVP, 비즈니스 모델, SWOT, OKR, Blue Ocean, 전략, 시나리오, 신시장 진출, 해외 진출

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 전략 판단 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
