# claudemd-generator.md — CLAUDE.md 생성 프로토콜

## 개요

bare `/project`(레거시 `/project init`) 초기화 Phase 6에서 호출되는 CLAUDE.md 자동 생성 프로토콜.
사용자 맞춤형 `./CLAUDE.md`를 생성하되, **200라인 이내**로 제한한다.
스킬의 상세 내용은 CLAUDE.md에 복사하지 않고, 실행 시 해당 **스킬(SKILL.md)을 런타임에 로드**하여 사용한다.

**핵심 원칙:**
- CLAUDE.md 템플릿은 **외부 파일(`references/templates/CLAUDE.md.tmpl`)로 분리**. 인라인 하드코딩 금지.
- 초기화 워크플로우는 Phase 3에서 설계된 **스킬 체인**을 템플릿의 `{workflow_chains}` 슬롯에 주입한다.
- 모든 생성된 CLAUDE.md에 **office/web 스킬 우선 + AI 슬롭 후처리 HARD 규칙 블록**이 고정 포함된다.
- **글로벌 프로필 변수(`{user_name}`, `{company_name}`, `{role}`, `{industry}`) 사용 안 함.** 프로젝트 맥락 변수만 사용한다.
- `.claude/rules/` 생성 안 함 → CLAUDE.md 하나에 지침 통합
- **한국어 전용** (다국어 템플릿 없음)

---

## 1. 생성 대상

```
<프로젝트>/
├── CLAUDE.md              ← 이 파일만 생성 (≤ 200라인)
└── .moai/
    ├── config.json        ← 플러그인, 커넥터, API 키 참조
    ├── context.md         ← 프로젝트 맥락 누적
    └── evolution/
```

**생성하지 않는 것:**
- `.claude/rules/` — v1.0.0에서 제거
- `.claude/settings.json` — 사용하지 않음
- `moai-profile.md`, `moai-credentials.env` (글로벌 저장소) — **v1.3.0에서 제거**. 키는 `.moai/credentials.env`에 프로젝트별로 저장.

---

## 2. CLAUDE.md 구성 원칙

### 2.1 라인 예산 (200라인 이내)

| 섹션 | 예산 | 설명 |
|------|------|------|
| 헤더 + 프로젝트 개요 | 약 15라인 | 프로젝트명, 산출물, 톤 제약 |
| 행동 원칙 | 약 10라인 | 핵심 원칙 4개 (HARD) |
| 문서 생성 우선순위 블록 | 약 18라인 | office/content/media 스킬 매핑 (HARD 고정) |
| AI 슬롭 후처리 블록 | 약 8라인 | ai-slop-reviewer 호출 규칙 (HARD 고정) |
| 스킬 체인 워크플로우 | 약 50라인 | Phase 3에서 설계된 체인 최대 10개 |
| 라우팅 요약 | 약 15라인 | 설치된 플러그인의 키워드 매핑 |
| 커넥터 + API 키 | 약 15라인 | 등록 상태 요약 |
| 딥씽킹 + 참조 | 약 10라인 | `--deepthink`/`ultrathink` 조건 |
| **여유분** | 약 59라인 | 맥락 확장용 |
| **합계** | **≤ 200** | |

### 2.2 스킬 내용 처리 방식

```
❌ 잘못된 방식:
  CLAUDE.md에 스킬의 전문가 역할, 워크플로우, 출력 기준을 전체 복사
  → 200라인 초과, 토큰 낭비

✅ 올바른 방식:
  CLAUDE.md에는 스킬 체인의 핵심 역할과 목적을 2~3줄로 요약
  → 실행 시 해당 스킬(SKILL.md)이 런타임에 로드되어 상세 지침을 제공
```

### 2.3 스킬 체인 기록

