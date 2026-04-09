---
name: newsletter
description: >
  뉴스레터 엔진 — 뉴스레터 기획부터 발행까지, 구독자 확보 전략, 콘텐츠 캘린더 연동. 뉴스레터, 이메일 뉴스레터, 구독자, 콘텐츠 발행.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 뉴스레터 (Newsletter)

> moai-content | 뉴스레터 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| newsletter-engine | 뉴스레터 엔진 | 뉴스레터 기획~발행, 구독자 확보 전략 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

뉴스레터, 이메일 뉴스레터, 구독자, 뉴스레터 발행, 위클리, 먼슬리, 콘텐츠 구독

## 실행 규칙

1. 사용자 요청 수신 → 뉴스레터 유형 판별
2. `references/newsletter-engine.md` 로드 → 가이드에 따라 실행
3. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
