# init-protocol.md — /project init 전체 플로우 (v2.11.0)

## 개요

`/project init`은 Claude Cowork 프로젝트를 초기화하고, 사용자의 업무 워크플로우를 인터뷰한 뒤, **스킬 체이닝 기반 CLAUDE.md**를 생성한다.

**v2.11.0 핵심 변경 (v1.3 대비):**
- Phase 2 Inventory: 추상적 "플러그인 감지" → Bash + system reminder 교차 검증 구체 메커니즘
- Phase 4 Gap Detection 신규: 체인 스킬 ↔ Inventory 대조 → 누락 감지 → 설치 안내 → Re-entry
- `/project init resume` 커맨드 신규: 설치 완료 후 저장된 진행 상태에서 재개
- 17 → 22 플러그인 (moai-book·moai-bi·moai-pm·moai-sales·moai-commerce 추가)
- moai-media 7 → 4 스킬 (Higgsfield MCP·ElevenLabs MCP가 직접 지원)

**v1.3 핵심 변경 (v1.2 대비):**
- `/moai init` → `/project init` 커맨드 변경
- **글로벌 프로필 시스템 전면 제거** (이름·회사·역할 재질문 없음)
- 스킬 체인 설계(Phase 3) 신규 추가
- CLAUDE.md에 office/web 스킬 우선 규칙 + AI 슬롭 후처리 규칙 HARD로 고정

---

## 전체 플로우

```
/project init
    ↓
Phase 1: 워크플로우 인터뷰 (최대 3질문)
    ↓
Phase 2: Inventory — 설치된 플러그인·스킬 인벤토리 구성
    ↓
Phase 3: 스킬 체인 설계 (산출물별 파이프라인)
    ↓
Phase 4: Gap Detection — 누락 플러그인/스킬 감지 + 설치 안내 (신규)
    ↓ (누락 0건이거나 옵션 2/3 선택 시)
Phase 5: 설계 확인 (AskUserQuestion)
    ↓
Phase 6: CLAUDE.md 생성 (CLAUDE.md.tmpl 기반, ≤ 200라인)
    ↓
Phase 7: API 키 / 커넥터 (필요한 경우만)
    ↓
Phase 8: 첫 실행 안내 (스킬 체인 기반 예시 3개)
```

---

## Phase 1: 워크플로우 인터뷰

사용자의 **이 프로젝트 맥락**만 수집한다. 이름·회사·역할 같은 **글로벌 프로필 정보는 묻지 않는다**.

### 1-1. 업무 유형

AskUserQuestion (1질문, 4옵션, multiSelect)

```
"이 프로젝트에서 어떤 일을 하시나요? (복수 선택 가능)"

☐ 사업 기획·전략 — 사업계획서, 시장조사, IR, 투자제안서
☐ 콘텐츠 제작 — 블로그, 카드뉴스, 뉴스레터, SNS, 카피
☐ 문서·행정 — PPT, 한글, Word, Excel, 공문, 계약서
☐ 제품·연구 — PM 문서, UX 리서치, 논문, 특허, 데이터 분석
+ Other (직접 입력)
```

### 1-2. 주요 산출물

AskUserQuestion (1질문, 자유입력 + 예시 4개)

```
"주로 만드는 산출물은 무엇인가요? 구체적으로 적어주세요.
 예: '사업계획서 PPT, 투자자용 IR 덱, 언론 보도자료'
     '주 2회 블로그, 카드뉴스, 인스타 릴스 스크립트'
     '계약서 검토, 근로계약서, NDA 초안'
     'Series A 피칭 자료, 시장 분석 리포트'"

+ Other (자유 입력)
```

### 1-3. 톤·형식 제약 (선택)

AskUserQuestion (1질문, 4옵션)

```
"특별히 지키고 싶은 톤이나 형식 제약이 있나요?"

○ 공식·격식체 유지 (관공서·기업 보고)
○ 캐주얼·대화체 (SNS·블로그·콘텐츠)
○ 산업별 전문 용어 사용 (법률·의료·금융·기술)
○ 제약 없음 — 그때그때 지정
+ Other (직접 입력)
```

