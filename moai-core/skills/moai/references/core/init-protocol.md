# init-protocol.md — /moai init 전체 플로우

## 개요
사용자의 MoAI 초기화 프로세스를 정의한다.
setup-cowork 패턴(역할→플러그인→커넥터)과 claude-code-setup 패턴(자동 감지+추천)을 결합한 5단계 빠른 설정.

**v2.0 핵심 변경 (v1.0 대비):**
- Phase 1: 프로필 7질문 → 1질문으로 간소화 (역할/분야만)
- Phase 2-3 (카테고리+하네스): 제거 → 플러그인 자동 감지로 대체
- Phase 4 (맥락 수집): init에서 제거 → 하네스 첫 실행 시 Lazy Collection
- Phase 3: 커넥터 + API 키 입력 통합
- Phase 4: 첫 실행 안내 추가
- 총 소요 시간: ~10분+ → **~3분**

---

## 프로필 저장 전략 (2계층)

MoAI 프로필은 **글로벌 지침**과 **프로젝트 메모리** 2계층으로 관리된다.

```
계층 1: 글로벌 지침 (설정 > 협업 > 글로벌 지침)
  └── 사용자 기본 정보 (이름, 회사, 역할, 분야)
      → 모든 Cowork 프로젝트에서 자동 적용
      → 사용자가 직접 복사하여 설정에 추가

계층 2: 프로젝트 메모리 (프로젝트별)
  └── 프로젝트별 설정 (선택된 플러그인, 커넥터, API 키)
      → .moai/config.json에 저장
      → 프로젝트 내 모든 세션에서 유지
```

**글로벌 지침 형식** (사용자가 설정 > 협업에 복사):

```
[MoAI 프로필]
이름: {name}
회사: {company}
역할: {role}
분야: {category}
```

**API 키**: 프로젝트 메모리(memory/)에 moai-credentials.env로 저장.
새 프로젝트에서도 API 키는 재입력 필요 (프로젝트별 격리).

---

## Phase 0: 글로벌 프로필 감지

```
글로벌 지침에서 "[MoAI 프로필]" 블록 검색
├── [있음] → 프로필 정보 파싱하여 재사용
│   "기존 프로필이 감지되었습니다.
│    • 이름: {name}
│    • 회사: {company}
│    • 역할: {role}
│    이 정보로 진행합니다."
│   → Phase 2로 스킵
│
└── [없음] → Phase 1로
    프로젝트 메모리에서 moai-profile.md 추가 검색
    ├── [있음] → 재사용 확인 후 Phase 2로
    └── [없음] → Phase 1 (신규 수집)
```

**글로벌 지침 감지 방법:**
Claude는 Cowork 글로벌 지침을 세션 시작 시 자동으로 읽는다.
"[MoAI 프로필]" 패턴이 글로벌 지침에 포함되어 있으면 파싱하여 사용한다.

---

## Phase 1: 빠른 프로필

프로필이 없는 경우, 최소 정보만 수집한다. 나머지는 auto-memory로 점진 축적.

### 1-1. 역할/분야 선택

AskUserQuestion (1질문, 4옵션) ✅

```
"어떤 분야에서 일하시나요?"

○ 비즈니스/전략/창업 — 사업계획, 투자, 시장조사, 재무
○ 마케팅/콘텐츠/영업 — SNS, 블로그, 광고, 이메일, 카피
○ 관리/운영/전문직 — 법률, 세무, 인사, 문서, 결재
○ 제품/기술/연구 — PM, UX, 교육, 데이터, 커리어
+ Other (직접 입력)
```

### 1-2. 이름/회사 수집

AskUserQuestion (1질문, 자유입력) ✅

```
"이름(또는 닉네임)과 회사명을 알려주세요.
 예: '홍길동, 테크스타트업' 또는 '길동'만 입력해도 됩니다.
 사업자등록증을 첨부하시면 자동으로 정보를 추출합니다."
+ Other (자유 입력)
```

사업자등록증 첨부 시:
- 이미지에서 사업자번호, 회사명, 대표자명, 업종을 자동 추출
- 추출 결과를 AskUserQuestion으로 확인 후 프로필에 반영

