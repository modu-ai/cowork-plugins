---
name: wellness-coach
description: >
  웰니스 코치 — 운동 프로그램, 식단 플래너, 육아 가이드, 시니어 케어 하네스. 운동, 다이어트, 식단, 피트니스, 육아, 노인 돌봄.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 웰니스 코치 (Wellness Coach)

> moai-lifestyle | 건강/육아 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| fitness-program | 운동 프로그램 | 운동 계획, 루틴 설계, 진도 관리 |
| meal-planner | 식단 플래너 | 영양 균형, 식단 구성, 장보기 리스트 |
| parenting-guide | 육아 가이드 | 아이 발달, 교육 전략, 학교 준비 |
| elderly-care-planning | 시니어 케어 | 노인 돌봄 계획, 복지 서비스, 건강 관리 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

운동, 다이어트, 식단, 피트니스, 건강, 루틴, 영양, 육아, 아이, 시니어, 노인 케어, 웰니스

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 의사결정 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
