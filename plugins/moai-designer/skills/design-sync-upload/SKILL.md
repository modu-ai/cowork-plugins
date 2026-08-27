---
name: design-sync-upload
description: |
  디자인 시스템 자산(DESIGN.md·토큰·로고)을 Claude Design에 업로드합니다. 자동 우선 + 수동 폴백 양경로.
  자동 경로는 DesignSync MCP로 바로 등록하며(`list/read` → `finalize_plan` → `write_files` 순서 강제, `register_assets`는 legacy) `/design-login` 인증이 필요합니다. 인증이 없거나 MCP가 없으면 수동 폴백으로 `UPLOAD-GUIDE.md` + 스테이징 자산 폴더를 산출해 사용자가 직접 업로드합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "Claude Design에 디자인 시스템 업로드"
  - "DesignSync로 자산 등록"
  - "DESIGN.md 업로드해 줘"
  - "디자인 시스템 자동 동기화"
  - "업로드 가이드 만들어 줘 (수동)"
  - "claude.ai/design에 올릴 자료 스테이징"
version: "1.3.0"
---

# design-sync-upload — Claude Design 업로드 (자동 + 수동 폴백)

## 개요

디자인 시스템 자산을 Claude Design에 올리는 방식은 환경에 따라 두 가지입니다. 이 스킬은 **자동(DesignSync MCP)을 먼저 시도**하고, 인증·가용성 조건이 안 되면 **수동 폴백(UPLOAD-GUIDE.md + 스테이징 폴더)**으로 자연스럽게 강등합니다. 어느 경로든 사용자가 손으로 파일을 흩뿌리지 않고 한 번에 업로드할 수 있게 만드는 것이 목표입니다.

> 이 SKILL.md는 인증 감지·자동(DesignSync MCP) 경로·수동 폴백·사용 예시를 모두 포함합니다. DesignSync는 `method`로 디스패치하는 단일 MCP 도구이며(파라미터 상세는 §자동 경로 참조), 미인증·미가용 시 조용히 수동 폴백으로 강등합니다.

## 트리거 키워드

Claude Design 업로드, DesignSync MCP, design-login, 디자인 시스템 동기화, UPLOAD-GUIDE, 자산 스테이징, write_files, register_assets

## 입력

| 입력 | 형태 |
|---|---|
| DESIGN.md | `design-system-prep` 산출물 |
| 토큰 | `design-tokens-transformer` 산출물(DTCG/CSS/shadcn) |
| 자산 | 로고 변형(가로/정사각/마스코트/WH), 폰트, 이미지 |

## 경로 선택 — 인증 감지 분기

```
자산 준비
  → [감지] DesignSync MCP 가용 AND /design-login 인증됨?
      ├─ YES → 자동 경로 (DesignSync MCP)
      └─ NO  → 수동 폴백 (UPLOAD-GUIDE.md + 스테이징 폴더)
```

**감지 신호**

| 신호 | 확인 방법 | 판정 |
|---|---|---|
| DesignSync MCP 도구 존재 | 현재 세션 도구 목록에 `DesignSync`가 로드됐는지 | 없음 → 즉시 수동 |
| `/design-login` 인증됨 | 무해한 read 메서드(`list_projects`) 호출 시 인증 에러 미발생 | 정상 반환 → 자동 가능 |
| 미인증 에러 시그니처 | 관측된 문자열: `DesignSync needs design-system authorization. Run /design-login to authorize it with your claude.ai account` | 이 문자열 감지 → 미인증 확정 → 수동 |

**감지 순서(부작용 최소화)**: ① 도구 존재만 사전 확인 → ② 무해한 read 메서드(`list_projects`/`get_project`)로 인증 상태 판별(쓰기 없음) → ③ 여기서 미인증 에러가 나오면 폴백. 쓰기 메서드로 인증을 떠보지 않는다(부분 업로드 위험).

