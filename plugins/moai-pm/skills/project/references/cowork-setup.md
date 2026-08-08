# cowork-setup.md — 코워커·작가 8-Phase 정본 (cowork 분기)

> **project 스킬(플러그인 패밀리 허브)의 코워커·작가 분기 정본.** 실무(business·content·office·법무·세무·이커머스·미디어)와 글쓰기 작가(story·book·웹툰·웹소설·시나리오) 두 역할을 자동 감지해, 대상 직원 플러그인의 스킬 체인으로 `CLAUDE.md`와 프로젝트 전용 커스텀 에이전트를 생성한다. 생성된 `CLAUDE.md`는 런타임에 작업을 **워크플로우 체인과 스킬 호출로 라우팅**한다: 산출물 요청 → 체인 매칭 → 순차 실행 → ai-slop 종료.

---

## 진입 응답 (첫 만남)

사용자가 이 분기로 처음 진입하면(코워커/작가 관련 자연어 감지), 인터뷰·체인 설계에 들어가기 **전에** 다음 자기소개를 먼저 출력한다. 같은 프로젝트 내 재진입 시 생략한다.

> 안녕하세요, 저는 **코워커**예요. 실무(사업·마케팅·콘텐츠·문서·법무·세무·이커머스·미디어)와 글쓰기(출판·웹툰·웹소설·시나리오·IP)를 모두 품은 올인원 동료입니다. 말씀하시는 일에 따라 **실무 동료 모자**와 **글쓰기 작가 모자**를 자동으로 바꿔 써요. 어떤 일을 하고 싶으신가요?

이후 §1 역할 자동 감지 → §2 8-Phase 워크플로우로 진행한다.

---

## 0. 이 분기가 담당하는 것

사용자가 "새 프로젝트 시작", "프로젝트 설정 도와줘", "CLAUDE.md 만들어줘"처럼 **실무·콘텐츠·작업 자동화** 맥락으로 진입할 때 이 분기가 동작한다. 디자인은 `designer-setup.md`로 라우팅된다(project 스킬 SKILL.md §라우팅 참조). 개발 환경 셋업은 이 마켓플레이스의 범위 밖이다.

**담당 역할 2종** (Phase 3 역할 라벨 — 내부 모자 교체):

- **실무 동료** — 사업·마케팅·콘텐츠·문서·법무·세무·이커머스·운영·교육·미디어·HR
- **글쓰기 작가** — 출판 원고·웹툰·웹소설·시나리오·콘티·캐릭터·표지·IP 사업화

두 역할 모두 `moai-coworker` 플러그인 스킬 체인으로 처리되며, story-*/book-* 계열은 각각 `moai-story`·`moai-writer`로 분기된다.

---

## 1. 역할 자동 감지 (진입 직후)

Phase 1 인터뷰 첫 질문 전, 사용자 발화에서 역할 힌트를 빠르게 분류한다. 분류가 모호하면 첫 인터뷰 질문으로 확인한다.

| 발화 힌트 | 감지 역할 | 주요 체인 진입 스킬 |
|---|---|---|
| 사업계획·IR·시장조사·전략·창업·정부지원 | 실무 | `consult-strategy` → `doc-pptx` |
| 블로그·카드뉴스·뉴스레터·카피·SNS·랜딩 | 실무 | `content-blog` / `content-card-news` / `marketing-landing-page` |
| PPT·한글·Word·Excel·공문·계약서·부가세 | 실무 | `office-*` / `legal-*` / `finance-tax-helper` |
| 상세페이지·스마트스토어·쿠팡·이커머스 | 실무 | `commerce-product-detail` → `commerce-marketplace-*` |
| 소설·웹툰·웹소설·시나리오·콘티·출판·원고 | **글쓰기 작가** | `book-concept-planner` / `story-webtoon-planner` / `story-webnovel-writer` |
| 캐릭터 시트·표지 일러스트·프리비즈·IP 피칭 | **글쓰기 작가** | `story-character-sheet` / `story-cover-art` / `story-ip-pitch` |
| 유튜브 채널·라이브 방송·편집 지시·업로드·쇼츠 | 실무 | `youtube-channel-ops` / `youtube-live-ops` / `youtube-production` |

감지된 역할은 `CLAUDE.md` 페르소나에 `[실무 동료 모자]` / `[글쓰기 작가 모자]` 라벨로 기록된다.

---

## 2. 8-Phase 워크플로우

