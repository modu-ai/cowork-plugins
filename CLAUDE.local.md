# CLAUDE.local.md — cowork-plugins 저장소 로컬 지침

이 파일은 이 저장소에서 Claude Code가 작업할 때 반드시 지켜야 할 로컬 규칙입니다.

---

## 1. 버저닝 정책 (HARD)

**단일 진실 원칙**: cowork-plugins 저장소의 모든 버전 표기는 **완전히 동일**해야 합니다.

### v2.0.0 변경: SKILL.md frontmatter `version` 필드 복구 (Cowork 자동 업데이트 지원)

v2.0.0부터 **모든 SKILL.md frontmatter에 `version: X.Y.Z` 단일 필드를 의무화**합니다. Cowork(Claude Cowork)가 SKILL.md `version` 필드를 보고 사용자 측 자동 업데이트를 감지합니다.

> **v2.1.0 카운트 갱신**: 마켓플레이스 SKILL.md 106 → **107**개 (humanize-korean 추가). 동기화 지점 총 **129개** (marketplace 1 + plugin.json 21 + SKILL.md 107).

- **이전 정책(v1.3.0~v1.8.x)**: `metadata:` 블록 전체 제거 + plugin.json 단일 소스 → 자동 업데이트 미작동
- **새 정책(v2.0.0+)**: SKILL.md `version` 단일 필드 필수 + `metadata:` 블록(중첩 객체)은 여전히 금지

### 동기화 대상 (총 129개 지점, v2.1.0 기준)

| 범주 | 경로 | 필드 | 개수 |
|---|---|---|---|
| 마켓플레이스 | `.claude-plugin/marketplace.json` | `metadata.version` | 1 |
| 플러그인 매니페스트 | `<plugin>/.claude-plugin/plugin.json` | `version` | 21 |
| 스킬 frontmatter (v2.0.0+ 복구) | `<plugin>/skills/<skill>/SKILL.md` | `version` (단일 필드) | 107 |

**모두 동일한 값**(예: `2.0.0`)을 가져야 하며, 플러그인·스킬 추가·삭제 시 이 카운트를 함께 갱신합니다.

### [HARD] 신규 스킬 추가 시 버전 표기 규칙

신규 스킬을 추가할 때:
- SKILL.md `version` 필드에 **추가 시점의 발행 버전**을 명시 (예: v2.1.0 출시 신규 스킬은 `version: 2.1.0`)
- plugin.json·marketplace.json도 동일 버전으로 bump
- CHANGELOG `## [vX.Y.Z]` 섹션에 신규 스킬 추가 기록

### [HARD] 버전 변경 절차

릴리스 버전을 올릴 때는 **반드시 아래 4단계를 함께 실행**합니다.

1. **3곳 동시 업데이트** (위 표의 128개 지점 전부)
   ```bash
   NEW="2.0.1"
   # marketplace
   sed -i '' -E 's/"version": *"[0-9]+\.[0-9]+\.[0-9]+"/"version": "'$NEW'"/' .claude-plugin/marketplace.json
   # 모든 plugin.json
   find . -path "*/.claude-plugin/plugin.json" -not -path "*/.git/*" -exec \
     sed -i '' -E 's/"version": *"[0-9]+\.[0-9]+\.[0-9]+"/"version": "'$NEW'"/' {} +
   # 모든 SKILL.md frontmatter version (v2.0.0+ 추가)
   find moai-*/skills -name SKILL.md -exec \
     sed -i '' -E 's/^version: [0-9]+\.[0-9]+\.[0-9]+$/version: '$NEW'/' {} +
   ```

2. **CHANGELOG.md 항목 추가**: `## [NEW] - YYYY-MM-DD` 섹션, Added/Changed/Fixed/Removed 분류

3. **커밋**: `chore(release): vX.Y.Z — 요약` 형식의 단일 릴리스 커밋

4. **태그 생성·푸시**: `git tag vX.Y.Z && git push origin vX.Y.Z`
   - 태그는 `vX.Y.Z` 형식 (v 접두어 필수)
   - 태그 값과 파일 내 버전은 **반드시 동일**

### [HARD] 금지 사항

