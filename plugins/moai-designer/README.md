# moai-designer (디자이너) — 흩어진 브랜드를 Claude Design으로 합성하는 동료

> **디자이너**는 로고·색·타이포 같은 흩어진 브랜드 자산을 모아 Claude Design에 올릴 **DESIGN.md**로 합성하고, 코드 기반 브랜드 디자인과 Claude Design 시안 핸드오프까지 처리하는 동료입니다.

---

## 무엇을 하나요 (14스킬)

| 역할 | 언제 | 무엇을 하나요 |
|------|------|---------------|
| 🎨 **브랜드 시스템 합성** | 브랜드 자산(로고·색·타이포·기존 사이트·PPT)이 흩어져 있을 때 | 자산 수집 → Claude Design용 **DESIGN.md** + 디자인 토큰(DTCG) 생성 |
| 📥 **Claude Design 핸드오프** | claude.ai/design에서 만든 시안을 코드로 받을 때 | 핸드오프 번들(.zip·URL) 분석 → 토큰·컴포넌트 추출 |
| ✍️ **디자인 카피 검수** | 랜딩 페이지·카드뉴스 카피의 AI 맛을 뺄 때 | AI 슬롭 감사 → 검수 보고서 + 자연스러운 대안 |
| 🛠️ **코드 기반 브랜드 디자인** | 브랜드 컨텍스트에서 카피+비주얼 토큰을 코드로 만들 때 | 카피·비주얼 토큰 병렬 생성 → GAN 품질 루프 |
| 🖼️ **브랜드 정합 비주얼 생성** | 히어로·OG·목업·마스코트 이미지가 필요할 때 | 디자인 토큰을 읽어 제약으로 변환 → Higgsfield 생성 위임 → 정합 검증 |

> 실무 문서·카피·글쓰기는 **코워커**가 담당합니다.

---

## 사용법

### 그냥 말걸기

```
"우리 브랜드 자산 정리해서 Claude Design에 올릴 수 있게 만들어줘"
→ 브랜드 자산 수집 → DESIGN.md + 디자인 토큰 합성

"claude.ai/design에서 만든 시안 핸드오프 받아줘"
→ 핸드오프 번들 분석 → 토큰·컴포넌트 추출

"랜딩 페이지 카피 AI 맛 좀 빼줘"
→ 디자인 카피 AI 슬롭 감사 → 자연스러운 대안
```

### `/design` 명령 (6개)

| 명령 | 무슨 일 |
|------|--------|
| `/design` | 브리프부터 핸드오프까지 (Path A/B 자동 선택) |
| `/design:brief` | 6요소 브리프(Project·Audience·Pages·Tone·Reference·Constraints) |
| `/design:tokens` | 브랜드 자산 → DESIGN.md + DTCG 토큰(색·타이포·spacing·radii·shadows) |
| `/design:import` | Claude Design 핸드오프 번들(.zip·URL) import·분석 |
| `/design:check` | 디자인 카피 AI 슬롭 감사 → 검수 보고서 + 대안 |
| `/design:system` | 75종 브랜드 디자인 시스템 라이브러리 + Tailwind CDN 매핑 |

---

## 프로젝트 시작하기

처음 브랜드 컨텍스트를 셋업할 때는 **PM** 플러그인의 `/project --designer`가 안내합니다.

```
/project --designer
"러닝 브랜드라 색상·타이포 정리하고 싶어"
→ PM이 디자이너 브랜드 셋업으로 연결
```

자세한 건 [moai-pm README](../moai-pm/README.md)를 참고하세요.

---

## 설치

모두의 코워크는 `modu-ai/moai-cowork` 마켓플레이스 하나에서 4명의 AI 직원을 설치합니다.

**① 마켓 등록 (최초 1회)**

    /plugin marketplace add modu-ai/moai-cowork

**② 이 직원 추가**

    /plugin install moai-designer@moai-cowork

또는 `/plugin` 입력 → **"Browse Plugins"** → moai-designer 선택.

> 브랜드·디자인 시스템 작업이 필요할 때 설치하세요.

---

## 다른 AI 직원과 함께 쓰기

디자이너는 4명의 AI 직원 중 한 명입니다.

| AI 직원 | 언제 |
|---------|------|
| 🧑‍💼 코워커 | 실무·콘텐츠·작가 |
| 🎨 **디자이너**(본 플러그인) | 브랜드·디자인 시스템·Claude Design |
| 📋 PM | 프로젝트 시작 허브 (`/project`) |

실무 문서·카피는 코워커가, 프로젝트 셋업은 PM이 담당합니다.

---

## 더 알아보기 (개발자·디자이너 기술)

- **두 갈래 경로** — `/design`(bare)이 Path A(Claude Design import)와 Path B(코드 기반 브랜드 디자인)를 1라운드 인터뷰로 선택
- **GAN 품질 루프** — Design Quality(30%)·Originality(25%)·Completeness(25%)·Functionality(20%) 4차원 회의적 채점 + `config/design.yaml`의 `max_iterations`/`pass_threshold`/`escalation_after`로 반복 제어
- **파이프라인** — `manager-spec`(BRIEF) → 카피·비주얼 토큰 병렬 생성 → frontend 구현 → `sync-auditor`(GAN 루프)
- **스킬 14종** — 도메인/워크플로우 5종(`moai-domain-brand-design`, `moai-domain-copywriting`, `moai-workflow-design`, `moai-workflow-gan-loop`, `moai-domain-design-handoff`) + Claude Design 전처리·라이브러리 6종(`cd-brief`, `cd-system-prep`, `cd-prompt-builder`, `cd-handoff-reader`, `cd-slop-check`, `design-system-library`) + 토큰·업로드 2종(`design-tokens-transformer`, `design-sync-upload`) + 비주얼 생성 1종(`design-brand-visual`)
- **MCP 연동 1종** — `higgsfield`(mcp.higgsfield.ai). `design-brand-visual`이 사용하며, 생성 실행·모델 선택·크레딧 사전 고지 계약은 `moai-media:media-higgsfield-core`에 위임한다. 인증은 Higgsfield 계정 토큰(파일에 키를 적지 않음)
- **에이전트 3종** — `manager-spec`(BRIEF), `sync-auditor`(GAN 4차원 평가), `builder-harness`(Path B 동적 생성). 조사는 Anthropic 내장 `Explore`
- **anti-slop 정본** — 디자인 카피 AI 슬롭 사전(영문·한국어 Tier 1/2)은 `moai-domain-copywriting`이 정본, `cd-slop-check`는 다운스트림 QA 게이트
- **디자인 헌법** — `rules/moai/design/constitution.md` (파이프라인 순서·5 안전 계층·GAN 루프 계약·평가자 관대성 방지, FROZEN)
- **설정** — `config/design.yaml` (GAN 컨트롤·브랜드 컨텍스트·Claude Design 통합·design_docs 자동 로드)
- **런타임 산출물 경로** — `.moai/design/`(토큰·컴포넌트·브리프), `.moai/project/brand/`(브랜드 컨텍스트). 플러그인은 참조만, 스캐폴드하지 않음

---

**라이선스**: Apache-2.0 · **작성자**: 모두의AI
