# init-protocol.md — `/project` 초기화 전체 플로우

## 개요

`/project`는 모두의 코워크 프로젝트를 초기화하고, 사용자의 업무 워크플로우를 인터뷰한 뒤, **스킬 체이닝 + 프로젝트 전용 커스텀 에이전트 기반 AGENTS.md**(폴더 지침 정본)와 이를 불러오는 `CLAUDE.md` 포인터를 생성한다.

**현재 상태**:
- Phase 2 인벤토리는 설치된 플러그인을 **동적으로 도출**(plugin.json 스캔)하여 신규 플러그인을 자동 포함한다.
- Phase 4 Gap Detection: 체인 스킬 ↔ 인벤토리 대조 → 누락 감지 → 설치 안내 → Re-entry.
- 설치 완료 후 사용자가 "이어서 진행"·"설치 완료"라고 하면 저장된 진행 상태에서 재개한다(자연어 단일 경로).
- 글로벌 프로필 시스템은 사용하지 않는다(이름·회사·역할 재질문 없음).
- 생성 `AGENTS.md`에 8개 HARD 규칙 블록이 고정 포함된다.

---

## 전체 플로우

```
/project
    ↓
Phase 1: 워크플로우 인터뷰 (맥락 충분까지 수집)
    ↓
Phase 2: Inventory — 설치된 플러그인·스킬 인벤토리 구성
    ↓
Phase 3: 스킬 체인 설계 (산출물별 파이프라인)
    ↓
Phase 4: Gap Detection — 누락 플러그인/스킬 감지 + 설치 안내
    ↓ (누락 0건이거나 옵션 2/3 선택 시)
Phase 5: 설계 확인 (AskUserQuestion)
    ↓
Phase 6: 지침 생성 (AGENTS.md.tmpl 기반 AGENTS.md ≤500라인 + CLAUDE.md 포인터)
    ↓
Phase 7: 커스텀 에이전트 생성 (.claude/agents/*.md + .codex/agents/*.toml)
    ↓
Phase 8: API 키 / 커넥터 + 첫 실행 안내
```

---

## Phase 1: 워크플로우 인터뷰 (커버리지 기반 · 라운드 무제한)

사용자의 **이 프로젝트 맥락**만 수집한다. 이름·회사·역할 같은 **글로벌 프로필 정보는 묻지 않는다**.

**[HARD] 질문은 나눠 내지 않는다.** 과거의 1-1/1-2/1-3 3연발 순차 호출은 폐기됐다. 한 라운드에 필요한 질문을 **모두 묶어 한 번의 `AskUserQuestion`으로** 낸다.

### S1 — 일괄 진단 라운드 (`AskUserQuestion` 1회, 최대 4질문 × 각 4옵션)

질문은 **고정 세트가 아니다.** 아래 풀에서 이번 프로젝트에 정보 이득이 큰 순으로 4개를 골라 **한 화면에 배치**한다.

| # | 축 | 형태 | 기본 선택지 예시 |
|---|---|---|---|
| ① | 업무 유형 | multiSelect 4옵션 | 사업 기획·전략 / 콘텐츠 제작 / 문서·행정 / 제품·연구 |
| ② | 주요 산출물 | 4옵션(+Other 자유입력) | 보고서·기획서 / 마케팅 콘텐츠 / 계약·공문 / 데이터·분석물 |
| ③ | 대상 독자·수신자 | 4옵션 | 경영진·투자자 / 고객·소비자 / 내부 팀·부서 / 공공기관·심사역 |
| ④ | 톤·형식 제약 | 4옵션 | 공식·격식체 / 캐주얼·대화체 / 산업 전문용어 / 제약 없음 |
| ⑤ | 산출물 포맷 | multiSelect 4옵션 | 한글(HWP) / PPTX·Word / 웹·노션·마크다운 / 이미지·영상 |
| ⑥ | 작업 주기·마감 | 4옵션 | 일회성 / 주간 반복 / 월간 반복 / 상시·수시 |
| ⑦ | 기존 자료 유무 | 4옵션 | 기존 산출물 있음 / 레퍼런스만 있음 / 브랜드 가이드 있음 / 백지에서 시작 |
| ⑧ | 반드시 피할 것 | 4옵션(+Other) | 과장·단정 표현 / 특정 경쟁사 언급 / 개인정보 노출 / 없음 |
| ⑨ | 배경·동기 (소크라테스 축) | 4옵션(+Other) | 신규 사업 착수 / 기존 업무 자동화 / 품질 편차 해소 / 인력 부족 보완 |

