---
title: "랩 1 - 기초 실습"
weight: 90
description: "Cowork 기초 다지기: 플러그인 생성, 스킬 개발, Schedule 등록 실습"
geekdocBreadcrumb: true
---

# 랩 1 — Cowork 기초 실습

> [커리큘럼 개요](../)의 1-2주차 과제입니다. 재무 대리 AI를 만들면서 Cowork 기본기를 다집니다.

## 랩 목표

끝났을 때 결과물:

- `finance-assistant` 플러그인 1개 (스킬 3개)
- 매일 08:50 자동 실행되는 Schedule 1개
- Slack `#finance-daily` 채널에 자동 게시되는 일일 브리핑

## 사전 준비

```
[ ] Cowork 설치·로그인 완료 (Pro 이상)
[ ] Slack MCP 커넥터 연결 완료 (#finance-daily 채널 쓰기 권한)
[ ] Gmail MCP 커넥터 연결 완료 (읽기 권한)
[ ] Claude 프로젝트 폴더 생성 — 예: D:/Projects/finance-ai/
[ ] 샘플 CSV — D:/Projects/finance-ai/samples/pending-invoices.csv
    (아래 섹션에서 제공)
```

샘플 CSV는 다음 구조로 맞추세요.

```csv
invoice_no,vendor,amount,due_date,status
INV-2026-0412,ACME Logistics,12500000,2026-04-25,pending
INV-2026-0418,Beta Supplies,4800000,2026-04-30,pending
INV-2026-0420,Gamma Software,3200000,2026-05-02,pending
```

## 실습 과제

### Week 1: 플러그인 생성 및 첫 번째 스킬

#### Step 1 — 플러그인 스캐폴드 (5분)

프로젝트 폴더에 빈 플러그인을 만듭니다.

```text
D:/Projects/finance-ai/
├── finance-assistant/
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── (빈 폴더)
└── samples/
    └── pending-invoices.csv
```

Cowork에 이렇게 지시하세요.

{{< terminal title="claude — cowork" >}}
> D:/Projects/finance-ai/finance-assistant/ 폴더에 플러그인 스캐폴드를 만들어줘.

  - .claude-plugin/plugin.json에 name, version 0.1.0, description 작성
  - description: "재무 대리 AI — 환율·미결·월마감·현금흐름 자동화"
  - skills 배열은 일단 빈 배열로 두고, 이후 스킬 추가 시 채워줘
{{< /terminal >}}

#### Step 2 — 일일 브리핑 스킬 (10분)

첫 번째 스킬을 만듭니다.

```text
> finance-assistant/skills/daily-briefing/SKILL.md 파일을 만들어줘.

name: daily-briefing
description: 매일 아침 환율 3종 조회 + 미결 메일 분류 후
  Slack #finance-daily 채널에 게시한다.
  트리거 — "일일 재무 브리핑", "환율 브리핑", "/finance daily"

본문 절차:
1. WebFetch로 naver.com/finance에서 KRW/USD, KRW/JPY, KRW/EUR 조회
2. 전일 대비 변동률 계산, ±1% 이상이면 "경고" 마커 부착
3. Gmail 받은편지함에서 어제 00:00 이후 안 읽은 메일 중
   "인보이스·결제·정산" 키워드 포함 메일 분류
4. D:/Projects/finance-ai/samples/pending-invoices.csv의 미결 건수 조회
5. Slack #finance-daily 채널에 Markdown 형식으로 게시:
  - 헤더: "YYYY-MM-DD 재무 브리핑"
  - 섹션 1: 환율 3종 (변동률 표시)
  - 섹션 2: 신규 결제·인보이스 메일 N건 (발신자·제목·금액)
  - 섹션 3: 미결 인보이스 총액
```

스킬이 만들어지면 Cowork가 자동으로 SKILL.md를 로드합니다. 수동 테스트:

{{< terminal title="claude — cowork" >}}
> 일일 재무 브리핑 실행해줘
{{< /terminal >}}

성공하면 Slack에 Markdown 카드가 올라옵니다. 실패 원인 대부분은 MCP 권한 부족입니다.

#### Step 3 — Schedule 등록 (5분)

이 단계가 이번 랩의 하이라이트입니다. 매일 아침 출근하기 전에 PC 스스로 알아서 재무 데이터를 정리해 Slack에 올리도록 만드는 작업이에요. 한 번만 등록해 놓으면 잊어버려도 매일 8시 50분에 자동으로 돌아갑니다.

Cowork 대화창에 아래와 같이 자연어로 입력하면 됩니다. 슬래시 명령 `/schedule` 한 줄을 먼저 적고, 줄을 바꿔 "언제·무엇을·실패하면 어떻게"를 한국어로 풀어 쓰면 Cowork가 알아서 cron 표현식과 핸들러를 생성합니다.

{{< terminal title="claude — cowork" >}}
> /schedule

