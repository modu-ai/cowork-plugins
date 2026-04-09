---
name: investor-relations
description: >
  투자자 관계 관리 — 투자자 보고서, 재무 모델 하네스. IR 자료, 피칭 덱, 투자 유치, 매출 예측, 손익분석, 현금흐름.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 투자자 관계 (Investor Relations)

> moai-business | IR 및 재무 모델 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| investor-report | 투자자 보고서 | IR 자료, 피칭 덱, 투자 유치 전략 |
| financial-modeler | 재무 모델 | 매출 예측, 손익분석, 현금흐름 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

투자, IR, 피칭, 투자자 보고서, 재무모델, 매출 예측, 손익분석, 현금흐름, 밸류에이션, 시리즈 A, 투자 유치

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. 복잡 재무 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
