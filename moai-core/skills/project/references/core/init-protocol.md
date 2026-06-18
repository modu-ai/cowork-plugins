# init-protocol.md — /project 초기화 전체 플로우

## 개요

bare `/project`(또는 레거시 `/project init`)는 Claude Cowork 프로젝트를 초기화하고, 사용자의 업무 워크플로우를 인터뷰한 뒤, **스킬 체이닝 기반 CLAUDE.md**를 생성한다.

**현재 상태:**
- 초기화 워크플로우는 bare `/project`가 기본 진입점이며, `/project init`은 레거시 별칭으로 계속 인식된다(비파괴).
- Phase 2 Inventory는 설치된 cowork 플러그인을 **동적으로 도출**(plugin.json 스캔)하여 신규 플러그인을 자동 포함한다.
- Phase 4 Gap Detection: 체인 스킬 ↔ Inventory 대조 → 누락 감지 → 설치 안내 → Re-entry.
- `/project resume`로 설치 완료 후 저장된 진행 상태에서 재개한다(레거시 `/project init resume`도 인식).
- 글로벌 프로필 시스템은 사용하지 않는다(이름·회사·역할 재질문 없음). 프로젝트 맥락만 CLAUDE.md에 기록한다.
- CLAUDE.md에 office/web 스킬 우선 규칙 + AI 슬롭 후처리 규칙이 HARD로 고정 포함된다.

---

## 전체 플로우

```
/project (또는 /project init — 레거시 별칭)
    ↓
Phase 1: 워크플로우 인터뷰 (최대 3질문)
    ↓
Phase 2: Inventory — 설치된 플러그인·스킬 인벤토리 구성
    ↓
Phase 3: 스킬 체인 설계 (산출물별 파이프라인)
    ↓
Phase 3.5: Agent Synthesis — 자격 워크플로우를 전담 프로젝트 에이전트로 생성 (선택, ./.claude/agents/)
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

## Phase 2: Inventory — 활성 스킬 인벤토리 구성

체인 설계에 앞서 실제 사용 가능한 스킬 목록을 정확히 구성한다.

### 2-1. 인벤토리 소스

**[HARD] 스캔 필터링 — cowork-plugins 출처만 인정 (동적 도출)**:

`~/.claude/plugins/` 디렉토리에는 사용자가 여러 마켓플레이스에서 설치한 플러그인이 섞여있을 수 있다. project 스킬은 **cowork-plugins (modu-ai/cowork-plugins) 마켓플레이스 출처 플러그인만** 인벤토리에 포함시키고, 그 외 플러그인은 **완전히 제외**한다.

**[HARD] 플러그인 집합은 하드코딩 화이트리스트가 아니라 동적으로 도출한다.** `moai-*` 접두어 디렉토리이면서 cowork-plugins 마켓플레이스 출처인 플러그인을 plugin.json 스캔으로 식별한다. 이렇게 하면 마켓플레이스에 신규 플러그인이 추가될 때 화이트리스트를 수정하지 않아도 자동으로 포함된다. **카운트(플러그인 수·스킬 수)는 하드코딩하지 않는다.**

현재 스냅샷 — **27 플러그인 / 173 스킬** (동적 도출 결과의 참고 스냅샷일 뿐, 고정값 아님):

```
moai-core          moai-business      moai-marketing
moai-legal         moai-finance       moai-hr
moai-content       moai-operations    moai-education
moai-lifestyle     moai-product       moai-support
moai-office        moai-career        moai-data
moai-public-data   moai-research      moai-media
moai-commerce      moai-bi            moai-pm
moai-sales         moai-book          moai-design
moai-wealth        moai-productivity  moai-comms
```

합계: 현재 27 플러그인 / 173 스킬 (동적 도출 — 카운트 하드코딩 금지)

**소스 A — Bash 디렉토리 스캔 (moai-* 글롭 + cowork 출처 필터 + 모든 SKILL.md 완전 스캔)**:

```bash
PLUGIN_DIR=~/.claude/plugins

