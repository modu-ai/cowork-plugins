# moai-pm (PM) — AI 코워커를 부르는 진입점

> **PM**은 프로젝트를 시작할 때 **어떤 AI 코워커가 필요한지 판단해 팀을 꾸려 주는** 허브 플러그인입니다. 진입점은 단 하나 — `/project` 스킬 하나로 통합되어 있습니다.

---

## `/project` — 단일 진입점

```
/project <자연어 지시>
```

Claude Cowork(Desktop) 프로젝트 초기화 — 소크라테스 인터뷰 → 설치된 AI 코워커 인벤토리 스캔 → **프로젝트 전용 커스텀 에이전트·스킬 체인 설계** → `CLAUDE.md`(≤200라인) + `.claude/agents/` + `.moai/` 스캐폴드 생성 → **사용하면서 재귀적 자가 개선**

```
                        ┌───────────────────────┐
                        │  이번에 뭘 할 건가요?   │
                        └───────────┬───────────┘
                                    ▼
                          /project <지시>
                                    ▼
                     ┌──────────────────────────┐
                     │ 🪿 Cowork 셋업            │
                     │ 모든 Claude Cowork        │
                     │ (Desktop) 업무 — 지침 +   │
                     │ 커스텀 에이전트 +         │
                     │ 재귀적 자가 개선          │
                     └──────────────────────────┘
```

> **범위 주의**: 이 마켓플레이스는 비개발 AI 코워커 전용입니다. 개발-프로젝트 초기화(SPEC·DDD/TDD·품질 게이트)는 범위 밖입니다.

---

## AI 코워커 ('MoAI-Cowork, 모두의 코워크')

