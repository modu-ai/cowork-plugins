---
title: "재무 트랙"
weight: 60
description: "세무 · 결산 · 예산 자동화 - financial-statements → xlsx-creator → ai-slop-reviewer"
geekdocBreadcrumb: true
---

# 재무 트랙 — 세무 · 결산 · 예산 자동화

> 재무팀, 회계사, 재무 분석가를 위한 트랙입니다. **재무제표 생성 → 엑셀 리포트 → 세무 검수** 3단계로 재무 업무 전체를 자동화합니다. 결산 작업부터 세무 신고, 예산 분석까지 재무 리스크 관리를 커버합니다.

## 트랙 개요

### 🎯 학습 목표

- 재무제표 생성 및 분석(`financial-statements`, `tax-helper`) 전문 스킬 활용법
- 재무 리포트 자동 생성(`xlsx-creator`) 기술
- 세무 검수 및 품질 관리(`ai-slop-reviewer`) 프로세스
- 재무 업무의 완전 자동화 워크플로우

### 📋 준비물

```
[ ] financial-statements, tax-helper, close-management, variance-analysis, xlsx-creator, ai-slop-reviewer 스킬 접근 권한
[ ] 회사 재무 데이터 (전표, 잔고, 매출, 비용 데이터)
[ ] 회계 템플릿 (재무제표, 세무 신서식, 결산 서식)
[ ] 데이터 저장소 (D:/Projects/finance-data/raw/)
[ ] 샘플 재무 데이터 및 세무 문서
```

## Step 1 — 플러그인 스캐폘드 구축 (10분)

```bash
# 프로젝트 폴더 구조
D:/Projects/finance-automation/
└── finance-assistant/
    ├── .claude-plugin/
    │   └── plugin.json
    ├── templates/
    │   ├── financial-statements/
    │   ├── tax-documents/
    │   └── budget-analysis/
    ├── data/
    │   ├── accounting/
    │   ├── budget/
    │   └── tax/
    ├── reports/
    │   ├── monthly/
    │   ├── quarterly/
    │   └── annual/
    └── skills/
        ├── financial-reporter/
        ├── tax-processor/
        ├── budget-analyzer/
        └── finance-reviewer/
```

플러그인을 생성하는 명령어:

```text
D:/Projects/finance-automation/finance-assistant/ 폴더에 플러그인을 생성해줘.

- plugin.json에 name: "finance-assistant", version: "1.0.0", description: "재무 업무 자동화 — 결산, 세무, 예산 분석"
- skills 배열은 일단 비워두고, 이후 스킬 추가 시 채워줘
```

## Step 2 — 재무제표 생성 스킬 (25분)

첫 번째 스킬로 `financial-statements`를 활용한 재무제표 생성 스킬을 만듭니다.

```text
finance-assistant/skills/financial-reporter/SKILL.md 파일을 생성해줘。

name: financial-reporter
description: 재무제표 자동 생성 및 분석. 손익계산서, 대차대조표, 현금흐름표를 자동으로 생성하고 분석하여 재무 건전성 평가.
  트리거 — "재무제표 생성", "결산 작업", "재무 분석", "/finance report"

본문 절차:
1. 재무 데이터 로드 및 전처리:
   - 회사 회계 데이터 로드 (전표, 잔고, 거래 내역)
   - 데이터 분류 (매출, 비용, 자산, 부채, 자본)
   - 기간별 데이터 정리 (월별, 분기별, 연별)
   - 원화/외화 환율 적용 (해외 거래가 있을 경우)
2. financial-statements 스킬 호출:
   - 손익계산서 생성 (매출 - 비용 = 영업이익)
   - 대차대조표 생성 (자산 = 부채 + 자본)
   - 현금흐름표 생성 (영업, 투자, 재무 활동)
   - 재무 비율 계산 (유동비율, 부채비율, 이익률 등)
3. 재무제표 구성 요소:
   - 기본 재무제표 3종
   - 재무 비율 분석
   - 추이 분석 (전기 대비 변동률)
   - 산업별 벤치마킹 데이터
4. 분석 기법 적용:
   - 수익성 분석 (이익률, ROA, ROE)
   - 안정성 분석 (유동비율, 부채비율)
   - 성장성 분석 (매출 성장률, 이익 성장률)
   - 활동성 분석 (자산 회전율, 재고 회전율)
5. 출력 형식:
   - 재무제표 엑셀 파일 (.xlsx)
   - 재무 비율 요약 보고서
   - 주요 재무 지표 KPI
   - 개선 제안 사항
```

