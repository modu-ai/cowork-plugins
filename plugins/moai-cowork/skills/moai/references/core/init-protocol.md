# init-protocol.md — /moai init 전체 플로우

## 개요
사용자의 MoAI 초기화 프로세스를 정의합니다. 글로벌 프로필 구축, 언어/로케일 설정, 카테고리 선택,
하네스 선택까지 6단계 Phase로 구성됩니다.

**핵심 원칙:**
- **심화 인터뷰**: 모든 설문 단계에서 객관식 → 열린 후속 질문 → 확인의 3단계 패턴 사용
- **문서 우선 수집**: 사업자등록증 등 공식 문서가 있으면 업로드 우선, 없으면 인터뷰 진행
- **풀 하네스 복사**: 하네스 설치 시 `references/harness-100/{lang}/` 원본을 그대로 복사 후 사용자 맥락으로 커스터마이징
- **언어 일관성**: 모든 생성 파일은 Phase 1-A Q1에서 선택한 언어로 작성
- **하네스 ID 정합성**: 반드시 `references/harness-100/{lang}/` 에 실제 존재하는 파일명만 사용
- **하네스 명칭 사용자 언어**: 사용자에게 표시하는 모든 하네스 명칭은 사용자 언어로 표기 (내부 ID는 영어 유지)

---

## 하네스 표시명 규칙 (모든 Phase 공통)

### 원칙
사용자에게 노출되는 모든 하네스 명칭은 **사용자 언어(target_language)**로 표기한다.
내부적으로 파일명/ID는 영어 하이픈 형식(예: `course-builder`)을 유지하되,
UI/메시지/생성 문서에서는 반드시 사용자 언어 이름을 사용한다.

### 표시 형식
```
{사용자 언어 하네스명} — {레퍼런스 개요에서 추출한 기능 요약}

예시 (한국어):
  강의 빌더 — 커리큘럼, 퀴즈, 실습 과제 설계
  시장 조사 — 시장 규모, 경쟁사 분석, 트렌드 리서치
  카피라이팅 — 브랜드 카피, 세일즈 레터, 콘텐츠 작성
  기술 문서 작성 — API 가이드, 사용자 매뉴얼, 운영 문서

잘못된 예시 (사용 금지):
  ✗ course-builder (강의 빌더)     ← 영어 ID가 먼저 오면 안 됨
  ✗ copywriting                    ← 영어 ID만 표시하면 안 됨
  ✗ [3] ad-campaign (광고 캠페인)  ← 영어 ID 우선 표기 금지
```

### 이름 추출 방법
```python
harness_ref = Read(f"references/harness-100/{target_lang}/{harness_id}.md")
display_name = extract_title(harness_ref)       # 예: "시장 조사 (market-research)"의 첫 부분
overview = extract_section(harness_ref, "개요")  # 1줄 기능 요약
display_label = f"{display_name} — {overview}"
```

### 적용 범위
- Phase 3 하네스 선택 UI
- Phase 4 맥락 수집 메시지 ("시장 조사 하네스에 대해 질문드리겠습니다")
- .claude/CLAUDE.md 내 하네스 목록
- .claude/rules/01-{harness-id}.md 내 설명
- .moai/harness-contexts/ 파일 제목
- .moai/harness-selection.json (display_name 필드 추가)
- 사용자와의 모든 대화 메시지

---

## 심화 인터뷰 패턴 (모든 Phase 공통)

### 패턴 정의
AskUserQuestion 객관식 선택 후 텍스트 대화로 심화하는 3단계 패턴:

```
[Step 1] AskUserQuestion — 객관식으로 대략적 방향 파악
  ↓
[Step 2] 심화 인터뷰 — 열린 질문으로 맥락 심화
  예: "그렇게 선택하신 이유나 배경이 있으신가요?"
  예: "구체적으로 어떤 상황에서 주로 필요하신가요?"
  예: "현재 가장 큰 도전이나 과제는 무엇인가요?"
  ↓
[Step 3] 확인 요약 — "정리하면 ~이라는 뜻이 맞으시죠?"
```

