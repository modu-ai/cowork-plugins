# claudemd-generator.md — CLAUDE.md 생성 프로토콜 (project 스킬 Desktop 변형)

## 개요

`/project` Phase 6에서 호출되는 `CLAUDE.md` 자동 생성 프로토콜. 사용자 맞춤형 `./CLAUDE.md`를 생성하되, **200라인 이내**로 제한한다. 스킬 상세 내용은 `CLAUDE.md`에 복사하지 않고, 실행 시 해당 스킬(SKILL.md)을 런타임에 로드하여 사용한다.

**핵심 원칙**:
- 템플릿은 **외부 파일(`references/templates/CLAUDE.md.tmpl`)로 분리**. 인라인 하드코딩 금지.
- Phase 3에서 설계된 **스킬 체인**을 템플릿의 `{workflow_chains}` 슬롯에 주입한다.
- 모든 생성된 `CLAUDE.md`에 **8개 `## N. … (HARD)` 블록**이 고정 포함된다(§2.1 예산 표 참조). 라인 예산 초과 시에도 축소 대상이 아니다(축소는 체인 나열만).
- **글로벌 프로필 변수 사용 안 함.** 프로젝트 맥락 변수만 사용한다.
- 별도 규칙 디렉터리 생성 안 함 → `CLAUDE.md` 하나에 지침 통합.

---

## 1. 생성 대상

```
<프로젝트>/
├── CLAUDE.md              ← 이 파일만 생성(≤200라인)
└── .moai/
    ├── config.json         ← 플러그인·커넥터·API 키 참조
    ├── context.md           ← 프로젝트 맥락 누적
    └── evolution/
```

**생성하지 않는 것**: 개발 러너타임 전용 산출물 클래스(§Desktop Parity Constraints — SKILL.md 참조) — Desktop 실행 환경에서 동작하지 않는다. 글로벌 저장소(`moai-profile.md` 등)도 생성하지 않는다. 키는 `.moai/credentials.env`에 프로젝트별로 GUIDANCE만 저장한다(실제 값은 절대 기록하지 않음).

---

## 2. CLAUDE.md 구성 원칙

### 2.1 라인 예산 (200라인 이내)

<!-- @MX:ANCHOR: [AUTO] 200라인 예산 표 — NFR-PMR-002 불변식(생성 CLAUDE.md ≤ 200라인)의 증명 지점 -->
<!-- @MX:REASON: 신규 규칙 블록 5종은 기존 여유분에서 재배분해 조달했다. 표를 수정하면 합계 ≤ 200이 유지되는지 반드시 재검산할 것 -->

| 섹션 | 예산 | 설명 |
|------|------|------|
| 헤더 + 프로젝트 개요 | 약 15라인 | 프로젝트명, 산출물, 톤 제약 |
| 행동 원칙 | 약 10라인 | 핵심 원칙 5개(HARD) |
| 요청 평가 사다리 | 약 6라인 | 대화→스킬→파일 3단 판단(HARD 고정) |
| 파일 생성 기준 | 약 8라인 | 파일/대화 판단 + 장문 반복 생성(HARD 고정) |
| 문서 생성 우선순위 블록 | 약 18라인 | office/content/media 스킬 매핑(HARD 고정) |
| AI 슬롭 후처리 블록 | 약 8라인 | `general-ai-slop-reviewer` 호출 규칙(HARD 고정) |
| 인용·저작권 가드 | 약 6라인 | 인용 한도·재표현 원칙(HARD 고정) |
| 톤 규칙 | 약 5라인 | 프로즈 기본·응답 깊이 비례(HARD 고정) |
| 스킬 체인 워크플로우 | 약 50라인 | Phase 3에서 설계된 체인 최대 10개 |
| 라우팅 요약 | 약 15라인 | 설치된 플러그인의 키워드 매핑 |
| 커넥터 + API 키 | 약 15라인 | 등록 상태 요약 |
| 딥씽킹 + 참조 | 약 10라인 | `ultrathink` 조건 |
| 맥락 적용 규칙 + 프로젝트 맥락 | 약 5라인 | 선택 적용·메타 코멘터리 금지(HARD 고정) |
| **여유분** | 약 29라인 | 맥락 확장용 |
| **합계** | **≤ 200** | 8개 HARD 블록은 축소 대상이 아니다 — 초과 시 축소는 체인 나열만 |

