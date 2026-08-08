# 모두의 코워크 (MoAI-Cowork) — 한국 실무 AI 직원 패밀리

> **비개발자도 한마디면 시작.** Claude Cowork와 ChatGPT Work 양쪽에서 쓰는, 한국 실무에 맞춘 AI 직원(전문가) 패밀리입니다.

PM이 프로젝트 성격을 파악해 알맞은 직원을 배치하고, 나머지 직원들이 각자의 전문 영역(마케팅·콘텐츠·미디어·커머스·법무·재무·HR·CS·디자인 등)에서 실무를 지원합니다. 설치는 마켓플레이스 한 번 등록으로 끝나고, 이후에는 자연어 한 줄만 던지면 됩니다.

- **두 데스크톱 앱 지원** — Claude Cowork와 ChatGPT Work(Codex) 양쪽 매니페스트(`.claude-plugin` / `.codex-plugin`)를 함께 제공합니다. 평소 쓰는 쪽에 설치하세요.
- **한국 실무 설계** — 한국어 문서·말투·업무 규격(한글·HWPX·스마트스토어·공공데이터 등)에 맞췄습니다.
- **슬래시 명령 없이 자연어** — "사업계획서 써줘"처럼 하려는 일을 말하면 알맞은 스킬이 자동으로 매칭됩니다.
- **결과물은 여러분 것** — 상업적 사용 제한 없음. [LICENSE-OUTPUT.md](./LICENSE-OUTPUT.md)

---

## MoAI-Cowork가 무엇인가요?

MoAI-Cowork(모두의 코워크)는 **비개발자도 AI와 함께 실무를 풀 수 있게 만든 AI 직원 패밀리**입니다.

"AI 직원"은 한 가지 일에 깊이 특화된 전문가 AI입니다. 거대한 AI 하나가 모든 걸 다루는 게 아니라, 마케터·작가·셀러·법무 담당·디자이너처럼 **직무별로 나뉜 전문가 AI**가 각자의 영역을 맡습니다. 마치 회사에 부서가 있고 부서마다 담당자가 있는 것과 같습니다.

### 왜 만들었나요?

AI 도구는 강력하지만 "어떻게 시작하지?"에서 막히는 분이 많습니다.

- 영문 메뉴와 개발자 중심 인터페이스가 익숙하지 않은 분
- "뭘 입력해야 할지"를 매번 고민하게 되는 분
- 한국 실무 맥락(한글 문서, 스마트스토어, 공공데이터, 한국어 말투)을 잘 다루는 도구를 찾는 분

MoAI-Cowork는 이 분들이 "**하고 싶은 일만 말하면 시작**" 할 수 있도록 만들었습니다. 시작은 PM 직원이 인터뷰로 안내하고, 그 뒤로는 자연어 한 줄로 실무가 굴러갑니다.

### 핵심 특징

| 특징 | 설명 |
|------|------|
| **직무별 전문가 AI** | 코워커(범용)·작가·마케터·미디어·셀러·법무·재무·디자이너 등 각자의 영역을 맡은 직원 패밀리 |
| **PM 허브가 진입 안내** | `/project` 한 명령으로 프로젝트 성격을 파악하고 알맞은 직원을 배치 |
| **두 데스크톱 앱** | Claude Cowork와 ChatGPT Work 양쪽에서 동일한 직원을 사용 |
| **자연어 단일 진입** | 스킬 이름을 외울 필요 없이, 하려는 일을 말하면 자동 매칭 |
| **한국 실무 정합** | 한국어 경어체, 한글 오피스 문서, 스마트스토어·공공데이터 등 국내 실무 규격 대응 |

---

## 어떻게 동작하나요?

처음 한 번은 PM 직원이 프로젝트를 준비하고, 그 뒤로는 자연어 한 줄로 일합니다.

### ① 최초 1회 — PM이 프로젝트를 준비합니다

`/project`를 실행하면 PM이 목적과 산출물을 **인터뷰**로 묻습니다. 그 답에서 필요한 일을 **감지**해 알맞은 직원과 스킬을 순서대로 이은 **체인**으로 조립합니다. 확인을 받으면 프로젝트 규칙 파일을 생성합니다.

```
/project (최초 1회)
      │
      ▼
  PM이 인터뷰 ──▶ 필요한 일 감지 ──▶ 스킬 체인 조립 ──▶ 확인
      │
      ▼
  규칙 파일 생성: CLAUDE.md (Claude Cowork) / AGENTS.md (ChatGPT Work)
      │  + 커스텀 에이전트·스킬 체인 설계
      ▼
  (필요 시) 외부 서비스 API 키 안내
```