**감지 실패 시 기본 강등 정책**: 감지 자체가 모호하면(도구는 있으나 인증 상태 불명, read 호출이 애매한 에러 반환 등) **수동 폴백을 기본값**으로 강등한다. 인증됨을 관측 없이 가정하고 자동을 강행하면 부분·중복 업로드 위험이 있으므로, 애매하면 항상 수동이다(미관측 상태를 성공으로 가정 금지).

## 자동 경로 — DesignSync MCP

`/design-login` 인증 상태에서 DesignSync MCP 도구로 자산을 직접 등록합니다.

DesignSync는 `method`로 디스패치하는 단일 도구다. 순서 의존성이 강제된다: **read → `finalize_plan` → write**. `finalize_plan`이 먼저 경로 집합을 잠근 뒤에야 write가 허용된다(플랜 밖 경로/planId 없는 write는 거부).

1. **read** (`list_projects`/`get_project`/`list_files`/`get_file`) — 대상 프로젝트 확인(쓰기 가능 + `type: PROJECT_TYPE_DESIGN_SYSTEM`) 후 원격 구조로 컴포넌트 단위 diff 구성. 전량 교체가 아니라 증분.
2. **승인 게이트 — `finalize_plan` 호출 전.** 아래 §쓰기·삭제 승인 게이트. `finalize_plan`이 띄우는 런타임 권한 프롬프트가 이 게이트를 대신하지 못한다 — 그 프롬프트는 **경로만** 보여주고 그 경로에 무엇이 들어가는지는 보여주지 않는다.
3. **`finalize_plan`** — 승인된 경로 집합(`writes`/`deletes`, 글롭 허용)과 읽기 소스 디렉토리(`localDir`)를 확정 → `planId` 반환. 권한 프롬프트 발생.
4. **`write_files`** (+ `delete_files`) — `planId`로 파일 업로드. 각 파일은 `localPath`(디스크에서 직접 읽어 업로드 — 내용이 컨텍스트에 유입되지 않음, 권장) 또는 소량 인라인 `data`. 콜당 최대 256개(초과 시 같은 `planId`로 분할).
5. **`register_assets`** (레거시) — Design System 카드는 이제 preview HTML 첫 줄 `<!-- @dsCard group="…" -->` 마커에서 자동 인덱싱(앱이 `_ds_manifest.json`으로 컴파일)되므로 명시 등록 불필요. `@dsCard` 마커가 없는 수기 프로젝트에서만 사용.

**각 메서드 파라미터 스키마 (핵심 필드)**

| 메서드 | 필수 | 주요 파라미터 | 비고 |
|---|---|---|---|
| `finalize_plan` | — | `projectId`, `writes[]`(글롭, 최대 256), `deletes[]`, `localDir`(기본 cwd) | `planId` 반환. 사용자에게 경로 목록·소스 디렉토리 노출 |
| `write_files` | `planId` | `projectId`, `files[]`={`path`, `localPath`\|`data`, `mimeType`} | `localPath`는 `localDir` 안이어야 함. 콜당 256개 |
| `delete_files` | `planId` | `projectId`, `paths[]` | 플랜의 `deletes`에 포함된 경로만 |
| `register_assets`(레거시) | `planId` | `assets[]`={`name`, `path`, `group`, `viewport`, `subtitle`} | `path`는 플랜의 `writes`에 포함돼야 함 |
| `create_project` | — | `name` | `list_projects`가 비었거나 사용자가 신규 선택 시 |

**순서 의존성**: read → **승인 게이트** → `finalize_plan`(planId 발급) → `write_files`/`delete_files` → (필요 시) `register_assets`. planId 없이, 또는 플랜 밖 경로로 write/delete/register 호출 시 거부된다.

### 쓰기·삭제 승인 게이트

원격 디자인 시스템은 **다른 사람이 쓰고 있는 공용 자산**이다. 덮어쓴 파일의 이전 내용과 지운 파일은 원격에 남지 않는다 — 이 MCP에는 원자적 롤백이 없다(아래 §부분 실패 정책). 그래서 `finalize_plan`으로 경로를 잠그기 전에 멈춘다.

