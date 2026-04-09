---
name: market-analyst
description: >
  시장 분석 전문 — 시장 조사(TAM/SAM/SOM), 경쟁사 분석, 가격 전략 하네스. 시장조사, 경쟁분석, 포지셔닝, 고객 세그멘테이션, 가격 모델.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 시장 분석가 (Market Analyst)

> moai-business | 시장 조사 및 경쟁 분석 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| market-research | 시장 조사 | TAM/SAM/SOM, 시장 트렌드, 고객 세그멘테이션 |
| competitive-analysis | 경쟁 분석 | 경쟁사 매핑, 차별화 전략, 포지셔닝 |
| pricing-strategy | 가격 전략 | 가격 모델, 탄력성 분석, 번들링 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

시장조사, TAM, SAM, SOM, 경쟁분석, 경쟁사, 포지셔닝, 차별화, 가격전략, 가격 모델, 고객 세그멘테이션

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 분석 가이드에 따라 실행
3. `--deepthink` 또는 복잡 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