→ 프로젝트 메모리에 moai-profile.md 저장
→ 추가 정보(산업, 경력, 호칭 등)는 하네스 사용 중 메모리에 자연스럽게 축적

### 1-3. 글로벌 지침 텍스트 생성

프로필 수집 완료 후, 사용자에게 **글로벌 지침용 텍스트**를 생성하여 제공한다.
사용자가 이 텍스트를 설정 > 협업 > 글로벌 지침에 복사하면
모든 프로젝트에서 프로필이 자동 적용된다.

```
"프로필이 저장되었습니다.

 다른 프로젝트에서도 이 프로필을 자동으로 사용하려면,
 아래 텍스트를 복사하여 설정 > 협업 > 글로벌 지침에 추가하세요:

 ─────────────────────
 [MoAI 글로벌 지침]

 모든 대화는 한국어로 해야 한다.

 사용자가 충분한 맥락을 제공하지 않은 지시이거나 모호한 요청이면,
 바로 실행하지 말고 소크라테스식 인터뷰로 정보를 수집한다.
 목표, 범위, 독자, 형식, 제약 등을 확인한 뒤 진행한다.

 [MoAI 프로필]
 이름: {name}
 회사: {company}
 역할: {role}
 분야: {category}
 ─────────────────────

 설정 방법: 설정 > 협업 > 글로벌 지침 > 위 텍스트 붙여넣기 > 저장

 이미 글로벌 지침에 추가하셨나요?"

AskUserQuestion (2옵션):
○ 추가 완료 — 다음 단계로 진행 (권장)
○ 나중에 추가 — 이 프로젝트에서만 사용
+ Other
```

---

## Phase 2: 플러그인 감지 + 선택

### 2-1. 설치된 플러그인 자동 감지

```
Cowork에 설치된 moai-* 플러그인을 자동 스캔:

installed_plugins = scan_installed_moai_plugins()

예: [moai-core, moai-business, moai-office, moai-legal]
```

### 2-2. 주 사용 플러그인 선택

Phase 1 답변 기반으로 관련성 높은 순서로 표시.

AskUserQuestion (1질문, 4옵션, multiSelect) ✅

```
[예: "비즈니스/전략/창업" 선택 + 4개 플러그인 설치된 경우]
"주로 사용할 플러그인을 선택하세요 (복수 선택 가능)"

☑ moai-business — 사업계획서, 시장조사, 투자제안서, 재무모델
☐ moai-office — PPT, 한글(HWPX), Word, Excel 문서 생성
☐ moai-legal — 계약서 검토, 컴플라이언스, NDA
+ Other ("더 보기")
```

```
[예: "마케팅/콘텐츠/영업" 선택 시]
"주로 사용할 플러그인을 선택하세요 (복수 선택 가능)"

☑ moai-content — 카드뉴스, 블로그, 뉴스레터, 카피라이팅
☐ moai-marketing — SEO, SNS, 캠페인, 이메일 시퀀스
☐ moai-office — PPT, Word, Excel 문서 생성
+ Other ("더 보기")
```

표시 규칙:
- moai-core는 오케스트레이터이므로 **선택 목록에서 제외**
- 설치되지 않은 플러그인은 표시하지 않는다
- "더 보기" 선택 시 나머지 플러그인 페이지네이션

### 2-3. 미설치 플러그인 안내

```
IF Phase 1 답변에 매칭되지만 미설치된 플러그인이 있으면:

"추가로 이런 플러그인을 설치하면 좋습니다:
 - moai-finance — 세무, 부가세, 홈택스, K-IFRS
 - moai-hr — 근로계약서, 4대보험, 채용
 
 Settings > Plugins에서 설치할 수 있습니다."
```

---

## Phase 3: 커넥터 + API 키 설정

### 3-1. 공식 커넥터 선택

선택된 플러그인에 맞는 Cowork 공식 커넥터를 추천한다.

**커넥터 매핑 테이블:**