- **[HARD] 승인은 §승인 요청 계약의 경로로 받는다.** `finalize_plan`의 런타임 권한 프롬프트로 갈음하지 않는다 — 그 프롬프트는 경로 목록만 보여주고 digest·의미 diff·스냅샷 위치를 보여주지 않는다. 그 프롬프트는 경로 목록과 소스 디렉토리만 노출하며, `localPath` 경로는 **내용이 컨텍스트에 유입되지 않는 것이 설계 의도**이므로 사용자는 무엇이 덮어써지는지 보지 못한 채 승인하게 된다.
- **[HARD] 글롭은 승인 전에 펼쳐서 보여준다.** `writes[]`/`deletes[]`는 글롭을 허용한다. 펼치지 않은 글롭은 사용자가 의도한 것보다 훨씬 많이 매치될 수 있고, 그 차이는 승인 시점에 보이지 않는다. **실제로 매치된 경로를 하나씩 나열**하고 개수를 함께 적는다.
- **[HARD] 요약하지 말고 다음을 그대로 보여준다:**

| 보여줄 것 | 왜 필요한가 |
|---|---|
| 대상 프로젝트 이름·ID·타입 | 엉뚱한 프로젝트에 쓰는 사고를 막는다 |
| 펼친 경로 목록 — **신규 / 덮어쓰기** 구분 | 신규는 잃을 것이 없고, 덮어쓰기는 있다 |
| **삭제 경로 목록** (별도 구획) | 가장 되돌리기 어려운 항목이라 섞지 않는다 |
| 파일별 크기와 **digest(해시)** — 선택이 아니라 필수 | 내용을 못 봐도 규모와 동일성은 확인된다. `planId`가 잠그는 것은 **경로**뿐이므로, 내용을 묶는 것은 이 digest다 |
| 덮어쓰기 대상의 **의미 diff 요약** | 아래 규칙 참조 |
| **사본 없음 고지** | 이 작업으로 사라지는 내용은 복구되지 않는다는 사실 |

- **[HARD] 이 MCP에는 안전한 복구 스냅샷 수단이 없다. 스킬이 대신 만들지 않는다.** 원격 내용을 가져오는 유일한 경로는 `get_file`인데, 그 응답은 **모델 컨텍스트를 통과한다.** 자격증명·고객 자산·미공개 디자인이 섞여 있어도 그대로 지나가며, 받아 놓은 로컬 사본에는 권한·보존 기간·저장소 제외 규칙이 없다. **백업을 만들려다 유출 경로를 만드는 것이 더 나쁘다.**
- **[HARD] 대신 사용자에게 사실을 알린다.** 덮어쓰거나 지울 경로 목록을 보여주면서 **"이 파일들의 현재 내용은 이 작업으로 사라지며, 스킬은 사본을 만들지 않는다"** 고 명시한다. 사본이 필요하면 사용자가 직접 내려받은 뒤 진행하도록 안내한다.
- **대상은 덮어쓰기·삭제 경로뿐이다.** 신규 경로는 잃을 것이 없으므로 이 안내에서 뺀다 — 신규와 덮어쓰기를 나눠 보여주는 이유가 이것이다.
- 나중에 서버가 **내용을 응답하지 않고 제한 권한 디렉터리로 직접 내보내는** 기능을 제공하면 그때 자동 스냅샷을 다시 논한다. 그 전에는 **"복구 사본을 받아 둡니다"라고 약속하지 않는다.**
- **[HARD] 의미 diff를 만들려고 원격 원문을 가져오지 않는다.** 내용 대조를 하려면 `get_file`로 원격 전체를 받아야 하는데, 그것이 바로 위에서 막은 유출 경로다. 승인 화면에는 **원문 없이 알 수 있는 것만** 적는다 — 경로, 신규/덮어쓰기 구분, 로컬 파일의 크기와 digest, 삭제 대상.
- 내용 수준의 diff가 꼭 필요하면 **사용자가 직접 받아 둔 사본을 건네줄 때만** 만든다. 스킬이 원격에서 끌어오지 않는다.

