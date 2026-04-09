---
name: compliance-check
description: >
  컴플라이언스 점검 — 규제 준수 체크, 감사 보고서, ESG 보고, 규제 서류(인허가) 하네스. 컴플라이언스, 내부 감사, 규제, ESG, 환경, 사회, 지배구조.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 컴플라이언스 점검 (Compliance Check)

> moai-legal | 규제 준수 및 감사 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| compliance-checker | 컴플라이언스 체커 | 규제 준수 점검, 갭 분석, 시정 계획 |
| audit-report | 감사 보고서 | 내부 감사, 보고서 구성, 개선 권고 |
| esg-reporting | ESG 보고 | ESG 지표 수집, 보고서 프레임워크 |
| regulatory-filing | 규제 서류 | 인허가 신청, 규제 대응 문서 |

→ 하네스 파일: `references/{id}.md`

## 트리거 키워드

컴플라이언스, 규제 준수, 감사, 내부 감사, ESG, 환경경영, 인허가, 규제, 갭 분석

## 실행 규칙

1. 사용자 요청 수신 → 해당 하네스 판별
2. `references/{id}.md` 로드 → 가이드에 따라 실행
3. **규제/컴플라이언스 판단은 항상** `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

⚠️ 면책 고지: MoAI는 AI 어시스턴트이며 공인 법률/규제 자문을 대체하지 않습니다.