**수집 결과는 메모리에 임시 저장**되며, Phase 6에서 CLAUDE.md에 직접 기록된다.
별도 `moai-profile.md`를 생성하지 않는다.

---

## Phase 2: Inventory — 활성 스킬 인벤토리 구성 (v2.11.0 신규)

체인 설계에 앞서 실제 사용 가능한 스킬 목록을 정확히 구성한다.

### 2-1. 인벤토리 소스

**[HARD] 스캔 필터링 — cowork-plugins 출처만 인정 (v2.11.0)**:

`~/.claude/plugins/` 디렉토리에는 사용자가 여러 마켓플레이스에서 설치한 플러그인이 섞여있을 수 있다. project 스킬은 **cowork-plugins (modu-ai/cowork-plugins) 마켓플레이스 출처 22 플러그인만** 인벤토리에 포함시키고, 그 외 플러그인은 **완전히 제외**한다.

**cowork-plugins 22 플러그인 화이트리스트** (v2.11.0 기준, 괄호 안은 스킬 수):

```
moai-core (8)         moai-business (10)    moai-marketing (11)
moai-legal (5)        moai-finance (6)      moai-hr (5)
moai-content (12)     moai-operations (3)   moai-education (5)
moai-lifestyle (3)    moai-product (4)      moai-support (4)
moai-office (5)       moai-career (4)       moai-data (3)
moai-research (5)     moai-media (4)        moai-commerce (35)
moai-book (8)         moai-bi (1)           moai-pm (1)
moai-sales (1)
```

합계: 22 플러그인 / 143 스킬

**소스 A — Bash 디렉토리 스캔 (화이트리스트 필터 + 모든 SKILL.md 완전 스캔)**:

```bash
PLUGIN_DIR=~/.claude/plugins
WHITELIST=(moai-core moai-business moai-marketing moai-legal moai-finance \
           moai-hr moai-content moai-operations moai-education moai-lifestyle \
           moai-product moai-support moai-office moai-career moai-data \
           moai-research moai-media moai-commerce moai-book moai-bi \
           moai-pm moai-sales)

# Step 1: 화이트리스트 22 플러그인 중 실제 설치된 것만 식별
INSTALLED_COWORK_PLUGINS=()
for p in "${WHITELIST[@]}"; do
  if [ -d "$PLUGIN_DIR/$p" ] && [ -f "$PLUGIN_DIR/$p/.claude-plugin/plugin.json" ]; then
    INSTALLED_COWORK_PLUGINS+=("$p")
  fi
done

# Step 2: 발견된 cowork 플러그인 안의 모든 SKILL.md 완전 스캔
for plugin in "${INSTALLED_COWORK_PLUGINS[@]}"; do
  find "$PLUGIN_DIR/$plugin/skills" -maxdepth 2 -name SKILL.md 2>/dev/null
done

# Step 3: 화이트리스트 외 디렉토리(다른 마켓플레이스 출처)는 무시
# 예: ~/.claude/plugins/other-vendor-plugin/ → 인벤토리에서 완전 제외
```

각 SKILL.md frontmatter의 `name:` 필드를 추출해 `<skill-name> → <plugin>` 매핑을 구성한다. 화이트리스트 0건이면 "설치된 cowork 플러그인 없음"으로 처리하되, 소스 B로 보완한다.

**소스 B — system reminder 파싱 (cowork 출처만 필터링)**:

현재 세션 system reminder에 포함된 "user-invocable skills" 목록을 파싱하되, **cowork-plugins 출처 스킬만** 인벤토리에 등록한다.

- 포함: 22 화이트리스트 플러그인이 제공하는 스킬 (예: `moai-content:blog`, `moai-office:docx-generator`)
- 제외: 그 외 출처 스킬 (예: `find-skills`, `update-config`, `notion-cli`, 사용자가 별도 설치한 모든 스킬)

`plugin:skill-name` 형태로 추출하되, `plugin`이 22 화이트리스트에 없으면 인벤토리에서 제외한다.

**교차 검증 알고리즘**:

```
소스 A 목록 ∩ 22 화이트리스트 = cowork 설치 플러그인
소스 B 목록에서 cowork 출처만 필터링 = cowork 활성 스킬
두 소스 교차 → "플러그인 → [스킬, ...]" 매핑 구성
→ inventory.skills_available 딕셔너리 완성
```

두 소스가 일치하면 신뢰도 HIGH. 소스 B에만 있으면 신뢰도 MEDIUM(설치됐으나 디렉토리 구조가 다를 수 있음). 소스 A에만 있으면 신뢰도 MEDIUM(설치는 됐으나 세션에 로드되지 않음 — Claude Code 재시작 필요).

### 2-2. inventory.json 스키마

`.moai/cache/inventory.json`에 저장한다:

```json
{
  "scanned_at": "2026-05-18T00:00:00+09:00",
  "plugins_installed": ["moai-core", "moai-content", "moai-office"],
  "skills_available": {
    "blog": "moai-content",
    "card-news": "moai-content",
    "docx-generator": "moai-office",
    "pptx-designer": "moai-office",
    "ai-slop-reviewer": "moai-core"
  },
  "confidence": {
    "moai-content": "HIGH",
    "moai-office": "HIGH",
    "moai-core": "HIGH"
  }
}
```

### 2-3. Phase 1 답변 기반 매칭

인터뷰 답변에서 관련 플러그인을 우선 순위화한다:

| 업무 유형 | 우선 플러그인 |
|----------|------------|
| 사업 기획·전략 | moai-business, moai-finance |
| 콘텐츠 제작 | moai-content, moai-marketing, moai-media |
| 문서·행정 | moai-office, moai-legal, moai-hr |
| 제품·연구 | moai-product, moai-research, moai-data |
| 이커머스 | moai-commerce |
| 출판·원고 | moai-book |
| BI·보고 | moai-bi, moai-pm |
| 영업·제안 | moai-sales |

**moai-core는 항상 포함** (라우터·ai-slop-reviewer). 선택 UI에는 표시하지 않는다.

---

## Phase 3: 스킬 체인 설계 (핵심)

Phase 1-2 결과를 바탕으로 **산출물별 실행 체인**을 설계한다.

### 3-1. 체인 구성 규칙

각 산출물 체인은 다음 구조를 따른다:

```
[기획/분석 스킬] → [생성 스킬] → [포맷 변환 스킬 or 미디어 스킬] → ai-slop-reviewer
```

- 텍스트 산출물 체인은 **반드시 `ai-slop-reviewer`로 종료**
- 비텍스트(차트·데이터·숫자)는 ai-slop 단계 **생략**
- 체인이 단순하면 스킬 1-2개만으로도 OK
- **Inventory에 없는 스킬은 체인에서 제외하거나 Gap Detection으로 넘긴다**

### 3-2. 체인 프리셋 테이블 (주요 산출물)

