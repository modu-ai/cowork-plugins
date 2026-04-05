# init-protocol.md — /moai init 전체 플로우

## 개요
사용자의 MoAI 초기화 프로세스를 정의합니다. 글로벌 프로필 구축, 언어/로케일 설정, 카테고리 선택, 
하네스 선택까지 6단계 Phase로 구성됩니다.

---

## Phase 0: 글로벌 프로필 감지

사용자 최초 실행 또는 기존 환경 확인:

```
IF /mnt/.auto-memory/moai-profile.md 존재
  → Phase 0-B: 프로필 재사용 확인
  → AskUserQuestion (3옵션): 재사용 / 수정 / 신규 생성
ELSE
  → Phase 1-A: 새 프로필 구축
```

### Phase 0-B: 기존 프로필 확인
**질문**: "기존 프로필을 계속 사용하시겠습니까?"
- [1] 그대로 사용
- [2] 일부 항목 수정
- [3] 새로 만들기

---

## Phase 1-A: 언어 & 기본 프로필 (4질문)

### Q1. 주 사용 언어 [header: "언어설정"]
```
선택지:
  [1] English
  [2] 한국어
  [3] 日本語
  [4] Español
  [Other]
```
**기본값**: 시스템 로케일 감지

### Q2. 근무 국가 [header: "근무국가"]
```
선택지:
  [1] 한국 (KRW, ko-KR)
  [2] 미국 (USD, en-US)
  [3] 일본 (JPY, ja-JP)
  [Other] → 사용자가 직접 국가명 입력 (전세계 모든 국가 지원)
```
**중요**: [Other] 선택 시 사용자가 입력한 국가명으로 웹검색 기반 로케일 현지화 수행.
입력된 국가의 세법, 노동법, 데이터보호법, 비즈니스 관행, 형식 표준을
웹검색으로 수집하여 `/mnt/.auto-memory/locale-context.md`에 저장한다.
**재사용**: 이미 locale-context.md가 존재하면 설문(Q2)을 건너뛰고 기존 데이터를 재사용한다.

### Q3. 역할 [header: "직무설정"]
```
선택지:
  [1] 기획PM
  [2] 마케팅
  [3] 경영전략
  [4] 연구분석
  [Other]
```

### Q4. 산업 [header: "산업설정"]
```
선택지:
  [1] IT테크
  [2] 금융핀테크
  [3] 이커머스리테일
  [4] 교육연구
  [Other]
```

**저장 위치**: `/mnt/.auto-memory/moai-profile.md`

---

## Phase 1-B: 회사/사업자 프로필 (3질문)

### Q1. 사업형태 [header: "사업설정"]
```
선택지:
  [1] 개인사업자
  [2] 법인
  [3] 프리랜서
  [4] 해당없음
```

### Q2. 회사규모 [header: "규모설정"]
```
선택지:
  [1] 1인
  [2] 2~50인
  [3] 51~200인
  [4] 200인+
```

### Q3. 업종 분류 [header: "업종설정"]
```
선택지:
  [1] IT소프트웨어
  [2] 금융핀테크
  [3] 이커머스리테일
  [4] 제조물류
  [Other]
```

**세부정보 수집**: 텍스트 대화 (하네스별 필요 여부에 따라)
- 회사명, 등록번호, 웹사이트, 회계년도 말
- 팀 규모, 핵심 KPI, 주요 과제

**저장 위치**: `/mnt/.auto-memory/moai-profile.md` (Company Profile 섹션)

---

## Phase 2: 카테고리 선택 (2단계)

### Phase 2-A: 대분류 선택 [header: "카테고리"]
```
질문: "주로 어떤 업무를 도움받고 싶으신가요?"

선택지:
  [1] 콘텐츠&마케팅 (블로그, 이메일, SNS, 광고)
  [2] 비즈니스&전략 (계획, 자동화, 분석)
  [3] 전문분야&규제 (법규, 계약, 컴플라이언스)
  [4] 라이프&커뮤니케이션 (회의, 일정, 협업)
```

**선택 저장**: `.moai/category-selection.md`

### Phase 2-B: 소분류 선택 [header: "세부분야"]
선택된 대분류에 따른 소분류:

**콘텐츠&마케팅**:
- [1] 블로그/뉴스레터
- [2] 이메일 마케팅
- [3] SNS 콘텐츠
- [4] 광고 카피

**비즈니스&전략**:
- [1] 사업 계획/OKR
- [2] 프로세스 자동화
- [3] 재무/성과 분석
- [4] 조직 최적화

**전문분야&규제**:
- [1] 법규 검토/준수
- [2] 계약서 작성/검토
- [3] 규제 대응
- [4] 리스크 관리

**라이프&커뮤니케이션**:
- [1] 회의 관리
- [2] 일정 계획
- [3] 피드백/평가
- [4] 팀 협업

---

## Phase 3: 하네스 선택 (multiSelect, 페이지네이션)