### 🧪 테스트 명령어

```text
# 2024년 결산 재무제표 생성해줘
# 데이터: 매출 100억원, 비용 70억원, 자산 200억원, 부채 120억원
# 손익계산서, 대차대조표, 현금흐름표 3종 생성
# 주요 재무 비율 계산 포함

# 분기별 재무 추이 분석해줘
# 1분기 ~ 4분기 데이터로 성장성, 안정성, 수익성 분석
# 전기 대비 변동률, 산업 평균 대비 비교
```

## Step 3 — 세무 처리 스킬 (20분)

두 번째 스킬로 `tax-helper`를 활용해 세무 문서를 처리합니다.

```text
finance-assistant/skills/tax-processor/SKILL.md 파일을 생성해줘。

name: tax-processor
description: 세무 문서 자동 처리 및 세금 계산. 법인세, 부가가치세, 소득세 등 세금 계산 및 신고서 생성, 세무 리스크 평가.
  트리거 — "세무 처리", "세금 계산", "세무 신고", "/finance tax"

본문 절차:
1. 세무 정보 수집 및 분류:
   - 회사 형태 (법인, 개인, 법인사업자)
   - 사업 유형 (제조, 서비스, 도매, 소매)
   - 세무 관련 데이터 (매출, 매입, 공제 내역)
   - 과세 기간 (월별, 분기별, 연별)
2. tax-helper 스킬 호출:
   - 법인세 계산 (소득금액 - 필요경비 = 과세표준)
   - 부가가치세 계산 (매출세액 - 매입세액 = 납부세액)
   - 소득세 계산 (근로소득, 사업소득 등)
   - 지방세 계산 (재산세, 주민세 등)
3. 주요 세금 계산 항목:
   - 법인세: 법인세율 적용, 세액 계산
   - 부가가치세: 면세공제, 영세율 적용
   - 종합소득세: 소득별 세율 누진 적용
   - 기타 세금: 교육세, 농특세 등
4. 세무 문서 생성:
   - 법인세 신고서
   - 부가가치세 신고서
   - 종합소득세 신고서
   - 기타 신고서류
5. 세무 리스크 평가:
   - 과다 납부 리스크
   - 탈세 리스크
   - 기한 초과 리스크
   - 서류 미비 리스크
6. 출력 형식:
   - 세금 계산 요약 보고서
   - 세무 신고서 양식
   - 납부 예상 세액
   - 세무 리스크 평가
```

### 🧪 테스트 명령어

```text
# 법인세 신고서 생성해줘
# 법인 ABC Corp, 과세표준 20억원, 법인세율 25%
 손금경비 처리, 세액 공제 포함
 정액공제 적용, 법인세 최종 계산

# 부가가치세 신고서 작성해줘
# 매출세액 5억원, 매입세액 3억원, 영세율 적용 대상
# 면세공제, 공제세액 계산, 납부세액 결정
```

## Step 4 — 결산 관리 스킬 (20분)

세 번째 스킬로 `close-management`를 활용해 결산을 관리합니다.

