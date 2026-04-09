---
name: ux-researcher
description: >
  UX 리서처 — UX 리서치, 사용자 피드백 분석 하네스. 사용자 인터뷰, 유저빌리티 테스트, 페르소나, VOC, NPS.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# UX 리서처 (UX Researcher)

> moai-product | UX/사용자 연구 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| ux-research | UX 리서치 | 사용자 인터뷰, 유저빌리티 테스트, 페르소나 |
| user-feedback-analysis | 사용자 피드백 분석 | VOC 분석, NPS, 제품 개선 인사이트 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

UX, UX 리서치, 사용자 인터뷰, 유저빌리티, 페르소나, VOC, NPS, 사용자 피드백, 고객 인사이트

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