매일 08:50에 finance-assistant의 daily-briefing 스킬을 실행해줘.
시간대는 로컬 PC 기준 (Asia/Seoul).
실패 시 카카오톡 "나에게 보내기"로 오류 알림 전송.
{{< /terminal >}}

Cowork가 다음과 같은 확인 폼을 띄웁니다 — 빨간 버튼이 아니라 "승인" 초록 버튼을 누르면 예약이 등록됩니다.

```text
[Schedule 등록 확인]
  • 이름: finance-daily-briefing
  • 빈도: 매일 08:50 (Asia/Seoul)
  • 실행 대상: finance-assistant / daily-briefing
  • 실패 알림: 카카오톡 나에게 보내기 (kakaotalk-memo MCP)
  • 다음 실행 예정: 내일 08:50
  → [승인]  [취소]
```

**왜 08:50인가요?** 9시 출근 회의 직전입니다. PC를 켜고 커피를 내리는 동안 브리핑이 Slack에 도착해 있어요. 만약 9시 회의에 늦지 않게 더 일찍 받고 싶다면 08:30이나 08:00으로 바꿔도 됩니다.

**확인 방법** — 다음 날 아침 8시 50분 직전까지 사무실 PC를 켜둔 채로 두면 됩니다. PC가 켜져 있고 Cowork가 백그라운드에서 실행 중이어야 자동 실행이 동작합니다. 8시 51분에 Slack `#finance` 채널에 카드가 올라와 있으면 성공이에요. 만약 카드가 안 올라오면 Cowork 앱 화면 좌측 하단의 시계 모양 아이콘(예약 작업 패널)을 눌러서 "마지막 실행: 실패" 표시가 있는지 확인하세요. 카카오톡 나에게 보내기에도 오류 메시지가 도착해 있을 겁니다.

> **자주 하는 실수** — PC를 끄거나 절전 모드로 들어가면 그 회차는 그냥 스킵됩니다 (자동으로 다음 시간에 다시 안 돌려요). 출근 전에 PC를 꼭 켜두세요. 노트북이라면 전원 어댑터 연결 + 절전 모드 비활성화를 권장합니다.

#### Week 1 자가 퀴즈

**Q1.** 플러그인을 생성할 때 가장 먼저 설정해야 할 필수 항목은 무엇인가요?
**Q2.** 스킬이 자동으로 실행되도록 하려면 어떤 설정이 필요한가요?
**Q3.** MCP 커넥터 연결이 실패하는 가장 흔한 원인은 무엇인가요?

### Week 2: 추가 스킬 개발 및 테스트

#### Step 4 — 월마감 스킬 추가 (10분)

두 번째 스킬. 자동 실행이 아니라 "수시 호출" 전용입니다.

```text
> finance-assistant/skills/monthly-close/SKILL.md 파일을 추가해줘.

name: monthly-close
description: 월마감 긴급 조회. 이번 달 미결 전표·미수금·지급 예정 요약.
  트리거 — "월마감 긴급", "이번달 미결 확인", "/finance close"

본문 절차:
1. D:/ERP/monthly/YYYY-MM.xlsx 파일이 있으면 열고,
   없으면 D:/Projects/finance-ai/samples/pending-invoices.csv로 대체
2. 이번 달 미결 전표 건수 + 총액 집계
3. 지급 예정일이 7일 이내인 건 별도 강조
4. Markdown 테이블로 결과 제시 — Slack 게시는 하지 않고
   Cowork 대화창에 표시
```

테스트:

{{< terminal title="claude — cowork" >}}
> 월마감 긴급 확인해줘
{{< /terminal >}}

모바일에서도 같은 지시를 내려 Dispatch 동작을 확인하세요.

{{< terminal title="claude — cowork" >}}
> (모바일 Claude 앱)
내 사무실 PC에서 월마감 긴급 확인해줘
{{< /terminal >}}

#### Step 5 — 주간 현금흐름 스킬 (10분)

세 번째 스킬. 스케줄 + 수동 호출 둘 다 지원.

```text
> finance-assistant/skills/weekly-cashflow/SKILL.md 파일을 추가해줘.

name: weekly-cashflow
description: 주간 현금흐름 요약. 지난주 입출금 내역 + 이번 주 예측.
  트리거 — "주간 현금흐름", "/finance weekly"

본문 절차:
1. D:/Finance/weekly/에서 가장 최근 주차 파일 로드
2. 입출금 카테고리별 집계 (매출·매입·인건비·기타)
3. 이번 주 지급 예정·입금 예정 일정 추출
4. PPT 5장 생성:
  - 1장: 요약 (주요 수치)
  - 2장: 카테고리별 그래프
  - 3장: 지급 예정
  - 4장: 입금 예정
  - 5장: 리스크 경고
5. D:/Projects/finance-ai/output/ 폴더에
   weekly-cashflow-YYYY-WW.pptx로 저장
6. Notion "주간 현금흐름" 페이지에 요약 텍스트 + PPT 링크 추가
```

Schedule 추가:

