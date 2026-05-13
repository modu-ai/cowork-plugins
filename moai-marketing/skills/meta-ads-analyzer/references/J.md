# 부록 J — 자매 스킬 후보

SPEC-META-ADS-001 §8.3 + 작업명세서 부록 J 직접 인용.

---

## J.1 자매 스킬 후보 개요

본 스킬(`meta-ads-analyzer`)은 메타 광고 3종 진단 패키지 중 "보고서 분석" 슬롯을 담당합니다. 아래 자매 스킬은 v1 출시 이후 별도 SPEC으로 추진할 후보입니다.

| 자매 스킬 가칭 | 역할 | 현재 상태 |
|------------|------|---------|
| `meta-ads-creative-generator` | 광고 소재 카피 생성 | 미출시 — 향후 별도 SPEC |
| `meta-ads-budget-planner` | 예산 시뮬레이션 전용 | 미출시 — 향후 별도 SPEC |
| `meta-ads-curriculum-builder` | 강의 자료 자동 생성 | 미출시 — 향후 별도 SPEC |

---

## J.2 meta-ads-creative-generator (소재 카피 생성)

**역할**: 기존 광고 소재 성과 분석 결과를 기반으로 새로운 광고 소재 카피를 생성합니다.

**본 스킬과의 관계**:
- 본 스킬 (`meta-ads-analyzer`): 기존 소재 성과 분석 + 노후화 진단
- 자매 스킬: 분석 결과를 바탕으로 신규 소재 카피 생성

**체인 예시**:
```
meta-ads-analyzer (소재 노후화 감지 + 방향 제시)
       ↓ 모듈 6 결과 전달
meta-ads-creative-generator (신규 소재 카피 생성)
       ↓
moai-core:ai-slop-reviewer (AI 슬롭 검수)
```

**포함될 기능 (계획)**:
- 고성과 소재 패턴 기반 카피 생성
- 관여도·운영 철학 반영 메시지 프레임
- A/B 테스트 변형 3~5개 자동 생성
- 카피별 예상 효과 가설 제시

---

## J.3 meta-ads-budget-planner (예산 시뮬레이션 전용)

**역할**: 예산 배분·최적화에 특화된 심층 시뮬레이션 도구입니다.

**본 스킬과의 관계**:
- 본 스킬: 모듈 8(예산 적정성) + 모듈 9(기본 시뮬레이션) 제공
- 자매 스킬: 더 정교한 예산 최적화 전용 분석

**체인 예시**:
```
meta-ads-analyzer (전반적 진단 + 기본 예산 적정성)
       ↓ 예산 최적화 심층 분석 필요 시
meta-ads-budget-planner (채널별·캠페인별 예산 배분 최적화)
```

**포함될 기능 (계획)**:
- 캠페인별·광고세트별 예산 재배분 시뮬레이션
- LTV(고객 생애 가치) 기반 CPA 목표 역산
- 계절성·트렌드 반영 예산 조정 시나리오
- 예산 증액 시 예상 매출 곡선 (수확 체감 구간 표시)

---

## J.4 meta-ads-curriculum-builder (강의 자료 자동 생성)

**역할**: 분석 결과를 강의·워크샵용 교육 자료로 변환합니다.

**본 스킬과의 관계**:
- 본 스킬: 분석 결과 PPTX 출력 (발표 자료 수준)
- 자매 스킬: 메타 광고 강의용 커리큘럼·실습 데이터셋 생성

**체인 예시**:
```
meta-ads-analyzer (실제 케이스 분석 결과)
       ↓ 강의 케이스 스터디 필요 시
meta-ads-curriculum-builder (강의자료·실습 문제 자동 생성)
```

**포함될 기능 (계획)**:
- 실제 데이터 기반 케이스 스터디 슬라이드 생성
- 수강생 실습용 익명화 데이터셋 생성
- 강의 진행 순서별 포인트 정리
- Q&A 예상 문제 및 모범 답안

**연계 가능성**: moai-education 플러그인 (향후) 과 연계.

---

## J.5 v2 로드맵 — API 연동

SPEC-COMMERCE-MCP-002 연계 (SPEC-META-ADS-001 §1.2).

| 단계 | 설명 | SPEC |
|------|------|------|
| v1 (현재) | .xlsx 보고서 업로드 방식 | SPEC-META-ADS-001 |
| v2 (계획) | 메타 마케팅 API 직접 연동 (사용자 본인 토큰) | SPEC-COMMERCE-MCP-002 |
| v3 (장기) | SaaS화 — 메타 앱 심사 + 상시 대시보드 | 미확정 |

v2 단계에서 본 스킬은 Layer 3(사용자 UI)으로 동작하며, Layer 1(Meta MCP)·Layer 2(moai-ads-audit-mcp) 와 결합됩니다. 상세: 부록 H.6.

---

## J.6 메타 광고 3종 진단 패키지

본 스킬은 다음 3종 패키지의 "보고서 분석" 슬롯입니다:

```
메타 광고 3종 진단 패키지:

[인프라 진단]         pixel-audit
                      ↓ 픽셀·CAPI·1st Party 데이터
[랜딩 진단]    landing-page-conversion-audit
                      ↓ 6섹션 전환율
[보고서 분석]  meta-ads-analyzer (본 스킬)
                      ↓ 성과 데이터 사후 분석
```

체인 사용 예시 (종합 진단 워크플로우):
```
pixel-audit (인프라 선점검)
       ↓
meta-ads-analyzer (보고서 분석 + 액션 도출)
       ↓ CVR 낮음 감지 시
landing-page-conversion-audit (랜딩 전환율 진단)
       ↓
campaign-planner (다음 캠페인 기획)
```
