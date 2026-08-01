# SPEC-MOC-PLUGIN-MOAI-V2-001 — 설계 (design)

> 본 문서는 설계 정본 `.moai/reports/design-moai-plugin-v2-2026-07-08.md`(이하 v2)와 원천 기록 `design-moai-adk-desktop-plugin-2026-07-08.md`(이하 v1)의 **증류본**이다. 상세·근거·출처는 원본을 인용하며 여기 재복사하지 않는다. 본 SPEC 범위(P2, 본 저장소)에 유효한 결정만 요약한다.

## §A. 확정 결정 레지스터 (v2 §1 — 전부 사용자 확정 2026-07-08)

| # | 결정 | 확정값 | 본 SPEC 반영 |
|---|---|---|---|
| D-1 | 플러그인 이름 | `moai` 개명 + `displayName: "코더"` (name=네임스페이스, displayName=UI 분리) | R1 / M1 |
| D-2 | 파리티 모델 | Slim-Scaffold — 프로젝트 귀속 자산만 스캐폴드, 프롬프트 자산은 플러그인 네이티브 | R2 / M2 |
| D-3 | 배포 원천 | 현행 vendor 유지 (export→CI→PR은 P1, Out of Scope) — 본 SPEC은 수동 vendor + parity-source 마커 | C-2 |
| D-4 | 언어 전략 | ko 단일 export | Out of Scope 항목 |
| D-5 | persona `agent` 키 | 기본 미동봉 + opt-in (P3 이후) | Out of Scope 항목 |

## §B. 환경 매트릭스 · 티어 모델 (v2 §2~§3 요약)

핵심 원리: **Web으로 갈수록 "repo에 커밋된 것만 동작"의 한 방향 감쇠.** Web 지원은 세션 종류가 아니라 **repo 커밋 여부**가 결정한다(구 T0 폐기).

| Tier | 조건 | 도달 환경 |
|---|---|---|
| T1 | 플러그인 설치(user scope) | CLI·Desktop 로컬만 (Web 전달 안 됨) |
| T2 | `/moai:project` 스캐폴드 + **repo 커밋** | **CLI·Desktop·Web 전부** — 프로젝트 settings.json의 마켓·플러그인 선언이 열쇠 |
| T3 | + `moai` 바이너리 | CLI·Desktop 로컬 (statusline·doctor 등 — P3) |

Web 열은 공식 문서·커뮤니티 근거의 **저신뢰 셀**(R9 — research.md §C). 설계는 실패해도 안전(fail-open, 무해한 JSON 선언).

## §C. 2계층 아키텍처 (v2 §4)

```
Layer 1 — 플러그인 네이티브 (name: "moai", 표기 "코더")
  commands 14 · agents 8 · skills 29팩 · output-styles 2 (P0-2 PASS → 네이티브 확정)
  · hooks.json + dispatch.sh + gates/ · .mcp.json · templates/(Layer 2 페이로드 보관)
Layer 2 — 스캐폴드 페이로드 (templates/, /moai:project 가 생성)
  CLAUDE.md · rules 61 (P0-1 FAIL → 스캐폴드 필수 확정)
  · settings.project.json — outputStyle "moai:MoAI" + extraKnownMarketplaces(moai-claude)
    + enabledPlugins("moai@moai-claude": true) ← Web 활성화의 열쇠
  · .moai 골격 (config sections ≥27, {{TOKEN}} 형태)
```

원칙: Claude Code가 플러그인에서 로드하는 것은 Layer 1에, 프로젝트에 있어야만 효력이 생기는 것은 Layer 2에. 중복 배치(현행 rules 루트 동봉 = 죽은 페이로드) 제거.

## §D. 컴포넌트 매핑 (v2 §5 + 2026-07-09 실측 보정)

| 자산 | 현행 (HEAD) | v2 목적지 |
|---|---|---|
| rules 61 | 플러그인 루트 `rules/moai/` (미로드) | `templates/claude/rules/moai/` (git mv, 내용 무변경) |
| output-styles | `output-styles/` 2파일 (moai.md `name: MoAI`, einstein.md) | 잔류 (Layer 1) — 문서상 3종이나 vendor는 2종, 추가는 P1 소관 |
| settings 페이로드 | 부재 | `templates/claude/settings.project.json` (3키 + permissions/env 축소판) |
| CLAUDE.md 페이로드 | 부재 | `templates/CLAUDE.md` (ADK 정본 vendor + parity-source, 루트 CLAUDE.md 복사 금지) |
| .moai 골격 | 부재 | `templates/moai/config/sections/` ≥27 yaml |
| hooks 24 스크립트 | handle-* 20 + 게이트 4 | dispatch.sh 1 + gates/ 4~5 |
| 커맨드 스킬 참조 | `Skill("moai")` ×13 | `Skill("moai:moai")` 정규화 (SHOULD — P0-3 PASS로 하향) |
| skills·agents·commands·.mcp.json | 현행 | 무변경 보존 (PRESERVE) |

## §E. 훅 설계 (v2 §6)