### 3-1. 설치할 하네스 선택
```
질문: "도움을 받을 하네스를 선택하세요 (다중 선택 가능)"

페이지 1/2:
  [1] copywriting (카피라이팅)
  [2] email-crafter (이메일 작성)
  [3] ad-campaign (광고 캠페인)
  [4] financial-model (재무 모델링)
  [5] 다음 (→ 페이지 2)

페이지 2/2:
  [1] sop-writer (SOP 작성)
  [2] compliance (컴플라이언스)
  [3] meeting-strategist (회의 전략)
  [4] market-research (시장 조사)
  [5] 이전 (← 페이지 1)

**저장 파일 예**: `.moai/harness-contexts/{harness-id}.md`
예시:
  - copywriting.md
  - email-crafter.md
  - ad-campaign.md
  - financial-model.md
  - sop-writer.md
  - compliance.md
  - meeting-strategist.md
  - market-research.md

---

## Phase 4: 심층 맥락 수집 (하네스별)

각 선택된 하네스에 대해 최대 **4질문**으로 컨텍스트 수집:

### 예시 1: copywriting
```
Q1. 주요 콘텐츠 형식? (4옵션)
Q2. 타겟 독자? (3옵션)
Q3. 톤&스타일? (4옵션)
Q4. 발행 채널? (3옵션)
```

### 예시 2: financial-model
```
Q1. 분석 범위? (4옵션)
Q2. 주요 메트릭? (3옵션)
Q3. 기준 시간? (3옵션)
Q4. 보고 형식? (3옵션)
```

**저장 위치**: `.moai/harness-contexts/{harness-id}.md`

---

## Phase 5: 로캘 현지화 (웹검색 기반)

### 5-0. 기존 로케일 데이터 확인 (재사용 판단)
```
IF /mnt/.auto-memory/locale-context.md 존재:
  → Phase 5 전체 SKIP
  → 기존 locale-context.md 재사용
  → "기존 로케일 데이터(XX국가)를 재사용합니다." 메시지 출력
  → Phase 6으로 진행

IF 존재하지 않음:
  → Phase 5-1부터 정상 진행
```

### 5-1. 로케일 결정
- **언어**: Phase 1-A Q1 결과
- **근무 국가**: Phase 1-A Q2 결과
- **시간대**: 국가 기본값 또는 사용자 입력
- **통화**: 국가 기본값

### 5-2. 웹검색 기반 로케일 데이터 수집

근무 국가가 한국(KR)인 경우:
- `references/locale/kr/index.md` 내장 데이터를 로딩한다.

근무 국가가 한국 외인 경우:
- 웹검색으로 해당 국가의 로케일 데이터를 **실시간** 수집한다.
- `references/locale/cultural-adaptation-guide.md`를 참조하여 수집 항목을 결정한다.

**수집 항목** (웹검색 쿼리 예시):
```
1. "{국가명} tax law basics {연도}" → 세법 기본사항
2. "{국가명} labor law employment rules" → 노동법 핵심
3. "{국가명} data protection privacy law" → 데이터보호법
4. "{국가명} business culture etiquette" → 비즈니스 관행
5. "{국가명} date format currency number format" → 형식 표준
```

수집된 데이터를 `/mnt/.auto-memory/locale-context.md`에 저장한다.
이후 하네스 실행 시 이 파일을 참조하여 현지화된 산출물을 생성한다.
**한 번 생성되면 세션 간 영구 재사용** — 다음 `/moai init`에서 재설문 없이 기존 데이터 활용.

### 5-3. Graceful Degradation
- 웹검색 실패 시: 사용자에게 직접 입력 요청
- 부분 실패 시: 수집된 항목만 저장, 누락 항목은 추후 보완

---

## Phase 6: 파일 생성

### 6-1. 글로벌 프로필 업데이트
**파일**: `/mnt/.auto-memory/moai-profile.md`
```yaml
User Profile:
  name: {user_input}
  locale: {lang_country}
  language: {language}
  country: {country}
  timezone: {timezone}

Role & Industry:
  role: {role}
  industry: {industry}
  experience_level: {inferred}

Company Profile:
  company_name: {optional}
  business_type: {business_type}
  company_size: {size}
  ...

Preferences:
  response_language: {language}
  file_language: {language}
  ...

Context Depth:
  collected_rounds: 1
  sufficiency_score: 85%
  last_updated: {timestamp}
```

### 6-2. CLAUDE.md 생성
**파일**: `.claude/CLAUDE.md`
(claudemd-generator.md 참조)

### 6-3. rules/ 파일 생성
**파일들**:
- `.claude/rules/00-moai-core.md`
- `.claude/rules/01-{harness-id}.md`
- `.claude/rules/02-locale-{country}.md` (필요시)

### 6-4. .moai/ 프로젝트 구조 생성
```
.moai/
├── harness-contexts/
│   ├── copywriting.md
│   ├── email-crafter.md
│   └── ...
├── evolution/
│   └── self-refine-log.md
├── category-selection.md
└── harness-selection.json
```

---

## --harness 옵션 (빠른 경로)

```bash
/moai init --harness email-crafter
```

이 경우:
- Phase 2-3 자동 스킵
- Phase 1 필수 질문만 수행
- Phase 4 심층 컨텍스트 수집

---

## 에러 처리

| 상황 | 조치 |
|-----|------|
| 프로필 이미 존재 | Phase 0-B로 분기 |
| 질문 응답 불완전 | 현재 질문 재시도 |
| 하네스 미설치 | `/moai init` 안내 |
| 네트워크 오류 (웹검색) | 오프라인 모드로 진행 |

---

## 완료 메시지

```
✓ MoAI 초기화 완료! ({user_name}님)

설정:
  - 언어: {language}
  - 국가: {country}
  - 역할: {role}
  - 카테고리: {categories}
  - 선택 하네스: {harness_list}

다음 단계:
  /moai help          (명령어 확인)
  /moai status        (설치 상태)
  /moai {harness-id}  (하네스 실행)
```

