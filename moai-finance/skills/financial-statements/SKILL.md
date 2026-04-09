---
name: financial-statements
description: >
  재무제표 관리 — 청구서/인보이스 관리, 보조금 신청, 비영리 재무 관리 하네스. 인보이스, 수금, 정부 지원사업, 비영리 운영.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 재무제표 (Financial Statements)

> moai-finance | 재무 문서 관리 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| invoice-mgmt | 청구서 관리 | 인보이스 작성, 수금 관리, 미수금 추적 |
| grant-writer | 보조금 신청서 | 정부 지원사업, 보조금 신청, 사업계획 |
| nonprofit-management | 비영리 관리 | 비영리 운영, 기부금 관리, 보고 의무 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

재무제표, 청구서, 인보이스, 수금, 보조금, 정부 지원사업, 비영리, 기부금, 사업비 관리

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. **세무/재무 판단은 항상** `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

⚠️ 면책 고지: MoAI는 AI 어시스턴트이며 공인 세무/회계 자문을 대체하지 않습니다.