- 일부 파일만 버전 올리기 (예: marketplace.json만 bump, plugin.json 방치)
- 태그 형식 불일치 (예: `v1.3.0` 태그인데 marketplace.json은 `1.2.0`)
- 버전 번호와 무관한 마이너 수정에 버전 bump
- 이미 배포된 태그를 force-push로 덮어쓰기 (사용자 캐시 손상)
- **SKILL.md에 `metadata:` 블록(중첩 객체) 재도입 금지** — `version:` 단일 필드는 v2.0.0+에서 필수
- **버전 변경 시 SKILL.md `version` 필드 일괄 갱신 누락 금지** — plugin.json·marketplace.json과 항상 동일 값 유지
- **신규 스킬 추가 시 SKILL.md `version` 누락 금지** — 발행 시점 버전(예: `2.1.0`) 명시 필수
- 일부 SKILL.md만 갱신하고 나머지 누락 (Cowork 자동 업데이트 감지 실패 → 사용자 환경 stale)

### 검증 명령

커밋 전 반드시 실행:
```bash
# 모든 버전이 동일한지 확인 — marketplace + plugin.json + SKILL.md frontmatter (한 줄만 출력되어야 통과)
{ grep -h '"version"' .claude-plugin/marketplace.json moai-*/.claude-plugin/plugin.json \
    | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'; \
  grep -h '^version:' moai-*/skills/*/SKILL.md \
    | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'; } | sort -u

# SKILL.md에 metadata 블록(중첩 객체)이 남아있지 않은지 확인 (아무 것도 출력되지 않아야 통과)
grep -l "^metadata:" moai-*/skills/*/SKILL.md 2>/dev/null

# 모든 SKILL.md에 version 필드가 있는지 확인 (실측 = 전체 카운트)
total=$(grep -lE "^version:" moai-*/skills/*/SKILL.md | wc -l | tr -d ' ')
expected=$(find moai-*/skills -name SKILL.md | wc -l | tr -d ' ')
[ "$total" = "$expected" ] && echo "  ✅ 전체 $expected개 SKILL.md에 version 필드 적용" || echo "  ❌ 누락 $((expected-total))개"
```

---

## 2. 플러그인 컴포넌트 규격 (HARD)

### SKILL.md frontmatter 규격 (v2.0.0 기준)

**v1.3.0부터 `metadata:` 블록(중첩 객체) 금지**. **v2.0.0부터 `version:` 단일 필드 필수**. 허용되는 필드는 3-4개뿐입니다.

#### 카테고리 A: 슬래시 호출 스킬 (Tab 자동완성 대상)

`/skill-name` 형태로 Tab 자동완성하고 싶은 모든 스킬:

```yaml
---
name: <skill-name>
description: |
  스킬의 목적과 트리거 조건을 자연스러운 서술로 풍부하게 작성.
  "다음과 같은 요청 시 반드시 이 스킬을 사용하세요:" 블록으로
  트리거 키워드/문장을 구체적으로 나열.
user-invocable: true
version: 2.0.0          # v2.0.0+ 필수 (Cowork 자동 업데이트 감지)
---
```

#### 카테고리 B: 모델 자동 호출 스킬 (체인 내부 호출만)

Tab 자동완성 불필요하고 모델이 문맥으로 자동 호출하는 스킬:

```yaml
---
name: <skill-name>
description: |
  서술형 설명 + 트리거 키워드.
version: 2.0.0          # v2.0.0+ 필수
---
```

### [HARD] 금지 필드

- `metadata:` 블록(중첩 객체 — status, updated, tags). 단, **단일 `version:` top-level 필드는 v2.0.0+에서 필수**
- `keywords:` (비표준, 사용 금지)
- 본문 상단의 `> vX.Y.Z | ...` 식 버전 배너 라인 (frontmatter `version`이 단일 소스)
- SKILL.md `version` 필드 누락 (Cowork 자동 업데이트 미감지)

### Plugin 매니페스트

`<plugin>/.claude-plugin/plugin.json` 필수 필드:
```json
{
  "name": "plugin-name",
  "version": "1.3.0",
  "description": "...",
  "author": { "name": "..." },
  "keywords": ["..."],
  "license": "MIT"
}
```

---

## 3. /project init — CLAUDE.md 생성 지침 정책 (HARD, v1.3.0 신규)