### 2.2 스킬 내용 처리 방식

`CLAUDE.md`에 스킬의 전문가 역할·워크플로우·출력 기준을 전체 복사하지 않는다(200라인 초과, 토큰 낭비). 대신 스킬 체인의 핵심 역할과 목적을 2~3줄로 요약하고, 실행 시 해당 스킬이 런타임에 로드되어 상세 지침을 제공한다.

### 2.3 스킬 체인 기록

Phase 3에서 설계된 각 산출물 체인을 `{workflow_chains}` 슬롯에 인라인 스킬 체인으로 주입한다. 최대 **10개 체인까지** 나열한다. 나머지 체인은 `/project catalog`로 참조 유도한다.

---

## 3. CLAUDE.md 템플릿

템플릿은 외부 파일 `references/templates/CLAUDE.md.tmpl`로 분리되어 있다. 이 파일을 Read하여 변수 치환을 수행한 결과를 `./CLAUDE.md`로 Write한다.

---

## 4. 변수 치환 규칙

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

1. 템플릿 로드: `references/templates/CLAUDE.md.tmpl`을 Read.
2. 변수 수집: Phase 1 인터뷰 결과 + Phase 2 인벤토리 + Phase 3 체인 설계 + Phase 8 등록 키.
3. 치환: 각 `{변수}`를 수집된 값으로 치환한다.
4. 길이 검증: `wc -l`이 200라인 이하인지 확인. 초과 시 스킬 체인 나열을 최대 10개로 자동 축소한다. **8개 HARD 규칙 블록은 축소·삭제 대상이 아니다.**
5. 주석 제거 + Write: 템플릿의 HTML 주석(출처 표기 포함)은 생성 결과에서 전부 제거한 뒤 `./CLAUDE.md`에 저장한다.
6. 보조 파일 생성: `./.moai/config.json`, `./.moai/context.md`(빈 파일).

---

## 6. 검증 체크리스트

- [ ] `./CLAUDE.md` 파일 존재
- [ ] 200라인 이내(`wc -l` 확인)
- [ ] 프로젝트명·산출물·톤 제약이 올바르게 치환됨
- [ ] 스킬 체인 블록이 `{workflow_chains}` 자리에 주입됨
- [ ] 8개 `## N. … (HARD)` 블록 전부 고정 포함됨
- [ ] `요청 평가 사다리` / `파일 생성 기준` / `맥락 적용 규칙` / `톤 규칙` / `인용·저작권 가드` 블록 포함
- [ ] `.moai/config.json` 생성됨
- [ ] 프로필 관련 변수 흔적 없음

---

## 7. 업데이트 트리거

| 상황 | 동작 |
|------|------|
| `/project` 재실행 | `CLAUDE.md` 재생성(재진입 확인 후 — SKILL.md §Socratic Interview S3 참조) |
| `/project evolve` | 자가 개선 진단을 `.moai/evolution/`에 기록(`CLAUDE.md`는 `<!-- evolution-log -->`만 갱신 — 최근 10건 유지, 초과분은 `.moai/evolution/log.md`로 이관) |
| 플러그인 추가 설치 | `/project` 재실행 권장(체인 재설계) |
| 스킬 체인 수정 요청 | 해당 체인 블록만 Edit로 교체(전체 재생성 불필요) |

**개선 경로 예산 재검증**: 자가 개선 diff가 `CLAUDE.md`를 수정한 경우에도 §5-4 길이 검증(`wc -l` ≤ 200)을 재실행한다. 라인 예산은 생성 시 1회 검증이 아니라 **`CLAUDE.md`가 수정될 때마다 지켜야 하는 불변식**이며, 초과 시 축소 대상은 생성 시와 동일하다(체인 나열만 — 8개 HARD 블록·evolution-log 최근 10건은 축소 대상이 아니다).

---

## 8. 참조 경로

- 템플릿: `references/templates/CLAUDE.md.tmpl`
- 플러그인 설정: `./.moai/config.json`
- 프로젝트 맥락: `./.moai/context.md`
- API 키: `./.moai/credentials.env`(프로젝트 격리, GUIDANCE 전용)
- 체인 프리셋: `references/cowork-setup.md` §3
- 라우팅 키워드 맵: `references/router.md` §2
