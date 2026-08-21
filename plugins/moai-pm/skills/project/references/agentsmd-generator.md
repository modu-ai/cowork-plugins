# agentsmd-generator.md — AGENTS.md(정본) + CLAUDE.md(임포트) 생성 프로토콜 (project 스킬, Claude·Codex 겸용)

## 개요

`/project` Phase 6에서 호출되는 프로젝트 지침 생성 프로토콜. 폴더 지침의 **정본은 `./AGENTS.md` 한 파일**이며(**200라인 이내**), `./CLAUDE.md`는 그 정본을 `@AGENTS.md` 한 줄로 불러오는 **포인터**다. 두 파일에 같은 내용을 복제하지 않는다 — 복제는 한쪽만 고쳤을 때 조용히 어긋나기 때문이다.

- `AGENTS.md` — Codex(ChatGPT Work)가 자동 로드하는 정본. 전체 지침 본문이 여기에만 있다.
- `CLAUDE.md` — Claude(Cowork/Code)가 자동 로드하며, `@AGENTS.md` 임포트로 정본을 세션 시작 시 펼쳐 읽는다. 결과적으로 두 런타임이 **같은 지침**을 본다(기능 동등).

스킬 상세 내용은 두 파일 어디에도 복사하지 않고, 실행 시 해당 스킬(SKILL.md)을 런타임에 로드하여 사용한다.

**핵심 원칙**:
- 템플릿은 **외부 파일 2종으로 분리**(`references/templates/AGENTS.md.tmpl`, `references/templates/CLAUDE.md.tmpl`). 인라인 하드코딩 금지.
- Phase 3에서 설계된 **스킬 체인**을 `AGENTS.md.tmpl`의 `{workflow_chains}` 슬롯에 주입한다.
- 모든 생성된 `AGENTS.md`에 **8개 `## N. … (HARD)` 블록**이 고정 포함된다(§2.1 예산 표 참조). 라인 예산 초과 시에도 축소 대상이 아니다(축소는 체인 나열만).
- **글로벌 프로필 변수 사용 안 함.** 프로젝트 맥락 변수만 사용한다.
- 별도 규칙 디렉터리 생성 안 함 → `AGENTS.md` 하나에 지침 통합.

---

## 1. 생성 대상

```
<프로젝트>/
├── AGENTS.md              ← 폴더 지침 정본(≤200라인). Codex가 자동 로드
├── CLAUDE.md              ← 포인터(≈11라인). `@AGENTS.md` 임포트만
└── .moai/
    ├── config.json         ← 플러그인·커넥터·API 키 참조
    ├── context.md           ← 프로젝트 맥락 누적
    └── evolution/
```

**생성하지 않는 것**: 개발 러너타임 전용 산출물 클래스(§Desktop Parity Constraints — SKILL.md 참조) — Desktop 실행 환경에서 동작하지 않는다. 글로벌 저장소(`moai-profile.md` 등)도 생성하지 않는다. 키는 `.moai/credentials.env`에 프로젝트별로 GUIDANCE만 저장한다(실제 값은 절대 기록하지 않음).

---

## 2. AGENTS.md 구성 원칙

### 2.1 라인 예산 (200라인 이내)

<!-- @MX:ANCHOR: [AUTO] 200라인 예산 표 — 생성 AGENTS.md ≤ 200라인 불변식의 증명 지점 -->
<!-- @MX:REASON: 신규 규칙 블록 5종은 기존 여유분에서 재배분해 조달했다. 표를 수정하면 합계 ≤ 200이 유지되는지 반드시 재검산할 것 -->