`moai-core:project` 스킬의 `/project init` 커맨드는 프로젝트 루트에 `CLAUDE.md`를 생성합니다. 생성된 CLAUDE.md에는 **다음 HARD 규칙 블록이 반드시 포함**되어야 합니다.

### 3-1. 문서·콘텐츠 생성 우선순위 (HARD)

사용자 프로젝트에서 DOCX/PPTX/XLSX/HWPX/HTML/블로그/카드뉴스/뉴스레터/SNS/카피/상세페이지/이미지/영상/음성 등 산출물을 만들 때는 **Claude 기본 artifacts·도구가 아니라 moai 스킬을 우선 사용**합니다.

| 산출물 | 우선 스킬 |
|---|---|
| DOCX / Word | `moai-office:docx-generator` |
| PPTX / 발표자료 | `moai-office:pptx-designer` |
| XLSX / Excel | `moai-office:xlsx-creator` |
| HWPX / 한글 | `moai-office:hwpx-writer` |
| HTML / 웹페이지 / 랜딩 | `moai-content:landing-page` |
| 블로그 / 카드뉴스 / 뉴스레터 / 카피 / 상세페이지 / SNS | `moai-content:*` |
| 이미지 / 영상 / 음성 | `moai-media:*` |

### 3-2. AI 슬롭 후처리 (HARD)

**모든 텍스트 산출물 워크플로우의 마지막 단계**에 `moai-core:ai-slop-reviewer` 스킬을 호출해 AI 패턴을 검수·수정합니다.

- 대상: 블로그, 뉴스레터, 카피, 사업계획서, 계약서/공문, 제안서, 보고서, 이메일, 랜딩 카피, 사업보고, 특허 초안, 강의자료 원고 등 **모든 텍스트 산출물**
- 제외: 코드, JSON/CSV 데이터, 차트·표, 숫자 리포트, 단순 조회 응답

### 3-3. 스킬 체이닝 (HARD)

`/project init`은 산출물별 **스킬 체인**을 설계해 CLAUDE.md의 "프로젝트 워크플로우" 섹션에 기록합니다. 예:

```
사업계획서(PPT)
  체인: strategy-planner → pptx-designer → ai-slop-reviewer
블로그 발행
  체인: blog → ai-slop-reviewer → (선택) nano-banana
제품 랜딩
  체인: copywriting → landing-page → ai-slop-reviewer
```

체인은 `moai-core/skills/project/references/templates/CLAUDE.md.tmpl`의 `{workflow_chains}` 슬롯에 주입됩니다.

### 3-4. 글로벌 프로필 질문 금지

v1.3.0 기준 `/project init`은 **이름·회사·역할을 재질문하지 않습니다**. `moai-profile.md`를 생성하지 않으며, 사용자 정보는 **프로젝트 CLAUDE.md 한 곳에만** 기록됩니다.

---

## 4. 푸시 전 문서 검수 정책 (HARD, v1.3.1 신규)

커밋/태그를 푸시하기 **이전에** 다음 문서들의 갱신 필요 여부를 반드시 점검한다. 코드·스킬 변경 대비 문서가 뒤처지는 경우가 많아, 릴리스 시점의 단일 체크포인트로 운영한다.

### 4-1. 점검 대상 문서 (필수)

| 문서 | 점검 항목 |
|---|---|
| 루트 `README.md` | 버전 배지, 플러그인/스킬 수 배지, `v{X}.{Y}.{Z} 하이라이트` 섹션, 플러그인 카탈로그 테이블의 스킬 수, 총 산출물 수, 플러그인 상세 소개 섹션의 스킬 테이블 |
| `.claude-plugin/marketplace.json` | `metadata.version` bump, `plugins[]` 배열의 신규/이름 변경 반영, 각 플러그인 `description` 최신화 |
| 루트 `CHANGELOG.md` | `## [X.Y.Z]` 섹션 존재, Added/Changed/Fixed/Removed/Migration 분류, 동기화 지점 표기 |
| `CLAUDE.local.md` | 태그 히스토리(§8) 업데이트, 버저닝 정책 테이블 |
| `<plugin>/README.md` × 17 | 플러그인 설명·스킬 수·신규 스킬 소개 최신화, `v{X}.{Y}.{Z}` 언급 일관성 |
| `<plugin>/CONNECTORS.md` (있는 경우) | MCP 서버 등록 절차, 환경변수 목록, API 키 발급처 |
| `moai-core/skills/project/references/core/INDEX.md` | 프로토콜 파일 목록, 플러그인 카운트, 변경 요약 |
| `moai-core/skills/project/references/templates/CLAUDE.md.tmpl` | 변수 슬롯, HARD 규칙 블록, 스킬 체인 포맷 |