전부 `modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. 정확한 로스터·스킬 수는 마켓플레이스 카탈로그(`.claude-plugin/marketplace.json`)가 정본입니다 — 아래는 역할 요약입니다.

| AI 코워커 | 플러그인 | 무엇을 하나요 |
|---------|---------|---------------|
| 🧑‍💼 코워커 | `moai-coworker` | 범용 비즈니스 실무 + 라이프스타일 |
| ✍️ 작가 | `moai-writer` | 출판 기획·집필(book-*) |
| 🎬 스토리 크리에이터 | `moai-story` | 웹툰·웹소설·시나리오·IP(story-*) |
| 📣 마케터 | `moai-marketer` | 캠페인·콘텐츠 |
| 🎨 미디어 크리에이터 | `moai-media` | 이미지·영상·오디오 생성 |
| 🛒 셀러 | `moai-seller` | 이커머스(스마트스토어·아임웹·카페24 MCP) |
| 🗂️ 사무관 | `moai-officer` | 오피스 문서 |
| 📊 데이터 애널리스트 | `moai-analyst` | 공공데이터·데이터 시각화 |
| ⚖️ 법무 담당 | `moai-lawyer` | 계약·법령·판례·특허 |
| 💰 재무·세무 담당 | `moai-accountant` | 재무제표·결산·세금 |
| 🤝 인사·채용 담당 | `moai-recruiter` | 채용·이력서·면접·평가 |
| 🎧 CS매니저 | `moai-cs` | 고객지원·CRM·VOC 분석 |
| 🧭 컨설턴트 | `moai-consultant` | 사업계획·시장분석·경영 진단 |
| 🎯 커리어코치 | `moai-career` | 이력서·면접·이직(구직자 편) |
| 🎓 튜터 | `moai-tutor` | 커리큘럼·평가·논문 |
| 🎨 디자이너 | `moai-designer` | 브랜드·디자인 시스템·Claude Design |
| 📸 SNS 크리에이터 | `moai-threads-poster` | Threads·Instagram 자율 발행 |
| 📋 PM | `moai-pm`(본 플러그인) | `/project` 단일 진입점 제공 |

PM은 직접 일하지 않습니다. **누가 이 일에 맞는지 찾아 팀을 꾸리는 안내자** 역할만 합니다.

---

## 설치

### ① 마켓플레이스 등록 (최초 1회만)

'MoAI-Cowork, 모두의 코워크' AI 코워커는 `modu-ai/moai-cowork` 마켓플레이스 하나에 들어있습니다:

    /plugin marketplace add modu-ai/moai-cowork

### ② 플러그인 추가

**가장 쉬운 방법** — `/plugin`이라고 치면 나오는 창에서 **"Browse Plugins"**을 누르고 원하는 직원을 선택하세요.

**직접 명령으로** 설치하려면:

    /plugin install moai-pm@moai-cowork            # PM 허브 (필수)
    /plugin install moai-coworker@moai-cowork       # 범용 실무 코어 (권장)
    # 필요한 전문가 직원 추가: moai-writer / moai-story / moai-marketer / moai-media /
    # moai-seller / moai-officer / moai-analyst / moai-lawyer / moai-accountant /
    # moai-recruiter / moai-cs / moai-consultant / moai-career / moai-tutor /
    # moai-designer / moai-threads-poster

> 처음엔 PM + 코워커만 설치해도 충분합니다. 나중에 다른 직원이 필요해지면 셋업 중 **Gap Detection**이 감지해 설치를 안내한 뒤, 완료되면 "이어서 진행"이라고 말해 이어서 진행합니다.

---

## 사용법

```
/project
```

PM이 먼저 인사하고 무엇을 할지 묻습니다. "온라인 클래스 런칭 준비할 거야"처럼 답하면 프로젝트 전용 커스텀 에이전트와 스킬 체인을 설계해 `CLAUDE.md`를 생성합니다.

### 서브커맨드

`/project`는 자연어 단일 진입 스킬입니다. 기본 동작은 `<자연어 지시>`로 진입하는 것이고, 아래 3가지 액션만 명시적 서브커맨드로 씁니다. 그 외(재개·카탈로그·상태·API 키)는 자연어로 요청하면 알아서 라우팅합니다.

| 커맨드 | 동작 |
|--------|------|
| `/project <지시>` | 진입 — 인터뷰 후 에이전트/체인 설계 + 생성. **기본 동작.** |
| `/project update` | 플러그인 업데이트 후 전수조사 → CLAUDE.md·에이전트 재동기화 |
| `/project evolve` | 재귀적 자가 개선 수동 발동 |
| `/project doctor` | 환경 진단 |

### 재귀적 자가 개선

셋업이 끝난 뒤에도 PM의 역할은 끝나지 않습니다. 사용 중 아래 신호가 감지되면 에이전트와 `CLAUDE.md`를 **자율적으로 개선**합니다:

- 같은 유형의 수정 요청이 2회 이상 반복될 때(톤·형식 불일치)
- 스킬 체인이 반복적으로 같은 단계에서 실패·우회할 때
- 플러그인 설치·제거로 인벤토리가 실제와 어긋날 때(inventory drift)
- 사용자가 직접 요청할 때(`/project evolve`)

개선은 최소 diff(최대 3개 파일) 단위로만 이루어지고, 변경 요지를 1-3줄로 보고한 뒤 적용하며, 이력은 `CLAUDE.md` 말미 `<!-- evolution-log -->`에 기록됩니다. 자가 개선은 `CLAUDE.md`와 `.claude/agents/`만 수정합니다.

---

## 산출물

| 파일 | 내용 |
|------|------|
| `./CLAUDE.md` | 프로젝트 지침(≤200라인) — 워크플로우 표 + 8개 HARD 규칙 + evolution-log |
| `./.claude/agents/*.md` | 프로젝트 전용 커스텀 에이전트(자가 개선 대상) |
| `./.moai/config.json` | 플러그인·커넥터·API 키 참조 |
| `./.moai/credentials.env` | API 키 안내(프로젝트 격리, GUIDANCE 전용 — 실제 값은 기록하지 않음) |

---

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