```text
finance-assistant/skills/close-manager/SKILL.md 파일을 생성해줘。

name: close-manager
description: 월간/분기별/연간 결산 자동 관리. 회계기간 종료 후 자동으로 결산 프로세스를 진행하고 보고서를 생성.
  트리거 — "결산 작업", "월간 마감", "분기 결산", "연간 결산", "/finance close"

본문 절차:
1. 결산 사전 준비:
   - 회계기간 확인 (월별, 분기별, 연별)
   - 데이터 완전성 검증 (전표, 잔고, 거래 내역)
   - 조정 필요 항목 식별 (미결산, 미지출, 미수금)
   - 결산 일정 검토 (마감일, 검수일)
2. close-management 스킬 호출:
   - 자동 조정 항목 처리
   - 회계기간 종료 처리
   - 재무제표 생성
   - 결산 보고서 작성
3. 결산 프로세스 단계:
   - Stage 1: 데이터 검증 및 정제
   - Stage 2: 자동 조정 항목 처리
   - Stage 3: 재무제표 생성
   - Stage 4: 결산 검수
   - Stage 5: 보고서 생성
4. 조정 항목 처리:
   - 미결산 전표 작성
   - 감가상각비 계산
   - 매출채권/매입채권 조정
   - 재고자산 평가
5. 출력 형식:
   - 결산 진행 상황 보고서
   - 조정 항목 목록
   - 완성된 재무제표
   - 결산 검수 보고서
```

### 🧪 테스트 명령어

```text
# 4월 분기 결산 작업해줘
# 1분기 ~ 3분기 데이터 집계
# 자동 조정 항목 처리, 재무제표 생성
# 결산 보고서 작성

# 2024년 연간 결산 작업해줘
# 연간 누계 데이터 집계
 감가상각비 계산, 매출채권 조정
 연간 재무제표 생성, 결산 검수
```

## Step 5 — 예산 분석 스킬 (15분)

네 번째 스킬로 `variance-analysis`를 활용해 예산 분석을 수행합니다.

```text
finance-assistant/skills/budget-analyzer/SKILL.md 파일을 생성해줘。

name: budget-analyzer
description 예산 대비 실적 분석 및 편차 분석. 예산과 실적을 비교하여 편차 원인을 분석하고 개선 방안을 제시.
  트리gger — "예산 분석", "편차 분석", "예산 관리", "/finance budget"

본문 절차:
1. 예산 및 실적 데이터 준비:
   - 예산 데이터 로드 (부문별, 항목별)
   - 실적 데이터 로드 (동일 기간)
   - 데이터 정합성 검증
   - 분석 기간 설정 (월별, 분기별, 누적)
2. variance-analysis 스킬 호출:
   - 예산 대비 실적 비교
   - 편차율 계산 ((실적-예산)/예산*100)
   - 편차 원인 분석
   - 추세 분석 (시간별 변동 패턴)
3. 분석 수준:
   - 부문별 분석 (영업, 생산, 관리)
   - 항목별 분석 (인건비, 원자재, 광비용)
   - 시간별 분석 (월별, 분기별 누적)
   - 예측 분석 (향후 추세 예측)
4. 편차 분석 항목:
   - 유리 편차 (실적 > 예산)
   - 불리 편차 (실적 < 예산)
   - 원인 분석 (내부적, 외부적)
   - 개선 방안 (단기, 장기)
5. 출력 형식:
   - 예산 대비 실적 비교 보고서
   - 편차 분석 결과
   - 개선 제안 사항
   - 예측 분석 보고서
```

### 🧪 테스트 명령어

```text
# 2분기 예산 대비 실적 분석해줘
# 영업부문: 예산 50억원, 실적 45억원 (불리 10%)
# 생산부문: 예산 30억원, 실적 33억원 (유리 10%)
# 부문별 편차 원인 분석, 개선 방안 제시

# 연간 예집 대비 실적 추이 분석해줘
# 월별 누계 데이터로 분기별 추이 분석
# 주요 편차 요인 식별, 예측 모델 적용
```

## Step 6 — 엑셀 리포트 생성 스킬 (15분)

다섯 번째 스킬로 `xlsx-creator`를 활용해 재무 리포트를 생성합니다.