| 섹션 | 예산 | 설명 |
|------|------|------|
| 헤더 + 프로젝트 개요 | 약 15라인 | 프로젝트명, 산출물, 톤 제약 |
| 행동 원칙 | 약 10라인 | 핵심 원칙 5개(HARD) |
| 요청 평가 사다리 | 약 6라인 | 대화→스킬→파일 3단 판단(HARD 고정) |
| 파일 생성 기준 | 약 8라인 | 파일/대화 판단 + 장문 반복 생성(HARD 고정) |
| 문서 생성 우선순위 블록 | 약 18라인 | office/content/media 스킬 매핑(HARD 고정) |
| AI 슬롭 후처리 + 최종 검수 블록 | 약 12라인 | `ai-slop-reviewer` → `korean-humanize` → 최종 검수 규칙(HARD 고정). 최종 검수는 생략 불가 |
| 인용·저작권 가드 | 약 6라인 | 인용 한도·재표현 원칙(HARD 고정) |
| 톤 규칙 | 약 5라인 | 프로즈 기본·응답 깊이 비례(HARD 고정) |
| 스킬 체인 워크플로우 | 약 50라인 | Phase 3에서 설계된 체인 최대 10개 |
| 라우팅 요약 | 약 15라인 | 설치된 플러그인의 키워드 매핑 |
| 커넥터 + API 키 | 약 15라인 | 등록 상태 요약 |
| 딥씽킹 + 참조 | 약 10라인 | `ultrathink` 조건 |
| 맥락 적용 규칙 + 프로젝트 맥락 | 약 5라인 | 선택 적용·메타 코멘터리 금지(HARD 고정) |
| **여유분** | 약 25라인 | 맥락 확장용 |
| **합계** | **≤ 200** | 8개 HARD 블록은 축소 대상이 아니다 — 초과 시 축소는 체인 나열만 |

포인터 `CLAUDE.md`(≈11라인)는 이 예산에 포함하지 않는다 — 고정 길이이고 변수가 없다.

### 2.2 스킬 내용 처리 방식

`AGENTS.md`에 스킬의 전문가 역할·워크플로우·출력 기준을 전체 복사하지 않는다(200라인 초과, 토큰 낭비). 대신 스킬 체인의 핵심 역할과 목적을 2~3줄로 요약하고, 실행 시 해당 스킬이 런타임에 로드되어 상세 지침을 제공한다.

### 2.3 스킬 체인 기록

Phase 3에서 설계된 각 산출물 체인을 `{workflow_chains}` 슬롯에 인라인 스킬 체인으로 주입한다. 최대 **10개 체인까지** 나열한다. 나머지 체인은 안내하지 않고, 사용자가 "어떤 코워커 있어?"로 물을 때 안내한다(제거된 `/project catalog`는 참조 유도에 쓰지 않는다).

### 2.4 CLAUDE.md 포인터 규칙 (HARD)

포인터는 정적 파일이다 — 변수 치환도, 프로젝트별 분기도 없다. `CLAUDE.md.tmpl`을 그대로 복사한다. 다음 두 규칙을 어기면 임포트가 **조용히** 실패한다(에러 없이 지침이 통째로 누락된다).

1. **`@AGENTS.md`를 백틱으로 감싸지 않는다.** 임포트 파서는 마크다운 코드 스팬과 펜스 코드 블록을 건너뛴다. `` `@AGENTS.md` ``라고 쓰면 글자로만 남고 아무것도 불러오지 않는다. 파일 본문에서 이 경로를 "언급"할 일이 있으면 그때만 백틱을 쓴다.
2. **임포트 줄이 파일의 첫 비어있지 않은 줄이어야 한다.** 정본이 세션 컨텍스트에 먼저 들어가고, 그 뒤에 Claude 전용 추가 지침(있다면)이 붙는 순서를 보장하기 위해서다.

보조 사실 두 가지:
- **안내 주석은 토큰을 쓰지 않는다.** 블록 단위 HTML 주석은 컨텍스트 주입 전에 제거된다 — 사람이 파일을 열었을 때만 보인다. 그래서 포인터에 설명을 넉넉히 달아도 비용이 없다.
- **심볼릭 링크는 쓰지 않는다.** `ln -s AGENTS.md CLAUDE.md`도 같은 효과를 내지만 Windows에서 관리자 권한 또는 개발자 모드를 요구한다 — 4조합(macOS/Windows × Claude Cowork/ChatGPT Work) 동일 동작 원칙에 어긋난다. 임포트 방식만 쓴다.

**역방향 금지**: `AGENTS.md`에 `@CLAUDE.md`를 넣는 반대 배선은 동작하지 않는다. Codex는 `@` 임포트를 펼치지 않고 한 줄 텍스트로 넘긴다 — 정본은 반드시 `AGENTS.md` 쪽이어야 한다.