Phase 3에서 설계된 각 산출물 체인을 `{workflow_chains}` 슬롯에 주입한다. 체인 표기 규약의 SSOT는 `references/core/agent-catalog.md` §체인 표기 규약이며, 코디네이터 우선 판정(§결정 규칙)에 따라 아래 두 형식 중 하나를 쓴다.

**(a) 매칭 코디네이터가 있는 경우** — 담당 코디네이터를 실행기로 명시한다:

```markdown
### {산출물명}
- 요청 예시: "..."
- 실행기: `{coordinator-name}` (에이전트, Cowork)
- 내부 체인: `skill-A` → `skill-B` → `ai-slop-reviewer` → `humanize-korean`
- 폴백(에이전트 미가용 시): `skill-A` → `skill-B` → `ai-slop-reviewer`  (인라인 스킬 체인)
```

**(b) 매칭 코디네이터가 없는 경우** — 인라인 스킬 체인으로 표기한다:

```markdown
### {산출물명}
- 요청 예시: "..."
- 체인: `skill-A` → `skill-B` → `skill-C` → `ai-slop-reviewer`
- 입력: ...
- 출력: ... + 검수 리포트
```

최대 **10개 체인까지** 나열. 나머지 체인은 `/project catalog`로 참조 유도.

---

## 3. CLAUDE.md 템플릿

템플릿은 외부 파일로 분리되어 있다:

```
moai-core/skills/project/references/templates/CLAUDE.md.tmpl
```

이 파일을 Read하여 아래 변수 치환을 수행한 결과를 `./CLAUDE.md`로 Write한다.

---

## 4. 변수 치환 규칙

### 4.1 프로젝트 맥락 변수 (Phase 1 인터뷰 결과)

| 변수 | 출처 | 예시 |
|------|------|------|
| `{project_name}` | 프로젝트 폴더명 (basename) | `my-startup` |
| `{project_purpose}` | Phase 1-1·1-2 답변 요약 | "초기 스타트업의 사업계획 및 투자유치 문서 제작" |
| `{audience}` | Phase 1-2에서 추출 또는 `미지정` | "투자자, 관공서, 내부 팀" |
| `{tone_constraints}` | Phase 1-3 답변 | "공식·격식체 유지, 국문 전용" |
| `{primary_deliverables}` | Phase 1-2 자유입력 원문 | "사업계획서 PPT, IR 덱, 시장조사 리포트" |

### 4.2 플러그인 / 체인 변수 (Phase 2-3 결과)

| 변수 | 출처 |
|------|------|
| `{installed_plugins}` | Phase 2에서 감지된 플러그인 리스트(쉼표 구분) |
| `{workflow_chains}` | Phase 3에서 설계된 체인 블록(Markdown, 담당 코디네이터 명시 — §2.3 형식) |
| `{coordinator_agents}` | Phase 3에서 실행기로 채택된 코디네이터를 §5.4 표로 렌더(`agents_available` ∩ Phase 3 선택분, `agent-catalog.md` §체인 표기 규약). 관련 0건이면 빈 값 |
| `{generated_agents}` | Phase 3.5에서 생성된 프로젝트 에이전트 목록(이름 + 한 줄 설명). 생성 0건이면 빈 값 |
| `{routing_summary}` | 설치된 플러그인 기반 키워드 → 플러그인 매핑 테이블(각 플러그인의 `router.md` §3 키워드 행에서 도출) |

### 4.3 시스템 변수

| 변수 | 출처 |
|------|------|
| `{version}` | `moai-core/.claude-plugin/plugin.json` `version` |
| `{date}` | 오늘 날짜 (YYYY-MM-DD, `+09:00` 기준) |
| `{connectors_and_apikeys}` | Phase 7에서 등록된 키·커넥터 요약 |
| `{project_context_notes}` | 초기값 비어있음 (실행 중 자동 누적) |

### 4.4 사용 금지 변수

다음 변수는 템플릿에 **사용 금지**:

- `{user_name}`, `{company_name}`, `{role}`, `{industry}` — 글로벌 프로필 시스템을 사용하지 않음
- `{harness_name_ko}`, `{harness_id}`, `{installed_skill}` — 단일 하네스 모델 폐기, 스킬 체인으로 대체

---

## 5. 생성 절차

```
1. 템플릿 로드
   Read: moai-core/skills/project/references/templates/CLAUDE.md.tmpl

2. 변수 수집
   - Phase 1 인터뷰 결과
   - Phase 2 감지된 플러그인 + `agents_available`(코디네이터 인벤토리)
   - Phase 3 스킬 체인 설계
   - Phase 3에서 실행기로 채택된 코디네이터 → {coordinator_agents} 슬롯에 §5.4 표로 주입
     (`agents_available` ∩ Phase 3 선택분, `agent-catalog.md` §체인 표기 규약. 관련 0건이면 빈 값)
   - Phase 3.5에서 생성한 프로젝트 에이전트 목록 → {generated_agents} 슬롯에 주입
     (생성 0건이면 빈 값 — 해당 섹션은 비어 있게 둔다)
   - 설치된 플러그인 각각의 `router.md` §3 키워드 행 → {routing_summary} 요약 테이블 생성
   - Phase 7 등록된 API 키/커넥터

3. 치환
   각 {변수}를 수집된 값으로 치환.

4. 길이 검증
   wc -l 결과가 200라인 이하인지 확인. 초과 시 스킬 체인 나열을 최대 10개로 자동 축소.

5. Write
   ./CLAUDE.md에 저장.

6. 보조 파일 생성
   - ./.moai/config.json (플러그인/커넥터/키 상태)
   - ./.moai/context.md (빈 파일, 실행 중 누적)
```

---

## 6. 검증 체크리스트

생성 후 확인:

- [ ] `./CLAUDE.md` 파일 존재
- [ ] **200라인 이내** (`wc -l` 확인)
- [ ] 프로젝트명·산출물·톤 제약이 올바르게 치환됨
- [ ] 스킬 체인 블록이 `{workflow_chains}` 자리에 주입됨
- [ ] `{coordinator_agents}` 표가 §5.4에 주입됨 (관련 코디네이터 0건이면 의도적 빈 값)
- [ ] `{generated_agents}`가 §5.5에 처리됨 (생성 0건이면 의도적 빈 값)
- [ ] `{routing_summary}`가 §7에 주입됨
- [ ] office/web 스킬 우선 표(§3)가 고정 포함됨
- [ ] AI 슬롭 후처리 규칙(§4)이 고정 포함됨
- [ ] 실행 플로우(Interview → Plan → Confirm → Execute) 포함
- [ ] `.moai/config.json` 생성됨
- [ ] 프로필 관련 변수(`{user_name}` 등) 흔적 없음

---

## 7. 업데이트 트리거

| 상황 | 동작 |
|------|------|
| `/project` 재실행 (레거시 `/project init`) | CLAUDE.md 재생성 (기존 덮어쓰기, 사용자 확인 후) |
| `/project evolve` | 반성 결과를 `.moai/evolution/`에 기록 (CLAUDE.md 변경 없음) |
| 플러그인 추가 설치 | `/project` 재실행 권장 (체인 재설계) |
| 스킬 체인 수정 요청 | 해당 체인 블록만 Edit로 교체 (전체 재생성 불필요) |

---

## 8. 참조 경로

- 템플릿: `moai-core/skills/project/references/templates/CLAUDE.md.tmpl`
- 플러그인 설정: `./.moai/config.json`
- 프로젝트 맥락: `./.moai/context.md`
- API 키: `./.moai/credentials.env` (프로젝트 격리)
- 체인 프리셋: `references/core/init-protocol.md` §3-2
- 코디네이터 인지·체인 표기 규약: `references/core/agent-catalog.md` (§체인 표기 규약·§결정 규칙)
- 라우팅 키워드 맵: `references/core/router.md` §3
