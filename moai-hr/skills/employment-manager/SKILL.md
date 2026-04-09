---
name: employment-manager
description: >
  채용 관리 — 채용 파이프라인, 온보딩 시스템 하네스. JD 작성, 면접 설계, 평가 기준, 신입 온보딩, 체크리스트, 멘토링 프로그램.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# 채용 관리자 (employment-manager)

> moai-hr v1.0.0 | 2 하네스

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| hiring-pipeline | 채용 파이프라인 | JD 작성, 면접 설계, 평가 기준, 채용 프로세스 |
| onboarding-system | 온보딩 시스템 | 신입 온보딩, 체크리스트, 멘토링 프로그램 |

→ 하네스 파일: `references/{id}.md`

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 채용 설계 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

## 트리거 키워드

채용, JD, 공고, 면접, 온보딩, 신입, 입사, 멘토링, 채용 프로세스