---

## 3. 템플릿

| 템플릿 | 산출 | 성격 |
|--------|------|------|
| `references/templates/AGENTS.md.tmpl` | `./AGENTS.md` | 변수 치환 필요. 8개 HARD 블록 고정 |
| `references/templates/CLAUDE.md.tmpl` | `./CLAUDE.md` | 변수 없음. 그대로 복사 |

`AGENTS.md.tmpl`을 Read하여 변수 치환을 수행한 결과를 `./AGENTS.md`에 Write한다. 생성된 산출물 내부의 스킬 참조는 `moai-*:` 접두어를 그대로 쓴다(Claude·Codex 공통 포맷).

---

## 4. 변수 치환 규칙

변수는 `AGENTS.md.tmpl`에만 존재한다. `CLAUDE.md.tmpl`에는 치환 대상이 없다.

### 4.1 프로젝트 맥락 변수 (Phase 1 인터뷰 결과)

| 변수 | 출처 |
|------|------|
| `{project_name}` | 프로젝트 폴더명(basename) |
| `{project_purpose}` | Phase 1 답변 요약 |
| `{audience}` | Phase 1에서 추출 또는 `미지정` |
| `{tone_constraints}` | Phase 1 톤 답변 |
| `{primary_deliverables}` | Phase 1 자유입력 원문 |

### 4.2 플러그인 / 체인 변수 (Phase 2-3 결과)

| 변수 | 출처 |
|------|------|
| `{installed_plugins}` | Phase 2에서 감지된 플러그인 리스트 |
| `{workflow_chains}` | Phase 3에서 설계된 체인 블록 |
| `{routing_summary}` | 설치된 플러그인 기반 키워드 → 플러그인 매핑 요약 |

### 4.3 시스템 변수

| 변수 | 출처 |
|------|------|
| `{version}` | `moai-pm/.claude-plugin/plugin.json` `version` |
| `{date}` | 오늘 날짜(YYYY-MM-DD) |
| `{connectors_and_apikeys}` | Phase 8에서 등록된 키·커넥터 요약 |
| `{project_context_notes}` | 초기값 비어있음(실행 중 자동 누적) |

### 4.4 사용 금지 변수

`{user_name}`, `{company_name}`, `{role}`, `{industry}` — 글로벌 프로필 시스템을 사용하지 않는다.

---

## 5. 생성 절차

1. 템플릿 로드: `references/templates/AGENTS.md.tmpl`을 Read.
2. 변수 수집: Phase 1 인터뷰 결과 + Phase 2 인벤토리 + Phase 3 체인 설계 + Phase 8 등록 키.
3. 치환: 각 `{변수}`를 수집된 값으로 치환한다.
4. 길이 검증: `wc -l`이 200라인 이하인지 확인. 초과 시 스킬 체인 나열을 최대 10개로 자동 축소한다. **8개 HARD 규칙 블록은 축소·삭제 대상이 아니다.**
5. 주석 제거 + Write: 템플릿의 HTML 주석(출처 표기 포함)은 생성 결과에서 전부 제거한 뒤 `./AGENTS.md`에 저장한다.
6. 포인터 생성: `references/templates/CLAUDE.md.tmpl`을 **치환 없이 그대로** `./CLAUDE.md`에 Write한다(§2.4 HARD 규칙 준수 — 포인터의 안내 주석은 제거하지 않는다. 사람이 읽으라고 있는 것이고 컨텍스트 비용이 없다).
7. 보조 파일 생성: `./.moai/config.json`, `./.moai/context.md`(빈 파일).

---

## 6. 검증 체크리스트