이번에는 매주 월요일 한 번만 도는 주간 리포트입니다. 일일 브리핑(매일 08:50)과 비슷한 패턴인데, 빈도만 "매주 월요일 오전 9시"로 달라요. 입력 형식도 동일합니다. Cowork는 "매주 월요일 09:00"을 cron 표현식 `0 9 * * 1`로 자동 변환합니다.

{{< terminal title="claude — cowork" >}}
> /schedule

매주 월요일 09:00에 finance-assistant의 weekly-cashflow 스킬을 실행해줘.
시간대는 로컬 PC 기준 (Asia/Seoul).
실패 시 카카오톡 나에게 보내기로 오류 알림 전송.
{{< /terminal >}}

월요일 출근 직후 PPT 5장이 자동으로 만들어지고 Notion에 업로드되어 있다면 정상 동작입니다. 일일 브리핑(daily-briefing)과 주간 리포트(weekly-cashflow) 둘 다 동작 중이라면 Cowork 좌측 하단 예약 작업 패널에 두 개의 항목이 표시됩니다.

## 검증 체크리스트

랩을 끝내기 전에 다음을 모두 확인하세요.

```
[ ] plugin.json에 skills 배열 3개 모두 등록됨
[ ] daily-briefing 수동 실행 → Slack 게시 성공
[ ] monthly-close 수동 실행 → 대화창 표시 성공
[ ] weekly-cashflow 수동 실행 → PPT 생성 성공
[ ] Schedule 08:50 자동 실행 확인 (다음 날 아침)
[ ] Schedule 월 09:00 자동 실행 확인 (다음 월요일)
[ ] Dispatch — 모바일에서 "월마감 긴급" 호출 → PC 실행 성공
[ ] MCP 권한 — Slack 쓰기 / Gmail 읽기 / Notion 쓰기 확인
```

## 자주 걸리는 지점

### 스킬이 자동 트리거되지 않음

원인은 대부분 **description 키워드 부족**입니다. "일일 재무 브리핑"이라고만 적어두면 "환율 확인해줘"라는 자연어에는 매칭되지 않습니다. description 본문에 동의어 3~5개를 쉼표로 나열하세요.

### Slack 메시지가 깨짐

Markdown 형식을 지정하지 않고 그냥 텍스트로 전송했을 가능성. Slack MCP는 `mrkdwn: true` 플래그가 필요합니다. SKILL.md에 "Slack Block Kit 또는 mrkdwn 형식 사용" 문구를 추가하세요.

### Schedule이 실행 안 됨

세 가지 중 하나:

1. PC가 08:50에 꺼져 있었음 (회차 스킵됨 — 자동 보충 안 됨)
2. Claude Desktop이 닫혀 있었음
3. Schedule 승인 시 MCP 쓰기 권한을 승인하지 않았음

Schedule 로그는 Cowork 탭 → 예약 작업 섹션에서 확인할 수 있습니다.

### Dispatch가 엉뚱한 PC로 감

Dispatch는 **가장 최근 사용 PC**로 라우팅됩니다. 퇴근 후 집 PC로 로그인했다면, 다음 Dispatch는 집 PC로 갑니다. 자세한 규칙은 [자동화 레시피](../../automation-recipes/)를 참고하세요.

## Week 2 자가 퀴즈

**Q1.** 수동 호출용 스킬과 자동 실행용 스킬의 주요 차이점은 무엇인가요?
**Q2.** Dispatch 기능이 동작하려면 어떤 조건이 필요한가요?
**Q3.** 주간 현금흐름 스킬에서 가장 중요한 데이터는 무엇이며 왜 중요한가요?

## 학습 포인트

### 기술 습득
- 플러그인 스캐폴드 생성 방법
- 스킬 기본 구조 및 설계 원리
- MCP 커넥터 연결 및 권한 관리
- Schedule 설정 및 자동화 실행
- Dispatch 기능 활용법

### 실무 적용
- 재무 업무 자동화 사례
- 데이터 처리 및 분석 기법
- 실시간 알림 시스템 구축
- 다양한 출력 포맷 생성 (PPT, Slack, Notion)

### 문제 해결
- MCP 권한 문제 진단
- 스킬 트리거 조건 최적화
- Schedule 실행 문제 해결
- Dispatch 라우팅 관리

## 다음 단계

랩 1이 안정화되면 [랩 2 — 품질·SCM 부서 AI](../lab-2/)로 넘어가세요. 공장 데이터와 벤더 리스크 모니터링을 함께 다룹니다.

## 다음 읽을거리

- [AI 사원 설계](../../ai-employee-design/)
- [AI 사원 실습 2](../lab-2/)
- [자동화 레시피](../../automation-recipes/)
- [예약 작업](../../../cowork/schedule/)

---

### Sources
- CTR-AX S5 · Skill 라이브 제작 + S6 · Schedule + Dispatch
- [Claude Docs — MCP Connectors](https://docs.claude.com/en/docs/claude-cowork/connectors)
- [modu-ai/cowork-plugins — moai-finance](https://github.com/modu-ai/cowork-plugins/tree/main/moai-finance)