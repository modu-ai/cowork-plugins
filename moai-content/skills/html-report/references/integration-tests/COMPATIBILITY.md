# P1 컨슈머 통합 호환성 보고서

> html-report v2.2.0 Wave 3 검증 — 4개 P1 소비 스킬 통합 테스트 결과
> 작성일: 2026-05-09

---

## 1. moai-bi:executive-summary → mode=status

### 적합 모드

`status` 모드 — 경영진 요약 보고서 구조(What/So What/Now What/Risks/Next Review)는 status 모드의 헤더·하이라이트·Carryover 구조에 자연스럽게 매핑됨.

### 매핑된 입력 슬롯

| 마크다운 섹션 | status 템플릿 슬롯 | 매핑 방식 |
|---|---|---|
| `## What` 3 bullet | `{{#highlights}}` | 직접 삽입 |
| `## So What` 3 bullet | `{{#highlights}}` (연장) | 직접 삽입 |
| `## Now What` 옵션 A/B + 권고 | `{{#carryover}}` | 그룹 레이아웃 재활용 |
| `## Risks` bullet | `{{#carryover.blocked}}` | 블로킹 그룹 재활용 |
| `## Next Review` | `footer` | 푸터 텍스트 |
| 헤드라인(> 인용) | `{{eyebrow}}` | 요약 텍스트 |
| K-IFRS 재무 수치 4개 | `{{#metrics}}` (stat-card) | 메트릭 카드 4개 |

### 매핑되지 않은 섹션

- **의사결정 옵션 레이아웃**: Now What의 옵션 A/B 구조는 status 템플릿의 Carryover 슬롯을 재활용했으나, 원본 `shipped_table`(완료 테이블)이 executive-summary 출력에는 존재하지 않아 빈 슬롯으로 남음.
- **Velocity 차트 원본 데이터**: executive-summary는 시계열 주간 데이터를 출력하지 않아 차트 데이터를 수동으로 재구성해야 함.
- **담당자(author) 컬럼**: shipped_table의 담당자 정보가 executive-summary 출력에는 없음.

### 권장 사용법

```
moai-bi:executive-summary → moai-core:ai-slop-reviewer → moai-content:html-report mode=status
```

재무 수치 4개를 `{{#metrics}}` 슬롯에 수동 지정하거나, `executive-summary` 출력의 `## What` 섹션에서 굵은 수치를 자동 추출하도록 프롬프트 지정 권장.

### 향후 개선 메모

- executive-summary가 K-IFRS 재무 지표를 정형화된 표로 출력할 경우 status 템플릿의 `metrics` 슬롯 자동 추출 가능.
- "Now What" 옵션 패턴을 위한 `decisions` 전용 섹션 추가 검토 (status 템플릿 v2 대상).
- 헤드라인 1줄을 `eyebrow`가 아닌 별도 call-out 배너로 강조하는 변형 검토.

---

## 2. moai-finance:financial-statements → mode=financial

### 적합 모드

`financial` 모드 — 재무제표 세트(손익계산서/재무상태표/현금흐름표) 구조가 financial 템플릿에 직접 매핑. K-IFRS 5개 범주 분류가 `row-header` 스타일로 자연스럽게 표현됨.

### 매핑된 입력 슬롯

| 마크다운 섹션 | financial 템플릿 슬롯 | 매핑 방식 |
|---|---|---|
| 핵심 재무 지표 표 | `{{#kpis}}` (kpi-card) | 4개 KPI 카드 |
| `## 손익계산서` 영업/투자/재무 범주 | `{{#statement_rows}}` + `row-header` | 5개 범주 그룹핑 |
| 매출총이익·영업이익 소계 | `row-subtotal` 클래스 | 소계 행 스타일링 |
| 당기순이익 합계 | `row-total` 클래스 | 합계 행 강조 |
| 전기 대비 증감/증감률 | `change_abs` / `change_pct` | 직접 삽입 |
| `## 주석` 번호 목록 | `{{#notes}}` | 직접 삽입 |

### 매핑되지 않은 섹션

- **재무상태표**: financial 템플릿은 손익계산서 중심 레이아웃으로 재무상태표 전체를 수용하기에 좁음. 별도 섹션 추가 또는 요약 4개 행으로 압축 필요.
- **현금흐름표**: 현금흐름 섹션이 템플릿에 없어 Notes 슬롯에 텍스트로 압축해야 함.
- **자본변동표**: 완전 재무제표 세트 중 자본변동표는 현재 financial 템플릿 범위 밖.
- **재무비율 분석 테이블**: variance 차트와 별개로 비율 테이블을 위한 슬롯 없음.

