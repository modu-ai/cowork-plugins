# M3.3 — 비개발자 설치 가이드 (4-plugin 재설계 Phase 3)

## Context

모두의클로드는 goos.kim의 "플러그인 = AI 직원" 발상으로 4개 플러그인(코워커·디자이너·코더·PM)으로 재설계되었습니다. Phase 3의 M3.2(런타임 진입 UX)까지 완료(HEAD `9696a6d`)되었으나, **비개발자가 처음 설치하는 경험**은 아직 다듬어지지 않았습니다.

현재 4개 README의 설치 섹션은 모두 `/plugin install moai-X` 한 줄만 있고, **`/plugin marketplace add modu-ai/claude` 마켓 등록 단계가 누락**되어 있어 비개발자는 첫 단계에서 막힙니다. 또한 텍스트 매체인 README에 시각적 안내(구조도·흐름도)가 전혀 없습니다.

M3.3의 목표: **비개발자가 README만 보고 마켓 등록부터 첫 대화까지 도달할 수 있도록**, PM README에 ASCII 그림 5장 + Claude Desktop 설치 안내를 갖추고, 4개 README의 설치 블록을 동일 패턴으로 통일합니다.

## goos.kim 결정 사항 (4문항 AskUserQuestion 확정)

1. **그림 매체**: ASCII/이모지 아트 (README 코드블록 내장 — TUI·터미널·GitHub 모두 렌더링)
2. **그림 5장 주제**: 제안 세트 — ①4직원 구조도 ②`/project` 라우팅 흐름 ③코워커 두 모자 교체 ④3단 progressive disclosure ⑤설치→첫실행 여정
3. **설치 블록**: "Claude Desktop에서 추가하는 방법 안내" (`/plugin` GUI → Browse Plugins 흐름 + marketplace add)
4. **반영 범위**: PM README 중심(그림 5장 + 상세) + coworker/designer/coder README 설치 블록 통일

**문법 실측 (docs.claude.com/en/docs/claude-code/plugins verified)**: 마켓 등록 `/plugin marketplace add modu-ai/claude`, 직접 설치 `/plugin install <plugin>@<marketplace>`, GUI 진입 `/plugin` → "Browse Plugins". marketplace name = `moai-claude`(`.claude-plugin/marketplace.json` L2).

---

## 산출물 A — PM README (`plugins/moai-pm/README.md`, 현재 132줄)

### A.1 ASCII 그림 5장 (초안 — 승인 후 manager-docs가 정교화)

**그림 1 — 4명 AI 직원 구조도** (현재 "4명의 AI 직원" 표 위에 삽입):
```
                    ┌──────────────┐
                    │  📋 PM 허브   │  /project
                    │  (라우팅만)   │  "무슨 일 할까?"
                    └──────┬───────┘
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │🧑‍💼 코워커   │  │🎨 디자이너  │  │💻  코더     │
   │ 실무 + 작가 │  │ 브랜드 시스템│  │ SPEC 개발   │
   │  192스킬    │  │  11스킬     │  │  28스킬     │
   └─────────────┘  └─────────────┘  └─────────────┘
```

**그림 2 — `/project` 라우팅 흐름** ("사용법" 섹션 상단):
```
   방법 1: 자연어          방법 2: 플래그         방법 3: 메뉴
   /project               /project --cowork      /project
   "사업계획서 만들고 싶어"                        (4직원 중 선택)
                \              |              /
                 \             |             /
                  ┌────────────▼────────────┐
                  │   PM이 가장 맞는 직원 판단 │
                  └────────────┬────────────┘
                               ▼
                    코워커 · 디자이너 · 코더
```

**그림 3 — 코워커 두 모자 자동 교체** ("각 직원이 셋업해 주는 것 > 코워커 분기"):
```
      "사업계획서 써줘"            "웹소설 연재할래"
            │                          │
            ▼                          ▼
    ┌───────────────┐          ┌───────────────┐
    │ 🧑‍💼 실무 동료  │   ⇄⇄⇄   │ ✍️ 글쓰기 작가 │
    │  (모자 ON)    │          │  (모자 ON)    │
    └───────────────┘          └───────────────┘
       말하는 내용이 모자를 자동으로 바꿉니다 (슬래시 명령 불필요)
```

**그림 4 — 3단 progressive disclosure** (새 "## 진입 경험" 섹션, M3.2 런타임 성과 시각화):
```
   L1 (~1줄)          L2 (~2문장)             L3 (전체)
   정체성              자기소개                 스킬 맵
   ─────────         ───────────────         ───────────────
   plugin.json   →    README blockquote   →   SKILL.md 본문
   description        + 진입 응답(런타임)       + references/core/

   "어떤 일 하나요?"   "안녕하세요,             192스킬 전체 지도
                       코워커입니다"
```

**그림 5 — 설치 → 첫 실행 여정** ("설치" 섹션 상단, 설치 블록 바로 위):
```
   ① 마켓 등록(1회)      ② 직원 설치           ③ 첫 대화
   /plugin marketplace   /plugin install       /project
   add modu-ai/claude    moai-coworker@...     "카페 창업 사업계획서..."
         │                     │                      │
         ▼                     ▼                      ▼
      (최초 1회)          (필요한 만큼)         PM이 코워커로 연결
                                                    │
                                                    ▼
                                          "몇 가지만 물어볼게요"
                                          인터뷰 → 체인 → CLAUDE.md
```