| 플러그인 | 권장 커넥터 |
|---------|-----------|
| moai-content | WordPress, Canva |
| moai-marketing | Gmail, HubSpot, Canva |
| moai-product | Notion, Figma, Asana/Linear/Jira |
| moai-office | Google Drive, Gmail, Notion, Microsoft 365 |
| moai-support | Slack, HubSpot |
| moai-operations | Slack, Notion, Asana/Jira |
| moai-data | Airtable, Google Sheets, Google Drive, Notion |
| moai-research | Google Drive, Notion, Google Calendar |

AskUserQuestion (1질문, 최대 4옵션, multiSelect) ✅

```
[예: moai-office + moai-business 선택 시 — 중복 제거 후 상위 4개]
"연동할 도구를 선택하세요 (나중에 설정 가능)"

☐ Google Drive — 문서 저장/공유, Google Docs/Sheets 연동
☐ Notion — 보고서/회의록을 Notion 페이지로 발행
☐ Gmail — 문서 이메일 발송
☐ Microsoft 365 — Outlook, OneDrive, Teams
+ Other ("건너뛰기")
```

선택 시:
```
"선택한 커넥터를 연결하세요:
 1. Settings > Connectors 이동
 2. {커넥터명} 찾기 > Connect 클릭
 3. 계정 인증 (OAuth)
 
 한 번 연결하면 모든 세션에서 유지됩니다."
```

건너뛰기 시:
```
"커넥터 없이도 모든 기능이 독립 실행됩니다.
 나중에 Settings > Connectors에서 언제든 연결 가능합니다."
```

### 3-2. API 키 등록 (커스텀 MCP)

선택된 플러그인 중 API 키가 필요한 것이 있으면, API 키 등록을 안내한다.

**주의: 아래 목록에 있는 서비스만 안내한다. 네이버 API 등 목록에 없는 서비스는 안내하지 않는다.**

**API 키 필요 플러그인 (이 목록만 해당):**

| 플러그인 | 서비스 | 환경변수 | 용도 | 발급처 |
|---------|--------|---------|------|--------|
| moai-content | Nano Banana | NANO_BANANA_API_KEY | AI 이미지 생성 | ai.google.dev |
| moai-business | DART 전자공시 | DART_API_KEY | 기업 공시/재무제표 | opendart.fss.or.kr |
| moai-legal | 국가법령정보 | KOREAN_LAW_OC | 법령/판례 검색 | law.go.kr |
| moai-data | 공공데이터포털 | DATA_GO_KR_API_KEY | 공공데이터 조회 | data.go.kr |
| moai-data | KOSIS 통계 | KOSIS_API_KEY | 통계청 데이터 | kosis.kr/openapi |
| moai-research | KIPRIS Plus | KIPRIS_API_KEY | 특허 검색 | plus.kipris.or.kr |
| moai-research | KCI 논문 | KCI_API_KEY | 논문 검색 | data.go.kr (KCI) |

해당 서비스가 **2개 이상**이면 AskUserQuestion:

AskUserQuestion (1질문, 최대 4옵션, multiSelect) ✅

```
[설치된 플러그인에서 API 키 필요 서비스만 추출, 최대 4개씩 페이지네이션]

"API 키를 등록할 서비스를 선택하세요 (나중에 등록 가능)"

[페이지 1 — 4개]
☐ DART 전자공시 — 기업 공시, 재무제표 (opendart.fss.or.kr)
☐ 공공데이터포털 — 공공 API 조회 (data.go.kr)
☐ KOSIS 통계 — 통계청 데이터 (kosis.kr)
☐ KIPRIS Plus — 특허 검색 (plus.kipris.or.kr)
+ Other ("더 보기 / 건너뛰기")

[페이지 2 — 나머지]
☐ KCI 논문 — 학술 논문 검색 (data.go.kr 경유)
☐ 법령 정보 — 법령/판례 검색 (law.go.kr)
☐ Nano Banana — AI 이미지 생성 (ai.google.dev)
+ Other ("건너뛰기 — 나중에 /moai apikey로 등록")

※ 설치되지 않은 플러그인의 서비스는 표시하지 않는다
```

해당 서비스가 **1개만**이면 AskUserQuestion으로 직접 안내:

```
[예: moai-content만 설치 시]
AskUserQuestion (1질문, 2옵션):
"Nano Banana API 키를 등록하시겠습니까? (AI 이미지 생성)"
○ 키 입력 — ai.google.dev에서 발급
○ 건너뛰기 — 나중에 /moai apikey로 등록
+ Other
```

