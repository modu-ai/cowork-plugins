# agent-catalog.md — 코디네이터 에이전트 인지 & 체인 설계 SSOT

`/project` 초기화가 **스킬뿐 아니라 코디네이터 에이전트까지** 체인 설계에 활용하기 위한 단일 진실(SSOT). Phase 2 인벤토리(에이전트 스캔), Phase 3 체인 설계(코디네이터 우선), Phase 3.5 에이전트 생성(기존 우선)이 모두 이 문서를 참조한다.

---

## 개요 — 코디네이터 에이전트란

cowork-plugins의 각 도메인 플러그인은 `<plugin>/agents/*.md`에 **코디네이터(오케스트레이터) 서브에이전트**를 번들한다. 각 코디네이터는 해당 도메인의 **여러 스킬을 정해진 순서/병렬로 엮은 체인을 캡슐화**한다. 예: `business-plan-coordinator` = strategy-planner → market-analyst → investor-relations → ai-slop-reviewer → humanize-korean → pptx-designer.

즉 많은 산출물에서 **코디네이터 에이전트 = 그 도메인 체인의 완성형 실행기**다. `/project`는 이를 인지해, 매칭되는 워크플로우에 **코디네이터를 우선 실행기로 추천**하고, 코디네이터가 없는 경우에만 인라인 스킬 체인을 설계한다.

### Cowork 환경 제약 (HARD)

- 코디네이터 에이전트는 **Cowork 서브에이전트 전용**이다(Chat 표면에서는 회색·비활성). cowork-plugins는 Cowork를 대상 환경으로 가정한다.
- 모든 코디네이터의 `tools`는 `Read, Grep, Glob, Write, Edit, WebSearch`로 통일된다 — **Bash·WebFetch는 Cowork 서브에이전트에서 동작하지 않는다**. 셸·페이지 fetch가 필요한 단계는 부모 세션(오케스트레이터)이 수행한다.
- 자연어로 위임하면 자동 호출된다(예: "사업계획서 만들어줘" → `business-plan-coordinator`).

---

## Phase 2 — 에이전트 인벤토리 (동적 스캔)

스킬 인벤토리와 **동일한 동적 도출 원칙**을 따른다(하드코딩 목록 금지 — 신규 코디네이터 자동 포함).

```bash
PLUGIN_DIR=~/.claude/plugins
# 설치된 cowork 플러그인의 agents/*.md frontmatter 스캔
for plugin in "${INSTALLED_COWORK_PLUGINS[@]}"; do
  for af in "$PLUGIN_DIR/$plugin"/agents/*.md; do
    [ -f "$af" ] || continue
    name=$(grep -m1 '^name:' "$af" | sed 's/^name: *//')
    # description: | 블록 첫 줄 = 호출 트리거 요약
    echo "$name → $plugin"
  done
done
```

각 에이전트의 `name`과 `description`(호출 트리거)을 추출해 `inventory.json`의 `agents_available`에 등록한다. 플러그인이 설치돼 있으면 해당 코디네이터도 가용한 것으로 간주한다(에이전트는 플러그인에 번들됨).

`inventory.json` 확장 스키마:

```json
{
  "plugins_installed": ["moai-business", "moai-office"],
  "skills_available": { "strategy-planner": "moai-business", "pptx-designer": "moai-office" },
  "agents_available": {
    "business-plan-coordinator": "moai-business",
    "office-doc-qa": "moai-office"
  }
}
```

---

## 코디네이터 ↔ 도메인 워크플로우 매핑 (참고 스냅샷)

아래는 **동적 스캔의 참고 스냅샷**이며 권위 있는 목록이 아니다(SSOT는 런타임 스캔). 카운트·항목을 하드코딩하지 않는다. 현재 스냅샷: **31개 코디네이터 / 24개 플러그인**.

