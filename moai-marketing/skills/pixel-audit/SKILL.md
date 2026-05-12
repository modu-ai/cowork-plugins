---
name: pixel-audit
description: |
  [책임 경계] 메타·구글·네이버 픽셀 설치 검증 + 1st Party 데이터 활용 진단 + Lookalike 씨앗 품질 평가 전담. 페어 스킬 performance-report(GA4·메타 광고 ROAS 분석)와 명확히 구분 — 본 스킬은 픽셀·데이터 인프라 검증, 페어는 광고 성과 분석.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "픽셀 설치 점검", "메타 픽셀 검증", "구글 픽셀 확인", "CAPI 설치 확인", "전환 API 점검", "Lookalike 씨앗 품질", "VIP 구매자 Lookalike", "1st Party 데이터 진단", "이메일 리스트 활용", "픽셀 실수 점검", "iOS 14 전환 추적 손실".
  3종 픽셀 실수(구매자 미제외/이벤트 파라미터 미설정/CAPI 미설치) 검증 + 1st Party 데이터 3종(이메일·전화번호 / 픽셀 이벤트 / 구매·CRM) 활용도 진단 + Lookalike 씨앗(VIP 구매자 상위 20%) 품질 평가.
  ai-slop-reviewer 자동 체이닝 (진단 보고서 텍스트 산출물).
  v2.4.0 신규 (자료 4 "온라인 광고의 심리학" §5 풀세트).
user-invocable: true
version: 2.4.0
---

# 픽셀·1st Party 데이터 진단 (Pixel Audit)

## 개요

3rd party 쿠키 종료 시대(애플 ATT + 구글 쿠키 종료)에 1st party 데이터를 가진 브랜드 vs 없는 브랜드의 광고 효율 차이가 점점 벌어집니다. 본 스킬은 그 격차를 측정·진단합니다.

**책임 한 줄**: 메타·구글 픽셀 설치 상태 + 1st Party 데이터 + Lookalike 씨앗 품질 진단 → 개선 우선순위 자동 생성.

## 픽셀 설계에서 가장 많이 하는 실수 3종 (자료 4 §5)

### 실수 1: 구매자 미제외
이미 산 사람에게 "아직 구매 안 하셨나요?" 광고를 계속 보내는 것.

**진단**: 메타 광고 관리자 → 광고 세트 → 오디언스 제외에 **Purchase 이벤트 30일 트리거** 추가 여부.
- ❌ 미설정 → 광고비 누수 (구매자도 광고 노출)
- ✅ 설정 → 신규 구매 후보에만 노출

### 실수 2: 이벤트 파라미터 미설정
ViewContent·AddToCart에 **상품 ID와 가격 파라미터**를 붙여야 동적 광고(DPA)가 작동.

**진단 코드**:
```javascript
// ❌ 잘못된 예
fbq('track', 'ViewContent');

// ✅ 올바른 예
fbq('track', 'ViewContent', {
  content_ids: ['SKU123'],
  content_type: 'product',
  value: 19800,
  currency: 'KRW'
});
```

### 실수 3: 전환 API 미설치 (CAPI)
픽셀만으로는 iOS 사용자의 전환 추적이 불완전. **서버 사이드 전환 API(CAPI)를 같이 설치 필수**.

iOS 14.5+ 이후:
- pixel-only: 실제 전환의 50~70%만 추적
- pixel + CAPI: 90%+ 추적 가능

## 1st Party 데이터 3종 (자료 4 §5)

| 데이터 | 활용 강도 | 활용 방법 |
|--------|----------|----------|
| **이메일·전화번호** | 가장 강력 | 뉴스레터·구매·이벤트로 수집 → 메타·구글 업로드 → 커스텀 오디언스 + Lookalike 씨앗 |
| **픽셀 이벤트 데이터** | 강함 | PageView → ViewContent → AddToCart → InitiateCheckout → Purchase 5단계 |
| **구매·CRM 데이터** | 매우 강함 | 재구매 주기 예측, VIP 세그먼트, 휴면 고객 재활성 |

## Lookalike — 씨앗 품질이 전부 (자료 4 §5)

Lookalike의 품질 한계 = 씨앗 데이터의 품질 한계.

| 씨앗 데이터 | Lookalike 품질 |
|------------|---------------|
| 전체 방문자 | 낮음 (구매 의도 없는 사람 포함) |
| 장바구니 추가자 | 중 |
| 구매자 전체 | 높음 |
| **VIP 구매자 (상위 20%)** | **최고** ⭐ |