### A.2 설치 섹션 재설계 (현재 L22-37 → Claude Desktop GUI 안내)

```
## 설치

### ① 마켓플레이스 등록 (최초 1회만)

모두의클로드 4명의 AI 직원은 `modu-ai/claude` 마켓플레이스 하나에 들어있습니다.
Claude Code(또는 Desktop)에서 한 번만 등록하면 됩니다:

    /plugin marketplace add modu-ai/claude

### ② 플러그인 추가

**가장 쉬운 방법** — `/plugin`이라고 치면 나오는 창에서
**"Browse Plugins"**을 누르고 원하는 직원을 선택하세요.

**직접 명령으로** 설치하려면:

    /plugin install moai-pm@moai-claude            # PM 허브 (필수)
    /plugin install moai-coworker@moai-claude      # 실무·콘텐츠·작가 (대다수)
    /plugin install moai-designer@moai-claude      # 디자인 (필요 시)
    /plugin install moai-coder@moai-claude         # 개발 (필요 시)

> 처음엔 PM + 코워커만 설치해도 충분합니다. 나중에 다른 직원이 필요해지면
> PM이 자동으로 감지하고 "이 직원을 설치해 주세요"라고 안내한 뒤,
> 설치 완료 시 `/project resume`으로 이어서 진행합니다.
```

나머지 PM README 섹션(사용법·각 직원 셋업·자주 쓰는 명령·첫 실행 예시·더 알아보기)은 현행 유지하되, 그림 2/3/4가 자연스럽게 안식처에 삽입되도록 섹션 순서만 미세 조정.

---

## 산출물 B — coworker/designer/coder README 설치 블록 통일

각 README의 "## 설치" 섹션을 동일 패턴으로 교체 (페르소나 blockquote·스킬 표·사용법 등 M3.4 성과는 그대로 보존). `{X}`는 각 직원 이름, `{설명}`은 직원별 한 줄:

```
## 설치

모두의클로드는 `modu-ai/claude` 마켓플레이스 하나에서 4명의 AI 직원을 설치합니다.

**① 마켓 등록 (최초 1회)**

    /plugin marketplace add modu-ai/claude

**② 이 직원 추가**

    /plugin install moai-{X}@moai-claude

또는 `/plugin` 입력 → "Browse Plugins" → moai-{X} 선택.

> {설명 — 예: "코워커 하나로 실무 + 글쓰기 전 영역이 커버됩니다."}
```

대상 3개 파일:
- `plugins/moai-coworker/README.md` (L79-85 교체, `{설명}` = 코워커 하나로 실무+글쓰기 전 영역)
- `plugins/moai-designer/README.md` (L62-68 교체, `{설명}` = 브랜드·디자인 시스템 작업이 필요할 때)
- `plugins/moai-coder/README.md` (L57-63 교체, `{설명}` = 개발 프로젝트를 시작할 때)

---

## 구현 방식

**manager-docs 에이전트 위임** (MoAI Core Rule: 직접 구현 금지, README = manager-docs 영역). 위임 프롬프트에 본 plan의 ASCII 그림 5장 초안 + 통일 설치 블록 패턴을 그대로 제공하여 창작 편차를 최소화. 4개 파일은 독립적이므로 단일 위임으로 순차 처리.

> Multi-File Decomposition(Rule 2): 4개 파일 수정이나 동일 패턴 반복이므로 단일 manager-docs 위임으로 처리, 파일별 진행 보고.

## 커밋 / 병렬 세션 안전

- 병렬 humanize 세션이 working tree 공유 가능 → 수정 전후 persist 재확인 (교훈: parallel-session-stash-race)
- pathspec 커밋 보호: `git add plugins/moai-*/README.md` 만 스테이지
- `--amend` 금지 (HEAD 경쟁 위험 — M3.2 세션 교훈)

## 검증 (verification-claim-integrity 준수 — 관측된 출력만 PASS)

1. 4개 README 설치 섹션에 `marketplace add modu-ai/claude` 포함 — `grep -l 'marketplace add modu-ai/claude' plugins/moai-*/README.md` → 4
2. 4개 README에 `@moai-claude` install 형식 포함 — `grep -l '@moai-claude' plugins/moai-*/README.md` → 4
3. PM README에 ASCII 그림 5개 코드블록 — `grep -c '^```' plugins/moai-pm/README.md` 증가 + 시각 확인
4. stale 재발 없음 — `grep -rE 'moai-cowork[^e]' plugins/ | wc -l` → 1 유지 (CHANGELOG만)
5. M3.4 페르소나 보존 — 각 README blockquote + "다른 AI 직원과 함께 쓰기" 표 유지 확인
6. 상호 링크 정합 — `[moai-pm README](../moai-pm/README.md)` 참조 유효

## Out of scope (별도 후속)

- pm `references/core/` 27-plugin 잔재 정리 (known-debt #1, 별도 SPEC)
- `docs/plugin-family-design/` broken link (known-debt #2, www repo 소관)
- Phase 4 런타임 검증 (`/plugin install` 실동작 + `/project` 플래그 분기 + 코워커 자연어 역할 분기)