해당 서비스가 **0개**이면 Phase 3-2 전체를 건너뛴다.

선택 시, 각 서비스별 기존 키 확인 → 입력:

```
[각 서비스 공통 패턴]
IF 프로젝트 메모리의 moai-credentials.env에 해당 키 존재:
  AskUserQuestion (1질문, 2옵션):
  "{서비스명} API 키가 이미 등록되어 있습니다."
  ○ 기존 키 사용 (권장)
  ○ 새 키로 변경
  + Other

  "기존 키 사용" → 기존 값 유지, 다음 서비스로
  "새 키로 변경" → AskUserQuestion으로 키 입력

ELSE:
  AskUserQuestion으로 키 입력

[각 서비스별 AskUserQuestion]

AskUserQuestion (자유입력):
"{서비스명} API 키를 입력해 주세요. {발급처 URL}에서 발급 가능합니다."
+ Other ("건너뛰기")

서비스별 발급처:
- DART: opendart.fss.or.kr
- 법령: law.go.kr
- Nano Banana: ai.google.dev
- 공공데이터: data.go.kr
- KOSIS: kosis.kr/openapi
- KIPRIS: plus.kipris.or.kr
- KCI: data.go.kr/data/3049042
```

### 3-2.5. Nano Banana 모델 + 사이즈 설정

Nano Banana API 키가 등록된 경우 (기존 또는 신규), 사용할 모델과 이미지 비율을 설정한다.

**모델 선택** — AskUserQuestion (1질문, 3옵션, multiSelect) ✅

```
"사용할 이미지 생성 모델을 선택하세요 (복수 선택 가능)"

☑ Nano Banana Pro — 고품질, 텍스트 렌더링 우수 (권장)
☐ Nano Banana 2 — 빠른 생성, Pro 대비 절반 비용
☐ Nano Banana Ultra — 최고 품질, 프리미엄 결과물
+ Other ("건너뛰기 — Pro만 사용")
```

**이미지 비율 선택** — AskUserQuestion (1질문, 4옵션, multiSelect) ✅

```
"기본 이미지 비율을 선택하세요 (복수 선택 가능)"

☑ 3:4 — 인스타그램 피드 최적 (권장)
☐ 1:1 — 정사각형 (프로필, 썸네일)
☐ 9:16 — 세로형 (스토리, 릴스)
☐ 16:9 — 가로형 (블로그, 프레젠테이션)
+ Other ("건너뛰기 — 3:4만 사용")
```

**이미지 해상도 선택** — AskUserQuestion (1질문, 4옵션) ✅

```
"이미지 생성 해상도를 선택하세요"

○ 1K — 기본 해상도, 빠른 생성 (권장)
○ 2K — 고해상도, 인쇄용
○ 4K — 최고 해상도, 프리미엄 (비용 2배)
○ 512 — 저해상도, 미리보기/썸네일용
+ Other ("1K만 사용")
```

**저장**: config.json의 nano_banana 필드에 기록:
```json
"nano_banana": {
  "models": ["nano-banana-pro", "nano-banana-2"],
  "default_model": "nano-banana-pro",
  "ratios": ["3:4", "1:1", "9:16"],
  "default_ratio": "3:4",
  "resolutions": ["1K", "2K"],
  "default_resolution": "1K"
}
```

**실행 시 동작**:
- 모델/비율/해상도가 **1개만 설정**: 자동 사용 (질문 없음)
- **복수 설정** + 사용자 미지정: AskUserQuestion으로 선택 요청:
  - "어떤 모델로 생성할까요?" (Pro/2/Ultra)
  - "이미지 비율은?" (3:4/1:1/9:16/16:9)
  - "해상도는?" (512/1K/2K/4K)
- 사용자가 명시한 경우: 명시된 값 사용 (질문 없음)
- **API 키 필수**: 키 없으면 생성 진행 안 됨 → 키 입력 안내

### 3-3. API 키 저장 (글로벌 공유)

API 키는 **글로벌 경로**에 저장하여 모든 프로젝트에서 재입력 없이 공유한다.

