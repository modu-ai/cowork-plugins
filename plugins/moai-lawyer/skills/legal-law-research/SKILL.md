---
name: legal-law-research
description: |
  법제처 법령·판례·행정규칙·자치법규·조약·해석례(국세청) 원문 조회와 LLM 환각방지 인용검증·판례 생사 확인·행위시법 판단·조문 영향 그래프·신구대조표를 전담합니다. korean-law MCP(법제처 42개 API → 9 도구) 사용.
  다음과 같은 요청 시 사용하세요:
  - "근로기준법 제74조 본문 알려줘"
  - "이 답변에 인용된 조문 실존하는지 검증해줘" (verify_citations — LLM 환각방지)
  - "이 판례 아직 유효한가" (cite_check — 판례 생사)
  - "2023년 당시 도로교통법 제44조" (applicable_law — 행위시법)
  - "민법 제103조 관련 판례·헌재결정 영향 그래프" (impact_map)
  - "관세법 제38조 + 관세청 해석례 + FTA 조약" (legal_research customs)
  - "산업안전보건법 별표1 내용" (get_annexes)
  - "주택임대차보호법 5단계 안내" (legal_research action_plan)
  - "근로기준법 최근 개정 신구대조표" (amendment_track)
  법무팀·로펌·법률 연구자·공무원·계약서 검토자·학생 대상. 사전 준비: 법제처 OC 키(law.go.kr 무료), 환경변수 KOREAN_LAW_OC.
version: "1.0.0"
---

# 법령 리서치 (Law Research)

## 개요

국가법령정보센터(법제처) 법령·판례·행정규칙·자치법규·조약·해석례(국세청 포함) 원문 조회와 정밀 분석을 전담한다. `korean-law` MCP(chrisryugj/korean-law-mcp v4.4, MIT)가 법제처 42개 API를 9개 도구로 압축하며, LLM 환각 방지 인용 검증·판례 생사 확인·행위시법 판단·조문 영향 그래프를 지원한다.

**면책 고지: AI 보조 조회이며 전문 법률 자문을 대체하지 않습니다**

## 트리거 키워드

법령 조문, 법률 본문, 판례 검색, 판례 생사, 인용 검증, 행위시법, 신구대조표, 영향 그래프, 조례, 시행령, 시행규칙, 행정규칙, 자치법규, 조약, 해석례, 국세청 해석, 별표, 서식, 법제처, law.go.kr, Korean Law MCP

## 지원 도구 (korean-law MCP — 9개)

| 구분 | 도구 | 설명 |
|------|------|------|
| 리서치 | `legal_research` | 다단계 법령 리서치. `task` 8종 선택 (아래 표) |
| 정밀분석 | `legal_analysis` | 검증·분석. `mode` 4종 선택 (아래 표) |
| 법령 | `search_law` | 법령 검색 → lawId, MST 획득 |
| 법령 | `get_law_text` | 조문 전문 조회 (조호=4자리 숫자 사용) |
| 법령 | `get_annexes` | 별표/서식 조회 (금액표·요율표·별지서식) |
| 통합 | `search_decisions` | 17개 도메인 통합 검색 (판례·헌재·조세심판·공정위·노동위·관세·해석례·행심·개인정보위·권익위·소청심사·학칙·공사공단·공공기관·조약·영문법령) |
| 통합 | `get_decision_text` | 17개 도메인 결정례 전문 조회 |
| 메타 | `discover_tools` | 전문 도구 검색 (용어·이력·비교 등) |
| 메타 | `execute_tool` | 전문 도구 프록시 실행 |

### `legal_research` task 8종

| task | 설명 |
|------|------|
| `full_research` (기본) | 종합 리서치 (AI검색 → 법령 → 판례 → 해석). `customs`/`action_plan` 시나리오 확장 |
| `law_system` | 법체계 분석 (3단비교, 위임구조). `delegation`/`impact` 확장 |
| `action_basis` | 처분 근거 확인 (허가·인가·처분). `penalty` 확장 |
| `dispute_prep` | 쟁송 대비 (불복·소송·심판) |
| `amendment_track` | 개정 추적 (신구대조, 연혁). `timeline`/`time_travel` 확장 |
| `ordinance_compare` | 조례 비교 (상위법 → 전국 조례). `compliance` 확장 |
| `procedure_detail` | 절차·비용·서식 안내. `manual` 확장 |
| `document_review` | 계약서·약관 리스크 분석 (`text` 필수) |

### `legal_analysis` mode 4종

