# 작가 (moai-writer)

출판·텍스트 전담 AI 코워커입니다. 출판 기획·집필·제안서·출판사 매칭(book-* 8종), 한국어 인문화 윤문과 맞춤법 검수까지 텍스트 창작 전 과정 스킬 10종을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> **스토리/IP 창작 분리 안내**: 웹툰·웹소설·시나리오·콘티·표지·IP 사업화(story-* 13종)는 `moai-story` 플러그인으로 분리되었습니다. 스토리 창작 요청은 moai-story을 설치해 사용하세요.

**이런 분께 추천**: 작가 · 1인 출판인 · 실용서 저자

## 설치

`modu-ai/moai-cowork` 마켓플레이스 하나에서 설치합니다. **Claude Cowork**와 **ChatGPT Work** 두 데스크톱 앱 모두 같은 방식입니다.

**가장 쉬운 방법** — 설정(Settings) 또는 플러그인(Plugins) 메뉴 → 마켓플레이스(Marketplace)에서 주소 `modu-ai/moai-cowork`를 추가한 뒤, 플러그인 목록에서 `moai-writer`를 찾아 **Install**을 누르세요.

**터미널에 익숙하다면 (대안)**

```bash
# Claude Cowork CLI
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-writer@moai-cowork

# ChatGPT Work CLI
codex plugin marketplace add modu-ai/moai-cowork
codex plugin add moai-writer@moai-cowork
```

> 앱별 정확한 클릭 경로와 잘 안 될 때 대처법은 [플러그인 설치와 관리](https://cowork.mo.ai.kr/plugins/install/)에 정리해 두었습니다.

## 스킬 10종

호출 형식: `/moai-writer:<스킬명>` — 예: `/moai-writer:book-concept-planner`. 자연어 요청("책 컨셉서 만들어줘")으로도 자동 매칭됩니다.

### 출판 (book-* 8종)

| 스킬 | 역할 |
|------|------|
| `book-concept-planner` | 출판사 제출용 도서 컨셉서 작성 (한 줄·30자·300자 요약, USP 3축, 시장 포지셔닝) |
| `book-target-reader` | 타깃 독자 페르소나·JTBD·페인포인트 매트릭스 설계 |
| `book-outline-designer` | 부·장·꼬지 3레벨 목차 설계 + 분량 배분 + 챕터 시놉시스 |
| `book-chapter-writer` | 챕터 초고 집필 — 꼭지 단위 작성·매수 관리·4 장르 문체 분기 |
| `book-revision-coach` | 퇴고·교열 코치 — 어법·문체·논리·인용·분량 7단계 점검 |
| `book-author-bio` | 저자 약력·저자의 말 통합 작성 (50/200/500자 3길이) |
| `book-proposal-writer` | 출판사 투고용 제안서 — 기획서 + 샘플 챕터 + 마케팅 플랜 통합 |
| `book-publisher-matcher` | 한국 출판사 매칭 — 장르·규모·계약·인세 4차원 평가로 Top 5 추천 |

### 한국어 마감 (2종)

| 스킬 | 역할 |
|------|------|
| `korean-humanize` | AI가 쓴 한국어의 "AI 티"를 제거하는 인문화 윤문 (의미·수치·인용 100% 보존, 변경률 30%/50% 가드) |
| `korean-spell-check` | 바른한글 기반 띄어쓰기·맞춤법·문법 최종 검수 |

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `writer-director` | worker | 책 기획·원고·제안서 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → book-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 표절 금지·사실 앵커 보존·출판사/공모전 정보 출처 필수를 HARD 가드레일로 준수. 스토리/IP 요청은 moai-story의 story-director로 인계 |
| `manuscript-auditor` | read-only audit | 원고·제안서를 회의적으로 검증하는 감사 에이전트 — 캐릭터·세계관·시점 일관성, 표절/AI 티 위험, 장르 관습 적합성, 제안서 완결성. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