승인 선택지는 이렇게 구성한다:

| 선택지 | 뜻 |
|---|---|
| 이 매니페스트대로 실행 (권장) | 보여준 경로 집합 그대로 `finalize_plan` → write/delete |
| 삭제는 빼고 쓰기만 | `deletes[]`를 비우고 플랜을 다시 수립 |
| 경로 좁히기 | 매니페스트를 줄여 게이트를 다시 |
| 취소 | `finalize_plan`을 호출하지 않고 종료. 원격 변경 없음 |

- **[HARD] `planId`는 승인된 그 매니페스트에 묶인다.** 승인 뒤 경로를 추가하거나 글롭을 넓히려면 **재승인**을 받고 `finalize_plan`을 다시 실행한다. 기존 `planId`에 슬쩍 얹지 않는다.
- **[HARD] `write_files` 직전에 digest를 다시 계산해 승인 시점 값과 대조한다.** `write_files`는 승인 뒤 `localPath`를 **다시 읽는다** — 승인과 업로드 사이에 파일이 바뀌면 사용자가 승인한 적 없는 내용이 같은 경로로 올라간다. 동시 편집·빌드 산출물 갱신·파일 교체가 실제로 일어나는 구간이다.
- **하나라도 어긋나면 그 `planId`를 폐기하고 재승인을 받는다.** 어긋난 파일만 빼고 진행하지 않는다 — 무엇이 왜 바뀌었는지 모르는 상태이기 때문이다.
- **[HARD] 이 대조는 창을 좁힐 뿐 닫지 못한다. 그 한계를 사용자에게 숨기지 않는다.** `write_files` 스키마에는 `expectedDigest`가 없고, 서버가 파일을 여는 시점은 스킬이 해시를 잰 **뒤**다. 그 사이에 파일이 바뀌면 막을 방법이 현재 계약에는 없다. 따라서 **"승인한 바이트가 그대로 올라간다"고 보증하지 않는다** — 보증하는 것은 "직전까지 바뀐 흔적이 없었다"까지다.
- **창을 좁히는 실무**: digest 재계산과 `write_files` 호출 **사이에 다른 작업을 끼우지 않는다.** 빌드·포맷터·동기화 도구가 도는 중이면 끝난 뒤에 시작한다. 승인 화면에서 업로드까지의 시간이 길어질수록 위험이 커진다.
- 서버가 `expectedDigest`를 받아 파일을 연 직후 검증하는 기능을 제공하면 그때 보증 수준을 올린다. **없는 기능을 전제로 계약을 쓰지 않는다.**
- **[HARD] 삭제는 쓰기와 같은 승인으로 묶지 않는다.** 위 선택지에 "삭제는 빼고 쓰기만"을 항상 넣어, 삭제만 따로 거부할 수 있게 한다. 쓰기를 승인받으려고 삭제를 함께 통과시키는 형태가 되지 않게 한다.

**부분 실패 재시도/롤백 정책**

- `write_files` 실패: 같은 경로 덮어쓰기는 멱등이므로 최대 3회 재시도. 계속 실패하면 이미 기록된 파일을 사용자에게 고지하고 폴백.
- 256개 초과 분할 중 일부 실패: 실패 배치만 재시도, 성공 배치는 유지(같은 `planId`).
- MCP는 원자적 롤백을 제공하지 않음 → 부분 기록 상태를 **가짜 완료로 보고 금지**. 남은 파일만 이어서 쓰거나 수동 폴백으로 넘긴다(부작용 있는 호출은 상태 확인 후 재개 — 중복 업로드 방지).

**에러 → 폴백 전환 조건**

