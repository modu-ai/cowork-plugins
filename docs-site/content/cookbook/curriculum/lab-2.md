---
title: "랩 2 - 체이닝 실습"
weight: 100
description: "스킬 체이닝 마스터리: 품질·SCM AI 만들기 및 복잡한 자동화 설계"
geekdocBreadcrumb: true
---

# 랩 2 — 스킬 체이닝 실습

> [커리큘럼 개요](../)의 3-4주차 과제입니다. 품질·SCM 부서 AI를 만들면서 체이닝 기술을 익힙니다.

## 랩 목표

끝났을 때 결과물:

- `quality-ops` 플러그인 1개 (스킬 2개)
- `scm-watcher` 플러그인 1개 (스킬 2개)
- 매일 07:00 품질 대시보드 + 매주 월 08:00 벤더 리스크 스캔

## 사전 준비

```
[ ] 랩 1 완료
[ ] WebSearch·WebFetch 권한 기본 활성화
[ ] Gmail·Slack·Notion MCP 연결
[ ] 샘플 데이터 2종:
    D:/Projects/quality-ops/samples/daily-defects.xlsx
    D:/Projects/scm-watcher/samples/vendor-list.csv
```

샘플 Excel 스키마 (daily-defects.xlsx):

| date | line | product | defect_count | inspection_count | defect_rate |
|---|---|---|---|---|---|
| 2026-04-21 | L1 | Widget-A | 12 | 2000 | 0.60% |
| 2026-04-21 | L2 | Widget-B | 58 | 1800 | 3.22% |

샘플 벤더 CSV (vendor-list.csv):

```csv
vendor_id,name,category,country,risk_tier
V-0001,ACME Logistics,물류,KR,B
V-0002,Beta Electronics,전자부품,CN,A
V-0003,Gamma Chemicals,화학,JP,B
```

## Part 1 — quality-ops 플러그인

### Step 1-1. 스캐폴드

```text
D:/Projects/quality-ops/quality-ops/ 폴더에 플러그인 스캐폴드를 만들어줘.
plugin.json description: "품질 관제 AI — 일일 불량 대시보드와 이상 탐지"
```

### Step 1-2. 불량 대시보드 스킬 (Week 3)

```text
quality-ops/skills/defect-dashboard/SKILL.md를 만들어줘.

name: defect-dashboard
description: 공장 일일 불량률 대시보드. 라인별·제품별 집계,
  임계치(2%) 초과 라인 강조.
  트리거 — "불량 대시보드", "오늘 품질 리포트", "/quality daily"

본문 절차:
1. D:/Projects/quality-ops/samples/daily-defects.xlsx 로드
2. 어제 날짜 데이터만 필터링
3. 라인별 불량률 집계 — 임계치 2% 초과 라인은 빨간색 마커
4. 제품별 Top 3 불량 품목 추출
5. HTML 리포트 생성 — 90_Output/YYYY-MM-DD-quality.html
   - 헤더: 전사 평균 불량률 + 전일 대비 증감
   - 테이블 1: 라인별 불량률
   - 테이블 2: 제품별 Top 3
   - 푸터: 경고 라인 목록 + 대응 담당자
6. 공장장 Gmail(factory@company.com)로 HTML 첨부 발송
```

### Step 1-3. 이상 탐지 스킬 (Week 3)

```text
quality-ops/skills/anomaly-alert/SKILL.md를 추가해줘.

name: anomaly-alert
description: 불량률 급증 조기 경보.
  최근 7일 평균 대비 오늘 불량률이 2배 이상이면 즉시 알림.
  트리거 — "이상 탐지", "불량 급증 확인", "/quality alert"

본문 절차:
1. 최근 8일치 데이터 로드 (어제 + 지난 7일)
2. 라인·제품 조합별 최근 7일 평균 불량률 계산
3. 어제 불량률이 평균 2배 이상인 조합 추출
4. 해당 조합이 있으면:
   - Slack #quality-alert 채널에 즉시 게시
   - 메시지 포맷: @공장장 "이상 탐지 N건" + 상세 테이블
5. 없으면 "이상 없음" 대화창 응답
```

### Step 1-4. Schedule 등록 (Week 3)

