---
title: "AI 사원 실습 2"
weight: 140
description: "품질·SCM 부서 AI 실습 — 일일 불량 대시보드, 이상 탐지, 벤더 리스크 주간 스캔."
geekdocBreadcrumb: true
tags: [cookbook, ai-employee, operations]
---

# AI 사원 랩 2 — 품질·SCM 부서 AI

> [랩 1 — 재무 대리 AI](../ai-employee-lab-1/)에서 기본 설계를 경험했다면, 랩 2는 **현장 공장 데이터**와 **다중 벤더 모니터링**이라는 더 실무적인 영역을 다룹니다.

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
{{< terminal title="claude — cowork" >}}

> ## Part 1 — quality-ops 플러그인

### Step 1-1. 스캐폴드

```text
D:/Projects/quality-ops/quality-ops/ 폴더에 플러그인 스캐폴드를 만들어줘.
plugin.json description: "품질 관제 AI — 일일 불량 대시보드와 이상 탐지"
{{< /terminal >}}

### Step 1-2. 불량 대시보드 스킬

```text
> quality-ops/skills/defect-dashboard/SKILL.md를 만들어줘.

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

### Step 1-3. 이상 탐지 스킬

```text
> quality-ops/skills/anomaly-alert/SKILL.md를 추가해줘.

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

### Step 1-4. Schedule 등록

{{< terminal title="claude — cowork" >}}
> /schedule

매일 07:00에 quality-ops의 defect-dashboard 스킬을 실행해줘.
실행 후 즉시 anomaly-alert 스킬도 체이닝으로 실행해줘.
{{< /terminal >}}

## Part 2 — scm-watcher 플러그인

### Step 2-1. 스캐폴드

{{< terminal title="claude — cowork" >}}
> D:/Projects/scm-watcher/scm-watcher/ 폴더에 플러그인을 만들어줘.
plugin.json description: "공급망 리스크 모니터링 AI — 벤더 뉴스·주가·공시 스캔"
{{< /terminal >}}

### Step 2-2. 벤더 리스크 스캔 스킬

```text
> scm-watcher/skills/vendor-risk-scan/SKILL.md를 만들어줘.

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

### Step 2-3. 긴급 공시 알림 스킬

```text
> scm-watcher/skills/disclosure-alert/SKILL.md를 추가해줘.

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

### Step 2-4. Schedule 등록

{{< terminal title="claude — cowork" >}}
> /schedule

매주 월 08:00에 scm-watcher의 vendor-risk-scan 실행해줘.
매일 17:00에 disclosure-alert 실행해줘.
{{< /terminal >}}

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

## 다음 읽을거리

- [트랙 — 데이터 분석](../track-data/)
- [트랙 — 마케팅](../track-marketing/)
- [AI 사원 설계](../ai-employee-design/)
- [최종 프로젝트](../final-project/)

---

### Sources
- [Claude Docs — Sub-agents](https://docs.claude.com/en/docs/claude-cowork/sub-agents)
- [modu-ai/cowork-plugins — moai-data, moai-operations](https://github.com/modu-ai/cowork-plugins)