**슬롯 채우기 규칙 (HARD)**: 진입 발화·기존 `./AGENTS.md`·`.moai/context.md`에서 **이미 확보된 축은 질문 목록에서 제거**하고, 빈 슬롯은 다음 순위 축으로 채워 **항상 4슬롯을 채운다**. 남은 축이 4개 미만이면 그만큼만 낸다.

**작성 규칙**: 모든 옵션에 `description`(선택 시 무엇이 달라지는지)을 붙인다. 첫 옵션에만 `(권장)` 라벨. 자유 서술이 필요한 축은 `Other`로 흡수한다(별도 텍스트 질문을 만들지 않는다).

### S2 — 보강 라운드 (조건부, `AskUserQuestion` 추가 호출)

**발동 조건** — 하나라도 해당할 때만 실행한다:

| 조건 | 판정 신호 |
|---|---|
| (a) 필수 축 공백 | A등급 + 필수 B등급 중 미확보 항목 존재 |
| (b) 저신뢰 응답 | `Other` 선택, 모호한 자유입력 |
| (c) 답변 상충 | 예: 산출물=공문인데 톤=캐주얼 |
| (d) 슬롯 초과 | S1의 4슬롯에 못 담은 필수 축이 남음 |

해당 없으면 **S2를 건너뛰지 않고 즉시 Phase 2로 진행**한다. 실행할 때도 질문을 쪼개지 않고 **부족분을 한 번에 묶어** 배치한다. S2가 2회를 넘어가면 그 라운드에 「지금 아는 것으로 진행」 옵션을 함께 넣어 사용자가 종료할 수 있게 한다.

### 종료 판정

라운드 수를 미리 정하지 않는다. **A등급 + 필수 B등급이 채워지면 종료**한다. 수집 결과는 메모리에 임시 저장되며, Phase 6에서 `AGENTS.md`에 직접 기록된다. 별도 `moai-profile.md`를 생성하지 않는다.

---

## Phase 2: Inventory — 활성 스킬 인벤토리 구성

### 2-1. 인벤토리 소스

**[HARD] 스캔 필터링 — moai-cowork 출처만 인정 (동적 도출)**: `~/.claude/plugins/`(Claude)와 `~/.codex/plugins/`(Codex)에는 여러 마켓플레이스 플러그인이 섞여있을 수 있다. project 스킬은 **양쪽을 모두 스캔**해 **moai-cowork(modu-ai/moai-cowork) 마켓플레이스 출처 플러그인만** 인벤토리에 포함하고, 그 외는 완전히 제외한다.

**[HARD] 플러그인 집합은 하드코딩 화이트리스트가 아니라 동적으로 도출한다.** `moai-*` 접두어이면서 moai-cowork 마켓플레이스 출처인 플러그인을 `plugin.json` 스캔으로 식별한다. 마켓플레이스에 신규 플러그인이 추가되면 자동으로 포함된다. **카운트(플러그인 수·스킬 수)는 하드코딩하지 않는다** — `.claude-plugin/marketplace.json`이 로스터 정본이다.

**소스 A — Bash 디렉터리 스캔**:

```bash
# [HARD] 설치 깊이를 가정하지 않는다. 매니페스트를 먼저 찾고 거기서 플러그인
# 루트를 역산한다. 실측(2026-08-27): Claude는 ~/.claude/plugins/<plugin>/,
# Codex는 ~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/ 로 깊이가
# 두 단계 다르다. 고정 glob(`cache/*/moai-*`)을 쓰면 Codex 설치에서 0개가
# 잡히고, 전수 탐색·Gap Detection·체인 설계가 빈 인벤토리로 돌아간다.
ROOTS="$HOME/.claude/plugins $HOME/.codex/plugins/cache"
SEEN=""
for m in $(find $ROOTS -maxdepth 6 -type f \
             \( -path '*/.claude-plugin/plugin.json' -o -path '*/.codex-plugin/plugin.json' \) 2>/dev/null); do
  name=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('name',''))" "$m" 2>/dev/null)
  case "$name" in moai-*) ;; *) continue ;; esac
  root=$(dirname "$(dirname "$m")")          # <plugin>/<version> 또는 <plugin>
  # 같은 폴더에 .claude-plugin과 .codex-plugin이 둘 다 있으면 두 번 잡힌다 — 루트로 중복 제거
  case "$SEEN" in *"|$root|"*) continue ;; esac
  SEEN="$SEEN|$root|"
  ver=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('version',''))" "$m" 2>/dev/null)
  echo "PLUGIN $name $ver $root"
  find "$root/skills" -maxdepth 2 -name SKILL.md 2>/dev/null