```text
/schedule

매일 07:00에 quality-ops의 defect-dashboard 스킬을 실행해줘.
실행 후 즉시 anomaly-alert 스킬도 체이닝으로 실행해줘.
```

## Part 2 — scm-watcher 플러그인

### Step 2-1. 스캐폴드 (Week 4)

```text
D:/Projects/scm-watcher/scm-watcher/ 폴더에 플러그인을 만들어줘.
plugin.json description: "공급망 리스크 모니터링 AI — 벤더 뉴스·주가·공시 스캔"
```

### Step 2-2. 벤더 리스크 스캔 스킬 (Week 4)

```text
scm-watcher/skills/vendor-risk-scan/SKILL.md를 만들어줘.

name: vendor-risk-scan
description: 주요 벤더 뉴스·주가·공시를 주간 단위로 스캔하여 리스크 리포트 생성.
  트리거 — "벤더 리스크", "공급망 모니터링", "/scm weekly"

본문 절차:
1. D:/Projects/scm-watcher/samples/vendor-list.csv 로드
2. 각 벤더에 대해:
   a. WebSearch로 회사명 + 지난 7일 뉴스 검색
   b. 리스크 키워드 탐지 — "파업, 화재, 파산, 소송, 공시, 제재, 부도"
   c. 탐지 시 출처 링크와 함께 리스크 건 기록
3. 리스크 Tier A 벤더에 대해서는 주가 5% 이상 변동도 체크
4. Notion "공급망 리스크 로그" 페이지에 주차별로 섹션 추가:
   - 헤더: YYYY-WW주차
   - 리스크 탐지 건 (벤더·키워드·링크)
   - 이상 없음 벤더 수
5. 리스크 건이 3건 이상이면 Slack #scm-weekly 채널에 요약 알림
```

### Step 2-3. 긴급 공시 알림 스킬 (Week 4)

```text
scm-watcher/skills/disclosure-alert/SKILL.md를 추가해줘.

name: disclosure-alert
description: 상장 벤더 긴급 공시 실시간 모니터링.
  트리거 — "공시 확인", "DART 공시", "/scm disclosure"

본문 절차:
1. vendor-list.csv에서 상장 벤더만 필터링
2. DART(공시) 또는 해외 SEC를 WebFetch로 확인
3. 어제~오늘 공시 중 "감사의견, 회생절차, 대규모 유상증자" 키워드 탐지
4. 탐지 시:
   - 즉시 모바일 카카오톡 나에게 보내기 푸시
   - Notion 로그 페이지에도 별표(*) 마커로 기록
5. 없으면 대화창에 "공시 이상 없음" 응답
```

### Step 2-4. Schedule 등록 (Week 4)

```text
/schedule

매주 월 08:00에 scm-watcher의 vendor-risk-scan 실행해줘.
매일 17:00에 disclosure-alert 실행해줘.
```

## 검증 체크리스트

```
[ ] 두 플러그인 모두 plugin.json skills 배열 2개씩 등록됨
[ ] defect-dashboard 수동 실행 → HTML + Gmail 발송 성공
[ ] anomaly-alert 수동 실행 → 이상 없음 / 이상 탐지 분기 확인
[ ] vendor-risk-scan 수동 실행 → Notion 페이지 생성 확인
[ ] disclosure-alert 수동 실행 → 카톡 푸시 확인
[ ] Schedule 매일 07:00 / 월 08:00 / 매일 17:00 등록 확인
[ ] Dispatch — 모바일에서 "오늘 품질 리포트" → PC 실행 확인
```

## Week 3 자가 퀴즈

**Q1.** 체이닝에서 앞 스킬의 출력이 뒷 스킬의 입력이 되도록 하려면 어떤 설계가 필요한가요?
**Q2.** 이상 탐지 스킬에서 "2배 이상"이라는 기준을 동적으로 조정하려면 어떻게 해야 하나요?
**Q3.** HTML 리포트 생성 시 가장 중요한 사용자 경험 요소는 무엇인가요?

## Week 4 자가 퀴즈

**Q1.** 벤더 리스크 스캔에서 WebSearch 결과의 일관성을 유지하려면 어떤 전략을 사용해야 하나요?
**Q2.** 상장 벤더와 비상장 벤더를 처리하는 로직의 주요 차이점은 무엇인가요?
**Q3.** 공급망 리스크 모니터링에서 가장 큰 기술적 어려움은 무엇이며 어떻게 해결할 수 있나요?