### 권장 사용법

```
moai-finance:financial-statements → moai-content:html-report mode=financial
```

손익계산서 핵심 항목에 집중하고, 재무상태표·현금흐름표는 요약 KPI 카드(4개)로 압축하여 50KB 제한 내 유지.

### 향후 개선 메모

- financial 템플릿에 "재무상태표 요약" 별도 섹션 추가 검토 (자산/부채/자본 3행 카드 형태).
- K-IFRS 5개 범주 자동 인식 파서 힌트 추가 권장 (SKILL.md 슬롯 설명에 범주 명 목록 포함).
- 재무비율 분석 결과를 status 모드 metrics 카드 그리드로 병행 렌더링하는 체인 구성도 유효.

---

## 3. moai-business:sbiz365-analyst → mode=plan

### 적합 모드

`plan` 모드 — sbiz365-analyst의 9개 섹션 보고서 구조(Executive Summary/분석 개요/각 분석/타당성 평가/리스크/결론)가 plan 템플릿의 마일스톤·데이터흐름·리스크·성공지표 구조에 잘 대응됨.

### 매핑된 입력 슬롯

| 마크다운 섹션 | plan 템플릿 슬롯 | 매핑 방식 |
|---|---|---|
| 창업 타당성 종합 판정 + 핵심 발견 | `{{goal_html}}` (goal-box) | 목표 요약 텍스트 |
| 종합 판정·타당성 점수·유동인구·업소 수 | `{{#summary_cells}}` (sum-cell) | 4개 요약 카드 |
| 단기·중기 액션 아이템 | `{{#milestones}}` | 창업 단계 타임라인 |
| 데이터 흐름 (소상공인365 → 분석 → 판정) | `{{diagram_svg}}` | 인라인 SVG 플로우차트 |
| `## 리스크 요인 및 대응 전략` 표 | `{{#risks}}` + `sev_class` | 리스크 매트릭스 |
| 성공 조건 3가지 + 측정 목표 | `{{#success_metrics}}` | 성공 지표 행 |

### 매핑되지 않은 섹션

- **5대 분석 섹션 (유동인구/매출/경쟁/입지/타당성)**: plan 템플릿의 milestones에 창업 단계로 재구성하여 표현했으나, 원본의 상세 수치 표(성별 비율, 시간대 분포 등)를 수용할 슬롯이 없음.
- **4축 평가 점수표**: 점수 매트릭스 테이블 형태를 수용하는 전용 슬롯 없어 success_metrics로 개별 행 표현으로 대체.
- **분석 데이터 수치 표들**: 5개 분석 섹션의 테이블 데이터가 상세하여 50KB 제한 내 전체 수용 어려움.

### 권장 사용법

```
moai-business:sbiz365-analyst → moai-core:ai-slop-reviewer → moai-content:humanize-korean → moai-content:html-report mode=plan
```

sbiz365 보고서의 "Executive Summary" + "창업 타당성 평가" + "리스크" + "결론" 핵심 섹션만 추출하여 plan 모드 렌더링 권장. 5개 상세 분석 섹션은 마크다운 원본 보고서(docx)에서 참조하도록 안내.

### 향후 개선 메모

- sbiz365-analyst의 4축 평가 점수(100점 만점)를 `summary_cells`의 accent 스타일로 자동 강조하는 프롬프트 패턴 문서화 권장.
- 분석 섹션별 수치 표를 컴팩트하게 표현하는 "data-table" 컴포넌트 슬롯 추가 검토.
- 소상공인365 공공데이터 상권 영역을 SVG 지도 인라인으로 시각화하는 확장 검토 (오픈 데이터 좌표 활용).

---

## 4. moai-business:daily-briefing → mode=status (daily variant)

### 적합 모드

`status` 모드 — daily-briefing의 표준 섹션(헤드라인/업계뉴스/경쟁사/규제/시장지표/액션아이템)이 status 모드의 메트릭카드·하이라이트·Shipped테이블·Velocity차트·Carryover 구조에 잘 대응됨.

### 매핑된 입력 슬롯

