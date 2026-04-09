---
name: tax-helper
description: >
  세무 도우미 — 한국 세법 기반 세무 상담. 3.3% 원천징수, 종합소득세, 부가가치세, 홈택스 안내. 세금, 부가세, 3.3%, 종소세, 홈택스.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 세무 도우미 (Tax Helper)

> moai-finance | 한국 세무 전문 스킬

## 실행 모듈

### 세무 도우미 (한국 3.3%/홈택스)
한국 세법 기반 세무 상담. 3.3% 원천징수, 종합소득세, 부가가치세, 홈택스 안내.
- 가이드: `references/tax/guide.md`
- 참조: `references/tax-helper/guide.md`

## 트리거 키워드

세금, 세무, 부가세, 3.3%, 원천징수, 종합소득세, 종소세, 홈택스, 사업자 세금, 연말정산, 절세

## 실행 규칙

1. 사용자 요청 수신 → 세무 유형 판별
2. `references/tax/guide.md` 로드 → 한국 세법 기반 분석
3. **세무/재무 판단은 항상** `mcp__sequential-thinking__sequentialthinking` 호출
4. 결과물 생성 후 사용자 검토 요청

⚠️ 면책 고지: MoAI는 AI 어시스턴트이며 공인 세무/회계 자문을 대체하지 않습니다. 중요한 세무 사안은 반드시 세무사와 상담하세요.
