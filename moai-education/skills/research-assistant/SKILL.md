---
name: research-assistant
description: >
  리서치 어시스턴트 — 데이터 수집/분석, 학술 논문 작성, 논문 어드바이저 하네스. 리서치, 보고서, 논문, 학술, 데이터 분석.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 리서치 어시스턴트 (Research Assistant)

> moai-education | 학술 연구 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| research-assistant | 리서치 어시스턴트 | 데이터 수집, 분석, 보고서 작성 |
| academic-paper | 학술 논문 | 학술 논문 작성, 인용, 피어 리뷰 대비 |
| thesis-advisor | 논문 어드바이저 | 연구 설계, 문헌 검토, 논문 구조화 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

리서치, 논문, 학술 논문, 데이터 수집, 데이터 분석, 보고서, 문헌 검토, 피어 리뷰, 연구 설계

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 학술 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