done
# Codex 커스텀 에이전트(.codex/agents/*.toml)도 인벤토리에 포함
for f in ./.codex/agents/*.toml ~/.codex/agents/*.toml; do [ -f "$f" ] && basename "$f" .toml; done 2>/dev/null
```

**[HARD] 0개는 실패다.** 위 스캔이 플러그인 0개를 반환했는데 사용자가 설치했다고 말하거나 세션 스킬 목록에 `moai-*`가 보이면, **빈 인벤토리로 진행하지 않는다.** 경로 구조가 또 바뀐 것이므로 그 사실을 보고하고 소스 B(세션 스킬 목록)로 대체한다.

각 SKILL.md frontmatter의 `name:` 필드를 추출해 `<skill-name> → <plugin>` 매핑을 구성한다.

**소스 B — system reminder 파싱**: 현재 세션 system reminder의 "user-invocable skills" 목록에서 moai-cowork 출처 `moai-*` 스킬만 등록한다.

**교차 검증**: 두 소스가 일치하면 신뢰도 HIGH. 한쪽에만 있으면 MEDIUM(설치는 됐으나 세션 미반영 등).

### 2-2. `.moai/config.json` 인벤토리 스냅샷 스키마

**[HARD] 아래 네 필드는 없으면 후속 기능이 통째로 죽는다.** `plugins_installed`의 **버전**과 `skills_available`의 **digest**가 없으면 `update`가 "변경된 스킬"을 영영 검출하지 못하고, `template_version`·`hard_block_digests`가 없으면 HARD 블록 재동기화가 사용자 편집과 구 템플릿을 구분하지 못한다(`update-protocol.md` §4-1). `sensitivity`가 없으면 맞춤법 단계가 fail-open 된다. `coverage`가 없으면 재개(resume) 시 이미 답한 축을 **다시 묻게 된다** — 커버리지 표(SKILL.md §Socratic Interview)의 24축 상태를 그대로 저장한다.

```json
{
  "scanned_at": "2026-07-11T00:00:00+09:00",
  "plugins_installed": { "moai-pm": "1.5.0", "moai-coworker": "1.2.0" },
  "skills_available": {
    "content-blog": { "plugin": "moai-coworker", "digest": "sha256:..." },
    "ai-slop-reviewer": { "plugin": "moai-coworker", "digest": "sha256:..." }
  },
  "template_version": "1.5.0",
  "hard_block_digests": { "6. 한국어 품질 체인 (HARD)": "sha256:...", "...": "..." },
  "sensitivity": "public | sensitive | unknown",
  "coverage": {
    "A": { "1": "충족", "2": "충족", "3": "유예" },
    "H": { "22": "충족", "23": "미확인", "24": "유예" }
  },
  "confidence": { "moai-pm": "HIGH" }
}
```

### 2-3. Phase 1 답변 기반 매칭

| 업무 유형 | 우선 코워커(플러그인) |
|----------|------------|
| 사업 기획·전략 | 코워커(business-* 스킬군) |
| 콘텐츠 제작 | 마케터(content-*, marketing-* 스킬군) |
| 문서·행정 | 사무관(office-*), 법무(legal-*) |
| 제품·연구 | 코워커(spec/ux 스킬군), 튜터(education-* 스킬군) |
| 이커머스 | 셀러(commerce-* 스킬군) |
| 출판·원고·웹툰·IP | 작가(book-*), 스토리(story-*) |
| 디자인 핸드오프·브랜드 | 디자이너(cd-*, moai-domain-design 스킬군) |

라우터 허브는 project 스킬(`/project` 진입). 실무/콘텐츠/사무 도메인은 코워커로 수렴하며, 스토리는 `moai-story`, 출판은 `moai-writer`, 디자인은 `moai-designer`로 분기된다. `moai-coworker:ai-slop-reviewer`·`moai-writer:korean-humanize`은 `moai-coworker` 소속으로 텍스트 후처리 체인에 항상 활용 가능하다.

---

## Phase 3: 스킬 체인 설계 (핵심)

### 3-1. 체인 구성 규칙

```
[기획/분석 스킬] → [생성 스킬] → [포맷 변환/미디어 스킬] → ⟨한국어 감사 3단⟩
```

한국어 텍스트 산출물 체인은 **반드시 ⟨한국어 감사 3단⟩(`moai-coworker:ai-slop-reviewer` → `moai-writer:korean-spell-check` → `moai-writer:korean-humanize`)으로 종료**한다 — 정본은 `cowork-setup.md` §3이며 `korean-humanize`가 마지막이어야 한다(Phase 6 최종 검수가 판정한 산출물이 그대로 전달되도록). 비텍스트는 감사 단계 생략. Inventory에 없는 스킬은 체인에서 제외하거나 Gap Detection으로 넘긴다.

### 3-2. 체인 프리셋 테이블

상세 체인 프리셋(주요 산출물별 권장 체인)은 `cowork-setup.md` §3을 참조한다(단일 소스 — 중복 유지 안 함).

### 3-3. 체인 요약 포맷

Phase 5(확인 단계)에서 사용자에게 보여줄 요약:

```
이 프로젝트의 실행 체인 설계

[주 산출물 1] 사업계획서(PPT)
  체인: consult-strategy → doc-pptx → ⟨한국어 감사 3단⟩
  트리거 예시: "사업계획서 만들어줘"
```

---

## Phase 4: Gap Detection — 누락 플러그인/스킬 감지

### 4-1. 누락 감지 알고리즘

```
for each skill in chain_skills:
    if skill not in inventory.skills_available:
        missing_skills.append(skill)
        missing_plugin = SKILL_PLUGIN_MAP[skill]
        missing_plugins.add(missing_plugin)
```

### 4-2. 스킬 → 플러그인 매핑

스킬군 → 소속 플러그인 매핑은 **`.claude-plugin/marketplace.json` 로스터를 정본으로 삼는다** — 하드코딩 매핑 테이블을 유지하지 않는다(신규 플러그인 추가 시 자동 반영). 참고 패턴: `business-*`/`content-*`/`marketing-*`/`office-*`/`legal-*`/`finance-*`/`education-*`/`media-*`/`general-*` → `moai-coworker`; `commerce-*` → `moai-seller`; `book-*` → `moai-writer`; `story-*` → `moai-story`; `cd-*`/디자인 도메인 → `moai-designer`; 개발 도메인 스킬 → `moai`; `project`(PM 허브) → `moai-pm`.

### 4-3. 누락 발견 시 AskUserQuestion 4 옵션

```
"체인에 필요한 스킬이 설치되지 않은 플러그인에 포함돼 있습니다."

누락 스킬: [skill-A] → [moai-X] 플러그인 필요

옵션:
  1. (권장) 설치 안내 받기 + 설치 후 재개
     → 설치 명령을 안내하고, 완료 후 "이어서 진행"으로 재개합니다.
     → 현재 진행 상태(.moai/cache/init-progress.json)는 보존됩니다.
  2. 누락 스킬 제외하고 진행
  3. 대체 스킬로 변경
  4. 중단
```

### 4-4. 옵션 1 선택 시: 설치 안내 흐름

```
1. 누락 플러그인별 설치 안내 (데스크톱 앱 — /plugin 슬래시 명령은 Claude Code 전용이라 안내하지 않음):
   - 앱 UI: Plugins 메뉴 → 해당 플러그인 Install
   - 터미널: claude plugin install <플러그인>@moai-cowork (Claude Cowork) / codex plugin add <플러그인>@moai-cowork (ChatGPT Work)
   (최초 1회 마켓 등록: Marketplace에서 modu-ai/moai-cowork 추가, 또는 claude/codex plugin marketplace add modu-ai/moai-cowork)

2. .moai/cache/init-progress.json 저장

3. 안내: "'이어서 진행' 또는 '설치 완료' 발화"
```

`.moai/cache/` 디렉터리가 없으면 `Bash("mkdir -p .moai/cache")`로 생성한다.

### 4-5. `init-progress.json` 스키마

```json
{
  "started_at": "2026-07-11T14:30:00+09:00",
  "phase_completed": 3,
  "interview_answers": { "work_type": ["사업 기획·전략"] },
  "chain_design": [
    { "deliverable": "사업계획서(PPT)", "chain": ["consult-strategy", "doc-pptx", "ai-slop-reviewer", "korean-spell-check", "korean-humanize"] }
  ],
  "missing_skills": [],
  "missing_plugins": []
}
```

### 4-6. 옵션 2/3 선택 시

옵션 2(제외): `missing_skills`에 해당하는 체인 단계를 제거하고 Phase 5로 진행하며, `AGENTS.md`의 해당 체인에 미설치 주석을 삽입한다. 옵션 3(대체): `inventory.skills_available`에서 유사 기능 스킬을 검색해 재설계 후 Phase 5로 진행한다.

### 4-7. 누락 0건이면

즉시 Phase 5 Confirm으로 진행한다.

---

## Phase 5: 설계 확인

`AskUserQuestion`(1질문, 3옵션): 승인(권장) / 수정 / 취소.

---

## Phase 6: 지침 생성 (AGENTS.md 정본 + CLAUDE.md 포인터)

`references/templates/AGENTS.md.tmpl`을 로드하여 변수를 치환하고 `./AGENTS.md`에 쓴다. 이어서 `references/templates/CLAUDE.md.tmpl`을 **치환 없이 그대로** `./CLAUDE.md`에 복사해 `@AGENTS.md` 포인터를 만든다(본문 복제 금지). 상세 변수 치환 테이블·생성 절차·포인터 규칙은 `agentsmd-generator.md` 참조. 생성 원칙: AGENTS.md ≤500라인, 스킬 체인 최대 10개, 8개 HARD 규칙 블록 항상 포함, UTF-8/LF/한국어.

---

## Phase 7: 커스텀 에이전트 생성

Phase 3-6 결과를 바탕으로 커스텀 에이전트를 **Claude용 `.claude/agents/*.md`(markdown+YAML frontmatter)와 Codex용 `.codex/agents/*.toml`(TOML: `name`·`description`·`developer_instructions`, `model`·`sandbox_mode` 선택) 양쪽**으로 생성한다. 절차·frontmatter·7-step 루프는 project 스킬 SKILL.md §Custom Agent & Skill-Chain Design 참조.

---

## Phase 8: API 키 / 커넥터 + 첫 실행 안내

Phase 2에서 선택된 플러그인이 API 키를 요구하면 등록 안내.

| # | 서비스 | 환경변수 | 용도 | 발급처 |
|---|--------|---------|------|--------|
| 1 | 공공데이터포털 | `DATA_GO_KR_API_KEY` | 공공데이터/KOSIS/KCI | data.go.kr |
| 2 | KIPRIS Plus | `KIPRIS_API_KEY` | 특허 검색 | plus.kipris.or.kr |
| 3 | 국가법령정보 | `KOREAN_LAW_OC` | 법령/판례 | law.go.kr |
| 4 | Google Gemini | `GEMINI_API_KEY` | 이미지 프롬프트 | ai.google.dev |
| 5 | Higgsfield | `HIGGSFIELD_API_KEY` + `HIGGSFIELD_SECRET` | Higgsfield MCP | higgsfield.ai |
| 6 | ElevenLabs | `ELEVENLABS_API_KEY` | media-audio-gen(TTS) | elevenlabs.io |

저장 위치: `./.moai/credentials.env`(프로젝트 격리, GUIDANCE 전용 — 실제 값은 절대 기록하지 않음).

첫 실행 안내는 Phase 3에서 설계된 체인 중 상위 3개를 예시로 제시한다. 전체 코워커 목록이 궁금하면 "어떤 코워커 있어?", 현재 상태는 "지금 상태 어때?"로 물으면 안내한다.

---

## Re-entry: 설치 완료 후 진행 재개

| 트리거 | 처리 |
|--------|------|
| "이어서 진행" / "설치 완료" / "다시 진행" | 자연어 → resume 흐름 자동 트리거(유일한 재개 경로) |

### 복원 흐름

1. `.moai/cache/init-progress.json` 존재 확인(없으면 "저장된 진행 상태가 없습니다. `/project`로 새로 시작하세요.")
2. `init-progress.json` 로드(Phase 1-3 결과 복원)
3. Phase 2 Inventory 재실행(설치 확인)
4. Phase 4 Gap Detection 재검증(여전히 누락 시 4옵션 재제시, 0건이면 Phase 5로 진행)
5. Phase 5 이후는 정상 흐름과 동일

---

## API 키 관리 — "API 키 설정할래" (자연어)

사용자가 "API 키 설정할래"·"키 등록할래"라고 하면 Phase 8 안내 흐름이 6개 API 키를 조회·변경·추가·삭제한다.

---

## AskUserQuestion 제약 준수 요약

**[HARD] 호출 수가 아니라 라운드 수를 센다.** 한 라운드는 질문 여러 개를 묶은 **1회 호출**이다. 질문 1개당 1회 호출하는 분할 방식은 금지한다.

| Phase | 호출 | 한 호출에 담는 질문 수 | 옵션 수 |
|-------|------|------------------------|---------|
| Phase 1 · S1 일괄 진단 | 1 | **최대 4 (묶음 배치)** | 각 ≤4 (+Other) |
| Phase 1 · 후속 라운드(커버리지 미충족 시) | 0-N (상한 없음) | 미확인 축을 정보 이득 순 최대 4 | 각 ≤4 (+Other) |
| Phase 4 Gap Detection(조건부) | 0-1 | 1 | 4 |
| Phase 5 설계 확인 | 1 | 1 | 3 |
| Phase 8 API 키(조건부) | 0-1 | 1-2 | 최대 4(multiSelect) |

- 정상 경로(맥락 충분): **총 2회 호출** — S1 + Phase 5 확인.
- 최대 경로: S1 + S2 반복 + Gap + 확인 + API 키. S2 반복이 2회를 넘으면 종료 선택지를 함께 제시한다.
- 모든 질문은 `AskUserQuestion` 채널만 사용한다. 자유 서술 질문·텍스트 대화형 심화 인터뷰는 사용하지 않는다(`Other` 옵션이 자유입력을 흡수한다).
