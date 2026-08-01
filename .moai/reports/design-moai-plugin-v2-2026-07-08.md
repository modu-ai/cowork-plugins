# MoAI 플러그인 재설계 v2 — 확정 결정 + 환경 매트릭스 개정판

- 작성: 2026-07-08 (session 8f3b6245) — v1(`design-moai-adk-desktop-plugin-2026-07-08.md`)을 대체(supersede)
- 반영 원천: v1 §1~§9(템플릿 분석·P0-1~5 실측) + 사용자 제공 확장 메커니즘×환경 실측·리서치 보고(CC 2.1.204, 17-agent 워크플로우, 공식 문서 인용) + D-1~D-4 사용자 확정
- v1 참조 유지: 템플릿 인벤토리(§3)·바이너리 커플링(§3.2)·P0 증거(§9)는 v1이 정본

---

## 1. 확정 결정 레지스터

| # | 결정 | 확정값 (2026-07-08 사용자 확정) |
|---|---|---|
| D-1 | 플러그인 이름 | **`moai`로 개명** — 커맨드 `/moai:plan` 템플릿 UX 완전 파리티. 브랜딩은 `displayName: "코더"` 유지로 해소(name=네임스페이스, displayName=UI 표기 분리) |
| D-2 | 파리티 모델 | **Slim-Scaffold** — 프로젝트 귀속 자산만 스캐폴드, 프롬프트 자산은 플러그인 네이티브. REQ-BD-006 byte-parity 계약 개정 |
| D-3 | 배포 원천 | **현행 vendor 유지** — moai-adk-go `moai plugin export` → CI → claude.mo.ai.kr `plugins/` 자동 PR, 단일 마켓 `moai-claude` |
| D-4 | 언어 전략 | **ko 단일 export** — 다국어는 후속 |
| D-5 | persona `agent` 키 | **기본 미동봉 + opt-in 확정** (2026-07-08 사용자 확정) — moai 플러그인 본체에는 `agent` 키 미포함, 페르소나는 T2 스캐폴드의 `outputStyle: "moai:MoAI"` 포인터로 전달. opt-in 경로(별도 경량 persona 플러그인 또는 설치 안내)는 P3 이후 검토 |

## 2. 환경 지원 매트릭스 (개정)

v1은 "Desktop 클라우드 세션 = 프롬프트 자산만"으로 단순화했으나, 신규 실측·리서치 보고로 개정한다. 핵심 원리: **Web으로 갈수록 "repo에 커밋된 `.claude/`·`.mcp.json`만 동작 + `~/.claude`(사용자 전역) 무시 + 대화형 관리 불가"의 한 방향 감쇠**.