# Step 1: moai-* 접두어 디렉토리 중 cowork-plugins 마켓플레이스 출처만 동적 식별
#   - plugin.json이 존재하고
#   - 해당 플러그인이 cowork-plugins 마켓플레이스에서 설치된 것
#   (화이트리스트를 고정하지 않는다 — 신규 플러그인 자동 포함)
INSTALLED_COWORK_PLUGINS=()
for dir in "$PLUGIN_DIR"/moai-*; do
  p=$(basename "$dir")
  if [ -d "$dir" ] && [ -f "$dir/.claude-plugin/plugin.json" ]; then
    # cowork-plugins 출처 검증: 마켓플레이스 메타데이터/plugin.json author·repository로 확인
    INSTALLED_COWORK_PLUGINS+=("$p")
  fi
done

# Step 2: 발견된 cowork 플러그인 안의 모든 SKILL.md 완전 스캔
for plugin in "${INSTALLED_COWORK_PLUGINS[@]}"; do
  find "$PLUGIN_DIR/$plugin/skills" -maxdepth 2 -name SKILL.md 2>/dev/null
done

# Step 3: moai-* 가 아니거나 cowork 출처가 아닌 디렉토리는 무시
# 예: ~/.claude/plugins/other-vendor-plugin/ → 인벤토리에서 완전 제외
```

각 SKILL.md frontmatter의 `name:` 필드를 추출해 `<skill-name> → <plugin>` 매핑을 구성한다. cowork 플러그인 0건이면 "설치된 cowork 플러그인 없음"으로 처리하되, 소스 B로 보완한다.

**소스 B — system reminder 파싱 (cowork 출처만 필터링)**:

현재 세션 system reminder에 포함된 "user-invocable skills" 목록을 파싱하되, **cowork-plugins 출처 스킬만** 인벤토리에 등록한다.

- 포함: cowork-plugins 마켓플레이스 출처 `moai-*` 플러그인이 제공하는 스킬 (예: `moai-content:blog`, `moai-office:docx-generator`)
- 제외: 그 외 출처 스킬 (예: `find-skills`, `update-config`, `notion-cli`, 사용자가 별도 설치한 모든 스킬)

`plugin:skill-name` 형태로 추출하되, `plugin`이 cowork 출처 `moai-*` 집합에 없으면 인벤토리에서 제외한다.

**교차 검증 알고리즘**:

```
소스 A 목록 (moai-* ∩ cowork 출처) = cowork 설치 플러그인
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
  "agents_available": {
    "content-publishing-pipeline": "moai-content",
    "office-doc-qa": "moai-office"
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
| 제품·연구 | moai-product, moai-research, moai-data, moai-public-data |
| 이커머스 | moai-commerce |
| 출판·원고 | moai-book |
| BI·보고 | moai-bi, moai-pm |
| 영업·제안 | moai-sales |
| 디자인 핸드오프 | moai-design |
| 자산·재무 설계 | moai-wealth |
| 생산성·루틴 | moai-productivity |
| 커뮤니케이션·협업 | moai-comms |

**moai-core는 항상 포함** (라우터·ai-slop-reviewer). 선택 UI에는 표시하지 않는다.

### 2-4. 에이전트 인벤토리 (코디네이터 동적 스캔)

스킬과 함께, 설치된 cowork 플러그인이 번들한 **코디네이터 에이전트**(`<plugin>/agents/*.md`)도 동적으로 인벤토리에 등록한다. 스킬 인벤토리와 동일하게 **하드코딩 목록 금지**(신규 코디네이터 자동 포함).

```bash
for plugin in "${INSTALLED_COWORK_PLUGINS[@]}"; do
  for af in "$PLUGIN_DIR/$plugin"/agents/*.md; do
    [ -f "$af" ] || continue
    grep -m1 '^name:' "$af" | sed 's/^name: *//'   # → agents_available[name] = plugin
  done
done
```

각 에이전트 `name`·`description`(호출 트리거)을 추출해 `inventory.json`의 `agents_available`에 등록한다. 플러그인이 설치돼 있으면 그 코디네이터도 가용으로 간주한다(에이전트는 플러그인 번들). 코디네이터는 **Cowork 서브에이전트 전용**이다. 상세·도메인 매핑·결정 규칙은 `references/core/agent-catalog.md` 참조.

---

## Phase 3: 스킬 체인 설계 (핵심)

Phase 1-2 결과를 바탕으로 **산출물별 실행 체인**을 설계한다. 스킬뿐 아니라 **기존 코디네이터 에이전트를 우선 활용**한다.

### 3-0. 코디네이터 우선 원칙 (agent-aware)

각 산출물 워크플로우마다 다음 순서로 실행기를 정한다(상세: `agent-catalog.md` §결정 규칙):

1. **매칭 코디네이터 존재** + 워크플로우가 그 도메인 체인과 일치 → **코디네이터 에이전트를 우선 실행기로 추천**(CLAUDE.md 체인에 담당 코디네이터 명시). 코디네이터가 내부에서 ai-slop·humanize까지 처리하면 후처리를 중복 추가하지 않는다.
2. **매칭 코디네이터 없음 / 부분 커버 / 단순 1-2단계** → 아래 인라인 스킬 체인(3-1·3-2)으로 설계.
3. 코디네이터도 없고 자격 조건(고정 게이트·병렬 fan-out·고빈도) 충족 → Phase 3.5 신규 에이전트 생성 후보.

매칭 판정은 `inventory.json`의 `agents_available`과 `agent-catalog.md` 매핑을 사용한다. cowork-plugins는 Cowork를 대상 환경으로 가정한다.

### 3-1. 체인 구성 규칙

각 산출물 체인은 다음 구조를 따른다:

```
[기획/분석 스킬] → [생성 스킬] → [포맷 변환 스킬 or 미디어 스킬] → ai-slop-reviewer
```

- 텍스트 산출물 체인은 **반드시 `moai-core:ai-slop-reviewer`로 종료**
- **한국어 최종본**은 ai-slop-reviewer 직후 `moai-content:humanize-korean`을 2차 패스로 추가
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
| SNS 콘텐츠 세트 | `moai-marketing:sns-content` → `ai-slop-reviewer` |
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
| 출판 원고 | `book-concept-planner` → `book-outline-designer` → `book-chapter-writer` → `ai-slop-reviewer` (moai-book 체인) |
| BI 리포트 | `executive-summary` (숫자·HTML — ai-slop 생략) |
| 주간보고 | `weekly-report` → `ai-slop-reviewer` |
| 영업 제안서 | `proposal-writer` → `docx-generator` → `ai-slop-reviewer` |
| 자산·재무 로드맵 | `wealth-roadmap` → `ai-slop-reviewer` |
| 커뮤니케이션 스크립트 | `report-speak` → `ai-slop-reviewer` |
| 영상 | `higgsfield-video` (Higgsfield MCP — ai-slop 생략) |
| TTS 더빙 | `audio-gen` (ElevenLabs MCP — ai-slop 생략) |
| 이미지 | `higgsfield-image` (Higgsfield MCP — ai-slop 생략) |
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

## Phase 3.5: Agent Synthesis (프로젝트 에이전트 생성)

Phase 3에서 설계된 체인 중 **전담 에이전트로 만들 가치가 있는데 매칭되는 기존 코디네이터가 없는** 워크플로우만 프로젝트 전용 서브에이전트로 생성한다. 디스크에 직접 작성하는 `./.claude/agents/<name>.md`는 서브에이전트 스코프 우선순위 3(플러그인 에이전트 5보다 높음)이며 Cowork/Claude Code가 세션 시작 시 자동 로드한다.

> **기존 코디네이터 우선 (HARD)**: cowork-plugins 각 도메인 플러그인은 코디네이터 에이전트(`<plugin>/agents/*.md`, 현재 스냅샷 31개)를 번들한다. **Phase 3.5는 기존 코디네이터로 커버되지 않는 워크플로우에만 신규 에이전트를 생성한다.** 매칭 코디네이터가 있으면 그것을 우선 활용하고(§Phase 3 코디네이터 우선), 신규 생성하지 않는다. 매핑·결정 규칙은 `agent-catalog.md` 참조.

이 Phase는 **선택·additive**다. 자격 워크플로우가 없거나 사용자가 "생성 안 함"을 고르면 아무 에이전트도 만들지 않고 Phase 4로 넘어간다. bare `/project`는 에이전트를 하나도 생성하지 않아도 정상 동작한다.

### 3.5-1. 자격 판정 규칙 (Decision Rule)

**Step 0 (선행) — 기존 코디네이터 확인**: 워크플로우에 매칭되는 기존 코디네이터(`agents_available`·`agent-catalog.md`)가 있으면 그것을 사용하고 **신규 생성하지 않는다**. 아래 자격 규칙은 매칭 코디네이터가 **없을 때만** 적용한다.

전담 프로젝트 에이전트는 (매칭 코디네이터가 없고) 다음 중 **하나 이상**을 만족하는 워크플로우에만 생성한다:

- **(a) 고정 다단계 파이프라인 + 비우회 컴플라이언스/면책 게이트** — 단계 순서가 고정돼 있고, 중간에 반드시 통과해야 하는 법적·면책 게이트가 있는 경우.
- **(b) 병렬 fan-out** — 여러 산출물을 동시에 생성한 뒤 하나로 종합해야 하는 경우(여러 스킬을 병렬 호출 → 종합).
- **(c) 사용자가 매우 자주 반복하는 동일 파이프라인** — 같은 체인을 반복 호출하는 빈도가 높아 전담 에이전트화가 토큰·맥락 측면에서 유리한 경우.

**생성하지 않는다(에이전트 남발 금지)**:

- 단일 스킬 호출로 끝나는 워크플로우
- 단순 1-2단계 체인 → orchestrator 인라인 스킬체이닝으로 충분

자격 미달 워크플로우는 CLAUDE.md의 "프로젝트 워크플로우(스킬 체인)" 섹션에 체인으로만 남기고, 별도 에이전트를 만들지 않는다.

### 3.5-2. Socratic 질문 (AskUserQuestion)

자격 규칙을 만족하는 체인이 **하나라도** 있으면 AskUserQuestion을 1회 제시한다(multiSelect). 후보는 **자격 충족 체인만** 나열하고, "생성 안 함" 옵션을 항상 포함한다.

```
"Phase 3에서 설계한 체인 중 전담 에이전트로 만들 워크플로우를 선택하세요. (복수 선택 가능)"

☐ [재무 보고 패키지] 병렬 fan-out + 세무 면책 게이트 → 전담 에이전트 권장
☐ [신상품 런칭]      고정 파이프라인 + 정보통신망법 게이트 → 전담 에이전트 권장
☐ 생성 안 함 — 인라인 스킬체이닝으로 충분
+ Other
```

자격 충족 체인이 **0건**이면 이 질문을 띄우지 않고 **Phase 3.5 전체를 건너뛴다**(Phase 4로 직행).

### 3.5-3. Writer 스텝

선택된 각 워크플로우마다 다음을 수행한다:

```
1. .claude/agents/ 디렉토리 확인
   - 없으면: Bash("mkdir -p .claude/agents")

2. 템플릿 로드
   Read: references/templates/agent.md.tmpl

3. 변수 치환
   - {agent_name}          체인을 대표하는 소문자-하이픈 식별자(파일명과 동일). 예: finance-report-pack
   - {agent_description}    호출 트리거 + 역할 서술 (블록 스칼라 본문, 여러 줄 가능)
   - {agent_tools}          기본 "Read, Grep, Glob, Write, Edit, WebSearch" (Cowork 서브에이전트 표준 — Bash·WebFetch는 Cowork 서브에이전트에서 미동작하므로 기본 도구에서 제외. 셸 작업이 필요하면 부모 세션에 위임)
   - {agent_color}          공식 enum 중 택1 (red/blue/green/yellow/purple/orange/pink/cyan)
   - {agent_display_name}   한국어 제목. 예: 재무 보고 패키지 에이전트
   - {agent_role_sentence}  역할 1-2문장 요약
   - {chain_steps_block}    Phase 3 체인을 번호 매긴 "작업 절차" 블록으로 변환

4. Write: ./.claude/agents/{agent_name}.md
```

[HARD] `{agent_description}`는 반드시 템플릿의 `description: |` 블록 스칼라 본문으로 주입한다. 인라인 description 안에 콜론+공백(예: `위임하세요: "..."`)이 들어가면 YAML frontmatter가 깨진다.

### 3.5-4. 활성화 안내 (HARD)

디스크에 직접 작성한 에이전트는 **세션 시작 시점에만 로드**된다. 따라서 생성 직후 사용자에게 **반드시** 활성화 안내를 출력한다:

```
프로젝트 에이전트 N개를 생성했습니다: ./.claude/agents/

- finance-report-pack — 재무 보고 패키지(병렬 fan-out + 세무 면책 게이트)
- commerce-launch     — 신상품 런칭(고정 파이프라인 + 정보통신망법 게이트)

⚠️ 디스크에 작성된 에이전트는 세션 시작 시 로드됩니다.
   새 세션을 시작(또는 /reload-plugins)해야 활성화됩니다.
   활성화 후 자연어로 위임하면 자동 호출됩니다.
```

### 3.5-5. 자격 워크플로우 예시

다음 두 예시는 **매칭되는 기존 코디네이터가 없을 때** 신규 생성하는 파이프라인 형태를 보여준다(기존 코디네이터가 있으면 그것을 우선 사용한다).

**예시 A — 재무 보고 패키지 에이전트** `[병렬 fan-out + 게이트 → 자격]`

```
병렬: (moai-finance:close-management ∥ moai-finance:variance-analysis ∥ moai-finance:financial-statements)
   → 종합: board pack(이사회 보고 패키지)으로 통합
   → 표·수치: moai-office:xlsx-creator (검수 제외)
   → 서술 부분만: moai-core:ai-slop-reviewer → moai-content:humanize-korean
   → 게이트: moai-finance:tax-helper 검토 + 세율·4대보험 면책 고지(비우회)
```

- 자격 근거: 3개 재무 스킬을 병렬 fan-out 후 board pack으로 종합(b) + 세무 면책 게이트(a).
- 표·수치(xlsx)는 ai-slop·humanize 검수 대상에서 제외, 서술 부분만 검수.

**예시 B — 신상품 런칭 에이전트** `[고정 파이프라인 + 비우회 게이트 → 자격]`

```
moai-commerce:commerce-market-research
   → moai-commerce:commerce-jtbd-persona
   → moai-commerce:commerce-product-naming
   → 병렬: (moai-commerce:commerce-channel-message ∥ moai-commerce:commerce-product-image-pipeline)
   → 게이트: moai-commerce:commerce-marketing-compliance-kr (정보통신망법 비우회 검수)
   → moai-commerce:commerce-integrated-strategy
```

- 자격 근거: 시장조사→페르소나→네이밍→채널/이미지→통합전략의 고정 순서 파이프라인(a) + 정보통신망법 컴플라이언스 게이트(a, 비우회).
- 채널 메시지·이미지 파이프라인은 병렬 fan-out, 컴플라이언스 게이트는 발행 전 반드시 통과.

위 예시의 스킬명은 모두 moai-finance·moai-commerce에 실재하는 정확한 이름이다. 임의 스킬명을 만들지 않는다.

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
| blog, card-news, newsletter, landing-page, copywriting, product-detail, humanize-korean | moai-content |
| docx-generator, pptx-designer, xlsx-creator, hwpx-writer, pdf-writer | moai-office |
| seo-audit, campaign-planner, sns-content, email-sequence, brand-identity | moai-marketing |
| nda-triage, contract-review, compliance-check | moai-legal |
| tax-helper, financial-statements | moai-finance |
| employment-manager, draft-offer | moai-hr |
| resume-builder, portfolio-guide | moai-career |
| data-visualizer, data-explorer, public-data | moai-data |
| paper-writer, grant-writer, patent-analyzer | moai-research |
| spec-writer, roadmap-manager, ux-researcher | moai-product |
| draft-response, kb-article | moai-support |
| curriculum-designer, assessment-creator | moai-education |
| travel-planner, event-planner | moai-lifestyle |
| higgsfield-image, higgsfield-video, gpt-image-2-prompt, gemini-3-image-prompt, midjourney-v8-prompt, audio-gen | moai-media |
| commerce-automation-audit, marketplace-coupang, product-photo-brief | moai-commerce |
| book-concept-planner, book-outline-designer, book-chapter-writer | moai-book |
| executive-summary | moai-bi |
| weekly-report | moai-pm |
| proposal-writer | moai-sales |
| korean-stock-search, court-auction-search, real-estate-search | moai-public-data |
| claude-design-brief, claude-design-prompt-builder | moai-design |
| wealth-roadmap, household-budget | moai-wealth |
| goal-planner, retro-builder | moai-productivity |
| report-speak, meeting-facilitator | moai-comms |

### 4-3. 누락 발견 시 AskUserQuestion 4 옵션

누락 스킬이 하나라도 있으면 즉시 AskUserQuestion을 제시한다.

```
"체인에 필요한 스킬이 설치되지 않은 플러그인에 포함돼 있습니다."

누락 스킬: [skill-A] → [moai-X] 플러그인 필요
           [skill-B] → [moai-Y] 플러그인 필요

옵션:
  1. (권장) 설치 안내 받기 + 설치 후 재개
     → 설치 명령을 안내하고, 완료 후 '/project resume'으로 재개합니다.
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
    - '/project resume' 입력 (레거시 '/project init resume'도 인식)
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
| `{workflow_chains}` | Phase 3에서 설계된 체인 블록 (Markdown, 담당 코디네이터 명시) |
| `{coordinator_agents}` | 이 프로젝트 관련 기존 코디네이터 에이전트 표 (§5.4, `agents_available` 기반) |
| `{generated_agents}` | Phase 3.5에서 생성된 프로젝트 에이전트 목록 (§5.5, 없으면 비움) |
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
| 5 | Higgsfield | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_SECRET` | Higgsfield MCP (Soul·DOP·말하는머리·캐릭터 단일 통합) | higgsfield.ai |
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
| `/project resume` | 명시적 재개 커맨드 |
| `/project init resume` | 레거시 별칭 — 계속 인식(비파괴) |
| "이어서 진행" | 자연어 → resume 흐름 자동 트리거 |
| "설치 완료" | 자연어 → resume 흐름 자동 트리거 |
| "다시 진행" | 자연어 → resume 흐름 자동 트리거 |

### 복원 흐름

```
1. .moai/cache/init-progress.json 존재 확인
   → 없으면: "저장된 진행 상태가 없습니다. /project 로 새로 시작하세요." 출력

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
| Phase 3.5 Agent Synthesis (조건부) | 1 | multiSelect (자격 체인 + "생성 안 함") |
| Phase 4 Gap Detection (조건부) | 1 | 4 |
| Phase 5 설계 확인 | 1 | 3 |
| Phase 7 API 키 (조건부) | 1-2 | 최대 4 (multiSelect) |
| **합계** | **최대 7회** | 모두 ≤ 4 |

---

## 현재 상태 요약

현재: 27 플러그인 / 173 스킬 (동적 도출, 카운트 하드코딩 금지), bare `/project` 초기화가 기본 진입점이며 `/project init`은 레거시 별칭으로 인식된다.