| 에러 | 전환 |
|---|---|
| 미인증 문자열(위 시그니처) | 자동 포기 → 즉시 수동 폴백 |
| `DesignSync` 도구 미로드 | 수동 폴백 |
| `write_files` 3회 재시도 후 실패 | 수동 폴백(부분 기록 시 사용자 고지) |
| 네트워크·일시 에러 | 재시도 후 성공하면 자동 유지 |
| planId 만료/플랜 밖 경로 거부 | `finalize_plan` 재실행으로 플랜 재수립 |

## 승인 요청 계약 (런타임 중립)

[HARD] 이 스킬의 게이트는 **특정 도구 이름에 묶이지 않는다.** `AskUserQuestion`은 Claude 런타임의 수단일 뿐이고, Codex를 비롯한 다른 런타임에는 그 도구가 없다. 도구 이름으로 계약을 쓰면 그 도구가 없는 런타임에서 게이트가 **영구 blocker**가 되어, 승인이 필요한 모든 작업이 그냥 멈춘다. 그건 안전이 아니라 고장이다.

승인은 아래 순서로 구한다. 위에서부터 **실제로 가능한 첫 번째**를 쓴다.

**승인의 정의는 수단이 아니라 결과다: 승인서를 사용자에게 그대로 보여주고, 그에 대한 명시적 응답을 받는 것.** 아래는 그 결과를 만드는 경로들이며, 위에서부터 가능한 첫 번째를 쓴다.

| 순위 | 경로 | 조건 |
|---|---|---|
| 1 | 런타임의 구조화 질문 도구 (`AskUserQuestion` 등) | 그 도구가 현재 세션에 노출돼 있을 때 |
| 2 | **일반 대화로 승인서를 제시하고 다음 턴에서 응답을 받는다** | 사용자와 직접 대화 중일 때. 도구가 없어도 이 경로는 언제나 열려 있다 |
| 3 | 구조화 blocker 반환 → 상위 오케스트레이터가 물어봄 | 서브에이전트로 실행 중일 때 |

**[HARD] 런타임의 도구 실행 권한 프롬프트는 승인이 아니다.** 그 프롬프트는 "이 도구를 호출해도 되는가"를 물을 뿐, 게이트가 보여주기로 한 인자·견적·동의 문항을 표시하지 않는다. 승인서 전체와 선택지를 실제로 표시하는 경우에만 2번 경로로 인정한다.

**[HARD] 2번 경로가 있으므로 "물을 수단이 없다"는 상황은 사실상 없다.** 대화가 가능한 곳에서는 언제나 승인서를 글로 제시할 수 있다. fail-closed는 **대화도 blocker 반환도 불가능한 완전 무인 실행**에만 해당한다 — 그 경우에만 실행하지 않고 멈춘다.

**[HARD] 3번을 쓸 때 blocker는 그 자체로 승인 요청서여야 한다.** 상위가 무엇을 물어야 할지 모르면 되물을 수 없고, 그러면 교착된다. 다음을 모두 담는다:

- 승인받을 **행위** 한 줄 (무엇이 되돌릴 수 없는지 / 얼마가 나가는지)
- 게이트가 요구하는 **인자 전부** (요약하지 않은 값)
- **선택지 목록** — 상위가 그대로 사용자에게 제시할 수 있는 형태
- **재개 방법** — 어떤 답을 받으면 무엇을 이어서 실행하는지

**[HARD] 세 경로가 모두 불가능한 무인 실행에서는 실행하지 않는다(fail-closed).** 물을 수단이 없다는 것은 승인을 받았다는 뜻이 아니다. 이때는 "승인 수단이 없어 진행하지 못했다"고 기록하고 멈춘다 — 조용히 진행하지 않는다. 반대로 **대화가 가능한데 도구가 없다는 이유로 멈추는 것도 잘못**이다. 2번 경로를 쓴다.

