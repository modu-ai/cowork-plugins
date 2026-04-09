---
name: legal-risk
description: >
  법적 리스크 분석 — 법률 리서치(판례/법령), 지적재산 포트폴리오 관리, 법적 위험 평가 및 대응 전략. 특허, 상표, 저작권, IP 전략.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 법적 리스크 (Legal Risk)

> moai-legal | 법률 리서치 및 지적재산 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| legal-research | 법률 리서치 | 판례 검색, 법률 해석, 쟁점 분석 |
| ip-portfolio | 지적재산 포트폴리오 | 특허/상표/저작권 관리, IP 전략 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

법률 리서치, 판례, 법률 해석, 지적재산, 특허, 상표, 저작권, IP, 법적 리스크, 쟁점 분석

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. **법률/규제 판단은 항상** `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

⚠️ 면책 고지: MoAI는 AI 어시스턴트이며 공인 법률 자문을 대체하지 않습니다.