이 단계가 끝나면 "어떤 일을, 어떤 순서로, 어떤 품질 기준으로 만들지"가 한 번에 정리됩니다.

### ② 이후 매번 — 한 줄만 던지면 됩니다

준비가 끝나면 스킬 이름을 몰라도 됩니다. 한 줄을 쓰면 맥락을 읽고 알맞은 스킬들이 자동으로 연쇄 실행됩니다.

```
"IR 덱 만들어줘"  ──▶  ① 도메인 스킬(내용 생성)
                         │
                         ▼
                      ② 포맷 스킬(PPTX로 변환)
                         │
                         ▼
                      ③ 품질 스킬(AI 특유 어투 솎아내기)
                         │
                         ▼
                      완성된 PPTX
```

> PM은 직접 일하지 않습니다. **누가 이 일에 맞는지 찾아 팀을 꾸리는 안내자** 역할만 합니다.

---

## AI 직원 명단

전부 `modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. 정확한 최신 로스터는 [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)이 정본이고, 아래는 역할 요약입니다.

| 직무 | 플러그인 | 역할 |
|---|---|---|
| 🚀 **PM (진입 허브)** | `moai-pm` | `/project` 라우터 — 프로젝트 성격 파악 → 알맞은 직원 배치 |
| 🧑‍💼 코워커 | `moai-coworker` | 범용 실무·라이프스타일 (협업·생산성·개인 일정) |
| ✍️ 작가 | `moai-writer` | 출판 기획·집필·한글 윤문·맞춤법 |
| 📖 스토리 크리에이터 | `moai-story` | 웹툰·웹소설·IP·스토리보드 |
| 📣 마케터 | `moai-marketer` | 캠페인·콘텐츠·광고·SEO·메타광고 |
| 🎬 미디어 크리에이터 | `moai-media` | 이미지·영상·오디오 생성 (Higgsfield·Midjourney·Gemini 등) |
| 🛒 셀러 | `moai-seller` | 커머스 운영 (스마트스토어·쿠팡·D2C·상세페이지·광고) |
| 📄 사무관 | `moai-officer` | 오피스 문서 (한글·워드·엑셀·PPT·PDF·노션) |
| 📊 데이터 애널리스트 | `moai-analyst` | 공공데이터·실거래가·경매·주식·통계 조회·시각화 |
| ⚖️ 법무 담당 | `moai-lawyer` | 계약 검토·컴플라이언스·특허·부동산 실명 |
| 💰 재무·세무 담당 | `moai-accountant` | 재무제표·세무·투자·보험·예산 |
| 🤝 인사·채용 담당 | `moai-recruiter` | 채용·이력서 검토·성과평가·인사 운영 |
| 🎧 CS매니저 | `moai-cs` | 고객응대·VOC·채널 메시지·티켓 분류 |
| 💼 컨설턴트 | `moai-consultant` | 전략·시장분석·정부지원금·스비즈365 |
| 🧭 커리어코치 | `moai-career` | 이력서·면접·포트폴리오·커리어 전환 |
| 🎓 튜터 | `moai-tutor` | 학습 자료·평가·논문·교육과정 |
| 🎨 디자이너 | `moai-designer` | 브랜드·로고·디자인 시스템·Claude Design 연동 |
| 📸 SNS 크리에이터 | `moai-threads-poster` | 소셜 발행 (Threads·Instagram) |

직원별 상세 소개는 [AI 직원](https://cowork.mo.ai.kr/moai-agents/)에서 볼 수 있습니다.

---

## 시작하기 — 두 데스크톱 앱에서 설치

두 데스크톱 앱 **Claude Cowork**와 **ChatGPT Work** 중 평소 쓰는 쪽에 설치합니다. 두 앱 모두 같은 마켓플레이스 주소 `modu-ai/moai-cowork`를 사용합니다.

### 1. 마켓플레이스 등록 (최초 1회)

마켓플레이스 주소를 추가합니다. (마켓플레이스 = "설치할 수 있는 앱 목록이 모여 있는 곳", 앱 스토어처럼 생각하시면 됩니다.)

<!-- ▼ 이미지 삽입 자리 — 마켓플레이스 등록 화면. 링크를 주시면 아래 줄의 TODO를 실제 이미지로 교체합니다. -->
<!-- ![마켓플레이스 등록 화면](TODO-사용자-제공-이미지-링크) -->

```bash
# Claude Cowork 또는 ChatGPT Work 앱 안에서
/plugin marketplace add modu-ai/moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/) 1절에 정리해 두었습니다. 동기화가 끝나면 직원 목록이 표시됩니다.

