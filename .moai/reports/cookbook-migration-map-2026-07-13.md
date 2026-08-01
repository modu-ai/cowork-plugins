# 쿡북 구 레시피 이관 맵 (P5 산출물)

기준: `www-ia-update-plan-v2-2026-07-10.html` §05 — 기존 레시피를 ① 개정 이관(새 "코워크 프로젝트" 골격으로 재작성) ② 트랙 이동(/guide/ 사용법 성격) ③ 폐기/유지 3분류로 고정한다.
신규 12선은 `content/cookbook/projects/`에 발행 완료(2026-07-10). 본 맵은 잔존 구 콘텐츠의 처분 기준을 고정하는 산출물이며, 실제 이동·삭제는 후속 배치에서 실행한다.

## 분류 결과

### ① 개정 이관 — 코워크 프로젝트 골격으로 재작성 후 projects/로 흡수

| 구 문서 | 대응 신규 레시피 | 비고 |
|---|---|---|
| cookbook/business-plan.md | projects/startup-feasibility, gov-grant-application | 컨설턴트·재무세무 투입형으로 재작성 |
| cookbook/contract-review.md | projects/contract-risk-report | 법무→코워커 골격으로 흡수 |
| cookbook/legal-nda-batch.md | projects/contract-risk-report | 일괄 처리 변형 예시로 병합 |
| cookbook/report-automation.md | projects/weekly-report-routine | 코워커→사무관 골격으로 흡수 |
| cookbook/blog-pipeline.md | projects/sns-content-month | 마케터 투입형으로 흡수 |
| cookbook/ir-deck.md | (후속) 투자 유치 IR 프로젝트 레시피 | 13번째 레시피 후보 — 컨설턴트→디자이너 |
| cookbook/design/presentation.md | (후속) 디자이너 프로젝트 레시피 | guide/design 트랙과 중복 부분은 제거 |

### ② /guide/ 트랙 이동 — 기능 소개·사용법 성격

| 구 문서 | 목적지 |
|---|---|
| cookbook/skill-chaining.md | /guide/cowork/ (스킬 사용법 심화) |
| cookbook/best-practices.md | /guide/cowork/ (사용 패턴) |
| cookbook/troubleshooting.md | /guide/cowork/troubleshooting 및 /help/troubleshooting과 병합 |
| cookbook/automation-recipes.md | /guide/cowork/ (예약 작업·자동화) |

### ③ 유지 (현행 보존) 또는 폐기

| 구 문서 | 처분 |
|---|---|
| cookbook/tracks/ (12 트랙) | **유지** — 직무별 실전 트랙으로 projects/와 상호 보완. 각 트랙 상단에 대응 projects/ 레시피 크로스링크 추가(후속) |
| cookbook/guides/ (7편) | **유지 후 축차 흡수** — 주제가 겹치는 projects/ 레시피가 생기는 시점에 개별 폐기 |
| cookbook/templates/ (4편) | **유지** — 레시피가 참조하는 부속 템플릿 |
| cookbook/design/_index.md | design/presentation 이관 완료 시 **폐기** |

## 집행 규칙

- 이동·폐기 시 구 URL은 반드시 `aliases`로 목적지에 남긴다 (301 유지).
- 메뉴(`data/menu/main.yaml`)의 쿡북·실전 트랙 그룹은 처분 실행 커밋에서 함께 갱신한다.
- 신규 레시피 추가는 §05 공통 골격(문제 상황 → 투입 직원·스킬 → 단계별 진행 → 결과물 → 생산성 포인트)을 따른다.
