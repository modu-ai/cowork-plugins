---
name: spec-writer
description: >
  스펙 작성 — PRD, 기능 명세, AI 전략, 정부 지원금 기획 하네스. 프로덕트 매니저, 기능 명세서, 로드맵, AI/ML 전략, R&D, SBIR.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 스펙 작성 (Spec Writer)

> moai-product | 제품 명세 및 전략 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| product-manager | 프로덕트 매니저 | PRD, 기능 명세, 우선순위 결정, 로드맵 |
| ai-strategy | AI 전략 | AI/ML 도입 전략, 디지털 전환 로드맵 |
| gov-funding-plan | 정부 지원금 기획 | R&D 과제, SBIR/STTR, 정부 사업 신청 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

PRD, 기능명세, 스펙, 제품 기획, AI 전략, 디지털전환, 정부 지원금, R&D, 과제 신청, 프로덕트 매니저

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 전략 판단 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
