# update-protocol.md — 플러그인 업데이트 동기화 프로토콜 (project 스킬)

## 개요

`/project --update`의 상세 정본이다. 외부에서 AI 직원 플러그인이 업데이트된 직후, 프로젝트(`CLAUDE.md` + `.claude/agents/` + `.moai/config.json` 스냅샷)를 **최신 설치 인벤토리에 동기화**한다.

project 스킬 SKILL.md의 §Recursive Self-Improvement가 정의하는 `inventory drift` 트리거를 "감지 대기"가 아니라 **즉시·전수조사로 강제 실행**하는 모드다. 따라서 자가 개선의 진단→최소 diff→검증→롤백 사이클과 가드레일을 그대로 계승하며, 본 프로토콜은 그중 **드리프트 동기화 특화 절차**만 다룬다.

**`evolve` vs `--update` 재확인** — `/project evolve`는 사용 중 신호(`repeated correction`·`chain failure`)가 `.moai/evolution/signals.md`에 누적되어 발동하지만, `/project --update`는 사용자가 **수동으로** 호출해 drift를 기다리지 않고 즉시 전수조사한다. 둘은 같은 자가 개선 파이프라인의 서로 다른 진입점이다.

---

## 1. 발동 전 검문 (HARD)

`--update` 절차에 들어가기 전 반드시 확인한다.

1. **프로젝트 존재 여부** — `./CLAUDE.md` 또는 `./.moai/config.json`이 없으면 동기화 대상이 없다.
   - 침묵 생성 금지. `AskUserQuestion`으로 `/project`(최초 셋업)로 안내한다.
   - 옵션: `/project 시작으로 안내` / `--update 중단`.
2. **스냅샷 존재 여부** — `.moai/config.json`에 `plugins_installed` + `skills_available` 스냅샷이 없으면(최초 셋업 직후 미저장 등), 현재 인벤토리를 그대로 최초 스냅샷으로 저장하고 "이미 최신 상태"로 보고한다(비교 기준이 없으므로 diff는 공집합).
3. **진입 발화 인자** — `/project --update` 외 추가 자연어 지시가 있으면 1줄 요약으로 `context.md`에 누적한다(인터뷰는 생략 — `--update`는 맥락 수집이 아니라 동기화가 목적).

검문 1에서 중단이 아니면 §2로 진입한다.

---

## 2. Full Census (전수조사)

설치된 전체 플러그인을 조사해 기존 스냅샷과 비교, **diff(추가·변경·제거 스킬/MCP)**를 도출한다. §Plugin Inventory Scan(SKILL.md)의 2소스 교차 검증을 확장한다.

### 2-1. 인벤토리 수집 (3소스 교차)

```bash
# 소스 A: 디렉터리 스캔 — 플러그인 + 각 플러그인의 skills/ + plugin.json
for dir in ~/.claude/plugins/moai-*; do
  [ -d "$dir" ] && [ -f "$dir/.claude-plugin/plugin.json" ] || continue
  echo "### $(basename "$dir")"
  # 스킬: skills/*/SKILL.md 의 frontmatter name
  for skill in "$dir"/skills/*/SKILL.md; do
    [ -f "$skill" ] && grep -m1 '^name:' "$skill" | sed 's/name: */  - /'
  done
done

# 소스 B: MCP 정의 — 각 플러그인의 .mcp.json 또는 plugin.json 의 mcpServers
for dir in ~/.claude/plugins/moai-*; do
  [ -f "$dir/.mcp.json" ] && echo "MCP: $(basename "$dir")" && grep -oE '"[^"]+":' "$dir/.mcp.json"
done

# 소스 C: 현재 세션 system reminder의 "user-invocable skills" 목록(moai-* 접두만)
```

3소스를 교차 검증해 `new_inventory`를 구성한다(신뢰도 HIGH = 2소스 이상 일치 / MEDIUM = 단일 소스).

### 2-2. diff 도출

`new_inventory`를 `.moai/config.json`의 스냅샷과 비교해 세 가지 diff를 만든다:

| 분류 | 조건 | 동기화 우선순위 |
|---|---|---|
| **추가(added)** | 스냅샷에 없는 새 스킬/MCP | 높음 — 워크플로우 표·체인 후보에 반영 |
| **변경(changed)** | 같은 name이지만 버전/설명이 다른 스킬 | 중간 — 체인 본문이 구버전 시그니처를 참조하면 갱신 |
| **제거(removed)** | 스냅샷에는 있으나 인벤토리에 없는 스킬 | 높음 — CLAUDE.md·에이전트가 더 이상 존재하지 않는 스킬을 호출하면 안 됨 |

diff가 공집합이면 "이미 최신 상태"로 보고하고 종료한다(스냅샷 리셋만 수행).

---

## 3. 세션 신호 분석 (재귀적 자가 학습 입력)

"기존 대화 세션을 분석"하는 실체 절차다. 트랜스크립트 전체를 뒤지는 게 아니라 **영속화된 신호 파일**을 읽는다 — 세션이 바뀌어도 유실되지 않는다.

1. **`.moai/evolution/signals.md` 읽기** — 누적된 `repeated correction`·`chain failure` 신호를 최근 순으로 스캔.
2. **`.moai/context.md` 읽기** — 프로젝트 맥락(목적·주요 산출물·톤·금지 사항) 재확보.
3. **교차 매칭** — §2-2의 diff와 신호를 교차:
   - **추가된 스킬이 기존 `chain failure` 신호를 해소할 수 있는가?** → 그 스킬을 관련 체인에 편입(우선 동기화).
   - **제거된 스킬에 대해 과거 `repeated correction`이 있었는가?** → 이미 쓰지 않는 스킬이면 안전 제거.