## 체이닝 설계 핵심 포인트

### 데이터 흐름 설계
```
입력 데이터 → 전처리 → 분석 → 가공 → 출력
    ↓           ↓         ↓        ↓        ↓
  Excel CSV  → 필터링  → 통계  → 시각화  → HTML/Slack
```

### 체인 오류 처리
1. **입력 데이터 검증**: 파일 존재 여부, 데이터 형식 확인
2. **중간 과정 모니터링**: 각 단계별 로그 남기기
3. **출력后备 방안**: 실패 시 알림 + 수동 실행 옵션 제공

### 성능 최적화
- **병렬 처리**: 여러 벤더 검색은 서브 에이전트로 동시 실행
- **캐싱**: 반복되는 데이터는 로컬에 저장
- **스케줄링**: 실행 시간대를 분산하여 부하 분산

## 고급 기술 적용

### 동적 임계치 설정
```yaml
# SKILL.md에 설정 추가
config:
  defect_threshold: 2.0      # 불량률 임계치 (%)
  anomaly_multiplier: 2.0   # 이상 탐지 배수
  risk_keywords: ["파업", "화재", "파산", "소송", "공시", "제재", "부도"]
```

### 조건부 실행 로직
```python
# 이상 탐지 스킬의 분기 로직
if anomaly_detected:
    send_slack_alert()
    log_to_notion()
else:
    respond_normal()
```

### 데이터 연동 최적화
- **WebSearch**: 쿼리 파라미터 표준화
- **Excel/CSV**: 데이터 스키마 검증
- **MCP 연결**: 연결 상태 모니터링

## 자주 걸리는 지점

### WebSearch 결과가 일관되지 않음

WebSearch 결과는 쿼리·시간·지역 설정에 따라 달라집니다. SKILL.md에 검색 파라미터를 명시하세요.

```text
WebSearch 쿼리: "{vendor_name} 뉴스 최근 7일"
지역: KR (한국어 우선)
결과 수: 10개
```

### Slack 알림이 너무 시끄러움

초기에는 리스크 감지 기준을 느슨하게 두고 반복 실행하며 튜닝하세요. 임계치(2%)·변동률(5%)·키워드 필터는 모두 SKILL.md 본문에서 쉽게 조정 가능합니다.

### 벤더가 많으면 시간이 오래 걸림

50개 이상 벤더는 병렬 서브 에이전트 활용을 명시하세요.

```text
SKILL.md 본문에 추가:
"각 벤더 검색은 서브 에이전트로 병렬 실행. 최대 10개 동시."
```

10개 벤더 순차 5분 → 병렬 40초 정도로 단축됩니다.

### Notion 페이지가 너무 길어짐

주차별 섹션이 쌓이면 40주 뒤에는 수백 개 블록이 됩니다. SKILL.md에 "12주 이상 된 섹션은 아카이브 페이지로 이동" 규칙을 추가하세요.

## 확장 아이디어

- **CSR·ESG 모니터링** — 벤더 뉴스에 "환경·안전사고" 키워드 추가
- **가격 변동 추적** — 원자재 벤더는 주간 단가 변동을 그래프로
- **대체 벤더 추천** — 리스크 Tier A 벤더에 문제 발생 시 대체 벤더 Top 3 제안

## 다음 단계

랩 2를 완료하면 [최종 프로젝트](../final-project/)로 진행하세요. 실제 업무를 3-스킬 체인으로 자동화합니다.

## 다음 읽을거리

- [트랙 — 데이터 분석](../../track-data/)
- [트랙 — 마케팅](../../track-marketing/)
- [AI 사원 설계](../ai-employee-design/)
- [최종 프로젝트](../final-project/)

---

### Sources
- CTR-AX S6 · Schedule + Dispatch + 과제 계약 (품질·SCM 본부 레시피)
- [Claude Docs — Sub-agents](https://docs.claude.com/en/docs/claude-cowork/sub-agents)
- [modu-ai/cowork-plugins — moai-data, moai-operations](https://github.com/modu-ai/cowork-plugins)