### 4-2. [HARD] 푸시 전 체크리스트

```bash
# 1. 루트 README.md 버전/카운트 일관성
grep -E "Version-[0-9]+\.[0-9]+\.[0-9]+|Skills-[0-9]+|Plugins-[0-9]+" README.md
# 2. CHANGELOG.md 최신 섹션 존재 확인
head -5 CHANGELOG.md | grep -E "^## \[[0-9]+\.[0-9]+\.[0-9]+\]"
# 3. marketplace.json 버전과 plugin.json 전체 버전 일치 (한 줄만 출력되어야 통과)
{ grep -h '"version"' .claude-plugin/marketplace.json moai-*/.claude-plugin/plugin.json \
  | grep -oE '[0-9]+\.[0-9]+\.[0-9]+'; } | sort -u
# 4. marketplace.json plugins[] 개수 == plugin.json 파일 개수
python3 -c "import json; print(len(json.load(open('.claude-plugin/marketplace.json'))['plugins']))"
find . -path '*/.claude-plugin/plugin.json' -not -path '*/.git/*' | wc -l
# 5. 모든 플러그인 README 존재 (기대: 18 = 루트 + 17 플러그인)
find . -maxdepth 2 -name README.md -not -path "*/.git/*" | wc -l
# 6. 스킬 수 실측 vs README 선언 일치
find . -name SKILL.md -not -path "*/.git/*" | wc -l
# 7. v{X}.{Y}.{Z} 하이라이트가 최신인지
grep -n "하이라이트" README.md
```

### 4-3. [HARD] 금지 사항

- 플러그인·스킬 신규 추가 후 **README / marketplace.json 미갱신** 상태로 푸시
- 카탈로그 테이블의 스킬 수가 실제 `<plugin>/skills/*` 개수와 불일치한 채 푸시
- `v{X-1}.{Y}.{Z} 하이라이트`가 최신 버전에도 그대로 노출된 채 푸시
- 신규 스킬(예: `ai-slop-reviewer`) 추가 후 해당 플러그인 README의 스킬 테이블에 누락된 채 푸시
- `marketplace.json`의 `plugins[]` 배열이 신규 플러그인 추가·이름 변경·description 변경을 반영하지 않은 채 푸시
- `marketplace.json`의 플러그인 개수와 실제 `plugin.json` 개수 불일치 상태로 푸시

### 4-4. 검수 트리거 시점

- **MINOR 이상 릴리스**: 반드시 실행 (전체 체크리스트 1~7)
- **PATCH 릴리스**: 스킬·플러그인 변경이 있으면 실행 (선택적)
- **핫픽스 커밋**: 영향받은 문서만 선택적으로 실행
- **신규 플러그인 추가**: marketplace.json `plugins[]` 배열 업데이트 + 루트 README 카탈로그 테이블 추가 필수

### 4-5. [HARD] README 릴리스 동기화 게이트 (v1.5.1 신규)

v1.5.0 릴리스 시 README 선행 업데이트 누락 사고 재발 방지용. 체인 C(릴리스) 단계 4 검증 단계에 아래 명령을 **반드시** 포함한다.