4. 매칭 결과를 `.moai/evolution/` 진단 기록에 1줄로 남긴다(`날짜 | --update | 대상 | 신호-스킬 매칭 요지`).

신호 파일이 비어 있어도 정상이다 — 이 경우 §2 diff만으로 동기화를 진행한다.

---

## 4. CLAUDE.md·에이전트 동기화 (최소 diff)

diff에 맞춰 프로젝트 산출물을 갱신한다. **전면 재작성 금지** — 최소 diff 원칙(SKILL.md §Recursive Self-Improvement).

### 4-1. CLAUDE.md

- **워크플로우 표** — 추가된 스킬을 적합한 산출물 행에 편성, 제거된 스킬 행은 삭제 또는 대체 스킬로 교체.
- **200라인 예산 준수** — 갱신 후 `wc -l`로 재검증. 초과 시 스킬 체인 나열만 축소(HARD 블록 8개는 절대 축소·삭제하지 않는다 — `claudemd-generator.md` §5).
- **diff 적용 전 원문 조각 보존** — 수정 지점의 원문을 `.moai/evolution/`에 남겨 롤백 가능 상태를 유지.

### 4-2. `.claude/agents/*.md`

- 추가된 스킬을 호출하는 에이전트 본문의 체인을 갱신(7-step 루프의 ④ 실행 계획 단계).
- 제거된 스킬을 참조하는 에이전트는 대체 스킬로 재배선 — 참조가 끊긴 체인을 방치하지 않는다.
- frontmatter `tools` 최소 권한 원칙 유지(`Agent` 툴 포함 금지).

### 4-3. 파괴적 변경 (사전 확인)

제거된 스킬로 인해 **에이전트 1개 이상을 통째로 폐기**해야 하거나, CLAUDE.md HARD 블록 외의 섹션을 재구조해야 하는 경우 — 적용 전 `AskUserQuestion`으로 1-3줄 요지를 보고하고 승인받는다. 비파괴적 최소 diff는 보고 후 적용한다.

---

## 5. 스냅샷 갱신 + evolution-log

1. **스냅샷 리셋** — `.moai/config.json`의 `plugins_installed` + `skills_available`을 `new_inventory`로 갱신. 이로써 `inventory drift`는 0이 된다(다음 drift 감지의 새 기준).
2. **evolution-log 기록** — `CLAUDE.md` 말미 `<!-- evolution-log -->`에 1줄 추가:
   - 형식: `inventory drift | --update | <추가 N / 변경 N / 제거 N> | <신호-매칭 요지>`
3. **evolution-log 큐레이션** — 최근 10건 유지, 초과분은 `.moai/evolution/log.md`로 이관(SKILL.md §Recursive Self-Improvement 큐레이션 규칙).

---

## 6. 검증 + 롤백 (HARD)

동기화는 적용으로 끝나지 않는다 — 적용 이후 **같은 `inventory drift` 트리거**의 신호가 다시 발동하면 그 동기화는 **실패**로 판정한다.

- **실패 판정 시**: `.moai/evolution/`에 남긴 원문 조각으로 §4 diff를 되돌린다.
- **재시도 금지**: 같은 지점을 자동으로 재동기화하지 않는다 — 사용자에게 상황을 1-3줄로 보고하고 방향을 확인받는다(동일 지점 자동 재수정 반복 금지).
- **성공 판정 기준**: 다음 세션 진입 시 `inventory drift` 신호가 발동하지 않으면 성공으로 확정.

---

## 가드레일 (HARD — SKILL.md §Recursive Self-Improvement 계승)

- **수정 대상**: `CLAUDE.md`와 `.claude/agents/` 파일만. `.moai/evolution/`·`.moai/config.json`의 진단·스냅샷 기록은 예외. **스킬 본문·플러그인 파일은 건드리지 않는다.**
- **1회 동기화당 수정 파일 상한**: 최대 3개(evolution 기록 파일은 카운트 제외). diff가 상한을 넘으면 우선순위(추가 > 제거 > 변경)로 나눠 여러 번에 걸쳐 적용한다.
- **파괴적 변경**: 사전 확인 없이 적용하지 않는다(§4-3).
- **Desktop Parity**: hooks·LSP·output-styles는 생성하지 않는다(SKILL.md §Desktop Parity Constraints).

---

## 관련 파일

| 파일 | 역할 |
|------|------|
| `.moai/config.json` | `plugins_installed` + `skills_available` 스냅샷 — diff 비교 기준이자 갱신 대상 |
| `.moai/context.md` | 프로젝트 맥락 — §3 세션 신호 분석 입력 |
| `.moai/evolution/signals.md` | 누적 교정·체인 실패 신호 — §3 세션 신호 분석 입력 |
| `.moai/evolution/log.md` | evolution-log 이관 대상(10건 초과분) |
| `./CLAUDE.md` | 워크플로우 표·HARD 블록 — §4-1 동기화 대상 |
| `./.claude/agents/*.md` | 스킬 체인 에이전트 — §4-2 동기화 대상 |

---

## 교차 참조

- SKILL.md §Recursive Self-Improvement — 자가 개선 사이클·검증·롤백·가드레일 정본
- SKILL.md §Plugin Inventory Scan — 2소스 교차 검증 베이스(본 프로토콜 §2-1이 확장)
- `init-protocol.md` — 인터뷰·인벤토리 스캔·Gap Detection(최초 셋업 절차)
- `claudemd-generator.md` — CLAUDE.md 200라인 예산·8 HARD 블록 보존 정책
- `diagnostic-protocol.md` — `/project status`로 동기화 결과를 확인하는 진단 경로