| 기능 | CLI (로컬) | Desktop 로컬 세션 | Web (claude.ai/code · Desktop 원격 세션) |
|---|---|---|---|
| 플러그인 로드 | ✅ user/project scope | ✅ (관리는 GUI — `/plugin` 슬래시는 CLI 전용) | ⚠️ **repo `.claude/settings.json`에 선언된 것만** (`extraKnownMarketplaces`+`enabledPlugins`), 대화형 관리 불가, 첫 세션 불안정(issue #63028) |
| hooks | ✅ | ✅ | ⚠️ repo 선언 훅만, 샌드박스 VM 내 실행(`$CLAUDE_CODE_REMOTE=true`), 네트워크 egress 정책 적용 — 문서 기반, 실측 권장 |
| agents | ✅ | ✅ | ✅ repo `.claude/agents/`만 |
| rules / CLAUDE.md | ✅ | ✅ | ⚠️ repo 것만, 사용자 메모리·`~/.claude/CLAUDE.md` 무시 |
| commands / skills | ✅ (내부적으로 통합: commands=skills) | ✅ | ⚠️ repo + claude.ai에서 켠 skills, `~/.claude` personal 무시 |
| MCP | ✅ stdio/http/sse + claude.ai 커넥터 브리지 | ✅ + Desktop 커넥터/임포트 | ⚠️ repo `.mcp.json` + 프록시 커넥터만, `mcp add` 불가 |
| `moai` 바이너리 (T3) | ✅ 설치 시 | ✅ 설치 시 | ❌ 설치 불가 확정 |
| dynamic-workflow | ✅ | ✅ | ❌ 미문서(저신뢰 추론) |

신뢰도 주석: CLI/Desktop 로컬 열은 로컬 실측(P0 + 사용자 보고 🧪), Web 열은 공식 문서·커뮤니티 근거(이 머신에서 실행 불가). v1 §2.2의 "클라우드 세션 Bash/MCP/LSP 불가"(desktop.md 근거)와 신규 보고의 "웹 훅은 샌드박스 VM에서 실행"은 표면상 충돌 — 해석: 클라우드/웹 세션은 **로컬 머신 자원 접근·stdio 영속화·바이너리 설치**가 차단되는 것이며 VM 내 셸 실행 자체는 가능. 최종 확정은 P0-w(§8) 실측으로.

## 3. 티어 모델 개정 — "스캐폴드가 Web 지원의 열쇠"

| Tier | 조건 | 도달 환경 | 제공 능력 |
|---|---|---|---|
| **T1** | 플러그인 설치 (user scope) | CLI·Desktop 로컬 **만** | 스킬·커맨드·에이전트·훅(bash 게이트)·MCP. 방법론 ≈90%. **Web에는 전달 안 됨**(user scope 무시) |
| **T2** | `/moai:project` 스캐폴드 + **repo 커밋** | **CLI·Desktop·Web 전부** | T1 + CLAUDE.md 헌법 + rules + MoAI output-style 포인터 + `.moai` 체계 + **프로젝트 스코프 플러그인 선언**(웹에서 플러그인 자동 활성) |
| **T3** | + `moai` 바이너리 | CLI·Desktop 로컬 | + statusline·세션 레지스트리·harness 학습·spec audit·doctor·update |

v1 대비 변화: 구 "T0(클라우드=프롬프트 자산만)" 폐기. Web 지원은 세션 종류가 아니라 **repo 커밋 여부**가 결정한다. 따라서 Slim-Scaffold(D-2)의 산출물에 **프로젝트 `.claude/settings.json`의 마켓·플러그인 선언이 반드시 포함**되어야 하며, 이것이 스캐폴드의 신규 핵심 책무다.

## 4. 아키텍처 (v1 §5.1 개정)

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 1 — 플러그인 네이티브 (plugin name: "moai", 표기 "코더")   │
│  commands 13 (/moai:plan·run·sync…) · agents 7 · skills 28팩  │
│  · output-styles 3 (Δ1: P0-2 검증으로 네이티브 확정)            │
│  · hooks.json + dispatch.sh + gates/ · .mcp.json              │
│  · bin/moai-install(옵션) · templates/(Layer 2 페이로드 보관)   │
├──────────────────────────────────────────────────────────────┤
│ Layer 2 — 스캐폴드 페이로드 (templates/, /moai:project 가 생성)  │
│  CLAUDE.md · rules 61 (P0-1 FAIL로 스캐폴드 필수 확정)          │
│  · settings.project.json — outputStyle: "moai:MoAI"           │
│    + extraKnownMarketplaces(moai-claude) + enabledPlugins     │
│    ("moai@moai-claude": true)  ← Web 활성화의 열쇠              │
│  · .moai 골격 + config 29 + docs + project/db                 │
└──────────────────────────────────────────────────────────────┘
```

- **이름 설계**: `plugin.json { "name": "moai", "displayName": "코더", "version": <ADK SSOT> }` — 네임스페이스 파리티와 4-직원 브랜딩을 동시에 충족(D-1 확정의 구현 형태).
- output-styles는 Layer 1(플러그인)에 배치하고 스캐폴드는 `"outputStyle": "moai:MoAI"` 포인터만 기록(P0-2: 네임스페이스 셀렉터 필수, bare name은 무경고 무시).
- rules는 Layer 2 전용(P0-1: 플러그인 rules는 로드되지 않는 죽은 페이로드).

## 5. 컴포넌트 매핑 (v1 §5.2 갱신분만)

| 자산 | v1 | v2 확정 |
|---|---|---|
| output-styles 3 | Layer 2 스캐폴드 | **Layer 1 플러그인 네이티브** + 스캐폴드는 settings 포인터 1줄 |
| settings.project.json | 훅 등록 제거 + permissions/env 유지 | + **`extraKnownMarketplaces` + `enabledPlugins` 선언 추가**(Web 활성화) + `outputStyle: "moai:MoAI"` |
| 커맨드 스킬 참조 | `Skill("<ns>:moai")` 정규화 MUST | 비정규도 동작(P0-3) — 충돌 방어 SHOULD로 하향. 단 T3 공존 시나리오는 §8 검증 후 확정 |
| 나머지 (skills·agents·hooks·CLAUDE.md·rules·.moai) | v1 §5.2 | 변경 없음 |

## 6. 훅 설계 (v1 §5.4 보강)

- 단일 `dispatch.sh` + 순수 bash 게이트 5종 구조 유지.
- **Web 세션 분기**: `$CLAUDE_CODE_REMOTE=true`면 바이너리 프로브를 생략하고 게이트 전용 모드로 즉시 진입(바이너리 설치 불가 확정 환경에서 PATH 프로브 낭비 제거). 네트워크 egress 정책 하에서 외부 호출 게이트는 fail-open.
- `${CLAUDE_PLUGIN_DATA}`는 uninstall 시 소멸(P0-5) → 영속 상태는 프로젝트 `.moai/` 우선 원칙 유지.

## 7. 스캐폴드 설계 (v1 §5.5 보강 — Web 책무 추가)

- `scripts/scaffold.sh` 결정론 생성 + 백업 + user-owned 보존: 유지.
- **신규 책무**: 프로젝트 `.claude/settings.json`에 다음을 병합(기존 사용자 설정 보존 병합, 덮어쓰기 금지):
  ```json
  {
    "outputStyle": "moai:MoAI",
    "extraKnownMarketplaces": { "moai-claude": { "source": { "source": "github", "repo": "modu-ai/claude" } } },
    "enabledPlugins": { "moai@moai-claude": true }
  }
  ```
  이 파일이 repo에 커밋되면 Web/원격 세션에서도 플러그인·페르소나가 자동 활성화된다.
- 스캐폴드 완료 메시지에 Web 첫 세션 불안정(issue #63028: 마켓 clone이 세션 시작을 앞지르지 못하면 첫 클라우드 세션에서 inactive → 재접속 시 정상) 안내 문구 포함.
- 클라우드 폴백(구 T0 최소 세트 Write 생성)은 폐기 — Web은 T2 커밋 경로로 일원화.

## 8. 검증 항목 (P0 잔여 + 신규)

| 항목 | 내용 | 상태 |
|---|---|---|
| P0-6 | Desktop GUI 설치 E2E (+ → Plugins → moai-claude → `/reload-plugins`) | 사용자 수행 대기 |
| P0-7 → P0-w | **Web 실측으로 확장**: claude.ai/code에서 T2 커밋 repo 열기 → 플러그인 자동 활성(#63028 재현 여부)·훅 발화·outputStyle 적용·`$CLAUDE_CODE_REMOTE` 확인 | 사용자 수행 대기 (본 매트릭스 Web 열의 문서 기반 셀 확정) |
| P0-8 (신규) | **이름 충돌**: T3 프로젝트(프로젝트 커맨드 `/moai:plan` + 스킬 `moai`)와 플러그인(`moai:plan`·`moai:moai`) 공존 시 typed-name 충돌·우선순위 실측 → T3 승격 시 플러그인 비활성 안내 문구 확정 | 미실측 |

## 9. 개명 마이그레이션 계획 (moai-coder → moai)

1. `plugins/moai-coder/` → `plugins/moai/` 디렉토리 rename + `plugin.json` `{name: "moai", displayName: "코더"}`.
2. `.claude-plugin/marketplace.json`: 플러그인 엔트리 name/source 갱신. 마켓 배포 특성상 rename = 신규 플러그인 취급 → 기존 설치자(내부 사용자 위주)에게는 README·www에 1회 재설치 공지. 구명칭 tombstone 엔트리는 두지 않는다(카탈로그 오염 방지).
3. 참조 갱신: moai-pm 라우터(`coder-setup.md` 등)의 `moai-coder:` 참조, 4-README 설치 블록, www 카탈로그(G7과 병합 처리).
4. 버전: 개명 시점에 ADK 버전 SSOT로 재정렬(현 드리프트 G5 해소와 동시 수행).
5. `moai plugin export`(D-3)의 출력 대상 경로를 `plugins/moai/`로 고정 — parity-source 마커 체계 유지.

## 10. 로드맵 (v1 §7 갱신)

| 단계 | 내용 | 변경점 |
|---|---|---|
| **P0'** | 잔여 검증: P0-6 GUI · P0-w Web 실측 · P0-8 충돌 | P0-1~5 완료, Web 항목 확장 |
| **P1** | `moai plugin export` + parity manifest + CI job (moai-adk-go) | D-3·D-4 반영(ko 단일, vendor PR) |
| **P2** | **개명(§9)** + 2계층 재구조화(rules/output-styles 재배치, dispatch.sh 통합) + `scaffold.sh` + `/moai:project` 완성(**Web 선언 병합 포함**) | 개명·Web 책무 추가 |
| **P3** | T3 승격: doctor `plugin-deployed`(REQ-BD-007) + `bin/moai-install` + **P0-8 결과에 따른 플러그인 비활성 안내** | 충돌 처리 추가 |
| **P4** | 릴리스: 버전 SSOT 4-plugin 정렬, www 카탈로그·README(G7), 재설치 공지 | 개명 공지 추가 |

## 11. 리스크 갱신

- (해소) R2 스킬 참조 — P0-3 PASS로 하향. (해소) R7 agent 키 — P0-4 PASS, D-5 opt-in 설계로 관리.
- (신규) **R8 개명 단절**: 기존 moai-coder 설치자는 자동 마이그레이션 없음 → 재설치 공지 필요(사용자 기반 소규모, 영향 낮음).
- (신규) **R9 Web 문서 기반 셀**: Web 열의 훅·플러그인 동작은 공식 문서·커뮤니티 근거로, 본 머신 실측 불가 — P0-w 전까지 저신뢰. 설계는 실패해도 안전(fail-open, 선언은 무해한 JSON)하도록 구성됨.
- (신규) **R10 첫 세션 불안정(#63028)**: 스캐폴드 완료 메시지·README에 재접속 안내로 완화.

## Sources

- v1 보고서 Sources 6종 (code.claude.com/docs: plugins·plugin-marketplaces·discover-plugins·hooks-guide·desktop·skills)
- code.claude.com/docs/en/claude-code-on-the-web — Web 세션 repo-커밋 기반 로딩·샌드박스
- github.com/anthropics/claude-code issues #42142(Desktop /plugin 환각) · #63028(웹 첫 세션 플러그인 inactive) · #25086(settings.local.json enabledPlugins 무시)
- 본 저장소 P0 실측(v1 §9) + 사용자 제공 확장 메커니즘×환경 리서치 보고(2026-07-08, CC 2.1.204)