### Phase별 적용 깊이
| Phase | Step 1 (객관식) | Step 2 (심화 인터뷰) | Step 3 (확인) | 이유 |
|-------|----------------|---------------------|-------------|------|
| 1-A (기본 프로필) | O | X | X | 빠른 진행 |
| 1-B (기업 정보) | 문서업로드 우선 | O (최대 2개) | O | 기업 맥락 중요 |
| 2 (카테고리) | O | O (최대 2개) | X | 업무 맥락 심화 |
| 3 (하네스 선택) | O | X | X | 다중 선택 |
| 4 (심층 맥락) | O | O (최대 2개) | O | 가장 상세 수집 |

### 사용자 피로 방지 규칙
- 후속 질문은 Phase당 최대 2개
- 사용자가 "빨리 진행해", "넘어가자", 간단히 답하면 즉시 다음 Phase로 전환
- 전체 init 소요 시간 목표: 5-10분 이내
- 질문은 친근하되 전문적인 톤으로 (사용자 로케일에 맞춤)

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

> **적용 깊이**: Step 1만 (빠른 진행)

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
**중요**: 이후 모든 생성 파일(CLAUDE.md, rules/, harness-contexts/, config.json 등)은
여기서 선택한 언어로 작성된다. 하네스 레퍼런스 복사 시 해당 언어 폴더에서 가져온다.

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

## Phase 1-B: 회사/사업자 프로필 (문서 우선 수집)

> **적용 깊이**: 문서업로드 우선 → Step 1 + Step 2 + Step 3

### Step 0: 사업자등록증 업로드 (우선 시도)

```
AskUserQuestion [header: "기업정보"]
질문: "회사/사업자 정보를 어떻게 입력하시겠습니까?"

선택지:
  [1] 사업자등록증 업로드 (자동 추출)
  [2] 직접 입력 (인터뷰)
  [3] 건너뛰기 (나중에)
```

#### [1] 사업자등록증 업로드 경로

```
IF 사용자가 사업자등록증 파일 업로드:
  1. 업로드된 파일을 Read 도구로 읽기 (이미지/PDF)
  2. OCR/시각 분석으로 다음 정보 자동 추출:
     - 상호명 (회사명)
     - 대표자명
     - 사업자등록번호 (XXX-XX-XXXXX)
     - 사업장 소재지
     - 업태 / 종목
     - 개업일
     - 법인등록번호 (법인인 경우)
     - 사업의 종류 (업태/종목)
  3. 추출 결과를 사용자에게 확인:
     "추출된 정보를 확인해주세요:"
     - 회사명: {extracted}
     - 사업자번호: {extracted}
     - 업태: {extracted}
     - ...
     "맞으시면 '확인', 수정할 부분이 있으면 알려주세요."
  4. [Step 2] 심화 인터뷰 (추가 정보 수집):
     - "회사의 주력 제품/서비스는 무엇인가요?"
     - "현재 팀 규모와 주요 과제는 무엇인가요?"
  5. [Step 3] 확인 요약:
     "정리하면, {회사명}은(는) {업태} 분야의 {사업형태}이시고,
      주력은 {주력분야}이며, {팀규모} 규모의 조직이시군요. 맞으시죠?"
  6. moai-profile.md의 Company Profile 섹션에 저장
```

#### [2] 직접 입력 (인터뷰) 경로

사업자등록증이 없는 경우, 심화 인터뷰로 진행:

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

**[Step 2] 심화 인터뷰** (Q1~Q3 완료 후):
- "사업의 주력 분야나 핵심 제품/서비스는 무엇인가요?"
- "현재 가장 큰 비즈니스 과제나 목표는 무엇인가요?"

**[Step 3] 확인 요약**:
"정리하면, {사업형태} 형태의 {업종} 기업이시고,
주력 분야는 {사용자 답변}이며, 팀 규모는 {규모}이시군요. 맞으시죠?"

#### [3] 건너뛰기

```
→ Company Profile은 비워둔 채 진행
→ 이후 `/moai profile` 명령으로 보완 가능
→ 안내 메시지: "기업 정보 없이 진행합니다. 필요시 `/moai profile`로 추가하세요."
```

**세부정보 수집** (문서 업로드/인터뷰 공통, 심화 인터뷰 답변에서 추출):
- 회사명, 등록번호, 웹사이트, 회계년도 말
- 팀 규모, 핵심 KPI, 주요 과제

**저장 위치**: `/mnt/.auto-memory/moai-profile.md` (Company Profile 섹션)