```
저장 경로: Claude 메모리의 moai-credentials.env

입력받은 API 키를 글로벌 파일에 저장:

DART_API_KEY=abc123def456
KOREAN_LAW_OC=xyz789
NANO_BANANA_API_KEY=nb_key_...

저장 후 안내:
"API 키가 글로벌 설정에 저장되었습니다.
 다른 프로젝트에서도 자동으로 사용됩니다.
 키 변경: /moai apikey 로 언제든 수정 가능합니다."
```

**글로벌 공유 원리:**
- `Claude 메모리 (memory/)`는 모든 Cowork 세션/프로젝트에서 접근 가능
- 한 번 등록하면 재입력 불필요
- 프로필(`moai-profile.md`)과 같은 경로에 저장
- 프로젝트별 키가 필요하면 `.moai/credentials.env`로 오버라이드 가능

### 3-4. 스크립트에서 API 키 로드

```
스크립트에서 API 키가 필요한 경우, Claude가 메모리에서 키를 읽어 환경변수로 전달한다.

로드 우선순위:
1. 환경변수 (os.environ) — Claude가 메모리에서 읽어 주입
2. 프로젝트별 키 (.moai/credentials.env) — 프로젝트 오버라이드
3. Claude 메모리 — moai-credentials.env에서 직접 읽기 (Claude Read 도구)
```

**Claude의 역할:** 스크립트 실행 전에 메모리에서 API 키를 읽어 환경변수로 설정한 뒤 스크립트를 실행한다.
이렇게 하면 스크립트가 특정 경로에 의존하지 않고 표준 환경변수만으로 동작한다.
    return None
```

---

## Phase 4: CLAUDE.md 생성 + 첫 실행 안내

### 4-1. 생성 대상

```
<프로젝트>/
├── CLAUDE.md              ← 맞춤형 (≤ 200라인)
└── .moai/
    ├── config.json        ← 플러그인 설정, 커넥터 참조
    └── evolution/

글로벌 (모든 프로젝트 공유):
Claude 메모리 (memory/)
├── moai-profile.md        ← 사용자 프로필
└── moai-credentials.env   ← API 키 (Phase 3에서 생성)
```

### 4-2. CLAUDE.md 생성 규칙

1. **200라인 이내** — 맞춤형 지침 + 스킬 라우팅만 포함
2. **하네스 전체 복사 금지** — 핵심 역할/목적을 2~3줄로 요약
3. 실행 시 `references/harness/{id}.md`를 **런타임에 로드**
4. Phase 1의 사용자 프로필 정보를 페르소나에 반영
5. Phase 2에서 선택한 플러그인의 스킬 라우팅 테이블 포함
6. Phase 3에서 연결한 커넥터 정보 포함
7. 딥씽킹(--deepthink) 사용 조건 명시

→ 참조: `claudemd-generator.md`

### 4-3. config.json 예시

```json
{
  "moai_version": "1.0.0",
  "installed_at": "2026-04-10T15:30:00+09:00",
  "global_profile_ref": "memory/moai-profile.md",
  "global_credentials_ref": "memory/moai-credentials.env",
  "selected_plugins": ["moai-business", "moai-office", "moai-legal"],
  "connectors": {
    "official": ["Google Drive", "Notion"],
    "custom_mcp": {
      "dart": { "env_key": "DART_API_KEY", "configured": true },
      "korean-law": { "env_key": "KOREAN_LAW_OC", "configured": true },
      "nano-banana": { "env_key": "NANO_BANANA_API_KEY", "configured": false }
    }
  },
  "nano_banana": {
    "models": ["nano-banana-pro", "nano-banana-2"],
    "default_model": "nano-banana-pro",
    "ratios": ["3:4", "1:1"],
    "default_ratio": "3:4",
    "resolutions": ["1K", "2K"],
    "default_resolution": "1K"
  },
  "evolution": {
    "cycle_count": 0,
    "last_evolved": null
  }
}
```

### 4-4. 첫 실행 안내

CLAUDE.md 생성 완료 후, **Phase 2에서 선택된 플러그인 기반으로 예시를 동적 생성**:

```
"설정이 완료되었습니다! 바로 시작해 보세요:

 {selected_plugins 기반 예시 3개 동적 생성}

 전체 기능:
 - '/moai catalog' → 설치된 플러그인 + 하네스 전체 목록
 - '/moai status' → 현재 설정 상태 확인

 작업을 요청하면 필요한 맥락을 그때 수집합니다.
 자연스럽게 대화하시면 됩니다."