- [ ] `./AGENTS.md` 존재 + 200라인 이내(`wc -l` 확인)
- [ ] `./CLAUDE.md` 존재 + 첫 비어있지 않은 줄이 정확히 `@AGENTS.md`
- [ ] `./CLAUDE.md`의 임포트 줄이 백틱·코드 블록 안에 있지 않음
- [ ] 두 파일에 같은 지침 본문이 중복 저장되어 있지 않음(정본은 `AGENTS.md` 한 곳)
- [ ] 프로젝트명·산출물·톤 제약이 올바르게 치환됨
- [ ] 스킬 체인 블록이 `{workflow_chains}` 자리에 주입됨
- [ ] 8개 `## N. … (HARD)` 블록 전부 고정 포함됨
- [ ] `요청 평가 사다리` / `파일 생성 기준` / `맥락 적용 규칙` / `톤 규칙` / `인용·저작권 가드` 블록 포함
- [ ] `.moai/config.json` 생성됨
- [ ] 프로필 관련 변수 흔적 없음

검증 명령 예시:

```bash
wc -l ./AGENTS.md                              # ≤ 200
grep -cE '^## .*\(HARD\)' ./AGENTS.md          # == 8
grep -m1 -v '^[[:space:]]*$' ./CLAUDE.md       # == @AGENTS.md
```

---

## 7. 업데이트 트리거

| 상황 | 동작 |
|------|------|
| `/project` 재실행 | `AGENTS.md` 재생성 + `CLAUDE.md` 포인터 재작성(재진입 확인 후 — SKILL.md §Socratic Interview S3 참조) |
| `/project evolve` | 자가 개선 진단을 `.moai/evolution/`에 기록(`AGENTS.md`는 `<!-- evolution-log -->`만 갱신 — 최근 10건 유지, 초과분은 `.moai/evolution/log.md`로 이관) |
| 플러그인 추가 설치 | `/project` 재실행 권장(체인 재설계) |
| 스킬 체인 수정 요청 | `AGENTS.md`의 해당 체인 블록만 Edit로 교체(전체 재생성 불필요) |
| **레거시 프로젝트 감지** | `CLAUDE.md`가 포인터가 아니라 전체 지침을 담고 있으면(구 복제 방식) — §7.1 마이그레이션 |

### 7.1 레거시 복제 프로젝트 마이그레이션

구 방식으로 생성된 프로젝트는 `CLAUDE.md`와 `AGENTS.md`에 같은 본문이 두 벌 들어 있다. `/project update` 또는 `/project` 재실행 시 이를 감지하면 다음 순서로 정리한다.

1. **감지**: `./CLAUDE.md`의 첫 비어있지 않은 줄이 `@AGENTS.md`가 아니고, 파일에 `## ` 헤딩이 2개 이상이면 레거시로 판정한다.
2. **정본 확정**: 두 파일의 내용이 다르면 **더 최근에 수정된 쪽**을 정본 후보로 삼고, 어느 쪽을 남길지 `AskUserQuestion`으로 확인한다(내용이 같으면 확인 없이 진행).
3. **이관**: 확정된 본문을 `./AGENTS.md`에 쓴다. `<!-- evolution-log -->` 이력이 `CLAUDE.md`에만 있으면 함께 옮긴다 — **이력을 잃지 않는다.**
4. **포인터 교체**: `./CLAUDE.md`를 `CLAUDE.md.tmpl` 내용으로 덮어쓴다.
5. **검증**: §6 체크리스트를 실행한다.

**개선 경로 예산 재검증**: 자가 개선 diff가 `AGENTS.md`를 수정한 경우에도 §5-4 길이 검증(`wc -l` ≤ 200)을 재실행한다. 라인 예산은 생성 시 1회 검증이 아니라 **`AGENTS.md`가 수정될 때마다 지켜야 하는 불변식**이며, 초과 시 축소 대상은 생성 시와 동일하다(체인 나열만 — 8개 HARD 블록·evolution-log 최근 10건은 축소 대상이 아니다).

---

## 8. 참조 경로

- 정본 템플릿: `references/templates/AGENTS.md.tmpl`
- 포인터 템플릿: `references/templates/CLAUDE.md.tmpl`
- 플러그인 설정: `./.moai/config.json`
- 프로젝트 맥락: `./.moai/context.md`
- API 키: `./.moai/credentials.env`(프로젝트 격리, GUIDANCE 전용)
- 체인 프리셋: `references/cowork-setup.md` §3
- 라우팅 키워드 맵: `references/router.md` §2