| 마크다운 섹션 | status 템플릿 슬롯 | 매핑 방식 |
|---|---|---|
| 시장 지표 4개 (코스피/코스닥/환율/금리) | `{{#metrics}}` (stat-card) | 메트릭 카드 4개 |
| `## 헤드라인 요약` 3줄 | `{{#highlights}}` | 하이라이트 목록 |
| `## 업계 주요 뉴스` 표 (제목/출처/시사점) | `table.shipped` | 완료 테이블 재활용 |
| 경쟁사 채용 공고 수 | `velocity_chart.bars` | Velocity 차트 데이터 |
| `## 오늘의 액션 아이템` P0/P1/P2 그룹 | `{{#carryover}}` 그룹 | Carryover 3개 그룹 |

### 매핑되지 않은 섹션

- **경쟁사 동향 서술**: 각 경쟁사별 주요 활동 텍스트 블록은 shipped 테이블 형식으로 압축하기 어렵고, 별도 섹션 없음. 하이라이트 목록에 1~2줄로 요약하거나 생략.
- **규제·정책 업데이트**: 별도 섹션으로 시각적 강조가 필요하나, status 템플릿에 전용 슬롯 없어 highlights나 carryover에 통합됨.
- **시장 지표 상세 (비트코인 등)**: 4개 카드 제한으로 전체 시장 지표 수용 불가, 주요 4개만 표시.

### 권장 사용법

```
moai-business:daily-briefing → moai-content:html-report mode=status
```

간단 체인: ai-slop-reviewer 없이도 구조가 명확하여 직접 렌더링 가능. 경쟁사 동향·규제 섹션은 highlights에 1~2줄 요약 삽입. 시장 지표 4개를 메트릭 카드로 우선 배치.

### 향후 개선 메모

- daily-briefing용 status 변형 모드 추가 검토: "status-daily" 또는 status 템플릿에 `news_table` 별도 슬롯 추가.
- 경쟁사 섹션을 위한 `competitor_cards` 패널 컴포넌트 추가 검토.
- 규제·정책 업데이트를 위한 `policy_alerts` 배너 슬롯 추가 검토 (clay 색상 강조).

---

## 호환성 평가 요약

### 호환성 평가표

| 컨슈머 스킬 | 적합 모드 | 핵심 슬롯 매핑 수 | 미매핑 섹션 수 | 호환성 점수 (0~5) |
|---|---|---|---|---|
| moai-bi:executive-summary | status | 7개 | 3개 | **4** |
| moai-finance:financial-statements | financial | 6개 | 4개 | **4** |
| moai-business:sbiz365-analyst | plan | 6개 | 3개 | **4** |
| moai-business:daily-briefing | status | 5개 | 3개 | **4** |

**점수 기준**:
- 5 = 모든 섹션 완전 매핑, 추가 작업 불필요
- 4 = 핵심 섹션 매핑 완료, 일부 섹션 창의적 재해석 필요
- 3 = 주요 섹션 매핑 가능하나 상당한 구조 조정 필요
- 2 = 부분적 매핑만 가능, 별도 커스텀 모드 권장
- 1 = 호환성 없음, 새 모드 필요

### Phase 1 (P1) 권장 체인 통합 결론

**4건 모두 사용 가능 (호환성 점수 4/5)**

모든 P1 소비 스킬이 지정된 html-report 모드로 렌더링 가능함을 확인했습니다. 각 스킬 출력의 핵심 정보(수치·헤드라인·액션·리스크)는 템플릿 슬롯에 매핑되며, 미매핑 세부 섹션은 마크다운 원본 보고서에서 보완 참조하도록 안내하는 사용 패턴이 권장됩니다.

**주요 제약 사항**:
- financial-statements의 재무제표 전체 세트(상태표+현금흐름표)는 financial 템플릿 단일 파일 50KB 제한으로 손익계산서 핵심 항목 위주로 압축 필요.
- sbiz365-analyst의 5대 상세 분석 수치표는 plan 모드 내에 전부 수용하기 어렵고, 핵심 요약 + 타당성 판정 + 리스크 + 결론 중심 렌더링 권장.
- executive-summary의 Now What 의사결정 옵션 구조는 carryover 슬롯 재활용으로 표현하나, 향후 `decisions` 전용 컴포넌트 추가 시 더 자연스러운 렌더링 가능.
- daily-briefing은 경쟁사·규제 상세 섹션을 위한 status 템플릿 확장 여지가 있으나, 현재 구조로도 핵심 정보 전달에 충분.

---

*작성: moai-content:html-report Wave 3 통합 검증 | html-report v2.2.0*
