# moai-core

MoAI 코어 플러그인 — 프로젝트 초기화, 도메인 라우터, AI 슬롭 검수, 피드백 허브.

스킬을 자연어로 트리거하는 중앙 허브입니다. 사용자 요청을 자동 감지하여 16개 도메인 플러그인의 전문 스킬로 즉시 라우팅합니다. `/project init`으로 프로젝트 맞춤형 `CLAUDE.md`와 **스킬 체이닝 워크플로우**를 생성하고, `/project catalog`로 전체 스킬 목록을 조회합니다. 모든 텍스트 산출물은 `ai-slop-reviewer` 스킬로 검수되어 인간적인 톤으로 다듬어집니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [project](./skills/project/) | Cowork 프로젝트 초기화 — 워크플로우 인터뷰, 스킬 체인 설계, CLAUDE.md 자동 생성, 도메인 라우팅, API 키 관리 | 9 + 1 템플릿 | ✅ |
| [ai-slop-reviewer](./skills/ai-slop-reviewer/) | AI 슬롭 검수 — 기계적 패턴(과장 형용사·뻔한 결론·반복 구조)을 진단하고 인간적인 톤으로 수정. 모든 텍스트 산출물 체인의 필수 마지막 단계 | 0 | ✅ |
| [feedback](./skills/feedback/) | 버그/기능 요청 → GitHub Issues 자동 등록 (`/project feedback`) | 0 | ✅ |
| [ai-diagnostic](./skills/ai-diagnostic/) | 4차원 병렬 진단(기술·프로세스·사람·비즈니스) → 근본 원인 식별 + 우선순위별 해결책 | 1 | ✅ |
| [skill-builder](./skills/skill-builder/) | 6-Phase 스킬 생성 워크플로우 (revfactory/harness 방법론). 새 SKILL.md 자동 작성·검증 | 5 | ✅ |
| [skill-template](./skills/skill-template/) | SKILL.md 표준 템플릿. skill-builder가 기반으로 사용 | 0 | ✅ |
| [skill-tester](./skills/skill-tester/) | 스킬 품질 자동 검증 — 4차원 루브릭(Correctness/Completeness/Clarity/Efficiency) + 체인 회귀 테스트 | 4 | ✅ |

## 사용 예시

```
/project init
```
워크플로우 인터뷰(최대 3질문) → 설치 플러그인 감지 → 산출물별 **스킬 체인** 설계 → 사용자 확인 → `./CLAUDE.md` 자동 생성.

```
사업계획서 써줘
```
자연어를 감지하여 `moai-business`의 `strategy-planner` 스킬을 자동 트리거 → `docx-generator` 또는 `pptx-designer` → **`ai-slop-reviewer`** 검수로 마무리.

```
/project catalog
```
16개 도메인 플러그인 전체 스킬 목록(70개 스킬)을 조회합니다.

```
/project apikey
```
등록된 API 키(공공데이터포털, KIPRIS, 국가법령정보, Gemini, fal.ai, ElevenLabs)를 조회·변경·추가·삭제합니다.

```
/project feedback PPT 생성 시 한글 폰트가 깨져요
```
버그 리포트를 수집하여 GitHub Issues에 자동 등록합니다.

```
이 블로그 초안 AI 티 나는 부분 고쳐줘
```
`ai-slop-reviewer` 스킬을 직접 호출하여 AI 패턴을 진단·수정합니다.

## CLAUDE.md 자동 생성 규칙 (HARD)

`/project init`이 생성하는 모든 CLAUDE.md에는 다음 HARD 규칙이 **반드시** 포함됩니다:

1. **문서·콘텐츠 생성 우선순위** — DOCX/PPTX/XLSX/HWPX는 `moai-office:*`, HTML·랜딩은 `moai-content:landing-page`, 블로그·카드뉴스·카피·뉴스레터·SNS는 `moai-content:*`, 이미지·영상·음성은 `moai-media:*`. Claude 기본 artifacts보다 항상 우선.
2. **AI 슬롭 후처리** — 모든 텍스트 산출물 체인의 마지막 단계에 `ai-slop-reviewer` 호출(코드·데이터·숫자는 제외).
3. **스킬 체이닝** — 산출물별 체인이 CLAUDE.md "워크플로우" 섹션에 기록됨.

## v1.3.0 주요 변경

- `/moai` → `/project` 커맨드 리네임 (Claude Code 내부 스킬과의 shadowing 충돌 해소)
- `ai-slop-reviewer` 스킬 신규 도입
- 스킬 체이닝 기반 CLAUDE.md 자동 생성
- 글로벌 프로필 시스템(`moai-profile.md`, `[MoAI 프로필]`) 전면 제거 — 프로젝트마다 이름·회사·역할 재질문하지 않음
- SKILL.md `metadata:` 블록 삭제 (버전은 plugin.json 단일 소스)

## 설치

Settings > Plugins > cowork-plugins에서 `moai-core` 선택.

## 참고자료

| 항목 | URL |
|------|-----|
| OWPML 스펙 | [hancom.com/support/downloadCenter/hwpOwpml](https://www.hancom.com/support/downloadCenter/hwpOwpml) |
| Cowork 플러그인 가이드 | [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins) |
| Anthropic knowledge-work-plugins | [github.com/anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) |