### 2. 플러그인 설치

**가장 쉬운 방법** — `/plugin`이라고 치면 나오는 창에서 "**Browse Plugins**"을 누르고 원하는 직원을 선택하세요.

<!-- ▼ 이미지 삽입 자리 — 플러그인 설치 화면. 링크를 주시면 아래 줄의 TODO를 실제 이미지로 교체합니다. -->
<!-- ![플러그인 설치 화면](TODO-사용자-제공-이미지-링크) -->

**명령으로 직접 설치**하려면:

```bash
/plugin install moai-pm@moai-cowork            # PM 허브 (먼저 설치 — 필수)
/plugin install moai-coworker@moai-cowork       # 범용 실무 코어 (권장)
```

필요한 전문가 직원을 추가로 설치합니다:

```bash
# 예: 마케팅·콘텐츠 작업
/plugin install moai-marketer@moai-cowork
/plugin install moai-media@moai-cowork

# 예: 법무·문서 작업
/plugin install moai-lawyer@moai-cowork
/plugin install moai-officer@moai-cowork
```

> 처음엔 **PM + 코워커**만 설치해도 충분합니다. 나중에 다른 직원이 필요해지면 셋업 중 자동으로 감지해 설치를 안내합니다.

### 3. 프로젝트 시작

작업 폴더를 연결한 프로젝트를 만들고, 대화창에 `/project`를 입력합니다. PM이 인사하며 무엇을 할지 묻습니다.

```
/project
```

"온라인 클래스 런칭 준비할 거야"처럼 답하면, PM이 프로젝트 전용 커스텀 에이전트와 스킬 체인을 설계해 `CLAUDE.md`(Claude Cowork) 또는 `AGENTS.md`(ChatGPT Work)를 생성합니다. 이후에는 자연어 한 줄로 실무가 굴러갑니다.

