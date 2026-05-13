# 부록 H — 정합성 검증 + Layer 2 MCP 호출 가이드

SPEC-META-ADS-001 §3 REQ-AUDIT-MCP-016 + 작업명세서 부록 H 직접 인용.

---

## H.1 정합성 검증 체크 항목 6종 (작업명세서 H.1 직접 인용)

컬럼 매핑 완료 후, 분석 실행 전에 다음 6개 항목을 자동 검증합니다:

| # | 항목 | 검증 방법 | 실패 시 처리 |
|---|------|---------|------------|
| 1 | **보고 기간 일관성** | 파일 내 모든 행의 보고 시작·종료 일자 범위 확인. 다중 파일 시 기간 중복·공백 확인 | 경고 + 이상 행 목록 표시 |
| 2 | **필수 컬럼 존재 여부** | B.3의 12개 필수 컬럼 모두 존재 확인 | 누락 컬럼 목록 + 가능한 분석만 진행 |
| 3 | **수치 범위 합리성** | 음수 ROAS, 음수 지출, CTR > 100%, ROAS > 100 등 이상값 감지 | 이상값 행 목록 + 분석 제외 여부 사용자 확인 |
| 4 | **결측치 비율** | 각 컬럼 결측치(빈 셀, N/A) 비율 계산 | 30% 이상 시 경고 + 해당 컬럼 분석 주의 표시 |
| 5 | **중복 행 감지** | 광고 이름 + 노출 위치 + 기간이 동일한 행 중복 여부 | 중복 행 목록 + 합산 또는 제거 선택 |
| 6 | **인구통계 컬럼 일관성** | 연령·성별 컬럼이 일부 행에만 있는 경우 감지 | 불완전한 인구통계 컬럼 경고 + 완전한 행만 인구통계 분석 |

### 통합/분리 보고서 판정 (작업명세서 H.4)

파일 2개인 경우 분리 보고서 판정:
- 공통 키(광고 이름 + 보고 기간) 매칭 시도
- 매칭률 > 80%: 분리 보고서 통합 모드 확정
- 매칭률 50~80%: 경고 + 사용자 확인 요청
- 매칭률 < 50%: 다중 캠페인 일괄 모드로 전환 권고

---

## H.2 노출수 추정 (작업명세서 H.2)

**조건**: 노출수(Impressions) 컬럼 부재 + CTR 컬럼 존재

```
노출 추정 공식:
노출수 = 링크 클릭 / (CTR / 100)

주의: CTR = 0인 행은 추정 불가 → 해당 행 분석 제외
```

추정값 사용 시 출력물에 명시: "(노출수 CTR 기반 추정값)"

---

## H.3 다중 월 정규화 (작업명세서 H.3)

다중 월 비교 모드 시 보고 기간이 다를 경우 일평균으로 정규화:

```
각 파일 처리:
1. 보고 기간 일수 = (Reporting ends - Reporting starts) + 1
2. 일평균 = 해당 기간 지표 합계 ÷ 보고 기간 일수
3. 30일 환산 = 일평균 × 30
```

정규화 후 월간 비교 차트 생성 시 "30일 환산 기준" 명시.

---

## H.4 분리 보고서 매칭 (작업명세서 H.4 직접 인용)

두 보고서 통합 시 매칭 키:

1. **광고 이름 (Ad name)** — 정확 일치 우선, 공백·대소문자 정규화 후 Fuzzy 매칭
2. **보고 기간 (Reporting period)** — Reporting starts + Reporting ends 동일 여부

매칭 결과 처리:
- 완전 매칭: 두 보고서의 지표를 같은 행에 결합
- 매칭 실패: 사용자에게 알림 + 해당 행은 단일 차원으로만 분석

---

## H.5 데이터 처리 원칙

### 집계 기준

- 광고 단위로 집계 (캠페인→광고세트→광고 계층에서 광고 레벨 기준)
- 노출 위치·연령·성별로 분해 시 각 차원별 합산
- 퍼센트 지표(CTR, CVR, ROAS)는 가중평균 (지출 기준) 적용

### 결측치 처리

- 지출 0원 행: 분석에 포함하되 ROAS·CPC 계산 제외 (0 나누기 방지)
- 구매 0건 행: 모듈 5 누수 분석의 핵심 타겟으로 포함
- CTR 0% 행: 노출수 추정 불가 행으로 별도 처리

---

## H.6 Layer 2 MCP 호출 가이드 (v2 단계 — 현재 v1에서는 참고만)

SPEC-META-ADS-001 v0.2.0 Amendment REQ-META-ADS-AMEND-001 기준.

### 3-Layer 아키텍처 (v2 단계 계획)

```
Layer 1: Meta 공식 MCP (mcp.facebook.com/ads) 또는 .xlsx 업로드 (v1 현재)
   ↓ 데이터 fetch
Layer 2: moai-ads-audit-mcp (SPEC-MOAI-ADS-AUDIT-MCP-001 — v2 별도 SPEC)
   ↓ 50-check audit 비즈니스 로직
Layer 3: meta-ads-analyzer (본 스킬 — 사용자 UI + 톤 조정 + 액션 옵션)
```

### v2 단계 Layer 2 MCP 주요 도구 (계획)

| 도구 | 역할 |
|------|------|
| `audit_meta_account` | Meta 50-check 진행 |
| `calculate_health_score` | 가중 점수 계산 (Critical 5× / High 3× / Medium 1.5× / Low 0.5×) |
| `get_quick_wins` | 15분 이내 조치 가능 항목 추출 |
| `get_emq_score` | EMQ tiered targets 평가 (Purchase 8.5+ / AddToCart 6.5+ / PageView 5.5+) |

> **v1 현재**: Layer 2 MCP는 미구현 상태. 모든 분석은 업로드된 .xlsx 데이터 기반. v2 API 연동 시 SPEC-COMMERCE-MCP-002 참조.

### Meta 공식 MCP 활성화 조건 (v2 계획)

```
is_ads_mcp_enabled: true → Meta 공식 MCP 우선 사용
is_ads_mcp_enabled: false → Adspirer 또는 byadsco MCP fallback
.xlsx 업로드 → Layer 1 없이 직접 Layer 3 (현재 v1)
```

---

## H.7 50-check ID → 9 모듈 매핑 (SPEC v0.2.0 Amendment)

claude-ads v1.5.1 차용 (MIT). 50 check를 본 스킬 9 모듈에 매핑:

| 9 모듈 | claude-ads 50 check ID |
|--------|----------------------|
| 모듈 1: 퍼널 분해 | 별도 (claude-ads 미포함, 본 스킬 고유) |
| 모듈 2: KPI 분해 | M-CR4 (CTR), M-ST1-2 (Budget) + benchmarks |
| 모듈 3: 차원별 분해 | M-CR1~4 (Creative), M19~M24 (Audience), M34 (Placement) |
| 모듈 4: 범용 매트릭스 | M16 (Audience overlap), M-AN1 (Andromeda Similarity) |
| 모듈 5: 누수·파레토 | M28 (Creative fatigue) + breakdown analysis |
| 모듈 6: 소재 라이프사이클 | M-CR1 (Creative freshness), M28, M29 (Hook rate) |
| 모듈 7: 학습 단계 진입 | M13 (Learning Limited), M14 (Learning resets) |
| 모듈 8: 예산 적정성 | M-ST1 (Budget ≥5x CPA), M-ST2 (Utilization), M17 |
| 모듈 9: 시나리오 시뮬레이션 | 별도 (본 스킬 고유) |

Pixel/CAPI Health (M01-M10): 모듈 외 → pixel-audit 페어 스킬 담당.
