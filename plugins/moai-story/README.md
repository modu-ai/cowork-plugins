# 스토리 크리에이터 (moai-story)

스토리/IP 창작 전담 AI 직원입니다. 웹툰·웹소설·시나리오·콘티·표지·캐릭터 시트·IP 사업화(story-* 17종) 스킬을 하나의 플러그인으로 제공합니다. 슬래시 명령을 외울 필요 없이 자연어로 요청하면 매칭되는 스킬이 자동 호출됩니다.

> **분리 안내**: 본 플러그인의 스토리 스킬들은 `moai-writer`에서 분리되었습니다(출판 book-* 스킬은 moai-writer에 잔류). 신규 호출은 `moai-story:<스킬명>` 네임스페이스를 사용하세요. 이미지·영상 **생성 실행**은 `moai-media` 플러그인에 위임합니다.

**이런 분께 추천**: 웹툰/웹소설 창작자 · 시나리오 작가 · IP 콘텐츠 기획자

## 설치

```
claude plugin marketplace add modu-ai/moai-cowork
claude plugin install moai-story@moai-cowork
```

또는 Claude Code 세션 안에서:

```
/plugin marketplace add modu-ai/moai-cowork
/plugin install moai-story
```

## 스킬 17종 (계층별)

호출 형식: `/moai-story:<스킬명>` — 예: `/moai-story:story-webtoon-episode`. 자연어 요청("웹툰 회차 대본 써줘")으로도 자동 매칭됩니다.

### L0 — 진입 라우터

| 스킬 | 역할 |
|------|------|
| `story-project` | 작품 유형 분류 후 알맞은 story-* 파이프라인으로 라우팅하는 진입점 |

### L1 — 연재 상태 관리

| 스킬 | 역할 |
|------|------|
| `story-series-bible` | 연재 상태 원장 — 마스터 기획서 소유·에피소드 현황표 갱신으로 다회차 연속성 복원 |

### L2 — 규격 SSOT

| 스킬 | 역할 |
|------|------|
| `story-webtoon-spec` | 한국 웹툰 플랫폼 규격 단일 진실 원천 — 데뷔 경로·원고 규격·회차 분량·수익화 훅·용어 사전 |

### L3 — 서사 설계·집필

| 스킬 | 역할 |
|------|------|
| `story-webtoon-planner` | 웹툰 기획 — 세계관·연재구조 3분류·시리즈 아크·관통 주제·훅 전략 설계 |
| `story-webtoon-episode` | 웹툰 회차 — 회차 플롯·세로 스크롤 컷 분할·컷별 프레임 연출 지시 |
| `story-webnovel-planner` | 웹소설 기획 — 6개 플랫폼 회차 분량·결제·태그·독점 비교로 타깃 확정 |
| `story-webnovel-writer` | 웹소설 회차 집필 — 장르별 문법·회차 절단(클리프행어) 등급 설계 |
| `story-synopsis` | 영상 시놉시스 — 로그라인·기획의도·인물·구성, 편성/공모 제출 규격 |
| `story-screenplay` | 시나리오 대본 — S# 넘버·지문·대사를 한국 드라마·영화 관행으로 작성 |
| `story-ip-pitch` | IP 사업화 — 2차 저작 피칭 문서·판권 제안서, 표준계약·저작권 등록 개요 |

### L4 — 연출·작화·식자

| 스킬 | 역할 |
|------|------|
| `story-character-sheet` | 캐릭터 시트 — 비주얼 시트(외형 8항목)·일관성 앵커·Soul ID 참조 세트 사양 |
| `story-webtoon-lettering` | 웹툰 식자 — 말풍선 종류·서체 통일·SFX 스타일·2패스 오버레이 워크플로우 |
| `story-webtoon-art` | 웹툰 작화 프롬프트 — 화풍 앵커 고정·컷별 복붙 프롬프트·내용물 가드 |
| `story-conti` | 영상 콘티·스토리보드 — 프레임 분해·화각/앵글/전환, 드라마·영화·광고 프리셋 |
| `story-previz` | 시네마틱 프리비즈 — 카메라 무빙·렌즈·조명 지정 숏 리스트 |
| `story-cover-art` | 표지·썸네일 — 단행본/웹툰/웹소설 3분기 구도·시선 유도·제목 자리 |

### L5 — 검수 QC

| 스킬 | 역할 |
|------|------|
| `story-webtoon-qc` | 웹툰 산출 이미지 검수 — 결함 7종 점검·세로 스크롤 규격·일관성 앵커 위반 판정 |

> **비고**: 이전 `story-ad-conti`(광고 콘티)는 `story-conti`의 광고 프리셋으로 통합되었습니다.

## 생성 실행 위임 (moai-media)

이미지·영상 생성이 필요한 스킬(`story-webtoon-art`·`story-conti`·`story-character-sheet`·`story-cover-art`·`story-previz`)은 프롬프트 조립·연출 설계까지만 책임지고, **실제 생성 실행·크레딧 고지·모델 선택**은 `moai-media` 플러그인에 위임합니다.

- 생성 작업은 크레딧이 소모되므로 moai-media가 **사전 크레딧 고지 + 사용자 확인** 후에만 실행합니다
- MCP 미연결 시 프롬프트 온리 모드(생성 프롬프트만 산출)로 자동 전환됩니다

## 에이전트 2종

| 에이전트 | 등급 | 역할 |
|----------|------|------|
| `story-director` | worker | 웹툰·웹소설 에피소드, 시나리오, 콘티/프리비즈, 표지, IP 피칭 산출물을 만드는 실무 에이전트. 목표 이해 → 계획 → story-* 스킬 선택 → 실행 → 검증의 에이전트 루프로 동작. 표절 금지·캐릭터/Soul-ID 연속성 보존·플랫폼/제작사 정보 출처 필수·생성 크레딧 사전 고지를 HARD 가드레일로 준수 |
| `story-continuity-auditor` | read-only audit | 스토리 산출물을 회의적으로 검증하는 **서사 연속성 검수** 에이전트 — 캐릭터·플롯·설정 연속성(Soul-ID 포함), 플랫폼 포맷 적합성, 표절/AI 티 위험, IP 권리/피칭 완결성. 증거 기반 PASS/FAIL 판정만 반환하며 파일을 수정하지 않음 |

## 후속 검수 체인

모든 텍스트 산출물은 다음 검수 체인으로 마무리를 권장합니다.

- AI 티 제거 → `moai-coworker:ai-slop-reviewer` → `moai-writer:korean-humanize`

## 라이선스

Apache-2.0 · © 2026 modu-ai (email@mo.ai.kr) — 산출물은 이용자 소유([LICENSE-OUTPUT.md](../../LICENSE-OUTPUT.md))