```bash
NEW="1.5.0"  # 새 버전 (체인 C 단계 1에서 확보한 값)

# [게이트 1] 루트 README 버전 배지가 NEW와 일치
grep -E "Version-${NEW//./\\.}-blue" README.md || { echo "FAIL: 루트 README Version 배지 갱신 누락"; exit 1; }

# [게이트 2] 루트 README Skills 배지가 실측값과 일치
SKILL_COUNT=$(find moai-*/skills -name SKILL.md -not -path "*/.git/*" | wc -l | tr -d ' ')
grep -E "Skills-${SKILL_COUNT}-green" README.md || { echo "FAIL: 루트 README Skills 배지(${SKILL_COUNT})와 실제 스킬 수 불일치"; exit 1; }

# [게이트 3] 루트 README에 v{NEW} 하이라이트 섹션 존재
grep -F "v${NEW} 하이라이트" README.md || { echo "FAIL: 루트 README에 v${NEW} 하이라이트 섹션 부재"; exit 1; }

# [게이트 4] 플러그인별 README 스킬 테이블 실측 일치
# 스킬 테이블 패턴: "| [skill-name](./skills/..." 으로 시작하는 줄만 카운트 (참고자료 테이블 제외)
for plugin_dir in moai-*; do
  declared=$(grep -cE '^\| \[[a-z0-9-]+\]\(\./skills/' "$plugin_dir/README.md" 2>/dev/null || echo 0)
  actual=$(find "$plugin_dir/skills" -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')
  [ "$declared" -eq "$actual" ] || echo "WARN: $plugin_dir README 스킬 테이블 $declared행 vs 실제 $actual개"
done

# [게이트 5] 신규 스킬이 추가된 플러그인의 README에 해당 스킬명 언급 확인
# (release-notes-vX.Y.Z.md의 "What's New" 섹션에서 스킬명을 추출해 개별 README에 grep)
```

[HARD] 게이트 1·2·3 **하나라도 실패하면 릴리스 커밋 금지**. 수정 후 재검증 통과해야 진행.
[HARD] 게이트 4·5는 WARN이면 사용자에게 보고 후 명시적 승인 시에만 진행.
[HARD] README 게이트 실패 시 **force-push로 우회 금지**. 정상 커밋으로 수정본 추가.

## 5. 릴리스 후 사용자 안내

신버전 배포 후 사용자 측 캐시 갱신 필요:
```
/plugin marketplace update cowork-plugins
```
이후 플러그인 상세 재진입 시 반영됨. README나 릴리스 노트에 해당 안내 포함.

---

## 6. MCP 서버 통합 정책 (HARD)

플러그인이 MCP 서버를 번들하려면 다음 규칙을 따릅니다:

- 플러그인 루트에 **`.mcp.json`** 파일 배치 (예: `moai-media/.mcp.json`)
- 환경변수는 `${VAR_NAME}` 구문으로만 주입 — 절대 하드코딩 금지
- hosted MCP는 `type: "http"` + `url` + `headers`로 등록
- local stdio MCP는 `command` + `args` (권장: `uvx <package>` 형태)
- API 키 등록 절차는 플러그인 루트의 `CONNECTORS.md`에 필수 문서화

현재 MCP 번들 플러그인:
- `moai-media`: `fal-ai` (hosted), `elevenlabs` (local stdio via uvx)

## 7. 외부 API 모델 ID 업데이트 정책

외부 API(Google, OpenAI, Anthropic 등)가 모델 이름·엔드포인트를 변경하면:

1. 영향 스킬 식별 (`grep -r "<old-model-id>" .`)
2. 공식 문서 확인 후 매핑 테이블 업데이트 (예: `generate_image.py` MODEL_MAP)
3. 레거시 별칭은 **최소 1 메이저 버전** 동안 유지 (v1.0.x → v1.1.x는 호환)
4. 응답 스키마가 바뀌면 스크립트 v번호 메이저 bump (예: `generate_image.py v3 → v4`)
5. CHANGELOG Migration 섹션에 사용자 조치 사항 명시

## 8. GitHub Release 정책 (HARD)

태그를 푸시할 때마다 **반드시 같은 태그 이름의 GitHub Release를 생성**합니다. 릴리스 노트는 **CHANGELOG 섹션 + 사용자 친화 확장 블록**을 합친 풀 버전으로, 초보자도 "이번에 뭐가 바뀌었고 내가 뭘 해야 하는지"를 그 한 페이지에서 이해할 수 있어야 합니다.

### 8-1. 릴리스 노트 필수 섹션 (HARD)

모든 공식 Release 본문은 아래 **7개 섹션을 이 순서대로** 포함합니다. 섹션이 해당 없는 경우에도 "해당 없음" 한 줄로 명시해 누락을 방지합니다.