| mode | 설명 | 필수 파라미터 |
|------|------|---------------|
| `verify_citations` | LLM 환각 방지 — 인용 조문 실존 여부 일괄 검증 | `text` |
| `cite_check` | 판례 생사 확인 — 후속 인용 역추적 + 변경·폐기 감지 (한국형 Citator) | `caseNumber` |
| `applicable_law` | 행위시법 판단 — 시점 적용 버전 + 부칙 경과규정 발췌 | `lawName`, `date` |
| `impact_map` | 조문 영향 그래프 — 인용 판례·해석·자치법규 역방향 탐색 + mermaid | `lawName`, `jo` |

## 워크플로우

### 1단계: OC 키 확인 (필수)

`korean-law` MCP는 법제처 Open API OC 키가 사용자마다 필요하다 (공용키 모덜 아님).

```
IF KOREAN_LAW_OC 미설정 (또는 .mcp.json URL 의 ?oc= 이 빈 값):
  "법령 조회를 위해 법제처 Open API OC 키가 필요합니다.

   발급 방법 (무료, 즉시):
   1. law.go.kr 접속 → 회원가입·로그인
   2. Open API 신청 페이지 → 'Open API 사용 신청'
   3. 신청서 작성 → 인증키(OC) 즉시 발급 (예: honggildong)

   설정 방법:
   - .mcp.json 의 korean-law 항목 URL ?oc=<본인키> 에 보간
   - 또는 환경변수 KOREAN_LAW_OC 등록

   키를 입력해 주세요:"

  → 사용자가 키 입력
  → ${CLAUDE_PLUGIN_DATA}/moai-credentials.env에 KOREAN_LAW_OC 저장
  → Step 2로 진행
```

> 사내망·폐쇄망 환경에서 법제처 API 인증서 검증 이슈가 있으면 `LAW_API_PROTOCOL=http` 설정을 안내한다 (자세한 설정은 korean-law MCP README 참조).

### 2단계: 요청 유형 분류 및 도구 선택

| 사용자 요청 | 호출 도구 |
|-------------|-----------|
| "근로기준법 제74조 본문" | `search_law` → `get_law_text` |
| "이 답변/계약서 인용 조문 실존 검증" | `legal_analysis(mode=verify_citations)` |
| "이 판례 아직 유효한가" | `legal_analysis(mode=cite_check)` |
| "2023년 당시 도로교통법 제44조" | `legal_analysis(mode=applicable_law)` |
| "민법 제103조 영향 그래프" | `legal_analysis(mode=impact_map)` |
| "관세법 + 관세청 해석례 + FTA 종합" | `legal_research(task=full_research, scenario=customs)` |
| "산업안전보건법 별표1" | `get_annexes` |
| "주택임대차보호법 5단계 안내" | `legal_research(task=full_research, scenario=action_plan)` |
| "근로기준법 신구대조표" | `legal_research(task=amendment_track)` |
| "대법원 판례 검색" | `search_decisions(domain=precedent)` |

### 3단계: 조회·분석 실행

- 법령명 약칭 자동 인식 (`화관법` → `화학물질관리법`, `산안법` → `산업안전보건법` 등 52개 사전 탑재)
- 조문번호 변환 (`제38조` ↔ `003800` 4자리 숫자) 자동 처리
- `search_law` 결과에 `[현행]` / `⚠️[연혁-과거버전]` 라벨로 현행성 가드 (LLM 분법 오답 방지)
- `verify_citations` 결과: ✓(실존) / ✗(없음, 존재 범위 제시) / ⚠(법령명 불명확)
- `[NOT_FOUND]` / `[HALLUCINATION_DETECTED]` 마커로 실패 명시 (LLM 추측 금지 안내 포함)

### 4단계: 결과 정리

- 조문 본문 (조·항·호·목 구조 유지)
- 판례 요약 (판시사항·판결요지·주문 우선, 본문은 축약 제공)
- 인용 검증 결과표 (실존/없음/범위)
- 영향 그래프 (mermaid 코드 — claude.ai에서 시각화)
- 신구대조표 (추가/삭제/변경 분류)
- "이어서 할 수 있는 조회" 후속 제안

## 사용 예시

**예시 1**: "근로기준법 제74조 본문 알려줘"
→ `search_law("근로기준법")` → MST 획득 → `get_law_text(mst, jo="007400")` → 조문 본문 + 위임 구조

**예시 2**: "이 계약서에 인용된 조문 다 실존하는지 검증해줘" (LLM 환각방지)
→ `legal_analysis(mode=verify_citations, text=<계약서 본문>)` → ✓/✗ 결과표 + 존재 범위

**예시 3**: "2023년 5월 당시 도로교통법 제44조가 뭐였어?" (행위시법)
→ `legal_analysis(mode=applicable_law, lawName="도로교통법", date="2023-05-10")` → 시행 중 버전 본문 + 현행 비교 + 부칙 경과규정

