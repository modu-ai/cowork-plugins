# moai-core

MoAI 코어 플러그인 — 도메인 AI 라우터, 초기화, 자가학습 엔진.

스킬을 자연어로 트리거하는 중앙 허브입니다. 사용자 요청을 자동 감지하여 16개 플러그인의 전문 스킬로 즉시 라우팅합니다. `/moai init`으로 프로젝트 맞춤형 `CLAUDE.md`를 생성하고, `/moai catalog`로 전체 스킬 목록을 조회합니다.

## 스킬

| 스킬 | 설명 | 레퍼런스 | 상태 |
|------|------|:--------:|:----:|
| [moai](./skills/moai/) | 도메인 AI 라우터 — 자연어 감지, `/moai init`, `/moai catalog` 커맨드 처리 | 10 | ✅ |

## 에이전트

| 에이전트 | 모델 | 역할 |
|---------|:----:|------|
| quality-evaluator | Haiku | 바이너리(PASS/FAIL) 산출물 품질 평가. 전 플러그인에서 공유 호출 |

## 사용 예시

```
/moai init
```
대화형 설문을 통해 프로젝트 맞춤형 `./CLAUDE.md`를 자동 생성합니다.

```
사업계획서 써줘
```
자연어를 감지하여 `moai-business`의 `strategy-planner` 스킬을 자동 트리거합니다.

```
/moai catalog
```
16개 플러그인 전체 스킬 목록을 조회합니다.

## 설치

Settings > Plugins > moai-cowork-plugins에서 `moai-core` 선택