1. **Highlights** — 한 줄 요약 + 이번 릴리스가 사용자에게 왜 중요한지 2~4문장. 초보자가 2초 안에 성격을 파악할 수 있게.
2. **What's New (추가)** — 신규 스킬·플러그인·기능. 각 항목마다:
   - 스킬 전체 경로(예: `moai-business:kr-gov-grant`)
   - 한 줄 기능 요약
   - 주요 입출력·MODE·지원 범위
   - **관련 링크 3종**: (a) SKILL.md 파일 GitHub URL, (b) 온라인 문서 URL, (c) 공식 외부 참고 URL(해당 시)
3. **Changed (변경)** — 기존 스킬·메타데이터·버전 변경. 변경 전/후 대비가 드러나야 함. marketplace.json description 변경, 버전 동기화 범위(18지점), 파일 수 등.
4. **Fixed (수정)** — 버그·정합성 수정. 해당 없으면 "해당 없음".
5. **Removed (제거)** — 제거된 스킬·필드·규칙. 해당 없으면 "해당 없음".
6. **업그레이드 방법** — Cowork/Claude Code 사용자 기준 단계별 명령. 반드시 포함:
   - `/plugin marketplace update cowork-plugins`
   - 플러그인 상세 재진입 필요성 안내
   - API 키 재등록이 필요한 경우 명시
   - 이전 버전과의 호환성(Breaking change 여부)
7. **관련 문서 & 출처** — 온라인 문서 사이트 플러그인 페이지, CHANGELOG 전체 링크, 공식 기관·커넥터 URL, 참고 이슈/PR 번호.

### 8-2. 사용자 이해 장치 (HARD)

- **사용 예시 문장 최소 2개**: "이렇게 입력하면 됩니다" 형태의 복사·붙여넣기 가능한 자연어 프롬프트.
- **비교표 권장**: 기존 스킬과 겹치는 범위가 있으면 "언제 어떤 걸 쓰나" 표로 명시(예: `kr-gov-grant` vs `moai-research:grant-writer`).
- **Mermaid 다이어그램 권장**: 신규 스킬의 워크플로우가 3단계 이상이면 Mermaid로 시각화. GitHub Release 페이지는 Mermaid를 렌더합니다.
- **초보자 안심 문구**: Breaking change가 없으면 "기존 워크플로우 그대로 동작합니다"를, Breaking이면 구체 대응 방법을 명시.

### 8-3. CHANGELOG → 릴리스 노트 생성 절차

CHANGELOG.md에는 구조화된 diff만 남기고, 릴리스 노트 본문은 CHANGELOG 섹션을 기본 소스로 삼되 8-1 필수 섹션을 맞추도록 확장·재구성합니다.

```bash
NEW="1.5.0"
REPO="modu-ai/cowork-plugins"
NOTES="/tmp/release-notes-v${NEW}.md"

# 1단계: CHANGELOG에서 해당 버전 섹션 추출 (초안)
awk -v v="$NEW" '
  $0 ~ "^## \\[" v "\\]" {flag=1; next}
  /^## \[/{flag=0}
  flag
' CHANGELOG.md > "$NOTES"

# 2단계: 필수 7개 섹션 확장 (에디터로 직접 작성) — 8-1·8-2 규칙 적용
#   - Highlights, What's New(링크 3종 포함), Changed, Fixed, Removed,
#     업그레이드 방법, 관련 문서 & 출처

# 3단계: 본문 유효성 검사 — 100 바이트 미만이면 중단
[ $(wc -c < "$NOTES") -lt 100 ] && echo "❌ 릴리스 노트 미작성" && exit 1

# 4단계: Release 생성 또는 업데이트
if gh release view "v$NEW" --repo "$REPO" >/dev/null 2>&1; then
  gh release edit "v$NEW" --repo "$REPO" --notes-file "$NOTES"
else
  gh release create "v$NEW" --repo "$REPO" \
    --title "v$NEW — <한줄_핵심_요약>" \
    --notes-file "$NOTES" \
    --latest  # MINOR 이상일 때
fi

# 5단계: body 비어있음 회귀 검증 (가장 중요 — CI 대체)
BODY_LEN=$(gh release view "v$NEW" --repo "$REPO" --json body -q '.body' | wc -c)
[ "$BODY_LEN" -lt 500 ] && echo "❌ 릴리스 본문이 500자 미만입니다" && exit 1
echo "✅ 릴리스 본문 ${BODY_LEN}자"
```

### 8-4. [HARD] 규칙