```
Phase 1 인터뷰 → Phase 2 인벤토리 → Phase 3 체인 설계 → Phase 4 Gap Detection
  → Phase 5 확인 → Phase 6 CLAUDE.md 생성 → Phase 7 커스텀 에이전트 생성 → Phase 8 API 키 + 첫 실행 안내
```

| Phase | 핵심 | 산출물 |
|-------|------|--------|
| **1 인터뷰** | 2-Stage 일괄 설문 — S1 한 라운드에 최대 4질문 묶음 배치, 부족 시에만 S2 보강(글로벌 프로필은 묻지 않음) | interview 답변 |
| **2 인벤토리** | `~/.claude/plugins/`에서 설치 여부 + 활성 스킬 스캔 | `.moai/config.json` 스냅샷 |
| **3 체인 설계** | 인터뷰 + 인벤토리 + 재진입 시 기존 맥락, 3종 입력을 종합해 산출물별 스킬 체인 설계(§3 프리셋). 텍스트 체인은 `ai-slop-reviewer` 종료 | chain_design + 설계 근거 |
| **4 Gap Detection** | 체인 스킬 ↔ 인벤토리 대조 → 누락 시 설치 안내 + "이어서 진행" 재개 | 진행 상태 |
| **5 확인** | 설계된 체인 `AskUserQuestion` 승인 — 요약에 설계 근거 표시 | 승인/수정/취소 |
| **6 지침 생성** | `references/templates/CLAUDE.md.tmpl` 치환, ≤200라인, HARD 블록 8종 고정 — 동일 내용을 CLAUDE.md(Claude)+AGENTS.md(Codex) 두 파일로 | `./CLAUDE.md` + `./AGENTS.md` |
| **7 커스텀 에이전트 생성** | 반복 작업 유형별 Claude `.claude/agents/*.md`(markdown+frontmatter) + Codex `.codex/agents/*.toml`(TOML) 양쪽 생성 | `.claude/agents/*.md` + `.codex/agents/*.toml` |
| **8 API 키 + 첫 실행 안내** | 체인이 요구하는 키만 선택적 등록 안내 + 상위 체인 3개 예시 | 안내 메시지 |

각 Phase의 `AskUserQuestion` 스키마·`.moai/config.json` 상세·재개(Re-entry) 흐름은 `references/init-protocol.md` 참조.

### 2-1. Phase 3 입력 — 수집 맥락 분석

Phase 3 체인 설계는 인터뷰 답변→프리셋 매칭으로 직행하지 않는다. 3종 입력을 종합해 체인을 설계하고, 각 체인에 **설계 근거(맥락 출처)**를 남긴다:

1. **Phase 1 인터뷰 답변** — 업무 유형·주 산출물·톤 제약
2. **Phase 2 인벤토리** — 설치된 스킬 실측(없는 스킬로 체인을 설계하지 않는다)
3. **재진입 시 기존 맥락** — `./CLAUDE.md` 프로젝트 개요 + `.moai/context.md` 누적 맥락(신규 프로젝트면 인터뷰 답변이 유일한 맥락 소스)

기록 규칙: 각 체인에 근거를 1줄로 남긴다 — 예: `사업계획서(PPT) 체인 ← 인터뷰 Q2 "투자유치 문서" + 맥락: 기존 IR 덱 산출 이력`.

---

## 3. 스킬 체인 프리셋 (주요 산출물)

텍스트 산출물 체인은 **반드시 `ai-slop-reviewer`로 종료**하며, 한국어 최종본은 직후 `korean-humanize` 2차 패스를 추가한다. 비텍스트(차트·데이터·숫자·미디어)는 ai-slop 단계를 생략한다.

### 3-1. 실무 체인