| 산출물 | 권장 체인 |
|---|---|
| 사업계획서(Word) | `strategy-planner` → `market-analyst` → `docx-generator` → `ai-slop-reviewer` |
| 사업계획서(PPT) | `strategy-planner` → `pptx-designer` → `ai-slop-reviewer` |
| IR 피칭덱 | `investor-relations` → `pptx-designer` → `ai-slop-reviewer` |
| 시장조사 리포트 | `market-analyst` → `docx-generator` → `ai-slop-reviewer` |
| 블로그 포스트 | `blog` → `ai-slop-reviewer` |
| 카드뉴스 | `card-news` → `ai-slop-reviewer` |
| 뉴스레터 | `newsletter` → `ai-slop-reviewer` |
| 랜딩 페이지(HTML) | `copywriting` → `landing-page` → `ai-slop-reviewer` |
| SNS 콘텐츠 세트 | `sns-content` → `ai-slop-reviewer` |
| 이메일 시퀀스 | `email-sequence` → `ai-slop-reviewer` |
| 계약서 초안 | `contract-review` or `nda-triage` → `docx-generator` → `ai-slop-reviewer` |
| 컴플라이언스 체크 | `compliance-check` → `ai-slop-reviewer` |
| 부가세 신고 | `tax-helper` (숫자 산출물 — ai-slop 생략) |
| 재무제표 분석 | `financial-statements` → `xlsx-creator` (숫자 — ai-slop 생략) |
| 근로계약서 | `employment-manager` → `docx-generator` → `ai-slop-reviewer` |
| 채용 공고 | `draft-offer` → `ai-slop-reviewer` |
| 이력서·자기소개서 | `resume-builder` → `ai-slop-reviewer` |
| 논문 초안 | `paper-writer` → `docx-generator` → `ai-slop-reviewer` |
| 연구비 제안서 | `grant-writer` → `docx-generator` → `ai-slop-reviewer` |
| 특허 명세서 | `patent-analyzer` → `docx-generator` → `ai-slop-reviewer` |
| 한글 공문 | `hwpx-writer` → `ai-slop-reviewer` |
| 데이터 시각화 | `data-visualizer` (차트 — ai-slop 생략) |
| 제품 SPEC | `spec-writer` → `ai-slop-reviewer` |
| 로드맵 | `roadmap-manager` → `pptx-designer` → `ai-slop-reviewer` |
| 강의 커리큘럼 | `curriculum-designer` → `pptx-designer` → `ai-slop-reviewer` |
| 상세페이지 | `product-detail` → `ai-slop-reviewer` |
| 캠페인 플랜 | `campaign-planner` → `pptx-designer` → `ai-slop-reviewer` |
| SEO 감사 | `seo-audit` → `ai-slop-reviewer` |
| 출판 원고 | `book-manuscript` → `docx-generator` → `ai-slop-reviewer` |
| BI 리포트 | `executive-summary` (숫자·HTML — ai-slop 생략) |
| 주간보고 | `weekly-report` → `ai-slop-reviewer` |
| 영업 제안서 | `sales-proposal` → `docx-generator` → `ai-slop-reviewer` |
| TTS 더빙 | `audio-gen` (ElevenLabs MCP — ai-slop 생략) |
| 이미지 프롬프트 | `gpt-image-2-prompt` or `gemini-3-image-prompt` or `midjourney-v8-prompt` |

### 3-3. 체인 요약 포맷

Phase 5(확인 단계)에서 사용자에게 보여줄 요약:

```
이 프로젝트의 실행 체인 설계

[주 산출물 1] 사업계획서(PPT)
  체인: strategy-planner → pptx-designer → ai-slop-reviewer
  트리거 예시: "사업계획서 만들어줘"

[주 산출물 2] IR 피칭덱
  체인: investor-relations → pptx-designer → ai-slop-reviewer
  트리거 예시: "IR 자료 써줘"

[보조 산출물 3] 시장조사 리포트
  체인: market-analyst → docx-generator → ai-slop-reviewer
  트리거 예시: "시장조사 해줘"
```

---

## Phase 4: Gap Detection — 누락 플러그인/스킬 감지 (v2.11.0 신규)

### 4-1. 누락 감지 알고리즘

Phase 3에서 설계된 체인의 각 스킬을 Inventory와 대조한다:

```
for each skill in chain_skills:
    if skill not in inventory.skills_available:
        missing_skills.append(skill)
        missing_plugin = SKILL_PLUGIN_MAP[skill]  # 아래 4-2 매핑 참조
        missing_plugins.add(missing_plugin)
```

`ai-slop-reviewer`는 moai-core 소속이므로 항상 설치됨으로 간주한다.

### 4-2. 스킬 → 플러그인 기본 매핑