```

예시 생성 규칙:
- 선택된 플러그인별 대표 작업 1개씩, 총 3개 이내
- **형식**: `"요청 문장" → Skill(스킬명) 자동실행`
- 사용자 요청 → 어떤 스킬이 자동 트리거되는지 명확히 표시

예시 (moai-content + moai-education + moai-office 선택 시):

```
첫 작업 예시

1. 커리큘럼 설계
  당신: "초등학교 5학년 대상 AI 입문 강의 커리큘럼 12주 과정으로 설계해줘"
  → Skill(curriculum-designer) 자동실행
  → 학습 목표, 주차별 주제, 평가 기준, 필요 자료 생성

2. 강의 슬라이드 제작
  당신: "위의 커리큘럼 1주차 강의 슬라이드 PPT로 만들어줘"
  → Skill(pptx-designer) 자동실행
  → 제목, 학습 목표, 핵심 개념, 실습 활동 포함 슬라이드 생성

3. 블로그 포스팅
  당신: "AI 강의 설계 팁 블로그 글 써줘"
  → Skill(blog) 자동실행
  → SEO 최적화된 블로그 포스팅 자동 작성
```

---

## --harness 옵션 (바로 설치)

```
/moai init --harness youtube-production
```

Phase 0 (프로필 감지) → Phase 2-3 스킵 → Phase 4 (CLAUDE.md 생성)

---

## /moai apikey — API 키 관리 커맨드

```
/moai apikey
```

기존 등록된 API 키를 조회/변경/추가한다.

```
AskUserQuestion (1질문, 4옵션):
"어떤 작업을 하시겠습니까?"

○ 등록된 키 조회 — 현재 설정된 API 키 목록
○ 키 추가/변경 — 새 API 키 입력 또는 기존 변경
○ 키 삭제 — 등록된 API 키 제거
+ Other
```

---

## 맥락 수집 전략: Lazy Collection

init에서 맥락을 수집하지 않는다. 하네스 첫 실행 시 context-collector.md가 자동 작동:

```
사용자: "사업계획서 써줘"
    ↓
router.md → moai-business 매칭
    ↓
execution-protocol.md: 컨텍스트 로드 시도
    ↓
.moai/harness-contexts/ 없음 → context-collector.md 실행
    ↓
"사업계획서 작성을 위해 몇 가지 여쭤볼게요..."
(해당 하네스에 필요한 맥락만 수집)
    ↓
.moai/harness-contexts/{harness-id}.md에 저장 (다음 실행 시 재사용)
```

장점:
- 사용하지 않을 하네스의 맥락은 수집하지 않음
- 실제 작업 맥락에서 더 정확한 질문 가능
- init 시간 대폭 단축 (~10분 → ~3분)
- 맥락 캐시 30일 유효 (context-collector.md 참조)

---

## AskUserQuestion 제약 준수 요약

| Phase | 질문 수 | 옵션 수 | 제약 준수 |
|-------|---------|---------|----------|
| Phase 0 | 1 | 3 | ✅ |
| Phase 1 | 1 | 4 | ✅ |
| Phase 2 | 1 | 3~4 (multiSelect) | ✅ |
| Phase 3-1 커넥터 | 1 | 최대 4 (multiSelect) | ✅ |
| Phase 3-2 API 키 | 1 | 최대 4 (multiSelect) | ✅ |
| Phase 3-2 기존 키 | 조건부 | 2 | ✅ |
| Phase 3-2.5 모델 | 조건부 | 3 (multiSelect) | ✅ |
| Phase 3-2.5 비율 | 조건부 | 4 (multiSelect) | ✅ |
| Phase 3-2.5 해상도 | 조건부 | 4 | ✅ |
| 키 입력 | 텍스트 | N/A | ✅ (대화형) |

**총 AskUserQuestion 호출: 최대 9회** (Nano Banana 설정 포함)