> 이 계약은 `CLAUDE.local.md` §범용성 원칙(OS 2종 × 런타임 2종에서 동일 동작)의 게이트 쪽 적용이다. 한 런타임에서만 도는 게이트는 미완성으로 본다.

---

## 수동 폴백 — UPLOAD-GUIDE.md + 스테이징 폴더

MCP가 없거나 미인증이면 사용자가 직접 업로드할 수 있는 산출물을 만듭니다.

1. **스테이징 폴더 구성** — 기본 `./design-sync-staging/`에 DESIGN.md + 토큰 + 정리된 자산 사본 배치
2. **UPLOAD-GUIDE.md 생성** — 업로드 우선순위·주의사항·Published 토글 절차 기재
3. **사용자 안내** — 폴더 전체를 claude.ai/design에 업로드하도록 지시

```markdown
## Claude Design 업로드 가이드 (수동)

### 업로드 우선순위
1. DESIGN.md — 가장 먼저
2. 토큰 세트(DTCG/CSS/shadcn)
3. 로고 변형(SVG 우선)
4. 참고 자산

### 주의
- 모노레포 전체 X → 정리된 폴더만
- 민감 자산(고객 데이터·매출) 익명화 후 업로드
- 폰트 라이선스 확인

### Published 토글
1. 업로드 후 5-15분 대기(분석)
2. 테스트 프롬프트로 검증
3. 브랜드 일치 시 Published ON, 어긋나면 Remix
```

**스테이징 폴더 레이아웃**

```
./design-sync-staging/
├── DESIGN.md                    # 최우선
├── tokens/
│   ├── 02-tokens.json           # L1 DTCG SSOT
│   ├── colors_and_type.css      # L2 원시 CSS 변수
│   └── globals.css              # L3 semantic/shadcn + .dark
├── assets/
│   ├── logo/                    # 로고 변형(아래 매트릭스)
│   ├── fonts/                   # 라이선스 확인된 폰트
│   └── reference/               # 참고 이미지·캡처
└── UPLOAD-GUIDE.md              # 업로드 절차
```

**UPLOAD-GUIDE.md 완전 템플릿**

```markdown
# Claude Design 업로드 가이드 (수동)

## 업로드 순서
1. DESIGN.md — 가장 먼저(디자인 시스템 요약)
2. tokens/ — L1 DTCG → L2 CSS → L3 globals.css 순
3. assets/logo/ — 변형별(가로/정사각/마스코트/화이트 녹아웃)
4. assets/fonts/ — 라이선스 확인된 것만
5. assets/reference/ — 톤 비교용 참고 자산

## 업로드 방법
1. claude.ai/design 진입 → Organization settings → Design systems
2. 위 폴더를 통째로 업로드(모노레포 전체 X)
3. `/design-login` 후 Claude Code 터미널이면 다음부터 자동 경로 사용 가능

## 주의
- 민감 자산(고객 데이터·매출 박힌 덱)은 익명화 후 업로드
- 폰트 라이선스 확인 — 불명 자산 제외
- 누락된 로고 변형은 "미제공"으로 표기(임의 생성 금지)

## Published 토글
1. 업로드 후 분석 대기(5–15분)
2. 테스트 프롬프트로 검증("마케팅 랜딩 페이지 디자인해 줘" 등)
3. 브랜드 일치 → Published ON / 어긋나면 Remix 또는 자산 추가
```

**자산 변형 매트릭스 매핑 규칙**

| 변형 | 파일명 규칙(예) | 의도된 용도 |
|---|---|---|
| 가로형(horizontal) | `logo-horizontal.*` | 헤더·네비 — 가로 여백이 확보된 곳 |
| 정사각(square) | `logo-square.*` | 파비콘·앱 아이콘·소셜 프로필 |
| 마스코트(mascot) | `mascot.*` | 히어로·엠프티·404 (정서 영역 한정) |
| 화이트 녹아웃(white-knockout) | `logo-*-WH.*` | 어두운/그라디언트 배경 위 단색 화이트 |

