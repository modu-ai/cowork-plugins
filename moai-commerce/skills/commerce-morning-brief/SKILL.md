---
name: commerce-morning-brief
description: |
  [책임 경계] MCP dashboard_morning_brief 호출로 매장 운영 데이터(어제 주문·신규 문의·트렌드·ROAS) 1개 호출 통합 요약 전담. 페어 moai-business:daily-briefing(외부 뉴스·웹 정보)와 명확히 구분 — 본 스킬은 MCP 매장 운영 데이터, 페어는 외부 뉴스·시장 정보.
  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  "아침 브리핑 해줘", "오늘 매장 현황 보여줘", "어제 주문 몇 개야", "ROAS 확인해줘", "매장 대시보드 요약", "아침에 매장 상황 한눈에 보기", "daily brief", "모닝 브리핑".
  ai-slop-reviewer 체이닝 제외 (MCP 매장 운영 숫자·데이터 1줄 통합 스킬).
  v2.3.0 신규 (Wave 3 — Day 1 S4·S5 라이브 시연).
user-invocable: true
version: 2.5.0
---

# 커머스 아침 브리핑

## 개요

`dashboard_morning_brief` MCP 도구를 1회 호출하여 어제 주문·신규 문의·트렌드·ROAS를 통합 요약합니다. 수기 30분 → 30초 충격을 실현하는 Day 1 라이브 시연 핵심 스킬입니다 (PDF §4.3 S4 14:25–14:45, REQ-SETUP-004).

**시연 매핑**
- Day 1 S4 14:25–14:45: 강사 라이브 충격 시연 (수기 30분 → 30초)
- Day 1 S5 15:30–15:45: 수강생 실습 (본인 매장 ID로 직접 호출)
- 강의 후: 매일 아침 1회 호출 루틴으로 정착

**합격 기준 (PDF §4.4 ④)**
페르소나 톤 기준 1줄 요약 + ai-slop 후처리 + 본인 폴더 .md 저장 확인.

---

## 트리거 키워드

아침 브리핑, 모닝 브리핑, 매장 현황, 어제 주문, 신규 문의, ROAS 확인, dashboard_morning_brief, 매장 대시보드, daily brief, 30초 브리핑

---

## 워크플로우

### 입력 슬롯

| 슬롯 | 필수 여부 | 기본값 | 설명 |
|------|-----------|--------|------|
| `seller_id` | 필수 | 없음 | 셀러 매장 ID (Cowork 연결 매장) |
| `date` | 선택 | 어제 날짜 (자동) | 조회 기준 날짜 (YYYY-MM-DD) |
| `persona_tone` | 선택 | 페르소나 기본값 | CLAUDE.md에 설정된 페르소나 톤 적용 |

### MCP 호출

```
MCP: dashboard_morning_brief
입력: { seller_id: "[매장_ID]", date: "[어제_날짜]" }
출력: 어제 주문 + 신규 문의 + 트렌드 + ROAS 4개 영역 통합 요약
```

### 처리 체인

1. `dashboard_morning_brief` MCP 1회 호출
2. 4개 영역 데이터 수신 (주문·문의·트렌드·ROAS)
3. 페르소나 톤 적용하여 1줄 요약 생성
4. `moai-core:ai-slop-reviewer` 자동 체이닝 (AI 패턴 후처리)
5. 결과 .md 파일로 저장 (본인 폴더)

### MCP Phase 1 미출시 상태 (REQ-SETUP-007)

MoAI eCommerce MCP Phase 1이 미출시 상태일 때:

> 현재 MoAI eCommerce MCP Phase 1은 출시 준비 중입니다.  
> 강사 사전 녹화 영상(5분)을 함께 시청해 주세요.  
> 수강생 베타 테스터 우선 배정 신청 가능합니다.

---

## 사용 예시

**예시 1 — 기본 호출**
> "오늘 아침 브리핑 해줘"

```
MCP dashboard_morning_brief 호출 → 어제 날짜 자동 설정
출력:
[2026-05-11 아침 브리핑]
주문: 신규 32건 (전일 대비 +8%) · 문의: 5건 미답변 · 트렌드: "여름 원피스" 급상승 · ROAS: 3.2
→ ai-slop-reviewer 후처리 → 본인 폴더 morning-brief-20260511.md 저장
```

**예시 2 — 특정 날짜 지정**
> "지난주 월요일 브리핑 보여줘"

```
MCP dashboard_morning_brief 호출 → date: "2026-05-05"
출력: 해당 날짜 주문·문의·트렌드·ROAS 통합 요약
```

**예시 3 — 수강생 실습 (Day 1 S5)**
> "내 매장 ID는 shop_abc123이야, 브리핑 해줘"

```
MCP dashboard_morning_brief 호출 → seller_id: "shop_abc123"
출력: 수강생 본인 매장 어제 현황 1줄 요약 → .md 저장
```

---

## 출력 형식

```markdown
# [날짜] 아침 브리핑

**주문**: [신규 N건] (전일 대비 ±N%)
**문의**: [미답변 N건] / 전체 N건
**트렌드**: "[키워드]" [상승/하락/유지]
**ROAS**: [N.N]

> [페르소나 톤 적용 1줄 요약]
```

저장 경로: `본인_폴더/morning-brief-YYYYMMDD.md`

---

## 합격 기준 (PDF §4.4 ④)

- 페르소나 톤 기준 1줄 요약 포함
- ai-slop-reviewer 후처리 통과
- 본인 폴더에 .md 파일 저장 확인
- 응답 시간: 30초 이내 (수기 30분 대비 충격 검증, PDF §3.1)
- 4개 영역 (주문·문의·트렌드·ROAS) 모두 포함

---

## 관련 스킬

- `moai-core:mcp-connector-setup` — 선행 조건: 4커넥터 인증 완료 필요
- `moai-commerce:commerce-order-summary` — 채널 통합 신규 주문 상세 (본 스킬 주문 요약의 상세 버전)
- `moai-commerce:commerce-integrated-strategy` — 브리핑 데이터 기반 전략 수립

---

## 이 스킬을 사용하지 말아야 할 때

- 외부 뉴스·시장 트렌드·경쟁사 정보가 필요한 경우 → `moai-business:daily-briefing` 사용
- 채널별 신규 주문 목록 상세 내역이 필요한 경우 → `moai-commerce:commerce-order-summary` 사용
- 광고 캠페인 성과 분석 심층 리포트가 필요한 경우 → 별도 광고 분석 스킬 사용
- MCP 커넥터 인증이 완료되지 않은 경우 → `moai-core:mcp-connector-setup` 먼저 실행