| 스킬 | 소속 플러그인 |
|------|------------|
| strategy-planner, market-analyst, investor-relations, consulting-brief | moai-business |
| blog, card-news, newsletter, landing-page, sns-content, email-sequence, copywriting | moai-content |
| docx-generator, pptx-designer, xlsx-creator, hwpx-writer, pdf-writer | moai-office |
| seo-audit, campaign-planner, sns-content | moai-marketing |
| nda-triage, contract-review, compliance-check | moai-legal |
| tax-helper, financial-statements | moai-finance |
| employment-manager, draft-offer | moai-hr |
| resume-builder, portfolio-guide | moai-career |
| data-visualizer, csv-analyzer | moai-data |
| paper-writer, grant-writer, patent-analyzer | moai-research |
| spec-writer, roadmap-manager, ux-researcher | moai-product |
| draft-response, kb-article | moai-support |
| curriculum-designer, assessment-creator | moai-education |
| travel-planner | moai-lifestyle |
| gpt-image-2-prompt, gemini-3-image-prompt, midjourney-v8-prompt, audio-gen | moai-media |
| product-detail, commerce-automation-audit | moai-commerce |
| book-manuscript | moai-book |
| executive-summary | moai-bi |
| weekly-report | moai-pm |
| sales-proposal | moai-sales |

### 4-3. 누락 발견 시 AskUserQuestion 4 옵션

누락 스킬이 하나라도 있으면 즉시 AskUserQuestion을 제시한다.

```
"체인에 필요한 스킬이 설치되지 않은 플러그인에 포함돼 있습니다."

누락 스킬: [skill-A] → [moai-X] 플러그인 필요
           [skill-B] → [moai-Y] 플러그인 필요

옵션:
  1. (권장) 설치 안내 받기 + 설치 후 재개
     → 설치 명령을 안내하고, 완료 후 '/project init resume'으로 재개합니다.
     → 현재 진행 상태(.moai/cache/init-progress.json)는 보존됩니다.
  2. 누락 스킬 제외하고 진행
     → 해당 체인 단계를 건너뛰고 설치된 스킬만으로 진행합니다.
     → 나중에 플러그인을 설치하면 CLAUDE.md를 직접 수정해 체인에 추가하세요.
  3. 대체 스킬로 변경
     → 현재 Inventory에서 유사 스킬을 추천하고 체인을 재설계합니다.
  4. 중단
     → 초기화를 중단합니다. 진행 상태는 저장되지 않습니다.
```

### 4-4. 옵션 1 선택 시: 설치 안내 흐름

```
1. 누락 플러그인별 설치 명령 안내:

   /plugin install modu-ai/cowork-plugins

   (개별 플러그인 설치가 아닌 전체 패키지 설치 후 활성화)
   Settings > Plugins > cowork-plugins > [moai-X] > Enable

2. .moai/cache/init-progress.json 저장 (4-5 스키마 참조)

3. 사용자에게 안내 메시지 출력:

   "플러그인을 설치하신 후 아래 방법으로 진행을 재개하세요:
    - '/project init resume' 입력
    - 또는 '이어서 진행', '설치 완료' 발화"
```

`.moai/cache/` 디렉토리가 없으면 `Bash("mkdir -p .moai/cache")`로 생성한다.

### 4-5. init-progress.json 스키마

```json
{
  "started_at": "2026-05-18T14:30:00+09:00",
  "phase_completed": 3,
  "interview_answers": {
    "work_type": ["사업 기획·전략"],
    "deliverables": "사업계획서 PPT, IR 피칭덱",
    "tone_constraints": "공식·격식체"
  },
  "chain_design": [
    {
      "deliverable": "사업계획서(PPT)",
      "chain": ["strategy-planner", "pptx-designer", "ai-slop-reviewer"],
      "trigger_example": "사업계획서 만들어줘"
    }
  ],
  "missing_skills": ["strategy-planner"],
  "missing_plugins": ["moai-business"]
}
```

### 4-6. 옵션 2 선택 시 (누락 제외 진행)

- `missing_skills`에 해당하는 체인 단계를 제거
- 체인 재구성 후 Phase 5 Confirm으로 진행
- CLAUDE.md의 해당 체인에 `# (moai-X 미설치 — 추후 추가)` 주석 삽입

### 4-7. 옵션 3 선택 시 (대체 스킬 변경)

- `inventory.skills_available`에서 유사 기능 스킬 검색
- 예: `strategy-planner` 부재 → `market-analyst`로 대체 제안
- 대체 스킬로 체인 재설계 후 Phase 5로 진행