매핑 규칙: 원본 로고를 위 4변형으로 분류하고 각 변형에 용도 태그를 부여해 UPLOAD-GUIDE.md에 명시한다 — 업로드 후 Claude Design이 문맥별로 올바른 변형을 고르게 하기 위함. 제공되지 않은 변형은 "미제공"으로 표기하고 임의 생성하지 않는다.

## 출력 형식

```
## Claude Design 업로드 [자동 / 수동]

### 경로
- 선택: 자동(DesignSync MCP) / 수동 폴백
- 사유: [인증 상태 / MCP 가용성]

### (자동) 등록 결과
- finalize_plan: planId 발급 / writes N · deletes N
- write_files: N개 (localPath 업로드)
- register_assets: (레거시) @dsCard 자동 인덱싱 또는 N개 수동

### (수동) 산출물
- ./design-sync-staging/  (DESIGN.md + 토큰 + 자산 N개)
- ./design-sync-staging/UPLOAD-GUIDE.md

### 다음 단계
- (자동) 5-15분 분석 대기 → 테스트 프롬프트 → Published 토글
- (수동) 폴더 업로드 → 위 가이드 따라 진행
```

## 사용 예시

**예시 1 — 인증됨 → 자동 등록**

```
사전: DesignSync MCP 로드됨 + list_projects 정상 반환(인증됨)
동작: finalize_plan(writes=DESIGN.md+토큰+로고, localDir=./staging)
      → write_files(planId, localPath로 8개) → (@dsCard 자동 인덱싱)
출력: 자동 등록 완료 → 분석 대기
보고: finalize_plan planId 발급, write_files 8, 카드 자동 인덱싱
```

**예시 2 — 미인증 → 수동 스테이징**

```
사전: list_projects 호출 시 "DesignSync needs design-system authorization. Run
      /design-login to authorize it with your claude.ai account" 에러
동작: 자동 포기 → ./design-sync-staging/ 구성 + UPLOAD-GUIDE.md 생성
출력: 스테이징 폴더(DESIGN.md + tokens/ + assets/) + 가이드
안내: 폴더째 claude.ai/design 업로드. /design-login 하면 다음엔 자동 경로
```

**예시 3 — 자동 시작 후 에러 → 폴백 전환**

```
사전: 인증됨으로 자동 시작
동작: finalize_plan OK → write_files 진행 중 5개 중 2개 반복 실패
전환: 실패 배치 3회 재시도 후에도 실패 → 부분 기록 상태 고지 → 남은 자산 수동 스테이징
출력: (자동 부분: write_files 3개 완료) + (수동: 실패 2개 스테이징 + 재개 안내)
보고: 부분 성공을 완료로 보고하지 않음 — 미기록 파일 명시, 중복 방지 재개 안내
```

## 주의사항

### Do

- 자동을 먼저 시도하고, 조건 미달 시 조용히 수동으로 강등 — 사용자 작업 흐름을 끊지 않음
- 수동 폴백에서도 사용자가 손으로 파일을 흩뿌리지 않도록 폴더를 완결적으로 구성
- 민감 자산은 업로드 전 익명화 안내

### Don't

- `/design-login` 미인증 상태에서 자동 경로 강행 금지 — 즉시 수동 폴백
- 자동 부분 성공을 완료로 보고 금지 — `finalize_plan`까지 확정돼야 완료
- 폰트 라이선스 미확인 자산을 업로드 세트에 포함 금지

## 관련 스킬

| 스킬 | 사용 시점 |
|---|---|
| `moai-designer:design-system-prep` | 선행: DESIGN.md 합성 |
| `moai-designer:design-tokens-transformer` | 선행: 업로드할 3계층 토큰 생성 |
| `moai-designer:design-handoff` | 대안: 핸드오프 패키지가 산출물일 때 |
| `moai-designer:design-handoff-reader` | 역방향: Claude Design → Claude Code 인계 분석 |