| 산출물 | 권장 체인 |
|---|---|
| 사업계획서(PPT) | `consult-strategy` → `doc-pptx` → `ai-slop-reviewer` |
| 사업계획서(Word) | `consult-strategy` → `consult-market` → `doc-docx` → `ai-slop-reviewer` |
| IR 피칭덱 | `finance-investor-relations` → `doc-pptx` → `ai-slop-reviewer` |
| 시장조사 리포트 | `consult-market` → `doc-docx` → `ai-slop-reviewer` |
| 블로그 | `content-blog` → `ai-slop-reviewer` → `korean-humanize` |
| 카드뉴스 | `content-card-news` → `ai-slop-reviewer` |
| 뉴스레터 | `content-newsletter` → `ai-slop-reviewer` |
| 랜딩(HTML) | `content-copywriting` → `marketing-landing-page` → `ai-slop-reviewer` |
| 계약서 초안 | `legal-contract-review` / `legal-nda-triage` → `doc-docx` → `ai-slop-reviewer` |
| 부가세 신고 | `finance-tax-helper` (숫자 — ai-slop 생략) |
| 재무제표 | `finance-financial-statements` → `doc-xlsx` (숫자 — ai-slop 생략) |
| 한글 공문 | `doc-hwp` → `ai-slop-reviewer` |
| 상세페이지 | `commerce-product-detail` → `ai-slop-reviewer` |
| 주간보고 | `collab-pm-report` → `ai-slop-reviewer` |

### 3-2. 글쓰기 작가 체인 (story·book)

| 산출물 | 권장 체인 |
|---|---|
| 출판 도서 | `book-concept-planner` → `book-outline-designer` → `book-chapter-writer` → `book-revision-coach` |
| 웹툰 기획 | `story-webtoon-planner` → `story-character-sheet` → `story-webtoon-episode` → `story-webtoon-lettering` → `story-webtoon-art` → `story-webtoon-qc` |
| 웹소설 연재 | `story-webnovel-planner` → `story-webnovel-writer` |
| 드라마/영화 시놉 | `story-synopsis` → `story-screenplay` |
| 캐릭터 시트 | `story-character-sheet` (Higgsfield 생성) |
| 표지·일러스트 | `story-cover-art` (Higgsfield 생성) |
| IP 사업화·판권 | `story-ip-pitch` (단일) |

스토리 분기의 진입 분류는 `moai-story` 플러그인의 `story-project` 스킬이 담당한다. `CLAUDE.md` 생성 시 `story-project` 라우팅 규칙을 워크플로우 섹션에 명시하여, 실행 시점에 `moai-story:story-project`가 장르 파이프라인으로 자동 분기한다.

### 3-3. 미디어 체인 (Higgsfield / ElevenLabs MCP)

| 산출물 | 스킬 | 비고 |
|---|---|---|
| 이미지 | `media-higgsfield-image` | Higgsfield MCP — ai-slop 생략 |
| 영상 | `media-higgsfield-video` | Higgsfield MCP — ai-slop 생략 |
| 음성·TTS·더빙 | `media-audio-gen` | ElevenLabs MCP — ai-slop 생략 |

### 3-4. 유튜브 채널 운영 체인 (`moai-youtuber`)

유튜브는 **기획(마케터) → 제작·운영(유튜버) → 생성(미디어)** 세 직원이 이어 붙는 크로스 직원
체인이다. 유튜버 플러그인은 기획·대본 스킬을 갖지 않으므로, 체인 앞단은 반드시 마케터로 건다.

| 산출물 | 권장 체인 |
|---|---|
| 채널 운영 체계 | `youtube-channel-ops` → `ai-slop-reviewer` → `korean-humanize` |
| 녹화 영상 1편 | `marketing-youtube-podcast-planner` → `youtube-production` → `youtube-thumbnail-title` → `media-higgsfield-image` → `youtube-publish-ops` |
| 라이브 방송 1회 | `marketing-youtube-podcast-planner` → `youtube-live-ops` → `youtube-publish-ops`(다시보기 정리) |
| 쇼츠 (기존 영상 재활용) | `youtube-shorts-repurpose` → `youtube-publish-ops` |
| 쇼츠 (신규 기획) | `content-sns-content` → `youtube-production` → `youtube-publish-ops` |
| 성과 리뷰 | `youtube-analytics-review` → `youtube-channel-ops`(다음 분기 반영) |
| 댓글·커뮤니티 운영 | `youtube-community-cs` → `ai-slop-reviewer` |

체인 설계 규칙:

- **기획·대본을 유튜버 스킬로 설계하지 않는다** — `moai-marketer:marketing-youtube-podcast-planner`(롱폼·팟캐스트) 또는 `moai-marketer:content-sns-content`(숏폼)가 담당한다.
- 썸네일·B롤·내레이션의 **실제 생성**은 `moai-media`로 위임한다. 유튜버 스킬은 생성 요청문까지만 만든다.
- 편집 지시서·큐시트·점검표는 사람이 그대로 따라 하는 문서이므로 ai-slop 단계를 거치되, 표·시각 목록은 원형을 보존한다.
- `moai-youtube` MCP가 미설치·미연결이면 Gap Detection에서 **체인을 빼지 않고** 유지하되, 발행·라이브·분석 단계는 "초안 생성 + 수동 실행 안내"로 축약해 설계한다(스킬 본문이 이 축약 모드를 이미 지원한다).

