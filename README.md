# 모두의 코워크 (MoAI) — `moai-cowork` 마켓플레이스

> **v1.1.0** — 2026-07-31 체계 재정립 이후 첫 공식 릴리스 (v1.0.0은 재시작 기준선).

한국 실무 **AI 직원(전문가)** 을 Claude Code / Claude Desktop에 한 번의 마켓플레이스 등록으로 설치해 쓰는 플러그인 패밀리입니다.

각 플러그인은 하나의 AI 직원입니다. PM(`/project`)이 프로젝트 성격을 파악해 알맞은 직원을 배치하고, 나머지 직원들이 각자의 전문 영역(마케팅·콘텐츠·미디어·커머스·법무·재무·HR·CS·디자인 등)에서 실무를 지원합니다. 비개발자부터 개발자까지 4가지 Claude 제품(Chat · Cowork · Design · Code) 활용 가이드도 함께 제공합니다.

## AI 직원 명단

| 직무 | 플러그인 | 역할 |
|---|---|---|
| **PM (진입 허브)** | `moai-pm` | `/project` 라우터 — 프로젝트 성격 파악 → 알맞은 직원 배치 |
| 코워커 | `moai-coworker` | 범용 실무·라이프스타일 (협업·생산성·AI 프롬프트·개인 일정) |
| 작가 | `moai-writer` | 출판 기획·집필·한글 윤문·맞춤법 |
| 스토리 크리에이터 | `moai-story` | 웹툰·웹소설·IP·스토리보드 |
| 마케터 | `moai-marketer` | 캠페인·콘텐츠·광고·SEO·메타광고 |
| 미디어 크리에이터 | `moai-media` | 이미지·영상·오디오 생성 (Higgsfield·Midjourney·Gemini 등) |
| 셀러 | `moai-seller` | 커머스 운영 (스마트스토어·쿠팡·D2C·상세페이지·광고) |
| 사무관 | `moai-officer` | 오피스 문서 (한글·워드·엑셀·PPT·PDF·노션) |
| 데이터 애널리스트 | `moai-analyst` | 공공데이터·실거래가·경매·주식·통계 조회·시각화 |
| 법무 | `moai-lawyer` | 계약 검토·컴플라이언스·특허·부동산 실명 |
| 재무세무 | `moai-accountant` | 재무제표·세무·투자·보험·예산 |
| 인사채용 | `moai-recruiter` | 채용·이력서 검토·성과평가·인사 운영 |
| CS 매니저 | `moai-cs` | 고객응대·VOC·채널 메시지·티켓 분류 |
| 컨설턴트 | `moai-consultant` | 전략·시장분석·정부지원금·스비즈365 |
| 커리어 코치 | `moai-career` | 이력서·면접·포트폴리오·커리어 전환 |
| 튜터 | `moai-tutor` | 학습 자료·평가·논문·교육과정 |
| 디자이너 | `moai-designer` | 브랜드·로고·디자인 시스템·Claude Design 연동 |
| 스레드 포스터 | `moai-threads-poster` | 소셜 자동 발행 (Threads·Instagram) |

직원별 상세 소개는 [AI 직원](https://cowork.mo.ai.kr/moai-agents/)에서 볼 수 있습니다.

## 설치

```bash
claude plugin marketplace add modu-ai/moai-cowork
```

등록 후 필요한 직원을 설치합니다:

```bash
/plugin install moai-pm@moai-cowork              # 프로젝트 시작 허브 (/project)
/plugin install moai-coworker@moai-cowork       # 범용 실무 올인원
/plugin install moai-writer@moai-cowork         # 작가
/plugin install moai-designer@moai-cowork       # 디자이너
```

전체 목록은 [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)를 참고하세요.

## 문서 사이트 — 4트랙 구조

문서 사이트 [cowork.mo.ai.kr](https://cowork.mo.ai.kr)는 비개발자(10~60대)를 위한 한국어 Claude 활용 가이드입니다. 학습 난이도 상승 순서로 4개 트랙을 제공하며, 각 트랙은 Anthropic 공식 자료(support.claude.com / docs.claude.com)에 정렬됩니다.

| 트랙 | 제품 | 학습 범위 | 가이드 |
|------|------|-----------|------|
| **Chat** | Claude Desktop App | 첫 대화·프롬프트·아티팩트·프로젝트·웹검색·리서치·확장사고·메모리·스킬·커넥터 | [Chat 트랙](https://cowork.mo.ai.kr/guide/chat/) |
| **Cowork** | Claude Cowork | "Claude Code for the rest of your work" — 자율 실행·프로젝트·스킬·플러그인·디스패치·컴퓨터사용·아키텍처 | [Cowork 트랙](https://cowork.mo.ai.kr/guide/cowork/) |
| **Design** | Claude Design | 디자인 시스템·컴포넌트·토큰·핸드오프 (Anthropic Labs 제품) | [Design 트랙](https://cowork.mo.ai.kr/guide/design/) |
| **Code** | Claude Code | 6가지 진입면(웹·데스크톱·IDE·CLI) — 비개발자도 터미널 없이 시작 | [Code 트랙](https://cowork.mo.ai.kr/guide/code/) |

목차의 진실 출처(SSOT)는 [`www/data/menu/main.yaml`](www/data/menu/main.yaml)입니다.

## 문서 사이트 섹션

문서 사이트는 8개 콘텐츠 섹션으로 구성됩니다:

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

## 저장소 구조

```
modu-ai/moai-cowork/
├── .claude-plugin/marketplace.json   # 마켓 매니페스트
├── plugins/                          # 마켓 플러그인 소스 (설치명 = 디렉터리명)
│   ├── moai-pm/                      # 프로젝트 허브
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

## 라이선스

[Apache License 2.0](./LICENSE) — 상업적 사용·수정·재배포 자유. 저작권 고지와 변경 사항 표시가 필요합니다.

이 플러그인으로 **만든 산출물은 여러분 것**이며 상업적 사용에 제한이 없습니다 — [LICENSE-OUTPUT.md](./LICENSE-OUTPUT.md).
제3자 저작물 고지는 [NOTICE](./NOTICE), 이름·로고 사용 규칙은 [TRADEMARKS.md](./TRADEMARKS.md)를 보세요.