- `hooks.json`의 모든 이벤트(20종) → `${CLAUDE_PLUGIN_ROOT}/hooks/dispatch.sh <event>`.
- dispatch 로직(의사코드):
  1. `[ "$CLAUDE_CODE_REMOTE" = "true" ]` → 바이너리 프로브 **생략**, 게이트 전용 모드로 즉시 진입 (Web: 바이너리 설치 불가 확정 — 프로브 낭비 제거)
  2. `command -v moai` 성공 → `exec moai hook <event>` (T3 자동 활성)
  3. 이벤트→게이트 매핑 존재 → `hooks/gates/<gate>.sh` 실행
  4. 매핑 없음 → `exit 0` (무음 fail-open)
- 게이트 인벤토리: 기존 4종(iggda-audit-preservation-guard · status-transition-ownership · sync-phase-quality-gate · team-ac-verify) 이관 + gateguard-fact-force vendor(DP-2, SHOULD).
- 영속 상태: `${CLAUDE_PLUGIN_DATA}`는 uninstall 시 소멸(P0-5 부수 발견) → 영속 상태는 프로젝트 `.moai/` 우선 원칙 유지.
- 모든 종료 경로 `exit 0` — 블로킹 도입 금지(death-spiral 방지 계열).

## §F. 스캐폴드 설계 (v2 §7)

- `scripts/scaffold.sh`: cp + sed 단순 토큰 치환(`{{PROJECT_NAME}}`·`{{VERSION}}`·`{{DATE}}`), LLM 개별 파일 복사 금지(토큰·오류 절감). Go 조건문은 vendor 시점에 이미 해소된 상태를 전제.
- 멱등·안전: `--dry-run`(무기록 + 계획 출력), 기존 파일 `.moai-backups/` 백업 후 갱신, user-owned 네임스페이스(`harness-*`, `agents/local/`) 절대 보존 — `moai update`의 보존 규칙 이식.
- **신규 핵심 책무 (Web 열쇠)**: 프로젝트 `.claude/settings.json` **보존 병합** — `outputStyle: "moai:MoAI"` + `extraKnownMarketplaces.moai-claude`(github `modu-ai/claude`) + `enabledPlugins."moai@moai-claude": true`. 이 파일이 repo에 커밋되면 Web/원격 세션에서 플러그인·페르소나 자동 활성.
- 완료 메시지: Web 첫 세션 불안정(issue #63028 — 마켓 clone 지연 시 첫 클라우드 세션 inactive → 재접속 시 정상) 안내 포함.
- 클라우드 폴백(구 T0 최소 세트) 폐기 — Web은 T2 커밋 경로로 일원화.

## §G. 개명 설계 (v2 §9)

1. `git mv plugins/moai-coder plugins/moai` + `plugin.json {name: "moai", displayName: "코더", version: "1.0.0"}` (DP-1 확정).
2. marketplace.json 엔트리 name/source 갱신. **rename = 신규 플러그인 취급** → 자동 마이그레이션 없음(R8) → README 재설치 공지 1회. 톰스톤 엔트리 금지(카탈로그 오염 방지).
3. 참조 갱신: moai-pm 라우터(coder-setup.md 등 6파일) · moai-designer 스킬 2파일 · 4-README + 루트 README · www 카탈로그(plugins 섹션 한정, G7 병합 처리) · `.claude/agents/harness/` 1파일.
4. 버전: **`"1.0.0"` 리셋**(DP-1 사용자 확정 2026-07-09 — 개명 = 신규 플러그인 정체성, clean-slate 버저닝; v2 §9.4의 "ADK 버전 SSOT로 재정렬"안은 사용자 override로 대체). 전면 SSOT 정렬(G5)은 P4.
5. `moai plugin export`(P1)의 출력 경로는 `plugins/moai/`로 고정 예정 — parity-source 마커 체계 유지(본 SPEC은 마커 스탬프만).

## §H. 리스크 (v2 §11 발췌 — 본 SPEC 유효분)

- **R8 개명 단절**: 기존 moai-coder 설치자 자동 마이그레이션 없음 → 재설치 공지(AC-MV2-005d). 영향 낮음(사용자 기반 소규모).
- **R9 Web 문서 기반 셀**: Web 열 저신뢰 — P0-w(사용자 수행) 전까지. fail-open + 무해한 JSON 선언으로 실패-안전.
- **R10 첫 세션 불안정(#63028)**: 스캐폴드 완료 메시지 안내로 완화(AC-MV2-004f).
- (신규) **R11 T3 공존 충돌**: 본 저장소 같은 T3 프로젝트에서 플러그인 `moai`와 프로젝트 커맨드/스킬 `moai`의 typed-name 충돌 — P0-8 실측(AC-MV2-006c)으로 관찰, 대응 구현은 P3.

## §I. 참조

- v2: `.moai/reports/design-moai-plugin-v2-2026-07-08.md` (§1 결정, §2~3 매트릭스/티어, §4~7 아키텍처/훅/스캐폴드, §9 개명, §11 리스크)
- v1: `.moai/reports/design-moai-adk-desktop-plugin-2026-07-08.md` (§3 템플릿 인벤토리, §5.4~5.5 훅/스캐폴드 상세, §9 P0 실측)
- research.md §B~§E (P0 증거 + HEAD 실측 정본)
