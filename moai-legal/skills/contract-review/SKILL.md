---
name: contract-review
description: >
  계약서 검토 — 한국 민법/상법 기반 계약서 분석, 10대 리스크 패턴, 이용약관 및 서비스 법률 문서 작성. 계약서, 위험 조항, 이용약관, 개인정보처리방침, SLA.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 계약서 검토 (Contract Review)

> moai-legal | 계약서 및 법률 문서 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| service-legal-docs | 서비스 법률 문서 | 이용약관, 개인정보처리방침, SLA |

→ 하네스 파일: `references/{id}.md`

## 실행 모듈

### 계약서 검토 (한국법 기반)
한국 민법/상법 기반 계약서 검토, 10대 리스크 패턴 분석.
- 가이드: `references/contract/guide.md`
- 참조: `references/contract-reviewer/guide.md`

## 트리거 키워드

계약서, 계약 검토, 위험 조항, 이용약관, 개인정보처리방침, SLA, 민법, 상법, 법률 문서

## 실행 규칙

1. 사용자 요청 수신 → 하네스/실행 모듈 판별
2. 법률 문서 요청 → `references/service-legal-docs.md` 로드 → 문서 작성
3. 계약서 검토 요청 → `references/contract/guide.md` 로드 → 한국법 기반 분석
4. **법률/규제 판단은 항상** `mcp__sequential-thinking__sequentialthinking` 호출
5. 결과물 생성 후 사용자 검토 요청

⚠️ 면책 고지: MoAI는 AI 어시스턴트이며 공인 법률 자문을 대체하지 않습니다. 중요한 법률 사안은 반드시 전문 법률가와 상담하세요.