```text
finance-assistant/skills/report-generator/SKILL.md 파일을 생성해줘。

name: report-generator
description: 재무 보고서 자동 생성. 다양한 분석 결과를 전문적인 엑셀 리포트로 통합하여 경영진 보고용으로 제작.
  트리거 — "재무 보고서", "경영진 보고", "분석 결과 리포트", "/finance excel"

본문 절차:
1. 리포트 구조 설계:
   - 실행 요약 (KPI 대시보드)
   - 재무제표 시트
   - 세무 분석 시트
   - 예산 분석 시트
   - 개선 제안 시트
2. xlsx-creator 스킬 호출:
   - 템플릿 적용 및 구조화
   - 데이터 삽입 및 서식 적용
   - 차트 및 그래프 추가
   - 계산 공식 및 피벗 테이블 생성
3. 리포트 요소:
   - KPI 대시보드 (주요 재무 지표)
   - 재무제표 표준 양식
   - 세금 계산 요약
   - 예집 대비 실적 비교
   - 트렌드 분석 차트
4. 시각화 요소:
   - 막대차트 (예산 vs 실적)
   - 선차트 (추이 분석)
   - 원차트 (비중 분석)
   - 히트맵 (부문별 성과)
5. 출력 형식:
   - 엑셀 파일 (.xlsx) (D:/Projects/finance-reports/)
   - PDF 버전 (인쇄용)
   - 프레젠테이션용 차트
   - 데이터 사전
```

### 🧪 테스트 명령어

```text
# 경영진용 재무 보고서 생성해줘
# 5개 시트 구성: 요약, 재무제표, 세무, 예산, 개선안
# KPI 대시보드, 피벗 테이블, 다양한 차트 포함

# 투자자용 재무 분석 보고서 생성해줘
# 성장성, 수익성, 안정성 분석 포함
# 투자 매력도 평가, 향전 전망 제시
```

## Step 7 — 품질 검수 스킬 (15분)

여섯 번째 스킬로 `ai-slop-reviewer`를 활용해 재무 문서를 검수합니다.

```text
finance-assistant/skills/finance-reviewer/SKILL.md 파일을 생성해줃。

name: finance-reviewer
description: 재무 문서 최종 검수 및 전문성 강화. 재무 데이터의 정확성과 전문성을 검증하고 경영 의사결정에 활용할 수 있도록 완성도를 높임.
  트리거 — "재무 검수", "최종 검토", "보고서 완성", "/finance final"

본문 절차:
1. ai-slop-reviewer 스킬 호출:
   - 재무 용어 정확성 검증
   - 계산 결과 정확성 확인
   - 전문가 수준의 표현 검수
   - 보고서 구조 검토
2. 검수 항목 상세:
   - 숫자 정확성 (계산, 변동률, 비율)
   - 용어 정확성 (회계 용어, 재무 용어)
   - 논리적 일관성 (데이터 간 관계)
   - 전문성 (경영진 수준의 표현)
3. 품질 기준 적용:
   - 데이터 정확성 (±1% 이내 오차 허용)
   - 계산 방법 정확성 (회계 기준 준수)
   - 표현 전문성 (경영진 수준)
   - 가독성 (명확한 구조, 시각화)
4. 개선 적용:
   - 계산 오류 수정
   - 용어 표준화
   - 표현 전문성 강화
   - 구조적 개선
5. 출력 형식:
   - 최종 검수 완료 문서
   - 검수 보고서
   - 오류 수정 내역
   - 품질 등급 평가
```

### 🧪 테스트 명명어

```text
# 재무제표 검수해줘
# 계산 정확성, 용어 정확성, 논리적 일관성 검토
# 전문가 수준의 재무 표현으로 개선

# 경영진 보고서 최종 검수해줘
# KPI 정확성, 분석 깊이, 전문성 평가
# 경영 의사결정에 활용 가능한 수준으로 완성
```

## Step 8 — 체인 연결 및 자동화 (15분)

