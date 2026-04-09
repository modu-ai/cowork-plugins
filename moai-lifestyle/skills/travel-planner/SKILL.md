---
name: travel-planner
description: >
  여행 플래너 — 여행 일정, 맛집, 숙소, 예산 관리 + 개인 재무, 부동산 분석, 사이드 프로젝트 런처 하네스. 여행, 맛집, 부동산, 부업.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 여행 플래너 (Travel Planner)

> moai-lifestyle | 여행 및 재무 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| travel-planner | 여행 플래너 | 여행 일정, 맛집, 숙소, 예산 관리 |
| personal-finance | 개인 재무 | 가계부, 저축 전략, 투자 기초 |
| real-estate-analyst | 부동산 분석 | 매매/전세 분석, 입지 평가, 수익률 |
| side-project-launcher | 사이드 프로젝트 런처 | 부업 아이디어, 수익화 전략, 시간 관리 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

여행, 맛집, 숙소, 여행 일정, 국내 여행, 해외 여행, 부동산, 매매, 전세, 부업, 사이드 프로젝트, 재테크

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 의사결정 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