### 실전 권장 사항

```
1. VIP 구매자(상위 20%) 데이터 추출 (LTV·구매 횟수·평균 객단가 상위)
2. 메타에 커스텀 오디언스 업로드
3. Lookalike 생성 (유사도 1~3%부터 시작 → 포화되면 확장)
4. 기존 고객 반드시 제외
5. 월 1회 이상 씨앗 데이터 최신 상태 업데이트
```

## 진단 체크리스트

### A. 메타 픽셀
- [ ] 픽셀 설치 (Facebook Pixel Helper로 확인)
- [ ] PageView 이벤트 작동
- [ ] ViewContent 이벤트 + content_ids/value/currency 파라미터
- [ ] AddToCart 이벤트 + 파라미터
- [ ] Purchase 이벤트 + 파라미터
- [ ] CAPI (서버 사이드 전환 API) 설치
- [ ] 광고 세트 오디언스 제외에 Purchase 30일 추가
- [ ] Aggregated Event Measurement (AEM) 8개 이벤트 설정

### B. 구글 픽셀 (GA4 + Ads)
- [ ] GA4 설치
- [ ] Enhanced Conversions 활성화
- [ ] 전환 이벤트 정의 (구매, 회원가입, 장바구니)
- [ ] Google Ads 연동
- [ ] 부정 키워드 등록 ('무료', 'DIY', '방법')

### C. 1st Party 데이터
- [ ] 이메일·전화번호 수집 채널 (뉴스레터·구매·이벤트)
- [ ] 메타 커스텀 오디언스 업로드 (월 1회+)
- [ ] CRM 시스템 (Customer Lifecycle 추적)
- [ ] VIP 구매자 상위 20% 자동 추출 가능

### D. Lookalike
- [ ] VIP 씨앗 데이터 사용
- [ ] 유사도 1~3% 시작
- [ ] 기존 고객 제외
- [ ] 월 1회 이상 씨앗 업데이트

## 트리거 키워드

픽셀, 메타 픽셀, 구글 픽셀, 페이스북 픽셀, CAPI, 전환 API, Lookalike, 유사 타겟, 1st Party 데이터, VIP 구매자, 이메일 리스트, 커스텀 오디언스, iOS 전환 손실, AEM, Aggregated Event

## 입력·출력

### 입력 슬롯

| 항목 | 필수 | 예시 |
|------|------|------|
| 사이트 URL | 필수 | https://example.com |
| 메타 광고 사용 여부 | 필수 | Yes/No |
| 구글 광고 사용 여부 | 필수 | Yes/No |
| 이메일 리스트 보유 | 권장 | 5,000개 |
| 현재 사용 중인 픽셀·도구 | 권장 | 메타 픽셀·GA4·CAPI 등 |

### 출력 (진단 보고서)

```markdown
## 픽셀·1st Party 데이터 진단 결과

### 📊 점수
- 메타 픽셀: 60/100
- 구글 GA4: 70/100
- 1st Party 데이터: 30/100 ⚠️
- Lookalike: 미구축 ⚠️
- **종합 점수: 53/100 (C)**

### 🔴 즉시 수정 (Phase 1, 1주)
1. CAPI 미설치 → iOS 전환 30% 손실 추정
2. VIP 씨앗 Lookalike 미구축 → Cold 광고비 효율 손실
3. 이메일 리스트 메타 업로드 미시행

### 🟡 단계적 개선 (Phase 2, 1개월)
4. ViewContent 이벤트 파라미터 보강
5. Enhanced Conversions 활성화

### 🟢 최적화 (Phase 3, 분기)
6. 코호트 분석 + LTV/CAC 측정 자동화
```

## 페어 분리

| 페어 스킬 | 차이 |
|----------|------|
| `performance-report` | GA4·메타·네이버 ROAS 종합 분석 (본 스킬은 픽셀·데이터 인프라 검증) |
| `campaign-planner` | 캠페인 기획·운영 (본 스킬은 데이터 인프라 진단) |
| `coupang-ad-optimizer` | 쿠팡 광고 (본 스킬은 메타·구글 픽셀) |

## SPEC

`.moai/specs/SPEC-PIXEL-AUDIT-001/spec.md` (v2.4.0 신규)