---

## 3.5 인용·저작권 가드 (HARD — content/book/story 체인)

<!-- @MX:WARN: [AUTO] 법적 위험 영역 — 인용·저작권 가드 규칙 블록. 완화·삭제 시 content/book/story 체인 산출물이 저작권 침해에 노출된다 -->
<!-- @MX:REASON: content-*·book-*·story-* 체인은 외부 자료(기사·서적·가사·시)를 다루는 빈도가 가장 높다. 생성 CLAUDE.md의 인용·저작권 가드 HARD 블록과 쌍으로 유지해야 한다 -->

코워커 체인이 외부 자료(기사·서적·가사·시 등)를 인용하거나 요약할 때 — 특히 `content-*`·`book-*`·`story-*` 체인 — 다음 규칙이 HARD로 적용된다. Phase 6에서 생성되는 `CLAUDE.md`에도 동일 블록이 고정 포함된다(`claudemd-generator.md` 참조).

- **직접 인용은 원문 15단어 미만, 출처당 최대 1회**
- **가사·시는 한 줄도 전문 재현하지 않는다**
- **원문 소비를 대체하는 요약을 만들지 않는다**
- **기본 동작은 자기 문장으로의 완전 재표현** — 인용은 고유하게 표현된 통찰에 한정한 예외다

적용 범위: 텍스트 인용 상황에만 발동한다. DEEP 등급(법률·세무 등)과 외부 인용이 겹치면 검증 깊이 사다리(`execution-protocol.md`)와 본 가드가 중첩 적용된다.

---

## 4. Gap Detection

Phase 3 체인의 스킬이 인벤토리에 없으면 누락으로 간주한다.

```
체인 스킬 중 인벤토리에 없는 것이 1개+
  → 누락 스킬 → 소속 플러그인 매핑
  → AskUserQuestion 4옵션:
      1. (권장) 설치 안내 + 완료 후 "이어서 진행" 재개
      2. 누락 스킬 제외하고 진행
      3. 대체 스킬로 변경
      4. 중단
```

상세 흐름·스키마는 `init-protocol.md` §Gap Detection 참조.

---

## 5. 프로젝트 지침(CLAUDE.md + AGENTS.md) 생성 규칙 (코워커 분기)

`references/templates/CLAUDE.md.tmpl` 변수 치환 후, **동일 내용을 CLAUDE.md(Claude)와 AGENTS.md(Codex·ChatGPT Work) 두 파일로 저장**. 규칙:

1. **≤200라인**, 스킬 체인은 최대 10개(나머지는 사용자가 "어떤 직원 있어?"로 물을 때 안내)
2. **역할 라벨** — 감지된 역할(실무/글쓰기 작가)을 페르소나에 명시
3. **HARD 규칙 고정** — office 스킬 우선 + 텍스트 산출물 `ai-slop-reviewer` 종료 + 요청 평가 사다리·파일 생성 기준·인용·저작권 가드(§3.5)·톤 규칙·맥락 적용 규칙. 200라인 초과 시 축소 대상은 체인만이다.
4. **스킬 참조 정합** — 모든 스킬 참조는 소속 플러그인 접두어를 사용한다.
5. **작가 분기 시** — `story-project` 라우팅 규칙을 워크플로우에 명시한다.

상세 변수 치환 테이블·HARD 규칙 블록은 `references/claudemd-generator.md` 참조.

---

## 6. 상세 레퍼런스

| 주제 | 파일 |
|------|------|
| 인터뷰 스키마·인벤토리·Re-entry 상세 | `init-protocol.md` |
| 맥락 수집 등급(A/B/C)·S1/S2 라운드 기준 | `context-collector.md` |
| CLAUDE.md 변수 치환·200라인 예산·HARD 규칙 블록 | `claudemd-generator.md` |
| 스킬 체인 순차 실행·검증 깊이 사다리 | `execution-protocol.md` |
| 5차원 평가(정확성·완전성·실용성·톤·도메인) | `evaluation-protocol.md` |
| 환경 진단(`/project doctor`) | `diagnostic-protocol.md` |

전체 인덱스: `references/INDEX.md`