### 4-8. 누락 0건이면

즉시 Phase 5 Confirm으로 진행한다. Inventory 재확인 없이 넘어간다.

---

## Phase 5: 설계 확인

AskUserQuestion (1질문, 3옵션)

```
"위 스킬 체인 설계로 CLAUDE.md를 생성하시겠습니까?"

○ 승인 — 이 설계로 생성 (권장)
○ 수정 — 체인 일부를 수정하고 싶음
○ 취소 — 초기화 중단
+ Other
```

"수정" 선택 시: 수정하고 싶은 체인을 자유입력으로 받아 Phase 3-2 테이블을 참조하여 재설계.

---

## Phase 6: CLAUDE.md 생성

`references/templates/CLAUDE.md.tmpl`을 로드하여 다음 변수를 치환한다:

| 변수 | 소스 |
|---|---|
| `{project_name}` | 현재 프로젝트 폴더명 |
| `{version}` | plugin.json의 moai-core version |
| `{date}` | 오늘 날짜 (YYYY-MM-DD) |
| `{installed_plugins}` | Phase 2 Inventory의 plugins_installed |
| `{primary_deliverables}` | Phase 1-2 답변 요약 |
| `{project_purpose}` | Phase 1-2 답변에서 추출 |
| `{audience}` | Phase 1-2에서 추출 또는 "미지정" |
| `{tone_constraints}` | Phase 1-3 답변 |
| `{workflow_chains}` | Phase 3에서 설계된 체인 블록 (Markdown) |
| `{routing_summary}` | 사용하는 플러그인의 라우팅 키워드만 요약 |
| `{connectors_and_apikeys}` | Phase 7 결과 요약 |
| `{project_context_notes}` | 자유 메모 (초기값: 비어있음) |

### 생성 원칙

1. **≤ 200라인** — 하네스 상세 복사 금지
2. **스킬 체인은 최대 10개까지** 나열 (나머지는 catalog 참조)
3. **HARD 규칙 블록(office 우선, ai-slop 후처리)은 항상 포함**
4. **파일 인코딩**: UTF-8, LF, 한국어
5. 누락 스킬 제외 진행(옵션 2) 시 해당 체인에 미설치 주석 포함

상세: `references/core/claudemd-generator.md`

---

## Phase 7: API 키 / 커넥터 (선택적)

Phase 2에서 선택된 플러그인이 API 키를 요구하면 등록 안내.

**API 키 목록:**

| # | 서비스 | 환경변수 | 용도 | 발급처 |
|---|--------|---------|------|--------|
| 1 | 공공데이터포털 | `DATA_GO_KR_API_KEY` | 공공데이터/KOSIS/KCI | data.go.kr |
| 2 | KIPRIS Plus | `KIPRIS_API_KEY` | 특허 검색 | plus.kipris.or.kr |
| 3 | 국가법령정보 | `KOREAN_LAW_OC` | 법령/판례 | law.go.kr |
| 4 | Google Gemini | `GEMINI_API_KEY` | gemini-3-image-prompt | ai.google.dev |
| 5 | fal.ai | `FAL_KEY` | fal-ai MCP (Flux·Recraft·Hailuo·Luma 등) | fal.ai |
| 6 | ElevenLabs | `ELEVENLABS_API_KEY` | audio-gen (TTS/보이스 클로닝, ElevenLabs MCP) | elevenlabs.io |

선택된 플러그인과 무관한 키는 물어보지 않는다.
**저장 위치**: `./.moai/credentials.env` (프로젝트 격리).

**커넥터**: Cowork 공식 커넥터(Google Drive, Notion, Gmail, Slack 등)는 Settings > Connectors 안내만 제공. init은 OAuth에 관여하지 않는다.

---

## Phase 8: 첫 실행 안내

Phase 3에서 설계된 체인 중 상위 3개를 예시로 제시:

