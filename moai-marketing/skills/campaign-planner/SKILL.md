---
name: campaign-planner
description: >
  마케팅 캠페인 기획 — A/B 테스트, 그로스 해킹, 인플루언서 전략, CRM, 고객 여정, 영업 지원 하네스. AI 이미지 생성(Imagen), 이커머스 상세페이지 실행.
user-invocable: true
metadata:
  version: "1.0.0"
  status: "stable"
  updated: "2026-04-09"
---

# 캠페인 플래너 (Campaign Planner)

> moai-marketing | 캠페인 기획 및 퍼포먼스 마케팅 전문 스킬

## 하네스 (전략 가이드)

| ID | 한국명 | 설명 |
|----|--------|------|
| ab-testing | A/B 테스트 설계 | 실험 설계, 통계적 유의성, 결과 분석 |
| growth-hacking | 그로스 해킹 | 성장 실험, 바이럴 루프, 리퍼럴 |
| influencer-strategy | 인플루언서 전략 | 인플루언서 선정, 협찬 전략, ROI 측정 |
| crm-strategy | CRM 전략 | 고객 관계 관리, 리텐션, LTV 최적화 |
| customer-journey-map | 고객 여정 맵 | 터치포인트 매핑, 경험 최적화 |
| sales-enablement | 영업 지원 | 세일즈 콘텐츠, 영업 프로세스 최적화 |

→ 하네스 파일: `references/{id}.md`

## 실행 모듈

### AI 이미지 생성 (Nano Banana / Imagen)
Imagen API 기반 AI 이미지 생성.
- 가이드: `references/imagegen/guide.md`

### 이커머스 상세페이지
쿠팡, 스마트스토어, 자사몰 상세페이지 제작.
- 가이드: `references/product-detail/guide.md`
- 참조: `references/product-detail/conversion-formulas.md`

## 트리거 키워드

캠페인, A/B 테스트, 그로스해킹, 인플루언서, CRM, 고객 여정, 영업, 퍼포먼스 마케팅, 상세페이지, 쿠팡, 스마트스토어, 이미지 생성

## 실행 규칙

1. 사용자 요청 수신 → 하네스/실행 모듈 판별
2. 하네스 요청 → `references/{id}.md` 로드 → 전략 가이드 실행
3. 실행 모듈 요청 → 해당 `references/{module}/guide.md` 로드 → 콘텐츠/이미지 생성
4. `--deepthink` 또는 복잡 작업 → `mcp__sequential-thinking__sequentialthinking` 호출
5. 결과물 생성 후 사용자 검토 요청