---

## Phase 2: 카테고리 선택 (2단계)

> **적용 깊이**: Step 1 + Step 2

### Phase 2-A: 대분류 선택 [header: "카테고리"]
```
질문: "주로 어떤 업무를 도움받고 싶으신가요?"

선택지:
  [1] 콘텐츠&마케팅 (블로그, 이메일, SNS, 광고)
  [2] 비즈니스&전략 (계획, 자동화, 분석)
  [3] 전문분야&규제 (법규, 계약, 컴플라이언스)
  [4] 라이프&커뮤니케이션 (회의, 일정, 협업)
```

**[Step 2] 심화 인터뷰**:
"구체적으로 어떤 업무에서 가장 큰 도움이 필요하신가요?
예를 들어, 일상적으로 반복되는 업무나 특히 시간이 많이 드는 작업이 있으시면 알려주세요."

**중요**: 사용자의 텍스트 응답을 분석하여 Phase 3의 하네스 추천 목록에 반영한다.

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

> **적용 깊이**: Step 1만 (다중 선택)

### 3-0. 하네스 ID 매핑 규칙 (중요!)

선택된 하네스의 ID는 반드시 `references/harness-100/{lang}/` 디렉토리에 실제 존재하는 파일명(.md 제외)과 일치해야 한다.
**절대 임의의 ID를 생성하지 않는다.**

```
검증 절차:
  1. 하네스 추천 목록 생성 시 → Glob("references/harness-100/{lang}/*.md")로 실제 파일 목록 확인
  2. 사용자 선택 후 → Read("references/harness-100/{lang}/{harness-id}.md") 로 존재 확인
  3. 파일 없으면 → 에러: "해당 하네스 파일을 찾을 수 없습니다. 유사한 하네스를 제안합니다."

올바른 ID 예시 (실제 파일명):
  - market-research, technical-writer, course-builder, copywriting
  - ai-strategy, proposal-writer, email-crafter, ad-campaign
  - financial-model, sop-writer, compliance, meeting-strategist

잘못된 ID (파일 없음 → 사용 금지!):
  - documentation (→ technical-writer 사용)
  - course-development (→ course-builder 사용)
  - business-writing (→ proposal-writer 또는 copywriting 사용)
  - ai-integration (→ ai-strategy 사용)
  - content_generator, email_harness (→ 언더스코어 사용 금지, 하이픈 사용)
```

### 3-1. 설치할 하네스 선택

Phase 2의 카테고리 + 심화 인터뷰 답변을 분석하여 추천 하네스 목록을 구성한다.
카탈로그(`references/catalog/`)를 참조하여 사용자에게 적합한 하네스를 제안한다.

```
질문: "도움을 받을 하네스를 선택하세요 (다중 선택 가능)"

페이지 1/2:
  [1] 카피라이팅 — 브랜드 카피, 세일즈 레터, 콘텐츠 작성
  [2] 이메일 작성 — 비즈니스 이메일, 뉴스레터, 자동화 시퀀스
  [3] 광고 캠페인 — 광고 기획, 크리에이티브, 미디어 전략
  [4] 재무 모델링 — 사업계획 재무, 투자 분석, 예산 관리
  [5] 다음 (→ 페이지 2)

페이지 2/2:
  [1] SOP 작성 — 표준 운영 절차서, 업무 매뉴얼
  [2] 컴플라이언스 — 법규 준수, 규제 대응, 내부 감사
  [3] 회의 전략 — 안건 설계, 퍼실리테이션, 회의록
  [4] 시장 조사 — 시장 규모, 경쟁사 분석, 트렌드 리서치
  [5] 이전 (← 페이지 1)
```

**위 예시는 참고용**. 실제 선택지는 Phase 2 답변 + 카탈로그 기반으로 동적 구성.
**반드시** `references/harness-100/{lang}/` 에 존재하는 파일명만 선택지로 제시한다.
**표시명은 사용자 언어**로: 하네스 레퍼런스의 제목 + 개요에서 추출한 기능 요약 형식 사용.

**선택 저장**: `.moai/harness-selection.json`
```json
{
  "harnesses": [
    {
      "id": "market-research",
      "display_name": "시장 조사",
      "overview": "시장 규모, 경쟁사 분석, 트렌드 리서치",
      "category": 2
    }
  ]
}
```

