---
name: campaign-planner
description: |
  [책임 경계] 마케팅 캠페인 기획·퍼포먼스 마케팅·A/B 테스트·인플루언서·CRM·고객 여정 — 전술 단위만 담당. 페어 스킬 moai-business:strategy-planner와 명확히 구분 — 본 스킬은 캠페인 단위 전술(1~3개월), 페어는 사업·OKR·BMC 단위 전략(1~5년).
  '마케팅 캠페인 기획해줘', 'A/B 테스트 설계해줘', '인플루언서 전략 짜줘', '고객 여정 맵 만들어줘', 'CRM 전략 수립해줘'라고 요청하세요.
  상세페이지·이미지 생성 책임은 v2.3.0부터 제거되었습니다. 상세페이지 카피는 moai-commerce:detail-page-copy / 상세페이지 합성 이미지는 moai-commerce:detail-page-image / AI 이미지·영상은 moai-media:* 스킬을 사용하세요.
user-invocable: true
version: 2.3.0
---

# 캠페인 플래너 (Campaign Planner)

## 개요

마케팅 캠페인 기획 및 퍼포먼스 마케팅 전문 스킬입니다. A/B 테스트 설계, 그로스 해킹, 인플루언서 전략, CRM 전략, 고객 여정 맵, 영업 지원을 다룹니다.

> **v2.3.0 책임 정리**: 본 스킬에서 "이커머스 상세페이지 제작·AI 이미지 생성" 책임이 제거되었습니다(SPEC-CATALOG-CLEANUP-007 REQ-CLEANUP-007). 상세페이지·이미지가 필요한 경우 아래 "관련 스킬" 표를 참고하세요.

## 트리거 키워드

캠페인, 마케팅 캠페인, A/B 테스트, 그로스해킹, 인플루언서, 인플루언서 마케팅, CRM, 고객 여정, 고객 여정 맵, 퍼포먼스 마케팅, AARRR, 퍼널, 캠페인 KPI

## 워크플로우

### 1단계: 캠페인 목표 및 유형 확인

목표 설정(인지도/리드/전환/재구매), 채널 선택(유료 광고/SNS/이메일/인플루언서), 예산 규모 및 기간을 확인합니다.

### 2단계: 전략 수립

**캠페인 기획:** AARRR(Acquisition-Activation-Retention-Revenue-Referral) 퍼널 매핑, 채널별 예산 배분 및 KPI 설정, 크리에이티브 전략 방향을 수립합니다.

**A/B 테스트 설계:** 가설 수립 → 변수 정의 → 샘플 크기 계산, 통계적 유의성 기준 설정(p < 0.05), 결과 측정 지표 정의를 수행합니다.

**인플루언서 전략:** 메가/매크로/마이크로 인플루언서 티어 결정, 선정 기준(팔로워 수, 참여율, 타겟 부합도), 협찬 제안서 및 ROI 측정 방법을 수립합니다.

**CRM·고객 여정:** 고객 여정 맵(인지→고려→구매→리텐션→옹호) 매핑, 단계별 트리거·메시지 설계, 자동화 시퀀스 권고를 제공합니다.

### 3단계: 산출물 생성 및 검토

캠페인 전략 문서·A/B 테스트 설계서·인플루언서 제안서·고객 여정 맵·CRM 전략 문서 등 본 스킬 책임 범위의 산출물만 생성합니다.

## 사용 예시

**예시 1**: "신제품 런칭 캠페인 기획해줘. 예산 500만원, 타겟은 2030 여성"
→ 채널 믹스 → 예산 배분 → KPI 설정 → 크리에이티브 방향 → 타임라인

**예시 2**: "인플루언서 마케팅 전략 짜줘. 마이크로 인플루언서 위주로"
→ 인플루언서 티어 결정 → 선정 기준 → 협찬 제안서 → ROI 측정

**예시 3**: "이메일 시퀀스 A/B 테스트 설계해줘"
→ 가설 수립 → 변수 정의 → 샘플 크기 → 성공 지표 → 분석 방법

## 출력 형식

- 캠페인 전략 문서 (목표, 타겟, 채널, 예산, KPI)
- A/B 테스트 설계서 (가설, 변수, 샘플 크기, 성공 지표)
- 인플루언서 협찬 제안서
- 고객 여정 맵
- CRM 전략 문서

## 주의사항

| 상황 | 대응 |
|------|------|
| 예산이나 채널 정보가 없는 경우 | 업종·목표 기반 추천 예산 배분 제안 후 확인 |
| 사업·OKR·BMC 단위 전략이 필요한 경우 | 본 스킬 범위 밖. `moai-business:strategy-planner`로 안내 |
| 상세페이지·이미지 생성 요청 | 본 스킬 범위 밖 (v2.3.0부터 책임 분리). 아래 "관련 스킬" 표 참고 |

## 관련 스킬

| 스킬 | 사용 시점 |
|------|----------|
| `moai-business:strategy-planner` | 사업·OKR·BMC·Lean Canvas·SWOT 등 전략 단위 기획 (페어 분리) |
| `moai-marketing:sns-content` | SNS 콘텐츠 단건 작성, 브랜드 보이스 설정 |
| `moai-marketing:seo-audit` | SEO 검색 최적화 분석 |
| `moai-marketing:performance-report` | 마케팅 성과 분석 보고서 |
| `moai-marketing:email-sequence` | 이메일 시퀀스·드립 캠페인 카피 |
| `moai-marketing:target-script` | 타겟별 핵심 메시지 분석 (페인포인트→메시지) |
| `moai-commerce:detail-page-copy` | 이커머스 상세페이지 카피 (13섹션 감정여정) |
| `moai-commerce:detail-page-image` | 이커머스 상세페이지 합성 이미지 (1080×12720 PNG) |
| `moai-media:image-gen` | AI 이미지 생성 |
| `moai-media:video-gen` | AI 영상 생성 |

## 이 스킬을 사용하지 말아야 할 때

- 사업 단위 전략(OKR·BMC·SWOT·Lean Canvas): `moai-business:strategy-planner` 사용
- 이커머스 상세페이지 카피: `moai-commerce:detail-page-copy` 사용 (v2.3.0 책임 분리)
- 이커머스 상세페이지 합성 이미지: `moai-commerce:detail-page-image` 사용
- AI 이미지·영상 생성: `moai-media:*` 스킬 사용
- SNS 단건 콘텐츠 작성: `moai-marketing:sns-content` 사용