**예시 4**: "이 판례 아직 유효해? 2018다248626"
→ `legal_analysis(mode=cite_check, caseNumber="2018다248626")` → 후속 인용 역추적 + 변경·폐기 신호 감지

**예시 5**: "관세법 제38조 + 관세청 유권해석 + FTA 조약 종합해줘"
→ `legal_research(task=full_research, query="관세법 제38조", scenario=customs)` → 법률·시행령·해석례·조약·별표 일괄

## 산출물

- 법령 조문 본문 (현행성 라벨 포함)
- 판례·결정례 검색 결과 및 전문
- 인용 검증 결과표 (LLM 환각 탐지)
- 판례 생사 확인 결과 (변경·폐기 신호)
- 행위시법 판단 결과 (시점 적용 버전 + 부칙 경과규정)
- 조문 영향 그래프 (mermaid)
- 신구대조표
- 5단계 절차 안내 (action_plan)

## 주의사항

**면책 고지: AI 보조 조회이며 전문 법률 자문을 대체하지 않습니다**

- OC 키는 사용자 본인이 발급·보관. 채팅에 원문 붙여넣지 말고 `.mcp.json` 또는 환경변수로만 등록.
- `verify_citations`는 LLM이 지어낸 가짜 조문 탐지에 특화 — ChatGPT/Claude가 작성한 법률 답변을 신뢰하기 전 반드시 검증.
- `cite_check`로 "변경·폐기된 판례를 살아있는 것처럼 인용"하는 사고를 차단. 중요 사안은 변호사 최종 확인.
- `applicable_law` 없이 과거 사안을 현행법으로 판단하면 행위시법 위반 오답 발생 — 반드시 본 도구로 시점 적용 버전 확인.
- 법제처 API가 IP/도메인 등록 요구를 "사용자 정보 검증 실패"로 안내하는 경우, 실제 원인은 User-Agent·Referer 헤더 누락일 수 있음 (v3.5.5+에서 자동 주입되므로 최신 버전 사용 권장).
- 17개 도메인의 판례·결정례 본문은 계단식 축약(`compactBody`)으로 응답 토큰이 최대 74% 절감됨 — 전문이 필요하면 `get_decision_text(full=true)`로 재호출.

## 관련 스킬

- **moai-lawyer:legal-compliance-check**: 규제 준수 점검·ESG 보고 (현행 법령 근거는 본 스킬에서 조회 후 연계)
- **moai-lawyer:legal-legal-risk**: 법적 리스크 분석·IP 전략·법령 변화 영향 분석 (현행 원문·개정 추적·행위시법은 본 스킬에서 연계)
- **moai-lawyer:legal-contract-review**: 계약서 검토·이용약관 작성 (계약서에 인용된 조문 검증은 본 스킬 `verify_citations`)
- **moai-lawyer:legal-patent-search** / **moai-lawyer:legal-patent-analyzer**: 특허·상표·디자인 (KIPRIS, 본 스킬과 데이터 소스 상이)
- **moai-lawyer:legal-iros-registry-automation**: 대법원 등기부등본 (iros, 본 스킬과 데이터 소스 상이)
- **moai-lawyer:legal-mfds-safety**: 식약처 규제 (식약처 소스, 본 스킬과 데이터 소스 상이)
- **moai-lawyer:legal-nda-triage**: NDA 비밀유지계약 전문 검토
- **moai-coworker:ai-slop-reviewer** / **moai-writer:korean-humanize**: 서술형 산출물 후처리 체인 (법령 본문·표는 제외)

## 이 스킬을 사용하지 말아야 할 때 (책임 분담)

- **특허·상표·디자인 검색·분석** → `moai-lawyer:legal-patent-search` / `moai-lawyer:legal-patent-analyzer` (KIPRIS 소스)
- **계약서·이용약관·개인정보처리방침 작성·검토** → `moai-lawyer:legal-contract-review` (다만 계약서 인용 조문 검증은 본 스킬)
- **규제 준수·내부 감사·ESG 보고** → `moai-lawyer:legal-compliance-check` (현행 법령 근거 조회만 본 스킬 연계)
- **법적 리스크 평가·IP 포트폴리오 전략·법령 변화 영향 분석** → `moai-lawyer:legal-legal-risk` (현행 원문·개정 추적·행위시법은 본 스킬 연계)
- **대법원 등기부등본 발급·조회** → `moai-lawyer:legal-iros-registry-automation`
- **식약처 규제·안전 검사** → `moai-lawyer:legal-mfds-safety`
- **NDA 비밀유지계약 검토** → `moai-lawyer:legal-nda-triage`
- **실제 법적 분쟁·소송 대응** → 반드시 전문 변호사에게 의뢰
