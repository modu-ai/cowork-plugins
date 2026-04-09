---
name: event-planner
description: >
  이벤트 플래너 — 행사 기획, 웨딩 플래너, 세미나, 워크샵, 컨퍼런스 하네스. 이벤트, 결혼, 웨딩, 행사 기획, 워크샵.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 이벤트 플래너 (Event Planner)

> moai-lifestyle | 이벤트/웨딩 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| event-organizer | 이벤트 기획 | 행사 기획, 세미나, 워크샵, 컨퍼런스 |
| wedding-planner | 웨딩 플래너 | 결혼 준비, 스드메, 예산, 일정 관리 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

이벤트, 행사, 세미나, 워크샵, 컨퍼런스, 결혼, 웨딩, 스드메, 파티, 기념식

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 의사결정 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