---

## Phase 4: 심층 맥락 수집 (하네스별)

> **적용 깊이**: Step 1 + Step 2 + Step 3 (가장 상세)

### 4-0. 하네스 레퍼런스 로딩 (필수 선행)

각 선택된 하네스에 대해 먼저 원본 레퍼런스를 로딩한다:
```
target_lang = Phase 1-A Q1 결과 (ko/en/ja/es 등)
harness_ref = Read("references/harness-100/{target_lang}/{harness-id}.md")
```

레퍼런스 파일의 **"맥락 수집 질문 (AskUserQuestion)"** 섹션을 사용하여 질문을 구성한다.
**임의로 질문을 생성하지 말고, 레퍼런스에 정의된 질문을 그대로 사용한다.**

### 4-1. 심화 인터뷰 기반 맥락 수집 (하네스당)

```
FOR each selected_harness:

  [Step 1] AskUserQuestion (최대 4질문)
    — 하네스 레퍼런스의 "맥락 수집 질문" 섹션에서 필수 질문(Q1~Q4) 사용
    — 질문 텍스트, 옵션 예시 모두 레퍼런스 원본 그대로

  [Step 2] 심화 인터뷰 질문 (텍스트, 최대 2개)
    — "이 분야에서 특히 중요하게 생각하시는 부분은 무엇인가요?"
    — "현재 가장 큰 도전이나 과제는 무엇인가요?"
    — 또는 레퍼런스의 "선택적 심화 질문" 에서 택 2

  [Step 3] 확인 요약
    — "정리하면, {사용자 언어 하네스명} 분야에서 {user_name}님은 {요약}.
       이 방향으로 진행해도 될까요?"
    — 하네스명은 반드시 사용자 언어로 표기 (예: "시장 조사", "강의 빌더")

  저장 → .moai/harness-contexts/{harness-id}.md
```

### 4-2. harness-contexts 파일 생성 규칙 (핵심!)

**기존 문제**: 15줄짜리 축약본만 생성됨
**개선**: 풀 하네스 레퍼런스를 복사 + 사용자 맥락 섹션 추가

```markdown
# {사용자 언어 하네스명} ({harness-id}) — 하네스 컨텍스트

## 사용자 맥락 (Phase 4 수집 결과)
- **하네스 ID**: {harness-id}
- **표시명**: {사용자 언어 하네스명}
- **카테고리**: {category_number}
- **설치일**: {YYYY-MM-DD}
- **충분성 등급**: {A/B/C}

### 수집된 답변
- **Q1**: {질문} → {답변}
- **Q2**: {질문} → {답변}
- **Q3**: {질문} → {답변}
- **Q4**: {질문} → {답변}

### 심화 맥락 (심화 인터뷰 결과)
- {열린 질문 1}: {사용자 답변 요약}
- {열린 질문 2}: {사용자 답변 요약}

### 활용 시나리오
- {사용자 답변에서 도출된 구체적 시나리오 1}
- {사용자 답변에서 도출된 구체적 시나리오 2}
- {사용자 답변에서 도출된 구체적 시나리오 3}

---

## 하네스 레퍼런스 (원본)

{여기에 references/harness-100/{lang}/{harness-id}.md 의 전체 내용을 그대로 복사}
{축약 금지! 페르소나, 전문가 역할, 워크플로우, Phase 1~4, 산출물 형식,}
{맥락 수집 질문, 관련 하네스, Cowork 실행 가이드 모두 포함}
```

**파일 크기 기준**:
- 각 파일은 최소 80줄 이상 (사용자 맥락 ~25줄 + 풀 레퍼런스 ~55줄 이상)
- 15줄짜리 축약본은 품질 부적합 → 재생성 필요

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

### 6-0. 언어 규칙 (필수!)

