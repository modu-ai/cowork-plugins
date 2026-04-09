---
name: process-manager
description: >
  프로세스 관리 — 운영 매뉴얼, 조달 문서, SOP 작성, 회의 전략 하네스. 업무 프로세스, 운영 규정, 워크플로우 설계, 구매 요청서, 발주서, 벤더 평가, 표준 운영 절차, 회의록 작성.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# 프로세스 관리자 (process-manager)

> moai-operations v1.0.0 | 4 하네스

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| operations-manual | 운영 매뉴얼 | 업무 프로세스, 운영 규정, 워크플로우 설계 |
| procurement-docs | 조달 문서 | 구매 요청서, 발주서, 벤더 평가 |
| sop-writer | SOP 작성 | 표준 운영 절차, 매뉴얼, 가이드라인 |
| meeting-strategist | 회의 전략가 | 회의록 작성, 안건 관리, 후속 조치 |

→ 하네스 파일: `references/{id}.md`

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 프로세스 설계 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

## 트리거 키워드

프로세스, 운영 매뉴얼, 업무 절차, SOP, 조달, 구매, 발주, 회의록, 안건, 워크플로우