```
설정이 완료되었습니다. 바로 시작해 보세요.

1. 사업계획서 제작
   당신: "초기 스타트업 사업계획서 PPT로 만들어줘"
   → 체인: strategy-planner → pptx-designer → ai-slop-reviewer
   → 결과: .pptx 파일 + 진단·수정 리포트

2. 시장조사 리포트
   당신: "2026 K-뷰티 시장 리포트 써줘"
   → 체인: market-analyst → docx-generator → ai-slop-reviewer

3. 블로그 발행
   당신: "창업 인사이트 블로그 글 하나 써줘"
   → 체인: blog → ai-slop-reviewer

전체 플러그인/스킬 목록: /project catalog
현재 설정 상태: /project status
```

---

## Re-entry: 설치 완료 후 진행 재개

### 진입 패턴

| 트리거 | 처리 |
|--------|------|
| `/project init resume` | 명시적 재개 커맨드 |
| "이어서 진행" | 자연어 → resume 흐름 자동 트리거 |
| "설치 완료" | 자연어 → resume 흐름 자동 트리거 |
| "다시 진행" | 자연어 → resume 흐름 자동 트리거 |

### 복원 흐름

```
1. .moai/cache/init-progress.json 존재 확인
   → 없으면: "저장된 진행 상태가 없습니다. /project init 으로 새로 시작하세요." 출력

2. init-progress.json 로드 (Phase 1-3 결과 복원)
   → 인터뷰 답변, 체인 설계, 누락 목록 복원

3. Phase 2 Inventory 재실행 (설치 확인)
   → Bash + system reminder 교차 검증으로 최신 Inventory 재구성
   → inventory.json 갱신

4. Phase 4 Gap Detection 재검증
   → init-progress.json의 missing_skills를 최신 Inventory와 재대조
   → 여전히 누락: AskUserQuestion 4 옵션 재제시
   → 누락 0건: "설치 확인 완료" 메시지 후 Phase 5 Confirm으로 진행

5. Phase 5 이후는 정상 흐름과 동일
```

### 재개 성공 메시지 예시

```
이전 진행 상태를 복원했습니다.

복원된 정보:
- 업무 유형: 사업 기획·전략
- 주요 산출물: 사업계획서 PPT, IR 피칭덱
- 체인 설계: 3개

설치 확인:
- moai-business: ✓ 설치됨
- moai-office: ✓ 설치됨

모든 필요 플러그인이 설치되었습니다. 체인 설계를 확인하세요.
```

---

## /project apikey — API 키 관리

```
/project apikey
```

7개 API 키를 조회/변경/추가/삭제한다.

---

## AskUserQuestion 제약 준수 요약

| Phase | 질문 수 | 옵션 수 |
|-------|---------|---------|
| Phase 1-1 업무 유형 | 1 | 4 (multiSelect) |
| Phase 1-2 산출물 | 1 | 자유입력 |
| Phase 1-3 톤·제약 | 1 | 4 |
| Phase 4 Gap Detection (조건부) | 1 | 4 |
| Phase 5 설계 확인 | 1 | 3 |
| Phase 7 API 키 (조건부) | 1-2 | 최대 4 (multiSelect) |
| **합계** | **최대 7회** | 모두 ≤ 4 |

---

## v1.3 대비 v2.11.0 변경 요약

| 항목 | v1.3 | v2.11.0 |
|------|------|---------|
| Phase 수 | 7 (1-7) | 8 (1-8, Gap Detection 추가) |
| Phase 2 메커니즘 | 추상적 "자동 감지" | Bash + system reminder 교차 검증 |
| 누락 플러그인 처리 | 안내만 제공 (비차단) | Phase 4 Gap Detection — 4 옵션 제시 + Re-entry |
| 재개 커맨드 | 없음 | `/project init resume` + 자연어 패턴 |
| 진행 상태 저장 | 없음 | `.moai/cache/init-progress.json` |
| 활성 인벤토리 캐시 | 없음 | `.moai/cache/inventory.json` |
| 지원 플러그인 수 | 17개 | 22개 |
| moai-media 스킬 수 | 7개 | 4개 (Higgsfield·ElevenLabs MCP 직접 호출) |
| API 키 목록 | Gemini·fal.ai·ElevenLabs 등 | 동일 + Gemini 용도 명칭 변경 |
