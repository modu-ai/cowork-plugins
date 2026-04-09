---
name: close-management
description: >
  결산 및 무역 관리 — 수출입, 공급망 관리, RFP 응답, 이커머스 런처 하네스. 무역, 통관, HS 코드, SCM, 입찰 제안서.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 결산 관리 (Close Management)

> moai-finance | 무역/SCM/입찰 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| import-export | 수출입 | 무역 실무, 통관, HS 코드, 인코텀즈 |
| supply-chain | 공급망 관리 | SCM 최적화, 재고 관리, 물류 전략 |
| rfp-responder | RFP 응답 | 입찰 제안서, 기술 평가, 가격 전략 |
| ecommerce-launcher | 이커머스 런처 | 온라인 쇼핑몰 개설, 운영, 마케팅 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

수출입, 무역, 통관, HS코드, 인코텀즈, 공급망, SCM, 재고 관리, 물류, RFP, 입찰, 이커머스

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. 복잡 무역/계약 판단 → `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청