단계별 전체 가이드는 [빠른 시작](https://cowork.mo.ai.kr/getting-started/quick-start/)을 보세요.

---

## 문서 사이트 — 4트랙 구조

문서 사이트 [cowork.mo.ai.kr](https://cowork.mo.ai.kr)는 비개발자(10~60대)를 위한 한국어 Claude Cowork·ChatGPT Work 실무 가이드입니다. 학습 난이도 순서대로 3개 트랙을 제공하며, 각 트랙은 Anthropic 공식 자료(support.claude.com / docs.claude.com)를 따릅니다.

| 트랙 | 제품 | 학습 범위 | 가이드 |
|------|------|-----------|------|
| **Chat** | Claude Desktop App | 첫 대화·프롬프트·아티팩트·프로젝트·웹검색·리서치·확장사고·메모리·스킬·커넥터 | [Chat 트랙](https://cowork.mo.ai.kr/guide/chat/) |
| **Cowork** | Claude Cowork | 비개발자 실무를 위한 자율 실행 데스크톱 앱 — 자율 실행·프로젝트·스킬·플러그인·디스패치·컴퓨터사용·아키텍처 | [Cowork 트랙](https://cowork.mo.ai.kr/guide/cowork/) |
| **Design** | Claude Design | 디자인 시스템·컴포넌트·토큰·핸드오프 (Anthropic Labs 제품) | [Design 트랙](https://cowork.mo.ai.kr/guide/design/) |

### 문서 사이트 섹션

| 섹션 | 내용 | 링크 |
|------|------|------|
| **시작하기** | 첫 설치·등록·빠른 시작 | [getting-started](https://cowork.mo.ai.kr/getting-started/) |
| **가이드** | 4트랙(Chat/Cowork/Design/Code) 학습 경로 | [guide](https://cowork.mo.ai.kr/guide/) |
| **쿡북** | 실전 레시피·워크플로우 예제 | [cookbook](https://cowork.mo.ai.kr/cookbook/) |
| **AI 직원** | AI 직원 상세 소개 | [moai-agents](https://cowork.mo.ai.kr/moai-agents/) |
| **플러그인** | 설치·설정·팀즈·Higgsfield 연동 | [plugins](https://cowork.mo.ai.kr/plugins/) |
| **릴리스** | 버전별 변경 이력 | [releases](https://cowork.mo.ai.kr/releases/) |
| **도움말** | FAQ·트러블슈팅 | [help](https://cowork.mo.ai.kr/help/) |
| **CLI** | `moai` 명령행 도구 | [cli](https://cowork.mo.ai.kr/cli/) |

목차의 진실 출처(SSOT)는 [`www/data/menu/main.yaml`](www/data/menu/main.yaml)입니다.

---

## 자주 묻는 질문(FAQ)

**Q. Claude Cowork와 ChatGPT Work 중 어느 쪽에 설치해야 하나요?**
둘 다 지원합니다. 평소 쓰는 쪽에 설치하세요. 같은 마켓플레이스를 양쪽 매니페스트(`.claude-plugin` / `.codex-plugin`)로 제공하며, 규칙 파일도 각 앱에 맞게(`CLAUDE.md` / `AGENTS.md`) 생성됩니다.

**Q. 두 앱을 동시에 쓸 수 있나요?**
네. 각 앱에서 같은 마켓플레이스 주소 `modu-ai/moai-cowork`를 등록해 쓰시면 됩니다.

**Q. 사용 비용이 드나요?**
플러그인 자체는 무료(Apache-2.0)입니다. Claude·ChatGPT 구독이나 사용량은 각 서비스 정책을 따르고, 일부 직원은 외부 서비스(Higgsfield, ElevenLabs 등) 연동을 위해 API 키가 필요할 수 있습니다.

**Q. 제가 만든 결과물은 누구 것인가요?**
여러분 것입니다. 상업적 사용에 제한이 없습니다 — [LICENSE-OUTPUT.md](./LICENSE-OUTPUT.md).

**Q. 한국어를 잘하나요?**
네. 한국 실무 문서·경어체·업무 규격에 맞춰 설계됐습니다.

**Q. 개발(코딩) 작업도 도와주나요?**
이 마켓플레이스는 비개발 실무 중심입니다. 코딩 작업은 각 데스크톱 앱(Claude Cowork·ChatGPT Work) 자체 기능으로, 개발 환경 셋업은 PM의 개발 모드로 다룹니다.

**Q. 스킬 이름을 외워야 하나요?**
아니요. "사업계획서 써줘"처럼 하려는 일을 말하면 알맞은 스킬이 자동으로 매칭됩니다.

---

## 저장소 구조

```
modu-ai/moai-cowork/
├── .claude-plugin/marketplace.json   # Claude 마켓 매니페스트 (정본 로스터)
├── plugins/                          # 마켓 플러그인 소스 (설치명 = 디렉터리명)
│   ├── moai-pm/                      # 프로젝트 허브 (/project)
│   │   ├── .claude-plugin/           # Claude Cowork 매니페스트
│   │   └── .codex-plugin/            # ChatGPT Work(Codex) 매니페스트
│   ├── moai-coworker/                # 범용 실무
│   ├── moai-designer/                # 디자이너
│   ├── moai-threads-poster/          # 소셜 포스터 (Threads/Instagram)
│   └── ...                           # 전문가·크리에이티브 직원
├── www/                              # 문서 사이트 (cowork.mo.ai.kr, Hugo)
│   ├── content/
│   │   ├── getting-started/          # 시작하기
│   │   ├── guide/                    # 4-트랙 가이드 (chat·cowork·design·code)
│   │   ├── cookbook/                 # 쿡북·실전 트랙
│   │   ├── moai-agents/              # AI 직원 소개
│   │   ├── plugins/                  # 플러그인 설치·설정
│   │   ├── releases/                 # 릴리스 노트
│   │   ├── help/                     # 도움말·FAQ
│   │   └── cli/                      # CLI 도구
│   ├── data/menu/main.yaml           # 목차 SSOT (3축: 데스크탑·CLI·공통하단)
│   └── hugo.toml
├── README.md
└── LICENSE
```

> 이 저장소는 **마켓플레이스 + 문서**만을 다룹니다. MoAI-ADK 개발 환경(에이전트/규칙/스킬 설정 등)은 별도 관리되며 `.gitignore`로 이 저장소에서 제외됩니다.

---

## 라이선스

[Apache License 2.0](./LICENSE) — 상업적 사용·수정·재배포 자유. 저작권 고지와 변경 사항 표시가 필요합니다.

이 플러그인으로 **만든 산출물은 여러분 것**이며 상업적 사용에 제한이 없습니다 — [LICENSE-OUTPUT.md](./LICENSE-OUTPUT.md).
제3자 저작물 고지는 [NOTICE](./NOTICE), 이름·로고 사용 규칙은 [TRADEMARKS.md](./TRADEMARKS.md)를 보세요.