- [HARD] 모든 공식 태그(`vX.Y.Z`)는 **GitHub Release**가 반드시 존재해야 함
- [HARD] Release 본문은 **8-1의 7개 섹션을 모두 포함**해야 함 — "CHANGELOG 그대로 복붙" 금지
- [HARD] Release 본문은 **최소 500자 이상** — 생성 직후 `--json body` 로 검증 (8-3 5단계)
- [HARD] 신규 스킬은 반드시 **링크 3종**(SKILL.md GitHub URL + 온라인 문서 URL + 공식 외부 URL) 포함
- [HARD] Release 제목은 **`vX.Y.Z — <한줄 요약>`** 형식 (예: `v1.5.0 — sbiz365-analyst + kr-gov-grant`)
- [HARD] `do shell script` 다중라인 `\` 연결 금지 — 단일 라인 또는 `--notes-file` 절대경로 사용
- [HARD] MINOR 이상 릴리스는 `--latest` 플래그 적용 (PATCH도 최신이면 적용)
- [HARD] Pre-release (alpha/beta/rc)는 `--prerelease` 플래그 적용
- [HARD] 사용 예시 프롬프트 **최소 2개** 포함 (신규 스킬이 있으면 각 스킬당 1개 이상)
- [HARD] 내부 이터레이션(점진 PATCH)이 MINOR에 집약되는 경우, **중간 PATCH 태그의 Release는 Draft 또는 생략 가능**하되 집약 대상 MINOR Release 노트에 이력 요약 포함
- [HARD] Draft 상태로 방치된 과거 Release는 분기별로 정리 (삭제 또는 정식 발행)
- [HARD] 기존 Release 본문이 비었거나 500자 미만으로 발견되면 즉시 `gh release edit`로 보강 (과거 누적분 포함)

---

## 9. 태그 히스토리

- **v2.1.0** (2026-05-07): MINOR. `moai-content:humanize-korean` 신규 스킬 도입 — [`epoko77-ai/im-not-ai`](https://github.com/epoko77-ai/im-not-ai) v1.6.1 (MIT, ⭐937 stars) Fast 모드 단일 스킬 변형 포팅. 10대 카테고리 × 40+ AI 티 패턴 SSOT, 의미 100% 보존 가드(변경률 30/50%), A/B/C/D 등급 자동 판정, Python 표준 라이브러리만 쓰는 metrics.py 내장. 권장 체인: `… → moai-core:ai-slop-reviewer (1차) → moai-content:humanize-korean (2차)`. 마켓플레이스 106 → **107 스킬**, 플러그인 21개 유지. Breaking change 없음. 동기화 지점: marketplace.json + 21 plugin.json + 107 SKILL.md = 129 지점.
- **v1.3.0** (2026-04-14): 공식 MINOR. `/moai` → `/project` 커맨드 이름 전환 (Claude Code 프로젝트 레벨 스킬과의 shadowing 충돌 해소). `ai-slop-reviewer` 스킬 신규 도입 (모든 텍스트 산출물 후처리 검수). **스킬 체이닝 기반 CLAUDE.md 생성** — `/project init`이 산출물별 스킬 체인을 설계하고 확인 후 CLAUDE.md에 기록. SKILL.md `metadata:` 블록 전면 제거 (단일 버전 소스: plugin.json). 글로벌 프로필 시스템(`moai-profile.md`, `[MoAI 프로필]`) 전면 제거. CLAUDE.md 템플릿 외부 파일화(`templates/CLAUDE.md.tmpl`). office/web 스킬 우선 + AI 슬롭 후처리 HARD 규칙 고정 포함.
- **v1.2.0** (2026-04-14): 공식 MINOR. `moai-media` 신규 플러그인, Nano Banana Pro + 2 체제 확정(Imagen 4 → Gemini 3 Image Preview), Kling 영상 단일화, ElevenLabs·fal.ai MCP 번들, 전 저장소 17 플러그인/70 스킬로 확장.
- v1.1.0~v1.1.3 (2026-04-14, 내부 이터레이션): moai-media 개발 점진 릴리스. v1.2.0에 집약됨.
- **v1.0.3** (2026-04-14): `/moai` 자동완성 수정 + 전체 버전 통일 + 태그 정책 확립

---

Version: 1.3.0
Last Updated: 2026-04-14