```
target_language = Phase 1-A Q1에서 선택한 언어

모든 생성 파일은 target_language로 작성:
  - .claude/CLAUDE.md → target_language
  - .claude/rules/*.md → target_language
  - .moai/config.json → 키는 영어, 값/설명은 target_language
  - .moai/harness-contexts/*.md → target_language
  - .moai/category-selection.md → target_language
  - .moai/evolution/self-refine-log.md → target_language

하네스 레퍼런스 복사 시 언어 폴더 선택:
  - target_language == "ko" → references/harness-100/ko/
  - target_language == "en" → references/harness-100/en/
  - 다른 언어 → 가장 가까운 버전 + 필요시 번역
```

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
  company_name: {from_document_or_input}
  business_type: {business_type}
  registration_number: {from_document_or_input}
  company_size: {size}
  industry_code: {from_document_or_input}
  headquarters: {from_document_or_input}
  core_product: {from_socratic_answer}
  key_challenges: {from_socratic_answer}
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

**필수 규칙**:
- claudemd-generator.md의 전체 템플릿을 따르되, 사용자 정보로 치환
- 축약하지 않고 모든 섹션을 포함: 헤더, 나는 누구인가, 행동 원칙 4개,
  참조 경로, 세션 부팅 프로토콜, 주요 명령어, 버전 정보
- **target_language**로 작성

### 6-3. rules/ 파일 생성
**파일들**:
- `.claude/rules/00-moai-core.md`
- `.claude/rules/01-{harness-id}.md` (각 하네스별)
- `.claude/rules/02-locale-{country}.md` (필요시)

**필수 규칙** (rules-generator.md 참조):
- **00-moai-core.md**: 프로필 우선, 언어&로케일, 톤&스타일, 하네스 라우팅,
  컨텍스트 관리, 자기학습, 투명성, 보안, 품질보증, 성능 → **10개 섹션 모두 포함**
- **01-{harness-id}.md**: 하네스 레퍼런스의 페르소나, 워크플로우 Phase,
  핵심 스킬, 산출물 형식, 품질 체크리스트를 **모두 반영**한 상세 규칙.
  활성화 조건, 세부 행동 규칙, 산출물 포맷, 검증 체크리스트 포함.
  **최소 30줄 이상**. 5줄짜리 축약본 절대 금지!
- **02-locale-{country}.md**: 형식 규칙(날짜/시간/통화/주소),
  비즈니스 톤, 법률/규제 참조를 **상세** 포함.
  localization-protocol.md + locale 데이터를 반영.
- 모든 파일은 **target_language**로 작성

### 6-4. .moai/ 프로젝트 구조 생성
```
.moai/
├── config.json              # 프로젝트 설정 (사용자명, 로케일, 하네스 목록)
├── category-selection.md    # 카테고리 선택 결과 + 심화 인터뷰 답변 기록
├── harness-selection.json   # 설치 하네스 목록 (ID, 카테고리, 설치일)
├── harness-contexts/        # 하네스 컨텍스트 (사용자 맥락 + 풀 레퍼런스 복사!)
│   ├── {harness-id-1}.md    # 최소 80줄 이상
│   ├── {harness-id-2}.md
│   └── ...
└── evolution/               # 자기학습 데이터
    └── self-refine-log.md
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
- **하네스 ID 검증**: `references/harness-100/{lang}/{id}.md` 존재 확인 필수

---

## 에러 처리

| 상황 | 조치 |
|-----|------|
| 프로필 이미 존재 | Phase 0-B로 분기 |
| 질문 응답 불완전 | 현재 질문 재시도 |
| 하네스 미설치 | `/moai init` 안내 |
| 하네스 ID 불일치 | Glob으로 harness-100/ 검색 후 가장 유사한 ID 제안 |
| 사업자등록증 파싱 실패 | "자동 추출이 어렵습니다. 직접 입력으로 전환합니다." |
| 네트워크 오류 (웹검색) | 오프라인 모드로 진행 |

---

## 완료 메시지

```
✓ MoAI 초기화 완료! ({user_name}님)

설정:
  - 언어: {language}
  - 국가: {country}
  - 역할: {role}
  - 기업: {company_name} ({business_type})
  - 카테고리: {categories}
  - 선택 하네스: {harness_list}

파일 생성됨:
  - .claude/CLAUDE.md (상세 페르소나)
  - .claude/rules/ ({n}개 규칙 파일, 각 30줄+)
  - .moai/ (프로젝트 구조)
  - harness-contexts/ ({n}개, 풀 레퍼런스 포함, 각 80줄+)

다음 단계:
  /moai help          (명령어 확인)
  /moai status        (설치 상태)
  /moai {harness-id}  (하네스 실행)
```
