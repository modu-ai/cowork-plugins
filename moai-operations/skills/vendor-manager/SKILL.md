---
name: vendor-manager
description: >
  벤더 관리 — 리스크 레지스터, 벤더 평가, 계약 관리 하네스. 위험 식별, 영향 평가, 대응 계획, 공급업체 관리.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "active"
  updated: "2026-04-09"
---

# 벤더 관리자 (vendor-manager)

> moai-operations v1.0.0 | 1 하네스

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| risk-register | 리스크 레지스터 | 위험 식별, 영향 평가, 대응 계획 |

→ 하네스 파일: `references/{id}.md`

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 전략 가이드에 따라 실행
3. `--deepthink` 또는 복잡 리스크 분석 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

## 트리거 키워드

벤더, 공급업체, 리스크, 위험 관리, 계약, 평가, 리스크 레지스터