모든 스킬을 체인으로 연결하고 실제 재무 업무에 적용합니다.

### 🔗 체인 설정

```text
# 월간 결산 체인
"4월 결산 작업해줘" → close-manager → financial-reporter → tax-processor → report-generator → finance-reviewer

# 예산 분석 체인
"2분기 예집 분석해줘" → budget-analyzer → report-generator → finance-reviewer

# 투자자 보고서 체인
"투자자용 분석 보고서 만들어줘" → financial-reporter → budget-analyzer → report-generator → finance-reviewer
```

### ⏰ 스케줄링 설정

```text
/schedule

매월 1일 09:00에 finance-assistant의 close-manager 스킬을 실행해줘.
분기 마감일 (3/6/9/12월 말)에 financial-reporter 자동 실행.

실패 시 Slack #finance-alerts 채널로 오류 알림 전송.
```

## 성공 검증 체크리스트

```
[ ] financial-reporter 실행 → 재무제표 생성 확인
[ ] tax-processor 실행 → 세무 계산 및 문서 생성 확인
[ ] close-manager 실행 → 결산 관리 확인
[ ] budget-analyzer 실행 → 예산 분석 확인
[ ] report-generator 실행 → 엑셀 리포트 생성 확인
[ ] finance-reviewer 실행 → 품질 검수 확인
[ ] 체인 연결 → 6개 스킬 연속 실행 테스트 성공
[ ] 실제 재무 데이터 테스트 → 실제 회계 데이터로 테스트 완료
```

## 자주 발생하는 문제 해결

### 🚨 계산 오류

**원인:** 복잡한 재무 계산에서 오류 발생

**해결:** 다중 계산 검증 시스템
```text
# 계산 검증 시스템
1. 자동 계산 재검증
2. 수동 계산과의 비교
3. 이전 기간과의 비교
4. 산업 평균과의 비교
```

### 📊 데이터 불일치

**원인:** 여러 데이터 소스 간 불일치

**해결:** 데이터 정합성 검증
```text
# 데이터 정합성 검사
1. 원천 데이터 vs 집계 데이터 비교
2. 재무제표 항목 간 관계 검증
3. 이월 처리 확인
4. 환율 적용 일관성 확인
```

### 🔍 분석 깊이 부족

**원인:** 단순한 수치 비교에 그칠 경우

**해결:** 다차원 분석 시스템
```text
# 다차원 분석
1. 시간적 분석 (추이, 주기성)
2. 공간적 분석 (부문별, 지역별)
3. 원인 분석 (내부적, 외부적)
4. 예측 분석 (회귀, 시계열)
```

## 확장 아이디어

### 🎯 고급 활용

1. **실시간 재무 모니터링**:
   ```text
   # 실시간 재무 모니터링 체인
   "실시간 재무 모니터링" → real-time-data → alert-system → dashboard-update
   ```

2. **예측 분석 시스템**:
   ```text
   # 재무 예측 체인
   "재무 예측 분석" → historical-data → predictive-model → forecast-report
   ```

3. **자동 세금 계획**:
   ```text
   # 세금 최적화 체인
   "세금 계획 수립" → tax-optimization → scenario-analysis → recommendation
   ```

## 관련 자료

- [financial-statements 재무제표 생성 가이드](../../plugins/moai-finance/financial-statements/)
- [tax-helper 세무 처리 전문](../../plugins/moai-finance/tax-helper/)
- [close-management 결산 관리](../../plugins/moai-finance/close-management/)
- [variance-analysis 예산 분석](../../plugins/moai-finance/variance-analysis/)
- [xlsx-creator 재무 리포트 생성](../../plugins/moai-office/xlsx-creator/)

---

### Sources
- [modu-ai/cowork-plugins — moai-finance](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)
- [국세청 전자세무서](https://hometax.nts.go.kr/)
- [회계법인 재무 가이드](https://www.kr-icpa.or.kr/)
- [재무분석 전문가 협회](https://www.kfas.or.kr/)