| 코디네이터 (Cowork) | 플러그인 | 캡슐화 워크플로우 | 호출 트리거 예시 |
|---------------------|----------|-------------------|------------------|
| `business-plan-coordinator` | moai-business | 사업계획서·IR 전략→발표자료 | "사업계획서 만들어줘", "IR 덱 준비" |
| `business-grant-coordinator` | moai-business | 정부지원사업 진단→신청서 | "정부지원사업 신청서 써줘" |
| `content-publishing-pipeline` | moai-content | 멀티채널 발행·리퍼포징(블로그·SNS·뉴스레터·카드뉴스) | "블로그 쓰고 SNS용으로도" |
| `content-detail-orchestrator` | moai-content | 상세페이지 기획→구성→카피 | "상세페이지 기획부터 카피까지" |
| `office-doc-qa` | moai-office | 오피스 문서(워드·PPT·엑셀·한글·PDF) 생성+AI티 검수 | "이 내용 PPT로 만들고 검수까지" |
| `core-text-qa-coordinator` | moai-core | 한국어 텍스트 최종 품질 게이트(AI티 제거→윤문) | "이 글 자연스럽게 다듬어줘" |
| `finance-report-assembler` | moai-finance | 결산→재무제표→변동분석 리포트 | "재무 리포트 조립해줘" |
| `legal-review-coordinator` | moai-legal | 계약·법무 리스크 다단계 검토 | "이 계약서 법무 검토" |
| `commerce-launch-coordinator` | moai-commerce | 신상품 런칭 시장조사→채널 메시지 | "신상품 런칭 준비" |
| `commerce-compliance-coordinator` | moai-commerce | 광고법·식약처 컴플라이언스 게이트 | "광고 문구 법규 검수" |
| `commerce-detail-page-builder` | moai-commerce | 상품 상세페이지 이미지+카피 | "상세페이지 이미지랑 카피" |
| `commerce-growth-analyst` | moai-commerce | 유닛이코노믹스·리텐션·광고효율 분석 | "커머스 성장 분석" |
| `marketing-campaign-coordinator` | moai-marketing | 캠페인 기획→콘텐츠→성과 리포트 | "마케팅 캠페인 기획부터" |
| `marketing-audit-coordinator` | moai-marketing | SEO·랜딩·픽셀 종합 감사 | "마케팅 자산 감사" |
| `marketing-meta-ads-orchestrator` | moai-marketing | 메타 광고 셋업→운영→분석→리포트 | "메타 광고 셋업부터 분석" |
| `media-production-pipeline` | moai-media | 이미지→영상→음성 미디어 제작 | "이미지랑 영상이랑 음성까지" |
| `research-scout-coordinator` | moai-research | 논문·특허 조사→분석→작성 | "논문 조사부터 작성까지" |
| `public-data-research-coordinator` | moai-public-data | 공공데이터 다중 조회→종합 리서치 | "공공데이터 종합 리서치" |
| `data-analysis-coordinator` | moai-data | 데이터 탐색→시각화→리포트 | "데이터 분석 리포트" |
| `product-ux-audit-coordinator` | moai-product | UX 리서치→설계→스펙→로드맵 | "UX부터 스펙·로드맵까지" |
| `book-manuscript-coordinator` | moai-book | 단행본 기획→출간 제안 | "책 한 권 기획부터" |
| `education-course-builder` | moai-education | 커리큘럼→평가→운영→후속 | "강의 커리큘럼부터 운영까지" |
| `career-job-search-coordinator` | moai-career | 직무분석→이력서→포트폴리오→면접 | "이력서부터 면접 준비까지" |
| `hiring-coordinator` | moai-hr | 스크리닝→오퍼→온보딩→인사운영 | "채용 스크리닝부터 온보딩" |
| `sales-proposal-coordinator` | moai-sales | 제안서 작성+AI티 검수 | "제안서 써서 검수까지" |
| `comms-meeting-report-coordinator` | moai-comms | 회의→보고 변환→피드백 | "회의 정리해서 보고서로" |
| `operations-coordinator` | moai-operations | 프로세스→벤더→상태보고 | "운영 프로세스 정리" |
| `productivity-planning-coordinator` | moai-productivity | 목표→습관→시간→주간보고→회고 | "이번 분기 목표부터 회고까지" |
| `wealth-roadmap-coordinator` | moai-wealth | 가계→투자→보험→세금 로드맵 | "개인 재무 로드맵" |
| `design-handoff-coordinator` | moai-design | Claude Design 핸드오프 5단계 | "디자인 핸드오프 준비" |
| `support-ticket-triage-batch` | moai-support | 문의 분류→응답→에스컬레이션→KB화 | "문의 분류해서 응대까지" |

> 위 표는 스냅샷이다. 런타임 동적 스캔(Phase 2)이 실제 가용 코디네이터의 권위 있는 출처이며, 트리거·내부 체인은 각 에이전트의 `description`·본문이 SSOT다. 임의의 코디네이터 이름을 지어내지 않는다.

---

## 코디네이터 우선 vs 인라인 스킬 체인 — 결정 규칙

Phase 3 체인 설계에서 각 산출물 워크플로우마다 다음 순서로 판정한다:

1. **매칭 코디네이터 존재 + 워크플로우가 그 도메인 체인과 일치** → **코디네이터를 우선 실행기로 추천**.
   - CLAUDE.md 체인 표기에 담당 코디네이터를 명시한다(§체인 표기 규약).
   - 코디네이터가 내부에서 ai-slop-reviewer·humanize-korean까지 처리하면 별도 후처리 단계를 중복 추가하지 않는다.
2. **매칭 코디네이터 없음 / 부분만 커버 / 단순 1-2단계** → **인라인 스킬 체인**을 설계한다(기존 Phase 3 프리셋).
3. **코디네이터도 없고 자격 조건(고정 게이트·병렬 fan-out·고빈도 반복)을 만족** → Phase 3.5에서 **신규 프로젝트 에이전트 생성** 후보.

핵심: **기존 코디네이터를 우선 활용**하고, 없을 때만 인라인 체인 또는 신규 에이전트 생성으로 내려간다. 에이전트 남발을 막으면서 스킬·에이전트를 모두 최적 활용한다.

---

## 체인 표기 규약 (코디네이터 포함)

CLAUDE.md에 기록될 형식. 코디네이터가 있으면 `[에이전트]`로 표기하고 내부 체인을 괄호로 부기한다:

```
[산출물명]
  요청 예시: "..."
  실행기: business-plan-coordinator (에이전트, Cowork)
  내부 체인: strategy-planner → market-analyst → investor-relations → ai-slop-reviewer → humanize-korean → pptx-designer
  폴백(에이전트 미가용 시): strategy-planner → pptx-designer → ai-slop-reviewer  (인라인 스킬 체인)
```

코디네이터가 없는 산출물은 기존 인라인 표기를 그대로 쓴다:

```
[산출물명]
  요청 예시: "..."
  체인: skill-A → skill-B → ai-slop-reviewer
```

---

## 크로스레퍼런스

- `init-protocol.md` §Phase 2(에이전트 인벤토리)·§Phase 3(코디네이터 우선)·§Phase 3.5(기존 우선 생성)
- `router.md` §6.5(코디네이터 우선 라우팅)
- `templates/CLAUDE.md.tmpl` §5.4(활용 코디네이터 에이전트)·§5.5(생성 프로젝트 에이전트)
- 각 코디네이터 본문: `<plugin>/agents/<name>.md` (트리거·내부 체인의 SSOT)
